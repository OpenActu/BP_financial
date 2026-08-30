# Module 16 — Théorème de Fisher–Cochran ⭐

**Durée : 2 h.** Prérequis : modules [11](11-invariance-par-rotation-et-lemme-de-projection.md) et
[15](15-loi-du-chi2.md).

C'est le **point d'aboutissement du cours**. Il fait la différence entre savoir appliquer et
comprendre : toute l'inférence gaussienne sur petit échantillon en découle presque
mécaniquement ; sans lui, elle reste une collection de recettes.

Prenez le temps. Si un seul module doit être travaillé en profondeur, c'est celui-ci.

---

## 16.1 Énoncé

> **Théorème (Fisher–Cochran).** Soient $X_1,\dots,X_n$ i.i.d. $\mathcal N(\mu,\sigma^2)$, avec
> $n\ge 2$. Posons
> $$\bar X=\frac1n\sum_{i=1}^n X_i, \qquad S^2=\frac{1}{n-1}\sum_{i=1}^n (X_i-\bar X)^2 .$$
> Alors :
>
> **(i)** $\displaystyle \bar X \sim \mathcal N\!\left(\mu,\;\frac{\sigma^2}{n}\right)$
>
> **(ii)** $\displaystyle \frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)$
>
> **(iii)** $\bar X$ et $S^2$ sont **indépendantes**.

Le point (i) est élémentaire — c'est le
[§ 8.3](08-addition-de-lois-et-stabilite-gaussienne.md). Les points (ii) et (iii) sont le contenu
réel du théorème, et **(iii) est le plus remarquable** : $\bar X$ et $S^2$ sont calculées sur les
mêmes données.

> ⚠️ **Les trois points sont faux hors du cadre gaussien.** (i) devient asymptotique par le
> [TCL](12-theoreme-central-limite.md), (ii) est franchement faux, et (iii) l'est aussi.
> Retenez ce point : c'est **le** moment où l'hypothèse de normalité est réellement
> indispensable — et c'est le seul.

---

## 16.2 La maquette en dimension 2

Avant la démonstration générale, reprenons l'exemple du
[§ 10.3](10-decorrelation-et-independance.md), qui en contient toute la structure.

Soient $Z_1,Z_2$ i.i.d. $\mathcal N(0,1)$. Posons
$$U=\frac{Z_1+Z_2}{\sqrt 2}, \qquad W=\frac{Z_1-Z_2}{\sqrt 2}.$$

Trois constats :

1. $U$ et $W$ sont **gaussiennes centrées réduites** (combinaisons linéaires de gaussiennes, de
   variance $\frac{1+1}{2}=1$).
2. $\operatorname{Cov}(U,W)=\frac{1}{2}\bigl(\operatorname{Var}(Z_1)-\operatorname{Var}(Z_2)\bigr)=0$,
   et comme $(U,W)$ est un **vecteur gaussien**, cela entraîne l'**indépendance**
   ([§ 10.2](10-decorrelation-et-independance.md)).
3. $U^2+W^2 = Z_1^2+Z_2^2$ : la transformation **conserve la norme**.

Or $\bar Z = \frac{Z_1+Z_2}{2}=\frac{U}{\sqrt 2}$ ne dépend que de $U$, tandis que
$$\sum_{i=1}^2 (Z_i-\bar Z)^2 = \frac{(Z_1-Z_2)^2}{2}=W^2$$
ne dépend que de $W$. **Donc $\bar Z \perp\!\!\!\perp S^2$, et $\frac{S^2}{1}=W^2\sim\chi^2(1)=\chi^2(n-1)$.**

Le théorème est démontré pour $n=2$. La démonstration générale ne fait qu'étendre ce mécanisme
à $n$ dimensions : **une rotation qui envoie une direction sur la moyenne et les $n-1$ autres
sur les écarts.**

---

## 16.3 Démonstration générale — voie géométrique

### Étape 1 — Se ramener au cas standard

Posons $Z_i=\frac{X_i-\mu}{\sigma}$. Alors $\mathbf Z=(Z_1,\dots,Z_n)$ est un **vecteur gaussien
standard** de $\mathbb R^n$, et

$$\bar X = \mu+\sigma\bar Z, \qquad (n-1)S^2 = \sigma^2\sum_{i=1}^n (Z_i-\bar Z)^2 .$$

