# historique_sbf250.py — miroir d'exécution

Ce document décrit **exactement** ce que fait `historique_sbf250.py`, étape par
étape, dans l'ordre du déroulement. Il fait autorité : toute évolution du script
doit d'abord être décrite ici (voir `/python-sync`).

## Rôle

Récupérer l'historique de cotation d'une société du SBF 250 sur Yahoo Finance,
l'enrichir d'indicateurs statistiques glissants (dont un test de tendance de
Student), afficher un résumé en console et enregistrer le tout en CSV.

## Dépendances

- `yfinance` (`pip install yfinance`), qui embarque `pandas`.
- Modules standard : `argparse`, `math`, `sys`, `pathlib`.

## Invocation

```bash
python python/historique_sbf250.py                       # mode interactif
python python/historique_sbf250.py AIR.PA
python python/historique_sbf250.py AIR.PA --periode 5y
python python/historique_sbf250.py AIR.PA --debut 2023-01-01 --fin 2023-12-31
python python/historique_sbf250.py AIR.PA --csv airbus.csv
python python/historique_sbf250.py AIR.PA --alpha 0.01        # test plus exigeant
```

### Arguments

| Argument                          | Défaut | Rôle                                                                                                                          |
| --------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `ticker` (positionnel, optionnel) | —      | Ticker Yahoo Finance. Les valeurs de Paris se terminent par `.PA` (`AIR.PA`, `MC.PA`, `TTE.PA`, `SAN.PA`, `BNP.PA`, `AI.PA`). |
| `--periode`                       | `1y`   | `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`.                                                       |
| `--debut`                         | —      | Date de début `AAAA-MM-JJ`. **Prioritaire sur `--periode`.**                                                                  |
| `--fin`                           | —      | Date de fin `AAAA-MM-JJ`.                                                                                                     |
| `--intervalle`                    | `1d`   | `1d`, `1wk`, `1mo`, `1h`, …                                                                                                   |
| `--alpha`                         | `0.05` | Seuil du test de tendance bilatéral (§ étape 4). $H_0$ est rejetée quand `P_n < alpha`.                                        |
| `--csv`                           | —      | Chemin du CSV de sortie. Sans cet argument, le chemin est calculé (voir § Export CSV).                                        |

## Déroulé d'exécution

### 1. Lecture des arguments

`argparse` analyse la ligne de commande. Si `ticker` est absent, le script
demande le ticker en interactif (`Ticker (ex AIR.PA) : `) et applique un `strip()`.
Si la saisie est vide : message `Aucun ticker fourni.` sur `stderr` et **sortie 1**.

### 2. Récupération de l'historique — `recuperer_historique()`

- Construit `yf.Ticker(ticker)`.
- Si `--debut` **ou** `--fin` est fourni : appel `history(start=debut, end=fin, interval=intervalle)`.
- Sinon : appel `history(period=periode, interval=intervalle)`.
- Si le DataFrame renvoyé est vide : lève `ValueError` (« Aucune donnée pour … »,
  avec rappel du suffixe `.PA`).
- Toute exception remontée est capturée dans `main()` : `Erreur : …` sur `stderr`
  et **sortie 1**.

Le DataFrame est indexé par date et contient les colonnes de yfinance :
`Open`, `High`, `Low`, `Close`, `Volume`, `Dividends`, `Stock Splits`
(et éventuellement `Capital Gains`).

### 3. Colonne `INDICE`

Insérée en position 0 : compteur de séances `1, 2, 3, …, n` dans l'ordre
chronologique. Elle sert de variable temporelle pour la corrélation.

### 4. Indicateurs glissants, pour chaque fenêtre `n ∈ {20, 120}`

Fenêtre `rolling(window=n, min_periods=n)` sur `Close` — donc les `n-1`
premières lignes valent `NaN` (cellules vides dans le CSV).

Ces indicateurs transposent à une fenêtre glissante le modèle de droite ajustée
décrit dans `docs/raw/concept/modele/` (étapes 6 et 7). Sur chaque fenêtre de `n`
séances, les observations sont $V_i = \text{Close}$ aux instants régulièrement
espacés $T_i = i$, $i = 1,\dots,n$.

| Colonne | Modèle | Calcul |
|---|---|---|
| `E_n` | $E(V)$ | moyenne glissante de `Close` sur `n` séances |
| `VAR_n` | $\operatorname{Var}(V)$ | variance glissante **de population** (`ddof=0`) — même convention que $\operatorname{Var}(T)=\frac{n^2-1}{12}$ dans le modèle |
| `CORR_n` | $\rho_{V,T}$ | corrélation de Pearson glissante entre `Close` et `INDICE` (≈ +1 hausse régulière, ≈ −1 baisse régulière) |
| `VAL_n` | $f(n)$ | droite ajustée évaluée au **dernier point de la fenêtre** (voir ci-dessous) |
| `T_n` | $t$ | statistique de Student du test de tendance (voir ci-dessous) |
| `P_n` | — | $p$-valeur bilatérale associée, à $n-2$ degrés de liberté |
| `TEND_n` | — | verdict signé du test au seuil `alpha` : `+1`, `-1` ou `0` |

