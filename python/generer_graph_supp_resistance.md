# generer_graph_supp_resistance.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `generer_graph_supp_resistance.py`,
étape par étape, dans l'ordre du déroulement. Il fait autorité : toute évolution
du script doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Tracer un cours de bourse et son encadrement par droites de support et de
résistance, dans un fichier **SVG**. Les droites sont construites par enveloppe
convexe selon la méthode du cours
[`docs/raw/concept/encadrement/`](../docs/raw/concept/encadrement/README.md).

> **La seule donnée utilisée est la clôture** (`Close`). Ni `High`, ni `Low`, ni
> `Open`, ni `Volume`. Le cours d'encadrement, lui, construit ses chaînes sur les
> extrêmes de séance ; les droites produites ici sont donc **différentes** des
> siennes, et systématiquement plus resserrées. Voir § 8.

## Dépendances

- `pandas` (installé avec `yfinance`) pour la lecture du CSV.
- Modules standard : `argparse`, `sys`, `pathlib`, `statistics`.
- **Aucune bibliothèque de tracé.** Le SVG est écrit à la main : `matplotlib`
  n'est pas installé et n'est pas une dépendance de ce dépôt.

## Invocation

```bash
python python/generer_graph_supp_resistance.py
python python/generer_graph_supp_resistance.py --csv docs/raw/quotes/AIR_PA_2020-01-02_2023-12-29.csv
python python/generer_graph_supp_resistance.py --bloc 60 --fenetre 60
python python/generer_graph_supp_resistance.py --sans-blocs --sortie /tmp/airbus.svg
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `--csv` | le fichier le plus récent de `docs/raw/quotes/` | Chemin du CSV d'entrée. Doit contenir les colonnes `Date` et `Close`. |
| `--bloc` | `120` | Longueur des blocs de segmentation, en séances (§ 4). |
| `--fenetre` | `120` | Longueur de la fenêtre active, ancrée à droite (§ 5). |
| `--tolerance` | `0.25` | Tolérance de contact, en multiples de $\sigma_{\text{Close}}$ de la fenêtre (§ 3). |
| `--sans-blocs` | — | Ne trace que le canal actif, sans les droites par bloc. |
| `--sortie` | `docs/raw/graphs/{nom_du_csv}_supp_resistance.svg` | Chemin du SVG produit (répertoire créé si besoin). |
| `--titre` | le ticker, dérivé du nom du CSV | Titre inscrit dans le SVG. Par défaut, la partie du nom de fichier précédant la première date, `_` remplacé par `.` : `AIR_PA_2020-01-02_2023-12-29.csv` donne `AIR.PA`. |

## Déroulé d'exécution

### 1. Lecture des arguments et du CSV

`argparse` analyse la ligne de commande. Sans `--csv`, le script prend le fichier
`*.csv` le plus récemment modifié de `docs/raw/quotes/` ; s'il n'y en a aucun :
message `Aucun CSV dans docs/raw/quotes/.` sur `stderr` et **sortie 1**.

Le CSV est lu avec `pandas`, seules les colonnes `Date` et `Close` sont
conservées. Les dates sont tronquées au jour (`AAAA-MM-JJ`), le fuseau horaire de
l'horodatage est ignoré : ce sont des rangs de séance qui comptent, pas des
instants.

Si `Close` est absente, ou si le fichier compte moins de `--bloc` lignes :
message d'erreur sur `stderr` et **sortie 1**.

Les instants sont les **rangs de séance** $T_i = i$, $i = 0,\dots,n-1$ dans le
code (l'indexation à 1 du modèle est une convention d'exposé, sans effet sur les
pentes).

### 2. Les deux chaînes — `chaine(points, inferieure)`

Balayage de Andrew sur les points $(i, \texttt{Close}_i)$, en $O(n\log n)$ :

- `inferieure=True` → **chaîne inférieure**, d'où sortent les droites de
  **support** ;
- `inferieure=False` → **chaîne supérieure**, d'où sortent les droites de
  **résistance**.

Chaque arête de chaîne est une droite qui touche exactement deux clôtures sans en
traverser aucune ([module 1](../docs/raw/concept/encadrement/01-la-droite-qui-ne-coupe-rien.md)).

### 3. L'arête retenue et les épisodes de contact

- **Portée minimale** — `arete_retenue(chaine, portee_min)` parcourt la chaîne de
  droite à gauche et rend la **dernière arête dont la portée atteint
  `portee_min`**, fixée à `len(fenêtre) // 4`. Si aucune ne l'atteint, elle rend
  la corde joignant les deux extrémités de la chaîne.
