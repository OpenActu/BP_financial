# Module 8 — La covariance comme produit scalaire ⭐

**Durée : 1 h 15.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) à[7](07-dictionnaire-geometrique-des-statistiques.md). **Module de sortie du cours.**

> **La question traitée.** Le [module 7](07-dictionnaire-geometrique-des-statistiques.md) affirme que $\operatorname{Cov}(x,y)=\frac1n\langle\tilde x,\tilde y\rangle$. Est-ce une **notation
> commode**, ou la covariance **est-elle** un produit scalaire, au sens exact des trois propriétés
> du § 1.1 ?

**Ce qui est en jeu.** La réponse est « presque » — et le « presque » est instructif. Une fois
la vérification faite, quatre résultats de statistique tombent **sans aucun calcul nouveau** :
$|\rho|\le1$, la variance d'un portefeuille, la positivité d'une matrice de covariance, et les
contraintes qu'une corrélation impose aux autres.

---

## 8.1 Le préalable : le centrage

La covariance ne porte pas sur $x$ mais sur son **vecteur centré** $\tilde x = x-\bar x\,\mathbf 1$, qui est le résidu de la projection sur $\text{Vect}(\mathbf 1)$ ([§ 5.2](05-supplementaire-orthogonal-et-dimension.md)). Matriciellement, $\tilde x = Mx$ avec $M=I_n-\frac1nJ$ la matrice de centrage.

Les vecteurs centrés vivent donc tous dans l'hyperplan

$$H=\text{Vect}(\mathbf 1)^\perp=\Bigl\{u\in\mathbb R^n:\ \sum_i u_i=0\Bigr\},
\qquad \dim H = n-1$$

> 🔑 **Toute la statistique descriptive à deux variables se joue dans $H$, pas dans
> $\mathbb R^n$.** La moyenne a été retirée : ce qui reste est la seule dispersion. Retenir cela
> évite la moitié des confusions du module.

⚠️ Le centrage est une **application linéaire** ($M$ est une matrice) et **idempotente**
($M^2=M$) : centrer un vecteur déjà centré ne fait rien. C'est ce qui rend légitime tout ce qui
suit.

---

## 8.2 La vérification ⭐

Posons, pour $x,y\in\mathbb R^n$ :

$$c(x,y)\;=\;\operatorname{Cov}(x,y)\;=\;\frac{1}{n}\langle \tilde x,\tilde y\rangle
\;=\;\frac1n\,x^{\top}M y$$

*(La dernière écriture utilise $M^{\top}M=M^2=M$ : centrer les deux vecteurs ou un seul revient
au même.)*

Reprenons les trois propriétés du [§ 1.1](01-produit-scalaire-et-norme.md), une par une.

| Propriété            | La covariance la vérifie-t-elle ? | Pourquoi                                                                                                                     |
| -------------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Symétrie**         | ✅                                 | $\langle\tilde x,\tilde y\rangle=\langle\tilde y,\tilde x\rangle$                                                            |
| **Bilinéarité**      | ✅                                 | $x\mapsto\tilde x$ est **linéaire**, et $\langle\cdot,\cdot\rangle$ est bilinéaire                                           |
| **Définie positive** | ⚠️ **positive, mais PAS définie** | $\operatorname{Cov}(x,x)=\frac{\lVert\tilde x\rVert^2}{n}\ge 0$, mais elle s'annule dès que $x$ est **constant** — pas seulement nul |

**Le détail qui compte.** $\operatorname{Var}(x)=0$ signifie $\tilde x=0$, c'est-à-dire
$x=c\,\mathbf 1$ : une série **constante**, pas une série nulle. Le « noyau » de la covariance
n'est donc pas $\{0\}$ mais la droite $\text{Vect}(\mathbf 1)$ tout entière.

> **Conclusion.** La covariance est une **forme bilinéaire symétrique positive** sur
> $\mathbb R^n$ — un *semi*-produit scalaire. Elle devient un **vrai** produit scalaire dès qu'on
> se restreint à l'hyperplan $H$ des vecteurs centrés, où la seule série constante est la série
> nulle.