`INDICE` est un compteur global, mais la corrélation est invariante par
translation de la variable temporelle : sur une fenêtre, `CORR_n` vaut bien
$\rho_{V,T}$ avec $T_i = i$.

#### `VAL_n` — la droite ajustée évaluée en `t = n`

Le modèle ([étape 6](../docs/raw/concept/modele/06-instants-regulierement-espaces.md),
[étape 7](../docs/raw/concept/modele/07-droite-ajustee.md)) pose

$$\phi(V) = \rho_{V,T}\sqrt{\frac{3\operatorname{Var}(V)}{n^2-1}},
\qquad f(t) = E(V) + \phi(V)\,(2t-n-1).$$

`VAL_n` est cette droite évaluée à $t = n$, c'est-à-dire à la séance courante,
la plus récente de la fenêtre : $f(n) = E(V) + \phi(V)\,(n-1)$. Soit

$$\boxed{\;\texttt{VAL\_n} \;=\; \texttt{E\_n} + \texttt{CORR\_n}\,(n-1)\,\sqrt{\frac{3\,\texttt{VAR\_n}}{n^2-1}}\;}$$

forme équivalente : $\texttt{E\_n} + \texttt{CORR\_n}\,\sqrt{3\,\texttt{VAR\_n}}\,\sqrt{\dfrac{n-1}{n+1}}$.

`VAL_n` extrapole donc la moyenne de la fenêtre jusqu'à la séance courante en
suivant la tendance ajustée : au-dessus de `E_n` quand le cours monte
($\rho_{V,T} > 0$), en dessous quand il baisse. Le facteur $\sqrt{\frac{n-1}{n+1}}$
vaut $\approx 0{,}951$ pour $n = 20$ et $\approx 0{,}992$ pour $n = 120$.

#### `T_n`, `P_n`, `TEND_n` — test de tendance de Student

Transposition de l'[étape 8](../docs/raw/concept/modele/08-test-de-tendance.md).
On teste, sur chaque fenêtre, l'hypothèse nulle $H_0 : r = 0$ (le niveau ne
dépend pas du temps) contre $H_1 : r \ne 0$, test **bilatéral**.

**`T_n` — statistique de test.** Sous $H_0$ elle suit exactement une loi de
Student à $n-2$ degrés de liberté :

$$\boxed{\;\texttt{T\_n} \;=\; \texttt{CORR\_n}\,\sqrt{\frac{n-2}{1-\texttt{CORR\_n}^{2}}}\;}$$

Degrés de liberté : $\nu = n - 2$, soit 18 pour $n = 20$ et 118 pour $n = 120$.
Si $|\texttt{CORR\_n}| = 1$ (fenêtre parfaitement alignée), `T_n` vaut $\pm\infty$
et `P_n` vaut 0.

**`P_n` — $p$-valeur bilatérale.** $P_n = \Pr\bigl(|T_\nu| > |\texttt{T\_n}|\bigr)$,
calculée par la fonction bêta incomplète régularisée :

$$\texttt{P\_n} = I_{\,\nu/(\nu+\texttt{T\_n}^2)}\!\left(\tfrac{\nu}{2},\,\tfrac12\right)$$

évaluée en Python pur (fraction continue de Lentz, cf. § Fonctions internes) —
aucune dépendance à `scipy`.

**`TEND_n` — verdict signé**, entier dans $\{-1, 0, +1\}$ :

| Valeur | Condition | Lecture |
|---|---|---|
| `+1` | `P_n < alpha` et `CORR_n > 0` | $H_0$ **rejetée**, tendance haussière significative |
| `-1` | `P_n < alpha` et `CORR_n < 0` | $H_0$ **rejetée**, tendance baissière significative |
| `0` | `P_n >= alpha` | $H_0$ **non rejetée** au seuil `alpha` |

`alpha` provient de `--alpha` (défaut `0.05`). Les `n-1` premières lignes de
chaque fenêtre sont `NaN` pour `T_n` et `P_n` ; `TEND_n` y vaut `0`.

