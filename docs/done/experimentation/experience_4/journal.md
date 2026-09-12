# journal.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/done/experimentation/experience_4/journal.py`, étape par étape, dans
l'ordre du déroulement. Il fait autorité : toute évolution du script doit
d'abord être décrite ici.

Le **protocole** — l'univers quotidien, le TOP 10, les deux critères d'achat, le
motif unique de vente, les issues déclarées, le dimensionnement — est dans
[`README.md`](README.md). Ce miroir décrit le moteur qui l'applique.

## Rôle

Conduire mécaniquement le portefeuille de l'expérience 4, **séance par séance** :
lire l'univers du jour, évaluer chaque valeur à la clôture, former le TOP 10, en
déduire ventes et achats, les exécuter à l'ouverture suivante, tenir la
comptabilité du portefeuille et de son fantôme `SANS-P20`, confronter chaque
élément de la règle à son issue déclarée, recalculer les taux d'étalonnage
publiés au README, tracer les figures de canal, puis écrire les douze journaux
mensuels et le bilan.

> ⚠️ **Aucune décision n'est prise à la main.** Le TOP 10, les signaux, les
> ordres et les issues sortent tous de quantités calculées. Le seul texte rédigé
> à la main est dans [`actualites.md`](actualites.md) et `chartiste.md`, et le
> moteur n'en fait que la mise en page.

## Dépendances

- Modules standard uniquement : `argparse`, `csv`, `math`, `statistics`, `sys`,
  `pathlib`.
- **Aucune bibliothèque de tracé** : les SVG sont écrits à la main.
- **Aucun sous-processus.** Le moteur lit les colonnes glissantes déjà écrites
  par [`python/import_societe.py`](../../../../python/import_societe.md) — `E_n`,
  `VAR_n`, `CORR_n`, `VAL_n` pour `n` ∈ {20, 120} — et n'en réimplémente aucune.
  La seule grandeur recalculée est l'**enveloppe des 20 résidus**, que le CSV ne
  contient pas : elle se déduit des 20 dernières clôtures.

> 🔑 **Pourquoi plus de `generer_graph_decision.py`.** L'expérience 3 lançait la
> règle en sous-processus parce que sa règle était l'encadrement convexe, qui n'a
> qu'une implémentation. La règle de l'expérience 4 ne lit qu'un canal de
> régression, dont toutes les composantes sont des colonnes du CSV. Relancer un
> script pour relire ces colonnes coûterait 20 000 imports de `pandas`.

Le moteur reconfigure sa sortie en UTF-8 dès le premier appel de `main()` : il
imprime des `·`, des `€` et des espaces fines, et une console `cp1252` lèverait
`UnicodeEncodeError` à la fin d'une exécution complète.

## Invocation

```bash
python docs/done/experimentation/experience_4/journal.py
python docs/done/experimentation/experience_4/journal.py --figures
python docs/done/experimentation/experience_4/journal.py --markdown
python docs/done/experimentation/experience_4/journal.py --mois 2022-03
```

### Arguments

| Argument       | Défaut                  | Rôle                                                                  |
| -------------- | ----------------------- | --------------------------------------------------------------------- |
| `--figures`    | —                       | écrit les figures de canal de l'année narrée                          |
| `--markdown`   | —                       | écrit les figures, les douze journaux, les courbes et le bilan        |
| `--mois`       | —                       | n'affiche en console que ce mois (`AAAA-MM`)                          |
| `--repertoire` | le répertoire du script | où lire et écrire                                                     |
| `--quotes`     | `docs/raw/data/quotes`  | où sont les séries                                                    |
| `--dotation`   | `10000.0`               | dotation en euros                                                     |
| `--lignes`     | `5`                     | lignes détenues au maximum                                            |

`--dotation` négative ou nulle : sortie **1**. `--lignes` hors de `[1, 39]` :
sortie **1**. `--mois` hors de l'année narrée : sortie **1**.

Sans option, le moteur calcule tout, écrit les CSV et imprime la console : il ne
touche ni aux figures ni aux markdown. `--figures` existe pour qu'on puisse
produire les figures **avant** `chartiste.md`, que `--markdown` exige.

