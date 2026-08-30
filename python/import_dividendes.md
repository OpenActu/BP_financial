# import_dividendes.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `import_dividendes.py`, étape par
étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du script
doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Récupérer l'**historique des dividendes** et des **divisions du nominal** depuis
les archives de `bnains.org`, les normaliser, et les **confronter** à ce que rend
`yfinance`.

Trois apports que la source Yahoo ne donne pas :

| Apport | Ce que ça débloque |
|---|---|
| **Anciennes composantes du CAC 40** | le **biais du survivant** — la seule attaque possible depuis ce dépôt |
| **Date d'annonce** | la date de publication, la même qui manquait pour les comptes ([fondamentaux, module 2](../docs/raw/concept/semestre4/fondamentaux/02-les-quatre-dates-d-un-ratio.md)) |
| **Type : acompte / solde / exceptionnel** | yfinance agrège ; sans la ventilation, un dividende exceptionnel gonfle un facteur *rendement* |

Plus une profondeur supérieure — Saint-Gobain **1988** contre 2000 chez yfinance,
Accor 1994 contre 2000, Airbus 1999 contre 2002 — variable selon la valeur.

> ⚠️ **Ce script ne donne ni cours, ni comptes.** Il ne résout rien du problème
> de profondeur des ratios de valorisation, qui reste celui de
> [`reconstituer_fondamentaux.py`](reconstituer_fondamentaux.md).

## Le piège de la colonne « Dividende brut »

> 🔑 **La colonne intitulée « Dividende brut » porte, pour les années à retenue à
> la source, un montant qui en est déjà **net**.** La source le dit elle-même en
> commentaire : `Dividende brut = 0,2 €. Le dividende pris en compte intègre les
> 15% de retenue à la source.` Le libellé de colonne et le commentaire se
> contredisent ; c'est le commentaire qui est exact.

Conséquence mesurée sur Airbus, en confrontant la colonne **telle que publiée**
à yfinance : 14 montants identiques et **5 écarts exactement égaux au facteur de
retenue** — rapport $0{,}7500$ pour 25 %, $0{,}8500$ pour 15 %. Mélanger les deux
sources sans normaliser sous-estimerait le rendement de 15 à 25 % sur les années
2001-2009. Une fois `MONTANT_BRUT` reconstruit, ces cinq lignes deviennent
identiques : c'est la mesure de ce que la normalisation apporte.

Le script produit donc **deux colonnes distinctes** : `MONTANT` tel que publié
par la source, et `MONTANT_BRUT` reconstruit depuis le commentaire. C'est
`MONTANT_BRUT` qui se compare à yfinance.

## Dépendances

- `yfinance` pour le contrôle croisé — et lui seul en dépendance externe.
- Modules standard : `argparse`, `csv`, `html`, `re`, `sys`, `time`,
  `urllib.request`, `pathlib`, `datetime`.
- **Pas de `requests`, pas de `beautifulsoup4`.** L'analyse se fait par
  expressions régulières sur une structure vérifiée (§ 2).

## Invocation

```bash
python python/import_dividendes.py --index
python python/import_dividendes.py NL0000235190 --ticker AIR.PA
python python/import_dividendes.py FR0000125007 FR0000120404
python python/import_dividendes.py --toutes --delai 2
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `isins` | — | Un ou plusieurs codes ISIN. Sans argument ni `--toutes` ni `--index`, invite interactive. |
| `--index` | — | Affiche la liste des valeurs proposées par la source (ISIN, nom) et s'arrête. |
| `--toutes` | — | Traite **toutes** les valeurs de l'index, anciennes composantes comprises. |
| `--ticker` | — | Ticker Yahoo pour le contrôle croisé du § 5. Valide seulement avec un ISIN unique. |
| `--divisions` | — | Écrit aussi le tableau des divisions du nominal. |
| `--delai` | `1.5` | Secondes d'attente entre deux requêtes. **Ne pas descendre en dessous de 1.** |
| `--rafraichir` | — | Ignore le cache local et réinterroge la source. |
| `--csv` | `docs/raw/dividendes/dividendes_{AAAA-MM-JJ}.csv` | Chemin de sortie. |

## Déroulé d'exécution

### 1. Politesse et cache

Le script interroge le serveur d'un tiers. Trois règles, non désactivables :

- **Un délai** entre deux requêtes, `--delai` secondes, jamais inférieur à 1 —
  une valeur plus basse est relevée à 1 et signalée ;
- **un `User-Agent` explicite**, `BP_financial/1.0 (script de recherche
  personnel)`, qui identifie l'appelant au lieu de se faire passer pour un
  navigateur ;
- **un cache local** dans `docs/raw/dividendes/cache/{codeISIN}.html`. Une page
  déjà téléchargée n'est **pas** redemandée, sauf `--rafraichir`. Le cache est
  exclu du suivi git ; les CSV produits, eux, sont suivis — ils évitent d'avoir
  à réinterroger la source.

Le `robots.txt` du site ne déclare aucune interdiction sur ces pages ; cela
n'autorise pas pour autant un rythme soutenu.

### 2. Analyse d'une fiche

L'URL est `https://www.bnains.org/archives/action.php?codeISIN={ISIN}`.

