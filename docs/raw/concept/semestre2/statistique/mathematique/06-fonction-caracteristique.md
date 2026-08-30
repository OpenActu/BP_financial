# Module 6 — La fonction caractéristique

**Durée : 1 h.** Prérequis : [module 5](05-fonction-generatrice-des-moments.md).

> **La question traitée.** Comment garder le mécanisme « somme → produit » du module 5 tout en
> se débarrassant de son défaut — le fait que la FGM puisse ne pas exister ?

**Ce qui est en jeu.** La réponse tient en une modification d'apparence anodine : remplacer $t$
par $it$. Elle rend l'objet **toujours défini**, et c'est ce qui permettra au
[module 12](12-theoreme-central-limite.md) d'énoncer un théorème valable **pour toute loi de
variance finie**.

---

## 6.1 Définition

> **Définition.** La **fonction caractéristique** de $X$ est
> $$\varphi_X(t)=E\!\left(e^{itX}\right),\qquad t\in\mathbb R$$

> 🔑 **Elle existe toujours, sans aucune hypothèse.** Parce que $|e^{itX}|=1$ : on moyenne des
> quantités de module 1, l'espérance est donc automatiquement finie, et même bornée par 1.

C'est toute la différence avec la FGM, et elle est décisive. Comparons :

| | FGM $E(e^{tX})$ | Fonction caractéristique $E(e^{itX})$ |
|---|---|---|
| Existence | Conditionnelle | **Toujours** |
| Module | Peut exploser | $\lvert\varphi_X(t)\rvert\le 1$ |
| Calcul | Réel | Complexe |
| Sur une log-normale | Infinie pour $t>0$ | Parfaitement définie |
| Estimation par simulation | Instable | Stable |

---

## 6.2 Les quatre propriétés utiles

|          | Propriété                                                                             | Où elle sert          |
| -------- | ------------------------------------------------------------------------------------- | --------------------- |
| **(P1)** | $\varphi_X$ **caractérise** la loi de $X$                                             | Identifier une limite |
| **(P2)** | $X\perp\!\!\!\perp Y\;\Rightarrow\;\varphi_{X+Y}=\varphi_X\,\varphi_Y$                | Somme → produit       |
| **(P3)** | $\varphi_{aX}(t)=\varphi_X(at)$                                                       | Renormaliser          |
| **(P4)** | $E(X^2)<\infty\;\Rightarrow\;\varphi_X(t)=1+itE(X)-\frac{t^2}{2}E(X^2)+o(t^2)$ en $0$ | Développement limité  |

(P2) est la traduction de $E(UV)=E(U)E(V)$ pour des variables indépendantes — **exactement le
même mécanisme qu'au § 5.3**, démontré en détail au § 6.2 bis. (P4) vient de ce que deux moments
finis autorisent à dériver deux fois sous l'espérance, avec $\varphi'(0)=iE(X)$ et
$\varphi''(0)=-E(X^2)$.

> ⚠️ **(P4) demande seulement deux moments.** C'est précisément le niveau d'hypothèse du TCL :
> ni plus, ni moins. Un théorème ne peut pas exiger moins que ce que son outil exige.

---

## 6.2 bis Démonstration de (P2) : $\varphi_{X+Y}=\varphi_X\,\varphi_Y$

La démonstration du § 5.3 tenait en une ligne. Ici le mécanisme est **identique**, mais un point
mérite d'être établi et non supposé : $e^{itX}$ est une variable **complexe**, alors que
$E(UV)=E(U)E(V)$ a été démontré au [§ 2.4](02-esperance.md) pour des variables **réelles**. On
commence donc par étendre cette règle.

### Le lemme préalable : le produit d'espérances en complexe

Rappelons que l'espérance d'une variable complexe $U=A+iB$ ($A,B$ réelles intégrables) est
définie par $E(U)=E(A)+iE(B)$ ; elle est **linéaire sur $\mathbb C$**, exactement comme dans le
cas réel.

> **Lemme.** Si $U$ et $V$ sont des variables aléatoires **complexes, bornées et
> indépendantes**, alors
> $$E(UV)=E(U)\,E(V)$$

**Démonstration.** Écrivons $U=A+iB$ et $V=C+iD$ avec $A,B,C,D$ réelles.

