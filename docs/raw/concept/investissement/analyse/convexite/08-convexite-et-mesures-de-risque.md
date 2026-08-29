# Module 8 — Convexité et mesures de risque ⭐

**Durée : 1 h 15.** Prérequis : modules [5](05-jensen-probabiliste.md) et
[7](07-convexite-en-dimension-n.md), et la
[loi normale](../../statistique/mathematique/06f-loi-normale.md) pour la VaR.

> **La question traitée.** Une mesure de risque doit-elle être convexe ? Et que se passe-t-il
> quand elle ne l'est pas ?

**Ce qui est en jeu.** La convexité cesse ici d'être une commodité technique pour devenir un
**axiome économique** : elle est la traduction mathématique exacte de « diversifier ne peut pas
augmenter le risque ». La mesure la plus utilisée de l'industrie financière — la VaR — ne la
vérifie pas, et ce module le montre sur un exemple à trois lignes de calcul.

---

## 8.1 Le cadre

Une **mesure de risque** est une fonction $\rho$ qui associe à une perte aléatoire $L$ un nombre
$\rho(L)$ : le capital à immobiliser, la limite à respecter, le chiffre à reporter.

> **Convention.** On travaille sur la **perte** $L=-\text{gain}$, positive quand on perd. Toutes
> les inégalités sont alors dans le sens intuitif : plus $\rho$ est grand, plus c'est risqué.

Les quatre axiomes d'Artzner–Delbaen–Eber–Heath (1999) définissent une mesure **cohérente** :

| Axiome | Énoncé | Ce qu'il exige |
|---|---|---|
| **Monotonie** | $L_1\le L_2$ p.s. $\Rightarrow\rho(L_1)\le\rho(L_2)$ | Perdre plus est plus risqué |
| **Invariance par translation** | $\rho(L+c)=\rho(L)+c$ | Ajouter du liquide réduit le besoin de capital d'autant |
| **Homogénéité positive** | $\rho(\alpha L)=\alpha\rho(L)$, $\alpha\ge0$ | Doubler la position double le risque |
| ⭐ **Sous-additivité** | $\rho(L_1+L_2)\le\rho(L_1)+\rho(L_2)$ | **La diversification ne pénalise jamais** |

> 🔑 **Sous homogénéité, sous-additivité et convexité sont équivalentes.**
> $$\rho\big(\lambda L_1+(1-\lambda)L_2\big)\le\lambda\rho(L_1)+(1-\lambda)\rho(L_2)
> \iff\rho(L_1+L_2)\le\rho(L_1)+\rho(L_2)$$
> Le quatrième axiome **est** donc la convexité du [module 2](02-fonctions-convexes.md), écrite sur
> des variables aléatoires au lieu de nombres.

**Pourquoi cet axiome n'est pas négociable.** S'il est violé, il existe deux portefeuilles dont la
**fusion** exige plus de capital que la somme des deux séparés. Une banque aurait alors intérêt à
scinder ses activités en filiales pour réduire ses exigences réglementaires — un arbitrage
purement comptable, sans le moindre changement économique.

---

## 8.2 Deux mesures usuelles

### La valeur en risque (VaR)

> **Définition.** $\text{VaR}_\alpha(L)=\inf\{\ell\ :\ P(L\le\ell)\ge\alpha\}$ — le **quantile**
> d'ordre $\alpha$ de la perte. Typiquement $\alpha=95\,\%$ ou $99\,\%$.

Lecture : « dans 95 % des cas, la perte ne dépasse pas $\text{VaR}_{95\%}$ ».

### La perte moyenne au-delà (CVaR, ou *expected shortfall*)

> **Définition.**$\displaystyle\text{ES}_\alpha(L)=\frac1{1-\alpha}\int_\alpha^1 \text{VaR}_u(L)\,du$,
> qui vaut$E\big(L\mid L\ge\text{VaR}_\alpha\big)$ lorsque la loi de$L$
> est continue.

