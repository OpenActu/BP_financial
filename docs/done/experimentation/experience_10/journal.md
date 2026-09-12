# `journal.py` — le moteur de l'expérience 10

Miroir d'exécution du moteur. Il décrit **ce que le script fait**, dans l'ordre où
il le fait. Le markdown fait autorité : toute évolution doit d'abord être décrite
ici.

Le **protocole** — le tirage, les sept règles, les quatre conventions de la
règle 7, les deux références, les issues — est dans [`README.md`](README.md).

## Son rôle

Rejouer les six règles de l'[expérience 9](../experience_9/journal.md) sur **dix
valeurs tirées au sort**, en y ajoutant une **septième règle qui vend dès que le
repli depuis le prix d'achat atteint −15 %**, du 2022-01-03 au 2026-09-10, et
écrire les journaux annuels, le bilan, les figures et les cinq CSV.

Il ne lit **aucun** texte rédigé à la main.

## Ce dont il dépend

| Dépendance | Usage |
|---|---|
| `docs/raw/data/quotes/{ENGI,AC,EN,TTE,SAF,AIR,PUB,SGO,MC,CAP}_PA_2019-01-02_2026-09-11.csv` | les dix séries, par [`import_societe.py`](../../../../python/import_societe.md) |
| [`univers.csv`](univers.csv) | les 40 valeurs dans l'ordre du tirage, **revérifié** contre la graine |
| `docs/done/experimentation/experience_9/decisions.csv` | le contrôle de reproduction sur `ENGI.PA` et `SAF.PA` |
| `p_valeur_student()` de [`import_societe.py`](../../../../python/import_societe.md) | les intervalles de Student, par import local |

Bibliothèque standard seule, SVG écrits à la main.

## Son invocation

```bash
python docs/done/experimentation/experience_10/journal.py
python docs/done/experimentation/experience_10/journal.py --figures
python docs/done/experimentation/experience_10/journal.py --markdown
python docs/done/experimentation/experience_10/journal.py --annee 2023
```

| Argument | Défaut | Effet |
|---|---|---|
| `--figures` | absent | écrit les figures de canal, rangées par valeur |
| `--markdown` | absent | écrit les figures, les cinq journaux annuels et le bilan |
| `--annee AAAA` | toutes | n'affiche que cette année ; hors fenêtre jouée : sortie **1** |
| `--repertoire` | le répertoire du script | où lire `univers.csv` et écrire |
| `--quotes` | `docs/raw/data/quotes` | où sont les dix séries |

Sans argument, il calcule tout et n'écrit que les cinq CSV. La dotation, les
parts, le plafond, le **seuil de −15 %** et la **carence de quatre semaines** sont
des **constantes** : ce sont les sept règles, pas des réglages.

## Les constantes déclarées

