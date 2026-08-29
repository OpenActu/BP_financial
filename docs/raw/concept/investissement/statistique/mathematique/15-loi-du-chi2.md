# Module 15 — La loi du $\chi^2$

**Durée : 1 h 30.** Prérequis : modules [7](07-loi-normale-et-ses-transformees.md) et
[11](11-invariance-par-rotation-et-lemme-de-projection.md).

> **La question traitée.** Quelle est la loi de $\sum_i Z_i^2$ pour des gaussiennes standard
> indépendantes — et, surtout, quelle est celle de la **variance empirique** $S^2$ ?

**Ce qui est en jeu.** Cette loi est celle de toute **somme de carrés** en statistique. Elle est
le second ingrédient — avec la normale — de la construction de la loi de Student.

---

## 15.1 Définition

> **Définition.** Soient $Z_1,\dots,Z_k$ i.i.d. $\mathcal N(0,1)$. La variable
> $$K=\sum_{i=1}^k Z_i^2$$
> suit la **loi du khi-deux à $k$ degrés de liberté**, notée $K\sim\chi^2(k)$.

Trois observations immédiates :

- $K\ge 0$ : le support est $\mathbb R^+$. La loi est donc nécessairement **asymétrique**.
- $k$ est un **entier** (pour l'instant — voir § 15.6).
- $\chi^2(1)$ est la loi du **carré** d'une $\mathcal N(0,1)$, et non celle d'une gaussienne.

### Lecture géométrique — celle qu'il faut retenir

Si $\mathbf Z=(Z_1,\dots,Z_k)$ est un vecteur gaussien standard de $\mathbb R^k$
([§ 9.2](09-vecteur-gaussien.md)), alors

$$K=\|\mathbf Z\|^2$$

**La loi du $\chi^2$ est la loi du carré de la norme d'un vecteur gaussien standard.** Le nombre
de degrés de liberté est la **dimension de l'espace** dans lequel ce vecteur vit.

> 🔑 C'est cette lecture, et non la formule, qui rend le
> [module 16](16-theoreme-de-fisher-cochran.md) intelligible. Quand un vecteur gaussien est
> contraint à vivre dans un sous-espace de dimension $d < k$, le carré de sa norme suit un
> $\chi^2(d)$ — la dimension a été réduite, les degrés de liberté avec elle. C'est exactement
> l'énoncé du [lemme de projection](11-invariance-par-rotation-et-lemme-de-projection.md).

---

## 15.2 Propriétés

| Propriété                 | Énoncé                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------- |
| Espérance                 | $E(K)=k$                                                                                           |
| Variance                  | $\operatorname{Var}(K)=2k$                                                                         |
| Additivité                | $K_1\sim\chi^2(k_1)$, $K_2\sim\chi^2(k_2)$, indépendantes $\Rightarrow K_1+K_2\sim\chi^2(k_1+k_2)$ |
| Asymétrie                 | $\gamma_1=\sqrt{8/k}$ — décroît vers 0 quand $k$ croît                                             |
| Mode                      | $k-2$ pour $k\ge 2$ ; en 0 pour $k\le 2$                                                           |
| Comportement asymptotique | $\dfrac{K-k}{\sqrt{2k}}\xrightarrow{\mathcal L}\mathcal N(0,1)$ — [§ 11bis.7](11bis-convergence-en-loi.md)                                    |

### Démonstration de $E(K)=k$ et $\operatorname{Var}(K)=2k$

Pour $Z\sim\mathcal N(0,1)$ : $E(Z^2)=\operatorname{Var}(Z)+E(Z)^2=1$, d'où par linéarité
$E(K)=k$.

Pour la variance, il faut le moment d'ordre 4 de la gaussienne, $E(Z^4)=3$ — établi au
[§ 7.4](07-loi-normale-et-ses-transformees.md) :
$$\operatorname{Var}(Z^2)=E(Z^4)-E(Z^2)^2=3-1=2,$$
puis, les $Z_i^2$ étant indépendants, $\operatorname{Var}(K)=2k$.

### Démonstration de l'additivité

Immédiate par la définition : concaténer $k_1$ carrés et $k_2$ carrés de gaussiennes standard
indépendantes donne $k_1+k_2$ tels carrés. **C'est une propriété de comptage**, pas un calcul —
et c'est ce qui la rend si maniable.

⚠️ Comparez avec le [module 8](08-addition-de-lois-et-stabilite-gaussienne.md), où la stabilité
gaussienne demandait un calcul de FGM. Ici, la définition suffit.

### La dernière ligne du tableau est un TCL

$\frac{K-k}{\sqrt{2k}}\to\mathcal N(0,1)$ n'est rien d'autre que le
[TCL du module 12](12-theoreme-central-limite.md) appliqué à la somme des $Z_i^2$, qui sont i.i.d.
de moyenne 1 et de variance 2.

---

## 15.3 Densité

> 📐 **D'où vient cette densité.** Pour $k=1$, elle s'obtient en une ligne par changement de
> variable sur $Y=Z^2$ — avec le **facteur 2** des deux antécédents $\pm\sqrt y$ :
> [§ 9.3 du cours de dérivation et intégration](../../analyse/derivation-et-integration/09-changement-de-variable-et-densites.md).
> La constante $2^{k/2}\Gamma(k/2)$ est celle qui normalise l'intégrale à 1
> ([§ 4.4](../../analyse/derivation-et-integration/04-integrales-generalisees-et-moments.md)).

Pour $x>0$ :
$$f_k(x)=\frac{1}{2^{k/2}\,\Gamma(k/2)}\;x^{k/2-1}\,e^{-x/2}$$

> ⚠️ **À connaître, pas à mémoriser.** Retenez seulement que $\chi^2(k)=\text{Gamma}(k/2,\,1/2)$
> — c'est ce qui explique l'additivité et le calcul des moments. Aucun exercice de ce cours ne
> demande de manipuler cette expression à la main.

Deux cas particuliers utiles :
- $\chi^2(2)$ est la loi **exponentielle** de paramètre $1/2$ ;
- $\chi^2(1)$ a une densité qui **diverge en $0^+$** — conséquence directe du fait que $Z^2$ se
  concentre près de 0 lorsque $Z$ y est.

---

## 15.4 Le lien avec la variance empirique

C'est la raison d'être du module. Anticipons le résultat que le
[module 16](16-theoreme-de-fisher-cochran.md) démontrera :

> Si $X_1,\dots,X_n$ sont i.i.d. $\mathcal N(\mu,\sigma^2)$, alors
> $$\frac{(n-1)S^2}{\sigma^2}\;\sim\;\chi^2(n-1).$$

### Le cas facile — pour comprendre d'où vient le $n$, avant le $n-1$

Supposons $\mu$ **connu** et posons $\tilde S^2=\frac1n\sum_i (X_i-\mu)^2$. Alors
$$\frac{n\tilde S^2}{\sigma^2}=\sum_{i=1}^n\left(\frac{X_i-\mu}{\sigma}\right)^2
=\sum_{i=1}^n Z_i^2\;\sim\;\chi^2(n)$$
puisque les $\frac{X_i-\mu}{\sigma}$ sont i.i.d. $\mathcal N(0,1)$. **Ici, $n$ degrés de liberté**,
sans difficulté.

### Pourquoi le cas réel donne $n-1$

Dans la vraie vie, $\mu$ est inconnu et on le remplace par $\bar X$. Les écarts
$(X_i-\bar X)_i$ vérifient alors **une contrainte linéaire** :
$$\sum_{i=1}^n (X_i-\bar X)=0.$$
Connaissant $n-1$ d'entre eux, le dernier est déterminé. Le vecteur des écarts ne se promène
donc pas dans $\mathbb R^n$ mais dans un **hyperplan de dimension $n-1$** — et, par la lecture
géométrique du § 15.1, le carré de sa norme suit un $\chi^2(n-1)$.

> 🔑 **Un degré de liberté a été consommé par l'estimation de $\mu$.** C'est la formulation qui
> se généralise : estimer $p$ paramètres coûte $p$ degrés de liberté. La géométrie sous-jacente
> est celle du
> [module 5 du cours d'algèbre](../../algebre/05-supplementaire-orthogonal-et-dimension.md).

### Conséquence : pourquoi le diviseur $n-1$

De $\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)$ et de $E(\chi^2(k))=k$ on tire
$$E\!\left(\frac{(n-1)S^2}{\sigma^2}\right)=n-1 \quad\Longrightarrow\quad E(S^2)=\sigma^2 .$$

Le diviseur $n-1$ **rend l'estimateur sans biais**. Avec un diviseur $n$, on obtiendrait
$E(S^2)=\frac{n-1}{n}\sigma^2$ : une sous-estimation systématique de la variance.

⚠️ **Deux mises en garde.**
1. Le document [`modele.md`](../../modele/modele.md) normalise par $n$ — c'est **légitime** dans son
   cadre, qui est déterministe : il n'y a aucun paramètre à estimer sans biais, seulement des
   moments empiriques à décrire. Les deux conventions ne s'opposent pas, elles répondent à des
   questions différentes.
2. $S^2$ est sans biais, mais **$S$ ne l'est pas** : $E(S)=c_4(n)\,\sigma<\sigma$, par concavité
   de la racine (inégalité de Jensen, chiffrée au
   [§ 5.4 du cours d'analyse](../../analyse/convexite/05-jensen-probabiliste.md) : $-2{,}7\,\%$ à $n=10$,
   $-0{,}9\,\%$ à $n=30$). Il n'existe pas d'estimateur simple et sans biais de $\sigma$ — et
   c'est précisément le défaut que la
   [loi de Student](../loi-de-student/README.md) est construite pour absorber.

---

## 15.5 Simulations

### S15.1 — Vérifier la définition, l'espérance et la variance

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(2)
for k in (1, 5, 30):
    K = (rng.standard_normal((200_000, k)) ** 2).sum(axis=1)
    print(f"k={k:3d} | moyenne={K.mean():7.3f} (théorie {k})"
          f" | variance={K.var():8.3f} (théorie {2*k})"
          f" | asymétrie={stats.skew(K):.3f} (théorie {np.sqrt(8/k):.3f})")
```

### S15.2 — Voir la normalisation progressive

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(13, 3.5))
for ax, k in zip(axes, (1, 5, 30)):
    K = (rng.standard_normal((100_000, k)) ** 2).sum(axis=1)
    ax.hist(K, bins=120, density=True, alpha=.4)
    x = np.linspace(1e-6, K.max(), 400)
    ax.plot(x, stats.chi2.pdf(x, k))
    ax.set_title(f"$\\chi^2({k})$")
plt.tight_layout(); plt.show()
```

À $k=1$, la densité explose en 0 ; à $k=5$, elle est franchement asymétrique ; à $k=30$, elle
ressemble déjà à une gaussienne. C'est l'illustration du dernier point du tableau du § 15.2.

### S15.3 — Vérifier le résultat central (celui que le module 16 démontrera)

```python
n, SIGMA = 8, 2.5
X = rng.normal(loc=17.0, scale=SIGMA, size=(200_000, n))
S2 = X.var(axis=1, ddof=1)
Q = (n - 1) * S2 / SIGMA ** 2

print(f"E(Q)   = {Q.mean():.3f}  (théorie {n-1})")
print(f"Var(Q) = {Q.var():.3f}  (théorie {2*(n-1)})")
print("test de Kolmogorov–Smirnov contre chi2(n-1) :",
      stats.kstest(Q, "chi2", args=(n - 1,)))
```

**Puis la contre-épreuve, essentielle** : refaites-la avec `ddof=0` (diviseur $n$). La moyenne
de $Q$ tombe à $n-1$ multiplié par $\frac{n-1}{n}$, et l'ajustement au $\chi^2(n-1)$ échoue. Le
$n-1$ n'est pas un ornement.

---

## 15.6 Compléments (culture, non exigibles)

- **Degrés de liberté non entiers.** La densité du § 15.3 a un sens pour tout $k>0$ réel. Cela
  sert à l'approximation de **Welch–Satterthwaite**, qui produit des degrés de liberté
  fractionnaires lors de la comparaison de deux moyennes.
- **$\chi^2$ décentré.** Si les $Z_i$ sont $\mathcal N(\mu_i,1)$ avec des $\mu_i$ non tous nuls,
  on obtient un $\chi^2$ **décentré**, de paramètre $\lambda=\sum_i\mu_i^2$. C'est la loi qui
  gouverne la **puissance** des tests : sous $H_1$, la statistique ne suit plus la loi centrale.
- **Autres emplois du $\chi^2$.** Test d'ajustement, test d'indépendance dans un tableau de
  contingence, test du rapport de vraisemblance. Ces usages sont **sans lien direct** avec le
  présent cours : n'en tirez pas l'idée qu'un même $k$ y signifie la même chose.

---

## 15.7 Exercices

**E15.1.** Démontrer $\operatorname{Var}(\chi^2(k))=2k$ en établissant d'abord $E(Z^4)=3$ (par
intégration par parties ou par la FGM — voir le
[§ 7.4](07-loi-normale-et-ses-transformees.md)).

**E15.2.** Soient $K_1\sim\chi^2(3)$ et $K_2\sim\chi^2(7)$ indépendantes. Donner la loi, l'espérance
et la variance de $K_1+K_2$. Vérifier par simulation.

**E15.3.** Un échantillon gaussien de taille $n=20$ donne $s^2=14{,}6$. Construire un IC à 90 %
de $\sigma^2$ en utilisant $\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(19)$.
*Indication :* l'intervalle
est$\left[\frac{(n-1)s^2}{\chi^2_{19;\,0{,}95}}\,;\, \frac{(n-1)s^2}{\chi^2_{19;\,0{,}05}}\right]$ —
et **il n'est pas symétrique** autour de$s^2$.
Expliquer pourquoi.

**E15.4.** Pourquoi l'IC de la question précédente n'est-il **pas** symétrique, alors que celui
d'une moyenne l'est ? *(Réponse attendue : parce que la loi du $\chi^2$ ne l'est pas.)*

**E15.5.** Vérifier numériquement que $\chi^2(2)$ est bien une loi exponentielle de paramètre
$1/2$. *(Piste : comparer les fonctions de répartition.)*

**E15.6 — orientée finance.** Sur une série de rendements quotidiens, estimer la volatilité
annualisée et en donner un IC à 95 % par la méthode de E15.3. Commenter la largeur obtenue sur
20 séances, puis sur 250. *Conclusion attendue : la volatilité est une grandeur bien plus mal
estimée qu'on ne le suppose habituellement.*

---

## 15.8 À retenir

- $\chi^2(k)$ = loi du **carré de la norme** d'un vecteur gaussien standard de $\mathbb R^k$.
- $E=k$, $\operatorname{Var}=2k$, **additive par comptage**, asymétrique, tend vers la normale.
- $\dfrac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)$ — **le $n-1$ vient d'une contrainte géométrique**
  ($\sum_i(X_i-\bar X)=0$), pas d'une convention.
- Estimer $p$ paramètres coûte $p$ degrés de liberté. Cette règle vaudra pour toute la suite.
- **$S^2$ est sans biais, $S$ ne l'est pas** — et c'est ce défaut que la loi de Student absorbe.

---

⬅️ [Module 14 — Dépendance et échec du TCL](14-dependance-et-echec-du-tcl.md) ·
➡️ [Module 16 — Théorème de Fisher–Cochran](16-theoreme-de-fisher-cochran.md) ·
🏠 [Sommaire](README.md)
