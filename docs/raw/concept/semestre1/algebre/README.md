# Cours — Algèbre linéaire euclidienne dans $\mathbb R^n$

Cours dédié à la géométrie de $\mathbb R^n$ : espace vectoriel, produit scalaire, orthogonalité,
projection, dimension. Rédigé pour un niveau **bac+2**, entièrement **déterministe** — aucune probabilité
n'y intervient.

## Pourquoi ce cours dans ce dépôt

Toutes les quantités manipulées par [`modele.md`](../../../modele.md) et par
`import_societe.py` — moyenne, variance, covariance, corrélation — sont des **objets
géométriques déguisés** :

| Ce que le code calcule            | Ce que c'est réellement                         |
| --------------------------------- | ----------------------------------------------- |
| `E_20` — moyenne glissante        | Une **projection** sur la direction $\mathbf 1$ |
| `VAR_20` — variance glissante     | Un **carré de longueur**                        |
| `CORR_20` — corrélation glissante | Un **cosinus d'angle**                          |
| Le diviseur $n-1$                 | Une **dimension**, pas une convention           |

Ce cours établit ce dictionnaire et les théorèmes qui le soutiennent. Il était initialement un
module de remédiation unique du [cours sur la loi de Student](../../semestre3/statistique/loi-de-student/README.md) ; il en a été extrait et segmenté parce que son contenu est **autonome** et sert au-delà de ce seul usage.

## Fil directeur

Une seule opération — $\langle u,v\rangle=\sum_i u_iv_i$ — et l'examen systématique de son terme croisé $2\langle u,v\rangle$ :
- quand il est **maximal** → Cauchy–Schwarz, l'angle, la corrélation (module 3) ;
- quand il est **nul** → Pythagore, la décomposition de la variance (module 5) ;
- quand on le **rend nul** → la projection, les moindres carrés (module 6) ;
- ce qu'il en **coûte en dimensions** → le noyau, le rang, les degrés de liberté (modules 7 et 8) ;
- et ce qu'il **est**, sur des données → la covariance elle-même (module 11).

Deux modules préalables portent ce sur quoi l'opération s'exerce : le **module 1** définit l'espace
$\mathbb R^n$ et la combinaison linéaire — une série de $n$ nombres vue comme un seul objet —, et le
**module 4** en tire le **sous-espace**, décrit tout entier par une liste finie de vecteurs.

## Progression

