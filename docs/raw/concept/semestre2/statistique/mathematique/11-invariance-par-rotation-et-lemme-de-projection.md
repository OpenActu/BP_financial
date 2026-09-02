# Module 11 — Invariance par rotation et lemme de projection ⭐

**Durée : 1 h 15.** Prérequis : module [10](10-decorrelation-et-independance.md), et les
[modules 4 à 6 du cours d'algèbre](../../../semestre1/algebre/README.md) — projection orthogonale,
$\mathbb R^n=F\oplus F^\perp$, bases orthonormées, isométries.

⚠️ **C'est le module le plus important du cours.** Les modules 9 et 10 posent le décor ; celui-ci
fournit **l'outil**. Le [théorème de Fisher–Cochran](16-theoreme-de-fisher-cochran.md) n'est rien
d'autre que le lemme du § 11.3, appliqué en dimension $n$. Qui maîtrise ce § 11.3 trouvera le
module 16 presque évident ; qui le survole y verra de la magie.

> **La question traitée.** Le [§ 10.5](10-decorrelation-et-independance.md) a montré, en dimension
> 2, que deux directions orthogonales produisent des variables indépendantes. Que devient cet
> énoncé en dimension $n$, pour des **sous-espaces** au lieu de directions ?

---

## 11.1 L'invariance par rotation

> **Proposition.** Soit $\mathbf Z\sim\mathcal N_n(\mathbf 0,I_n)$ et $O$ une matrice
> **orthogonale** ($OO^{\top}=I_n$). Alors
> $$O\mathbf Z\;\sim\;\mathcal N_n(\mathbf 0,I_n).$$
> Autrement dit : **la loi gaussienne standard est invariante par rotation.**

**Démonstration.** $O\mathbf Z$ est un vecteur gaussien (image linéaire d'un vecteur gaussien,
[§ 9.4](09-vecteur-gaussien.md)), centré, de matrice de covariance
$$\operatorname{Cov}(O\mathbf Z)=O\,\operatorname{Cov}(\mathbf Z)\,O^{\top}=O\,I_n\,O^{\top}=OO^{\top}=I_n.
\qquad\blacksquare$$

Un vecteur gaussien étant caractérisé par $(\boldsymbol\mu,\Sigma)$ ([§ 9.1](09-vecteur-gaussien.md)),
et ces deux quantités étant inchangées, **la loi est identique**. Trois lignes.

**L'explication géométrique**, plus parlante que le calcul : la densité
$\frac{1}{(2\pi)^{n/2}}e^{-\|\mathbf z\|^2/2}$ ne dépend que de $\|\mathbf z\|$
([§ 9.2](09-vecteur-gaussien.md)), et une rotation **conserve la norme**. La densité est donc
littéralement inchangée. Les surfaces de niveau sont des **sphères**, et une sphère tourne sur
elle-même.

> 🔑 **C'est la rencontre exacte entre l'algèbre et la probabilité.** Le
> [module 9 du cours d'algèbre](../../../semestre1/algebre/09-bases-orthonormees-et-isometries.md) a établi
> qu'une matrice orthogonale conserve les normes ; le § 9.2 a établi que la densité gaussienne ne
> dépend que de la norme. La proposition ci-dessus est la simple mise bout à bout des deux.

---

## 11.2 Les deux conséquences

1. **Les coordonnées de $\mathbf Z$ dans n'importe quelle base orthonormée sont encore i.i.d.
   $\mathcal N(0,1)$.** La base canonique n'a rien de privilégié — on peut donc choisir *la base
   la plus commode* sans rien perdre.
2. **$\|\mathbf Z\|^2$ est invariant par rotation** — d'où la loi
   [$\chi^2(n)$ du module 15](15-loi-du-chi2.md), qui ne dépend que de la dimension.

⚠️ **La première conséquence est la licence dont vit toute la suite.** Sans elle, chaque
démonstration devrait travailler dans la base des données ; avec elle, on choisit la base adaptée
au problème.

---

## 11.3 Le lemme de projection ⭐

C'est le résultat que le [module 16](16-theoreme-de-fisher-cochran.md) utilisera tel quel. Il
n'est que la mise en forme des § 11.1 et 7.2.

> **Lemme.** Soit $\mathbf Z\sim\mathcal N_n(\mathbf 0,I_n)$ et $\mathbb R^n=F\oplus F^\perp$ une
> décomposition orthogonale avec $\dim F=d$. Alors :
> - $P_F(\mathbf Z)$ et $P_{F^\perp}(\mathbf Z)$ sont **indépendants** ;
> - $\|P_F(\mathbf Z)\|^2\sim\chi^2(d)$ et $\|P_{F^\perp}(\mathbf Z)\|^2\sim\chi^2(n-d)$.

**Démonstration.** Choisissons une base orthonormée $(u_1,\dots,u_n)$ **adaptée** : les $d$
premiers vecteurs engendrent $F$, les $n-d$ suivants engendrent $F^\perp$ — son existence est
garantie par Gram–Schmidt
([§ 9.3 du cours d'algèbre](../../../semestre1/algebre/09-bases-orthonormees-et-isometries.md)). Soit $O$ la
matrice orthogonale dont les lignes sont ces vecteurs, et $\mathbf Y=O\mathbf Z$.

Par le § 11.1, $Y_1,\dots,Y_n$ sont i.i.d. $\mathcal N(0,1)$. Or $Y_j=\langle\mathbf Z,u_j\rangle$,
donc
$$\|P_F(\mathbf Z)\|^2=\sum_{j=1}^{d}Y_j^2
\qquad\text{et}\qquad
\|P_{F^\perp}(\mathbf Z)\|^2=\sum_{j=d+1}^{n}Y_j^2 .$$

Ces deux sommes portent sur des **blocs disjoints** de variables indépendantes : elles sont donc
indépendantes, et chacune est une somme de carrés de $\mathcal N(0,1)$ indépendantes, c'est-à-dire
un $\chi^2$ dont le paramètre est le nombre de termes. $\blacksquare$

> 🔑 **Le [§ 10.3](10-decorrelation-et-independance.md) est le cas $n=2$, $d=1$** avec
> $F=\text{Vect}(1,1)$ : $S/\sqrt2$ est la coordonnée sur $F$, $D/\sqrt2$ celle sur $F^\perp$.
> Tout le [module 16](16-theoreme-de-fisher-cochran.md) consiste à appliquer ce même lemme avec
> $n$ quelconque et $F=\text{Vect}(\mathbf 1)$ — d'où $d=1$ et $n-d=n-1$ degrés de liberté.

---

## 11.4 Application directe : la transformation de Helmert

Pour rendre le lemme concret, voici la base adaptée à $F=\text{Vect}(\mathbf 1)$ en dimension 3 :

$$u_1=\frac{1}{\sqrt3}(1,1,1),\qquad
u_2=\frac{1}{\sqrt2}(1,-1,0),\qquad
u_3=\frac{1}{\sqrt6}(1,1,-2)$$

**Vérifications** (à faire soi-même) : les trois vecteurs sont unitaires, et
$\langle u_1,u_2\rangle=\langle u_1,u_3\rangle=\langle u_2,u_3\rangle=0$.

Les vecteurs $u_2,u_3$ sont les **contrastes de Helmert** : ils engendrent l'hyperplan des
vecteurs de somme nulle. Avec $\mathbf Y=O\mathbf Z$ :

- $Y_1=\sqrt3\,\bar Z$ — toute l'information sur la **moyenne** ;
- $Y_2^2+Y_3^2=\sum_i(Z_i-\bar Z)^2$ — toute l'information sur la **dispersion** ;
- et $Y_1\perp\!\!\!\perp(Y_2,Y_3)$ par le lemme.

**C'est Fisher–Cochran, en dimension 3, sans aucun calcul supplémentaire.** La généralisation à
$n$ quelconque ne demande qu'une base de Helmert de taille $n$, dont l'existence est garantie par
le procédé de Gram–Schmidt.

---

## 11.5 Simulations

### S11.1 — L'invariance par rotation

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(21)
Z = rng.standard_normal((500_000, 3))
th = 0.7
O = np.array([[np.cos(th), -np.sin(th), 0],
              [np.sin(th),  np.cos(th), 0],
              [0,           0,          1.0]])
print("O orthogonale ?", np.allclose(O @ O.T, np.eye(3)))

Y = Z @ O.T
print("cov(OZ) =\n", np.round(np.cov(Y.T), 3))          # ≈ identité
print("norme conservée ?", np.allclose((Z**2).sum(1), (Y**2).sum(1)))
```

La matrice de covariance après rotation est l'identité, à l'erreur de simulation près : la loi
n'a pas bougé. **Testez avec une matrice non orthogonale** — la covariance cesse aussitôt d'être
l'identité.

### S11.2 — Le lemme de projection en dimension 3 (Helmert)

```python
u1 = np.array([1, 1, 1]) / np.sqrt(3)
u2 = np.array([1, -1, 0]) / np.sqrt(2)
u3 = np.array([1, 1, -2]) / np.sqrt(6)
O = np.vstack([u1, u2, u3])
print("base orthonormée ?", np.allclose(O @ O.T, np.eye(3)))

Z = rng.standard_normal((400_000, 3))
Y = Z @ O.T
partF, partH = Y[:, 0]**2, Y[:, 1]**2 + Y[:, 2]**2

print(f"E(part F) = {partF.mean():.4f}  (théorie 1)")
print(f"E(part H) = {partH.mean():.4f}  (théorie 2)")
print("KS chi2(1) :", stats.kstest(partF, "chi2", args=(1,)).pvalue)
print("KS chi2(2) :", stats.kstest(partH, "chi2", args=(2,)).pvalue)
print(f"corr(partF, partH) = {np.corrcoef(partF, partH)[0, 1]:+.5f}")

# contrôle : partF = 3*Zbar², partH = somme des écarts au carré
Zb = Z.mean(1)
print("identités vérifiées :",
      np.allclose(partF, 3 * Zb**2),
      np.allclose(partH, ((Z - Zb[:, None])**2).sum(1)))
```

Les deux dernières lignes sont le cœur : elles montrent que $Y_1^2$ **est** l'information sur la
moyenne et $Y_2^2+Y_3^2$ **est** l'information sur la dispersion. Fisher–Cochran, en dimension 3.

### S11.3 — Le lemme pour un $d$ quelconque

```python
n, d, N = 10, 4, 200_000
A = rng.normal(size=(n, d))
P = A @ np.linalg.inv(A.T @ A) @ A.T          # projecteur sur un F de dimension d
Q = np.eye(n) - P

Z = rng.standard_normal((N, n))
nF = ((Z @ P.T) ** 2).sum(1)
nH = ((Z @ Q.T) ** 2).sum(1)

print(f"E = {nF.mean():.3f} / {nH.mean():.3f}   (théorie {d} / {n-d})")
print("KS chi2(d)   :", round(stats.kstest(nF, "chi2", args=(d,)).pvalue, 3))
print("KS chi2(n-d) :", round(stats.kstest(nH, "chi2", args=(n-d,)).pvalue, 3))
print(f"corr = {np.corrcoef(nF, nH)[0, 1]:+.5f}")
```

**Le sous-espace $F$ est tiré au hasard** — le lemme ne dépend que de sa **dimension**, jamais de
son orientation. C'est l'invariance par rotation, vue une dernière fois.

---

## 11.6 Exercices

**E11.1.** Vérifier que les trois vecteurs de Helmert du § 11.4 forment une base orthonormée.
Construire la base analogue en dimension 4.

**E11.2.** Démontrer les deux identités du § 11.4 : $Y_1=\sqrt3\,\bar Z$ et
$Y_2^2+Y_3^2=\sum_i(Z_i-\bar Z)^2$. *(Piste : Parseval — le carré de la norme est la somme des
carrés des coordonnées.)*

**E11.3.** Que devient le lemme du § 11.3 si $\mathbf Z\sim\mathcal N_n(\mathbf 0,\sigma^2 I_n)$ ?
Et si $\mathbf Z\sim\mathcal N_n(\boldsymbol\mu,I_n)$ avec $\boldsymbol\mu\ne\mathbf 0$ ?
*(Réponse au second point : on obtient un $\chi^2$ **décentré** — voir
[§ 15.6](15-loi-du-chi2.md).)*

**E11.4.** Soit $O$ orthogonale et $\mathbf X\sim\mathcal N_n(\mathbf 0,\Sigma)$ avec $\Sigma$
quelconque. $O\mathbf X$ a-t-il la même loi que $\mathbf X$ ? *Quelle propriété du § 11.1 est
perdue, et pourquoi ?*

**E11.5.** Appliquer le lemme avec $F=\text{Vect}(\mathbf 1, t)$, $t=(1,\dots,n)$. Quelles lois
obtient-on ? *(C'est la géométrie du test de pente en régression.)*

---

## 11.7 À retenir

- **La loi gaussienne standard est invariante par rotation** — parce que sa densité ne dépend que
  de la norme, et qu'une rotation conserve la norme.
- **Conséquence** : les coordonnées dans **n'importe quelle** base orthonormée restent i.i.d.
  $\mathcal N(0,1)$. On peut donc toujours choisir la base la plus commode.
- ⭐ **Lemme de projection** : projections sur sous-espaces orthogonaux ⟹ **indépendance**, et
  $\|P_F(\mathbf Z)\|^2\sim\chi^2(\dim F)$.
- **Une seule idée, trois modules** : *projeter un vecteur gaussien standard sur des sous-espaces
  orthogonaux produit des quantités indépendantes, dont les carrés des normes sont des $\chi^2$
  de paramètre la dimension.*
- **Helmert** rend la chose concrète : une coordonnée pour la moyenne, $n-1$ pour la dispersion.

---

⬅️ [Module 10 — Décorrélation et indépendance](10-decorrelation-et-independance.md) ·
➡️ [Module 11 bis — La convergence en loi](11bis-convergence-en-loi.md) ·
🏠 [Sommaire](README.md)