> 🔑 **Ce n'est pas une réserve technique, c'est le contenu du module.** Elle dit exactement ceci :
> *la covariance est aveugle au niveau, elle ne voit que les écarts.* Ajouter 1 000 € à tous les
> prix d'une série ne change aucune covariance — parce qu'on translate dans une direction que la
> forme écrase.

---

## 8.3 Ce qui tombe immédiatement

Une fois la vérification faite, **tout théorème des modules 1 à 4 se relit en statistique**, sans
la moindre démonstration nouvelle.

### La variance est un carré de norme

$$\operatorname{Var}(x)=\operatorname{Cov}(x,x)=\frac{\|\tilde x\|^2}{n}$$

### L'identité de développement devient la variance d'une somme

Le [§ 1.2](01-produit-scalaire-et-norme.md) donne $\|u+v\|^2=\|u\|^2+2\langle u,v\rangle+\|v\|^2$.
Traduit :

$$\boxed{\;\operatorname{Var}(x+y)=\operatorname{Var}(x)+2\operatorname{Cov}(x,y)+\operatorname{Var}(y)\;}$$

> ⚠️ **La formule que tout le monde apprend par cœur est l'identité remarquable
> $(a+b)^2=a^2+2ab+b^2$**, écrite dans le bon espace. Le « terme croisé » du § 1.2 est
> littéralement la covariance.

### Pythagore devient le théorème d'additivité des variances

$$\operatorname{Cov}(x,y)=0
\quad\Longleftrightarrow\quad
\operatorname{Var}(x+y)=\operatorname{Var}(x)+\operatorname{Var}(y)$$

**Décorrélé = orthogonal**, et l'additivité des variances **est** le
[théorème de Pythagore](03-orthogonalite-et-pythagore.md) — une équivalence, pas une implication.

### Cauchy–Schwarz devient $|\rho|\le 1$

C'est le [§ 2.3](02-cauchy-schwarz-et-angle.md), dont ce module est la justification :

$$\bigl|\operatorname{Cov}(x,y)\bigr|\le\sqrt{\operatorname{Var}(x)\operatorname{Var}(y)}
\qquad\text{soit}\qquad
\rho_{x,y}=\frac{\operatorname{Cov}(x,y)}{\sigma_x\sigma_y}=\cos\theta\in[-1,1]$$

avec **égalité si et seulement si** $\tilde x$ et $\tilde y$ sont colinéaires — c'est-à-dire si
$y=ax+b$ exactement.

---

## 8.4 La bilinéarité au travail : la variance d'un portefeuille

C'est l'usage le plus rentable de la propriété. Soient $x_1,\dots,x_p$ des séries et
$w_1,\dots,w_p$ des poids. Par **bilinéarité seule** :

$$\operatorname{Var}\Bigl(\sum_{j=1}^p w_jx_j\Bigr)
=\sum_{j=1}^p\sum_{k=1}^p w_jw_k\operatorname{Cov}(x_j,x_k)
=\boxed{\;w^{\top}\Sigma\,w\;}$$

où $\Sigma_{jk}=\operatorname{Cov}(x_j,x_k)$ est la **matrice de covariance**.

Aucun calcul probabiliste n'intervient : c'est le développement de
$\bigl\|\sum_j w_j\tilde x_j\bigr\|^2$, exactement comme on développerait un carré.

> 🔑 **La diversification est un énoncé géométrique.** $\operatorname{Var}(x+y)$ est plus petite
> que $\operatorname{Var}(x)+\operatorname{Var}(y)$ **si et seulement si** l'angle entre les deux
> vecteurs centrés est **obtus**. Deux actifs se couvrent quand ils pointent dans des directions
> opposées ; ils s'additionnent quand ils pointent dans la même. Il n'y a rien de plus dans
> l'idée de portefeuille.

---

## 8.5 La matrice de covariance est une matrice de Gram

Rangeons les $p$ séries centrées en colonnes d'une matrice $\tilde X$ ($n$ lignes, $p$ colonnes).
Alors

