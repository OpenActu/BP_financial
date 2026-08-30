# import_fondamentaux.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `import_fondamentaux.py`, étape par
étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du script
doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Récupérer, pour une ou plusieurs valeurs, les **indicateurs fondamentaux et de
marché** que `import_societe.py` ne fournit pas : valorisation (PER, P/B,
VE/EBITDA, rendement du FCF), rentabilité (ROE, marges), structure financière
(dette/EBITDA), taille (capitalisation, flottant) et première limite du carnet
d'ordres (bid, ask, spread).

Le complément de [`import_societe.py`](import_societe.md), qui ne rend que de
l'OHLCV. Ensemble, les deux couvrent les familles de sélection décrites au § 3 de
l'agent [`trading`](../.claude/agents/trading.md).

> 🔑 **Toute valeur est reprise de la source ou calculée depuis ses composants —
> aucune n'est estimée.** Quand ni le ratio ni ses composants ne sont
> disponibles, la cellule reste **vide**. Une cellule vide est une information ;
> un nombre plausible n'en est pas une.

## Ce que cette source ne peut pas donner

> ⚠️ **La profondeur du carnet d'ordres n'est pas accessible par Yahoo Finance,
> et ce script ne la produira jamais.** Yahoo expose au mieux la **première
> limite** — meilleur acheteur, meilleur vendeur et leurs quantités. Les limites
> 2 à 10, le nombre d'ordres par limite et l'historique du carnet relèvent des
> données de **niveau 2**, qui se paient auprès d'Euronext ou d'un courtier et
> transitent par un autre protocole.
>
> Le script produit donc `BID`, `ASK`, `BID_TAILLE`, `ASK_TAILLE`, `SPREAD` et
> `SPREAD_PCT` — la limite 1, honnêtement nommée — et **aucune colonne de
> profondeur**. Il l'écrit dans son résumé console à chaque exécution.

Deux réserves supplémentaires sur cette limite 1 :

- **Hors séance, Yahoo rend `0.0` pour `bid` et `ask`**, et non une valeur
  absente. Le script traite un bid ou un ask **nul ou négatif** comme manquant :
  les six colonnes de carnet restent alors vides plutôt que d'afficher un spread
  de $0$ €, qui serait faux et flatteur.
- Même en séance, ces valeurs sont **différées** et ne constituent pas un carnet
  temps réel exploitable pour de l'exécution.

## Dépendances

- `yfinance` — seule dépendance externe, comme pour `import_societe.py`.
- Modules standard : `argparse`, `csv`, `datetime`, `json`, `math`, `sys`, `pathlib`.
- **Ni `pandas` requis explicitement, ni `scipy`.** `pandas` arrive avec
  `yfinance` mais ce script ne s'en sert pas : il n'écrit que des lignes.

## Invocation

```bash
python python/import_fondamentaux.py AIR.PA
python python/import_fondamentaux.py AIR.PA MC.PA OR.PA SAN.PA
python python/import_fondamentaux.py AIR.PA --csv airbus_fonda.csv
python python/import_fondamentaux.py AIR.PA --json
```

Sans argument, le script demande les tickers de façon interactive — même
comportement que `import_societe.py`, séparateur espace ou virgule.

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `tickers` | — | Un ou plusieurs tickers Yahoo. Les valeurs de Paris portent le suffixe `.PA` (`AIR.PA`, `MC.PA`). |
| `--csv` | `docs/raw/fondamentaux/fondamentaux_{AAAA-MM-JJ}.csv` | Chemin du CSV produit (répertoire créé si besoin). |
| `--json` | — | Écrit en plus un `.json` de même nom, contenant les valeurs **non arrondies** et les composants ayant servi aux calculs. |
| `--sans-carnet` | — | N'interroge pas la limite 1 du carnet ; les six colonnes correspondantes restent vides. |
| `--archiver` | — | Ajoute les lignes du jour a **l'archive** `docs/raw/fondamentaux/archive.csv` (§ 5.1). |

## Déroulé d'exécution

### 1. Résolution des tickers

