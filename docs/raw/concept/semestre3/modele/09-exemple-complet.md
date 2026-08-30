# Étape 9 — Exemple complet d'évaluation

**Prérequis :** [étapes 1 à 8](../../../modele.md#plan-de-la-preuve).
**Ce qu'on établit ici :** rien de nouveau — les huit étapes précédentes, exécutées sur une série réelle de $20$ points, contrôles croisés et diagnostics compris.

---

## 9.0 — Les données

Clôtures d'**Airbus (AIR.PA)** sur les 20 premières séances de 2020, colonne `Close` du fichier `docs/raw/quotes/AIR_PA_2020-01-02_2023-12-29.csv` produit par [`python/import_societe.py`](../../../../../python/import_societe.md). Les instants sont les rangs de séance, $T_i = i$ pour $i = 1,\dots,20$ — c'est bien le cas de l'[étape 6](06-instants-regulierement-espaces.md), et non les dates calendaires : les week-ends ne comptent pas.

> **Convention de l'exemple.** Les cours sont **arrondis au centime**, et *tous* les calculs ci-dessous portent sur ces valeurs arrondies, de sorte que chaque nombre soit reproductible à partir du tableau. Le § 9.9 mesure l'écart avec les colonnes que le script calcule sur les cours non arrondis.

| $i$ | Date | $V_i$ | | $i$ | Date | $V_i$ |
|---|---|---|---|---|---|---|
| 1 | 2020-01-02 | 122,50 | | 11 | 2020-01-16 | 122,39 |
| 2 | 2020-01-03 | 122,97 | | 12 | 2020-01-17 | 125,49 |
| 3 | 2020-01-06 | 122,44 | | 13 | 2020-01-20 | 126,51 |
| 4 | 2020-01-07 | **121,10** | | 14 | 2020-01-21 | 125,14 |
| 5 | 2020-01-08 | 123,28 | | 15 | 2020-01-22 | 126,59 |
| 6 | 2020-01-09 | 123,78 | | 16 | 2020-01-23 | 124,59 |
| 7 | 2020-01-10 | 123,32 | | 17 | 2020-01-24 | **127,52** |
| 8 | 2020-01-13 | 123,96 | | 18 | 2020-01-27 | 121,93 |
| 9 | 2020-01-14 | 123,95 | | 19 | 2020-01-28 | 123,16 |
| 10 | 2020-01-15 | 123,17 | | 20 | 2020-01-29 | 125,28 |

Minimum $121{,}10$ ($i=4$), maximum $127{,}52$ ($i=17$), amplitude $6{,}42$ soit $5{,}2\,\%$ du niveau.

## 9.1 — Moments empiriques

Variances **de population** ($\div n$), même convention que $\operatorname{Var}(T)$.

| Grandeur | Valeur exacte | Valeur approchée |
| --- | --- | --- |
| $E(T)=\frac{n+1}{2}$ | $\frac{21}{2}$ | $10{,}5$ |
| $\operatorname{Var}(T)=\frac{n^2-1}{12}$ | $\frac{133}{4}$ | $33{,}25$ |
| $\sigma_T$ | — | $5{,}766281$ |
| $E(V)$ | $\frac{2479{,}07}{20}$ | $123{,}953500$ |
| $\operatorname{Var}(V)$ | — | $2{,}716043$ |
| $\sigma_V$ | — | $1{,}648042$ |
| $\operatorname{Cov}(V,T)$ | — | $5{,}022250$ |

## 9.2 — [Étape 4](04-forme-canonique.md) : pente, ordonnée, variance résiduelle

$$r_{\min}=\frac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)}=\frac{5{,}022250}{33{,}25}\approx 0{,}151045$$
$$v_{0,\min}=E(V)-r_{\min}E(T)=123{,}953500-10{,}5\times0{,}151045\approx 122{,}367526$$
$$\operatorname{Var}(\hat e)_{\min}=\operatorname{Var}(V)-\frac{\operatorname{Cov}(V,T)^2}{\operatorname{Var}(T)}=2{,}716043-0{,}758586\approx 1{,}957456$$

La pente vaut donc **$+0{,}151$ € par séance**.

## 9.3 — [Étape 5](05-coefficient-de-correlation.md) : corrélation et décomposition

$$\rho_{V,T}^{2}=\frac{0{,}758586}{2{,}716043}\approx 0{,}279298 \qquad\Longrightarrow\qquad \rho_{V,T}\approx +0{,}528487$$

