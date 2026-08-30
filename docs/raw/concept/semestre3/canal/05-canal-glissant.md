# Module 5 — Le canal glissant

**Prérequis :** [module 3](03-epaisseur-variable-et-levier.md).
**Ce qu'on établit ici :** ce que devient un canal recalculé à chaque séance, comment choisir la longueur de fenêtre, et où se cache le regard en avant.

---

## 5.1 — Un canal, ou une famille de canaux

Les modules 1 à 4 traitent d'**un** canal : une fenêtre fixe, une régression, une
bande. C'est ce que fait l'[étape 9](../modele/09-exemple-complet.md) sur 20
séances.

Le script du dépôt fait autre chose. `VAL_n` est calculée par
`rolling(window=n, min_periods=n)` : à **chaque** séance $\tau$, une régression
neuve sur les $n$ séances $[\tau-n+1,\ \tau]$, dont on ne retient que la valeur
au dernier point, $f_\tau(\tau)$.

Il n'y a donc pas un canal mais une famille $\{(\text{support}_\tau, \text{résistance}_\tau)\}$,
et la courbe `VAL_n` du CSV est le **lieu des extrémités droites** de tous ces
canaux — pas une droite, pas le bord d'un canal unique.

> **Conséquence à ne pas rater.** Le canal tracé à la séance $\tau$ n'est valable
> qu'en $\tau$. Le prolonger vers la gauche pour « voir comment il tenait » est
> faux : à ces dates-là, c'était un autre canal.

## 5.2 — Deux usages, un seul est causal

| | Canal **fixe** | Canal **glissant** |
|---|---|---|
| Ajusté sur | toute la période affichée | les $n$ dernières séances, à chaque date |
| Ce qu'il montre | la structure d'une période **révolue** | ce qu'on pouvait savoir à chaque date |
| Utilisable comme signal | ❌ **non** | ✅ oui |
| Usage légitime | description a posteriori, pédagogie | backtest, décision |

Le canal fixe utilise, pour juger la séance 5, des observations des séances 6 à
20. C'est du **regard en avant** (*look-ahead*) : parfaitement licite pour
décrire, disqualifiant pour évaluer une règle. Le canal glissant, lui, n'emploie
en $\tau$ que des données antérieures ou égales à $\tau$ — c'est ce que garantit
`min_periods=n`, qui laisse `NaN` les $n-1$ premières lignes plutôt que de
calculer sur une fenêtre tronquée.

> ⚠️ **Le canal glissant se repeint quand même — mais légitimement.** Le canal
> affiché à la séance $\tau$ diffère de celui de $\tau-1$ : nouvelle pente,
> nouveau pivot, nouvelle largeur. Ce n'est pas un défaut, c'est la définition.
> Le défaut serait d'oublier que le canal « qu'on voyait » à une date passée
> n'est pas celui qu'on redessine aujourd'hui sur cette date.

## 5.3 — Choisir la longueur de fenêtre

Le seul arbitrage réel du canal glissant. Il se chiffre.

### La pente se précise en $n^{-3/2}$

En repartant de l'[étape 8](../modele/08-test-de-tendance.md) et en substituant
$\operatorname{Var}(V)(1-\rho^2) = s^2(n-2)/n$, l'erreur type de la pente prend
une forme remarquablement propre :

$$\boxed{\;\operatorname{SE}(r_{\min}) \;=\; s\,\sqrt{\frac{12}{n\,(n^2-1)}} \;\underset{n\ \text{grand}}{\approx}\; \frac{s\sqrt{12}}{n^{3/2}}\;}$$

**La pente gagne en précision comme $n^{-3/2}$, pas comme $n^{-1/2}$.** Deux
effets se cumulent : on ajoute des points, et on allonge le bras de levier
temporel. À $s$ constant, passer d'une fenêtre de 20 à une fenêtre de 120 divise
l'erreur type par $6^{3/2} = 14{,}7$.

### Mais une pente longue peut ne plus exister

La contrepartie n'est pas statistique, elle est de modélisation : une fenêtre de
120 séances estime très précisément **la pente moyenne des six derniers mois**.
Si le régime a changé il y a trois semaines, cette précision porte sur une
grandeur sans intérêt. L'estimateur est excellent, l'estimande est périmé.

| Fenêtre | $\operatorname{SE}(r)$ relatif | Réactivité | Défaut dominant |
|---|---|---|---|
| $n=20$ (un mois) | $\times 14{,}7$ | forte | variance : la pente danse |
| $n=60$ (un trimestre) | $\times 2{,}8$ | moyenne | — |
| $n=120$ (six mois) | $\times 1$ | faible | biais : la pente est en retard |

C'est le compromis biais–variance usuel, et il n'a pas de solution universelle :
il dépend de la vitesse à laquelle le titre change de régime. Le dépôt tranche en
calculant **les deux** fenêtres, 20 et 120, côte à côte
([`import_societe.md`](../../../../../python/import_societe.md)) : la
comparaison de `VAL_20` et `VAL_120` — la droite courte au-dessus ou en dessous
de la longue — est laissée à la lecture plutôt que figée dans une règle.

## 5.4 — Le pivot bouge à chaque séance

Le [module 1](01-du-point-a-la-bande.md#13--le-canal-pivote-au-point-moyen)
établit que le canal pivote en $\bigl(E(T), E(V)\bigr)$. Sur une fenêtre
glissante, ce point avance d'une séance à chaque pas et son ordonnée est une
moyenne mobile — c'est `E_n` du CSV.

Le canal glissant subit donc simultanément une **translation** (le pivot avance)
et une **rotation** (la pente est réestimée). D'où deux propriétés contre-intuitives :

- La sortie d'une observation par la **gauche** de la fenêtre déplace le canal
  autant que l'entrée d'une observation nouvelle par la droite. Un canal peut
  donc « casser » sans qu'il ne se passe rien aujourd'hui, simplement parce
  qu'un point ancien vient d'être oublié.
- Le point le plus récent entre dans la fenêtre au **levier maximal**
  ($h(n) = (4n-2)/(n(n+1))$, module 3) : c'est celui qui tord le plus la droite.
  Il repart ensuite vers le centre, où son influence est minimale, avant de
  ressortir par la gauche à levier maximal de nouveau.

## 5.5 — Ce qu'il faut publier avec un canal glissant

Un canal glissant se cite avec **quatre** informations, faute de quoi il n'est
pas reproductible :

1. la **longueur de fenêtre** $n$ ;
2. la **convention de largeur** et son paramètre — $\pm 2s$, enveloppe, quantile
   ([module 2](02-les-trois-largeurs.md)) ;
3. la **date** à laquelle le canal est lu ;
4. le fait qu'il soit **glissant**, et non fixe.

Deux canaux qui diffèrent par le premier point ne se comparent pas en largeur
([module 2](02-les-trois-largeurs.md#21--lenveloppe-des-résidus)) ;
deux canaux qui diffèrent par le quatrième ne se comparent pas du tout.

---

⬅️ [Module 4 — Sorties de canal](04-sorties-de-canal.md) ·
➡️ [Module 6 — Exemple chiffré : Airbus](06-exemple-chiffre-airbus.md)
