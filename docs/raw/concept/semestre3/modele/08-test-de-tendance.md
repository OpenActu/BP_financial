# Étape 8 — Position du problème et statistique de test

**Prérequis :** [étapes 1 à 7](../../../modele.md#plan-de-la-preuve).
**Ce qu'on établit ici :** le passage du déterministe au probabiliste, le test de nullité de la pente, et les limites de ce test.
**Rupture :** c'est la **première** étape qui suppose un modèle génératif. Tout ce qui précède est une identité algébrique.

---

Les étapes 1–7 sont purement déterministes : ce sont des identités algébriques sur $n$ points, vraies sans aucun modèle probabiliste. En particulier $\rho_{V,T}$ y est une simple **mesure d'alignement** de l'échantillon, pas un estimateur — il n'y a rien, pour l'instant, dont elle serait l'estimation.

L'objectif est maintenant d'établir un critère qui permette de décider si un échantillon observé est tendanciel ou non. Le passage exige un **changement de statut** : il faut cesser de voir les $V_i$ comme $n$ nombres donnés et les voir comme la réalisation d'un mécanisme aléatoire, seul cadre où la question « cette pente est-elle attribuable au hasard ? » ait un sens.

> **Remarque (acquis de l'[étape 4](04-forme-canonique.md)).** L'équivalence $$\rho_{V,T}=0 \iff \operatorname{Cov}(V,T)=0 \iff r_{\min}=0$$ est **déterministe** : elle découle directement de $r_{\min}=\operatorname{Cov}(V,T)/\operatorname{Var}(T)$ et de $\operatorname{Var}(T)>0$. Elle ne requiert aucun modèle. Tester la nullité de la pente ajustée ou celle de la corrélation empirique, c'est donc le **même test** — ce qui justifie de construire la statistique sur $\rho_{V,T}$ tout en énonçant les hypothèses sur $r$.

> ⚠️  **Nouvelles hypothèses, propres à l'étape 8** (non requises aux étapes 1–7) : $$V_i = v_0 + r\,T_i + \varepsilon_i,\qquad \varepsilon_i \overset{\text{i.i.d.}}{\sim}\mathcal N(0,\sigma^2),\qquad T_i \text{ déterministes},\qquad n\ge 3 .$$ Soit : **indépendance** des erreurs, **homoscédasticité**, **normalité**. Les paramètres $v_0$, $r$ et $\sigma^2$ sont inconnus et fixes ; $v_{0,\min}$, $r_{\min}$ et $\operatorname{Var}(\hat e)_{\min}$ des étapes 1–5 en deviennent les **estimateurs** des moindres carrés.

**Hypothèses du test.** Elles portent sur le **paramètre** $r$ du modèle, jamais sur la statistique $\rho_{V,T}$ — qui, calculée sur un échantillon fini, ne vaut de toute façon jamais exactement $0$ :

1. **Hypothèse nulle.** $H_0 : r = 0$ — le niveau de la série ne dépend pas du temps ; les $V_i$ fluctuent indépendamment autour d'une constante $v_0$. Toute pente observée $r_{\min}\ne 0$ n'est alors qu'une **fluctuation d'échantillonnage**.
2. **Hypothèse alternative.** $H_1 : r \ne 0$ — le temps marque une variation directionnelle.
Hypothèse **bilatérale**, le sens de la tendance n'étant pas préjugé.

Trancher exige de connaître la **loi de $\rho_{V,T}$ sous $H_0$** : c'est exactement ce que le modèle génératif ci-dessus fournit.

## Théorème (statistique de test)

Sous $H_0$, la statistique
$$\boxed{\;t \;=\; \rho_{V,T}\sqrt{\frac{n-2}{1-\rho_{V,T}^{2}}}\;}$$
suit **exactement** une loi de Student à $n-2$ degrés de liberté. De façon équivalente,
$$t^{2}=\frac{(n-2)\,\rho_{V,T}^{2}}{1-\rho_{V,T}^{2}} \;\sim\; \mathcal F(1,\,n-2).$$

Les $n-2$ degrés de liberté sont ceux qui restent après consommation de $2$ paramètres ($v_0$ et $r$) — d'où l'exigence $n\ge 3$.

> ⚠️  **La statistique est une Student, pas une normale.** La noter $z$ conduirait à chercher $1{,}96$ dans une table normale ; à $n=11$ le quantile correct est $t_{9;\,0{,}975}=2{,}262$.

**Lecture.** La seconde écriture est le rapport $$t^{2} \;=\; (n-2)\,\frac{\text{variance expliquée}}{\text{variance résiduelle}}$$ de la section « Lecture géométrique » de l'[étape 5](05-coefficient-de-correlation.md#lecture-géométrique), corrigé des degrés de liberté consommés. La statistique n'est donc pas un objet nouveau : c'est le $R^2$ de l'étape 5, mis à l'échelle pour être comparable à une loi tabulée.

**Forme équivalente en $r_{\min}$.** Le même $t$ s'écrit comme un rapport de Student usuel $\hat r/\operatorname{SE}(\hat r)$, avec $$\operatorname{SE}(r_{\min}) = \sqrt{\frac{\operatorname{Var}(V)\bigl(1-\rho_{V,T}^{2}\bigr)}{(n-2)\operatorname{Var}(T)}} \;\;\overset{T_i=i}{=}\;\; \sqrt{\frac{12\operatorname{Var}(V)\bigl(1-\rho_{V,T}^{2}\bigr)}{(n-2)\,(n^{2}-1)}},$$ ce qui donne l'**intervalle de confiance** à $1-\alpha$ de la pente :
$$r_{\min} \;\pm\; t_{\,n-2;\,1-\alpha/2}\cdot\operatorname{SE}(r_{\min}).$$

Cette forme est à préférer en pratique : elle rend l'**ampleur** de la tendance et sa précision, là où le test seul ne rend qu'un verdict binaire. Un non-rejet de $H_0$ n'est **pas** une preuve d'absence de tendance — seulement un constat que l'échantillon ne permet pas de la distinguer du bruit.

## ⚠️  Portée et limites

Le test contrôle son risque de première espèce **sous les hypothèses ci-dessus, et sous elles seules**. Par ordre décroissant de nocivité :

- **Indépendance des $\varepsilon_i$ — critique.** C'est l'hypothèse qui casse en premier sur une série temporelle. En particulier, une **marche aléatoire** ($V_i = V_{i-1}+\eta_i$) ne relève **pas** de $H_0$ : ses chocs s'accumulent au lieu de se dissiper. Le test y rejette alors à tort dans **≈ 69 % des cas à $n=24$ et ≈ 84 % à $n=120$** pour un seuil nominal de 5 % — et la situation **empire** avec $n$, la statistique divergeant en $\sqrt n$ (régression fallacieuse,
Granger–Newbold 1974). Distinguer *stationnaire autour d'une tendance* de *marche aléatoire* est une question **préalable** au test de pente, qui relève d'un test de racine unitaire (ADF, KPSS).
- **Saisonnalité — critique en pratique.** C'est de l'autocorrélation déguisée ; sur une fenêtre ne couvrant pas un nombre entier de cycles, elle produit une pente purement artefactuelle.
- **Homoscédasticité — modérée.** Se corrige par des écarts-types robustes (White, HAC/Newey–West), qui laissent $r_{\min}$ inchangé et ne retouchent que $\operatorname{SE}(r_{\min})$.
- **Normalité — faible.** Le théorème central limite rend le test approximativement valide dès $n$ modéré ; c'est l'hypothèse dont on se soucie le moins, alors qu'elle est celle qu'on cite le plus.
- **Valeurs aberrantes et petits échantillons.** $\rho_{V,T}$ n'est pas robuste : un point extrême situé en bord de fenêtre — donc à fort effet de levier — peut piloter à lui seul la pente et, avec elle, la conclusion. L'[étape 9](09-exemple-complet.md) en donne une illustration frappante.

**Contrôle minimal** : examiner les résidus $\hat e_i$ avant de conclure (Durbin–Watson ou Ljung–Box). En cas d'autocorrélation avérée, préférer des écarts-types HAC, une modélisation explicite de la dynamique, ou un test non paramétrique de tendance (Mann–Kendall, pente de Sen, version de Hamed–Rao pour données corrélées).

---

⬅️ [Étape 7 — Droite ajustée](07-droite-ajustee.md) ·
➡️ [Étape 9 — Exemple complet d'évaluation](09-exemple-complet.md) ·
🏠 [Sommaire](../../../modele.md)
