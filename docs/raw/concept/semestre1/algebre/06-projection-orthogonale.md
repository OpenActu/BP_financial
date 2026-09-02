# Module 6 — La projection orthogonale ⭐

**Durée : 1 h.** Prérequis : modules [1](01-espace-vectoriel.md) à [5](05-orthogonalite-et-pythagore.md). ⭐ **Module central du cours.**

> **La question traitée.** Étant donné un vecteur $x$ et un sous-espace $F$, quel élément de $F$
> ressemble le plus à $x$ ?

**Ce qui est en jeu.** La réponse — la projection orthogonale — **est** la méthode des moindres
carrés. Tout le calcul différentiel d'une régression linéaire (annuler des dérivées partielles)
n'est qu'une façon coûteuse de retrouver la figure de ce module.

---

## 6.1 Ce que le sous-espace apporte à la question

La question du module parle d'un **sous-espace** $F$. Ce n'est pas un mot de décor : c'est l'hypothèse qui rend la question bien posée, et tout ce qui suit s'appuie sur elle.

> 📐 **Rappel du [module 4](04-sous-espaces-et-familles-generatrices.md).** $F\subseteq\mathbb R^n$ est un **sous-espace** s'il est non vide et **stable par combinaison linéaire** — il contient donc $0$. Et $\text{Vect}(u_1,\dots,u_d)$, l'ensemble de toutes les combinaisons linéaires des $u_j$, est le plus petit sous-espace qui les contienne. Les sous-espaces employés ici sont ceux du [§ 4.4](04-sous-espaces-et-familles-generatrices.md) : $\text{Vect}(\mathbf 1)$ pour la moyenne, $\text{Vect}(\mathbf 1,t)$ pour la droite ajustée, $\text{Vect}(\text{colonnes de }A)$ pour la régression multiple.

**Et de la stabilité, on n'utilisera rien d'autre.** C'est la seule propriété de $F$ dont ce module se sert : au § 6.3, elle sert à affirmer que $p(x)-y$ appartient encore à $F$, et c'est tout.

**Le cas $d=1$ — la droite.** $\text{Vect}(u)=\{\lambda u\ :\ \lambda\in\mathbb R\}$ est la **droite** passant par l'origine et dirigée par $u$ : c'est le $D$ du § 6.2. L'hypothèse $u\ne 0$ y est indispensable, et pour une raison de géométrie avant d'être de calcul — $\text{Vect}(0)=\{0\}$ est un sous-espace parfaitement légitime, mais réduit à un point : ce n'est pas une droite, et le projeté d'un $x$ dessus vaut $0$ sans qu'aucune direction ne soit en jeu.

**Dimension.** Le nombre $d$ de générateurs n'est pas la dimension de $\text{Vect}(u_1,\dots,u_d)$ : il la majore ([§ 4.3](04-sous-espaces-et-familles-generatrices.md)). Les deux coïncident exactement quand la famille est **libre** — et le [§ 5.3](05-orthogonalite-et-pythagore.md) donne un critère commode pour s'en assurer : une famille orthogonale de vecteurs non nuls est libre. C'est ce que le § 6.4 exploite en travaillant dans une base orthonormée.

> 🔑 **C'est la stabilité qui garantit une réponse.** Sur une partie quelconque de $\mathbb R^n$ — une sphère, un segment, un ensemble fini — « l'élément le plus proche de $x$ » peut ne pas exister, ou en exister plusieurs. Le § 6.3 montre que sur un sous-espace il existe et qu'il est unique, et la démonstration n'invoque rien d'autre que la stabilité et Pythagore.

---

## 6.2 Projection sur une droite

> **Proposition.** Soit $u\ne 0$ et $D=\text{Vect}(u)$. La projection orthogonale de $x$ sur $D$ est
> $$p(x)=\frac{\langle x,u\rangle}{\|u\|^2}\,u$$

