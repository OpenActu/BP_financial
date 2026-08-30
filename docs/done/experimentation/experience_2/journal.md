# journal.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/done/experimentation/experience_2/journal.py`, étape par étape, dans
l'ordre du déroulement. Il fait autorité : toute évolution du script doit
d'abord être décrite ici.

Le **protocole** — l'univers, le score, les seuils, les coûts, les cinq
corrections apportées à l'expérience 1 — est dans [`README.md`](README.md). Ce
miroir décrit le moteur qui l'applique.

## Rôle

Conduire mécaniquement le portefeuille de l'expérience 2 : classer l'univers à
chaque fin de mois, appliquer les vetos, en déduire les ordres, les exécuter à
l'ouverture suivante, tenir la comptabilité, engendrer et **dépouiller** les
thèses réfutables, tracer les graphiques, et écrire les douze journaux mensuels
puis le bilan.

Le moteur ajoute quatre choses au moteur de l'expérience 1, une par piste
retenue par [la revue](../experience_1/review.md) :

| Piste | Ce que le moteur fait en plus |
|---|---|
| **T3** | il lit les **vetos** dans la sortie de la règle et les **applique** à l'entrée ; il mesure les **poids effectifs** du score |
| **C3** | il simule **deux portefeuilles** — `s3` aligné, et `s3` au sens de l'expérience 1 |
| **C4** | il collecte **support, résistance, pentes, épisodes et τ**, et recalcule le score **à d−1 et d−2 séances** |
| **S4** | il écrit **deux thèses réfutables** par valeur et par date, et les **dépouille** à la date suivante |
| **T1** | il republie au bilan le **dimensionnement** déclaré avant, confronté à la tracking error réalisée |

> ⚠️ **Aucune décision n'est prise à la main.** Le classement, les vetos, les
> ordres et les thèses sortent tous de quantités calculées. Le seul texte rédigé
> à la main est dans [`actualites.md`](actualites.md) et
> [`chartiste.md`](chartiste.md), et le moteur n'en fait que la mise en page.

## Dépendances

- Modules standard uniquement : `argparse`, `csv`, `math`, `re`, `statistics`,
  `subprocess`, `sys`, `pathlib`, `concurrent.futures`.
- **Aucune bibliothèque de tracé** : les SVG sont écrits à la main.
- Il lance [`python/generer_graph_decision.py`](../../../../python/generer_graph_decision.md)
  en sous-processus et lit sa console. **Les cinq critères, les vetos et
  l'encadrement ne sont jamais réimplémentés ici.**

## Invocation

