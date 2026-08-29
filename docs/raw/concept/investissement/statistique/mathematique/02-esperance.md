# Module 2 — L'espérance ⭐

**Durée : 1 h 15.** Prérequis : [module 1](01-variable-aleatoire-et-loi.md).

> **La question traitée.** Comment résumer une loi entière par **un seul nombre** — et que
> perd-on en le faisant ?

**Ce qui est en jeu.** L'espérance est **linéaire**, et cette unique propriété fait plus de
travail que toutes les autres du cours réunies : elle ne demande **aucune hypothèse
d'indépendance**. C'est le point que le [module 3](03-variance-et-moments.md) ne pourra pas répéter.

---

## 2.1 Définition

> **Définition.** L'**espérance** de $X$ est
> $$E(X)=\sum_k k\,P(X=k) \quad\text{(discret)}
> \qquad\text{ou}\qquad
> E(X)=\int_{\mathbb R} x\,f(x)\,dx \quad\text{(continu)}$$
> lorsque la somme ou l'intégrale converge **absolument**.

C'est une **moyenne pondérée par les probabilités** : chaque valeur possible compte à hauteur de
sa vraisemblance.

⚠️ **La réserve de convergence n'est pas rhétorique.** Pour une loi de **Cauchy**, l'intégrale
diverge : $E(X)$ **n'existe pas**. Ce n'est pas une valeur infinie, c'est une absence — et elle
suffit à priver la loi de tout ce que ce cours construit
([§ 13.1](13-portee-et-limites-du-tcl.md)).

### Le lien avec la moyenne empirique

$$\bar x=\frac1n\sum_i x_i \qquad\text{contre}\qquad E(X)=\sum_k k\,P(X=k)$$

Ce sont **deux objets différents** qu'il ne faut jamais confondre :

|                                    | $\bar x$                              | $E(X)$                     |
| ---------------------------------- | ------------------------------------- | -------------------------- |
| Nature                             | Un **nombre calculé** sur les données | Un **paramètre** de la loi |
| Connu ?                            | Oui, toujours                         | **Non**, en général jamais |
| Varie d'un échantillon à l'autre ? | Oui                                   | Non — c'est une constante  |

> 🔑 **La loi des grands nombres est le pont entre les deux** : $\bar X_n\to E(X)$. Toute
> l'inférence de la partie VI consiste à quantifier ce que ce « $\to$ » laisse d'incertitude à
> $n$ fini.

---

## 2.2 La linéarité ⭐

> **Théorème.** Pour toutes variables aléatoires $X,Y$ d'espérance finie et tous réels $a,b$ :
> $$E(aX+bY)=a\,E(X)+b\,E(Y)$$

> ⚠️ **Aucune hypothèse d'indépendance.** C'est **la** propriété remarquable de l'espérance, et
> elle la distingue radicalement de la variance ([§ 3.3](03-variance-et-moments.md)), qui exige
> la décorrélation pour être additive.

**Conséquence immédiate — la loi d'échantillonnage de la moyenne, moitié gauche.** Pour
$X_1,\dots,X_n$ de même espérance $\mu$ :

$$E(\bar X)=E\!\left(\frac1n\sum_i X_i\right)=\frac1n\sum_i E(X_i)=\mu$$

$$\boxed{\;E(\bar X)=\mu\;}$$

On dit que$\bar X$ est un estimateur **sans biais** de$\mu$ : en moyenne sur tous les échantillons
possibles, il ne se trompe pas systématiquement.

> 🔑 **Ce résultat ne suppose ni normalité, ni indépendance, ni même que les $X_i$ aient une
> variance.** Il vaut pour des données autocorrélées, hétérogènes en dispersion, de n'importe
> quelle forme. C'est le seul résultat du cours dans ce cas — retenez-le comme tel.

---

## 2.3 Le théorème de transfert

Comment calculer $E(g(X))$ sans connaître la loi de $g(X)$ ?