Lecture : « **quand** on dépasse le seuil, on perd en moyenne $\text{ES}_\alpha$ ».

| | VaR | ES |
|---|---|---|
| Regarde | Le **seuil** de la queue | La **queue entière** |
| Monotone, translation, homogène | Oui | Oui |
| **Sous-additive** | ⚠️ **NON** (§ 8.3) | ✅ Oui (§ 8.4) |
| Cohérente | Non | Oui |
| Optimisation | **Non convexe** | **Convexe** (§ 8.5) |

---

## 8.3 ⚠️ La VaR n'est pas convexe — le contre-exemple

**La situation.** Deux obligations $A$ et $B$, de nominal 100, émises par des sociétés
**indépendantes**, chacune faisant défaut avec probabilité $4\,\%$ (perte de 100) et remboursant
intégralement sinon (perte 0).

**Chacune prise seule.** $P(L=0)=0{,}96\ge0{,}95$, donc le quantile à $95\,\%$ est atteint dès
$\ell=0$ :

$$\text{VaR}_{95\%}(A)=\text{VaR}_{95\%}(B)=\mathbf 0 .$$

**Le portefeuille moitié-moitié.** La perte $L=\frac12L_A+\frac12L_B$ prend trois valeurs :

| Perte $L$ | 0 | 50 | 100 |
|---|---|---|---|
| Probabilité | $0{,}96^2=0{,}9216$ | $2\times0{,}96\times0{,}04=0{,}0768$ | $0{,}04^2=0{,}0016$ |
| Cumulée | 0,9216 | 0,9984 | 1 |

$P(L\le0)=0{,}9216<0{,}95$ : le seuil de $95\,\%$ n'est pas atteint en 0. Il l'est en 50. Donc

$$\boxed{\ \text{VaR}_{95\%}\Big(\tfrac12L_A+\tfrac12L_B\Big)=50\;>\;
\tfrac12\text{VaR}_{95\%}(L_A)+\tfrac12\text{VaR}_{95\%}(L_B)=0\ }$$

> ⚠️ **La VaR du portefeuille diversifié est infiniment plus grande que la moyenne des VaR.** Et
> l'exemple n'a rien de pathologique : deux crédits indépendants, un seuil réglementaire standard.
> **Diversifier a augmenté la mesure de risque.**

**D'où vient l'échec.** La VaR est un **quantile** : elle ne regarde qu'un point de la
distribution et **ignore tout ce qu'il y a au-delà**. La première obligation avait une perte
possible de 100 avec probabilité $4\,\%$ — invisible pour la VaR à $95\,\%$. Le mélange rend la
perte moins grave mais **plus fréquente**, et la fréquence est précisément ce que le quantile
regarde.

> 🔑 **Techniquement : la VaR est quasi-convexe, pas convexe.** Ses ensembles de sous-niveau sont
> souvent convexes, sa valeur ne l'est pas — c'est exactement la distinction du
> [§ 1.2](01-ensembles-convexes.md), et elle coûte ici la sous-additivité.