1. **Intégrabilité.** $U$ et $V$ sont bornées, donc $A,B,C,D$ et leurs produits deux à deux le
   sont aussi : toutes les espérances écrites ci-dessous existent.
2. **Indépendance transportée.** $A$ et $B$ sont des fonctions (continues, donc mesurables) de
   $U$ ; $C$ et $D$ sont des fonctions de $V$. Or des fonctions mesurables de variables
   indépendantes sont indépendantes. Donc chacun des quatre couples $(A,C)$, $(A,D)$, $(B,C)$,
   $(B,D)$ est un couple de variables **réelles indépendantes**, et le [§ 2.4](02-esperance.md)
   s'applique à chacun.
3. **Développement.** En séparant partie réelle et partie imaginaire,
   $$UV=(AC-BD)+i\,(AD+BC)$$
   puis, par linéarité de l'espérance et par le point 2,
   $$E(UV)=\underbrace{E(A)E(C)-E(B)E(D)}_{\text{partie réelle}}
   +i\underbrace{\left(E(A)E(D)+E(B)E(C)\right)}_{\text{partie imaginaire}}$$
4. **Recomposition.** Ce membre de droite est exactement le développement du produit de deux
   nombres complexes :
   $$\bigl(E(A)+iE(B)\bigr)\bigl(E(C)+iE(D)\bigr)=E(U)\,E(V)\qquad\blacksquare$$

⬅️ **Rien de neuf n'a été utilisé** : seulement $E(XY)=E(X)E(Y)$ en réel, appliqué quatre fois,
et la linéarité. C'est en ce sens que la démonstration est « la même » qu'au § 5.3.

### La démonstration de (P2)

> **Propriété (P2).** Si $X\perp\!\!\!\perp Y$, alors pour **tout** $t\in\mathbb R$
> $$\varphi_{X+Y}(t)=\varphi_X(t)\,\varphi_Y(t)$$

**Démonstration.** Fixons $t\in\mathbb R$ et posons $U=e^{itX}$, $V=e^{itY}$.

$$\varphi_{X+Y}(t)
\overset{(a)}{=}E\!\left(e^{it(X+Y)}\right)
\overset{(b)}{=}E\!\left(e^{itX}e^{itY}\right)
\overset{(c)}{=}E\!\left(e^{itX}\right)E\!\left(e^{itY}\right)
=\varphi_X(t)\,\varphi_Y(t)$$

| Étape | Ce qui la justifie |
|---|---|
| $(a)$ | Définition de $\varphi$, appliquée à la variable $X+Y$ |
| $(b)$ | $e^{u+v}=e^{u}e^{v}$ dans $\mathbb C$ — pure algèbre, aucune probabilité |
| $(c)$ | Le lemme ci-dessus : $U=f(X)$ et $V=g(Y)$ avec $f(x)=g(x)=e^{itx}$ mesurables, donc $U\perp\!\!\!\perp V$ ; et $\lvertU\rvert=\lvertV\rvert=1$, donc bornées |

⬅️ **L'indépendance ne sert qu'en $(c)$**, exactement comme au § 5.3. Partout ailleurs, on ne
fait que de l'algèbre.

> 🔑 **Ce qui a changé par rapport au § 5.3 : rien dans le raisonnement, tout dans le domaine de
> validité.** Pour la FGM, l'égalité $M_{X+Y}=M_X M_Y$ n'a de sens que sur l'ensemble des $t$ où
> les deux FGM sont finies — ensemble qui peut se réduire à $\{0\}$. Ici les trois quantités sont
> définies et de module $\le 1$ pour **tout** $t\in\mathbb R$ : l'identité est valable partout,
> sans aucune hypothèse sur les lois de $X$ et $Y$.

### Le corollaire dont vit le module 12

Par récurrence immédiate sur le nombre de termes : si $X_1,\dots,X_n$ sont **indépendantes**,

$$\varphi_{X_1+\dots+X_n}(t)=\prod_{j=1}^{n}\varphi_{X_j}(t)$$

*Hérédité :* $X_1+\dots+X_n$ est une fonction mesurable de $(X_1,\dots,X_n)$, donc indépendante
de $X_{n+1}$ ; (P2) s'applique au couple ainsi formé.

Si de plus les $X_j$ sont **i.i.d.** de fonction caractéristique commune $\varphi$, en notant
$S_n=X_1+\dots+X_n$ :

