# Module 17 — Estimation et quantité pivotale

**Durée : 1 h.** Prérequis : module [8](08-addition-de-lois-et-stabilite-gaussienne.md).

> **La question traitée.** On observe $X_1,\dots,X_n$ i.i.d. $\mathcal N(\mu,\sigma^2)$ et l'on
> veut connaître $\mu$. Pourquoi le nombre $\bar x$ ne suffit-il pas — et quel objet permet d'aller
> plus loin ?

**Ce qui est en jeu.** La réponse — la **quantité pivotale** — est le mécanisme central de toute
la statistique classique. Sans pivot, aucun intervalle de confiance n'est constructible, et aucun
test non plus.

---

## 17.1 Pourquoi une estimation ponctuelle ne suffit pas

L'**estimation ponctuelle** est immédiate : $\bar x = 103{,}2$. Mais ce nombre, seul, est
**inexploitable pour décider**. Il ne dit pas s'il faut le lire comme « $\mu$ vaut à peu près
103 » ou « $\mu$ est quelque part entre 80 et 130 ». Or ce sont deux situations radicalement
différentes, et rien dans « 103,2 » ne permet de les distinguer.

Deux propriétés rassurent sur $\bar X$ :

$$E(\bar X)=\mu \qquad\text{(sans biais : pas d'erreur systématique)}$$
$$\operatorname{Var}(\bar X)=\frac{\sigma^2}{n} \qquad\text{(convergent : l'erreur décroît)}$$

Mais elles portent sur le **comportement moyen** de la procédure, pas sur la valeur obtenue ce
jour-là. La probabilité que $\bar X$ tombe **exactement** sur $\mu$ est nulle : une estimation
ponctuelle est **certainement fausse**, la seule question est de savoir de combien.

> 🔑 **L'intervalle de confiance répond à « de combien ? ».** Il transforme un nombre en une
> **plage assortie d'une garantie**. C'est ce qui en fait un objet de décision, là où
> l'estimation ponctuelle n'est qu'un résumé.

---

## 17.2 La loi d'échantillonnage de $\bar X$

Tout repose sur un résultat qu'il faut savoir énoncer sans hésiter :

> Si $X_1,\dots,X_n$ sont i.i.d. $\mathcal N(\mu,\sigma^2)$, alors
> $$\bar X \;\sim\; \mathcal N\!\left(\mu,\;\frac{\sigma^2}{n}\right).$$

Trois précisions qui font la différence entre réciter et comprendre :

1. **C'est une loi *exacte*, pas une approximation.** Une combinaison linéaire de gaussiennes
   indépendantes est gaussienne ([§ 8.3](08-addition-de-lois-et-stabilite-gaussienne.md)) —
   aucun TCL n'est invoqué ici. Le [TCL](12-theoreme-central-limite.md) ne servirait que si les
   $X_i$ n'étaient **pas** gaussiens.
2. **La variance est divisée par $n$, donc l'écart-type par $\sqrt n$.** C'est la
   dissymétrie fondamentale : $\sigma_{\bar X}=\sigma/\sqrt n$, appelée **erreur type**
   (*standard error*). Ne jamais confondre $\sigma$ (dispersion des **observations**) et
   $\sigma/\sqrt n$ (dispersion de la **moyenne**).
3. **C'est une loi théorique, non observable.** On ne dispose que d'**un seul** $\bar x$. La loi
   décrit ce qui se passerait si l'on répétait l'échantillonnage — c'est déjà, en germe, toute la
   difficulté d'interprétation du [module 19](19-interpretation-de-la-confiance.md).

**Sur l'exemple de référence** ($n=25$, $\sigma=8$) : $\sigma_{\bar X}=\dfrac{8}{\sqrt{25}}=\mathbf{1{,}6}$.

La moyenne de 25 observations est **cinq fois plus précise** qu'une observation isolée.

---

## 17.3 La quantité pivotale ⭐

Standardisons :

$$Z=\frac{\bar X-\mu}{\sigma/\sqrt n}\;\sim\;\mathcal N(0,1)$$

Cette variable a une propriété remarquable, qui porte un nom : c'est une **quantité pivotale**.

> **Définition.** Une quantité pivotale est une fonction des **données** et du **paramètre**
> dont la **loi ne dépend d'aucun paramètre inconnu**.

Vérifions les deux moitiés :
- elle dépend de $\mu$ (le paramètre cherché) et de $\bar X$ (les données) — donc elle relie bien
  ce qu'on veut à ce qu'on a ;
- sa loi est $\mathcal N(0,1)$, **la même quels que soient $\mu$ et $\sigma$** — on peut donc
  tabuler ses quantiles une fois pour toutes.

> 🔑 **C'est le mécanisme central de toute la statistique classique.** Sans pivot, aucun
> intervalle de confiance n'est constructible. Le [module 18](18-intervalle-de-confiance.md) ne
> fait qu'exploiter celui-ci.

⚠️ Attention à ce qui rend le pivot possible **ici** : $\sigma$ est **connu**, donc $\sigma/\sqrt n$
est un **nombre**, pas une variable aléatoire.

---

## 17.4 Ce qui se passe si $\sigma$ est inconnu

C'est le cas réel, et il n'a rien d'anodin : remplacer la constante $\sigma$ par la variable
aléatoire $S$ change la loi du rapport.

$$\frac{\bar X-\mu}{S/\sqrt n}\ \not\sim\ \mathcal N(0,1)$$

Le numérateur et le dénominateur sont tous deux aléatoires — et le
[théorème de Fisher–Cochran](16-theoreme-de-fisher-cochran.md) dit exactement ce qu'il faut pour
traiter le cas : le premier est gaussien, le carré du second est un $\chi^2(n-1)$, et **les deux
sont indépendants**. Le quotient d'une $\mathcal N(0,1)$ par la racine d'un $\chi^2(\nu)/\nu$
indépendant porte un nom : c'est la **loi de Student**, objet du
[cours dédié](../loi-de-student/README.md).

> 📐 **Il existe une seconde route, asymptotique.** Fisher–Cochran donne la loi **exacte** du
> pivot à $S$, au prix de l'hypothèse gaussienne. Sans elle, le
> [théorème de Slutsky](11bis-convergence-en-loi.md) donne directement
> $\frac{\bar X-\mu}{S/\sqrt n}\xrightarrow{\mathcal L}\mathcal N(0,1)$, puisque
> $\sigma/S\xrightarrow{P}1$ : remplacer $\sigma$ par $S$ ne change pas la loi **limite**. Les
> deux routes ne s'opposent pas — l'une est exacte à $n$ fini sous normalité, l'autre est
> approchée mais sans hypothèse de forme.

> ⚠️ **Ce module et le suivant supposent donc une hypothèse qui ne tient jamais en pratique.**
> Ils n'en sont pas moins la **maquette** de tout ce qui suit : pivot → retournement → intervalle.
> Seule la loi tabulée changera.

| | $\sigma$ connu (ici) | $\sigma$ estimé |
|---|---|---|
| Pivot | $\dfrac{\bar X-\mu}{\sigma/\sqrt n}$ | $\dfrac{\bar X-\mu}{S/\sqrt n}$ |
| Loi | $\mathcal N(0,1)$ | $\mathcal T(n-1)$ |
| Quantile à 95 % | $1{,}96$, **fixe** | $t_{n-1;\,0{,}975}$, **dépend de $n$** |
| Largeur de l'IC | **Constante** d'un échantillon à l'autre | **Aléatoire** (elle dépend de $S$) |
| Cadre de validité | Exact si les $X_i$ sont gaussiens | Idem, via Fisher–Cochran |

---

## 17.5 Simulation

### S17.1 — Le pivot ne dépend d'aucun paramètre

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
N, n = 200_000, 25

for MU, SIGMA in [(0.0, 1.0), (100.0, 8.0), (-3.5, 0.2)]:
    X = rng.normal(MU, SIGMA, (N, n))
    Z = (X.mean(axis=1) - MU) / (SIGMA / np.sqrt(n))
    print(f"mu={MU:>7}, sigma={SIGMA:>5} : "
          f"E(Z)={Z.mean():+.4f}  std(Z)={Z.std():.4f}  KS p={stats.kstest(Z, 'norm').pvalue:.3f}")
```

**Les trois lignes sont identiques.** C'est exactement ce que « pivotale » signifie : la loi ne
bouge pas quand les paramètres bougent. C'est ce qui autorise une table unique.

### S17.2 — Ce que devient le pivot quand $\sigma$ est estimé

```python
X = rng.normal(100.0, 8.0, (N, n))
Z = (X.mean(axis=1) - 100.0) / (8.0 / np.sqrt(n))          # sigma connu
T = (X.mean(axis=1) - 100.0) / (X.std(axis=1, ddof=1) / np.sqrt(n))   # sigma estimé

for nom, V in [("Z (sigma connu)", Z), ("T (sigma estime)", T)]:
    print(f"{nom:18s} std={V.std():.4f}  kurtosis={stats.kurtosis(V):+.4f}  "
          f"P(|V|>1.96)={np.mean(np.abs(V) > 1.96):.4f}")
```

$T$ est **plus dispersée** et à **queues plus épaisses** que $Z$ : $P(|T|>1{,}96)$ dépasse
nettement les 5 % attendus. Utiliser 1,96 quand $\sigma$ est estimé produit donc un test **trop
permissif** — et c'est toute la raison d'être de la loi de Student.

---

## 17.6 Exercices

**E17.1.** Démontrer $E(\bar X)=\mu$ et $\operatorname{Var}(\bar X)=\sigma^2/n$ pour des $X_i$
i.i.d. *Quelle hypothèse sert à chacune des deux ?* **(Réponse : la linéarité de l'espérance ne
demande rien ; la variance demande l'indépendance — ou au moins la décorrélation.)**

**E17.2.** Pourquoi $\frac{\bar X-\mu}{\sigma}$ n'est-elle **pas** une bonne quantité pivotale
pour construire un intervalle sur $\mu$ ? *(Piste : sa loi dépend-elle de $n$ ?)*

**E17.3.** $\frac{(n-1)S^2}{\sigma^2}$ est-elle une quantité pivotale ? Pour quel paramètre ?
*(Voir [§ 15.4](15-loi-du-chi2.md) — c'est le pivot d'un intervalle sur $\sigma^2$.)*

**E17.4.** Un procédé a $\sigma=2{,}5$ mm connu. Sur $n=16$ pièces, $\bar x=48{,}3$ mm. Calculer
l'erreur type. De combien faut-il multiplier $n$ pour la diviser par 2 ?

**E17.5.** Montrer que si $X_i$ ne sont **pas** gaussiens, $Z=\frac{\bar X-\mu}{\sigma/\sqrt n}$
reste centrée réduite mais n'est plus gaussienne. *Que dit alors le
[module 12](12-theoreme-central-limite.md) ?*

---

## 17.7 À retenir

- **Une estimation ponctuelle est certainement fausse** : la seule question utile est « de
  combien ».
- $\bar X\sim\mathcal N(\mu,\sigma^2/n)$ — loi **exacte** sous normalité, pas une approximation.
- **Erreur type** $=\sigma/\sqrt n$, à ne **jamais** confondre avec $\sigma$.
- ⭐ **Le pivot** $\frac{\bar X-\mu}{\sigma/\sqrt n}$ a une loi qui ne dépend d'aucun paramètre
  inconnu : c'est ce qui rend l'intervalle constructible et la table universelle.
- **$\sigma$ connu est une fiction commode.** Le cas réel remplace $\sigma$ par $S$, et change la
  loi du pivot — c'est l'objet du [cours sur Student](../loi-de-student/README.md).

---

⬅️ [Module 16 — Théorème de Fisher–Cochran](16-theoreme-de-fisher-cochran.md) ·
➡️ [Module 18 — L'intervalle de confiance](18-intervalle-de-confiance.md) ·
🏠 [Sommaire](README.md)
