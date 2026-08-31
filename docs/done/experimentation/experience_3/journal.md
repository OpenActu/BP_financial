# journal.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/done/experimentation/experience_3/journal.py`, étape par étape, dans
l'ordre du déroulement. Il fait autorité : toute évolution du script doit
d'abord être décrite ici.

Le **protocole** — l'univers point-in-time, le score, les seuils, les coûts, les
cinq corrections apportées à l'expérience 2 — est dans [`README.md`](README.md).
Ce miroir décrit le moteur qui l'applique.

## Rôle

Conduire mécaniquement le portefeuille de l'expérience 3 : lire l'univers **tel
qu'il était à chaque date de décision**, classer, appliquer les vetos, en déduire
les ordres, les exécuter à l'ouverture suivante, tenir la comptabilité, engendrer
et **dépouiller** les thèses réfutables, conserver les figures de décision,
tracer les graphiques, et écrire les douze journaux mensuels puis le bilan.

Le moteur ajoute six choses au moteur de l'expérience 2 — les cinq pistes
retenues par [la revue](../experience_2/review.md), plus l'univers :

| Piste       | Ce que le moteur fait en plus                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| *(univers)* | il lit [`univers.csv`](univers.csv) et travaille sur **la composition réelle de l'indice à chaque date**, 38 puis 39 valeurs, au lieu d'une liste figée |
| **C1**      | il passe `--fenetre` et `--tolerance` **explicitement** à la règle, et relance la collecte sous **quatre variantes déclarées**                          |
| **C3**      | il confronte chaque veto à l'**issue observable** contre laquelle le protocole l'a déclaré jugeable                                                     |
| **S1**      | il lit [`canaux.csv`](canaux.csv) et n'écrit de thèse `REFLEXIVE` que pour les valeurs à **canal de transmission déclaré**                              |
| **S3**      | il normalise la clause réflexive par $\hat\sigma_d$, écart-type des **12 écarts mensuels précédents de la valeur**                                      |
| **T1**      | il décompose l'alpha par **régression** sur la référence — bêta, alpha de régression, résidu, et l'IC95 de l'alpha                                      |

Il conserve aussi les **467 figures de décision** de l'année narrée, que
l'expérience 2 produisait puis jetait, et publie dans chaque journal mensuel le
**tableau de toutes les positions** prises depuis le début.

> ⚠️ **Aucune décision n'est prise à la main.** Le classement, les vetos, les
> ordres et les thèses sortent tous de quantités calculées. Le seul texte rédigé
> à la main est dans [`actualites.md`](actualites.md) et
> [`chartiste.md`](chartiste.md), et le moteur n'en fait que la mise en page.

## Dépendances

- Modules standard uniquement : `argparse`, `csv`, `math`, `os`, `re`,
  `statistics`, `subprocess`, `sys`, `pathlib`, `concurrent.futures`.
- **Aucune bibliothèque de tracé** : les SVG sont écrits à la main.
- Il lance [`python/generer_graph_decision.py`](../../../../python/generer_graph_decision.md)
  en sous-processus et lit sa console. **Les cinq critères, les vetos et
  l'encadrement ne sont jamais réimplémentés ici.**

### L'encodage du sous-processus, et pourquoi il est déclaré

Le moteur impose `PYTHONIOENCODING=utf-8` dans l'environnement de **chaque**
sous-processus, et reconfigure sa propre sortie en UTF-8 dès le premier appel de
`main()`.

> 🔑 **Sans cela, la collecte échoue en silence.** Le fils écrit sa console dans
> l'encodage de la console héritée — `cp1252` sous Windows — tandis que le père la
> décode en UTF-8. Les lignes de la règle contiennent des espaces fines
> insécables, des `·`, des `€`, des `τ` et des `∞` : la moindre substitution fait
> échouer les expressions régulières, tous les champs deviennent vides, et la
> ligne est enregistrée `VERDICT = ERREUR`. Le moteur ne s'arrête pas, il produit
> simplement **900 lignes vides** sans qu'aucun message ne le dise. Le défaut a
> été trouvé dans l'expérience 2 par une revue de code, pas par une exécution.

Symétriquement, le père imprime `∞`, `·` et des espaces fines : sans
reconfiguration, l'affichage du bilan lève `UnicodeEncodeError` sur une console
`cp1252` et **perd tout le travail déjà fait**.

## Invocation

```bash
python docs/done/experimentation/experience_3/journal.py --collecter --taches 12
python docs/done/experimentation/experience_3/journal.py --markdown
python docs/done/experimentation/experience_3/journal.py --mois 2022-03
```

### Arguments

| Argument        | Défaut                  | Rôle                                                                 |
| --------------- | ----------------------- | -------------------------------------------------------------------- |
| `--collecter`   | —                       | lance les évaluations manquantes de la règle et écrit `criteres.csv` |
| `--markdown`    | —                       | écrit aussi les douze journaux, le bilan et les graphiques           |
| `--mois`        | —                       | n'affiche en console que ce mois (`AAAA-MM`)                         |
| `--repertoire`  | le répertoire du script | où lire et écrire                                                    |
| `--quotes`      | `docs/raw/data/quotes`  | où sont les séries                                                   |
| `--dotation`    | `10000.0`               | dotation en euros                                                    |
| `--lignes`      | `5`                     | lignes détenues au maximum                                           |
| `--rang-entree` | `5`                     | rang d'achat                                                         |
| `--rang-sortie` | `7`                     | rang de vente                                                        |
| `--repartition` | `creneaux`              | diviser les espèces par les créneaux libres, ou par les candidats    |
| `--recollecter` | —                       | repartir de zéro au lieu de compléter `criteres.csv`                 |
| `--taches`      | `8`                     | sous-processus simultanés pendant la collecte                        |
| `--sans-veto`   | —                       | **diagnostic** : affiche en plus ce que la règle donne vetos jetés   |

`--rang-sortie` inférieur à `--rang-entree` : sortie **1** (l'hystérésis serait
inversée). `--dotation` négative ou nulle : sortie **1**. `--lignes` hors de
`[1, 38]` : sortie **1**. `--taches` hors de `[1, 32]` : sortie **1**.