`argparse` lit la ligne de commande. Sans ticker, invite interactive
`Ticker(s) Yahoo (ex. AIR.PA MC.PA) : ` ; la saisie est découpée sur les espaces
et les virgules, et mise en majuscules. Saisie vide : message sur `stderr` et
**sortie 1**.

### 2. Interrogation, valeur par valeur

Pour chaque ticker, un seul appel `yf.Ticker(ticker).info`. Les échecs sont
**isolés** : une valeur qui échoue produit une ligne dont toutes les colonnes
chiffrées sont vides et un message sur `stderr` ; les autres sont traitées
normalement.

Une valeur dont `quoteType` vaut `INDEX`, `ETF` ou `CURRENCY` n'a pas de
fondamentaux : le script l'annonce (`{ticker} : {quoteType}, sans fondamentaux`)
et n'écrit que les colonnes d'identité et de marché disponibles. Un indice comme
`^FCHI` tombe dans ce cas — il n'a ni PER, ni ROE, ni capitalisation.

### 3. Les colonnes produites

Identité et marché :

| Colonne | Source |
|---|---|
| `TICKER` | l'argument |
| `NOM` | `shortName` |
| `DEVISE` | `currency` |
| `SECTEUR` | `sector` |
| `TYPE` | `quoteType` |
| `COURS` | `currentPrice`, sinon `regularMarketPrice`, sinon `previousClose` |
| `DATE` | date d'exécution `AAAA-MM-JJ` |

Valorisation :

| Colonne | Priorité 1 — champ direct | Priorité 2 — calcul | Unité |
|---|---|---|---|
| `PER` | `trailingPE` | `COURS / trailingEps` | — |
| `PER_PREV` | `forwardPE` | `COURS / forwardEps` | — |
| `P_B` | `priceToBook` | `CAPI / (bookValue × ACTIONS)` | — |
| `VE_EBITDA` | `enterpriseToEbitda` | `VE / EBITDA` | — |
| `REND_FCF` | — | `100 × freeCashflow / CAPI` | % |

Rentabilité et structure :

| Colonne | Priorité 1 | Priorité 2 | Unité |
|---|---|---|---|
| `ROE` | `100 × returnOnEquity` | — | % |
| `MARGE_BRUTE` | `100 × grossMargins` | — | % |
| `MARGE_OP` | `100 × operatingMargins` | — | % |
| `MARGE_NETTE` | `100 × profitMargins` | — | % |
| `DETTE_EBITDA` | — | `totalDebt / EBITDA` | × |

Taille :

| Colonne | Source | Unité |
|---|---|---|
| `CAPI` | `marketCap` | devise |
| `VE` | `enterpriseValue` | devise |
| `EBITDA` | `ebitda` | devise |
| `DETTE` | `totalDebt` | devise |
| `FCF` | `freeCashflow` | devise |
| `ACTIONS` | `sharesOutstanding` | titres |
| `FLOTTANT` | `floatShares` | titres |
| `FLOTTANT_PCT` | `100 × floatShares / sharesOutstanding` | % |

Carnet d'ordres — **limite 1 seulement** (§ *Ce que cette source ne peut pas
donner*) :

| Colonne | Source | Unité |
|---|---|---|
| `BID` | `bid`, si $> 0$ | devise |
| `ASK` | `ask`, si $> 0$ | devise |
| `BID_TAILLE` | `bidSize`, si $> 0$ | titres |
| `ASK_TAILLE` | `askSize`, si $> 0$ | titres |
| `SPREAD` | `ASK − BID` | devise |
| `SPREAD_PCT` | `100 × (ASK − BID) / ((ASK + BID) / 2)` | % |
| `VOLUME` | `volume` | titres |
| `VOLUME_MOY_3M` | `averageDailyVolume3Month` | titres |

`SPREAD` et `SPREAD_PCT` ne sont calculés que si `BID` **et** `ASK` sont
strictement positifs, et si `ASK ≥ BID`. Un carnet croisé (`ASK < BID`) est un
artefact de données différées : les deux colonnes restent vides et le script le
signale.

### 4. Arrondis

Le CSV est destiné à être lu. Les arrondis sont donc appliqués à l'écriture, et
**seulement là** :