*Contrôle par la voie de l'étape 5 :*
$\operatorname{Var}(V)\bigl(1-\rho^2\bigr)=2{,}716043\times0{,}720702=1{,}957456$ ✓

$$\underbrace{2{,}716043}_{\text{totale}} \;=\; \underbrace{r_{\min}^{2}\operatorname{Var}(T)=0{,}758586}_{\text{expliquée},\;R^2=27{,}9\,\%} \;+\; \underbrace{1{,}957456}_{\text{résiduelle}}$$

La tendance n'explique que **28 %** de la dispersion : moins que dans un exemple d'école, et c'est normal — un cours de bourse est d'abord du bruit.

## 9.4 — [Étape 6](06-instants-regulierement-espaces.md) : forme en $\phi(V)$

$$\phi(V)=\rho_{V,T}\sqrt{\frac{3\operatorname{Var}(V)}{n^2-1}} = 0{,}528487\times\sqrt{\frac{3\times2{,}716043}{399}} = 0{,}528487\times 0{,}142903 \approx 0{,}075523$$

*Contrôles croisés :* $r_{\min}=2\phi=0{,}151045$ ✓ et $v_{0,\min}=E(V)-\phi\,(n+1)=123{,}953500-21\times0{,}075523=122{,}367526$ ✓

## 9.5 — [Étape 7](07-droite-ajustee.md) : droite ajustée et résidus

$$f(t)=122{,}367526+0{,}151045\,t \;=\; 123{,}953500+0{,}075523\,(2t-21)$$

| $i$ | $V_i$ | $f(i)$ | $\hat e_i$ | | $i$ | $V_i$ | $f(i)$ | $\hat e_i$ |
|---|---|---|---|---|---|---|---|---|
| 1 | 122,50 | 122,519 | −0,019 | | 11 | 122,39 | 124,029 | −1,639 |
| 2 | 122,97 | 122,670 | +0,300 | | 12 | 125,49 | 124,180 | +1,310 |
| 3 | 122,44 | 122,821 | −0,381 | | 13 | 126,51 | 124,331 | +2,179 |
| 4 | 121,10 | 122,972 | −1,872 | | 14 | 125,14 | 124,482 | +0,658 |
| 5 | 123,28 | 123,123 | +0,157 | | 15 | 126,59 | 124,633 | +1,957 |
| 6 | 123,78 | 123,274 | +0,506 | | 16 | 124,59 | 124,784 | −0,194 |
| 7 | 123,32 | 123,425 | −0,105 | | 17 | 127,52 | 124,935 | **+2,585** |
| 8 | 123,96 | 123,576 | +0,384 | | 18 | 121,93 | 125,086 | **−3,156** |
| 9 | 123,95 | 123,727 | +0,223 | | 19 | 123,16 | 125,237 | −2,077 |
| 10 | 123,17 | 123,878 | −0,708 | | 20 | 125,28 | 125,388 | −0,108 |

*Contrôles :* $\sum_i \hat e_i = 0$ exactement ([étape 1](01-elimination-de-l-ordonnee.md)) ✓ et $\frac1{20}\sum_i \hat e_i^{\,2} = 1{,}957456$ ✓

Les deux résidus extrêmes sont **consécutifs** : $+2{,}59$ le 24 janvier, $-3{,}16$ le 27 — une chute de $5{,}59$ € en une séance, soit $4{,}4\,\%$, sur laquelle la droite ne peut rien.

## 9.6 — [Étape 8](08-test-de-tendance.md) : le test

$$t = \rho_{V,T}\sqrt{\frac{n-2}{1-\rho_{V,T}^{2}}} = 0{,}528487\times\sqrt{\frac{18}{0{,}720702}} = 0{,}528487\times 4{,}997564 = \mathbf{2{,}6411}$$

| Élément | Valeur |
| --- | --- |
| Loi sous $H_0$ | Student à $n-2=18$ ddl |
| Valeur critique bilatérale à 5 % | $t_{18;\,0{,}975}=2{,}1009$ |
| **Décision** | $2{,}6411 > 2{,}1009$ → **rejet de $H_0$** |
| $p$-valeur bilatérale | $0{,}0166$ |
| Forme $F$ | $t^{2}=6{,}976 > F_{0{,}95}(1,18)=4{,}414$ ✓ |