- **Tolérance** — $\varepsilon = \texttt{tolerance} \times \sigma_{\texttt{Close}}$,
  l'écart-type étant celui de la **fenêtre considérée**, pas de l'historique
  entier.
- **Épisodes** — `episodes(indices, ecart=3)` regroupe les séances de contact
  distantes de moins de 3 séances. Le nombre d'épisodes est le nombre de
  contacts ; le nombre de jours ne l'est pas
  ([module 2](../docs/raw/concept/encadrement/02-portee-et-episodes-de-contact.md)).

### 4. Segmentation en blocs

Blocs consécutifs de `--bloc` séances depuis le début de l'historique. Si le
dernier bloc compte moins de 40 séances, il est **fusionné** avec le précédent.
Chaque bloc reçoit sa propre arête retenue, sa propre tolérance et ses propres
épisodes.

Ces droites ne sont jamais tracées hors de leur bloc : une droite d'encadrement
n'existe pas hors de la fenêtre qui l'a produite.

**Étendue de tracé.** Chaque droite est tracée de son **ancre** — le premier des
deux points de l'arête retenue — jusqu'à la **fin de sa fenêtre**, et non sur la
fenêtre entière. La raison est de lisibilité, et elle est importante : l'arête
retenue peut n'enjamber qu'une fraction de la fenêtre, et son prolongement vers
la gauche, quoique valide comme borne, s'éloigne alors très loin du cours. Sur
Airbus, le support actif est ancré au 2023-10-20 et n'enjambe que 48 des 120
séances ; extrapolé jusqu'au 2023-07-13 il passerait à $pprox 89$ € sous un
cours à 128 €. Le segment tracé va donc du 2023-10-20 au 2023-12-29.

### 5. Le canal actif

Recalcul sur les `--fenetre` **dernières** séances, indépendamment de la
partition en blocs — le dernier bloc n'est pas le canal courant, sa découpe étant
un artefact du point de départ
([module 3](../docs/raw/concept/encadrement/03-segmenter-un-historique-long.md)).

Le canal actif est tracé en trait plein plus épais, de l'ancre de chaque droite
à la dernière séance, selon la même règle d'étendue qu'au § 4.

### 6. Écriture du SVG

Un seul fichier, autonome, sans police externe ni script :

- fond clair, grille horizontale tous les 20 €, repères verticaux aux changements
  d'année ;
- **cours** en bleu `#2a78d6`, trait de 1,4 px, sur tout l'historique ;
- **résistances** en orange `#eb6834`, **supports** en vert `#1baf7a` ;
  les droites de bloc en trait fin pointillé, celles du canal actif en trait plein
  de 2 px ;
- points de contact du canal actif marqués par un cercle ;
- étiquettes de valeur au bord droit pour le canal actif ;
- cartouche récapitulatif en haut à gauche (fenêtre, pentes, portées, épisodes) ;
- légende en bas.

Dimensions par défaut : `1200 × 620` unités de `viewBox`, redimensionnable sans
perte.

### 7. Résumé console

```
{titre} — {n} séances, du {première date} au {dernière date}
Blocs : {k} de {bloc} séances (portée minimale {pm})

CANAL ACTIF — {date début} → {date fin} ({fenetre} séances, ε = {eps} €)
  résistance  pente {p} €/séance  portée {q}  épisodes {r}  → {valeur} €
  support     pente {p} €/séance  portée {q}  épisodes {r}  → {valeur} €
  clôture {c} €  |  position dans le canal {x} %  |  largeur {l} € ({m} %)

Graphique écrit dans : {chemin}
```