Le HTML des fiches a des balises `<tr>` **non fermées** : les lignes ne sont pas
délimitées. Le script ne s'y fie donc pas et découpe la suite des `<td>` en
**groupes de 9** pour le tableau des dividendes, de **5** pour celui des
divisions.

**Contrôle de structure, avant toute lecture.** Les 9 premières cellules du
tableau `id="table_dividendes"` doivent être exactement :

```
Date annonce · Date détachement · Date versement · Année réf. · Type ·
Dividende brut · Dividende normalisé · Rendement annuel · Commentaires
```

Si l'en-tête diffère, le script **s'arrête en sortie 2** plutôt que de produire
des colonnes décalées. C'est le garde-fou d'une analyse par expressions
régulières : la source peut changer sa mise en page sans prévenir.

Les entités HTML sont décodées (`html.unescape`), les espaces insécables
remplacés par des espaces ordinaires.

### 3. Normalisation d'une ligne

| Colonne produite | Origine |
|---|---|
| `ISIN`, `SOCIETE` | l'argument et le titre de la page |
| `ANNONCE`, `DETACHEMENT`, `VERSEMENT` | converties de `JJ/MM/AAAA` en `AAAA-MM-JJ` ; `-` et `?` deviennent **vides** |
| `ANNEE_REF` | entier |
| `TYPE` | `Solde`, `Acompte`, `Exceptionnel`… tel quel |
| `MONTANT` | la colonne « Dividende brut » de la source, en euros |
| `MONTANT_BRUT` | extrait du commentaire par `Dividende brut = ([0-9,.]+)` ; **à défaut, égal à `MONTANT`** |
| `RETENUE_PCT` | extrait du commentaire par `([0-9]+)% de retenue` ; vide sinon |
| `NORMALISE` | la colonne « Dividende normalisé », ajustée des divisions |
| `RENDEMENT` | en %, `-` devient vide |
| `COMMENTAIRE` | texte intégral, séparateurs internes neutralisés |

> ⚠️ **Un dividende annulé** — Airbus 2019, « annulé suite à crise Coronavirus » —
> est publié avec `MONTANT = 0`, pas ignoré. Un zéro daté est une information ;
> une ligne absente n'en est pas une.

### 4. Divisions du nominal

Second tableau de la fiche, 5 colonnes : `Date division`, `Diviseur`,
`Date dernier cours avant division`, `Dernier cours clôture avant division`,
`Commentaires`. Écrit dans un fichier séparé `divisions_{AAAA-MM-JJ}.csv` quand
`--divisions` est passé. Un tableau vide — cas d'Airbus — ne produit aucune
ligne et n'est pas une erreur.

### 5. Contrôle croisé avec yfinance

Avec `--ticker`, le script compare, **par date de détachement** :

- la somme des `MONTANT_BRUT` de la source pour cette date — somme, parce que la
  source sépare solde et exceptionnel là où yfinance agrège ;
- la valeur de `yf.Ticker(ticker).dividends`.

Chaque date reçoit un verdict :

| Verdict | Condition |
|---|---|
| `identique` | écart relatif $< 0{,}5\,\%$ |
| `retenue {r}%` | le rapport source/yfinance vaut $1 - r/100$ à $0{,}5\,\%$ près, et le commentaire annonce cette retenue |
| `ECART` | tout le reste |
| `absent d'une source` | la date ne figure que d'un côté |

