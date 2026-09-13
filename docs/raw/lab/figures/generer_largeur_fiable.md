# generer_largeur_fiable.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/raw/lab/figures/generer_largeur_fiable.py`, dans l'ordre du déroulement. Il
fait autorité : toute évolution du script doit d'abord être décrite ici.

## Rôle

Répondre par le calcul à la question de
[`../largeur-de-bande-fiable.md`](../largeur-de-bande-fiable.md) : **quelle
longueur de fenêtre donne la bande la plus étroite qui encadre encore les
clôtures à venir ?**

Deux sorties, produites du même balayage :

1. un **relevé console** — pour chaque longueur de fenêtre `n` et chaque horizon
   `h`, la largeur nominale de la bande, la proportion de clôtures futures qu'elle
   contient réellement, et la largeur qu'il **faudrait** lui donner pour en
   contenir 95 % ;
2. **deux figures SVG** — la bande ajustée sur l'étalonnage puis prolongée sur
   l'année hors échantillon, et la courbe de la largeur fiable en fonction de `n`.

Le script est versionné **à côté des figures qu'il produit**, comme
[`generer_figures.py`](../../concept/semestre3/canal/figures/generer_figures.md)
l'est à côté des siennes.

> ⚠️ **Ce script ne rend aucun verdict d'achat ou de vente.** Il mesure la
> fiabilité d'un encadrement et publie des proportions. Aucune règle, aucun seuil
> de décision, aucun conseil en investissement.

## Dépendances

**Aucune.** Le CSV est lu par le module `csv` de la bibliothèque standard, les
régressions et les quantiles sont en Python pur, le SVG est écrit à la main.
`pandas` n'est pas importé — contrairement aux générateurs de `python/`, ce script
n'a besoin d'aucune de ses commodités.

## La donnée d'entrée

Un CSV de `docs/raw/data/quotes/`, dont seules trois colonnes sont lues :
`Date`, `Close` et `Stock Splits`. Ce répertoire est **exclu de git** : le fichier
par défaut se régénère d'un appel.

```bash
python python/import_societe.py MC.PA --debut 2019-01-01 --fin 2026-09-12
```

> ⚠️ **`Close` est ajustée des dividendes et des divisions.** C'est la série que
> la règle **lit**, et c'est la bonne ici : tout ce qui est calculé — pente,
> écart-type résiduel, écart réduit — est invariant d'échelle. Le script
> n'achète rien, il n'a donc pas à retirer les divisions postérieures comme le
> fait le moteur de l'expérience 8.

## Invocation