Le script vérifie et affiche le **contrôle de non-traversée** : le nombre de
clôtures situées du mauvais côté de chaque droite retenue, qui doit être `0`.
S'il ne l'est pas, message sur `stderr` et **sortie 2** — c'est un bogue de
l'enveloppe convexe, pas une propriété des données.

### 8. Ce que change l'usage des clôtures seules

Le cours d'encadrement construit ses chaînes sur `High` et `Low`. Ici, sur
`Close`. Trois conséquences, à connaître avant de lire le graphique :

- **Le canal est plus étroit.** Les clôtures sont à l'intérieur de l'enveloppe
  haut/bas de chaque séance. Sur la fenêtre active d'Airbus, le canal mesure
  $3{,}39$ € contre $5{,}76$ € pour la version haut/bas — $2{,}6\,\%$ du cours au
  lieu de $4{,}4\,\%$.
- **Les mèches sont ignorées.** Un plus-haut de séance non confirmé en clôture ne
  crée aucune résistance. C'est un choix défendable — la clôture est le prix de
  référence — mais c'est un choix, pas une simplification neutre.
- ⚠️ **La dernière clôture est toujours un sommet des deux chaînes.** Le point le
  plus à droite d'un nuage appartient par construction à l'enveloppe convexe.
  Quand la règle de portée retient l'arête qui s'appuie dessus, la droite passe
  **exactement** par la dernière clôture, et l'écart affiché vaut zéro. C'est le
  cas sur Airbus au 29 décembre 2023 : support $= 131{,}93$ € $=$ clôture. Cette
  coïncidence est **géométrique, pas informative** — elle ne dit pas que le cours
  « tient son support ». Le script le signale explicitement dans son résumé quand
  l'écart à une borne est inférieur à $\varepsilon/10$.

### 9. Résultat sur AIR.PA, 2020-2023

Fenêtre active de 120 séances, du 2023-07-13 au 2023-12-29, $\varepsilon = 1{,}21$ € :

| | Ancre | Pente | Portée | Épisodes | Valeur au 2023-12-29 |
|---|---|---|---|---|---|
| Résistance | 2023-07-24, 128,70 € | $+0{,}0591$ €/séance | 101 | 2 | 135,32 € |
| Clôture | — | — | — | — | **131,93 €** |
| Support | 2023-10-20, 114,45 € | $+0{,}3642$ €/séance | 48 | 3 | 131,93 € |

Largeur $3{,}39$ € soit $2{,}6\,\%$ ; contrôle de non-traversée : 0 des deux côtés.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète, SVG écrit. |
| `1` | CSV introuvable, colonne `Close` absente, ou historique plus court que `--bloc`. |
| `2` | Contrôle de non-traversée en échec — bogue de l'enveloppe convexe. |

## Fonctions internes

- `chaine(points, inferieure)` — chaîne inférieure ou supérieure de l'enveloppe
  convexe, balayage de Andrew.
- `arete_retenue(chaine, portee_min)` — dernière arête de portée suffisante.
- `episodes(indices, ecart)` — regroupement des séances de contact en contacts.
- `analyser(closes, a, b, tolerance)` — assemble les trois précédentes sur la
  tranche `[a, b[` et rend un dictionnaire décrivant les deux droites.
- `svg(...)` — assemblage du fichier, sans dépendance.

## Constantes

- `REPERTOIRE_QUOTES = Path("docs/raw/quotes")` — source par défaut.
- `REPERTOIRE_GRAPHS = Path("docs/raw/graphs")` — destination par défaut, exclue
  du suivi git : un SVG est une sortie régénérable, pas une source.
- `ECART_EPISODE = 3` — séances séparant deux épisodes de contact.
- `BLOC_MINIMAL = 40` — en deçà, le dernier bloc est fusionné avec le précédent.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
