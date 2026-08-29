# Module 2 — Fonctions convexes : définition et stabilité

**Durée : 1 h.** Prérequis : [module 1](01-ensembles-convexes.md).

> **La question traitée.** Qu'est-ce qu'une fonction convexe — sans supposer qu'elle soit
> dérivable ? Et quelles constructions préservent la propriété ?

**Ce qui est en jeu.** Les critères différentiels du [module 3](03-criteres-differentiels.md)
sont commodes mais supposent $f$ deux fois dérivable. Or les fonctions qui comptent ici ne le
sont pas toujours : $|x|$, un maximum de fonctions, une perte $\max(0,-x)$. La définition par les
cordes couvre tout, et les règles de stabilité de ce module évitent 90 % des calculs de dérivée
seconde.

---

## 2.1 La définition

> **Définition.** $f:I\to\mathbb R$, définie sur un **intervalle** (ou plus généralement un
> convexe $C\subset\mathbb R^d$), est **convexe** si pour tous $x,y$ et tout $\lambda\in[0,1]$ :
> $$\boxed{\;f\big(\lambda x+(1-\lambda)y\big)\;\le\;\lambda f(x)+(1-\lambda)f(y)\;}$$
> Elle est **strictement convexe** si l'inégalité est stricte dès que $x\ne y$ et
> $\lambda\in\,]0,1[$. Elle est **concave** si $-f$ est convexe.

**La lecture géométrique est la définition elle-même.** À gauche : la valeur de $f$ au point
$\lambda x+(1-\lambda)y$, c'est-à-dire **le graphe**. À droite : la valeur au même endroit du
segment joignant $(x,f(x))$ à $(y,f(y))$, c'est-à-dire **la corde**.

> 🔑 **La corde est au-dessus du graphe.** Toute la suite du cours est cette phrase, appliquée à
> des objets de plus en plus concrets — des moyennes (module 4), des espérances (module 5), des
> portefeuilles (module 7), des mesures de risque (module 8).

⚠️ **Le domaine doit être convexe**, sinon $\lambda x+(1-\lambda)y$ pourrait sortir de l'ensemble
de définition et l'inégalité n'aurait pas de sens. C'est la raison d'être du
[module 1](01-ensembles-convexes.md).

⚠️ **Convexe $\ne$ croissante, et convexe $\ne$ positive.** $f(x)=-x$ est convexe (et concave) ;
$f(x)=x^2-4$ est convexe et prend des valeurs négatives. La convexité ne dit rien du **niveau**
ni du **sens de variation** : elle ne parle que de la **courbure**.

---

## 2.2 Trois formulations équivalentes

### ① L'épigraphe

> **Définition.** $\operatorname{epi}f=\{(x,t)\in C\times\mathbb R\ :\ t\ge f(x)\}$ — la région
> **au-dessus** du graphe.

> **Proposition.** $f$ est convexe $\iff$ $\operatorname{epi}f$ est un **ensemble convexe**.

*Démonstration.* ($\Rightarrow$) Soient $(x,s)$ et $(y,t)$ dans l'épigraphe, donc $s\ge f(x)$ et
$t\ge f(y)$. Alors
$\lambda s+(1-\lambda)t\ge\lambda f(x)+(1-\lambda)f(y)\ge f(\lambda x+(1-\lambda)y)$,
donc le barycentre est dans l'épigraphe. ($\Leftarrow$) Appliquer l'inclusion aux points
$(x,f(x))$ et $(y,f(y))$. $\blacksquare$

> 🔑 **L'intérêt de l'épigraphe est de tout ramener au module 1.** Une propriété des fonctions
> convexes devient une propriété des ensembles convexes, où l'on dispose déjà de la stabilité par
> intersection. Le § 2.3 en tire immédiatement la règle la plus utile du cours.

### ② Les pentes croissantes (lemme des trois cordes)

> **Lemme.** $f$ est convexe sur $I$ $\iff$ pour tous $x<y<z$ dans $I$ :
> $$\frac{f(y)-f(x)}{y-x}\;\le\;\frac{f(z)-f(x)}{z-x}\;\le\;\frac{f(z)-f(y)}{z-y}$$

Autrement dit : **la pente d'une corde croît avec ses extrémités**. C'est la formulation la plus
maniable sans dérivée, et c'est elle qui donnera au [§ 3.1](03-criteres-differentiels.md)
l'équivalence « $f$ convexe $\iff$ $f'$ croissante » par simple passage à la limite.

*Esquisse.* Poser $y=\lambda x+(1-\lambda)z$ avec $\lambda=\frac{z-y}{z-x}\in\,]0,1[$, injecter
dans la définition, et réarranger. Les trois inégalités sont algébriquement équivalentes à
l'inégalité de convexité.

### ③ Les sous-niveaux (implication seulement)

Si $f$ est convexe, $S_c=\{x:f(x)\le c\}$ est convexe pour tout $c$ : si $f(x)\le c$ et
$f(y)\le c$, alors $f(\lambda x+(1-\lambda)y)\le\lambda c+(1-\lambda)c=c$. $\blacksquare$

⚠️ **La réciproque est fausse** — c'est la quasi-convexité du [§ 1.2](01-ensembles-convexes.md).
Retenir le sens de l'implication : *convexe $\Rightarrow$ sous-niveaux convexes*, jamais
l'inverse.

---

## 2.3 Les opérations qui préservent la convexité

C'est la table à connaître par cœur : elle remplace la quasi-totalité des vérifications directes.

| Opération | Convexe ? | Justification en une ligne |
|---|---|---|
| $f+g$ | Oui | Additionner deux inégalités de même sens |
| $\alpha f$, $\alpha\ge0$ | Oui | Multiplier par un positif |
| $\alpha f$, $\alpha<0$ | **Non** — devient concave | Le sens s'inverse |
| $\max(f,g)$ | ⭐ Oui | $\operatorname{epi}\max=\operatorname{epi}f\cap\operatorname{epi}g$ |
| $\sup_{i\in I}f_i$, famille **quelconque** | ⭐ Oui | Intersection quelconque d'épigraphes |
| $\min(f,g)$ | **Non** | $\min(x,-x)=-\lvert x\rvert$, concave |
| $x\mapsto f(Ax+b)$ (précomposition **affine**) | Oui | Le segment est envoyé sur un segment |
| $g\circ f$ avec $g$ convexe **croissante**, $f$ convexe | Oui | Appliquer $g$ à l'inégalité, puis sa convexité |
| $g\circ f$ avec $g$ convexe **décroissante** | **Non** en général | $e^{-x^2}$ n'est pas convexe |
| $f\cdot g$ (produit) | **Non** en général | $x\cdot x^{-1}=1$ sur $\mathbb R_+^*$ : deux convexes, produit affine |
| $f$ convexe $\Rightarrow$ $\lvert f\rvert$ | **Non** | $f(x)=x^2-1$ convexe, mais $\lvert x^2-1\rvert$ n'est pas convexe |

**Deux remarques sur les lignes marquées ⭐.**

- La stabilité par **maximum** est ce qui rend convexes les fonctions de perte usuelles :
  $\max(0,-x)$ (perte sur une position), $\max(0,K-S)$ (paiement d'une option de vente),
  $\max_i(a_i^{\top}x+b_i)$ (pire cas sur un scénario).
- La stabilité par **sup d'une famille quelconque** est le mécanisme le plus puissant du module 8 :
  une mesure de risque définie comme *le pire cas sur une famille de scénarios* est convexe
  **automatiquement**, sans le moindre calcul.

> 🔑 **Le contraste minimum / maximum est fondamental.** Un maximum de fonctions convexes est
> convexe ; un minimum ne l'est pas. C'est pourquoi *minimiser un pire cas* est un problème
> convexe, alors que *minimiser un meilleur cas* ne l'est pas — et pourquoi le risque, en
> finance, se modélise toujours par le haut.

### Composition : le tableau complet à une variable intérieure

Pour $h=g\circ f$ avec $f:\mathbb R\to\mathbb R$ et $g:\mathbb R\to\mathbb R$ :

| $g$ | $f$ | $h=g\circ f$ |
|---|---|---|
| convexe croissante | convexe | **convexe** |
| convexe décroissante | concave | **convexe** |
| concave croissante | concave | **concave** |
| concave décroissante | convexe | **concave** |

*Exemple d'usage.* $x\mapsto e^{x^2}$ : $g=\exp$ convexe croissante, $f=x^2$ convexe $\Rightarrow$
convexe, sans calculer aucune dérivée seconde. Et $x\mapsto-\log(1-x)$ sur $]-\infty,1[$ :
$g=-\log$ convexe décroissante, $f=1-x$ concave (affine) $\Rightarrow$ convexe.

---

## 2.4 Continuité, et ce que la convexité ne donne pas

> **Théorème (admis).** Une fonction convexe sur un intervalle **ouvert** y est continue, et même
> localement lipschitzienne. Elle admet en tout point une dérivée à gauche et une dérivée à
> droite, avec $f'_g(x)\le f'_d(x)$.

C'est beaucoup, gratuitement : la convexité **implique** une régularité qu'on ne lui a pas
demandée.

⚠️ **Trois réserves à connaître.**

1. **Aux bornes, la continuité tombe.** Sur $[0,1]$, $f(0)=1$ et $f(x)=0$ pour $x\in\,]0,1]$ est
   convexe et discontinue en 0.
