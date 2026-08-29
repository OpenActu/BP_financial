# Module 6 — La matrice jacobienne ⭐

**Durée : 1 h 15.** Prérequis : [module 5](05-derivees-partielles-et-gradient.md).
⭐ **Module central du cours.**

> **La question traitée.** Que devient la dérivée quand la fonction va de $\mathbb R^n$ dans
> $\mathbb R^m$ ?

**Ce qui est en jeu.** Un tableau de dérivées partielles n'est pas un objet ; une **matrice** en
est un. Ce module montre que la jacobienne n'est pas une notation commode mais **l'application
linéaire qui approche $f$** — ce dont découlent, sans effort supplémentaire, la règle de la chaîne
comme produit de matrices, la Hessienne comme jacobienne du gradient, l'inversion locale, et
(module 8) le facteur de volume des intégrales.

---

## 6.1 La définition — la même qu'au module 1

> **Définition.** $f:\mathbb R^n\to\mathbb R^m$ est **différentiable** en $a$ s'il existe une
> matrice $J\in\mathbb R^{m\times n}$ telle que
> $$\boxed{\;f(a+h)=f(a)+J\,h+o\big(\lVert h\rVert\big)\;}$$
> Cette matrice est unique, appelée **matrice jacobienne** et notée $J_f(a)$. Ses coefficients
> sont
> $$\big(J_f(a)\big)_{ij}=\frac{\partial f_i}{\partial x_j}(a),\qquad
> 1\le i\le m,\ 1\le j\le n .$$

**Une ligne par composante de $f$, une colonne par variable.** Retenir la phrase, pas la formule :
c'est elle qui donne les dimensions dans tous les calculs du
[module 7](07-calcul-matriciel-des-derivees.md).

> 🔑 **Rien n'a changé depuis le module 1**, sinon la nature de l'objet : un nombre, puis un
> vecteur ligne, puis une matrice. La phrase « dériver, c'est linéariser » est la définition, et
> la jacobienne **est** cette application linéaire, écrite dans les bases canoniques.

