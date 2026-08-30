# dimensionner_exposition.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `dimensionner_exposition.py`, étape
par étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du
script doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Dimensionner une exposition — levier et couverture confondus — **sans jamais
supposer un rendement espéré**.

Le [cours finance](../docs/raw/concept/semestre4/finance/04-levier-optimal-et-drag.md)
donne le levier optimal $L^\star = (\mu - c)/\sigma^2$, et le
[cours alpha](../docs/raw/concept/semestre4/alpha/03-l-horizon-necessaire.md)
démontre que $\mu$ n'est pas mesurable à horizon humain : avec
$\sigma = 19\,\%$/an, estimer $\mu$ à $\pm 1$ point demande **359 ans**. Un script
qui demanderait $\mu$ en entrée produirait donc un levier entièrement déterminé
par une valeur inventée.

Celui-ci prend acte et **retourne la question** :

> 🔑 **Il ne suppose pas $\mu$ pour en déduire un levier ; il publie, pour chaque
> levier, le $\mu$ qu'il faudrait pour le justifier**, et le confronte à
> l'intervalle de confiance du $\mu$ mesuré sur la série.

C'est l'inversion de [`couts_transaction.py`](couts_transaction.md), qui ne
prétend pas connaître l'alpha d'une règle mais dit quel alpha serait nécessaire
pour couvrir ses frais.

Tout le reste — barrière d'appel de marge, drag de volatilité, coût de portage,
frais de rotation — ne dépend que de $\sigma$, qui **est** mesurable, et se
calcule sans hypothèse.

## Ce que le script ne fait pas

> ⚠️ **Il ne recommande aucun levier, et n'en désigne aucun comme optimal.** Il
> rend trois choses : ce qui est **admissible** (barrière), ce qui est **certain**
> (coûts et drag), et ce qui serait **nécessaire** (le $\mu$ de seuil). Le
> rapprochement des trois est un dimensionnement, pas un conseil.

Hors champ, explicitement : fiscalité et enveloppe, choix de l'instrument,
qualité de la réplication, risque de contrepartie, et toute prévision de cours.

## Dépendances

- `pandas` (installé avec `yfinance`) pour la lecture des CSV.
- Modules standard : `argparse`, `csv`, `math`, `statistics`, `sys`, `pathlib`.
- **Aucun réseau** : le script ne télécharge rien et n'importe pas `yfinance`.
- **Pas de `scipy`** : $\Phi$ est obtenue par `math.erf`.

## Invocation

