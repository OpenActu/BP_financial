# Module 2 — Taylor et les approximations qui servent

**Durée : 1 h.** Prérequis : [module 1](01-derivee-et-approximation-affine.md).

> **La question traitée.** L'approximation affine du module 1 commet une erreur. Quelle est-elle,
> et comment la contrôler ?

**Ce qui est en jeu.** Trois formules de ce dépôt sortent **toutes** d'un développement d'ordre 2,
et il vaut la peine de les voir naître au même endroit : le $\sigma^2/2$ du drag de volatilité, le
$\frac12C(\Delta y)^2$ de la convexité obligataire, et le $\frac12\sigma^2A(\mu)$ de la prime de
risque. Une seule formule, trois lectures.

---

## 2.1 Les trois formes de Taylor

Toutes disent : *$f$ est un polynôme, à un reste près*. Elles diffèrent par ce qu'elles affirment
du **reste**.

> **① Taylor–Young (local, qualitatif).** Si $f$ est $n$ fois dérivable en $a$ :
> $$f(a+h)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}h^k+o(h^n)$$

> **② Taylor–Lagrange (global, quantitatif).** Si $f$ est $n+1$ fois dérivable sur $[a,a+h]$, il
> existe $c$ strictement entre $a$ et $a+h$ tel que
> $$f(a+h)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}h^k+\frac{f^{(n+1)}(c)}{(n+1)!}h^{n+1}$$

> **③ Reste intégral (exact).** Si $f$ est $C^{n+1}$ :
> $$f(a+h)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}h^k
> +\int_0^h\frac{(h-t)^n}{n!}f^{(n+1)}(a+t)\,dt$$

| Forme | Ce qu'elle donne | Quand l'utiliser |
|---|---|---|
| Young | $o(h^n)$ — **aucune** borne | Calculs de limites, ordres de grandeur |
| Lagrange | Une **borne**, via $\sup\lvert f^{(n+1)}\rvert$ | Majorer une erreur d'approximation |
| Intégral | Le reste **exact** | Quand on veut le signe, ou une identité |

> 🔑 **C'est exactement la distinction du [module 12 de statistique](../../statistique/mathematique/12-theoreme-central-limite.md)** :
> le TCL donne un $o(1)$ (Young), Berry–Esseen donne une borne (Lagrange). Un développement
> qualitatif ne devient un chiffre qu'au prix d'une hypothèse supplémentaire — ici, une majoration
> de la dérivée suivante.

---

## 2.2 Les cinq développements à connaître par cœur

Au voisinage de $0$ :

| Fonction | Développement | Premier terme négligé |
|---|---|---|
| $e^x$ | $1+x+\frac{x^2}2+\frac{x^3}6+\cdots$ | $\frac{x^3}6$ |
| $\log(1+x)$ | $x-\frac{x^2}2+\frac{x^3}3-\cdots$ | $\frac{x^3}3$ |
| $(1+x)^\alpha$ | $1+\alpha x+\frac{\alpha(\alpha-1)}2x^2+\cdots$ | ordre 3 |
| $\frac1{1+x}$ | $1-x+x^2-x^3+\cdots$ | cas $\alpha=-1$ |
| $\sqrt{1+x}$ | $1+\frac x2-\frac{x^2}8+\cdots$ | cas $\alpha=\frac12$ |

⚠️ **Le rayon de validité n'est pas infini.** Les trois derniers ne valent que pour
$\lvert x\rvert<1$. Sur des rendements journaliers ($\lvert x\rvert<5\,\%$), aucun problème ; sur
une variation de taux de $200$ points de base appliquée dix ans, la question se pose — c'est le
sujet du § 2.4.

---

## 2.3 D'où vient le $\sigma^2/2$