$$\underbrace{f'(a)\,h}_{n=m=1}\qquad
\underbrace{\langle\nabla f(a),h\rangle}_{m=1}\qquad
\underbrace{J_f(a)\,h}_{\text{cas général}}$$

---

## 6.2 Lire une jacobienne

| $f$ | Type | $J_f$ | Taille |
|---|---|---|---|
| $f(x)=Ax$ ($A$ constante) | $\mathbb R^n\to\mathbb R^m$ | $A$ | $m\times n$ |
| $f(x)=Ax+b$ | idem | $A$ | $m\times n$ |
| $f$ scalaire | $\mathbb R^n\to\mathbb R$ | $\big(\nabla f\big)^{\top}$ — un vecteur **ligne** | $1\times n$ |
| $\gamma(t)$ courbe | $\mathbb R\to\mathbb R^m$ | Le vecteur vitesse, en **colonne** | $m\times1$ |
| $\nabla f$ (gradient d'une scalaire) | $\mathbb R^n\to\mathbb R^n$ | $J_{\nabla f}=H_f$ | $n\times n$ |

> ⚠️ **Le piège le plus fréquent du cours** : pour $f$ scalaire, **la jacobienne est une ligne, le
> gradient est une colonne**, et $\nabla f=(J_f)^{\top}$. Les deux objets contiennent les mêmes
> nombres et ne se placent pas au même endroit dans un produit matriciel. La convention est fixée
> au [§ 7.1](07-calcul-matriciel-des-derivees.md) ; elle n'est pas négociable en cours de calcul.

**Une application linéaire est sa propre dérivée.** $f(x)=Ax$ donne $f(a+h)=Aa+Ah$ **exactement** :
le reste $o(\lVert h\rVert)$ est nul, et $J_f=A$ partout. C'est le pendant de « la dérivée de
$x\mapsto cx$ est $c$ », et c'est la brique de tout le module 7.

---

## 6.3 ⭐ La règle de la chaîne est un produit de matrices

> **Théorème.** Si $f:\mathbb R^n\to\mathbb R^p$ est différentiable en $a$ et
> $g:\mathbb R^p\to\mathbb R^m$ en $f(a)$, alors $g\circ f$ est différentiable en $a$ et
> $$\boxed{\;J_{g\circ f}(a)\;=\;J_g\big(f(a)\big)\;J_f(a)\;}$$

**Démonstration** — c'est celle du [§ 1.3](01-derivee-et-approximation-affine.md), inchangée :

$$g\big(f(a+h)\big)=g\Big(f(a)+J_f(a)h+o(\lVert h\rVert)\Big)
=g\big(f(a)\big)+J_g\big(f(a)\big)\Big[J_f(a)h\Big]+o(\lVert h\rVert).$$

La composée de deux applications linéaires est l'application linéaire dont la matrice est le
**produit** des matrices. $\blacksquare$

> 🔑 **Les dimensions se vérifient toutes seules** : $(m\times p)\cdot(p\times n)=(m\times n)$.
> **Si les tailles ne se recollent pas, le calcul est faux** — c'est le test le plus rapide qui
> soit sur une dérivation matricielle, et il attrape la quasi-totalité des transposées oubliées.

**En coordonnées**, la même formule s'écrit

$$\frac{\partial (g\circ f)_i}{\partial x_j}=\sum_{k=1}^{p}
\frac{\partial g_i}{\partial y_k}\Big(f(a)\Big)\cdot\frac{\partial f_k}{\partial x_j}(a),$$

c'est-à-dire la règle « on somme sur les chemins » — mais l'écriture matricielle est plus sûre :
elle **impose** l'ordre des facteurs, que l'écriture en somme laisse libre.

### Deux cas particuliers qui servent

| Situation | Formule | Où |
|---|---|---|
| $t\mapsto f\big(x(t)\big)$, $f$ scalaire | $\frac{d}{dt}f(x(t))=\big\langle\nabla f(x(t)),\,x'(t)\big\rangle$ | Convexité le long d'un segment ([analyse § 7.1](../convexite/07-convexite-en-dimension-n.md)) |
| $x\mapsto f(Ax+b)$ | $J=J_f(Ax+b)\,A$ | Précomposition affine, partout au module 7 |

---

## 6.4 La Hessienne est la jacobienne du gradient

Pour $f:\mathbb R^n\to\mathbb R$, le gradient est une fonction $\nabla f:\mathbb R^n\to\mathbb R^n$.
Sa jacobienne est donc une matrice $n\times n$ :

$$J_{\nabla f}=\Big(\frac{\partial(\partial_jf)}{\partial x_i}\Big)_{ij}=H_f .$$

> 🔑 **Trois objets, une hiérarchie.** $f$ scalaire $\to$ $\nabla f$ vectorielle $\to$ $H_f$
> matricielle. Chaque étage est la jacobienne du précédent. Le théorème de Schwarz
> ([§ 5.4](05-derivees-partielles-et-gradient.md)) dit que cette jacobienne-là est **symétrique**,
> ce qui n'a aucune raison d'être vrai pour une jacobienne quelconque.

Le développement d'ordre 2 s'écrit alors, exactement comme au
[module 2](02-taylor-et-approximations.md) :

$$f(a+h)=f(a)+\langle\nabla f(a),h\rangle+\tfrac12h^{\top}H_f(a)h+o(\lVert h\rVert^2).$$

---

## 6.5 Inversion locale

> **Théorème d'inversion locale (admis).** Soit $f:\mathbb R^n\to\mathbb R^n$ de classe $C^1$. Si
> $$\det J_f(a)\ne0,$$
> alors $f$ est une **bijection** d'un voisinage de $a$ sur un voisinage de $f(a)$, sa réciproque
> est $C^1$, et
> $$\boxed{\;J_{f^{-1}}\big(f(a)\big)=\big(J_f(a)\big)^{-1}\;}$$

**La formule se démontre en une ligne** une fois l'inversibilité admise : dériver
$f^{-1}\circ f=\text{id}$ par la règle de la chaîne donne $J_{f^{-1}}\,J_f=I_n$.

C'est l'exacte généralisation de $(f^{-1})'(b)=1/f'(a)$ : la condition $f'(a)\ne0$ devient
$\det J_f(a)\ne0$, et l'inverse d'un nombre devient l'inverse d'une matrice.

⚠️ **« Locale » n'est pas décoratif.** Le passage en polaires
$(r,\theta)\mapsto(r\cos\theta,r\sin\theta)$ a un jacobien de déterminant $r\ne0$ partout hors de
l'origine, et n'est pourtant **pas** globalement injectif : $\theta$ et $\theta+2\pi$ donnent le
même point. Un déterminant non nul garantit l'inversibilité **au voisinage**, jamais sur tout le
domaine.

### L'exemple à connaître : les coordonnées polaires

$$\varphi(r,\theta)=\begin{pmatrix}r\cos\theta\\ r\sin\theta\end{pmatrix},
\qquad
J_\varphi=\begin{pmatrix}\cos\theta&-r\sin\theta\\ \sin\theta&r\cos\theta\end{pmatrix},
\qquad
\det J_\varphi=r\big(\cos^2\theta+\sin^2\theta\big)=r .$$

> 🔑 **Retenez $\det J=r$ : c'est tout le module 8.** Ce déterminant est le facteur $r$ du fameux
> $dx\,dy=r\,dr\,d\theta$, et c'est lui qui permettra de calculer $\int e^{-x^2}dx=\sqrt\pi$
> ([§ 8.4](08-integrales-multiples-et-jacobien.md)).

---

## 6.6 Ce que le déterminant du jacobien signifie

Trois lectures d'un même nombre, qu'il faut avoir en tête avant d'aborder la partie II :

| $\det J_f(a)$ | Signification |
|---|---|
| $\ne0$ | $f$ est **inversible** au voisinage de $a$ (§ 6.5) |
| $\lvert\det J_f(a)\rvert$ | Le **facteur de dilatation des volumes** au voisinage de $a$ ([module 8](08-integrales-multiples-et-jacobien.md)) |
| Signe | $f$ **préserve** ($>0$) ou **renverse** ($<0$) l'orientation |

La deuxième ligne est ce que l'intégration voit — et elle n'est pas une propriété nouvelle : le
[cours d'algèbre](../../algebre/README.md) établit qu'un déterminant **est** un volume orienté. La
seule nouveauté du module 8 est que ce facteur, constant pour une application linéaire, **varie
d'un point à l'autre** pour une application quelconque — d'où une intégrale.

---

## 6.7 Vérification numérique

### S6.1 — Jacobienne numérique, et la règle de la chaîne comme produit

```python
import numpy as np

rng = np.random.default_rng(6)

def jacobienne_num(f, x, h=1e-6):
    x = np.asarray(x, dtype=float)
    base = f(x)
    J = np.zeros((np.size(base), x.size))
    for j in range(x.size):
        e = np.zeros_like(x); e[j] = h
        J[:, j] = (f(x + e) - f(x - e)) / (2 * h)
    return J

f = lambda v: np.array([v[0] ** 2 * v[1], np.sin(v[0]) + v[1] ** 3, np.exp(v[0] * v[1])])
Jf = lambda v: np.array([[2 * v[0] * v[1],                 v[0] ** 2],
                         [np.cos(v[0]),                    3 * v[1] ** 2],
                         [v[1] * np.exp(v[0] * v[1]),      v[0] * np.exp(v[0] * v[1])]])

v = np.array([0.7, -1.3])
print("ecart jacobienne analytique / numerique :", np.abs(Jf(v) - jacobienne_num(f, v)).max())

# chaine : g o f  avec g(y) = (y0 + y1*y2, y2^2)
g = lambda y: np.array([y[0] + y[1] * y[2], y[2] ** 2])
Jg = lambda y: np.array([[1., y[2], y[1]],
                         [0., 0.,   2 * y[2]]])

J_compose = Jg(f(v)) @ Jf(v)                       # (2x3) @ (3x2) = (2x2)
J_direct = jacobienne_num(lambda z: g(f(z)), v)
print("chaine : ecart produit de matrices / numerique :", np.abs(J_compose - J_direct).max())
print("tailles :", Jg(f(v)).shape, "@", Jf(v).shape, "=", J_compose.shape)
```

Les deux écarts sont de l'ordre de $10^{-10}$ — l'erreur de la différence finie, pas celle du
calcul. **Le contrôle des tailles $(2\times3)\cdot(3\times2)=(2\times2)$ est la première chose à
vérifier** ; un produit dans le mauvais ordre serait ici impossible, ce qui est précisément
l'intérêt de la notation matricielle.

### S6.2 — Inversion locale sur les polaires

```python
polaire = lambda p: np.array([p[0] * np.cos(p[1]), p[0] * np.sin(p[1])])
inverse = lambda z: np.array([np.hypot(z[0], z[1]), np.arctan2(z[1], z[0])])

p = np.array([2.3, 0.9])
Jp = jacobienne_num(polaire, p)
Ji = jacobienne_num(inverse, polaire(p))
print(f"det J = {np.linalg.det(Jp):.6f}   r = {p[0]:.6f}")
print("J_inverse @ J = I ? ", np.allclose(Ji @ Jp, np.eye(2), atol=1e-6))
```

$\det J=r$ **exactement**, et les deux jacobiennes sont inverses l'une de l'autre : le théorème du
§ 6.5, vérifié numériquement.

---

## 6.8 Exercices

**E6.1.** Écrire la jacobienne de $f(x,y)=(x^2-y^2,\ 2xy)$ (c'est $z\mapsto z^2$ vu dans
$\mathbb C$). Calculer $\det J_f$ et dire où $f$ n'est pas localement inversible.

**E6.2.** Pour $f(x)=Ax$, vérifier $J_f=A$ à partir de la définition, sans passer par les dérivées
partielles.

**E6.3.** Démontrer $J_{g\circ f}=J_gJ_f$ en composant les deux approximations affines, et
identifier précisément le terme qui est un $o(\lVert h\rVert)$.

**E6.4.** Soit $f(w)=w^{\top}\Sigma w$. Écrire $J_f$ (une **ligne**) puis $\nabla f$ (une
**colonne**) puis $H_f$. *Vérifier que $H_f=J_{\nabla f}$.*

**E6.5.** Calculer la jacobienne du passage en coordonnées sphériques
$(r,\theta,\phi)\mapsto(r\sin\theta\cos\phi,\ r\sin\theta\sin\phi,\ r\cos\theta)$ et montrer que
$\det J=r^2\sin\theta$.

**E6.6.** Montrer que le passage en polaires n'est pas globalement injectif, alors que
$\det J\ne0$ hors de l'origine. *Quelle hypothèse du théorème d'inversion locale est locale, et
que faudrait-il pour conclure globalement ?*

---

## 6.9 À retenir

- ⭐ **$f(a+h)=f(a)+J_f(a)h+o(\lVert h\rVert)$** : la jacobienne **est** l'application linéaire qui
  approche $f$. Une **ligne par composante**, une **colonne par variable**.
- ⭐ **$J_{g\circ f}=J_g\,J_f$** : la règle de la chaîne est un produit de matrices, et les
  dimensions se recollent toutes seules. Test de cohérence immédiat.
- Pour $f$ **scalaire**, $J_f$ est une **ligne** et $\nabla f=(J_f)^{\top}$ une **colonne** —
  source d'erreur numéro un.
- **$H_f=J_{\nabla f}$** : trois étages, chacun jacobienne du précédent ; Schwarz rend le dernier
  symétrique.
- **$\det J_f(a)\ne0\Rightarrow$ inversion locale**, avec $J_{f^{-1}}=(J_f)^{-1}$. « Locale »
  n'est pas décoratif : les polaires en sont le contre-exemple global.
- **$\lvert\det J\rvert$ est un facteur de volume** — c'est ce que l'intégrale verra au
  [module 8](08-integrales-multiples-et-jacobien.md). Pour les polaires, $\det J=r$.

---

⬅️ [Module 5 — Dérivées partielles, différentielle, gradient](05-derivees-partielles-et-gradient.md) ·
➡️ [Module 7 — Le calcul matriciel des dérivées](07-calcul-matriciel-des-derivees.md) ·
🏠 [Sommaire](README.md)
