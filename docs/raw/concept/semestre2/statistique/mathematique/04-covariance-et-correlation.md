# Module 4 — Covariance et corrélation ⭐

**Durée : 1 h 15.** Prérequis : modules [1](01-variable-aleatoire-et-loi.md) à
[3](03-variance-et-moments.md).

> **La question traitée.** Le [§ 3.3](03-variance-et-moments.md) a laissé un terme sans nom dans
> $\operatorname{Var}(X+Y)$. Que mesure-t-il — et que ne mesure-t-il pas ?

**Ce qui est en jeu.** La covariance est le premier objet du cours qui porte sur **deux**
variables. Elle ne voit qu'une chose — le lien **linéaire** — et cette cécité est la source de la
moitié des erreurs de la statistique appliquée.

---

## 4.1 Définition

> **Définition.** La **covariance** de $X$ et $Y$ est
> $$\operatorname{Cov}(X,Y)=E\Bigl(\bigl(X-E(X)\bigr)\bigl(Y-E(Y)\bigr)\Bigr)$$

**Formule de calcul**, obtenue en développant par linéarité, exactement comme au
[§ 3.1](03-variance-et-moments.md) :

$$\boxed{\;\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)\;}$$

Deux cas particuliers à voir immédiatement :

- $\operatorname{Cov}(X,X)=\operatorname{Var}(X)$ — **la variance est un cas particulier de
  covariance**, et non l'inverse ;
- $\operatorname{Cov}(X,Y)=0 \iff E(XY)=E(X)E(Y)$, c'est-à-dire la conclusion du
  [§ 2.4](02-esperance.md).

**Lecture du signe** — c'est tout ce que la covariance sait dire :

| Signe | Ce qu'il indique |
|---|---|
| $>0$ | $X$ et $Y$ s'écartent de leur moyenne **dans le même sens** |
| $<0$ | En sens opposés |
| $=0$ | Aucune tendance linéaire — **et rien de plus** (§ 4.5) |

⚠️ **La covariance a une unité** : des euros × des jours, si $X$ est en euros et $Y$ en jours.
Sa **valeur** est donc ininterprétable telle quelle. C'est précisément le problème que la
corrélation résout (§ 4.4).

---

## 4.2 Les propriétés

| Propriété | Énoncé | Hypothèse |
|---|---|---|
| **Symétrie** | $\operatorname{Cov}(X,Y)=\operatorname{Cov}(Y,X)$ | aucune |
| **Bilinéarité** | $\operatorname{Cov}(aX+bZ,\,Y)=a\operatorname{Cov}(X,Y)+b\operatorname{Cov}(Z,Y)$ | aucune |
| **Invariance par translation** | $\operatorname{Cov}(X+c,\,Y)=\operatorname{Cov}(X,Y)$ | aucune |
| **Positivité** | $\operatorname{Cov}(X,X)\ge 0$ | aucune |
| **Indépendance ⟹ nullité** | $X\perp\!\!\!\perp Y\Rightarrow\operatorname{Cov}(X,Y)=0$ | indépendance |

