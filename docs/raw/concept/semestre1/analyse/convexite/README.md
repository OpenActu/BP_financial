# Cours — Analyse : la convexité

Cours dédié à une seule propriété — **la corde est au-dessus du graphe** — et à ce qu'elle
produit : des inégalités, des minima uniques, et une définition du risque qui récompense la
diversification. Niveau **bac+2**, à une variable puis à $n$ variables.

## Pourquoi ce cours dans ce dépôt

Trois documents de ce dépôt s'appuient sur la convexité sans jamais la démontrer.

| Où | Ce qui est utilisé | Statut là-bas |
|---|---|---|
| [`modele.md`](../../../../modele.md), étape 1 | « quadratique de coefficient dominant $>0$, donc **strictement convexe** : son unique point critique est le minimum global » | Admis en une incise |
| [`modele.md`](../../../../modele.md), étape 4 | La mise sous forme canonique, qui exhibe le minimum **sans dériver** | Admis |
| [Statistique § 2.5](../../../semestre2/statistique/mathematique/02-esperance.md) | L'**inégalité de Jensen**, $E(g(X))\ge g(E(X))$ | Énoncée, non démontrée |
| [Statistique § 15.4](../../../semestre2/statistique/mathematique/15-loi-du-chi2.md) | $E(S)<\sigma$ — le biais de l'écart type | Conséquence de Jensen, admise |