$$\varphi_{S_n}(t)=\varphi(t)^n
\qquad\text{puis, avec (P3),}\qquad
\boxed{\;\varphi_{S_n/\sqrt n}(t)=\varphi\!\left(\frac{t}{\sqrt n}\right)^{\!n}\;}$$

C'est **l'expression exacte** dont part la démonstration du
[module 12](12-theoreme-central-limite.md) : (P4) donne le développement de
$\varphi(t/\sqrt n)$ en $0$, la puissance $n$-ième produit $e^{-t^2/2}$ à la limite, et Lévy
conclut.

### ⚠️ La réciproque est fausse

$\varphi_{X+Y}=\varphi_X\varphi_Y$ **n'entraîne pas** l'indépendance. Contre-exemple : prenons
$X$ de loi de Cauchy standard, dont $\varphi_X(t)=e^{-|t|}$ (exercice E6.3), et posons $Y=X$ —
soit la dépendance la plus totale possible. Alors, par (P3),

$$\varphi_{X+Y}(t)=\varphi_{2X}(t)=\varphi_X(2t)=e^{-2|t|}=\left(e^{-|t|}\right)^2
=\varphi_X(t)\,\varphi_Y(t)$$

C'est le même piège qu'au [§ 2.4](02-esperance.md) et au
[module 4](04-covariance-et-correlation.md) : l'égalité « produit » est une **conséquence** de
l'indépendance, jamais un test de celle-ci.

---

## 6.3 Le théorème de continuité de Lévy

Les quatre propriétés permettent de calculer une limite de **fonctions**. Il manque le passage de
là aux **lois** — et c'est le seul ingrédient analytique non élémentaire du cours.

> **Théorème de continuité de Lévy (admis).** Si $\varphi_{X_n}(t)\to\psi(t)$ pour **tout**
> $t\in\mathbb R$ et si $\psi$ est **continue en 0**, alors $\psi$ est la fonction
> caractéristique d'une loi et $X_n\xrightarrow{\mathcal L}$ cette loi.

> 🔑 **Lévy est un dictionnaire.** Il échange une convergence en loi — objet probabiliste
> difficile à manipuler — contre une convergence **simple de fonctions**, c'est-à-dire un calcul
> de limite ordinaire. Toute la démonstration du module 12 se joue de ce côté-là du dictionnaire.

⚠️ **L'hypothèse « continue en 0 » n'est pas décorative** : elle écarte les cas où la masse
s'échappe à l'infini et où la limite n'est plus une loi de probabilité.

---

## 6.4 Les cumulants

Le logarithme de la fonction caractéristique, $K_X(t)=\log\varphi_X(t)$, a pour coefficients de
Taylor les **cumulants** $\kappa_j$ :

| $j$ | 1 | 2 | 3 |
|---|---|---|---|
| $\kappa_j$ | $E(X)$ | $\operatorname{Var}(X)$ | $\gamma_1\sigma^3$ (asymétrie non normalisée) |

Leur intérêt : (P2) devient **additive**. Pour $X\perp\!\!\!\perp Y$, $K_{X+Y}=K_X+K_Y$, donc
$\kappa_j(X+Y)=\kappa_j(X)+\kappa_j(Y)$. Les cumulants s'ajoutent là où les moments se mélangent.

> 🔑 **La gaussienne est l'unique loi dont tous les cumulants d'ordre $\ge 3$ sont nuls.** Cette
> caractérisation est ce qui donnera au module 12 sa lecture la plus courte : *le TCL est
> l'effacement des cumulants d'ordre $\ge 3$*.

---

## 6.5 Simulation

### S6.1 — Stabilité numérique, somme → produit, et le module borné

```python
import numpy as np

rng = np.random.default_rng(2)
N = 1_000_000
X = rng.lognormal(0, 1, N)           # variance finie, mais AUCUNE FGM

phi = lambda x, t: np.mean(np.exp(1j * t * x))

print("la FGM n'existe pas, la fonction caractéristique si :")
for t in (0.5, 2.0, 5.0):
    vals = [phi(rng.lognormal(0, 1, 500_000), t) for _ in range(3)]
    print(f"  t={t}: |phi| = {[round(abs(v), 4) for v in vals]}   (toujours <= 1)")

Y = rng.lognormal(0, 1, N)
for t in (0.5, 1.0, 2.0):
    g, d = phi(X + Y, t), phi(X, t) * phi(Y, t)
    print(f"t={t}: phi_(X+Y)={g:+.4f}   phi_X*phi_Y={d:+.4f}")
```

