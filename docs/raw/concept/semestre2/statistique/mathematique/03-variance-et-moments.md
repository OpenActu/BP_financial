# Module 3 — Variance et moments ⭐

**Durée : 1 h 15.** Prérequis : modules [1](01-variable-aleatoire-et-loi.md) et
[2](02-esperance.md).

> **La question traitée.** L'espérance dit **où** la loi se situe. Quel nombre dit à quel point
> elle est **étalée** — et quels nombres disent le reste ?

**Ce qui est en jeu.** La variance a une propriété que l'espérance n'a pas : elle **n'est pas
linéaire**, et son additivité exige une hypothèse. C'est là qu'apparaît, pour la première fois du
cours, la différence entre variables dépendantes et indépendantes — celle qui décidera de tout au
[module 14](14-dependance-et-echec-du-tcl.md).

---

## 3.1 Définition

> **Définition.** La **variance** de $X$ est
> $$\operatorname{Var}(X)=E\Bigl(\bigl(X-E(X)\bigr)^2\Bigr)\;\ge\;0$$
> et l'**écart-type** est $\sigma_X=\sqrt{\operatorname{Var}(X)}$.

C'est l'**écart quadratique moyen à l'espérance**. Le carré n'est pas un choix esthétique : il
rend la quantité additive (§ 3.3) et différentiable, ce que $E|X-\mu|$ n'est pas.

### La formule de calcul — König–Huygens

$$\boxed{\;\operatorname{Var}(X)=E(X^2)-E(X)^2\;}$$

**Démonstration**, par la seule linéarité du [§ 2.2](02-esperance.md). En posant $\mu=E(X)$ :

$$E\bigl((X-\mu)^2\bigr)=E\bigl(X^2-2\mu X+\mu^2\bigr)=E(X^2)-2\mu E(X)+\mu^2=E(X^2)-\mu^2
\qquad\blacksquare$$

> 🔑 **On y reconnaît le Pythagore du [cours d'algèbre](../../../semestre1/algebre/README.md)**  ([§ 8.2](../../../semestre1/algebre/08-degres-de-liberte-et-centrage.md)) : $\|x\|^2=\|\bar x\mathbf 1\|^2+\|\tilde x\|^2$. Même identité, écrite dans deux cadres — l'un descriptif, l'autre probabiliste.

**Corollaire immédiat** : $E(X^2)\ge E(X)^2$, puisqu'une variance est positive. C'est le cas
$g(x)=x^2$ de l'inégalité de Jensen ([§ 2.5](02-esperance.md)).

⚠️ **La variance peut ne pas exister** alors même que l'espérance existe : il suffit que
$E(X^2)=\infty$. C'est le cas des lois de **Pareto** d'exposant $\le 2$, et cela suffit à priver
la loi de [TCL](12-theoreme-central-limite.md).

---

## 3.2 Ce que la variance fait des transformations affines

> **Propriété.** $\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X)$, donc $\sigma_{aX+b}=|a|\,\sigma_X$.

Deux lectures :

- **$b$ disparaît.** Translater ne change pas la dispersion. C'est exactement l'invariance par
  translation de la covariance empirique du [§ 11.2 du cours d'algèbre](../../../semestre1/algebre/11-covariance-et-produit-scalaire.md) : les deux formes
  sont aveugles au niveau.
- **$a$ entre au carré.** La variance n'est **pas** homogène à $X$ ; l'écart-type l'est. C'est
  pourquoi on rapporte toujours un $\sigma$, jamais un $\sigma^2$, quand on parle en unités
  réelles.

**La standardisation**, conséquence directe : pour $Z=\frac{X-\mu}{\sigma}$,

$$E(Z)=0\qquad\text{et}\qquad \operatorname{Var}(Z)=1$$

C'est l'étape 0 de toutes les démonstrations du cours.

---

## 3.3 L'additivité — et sa condition ⭐

> **Théorème.**
> $$\operatorname{Var}(X+Y)=\operatorname{Var}(X)+2\operatorname{Cov}(X,Y)+\operatorname{Var}(Y)$$
> et donc, **si $X$ et $Y$ sont décorrélées** (en particulier si elles sont indépendantes) :
> $$\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)$$

