# couts_transaction.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `couts_transaction.py`, étape par
étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du script
doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Chiffrer ce qu'une règle de décision coûte à exécuter, et le comparer à l'alpha
qu'elle devrait produire pour être rentable.

Le dépôt sait mesurer des tendances, des canaux et des alphas ; il ne savait pas
dire qu'une règle à rotation mensuelle perd **6,4 % par an** avant d'avoir gagné
quoi que ce soit. C'est le seul chiffre qui disqualifie un écran avant même de le
tester.

> 🔑 **Les coûts ne s'estiment pas, ils se déclarent.** La taxe sur les
> transactions financières est un taux légal, le courtage une clause de contrat,
> le spread une donnée de marché observable. Aucun des trois n'a besoin d'être
> reconstruit statistiquement — et une estimation serait moins fiable que le
> paramètre lui-même.

### Pourquoi pas un estimateur de spread

L'estimateur de Corwin-Schultz (2012) ne demande que `High` et `Low`, que les CSV
du dépôt contiennent déjà. Il a été essayé, et **écarté sur mesure** : appliqué à
AIR.PA il rend un spread médian de $1{,}01\,\%$ sur 2019-2020 et $1{,}01\,\%$ sur
2020-2023, là où une grande capitalisation du CAC 40 en cote quelques points de
base. L'estimateur est construit pour des titres illiquides ; sur celles-ci il
surestime de deux ordres de grandeur.

Le script ne l'implémente donc pas. Un paramètre déclaré et discutable vaut mieux
qu'un nombre calculé et faux.

## Dépendances

- `yfinance`, pour le pays d'immatriculation et la capitalisation (§ 2).
- Modules standard : `argparse`, `csv`, `math`, `statistics`, `sys`, `pathlib`.
- **Aucune donnée n'est requise** en mode barème : le script tourne sans réseau
  et sans CSV.

## Invocation

