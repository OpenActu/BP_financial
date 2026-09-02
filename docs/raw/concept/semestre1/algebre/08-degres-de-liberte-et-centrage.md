# Module 8 — Degrés de liberté : le cas $\text{Vect}(\mathbf 1)$ ⭐

**Durée : 45 min.** Prérequis : modules [1](01-espace-vectoriel.md) à [7](07-supplementaire-orthogonal-et-dimension.md). ⭐ **Le module qui donne son sens au « $n-1$ ».**

> **La question traitée.** Dans $\mathbb R^n$, soit $\mathbf 1=(1,\dots,1)$ et $x=(x_1,\dots,x_n)$. Montrer que la projection orthogonale de $x$ sur $\text{Vect}(\mathbf 1)$ est $\bar x\,\mathbf 1$ ; en déduire que le vecteur des écarts $(x_i-\bar x)_i$ appartient à
> $\text{Vect}(\mathbf 1)^\perp$ ; donner la dimension de ce sous-espace.

**Ce qui est en jeu.** La réponse au troisième point est $n-1$ — et c'est la réponse à la question *« pourquoi divise-t-on par $n-1$ ? »*. Ce n'est pas une convention de calcul mais une **contrainte géométrique**, celle du [§ 7.3](07-supplementaire-orthogonal-et-dimension.md) appliquée à une seule direction. À la fin de ce module, ce doit être une évidence visuelle.

---

## 8.1 Le cas décisif : $F=\text{Vect}(\mathbf 1)$

### 1. La projection sur $\text{Vect}(\mathbf 1)$ est $\bar x\,\mathbf 1$

Appliquons la formule du § 6.2 avec $u=\mathbf 1$. Deux calculs :
$$\langle x,\mathbf 1\rangle=\sum_i x_i=n\bar x
\qquad\text{et}\qquad \|\mathbf 1\|^2=\langle\mathbf 1,\mathbf 1\rangle=n$$
D'où
$$p(x)=\frac{\langle x,\mathbf 1\rangle}{\|\mathbf 1\|^2}\,\mathbf 1=\frac{n\bar x}{n}\,\mathbf 1
=\boxed{\;\bar x\,\mathbf 1\;}$$
> 🔑 **La moyenne n'est pas un résumé arbitraire des données : c'est l'ombre de $x$ sur la
> direction $\mathbf 1$.** Autrement dit, c'est le vecteur constant le plus proche de $x$ — le point le plus proche parmi tous les « tous égaux à $c$ ». Ce que le § 6.3 formalise : $\bar x = \arg\min_c \sum_i (x_i-c)^2$.

### 2. Le vecteur des écarts est dans $\text{Vect}(\mathbf 1)^\perp$

Le vecteur des écarts est exactement le **résidu** de la projection :
$$\tilde x = x-p(x)=x-\bar x\,\mathbf 1=(x_i-\bar x)_i$$
Et un résidu de projection orthogonale est orthogonal au sous-espace, par construction. Le calcul
direct le confirme :

$$\langle \tilde x,\mathbf 1\rangle=\sum_i (x_i-\bar x)=\sum_i x_i-n\bar x=n\bar x-n\bar x=0$$

> ⚠️ **Retenez cette identité $\sum_i(x_i-\bar x)=0$ pour ce qu'elle est** : non pas une astuce de calcul, mais **une contrainte linéaire** que les écarts subissent. Elle dit que le vecteur des écarts n'est pas libre dans $\mathbb R^n$ : il est confiné à un **hyperplan** ([§ 7.3](07-supplementaire-orthogonal-et-dimension.md)) — celui d'équation $\sum_i u_i=0$.

### 3. La dimension : $n-1$

$\text{Vect}(\mathbf 1)^\perp=\{u\in\mathbb R^n:\;\sum_i u_i=0\}$ est le noyau de la forme linéaire **non nulle** $u\mapsto\sum_i u_i$ — c'est donc un hyperplan au sens du [§ 7.3](07-supplementaire-orthogonal-et-dimension.md), avec $a=\mathbf 1$. Le théorème du rang ([§ 7.2](07-supplementaire-orthogonal-et-dimension.md)) donne
$$\dim \text{Vect}(\mathbf 1)^\perp = n-1$$
C'est le cas particulier $\dim F=1$ de la formule générale $\dim F^\perp=n-\dim F$ du [§ 7.1](07-supplementaire-orthogonal-et-dimension.md). Cet hyperplan — celui des vecteurs de somme nulle, donc des vecteurs centrés — est noté $H$ dans toute la suite du cours ([module 11](11-covariance-et-produit-scalaire.md)) :
$$H=\text{Vect}(\mathbf 1)^\perp=\Bigl\{u\in\mathbb R^n:\ \sum_i u_i=0\Bigr\},\qquad \dim H=n-1$$

---

## 8.2 La figure complète
$$\mathbb R^n=\underbrace{\text{Vect}(\mathbf 1)}_{\dim\,1}\;\oplus\;\underbrace{\text{Vect}(\mathbf 1)^\perp}_{\dim\,n-1},
\qquad x=\underbrace{\bar x\,\mathbf 1}_{\text{la moyenne}}+\underbrace{\tilde x}_{\text{la dispersion}}$$
Et Pythagore relie les deux morceaux :
$$\|x\|^2=\|\bar x\,\mathbf 1\|^2+\|\tilde x\|^2
\qquad\text{soit}\qquad \sum_i x_i^2=n\bar x^2+\sum_i(x_i-\bar x)^2$$
On reconnaît la formule de **König–Huygens** — qui n'est donc que le théorème de Pythagore dans
la bonne base.

