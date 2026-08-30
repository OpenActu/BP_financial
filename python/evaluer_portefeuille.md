# evaluer_portefeuille.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `evaluer_portefeuille.py`, étape par
étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du script
doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Mesurer l'alpha d'un **panier** de valeurs contre son indice — et non celui d'un
titre isolé.

C'est un changement de question, pas d'outillage, et il change tout. Le
[module 3 du cours alpha](../docs/raw/concept/semestre4/alpha/03-l-horizon-necessaire.md)
établit que l'horizon nécessaire vaut
$Y = (1{,}96\,\sigma_\varepsilon/\alpha)^2$ : tout se joue sur la volatilité
résiduelle, que la diversification abaisse.

> 🔑 **« Cette valeur a-t-elle de l'alpha ? » n'a pas de réponse. « Cette règle
> a-t-elle de l'alpha ? » en a une.** Mesuré sur 1281 séances communes,
> 2021-2025, contre le CAC 40 : $\sigma_\varepsilon$ passe de **18,1 %/an** en
> moyenne sur dix titres isolés à **4,2 %/an** pour le panier équipondéré des
> mêmes dix. L'horizon pour distinguer un alpha de 3 % tombe de ~140 ans à
> **8 ans**.

> ⚠️ **Le gain n'est pas gratuit.** Quand le panier tend vers l'indice entier,
> $\sigma_\varepsilon$ tend vers zéro — **et l'alpha aussi**. Dix valeurs sur
> quarante n'ont pas beaucoup de latitude pour dévier. Le script publie donc
> toujours l'alpha **et** son intervalle, jamais l'horizon seul.

## Dépendances

- `yfinance` uniquement si `--telecharger` est passé ; sinon **aucun réseau**.
- `p_valeur_student()` de [`import_societe.py`](import_societe.md) et
  `aller_retour()` / `assujetti_ttf()` de
  [`couts_transaction.py`](couts_transaction.md) — réutilisés, jamais redupliqués.
- Modules standard : `argparse`, `csv`, `math`, `statistics`, `sys`, `pathlib`.

## Invocation

```bash
python python/evaluer_portefeuille.py AIR.PA OR.PA MC.PA SAN.PA TTE.PA
python python/evaluer_portefeuille.py AIR.PA OR.PA MC.PA --indice '^FCHI' --rebalancement mensuel
python python/evaluer_portefeuille.py --fichier panier.txt --debut 2021-01-01
python python/evaluer_portefeuille.py AIR.PA OR.PA --telecharger --csv resultat.csv
```

### Arguments

| Argument | Défaut | Rôle |
|---|---|---|
| `tickers` | — | Les valeurs du panier. Sans argument ni `--fichier`, invite interactive. |
| `--fichier` | — | Fichier texte, un ticker par ligne (`#` = commentaire). |
| `--indice` | `^FCHI` | Indice de référence. |
| `--debut`, `--fin` | l'intersection disponible | Bornes `AAAA-MM-JJ`. |
| `--rebalancement` | `mensuel` | `quotidien`, `mensuel`, `trimestriel`, `annuel` ou `aucun`. |
| `--telecharger` | — | Récupère les séries manquantes au lieu d'échouer (§ 1). |
| `--sans-couts` | — | N'applique aucun coût. Le résultat est alors **brut**, et dit comme tel. |
| `--csv` | — | Écrit le tableau titre par titre et la ligne du panier. |

## Déroulé d'exécution

### 1. Les séries

Chaque valeur est lue dans `docs/raw/quotes/{TICKER}_*.csv`, le fichier le plus
récent couvrant la période. **Aucune série n'est téléchargée par défaut** : si une
manque, le script affiche la commande `import_societe.py` exacte qui la produit,
puis **sort en 1**. `--telecharger` lève cette exigence.

Les séries sont ensuite **alignées sur leurs dates communes**. Le script annonce
combien de séances survivent à l'intersection : un panier dont une valeur a un
calendrier lacunaire perd des séances pour tout le monde.

### 2. Le rendement du panier

Rendements arithmétiques quotidiens $r_{i,t} = P_{i,t}/P_{i,t-1} - 1$ sur `Close`.

Le panier est **équipondéré**. Entre deux rebalancements, les poids **dérivent**
avec les cours : le script les fait dériver explicitement plutôt que de moyenner
naïvement les rendements, faute de quoi il supposerait un rebalancement quotidien
sans le dire.

