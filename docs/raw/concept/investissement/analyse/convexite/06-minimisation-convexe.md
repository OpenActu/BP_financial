# Module 6 — Minimisation convexe ⭐

**Durée : 1 h 15.** Prérequis : modules [1](01-ensembles-convexes.md) à
[3](03-criteres-differentiels.md).

> **La question traitée.** Que gagne-t-on, exactement, à minimiser une fonction **convexe** plutôt
> qu'une fonction quelconque ?

**Ce qui est en jeu.** [`modele.md`](../../modele/modele.md) écrit, à l'étape 1 : *« quadratique de
coefficient dominant $1>0$, donc strictement convexe : son unique point critique est le minimum
global »*. Cette incise contient trois théorèmes. Ce module les démontre, puis relit la preuve
complète en quelques lignes.

---

## 6.1 Le problème

$$\min_{x\in C}f(x),\qquad C\ \text{convexe},\ f\ \text{convexe sur }C .$$

C'est ce qu'on appelle un **problème convexe** — et la convexité de $C$ **comme** celle de $f$ y
sont indispensables. Quatre propriétés le distinguent d'un problème d'optimisation quelconque :

| Propriété | Cas convexe | Cas général |
|---|---|---|
| Minimum local | **Est** global (§ 6.2) | Ne dit rien |
| Ensemble des solutions | **Convexe** (§ 6.3) | Quelconque |
| Point critique | **Suffit** (§ 6.4) | Nécessaire seulement |
| Vérifier qu'on a fini | **Possible** localement | Impossible sans exploration globale |

> 🔑 **La quatrième ligne est celle qui compte en pratique.** Sur un problème non convexe, aucun
> calcul **local** ne permet d'affirmer qu'on tient l'optimum : il faudrait comparer avec tout le
> reste du domaine. Sur un problème convexe, la condition du § 6.4 est une **preuve** locale d'un
> fait global.

---

## 6.2 Tout minimum local est global

> **Théorème.** Soit $f$ convexe sur un convexe $C$. Si $x^\star$ est un minimum **local** de $f$
> sur $C$, alors c'est un minimum **global**.

**Démonstration.** Soit $y\in C$ quelconque. Pour $\lambda\in\,]0,1]$ petit, le point
$m_\lambda=x^\star+\lambda(y-x^\star)$ appartient à $C$ (convexité) et est aussi proche qu'on veut
de $x^\star$. La minimalité locale donne $f(x^\star)\le f(m_\lambda)$ pour $\lambda$ assez petit,
et la convexité majore le second membre :

$$f(x^\star)\;\le\;f\big(m_\lambda\big)\;\le\;(1-\lambda)f(x^\star)+\lambda f(y).$$

En retranchant $(1-\lambda)f(x^\star)$ et en divisant par $\lambda>0$ : $f(x^\star)\le f(y)$.
$\blacksquare$

⚠️ **Les deux hypothèses servent, et à deux endroits différents** : la convexité de $C$ pour que
$m_\lambda$ soit admissible, celle de $f$ pour la majoration. Retirer l'une des deux détruit la
conclusion.

---

## 6.3 Unicité

> **Proposition.** L'ensemble $\operatorname{Argmin}_Cf$ des minimiseurs est **convexe**. Si $f$
> est **strictement** convexe, il contient au plus un point.

