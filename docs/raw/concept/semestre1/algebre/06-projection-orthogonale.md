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

**Dimension.** Le nombre $d$ de générateurs n'est pas la dimension de $\text{Vect}(u_1,\dots,u_d)$ : il la majore ([§ 4.3](04-sous-espaces-et-familles-generatrices.md)). Les deux coïncident exactement quand la famille est **libre** — et le [§ 5.3](05-orthogonalite-et-pythagore.md) donne un critère commode pour s'en assurer : une famille orthogonale de vecteurs non nuls est libre. C'est ce que le § 6.4 exploite en travaillant dans une base orthogonale.

> 🔑 **C'est la stabilité qui garantit une réponse.** Sur une partie quelconque de $\mathbb R^n$ — une sphère, un segment, un ensemble fini — « l'élément le plus proche de $x$ » peut ne pas exister, ou en exister plusieurs. Le § 6.3 montre que sur un sous-espace il existe et qu'il est unique, et la démonstration n'invoque rien d'autre que la stabilité et Pythagore.

---

## 6.2 Projection sur une droite

> **Définition.** Soit $u\ne 0$ et $D=\text{Vect}(u)$. On appelle **projection orthogonale** de $x$ sur $D$ tout vecteur $p\in D$ tel que $x-p\perp D$.

La définition ne dit pas qu'un tel vecteur existe, ni qu'il n'y en a qu'un : c'est ce qu'il faut établir avant d'écrire « **la** projection » et de la noter comme une fonction de $x$.

> **Proposition.** La projection orthogonale de $x$ sur $D$ existe et elle est unique ; on la note $p(x)$, et
> $$p(x)=\frac{\langle x,u\rangle}{\|u\|^2}\,u$$

**Démonstration.** Un élément de $D$ s'écrit $\lambda u$. Être orthogonal à $D$ revient à être orthogonal à $u$ seul, puisque $\langle x-\lambda u,\;\mu u\rangle=\mu\,\langle x-\lambda u,\;u\rangle$ pour tout $\mu$. La condition s'écrit donc
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

**Une définition, une caractérisation.** « Le résidu est orthogonal » est la définition du § 6.2 ; « la distance est minimale » est le théorème ci-dessus, et il désigne le même vecteur. La première est commode pour **calculer**, la seconde pour **comprendre**.

---

## 6.4 Projection sur un sous-espace quelconque

Les § 6.2 et §6.3 ont traité une droite. On passe maintenant à un sous-espace $F$ de dimension quelconque — le plan $\text{Vect}(\mathbf 1,t)$ de la droite ajustée en est le premier exemple. Le chemin est le même, en quatre temps : **définir**, montrer que la réponse est **unique**, montrer qu'elle est **la plus proche**, puis la **calculer**. Seul le dernier temps demande une hypothèse sur la façon dont on décrit $F$.

**Définition.** Elle ne change pas d'un mot, $D$ devient $F$ :

> **Définition.** On appelle **projection orthogonale** de $x$ sur $F$ tout vecteur $p\in F$ tel que $x-p\perp F$.

Et le [§ 5.1](05-orthogonalite-et-pythagore.md) la rend vérifiable : si $F=\text{Vect}(g_1,\dots,g_m)$, la condition $x-p\perp F$ se ramène à $m$ égalités $\langle x-p,\,g_k\rangle=0$.

**Unicité — sans aucun calcul.** Supposons que $p$ et $p'$ conviennent tous deux. Alors :

- $p-p'\in F$, puisque $p$ et $p'$ sont dans $F$ et que $F$ est **stable** ;
- $p-p'=(x-p')-(x-p)$ est orthogonal à $F$, comme différence de deux vecteurs qui le sont.

Le vecteur $p-p'$ est donc orthogonal à tout $F$, et en particulier **à lui-même** : $\|p-p'\|^2=0$, donc $p=p'$. $\blacksquare$ Dès qu'elle existe, on peut donc parler de **la** projection et la noter $P_F(x)$.

**Meilleure approximation — la démonstration du § 6.3, recopiée.** Pour tout $y\in F$, $\|x-y\|\ge\|x-P_F(x)\|$, avec égalité si et seulement si $y=P_F(x)$. Relisez la démonstration du § 6.3 en remplaçant $D$ par $F$ : elle n'utilise que deux faits, $x-P_F(x)\perp F$ (la définition) et $P_F(x)-y\in F$ (la stabilité). Ni la dimension de $F$, ni une base n'y interviennent.

