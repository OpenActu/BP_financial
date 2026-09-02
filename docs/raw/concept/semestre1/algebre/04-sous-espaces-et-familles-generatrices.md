# Module 4 — Sous-espaces, $\text{Vect}$ et familles génératrices

**Durée : 45 min.** Prérequis : [module 1](01-espace-vectoriel.md), qu'il prolonge directement. **Ce module n'utilise pas le produit scalaire** : il est purement linéaire, et c'est précisément ce qui fait sa portée — tout ce qu'il établit reste vrai avant qu'on ait choisi une géométrie.

> **La question traitée.** Les modules qui suivent parlent sans cesse de « la droite $\text{Vect}(\mathbf 1)$ », du « plan $\text{Vect}(\mathbf 1,t)$ », d'« être orthogonal à un sous-espace ». Que sont exactement ces objets — et comment décrit-on un ensemble **infini** de vecteurs par une liste **finie** ?

**Ce qui est en jeu.** La droite des moindres carrés d'une série de clôtures est *l'élément de $\text{Vect}(\mathbf 1,t)$ le plus proche de cette série*. Tant que $\text{Vect}$ n'est pas défini, cette phrase — qui est l'énoncé du [module 6](06-projection-orthogonale.md) et le contenu de [`modele.md`](../../../modele.md) — n'a pas de sens. Ce module est court parce qu'il ne démontre presque rien ; il est placé avant les autres parce que sans lui, ils ne s'énoncent pas.

---

## 4.1 Sous-espace vectoriel

> **Définition (sous-espace vectoriel).** Une partie $F\subseteq\mathbb R^n$ est un **sous-espace vectoriel** si elle est non vide et **stable par combinaison linéaire** :
> $$y,z\in F\ \text{ et }\ \alpha,\beta\in\mathbb R\quad\Longrightarrow\quad \alpha y+\beta z\in F$$

Prendre $\alpha=\beta=0$ montre qu'un sous-espace **contient toujours $0$** ; « non vide et stable » et « contient $0$ et stable » sont donc deux formulations de la même chose. Il n'y a rien d'autre à retenir : la stabilité est, à elle seule, tout ce que les modules suivants utiliseront de $F$ — au [§ 6.3](06-projection-orthogonale.md), c'est elle qui autorise à dire que $p(x)-y$ appartient encore à $F$.

Quelques exemples, et un contre-exemple, à garder en tête :

| Partie de $\mathbb R^n$                                 | Sous-espace ?                                                              |
| ------------------------------------------------------- | -------------------------------------------------------------------------- |
| $\{0\}$ et $\mathbb R^n$ lui-même                       | Oui — les deux cas extrêmes, toujours licites                              |
| $\{u:\sum_i u_i=0\}$, les vecteurs de **somme nulle**   | Oui — une somme de sommes nulles est nulle                                 |
| $\{\lambda u:\lambda\in\mathbb R\}$ pour $u$ fixé       | Oui — c'est la droite dirigée par $u$                                      |
| $\{u:\sum_i u_i=1\}$, les vecteurs de **somme $1$**     | **Non** — il ne contient pas $0$, et la somme de deux éléments en sort     |

> ⚠️ **« Sous-espace » n'est pas « sous-ensemble », et un sous-espace passe toujours par l'origine.** Une droite du plan qui ne passe pas par $0$ n'est pas un sous-espace. Cela n'a rien de contradictoire avec la régression : la droite d'équation $v=v_0+rt$ est **affine dans le plan $(t,v)$**, mais le vecteur $v_0\mathbf 1+r\,t$ qu'elle produit vit dans $\mathbb R^n$, où il appartient bel et bien au sous-espace $\text{Vect}(\mathbf 1,t)$. Le sous-espace n'est pas la droite qu'on dessine ; c'est l'ensemble des **séries de $n$ valeurs** qu'une telle droite peut engendrer.

---

## 4.2 Le sous-espace engendré : $\text{Vect}$

Un sous-espace est défini par une propriété — « stable » — qu'on ne peut pas vérifier vecteur par vecteur, puisqu'il y en a une infinité. La construction suivante renverse le problème : elle **fabrique** un sous-espace à partir d'une liste finie.