## Les constantes déclarées

| Constante                              | Valeur                                    | Rôle                                                              |
| -------------------------------------- | ----------------------------------------- | ----------------------------------------------------------------- |
| `REFERENCE` / `REFERENCE_NUE`          | `TR39` / `^FCHI`                          | la référence en rendement total, et l'indice nu                   |
| `DEBUT_SERIE` / `FIN_SERIE`            | `2019-01-02` / `2022-12-30`               | la plage des CSV, **déclarée** et non devinée par glob            |
| `DEBUT_AUDIT` / `DEBUT_NARREE`         | `2020-12-31` / `2021-12-31`               | premières séances de décision de l'audit et de l'année narrée     |
| `SEANCES_ETALONNAGE` / `SEANCES_NARREES` | `258` / `257`                           | contrôlés, et fatals s'ils diffèrent                              |
| `ANNEE`                                | `2022`                                    | l'année narrée                                                    |
| `LONGUE` / `COURTE`                    | `120` / `20`                              | les deux fenêtres, celles des colonnes du CSV                     |
| `TOP` / `K`                            | `10` / `1.0`                              | la taille du TOP et la demi-largeur de bande, en multiples de `s` |
| `VARIANTES`                            | quatre couples `(TOP, K)`                 | `VAR-TOP5`, `VAR-TOP20`, `VAR-K05`, `VAR-K15`                     |
| `HORIZON` / `PAS_ECHANTILLON`          | `20` / `20`                               | l'horizon des issues, et le pas du sous-échantillon               |
| `TE_DECLAREE`                          | `15.58`                                   | la tracking error publiée au README avant la première séance      |
| `ETALONNAGE_PUBLIE`                    | les vingt nombres du README               | confrontés au recalcul du moteur                                  |
| `PROJECTIONS`                          | effectifs et EMD projetés, par élément    | les projections du README, confrontées aux issues au bilan        |
| `FRAIS_EXPERIENCE_3`                   | `75.24`                                   | les frais de l'expérience 3, cités au bilan                       |
| `Z95`                                  | `1.96`                                    | le quantile normal des IC à 95 %                                  |
| `COURTAGE` / `SPREAD` / `TTF`          | `0.10` / `0.015` / `0.30`                 | en %, barème de `couts_transaction.py`                            |
| `EXEMPTES_TTF`                         | `AIR.PA`, `STLAP.PA`, `MT.AS`, `STMPA.PA` | sièges hors de France                                             |
| `SPLITS_POSTERIEURS`                   | `AI.PA`, `ATO.PA`, `WLN.PA`               | divisions rétro-appliquées, avec leur motif                       |
| `SOCIETES`                             | 40 entrées                                | la table des noms d'affichage, **déclarée**                       |

`nom_fichier(ticker)` construit le chemin `{TICKER}_{DEBUT_SERIE}_{FIN_SERIE}.csv`
et **sort en 1** si le fichier manque, en rappelant la commande à lancer, avec un
`--fin` au **lendemain** de `FIN_SERIE`, puisque `--fin` est exclusif.

### Les quatre variantes déclarées

| Variante    | `TOP` | `K` |
| ----------- | ----- | --- |
| *(déclaré)* | 10    | 1,0 |
| `VAR-TOP5`  | 5     | 1,0 |
| `VAR-TOP20` | 20    | 1,0 |
| `VAR-K05`   | 10    | 0,5 |
| `VAR-K15`   | 10    | 1,5 |

Elles sont évaluées sur les 515 séances d'audit. **Elles ne décident rien** :
aucun euro, aucun ordre n'en dépend.

---

## Déroulé d'exécution

### 1. L'univers quotidien

`charger_univers()` lit [`univers.csv`](univers.csv), une ligne par valeur, et
rend la liste des lignes `RETENUE = oui` ainsi que les exclusions et leur motif.
Un fichier absent, ou un ticker retenu absent de `SOCIETES`, est une **sortie 1**.

`univers_du_jour(lignes, d)` rend, **triés**, les tickers tels que :

