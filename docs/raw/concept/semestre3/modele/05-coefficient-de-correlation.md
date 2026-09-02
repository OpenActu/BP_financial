# Étape 5 — Réécriture avec le coefficient de corrélation

**Prérequis :** [étape 4](04-forme-canonique.md) — la valeur minimale $\operatorname{Var}(V) - \operatorname{Cov}(V,T)^2/\operatorname{Var}(T)$.
**Ce qu'on établit ici :** la forme finale du théorème, le corollaire de Cauchy–Schwarz, et la lecture géométrique en $R^2$.

---

En factorisant par $\operatorname{Var}(V)$ :
$$\operatorname{Var}(\hat e)_{\min} = \operatorname{Var}(V)\left(1 - \frac{\operatorname{Cov}(V,T)^2}{\operatorname{Var}(V)\operatorname{Var}(T)}\right) = \operatorname{Var}(V)\bigl(1-\rho_{V,T}^2\bigr). \qquad\blacksquare$$

## Corollaire — Cauchy–Schwarz

Le membre de gauche est une moyenne de carrés, donc $\ge 0$. D'où $\operatorname{Cov}(V,T)^2 \le \operatorname{Var}(V)\operatorname{Var}(T)$, c'est-à-dire $|\rho_{V,T}|\le 1$, avec **égalité si et seulement si tous les résidus sont nuls**, i.e. les points sont exactement alignés.

## Lecture géométrique

$$\underbrace{\operatorname{Var}(V)}_{\text{variance totale}} = \underbrace{ r_{\min}^2\operatorname{Var}(T)}_{\text{variance expliquée}} + \underbrace{\operatorname{Var}(\hat e)_{\min}}_{\text{variance résiduelle}},$$

et $\rho_{V,T}^2 = \cos^2\theta$, où $\theta$ est l'angle entre les vecteurs **centrés** $t=(t_i)$ et $v=(v_i)$ de $\mathbb{R}^n$ : c'est la part de variance expliquée, autrement dit le $R^2$ de la régression simple. Les moindres carrés ne sont rien d'autre que la **projection orthogonale** de $v$ sur la droite engendrée par $t$.

> 📐 La projection orthogonale et l'identité de Pythagore qui sous-tendent cette décomposition sont traitées aux modules [5](../../semestre1/algebre/05-orthogonalite-et-pythagore.md) et [6](../../semestre1/algebre/06-projection-orthogonale.md) du cours d'algèbre.

---

⬅️ [Étape 4 — Mise sous forme canonique](04-forme-canonique.md) ·
➡️ [Étape 6 — Instants régulièrement espacés](06-instants-regulierement-espaces.md) ·
🏠 [Sommaire](../../../modele.md)