```bash
python docs/raw/lab/figures/generer_largeur_fiable.py
python docs/raw/lab/figures/generer_largeur_fiable.py --table
python docs/raw/lab/figures/generer_largeur_fiable.py --csv autre.csv --sortie /tmp
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `--csv` | `docs/raw/data/quotes/MC_PA_2019-01-02_2026-09-11.csv` | CSV d'entrée. Colonnes `Date` et `Close` requises. |
| `--debut` | `2019-01-01` | Première séance retenue. |
| `--charniere` | `2024-12-31` | Dernière séance de l'**étalonnage**. Tout ce qui suit est hors échantillon. |
| `--fin` | `2025-12-31` | Dernière séance **affichée**. |
| `--fenetres` | `20,40,60,90,120,180,250,375,500,750,1000,1275` | Longueurs de fenêtre balayées, en séances. |
| `--horizons` | `1,5,20,60,250` | Horizons de projection, en séances. |
| `--ancrages-min` | `100` | En deçà de ce nombre de dates d'ancrage, le couple `(n, h)` n'est pas publié. |
| `--prolonger` | *vide* | Étalonnages **supplémentaires** : des dates de début, séparées par des virgules, qui partagent la **même charnière** et la même série. Chacune produit une bande de plus, et leur présence déclenche la **troisième figure**. |
| `--sortie` | le répertoire du script | Où écrire les SVG. |
| `--table` | absent | Imprime le relevé **et n'écrit aucune figure**. |

> ⚠️ **Les trois bornes de dates sont INCLUSIVES**, `--fin` comprise. C'est
> l'inverse de [`import_societe.py`](../../../../python/import_societe.md), dont le
> `--fin` est exclusif. La divergence est assumée : ici une borne est une date de
> lecture, pas une borne de téléchargement.

## Déroulé d'exécution

### 1. Lecture et contrôle de recevabilité

Les lignes sans `Close` sont **ignorées** — la dernière ligne d'un import récent
en est souvent une. Seules les séances comprises entre `--debut` et `--fin`
incluses sont retenues.

Puis le contrôle d'**opération sur titre** exigé par les invariants du dépôt :
tout saut de clôture supérieur à **50 %** d'une séance à l'autre sans division
déclarée dans `Stock Splits` rend la série **irrecevable** — message sur `stderr`
et **sortie 2**. C'est le contrôle qui attrape la scission de Vivendi au
2024-12-09 ; il ne signale rien sur LVMH.

L'étalonnage est la portion allant de `--debut` à `--charniere` incluse ; le hors
échantillon est ce qui suit, jusqu'à `--fin`.

### 2. La droite ajustée — `ajuster(closes, fin, n)`

Sur les `n` dernières clôtures jusqu'au rang `fin`, avec les rangs
$T_i = i,\ i = 1..n$ :

$$r = \frac{\operatorname{cov}(T, C)}{V_T(n)}, \qquad V_T(n) = \frac{n^2-1}{12},
\qquad \varepsilon_i = C_i - \left(\bar C + r\,(T_i - \bar T)\right)$$

$$\operatorname{VAL} = \bar C + r\left(n - \tfrac{n+1}{2}\right), \qquad
s = \sqrt{\frac{\sum \varepsilon_i^2}{n-2}}$$

Covariance et variance **de population** (`ddof = 0`), comme partout dans le
dépôt. Le $s$ ainsi écrit est identique à celui de
[`generer_graph_canal.py`](../../../../python/generer_graph_canal.md) :
$\sqrt{\tfrac{n}{n-2}\operatorname{VAR}(1-\operatorname{CORR}^2)} =
\sqrt{\tfrac{\sum \varepsilon_i^2}{n-2}}$.

> **C'est ici qu'intervient l'optimisation par moindres carrés, et nulle part
> ailleurs.** Parmi **toutes** les droites, celle-ci est celle qui minimise
> $\sum \varepsilon_i^2$, donc $s$, donc la largeur de la bande à $k$ fixé. La
> largeur la plus étroite **à fenêtre donnée** est acquise dès qu'on ajuste par
> moindres carrés ; ce que le balayage cherche est la fenêtre.

La fonction rend `VAL`, la pente, `s`, `CORR`, la moyenne et les résidus.

### 3. Le balayage — `balayer(...)`

Pour chaque longueur `n` de `--fenetres`, le script ajuste une droite sur
**chaque date d'ancrage possible de l'étalonnage** — toute séance ayant `n`
séances derrière elle, sa propre comprise. Il en retient `VAL`, la pente et `s`,
ainsi que les comptages de résidus dans $\pm 1\,s$ et $\pm 2\,s$ *à l'intérieur de
la fenêtre d'ajustement*, qui servent de témoin.

Puis, pour chaque horizon `h` de `--horizons`, il ne garde que les ancrages
disposant de `h` séances devant eux **sans sortir de l'étalonnage**, et projette
la droite :

$$\widehat C_{t+j} = \operatorname{VAL}_t + r_t\,j, \qquad
z_{t,j} = \frac{C_{t+j} - \widehat C_{t+j}}{s_t}, \qquad j = 1..h$$

Tous les $|z_{t,j}|$ des ancrages retenus sont rassemblés dans un seul échantillon,
d'où sortent quatre grandeurs :

| Grandeur | Définition |
|---|---|
| $\tau_1$ | proportion de $\lvert z\rvert \le 1$ — à comparer à **68,3 %** |
| $\tau_2$ | proportion de $\lvert z\rvert \le 2$ — à comparer à **95,5 %** |
| $k_{95}$ | 95ᵉ centile des $\lvert z\rvert$ : le multiple qu'il **faut** pour contenir 95 % |
| $L(n,h)$ | $k_{95} \times \operatorname{méd}\left(2\,s_t/\operatorname{VAL}_t\right)$, en % du cours |

$L(n,h)$ est **la largeur fiable** : la largeur relative que la bande doit
atteindre pour encadrer réellement 95 % des clôtures à l'horizon `h`. C'est elle
que le balayage minimise, et son minimum désigne la fenêtre retenue.

Le centile suit la convention $(n-1)p$ par interpolation linéaire, celle de
`generer_figures.py` et de `numpy.percentile` par défaut.

Un couple `(n, h)` comptant moins de `--ancrages-min` dates d'ancrage n'est
**pas publié** : il rend `—`. C'est ce qui écarte les fenêtres longues aux
horizons longs — à 1 275 séances d'ajustement et 250 séances de projection,
l'étalonnage ne laisse que six ancrages.

> ⚠️ **Les ancrages se recouvrent massivement.** Deux ancrages voisins partagent
> $n-1$ clôtures, et les $h$ projections d'un même ancrage ne sont pas
> indépendantes entre elles. Les proportions publiées sont **descriptives** : leur
> incertitude est très supérieure à ce que $\sqrt N$ suggérerait, et le script ne
> publie **aucun intervalle de confiance** — il serait faux. C'est la leçon des
> grappes de dates de l'expérience 5, appliquée ici.

### 4. La figure de la bande — `figure_bande(...)`

Une seule bande, ajustée sur **tout l'étalonnage** — la fenêtre la plus longue
disponible —, tracée sur l'affichage entier :

- la zone hors échantillon est **ombrée**, et la droite comme ses quatre bords y
  passent en **pointillé** : ce qui est à gauche de la charnière est un
  ajustement, ce qui est à droite est une **projection** ;
- $\pm 2\,s$ en orange (haut) et vert (bas), $\pm 1\,s$ en violet, la droite
  centrale en gris, et $\pm 3\,s$ dans les mêmes teintes que $\pm 2\,s$ mais en
  **trait fin estompé** — le tiret portant déjà la distinction ajusté/projeté, un
  motif de plus la brouillerait. C'est $\pm 3\,s$ qui fixe l'échelle verticale ;
- les clôtures hors échantillon **sorties de $\pm 2\,s$** sont marquées d'un
  cercle ;
- cartouche : longueur de la fenêtre, pente en %/séance, `CORR`, `s`, largeur en
  € et en %, Durbin-Watson des résidus, proportions dedans **à l'ajustement** puis
  **hors échantillon**, et écart réduit de la dernière clôture.

Durbin-Watson est publié parce que le
[module 4](../../concept/semestre3/canal/04-sorties-de-canal.md#c-lautocorrélation-encore)
l'exige avant toute lecture de persistance :
$\mathrm{DW} = \sum (\varepsilon_i - \varepsilon_{i-1})^2 / \sum \varepsilon_i^2$,
que 2 signale l'indépendance et 0 l'autocorrélation parfaite.

Le cartouche est posé **sous l'aire de tracé**, sur toute la largeur et en deux
colonnes, et non dans un coin du cadre comme le fait `generer_figures.py`.

> ⚠️ **Chercher un coin libre ne marche pas sur une série longue.** Un cours sur
> plusieurs années barre toute la largeur de la figure et en occupe presque toute
> la hauteur : sur l'étalonnage 2022-2024, le tracé couvre `y` 158 à 501 dans un
> cadre de 92 à 524, et **aucun des quatre coins** ne laisse les 158 pixels
> nécessaires. Le meilleur des quatre masquait encore **105 clôtures sur 1 023**.
> Hors du cadre, le recouvrement est **nul par construction**, quelle que soit la
> série — c'est ce qui a fait supprimer la fonction `placer`.

Le cadre fait donc `1200 × 720` : l'aire de tracé occupe `y` 92 à 524, le
cartouche 566 et suivants, la légende les deux dernières lignes.

### 5. La figure du balayage — `figure_balayage(...)`

$L(n,h)$ en ordonnée, les fenêtres en abscisse à pas **constant** (elles ne sont
pas régulièrement espacées : l'axe est catégoriel, et le script le dit sur la
figure). Une polyligne par horizon, le **minimum de chacune marqué d'un disque**
et nommé. Les couples non publiés interrompent la ligne.

### 6. La figure des prolongements — `figure_prolongements(...)`

Écrite **seulement** si `--prolonger` a été passé et s'il reste une zone hors
échantillon. Elle affiche **tout l'historique chargé**, de `--debut` à `--fin`, et
y trace la bande de **chaque** étalonnage :

- **fond ombré à droite de la charnière** : la zone hors échantillon, celle où
  toutes les droites ne sont plus que des extrapolations ;
- **chaque bande ne commence qu'à sa propre date de départ** — celle de 2019 dès
  la première séance affichée, celle de 2022 trois ans plus tard. Une droite
  d'encadrement n'existe pas hors de la fenêtre qui l'a produite, et l'échelle
  verticale ne tient compte de chaque bande que sur l'étendue où elle est tracée ;
- trait **plein** jusqu'à la charnière, **pointillé** au-delà — la même convention
  que la figure de l'étape 4 ;
- une teinte par étalonnage (`TEINTES_ETALONNAGE`), et dans chaque teinte **deux
  droites seulement** : les bords à $\pm 3\,s$, en trait plein, avec un
  remplissage à 7 % entre eux. **Ni $\pm 1\,s$, ni $\pm 2\,s$, ni la droite
  centrale ne sont tracés** — cette figure ne pose qu'une question, « même la bande
  honnête tient-elle ? », et $\pm 3\,s$ est la largeur que le balayage désigne
  comme telle ($k_{95} \simeq 2{,}9$ dès l'horizon d'une séance). Les deux autres
  niveaux restent **chiffrés au cartouche**, qui les publie tous les trois. C'est
  aussi $\pm 3\,s$ qui fixe l'**échelle verticale** ;
- repères verticaux aux changements d'**année** si l'affichage couvre deux ans ou
  plus, aux changements de **mois** en deçà — même bascule que
  [`generer_graph_canal.py`](../../../../python/generer_graph_canal.md), sans
  laquelle un affichage d'un an ne porterait aucun repère ;
- cartouche à **une colonne par étalonnage** : début, nombre de séances, `CORR`,
  pente, $s$, largeur relative, puis les deux proportions **dans la zone affichée**
  et l'écart réduit final.

> ⚠️ **L'échelle verticale contient les clôtures affichées**, y compris celles du
> hors-échantillon — ce sont elles qu'on donne à voir. Aucune borne de bande n'en
> dépend : les droites sont entièrement déterminées par des séances antérieures à
> la première séance affichée. L'invariant « pas de regard en avant » porte sur les
> quantités calculées, pas sur le cadrage.

> **Contrôle gratuit de reproduction.** Une bande obtenue par `--prolonger` et la
> même bande obtenue par un appel séparé à `--debut` doivent rendre des nombres
> **identiques** : les deux chemins lisent des tranches de CSV différentes et ne
> partagent que la formule. Sur MC.PA au 2024-12-31, la bande 2022-2024 rend dans
> les deux cas pente +0,0139 %/séance, `CORR` +0,244, $s$ = 81,89 €, 15,3 % / 47,1 %
> et un écart final de −1,11 s. **Tout désaccord serait un bug de découpage.**

### 7. Écriture

Les deux SVG sont écrits en `newline=""` avec des `\r\n` **explicites**, comme
`generer_figures.py` : la sortie est alors identique sur tout système et une
régénération ne laisse aucun diff. Voir
[`.gitattributes`](../../../../.gitattributes).

Tout texte inscrit dans une figure passe par `ent(texte)`, qui échappe `&`, `<`
et `>` puis convertit **tout caractère non-ASCII en entité numérique**
(`é` → `&#233;`). Les deux autres générateurs écrivent ces entités à la main dans
leurs chaînes ; les faire produire par une fonction garde la source du script
lisible en français, et rend le SVG indépendant de toute déclaration d'encodage.

