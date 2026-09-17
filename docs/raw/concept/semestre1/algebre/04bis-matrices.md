# Module 4 bis — Les matrices

**Durée : 1 h 15.** Prérequis : modules [1](01-espace-vectoriel.md), [2](02-produit-scalaire-et-norme.md) et [4](04-sous-espaces-et-familles-generatrices.md). **Un préalable de vocabulaire** : les modules 5 à 12 écrivent $X^{\top}u$, $A^{\top}A$, $(A^{\top}A)^{-1}$, $\operatorname{tr}(P)$ ou $I_n-\frac1nJ$ sans les redéfinir. Ils sont tous définis ici, et chaque règle de calcul y est démontrée.

> **La question traitée.** Qu'est-ce qu'une matrice, que signifie le produit $Ax$ — et pourquoi a-t-on le droit de calculer avec comme on le fait ?

**Ce qui est en jeu.** Une matrice n'est pas un objet nouveau : c'est une **liste de vecteurs rangés côte à côte**, et le produit $Ax$ n'est qu'une **combinaison linéaire** de ces vecteurs, écrite en abrégé. Tout le reste en découle — le produit de deux matrices, la transposée, l'inverse. Ce module ne contient aucune géométrie nouvelle : il donne une **écriture compacte** à ce que les modules 1 à 4 savent déjà faire.

---

## 4bis.1 Une matrice, c'est des vecteurs rangés en colonnes

> **Définition.** Une **matrice** de taille $n\times p$ (lire « $n$ lignes, $p$ colonnes ») est un tableau de $np$ réels
> $$A=\begin{pmatrix}a_{11}&a_{12}&\cdots&a_{1p}\\a_{21}&a_{22}&\cdots&a_{2p}\\\vdots&\vdots&&\vdots\\a_{n1}&a_{n2}&\cdots&a_{np}\end{pmatrix}$$
> Le réel $a_{ij}$ est le **coefficient** situé à la **ligne $i$** et à la **colonne $j$** — toujours la ligne d'abord. On note aussi $A=(a_{ij})$.

L'ordre des indices est la première source d'erreur : $a_{23}$ est à la deuxième ligne, troisième colonne, et $a_{32}$ ailleurs.

**La lecture qui sert : par colonnes.** La $j$-ième colonne de $A$ est un vecteur de $\mathbb R^n$, noté $a_j=(a_{1j},\dots,a_{nj})$. Une matrice $n\times p$ est donc **$p$ vecteurs de $\mathbb R^n$ rangés côte à côte**, et l'on écrit
$$A=\begin{pmatrix}a_1&a_2&\cdots&a_p\end{pmatrix}$$
C'est exactement la matrice $X=(\mathbf 1\ \ t)$ du [§ 5.1](05-orthogonalite-et-pythagore.md) : ses deux colonnes sont les deux générateurs du plan de la droite ajustée,
$$X=\begin{pmatrix}\mathbf 1&t\end{pmatrix}=\begin{pmatrix}1&1\\1&2\\1&3\\1&4\end{pmatrix}\qquad(4\times 2)$$

Exemple de travail pour tout le module :
$$A=\begin{pmatrix}1&2\\0&1\\3&-1\end{pmatrix}\qquad(3\times 2),\qquad a_1=(1,0,3),\quad a_2=(2,1,-1)$$

**Les vecteurs sont des colonnes.** À partir de ce module, un vecteur $x\in\mathbb R^n$ est identifié à la matrice $n\times 1$ de ses coordonnées écrites **en colonne**. L'écriture $x=(x_1,\dots,x_n)$ du [module 1](01-espace-vectoriel.md) reste permise, mais ce n'est qu'une commodité typographique pour gagner de la place.

**Deux opérations, coefficient par coefficient.** Pour $A,B$ de **même taille** et $\lambda\in\mathbb R$ :
$$(A+B)_{ij}=a_{ij}+b_{ij}\qquad\text{et}\qquad(\lambda A)_{ij}=\lambda\,a_{ij}$$
Ce sont les deux opérations du [§ 1.2](01-espace-vectoriel.md), appliquées à un tableau de $np$ nombres au lieu d'une liste. Les huit règles du § 1.3 restent donc valables : **les matrices $n\times p$ forment un espace vectoriel**, comme le [§ 1.3](01-espace-vectoriel.md) l'annonçait. Deux matrices de tailles différentes ne s'additionnent pas.

**Quelques matrices qui reviendront.**

| Matrice            | Définition                                                                                                                                                     | Où elle sert                                                              |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **carrée**         | $n=p$                                                                                                                                                          | projecteurs, covariance                                                   |
| **nulle** $0$      | tous les coefficients valent $0$                                                                                                                               | partout                                                                   |
| **identité** $I_n$ | carrée, $1$ sur la **diagonale** ($i=j$), $0$ ailleurs : $(I_n)_{ij}=\delta_{ij}$, où le **symbole de Kronecker** $\delta_{ij}$ vaut $1$ si $i=j$ et $0$ sinon | § 4bis.3                                                                  |
| $J$                | carrée $n\times n$, tous les coefficients valent $1$                                                                                                           | la moyenne, le centrage ([module 8](08-degres-de-liberte-et-centrage.md)) |

La **diagonale** d'une matrice carrée est formée des coefficients $a_{11},a_{22},\dots,a_{nn}$.

---

## 4bis.2 Le produit d'une matrice par un vecteur

