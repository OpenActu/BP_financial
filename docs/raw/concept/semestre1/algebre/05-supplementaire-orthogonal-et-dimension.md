# Module 5 — Supplémentaire orthogonal, noyau, rang

**Durée : 45 min.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) à [4](04-projection-orthogonale.md). **L'outillage que le [module 6](06-degres-de-liberte-et-centrage.md) mettra au travail.**

> **La question traitée.** Un sous-espace $F$ de $\mathbb R^n$ étant donné, que reste-t-il de $\mathbb R^n$ une fois $F$ retiré ? Combien de dimensions une **contrainte linéaire** $\langle u,a\rangle=0$ coûte-t-elle exactement ?

**Ce qui est en jeu.** Une seule comptabilité, écrite de trois manières — $\dim F^\perp=n-\dim F$,
le théorème du rang, et la dimension $n-1$ d'un hyperplan. C'est elle que les statisticiens
appelleront « degrés de liberté », et le [module 6](06-degres-de-liberte-et-centrage.md) n'en sera qu'un cas particulier, celui de $F=\text{Vect}(\mathbf 1)$.

---

## 5.1 Le supplémentaire orthogonal

> **Définition.** $F^\perp=\{u\in\mathbb R^n:\ \langle u,f\rangle=0\ \ \forall f\in F\}$.

> **Théorème.** Pour tout sous-espace $F$ de $\mathbb R^n$ : $$\mathbb R^n=F\oplus F^\perp,\qquad \dim F^\perp=n-\dim F,\qquad (F^\perp)^\perp=F$$
> et tout $x$ s'écrit de **manière unique** $x=P_F(x)+P_{F^\perp}(x)$, avec
> $$\|x\|^2=\|P_F(x)\|^2+\|P_{F^\perp}(x)\|^2$$

La dernière égalité est le [Pythagore du module 3](03-orthogonalite-et-pythagore.md), appliqué à la décomposition ci-dessus. L'existence de la décomposition est la [projection du module 4](04-projection-orthogonale.md) ; l'unicité vient de $F\cap F^\perp=\{0\}$, conséquence immédiate du caractère défini positif du produit scalaire.

> 🔑 **Décomposer, c'est répartir des dimensions.** $n=\dim F+\dim F^\perp$ : chaque dimension de $\mathbb R^n$ est affectée à l'un des deux morceaux, jamais aux deux. C'est cette comptabilité — et rien d'autre — que les statisticiens appellent « degrés de liberté ».

## 5.2 Forme linéaire, noyau, théorème du rang

> **Définition.** Une application $f:\mathbb R^n\to\mathbb R^m$ est **linéaire** si $f(u+v)=f(u)+f(v)$ et $f(\lambda u)=\lambda f(u)$ pour tous $u,v$ et tout réel $\lambda$. Quand l'arrivée est $\mathbb R$ tout court ($m=1$), on parle de **forme linéaire**

> **Définition.** Le **noyau** de $f$ est l'ensemble des vecteurs que $f$ envoie sur $0$ :
> $$\ker f=\{u\in\mathbb R^n:\ f(u)=0\}$$

Le noyau est **toujours un sous-espace vectoriel** de l'espace de départ, et la vérification tient
en trois lignes : $f(0)=0$ donc $0\in\ker f$ ; si $f(u)=f(v)=0$ alors $f(u+v)=0+0=0$ ; et $f(\lambda u)=\lambda\cdot 0=0$. C'est ce qui autorise à lui appliquer tout ce qui précède — dimension, supplémentaire orthogonal, projection.

Dans $\mathbb R^n$ muni de son produit scalaire, **toute forme linéaire est un produit scalaire
déguisé.** En posant $a=\bigl(f(e_1),\dots,f(e_n)\bigr)$, la linéarité donne $$f(u)=f\Bigl(\sum_i u_ie_i\Bigr)=\sum_i u_i\,f(e_i)=\langle u,a\rangle$$
d'où la traduction qui servira partout : $\ker f=\{u:\ \langle u,a\rangle=0\}=\text{Vect}(a)^\perp$.
La forme linéaire est nulle exactement quand $a=0$.