```bash
python docs/done/experimentation/experience_2/journal.py --collecter
python docs/done/experimentation/experience_2/journal.py --markdown
python docs/done/experimentation/experience_2/journal.py --mois 2025-03
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `--collecter` | — | relance les 720 évaluations de la règle et réécrit `criteres.csv` |
| `--markdown` | — | écrit aussi les douze journaux, le bilan et les graphiques |
| `--mois` | — | n'affiche en console que ce mois (`AAAA-MM`) |
| `--repertoire` | le répertoire du script | où lire et écrire |
| `--quotes` | `docs/raw/data/quotes` | où sont les séries |
| `--dotation` | `10000.0` | dotation en euros |
| `--lignes` | `5` | lignes détenues au maximum |
| `--rang-entree` | `5` | rang d'achat |
| `--rang-sortie` | `7` | rang de vente |
| `--repartition` | `creneaux` | diviser les espèces par les créneaux libres, ou par les candidats |
| `--recollecter` | — | repartir de zéro au lieu de compléter `criteres.csv` |
| `--taches` | `8` | sous-processus simultanés pendant la collecte |
| `--sans-veto` | — | **diagnostic** : simule la règle sans appliquer les vetos |

`--rang-sortie` inférieur à `--rang-entree` : sortie **1** (l'hystérésis serait
inversée). `--dotation` négative ou nulle : sortie **1**. `--lignes` hors de
`[1, 12]` : sortie **1**. `--taches` hors de `[1, 32]` : sortie **1**.

> 🔑 **`--taches` ne change aucun résultat.** L'essentiel de la durée d'une
> évaluation est l'import de `pandas` par le sous-processus, pas le calcul ; les
> lancer à plusieurs divise le temps de collecte sans rien changer d'autre.
> `collecter()` range les lignes dans **l'ordre des tâches**, jamais dans celui
> des retours, si bien que `criteres.csv` est identique d'une exécution à
> l'autre quelle que soit la valeur de `--taches`. Chaque tâche écrit son SVG
> jetable dans un fichier qui lui est propre, et tous sont effacés à la fin.

> **La collecte est reprenable.** `--collecter` conserve les lignes déjà
> présentes dans `criteres.csv`, n'évalue que ce qui manque, et **dépose le
> fichier tous les `CADENCE_ECRITURE` résultats** : une collecte interrompue
> reprend où elle en était au lieu de tout perdre. `--recollecter` repart de
> zéro — c'est ce qu'il faut faire dès que la règle elle-même a changé, sans
> quoi des lignes anciennes cohabiteraient avec des lignes neuves sans que rien
> ne le signale.

> `--sans-veto` ne sert qu'à chiffrer ce que les vetos changent : il ajoute au
> flux console un bloc comparant la base 100 et le nombre d'ordres avec et sans
> vetos. Il ne modifie aucun CSV ni aucun markdown publié. Le protocole déclaré
> applique les vetos, sans option.

## Les constantes déclarées

| Constante | Valeur | Rôle |
|---|---|---|
| `UNIVERS` | les 12 tickers du README | l'univers, fixé |
| `REFERENCE` | `TR12` | la référence en rendement total |
| `REFERENCE_NUE` | `^FCHI` | l'indice nu, pour la section « trois conventions » |
| `DEBUT_SERIE` / `FIN_SERIE` | `2021-01-04` / `2025-12-31` | la plage des CSV, **déclarée** et non devinée par glob |
| `MOIS_AUDIT_DEBUT` | `2022-12` | mois de la première décision d'audit |
| `MOIS_INVESTI_DEBUT` | `2024-12` | mois de la première décision investie |
| `MOIS_ETALONNAGE_FIN` | `2024-11` | dernier mois de décision de la fenêtre d'étalonnage |
| `ANNEE` | `2025` | l'année narrée |
| `SEUIL_BAS` / `SEUIL_HAUT` | `35.0` / `65.0` | les seuils de `s3` **aligné** |
| `SEUIL_BAS_FANTOME` / `SEUIL_HAUT_FANTOME` | `20.0` / `50.0` | les seuils de `s3` au sens de l'expérience 1 |
| `CADENCE_ECRITURE` | `48` | dépôt intermédiaire de `criteres.csv` pendant la collecte |
| `TE_DECLAREE` | `8.20` | la tracking error de l'expérience 1, publiée au README |
| `TOLERANCE_REFLEXIVE` | `5.0` | la demi-largeur, en %, de la clause « aucune séquence » |
| `DECALAGES` | `(1, 2)` | les décalages rétrospectifs de la piste C4 |
| `COURTAGE` / `SPREAD` / `TTF` | `0.10` / `0.015` / `0.30` | en %, barème de `couts_transaction.py` |
| `EXEMPTES_TTF` | `("AIR.PA",)` | Airbus, immatriculée aux Pays-Bas |

`nom_fichier(ticker)` construit le chemin `{TICKER}_{DEBUT_SERIE}_{FIN_SERIE}.csv`
et **sort en 1** si le fichier manque, en rappelant la commande à lancer. Un
`glob` choisirait le mauvais CSV dès qu'une autre plage du même ticker traîne
dans le répertoire — c'est arrivé dans l'expérience 1.

---

## Déroulé d'exécution

### 1. Lecture des séries et construction du calendrier

Les treize CSV (douze valeurs, plus `TR12`) et celui de `^FCHI` sont lus par
`charger_serie()`, qui rend `{date: {"open": …, "close": …}}`, dates tronquées au
jour. Une ligne sans `Close` est ignorée ; une ligne sans `Open` reprend sa
clôture.

`calendrier(dates)` groupe les séances de `TR12` par mois et rend la liste des
couples **(date de décision, date d'exécution)** : dernière séance du mois `m`,
première séance du mois `m+1`. La liste est ensuite découpée :

- **couples d'audit** : décisions de `MOIS_AUDIT_DEBUT` à la dernière décision
  disponible → **36 couples** ;
- **couples investis** : ceux dont la décision est à partir de
  `MOIS_INVESTI_DEBUT` → **12 couples** ;
- **couples d'étalonnage** : ceux dont la décision va jusqu'à
  `MOIS_ETALONNAGE_FIN` → **24 couples**, tous antérieurs au 2 janvier 2025.

Un compte différent de 36 ou de 12 est une **erreur fatale** (sortie 1) : mieux
vaut refuser que publier un bilan sur onze mois sans le dire.

### 2. Phase 1 — la collecte, par le code du dépôt

`collecter()` construit la liste des (valeur, date) à évaluer et confie chacune à
`evaluer_un()`, qui lance `generer_graph_decision.py` avec `--csv`, `--indice`
(la série `TR12`), `--date` et `--sortie` vers un SVG jetable. Les lancements se
font par un `ThreadPoolExecutor` de `--taches` fils — un fil qui attend un
sous-processus ne consomme rien.

Les dates évaluées sont :

| Rôle | Dates | Nombre |
|---|---|---|
| `DECISION` | les 36 dates de décision d'audit | 36 × 12 = **432** |
| `DECALE-1` | les 12 dates investies, reculées d'**une** séance | 12 × 12 = **144** |
| `DECALE-2` | les 12 dates investies, reculées de **deux** séances | 12 × 12 = **144** |

soit **720 exécutions**. Le décalage est calculé sur le calendrier de `TR12`, et
la règle recule d'elle-même à la dernière séance disponible si la date demandée
n'est pas une séance de la valeur.

> 🔑 **Le décalage va vers l'arrière, jamais vers l'avant.** Reculer d'une séance
> n'utilise que des séances déjà connues à la date de décision. Avancer
> supposerait une séance postérieure, ce que le dépôt interdit partout.

`extraire(sortie)` tire de la console, par expressions régulières :

| Champ | Ligne lue |
|---|---|
| `TEND_120`, `TEND_20`, `POSITION`, `ALPHA`, `MOMENTUM` | les cinq lignes `Critère n …` |
| `ALPHA_BAS`, `ALPHA_HAUT` | l'`IC95 [ … ; … ]` de la ligne du critère 4 |
| `RESISTANCE`, `PENTE_RES`, `PORTEE_RES`, `EPISODES_RES` | la ligne `Résistance : pente … · portée … · … épisodes · … €` |
| `SUPPORT`, `PENTE_SUP`, `PORTEE_SUP`, `EPISODES_SUP` | la ligne `Support : …`, même forme |
| `LARGEUR`, `TAU` | la ligne `Largeur : … € (… %) · τ = … séances` |
| `VETOS` | la ligne `Vetos : …`, telle quelle |
| `VERDICT` | la ligne `VERDICT : …` |

`nombre(texte)` convertit « −11,38 » ou « +1 234,5 » en flottant, en retirant
espaces fines insécables et espaces ordinaires ; il rend `None` si la chaîne est
illisible.

**Conventions de cellule vide**, au sens de l'invariant du dépôt :

- une cellule vide signifie **non mesuré** — la règle n'a pas produit la ligne ;
- `TAU` vaut le mot **`inf`** quand le canal est parallèle ou divergent. C'est la
  valeur exacte, pas un nombre inventé, et le code la relit comme `+∞` ;
- `VETOS` vaut la chaîne **`aucun`** quand aucun veto ne se déclenche — c'est ce
  que la règle imprime, et c'est une information, pas une absence.

Un code de retour non nul de la règle produit une ligne dont tous les champs sont
vides, `VERDICT` valant `ERREUR`. Le moteur ne s'arrête pas, mais une telle
valeur est **exclue de l'achat au même titre qu'une valeur sous veto** — la
colonne `ERREUR` du classement le porte, et `acheter()` la lit. Les `ERREUR` sont
comptées à part au bilan, jamais rangées dans l'un des quatre vetos qu'elles
n'ont pas déclenchés. Le cas observé est le code **2** de la règle : son contrôle
de non-traversée de l'enveloppe convexe échoue et elle refuse de publier des
critères qu'elle sait faux.

**Écrit** : `criteres.csv`, 720 lignes, colonnes
`DATE, ROLE, DATE_EVALUEE, TICKER, CLOSE, TEND_120, TEND_20, POSITION, ALPHA,
ALPHA_BAS, ALPHA_HAUT, MOMENTUM, SUPPORT, RESISTANCE, PENTE_SUP, PENTE_RES,
PORTEE_SUP, PORTEE_RES, EPISODES_SUP, EPISODES_RES, LARGEUR, TAU, VETOS,
VERDICT`.

> `DATE` est la **date de décision à laquelle la ligne se rattache** ;
> `DATE_EVALUEE` est la date réellement passée à la règle. Les deux coïncident
> pour `ROLE = DECISION` et diffèrent d'une ou deux séances pour les décalages.
> Sans cette séparation, une ligne décalée ne pourrait plus être appariée à la
> décision qu'elle sert à contrôler.

### 3. Phase 2 — le score et le classement

`composantes(ligne, sens)` rend `(s1, s2, s3, s4, s5, score)` :

| | Calcul |
|---|---|
| `s1` | `2 × TEND_120` |
| `s2` | `TEND_20` |
| `s3` **aligné** | `+1` si `POSITION < 35`, `−1` si `POSITION > 65`, `0` entre les deux |
| `s3` **fantôme** | `+1` si `POSITION ≥ 50`, `0` si `POSITION ≥ 20`, `−1` sinon |
| `s4` | `+2` si `MOMENTUM > 10`, `+1` si `> 0`, `−1` si `≥ −10`, `−2` sinon |
| `s5` | `+1` si `ALPHA_BAS > 0`, `−1` si `ALPHA_HAUT < 0`, `0` sinon |

Une composante non calculable vaut `None` et **compte pour 0** dans la somme ;
elle s'affiche `.` dans les tableaux. Le score est la somme des cinq, entre `−7`
et `+7`.

`vetos_actifs(texte)` rend l'ensemble des numéros de veto cités dans la chaîne
`VETOS` — `{1, 3}` pour `« veto 1 : … ; veto 3 : … »`, l'ensemble vide pour
`« aucun »`.

`classer(criteres, date, sens)` rend les douze valeurs du jour triées par score
décroissant, puis momentum décroissant, puis ticker croissant, et leur attribue
un rang de 1 à 12. Le tri est **déterministe** : deux exécutions donnent le même
classement.

**Écrit** : `classement.csv`, 432 lignes (les 36 dates d'audit, sens aligné),
colonnes `DATE, RANG, TICKER, S1, S2, S3, S4, S5, SCORE, POSITION, MOMENTUM,
TAU, VETOS, VERDICT_REGLE`.

### 4. Phase 3 — les ordres

`vendre()` rend les ventes, `acheter()` les achats. Ni l'une ni l'autre ne
modifie l'état : la boucle principale applique les ordres rendus.

**Vendre** — une ligne détenue est vendue si son rang dépasse `--rang-sortie`,
ou si son score est `≤ −3`. Le motif est chiffré et écrit dans `ordres.csv`.
**Les vetos n'entrent pas dans la sortie** : c'est la décision de protocole
déclarée au README.

**Acheter** — les candidats sont les valeurs de rang `≤ --rang-entree`, de score
strictement positif, **sans aucun veto actif**, non déjà détenues. On en garde au
plus `creneaux = --lignes − (lignes détenues)`.

Les espèces disponibles sont divisées par **`creneaux`**, et non par le nombre de
candidats retenus : sans quoi un mois à candidat unique — cas fréquent dès que
les vetos s'appliquent — mettrait tout le portefeuille sur une seule ligne, ce
qui viderait de son sens le plafond de cinq lignes. `--repartition candidats`
rétablit la règle de l'expérience 1, et le bilan publie ce qu'elle aurait donné.

La quantité est `int(part // (prix × (1 + taux)))`, donc entière, et le reliquat
retourne aux espèces. Une quantité nulle annule l'ordre.

Le prix est l'**ouverture** de la date d'exécution. Une valeur sans séance ce
jour-là est une erreur fatale.

**Coûts** : `taux_achat(t) = (0,100 + 0,015 + 0,300) / 100`, sauf pour les
tickers de `EXEMPTES_TTF` où la TTF est nulle ; `taux_vente(t) = (0,100 + 0,015)
/ 100`.

**Écrit** : `ordres.csv`, colonnes `DATE, TICKER, SENS, QUANTITE, PRIX, BRUT,
FRAIS, NET, RANG, SCORE, VETOS, MOTIF`.

### 5. Phase 4 — la simulation, deux fois

`simuler(couples, criteres, series, reference, seances, args, sens,
vetos_appliques, repartition)` rend `(ordres, valeurs, historique)` pour une
variante déclarée. Ses trois leviers — le sens de `s3`, l'application des vetos
et la règle de répartition — sont des paramètres, ce qui permet de faire tourner
toutes les variantes sans dupliquer une ligne de comptabilité. Elle est appelée
**quatre fois** :

1. `aligne`, vetos appliqués, `creneaux` → **le portefeuille de l'expérience** ;
2. `fantome`, vetos appliqués → **le portefeuille fantôme** de la piste C3 ;
3. `aligne`, vetos appliqués, `candidats` → la **variante de répartition** ;
4. `aligne`, **vetos jetés** → la **variante sans veto**, celle de 2022.

Seule la première engage des euros ; les trois autres sont des comptabilités
parallèles, publiées au bilan.

À chaque couple, dans cet ordre : classement à la date de décision → état hérité
mesuré à la **clôture** de cette date → ventes → achats → valorisation de chaque
séance jusqu'à la veille de l'exécution suivante.

L'**alpha du mois** d'une ligne se mesure entre la dernière séance du mois
précédant la date de décision et la date de décision elle-même ; une ligne
achetée en cours de mois est marquée *(partiel)* et son alpha part de son prix
d'achat. L'**alpha global** part du prix d'achat.

**Écrit** : `portefeuille.csv` et `fantome.csv`, colonnes `DATE, ESPECES,
TITRES, TOTAL, BASE100, REFERENCE100`, une ligne par séance de l'année narrée.

### 6. Phase 5 — les thèses, écrites puis dépouillées

`ecrire_theses(criteres, couples_audit, series, reference)` parcourt les 36 dates
d'audit. Pour chaque date `d` ayant une date suivante `d'`, et pour chacune des
douze valeurs, elle écrit **deux thèses** puis les dépouille à `d'`.

`k` est le nombre de séances de `TR12` séparant `d` de `d'`.

**Thèse `CANAL`** :

- `BORNE_BASSE = SUPPORT(d) + k × PENTE_SUP(d)`
- `BORNE_HAUTE = RESISTANCE(d) + k × PENTE_RES(d)`
- `VALEUR_CONSTATEE = Close(d')`

**Thèse `REFLEXIVE`** — la phase se déduit de `TEND_120`, `TEND_20` et
`POSITION` à `d` :

| Phase | Condition à `d` | `BORNE_BASSE` | `BORNE_HAUTE` |
|---|---|---|---|
| `AUTO-RENFORCEMENT` | `TEND_120 = +1`, `TEND_20 = +1`, `POSITION > 65` | `0` | *(vide)* |
| `RETOURNEMENT` | `TEND_120 = −1`, `TEND_20 = −1`, `POSITION < 35` | *(vide)* | `0` |
| `AUCUNE SEQUENCE` | tous les autres cas | `−5` | `+5` |

`VALEUR_CONSTATEE` est l'écart de rendement relatif sur `[d, d']`, en points :

$$100 \times \left(\frac{\text{Close}_{\text{valeur}}(d')}{\text{Close}_{\text{valeur}}(d)}
- \frac{\text{Close}_{\text{TR12}}(d')}{\text{Close}_{\text{TR12}}(d)}\right)$$

**Le verdict est le même pour les deux types**, et c'est ce qui le rend
vérifiable : `CONFIRMEE` si `BORNE_BASSE ≤ VALEUR_CONSTATEE ≤ BORNE_HAUTE`, une
borne vide valant `∓∞` ; `DEMENTIE` sinon ; `NON TRANCHEE` si la valeur
constatée ou les deux bornes manquent.

Conséquence déclarée : quand `τ < k`, les bornes du canal se croisent,
`BORNE_BASSE > BORNE_HAUTE`, et la thèse `CANAL` est **mécaniquement démentie**.
C'est la mesure demandée par la piste C4, pas un artefact.

La dernière date d'audit n'a pas de date de décision suivante : ses 24 thèses
sont dépouillées à la **dernière séance de la série**, `FIN_SERIE`. C'est une
mesure postérieure, publiée au bilan et jamais dans un journal mensuel — aucune
décision ne s'y appuie. Les 864 thèses sont donc toutes dépouillées.

**Écrit** : `theses.csv`, 864 lignes, colonnes `DATE, TICKER, TYPE, PHASE,
ENONCE, BORNE_BASSE, BORNE_HAUTE, DATE_DEPOUILLEMENT, VALEUR_CONSTATEE,
VERDICT`. `ENONCE` est la phrase française lisible, engendrée par le moteur.

### 7. Phase 6 — les audits

Quatre fonctions, dont les résultats vont au bilan et, pour deux d'entre elles,
au README avant la première séance.

`poids_effectifs(criteres, dates, sens)` — la part de variance que chaque
composante explique dans le score :
$\operatorname{Cov}(s_i, \text{score}) / \operatorname{Var}(\text{score})$, dont
la somme vaut exactement 1. Calculée sur les 288 évaluations de la fenêtre
d'étalonnage pour le README, sur les 432 de la fenêtre d'audit pour le bilan.
Une composante de variance nulle rend un poids de 0 — ce n'est pas une erreur,
c'est le constat qu'elle ne distingue rien.

`taux_vetos(criteres, dates)` — pour chacun des quatre vetos, le nombre
d'évaluations où il se déclenche, sa proportion, et son IC95 par
$\hat p \pm 1{,}96\sqrt{\hat p(1-\hat p)/n}$.

`entrees_bloquees(historique, args)` — le nombre d'achats qu'un veto a interdits :
une valeur de rang `≤ --rang-entree`, de score strictement positif, non détenue,
mais sous veto. C'est **la différence exacte, sur ce point, entre la règle de
l'expérience 2 et celle de l'expérience 1**.

`stabilite(criteres, dates_investies)` — pour chaque couple (date, valeur) de
l'année narrée, compare `s3` et le score entre `DECISION`, `DECALE-1` et
`DECALE-2`, et rend le nombre de bascules de `s3`, le nombre de changements de
score, et le nombre de changements de l'ensemble des cinq premiers rangs.

`survie_encadrement(theses)` — le taux de démenti des thèses `CANAL`, la part
des évaluations dont `τ < k`, et la médiane de `τ`.

`dimensionnement(valeurs, ref100)` — la tracking error réalisée sur l'année
narrée, l'effet minimal détectable qui en découle, et l'écart apparié entre le
portefeuille et son fantôme avec son erreur-type. C'est la confrontation
demandée par la piste T1 : *le dimensionnement publié avant tenait-il ?*

### 8. Phase 7 — les graphiques

`svg()` écrit, pour chaque mois, une figure de 900 × 420 à **deux courbes en base
100** — le portefeuille et `TR12` — du 2 janvier à la dernière séance du mois
courant, avec un trait vertical pointillé à chaque date d'exécution. Grille
horizontale à pas choisi par `pas_de_grille()` pour ne jamais dépasser huit
lignes, ligne 100 en gris plus soutenu.

> L'échelle est calculée sur les seules séances tracées. Le graphique de mars ne
> connaît pas avril : c'est la même interdiction de regard en avant que pour les
> décisions.

**Écrit** : `graphiques/portefeuille-2025-MM.svg`, douze fichiers.

### 9. Phase 8 — les markdown

Avec `--markdown` seulement.

`charger_textes()` lit [`actualites.md`](actualites.md) et
[`chartiste.md`](chartiste.md) et les découpe par `decouper()` : les sections
`## AAAA-MM` du premier, les sections `## AAAA-MM-JJ` puis `### TICKER` du
second. **Les deux fichiers sont requis** : leur absence est une sortie 1.