> 🔑 **`--taches` ne change aucun résultat.** L'essentiel de la durée d'une
> évaluation est l'import de `pandas` par le sous-processus, pas le calcul.
> `collecter()` range les lignes dans **l'ordre des tâches**, jamais dans celui
> des retours, si bien que `criteres.csv` est identique d'une exécution à
> l'autre quelle que soit la valeur de `--taches`.

> **La collecte est reprenable.** `--collecter` conserve les lignes déjà
> présentes dans `criteres.csv`, n'évalue que ce qui manque, et **dépose le
> fichier tous les `CADENCE_ECRITURE` résultats** : une collecte interrompue
> reprend où elle en était au lieu de tout perdre. Avec 5 549 évaluations à
> 3,3 secondes chacune, c'est une nécessité, pas un confort. `--recollecter`
> repart de zéro — c'est ce qu'il faut faire dès que la règle elle-même a changé.

> 🔑 **Le dépôt est atomique.** `criteres.csv` est écrit dans un
> `criteres.csv.partiel` voisin, qui *remplace* ensuite le fichier. Une collecte
> d'une demi-heure sera interrompue ; écrire en place exposerait le fichier à
> être tronqué au milieu d'un dépôt — et **un CSV tronqué se relit sans erreur**,
> en silence, avec quelques centaines d'évaluations en moins.

> `--sans-veto` ne modifie aucun CSV ni aucun markdown publié : il ajoute au flux
> console un bloc comparant la base 100 et le nombre d'ordres. Le protocole
> déclaré applique les vetos, sans option. La comptabilité sans veto est de
> toute façon calculée à chaque exécution, puisque le bilan la publie : l'option
> n'ajoute qu'un affichage.

## Les constantes déclarées

| Constante                                  | Valeur                                    | Rôle                                                               |
| ------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------------ |
| `REFERENCE`                                | `TR39`                                    | la référence en rendement total                                    |
| `REFERENCE_NUE`                            | `^FCHI`                                   | l'indice nu, pour la section « trois conventions »                 |
| `DEBUT_SERIE` / `FIN_SERIE`                | `2019-01-02` / `2022-12-30`               | la plage des CSV, **déclarée** et non devinée par glob             |
| `MOIS_AUDIT_DEBUT`                         | `2020-12`                                 | mois de la première décision d'audit                               |
| `MOIS_INVESTI_DEBUT`                       | `2021-12`                                 | mois de la première décision investie                              |
| `MOIS_ETALONNAGE_FIN`                      | `2021-11`                                 | dernier mois de décision de la fenêtre d'étalonnage                |
| `COUPLES_AUDIT` / `COUPLES_INVESTIS`       | `24` / `12`                               | contrôlés, et fatals s'ils diffèrent                               |
| `ANNEE`                                    | `2022`                                    | l'année narrée                                                     |
| `FENETRE` / `TOLERANCE`                    | `120` / `0.25`                            | **piste C1** : les paramètres d'encadrement, passés explicitement  |
| `VARIANTES`                                | quatre couples                            | `F60`, `F180`, `T015`, `T040` — voir ci-dessous                    |
| `SEUIL_BAS` / `SEUIL_HAUT`                 | `35.0` / `65.0`                           | les seuils de `s3` **aligné**                                      |
| `SEUIL_BAS_FANTOME` / `SEUIL_HAUT_FANTOME` | `20.0` / `50.0`                           | les seuils de `s3` au sens de l'expérience 1                       |
| `FENETRE_SIGMA`                            | `12`                                      | **piste S3** : mois d'écarts servant à $\hat\sigma_d$              |
| `DEMI_BORNE`                               | `0.5`                                     | **piste S3** : les bornes de phase, en multiples de $\hat\sigma_d$ |
| `DECALAGES`                                | `(1, 2)`                                  | les décalages rétrospectifs                                        |
| `CADENCE_ECRITURE`                         | `48`                                      | dépôt intermédiaire de `criteres.csv` pendant la collecte          |
| `TE_DECLAREE`                              | `8.20`                                    | la tracking error publiée au README avant la première séance       |
| `Z95`                                      | `1.96`                                    | le quantile normal des IC à 95 %                                   |
| `COURTAGE` / `SPREAD` / `TTF`              | `0.10` / `0.015` / `0.30`                 | en %, barème de `couts_transaction.py`                             |
| `EXEMPTES_TTF`                             | `AIR.PA`, `STLAP.PA`, `MT.AS`, `STMPA.PA` | sièges hors de France                                              |
| `SOCIETES`                                 | 40 entrées                                | la table des noms d'affichage, **déclarée**                        |

`SOCIETES` est écrite dans le script plutôt que lue dans `univers.csv` : la
source rend des libellés hétérogènes (`AIR LIQUIDE`, `Cap Gémini`,
`Total`, `Renault`), utiles à l'appariement et impropres à l'affichage. Le
moteur **sort en 1** si un ticker de l'univers n'y figure pas : une valeur sans
nom déclaré serait publiée sous un libellé deviné.

`nom_fichier(ticker)` construit le chemin `{TICKER}_{DEBUT_SERIE}_{FIN_SERIE}.csv`
et **sort en 1** si le fichier manque, en rappelant la commande à lancer — avec
un `--fin` calculé au **lendemain** de `FIN_SERIE`, puisque `--fin` est exclusif.
Un `glob` choisirait le mauvais CSV dès qu'une autre plage du même ticker traîne
dans le répertoire.

### Les quatre variantes déclarées — piste C1

| Rôle dans `criteres.csv` | `--fenetre` | `--tolerance` |
| ------------------------ | ----------- | ------------- |
| `DECISION`               | **120**     | **0,25**      |
| `VAR-F60`                | 60          | 0,25          |
| `VAR-F180`               | 180         | 0,25          |
| `VAR-T015`               | 120         | 0,15          |
| `VAR-T040`               | 120         | 0,40          |

