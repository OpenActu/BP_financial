# journal.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/done/experimentation/experience_5/journal.py`, étape par étape, dans
l'ordre du déroulement. Il fait autorité : toute évolution du script doit
d'abord être décrite ici.

Le **protocole** — l'expérience 4 reprise, et les cinq pistes de sa revue — est
dans [`README.md`](README.md). Ce miroir décrit le moteur qui l'applique. Le
moteur est celui de l'expérience 4 ([miroir](../experience_4/journal.md)),
auquel s'ajoutent les calculs des cinq pistes ; ce qui en est repris sans
changement est rappelé brièvement, ce qui change est décrit en entier.

## Rôle

Rejouer mécaniquement le portefeuille de l'expérience 4, **vérifier qu'il est
identique**, puis le remesurer :

| Piste | Ce que le moteur fait en plus de l'expérience 4 |
|---|---|
| **T1** + C2 | erreurs types par grappes de dates, vingt phases, correction de Holm, verdict déclaré ; épisodes, séjours et durée d'épisode à l'achat |
| **T3** | le portefeuille fictif `MENSUEL` et la décomposition règle / cadence |
| **C1** | les deux références simulées et les matrices de passage de `BANDE` |
| **T4** | la simulation de la règle sur 2021, confrontée aux nombres publiés et au réalisé |
| **T2** | la référence à exposition appariée, les bêtas semestriels, le témoin aléatoire, la différence neutralisée avec l'expérience 3 |

> ⚠️ **Aucune décision n'est prise à la main.** Le seul texte rédigé à la main
> est dans [`actualites.md`](actualites.md) et [`chartiste.md`](chartiste.md),
> tous deux repris de l'expérience 4, dont le moteur ne fait que la mise en page.

## Dépendances

- Modules standard : `argparse`, `csv`, `datetime`, `math`, `statistics`, `sys`,
  `pathlib`.
- `p_valeur_student()` de [`python/import_societe.py`](../../../../python/import_societe.md),
  importée **localement** dans `quantile_student()` et `p_bilaterale()`, après
  ajout de `python/` au chemin : le dépôt n'a pas de structure de paquet. Cet
  import charge `yfinance` ; aucune fonction réseau n'est appelée.
- Aucune bibliothèque de tracé, aucun sous-processus.

## Invocation

```bash
python docs/done/experimentation/experience_5/journal.py
python docs/done/experimentation/experience_5/journal.py --figures
python docs/done/experimentation/experience_5/journal.py --markdown
python docs/done/experimentation/experience_5/journal.py --mois 2022-03
```

| Argument       | Défaut                  | Rôle                                                        |
| -------------- | ----------------------- | ----------------------------------------------------------- |
| `--figures`    | —                       | écrit les figures de canal de l'année narrée                |
| `--markdown`   | —                       | écrit les figures, les douze journaux, les courbes et le bilan |
| `--mois`       | —                       | n'affiche en console que ce mois (`AAAA-MM`)                |
| `--repertoire` | le répertoire du script | où lire et écrire                                           |
| `--quotes`     | `docs/raw/data/quotes`  | où sont les séries                                          |

**La dotation et le nombre de lignes ne sont plus des arguments.** Ce sont des
constantes : l'expérience 5 remesure un portefeuille qui doit être celui de
l'expérience 4, et un argument qui le changerait ferait échouer le contrôle de
reproduction. `--mois` hors de l'année narrée : sortie **1**.

## Les constantes déclarées

Reprises de l'expérience 4 sans changement : `REFERENCE`, `REFERENCE_NUE`,
`DEBUT_SERIE`, `FIN_SERIE`, `DEBUT_AUDIT`, `DEBUT_NARREE`, `SEANCES_ETALONNAGE`,
`SEANCES_NARREES`, `ANNEE`, `LONGUE`, `COURTE`, `TOP`, `K`, `VARIANTES`,
`HORIZON`, `PAS_ECHANTILLON`, `ETALONNAGE_PUBLIE`, `PROJECTIONS`,
`FRAIS_EXPERIENCE_3`, `Z95`, `COURTAGE`, `SPREAD`, `TTF`, `EXEMPTES_TTF`,
`SPLITS_POSTERIEURS`, `SOCIETES`. Nouvelles ou changées :

