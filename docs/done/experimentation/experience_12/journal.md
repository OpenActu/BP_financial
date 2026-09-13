# `journal.py` — le moteur de l'expérience 12

Miroir d'exécution du moteur. Il décrit **ce que le script fait**, dans l'ordre où
il le fait. Le markdown fait autorité : toute évolution doit d'abord être décrite
ici.

Le **protocole** — les deux modifications, l'étalonnage, les contrôles — est dans
[`README.md`](README.md).

## Son rôle

Rejouer les six règles de l'[expérience 11](../experience_11/journal.md) sur les
dix mêmes valeurs, du 2022-01-03 au 2026-09-10, avec **le veto de pente retiré de
la seule règle 3** et des **tranches de 5 % et 10 %** au lieu de 10 % et 20 %.

Il ne lit **aucun** texte rédigé à la main.

> **Sa différence avec le moteur voisin tient en deux lignes de code.** La règle 3
> n'évalue plus `TAUX_20 ≥ 0` ; `PART_ACHAT` et `PART_RENFORT` sont divisées par
> deux. Tout le reste est identique, contrôles de reproduction compris.

## Ce dont il dépend

| Dépendance | Usage |
|---|---|
| `docs/raw/data/quotes/{ENGI,AC,EN,TTE,SAF,AIR,PUB,SGO,MC,CAP}_PA_2019-01-02_2026-09-11.csv` | les dix séries, par [`import_societe.py`](../../../../python/import_societe.md) |
| [`univers.csv`](univers.csv) | les 40 valeurs du tirage, **revérifié** contre la graine 10 |
| `docs/done/experimentation/experience_11/decisions.csv` | le contrôle des évaluations, valeur par valeur |
| `p_valeur_student()` de [`import_societe.py`](../../../../python/import_societe.md) | les intervalles de Student, par import local |

Bibliothèque standard seule, SVG écrits à la main.

## Son invocation

```bash
python docs/done/experimentation/experience_12/journal.py
python docs/done/experimentation/experience_12/journal.py --figures
python docs/done/experimentation/experience_12/journal.py --markdown
python docs/done/experimentation/experience_12/journal.py --annee 2023
```

| Argument | Défaut | Effet |
|---|---|---|
| `--figures` | absent | écrit les figures de canal, rangées par valeur |
| `--markdown` | absent | écrit les figures, les cinq journaux annuels et le bilan |
| `--annee AAAA` | toutes | n'affiche que cette année ; hors fenêtre jouée : sortie **1** |
| `--repertoire` | le répertoire du script | où lire `univers.csv` et écrire |
| `--quotes` | `docs/raw/data/quotes` | où sont les dix séries |

Sans argument, il calcule tout et n'écrit que les cinq CSV. La dotation, les
parts, le plafond et les seuils sont des **constantes** : ce sont les six règles,
pas des réglages.

## Les constantes déclarées

