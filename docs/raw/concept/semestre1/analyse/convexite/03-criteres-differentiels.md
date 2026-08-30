# Module 3 — Les critères différentiels ⭐

**Durée : 1 h 15.** Prérequis : [module 2](02-fonctions-convexes.md). ⭐ **Module central : c'est
ici qu'est fabriqué l'outil qui démontre tout le reste du cours.**

> **La question traitée.** Comment reconnaître une fonction convexe quand elle est dérivable — et
> surtout, quelle **inégalité** en tirer ?

**Ce qui est en jeu.** Le critère $f''\ge0$ sert à *reconnaître*. L'inégalité de la tangente,

$$f(y)\;\ge\;f(x)+f'(x)(y-x),$$

sert à *démontrer* : Jensen ([module 4](04-jensen-fini-et-moyennes.md) et
[module 5](05-jensen-probabiliste.md)), la condition d'optimalité
([module 6](06-minimisation-convexe.md)) et la sous-additivité
([module 8](08-convexite-et-mesures-de-risque.md)) en sortent toutes en deux lignes.

---

## 3.1 Le critère du premier ordre : $f'$ croissante

> **Théorème.** Soit $f$ dérivable sur un intervalle $I$. Alors
> $$f\ \text{convexe sur }I\iff f'\ \text{croissante sur }I .$$
> $f$ est **strictement** convexe si et seulement si $f'$ est strictement croissante.

**Démonstration ($\Rightarrow$).** Soient $x<z$. Le lemme des trois cordes
([§ 2.2](02-fonctions-convexes.md)) donne, pour tout $y\in\,]x,z[$,

$$\frac{f(y)-f(x)}{y-x}\;\le\;\frac{f(z)-f(y)}{z-y} .$$

En faisant $y\to x^+$ à gauche et $y\to z^-$ à droite, il vient
$f'(x)\le\frac{f(z)-f(x)}{z-x}\le f'(z)$. $\blacksquare$

**Démonstration ($\Leftarrow$).** Soient $x<y$ et $m=\lambda x+(1-\lambda)y$. Le théorème des
accroissements finis fournit $c_1\in\,]x,m[$ et $c_2\in\,]m,y[$ tels que

$$f(m)-f(x)=f'(c_1)(m-x),\qquad f(y)-f(m)=f'(c_2)(y-m).$$

Comme $c_1<c_2$ et $f'$ croissante, $f'(c_1)\le f'(c_2)$. Avec $m-x=(1-\lambda)(y-x)$ et
$y-m=\lambda(y-x)$ :

$$\begin{aligned}
\lambda f(x)+(1-\lambda)f(y)-f(m)
&=(1-\lambda)\big[f(y)-f(m)\big]-\lambda\big[f(m)-f(x)\big]\\[2pt]
&=(1-\lambda)f'(c_2)(y-m)-\lambda f'(c_1)(m-x)\\[2pt]
&=\lambda(1-\lambda)(y-x)\big[f'(c_2)-f'(c_1)\big]\;\ge\;0 .
\end{aligned}$$

C'est exactement l'inégalité de convexité. $\blacksquare$

---

## 3.2 Le critère du second ordre

> **Corollaire.** Si $f$ est deux fois dérivable sur $I$ :
> $$f\ \text{convexe}\iff f''\ge0\ \text{sur }I .$$

C'est le critère de reconnaissance courant — celui qu'invoque
[`modele.md`](../../../../modele.md) quand il écrit qu'une quadratique de coefficient dominant positif est
strictement convexe.

⚠️ **Attention à la stricte convexité.** $f''>0$ **suffit** mais n'est **pas nécessaire** :
$f(x)=x^4$ est strictement convexe alors que $f''(0)=0$. L'équivalence correcte est celle du
§ 3.1 — $f'$ **strictement** croissante — jamais celle portant sur le signe strict de $f''$.

---

## 3.3 ⭐ L'inégalité de la tangente

> **Théorème (inégalité de premier ordre).** $f$ dérivable sur $I$ est convexe si et seulement si
> $$\boxed{\;f(y)\;\ge\;f(x)+f'(x)\,(y-x)\qquad\text{pour tous }x,y\in I\;}$$
> Autrement dit : **le graphe est au-dessus de chacune de ses tangentes.**

**Démonstration ($\Rightarrow$).** Pour $\lambda\in\,]0,1]$, la convexité donne

