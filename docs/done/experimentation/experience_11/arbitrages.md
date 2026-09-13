# Les arbitrages étiquetés sur Airbus — ce qu'on en infère, et ce qu'on n'en infère pas

Quatorze figures de canal d'`AIR.PA` ont été étiquetées à la main — CONSERVER,
ACHAT, ACHAT MASSIF, VENTE — puis relues par les trois agents du dépôt, qui
devaient en **inférer les règles de trading**. Ce document consigne le résultat.

> ⚠️ **Exercice de catégorie B au sens le plus fort.** Les étiquettes ont été
> posées sur des figures dont la suite des cours est connue, et dont le résultat
> — alpha officiel **−9,77 pt** — était publié en tête du [protocole](README.md).
> Rien ici n'établit qu'une règle fonctionne.

## 1. Le fait qui recadre l'exercice

Trouvé séparément par les trois agents, vérifié deux fois.

**a. Les figures portent déjà leur verdict**, imprimé par le moteur. L'application
verdict → étiquette est **univoque** :

| Verdict imprimé                               | n     | Étiquette                    |
| --------------------------------------------- | ----- | ---------------------------- |
| `dans la bande`                               | 1     | CONSERVER                    |
| `candidate à l'achat`                         | 3     | ACHAT                        |
| `sous le seuil de la règle 4`                 | 3     | ACHAT MASSIF                 |
| `au-dessus du bord haut`                      | 5     | VENTE                        |
| **`sous le bord bas, pente courte négative`** | **2** | **ACHAT** ← seule divergence |

**b. Neuf des quatorze dates sont les neuf ordres d'`AIR.PA`** de l'expérience 11
([`ordres.csv`](ordres.csv)), motifs compris : `ACHAT`→ACHAT, `REGLE-4`→ACHAT
MASSIF, `VENTE`→VENTE, sans exception ni omission. Les cinq autres sont les
dernières décisions de chaque année et la dernière de la fenêtre.

**c. Deux VENTE ne sont pas exécutables** — 2023-12-29 et 2024-12-27, aucune
position ouverte. L'étiquetage est **sans état**, la sélection des dates en a un.

> **L'information nouvelle des quatorze étiquettes se réduit à une décision
> binaire : supprimer le filtre `TAUX_20 ≥ 0` de la règle 3.** Tout le reste
> reproduit le verdict du moteur.

## 2. Le jeu de règles consolidé

**Couche signal**, avec `écart_s = (Close − VAL_120) / s_120` :

```
écart_s ≥ +1,00  →  VENTE
écart_s ≤ −2,50  →  ACHAT MASSIF   (ou : sous le seuil figé de la règle 4)
écart_s ≤ −1,00  →  ACHAT          ← sans condition de pente
sinon            →  CONSERVER
```

Priorité VENTE > ACHAT MASSIF > ACHAT > CONSERVER. `TAUX_120`, `TAUX_20`,
position et largeur de l'enveloppe **n'entrent pas** : aucun n'est nécessaire, et
aucun ne sépare les groupes sans recouvrement.

**Couche exécution** — nécessaire mais **non inférable** des étiquettes, donc
importée de l'expérience 11 : cadence hebdomadaire, exécution à l'ouverture
suivante ; tranches de 10 % et 20 % du portefeuille ; une tranche de chaque par
position ; la vente solde tout ; pas de vente à découvert ; ordre refusé en entier
si les espèces manquent.

## 3. Quatre limites, chiffrées

**a. Les seuils ne sont pas identifiés, seulement encadrés.** Tout seuil de vente
dans `]+0,09 ; +1,03]` et d'achat dans `]−1,14 ; +0,09]` rend le même 14/14. Le
seuil massif tient à **0,09 s** — une seule paire d'observations.

**b. Deux reconstructions sont indiscernables** : seuil de niveau à −2,50 s, ou
seuil de prix figé de la règle 4. Elles divergent sur **la moitié des
renforcements** sur les 245 décisions.

**c. Aucune machine à états cohérente ne produit ces quatorze étiquettes.**

| Machine simulée sur les 245 décisions      | Ordres | Première entrée | Accord      |
| ------------------------------------------ | ------ | --------------- | ----------- |
| Expérience 11 telle quelle                 | 9      | 2023-09-15      | **10 / 14** |
| Sans le filtre de pente — la règle inférée | 19     | **2022-03-04**  | **8 / 14**  |

Sans le filtre, la règle entre dès mars 2022 ; les achats de septembre 2023
**n'ont alors jamais lieu**. Les étiquettes ont été posées sur des figures
engendrées par un état, tout en énonçant une règle qui détruit cet état.

**d. La pente négative des ACHAT MASSIF est une tautologie, pas un critère.** La
règle 4 se déclenche sous un seuil **figé** : pour parcourir un écart-type de plus
en quelques semaines, `TAUX_20` **doit** être négatif.

## 4. Ce que coûterait la seule modification réelle

Supprimer le veto de pente sur `AIR.PA` : **9 ordres → 19**, exposition moyenne
4,7 % → 8,8 %, semaines investies 18 % → 49 %. Le veto écarte aujourd'hui **92 %
des occasions** — 5 évaluations sur 65 sous le bord bas portent `TAUX_20 ≥ 0`.

Ce qu'il écarte, en séries de décisions vetoées consécutivement :

| Période                 | Décisions | Traversée jusqu'au creux |
| ----------------------- | --------- | ------------------------ |
| 2024-05-31 → 2024-07-26 | 9         | **−19,0 %**              |
| 2026-01-30 → 2026-03-27 | 9         | **−17,7 %**              |
| 2025-11-21 → 2025-12-24 | 6         | −21,5 %                  |
| 2025-03-28 → 2025-04-25 | 5         | −19,7 %                  |