| Nature | Décimales |
|---|---|
| Ratios (`PER`, `P_B`, `VE_EBITDA`, `DETTE_EBITDA`) | 2 |
| Pourcentages (`ROE`, marges, `REND_FCF`, `FLOTTANT_PCT`, `SPREAD_PCT`) | 2 |
| Cours, `BID`, `ASK`, `SPREAD` | 4 |
| Montants et nombres de titres | 0 |

Le `.json` de `--json` contient les valeurs **non arrondies**, plus un objet
`composants` par ticker listant les champs bruts effectivement utilisés — de quoi
refaire chaque calcul sans réinterroger la source.

### 5. Écriture

Un CSV **UTF-8 avec BOM** (`utf-8-sig`, pour qu'Excel lise correctement les
accents), séparateur virgule, une ligne par ticker, colonnes dans l'ordre des
tableaux du § 3. Les valeurs manquantes sont écrites **vides**, jamais `nan`,
`None` ou `0`.

Le répertoire par défaut `docs/raw/fondamentaux/` est **exclu du suivi git**, au
même titre que `docs/raw/quotes/` : ces données sont régénérables et datées du
jour de l'appel.

### 5.1 — L'archive, la seule donnée qui ne se régénère pas

`--archiver` **ajoute** les lignes du jour à `docs/raw/fondamentaux/archive.csv`,
mêmes colonnes que le CSV du jour. Le fichier est créé avec son en-tête s'il
n'existe pas.

C'est la réponse au manque décrit au
[module 2 du cours fondamentaux](../docs/raw/concept/semestre4/fondamentaux/02-les-quatre-dates-d-un-ratio.md) :
on ne peut pas reconstituer le passé, mais on peut **commencer à horodater le
présent**. Chaque ligne porte sa `DATE` de lecture, qui est un fait observé et
non une date reconstituée — contrairement à celles de
[`reconstituer_fondamentaux.py`](reconstituer_fondamentaux.md), qui les déduit.

> 🔑 **L'archive est le seul fichier de `docs/raw/` qui n'est pas régénérable, et
> le seul qui soit suivi par git.** Tout le reste — cours, graphiques, CSV du
> jour — se reconstruit d'un appel. Une archive perdue est perdue pour de bon :
> c'est pourquoi `.gitignore` l'excepte explicitement de l'exclusion de
> `docs/raw/fondamentaux/`.

**Doublons.** Le script refuse d'écrire une ligne dont le couple
`(TICKER, DATE)` figure déjà dans l'archive, et le signale sans erreur :
`{ticker} : deja archive au {date}, ignore`. Relancer deux fois le même jour est
donc sans effet — utile si l'appel est planifié et rejoué.

**Ce que l'archive permet, et quand.** Rien le premier jour. Une série
exploitable après quelques trimestres. Un historique comparable à celui d'un
fournisseur de données après des années. C'est lent, et c'est la seule méthode
dont la date n'est pas une hypothèse.

### 6. Résumé console

Une ligne d'en-tête, puis une ligne par ticker avec les colonnes les plus lues,
puis les avertissements :

```
Valeur         Cours      PER    P/B  VE/EBITDA  Rdt FCF     ROE  Marge op.  Dette/EBITDA          Capi   Flottant
AIR.PA        203.05    27.04   6.21      17.99     1.95   23.19      11.36          1.59     160.71 Md     74.3 %
MC.PA         458.15    20.90   3.32      12.59     5.11   16.59      22.52          1.85     225.85 Md     49.0 %
TTE.PA         74.67    10.90   1.49       5.04     8.19   14.48      12.79          1.59     165.22 Md     92.5 %

AIR.PA : carnet indisponible — bid ou ask absent (hors séance ?)
MC.PA : carnet indisponible — bid ou ask absent (hors séance ?)
TTE.PA : carnet indisponible — bid ou ask absent (hors séance ?)
Profondeur du carnet : non fournie par Yahoo Finance (données de niveau 2, payantes chez Euronext ou un courtier).
Fondamentaux écrits dans : {chemin}
```