| Constante | Valeur | Écart avec l'expérience 11 |
|---|---|---|
| `VALEURS` | `ENGI.PA`, `AC.PA`, `EN.PA`, `TTE.PA`, `SAF.PA`, `AIR.PA`, `PUB.PA`, `SGO.PA`, `MC.PA`, `CAP.PA` | — |
| `GRAINE` | 10 | — |
| `EXEMPTES_TTF` | `AIR.PA` | — |
| `DOTATION` | 10 000,00 € | — |
| **`PART_ACHAT` · `PART_RENFORT`** | **5 % · 10 %** | ⚠️ **divisées par deux** |
| **`VETO_PENTE_REGLE_3`** | **`False`** | ⚠️ **la modification** |
| `PLAFOND` | 100 % — aucun levier | — |
| `LONGUE` · `COURTE` · `K` | 120 · 20 · 1,0 | — |
| `HORIZON` · `PAS_ECHANTILLON` | 20 séances · une décision sur 4 | — |
| `COURTAGE` · `SPREAD` · `TTF` | 0,100 % · 0,015 % · 0,300 % | — |
| `ETALONNAGE_PUBLIE` | les nombres du [protocole](README.md#le-dimensionnement-publié-avant-la-fenêtre-jouée) | — |
| `TEMOIN_EXP_11` | base 123,01 · alpha +7,77 · part 33,84 % · σ_d 6,92 %/an | le repère de comparaison |

`VETO_PENTE_REGLE_3` est une constante nommée, non un `if` enfoui : c'est l'objet
de l'expérience, et il doit se lire d'un coup d'œil.

## Le déroulé

### 1. `charger()` — les dix séries, un calendrier unique

Ignore toute ligne sans `Close` — la dernière de chaque série, au 2026-09-11.
**Exige que les dix calendriers coïncident exactement** : 1 970 séances, sinon
arrêt — code **2**. Aucune des dix ne porte de division ; `facteur()` et `reel()`
sont implémentés à l'identique et valent l'identité.

### 2. `tirage()` et `controler_univers()`

Rejoue la permutation : les 40 ISIN triés par ordre croissant, mélangés par
`random.Random(10)`. Compare rang par rang à `univers.csv`, vérifie que les dix
`RETENUE` sont exactement `VALEURS`, et que les seules `EXAMINEE` sont les
**rangs 1 à 13**. Tout écart arrête le moteur — code **2**.

### 3. `evaluer(valeur, jour)` — en unités ajustées

Rend `None` si la fenêtre de 120 séances est incomplète ou si une variance n'est
pas strictement positive. Sinon, avec $V_T(n) = \tfrac{n^2-1}{12}$ et
$r_n = \texttt{CORR\_n}\sqrt{\texttt{VAR\_n}/V_T(n)}$ :

$$s_{120} = \sqrt{\tfrac{120}{118}\,\texttt{VAR\_120}\,(1-\texttt{CORR\_120}^2)},
\qquad \texttt{TAUX\_n} = 100\,r_n/\texttt{E\_n}$$

et l'écart réduit `(Close − VAL_120)/s_120`. Résultats mis en cache.

### 4. `decisions_hebdomadaires(debut, fin)`

La **dernière séance de chaque semaine civile** où **les dix** sont évaluables.
Première évaluation possible : le **2019-06-21**.

### 5. `taux_achat(valeur)`

Courtage 0,100 % + demi-spread 0,015 %, plus **TTF 0,300 % sauf pour `AIR.PA`**.
Soit 0,530 % l'aller-retour pour neuf valeurs, **0,230 %** pour Airbus.

### 6. `simuler(debut, fin, avec_r4, avec_r6)` — l'ordre exact d'une séance

Pour chaque séance, dans cet ordre :

1. **les attributions d'actions gratuites sont créditées** — sans effet ici ;
2. si la **veille** était une décision, les signaux des dix valeurs sont collectés
   **sans qu'aucun ordre ne soit encore passé** :
   - **vente** (règle 5) si la valeur est détenue et clôture au-dessus du bord
     haut ;
   - ⚠️ **achat** (règle 3) si elle ne l'est pas et que la clôture est sous le bord
     bas — **et rien d'autre**. `TAUX_20` n'est **pas** consulté, parce que
     `VETO_PENTE_REGLE_3` vaut `False` ;
   - sinon, si elle est détenue : **règle 4** si la clôture passe sous le seuil
     figé et que la règle n'a pas déjà joué ; **règle 6** si la décision suit
     immédiatement l'achat, que la clôture est encore sous le bord bas **et que
     `TAUX_20 ≥ 0`** — la règle 6 **conserve** son veto ;
3. **les ventes s'exécutent d'abord**, à l'ouverture réelle : elles libèrent les
   espèces ;
4. **les achats s'exécutent ensuite, triés par écart croissant** — le plus négatif
   d'abord —, tous dimensionnés sur **la même** valeur de portefeuille : celle de
   la clôture de la décision, avant tout ordre ;
5. chaque achat est **borné par les espèces disponibles** : quantité
   $\lfloor \min(\text{montant}, \text{espèces}) / (\text{prix}(1+\text{frais}))\rfloor$.
   C'est un **service partiel** : l'ordre est réduit à ce que la trésorerie
   permet, et **refusé et compté** seulement s'il n'atteint pas un titre ;
6. un achat de la **règle 3** arme le seuil de la règle 4, à
   `clôture de la décision − 1 s₁₂₀`, **figé** jusqu'à la vente ;
7. **valorisation** : espèces, puis titres aux clôtures réelles du jour.

Une vente solde la position entière de cette valeur, tranches comprises, et
désarme son seuil. **La règle 5 est la seule sortie.**

`simuler` est appelé **cinq fois** : déclarée, sans la règle 4, sans la règle 6,
sans les deux, puis une **cinquième fois en témoin** — veto rétabli et tranches
10 / 20 %, c'est-à-dire exactement la règle de l'expérience 11 —, dont la seule
fonction est de fournir la série contre laquelle σ_d se calcule. Seule la déclarée
produit journaux, figures et CSV.

Les deux paramètres qui distinguent ces appels, `veto` et `parts`, sont **explicites
dans la signature** et valent par défaut `VETO_PENTE_REGLE_3` et
`(PART_ACHAT, PART_RENFORT)` : aucun appel ne modifie une constante globale.

### 7. `detention()` et `appariee()`

`detention()` place **un dixième de la dotation sur chacune des dix** à
l'ouverture de la deuxième séance, TTF due valeur par valeur, et garde jusqu'au
bout. `appariee()` rend la base 100 d'un placement subissant chaque séance le
rendement du panier **dans la proportion où le portefeuille était investi la
veille**. L'**alpha officiel** est `base − appariée`.

`ecart_type(a, b)` rend l'écart-type annualisé de la différence des rendements
quotidiens ; l'EMD vaut `1,96 ×` cette valeur.

### 8. `mesurer_positions()`

Pour chaque position : sa valeur, ses dates, son motif de sortie — `VENTE` ou
*ouverte* —, ses tranches, son prix de revient moyen, le prix de sa **première
tranche**, son prix de sortie, sa plus-value, son **repli maximal** rapporté à la
première tranche — en clôture et sur les `Low` — et au prix moyen, sa durée et sa
contribution en euros.

### 9. `issues()` et `comparer()` — par grappes de dates

`issues()` rend une ligne par **(décision, valeur)** : les trois états déclarés,
l'appartenance au sous-échantillon — une décision sur 4 —, et `RENDEMENT_20`.
Sans 20 séances disponibles, la cellule reste **vide**.

`comparer()` n'agrège pas les observations : les dix valeurs d'une même date
partagent le marché du jour. Méthode, héritée de l'[expérience
5](../experience_5/README.md) :

