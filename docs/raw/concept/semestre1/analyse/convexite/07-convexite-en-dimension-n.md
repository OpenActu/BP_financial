# Module 7 — Convexité en dimension $n$

**Durée : 1 h 15.** Prérequis : [module 6](06-minimisation-convexe.md), et le
[module 11 d'algèbre](../../algebre/11-covariance-et-produit-scalaire.md) ($\Sigma$ est une matrice de
Gram).

> **La question traitée.** Comment reconnaître une fonction convexe de plusieurs variables — et
> pourquoi la variance d'un portefeuille en est **toujours** une ?

**Ce qui est en jeu.** La phrase « la diversification ne peut pas nuire » est vraie, mais pas pour
la raison qu'on croit. Elle ne tient ni à la corrélation, ni au nombre de lignes : elle tient au
fait que $\Sigma$ est une **matrice de Gram**, donc semi-définie positive, donc que
$w\mapsto w^{\top}\Sigma w$ est convexe. Ce module fait ce chemin.

---

## 7.1 La définition ne change pas — et c'est tout l'intérêt

$$f\big(\lambda x+(1-\lambda)y\big)\le\lambda f(x)+(1-\lambda)f(y),\qquad x,y\in C\subset\mathbb R^d$$

Rien de nouveau. Mieux : **tout se ramène à la dimension 1**.

> **Théorème (restriction aux segments).** $f:C\to\mathbb R$ est convexe **si et seulement si**,
> pour tous $x\in C$ et $v\in\mathbb R^d$, la fonction d'une variable
> $$\varphi_{x,v}(t)=f(x+tv)$$
> est convexe sur $\{t:\ x+tv\in C\}$.

*Démonstration.* Les segments de $C$ sont exactement les images des segments de $\mathbb R$ par
$t\mapsto x+tv$, et l'inégalité de convexité ne porte que sur des segments. $\blacksquare$

> 🔑 **C'est la technique de travail en dimension $n$.** Toute question de convexité se teste
> **le long d'une droite**, où l'on dispose des critères du [module 3](03-criteres-differentiels.md).
> Aucun calcul multidimensionnel n'est nécessaire pour établir une convexité — seulement pour la
> **caractériser** par la Hessienne, ce qui est le § 7.2.

---

## 7.2 Gradient, Hessienne, et le critère matriciel

### L'inégalité de la tangente devient un plan tangent

> Pour $f$ différentiable convexe : $$f(y)\;\ge\;f(x)+\big\langle\nabla f(x),\,y-x\big\rangle .$$

Le graphe est au-dessus de chacun de ses **hyperplans tangents**. C'est le
[§ 3.3](03-criteres-differentiels.md) avec un produit scalaire à la place d'un produit de réels —
et c'est ce qui a servi à démontrer Jensen, la condition d'optimalité, et ce qui servira encore au
[§ 8.4](08-convexite-et-mesures-de-risque.md).

### Le critère du second ordre

> **Théorème.** $f$ deux fois différentiable sur un ouvert convexe est convexe **si et seulement
> si** sa matrice hessienne est **semi-définie positive** en tout point :
> $$H_f(x)\succeq0,\qquad\text{c'est-à-dire}\qquad v^{\top}H_f(x)\,v\ge0\ \ \text{pour tout }v .$$
> Si $H_f(x)\succ0$ partout, $f$ est **strictement** convexe (réciproque fausse : $x^4$).

*Démonstration.* Par le § 7.1, $f$ est convexe ssi $\varphi_{x,v}$ l'est pour tous $x,v$. Or
$\varphi''_{x,v}(t)=v^{\top}H_f(x+tv)\,v$, et le [§ 3.2](03-criteres-differentiels.md) conclut.
$\blacksquare$

**Comment vérifier $A\succeq0$ en pratique**, pour $A$ symétrique :

| Test | Énoncé | Coût |
|---|---|---|
| Valeurs propres | Toutes $\ge0$ | Le plus sûr ; $O(d^3)$ |
| Cholesky | La factorisation $A=LL^{\top}$ existe | $A\succ0$ seulement ; rapide |
| Mineurs principaux | **Tous** les mineurs principaux $\ge0$ | ⚠️ pas seulement ceux du coin nord-ouest |

⚠️ **L'erreur classique** : tester les seuls mineurs principaux **dominants** (coin supérieur
gauche) caractérise $A\succ0$, jamais $A\succeq0$. Contre-exemple :
$A=\begin{pmatrix}0&0\\0&-1\end{pmatrix}$ a ses mineurs dominants nuls et n'est pas $\succeq0$.