**Intervalle de confiance sur la pente** — la partie qui compte :

$$\operatorname{SE}(r_{\min})=\sqrt{\frac{12\times2{,}716043\times0{,}720702}{18\times399}}=0{,}057189$$
$$\text{IC}_{95\%}(r) = 0{,}151045 \pm 2{,}1009\times0{,}057189 = [\,0{,}0309\;;\;0{,}2712\,]$$

## 9.7 — Diagnostics

| Contrôle | Valeur | Lecture |
|---|---|---|
| Durbin–Watson | $1{,}870$ | Pas d'autocorrélation détectée ($\hat\rho_1=+0{,}065$) — voir la réserve 3 |
| Mann–Kendall (non paramétrique) | $S=72$, $z=2{,}304$, $p=0{,}0212$ | **Même conclusion**, sans hypothèse de normalité |
| Pente de Sen (robuste) | $0{,}1688$ | Un peu plus forte que $r_{\min}=0{,}1510$, même ordre |

La convergence des trois approches est le véritable argument : si Student rejetait et que Mann–Kendall ne rejetait pas, on saurait que le résultat tient à la normalité plutôt qu'aux données.

## 9.8 — Analyse de sensibilité (retrait d'un point)

Régression refaite en retirant chaque point tour à tour, les autres gardant leur rang d'origine.

| Point retiré | $r_{\min}$ | $R^2$ | $t$ | $p$ | Décision à 5 % |
|---|---|---|---|---|---|
| $i=1$ (122,50) | 0,1507 | 0,249 | 2,371 | 0,0298 | ✅ |
| $i=2$ (122,97) | 0,1556 | 0,268 | 2,492 | 0,0233 | ✅ |
| $i=3$ (122,44) | 0,1461 | 0,249 | 2,374 | 0,0296 | ✅ |
| $i=4$ (121,10) | 0,1304 | 0,231 | 2,258 | 0,0374 | ✅ |
| $i=5$ (123,28) | 0,1525 | 0,273 | 2,529 | 0,0216 | ✅ |
| $i=6$ (123,78) | 0,1548 | 0,284 | 2,597 | 0,0188 | ✅ |
| $i=7$ (123,32) | 0,1505 | 0,274 | 2,532 | 0,0215 | ✅ |
| $i=8$ (123,96) | 0,1526 | 0,282 | 2,585 | 0,0193 | ✅ |
| $i=9$ (123,95) | 0,1516 | 0,280 | 2,573 | 0,0198 | ✅ |
| $i=10$ (123,17) | 0,1505 | 0,280 | 2,574 | 0,0197 | ✅ |
| $i=11$ (122,39) | 0,1523 | 0,298 | 2,687 | 0,0156 | ✅ |
| $i=12$ (125,49) | 0,1479 | 0,280 | 2,569 | 0,0199 | ✅ |
| $i=13$ (126,51) | 0,1423 | 0,281 | 2,579 | 0,0195 | ✅ |
| $i=14$ (125,14) | 0,1473 | 0,268 | 2,494 | 0,0232 | ✅ |
| $i=15$ (126,59) | 0,1366 | 0,256 | 2,417 | 0,0272 | ✅ |
| $i=16$ (124,59) | 0,1528 | 0,274 | 2,535 | 0,0213 | ✅ |
| **$i=17$ (127,52)** | 0,1225 | 0,228 | **2,239** | **0,0389** | ✅ *(le plus proche du seuil)* |
| **$i=18$ (121,93)** | 0,1922 | 0,447 | **3,710** | **0,0017** | ✅ *(le plus contraignant)* |
| $i=19$ (123,16) | 0,1826 | 0,366 | 3,133 | 0,0061 | ✅ |
| $i=20$ (125,28) | 0,1529 | 0,254 | 2,407 | 0,0277 | ✅ |

**Résultat de cette section : la conclusion est robuste.** Aucun retrait ne la fait basculer ; le cas le moins favorable ($i=17$, le plus haut de la série) laisse $p=0{,}039$, sous le seuil. À l'inverse, retirer le décrochage du 27 janvier ($i=18$) porterait $R^2$ de $0{,}28$ à $0{,}45$ et $p$ à $0{,}0017$ : ce point ne soutient pas la conclusion, il la freine.

C'est la différence avec un échantillon fragile : ici la tendance est portée par l'ensemble des 20 points, pas par un seul.