Les variantes sont évaluées sur **les 24 dates d'audit**, comme la ligne
`DECISION`, afin que leurs taux se comparent à effectif égal. Elles ne décident
rien : aucun euro, aucun classement, aucune thèse n'en dépend. Le bilan les
publie côte à côte pour chiffrer **de combien l'incertitude de convention dépasse
l'incertitude d'échantillonnage**.

`ECART_EPISODE` vaut 3 : c'est la constante de
`generer_graph_decision.py`, que le protocole déclare sans la faire varier —
elle n'est pas exposée en ligne de commande.

---

## Déroulé d'exécution

### 1. L'univers point-in-time et les canaux

`charger_univers()` lit [`univers.csv`](univers.csv) et rend deux choses :

- `UNIVERS[date]` — la liste **triée** des tickers dont `RETENUE` vaut `oui` à
  cette date de décision ;
- `EXCLUSIONS[date]` — les autres, avec leur motif, republiés au bilan.

`TOUS_TICKERS` est l'union des univers : **40 valeurs** sur la fenêtre d'audit.
Un `univers.csv` absent est une sortie **1** — l'univers ne se devine pas.

`charger_canaux()` lit [`canaux.csv`](canaux.csv) et rend `{ticker: canal}`. Un
ticker de `TOUS_TICKERS` absent du fichier est une **sortie 1** : la piste S1
exige que le canal soit déclaré avant la première séance, et laisser une valeur
sans déclaration reviendrait à la traiter par défaut — ce que l'expérience 2
faisait pour les quarante.

### 1 bis. Les divisions postérieures à la fenêtre

`SPLITS_POSTERIEURS` est une table **déclarée** : les valeurs dont le
fournisseur a répercuté rétroactivement une division d'actions survenue **après**
`FIN_SERIE`, avec son facteur.

| Valeur | Division | Facteur | Cours historiques multipliés par |
|---|---|---|---|
| `AI.PA` | 2024-06-10 et 2026-06-08, attributions d'actions gratuites | 1,1 chacune | 0,826 |
| `ATO.PA` | 2025-04-24, regroupement | 0,0001 | 10 000 |
| `WLN.PA` | 2026-06-15, regroupement | 0,025 | 40 |

> 🔑 **Une division rétroactive est un regard en avant sur le nombre de titres.**
> Toutes les quantités que la règle calcule sont invariantes d'échelle — position
> dans le canal en %, momentum, alpha, tendances, τ en séances, largeur en %. Le
> **nombre de titres achetables** ne l'est pas. Un créneau de 2 000 € sur une
> valeur affichée à 506 € achète 3 titres et laisse 481 € oisifs ; à son cours
> réel de l'époque, il en achèterait dix fois plus et n'en laisserait que
> trente. Le portefeuille serait donc façonné par une opération de 2026.

`verifier_splits(ordres)` est appelée **après** la simulation et **sort en 1** si
un ordre porte sur une valeur de la table. Ce n'est pas un filtre — un filtre
changerait la règle, et agirait comme un cinquième veto. C'est une
**vérification** : si le cas se présente, l'expérience doit s'arrêter et
l'opérateur retélécharger une série non rétro-ajustée, pas publier un
portefeuille déformé.

Sur cette fenêtre, **aucune des trois valeurs n'est jamais achetée** — le bilan
publie la vérification et son résultat. Les trois restent dans l'univers, dans
les taux de veto et dans le registre des thèses, où seules des quantités
invariantes d'échelle interviennent.

### 2. Lecture des séries et construction du calendrier

Les 40 CSV de valeurs, celui de `TR39` et celui de `^FCHI` sont lus par
`charger_serie()`, qui rend `{date: {"open": …, "close": …}}`, dates tronquées au
jour. Une ligne sans `Close` est ignorée ; une ligne sans `Open` reprend sa
clôture.

