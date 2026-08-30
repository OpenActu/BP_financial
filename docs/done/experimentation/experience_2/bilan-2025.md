# Bilan de l'année 2025

> [Expérience 2](README.md) · dotation 10 000,00 € au 2025-01-02, arrêt au 2025-12-31 · **+12,52 %** contre **+11,70 %** pour TR12

> ⚠️ **L'alpha de cette ligne ne tranche rien**, et le [protocole](README.md#le-dimensionnement-publié-avant-la-première-séance) le déclarait avant la première séance. Ce que ce bilan établit est dans les sections 4 à 7.

---

## 1. Le compte

| | |
|---|---|
| Dotation | 10 000,00 € au 2025-01-02 |
| Valeur finale | **11 251,73 €** |
| Performance | **+12,52 %** |
| TR12, même convention | +11,70 % |
| **Alpha sur l'année** | **+0,81 pt** — *indiscernable de zéro* |
| Ordres | 11 (8 achats, 3 ventes) |
| Frais cumulés | 67,05 €, soit 0,67 % de la dotation |
| Repli maximal | -9,78 %, creux au 2025-04-09 |
| Espèces au 2025-12-31 | 438,50 € |

## 2. Mois par mois

| Mois | Valeur | Base 100 | TR12 | Alpha du mois | Alpha cumulé | Ordres |
|---|---|---|---|---|---|---|
| Janvier | [10 000,00 €](rapports/2025-01.md) | 100,00 | 106,92 | -6,92 pt | -6,92 pt | — |
| Février | [10 000,00 €](rapports/2025-02.md) | 100,00 | 107,44 | -0,49 pt | -7,44 pt | — |
| Mars | [10 108,57 €](rapports/2025-03.md) | 101,09 | 104,63 | +3,71 pt | -3,54 pt | 1 |
| Avril | [10 173,98 €](rapports/2025-04.md) | 101,74 | 103,83 | +1,41 pt | -2,09 pt | 3 |
| Mai | [10 677,86 €](rapports/2025-05.md) | 106,78 | 106,86 | +2,03 pt | -0,08 pt | — |
| Juin | [10 858,95 €](rapports/2025-06.md) | 108,59 | 105,91 | +2,58 pt | +2,67 pt | — |
| Juillet | [10 966,68 €](rapports/2025-07.md) | 109,67 | 107,00 | -0,03 pt | +2,67 pt | — |
| Août | [10 904,82 €](rapports/2025-08.md) | 109,05 | 107,64 | -1,17 pt | +1,40 pt | — |
| Septembre | [11 227,63 €](rapports/2025-09.md) | 112,28 | 107,88 | +2,74 pt | +4,40 pt | 1 |
| Octobre | [11 087,41 €](rapports/2025-10.md) | 110,87 | 109,95 | -3,17 pt | +0,93 pt | 1 |
| Novembre | [11 291,51 €](rapports/2025-11.md) | 112,92 | 111,28 | +0,62 pt | +1,63 pt | 2 |
| Décembre | [11 251,73 €](rapports/2025-12.md) | 112,52 | 111,70 | -0,73 pt | +0,81 pt | 3 |

## 3. Les positions

> Alpha d'une position : son rendement moins celui de TR12 sur **la même période de détention**. La contribution en euros est nette des frais des deux sens.