$$\Sigma=\frac{1}{n}\,\tilde X^{\top}\tilde X
\qquad\text{c'est-à-dire}\qquad
\Sigma_{jk}=\frac1n\langle\tilde x_j,\tilde x_k\rangle$$

Une matrice de la forme $G_{jk}=\langle v_j,v_k\rangle$ s'appelle une **matrice de Gram**. Elle a
trois propriétés, et **toutes trois sont des faits sur les matrices de covariance** :

| Propriété de Gram | Traduction statistique |
|---|---|
| $\Sigma^{\top}=\Sigma$ | $\operatorname{Cov}(x,y)=\operatorname{Cov}(y,x)$ |
| $w^{\top}\Sigma w\ge 0$ pour tout $w$ — **semi-définie positive** | **Aucun portefeuille ne peut avoir une variance négative** |
| $\operatorname{rang}(\Sigma)=\dim\text{Vect}(\tilde x_1,\dots,\tilde x_p)$ | Le rang compte les séries **réellement distinctes** |

**La deuxième ligne n'est pas une hypothèse, c'est un théorème** — et sa démonstration tient en
une ligne, déjà écrite au § 8.4 :

$$w^{\top}\Sigma w=\frac{1}{n}\Bigl\|\sum_j w_j\tilde x_j\Bigr\|^2\;\ge\;0$$

### Quand $\Sigma$ est-elle **définie** positive ?

$$w^{\top}\Sigma w=0
\;\Longleftrightarrow\;\sum_j w_j\tilde x_j=0
\;\Longleftrightarrow\;\text{une combinaison des séries est \textbf{constante}}$$

Donc : **$\Sigma$ est inversible si et seulement si les vecteurs centrés sont linéairement
indépendants.**

| Situation | Conséquence |
|---|---|
| Deux séries identiques (ou affines l'une de l'autre) | $\Sigma$ **singulière**, $\rho=\pm1$ |
| $p>n-1$ séries | Forcément singulière : $\dim H=n-1$ ne peut pas contenir $p$ vecteurs libres |
| Séries **presque** colinéaires | $\Sigma$ inversible mais **mal conditionnée** — c'est la *multicolinéarité* |

> ⚠️ **La multicolinéarité n'est pas un défaut des données, c'est un angle.** Deux prédicteurs
> corrélés à $0{,}99$ font un angle de $8°$ : la base qu'ils forment est presque plate, et
> décomposer un vecteur dessus amplifie énormément la moindre erreur. Aucune méthode statistique
> ne peut réparer une géométrie dégénérée.

---

## 8.6 La corrélation : la matrice de Gram des vecteurs **normés**

Normalisons : $e_j=\tilde x_j/\|\tilde x_j\|$. Alors

$$R_{jk}=\langle e_j,e_k\rangle=\rho_{jk}=\cos\theta_{jk}$$

La matrice de corrélation est donc la **matrice de Gram d'une famille de vecteurs unitaires** :
diagonale de 1, symétrique, semi-définie positive.

### La conséquence frappante : on ne choisit pas trois corrélations librement

Trois directions unitaires dans un espace euclidien obéissent à l'**inégalité triangulaire sur
les angles** : $\theta_{23}\le\theta_{12}+\theta_{13}$. En passant au cosinus :

$$\boxed{\;\rho_{12}\rho_{13}-\sqrt{(1-\rho_{12}^2)(1-\rho_{13}^2)}
\;\le\;\rho_{23}\;\le\;
\rho_{12}\rho_{13}+\sqrt{(1-\rho_{12}^2)(1-\rho_{13}^2)}\;}$$

**Exemple.** Si $A$ est corrélé à $0{,}9$ avec $B$ **et** à $0{,}9$ avec $C$, alors

$$\rho_{BC}\;\ge\;0{,}81-0{,}19=\mathbf{0{,}62}$$

$B$ et $C$ ne peuvent **pas** être décorrélés : c'est géométriquement impossible. Deux vecteurs à
$25{,}8°$ d'un même troisième sont au plus à $51{,}7°$ l'un de l'autre.

> 🔑 **Une matrice de corrélation « plausible » inventée à la main est presque toujours
> invalide.** Le test n'est pas que chaque coefficient soit dans $[-1,1]$ : c'est que la matrice
> soit semi-définie positive, autrement dit qu'il **existe** des vecteurs réalisant tous ces
> angles à la fois. C'est le contrôle que fait tout logiciel de gestion des risques avant
> d'accepter une matrice saisie à la main.

---

## 8.7 La régression : une pente est un coefficient de projection

Dernier dividende. Le coefficient de la droite des moindres carrés de $y$ sur $x$ vaut

$$\hat r=\frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)}
=\frac{\langle\tilde x,\tilde y\rangle}{\|\tilde x\|^2}$$