| Constante | Valeur | Rôle |
|---|---|---|
| `DOTATION` · `LIGNES` | `10000.0` · `5` | constantes du protocole, plus des arguments |
| `TE_DECLAREE` | `11.08` | **T4** : la tracking error projetée sur 2021 |
| `FIN_ETALONNAGE` | `2021-12-30` | aucune séance lue au-delà pour les projections |
| `FIN_SEMESTRE` | `2022-06-30` | **T2** : la borne des deux semestres |
| `PHASES` · `SEUIL_PHASES` | `20` · `11` | **T1** : les phases, et la majorité exigée |
| `RISQUE` · `DATES_MIN` | `0.05` · `3` | **T1** : le risque de la famille de Holm, et le minimum de dates |
| `TIRAGES_REFERENCE` · `GRAINE_IID` · `GRAINE_MARCHE` | `20000` · `1` · `2` | **C1** |
| `TIRAGES_TEMOIN` · `GRAINE_TEMOIN` · `RESERVOIR_FOI` | `4000` · `3` · `UNIVERS` | **T2** |
| `REFERENCES_PUBLIEES` | les taux et matrices du README | **C1** : confrontés au recalcul |
| `PROJECTIONS_PUBLIEES` | les grandeurs 2021 du README | **T4** : confrontées au recalcul et au réalisé |
| `EMD_GRAPPES` | ± 2,0 · 2,9 · 5,1 · 1,1 | **T1** : les EMD projetés par grappes |
| `CONTROLE` | `31` ordres · `10051.09` € | le portefeuille de l'expérience 4 |

---

## Déroulé d'exécution

### 1. L'univers, les divisions, les séries, le calendrier

Repris de l'expérience 4 : `charger_univers()`, `univers_du_jour()`,
`SPLITS_POSTERIEURS`, `charger_serie()`, et le calendrier de `TR39` avec ses
contrôles de 258 et 257 séances.

S'y ajoutent deux listes de décisions :

- `decisions_mensuelles(ctx, jours)` rend les séances de `jours` **dont la séance
  d'exécution tombe le mois suivant** — la dernière séance de chaque mois, sauf
  pour le mois final d'une fenêtre, dont la dernière décision s'exécute encore
  dans le même mois ;
- `jours_projection` — les séances d'étalonnage **strictement antérieures** au
  `FIN_ETALONNAGE`, du 2020-12-31 au 2021-12-29, dont les exécutions vont du
  2021-01-04 au 2021-12-30.

| Calendrier | Décisions | Exécutions |
|---|---|---|
| narré quotidien | 257, du 2021-12-31 au 2022-12-29 | 257, du 2022-01-03 au 2022-12-30 |
| narré mensuel | 12, du 2021-12-31 au 2022-11-30 | 12 premières séances de mois |
| projection quotidienne | 257, du 2020-12-31 au 2021-12-29 | 257, du 2021-01-04 au 2021-12-30 |
| projection mensuelle | 12, du 2020-12-31 au 2021-11-30 | 12 premières séances de mois |

Un compte différent de 12 décisions mensuelles est une **erreur fatale**.

### 2. L'évaluation et le TOP 10

Repris de l'expérience 4 sans changement : `evaluer()`, `enveloppe()`,
`classer()`, `est_candidat()`.

### 3. La simulation, généralisée

`simuler(ctx, decisions, seances, avec_p20)` rend
`(ordres, signaux, valeurs, journal, registre)`. Pour chaque séance `e` de
`seances`, dans l'ordre :

1. `d` est la séance qui précède `e` dans le calendrier de `TR39` ;
2. **si `d` appartient à `decisions`**, ventes puis achats décidés à la clôture de
   `d` et exécutés à l'ouverture de `e`, exactement comme dans l'expérience 4 ;
3. valorisation à la clôture de `e`.

Entre deux décisions, le portefeuille est tenu sans ordre. Avec une décision à
chaque séance, la fonction rend exactement la simulation de l'expérience 4.
Elle est appelée **six fois** :

| Comptabilité | Décisions | `avec_p20` | Engage des euros |
|---|---|---|---|
| **le portefeuille** | narrées, quotidiennes | oui | **oui** |
| le fantôme `SANS-P20` | narrées, quotidiennes | non | non |
| **`MENSUEL`** (T3) | narrées, mensuelles | oui | non |
| projection quotidienne (T4) | 2021, quotidiennes | oui | non |
| projection `MENSUEL` (T4) | 2021, mensuelles | oui | non |
| projection `SANS-P20` (T4) | 2021, quotidiennes | non | non |

