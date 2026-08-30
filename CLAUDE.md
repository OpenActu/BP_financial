# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Langue

Répondre à l'utilisateur en français. Cela s'applique à tous les échanges
(explications, résumés, questions, messages de commit) dans ce dépôt. Les
messages console et l'aide des CLI sont également en français — garder cette
convention dans toute modification.

## Ce qu'est ce dépôt

Deux choses, également importantes :

1. **Neuf utilitaires Python en ligne de commande** qui récupèrent et analysent
   des données de la Bourse de Paris. Pas de paquet, pas de tests, pas de
   `__init__.py` — chaque script se lance depuis la racine du dépôt.
2. **Un cours en quatre semestres**, dans `docs/raw/concept/`, qui démontre tout
   ce que les scripts calculent. Le parcours est décrit par
   [`docs/raw/planning.md`](docs/raw/planning.md).

Les tickers de Paris portent le suffixe `.PA` (`AIR.PA`, `MC.PA`) ; les indices
un `^` initial (`^FCHI`), qui **exige des guillemets** en ligne de commande.

## Règle : miroir Markdown des scripts Python

Tout fichier `.py` doit être accompagné d'un fichier `.md` **du même nom**, placé
à côté de lui (ex. `python/import_societe.py` ⇔ `python/import_societe.md`).

Ce markdown est le **miroir de l'exécution** du script : il décrit, dans l'ordre
du déroulement, ce que le script fait réellement — arguments CLI et valeurs par
défaut, étapes de traitement, formules exactes, colonnes produites, affichage
console, fichiers écrits, codes de sortie, cas limites. Il décrit le
comportement, pas le code.

Le markdown fait autorité : lorsqu'une évolution demande un arbitrage (nom d'une
colonne ou d'un argument, valeur par défaut, gestion des `NaN`, format de sortie,
comportement en cas d'erreur…), **mettre le markdown à jour d'abord**, puis
aligner le script dessus. Jamais l'inverse.

La skill `/python-sync` détecte les markdown modifiés et répercute les
changements dans les scripts correspondants.

## Les neuf scripts

| Script | Ce qu'il produit |
|---|---|
| `import_societe.py` | OHLCV + indicateurs glissants + test de tendance → `docs/raw/quotes/` |
| `import_fondamentaux.py` | ratios **du jour** + limite 1 du carnet ; `--archiver` empile dans `archive.csv` |
| `reconstituer_fondamentaux.py` | ratios **point-in-time** sur 3 à 4 ans, chaque exercice daté par sa publication |
| `import_dividendes.py` | dividendes et divisions depuis `bnains.org`, confrontés à yfinance |
| `generer_graph_supp_resistance.py` | SVG : encadrement support/résistance sur les **clôtures** |
| `generer_graph_decision.py` | SVG : encadrement sur **High/Low**, cinq critères et verdict |
| `couts_transaction.py` | coût d'exécution d'une règle, et l'alpha qu'il faudrait pour le couvrir |
| `evaluer_portefeuille.py` | alpha d'un **panier** contre son indice, coûts et biais d'indice nu compris |
| `construire_indice_total.py` | un indice de référence **en rendement total**, à partir de composants déclarés |

**Lire le miroir avant de modifier un script.** Il contient les formules, les
conventions et les pièges déjà rencontrés.

## Invariants, valables partout

- **`yfinance` est la seule dépendance externe** (`pandas` arrive avec lui).
  **Ne pas ajouter `scipy`** — la loi de Student est réimplémentée en Python pur
  dans `import_societe.py` (`p_valeur_student`), à réutiliser plutôt qu'à
  redoubler. Ni `matplotlib` (les SVG sont écrits à la main), ni `requests`
  (`urllib` suffit), ni `beautifulsoup4`.
- **Une cellule vide plutôt qu'un nombre inventé.** Quand ni la valeur ni ses
  composants ne sont disponibles, la colonne reste vide — jamais `nan`, `None`
  ou `0`. Une cellule vide est une information.
- **Un dénominateur nul ou négatif ne produit pas de ratio.** Un multiple
  d'EBITDA négatif ne se compare à rien.
- **Jamais de regard en avant.** Aucune quantité datée du jour `d` ne peut
  dépendre d'une séance postérieure, échelles de graphique comprises.
- ⚠️ **`Close` est ajustée des dividendes, `^FCHI` ne l'est pas.** Comparer les
  deux fabrique de l'alpha à partir de rien : **7,9 points par an** mesurés sur
  24 ans. La sortie propre est `construire_indice_total.py`, qui fabrique un
  indice de même convention. Le signaler en note de bas de page ne suffit pas,
  ce biais renverse les verdicts.
- **Une convention ne se devine pas depuis des nombres.** Un indice nu et un
  indice en rendement total sont deux séries de niveaux, formellement
  indiscernables. Quand une convention change un résultat, la faire **déclarer**
  plutôt que tenter de la détecter.
- **Fins de ligne : `.gitattributes` s'en charge, ne rien convertir à la main.**
  La règle est **LF partout**, sauf deux exceptions imposées par leurs
  producteurs : les `.csv` (`csv.writer` émet du CRLF, RFC 4180, Excel) et les
  `.svg` (les générateurs les écrivent ainsi sous Windows). Écrire un fichier
  sans se soucier de ses fins de ligne est donc désormais sans conséquence — et
  un script qui en convertirait d'autorité produirait des diffs de centaines de
  lignes pour zéro changement de contenu.