Les noms sont dérivés du ticker — lui-même dérivé du nom du CSV — **et de
l'étalonnage** :

| Fichier | Contenu |
|---|---|
| `{ticker}-{début}-{charnière}-bande.svg` | la bande de l'étape 4 |
| `{ticker}-{début}-{charnière}-largeur-fiable.svg` | la courbe de l'étape 5 |
| `{ticker}-prolongements-{année}.svg` | les prolongements de l'étape 6, si `--prolonger` |

Le troisième nom porte la **première année hors échantillon**, et non l'étalonnage :
la figure en contient plusieurs, et c'est son cartouche qui les nomme. Ce n'est pas
la zone affichée — celle-ci couvre tout l'historique chargé —, c'est la zone
**jugée**.

> ⚠️ **Les deux noms portent l'étalonnage, y compris celui du balayage.** Le même
> document compare plusieurs charnières — 2019-2024 et 2022-2024 —, et une figure
> qui ne nommerait que le ticker écraserait silencieusement celle de l'étalonnage
> précédent. C'est le seul défaut qu'une régénération ne rendrait pas visible : le
> fichier existe toujours, il décrit simplement autre chose.

## Affichage console

```
{TICKER} — {N} séances, du {début} au {fin}
  étalonnage       {n} séances, du {début} au {charnière}
  hors échantillon {n} séances, du {…} au {fin}

--- dans la fenêtre d'ajustement, pour mémoire ---
    n   largeur nominale   dedans ±1 s   dedans ±2 s

--- horizon {h} séances ---
    n   ancrages   largeur   k95   dedans ±1 s   dedans ±2 s   largeur fiable
  …
  minimum : n = {n}, largeur fiable {L} %

--- la bande affichée : {n} séances, du {début} au {charnière} ---
  droite {val} €   pente {r} %/séance   CORR {corr}   s {s} €
  largeur ± 1 s : {l} € ({p} %)   Durbin-Watson {dw}
  dedans à l'ajustement   ±1 s {a} %   ±2 s {b} %
  dedans hors échantillon ±1 s {c} %   ±2 s {d} %
  écart réduit au {fin} : {e} s

Graphique écrit dans : {chemin}
Graphique écrit dans : {chemin}
```

