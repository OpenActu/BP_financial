# Module 4 — Construction et propriétés de la loi de Student

**Durée : 3 h.** Les outils sont en place (modules 2 et 3). Ce module assemble et recense les
propriétés à connaître.

---

## 4.1 Définition

> **Définition.** Soient $Z\sim\mathcal N(0,1)$ et $K\sim\chi^2(\nu)$, **indépendantes**. La
> variable
> $$T=\frac{Z}{\sqrt{K/\nu}}$$
> suit la **loi de Student à $\nu$ degrés de liberté**, notée $T\sim\mathcal T(\nu)$.

⚠️ **L'hypothèse d'indépendance est constitutive.** Sans elle, le rapport suit une tout autre
loi. C'est précisément ce que le point (iii) de Fisher–Cochran est venu garantir : sans lui, la
définition serait inapplicable au cas qui nous intéresse.

**Lecture.** Le numérateur est un « signal » gaussien ; le dénominateur est un « bruit
d'estimation » qui vaut $1$ en moyenne ($E(K/\nu)=1$) mais fluctue. Student est la loi normale
**divisée par une estimation bruitée de son propre écart-type**.

---

## 4.2 Application immédiate : la statistique du module 1

Reprenons $T=\frac{\bar X-\mu}{S/\sqrt n}$ et écrivons-la sous la forme de la définition. Il
suffit de multiplier et diviser par $\sigma$ :

$$\frac{\bar X-\mu}{S/\sqrt n}
=\frac{\dfrac{\bar X-\mu}{\sigma/\sqrt n}}{\dfrac{S}{\sigma}}
=\frac{\overbrace{\dfrac{\bar X-\mu}{\sigma/\sqrt n}}^{\displaystyle Z\;\sim\;\mathcal N(0,1)\ \text{par (i)}}}
{\sqrt{\dfrac{\overbrace{(n-1)S^2/\sigma^2}^{\displaystyle K\;\sim\;\chi^2(n-1)\ \text{par (ii)}}}{n-1}}}$$

Les trois conditions de la définition sont réunies :
- le numérateur est $\mathcal N(0,1)$ — point **(i)** ;
- le radicande est un $\chi^2(n-1)$ divisé par ses degrés de liberté — point **(ii)** ;
- numérateur et dénominateur sont **indépendants** — point **(iii)**.

$$\boxed{\;\frac{\bar X-\mu}{S/\sqrt n}\;\sim\;\mathcal T(n-1)\;}$$

> 🔑 **Le $\sigma$ inconnu disparaît par simplification.** C'est tout le tour de force : la
> statistique est **calculable** (elle ne dépend que des données et de $\mu$), et sa loi est
> **connue et tabulée**, sans dépendre d'aucun paramètre inconnu. Une statistique ayant cette
> double propriété s'appelle une **quantité pivotale** — c'est ce qui permettra de construire
> intervalles de confiance et tests au module 5.

---

## 4.3 Densité

$$f_\nu(t)=\frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi}\;\Gamma\!\left(\frac{\nu}{2}\right)}
\left(1+\frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}}, \qquad t\in\mathbb R$$

> ⚠️ À reconnaître, pas à mémoriser. Deux éléments seulement importent :
> - la densité ne dépend de $t$ **que par $t^2$** → la loi est **symétrique** ;
> - la décroissance est en $\left(1+\frac{t^2}{\nu}\right)^{-(\nu+1)/2}\sim |t|^{-(\nu+1)}$,
>   c'est-à-dire **polynomiale**, alors que la gaussienne décroît en $e^{-t^2/2}$,
>   c'est-à-dire **exponentiellement**.

Cette dernière différence est **toute la loi de Student**. Une décroissance polynomiale est
incomparablement plus lente qu'une décroissance exponentielle : les valeurs extrêmes restent
possibles. C'est ce qu'on appelle des **queues épaisses** (*heavy tails*).

---

## 4.4 Propriétés

