# `journal.py` — miroir d'exécution

Moteur de l'**expérience 1**. Il tient le journal d'un portefeuille de 10 000 €
sur l'année 2022 : il classe l'univers déclaré chaque fin de mois, en déduit les
ordres, exécute, comptabilise, et produit les graphiques.

Le protocole complet — univers, score, règles de portefeuille, conventions — est
énoncé dans [`README.md`](README.md). **Ce miroir décrit ce que le script fait,
le README dit pourquoi.** En cas de désaccord entre les deux, c'est le README qui
tranche, et ce miroir qui est corrigé.

Le script ne dépend que de la bibliothèque standard (`csv`, `subprocess`, `math`,
`pathlib`, `argparse`, `datetime`). Il **ne va pas sur le réseau** : les séries
doivent avoir été téléchargées au préalable par `python/import_societe.py`.

---

## Arguments de la ligne de commande

| Argument | Défaut | Effet |
|---|---|---|
| `--collecter` | — | Relance la phase 1 : appelle `generer_graph_decision.py` 144 fois et réécrit `criteres.csv`. Sans ce drapeau, le fichier existant est lu tel quel. |
| `--repertoire` | le répertoire du script | Où lire et écrire `criteres.csv`, `classement.csv`, `ordres.csv`, `portefeuille.csv` et `graphiques/`. |
| `--quotes` | `docs/raw/data/quotes` | Où trouver les séries. |
| `--dotation` | `10000` | Dotation initiale, en euros. |
| `--lignes` | `5` | Nombre maximal de lignes détenues simultanément. |
| `--rang-entree` | `5` | Rang au-delà duquel on n'achète pas. |
| `--rang-sortie` | `7` | Rang au-delà duquel on vend. Doit être `>= --rang-entree` (hystérésis). |
| `--mois` | — | N'afficher que le bloc de ce mois (`AAAA-MM`). Sans lui, les douze blocs. |
| `--markdown` | — | Écrit en plus les douze journaux mensuels `2022-MM.md` (§ 6). |

Sortie **1** si un fichier manque, si `--rang-sortie < --rang-entree`, si la
dotation est négative, si `criteres.csv` est absent sans `--collecter`, ou si
`--markdown` est demandé sans `actualites.md` ni `chartiste.md`.

---

## Constantes

```python
UNIVERS = ("AIR.PA", "MC.PA", "OR.PA", "SAN.PA", "BNP.PA", "TTE.PA",
           "SU.PA", "AI.PA", "DG.PA", "CAP.PA", "RI.PA", "ORA.PA")
REFERENCE   = "TR12"          # indice de reference, rendement total
DEBUT       = "2022-01-03"    # premiere seance de l'experience
FIN         = "2022-12-30"    # derniere seance de l'experience
COURTAGE    = 0.10            # % par sens
SPREAD      = 0.015           # % par sens (un demi-spread complet)
TTF         = 0.30            # % a l'achat
EXEMPTES_TTF = ("AIR.PA",)    # immatriculee hors France
```

Les douze **dates de décision** sont les dernières séances de décembre 2021 à
novembre 2022 ; les douze **dates d'exécution** sont les premières séances des
mois suivants. Elles sont lues dans le calendrier de `TR12`, jamais codées en dur.

---

## Phase 1 — la collecte des critères (`--collecter`)

Pour chacun des 144 couples (valeur, date de décision), le script lance en
sous-processus :

```
python python/generer_graph_decision.py --csv <serie> --indice <TR12> --date <d> --sortie <jetable>
```

C'est **le code du dépôt qui calcule la règle**, jamais une réimplémentation : les
cinq critères, les quatre vetos et le verdict viennent tels quels de
[`python/generer_graph_decision.md`](../../../../python/generer_graph_decision.md).
Le SVG produit est écrit dans un fichier jetable et effacé.

La sortie console est analysée par expressions régulières pour en extraire :

| Champ | Ligne source |
|---|---|
| `TEND_120`, `TEND_20` | `Critère 1` et `Critère 2` |
| `POSITION` | `Critère 3`, en % de la hauteur |
| `ALPHA`, `ALPHA_BAS`, `ALPHA_HAUT` | `Critère 4`, valeur et bornes de l'IC95 |
| `MOMENTUM` | `Critère 5`, en % |
| `VETOS` | ligne `Vetos` (`aucun`, ou la liste) |
| `VERDICT` | ligne `VERDICT` |