### 4. Le contrôle de reproduction

`controler_reproduction(ordres, valeurs)` lit `../experience_4/ordres.csv` et
`../experience_4/portefeuille.csv`. Il compare, ordre par ordre et dans l'ordre,
`DATE`, `DATE_DECISION`, `TICKER`, `SENS`, `QUANTITE` et `PRIX` arrondi à quatre
décimales, puis le `TOTAL` de chaque séance arrondi au centime.

**Un fichier absent, un nombre d'ordres différent ou le moindre écart est une
sortie 1**, avec la première ligne en défaut. La console imprime
`Controle de reproduction : 31 ordres, 10 051,09 EUR, identiques a l'experience 4`.

### 5. Les issues, et leurs vingt phases — T1

`issues(ctx, jours, borne)` est celle de l'expérience 4, avec un champ de plus :
`PHASE`, le rang de la séance dans `jours_audit` modulo `PHASES`.
`SOUS_ECHANTILLON` vaut `PHASE == 0`.

#### `grappes(lignes, population, groupe)`

Sur les lignes de la population dont `EXCES_20` est tranché, sépare le groupe
testé $A$ du témoin $B$ et rend :

| Champ | Formule |
|---|---|
| `na`, `nb`, `moy_a`, `moy_b` | effectifs et moyennes |
| `difference` | $\bar y_A - \bar y_B$ |
| `G`, `ddl` | nombre de dates portant au moins une observation ; `G − 1` |
| `se` | $\sqrt{\frac{G}{G-1}\sum_g u_g^2}$, avec $u_g = \sum_{i\in A\cap g}\frac{y_i-\bar y_A}{n_A} - \sum_{i\in B\cap g}\frac{y_i-\bar y_B}{n_B}$ |
| `ic` | `quantile_student(ddl) × se` |
| `p` | `p_bilaterale(difference / se, ddl)` |
| `ic_welch` | $1{,}96\sqrt{s_A^2/n_A + s_B^2/n_B}$, l'intervalle de l'expérience 4 |
| `non_tranchees` | lignes de la population sans `EXCES_20` |

Rend `None` pour la différence et tout ce qui en dépend si `na < 2` ou `nb < 2` ;
si seulement `G < DATES_MIN`, la différence et l'intervalle de Welch sont rendus,
mais l'erreur type, l'intervalle par grappes et la p-valeur restent `None`.

`quantile_student(ddl)` cherche par dichotomie, sur 80 itérations entre 0 et 100,
le `t` tel que `p_valeur_student(t, ddl) = 0,05`.

#### `phases(lignes)`

Pour chaque comparaison déclarée et chaque `k` de 0 à 19 : `grappes()` sur les
lignes de `PHASE == k`. Rend la liste des vingt résultats, le nombre de phases
dont l'intervalle **exclut zéro avec le signe de la phase 0**, et l'étendue des
différences.

#### `holm(p_valeurs)`

Ordonne les p-valeurs de la phase 0, rejette $p_{(k)}$ tant que
$p_{(j)} \le \texttt{RISQUE}/(m-j+1)$ pour tout $j \le k$, $m = 4$. Une
comparaison non mesurable n'entre pas dans la famille, et $m$ diminue d'autant.

#### `verdict(comparaison)`

- `non mesurable` si la phase 0 l'est ;
- `sépare` si Holm la rejette **et** si au moins `SEUIL_PHASES` phases excluent
  zéro avec le signe de la phase 0 ;
- `ne sépare pas` sinon.

Le bilan publie, en regard, le verdict de l'expérience 4 — `exclut zéro` quand
l'intervalle de Welch de la phase 0 exclut zéro — et dit s'il **survit** ou
**tombe**.

#### `proportion_grappes(lignes, valeur)`

Pour une proportion $\hat p$ sur $N$ lignes : $u_g = \sum_{i\in g}(x_i - \hat p)/N$,
même variance, même quantile. Sert à `BANDE` et aux parts d'états.

#### Épisodes, séjours et durée d'épisode à l'achat — C2

- `episodes(ctx, predicat)` compte, sur les séances d'audit, les suites
  ininterrompues de séances où `predicat(ticker, jour)` est vrai, pour chaque
  ticker de l'univers. Appliqué à « candidate » et à « au TOP 10 ».
- `duree_a_l_achat(ctx, ordre)` remonte les séances depuis la décision incluse
  et compte celles, consécutives, où la valeur est sous le bord bas, puis celles
  où elle est candidate. Rien au-delà de la décision n'est lu.

