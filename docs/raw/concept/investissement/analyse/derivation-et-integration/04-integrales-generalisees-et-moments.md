# Module 4 — Intégrales généralisées, $\Gamma$, et les moments

**Durée : 1 h.** Prérequis : [module 3](03-integrale-et-theoreme-fondamental.md).

> **La question traitée.** Que veut dire $\int_0^{+\infty}$ ou $\int_0^1\frac{dx}{\sqrt x}$ — et
> quand cela existe-t-il ?

**Ce qui est en jeu.** « $X$ admet une variance finie » est l'hypothèse centrale du
[théorème central limite](../../statistique/mathematique/12-theoreme-central-limite.md). Ce n'est pas une
formalité : c'est une **condition de convergence d'intégrale**, et ce module dit exactement
laquelle. Il installe aussi la fonction $\Gamma$, sans laquelle ni la densité du $\chi^2$ ni le
biais de $S$ ne s'écrivent.

---

## 4.1 Définition

Deux situations, une seule définition — passer à la limite sur une borne.

| Situation | Définition |
|---|---|
| Borne infinie | $\displaystyle\int_a^{+\infty}f=\lim_{b\to+\infty}\int_a^bf$ |
| Fonction non bornée en $a$ | $\displaystyle\int_a^{b}f=\lim_{\varepsilon\to0^+}\int_{a+\varepsilon}^{b}f$ |

L'intégrale **converge** si la limite existe et est finie ; elle **diverge** sinon. Si les deux
bornes posent problème, on **découpe** en un point intérieur et on exige la convergence des deux
morceaux séparément.

⚠️ **Découper est obligatoire, et ce n'est pas une précaution d'école.** $\int_{-\infty}^{+\infty}x\,dx$
**diverge**, bien que $\int_{-A}^{A}x\,dx=0$ pour tout $A$. La symétrie ne sauve rien : c'est
exactement pourquoi une loi de **Cauchy**, pourtant parfaitement symétrique, n'a pas d'espérance
([§ 13.4 de statistique](../../statistique/mathematique/13-portee-et-limites-du-tcl.md)).

> **Convergence absolue.** Si $\int\lvert f\rvert$ converge, $\int f$ converge. En probabilité,
> c'est la **seule** notion utilisée : « $X$ est intégrable » signifie $E(\lvert X\rvert)<\infty$,
> jamais une convergence conditionnelle.

---

## 4.2 Les critères, et les deux à retenir

| Critère | Énoncé |
|---|---|
| **Comparaison** | $0\le f\le g$ et $\int g$ converge $\Rightarrow$ $\int f$ converge |
| **Équivalents** | $f\sim g>0$ au voisinage du problème $\Rightarrow$ même nature |
| ⭐ **Riemann à l'infini** | $\displaystyle\int_1^{+\infty}\frac{dx}{x^a}$ converge $\iff a>1$ |
| ⭐ **Riemann en 0** | $\displaystyle\int_0^{1}\frac{dx}{x^a}$ converge $\iff a<1$ |

**Les deux critères de Riemann sont l'essentiel du module**, et ils s'opposent : à l'infini il
faut décroître **vite** ($a>1$) ; en 0 il faut exploser **lentement** ($a<1$). Le cas $a=1$
diverge des deux côtés — $\log$ est la frontière.

**Trois exemples qu'on rencontre :**

| Intégrale | Nature | Pourquoi |
|---|---|---|
| $\int_1^{\infty}e^{-x^2/2}dx$ | Converge | $e^{-x^2/2}\le e^{-x/2}$ pour $x\ge1$ |
| $\int_0^{1}\frac{dx}{\sqrt x}$ | Converge | $a=\frac12<1$ ; vaut 2 |
| $\int_1^{\infty}\frac{dx}{x}$ | **Diverge** | $a=1$ : $\log b\to\infty$ |

---

## 4.3 L'intégrale de Gauss

