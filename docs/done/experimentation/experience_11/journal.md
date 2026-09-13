# `journal.py` — le moteur de l'expérience 11

Miroir d'exécution du moteur. Il décrit **ce que le script fait**, dans l'ordre où
il le fait. Le markdown fait autorité : toute évolution doit d'abord être décrite
ici.

Le **protocole** — les six règles, l'univers, l'étalonnage, les trois contrôles de
reproduction — est dans [`README.md`](README.md).

## Son rôle

Rejouer la règle de l'[expérience 10](../experience_10/journal.md) **privée de sa
règle 7**, sur les dix mêmes valeurs, du 2022-01-03 au 2026-09-10, et écrire les
journaux annuels, le bilan, les figures et les cinq CSV.

Il ne lit **aucun** texte rédigé à la main. Tous les chiffres publiés sortent de
son calcul.

> **Sa particularité.** Ce moteur est le seul du dépôt dont le résultat est connu
> **avant** son écriture : il doit retrouver, **ordre par ordre**, la variante
> « sans la règle 7 » de l'expérience 10. Ce n'est pas une mesure nouvelle, c'est
> une reproduction — et le moteur s'arrête si elle échoue.

## Ce dont il dépend

| Dépendance | Usage |
|---|---|
| `docs/raw/data/quotes/{ENGI,AC,EN,TTE,SAF,AIR,PUB,SGO,MC,CAP}_PA_2019-01-02_2026-09-11.csv` | les dix séries, par [`import_societe.py`](../../../../python/import_societe.md) |
| [`univers.csv`](univers.csv) | les 40 valeurs dans l'ordre du tirage, **revérifié** contre la graine 10 |
| `docs/done/experimentation/experience_9/decisions.csv` | contrôle sur `ENGI.PA` et `SAF.PA` |
| `docs/done/experimentation/experience_10/journal.py` | **le contrôle ordre par ordre** : sa variante sans règle 7 est rejouée et confrontée |
| `p_valeur_student()` de [`import_societe.py`](../../../../python/import_societe.md) | les intervalles de Student, par import local |

Bibliothèque standard seule, SVG écrits à la main.

## Son invocation

```bash
python docs/done/experimentation/experience_11/journal.py
python docs/done/experimentation/experience_11/journal.py --figures
python docs/done/experimentation/experience_11/journal.py --markdown
python docs/done/experimentation/experience_11/journal.py --annee 2023
```

| Argument | Défaut | Effet |
|---|---|---|
| `--figures` | absent | écrit les figures de canal, rangées par valeur |
| `--markdown` | absent | écrit les figures, les cinq journaux annuels et le bilan |
| `--annee AAAA` | toutes | n'affiche que cette année ; hors fenêtre jouée : sortie **1** |
| `--repertoire` | le répertoire du script | où lire `univers.csv` et écrire |
| `--quotes` | `docs/raw/data/quotes` | où sont les dix séries |
| `--sans-controle-10` | absent | saute le contrôle ordre par ordre contre l'expérience 10 — **uniquement** si son moteur est absent ou déplacé, jamais pour faire taire un écart |

Sans argument, il calcule tout et n'écrit que les cinq CSV. La dotation, les
parts et le plafond sont des **constantes** : ce sont les six règles, pas des
réglages.

## Les constantes déclarées

