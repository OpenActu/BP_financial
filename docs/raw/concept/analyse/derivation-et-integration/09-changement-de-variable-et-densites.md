# Module 9 — Changement de variable et densités

**Durée : 1 h.** Prérequis : [module 8](08-integrales-multiples-et-jacobien.md), et les
[densités du cours de statistique](../../statistique/mathematique/01-variable-aleatoire-et-loi.md).

> **La question traitée.** $X$ a pour densité $f_X$ et l'on pose $Y=g(X)$. Quelle est la densité
> de $Y$ ?

**Ce qui est en jeu.** C'est l'aboutissement du cours, et le point où il rend au
[cours de statistique](../../statistique/mathematique/README.md) ce qu'il lui a emprunté. Le
[§ 9.4 de statistique](../../statistique/mathematique/09-vecteur-gaussien.md) note qu'une définition du vecteur
gaussien par la densité « aurait exigé un calcul de jacobien » ; ce module fait ce calcul, ainsi
que ceux de la log-normale, du $\chi^2(1)$, de Box–Muller et de la PIT.

---

## 9.1 Le principe : une densité n'est pas une probabilité

Une probabilité se **transporte** sans correction :

$$P\big(Y\in B\big)=P\big(X\in g^{-1}(B)\big).$$

Une **densité**, elle, est une probabilité **par unité de volume** — et le volume, lui, se
déforme. C'est exactement le facteur $\lvert\det J\rvert$ du
[module 8](08-integrales-multiples-et-jacobien.md).

> 🔑 **Toute la difficulté du sujet tient dans cette phrase.** Si $g$ étire l'axe d'un facteur 3,
> la même masse de probabilité s'étale sur trois fois plus de longueur : la densité doit être
> **divisée par 3**. Le jacobien est la comptabilité de cet étirement.

---

## 9.2 Dimension 1

### La méthode générale : passer par la fonction de répartition

C'est la méthode à utiliser **toujours**, parce qu'elle ne suppose rien sur $g$ :

1. écrire $F_Y(y)=P\big(g(X)\le y\big)$ ;
2. exprimer l'événement en termes de $X$ ;
3. dériver en $y$ ([TFA](03-integrale-et-theoreme-fondamental.md)).

### La formule, quand $g$ est monotone

Si $g$ est $C^1$ et **strictement monotone** :