**Démonstration.** Soient $x,y$ deux minimiseurs, de valeur commune $m$. Pour $\lambda\in\,]0,1[$,
$\lambda x+(1-\lambda)y\in C$ et

$$f\big(\lambda x+(1-\lambda)y\big)\;\le\;\lambda m+(1-\lambda)m=m .$$

Comme $m$ est le minimum, il y a **égalité** : le segment entier est fait de minimiseurs, d'où la
convexité de l'ensemble. Si $f$ est strictement convexe et $x\ne y$, l'inégalité ci-dessus est
**stricte**, ce qui contredit la minimalité. Donc $x=y$. $\blacksquare$

> 🔑 **C'est l'argument du milieu du [§ 1.5](01-ensembles-convexes.md)**, tel quel. Il apparaît
> pour la troisième fois : projection sur un convexe, unicité d'un minimiseur, et il servira
> encore au [§ 7.5](07-convexite-en-dimension-n.md) pour le portefeuille à variance minimale.

**Ce que la stricte convexité achète.** Sans elle, l'optimum peut être tout un segment : minimiser
$f(x)=\max(0,\lvert x\rvert-1)$ donne $\operatorname{Argmin}=[-1,1]$. Le minimum **existe** et sa
**valeur** est unique ; c'est le **point** qui ne l'est pas.

---

## 6.4 Les conditions d'optimalité

### ① Sans contrainte : annuler la dérivée suffit

> **Théorème.** $f$ convexe dérivable sur un ouvert. Alors
> $$x^\star\ \text{minimise } f\iff f'(x^\star)=0 .$$

($\Leftarrow$) est l'inégalité de la tangente ([§ 3.3](03-criteres-differentiels.md)) :
$f(y)\ge f(x^\star)+f'(x^\star)(y-x^\star)=f(x^\star)$. ($\Rightarrow$) est vrai pour toute
fonction dérivable. $\blacksquare$

> ⚠️ **C'est le sens $\Leftarrow$ qui est le cadeau**, et il est faux hors convexité : $x^3$ a une
> dérivée nulle en 0 sans y avoir de minimum. **Annuler une dérivée ne démontre rien** — sauf sur
> une fonction convexe, où cela démontre tout.

### ② Sur un convexe : l'inégalité variationnelle

> **Théorème.** $f$ convexe dérivable, $C$ convexe. Alors
> $$x^\star\ \text{minimise } f\ \text{sur }C\iff
> \big\langle \nabla f(x^\star),\ y-x^\star\big\rangle\;\ge\;0\quad\text{pour tout }y\in C .$$

**Lecture** : depuis l'optimum, **aucune direction admissible ne descend**. Si $x^\star$ est à
l'intérieur de $C$, toutes les directions sont admissibles dans les deux sens, et la condition se
réduit à $\nabla f(x^\star)=0$ : on retrouve ①.

📐 C'est **exactement** la caractérisation de la projection du
[§ 1.5](01-ensembles-convexes.md), écrite pour $f(y)=\lVert x-y\rVert^2$ dont le gradient est
$-2(x-y)$. La projection est donc *un cas particulier* de minimisation convexe — et non l'inverse.

### ③ Contraintes d'égalité linéaires : Lagrange devient suffisant

Pour $\min f(x)$ sous $Ax=b$ avec $f$ convexe :

$$\exists\,\nu\ :\ \nabla f(x^\star)=A^{\top}\nu\ \ \text{et}\ \ Ax^\star=b
\qquad\Longleftrightarrow\qquad x^\star\ \text{optimal.}$$

En général, les conditions de Lagrange sont **nécessaires** ; sous convexité, elles deviennent
**suffisantes**. C'est ce qui rend le calcul du portefeuille à variance minimale
([§ 7.5](07-convexite-en-dimension-n.md)) non seulement faisable, mais **concluant**.

> 📚 Les contraintes d'inégalité $g_i(x)\le0$ relèvent des conditions **KKT**, hors programme ici :
> le principe est le même — sous convexité et une condition de qualification (Slater), elles
> passent de nécessaires à suffisantes.

---

## 6.5 Existence : la convexité n'y suffit pas

> ⚠️ **La convexité ne garantit pas qu'un minimum existe.** $f(x)=e^x$ est strictement convexe sur
> $\mathbb R$ et n'atteint jamais son infimum (qui vaut 0). $f(x)=-x$ non plus.

Il faut une hypothèse supplémentaire, de nature **topologique** :

| Hypothèse | Énoncé | Conclusion |
|---|---|---|
| **Compacité** | $C$ fermé borné, $f$ continue | Minimum atteint (Weierstrass) |
| **Coercivité** | $f(x)\to+\infty$ quand $\lVert x\rVert\to\infty$ | Minimum atteint sur $C$ fermé |

**Le cas quadratique**, qui est celui de tout ce dépôt : $f(x)=x^{\top}Ax+b^{\top}x+c$ est
coercive **si et seulement si** $A$ est définie positive ($A\succ0$). Si $A$ est seulement
semi-définie positive, la fonction est convexe mais peut être plate — voire décroissante — dans
les directions du noyau.

> 🔑 **Trois questions, à ne jamais confondre.** *Le minimum existe-t-il ?* (topologie :
> compacité, coercivité). *Est-il unique ?* (stricte convexité). *Comment le trouver ?*
> (condition d'optimalité). La convexité répond à la deuxième et à la troisième, **jamais à la
> première**.

---

## 6.6 `modele.md` relu

Le document minimise
$S(v_0,r)=\frac1n\sum_i\big(V_i-v_0-rT_i\big)^2$. Voici la preuve, avec le vocabulaire de ce
module.

**① $S$ est convexe.** $(v_0,r)\mapsto V_i-v_0-rT_i$ est **affine** ; $t\mapsto t^2$ est convexe
croissante sur $\mathbb R_+$ — plus simplement, $t\mapsto t^2$ composée avec une affine est
convexe ([§ 2.3](02-fonctions-convexes.md)) ; une **somme** de convexes est convexe. Aucun calcul
de dérivée n'est nécessaire.

**② La minimisation en deux temps est licite.**
$\min_{v_0,r}S=\min_r\big(\min_{v_0}S\big)$ : c'est toujours vrai pour un infimum, mais
[`modele.md`](../../modele/modele.md) prend soin de noter que l'infimum intérieur est **atteint**. La
convexité donne mieux :

> **Proposition (minimisation partielle).** Si $F(x,y)$ est convexe **conjointement**, alors
> $\varphi(x)=\inf_yF(x,y)$ est convexe.

C'est pourquoi la fonction $\varphi(r)$ de l'étape 3 est encore convexe — ce que le document
constate ensuite sur sa forme explicite, mais qui était acquis d'avance.

**③ La forme canonique est la preuve la plus courte.** L'étape 4 écrit

$$\varphi(r)=\operatorname{Var}(T)\Big(r-\tfrac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)}\Big)^2
+\Big(\operatorname{Var}(V)-\tfrac{\operatorname{Cov}(V,T)^2}{\operatorname{Var}(T)}\Big).$$