⚠️ **Le cas gaussien est trompeur.** Si $(L_A,L_B)$ est un vecteur **gaussien**,
$\text{VaR}_\alpha(L)=\mu_L+z_\alpha\sigma_L$ est convexe en $w$ (somme d'un terme linéaire et
d'une norme, § 7.3), donc sous-additive. **La VaR se comporte bien exactement là où le monde ne se
comporte pas comme la VaR le suppose** : queues fines, pas de défaut, pas de saut. Voir le
[§ 6f.5 de statistique](../../statistique/mathematique/06f-loi-normale.md).

---

## 8.4 L'ES est convexe — et pourquoi

**Sur l'exemple précédent.** Pour une obligation seule, la queue à $5\,\%$ contient les $4\,\%$ de
défaut (perte 100) et $1\,\%$ de non-défaut (perte 0) :

$$\text{ES}_{95\%}(A)=\frac{0{,}04\times100+0{,}01\times0}{0{,}05}=80 .$$

Pour le mélange, la queue à $5\,\%$ contient $0{,}16\,\%$ de perte 100 puis $4{,}84\,\%$ de perte
50 :

$$\text{ES}_{95\%}\Big(\tfrac12L_A+\tfrac12L_B\Big)
=\frac{0{,}0016\times100+0{,}0484\times50}{0{,}05}=51{,}6\;\le\;80 .$$

| Mesure | Obligation seule | Portefeuille 50/50 | Diversification |
|---|---|---|---|
| $\text{VaR}_{95\%}$ | 0 | **50** | ❌ pénalisée |
| $\text{ES}_{95\%}$ | 80 | **51,6** | ✅ récompensée |

**Le théorème, et sa démonstration en une ligne.**

> **Théorème (Rockafellar–Uryasev).** Pour tout $\alpha\in\,]0,1[$,
> $$\text{ES}_\alpha(L)=\min_{\tau\in\mathbb R}\ \Big\{\tau+\frac1{1-\alpha}
> E\big[\max(0,\ L-\tau)\big]\Big\}$$
> et le minimum est atteint en $\tau=\text{VaR}_\alpha(L)$.

*Pourquoi cela règle la question de la convexité.* À $\tau$ fixé, la fonction
$L\mapsto\tau+\frac1{1-\alpha}E[\max(0,L-\tau)]$ est convexe en $L$ : $\max(0,\cdot)$ est convexe
([§ 2.3](02-fonctions-convexes.md)) et l'espérance est **linéaire croissante**. Un **minimum** de
fonctions convexes n'est pas convexe en général… mais ici la minimisation porte sur une variable
**auxiliaire**, et la minimisation partielle d'une fonction **conjointement** convexe est convexe
([§ 6.6 ②](06-minimisation-convexe.md)). Donc $\text{ES}_\alpha$ est convexe. $\blacksquare$

> 🔑 **Cette formule fait deux choses d'un coup.** Elle **démontre** la cohérence de l'ES, et elle
> la rend **calculable** : sur $N$ scénarios simulés, minimiser
> $\tau+\frac1{N(1-\alpha)}\sum_k\max(0,L_k-\tau)$ est un **programme linéaire**. C'est la raison
> pour laquelle l'ES a remplacé la VaR dans la réglementation bancaire (Bâle III, revue du
> portefeuille de négociation) : elle est à la fois plus juste et plus facile à optimiser.

---

## 8.5 La conséquence qui décide : optimiser

| | Minimiser la VaR | Minimiser l'ES |
|---|---|---|
| Nature du problème | **Non convexe** | **Convexe** (programme linéaire) |
| Optima locaux | Multiples | Un seul ensemble d'optima, convexe |
| Garantie du calcul | Aucune | Le [module 6](06-minimisation-convexe.md) s'applique intégralement |
| Taille traitable | Quelques dizaines de positions | Des milliers |

> ⚠️ **Un optimiseur de VaR renvoie toujours un chiffre.** Rien, dans sa sortie, n'indique qu'il
> s'est arrêté dans une vallée parmi d'autres. C'est le point du
> [§ 6.1](06-minimisation-convexe.md) : sur un problème non convexe, **aucune vérification locale
> ne prouve l'optimalité**. La convexité n'est pas un confort de mathématicien, c'est ce qui
> distingue un résultat d'une estimation plausible.

**Ce que la convexité ne répare pas.** L'ES reste une **espérance conditionnelle de queue** :
elle s'estime sur les quelques pour cent d'observations les plus extrêmes, donc avec une variance
d'estimation élevée et une sensibilité forte au modèle de queue
([§ 13.1 de statistique](../../statistique/mathematique/13-portee-et-limites-du-tcl.md)). **Une mesure cohérente
mal estimée reste mal estimée.** La convexité garantit la cohérence des comparaisons, jamais la
qualité des données.