`calendrier(dates)` groupe les séances de `TR39` par mois et rend la liste des
couples **(date de décision, date d'exécution)** : dernière séance du mois `m`,
première séance du mois `m+1`. La liste est ensuite découpée :

- **couples d'audit** : décisions de `MOIS_AUDIT_DEBUT` à la dernière disponible
  → **24 couples** ;
- **couples investis** : décisions à partir de `MOIS_INVESTI_DEBUT` →
  **12 couples** ;
- **couples d'étalonnage** : décisions jusqu'à `MOIS_ETALONNAGE_FIN` →
  **12 couples**.

Un compte différent de 24 ou de 12 est une **erreur fatale** (sortie 1). Le
moteur vérifie en outre que **chaque date de décision du calendrier figure dans
`univers.csv`**, et sort en 1 sinon : un univers muet à une date produirait un
mois sans classement, sans le dire.

### 3. Phase 1 — la collecte, par le code du dépôt

`collecter()` construit la liste des (valeur, date, rôle) à évaluer et confie
chacune à `evaluer_un()`, qui lance `generer_graph_decision.py` avec `--csv`,
`--indice` (la série `TR39`), `--date`, `--fenetre`, `--tolerance` et `--sortie`.
Les lancements se font par un `ThreadPoolExecutor` de `--taches` fils.

Les évaluations sont :

| Rôle                                          | Dates                                                | Valeurs           | Nombre              |
| --------------------------------------------- | ---------------------------------------------------- | ----------------- | ------------------- |
| `DECISION`                                    | les 24 dates d'audit                                 | l'univers du jour | **923**             |
| `DECALE-1`                                    | les 12 dates investies, reculées d'**une** séance    | l'univers du jour | **467**             |
| `DECALE-2`                                    | les 12 dates investies, reculées de **deux** séances | l'univers du jour | **467**             |
| `VAR-F60`, `VAR-F180`, `VAR-T015`, `VAR-T040` | les 24 dates d'audit                                 | l'univers du jour | 4 × 923 = **3 692** |

soit **5 549 exécutions**. Le décalage est calculé sur le calendrier de `TR39`,
et la règle recule d'elle-même à la dernière séance disponible si la date
demandée n'est pas une séance de la valeur.

> 🔑 **Le décalage va vers l'arrière, jamais vers l'avant.** Reculer d'une séance
> n'utilise que des séances déjà connues à la date de décision. Avancer
> supposerait une séance postérieure, ce que le dépôt interdit partout.

#### Les figures conservées

Pour le rôle `DECISION` **et** une date de l'année narrée, le SVG est écrit dans
**`graphiques/{TICKER}/decision-{TICKER}-{AAAA-MM-JJ}.svg`** et **conservé** : ce
sont les **467 figures** que le journal mensuel insère sous chaque note
chartiste. Dans tous les autres cas, le SVG part dans un fichier jetable propre à
la tâche, et tous les jetables sont effacés en fin de collecte.

> 🔑 **Une figure propre à une société va dans un sous-répertoire portant son
> ticker.** À plat, 467 fichiers dans un même répertoire ne se parcourent ni par
> société ni dans le temps, et l'on ne voit pas d'un coup d'œil ce qui manque
> après une collecte interrompue ; un `ls graphiques/SU.PA/` répond aux deux
> questions. Le ticker reste dans le nom du fichier, pour qu'un SVG déplacé
> demeure identifiable. Les figures qui ne portent **pas** sur une société — les
> douze courbes du portefeuille — restent à la racine de `graphiques/`.

> **Aucun regard en avant.** `generer_graph_decision.py --date d` supprime toutes
> les lignes postérieures à `d` avant tout calcul, échelles comprises : la figure
> conservée est par construction celle qu'on pouvait tracer le jour de la
> décision.

#### L'extraction

`extraire(sortie)` tire de la console, par expressions régulières :

| Champ                                                   | Ligne lue                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------- |
| `TEND_120`, `TEND_20`, `POSITION`, `ALPHA`, `MOMENTUM`  | les cinq lignes `Critère n …`                                 |
| `ALPHA_BAS`, `ALPHA_HAUT`                               | l'`IC95 [ … ; … ]` de la ligne du critère 4                   |
| `RESISTANCE`, `PENTE_RES`, `PORTEE_RES`, `EPISODES_RES` | la ligne `Résistance : pente … · portée … · … épisodes · … €` |
| `SUPPORT`, `PENTE_SUP`, `PORTEE_SUP`, `EPISODES_SUP`    | la ligne `Support : …`, même forme                            |
| `LARGEUR`, `TAU`                                        | la ligne `Largeur : … € (… %) · τ = … séances`                |
| `VETOS`                                                 | la ligne `Vetos : …`, telle quelle                            |
| `VERDICT`                                               | la ligne `VERDICT : …`                                        |

`nombre(texte)` convertit « −11,38 » ou « +1 234,5 » en flottant, en retirant
tout ce qui n'est ni chiffre, ni virgule, ni point, ni signe ; il rend `None` si
la chaîne est illisible.

**Conventions de cellule vide**, au sens de l'invariant du dépôt :

- une cellule vide signifie **non mesuré** — la règle n'a pas produit la ligne ;
- `TAU` vaut le mot **`inf`** quand le canal est parallèle ou divergent. C'est la
  valeur exacte, pas un nombre inventé, et le code la relit comme `+∞` ;
- `VETOS` vaut la chaîne **`aucun`** quand aucun veto ne se déclenche — c'est ce
  que la règle imprime, et c'est une information, pas une absence.

#### Quand la règle échoue

Un code de retour non nul produit une ligne dont tous les champs de mesure sont
vides, `VERDICT` valant `ERREUR`, et **`DIAGNOSTIC` portant le code de retour
suivi de la dernière ligne non vide de la sortie d'erreur**.

> L'expérience 2 jetait `stderr`. Une évaluation impossible y était donc
> indiscernable d'une évaluation impossible pour une tout autre raison, et la
> colonne `DIAGNOSTIC` est la correction de ce point.

Une ligne `ERREUR` est **exclue du classement** : elle ne reçoit pas de rang, ne
décale pas les rangs des autres, et ne peut donc ni être achetée ni provoquer la
vente d'une ligne détenue. Elle est publiée à part, avec son diagnostic.

> 🔑 **C'est un changement par rapport à l'expérience 2**, où une `ERREUR`
> occupait un rang — le plus mauvais, son score valant 0 — et pouvait à ce titre
> pousser une valeur détenue au-delà du rang de sortie. Une évaluation que la
> règle n'a pas su produire ne dit rien ; elle ne doit donc rien déclencher.
> Une ligne détenue dont l'évaluation échoue est **conservée**, et la console
> comme le journal mensuel le disent.

**Écrit** : `criteres.csv`, 5 549 lignes, colonnes
`DATE, ROLE, DATE_EVALUEE, TICKER, CLOSE, TEND_120, TEND_20, POSITION, ALPHA,
ALPHA_BAS, ALPHA_HAUT, MOMENTUM, SUPPORT, RESISTANCE, PENTE_SUP, PENTE_RES,
PORTEE_SUP, PORTEE_RES, EPISODES_SUP, EPISODES_RES, LARGEUR, TAU, VETOS,
VERDICT, DIAGNOSTIC`.

> `DATE` est la **date de décision à laquelle la ligne se rattache** ;
> `DATE_EVALUEE` est la date réellement passée à la règle. Les deux coïncident
> partout sauf pour les deux rôles décalés.

### 4. Phase 2 — le score et le classement

`composantes(ligne, sens)` rend `(s1, s2, s3, s4, s5, score)` :

|                  | Calcul                                                               |
| ---------------- | -------------------------------------------------------------------- |
| `s1`             | `2 × TEND_120`                                                       |
| `s2`             | `TEND_20`                                                            |
| `s3` **aligné**  | `+1` si `POSITION < 35`, `−1` si `POSITION > 65`, `0` entre les deux |
| `s3` **fantôme** | `+1` si `POSITION ≥ 50`, `0` si `POSITION ≥ 20`, `−1` sinon          |
| `s4`             | `+2` si `MOMENTUM > 10`, `+1` si `> 0`, `−1` si `≥ −10`, `−2` sinon  |
| `s5`             | `+1` si `ALPHA_BAS > 0`, `−1` si `ALPHA_HAUT < 0`, `0` sinon         |

Une composante non calculable vaut `None` et **compte pour 0** dans la somme ;
elle s'affiche `.` dans les tableaux. Le score est la somme des cinq, entre `−7`
et `+7`.

`vetos_actifs(texte)` rend l'ensemble des numéros de veto cités dans la chaîne
`VETOS` — `{1, 3}` pour `« veto 1 : … ; veto 3 : … »`, l'ensemble vide pour
`« aucun »`.

`classer(criteres, date, sens)` rend les valeurs de **l'univers de cette date**,
`ERREUR` exclues, triées par score décroissant, puis momentum décroissant, puis
ticker croissant, et leur attribue un rang de 1 à *n*. Le tri est
**déterministe** : deux exécutions donnent le même classement.

**Écrit** : `classement.csv`, colonnes `DATE, RANG, TICKER, S1, S2, S3, S4, S5,
SCORE, POSITION, MOMENTUM, TAU, VETOS, VERDICT_REGLE`.

### 5. Phase 3 — les ordres

`vendre()` rend les ventes, `acheter()` les achats. Ni l'une ni l'autre ne
modifie l'état : la boucle principale applique les ordres rendus.

**Vendre** — une ligne détenue est vendue si son rang dépasse `--rang-sortie`,
ou si son score est `≤ −3`. Une ligne détenue **absente du classement** — sortie
de l'indice, ou évaluation en erreur — est **conservée sans ordre**, et le motif
est consigné. **Les vetos n'entrent pas dans la sortie.**

> **Le sort d'une ligne qui quitte l'indice est une décision de protocole**, et
> elle est prise ici : on la garde. Une valeur retirée du CAC 40 n'est pas une
> valeur qui s'effondre, et la vendre d'office produirait des ordres que le score
> n'a pas demandés, donc des frais que la règle n'explique pas. Le cas ne se
> présente qu'une fois sur la fenêtre — Atos, hors année narrée — et le bilan le
> republie.

**Acheter** — les candidats sont les valeurs de rang `≤ --rang-entree`, de score
strictement positif, **sans aucun veto actif**, non déjà détenues. On en garde au
plus `creneaux = --lignes − (lignes détenues)`.

Les espèces disponibles sont divisées par **`creneaux`**, et non par le nombre de
candidats retenus : sans quoi un mois à candidat unique mettrait tout le
portefeuille sur une seule ligne, ce qui viderait de son sens le plafond de cinq
lignes. `--repartition candidats` rétablit la règle de l'expérience 1, et le
bilan publie ce qu'elle aurait donné.

La quantité est `int(part // (prix × (1 + taux)))`, donc entière, et le reliquat
retourne aux espèces. Une quantité nulle annule l'ordre.

Le prix est l'**ouverture** de la date d'exécution. Une valeur sans séance ce
jour-là est une erreur fatale.

**Coûts** : `taux_achat(t) = (0,100 + 0,015 + 0,300) / 100`, sauf pour les
tickers de `EXEMPTES_TTF` où la TTF est nulle ; `taux_vente(t) = (0,100 + 0,015)
/ 100`.

**Écrit** : `ordres.csv`, colonnes `DATE, TICKER, SENS, QUANTITE, PRIX, BRUT,
FRAIS, NET, RANG, SCORE, VETOS, MOTIF`.

### 6. Phase 4 — la simulation, quatre fois

`simuler(couples, criteres, series, reference, seances, args, sens,
vetos_appliques, repartition)` rend `(ordres, valeurs, historique)` pour une
variante déclarée. Ses trois leviers sont des paramètres, ce qui permet de faire
tourner toutes les variantes sans dupliquer une ligne de comptabilité. Elle est
appelée **quatre fois** :

1. `aligne`, vetos appliqués, `creneaux` → **le portefeuille de l'expérience** ;
2. `fantome`, vetos appliqués → **le portefeuille fantôme** ;
3. `aligne`, vetos appliqués, `candidats` → la **variante de répartition** ;
4. `aligne`, **vetos jetés** → la **variante sans veto**.

Seule la première engage des euros ; les trois autres sont des comptabilités
parallèles, publiées au bilan. La quatrième est calculée **une seule fois** et
réutilisée par le diagnostic `--sans-veto`.

À chaque couple, dans cet ordre : classement à la date de décision → état hérité
mesuré à la **clôture** de cette date → ventes → achats → valorisation de chaque
séance jusqu'à la veille de l'exécution suivante.

L'**alpha du mois** d'une ligne se mesure entre la dernière séance du mois
précédant la date de décision et la date de décision elle-même ; une ligne
achetée en cours de mois est marquée *(partiel)* et son alpha part de son prix
d'achat. L'**alpha global** part du prix d'achat.

**Écrit** : `portefeuille.csv` et `fantome.csv`, colonnes `DATE, ESPECES,
TITRES, TOTAL, BASE100, REFERENCE100`, une ligne par séance de l'année narrée.

### 7. Phase 5 — les thèses, écrites puis dépouillées

`ecrire_theses()` parcourt les 24 dates d'audit. Pour chaque date `d`, sa date de
dépouillement `d'` et chaque valeur de l'univers de `d`, elle écrit **une ou deux
thèses** puis les dépouille à `d'`.

`k` est le nombre de séances de `TR39` séparant `d` de `d'`.

#### Thèse `CANAL` — une par évaluation

- `BORNE_BASSE = SUPPORT(d) + k × PENTE_SUP(d)`
- `BORNE_HAUTE = RESISTANCE(d) + k × PENTE_RES(d)`
- `VALEUR_CONSTATEE = Close(d')`

Quand `τ < k`, les bornes se croisent, `BORNE_BASSE > BORNE_HAUTE`, et la thèse
est **inconfirmable à l'écriture**. Elle reçoit le verdict `INCONFIRMABLE`,
compté **à part** — ni parmi les confirmées, ni parmi les démenties. C'est la
correction d'un point de l'expérience 2, qui les rangeait parmi les démenties et
gonflait ainsi son propre taux de démenti.

#### Thèse `REFLEXIVE` — seulement pour les valeurs à canal déclaré

**Une valeur dont `canaux.csv` dit `aucun` ne reçoit aucune thèse `REFLEXIVE`.**
Elle est comptée dans le registre sous la mention `HORS CHAMP REFLEXIF`, qui dit
*« la théorie ne s'applique pas »* — un énoncé différent d'`AUCUNE SEQUENCE`, qui
dit *« elle s'applique, et il ne se passe rien »*.

Une évaluation `ERREUR`, ou dont l'un de `TEND_120`, `TEND_20`, `POSITION`
manque, ne reçoit **pas** de thèse `REFLEXIVE` non plus : elle est comptée
`NON EVALUABLE`.

> L'expérience 2 rangeait ces cas dans `AUCUNE SEQUENCE`, phase par défaut : une
> évaluation ratée y devenait un énoncé réflexif comme un autre, et son verdict
> entrait dans le taux publié.

`sigma_mensuel(ticker, d)` rend $\hat\sigma_d$, l'**écart-type des 12 écarts
mensuels précédents** de la valeur contre `TR39`, calculés de fin de mois à fin
de mois sur le calendrier de la référence, tous **antérieurs à `d`**. S'il en
manque un seul, la fonction rend `None` et aucune thèse `REFLEXIVE` n'est écrite.

| Phase               | Condition à `d`                                  | `BORNE_BASSE` | `BORNE_HAUTE` | `BORNE_DEMENTI` |
| ------------------- | ------------------------------------------------ | ------------- | ------------- | --------------- |
| `AUTO-RENFORCEMENT` | `TEND_120 = +1`, `TEND_20 = +1`, `POSITION > 65` | `+0,5 σ̂`     | *(vide)*      | `−0,5 σ̂`       |
| `RETOURNEMENT`      | `TEND_120 = −1`, `TEND_20 = −1`, `POSITION < 35` | *(vide)*      | `−0,5 σ̂`     | `+0,5 σ̂`       |
| `AUCUNE SEQUENCE`   | tous les autres cas                              | `−σ̂`         | `+σ̂`         | *(vide)*        |

`VALEUR_CONSTATEE` est l'écart de rendement relatif sur `[d, d']`, en points :

$$100 \times \left(\frac{\text{Close}_{\text{valeur}}(d')}{\text{Close}_{\text{valeur}}(d)}
- \frac{\text{Close}_{\text{TR39}}(d')}{\text{Close}_{\text{TR39}}(d)}\right)$$

#### Les quatre verdicts

`depouiller(basse, haute, dementi, constatee)` sert les deux types de thèse :

| | `CONFIRMEE` | `DEMENTIE` | sinon |
|---|---|---|---|
| `CANAL` | `basse ≤ x ≤ haute` | `x < basse` ou `x > haute` | — |
| `AUCUNE SEQUENCE` | `−σ̂ ≤ x ≤ +σ̂` | `\|x\| > σ̂` | — |
| `AUTO-RENFORCEMENT` | `x ≥ +0,5 σ̂` | `x ≤ −0,5 σ̂` | **`ZONE MORTE`** |
| `RETOURNEMENT` | `x ≤ −0,5 σ̂` | `x ≥ +0,5 σ̂` | **`ZONE MORTE`** |

Une borne vide vaut `∓∞`. `NON TRANCHEE` si `VALEUR_CONSTATEE` manque.

> 🔑 **`ZONE MORTE` et `NON TRANCHEE` sont deux verdicts distincts.** Le premier
> dit *« la clause a été évaluée, et l'écart est trop petit pour trancher »*, le
> second *« il manque une donnée »*. Les confondre perdrait exactement ce que la
> piste S3 apporte.

> 🔑 **Les bornes de phase ne tombent plus sur le mode de la distribution.** En
> portant le seuil d'`AUTO-RENFORCEMENT` de `0` à `+0,5 σ̂`, le protocole crée
> une **zone morte** entre `−0,5 σ̂` et `+0,5 σ̂` où la phase n'est ni confirmée
> ni démentie. C'est délibéré : une phase qui se joue à un dixième de point de
> l'origine n'est pas une phase, c'est un tirage à pile ou face. Le prix en est un
> nombre de thèses tranchées mécaniquement plus faible pour ces deux phases, et
> le bilan publie les deux comptes séparément.

Le taux de confirmation d'une phase se lit donc **sur ses seules thèses
tranchées** — `CONFIRMEE + DEMENTIE` —, et le bilan publie à côté le nombre de
`ZONE MORTE` et de `NON TRANCHEE`, pour qu'aucun dénominateur ne soit implicite.

La dernière date d'audit n'a pas de date de décision suivante : ses thèses sont
dépouillées à la **dernière séance de la série**, `FIN_SERIE`. C'est une mesure
postérieure, publiée au bilan et jamais dans un journal mensuel.

**Écrit** : `theses.csv`, colonnes `DATE, TICKER, TYPE, PHASE, ENONCE,
BORNE_BASSE, BORNE_HAUTE, BORNE_DEMENTI, SIGMA, DATE_DEPOUILLEMENT,
VALEUR_CONSTATEE, VERDICT`.
`ENONCE` est la phrase française lisible, engendrée par le moteur ; `SIGMA` est
$\hat\sigma_d$, publié pour que la clause soit vérifiable.

### 8. Phase 6 — les audits

`poids_effectifs(criteres, dates, sens)` — la part de variance que chaque
composante explique dans le score :
$\operatorname{Cov}(s_i, \text{score}) / \operatorname{Var}(\text{score})$, dont
la somme vaut exactement 1. Calculée sur l'étalonnage et sur l'audit. Une
composante de variance nulle rend un poids de 0.

`occurrences_s5(criteres, dates, sens)` — le nombre d'évaluations où `s5` est non
nulle, **par signe**, et le détail par valeur. Le bilan en tire une phrase
**engendrée**, jamais rédigée d'avance : l'expérience 2 portait dans son moteur
un paragraphe qui affirmait « toutes à `−1` », vrai de son année et faux dès
qu'une autre année serait passée dans le même code.

`taux_vetos(criteres, dates)` — pour chacun des quatre vetos, le nombre
d'évaluations où il se déclenche, sa proportion, et son IC95 par
$\hat p \pm 1{,}96\sqrt{\hat p(1-\hat p)/n}$. Les `ERREUR` sont comptées à part.

#### Les deux comptes d'entrées bloquées

L'expérience 2 publiait un seul nombre, et il était faux : il comptait toutes les
occasions où une valeur bien classée était sous veto, **sans regarder s'il
restait un créneau libre** pour l'acheter. Le moteur en publie deux, nommés :

- `occasions_bloquees` — les couples (date, valeur) de rang `≤ --rang-entree`, de
  score strictement positif, non détenus, sous veto. C'est un compte
  d'**occasions**, pas d'achats ;
- `achats_bloques` — les achats que la simulation **sans veto** a réellement
  passés sur une valeur alors sous veto. C'est la différence exacte, en ordres,
  entre la règle appliquée et la règle de 2022.

#### `stabilite(criteres, dates, args)`

Pour chaque couple (date, valeur) de l'année narrée, compare `s3` et le score
entre `DECISION`, `DECALE-1` et `DECALE-2`, et rend le nombre de bascules de
`s3`, le nombre de changements de score, et le nombre de dates dont l'ensemble
des cinq premiers rangs change.

#### `survie_encadrement(theses, criteres, …)`

Le taux de démenti des thèses `CANAL` — **hors `INCONFIRMABLE`** —, la part des
évaluations dont `τ < k`, la part des `τ` infinis et la médiane des `τ` finis.

#### `jugement_vetos(theses, criteres, stabilite, dates)` — piste C3

Confronte chaque veto à l'**issue déclarée au protocole** :

| Veto | Issue | Ce que le moteur calcule |
|---|---|---|
| 1 | tenue de la thèse `CANAL` | taux de confirmation `CANAL` sous veto 1 / hors veto 1, différence, IC95 de la différence |
| 2 | tenue de la thèse `CANAL` | idem pour le veto 2 |
| 3 | stabilité de `s3` à d−1 | taux de bascule de `s3` sous veto 3 / hors veto 3, différence, IC95 |
| 4 | *(aucune)* | rien : le bilan écrit que le veto est arithmétique et ne prétend rien séparer |

L'IC95 de la différence de deux proportions est
$1{,}96\sqrt{\hat p_1(1-\hat p_1)/n_1 + \hat p_2(1-\hat p_2)/n_2}$. Un groupe
vide rend une ligne sans différence, jamais une différence inventée — **et le
bilan le nomme** : une ligne muette qu'on ne commente pas se lit comme une
absence de mesure, alors que c'est une mesure impossible, ce qui est un résultat.

> 🔑 **Le veto 2 ne peut pas être jugé contre l'issue que le protocole lui a
> assignée, et c'est structurel.** Le veto 2 se déclenche quand $\tau < 20$
> séances ; la cadence médiane entre deux décisions est du même ordre. Or une
> thèse `CANAL` dont $\tau$ est plus court que la cadence voit ses bornes se
> croiser, reçoit le verdict `INCONFIRMABLE` et sort du dénominateur. Le groupe
> « sous veto 2 » est donc **vide par construction** : les deux énoncés sont le
> même. Le bilan l'écrit au lieu d'afficher un tiret.

> **Un veto dont la différence contient zéro n'est pas retiré.** Le protocole l'a
> déclaré bloquant, et le retirer après l'avoir vu plat serait le
> rétro-ajustement même. Le bilan publie le chiffre ; l'expérience suivante en
> fera ce qu'elle voudra, **par une déclaration écrite avant sa première séance**.

#### `sensibilite(criteres, dates)` — piste C1

Pour chacun des cinq jeux de paramètres — le déclaré et les quatre variantes —
le taux de déclenchement de chaque veto, la part d'évaluations sans veto, et la
**part d'évaluations dont `s3` diffère de celui du jeu déclaré**. Une évaluation
absente d'une variante est comptée au dénominateur du seul jeu où elle existe.

#### `dimensionnement(valeurs, ref100, valeurs_f, seances, dotation)` — piste T1

- la **tracking error réalisée** sur l'année narrée, et l'effet minimal
  détectable qui en découle ;
- l'**écart apparié** entre le portefeuille et son fantôme, et son propre effet
  minimal détectable ;
- la **régression** des rendements quotidiens du portefeuille sur ceux de la
  référence : `bêta`, `alpha` de régression **annualisé**, coefficient de
  détermination `R²`, écart-type du résidu, et l'**IC95 de l'alpha** par
  $\hat\sigma_\varepsilon / \sqrt{n}$ annualisé.

> 🔑 **L'alpha de régression et l'écart de performance ne mesurent pas la même
> chose.** Le second suppose un bêta de 1 ; le premier ne le suppose pas. Un
> portefeuille souvent en espèces a un bêta nettement inférieur à 1, et l'écart
> de performance lui attribue alors une prudence que la régression sépare du
> talent. Les deux sont publiés côte à côte, avec leurs incertitudes.

### 9. Phase 7 — les graphiques

`svg()` écrit, pour chaque mois, une figure de 900 × 420 à **deux courbes en base
100** — le portefeuille et `TR39` — du 3 janvier à la dernière séance du mois
courant, avec un trait vertical pointillé à chaque date d'exécution. Grille
horizontale à pas choisi par `pas_de_grille()` pour ne jamais dépasser huit
lignes, ligne 100 en gris plus soutenu.

> L'échelle est calculée sur les seules séances tracées. Le graphique de mars ne
> connaît pas avril : c'est la même interdiction de regard en avant que pour les
> décisions.

**Écrit** : `graphiques/portefeuille-2022-MM.svg`, douze fichiers, en plus des
467 figures de décision conservées pendant la collecte.

### 10. Phase 8 — les markdown

Avec `--markdown` seulement.

`charger_textes()` lit [`actualites.md`](actualites.md) et
[`chartiste.md`](chartiste.md) et les découpe par `decouper()` : les sections
`## AAAA-MM` du premier, les sections `## AAAA-MM-JJ` puis `### TICKER` du
second. **Les deux fichiers sont requis** : leur absence est une sortie 1.

