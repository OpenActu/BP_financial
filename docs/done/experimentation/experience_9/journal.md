# `journal.py` — le moteur de l'expérience 9

Miroir d'exécution du moteur. Il décrit **ce que le script fait**, dans l'ordre
où il le fait. Le markdown fait autorité : toute évolution doit d'abord être
décrite ici.

Le **protocole** — le tirage, les six règles, les deux conventions que cinq
valeurs obligent à déclarer, les deux références, les issues — est dans
[`README.md`](README.md).

## Son rôle

Rejouer la règle de l'[expérience 8](../experience_8/journal.md) sur **cinq
valeurs** au lieu d'une, du 2022-01-03 au 2026-09-10, et écrire tout ce que le
protocole déclare : les journaux annuels, le bilan, les figures et les cinq CSV.

Il ne lit **aucun** texte rédigé à la main. Tous les chiffres publiés sortent de
son calcul.

## Ce dont il dépend

| Dépendance | Usage |
|---|---|
| `docs/raw/data/quotes/{AI,KER,ORA,SAF,ENGI}_PA_2019-01-02_2026-09-11.csv` | les cinq séries, produites par [`import_societe.py`](../../../../python/import_societe.md) |
| [`univers.csv`](univers.csv) | les 39 candidates dans l'ordre du tirage, **revérifié** contre la graine |
| `p_valeur_student()` de [`import_societe.py`](../../../../python/import_societe.md) | les intervalles de Student, par import local |

Aucune autre dépendance : bibliothèque standard seule, SVG écrits à la main.

## Son invocation

```bash
python docs/done/experimentation/experience_9/journal.py
python docs/done/experimentation/experience_9/journal.py --figures
python docs/done/experimentation/experience_9/journal.py --markdown
python docs/done/experimentation/experience_9/journal.py --annee 2023
```

| Argument | Défaut | Effet |
|---|---|---|
| `--figures` | absent | écrit les figures de canal, rangées par valeur |
| `--markdown` | absent | écrit les figures, les cinq journaux annuels et le bilan |
| `--annee AAAA` | toutes | n'affiche en console que cette année ; hors fenêtre jouée : sortie **1** |
| `--repertoire` | le répertoire du script | où lire `univers.csv` et écrire |
| `--quotes` | `docs/raw/data/quotes` | où sont les cinq séries |

Sans aucun argument, il calcule tout et n'écrit que les cinq CSV.

La dotation, les parts d'achat, le plafond et les seuils sont des **constantes** :
ce sont les six règles, pas des réglages.

## Les constantes déclarées