2. **La dérivabilité n'est pas garantie** : $|x|$ est convexe et non dérivable en 0. Les points
   anguleux sont autorisés, en nombre au plus dénombrable.
3. **Rien n'est dit du comportement à l'infini** : une convexe peut décroître indéfiniment
   ($f(x)=-x$), ce qui interdira toute conclusion d'existence de minimum sans hypothèse
   supplémentaire ([§ 6.5](06-minimisation-convexe.md)).

---

## 2.5 Simulation

### S2.1 — Tester la convexité sans dériver

```python
import numpy as np

rng = np.random.default_rng(2)

def ecart_corde(f, a, b, n=200_000):
    """max sur des couples aléatoires de  f(lam x+(1-lam)y) - [lam f(x)+(1-lam)f(y)].
    <= 0 partout <=> convexe (sur l'échantillonnage testé)."""
    x, y = rng.uniform(a, b, n), rng.uniform(a, b, n)
    lam = rng.uniform(0, 1, n)
    return (f(lam * x + (1 - lam) * y) - (lam * f(x) + (1 - lam) * f(y))).max()

for nom, f, a, b in [
    ("exp",            np.exp,                        -3, 3),
    ("x^2",            lambda t: t ** 2,              -3, 3),
    ("|x|",            np.abs,                        -3, 3),
    ("-log",           lambda t: -np.log(t),          .05, 5),
    ("sqrt (concave)", np.sqrt,                        0, 5),
    ("x^3 (ni l'un…)", lambda t: t ** 3,              -3, 3),
    ("exp(x^2)",       lambda t: np.exp(t ** 2),      -2, 2),
    ("max(0, 1-x)",    lambda t: np.maximum(0, 1 - t), -3, 3),
]:
    e = ecart_corde(f, a, b)
    verdict = "convexe" if e <= 1e-12 else "PAS convexe"
    print(f"{nom:>16} : ecart max corde-graphe = {e:+.4f}   -> {verdict}")
```