| Constante | Valeur |
|---|---|
| `VALEURS` | `ENGI.PA`, `AC.PA`, `EN.PA`, `TTE.PA`, `SAF.PA`, `AIR.PA`, `PUB.PA`, `SGO.PA`, `MC.PA`, `CAP.PA` |
| `GRAINE` | **10** — le tirage de l'expérience 10, inchangé |
| `EXEMPTES_TTF` | `AIR.PA` — Airbus SE, société néerlandaise |
| `DOTATION` | 10 000,00 € |
| `PART_ACHAT` · `PART_RENFORT` | 10 % · 20 % du portefeuille, **par valeur** |
| `PLAFOND` | **100 %** de part investie — aucun levier |
| `LONGUE` · `COURTE` · `K` | 120 · 20 · 1,0 écart-type |
| `HORIZON` · `PAS_ECHANTILLON` | 20 séances · une décision sur 4 |
| `COURTAGE` · `SPREAD` · `TTF` | 0,100 % · 0,015 % · 0,300 % |
| `ETALONNAGE_PUBLIE` | les nombres du [protocole](README.md#létalonnage-2019-2021-recalculé-sans-la-règle-7) |
| `RESULTAT_PUBLIE` | le résultat de la fenêtre jouée, **publié en tête du protocole** |

**Aucune constante de règle 7** : ni seuil de repli, ni carence. Elles n'existent
pas dans ce moteur.

## Le déroulé

### 1. `charger()` — les dix séries, un calendrier unique

Ignore toute ligne sans `Close` — la dernière de chaque série, au 2026-09-11.
**Exige que les dix calendriers coïncident exactement** : 1 970 séances
identiques, sinon arrêt — code **2**.

Aucune des dix ne porte de division sur la fenêtre ; `facteur()` et `reel()` sont
implémentés à l'identique de l'expérience 10 et valent l'identité.

### 2. `tirage()` et `controler_univers()`

Rejoue la permutation : les **40** ISIN triés par ordre croissant, mélangés par
`random.Random(10)`. Compare rang par rang à `univers.csv`, vérifie que les dix
`RETENUE` sont exactement `VALEURS`, et que les seules `EXAMINEE` sont les
**rangs 1 à 13**. Tout écart arrête le moteur — code **2**.

### 3. `evaluer(valeur, jour)` — en unités ajustées

Rend `None` si la fenêtre de 120 séances est incomplète ou si une variance n'est
pas strictement positive. Sinon, avec $V_T(n) = \tfrac{n^2-1}{12}$ et
$r_n = \texttt{CORR\_n}\sqrt{\texttt{VAR\_n}/V_T(n)}$ :

$$s_{120} = \sqrt{\tfrac{120}{118}\,\texttt{VAR\_120}\,(1-\texttt{CORR\_120}^2)},
\qquad \texttt{TAUX\_n} = 100\,r_n/\texttt{E\_n}$$

et l'écart réduit `(Close − VAL_120)/s_120`. Les résultats sont mis en cache.

### 4. `decisions_hebdomadaires(debut, fin)`

La **dernière séance de chaque semaine civile** où **les dix** sont évaluables.
Première évaluation possible : le **2019-06-21**.

### 5. `taux_achat(valeur)`

Courtage 0,100 % + demi-spread 0,015 %, plus **TTF 0,300 % sauf pour `AIR.PA`**.
Soit 0,530 % l'aller-retour pour neuf valeurs, **0,230 %** pour Airbus. La vente
ne porte jamais la TTF.

### 6. `simuler(debut, fin, avec_r4, avec_r6)` — l'ordre exact d'une séance

Pour chaque séance de la fenêtre, dans cet ordre :

1. **les attributions d'actions gratuites sont créditées** — sans effet ici ;
2. si la **veille** était une décision, les signaux des dix valeurs sont
   collectés **sans qu'aucun ordre ne soit encore passé** : **vente** (règle 5) si
   la valeur est détenue et clôture au-dessus du bord haut ; **achat** (règle 3)
   si elle ne l'est pas, clôture sous le bord bas et `TAUX_20 ≥ 0` ; sinon
   **règle 4** si la clôture passe sous le seuil figé et que la règle n'a pas déjà
   joué, et **règle 6** si la décision suit immédiatement l'achat, que la clôture
   est encore sous le bord bas avec `TAUX_20 ≥ 0`, et que le renfort n'a pas eu
   lieu ;
3. **les ventes s'exécutent d'abord**, à l'ouverture réelle : elles libèrent les
   espèces qui financeront les achats de la même séance ;
4. **les achats s'exécutent ensuite, triés par écart croissant** — le plus négatif
   d'abord —, tous dimensionnés sur **la même** valeur de portefeuille : celle de
   la clôture de la décision, avant tout ordre ;
5. chaque achat est **borné par les espèces disponibles** : quantité
   $\lfloor \min(\text{montant}, \text{espèces}) / (\text{prix}(1+\text{frais}))\rfloor$ ;
   à zéro titre, l'ordre est **refusé et compté** — il l'a été **11 fois** sur la
   fenêtre jouée, contre une seule avec la règle 7 ;
6. un achat de la **règle 3** arme le seuil de la règle 4, à
   `clôture de la décision − 1 s₁₂₀`, **figé** jusqu'à la vente. Un renfort ne le
   déplace pas ;
7. **valorisation** : espèces, puis titres aux clôtures réelles du jour.

Une vente solde la position entière de cette valeur, tranches comprises, et
désarme son seuil. **La règle 5 est la seule sortie** : une position qui ne
revient pas dans sa bande reste ouverte jusqu'au 2026-09-10.

`simuler` est appelé **quatre fois** : la variante déclarée, puis sans la règle 4,
sans la règle 6, et sans les deux. Seule la déclarée produit journaux, figures et
CSV.

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
première tranche — en clôture et sur les `Low` — et rapporté au prix moyen, sa
durée et sa contribution en euros.

> Les deux conventions de repli sont publiées côte à côte : rapporté au **prix
> moyen**, le repli est plus clément d'environ deux points sur les positions à
> plusieurs tranches, les renforts postérieurs au creux abaissant le prix de
> revient.

### 9. `issues()` et `comparer()` — par grappes de dates

`issues()` rend une ligne par **(décision, valeur)** : les trois états déclarés,
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

**Il n'y a que trois issues** : celle de la règle 7 disparaît avec elle.

### 10. Les trois contrôles de reproduction

| Fonction | Ce qu'elle exige | Échec |
|---|---|---|
| `controler_univers()` | la permutation se rejoue depuis la graine 10 | code **2** |
| `controler_evaluations_experience_9()` | l'écart réduit et `TAUX_20` d'`ENGI.PA` et `SAF.PA` coïncident à 5 × 10⁻⁴ près avec `experience_9/decisions.csv` | code **2** |
| `controler_ordres_experience_10()` | ⚠️ **les 112 ordres coïncident un par un** avec la variante sans règle 7 de l'expérience 10 | code **2** |

`controler_ordres_experience_10()` charge le moteur voisin par son chemin,
exécute `simuler(..., avec_r7=False)` sur la même fenêtre, et compare **date,
valeur, sens, quantité et prix** ordre par ordre. Le premier écart est nommé et
arrête le moteur.

C'est le contrôle **le plus strict du dépôt** : là où l'expérience 9 ne pouvait
comparer que des **dates** à l'expérience 8 — les quantités dépendant d'un
portefeuille différent —, ici le portefeuille est le même, donc **les quantités
doivent coïncider**. Si le moteur voisin est absent, le contrôle est **déclaré
sauté** en console et au bilan, jamais silencieusement ignoré.

### 11. `etalonnage()` et `ecarts_publies()`

Rejoue les quatre variantes sur **2019-06-21 → 2021-12-31** et compare chaque
nombre à `ETALONNAGE_PUBLIE`. Confronte en outre le résultat de la fenêtre jouée à
`RESULTAT_PUBLIE`, ce qu'aucune expérience antérieure ne pouvait faire — le
résultat y était inconnu à l'écriture. Tout écart est imprimé
`ECART ETALONNAGE …` ou `ECART RESULTAT …` et compté au bilan.

> **Un compteur qui se lit de travers, et que le bilan explique.** Dans la
> variante « sans la règle 4 », `règle 4 possible` vaut 89 et non 16 : le
> compteur mesure les semaines où la règle *aurait pu* jouer, et une règle
> désactivée laisse la position sous son seuil semaine après semaine. Seul le
> nombre de la variante déclarée est un taux de déclenchement.

## Les figures

`figure_canal(valeur, jour)` écrit `graphiques/{TICKER}/canal-{DATE}.svg` : les
120 clôtures ajustées, la droite et sa bande `± 1 s`, la droite sur 20 séances et
l'**enveloppe de ses résidus**, le **seuil de la règle 4** en violet quand il est
armé, et le verdict du jour. **Aucun seuil rouge** : il n'y a plus de règle 7. Une
figure par décision produisant un ordre, et une par valeur à la dernière décision
de chaque année.

`svg_portefeuille()` écrit `graphiques/portefeuille-{ANNEE}.svg` : portefeuille,
référence appariée et détention en base 100, avec un trait vertical par exécution.
Les échelles ne lisent **aucune** séance postérieure à la date tracée.

## Les journaux annuels et le bilan

`rapports/{ANNEE}.md` : le compte de l'année, la courbe, les ordres avec leur
motif engendré et leur rang de service, les positions par valeur, les décisions
notables, et la lecture de l'année, entièrement calculée.

`bilan.md` : le compte, les positions, la répartition par valeur, ce que coûte
l'absence de sortie en perte, ce qu'ajoutent les règles 4 et 6, les taux de
déclenchement, les trois issues par grappes, la confrontation de l'étalonnage
**et du résultat publié**, les trois contrôles de reproduction, la **comparaison
position par position avec l'expérience 10**, et ce que l'expérience établit ou
n'établit pas.

## L'affichage console

Un bloc par année, puis le bilan : alpha officiel et son EMD, écart brut, frais,
part investie et maximum, **ordres refusés faute d'espèces**, déclenchements,
apport de chaque règle, répartition par valeur, issues, résultat des trois
contrôles, et toute ligne `ECART ETALONNAGE` ou `ECART RESULTAT`.

## Les fichiers écrits

| Fichier | Colonnes |
|---|---|
| `decisions.csv` | `DATE`, `TICKER`, `EXECUTION`, `CLOSE_AJUSTE`, `CLOSE_REEL`, `VAL_120`, `S_120`, `ECART_S`, `TAUX_120`, `TAUX_20`, `SOUS_BAS`, `AU_DESSUS`, `SEUIL_4_FRANCHI`, `REPLI_COURANT`, `SIGNAL` |
| `ordres.csv` | `DATE`, `DATE_DECISION`, `TICKER`, `SENS`, `RANG_SERVICE`, `QUANTITE`, `PRIX_REEL`, `BRUT`, `FRAIS`, `NET`, `ECART_S`, `TAUX_20`, `MOTIF` |
| `positions.csv` | `TICKER`, `ACHAT`, `SORTIE`, `MOTIF`, `TRANCHES`, `QUANTITE`, `PRIX_PREMIERE_TRANCHE`, `PRIX_ACHAT`, `PRIX_SORTIE`, `SEUIL_REGLE_4`, `SEANCES`, `PLUS_VALUE`, `REPLI_PREMIERE`, `REPLI_MOYEN`, `REPLI_LOW`, `CONTRIBUTION` |
| `portefeuille.csv` | `DATE`, `ESPECES`, `TITRES`, `TOTAL`, `BASE100`, `APPARIEE100`, `DETENTION100`, `PART_INVESTIE`, `LIGNES_OUVERTES` |
| `issues.csv` | `DATE`, `TICKER`, `SOUS_BAS`, `TAUX_20_POSITIF`, `AU_DESSUS_HAUT`, `SOUS_ECHANTILLON`, `RENDEMENT_20` |

`SENS` vaut `ACHAT`, `REGLE-4`, `RENFORT` ou `VENTE` — **jamais `REGLE-7`**.
`RANG_SERVICE` est la place dans le tri par écart croissant, 1 pour le premier
servi. Les booléens s'écrivent `oui` / `non` ; une grandeur indisponible laisse
une **cellule vide**.

## Les codes de sortie

| Code | Cause |
|---|---|
| **0** | tout s'est déroulé |
| **1** | une série manque, `--quotes` n'est pas un répertoire, `--annee` est hors fenêtre, ou une colonne obligatoire est absente |
| **2** | un contrôle a échoué : calendriers divergents, tirage non reproduit, évaluations divergentes de l'expérience 9, ou **ordres divergents de l'expérience 10** |

## Les cas limites

- **Deux valeurs au même écart** : tri stable, départage par l'ordre de `VALEURS`,
  qui est fixe.
- **Espèces insuffisantes** : l'ordre est réduit à ce qu'elles permettent, et
  refusé s'il n'atteint pas un titre. Le compteur est publié même à zéro — il vaut
  **11** ici, et c'est un résultat.
- **Position encore ouverte à la dernière séance** : valorisée à la clôture réelle
  du 2026-09-10, marquée *ouverte*, et comptée comme telle au bilan.
- **Moins de deux dates dans une comparaison** : différence publiée sans
  intervalle, verdict *non mesurable*.
- **Moteur de l'expérience 10 absent** : le contrôle ordre par ordre est sauté, et
  **le bilan l'écrit** au lieu de laisser croire qu'il a réussi.
