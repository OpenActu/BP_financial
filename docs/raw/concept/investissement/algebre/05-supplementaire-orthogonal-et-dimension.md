# Module 5 — Supplémentaire orthogonal, dimension, degrés de liberté ⭐

**Durée : 1 h.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) à
[4](04-projection-orthogonale.md). ⭐ **Le module qui donne son sens au « $n-1$ ».**

> **La question traitée.** Dans $\mathbb R^n$, soit $\mathbf 1=(1,\dots,1)$ et
> $x=(x_1,\dots,x_n)$. Montrer que la projection orthogonale de $x$ sur $\text{Vect}(\mathbf 1)$
> est $\bar x\,\mathbf 1$ ; en déduire que le vecteur des écarts $(x_i-\bar x)_i$ appartient à
> $\text{Vect}(\mathbf 1)^\perp$ ; donner la dimension de ce sous-espace.

**Ce qui est en jeu.** La réponse au troisième point est $n-1$ — et c'est la réponse à la
question *« pourquoi divise-t-on par $n-1$ ? »*. Ce n'est pas une convention de calcul mais une
**contrainte géométrique**. À la fin de ce module, ce doit être une évidence visuelle.

---

## 5.1 Le supplémentaire orthogonal

> **Définition.** $F^\perp=\{u\in\mathbb R^n:\ \langle u,f\rangle=0\ \ \forall f\in F\}$.

> **Théorème.** Pour tout sous-espace $F$ de $\mathbb R^n$ :
> $$\mathbb R^n=F\oplus F^\perp,\qquad \dim F^\perp=n-\dim F,\qquad (F^\perp)^\perp=F$$
> et tout $x$ s'écrit de **manière unique** $x=P_F(x)+P_{F^\perp}(x)$, avec
> $$\|x\|^2=\|P_F(x)\|^2+\|P_{F^\perp}(x)\|^2$$

La dernière égalité est le [Pythagore du module 3](03-orthogonalite-et-pythagore.md), appliqué à
la décomposition ci-dessus. L'existence de la décomposition est la
[projection du module 4](04-projection-orthogonale.md) ; l'unicité vient de
$F\cap F^\perp=\{0\}$, conséquence immédiate du caractère défini positif du produit scalaire.

> 🔑 **Décomposer, c'est répartir des dimensions.** $n=\dim F+\dim F^\perp$ : chaque dimension
> de $\mathbb R^n$ est affectée à l'un des deux morceaux, jamais aux deux. C'est cette
> comptabilité — et rien d'autre — que les statisticiens appellent « degrés de liberté ».

---

## 5.2 Le cas décisif : $F=\text{Vect}(\mathbf 1)$

### 1. La projection sur $\text{Vect}(\mathbf 1)$ est $\bar x\,\mathbf 1$

Appliquons la formule du § 4.1 avec $u=\mathbf 1$. Deux calculs :

$$\langle x,\mathbf 1\rangle=\sum_i x_i=n\bar x
\qquad\text{et}\qquad \|\mathbf 1\|^2=\langle\mathbf 1,\mathbf 1\rangle=n$$

D'où

$$p(x)=\frac{\langle x,\mathbf 1\rangle}{\|\mathbf 1\|^2}\,\mathbf 1=\frac{n\bar x}{n}\,\mathbf 1
=\boxed{\;\bar x\,\mathbf 1\;}$$

> 🔑 **La moyenne n'est pas un résumé arbitraire des données : c'est l'ombre de $x$ sur la
> direction $\mathbf 1$.** Autrement dit, c'est le vecteur constant le plus proche de $x$ — le
> point le plus proche parmi tous les « tous égaux à $c$ ». Ce que le § 4.2 formalise :
> $\bar x = \arg\min_c \sum_i (x_i-c)^2$.

### 2. Le vecteur des écarts est dans $\text{Vect}(\mathbf 1)^\perp$

Le vecteur des écarts est exactement le **résidu** de la projection :

$$\tilde x = x-p(x)=x-\bar x\,\mathbf 1=(x_i-\bar x)_i$$

Et un résidu de projection orthogonale est orthogonal au sous-espace, par construction. Le calcul
direct le confirme :

$$\langle \tilde x,\mathbf 1\rangle=\sum_i (x_i-\bar x)=\sum_i x_i-n\bar x=n\bar x-n\bar x=0$$

> ⚠️ **Retenez cette identité $\sum_i(x_i-\bar x)=0$ pour ce qu'elle est** : non pas une astuce de
> calcul, mais **une contrainte linéaire** que les écarts subissent. Elle dit que le vecteur des
> écarts n'est pas libre dans $\mathbb R^n$ : il est confiné à un hyperplan.

### 3. La dimension : $n-1$