### Lint

```bash
pip install ruff
python -m ruff check python/     # doit sortir « All checks passed! »
```

`ruff.toml` fige le jeu de règles à la racine. **L'objectif est zéro
signalement**, et il est tenu : un lint qui rend toujours onze lignes n'est plus
un signal, c'est un bruit de fond qu'on cesse de lire — et c'est ainsi qu'on
manque le douzième.

Les exemptions sont de deux natures, à ne jamais mélanger :

- une règle **contraire à une convention du dépôt** est écartée dans
  `ruff.toml`, motif à l'appui — `DTZ011` parce qu'on travaille en dates
  calendaires locales, `RUF001` parce que la typographie française utilise
  délibérément espaces insécables et tirets demi-cadratins ;
- un **cas particulier justifié** porte un `# noqa: RÈGLE` sur sa ligne, avec sa
  raison. Les six `except Exception` autour des appels réseau sont dans ce cas.

Conséquence à respecter : **ne pas ajouter d'exemption globale pour faire taire
un cas isolé.** Un nouveau `except` aveugle doit rester visible — c'est ce
mécanisme qui a fait trouver quatre gestionnaires qui avalaient l'erreur en
silence dans `reconstituer_fondamentaux.py`.

`ruff format` **n'est pas** appliqué : il reformaterait les six scripts d'un
coup, pour un gain nul.

### Ce qui est suivi par git, et ce qui ne l'est pas

`docs/raw/quotes/`, `docs/raw/graphs/`, les CSV du jour de `docs/raw/fondamentaux/`
et le cache HTML de `docs/raw/dividendes/` sont **exclus** : ils se régénèrent
d'un appel.

> ⚠️ **`docs/raw/fondamentaux/archive.csv` est la seule donnée du dépôt qui ne se
> régénère pas.** Le `.gitignore` l'excepte explicitement. Ne jamais l'écraser :
> le script n'y ajoute que des lignes, et refuse les doublons `(TICKER, DATE)`.

## Les cours

```
docs/raw/planning.md              le parcours, quatre semestres
docs/raw/modele.md                l'énoncé de la démonstration centrale
docs/raw/concept/
├── semestre1/  algèbre · dérivation-intégration · convexité
├── semestre2/  statistique mathématique
├── semestre3/  loi de Student · modèle · canal · encadrement
├── semestre4/  alpha · fondamentaux · trading · finance
└── sommaire/   les index, hors parcours
```

Un répertoire contient **soit** des sous-répertoires, **soit** des fichiers.
Les liens entre cours sont **relatifs** ; après tout déplacement, vérifier qu'ils
résolvent tous.

## Agents

- `chartiste` (`.claude/agents/chartiste.md`) — lit la tendance d'une valeur à
  partir d'un CSV de `docs/raw/quotes/` : droite ajustée, canal de régression,
  encadrement par enveloppe convexe, test de significativité, ruptures.
- `trading` (`.claude/agents/trading.md`) — performance, alpha et bêta contre un
  indice de référence, techniques de sélection et ce qui est calculable ici,
  verdict achat/vente/attente issu d'une règle **écrite à l'avance**.
- `sorosien` (`.claude/agents/sorosien.md`) — lecture réflexive au sens de Soros :
  canal de transmission entre cours et fondamentaux, phase du cycle boom-bust, et
  « aucune séquence réflexive identifiable » par défaut.

**Aucun des trois ne donne de conseil en investissement**, ne dimensionne une
position ni ne prédit un cours. Cette limite est structurante : ne pas la relâcher
sans demande explicite.

## Setup & run

```bash
pip install yfinance

python python/import_societe.py AIR.PA --periode 5y
python python/import_societe.py AIR.PA --debut 2023-01-01 --fin 2024-01-01
python python/import_fondamentaux.py AIR.PA MC.PA --archiver
python python/reconstituer_fondamentaux.py AIR.PA --mensuel
python python/import_dividendes.py --index
```

> ⚠️ **`--fin` est exclusif** : `--fin 2023-12-31` s'arrête à la séance du 30.

Sans argument, chaque script bascule dans une invite interactive.

## Ce que produit `import_societe.py`

Le cœur du dépôt. À l'OHLCV il ajoute un compteur `INDICE` (1, 2, …) puis, pour
chaque fenêtre glissante `n` ∈ {20, 120} sur `Close` : `E_n` (moyenne), `VAR_n`
(variance de population, `ddof=0`), `CORR_n` (corrélation avec `INDICE`), `VAL_n`
(la droite des moindres carrés évaluée au dernier point de la fenêtre), et le test
de Student bilatéral — `T_n`, `P_n` et le verdict signé `TEND_n` au seuil
`--alpha` (0,05 par défaut). Les `n-1` premières lignes restent vides.

Les formules, leur démonstration et tous les cas limites sont dans
[`python/import_societe.md`](python/import_societe.md) et
[`docs/raw/modele.md`](docs/raw/modele.md).