`journal_mensuel()` écrit `rapports/2022-MM.md`, neuf sections dans l'ordre
déclaré au README. Une section dont le texte manque porte la mention
`*(section absente)*` — jamais un texte inventé.

La **section 4** publie, après les données générales et le graphique, le
**tableau de toutes les positions prises depuis le début de l'expérience**,
closes comme ouvertes, engendré par `positions_a_date(ordres, jusqu_a)` :
`| Société | Prix d'achat | Date d'achat | Prix de vente | Date de vente |`. Une
position encore ouverte laisse les deux dernières colonnes vides. Le tableau
n'utilise **aucune séance postérieure** à la fin du mois courant.

La **section 5** rend une note par valeur de l'univers du jour, chacune précédée
de sa **figure de décision** :

```markdown
### 12. `SU.PA` — Schneider Electric

![Figure de décision SU.PA au 2022-05-31](../graphiques/SU.PA/decision-SU.PA-2022-05-31.svg)

- …
```

Une figure absente du répertoire — collecte incomplète, ou règle en échec —
n'est pas insérée, et la note porte alors la mention `*(figure absente)*`. Le
moteur ne fabrique pas un lien vers un fichier qui n'existe pas.

> 🔑 **Les valeurs non classées reçoivent leur note quand même**, à la suite des
> valeurs classées, sous un titre sans numéro de rang portant la mention
> *« hors classement »*. Une évaluation que la règle n'a pas su produire ne doit
> ni faire acheter ni faire vendre — mais la valeur reste dans l'univers du jour,
> et la taire ferait disparaître du journal une société que le protocole déclare
> étudier. C'est le cas de Kering aux décisions du 2022-03-31 et du 2022-04-29.

