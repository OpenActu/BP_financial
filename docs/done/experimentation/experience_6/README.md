# Expérience 6 — dix lignes, un achat persistant, un alpha mesuré contre son exposition

La règle de l'[expérience 4](../experience_4/README.md), rejouée sur **2022** et sur
**tout le CAC 40** en composition point-in-time, avec l'appareil de mesure de
l'[expérience 5](../experience_5/README.md), et **trois changements** tirés des
cinq bilans :

| Piste | Constat des expériences 1 à 5 | Ce qui change |
|---|---|---|
| **1 — les frais, seule composante certaine de l'alpha** | 1,17 %, 0,67 %, 0,75 % puis 1,60 % de la dotation en frais, quand tout le reste est indiscernable de zéro ; 14 achats sur 16 décidés dès la première clôture sous le bord bas en 2022 | **l'achat exige deux clôtures consécutives sous le bord bas** ; les frais de chaque comptabilité sont projetés avant, puis confrontés |
| **2 — séparer l'alpha du bêta** | 6,15 des 10,69 points d'écart de l'expérience 5 venaient de l'exposition ; bêta 0,860 puis 0,406 d'un semestre à l'autre | **l'alpha officiel est l'écart à la référence à exposition appariée** ; l'écart à `TR39` devient l'écart brut |
| **4 — rendre l'alpha mesurable** | cinq lignes : tracking error de 8 à 16 %/an, 23 signaux perdus faute de créneau en 2022 et 75 projetés sur 2021 | **dix lignes au lieu de cinq** |

Les deux autres pistes — tester chaque signal avant de l'assembler (3), lire la
vente dans le canal de l'achat (5) — **ne sont pas appliquées**.

---

## ⚠️ Ce que rejouer 2022 une quatrième fois coûte

**La règle est de catégorie B.** Les trois changements ont été choisis après avoir
lu cinq bilans, dont quatre portent sur 2022. La persistance l'est doublement :
elle répond à un constat de l'expérience 4 — 14 achats sur 16 à la première
séance hors bande. **Sa performance sur 2022 ne vaut pas preuve**, et c'est écrit
avant de la connaître.

L'expérience garde trois usages qui ne dépendent pas de la performance :

1. **Les frais sont exacts.** Ce que la persistance et les lignes font aux ordres
   et aux frais se mesure sans erreur d'échantillonnage.
2. **Les effets sont attribuables.** Les quatre combinaisons lignes × persistance
   partagent l'année, l'univers, les coûts et les dates ; leurs écarts appariés
   isolent chaque changement.
3. **L'alpha officiel est mesuré contre son exposition**, avec un effet minimal
   détectable publié avant — et deux fois plus étroit que celui de l'expérience 5.

### Le contrôle de reproduction

La comptabilité **`L5-P1`** — cinq lignes, sans persistance — est la règle de
l'expérience 4. Le moteur vérifie qu'elle retrouve, ordre par ordre et séance par
séance, [`ordres.csv`](../experience_4/ordres.csv) et
[`portefeuille.csv`](../experience_4/portefeuille.csv) de l'expérience 4 — 31
ordres, 10 051,09 € — et **s'arrête** sinon. Les deux changements de règle sont
ainsi garantis être les seuls.

---

## La règle de l'expérience 6

| | |
|---|---|
| Dotation · lignes | **10 000 €** au 3 janvier 2022 · **10 lignes** au maximum |
| Univers | le CAC 40 à sa composition du jour, [`univers.csv`](univers.csv), repris à l'identique |
| Calendrier | décision à la **clôture** de chaque séance, exécution à l'**ouverture** suivante |
| TOP 10 | les dix `TAUX_120` strictement positifs les plus élevés de l'univers du jour |
| **Achat** | dans le TOP 10, **clôture sous `VAL_120 − 1 s` le jour de la décision et la séance précédente**, `TAUX_20 > 0` le jour de la décision, non détenue ; espèces divisées par les créneaux libres ; titres entiers |
| Vente | clôture au-dessus de `VAL_120 + 1 s`, motif unique |
| Coûts | 0,530 % l'aller-retour, TTF exemptée pour Airbus, Stellantis, ArcelorMittal, STMicroelectronics |
| Divisions postérieures | Air Liquide, Atos, Worldline : achat **refusé**, créneau rendu au candidat suivant |
| Référence | `TR39` en rendement total ; **alpha officiel contre la référence à exposition appariée** |

> **Seule la condition de bande persiste.** Le TOP 10 et la pente courte se lisent
> le jour de la décision. La veille est évaluée comme n'importe quelle séance, sur
> ses seules données ; une veille muette n'est pas persistante.

---

## Piste 1 — les frais

### La persistance à l'achat

Une valeur n'est candidate que si elle a clôturé sous le bord bas **deux séances
de suite**. Sur l'étalonnage 2021, **143 des 210 évaluations candidates** au sens
de l'expérience 4 le sont aussi au sens de l'expérience 6.

La persistance entre dans les issues déclarées comme un élément de la règle
parmi les autres :

| Élément | Population | Groupe testé | Témoin |
|---|---|---|---|
| **`PERSISTANCE`** | les candidats au sens de l'expérience 4 | la veille aussi sous le bord bas | les autres |