Le premier terme est $\ge0$ et s'annule en un point unique ; le second est constant. **Il n'y a
même pas besoin d'invoquer la convexité** : la forme canonique *est* la démonstration, minimum et
minimiseur compris. C'est le cas particulier où l'on peut se passer de toute la théorie —
précisément parce que la fonction est quadratique.

**④ L'unicité tient à $\operatorname{Var}(T)>0$.** C'est l'hypothèse annoncée en tête de
`modele.md`. Si les $T_i$ sont tous égaux, $\operatorname{Var}(T)=0$, la fonction $\varphi$ est
**constante** : convexe, mais pas strictement — l'optimum est toute une droite. Le § 6.3 dit
exactement cela.

> 🔑 **Ce que la relecture apporte.** Le calcul de `modele.md` est correct sans ce module ; ce
> module dit **pourquoi** il l'est, et ce qui casserait si l'on changeait le critère. Remplacer
> les carrés par des valeurs absolues (régression médiane) garde la convexité — donc les
> théorèmes — mais perd la **stricte** convexité, donc l'unicité : le minimiseur peut être un
> segment.

---

## 6.7 Simulations

### S6.1 — Convexe : tous les chemins mènent au même point

```python
import numpy as np

rng = np.random.default_rng(6)

def descente(f, df, x0, pas=0.01, n=20_000):
    x = float(x0)
    for _ in range(n):
        x -= pas * df(x)
    return x

f_cv,  df_cv  = lambda x: x ** 4 + 2 * x ** 2 - 3 * x, lambda x: 4 * x ** 3 + 4 * x - 3
f_ncv, df_ncv = (lambda x: x ** 4 - 8 * x ** 2 + x,
                 lambda x: 4 * x ** 3 - 16 * x + 1)

departs = rng.uniform(-4, 4, 8)
print("convexe     :", np.round([descente(f_cv,  df_cv,  x0) for x0 in departs], 5))
print("non convexe :", np.round([descente(f_ncv, df_ncv, x0) for x0 in departs], 5))
```

Sur la convexe, les huit points d'arrivée sont **identiques** : le minimum est unique et global.
Sur la non convexe, ils se répartissent entre deux vallées — et **rien, localement, ne dit
laquelle est la bonne**.

### S6.2 — Vérifier la relecture de `modele.md`