---

## 7.3 La variance d'un portefeuille est convexe

**Le résultat, et sa raison.**

> **Proposition.** Pour toute matrice de covariance $\Sigma$, la fonction
> $$q(w)=w^{\top}\Sigma\,w$$
> est convexe sur $\mathbb R^d$. Elle est **strictement** convexe si et seulement si
> $\Sigma\succ0$.

*Démonstration.* $H_q=2\Sigma$, et $\Sigma\succeq0$ **toujours** — parce que $\Sigma$ est la
matrice de **Gram** des vecteurs centrés
([module 11 d'algèbre](../../algebre/11-covariance-et-produit-scalaire.md)) : pour tout $w$,
$w^{\top}\Sigma w=\operatorname{Var}\big(\sum_iw_iX_i\big)\ge0$, une variance ne pouvant pas être
négative. $\blacksquare$

> 🔑 **Deux lectures d'un même fait.** *Algébriquement*, $\Sigma\succeq0$ parce que c'est une
> matrice de Gram. *Statistiquement*, parce que $w^{\top}\Sigma w$ **est** la variance du
> portefeuille $\sum_iw_iX_i$. La convexité de la variance n'est donc pas une hypothèse de
> modélisation : elle est **impossible à violer**, et cela vaut pour n'importe quelle matrice de
> covariance, estimée sur n'importe quelles données.

### L'écart type aussi — mais pas pour la raison qu'on croit

$\sigma(w)=\sqrt{w^{\top}\Sigma w}$ est convexe. ⚠️ **Ce n'est pas une conséquence de la règle de
composition** du [§ 2.3](02-fonctions-convexes.md) : $\sqrt{\ }$ est concave, et la racine d'une
fonction convexe n'est en général pas convexe.

La bonne raison est que $\sigma$ est une **norme** (au sens large : une semi-norme si $\Sigma$ est
singulière) — celle associée au produit scalaire de Gram — et que **toute norme est convexe**
([§ 4.3](04-jensen-fini-et-moyennes.md)) :

$$\sigma\big(\lambda w+(1-\lambda)w'\big)\;\le\;\lambda\,\sigma(w)+(1-\lambda)\,\sigma(w') .$$

---

## 7.4 « La diversification ne peut pas nuire » — l'énoncé exact

L'inégalité ci-dessus **est** l'énoncé, et il vaut la peine de le lire lentement :

> Le risque d'un mélange de deux portefeuilles n'excède **jamais** la moyenne pondérée de leurs
> risques.

| Ce que l'énoncé dit | Ce qu'il ne dit **pas** |
|---|---|
| $\sigma(\text{mélange})\le$ moyenne des $\sigma$ | Que $\sigma$ diminue toujours |
| C'est vrai pour **toute** $\Sigma$ | Que la corrélation n'a pas d'importance |
| L'égalité est un cas limite | Que le mélange soit meilleur en espérance |

**Le cas d'égalité.** Il y a égalité si et seulement si les deux vecteurs de rendements sont
**colinéaires de même sens** — c'est-à-dire $\rho=1$. La diversification ne rapporte rien
exactement quand il n'y a rien à diversifier ; la géométrie et l'intuition coïncident, via le cas
d'égalité de Cauchy–Schwarz ([module 3 d'algèbre](../../algebre/03-cauchy-schwarz-et-angle.md)).