```bash
python python/couts_transaction.py
python python/couts_transaction.py --montant 50000
python python/couts_transaction.py AIR.PA OR.PA ATO.PA --montant 50000
python python/couts_transaction.py --courtage 0.02 --spread 0.01 --sans-ttf
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `tickers` | — | Valeurs à chiffrer. Sans argument : **mode barème**, sans réseau. |
| `--ttf` | `0.30` | Taux de la TTF, en %, prélevé **à l'achat seulement**. |
| `--courtage` | `0.10` | Courtage en %, **par sens**. |
| `--spread` | `0.03` | Spread **complet** en % ; on en paie la moitié à chaque sens. |
| `--montant` | `10000` | Taille de l'ordre en euros, pour l'impact de marché (§ 3). |
| `--sans-ttf` | — | Ignore la TTF, quel que soit le pays. Pour un compte non assujetti. |
| `--sigma-residuel` | `30` | Volatilité résiduelle en %/an, pour le § 5. |
| `--csv` | — | Écrit le tableau des rotations. Sans l'argument, affichage seul. |

## Déroulé d'exécution

### 1. Le coût d'un aller-retour

Quatre termes, dont trois sont des paramètres et un seul est estimé :

| Terme | Achat | Vente | Nature |
|---|---|---|---|
| **TTF** | `--ttf` | — | taux **légal** |
| **Courtage** | `--courtage` | `--courtage` | clause de **contrat** |
| **Demi-spread** | `--spread / 2` | `--spread / 2` | **observable** |
| **Impact de marché** | § 3 | § 3 | **estimé** — le seul |

$$\text{aller-retour} = \text{TTF} + 2\,\text{courtage} + \text{spread} + 2\,\text{impact}$$

Avec les valeurs par défaut et un impact nul : $0{,}30 + 0{,}20 + 0{,}03 =
\mathbf{0{,}53\,\%}$.

### 2. L'assujettissement à la TTF, déduit et non supposé

Deux conditions cumulatives, toutes deux lisibles dans les données :

- la société est **immatriculée en France** — champ `country` de yfinance ;
- sa **capitalisation dépasse 1 milliard d'euros** — champ `marketCap`.

Le script les évalue par ticker et l'annonce. Exemples mesurés :

| Valeur | Pays | Capitalisation | TTF |
|---|---|---|---|
| OR.PA, MC.PA, TTE.PA | France | > 100 Md | **assujetties** |
| **AIR.PA** | **Pays-Bas** | 160,7 Md | **exemptée** — Airbus SE est de droit néerlandais |
| **STLAP.PA** | **Pays-Bas** | 17,6 Md | exemptée |
| **ATO.PA** | France | **0,6 Md** | **exemptée** — sous le seuil |

> ⚠️ **Cette déduction est une approximation, et le script le dit.** Le périmètre
> réel de la TTF est fixé par une **liste officielle publiée chaque année** par
> l'administration fiscale, arrêtée sur la capitalisation au 1ᵉʳ décembre de
> l'année précédente. Le script raisonne sur la capitalisation **du jour**. Une
> valeur qui vient de franchir le seuil dans un sens ou dans l'autre sera classée
> à tort pendant un an. Pour un chiffrage engageant, se reporter à la liste.

### 3. L'impact de marché — le seul terme estimé

Loi en racine carrée, la forme usuelle :

$$\text{impact} = Y\,\sigma_{\text{jour}}\sqrt{\frac{Q}{V}}$$

où $Q$ est la taille de l'ordre en titres, $V$ le volume quotidien médian sur un
an, $\sigma_{\text{jour}}$ la volatilité quotidienne des rendements, et $Y = 0{,}5$
un coefficient conventionnel.

$Q/V$ est lu depuis le CSV de `docs/raw/quotes/` s'il existe pour le ticker ;
sinon l'impact est **non calculé** et la colonne reste vide plutôt que d'être
posée à zéro — un impact inconnu n'est pas un impact nul.

> **Pour un particulier, ce terme est négligeable et le script le montre.** Un
> ordre de 10 000 € sur une valeur qui échange 300 M€ par jour donne
> $Q/V \approx 3\cdot10^{-5}$, donc un impact de l'ordre du point de base. Il
> n'est là que pour rendre visible le seuil à partir duquel il cesse de l'être.

### 4. Le tableau des rotations

Le freinage annuel vaut $n \times \text{aller-retour}$, où $n$ est le nombre
d'allers-retours par an. Rotations tabulées : quotidienne (252), hebdomadaire
(52), mensuelle (12), trimestrielle (4), annuelle (1), triennale (0,33).

Aux valeurs par défaut :

| Rotation | Freinage annuel |
|---|---|
| quotidienne | 133,6 % |
| hebdomadaire | **27,6 %** |
| mensuelle | **6,4 %** |
| trimestrielle | 2,1 % |
| annuelle | 0,5 % |

### 5. Le verdict qui ferme la boucle — combien d'années pour le prouver

C'est la sortie qui donne son sens au reste. Pour chaque rotation, le script
calcule :

1. **l'alpha de seuil** — celui qui couvre tout juste les frais, donc égal au
   freinage annuel ;
2. **l'horizon nécessaire pour distinguer cet alpha de zéro**, par la formule du
   [module 3 du cours alpha](../docs/raw/concept/semestre4/alpha/03-l-horizon-necessaire.md) :

$$Y = \left(\frac{1{,}96\,\sigma_\varepsilon}{\alpha}\right)^2$$

Aux valeurs par défaut, avec $\sigma_\varepsilon = 30\,\%$ :

| Rotation | Alpha de seuil | Années pour le prouver |
|---|---|---|
| quotidienne | 133,6 % | 0,2 |
| hebdomadaire | 27,6 % | **4,6** |
| mensuelle | 6,4 % | **85,5** |
| trimestrielle | 2,1 % | 769,3 |
| annuelle | 0,5 % | 12 308 |
| triennale | 0,2 % | 110 776 |

> 🔑 **Lecture du tableau, et c'est un piège inversé.** Plus la rotation est
> rapide, plus l'alpha de seuil est élevé, donc plus il serait *facile* à
> détecter — mais il devient absurdement grand : aucune règle ne produit 27,6 %
> d'alpha par an. Plus la rotation est lente, plus le seuil devient atteignable,
> mais il tombe alors sous le plancher du mesurable. **Il n'existe aucune
> rotation où une règle puisse à la fois couvrir ses frais et le démontrer** avec
> une volatilité résiduelle de 30 %. C'est l'argument central en faveur du
> portefeuille diversifié, qui abaisse $\sigma_\varepsilon$.

### 6. Résumé console

```
Bareme, par aller-retour
  TTF (achat)                       0,300 %
  Courtage (2 sens)                 0,200 %
  Spread (1 spread complet)         0,030 %
  Impact de marche              non calcule   (mode bareme)
  ─────────────────────────────────────────
  Aller-retour                      0,530 %