> 🔑 **Symétrique, bilinéaire, positive : ce sont exactement les trois propriétés d'un produit
> scalaire** ([§ 1.1 du cours d'algèbre](../../../semestre1/algebre/01-produit-scalaire-et-norme.md)). Ce n'est
> pas une coïncidence, et ce n'est pas une analogie : le
> [module 9 du cours d'algèbre](../../../semestre1/algebre/09-covariance-et-produit-scalaire.md) démontre
> l'identification — avec la même réserve qu'ici, la positivité n'est pas **définie** ($X$
> constante donne une variance nulle sans être nulle).

**Ce que la bilinéarité produit gratuitement** — la variance d'une combinaison linéaire :

$$\operatorname{Var}\Bigl(\sum_{j} w_jX_j\Bigr)=\sum_j\sum_k w_jw_k\operatorname{Cov}(X_j,X_k)
=w^{\top}\Sigma\,w$$

où $\Sigma_{jk}=\operatorname{Cov}(X_j,X_k)$ est la **matrice de covariance**. C'est la formule
de la variance d'un portefeuille, et elle ne demande **aucune hypothèse** : ni indépendance, ni
normalité.

---

## 4.3 Le terme croisé du § 3.3, enfin nommé

$$\operatorname{Var}(X+Y)=\operatorname{Var}(X)+2\operatorname{Cov}(X,Y)+\operatorname{Var}(Y)$$

C'est le cas $p=2$, $w=(1,1)$ de la formule ci-dessus. Trois régimes :

| $\operatorname{Cov}$ | $\operatorname{Var}(X+Y)$ vs somme des variances | Lecture financière |
|---|---|---|
| $>0$ | **Plus grande** | Les risques s'ajoutent |
| $=0$ | **Égale** | Additivité — le cas i.i.d. du [§ 3.3](03-variance-et-moments.md) |
| $<0$ | **Plus petite** | Les actifs se **couvrent** |

> 🔑 **Toute la diversification est dans la troisième ligne**, et elle ne suppose rien de plus
> que la bilinéarité. Réunir deux actifs de covariance négative produit un portefeuille moins
> risqué que chacun d'eux — un résultat qui n'a rien de probabiliste au fond, seulement de
> quadratique.

---

## 4.4 La corrélation : la covariance rendue lisible

> **Définition.** Pour $\sigma_X,\sigma_Y>0$ :
> $$\rho_{X,Y}=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\,\sigma_Y}\;\in\;[-1,1]$$

La normalisation par les deux écarts-types élimine les unités : $\rho$ est **sans dimension**, et
donc comparable d'un couple de variables à un autre — ce que la covariance n'est pas.

**Pourquoi $|\rho|\le 1$.** C'est l'inégalité de **Cauchy–Schwarz**
([module 2 du cours d'algèbre](../../../semestre1/algebre/02-cauchy-schwarz-et-angle.md)) appliquée à la forme
bilinéaire du § 4.2 :

$$\operatorname{Cov}(X,Y)^2\;\le\;\operatorname{Var}(X)\operatorname{Var}(Y)$$

avec **égalité si et seulement si** $Y=aX+b$ presque sûrement. Une corrélation de $\pm1$ ne
signifie donc pas « très fort lien » : elle signifie **lien affine exact**.

**Propriétés :**

| Propriété | Énoncé |
|---|---|
| Invariance affine | $\rho_{aX+b,\;cY+d}=\operatorname{sgn}(ac)\,\rho_{X,Y}$ |
| Cas extrêmes | $\rho=\pm1\iff Y=aX+b$ p.s. |
| Lecture géométrique | $\rho=\cos\theta$ ([cours d'algèbre](../../../semestre1/algebre/09-covariance-et-produit-scalaire.md)) |

> ⚠️ **$\rho=0{,}9$ n'est pas « presque 1 ».** Lu comme un cosinus, c'est un angle de $25{,}8°$ —
> pas $0°$. Et $\rho^2=0{,}81$ : 19 % de la variance reste inexpliquée. L'intuition linéaire sur
> $\rho$ est systématiquement trop optimiste.

---

## 4.5 ⚠️ Les quatre choses que la corrélation ne dit pas

C'est la section à relire. Chacun de ces points coûte cher en pratique.

### ① Décorrélé n'est pas indépendant

$$X\perp\!\!\!\perp Y\;\Longrightarrow\;\rho=0
\qquad\text{mais la réciproque est \textbf{FAUSSE}}$$

**Contre-exemple minimal.** $X\sim\mathcal N(0,1)$ et $Y=X^2$. Alors
$\operatorname{Cov}(X,Y)=E(X^3)=0$ : elles sont décorrélées. Et pourtant $Y$ est une **fonction
déterministe** de $X$ — la dépendance est totale.

**Pourquoi** : la covariance ne mesure que la dépendance **linéaire**. Sur un nuage en forme de
parabole, de cercle ou de sablier, $\rho=0$ et la dépendance est complète.

> 🔑 Il existe un cas — et un seul dans ce cours — où la réciproque est vraie : celui du
> **vecteur gaussien**, au [module 10](10-decorrelation-et-independance.md). C'est le privilège
> dont vit tout l'édifice, et il ne s'étend à aucune autre famille.

### ② $\rho$ ne mesure pas la pente

Une corrélation de $0{,}99$ est compatible avec une pente de $0{,}001$ comme de $1000$ : $\rho$
mesure la **dispersion autour** de la droite, pas son inclinaison. Les deux sont liés par

$$\text{pente}=\rho\,\frac{\sigma_Y}{\sigma_X}$$

### ③ $\rho$ n'est pas la causalité

Deux séries croissantes dans le temps sont corrélées sans aucun lien — c'est la **corrélation
fallacieuse** (*spurious correlation*), et elle est la règle, non l'exception, sur des séries
chronologiques non stationnaires. Le [module 14](14-dependance-et-echec-du-tcl.md) montre que ce
n'est pas qu'une question d'interprétation : le test lui-même s'effondre.

### ④ $\rho$ est instable, et il l'est quand cela compte

Estimé sur peu de points, $\rho$ fluctue énormément : sur 20 observations réellement décorrélées,
$|\hat\rho|$ dépasse $0{,}38$ une fois sur dix, et $0{,}82$ a été observé (simulation S4.3). Et sur des rendements
financiers, les corrélations **montent brutalement dans les krachs** — au moment précis où la
diversification devrait protéger.

---

## 4.6 Simulations

### S4.1 — Covariance, bilinéarité, et le terme croisé

```python
import numpy as np

rng = np.random.default_rng(4)
N = 1_000_000
cov = lambda A, B: np.mean((A - A.mean()) * (B - B.mean()))

X = rng.normal(3, 2, N)
Y = 1.5 * X + rng.normal(0, 2, N)             # dépendance linéaire + bruit
Z = rng.normal(0, 1, N)

print(f"Cov = E(XY) - E(X)E(Y) : {cov(X, Y):.4f} vs "
      f"{np.mean(X*Y) - X.mean()*Y.mean():.4f}")
print(f"Cov(X,X) = Var(X)      : {cov(X, X):.4f} vs {X.var():.4f}")
print(f"bilinearite            : {cov(2*X + 5*Z, Y):.4f} vs "
      f"{2*cov(X, Y) + 5*cov(Z, Y):.4f}")
print(f"invariance/translation : {cov(X + 1000, Y):.4f}")

print(f"\nVar(X+Y) = {np.var(X+Y):8.4f}")
print(f"Var X + 2Cov + Var Y = {X.var() + 2*cov(X, Y) + Y.var():8.4f}")
print(f"(somme des variances seules : {X.var() + Y.var():.4f})")
```

La dernière comparaison est le § 4.3 : ignorer le terme croisé sous-estime ici la variance de la
somme de **40 %**.

### S4.2 — Décorrélé mais dépendant, et la cécité de $\rho$

```python
X = rng.standard_normal(N)
cas = {
    "Y = X²  (parabole)":     X**2,
    "Y = |X| (V)":            np.abs(X),
    "Y = signe aleatoire · X": rng.choice([-1.0, 1.0], N) * X,
}
for nom, Y in cas.items():
    r = np.corrcoef(X, Y)[0, 1]
    # diagnostic de dépendance : la dispersion de Y change-t-elle selon X ?
    tr = [Y[(X > a) & (X < b)].std() for a, b in [(-3, -1), (-.2, .2), (1, 3)]]
    print(f"{nom:26s} rho = {r:+.4f}   std(Y) par tranche : {[round(t,3) for t in tr]}")
```

Les trois corrélations sont nulles à la troisième décimale ; les dispersions conditionnelles
varient d'un facteur 10. **La dépendance est massive et $\rho$ ne la voit pas.**

### S4.3 — $\rho$ ne mesure pas la pente, et il est instable

```python
print("meme rho, pentes tres differentes :")
for pente in (0.001, 1.0, 1000.0):
    U = rng.standard_normal(200_000)
    V = pente * U + rng.normal(0, pente * 0.1435, 200_000)
    print(f"  pente = {pente:>8} -> rho = {np.corrcoef(U, V)[0,1]:.3f}"
          f"   pente lue = rho*sy/sx = "
          f"{np.corrcoef(U,V)[0,1] * V.std()/U.std():.4f}")

print("\ninstabilite de rho sur petit echantillon (vraies variables DECORRELEES) :")
for n in (10, 20, 50, 250):
    r = np.array([np.corrcoef(rng.standard_normal(n), rng.standard_normal(n))[0, 1]
                  for _ in range(20_000)])
    print(f"  n={n:>4} : |rho| depasse {np.quantile(np.abs(r), 0.90):.3f} "
          f"une fois sur dix   (max observe {np.abs(r).max():.3f})")
```

**La seconde boucle est celle à retenir.** Sur 20 points de données sans le moindre lien, une
corrélation de $0{,}38$ arrive une fois sur dix, et $0{,}82$ a été observée sur 20 000 tirages.
À $n=10$, il faut atteindre $0{,}55$ pour être dans les 10 % les plus élevés. Une
corrélation lue sur peu de points ne prouve rien : c'est le point de départ du
[module 13](13-portee-et-limites-du-tcl.md).

---

## 4.7 Exercices

**E4.1.** Démontrer $\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)$ par la seule linéarité de
l'espérance.

**E4.2.** Démontrer la bilinéarité et l'invariance par translation. *Quelle propriété du
[§ 3.2](03-variance-et-moments.md) retrouve-t-on en posant $Y=X$ ?*

**E4.3.** Montrer que $\rho_{aX+b,\;cY+d}=\operatorname{sgn}(ac)\,\rho_{X,Y}$. *Pourquoi cette
invariance rend-elle $\rho$ comparable d'un couple à l'autre, là où la covariance ne l'est pas ?*

**E4.4.** Soient $X\sim\mathcal N(0,1)$ et $Y=X^2$. Calculer $\operatorname{Cov}(X,Y)$ et
$\operatorname{Cov}(X^2,Y)$. *La seconde est-elle nulle ? Que conclure sur ce que « décorrélé »
mesure exactement ?*

**E4.5.** Deux actifs ont $\sigma_1=20\,\%$, $\sigma_2=30\,\%$. Calculer la volatilité d'un
portefeuille $50/50$ pour $\rho=1$, $0$, $-1$. *(Réponses : $25\,\%$, $18{,}0\,\%$, $5\,\%$.)
Commenter le fait que le cas $\rho=0$ soit déjà inférieur à la plus petite des deux
volatilités.*

**E4.6.** Montrer que $\operatorname{Cov}(X,Y)^2\le\operatorname{Var}(X)\operatorname{Var}(Y)$
en étudiant le signe de $t\mapsto\operatorname{Var}(X+tY)$. *(Piste : c'est un trinôme positif —
la démonstration exacte du [§ 2.1 du cours d'algèbre](../../../semestre1/algebre/02-cauchy-schwarz-et-angle.md).)*

**E4.7.** Une corrélation vaut $0{,}7$. Quelle **part de la variance** est expliquée ? Quel angle
géométrique cela représente-t-il ? *(Réponses : $49\,\%$ et $45{,}6°$.)*

**E4.8 — orientée finance.** Sur trois séries obtenues avec `import_societe.py` :
1. calculer $\Sigma$ et la matrice de corrélation des rendements quotidiens ;
2. calculer la volatilité du portefeuille équipondéré par $w^{\top}\Sigma w$, et la comparer à la
   moyenne des volatilités individuelles ;
3. refaire le calcul sur les 20 % de séances les plus baissières du marché.
*La diversification vous protège-t-elle davantage, ou moins, en période de crise ?*

---

## 4.8 À retenir

- **$\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)$**, et $\operatorname{Cov}(X,X)=\operatorname{Var}(X)$ :
  la variance est un cas particulier.
- **Symétrique, bilinéaire, positive** — les trois propriétés d'un produit scalaire, ce qui n'est
  pas une image : voir le
  [module 9 du cours d'algèbre](../../../semestre1/algebre/09-covariance-et-produit-scalaire.md).
- **La bilinéarité donne $\operatorname{Var}(w^{\top}X)=w^{\top}\Sigma w$** sans aucune
  hypothèse — c'est la variance d'un portefeuille, et toute la diversification.
- **$\rho=\operatorname{Cov}/(\sigma_X\sigma_Y)\in[-1,1]$** par Cauchy–Schwarz, sans dimension,
  égal à $\pm1$ **si et seulement si** le lien est **affine exact**.
- ⚠️ **Quatre cécités** : décorrélé ≠ indépendant ; $\rho$ ≠ pente ; $\rho$ ≠ causalité ; $\rho$
  est très instable sur petit échantillon.
- ⭐ **Une seule famille échappe à la première** : le vecteur gaussien
  ([module 10](10-decorrelation-et-independance.md)).

---

⬅️ [Module 3 — Variance et moments](03-variance-et-moments.md) ·
➡️ [Module 5 — La fonction génératrice des moments](05-fonction-generatrice-des-moments.md) ·
🏠 [Sommaire](README.md)