```bash
python python/dimensionner_exposition.py
python python/dimensionner_exposition.py --csv 'docs/raw/data/quotes/^FCHI_2019-01-02_2025-12-31.csv'
python python/dimensionner_exposition.py --marge 0.40 --portage 6 --baisse 40
python python/dimensionner_exposition.py --leviers 1 2 3 --horizon 3 --sortie exposition.csv
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `--csv` | le fichier le plus récent de `docs/raw/data/quotes/` | Série étudiée. Première colonne : les dates. Colonne requise : `Close`. |
| `--fenetre` | tout l'historique | Nombre de séances retenues, **ancrées à droite**, pour $\sigma$ et $\hat\mu$. |
| `--marge`, `-m` | `0.20` | Couverture exigée. SRD espèces $20\,\%$, collatéral actions $40\,\%$ ([finance § 1.2](../docs/raw/concept/semestre4/finance/01-le-cadre-cac40-et-le-srd.md)). |
| `--portage`, `-c` | `5.0` | Coût du levier, en $\%$/an. **Déclaré, jamais estimé.** |
| `--baisse`, `-d` | `30.0` | Baisse à supporter sans appel de marge, en $\%$. |
| `--leviers` | `1 1.5 2 2.5 3 4` | Leviers examinés. |
| `--horizon` | `1.0` | Années, pour la probabilité d'appel. |
| `--cout-ar` | `0.53` | Coût d'un aller-retour, en $\%$ — le barème de [`couts_transaction.py`](couts_transaction.md). |
| `--rotation` | `1.0` | Aller-retours par an. |
| `--sortie` | — | Écrit le tableau par levier dans un CSV. Sans l'argument, affichage seul. |

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.

## Déroulé d'exécution

### 1. Lecture et contrôles

Sans `--csv`, le script prend le fichier `*.csv` le plus récemment modifié de
`docs/raw/data/quotes/` — **indices compris**, contrairement à
[`generer_graph_decision.py`](generer_graph_decision.md) : ici un indice est une
entrée légitime, c'est même le cas d'usage principal.

Le CSV est lu avec `pandas` ; la première colonne porte les dates, tronquées au
jour. `--fenetre` ne conserve que les $n$ dernières lignes.

Sortie **1** avec message sur `stderr` si : aucun CSV disponible, fichier
introuvable, colonne `Close` absente, **moins de 250 séances retenues**,
$\sigma$ nulle, ou l'un de ces arguments hors domaine — `--marge` hors
$\left]0\,;1\right[$, `--baisse` hors $\left]0\,;100\right[$, `--horizon` $\le 0$,
`--rotation` $< 0$, `--cout-ar` $< 0$, ou un levier $\le 0$.

Le seuil de 250 séances est celui de
[`construire_indice_total.py`](construire_indice_total.md) : une volatilité
estimée sur moins d'un an ne mérite pas d'être publiée.

### 2. Ce que la série dit, et ce qu'elle ne dit pas

Rendements arithmétiques quotidiens $r_t = P_t/P_{t-1} - 1$ sur `Close`.

| Grandeur | Formule |
|---|---|
| $\hat\mu$, dérive arithmétique annualisée | $252\,\overline{r}$ — c'est le $\mu$ de $L^\star$ |
| $\sigma$, volatilité annualisée | $\sqrt{252}\,\operatorname{pstdev}(r)$, variance de population (`ddof=0`) |
| CAGR | $(P_n/P_0)^{252/n} - 1$, pour mémoire |
| $Y$, horizon | $n/252$ années |
| $\operatorname{SE}(\hat\mu)$ | $\sigma/\sqrt{Y}$ |
| IC95 de $\hat\mu$ | $\hat\mu \pm 1{,}96\operatorname{SE}(\hat\mu)$ |
| Repli maximal | $\min_t\left(P_t/\max_{s\le t}P_s - 1\right)$ |

$\sigma$ est **aussi** publiée sur la dernière moitié et le dernier quart de la
fenêtre. Ce n'est pas une prévision : c'est la seule façon de voir d'un coup
d'œil si la volatilité retenue est un régime stable ou une moyenne entre deux
régimes.

Deux mentions obligatoires dans la sortie :

- la **largeur de l'IC95 de $\hat\mu$**, en points, suivie du mot
  **indiscernable de zéro** si l'intervalle contient $0$ — la règle du
  [cours alpha](../docs/raw/concept/semestre4/alpha/02-le-calcul-et-ses-erreurs-types.md),
  appliquée ici à une dérive plutôt qu'à un alpha ;
- si le **nom du fichier commence par `^`**, un rappel : *s'il s'agit d'un indice
  nu, $\hat\mu$ est sous-estimé du rendement du dividende.* C'est un **rappel
  fondé sur un nom de fichier, pas une détection** — une convention ne se devine
  pas depuis des nombres, et le script n'essaie pas.

### 3. Le levier admissible, qui ne dépend pas de $\mu$

Seuil d'appel de marge et son inverse, tous deux du
[finance § 3.1 et § 3.5](../docs/raw/concept/semestre4/finance/03-marge-appel-de-marge-et-ruine.md) :

$$x^\star = \frac{1/L - m}{1 - m}
\qquad\text{et}\qquad
L \le \frac{1}{m + (1-m)\,d}$$

Le script publie la borne pour la baisse demandée, puis la même borne pour
$d \in \{10, 20, 30, 40, 50\}\,\%$. **Aucune de ces valeurs ne dépend de la
série** : elles ne dépendent que de la marge et de la baisse qu'on veut
traverser. C'est le seul dimensionnement du script qui soit exact.

### 4. Par levier : le coût est certain, le bénéfice est inconnu

Pour chaque levier $L$ demandé :

| Colonne | Formule | Dépend de |
|---|---|---|
| Seuil d'appel | $x^\star = \frac{1/L-m}{1-m}$ | $m$ seul |
| Baisse à franchir | $-\ln(1-x^\star)$, en log | $m$ seul |
| $P(\text{appel})$ | § 4.1 | $\sigma$, $\mu$ déclaré, horizon |
| Drag | $L^2\sigma^2/2$ | $\sigma$ seul |
| Surcoût contre $L=1$ | $(L^2-1)\,\sigma^2/2$ | $\sigma$ seul |
| Portage | $(L-1)\,c$ | déclaré |
| Frais de rotation | $L \times \text{rotation} \times \text{coût}_{\text{A/R}}$ | déclaré |
| **$\mu$ requis** | $\mu_{\text{seuil}} = c + (L+1)\,\sigma^2/2$ | $\sigma$, $c$ |
| **Verdict** | § 4.2 | comparaison à l'IC95 |

#### 4.1 La probabilité d'appel, publiée en trois colonnes

La loi du minimum d'un brownien, formule du
[finance § 3.2](../docs/raw/concept/semestre4/finance/03-marge-appel-de-marge-et-ruine.md) :

$$P\left(\min_{t\le T} X_t \le a\right)
= \Phi\!\left(\frac{a-\nu T}{\sigma\sqrt T}\right)
+ e^{2\nu a/\sigma^{2}}\,\Phi\!\left(\frac{a+\nu T}{\sigma\sqrt T}\right),
\qquad a = \ln(1-x^\star),\ \nu = \mu - \sigma^2/2$$

Elle exige un $\mu$. Le script n'en invente donc pas **un** : il la calcule pour
**trois valeurs déclarées** — la borne basse de l'IC95, $\hat\mu$, et la borne
haute — et publie les trois côte à côte.

> ⚠️ **Les trois colonnes sont là pour être comparées, et ce qu'elles montrent
> n'est pas rassurant.** À levier modéré elles se ressemblent — $0{,}0$ à
> $2{,}8\,\%$ à $L = 2$ sur le CAC 40 ; à levier élevé elles s'écartent
> massivement : $8{,}1$ contre $44{,}7\,\%$ à $L = 3$, d'une borne de l'IC à
> l'autre. **La probabilité d'appel n'est donc pas robuste à l'ignorance sur
> $\mu$**, et il ne faut pas la lire comme un nombre.
>
> 🔑 **Une seule grandeur de ce script est exempte de $\mu$ : la borne admissible
> du § 3**, parce qu'elle ne fait intervenir aucun rendement. C'est elle qui doit
> porter le dimensionnement ; la probabilité d'appel n'est qu'un ordre de
> grandeur, et le $\mu$ requis du § 4.2 une exigence, jamais une prévision.

#### 4.2 Le $\mu$ requis, et le verdict

La croissance logarithmique d'une position à levier vaut
$g(L) = L\mu - (L-1)c - L^2\sigma^2/2$. Alors, pour $L > 1$ :

$$g(L) > g(1)
\iff (L-1)(\mu-c) > (L^2-1)\frac{\sigma^2}{2}
\iff \boxed{\;\mu > c + (L+1)\frac{\sigma^2}{2}\;}$$

C'est le **$\mu$ requis** : en deçà, ce levier fait moins bien que pas de levier
du tout. Le verdict le confronte à l'IC95 de $\hat\mu$ :

| Verdict | Condition |
|---|---|
| `justifie` | $\mu_{\text{seuil}} <$ borne basse de l'IC95 |
| `exclu` | $\mu_{\text{seuil}} >$ borne haute |
| **`indiscernable`** | l'intervalle contient $\mu_{\text{seuil}}$ — **le cas normal** |

Pour $L = 1$ les quatre colonnes de levier sont **vides** : sans levier il n'y a
ni seuil, ni portage, ni comparaison à soi-même. Une cellule vide plutôt qu'un
nombre inventé.

### 5. L'exposition nette, et pourquoi couvrir n'est pas un second cadran

Sur un actif **unique**, la couverture optimale du
[finance § 6](../docs/raw/concept/semestre4/finance/06-la-couverture-optimale.md)
est dégénérée : $\beta = 1$, $\rho^2 = 1$, $h^\star = 1$, variance résiduelle
nulle. Il n'y a rien à optimiser, et l'exposition nette

$$e = L\,(1-h)$$

est la seule grandeur qui décide. Le script publie donc, pour chaque levier, le
$h$ qui ramène l'exposition à $1$ — soit $h = 1 - 1/L$ — et **le coût annuel de
ce détour** :

$$\text{coût}(L) = (L-1)\left(c + \text{rotation}\times\text{coût}_{\text{A/R}}\right)$$

> ⚠️ **Atteindre $e = 1$ par un levier couvert coûte $(L-1)$ fois le portage,
> quand l'acheter directement coûte zéro.** Couvrir un actif par lui-même n'est
> pas une protection, c'est un chemin plus cher vers la même exposition. La
> couverture ne redevient un vrai second cadran que si l'actif couvert **n'est
> pas** l'actif de couverture — c'est-à-dire dès que $\rho^2 < 1$.

### 6. Résumé console

```
Serie            : ^FCHI (1793 seances, 2019-01-02 -> 2025-12-31, 7,11 ans)
Volatilite       : 18,94 %/an   (derniere moitie 14,66 % - dernier quart 14,79 %)
Repli maximal    : -38,6 %
CAGR             : 8,08 %/an
Derive mesuree   : mu = 9,58 %/an - SE 7,10 pt - IC95 [-4,34 ; 23,50] %
                   intervalle large de 27,8 points - indiscernable de zero