> 🔑 **Voici la réponse à « pourquoi $n-1$ ? ».** L'information sur la **dispersion** vit dans un sous-espace de dimension $n-1$, pas $n$ : une dimension a été consommée par la moyenne. Le nombre de degrés de liberté n'est **pas** un compteur de paramètres estimés que l'on retrancherait par convention — c'est **la dimension du sous-espace dans lequel le vecteur des écarts est contraint de vivre**.

**Le contrôle décisif.** Si l'on vous impose $n=5$ écarts dont la somme doit être nulle, combien en choisissez-vous librement ? Quatre — le cinquième est déterminé. C'est $n-1$, et c'est tout ce que l'expression « degrés de liberté » a jamais voulu dire.

---

## 8.3 La matrice de centrage

Dans le cas $F=\text{Vect}(\mathbf 1)$, les deux projecteurs s'écrivent explicitement. Avec $J=\mathbf 1\mathbf 1^{\top}$ la matrice remplie de 1 :
$$P_{\text{Vect}(\mathbf 1)}=\frac{1}{n}J
\qquad\text{et}\qquad
M=I_n-\frac{1}{n}J$$
$M$ est la **matrice de centrage** : $Mx$ n'est autre que le vecteur des écarts $\tilde x$. Vérifiez ces trois points — c'est l'exercice E8.2 :

| Propriété                  | Lecture                                                       |
| -------------------------- | ------------------------------------------------------------- |
| $M^{\top}=M$               | projecteur **orthogonal**                                     |
| $M^2=M$                    | centrer deux fois = centrer une fois                          |
| $\operatorname{tr}(M)=n-1$ | rang $n-1$ : **les degrés de liberté se lisent sur la trace** |

---

## 8.4 Généralisation : quand $\dim F=2$

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

## 8.5 Simulations

### S8.1 — La projection sur $\text{Vect}(\mathbf 1)$ et Pythagore

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

### S8.2 — La matrice de centrage et la trace qui compte les degrés de liberté

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

### S8.3 — Le passage à $\dim F=2$

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

## 8.6 Exercices

**E8.1.** Refaire le § 8.1 avec $n=5$ et $x=(2,4,4,4,6)$ : calculer $p(x)$, $\tilde x$, vérifier
$\sum_i\tilde x_i=0$ et König–Huygens numériquement.

**E8.2.** Vérifier à la main que $M=I_n-\frac1nJ$ est symétrique, idempotente, et que
$\operatorname{tr}(M)=n-1$. En déduire son rang **sans calculer de déterminant**. *(Piste : pour
un projecteur, rang = trace — voir § 6.5.)*

**E8.3.** Déterminer $\ker M$ et $\operatorname{im}M$, puis vérifier le théorème du rang
([§ 7.2](07-supplementaire-orthogonal-et-dimension.md)) sur $M$. *Pourquoi
$\ker M=\operatorname{im}(I_n-M)$ ? Que devient cette égalité pour un projecteur orthogonal
quelconque ?*

**E8.4.** Soit $t=(1,2,\dots,n)$ et $F=\text{Vect}(\mathbf 1,\,t)$.
1. Montrer que $\dim F=2$ dès que $n\ge 2$.
2. En déduire $\dim F^\perp$.
3. Quel nombre de degrés de liberté un test sur la pente d'une régression simple doit-il donc
   utiliser ? *(Réponse au module 7 du
   [cours sur la loi de Student](../../semestre3/statistique/loi-de-student/07-student-en-regression.md).)*

**E8.5 — orientée finance.** `import_societe.py` calcule `VAR_20` et `VAR_120` en variance de
**population** (`ddof=0`, diviseur $n$). Recalculer les deux colonnes avec le diviseur $n-1$ sur
un CSV de `docs/raw/data/quotes/`. *De quel facteur diffèrent-elles ? Laquelle des deux fenêtres
est la plus sensible au choix du diviseur, et pourquoi le script a-t-il raison de diviser par $n$
pour une quantité purement descriptive ?*

---

## 8.7 À retenir

- **Sur $\text{Vect}(\mathbf 1)$** : $p(x)=\bar x\,\mathbf 1$, résidu = vecteur des écarts,
  contraint par $\sum_i(x_i-\bar x)=0$.
- **König–Huygens est un Pythagore** dans la décomposition moyenne / dispersion.
- ⭐ **$\dim\text{Vect}(\mathbf 1)^\perp=n-1$ : voilà les degrés de liberté.** Une **dimension**,
  pas une convention.
- **Matrice de centrage** $M=I_n-\frac1nJ$ : symétrique, idempotente,
  $\operatorname{tr}(M)=n-1$ ; noyau $\text{Vect}(\mathbf 1)$, image $H$.
- Avec $\dim F=2$ (constante **et** pente), la même figure donne $n-2$.

---

⬅️ [Module 7 — Supplémentaire orthogonal, noyau, rang](07-supplementaire-orthogonal-et-dimension.md) ·
➡️ [Module 9 — Bases orthonormées et isométries](09-bases-orthonormees-et-isometries.md) ·
🏠 [Sommaire](README.md)