Il suffit donc de démontrer le théorème pour $\mu=0$, $\sigma=1$ : tout le reste est affine.

### Étape 2 — La décomposition orthogonale

Soit $\mathbf 1=(1,\dots,1)\in\mathbb R^n$, et posons
$$D=\text{Vect}(\mathbf 1) \quad (\dim D=1), \qquad H=D^\perp \quad (\dim H=n-1).$$

La projection orthogonale de $\mathbf Z$ sur $D$ vaut
$$P_D(\mathbf Z)=\frac{\langle \mathbf Z,\mathbf 1\rangle}{\|\mathbf 1\|^2}\,\mathbf 1
=\frac{\sum_i Z_i}{n}\,\mathbf 1=\bar Z\,\mathbf 1 ,$$
et la projection sur $H$ est le **vecteur des écarts**
$$P_H(\mathbf Z)=\mathbf Z-\bar Z\,\mathbf 1 = (Z_i-\bar Z)_{1\le i\le n}.$$

Le théorème de Pythagore donne alors la décomposition fondamentale :
$$\underbrace{\|\mathbf Z\|^2}_{\sum_i Z_i^2}
=\underbrace{\|P_D(\mathbf Z)\|^2}_{n\bar Z^2}
+\underbrace{\|P_H(\mathbf Z)\|^2}_{\sum_i (Z_i-\bar Z)^2}$$