> **Définition (sous-espace engendré).** Pour $u_1,\dots,u_d\in\mathbb R^n$,
> $$\text{Vect}(u_1,\dots,u_d)=\bigl\{\lambda_1u_1+\dots+\lambda_du_d\ :\ \lambda_1,\dots,\lambda_d\in\mathbb R\bigr\}$$
> — l'ensemble de **toutes** leurs combinaisons linéaires.

**C'est bien un sous-espace.** Une combinaison linéaire de combinaisons linéaires des $u_j$ est encore une combinaison linéaire des $u_j$, en regroupant les coefficients :
$$\alpha\sum_{j=1}^d\lambda_ju_j+\beta\sum_{j=1}^d\mu_ju_j=\sum_{j=1}^d(\alpha\lambda_j+\beta\mu_j)\,u_j$$

**Et c'est le plus petit qui contienne les $u_j$.** Soit $G$ un sous-espace contenant $u_1,\dots,u_d$. Par stabilité, $G$ contient chacune de leurs combinaisons linéaires, donc $\text{Vect}(u_1,\dots,u_d)\subseteq G$. D'où le nom : le sous-espace **engendré** par $u_1,\dots,u_d$ est le plus économique de tous ceux qui les contiennent.

**Le cas $d=1$ — la droite.** $\text{Vect}(u)=\{\lambda u:\lambda\in\mathbb R\}$ est la **droite** passant par l'origine et dirigée par $u$. L'hypothèse $u\ne 0$ y est indispensable, et pour une raison de géométrie avant d'être de calcul : $\text{Vect}(0)=\{0\}$ est un sous-espace parfaitement légitime, mais réduit à un point — ce n'est pas une droite, et aucune direction n'y est en jeu.

**Le cas $d=2$ — le plan.** $\text{Vect}(u,v)$ est le plan contenant $u$, $v$ et l'origine — *pourvu que $u$ et $v$ ne soient pas colinéaires* (au sens du [§ 3.1](03-cauchy-schwarz-et-angle.md)). S'ils le sont, les deux vecteurs décrivent la même droite et $\text{Vect}(u,v)$ est cette droite. **Le nombre de générateurs ne dit donc pas la dimension : il la majore**, et le § 4.3 explique ce qui sépare les deux.

---

## 4.3 Famille génératrice

> **Définition.** Une famille $g_1,\dots,g_m$ de vecteurs de $F$ est **génératrice** de $F$ si tout élément de $F$ est une combinaison linéaire des $g_i$ :
> $$F=\text{Vect}(g_1,\dots,g_m)$$

Une telle famille est un **jeu de paramètres** pour $F$ : elle le décrit tout entier par un nombre fini de vecteurs. C'est le seul moyen de manipuler un ensemble infini, et c'est ce qui rend calculables les énoncés des modules suivants — le [§ 5.1](05-orthogonalite-et-pythagore.md) ramènera « $u$ est orthogonal à tout $f\in F$ » à $m$ produits scalaires nuls, un par générateur.

**Ce qu'une famille génératrice garantit, et ce qu'elle ne garantit pas.** Elle garantit l'**existence** des coefficients $\lambda_i$ ; elle ne dit rien de leur **unicité**. Une famille génératrice n'est pas tenue d'être minimale : un $g_i$ redondant ne retire rien au caractère générateur, il rend seulement l'écriture non unique.

Ainsi, dans $\mathbb R^2$, $\text{Vect}\bigl((1,0),(0,1),(1,1)\bigr)=\mathbb R^2$ : la famille est génératrice, mais le troisième vecteur est de trop, et $(2,3)$ s'y écrit de deux façons —
$$(2,3)=2(1,0)+3(0,1)=1(1,0)+2(0,1)+1(1,1)$$
Retirer $(1,1)$ ne change rien à l'espace engendré et rend l'écriture unique.

> **Définition (rappel anticipé).** Une famille est **libre** lorsque la seule combinaison linéaire qui donne $0$ est celle à coefficients tous nuls ; une famille **libre et génératrice** est une **base**, et c'est exactement le cas où l'écriture de chaque élément est unique. Le [§ 5.3](05-orthogonalite-et-pythagore.md) reprend cette définition et en donne un critère commode : *une famille orthogonale de vecteurs non nuls est libre*.

