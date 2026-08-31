# generer_figures.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/raw/concept/semestre3/canal/figures/generer_figures.py`, dans l'ordre du
déroulement. Il fait autorité : toute évolution du script doit d'abord être
décrite ici.

## Rôle

Tracer les trois figures du [module 2](../02-les-trois-largeurs.md) du cours sur
le canal — une par convention de demi-largeur — à partir d'une **série
simulée reproductible**, et imprimer les nombres que le texte du module cite.

Le script est versionné **à côté des figures qu'il produit**, comme les
`journal.py` des expériences le sont à côté de leurs rapports. Sans lui, les
trois SVG seraient des fichiers que personne ne peut refaire ni corriger.

> Le cours publie la recette de la **série** (§ 2.0) ; ce script publie celle du
> **tracé**. Les deux ensemble rendent les figures entièrement vérifiables.

## Dépendances

**Aucune.** La série, la régression, les quantiles et le SVG sont en Python pur.
Conforme à l'invariant du dépôt : `yfinance` est la seule dépendance externe, et
elle n'est pas requise ici.

## Arguments

| Argument | Défaut | Effet |
|---|---|---|
| `--sortie RÉPERTOIRE` | le répertoire du script (`Path(__file__).resolve().parent`) | où écrire les trois SVG ; créé s'il n'existe pas |
| `--stats` | absent | imprime le relevé statistique **et n'écrit aucune figure** |

Il n'y a **pas d'invite interactive** : sans argument, le script écrit les trois
figures à côté de lui-même. C'est le mode normal, et il est idempotent.

## La série — quatre constantes, aucune donnée de marché

| Constante | Valeur | Rôle |
|---|---|---|
| `GRAINE` | `1` | graine du générateur congruentiel, **déclarée dans le cours** |
| `N` | `100` | nombre de pas |
| `DEPART` | `100.0` | $V_0$ |
| `SIGMA` | `1.0` | écart-type d'un incrément |

`uniformes(graine, combien)` — générateur congruentiel linéaire de *Numerical
Recipes*, en entiers 32 bits :

$$x_{k+1} = (1664525\,x_k + 1013904223) \bmod 2^{32}, \qquad u_k = \frac{x_{k+1} + 0{,}5}{2^{32}}$$

Le $+\,0{,}5$ écarte $u = 0$, qui ferait diverger le $\log$ de Box-Muller.

`serie()` — marche aléatoire gaussienne $V_i = V_{i-1} + \sigma z_i$, les $z$
tirés **par paires** (Box-Muller) :

$$r = \sqrt{-2\ln u_{2j}}, \qquad z_1 = r\cos(2\pi u_{2j+1}), \qquad z_2 = r\sin(2\pi u_{2j+1})$$

Rend les **100 valeurs $V_1 \dots V_{100}$**, sans $V_0$. Le garde
`if len(valeurs) <= N` empêche la paire finale d'ajouter un 101ᵉ point.

**Repères de contrôle** — ces trois nombres doivent sortir identiques, sur tout
système et toute version de Python ≥ 3.10 :

| | valeur |
|---|---|
| $V_1$ | 98,8432 |
| $V_{50}$ | 96,6119 |
| $V_{100}$ | 103,2872 |

> ⚠️ **Le processus n'a aucune tendance.** La droite ajustée sur les 100 points
> rend pourtant une pente de $+0{,}12650$ par pas. Tout ce que les figures
> montrent est donc un **artefact de la mesure**, jamais une propriété du monde —
> c'est la raison d'être du choix de série.

## Les trois fonctions de calcul

### `ajuste(v)` → `(a, b, résidus)`

Droite des moindres carrés sur les **rangs 1..n**, pas sur des dates :

$$b = \frac{\operatorname{cov}(t, v)}{\operatorname{var}(t)}, \qquad a = \bar v - b\,\bar t, \qquad e_i = v_i - (a + b\,i)$$

Covariance et variance **de population** (division par $n$) — le rapport est le
même qu'avec $n-1$, et cela reste cohérent avec le `ddof=0` de
[`import_societe.py`](../../../../../../python/import_societe.md). Les deux `zip`
portent `strict=True` : une longueur discordante lèverait `ValueError` au lieu de
tronquer en silence.

### `stats(res)` → `(s, sigma_e, min, max)`

$$s = \sqrt{\frac{\sum e_i^2}{n-2}} \quad\text{(sans biais, 2 paramètres estimés)}, \qquad \hat\sigma_e = \sqrt{\frac{\sum e_i^2}{n}}$$