---

## 8.6 Simulations

### S8.1 — Le contre-exemple, vérifié par énumération

```python
import numpy as np
from itertools import product

p, N = 0.04, 100.0

def var_es(valeurs, probas, alpha=0.95):
    ordre = np.argsort(valeurs)
    v, q = np.array(valeurs)[ordre], np.array(probas)[ordre]
    cum = np.cumsum(q)
    i = np.searchsorted(cum, alpha)                       # premier quantile >= alpha
    var = v[i]
    # ES : moyenne de la queue de masse 1-alpha, au-dela de VaR
    reste, tot, masse = 1 - alpha, 0.0, 0.0
    for val, pr in zip(v[::-1], q[::-1]):
        pris = min(pr, reste - masse)
        tot += pris * val
        masse += pris
        if masse >= reste - 1e-15:
            break
    return var, tot / (1 - alpha)

seule = var_es([0, N], [1 - p, p])
etats = list(product([0, N], repeat=2))
pertes = [0.5 * a + 0.5 * b for a, b in etats]
probas = [((1 - p) if a == 0 else p) * ((1 - p) if b == 0 else p) for a, b in etats]
melange = var_es(pertes, probas)

print(f"obligation seule : VaR95={seule[0]:6.2f}   ES95={seule[1]:6.2f}")
print(f"melange 50/50    : VaR95={melange[0]:6.2f}   ES95={melange[1]:6.2f}")
print(f"VaR sous-additive ? {melange[0] <= seule[0] + 1e-9}")
print(f"ES  sous-additive ? {melange[1] <= seule[1] + 1e-9}")
```

Sortie attendue : `VaR95 = 0.00` puis `50.00` (**non** sous-additive), `ES95 = 80.00` puis
`51.60` (sous-additive).

### S8.2 — La formule de Rockafellar–Uryasev

```python
rng = np.random.default_rng(8)
L = np.concatenate([rng.normal(0, 1, 199_000), rng.normal(6, 2, 1_000)])   # queue épaisse
alpha = 0.95

def objectif(tau):
    return tau + np.maximum(0, L - tau).mean() / (1 - alpha)

taus = np.linspace(np.quantile(L, 0.80), np.quantile(L, 0.999), 4001)
val = np.array([objectif(t) for t in taus])
print(f"argmin tau = {taus[val.argmin()]:.4f}   VaR95 empirique = {np.quantile(L, alpha):.4f}")
print(f"min de l'objectif = {val.min():.4f}   ES95 empirique = {L[L >= np.quantile(L, alpha)].mean():.4f}")
print("objectif convexe en tau :", (val[2:] - 2 * val[1:-1] + val[:-2] >= -1e-9).all())
```

Trois vérifications d'un coup : l'argmin **est** la VaR, la valeur minimale **est** l'ES, et la
fonction est convexe en $\tau$ — d'où l'existence d'un programme linéaire équivalent.

### S8.3 — La frontière VaR est rentrante, la frontière ES ne l'est pas

```python
# deux actifs a defaut, comme au 8.3, mais avec un poids variable
w = np.linspace(0, 1, 101)
etats = list(product([0, N], repeat=2))
courbe_var, courbe_es = [], []
for wi in w:
    pertes = [wi * a + (1 - wi) * b for a, b in etats]
    probas = [((1 - p) if a == 0 else p) * ((1 - p) if b == 0 else p) for a, b in etats]
    v, e = var_es(pertes, probas)
    courbe_var.append(v); courbe_es.append(e)

courbe_var, courbe_es = np.array(courbe_var), np.array(courbe_es)
print("VaR convexe en w :", (courbe_var[2:] - 2 * courbe_var[1:-1] + courbe_var[:-2] >= -1e-9).all())
print("ES  convexe en w :", (courbe_es[2:] - 2 * courbe_es[1:-1] + courbe_es[:-2] >= -1e-9).all())
print("VaR aux extremites :", courbe_var[0], courbe_var[-1], " au milieu :", courbe_var[50])
```