On reconnaît **exactement** le $\lambda$ de la projection du
[§ 4.1](04-projection-orthogonale.md). La pente n'est pas « une formule de régression » : c'est
le coefficient de $\tilde y$ sur la direction $\tilde x$.

Et la décomposition qui va avec est un [Pythagore](03-orthogonalite-et-pythagore.md) :

$$\tilde y=\underbrace{\hat r\,\tilde x}_{\text{expliqué}}+\underbrace{\tilde e}_{\perp\ \tilde x}
\qquad\Longrightarrow\qquad
\operatorname{Var}(y)=\underbrace{\rho^2\operatorname{Var}(y)}_{\text{expliquée}}
+\underbrace{\operatorname{Var}(y)(1-\rho^2)}_{\text{résiduelle}}$$

> 🔑 **$\rho^2$ est une part de variance parce que c'est un $\cos^2\theta$.** La variance
> résiduelle minimale $\operatorname{Var}(y)(1-\rho^2)$ qu'établit
> [`modele.md`](../../modele.md) par le calcul est ici lue directement sur la figure : c'est
> $\sin^2\theta$, le carré de la distance à la droite.

---

## 8.8 Simulations

### S8.1 — Les trois propriétés, et celle qui manque

```python
import numpy as np

rng = np.random.default_rng(8)
n = 15
cov = lambda a, b: ((a - a.mean()) @ (b - b.mean())) / n

x, y, z = rng.normal(100, 12, n), rng.normal(50, 4, n), rng.normal(0, 1, n)
a, b = 2.5, -1.3

print("symétrie    :", np.isclose(cov(x, y), cov(y, x)))
print("bilinéarité :", np.isclose(cov(a*x + b*z, y), a*cov(x, y) + b*cov(z, y)))
print("positive    :", cov(x, x) >= 0)

# ... mais PAS définie : une série constante non nulle a une variance nulle
c = np.full(n, 7.0)
print(f"Var(serie constante 7) = {cov(c, c):.1f}   et pourtant le vecteur n'est pas nul")
print("noyau = Vect(1) :", np.isclose(cov(np.ones(n) * 3.2, y), 0))

# invariance par translation : ajouter une constante ne change rien
print("Cov(x+1000, y) = Cov(x, y) :", np.isclose(cov(x + 1000, y), cov(x, y)))
```

La quatrième ligne est le cœur du § 8.2 : **une variance nulle ne signifie pas un vecteur nul**,
elle signifie un vecteur **constant**. C'est toute la différence entre « positive » et « définie
positive ».

### S8.2 — L'identité de développement, lue deux fois

```python
print("Var(x+y) = Var(x) + 2Cov(x,y) + Var(y) :",
      np.isclose(cov(x + y, x + y), cov(x, x) + 2*cov(x, y) + cov(y, y)))

# Pythagore : additivité des variances <=> orthogonalité des centrés
xt = x - x.mean()
yperp = y - y.mean() - (cov(x, y) / cov(x, x)) * xt      # partie de y orthogonale à x
print(f"Cov(x, y_perp) = {cov(x, yperp):+.2e}   (nulle)")
print("Var(x + y_perp) = Var(x) + Var(y_perp) :",
      np.isclose(cov(x + yperp, x + yperp), cov(x, x) + cov(yperp, yperp)))
```

### S8.3 — La matrice de covariance est une matrice de Gram

