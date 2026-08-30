# Module 3 — L'intégrale et le théorème fondamental ⭐

**Durée : 1 h 15.** Prérequis : [module 1](01-derivee-et-approximation-affine.md).

> **La question traitée.** Qu'est-ce qu'une intégrale — et par quel miracle se calcule-t-elle avec
> des primitives ?

**Ce qui est en jeu.** Une espérance est une intégrale, une fonction de répartition est une
intégrale, une CVaR est une intégrale. Le théorème fondamental est ce qui permet de les
**calculer** au lieu de les approcher ; le changement de variable est ce qui, au
[module 9](09-changement-de-variable-et-densites.md), donnera les densités.

---

## 3.1 L'intégrale de Riemann, en une page

**L'idée.** Découper $[a,b]$ en $n$ morceaux, approcher $f$ par une constante sur chacun,
sommer les aires des rectangles, faire tendre le pas vers 0 :

$$\int_a^bf(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n}f(x_i^*)\,\Delta x_i,
\qquad \Delta x_i=\frac{b-a}{n}$$

lorsque cette limite existe indépendamment des points $x_i^*$ choisis dans chaque morceau.

> **Théorème (admis).** Toute fonction **continue** sur un segment $[a,b]$ y est intégrable. Toute
> fonction **monotone bornée** aussi. Une fonction bornée ayant un nombre fini (ou dénombrable) de
> discontinuités l'est également.

**Les propriétés, toutes immédiates sur les sommes de rectangles :**

| Propriété | Énoncé |
|---|---|
| **Linéarité** | $\int(\alpha f+\beta g)=\alpha\int f+\beta\int g$ |
| **Croissance** | $f\le g\Rightarrow\int f\le\int g$ |
| **Relation de Chasles** | $\int_a^b=\int_a^c+\int_c^b$ |
| **Inégalité triangulaire** | $\left\lvert\int f\right\rvert\le\int\lvert f\rvert$ |
| **Moyenne** | $f$ continue $\Rightarrow\exists c,\ \int_a^bf=(b-a)f(c)$ |