Les trois estimations de $|\varphi|$ coïncident à la quatrième décimale — comparez avec la
simulation S5.2, où la FGM de la même loi divergeait d'un facteur 10. **Même mécanisme, outil
qui existe.**

---

## 6.6 Exercices

**E6.1.** Montrer que $\varphi_X(0)=1$, $|\varphi_X(t)|\le 1$ et
$\varphi_X(-t)=\overline{\varphi_X(t)}$. *En déduire que $\varphi_X$ est réelle si et seulement
si la loi de $X$ est symétrique.*

**E6.2.** Démontrer (P3) à partir de la définition, puis refaire la démonstration de (P2) sans
regarder le § 6.2 bis. *Comparer mot à mot avec le § 5.3 : qu'est-ce qui change dans le
raisonnement ?* **(Réponse : rien — seul le passage au complexe demande le lemme préalable, et ce
lemme n'est lui-même que $E(XY)=E(X)E(Y)$ appliqué quatre fois.)** *Où, précisément, l'hypothèse
d'indépendance est-elle utilisée ?*

**E6.3.** La loi de Cauchy standard a pour fonction caractéristique $\varphi(t)=e^{-|t|}$.
Calculer $\varphi_{\bar X_n}$ pour $n$ variables i.i.d. de cette loi. *Que constatez-vous ?
(Ce résultat est repris au [§ 13.1](13-portee-et-limites-du-tcl.md).)*

**E6.4.** Pourquoi ne peut-on pas conclure « $\varphi_X = \varphi_Y$ sur $[-1,1]$ donc même
loi » ? *(Piste : (P1) porte sur $\mathbb R$ tout entier.)*

**E6.5.** Montrer que si $X\perp\!\!\!\perp Y$, alors $\kappa_3(X+Y)=\kappa_3(X)+\kappa_3(Y)$.
*En déduire, pour $n$ variables i.i.d., que l'asymétrie de la somme se comporte en
$1/\sqrt n$ une fois renormalisée — résultat central du
[module 13](13-portee-et-limites-du-tcl.md).*

---

## 6.7 À retenir

- **$\varphi_X(t)=E(e^{itX})$ existe toujours** et $|\varphi_X|\le 1$ : c'est la seule différence
  avec la FGM, et elle suffit à tout changer.
- **(P1) caractérise**, **(P2) transforme la somme en produit**, **(P3) renormalise**,
  **(P4) développe à l'ordre 2** — dès que deux moments existent.
- **(P2) est démontrée pour tout $t$ et sans aucune hypothèse sur les lois** (§ 6.2 bis) : même
  raisonnement qu'au § 5.3, l'indépendance servant uniquement à écrire
  $E(e^{itX}e^{itY})=E(e^{itX})E(e^{itY})$. Par récurrence, $n$ variables i.i.d. donnent
  $\varphi_{S_n/\sqrt n}(t)=\varphi(t/\sqrt n)^n$ — le point de départ du module 12.
  ⚠️ La réciproque est fausse (contre-exemple de Cauchy avec $Y=X$).
- **Lévy** échange convergence en loi contre convergence simple de fonctions.
- **Cumulants** : additifs sur les sommes d'indépendantes ; la gaussienne est l'unique loi dont
  tous ceux d'ordre $\ge 3$ sont nuls.

---

> 📚 **Les six modules qui suivent (6a à 6f) forment le catalogue des lois usuelles.** Chacun
> applique les outils des modules 1 à 6 à une loi précise — Bernoulli, binomiale, Poisson,
> uniforme, exponentielle, normale — avec, à chaque fois, l'espérance et la variance démontrées
> **deux fois** : directement, puis par la fonction caractéristique, plus un exemple complet
> d'utilisation. Le [module 7](07-loi-normale-et-ses-transformees.md) reprend ensuite le fil
> théorique là où celui-ci s'arrête.

⬅️ [Module 5 — La fonction génératrice des moments](05-fonction-generatrice-des-moments.md) ·
➡️ [Module 6a — La loi de Bernoulli](06a-loi-de-bernoulli.md) ·
🏠 [Sommaire](README.md)