Rappel           : le nom du fichier commence par ^ ; s'il s'agit d'un indice nu,
                   mu est sous-estime du rendement du dividende.

Parametres declares : marge 20 % - portage 5,00 %/an - rotation 1,00 A/R/an a 0,530 %

Levier admissible pour supporter -30,0 % sans appel : L <= 2,27
   -10 %  L <= 3,57      -20 %  L <= 2,78      -30 %  L <= 2,27
   -40 %  L <= 1,92      -50 %  L <= 1,67

 levier    seuil   baisse      P(appel) bas/mu/haut      drag  surcout  portage    frais     mu requis  verdict
   1,00        -        -       -       -       -   -1,79 %        -        -   0,53 %            -  -
   1,50  58,33 %  87,55 %   0,0 %   0,0 %   0,0 %   -4,04 %  -2,24 %   2,50 %   0,80 %    9,49 %/an  indiscernable
   2,00  37,50 %  47,00 %   2,8 %   0,4 %   0,0 %   -7,18 %  -5,38 %   5,00 %   1,06 %   10,38 %/an  indiscernable
   2,50  25,00 %  28,77 %  20,4 %   6,5 %   1,5 %  -11,21 %  -9,42 %   7,50 %   1,33 %   11,28 %/an  indiscernable
   3,00  16,67 %  18,23 %  44,7 %  21,7 %   8,1 %  -16,15 % -14,35 %  10,00 %   1,59 %   12,18 %/an  indiscernable
   4,00   6,25 %   6,45 %  80,9 %  62,5 %  43,0 %  -28,71 % -26,91 %  15,00 %   2,12 %   13,97 %/an  indiscernable