> **Théorème de transfert.**
> $$E\bigl(g(X)\bigr)=\sum_k g(k)\,P(X=k)
> \qquad\text{ou}\qquad
> E\bigl(g(X)\bigr)=\int_{\mathbb R} g(x)\,f(x)\,dx$$

On intègre $g$ **contre la densité de $X$** : aucun changement de variable, aucune loi nouvelle à
déterminer.

> 🔑 **C'est l'outil qui rend tout le cours calculable.** $E(X^2)$ (la variance, [module 3](03-variance-et-moments.md)), $E(e^{tX})$ (la FGM,  [module 5](05-fonction-generatrice-des-moments.md)), $E(e^{itX})$ (la fonction caractéristique,  [module 6](06-fonction-caracteristique.md)) : chacune de ces définitions **est** une application du transfert. Sans lui, il faudrait déterminer la loi de $e^{tX}$ avant d'en prendre l'espérance.

---

## 2.4 L'espérance d'un produit : le cas où l'indépendance sert

> **Théorème.** Si $X$ et $Y$ sont **indépendantes**,
> $$E(XY)=E(X)\,E(Y)$$

⚠️ **La réciproque est fausse**, et c'est tout l'objet du [module 4](04-covariance-et-correlation.md) : $E(XY)=E(X)E(Y)$ signifie exactement $\operatorname{Cov}(X,Y)=0$, ce qui est **strictement plus faible** que l'indépendance.

| Opération          | Hypothèse requise                           |
| ------------------ | ------------------------------------------- |
| $E(X+Y)=E(X)+E(Y)$ | **Aucune**                                  |
| $E(XY)=E(X)E(Y)$   | Indépendance (ou seulement : décorrélation) |

> 🔑 **Ce théorème est le moteur du [module 5](05-fonction-generatrice-des-moments.md).**  « Somme → produit » n'est rien d'autre que
> $E(e^{t(X+Y)})=E(e^{tX}e^{tY})=E(e^{tX})E(e^{tY})$ : une seule ligne, qui est celle-ci.

---

## 2.5 ⚠️ $E(g(X))\ne g(E(X))$

L'erreur la plus coûteuse du cours, et elle a un nom.

> **Inégalité de Jensen.** Si $g$ est **convexe**, $E(g(X))\ge g(E(X))$ ; si $g$ est **concave**, $E(g(X))\le g(E(X))$. L'égalité n'a lieu que si $g$ est affine ou $X$ constante.

> 📐 **Démontrée ailleurs.** Une ligne suffit — l'inégalité de la tangente appliquée en $E(X)$ — mais elle suppose la convexité définie : voir le [module 5 du cours d'analyse](../../analyse/convexite/05-jensen-probabiliste.md), qui en tire aussi le **drag de volatilité** et la valeur exacte du biais de $S$.

Trois conséquences que vous rencontrerez dans ce cours :

| Fonction                | Sens                          | Conséquence                                                                  |
| ----------------------- | ----------------------------- | ---------------------------------------------------------------------------- |
| $g(x)=x^2$, convexe     | $E(X^2)\ge E(X)^2$            | La variance est $\ge 0$ — c'est le [§ 3.1](03-variance-et-moments.md)        |
| $g(x)=\sqrt x$, concave | $E(S)\le\sqrt{E(S^2)}=\sigma$ | **$S$ sous-estime $\sigma$ systématiquement** ([§ 15.4](15-loi-du-chi2.md))  |
| $g(x)=e^x$, convexe     | $E(e^X)\ge e^{E(X)}$          | Une moyenne de rendements logarithmiques n'est pas le log du rendement moyen |

> ⚠️ **$S^2$ est sans biais, $S$ ne l'est pas.** Ce n'est pas une bizarrerie du diviseur $n-1$ : c'est Jensen. Prendre la racine d'un estimateur sans biais ne donne pas un estimateur sans biais — et il n'existe pas de correction simple. C'est précisément le défaut que la [loi de Student](../loi-de-student/README.md) est construite pour absorber.