Le terme $\operatorname{Cov}(X,Y)$ est l'objet du [module 4](04-covariance-et-correlation.md) ; retenez pour l'instant qu'il vaut 0 sous indépendance.

> ⚠️ **C'est la rupture avec l'espérance.** $E(X+Y)=E(X)+E(Y)$ **sans aucune hypothèse**
> ([§ 2.2](02-esperance.md)) ; $\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)$ **seulement si** le terme croisé s'annule. Toute la fragilité de l'inférence tient dans cette différence.

### La conséquence : la loi d'échantillonnage de la moyenne, moitié droite

Pour $X_1,\dots,X_n$ i.i.d. de variance $\sigma^2$ :

$$\operatorname{Var}(\bar X)=\operatorname{Var}\!\left(\frac1n\sum_i X_i\right)
=\frac{1}{n^2}\sum_i\operatorname{Var}(X_i)=\frac{n\sigma^2}{n^2}$$

$$\boxed{\;\operatorname{Var}(\bar X)=\frac{\sigma^2}{n}
\qquad\text{et}\qquad \sigma_{\bar X}=\frac{\sigma}{\sqrt n}\;}$$

$\sigma/\sqrt n$ s'appelle l'**erreur type**. C'est le nombre le plus important de tout le
cours : il gouverne la largeur de tout intervalle de confiance
([§ 18.3](18-intervalle-de-confiance.md)) et la vitesse du TCL.

> 🔑 **Le $\frac{1}{n^2}$ vient du carré du § 3.2, le $n$ de l'additivité du § 3.3.** Le
> $\frac1{\sqrt n}$ n'est donc pas une convention : c'est ce qui reste quand on divise $n$ par
> $n^2$. Et il **exige l'indépendance** — c'est très exactement ce que le
> [module 14](14-dependance-et-echec-du-tcl.md) fera sauter.

---

## 3.4 Les moments

> **Définition.** Le **moment d'ordre $k$** de $X$ est $m_k=E(X^k)$ ; le **moment centré
> d'ordre $k$** est $\mu_k=E\bigl((X-E(X))^k\bigr)$.

Espérance et variance sont donc les deux premiers : $m_1=E(X)$ et $\mu_2=\operatorname{Var}(X)$.
Les deux suivants portent des noms, car ils décrivent la **forme** de la loi.

### Asymétrie et kurtosis

$$\gamma_1=\frac{\mu_3}{\sigma^3}\qquad\text{(asymétrie, \emph{skewness})}
\qquad\qquad
\beta_2=\frac{\mu_4}{\sigma^4}\qquad\text{(kurtosis)}$$

Ils sont normalisés par $\sigma^k$ pour être **sans dimension** : ils ne changent pas si l'on
convertit des euros en dollars, ce qui est la seule façon de comparer deux lois de dispersions
différentes.

| Grandeur | Loi symétrique | Loi étalée à droite | Gaussienne |
|---|---|---|---|
| $\gamma_1$ | $0$ | $>0$ | $0$ |
| $\beta_2$ | — | — | **$3$** (la référence) |

Le **kurtosis excédentaire** $\beta_2-3$ est ce qu'affichent la plupart des logiciels : positif
signifie « queues plus épaisses que la gaussienne ».

| Loi | $\gamma_1$ | $\beta_2$ |
|---|---|---|
| Normale | 0 | 3 |
| Uniforme | 0 | 1,8 |
| Exponentielle | **2** | 9 |
| Log-normale $\mathcal{LN}(0,1)$ | **6,18** | 113,9 |

> 🔑 **Ces deux colonnes décident de tout au [module 13](13-portee-et-limites-du-tcl.md).** La
> règle $\gamma_1(\bar X_n)=\gamma_1(X)/\sqrt n$ y remplace le « $n\ge 30$ » des manuels, et
> l'écart entre 2 et 6,18 explique à lui seul pourquoi la log-normale exige **dix fois plus**
> d'observations que l'exponentielle.

⚠️ **Un moment d'ordre $k$ n'existe que si $E|X|^k<\infty$**, et les conditions se durcissent avec
$k$ : une loi peut avoir une espérance sans variance, une variance sans asymétrie. C'est
exactement ce que demande, en plus du TCL, l'inégalité de
[Berry–Esseen](13-portee-et-limites-du-tcl.md) — un moment d'ordre 3.