> **Définition.** Soit $A$ de taille $n\times p$ et $x\in\mathbb R^p$. Le produit $Ax$ est le vecteur de $\mathbb R^n$ de coordonnées
> $$(Ax)_i=\sum_{j=1}^p a_{ij}\,x_j=a_{i1}x_1+a_{i2}x_2+\dots+a_{ip}x_p\qquad i=1,\dots,n$$

⚠️ **Le produit n'existe que si les tailles s'emboîtent** : $x$ doit avoir autant de coordonnées que $A$ a de **colonnes**. Une matrice $n\times p$ prend un vecteur de $\mathbb R^p$ et rend un vecteur de $\mathbb R^n$.

Sur l'exemple, avec $x=(2,1)$ :
$$Ax=\begin{pmatrix}1&2\\0&1\\3&-1\end{pmatrix}\begin{pmatrix}2\\1\end{pmatrix}=\begin{pmatrix}1\cdot2+2\cdot1\\0\cdot2+1\cdot1\\3\cdot2+(-1)\cdot1\end{pmatrix}=\begin{pmatrix}4\\1\\5\end{pmatrix}$$

La formule se lit de deux façons, et **les deux sont indispensables**.

**Lecture par colonnes — $Ax$ est une combinaison linéaire des colonnes.**

> **Proposition.** $Ax=x_1a_1+x_2a_2+\dots+x_pa_p$.

**Démonstration.** Comparons coordonnée par coordonnée. La $i$-ième coordonnée de $x_ja_j$ est $x_j\,a_{ij}$ (§ 1.2), donc celle de la somme est $\sum_jx_ja_{ij}$ — c'est $(Ax)_i$. Deux vecteurs qui ont les mêmes coordonnées sont égaux. $\blacksquare$

Sur l'exemple : $2\,(1,0,3)+1\,(2,1,-1)=(4,1,5)$. Et sur la matrice $X=(\mathbf 1\ \ t)$ :
$$X\begin{pmatrix}9\\2\end{pmatrix}=9\,\mathbf 1+2\,t=(11,\,13,\,15,\,17)$$
c'est la droite ajustée $\hat x$ du [§ 5.1](05-orthogonalite-et-pythagore.md). **Le vecteur $x$ contient les coefficients, la matrice contient les vecteurs à combiner.**

> 🔑 **$\text{Vect}(\text{colonnes de }A)=\{A\lambda:\ \lambda\in\mathbb R^p\}$.** C'est la proposition, lue pour tous les $\lambda$ à la fois : les combinaisons linéaires des colonnes sont exactement les produits $A\lambda$. « Ajuster un modèle linéaire », c'est chercher un $\lambda$ — et le [§ 6.4](06-projection-orthogonale.md) le trouve.

**Lecture par lignes — chaque coordonnée est un produit scalaire.** La $i$-ième ligne de $A$, $(a_{i1},\dots,a_{ip})$, est un vecteur de $\mathbb R^p$, et la définition dit exactement
$$(Ax)_i=\bigl\langle\,\text{ligne } i \text{ de } A,\ x\,\bigr\rangle$$
au sens du [§ 2.1](02-produit-scalaire-et-norme.md). C'est la lecture qui sert pour **calculer** à la main, et celle du § 5.1 : $X^{\top}u$ y est le vecteur des produits scalaires de $u$ avec les générateurs.

**La propriété fondamentale : la linéarité.**

> **Proposition.** Pour toute matrice $M$ de taille $n\times p$, tous $x,y\in\mathbb R^p$ et tous $\alpha,\beta\in\mathbb R$ :
> $$M(\alpha x+\beta y)=\alpha\,Mx+\beta\,My$$

**Démonstration par les coordonnées.** Le vecteur $\alpha x+\beta y$ a pour $j$-ième coordonnée $\alpha x_j+\beta y_j$ (§ 1.2). Par définition du produit, pour chaque $i$ :
$$\bigl(M(\alpha x+\beta y)\bigr)_i=\sum_{j=1}^p m_{ij}\,(\alpha x_j+\beta y_j)$$
On développe chaque terme par distributivité **dans $\mathbb R$**, $m_{ij}(\alpha x_j+\beta y_j)=\alpha\,m_{ij}x_j+\beta\,m_{ij}y_j$, puis on sépare la somme en deux et on sort les constantes $\alpha$ et $\beta$ :
$$\sum_{j=1}^p m_{ij}\,(\alpha x_j+\beta y_j)=\alpha\sum_{j=1}^p m_{ij}x_j+\beta\sum_{j=1}^p m_{ij}y_j=\alpha\,(Mx)_i+\beta\,(My)_i$$
Le membre de droite est la $i$-ième coordonnée de $\alpha Mx+\beta My$ (§ 1.2 encore). Les deux vecteurs ont les mêmes $n$ coordonnées : ils sont égaux. $\blacksquare$

**Démonstration par les colonnes.** Par la proposition précédente, puis les huit règles du [§ 1.3](01-espace-vectoriel.md) pour redistribuer et regrouper :
$$M(\alpha x+\beta y)=\sum_{j=1}^p(\alpha x_j+\beta y_j)\,m_j=\alpha\sum_{j=1}^px_j\,m_j+\beta\sum_{j=1}^py_j\,m_j=\alpha\,Mx+\beta\,My\qquad\blacksquare$$

Les deux preuves disent la même chose : **aucun terme du calcul ne multiplie deux coordonnées de $x$ entre elles**. Chaque $x_j$ apparaît au premier degré, multiplié par un coefficient fixe — c'est tout ce que « linéaire » veut dire. Deux conséquences immédiates :

