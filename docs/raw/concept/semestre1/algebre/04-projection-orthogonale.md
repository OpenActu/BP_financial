# Module 4 — La projection orthogonale ⭐

**Durée : 1 h.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) à [3](03-orthogonalite-et-pythagore.md). ⭐ **Module central du cours.**

> **La question traitée.** Étant donné un vecteur $x$ et un sous-espace $F$, quel élément de $F$
> ressemble le plus à $x$ ?

**Ce qui est en jeu.** La réponse — la projection orthogonale — **est** la méthode des moindres
carrés. Tout le calcul différentiel d'une régression linéaire (annuler des dérivées partielles)
n'est qu'une façon coûteuse de retrouver la figure de ce module.

---

## 4.1 Sous-espace, et sous-espace engendré

La question du module parle d'un **sous-espace** $F$. Ce n'est pas un mot de décor : c'est l'hypothèse qui rend la question bien posée, et tout ce qui suit s'appuie sur elle.

> **Définition (sous-espace vectoriel).** Une partie $F\subseteq\mathbb R^n$ est un **sous-espace vectoriel** si elle est non vide et **stable par combinaison linéaire** :
> $$y,z\in F\ \text{ et }\ \alpha,\beta\in\mathbb R\quad\Longrightarrow\quad \alpha y+\beta z\in F$$

Prendre $\alpha=\beta=0$ montre qu'un sous-espace **contient toujours $0$** ; « non vide et stable » et « contient $0$ et stable » sont donc deux formulations de la même chose. Il n'y a rien d'autre à retenir : la stabilité est la seule propriété de $F$ utilisée dans tout le module — au § 4.3, elle sert à affirmer que $p(x)-y$ appartient encore à $F$.

> **Définition (sous-espace engendré).** Pour $u_1,\dots,u_d\in\mathbb R^n$,
> $$\text{Vect}(u_1,\dots,u_d)=\bigl\{\lambda_1u_1+\dots+\lambda_du_d\ :\ \lambda_1,\dots,\lambda_d\in\mathbb R\bigr\}$$
> — l'ensemble de **toutes** leurs combinaisons linéaires.

C'est bien un sous-espace : une combinaison linéaire de combinaisons linéaires des $u_j$ est encore une combinaison linéaire des $u_j$, en regroupant les coefficients. Et c'est le **plus petit** qui contienne les $u_j$ : tout sous-espace les contenant contient, par stabilité, chacune de leurs combinaisons. D'où le nom : le sous-espace **engendré** par $u_1,\dots,u_d$.

**Le cas $d=1$ — la droite.** $\text{Vect}(u)=\{\lambda u\ :\ \lambda\in\mathbb R\}$ est la **droite** passant par l'origine et dirigée par $u$ : c'est le $D$ du § 4.2. L'hypothèse $u\ne 0$ y est indispensable, et pour une raison de géométrie avant d'être de calcul — $\text{Vect}(0)=\{0\}$ est un sous-espace parfaitement légitime, mais réduit à un point : ce n'est pas une droite, et le projeté d'un $x$ dessus vaut $0$ sans qu'aucune direction ne soit en jeu.

**Dimension.** Le nombre $d$ de générateurs n'est pas la dimension de $\text{Vect}(u_1,\dots,u_d)$ : il la majore. Les deux coïncident exactement quand la famille est **libre** — et le [§ 3.3](03-orthogonalite-et-pythagore.md) donne un critère commode pour s'en assurer : une famille orthogonale de vecteurs non nuls est libre. C'est ce que le § 4.4 exploite en travaillant dans une base orthonormée.

Les sous-espaces qui reviennent dans tout ce cours sont peu nombreux :

| Sous-espace                         | Ce qu'il contient                               | Où il sert                                                            |
| ----------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------- |
| $\text{Vect}(\mathbf 1)$            | les vecteurs **constants** $(c,\dots,c)$        | la moyenne — [module 5](05-supplementaire-orthogonal-et-dimension.md) |
| $\text{Vect}(\mathbf 1)^{\perp}$    | les vecteurs de **somme nulle** (exercice E3.2) | les écarts à la moyenne, les $n-1$ degrés de liberté                  |
| $\text{Vect}(\mathbf 1,t)$          | les suites **affines** $v_0+r\,t_i$             | la droite des moindres carrés — [`modele.md`](../../../modele.md)     |
| $\text{Vect}(\text{colonnes de }A)$ | les ajustements atteignables                    | la régression multiple — simulation S4.2                              |

> ⚠️ **« Sous-espace » n'est pas « sous-ensemble », et un sous-espace passe toujours par
> l'origine.** Une droite du plan qui ne passe pas par $0$ n'est pas un sous-espace. Cela n'a rien de contradictoire avec la régression : la droite d'équation $v=v_0+rt$ est **affine dans le plan $(t,v)$**, mais le vecteur $v_0\mathbf 1+r\,t$ qu'elle produit vit dans $\mathbb R^n$, où il appartient bel et bien au sous-espace $\text{Vect}(\mathbf 1,t)$. Le sous-espace n'est pas la droite qu'on dessine ; c'est l'ensemble des **séries de $n$ valeurs** qu'une telle droite peut engendrer.

> 🔑 **C'est la stabilité qui garantit une réponse.** Sur une partie quelconque de $\mathbb R^n$ — une sphère, un segment, un ensemble fini — « l'élément le plus proche de $x$ » peut ne pas exister, ou en exister plusieurs. Le § 4.3 montre que sur un sous-espace il existe et qu'il est unique, et la démonstration n'invoque rien d'autre que la stabilité et Pythagore.

---

## 4.2 Projection sur une droite

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

## 4.3 La propriété qui compte : c'est le point le plus proche

