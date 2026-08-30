# Cours — Analyse

Deux cours autonomes, à lire dans cet ordre si les deux sont nouveaux : le calcul différentiel et
intégral fournit les outils (dérivée, gradient, hessienne, intégrale), la convexité les utilise
pour démontrer des inégalités et garantir des minima.

| # | Cours | Modules | Volume | Ce qu'on en sort |
|---|---|---|---|---|
| 1 | [**Dérivation et intégration, jusqu'au jacobien**](../semestre1/analyse/derivation-et-integration/README.md) | 9 | 10 h | Taylor, TFA, **matrice jacobienne**, calcul matriciel, changement de variable |
| 2 | [**La convexité**](../semestre1/analyse/convexite/README.md) | 9 | 10 h | Jensen, minimisation convexe, $H_f\succeq0$, mesures de risque |

**Volume total** : ≈ 20 h.

## Pourquoi deux cours et non un seul

Ils répondent à deux questions différentes, et l'un peut se lire sans l'autre :

| | Dérivation et intégration | Convexité |
|---|---|---|
| Question | **Comment** varie une fonction, et comment la reconstruire | **Dans quel sens** penche-t-elle |
| Objet central | La matrice **jacobienne** | L'inégalité de la **corde** |
| Nature | Calculatoire | Structurelle |
| Ce qu'il donne au dépôt | Les densités, les équations normales, $\Gamma$ | Jensen, l'unicité des optima, la cohérence des mesures de risque |

## Ce qui circule entre eux

- La **tangente sous le graphe** ([convexité § 3.3](../semestre1/analyse/convexite/03-criteres-differentiels.md)) est
  une inégalité sur le reste de Taylor d'ordre 1
  ([dérivation § 2.1](../semestre1/analyse/derivation-et-integration/02-taylor-et-approximations.md)).
- La **Hessienne** ([dérivation § 6.4](../semestre1/analyse/derivation-et-integration/06-la-matrice-jacobienne.md)) est
  l'objet dont la convexité teste la positivité
  ([convexité § 7.2](../semestre1/analyse/convexite/07-convexite-en-dimension-n.md)).
- Le $\sigma^2/2$ du **drag de volatilité** est un développement d'ordre 2
  ([dérivation § 2.3](../semestre1/analyse/derivation-et-integration/02-taylor-et-approximations.md)) dont la convexité
  donne le **signe** ([convexité § 5.3](../semestre1/analyse/convexite/05-jensen-probabiliste.md)).
- Les **moindres carrés** sont dérivés au
  [§ 7.5 de dérivation](../semestre1/analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md) et
  **prouvés minimaux** au [§ 6.4 de convexité](../semestre1/analyse/convexite/06-minimisation-convexe.md).

## Parcours courts

| Objectif | Chemin |
|---|---|
| Lire [`modele.md`](../../modele.md) sans trou | dérivation 1, 5, 7 → convexité 2, 3, 6 |
| Comprendre les biais d'estimation | dérivation 1, 2 → convexité 3, 4, 5 |
| Optimiser un portefeuille | dérivation 5, 6, 7 → convexité 1, 6, 7, 8 |
| D'où viennent les densités | dérivation 3, 8, 9 |

## Ce que ces cours empruntent aux autres

| Cours | Ce qu'il fournit |
|---|---|
| [Algèbre linéaire](../semestre1/algebre/README.md) | Produit scalaire, projection, **déterminant comme volume**, $\Sigma$ matrice de Gram |
| [Statistique](../semestre2/statistique/mathematique/README.md) | L'espérance et ses règles, la loi normale — empruntées à partir de Jensen probabiliste |

🏠 [Sommaire général](README.md)