- avec $\alpha=\beta=0$, **$M\,0=0$** : le vecteur nul a toujours pour image le vecteur nul ;
- par récurrence sur le nombre de termes, $M\bigl(\sum_k\lambda_kx_k\bigr)=\sum_k\lambda_k\,Mx_k$ pour toute combinaison finie.

---

## 4bis.3 Applications linéaires : toute matrice en est une, et réciproquement

La proposition précédente dit que $x\mapsto Mx$ **conserve les combinaisons linéaires**. Cette propriété mérite un nom, parce qu'on la rencontrera sur des applications qui ne sont pas données par une matrice — la projection du [module 6](06-projection-orthogonale.md), par exemple, est définie par une propriété géométrique.

> **Définition (application linéaire).** Une application $f:\mathbb R^p\to\mathbb R^n$ est **linéaire** si, pour tous $x,y\in\mathbb R^p$ et tous $\alpha,\beta\in\mathbb R$,
> $$f(\alpha x+\beta y)=\alpha f(x)+\beta f(y)$$

Autrement dit, combiner puis appliquer $f$ donne la même chose qu'appliquer $f$ puis combiner.

| Application de $\mathbb R^n$ dans $\mathbb R^n$ | Linéaire ?                                                                        |
| ----------------------------------------------- | --------------------------------------------------------------------------------- |
| $x\mapsto 2x$                                   | oui                                                                               |
| $x\mapsto Mx$, pour une matrice $M$ $n\times n$ | oui : c'est la proposition du § 4bis.2                                            |
| $x\mapsto x-\bar x\,\mathbf 1$ (le centrage)    | oui, car $\overline{\alpha x+\beta y}=\alpha\bar x+\beta\bar y$                   |
| $x\mapsto x+\mathbf 1$ (une translation)        | **non** : $0\mapsto\mathbf 1\ne 0$                                                |
| $x\mapsto\lVert x\rVert\,\mathbf 1$             | **non** : $-x$ et $x$ ont la même image, alors qu'il faudrait des images opposées |

**La réciproque : toute application linéaire est une matrice.** Notons $e_1,\dots,e_p$ la **base canonique** de $\mathbb R^p$ : $e_j$ a un $1$ en position $j$ et des $0$ ailleurs, de sorte que
$$x=(x_1,\dots,x_p)=x_1e_1+x_2e_2+\dots+x_pe_p$$

> **Proposition.** Soit $f:\mathbb R^p\to\mathbb R^n$ linéaire, et $M$ la matrice $n\times p$ dont la $j$-ième colonne est $f(e_j)$. Alors $f(x)=Mx$ pour tout $x$.

**Démonstration.** Par linéarité de $f$, puis par la lecture par colonnes du § 4bis.2 :
$$f(x)=f\Bigl(\sum_{j=1}^px_je_j\Bigr)=\sum_{j=1}^px_j\,f(e_j)=Mx\qquad\blacksquare$$

La matrice $M$ s'appelle la **matrice de $f$**. Connaître $f$ sur les $p$ vecteurs $e_j$ suffit à la connaître partout : **la matrice n'est que le tableau de ces $p$ images.** Le même argument donne un critère d'égalité qui servira plusieurs fois :

> **Deux matrices $n\times p$ sont égales dès qu'elles ont le même effet sur tout vecteur.** Si $Ax=Bx$ pour tout $x$, alors en prenant $x=e_j$ on obtient $a_j=Ae_j=Be_j=b_j$ : les colonnes coïncident une à une.

**L'identité.** $I_n$ est la matrice de l'application $x\mapsto x$ : ses colonnes sont $e_1,\dots,e_n$ eux-mêmes, et $I_nx=\sum_jx_je_j=x$.

---

## 4bis.4 Le produit de deux matrices

On veut composer : appliquer $B$, puis $A$. Soit $B$ de taille $p\times q$ et $A$ de taille $n\times p$ ; pour $x\in\mathbb R^q$, le vecteur $Bx$ est dans $\mathbb R^p$ et $A(Bx)$ dans $\mathbb R^n$. L'application $x\mapsto A(Bx)$ est linéaire — composée de deux applications qui le sont —, donc elle a une matrice. **C'est elle qu'on appelle $AB$.** Calculons-la.

$$\bigl(A(Bx)\bigr)_i=\sum_{j=1}^p a_{ij}\,(Bx)_j=\sum_{j=1}^p a_{ij}\sum_{k=1}^q b_{jk}\,x_k=\sum_{k=1}^q\Bigl(\sum_{j=1}^p a_{ij}\,b_{jk}\Bigr)x_k$$
La dernière égalité ne fait qu'échanger l'ordre de deux sommes **finies** et regrouper les termes en $x_k$. Le coefficient de $x_k$ est ce qui doit figurer en ligne $i$, colonne $k$ :

> **Définition (produit matriciel).** Pour $A$ de taille $n\times p$ et $B$ de taille $p\times q$, le produit $AB$ est la matrice $n\times q$ de coefficients
> $$(AB)_{ik}=\sum_{j=1}^p a_{ij}\,b_{jk}$$
> et le calcul ci-dessus **démontre** que $(AB)x=A(Bx)$ pour tout $x\in\mathbb R^q$.

⚠️ **La règle des tailles : $(n\times p)(p\times q)=n\times q$.** Les deux tailles **intérieures** doivent coïncider — le nombre de colonnes de $A$ égale le nombre de lignes de $B$ — et disparaissent ; les tailles **extérieures** donnent celle du produit. Le produit $Ax$ du § 4bis.2 en est le cas $q=1$.

