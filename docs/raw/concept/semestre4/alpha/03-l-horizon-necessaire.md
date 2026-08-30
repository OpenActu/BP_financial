# Module 3 — L'horizon nécessaire

**Prérequis :** [module 2](02-le-calcul-et-ses-erreurs-types.md).
**Ce qu'on établit ici :** une formule en trois symboles qui explique pourquoi presque aucun alpha publié n'est mesurable, et pourquoi accélérer l'échantillonnage n'y change rien.

---

## 3.1 — La formule

Reprenons $\operatorname{SE}(\alpha) \simeq s/\sqrt n$ du
[module 2](02-le-calcul-et-ses-erreurs-types.md#23--les-erreurs-types-viennent-du-levier),
et écrivons tout en grandeurs annuelles. Notons $m$ le nombre de périodes par an
(252 en quotidien), $Y$ le nombre d'**années** d'historique, donc $n = mY$, et
$\sigma_\varepsilon$ la volatilité résiduelle **annualisée**, soit $s\sqrt m$.

L'alpha annualisé vaut $m\alpha$, donc son erreur type vaut
$m\operatorname{SE}(\alpha)$ :

$$\operatorname{SE}(\alpha_{\text{an}}) = m\,\frac{s}{\sqrt n}
= m\,\frac{\sigma_\varepsilon/\sqrt m}{\sqrt{mY}}
= \frac{\sigma_\varepsilon}{\sqrt Y}$$

$$\boxed{\;\operatorname{SE}(\alpha_{\text{an}}) \;=\; \frac{\sigma_\varepsilon}{\sqrt{Y}}\;}$$

Trois symboles, et tout est dit : **la précision d'un alpha ne dépend que de la
volatilité résiduelle et du nombre d'années.**

*Vérification sur Airbus* : $\sigma_\varepsilon = 29{,}98\,\%$ et
$Y = 1026/252 = 4{,}071$ ans donnent $29{,}98/\sqrt{4{,}071} = 14{,}86\,\%$ — la
valeur exacte obtenue par le calcul complet du
[module 5](05-exemple-chiffre-airbus.md), au centième près.

## 3.2 — La fréquence d'échantillonnage n'y change rien

$m$ a disparu de la formule. Ce n'est pas une approximation, c'est une
simplification exacte : passer du quotidien à l'horaire multiplie $n$ par 8 mais
divise $s$ par $\sqrt 8$, et les deux effets s'annulent.

| Fréquence | $m$ | $n$ sur 4,07 ans | $\operatorname{SE}(\alpha_{\text{an}})$ |
|---|---|---|---|
| Mensuelle | 12 | 49 | 14,86 % |
| Hebdomadaire | 52 | 212 | 14,86 % |
| Quotidienne | 252 | 1026 | 14,86 % |
| Horaire | 2016 | 8208 | 14,86 % |

> 🔑 **Multiplier les observations sans allonger la période n'apporte
> rigoureusement aucune précision sur l'alpha.** Seul le calendrier compte. Une
> étude sur 8208 rendements horaires de quatre ans n'en sait pas plus qu'une
> étude sur 49 rendements mensuels des mêmes quatre ans.

C'est contre-intuitif et c'est pourtant la conséquence directe du fait que
l'alpha est un **taux par unité de temps** : en gagnant des points on mesure
mieux chaque période, mais on mesure des périodes plus courtes, dans exactement
la même proportion.

*(Le résultat vaut sous l'hypothèse d'erreurs i.i.d. de l'[étape 8](../../semestre3/modele/08-test-de-tendance.md).
En haute fréquence, microstructure et autocorrélation la mettent en défaut — et
dans le sens défavorable, voir le [module 4](04-cinq-pieges.md#44--des-erreurs-qui-ne-sont-pas-iid).)*

## 3.3 — Combien d'années pour détecter un alpha

Détecter $\alpha$ au seuil de 5 % demande
$|\alpha| > 1{,}96\operatorname{SE}(\alpha_{\text{an}})$, soit

$$\boxed{\;Y \;>\; \left(\frac{1{,}96\,\sigma_\varepsilon}{\alpha}\right)^{2}\;}$$

Le carré est ce qui rend l'affaire désespérée : viser un alpha deux fois plus
petit demande **quatre fois** plus d'histoire.

**Années nécessaires, au seuil de 5 % :**

| Alpha visé | $\sigma_\varepsilon = 10\,\%$ | $15\,\%$ | $20\,\%$ | $30\,\%$ |
|---|---|---|---|---|
| 1 %/an | 384 ans | 864 ans | 1537 ans | 3457 ans |
| 2 %/an | 96 ans | **216 ans** | 384 ans | 864 ans |
| 3 %/an | 43 ans | 96 ans | 171 ans | 384 ans |
| 5 %/an | 15 ans | 35 ans | 61 ans | 138 ans |
| 10 %/an | 4 ans | 9 ans | 15 ans | 35 ans |
| 20 %/an | 1 an | 2 ans | 4 ans | 9 ans |

Un fonds diversifié a une volatilité résiduelle de l'ordre de 5 à 15 % ; une
action isolée, 25 à 40 %. **Un alpha de 2 %/an sur un fonds à 15 % de volatilité
résiduelle demande 216 ans de données pour être distingué de zéro.** Aucune série
financière ne le permet, et aucun gérant ne vit assez longtemps.

## 3.4 — Le plus petit alpha détectable

La même formule dans l'autre sens, plus utile en pratique : sur l'historique dont
on dispose, quel est le plus petit alpha qu'on pourrait établir ?

$$\alpha_{\min} = \frac{1{,}96\,\sigma_\varepsilon}{\sqrt Y}$$

| Horizon | $\sigma_\varepsilon = 10\,\%$ | $15\,\%$ | $20\,\%$ | $30\,\%$ |
|---|---|---|---|---|
| 1 an | 19,6 % | 29,4 % | 39,2 % | 58,8 % |
| 3 ans | 11,3 % | 17,0 % | 22,6 % | 33,9 % |
| 4 ans | 9,8 % | 14,7 % | 19,6 % | **29,4 %** |
| 5 ans | 8,8 % | 13,1 % | 17,5 % | 26,3 % |
| 10 ans | 6,2 % | 9,3 % | 12,4 % | 18,6 % |
| 20 ans | 4,4 % | 6,6 % | 8,8 % | 13,1 % |
| 30 ans | 3,6 % | 5,4 % | 7,2 % | 10,7 % |

La case en gras est celle d'Airbus : quatre ans, 30 % de volatilité résiduelle.
**Seul un alpha dépassant 29,4 %/an aurait pu y être établi.** Autant dire qu'on
n'a rien mesuré — et c'est bien ce que dit l'intervalle $[-29{,}3\ ;\ +29{,}1]\,\%$.

## 3.5 — Ce que la formule suggère de faire

Elle n'a que deux leviers, et un seul est actionnable.

**Allonger $Y$.** Le seul moyen honnête, et il est lent : quadrupler l'histoire
divise l'incertitude par deux. Sur des données financières, allonger l'historique
suppose en outre que le processus n'a pas changé sur toute la période — hypothèse
d'autant plus douteuse que la fenêtre est longue. Le gain statistique se paie en
pertinence.

**Réduire $\sigma_\varepsilon$.** C'est ce que fait la diversification : un
portefeuille de 30 titres a une volatilité résiduelle très inférieure à celle de
chacun. Passer de 30 % à 10 % divise l'horizon nécessaire par **neuf**. C'est la
raison profonde pour laquelle on peut espérer parler de l'alpha d'un fonds, et
presque jamais de celui d'une action isolée.

> ⚠️ **Ce module ne dit pas que l'alpha n'existe pas.** Il dit que sur les
> horizons dont on dispose, on ne peut généralement pas le distinguer de zéro.
> Absence de preuve n'est pas preuve d'absence — c'est la réserve de
> l'[étape 8](../../semestre3/modele/08-test-de-tendance.md), et elle joue ici dans les deux
> sens : ni « ce gérant produit de l'alpha », ni « ce gérant n'en produit pas »
> ne sont établis par quatre ans de données.

---

⬅️ [Module 2 — Le calcul et ses erreurs types](02-le-calcul-et-ses-erreurs-types.md) ·
➡️ [Module 4 — Cinq pièges](04-cinq-pieges.md)
