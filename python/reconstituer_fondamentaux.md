# reconstituer_fondamentaux.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `reconstituer_fondamentaux.py`,
étape par étape, dans l'ordre du déroulement. Il fait autorité : toute évolution
du script doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Reconstituer une **série historique de ratios fondamentaux**, séance par séance,
en n'utilisant à chaque date que ce qui était **publié** à cette date.

C'est la réponse partielle au manque établi par le
[module 2 du cours fondamentaux](../docs/raw/concept/semestre4/fondamentaux/02-les-quatre-dates-d-un-ratio.md) :
un ratio a quatre dates et
[`import_fondamentaux.py`](import_fondamentaux.md) n'en fournit que deux. Ce
script va chercher la **troisième — la date de publication** — et s'en sert pour
dater correctement chaque valeur comptable.

> 🔑 **La règle unique du script : à la séance $d$, on n'utilise que le dernier
> exercice dont la date de publication est $\le d$.** Jamais celui qui sera
> publié demain, même s'il porte sur une période déjà close. C'est toute la
> différence entre une série exploitable et un regard en avant.

## Ce que le script ne répare pas

> ⚠️ **Trois biais survivent à la reconstruction. Il faut les annoncer avec toute
> série produite ici.**
>
> - **Le chiffre servi n'est pas toujours celui qui fut publié.** La
>   reconstruction corrige le regard en avant sur la *date*, pas sur le
>   *contenu* — mais l'ampleur du problème dépend du poste, et se mesure
>   (§ 10).
> - **Le biais du survivant**, entier : un ticker radié a disparu de la source,
>   donc de tout univers construit aujourd'hui.
> - **La profondeur**, plafonnée par la source : 4 à 5 exercices annuels. Assez
>   pour illustrer une méthode, pas pour valider un facteur.

## Dépendances

- `yfinance` et `pandas` (installé avec lui).
- Modules standard : `argparse`, `csv`, `math`, `sys`, `pathlib`, `datetime`.
- **Ni `scipy`, ni bibliothèque de tracé.**

## Invocation