Ce cours démontre ces énoncés et en tire la suite. Il est, comme le
[cours d'algèbre](../../algebre/README.md), entièrement **déterministe** jusqu'au module 4 ; la
probabilité n'entre qu'au module 5, et elle n'y sert qu'à faire tourner une inégalité établie
avant.

> 🔑 **La question qui organise tout le cours.** Une moyenne de transformations n'est pas la
> transformation de la moyenne. La convexité est ce qui dit **dans quel sens** l'écart se fait —
> et c'est un sens toujours le même, jamais un aléa.

## Fil directeur

Une seule inégalité, écrite une fois :

$$f\big(\lambda x+(1-\lambda)y\big)\;\le\;\lambda f(x)+(1-\lambda)f(y),\qquad \lambda\in[0,1]$$

et sept déclinaisons :

- la **tangente passe sous le graphe** → module 3, l'outil de démonstration de tout le reste ;
- moyenner **avant** ou **après** → Jensen, fini (module 4) puis probabiliste (module 5) ;
- un minimum local **est** global → module 6, et la preuve de [`modele.md`](../../../../modele.md) devient
  une ligne ;
- en dimension $n$, la Hessienne **semi-définie positive** → module 7, où $w^{\top}\Sigma w$ est
  convexe parce que $\Sigma$ est une matrice de Gram ;
- **diversifier ne peut pas nuire** → module 8, et la VaR échoue à ce test ;
- une obligation gagne à la volatilité des taux → module 9, la « convexité » des praticiens, qui
  est exactement celle des mathématiciens.

## Progression

### Partie 0 — Les objets

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 1 | [Ensembles convexes](01-ensembles-convexes.md) | 45 min | Segment, combinaison convexe, simplexe des portefeuilles |
| 2 | [Fonctions convexes : définition et stabilité](02-fonctions-convexes.md) | 1 h | Épigraphe, pentes croissantes, les opérations qui préservent |
| 3 | [**Les critères différentiels**](03-criteres-differentiels.md) ⭐ | 1 h 15 | $f''\ge0$, et **la tangente sous le graphe** |

### Partie I — La machine à inégalités

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 4 | [Jensen fini et les moyennes](04-jensen-fini-et-moyennes.md) | 1 h | AM $\ge$ GM $\ge$ HM, Hölder, Minkowski |
| 5 | [**Jensen probabiliste**](05-jensen-probabiliste.md) ⭐ | 1 h 15 | Le biais de $S$, le drag de volatilité, la prime de risque |

### Partie II — L'optimisation

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 6 | [**Minimisation convexe**](06-minimisation-convexe.md) ⭐ | 1 h 15 | Local $=$ global ; `modele.md` relu en trois lignes |
| 7 | [Convexité en dimension $n$](07-convexite-en-dimension-n.md) | 1 h 15 | Hessienne $\succeq0$ ; $w^{\top}\Sigma w$ ; variance minimale |

### Partie III — Le risque

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 8 | [**Convexité et mesures de risque**](08-convexite-et-mesures-de-risque.md) ⭐ | 1 h 15 | La VaR n'est pas convexe — contre-exemple chiffré ; la CVaR l'est |
| 9 | [La convexité obligataire](09-la-convexite-obligataire.md) | 1 h | $\frac{\Delta P}{P}\approx-D\Delta y+\frac12 C\Delta y^2$, et pourquoi le second terme est un cadeau |

**Volume total** : ≈ 10 h, à répartir sur 3 à 4 semaines. Les modules se lisent **dans
l'ordre** : chacun n'utilise que les précédents.

## Parcours

| Objectif | Modules |
|---|---|
| Le minimum vital pour lire `modele.md` | 2 → 3 → 6 |
| Comprendre le biais de $S$ et le drag de volatilité | 3 → 4 → 5 |
| Optimiser un portefeuille | 1 → 6 → 7 → 8 |
| Le vocabulaire du risque | 5 → 8 → 9 |

## Les quatre modules décisifs

- **Module 3 — La tangente sous le graphe.** L'inégalité $f(y)\ge f(x)+f'(x)(y-x)$ est le seul
  outil dont on aura besoin : Jensen en découle en deux lignes, et la condition d'optimalité du
  module 6 aussi.
- **Module 5 — Jensen probabiliste.** Celui qui explique pourquoi une moyenne de rendements
  surestime la performance réalisée, pourquoi $S$ sous-estime $\sigma$, et pourquoi un investisseur
  averse paie pour éviter un risque à espérance nulle. Trois faits, une seule inégalité.
- **Module 6 — Minimisation convexe.** Celui qui transforme « j'ai annulé la dérivée » en preuve.
  Sans convexité, un point critique n'est **rien** ; avec elle, c'est le minimum global.
- **Module 8 — Les mesures de risque.** Celui qui montre que la convexité n'est pas une commodité
  technique mais un **axiome économique** : elle dit qu'un portefeuille diversifié n'est jamais
  plus risqué que la moyenne de ses parts. La VaR ne le vérifie pas, et cela s'est payé.

## Ce que ce cours ne contient pas

- **La dualité et les conditions KKT complètes** : le module 6 traite les contraintes d'égalité
  linéaires (le seul cas dont ce dépôt a besoin) et cite le reste.
- **L'algorithmique** : descente de gradient, points intérieurs, programmation quadratique ne sont
  évoqués que dans les simulations, sans étude de convergence.
- **L'analyse convexe en dimension infinie**, la théorie de la mesure, la transformée de Legendre.
- **La probabilité** : elle est empruntée au [cours de statistique](../../../semestre2/statistique/mathematique/README.md) à
  partir du module 5, jamais construite ici.

## Ce que les autres cours du dépôt apportent

| Cours | Ce qu'il fournit à celui-ci |
|---|---|
| [Algèbre linéaire](../../algebre/README.md) | Le produit scalaire (module 1), la projection (module 4), et surtout $\Sigma$ **matrice de Gram** (module 8), qui est ce qui rend $w^{\top}\Sigma w$ convexe |
| [Statistique](../../../semestre2/statistique/mathematique/README.md) | L'espérance et ses règles (module 2), la variance (module 3), la loi normale (module 6f) |
| [Loi de Student](../../../semestre3/statistique/loi-de-student/README.md) | L'usage inférentiel de $S$, dont le module 5 explique le biais |
| [Dérivation et intégration](../derivation-et-integration/README.md) | La différentiabilité, le **gradient** et la **Hessienne** dont les modules 3, 6 et 7 testent la positivité |

## Outillage

```bash
pip install numpy scipy matplotlib
```

Chaque module se conclut par une simulation courte à écrire soi-même. La convexité est un domaine
où l'intuition est **bonne en dimension 1 et mauvaise ensuite** : le contre-exemple de la VaR
(module 8) ne s'invente pas, il se calcule.

## Notations retenues dans tout le cours

| Symbole | Sens |
|---|---|
| $C$, $I$ | Un ensemble convexe, un intervalle de $\mathbb R$ |
| $\lambda$, $1-\lambda$ | Les poids d'une combinaison convexe, $\lambda\in[0,1]$ |
| $[x,y]$ | Le segment $\{\lambda x+(1-\lambda)y,\ \lambda\in[0,1]\}$ |
| $\operatorname{epi}f$ | Épigraphe $\{(x,t)\ :\ t\ge f(x)\}$ |
| $f'$, $f''$, $\nabla f$, $H_f$ | Dérivées, gradient, matrice hessienne |
| $A\succeq0$, $A\succ0$ | Matrice symétrique semi-définie positive, définie positive |
| $\Delta_d$ | Simplexe $\{w\in\mathbb R^d:\ w_i\ge0,\ \sum_i w_i=1\}$ |
| $w$, $\Sigma$ | Poids d'un portefeuille, matrice de covariance |
| $L$, $\text{VaR}_\alpha$, $\text{ES}_\alpha$ | Perte, valeur en risque, perte moyenne au-delà (module 8) |
| $D$, $C$ (module 9) | Duration modifiée et convexité d'une obligation |

## Références

| Usage | Référence |
|---|---|
| La référence, gratuite et complète | Boyd & Vandenberghe, *Convex Optimization* — ch. 2 à 4, stanford.edu/~boyd/cvxbook |
| Cours français, rigoureux | J.-B. Hiriart-Urruty, *Optimisation et analyse convexe*, EDP Sciences |
| Inégalités classiques | Hardy, Littlewood & Pólya, *Inequalities* — ch. 3 |
| Mesures de risque | Artzner, Delbaen, Eber & Heath, « Coherent Measures of Risk », *Math. Finance*, 1999 |
| CVaR et optimisation | Rockafellar & Uryasev, « Optimization of Conditional Value-at-Risk », *J. of Risk*, 2000 |
| Obligations | Fabozzi, *Bond Markets, Analysis and Strategies* — ch. duration et convexité |