**Calcul — le cas d'une base orthogonale.** Reste l'existence, et pour l'établir il faut *construire* $p$. Supposons d'abord que $F$ possède une base $(w_1,\dots,w_d)$ **orthogonale** : $\langle w_j,w_k\rangle=0$ pour $j\ne k$, et aucun $w_j$ nul. On cherche $p$ sous la forme $p=\sum_j\lambda_jw_j$ — tout élément de $F$ s'écrit ainsi — et la condition d'orthogonalité, testée sur chaque $w_k$, s'écrit
$$\langle x,w_k\rangle-\sum_{j=1}^d\lambda_j\,\langle w_j,w_k\rangle=0\qquad k=1,\dots,d$$
Dans la somme, **tous les termes $j\ne k$ sont nuls** par orthogonalité ; il ne reste que $j=k$ :
$$\langle x,w_k\rangle-\lambda_k\,\|w_k\|^2=0\quad\Longleftrightarrow\quad\lambda_k=\frac{\langle x,w_k\rangle}{\|w_k\|^2}$$
Chaque équation ne contient qu'une inconnue, et c'est **exactement** l'équation du § 6.2. D'où l'existence, et la formule :
$$P_F(x)=\sum_{j=1}^d\frac{\langle x,w_j\rangle}{\|w_j\|^2}\,w_j$$
C'est la formule de la droite, appliquée à chaque direction et sommée. $\blacksquare$

**Et en base orthonormée, le dénominateur disparaît.** Si de plus chaque vecteur est de norme $1$ — on note alors la base $(e_1,\dots,e_d)$ —, chaque $\|e_j\|^2$ vaut $1$ et
$$P_F(x)=\sum_{j=1}^d \langle x,e_j\rangle\,e_j$$
Le dénominateur n'a pas été oublié : il vaut $1$. On résume souvent les deux conditions « orthogonaux deux à deux » et « de norme $1$ » par $\langle e_j,e_k\rangle=\delta_{jk}$, où le **symbole de Kronecker** $\delta_{jk}$ vaut $1$ si $j=k$ et $0$ sinon. La formule du § 6.2 elle-même est de ce type : avec $e=u/\|u\|$,
$$\langle x,e\rangle\,e=\Bigl\langle x,\frac{u}{\|u\|}\Bigr\rangle\frac{u}{\|u\|}=\frac{\langle x,u\rangle}{\|u\|^2}\,u$$
le $\|u\|^2$ du § 6.2 est simplement **caché dans la normalisation**.

**Sans orthogonalité, les équations se couplent.** Si la base $(w_1,\dots,w_d)$ n'est pas orthogonale, aucun terme de la somme ne disparaît : les $d$ équations
$$\sum_{j=1}^d\lambda_j\,\langle w_j,w_k\rangle=\langle x,w_k\rangle\qquad k=1,\dots,d$$
forment un **système** où chaque inconnue apparaît partout. Les $w_j$ rangés en colonnes d'une matrice $A$, elles s'écrivent $A^{\top}A\,\lambda=A^{\top}x$, soit $A^{\top}(x-A\lambda)=0$ : ce sont les **équations normales** annoncées au [§ 5.1](05-orthogonalite-et-pythagore.md). On peut les résoudre directement — c'est le $A(A^{\top}A)^{-1}A^{\top}$ de la simulation S6.2 —, ou d'abord **orthogonaliser** la base ; le [module 9](09-bases-orthonormees-et-isometries.md) montre (Gram–Schmidt) que c'est toujours possible, ce qui établit l'existence de $P_F(x)$ pour **tout** sous-espace.

**Exemple — la droite ajustée du § 5.1.** Dans $\mathbb R^4$, $x=(12,\,12,\,14,\,18)$, $F=\text{Vect}(\mathbf 1,t)$ avec $t=(1,2,3,4)$. La base $(\mathbf 1,t)$ n'est **pas** orthogonale : $\langle\mathbf 1,t\rangle=1+2+3+4=10\ne 0$. Il faut donc commencer par en fabriquer une qui le soit.

