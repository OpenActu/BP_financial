# Module 10 — Décorrélation et indépendance ⭐

**Durée : 1 h.** Prérequis : module [9](09-vecteur-gaussien.md).

> **La question traitée.** Soient $Z_1,Z_2$ i.i.d. $\mathcal N(0,1)$. Les variables $Z_1+Z_2$ et
> $Z_1-Z_2$ sont-elles indépendantes ? Justifier.

**Ce qui est en jeu.** La réponse est oui, mais **pour deux raisons conjointes**, et l'oubli de
l'une des deux est l'erreur la plus répandue du cours. C'est aussi le module qui isole ce que la
gaussianité apporte — et ce qu'elle est seule à apporter.

---

## 10.1 En général : une implication, dans un seul sens

$$X\perp\!\!\!\perp Y \quad\Longrightarrow\quad \operatorname{Cov}(X,Y)=0
\qquad\text{mais la réciproque est FAUSSE}$$

Le contre-exemple du [§ 9.3](09-vecteur-gaussien.md) le montre. En voici un second, encore plus
dépouillé : si $X\sim\mathcal N(0,1)$ et $Y=X^2$, alors $\operatorname{Cov}(X,Y)=E(X^3)=0$ —
décorrélées — alors que $Y$ est une **fonction déterministe** de $X$.

**Pourquoi** : la covariance ne mesure que la dépendance **linéaire**. Elle est aveugle à toute
relation non linéaire, aussi forte soit-elle.

> ⚠️ **Une corrélation nulle ne dit rien de l'absence de lien.** Elle dit seulement qu'aucune
> **droite** ne résume ce lien. Sur un nuage en forme de parabole, de cercle ou de sablier, la
> corrélation est nulle et la dépendance totale.

---

## 10.2 Pour un vecteur gaussien : l'équivalence

> **Théorème.** Si $(X,Y)$ est un **vecteur gaussien**, alors
> $$X\perp\!\!\!\perp Y \quad\Longleftrightarrow\quad \operatorname{Cov}(X,Y)=0$$

Plus généralement, pour $\mathbf X\sim\mathcal N_n(\boldsymbol\mu,\Sigma)$, deux blocs de
coordonnées sont indépendants si et seulement si le bloc de covariances croisées de $\Sigma$ est
nul. En particulier, $\mathbf X$ a des coordonnées **mutuellement indépendantes** si et seulement
si $\Sigma$ est **diagonale**.

**Idée de démonstration.** Si $\Sigma$ est diagonale, la densité conjointe se factorise :
$$f(\mathbf x)=\frac{1}{(2\pi)^{n/2}\prod_i\sigma_i}
\exp\!\left(-\sum_i\frac{(x_i-\mu_i)^2}{2\sigma_i^2}\right)
=\prod_{i=1}^n f_i(x_i)$$
et une densité conjointe qui se factorise en produit de densités marginales **est** l'indépendance.

> ⚠️ **L'hypothèse « vecteur gaussien » n'est pas décorative.** Dans le contre-exemple du § 9.3,
> $X$ et $Y$ sont gaussiennes et décorrélées, mais dépendantes — précisément parce que $(X,Y)$
> **n'est pas** un vecteur gaussien. L'équivalence porte sur la loi **conjointe**, jamais sur les
> marges prises séparément.

> 🔑 **Cette équivalence est le privilège de la gaussienne.** Ailleurs, établir une indépendance
> est laborieux ; ici, il suffit de calculer une covariance. Toute l'élégance du
> [module 16](16-theoreme-de-fisher-cochran.md) en vient.

---

## 10.3 L'exemple décisif : $Z_1+Z_2$ et $Z_1-Z_2$

Nous avons maintenant tout ce qu'il faut. Posons $S=Z_1+Z_2$ et $D=Z_1-Z_2$.

**Étape 1 — $(S,D)$ est un vecteur gaussien.**

$(Z_1,Z_2)$ est un vecteur gaussien standard, et $(S,D)$ s'en déduit par l'application linéaire
$$\begin{pmatrix}S\\D\end{pmatrix}=A\begin{pmatrix}Z_1\\Z_2\end{pmatrix},
\qquad A=\begin{pmatrix}1&1\\1&-1\end{pmatrix}.$$