---

## 2.6 Simulations

### S2.1 — La linéarité tient sans indépendance ; le produit, non

```python
import numpy as np

rng = np.random.default_rng(2)
N = 1_000_000

X = rng.normal(3, 2, N)
Y_ind = rng.normal(-1, 5, N)                  # indépendante de X
Y_dep = 4 * X - 7 + rng.normal(0, 0.5, N)     # très dépendante de X

for nom, Y in [("independantes", Y_ind), ("dependantes", Y_dep)]:
    print(f"\n{nom} :")
    print(f"  E(2X - 3Y) = {np.mean(2*X - 3*Y):+8.4f}   "
          f"2E(X) - 3E(Y) = {2*X.mean() - 3*Y.mean():+8.4f}   <- toujours vrai")
    print(f"  E(XY)      = {np.mean(X*Y):+8.4f}   "
          f"E(X)E(Y)      = {X.mean()*Y.mean():+8.4f}   <- seulement si independantes")
```

**Les deux lignes du haut coïncident dans les deux cas ; les deux lignes du bas seulement dans
le premier.** C'est toute la différence entre le § 2.2 et le § 2.4, en un écran.

### S2.2 — $E(\bar X)=\mu$, même quand tout le reste est violé

```python
n = 30
def esperance_moyenne(nom, tirage):
    Xb = np.array([tirage().mean() for _ in range(50_000)])
    print(f"{nom:34s} E(Xbar) = {Xb.mean():+.4f}   std(Xbar) = {Xb.std():.4f}")

esperance_moyenne("i.i.d. normales, mu = 5",
                  lambda: rng.normal(5, 3, n))
esperance_moyenne("i.i.d. exponentielles, mu = 5",
                  lambda: rng.exponential(5, n))
esperance_moyenne("autocorrelees (AR1 phi=.9), mu = 5",
                  lambda: 5 + np.cumsum(rng.standard_normal(n) * 0.9**np.arange(n)))
esperance_moyenne("heterogenes en variance, mu = 5",
                  lambda: rng.normal(5, np.linspace(0.1, 10, n)))
```

Les quatre `E(Xbar)` valent 5. Les quatre `std(Xbar)` sont **complètement différents** — et c'est
exactement la frontière entre ce module et le suivant : **la linéarité protège l'espérance,
rien ne protège la variance.**

### S2.3 — Jensen, et le biais de $S$

```python
n, SIGMA = 5, 4.0
X = rng.normal(0, SIGMA, (500_000, n))
S2 = X.var(axis=1, ddof=1)
S = np.sqrt(S2)

print(f"E(S²) = {S2.mean():7.4f}   sigma²   = {SIGMA**2:7.4f}   -> sans biais")
print(f"E(S)  = {S.mean():7.4f}   sigma    = {SIGMA:7.4f}   -> BIAISE de "
      f"{100*(S.mean()/SIGMA - 1):+.1f} %")

for n2 in (2, 5, 30, 100):
    s = np.sqrt(rng.normal(0, SIGMA, (200_000, n2)).var(axis=1, ddof=1))
    print(f"  n={n2:>4} : E(S)/sigma = {s.mean()/SIGMA:.4f}")
```

À $n=5$, $S$ sous-estime $\sigma$ de 6 % **en moyenne, systématiquement**. Le biais décroît en
$1/n$ mais ne s'annule jamais. **Refaites-le avec `ddof=0`** : le biais passe de $-6{,}0\,\%$ à
$-15{,}9\,\%$, soit près du triple.

---

## 2.7 Exercices

**E2.1.** Calculer $E(X)$ pour une loi de Bernoulli $\mathcal B(p)$, une uniforme $\mathcal U(a,b)$ et une exponentielle $\mathcal E(\lambda)$. *Vérifier les trois lignes du tableau du [§ 1.6](01-variable-aleatoire-et-loi.md).*