> ⚠️ `TEND_n = 0` n'est **pas** une preuve d'absence de tendance : seulement le
> constat que la fenêtre ne permet pas de la distinguer du bruit. Et le test
> suppose des erreurs i.i.d. normales — hypothèse notoirement fausse sur une
> série de cours, où l'autocorrélation fait rejeter $H_0$ bien plus souvent que
> le seuil nominal (§ *Portée et limites* de l'étape 8). `TEND_n` est un
> indicateur descriptif, pas un test valide de la tendance d'un cours.

### 5. Colonne `CURR` — buy & hold, base 100

`CURR = 100 · Close / Close[première séance]`.
Performance d'une détention passive depuis le début de la période, base 100.

### 6. Colonne `BUY_120` — backtest de la stratégie, base 100

1. `ratio = Close / Close.shift(1)` — rendement brut d'une séance à l'autre.
2. `achete = (VAL_120 < VAL_20) & (TEND_20 == 1)` — on est investi une séance
   donnée si **les deux** conditions sont réunies :
   - la valeur de référence longue passe sous la valeur de référence courte
     (tendance courte plus favorable que la tendance longue) ;
   - le test de tendance sur la fenêtre courte rejette $H_0$ **dans le sens
     haussier** au seuil `alpha` (cf. `TEND_20`, étape 4).
3. `multiplicateur = ratio` si `achete`, sinon `1.0` (hors marché : capital figé).
4. `multiplicateur[première séance] = 1.0`.
5. `BUY_120 = 100 · cumprod(multiplicateur)`.

Le filtre de significativité écarte les séances où la configuration
`VAL_120 < VAL_20` n'est pas adossée à une tendance courte statistiquement
distinguable du bruit. Il rend donc la stratégie **dépendante de `--alpha`** :
un seuil plus exigeant réduit mécaniquement le nombre de séances investies.

Tant que `VAL_120` est `NaN` (les 119 premières séances), la comparaison est
fausse ; `TEND_20` y vaut `0` sur les 19 premières. Dans les deux cas le capital
reste hors marché, à 100.

### 7. Affichage console

Dans l'ordre :

```
Historique de {ticker} — {n} séances
Du {première date} au {dernière date}
Test de tendance bilatéral au seuil alpha = {alpha}

<tableau des colonnes ci-dessous ; 2 décimales, sauf P_20 et P_120 à 4>

Clôture initiale : {Close[0]}
Clôture finale   : {Close[-1]}
Variation        : {+/- x.xx} %
```

Colonnes affichées (celles réellement présentes, dans cet ordre) :
`INDICE`, `Open`, `High`, `Low`, `Close`, `Volume`,
`E_20`, `VAR_20`, `CORR_20`, `VAL_20`, `T_20`, `P_20`, `TEND_20`,
`E_120`, `VAR_120`, `CORR_120`, `VAL_120`, `T_120`, `P_120`, `TEND_120`,
`CURR`, `BUY_120`.

`Variation` = `(Close[-1] / Close[0] - 1) · 100`.

### 8. Export CSV

L'export est **toujours** effectué.

- Avec `--csv` : le chemin fourni est utilisé tel quel.
- Sans `--csv` : `docs/raw/quotes/{ticker}_{debut}_{fin}.csv`, où les `.` du
  ticker sont remplacés par `_` et où `debut`/`fin` sont les dates **réellement
  présentes** dans les données (`AAAA-MM-JJ`). Exemple : `AIR_PA_2023-01-03_2023-12-29.csv`.

Le répertoire parent est créé si nécessaire (`mkdir -p`). Le CSV contient
**toutes** les colonnes du DataFrame (y compris `Dividends` et `Stock Splits`),
non arrondies, l'index de dates en première colonne, les `NaN` en cellules vides.

Dernière ligne affichée : `Historique enregistré dans : {chemin}`.

`docs/raw/quotes/` est exclu du suivi git (`.gitignore`) : les CSV sont des
sorties régénérables, pas des sources.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète, CSV écrit. |
| `1` | Aucun ticker fourni, ou échec de récupération (ticker inconnu, période vide, erreur réseau). |

## Fonctions internes

Outre `recuperer_historique()` et `main()`, le script embarque le strict
nécessaire pour la loi de Student, afin de ne dépendre que de `yfinance` :

- `_beta_incomplete_reg(x, a, b)` — fonction bêta incomplète régularisée
  $I_x(a,b)$, évaluée par la fraction continue de Lentz (avec la relation de
  symétrie $I_x(a,b) = 1 - I_{1-x}(b,a)$ quand $x > \frac{a+1}{a+b+2}$, qui
  garantit la convergence). Précision visée : $10^{-12}$.
- `p_valeur_student(t, ddl)` — $p$-valeur **bilatérale**
  $\Pr(|T_\nu| > |t|) = I_{\,\nu/(\nu+t^2)}(\nu/2,\ 1/2)$.
  Renvoie `NaN` si `t` est `NaN`, et `0.0` si `t` est infini.

## Constantes

- `REPERTOIRE_CSV_DEFAUT = Path("docs/raw/quotes")` — chemin **relatif** au
  répertoire courant : lancer le script depuis la racine du dépôt.