```bash
python python/reconstituer_fondamentaux.py AIR.PA
python python/reconstituer_fondamentaux.py AIR.PA BNP.PA --debut 2022-01-01
python python/reconstituer_fondamentaux.py AIR.PA --trimestriel --mensuel
python python/reconstituer_fondamentaux.py AIR.PA --decalage 90
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `tickers` | — | Un ou plusieurs tickers Yahoo. Sans argument, invite interactive. |
| `--debut` | la plus ancienne publication exploitable | Date `AAAA-MM-JJ` de début de la série. |
| `--fin` | aujourd'hui | Date `AAAA-MM-JJ` de fin. |
| `--trimestriel` | — | Utilise les comptes **trimestriels** (6 périodes) au lieu des annuels (4 à 5). |
| `--mensuel` | — | Ne garde que la **dernière séance de chaque mois**. Divise le volume par ~21. |
| `--decalage` | `75` | Décalage de repli, en jours, quand aucune date de publication réelle n'est trouvée (§ 3). |
| `--csv` | `docs/raw/fondamentaux/historique_{ticker}_{debut}_{fin}.csv` | Chemin de sortie (un fichier par ticker). |

## Déroulé d'exécution

### 1. Ce qu'on récupère, valeur par valeur

Cinq appels `yfinance` par ticker :

| Appel | Ce qu'il donne | Profondeur constatée sur AIR.PA |
|---|---|---|
| `income_stmt` / `quarterly_income_stmt` | `Net Income`, `Total Revenue`, `EBITDA`, `Operating Income`, `Gross Profit` | 4 exercices / 6 trimestres |
| `balance_sheet` / `quarterly_balance_sheet` | `Stockholders Equity`, `Total Debt`, `Cash And Cash Equivalents` | 4 exercices / 6 trimestres |
| `cashflow` / `quarterly_cashflow` | `Free Cash Flow` | 5 exercices |
| `get_earnings_dates(limit=100)` | les dates de publication **réelles** | 88 publications, de 2004 à 2026 |
| `get_shares_full(start=...)` | le nombre d'actions dans le temps | 706 points depuis 2019 |

Plus l'historique de cours, par `yf.Ticker(...).history(...)`.

Une ligne de compte absente laisse **vides** les ratios qui en dépendent ; ils ne
sont jamais remplacés par une estimation.

> ⚠️ **Les trois états n'ont pas la même profondeur.** Sur AIR.PA, le tableau de
> flux remonte à l'exercice 2021 alors que le compte de résultat et le bilan
> s'arrêtent à 2022. Une période présente dans un seul état, et **dont tous les
> postes sont vides**, est écartée : sans ce filtre elle produirait des centaines
> de lignes sans un seul ratio. Une période partiellement renseignée est en
> revanche conservée — les ratios calculables le sont, les autres restent vides.

### 2. La colonne des dates de publication

`get_earnings_dates()` rend un tableau indexé par la date d'annonce, avec
`EPS Estimate`, `Reported EPS` et `Surprise(%)`. **La source plafonne `limit` à
100** et lève `ValueError` au-delà : la constante `LIMITE_ANNONCES = 100` est ce
plafond, et l'échec de cet appel est signalé sur `stderr` plutôt qu'avalé — sans
quoi toutes les dates basculeraient silencieusement sur le repli du § 3. Le script ne garde que les
lignes dont `Reported EPS` est renseigné — les autres sont des **annonces à
venir**, et les utiliser serait le regard en avant sous sa forme la plus directe.

> ⚠️ **La couverture est très inégale d'un ticker à l'autre.** Sur les trois
> valeurs testées : AIR.PA **88** publications depuis 2004, BNP.PA **87** depuis
> 2004, et **MC.PA aucune**. Le script mesure cette couverture pour chaque ticker
> et l'annonce ; il ne la suppose jamais.

### 3. L'appariement exercice → publication

Pour chaque période comptable de date de clôture $t_{\text{exercice}}$ :

1. **Voie normale** — la première date de publication **strictement postérieure**
   à $t_{\text{exercice}}$. Sur AIR.PA, les quatre exercices annuels donnent des
   décalages de **46 à 51 jours**, tous issus de dates réelles :

   | Exercice | Publication | Décalage |
   |---|---|---|
   | 2022-12-31 | 2023-02-16 | 47 j |
   | 2023-12-31 | 2024-02-15 | 46 j |
   | 2024-12-31 | 2025-02-20 | 51 j |
   | 2025-12-31 | 2026-02-18 | 49 j |

2. **Voie de repli** — si aucune date réelle n'existe (couverture absente, ou
   période trop récente), $t_{\text{exercice}} + \texttt{--decalage}$ jours,
   75 par défaut. La colonne `PUBLICATION_ESTIMEE` vaut alors `1`.

**Cette colonne est obligatoire dans toute lecture de la série.** Une ligne à
`PUBLICATION_ESTIMEE = 1` repose sur une convention, pas sur un fait ; mélanger
les deux sans le dire annulerait tout l'intérêt du script.

### 4. Le nombre d'actions

`get_shares_full()` rend une série irrégulière. Le script la **reporte en avant**
(`ffill`) sur le calendrier des séances : à une date donnée, on utilise le
dernier nombre d'actions connu. Les séances **antérieures** au premier point
disponible restent **vides** — pas de report en arrière, qui inventerait une
donnée.

> ⚠️ **Cette série est bruitée.** Sur AIR.PA depuis 2021 elle varie de
> $763$ à $910$ millions de titres, là où la valeur courante est de $791$
> millions : certains points sont manifestement aberrants. Le script **ne les
> corrige pas** — il n'a aucun moyen de distinguer une aberration d'une
> augmentation de capital réelle — mais il affiche le minimum et le maximum dans
> son résumé pour que l'anomalie saute aux yeux.

### 5. Le panel, séance par séance

Pour chaque séance $d$ de la période demandée :

- une séance **sans clôture** — jour en cours, cotation suspendue — est ignorée :
  elle ne produirait qu'une ligne creuse ;
- on retient la période comptable la plus récente dont la publication est $\le d$ ;
  s'il n'y en a aucune, la séance est **ignorée** ;
- `CAPI` $= \text{Close}(d) \times \text{actions}(d)$ ;
- `VE` $= \text{CAPI} + \text{Total Debt} - \text{Cash And Cash Equivalents}$ ;
- les ratios, avec la même règle de dénominateur strictement positif que
  [`import_fondamentaux.py`](import_fondamentaux.md) :

| Colonne | Formule |
|---|---|
| `PER` | `CAPI / Net Income` |
| `P_B` | `CAPI / Stockholders Equity` |
| `VE_EBITDA` | `VE / EBITDA` |
| `REND_FCF` | `100 × Free Cash Flow / CAPI` |
| `ROE` | `100 × Net Income / Stockholders Equity` |
| `MARGE_NETTE` | `100 × Net Income / Total Revenue` |
| `MARGE_OP` | `100 × Operating Income / Total Revenue` |
| `DETTE_EBITDA` | `Total Debt / EBITDA` |

### 6. Colonnes produites

`DATE`, `TICKER`, `CLOTURE`, `ACTIONS`, `CAPI`, `VE`, puis les huit ratios du
§ 5, puis les trois colonnes de **traçabilité** sans lesquelles la série n'est
pas auditable :

| Colonne | Contenu |
|---|---|
| `EXERCICE` | date de clôture de la période utilisée |
| `PUBLICATION` | date à laquelle elle est devenue publique |
| `PUBLICATION_ESTIMEE` | `1` si cette date vient du repli du § 3, `0` si elle est réelle |

Arrondis à l'écriture : 2 décimales pour les ratios et pourcentages, 4 pour la
clôture, 0 pour les montants et les nombres de titres. Valeurs manquantes
écrites **vides**.

### 7. Résumé console

Une ligne par ticker, puis les avertissements :

```
AIR.PA   1 148 séances du 2023-02-16 au 2026-08-28
         4 exercices, 4 publications reelles, 0 estimee
         actions : 763 350 976 -> 910 182 016 (serie bruitee, non corrigee)
         PER median 24,13 · P/B median 5,02