**Démonstration.** Cherchons $p(x)=\lambda u$ tel que le résidu $x-\lambda u$ soit orthogonal à $u$ :
$$\langle x-\lambda u,\;u\rangle=0
\;\Longleftrightarrow\;\langle x,u\rangle=\lambda\|u\|^2
\;\Longleftrightarrow\;\lambda=\frac{\langle x,u\rangle}{\|u\|^2}$$
L'existence et l'unicité tombent en une ligne : la condition d'orthogonalité est une équation du
premier degré en $\lambda$, de coefficient $\|u\|^2\ne 0$. $\blacksquare$

Le vecteur $x-p(x)$ s'appelle le **résidu**. Par construction il est orthogonal à $D$, et $x=p(x)+(x-p(x))$ est une décomposition orthogonale : Pythagore s'applique.

---

## 6.3 La propriété qui compte : c'est le point le plus proche

> **Théorème (meilleure approximation).** Pour tout $y\in D$,
> $$\|x-y\|\;\ge\;\|x-p(x)\|$$
> avec égalité si et seulement si $y=p(x)$.

**Démonstration.** Écrivons $x-y=\underbrace{(x-p(x))}_{\perp\,D}+\underbrace{(p(x)-y)}_{\in\,D}$.
Ces deux vecteurs sont orthogonaux, donc par Pythagore :
$$\|x-y\|^2=\|x-p(x)\|^2+\|p(x)-y\|^2\;\ge\;\|x-p(x)\|^2 \qquad\blacksquare$$
> 🔑 **Les moindres carrés ne sont rien d'autre que ce théorème.** Minimiser $\sum_i(v_i-v_0-rt_i)^2$, c'est minimiser $\|v-y\|^2$ sur le sous-espace $y\in\text{Vect}(\mathbf 1,t)$ : la solution **est** la projection orthogonale. Tout le calcul différentiel de [`modele.md`](../../../modele.md) (annuler deux dérivées partielles) retrouve cette figure par un autre chemin.

**Deux définitions, une seule notion.** « Le résidu est orthogonal » et « la distance est minimale » caractérisent le même vecteur. La première est commode pour **calculer**, la seconde pour **comprendre**.

---

## 6.4 Projection sur un sous-espace quelconque

Si $(e_1,\dots,e_d)$ est une base **orthonormée** de $F$ ($\langle e_j,e_k\rangle=\delta_{jk}$) :
$$P_F(x)=\sum_{j=1}^d \langle x,e_j\rangle\,e_j$$
C'est la formule de la droite, appliquée à chaque direction et sommée — licite **parce que** les directions sont orthogonales entre elles. Le [module 9](09-bases-orthonormees-et-isometries.md) montre qu'une telle base existe toujours.

Le théorème de meilleure approximation du § 6.3 vaut à l'identique : la démonstration n'utilise que l'orthogonalité du résidu, jamais la dimension de $F$.

---

## 6.5 Le projecteur comme matrice

$P_F$ est une application **linéaire** ; sa matrice vérifie deux propriétés caractéristiques :
$$P^{\top}=P \quad\text{(symétrie)}\qquad\text{et}\qquad P^2=P\quad\text{(idempotence)}$$
- **Idempotence** : projeter ce qui est déjà projeté ne change rien.
- **Symétrie** : c'est elle qui distingue une projection **orthogonale** d'une projection oblique. Sans elle, $P^2=P$ décrit encore une projection, mais parallèlement à une direction arbitraire.

Et surtout :

> **La trace d'un projecteur orthogonal est égale à son rang**, c'est-à-dire à $\dim F$.

C'est un moyen commode de lire une dimension — donc un **nombre de degrés de liberté** — sur une matrice, sans calculer ni déterminant ni base. Le [module 7](07-supplementaire-orthogonal-et-dimension.md) en fait l'usage décisif.

---

## 6.6 Simulations

### S6.1 — La projection est bien le point le plus proche

```python
import numpy as np

rng = np.random.default_rng(4)
n = 12
x = rng.normal(100, 15, n)
un = np.ones(n)

# on balaye toutes les constantes c et on mesure la distance de x au vecteur c·1
grille = np.linspace(x.mean() - 20, x.mean() + 20, 4001)
dist = np.array([np.linalg.norm(x - c * un) for c in grille])

print(f"minimum atteint en c = {grille[dist.argmin()]:.4f}")
print(f"moyenne empirique    = {x.mean():.4f}")
```