**Dimension.** Le nombre $d$ de générateurs n'est pas la dimension de $\text{Vect}(u_1,\dots,u_d)$ : il la majore, et les deux coïncident exactement quand la famille est libre. La dimension elle-même est traitée au [module 7](07-supplementaire-orthogonal-et-dimension.md), où elle devient l'outil de comptage des degrés de liberté.

> 🔑 **Générateur et libre sont deux qualités indépendantes, et opposées.** Ajouter un vecteur ne peut qu'aider à engendrer et que nuire à la liberté ; en retirer un fait l'inverse. Une base est le point d'équilibre — assez de vecteurs pour tout atteindre, pas un de trop.

---

## 4.4 Les sous-espaces de tout le cours

Ils sont peu nombreux, et ce sont toujours les mêmes. Dans $\mathbb R^n$ — l'espace d'une série de $n$ observations —, avec $\mathbf 1=(1,1,\dots,1)$ et $t=(1,2,\dots,n)$ :

| Sous-espace                         | Ce qu'il contient                                                         | Où il sert                                                            |
| ----------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| $\text{Vect}(\mathbf 1)$            | $\{\lambda\mathbf 1\}$ — les séries **constantes**, une droite            | la moyenne — [module 8](08-degres-de-liberte-et-centrage.md)          |
| $\text{Vect}(t)$                    | $\{\mu t\}$ — les séries **proportionnelles au temps**, une autre droite  | rarement seule, mais elle éclaire la précédente                       |
| $\text{Vect}(\mathbf 1,t)$          | $\{a\mathbf 1+bt\}$ — les séries **affines** $(a+bi)_{i=1,\dots,n}$       | la droite des moindres carrés — [`modele.md`](../../../modele.md)     |
| $\text{Vect}(\mathbf 1)^{\perp}$    | les vecteurs de **somme nulle** ($^{\perp}$ : [module 5](05-orthogonalite-et-pythagore.md)) | les écarts à la moyenne, les $n-1$ degrés de liberté     |
| $\text{Vect}(\text{colonnes de }A)$ | les ajustements atteignables                                              | la régression multiple — [§ 6.6](06-projection-orthogonale.md)        |

Le troisième est **le** sous-espace du cours. Deux paramètres, $a$ et $b$, décrivent un plan de dimension $2$ logé dans un espace de dimension $n$ : c'est tout l'écart entre une série quelconque de $n$ clôtures et la droite qu'on lui ajuste.

> 🔑 **Choisir un modèle linéaire, c'est choisir un sous-espace — rien de plus.** « Ajuster une constante » est le choix de $\text{Vect}(\mathbf 1)$, « ajuster une droite » celui de $\text{Vect}(\mathbf 1,t)$, « ajuster $p$ variables explicatives » celui de $\text{Vect}(\text{colonnes de }A)$. La méthode qui suit — projeter — est la **même** dans les trois cas ; seul le sous-espace change. C'est ce qui explique qu'un seul module, le [module 6](06-projection-orthogonale.md), suffise à traiter toutes les régressions du dépôt.

---

## 4.5 Simulation

### S4.1 — Engendrer, appartenir, être redondant

```python
import numpy as np

n = 8
un = np.ones(n)
t = np.arange(1.0, n + 1)

G2 = np.column_stack([un, t])                    # deux générateurs
G3 = np.column_stack([un, t, 3 * un - 2 * t])    # le troisième est de trop

# « v appartient à Vect(G) » : l'ajouter aux générateurs n'augmente pas le rang
rang = np.linalg.matrix_rank
dans = lambda G, v: rang(np.column_stack([G, v])) == rang(G)

print("rangs :", rang(G2), rang(G3))             # 2 et 2 : le même plan

x = 9 * un + 2 * t                               # une série affine
y = np.array([12.0, 12, 14, 18, 13, 15, 20, 19]) # une série quelconque
print("x dans Vect(1,t) :", dans(G2, x))
print("y dans Vect(1,t) :", dans(G2, y))

# même espace engendré : chaque générateur de l'un est dans l'autre
print("Vect(G3) = Vect(G2) :", all(dans(G2, g) for g in G3.T))

# la redondance ne coûte que l'unicité de l'écriture
c1 = np.array([9.0, 2.0, 0.0])
c2 = np.array([12.0, 0.0, -1.0])
print("deux écritures de x :", np.allclose(G3 @ c1, x), np.allclose(G3 @ c2, x))
```