`journal_mensuel()` écrit `rapports/2025-MM.md`, huit sections dans l'ordre
déclaré au README : actualités, **dépouillement des thèses du mois précédent**,
exposition héritée, valeur et graphique, étude chartiste, classement **avec vetos
et τ**, ordres exécutés, **thèses du mois**. Une section dont le texte manque
porte la mention `*(section absente)*` — jamais un texte inventé.

`lecture_du_mois()` rend un paragraphe **entièrement calculé** : meilleure et
moins bonne contribution en euros, frais du mois, position par rapport à `TR12`,
et le taux de confirmation des thèses dépouillées. Aucun récit écrit après coup.

`bilan_annuel()` écrit [`bilan-2025.md`](bilan-2025.md), dix sections : le
compte, mois par mois, les positions, **l'audit de la règle** (T3), **le sens de
`s3`** (C3), **la durée de vie de l'encadrement** (C4), **le registre des
thèses** (S4), les trois conventions, **le dimensionnement confronté** (T1), et
ce que l'expérience établit ou n'établit pas. Les quatre sections d'audit sont
écrites par `section_audit_regle()`, `section_sens_s3()`, `section_encadrement()`
et `section_theses()`.

### 10. La console

Sans `--mois`, le moteur imprime un bloc par mois investi — classement complet
avec vetos, exposition héritée, ordres, valeur de fin de mois — puis le bloc de
bilan :