```python
n = 40
T = np.arange(1, n + 1)
V = 100 + 0.8 * T + rng.normal(0, 3, n)

# la solution fermee
r_star = np.cov(V, T, bias=True)[0, 1] / T.var()
v0_star = V.mean() - r_star * T.mean()

# le balayage brut : la surface est-elle convexe, et le minimum est-il bien la?
S = lambda v0, r: np.mean((V - v0 - r * T) ** 2)
gr_v0 = np.linspace(v0_star - 5, v0_star + 5, 401)
gr_r = np.linspace(r_star - .5, r_star + .5, 401)
Z = np.array([[S(a, b) for b in gr_r] for a in gr_v0])
i, j = np.unravel_index(Z.argmin(), Z.shape)
print(f"solution fermee : v0={v0_star:.4f}  r={r_star:.4f}")
print(f"minimum sur grille : v0={gr_v0[i]:.4f}  r={gr_r[j]:.4f}")

# convexite le long de segments aleatoires du plan (v0, r)
p1, p2 = rng.normal(size=(2, 2)) * 3 + [v0_star, r_star]
lam = np.linspace(0, 1, 501)
seg = np.array([S(*(l * p1 + (1 - l) * p2)) for l in lam])
print("convexe le long du segment :", (seg[2:] - 2 * seg[1:-1] + seg[:-2] >= -1e-9).all())
```

La dernière ligne teste la convexité **le long d'un segment**, qui est la seule définition dont on
dispose en dimension 2 — et le [module 7](07-convexite-en-dimension-n.md) montrera que cela suffit.

---

## 6.8 Exercices

**E6.1.** Démontrer que tout minimum local d'une fonction convexe est global, puis exhiber une
fonction **non** convexe ayant un minimum local qui n'est pas global — et dire quelle ligne de la
démonstration échoue.

**E6.2.** Montrer que $\operatorname{Argmin}f$ est convexe, et donner une fonction convexe dont
l'ensemble des minimiseurs est un segment de longueur 2.

**E6.3.** $f(x)=e^x$ sur $\mathbb R$ : convexe, bornée inférieurement, sans minimum. Quelle
hypothèse du § 6.5 manque-t-il ? Ajouter une contrainte pour que le minimum existe.

**E6.4.** Soit $f(x)=\frac12x^{\top}Ax-b^{\top}x$ avec $A$ symétrique. À quelle condition $f$
est-elle convexe ? Strictement convexe ? Coercive ? *Traiter les trois cas
$A=\begin{pmatrix}2&0\\0&1\end{pmatrix}$, $\begin{pmatrix}1&1\\1&1\end{pmatrix}$,
$\begin{pmatrix}1&0\\0&-1\end{pmatrix}$.*

**E6.5.** Reprendre la régression par valeur absolue $\min\sum_i\lvert V_i-v_0-rT_i\rvert$.
Montrer que le critère est convexe, non strictement. *Sur un exemple à 4 points, exhiber deux
solutions distinctes.*

**E6.6.** Démontrer la proposition de minimisation partielle du § 6.6 ②. *(Piste : partir de deux
points $(x_1,y_1)$ et $(x_2,y_2)$ presque optimaux et appliquer la convexité conjointe.)*

---

## 6.9 À retenir

- Un **problème convexe** = minimiser une fonction convexe sur un ensemble convexe. Les deux
  hypothèses servent séparément.
- ⭐ **Tout minimum local est global**, et **l'ensemble des minimiseurs est convexe** — réduit à un
  point si $f$ est **strictement** convexe.
- ⭐ **$\nabla f(x^\star)=0$ suffit** sur une convexe. Hors convexité, cela ne prouve rien.
  Sur un convexe $C$ avec bord : $\langle\nabla f(x^\star),y-x^\star\rangle\ge0$ pour tout $y\in C$.
- **Lagrange devient suffisant** sous convexité — d'où la validité du calcul de portefeuille du
  module 7.
- ⚠️ **La convexité ne donne pas l'existence** : il y faut compacité ou coercivité. Trois
  questions distinctes — existence, unicité, caractérisation — et la convexité n'en traite que
  deux.
- La preuve de [`modele.md`](../../modele/modele.md) est un problème convexe quadratique : la **forme
  canonique** en donne le minimum sans dériver, et l'unicité tient à la seule hypothèse
  $\operatorname{Var}(T)>0$.

---

⬅️ [Module 5 — Jensen probabiliste](05-jensen-probabiliste.md) ·
➡️ [Module 7 — Convexité en dimension $n$](07-convexite-en-dimension-n.md) ·
🏠 [Sommaire](README.md)