`lecture_du_mois()` rend un paragraphe **entièrement calculé** : meilleure et
moins bonne contribution en euros, frais du mois, position par rapport à `TR39`,
et le taux de confirmation des thèses dépouillées.

> **Le périmètre des contributions comprend les lignes vendues dans le mois.**
> L'expérience 2 ne regardait que les lignes encore détenues à la fin du mois :
> une ligne vendue le 2 et suivie d'une chute était invisible, et la « moins
> bonne contribution » du mois pouvait être la deuxième moins bonne. La
> contribution d'une ligne vendue court de son prix de référence au **prix de
> vente**, frais des deux sens déduits.

`bilan_annuel()` écrit [`bilan-2022.md`](bilan-2022.md), douze sections : le
compte, mois par mois, les positions, **l'univers et ses mouvements**, l'audit de
la règle, **le jugement des vetos** (C3), **la sensibilité aux paramètres** (C1),
le sens de `s3`, la durée de vie de l'encadrement, **le registre des thèses**
(S1, S3), les trois conventions, **le dimensionnement confronté** (T1), et ce que
l'expérience établit ou n'établit pas.

### 11. La console

Sans `--mois`, le moteur imprime un bloc par mois investi — classement complet
avec vetos, exposition héritée, ordres, valeur de fin de mois — puis le bloc de
bilan :