Les deux dernières lignes sont le § 4.3 en action : `G3` engendre exactement le même plan que `G2`, mais $x$ y admet **deux** jeux de coefficients. Rien n'est faux ; simplement, « les coefficients de $x$ » n'est plus une expression bien définie.

---

## 4.6 Exercices

**E4.1.** Montrer que l'intersection de deux sous-espaces est un sous-espace. *Puis montrer, par un contre-exemple dans $\mathbb R^2$, que leur réunion n'en est généralement pas un.*

**E4.2.** Démontrer que $\text{Vect}(u_1,\dots,u_d)$ est le plus petit sous-espace contenant $u_1,\dots,u_d$, au sens de l'inclusion. *(La démonstration du § 4.2 tient en deux lignes : les réécrire sans les relire.)*

**E4.3.** Soit $t=(1,\dots,n)$ et $\bar t$ sa moyenne. Montrer que $\text{Vect}(\mathbf 1,t)=\text{Vect}(\mathbf 1,\,t-\bar t\,\mathbf 1)$. *Les deux familles engendrent le même plan ; qu'est-ce que la seconde a de mieux ? (Piste : calculer $\langle\mathbf 1,\,t-\bar t\,\mathbf 1\rangle$ — la notion est au [§ 5.1](05-orthogonalite-et-pythagore.md), le bénéfice au [§ 6.4](06-projection-orthogonale.md).)*

**E4.4.** Déterminer $\text{Vect}(\mathbf 1)\cap\{u\in\mathbb R^n:\sum_i u_i=0\}$. *(Réponse : $\{0\}$.) En déduire qu'aucun vecteur constant non nul n'est de somme nulle — l'énoncé sera réutilisé tel quel au [module 7](07-supplementaire-orthogonal-et-dimension.md).*

**E4.5.** Les colonnes d'une matrice $A$ de taille $n\times p$ engendrent $\text{Vect}(\text{colonnes de }A)\subseteq\mathbb R^n$. *Que vaut ce sous-espace si deux colonnes de $A$ sont identiques ? Et si $p>n$ ?*

**E4.6 — orientée finance.** Prendre 20 clôtures consécutives dans un CSV de `docs/raw/data/quotes/`, poser $t=(1,\dots,20)$ et calculer la droite des moindres carrés $\hat x=a\mathbf 1+b\,t$. *Vérifier avec le critère de rang du § 4.5 que $\hat x$ appartient à $\text{Vect}(\mathbf 1,t)$ et que le résidu $x-\hat x$ n'y appartient pas — sauf si le résidu est nul. Que signifierait un résidu nul sur des cours de bourse ?*

---

## 4.7 À retenir

- **Sous-espace = non vide et stable par combinaison linéaire.** Il contient donc $0$ : un sous-espace passe toujours par l'origine, un sous-ensemble quelconque non.
- **$\text{Vect}(u_1,\dots,u_d)$ est l'ensemble de toutes les combinaisons linéaires** des $u_j$ — le plus petit sous-espace qui les contienne.
- **Une famille génératrice décrit un ensemble infini par une liste finie**, et c'est le seul point qui compte : elle garantit l'**existence** des coefficients, jamais leur unicité.
- **Le nombre de générateurs majore la dimension** ; les deux coïncident quand la famille est libre — une famille libre et génératrice est une **base**.
- **Choisir un modèle linéaire, c'est choisir un sous-espace.** $\text{Vect}(\mathbf 1)$ pour la moyenne, $\text{Vect}(\mathbf 1,t)$ pour la droite ajustée, les colonnes de $A$ pour la régression multiple.

---

⬅️ [Module 3 — Cauchy–Schwarz et l'angle](03-cauchy-schwarz-et-angle.md) ·
➡️ [Module 5 — Orthogonalité et Pythagore](05-orthogonalite-et-pythagore.md) ·
🏠 [Sommaire](README.md)