$\text{Vect}(\mathbf 1)^\perp=\{u\in\mathbb R^n:\;\sum_i u_i=0\}$ est le noyau de la forme
linéaire **non nulle** $u\mapsto\sum_i u_i$. Le théorème du rang donne

$$\dim \text{Vect}(\mathbf 1)^\perp = n-1$$

C'est le cas particulier $\dim F=1$ de la formule générale $\dim F^\perp=n-\dim F$ du § 5.1.

---

## 5.3 La figure complète

$$\mathbb R^n=\underbrace{\text{Vect}(\mathbf 1)}_{\dim\,1}\;\oplus\;\underbrace{\text{Vect}(\mathbf 1)^\perp}_{\dim\,n-1},
\qquad x=\underbrace{\bar x\,\mathbf 1}_{\text{la moyenne}}+\underbrace{\tilde x}_{\text{la dispersion}}$$

Et Pythagore relie les deux morceaux :

$$\|x\|^2=\|\bar x\,\mathbf 1\|^2+\|\tilde x\|^2
\qquad\text{soit}\qquad \sum_i x_i^2=n\bar x^2+\sum_i(x_i-\bar x)^2$$

On reconnaît la formule de **König–Huygens** — qui n'est donc que le théorème de Pythagore dans
la bonne base.

> 🔑 **Voici la réponse à « pourquoi $n-1$ ? ».** L'information sur la **dispersion** vit dans un
> sous-espace de dimension $n-1$, pas $n$ : une dimension a été consommée par la moyenne. Le
> nombre de degrés de liberté n'est **pas** un compteur de paramètres estimés que l'on
> retrancherait par convention — c'est **la dimension du sous-espace dans lequel le vecteur des
> écarts est contraint de vivre**.

**Le contrôle décisif.** Si l'on vous impose $n=5$ écarts dont la somme doit être nulle, combien
en choisissez-vous librement ? Quatre — le cinquième est déterminé. C'est $n-1$, et c'est tout ce
que l'expression « degrés de liberté » a jamais voulu dire.

---

## 5.4 La matrice de centrage

Dans le cas $F=\text{Vect}(\mathbf 1)$, les deux projecteurs s'écrivent explicitement. Avec
$J=\mathbf 1\mathbf 1^{\top}$ la matrice remplie de 1 :

$$P_{\text{Vect}(\mathbf 1)}=\frac{1}{n}J
\qquad\text{et}\qquad
M=I_n-\frac{1}{n}J$$

$M$ est la **matrice de centrage** : $Mx$ n'est autre que le vecteur des écarts $\tilde x$.
Vérifiez ces trois points — c'est l'exercice E5.4 :

| Propriété | Lecture |
|---|---|
| $M^{\top}=M$ | projecteur **orthogonal** |
| $M^2=M$ | centrer deux fois = centrer une fois |
| $\operatorname{tr}(M)=n-1$ | rang $n-1$ : **les degrés de liberté se lisent sur la trace** |

---

## 5.5 Généralisation : quand $\dim F=2$

Rien dans ce module n'est propre à $\dim F=1$. Prenons $t=(1,2,\dots,n)$ et
$F=\text{Vect}(\mathbf 1,\,t)$ — le sous-espace des droites $y=a+bt$ :

$$\dim F=2\quad\text{(dès que } n\ge 2\text{)}\qquad\Longrightarrow\qquad \dim F^\perp=n-2$$

C'est **la même figure**, avec deux dimensions consommées au lieu d'une : la constante et la
pente. Le $n-2$ d'une régression linéaire simple n'a pas d'autre origine.

| $F$ | $\dim F$ | $\dim F^\perp$ | Modèle correspondant |
|---|---|---|---|
| $\text{Vect}(\mathbf 1)$ | 1 | $n-1$ | moyenne seule |
| $\text{Vect}(\mathbf 1,t)$ | 2 | $n-2$ | droite de régression |
| $p$ prédicteurs + constante | $p+1$ | $n-p-1$ | régression multiple |

---

## 5.6 Simulations

### S5.1 — La projection sur $\text{Vect}(\mathbf 1)$ et Pythagore

```python
import numpy as np

rng = np.random.default_rng(7)
n = 12
x = rng.normal(100, 15, n)
un = np.ones(n)

p = (x @ un) / (un @ un) * un                # projection
r = x - p                                    # résidu = vecteur des écarts

print("projection = moyenne × 1 :", np.allclose(p, x.mean() * un))
print("résidu orthogonal à 1    :", abs(r @ un) < 1e-10)
print("somme des écarts nulle   :", abs(r.sum()) < 1e-10)

print("Pythagore :", np.allclose(x @ x, p @ p + r @ r))
print(f"   ‖x‖² = {x @ x:.2f} = {p @ p:.2f} (moyenne) + {r @ r:.2f} (dispersion)")
```