| Constante | Valeur |
|---|---|
| `VALEURS` | `ENGI.PA`, `AC.PA`, `EN.PA`, `TTE.PA`, `SAF.PA`, `AIR.PA`, `PUB.PA`, `SGO.PA`, `MC.PA`, `CAP.PA` |
| `GRAINE` | **10** |
| `EXEMPTES_TTF` | `AIR.PA` — Airbus SE, société néerlandaise |
| `DOTATION` | 10 000,00 € |
| `PART_ACHAT` · `PART_RENFORT` | 10 % · 20 % du portefeuille, **par valeur** |
| `PLAFOND` | **100 %** de part investie — aucun levier |
| `REPLI_R7` · `CARENCE` | **−15 %** · **4** décisions hebdomadaires |
| `LONGUE` · `COURTE` · `K` | 120 · 20 · 1,0 écart-type |
| `HORIZON` · `PAS_ECHANTILLON` | 20 séances · une décision sur 4 |
| `COURTAGE` · `SPREAD` · `TTF` | 0,100 % · 0,015 % · 0,300 % |
| `ETALONNAGE_PUBLIE` | les nombres du [protocole](README.md#le-dimensionnement-publié-avant-la-fenêtre-jouée) |
| `COUPES_PUBLIEES` | les cinq coupes de la règle 7 sur l'étalonnage, avec leur contrefactuel |

## Le déroulé

### 1. `charger()` — les dix séries, un calendrier unique

Ignore toute ligne sans `Close` — la dernière de chaque série, au 2026-09-11.
Retient `Open`, `High`, `Low`, `Close`, les indicateurs des deux fenêtres et les
`Stock Splits` non nuls. **Exige que les dix calendriers coïncident exactement** :
1 970 séances identiques, sinon arrêt — code **2**.

Aucune des dix ne porte de division sur la fenêtre ; `facteur()` et `reel()` sont
néanmoins implémentés à l'identique de l'expérience 9, et valent l'identité.

### 2. `tirage()` et `controler_univers()`

Rejoue la permutation : les **40** ISIN du CAC 40 du 2019-01-02 triés par ordre
croissant, mélangés par `random.Random(10)`. Compare rang par rang à
`univers.csv`, vérifie que les dix `RETENUE` sont exactement `VALEURS`, et que les
seules `EXAMINEE` sont les **rangs 1 à 13**. Tout écart arrête le moteur —
code **2**.

### 3. `evaluer(valeur, jour)` — en unités ajustées

Rend `None` si la fenêtre de 120 séances est incomplète ou si une variance n'est
pas strictement positive. Sinon, avec
$V_T(n) = \tfrac{n^2-1}{12}$ et
$r_n = \texttt{CORR\_n}\sqrt{\texttt{VAR\_n}/V_T(n)}$ :

$$s_{120} = \sqrt{\tfrac{120}{118}\,\texttt{VAR\_120}\,(1-\texttt{CORR\_120}^2)},
\qquad \texttt{TAUX\_n} = 100\,r_n/\texttt{E\_n}$$

et l'écart réduit `(Close − VAL_120)/s_120`. Les résultats sont mis en cache : le
moteur évalue 10 valeurs sur 1 970 séances, cinq fois.

### 4. `decisions_hebdomadaires(debut, fin)`

La **dernière séance de chaque semaine civile** où **les dix** sont évaluables.
Première évaluation possible : le **2019-06-21**.

### 5. `taux_achat(valeur)` — la TTF n'est pas due par tout le monde

Courtage 0,100 % + demi-spread 0,015 %, plus **TTF 0,300 % sauf pour `AIR.PA`**.
Soit 0,530 % l'aller-retour pour neuf valeurs, **0,230 %** pour Airbus. La vente
ne porte jamais la TTF.

### 6. `simuler(debut, fin, avec_r4, avec_r6, avec_r7)` — l'ordre exact d'une séance

Pour chaque séance, dans cet ordre et pas un autre :

1. **les attributions d'actions gratuites sont créditées** — sans effet ici,
   aucune des dix n'en porte ;
2. ⚠️ **la règle 7 est constatée avant tout le reste**, sur la clôture de la
   veille, **qu'elle soit ou non un jour de décision** : toute position dont la
   clôture ajustée est passée **sous son seuil figé** est vendue à l'ouverture du
   jour. C'est l'entorse déclarée à la règle 2 ;
3. la valeur coupée entre en **carence** : elle ne pourra être rachetée par la
   règle 3 qu'après **quatre décisions hebdomadaires**, et elle est **exclue des
   signaux de la séance même** — on ne rachète pas ce qu'on vient de couper ;
4. si la **veille** était une décision, les signaux des dix valeurs sont
   collectés sans qu'aucun ordre ne soit encore passé : **vente** (règle 5),
   **achat** (règle 3, si la carence est purgée), sinon **règle 4** et
   **règle 6** ;
5. **les ventes de la règle 5 s'exécutent** à l'ouverture réelle ;
6. **les achats s'exécutent ensuite, triés par écart croissant** — le plus
   négatif d'abord —, tous dimensionnés sur **la même** valeur de portefeuille :
   celle de la clôture de la décision, avant tout ordre ;
7. chaque achat est **borné par les espèces** : quantité
   $\lfloor \min(\text{montant}, \text{espèces}) / (\text{prix}(1+\text{frais}))\rfloor$ ;
   à zéro titre, l'ordre est **refusé et compté** ;
8. un achat de la **règle 3** arme **deux** seuils, tous deux figés jusqu'à la
   sortie : celui de la règle 4, à `clôture de la décision − 1 s₁₂₀`, et celui de
   la **règle 7**, à `prix d'exécution ajusté × 0,85`. Ni un renfort ni une
   règle 4 ne les déplacent ;
9. **valorisation** : espèces, puis titres aux clôtures réelles du jour.

Une vente — règle 5 ou règle 7 — solde la position entière de cette valeur,
tranches comprises, et désarme ses deux seuils. Les autres valeurs ne sont pas
touchées.

> **Le conflit règle 7 / règle 4 est tranché par l'ordre même du déroulé** : la
> règle 7 s'exécute à l'étape 2, les renforts à l'étape 6. On ne renforce jamais
> une ligne coupée le matin même. Le moteur **compte** les séances où les deux
> étaient remplies.

`simuler` est appelé **cinq fois** : la variante déclarée, puis **sans la
règle 7** — qui est exactement la règle de l'expérience 9 —, sans la règle 4,
sans la règle 6, et sans les règles 4 et 6.

### 7. `detention()` et `appariee()`

`detention()` place **un dixième de la dotation sur chacune des dix** à
l'ouverture de la deuxième séance, en parties entières, TTF due valeur par
valeur, et garde jusqu'au bout. `appariee()` rend la base 100 d'un placement qui
subit chaque séance le rendement du panier **dans la proportion où le
portefeuille était investi la veille**. L'**alpha officiel** est
`base − appariée`.

`ecart_type(a, b)` rend l'écart-type annualisé de la différence des rendements
quotidiens ; l'effet minimal détectable vaut `1,96 ×` cette valeur.

### 8. `mesurer_positions()`

Pour chaque position : sa valeur, ses dates, son motif de sortie — `VENTE`,
`REGLE-7` ou *ouverte* —, ses tranches, son prix de revient moyen, **le prix de sa
première tranche**, son prix de sortie, sa plus-value, son **repli maximal**
rapporté à la **première tranche** — en clôture et sur les `Low` — et rapporté au
prix moyen, sa durée et sa contribution en euros.

> Les deux conventions de repli sont publiées côte à côte : le repli rapporté au
> **prix moyen** est plus clément d'environ deux points sur les positions à
> plusieurs tranches, parce que les renforts postérieurs au creux abaissent le
> prix de revient. Celui que la **règle 7 surveille** est celui de la première
> tranche.

### 9. `contrefactuel_r7()` — ce que la règle 7 a réellement coupé

Rapproche chaque position coupée par la règle 7 de **la position de même valeur et
de même date d'achat** dans la variante *sans la règle 7*, et publie ce qu'elle
serait devenue : motif de sortie, date, résultat, contribution en euros. Le bilan
en tire le compte des **bonnes et des mauvaises coupes**, et l'écart cumulé.

C'est la mesure qui décide si la règle 7 protège ou coûte — l'étalonnage
l'annonçait **coûteuse de 208 €** sur cinq coupes.

### 10. `issues()` et `comparer()` — par grappes de dates

`issues()` rend une ligne par **(décision, valeur)** : les quatre états déclarés,
l'appartenance au sous-échantillon — une décision sur 4, de sorte que deux
décisions retenues ne partagent aucune des 20 séances de l'horizon — et
`RENDEMENT_20`. Sans 20 séances disponibles, la cellule reste **vide**.

`comparer()` n'agrège pas les observations : les dix valeurs d'une même date
partagent le marché du jour. La méthode, héritée de l'[expérience
5](../experience_5/README.md) :