Les grands nombres sont abrégés dans la console (`Md`, `M`, `k`) mais écrits en
entier dans le CSV.

### 7. Cas limites

- **Ticker vraiment inconnu** : la source répond `404`, toutes les colonnes
  chiffrées sont vides, message `{ticker} : aucune donnée — suffixe de place
  manquant ?` sur `stderr`, et le script **continue** avec les autres tickers.
- ⚠️ **Suffixe de place oublié : le danger n'est pas l'absence de donnée, c'est
  la mauvaise société.** `AIR` sans `.PA` n'échoue pas — c'est le ticker d'AAR
  Corp à New York, et le script rend consciencieusement ses fondamentaux en
  dollars. Aucun contrôle automatique ne peut détecter cela ; les deux garde-fous
  sont la colonne `NOM`, à relire, et l'avertissement de **devises mélangées**
  qui se déclenche dès qu'un même appel mêle plusieurs monnaies. Vérifier `NOM`
  avant d'exploiter une ligne.
- **Toutes les valeurs en échec** : sortie **1**.
- **EBITDA nul ou négatif** : `VE_EBITDA` et `DETTE_EBITDA` restent vides. Un
  multiple d'EBITDA négatif n'a pas de sens économique et ne doit pas être écrit.
- **Bénéfice négatif** : Yahoo ne rend alors pas de `trailingPE`. La colonne
  reste vide — elle n'est **pas** remplie par un PER négatif, qui ne se compare à
  rien.
- **`sharesOutstanding` absent** : `FLOTTANT_PCT` reste vide même si `floatShares`
  est connu.
- **Devises hétérogènes** : les montants ne sont **pas** convertis. La colonne
  `DEVISE` est là pour empêcher d'additionner des capitalisations en euros et en
  couronnes ; le script avertit si un même appel mélange plusieurs devises.

## Ce que ces données ne disent pas

- Elles sont **datées du jour de l'appel**. Sans `--archiver`, rien ne s'accumule
  et aucun PER passé n'est reconstituable ; deux réponses partielles existent,
  l'archive du § 5.1 pour l'avenir et
  [`reconstituer_fondamentaux.py`](reconstituer_fondamentaux.md) pour les quatre
  ou cinq exercices que la source expose. Le [piège du regard en avant](../docs/raw/concept/semestre4/trading/04-les-pieges-du-passage-a-l-acte.md)
  s'applique intégralement — un fondamental n'est connu qu'à sa date de
  publication, et Yahoo ne dit pas laquelle.
- Le **biais du survivant** n'est pas corrigé : un univers construit aujourd'hui
  exclut les faillites.
- Ces chiffres ne constituent **aucune recommandation d'investissement**. Ils
  décrivent une entreprise à une date, pas ce qu'il convient d'en faire.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Au moins une valeur récupérée, CSV écrit. |
| `1` | Aucun ticker fourni, saisie interactive vide, ou toutes les valeurs en échec. |

## Fonctions internes

- `recuperer_fondamentaux(ticker, avec_carnet)` — un appel `yf.Ticker(...).info`,
  puis assemblage du dictionnaire de colonnes. Rend aussi les composants bruts.
- `_ratio(direct, numerateur, denominateur)` — applique la règle de priorité du
  § 3 : champ direct, sinon calcul, sinon `None`. Refuse un dénominateur nul,
  négatif ou absent.
- `_carnet(info)` — la limite 1 et le spread, avec les contrôles du § 3.
- `formater(valeur, decimales)` — arrondi à l'écriture, chaîne vide si `None`.
- `abreger(nombre)` — `Md` / `M` / `k` pour la console uniquement.
- `main()` — CLI argparse, boucle sur les tickers, écriture CSV et JSON, résumé.

## Constantes

- `REPERTOIRE_DEFAUT = Path("docs/raw/fondamentaux")` — destination par défaut,
  exclue du suivi git.
- `TYPES_SANS_FONDAMENTAUX = {"INDEX", "ETF", "CURRENCY", "MUTUALFUND"}`.
- `COLONNES` — l'ordre exact des colonnes du CSV, unique source de vérité pour
  l'en-tête comme pour les lignes.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