---

## 3.5 Ce que deux nombres ne disent pas

> ⚠️ **Espérance et variance ne caractérisent pas une loi.** Une infinité de lois partagent les
> mêmes.

C'est la limite structurelle des modules 2 et 3, et la raison d'être des modules 5 et 6 : la
**FGM** et la **fonction caractéristique**, elles, caractérisent la loi — parce qu'elles encodent
**tous** les moments à la fois ([§ 5.2](05-fonction-generatrice-des-moments.md)).

La simulation S3.3 exhibe quatre lois de mêmes espérance et variance dont les probabilités de
queue vont de $0$ à $1{,}4\,\%$.

> 🔑 **En finance, cet écart est le sujet.** Deux portefeuilles de même rendement espéré et de
> même volatilité peuvent avoir des risques de perte extrême sans commune mesure. La volatilité
> ne mesure le risque que si l'on a déjà admis que la loi est gaussienne — et le
> [module 9](09-vecteur-gaussien.md) montre à quel point c'est une hypothèse forte.

---

## 3.6 Simulations

### S3.1 — König–Huygens, et l'effet des transformations affines

```python
import numpy as np

rng = np.random.default_rng(3)
N = 1_000_000
X = rng.exponential(2.0, N)                   # E = 2, Var = 4

print(f"Var directe   = {np.mean((X - X.mean())**2):.4f}")
print(f"E(X²) - E(X)² = {np.mean(X**2) - X.mean()**2:.4f}   (theorie 4)")

a, b = -3.0, 100.0
Y = a * X + b
print(f"\nVar(aX+b) = {Y.var():9.4f}   a²Var(X) = {a**2 * X.var():9.4f}")
print(f"E(aX+b)   = {Y.mean():9.4f}   aE(X)+b  = {a * X.mean() + b:9.4f}")
print(f"-> b decale l'esperance et disparait de la variance")
```

### S3.2 — L'additivité, et ce qui la détruit

```python
n = 25
def erreur_type(nom, tirage):
    Xb = np.array([tirage().mean() for _ in range(30_000)])
    return f"{nom:32s} std(Xbar) = {Xb.std():.4f}"

SG = 3.0
print(erreur_type("i.i.d.", lambda: rng.normal(0, SG, n)),
      f"  <- theorie sigma/sqrt(n) = {SG/np.sqrt(n):.4f}")

# dépendance positive : la variance de la moyenne EXPLOSE
phi = 0.8
def ar1():
    e = rng.normal(0, SG * np.sqrt(1 - phi**2), n)
    x = np.empty(n); x[0] = rng.normal(0, SG)
    for i in range(1, n):
        x[i] = phi * x[i-1] + e[i]
    return x
print(erreur_type(f"AR(1) phi={phi} (meme sigma)", ar1),
      f"  <- x{np.sqrt((1+phi)/(1-phi)):.2f} !")

# dépendance négative : elle s'effondre
print(erreur_type("alternee (dep. negative)",
                  lambda: rng.normal(0, SG, n) * (-1)**np.arange(n) + 0))
```

**Les trois séries ont la même variance marginale $\sigma^2=9$.** Seule la première donne
$\sigma/\sqrt n$. L'AR(1) en donne **2,70 fois plus** à $n=25$ — et le rapport monte vers sa
valeur asymptotique $\sqrt{\frac{1+\varphi}{1-\varphi}}=3$ quand $n$ croît (2,95 à $n=100$,
3,00 à $n=400$). **Augmenter $n$ n'y change donc rien : l'erreur ne s'estompe pas, elle se
stabilise** ([module 14](14-dependance-et-echec-du-tcl.md)).

### S3.3 — Deux nombres ne suffisent pas