- `ENTREE_INDICE` est vide ou `≤ d` ;
- `SORTIE_INDICE` est vide ou `≥ d` ;
- `EVALUABLE_DES` est vide ou `≤ d`.

Les bornes sont incluses : `SORTIE_INDICE` est la **dernière** séance dans
l'indice, `ENTREE_INDICE` la **première**.

### 1 bis. Les divisions postérieures à la fenêtre

`SPLITS_POSTERIEURS` est une table **déclarée** :

| Valeur   | Division                                                     | Cours historiques multipliés par |
| -------- | ------------------------------------------------------------ | -------------------------------- |
| `AI.PA`  | 2024-06-10 et 2026-06-08, attributions d'actions gratuites 1,1 | 0,826                          |
| `ATO.PA` | 2025-04-24, regroupement 1 pour 10 000                       | 10 000                           |
| `WLN.PA` | 2026-06-15, regroupement 1 pour 40                           | 40                               |

Ces valeurs restent dans l'univers, dans le TOP 10 et dans tous les taux. Un
**achat** qui les viserait est **refusé** au moment de passer l'ordre, et le
créneau revient au candidat suivant de la séance. Le TOP 10 n'est jamais
recalculé sans elles.

> 🔑 **C'est un changement déclaré par rapport à l'expérience 3**, dont le moteur
> s'arrêtait au premier ordre de ce genre. Avec 12 décisions, l'arrêt ne coûtait
> rien ; avec 257, il rendrait l'expérience otage d'une donnée. Refuser l'ordre
> est un contrôle de recevabilité : il n'intervient ni dans le TOP 10, ni dans
> les signaux, ni dans les issues.

### 2. Lecture des séries et construction du calendrier

`charger_serie(chemin)` rend un objet par série :

- `jours` — la liste ordonnée des dates, tronquées au jour ;
- `par_jour[date]` — `open`, `high`, `low`, `close` et les colonnes `E_120`,
  `VAR_120`, `CORR_120`, `VAL_120`, `E_20`, `VAR_20`, `CORR_20`, `VAL_20`, en
  flottants, **`None` pour une cellule vide** ;
- `rang[date]` — la position de la séance dans `jours`.

Une ligne sans `Close` est ignorée. Une ligne sans `Open` reprend sa clôture —
c'est le cas de `TR39`, qui n'a que `Close`. `High` et `Low` absents reprennent
aussi la clôture.

Les 40 séries de valeurs, `TR39` et `^FCHI` sont lues. **Le calendrier est celui
de `TR39`** :

- `jours_audit` — ses séances de `DEBUT_AUDIT` à l'**avant-dernière** séance,
  2022-12-29 ; la dernière n'a pas de lendemain où exécuter ;
- `jours_etalonnage` — celles d'avant `DEBUT_NARREE` ;
- `jours_narres` — celles à partir de `DEBUT_NARREE`.

Un compte différent de `SEANCES_ETALONNAGE` ou de `SEANCES_NARREES` est une
**erreur fatale**. `execution[d]` est la séance qui suit `d` dans le calendrier.

### 3. Phase 1 — l'évaluation de chaque valeur à chaque séance

`evaluer(serie, d)` rend l'évaluation d'une valeur à la clôture de `d`, ou une
évaluation **muette** avec son diagnostic. Elle est calculée pour chaque séance
de `jours_audit`, **plus la dernière séance, 2022-12-30**, qui sert les figures
de fin d'année et ne produit aucun ordre, et pour **chaque ticker** des séries
lues — l'univers ne filtre qu'ensuite.

Avec $V_T = (n^2 - 1)/12$ :

| Champ       | Formule                                                                  |
| ----------- | ------------------------------------------------------------------------ |
| `R_120`     | $\texttt{CORR\_120}\sqrt{\texttt{VAR\_120}/V_T(120)}$, en €/séance        |
| `TAUX_120`  | $100 \times$ `R_120` / `E_120`, en %/séance                              |
| `S_120`     | $\sqrt{\tfrac{120}{118}\,\texttt{VAR\_120}\,(1-\texttt{CORR\_120}^2)}$  |
| `ECART_S`   | $(\texttt{Close} - \texttt{VAL\_120}) / $ `S_120`                        |
| `R_20`      | $\texttt{CORR\_20}\sqrt{\texttt{VAR\_20}/V_T(20)}$                        |
| `TAUX_20`   | $100 \times$ `R_20` / `E_20`                                             |
| `S_20`      | $\sqrt{\tfrac{20}{18}\,\texttt{VAR\_20}\,(1-\texttt{CORR\_20}^2)}$      |