$$f\big(x+\lambda(y-x)\big)=f\big(\lambda y+(1-\lambda)x\big)\le\lambda f(y)+(1-\lambda)f(x),$$

d'où, en retranchant $f(x)$ et en divisant par $\lambda>0$ :

$$\frac{f\big(x+\lambda(y-x)\big)-f(x)}{\lambda}\;\le\;f(y)-f(x).$$

Le membre de gauche tend vers $f'(x)(y-x)$ quand $\lambda\to0^+$. $\blacksquare$

**Démonstration ($\Leftarrow$).** Poser $m=\lambda x+(1-\lambda)y$ et écrire l'inégalité **deux
fois**, en $y$ puis en $x$, autour du point $m$ :

$$f(x)\ge f(m)+f'(m)(x-m),\qquad f(y)\ge f(m)+f'(m)(y-m).$$

Combiner avec les poids $\lambda$ et $1-\lambda$ : le terme en $f'(m)$ vaut
$f'(m)\big[\lambda x+(1-\lambda)y-m\big]=0$, et il reste
$\lambda f(x)+(1-\lambda)f(y)\ge f(m)$. $\blacksquare$

> 🔑 **Ce « deux fois, puis on combine » est le geste central du cours.** Il reparaîtra
> **identique** au [§ 4.1](04-jensen-fini-et-moyennes.md) avec $n$ points, au
> [§ 5.2](05-jensen-probabiliste.md) avec une espérance, et au
> [§ 8.4](08-convexite-et-mesures-de-risque.md) avec deux portefeuilles. Une seule technique,
> quatre théorèmes.

**Deux conséquences immédiates, à retenir séparément.**

| Conséquence | Énoncé | Où elle sert |
|---|---|---|
| **Minorante affine** | Toute tangente minore $f$ partout | Jensen (modules 4 et 5) |
| **Point critique** | $f'(x^\star)=0\Rightarrow f(y)\ge f(x^\star)$ pour tout $y$ | Minimum **global** ([§ 6.2](06-minimisation-convexe.md)) |

La seconde ligne mérite d'être lue lentement : elle dit qu'**annuler la dérivée d'une fonction
convexe suffit à avoir le minimum global**, sans étude de variations, sans comparaison de valeurs,
sans examen des bords. C'est ce que [`modele.md`](../../../../modele.md) fait deux fois.

---

## 3.4 Le catalogue