### 6. Les références de la bande — C1

`reference_bande(modele, graine)` : pour chacun des `TIRAGES_REFERENCE` tirages,
121 normales du générateur congruentiel du module 2 — `x ← (1664525 x +
1013904223) mod 2³²`, Box-Muller par paires —, cumulées pour la marche aléatoire.
Régression des 120 premières valeurs sur $t = 1\dots120$, $s_{120}$ par la formule
du protocole, état de la 120ᵉ valeur dans sa bande et de la 121ᵉ dans la bande
prolongée d'un pas. Rend les parts des trois états, `BANDE`, et la matrice 3 × 3
en effectifs.

`matrice_bande(ctx, jours, borne)` rend la même matrice **observée** : pour chaque
évaluation non muette de l'univers dont la séance suivante ne dépasse pas
`borne`, l'état de la clôture dans sa bande et celui de la clôture suivante dans
la bande prolongée. Elle est calculée sur l'étalonnage (borne `FIN_ETALONNAGE`),
l'année narrée et l'audit (borne `FIN_SERIE`).

Les références recalculées sont confrontées à `REFERENCES_PUBLIEES`, arrondies au
dixième ; un écart imprime `ECART REFERENCE`.

### 7. Les projections — T4

`resumer(sim, seances)` rend, pour une comptabilité : tracking error contre
`TR39` rebasé à la première séance, bêta, part investie, séances en espèces,
ordres, frais, durée médiane des positions closes, lignes encore détenues,
signaux `FAUTE DE CRENEAU`. `ecart_apparie(a, b, indice)` rend l'écart-type
annualisé de la différence des rendements quotidiens, et, si `indice` est donné,
le bêta de cette différence et l'écart-type de son résidu.

Les trois projections de 2021 sont résumées, confrontées à
`PROJECTIONS_PUBLIEES` — un écart imprime `ECART PROJECTION` — puis, au bilan, au
réalisé de 2022.

### 8. L'exposition et la sélection — T2

- `reference_appariee(valeurs, seances)` : base 100 à la première séance, puis
  $B_d = B_{d-1}\bigl(1 + w_{d-1} R^{\text{TR39}}_d\bigr)$ avec
  $w_{d-1} = \text{titres}_{d-1}/\text{total}_{d-1}$. Elle est calculée sur 2022
  et sur la projection 2021.
- **Bêtas par semestre** : `regression()` sur les séances jusqu'à `FIN_SEMESTRE`
  incluse, puis à partir de cette séance incluse.
- `temoin(ctx, positions, fin, valeur_finale, reservoir)` : `TIRAGES_TEMOIN`
  tirages, générateur congruentiel de graine `GRAINE_TEMOIN`, **repartant de la
  graine pour chaque réservoir** — c'est la convention sous laquelle le README a
  publié les écarts-types de 2021. Dans chaque tirage, les positions réelles sont
  parcourues dans l'ordre de leurs achats ; pour chacune, le réservoir du jour de
  décision — l'univers du jour aux évaluations non muettes, ou les places du TOP
  10 — privé des valeurs que le témoin détient encore ce jour-là, trié par
  ticker ; la valeur est `réservoir[⌊u × taille⌋]`. Si le réservoir est vide, la
  valeur réelle est reprise. Le gain net d'une position vaut
  $\text{brut}\,(\rho - 1) - \text{brut}\cdot\text{taux\_achat} - \text{brut}\,\rho\cdot\text{taux\_vente}$,
  avec $\rho$ le rapport du cours de sortie — ouverture de la séance de vente
  réelle, ou clôture du `FIN_SERIE` sans frais de vente si la position réelle est
  ouverte — au cours d'ouverture de l'achat.
- La même formule appliquée aux valeurs réelles doit retomber sur la valeur
  finale du portefeuille au centime ; sinon, sortie 1.
- Rend, par réservoir : moyenne et écart-type des valeurs finales en base 100,
  **rang** — part des témoins strictement sous le portefeuille —, `z`, effet
  minimal détectable $1{,}96\,\sigma$.
- **La différence avec l'expérience 3** : `ecart_apparie()` avec `TR39`, plus
  l'alpha annualisé de cette régression et son IC95 par `regression()` appliquée
  à la base cumulée de la différence.

### 9. La règle et la cadence — T3