> ⚠️ **Ce théorème ne protège que contre un excès de risque, jamais contre la perte.** Il porte
> sur $\sigma$, pas sur le rendement ; et $\sigma$ n'est un bon résumé du risque que si les queues
> sont fines — ce que le [module 13 de statistique](../../../semestre2/statistique/mathematique/13-portee-et-limites-du-tcl.md)
> conteste sur données financières. Le [module 8](08-convexite-et-mesures-de-risque.md) reprend la
> question avec des mesures de risque qui regardent la queue.

---

## 7.5 Le portefeuille à variance minimale

$$\min_{w}\ w^{\top}\Sigma w\quad\text{sous}\quad \mathbf 1^{\top}w=1 .$$

Problème **convexe** (critère convexe, contrainte affine) : par le
[§ 6.4 ③](06-minimisation-convexe.md), les conditions de Lagrange sont **suffisantes**.
$\nabla q=2\Sigma w=\nu\mathbf 1$ donne, si $\Sigma\succ0$ :

$$\boxed{\;w^\star=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^{\top}\Sigma^{-1}\mathbf 1}\;}$$

unique par stricte convexité ([§ 6.3](06-minimisation-convexe.md)).

**L'exemple à deux actifs**, avec $\sigma_1=20\,\%$, $\sigma_2=30\,\%$, $\rho=0{,}3$ :

$$w^\star_1=\frac{\sigma_2^2-\rho\sigma_1\sigma_2}{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}
=\frac{0{,}090-0{,}018}{0{,}130-0{,}036}=0{,}766
\qquad\Longrightarrow\qquad \sigma_{\min}=18{,}67\,\%$$

| Quantité | Valeur |
|---|---|
| Moyenne pondérée des risques $w^\star\sigma_1+(1-w^\star)\sigma_2$ | $22{,}34\,\%$ |
| Risque du mélange $\sigma(w^\star)$ | $\mathbf{18{,}67\,\%}$ |
| Risque de l'actif le **moins** risqué | $20{,}00\,\%$ |

> 🔑 **Deux faits, de natures différentes.** Que $18{,}67<22{,}34$ est **garanti** par la convexité
> (§ 7.4). Que $18{,}67<20{,}00$ — le portefeuille est moins risqué que **chacun** de ses
> composants — n'est **pas** garanti : cela dépend de $\rho$, et cesse d'être vrai quand
> $\rho\ge\sigma_1/\sigma_2$. Ne pas attribuer à la convexité ce qui revient à la corrélation.

**L'effet de $\rho$**, à $\sigma_1,\sigma_2$ fixés :

| $\rho$ | $-1$ | $-0{,}5$ | $0$ | $0{,}3$ | $0{,}5$ | $1$ |
|---|---|---|---|---|---|---|
| $w^\star_1$ | 0,600 | 0,632 | 0,692 | 0,766 | 0,857 | 3,000 |
| $\sigma_{\min}$ | $0\,\%$ | $11{,}9\,\%$ | $16{,}6\,\%$ | $18{,}7\,\%$ | $19{,}6\,\%$ | $0\,\%$ |

⚠️ **Les deux colonnes extrêmes sont des artefacts, et il faut savoir les reconnaître.** À
$\lvert\rho\rvert=1$, $\Sigma$ est **singulière** (matrice de Gram de deux vecteurs colinéaires) :
la variance n'est plus strictement convexe, et l'optimum sans contrainte utilise un levier
($w^\star_1=3$, donc $-200\,\%$ sur le second actif) pour annuler le risque. Un modèle de
corrélation estimée à $1$ produit toujours ce type de solution — c'est un signal d'erreur
d'estimation, pas une opportunité.