## 9.9 — Contrôle : les colonnes du script

Le script calcule ces mêmes quantités sur les cours **non arrondis**. Ses colonnes à la 20ᵉ séance :

| Colonne | Script (cours bruts) | Exemple (cours au centime) | Écart |
|---|---|---|---|
| `E_20` | 123,953734 | 123,953500 | $2{,}3\cdot10^{-4}$ |
| `VAR_20` | 2,718019 | 2,716043 | $2{,}0\cdot10^{-3}$ |
| `CORR_20` | 0,528031 | 0,528487 | $4{,}6\cdot10^{-4}$ |
| `VAL_20` | 125,387945 | 125,388400 | $4{,}5\cdot10^{-4}$ |
| `T_20` | 2,637985 | 2,641100 | $3{,}1\cdot10^{-3}$ |
| `P_20` | 0,016708 | 0,016596 | $1{,}1\cdot10^{-4}$ |
| `TEND_20` | $+1$ | $+1$ | — |

Tous les écarts s'expliquent par l'arrondi au centime des 20 cours.

> ℹ️ La colonne « script » est relevée sur une exécution donnée. yfinance renvoie les cours
> en simple précision : deux téléchargements de la même période peuvent différer d'environ
> $10^{-5}$, ce qui déplace ces valeurs à la sixième décimale sans rien changer aux écarts. On notera au passage que $\texttt{VAL\_20} = f(20) = 125{,}388$ : la colonne `VAL_n` du script est exactement la droite ajustée évaluée au dernier point de la fenêtre.

## 9.10 — Conclusion et réserves

**Conclusion.** Sur ces 20 séances, le cours d'Airbus est **tendanciellement croissant** au seuil de 5 % ($t=2{,}64$, $p=0{,}017$, $R^2=27{,}9\,\%$). La pente estimée est de **$+0{,}151$ € par séance**, soit environ **$+0{,}12\,\%$ par séance** rapporté au niveau moyen de $123{,}95$. Sur les $19$ intervalles observés, cela représente une progression de $\approx +2{,}87$ €, du même ordre que l'écart entre première et dernière clôture ($122{,}50 \to 125{,}28$, soit $+2{,}78$).

**Réserve 1 — la pente est mal déterminée.** L'IC va de $0{,}031$ à $0{,}271$ : un **facteur 8,8** entre les bornes, soit entre $+0{,}025\,\%$ et $+0{,}219\,\%$ par séance. On peut affirmer *qu'il y a* une hausse ; on ne peut pas dire *de combien*. C'est pourquoi l'IC vaut mieux que le seul $p=0{,}017$, qui donnerait l'illusion d'un résultat net.

**Réserve 2 — 72 % de la variance reste du bruit.** Un $R^2$ de $0{,}28$ signifie que la droite ne rend compte que de moins de 30 % de ce qui bouge. Le graphique des résidus le montre : $\pm 3$ € d'écart autour d'une droite qui ne monte que de $2{,}87$ € sur toute la fenêtre. La tendance existe, elle est petite devant l'agitation quotidienne.

**Réserve 3 — l'hypothèse d'indépendance, sur un cours de bourse.** C'est la réserve décisive de l'[étape 8](08-test-de-tendance.md#portée-et-limites). Durbin–Watson vaut ici $1{,}87$ et ne détecte pas d'autocorrélation des résidus, ce qui est plutôt rassurant sur cette fenêtre précise — mais un DW calculé sur 20 points a une puissance très faible, et une marche aléatoire ne relève pas de $H_0$ même quand ses résidus semblent blancs. Le test dit que le modèle « niveau constant + bruit i.i.d. » explique mal ces 20 cours ; il ne dit pas que le modèle « tendance linéaire + bruit i.i.d. » les explique bien.

**Réserve 4 — ce qu'on ne peut pas conclure.** Rien de ce qui précède ne dit que la hausse se poursuivra. La suite de l'historique est d'ailleurs sans appel : le cours d'Airbus touchera $45{,}01$ € le 18 mars 2020, sept semaines après la fin de cette fenêtre — soit $-64\,\%$ depuis la dernière clôture du tableau. Une tendance mesurée sur 20 séances décrit le passé récent, pas l'avenir.

---

⬅️ [Étape 8 — Position du problème et statistique de test](08-test-de-tendance.md) ·
🏠 [Sommaire](../../../modele.md)