**E2.2.** Démontrer $E(\bar X)=\mu$ en n'utilisant que la linéarité. *Quelles hypothèses du [§ 1.5](01-variable-aleatoire-et-loi.md) avez-vous utilisées ?* **(Réponse : « identiquement distribuées » seulement, et encore — il suffit que les $E(X_i)$ soient égales.)**

**E2.3.** Par le théorème de transfert, calculer$E(X^2)$ pour une$\mathcal U(0,1)$, puis en déduire
sa variance. *Vérifier avec la formule$\frac{(b-a)^2}{12}$.*

**E2.4.** Montrer que la loi de Cauchy n'a pas d'espérance. *(Piste : étudier la convergence
de$\int \frac{|x|}{\pi(1+x^2)}dx$.) Que vaut néanmoins sa médiane ?*

**E2.5.** Soit $X\sim\mathcal N(0,1)$ et $Y=X^2$. Calculer $E(XY)$ et $E(X)E(Y)$. *Sont-ils
égaux ? $X$ et $Y$ sont-elles indépendantes ? Que conclure sur la réciproque du § 2.4 ?*

**E2.6.** Un actif rapporte $+50\,\%$ une année sur deux et $-40\,\%$ l'autre. Calculer
l'espérance du rendement annuel, puis le rendement **effectivement obtenu** sur deux ans.
*(Réponses : $+5\,\%$ par an en espérance, mais $1{,}5\times0{,}6=0{,}9$, soit $-10\,\%$ sur deux
ans.) Quel théorème du § 2.5 explique l'écart ?*

**E2.7.** Démontrer $E(X^2)\ge E(X)^2$ **sans** invoquer Jensen. *(Piste : développer
$E\bigl((X-E(X))^2\bigr)\ge 0$.) C'est le [§ 3.1](03-variance-et-moments.md) en avance.*

---
### 2.7bis réponses

**E2.1**
* loi de Bernouilli $\mathcal B(p)$

Rappel : $P[X=1]=p ; P[X=0]=1-p$

Par le calcul direct, on obtient :
$$E(X)=1 . P[X=1] + 0 . P[X=0]=P[X=1]=q$$

* loi Binomiale $\mathcal U(a,b)$

Rappel :
* $P[X=x] = \dfrac{1}{b-a} ,\forall x \in [a,b]$; $P[X=y]=0$ sinon
* $\sum_{x=a}^b x=\dfrac{(b-a)^2}{2}$
Preuve :
$$E(X)=\sum_{x=a}^b xP[X=x]=\dfrac{1}{b-a}\sum_{x=a}^b x=\dfrac{b-a}{2}$$

---

## 2.8 À retenir

- **$E(X)$ est une moyenne pondérée par les probabilités** — et elle peut **ne pas exister**
  (Cauchy).
- ⚠️ **$E(X)$ n'est pas $\bar x$** : un paramètre inconnu contre un nombre calculé.
- ⭐ **La linéarité ne demande aucune hypothèse** : $E(aX+bY)=aE(X)+bE(Y)$, dépendance ou non.
  D'où $E(\bar X)=\mu$ **toujours**.
- **Théorème de transfert** : $E(g(X))=\int g\,f$ — c'est lui qui rend calculables la variance et
  toutes les transformées du cours.
- **$E(XY)=E(X)E(Y)$ exige l'indépendance** (en fait : la décorrélation). C'est le moteur du
  « somme → produit » du module 5.
- ⚠️ **$E(g(X))\ne g(E(X))$** — Jensen. D'où le biais de $S$, que $S^2$ n'a pas.

---

⬅️ [Module 1 — Variable aléatoire et loi](01-variable-aleatoire-et-loi.md) ·
➡️ [Module 3 — Variance et moments](03-variance-et-moments.md) ·
🏠 [Sommaire](README.md)