La VaR vaut 0 aux deux extrémités et 50 au milieu : une fonction qui **monte au centre du
segment** est exactement le contraire de la convexité.

---

## 8.7 Exercices

**E8.1.** Démontrer l'équivalence « homogénéité + sous-additivité $\iff$ homogénéité + convexité »
du § 8.1.

**E8.2.** Vérifier que la VaR satisfait la monotonie, l'invariance par translation et
l'homogénéité. *(Trois lignes chacune : ce sont des propriétés des quantiles.)*

**E8.3.** Reprendre le contre-exemple du § 8.3 avec une probabilité de défaut de $2\,\%$ au lieu de
$4\,\%$. La VaR à $95\,\%$ reste-t-elle non sous-additive ? *Et à $99\,\%$ ? Que conclure sur le
rôle du seuil ?*

**E8.4.** Montrer que si $(L_A,L_B)$ est gaussien, la VaR **est** sous-additive. *Où l'argument
utilise-t-il le [§ 7.3](07-convexite-en-dimension-n.md), et où utilise-t-il l'hypothèse
gaussienne ?*

**E8.5.** Démontrer que $\text{ES}_\alpha\ge\text{VaR}_\alpha$ toujours. *(Piste : la définition
intégrale et la croissance de $u\mapsto\text{VaR}_u$.)* En déduire qu'une limite de risque exprimée
en ES est **toujours** plus contraignante qu'à VaR égale.

**E8.6.** Vérifier la formule de Rockafellar–Uryasev à la main sur la loi discrète du § 8.3 : poser
$\tau$ variable, calculer l'objectif pour $\tau\in\{0,50,100\}$, et constater où est le minimum.

**E8.7 — orientée finance.** Sur une série de rendements obtenue avec `historique_sbf250.py` :
1. estimer VaR et ES empiriques à $95\,\%$ et $99\,\%$ ;
2. comparer avec les valeurs **gaussiennes** $\mu+z_\alpha\sigma$ ;
3. quel est le sens de l'écart, et lequel des deux modules — [13](../../statistique/mathematique/13-portee-et-limites-du-tcl.md)
   ou [§ 11bis.8](../../statistique/mathematique/11bis-convergence-en-loi.md) — l'avait annoncé ?

---

## 8.8 À retenir

- Les quatre axiomes de cohérence ; le quatrième — la **sous-additivité** — **est** la convexité,
  et il traduit exactement « diversifier ne peut pas pénaliser ».
- ⭐ **La VaR n'est pas convexe.** Deux obligations indépendantes à $4\,\%$ de défaut :
  $\text{VaR}_{95\%}=0$ chacune, **50** pour le mélange. L'échec vient de ce qu'un quantile ignore
  tout ce qui se passe au-delà du seuil.
- **La VaR redevient sous-additive dans le cas gaussien** — c'est-à-dire précisément là où les
  queues sont fines, donc là où la question ne se pose pas.
- ⭐ **L'ES est convexe**, par la formule variationnelle de Rockafellar–Uryasev, qui la donne comme
  minimisation d'une fonction convexe en $\tau$ — et qui la rend calculable par programmation
  linéaire.
- **La conséquence opératoire** : minimiser une VaR est un problème non convexe, dont aucun
  résultat n'est certifiable localement ; minimiser une ES est un problème convexe, auquel tout le
  [module 6](06-minimisation-convexe.md) s'applique.
- ⚠️ La cohérence ne remplace pas l'estimation : une mesure de queue reste estimée sur peu
  d'observations.

---

⬅️ [Module 7 — Convexité en dimension $n$](07-convexite-en-dimension-n.md) ·
➡️ [Module 9 — La convexité obligataire](09-la-convexite-obligataire.md) ·
🏠 [Sommaire](README.md)