**Avec interdiction de vente à découvert**, on ajoute $w\in\Delta_d$
([§ 1.2](01-ensembles-convexes.md)) : l'intersection de deux convexes reste convexe, le problème
reste convexe (c'est un **programme quadratique**), mais la solution n'a plus de forme fermée.

---

## 7.6 La frontière efficiente est convexe

Pour chaque rendement cible $m$, posons

$$\sigma_{\min}(m)=\min\big\{\sigma(w)\ :\ \mathbf 1^{\top}w=1,\ \mu^{\top}w=m\big\}.$$

> **Proposition.** $m\mapsto\sigma_{\min}(m)$ est **convexe**.

*Démonstration.* Soient $w_1,w_2$ optimaux pour $m_1,m_2$. Le mélange
$w=\lambda w_1+(1-\lambda)w_2$ vérifie les deux contraintes pour la cible
$\lambda m_1+(1-\lambda)m_2$ — les contraintes sont **affines** — donc

$$\sigma_{\min}\big(\lambda m_1+(1-\lambda)m_2\big)\le\sigma(w)
\le\lambda\sigma(w_1)+(1-\lambda)\sigma(w_2)
=\lambda\sigma_{\min}(m_1)+(1-\lambda)\sigma_{\min}(m_2).\ \blacksquare$$

> 🔑 **La courbe en « balle » du plan $(\sigma,\mu)$ n'est pas un dessin d'illustration : c'est un
> théorème.** Et la démonstration montre exactement d'où vient sa forme — de la convexité de
> $\sigma$ et de la **linéarité** des contraintes. Un critère de risque non convexe (la VaR,
> [module 8](08-convexite-et-mesures-de-risque.md)) produit une frontière qui peut être
> **rentrante**, et un problème d'optimisation à optima locaux multiples.

---

## 7.7 Simulations

### S7.1 — $\Sigma\succeq0$ toujours, et la convexité qui en découle

```python
import numpy as np

rng = np.random.default_rng(7)
d, n = 6, 250
X = rng.normal(size=(n, d)) @ rng.normal(size=(d, d))     # rendements corrélés
Sig = np.cov(X, rowvar=False)

vp = np.linalg.eigvalsh(Sig)
print(f"valeurs propres de Sigma : min={vp.min():.6f}  -> semi-definie positive : {vp.min() >= -1e-12}")

# convexite de w -> w' Sigma w le long de segments aleatoires
q = lambda w: w @ Sig @ w
w1, w2 = rng.dirichlet(np.ones(d)), rng.dirichlet(np.ones(d))
lam = rng.uniform(0, 1, 100_000)
melange = lam[:, None] * w1 + (1 - lam)[:, None] * w2
gauche = np.einsum("ij,jk,ik->i", melange, Sig, melange)
droite = lam * q(w1) + (1 - lam) * q(w2)
print("variance convexe   :", (gauche <= droite + 1e-12).all())
print("ecart type convexe :", (np.sqrt(gauche) <= lam * np.sqrt(q(w1))
                              + (1 - lam) * np.sqrt(q(w2)) + 1e-12).all())
```

⚠️ **Attention à un piège d'estimation** : si $n<d$, la matrice $\Sigma$ estimée est **singulière**
($\Sigma\succeq0$ mais pas $\succ0$). La convexité tient toujours, la **stricte** convexité non — et
le portefeuille à variance minimale cesse d'être unique. C'est le cas de tout portefeuille avec
plus de lignes que d'observations.

### S7.2 — Le portefeuille à variance minimale, et la borne de convexité

```python
un = np.ones(d)
w_star = np.linalg.solve(Sig, un)
w_star /= w_star.sum()
sig = lambda w: np.sqrt(w @ Sig @ w)

print(f"w* = {np.round(w_star, 3)}   (somme = {w_star.sum():.3f})")
print(f"sigma(w*) = {sig(w_star):.4f}")
print(f"min sur 20 000 portefeuilles tires au hasard : "
      f"{min(sig(w) for w in rng.dirichlet(np.ones(d), 20_000)):.4f}")

# la borne du 7.4, sur des couples aleatoires
w1, w2 = rng.dirichlet(np.ones(d)), rng.dirichlet(np.ones(d))
for l in (0.25, 0.5, 0.75):
    m = l * w1 + (1 - l) * w2
    print(f"lam={l}: sigma(melange)={sig(m):.4f}  <=  "
          f"moyenne des sigma={l * sig(w1) + (1 - l) * sig(w2):.4f}")
```

Le tirage aléatoire de portefeuilles ne retrouve **jamais** $w^\star$ : en dimension 6, le
simplexe est trop grand pour être exploré au hasard. C'est l'argument pratique en faveur d'une
formulation convexe — on **résout**, on n'échantillonne pas.

---

## 7.8 Exercices

**E7.1.** Démontrer le théorème de restriction aux segments (§ 7.1), puis l'utiliser pour montrer
que $f(x,y)=e^{x+2y}$ est convexe sans calculer de Hessienne.

**E7.2.** Calculer la Hessienne de $f(w)=w^{\top}\Sigma w$ et vérifier le § 7.3. *Que devient
l'énoncé si $\Sigma$ n'est pas symétrique — et pourquoi ce cas ne se présente-t-il jamais ici ?*

**E7.3.** Montrer que $\sqrt{f}$ n'est **pas** convexe en général pour $f$ convexe positive.
*(Piste : $f(x)=x^2$.)* Pourquoi l'argument échoue-t-il à disqualifier $\sigma(w)$ ?

**E7.4.** Établir la formule $w^\star=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^{\top}\Sigma^{-1}\mathbf 1}$
par les conditions de Lagrange, puis vérifier qu'elle donne bien $0{,}766$ dans l'exemple à deux
actifs du § 7.5.

