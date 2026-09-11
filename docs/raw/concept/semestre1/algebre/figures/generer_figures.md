# generer_figures.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/raw/concept/semestre1/algebre/figures/generer_figures.py`, dans l'ordre du
déroulement. Il fait autorité : toute évolution du script doit d'abord être
décrite ici.

## Rôle

Tracer la figure du [§ 4.2](../04-sous-espaces-et-familles-generatrices.md) —
le cas $d=2$ de $\text{Vect}$ — qui montre, dans $\mathbb R^3$, que **deux
générateurs donnent un plan ou seulement une droite** selon qu'ils sont
colinéaires ou non.

Le script est versionné **à côté de la figure qu'il produit**, sur le modèle de
[`semestre3/canal/figures/generer_figures.py`](../../../semestre3/canal/figures/generer_figures.md) :
une figure de cours qu'on ne peut pas refaire ne peut pas être corrigée.

## Dépendances

**Aucune.** Produit vectoriel, projection et SVG sont en Python pur.

## Arguments

| Argument | Défaut | Effet |
|---|---|---|
| `--sortie RÉPERTOIRE` | le répertoire du script (`Path(__file__).resolve().parent`) | où écrire le SVG ; créé s'il n'existe pas |

Pas d'invite interactive : sans argument, le script écrit la figure à côté de
lui-même. C'est le mode normal, et il est idempotent.

## Les constantes — la figure entière en découle

| Constante | Valeur | Rôle |
|---|---|---|
| `U` | $(0,\,2,\,1)$ | le premier générateur, **le même dans les deux panneaux** |
| `V_LIBRE` | $(1,\,-1,\,2)$ | le second générateur du panneau de gauche, non colinéaire à `U` |
| `K_COLINEAIRE` | $-1{,}5$ | le panneau de droite prend $v = -1{,}5\,u = (0,\,-3,\,-1{,}5)$ |
| `COEFFICIENTS` | $\{-1,\,0,\,1\}$ | les $\lambda$ et $\mu$ des neuf combinaisons $\lambda u+\mu v$ tracées |
| `BORD` | $1{,}5$ | le morceau de plan dessiné : $\lambda,\mu\in[-1{,}5\,;\,1{,}5]$ |
| `DEMI_DROITE` | $2{,}9$ | le morceau de droite dessiné : $t\,u$, $t\in[-2{,}9\,;\,2{,}9]$ |
| `AXE_LONGUEUR` | $3$ | longueur des demi-axes $e_1, e_2, e_3$ |
| `AZIMUT`, `ELEVATION` | $30°$, $25°$ | direction d'observation |
| `ECHELLE` | $54$ | pixels par unité |

> ⚠️ **Les deux panneaux ne diffèrent que par $v$.** C'est tout le propos : même
> $u$, mêmes coefficients, même nombre de générateurs — seule la colinéarité
> change, et avec elle la dimension.

## Algèbre

| Fonction | Ce qu'elle rend |
|---|---|
| `combinaison(λ, a, μ, b)` | $\lambda a+\mu b$ |
| `scalaire(a, b)` | $\langle a,b\rangle$ |
| `vectoriel(a, b)` | $a\times b$, chaque composante augmentée de `0.0` pour ne jamais afficher `-0.0` |
| `rang(a, b)` | $\dim\text{Vect}(a,b)$ : **2** si $a\times b\neq 0$ (tolérance $10^{-12}$), sinon **1** si $a$ ou $b$ est non nul, sinon **0** |
| `distincts(a, b)` | le nombre de points distincts parmi les neuf $\lambda a+\mu b$, coordonnées arrondies à $10^{-9}$ |

Le critère du produit vectoriel est propre à $\mathbb R^3$ : $a\times b = 0$ si et
seulement si $a$ et $b$ sont colinéaires. Les en-têtes de la figure (« dimension 2 »,
« dimension 1 », « 9 points ») sont **calculés** par ces fonctions, jamais saisis.

Valeurs rendues :

| Panneau | $v$ | $u\times v$ | rang | points distincts |
|---|---|---|---|---|
| gauche | $(1,\,-1,\,2)$ | $(5,\,1,\,-2)$ | 2 | 9 |
| droite | $(0,\,-3,\,-1{,}5)$ | $(0,\,0,\,0)$ | 1 | 9 |

> À droite, les neuf points sont **distincts mais alignés** : $\lambda u+\mu v=(\lambda-1{,}5\,\mu)\,u$,
> et $\lambda-1{,}5\,\mu$ prend neuf valeurs différentes sur $\{-1,0,1\}^2$. Ce
> n'est donc pas une coïncidence de points qui fait perdre une dimension, c'est
> l'alignement.

