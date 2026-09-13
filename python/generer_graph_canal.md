# generer_graph_canal.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `generer_graph_canal.py`, étape par
étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du script
doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Tracer, dans un fichier **SVG**, un cours de bourse sur **trois ans** et ses
**trois derniers encadrements**, tous ancrés à une même **date d'observation** :

| Fenêtre | Méthode | Largeur |
|---|---|---|
| **250 séances** | droite des moindres carrés | **± 1 écart-type résiduel** |
| **120 séances** | droite des moindres carrés | **± 1 écart-type résiduel** |
| **20 séances** | droite des moindres carrés | **enveloppe des résidus** |

> **Une seule largeur par fenêtre, la dernière.** Contrairement à
> [`generer_graph_supp_resistance.py`](generer_graph_supp_resistance.md), ce script
> ne segmente pas l'historique en blocs : il ne trace que l'encadrement **actif** de
> chacune des trois fenêtres, celui qui se termine à la date d'observation.

> **Ce ne sont pas les mêmes droites que les deux autres scripts de graphique.**
> `generer_graph_supp_resistance.py` et `generer_graph_decision.py` encadrent par
> **enveloppe convexe** — des droites qui ne coupent aucun point. Ici, les fenêtres
> 250 et 120 sont encadrées par l'**écart-type résiduel** de la régression, qui
> laisse au contraire environ un tiers des séances dehors. Seule la fenêtre 20
> reprend une idée d'enveloppe, sur les **résidus** et non sur les cours.

> ⚠️ **Ce script ne rend aucun verdict.** Il trace les trois encadrements et
> publie les écarts chiffrés ; il ne dit pas quoi en faire. Aucune règle, aucun
> seuil de décision, aucun conseil en investissement.

## Dépendances

- `pandas` (installé avec `yfinance`) pour la lecture du CSV.
- Modules standard : `argparse`, `math`, `statistics`, `sys`, `pathlib`.
- **Aucune bibliothèque de tracé.** Le SVG est écrit à la main : `matplotlib`
  n'est pas installé et ne doit pas l'être.
- **Aucune colonne calculée n'est requise.** Le script ne lit que `Date` et
  `Close`, et recalcule lui-même les trois régressions — voir § 2.

## Invocation