> **Théorème du rang.** Pour $f:\mathbb R^n\to\mathbb R^m$ linéaire,
> $$\dim\ker f+\dim\operatorname{im}f=n$$
> où $\operatorname{im}f=\{f(u):u\in\mathbb R^n\}$ est l'**image**.

**Démonstration.** Posons $K=\ker f$ et prenons pour espace de travail son supplémentaire
orthogonal $S=K^\perp$. Le théorème du § 5.1 donne déjà
$$\mathbb R^n=K\oplus S,\qquad \dim S=n-\dim K$$
Il reste donc à établir un seul point : $\dim\operatorname{im}f=\dim S$. Soit $(s_1,\dots,s_p)$ une
base de $S$, avec $p=\dim S$. Montrons que $\bigl(f(s_1),\dots,f(s_p)\bigr)$ est une base de
$\operatorname{im}f$.

*Elle engendre l'image.* Tout $u\in\mathbb R^n$ se décompose en $u=k+s$ avec $k\in K$ et $s\in S$,
et alors
$$f(u)=f(k)+f(s)=0+f(s)=f(s)$$
Autrement dit **$f$ ne perd rien à être restreinte à $S$** : $\operatorname{im}f=f(S)$. En écrivant
$s=\sum_j\lambda_js_j$ et en repassant par la linéarité, $f(u)=\sum_j\lambda_jf(s_j)$.

*Elle est libre.* Supposons $\sum_j\lambda_jf(s_j)=0$. Par linéarité, $f\bigl(\sum_j\lambda_js_j\bigr)=0$,
donc le vecteur $\sum_j\lambda_js_j$ appartient à $K$ ; mais il appartient aussi à $S$, comme
combinaison des $s_j$. Il est donc dans $K\cap S=K\cap K^\perp=\{0\}$ — c'est l'exercice E5.1, et
c'est exactement là que le caractère **défini** positif du produit scalaire est utilisé. Ainsi
$\sum_j\lambda_js_j=0$, et la liberté de la base $(s_j)$ force $\lambda_1=\dots=\lambda_p=0$.

Une famille génératrice et libre est une base : $\dim\operatorname{im}f=p=\dim S=n-\dim K$, ce qui
est l'énoncé. $\square$

> 🔑 **La démonstration dit ce que le théorème compte.** $f$ écrase $K$ sur $0$ et reproduit
> **fidèlement** $S=K^\perp$ dans l'image : $f$ restreinte à $S$ est une bijection de $S$ sur
> $\operatorname{im}f$. Les $n$ dimensions du départ se répartissent donc en deux tas, celles qui
> sont effacées et celles qui survivent — la même comptabilité qu'au § 5.1, à ceci près que le
> second tas est lu **à l'arrivée** plutôt qu'au départ.

> ⚠️ **Aucune circularité.** La démonstration ci-dessus consomme $\dim F^\perp=n-\dim F$ (§ 5.1),
> qui s'établit de son côté par **Gram–Schmidt** — une BON dont les $d$ premiers vecteurs
> engendrent $F$ et les $n-d$ suivants $F^\perp$ ([module 7](07-bases-orthonormees-et-isometries.md),
> § 7.3) — sans jamais invoquer le théorème du rang. La preuve algébrique usuelle, valable dans un
> espace vectoriel **sans** produit scalaire, remplace $K^\perp$ par n'importe quel supplémentaire
> de $K$ obtenu en complétant une base du noyau ; l'argument est mot pour mot le même.

Pour une **forme** linéaire non nulle, l'image est un sous-espace de $\mathbb R$ non réduit à
$\{0\}$, donc $\mathbb R$ tout entier : $\dim\operatorname{im}f=1$, et le théorème donne $\dim\ker f=n-1$. C'est
le même $n-1$ que celui du théorème du § 5.1 avec $F=\text{Vect}(a)$ — deux chemins vers le même
comptage.

| Forme linéaire $f$ | Vecteur $a$ | $\ker f$ | $\dim$ |
| --- | --- | --- | --- |
| $u\mapsto\sum_i u_i$ | $\mathbf 1$ | les vecteurs de somme nulle | $n-1$ |
| $u\mapsto u_1$ | $e_1$ | les vecteurs de première coordonnée nulle | $n-1$ |
| $u\mapsto 0$ | $0$ | $\mathbb R^n$ tout entier | $n$ |