Le bord bas vaut `VAL_120 − K × S_120`, le bord haut `VAL_120 + K × S_120`.
Toutes les comparaisons de la règle se font sur `ECART_S`, qui est invariant
d'échelle : **sous le bord bas** ⇔ `ECART_S < −K`, **au-dessus du bord haut** ⇔
`ECART_S > K`, **dans la bande** ⇔ `−K ≤ ECART_S ≤ K`.

**L'enveloppe des 20 résidus** : `enveloppe(serie, d)` prend les 20 clôtures
finissant à `d`, les régresse sur `t = 1 … 20` par les moindres carrés, et rend
les demi-largeurs `ENV_BAS` $= -\min_t \hat e_t$ et `ENV_HAUT` $= \max_t \hat e_t$,
les deux indices qui les fixent, et `LARGEUR_ENV_S` $= $ (`ENV_BAS` + `ENV_HAUT`)
/ `S_20`. Elle ne sert qu'aux figures et aux notes.

Une évaluation est **muette** quand l'une de ces conditions est vraie, et son
diagnostic cite la première rencontrée :

- aucune séance du ticker à `d` ;
- une des huit colonnes glissantes est vide ;
- `VAR_120` ou `VAR_20` est nulle, ou `1 − CORR_120²` ne l'est pas strictement ;
- `E_120` ou `E_20` n'est pas strictement positive ;
- moins de 20 clôtures jusqu'à `d`.

### 4. Phase 2 — le TOP 10

`classer(evaluations_du_jour, univers)` ne garde que les évaluations **non
muettes** des tickers de l'univers du jour, de `TAUX_120` **strictement
positif**, et les trie par `TAUX_120` décroissant, puis par ticker. Le **rang**
est la position dans ce tri, à partir de 1 ; il est défini pour **toutes** les
pentes positives, pas seulement les dix premières, ce qui rend les variantes
`VAR-TOP20` calculables sans nouveau tri. Le TOP est l'ensemble des rangs
`≤ TOP`.

Une valeur est **candidate** à `d` si son rang est `≤ TOP`, son `ECART_S` est
`< −K` et son `TAUX_20` est `> 0`. Pour le fantôme `SANS-P20`, la dernière
condition est omise. Être candidate ne dépend pas du portefeuille : c'est une
propriété de la valeur et du jour.

### 5. Phase 3 — la simulation, séance par séance

`simuler(avec_p20)` rend `(ordres, signaux, valeurs, journal)`. Elle est appelée
deux fois : `avec_p20 = True` pour **le portefeuille**, `False` pour **le
fantôme `SANS-P20`**. Seul le premier engage des euros.

Pour chaque séance de décision `d` de `jours_narres`, avec `e = execution[d]`,
dans cet ordre :

1. **Ventes.** Toute ligne détenue dont l'évaluation à `d` est non muette et
   d'`ECART_S > K` est vendue à l'ouverture de `e`. L'univers n'intervient pas :
   une ligne détenue s'évalue qu'elle soit dans l'indice ou non. Une ligne dont
   l'évaluation est **muette** est conservée sans ordre, et la séance est comptée
   comme **séance de silence** de cette ligne.
2. **Espèces et créneaux.** Les produits des ventes rejoignent les espèces.
   `creneaux = lignes − lignes encore détenues`, et `part = espèces / creneaux`,
   calculée **une fois** pour la séance.
