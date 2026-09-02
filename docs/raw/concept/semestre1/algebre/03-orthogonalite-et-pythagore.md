# Module 3 — Orthogonalité et théorème de Pythagore

**Durée : 45 min.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) et [2](02-cauchy-schwarz-et-angle.md).

> **La question traitée.** Que se passe-t-il quand le terme croisé $2\langle u,v\rangle$ de  l'identité de développement s'annule ?

**Ce qui est en jeu.** Toute « décomposition de la variance » de la statistique — somme des
carrés totale = expliquée + résiduelle — est une instance de ce module, et d'aucun autre.

---

## 3.1 Définition

> **Définition.** $u\perp v \iff \langle u,v\rangle=0$.

Dans le vocabulaire du [module 2](02-cauchy-schwarz-et-angle.md), c'est le cas $\theta=90°$. Le vecteur nul est orthogonal à tout le monde ; c'est le seul vecteur orthogonal à lui-même (par la propriété « définie positive » du § 1.1).

**Orthogonalité à un sous-espace.** $u\perp F$ signifie $u\perp f$ pour **tout** $f\in F$. Par bilinéarité, il suffit de le vérifier sur une famille génératrice de $F$ : c'est ce qui rend la vérification praticable.

> **Définition.** Une famille $g_1,\dots,g_m$ de vecteurs de $F$ est **génératrice** de $F$ si tout élément de $F$ est une combinaison linéaire des $g_i$ : $F=\text{Vect}(g_1,\dots,g_m)$.

**Exemple.** Dans $\mathbb R^n$ — l'espace d'une série de $n$ observations —, posons $\mathbf 1=(1,1,\dots,1)$ et $t=(1,2,\dots,n)$. Alors :

| Sous-espace                | Ce qu'il contient                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| $\text{Vect}(\mathbf 1)$   | $\{\lambda\mathbf 1:\lambda\in\mathbb R\}$ — les séries **constantes**, une droite       |
| $\text{Vect}(t)$           | $\{\mu t:\mu\in\mathbb R\}$ — les séries **proportionnelles au temps**, une autre droite |
| $\text{Vect}(\mathbf 1,t)$ | $\{a\mathbf 1+bt\}$ — les séries **affines** $(a+bi)_{i=1,\dots,n}$, un plan             |

Le troisième est le sous-espace du cours : la droite ajustée d'une série de clôtures est
l'élément de $\text{Vect}(\mathbf 1,t)$ le plus proche de cette série ([module 4](04-projection-orthogonale.md)) — deux paramètres, $a$ et $b$, pour un plan de dimension 2 dans un espace de dimension $n$. Et la proposition ci-dessous y prend un sens concret : $u\perp\text{Vect}(\mathbf 1,t)$ ne demande que **deux** vérifications, $\sum_iu_i=0$ et $\sum_i i\,u_i=0$, au lieu d'une infinité.

Une telle famille est un **jeu de paramètres** pour $F$ : elle le décrit tout entier par un nombre fini de vecteurs, sans être tenue d'être libre — un $g_i$ redondant ne retire rien au caractère générateur, il rend seulement l'écriture non unique. Une famille génératrice **et** libre est une base ; c'est le cas particulier où l'écriture est unique.

Ainsi, dans $\mathbb R^2$, $\text{Vect}\bigl((1,0),(0,1),(1,1)\bigr)=\mathbb R^2$ : la famille est génératrice, mais le troisième vecteur est de trop, et $(2,3)$ s'y écrit de deux façons — $2(1,0)+3(0,1)$ ou $(1,0)+2(0,1)+(1,1)$. Retirer $(1,1)$ ne change rien à l'espace engendré et rend l'écriture unique : on obtient une base.

> **Proposition.** Soit $g_1,\dots,g_m$ une famille génératrice de $F$. Alors
> $$u\perp F\quad\Longleftrightarrow\quad \langle u,g_i\rangle=0\ \text{ pour tout } i\in\{1,\dots,m\}$$

**Démonstration.** Les deux sens, dont un seul demande un calcul.

*Sens direct ($\Rightarrow$).* Chaque $g_i$ est un vecteur **de** $F$. L'hypothèse $u\perp F$ portant sur *tout* $f\in F$, il suffit de l'appliquer à $f=g_i$, ce qui donne $\langle u,g_i\rangle=0$. Ce sens n'utilise pas que la famille engendre $F$, seulement qu'elle y vit.

