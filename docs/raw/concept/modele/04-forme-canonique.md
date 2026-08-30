# Étape 4 — Mise sous forme canonique

**Prérequis :** [étape 3](03-developpement-du-carre.md) — le trinôme (2).
**Ce qu'on établit ici :** le minimiseur $r_{\min}$, l'ordonnée $v_{0,\min}$ et la valeur minimale, **d'un seul coup et sans dériver**.

---

Plutôt que de dériver, complétons le carré — cela donne le minimiseur et la valeur minimale d'un seul coup. Avec $a=\operatorname{Var}(T)$, $b=\operatorname{Cov}(V,T)$, $c=\operatorname{Var}(V)$ :
$$\varphi(r) = a\left(r^2 - 2\frac{b}{a}r\right) + c = a\left(r - \frac{b}{a}\right)^2 - \frac{b^2}{a} + c ,$$
soit
$$\boxed{\;\varphi(r) = \operatorname{Var}(T)\left(r - \frac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)}\right)^{2} + \left(\operatorname{Var}(V) - \frac{\operatorname{Cov}(V,T)^2}{\operatorname{Var}(T)}\right)\;}\tag{3}$$

Le premier terme est positif et s'annule si et seulement si
$$r_{\min} = \frac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)}, \qquad v_{0,\min} = v_0(r_{\min}) = E(V) - r_{\min}\,E(T).$$

Le second terme est constant (indépendant de $r$) : c'est donc la valeur minimale.
$$\operatorname{Var}(\hat e)_{\min} = \varphi(r_{\min}) = \operatorname{Var}(V) - \frac{\operatorname{Cov}(V,T)^2}{\operatorname{Var}(T)} .$$

---

⬅️ [Étape 3 — Développement du carré](03-developpement-du-carre.md) ·
➡️ [Étape 5 — Réécriture avec le coefficient de corrélation](05-coefficient-de-correlation.md) ·
🏠 [Sommaire](../../modele.md)