| Propriété | Contenu |
|---|---|
| Symétrie | Densité paire ; médiane et mode en 0 ; $t_{\nu;\,\alpha}=-t_{\nu;\,1-\alpha}$ |
| Queues | Polynomiales, en $\lvertt\rvert^{-(\nu+1)}$ |
| Moments d'ordre $k$ | Existent **si et seulement si** $k<\nu$ |
| Espérance | $E(T)=0$ — **existe seulement si $\nu>1$** |
| Variance | $\operatorname{Var}(T)=\dfrac{\nu}{\nu-2}$ — **existe seulement si $\nu>2$** |
| Kurtosis (excès) | $\dfrac{6}{\nu-4}$ pour $\nu>4$ ; **infini** pour $\nu\le 4$ |
| Cas $\nu=1$ | **Loi de Cauchy** : ni espérance ni variance |
| Cas $\nu=2$ | Espérance nulle, mais **variance infinie** |
| Limite | $\mathcal T(\nu)\xrightarrow[\nu\to\infty]{\mathcal L}\mathcal N(0,1)$ |

### Le point contre-intuitif : la variance vaut toujours plus que 1

$$\operatorname{Var}(T)=\frac{\nu}{\nu-2}>1 \quad\text{pour tout } \nu>2$$

| $\nu$ | 3 | 4 | 5 | 9 | 10 | 20 | 30 | 50 | 100 | $\infty$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $\operatorname{Var}(T)$ | 3,000 | 2,000 | 1,667 | 1,286 | 1,250 | 1,111 | 1,071 | 1,042 | 1,020 | 1 |
| $t_{\nu;\,0{,}975}$ | 3,182 | 2,776 | 2,571 | 2,262 | 2,228 | 2,086 | 2,042 | 2,009 | 1,984 | 1,960 |

Student est **toujours plus dispersée** que la normale, et d'autant plus que $\nu$ est petit.
C'est la traduction quantitative de l'intuition du module 1 : l'estimation du dénominateur
**ajoute** de la variabilité, elle n'en retire jamais.

### Le cas $\nu=1$ : la loi de Cauchy

Pour $\nu=1$, la densité se réduit à $f_1(t)=\frac{1}{\pi(1+t^2)}$ : c'est la **loi de Cauchy**.
Elle n'a **pas d'espérance** — l'intégrale $\int |t| f_1(t)\,dt$ diverge.

Conséquence spectaculaire : **la loi des grands nombres ne s'y applique pas**. La moyenne de $n$
Cauchy indépendantes suit… une loi de Cauchy, identique, quel que soit $n$. Moyenner n'apporte
strictement rien.

C'est aussi ce que révèle le quantile : $t_{1;\,0{,}975}=12{,}71$, contre $1{,}96$ pour la
normale. Avec deux observations ($n=2$, donc $\nu=1$), l'intervalle de confiance est six fois
plus large — et c'est justifié.

---

## 4.5 Convergence vers la normale

**Pourquoi elle a lieu.** Quand $\nu\to\infty$, la loi des grands nombres donne
$K/\nu\to 1$ en probabilité : le dénominateur cesse de fluctuer, et $T\to Z$.

**À quelle vitesse.** Lentement — c'est le point à retenir :

| $\nu$ | 10 | 20 | 30 | 50 | 100 | 200 | 1000 |
|---|---|---|---|---|---|---|---|
| $t_{\nu;\,0{,}975}$ | 2,228 | 2,086 | 2,042 | 2,009 | 1,984 | 1,972 | 1,962 |
| Écart relatif à 1,96 | +13,7 % | +6,4 % | +4,2 % | +2,5 % | +1,2 % | +0,6 % | +0,1 % |

La règle usuelle « au-delà de $\nu=30$, on peut prendre la normale » laisse subsister un écart de
**4 %** sur la valeur critique. C'est acceptable pour une estimation rapide, jamais pour un
résultat publié.