```
=== Bilan au 2022-12-30 ===

  Dotation                10 000,00 EUR au 2022-01-03
  Valeur finale           ...
  Performance             ...
  TR39                    ...
  Alpha sur l'annee       ... pt   (non concluant : MDE +/- ... pt)
  Alpha de regression     ... %/an  (beta ..., IC95 +/- ... pt)

  Fantome (s3 exp. 1)     ... base 100 · ecart appari ... pt
  Ordres                  ... (... achats, ... ventes)
  Frais cumules           ... EUR, soit ... % de la dotation
  Vetos declenches        ... / 923 evaluations
  Occasions bloquees      ...   ·   achats bloques ...
  Theses                  ... confirmees sur ... tranchees
```

Le classement d'un mois affiche, sous le tableau, la liste des valeurs **non
classées** — sortie de l'indice, ou évaluation en erreur — avec leur motif.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | exécution complète |
| `1` | série absente, `univers.csv` ou `canaux.csv` absent ou incomplet, ticker sans nom déclaré, `criteres.csv` absent sans `--collecter`, calendrier incomplet, argument invalide, ou `actualites.md` / `chartiste.md` absent avec `--markdown` |

## Cas limites

- **Un ticker sans séance à une date d'exécution** : erreur fatale. Un ordre ne
  peut pas être exécuté à un prix qui n'existe pas.
