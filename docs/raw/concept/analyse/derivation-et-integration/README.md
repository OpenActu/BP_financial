# Cours — Dérivation et intégration, jusqu'au jacobien

Cours de calcul différentiel et intégral, du scalaire à $\mathbb R^n$ : dérivée, Taylor,
intégrale, dérivées partielles, **matrice jacobienne**, calcul matriciel des dérivées, intégrales
multiples et changement de variable. Niveau **bac+2**.

## Pourquoi ce cours dans ce dépôt

Un seul objet — la **matrice jacobienne** — y apparaît deux fois, sous deux visages que rien ne
relie à première vue :

| Visage | Où | Ce qu'il fait |
|---|---|---|
| **Approximation linéaire locale** | Dérivation (modules 5 à 7) | $f(x+h)\approx f(x)+J_f(x)\,h$ |
| **Facteur de volume** | Intégration (modules 8 et 9) | $dy=\lvert\det J\rvert\,dx$ |

Ces deux visages sont le **même** : la jacobienne est l'application linéaire qui approche $f$
localement, et le déterminant d'une application linéaire *est* son facteur de dilatation des
volumes. Le cours va d'un bout à l'autre de cette phrase.

**Ce que les autres documents du dépôt en attendent :**

| Où | Ce qui est utilisé | Statut là-bas |
|---|---|---|
| [`modele.md`](../../../modele.md), étapes 1 et 3 | Dérivées partielles, équations normales | Calculées, non justifiées |
| [Statistique § 9.4](../../statistique/mathematique/09-vecteur-gaussien.md) | « Une définition par la densité aurait exigé un calcul de **jacobien** » | Évité |
| [Statistique § 6d.4](../../statistique/mathematique/06d-loi-uniforme.md) | Transformation inverse et PIT | Admises |
| [Statistique § 15.3](../../statistique/mathematique/15-loi-du-chi2.md) | La densité du $\chi^2$ | Donnée |
| [Analyse § 3.3](../convexite/03-criteres-differentiels.md) | Tangente, Hessienne, $H_f\succeq0$ | Suppose la différentiabilité connue |

> 🔑 **La question qui organise le cours.** Quand on remplace une variable par une fonction d'elle
> — $Y=g(X)$ —, deux choses changent : la **valeur** et l'**échelle**. La dérivation mesure la
> première, le jacobien mesure la seconde, et une densité de probabilité est précisément l'objet
> qui a besoin des deux.

## Fil directeur

Une seule idée, déclinée en cinq étages : **dériver, c'est linéariser.**

- en dimension 1, l'application linéaire est un nombre — la dérivée (module 1) ;
- l'erreur de linéarisation se contrôle par Taylor (module 2) ;
- l'opération inverse — reconstituer à partir des pentes — est l'intégrale (modules 3 et 4) ;
- en dimension $n$, l'application linéaire est une **matrice**, la jacobienne (modules 5 à 7) ;
- son **déterminant** est ce que l'intégration voit : un facteur de volume (modules 8 et 9).

## Progression