Exposition nette e = L (1 - h) : couvrir un actif par lui-meme ne fait que baisser e
 levier   h pour e = 1   cout annuel de ce detour
   1,50          0,333                  2,77 %/an
   2,00          0,500                  5,53 %/an
   2,50          0,600                  8,29 %/an
   3,00          0,667                 11,06 %/an
   4,00          0,750                 16,59 %/an

Aucun levier n'est recommande : ce script rend ce qui est admissible, ce qui est
certain, et ce qu'il faudrait. Le rapprochement des trois est un dimensionnement,
pas un conseil.
```

Les nombres de ce bloc sont ceux mesurés sur `^FCHI` 2019-2025 aux paramètres par
défaut ; ils changent avec la série et avec les paramètres déclarés.

Le nom affiché est **dérivé du nom de fichier** — ce qui précède `_20`, `_`
remplacé par `.` : la convention de
[`generer_graph_decision.py`](generer_graph_decision.md). `AIR_PA_2019-…` donne
`AIR.PA`, `^FCHI_2019-…` donne `^FCHI`.

### 7. Le CSV de sortie

Avec `--sortie`, une ligne par levier, écrite par `csv.writer` (donc en CRLF,
RFC 4180) :

| Colonne | Contenu |
|---|---|
| `LEVIER` | le levier |
| `SEUIL_APPEL` | $x^\star$ en %, **vide** si $L = 1$ ou $x^\star \le 0$ |
| `BAISSE_LOG` | baisse à franchir en %, même règle |
| `P_APPEL_BAS`, `P_APPEL_MU`, `P_APPEL_HAUT` | les trois probabilités en % |
| `DRAG` | $-L^2\sigma^2/2$ en %/an |
| `SURCOUT` | $-(L^2-1)\sigma^2/2$ en %/an, vide si $L = 1$ |
| `PORTAGE` | $(L-1)c$ en %/an, vide si $L = 1$ |
| `FRAIS` | frais de rotation en %/an |
| `MU_REQUIS` | $\mu_{\text{seuil}}$ en %/an, vide si $L = 1$ |
| `VERDICT` | `justifie`, `exclu`, `indiscernable`, ou vide si $L = 1$ |
| `H_POUR_E1` | $1 - 1/L$, vide si $L = 1$ |
| `COUT_DETOUR` | coût annuel du détour en %/an, vide si $L = 1$ |

**Une cellule vide plutôt qu'un nombre inventé** : c'est la convention du dépôt,
et elle s'applique ici à toute quantité qui n'a pas de sens à $L = 1$ ou au-delà
du levier de défaut.

### 8. Cas limites

- **$L \ge 1/m$** — le seuil d'appel est nul ou négatif : la position est *déjà
  en défaut*. Le script écrit `defaut` dans la colonne du seuil, laisse la
  probabilité vide, et continue.
- **$L = 1$** : ni seuil, ni portage, ni surcoût, ni $\mu$ requis, ni verdict —
  cellules vides. Le drag et les frais, eux, existent.
- **IC95 contenant zéro** : le mot *indiscernable de zéro* est écrit, et **aucun
  commentaire n'est fait sur le signe de $\hat\mu$**.
- **$\mu_{\text{seuil}}$ comparé à un IC très large** : le verdict est
  `indiscernable` dans l'immense majorité des cas, et c'est le résultat, pas une
  défaillance.
- **Série d'un actif déjà à levier** (ETF $\times(-2)$, par exemple) : le script
  ne le sait pas et ne peut pas le savoir. Le $\sigma$ mesuré est celui de la
  série fournie ; appliquer un levier par-dessus le multiplie.
- **`--fenetre` plus grande que l'historique** : toute la série est retenue, sans
  message.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète. |
| `1` | CSV introuvable ou absent, colonne `Close` manquante, moins de 250 séances, $\sigma$ nulle, ou argument hors domaine. |

## Fonctions internes

- `charger(chemin)` — lit le CSV et rend (dates, clôtures).
- `phi(z)` — fonction de répartition normale, par `math.erf`.
- `p_barriere(x, mu, sigma, horizon)` — la formule du § 4.1.
- `mesures(closes)` — $\hat\mu$, $\sigma$, CAGR, IC95, repli maximal, $\sigma$ par
  sous-fenêtres.
- `ligne_levier(...)` — une ligne du tableau du § 4.
- `main()` — CLI, calculs, affichage, écriture éventuelle du CSV.

## Constantes

- `JOURS_AN = 252` — séances par an.
- `SEANCES_MINIMALES = 250` — en deçà, sortie 1.
- `Z95 = 1.959963985` — quantile normal bilatéral à 95 %, la loi normale
  suffisant ici : l'IC porte sur une moyenne de plusieurs centaines de
  rendements.
- `LEVIERS_DEFAUT = (1, 1.5, 2, 2.5, 3, 4)`.
- `MARGE_DEFAUT = 0.20`, `PORTAGE_DEFAUT = 5.0`, `BAISSE_DEFAUT = 30.0`,
  `HORIZON_DEFAUT = 1.0`, `COUT_AR_DEFAUT = 0.53`, `ROTATION_DEFAUT = 1.0`.
- `REPERTOIRE_QUOTES = Path("docs/raw/data/quotes")`.