*Réciproque ($\Leftarrow$).* C'est le sens utile, et le seul où le caractère générateur sert.
Donnons-nous $f\in F$ **quelconque**. Par définition d'une famille génératrice, il existe des
réels $\lambda_1,\dots,\lambda_m$ tels que $f=\sum_{i=1}^m\lambda_ig_i$. La **linéarité à droite** du produit scalaire (§ 1.1 — la moitié de la bilinéarité que la symétrie offre gratuitement), étendue de deux à $m$ termes par récurrence immédiate, permet de sortir la somme du crochet :
$$\langle u,f\rangle=\Bigl\langle u,\;\sum_{i=1}^m\lambda_ig_i\Bigr\rangle
=\sum_{i=1}^m\lambda_i\,\langle u,g_i\rangle
=\sum_{i=1}^m\lambda_i\cdot 0=0$$
Le vecteur $f$ étant arbitraire dans $F$, on a bien $u\perp F$. $\blacksquare$

Deux remarques sur cette démonstration :

- **Les $\lambda_i$ n'ont pas à être uniques.** Seule leur *existence* a servi : si $f$ admet deux décompositions, l'une et l'autre donnent $0$. C'est pourquoi la famille n'a pas besoin d'être libre — une base convient, mais n'est pas requise.
- **Un seul produit scalaire non nul ruine tout.** Si $\langle u,g_j\rangle=c\neq 0$, alors $g_j$ est lui-même un $f\in F$ avec $\langle u,f\rangle=c$ : l'équivalence est stricte, il n'y a pas de $u$ « presque orthogonal » à $F$.

> 🔑 **Une infinité de vérifications se ramène à $m$ produits scalaires.** $F$ est infini dès qu'il n'est pas $\{0\}$ ; la proposition remplace « pour tout $f\in F$ » par $m$ égalités numériques. C'est exactement le mécanisme réutilisé au § 3.2 pour l'hérédité — où $S$ est engendré par $w_1,\dots,w_{k-1}$ — et au [module 4](04-projection-orthogonale.md) pour caractériser la projection.

**Exemple — un vecteur orthogonal à $\text{Vect}(\mathbf 1)$.** C'est le cas $m=1$, avec $g_1=\mathbf 1$ : la proposition dit que $u\perp\text{Vect}(\mathbf 1)$ se ramène à **une seule** égalité,
$$\langle u,\mathbf 1\rangle=\sum_{i=1}^n u_i\cdot 1=\sum_{i=1}^n u_i=0$$
Prenons dans $\mathbb R^4$ le vecteur $u=(-2,\,0,\,-1,\,3)$, dont la somme des composantes est bien nulle. La proposition affirme qu'il est orthogonal à la droite $\text{Vect}(\mathbf 1)$ **tout entière**, et la réciproque le redonne à la main : pour $f=\lambda\mathbf 1$ quelconque,
$$\langle u,\lambda\mathbf 1\rangle=\lambda\langle u,\mathbf 1\rangle=\lambda\cdot 0=0$$
Une addition de quatre nombres a couvert une infinité de vecteurs $f$.

Ce $u$ n'est pas tombé du ciel : c'est le vecteur **centré** de la série $x=(10,\,12,\,11,\,15)$, de moyenne $\bar x=12$, soit $u=x-\bar x\mathbf 1$. Ce n'est pas une coïncidence — *tout* vecteur centré est orthogonal à $\mathbf 1$, puisque $\sum_i(x_i-\bar x)=\sum_ix_i-n\bar x=0$ par définition de la moyenne. C'est l'objet de l'exercice E3.2, la décomposition $x=\bar x\mathbf 1+\tilde x$ du § 3.4, et tout le [module 6](06-degres-de-liberte-et-centrage.md).

À l'inverse, $v=(1,\,1,\,2,\,-1)$ n'est **pas** orthogonal à $\text{Vect}(\mathbf 1)$ : $\langle v,\mathbf 1\rangle=3\neq0$. Conformément à la seconde remarque, un seul produit scalaire non nul suffit à le disqualifier, et le témoin est $\mathbf 1$ lui-même.

