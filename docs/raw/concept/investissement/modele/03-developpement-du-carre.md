# Étape 3 — Développement du carré

**Prérequis :** [étape 2](02-centrage.md) — la fonction $\varphi(r)=\frac1n\sum_i (v_i - r t_i)^2$.
**Ce qu'on établit ici :** $\varphi$ est un trinôme du second degré en $r$, strictement convexe.

---

$$\varphi(r) = \frac1n\sum_i v_i^2 \;-\; 2r\,\frac1n\sum_i v_i t_i \;+\; r^2\,\frac1n\sum_i t_i^2$$

c'est-à-dire, avec les notations de moments (le centrage rend ces sommes exactement les variances/covariance empiriques) :
$$\varphi(r) = \operatorname{Var}(V) - 2r\operatorname{Cov}(V,T) + r^2\operatorname{Var}(T). \tag{2}$$

C'est un trinôme du second degré en $r$, de coefficient dominant $\operatorname{Var}(T)>0$
**par hypothèse** : il est strictement convexe et admet un minimum global unique.

---

⬅️ [Étape 2 — Centrage](02-centrage.md) ·
➡️ [Étape 4 — Mise sous forme canonique](04-forme-canonique.md) ·
🏠 [Sommaire](modele.md)