La famille de Holm compte désormais **cinq** comparaisons. Sur la phase 0 de
l'étalonnage, la comparaison ne réunit que 9 observations contre 2 : **elle sera
très probablement non mesurable sur le sous-échantillon d'audit**, et c'est
déclaré ici. L'intervalle par grappes sur toutes les séances de 2021 vaut
± 1,9 point — une borne inférieure, publiée pour qu'on voie l'écart.

### Les frais projetés

Les frais sont la seule composante de l'alpha qui se mesure **exactement**. Voici
ce que chaque combinaison aurait coûté sur 2021, décisions du 2020-12-31 au
2021-12-29 :

| Comptabilité | Lignes | Persistance | Ordres | Frais | En points de dotation |
|---|---|---|---|---|---|
| `L5-P1` — règle de l'expérience 4 | 5 | 1 | 34 | 203,65 € | 2,04 pt |
| `L10-P1` | 10 | 1 | 52 | 145,16 € | 1,45 pt |
| `L5-P2` | 5 | 2 | 33 | 183,24 € | 1,83 pt |
| **`L10-P2` — expérience 6** | **10** | **2** | **45** | **119,37 €** | **1,19 pt** |

> **Déclaration.** Le bilan publie, pour chaque comptabilité, les ordres et les
> frais réalisés en 2022 à côté de ces projections, et l'effet de chaque
> changement sur les frais. **Moins de frais n'est pas plus d'alpha** : la
> persistance et les lignes changent aussi l'exposition, et ne se lisent qu'avec la
> piste 2.

---

## Piste 2 — l'alpha officiel, mesuré contre son exposition

### La référence à exposition appariée

Chaque séance, elle détient `TR39` dans la proportion où le portefeuille était
investi la veille :

$$R^{\text{app}}_d = w_{d-1}\,R^{\text{TR39}}_d, \qquad w_{d-1} = \frac{\text{titres}_{d-1}}{\text{total}_{d-1}}.$$

> **Déclaration.** **L'alpha officiel de l'expérience 6 est l'écart, en base 100,
> entre le portefeuille et la référence à exposition appariée.** L'écart à `TR39`
> est publié comme **écart brut**, décomposé en exposition et sélection. L'alpha de
> régression, les bêtas semestriels et le témoin aléatoire restent publiés.

### Le dimensionnement, publié avant la première séance

Projeté sur 2021 par la règle elle-même :

| Mesure | Tracking error | **Effet minimal détectable sur un an** |
|---|---|---|
| **Alpha officiel — contre la référence appariée** | **5,25 %/an** | **± 10,3 pt** |
| Écart brut — contre `TR39` | 9,95 %/an | ± 19,5 pt |
| Rang parmi les témoins `UNIVERS` | écart-type 4,72 pt | ± 9,3 pt |
| *Expérience 5, pour mémoire : écart à `TR39`, réalisé* | *13,13 %/an* | *± 25,7 pt* |

> **La tracking error déclarée est 5,25 %/an.** L'effet minimal détectable de
> l'alpha officiel est ainsi **deux fois et demie plus étroit** que celui de l'écart
> brut de l'expérience 5. Il reste de ± 10 points : un alpha annuel de quelques
> points **ne tranchera toujours rien**, mais un écart de l'ordre de dix points
> deviendrait lisible.

Sur 2021, les bêtas semestriels du portefeuille valent **0,346** puis **0,642**.

---

## Piste 4 — dix lignes

### Les quatre combinaisons, projetées sur 2021

| Grandeur | `L5-P1` | `L10-P1` | `L5-P2` | **`L10-P2`** |
|---|---|---|---|---|
| Tracking error contre `TR39` | 11,08 %/an | 9,82 %/an | 11,02 %/an | **9,95 %/an** |
| Tracking error contre la référence appariée | 9,08 %/an | 6,06 %/an | 8,69 %/an | **5,25 %/an** |
| Bêta | 0,832 | 0,630 | 0,798 | **0,509** |
| Part investie moyenne | 75,5 % | 56,4 % | 67,1 % | **44,0 %** |
| Séances intégralement en espèces | 10 | 10 | 11 | **11** |
| Durée médiane d'une position close | 55,5 séances | 54 séances | 53 séances | **53 séances** |
| Lignes encore détenues en fin d'année | 2 | 2 | 1 | **1** |
| Signaux perdus faute de créneau | 75 | 5 | 38 | **1** |

> **Ce que la table dit avant la première séance.** Doubler les lignes fait
> presque disparaître les signaux perdus — 75 à 5 — et réduit d'un tiers la
> tracking error contre la référence appariée. Mais **la part investie baisse**,
> de 75,5 % à 44,0 % avec la persistance : dix créneaux pour autant de candidats,
> c'est plus d'espèces oisives. Le bêta suit. **L'alpha officiel est fait pour
> lire cela**, et l'écart brut à `TR39` ne le permettrait pas.

### Les écarts appariés, et ce qu'ils isolent