| Valeur | Achat | Sortie | Séances | Prix d'achat | Prix de sortie | +/− value | Alpha | Contribution |
|---|---|---|---|---|---|---|---|---|
| `BNP.PA` BNP Paribas | 2025-03-03 | 2025-12-01 | 193 | 64,10 € | 71,57 € | **+11,65 %** | +9,38 pt | +220,63 € |
| `AIR.PA` Airbus | 2025-04-01 | 2025-12-31 *(ouverte)* | 192 | 157,06 € | 194,80 € | **+24,03 %** | +18,65 pt | +450,69 € |
| `DG.PA` Vinci | 2025-04-01 | 2025-11-03 | 152 | 108,29 € | 112,41 € | **+3,80 %** | +0,57 pt | +63,65 € |
| `ORA.PA` Orange | 2025-04-01 | 2025-12-31 *(ouverte)* | 192 | 11,05 € | 13,85 € | **+25,27 %** | +19,89 pt | +494,43 € |
| `AI.PA` Air Liquide | 2025-09-01 | 2025-10-01 | 23 | 157,12 € | 157,10 € | **-0,01 %** | -1,06 pt | -11,06 € |
| `OR.PA` L'Oréal | 2025-11-03 | 2025-12-31 *(ouverte)* | 41 | 356,10 € | 359,54 € | **+0,96 %** | -1,11 pt | +9,77 € |
| `MC.PA` LVMH | 2025-12-01 | 2025-12-31 *(ouverte)* | 21 | 620,25 € | 634,65 € | **+2,32 %** | +1,68 pt | +35,50 € |
| `TTE.PA` TotalEnergies | 2025-12-01 | 2025-12-31 *(ouverte)* | 21 | 54,39 € | 54,33 € | **-0,11 %** | -0,75 pt | -11,88 € |

**6 positions sur 8** finissent en gain net de frais. La contribution la plus forte est +494,43 €, la plus faible -11,88 €.


Le contrefactuel « garder le portefeuille de janvier jusqu'au bout » **n'existe pas cette année** : aucun achat n'a eu lieu à la première séance, les vetos ayant écarté les deux seules valeurs de score positif. Le tenir aurait donc voulu dire rester en espèces douze mois, pour 100,00 en base 100.

## 4. L'audit de la règle — les vetos et les poids effectifs

> Piste **T3**. L'expérience 1 calculait les quatre vetos de la règle du module 3 et les jetait. Ici ils s'appliquent : une valeur sous veto ne peut pas entrer. Voici à quelle fréquence ils se déclenchent, sur les **432 évaluations** de la fenêtre d'audit.

| Veto | Ce qu'il dit | Déclenchements | Taux | IC95 |
|---|---|---|---|---|
| **1** | encadrement illisible (moins de 3 épisodes de contact) | 209 / 432 | 48,4 % | ± 4,7 pt |
| **2** | canal se refermant en moins de 20 séances | 50 / 432 | 11,6 % | ± 3,0 pt |
| **3** | critères 1 et 2 de signes opposés | 105 / 432 | 24,3 % | ± 4,0 pt |
| **4** | historique de moins de 120 séances | 0 / 432 | 0,0 % | ± 0,0 pt |

**145 évaluations sur 432** — 33,6 %, ± 4,5 pt — ne déclenchent aucun veto. Ce sont les seules où un achat était possible.

**2 évaluations sur 432** n'ont produit aucun critère : le contrôle de non-traversée de l'enveloppe convexe y échoue, et `generer_graph_decision.py` sort en 2. Le protocole les traite comme un veto de plus — une figure qu'on ne sait pas calculer n'est pas une figure qu'on peut acheter — et elles sont comptées à part plutôt que rangées dans l'un des quatre vetos, qu'elles n'ont pas déclenchés.

Les vetos ont bloqué **19 entrées** qui auraient eu lieu sans eux : une valeur classée au rang 5 ou mieux, de score strictement positif, non détenue, mais sous veto. C'est la différence exacte, sur ce point, entre la règle de l'expérience 2 et celle de l'expérience 1.

### Les poids effectifs du score

> Part de variance expliquée par chaque composante — la covariance de la composante avec le score, divisée par la variance du score, dont la somme fait exactement 100 %. Un score à cinq composantes n'a pas cinq axes.

| Composante | Poids sur l'étalonnage (288) | Poids sur l'audit (432) |
|---|---|---|
| `s1` — tendance longue `TEND_120` | 51,0 % | 47,3 % |
| `s2` — tendance courte `TEND_20` | 5,9 % | 5,1 % |
| `s3` — position dans l'encadrement | 8,3 % | 8,7 % |
| `s4` — momentum 12-1 | 34,7 % | 37,6 % |
| `s5` — alpha annualisé, IC95 | 0,0 % | 1,2 % |

