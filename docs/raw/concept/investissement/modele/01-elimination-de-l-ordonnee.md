# Étape 1 — Élimination de l'ordonnée à l'origine

**Prérequis :** l'[énoncé, les notations et le théorème](modele.md).
**Ce qu'on établit ici :** à pente $r$ fixée, l'ordonnée optimale vaut $v_0(r)=E(V)-r\,E(T)$, et les résidus sont de **moyenne nulle**.

---

La minimisation se fait en deux temps :
$$\min_{v_0,r} S(v_0,r) \;=\; \min_r\Bigl(\min_{v_0} S(v_0,r)\Bigr),$$
égalité licite car, à $r$ fixé, l'infimum intérieur est **atteint** — c'est ce que cette étape démontre.

$S$ est polynomiale, donc $C^\infty$ ; à $r$ fixé, elle est quadratique en $v_0$ de coefficient dominant $1>0$, donc strictement convexe : son unique point critique est le minimum global.

> 📐 **Les trois théorèmes contenus dans cette incise** — un minimum local d'une fonction convexe est global, il est unique si la convexité est stricte, et annuler la dérivée suffit à le caractériser — sont démontrés au [module 6 du cours d'analyse](../analyse/convexite/06-minimisation-convexe.md), qui relit cette preuve intégralement au § 6.6.

Annulons la dérivée partielle :
$$\frac{\partial S}{\partial v_0} = -\frac2n\sum_{i=1}^n \bigl(V_i - v_0 - r T_i\bigr) = 0 \;\Longleftrightarrow\; \frac1n\sum_i \hat e_i = E(V)-v_0-rE(T) = 0 .$$

C'est l'équation normale associée à la constante : **les résidus sont de moyenne nulle**.

> 📐 **La même chose, sans somme et pour un nombre quelconque de variables explicatives.** Le [§ 7.5 du cours de dérivation et intégration](../analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md) obtient $\hat\beta=(X^{\top}X)^{-1}X^{\top}y$ en trois lignes de calcul matriciel, Hessienne comprise — donc avec la preuve qu'il s'agit bien d'un minimum. D'où $$v_0(r) = E(V) - r\,E(T). \tag{1}$$

La droite ajustée passe donc toujours par le point moyen $\bigl(E(T),E(V)\bigr)$.

> **Conséquence utile.** Les résidus étant centrés, $S=\frac1n\sum_i\hat e_i^{\,2}$ **est** bien la variance empirique des résidus, ce qui justifie la notation $\operatorname{Var}(\hat e)$ annoncée dans l'énoncé.

---

⬅️ [Énoncé et théorème](modele.md) ·
➡️ [Étape 2 — Centrage](02-centrage.md) ·
🏠 [Sommaire](modele.md)