$$\boxed{\;f_Y(y)=f_X\big(g^{-1}(y)\big)\ \left\lvert\frac{d\,g^{-1}}{dy}(y)\right\rvert
=\frac{f_X(x)}{\lvert g'(x)\rvert}\Bigg|_{\,x=g^{-1}(y)}\;}$$

⚠️ **Et quand $g$ n'est pas injective, il faut sommer sur les antécédents :**

$$f_Y(y)=\sum_{x\,:\,g(x)=y}\frac{f_X(x)}{\lvert g'(x)\rvert}.$$

C'est le piège du § 9.3 ③ — l'oubli du facteur 2 sur $Y=Z^2$.

---

## 9.3 Trois exemples qui couvrent tout le dépôt

### ① La standardisation $Z=\frac{X-\mu}{\sigma}$

$g^{-1}(z)=\mu+\sigma z$, de dérivée $\sigma$ :

$$f_Z(z)=\sigma\,f_X(\mu+\sigma z)
=\sigma\cdot\frac1{\sigma\sqrt{2\pi}}e^{-z^2/2}=\frac{e^{-z^2/2}}{\sqrt{2\pi}} .$$

> 📐 **Le $\frac1\sigma$ de la densité normale est un jacobien.** Il n'est pas là pour « normaliser
> à 1 » par convention : il est le facteur d'étirement de $x\mapsto\mu+\sigma x$. C'est pourquoi
> une densité change d'**unité** quand la variable en change ([§ 1.3 de statistique](../../statistique/mathematique/01-variable-aleatoire-et-loi.md)).

### ② La log-normale $Y=e^X$, $X\sim\mathcal N(0,1)$

$g^{-1}(y)=\log y$ sur $\mathbb R_+^*$, de dérivée $\frac1y$ :

$$f_Y(y)=\frac1{y\sqrt{2\pi}}\exp\!\left(-\frac{(\log y)^2}{2}\right),\qquad y>0 .$$

Le facteur $\frac1y$ **est** le jacobien — et il est la raison mathématique pour laquelle la
log-normale est asymétrique alors que la normale ne l'est pas : l'exponentielle étire les grandes
valeurs et comprime les petites.

### ③ ⚠️ Le carré $Y=Z^2$, et le facteur 2

$g(z)=z^2$ n'est **pas injective** : $y$ a deux antécédents, $\pm\sqrt y$. Par la méthode générale :

$$F_Y(y)=P\big(-\sqrt y\le Z\le\sqrt y\big)=2\Phi\big(\sqrt y\big)-1
\qquad\Longrightarrow\qquad
f_Y(y)=2\,\phi\big(\sqrt y\big)\cdot\frac1{2\sqrt y}=\frac{e^{-y/2}}{\sqrt{2\pi y}} .$$

C'est exactement la densité du $\chi^2(1)$ du
[§ 15.3 de statistique](../../statistique/mathematique/15-loi-du-chi2.md) — puisque
$\frac{1}{2^{1/2}\Gamma(1/2)}=\frac1{\sqrt{2\pi}}$ par
$\Gamma(\frac12)=\sqrt\pi$ ([§ 4.4](04-integrales-generalisees-et-moments.md)).

> ⚠️ **Appliquer la formule monotone ici donnerait la moitié du résultat.** Les deux branches
> $\pm\sqrt y$ contribuent, et le facteur 2 n'est pas un ajustement : c'est la somme sur les
> antécédents. **Vérifier l'injectivité avant d'utiliser la formule** est la règle.

---

## 9.4 Dimension $n$ : la formule au jacobien

> **Théorème.** Soit $X$ un vecteur aléatoire de densité $f_X$ sur $\mathbb R^n$ et
> $Y=g(X)$ où $g$ est un **difféomorphisme** ($C^1$, bijectif, $\det J_g\ne0$). Alors
> $$\boxed{\;f_Y(y)=f_X\big(g^{-1}(y)\big)\;\Big\lvert\det J_{g^{-1}}(y)\Big\rvert
> =\frac{f_X(x)}{\big\lvert\det J_g(x)\big\rvert}\Bigg|_{\,x=g^{-1}(y)}\;}$$

*Démonstration.* Pour tout borélien $B$,
$P(Y\in B)=P\big(X\in g^{-1}(B)\big)=\int_{g^{-1}(B)}f_X(x)\,dx$. Le changement de variables
$x=g^{-1}(y)$ ([§ 8.3](08-integrales-multiples-et-jacobien.md)) donne
$\int_Bf_X\big(g^{-1}(y)\big)\lvert\det J_{g^{-1}}(y)\rvert\,dy$, valable pour tout $B$ : les deux
densités coïncident. $\blacksquare$

### ⭐ La densité du vecteur gaussien, enfin calculée

Soit $Z\sim\mathcal N_n(0,I_n)$, de densité
$f_Z(z)=(2\pi)^{-n/2}e^{-\lVert z\rVert^2/2}$, et posons $X=\mu+LZ$ avec $LL^{\top}=\Sigma$
(factorisation de Cholesky, $L$ inversible). Alors $g(z)=\mu+Lz$ est affine, donc
$J_g=L$ **constante**, et $g^{-1}(x)=L^{-1}(x-\mu)$ :

$$f_X(x)=\frac{f_Z\big(L^{-1}(x-\mu)\big)}{\lvert\det L\rvert}
=\frac{1}{(2\pi)^{n/2}\lvert\det L\rvert}
\exp\!\left(-\frac12\big\lVert L^{-1}(x-\mu)\big\rVert^2\right).$$

Or $\lVert L^{-1}(x-\mu)\rVert^2=(x-\mu)^{\top}L^{-\top}L^{-1}(x-\mu)=(x-\mu)^{\top}\Sigma^{-1}(x-\mu)$
et $(\det L)^2=\det\Sigma$, d'où

$$\boxed{\;f_X(x)=\frac{1}{(2\pi)^{n/2}\sqrt{\det\Sigma}}
\exp\!\left(-\tfrac12(x-\mu)^{\top}\Sigma^{-1}(x-\mu)\right)\;}$$

> 🔑 **Le $\sqrt{\det\Sigma}$ est un jacobien, ni plus ni moins.** C'est le facteur de volume de
> $L$, exactement comme le $\sigma$ du cas scalaire — dont il est la généralisation, puisque
> $\sqrt{\det\Sigma}=\sigma$ quand $n=1$. Le
> [§ 9.4 de statistique](../../statistique/mathematique/09-vecteur-gaussien.md) avait raison de dire que la voie
> par les combinaisons linéaires est plus courte : **elle évite ce calcul, et fonctionne même
> quand $L$ n'est pas inversible**, cas où aucune densité n'existe.

---

## 9.5 Deux applications directes

### ① Box–Muller : fabriquer des gaussiennes avec deux uniformes

Prenons $(R,\Theta)$ de densité $\frac{r}{2\pi}e^{-r^2/2}$ sur
$\mathbb R_+\times[0,2\pi[$ — c'est-à-dire $\Theta$ uniforme et $R^2\sim\mathcal E(\frac12)$ —
et posons $(X,Y)=(R\cos\Theta,\ R\sin\Theta)$. Le jacobien du passage en polaires vaut $r$
([§ 6.5](06-la-matrice-jacobienne.md)), donc

$$f_{X,Y}(x,y)=\frac{f_{R,\Theta}(r,\theta)}{r}=\frac{e^{-r^2/2}}{2\pi}
=\underbrace{\frac{e^{-x^2/2}}{\sqrt{2\pi}}}_{\mathcal N(0,1)}\cdot
\underbrace{\frac{e^{-y^2/2}}{\sqrt{2\pi}}}_{\mathcal N(0,1)} .$$

**Deux gaussiennes indépendantes**, obtenues de $U_1,U_2$ uniformes par
$R=\sqrt{-2\log U_1}$, $\Theta=2\pi U_2$.

> 🔑 **Le $r$ du jacobien se simplifie exactement avec le $r$ de la densité polaire.** C'est la
> même simplification qu'au [§ 8.4](08-integrales-multiples-et-jacobien.md) — et ce n'est pas une
> coïncidence : Box–Muller **est** le calcul de l'intégrale de Gauss, lu à l'envers.

### ② La transformation inverse et la PIT

| Sens | Énoncé | Où |
|---|---|---|
| **Fabriquer** | $U\sim\mathcal U(0,1)\Rightarrow F^{-1}(U)$ a pour répartition $F$ | Simulation |
| **Valider** | $X$ de répartition $F$ continue $\Rightarrow F(X)\sim\mathcal U(0,1)$ | La **PIT** |

*Démonstration du second sens, en une ligne :* $P\big(F(X)\le u\big)=P\big(X\le F^{-1}(u)\big)=F\big(F^{-1}(u)\big)=u$.
C'est un changement de variable où le jacobien $F'=f$ **s'annule exactement** contre la densité —
la densité de $U$ est plate, précisément parce que $F$ étire là où $f$ est faible.

Ces deux résultats sont énoncés au
[§ 6d.4 de statistique](../../statistique/mathematique/06d-loi-uniforme.md) ; on vient de les démontrer.

---

## 9.6 Vérification numérique

### S9.1 — Les trois densités du § 9.3, testées par la répartition

```python
import numpy as np
from math import erf, sqrt

Phi = lambda t: 0.5 * (1 + np.vectorize(erf)(np.asarray(t) / sqrt(2)))
rng = np.random.default_rng(9)
N = 2_000_000

# (a) log-normale
x = rng.normal(size=N); y = np.exp(x)
g = np.linspace(0.05, 10, 400)
F_emp = np.searchsorted(np.sort(y), g) / N
print("log-normale : sup |F_emp - F_theo| =", np.abs(F_emp - Phi(np.log(g))).max())

# (b) chi2(1) : le facteur 2 compte
z = rng.normal(size=N); w = z ** 2
g = np.linspace(0.01, 12, 400)
F_emp = np.searchsorted(np.sort(w), g) / N
print("chi2(1)     : sup |F_emp - F_theo| =", np.abs(F_emp - (2 * Phi(np.sqrt(g)) - 1)).max())
print("   sans le facteur 2, l'ecart serait de :",
      np.abs(F_emp - (Phi(np.sqrt(g)) - 0.5)).max())
```

Sortie : $8{,}9\cdot10^{-4}$ et $6{,}5\cdot10^{-4}$ — l'erreur d'échantillonnage, rien d'autre.
La dernière ligne montre ce que coûte l'oubli des deux branches : un écart de **0,5**, c'est-à-dire
une densité fausse d'un facteur 2.

> ⚠️ **Comparer des répartitions, pas des histogrammes.** Un histogramme de densité près d'une
> singularité (ici $y\to0$, où la densité du $\chi^2(1)$ explose) donne des erreurs relatives de
> plusieurs dizaines de pour cent qui ne prouvent rien. **La fonction de répartition, elle, est
> bornée et stable** : c'est le bon outil de vérification.

### S9.2 — Box–Muller à la main

```python
u1, u2 = rng.random(1_000_000), rng.random(1_000_000)
r, theta = np.sqrt(-2 * np.log(u1)), 2 * np.pi * u2
X, Y = r * np.cos(theta), r * np.sin(theta)

print(f"moyennes  : {X.mean():+.4f} {Y.mean():+.4f}   (attendu 0)")
print(f"variances : {X.var():.4f} {Y.var():.4f}   (attendu 1)")
print(f"correlation : {np.corrcoef(X, Y)[0, 1]:+.4f}   (attendu 0)")
print(f"kurtosis  : {(((X - X.mean()) / X.std()) ** 4).mean():.4f}   (attendu 3)")
```

Quatre moments, quatre valeurs gaussiennes — obtenues à partir de deux uniformes et d'un jacobien.

### S9.3 — La densité gaussienne multivariée, par la formule du § 9.4

```python
d = 3
L = np.tril(rng.normal(size=(d, d))) + d * np.eye(d)
Sigma, mu = L @ L.T, rng.normal(size=d)
N = 4_000_000
Z = rng.normal(size=(N, d))
X = mu + Z @ L.T

def densite(x):
    e = x - mu
    return np.exp(-0.5 * e @ np.linalg.solve(Sigma, e)) / \
           np.sqrt((2 * np.pi) ** d * np.linalg.det(Sigma))

# verification : la densite estimee par voisinage colle-t-elle a la formule ?
pt = mu + 0.3 * np.sqrt(np.diag(Sigma))
for eps in (0.15, 0.3, 0.5, 1.0):
    masse = (np.abs(X - pt) < eps / 2).all(axis=1).mean()
    print(f"eps={eps:4.2f} : formule = {densite(pt):.6f}   estimee = {masse / eps ** d:.6f}"
          f"   ({masse * N:.0f} points dans le cube)")
print(f"covariance empirique vs Sigma : ecart max = "
      f"{np.abs(np.cov(X, rowvar=False) - Sigma).max():.4f}")
```

La densité calculée par la formule au jacobien coïncide avec la masse observée dans un petit cube
divisée par son volume — c'est-à-dire avec la **définition** d'une densité : $0{,}002411$ contre
$0{,}002430$ à $\varepsilon=0{,}5$.

⚠️ **La boucle sur $\varepsilon$ est l'enseignement du test.** Trop petit ($0{,}15$ : 29 points
dans le cube), l'estimation est bruitée ; trop grand ($1{,}0$), elle est biaisée par la courbure
de la densité. **En dimension $d$, le nombre de points dans un cube de côté $\varepsilon$ décroît
comme $\varepsilon^{d}$** — c'est la raison pour laquelle estimer une densité devient impraticable
bien avant $d=10$.

---

## 9.7 Exercices

**E9.1.** Établir la densité de $Y=aX+b$ ($a\ne0$) par la méthode de la répartition, et vérifier
qu'on retrouve $\frac1{\lvert a\rvert}f_X\big(\frac{y-b}a\big)$. *Pourquoi la valeur absolue ?*

**E9.2.** Calculer la densité de $Y=1/X$ pour $X\sim\mathcal U(1,2)$. *Vérifier que
$\int f_Y=1$ — c'est le test qui détecte un jacobien oublié.*

**E9.3.** Refaire le calcul de la densité du $\chi^2(1)$ en oubliant volontairement le facteur 2,
puis montrer que la fonction obtenue **ne s'intègre pas à 1**. *Quelle vérification systématique
cet exercice suggère-t-il ?*

**E9.4.** Soit $X\sim\mathcal E(\lambda)$. Trouver la densité de $Y=\sqrt X$. *(Loi de Rayleigh.)*

**E9.5.** Démontrer la formule de la densité gaussienne multivariée en détaillant le passage
$\lvert\det L\rvert=\sqrt{\det\Sigma}$. *Que se passe-t-il si $\Sigma$ est **singulière** — et
quelle affirmation du [§ 9.4 de statistique](../../statistique/mathematique/09-vecteur-gaussien.md) cela
justifie-t-il ?*

**E9.6.** Démontrer la PIT, puis l'utiliser pour construire un test graphique de normalité sur
une série de rendements obtenue avec `import_societe.py`. *(Tracer $F(x_i)$ trié contre
$i/n$ : la droite $y=x$ est l'hypothèse.)*

**E9.7.** Montrer que $(X,Y)$ de Box–Muller sont **indépendantes**, en constatant que la densité
jointe se factorise. *À quel endroit précis du calcul l'indépendance apparaît-elle ?*

---

## 9.8 À retenir

- **Une probabilité se transporte sans correction ; une densité, non** — car elle est une
  probabilité **par unité de volume**, et le volume se déforme.
- ⭐ **$f_Y(y)=f_X\big(g^{-1}(y)\big)\,\lvert\det J_{g^{-1}}(y)\rvert$** : c'est le théorème de
  changement de variables du [module 8](08-integrales-multiples-et-jacobien.md), lu en
  probabilité.
- ⚠️ **Vérifier l'injectivité** : pour $Y=Z^2$, il faut **sommer sur les deux antécédents**, d'où
  le facteur 2 qui donne la densité du $\chi^2(1)$.
- **Le $\frac1\sigma$ de la densité normale et le $\sqrt{\det\Sigma}$ du vecteur gaussien sont le
  même objet** : le facteur de volume de la transformation affine qui fabrique la variable.
- **Box–Muller est l'intégrale de Gauss lue à l'envers** : le $r$ du jacobien s'y simplifie de la
  même façon.
- **Test systématique** : une densité obtenue doit s'intégrer à 1, et se vérifie **par la fonction
  de répartition**, jamais par un histogramme près d'une singularité.

---

⬅️ [Module 8 — Intégrales multiples et facteur de volume](08-integrales-multiples-et-jacobien.md) ·
🏠 [Sommaire](README.md) ·
📘 [Cours de statistique](../../statistique/mathematique/README.md) ·
📗 [Cours d'analyse — convexité](../convexite/README.md) ·
📐 [Cours d'algèbre](../../algebre/README.md)