- **Une valeur qui quitte l'indice alors qu'elle est détenue** : conservée, sans
  ordre, motif consigné. Décision de protocole, déclarée au README.
- **Une valeur qui entre dans l'indice** : évaluable dès sa première date de
  décision dans `univers.csv`, à condition d'y être `RETENUE`. Les 253 séances de
  volume strictement positif exigées par le critère 5 sont vérifiées **en amont**,
  à la construction du fichier, et non à l'exécution.
- **`τ` infini** : le canal est parallèle ou divergent ; le veto 2 ne se
  déclenche pas, et les bornes de la thèse `CANAL` restent dans le bon ordre.
- **Position hors canal** (`POSITION` < 0 ou > 100) : reprise telle quelle. `s3`
  vaut alors `+1` ou `−1` dans le sens aligné — la valeur est extrême, le score
  le dit.
- **Aucun candidat à l'achat** : les espèces restent oisives, aucun ordre n'est
  écrit, et la console le dit.
- **Toutes les valeurs sous veto** : cas possible et non pathologique ; le
  portefeuille reste en l'état.
- **Une composante manquante** : elle compte pour 0 dans le score et s'affiche
  `.`. `criteres.csv` garde la trace de laquelle manquait.
- **$\hat\sigma_d$ nul** — douze écarts mensuels rigoureusement identiques : la
  clause `AUCUNE SEQUENCE` devient d'épaisseur nulle. Le cas est traité comme un
  $\hat\sigma_d$ indisponible et **aucune thèse `REFLEXIVE` n'est écrite**, pour
  la même raison qu'une série à volume nul n'est pas un cours.
- **Une thèse dont la valeur constatée manque** : `NON TRANCHEE`. Elle compte au
  dénominateur des thèses écrites, jamais à celui des thèses dépouillées.