1. ne retenir que les dates du sous-échantillon où **les deux groupes** ont au
   moins une observation ;
2. à chaque date, la **différence des moyennes** des deux groupes ;
3. Student sur ces différences, à **`nombre de dates − 1`** degrés de liberté,
   quantile obtenu par **dichotomie** sur `p_valeur_student()`.

La quatrième issue — **règle 7, seuil** — compare les évaluations dont le repli
courant dépasse −15 % aux autres évaluations sous le bord bas.

### 11. Les deux contrôles de reproduction

`controler_univers()` (§ 2) et `controler_evaluations_experience_9()`, qui relit
`experience_9/decisions.csv` et exige que l'écart réduit et `TAUX_20` d'`ENGI.PA`
et `SAF.PA` coïncident à 5 × 10⁻⁴ près. Ces quantités **ne dépendent pas du
portefeuille** : elles doivent coïncider. Un écart arrête le moteur — code **2**.

Les quantités et les dates d'ordre, elles, ne sont **pas** contrôlées : le
portefeuille diffère, comme l'expérience 9 le déclarait face à l'expérience 8.

### 12. `etalonnage()` et `ecarts_publies()`

Rejoue les cinq variantes sur **2019-06-21 → 2021-12-31**, compare chaque nombre à
`ETALONNAGE_PUBLIE` et chaque coupe à `COUPES_PUBLIEES`. Tout écart est imprimé
`ECART ETALONNAGE …` et compté au bilan. **Le README n'est jamais corrigé après
coup.**

## Les figures

`figure_canal(valeur, jour)` écrit `graphiques/{TICKER}/canal-{DATE}.svg` : les
120 clôtures ajustées, la droite et sa bande `± 1 s`, la droite sur 20 séances et
l'**enveloppe de ses résidus**, le **seuil de la règle 4** en violet et le **seuil
de la règle 7** en rouge quand ils sont armés, et le verdict du jour. Une figure
par décision produisant un ordre, et une par valeur à la dernière décision de
chaque année.

`svg_portefeuille()` écrit `graphiques/portefeuille-{ANNEE}.svg` : portefeuille,
référence appariée et détention en base 100, avec un trait vertical par
exécution. Les échelles ne lisent **aucune** séance postérieure à la date tracée.

## Les journaux annuels et le bilan

