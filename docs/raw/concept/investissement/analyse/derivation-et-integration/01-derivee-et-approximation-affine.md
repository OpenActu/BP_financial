# Module 1 — La dérivée comme approximation affine

**Durée : 1 h.** Prérequis : aucun.

> **La question traitée.** Qu'est-ce qu'une dérivée — non pas comme limite de taux
> d'accroissement, mais comme **objet** qui se généralisera à $\mathbb R^n$ ?

**Ce qui est en jeu.** La définition « limite du taux d'accroissement » ne survit pas au passage à
plusieurs variables : on ne divise pas par un vecteur. La définition par **approximation affine**,
elle, se transporte telle quelle — et devient la matrice jacobienne du
[module 6](06-la-matrice-jacobienne.md). Tout ce module consiste à adopter la bonne définition dès
la dimension 1.

---

## 1.1 Les deux définitions, et pourquoi la seconde gagne

> **Définition A (usuelle).** $f$ est dérivable en $a$ si
> $\displaystyle f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}$ existe.

> **Définition B (approximation affine).** $f$ est dérivable en $a$ s'il existe un nombre $\ell$
> tel que
> $$\boxed{\;f(a+h)=f(a)+\ell\,h+o(h)\;}$$
> c'est-à-dire $\frac{f(a+h)-f(a)-\ell h}{h}\to0$. Ce $\ell$ est alors unique et vaut $f'(a)$.

Les deux sont **équivalentes** en dimension 1 — il suffit de réarranger. Mais elles ne disent pas
la même chose :

| | Définition A | Définition B |
|---|---|---|
| Objet produit | Un **nombre** | Une **application linéaire** $h\mapsto\ell h$ |
| Se généralise à $\mathbb R^n\to\mathbb R^m$ | ❌ (on ne divise pas par un vecteur) | ✅ telle quelle |
| Lecture | Une pente | La **meilleure approximation affine** |

> 🔑 **Dériver, c'est linéariser.** $f$ est dérivable en $a$ si elle est, au voisinage de $a$,
> égale à une fonction **affine** à une erreur négligeable devant $h$. La dérivée est le
> coefficient de cette fonction affine — et rien d'autre. C'est cette phrase qui sera reprise mot
> pour mot au [§ 6.1](06-la-matrice-jacobienne.md), avec une **matrice** à la place du nombre.

⚠️ **« Négligeable » a un sens précis.** $o(h)$ signifie « divisé par $h$, tend vers 0 » — pas
« petit ». L'erreur $h^{3/2}$ est un $o(h)$ ; l'erreur $0{,}001\,h$ ne l'est pas, si petite
soit-elle.

---

## 1.2 Ce que la dérivabilité donne, et ce qu'elle ne donne pas

| Fait | Vrai ? | Contre-exemple ou raison |
|---|---|---|
| Dérivable $\Rightarrow$ continue | ✅ | $f(a+h)-f(a)=\ell h+o(h)\to0$ |
| Continue $\Rightarrow$ dérivable | ❌ | $\lvert x\rvert$ en 0 |
| Dérivable $\Rightarrow$ $f'$ continue | ❌ | $x^2\sin(1/x)$ prolongée par 0 |
| $f'(a)=0$ $\Rightarrow$ extremum | ❌ | $x^3$ en 0 — sauf si $f$ est **convexe** ([§ 6.4 analyse](../convexite/06-minimisation-convexe.md)) |
| $f$ croissante $\Rightarrow$ $f'\ge0$ | ✅ | Et réciproquement sur un intervalle |

> ⚠️ **La quatrième ligne est celle qui coûte le plus cher dans ce dépôt.** Annuler une dérivée ne
> démontre rien en général ; c'est la **convexité** qui transforme un point critique en minimum
> global, et c'est l'objet d'un cours à part.

---

## 1.3 Les quatre règles, et leur démonstration en une ligne chacune

| Règle | Énoncé | Démonstration par la définition B |
|---|---|---|
| **Linéarité** | $(\alpha f+\beta g)'=\alpha f'+\beta g'$ | Additionner les deux approximations affines |
| **Produit** | $(fg)'=f'g+fg'$ | $(f+f'h)(g+g'h)=fg+(f'g+fg')h+\underbrace{f'g'h^2}_{o(h)}$ |
| **Quotient** | $\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}$ | Produit $+$ dérivée de $1/u$ |
| ⭐ **Chaîne** | $(g\circ f)'(a)=g'\big(f(a)\big)\cdot f'(a)$ | **Composer** les deux approximations affines |