| #   | Module                                                                                                | Durée  | Sortie attendue                                            |
| --- | ----------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------- |
| 1   | [L'espace vectoriel $\mathbb R^n$](01-espace-vectoriel.md)                                            | 45 min | Une série de $n$ nombres est **un** objet                   |
| 2   | [Produit scalaire, norme, distance](02-produit-scalaire-et-norme.md)                                  | 45 min | Les trois propriétés, l'identité de développement          |
| 3   | [Cauchy–Schwarz et l'angle](03-cauchy-schwarz-et-angle.md)                                            | 45 min | $\lvert\rho\rvert\le1$ et son cas d'égalité                |
| 4   | [Sous-espaces, $\text{Vect}$ et familles génératrices](04-sous-espaces-et-familles-generatrices.md)   | 45 min | Décrire un espace infini par une liste finie               |
| 5   | [Orthogonalité et théorème de Pythagore](05-orthogonalite-et-pythagore.md)                            | 45 min | Toute décomposition de variance est un Pythagore           |
| 6   | [**La projection orthogonale**](06-projection-orthogonale.md) ⭐                                       | 1 h    | Les moindres carrés sans calcul différentiel               |
| 7   | [Supplémentaire orthogonal, noyau, rang](07-supplementaire-orthogonal-et-dimension.md)                | 45 min | Ce qu'une contrainte linéaire coûte en dimensions          |
| 8   | [**Degrés de liberté : le cas $\text{Vect}(\mathbf 1)$**](08-degres-de-liberte-et-centrage.md) ⭐      | 45 min | Pourquoi $n-1$ — et $n-2$ en régression                    |
| 9   | [Bases orthonormées, isométries, Gram–Schmidt](09-bases-orthonormees-et-isometries.md)                | 1 h    | Base de Helmert, invariance par rotation                   |
| 10  | [**Le dictionnaire géométrique des statistiques**](10-dictionnaire-geometrique-des-statistiques.md) ⭐ | 1 h    | Moyenne = projection, corrélation = cosinus                |
| 11  | [**La covariance comme produit scalaire**](11-covariance-et-produit-scalaire.md) ⭐                    | 1 h 15 | $\Sigma$ est une matrice de Gram — et ce que cela interdit |

**Volume total** : ≈ 9 h 30. Les modules se lisent **dans l'ordre** : chacun n'utilise que les précédents.

## Les quatre modules décisifs

- **Module 6 — La projection.** Le point de bascule. « Le point le plus proche » est la définition des moindres carrés ; tout le calcul différentiel de [`modele.md`](../../../modele.md) en est une reformulation coûteuse.
- **Module 8 — Les degrés de liberté.** Celui qui répond à « pourquoi $n-1$ ? » : les degrés de liberté sont la **dimension** du sous-espace où vit le vecteur des écarts, jamais un compteur de paramètres.
- **Module 10 — Le dictionnaire.** Celui qui rend le reste utilisable : il traduit chaque théorème d'algèbre en énoncé statistique — par **égalité**, non par analogie.
- **Module 11 — La covariance.** Celui qui **démontre** que le dictionnaire a le droit d'exister, et qui en tire le plus de conséquences concrètes : variance d'un portefeuille, positivité d'une matrice de covariance, bornes qu'une corrélation impose aux autres.

## Ce que ce cours ne contient pas

Aucune probabilité. Vecteurs gaussiens, invariance en loi par rotation, indépendance de $\bar X$ et $S^2$ : tout cela suppose un **modèle génératif** et relève du [cours de statistique mathématique](../../semestre2/statistique/mathematique/README.md), qui commence exactement là où celui-ci s'arrête — puis du [cours sur la loi de Student](../../semestre3/statistique/loi-de-student/README.md).

⚠️ Le [module 11](11-covariance-et-produit-scalaire.md) parle de covariance **empirique**, celle d'un jeu de $n$ nombres. La covariance **théorique** $\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)$ de deux variables aléatoires est un autre objet — qui obéit d'ailleurs à la même géométrie, pour la même raison.

## Suite naturelle

| Après ce cours                                  | Module                                                                                                              | Pourquoi                                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Ajouter l'hypothèse gaussienne                  | [Vecteurs gaussiens](../../semestre2/statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md) | Reprend la base de Helmert du module 9 mot pour mot                             |
| La loi de la dispersion                         | [Loi du $\chi^2$](../../semestre2/statistique/mathematique/15-loi-du-chi2.md)                                       | Donne une loi au $\lVert\tilde x\rVert^2$ du module 8                           |
| Le théorème central du cours                    | [Fisher–Cochran](../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md)                         | Est la version probabiliste des modules 8 et 9                                  |
| Tester une pente                                | [Student en régression](../../semestre3/statistique/loi-de-student/07-student-en-regression.md)                     | Rejoue le module 8 avec $\dim F=2$                                              |
| Généraliser la projection                       | [Projection sur un convexe](../analyse/convexite/01-ensembles-convexes.md)                                          | Le module 6 sans hypothèse de linéarité — c'est la convexité qui portait tout   |
| Optimiser un portefeuille                       | [Convexité en dimension $n$](../analyse/convexite/07-convexite-en-dimension-n.md)                                   | Utilise le module 11 : $\Sigma$ est de Gram, donc $w^{\top}\Sigma w$ est convexe |
| Le déterminant comme volume, sous une intégrale | [Le jacobien, facteur de volume](../analyse/derivation-et-integration/08-integrales-multiples-et-jacobien.md)       | Reprend le déterminant-volume et en fait le changement de variables             |

## Outillage

Python. Chaque module se conclut par une simulation courte à écrire soi-même — la géométrie en grande dimension est un domaine où l'intuition planaire trompe (voir S2.1 : deux vecteurs tirés
au hasard en dimension 50 sont presque orthogonaux).

```bash
pip install numpy
```

## Notations retenues dans tout le cours

| Symbole              | Sens                                                                          |
| -------------------- | ----------------------------------------------------------------------------- |
| $n$                  | Dimension de l'espace = taille de l'échantillon                               |
| $\langle u,v\rangle$ | Produit scalaire $\sum_i u_iv_i$                                              |
| $\lVert u\rVert$     | Norme $\sqrt{\langle u,u\rangle}$                                             |
| $\mathbf 1$          | Le vecteur $(1,\dots,1)$                                                      |
| $\tilde x$           | Vecteur centré $x-\bar x\,\mathbf 1$                                          |
| $F^\perp$            | Supplémentaire orthogonal de $F$                                              |
| $P_F$                | Projecteur orthogonal sur $F$                                                 |
| $J$, $M$             | $\mathbf 1\mathbf 1^{\top}$, et la matrice de centrage $I_n-\frac1nJ$         |
| $\ker f$, $H$        | Noyau d'une application linéaire ; l'hyperplan $\text{Vect}(\mathbf 1)^\perp$, $\dim H=n-1$ |
| $\Sigma$, $R$        | Matrices de covariance et de corrélation (module 11)                           |
| $\delta_{jk}$        | Symbole de Kronecker                                                          |

## Références

| Usage                                     | Référence                                                                            |
| ----------------------------------------- | ------------------------------------------------------------------------------------ |
| Cours général, français                   | J. Grifone, *Algèbre linéaire*, Cépaduès — ch. espaces euclidiens                    |
| Orienté statistique                       | G. Saporta, *Probabilités, analyse des données et statistique*, Technip — ch. 1 et 7 |
| Le point de vue géométrique en régression | Faraway, *Linear Models with R* — ch. 2                                              |
| Calcul matriciel                          | Strang, *Linear Algebra and Its Applications* — ch. 3 et 4                           |
| Gratuit                                   | Strang, *MIT 18.06* — ocw.mit.edu                                                    |