3. **Achats.** Les candidats non détenus sont parcourus dans l'ordre du rang :
   - un ticker de `SPLITS_POSTERIEURS` est **refusé**, signal `REFUSE DIVISION`,
     et ne consomme aucun créneau ;
   - s'il ne reste aucun créneau, le signal est `FAUTE DE CRENEAU` ;
   - sinon la quantité vaut `int(part // (prix × (1 + taux_achat)))` ; nulle,
     l'ordre est annulé, signal `QUANTITE NULLE`, et le créneau est consommé
     pour la séance ; positive, l'ordre est passé, signal `EXECUTE`.
4. **Exécution** au cours d'**ouverture** de `e`. Une valeur sans séance à `e`
   est une **erreur fatale** : un ordre ne s'exécute pas à un prix qui n'existe
   pas.
5. **Valorisation** à la clôture de `e` : espèces, titres au `Close` de `e`,
   total, nombre de lignes. Une ligne détenue sans séance à `e` est une erreur
   fatale.

Le premier `e` est le 2022-01-03, le dernier le 2022-12-30 : **257
valorisations**.

**Coûts** : `taux_achat(t) = (0,100 + 0,015 + 0,300) / 100`, TTF nulle pour
`EXEMPTES_TTF` ; `taux_vente(t) = (0,100 + 0,015) / 100`.

**L'écart d'ouverture** d'un ordre vaut $100 \times (\text{Open}_e / \text{Close}_d - 1)$.
Il est publié, jamais corrigé.

**Le motif** d'un ordre est engendré. Achat : *« clôture 50,43 € sous le bord
bas 51,20 € (−1,34 s), rang 3, TAUX_120 +0,212 %/séance, TAUX_20 +0,051
%/séance »*. Vente : *« clôture 58,10 € au-dessus du bord haut 57,02 €
(+1,21 s) »*.

`journal[d]` conserve, pour chaque séance : le TOP, les candidats et leur sort,
les ordres, les lignes muettes, le nombre de lignes et de créneaux libres.

### 6. Phase 4 — la comparaison appariée avec l'expérience 3

`charger_experience_3()` lit `../experience_3/portefeuille.csv`, colonnes `DATE`,
`TITRES`, `TOTAL`, `BASE100`. **Un fichier absent, ou une séance de l'année
narrée qui y manque, est une sortie 1** : une comparaison déclarée au protocole
ne disparaît pas en silence.

### 7. Phase 5 — les issues déclarées

`sous_echantillon = jours_audit[::PAS_ECHANTILLON]` — **26 séances**, dont 13
d'étalonnage et 13 narrées.

Pour chaque séance d'audit `d` et chaque ticker de l'univers du jour dont
l'évaluation est non muette, `issue()` rend une ligne :

- `TOP10`, `SOUS_BAS` (`ECART_S < −K`), `AU_DESSUS_HAUT` (`ECART_S > K`),
  `TAUX_20_POSITIF` ;
- `EXCES_20` $= 100 \times (\text{Close}_{d+20}/\text{Close}_d - \text{TR39}_{d+20}/\text{TR39}_d)$,
  où `d+20` est la vingtième séance suivante **du calendrier** et doit être une
  séance du ticker ; **vide** si elle dépasse `FIN_SERIE` ou manque ;
- `BANDE_SUIVANTE` — `oui` si la clôture de la séance suivante tombe dans la
  bande prolongée d'un pas, $[\texttt{VAL\_120} + R_{120} - K S_{120},\ \texttt{VAL\_120} + R_{120} + K S_{120}]$,
  `non` sinon, vide si cette séance manque.

`comparer(lignes, filtre, groupe)` rend, pour deux groupes : effectifs, moyennes
d'`EXCES_20`, différence, et demi-largeur de l'IC95 de la différence,
$1{,}96\sqrt{s_A^2/n_A + s_B^2/n_B}$ ; `None` si un groupe a moins de deux
observations. Les quatre comparaisons déclarées :

| Élément     | Population                         | Groupe A              | Groupe B      |
| ----------- | ---------------------------------- | --------------------- | ------------- |
| `TOP10`     | l'univers                          | `TOP10`               | hors `TOP10`  |
| `CRITERE-2` | le `TOP10`                         | `SOUS_BAS`            | les autres    |
| `CRITERE-3` | le `TOP10` et `SOUS_BAS`           | `TAUX_20_POSITIF`     | les autres    |
| `VENTE`     | l'univers                          | `AU_DESSUS_HAUT`      | les autres    |