➡️ **Cette étape est purement algébrique** : elle est établie en détail, sans aucune probabilité,
au [module 5 du cours d'algèbre](../../../semestre1/algebre/05-supplementaire-orthogonal-et-dimension.md).

### Étape 3 — Le lemme gaussien

C'est le [lemme de projection du § 11.3](11-invariance-par-rotation-et-lemme-de-projection.md),
rappelé ici :

> **Lemme.** Soit $\mathbf Z$ un vecteur gaussien standard de $\mathbb R^n$ et
> $\mathbb R^n=F\oplus F^\perp$ une décomposition orthogonale, $\dim F = d$. Alors :
> - $P_F(\mathbf Z)$ et $P_{F^\perp}(\mathbf Z)$ sont **indépendants** ;
> - $\|P_F(\mathbf Z)\|^2\sim\chi^2(d)$ et $\|P_{F^\perp}(\mathbf Z)\|^2\sim\chi^2(n-d)$.

⚠️ **Tout le contenu probabiliste du théorème est ici, et nulle part ailleurs.** Les étapes 1, 2
et 4 sont de l'algèbre et de la substitution.

### Étape 4 — Conclusion

Appliquons le lemme à $F=D$ (donc $d=1$) :

- $\|P_D(\mathbf Z)\|^2=n\bar Z^2\sim\chi^2(1)$ — soit $\sqrt n\,\bar Z\sim\mathcal N(0,1)$, ce qui
  redonne **(i)** ;
- $\|P_H(\mathbf Z)\|^2=\sum_i(Z_i-\bar Z)^2\sim\chi^2(n-1)$, et en revenant aux $X_i$ :
  $$\frac{(n-1)S^2}{\sigma^2}=\sum_i\left(\frac{X_i-\bar X}{\sigma}\right)^2\sim\chi^2(n-1)
  \qquad\text{soit \textbf{(ii)}} ;$$
- $P_D(\mathbf Z)$ et $P_H(\mathbf Z)$ sont indépendants ; or $\bar X$ est fonction du premier et
  $S^2$ du second, d'où **(iii)**. $\blacksquare$

---

## 16.4 Les trois points à avoir vraiment compris

### ① Pourquoi $n-1$ et pas $n$

Le vecteur des écarts $(X_i-\bar X)_i$ **ne se promène pas librement dans $\mathbb R^n$**. Il est
astreint à l'hyperplan $H$ d'équation $\sum_i h_i=0$, de dimension $n-1$ — parce que la somme
des écarts à la moyenne est nulle **par construction**, pas par hasard.

Autrement dit : connaissant $n-1$ écarts, le dernier est entièrement déterminé. Il n'y a que
$n-1$ quantités réellement libres.

> 🔑 **Un degré de liberté a été consommé par l'estimation de $\mu$ via $\bar X$.** C'est une
> **contrainte géométrique**, pas une correction cosmétique ni un artifice pour débiaiser.
> Le débiaisage ($E(S^2)=\sigma^2$) en est la *conséquence*, non la cause.

Cette formulation se généralise directement : **estimer $p$ paramètres consomme $p$ degrés de
liberté**, parce que cela impose $p$ contraintes linéaires au vecteur des résidus, qui vit alors
dans un sous-espace de dimension $n-p$.

### ② Pourquoi l'indépendance est remarquable

$\bar X$ et $S^2$ sont deux fonctions des **mêmes** $n$ nombres. Rien ne laisse présager leur
indépendance ; on s'attendrait plutôt au contraire.

Elle vient d'une conjonction de deux faits :
- $\bar X$ est la projection sur $D$, $S^2$ une fonction de la projection sur $D^\perp$ —
  **deux directions orthogonales** ;
- pour un **vecteur gaussien**, les projections sur des sous-espaces orthogonaux sont
  indépendantes ([§ 11.3](11-invariance-par-rotation-et-lemme-de-projection.md)).

⚠️ **Le second point est spécifique à la gaussienne.** Pour une autre loi, les projections sont
décorrélées mais **pas indépendantes** — exactement comme dans la contre-épreuve exponentielle
du [§ 10.4](10-decorrelation-et-independance.md).

**Réciproque (culture) :** ce résultat caractérise la gaussienne. Si $X_1,\dots,X_n$ ($n\ge 2$)
sont i.i.d. et que $\bar X\perp\!\!\!\perp S^2$, alors leur loi **est** gaussienne
(théorème de Geary, 1936). L'indépendance de la moyenne et de la variance empiriques n'est pas
une propriété parmi d'autres : c'est une signature.

### ③ Ce que le TCL ne sauve pas

> 🔑 Le [TCL](12-theoreme-central-limite.md) rend $\bar X$ asymptotiquement gaussienne, donc il
> sauve **le point (i)** et, par voie de conséquence, le *niveau* des tests fondés dessus. Il ne
> sauve **ni (ii) ni (iii)**, qui sont faux hors du cadre gaussien **à tout $n$**.

Autrement dit : les résultats **exacts** de ce cours sont gaussiens ; leurs conséquences
**pratiques** survivent bien au-delà, et c'est le TCL qui explique pourquoi — mais le théorème
lui-même, non.

---

## 16.5 Simulations de validation

### S16.1 — Vérifier l'indépendance (le point (iii))

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(3)
n = 8
X = rng.normal(loc=5.0, scale=2.0, size=(200_000, n))
Xbar, S2 = X.mean(axis=1), X.var(axis=1, ddof=1)

print("corrélation :", np.corrcoef(Xbar, S2)[0, 1])       # ≈ 0

# La décorrélation ne suffit pas : vérifions que la loi de S2
# ne dépend PAS de la valeur de Xbar.
for lo, hi in [(4.0, 4.5), (4.9, 5.1), (5.5, 6.0)]:
    m = (Xbar > lo) & (Xbar < hi)
    print(f"Xbar∈[{lo},{hi}] → E(S²)={S2[m].mean():.3f}, "
          f"écart-type={S2[m].std():.3f}")   # identiques dans les trois tranches
```

### S16.2 — La contre-épreuve non gaussienne (à ne pas sauter)

```python
for nom, tirage in [("gaussienne", lambda s: rng.normal(0, 1, s)),
                    ("exponentielle", lambda s: rng.exponential(1.0, s)),
                    ("uniforme", lambda s: rng.uniform(-1, 1, s))]:
    X = tirage((200_000, n))
    Xbar, S2 = X.mean(axis=1), X.var(axis=1, ddof=1)
    tranches = [S2[(Xbar > q0) & (Xbar < q1)].mean()
                for q0, q1 in zip(np.quantile(Xbar, [.0, .45, .9]),
                                  np.quantile(Xbar, [.1, .55, 1.]))]
    print(f"{nom:14s} corr={np.corrcoef(Xbar, S2)[0,1]:+.4f}  "
          f"E(S²) par tranche de Xbar : {[round(t, 3) for t in tranches]}")
```

**Ce que vous devez observer.** Pour la gaussienne, les trois moyennes conditionnelles sont
identiques : $S^2$ ne « sait » rien de $\bar X$. Pour l'exponentielle, elles **croissent
nettement** avec $\bar X$ — l'indépendance est fausse, alors même que la corrélation reste
faible. Pour l'uniforme, elles varient dans l'autre sens.

> 🔑 C'est l'expérience la plus importante du cours. Elle montre que le théorème n'est pas une
> commodité technique dont on pourrait se passer : **il est propre à la gaussienne.**

### S16.3 — Vérifier (ii) et la décomposition de Pythagore

```python
n, SIGMA = 6, 3.0
X = rng.normal(0.0, SIGMA, size=(200_000, n))
Z = X / SIGMA
gauche = (Z ** 2).sum(axis=1)                       # ~ chi2(n)
d_part = n * Z.mean(axis=1) ** 2                    # ~ chi2(1)
h_part = ((Z - Z.mean(axis=1, keepdims=True)) ** 2).sum(axis=1)   # ~ chi2(n-1)

print("Pythagore, écart max :", np.abs(gauche - d_part - h_part).max())   # ≈ 1e-12
print("E(part D) =", d_part.mean(), " (théorie 1)")
print("E(part H) =", h_part.mean(), " (théorie", n - 1, ")")
print("KS chi2(n-1) :", stats.kstest(h_part, "chi2", args=(n - 1,)))
```

---

## 16.6 Exercices

**E16.1.** Rédiger entièrement la démonstration pour $n=3$, en explicitant une base
orthonormée adaptée à $D=\text{Vect}(1,1,1)$ et à son orthogonal. *(Une base classique de $H$ :
$\frac{1}{\sqrt2}(1,-1,0)$ et $\frac{1}{\sqrt6}(1,1,-2)$ — les contrastes de Helmert du
[§ 11.4](11-invariance-par-rotation-et-lemme-de-projection.md).)*

**E16.2.** Montrer que $\sum_i (X_i-\bar X)^2=\sum_i X_i^2 - n\bar X^2$. Interpréter cette
identité comme le théorème de Pythagore de l'étape 2.

**E16.3.** Déduire du théorème que $E(S^2)=\sigma^2$ et $\operatorname{Var}(S^2)=\frac{2\sigma^4}{n-1}$.
*Commenter la seconde : à $n=5$, l'écart-type de $S^2$ vaut-il une fraction négligeable de
$\sigma^2$ ?* **(Réponse : $\sqrt{2/4}\,\sigma^2\approx 0{,}71\sigma^2$ — l'estimation de la
variance est extraordinairement instable sur petit échantillon. C'est toute la raison d'être de
la [loi de Student](../../../semestre3/statistique/loi-de-student/README.md).)*

**E16.4.** Pourquoi le théorème exige-t-il $n\ge 2$ ? Que vaut $S^2$ pour $n=1$, et quelle serait
la loi correspondante ?

**E16.5.** Le vecteur des résidus d'une régression simple vérifie **deux** contraintes :
$\sum_i \hat e_i=0$ et $\sum_i t_i\hat e_i=0$. Dans quel sous-espace vit-il ? De quelle dimension ?
Quelle loi suit alors $\frac{1}{\sigma^2}\sum_i \hat e_i^{\,2}$ ?
*(Réponse : dimension $n-2$, loi $\chi^2(n-2)$.)*

**E16.6.** Où exactement, dans la démonstration du § 16.3, l'hypothèse gaussienne est-elle
utilisée ? *Répondre en citant l'étape et la ligne.*

---

## 16.7 À retenir

- **Le vecteur des écarts vit dans un hyperplan de dimension $n-1$.** De là viennent, d'un seul
  coup, la loi $\chi^2(n-1)$ et le diviseur $n-1$.
- **Projections orthogonales d'un vecteur gaussien ⟹ indépendance.** C'est le seul endroit du
  cours où la normalité est indispensable.
- **Estimer $p$ paramètres coûte $p$ degrés de liberté**, parce que cela impose $p$ contraintes
  linéaires aux résidus.
- **Le TCL sauve (i), pas (ii) ni (iii).** Les résultats exacts sont gaussiens ; leurs
  conséquences pratiques survivent au-delà.
- **Réciproque de Geary** : $\bar X\perp\!\!\!\perp S^2$ **caractérise** la gaussienne.

---

⬅️ [Module 15 — La loi du $\chi^2$](15-loi-du-chi2.md) ·
➡️ [Module 17 — Estimation et quantité pivotale](17-estimation-et-quantite-pivotale.md) ·
🏠 [Sommaire](README.md)
