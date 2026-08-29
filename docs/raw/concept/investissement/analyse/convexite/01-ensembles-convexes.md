# Module 1 — Ensembles convexes

**Durée : 45 min.** Prérequis : aucun, hormis le produit scalaire du[module 1 d'algèbre](../../algebre/01-produit-scalaire-et-norme.md).

> **La question traitée.** Avant les fonctions convexes, les ensembles : lesquels, et pourquoi
> ceux-là ?

**Ce qui est en jeu.** L'ensemble des portefeuilles admissibles — poids positifs de somme 1 — est
convexe. C'est cette propriété, et elle seule, qui donne un sens à la phrase « mélanger deux
portefeuilles admissibles en donne un troisième ». Tout le module 8 en dépendra.

---

## 1.1 Le segment, puis la définition

> **Définition.** $C\subset\mathbb R^d$ est **convexe** si, pour tous $x,y\in C$ et tout $\lambda\in[0,1]$,
> $$\lambda x+(1-\lambda)y\;\in\;C .$$

Autrement dit : **le segment joignant deux points de $C$ reste dans $C$**. Aucune autre propriété n'est demandée — ni ouverture, ni fermeture, ni bornitude.

Le point $\lambda x+(1-\lambda)y$ est une **combinaison convexe** de $x$ et $y$ : une moyenne pondérée, à poids positifs de somme 1. Le vocabulaire est déjà celui des portefeuilles.

| Convexe                                             | Non convexe                            |
| --------------------------------------------------- | -------------------------------------- |
| Un intervalle de $\mathbb R$                        | $\mathbb R\setminus\{0\}$              |
| Une boule $\{x:\lVert x-a\rVert\le r\}$             | Une sphère $\{x:\lVert x-a\rVert=r\}$  |
| Un demi-espace $\{x:\langle a,x\rangle\le b\}$      | $\{x:\langle a,x\rangle= b\}\cup\{0\}$ |
| Un sous-espace vectoriel, un sous-espace affine     | Une réunion de deux disques disjoints  |
| $\{x\in\mathbb R^d:\ x_i\ge0\}$ (l'orthant positif) | $\{x:\ x_1x_2\ge1\}$                   |

⚠️ **Un ensemble convexe n'a pas de « creux », mais il peut être non borné, vide, ou réduit à un
point.** L'ensemble vide et les singletons sont convexes — convention utile, jamais gênante.

---

## 1.2 Les trois exemples qui serviront

### ① Le simplexe des portefeuilles

$$\Delta_d=\Big\{w\in\mathbb R^d\ :\ w_i\ge0\ \text{pour tout }i,\quad \sum_{i=1}^d w_i=1\Big\}$$

C'est l'ensemble des portefeuilles **sans vente à découvert** et **entièrement investis**.
Convexité : si $w$ et $w'$ y sont, les coordonnées de $\lambda w+(1-\lambda)w'$ sont positives (somme de positifs) et somment à $\lambda\cdot1+(1-\lambda)\cdot1=1$. $\blacksquare$

> 🔑 **Lecture financière.** Mélanger deux portefeuilles admissibles dans les proportions
> $\lambda$ et $1-\lambda$ donne un portefeuille admissible. Cette phrase, qui paraît une évidence, est **exactement** la convexité de $\Delta_d$ — et c'est elle qui autorisera au module 8 à écrire $\rho(\lambda X+(1-\lambda)Y)\le\lambda\rho(X)+(1-\lambda)\rho(Y)$.

Autoriser la vente à découvert revient à retirer la contrainte $w_i\ge0$ : l'ensemble $\{w:\sum_i w_i=1\}$ reste convexe — c'est un sous-espace **affine**. Il est en revanche non borné, ce qui aura des conséquences au [module 7](07-convexite-en-dimension-n.md).

### ② Les ensembles définis par des contraintes linéaires

$$P=\{x\in\mathbb R^d\ :\ Ax\le b\}$$

Un **polyèdre** : une intersection de demi-espaces. Toutes les contraintes usuelles d'un portefeuille (budget, plafond par ligne, exposition sectorielle maximale) sont de cette forme, et l'ensemble admissible reste donc convexe.

### ③ Les ensembles de sous-niveau d'une fonction convexe

$$S_c=\{x\ :\ f(x)\le c\}$$

Si $f$ est convexe, $S_c$ est convexe pour tout $c$ (démonstration au [§ 2.4](02-fonctions-convexes.md)). Exemple concret : « les portefeuilles dont la variance ne dépasse pas $c$ » est un ensemble convexe.

⚠️ **La réciproque est fausse.** Tous les ensembles de sous-niveau de $f(x)=\sqrt{|x|}$ sont des
intervalles — donc convexes — alors que $f$ n'est pas convexe. Une telle fonction est dite
**quasi-convexe** ; c'est une propriété strictement plus faible, et elle ne suffit à presque aucun des théorèmes de ce cours. Le [module 8](08-convexite-et-mesures-de-risque.md) montrera que la VaR est précisément dans ce cas.

---

## 1.3 Les opérations qui préservent la convexité

| Opération                                          | Convexe ? | Pourquoi                                                 |
| -------------------------------------------------- | --------- | -------------------------------------------------------- |
| Intersection $\bigcap_{i\in I}C_i$, **quelconque** | ⭐ Oui     | $x,y$ dans tous les $C_i$ $\Rightarrow$ le segment aussi |
| Réunion $C_1\cup C_2$                              | **Non**   | Deux disques disjoints                                   |
| Image affine $\{Ax+b:\ x\in C\}$                   | Oui       | $A(\lambda x+(1-\lambda)y)+b$ se redistribue             |
| Image réciproque affine $\{x:\ Ax+b\in C\}$        | Oui       | Même calcul                                              |
| Somme de Minkowski $C_1+C_2$                       | Oui       | Sommer deux segments                                     |
| Produit cartésien $C_1\times C_2$                  | Oui       | Coordonnée par coordonnée                                |

> 🔑 **La stabilité par intersection est la propriété de travail.** Elle dit qu'**empiler des
> contraintes convexes laisse un problème convexe**. Un portefeuille soumis à dix contraintes
> linéaires plus un plafond de variance reste un problème convexe — donc résoluble avec les
> garanties du [module 6](06-minimisation-convexe.md). Ajouter une contrainte non convexe (par exemple « au plus 5 lignes non nulles ») détruit tout, d'un coup.

---

## 1.4 Enveloppe convexe

> **Définition.** L'**enveloppe convexe** $\operatorname{conv}(A)$ est le plus petit convexe contenant $A$ — c'est-à-dire l'intersection de tous les convexes qui contiennent $A$  (intersection licite par le § 1.3).

Description constructive : $\operatorname{conv}(A)$ est l'ensemble des combinaisons convexes finies de points de $A$,
$$\operatorname{conv}(A)=\Big\{\sum_{k=1}^m\lambda_k a_k\ :\ m\in\mathbb N^*,\ a_k\in A,\
\lambda_k\ge0,\ \sum_k\lambda_k=1\Big\} .$$

**Exemple.** $\Delta_d=\operatorname{conv}(e_1,\dots,e_d)$ : le simplexe est l'enveloppe convexe des $d$ portefeuilles « tout sur un seul actif ». Ces $d$ points en sont les **points extrêmes** — ceux qui ne sont combinaison convexe d'aucun autre couple de points de $\Delta_d$.

> 📐 **Pourquoi les points extrêmes comptent.** Un critère **linéaire** optimisé sur un convexe
> compact atteint son optimum en un point extrême. C'est ce qui fait qu'un portefeuille qui
> maximise le seul rendement espéré, sans contrainte de risque, met **tout** sur un seul actif :
> l'optimum est un sommet du simplexe. Il faut un critère strictement convexe — la variance — pour que l'optimum rentre à l'intérieur et que la diversification apparaisse ([module 7](07-convexite-en-dimension-n.md)).

---

## 1.5 Projection sur un convexe fermé

Le [module 4 d'algèbre](../../algebre/04-projection-orthogonale.md) projette sur un **sous-espace**. Le résultat vaut en réalité sur n'importe quel convexe fermé, et c'est la convexité — non la linéarité — qui le porte.

> **Théorème (projection).** Soit $C\subset\mathbb R^d$ **convexe fermé non vide** et $x\in\mathbb R^d$. Il existe un **unique** $p_C(x)\in C$ tel que $\|x-p_C(x)\|=\min_{y\in C}\|x-y\|$. Il est caractérisé par
> $$\big\langle\, x-p_C(x),\ y-p_C(x)\,\big\rangle\;\le\;0\qquad\text{pour tout }y\in C .$$

**L'unicité, qui est le point intéressant.** Supposons deux minimiseurs $p\ne q$, de distance commune $m$ à $x$. Leur milieu $\frac{p+q}2$ appartient à $C$ **par convexité**, et l'identité du parallélogramme donne

$$\Big\|x-\frac{p+q}2\Big\|^2=\frac{\|x-p\|^2+\|x-q\|^2}{2}-\frac{\|p-q\|^2}{4}
=m^2-\frac{\|p-q\|^2}{4}\;<\;m^2 .$$

Le milieu est **strictement plus proche** que $p$ et $q$ : contradiction. $\blacksquare$

> 🔑 **Retenez ce mécanisme, il resservira trois fois.** *Deux optima distincts $\Rightarrow$ leur milieu est admissible (convexité de l'ensemble) et fait mieux (stricte convexité du critère) $\Rightarrow$ contradiction.* C'est exactement l'argument d'unicité du [§ 6.3](06-minimisation-convexe.md), et il ne coûte jamais plus de trois lignes.

⚠️ Sur un ensemble **non convexe**, l'unicité tombe : le projeté du centre d'un cercle sur ce cercle est... tout le cercle. Sur un ensemble non **fermé**, c'est l'existence qui tombe.

---

## 1.6 Simulation

### S1.1 — Le simplexe est convexe, la sphère ne l'est pas

```python
import numpy as np

rng = np.random.default_rng(1)

def dans_simplexe(w, tol=1e-9):
    return (w >= -tol).all() and abs(w.sum() - 1) < tol

# deux portefeuilles admissibles tirés au hasard sur le simplexe
w1, w2 = rng.dirichlet(np.ones(5)), rng.dirichlet(np.ones(5))
ok = all(dans_simplexe((1 - t) * w1 + t * w2) for t in np.linspace(0, 1, 1001))
print("segment inclus dans le simplexe :", ok)

# la sphère unité : le milieu de deux points opposés est 0, qui n'y est pas
u = rng.normal(size=5); u /= np.linalg.norm(u)
milieu = 0.5 * u + 0.5 * (-u)
print(f"norme du milieu de u et -u : {np.linalg.norm(milieu):.3f}  (attendu 1 si convexe)")

# projection sur le simplexe : unique, et le résidu forme un angle obtus avec C - p
x = rng.normal(size=5)
grille = rng.dirichlet(np.ones(5), size=200_000)
p = grille[np.linalg.norm(grille - x, axis=1).argmin()]
angles = (grille - p) @ (x - p)
print(f"projeté approché : {np.round(p, 3)}")
print(f"part des y de C avec <x-p, y-p> > 1e-3 : {(angles > 1e-3).mean():.4f}  (attendu ~0)")
```

La dernière ligne teste la **caractérisation variationnelle** du § 1.5 : vue depuis le projeté,
aucune direction admissible ne rapproche de $x$. C'est la même condition que celle qui
définira l'optimalité au [§ 6.4](06-minimisation-convexe.md) — ici sur un critère quadratique,
là sur un critère convexe quelconque.

---

## 1.7 Exercices

**E1.1.** Montrer que l'intersection d'une famille **quelconque** (même infinie) de convexes est
convexe, et donner un exemple où une réunion de deux convexes ne l'est pas.

**E1.2.** Le simplexe $\Delta_3$ est-il borné ? Fermé ? Et l'ensemble
$\{w\in\mathbb R^3:\sum_iw_i=1\}$ des portefeuilles avec vente à découvert autorisée ?
*Conséquence pour l'existence d'un minimum (à relier au [§ 6.5](06-minimisation-convexe.md)).*

**E1.3.** Montrer que $\{x\in\mathbb R^2:\ x_1x_2\ge1,\ x_1>0\}$ **est** convexe, alors que
$\{x:\ x_1x_2\ge1\}$ ne l'est pas. *Que s'est-il passé ?*

**E1.4.** Soit $\Sigma$ une matrice de covariance. Montrer que
$\{w\in\Delta_d:\ w^{\top}\Sigma w\le c\}$ est convexe. *(Admettre la convexité de
$w\mapsto w^{\top}\Sigma w$, démontrée au [§ 7.3](07-convexite-en-dimension-n.md).)*

**E1.5.** Montrer que l'ensemble des portefeuilles ayant **au plus deux lignes non nulles** n'est
pas convexe, en dimension 3. *Pourquoi cette contrainte, très demandée en pratique, rend-elle le
problème d'optimisation d'une autre nature ?*

**E1.6.** Reprendre la démonstration d'unicité du § 1.5 et identifier **exactement** l'endroit où
la convexité de $C$ est utilisée. *Que devient l'énoncé si $C$ est fermé mais non convexe ?*

---

## 1.8 À retenir

- **Convexe** = stable par segment : $x,y\in C\Rightarrow\lambda x+(1-\lambda)y\in C$.
- Le **simplexe** $\Delta_d$ des portefeuilles, les **polyèdres** de contraintes linéaires et les
  **sous-niveaux** d'une fonction convexe sont les trois convexes de ce dépôt.
- ⭐ La convexité est stable par **intersection quelconque** et par application **affine** ;
  jamais par réunion. Empiler des contraintes convexes garde un problème convexe.
- Un critère **linéaire** s'optimise en un **point extrême** — d'où la concentration ; il faut un
  critère **strictement convexe** pour que la diversification apparaisse.
- **Projection** : sur un convexe fermé non vide, elle existe et est **unique**, caractérisée par
  $\langle x-p_C(x),y-p_C(x)\rangle\le0$. L'argument du milieu qui la démontre resservira à
  chaque unicité du cours.

---

⬅️ [🏠 Sommaire](README.md) ·
➡️ [Module 2 — Fonctions convexes](02-fonctions-convexes.md)