```bash
python python/generer_graph_canal.py
python python/generer_graph_canal.py --csv docs/raw/data/quotes/AI_PA_2020-01-02_2025-12-31.csv
python python/generer_graph_canal.py --date 2025-12-31
python python/generer_graph_canal.py --annees 5 --sortie docs/done/graphiques/canal.svg
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `--csv` | le fichier le plus récent de `docs/raw/data/quotes/` dont le nom ne commence pas par `^` | Chemin du CSV d'entrée. Colonnes requises : `Date` et `Close`. |
| `--date` | la dernière séance du CSV | **La date d'observation**, `AAAA-MM-JJ`. Les trois encadrements s'y terminent, et le tracé s'y arrête. Si ce n'est pas une séance, le script recule à la dernière séance **avant ou à** cette date et le signale. |
| `--annees` | `3` | Nombre d'années civiles de **construction** avant la date d'observation : c'est cette fenêtre qui fixe l'**échelle verticale** et les bornes du graphique. |
| `--zoom` | `--annees` | Nombre d'années **réellement affichées**, en tronquant à gauche. Le graphique est bâti sur `--annees`, **puis** recadré sur `--zoom` : l'échelle verticale reste celle de la construction. |
| `--fenetres` | `250,120` | Fenêtres encadrées à l'**écart-type**, décroissantes, séparées par des virgules. |
| `--enveloppe` | `20` | Fenêtre encadrée par l'**enveloppe des résidus**. |
| `--sortie` | `docs/raw/data/graphs/{nom_du_csv}_canal_{date}.svg` | Chemin du SVG produit (répertoire créé si besoin). |
| `--titre` | `{ticker} — canal au {date d'observation}` | Titre inscrit dans le SVG. Le ticker est dérivé du nom de fichier, `_` remplacé par `.`. |

## Déroulé d'exécution

### 1. Lecture des arguments et du CSV

`argparse` analyse la ligne de commande. Sans `--csv`, le script prend le fichier
`*.csv` le plus récemment modifié de `docs/raw/data/quotes/` dont le nom ne
commence pas par `^` — un indice n'est pas une valeur ; s'il n'y en a aucun :
message sur `stderr` et **sortie 1**.

Le CSV est lu avec `pandas`, seules `Date` et `Close` sont conservées. Les lignes
sans `Close` sont **ignorées** — la dernière ligne d'un import récent en est
souvent une. Les dates sont tronquées au jour, le fuseau de l'horodatage ignoré :
ce sont des rangs de séance qui comptent.

Si `Close` est absente : message sur `stderr` et **sortie 1**.

### 2. La date d'observation, et ce qu'elle exige

La date d'observation est le **point d'ancrage de tout le graphique**. Si
`--date` ne tombe pas sur une séance — week-end, férié —, le script recule à la
dernière séance disponible avant ou à cette date, et l'écrit dans son résumé.

Il faut **au moins `max(--fenetres)` séances** dans le CSV jusqu'à cette date
incluse, faute de quoi la plus longue régression ne peut pas se calculer :
message sur `stderr` et **sortie 1**. Avec les valeurs par défaut, il faut donc
250 séances avant le 2025-12-31, et non 250 séances dans le fichier.

### 3. Les régressions à l'écart-type — fenêtres 250 et 120

Pour chaque fenêtre `n` de `--fenetres`, sur les `n` dernières clôtures jusqu'à
la date d'observation, avec les rangs $T_i = i$, $i = 1,\dots,n$ :

$$E_n = \frac{1}{n}\sum C_i, \qquad
\operatorname{VAR}_n = \frac{1}{n}\sum (C_i - E_n)^2, \qquad
V_T(n) = \frac{n^2-1}{12}$$

$$\operatorname{CORR}_n = \frac{\operatorname{cov}(T, C)}{\sqrt{V_T(n)\operatorname{VAR}_n}},
\qquad r_n = \frac{\operatorname{cov}(T, C)}{V_T(n)}, \qquad
\operatorname{VAL}_n = E_n + r_n\left(n - \tfrac{n+1}{2}\right)$$

$$s_n = \sqrt{\frac{n}{n-2}\,\operatorname{VAR}_n\,(1 - \operatorname{CORR}_n^2)}$$

La bande est $\operatorname{VAL}_n \pm 1\,s_n$, évaluée le long de la droite.

> **La variance est celle de population, `ddof = 0`**, comme partout dans ce
> dépôt. Ce sont exactement les colonnes `E_n`, `VAR_n`, `CORR_n`, `VAL_n` que
> produit [`import_societe.py`](import_societe.md) — le script les **recalcule**
> au lieu de les lire, parce que la fenêtre **250 n'existe dans aucun CSV** :
> `import_societe.py` ne calcule que `n ∈ {20, 120}`. Recalculer les deux assure
> que les trois bandes sortent de la même formule.
>
> **Contrôle effectué** : sur `AI_PA_2020-01-02_2025-12-31.csv` au 2025-12-31, la
> fenêtre 120 recalculée retrouve les colonnes du CSV à **10⁻¹¹ près** sur les
> quatre grandeurs.

L'écart réduit publié est $(C_{\text{obs}} - \operatorname{VAL}_n)/s_n$, en
écarts-types — la grandeur que lisent les expériences 4 à 12.

### 4. L'enveloppe des résidus — fenêtre 20

Même droite des moindres carrés sur les `--enveloppe` dernières clôtures, mais la
largeur n'est **pas** un écart-type :

1. les résidus $\varepsilon_i = C_i - (E_n + r_n(T_i - \bar T))$ sont calculés ;
2. la demi-largeur **basse** est $-\min_i \varepsilon_i$, la **haute** est
   $\max_i \varepsilon_i$ ;
3. les deux séances qui réalisent ces extrêmes sont les **points de contact**, et
   le script les nomme.

> ⚠️ **Cette enveloppe est asymétrique, et c'est son intérêt.** Une bande à
> l'écart-type est symétrique par construction et ne peut pas montrer qu'un cours
> s'écarte davantage vers le bas que vers le haut. Sur Air Liquide au 2025-12-31,
> l'enveloppe mesure 2,32 € sous la droite contre 2,13 € au-dessus.
>
> Par construction, elle **touche exactement deux points et n'en laisse aucun
> dehors**, là où la bande à 1 s en laisse environ un tiers.

### 5. Les deux fenêtres : construction, puis troncature

Le script distingue **deux** fenêtres, et l'ordre entre elles est ce qui donne son
sens au graphique.

**La fenêtre de construction** couvre les `--annees` années avant la date
d'observation : toutes les séances strictement postérieures à la date
d'observation **diminuée de `--annees` années civiles**. C'est elle qui fixe
l'**échelle verticale** — le minimum et le maximum de l'axe des ordonnées sont
calculés sur ses clôtures et sur les six bornes des encadrements.

**La fenêtre affichée** couvre les `--zoom` dernières années, et le graphique y
est **tronqué à gauche**. L'échelle verticale n'est **pas** recalculée.

> **Pourquoi cet ordre importe.** Recalculer l'échelle sur la seule fenêtre
> affichée ne produit pas un graphique tronqué, mais **un autre graphique** : les
> amplitudes changent, les bandes paraissent plus larges ou plus étroites, et deux
> figures de la même valeur cessent d'être comparables. Ici, `--zoom` ne fait que
> recadrer ce que `--annees` a construit — les proportions verticales sont
> préservées.

Par défaut `--zoom` vaut `--annees` : aucune troncature.

Chaque droite n'est tracée que **sur sa fenêtre**, jamais au-delà. Une droite
d'encadrement n'existe pas hors de la fenêtre qui l'a produite — c'est la règle du
[module 3](../docs/raw/concept/semestre3/encadrement/03-segmenter-un-historique-long.md).

> ⚠️ **L'affichage est élargi si une fenêtre déborde.** Avec `--annees 3`, les
> trois encadrements tiennent largement dans le tracé. Avec `--annees 1`, la
> fenêtre de 250 séances couvre à elle seule presque toute l'année : le script
> prend alors comme départ le **minimum** entre le début de l'affichage demandé et
> le début de la plus longue fenêtre, de sorte qu'aucune droite ne soit tronquée à
> gauche.
>
> Conséquence à connaître : **`--annees` borne l'affichage par le bas, pas par le
> haut.** Demander une fenêtre plus courte que `max(--fenetres)` séances ne
> resserre pas le graphique en deçà de cette limite. Pour zoomer davantage, il faut
> réduire `--fenetres`.

Aucune séance postérieure à la date d'observation n'est lue, ni pour les droites,
ni pour les échelles : **pas de regard en avant**, échelles de graphique
comprises.

### 6. Écriture du SVG

Un seul fichier autonome, sans police externe ni script :

- fond clair, grille horizontale à pas lisible ;
- **repères verticaux datés, dont le pas s'adapte à l'affichage** : aux changements
  d'**année** si le tracé couvre **deux ans ou plus**, aux changements de **mois**
  en deçà. Sans cette bascule, un affichage d'un an ne porterait **aucun repère** —
  il ne contient aucun changement d'année —, et l'axe des abscisses serait muet ;
- **cours** en bleu `#2a78d6`, trait de 1,4 px, sur toute la fenêtre d'affichage ;
- **bande 250** en gris-bleu `#7a8ba6`, la plus large, remplissage à 6 % ;
- **bande 120** en bleu `#1f5f8b`, remplissage à 8 % ;
- **enveloppe 20** en orange `#b35c1e`, sans remplissage ;
- chaque droite centrale en trait plein, ses deux bords en pointillé ;
- les **deux points de contact** de l'enveloppe 20 marqués par un cercle ;
- la **clôture d'observation** marquée par un disque plein ;
- étiquettes de valeur au bord droit pour les six bornes ;
- cartouche en haut à gauche : pour chaque fenêtre, la pente en €/séance et en
  %/séance, la largeur en € et en %, et l'écart réduit du cours ;
- légende en bas, et la mention que le graphique ne rend aucun verdict.

Dimensions : `1200 × 620` unités de `viewBox`, redimensionnable sans perte.

### 7. Résumé console

```
{titre} — {n} séances affichées, du {première date} au {date d'observation}
Clôture au {date d'observation} : {c} €

  bande 250   {bas} – {haut} €   largeur {l} € ({p} %)   pente {r} €/séance ({t} %/séance)
              droite {val} €   CORR {corr}   écart réduit {e} s
  bande 120   {bas} – {haut} €   largeur {l} € ({p} %)   pente {r} €/séance ({t} %/séance)
              droite {val} €   CORR {corr}   écart réduit {e} s
  enveloppe 20 {bas} – {haut} €  largeur {l} € ({p} %)   pente {r} €/séance ({t} %/séance)
              droite {val} €   contacts bas {d1}, haut {d2}   asymétrie {b} bas / {h} haut

Graphique écrit dans : {chemin}
```

Deux avertissements sont émis sur `stdout` quand ils s'appliquent :

- ⚠️ **`CORR_n` proche de zéro** — en deçà de `0,20` en valeur absolue, la droite
  n'explique presque rien et la bande est une **dispersion, pas un canal**. C'est
  le cas de la fenêtre 250 d'Air Liquide au 2025-12-31 : `CORR = −0,085`.
- ⚠️ **La clôture d'observation touche une borne** à moins de `s_n/10` : la
  coïncidence est alors à lire avec prudence.

### 8. Résultat sur AI.PA au 2025-12-31

Fichier `AI_PA_2020-01-02_2025-12-31.csv`, 1 538 séances ; affichage sur 3 ans,
soit 766 séances du 2023-01-02 au 2025-12-31. Clôture **142,63 €**.

| Fenêtre | Encadrement | Largeur | Droite | Pente | Écart réduit |
|---|---|---|---|---|---|
| **250**, écart-type | 145,86 – 158,92 € | 13,06 € (9,16 %) | 152,39 € | −0,0050 %/séance | **−1,49 s** |
| **120**, écart-type | 141,40 – 148,20 € | 6,80 € (4,76 %) | 144,80 € | −0,0813 %/séance | −0,64 s |
| **20**, enveloppe | 139,19 – 143,64 € | 4,45 € (3,12 %) | 141,51 € | −0,0947 %/séance | — |

Les trois pentes sont négatives et **s'accentuent à mesure que la fenêtre se
raccourcit**. La bande 250 a `CORR = −0,085` : elle déclenche l'avertissement du
§ 7. L'enveloppe 20 touche le bas au **2025-12-09** et le haut au **2025-12-02**.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète, SVG écrit. |
| `1` | CSV introuvable, colonne `Close` absente, `--date` antérieure à la première séance, ou moins de `max(--fenetres)` séances jusqu'à la date d'observation. |
| `2` | Une variance nulle ou une corrélation non calculable sur l'une des fenêtres — cours constant. |

## Fonctions internes

- `charger(chemin)` — lit le CSV, écarte les lignes sans `Close`, rend dates et
  clôtures.
- `rang_observation(jours, date)` — l'indice de la séance d'observation, en
  reculant si nécessaire.
- `regression(closes, fin, n)` — les six grandeurs du § 3 pour la fenêtre `n` se
  terminant au rang `fin`.
- `enveloppe(closes, fin, n)` — la droite, les deux demi-largeurs et les deux
  points de contact du § 4.
- `svg(...)` — assemblage du fichier, sans dépendance.

## Constantes

- `REPERTOIRE_QUOTES = Path("docs/raw/data/quotes")` — source par défaut.
- `REPERTOIRE_GRAPHS = Path("docs/raw/data/graphs")` — destination par défaut,
  exclue du suivi git : un SVG est une sortie régénérable, pas une source. Pour
  conserver un graphique, passer `--sortie` vers un répertoire suivi, par exemple
  `docs/done/graphiques/`.
- `CORR_FAIBLE = 0.20` — en deçà, la droite n'explique presque rien (§ 7).
- `LARGEUR = 1200`, `HAUTEUR = 620` — dimensions du `viewBox`.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
