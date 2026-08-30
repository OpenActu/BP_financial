# Cours — Statistique

Deux cours autonomes, à lire dans cet ordre : la statistique mathématique construit tout
l'appareil probabiliste jusqu'à l'intervalle de confiance **à $\sigma$ connu** ; le cours sur la
loi de Student reprend exactement là où le premier s'arrête, au moment où l'on remplace ce
$\sigma$ par la variable aléatoire $S$.

| # | Cours | Modules | Volume | Ce qu'on en sort |
|---|---|---|---|---|
| 1 | [**Statistique mathématique**](../semestre2/statistique/mathematique/README.md) | 25 | 32 h | Loi, moments, transformées, catalogue des lois, TCL, $\chi^2$, Fisher–Cochran, intervalle de confiance |
| 2 | [**La loi de Student**](../semestre3/statistique/loi-de-student/README.md) | 8 | 24 h | Construction de $\mathcal T(\nu)$, inférence à $\sigma$ inconnu, tests, régression, robustesse |

**Volume total** : ≈ 56 h.

## La ligne de partage entre les deux

| | Statistique mathématique | Loi de Student |
|---|---|---|
| Hypothèse sur $\sigma$ | **Connu** — fiction commode | **Estimé** par $S$ — le cas réel |
| Pivot | $\dfrac{\bar X-\mu}{\sigma/\sqrt n}\sim\mathcal N(0,1)$ | $\dfrac{\bar X-\mu}{S/\sqrt n}\sim\mathcal T(n-1)$ |
| Quantile à 95 % | $1{,}96$, **fixe** | $t_{n-1;0{,}975}$, **dépend de $n$** |
| Nature | Construction de l'appareil | Emploi de l'appareil |

> 🔑 **Le second cours existe parce qu'un dénominateur aléatoire change la loi.** C'est le seul
> objet du passage de l'un à l'autre — et il coûte une loi entière.

## Ce qui circule entre les deux

- Le [module 16 — Fisher–Cochran](../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md)
  et le [module 15 — loi du $\chi^2$](../semestre2/statistique/mathematique/15-loi-du-chi2.md) sont les
  **deux outils** de la construction de Student : ce sont d'anciens modules du cours de Student,
  versés au cours de statistique parce qu'ils servent au-delà de lui. C'est ce qui explique le
  saut de numérotation 1 → 4 du second cours.
- L'[intervalle de confiance](../semestre2/statistique/mathematique/18-intervalle-de-confiance.md) et son
  [interprétation](../semestre2/statistique/mathematique/19-interpretation-de-la-confiance.md) sont
  construits à $\sigma$ connu ; Student ne change que la **loi tabulée**, jamais le mécanisme.
- Le [module 0 de Student](../semestre3/statistique/loi-de-student/00-mise-a-niveau.md) est un
  **auto-diagnostic** : il dit précisément quels modules amont traiter avant d'attaquer.

## Parcours courts

| Objectif | Chemin |
|---|---|
| Comprendre d'où vient le $n-1$ | mathématique 7 → 9 → 10 → 11 → 15 → 16 |
| Savoir quand l'approximation normale tient | mathématique 3 → 11 bis → 12 → 13 → 14 |
| Construire et interpréter un intervalle | mathématique 2 → 3 → 8 → 17 → 18 → 19 |
| Tester une pente de régression | mathématique 15 → 16 → Student 4 → 5 → 7 |
| Choisir entre binomiale, Poisson et normale | mathématique 6b → 6c → 11 bis |

## Ce que ces cours empruntent aux autres

| Cours | Ce qu'il fournit |
|---|---|
| [Algèbre linéaire](../semestre1/algebre/README.md) | Projection, orthogonalité, **dimension** — d'où les degrés de liberté et Fisher–Cochran |
| [Analyse — dérivation et intégration](analyse.md) | Le **jacobien** (toutes les densités), $\Gamma$, l'intégrale de Gauss, l'intégrale de $E(g(X))$ |
| [Analyse — convexité](analyse.md) | **Jensen** : le biais de $S$, le drag de volatilité |

## Ce que ces cours fournissent en retour

Le [`modele.md`](../../modele.md) calcule une pente et une variance résiduelle ; ces deux
cours sont ce qui permet de dire si cette pente est **réelle** — c'est-à-dire de lui attacher un
intervalle, un test, et une phrase d'interprétation qui résiste à l'examen.

🏠 [Sommaire général](README.md)
