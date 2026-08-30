# generer_graph_decision.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `generer_graph_decision.py`, étape
par étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du
script doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Tracer, dans un fichier **SVG**, la figure que lit la règle du cours
[`docs/raw/concept/semestre4/trading/`](../docs/raw/concept/semestre4/trading/README.md) : un cours de
bourse, son encadrement actif, la séance de décision, et les **cinq critères**
avec le **verdict** qu'ils produisent.

C'est une figure de *décision*, pas de géométrie : elle ne montre pas seulement
les droites, elle montre ce que la règle en fait. Le verdict inscrit dans le SVG
est calculé par le script, jamais saisi à la main.

> **Les chaînes sont construites sur `High` et `Low`**, comme les modules du
> cours encadrement et comme les tableaux du cours trading — et **non** sur
> `Close` comme
> [`generer_graph_supp_resistance.py`](generer_graph_supp_resistance.md). Les deux
> scripts tracent donc des droites différentes sur la même série ; c'est voulu, et
> le § 8 de l'autre miroir explique l'écart.

> ⚠️ **Ce script ne produit aucun conseil en investissement.** Il affiche la
> sortie d'une règle écrite à l'avance, appliquée à des données passées. Le SVG
> porte cette mention en pied de figure, et elle n'est pas désactivable.

## Dépendances

- `pandas` (installé avec `yfinance`) pour la lecture des CSV.
- `p_valeur_student()` de [`import_societe.py`](import_societe.md), importée
  depuis le répertoire du script — la loi de Student n'est pas réimplémentée.
- Modules standard : `argparse`, `math`, `statistics`, `sys`, `pathlib`.
- **Aucune bibliothèque de tracé.** Le SVG est écrit à la main : `matplotlib`
  n'est pas installé, `scipy` non plus, et ni l'un ni l'autre ne doit l'être.

## Invocation

```bash
python python/generer_graph_decision.py
python python/generer_graph_decision.py --csv docs/raw/quotes/AIR_PA_2019-01-02_2020-12-31.csv \
                                        --indice docs/raw/quotes/^FCHI_2019-01-02_2020-12-31.csv
python python/generer_graph_decision.py --date 2020-12-31 --fenetre 120
python python/generer_graph_decision.py --sans-indice --sortie /tmp/decision.svg
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `--csv` | le fichier le plus récent de `docs/raw/quotes/` dont le nom ne commence pas par `^` | CSV de la valeur. Colonnes requises : `Date`, `High`, `Low`, `Close`, `TEND_20`, `TEND_120`. |
| `--indice` | — | CSV de l'indice de référence, pour le critère 4. |
| `--sans-indice` | — | Ne pas calculer le critère 4. Incompatible avec `--indice`. |
| `--date` | la dernière séance du CSV | Séance de décision `AAAA-MM-JJ`. Si la date n'est pas une séance, le script recule à la dernière séance disponible **avant ou à** cette date, et le signale (§ 2). |
| `--fenetre` | `120` | Longueur de la fenêtre active, ancrée à la séance de décision (§ 3). |
| `--tolerance` | `0.25` | Tolérance de contact, en multiples de $\sigma_{\text{Close}}$ de la fenêtre. |
| `--sortie` | `docs/raw/graphs/{nom_du_csv}_decision.svg` | Chemin du SVG produit (répertoire créé si besoin). |
| `--titre` | `{ticker} — les cinq critères au {date de décision}` | Titre inscrit dans le SVG. Le ticker est dérivé du nom de fichier, `_` remplacé par `.`. |

## Déroulé d'exécution

### 1. Lecture des arguments et des CSV

`argparse` analyse la ligne de commande. Sans `--csv`, le script prend le fichier
`*.csv` le plus récemment modifié de `docs/raw/quotes/` **dont le nom ne commence
pas par `^`** — sans quoi le CSV d'un indice serait pris pour une valeur.

Chaque CSV est lu avec `pandas`. Les dates sont tronquées au jour (`AAAA-MM-JJ`),
le fuseau horaire est ignoré : ce sont des rangs de séance qui comptent.

Sortie **1** avec message sur `stderr` si : aucun CSV disponible, fichier
introuvable, colonne requise absente, ou historique plus court que `--fenetre`.

`--indice` et `--sans-indice` ensemble : sortie **1**. Aucun des deux : le
critère 4 est marqué *non calculé*, exactement comme avec `--sans-indice`, et le
script le rappelle dans son résumé console.

### 2. La séance de décision — le point qui interdit le regard en avant

La séance de décision est la dernière séance dont la clôture est **connue** au
moment où l'on décide.

- Sans `--date` : la dernière ligne du CSV.
- Avec `--date` : la dernière séance dont la date est **inférieure ou égale** à
  la date demandée. Si aucune, sortie **1**.
- Si la date demandée n'est pas elle-même une séance (week-end, jour férié), le
  script affiche `Le {date} n'est pas une séance ; décision au {séance retenue}.`
  et l'inscrit dans le sous-titre du SVG.