**Exemple — un vecteur orthogonal à $\text{Vect}(\mathbf 1,t)$.** Cette fois $m=2$, et la proposition demande **deux** égalités, une par générateur :
$$\langle u,\mathbf 1\rangle=\sum_{i=1}^n u_i=0
\qquad\text{et}\qquad
\langle u,t\rangle=\sum_{i=1}^n i\,u_i=0$$
Toujours dans $\mathbb R^4$, avec $t=(1,2,3,4)$, prenons $u=(1,\,-1,\,-1,\,1)$ : sa somme est nulle, et $1-2-3+4=0$ également. Pour un élément quelconque $f=a\mathbf 1+bt$ du plan, la réciproque donne alors
$$\langle u,f\rangle=a\,\langle u,\mathbf 1\rangle+b\,\langle u,t\rangle=a\cdot 0+b\cdot 0=0$$
et ce, pour **tout** couple $(a,b)$ — deux additions ont couvert un plan entier.

> ⚠️ **Plus le sous-espace grandit, plus son orthogonal rétrécit.** $\text{Vect}(\mathbf 1)\subset\text{Vect}(\mathbf 1,t)$, donc être orthogonal au second est **plus** exigeant. Le $u=(-2,\,0,\,-1,\,3)$ de l'exemple précédent le montre : il passe la première condition, mais $\langle u,t\rangle=-2+0-3+12=7\neq 0$ — orthogonal à la droite $\text{Vect}(\mathbf 1)$, pas au plan $\text{Vect}(\mathbf 1,t)$.

D'où vient ce $u$, là encore : c'est le **résidu** d'un ajustement affine. La série $x=(12,\,12,\,14,\,18)$ a pour droite des moindres carrés $\hat x_i=9+2i$, soit $\hat x=9\,\mathbf 1+2\,t=(11,\,13,\,15,\,17)$, et $u=x-\hat x=(1,\,-1,\,-1,\,1)$. Que le résidu soit orthogonal aux **deux** générateurs n'est pas un hasard de cet exemple : c'est la définition même de l'ajustement au sens des moindres carrés — ce sont ses *équations normales*, démontrées au [module 4](04-projection-orthogonale.md). Le § 3.1 en donne déjà la moitié pratique : il n'y a que deux produits scalaires à annuler, quel que soit $n$.

---

## 3.2 Le théorème

> **Théorème de Pythagore.**
> $$u\perp v\quad\Longleftrightarrow\quad \|u+v\|^2=\|u\|^2+\|v\|^2$$

**Démonstration.** Immédiate par développement (§ 1.2) : $\|u+v\|^2=\|u\|^2+2\langle u,v\rangle+\|v\|^2$. Le terme croisé disparaît si et seulement si $\langle u,v\rangle=0$. $\blacksquare$

Notez bien que dans $\mathbb R^n$ c'est une **équivalence**, pas une simple implication : la réciproque du Pythagore scolaire est ici gratuite.

**Généralisation à une famille orthogonale.** Si $w_1,\dots,w_k$ sont deux à deux orthogonaux :

$$\Big\|\sum_{j=1}^k w_j\Big\|^2=\sum_{j=1}^k\|w_j\|^2$$

**Démonstration par récurrence sur $k$.**

*Initialisation.* Pour $k=1$, l'énoncé se réduit à $\|w_1\|^2=\|w_1\|^2$. Le rang $k=2$ est
exactement le théorème du § 3.2.

*Hérédité.* Supposons le résultat acquis au rang $k-1$ **pour toute** famille orthogonale de
$k-1$ vecteurs, et donnons-nous $w_1,\dots,w_k$ deux à deux orthogonaux. Posons
$$S=\sum_{j=1}^{k-1}w_j,\qquad\text{de sorte que}\qquad \sum_{j=1}^{k}w_j=S+w_k$$