Un critère non calculé (historique trop court, aucune date commune avec l'indice)
donne une **cellule vide** — jamais `0`, jamais `nan`. Si le sous-processus sort
en erreur, la ligne est écrite avec toutes ses cellules vides et le message est
repris dans `VERDICT`.

Le résultat est écrit dans `criteres.csv` :

```
DATE,TICKER,CLOSE,TEND_120,TEND_20,POSITION,ALPHA,ALPHA_BAS,ALPHA_HAUT,MOMENTUM,VETOS,VERDICT
```

La collecte prend deux à trois minutes. Elle est **idempotente** : relancée, elle
réécrit exactement le même fichier.

---

## Phase 2 — le score et le classement

Le score est la somme de cinq composantes, **déclarées avant l'expérience** et
tirées des cinq critères de la règle. Chacune est un petit entier, ce qui rend le
classement lisible et reproductible à la main.

| Composante | Source | Valeurs |
|---|---|---|
| `s1` | tendance longue `TEND_120` | `+2` si `+1`, `0` si `0`, `-2` si `-1` |
| `s2` | tendance courte `TEND_20` | `+1` / `0` / `-1`, à l'identique |
| `s3` | position dans l'encadrement actif | `+1` si `>= 50 %`, `0` si `20 %` à `50 %`, `-1` si `< 20 %` |
| `s4` | momentum 12-1 | `+2` si `> +10 %`, `+1` si `0` à `+10 %`, `-1` si `-10 %` à `0`, `-2` si `< -10 %` |
| `s5` | alpha annualisé contre `TR12` | `+1` si l'IC95 est entièrement positif, `-1` s'il est entièrement négatif, `0` s'il contient zéro |

`score = s1 + s2 + s3 + s4 + s5`, entre `-7` et `+7`.

Une composante dont le critère est vide vaut `0`, et la cellule reste vide dans
`classement.csv` : on distingue « neutre » de « non mesuré ».

**Départage**, dans cet ordre : score décroissant, puis momentum 12-1 décroissant,
puis ticker par ordre alphabétique. Aucune ambiguïté ne subsiste.

Le classement des douze valeurs à chaque date est écrit dans `classement.csv` :

```
DATE,RANG,TICKER,S1,S2,S3,S4,S5,SCORE,POSITION,MOMENTUM,VERDICT_REGLE
```

---

## Phase 3 — les ordres

À chaque date de décision `d`, exécution à la séance suivante `e` :

1. **Ventes d'abord.** Une ligne détenue est vendue si son rang à `d` dépasse
   `--rang-sortie`, ou si son score est `<= -3`. Motif inscrit dans `ordres.csv`.
2. **Achats ensuite**, dans l'ordre du classement. Un titre est acheté s'il est
   classé à `--rang-entree` ou mieux, que son score est `> 0`, qu'il n'est pas
   déjà détenu, et qu'il reste une place parmi les `--lignes`.
3. Les espèces disponibles après les ventes sont **réparties à parts égales**
   entre les titres à acheter. Rien n'est réinvesti dans les lignes déjà tenues :
   il n'y a **aucun rebalancement**, seulement des entrées et des sorties.

**Le prix d'exécution est l'`Open` de la séance `e`**, jamais la clôture de `d`.
La décision est prise après la clôture du dernier jour du mois ; l'ordre ne peut
pas être servi avant l'ouverture suivante. C'est le point qui coûte le plus cher
dans le cas pratique du module 6, et il n'est pas escamoté ici.

**Quantités entières.** Le nombre de titres est `floor(montant / (prix × (1 + frais)))`.
Le reliquat retourne aux espèces. Un montant qui n'achète pas un seul titre ne
produit aucun ordre.

**Frais**, en pourcentage du montant brut :

- achat : `COURTAGE + SPREAD + TTF`, soit `0,415 %` — et `0,115 %` pour `AIR.PA`,
  exemptée de taxe sur les transactions financières ;
- vente : `COURTAGE + SPREAD`, soit `0,115 %`.

L'aller-retour ressort donc à `0,530 %`, et `0,230 %` pour `AIR.PA` — les chiffres
que rend `python/couts_transaction.py` sur le même barème.

`ordres.csv` :

```
DATE,TICKER,SENS,QUANTITE,PRIX,BRUT,FRAIS,NET,RANG,SCORE,MOTIF
```

---

## Phase 4 — la comptabilité

Pour chaque séance de `DEBUT` à `FIN` :

- `TITRES` = somme des `quantité × Close` de chaque ligne détenue ;
- `ESPECES` = dotation, moins les achats nets, plus les ventes nettes ;
- `TOTAL` = `TITRES + ESPECES` ;
- `BASE100` = `100 × TOTAL / dotation` ;
- `REFERENCE100` = `100 × TR12(d) / TR12(DEBUT)`.

Les dividendes ne sont **pas** comptabilisés séparément : la colonne `Close` de
`yfinance` est déjà ajustée des détachements, et `TR12` est construit dans la même
convention. Les deux courbes sont donc comparables — c'est toute la raison d'être
de `TR12`, et l'avertissement central de `CLAUDE.md` sur `^FCHI`.

`portefeuille.csv` :

```
DATE,ESPECES,TITRES,TOTAL,BASE100,REFERENCE100
```

### Les alphas

Convention déclarée : **excédent arithmétique de rendement**, jamais une
régression. Sur vingt et une séances, une régression rendrait un coefficient dont
l'intervalle de confiance couvrirait tout le domaine utile ; l'excédent, lui, est
exactement ce qu'on veut lire.

- alpha mensuel d'une ligne = rendement de la ligne sur le mois − rendement de
  `TR12` sur le même mois ;
- alpha global d'une ligne = rendement depuis son prix d'achat − rendement de
  `TR12` depuis la même séance ;
- alpha du portefeuille = rendement du portefeuille − rendement de `TR12`,
  mensuel et depuis `DEBUT`.

Une ligne entrée en cours de mois n'a pas d'alpha mensuel plein : sa cellule
porte la mention `(partiel)`.

---

## Phase 5 — les graphiques

Douze SVG écrits à la main dans `graphiques/`, un par mois :
`portefeuille-2022-MM.svg`, du `2022-01-03` à la dernière séance du mois `MM`.

Chaque graphique porte deux courbes en base 100 — le portefeuille en trait plein,
`TR12` en trait tireté —, une grille horizontale, les bornes de l'axe des dates,
et **des repères verticaux aux dates d'exécution**. Aucune bibliothèque : le SVG
est un fichier texte, comme dans `generer_graph_supp_resistance.py`.

L'échelle verticale est calculée sur les seules séances tracées. Un graphique
arrêté en mars n'utilise **aucune** valeur d'avril : la règle de non-regard-en-avant
vaut aussi pour les échelles.

---

## Affichage console

Un bloc par mois, prêt à être repris dans le markdown mensuel :

```
=== 2022-03 · decision au 2022-02-28 · execution au 2022-03-01 ===

Classement
  rang  valeur    s1  s2  s3  s4  s5  score  position  momentum  regle
     1  TTE.PA    +2  +1  +1  +2   0     +6     75,3 %   +19,8 %  ATTENTE
   ...

Ordres
  VENTE  MC.PA    12 titres a 601,40 EUR  brut 7 216,80  frais 8,30  motif rang 9 > 7
  ACHAT  TTE.PA   ...

Portefeuille au 2022-03-31
  especes 412,18 EUR - titres 9 733,52 EUR - total 10 145,70 EUR - base 101,46
  TR12 base 96,31 - alpha du mois +2,14 pt - alpha depuis janvier +5,15 pt
```

Les nombres sont mis en forme à la française — virgule décimale, espace insécable
comme séparateur de milliers.

---

## Phase 6 — les douze journaux mensuels et le bilan (`--markdown`)

Le script assemble `rapports/2022-01.md` à `rapports/2022-12.md`, plus le
`bilan-2022.md` de la racine, à partir de trois sources, dont **deux sont des
fichiers de texte rédigés à la main** :

| Source | Rôle |
|---|---|
| `actualites.md` | le préambule de chaque mois, découpé sur les titres `## AAAA-MM` |
| `chartiste.md` | les notes de perspective, découpées sur `## AAAA-MM-JJ` puis `### TICKER` |
| l'état du moteur | tout le reste : chiffres, tableaux, ordres, graphique |

Séparer ainsi le texte des nombres a une raison précise : **aucun chiffre du
journal n'est saisi à la main**, donc aucun ne peut diverger du moteur. Une
relance de `--markdown` réécrit les douze fichiers à l'identique.

Chaque journal mensuel suit le même plan, dans l'ordre voulu par le protocole :

1. un bandeau — dates de décision et d'exécution, valeur du portefeuille, alpha ;
2. **les actualités du mois précédent**, reprises de `actualites.md` ;
3. **l'exposition héritée** à la date de décision : par ligne, date d'achat,
   plus ou moins-value, alpha du mois, alpha global ;
4. **le portefeuille depuis le 3 janvier**, en euros et en base 100, avec le
   graphique du mois ;
5. **l'étude chartiste**, une note de cinq lignes au plus par société ;
6. **le classement** des douze valeurs, du plus intéressant à détenir au plus à
   fuir, avec le détail des cinq composantes ;
7. **les ordres exécutés**, chacun avec son motif chiffré ;
8. **la lecture du mois** — un paragraphe **entièrement calculé** : meilleure et
   pire contribution, frais du mois, écart à la référence. Aucun récit rédigé
   après coup n'y est produit, précisément parce que l'année est passée.

Un mois dont la section manque dans `actualites.md` ou `chartiste.md` reçoit la
mention `*(section absente)*` plutôt qu'un texte inventé — c'est la même règle
que la cellule vide des CSV.

**Les douze journaux vivent dans `rapports/`**, un cran sous la racine de
l'expérience. Leurs liens sont donc relatifs à ce sous-répertoire : `../README.md`
pour le protocole, `../graphiques/portefeuille-2022-MM.svg` pour la figure,
`../bilan-2022.md` pour le bilan, et `2022-MM.md` entre mois voisins.

### Le bilan de l'année — `bilan-2022.md`

Écrit à la racine, parce qu'il n'est pas un rapport mensuel de plus mais la
lecture de l'ensemble. Six sections, **toutes calculées** :

1. **Le compte** — dotation, valeur finale, performance, référence, alpha, ordres,
   frais, repli maximal et sa date.
2. **Mois par mois** — une ligne par mois : valeur, base 100, `TR12`, alpha du
   mois, alpha cumulé, nombre d'ordres.
3. **Les positions** — une ligne par position ouverte dans l'année : dates
   d'achat et de vente, prix, durée en séances, plus ou moins-value, alpha contre
   `TR12` sur la même période, contribution en euros. Une ligne encore ouverte au
   30 décembre est marquée comme telle.
4. **Ce que la rotation a coûté** — frais par sens, et le contrefactuel
   **« janvier tenu toute l'année »** : le même portefeuille initial conservé sans
   un seul ordre jusqu'au 30 décembre. C'est la mesure directe de ce que les
   vingt-deux ordres suivants ont apporté, ou retiré.
5. **Les trois conventions de référence** — le portefeuille, `TR12` en rendement
   total, et `^FCHI` nu, côte à côte, pour montrer sur cette année précise de
   combien le choix de la référence déplace le verdict.
6. **Ce que l'expérience établit, et ce qu'elle n'établit pas** — texte fixe,
   parce que la conclusion méthodologique ne dépend pas du résultat obtenu.

Le `README.md` renvoie à ce fichier, et le journal de décembre s'y termine.

---

## Cas limites

| Situation | Comportement |
|---|---|
| Aucune valeur de score `> 0` à une date | Aucun achat. Le portefeuille reste en espèces, ce qui est un résultat et non une panne. |
| Moins de titres éligibles que de places | On n'ouvre que ce qui est éligible ; les espèces dorment. |
| Espèces insuffisantes pour un titre entier | Aucun ordre pour cette ligne, un avertissement en console. |
| Une série ne couvre pas une date d'exécution | Sortie **1**, avec le nom du fichier. On n'invente pas un prix. |
| Un critère vide | Composante à `0`, cellule vide dans `classement.csv`. |
| Deux valeurs à score et momentum égaux | Départage alphabétique. Le classement est déterministe. |

---

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Journal produit. |
| `1` | Fichier manquant, argument hors domaine, ou date d'exécution non couverte. |

---

## Fonctions internes

- `fr(x, d=2)` — mise en forme française d'un nombre.
- `charger_serie(chemin)` — rend `{date: {"open": …, "close": …}}`.
- `calendrier(dates)` — rend les couples (date de décision, date d'exécution).
- `collecter(dates, quotes, repertoire)` — phase 1.
- `composantes(ligne)` — rend `(s1, s2, s3, s4, s5, score)`.
- `classer(criteres, date)` — rend la liste ordonnée des douze valeurs.
- `executer(etat, classement, date_exec, series)` — rend la liste des ordres.
- `valoriser(etat, dates, series)` — rend la série quotidienne du portefeuille.
- `svg(chemin, dates, portefeuille, reference, executions)` — écrit un graphique.
- `bloc_mensuel(...)` — l'affichage console d'un mois.