**Étape 1 — orthogonaliser la base.** On remplace $t$ par le $t$ **centré**, c'est-à-dire par $t$ privé de sa projection sur $\mathbf 1$ :

- $\bar t=\dfrac{\sum_{i=1}^4 i}{4}=\dfrac{5}{2}$, donc $w=t-\bar t\,\mathbf 1=\left(-\frac{3}{2},\,-\frac{1}{2},\,\frac{1}{2},\,\frac{3}{2}\right)$ ;
- $\langle\mathbf 1,w\rangle=\sum_i(i-\bar t)=0$ : la nouvelle base $(\mathbf 1,w)$ est orthogonale, ce qui est exactement ce qu'exige la formule ;
- et $\text{Vect}(\mathbf 1,w)=\text{Vect}(\mathbf 1,t)$, car $w$ s'obtient de $t$ en lui retranchant un multiple de $\mathbf 1$, et $t=w+\bar t\,\mathbf 1$ le redonne. **Le sous-espace n'a pas changé, seule sa description a changé.**

Les deux normes dont la formule a besoin :
$$\|\mathbf 1\|^2=\sum_{i=1}^4 1=4
\qquad
\|w\|^2=\sum_i(i-\bar t)^2=\tfrac94+\tfrac14+\tfrac14+\tfrac94=5$$

**Étape 2 — la composante sur $\mathbf 1$.** Avec $\langle x,\mathbf 1\rangle=12+12+14+18=56$ :
$$P_{\mathbf 1}(x)=\frac{\langle x,\mathbf 1\rangle}{\|\mathbf 1\|^2}\,\mathbf 1=\frac{56}{4}\,\mathbf 1=14\,\mathbf 1$$

**Étape 3 — la composante sur $w$.** Avec $\langle x,w\rangle=-\frac{36}{2}-\frac{12}{2}+\frac{14}{2}+\frac{54}{2}=10$ :
$$P_w(x)=\frac{\langle x,w\rangle}{\|w\|^2}\,w=\frac{10}{5}\,w=2\,w$$

**Étape 4 — sommer, puis revenir aux coordonnées.** La formule additionne les deux composantes :
$$P_F(x)=14\,\mathbf 1+2\,w$$
Cette écriture donne le projeté **dans la base $(\mathbf 1,w)$** : elle dit *combien* de $\mathbf 1$ et *combien* de $w$, pas ce que valent les quatre nombres. Pour les obtenir, on remplace $\mathbf 1$ et $w$ par leurs coordonnées et on calcule composante par composante :
$$14\,\mathbf 1+2\,w
=14\,(1,\,1,\,1,\,1)+2\left(-\tfrac32,\,-\tfrac12,\,\tfrac12,\,\tfrac32\right)
=(14-3,\;14-1,\;14+1,\;14+3)
=(11,\,13,\,15,\,17)$$
Autrement dit, la $i$-ème composante vaut
$$14+2\left(i-\tfrac52\right)=14+2i-5=9+2i$$
— c'est bien une **droite** en $i$, celle du § 5.1 : $\hat x_i=9+2i$. On lit au passage les coefficients dans la base de départ : $P_F(x)=14\,\mathbf 1+2(t-\tfrac52\mathbf 1)=9\,\mathbf 1+2\,t$, soit une ordonnée à l'origine de $9$ et une pente de $2$. L'orthogonalisation a servi au **calcul** ; le résultat, lui, se relit dans la base que l'on veut.

**Contrôle.** Le résidu $x-P_F(x)=(1,\,-1,\,-1,\,1)$ doit être orthogonal aux deux générateurs de $F$ ([§ 5.1](05-orthogonalite-et-pythagore.md)) : $1-1-1+1=0$ et $1-2-3+4=0$. C'est le $u$ du § 5.1, et il l'est.

> ⚠️ **Sauter l'étape 1 donne un résultat faux.** Appliquer la formule directement à $(\mathbf 1,t)$, qui n'est pas orthogonale, donnerait $\frac{56}{4}\mathbf 1+\frac{150}{30}t=14\,\mathbf 1+5\,t=(19,\,24,\,29,\,34)$ — un vecteur de $F$, mais pas le plus proche de $x$ : son résidu $(-7,-12,-15,-16)$ n'est orthogonal ni à $\mathbf 1$ ni à $t$. C'est l'objet de l'exercice E6.4.