```python
from scipy import stats

MU, SG = 0.0, 1.0
lois = {
    "normale":       rng.normal(MU, SG, N),
    "uniforme":      rng.uniform(MU - SG*np.sqrt(3), MU + SG*np.sqrt(3), N),
    "Laplace":       rng.laplace(MU, SG/np.sqrt(2), N),
    "t de Student 5": stats.t.rvs(5, size=N, random_state=3) / np.sqrt(5/3),
}
print(f"{'loi':<16}{'E':>8}{'std':>8}{'skew':>9}{'kurtosis':>10}{'P(|X|>3)':>11}")
for nom, V in lois.items():
    print(f"{nom:<16}{V.mean():>8.3f}{V.std():>8.3f}{stats.skew(V):>9.3f}"
          f"{stats.kurtosis(V, fisher=False):>10.2f}{np.mean(np.abs(V) > 3):>11.5f}")
```

Les colonnes `E` et `std` sont identiques à la troisième décimale. **La dernière ne l'est pas
du tout** : $0$ pour l'uniforme, $0{,}27\,\%$ pour la normale, $1{,}44\,\%$ pour la Laplace —
**cinq fois la valeur gaussienne**, sur des lois de même dispersion. Espérance et variance ne
disent rien du risque extrême.

---

## 3.7 Exercices

**E3.1.** Démontrer $\operatorname{Var}(X)=E(X^2)-E(X)^2$ par la seule linéarité, puis
$\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X)$.

**E3.2.** Calculer $\operatorname{Var}(X)$ pour une Bernoulli $\mathcal B(p)$. *Pour quelle
valeur de $p$ est-elle maximale, et pourquoi est-ce intuitif ?* **(Réponse : $p=1/2$.)**

**E3.3.** Démontrer $\operatorname{Var}(\bar X)=\sigma^2/n$ en explicitant **où** l'indépendance
est utilisée. *Que devient le résultat si $\operatorname{Cov}(X_i,X_j)=c\ne0$ pour tout
$i\ne j$ ?* **(Réponse : $\frac{\sigma^2}{n}+\frac{n-1}{n}c$ — qui ne tend pas vers 0.)**

**E3.4.** Une loi de Pareto de paramètre $\alpha$ a une densité $\propto x^{-\alpha-1}$ sur
$[1,\infty)$. Pour quels $\alpha$ l'espérance existe-t-elle ? Et la variance ? *(Réponses :
$\alpha>1$ et $\alpha>2$.)*

**E3.5.** Montrer que $\gamma_1$ et $\beta_2$ sont invariants par transformation affine
croissante. *Pourquoi cette invariance est-elle indispensable pour comparer deux lois ?*

**E3.6.** Vérifier que le kurtosis d'une gaussienne vaut 3, sachant $E(Z^4)=3$
([§ 7.4](07-loi-normale-et-ses-transformees.md)). *Que vaut son kurtosis excédentaire ?*

**E3.7 — orientée finance.** Sur les rendements quotidiens d'un titre obtenus avec
`import_societe.py` :
1. estimer $\gamma_1$ et $\beta_2$ ;
2. comparer aux valeurs gaussiennes (0 et 3) ;
3. calculer la proportion de jours à plus de 3 écarts-types, et la comparer à la valeur
   gaussienne de $0{,}27\,\%$.
*Combien de « krachs à 5 sigma » un modèle gaussien prévoit-il par siècle, et combien en
observe-t-on ?*

---

## 3.8 À retenir

- **$\operatorname{Var}(X)=E((X-\mu)^2)=E(X^2)-E(X)^2$** — c'est le Pythagore du cours d'algèbre,
  écrit en probabilité.
- **$\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X)$** : $b$ disparaît, $a$ entre au carré.
- ⭐ **L'additivité exige la décorrélation** — c'est **la** différence avec la linéarité de
  l'espérance, qui n'exige rien.
- ⭐ **$\operatorname{Var}(\bar X)=\sigma^2/n$, donc erreur type $=\sigma/\sqrt n$.** Le nombre
  central du cours — et il **suppose l'indépendance**.
- **Moments d'ordre 3 et 4** : asymétrie $\gamma_1$ et kurtosis $\beta_2$ (référence gaussienne :
  **3**). Sans dimension, donc comparables.
- ⚠️ **Espérance et variance ne caractérisent pas une loi.** D'où les transformées des modules 5
  et 6.

---

⬅️ [Module 2 — L'espérance](02-esperance.md) ·
➡️ [Module 4 — Covariance et corrélation](04-covariance-et-correlation.md) ·
🏠 [Sommaire](README.md)