Le test est une **traduction littérale de la définition** : aucune dérivée n'y intervient, ce qui
lui permet de traiter $|x|$ et $\max(0,1-x)$ comme les autres. Il ne **prouve** rien — un
échantillonnage ne couvre pas $I\times I$ — mais il **réfute** de façon fiable : un seul couple
avec écart positif suffit à conclure que la fonction n'est pas convexe.

### S2.2 — Le sup d'une famille est convexe, le min ne l'est pas

```python
t = np.linspace(-3, 3, 2001)
droites = [(a, b) for a, b in zip(rng.normal(size=12), rng.normal(size=12))]
sup_droites = np.max([a * t + b for a, b in droites], axis=0)
min_deux = np.minimum(t ** 2, (t - 2) ** 2)

def convexe_sur_grille(y, x=t):
    d2 = y[2:] - 2 * y[1:-1] + y[:-2]        # dérivée seconde discrète
    return (d2 >= -1e-9).all()

print("sup de 12 droites convexe :", convexe_sur_grille(sup_droites))
print("min de deux paraboles convexe :", convexe_sur_grille(min_deux))
```

Le premier est convexe **quelle que soit** la famille de droites — c'est le mécanisme du module 8.
Le second ne l'est pas, alors que chacune des deux paraboles l'est.