`rapports/{ANNEE}.md` : le compte de l'année, la courbe, les ordres avec leur
motif engendré et leur rang de service, les positions par valeur, les décisions
notables, et la lecture de l'année, entièrement calculée.

`bilan.md` : le compte, les positions, la répartition par valeur, **ce que la
règle 7 a coupé et son contrefactuel**, ce que coûte ou rapporte chaque règle,
les taux de déclenchement, les quatre issues par grappes, la confrontation de
l'étalonnage, les deux contrôles de reproduction, et ce que l'expérience établit
ou n'établit pas.

## L'affichage console

Un bloc par année, puis le bilan : alpha officiel et son EMD, écart brut, frais,
part investie et maximum, déclenchements, **coupes de la règle 7 et leur
contrefactuel**, refus faute d'espèces, achats bloqués par la carence, apport de
chaque règle, répartition par valeur, issues, et toute ligne `ECART ETALONNAGE`.

## Les fichiers écrits

| Fichier | Colonnes |
|---|---|
| `decisions.csv` | `DATE`, `TICKER`, `EXECUTION`, `CLOSE_AJUSTE`, `CLOSE_REEL`, `VAL_120`, `S_120`, `ECART_S`, `TAUX_120`, `TAUX_20`, `SOUS_BAS`, `AU_DESSUS`, `SEUIL_4_FRANCHI`, `SEUIL_7_FRANCHI`, `REPLI_COURANT`, `EN_CARENCE`, `SIGNAL` |
| `ordres.csv` | `DATE`, `DATE_DECISION`, `TICKER`, `SENS`, `RANG_SERVICE`, `QUANTITE`, `PRIX_REEL`, `BRUT`, `FRAIS`, `NET`, `ECART_S`, `TAUX_20`, `MOTIF` |
| `positions.csv` | `TICKER`, `ACHAT`, `SORTIE`, `MOTIF`, `TRANCHES`, `QUANTITE`, `PRIX_PREMIERE_TRANCHE`, `PRIX_ACHAT`, `PRIX_SORTIE`, `SEUIL_REGLE_4`, `SEUIL_REGLE_7`, `SEANCES`, `PLUS_VALUE`, `REPLI_PREMIERE`, `REPLI_MOYEN`, `REPLI_LOW`, `CONTRIBUTION` |
| `portefeuille.csv` | `DATE`, `ESPECES`, `TITRES`, `TOTAL`, `BASE100`, `APPARIEE100`, `DETENTION100`, `PART_INVESTIE`, `LIGNES_OUVERTES` |
| `issues.csv` | `DATE`, `TICKER`, `SOUS_BAS`, `TAUX_20_POSITIF`, `AU_DESSUS_HAUT`, `REPLI_SOUS_SEUIL`, `SOUS_ECHANTILLON`, `RENDEMENT_20` |

`SENS` vaut `ACHAT`, `REGLE-4`, `RENFORT`, `VENTE` ou **`REGLE-7`**.
`RANG_SERVICE` est la place dans le tri par écart croissant, et **0 pour une
vente de la règle 7**, qui précède tout. Les booléens s'écrivent `oui` / `non` ;
une grandeur indisponible laisse une **cellule vide**.

## Les codes de sortie

| Code | Cause |
|---|---|
| **0** | tout s'est déroulé |
| **1** | une série manque, `--quotes` n'est pas un répertoire, `--annee` est hors fenêtre, ou une colonne obligatoire est absente |
| **2** | un contrôle a échoué : calendriers divergents, tirage non reproduit, ou évaluations divergentes de l'expérience 9 |

## Les cas limites

- **Règle 7 un jour de décision** : elle passe d'abord, et la valeur est retirée
  des signaux de cette séance — aucun rachat le jour même de la coupe.
- **Règle 7 et règle 5 le même jour** : impossible en pratique — l'une exige une
  clôture très basse, l'autre au-dessus du bord haut — mais si le cas survenait,
  la règle 7 s'exécute et la règle 5 ne trouve plus de position.
- **Carence courant après la fin de fenêtre** : sans effet, elle ne fait que
  bloquer des achats qui n'auront pas lieu.
- **Deux valeurs au même écart** : tri stable, départage par l'ordre de
  `VALEURS`, qui est fixe.
- **Position encore ouverte à la dernière séance** : valorisée à la clôture réelle
  du 2026-09-10, marquée *ouverte*.
- **Moins de deux dates dans une comparaison** : différence publiée sans
  intervalle, verdict *non mesurable*.
- **Aucune coupe de la règle 7 sur la fenêtre jouée** : le § du contrefactuel le
  dit explicitement plutôt que d'afficher un tableau vide — et ce serait, en soi,
  un résultat.