Le résumé donne le décompte des quatre catégories. **Un `ECART` n'est pas une
erreur du script : c'est un désaccord entre deux sources, à trancher à la main.**

Résultat obtenu sur Airbus / `AIR.PA`, sur 22 dates : **19 identiques**,
2 présentes d'un seul côté, **1 écart**.

> 🔑 **L'écart est une erreur de la source, et le contrôle croisé l'a trouvée.**
> Au détachement du 22/04/2025, la fiche additionne un solde de 2,000 € et un
> exceptionnel de 2,000 €, soit 4,000 € — alors que son propre commentaire écrit
> « Dividende 2024 : 3 € dont exceptionnel de 1 € », et que yfinance rend 3,000 €.
> La ligne se contredit elle-même. C'est exactement ce à quoi sert la
> confrontation de deux sources : le script ne tranche pas, il signale.

Les deux dates orphelines sont les détachements de 2003 et 2005, que la source
laisse à `?` — elle ne les connaît pas, la cellule reste vide, et rien ne peut
être apparié.

### 6. Résumé console

```
Airbus Group (ex-EADS)                NL0000235190
  28 dividendes de 1999 a 2025 · 0 division(s)
  types : Exceptionnel 2 · Solde 26
  retenue a la source signalee sur 9 ligne(s)
  controle AIR.PA : 19 identiques · 0 expliques par la retenue · 1 ecart(s) · 2 orpheline(s)
      2003-05-12  source       —  yfinance   0.300  presente d'un seul cote
      2005-05-16  source       —  yfinance   0.500  presente d'un seul cote
      2025-04-22  source   4.000  yfinance   3.000  ECART rapport 1.3333

28 dividendes ecrits dans : docs/raw/dividendes/dividendes_2026-08-30.csv
```

Sur une ancienne composante, le gain se voit d'un coup d'oeil :

```
ALCATEL                               FR0000130007
  28 dividendes de 1988 a 2015 · 1 division(s)
```

**yfinance ne rend rien pour cette valeur** — `ALU.PA` répond *possibly delisted*,
`ALU` un 404. Vingt-huit ans d'historique que l'univers construit aujourd'hui
avait effacés.

### 7. Cas limites

- **ISIN inconnu** : la page répond mais sans tableau de dividendes ; message sur
  `stderr`, le ticker est ignoré, les autres sont traités.
- **Erreur réseau** : signalée, valeur ignorée, exécution poursuivie.
- **Colonne de date à `?`** : la source ignore la date. Cellule **vide**, jamais
  remplacée par une date approchée.
- **`--ticker` avec plusieurs ISIN** : refusé en sortie 1 — le contrôle croisé
  n'a de sens que pour une valeur.
- **En-tête de tableau modifié** : sortie 2 (§ 2).

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Au moins une valeur récupérée, CSV écrit. |
| `1` | Aucun ISIN utilisable, ou `--ticker` avec plusieurs ISIN. |
| `2` | Structure de la page inattendue — l'analyse serait décalée. |

## Fonctions internes

- `telecharger(url, cache, delai, rafraichir)` — requête polie avec cache local.
- `cellules(html_source, identifiant)` — les `<td>` d'un tableau, décodés.
- `decouper(cellules, largeur)` — groupes de `largeur` cellules, en-tête exclu.
- `verifier_entete(cellules)` — le garde-fou du § 2.
- `date_iso(texte)` — `JJ/MM/AAAA` → `AAAA-MM-JJ`, vide pour `-` et `?`.
- `montant(texte)` — `« 3.200 € »` → `3.2`.
- `brut_et_retenue(commentaire)` — le § 3, par expressions régulières.
- `lire_index(html_source)` — les couples (ISIN, société) de la page d'index.
- `controler(lignes, ticker)` — le § 5.

## Constantes

- `BASE = "https://www.bnains.org/archives/action.php"`.
- `AGENT = "BP_financial/1.0 (script de recherche personnel)"`.
- `DELAI_MINIMAL = 1.0` — secondes, plancher non contournable.
- `REPERTOIRE_DEFAUT = Path("docs/raw/dividendes")`, son sous-répertoire
  `cache/` étant exclu du suivi git.
- `ENTETE_ATTENDUE` — les 9 libellés du § 2, source de vérité du contrôle.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