**Le seul point à établir est $S\perp w_k$**, et il n'est pas donné par l'hypothèse : $S$ n'est aucun des $w_j$, c'est un vecteur nouveau, dont rien ne dit *a priori* qu'il est orthogonal à $w_k$. C'est la **linéarité à gauche** du produit scalaire (§ 1.1) qui le donne — le produit scalaire d'une somme est la somme des produits scalaires :
$$\langle S,\,w_k\rangle=\Bigl\langle \sum_{j=1}^{k-1}w_j,\;w_k\Bigr\rangle
=\sum_{j=1}^{k-1}\langle w_j,w_k\rangle=0$$
chacun des $k-1$ termes étant nul par l'hypothèse d'orthogonalité **deux à deux** : c'est ici, et
nulle part ailleurs, qu'elle sert. C'est aussi le mécanisme annoncé au § 3.1 — être orthogonal à
une famille génératrice suffit à l'être à tout ce qu'elle engendre, et $S$ appartient à l'espace engendré par $w_1,\dots,w_{k-1}$.

Le théorème du § 3.2 s'applique alors au **couple** $(S,w_k)$ :
$$\Bigl\|\sum_{j=1}^{k}w_j\Bigr\|^2=\|S+w_k\|^2=\|S\|^2+\|w_k\|^2$$
Enfin $w_1,\dots,w_{k-1}$ est encore deux à deux orthogonale — une sous-famille d'une famille
orthogonale l'est —, donc l'hypothèse de récurrence s'y applique et donne $\|S\|^2=\sum_{j<k}\|w_j\|^2$ :
$$\Bigl\|\sum_{j=1}^{k}w_j\Bigr\|^2=\sum_{j=1}^{k-1}\|w_j\|^2+\|w_k\|^2=\sum_{j=1}^{k}\|w_j\|^2
\qquad\blacksquare$$

> ⚠️ **Au-delà de deux vecteurs, ce n'est plus une équivalence.** Le développement complet fait
> apparaître **tous** les termes croisés :
> $$\Bigl\|\sum_{j=1}^k w_j\Bigr\|^2=\sum_{j=1}^k\|w_j\|^2+2\sum_{i<j}\langle w_i,w_j\rangle$$
> L'égalité de Pythagore équivaut donc à l'annulation de la **somme** des termes croisés, pas de  chacun d'eux. Contre-exemple dans $\mathbb R^2$ : $w_1=(1,0)$, $w_2=(0,1)$, $w_3=(1,-1)$ ont  pour termes croisés $0$, $1$ et $-1$, de somme nulle ; l'identité tient bien — $\|(2,0)\|^2=4$ et $1+1+2=4$ — alors que $w_1$ et $w_3$ ne sont **pas** orthogonaux. La réciproque gratuite du § 3.2 est un privilège du couple.

---

## 3.3 Familles orthogonales et indépendance linéaire

> **Définition.** Une famille $w_1,\dots,w_k$ est **libre** — on dit aussi *linéairement indépendante* — si la seule combinaison linéaire qui donne le vecteur nul est celle dont **tous** les coefficients sont nuls:
>$$\sum_{j=1}^k\lambda_jw_j=0\quad\Longrightarrow\quad\lambda_1=\dots=\lambda_k=0$$
> Une famille qui ne l'est pas est dite **liée**.

Trois formulations du même fait :
- **aucune redondance** — aucun $w_j$ ne s'écrit comme combinaison des autres ; s'il le faisait, l'isoler produirait une relation nulle à coefficients non tous nuls ;
- **écriture unique** — tout vecteur de $\text{Vect}(w_1,\dots,w_k)$ s'y décompose d'une seule façon. C'est précisément ce qui manquait à la famille génératrice quelconque du § 3.1, où seule l'*existence* des coefficients était acquise ;
- **libre et génératrice = base**, le cas où les deux qualités sont réunies.

> **Proposition.** Une famille orthogonale de vecteurs **non nuls** est libre.

**Démonstration.** Si $\sum_j \lambda_j w_j=0$, le produit scalaire des deux membres avec $w_k$ donne $\lambda_k\|w_k\|^2=0$ — tous les autres termes s'annulent par orthogonalité — donc $\lambda_k=0$. $\blacksquare$

> ⚠️ **« Non nuls » est une hypothèse, pas un ornement.** Le vecteur nul est orthogonal à tout le
> monde (§ 3.1) : $\{w_1,0\}$ est donc une famille orthogonale parfaitement valide, et **liée**,
> puisque $1\cdot 0=0$ est une relation à coefficient non nul. La démonstration le fait voir à
> l'endroit exact où elle s'appuie dessus : de $\lambda_k\|w_k\|^2=0$ on ne conclut $\lambda_k=0$
> que si $\|w_k\|^2\neq0$, c'est-à-dire $w_k\neq0$ — la propriété « définie positive » du § 1.1.