Or **l'image d'un vecteur gaussien par une application linéaire est un vecteur gaussien**
([§ 9.4](09-vecteur-gaussien.md)).

**Étape 2 — leurs lois marginales.**

Par le [§ 8.1](08-addition-de-lois-et-stabilite-gaussienne.md) : $S\sim\mathcal N(0,2)$ et
$D\sim\mathcal N(0,2)$.

**Étape 3 — leur covariance.**

$$\operatorname{Cov}(S,D)=\operatorname{Cov}(Z_1+Z_2,\;Z_1-Z_2)
=\underbrace{\operatorname{Var}(Z_1)}_{1}
\underbrace{-\operatorname{Cov}(Z_1,Z_2)+\operatorname{Cov}(Z_2,Z_1)}_{0\ \text{(termes croisés nuls)}}
-\underbrace{\operatorname{Var}(Z_2)}_{1}=0$$

**Étape 4 — conclusion.**

$(S,D)$ est un vecteur gaussien de covariance nulle : par le théorème du § 10.2,

$$\boxed{\;S=Z_1+Z_2 \quad\text{et}\quad D=Z_1-Z_2 \quad\text{sont INDÉPENDANTES.}\;}$$

---

## 10.4 Ce qui rend le résultat possible — et ce qui le détruirait

⚠️ **Il faut les deux ingrédients**, et l'oubli de l'un des deux est l'erreur classique :

| Ingrédient | Rôle | Si on l'enlève |
|---|---|---|
| $\operatorname{Cov}(S,D)=0$ | Vient de $\operatorname{Var}(Z_1)=\operatorname{Var}(Z_2)$ | Si les variances diffèrent, la covariance ne s'annule pas et il n'y a **pas** d'indépendance |
| $(S,D)$ vecteur gaussien | Vient de la gaussianité de $(Z_1,Z_2)$ | Sans elle, décorrélation ≠ indépendance (§ 10.1) |

**La contre-épreuve indispensable.** Refaites le calcul avec $Z_1,Z_2$ i.i.d. **exponentielles**.
La covariance de $S$ et $D$ est **encore nulle** (le calcul de l'étape 3 n'utilise que l'égalité
des variances), mais elles sont **dépendantes** : la simulation S10.2 le montre en exhibant une
loi conditionnelle de $D$ qui varie avec $S$. Sur un couple exponentiel, $D$ est même contraint
par $S$ — on a toujours $|D|\le S$.

---

## 10.5 Lecture géométrique — celle qui prépare la suite

Les vecteurs $u=(1,1)$ et $v=(1,-1)$ de $\mathbb R^2$ sont **orthogonaux** :
$\langle u,v\rangle=1-1=0$.

Or $S=\langle \mathbf Z,u\rangle$ et $D=\langle \mathbf Z,v\rangle$.

> 🔑 **Le résultat n'est donc pas un accident de calcul.** Il énonce que **deux formes linéaires
> associées à des directions orthogonales, appliquées à un vecteur gaussien standard, sont
> indépendantes.** Formulé ainsi, il se généralise immédiatement à $n$ dimensions — et c'est
> précisément ce que fait le
> [module 11](11-invariance-par-rotation-et-lemme-de-projection.md).

---

## 10.6 Simulations

### S10.1 — Décorrélé mais dépendant, en une image

```python
import numpy as np

rng = np.random.default_rng(6)
N = 300_000
X = rng.standard_normal(N)

for nom, Y in [("Y = X²",   X**2),
               ("Y = |X|",  np.abs(X)),
               ("Y = eps·X", rng.choice([-1.0, 1.0], N) * X)]:
    c = np.corrcoef(X, Y)[0, 1]
    # test de dépendance : la variance de Y change-t-elle selon la tranche de X ?
    tr = [Y[(X > a) & (X < b)].std() for a, b in [(-3, -1), (-0.2, 0.2), (1, 3)]]
    print(f"{nom:11s} corr={c:+.4f}   std(Y) par tranche de X : {[round(t,3) for t in tr]}")
```

Les trois corrélations sont nulles à la troisième décimale. Les écarts-types conditionnels, eux,
**varient franchement** : la dépendance est massive et la corrélation ne la voit pas.