Chacune est calculée **deux fois** : sur le sous-échantillon d'audit — *fait
foi* — et sur toutes les séances d'audit — *borne inférieure de l'incertitude*.
La proportion `BANDE_SUIVANTE` est publiée sur les mêmes deux ensembles, et
confrontée à 68,3 %.

### 8. Phase 6 — les audits

#### `etalonnage()` — le recalcul des taux publiés au README

Sur `jours_etalonnage` seulement, et **sans lire aucune séance postérieure au
2021-12-30** : une issue `BANDE_SUIVANTE` ou `EXCES_20` dont la séance d'arrivée
dépasse le 2021-12-30 n'est pas comptée. C'est la convention sous laquelle le
README les a calculés.

Il rend les onze nombres de `ETALONNAGE_PUBLIE` : évaluations et muettes ; pentes
positives par séance (minimum, médiane, maximum) ; entrants moyens dans le TOP et
séances à au moins un entrant ; clôtures sous le bord bas, au-dessus du bord haut
et dans la bande, sur l'univers ; places du TOP sous le bord bas et au-dessus du
bord haut ; candidats, et `SOUS_BAS` à pente courte nulle ou négative ; séances à
au moins un candidat ; `BANDE_SUIVANTE` ; écart-type d'`EXCES_20` au quotidien et
sur le sous-échantillon, par `statistics.stdev`.

Le bilan publie **les deux colonnes côte à côte**. Un écart est signalé en
console par une ligne `ECART ETALONNAGE`, sans arrêter le moteur : l'écart est
lui-même un résultat, et le README ne se corrige pas après coup.

La même fonction, appliquée à `jours_narres` avec `FIN_SERIE` pour borne, rend
les taux de 2022.

#### `sensibilite()` — les variantes

Pour chaque couple `(TOP, K)`, sur les séances d'audit : le taux de candidats
par évaluation, le taux d'`ECART_S > K` sur l'univers, et le nombre moyen
d'entrants par séance dans le TOP.

#### `positions()` — ce que coûte le motif unique de vente

Chaque position ouverte dans l'année, close ou non : dates, prix, séances de
détention, +/− value, alpha contre `TR39` sur la même période, contribution en
euros nette des frais des deux sens, et **repli maximal** entre la séance
d'achat et la séance de sortie incluses, en clôture et sur le `Low`, rapporté au
prix d'achat. Une position ouverte au 2022-12-30 est valorisée à sa clôture.

S'y ajoutent : les **séances de silence** de chaque position, le nombre de
**séances à créneaux pleins** avec au moins un candidat `FAUTE DE CRENEAU`, le
total de ces signaux, les signaux `REFUSE DIVISION`, et le nombre de séances où
une valeur de `SPLITS_POSTERIEURS` occupe une place du TOP.

#### `dimensionnement()`

Tracking error annualisée des écarts quotidiens contre `TR39`, effet minimal
détectable $1{,}96 \times TE$, et les mêmes grandeurs pour les deux écarts
appariés — contre le fantôme et contre l'expérience 3. `regression(base, indice)`
rend bêta, alpha de régression annualisé, IC95 de cet alpha, R² et écart-type du
résidu ; elle est appliquée au portefeuille et au portefeuille de l'expérience 3.
`exposition()` rend la part investie moyenne et les séances intégralement en
espèces.

### 9. Phase 7 — les figures

#### La figure de canal

`figure_canal(chemin, serie, evaluation, rang, verdict, societe)` écrit un SVG de
900 × 470 dans `graphiques/{TICKER}/canal-{TICKER}-{DATE}.svg` :

- les **120 dernières clôtures** jusqu'à `d` incluse, en polyligne ;
- la **droite ajustée sur 120 séances**, $f(t) = \texttt{VAL\_120} + R_{120}(t - 120)$,
  et sa **bande ± K s**, deux droites parallèles et une surface claire ;