**Deux lectures, encore.**

- **Par lignes et colonnes** : $(AB)_{ik}=\langle\,\text{ligne } i \text{ de } A,\ \text{colonne } k \text{ de } B\,\rangle$. C'est la règle de calcul à la main.
- **Par colonnes** : la $k$-ième colonne de $AB$ est $A\,b_k$, l'image par $A$ de la $k$-ième colonne de $B$. En effet, elle vaut $(AB)e_k=A(Be_k)=Ab_k$.

Sur l'exemple, avec $B=\begin{pmatrix}1&1\\0&2\end{pmatrix}$ ($2\times2$) : les colonnes de $AB$ sont $A(1,0)=(1,0,3)$ et $A(1,2)=1\cdot(1,0,3)+2\cdot(2,1,-1)=(5,2,1)$, d'où
$$AB=\begin{pmatrix}1&2\\0&1\\3&-1\end{pmatrix}\begin{pmatrix}1&1\\0&2\end{pmatrix}=\begin{pmatrix}1&5\\0&2\\3&1\end{pmatrix}$$
Contrôle par la règle lignes × colonnes, coefficient $(3,2)$ : $3\cdot1+(-1)\cdot2=1$. Le produit $BA$, lui, **n'existe pas** : $(2\times2)(3\times2)$, les tailles intérieures $2$ et $3$ diffèrent.

**Les règles de calcul, et d'où elles viennent.**

| Règle                                        | Pourquoi elle est vraie                                                               |
| -------------------------------------------- | ------------------------------------------------------------------------------------- |
| $(AB)C=A(BC)$ — **associativité**            | les deux matrices envoient $x$ sur $A(B(Cx))$, donc sont égales (critère du § 4bis.3) |
| $A(B+C)=AB+AC$ et $(A+B)C=AC+BC$             | même argument, avec la linéarité du § 4bis.2 pour la première                         |
| $A(\lambda B)=\lambda(AB)=(\lambda A)B$      | idem                                                                                  |
| $I_nA=A=AI_p$ pour $A$ de taille $n\times p$ | $I_n(Ax)=Ax$ et $A(I_px)=Ax$                                                          |

L'associativité autorise à écrire $ABC$ sans parenthèses, et $A^2=AA$, $A^3=AAA$ pour une matrice carrée. **C'est tout ce qu'il faut pour lire $P^2=P$** au [§ 6.5](06-projection-orthogonale.md) : appliquer $P$ deux fois revient à l'appliquer une fois.

> ⚠️ **Le produit n'est pas commutatif, et un produit peut être nul sans qu'aucun facteur ne le soit.** Même quand $AB$ et $BA$ existent tous deux et ont la même taille, ils diffèrent en général. Avec
> $$C=\begin{pmatrix}0&1\\0&0\end{pmatrix},\quad D=\begin{pmatrix}1&0\\0&0\end{pmatrix}:\qquad CD=\begin{pmatrix}0&0\\0&0\end{pmatrix},\qquad DC=\begin{pmatrix}0&1\\0&0\end{pmatrix}$$
> $CD=0$ alors que $C\ne0$ et $D\ne0$ ; et $DC=C\ne CD$. **Deux réflexes des réels sont donc faux** : on ne peut pas échanger les facteurs, et $AB=0$ n'entraîne pas « $A=0$ ou $B=0$ ». Composer deux opérations dépend de l'ordre dans lequel on les fait — centrer puis mettre à l'échelle n'est pas mettre à l'échelle puis centrer, en général.

---

## 4bis.5 La transposée

> **Définition.** La **transposée** de $A$, de taille $n\times p$, est la matrice $A^{\top}$ de taille $p\times n$ définie par
> $$(A^{\top})_{ij}=a_{ji}$$
> Ses **lignes** sont les colonnes de $A$, dans le même ordre.

$$A=\begin{pmatrix}1&2\\0&1\\3&-1\end{pmatrix}\qquad A^{\top}=\begin{pmatrix}1&0&3\\2&1&-1\end{pmatrix}$$
On trouve aussi la notation $A^T$ ou ${}^tA$ ; le [§ 5.1](05-orthogonalite-et-pythagore.md) écrit $X^T$, c'est le même objet.

**Les règles immédiates.** $(A^{\top})^{\top}=A$, $(A+B)^{\top}=A^{\top}+B^{\top}$ et $(\lambda A)^{\top}=\lambda A^{\top}$ : chacune se vérifie en lisant un coefficient.

> **Proposition.** Pour $A$ de taille $n\times p$ et $B$ de taille $p\times q$ : $(AB)^{\top}=B^{\top}A^{\top}$.

**Démonstration.** Les deux membres sont de taille $q\times n$. Coefficient $(k,i)$ :
$$\bigl((AB)^{\top}\bigr)_{ki}=(AB)_{ik}=\sum_{j=1}^pa_{ij}\,b_{jk}=\sum_{j=1}^p(B^{\top})_{kj}\,(A^{\top})_{ji}=(B^{\top}A^{\top})_{ki}\qquad\blacksquare$$
L'ordre s'inverse, et il ne peut pas en être autrement : $A^{\top}B^{\top}$ n'aurait en général même pas des tailles compatibles. C'est la règle de l'habillage : on enfile la chemise puis la veste, on retire la veste puis la chemise.