### S10.2 — L'expérience décisive : gaussienne contre exponentielle

```python
def diagnostic(nom, tirage):
    Z = tirage((400_000, 2))
    S, D = Z[:, 0] + Z[:, 1], Z[:, 0] - Z[:, 1]
    print(f"\n{nom} : cov(S,D) = {np.cov(S, D)[0, 1]:+.5f}")
    # la décorrélation ne suffit pas : la LOI de D doit être la même à S fixé
    for q0, q1 in zip(np.quantile(S, [.05, .45, .90]), np.quantile(S, [.15, .55, 1.0])):
        m = (S > q0) & (S < q1)
        print(f"   S ∈ [{q0:+7.3f},{q1:+7.3f}] → écart-type de D = {D[m].std():.4f}")

diagnostic("gaussienne",    lambda s: rng.standard_normal(s))
diagnostic("exponentielle", lambda s: rng.exponential(1.0, s))
```

**Ce que vous devez observer.** Pour la gaussienne, les trois écarts-types conditionnels valent
tous $\sqrt2\approx1{,}414$ : la loi de $D$ ne dépend **pas** de $S$ — c'est l'indépendance.
Pour l'exponentielle, la covariance est **également nulle**, mais les écarts-types conditionnels
**croissent** nettement avec $S$ : décorrélées, dépendantes.

> 🔑 C'est l'expérience la plus utile du cours. Elle isole exactement ce que la gaussianité
> apporte, et ce qu'elle est seule à apporter.

---

## 10.7 Exercices

**E10.1.** Démontrer $X\perp\!\!\!\perp Y\Rightarrow\operatorname{Cov}(X,Y)=0$. *Où la réciproque
échoue-t-elle ?*

**E10.2.** Soient $Z_1,Z_2$ i.i.d. $\mathcal N(0,1)$ et $a,b,c,d$ réels. À quelle condition
$aZ_1+bZ_2$ et $cZ_1+dZ_2$ sont-elles indépendantes ? *(Réponse : $ac+bd=0$, soit
l'**orthogonalité** des vecteurs $(a,b)$ et $(c,d)$.)*

**E10.3.** Soient $X_1\sim\mathcal N(0,1)$ et $X_2\sim\mathcal N(0,4)$ indépendantes. $X_1+X_2$
et $X_1-X_2$ sont-elles indépendantes ? Calculer leur covariance et conclure. *(Réponse : non,
$\operatorname{Cov}=1-4=-3\ne 0$. L'égalité des variances était essentielle au § 10.3.)*

**E10.4.** Reprendre E10.3 en cherchant $\lambda$ tel que $X_1+X_2$ et $X_1-\lambda X_2$ soient
indépendantes. *Interpréter géométriquement avec le § 10.5.*

**E10.5.** Pour $X\sim\mathcal N(0,1)$ et $Y=X^2$, calculer $\operatorname{Cov}(X,Y)$ et
$\operatorname{Cov}(X^2,Y)$. *La seconde est-elle nulle ? Que conclure sur ce que « décorrélé »
mesure ?*

**E10.6.** Pour un vecteur gaussien de matrice $\Sigma$ diagonale par blocs, montrer que les blocs
de coordonnées sont indépendants. *(Piste : factoriser la densité, comme au § 10.2.)*

---

## 10.8 À retenir

- **Indépendance ⟹ décorrélation.** La réciproque est **fausse** en général : la covariance ne
  voit que le **linéaire**.
- ⭐ **Pour un vecteur gaussien, les deux sont équivalentes.** C'est le privilège dont vit tout ce
  cours : une indépendance s'établit par un calcul de covariance.
- **$Z_1+Z_2$ et $Z_1-Z_2$ sont indépendantes** parce que $(1,1)\perp(1,-1)$ **et** que le vecteur
  de départ est gaussien. Les deux conditions sont nécessaires.
- **Contre-épreuve exponentielle** : même covariance nulle, dépendance flagrante. À faire soi-même
  une fois pour toutes.

---

⬅️ [Module 9 — Le vecteur gaussien](09-vecteur-gaussien.md) ·
➡️ [Module 11 — Invariance par rotation et lemme de projection](11-invariance-par-rotation-et-lemme-de-projection.md) ·
🏠 [Sommaire](README.md)