> **Le veto est la seule protection du dispositif contre un enfoncement durable**
> — et c'est lui que les deux étiquettes divergentes suppriment. La baisse de 2026
> était à 96 % propre à la valeur : **−27,7 %** pour Airbus contre **−6,9 %** pour
> l'indice.

## 5. Le test hors échantillon

Règle appliquée là où elle n'a pas été fabriquée, rendements postérieurs cachés
aux trois agents. Intervalles **par grappes de dates** :

|                                                | R+20            | R+60                              |
| ---------------------------------------------- | --------------- | --------------------------------- |
| `AIR.PA`, ACHAT moins VENTE                    | −0,48 pt ± 2,97 | **−4,63 pt ± 4,38 — exclut zéro** |
| Les **neuf autres** valeurs, ACHAT moins VENTE | −0,64 pt ± 1,25 | −0,81 pt ± 1,98                   |
| Les neuf autres, ACHAT MASSIF moins VENTE      | −0,16 pt ± 2,43 | +2,46 pt ± 3,53                   |

Sur la valeur qui a servi à étiqueter, le seul verdict tranché va **contre** le
sens de la règle ; hors échantillon, les quatre groupes sont **indiscernables**.
Même destin que le seuil de −15 % de l'[expérience 10](../experience_10/README.md).

## 6. Trois constats de géométrie que le tableau ne montre pas

- **`s_120` varie d'un facteur 3,9** — de 2,36 € à 9,26 €. « −1 s » n'est pas une
  distance de marché constante.
- **Le 2025-06-20 (VENTE) : R² = 0,002, p = 0,60.** La droite n'explique rien ; la
  bande y est une dispersion, pas un canal. Deux objets géométriques différents
  portent le même mot.
- **Le 2025-04-04 est la seule exécution où l'ouverture s'écarte de la clôture qui
  l'a décidée** — 141,06 € décidé, 126,97 € exécuté, **−9,99 %** — et c'est la date
  dont l'enveloppe est la plus large (15,4 % ; corrélation 0,89 avec la
  volatilité). L'enveloppe le disait avant.

## 7. Classement A / B

| Élément                                                        | Classe                                                                                    |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Cadence, tranches, seuils ± 1 s                                | **A** — pré-enregistrés au protocole ; les étiquettes y sont compatibles sans les établir |
| La pente négative des ACHAT MASSIF est mécanique               | **A** — déductible de l'énoncé de la règle 4                                              |
| Le veto écarte 92 % des occasions ; la règle 4 ne le porte pas | **A** — compté sur [`decisions.csv`](decisions.csv)                                       |
| **Suppression du filtre `TAUX_20 ≥ 0`**                        | **B** — inférée de 2 étiquettes sur 245 décisions, résultat connu                         |
| **Seuil ACHAT MASSIF à −2,50 s**                               | **B**, et fragile — calé à 0,09 s près                                                    |

La suppression du filtre est **promouvable en A** : elle *retire* un paramètre,
elle est motivée a priori par une asymétrie réelle — la règle 4 n'a jamais porté
ce filtre —, et elle peut être déclarée avant une fenêtre non jouée. L'issue
« règle 3, pente » du [bilan](bilan.md) donne **−1,81 pt ± 2,89** : le point
estimé est négatif, mais l'intervalle contient zéro. **La mesure n'arbitre pas.**

## 8. Lecture réflexive

**Aucune séquence réflexive identifiable** sur Airbus entre 2022 et 2026 : pas
d'émission de titres, pas d'acquisition payée en actions, dette/EBITDA
décroissante (1,34 → 1,08), carnet pluriannuel et contractuel. Le canal de
transmission du cours vers les fondamentaux n'existe pas — les cadences de
livraison sont contraintes par la chaîne physique. **Le cours est un effet, jamais
une cause**, et l'étiquetage a raison d'être purement géométrique. Ce qui ferait
réviser cette conclusion : des acquisitions en titres, un financement client
adossé à la capitalisation, ou une sortie d'indice déclenchant des flux non
discrétionnaires.

## 9. Ce que cet exercice n'établit pas

- **Aucune performance.** Sur une valeur et 4,71 ans, l'effet minimal détectable
  vaut **± 18 points d'alpha annuel**.
- **Aucun arbitrage entre les deux reconstructions**, qui diffèrent sur la moitié
  des renforcements.
- **Quatorze étiquettes ne sont pas quatorze informations** : les seuils n'étant
  contraints que par les paires adjacentes, elles se réduisent à **trois nombres**,
  et se regroupent en **cinq épisodes**, non quatorze unités indépendantes.

**Ce qui serait testable — une expérience 12.** Même univers, même fenêtre, deux
variantes appariées : avec et sans le filtre de pente. Mesure = différence des
**alphas officiels contre la référence à exposition appariée**, jamais l'écart
brut à l'indice ; intervalle sur la **différence**, par grappes de dates, avec
contrôle de reproduction ordre par ordre sur les ordres communs. La quantité à
mesurer d'abord est l'écart-type de cette différence — inconnue du dépôt, et sans
elle l'étude n'est pas dimensionnable.

**Aucun conseil en investissement, aucun dimensionnement, aucune prédiction de
cours.** Ce document décrit une règle inférée d'étiquettes posées après coup, et
la sortie de cette règle sur les données qui l'ont produite.

Sources : [`README.md`](README.md) · [`bilan.md`](bilan.md) ·
[`decisions.csv`](decisions.csv) · [`ordres.csv`](ordres.csv) ·
[`positions.csv`](positions.csv) · les 14 figures de
[`graphiques/AIR.PA/`](graphiques/AIR.PA) ·
[Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md)