**`s5` s'est réveillée.** L'expérience 1 constatait qu'elle valait `0` à ses 144 évaluations, et en concluait que l'alpha d'une valeur ne se mesure pas sur quelques mois. Sur les 430 évaluations calculables de la fenêtre d'audit, elle est non nulle **9 fois** — `RI.PA` 9 fois — toutes dans l'année narrée, et toutes à `−1` : l'intervalle de confiance de l'alpha y est **entièrement négatif**.

C'est le seul cas de trois ans où la composante distingue quelque chose, et il va dans un seul sens. Une composante qui ne sait dire que du mal, et seulement d'une valeur sur douze, n'est pas pour autant à retirer : la retirer maintenant qu'on l'a vue serait exactement l'ajustement rétrospectif que ce protocole s'interdit.

## 5. Le sens de `s3` — l'aligné contre le fantôme

> Piste **C3**. `s3` a été inversé pour suivre la règle citée : on achète **bas** dans le canal, pas haut. Le sens de l'expérience 1 tourne en parallèle, sans engager un euro, et il a été déclaré avant la première séance.

| | Base 100 au 2025-12-31 | Performance | Ordres | Frais |
|---|---|---|---|---|
| **`s3` aligné** — le portefeuille | **112,52** | +12,52 % | 11 | 67,05 € |
| `s3` au sens de l'expérience 1 — le fantôme | 109,11 | +9,11 % | 9 | 56,70 € |
| `--repartition candidats` — la répartition de l'expérience 1 | 111,71 | +11,71 % | 5 | 97,43 € |
| `--sans-veto` — les vetos calculés mais jetés, comme en 2022 | 105,73 | +5,73 % | 15 | 80,45 € |