Un avertissement est émis quand `|CORR|` de la bande affichée est inférieur à
**0,20** : la droite n'explique alors presque rien, et la bande est une
dispersion et non un canal — même seuil que `generer_graph_canal.py`.

## Repères de contrôle — MC.PA, 2019-01-02 → 2025-12-31

Ces nombres sortent des arguments par défaut. **S'ils changent, le document de
[`../largeur-de-bande-fiable.md`](../largeur-de-bande-fiable.md) est faux** —
c'est le contrôle à faire après toute modification du script.

| Grandeur | Valeur |
|---|---|
| Séances lues | 1 794, dont 1 539 d'étalonnage et 255 hors échantillon |
| Bande affichée : pente | +0,0596 %/séance, `CORR` +0,868 |
| Bande affichée : `s` | 81,72 €, soit ± 1 s large de 163,44 € (20,76 %) |
| Durbin-Watson | **0,014** |
| Dedans à l'ajustement | 67,8 % · 94,0 % · **100,0 %** à ± 1, 2, 3 s |
| Dedans hors échantillon | **0,8 %** · **13,3 %** · **29,4 %** à ± 1, 2, 3 s |
| Écart réduit au 2025-12-31 | −2,87 s |

Minimums de largeur fiable, un par horizon :

| Horizon | Fenêtre | $L$ |
|---|---|---|
| 1 | 20 | 10,74 % |
| 5 | 20 | 16,75 % |
| 20 | 60 | 29,80 % |
| 60 | 750 | 45,96 % |
| 250 | 750 | 53,40 % |