**Le produit scalaire est un produit matriciel.** Un vecteur $u\in\mathbb R^n$ est une colonne $n\times1$ ; sa transposée $u^{\top}$ est une **ligne** $1\times n$. Le produit $u^{\top}v$ est donc de taille $1\times1$ — un nombre — et vaut
$$u^{\top}v=\sum_{i=1}^nu_iv_i=\langle u,v\rangle$$
On identifie une matrice $1\times 1$ au réel qu'elle contient. Toute l'écriture matricielle du cours repose sur cette identité.

> **Proposition (passage d'un côté à l'autre).** Pour $A$ de taille $n\times p$, $x\in\mathbb R^p$ et $y\in\mathbb R^n$ :
> $$\langle Ax,\,y\rangle=\langle x,\,A^{\top}y\rangle$$

**Démonstration.** $\langle Ax,y\rangle=(Ax)^{\top}y=x^{\top}A^{\top}y=x^{\top}(A^{\top}y)=\langle x,A^{\top}y\rangle$, par la proposition précédente appliquée à $A$ et à la matrice $p\times1$ qu'est $x$, puis l'associativité. $\blacksquare$

C'est **la** propriété de la transposée : elle fait passer une matrice d'un côté à l'autre du produit scalaire. Le [§ 6.5](06-projection-orthogonale.md) en tire que la symétrie $P^{\top}=P$ caractérise une projection **orthogonale**.

**$A^{\top}u$ : les produits scalaires de $u$ avec les colonnes.** Les lignes de $A^{\top}$ sont les colonnes $a_j$ de $A$ ; par la lecture par lignes du § 4bis.2,
$$A^{\top}u=\bigl(\langle a_1,u\rangle,\ \dots,\ \langle a_p,u\rangle\bigr)$$
D'où l'équivalence que le [§ 5.1](05-orthogonalite-et-pythagore.md) utilise : **$u\perp\text{Vect}(\text{colonnes de }A)\iff A^{\top}u=0$.**

**$A^{\top}A$ : la matrice de Gram des colonnes.** Elle est carrée, $p\times p$, et son coefficient $(j,k)$ est le produit de la ligne $j$ de $A^{\top}$ par la colonne $k$ de $A$ :
$$(A^{\top}A)_{jk}=\langle a_j,a_k\rangle$$
Sur l'exemple, $\langle a_1,a_1\rangle=10$, $\langle a_1,a_2\rangle=2+0-3=-1$, $\langle a_2,a_2\rangle=6$. Et pour $X=(\mathbf 1\ \ t)$ dans $\mathbb R^4$, avec $x=(12,12,14,18)$ :
$$A^{\top}A=\begin{pmatrix}10&-1\\-1&6\end{pmatrix}\qquad X^{\top}X=\begin{pmatrix}\langle\mathbf 1,\mathbf 1\rangle&\langle\mathbf 1,t\rangle\\\langle t,\mathbf 1\rangle&\langle t,t\rangle\end{pmatrix}=\begin{pmatrix}4&10\\10&30\end{pmatrix}\qquad X^{\top}x=\begin{pmatrix}56\\150\end{pmatrix}$$
Ce sont exactement les nombres des **équations normales** $4a+10b=56$, $10a+30b=150$ du [§ 6.4](06-projection-orthogonale.md). La matrice de covariance du [module 11](11-covariance-et-produit-scalaire.md) est de cette forme.

> **Définition.** Une matrice carrée est **symétrique** si $A^{\top}=A$, c'est-à-dire $a_{ij}=a_{ji}$ : elle est inchangée par réflexion autour de sa diagonale.

$A^{\top}A$ est toujours symétrique : $(A^{\top}A)^{\top}=A^{\top}(A^{\top})^{\top}=A^{\top}A$. On le voyait déjà sur ses coefficients, puisque $\langle a_j,a_k\rangle=\langle a_k,a_j\rangle$.

**Le produit $uv^{\top}$.** À l'inverse de $u^{\top}v$, qui est un nombre, $uv^{\top}$ est une matrice $n\times n$ — une colonne fois une ligne — de coefficients $(uv^{\top})_{ij}=u_iv_j$. Par associativité, pour tout $x$ :
$$(uv^{\top})\,x=u\,(v^{\top}x)=\langle v,x\rangle\,u$$
Deux cas reviennent sans cesse :

- $J=\mathbf 1\mathbf 1^{\top}$ est la matrice remplie de $1$, et $Jx=\langle\mathbf 1,x\rangle\,\mathbf 1=\bigl(\sum_ix_i\bigr)\mathbf 1=n\,\bar x\,\mathbf 1$. Donc $\frac1nJ\,x=\bar x\,\mathbf 1$ : **la moyenne répétée $n$ fois est un produit matriciel**, et $I_n-\frac1nJ$ est la matrice de centrage du [module 8](08-degres-de-liberte-et-centrage.md).
- $uu^{\top}x=\langle u,x\rangle\,u$ : au dénominateur $\|u\|^2$ près, c'est la formule de la projection sur une droite du [§ 6.2](06-projection-orthogonale.md). C'est la clé de l'exercice E6.2.

---

## 4bis.6 Matrices carrées : trace, inverse, rang

### La trace

> **Définition.** La **trace** d'une matrice carrée $A$ de taille $n\times n$ est la somme de ses coefficients diagonaux :
> $$\operatorname{tr}(A)=\sum_{i=1}^na_{ii}$$

Elle est linéaire, $\operatorname{tr}(\alpha A+\beta B)=\alpha\operatorname{tr}(A)+\beta\operatorname{tr}(B)$, et $\operatorname{tr}(I_n)=n$.