Rien n'obligeait à orthogonaliser : on pouvait aussi résoudre directement les équations normales $4a+10b=56$ et $10a+30b=150$, qui donnent $a=9$, $b=2$. Mais ces deux équations **se résolvent ensemble**, alors que les étapes 2 et 3 ci-dessus se calculent **chacune seule**, avec son propre dénominateur $\|w_j\|^2$.

> 🔑 **L'orthogonalité de la base ne sert qu'au calcul.** L'unicité et la propriété de meilleure approximation valent pour n'importe quel sous-espace, décrit comme on veut. Une base orthogonale transforme un système de $d$ équations couplées en $d$ projections sur des droites, indépendantes ; une base orthonormée supprime en plus les dénominateurs.

**Et si l'on cherchait $F$ lui-même ? — l'analyse en composantes principales.** Tout ce module suppose $F$ **donné** : $\text{Vect}(\mathbf 1,t)$ parce que l'axe du temps est connu d'avance. Renversons l'hypothèse — donnons-nous $N$ vecteurs $x_1,\dots,x_N$ et cherchons le sous-espace de dimension $d$ qui les approche tous au mieux :
$$\min_{\dim F=d}\ \sum_{i=1}^{N}\bigl\|x_i-P_F(x_i)\bigr\|^2$$
La quantité placée sous ce minimum est exactement celle que le § 6.3 sait déjà rendre minimale ; ce qui reste — **le choix de $F$** — s'appelle l'**analyse en composantes principales** ([module 12](12-analyse-en-composantes-principales.md)), et sa réponse est la base orthonormée des vecteurs propres de la matrice de covariance ([module 11](11-covariance-et-produit-scalaire.md)). L'ACP n'est donc pas une autre projection : c'est le **problème inverse**, qui choisit le sous-espace au lieu de le recevoir. Le statut de la base s'en trouve renversé — ici l'orthogonalisation est un moyen de calcul, et **n'importe quelle** base orthogonale de $F$ rend le même $P_F(x)$ ; en ACP la base *est* le résultat, elle est ordonnée, et tronquer à $d$ vecteurs change $F$.

> ⚠️ **La droite ajustée de [`modele.md`](../../../modele.md) n'est pas le premier axe principal du nuage $(t_i,v_i)$.** La projection de ce module vit dans $\mathbb R^n$, l'espace des **observations** : le résidu s'y mesure **verticalement**, parce que $t$ est exact et que seul $v$ porte l'écart. L'ACP du nuage de points dans le plan minimiserait la distance **perpendiculaire** à la droite, en traitant les deux coordonnées symétriquement — et cette seconde droite n'est même pas invariante d'unité : coter en centimes plutôt qu'en euros la déplace, alors que les moindres carrés donnent la même droite relue dans la nouvelle unité. Pour `VAL_n`, `CORR_n` et `T_n` d'[`import_societe.py`](../../../../../python/import_societe.md), c'est la première qu'il faut.

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
- **$p(x)=\frac{\langle x,u\rangle}{\|u\|^2}u$** sur une droite ; $P_F(x)=\sum_j\frac{\langle x,w_j\rangle}{\|w_j\|^2}w_j$ sur un sous-espace **en base orthogonale**, et $\sum_j\langle x,e_j\rangle e_j$ en base orthonormée, où chaque dénominateur vaut $1$.
- **Sans base orthogonale**, les coefficients sont couplés : ils résolvent les équations normales $A^{\top}A\lambda=A^{\top}x$.
- **Le résidu est orthogonal au sous-espace** — c'est la définition opérationnelle.
- ⭐ **La projection est le point le plus proche** : les moindres carrés ne sont que cela.
- **$P^{\top}=P$ et $P^2=P$** caractérisent un projecteur orthogonal.
- **$\operatorname{tr}(P)=\operatorname{rang}(P)=\dim F$** : les dimensions se lisent sur la trace.

---

⬅️ [Module 5 — Orthogonalité et Pythagore](05-orthogonalite-et-pythagore.md) ·
➡️ [Module 7 — Supplémentaire orthogonal et dimension](07-supplementaire-orthogonal-et-dimension.md) ·
🏠 [Sommaire](README.md)
