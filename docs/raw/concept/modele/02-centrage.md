# Étape 2 — Centrage

**Prérequis :** [étape 1](01-elimination-de-l-ordonnee.md) — l'identité $v_0(r)=E(V)-r\,E(T)$.
**Ce qu'on établit ici :** le problème à deux variables se réduit à une fonction $\varphi$ d'une seule variable, la pente.

---

Posons les variables centrées $t_i = T_i-E(T)$ et $v_i = V_i - E(V)$, qui vérifient $\sum_i t_i=\sum_i v_i=0$. En injectant (1) dans le résidu :
$$\hat e_i(r) = V_i - v_0(r) - rT_i = \bigl(V_i-E(V)\bigr) - r\bigl(T_i - E(T)\bigr) = v_i - r\,t_i .$$

Le problème se réduit à une fonction d'une seule variable :
$$\varphi(r) \;=\; \min_{v_0} S(v_0,r) \;=\; S\bigl(v_0(r),\,r\bigr) \;=\; \frac1n\sum_{i=1}^n (v_i - r t_i)^2 .$$

---

⬅️ [Étape 1 — Élimination de l'ordonnée à l'origine](01-elimination-de-l-ordonnee.md) ·
➡️ [Étape 3 — Développement du carré](03-developpement-du-carre.md) ·
🏠 [Sommaire](../../modele.md)