$$\boxed{\;\int_{-\infty}^{+\infty}e^{-x^2}\,dx=\sqrt\pi
\qquad\text{d'où}\qquad\int_{-\infty}^{+\infty}\frac{e^{-x^2/2}}{\sqrt{2\pi}}\,dx=1\;}$$

La convergence est acquise par le § 4.2 ; la **valeur**, elle, ne s'obtient par aucune primitive
([§ 3.4](03-integrale-et-theoreme-fondamental.md)). Elle se calcule en passant par une intégrale
**double** et un changement de variables polaire — c'est le
[§ 8.4](08-integrales-multiples-et-jacobien.md), l'un des deux calculs qui justifient à eux seuls
la partie II de ce cours.

Le facteur $\frac1{\sqrt{2\pi}}$ de la densité normale n'est donc **pas une convention** : c'est
la constante qui rend l'intégrale égale à 1, et elle vaut ce que vaut cette intégrale double.

---

## 4.4 La fonction $\Gamma$

> **Définition.** Pour $s>0$ : $\displaystyle\Gamma(s)=\int_0^{+\infty}t^{s-1}e^{-t}\,dt$.

**Elle converge pour tout $s>0$** : en 0, $t^{s-1}$ est intégrable car $1-s<1$ ; à l'infini,
l'exponentielle écrase toute puissance.

| Propriété | Énoncé | Démonstration |
|---|---|---|
| **Récurrence** | $\Gamma(s+1)=s\,\Gamma(s)$ | IPP avec $u=t^s$, $v'=e^{-t}$ |
| **Factorielle** | $\Gamma(n)=(n-1)!$ pour $n\in\mathbb N^*$ | $\Gamma(1)=1$ puis récurrence |
| ⭐ **Demi-entier** | $\Gamma\!\left(\frac12\right)=\sqrt\pi$ | Poser $t=u^2/2$ : on retombe sur Gauss |

$$\Gamma\!\left(\tfrac12\right)=\int_0^\infty t^{-1/2}e^{-t}dt
\;\overset{t=u^2/2}{=}\;\int_0^\infty\frac{\sqrt2}{u}e^{-u^2/2}\,u\,du
=\sqrt2\int_0^{\infty}e^{-u^2/2}du=\sqrt2\cdot\frac{\sqrt{2\pi}}2=\sqrt\pi$$

> 🔑 **$\Gamma$ est la factorielle des demi-entiers**, et c'est pour cela qu'elle est partout en
> statistique : les degrés de liberté d'un $\chi^2$ ou d'une Student se divisent par 2.

**Deux formules du dépôt qu'elle rend lisibles :**

| Où | Formule | Lecture |
|---|---|---|
| [Densité du $\chi^2(k)$](../../statistique/mathematique/15-loi-du-chi2.md) | $f(x)=\frac{x^{k/2-1}e^{-x/2}}{2^{k/2}\Gamma(k/2)}$ | La constante **est** ce qui normalise $\int f=1$ |
| [Biais de $S$](../convexite/05-jensen-probabiliste.md) | $c_4(n)=\sqrt{\frac2{n-1}}\cdot\frac{\Gamma(n/2)}{\Gamma((n-1)/2)}$ | Un **rapport de $\Gamma$ à demi-entiers** |

Le rapport $\Gamma(n/2)/\Gamma((n-1)/2)$ n'a rien de mystérieux : c'est le prix du passage de
$S^2$ à $S$, c'est-à-dire d'un moment d'ordre 2 à un moment d'ordre 1 — un exposant **demi-entier**,
donc une $\Gamma$ en demi-entier.

---

## 4.5 Moments et queues : quand une espérance n'existe pas

$$E\big(\lvert X\rvert^p\big)=\int_{-\infty}^{+\infty}\lvert x\rvert^pf(x)\,dx$$

La convergence se joue **dans les queues**, et le critère de Riemann tranche.

> **Règle.** Si $f(x)\sim\dfrac{c}{x^{\alpha+1}}$ quand $x\to+\infty$ (queue de type Pareto
> d'indice $\alpha>0$), alors
> $$E(X^p)<\infty\iff p<\alpha .$$

*Pourquoi.* $\displaystyle\int^{\infty}x^p\cdot\frac{c}{x^{\alpha+1}}\,dx=c\int^{\infty}x^{\,p-\alpha-1}\,dx$,
qui converge — critère de Riemann — si et seulement si l'exposant est $<-1$, c'est-à-dire
$p-\alpha-1<-1$, soit $p<\alpha$. $\blacksquare$

| Loi | Indice de queue | Espérance | Variance |
|---|---|---|---|
| Normale, exponentielle | Décroissance exponentielle | ✅ | ✅ Tous les moments |
| Pareto $\alpha=3$ | 3 | ✅ | ✅ ($p=2<3$) |
| Pareto $\alpha=1{,}5$ | 1,5 | ✅ | ❌ **Variance infinie** |
| Cauchy | 1 | ❌ | ❌ |

> ⚠️ **« Variance finie » est une hypothèse d'intégrabilité, pas une formalité.** C'est
> l'hypothèse dont dépend tout le [TCL](../../statistique/mathematique/12-theoreme-central-limite.md) — et sur
> données financières, les indices de queue estimés se situent souvent entre 2 et 4, c'est-à-dire
> **au voisinage exact** de la frontière où la variance cesse d'exister
> ([§ 13.1 de statistique](../../statistique/mathematique/13-portee-et-limites-du-tcl.md)).

⚠️ **Un moment empirique existe toujours** : $\frac1n\sum x_i^2$ est un nombre fini, quelles que
soient les données. Ce n'est pas une preuve que $E(X^2)$ existe — c'est même le piège : sur une
loi à variance infinie, la variance empirique **augmente** avec $n$ au lieu de converger. Le § 4.6
le montre.

---

## 4.6 Vérification numérique

### S4.1 — Convergence, divergence, et la frontière $a=1$

```python
import numpy as np

for a in (0.5, 0.9, 1.0, 1.1, 2.0):
    print(f"a={a:4.1f} : ", end="")
    for B in (1e2, 1e4, 1e6, 1e8):
        x = np.linspace(1, B, 2_000_001)
        val = np.trapezoid(x ** (-a), x)
        print(f"int_1^{B:.0e} = {val:12.4f}   ", end="")
    print()
```

Pour $a>1$ la suite se stabilise (vers $\frac1{a-1}$) ; pour $a\le1$ elle croît sans limite — très
lentement à $a=1$ ($\log B$), ce qui est précisément ce qui rend la divergence **invisible** sur
un échantillon fini.

### S4.2 — $\Gamma$, sa récurrence, et le biais de $S$

```python
from math import lgamma, exp, sqrt, pi

G = lambda s: exp(lgamma(s))                    # en log, pour eviter les debordements
print(f"Gamma(1/2) = {G(0.5):.6f}   sqrt(pi) = {sqrt(pi):.6f}")
print(f"Gamma(6) = {G(6):.1f}   5! = 120")
print(f"Gamma(5.5) = {G(5.5):.4f}   4.5*Gamma(4.5) = {4.5 * G(4.5):.4f}")

for n in (5, 10, 30, 100):
    c4 = sqrt(2 / (n - 1)) * exp(lgamma(n / 2) - lgamma((n - 1) / 2))
    print(f"n={n:>4} : c4={c4:.5f}   biais={100 * (c4 - 1):+.2f} %   1-1/(4n)={1 - 1 / (4 * n):.5f}")
```

⚠️ **Toujours calculer une $\Gamma$ en logarithme** (`lgamma`) : $\Gamma(200)$ déborde en flottant,
$\log\Gamma(200)$ non. C'est la règle pour tout rapport de factorielles — la même qu'au
[§ 6b.6 de statistique](../../statistique/mathematique/06b-loi-binomiale.md) pour les coefficients binomiaux.

### S4.3 — Une variance empirique qui ne converge pas

```python
rng = np.random.default_rng(4)
N = 2_000_000

for nom, ech in [("normale", rng.normal(size=N)),
                 ("Pareto alpha=1.5", (1 - rng.random(N)) ** (-1 / 1.5)),
                 ("Cauchy", rng.standard_cauchy(N))]:
    print(f"\n{nom}")
    for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        x = ech[:n]
        print(f"  n={n:>8} : moyenne={x.mean():>12.3f}   variance={x.var():>14.3f}")
```

Sur la normale, les deux colonnes se stabilisent. Sur la Pareto $\alpha=1{,}5$, la moyenne
converge (car $1<1{,}5$) mais **la variance croît avec $n$** (car $2>1{,}5$). Sur la Cauchy,
**rien** ne converge. Les trois lignes du tableau du § 4.5, vues en direct.

---

## 4.7 Exercices

**E4.1.** Étudier la convergence de $\int_0^{+\infty}\frac{dx}{1+x^2}$ et calculer sa valeur.
*Quelle loi de probabilité vient-on de normaliser ?*

**E4.2.** Démontrer $\Gamma(s+1)=s\Gamma(s)$ par IPP, en justifiant l'annulation du crochet aux
deux bornes.

**E4.3.** Montrer que $\int_{-\infty}^{+\infty}x\,dx$ diverge alors que $\int_{-A}^{A}x\,dx=0$
pour tout $A$. *Rédiger en trois lignes pourquoi la loi de Cauchy n'a pas d'espérance.*

**E4.4.** Vérifier que la densité du $\chi^2(k)$ s'intègre bien à 1, en reconnaissant une
$\Gamma$ après le changement de variable $u=x/2$.

**E4.5.** Pour une loi de Pareto de densité $f(x)=\frac{\alpha}{x^{\alpha+1}}$ sur $[1,+\infty[$,
calculer $E(X)$ et $E(X^2)$ **quand ils existent**, et retrouver la règle $p<\alpha$.

**E4.6 — orientée finance.** Sur une série de rendements obtenue avec `historique_sbf250.py` :
1. tracer $\frac1n\sum_{i\le n}r_i^2$ en fonction de $n$ ;
2. la courbe se stabilise-t-elle ? Comparer avec la même courbe sur des tirages gaussiens de même
   écart type ;
3. que conclure quant à l'hypothèse de variance finie du
   [module 12 de statistique](../../statistique/mathematique/12-theoreme-central-limite.md) ?

---

## 4.8 À retenir

- Une intégrale généralisée est une **limite** ; si les deux bornes posent problème, il faut
  **découper** — la symétrie ne sauve rien.
- ⭐ **Riemann** : $\int_1^\infty x^{-a}$ converge ssi $a>1$ ; $\int_0^1x^{-a}$ converge ssi
  $a<1$. Presque toutes les questions de moments s'y ramènent.
- **$\int e^{-x^2}=\sqrt\pi$** : la valeur ne vient d'aucune primitive, elle vient d'une intégrale
  **double** ([module 8](08-integrales-multiples-et-jacobien.md)).
- **$\Gamma(s)$** prolonge la factorielle ; $\Gamma(n)=(n-1)!$, $\Gamma(1/2)=\sqrt\pi$. Elle
  normalise la densité du $\chi^2$ et chiffre le biais de $S$. À calculer **en logarithme**.
- ⭐ **Queue en $x^{-\alpha-1}$ $\Rightarrow$ $E(X^p)$ existe ssi $p<\alpha$.** « Variance finie »
  est une condition de convergence d'intégrale — celle dont dépend le TCL.
- ⚠️ **Un moment empirique existe toujours** : sa finitude ne prouve rien sur celle du moment
  théorique.

---

⬅️ [Module 3 — L'intégrale et le théorème fondamental](03-integrale-et-theoreme-fondamental.md) ·
➡️ [Module 5 — Dérivées partielles, différentielle, gradient](05-derivees-partielles-et-gradient.md) ·
🏠 [Sommaire](README.md)