> **Théorème (meilleure approximation).** Pour tout $y\in D$,
> $$\|x-y\|\;\ge\;\|x-p(x)\|$$
> avec égalité si et seulement si $y=p(x)$.

**Démonstration.** Écrivons $x-y=\underbrace{(x-p(x))}_{\perp\,D}+\underbrace{(p(x)-y)}_{\in\,D}$.
Ces deux vecteurs sont orthogonaux, donc par Pythagore :
$$\|x-y\|^2=\|x-p(x)\|^2+\|p(x)-y\|^2\;\ge\;\|x-p(x)\|^2 \qquad\blacksquare$$
> 🔑 **Les moindres carrés ne sont rien d'autre que ce théorème.** Minimiser $\sum_i(v_i-v_0-rt_i)^2$, c'est minimiser $\|v-y\|^2$ sur le sous-espace $y\in\text{Vect}(\mathbf 1,t)$ : la solution **est** la projection orthogonale. Tout le calcul différentiel de [`modele.md`](../../../modele.md) (annuler deux dérivées partielles) retrouve cette figure par un autre chemin.

**Deux définitions, une seule notion.** « Le résidu est orthogonal » et « la distance est minimale » caractérisent le même vecteur. La première est commode pour **calculer**, la seconde pour **comprendre**.

---

## 4.4 Projection sur un sous-espace quelconque

Si $(e_1,\dots,e_d)$ est une base **orthonormée** de $F$ ($\langle e_j,e_k\rangle=\delta_{jk}$) :
$$P_F(x)=\sum_{j=1}^d \langle x,e_j\rangle\,e_j$$
C'est la formule de la droite, appliquée à chaque direction et sommée — licite **parce que** les directions sont orthogonales entre elles. Le [module 7](07-bases-orthonormees-et-isometries.md) montre qu'une telle base existe toujours.

Le théorème de meilleure approximation du § 4.3 vaut à l'identique : la démonstration n'utilise que l'orthogonalité du résidu, jamais la dimension de $F$.

---

## 4.5 Le projecteur comme matrice

$P_F$ est une application **linéaire** ; sa matrice vérifie deux propriétés caractéristiques :
$$P^{\top}=P \quad\text{(symétrie)}\qquad\text{et}\qquad P^2=P\quad\text{(idempotence)}$$
- **Idempotence** : projeter ce qui est déjà projeté ne change rien.
- **Symétrie** : c'est elle qui distingue une projection **orthogonale** d'une projection oblique. Sans elle, $P^2=P$ décrit encore une projection, mais parallèlement à une direction arbitraire.

Et surtout :

> **La trace d'un projecteur orthogonal est égale à son rang**, c'est-à-dire à $\dim F$.

C'est un moyen commode de lire une dimension — donc un **nombre de degrés de liberté** — sur une matrice, sans calculer ni déterminant ni base. Le [module 5](05-supplementaire-orthogonal-et-dimension.md) en fait l'usage décisif.

---

## 4.6 Simulations

### S4.1 — La projection est bien le point le plus proche

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

### S4.2 — Symétrie, idempotence, trace = rang

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

## 4.7 Exercices

**E4.1.** Vérifier directement, à partir de la formule du § 4.2, que $p(p(x))=p(x)$ et que $\langle p(x),x-p(x)\rangle=0$.

**E4.2.** Écrire la matrice du projecteur sur $D=\text{Vect}(u)$ sous la forme $P=\frac{uu^{\top}}{\|u\|^2}$. Vérifier $P^{\top}=P$, $P^2=P$, puis calculer $\operatorname{tr}(P)$. *Que vaut-elle, et pourquoi était-ce prévisible ?*

**E4.3.** Montrer que $\|p(x)\|\le\|x\|$, avec égalité si et seulement si $x\in D$. *(Piste : Pythagore.) Quel résultat du [module 2](02-cauchy-schwarz-et-angle.md) retrouve-t-on en explicitant cette inégalité ?*

**E4.4.** Soit $F$ engendré par deux vecteurs $u,v$ **non orthogonaux**. Montrer sur un exemple en dimension 3 que $\frac{\langle x,u\rangle}{\|u\|^2}u+\frac{\langle x,v\rangle}{\|v\|^2}v$ n'est **pas** la projection de $x$ sur $F$. *Où la démonstration du § 4.4 échoue-t-elle ?*

**E4.5.** Une matrice vérifie $P^2=P$ mais pas $P^{\top}=P$. Construire un tel exemple en dimension 2 et représenter géométriquement l'application. *(Réponse attendue : une projection oblique.)*

---

## 4.8 À retenir

- **Un sous-espace est une partie stable par combinaison linéaire**, donc contenant $0$ ;
  $\text{Vect}(u_1,\dots,u_d)$ est le plus petit qui contienne les $u_j$.
- **$p(x)=\frac{\langle x,u\rangle}{\|u\|^2}u$** sur une droite ; $P_F(x)=\sum_j\langle x,e_j\rangle e_j$ sur un sous-espace, **en base orthonormée**.
- **Le résidu est orthogonal au sous-espace** — c'est la définition opérationnelle.
- ⭐ **La projection est le point le plus proche** : les moindres carrés ne sont que cela.
- **$P^{\top}=P$ et $P^2=P$** caractérisent un projecteur orthogonal.
- **$\operatorname{tr}(P)=\operatorname{rang}(P)=\dim F$** : les dimensions se lisent sur la trace.

---

⬅️ [Module 3 — Orthogonalité et Pythagore](03-orthogonalite-et-pythagore.md) ·
➡️ [Module 5 — Supplémentaire orthogonal et dimension](05-supplementaire-orthogonal-et-dimension.md) ·
🏠 [Sommaire](README.md)