Le balayage complet prend une vingtaine de secondes : environ 3,4 millions de
termes de régression et 3,7 millions d'écarts réduits, en Python pur. C'est
assumé — des sommes cumulées rendraient le balayage instantané, au prix d'une
soustraction de grands nombres dont la précision se dégraderait là où le dépôt
contrôle à 10⁻¹¹ près.

### Le second étalonnage

```bash
python docs/raw/lab/figures/generer_largeur_fiable.py \
    --debut 2022-01-01 --charniere 2024-12-31 --fin 2025-12-31
```

| Grandeur | Valeur |
|---|---|
| Séances lues | 1 023, dont 768 d'étalonnage et 255 hors échantillon |
| Bande affichée : pente | +0,0139 %/séance, `CORR` +0,244 |
| Bande affichée : `s` | 81,89 €, soit ± 1 s large de 163,79 € (23,33 %) |
| Durbin-Watson | **0,021** |
| Dedans à l'ajustement | 59,1 % · 98,8 % · **100,0 %** à ± 1, 2, 3 s |
| Dedans hors échantillon | **15,3 %** · **47,1 %** · **81,2 %** à ± 1, 2, 3 s |
| Écart réduit au 2025-12-31 | −1,11 s |

| Horizon | Fenêtre | $L$ |
|---|---|---|
| 1 | 20 | 11,00 % |
| 5 | 20 | 16,75 % |
| 20 | 60 | 29,76 % |
| 60 | 500 | 45,51 % |
| 250 | 375 | 99,75 % |