Le rapport $s/\hat\sigma_e = \sqrt{n/(n-2)}$ vaut **1,010** à $n = 100$ : c'est
l'écart de 1,0 % affiché sur la figure 2.2.

### `centile(tri, p)`

Interpolation linéaire sur une liste **déjà triée**, convention $(n-1)p$ — celle
de `numpy.percentile` par défaut. Si l'indice tombe sur le dernier élément, rend
le dernier élément.

## Les primitives de tracé

Le SVG est écrit à la main, sans bibliothèque, dans un cadre de **1200 × 620**
avec l'aire de tracé en `X0..X1 = 62..1104` et `Y0..Y1 = 74..574`. La palette
reprend celle de
[`generer_graph_decision.py`](../../../../../../python/generer_graph_decision.md)
— `COURS` bleu, `RES` orange (résistance), `SUP` vert (support), `DECISION`
violet pour ce qui est propre à une fenêtre.

| Fonction | Ce qu'elle fait |
|---|---|
| `fr(texte)` | virgule décimale française, et **espaces multiples convertis en `&#160;`** — sans quoi le SVG les fusionne et les colonnes des cartouches se décalent |
| `echelle(*couvre)` | rend `(x, y, bas, haut)` en englobant toutes les valeurs passées, avec une marge de 6 % ; `x` mappe le rang 1..100, `y` la valeur |
| `entete` · `grille` · `polyligne` · `droite` · `bande` | les couches du dessin, dans cet ordre de superposition |
| `occupe(...)` | vrai si la courbe traverse une boîte donnée — échantillonnage de 24 points par segment |
| `placer(...)` | rend le **premier des quatre coins libres** pour un cartouche, sinon celui du bas à gauche |
| `cartouche(lignes, x, y, largeur)` | l'encadré de lecture ; chaque ligne est un triplet `(texte, couleur, gras)` |
| `points(...)` | les disques marquant les points remarquables |

`placer` est la seule qui rende un résultat **dépendant de la série** : si la
courbe change, le cartouche peut migrer d'un coin à l'autre. C'est voulu — un
cartouche posé sur la courbe rendrait la figure illisible.

## `ecrire(sortie, nom, lignes)`

Ferme le SVG par `</svg>`, crée le répertoire au besoin, puis écrit en
**`newline=""` avec des `\r\n` explicites**.

> ⚠️ **Le CRLF est écrit délibérément, pas hérité du système.** Le
> [`.gitattributes`](../../../../../../.gitattributes) fixe `*.svg text eol=crlf`,
> donc un checkout pose du CRLF sur le disque. Un script qui écrirait en
> `newline=None` produirait du LF sous Linux et du CRLF sous Windows : la même
> figure « changerait » selon la machine, pour zéro changement de contenu. Le
> `newline=""` rend la sortie **identique partout**, et une régénération ne
> laisse aucun diff.

Imprime `Graphique écrit dans : <chemin>`, comme les deux générateurs de
`python/`.

## Les trois figures

### `figure_enveloppe(v, sortie)` → `brownien-enveloppe.svg`

Illustre le § 2.1. Ajuste **deux** droites sur la même série : une sur les 100
points, une sur les **20 derniers**. La seconde est réexprimée dans le repère
global (`a20g = a20 - b20 * 80`) pour être tracée aux rangs 81..100 sur la même
échelle. Les deux enveloppes sont les droites décalées de `min(res)` et
`max(res)`.

La fenêtre de 20 est ombrée, les **deux points extrêmes** qui fixent toute la
largeur sont marqués. Le cartouche donne les demi-largeurs **en unités de $s$** —
la seule normalisation qui isole l'effet de $n$, puisque $s$ vaut 2,61 sur 100
pas contre 0,78 sur les 20 derniers.

Rend `(demi-largeur à n=100, demi-largeur à n=20)` = **(2,45 s ; 1,41 s)**.

### `figure_ecart_type(v, sortie)` → `brownien-ecart-type.svg`

Illustre le § 2.2. Bandes $\pm 1\,s$ et $\pm 2\,s$ autour de la droite des 100
points, comptage des points à l'intérieur, marquage de ceux qui sortent de
$\pm 2\,s$.

Rend `(d1, d2, s, sigma_e)` = **(70, 94, 2,6117, 2,5854)**, à comparer aux
68,3 % et 95,5 % attendus sous loi normale.

### `figure_quantile(v, sortie)` → `brownien-quantile.svg`