> **Proposition.** Pour $A$ de taille $n\times p$ et $B$ de taille $p\times n$ — de sorte que $AB$ ($n\times n$) et $BA$ ($p\times p$) sont carrées toutes deux :
> $$\operatorname{tr}(AB)=\operatorname{tr}(BA)$$

**Démonstration.** On écrit les deux traces et on échange l'ordre de deux sommes finies :
$$\operatorname{tr}(AB)=\sum_{i=1}^n(AB)_{ii}=\sum_{i=1}^n\sum_{j=1}^pa_{ij}\,b_{ji}=\sum_{j=1}^p\sum_{i=1}^nb_{ji}\,a_{ij}=\sum_{j=1}^p(BA)_{jj}=\operatorname{tr}(BA)\qquad\blacksquare$$

C'est remarquable parce que $AB\ne BA$ en général — ils n'ont parfois même pas la même taille — et que leurs traces coïncident pourtant toujours. ⚠️ Avec trois facteurs, seules les **permutations circulaires** sont permises : $\operatorname{tr}(ABC)=\operatorname{tr}(BCA)=\operatorname{tr}(CAB)$, mais pas $\operatorname{tr}(BAC)$ en général.

Le [§ 6.5](06-projection-orthogonale.md) y lira la dimension d'un sous-espace : pour un projecteur orthogonal, **la trace vaut le rang**.

### L'inverse

> **Définition.** Une matrice **carrée** $A$ de taille $n\times n$ est **inversible** s'il existe une matrice $B$ de taille $n\times n$ telle que
> $$AB=BA=I_n$$
> Une telle $B$ est alors **unique** ; on la note $A^{-1}$, l'**inverse** de $A$.

**Unicité.** Si $B$ et $B'$ conviennent toutes deux, alors par associativité
$$B=B\,I_n=B\,(AB')=(BA)\,B'=I_n\,B'=B'\qquad\blacksquare$$

**Ce que l'inverse permet : résoudre.** Si $A$ est inversible, l'équation $Ax=b$ a **une et une seule** solution, $x=A^{-1}b$. Elle en est une, car $A(A^{-1}b)=(AA^{-1})b=b$ ; et c'est la seule, car $Ax=b$ entraîne $x=A^{-1}(Ax)=A^{-1}b$.

**Les règles, démontrées par simple vérification** — l'unicité autorise à conclure dès qu'on a exhibé une matrice qui convient :

| Règle                                        | Vérification                                                                                             |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| $(A^{-1})^{-1}=A$                            | $A^{-1}A=AA^{-1}=I_n$ : la définition est symétrique en $A$ et $A^{-1}$                                  |
| $(AB)^{-1}=B^{-1}A^{-1}$                     | $(AB)(B^{-1}A^{-1})=A\,(BB^{-1})\,A^{-1}=AA^{-1}=I_n$, et de même dans l'autre sens                      |
| $(A^{\top})^{-1}=(A^{-1})^{\top}$            | $A^{\top}(A^{-1})^{\top}=(A^{-1}A)^{\top}=I_n^{\top}=I_n$ (§ 4bis.5), et de même dans l'autre sens       |

L'ordre s'inverse encore dans la deuxième ligne, pour la même raison que pour la transposée.

> ⚠️ **Toutes les matrices carrées non nulles ne sont pas inversibles.** Et seules les matrices **carrées** peuvent l'être au sens de la définition : $X$, de taille $4\times2$, n'a pas d'inverse ; $X^{\top}X$, de taille $2\times2$, peut en avoir une.

> **Proposition.** Si $Ax=0$ pour un $x\ne 0$, alors $A$ n'est pas inversible. Autrement dit : **si $A$ est inversible, ses colonnes forment une famille libre.**

**Démonstration.** Si $A$ était inversible, on aurait $x=A^{-1}(Ax)=A^{-1}0=0$, contradiction. Et par la lecture par colonnes, $Ax=\sum_jx_ja_j$ : un $x\ne0$ tel que $Ax=0$ est exactement une combinaison nulle des colonnes à coefficients non tous nuls, c'est-à-dire une famille de colonnes **liée** ([§ 4.3](04-sous-espaces-et-familles-generatrices.md)). $\blacksquare$

Exemple : $K=\begin{pmatrix}1&1\\1&1\end{pmatrix}$ envoie $(1,-1)$ sur $0$ — ses deux colonnes sont égales —, donc $K$ n'est pas inversible.

**La réciproque est vraie aussi** : une matrice carrée dont les colonnes sont libres est inversible. Elle demande un comptage de dimensions, et découle du théorème du rang du [module 7](07-supplementaire-orthogonal-et-dimension.md) ; on l'admet ici. D'où le critère complet, pour $A$ carrée :
$$A\text{ inversible}\iff\text{colonnes de }A\text{ libres}\iff\bigl(Ax=0\Rightarrow x=0\bigr)$$

**Le cas $2\times2$, explicitement.** Pour $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$, un produit direct donne
$$\begin{pmatrix}a&b\\c&d\end{pmatrix}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}=\begin{pmatrix}ad-bc&0\\0&ad-bc\end{pmatrix}=(ad-bc)\,I_2$$
Donc, si $ad-bc\ne0$,
$$A^{-1}=\frac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$$
(la vérification $BA=I_2$ est identique). Le nombre $ad-bc$ est le **déterminant** de $A$. Si $ad-bc=0$, les colonnes sont proportionnelles et $A$ n'est pas inversible — c'est le cas de $K$.