## Projection

`vers_camera()` rend le vecteur unitaire de l'origine vers l'observateur :

$$d = (\cos\theta\cos\varphi,\ \cos\theta\sin\varphi,\ \sin\theta), \qquad \varphi = 30°,\ \theta = 25°$$

`ecran(p, cx)` est la projection **orthographique** sur le plan orthogonal à $d$,
avec pour axes écran

$$r = (-\sin\varphi,\ \cos\varphi,\ 0), \qquad h = (-\cos\varphi\sin\theta,\ -\sin\varphi\sin\theta,\ \cos\theta)$$

— $r$ vers la droite, $h$ vers le haut, et $r\times h = d$ : le repère est direct.
Le point $p$ va en $\bigl(c_x + 54\,\langle p,r\rangle,\ 372 - 54\,\langle p,h\rangle\bigr)$ ;
l'origine est en $(300, 372)$ à gauche, $(900, 372)$ à droite. Pas de
perspective : deux segments parallèles dans $\mathbb R^3$ restent parallèles à
l'écran, ce qui garde la grille du plan lisible comme une grille.

## Les primitives de tracé

Cadre de **1200 × 650**, fond `#fcfcfb`, un filet vertical en $x=600$ sépare les
panneaux. Couleurs : $u$ en bleu `#2a78d6`, $v$ en orange `#eb6834`, le
**sous-espace engendré en violet** `#8b5cd6` dans les deux panneaux, les axes en
gris `#a9a89e`.

| Fonction | Ce qu'elle fait |
|---|---|
| `nombre(x)` | `-1.5` → `−1,5` : virgule décimale, signe moins U+2212 |
| `texte(...)` · `segment(...)` · `point(...)` | un `<text>`, un `<line>`, un `<circle>` |
| `fleche(p0, p1, couleur)` | un vecteur : segment raccourci de 14 px et pointe triangulaire pleine — **sans `<marker>`**, que certains moteurs de rendu ignorent |
| `nom_vecteur(...)` | le nom du vecteur, en Georgia italique, posé 19 px au-delà de la pointe dans son prolongement |
| `dans_polygone(p, poly)` | vrai si le point écran est dans le polygone **convexe** (bord compris) : tous les produits vectoriels arête × point ont le même signe |
| `axes(cx, normale, plan)` | les trois demi-axes positifs et leurs étiquettes $e_1, e_2, e_3$ ; voir ci-dessous |
| `origine(cx)` | le point noir et le « 0 » |

> ⚠️ **Le « 0 » et les indices des axes sont en chasse fixe, pas en Georgia.**
> Georgia a des chiffres elzéviriens : son « 0 » est un « o », et l'origine y
> devient une lettre.

### Les axes et le plan qui les masque

Sans plan (panneau de droite), les trois demi-axes sont tracés en trait plein.

Avec un plan de normale $n = u\times v$, le demi-axe $e_k$ est **derrière** le
plan si $n_k$ et $\langle n,d\rangle$ sont de signes contraires. Ici
$\langle n,d\rangle \approx 3{,}53 > 0$ et $n = (5,1,-2)$ : **seul $e_3$ passe
derrière.** Pour lui :

1. le segment écran de l'origine à son extrémité est échantillonné en 200 pas ;
2. le plus grand $t$ dont le point reste dans le morceau de plan est retenu —
   l'origine y est toujours, puisque le plan passe par elle ;
3. la part $[0, t]$ est tracée **en tirets** (ligne cachée), la part $[t, 1]$ en
   trait plein ;
4. le demi-axe est émis **avant** le polygone du plan, les autres **après**.

Sur la figure publiée, $e_3$ est entièrement recouvert : il est tout en tirets.

## `ecrire(sortie, nom, lignes)`

Identique à celle du générateur du canal : ferme par `</svg>`, crée le
répertoire, écrit en **`newline=""` avec des `\r\n` explicites**. La sortie est
la même sur tout système, conforme au `*.svg text eol=crlf` du
[`.gitattributes`](../../../../../../.gitattributes), et une régénération ne
laisse aucun diff. Imprime `Graphique écrit dans : <chemin>`.

## La figure

### `entete()`

Titre « 4.2 — Vect(u, v) : un plan, ou seulement une droite », sous-titre
rappelant que $u$ est commun et que les points sont les neuf combinaisons, filet
séparateur.