> 🔑 **Le noyau, c'est ce que l'application efface.** Un projecteur se lit ainsi : $M=I_n-\frac1nJ$
> du [§ 6.3](06-degres-de-liberte-et-centrage.md) a pour noyau $\text{Vect}(\mathbf 1)$ — la moyenne, écrasée — et pour image $H$. C'est
> exactement ce que la simulation S6.2 fait apparaître dans le spectre : une valeur propre $0$ (le
> noyau) et $n-1$ valeurs propres $1$ (l'image, laissée intacte).

> ⚠️ **Le mot « noyau » a un autre emploi**, plus tardif : au [module 9](09-covariance-et-produit-scalaire.md),
> le « noyau de la covariance » désigne les séries que la covariance ne distingue pas de la série
> nulle — les séries **constantes**. C'est le noyau d'une forme *bilinéaire*, pas d'une application
> linéaire ; l'ensemble obtenu est pourtant le même que $\ker M=\text{Vect}(\mathbf 1)$, et ce n'est
> pas un hasard : la covariance ne voit de $x$ que $Mx$.

---

## 5.3 L'hyperplan

> **Définition.** Un **hyperplan** (vectoriel) de $\mathbb R^n$ est un sous-espace de dimension $n-1$ — une dimension de moins que l'espace tout entier.

Le nom généralise « plan » à toute dimension : un hyperplan de $\mathbb R^2$ est une droite passant par l'origine, un hyperplan de $\mathbb R^3$ est un plan passant par l'origine, et un hyperplan de $\mathbb R^{12}$ est un sous-espace de dimension 11 que personne ne dessine mais qui se manipule à l'identique.

Trois descriptions d'un même objet, équivalentes dans $\mathbb R^n$ :

| Description | Écriture |
| --- | --- |
| sous-espace de dimension $n-1$ | $\dim H=n-1$ |
| noyau d'une forme linéaire **non nulle** | $H=\{u:\ a_1u_1+\dots+a_nu_n=0\}$, avec $a\neq 0$ |
| orthogonal d'une **droite** vectorielle | $H=\text{Vect}(a)^\perp$, avec $a\neq 0$ |

Les deux dernières coïncident parce que $\sum_i a_iu_i=\langle u,a\rangle$ : annuler une forme linéaire, c'est être orthogonal au vecteur $a$ de ses coefficients. Et la première suit du théorème du § 5.1 appliqué à $F=\text{Vect}(a)$, de dimension 1 : $\dim\text{Vect}(a)^\perp=n-1$.

> 🔑 **Un hyperplan, c'est exactement « une contrainte linéaire ».** Une équation $\langle u,a\rangle=0$ retire **une** dimension et pas davantage — le rang du système est 1. C'est tout ce qu'il faudra pour lire $\sum_i(x_i-\bar x)=0$ comme la perte d'un seul degré de liberté, au [module 6](06-degres-de-liberte-et-centrage.md).

> ⚠️ **Hyperplan vectoriel, pas affine.** Tous les hyperplans de ce cours passent par l'origine : ce sont des **sous-espaces**. L'ensemble $\{u:\langle u,a\rangle=c\}$ avec $c\neq 0$ est un hyperplan *affine* — le translaté du précédent — et n'est pas un sous-espace, puisqu'il ne contient pas $0$.

---

---

## 5.4 Simulations

### S5.1 — Le théorème du rang, vérifié sur une matrice quelconque

```python
import numpy as np

rng = np.random.default_rng(5)
n, m = 8, 5
A = rng.normal(size=(m, n)) @ np.diag([1, 1, 1, 0, 0, 0, 0, 0])   # rang volontairement bas
f = lambda u: A @ u                                               # f : R^n -> R^m, linéaire

rang = np.linalg.matrix_rank(A)                  # dim im f
noyau = n - rang                                 # dim ker f, attendu par le théorème

print(f"dim im f  = {rang}")
print(f"dim ker f = {noyau}   (n - rang = {n} - {rang})")
print("théorème du rang :", rang + noyau == n)

# le noyau, explicitement : les vecteurs singuliers de valeur singulière nulle
_, s, Vt = np.linalg.svd(A)
K = Vt[np.sum(s > 1e-10):]                       # base de ker f
print("f écrase bien le noyau :", np.allclose([f(k) for k in K], 0))
print("dim de la base trouvée :", K.shape[0])
```

**Le noyau n'est jamais calculé, il est constaté** : sa dimension se lit sur le rang, sans qu'aucun
vecteur ne soit résolu.

### S5.2 — Une contrainte linéaire coûte exactement une dimension

```python
a = rng.normal(size=n)                           # une direction quelconque, non nulle
P = np.outer(a, a) / (a @ a)                     # projecteur sur Vect(a)
Q = np.eye(n) - P                                # projecteur sur l'hyperplan Vect(a)⟂

print(f"tr(P) = {np.trace(P):.4f}  (dim Vect(a) = 1)")
print(f"tr(Q) = {np.trace(Q):.4f}  (dim de l'hyperplan = n-1 = {n-1})")

u = Q @ rng.normal(size=n)                       # un vecteur de l'hyperplan
print("il vérifie la contrainte ⟨u,a⟩ = 0 :", abs(u @ a) < 1e-10)
```

Une contrainte, une dimension — **pas deux, pas zéro**. Recommencez avec $a=0$ : le projecteur $Q$
devient l'identité, la contrainte ne contraint plus rien, et l'« hyperplan » est $\mathbb R^n$
tout entier.

---

## 5.5 Exercices

**E5.1.** Montrer que $F\cap F^\perp=\{0\}$. *Quelle propriété du § 1.1 est en jeu ?*

**E5.2.** Montrer que $F\subset G\Rightarrow G^\perp\subset F^\perp$. *Illustrer avec
$F=\text{Vect}(\mathbf 1)$ et $G=\text{Vect}(\mathbf 1,t)$ où $t=(1,2,\dots,n)$, et relier aux
dimensions $n-1$ et $n-2$ ([module 6](06-degres-de-liberte-et-centrage.md)).*

**E5.3.** Soit $f:\mathbb R^n\to\mathbb R^m$ linéaire.
1. Vérifier directement que $\ker f$ est un sous-espace, sans invoquer le résultat général.
2. Montrer que $f$ est **injective** si et seulement si $\ker f=\{0\}$.
3. *Qu'affirme alors le théorème du rang pour une application injective de $\mathbb R^n$ dans
   $\mathbb R^m$ ? Qu'impose-t-il sur $m$ ?*

**E5.4.** Montrer que toute forme linéaire sur $\mathbb R^n$ s'écrit $u\mapsto\langle u,a\rangle$
pour un unique $a$, et que $f$ est la forme nulle si et seulement si $a=0$. *En déduire qu'un
hyperplan détermine sa direction normale à un facteur multiplicatif près.*

**E5.5.** Que devient $\dim F^\perp$ si l'on ajoute à $F$ un vecteur **déjà dans $F$** ? *En quoi
cela justifie-t-il que « degrés de liberté » soit une dimension et non un compteur de
paramètres ?*

---

## 5.6 À retenir

- **$\mathbb R^n=F\oplus F^\perp$**, $\dim F^\perp=n-\dim F$, décomposition unique et Pythagore.
- **Noyau** $\ker f=\{u:f(u)=0\}$ : toujours un sous-espace. Dans $\mathbb R^n$, toute forme
  linéaire s'écrit $u\mapsto\langle u,a\rangle$, donc $\ker f=\text{Vect}(a)^\perp$.
- **Théorème du rang** $\dim\ker f+\dim\operatorname{im}f=n$, démontré en restreignant $f$ à
  $(\ker f)^\perp$, où elle devient bijective : ce que $f$ efface, et ce qu'elle reproduit.
- **Hyperplan** = sous-espace de dimension $n-1$ = noyau d'une forme linéaire non nulle =
  orthogonal d'une droite. **Une contrainte linéaire, une dimension en moins** — c'est tout le
  [module 6](06-degres-de-liberte-et-centrage.md).

---

⬅️ [Module 4 — La projection orthogonale](04-projection-orthogonale.md) ·
➡️ [Module 6 — Degrés de liberté et centrage](06-degres-de-liberte-et-centrage.md) ·
🏠 [Sommaire](README.md)
