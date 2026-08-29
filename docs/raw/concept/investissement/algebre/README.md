# Cours — Algèbre linéaire euclidienne dans $\mathbb R^n$

Cours dédié à la géométrie de $\mathbb R^n$ : produit scalaire, orthogonalité, projection,
dimension. Rédigé pour un niveau **bac+2**, entièrement **déterministe** — aucune probabilité
n'y intervient.

## Pourquoi ce cours dans ce dépôt

Toutes les quantités manipulées par [`modele.md`](../modele/modele.md) et par
`historique_sbf250.py` — moyenne, variance, covariance, corrélation — sont des **objets
géométriques déguisés** :

| Ce que le code calcule | Ce que c'est réellement |
|---|---|
| `E_20` — moyenne glissante | Une **projection** sur la direction $\mathbf 1$ |
| `VAR_20` — variance glissante | Un **carré de longueur** |
| `CORR_20` — corrélation glissante | Un **cosinus d'angle** |
| Le diviseur $n-1$ | Une **dimension**, pas une convention |

Ce cours établit ce dictionnaire et les théorèmes qui le soutiennent. Il était initialement un
module de remédiation unique du [cours sur la loi de Student](../statistique/loi-de-student/README.md) ; il
en a été extrait et segmenté parce que son contenu est **autonome** et sert au-delà de ce seul
usage.

## Fil directeur

Une seule opération — $\langle u,v\rangle=\sum_i u_iv_i$ — et l'examen systématique de son
terme croisé $2\langle u,v\rangle$ :

- quand il est **maximal** → Cauchy–Schwarz, l'angle, la corrélation (module 2) ;
- quand il est **nul** → Pythagore, la décomposition de la variance (module 3) ;
- quand on le **rend nul** → la projection, les moindres carrés (module 4) ;
- ce qu'il en **coûte en dimensions** → les degrés de liberté (module 5) ;
- et ce qu'il **est**, sur des données → la covariance elle-même (module 8).