```python
p = 4
X = rng.normal(size=(n, p)) @ rng.normal(size=(p, p))    # 4 séries corrélées
Xt = X - X.mean(axis=0)
Sigma = Xt.T @ Xt / n

print("Sigma = X~ᵀX~/n :", np.allclose(Sigma, np.cov(X.T, bias=True)))
print("symétrique      :", np.allclose(Sigma, Sigma.T))
print("valeurs propres :", np.round(np.linalg.eigvalsh(Sigma), 6), " → toutes >= 0")

# aucun portefeuille ne peut avoir une variance négative
W = rng.normal(size=(20_000, p))
q = np.einsum("ij,jk,ik->i", W, Sigma, W)
print(f"min sur 20 000 portefeuilles : {q.min():.6f}   (>= 0, toujours)")

# une série redondante rend Sigma singulière
Xd = np.column_stack([X, 3 * X[:, 0] - 2 * X[:, 1] + 5])   # combinaison affine des deux 1res
Sd = np.cov(Xd.T, bias=True)
print(f"rang avec serie redondante : {np.linalg.matrix_rank(Sd)} / {Sd.shape[0]}")
```

**La ligne des valeurs propres est la démonstration visuelle** : aucune n'est négative, et il ne
peut pas en être autrement — c'est une matrice de Gram.

### S8.4 — Trois corrélations ne se choisissent pas librement

```python
def bornes(r12, r13):
    s = np.sqrt((1 - r12**2) * (1 - r13**2))
    return r12 * r13 - s, r12 * r13 + s

for r in (0.9, 0.7, 0.5):
    lo, hi = bornes(r, r)
    print(f"rho(A,B) = rho(A,C) = {r}  ->  rho(B,C) ∈ [{lo:+.3f}, {hi:+.3f}]"
          f"   angles : {np.degrees(np.arccos(r)):.1f}° chacun")

# contrôle : une matrice hors bornes n'est pas semi-définie positive
for r23 in (0.62, 0.30, -0.50):
    R = np.array([[1, .9, .9], [.9, 1, r23], [.9, r23, 1.0]])
    vp = np.linalg.eigvalsh(R).min()
    print(f"rho(B,C)={r23:+.2f} -> plus petite valeur propre = {vp:+.4f}"
          f"   {'valide' if vp > -1e-12 else 'IMPOSSIBLE'}")
```

La seconde boucle est le contrôle décisif : dès qu'on descend sous $0{,}62$, une valeur propre
devient **négative**. Aucune donnée au monde ne peut produire cette matrice.

### S8.5 — La pente est un coefficient de projection

```python
t = np.arange(1., n + 1.)
tt, yt = t - t.mean(), y - y.mean()

pente_stat = cov(t, y) / cov(t, t)
pente_geo = (tt @ yt) / (tt @ tt)
pente_lib = np.polyfit(t, y, 1)[0]
print(f"Cov/Var = {pente_stat:.6f}   projection = {pente_geo:.6f}   polyfit = {pente_lib:.6f}")

rho = (tt @ yt) / (np.linalg.norm(tt) * np.linalg.norm(yt))
resid = yt - pente_geo * tt
print(f"Var residuelle = {cov(resid, resid):.6f}"
      f"   Var(y)(1-rho²) = {cov(y, y) * (1 - rho**2):.6f}")
print(f"angle = {np.degrees(np.arccos(abs(rho))):.1f}°   -> rho² = cos² = {rho**2:.4f}")
```

Les trois pentes coïncident à la sixième décimale, et la variance résiduelle **est** le
$\sin^2\theta$ annoncé au § 8.7.

---

## 8.9 Exercices

**E8.1.** Démontrer que $x\mapsto\tilde x$ est linéaire, puis en déduire la bilinéarité de la
covariance à partir de celle du produit scalaire. *Combien de lignes ?*

**E8.2.** Montrer que $\operatorname{Cov}(x,y)=\frac1n x^{\top}My$ et que cette écriture est
symétrique en $x$ et $y$ malgré les apparences. *(Piste : $M^{\top}=M$ et $M^2=M$.)*

**E8.3.** Caractériser exactement les $x$ tels que $\operatorname{Var}(x)=0$. *Pourquoi cela
empêche-t-il la covariance d'être un produit scalaire sur $\mathbb R^n$, et pourquoi cela cesse
d'être un problème sur $H$ ?*

