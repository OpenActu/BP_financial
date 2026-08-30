# Module 3 — Orthogonalité et théorème de Pythagore

**Durée : 45 min.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) et
[2](02-cauchy-schwarz-et-angle.md).

> **La question traitée.** Que se passe-t-il quand le terme croisé $2\langle u,v\rangle$ de  l'identité de développement s'annule ?

**Ce qui est en jeu.** Toute « décomposition de la variance » de la statistique — somme des
carrés totale = expliquée + résiduelle — est une instance de ce module, et d'aucun autre.

---

## 3.1 Définition

> **Définition.** $u\perp v \iff \langle u,v\rangle=0$.

Dans le vocabulaire du [module 2](02-cauchy-schwarz-et-angle.md), c'est le cas $\theta=90°$. Le
vecteur nul est orthogonal à tout le monde ; c'est le seul vecteur orthogonal à lui-même (par la
propriété « définie positive » du § 1.1).

**Orthogonalité à un sous-espace.** $u\perp F$ signifie $u\perp f$ pour **tout** $f\in F$. Par
bilinéarité, il suffit de le vérifier sur une famille génératrice de $F$ : c'est ce qui rend la
vérification praticable.

---

## 3.2 Le théorème

> **Théorème de Pythagore.**
> $$u\perp v\quad\Longleftrightarrow\quad \|u+v\|^2=\|u\|^2+\|v\|^2$$

**Démonstration.** Immédiate par développement (§ 1.2) :
$\|u+v\|^2=\|u\|^2+2\langle u,v\rangle+\|v\|^2$. Le terme croisé disparaît si et seulement si
$\langle u,v\rangle=0$. $\blacksquare$

Notez bien que dans $\mathbb R^n$ c'est une **équivalence**, pas une simple implication : la
réciproque du Pythagore scolaire est ici gratuite.

**Généralisation à une famille orthogonale.** Si $w_1,\dots,w_k$ sont deux à deux orthogonaux :

$$\Big\|\sum_{j=1}^k w_j\Big\|^2=\sum_{j=1}^k\|w_j\|^2$$

Démonstration par récurrence sur $k$ : la somme partielle $\sum_{j<k}w_j$ est orthogonale à $w_k$
par bilinéarité, et on applique le théorème. $\blacksquare$

---

## 3.3 Familles orthogonales et indépendance linéaire

> **Proposition.** Une famille orthogonale de vecteurs **non nuls** est libre.

**Démonstration.** Si $\sum_j \lambda_j w_j=0$, le produit scalaire des deux membres avec $w_k$
donne $\lambda_k\|w_k\|^2=0$ — tous les autres termes s'annulent par orthogonalité — donc
$\lambda_k=0$. $\blacksquare$

> 🔑 **L'orthogonalité est une forme forte, et vérifiable en un produit scalaire, de
> l'indépendance linéaire.** C'est ce qui la rend commode : prouver qu'une famille est libre
> demande en général de résoudre un système ; ici, il suffit de $k(k-1)/2$ produits scalaires
> nuls.

---

## 3.4 Ce que le théorème devient sur des données

> 🔑 **Toute « décomposition de la variance » est un Pythagore.** Somme des carrés totale = somme
> des carrés expliquée + somme des carrés résiduelle : ce n'est pas une identité algébrique
> fortuite, c'est Pythagore appliqué à une décomposition orthogonale.

Deux occurrences que vous rencontrerez :

| Identité statistique | Ce qu'elle est réellement |
|---|---|
| König–Huygens $\sum_i(x_i-\bar x)^2=\sum_i x_i^2-n\bar x^2$ | Pythagore sur $x=\bar x\mathbf 1+\tilde x$ — [module 5](05-supplementaire-orthogonal-et-dimension.md) |
| Table d'ANOVA : $SC_{\text{tot}}=SC_{\text{exp}}+SC_{\text{rés}}$ | Pythagore sur $y=P_F(y)+(y-P_F(y))$ — [module 4](04-projection-orthogonale.md) |

---

## 3.5 Simulation

### S3.1 — Pythagore, dans les deux sens

```python
import numpy as np

rng = np.random.default_rng(3)
n = 8
u = rng.normal(size=n)

# construire un v orthogonal à u : retirer à un vecteur quelconque sa composante sur u
v0 = rng.normal(size=n)
v = v0 - (v0 @ u) / (u @ u) * u

print("orthogonaux :", abs(u @ v) < 1e-12)
print("Pythagore   :", np.allclose(np.linalg.norm(u + v)**2,
                                   np.linalg.norm(u)**2 + np.linalg.norm(v)**2))

# le sens réciproque : si Pythagore tient, l'orthogonalité suit
ecart = np.linalg.norm(u + v0)**2 - np.linalg.norm(u)**2 - np.linalg.norm(v0)**2
print(f"avec v0 non orthogonal : écart = {ecart:.3f}, et 2<u,v0> = {2 * u @ v0:.3f}")

# famille orthogonale à k termes
w = np.linalg.qr(rng.normal(size=(n, 4)))[0].T * np.array([1., 2., 3., 4.])[:, None]
print("Pythagore à 4 termes :", np.allclose(np.linalg.norm(w.sum(0))**2,
                                            (np.linalg.norm(w, axis=1)**2).sum()))
```

La ligne centrale est la plus parlante : **l'écart à Pythagore vaut exactement le terme
croisé**. Le théorème ne dit rien d'autre.

---

## 3.6 Exercices

**E3.1.** Montrer que si $u\perp v$ alors $\|u-v\|=\|u+v\|$. *Interpréter avec les diagonales
d'un parallélogramme (voir E1.2).*

**E3.2.** Soit $\mathbf 1=(1,\dots,1)$. Caractériser les vecteurs $u$ tels que $u\perp\mathbf 1$.
*(Réponse : $\sum_i u_i=0$.)* **C'est l'ensemble le plus important de tout le cours** — voir le
[module 5](05-supplementaire-orthogonal-et-dimension.md).

**E3.3.** Retrouver König–Huygens $\sum_i(x_i-\bar x)^2=\sum_i x_i^2-n\bar x^2$ **par Pythagore
seul**, sans développer le carré. *(Piste : admettre provisoirement que $x-\bar x\mathbf 1$ est
orthogonal à $\bar x\mathbf 1$ — l'exercice E3.2 le donne.) Comparer la longueur des deux
démonstrations.*

**E3.4.** Montrer qu'une famille orthogonale de $\mathbb R^n$ comporte au plus $n$ vecteurs non
nuls. *Quel résultat du § 3.3 utilise-t-on ?*

**E3.5.** Deux vecteurs sont orthogonaux ; leur somme peut-elle être de norme inférieure à
chacun d'eux ? *Justifier par le théorème, puis par un dessin en dimension 2.*

---

## 3.7 À retenir

- **$u\perp v\iff\langle u,v\rangle=0$** ; orthogonal à $F$ = orthogonal à une famille
  génératrice de $F$.
- **Pythagore $\|u+v\|^2=\|u\|^2+\|v\|^2\iff u\perp v$** — une **équivalence**, et sa
  démonstration tient en une ligne de développement.
- **L'écart à Pythagore est le terme croisé** $2\langle u,v\rangle$.
- **Une famille orthogonale de vecteurs non nuls est libre.**
- Toute décomposition de la variance en statistique est une instance de ce théorème.

---

⬅️ [Module 2 — Cauchy–Schwarz et l'angle](02-cauchy-schwarz-et-angle.md) ·
➡️ [Module 4 — La projection orthogonale](04-projection-orthogonale.md) ·
🏠 [Sommaire](README.md)