**Application : les équations normales.** Avec $X^{\top}X=\begin{pmatrix}4&10\\10&30\end{pmatrix}$, le déterminant vaut $4\cdot30-10\cdot10=20\ne0$, et
$$\begin{pmatrix}a\\b\end{pmatrix}=(X^{\top}X)^{-1}X^{\top}x=\frac1{20}\begin{pmatrix}30&-10\\-10&4\end{pmatrix}\begin{pmatrix}56\\150\end{pmatrix}=\frac1{20}\begin{pmatrix}1680-1500\\-560+600\end{pmatrix}=\begin{pmatrix}9\\2\end{pmatrix}$$
C'est la droite $\hat x_i=9+2i$ du § 5.1, retrouvée par un seul produit matriciel.

> **Proposition.** Si les colonnes de $A$ ($n\times p$) sont libres, alors $A^{\top}A$ est inversible.

**Démonstration.** $A^{\top}A$ est carrée ; par le critère, il suffit de montrer que $A^{\top}A\lambda=0$ entraîne $\lambda=0$. Si $A^{\top}A\lambda=0$, alors
$$0=\lambda^{\top}A^{\top}A\lambda=(A\lambda)^{\top}(A\lambda)=\|A\lambda\|^2$$
donc $A\lambda=0$, c'est-à-dire $\sum_j\lambda_ja_j=0$ ; les colonnes étant libres, $\lambda=0$. $\blacksquare$

C'est ce qui donne un sens au $A(A^{\top}A)^{-1}A^{\top}$ de la simulation [S6.2](06-projection-orthogonale.md), et à l'énoncé du [§ 11.5](11-covariance-et-produit-scalaire.md) : une matrice de covariance est inversible exactement quand les séries centrées sont libres. La démonstration utilise la réciproque admise ; le sens « non inversible ⇒ colonnes liées » est, lui, entièrement démontré.

### Le rang

> **Définition.** Le **rang** d'une matrice $A$ est la dimension du sous-espace engendré par ses colonnes :
> $$\operatorname{rang}(A)=\dim\text{Vect}(a_1,\dots,a_p)$$

Au sens du [§ 4.3](04-sous-espaces-et-familles-generatrices.md) : c'est le nombre de colonnes d'une sous-famille libre et génératrice. Il ne dépasse ni $p$ (le nombre de générateurs majore la dimension) ni $n$ (on est dans $\mathbb R^n$). $\operatorname{rang}(A)=p$ exactement quand les colonnes sont libres ; pour $A$ carrée, cela revient à dire que $A$ est inversible. C'est la fonction `np.linalg.matrix_rank` de la simulation [S4.1](04-sous-espaces-et-familles-generatrices.md), et le [module 7](07-supplementaire-orthogonal-et-dimension.md) en fait un théorème.

---

> 📐 **Ce que ce module ne contient pas.**
> - **Le déterminant en dimension quelconque.** Seul le cas $2\times2$ est donné. Le [module 9](09-bases-orthonormees-et-isometries.md) n'en utilise que le signe, et le [cours de dérivation](../analyse/derivation-et-integration/08-integrales-multiples-et-jacobien.md) le reprend comme facteur de volume.
> - **Les valeurs propres.** Un vecteur $w\ne0$ tel que $Aw=\lambda w$ est un **vecteur propre** de $A$, et $\lambda$ sa **valeur propre** : $A$ ne fait qu'étirer la direction de $w$. Les simulations des modules [8](08-degres-de-liberte-et-centrage.md) et [11](11-covariance-et-produit-scalaire.md) les affichent ; le théorème qui les gouverne pour une matrice symétrique est démontré au [module 12](12-analyse-en-composantes-principales.md).

---

## 4bis.7 Simulation

### S4bis.1 — Chaque règle, vérifiée sur des nombres

```python
import numpy as np

A = np.array([[1.0, 2], [0, 1], [3, -1]])       # 3 x 2
x = np.array([2.0, 1])

# le produit Ax, par ses trois écritures
print("A @ x            :", A @ x)
print("par les colonnes :", x[0] * A[:, 0] + x[1] * A[:, 1])
print("par les lignes   :", np.array([A[i] @ x for i in range(3)]))

# linéarité
rng = np.random.default_rng(0)
M = rng.normal(size=(4, 3))
u, v = rng.normal(size=(2, 3))
a, b = 2.5, -1.3
print("M(au+bv) = aMu+bMv :", np.allclose(M @ (a * u + b * v), a * (M @ u) + b * (M @ v)))

# produit : composition, et non-commutativité
B = np.array([[1.0, 1], [0, 2]])
print("AB =\n", A @ B)
print("(AB)x = A(Bx)  :", np.allclose((A @ B) @ x, A @ (B @ x)))
C = np.array([[0.0, 1], [0, 0]])
D = np.array([[1.0, 0], [0, 0]])
print("CD =\n", C @ D, "\nDC =\n", D @ C)

# transposée
N = rng.normal(size=(3, 5))
print("(MN)^T = N^T M^T :", np.allclose((M @ N).T, N.T @ M.T))
y = rng.normal(size=4)
print("<Mu,y> = <u,M^T y> :", np.isclose((M @ u) @ y, u @ (M.T @ y)))

# trace : tr(MP) = tr(PM) alors que les deux produits n'ont pas la même taille
P = rng.normal(size=(3, 4))
print("tailles MP, PM :", (M @ P).shape, (P @ M).shape)
print("tr(MP) = tr(PM) :", np.isclose(np.trace(M @ P), np.trace(P @ M)))

# les équations normales du § 5.1, résolues par l'inverse
t = np.arange(1.0, 5)
X = np.column_stack([np.ones(4), t])
xs = np.array([12.0, 12, 14, 18])
print("X^T X =\n", X.T @ X, "\nX^T x =", X.T @ xs)
print("(a, b) =", np.linalg.inv(X.T @ X) @ (X.T @ xs))
print("rangs de X et de K :", np.linalg.matrix_rank(X), np.linalg.matrix_rank(np.ones((2, 2))))
```

