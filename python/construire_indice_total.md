# construire_indice_total.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `construire_indice_total.py`, étape
par étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du
script doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Construire un indice de référence **en rendement total**, pour comparer un
portefeuille à quelque chose de la même nature que lui.

Le problème qu'il résout est chiffré : `Close` est ajustée des dividendes,
`^FCHI` est un indice **nu**, et l'écart vaut **6,22 points d'alpha par an** sur
24 ans. Faute d'indice comparable,
[`evaluer_portefeuille.py`](evaluer_portefeuille.md) devait sur-corriger en
retranchant tout le rendement du dividende du panier — une borne basse, honnête
mais grossière.

> 🔑 **Les deux séries doivent être de même convention.** Un panier construit sur
> des cours ajustés se compare à un indice construit sur des cours ajustés. Tout
> le reste est de la comptabilité de conventions déguisée en performance.

`^FCHIGR`, la version rendement total du CAC 40, n'est pas servie par yfinance.
Le script en fabrique donc un substitut à partir des composants.

## Ce que le résultat n'est pas

> ⚠️ **Ce n'est pas le CAC 40.** C'est un panier de valeurs **déclarées**,
> pondéré selon une règle **déclarée**. Trois différences irréductibles :
>
> - **la composition** : l'univers est fourni par l'utilisateur, pas par
>   Euronext, et il est constitué **aujourd'hui** — le biais du survivant est
>   entier ;
> - **la pondération** : équipondérée par défaut, quand le CAC 40 est pondéré par
>   les capitalisations flottantes, plafonnées à 15 % ;
> - **le nombre de valeurs** : dix ou vingt ne se comportent pas comme quarante.
>
> Le script nomme donc sa sortie `TR{N}` — *total return, N valeurs* — et jamais
> « CAC 40 ». L'écart qu'il mesure contre `^FCHI` (§ 4) **n'est pas le rendement
> du dividende de l'indice** : c'est l'effet cumulé des dividendes, de la
> composition et de la pondération. Le lire comme un rendement de dividende
> serait une erreur.

## Dépendances

- `yfinance` uniquement si `--telecharger` ; sinon aucun réseau.
- Modules standard : `argparse`, `csv`, `math`, `statistics`, `sys`, `pathlib`.

## Invocation

```bash
python python/construire_indice_total.py AIR.PA OR.PA MC.PA SAN.PA TTE.PA
python python/construire_indice_total.py --fichier univers.txt --debut 2001-09-04
python python/construire_indice_total.py AIR.PA OR.PA --ponderation capi --telecharger
```

Puis, sans rien changer à l'évaluateur :

```bash
python python/evaluer_portefeuille.py AIR.PA OR.PA MC.PA --indice TR10
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `tickers` | — | L'univers de référence. Sans argument ni `--fichier`, invite interactive. |
| `--fichier` | — | Fichier texte, un ticker par ligne (`#` = commentaire). |
| `--debut`, `--fin` | l'intersection disponible | Bornes `AAAA-MM-JJ`. |
| `--ponderation` | `egale` | `egale` ou `capi` (§ 2). |
| `--rebalancement` | `annuel` | `mensuel`, `trimestriel`, `annuel` ou `aucun`. |
| `--nom` | `TR{N}` | Nom de l'indice produit. |
| `--comparer` | `^FCHI` | Indice nu contre lequel mesurer l'écart (§ 4). Vide pour l'omettre. |
| `--telecharger` | — | Récupère les séries manquantes. |

## Déroulé d'exécution

### 1. Les séries et leur alignement

Mêmes règles que
[`evaluer_portefeuille.py`](evaluer_portefeuille.md) § 1 : lecture depuis
`docs/raw/quotes/`, **contrôle de couverture** de la période demandée, et
alignement sur les dates communes. Une valeur dont le CSV est trop court est
traitée comme manquante, avec la commande à lancer.

Le script exige au moins **deux valeurs** et **250 séances** communes : en deçà,
l'objet produit ne mérite pas le nom d'indice. Sortie **1**.

### 2. La pondération

- **`egale`** — chaque valeur pèse $1/N$ à chaque rebalancement. Simple, sans
  donnée supplémentaire, et c'est la convention qui se compare le mieux à un
  portefeuille équipondéré.