### `panneau_plan(u, v)` — gauche

Dans l'ordre de superposition :

1. en-tête « v non colinéaire à u → Vect(u, v) est un plan » et, dessous, le
   nombre de points distincts et `rang(u, v)` ;
2. les demi-axes situés derrière le plan ;
3. le **morceau de plan** : le parallélogramme $\{\lambda u+\mu v : \lambda,\mu\in[-1{,}5\,;\,1{,}5]\}$,
   rempli à 10 %, bordé en violet ;
4. sa **grille** : les droites $\lambda = c$ et $\mu = c$ pour $c\in\{-1,0,1\}$, en
   tirets — les deux passant par l'origine sont $\text{Vect}(v)$ et $\text{Vect}(u)$ ;
5. les demi-axes situés devant ;
6. l'étiquette « Vect(u, v) » au-dessus du coin $(\lambda,\mu) = (-1{,}5\,;\,1{,}5)$ ;
7. les **neuf points** $\lambda u+\mu v$ — les nœuds de la grille — et l'étiquette « u + v » ;
8. les flèches $u$ et $v$, leurs noms, l'origine.

Rend `(rang, u × v)`.

### `panneau_droite(u, k)` — droite

$v = k\,u$. Dans l'ordre :

1. en-tête « v = −1,5 u → Vect(u, v) est la droite Vect(u) » et, dessous,
   « λu + μv = (λ − 1,5 μ) u », le nombre de points et le rang ;
2. les trois demi-axes, pleins ;
3. la **droite** $\{t\,u : t\in[-2{,}9\,;\,2{,}9]\}$ en violet, étiquetée
   « Vect(u, v) = Vect(u) » au-dessus de son extrémité droite ;
4. les **neuf points**, tous sur la droite, et l'étiquette « u + v = −0,5 u » ;
5. la flèche $v$ **puis** la flèche $u$ — $u$ par-dessus, bien qu'ici elles
   partent en sens opposés —, leurs noms, l'origine.

Rend `(rang, v)`.

### `figure_vect(sortie)` → `vect-plan-ou-droite.svg`

Assemble les deux panneaux et ajoute le pied, **calculé** à partir des deux rangs :

> deux générateurs dans les deux panneaux, et pourtant dimension 2 à gauche, 1 à droite
> le nombre de générateurs majore la dimension, il ne la donne pas

## Affichage console

```
Graphique écrit dans : …/vect-plan-ou-droite.svg

gauche  u = (0.0, 2.0, 1.0)  v = (1.0, -1.0, 2.0)  u x v = (5.0, 1.0, -2.0)  rang 2  9 points distincts
droite  u = (0.0, 2.0, 1.0)  v = (0.0, -3.0, -1.5)  u x v = (0.0, 0.0, 0.0)  rang 1  9 points distincts
```

**Si le rang de gauche n'est plus 2, ou celui de droite plus 1, la figure
contredit le cours** — c'est le contrôle à faire après toute modification des
constantes.

## Fichiers écrits

Un seul, dans `--sortie` :

| Fichier | Section illustrée |
|---|---|
| `vect-plan-ou-droite.svg` | § 4.2, le cas $d=2$ |

**Toujours écrasé.** Il est suivi par git, et une régénération ne doit produire
**aucun diff**.

## Codes de sortie

`0` dans tous les cas nominaux. Ni entrée ni réseau : les seules erreurs
possibles sont un `--sortie` non inscriptible (`OSError` non rattrapée,
volontairement) et un argument inconnu (`2`, rendu par `argparse`).

## Cas limites

- **`V_LIBRE` colinéaire à `U`** — le panneau de gauche afficherait « dimension 1 »
  sous un titre qui dit « est un plan », et le parallélogramme serait plat. Le
  titre n'est pas conditionné au rang : changer `V_LIBRE` impose de relire la
  figure.
- **Plan vu par la tranche** — si $\langle n,d\rangle$ tend vers $0$, le
  parallélogramme s'aplatit en segment. Avec les constantes publiées, l'angle
  entre la normale et la direction d'observation est d'environ $50°$.
- **Origine hors du morceau de plan** — impossible tant que `BORD > 0` ; c'est ce
  qui garantit que le `max` de `axes` n'est jamais pris sur une suite vide.
- **Régénération répétée** — idempotente à l'octet près.

## Ce que ce script n'est pas

Ce n'est **pas** un utilitaire du dépôt : il ne lit aucune donnée de marché et ne
compte pas parmi les dix scripts de `python/`.
