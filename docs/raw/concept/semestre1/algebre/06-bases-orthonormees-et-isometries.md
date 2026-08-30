# Module 6 — Bases orthonormées, isométries, Gram–Schmidt

**Durée : 1 h.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) à
[5](05-supplementaire-orthogonal-et-dimension.md).

> **La question traitée.** Le [module 4](04-projection-orthogonale.md) suppose une base
> orthonormée pour projeter. En existe-t-il toujours une ? Peut-on en choisir une **adaptée** à
> une décomposition $F\oplus F^\perp$ donnée ?

**Ce qui est en jeu.** La réponse est oui dans les deux cas, et c'est ce qui rend calculable tout
ce qui précède. C'est aussi le module qui fait le pont vers la probabilité : une base orthonormée
est une **isométrie**, et une isométrie laisse invariante la loi gaussienne standard.

---

## 6.1 Bases orthonormées

> **Définition.** $(e_1,\dots,e_n)$ est une **base orthonormée** (BON) de $\mathbb R^n$ si
> $\langle e_j,e_k\rangle=\delta_{jk}$.

C'est bien une base : la famille est orthogonale et sans vecteur nul, donc libre
([§ 3.3](03-orthogonalite-et-pythagore.md)), et elle compte $n$ vecteurs.

Deux conséquences immédiates :

- **Coordonnées gratuites** : $x=\sum_j\langle x,e_j\rangle\,e_j$ — chaque coordonnée est un
  simple produit scalaire, sans résolution de système.
- **Identité de Parseval** : $\|x\|^2=\sum_j\langle x,e_j\rangle^2$ — un Pythagore à $n$ termes
  (§ 3.2), appliqué à la décomposition ci-dessus.

> 🔑 **En base orthonormée, tout devient une somme de carrés.** C'est la raison technique pour
> laquelle les sommes de carrés sont omniprésentes en statistique : ce sont les normes, lues dans
> une base bien choisie.

---

## 6.2 Matrices orthogonales et isométries

Soit $O$ la matrice dont les **lignes** sont les $e_j$. Alors

$$OO^{\top}=I_n
\qquad\Longleftrightarrow\qquad
\langle Ou,Ov\rangle=\langle u,v\rangle\ \ \forall u,v
\qquad\Longrightarrow\qquad \|Ou\|=\|u\|$$

Une matrice orthogonale est donc une **isométrie** : elle conserve longueurs, angles et
orthogonalité. Géométriquement, une rotation (ou une rotation composée d'une symétrie, selon le
signe du déterminant, qui vaut $\pm1$).

> ⚠️ **Changer de base orthonormée ne change rien à la géométrie.** C'est pourquoi on peut
> toujours se placer « dans la base la plus commode » sans perte de généralité — argument utilisé
> sans relâche dans les démonstrations du
> [cours sur la loi de Student](../../semestre3/statistique/loi-de-student/README.md).

---

## 6.3 Gram–Schmidt : une BON adaptée existe toujours

> **Théorème.** Étant donné $F$ de dimension $d$, il existe une BON $(e_1,\dots,e_n)$ de
> $\mathbb R^n$ dont les $d$ premiers vecteurs engendrent $F$ et les $n-d$ suivants $F^\perp$.

Le procédé de **Gram–Schmidt** le construit explicitement : partant d'une base $(u_1,\dots,u_d)$
de $F$, on pose $e_1=u_1/\|u_1\|$, puis à chaque étape on retranche à $u_k$ ses projections sur
les $e_j$ déjà construits — c'est la
[projection du module 4](04-projection-orthogonale.md) — et on normalise :

$$w_k=u_k-\sum_{j<k}\langle u_k,e_j\rangle\,e_j,\qquad e_k=\frac{w_k}{\|w_k\|}$$

On complète ensuite en une base de $\mathbb R^n$ et on recommence : les vecteurs ajoutés
engendrent $F^\perp$.

**Dans une telle base, les deux projections se lisent sur des blocs de coordonnées disjoints** :
$P_F$ garde les $d$ premières coordonnées et annule les autres. Projeter devient trivial ; c'est
tout l'intérêt.

---

## 6.4 L'exemple à connaître : la base de Helmert

Pour $F=\text{Vect}(\mathbf 1)$ en dimension 3 :

$$e_1=\frac{1}{\sqrt3}(1,1,1),\qquad
e_2=\frac{1}{\sqrt2}(1,-1,0),\qquad
e_3=\frac{1}{\sqrt6}(1,1,-2)$$

$$\langle x,e_1\rangle=\sqrt3\,\bar x
\qquad\text{et}\qquad
\langle x,e_2\rangle^2+\langle x,e_3\rangle^2=\sum_i(x_i-\bar x)^2$$

**Une coordonnée pour la moyenne, $n-1$ pour la dispersion.** La décomposition du
[module 5](05-supplementaire-orthogonal-et-dimension.md) devient une simple séparation de
coordonnées.