| Écart | Ce qu'il isole | Écart-type de la différence, 2021 | EMD sur un an |
|---|---|---|---|
| `L10-P2` − `L10-P1` | la **persistance**, à dix lignes | 3,18 %/an | ± 6,2 pt |
| `L10-P2` − `L5-P2` | les **lignes**, à persistance 2 | 6,61 %/an | ± 13,0 pt |
| `L10-P2` − `L5-P1` | les deux, contre la règle de l'expérience 4 | 8,20 %/an | ± 16,1 pt |

Le bilan publie aussi les écarts `L10-P1` − `L5-P1` et `L5-P2` − `L5-P1`, et
l'**interaction** — la différence des deux effets des lignes.

---

## Les fantômes, repris à dix lignes et à achat persistant

| Grandeur, 2021 | `SANS-P20` | `MENSUEL` |
|---|---|---|
| Tracking error contre `TR39` | 9,55 %/an | 12,60 %/an |
| Bêta | 0,796 | 0,120 |
| Part investie moyenne | 68,6 % | 10,9 % |
| Ordres · frais | 65 · 196,99 € | 9 · 22,42 € |
| Écart-type de la différence avec `L10-P2` | 7,14 %/an | 8,28 %/an ; 6,19 %/an bêta neutralisé |

`SANS-P20` retire la pente courte, `MENSUEL` décide à la dernière séance de chaque
mois. **La comparaison à l'expérience 3 n'est pas reconduite** : l'expérience 5 l'a
faite, et l'expérience 6 se compare à la règle de l'expérience 4, rejouée dans
`L5-P1`.

---

## Ce qui est repris de l'expérience 5, sans changement

| | |
|---|---|
| **T1** | issues par grappes de dates, vingt phases, Holm, verdict déclaré — la règle du verdict, ses seuils et sa convention d'intervalle sont ceux de l'[expérience 5](../experience_5/README.md#t1--une-convention-dintervalle-déclarée-une-fois) |
| **C1** | la bande contre ses deux références simulées, et ses matrices de passage, publiées par l'expérience 5 |
| **T2** | la référence appariée, les bêtas semestriels, le témoin aléatoire de 4 000 tirages, réservoir `UNIVERS` faisant foi |
| **T4** | toutes les grandeurs projetées ci-dessus, recalculées par le moteur et confrontées au réalisé |
| Étalonnage | les vingt taux publiés par l'expérience 4, recalculés |
| Figures · notes · actualités | redessinées aux mêmes dates ; [`chartiste.md`](chartiste.md) et [`actualites.md`](actualites.md) repris, avec un verdict corrigé |

---

## Ce que l'expérience 6 peut établir

| Quantité | Incertitude déclarée |
|---|---|
| **Frais de chaque comptabilité, et effet de chaque changement sur les frais** | **aucune — exacts** |
| Effet des changements sur la part investie et les signaux perdus | exacts |
| **Alpha officiel** | **± 10,3 pt** |
| Écart brut à `TR39` | ± 19,5 pt |
| Rang parmi les témoins `UNIVERS` | ± 9,3 pt |
| Effet de la persistance, à dix lignes | ± 6,2 pt |
| Effet des lignes, à persistance 2 | ± 13,0 pt |
| Chaque issue, par grappes | ± 1,1 à ± 5,1 pt sur 20 séances ; `PERSISTANCE` probablement non mesurable |

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| `bilan-2022.md` · `rapports/2022-MM.md` | le bilan et les douze journaux |
| [`journal.md`](journal.md) · [`journal.py`](journal.py) | le miroir d'exécution, puis le moteur |
| [`univers.csv`](univers.csv) · [`actualites.md`](actualites.md) · [`chartiste.md`](chartiste.md) | repris des expériences 4 et 5 |
| `evaluations.csv` · `top10.csv` · `ordres.csv` · `signaux.csv` · `issues.csv` | comme l'expérience 5, sous la règle de l'expérience 6 |
| `portefeuille.csv` · `fantome.csv` · `mensuel.csv` | le portefeuille, `SANS-P20` et `MENSUEL`, quotidiennement |
| `combinaisons.csv` | les quatre combinaisons, la référence appariée et `TR39`, en base 100 |
| `phases.csv` · `temoin.csv` | les vingt phases des cinq comparaisons, et les témoins |
| `graphiques/` | les courbes et les figures de canal |

---

## Ce que l'expérience 6 ne fait toujours pas

- **Aucun levier, aucune couverture exécutée, aucun ordre stop, aucune vente à
  découvert.** La référence appariée mesure l'exposition ; elle ne la couvre pas.
- **Aucune année neuve** : c'est la limite principale, et elle est déclarée en tête.
- **Aucun signal testé seul avant d'entrer dans la règle** : la piste 3 n'est pas
  appliquée.
- **Aucune prédiction de cours, aucun conseil en investissement.**

## Pour aller plus loin

- [L'expérience 5](../experience_5/README.md) et son [bilan](../experience_5/bilan-2022.md) — l'appareil de mesure repris ici
- [L'expérience 4](../experience_4/README.md) — la règle, rejouée dans `L5-P1`
- [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md) · [finance](../../../raw/concept/semestre4/finance/README.md)