La dernière ligne de coefficients doit afficher $(9,2)$ : la droite ajustée du § 5.1. En pratique, on n'inverse pas une matrice pour résoudre un système — `np.linalg.solve(X.T @ X, X.T @ xs)` fait le même travail plus vite et plus précisément —, mais l'inverse est la bonne écriture pour **raisonner**.

---

## 4bis.8 Exercices

**E4bis.1.** Calculer $AB$ et $BA$ pour $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$ et $B=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, une fois par la règle lignes × colonnes, une fois par la lecture par colonnes. *Décrire en mots ce que fait $B$ à une matrice selon qu'on la multiplie à gauche ou à droite.*

**E4bis.2.** Soit $u,v\in\mathbb R^n$. Montrer que $\operatorname{tr}(uv^{\top})=\langle u,v\rangle$, de deux façons : par les coefficients, puis par la proposition $\operatorname{tr}(AB)=\operatorname{tr}(BA)$. *Que vaut $\operatorname{tr}(J)$ ?*

**E4bis.3.** Montrer que $M=I_n-\frac1nJ$ vérifie $Mx=x-\bar x\,\mathbf 1$. *En déduire, sans aucun calcul supplémentaire, que le centrage est une application linéaire, et donner $\operatorname{tr}(M)$.*

**E4bis.4.** Montrer que si $A$ est carrée, inversible, et vérifie $A^2=A$, alors $A=I_n$. *Qu'en conclut-on sur un projecteur qui ne serait pas l'identité ? (Piste : multiplier $A^2=A$ par $A^{-1}$.)*

**E4bis.5.** Soit $A$ de taille $n\times p$. Montrer que le **noyau** $\ker A=\{x\in\mathbb R^p:\ Ax=0\}$ est un sous-espace de $\mathbb R^p$, en n'utilisant que la linéarité du § 4bis.2. *Le décrire pour $A=K=\begin{pmatrix}1&1\\1&1\end{pmatrix}$.*

**E4bis.6.** Une application $g:\mathbb R^n\to\mathbb R^n$ de la forme $g(x)=Ax+b$, avec $b\ne0$, est dite **affine**. Montrer qu'elle n'est pas linéaire. *La mise en « base 100 » d'une série de cours, $x\mapsto 100\,x/x_1$, est-elle linéaire ? Et le passage des cours aux écarts à la première séance, $x\mapsto x-x_1\mathbf 1$ ?*

**E4bis.7 — orientée finance.** Un portefeuille détient $w=(w_1,\dots,w_p)$ titres de $p$ valeurs, dont les clôtures sur $n$ séances sont rangées en colonnes d'une matrice $C$ de taille $n\times p$. *Que représente le vecteur $Cw$ ? Sa taille ? Et pourquoi le fait que ce soit une combinaison linéaire des colonnes impose-t-il des **dates alignées** entre les $p$ séries ([§ 1.1](01-espace-vectoriel.md)) ?*

---

## 4bis.9 À retenir

- **Une matrice $n\times p$, c'est $p$ vecteurs de $\mathbb R^n$ rangés en colonnes.** Le coefficient $a_{ij}$ est en ligne $i$, colonne $j$.
- **$Ax=\sum_jx_ja_j$** : le produit est une combinaison linéaire des colonnes, de coefficients les coordonnées de $x$. Chaque coordonnée $(Ax)_i$ est le produit scalaire de la ligne $i$ avec $x$.
- **$M(\alpha x+\beta y)=\alpha Mx+\beta My$**, parce qu'aucune coordonnée de $x$ n'y est multipliée par une autre. Toute application linéaire est une matrice, dont la $j$-ième colonne est l'image de $e_j$.
- **$AB$ est la matrice de « appliquer $B$, puis $A$ »** : $(n\times p)(p\times q)=n\times q$. Associatif, **pas commutatif**, et $AB=0$ n'entraîne pas $A=0$ ou $B=0$.
- **$(AB)^{\top}=B^{\top}A^{\top}$, $\langle u,v\rangle=u^{\top}v$, $\langle Ax,y\rangle=\langle x,A^{\top}y\rangle$.** $A^{\top}u$ rassemble les produits scalaires de $u$ avec les colonnes ; $A^{\top}A$ rassemble ceux des colonnes entre elles.
- **$\operatorname{tr}(AB)=\operatorname{tr}(BA)$**, même quand $AB\ne BA$.
- **$A$ carrée est inversible $\iff$ ses colonnes sont libres $\iff$ $Ax=0$ n'a que la solution $0$.** $(AB)^{-1}=B^{-1}A^{-1}$ ; et $A^{\top}A$ est inversible dès que les colonnes de $A$ sont libres.

---

⬅️ [Module 4 — Sous-espaces, Vect et familles génératrices](04-sous-espaces-et-familles-generatrices.md) ·
➡️ [Module 5 — Orthogonalité et Pythagore](05-orthogonalite-et-pythagore.md) ·
🏠 [Sommaire](README.md)