$$r_{p,t} = \sum_i w_{i,t-1}\,r_{i,t}, \qquad
w_{i,t} = \frac{w_{i,t-1}(1+r_{i,t})}{\sum_j w_{j,t-1}(1+r_{j,t})}$$

À chaque date de rebalancement, les poids sont ramenés à $1/N$.

### 3. La rotation, mesurée et non supposée

À chaque rebalancement, la **rotation à sens unique** vaut

$$\tau = \tfrac12 \sum_i \bigl|w_{i,\text{avant}} - \tfrac1N\bigr|$$

C'est la fraction du portefeuille effectivement vendue, donc rachetée. Elle est
**mesurée sur la dérive réelle des poids**, pas postulée : un panier de valeurs
très corrélées dérive peu et coûte peu.

Le coût de l'événement vaut $\tau \times (\text{coût achat} + \text{coût vente})$,
les deux termes venant de [`couts_transaction.py`](couts_transaction.md) — dont
la TTF, **évaluée valeur par valeur** : un panier contenant AIR.PA (de droit
néerlandais) coûte moins cher qu'un panier de sociétés françaises.

Le coût est retranché du rendement du panier **le jour du rebalancement**, ce qui
donne une série *nette*. Le script publie les deux, brute et nette.

### 4. La régression, et les deux volatilités résiduelles

Régression des rendements du panier sur ceux de l'indice, exactement celle du § 2
de l'agent [`trading`](../.claude/agents/trading.md) :

$$r_{p,t} = \alpha + \beta\,r_{m,t} + \varepsilon_t$$

avec $\operatorname{SE}(\alpha)$ par le levier, le test de Student à $n-2$ degrés
de liberté, et l'annualisation par 252.

**Le script calcule aussi la même régression pour chaque titre pris isolément**,
et met les deux en regard. C'est la mesure du gain de diversification, et elle
est le cœur de la sortie :

| | $\sigma_\varepsilon$ | Années pour prouver 3 % |
|---|---|---|
| moyenne des titres isolés | 18,1 %/an | ~140 |
| panier équipondéré, N=10 | **4,2 %/an** | **8** |

### 4bis. Le biais de l'indice nu, corrigé et non seulement signalé

`Close` est **ajustée des dividendes**, `^FCHI` est un indice **nu**. Comparer
les deux fabrique de l'alpha à partir de rien, et l'effet est massif : sur le
panier de dix valeurs 2021-2025, l'alpha brut mesuré vaut $+7{,}22\,\%$/an et le
rendement du dividende du panier **$4{,}71\,\%$/an**. Les deux tiers de l'« alpha »
sont un artefact de convention.

> ⚠️ **La signaler en pied de page ne suffit pas** : le verdict s'en trouve
> renversé, et un lecteur pressé ne lirait que le verdict.

Le script calcule donc le rendement du dividende du panier depuis la colonne
`Dividends` des CSV, et publie un **alpha prudent** :

$$lpha_{	ext{prudent}} = lpha_{	ext{net}} - 	ext{rendement du dividende du panier}$$

**C'est une borne basse, délibérément sur-corrigée.** L'indice, s'il était en
rendement total, aurait lui aussi rapporté ses propres dividendes ; retrancher la
totalité du rendement du panier retire donc trop. La conséquence est celle qu'on
veut : **si l'alpha prudent reste significatif, la conclusion est robuste** ; s'il
ne l'est pas — cas le plus fréquent — on n'a rien démontré.

Le **verdict du § 5 porte sur l'alpha prudent**, jamais sur le brut.

Un indice en rendement total lèverait cette approximation, mais `^FCHIGR` n'est
pas servi par yfinance. À noter pour qui voudrait comparer : `^GDAXI`, le DAX,
est un indice de rendement total par construction, et ne souffre donc pas de ce
biais.

### 5. Le verdict — trois nombres, jamais un seul

1. **L'alpha annualisé net et son IC95.** S'il contient zéro, le script écrit
   *indiscernable de zéro* et **ne commente pas son signe**.
2. **L'horizon** $Y = (1{,}96\,\sigma_\varepsilon/\alpha)^2$ nécessaire pour
   distinguer cet alpha-là de zéro, comparé à la longueur réelle de l'échantillon.
3. **Le freinage annuel** dû aux coûts, et l'alpha **brut** qu'il aurait fallu
   pour l'absorber.