Le [§ 5.3 du cours d'analyse](../convexite/05-jensen-probabiliste.md) énonce
$g\approx\mu-\frac{\sigma^2}2$. Voici le calcul complet, qui tient en trois lignes de Taylor.

Le taux de croissance géométrique est $g=E\big[\log(1+R)\big]$. Développons à l'ordre 2 autour
de 0 :

$$\log(1+R)=R-\frac{R^2}{2}+O(R^3).$$

Prenons l'espérance, terme à terme (**linéarité**, [§ 2.3 de statistique](../../statistique/mathematique/02-esperance.md)) :

$$g=E(R)-\frac{E(R^2)}{2}+O(E(R^3))
=\mu-\frac{\mu^2+\sigma^2}{2}+O(\cdot)
\;\approx\;\boxed{\;\mu-\frac{\sigma^2}{2}\;}$$

la dernière étape négligeant $\mu^2$ devant $\sigma^2$ — légitime en rendement journalier, où
$\mu\sim10^{-4}$ et $\sigma\sim10^{-2}$ : $\mu^2$ est $10^4$ fois plus petit.

> 🔑 **Le $\frac12$ vient du $\frac{x^2}{2}$ de Taylor, et le $\sigma^2$ vient de $E(R^2)$.** Deux
> objets d'origines différentes — une dérivée seconde et un moment — qui se rencontrent dans une
> espérance. C'est le mécanisme de **toutes** les approximations du second ordre en probabilité,
> y compris la delta-méthode ([§ 11bis.5 de statistique](../../statistique/mathematique/11bis-convergence-en-loi.md))
> et la prime de risque d'Arrow–Pratt.

### Le même calcul, trois fois

| Objet | Fonction développée | Terme d'ordre 2 | Signe |
|---|---|---|---|
| Drag de volatilité | $\log(1+R)$, **concave** | $-\frac{\sigma^2}{2}$ | Coût |
| Convexité obligataire | $P(y)$, **convexe** | $+\frac12C(\Delta y)^2$ | Gain |
| Prime de risque | $u(W)$, **concave** | $-\frac12\sigma^2\lvert u''\rvert/u'$ | Coût |

> 📐 **Le signe du terme d'ordre 2 est le signe de la dérivée seconde**, c'est-à-dire la
> **courbure** — et l'on retrouve exactement la lecture du
> [cours de convexité](../convexite/README.md). Taylor **calcule** ce que la convexité **oriente**.

---

## 2.4 Contrôler l'erreur : la duration ne suffit pas

Reprenons $P(y)=\sum_tc_t(1+y)^{-t}$, développée autour de $y_0$ :

$$P(y_0+\Delta y)=P(y_0)\Big[1-D_{\text{mod}}\Delta y+\tfrac12C(\Delta y)^2\Big]+R_3 .$$

**Taylor–Lagrange donne le reste** : $R_3=\frac{P'''(c)}{6}(\Delta y)^3$, avec

$$P'''(y)=-\sum_t t(t+1)(t+2)\,c_t\,(1+y)^{-t-3}\;<\;0 .$$

Le reste est donc **négatif pour $\Delta y>0$ et positif pour $\Delta y<0$** — exactement le
changement de signe observé dans le tableau du
[§ 9.3 du cours d'analyse](../convexite/09-la-convexite-obligataire.md) : erreur $+0{,}016$ à
$+1\,\%$, $-0{,}017$ à $-1\,\%$. **Un tableau numérique confirmé par le signe d'une dérivée
troisième.**

| $\Delta y$ | Erreur ordre 1 | Erreur ordre 2 | Rapport |
|---|---|---|---|
| $\pm1\,\%$ | $\approx0{,}44$ | $\approx0{,}017$ | $\approx26$ |
| $\pm2\,\%$ | $\approx1{,}75$ | $\approx0{,}13$ | $\approx13$ |

L'erreur d'ordre 1 est en $(\Delta y)^2$ (elle quadruple quand $\Delta y$ double : $0{,}44\to1{,}75$),
l'erreur d'ordre 2 est en $(\Delta y)^3$ (elle est multipliée par 8 : $0{,}017\to0{,}13$). **Les
exposants se lisent directement dans le tableau** — c'est la meilleure vérification qu'un
développement soit correct.

---

## 2.5 Vérification numérique

### S2.1 — L'ordre du reste se lit sur le rapport des erreurs

```python
import numpy as np

f = np.log1p                       # log(1+x)
for ordre, approx in [(1, lambda x: x),
                      (2, lambda x: x - x ** 2 / 2),
                      (3, lambda x: x - x ** 2 / 2 + x ** 3 / 3)]:
    print(f"\n--- developpement d'ordre {ordre} ---")
    prec = None
    for x in (0.2, 0.1, 0.05, 0.025):
        e = abs(f(x) - approx(x))
        r = "" if prec is None else f"   rapport = {prec / e:6.2f}"
        print(f"x={x:6.3f}   erreur={e:.3e}{r}")
        prec = e
```

Quand $x$ est divisé par 2, l'erreur est divisée par $2^{n+1}$ : **4** à l'ordre 1, **8** à
l'ordre 2, **16** à l'ordre 3. C'est la signature de $O(x^{n+1})$, et c'est le test à faire chaque
fois qu'on doute d'un développement.

### S2.2 — Le drag, terme à terme

```python
rng = np.random.default_rng(2)
for s in (0.05, 0.10, 0.20, 0.40):
    R = np.exp(rng.normal(-s ** 2 / 2, s, 4_000_000)) - 1     # E(R) = 0
    g = np.mean(np.log1p(R))
    print(f"sigma={s:.2f} : E(R)={R.mean():+.5f}   E[log(1+R)]={g:+.5f}"
          f"   -sigma^2/2={-s ** 2 / 2:+.5f}   -E(R^2)/2={-np.mean(R ** 2) / 2:+.5f}")
```

La colonne $-E(R^2)/2$ colle mieux que $-\sigma^2/2$ quand $\sigma$ est grand : c'est que
l'approximation $E(R^2)\approx\sigma^2$ néglige $\mu^2$, et surtout que le terme d'ordre 3 pèse.
**Savoir quel terme on néglige est plus utile que connaître la formule.**

---

## 2.6 Exercices

**E2.1.** Écrire Taylor–Lagrange à l'ordre 2 pour $\log(1+x)$ et majorer l'erreur pour
$\lvert x\rvert\le0{,}1$. *Comparer à l'erreur réelle en $x=0{,}1$ : de quel facteur la borne
est-elle conservatrice ?*

**E2.2.** Retrouver $\sqrt{1+x}\approx1+\frac x2-\frac{x^2}8$ et l'appliquer à
$\sqrt{S^2}$ : en déduire, au second ordre, une explication du biais $E(S)<\sigma$.
*(Comparer avec le [§ 5.4 d'analyse](../convexite/05-jensen-probabiliste.md) : retrouve-t-on le bon
ordre de grandeur $1-\frac1{4n}$ ?)*

**E2.3.** Démontrer la formule d'Arrow–Pratt $\pi\approx\frac12\sigma^2\frac{-u''(\mu)}{u'(\mu)}$
en développant $u$ à l'ordre 2 d'un côté de l'équation $u(\text{CE})=E[u(W)]$ et à l'ordre 1 de
l'autre.

**E2.4.** Écrire le reste intégral à l'ordre 1 pour $f$ convexe et en déduire l'**inégalité de la
tangente** $f(a+h)\ge f(a)+f'(a)h$. *(Piste : le reste est $\int_0^h(h-t)f''(a+t)dt$, et
$f''\ge0$.)* Quel résultat du [module 3 d'analyse](../convexite/03-criteres-differentiels.md)
vient-on de redémontrer, et par quel chemin ?

**E2.5.** Un actif a un rendement journalier moyen de $0{,}04\,\%$ et une volatilité journalière
de $1{,}2\,\%$. Estimer la performance annualisée (252 séances) par $(1+\mu)^{252}$ puis par
$e^{252(\mu-\sigma^2/2)}$. *Quel écart en points de pourcentage ?*

**E2.6.** Vérifier numériquement que l'erreur de l'approximation duration $+$ convexité d'une
obligation est bien en $(\Delta y)^3$, en la mesurant pour $\Delta y=0{,}25\,\%$, $0{,}5\,\%$,
$1\,\%$, $2\,\%$.

---

## 2.7 À retenir

- **Trois Taylor, trois usages** : Young donne un $o(h^n)$, Lagrange une **borne**, la forme
  intégrale le reste **exact**. Ne pas utiliser le premier pour chiffrer.
- **Cinq développements** suffisent à tout ce dépôt : $e^x$, $\log(1+x)$, $(1+x)^\alpha$ et ses
  deux cas particuliers.
- ⭐ **Le $\sigma^2/2$ du drag est le $\frac{x^2}{2}$ de Taylor rencontrant $E(R^2)$.** Même
  mécanisme pour la convexité obligataire et la prime de risque — seul change le **signe de la
  dérivée seconde**.
- **L'ordre d'un reste se vérifie numériquement** : diviser $x$ par 2 divise l'erreur par
  $2^{n+1}$. Test systématique avant de croire un développement.
- **Le signe de la dérivée troisième explique l'asymétrie** de l'approximation duration $+$
  convexité, observée au module 9 d'analyse.

---

⬅️ [Module 1 — La dérivée comme approximation affine](01-derivee-et-approximation-affine.md) ·
➡️ [Module 3 — L'intégrale et le théorème fondamental](03-integrale-et-theoreme-fondamental.md) ·
🏠 [Sommaire](README.md)