```

Puis le tableau du § 4, celui du § 5, et — en mode ticker — une ligne par valeur :

```
AIR.PA
  TTF               : exemptee (immatriculee Netherlands)
  Impact de marche  : 0,0190 % par sens — 485 titres sur 1 463 472 echanges (0.0331 % du volume)
  Aller-retour      : 0,268 % pour un ordre de 50 000 €

OR.PA
  TTF               : assujettie (France, capitalisation 206,9 Md)
  Impact de marche  : non calcule — aucun CSV dans docs/raw/quotes/
  Aller-retour      : 0,530 % pour un ordre de 50 000 €

ATO.PA
  TTF               : exemptee (capitalisation 0,6 Md < 1,0 Md)
  Impact de marche  : non calcule — aucun CSV dans docs/raw/quotes/
  Aller-retour      : 0,230 % pour un ordre de 50 000 €
```

> 🔑 **Airbus coûte moitié moins cher à traiter que L'Oréal** — $0{,}268\,\%$
> contre $0{,}530\,\%$ — pour la seule raison qu'elle est de droit néerlandais.
> Une différence de coût de cette taille entre deux valeurs du même indice ne se
> devine pas : elle se calcule, et elle change le classement de tout écran à
> rotation soutenue.

### 7. Cas limites

- **Aucun ticker** : mode barème, aucun appel réseau, aucun CSV lu.
- **Ticker sans CSV dans `docs/raw/quotes/`** : impact non calculé, colonne vide,
  message sur `stderr`. Les autres termes restent valables.
- **`country` ou `marketCap` absents** : assujettissement **indéterminé**, signalé
  comme tel. Le script ne tranche pas à la place de l'utilisateur, et retient la
  TTF par prudence en le disant.
- **`--sans-ttf`** : force l'exemption, quel que soit le pays.
- **Paramètres négatifs** : refusés en sortie 1.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète. |
| `1` | Paramètre négatif. |

## Fonctions internes

- `assujetti_ttf(ticker)` — les deux conditions du § 2 ; rend `True`, `False` ou
  `None` quand la donnée manque.
- `impact_marche(ticker, montant, coefficient)` — le § 3, depuis le CSV local.
- `aller_retour(ttf, courtage, spread, impact)` — la somme du § 1.
- `horizon(alpha, sigma_residuel)` — la formule du § 5.
- `main()` — CLI, barème, tableaux, résumé.

## Constantes

- `ROTATIONS` — les six rotations tabulées et leur nombre d'allers-retours.
- `SEUIL_TTF_MDS = 1.0` — le seuil de capitalisation, en milliards d'euros.
- `PAYS_TTF = "France"` — le pays d'immatriculation assujetti.
- `COEFFICIENT_IMPACT = 0.5` — le $Y$ de la loi en racine carrée.
- `REPERTOIRE_QUOTES = Path("docs/raw/quotes")`.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