**E7.5.** À quelle condition sur $\rho$ le portefeuille à variance minimale est-il moins risqué
que **chacun** des deux actifs ? *(Réponse attendue : $\rho<\sigma_1/\sigma_2$ en supposant
$\sigma_1<\sigma_2$.)* Interpréter le cas $\rho=\sigma_1/\sigma_2$.

**E7.6.** Montrer que l'ensemble $\{w\in\Delta_d:\ w^{\top}\Sigma w\le c,\ \mu^{\top}w\ge m\}$ est
convexe. *Combien de contraintes convexes y a-t-il empilées, et quelle propriété du
[§ 1.3](01-ensembles-convexes.md) autorise l'empilement ?*

**E7.7 — orientée finance.** Construire $\Sigma$ sur 5 titres du SBF 250 avec
`import_societe.py`, calculer $w^\star$, et vérifier : (a) que $\Sigma\succeq0$ ; (b) que
$\sigma(w^\star)$ est inférieur à la moyenne pondérée des $\sigma_i$ ; (c) si $w^\star$ contient
des poids négatifs — et ce que cela signifie.

---

## 7.9 À retenir

- **La définition ne change pas** ; tout se teste **le long d'un segment** (§ 7.1), où les critères
  du module 3 s'appliquent.
- **$f$ convexe $\iff$ $H_f\succeq0$ partout.** $H_f\succ0$ suffit à la stricte convexité, sans
  être nécessaire.
- ⭐ **$w\mapsto w^{\top}\Sigma w$ est convexe pour toute matrice de covariance**, parce que
  $\Sigma$ est une matrice de Gram : c'est une variance, donc $\ge0$. **Impossible à violer.**
- **$\sigma(w)$ est convexe parce que c'est une norme**, jamais par composition — la racine d'une
  convexe n'est pas convexe en général.
- **« La diversification ne peut pas nuire »** = $\sigma$ convexe. Elle ne dit **pas** que le
  risque baisse ; qu'il baisse sous $\min(\sigma_1,\sigma_2)$ dépend de $\rho$, pas de la
  convexité.
- **Le portefeuille à variance minimale** $w^\star=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^{\top}\Sigma^{-1}\mathbf 1}$
  est unique tant que $\Sigma\succ0$ ; il cesse de l'être dès que $n<d$ ou $\lvert\rho\rvert=1$.
- **La frontière efficiente est une courbe convexe** — c'est un théorème, dont la démonstration
  tient en trois lignes et n'utilise que la linéarité des contraintes.

---

⬅️ [Module 6 — Minimisation convexe](06-minimisation-convexe.md) ·
➡️ [Module 8 — Convexité et mesures de risque](08-convexite-et-mesures-de-risque.md) ·
🏠 [Sommaire](README.md)