1. ne retenir que les dates du sous-échantillon où **les deux groupes** ont au
   moins une observation ;
2. à chaque date, la **différence des moyennes** des deux groupes ;
3. Student sur ces différences, à **`nombre de dates − 1`** degrés de liberté,
   quantile obtenu par **dichotomie** sur `p_valeur_student()`.

L'issue « règle 3, pente » porte l'objet de l'expérience : elle compare ce que le
veto laissait passer à ce qu'il écartait. Elle est calculée **sur toutes les
évaluations**, que la règle ait acheté ou non.

### 10. Les deux contrôles de reproduction

| Fonction | Ce qu'elle exige | Échec |
|---|---|---|
| `controler_univers()` | la permutation se rejoue depuis la graine 10 | code **2** |
| `controler_evaluations_experience_11()` | l'écart réduit et `TAUX_20` de **chacune des dix valeurs** coïncident à 5 × 10⁻⁴ près avec `experience_11/decisions.csv` | code **2** |

> **Les ordres ne sont pas contrôlables**, et le moteur ne prétend pas le faire.
> Retirer le veto change l'état du portefeuille dès la première décision, et les
> tranches sont deux fois plus petites : aucun ordre ne peut coïncider. C'est la
> limite que l'expérience 11 n'avait pas — elle pouvait exiger la coïncidence
> ordre par ordre, parce que son portefeuille était le même.
>
> Les **évaluations**, elles, ne dépendent pas du portefeuille : un écart y
> signalerait un défaut de chargement ou de formule, et arrête le moteur.

### 11. `etalonnage()` et `ecarts_publies()`

Rejoue les quatre variantes sur **2019-06-21 → 2021-12-31** et compare chaque
nombre à `ETALONNAGE_PUBLIE`, recopié du protocole. Recalcule en outre **σ_d**,
l'écart-type de la différence avec l'expérience 11, et le confronte à
`TEMOIN_EXP_11`. Tout écart est imprimé `ECART ETALONNAGE …` et compté au bilan.
**Le README n'est jamais corrigé après coup.**

## Les figures

`figure_canal(valeur, jour)` écrit `graphiques/{TICKER}/canal-{DATE}.svg` : les
120 clôtures ajustées, la droite et sa bande `± 1 s`, la droite sur 20 séances et
l'**enveloppe de ses résidus**, le **seuil de la règle 4** en violet quand il est
armé, et le verdict du jour.

> ⚠️ **Le vocabulaire du verdict change, et c'est voulu.** Là où l'expérience 11
> imprimait `sous le bord bas, pente courte négative` — le libellé du veto —, ce
> moteur imprime **`candidate à l'achat`** dans les deux cas, puisque la pente
> n'entre plus dans la règle 3. La figure dit ce que la règle fait ; c'est la
> leçon tirée d'[`arbitrages.md`](../experience_11/arbitrages.md), où le verdict
> imprimé avait déterminé l'étiquetage.

`svg_portefeuille()` écrit `graphiques/portefeuille-{ANNEE}.svg` : portefeuille,
référence appariée et détention en base 100, un trait vertical par exécution. Les
échelles ne lisent **aucune** séance postérieure à la date tracée.

## Les journaux annuels et le bilan