| Fonction | Domaine | Convexe ? | Vérification |
|---|---|---|---|
| $ax+b$ | $\mathbb R$ | Convexe **et** concave | $f''=0$ |
| $x^2$, et $x^{2k}$ | $\mathbb R$ | Strictement convexe | $f''=2>0$ ; $x^4$ : voir § 3.2 |
| $e^{ax}$ | $\mathbb R$ | Strictement convexe | $f''=a^2e^{ax}>0$ si $a\ne0$ |
| $-\log x$ | $\mathbb R_+^*$ | Strictement convexe | $f''=1/x^2>0$ |
| $\log x$ | $\mathbb R_+^*$ | Strictement **concave** | $f''=-1/x^2<0$ |
| $x\log x$ | $\mathbb R_+^*$ | Strictement convexe | $f''=1/x>0$ (entropie) |
| $x^a$ | $\mathbb R_+^*$ | Convexe si $a\le0$ ou $a\ge1$ ; concave si $0\le a\le1$ | $f''=a(a-1)x^{a-2}$ |
| $\sqrt x$ | $\mathbb R_+$ | **Concave** | Cas $a=\frac12$ — c'est le biais de $S$ ([§ 5.4](05-jensen-probabiliste.md)) |
| $1/x$ | $\mathbb R_+^*$ | Convexe | Cas $a=-1$ — c'est $E(1/X)\ge1/E(X)$ |
| $\lvert x\rvert$, $\lvert x\rvert^p$ ($p\ge1$) | $\mathbb R$ | Convexe | Non dérivable en 0 : passer par le § 2.1 |
| $\max(0,x)$ | $\mathbb R$ | Convexe | Max de deux affines ([§ 2.3](02-fonctions-convexes.md)) |
| $\frac1{1+e^{-x}}$ (logistique) | $\mathbb R$ | **Ni l'une ni l'autre** | Point d'inflexion en 0 |
| $x^3$ | $\mathbb R$ | **Ni l'une ni l'autre** | Convexe sur $\mathbb R_+$ seulement |

⚠️ **Le domaine fait partie de l'énoncé.** $1/x$ est convexe sur $\mathbb R_+^*$ et concave sur
$\mathbb R_-^*$ ; sur $\mathbb R^*$ — qui n'est pas convexe — la question n'a pas de sens. C'est
la raison pour laquelle le [module 1](01-ensembles-convexes.md) précède celui-ci.

---

## 3.5 Le mémo financier

Trois fonctions de ce catalogue reviennent partout dans ce dépôt, et il vaut la peine de savoir
**par cœur** dans quel sens elles penchent.

| Fonction | Courbure | Ce qu'elle produit une fois moyennée |
|---|---|---|
| $x\mapsto\log(1+x)$ | **Concave** | La moyenne des log-rendements est $\le$ le log du rendement moyen : le **drag de volatilité** ([§ 5.3](05-jensen-probabiliste.md)) |
| $x\mapsto\sqrt x$ | **Concave** | $E(S)<\sigma$ : l'écart type empirique **sous-estime** ([§ 5.4](05-jensen-probabiliste.md)) |
| $x\mapsto x^2$ | **Convexe** | $E(X^2)\ge E(X)^2$ : la variance est positive ([§ 5.2](05-jensen-probabiliste.md)) |

> 🔑 **Une règle mnémotechnique qui ne trompe pas.** *Concave $\Rightarrow$ moyenner d'abord donne
> plus.* Le sens de l'écart ne dépend jamais de la loi, jamais des données : il est fixé par la
> **courbure seule**. C'est ce qui rend ces biais **prévisibles** — donc corrigeables.

---

## 3.6 Simulations

### S3.1 — La tangente passe sous le graphe

```python
import numpy as np

rng = np.random.default_rng(3)

def test_tangente(f, df, a, b, n=200_000):
    x, y = rng.uniform(a, b, n), rng.uniform(a, b, n)
    ecart = f(y) - (f(x) + df(x) * (y - x))      # >= 0 partout <=> convexe
    return ecart.min()

for nom, f, df, a, b in [
    ("exp",   np.exp,               np.exp,                -2, 2),
    ("x^2",   lambda t: t ** 2,     lambda t: 2 * t,       -3, 3),
    ("-log",  lambda t: -np.log(t), lambda t: -1 / t,      .05, 5),
    ("sqrt",  np.sqrt,              lambda t: .5 / np.sqrt(t), .05, 5),
    ("x^3",   lambda t: t ** 3,     lambda t: 3 * t ** 2,  -2, 2),
]:
    print(f"{nom:>6} : min de f(y) - [f(x)+f'(x)(y-x)] = {test_tangente(f, df, a, b):+.4f}")
```

Attendu : $\ge0$ pour `exp`, `x^2`, `-log` ; **négatif** pour `sqrt` (concave, la tangente passe
au-dessus) et pour `x^3` (ni l'un ni l'autre).