**E8.4.** Montrer que $\operatorname{Cov}(ax+b,\;cy+d)=ac\operatorname{Cov}(x,y)$ pour tous
réels $a,b,c,d$. *Quelle propriété géométrique du centrage explique la disparition de $b$ et
$d$ ?*

**E8.5.** Deux actifs ont pour écarts-types $\sigma_1=20\,\%$ et $\sigma_2=30\,\%$. Calculer la
volatilité d'un portefeuille $50/50$ pour $\rho=1$, $\rho=0$, $\rho=-1$. *Représenter les trois
cas par un triangle de côtés $\sigma_1/2$ et $\sigma_2/2$ : quel théorème du
[module 3](03-orthogonalite-et-pythagore.md) donne le cas central ?*

**E8.6.** Montrer que la variance d'un portefeuille équipondéré de $p$ actifs de même variance
$\sigma^2$ et de corrélation commune $\rho$ vaut
$\frac{\sigma^2}{p}\bigl(1+(p-1)\rho\bigr)$. *En déduire la limite quand $p\to\infty$, et le
$\rho$ minimal possible pour $p$ actifs.* **(Réponse : $\rho\sigma^2$, et $\rho\ge-\frac{1}{p-1}$
— la semi-définie positivité borne la corrélation commune par le bas.)**

**E8.7.** Démontrer l'encadrement du § 8.6 à partir de l'inégalité triangulaire sur les angles.
*Puis vérifier, avec $\rho_{12}=\rho_{13}=0{,}5$, que $\rho_{23}$ peut être négatif — et jusqu'où.*

**E8.8.** Pourquoi $p$ séries ne peuvent-elles pas être linéairement indépendantes dès que
$p>n-1$ ? *(Piste : $\dim H$.) Quelle conséquence pour une régression à plus de prédicteurs que
d'observations ?*

**E8.9 — orientée finance.** À partir de trois séries obtenues avec `historique_sbf250.py` :
1. construire $\Sigma$ et $R$ à la main par produits scalaires, et vérifier avec `np.cov` /
   `np.corrcoef` ;
2. vérifier que les valeurs propres de $R$ sont toutes positives ;
3. remplacer un coefficient de $R$ par une valeur « intuitive » hors des bornes du § 8.6 et
   observer l'apparition d'une valeur propre négative ;
4. calculer la volatilité du portefeuille équipondéré et la comparer à la moyenne des
   volatilités. *D'où vient l'écart, géométriquement ?*

---

## 8.10 À retenir

- **La covariance est une forme bilinéaire symétrique positive** — un produit scalaire à une
  réserve près : elle n'est **pas définie**, son noyau est $\text{Vect}(\mathbf 1)$.
- **Traduction de cette réserve** : la covariance est aveugle au niveau, elle ne voit que les
  écarts. Sur l'hyperplan $H$ des vecteurs centrés, c'est un vrai produit scalaire.
- **Quatre résultats tombent sans calcul nouveau** :
  $\operatorname{Var}(x+y)=\operatorname{Var} x+2\operatorname{Cov}+\operatorname{Var} y$ (identité
  de développement), décorrélé = orthogonal (Pythagore), $|\rho|\le1$ (Cauchy–Schwarz), et
  $\operatorname{Var}(w^{\top}x)=w^{\top}\Sigma w$ (bilinéarité).
- ⭐ **$\Sigma$ est une matrice de Gram** : symétrique, **semi-définie positive** — d'où
  l'impossibilité d'une variance de portefeuille négative — et de rang le nombre de séries
  réellement distinctes.
- **$R$ est la matrice de Gram des vecteurs unitaires** : ses coefficients sont des cosinus, et
  ils ne se choisissent **pas** indépendamment les uns des autres.
- **Une pente de régression est un coefficient de projection**, et $\rho^2$ une part de variance
  parce que c'est un $\cos^2\theta$.

---

⬅️ [Module 7 — Le dictionnaire géométrique des statistiques](07-dictionnaire-geometrique-des-statistiques.md) ·
🏠 [Sommaire](README.md) ·
➡️ **Suite** : [Cours de statistique mathématique](../statistique/mathematique/README.md)