- **`capi`** — poids proportionnels à `marketCap`, lu **une fois** au moment de
  l'appel.

> ⚠️ **`capi` utilise la capitalisation d'aujourd'hui pour pondérer tout le
> passé.** C'est un **regard en avant caractérisé** : les valeurs qui ont réussi
> pèsent lourd dès la première séance. L'option existe parce qu'on la demande,
> le script l'accompagne d'un avertissement à chaque exécution, et
> **`egale` reste le défaut**. Une pondération correcte exigerait l'historique
> des capitalisations, que le dépôt n'a pas.

### 3. La série

Rendements arithmétiques quotidiens sur `Close` — déjà ajustée des dividendes,
donc **rendement total par construction**. Les poids dérivent entre
rebalancements exactement comme au § 2 de l'évaluateur, et sont ramenés à leur
cible aux dates de rebalancement.

L'indice démarre à **1000** et vaut $I_t = I_{t-1}(1 + r_{p,t})$.

Aucun coût n'est appliqué : un indice de référence n'en supporte pas. C'est une
différence assumée avec un portefeuille réel, et elle joue **contre** le
portefeuille.

### 4. L'écart avec l'indice nu

Le script mesure, sur les mêmes dates, la performance annualisée des deux séries
et publie leur écart. Sur les dix valeurs du fil rouge, 2001-2025 :

| | CAGR |
|---|---|
| `TR10`, rendement total | mesuré à l'exécution |
| `^FCHI`, nu | mesuré à l'exécution |
| **écart** | l'ordre de grandeur des **6,2 points/an** constatés par l'évaluateur |

Rappel du § *Ce que le résultat n'est pas* : cet écart **mélange** dividendes,
composition et pondération. Il ne s'interprète pas comme un rendement de
dividende.

### 5. Écriture

Un CSV dans `docs/raw/quotes/{nom}_{debut}_{fin}.csv`, colonnes `Date` et
`Close`, afin que
[`evaluer_portefeuille.py`](evaluer_portefeuille.md) et
[`import_societe.py`](import_societe.md) le lisent sans modification. Le
répertoire est exclu du suivi git : l'indice se régénère d'un appel.

Une colonne `Dividends` valant `0` est écrite, pour que l'évaluateur ne compte
pas de rendement de dividende sur un indice qui l'intègre déjà — sans quoi la
correction prudente du § 4bis s'appliquerait deux fois.

### 6. Résumé console

```
Indice TR10 · 10 valeurs · ponderation egale · rebalancement annuel
  6136 seances du 2001-09-04 au 2025-12-31
  base 1000 -> valeur finale mesuree a l'execution

  TR10   (rendement total)  CAGR mesure a l'execution
  ^FCHI  (nu)               CAGR mesure a l'execution
  ecart                     dividendes + composition + ponderation

  Ecrit dans : docs/raw/quotes/TR10_2001-09-04_2025-12-31.csv
```

### 7. Cas limites

- **Moins de deux valeurs ou moins de 250 séances** : sortie **1**.
- **Série manquante ou trop courte** : sortie **1**, avec la commande à lancer.
- **`--ponderation capi` avec une capitalisation absente** : la valeur est
  écartée de l'univers et le script le dit ; si moins de deux subsistent,
  sortie **1**.
- **`--comparer` vide ou introuvable** : le § 4 est omis, l'indice est produit
  quand même.
- **`--rebalancement aucun`** : achat initial puis dérive libre. L'indice cesse
  d'être équipondéré, et c'est dit.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Indice construit et écrit. |
| `1` | Univers insuffisant, série manquante, ou moins de 250 séances communes. |

## Fonctions internes

- `poids_initiaux(tickers, ponderation)` — le § 2, avec l'avertissement de
  regard en avant pour `capi`.
- `construire(dates, rendements, tickers, poids_cible, declencheur)` — le § 3.
- `cagr(serie)` — performance annualisée, pour le § 4.
- `main()` — CLI, construction, comparaison, écriture.

## Constantes

- `BASE = 1000.0` — valeur initiale de l'indice.
- `SEANCES_MINIMALES = 250`, `VALEURS_MINIMALES = 2`.
- `REPERTOIRE_QUOTES = Path("docs/raw/quotes")`.
- `JOURS_AN = 252`.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