Les deux dernières lignes sont les **variantes déclarées** du [protocole](README.md#les-deux-variantes-déclarées) : elles ne décident rien, elles chiffrent ce que valent deux choix de règle que l'expérience aurait pu faire autrement.

L'écart entre les deux vaut **+3,41 point** sur l'année.

Ce chiffre est le seul de ce bilan dont l'incertitude soit favorable, et c'est pourquoi le fantôme existe : les deux portefeuilles partagent l'univers, les dates et les coûts, si bien que l'écart-type de leur **différence** est plus faible que celui de chacun contre la référence :

| Écart mesuré | Écart-type annualisé | Effet minimal détectable |
|---|---|---|
| Portefeuille contre `TR12` | 9,52 %/an | ± 18,7 pt |
| Portefeuille contre son fantôme | 2,68 %/an | ± 5,3 pt |

> Ce que le fantôme **ne** dit **pas** : quel sens est le bon. Un an reste un an. Il dit de combien les deux sens divergent, et à quelle vitesse — ce qui permet de dimensionner l'expérience qui, elle, pourrait trancher.

## 6. La durée de vie de l'encadrement contre la cadence

> Piste **C4**. Le score lit une position dans un canal. Encore faut-il que le canal existe encore au moment où l'on relit.

| Mesure | Valeur |
|---|---|
| Cadence médiane entre deux décisions | 21 séances |
| τ médian, canaux convergents | 61,8 séances |
| Canaux parallèles ou divergents (τ infini) | 113 / 430 |
| Canaux se refermant **avant** la décision suivante | 56 / 430 — 13,0 % |
| Clôtures **sorties** de l'encadrement prolongé | 274 / 430 — 63,7 % ± 4,5 pt |

### La stabilité rétrospective, à une et deux séances

> La décision est recalculée à **d−1** et **d−2 séances**, vers l'arrière uniquement. Si `s3` bascule quand on décale la décision d'une séance, la composante mesure du bruit de calendrier, pas une configuration.

| Décalage | Bascules de `s3` | Changements de score | Têtes de classement modifiées |
|---|---|---|---|
| **d−1** | 27 / 144 — 18,8 % | 45 / 144 — 31,2 % | 7 / 12 |
| **d−2** | 35 / 144 — 24,3 % | 65 / 144 — 45,1 % | 7 / 12 |

## 7. Le registre des thèses réfutables

> Piste **S4**. Deux thèses par valeur et par date de décision, **864 en tout**, engendrées mécaniquement et dépouillées à la date suivante. Aucune n'a été rédigée à la main, aucune n'a été retirée.

| Thèse | Confirmées | Taux | IC95 |
|---|---|---|---|
| `CANAL` — la figure tient | 156 / 430 | 36,3 % | ± 4,5 pt |
| `REFLEXIVE` — toutes phases | 267 / 432 | 61,8 % | ± 4,6 pt |
| └ `AUTO-RENFORCEMENT` | 24 / 60 | 40,0 % | ± 12,4 pt |
| └ `RETOURNEMENT` | 19 / 32 | 59,4 % | ± 17,0 pt |
| └ `AUCUNE SEQUENCE` | 224 / 340 | 65,9 % | ± 5,0 pt |

La ligne `AUCUNE SEQUENCE` est celle qui compte le plus. C'est le défaut de charte de l'agent [`sorosien`](../../../../.claude/agents/sorosien.md) — *« aucune séquence réflexive identifiable »* — rendu réfutable : dire qu'il ne se passe rien, c'est prédire que l'écart contre `TR12` restera dans ± 5 points sur le mois. Le taux ci-dessus dit à quelle fréquence ce défaut prudent est quand même démenti.

## 8. Les trois conventions

> ⚠️ `Close` est **ajustée des dividendes**, `^FCHI` ne l'est pas. Comparer les deux fabrique de l'alpha à partir de rien.

| Série | Convention | 2025 | Alpha du portefeuille |
|---|---|---|---|
| Le portefeuille | rendement total | **+12,52 %** | — |
| `TR12` | rendement total | +11,70 % | **+0,81 pt** |
| `^FCHI` | indice **nu** | +10,22 % | +2,30 pt |

L'écart de convention vaut **1,48 points** sur l'année. Il est déclaré, pas deviné : c'est pour cela que la référence est `TR12` et non `^FCHI`.

## 9. Le dimensionnement, confronté

> Piste **T1**. Le [protocole](README.md#le-dimensionnement-publié-avant-la-première-séance) a publié **avant la première séance** une tracking error attendue de 8,20 %/an, mesurée sur l'expérience 1, et l'effet minimal détectable qui en découlait. Voici ce qui s'est réellement produit.

| | Déclaré avant | Réalisé |
|---|---|---|
| Tracking error annualisée | 8,20 %/an | **9,52 %/an** |
| Effet minimal détectable sur un an | ± 16,1 pt | **± 18,7 pt** |
| Alpha mesuré | — | +0,81 pt |

L'alpha de l'année vaut +0,81 point pour un effet minimal détectable de ± 18,7 points. **Il est indiscernable de zéro**, et il était déclaré comme tel avant la première séance — ce qui est toute la différence avec l'expérience 1, qui a publié le sien comme un résultat.

## 10. Ce que l'expérience établit, et ce qu'elle n'établit pas

**Elle établit**, avec les incertitudes publiées :

- à quelle fréquence chacun des quatre vetos de la règle se déclenche — § 4, sur 432 évaluations ;
- à quelle fréquence l'encadrement que le score lit ne survit pas d'une décision à la suivante — § 6 ;
- à quelle fréquence `s3` bascule quand on décale la décision d'une seule séance — § 6, et c'est une propriété de la composante, pas de l'année ;
- à quelle fréquence les thèses engendrées par la règle sont démenties, par type et par phase — § 7.

**Elle n'établit pas** :

- que la règle est bonne ou mauvaise. L'alpha de l'année, +0,81 point, est plus petit que son propre effet minimal détectable de ± 18,7 points ;
- quel sens de `s3` est le bon. L'écart apparié au fantôme est mesuré, son incertitude aussi, et l'un ne dépasse pas l'autre en un an ;
- quoi que ce soit sur 2026. Aucune quantité mesurée ici ne se prolonge.

Ce qui reste acquis est de nature différente : **les lignes du tableau de dimensionnement ont été écrites avant de regarder l'année, et ce sont exactement celles que l'expérience a pu remplir.** C'est ce qu'une expérience sur une année passée peut honnêtement offrir.

---

[← Protocole](README.md) · [Décembre](rapports/2025-12.md) · [Janvier](rapports/2025-01.md) · [La revue de l'expérience 1](../experience_1/review.md)
