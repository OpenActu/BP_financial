# Variance résiduelle minimale de la régression linéaire simple

Document de référence du dépôt : il démontre ce que calcule `historique_sbf250.py` (colonnes
`E_20`, `VAR_20`, `CORR_20`, `VAL_20`), puis en tire un test de tendance.

La démonstration est découpée en **neuf pages, une par étape** ; cette page porte l'énoncé, les
notations et le théorème, communs à toutes.

## Énoncé

On dispose de $n$ couples $(T_i, V_i)_{1\le i\le n}$ et on ajuste le modèle $V \approx v_0 + r\,T$ au sens des moindres carrés. On s'intéresse aux résidus $$\hat e = (\hat e_i)_{1\le i\le n} = \bigl(V_i - v_0 - r T_i\bigr)_{1\le i\le n}$$
et au critère $$S(v_0,r) \;=\; \frac1n\sum_{i=1}^n \bigl(V_i - v_0 - r T_i\bigr)^2 \;=\; \frac1n\sum_{i=1}^n\hat e_i^{\,2}$$ avec les moments empiriques $$E(T)=\frac1n\sum_i T_i,\qquad E(V)=\frac1n\sum_i V_i,$$
$$\operatorname{Var}(T)=\frac1n\sum_i\bigl(T_i-E(T)\bigr)^2,\qquad \operatorname{Var}(V)=\frac1n\sum_i\bigl(V_i-E(V)\bigr)^2,$$
$$\operatorname{Cov}(V,T)=\frac1n\sum_i\bigl(T_i-E(T)\bigr)\bigl(V_i-E(V)\bigr),\qquad \rho_{V,T}=\frac{\operatorname{Cov}(V,T)}{\sqrt{\operatorname{Var}(V)\operatorname{Var}(T)}} .$$

> **Note de notation.** $S(v_0,r)$ est un **moment d'ordre 2 non centré** des résidus. Il ne coïncide avec leur *variance* que si $\frac1n\sum_i \hat e_i = 0$ — ce que l'[étape 1](01-elimination-de-l-ordonnee.md) établira pour tout couple optimal $(v_0(r), r)$. L'écriture $\operatorname{Var}(\hat e)$ est donc légitime **le long de la trajectoire d'optimisation**, et en particulier au minimum ; c'est en ce sens qu'elle est employée ci-après.

**Hypothèses.** $\operatorname{Var}(T)>0$ (les $T_i$ ne sont pas tous égaux) et $\operatorname{Var}(V)>0$ — cette seconde hypothèse n'est requise que pour que $\rho_{V,T}$ soit défini ; si $\operatorname{Var}(V)=0$ le minimum vaut trivialement $0$.

## Théorème

$$\boxed{\operatorname{Var}(\hat e)_{\min} \;=\; \min_{v_0,r} S(v_0,r) \;=\; \operatorname{Var}(V) - \frac{\operatorname{Cov}(V,T)^2}{\operatorname{Var}(T)} \;=\; \operatorname{Var}(V)\bigl(1-\rho_{V,T}^2\bigr)}$$

## Plan de la preuve

La minimisation se fait en deux temps : $$\min_{v_0,r} S(v_0,r) \;=\; \min_r\Bigl(\min_{v_0} S(v_0,r)\Bigr),$$ égalité licite car, à $r$ fixé, l'infimum intérieur est **atteint** ([étape 1](01-elimination-de-l-ordonnee.md)).

### Partie déterministe — aucune hypothèse probabiliste

| # | Étape | Ce qu'elle établit |
|---|---|---|
| 1 | [Élimination de l'ordonnée à l'origine](01-elimination-de-l-ordonnee.md) | $v_0(r)=E(V)-r\,E(T)$ ; les résidus sont **centrés**, d'où la notation $\operatorname{Var}(\hat e)$ |
| 2 | [Centrage](02-centrage.md) | $\hat e_i(r)=v_i-r\,t_i$ : le problème n'a plus qu'une variable |
| 3 | [Développement du carré](03-developpement-du-carre.md) | $\varphi(r)=\operatorname{Var}(V)-2r\operatorname{Cov}(V,T)+r^2\operatorname{Var}(T)$, trinôme strictement convexe |
| 4 | [**Mise sous forme canonique**](04-forme-canonique.md) ⭐ | $r_{\min}=\operatorname{Cov}(V,T)/\operatorname{Var}(T)$, $v_{0,\min}$, et la valeur minimale — **sans dériver** |
| 5 | [**Réécriture avec $\rho_{V,T}$**](05-coefficient-de-correlation.md) ⭐ | $\operatorname{Var}(\hat e)_{\min}=\operatorname{Var}(V)(1-\rho^2)$ ; Cauchy–Schwarz ; le $R^2$ comme $\cos^2\theta$ |

### Cas $T_i = i$ — instants régulièrement espacés

| # | Étape | Ce qu'elle établit |
|---|---|---|
| 6 | [Instants régulièrement espacés](06-instants-regulierement-espaces.md) | $\operatorname{Var}(T)=\frac{n^2-1}{12}$, $r_{\min}=2\phi(V)$, $v_{0,\min}=E(V)-\phi(V)(n+1)$ |
| 7 | [Droite ajustée](07-droite-ajustee.md) | $f(t)=E(V)+\phi(V)(2t-n-1)$, symétrique autour du point moyen |

### Partie probabiliste — un modèle génératif est ajouté

| # | Étape | Ce qu'elle établit |
|---|---|---|
| 8 | [**Position du problème et statistique de test**](08-test-de-tendance.md) ⭐ | $H_0:r=0$ ; $t=\rho\sqrt{(n-2)/(1-\rho^2)}\sim\mathcal T_{n-2}$ ; IC sur la pente ; **portée et limites** |
| 9 | [Exemple complet d'évaluation](09-exemple-complet.md) | Les huit étapes sur $n=11$ points, diagnostics et analyse de sensibilité |

> ⚠️  **La ligne de partage est entre les étapes 7 et 8.** Les étapes 1 à 7 sont des identités
> algébriques sur $n$ points, vraies sans aucun modèle ; $\rho_{V,T}$ y est une mesure
> d'alignement, pas un estimateur. L'étape 8 seule suppose $\varepsilon_i$ i.i.d. gaussiennes.

## Ce que les cours du dépôt apportent à cette preuve

| Cours | Ce qu'il fournit |
|---|---|
| [Convexité](../analyse/convexite/06-minimisation-convexe.md) | Les trois théorèmes admis à l'étape 1 : local $=$ global, unicité, point critique suffisant (le § 6.6 relit la preuve entière) |
| [Dérivation et intégration](../analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md) | Les équations normales $\hat\beta=(X^\top X)^{-1}X^\top y$, Hessienne comprise |
| [Algèbre linéaire](../algebre/04-projection-orthogonale.md) | La projection orthogonale et Pythagore, derrière la lecture géométrique de l'étape 5 |
| [Loi de Student](../statistique/loi-de-student/07-student-en-regression.md) | La loi exacte de la statistique de l'étape 8 |

---

➡️ Commencer par l'[étape 1 — Élimination de l'ordonnée à l'origine](01-elimination-de-l-ordonnee.md)