**Toutes les lignes postérieures à la séance de décision sont supprimées** avant
tout calcul. C'est la garantie de non-regard-en-avant : aucune quantité tracée ou
chiffrée ne peut dépendre d'une séance future, y compris l'échelle des axes.

### 3. La fenêtre active et l'encadrement

La fenêtre active est constituée des `--fenetre` dernières séances, ancrée à
droite sur la séance de décision. Sur cette tranche, et pour chaque côté :

- **Résistance** : chaîne **supérieure** de l'enveloppe convexe des points
  $(i, \text{High}_i)$ ;
- **Support** : chaîne **inférieure** de l'enveloppe convexe des points
  $(i, \text{Low}_i)$.

Balayage de Andrew, `chaine(points, inferieure)`, identique à celui du cours
encadrement et de l'autre script.

L'arête retenue est la **dernière arête dont la portée atteint
$\max(3, \text{fenêtre}//4)$**, en remontant la chaîne depuis la droite —
`arete_retenue()`. Sa pente et son ancre définissent la droite
$d(t) = y_1 + \text{pente}\,(t - x_1)$, prolongée jusqu'à la séance de décision.

Les **épisodes de contact** se comptent sur la série qui a **construit** la
droite : $|{\text{High}_i - d(i)}| \le \varepsilon$ pour la résistance,
$|{\text{Low}_i - d(i)}| \le \varepsilon$ pour le support. La tolérance, elle,
reste calée sur les clôtures — $\varepsilon = \text{tolerance} \times
\sigma_{\text{Close}}$ de la fenêtre, convention du
[module 2 du cours encadrement](../docs/raw/concept/semestre3/encadrement/02-portee-et-episodes-de-contact.md).
Deux séances de contact distantes de moins de `ECART_EPISODE = 3` appartiennent
au même épisode.

> ⚠️ **Compter les contacts sur `Close` est une erreur, pas une variante.** Une
> droite ajustée sur les extrêmes de séance n'a aucune raison de frôler les
> clôtures, et le comptage s'effondre : sur la fenêtre active d'Airbus au
> 29 décembre 2023, la mesure sur `Close` donne 1 épisode de résistance et
> **0** de support là où la mesure sur `High`/`Low` en donne 2 et 4 — les
> chiffres publiés par le cours encadrement. Le veto 1 en dépend directement.

**Contrôle de non-traversée** : le nombre de `High` au-dessus de la résistance et
de `Low` sous le support doit être nul sur la fenêtre. Sinon, message sur
`stderr` et sortie **2** — c'est un bogue de l'enveloppe convexe, pas une
propriété des données.

### 4. Les cinq critères

| # | Critère | Calcul | Sortie |
|---|---|---|---|
| 1 | Tendance longue | colonne `TEND_120` à la séance de décision | $-1$, $0$ ou $+1$ |
| 2 | Tendance courte | colonne `TEND_20` idem | $-1$, $0$ ou $+1$ |
| 3 | Position | $100 \times \dfrac{\text{Close} - \text{support}(t)}{\text{résistance}(t) - \text{support}(t)}$ | % de la hauteur |
| 4 | Alpha | § 4.1 | % annualisé et IC95 |
| 5 | Momentum 12-1 | $\dfrac{P_{t-21}}{P_{t-252}} - 1$, en **rangs de séance** | % |

Le critère 3 n'est pas borné à $[0, 100]$ : une clôture hors canal donne une
position négative ou supérieure à 100, et c'est une information, pas une erreur.

Le critère 5 exige au moins 253 séances d'historique ; sinon il est marqué *non
calculé* et le **veto 4** s'applique de toute façon.

#### 4.1 Alpha et bêta

Rendements arithmétiques quotidiens $r_t = P_t/P_{t-1} - 1$ sur `Close`, **sur les
seules dates communes** aux deux séries, alignées par date — les calendriers ne
sont pas supposés identiques. Taux sans risque $r_f = 0$, valeur annoncée dans le
résumé et dans le SVG.

```
beta  = Cov(ri, rm) / Var(rm)
alpha = E(ri) - beta * E(rm)
e_t   = ri_t - (alpha + beta * rm_t)
s²    = somme(e²) / (n - 2)
SE(alpha) = s * sqrt(1/n + E(rm)² / (n * Var(rm)))
```

Annualisation par $252$ : $\alpha_{\text{an}} = 252\,\alpha$ et
$\operatorname{SE}(\alpha_{\text{an}}) = 252\operatorname{SE}(\alpha)$.

L'IC95 vaut $\alpha_{\text{an}} \pm t_{n-2;\,0{,}975}\operatorname{SE}(\alpha_{\text{an}})$.
Le quantile $t_{n-2;\,0{,}975}$ est obtenu par **dichotomie sur
`p_valeur_student()`** — `quantile_student(ddl, 0.975)`, 80 itérations sur
$[0, 100]$ — puisque le dépôt ne fournit que la $p$-valeur et que `scipy` est
proscrit.

> 🔑 **Seule la borne haute de l'IC entre dans la règle**, jamais le signe de
> $\alpha$. Le SVG affiche l'intervalle en entier, et le mot
> **indiscernable de zéro** dès qu'il contient zéro.

### 5. Le verdict

La règle est celle du
[module 3 du cours trading](../docs/raw/concept/semestre4/trading/03-la-regle-ecrite-a-l-avance.md),
recopiée ici sans modification. Elle est évaluée **dans cet ordre** : les vetos
d'abord, les conditions ensuite.

**Quatre vetos, qui imposent `ATTENTE` quels que soient les critères :**

| # | Veto |
|---|---|
| 1 | moins de 3 épisodes de contact d'un côté de l'encadrement actif |
| 2 | canal convergent se refermant en moins de 20 séances |
| 3 | critères 1 et 2 de signes opposés |
| 4 | historique de moins de 120 séances |

La **date de péremption** du veto 2 est
$\tau = \dfrac{\text{résistance}(t) - \text{support}(t)}{\text{pente}_{\text{support}} - \text{pente}_{\text{résistance}}}$
quand le dénominateur est strictement positif, et $+\infty$ sinon (canal
parallèle ou divergent).

**Les deux conditions :**

- `ACHAT` — critères 1 et 2 à $+1$, position $< 35\,\%$, momentum 12-1 positif,
  et borne haute de l'IC de l'alpha $> 0$ ;
- `VENTE` — critères 1 et 2 à $-1$, position $> 65\,\%$, momentum 12-1 négatif ;
- `ATTENTE` dans **tous** les autres cas.

Quand le critère 4 n'est pas calculé, la condition d'IC est réputée **non
satisfaite** : `ACHAT` devient inatteignable. `VENTE` reste atteignable, la règle
ne lui imposant aucune condition d'alpha.

Le script rend la liste des vetos déclenchés **et** la liste des conditions
manquantes, pas seulement le verdict : un `ATTENTE` sans motif n'est pas
publiable.

### 6. Écriture du SVG

Fichier de $1200 \times 700$, fond `#fcfcfb`, police monospace pour les chiffres
et Georgia pour le titre. Aucune police externe, aucune ressource distante.

De haut en bas :

1. **Titre** et sous-titre — nombre de séances, plage de dates, séance de
   décision, et la mention du jour férié le cas échéant.
2. **Grille** horizontale tous les 20 €, étiquettes d'années aux changements
   d'année. L'échelle verticale couvre les clôtures **et les seuls segments de
   droite réellement tracés**, c'est-à-dire de l'ancre de chaque droite à la
   séance de décision — jamais leur prolongement vers la gauche, qui plonge très
   bas et écraserait le graphique.
3. **Zone de la fenêtre active** en aplat léger, pour distinguer d'un coup d'œil
   ce que la règle regarde de ce qu'elle ignore.
4. **Cours** (`Close`) en trait bleu sur tout l'historique retenu.
5. **Support** (vert) et **résistance** (orange) en trait plein sur la fenêtre
   active, avec la valeur à la séance de décision en bout de droite et un disque
   sur chaque séance de contact — **posé sur le `High` ou le `Low` de la séance**,
   c'est-à-dire sur le point qui touche réellement la droite, et non sur la
   clôture, qui peut en être loin.
6. **Séance de décision** : trait vertical en pointillé, disque sur la clôture,
   et étiquette portant la date et la clôture. L'étiquette est placée **en haut
   de la zone de tracé, alignée à droite** — pas à côté du disque, où les droites
   de support et de résistance la traversent ; le trait vertical suffit à la
   rattacher au point.
7. **Encart des cinq critères**, un par ligne : numéro, libellé, valeur, et une
   pastille `✓` / `✗` / `–` indiquant si le critère va dans le sens d'un `ACHAT`,
   d'une `VENTE`, ou d'aucun des deux.
8. **Bandeau du verdict**, en bas : le mot (`ACHAT`, `VENTE` ou `ATTENTE`), les
   vetos déclenchés, et la mention obligatoire *sortie d'une règle écrite, pas
   une recommandation*.

Les couleurs sont celles de l'autre script, plus `COULEUR_VERDICT` (gris ardoise)
pour le bandeau : `ATTENTE` n'est pas un signal, il ne doit pas être coloré comme
tel.

### 7. Résumé console

```
Valeur           : AIR.PA (513 séances, 2019-01-02 → 2020-12-31)
Décision         : 2020-12-31
Fenêtre active   : 2020-07-16 → 2020-12-31 (120 séances, ε = 2,62 €)
Résistance       : pente +0,2306 €/séance · portée 83 · 6 épisodes · 93,18 €
Support          : pente +0,5820 €/séance · portée 37 · 3 épisodes · 79,99 €
Largeur          : 13,19 € (16,0 %) · τ = 37,5 séances

Critère 1  tendance longue — TEND_120        : +1
Critère 2  tendance courte — TEND_20         : -1
Critère 3  position dans l'encadrement actif : 18,0 % de la hauteur
Critère 4  alpha annualisé contre l'indice   : -0,29 %/an · IC95 [-49,44 ; +48,85] % · indiscernable de zéro
Critère 5  momentum 12-1                     : -33,47 %

Vetos            : veto 3 : critères 1 et 2 de signes opposés
VERDICT          : ATTENTE

Sortie d'une règle écrite à l'avance, pas une recommandation.
Graphique écrit dans : {chemin}
```

### 8. Cas limites

- **Clôture hors canal** : position < 0 ou > 100, affichée telle quelle et
  signalée par le mot `hors canal` dans l'encart.
- **Canal divergent ou parallèle** : $\tau = \infty$, affiché `∞`, veto 2 inactif.
- **Moins de 253 séances** : critère 5 non calculé, veto 4 déjà actif si moins de
  120 séances ; entre 120 et 252 séances, le veto 4 ne s'applique pas mais
  `ACHAT` et `VENTE` sont tous deux inatteignables faute de momentum.
- **Aucune date commune** avec l'indice : critère 4 non calculé, message sur
  `stderr`, exécution poursuivie.
- **`TEND_20` ou `TEND_120` vide** à la séance de décision (moins de $n$ séances
  d'historique) : critère lu comme $0$, ce qui ne déclenche pas le veto 3 mais
  interdit `ACHAT` comme `VENTE`.

### 9. Résultat sur AIR.PA au 31 décembre 2020

C'est la figure du README du cours trading. Fenêtre active du 2020-07-16 au
2020-12-31, $\varepsilon = 2{,}62$ € :

| | Ancre | Pente | Portée | Épisodes | Valeur au 2020-12-31 |
|---|---|---|---|---|---|
| Résistance | 2020-08-11 | $+0{,}2306$ €/séance | 83 | 6 | 93,18 € |
| Clôture | — | — | — | — | **82,37 €** |
| Support | 2020-10-29 | $+0{,}5820$ €/séance | 37 | 3 | 79,99 € |

Largeur $13{,}19$ € soit $16{,}0\,\%$ ; position $18{,}0\,\%$ ; $\tau = 37{,}5$
séances ; contrôle de non-traversée : 0 des deux côtés. Verdict `ATTENTE`,
veto 3.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète, SVG écrit. |
| `1` | CSV introuvable, colonne requise absente, historique plus court que `--fenetre`, date de décision antérieure au premier jour coté, ou `--indice` et `--sans-indice` ensemble. |
| `2` | Contrôle de non-traversée en échec — bogue de l'enveloppe convexe. |

## Fonctions internes

- `chaine(points, inferieure)` — chaîne inférieure ou supérieure de l'enveloppe
  convexe, balayage de Andrew.
- `arete_retenue(chaine, portee_min)` — dernière arête de portée suffisante.
- `episodes(indices, ecart)` — regroupement des séances de contact en contacts.
- `quantile_student(ddl, niveau)` — quantile de Student par dichotomie sur
  `p_valeur_student()`.
- `alpha_beta(closes_valeur, dates_valeur, closes_indice, dates_indice)` —
  régression des rendements sur dates communes ; rend $\alpha$, $\beta$, leurs
  erreurs types, l'IC95 annualisé, $R^2$ et le nombre de rendements.
- `encadrement(hauts, bas, closes, a, b, tolerance)` — les deux droites de la
  fenêtre active et leurs contacts.
- `verdict(criteres, vetos)` — applique la règle et rend le mot, les vetos
  déclenchés et les conditions manquantes.
- `svg(...)` — assemblage du fichier, sans dépendance.

## Constantes

- `REPERTOIRE_QUOTES = Path("docs/raw/quotes")` — source par défaut.
- `REPERTOIRE_GRAPHS = Path("docs/raw/graphs")` — destination par défaut, exclue
  du suivi git : un SVG est une sortie régénérable, pas une source. La figure du
  cours, elle, est écrite explicitement dans
  `docs/raw/concept/semestre4/trading/figures/` et **est** suivie.
- `ECART_EPISODE = 3` — séances séparant deux épisodes de contact.
- `JOURS_AN = 252` — séances par an, pour l'annualisation et le momentum.
- `SEUIL_ACHAT = 35`, `SEUIL_VENTE = 65` — positions, en % de la hauteur.
- `TAU_MINIMAL = 20` — séances avant fermeture du canal, seuil du veto 2.
- `EPISODES_MINIMAUX = 3` — seuil du veto 1.
- `HISTORIQUE_MINIMAL = 120` — séances, seuil du veto 4.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