Les fenêtres de 750 séances et plus ne réunissent jamais 100 ancrages sur 768
séances d'étalonnage : elles rendent `—` à tous les horizons.

### Les prolongements

```bash
python docs/raw/lab/figures/generer_largeur_fiable.py --prolonger 2022-01-01
```

| Grandeur | Valeur |
|---|---|
| Droite 2019-2024, prolongée au 2025-12-31 | **869,51 €** |
| Droite 2022-2024, prolongée au 2025-12-31 | **725,64 €** |
| Écart entre les deux centres | **143,87 €**, soit 88,0 % de la largeur ± 1 s |
| Clôture réelle au 2025-12-31 | **634,65 €** |
| Dedans sur 2025, étalonnage 2019-2024 | 0,8 % · 13,3 % · **29,4 %** à ± 1, 2, 3 s |
| Dedans sur 2025, étalonnage 2022-2024 | 15,3 % · 47,1 % · **81,2 %** à ± 1, 2, 3 s |
| Dedans dans leur ajustement, à ± 3 s | **100,0 %** pour les deux |

La bande 2022-2024 rendue par `--prolonger` doit être **identique**, au chiffre
près, à celle du run autonome ci-dessus : c'est le contrôle de reproduction de
l'étape 6, et il ne coûte rien.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète. |
| `1` | CSV introuvable, colonnes absentes, aucune séance dans la plage, étalonnage trop court pour la plus petite fenêtre, ou `--charniere` hors de `[--debut, --fin]`. |
| `2` | Saut de clôture supérieur à 50 % sans division déclarée : série irrecevable. |

## Cas limites

- **Aucune séance hors échantillon** (`--charniere` = `--fin`) — les figures sont
  écrites, la zone ombrée est vide et les proportions hors échantillon rendent `—`.
- **Une fenêtre plus longue que l'étalonnage** est ignorée en silence dans le
  balayage ; si aucune ne subsiste, sortie `1`.
- **`n < 3`** — refusé à l'analyse des arguments : la division par `n - 2` n'aurait
  pas de sens. Un **horizon**, lui, n'a besoin que d'une séance : le plancher est
  de 3 pour `--fenetres`, de 1 pour `--horizons`.
- **Variance nulle** sur une fenêtre — cours constant : sortie `2`.
- **Régénération répétée** — idempotente à l'octet près, placement du cartouche
  compris.

## Ce que ce script n'est pas

Ce n'est **pas** un des onze utilitaires de `python/`. Il ne prend pas de ticker,
n'appelle pas le réseau, et ne sert qu'au document de `docs/raw/lab/` qu'il
illustre. L'encadrement courant d'une valeur reste le travail de
[`generer_graph_canal.py`](../../../../python/generer_graph_canal.md).