> 🔑 **Linéarité et croissance** — ce sont exactement les deux propriétés de l'**espérance** qui
> ont servi à démontrer Jensen ([§ 5.2 d'analyse](../convexite/05-jensen-probabiliste.md)). Ce n'est
> pas une coïncidence : $E(g(X))=\int g(x)f_X(x)\,dx$ **est** une intégrale, et hérite de tout ce
> tableau.

---

## 3.2 Le théorème fondamental, et ses deux formes

Elles disent que dérivation et intégration sont **réciproques** — mais pas dans le même sens, et
la distinction compte.

> **① Forme « dérivée de l'intégrale ».** Si $f$ est continue sur $I$ et $a\in I$, la fonction
> $$F(x)=\int_a^xf(t)\,dt$$
> est de classe $C^1$ et $F'=f$. **Toute fonction continue admet donc une primitive.**

> **② Forme « intégrale de la dérivée » (Newton–Leibniz).** Si $F$ est une primitive de $f$
> continue :
> $$\int_a^bf(x)\,dx=F(b)-F(a).$$

**Démonstration de ①**, qui tient en trois lignes et mérite d'être lue :

$$\frac{F(x+h)-F(x)}{h}=\frac1h\int_x^{x+h}f(t)\,dt=f(c_h)
\quad\text{pour un }c_h\in[x,x+h]$$

par la propriété de la moyenne. Quand $h\to0$, $c_h\to x$ et la continuité de $f$ donne
$f(c_h)\to f(x)$. Donc $F'(x)=f(x)$. $\blacksquare$

> 🔑 **La continuité sert exactement là**, dans la dernière ligne. Sans elle, $F$ reste continue
> mais peut cesser d'être dérivable aux points de saut de $f$ — ce qui arrive précisément aux lois
> **discrètes**, dont la fonction de répartition est en escalier et n'a **pas** de densité
> ([§ 1.3 de statistique](../../../semestre2/statistique/mathematique/01-variable-aleatoire-et-loi.md)).

### La lecture probabiliste, à retenir telle quelle

| Objet | Écriture | Ce que le TFA dit |
|---|---|---|
| Répartition | $F(x)=\int_{-\infty}^{x}f(t)\,dt$ | $F'=f$ : **la densité est la dérivée de la répartition** |
| Probabilité d'un intervalle | $P(a<X\le b)=F(b)-F(a)$ | C'est Newton–Leibniz |
| Espérance | $E(X)=\int xf(x)\,dx$ | Une intégrale ordinaire |

---

## 3.3 Les deux techniques qui servent

### ① L'intégration par parties

$$\int_a^bu(x)v'(x)\,dx=\big[u(x)v(x)\big]_a^b-\int_a^bu'(x)v(x)\,dx$$

*Démonstration.* Intégrer $(uv)'=u'v+uv'$ et appliquer Newton–Leibniz. $\blacksquare$

**Son usage le plus utile ici** : la formule de survie. Pour $X\ge0$ intégrable,

$$\boxed{\;E(X)=\int_0^{+\infty}\big(1-F(x)\big)\,dx\;}$$

*Démonstration.* $E(X)=\int_0^\infty xf(x)dx$ ; poser $u=x$, $v'=f$ donc $v=-(1-F)$ :
$E(X)=\big[-x(1-F(x))\big]_0^{\infty}+\int_0^\infty(1-F(x))dx$, le crochet étant nul si
$E(X)<\infty$. $\blacksquare$

> 📐 **L'espérance est l'aire sous la courbe de survie.** C'est la formule qui rend l'**ES** du
> [§ 8.2 d'analyse](../convexite/08-convexite-et-mesures-de-risque.md) manipulable, et qui explique
> pourquoi une queue épaisse pèse directement sur la moyenne : l'aire de la queue **est** une part
> de $E(X)$.

### ② Le changement de variable

> **Théorème.** Si $\varphi$ est $C^1$ et $f$ continue :
> $$\int_{\varphi(a)}^{\varphi(b)}f(u)\,du=\int_a^bf\big(\varphi(t)\big)\,\varphi'(t)\,dt$$

*Démonstration.* Les deux membres, vus comme fonctions de $b$, ont la même dérivée
($f(\varphi(b))\varphi'(b)$, par la règle de la chaîne) et coïncident en $b=a$. $\blacksquare$

⚠️ **Le facteur $\varphi'(t)$ n'est pas un artifice de notation.** C'est le **taux de dilatation**
de $\varphi$ : changer de variable étire ou comprime les intervalles, et $dx$ doit être corrigé
d'autant.

> 🔑 **Ce $\varphi'$ est le jacobien du cours, en dimension 1.** Au
> [module 8](08-integrales-multiples-et-jacobien.md), il deviendra $\lvert\det J_\varphi\rvert$ ;
> et au [module 9](09-changement-de-variable-et-densites.md), c'est lui qui produira le
> $\frac1{\lvert g'\rvert}$ des formules de densité. **Toute la seconde moitié du cours est la
> généralisation de cette seule ligne.**

⚠️ **Pourquoi $\lvert\varphi'\rvert$ en dimension $\ge2$ et $\varphi'$ ici ?** Parce qu'en
dimension 1, l'orientation est portée par les bornes : si $\varphi$ décroît, $\varphi(a)>\varphi(b)$
et l'intégrale change de signe toute seule. En dimension supérieure, il n'y a plus de « bornes
orientées » : on intègre sur un **domaine**, et il faut prendre la valeur absolue.

---

## 3.4 Le catalogue des primitives utiles

| $f(x)$ | Primitive | Où elle sert |
|---|---|---|
| $x^n$, $n\ne-1$ | $\frac{x^{n+1}}{n+1}$ | Moments d'une loi uniforme |
| $\frac1x$ | $\log\lvert x\rvert$ | Loi de Pareto, log-rendements |
| $e^{ax}$ | $\frac{e^{ax}}a$ | Loi exponentielle, FGM |
| $xe^{-ax}$ | $-\frac{(ax+1)e^{-ax}}{a^2}$ | $E(X)$ d'une exponentielle (par IPP) |
| $\frac1{1+x^2}$ | $\arctan x$ | Loi de Cauchy — et sa répartition |
| $e^{-x^2/2}$ | **Aucune primitive élémentaire** | D'où la table de $\Phi$ ([module 4](04-integrales-generalisees-et-moments.md)) |

> ⚠️ **La dernière ligne est un fait, pas une lacune de technique.** $\Phi$ n'a pas d'expression en
> fonctions usuelles ; c'est pourquoi la loi normale se tabule, et pourquoi le
> [module 8](08-integrales-multiples-et-jacobien.md) devra passer par une **intégrale double** pour
> obtenir $\int e^{-x^2}dx=\sqrt\pi$ — un détour qui est l'un des plus beaux calculs du cours.

---

## 3.5 Vérification numérique

### S3.1 — Trois quadratures, et l'ordre de convergence

```python
import numpy as np
from math import erf, sqrt

f = lambda x: np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)     # densite normale
exact = 0.5 * (1 + erf(1 / sqrt(2))) - 0.5                 # P(0 < Z <= 1) = 0.341345

print(f"{'n':>7}{'rectangles':>14}{'trapezes':>14}{'Simpson':>14}")
for n in (10, 100, 1000, 10_000):
    x = np.linspace(0, 1, n + 1)
    y, h = f(x), 1 / n
    rect = h * y[:-1].sum()
    trap = h * (y[:-1] + y[1:]).sum() / 2
    simp = h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()) if n % 2 == 0 else np.nan
    print(f"{n:>7}{abs(rect - exact):>14.2e}{abs(trap - exact):>14.2e}{abs(simp - exact):>14.2e}")
```

Erreurs en $O(h)$, $O(h^2)$, $O(h^4)$ : multiplier $n$ par 10 divise l'erreur par 10, 100, puis
10 000. **La valeur exacte est $\Phi(1)-\Phi(0)=0{,}341345$**, qu'aucune primitive élémentaire ne
fournit — d'où la quadrature.

### S3.2 — L'espérance est l'aire sous la survie

```python
rng = np.random.default_rng(3)
X = rng.exponential(2.0, 2_000_000)                 # E(X) = 2

survie = np.array([(X > t).mean() for t in np.linspace(0, 40, 2001)])
aire = np.trapezoid(survie, np.linspace(0, 40, 2001))
print(f"moyenne empirique = {X.mean():.4f}   aire sous la survie = {aire:.4f}   theorie = 2")
```

Les deux nombres coïncident à la troisième décimale : $E(X)=\int_0^\infty(1-F)$ n'est pas une
astuce de calcul, c'est **une autre façon de voir la même aire**.

---

## 3.6 Exercices

**E3.1.** Démontrer la forme ① du TFA en détaillant l'usage de la propriété de la moyenne. *Où la
continuité de $f$ intervient-elle exactement ?*

**E3.2.** Calculer $\int_0^{+\infty}xe^{-\lambda x}\,dx$ par IPP et retrouver
$E(X)=\frac1\lambda$ pour une loi exponentielle
([§ 6e.2 de statistique](../../../semestre2/statistique/mathematique/06e-loi-exponentielle.md)).

**E3.3.** Démontrer $E(X)=\int_0^\infty(1-F(x))dx$ pour $X\ge0$, puis écrire l'analogue pour
$E(X^2)$. *(Piste : $E(X^2)=\int_0^\infty2x(1-F(x))dx$.)*

**E3.4.** Par changement de variable $u=\frac{x-\mu}{\sigma}$, montrer que
$\int_{-\infty}^{+\infty}\frac1{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}dx$ ne dépend ni de
$\mu$ ni de $\sigma$. *Quel facteur le $dx$ a-t-il fourni, et où le retrouve-t-on dans la densité
elle-même ?*

**E3.5.** Montrer que $\int_a^b f=0$ pour toute $f$ continue **positive** entraîne $f\equiv0$ sur
$[a,b]$. *Conséquence : deux densités qui donnent les mêmes probabilités à tous les intervalles
sont égales — c'est l'unicité de la densité.*

**E3.6.** Écrire une quadrature de Simpson et l'utiliser pour tabuler $\Phi(x)$ pour
$x\in\{1{,}28\,;1{,}645\,;1{,}96\,;2{,}576\}$. *Comparer aux quantiles usuels du
[cours de statistique](../../../semestre2/statistique/mathematique/18-intervalle-de-confiance.md).*

---

## 3.7 À retenir

- **L'intégrale est une limite de sommes de rectangles** ; ses cinq propriétés — dont
  **linéarité** et **croissance** — sont celles de l'espérance, qui en est un cas particulier.
- ⭐ **Théorème fondamental, deux formes** : $\left(\int_a^xf\right)'=f$ (toute continue a une
  primitive) et $\int_a^bf=F(b)-F(a)$. En probabilité : **la densité est la dérivée de la
  répartition**.
- **IPP** $\Rightarrow$ $E(X)=\int_0^\infty(1-F)$ : l'espérance est l'aire sous la courbe de
  survie.
- ⭐ **Changement de variable** : $\int f(u)du=\int f(\varphi(t))\varphi'(t)dt$. Le facteur
  $\varphi'$ est un **taux de dilatation** — c'est le jacobien en dimension 1, et toute la partie
  II du cours n'est que sa généralisation.
- $e^{-x^2/2}$ **n'a pas de primitive élémentaire** : d'où les tables, et d'où le détour par
  l'intégrale double du [module 8](08-integrales-multiples-et-jacobien.md).

---

⬅️ [Module 2 — Taylor et les approximations](02-taylor-et-approximations.md) ·
➡️ [Module 4 — Intégrales généralisées, $\Gamma$, et les moments](04-integrales-generalisees-et-moments.md) ·
🏠 [Sommaire](README.md)