Trois écarts appariés sur 2022, chacun avec son bêta contre `TR39` et
l'écart-type de son résidu : **expérience 5 − `MENSUEL`**, **`MENSUEL` −
expérience 3**, et **expérience 5 − expérience 3**. Plus, pour `MENSUEL` : base
100 finale, part investie, bêta, ordres, frais.

### 10. Les audits repris

Repris de l'expérience 4 : `taux_regle()` et sa confrontation à
`ETALONNAGE_PUBLIE`, `sensibilite()`, `positions_annee()`, `regression()`,
`exposition()`, la tracking error et les effets minimaux détectables.

### 11. Les figures

Figures de canal reprises sans changement. Les courbes du portefeuille portent
**quatre** tracés : le portefeuille, le fantôme `SANS-P20`, `MENSUEL` et `TR39`.

### 12. Les markdown

Les journaux mensuels sont ceux de l'expérience 4, étiquetés « expérience 5 »,
avec une ligne `MENSUEL` dans le tableau du portefeuille.

`bilan_annuel()` écrit `bilan-2022.md`, quinze sections :

1. le compte — dont le contrôle de reproduction ;
2. mois par mois, avec `MENSUEL` ;
3. les positions — contribution « nette des frais payés », convention de l'alpha
   déclarée ;
4. le motif unique de vente, avec les **durées d'épisode à l'achat** ;
5. l'univers et la recevabilité ;
6. les taux d'étalonnage, README contre moteur ;
7. **les issues remesurées** (T1) : phase 0 par grappes et par Welch, Holm, vingt
   phases, verdict, survie des verdicts de l'expérience 4, EMD projetés contre
   réalisés, épisodes et séjours ;
8. **la bande contre ses références** (C1) ;
9. **l'exposition et la sélection** (T2) ;
10. **la règle et la cadence** (T3) ;
11. le fantôme `SANS-P20` ;
12. la sensibilité ;
13. les trois conventions ;
14. **le dimensionnement confronté** (T4) : publié, recalculé, réalisé ;
15. ce que l'expérience établit, et ce qu'elle n'établit pas.

> 🔑 **Toute phrase conclusive est engendrée** par la valeur qu'elle résume : un
> verdict, une survie, un rang, une position entre deux références. Aucune n'est
> écrite d'avance dans le moteur.

### 13. La console

Blocs mensuels repris, puis le bloc de bilan, auquel s'ajoutent : le contrôle de
reproduction, les verdicts T1 et leur survie, `BANDE` contre ses deux références,
la décomposition exposition / sélection, les deux rangs du témoin, l'écart de
cadence, et toute ligne `ECART ETALONNAGE`, `ECART REFERENCE` ou
`ECART PROJECTION`.

## Les fichiers écrits

Repris de l'expérience 4 : `evaluations.csv`, `top10.csv`, `ordres.csv`,
`signaux.csv`, `portefeuille.csv`, `fantome.csv` — mêmes colonnes. `issues.csv`
gagne la colonne `PHASE`.

| Fichier | Colonnes |
|---|---|
| `mensuel.csv` | `DATE, ESPECES, TITRES, TOTAL, BASE100, REFERENCE100, LIGNES` |
| `phases.csv` | `COMPARAISON, PHASE, NA, NB, DIFFERENCE, SE, G, IC, P, EXCLUT_ZERO` |
| `temoin.csv` | `TIRAGE, UNIVERS, TOP10` — valeurs finales en base 100 |

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | exécution complète |
| `1` | les causes de l'expérience 4 ; **fichiers de l'expérience 4 absents ou portefeuille non reproduit** ; valeur du portefeuille réel non retrouvée par la formule du témoin ; compte de décisions mensuelles différent de 12 |

## Cas limites

Ceux de l'expérience 4, plus :

- **Une phase dont une comparaison a moins de trois dates** : non mesurable dans
  cette phase, et comptée comme n'excluant pas zéro.
- **Une comparaison non mesurable à la phase 0** : hors de la famille de Holm, et
  verdict `non mesurable`.
- **Une différence nulle à la phase 0** : aucun signe de référence ; aucune phase
  n'est comptée comme excluant zéro « avec le même signe », et le verdict est
  `ne sépare pas`.
- **Un réservoir de témoin vide** : la valeur réelle est reprise. Le cas ne se
  présente pas sur 2022.
- **Une séance de décision mensuelle sans séance suivante dans la fenêtre** :
  impossible par construction, les mois retenus s'arrêtent à novembre.
