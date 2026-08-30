# Module 1 — De quoi alpha est le nom

**Prérequis :** [étape 1](../modele/01-elimination-de-l-ordonnee.md) et [étape 4](../modele/04-forme-canonique.md) du modèle.
**Ce qu'on établit ici :** la définition, l'identité avec la régression déjà démontrée dans le dépôt, et le fait que l'alpha n'existe que relativement à un modèle.

---

## 1.1 — Le modèle de marché

On observe deux séries de rendements sur les mêmes séances : ceux d'un titre
$r_{i,t}$ et ceux d'un indice $r_{m,t}$. Le **modèle de marché** postule

$$\boxed{\;r_{i,t} - r_f \;=\; \alpha \;+\; \beta\,(r_{m,t} - r_f) \;+\; \varepsilon_t\;}$$

où $r_f$ est le taux sans risque de la période. Trois quantités, trois rôles très
différents :

| Terme | Nom | Ce qu'il représente |
|---|---|---|
| $\beta$ | exposition au marché | de combien le titre bouge quand l'indice bouge de 1 |
| $\alpha$ | rendement inexpliqué | ce que le titre rapporte **en plus** de sa seule exposition |
| $\varepsilon_t$ | résidu | le mouvement propre au titre, de moyenne nulle |

La lecture usuelle : un gérant qui prend $\beta = 1{,}5$ et gagne 50 % de plus
que l'indice n'a rien produit — il a simplement pris plus de risque de marché,
et ce levier était accessible à tous. **Alpha est ce qui reste après avoir retiré
la part achetable en levier sur l'indice.**

## 1.2 — Alpha est l'ordonnée à l'origine de l'étape 1

Ce cours n'introduit **aucune mathématique nouvelle**. Le modèle ci-dessus est la
régression linéaire simple de [`modele.md`](../../modele.md), à un changement de
variable près :

| Dans le modèle | Ici |
|---|---|
| $V_i$ — les observations | $r_{i,t}$ — les rendements du titre |
| $T_i$ — les instants | $r_{m,t}$ — les rendements de l'indice |
| $r_{\min} = \operatorname{Cov}(V,T)/\operatorname{Var}(T)$ | $\beta$ |
| $v_{0,\min} = E(V) - r_{\min}E(T)$ | $\alpha$ |

L'[étape 1](../modele/01-elimination-de-l-ordonnee.md) établit
$v_{0,\min} = E(V) - r_{\min}E(T)$ : **c'est exactement la formule de l'alpha.**
L'[étape 4](../modele/04-forme-canonique.md) donne la pente, l'[étape 5](../modele/05-coefficient-de-correlation.md)
donne $R^2 = \rho^2$, l'[étape 8](../modele/08-test-de-tendance.md) donne la loi
de la statistique de test. Tout est déjà prouvé.

Une seule différence, et elle compte : dans le modèle, $T_i = i$ sont des instants
**déterministes et régulièrement espacés** ; ici $r_{m,t}$ est **aléatoire**. Les
formules de l'étape 6 spécifiques à $T_i = i$ — $\operatorname{Var}(T) = (n^2-1)/12$,
$\phi(V)$, la droite symétrique de l'[étape 7](../modele/07-droite-ajustee.md) —
ne s'appliquent donc **pas**. Il faut revenir aux formes générales des étapes 1 à 5.

## 1.3 — Alpha n'existe que relativement à un modèle

C'est le point que la pratique oublie le plus souvent. $\alpha$ n'est pas une
propriété du titre : c'est l'écart entre le titre et **un modèle qu'on a choisi**.
Changez le modèle, l'alpha change.

**L'indice de référence.** Mesurer Airbus contre le CAC 40, contre le SBF 120, ou
contre un indice aéronautique mondial donne trois alphas différents. Aucun n'est
« le bon » : chacun répond à la question *que reste-t-il une fois retiré ce que
cette référence-là explique ?*

**Le nombre de facteurs.** Le modèle à un facteur ci-dessus est le plus pauvre. En
ajouter d'autres — taille, valeur, momentum, qualité, faible volatilité — absorbe
une part de ce qui apparaissait comme alpha :

$$r_i - r_f = \alpha + \beta_m (r_m - r_f) + \beta_1 F_1 + \dots + \beta_k F_k + \varepsilon$$

Un alpha positif dans le modèle à un facteur devient couramment nul dans un modèle
à trois ou cinq. **L'alpha rétrécit à mesure que le modèle s'enrichit** — ce qui
est logique : on lui retire chaque fois une explication supplémentaire.

> 🔑 **Publier un alpha sans nommer son modèle de référence, c'est publier un
> écart sans dire à quoi.** Le minimum : l'indice, la période, la fréquence, et le
> traitement du taux sans risque.

## 1.4 — Alpha n'est pas la surperformance

Deux grandeurs distinctes, souvent confondues :

| | Définition | Corrigée du risque ? |
|---|---|---|
| **Surperformance** | $r_i - r_m$, l'écart brut | ❌ non |
| **Alpha** | $r_i - \beta\,r_m$ (avec $r_f = 0$) | ✅ oui |

Elles ne coïncident que si $\beta = 1$. Sur Airbus, $\beta = 1{,}53$ : sur une
année où le CAC monte de 10 %, le titre est *attendu* à 15,3 %, et faire 12 %
serait un **alpha négatif** malgré une surperformance apparente de $+2$ points.

Et même la surperformance a son propre piège — moyenne arithmétique contre
performance réalisée, traité au [module 4](04-cinq-pieges.md#41--le-drag-de-volatilité).

---

⬅️ [README du cours](README.md) ·
➡️ [Module 2 — Le calcul et ses erreurs types](02-le-calcul-et-ses-erreurs-types.md)