| Constante | Valeur |
|---|---|
| `VALEURS` | `AI.PA`, `KER.PA`, `ORA.PA`, `SAF.PA`, `ENGI.PA` |
| `GRAINE` | **9** |
| `DOTATION` | 10 000,00 € |
| `PART_ACHAT` · `PART_RENFORT` | 10 % · 20 % du portefeuille, **par valeur** |
| `PLAFOND` | **100 %** de part investie — aucun levier |
| `LONGUE` · `COURTE` · `K` | 120 · 20 · 1,0 écart-type |
| `HORIZON` · `PAS_ECHANTILLON` | 20 séances · une décision sur 4 |
| `COURTAGE` · `SPREAD` · `TTF` | 0,100 % · 0,015 % · 0,300 % — les cinq sont françaises |
| `DEBUT_NARREE` · `FIN_ETALONNAGE` | 2022-01-03 · 2021-12-31 |
| `ETALONNAGE_PUBLIE` | les nombres du [protocole](README.md#le-dimensionnement-publié-avant-la-fenêtre-jouée), pour la confrontation |
| `DATES_EXPERIENCE_8` | les huit dates d'ordre d'Air Liquide sur l'étalonnage, pour le contrôle de reproduction |

## Le déroulé

### 1. `charger()` — les cinq séries, et un calendrier unique

Lit les cinq CSV. Une ligne sans `Close` est ignorée — la dernière ligne de
chaque série, datée du 2026-09-11, en est une. Retient `Open`, `High`, `Low`,
`Close` et, pour chaque fenêtre, `E_n`, `VAR_n`, `CORR_n`, `VAL_n`, ainsi que les
`Stock Splits` non nuls.

Puis **exige que les cinq calendriers coïncident exactement** : 1 970 séances
identiques. Une séance présente chez l'une et absente chez l'autre arrête le
moteur — code **2**. Ce n'est pas une commodité : deux calendriers différents
feraient décider certaines valeurs un jour et les autres un autre.

### 2. `facteur()` et `reel()` — la dé-ajustement, par valeur

`facteur(valeur, jour)` est le produit des divisions **postérieures** à `jour`
pour cette valeur ; `reel(...) = ajusté × facteur`. Seul Air Liquide en porte —
quatre attributions de 1,1. Pour les quatre autres, le facteur vaut 1,0 à toute
date, et cours réel et cours ajusté coïncident.

**La règle ne lit jamais un cours réel** : bandes, écarts et seuil de la règle 4
sont pris sur la série ajustée, où ils sont invariants d'échelle. Les cours réels
ne servent qu'aux quantités, aux espèces et à la valorisation.

### 3. `tirage()` et `controler_univers()` — le tirage, revérifié

Refait la permutation : les 39 candidates triées par ISIN croissant, mélangées
par `random.Random(9)`. Compare le résultat, rang par rang, à `univers.csv`.
Contrôle en outre que les cinq valeurs `RETENUE` du fichier sont exactement
`VALEURS`, et que les seules `EXAMINEE` sont les rangs 1 à 5. Tout écart arrête
le moteur — code **2**.

C'est ce contrôle qui rend le tirage vérifiable : il interdit qu'on ait retouché
l'univers après coup.

### 4. `evaluer(valeur, jour)` — tout en unités ajustées

Rend `None` si la fenêtre de 120 séances n'est pas complète, si `VAR_120`,
`VAR_20` ou `1 − CORR_120²` n'est pas strictement positif, ou si `E_120` ou
`E_20` ne l'est pas. Sinon :

$$r_n = \texttt{CORR\_n}\sqrt{\frac{\texttt{VAR\_n}}{V_T(n)}},\quad
V_T(n) = \frac{n^2-1}{12},\quad
s_{120} = \sqrt{\tfrac{120}{118}\,\texttt{VAR\_120}\,(1-\texttt{CORR\_120}^2)}$$

et rend la clôture, `VAL_120`, `s_120`, l'écart réduit
`(Close − VAL_120)/s_120`, puis `TAUX_120` et `TAUX_20`, tous deux
$100\,r_n/\texttt{E\_n}$ — sans dimension, donc comparables d'une valeur à
l'autre.

### 5. `decisions_hebdomadaires(debut, fin)`

La **dernière séance de chaque semaine civile** où **les cinq** sont évaluables,
la semaine étant celle du calendrier ISO. La première évaluation possible est le
**2019-06-21**, 120ᵉ séance de chaque série.

### 6. `simuler(debut, fin, avec_r4, avec_r6)` — l'ordre exact d'une séance

Pour chaque séance de la fenêtre, dans cet ordre et pas un autre :

1. **les attributions d'actions gratuites sont créditées** : toute valeur dont
   une division tombe ce jour voit ses titres multipliés, partie entière ;
2. si la **veille** était une décision, les signaux des cinq valeurs sont
   collectés à partir de son évaluation, et **aucun ordre n'est encore passé** :
   - **vente** (règle 5) si la valeur est détenue et clôture au-dessus du bord
     haut ;
   - **achat** (règle 3) si elle n'est pas détenue, clôture sous le bord bas et
     `TAUX_20 ≥ 0` ;
   - sinon, si elle est détenue : **règle 4** si sa clôture passe sous le seuil
     figé et que la règle n'a pas déjà joué pour cette position ; **règle 6** si
     la décision est celle qui suit immédiatement l'achat, que la clôture est
     encore sous le bord bas avec `TAUX_20 ≥ 0`, et que le renfort n'a pas déjà
     eu lieu ;
3. **les ventes s'exécutent d'abord**, à l'ouverture réelle du jour : elles
   libèrent les espèces qui financeront les achats de la même séance ;
4. **les achats s'exécutent ensuite, triés par écart croissant** — le plus
   négatif d'abord. Tous sont dimensionnés sur **la même** valeur de
   portefeuille : celle de la clôture de la décision, avant tout ordre. Pas de
   composition à l'intérieur d'une séance ;
5. chaque achat est **borné par les espèces disponibles à cet instant** :
   la quantité est $\lfloor \min(\text{montant}, \text{espèces}) / (\text{prix}
   \times (1+\text{frais}))\rfloor$. À zéro titre, l'ordre est **refusé et
   compté** ;
6. le **seuil de la règle 4** n'est armé que par un achat de la **règle 3**, à
   `clôture de la décision − 1 s₁₂₀` de cette décision, et reste **figé** jusqu'à
   la vente. Un renfort ne le déplace pas ;
7. **valorisation** : espèces, puis somme des titres aux clôtures réelles du
   jour.

Une vente solde la position entière de cette valeur, tranches comprises, et
désarme seuil, règle 4 et règle 6 pour elle seule. Les autres valeurs ne sont pas
touchées.

`simuler` est appelé **quatre fois** : la variante déclarée, puis sans la
règle 4, sans la règle 6, et sans les deux. Les trois dernières ne servent qu'à
la comparaison du bilan ; seule la déclarée produit journaux, figures et CSV.

### 7. `detention()` et `appariee()` — les deux références

`detention()` place **un cinquième de la dotation sur chacune des cinq** à
l'ouverture de la deuxième séance, en parties entières, et garde jusqu'au bout —
divisions créditées comme au portefeuille.

`appariee()` rend la base 100 d'un placement qui, chaque séance, subit le
rendement du panier **dans la proportion où le portefeuille était investi la
veille**. C'est l'**alpha officiel** : `base − appariée`, en points.

`ecart_type(a, b)` rend l'écart-type annualisé de la différence des rendements
quotidiens, en %/an ; l'effet minimal détectable est `1,96 ×` cette valeur.

### 8. `mesurer_positions()`

Pour chaque position : sa valeur, ses dates, ses tranches, son prix de revient
moyen, son prix de sortie — ou la dernière clôture si elle est encore ouverte —,
sa plus-value, le **repli maximal** atteint entre le premier achat et la sortie,
en clôture et sur les `Low`, sa durée en séances et sa contribution en euros.

### 9. `issues()` et `comparer()` — les intervalles par grappes de dates

`issues()` rend une ligne par **(décision, valeur)** : les trois états déclarés,
l'appartenance au sous-échantillon — une décision sur `PAS_ECHANTILLON`, de sorte
que deux décisions retenues ne partagent aucune des 20 séances de l'horizon — et
`RENDEMENT_20`, le rendement de la valeur sur les 20 séances suivantes. Sans
20 séances disponibles avant la fin de la fenêtre, la cellule reste **vide** —
jamais zéro.

`comparer()` n'agrège **pas** les observations : les cinq valeurs d'une même date
partagent le marché du jour, et les compter comme indépendantes fabriquerait des
intervalles trop étroits — c'est la faute corrigée par l'[expérience
5](../experience_5/README.md). La méthode est donc :

1. ne retenir que les dates du sous-échantillon où **les deux groupes** ont au
   moins une observation ;
2. à chaque date retenue, calculer la **différence des moyennes** des deux
   groupes ce jour-là ;
3. appliquer Student à ces différences, à **`nombre de dates − 1`** degrés de
   liberté.

Le quantile à 95 % s'obtient par **dichotomie** sur `p_valeur_student()`, qui est
la seule loi de Student du dépôt. Le bilan publie, pour chaque comparaison, le
nombre de dates, la différence moyenne, son intervalle et son verdict — « exclut
zéro » ou « contient zéro ».

### 10. `etalonnage()` et `ecarts_publies()` — la confrontation

Rejoue les quatre variantes sur **2019-06-21 → 2021-12-31** et compare chaque
nombre à `ETALONNAGE_PUBLIE`, recopié du protocole. Tout écart est **imprimé en
console** sous la forme `ECART ETALONNAGE {variante} {grandeur} : publié …,
moteur …`, et compté au § 7 du bilan. **Le README n'est jamais corrigé après
coup** : c'est l'écart qui est publié, pas le nombre rectifié.

### 11. `controler_dates_air_liquide()` — le contrôle de reproduction, et sa limite

Compare les **dates** d'ordre d'Air Liquide sur l'étalonnage à celles de
l'expérience 8, figées dans `DATES_EXPERIENCE_8`. Un écart arrête le moteur —
code **2** : la règle par valeur doit être rigoureusement inchangée.

Les **quantités** ne sont pas contrôlées, et ne peuvent pas l'être : la règle 3
dimensionne en part du portefeuille, et le portefeuille de l'expérience 9 n'est
pas celui de l'expérience 8. Le bilan publie l'écart de résultat que cela
produit, plutôt que de le taire.

## Les figures

`figure_canal(valeur, jour)` écrit `graphiques/{TICKER}/canal-{DATE}.svg` : les
120 clôtures ajustées, la droite de régression et sa bande `± 1 s`, la droite sur
20 séances et l'**enveloppe de ses résidus** avec les deux points de contact, le
**seuil de la règle 4** en trait violet quand il est armé, et le verdict du jour
en titre. Une figure est écrite à chaque décision produisant un ordre, et à la
dernière décision de chaque année.

`svg_portefeuille()` écrit `graphiques/portefeuille-{ANNEE}.svg` : le
portefeuille, la référence appariée et la détention continue en base 100, avec un
trait vertical à chaque exécution.

Tout est écrit à la main, sans bibliothèque. Les échelles ne lisent **aucune**
séance postérieure à la date tracée.

## Les journaux annuels et le bilan

Avec `--markdown`, `journal_annuel(annee)` écrit `rapports/{ANNEE}.md` : le
compte de l'année, la courbe, les ordres avec leur motif engendré et leur rang de
service, les positions ouvertes et closes **par valeur**, les décisions notables,
et la lecture de l'année, entièrement calculée.

`bilan.md` rassemble : le compte, les positions, ce que coûte l'absence de sortie
en perte, ce qu'ajoutent les règles 4 et 6, les taux de déclenchement, la
**répartition par valeur** — ordres, contribution, part investie —, les trois
issues par grappes, la confrontation de l'étalonnage, le contrôle de reproduction
contre l'expérience 8, et ce que l'expérience établit ou n'établit pas.

## L'affichage console

Un bloc par année — ordres, valeur de fin d'année contre les deux références —
puis le bloc de bilan : alpha officiel et son EMD, écart brut, frais, part
investie et maximum, déclenchements, refus faute d'espèces, apport des règles 4
et 6, répartition par valeur, issues, et toute ligne `ECART ETALONNAGE`.

## Les fichiers écrits

| Fichier | Colonnes |
|---|---|
| `decisions.csv` | `DATE`, `TICKER`, `EXECUTION`, `CLOSE_AJUSTE`, `CLOSE_REEL`, `VAL_120`, `S_120`, `ECART_S`, `TAUX_120`, `TAUX_20`, `SOUS_BAS`, `AU_DESSUS`, `SEUIL_FRANCHI`, `SIGNAL` |
| `ordres.csv` | `DATE`, `DATE_DECISION`, `TICKER`, `SENS`, `RANG_SERVICE`, `QUANTITE`, `PRIX_REEL`, `BRUT`, `FRAIS`, `NET`, `ECART_S`, `TAUX_20`, `MOTIF` |
| `positions.csv` | `TICKER`, `ACHAT`, `SORTIE`, `MOTIF`, `TRANCHES`, `QUANTITE`, `PRIX_ACHAT`, `PRIX_SORTIE`, `SEUIL_REGLE_4`, `SEANCES`, `PLUS_VALUE`, `REPLI_CLOTURE`, `REPLI_LOW`, `CONTRIBUTION` |
| `portefeuille.csv` | `DATE`, `ESPECES`, `TITRES`, `TOTAL`, `BASE100`, `APPARIEE100`, `DETENTION100`, `PART_INVESTIE`, `LIGNES_OUVERTES` |
| `issues.csv` | `DATE`, `TICKER`, `SOUS_BAS`, `TAUX_20_POSITIF`, `AU_DESSUS_HAUT`, `SOUS_ECHANTILLON`, `RENDEMENT_20` |

`SENS` vaut `ACHAT`, `REGLE-4`, `RENFORT` ou `VENTE`. `RANG_SERVICE` est la place
de l'ordre dans le tri par écart croissant de sa séance, 1 pour le premier servi.
Les booléens s'écrivent `oui` / `non`. Une grandeur indisponible laisse une
**cellule vide**.

## Les codes de sortie

| Code | Cause |
|---|---|
| **0** | tout s'est déroulé |
| **1** | une série manque, `--quotes` n'est pas un répertoire, `--annee` est hors de la fenêtre jouée, ou une colonne obligatoire est absente |
| **2** | un contrôle a échoué : calendriers divergents, tirage non reproduit, ou dates d'Air Liquide différentes de l'expérience 8 |

## Les cas limites

- **Dernière ligne sans `Close`** : ignorée au chargement ; la fenêtre s'arrête au
  2026-09-10.
- **Division un jour de décision** : les titres sont crédités **avant** tout
  ordre de la séance, de sorte que la valeur du portefeuille reste continue.
- **Deux valeurs au même écart** : le tri est stable, et le départage se fait
  alors sur l'ordre de `VALEURS`, qui est fixe.
- **Règles 4 et 6 la même semaine sur la même valeur** : les deux s'exécutent,
  règle 4 puis règle 6, toutes deux dimensionnées sur la même valeur de
  portefeuille. Le cas ne s'est jamais présenté sur l'étalonnage.
- **Espèces insuffisantes** : l'ordre est réduit, et refusé s'il n'atteint pas un
  titre. Le compteur `refus faute d'espèces` est publié même quand il vaut zéro.
- **Position encore ouverte à la dernière séance** : valorisée à la clôture
  réelle du 2026-09-10, marquée *ouverte*, et comptée comme telle au bilan.
- **Moins de deux dates dans une comparaison** : la différence est publiée sans
  intervalle, et le verdict devient *non mesurable*.