**La règle de la chaîne, écrite avec la définition B**, parce que c'est elle qui se généralise :

$$g\big(f(a+h)\big)=g\big(f(a)+f'(a)h+o(h)\big)
=g\big(f(a)\big)+g'\big(f(a)\big)\cdot\big[f'(a)h\big]+o(h).$$

> 🔑 **La composée de deux applications linéaires est une application linéaire, et le coefficient
> est le produit.** En dimension 1, ce produit est celui de deux nombres ; en dimension $n$, ce
> sera le **produit de deux matrices** ([§ 6.3](06-la-matrice-jacobienne.md)). L'énoncé ne change
> pas d'un mot, seul l'objet change de nature.

### La dérivée d'une réciproque

Si $f$ est bijective, dérivable en $a$ avec $f'(a)\ne0$, alors $f^{-1}$ est dérivable en
$b=f(a)$ et

$$\big(f^{-1}\big)'(b)=\frac1{f'(a)} .$$

*Pourquoi.* Dériver $f^{-1}\circ f=\text{id}$ par la règle de la chaîne : $(f^{-1})'(b)\,f'(a)=1$.
$\blacksquare$

> 📐 **C'est l'ancêtre de l'inversion locale du [§ 6.5](06-la-matrice-jacobienne.md)** :
> $J_{f^{-1}}=(J_f)^{-1}$. L'hypothèse $f'(a)\ne0$ deviendra $\det J_f(a)\ne0$, et la division
> deviendra une inversion de matrice.

---

## 1.4 Le catalogue à connaître

| $f(x)$ | $f'(x)$ | Remarque utile dans ce dépôt |
|---|---|---|
| $x^\alpha$ | $\alpha x^{\alpha-1}$ | $\alpha=-t$ : l'actualisation ([module 9 d'analyse](../convexite/09-la-convexite-obligataire.md)) |
| $e^{ax}$ | $a\,e^{ax}$ | La FGM et la fonction caractéristique |
| $\log x$ | $1/x$ | Les rendements logarithmiques |
| $\log(1+x)$ | $\frac1{1+x}$ | $\approx x$ pour $x$ petit : rendement log $\approx$ rendement simple |
| $\sqrt x$ | $\frac1{2\sqrt x}$ | La delta-méthode sur $S=\sqrt{S^2}$ |
| $\frac1x$ | $-\frac1{x^2}$ | $\left(\frac{\text{cours}}{\text{bénéfice}}\right)^{-1}$ |
| $\Phi(x)$ | $\phi(x)=\frac{e^{-x^2/2}}{\sqrt{2\pi}}$ | La densité **est** la dérivée de la répartition ([§ 3.4](03-integrale-et-theoreme-fondamental.md)) |

---

## 1.5 Deux applications immédiates au dépôt

### ① Rendement simple contre rendement logarithmique

$$\log(1+r)=r+o(r)\qquad\Longrightarrow\qquad \log(1+r)\approx r\ \text{ pour }r\text{ petit}.$$

À $r=1\,\%$, l'écart est de $0{,}005\,\%$ — invisible. À $r=30\,\%$, $\log(1{,}30)=26{,}2\,\%$ :
l'écart est de près de 4 points. **L'approximation est une approximation, et le
[module 2](02-taylor-et-approximations.md) en donne le terme suivant** — qui n'est autre que le
$\sigma^2/2$ du drag de volatilité.

### ② La dérivée d'une valeur actualisée

$P(y)=\sum_t c_t(1+y)^{-t}$ donne $P'(y)=-\sum_t t\,c_t(1+y)^{-t-1}$, d'où la **duration
modifiée** $-P'/P$ du [module 9 d'analyse](../convexite/09-la-convexite-obligataire.md). Une dérivée,
normalisée par le prix, porte un nom en finance ; c'est **le même objet**.

---

## 1.6 Vérification numérique

### S1.1 — La différence finie centrée, et le bon pas

```python
import numpy as np

f, df = np.exp, np.exp                      # fonction et derivee exacte
a = 0.7

print(f"{'h':>10}{'avant':>14}{'centree':>14}{'err avant':>12}{'err centree':>13}")
for h in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-11):
    avant = (f(a + h) - f(a)) / h
    centree = (f(a + h) - f(a - h)) / (2 * h)
    print(f"{h:>10.0e}{avant:>14.9f}{centree:>14.9f}"
          f"{abs(avant - df(a)):>12.2e}{abs(centree - df(a)):>13.2e}")
```