- la **droite ajustée sur 20 séances** sur ses 20 dernières abscisses, et son
  **enveloppe** `f − ENV_BAS`, `f + ENV_HAUT`, avec les deux clôtures qui la
  fixent cerclées ;
- la clôture de `d`, pointée ;
- un titre — société, ticker, date — et une ligne portant rang, `TAUX_120`,
  `ECART_S`, `TAUX_20`, largeur d'enveloppe et verdict du jour ;
- les dates de la première et de la dernière séance de la fenêtre.

> L'échelle verticale est calculée sur les seules grandeurs tracées, toutes
> datées de `d` ou avant. **Une figure ne connaît pas la séance suivante.**

Une évaluation muette ne produit pas de figure : la note porte alors
`*(figure absente)*`.

Figures écrites : pour chaque mois narré, **chaque ticker de l'univers** à la
**dernière séance du mois** — le 2022-12-30 compris —, et **chaque ordre du
portefeuille** à sa séance de décision.

#### Les courbes du portefeuille

`svg()` écrit, pour chaque mois, `graphiques/portefeuille-2022-MM.svg` : trois
courbes en base 100 — le portefeuille, le fantôme `SANS-P20` et `TR39` — du
3 janvier à la dernière séance du mois, un trait vertical à chaque séance
d'exécution d'au moins un ordre. L'échelle ne connaît pas le mois suivant.

### 10. Phase 8 — les markdown

Avec `--markdown` seulement. `charger_textes()` lit `actualites.md` — sections
`## AAAA-MM` — et `chartiste.md` — sections `## AAAA-MM-JJ` puis `### TICKER`.
**Les deux sont requis** : leur absence est une sortie 1. Une section manquante
porte `*(section absente)*`, jamais un texte inventé.

`journal_mensuel()` écrit `rapports/2022-MM.md`. Le mois `m` couvre les
**exécutions** du mois : ses décisions vont de la dernière séance du mois
précédent à l'avant-dernière séance du mois.

1. **Les actualités** du mois précédent.
2. **L'exposition héritée** à la clôture de la dernière séance du mois précédent :
   valeur, date et prix d'achat, cours, +/− value, alpha depuis l'achat.
3. **Le portefeuille depuis le 2022-01-03** : données générales, courbe, puis
   **le tableau de toutes les positions prises depuis le début**, closes comme
   ouvertes, sans aucune séance postérieure au mois.
4. **L'étude chartiste** à la dernière séance du mois : une entrée par ticker de
   l'univers du jour, dans l'ordre des rangs, puis les pentes nulles ou
   négatives par `TAUX_120` décroissant, puis les muettes. Chaque entrée porte
   sa figure, une ligne **calculée** — rang, `TAUX_120`, clôture, bande, écart,
   `TAUX_20`, enveloppe, verdict — et la note de `chartiste.md`. Suit la
   sous-section **« Les figures des ordres du mois »**, une figure par ordre, à
   sa séance de décision.
5. **Le TOP 10** à la dernière séance du mois, puis les **entrées et sorties du
   TOP 10** au fil des séances du mois, datées.
6. **Les ordres exécutés**, avec leur motif engendré et l'écart d'ouverture.
7. **Les signaux non exécutés** : `FAUTE DE CRENEAU`, `REFUSE DIVISION`,
   `QUANTITE NULLE`.
8. **La lecture du mois**, entièrement calculée : meilleure et moins bonne
   contribution en euros, lignes vendues dans le mois comprises ; frais ; écart
   contre `TR39` ; séances à créneaux pleins.

`bilan_annuel()` écrit `bilan-2022.md` : le compte ; mois par mois ; les
positions ; le motif unique de vente ; l'univers et la recevabilité ;
l'étalonnage, README contre moteur, et les mêmes taux sur 2022 ; chaque élément
contre son issue ; le fantôme `SANS-P20` ; la comparaison appariée avec
l'expérience 3 ; la sensibilité ; les trois conventions ; le dimensionnement
confronté ; ce que l'expérience établit et n'établit pas.

> 🔑 **Les phrases conclusives du bilan sont engendrées**, pas écrites d'avance :
> « indiscernable de zéro » n'est imprimé que si l'intervalle contient zéro, et
> la phrase inverse sinon. L'expérience 2 portait dans son moteur une phrase
> vraie de son année et fausse du code.