> ⚠️ **Un alpha net positif sur un échantillon plus court que son horizon n'est
> pas un résultat.** Le script le dit explicitement quand c'est le cas — et c'est
> le cas presque toujours.

### 6. Résumé console

```
Panier de 10 valeurs · indice ^FCHI · 1281 seances communes (2021-01-04 -> 2025-12-31)
Rebalancement mensuel · 60 evenements · rotation moyenne 4,21 % par evenement

Titre par titre
  ticker      beta   sigma_eps    alpha/an        IC95
  AIR.PA      1,26      20,3 %      ...

Panier equipondere
  beta 1,03 · R2 0,962 · sigma_eps 4,2 %/an
  alpha brut  +1,42 %/an   IC95 [-0,89 ; +3,73]  indiscernable de zero
  couts       -0,53 %/an   (rotation 4,21 % x 12 evenements)
  alpha net   +0,89 %/an   IC95 [-1,42 ; +3,20]  indiscernable de zero

  Gain de diversification : sigma_eps 18,1 % -> 4,2 %/an
  Horizon pour prouver cet alpha : 86 ans — echantillon de 5,1 ans
  VERDICT : echantillon 17 fois trop court. Ce n'est pas un resultat.
```

### 7. Cas limites

- **Une seule valeur** : accepté, mais le script signale qu'il n'y a alors aucun
  gain de diversification et que le résultat est celui d'un titre isolé.
- **Série manquante** : sortie **1**, avec la commande exacte à lancer.
- ⚠️ **CSV local ne couvrant pas la période demandée** : traité comme
  **manquant**, avec la mention de ce qu'il couvre réellement. Sans ce
  contrôle, un panier mélangeant un fichier 2019-2021 et des séries
  2021-2025 verrait son échantillon tronqué à l'intersection — **en
  silence**, ce qui est le pire des cas : le résultat reste plausible et
  repose sur cinq fois moins de séances qu'annoncé.
- **Moins de 60 séances communes** : sortie **1** — une régression sur si peu de
  points ne dit rien.
- **Indice absent des CSV** : même traitement qu'une valeur manquante ; rappel que
  le `^` exige des guillemets en ligne de commande.
- **`--rebalancement aucun`** : achat initial puis dérive libre. Rotation nulle,
  coûts limités à l'entrée, et le panier cesse d'être équipondéré — dit tel quel.
- **`--sans-couts`** : la série nette est identique à la brute, et le résumé porte
  la mention *brut, coûts non appliqués*.

## Ce que ce script ne fait pas

- **Aucune recommandation.** Il mesure l'alpha d'un panier donné ; il ne choisit
  pas les valeurs, ne dimensionne aucune position et ne conseille rien.
- **Aucune sélection.** Le panier est fourni, jamais construit par le script — le
  construire à partir des données reviendrait à choisir après avoir vu, ce que le
  [module 3 du cours trading](../docs/raw/concept/semestre4/trading/03-la-regle-ecrite-a-l-avance.md)
  interdit.
- **Aucun rendement de dividende ajouté** : `Close` de yfinance est déjà ajustée,
  l'indice `^FCHI` ne l'est pas — le biais est rappelé dans le résumé.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète. |
| `1` | Panier vide, série manquante sans `--telecharger`, ou moins de 60 séances communes. |

## Fonctions internes

- `charger(ticker, telecharger)` — la série de clôtures, depuis `docs/raw/quotes/`
  ou téléchargée.
- `aligner(series)` — l'intersection des dates.
- `serie_panier(rendements, rebalancements, couts_unitaires)` — le § 2 et le § 3 ;
  rend la série brute, la série nette et la rotation moyenne.
- `regression(rp, rm)` — le § 4 ; rend $\alpha$, $\beta$, IC95, $R^2$,
  $\sigma_\varepsilon$.
- `horizon(alpha, sigma)` — la formule du § 5.
- `main()` — CLI, tableaux, verdict.

## Constantes

- `INDICE_DEFAUT = "^FCHI"`.
- `SEANCES_MINIMALES = 60`.
- `JOURS_AN = 252`.
- `REBALANCEMENTS` — la correspondance nom → périodicité.
- `REPERTOIRE_QUOTES = Path("docs/raw/quotes")`.

Chemins **relatifs** au répertoire courant : lancer le script depuis la racine du
dépôt.
