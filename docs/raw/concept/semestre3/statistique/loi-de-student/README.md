# Cours — La loi de Student

Cours complet sur la loi de Student, de sa construction théorique à son emploi en
régression linéaire. Rédigé pour un niveau **bac+2 en statistique**.

## Pourquoi ce cours dans ce dépôt

Le document [`modele.md`](../../../../modele.md) établit, de façon purement **déterministe**, les
estimateurs de tendance $r_{\min}$ et $v_0$ d'une série chronologique, ainsi que la variance
résiduelle minimale $\operatorname{Var}(\beta)_{\min}=\operatorname{Var}(V)(1-\rho^2)$.

Ces résultats sont des **identités algébriques** : elles sont vraies sur n'importe quels $n$
points, sans aucun modèle probabiliste. Elles ne permettent donc pas de répondre à la seule
question qui compte pour décider :

> La tendance $r_{\min}$ que je viens de calculer est-elle **réelle**, ou n'est-elle que
> le produit du hasard d'échantillonnage ?

Répondre exige d'ajouter un modèle génératif, et la loi qui en sort est **la loi de Student**.
Ce cours en fait le tour, du problème initial jusqu'au test sur la pente d'une régression.

## Fil directeur

Student n'est pas une loi de plus dans un catalogue : c'est **la réponse à un problème précis**,
celui de l'écart-type inconnu. Le cours est construit pour que ce problème soit **posé avant**
que la solution n'apparaisse.

## Principe pédagogique

Chaque module se conclut par une **simulation à écrire soi-même**. La loi de Student est un objet
où l'intuition trompe — queues épaisses, degrés de liberté, variance infinie — et la simulation
est le seul garde-fou fiable à ce niveau. Les corrigés sont donnés, mais la valeur est dans
l'écriture, pas dans la lecture.

## Prérequis — les deux cours amont

Ce cours ne se suffit pas à lui-même, et c'est délibéré : ce qui n'est pas propre à Student a été
sorti dans deux cours autonomes.

| Cours | Durée | Ce qu'il apporte ici |
|---|---|---|
| [**Algèbre linéaire euclidienne**](../../../semestre1/algebre/README.md) | 7 h 30 | Projection, orthogonalité, $\mathbb R^n=F\oplus F^\perp$, degrés de liberté comme **dimension** |
| [**Statistique mathématique**](../../../semestre2/statistique/mathematique/README.md) | 32 h | Loi normale, vecteur gaussien, TCL, loi du $\chi^2$, **Fisher–Cochran**, intervalle de confiance |

Le [module 0](00-mise-a-niveau.md) ci-dessous est un **auto-diagnostic** : il dit lesquels de ces
modules amont vous devez traiter, et lesquels vous pouvez sauter.

⚠️ **Trois modules du cours de statistique sont indispensables**, quel que soit votre niveau, car
ce cours-ci les utilise sans les redémontrer :

- [**Module 15 — La loi du $\chi^2$**](../../../semestre2/statistique/mathematique/15-loi-du-chi2.md) : la loi de $S^2$ ;
- [**Module 16 — Fisher–Cochran**](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md) ⭐ : le
  point de bascule — $\bar X\perp\!\!\!\perp S^2$, sans quoi la construction du module 4 est
  impossible ;