### 11. La console

Un bloc par mois — ordres exécutés, signaux non exécutés, valeur de fin de mois
contre `TR39` — puis le bloc de bilan : valeur finale, performance, alpha et son
effet minimal détectable, alpha de régression, part investie, fantôme, écart à
l'expérience 3, ordres et frais, lignes jamais revendues, et les issues du
sous-échantillon. `--mois` restreint les blocs mensuels à ce mois.

## Les fichiers écrits

| Fichier             | Colonnes                                                                                                                                                   |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `evaluations.csv`   | `DATE, TICKER, UNIVERS, CLOSE, E_120, VAL_120, S_120, TAUX_120, ECART_S, E_20, VAL_20, TAUX_20, ENV_BAS, ENV_HAUT, LARGEUR_ENV_S, RANG, CANDIDAT, DIAGNOSTIC` |
| `top10.csv`         | `DATE, RANG, TICKER, TAUX_120, ECART_S, TAUX_20, CANDIDAT`                                                                                                 |
| `ordres.csv`        | `DATE, DATE_DECISION, TICKER, SENS, QUANTITE, PRIX, BRUT, FRAIS, NET, RANG, TAUX_120, ECART_S, TAUX_20, ECART_OUVERTURE, MOTIF`                            |
| `signaux.csv`       | `DATE_DECISION, TICKER, RANG, ECART_S, TAUX_20, SORT`                                                                                                      |
| `issues.csv`        | `DATE, TICKER, SOUS_ECHANTILLON, TOP10, SOUS_BAS, AU_DESSUS_HAUT, TAUX_20_POSITIF, EXCES_20, BANDE_SUIVANTE`                                               |
| `portefeuille.csv` · `fantome.csv` | `DATE, ESPECES, TITRES, TOTAL, BASE100, REFERENCE100, LIGNES`                                                                               |

`evaluations.csv` porte toutes les séances d'audit, plus le 2022-12-30, et
**tous les tickers lus** ; `UNIVERS` dit si le ticker appartient à l'univers du
jour. Les cellules d'une évaluation muette restent vides, `DIAGNOSTIC` en donne
la cause. Les booléens s'écrivent `oui` / `non`. Les CSV sont écrits par
`csv.DictWriter`, donc en CRLF, et les markdown en LF.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | exécution complète |
| `1` | série absente, `univers.csv` absent, ticker sans nom déclaré, calendrier incomplet, séance d'exécution manquante pour un ordre ou une ligne détenue, portefeuille de l'expérience 3 absent ou incomplet, argument invalide, ou `actualites.md` / `chartiste.md` absent avec `--markdown` |

## Cas limites

- **Moins de dix pentes positives** : le TOP compte ce qu'il y a, sans compléter.
  Le bilan publie le nombre de séances concernées et le minimum atteint.
- **Aucune pente positive** : TOP vide, aucun candidat ; les ventes restent
  possibles.
- **`1 − CORR_120² ≤ 0`** — une série parfaitement alignée : `S_120` serait nul,
  la bande d'épaisseur nulle. L'évaluation est muette.
- **Une ligne détenue muette** : conservée, sans ordre, séance de silence comptée.
- **Une ligne détenue qui quitte l'indice** : toujours évaluée pour la vente. Le
  cas ne se présente pas en 2022.
- **Un candidat déjà détenu** : il n'est pas candidat à l'achat. Une ligne n'est
  jamais renforcée.
- **Une valeur vendue puis de nouveau candidate** : rachetée librement, dès la
  séance où elle le redevient.
- **Une vente et un achat du même ticker à la même séance** : impossible, la
  vente exige `ECART_S > K` et l'achat `ECART_S < −K`.
- **`EXCES_20` dont l'horizon dépasse `FIN_SERIE`** : vide, et hors des
  moyennes. Ce sont les issues **non tranchées**, comptées au bilan.
- **Un groupe d'issue de moins de deux observations** : moyenne publiée si elle
  existe, différence et IC95 notés `—`.