> ⚠️ **Il n'y a de toute façon aucune raison pratique de recourir à l'approximation.**
> `scipy.stats.t.ppf(0.975, nu)` coûte le même temps de calcul que `1.96`. L'approximation
> normale est un héritage de l'époque des tables imprimées.

---

## 4.6 Représentation en mélange (complément)

$T$ peut se lire comme une **gaussienne dont la variance est elle-même aléatoire** :

$$T \;\big|\; K \;\sim\; \mathcal N\!\left(0,\;\frac{\nu}{K}\right),
\qquad K\sim\chi^2(\nu)$$

Student est donc un **mélange d'échelle de gaussiennes**. Cette lecture explique intuitivement
les queues épaisses : la loi est une superposition de gaussiennes de variances diverses, et les
composantes de grande variance — bien que peu probables — alimentent les extrêmes.

Elle explique aussi pourquoi la loi de Student sert, **en dehors de tout contexte de test**, à
modéliser des données à valeurs extrêmes : rendements financiers, sinistres d'assurance, tailles
d'événements. Un $\mathcal T(\nu)$ ajusté sur des rendements quotidiens d'actions donne
typiquement $\nu$ entre 3 et 6 — c'est-à-dire des queues **beaucoup** plus épaisses que la
gaussienne, et parfois une variance théoriquement infinie.

> 🔑 **Attention au double usage.** Ici, $\nu$ n'est **pas** un nombre de degrés de liberté issu
> d'une estimation : c'est un **paramètre de forme** ajusté aux données. Ne pas confondre la loi
> de Student comme *loi d'une statistique de test* (tout le reste de ce cours) et comme
> *modèle de distribution* (usage en finance). Le même objet mathématique, deux emplois sans
> rapport.

---

## 4.7 Simulations

### S4.1 — Vérifier la définition

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(4)
nu = 7
Z = rng.standard_normal(500_000)
K = rng.chisquare(nu, 500_000)          # indépendant de Z
T = Z / np.sqrt(K / nu)

print("KS contre Student(nu) :", stats.kstest(T, "t", args=(nu,)))
print(f"Var simulée = {T.var():.4f}   théorie = {nu/(nu-2):.4f}")
```

**Contre-épreuve indispensable** : refaites-le en rendant $K$ **dépendant** de $Z$
(par exemple `K = nu * (1 + 0.5 * Z**2) / 1.5`). L'ajustement échoue — l'indépendance n'est pas
décorative.

### S4.2 — Reconstruire la table des quantiles

```python
print(f"{'nu':>5} {'t(0,975)':>10} {'Var':>10}")
for nu in list(range(1, 31)) + [40, 50, 100, 200, 1000]:
    var = nu / (nu - 2) if nu > 2 else float("inf")
    print(f"{nu:5d} {stats.t.ppf(0.975, nu):10.4f} {var:10.4f}")
print(f"{'inf':>5} {stats.norm.ppf(0.975):10.4f} {1.0:10.4f}")
```

### S4.3 — Voir une variance infinie (l'expérience la plus instructive)

```python
for nu in (2, 3, 10):
    print(f"\n--- nu = {nu} (variance théorique "
          f"{'infinie' if nu <= 2 else nu/(nu-2):.4} ) ---")
    T = stats.t.rvs(nu, size=2_000_000, random_state=42)
    for m in (10_000, 100_000, 1_000_000, 2_000_000):
        print(f"  sur {m:>9,} tirages : variance empirique = {T[:m].var():10.3f}")
