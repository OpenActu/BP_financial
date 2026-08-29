# Module 9 — Le vecteur gaussien

**Durée : 1 h.** Prérequis : module [8](08-addition-de-lois-et-stabilite-gaussienne.md), et la
notion de norme dans $\mathbb R^n$ (module 5 du [cours d'algèbre](../../algebre/01-produit-scalaire-et-norme.md)).

> **La question traitée.** Le [§ 8.5](08-addition-de-lois-et-stabilite-gaussienne.md) a laissé
> une hypothèse en suspens : que faut-il exiger d'un couple de gaussiennes **dépendantes** pour
> que leurs combinaisons linéaires restent gaussiennes ?

**Ce qui est en jeu.** La réponse est une définition — celle du vecteur gaussien — et elle est
contre-intuitive : **des marges gaussiennes ne suffisent pas**. Le contre-exemple du § 9.3 est le
plus rentable de tout le cours ; il réfute trois erreurs classiques d'un seul coup.

---

## 9.1 Définition

> **Définition.** Un vecteur aléatoire $\mathbf X=(X_1,\dots,X_n)$ de $\mathbb R^n$ est un
> **vecteur gaussien** si **toute** combinaison linéaire $\sum_i a_iX_i$ ($a\in\mathbb R^n$) suit
> une loi gaussienne (éventuellement dégénérée, c'est-à-dire constante).

Cette définition surprend : on définit un objet de dimension $n$ par une propriété de toutes ses
projections unidimensionnelles. C'est pourtant la bonne — et c'est exactement ce qui la rend
maniable, comme le montrera le [§ 10.4](10-decorrelation-et-independance.md).

Un vecteur gaussien est entièrement caractérisé par :
- son **vecteur espérance** $\boldsymbol\mu=E(\mathbf X)$ ;
- sa **matrice de covariance** $\Sigma$, avec $\Sigma_{ij}=\operatorname{Cov}(X_i,X_j)$.

On note $\mathbf X\sim\mathcal N_n(\boldsymbol\mu,\Sigma)$.

> 🔑 **Deux nombres par coordonnée et une matrice suffisent à tout.** Aucune autre famille de lois
> multivariées n'est aussi complètement décrite par ses deux premiers moments.

---

## 9.2 Le cas fondamental : le vecteur gaussien standard

Si $Z_1,\dots,Z_n$ sont i.i.d. $\mathcal N(0,1)$, alors
$\mathbf Z\sim\mathcal N_n(\mathbf 0, I_n)$ — le **vecteur gaussien standard**. Sa densité vaut

$$f(\mathbf z)=\frac{1}{(2\pi)^{n/2}}\exp\!\left(-\frac{\|\mathbf z\|^2}{2}\right)$$

> 🔑 **Retenez cette densité, elle contient tout ce qui suit.** Elle ne dépend de $\mathbf z$ que
> par sa **norme** $\|\mathbf z\|$. Autrement dit : la loi gaussienne standard est **isotrope** —
> elle ne privilégie aucune direction de l'espace. Les surfaces de niveau sont des **sphères**.

Toutes les conséquences du [module 11](11-invariance-par-rotation-et-lemme-de-projection.md) — et
donc tout [Fisher–Cochran](16-theoreme-de-fisher-cochran.md) — découlent de cette seule
observation.

**Le cas général s'y ramène.** Si $\Sigma$ est inversible,
$\Sigma^{-1/2}(\mathbf X-\boldsymbol\mu)\sim\mathcal N_n(\mathbf 0,I_n)$ : c'est la
**standardisation multivariée** (exercice E9.5).

---

## 9.3 ⚠️ Le piège : marges gaussiennes ≠ vecteur gaussien

> **Ce n'est pas parce que chaque $X_i$ est gaussienne que $(X_1,\dots,X_n)$ est un vecteur
> gaussien.**

**Contre-exemple.** Soient $X\sim\mathcal N(0,1)$ et $\varepsilon$ valant $+1$ ou $-1$ avec
probabilité $\tfrac12$ chacune, **indépendante** de $X$. Posons $Y=\varepsilon X$.

- $Y\sim\mathcal N(0,1)$ : par symétrie de la loi normale, $-X$ a la même loi que $X$, donc
  $Y$ aussi. **Les deux marges sont parfaitement gaussiennes.**
- $\operatorname{Cov}(X,Y)=E(\varepsilon X^2)=E(\varepsilon)\,E(X^2)=0\times 1=0$.
  **Elles sont décorrélées.**
- **Mais $X+Y=(1+\varepsilon)X$ vaut $0$ avec probabilité $\tfrac12$** et $2X$ sinon. Une loi qui
  charge le point 0 d'une masse $\tfrac12$ n'est pas gaussienne. **Donc $(X,Y)$ n'est pas un
  vecteur gaussien.**
- Et $X$ et $Y$ sont manifestement **dépendantes** : on a toujours $|X|=|Y|$. Connaître $X$
  détermine $Y$ au signe près.

Vérification numérique (§ 9.5, S9.1) : les deux marges passent un test de Kolmogorov–Smirnov de
normalité ($p=0{,}69$ et $p=0{,}26$), la corrélation vaut $+0{,}001$, et pourtant $49{,}9\,\%$ des
valeurs de $X+Y$ sont **exactement nulles**.

> ⚠️ **C'est le contre-exemple à connaître.** Il montre d'un coup que :
>  ① des marges gaussiennes ne font pas un vecteur gaussien ;
>  ② décorrélation n'implique pas indépendance ([module 10](10-decorrelation-et-independance.md)) ;
>  ③ une somme de gaussiennes dépendantes peut ne pas être gaussienne
>  ([§ 8.5](08-addition-de-lois-et-stabilite-gaussienne.md)).
>  Trois erreurs classiques, un seul exemple.

---

## 9.4 La propriété qui rend la définition efficace

> **Proposition.** L'image d'un vecteur gaussien par une application **linéaire** est un vecteur
> gaussien.

**Démonstration.** Soit $\mathbf Y=A\mathbf X$. Toute combinaison linéaire de $\mathbf Y$,
$\langle a,\mathbf Y\rangle=\langle A^{\top}a,\mathbf X\rangle$, est une combinaison linéaire de
$\mathbf X$ — donc gaussienne par définition. $\blacksquare$

Et ses paramètres se calculent sans effort :
$$E(A\mathbf X)=A\boldsymbol\mu\qquad\text{et}\qquad \operatorname{Cov}(A\mathbf X)=A\,\Sigma\,A^{\top}$$

> 🔑 **C'est ici que la définition « par les combinaisons linéaires » montre son efficacité.**
> Une définition par la densité aurait exigé un calcul de jacobien — celui-ci est fait au
> [§ 9.4 du cours de dérivation et intégration](../../analyse/derivation-et-integration/09-changement-de-variable-et-densites.md),
> et il confirme le point : la voie par les combinaisons linéaires donne le résultat
> en une ligne, et **même quand $A$ n'est pas inversible**. Le
> [module 11](11-invariance-par-rotation-et-lemme-de-projection.md) l'utilisera avec $A$
> orthogonale, le [module 16](16-theoreme-de-fisher-cochran.md) avec $A$ un projecteur.

---

## 9.5 Simulation

### S9.1 — Le contre-exemple : marges gaussiennes, vecteur non gaussien

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(21)
N = 500_000

X = rng.standard_normal(N)
eps = rng.choice([-1.0, 1.0], N)          # indépendant de X
Y = eps * X

print(f"X gaussienne ?  KS p = {stats.kstest(X, 'norm').pvalue:.3f}")
print(f"Y gaussienne ?  KS p = {stats.kstest(Y, 'norm').pvalue:.3f}")
print(f"corrélation     = {np.corrcoef(X, Y)[0, 1]:+.5f}")
print(f"mais |X| = |Y| toujours : {np.allclose(np.abs(X), np.abs(Y))}")

S = X + Y
print(f"part de X+Y EXACTEMENT nuls : {np.mean(S == 0):.3f}   → pas gaussienne")
```

**Résultat** : $p=0{,}69$ et $p=0{,}26$ (les deux marges sont gaussiennes), corrélation
$+0{,}001$ — et pourtant **49,9 %** des valeurs de $X+Y$ valent exactement 0. Trois erreurs
classiques réfutées d'un coup.

### S9.2 — L'isotropie, et l'image linéaire

```python
Z = rng.standard_normal((300_000, 2))
r = np.linalg.norm(Z, axis=1)
angle = np.arctan2(Z[:, 1], Z[:, 0])
print("angle uniforme sur [-pi, pi] ? KS p =",
      round(stats.kstest(angle, "uniform", args=(-np.pi, 2*np.pi)).pvalue, 3))
print("norme independante de l'angle ? corr =",
      round(np.corrcoef(r, np.abs(angle))[0, 1], 4))

A = np.array([[2.0, 1.0], [0.0, 3.0]])
Y = Z @ A.T
print("\ncov(AZ) =\n", np.round(np.cov(Y.T), 3))
print("theorie A A^T =\n", np.round(A @ A.T, 3))
```

**L'angle est uniforme et indépendant de la norme** : c'est l'isotropie du § 9.2, vue
directement. Aucune direction n'est privilégiée.

---

## 9.6 Exercices

**E9.1.** Vérifier que si $(X,Y)$ est un vecteur gaussien, alors $X$ et $Y$ sont gaussiennes.
*La réciproque est-elle vraie ? (§ 9.3.)*

**E9.2.** Dans le contre-exemple du § 9.3, calculer explicitement la loi de $X+Y$ et celle de
$X-Y$. *L'une des deux est-elle gaussienne ?*

**E9.3.** Soit $\mathbf X\sim\mathcal N_2(\mathbf 0,\Sigma)$ avec
$\Sigma=\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}$. Donner la loi de $X_1+X_2$ et celle de
$X_1-X_2$. *Pour quelle valeur de $\rho$ la seconde est-elle dégénérée ?*

**E9.4.** Montrer que $\operatorname{Cov}(A\mathbf X)=A\Sigma A^{\top}$. *(Piste : partir de
$\operatorname{Cov}(\mathbf Y)=E\bigl((\mathbf Y-E\mathbf Y)(\mathbf Y-E\mathbf Y)^{\top}\bigr)$.)*

**E9.5.** Montrer que si $\mathbf X\sim\mathcal N_n(\boldsymbol\mu,\Sigma)$ avec $\Sigma$
inversible, alors $\Sigma^{-1/2}(\mathbf X-\boldsymbol\mu)\sim\mathcal N_n(\mathbf 0,I_n)$.
*C'est la standardisation multivariée : elle ramène tout vecteur gaussien au cas standard.*

**E9.6.** Trouver un troisième contre-exemple de couple gaussien-décorrélé-dépendant, différent
de $Y=\varepsilon X$ et de $Y=X^2$. *(Piste : $Y=X$ si $|X|>c$ et $Y=-X$ sinon ; ajuster $c$ pour
annuler la covariance.)*

**E9.7 — orientée finance.** Les rendements de deux titres sont-ils un vecteur gaussien ?
1. Tester la normalité de chaque marge (QQ-plot, Jarque–Bera).
2. Tester la normalité de $R_1+R_2$ et de $R_1-R_2$.
3. Comparer la corrélation en période calme et en période de crise.

**Enseignement attendu** : les marges peuvent paraître à peu près gaussiennes tandis que le
couple ne l'est pas du tout — la corrélation des actions **monte fortement dans les krachs**
(*correlation breakdown*). Un modèle de portefeuille qui suppose un vecteur gaussien sous-estime
alors gravement le risque simultané, précisément au moment où il importe. C'est l'illustration
financière du piège du § 9.3.

---

## 9.7 À retenir

- **Vecteur gaussien** = *toute* combinaison linéaire de ses coordonnées est gaussienne.
  Caractérisé par $(\boldsymbol\mu,\Sigma)$, rien d'autre.
- ⚠️ **Des marges gaussiennes ne suffisent pas** : $Y=\varepsilon X$ le montre en trois lignes.
- **Densité standard** $\propto e^{-\|\mathbf z\|^2/2}$ : elle ne dépend que de la **norme**, donc
  la loi est **isotrope**.
- **L'image linéaire d'un vecteur gaussien est un vecteur gaussien**, de paramètres
  $A\boldsymbol\mu$ et $A\Sigma A^{\top}$ — même si $A$ n'est pas inversible.

---

⬅️ [Module 8 — Addition de lois et stabilité gaussienne](08-addition-de-lois-et-stabilite-gaussienne.md) ·
➡️ [Module 10 — Décorrélation et indépendance](10-decorrelation-et-independance.md) ·
🏠 [Sommaire](README.md)
