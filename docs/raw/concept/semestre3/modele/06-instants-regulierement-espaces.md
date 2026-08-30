# Étape 6 — Cas particulier : instants régulièrement espacés

**Prérequis :** [étapes 1 à 5](../../../modele.md#plan-de-la-preuve), et notamment $r_{\min}=\operatorname{Cov}(V,T)/\operatorname{Var}(T)$.
**Ce qu'on établit ici :** les formules explicites de la pente et de l'ordonnée quand $T_i=i$.

---

> ⚠️  **Nouvelle hypothèse, propre aux étapes 6 et 7 :** on suppose désormais $T_i = i$ pour $i=1,\dots,n$ (avec $n\ge 2$), c'est-à-dire des instants entiers régulièrement espacés. Les étapes 1 à 5 sont, elles, générales.

Sous cette hypothèse :
$$E(T)=\frac{n+1}{2},\qquad \operatorname{Var}(T)=\frac{n^2-1}{12},\qquad \sigma_T=\frac{\sqrt{n^2-1}}{2\sqrt3}.$$

En partant de $r_{\min}=\dfrac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)}=\rho_{V,T}\dfrac{\sigma_V}{\sigma_T}$ et en posant
$$\phi(V) \;=\; \rho_{V,T}\,\sqrt{\dfrac{3\operatorname{Var}(V)}{n^2-1}}$$
il vient
$$\boxed{\;r_{\min} = 2\,\phi(V)\;}$$
$$\boxed{\;v_{0,\min} = E(V) - r_{\min}E(T) = E(V) - \phi(V)\,(n+1)\;}$$

*(Le signe de $\phi(V)$ est celui de $\rho_{V,T}$, donc celui de la pente.)*

---

⬅️ [Étape 5 — Réécriture avec le coefficient de corrélation](05-coefficient-de-correlation.md) ·
➡️ [Étape 7 — Droite ajustée](07-droite-ajustee.md) ·
🏠 [Sommaire](../../../modele.md)