> 🔑 **Vous venez de faire tout le travail géométrique du théorème de Fisher–Cochran.** Il ne
> reste qu'à poser une question probabiliste : *que devient un vecteur **aléatoire gaussien**
> dans une telle base ?* C'est l'objet du
> [module 11 du cours de statistique](../../semestre2/statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md). La réponse — les
> coordonnées restent i.i.d. $\mathcal N(0,1)$ — est le
> [théorème de Fisher–Cochran](../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md).

---

## 6.5 Simulations

### S6.1 — Une base adaptée (Helmert) sépare moyenne et dispersion

```python
import numpy as np

rng = np.random.default_rng(7)
n = 12
x = rng.normal(100, 15, n)

def helmert(n):
    """Base orthonormée dont le 1er vecteur est 1/√n et les autres engendrent son orthogonal."""
    O = np.zeros((n, n))
    O[0] = 1 / np.sqrt(n)
    for k in range(1, n):
        O[k, :k] = 1 / np.sqrt(k * (k + 1))
        O[k, k] = -k / np.sqrt(k * (k + 1))
    return O

O = helmert(n)
print("orthogonale :", np.allclose(O @ O.T, np.eye(n)))

c = O @ x                                    # coordonnées de x dans la base adaptée
print("1re coordonnée = √n·moyenne :", np.allclose(c[0], np.sqrt(n) * x.mean()))
print("reste = dispersion          :", np.allclose(c[1:] @ c[1:], ((x - x.mean())**2).sum()))
print("Parseval :", np.allclose(c @ c, x @ x))
```

**Gardez cette fonction `helmert`** : c'est celle qu'utilise le
[module 11 du cours de statistique](../../semestre2/statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md).

### S6.2 — Une isométrie conserve tout

```python
u, v = rng.normal(size=n), rng.normal(size=n)

print("produits scalaires :", np.allclose((O @ u) @ (O @ v), u @ v))
print("normes             :", np.allclose(np.linalg.norm(O @ u), np.linalg.norm(u)))
print("déterminant        :", round(abs(np.linalg.det(O)), 12))   # 1
```

### S6.3 — Gram–Schmidt, et la BON n'est pas unique

```python
A = np.column_stack([np.ones(n), np.arange(1., n + 1.)])   # base de F = Vect(1, t)
Q, _ = np.linalg.qr(A)                                     # Gram-Schmidt (via QR)

print("orthonormée :", np.allclose(Q.T @ Q, np.eye(2)))
print("engendre F  :", np.allclose(Q @ Q.T @ A, A))

# deux BON différentes, même projecteur
theta = 0.7
R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
Q2 = Q @ R
print("Q2 ≠ Q :", not np.allclose(Q, Q2))
print("même projecteur :", np.allclose(Q @ Q.T, Q2 @ Q2.T))
```

**La base est arbitraire, le sous-espace ne l'est pas.** Toute BON de $F$ donne le même
projecteur, donc la même figure — c'est ce qui rend le choix « la base la plus commode »
légitime.

---

## 6.6 Exercices

**E6.1.** Vérifier que la base de Helmert du § 6.4 est bien orthonormée, et démontrer à la main
les deux identités qui la suivent.

**E6.2.** Orthonormaliser $(1,1,1)$ puis $(1,0,0)$ par **Gram–Schmidt**, et comparer le résultat
à la base de Helmert du § 6.4. *Sont-elles identiques ? Pourquoi la BON adaptée à
$\text{Vect}(\mathbf 1)$ n'est-elle pas unique — et pourquoi cela n'a-t-il aucune importance ?*

**E6.3.** Montrer que $OO^{\top}=I_n\iff O^{\top}O=I_n$, et en déduire que les **colonnes** d'une
matrice orthogonale forment aussi une BON.

**E6.4.** Montrer que le déterminant d'une matrice orthogonale vaut $\pm1$. *Donner un exemple de
chaque cas en dimension 2 et l'interpréter (rotation / symétrie).*

**E6.5.** Soit $P$ le projecteur sur $F$ et $O$ une BON adaptée. Écrire la matrice de $P$ dans
cette base. *(Réponse : un bloc diagonal de $d$ uns suivi de $n-d$ zéros.) Retrouver ainsi
$\operatorname{tr}(P)=\dim F$ du § 4.4 — sans calcul.*

---

## 6.7 À retenir

- **BON** : $\langle e_j,e_k\rangle=\delta_{jk}$ ; coordonnées = produits scalaires ;
  **Parseval** $\|x\|^2=\sum_j\langle x,e_j\rangle^2$.
- **Matrice orthogonale $\iff$ isométrie** : longueurs, angles et orthogonalité conservés.
- **Gram–Schmidt** : une BON adaptée à $F\oplus F^\perp$ existe toujours ; dans cette base, les
  projections sont des blocs de coordonnées.
- **Helmert** : une coordonnée pour la moyenne, $n-1$ pour la dispersion.
- La BON n'est pas unique — **le sous-espace et le projecteur, si**.

---

⬅️ [Module 5 — Supplémentaire orthogonal et dimension](05-supplementaire-orthogonal-et-dimension.md) ·
➡️ [Module 7 — Le dictionnaire géométrique des statistiques](07-dictionnaire-geometrique-des-statistiques.md) ·
🏠 [Sommaire](README.md)