---

## 2.6 Exercices

**E2.1.** Démontrer le lemme des trois cordes (§ 2.2 ②) à partir de la définition, dans les deux
sens.

**E2.2.** Montrer que $f$ convexe et $g$ convexe $\Rightarrow$ $\max(f,g)$ convexe, de **deux
façons** : par les épigraphes, puis directement par l'inégalité.

**E2.3.** Donner deux fonctions convexes **positives** dont le produit n'est pas convexe.
*(Piste : chercher du côté de $x$ et $1/x$ sur $\mathbb R_+^*$, ou de $x^2$ et $e^{-x}$.)*

**E2.4.** Soit $f$ convexe et $g$ affine. Montrer que $f\circ g$ est convexe. *Pourquoi
l'hypothèse « affine » ne peut-elle pas être remplacée par « convexe » ?*

**E2.5.** La fonction $x\mapsto\max(0,K-x)$ (paiement d'une option de vente de prix d'exercice
$K$) est convexe. En déduire, **sans probabilité**, que le paiement d'un portefeuille de deux
options de prix d'exercice $K_1$ et $K_2$ détenues à parts égales est supérieur ou égal au
paiement d'une option de prix d'exercice $\frac{K_1+K_2}2$. *(Ce résultat porte un nom : la
convexité du prix par rapport au prix d'exercice.)*

**E2.6.** Montrer que la quasi-convexité (tous les sous-niveaux convexes) est strictement plus
faible que la convexité, avec $f(x)=\sqrt{|x|}$. *Vérifier ensuite que la somme de deux fonctions
quasi-convexes n'est pas toujours quasi-convexe — propriété que la convexité, elle, possède.*

---

## 2.7 À retenir

- **Définition** : $f(\lambda x+(1-\lambda)y)\le\lambda f(x)+(1-\lambda)f(y)$ — la **corde est
  au-dessus du graphe**. Aucune dérivabilité n'est requise.
- **$f$ convexe $\iff$ $\operatorname{epi}f$ convexe** : toute question sur les fonctions se
  ramène au module 1.
- **Pentes croissantes** : $\frac{f(y)-f(x)}{y-x}$ croît avec $x$ et avec $y$. C'est la version
  sans dérivée du critère $f''\ge0$.
- ⭐ **Stabilité** : somme, multiple positif, **max**, **sup quelconque**, précomposition affine,
  composition par une convexe **croissante**. Pas de min, pas de produit, pas de multiple négatif.
- **$f$ convexe $\Rightarrow$ sous-niveaux convexes**, jamais la réciproque (quasi-convexité) —
  et c'est exactement le piège de la VaR ([module 8](08-convexite-et-mesures-de-risque.md)).
- La convexité **offre** la continuité sur l'ouvert, mais **ne donne ni** la dérivabilité **ni**
  l'existence d'un minimum.

---

⬅️ [Module 1 — Ensembles convexes](01-ensembles-convexes.md) ·
➡️ [Module 3 — Les critères différentiels](03-criteres-differentiels.md) ·
🏠 [Sommaire](README.md)
