# Module 7 — Le calcul matriciel des dérivées ⭐

**Durée : 1 h 15.** Prérequis : [module 6](06-la-matrice-jacobienne.md), et le
[cours d'algèbre](../../algebre/README.md) pour trace, transposée et inverse.

> **La question traitée.** Comment dériver $w^{\top}\Sigma w$, $\lVert y-X\beta\rVert^2$ ou
> $\log\det\Sigma$ **sans écrire une seule somme indexée** ?

**Ce qui est en jeu.** [`modele.md`](../../../../modele.md) dérive à la main une somme sur $n$ termes, deux
fois, sur un modèle à **deux** paramètres. Avec $p$ variables explicatives, la même méthode devient
impraticable. Le calcul matriciel donne $\hat\beta=(X^{\top}X)^{-1}X^{\top}y$ **en trois lignes**,
valable pour tout $p$ — et il fournit au passage la Hessienne, donc la preuve que le point critique
est bien un minimum.

---

## 7.1 ⚠️ La convention, fixée une fois pour toutes

C'est la source de 90 % des erreurs : deux conventions coexistent dans la littérature, et
mélanger les deux produit des transposées fantômes.

> **Convention de ce cours.**
> - $x\in\mathbb R^n$ est un vecteur **colonne** ;
> - pour $f$ **scalaire**, $\dfrac{\partial f}{\partial x}=\nabla f$ est une **colonne** $n\times1$ ;
> - pour $f:\mathbb R^n\to\mathbb R^m$, $\dfrac{\partial f}{\partial x^{\top}}=J_f$ est
>   $m\times n$ (**une ligne par composante**) ;
> - pour $f$ scalaire et $A$ matrice, $\dfrac{\partial f}{\partial A}$ a **la même forme que $A$**,
>   de coefficient $(i,j)$ égal à $\partial f/\partial A_{ij}$.

> 🔑 **La règle de survie : compter les dimensions à chaque ligne.** Un gradient a la forme de la
> variable ; une jacobienne a autant de lignes que la fonction a de composantes. Si un produit ne
> se recolle pas, c'est le calcul — jamais la convention — qu'il faut corriger.

⚠️ Le *Matrix Cookbook* et une partie de la littérature d'apprentissage automatique utilisent la
disposition **numérateur** ($\partial f/\partial x$ en ligne pour $f$ scalaire). Les formules y
diffèrent d'une transposition. **Vérifiez toujours par différence finie** (§ 7.7) avant de recopier
une formule trouvée ailleurs.

---

## 7.2 Le formulaire vectoriel

Pour $a$ constant, $A$ constante, $x$ variable :

| $f(x)$ | Type | $\nabla f$ ou $J_f$ | Cas symétrique |
|---|---|---|---|
| $a^{\top}x=x^{\top}a$ | scalaire | $\nabla f=a$ | — |
| $Ax$ | vecteur | $J_f=A$ | — |
| $x^{\top}Ax$ | scalaire | $\nabla f=\big(A+A^{\top}\big)x$ | $=2Ax$ si $A=A^{\top}$ |
| $x^{\top}Ax$ | scalaire | $H_f=A+A^{\top}$ | $=2A$ si $A=A^{\top}$ |
| $\lVert x\rVert^2=x^{\top}x$ | scalaire | $\nabla f=2x$ | cas $A=I$ |
| $\lVert Ax-b\rVert^2$ | scalaire | $\nabla f=2A^{\top}(Ax-b)$ | ⭐ les moindres carrés |
| $u(x)^{\top}v(x)$ | scalaire | $\nabla f=J_u^{\top}v+J_v^{\top}u$ | règle du produit |
| $f\big(g(x)\big)$, $f$ scalaire | scalaire | $\nabla(f\circ g)=J_g^{\top}\,\nabla f\big(g(x)\big)$ | ⭐ chaîne |

> ⚠️ **La dernière ligne mérite un arrêt.** La règle de la chaîne du
> [§ 6.3](06-la-matrice-jacobienne.md) s'écrit $J_{f\circ g}=J_f\,J_g$ — un produit **dans cet
> ordre**. En transposant pour obtenir un gradient (colonne), l'ordre **s'inverse** :
> $\nabla(f\circ g)=J_g^{\top}\nabla f$. C'est mécanique, et c'est exactement l'endroit où l'on se
> trompe.

---

## 7.3 La méthode qui ne trompe jamais : passer par la différentielle

Plutôt que de mémoriser le formulaire, on peut le **reconstruire**. La méthode tient en deux temps.

> **① Calculer la différentielle** $\mathrm df$ en traitant $\mathrm dx$ comme un accroissement,
> avec les règles ordinaires : $\mathrm d(u+v)=\mathrm du+\mathrm dv$,
> $\mathrm d(uv)=(\mathrm du)v+u(\mathrm dv)$, $\mathrm d(A^{-1})=-A^{-1}(\mathrm dA)A^{-1}$.
>
> **② Identifier** en mettant $\mathrm df$ sous la forme canonique
> $$\mathrm df=\big\langle\nabla f,\ \mathrm dx\big\rangle
> \qquad\text{ou}\qquad
> \mathrm df=\operatorname{tr}\!\big(G^{\top}\,\mathrm dA\big)\ \Rightarrow\ \frac{\partial f}{\partial A}=G .$$

**Exemple 1 — $f(x)=x^{\top}Ax$.**

$$\mathrm df=(\mathrm dx)^{\top}Ax+x^{\top}A\,\mathrm dx
=x^{\top}A^{\top}\mathrm dx+x^{\top}A\,\mathrm dx
=\big[(A+A^{\top})x\big]^{\top}\mathrm dx
\;\Longrightarrow\;\nabla f=(A+A^{\top})x .$$

*(On a utilisé que $(\mathrm dx)^{\top}Ax$ est un scalaire, donc égal à sa transposée.)*

**Exemple 2 — $f(\beta)=\lVert y-X\beta\rVert^2$.**

$$\mathrm df=2\,(y-X\beta)^{\top}\,\mathrm d(y-X\beta)=-2\,(y-X\beta)^{\top}X\,\mathrm d\beta
\;\Longrightarrow\;\nabla f=-2X^{\top}(y-X\beta).$$

> 🔑 **Cette méthode transforme un calcul de $n^2$ dérivées partielles en trois lignes
> d'algèbre.** Elle est celle de Magnus & Neudecker, et c'est la seule qui reste praticable dès
> que des inverses ou des déterminants apparaissent.

---

## 7.4 Dériver par rapport à une matrice

| $f(A)$ | $\dfrac{\partial f}{\partial A}$ | Différentielle qui le donne |
|---|---|---|
| $\operatorname{tr}(A^{\top}B)$ | $B$ | $\mathrm df=\operatorname{tr}(\mathrm dA^{\top}B)$ |
| $\operatorname{tr}(AB)$ | $B^{\top}$ | idem |
| $x^{\top}Ax$ | $xx^{\top}$ | $\mathrm df=\operatorname{tr}(xx^{\top}\mathrm dA)$ |
| ⭐ $\log\det A$ ($A\succ0$) | $\big(A^{-1}\big)^{\top}=A^{-1}$ si symétrique | $\mathrm d\log\det A=\operatorname{tr}\!\big(A^{-1}\mathrm dA\big)$ |
| $x^{\top}A^{-1}x$ | $-A^{-\top}xx^{\top}A^{-\top}$ | $\mathrm d(A^{-1})=-A^{-1}(\mathrm dA)A^{-1}$ |

### L'application qui justifie ce tableau

La log-vraisemblance d'un échantillon gaussien centré $x_1,\dots,x_n$ de $\mathbb R^d$ vaut

$$\ell(\Sigma)=-\frac n2\log\det\Sigma-\frac12\sum_{i=1}^{n}x_i^{\top}\Sigma^{-1}x_i+\text{cte}.$$

Les deux dernières lignes du tableau donnent

$$\frac{\partial\ell}{\partial\Sigma}
=-\frac n2\Sigma^{-1}+\frac12\Sigma^{-1}\Big(\sum_ix_ix_i^{\top}\Big)\Sigma^{-1}=0
\qquad\Longrightarrow\qquad
\boxed{\;\hat\Sigma=\frac1n\sum_{i=1}^{n}x_ix_i^{\top}\;}$$

> 🔑 **L'estimateur du maximum de vraisemblance de $\Sigma$ est la covariance empirique — divisée
> par $n$, pas par $n-1$.** C'est exactement la convention de [`modele.md`](../../../../modele.md), et cela
> **explique** l'écart de convention signalé dans le
> [README de statistique](../../../semestre2/statistique/mathematique/README.md) : $n$ vient du maximum de vraisemblance,
> $n-1$ vient de l'absence de biais. Deux critères, deux diviseurs, aucune contradiction.

---

## 7.5 Les moindres carrés, en trois lignes

$$f(\beta)=\lVert y-X\beta\rVert^2
=y^{\top}y-2\beta^{\top}X^{\top}y+\beta^{\top}X^{\top}X\beta$$

**① Gradient** (formulaire, ou § 7.3) :
$$\nabla f(\beta)=-2X^{\top}y+2X^{\top}X\beta .$$

**② Point critique** — les **équations normales** :
$$X^{\top}X\hat\beta=X^{\top}y
\qquad\Longrightarrow\qquad
\boxed{\;\hat\beta=\big(X^{\top}X\big)^{-1}X^{\top}y\;}\quad\text{si }X^{\top}X\text{ est inversible.}$$

**③ Hessienne** — c'est elle qui **conclut** :
$$H_f=2X^{\top}X\;\succeq\;0\quad\text{toujours, car } v^{\top}X^{\top}Xv=\lVert Xv\rVert^2\ge0 .$$

Donc $f$ est **convexe** ([§ 7.2 d'analyse](../convexite/07-convexite-en-dimension-n.md)), et le
point critique est un **minimum global** ([§ 6.4 d'analyse](../convexite/06-minimisation-convexe.md)).
Si de plus $X$ est de rang plein, $H_f\succ0$ : le minimum est **unique**.

| Ce que donne chaque étape | Sans convexité |
|---|---|
| ① et ② : un point critique | Un candidat, rien de plus |
| ③ : $H_f\succeq0$ | **La preuve** qu'il s'agit du minimum global |

> 🔑 **Trois lignes remplacent les huit étapes de [`modele.md`](../../../../modele.md)** — et pour un
> nombre quelconque de variables explicatives, pas seulement deux. Le document reste utile pour
> ce qu'il fait ensuite (forme canonique, lecture en $\rho$, décomposition de variance) ; ce
> module remplace seulement sa partie calculatoire.

📐 **Et géométriquement**, l'équation normale $X^{\top}(y-X\hat\beta)=0$ dit exactement que **le
résidu est orthogonal aux colonnes de $X$** : c'est la
[projection orthogonale](../../algebre/06-projection-orthogonale.md), obtenue ici par le calcul, là
sans aucun calcul.

---

## 7.6 Le portefeuille à variance minimale, par Lagrange matriciel

$$\min_w\ w^{\top}\Sigma w\quad\text{sous}\quad\mathbf 1^{\top}w=1 .$$

Lagrangien $L(w,\nu)=w^{\top}\Sigma w-\nu(\mathbf 1^{\top}w-1)$. Le formulaire donne
$\nabla_wL=2\Sigma w-\nu\mathbf 1=0$, d'où $w=\frac\nu2\Sigma^{-1}\mathbf 1$, et la contrainte fixe
$\nu$ :

$$w^\star=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^{\top}\Sigma^{-1}\mathbf 1}.$$

C'est le résultat du [§ 7.5 du cours de convexité](../convexite/07-convexite-en-dimension-n.md),
obtenu ici **par le calcul** ; là-bas, c'est la convexité qui garantissait que la condition de
Lagrange **suffit**. Les deux moitiés du raisonnement viennent de deux cours différents et ne se
recouvrent pas.

---

## 7.7 Vérification numérique

### S7.1 — Le formulaire, testé ligne par ligne

```python
import numpy as np

rng = np.random.default_rng(7)
h = 1e-6

def gradient_num(f, x):
    g = np.zeros_like(x, dtype=float)
    for j in range(x.size):
        e = np.zeros_like(x, dtype=float); e[j] = h
        g[j] = (f(x + e) - f(x - e)) / (2 * h)
    return g

d = 5
A = rng.normal(size=(d, d))
Sym = A + A.T
a = rng.normal(size=d)
x = rng.normal(size=d)

tests = [
    ("a'x",        lambda v: a @ v,            lambda v: a),
    ("x'Ax",       lambda v: v @ A @ v,        lambda v: (A + A.T) @ v),
    ("x'Sym x",    lambda v: v @ Sym @ v,      lambda v: 2 * Sym @ v),
    ("||x||^2",    lambda v: v @ v,            lambda v: 2 * v),
    ("||Ax-a||^2", lambda v: (A @ v - a) @ (A @ v - a), lambda v: 2 * A.T @ (A @ v - a)),
]
for nom, f, grad in tests:
    print(f"{nom:>12} : ecart = {np.abs(grad(x) - gradient_num(f, x)).max():.2e}")
```

Tous les écarts sont de l'ordre de $10^{-10}$ — c'est-à-dire l'erreur de la différence finie
elle-même ([§ 1.6](01-derivee-et-approximation-affine.md)), et non celle des formules.

### S7.2 — Dérivée par rapport à une matrice : $\log\det$

```python
M = rng.normal(size=(4, 4)); M = M @ M.T + 4 * np.eye(4)          # symetrique definie positive
f = lambda Z: np.log(np.linalg.det(Z))

G = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        E = np.zeros((4, 4)); E[i, j] = h
        G[i, j] = (f(M + E) - f(M - E)) / (2 * h)

print("ecart avec (M^-1)^T :", np.abs(G - np.linalg.inv(M).T).max())
```

Écart $\approx10^{-9}$ : $\frac{\partial\log\det M}{\partial M}=M^{-\top}$ est vérifié
coefficient par coefficient.

### S7.3 — Les moindres carrés

```python
n, p = 200, 4
X = np.column_stack([np.ones(n), rng.normal(size=(n, p - 1))])
beta = np.array([2., -1., 0.5, 3.])
y = X @ beta + rng.normal(0, 0.5, n)

beta_hat = np.linalg.solve(X.T @ X, X.T @ y)
print("beta chapeau      :", np.round(beta_hat, 4))
print("identique a lstsq :", np.allclose(beta_hat, np.linalg.lstsq(X, y, rcond=None)[0]))
print("norme du gradient :", np.linalg.norm(-2 * X.T @ (y - X @ beta_hat)))
print("residu orthogonal aux colonnes de X :",
      np.allclose(X.T @ (y - X @ beta_hat), 0, atol=1e-9))
print("valeurs propres de H = 2X'X :", np.round(np.linalg.eigvalsh(2 * X.T @ X), 1))
```

Trois faits d'un coup : $\hat\beta$ coïncide avec la routine de référence, **le gradient y est nul
à $10^{-13}$**, et le résidu est orthogonal aux colonnes de $X$. Les valeurs propres de la
Hessienne sont toutes $>0$ : minimum **unique**.

---

## 7.8 Exercices

**E7.1.** Démontrer $\nabla(x^{\top}Ax)=(A+A^{\top})x$ de **deux façons** : coefficient par
coefficient, puis par la différentielle du § 7.3. *Combien de lignes chacune ?*

**E7.2.** Calculer $\nabla_\beta\lVert y-X\beta\rVert^2$ et $H_\beta$, puis retrouver les
équations normales. *Que devient l'unicité si deux colonnes de $X$ sont proportionnelles ?
Interpréter en termes de [rang](../../algebre/07-supplementaire-orthogonal-et-dimension.md).*

**E7.3.** Vérifier que le formulaire redonne, pour $p=2$ et $X=[\mathbf 1\ \ T]$, exactement les
deux équations partielles de [`modele.md`](../../../../modele.md), étape 1.

**E7.4.** Établir $\mathrm d(A^{-1})=-A^{-1}(\mathrm dA)A^{-1}$ en différentiant $AA^{-1}=I$. *En
déduire $\frac{\partial}{\partial A}\big(x^{\top}A^{-1}x\big)$.*

**E7.5.** Retrouver $\hat\Sigma=\frac1n\sum_ix_ix_i^{\top}$ à partir de $\ell(\Sigma)$ du § 7.4.
*Pourquoi obtient-on $n$ et non $n-1$ ? Relier à la note de convention du
[README de statistique](../../../semestre2/statistique/mathematique/README.md).*

**E7.6.** Écrire la ridge : $\min_\beta\lVert y-X\beta\rVert^2+\lambda\lVert\beta\rVert^2$.
Calculer le gradient, résoudre, et montrer que la solution existe **même si $X^{\top}X$ est
singulière**. *Quelle propriété de la Hessienne a été achetée par le terme en $\lambda$ ?*

**E7.7 — orientée finance.** Avec `import_societe.py`, construire $X=[\mathbf 1\ \ t]$ sur une
série de prix, calculer $\hat\beta$ par la formule matricielle, et comparer aux
$v_{0,\min}$ et $r_{\min}$ de [`modele.md`](../../../../modele.md).

---

## 7.9 À retenir

- ⚠️ **Fixer la convention avant de calculer** : gradient en **colonne**, jacobienne $m\times n$,
  $\partial f/\partial A$ de la forme de $A$. Puis **compter les dimensions à chaque ligne**.
- **Le formulaire de base** : $\nabla(a^{\top}x)=a$, $J_{Ax}=A$,
  $\nabla(x^{\top}Ax)=(A+A^{\top})x$, $\nabla\lVert Ax-b\rVert^2=2A^{\top}(Ax-b)$.
- ⭐ **La chaîne inverse l'ordre en gradient** : $J_{f\circ g}=J_fJ_g$ mais
  $\nabla(f\circ g)=J_g^{\top}\nabla f$.
- ⭐ **La méthode par différentielle** reconstruit tout le formulaire, y compris
  $\partial\log\det A/\partial A=A^{-\top}$ et les dérivées d'un inverse.
- ⭐ **Les moindres carrés en trois lignes** : gradient $\to$ équations normales $\to$ Hessienne
  $2X^{\top}X\succeq0$, donc minimum **global**. La troisième ligne n'est pas facultative : c'est
  elle qui fait la preuve.
- **Vérifier chaque formule par différence finie** avant de l'utiliser — trois lignes de code,
  et toutes les transposées se voient.

---

⬅️ [Module 6 — La matrice jacobienne](06-la-matrice-jacobienne.md) ·
➡️ [Module 8 — Intégrales multiples et facteur de volume](08-integrales-multiples-et-jacobien.md) ·
🏠 [Sommaire](README.md)