`rapports/{ANNEE}.md` : le compte de l'année, la courbe, les ordres avec leur
motif engendré et leur rang de service, les positions par valeur, les décisions
notables, et la lecture de l'année, entièrement calculée.

`bilan.md` : **l'alpha officiel en tête, avec son EMD à côté de lui**, puis les
positions, la répartition par valeur, ce que coûte l'absence de sortie en perte,
ce qu'ajoutent les règles 4 et 6, les taux de déclenchement, les trois issues par
grappes, la confrontation de l'étalonnage, les deux contrôles de reproduction, la
**comparaison avec l'expérience 11** — écart de base, d'alpha, de part investie et
σ_d —, et ce que l'expérience établit ou n'établit pas.

## L'affichage console

Un bloc par année, puis le bilan : alpha officiel et son EMD, écart brut, frais,
part investie et maximum, refus faute d'espèces, déclenchements, apport de chaque
règle, répartition par valeur, issues, comparaison à l'expérience 11, résultat des
deux contrôles, et toute ligne `ECART ETALONNAGE`.

## Les fichiers écrits

| Fichier | Colonnes |
|---|---|
| `decisions.csv` | `DATE`, `TICKER`, `EXECUTION`, `CLOSE_AJUSTE`, `CLOSE_REEL`, `VAL_120`, `S_120`, `ECART_S`, `TAUX_120`, `TAUX_20`, `SOUS_BAS`, `AU_DESSUS`, `SEUIL_4_FRANCHI`, `ACHETABLE_SANS_VETO`, `ACHETABLE_AVEC_VETO`, `SIGNAL` |
| `ordres.csv` | `DATE`, `DATE_DECISION`, `TICKER`, `SENS`, `RANG_SERVICE`, `QUANTITE`, `PRIX_REEL`, `BRUT`, `FRAIS`, `NET`, `ECART_S`, `TAUX_20`, `MOTIF` |
| `positions.csv` | `TICKER`, `ACHAT`, `SORTIE`, `MOTIF`, `TRANCHES`, `QUANTITE`, `PRIX_PREMIERE_TRANCHE`, `PRIX_ACHAT`, `PRIX_SORTIE`, `SEUIL_REGLE_4`, `TAUX_20_ACHAT`, `SEANCES`, `PLUS_VALUE`, `REPLI_PREMIERE`, `REPLI_MOYEN`, `REPLI_LOW`, `CONTRIBUTION` |
| `portefeuille.csv` | `DATE`, `ESPECES`, `TITRES`, `TOTAL`, `BASE100`, `APPARIEE100`, `DETENTION100`, `PART_INVESTIE`, `LIGNES_OUVERTES` |
| `issues.csv` | `DATE`, `TICKER`, `SOUS_BAS`, `TAUX_20_POSITIF`, `AU_DESSUS_HAUT`, `SOUS_ECHANTILLON`, `RENDEMENT_20` |

Deux colonnes sont propres à cette expérience. `ACHETABLE_SANS_VETO` et
`ACHETABLE_AVEC_VETO` marquent, à chaque décision, ce que chacune des deux règles
aurait autorisé : leur différence **est** l'objet de l'expérience, ligne à ligne.
`TAUX_20_ACHAT` conserve la pente courte au moment de l'achat, pour que le bilan
puisse dire combien de positions le veto aurait refusées.

`SENS` vaut `ACHAT`, `REGLE-4`, `RENFORT` ou `VENTE`. Les booléens s'écrivent
`oui` / `non` ; une grandeur indisponible laisse une **cellule vide**.

## Les codes de sortie

| Code | Cause |
|---|---|
| **0** | tout s'est déroulé |
| **1** | une série manque, `--quotes` n'est pas un répertoire, `--annee` est hors fenêtre, ou une colonne obligatoire est absente |
| **2** | un contrôle a échoué : calendriers divergents, tirage non reproduit, ou évaluations divergentes de l'expérience 11 |

## Les cas limites

- **Deux valeurs au même écart** : tri stable, départage par l'ordre de `VALEURS`.
- **Espèces insuffisantes** : l'ordre est **réduit** à ce qu'elles permettent, et
  refusé seulement s'il n'atteint pas un titre. Le compteur est publié même à
  zéro — l'étalonnage en comptait **10**.
- **Position encore ouverte à la dernière séance** : valorisée à la clôture réelle
  du 2026-09-10, marquée *ouverte*.
- **Moins de deux dates dans une comparaison** : différence publiée sans
  intervalle, verdict *non mesurable*.
- **Écart d'alpha inférieur à l'EMD** : le bilan l'écrit explicitement plutôt que
  de laisser lire un écart de quelques points comme un résultat. C'est le cas
  attendu : l'EMD vaut **± 13,6 points**.