- [**Module 18 — L'intervalle de confiance**](../../../semestre2/statistique/mathematique/18-intervalle-de-confiance.md) : la
  maquette que le module 5 transpose telle quelle.

## Progression

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 0 | [Mise à niveau et auto-diagnostic](00-mise-a-niveau.md) | 2 h | Feu vert ou révision ciblée |
| 1 | [Le problème que Student résout](01-le-probleme.md) | 2 h | Simulation « pourquoi 1,96 ne marche pas » |
| — | *Outils : [loi du $\chi^2$](../../../semestre2/statistique/mathematique/15-loi-du-chi2.md) et [Fisher–Cochran](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md)* | *3 h 30* | *→ cours de statistique* |
| 4 | [Construction et propriétés de Student](04-construction-et-proprietes.md) | 3 h | Table de quantiles reconstruite |
| 5 | [Inférence sur une moyenne](05-inference-sur-une-moyenne.md) | 4 h | IC et test à une population |
| 6 | [Comparaison de deux moyennes](06-comparaison-de-deux-moyennes.md) | 4 h | Welch vs apparié vs poolé |
| 7 | [**Student en régression**](07-student-en-regression.md) ⭐ | 4 h | `modele.md` complété par son test |
| 8 | [**Robustesse, limites, alternatives**](08-robustesse-et-limites.md) ⭐ | 3 h | Savoir quand ne PAS l'utiliser |
| 9 | [Synthèse et arbre de décision](09-synthese.md) | 2 h | Fiche récapitulative d'une page |

**Volume total** : ≈ 24 h pour ce cours seul, ≈ 63 h 30 avec les deux cours amont.

> ℹ️ **La numérotation saute de 1 à 4.** Les anciens modules 2 (loi du $\chi^2$) et 3
> (Fisher–Cochran) ont été versés au [cours de statistique](../../../semestre2/statistique/mathematique/README.md), dont ils
> sont les [modules 15](../../../semestre2/statistique/mathematique/15-loi-du-chi2.md) et [16](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md). Les
> numéros des modules restants n'ont **pas** été décalés, afin que
> toutes les références internes du cours (« le module 7 », « le module 8 ») restent valables.

## Le module décisif

- **Module 8 — Robustesse.** Celui dont l'absence coûte le plus cher en pratique. C'est lui qui
  explique pourquoi un test de tendance appliqué naïvement à une série boursière rejette à tort
  dans **73 % des cas sur 24 points, et 92 % sur 250** — alors que le risque annoncé est de 5 %.

> ⭐ Le module réellement pivot de l'édifice, [Fisher–Cochran](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md),
> est désormais dans le cours de statistique. Les modules 4 à 7 en découlent presque
> mécaniquement ; sans lui, ils restent des recettes. Si vous ne deviez en approfondir qu'un
> seul, c'est celui-là — et il n'est plus ici.

## Outillage

R (`t.test`, `lm`, `qt`) ou Python (`scipy.stats`, `statsmodels`). Les corrigés de ce cours sont
en **Python**, pour rester cohérents avec `import_societe.py`.

```bash
pip install numpy scipy statsmodels matplotlib
```

> ⚠️ Écrivez les simulations **vous-même** plutôt que d'appeler les fonctions toutes faites.
> `scipy.stats.ttest_1samp` donne le bon résultat sans rien enseigner ; reconstruire la
> statistique à la main est ce qui fait passer le cours de la lecture à la compréhension.

## Notations retenues dans tout le cours

| Symbole | Sens |
|---|---|
| $n$ | Taille de l'échantillon |
| $\nu$ (ou `df`) | Degrés de liberté |
| $\mu,\ \sigma^2$ | Espérance et variance **théoriques** (paramètres inconnus) |
| $\bar X,\ S^2$ | Moyenne et variance **empiriques** (statistiques calculables) |
| $\mathcal T(\nu)$ | Loi de Student à $\nu$ degrés de liberté |
| $t_{\nu;\,p}$ | Quantile d'ordre $p$ de $\mathcal T(\nu)$ |
| $\perp\!\!\!\perp$ | Indépendance de deux variables aléatoires |

> ⚠️ **Divergence de convention avec `modele.md`.** Ce document-là normalise les moments par
> $n$ (moments de population). Le présent cours utilise, pour la variance d'échantillon,
> le diviseur $n-1$ :
> $$S^2=\frac{1}{n-1}\sum_i (X_i-\bar X)^2$$
> Ce n'est pas une incohérence mais un **changement de finalité** : le diviseur $n-1$ rend
> l'estimateur sans biais, ce qui n'a de sens que dans un cadre probabiliste. Le
> [module 16 du cours de statistique](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md) explique précisément
> d'où vient ce $n-1$, et le module 7 fait le pont entre les deux conventions.

## Références

| Usage | Référence |
|---|---|
| Cours général, français | G. Saporta, *Probabilités, analyse des données et statistique*, Technip |
| Théorie rigoureuse | Casella & Berger, *Statistical Inference* — ch. 5 pour Fisher–Cochran |
| Concis et moderne | Wasserman, *All of Statistics* |
| Régression | Faraway, *Linear Models with R* ; Sheather, *A Modern Approach to Regression* |
| Gratuit et accessible | *OpenIntro Statistics* — openintro.org |
| Source historique | Student (W. S. Gosset), *The probable error of a mean*, Biometrika, 1908 |