### S3.2 — $f''>0$ n'est pas nécessaire à la stricte convexité

```python
t = np.linspace(-1, 1, 9)
for lam in (0.25, 0.5, 0.75):
    x, y = -0.7, 0.9
    m = lam * x + (1 - lam) * y
    corde = lam * x ** 4 + (1 - lam) * y ** 4
    print(f"lam={lam}: f(m)={m ** 4:.6f} < corde={corde:.6f} ?  {m ** 4 < corde}")
print("f''(0) =", 12 * 0.0 ** 2, "-> nulle, et pourtant stricte convexité")
```

$x^4$ est **strictement** convexe bien que sa dérivée seconde s'annule en 0 : le critère par
$f''>0$ est suffisant, jamais nécessaire.

---

## 3.7 Exercices

**E3.1.** Démontrer l'inégalité de la tangente **sans** utiliser la définition de la dérivée,
mais à partir du lemme des trois cordes.

**E3.2.** Montrer que $x\mapsto x\log x$ est strictement convexe sur $\mathbb R_+^*$, puis en
déduire par l'inégalité de la tangente que $x\log x\ge x-1$ pour tout $x>0$. *(Prendre la
tangente au bon point.)*

**E3.3.** Pour quelles valeurs de $a$ la fonction $x\mapsto x^a$ est-elle convexe sur
$\mathbb R_+^*$ ? Tracer la frontière et vérifier les trois cas particuliers $a=\frac12$, $a=1$,
$a=-1$.

**E3.4.** Soit $f$ convexe dérivable avec $f'(x^\star)=0$. Démontrer en **une ligne** que $x^\star$
est un minimum global. *Puis expliquer pourquoi la même conclusion est fausse pour $f(x)=x^3$ en
$x^\star=0$ — et à quelle hypothèse cela tient.*

**E3.5.** Soit $u$ une fonction d'utilité, deux fois dérivable, avec $u'>0$ et $u''<0$. Montrer
que $u$ est concave, et interpréter $u'>0$ et $u''<0$ en une phrase chacun. *(À reprendre au
[§ 5.5](05-jensen-probabiliste.md).)*

**E3.6.** La fonction $P(y)$ donnant le prix d'une obligation en fonction du taux $y$ est
$P(y)=\sum_t c_t(1+y)^{-t}$ avec $c_t\ge0$. Montrer que $P$ est **convexe décroissante** sur
$]-1,+\infty[$. *(Ce sera tout le [module 9](09-la-convexite-obligataire.md).)*

---

## 3.8 À retenir

- **$f$ convexe $\iff$ $f'$ croissante $\iff$ $f''\ge0$** (sous les hypothèses de dérivabilité
  correspondantes). Le critère avec $f''$ est le plus commode, le critère avec $f'$ est le plus
  général.
- ⚠️ **$f''>0$ est suffisant mais non nécessaire** à la stricte convexité : $x^4$.
- ⭐ **L'inégalité de la tangente** $f(y)\ge f(x)+f'(x)(y-x)$ est **l'outil** du cours : toute
  tangente est une minorante affine de $f$.
- Elle donne immédiatement : **$f'(x^\star)=0\Rightarrow x^\star$ minimum global**. Annuler une
  dérivée ne prouve rien en général ; sur une convexe, cela prouve tout.
- **Le catalogue** : $e^x$, $x^2$, $-\log x$, $x\log x$, $1/x$, $\lvert x\rvert$, $\max(0,x)$ sont
  convexes ; $\log x$ et $\sqrt x$ sont **concaves** — ce sont les deux dont ce dépôt paie le
  biais.

---

⬅️ [Module 2 — Fonctions convexes](02-fonctions-convexes.md) ·
➡️ [Module 4 — Jensen fini et les moyennes](04-jensen-fini-et-moyennes.md) ·
🏠 [Sommaire](README.md)