**Deux enseignements, et le second est le plus utile.**

- La différence **centrée** est d'erreur $O(h^2)$ contre $O(h)$ pour la différence avant : à
  $h=10^{-4}$, elle est déjà $10^4$ fois plus précise.
- ⚠️ **En dessous de $h\approx10^{-8}$, l'erreur remonte.** Ce n'est pas un défaut du calcul mais
  de l'arithmétique flottante : $f(a+h)-f(a-h)$ soustrait deux nombres presque égaux, et les
  chiffres significatifs disparaissent. **Le pas optimal est $h\approx10^{-5}$ à $10^{-6}$**, et
  c'est celui qu'on utilisera pour vérifier toutes les dérivées matricielles du
  [module 7](07-calcul-matriciel-des-derivees.md).

### S1.2 — L'approximation affine, vue de près

```python
a, h = 0.7, np.logspace(-1, -6, 6)
erreur = np.abs(np.exp(a + h) - (np.exp(a) + np.exp(a) * h))
for hi, e in zip(h, erreur):
    print(f"h={hi:.0e}  erreur={e:.3e}   erreur/h={e / hi:.3e}   erreur/h^2={e / hi ** 2:.4f}")
```

`erreur/h` tend vers 0 — c'est la définition B — tandis que `erreur/h²` tend vers une constante
($\frac12 e^{0{,}7}\approx1{,}007$) : le terme suivant est quadratique, ce que le
[module 2](02-taylor-et-approximations.md) va chiffrer.

---

## 1.7 Exercices

**E1.1.** Démontrer l'équivalence des définitions A et B, puis expliquer en une phrase pourquoi
seule B se transporte à $f:\mathbb R^n\to\mathbb R^m$.

**E1.2.** Démontrer la règle du produit **par la définition B** (et non par la limite du taux
d'accroissement). *Où le terme $f'g'h^2$ est-il absorbé, et pourquoi a-t-on le droit ?*

**E1.3.** Montrer que $x\mapsto x^2\sin(1/x)$ (prolongée par $0$) est dérivable en 0 mais que sa
dérivée n'est pas continue en 0. *Conséquence : « dérivable » et « de classe $C^1$ » ne sont pas
synonymes — distinction qui comptera au [§ 5.3](05-derivees-partielles-et-gradient.md).*

**E1.4.** Calculer $\frac{d}{dy}\big[(1+y)^{-t}\big]$ puis retrouver la duration modifiée d'une
obligation. *Vérifier sur l'obligation 10 ans / 3 % du
[§ 9.3 d'analyse](../convexite/09-la-convexite-obligataire.md) que $D_{\text{mod}}=8{,}530$.*

**E1.5.** Soit $g(x)=\log(1+x)$. Calculer $g'$, $g''$, et majorer $\lvert g(x)-x\rvert$ pour
$\lvert x\rvert\le0{,}3$. *Comparer à l'écart réel en $x=0{,}30$.*

**E1.6.** Écrire une fonction `derivee_num(f, a, h=1e-6)` en différence centrée, la tester sur
$\sqrt{\ }$, $\log$ et $x\mapsto1/x$, et repérer pour chacune le domaine où l'approximation se
dégrade.

---

## 1.8 À retenir

- ⭐ **Dériver, c'est linéariser** : $f(a+h)=f(a)+f'(a)h+o(h)$. C'est la définition qui se
  généralise ; la « limite du taux d'accroissement » ne se généralise pas.
- **La règle de la chaîne est une composition d'applications linéaires** — d'où un **produit** en
  dimension 1, un **produit de matrices** en dimension $n$.
- **$(f^{-1})'(b)=1/f'(a)$**, ancêtre de $J_{f^{-1}}=(J_f)^{-1}$.
- **Dérivable $\Rightarrow$ continue**, jamais l'inverse ; et **$f'(a)=0$ ne prouve rien** sans
  convexité.
- **Vérification numérique** : différence **centrée**, pas $h\approx10^{-6}$. Plus petit, l'erreur
  d'arrondi domine.

---

⬅️ [🏠 Sommaire](README.md) ·
➡️ [Module 2 — Taylor et les approximations qui servent](02-taylor-et-approximations.md)