La dernière ligne est König–Huygens, lue comme un Pythagore. **Refaites-la avec des données
centrées** : le premier terme s'annule, et toute la norme passe dans la dispersion.

### S5.2 — La matrice de centrage et la trace qui compte les degrés de liberté

```python
M = np.eye(n) - np.ones((n, n)) / n

print("symétrique  :", np.allclose(M, M.T))
print("idempotente :", np.allclose(M @ M, M))
print("centre bien :", np.allclose(M @ x, x - x.mean()))
print(f"trace = {np.trace(M):.4f}   rang = {np.linalg.matrix_rank(M)}   (n-1 = {n-1})")

vp = np.round(np.linalg.eigvalsh(M), 10)
print("valeurs propres :", np.unique(vp, return_counts=True))   # 0 (×1) et 1 (×n-1)
```

**Le spectre est la démonstration visuelle** : une valeur propre 0 — la direction $\mathbf 1$,
écrasée — et $n-1$ valeurs propres 1 — l'hyperplan, laissé intact. Les degrés de liberté sont là,
littéralement comptés.

### S5.3 — Le passage à $\dim F=2$

```python
t = np.arange(1., n + 1.)
A = np.column_stack([un, t])                 # base (non orthonormée) de F = Vect(1, t)
P = A @ np.linalg.inv(A.T @ A) @ A.T
Q = np.eye(n) - P                            # projecteur sur F⟂

print(f"tr(P) = {np.trace(P):.4f}  (dim F   = 2)")
print(f"tr(Q) = {np.trace(Q):.4f}  (dim F⟂ = n-2 = {n-2})")
print("les résidus de régression sont orthogonaux à 1 ET à t :",
      np.allclose(A.T @ (Q @ x), 0))
```

Les résidus d'une régression subissent **deux** contraintes linéaires, pas une : d'où $n-2$.

---

## 5.7 Exercices

**E5.1.** Montrer que $F\cap F^\perp=\{0\}$. *Quelle propriété du § 1.1 est en jeu ?*

**E5.2.** Montrer que $F\subset G\Rightarrow G^\perp\subset F^\perp$. *Illustrer avec
$F=\text{Vect}(\mathbf 1)$ et $G=\text{Vect}(\mathbf 1,t)$, et relier aux dimensions $n-1$ et
$n-2$.*

**E5.3.** Refaire le § 5.2 avec $n=5$ et $x=(2,4,4,4,6)$ : calculer $p(x)$, $\tilde x$, vérifier
$\sum_i\tilde x_i=0$ et König–Huygens numériquement.

**E5.4.** Vérifier à la main que $M=I_n-\frac1nJ$ est symétrique, idempotente, et que
$\operatorname{tr}(M)=n-1$. En déduire son rang **sans calculer de déterminant**. *(Piste : pour
un projecteur, rang = trace — voir § 4.4.)*

**E5.5.** Soit $t=(1,2,\dots,n)$ et $F=\text{Vect}(\mathbf 1,\,t)$.
1. Montrer que $\dim F=2$ dès que $n\ge 2$.
2. En déduire $\dim F^\perp$.
3. Quel nombre de degrés de liberté un test sur la pente d'une régression simple doit-il donc
   utiliser ? *(Réponse au module 7 du
   [cours sur la loi de Student](../statistique/loi-de-student/07-student-en-regression.md).)*

**E5.6.** Que devient $\dim F^\perp$ si l'on ajoute à $F$ un vecteur **déjà dans $F$** ? *En quoi
cela justifie-t-il que « degrés de liberté » soit une dimension et non un compteur de
paramètres ?*

---

## 5.8 À retenir

- **$\mathbb R^n=F\oplus F^\perp$**, $\dim F^\perp=n-\dim F$, décomposition unique et Pythagore.
- **Sur $\text{Vect}(\mathbf 1)$** : $p(x)=\bar x\,\mathbf 1$, résidu = vecteur des écarts,
  contraint par $\sum_i(x_i-\bar x)=0$.
- **König–Huygens est un Pythagore** dans la décomposition moyenne / dispersion.
- ⭐ **$\dim\text{Vect}(\mathbf 1)^\perp=n-1$ : voilà les degrés de liberté.** Une **dimension**,
  pas une convention.
- **Matrice de centrage** $M=I_n-\frac1nJ$ : symétrique, idempotente,
  $\operatorname{tr}(M)=n-1$.
- Avec $\dim F=2$ (constante **et** pente), la même figure donne $n-2$.

---

⬅️ [Module 4 — La projection orthogonale](04-projection-orthogonale.md) ·
➡️ [Module 6 — Bases orthonormées et isométries](06-bases-orthonormees-et-isometries.md) ·
🏠 [Sommaire](README.md)