Le minimum tombe sur la moyenne, à la maille de la grille près. **La moyenne est définie par une
propriété de minimisation, pas par sa formule** — c'est ce point de vue que reprend
[`modele.md`](../../../modele.md) pour la droite des moindres carrés.

### S6.2 — Symétrie, idempotence, trace = rang

```python
# projecteur sur un sous-espace F de dimension 3, engendré au hasard
A = rng.normal(size=(n, 3))
P = A @ np.linalg.inv(A.T @ A) @ A.T          # matrice de projection sur Vect(colonnes de A)

print("symétrique  :", np.allclose(P, P.T))
print("idempotente :", np.allclose(P @ P, P))
print(f"trace = {np.trace(P):.4f}   rang = {np.linalg.matrix_rank(P)}   dim F = 3")

y = rng.normal(size=n)
print("résidu ⟂ F  :", np.allclose(A.T @ (y - P @ y), 0))
print("Pythagore   :", np.allclose(y @ y, (P @ y) @ (P @ y) + (y - P @ y) @ (y - P @ y)))
```

La trace vaut $3$ **exactement** — pas approximativement. Retenez ce test : c'est ainsi qu'on
compte des degrés de liberté sans jamais construire de base.

---

## 6.7 Exercices

**E6.1.** Vérifier directement, à partir de la formule du § 6.2, que $p(p(x))=p(x)$ et que $\langle p(x),x-p(x)\rangle=0$.

**E6.2.** Écrire la matrice du projecteur sur $D=\text{Vect}(u)$ sous la forme $P=\frac{uu^{\top}}{\|u\|^2}$. Vérifier $P^{\top}=P$, $P^2=P$, puis calculer $\operatorname{tr}(P)$. *Que vaut-elle, et pourquoi était-ce prévisible ?*

**E6.3.** Montrer que $\|p(x)\|\le\|x\|$, avec égalité si et seulement si $x\in D$. *(Piste : Pythagore.) Quel résultat du [module 3](03-cauchy-schwarz-et-angle.md) retrouve-t-on en explicitant cette inégalité ?*

**E6.4.** Soit $F$ engendré par deux vecteurs $u,v$ **non orthogonaux**. Montrer sur un exemple en dimension 3 que $\frac{\langle x,u\rangle}{\|u\|^2}u+\frac{\langle x,v\rangle}{\|v\|^2}v$ n'est **pas** la projection de $x$ sur $F$. *Où la démonstration du § 6.4 échoue-t-elle ?*

**E6.5.** Une matrice vérifie $P^2=P$ mais pas $P^{\top}=P$. Construire un tel exemple en dimension 2 et représenter géométriquement l'application. *(Réponse attendue : une projection oblique.)*

---

## 6.8 À retenir

- **Du [module 4](04-sous-espaces-et-familles-generatrices.md), on ne retient ici que la
  stabilité** : c'est elle, et rien d'autre, qui fait exister le point le plus proche.
- **$p(x)=\frac{\langle x,u\rangle}{\|u\|^2}u$** sur une droite ; $P_F(x)=\sum_j\langle x,e_j\rangle e_j$ sur un sous-espace, **en base orthonormée**.
- **Le résidu est orthogonal au sous-espace** — c'est la définition opérationnelle.
- ⭐ **La projection est le point le plus proche** : les moindres carrés ne sont que cela.
- **$P^{\top}=P$ et $P^2=P$** caractérisent un projecteur orthogonal.
- **$\operatorname{tr}(P)=\operatorname{rang}(P)=\dim F$** : les dimensions se lisent sur la trace.

---

⬅️ [Module 5 — Orthogonalité et Pythagore](05-orthogonalite-et-pythagore.md) ·
➡️ [Module 7 — Supplémentaire orthogonal et dimension](07-supplementaire-orthogonal-et-dimension.md) ·
🏠 [Sommaire](README.md)