## Progression

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 1 | [Produit scalaire, norme, distance](01-produit-scalaire-et-norme.md) | 45 min | Les trois propriétés, l'identité de développement |
| 2 | [Cauchy–Schwarz et l'angle](02-cauchy-schwarz-et-angle.md) | 45 min | $\lvert\rho\rvert\le1$ et son cas d'égalité |
| 3 | [Orthogonalité et théorème de Pythagore](03-orthogonalite-et-pythagore.md) | 45 min | Toute décomposition de variance est un Pythagore |
| 4 | [**La projection orthogonale**](04-projection-orthogonale.md) ⭐ | 1 h | Les moindres carrés sans calcul différentiel |
| 5 | [**Supplémentaire orthogonal et dimension**](05-supplementaire-orthogonal-et-dimension.md) ⭐ | 1 h | Pourquoi $n-1$ — et $n-2$ en régression |
| 6 | [Bases orthonormées, isométries, Gram–Schmidt](06-bases-orthonormees-et-isometries.md) | 1 h | Base de Helmert, invariance par rotation |
| 7 | [**Le dictionnaire géométrique des statistiques**](07-dictionnaire-geometrique-des-statistiques.md) ⭐ | 1 h | Moyenne = projection, corrélation = cosinus |
| 8 | [**La covariance comme produit scalaire**](08-covariance-et-produit-scalaire.md) ⭐ | 1 h 15 | $\Sigma$ est une matrice de Gram — et ce que cela interdit |

**Volume total** : ≈ 7 h 30. Les modules se lisent **dans l'ordre** : chacun n'utilise que les
précédents.

## Les quatre modules décisifs

- **Module 4 — La projection.** Le point de bascule. « Le point le plus proche » est la
  définition des moindres carrés ; tout le calcul différentiel de [`modele.md`](../modele/modele.md) en
  est une reformulation coûteuse.
- **Module 5 — La dimension.** Celui qui répond à « pourquoi $n-1$ ? » : les degrés de liberté
  sont la **dimension** du sous-espace où vit le vecteur des écarts, jamais un compteur de
  paramètres.
- **Module 7 — Le dictionnaire.** Celui qui rend le reste utilisable : il traduit chaque théorème
  d'algèbre en énoncé statistique — par **égalité**, non par analogie.
- **Module 8 — La covariance.** Celui qui **démontre** que le dictionnaire a le droit d'exister,
  et qui en tire le plus de conséquences concrètes : variance d'un portefeuille, positivité d'une
  matrice de covariance, bornes qu'une corrélation impose aux autres.

## Ce que ce cours ne contient pas

Aucune probabilité. Vecteurs gaussiens, invariance en loi par rotation, indépendance de
$\bar X$ et $S^2$ : tout cela suppose un **modèle génératif** et relève du
[cours de statistique mathématique](../statistique/mathematique/README.md), qui commence exactement là où
celui-ci s'arrête — puis du [cours sur la loi de Student](../statistique/loi-de-student/README.md).

⚠️ Le [module 8](08-covariance-et-produit-scalaire.md) parle de covariance **empirique**, celle
d'un jeu de $n$ nombres. La covariance **théorique** $\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)$ de
deux variables aléatoires est un autre objet — qui obéit d'ailleurs à la même géométrie, pour la
même raison.

## Suite naturelle

| Après ce cours | Module | Pourquoi |
|---|---|---|
| Ajouter l'hypothèse gaussienne | [Vecteurs gaussiens](../statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md) | Reprend la base de Helmert du module 6 mot pour mot |
| La loi de la dispersion | [Loi du $\chi^2$](../statistique/mathematique/15-loi-du-chi2.md) | Donne une loi au $\lVert\tilde x\rVert^2$ du module 5 |
| Le théorème central du cours | [Fisher–Cochran](../statistique/mathematique/16-theoreme-de-fisher-cochran.md) | Est la version probabiliste des modules 5 et 6 |
| Tester une pente | [Student en régression](../statistique/loi-de-student/07-student-en-regression.md) | Rejoue le module 5 avec $\dim F=2$ |
| Généraliser la projection | [Projection sur un convexe](../analyse/convexite/01-ensembles-convexes.md) | Le module 4 sans hypothèse de linéarité — c'est la convexité qui portait tout |
| Optimiser un portefeuille | [Convexité en dimension $n$](../analyse/convexite/07-convexite-en-dimension-n.md) | Utilise le module 8 : $\Sigma$ est de Gram, donc $w^{\top}\Sigma w$ est convexe |
| Le déterminant comme volume, sous une intégrale | [Le jacobien, facteur de volume](../analyse/derivation-et-integration/08-integrales-multiples-et-jacobien.md) | Reprend le déterminant-volume et en fait le changement de variables |

## Outillage

Python. Chaque module se conclut par une simulation courte à écrire soi-même — la géométrie en
grande dimension est un domaine où l'intuition planaire trompe (voir S2.1 : deux vecteurs tirés
au hasard en dimension 50 sont presque orthogonaux).

```bash
pip install numpy
```

## Notations retenues dans tout le cours

| Symbole | Sens |
|---|---|
| $n$ | Dimension de l'espace = taille de l'échantillon |
| $\langle u,v\rangle$ | Produit scalaire $\sum_i u_iv_i$ |
| $\lVertu\rVert$ | Norme $\sqrt{\langle u,u\rangle}$ |
| $\mathbf 1$ | Le vecteur $(1,\dots,1)$ |
| $\tilde x$ | Vecteur centré $x-\bar x\,\mathbf 1$ |
| $F^\perp$ | Supplémentaire orthogonal de $F$ |
| $P_F$ | Projecteur orthogonal sur $F$ |
| $J$, $M$ | $\mathbf 1\mathbf 1^{\top}$, et la matrice de centrage $I_n-\frac1nJ$ |
| $H$ | L'hyperplan $\text{Vect}(\mathbf 1)^\perp$ des vecteurs centrés, $\dim H=n-1$ |
| $\Sigma$, $R$ | Matrices de covariance et de corrélation (module 8) |
| $\delta_{jk}$ | Symbole de Kronecker |

## Références

| Usage | Référence |
|---|---|
| Cours général, français | J. Grifone, *Algèbre linéaire*, Cépaduès — ch. espaces euclidiens |
| Orienté statistique | G. Saporta, *Probabilités, analyse des données et statistique*, Technip — ch. 1 et 7 |
| Le point de vue géométrique en régression | Faraway, *Linear Models with R* — ch. 2 |
| Calcul matriciel | Strang, *Linear Algebra and Its Applications* — ch. 3 et 4 |
| Gratuit | Strang, *MIT 18.06* — ocw.mit.edu |