Illustre le § 2.3. **Trace les résidus, pas les niveaux** — c'est ce qui rend les
bandes horizontales et permet de ne faire varier **qu'une seule chose** d'une
bande à l'autre : le nombre de points.

Les 5ᵉ et 95ᵉ centiles sont calculés sur les 100 résidus, puis sur **trois
fenêtres de 20** (rangs 1–20, 41–60, 81–100) découpées dans les **mêmes**
résidus, issus de la **même** droite. Les $\pm 1{,}645\,s$ gaussiens sont tracés
en tirets pour référence. L'étiquette de chaque fenêtre passe au-dessus ou en
dessous de la bande selon ce que `occupe` trouve de libre.

Rend `(q05, q95, s, fenetres)`. Le rapport $|q_{95}|/|q_{05}|$ vaut **1,13** sur
100 points, mais **3,96 · 0,45 · 0,94** sur les trois fenêtres de 20 — un facteur
9 sur une série **parfaitement symétrique par construction**. Toute cette
asymétrie est du bruit.

## `releve(v)` — le mode `--stats`

Imprime, pour trois découpes (`100 points`, `20 derniers`, `20 premiers`), la
droite ajustée, $s$ et $\hat\sigma_e$, l'enveloppe et sa demi-largeur en $s$, les
comptages à $\pm 1\,s$ et $\pm 2\,s$, les quantiles et l'asymétrie. C'est le
relevé qui a produit les nombres cités par le module ; il permet de les
revérifier sans ouvrir un SVG.

**Aucune figure n'est écrite dans ce mode.**

## Affichage console du mode normal

```
Graphique écrit dans : …/brownien-enveloppe.svg
Graphique écrit dans : …/brownien-ecart-type.svg
Graphique écrit dans : …/brownien-quantile.svg

2.1  demi-largeur  2.45 s sur n = 100,  1.41 s sur n = 20
2.2  70/100 dans +/- 1 s,  94/100 dans +/- 2 s   (s = 2.6117, sigma_e = 2.5854)
2.3  quantiles n = 100 : [-1.55 s ; +1.76 s]   asymetrie 1.13
       rangs 1-20 : [-0.65 s ; +2.59 s]   asymetrie 3.96
       rangs 41-60 : [-1.70 s ; +0.75 s]   asymetrie 0.45
       rangs 81-100 : [-0.72 s ; +0.68 s]   asymetrie 0.94
```

Ces nombres sont exactement ceux du texte du module. **S'ils changent, le cours
est faux** — c'est le contrôle à faire après toute modification du script.

## Fichiers écrits

Trois, dans `--sortie` :

| Fichier | Section illustrée |
|---|---|
| `brownien-enveloppe.svg` | § 2.1 |
| `brownien-ecart-type.svg` | § 2.2 |
| `brownien-quantile.svg` | § 2.3 |

**Toujours écrasés**, jamais empilés. Ils sont suivis par git — ce sont des
illustrations de cours, pas des données de marché régénérables d'un appel
réseau — et une régénération ne doit produire **aucun diff**.

## Codes de sortie

`0` dans tous les cas nominaux. Le script n'a ni entrée ni réseau : les seules
erreurs possibles sont un `--sortie` non inscriptible (`OSError` non rattrapée,
volontairement — un échec d'écriture doit être bruyant) et un argument inconnu
(`2`, rendu par `argparse`).

## Cas limites

- **`N` impair** — Box-Muller produit les normales par paires ; le garde
  `len(valeurs) <= N` coupe la dernière. Le code fonctionne, mais la constante
  vaut 100 et le cours en dépend : **la changer invalide les repères de contrôle
  et les nombres publiés dans le module.**
- **`n < 3`** dans `stats` — division par `n - 2` ; sans objet ici, les fenêtres
  faisant 20 ou 100 points.
- **Résidu nul au dénominateur** — `figure_quantile` divise par `abs(c5)`. Un
  quantile exactement nul lèverait `ZeroDivisionError` ; impossible sur une série
  continue, non gardé.
- **Régénération répétée** — idempotente à l'octet près, `placer` compris.

## Ce que ce script n'est pas

Ce n'est **pas** un utilitaire du dépôt : il ne lit aucun CSV de
`docs/raw/data/quotes/`, ne prend aucun ticker, et ne sert qu'à un module de
cours. Les dix utilitaires restent ceux de `python/`, et l'encadrement des
**vraies** séries est le travail de
[`generer_graph_supp_resistance.py`](../../../../../../python/generer_graph_supp_resistance.md)
et [`generer_graph_decision.py`](../../../../../../python/generer_graph_decision.md).