### Partie 0 — Une variable

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 1 | [La dérivée comme approximation affine](01-derivee-et-approximation-affine.md) | 1 h | $f(a+h)=f(a)+f'(a)h+o(h)$ ; les quatre règles |
| 2 | [Taylor et les approximations qui servent](02-taylor-et-approximations.md) | 1 h | $\log(1+x)$, $(1+y)^{-t}$, et d'où sortent $\sigma^2/2$ et la convexité obligataire |
| 3 | [**L'intégrale et le théorème fondamental**](03-integrale-et-theoreme-fondamental.md) ⭐ | 1 h 15 | Les deux formes du TFA, IPP, changement de variable |
| 4 | [Intégrales généralisées, $\Gamma$, et les moments](04-integrales-generalisees-et-moments.md) | 1 h | $\int e^{-x^2}$, $\Gamma$, existence des moments et queues |

### Partie I — Plusieurs variables

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 5 | [Dérivées partielles, différentielle, gradient](05-derivees-partielles-et-gradient.md) | 1 h | Partielles $\ne$ différentiabilité ; $\nabla f$ et le plan tangent |
| 6 | [**La matrice jacobienne**](06-la-matrice-jacobienne.md) ⭐ | 1 h 15 | $J_{g\circ f}=J_g\,J_f$ ; gradient, Hessienne et inversion locale |
| 7 | [**Le calcul matriciel des dérivées**](07-calcul-matriciel-des-derivees.md) ⭐ | 1 h 15 | Le formulaire, les conventions, $\hat\beta=(X^{\top}X)^{-1}X^{\top}y$ |

### Partie II — Le jacobien en intégration

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 8 | [**Intégrales multiples et facteur de volume**](08-integrales-multiples-et-jacobien.md) ⭐ | 1 h 15 | Fubini, $\lvert\det J\rvert$, et $\int e^{-x^2}=\sqrt\pi$ par les polaires |
| 9 | [Changement de variable et densités](09-changement-de-variable-et-densites.md) | 1 h | $f_Y(y)=f_X(g^{-1}(y))\,\lvert\det J_{g^{-1}}\rvert$ ; log-normale, $\chi^2(1)$, Box–Muller |

**Volume total** : ≈ 10 h, à répartir sur 3 à 4 semaines. Les modules se lisent **dans l'ordre** ;
la partie 0 est révisable rapidement si le calcul à une variable est acquis.

## Parcours

| Objectif | Modules |
|---|---|
| Réviser le calcul à une variable | 1 → 2 → 3 |
| Aller droit au jacobien | 1 → 5 → 6 → 8 |
| Dériver proprement en notation matricielle | 5 → 6 → 7 |
| Comprendre d'où viennent les densités | 3 → 8 → 9 |
| Le strict nécessaire pour lire `modele.md` | 1 → 5 → 7 |

## Les trois modules décisifs

- **Module 6 — La matrice jacobienne.** Celui qui remplace « un tableau de dérivées partielles »
  par un **objet** : l'application linéaire qui approche $f$. La règle de la chaîne y devient un
  produit de matrices, et trois notions du dépôt (gradient, Hessienne, équations normales) s'y
  rangent comme des cas particuliers.
- **Module 7 — Le calcul matriciel.** Celui qui évite d'écrire $n^2$ dérivées partielles à la
  main. Il contient le formulaire, la **convention de disposition** — d'où viennent 90 % des
  erreurs de signe et de transposée — et la dérivation propre des moindres carrés.
- **Module 8 — Le facteur de volume.** Celui qui referme le cours : $\lvert\det J\rvert$ est le
  même jacobien qu'au module 6, vu par l'intégrale. C'est ce qui rend le module 9 — donc toutes
  les densités du [cours de statistique](../../statistique/mathematique/README.md) — calculable.

## Ce que ce cours ne contient pas

- **La topologie et l'analyse réelle rigoureuse** : convergence uniforme, théorie de la mesure,
  intégrale de Lebesgue. L'intégrale est ici celle de Riemann, et les théorèmes d'échange
  limite/intégrale sont cités, non démontrés.
- **Les équations différentielles**, sauf la seule qui sert au dépôt ($\varphi'=-t\varphi$, au
  [§ 7.3 de statistique](../../statistique/mathematique/07-loi-normale-et-ses-transformees.md)).
- **L'optimisation** : elle relève du [cours de convexité](../convexite/README.md), qui utilise les
  dérivées d'ici sans les redémontrer.
- **Les probabilités** : empruntées au [cours de statistique](../../statistique/mathematique/README.md) au
  module 9, jamais construites.

## Ce que ce cours fournit aux autres

| Cours | Ce qu'il reçoit |
|---|---|
| [Analyse — convexité](../convexite/README.md) | La différentiabilité, le gradient, la **Hessienne** dont le module 7 teste la positivité |
| [Statistique](../../statistique/mathematique/README.md) | Le calcul de densité par jacobien (§ 9.4, 15.3), l'intégrale de $E(g(X))$, $\Gamma$ |
| [Algèbre](../../algebre/README.md) | Rien — c'est l'inverse : le **déterminant comme volume** y est établi, et sert au module 8 |
| [`modele.md`](../../../modele.md) | Les équations normales, obtenues en trois lignes au § 7.5 |

## Outillage

```bash
pip install numpy scipy matplotlib
```

Chaque module se conclut par une vérification numérique. En calcul différentiel, la vérification
la plus utile est la **différence finie centrée** :

$$\frac{\partial f}{\partial x_j}(x)\;\approx\;\frac{f(x+he_j)-f(x-he_j)}{2h},\qquad h\approx10^{-6}$$

Elle prend trois lignes, détecte immédiatement une transposée oubliée, et devrait être écrite
**avant** de faire confiance à toute dérivée matricielle calculée à la main.

## Notations retenues dans tout le cours

| Symbole | Sens |
|---|---|
| $f'(a)$, $\mathrm df_a$ | Dérivée en $a$ ; différentielle (application linéaire) |
| $o(h)$, $O(h^2)$ | Négligeable devant $h$ ; dominé par $h^2$ |
| $\partial_j f=\frac{\partial f}{\partial x_j}$ | Dérivée partielle |
| $\nabla f(x)$ | Gradient — vecteur **colonne** de $\mathbb R^n$ |
| $J_f(x)$ | Matrice jacobienne, $m\times n$, $(J_f)_{ij}=\partial f_i/\partial x_j$ |
| $H_f(x)$ | Matrice hessienne, $n\times n$, $(H_f)_{ij}=\partial^2f/\partial x_i\partial x_j$ |
| $\lvert\det J\rvert$ | Facteur de dilatation des volumes (modules 8 et 9) |
| $\int_a^b$, $\iint_D$ | Intégrale simple, intégrale double |
| $\Gamma(s)$ | $\int_0^{+\infty}t^{s-1}e^{-t}\,dt$ |
| $X$, $y$, $\hat\beta$ | Matrice de plan d'expérience, réponse, estimateur des moindres carrés |

⚠️ **Convention de disposition.** Le gradient est une **colonne**, la jacobienne a une **ligne par
composante de $f$** et une **colonne par variable**. Pour $f$ scalaire, $\nabla f=(J_f)^{\top}$.
Cette convention est fixée une fois pour toutes au [§ 7.1](07-calcul-matriciel-des-derivees.md) —
et c'est la seule chose à ne pas changer en cours de calcul.

## Références

| Usage | Référence |
|---|---|
| Cours français complet | J.-M. Monier, *Analyse MP*, Dunod — chapitres calcul différentiel et intégrales multiples |
| Calcul matriciel, la référence | Petersen & Pedersen, *The Matrix Cookbook* (gratuit, PDF) |
| Rigoureux et lisible | Rudin, *Principles of Mathematical Analysis* — ch. 5, 6, 9, 10 |
| Orienté statistique | Magnus & Neudecker, *Matrix Differential Calculus with Applications in Statistics* |
| Gratuit, visuel | *MIT 18.02 Multivariable Calculus* — ocw.mit.edu |
