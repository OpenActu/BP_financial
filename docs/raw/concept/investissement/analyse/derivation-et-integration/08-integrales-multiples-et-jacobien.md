# Module 8 — Intégrales multiples et le jacobien comme facteur de volume ⭐

**Durée : 1 h 15.** Prérequis : modules [3](03-integrale-et-theoreme-fondamental.md) et
[6](06-la-matrice-jacobienne.md), et le déterminant du
[cours d'algèbre](../../algebre/README.md).

> **La question traitée.** Qu'est-ce qui remplace le facteur $\varphi'(t)$ du changement de
> variable ([§ 3.3](03-integrale-et-theoreme-fondamental.md)) quand on intègre sur un domaine de
> $\mathbb R^n$ ?

**Réponse : $\lvert\det J_\varphi\rvert$ — le déterminant de la jacobienne du module 6.** Ce module
est la charnière du cours : le même objet, jusqu'ici approximation linéaire, devient **facteur de
volume**. Il donne au passage $\int e^{-x^2}dx=\sqrt\pi$, que le
[module 4](04-integrales-generalisees-et-moments.md) avait laissé en suspens.

---

## 8.1 Intégrale double, et Fubini

Sur un pavé $[a,b]\times[c,d]$, l'intégrale double se définit comme l'intégrale simple : limite de
sommes de **volumes** de parallélépipèdes $f(x_i,y_j)\Delta x\Delta y$. Sur un domaine $D$ borné,
on intègre $f\cdot\mathbf 1_D$.

> **Théorème de Fubini (admis).** Si $f$ est continue sur un domaine $D$ décrit par
> $a\le x\le b$, $u(x)\le y\le v(x)$, alors
> $$\iint_Df(x,y)\,dx\,dy=\int_a^b\left(\int_{u(x)}^{v(x)}f(x,y)\,dy\right)dx$$
> et l'on peut échanger les deux intégrations lorsque le domaine se décrit aussi dans l'autre
> sens.

⚠️ **L'échange n'est pas gratuit.** Il exige $f$ continue sur un domaine borné, ou — cas des
intégrales généralisées — la convergence **absolue** $\iint\lvert f\rvert<\infty$. Sans elle,
échanger peut changer le résultat ; c'est le même avertissement qu'au
[§ 4.1](04-integrales-generalisees-et-moments.md).

> 📐 **En probabilité, Fubini est l'outil qui sépare les variables.** Pour $X\perp\!\!\!\perp Y$
> de densités $f$ et $g$, la densité du couple est $f(x)g(y)$, et toute espérance se factorise :
> $$E\big(u(X)v(Y)\big)=\iint u(x)v(y)f(x)g(y)\,dx\,dy=E\big(u(X)\big)E\big(v(Y)\big).$$
> C'est le théorème utilisé sans le nommer au
> [§ 2.4 de statistique](../../statistique/mathematique/02-esperance.md).

---

## 8.2 Le cas linéaire : $\lvert\det A\rvert$ est un facteur de volume

Avant le cas général, le cas où tout se voit.

> **Proposition (algèbre).** Si $A$ est une matrice $n\times n$, l'image du cube unité
> $[0,1]^n$ par $x\mapsto Ax$ est un parallélépipède de volume $\lvert\det A\rvert$.

Conséquence immédiate, par découpage en petits cubes :

$$\int_{A(D)}f(y)\,dy=\lvert\det A\rvert\int_Df(Ax)\,dx .$$

| $A$ | $\det A$ | Effet |
|---|---|---|
| $\lambda I_n$ | $\lambda^n$ | Dilate d'un facteur $\lambda^n$ |
| Rotation | $1$ | **Conserve** les volumes ([algèbre § 6](../../algebre/06-bases-orthonormees-et-isometries.md)) |
| Projection | $0$ | Écrase : l'image est de volume nul |
| $\operatorname{diag}(\sigma_1,\dots,\sigma_n)$ | $\prod\sigma_i$ | Étire chaque axe séparément |

> 🔑 **Que le déterminant soit un volume n'est pas un fait nouveau** : c'est l'un des résultats du
> cours d'algèbre. La seule nouveauté ici est **où** on l'utilise — sous une intégrale.

---

## 8.3 ⭐ Le théorème du changement de variables

> **Théorème (admis).** Soit $\varphi:D\to\varphi(D)$ une bijection de classe $C^1$ entre ouverts
> de $\mathbb R^n$, de jacobienne inversible en tout point. Alors pour $f$ intégrable :
> $$\boxed{\;\int_{\varphi(D)}f(y)\,dy=\int_Df\big(\varphi(x)\big)\,\big\lvert\det J_\varphi(x)\big\rvert\,dx\;}$$

**Pourquoi $\lvert\det J_\varphi\rvert$, en une phrase.** Au voisinage de $x$, $\varphi$ est
**égale à une application affine** de partie linéaire $J_\varphi(x)$
([§ 6.1](06-la-matrice-jacobienne.md)) ; celle-ci multiplie les volumes par
$\lvert\det J_\varphi(x)\rvert$ (§ 8.2). Un élément de volume $dx$ devient donc
$\lvert\det J_\varphi(x)\rvert\,dx$ — la seule différence avec le cas linéaire étant que **le
facteur change d'un point à l'autre**, d'où une intégrale au lieu d'un produit.

$$\underbrace{\varphi'(t)\,dt}_{n=1,\ \S\,3.3}
\qquad\longrightarrow\qquad
\underbrace{\big\lvert\det J_\varphi(x)\big\rvert\,dx}_{\text{cas général}}$$

⚠️ **Trois hypothèses, trois pièges** : la bijectivité (sinon on compte deux fois — voir le cas
$Z^2$ au [§ 9.3](09-changement-de-variable-et-densites.md)), la régularité $C^1$, et
$\det J\ne0$ (sinon le changement écrase le domaine). La **valeur absolue** est indispensable :
en dimension $\ge2$, il n'y a plus de bornes orientées pour porter le signe
([§ 3.3](03-integrale-et-theoreme-fondamental.md)).

---

## 8.4 ⭐ L'intégrale de Gauss, enfin

**Le problème.** $e^{-x^2}$ n'a pas de primitive élémentaire. Le calcul suivant contourne
l'obstacle en **passant à deux dimensions**, où un changement de variables devient possible.

Posons $I=\int_{-\infty}^{+\infty}e^{-x^2}dx$. Alors, par Fubini :

$$I^2=\left(\int_{\mathbb R}e^{-x^2}dx\right)\left(\int_{\mathbb R}e^{-y^2}dy\right)
=\iint_{\mathbb R^2}e^{-(x^2+y^2)}\,dx\,dy .$$

Passons en polaires, $\varphi(r,\theta)=(r\cos\theta,r\sin\theta)$, dont le
[§ 6.5](06-la-matrice-jacobienne.md) donne $\det J_\varphi=r$ :

$$I^2=\int_0^{2\pi}\!\!\int_0^{+\infty}e^{-r^2}\,\underbrace{r\,dr\,d\theta}_{\lvert\det J\rvert\,dr\,d\theta}
=2\pi\int_0^{+\infty}re^{-r^2}dr
=2\pi\left[-\tfrac12e^{-r^2}\right]_0^{+\infty}=2\pi\cdot\tfrac12=\pi .$$

$$\boxed{\;I=\sqrt\pi\;}\qquad\text{d'où}\qquad
\int_{-\infty}^{+\infty}e^{-x^2/2}dx=\sqrt{2\pi}.$$

> 🔑 **Tout le calcul tient dans le facteur $r$.** Sans lui, l'intégrale en $r$ serait
> $\int e^{-r^2}dr$ — c'est-à-dire le problème de départ. **C'est le jacobien qui fournit
> exactement le facteur manquant pour que la primitive devienne élémentaire.** Le $\sqrt{2\pi}$ de
> la densité normale n'a pas d'autre origine que cette ligne.

---

## 8.5 Deux autres changements qui servent

### ① Le changement affine, et la densité gaussienne multivariée

Pour $\varphi(x)=Ax+b$ avec $A$ inversible, $J_\varphi=A$ est **constante** et

$$\int_{\mathbb R^n}f(y)\,dy=\lvert\det A\rvert\int_{\mathbb R^n}f(Ax+b)\,dx .$$

C'est ce facteur $\lvert\det A\rvert$ qui produira, au
[§ 9.4](09-changement-de-variable-et-densites.md), le $\sqrt{\det\Sigma}$ de la densité d'un
vecteur gaussien — le calcul que le
[§ 9.4 de statistique](../../statistique/mathematique/09-vecteur-gaussien.md) déclare avoir **évité**.

### ② Les coordonnées sphériques

$\det J=r^2\sin\theta$, d'où le volume de la boule de rayon $R$ :

$$\int_0^{2\pi}\!\!\int_0^{\pi}\!\!\int_0^{R}r^2\sin\theta\,dr\,d\theta\,d\phi
=2\pi\cdot2\cdot\frac{R^3}{3}=\frac{4\pi R^3}{3}.$$

Le facteur $r^2$ — encore un jacobien — est ce qui explique que **le volume se concentre près de
la surface en grande dimension**, phénomène qui rend l'intuition géométrique trompeuse dès
$n\ge5$ (voir S2.1 du [cours d'algèbre](../../algebre/02-cauchy-schwarz-et-angle.md)).

---

## 8.6 Vérification numérique

### S8.1 — L'intégrale de Gauss, des deux côtés

```python
import numpy as np

# côté cartesien : quadrature 2D brute
N = 4000
g = np.linspace(-6, 6, N); dx = g[1] - g[0]
X, Y = np.meshgrid(g, g)
I2 = np.exp(-(X ** 2 + Y ** 2)).sum() * dx * dx
print(f"integrale double  = {I2:.6f}    pi = {np.pi:.6f}")
print(f"donc int e^-x^2   = {np.sqrt(I2):.6f}    sqrt(pi) = {np.sqrt(np.pi):.6f}")

# côté polaire : le jacobien r rend la primitive elementaire
r = np.linspace(0, 8, 400_001)
I2_polaire = 2 * np.pi * np.trapezoid(r * np.exp(-r ** 2), r)
print(f"par les polaires  = {I2_polaire:.6f}")
```

Les deux valent $\pi$ à $10^{-6}$ près. **La seconde ligne de code est une intégrale simple à
primitive élémentaire ; la première est une quadrature en dimension 2 de 16 millions de points.**
C'est tout le gain du changement de variables.

### S8.2 — $\lvert\det J\rvert$ est bien un facteur de volume

```python
rng = np.random.default_rng(8)
A = rng.normal(size=(3, 3))

# volume de l'image du cube unite, par comptage Monte-Carlo
U = rng.random((200_000, 3)) @ A.T                       # image du cube
lo, hi = U.min(0) - 0.1, U.max(0) + 0.1
P = rng.uniform(lo, hi, size=(4_000_000, 3))
X = P @ np.linalg.inv(A).T                               # antecedents
dedans = ((X >= 0) & (X <= 1)).all(axis=1)

print(f"|det A|         = {abs(np.linalg.det(A)):.4f}")
print(f"volume estime   = {dedans.mean() * np.prod(hi - lo):.4f}")
```

Sortie : $\lvert\det A\rvert=0{,}9280$ contre un volume estimé de $0{,}9277$. **Le déterminant
n'approche pas le facteur de volume : il l'est.**

---

## 8.7 Exercices

**E8.1.** Calculer $\iint_D xy\,dx\,dy$ sur le triangle $x\ge0$, $y\ge0$, $x+y\le1$, dans les deux
ordres d'intégration, et vérifier que Fubini dit vrai.

**E8.2.** Refaire le calcul de l'intégrale de Gauss en détaillant : (a) où sert Fubini, (b) où
sert la bijectivité du passage en polaires, (c) pourquoi l'origine, où $\det J=0$, ne pose pas
problème.

**E8.3.** Calculer $\iint_{\mathbb R^2}e^{-(x^2+xy+y^2)}dx\,dy$ par un changement **linéaire** bien
choisi. *(Piste : diagonaliser la forme quadratique — [algèbre](../../algebre/README.md) — et lire le
$\lvert\det\rvert$.)* Vérifier que le résultat vaut $2\pi/\sqrt3$.

**E8.4.** Établir $\det J=r^2\sin\theta$ pour les coordonnées sphériques, puis calculer le volume
de la boule de rayon $R$ en dimension 3.

**E8.5.** Montrer que le volume de la boule unité de $\mathbb R^n$ tend vers **0** quand
$n\to\infty$. *(Piste : $V_n=\frac{\pi^{n/2}}{\Gamma(n/2+1)}$ — la $\Gamma$ du
[module 4](04-integrales-generalisees-et-moments.md).)* Que devient l'intuition « la boule remplit
le cube » ?

**E8.6.** Vérifier numériquement que l'image du cube unité par une **rotation** a un volume de 1,
et par une matrice singulière un volume de 0. *Relier au tableau du § 8.2.*

---

## 8.8 À retenir

- **Fubini** ramène une intégrale multiple à des intégrales simples emboîtées — sous condition de
  **convergence absolue**. En probabilité, c'est ce qui factorise l'espérance d'un produit de
  variables indépendantes.
- ⭐ **Changement de variables** :
  $\int_{\varphi(D)}f(y)dy=\int_Df(\varphi(x))\lvert\det J_\varphi(x)\rvert dx$. Le facteur est le
  **déterminant du jacobien du [module 6](06-la-matrice-jacobienne.md)** — même objet, autre usage.
- **Pourquoi ce facteur** : localement $\varphi$ est affine de partie linéaire $J_\varphi$, et une
  application linéaire multiplie les volumes par $\lvert\det\rvert$. Ce qui change par rapport au
  cas linéaire, c'est que le facteur **dépend du point**.
- ⭐ **$\int e^{-x^2}dx=\sqrt\pi$** s'obtient en passant au carré, en passant en polaires, et en
  laissant le jacobien $r$ fournir le facteur manquant. Le $\sqrt{2\pi}$ de la loi normale vient
  de là.
- **Trois hypothèses** : bijectivité, $C^1$, $\det J\ne0$ ; et la **valeur absolue**, car il n'y a
  plus de bornes orientées en dimension $\ge2$.

---

⬅️ [Module 7 — Le calcul matriciel des dérivées](07-calcul-matriciel-des-derivees.md) ·
➡️ [Module 9 — Changement de variable et densités](09-changement-de-variable-et-densites.md) ·
🏠 [Sommaire](README.md)