> 🔑 **L'orthogonalité est une forme forte, et vérifiable en un produit scalaire, de  l'indépendance linéaire.** C'est ce qui la rend commode : prouver qu'une famille est libre
> demande en général de résoudre un système ; ici, il suffit de $k(k-1)/2$ produits scalaires
> nuls.

---

## 3.4 Ce que le théorème devient sur des données

> 🔑 **Toute « décomposition de la variance » est un Pythagore.** Somme des carrés totale = somme des carrés expliquée + somme des carrés résiduelle : ce n'est pas une identité algébrique
> fortuite, c'est Pythagore appliqué à une décomposition orthogonale.

Deux occurrences que vous rencontrerez :

| Identité statistique                                              | Ce qu'elle est réellement                                                                             |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| König–Huygens $\sum_i(x_i-\bar x)^2=\sum_i x_i^2-n\bar x^2$       | Pythagore sur $x=\bar x\mathbf 1+\tilde x$ — [module 5](05-supplementaire-orthogonal-et-dimension.md) |
| Table d'ANOVA : $SC_{\text{tot}}=SC_{\text{exp}}+SC_{\text{rés}}$ | Pythagore sur $y=P_F(y)+(y-P_F(y))$ — [module 4](04-projection-orthogonale.md)                        |

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

La ligne centrale est la plus parlante : **l'écart à Pythagore vaut exactement le terme croisé**. Le théorème ne dit rien d'autre.

---

## 3.6 Exercices

**E3.1.** Montrer que si $u\perp v$ alors $\|u-v\|=\|u+v\|$. *Interpréter avec les diagonales d'un parallélogramme (voir E1.2).*

**E3.2.** Soit $\mathbf 1=(1,\dots,1)$. Caractériser les vecteurs $u$ tels que $u\perp\mathbf 1$.
*(Réponse : $\sum_i u_i=0$.)* **C'est l'ensemble le plus important de tout le cours** — voir le
[module 5](05-supplementaire-orthogonal-et-dimension.md).

**E3.3.** Retrouver König–Huygens $\sum_i(x_i-\bar x)^2=\sum_i x_i^2-n\bar x^2$ **par Pythagore seul**, sans développer le carré. *(Piste : admettre provisoirement que $x-\bar x\mathbf 1$ est orthogonal à $\bar x\mathbf 1$ — l'exercice E3.2 le donne.) Comparer la longueur des deux démonstrations.*

**E3.4.** Montrer qu'une famille orthogonale de $\mathbb R^n$ comporte au plus $n$ vecteurs non nuls. *Quel résultat du § 3.3 utilise-t-on ?*

**E3.5.** Deux vecteurs sont orthogonaux ; leur somme peut-elle être de norme inférieure à
chacun d'eux ? *Justifier par le théorème, puis par un dessin en dimension 2.*

---

## 3.7 À retenir

- **$u\perp v\iff\langle u,v\rangle=0$** ; orthogonal à $F$ = orthogonal à une famille
  génératrice de $F$ — une famille finie dont les combinaisons linéaires remplissent $F$.
- **Pythagore $\|u+v\|^2=\|u\|^2+\|v\|^2\iff u\perp v$** — une **équivalence**, et sa démonstration tient en une ligne de développement.
- **L'écart à Pythagore est le terme croisé** $2\langle u,v\rangle$.
- **La généralisation à $k$ termes n'est qu'une implication** : au-delà du couple, l'identité
  n'exige que l'annulation de la **somme** des termes croisés.
- **Une famille orthogonale de vecteurs non nuls est libre** — libre : la seule combinaison
  linéaire nulle est celle à coefficients tous nuls. L'hypothèse « non nuls » est nécessaire, le
  vecteur nul étant orthogonal à tout.
- Toute décomposition de la variance en statistique est une instance de ce théorème.

---

⬅️ [Module 2 — Cauchy–Schwarz et l'angle](02-cauchy-schwarz-et-angle.md) ·
➡️ [Module 4 — La projection orthogonale](04-projection-orthogonale.md) ·
🏠 [Sommaire](README.md)