```

### 8. Cas limites

- **Aucune publication trouvée et `--decalage` inutilisable** (pas de comptes du
  tout) : le ticker est ignoré, message sur `stderr`, les autres sont traités.
- **Échec d'un appel à la source** — réseau, ticker sans comptes, réponse
  illisible : **chacun des cinq appels du § 1 signale son échec sur `stderr`**,
  en nommant l'appel et le type d'erreur. Aucun n'est avalé en silence : sans
  cela, une panne réseau se confondrait avec une absence de donnée, et la
  série basculerait sur le repli du § 3 sans que rien ne l'indique.
- **Ticker sans comptes** (indice, ETF) : ignoré de la même façon.
- **Bénéfice, fonds propres ou EBITDA négatifs** : le ratio correspondant reste
  vide, comme dans `import_fondamentaux.py`. Un PER négatif ne se compare à rien.
- **Séances antérieures à la première publication** : ignorées, la série commence
  à la première date où quelque chose était connu.
- **Période comptable entièrement vide** : écartée (§ 1), et la série démarre donc
  à la première publication réellement exploitable.
- **Séance sans clôture** : ignorée (§ 5).
- **`--trimestriel`** donne des ratios plus réactifs mais une profondeur de
  6 trimestres seulement, soit un an et demi.

### 9. Résultat sur trois valeurs du CAC 40

```bash
python python/reconstituer_fondamentaux.py AIR.PA BNP.PA MC.PA
```

| | Lignes | Période | Publications réelles | Estimées |
|---|---|---|---|---|
| AIR.PA | 900 | 2023-02-16 → 2026-08-27 | **4** | 0 |
| BNP.PA | 907 | 2023-02-07 → 2026-08-27 | **4** | 0 |
| MC.PA | 880 | 2023-03-16 → 2026-08-27 | **0** | **4** |

Aucune cellule vide sur AIR.PA et MC.PA. Sur BNP.PA, `VE_EBITDA` est vide sur les
907 lignes — **c'est le résultat attendu** : une banque n'a ni valeur
d'entreprise ni EBITDA
([fondamentaux, module 3 § 3.5](../docs/raw/concept/semestre4/fondamentaux/03-ce-que-la-comptabilite-laisse-au-choix.md)).

Le basculement se lit sur la série. Autour de la publication du 20 février 2025 :

| Séance | PER | Exercice utilisé |
|---|---|---|
| 2025-02-19 | 33,76 | 2023-12-31 |
| **2025-02-20** | **30,25** | **2024-12-31** |

La discontinuité tombe **le jour de la publication**, pas le jour de la clôture
de l'exercice. C'est la signature d'une série *point-in-time* correcte.

> ⚠️ **Le PER de ce script et celui d'[`import_fondamentaux.py`](import_fondamentaux.md)
> ne coïncident pas, et c'est normal.** Au 27 août 2026 : **30,83** ici contre
> **27,04** là. Les dénominateurs diffèrent — le résultat du dernier **exercice
> annuel** publié d'un côté, le bénéfice des **douze mois glissants** (trimestres
> compris) de l'autre. Aucune des deux valeurs n'est fausse ; les comparer
> revient à comparer deux définitions. Avec `--trimestriel`, l'écart se réduit
> sans disparaître.

### 10. Ce que vaut le contenu, poste par poste

Réserve vérifiable, donc vérifiée. Le communiqué de résultats d'Airbus du
**20 février 2025** — le document d'origine, archivé par `bnains.org` — confronté
à ce que la source sert aujourd'hui pour le même exercice 2024 :

| Poste | Publié | Servi aujourd'hui | Écart |
|---|---|---|---|
| Chiffre d'affaires | 69 230 M | 69 230 M | **0,00 %** |
| Résultat net | 4 232 M | 4 232 M | **0,00 %** |
| BPA | 5,36 | 5,36 | **0,00 %** |
| **EBIT** | **5 304 M** | **6 325 M** | **19,3 %** |
| **Flux de trésorerie disponible** | **4 461 M** | **3 733 M** | **16,3 %** |

> 🔑 **Deux causes distinctes, qu'il ne faut pas confondre.** Le *retraitement*
> vient de l'entreprise, qui corrige un exercice clos ; la *normalisation* vient
> du fournisseur, qui recalcule un agrégat à sa façon. Ici, rien n'indique un
> retraitement — chiffre d'affaires, résultat net et BPA tombent au centime. En
> revanche l'`EBIT` servi ne vaut ni l'EBIT publié (5 304) ni l'EBIT ajusté
> (5 354), et l'`Operating Income` (4 804) non plus : **c'est une définition
> différente**, pas une histoire réécrite.

Conséquence pratique, et c'est elle qu'il faut retenir :

| Ratios | Dénominateur | Confiance |
|---|---|---|
| `PER`, `MARGE_NETTE`, `P_B` | résultat net, chiffre d'affaires, fonds propres | ✅ le chiffre servi est celui qui fut publié |
| `VE_EBITDA`, `DETTE_EBITDA`, `REND_FCF` | EBITDA, FCF | ⚠️ **le chiffre servi n'est pas celui que le marché a lu** |

⚠️ **Portée de ce contrôle : une société, un exercice, cinq postes.** Il établit
que le problème existe et qu'il est inégal selon le poste ; il n'établit pas de
taux d'erreur général. Refaire la mesure sur une autre valeur avant de
généraliser.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Au moins un ticker reconstitué, CSV écrit. |
| `1` | Aucun ticker fourni, ou aucun ticker exploitable. |

## Fonctions internes

- `comptes(ticker, trimestriel)` — les trois états financiers, en un dictionnaire
  `{date de clôture: {poste: valeur}}`.
- `publications(ticker)` — les dates d'annonce passées, celles dont l'EPS est
  publié.
- `apparier(periodes, dates_publication, decalage)` — le § 3 ; rend pour chaque
  période sa date de publication et si elle est estimée.
- `serie_actions(ticker, calendrier)` — `get_shares_full()` reporté en avant.
- `reconstituer(ticker, ...)` — assemble le panel du § 5.
- `main()` — CLI, boucle sur les tickers, écriture, résumé.

## Constantes

- `REPERTOIRE_DEFAUT = Path("docs/raw/fondamentaux")`.
- `DECALAGE_DEFAUT = 75` — jours, repli du § 3.
- `LIMITE_ANNONCES = 100` — plafond imposé par la source à `get_earnings_dates`.
- `POSTES` — la correspondance entre colonnes produites et libellés de lignes
  yfinance, source de vérité unique.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