```

**Ce que vous devez observer.** À $\nu=10$, la variance empirique se stabilise vers $1{,}25$.
À $\nu=3$, elle tend vers 3 mais **très** lentement. À $\nu=2$, elle **ne converge pas** : elle
augmente irrégulièrement avec le nombre de tirages, par bonds, chaque fois qu'un tirage extrême
survient. Relancez avec une autre graine : le résultat change du tout au tout.

> 🔑 Voir de ses propres yeux une variance qui ne converge pas vaut tous les discours sur les
> queues épaisses. C'est aussi une leçon transposable : sur des données financières réelles, une
> volatilité empirique qui « saute » à chaque nouvelle observation extrême est le symptôme d'une
> queue plus épaisse que le modèle supposé.

### S4.4 — Queues, en échelle logarithmique

```python
import matplotlib.pyplot as plt
x = np.linspace(0, 8, 500)
for nu in (1, 3, 10, 30):
    plt.plot(x, stats.t.pdf(x, nu), label=f"Student({nu})")
plt.plot(x, stats.norm.pdf(x), "k--", lw=2, label="N(0,1)")
plt.yscale("log"); plt.legend(); plt.xlabel("t"); plt.ylabel("densité (log)")
plt.show()
```

En échelle logarithmique, la normale est une **parabole** descendante et Student une **droite**
asymptotique : la différence de nature entre décroissance exponentielle et polynomiale devient
visible d'un coup d'œil.

---

## 4.8 Exercices

**E4.1.** Démontrer que $\mathcal T(1)$ est la loi de Cauchy en partant de la définition.
*Indication : $\chi^2(1)=Z_2^2$, donc $T=Z_1/|Z_2|$ ; utiliser le rapport de deux gaussiennes.*

**E4.2.** Vérifier sur la formule de la densité que $f_\nu(t)\to\frac{1}{\sqrt{2\pi}}e^{-t^2/2}$
quand $\nu\to\infty$. *Indication : $\left(1+\frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}}\to e^{-t^2/2}$,
et la constante converge par la formule de Stirling.*

**E4.3.** Pour quelles valeurs de $\nu$ la loi de Student admet-elle un moment d'ordre 4 ?
Que devient le kurtosis quand $\nu\downarrow 4$ ? Quelle conséquence pratique pour un test qui
reposerait sur une estimation de kurtosis ?

**E4.4.** Simuler 10 000 échantillons de taille $n=4$ issus d'une $\mathcal N(0,1)$ et vérifier
que $\frac{\bar X}{S/\sqrt 4}$ suit bien $\mathcal T(3)$ (test de Kolmogorov–Smirnov). Puis
comparer les quantiles empiriques à $1{,}96$ et à $t_{3;\,0{,}975}=3{,}182$.

**E4.5 — orientée finance.** Ajuster par maximum de vraisemblance une loi de Student sur les
rendements quotidiens d'un titre du SBF 250 (`stats.t.fit`). Quel $\nu$ obtenez-vous ? Comparer
la probabilité d'un mouvement à $-5\,\sigma$ sous la gaussienne ajustée et sous la Student
ajustée. *(L'écart se compte en ordres de grandeur : c'est l'argument décisif contre la
normalité en gestion des risques.)*

---

## 4.9 À retenir

- $T=\dfrac{Z}{\sqrt{K/\nu}}$ avec $Z\perp\!\!\!\perp K$ — l'indépendance est **constitutive**.
- $\dfrac{\bar X-\mu}{S/\sqrt n}\sim\mathcal T(n-1)$ : le $\sigma$ inconnu se simplifie, la
  statistique devient **pivotale**.
- Symétrique, à **queues polynomiales** ; $\operatorname{Var}=\frac{\nu}{\nu-2}>1$ ;
  moments d'ordre $k$ définis **ssi** $k<\nu$.
- Converge vers $\mathcal N(0,1)$, mais **lentement** : encore +4 % sur la valeur critique à
  $\nu=30$.
- Ne pas confondre les deux usages : **loi d'une statistique** (ce cours) et **modèle de queues
  épaisses** (finance).

---

⬅️ [Fisher–Cochran (cours de statistique)](../mathematique/16-theoreme-de-fisher-cochran.md) ·
➡️ [Module 5 — Inférence sur une moyenne](05-inference-sur-une-moyenne.md) ·
🏠 [Sommaire](README.md)
