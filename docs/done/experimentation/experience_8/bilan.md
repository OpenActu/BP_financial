# Bilan de l'expérience 8

> [Expérience 8](README.md) · Air Liquide seule, une décision par semaine · **+3,77 %** · alpha officiel **+0,17 pt**

> ⚠️ **La règle est de catégorie B**, et sa fenêtre contient des années déjà jouées : le [protocole](README.md#-ce-que-cette-expérience-ne-pourra-pas-établir) le déclarait avant la fenêtre jouée. Ce que ce bilan établit est aux sections 3 à 6.

---

## 1. Le compte

| | |
|---|---|
| Dotation | 10 000,00 € au 2022-01-03 |
| Valeur finale au 2026-09-10 | **10 377,30 €** |
| Performance | **+3,77 %** |
| Référence à exposition appariée | +3,60 % |
| Détention continue d'Air Liquide | +53,92 % |
| **Alpha officiel** | **+0,17 pt** — *indiscernable de zéro*, effet minimal détectable ± 0,5 pt |
| Écart brut à la détention | -50,15 pt |
| Ordres | 10 — 4 achat, 2 regle-4, 4 vente |
| Frais cumulés | 29,49 €, soit 0,29 pt de dotation |
| Part investie moyenne · maximum | 1,39 % · 18,6 % |
| Décisions hebdomadaires | 245 |

## 2. Les positions

| Premier achat | Sortie | Tranches | Titres | Prix moyen | Prix de sortie | +/− value | Repli max. | Contribution | Séances |
|---|---|---|---|---|---|---|---|---|---|
| 2022-03-07 | 2022-03-28 | 1 | 7 | 127,61 € | 144,82 € | **+13,49 %** | -1,70 % | +115,59 € | 16 |
| 2023-06-26 | 2023-09-18 | 2 | 12 | 148,09 € | 158,42 € | **+6,98 %** | -1,22 % | +114,40 € | 61 |
| 2024-12-16 | 2025-01-27 | 2 | 12 | 150,99 € | 156,76 € | **+3,82 %** | -1,76 % | +59,56 € | 28 |
| 2026-06-22 | 2026-07-06 | 1 | 6 | 165,48 € | 181,00 € | **+9,38 %** | +0,13 % | +87,75 € | 11 |

## 3. Ce que coûte l'absence de sortie en perte

> La règle 5 est la seule sortie : une position qui ne revient pas dans sa bande reste ouverte.

| Mesure | Valeur |
|---|---|
| Positions · dont closes | 4 · 4 |
| **Lignes jamais revendues** au 2026-09-10 | **0** |
| Repli maximal le plus profond, en clôture · sur `Low` | -1,76 % · -2,28 % |
| Durée médiane d'une position close | 22 séances |
| Durée d'une position encore ouverte | — |

## 4. Ce qu'ajoutent les règles 4 et 6

| Variante | Base 100 | Appariée | **Alpha officiel** | Ordres | Frais | Part investie | Maximum |
|---|---|---|---|---|---|---|---|
| **Déclarée** — règles 4 et 6 | 103,77 | 103,60 | **+0,17 pt** | 10 | 29,49 € | 1,39 % | 18,6 % |
| Sans la règle 4 | 102,65 | 102,46 | **+0,19 pt** | 8 | 19,97 € | 0,86 % | 10,5 % |
| Sans la règle 6 | 103,77 | 103,60 | **+0,17 pt** | 10 | 29,49 € | 1,39 % | 18,6 % |
| Ni l'une ni l'autre | 102,65 | 102,46 | **+0,19 pt** | 8 | 19,97 € | 0,86 % | 10,5 % |

La règle 4 ajoute 2 ordres et +9,52 € de frais ; la règle 6, 0 ordres et +0,00 €. Ensemble, elles portent la part investie de 0,86 % à 1,39 %, et son maximum de 10,5 % à 18,6 %.

| Écart apparié | Base 100 | Écart-type de la différence | EMD |
|---|---|---|---|
| déclarée − Sans la règle 4 | **+1,12 pt** | 0,32 %/an | ± 0,6 pt |
| déclarée − Sans la règle 6 | **+0,00 pt** | 0,00 %/an | ± 0,0 pt |
| déclarée − Ni l'une ni l'autre | **+1,12 pt** | 0,32 %/an | ± 0,6 pt |

## 5. Les taux de déclenchement

| Règle | Déclenchée | Exécutée |
|---|---|---|
| **3** — sous le bord bas et `TAUX_20 ≥ 0` | 5 | 4 |
| **4** — sous le seuil figé | 2 | 2 |
| **6** — renforcement | 0 | 0 |
| **5** — au-dessus du bord haut | 58 | 4 |

Les règles 4 et 6 ont été remplies la même semaine **0 fois**. 62 décisions sont passées sous le bord bas, dont 5 avec une pente courte positive : c'est la pente qui filtre, pas la bande.

## 6. Les issues déclarées

> Rendement du cours sur les 20 séances suivant la décision, sur une décision hebdomadaire sur 4 pour que deux observations ne partagent aucune séance.

| Élément | Groupe testé | Témoin | Effectifs | Moyennes | Différence | IC95 | Verdict |
|---|---|---|---|---|---|---|---|
| Règle 3, bande | sous le bord bas | les autres | 16 contre 44 | +1,57 % contre +0,61 % | **+0,96 pt** | ± 2,83 pt | contient zéro |
| Règle 3, pente | sous le bord bas et `TAUX_20 ≥ 0` | sous le bord bas et `TAUX_20 < 0` | 3 contre 13 | +6,74 % contre +0,38 % | **+6,36 pt** | ± 6,59 pt | contient zéro |
| Règle 5, bande haute | au-dessus du bord haut | les autres | 18 contre 42 | +0,74 % contre +0,92 % | **-0,19 pt** | ± 2,83 pt | contient zéro |

## 7. L'étalonnage, publié avant, recalculé après

| Variante | Base publiée | Base recalculée | Alpha publié | Alpha recalculé | Concorde |
|---|---|---|---|---|---|
| **Déclarée** — règles 4 et 6 | 100,66 | 100,66 | -1,05 pt | -1,05 pt | ✓ |
| Sans la règle 4 | 100,26 | 100,26 | -0,95 pt | -0,95 pt | ✓ |
| Sans la règle 6 | 101,14 | 101,14 | -0,51 pt | -0,51 pt | ✓ |
| Ni l'une ni l'autre | 100,73 | 100,73 | -0,41 pt | -0,41 pt | ✓ |

**39 nombres publiés sur 39** sont retrouvés à l'identique par le moteur.

## 8. Ce que l'expérience établit, et ce qu'elle n'établit pas

**Elle établit** :

- ce que les règles 4 et 6 coûtent en frais — 29,49 € contre 19,97 € sans elles, sans aucune incertitude — § 4 ;
- ce qu'elles font à l'exposition : part investie 1,39 % contre 0,86 %, maximum 18,6 % contre 10,5 % — § 4 ;
- les taux de déclenchement des six règles sur 245 décisions — § 5 ;
- ce que l'absence de sortie en perte laisse ouvert : 0 ligne jamais revendue — § 3.

**Elle n'établit pas** :

- que la règle bat la détention : l'alpha officiel vaut +0,17 point pour un effet minimal détectable de ± 0,5 ;
- que l'inversion du stop est une amélioration : la comparaison est faite sur une seule valeur, sur une fenêtre qui contient des années déjà jouées, et la règle est de catégorie B ;
- quoi que ce soit de généralisable : une valeur, un régime, et une part investie moyenne de 1,39 %.

---

[← Protocole](README.md) · [2022](rapports/2022.md) · [2026](rapports/2026.md)