```
=== Bilan au 2025-12-31 ===

  Dotation                10 000,00 EUR au 2025-01-02
  Valeur finale           ...
  Performance             ...
  TR12                    ...
  Alpha sur l'annee       ... pt   (non concluant : MDE +/- ... pt)

  Fantome (s3 experience 1)  ... pt    ecart appari ... pt
  Ordres                  ... (... achats, ... ventes)
  Frais cumules           ... EUR, soit ... % de la dotation
  Vetos declenches        ... / 432 evaluations
  Theses depouillees      ... confirmees sur ...
```

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | exécution complète |
| `1` | série absente, `criteres.csv` absent sans `--collecter`, calendrier incomplet, argument invalide, ou `actualites.md` / `chartiste.md` absent avec `--markdown` |

## Cas limites

- **Un ticker sans séance à une date d'exécution** : erreur fatale. Un ordre ne
  peut pas être exécuté à un prix qui n'existe pas.
- **`τ` infini** : le canal est parallèle ou divergent ; le veto 2 ne se
  déclenche pas, et les bornes de la thèse `CANAL` restent dans le bon ordre.
- **Position hors canal** (`POSITION` < 0 ou > 100) : reprise telle quelle. `s3`
  vaut alors `+1` (sous le support) ou `−1` (au-dessus de la résistance) dans le
  sens aligné — la valeur est extrême, le score le dit.
- **Aucun candidat à l'achat** : les espèces restent oisives, aucun ordre n'est
  écrit, et la console le dit.
- **Toutes les valeurs sous veto** : cas possible et non pathologique ; le
  portefeuille reste en l'état.
- **Une composante manquante** : elle compte pour 0 dans le score et s'affiche
  `.`. Un score peut donc être calculé sur quatre composantes ; `criteres.csv`
  garde la trace de laquelle manquait.
- **Une thèse dont la valeur constatée manque** : `NON TRANCHEE`. Elle compte au
  dénominateur des thèses écrites, jamais à celui des thèses dépouillées.
