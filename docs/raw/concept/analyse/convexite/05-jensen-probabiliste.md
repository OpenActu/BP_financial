# Module 5 — Jensen probabiliste ⭐

**Durée : 1 h 15.** Prérequis : [module 4](04-jensen-fini-et-moyennes.md), et les
[modules 2 et 3 de statistique](../../statistique/mathematique/02-esperance.md) (espérance, variance).

> **La question traitée.** Le [cours de statistique](../../statistique/mathematique/02-esperance.md) énonce
> l'inégalité de Jensen au § 2.5 et l'admet. On la démontre ici — puis on en tire trois faits
> chiffrés que ce dépôt subit en permanence.

**Ce qui est en jeu.** Trois biais que toute analyse de rendements rencontre, et qui sont **le
même** :

| Fait | Fonction en cause | Sens de l'écart |
|---|---|---|
| La performance réalisée est inférieure à la moyenne des rendements | $\log$, concave | Toujours défavorable |
| $S$ sous-estime $\sigma$ | $\sqrt{\ }$, concave | Toujours à la baisse |
| Un investisseur averse paie pour éviter un pari à espérance nulle | $u$, concave | Toujours positif |

Aucun de ces trois écarts n'est un artefact d'échantillon : ils sont **garantis par la courbure**,
et donc prévisibles.

---

## 5.1 L'énoncé

> **Théorème (Jensen).** Soit $X$ une variable aléatoire à valeurs dans un intervalle $I$,
> intégrable, et $g:I\to\mathbb R$ **convexe** telle que $g(X)$ soit intégrable. Alors
> $$\boxed{\;E\big(g(X)\big)\;\ge\;g\big(E(X)\big)\;}$$
> Si $g$ est **concave**, l'inégalité est inversée. Si $g$ est **strictement** convexe, l'égalité
> a lieu **si et seulement si** $X$ est presque sûrement constante.

⚠️ **Trois hypothèses, souvent oubliées.** $X$ doit être intégrable (sinon $E(X)$ n'existe pas),
$g(X)$ aussi (sinon le membre de gauche n'a pas de sens), et $E(X)$ doit appartenir à $I$ — ce qui
est automatique si $I$ est un intervalle, par convexité.

---

## 5.2 La démonstration — la même qu'au module 4

Notons $\mu=E(X)$, qui appartient à $I$. L'inégalité de la tangente
([§ 3.3](03-criteres-differentiels.md)) au point $\mu$ donne, **pour tout** $x\in I$ :

$$g(x)\;\ge\;g(\mu)+g'(\mu)\,(x-\mu).$$

Cette inégalité vaut ponctuellement, donc en particulier en $x=X(\omega)$ pour chaque $\omega$ :

$$g(X)\;\ge\;g(\mu)+g'(\mu)\,(X-\mu)\qquad\text{presque sûrement.}$$

L'espérance étant **croissante** ([§ 2.3 de statistique](../../statistique/mathematique/02-esperance.md)) et
**linéaire** :

$$E\big(g(X)\big)\;\ge\;g(\mu)+g'(\mu)\underbrace{\big(E(X)-\mu\big)}_{=\,0}=g\big(E(X)\big).
\qquad\blacksquare$$

> 🔑 **C'est la démonstration du [§ 4.1](04-jensen-fini-et-moyennes.md), mot pour mot**, avec
> $E$ à la place de $\sum_i\lambda_i$. Les deux opérations partagent exactement les deux
> propriétés utilisées : **linéarité** et **croissance**. Rien d'autre n'a servi — ni la loi de
> $X$, ni son support, ni ses moments d'ordre supérieur.

⚠️ **Si $g$ n'est pas dérivable** ($g=\lvert\cdot\rvert$, $g=\max(0,\cdot)$), la démonstration
tient encore : une convexe admet en tout point intérieur au moins une **droite d'appui**
$g(x)\ge g(\mu)+s(x-\mu)$ (avec $s$ entre les dérivées à gauche et à droite,
[§ 2.4](02-fonctions-convexes.md)), et c'est tout ce dont le calcul a besoin.

### Le catalogue des conséquences

| $g$ | Courbure | Inégalité | Ce que c'est |
|---|---|---|---|
| $x^2$ | Convexe | $E(X^2)\ge E(X)^2$ | $\operatorname{Var}(X)\ge0$ — [§ 3.1 stat](../../statistique/mathematique/03-variance-et-moments.md) |
| $1/x$ sur $\mathbb R_+^*$ | Convexe | $E(1/X)\ge1/E(X)$ | Le rendement moyen d'un panier $\ne$ l'inverse du prix moyen |
| $e^x$ | Convexe | $E(e^X)\ge e^{E(X)}$ | La **FGM** est $\ge$ $e^{\mu t}$ ([§ 5 stat](../../statistique/mathematique/05-fonction-generatrice-des-moments.md)) |
| $\log x$ | **Concave** | $E(\log X)\le\log E(X)$ | Le **drag de volatilité** (§ 5.3) |
| $\sqrt x$ | **Concave** | $E(\sqrt{X})\le\sqrt{E(X)}$ | Le **biais de $S$** (§ 5.4) |
| $u$ utilité | **Concave** | $E(u(W))\le u(E(W))$ | L'**aversion au risque** (§ 5.5) |

---

## 5.3 Le drag de volatilité

**Le problème.** Un actif rapporte, chaque période, un rendement aléatoire $R_t$ d'espérance
$\mu$. Sur $n$ périodes, le capital est multiplié par $\prod_t(1+R_t)$ — un **produit**, alors que
la moyenne $\mu$ décrit une **somme**. Le passage de l'un à l'autre est un logarithme, donc un
Jensen.

> **Proposition.** Le taux de croissance géométrique $g$ vérifie
> $$g=E\big[\log(1+R)\big]\;\le\;\log\big(1+E(R)\big).$$
> Un développement au second ordre autour de $\mu$ donne l'approximation retenue partout :
> $$\boxed{\;g\;\approx\;\mu-\frac{\sigma^2}{2}\;}$$

*Où le $\sigma^2/2$ apparaît.* Avec $\log(1+r)\approx r-\frac{r^2}{2}$ :
$E[\log(1+R)]\approx\mu-\frac{E(R^2)}2=\mu-\frac{\mu^2+\sigma^2}{2}\approx\mu-\frac{\sigma^2}2$
pour $\mu$ petit. Pour des rendements **log-normaux**, l'égalité $g=\mu_{\log}$ et
$\mu=\mu_{\log}+\sigma^2/2$ est **exacte**.

### L'exemple minimal, à connaître

Un actif fait $+10\,\%$ puis $-10\,\%$. La moyenne arithmétique des rendements est **nulle**.
Le capital, lui, est multiplié par $1{,}10\times0{,}90=0{,}99$ : **$-1\,\%$ en deux périodes**, soit
$-0{,}50\,\%$ par période — et $\sigma^2/2=0{,}10^2/2=0{,}50\,\%$.

### Ce que cela coûte, chiffré

| $\mu$ (arithmétique) | $\sigma$ | $g\approx\mu-\sigma^2/2$ | Lecture |
|---|---|---|---|
| $8\,\%$ | $20\,\%$ | $6{,}0\,\%$ | Le cas d'une action de marché développé |
| $8\,\%$ | $40\,\%$ | $0{,}0\,\%$ | **Toute l'espérance est mangée par la volatilité** |
| $10\,\%$ | $60\,\%$ | $-8{,}0\,\%$ | Espérance positive, capital qui fond |

> 🔑 **Deux actifs de même espérance n'ont pas la même performance.** Le plus volatil croît
> moins vite — non par malchance, mais par Jensen. C'est la justification quantitative de la
> phrase « la volatilité est un coût », et la raison pour laquelle un effet de levier accroît
> $\mu$ **linéairement** et $\sigma^2/2$ **quadratiquement.**

⚠️ **Ne pas confondre avec l'aversion au risque** (§ 5.5). Le drag est un fait **comptable** : il
frappe un investisseur parfaitement indifférent au risque. L'aversion, elle, est une préférence.

---

## 5.4 Le biais de l'écart type

Le [cours de statistique](../../statistique/mathematique/02-esperance.md) affirme au § 2.5 que $S$ sous-estime
$\sigma$. C'est un Jensen : $S=\sqrt{S^2}$ et la racine est **strictement concave**, donc

$$E(S)=E\big(\sqrt{S^2}\big)\;<\;\sqrt{E(S^2)}=\sqrt{\sigma^2}=\sigma$$

l'inégalité étant **stricte** dès que $S^2$ n'est pas dégénéré. Le diviseur $n-1$ rend $S^2$ sans
biais ; **aucun diviseur ne peut rendre $\sqrt{S^2}$ sans biais**, parce que le défaut n'est pas
dans la normalisation mais dans la courbure.

**L'ampleur du biais, pour un échantillon gaussien.** On a exactement $E(S)=c_4(n)\,\sigma$ avec
$c_4(n)=\sqrt{\frac{2}{n-1}}\cdot\frac{\Gamma(n/2)}{\Gamma((n-1)/2)}$ :

| $n$ | 3 | 5 | 10 | 30 | 100 |
|---|---|---|---|---|---|
| $c_4(n)$ | 0,8862 | 0,9400 | 0,9727 | 0,9914 | 0,9975 |
| Biais relatif | $-11{,}4\,\%$ | $-6{,}0\,\%$ | $-2{,}7\,\%$ | $-0{,}9\,\%$ | $-0{,}25\,\%$ |
| Approximation $1-\frac1{4n}$ | 0,9167 | 0,9500 | 0,9750 | 0,9917 | 0,9975 |

> 🔑 **Le biais décroît en $1/n$, alors que l'erreur d'estimation décroît en $1/\sqrt n$.** À
> $n=30$, le biais ($-0{,}9\,\%$) est déjà négligeable devant l'incertitude
> ($\approx1/\sqrt{2(n-1)}\approx13\,\%$). C'est pourquoi on vit très bien avec $S$ : le défaut
> **existe**, il est **du bon côté de la prudence** (on sous-estime le risque… ce qui n'est pas
> prudent du tout), mais il est **petit** dès que $n$ dépasse quelques dizaines.

⚠️ **Sur une volatilité annualisée à partir de 20 séances** ($n=20$, cas de la colonne `VAR_20` de
`import_societe.py`), le biais est de $-1{,}3\,\%$ environ. Il s'ajoute au fait, bien plus
grave, que l'annualisation par $\sqrt{252}$ suppose l'indépendance
([module 14 de statistique](../../statistique/mathematique/14-dependance-et-echec-du-tcl.md)).

---

## 5.5 Utilité, aversion au risque, prime de risque

**Le modèle.** Un investisseur évalue une richesse aléatoire $W$ non par $E(W)$ mais par
$E\big(u(W)\big)$, où $u$ est croissante ($u'>0$ : plus est mieux) et **concave** ($u''<0$ : chaque
euro supplémentaire apporte moins que le précédent).

> **Conséquence immédiate (Jensen).** $E\big(u(W)\big)\le u\big(E(W)\big)$ : **le pari est
> toujours moins désirable que son espérance reçue avec certitude.**

> **Définition.** L'**équivalent certain** $\text{CE}$ est le montant sûr de même utilité :
> $u(\text{CE})=E\big(u(W)\big)$. La **prime de risque** est $\pi=E(W)-\text{CE}\ \ge0$.

**Approximation d'Arrow–Pratt.** En développant à l'ordre 2 autour de $\mu=E(W)$ :

$$\boxed{\;\pi\;\approx\;\frac12\,\sigma^2\,A(\mu),\qquad
A(\mu)=-\frac{u''(\mu)}{u'(\mu)}\;}$$

où $A$ est le **coefficient d'aversion absolue au risque**. Pour $u(x)=-e^{-ax}$ (aversion
constante) et $W$ gaussienne, le calcul est **exact** :
$\text{CE}=\mu-\frac a2\sigma^2$.

| $a$ | $\sigma$ | Prime $\frac a2\sigma^2$ |
|---|---|---|
| 2 | $20\,\%$ | $4{,}0\,\%$ de richesse |
| 5 | $20\,\%$ | $10{,}0\,\%$ |
| 2 | $40\,\%$ | $16{,}0\,\%$ |

> 🔑 **Le critère « moyenne–variance » de Markowitz est cette approximation.** Maximiser
> $\mu-\frac a2\sigma^2$ n'est pas un axiome : c'est le développement au second ordre d'une
> utilité concave — exact sous gaussienne et utilité exponentielle, approché sinon. Toute la
> [partie II](06-minimisation-convexe.md) du cours optimise cette expression.

---

## 5.6 Le biais de transformation, en général

Les trois exemples précédents sont un seul énoncé :

> **Règle.** Si $\hat\theta$ est un estimateur **sans biais** de $\theta$ et $g$ est strictement
> convexe, alors $g(\hat\theta)$ est un estimateur **biaisé par excès** de $g(\theta)$ :
> $E\big(g(\hat\theta)\big)>g(\theta)$. Avec $g$ concave, biais par défaut.

**L'absence de biais ne survit donc à aucune transformation non affine.** Quelques cas qu'on
rencontre :

| Estimateur sans biais | Transformation | Résultat |
|---|---|---|
| $S^2$ de $\sigma^2$ | $\sqrt{\ }$ concave | $S$ **sous-estime** $\sigma$ |
| $\hat p$ d'une probabilité | $\frac{p}{1-p}$ convexe | La cote estimée **surestime** |
| $\hat\mu$ d'un rendement | $e^x$ convexe | Le facteur de capitalisation **surestime** |
| $\hat\beta$ d'une pente | $\beta^2$ convexe | Le $R^2$ **surestime** la part expliquée |

> 📐 **Jensen donne le sens, la delta-méthode donne la taille.** Le
> [§ 11bis.5 du cours de statistique](../../statistique/mathematique/11bis-convergence-en-loi.md) montre que
> $g(\hat\theta)$ est asymptotiquement normal de variance $g'(\theta)^2\sigma^2/n$ ; le biais,
> lui, est d'ordre $\frac{g''(\theta)\sigma^2}{2n}$ — **d'un ordre plus petit que l'écart type**,
> ce qui explique qu'on puisse l'ignorer quand $n$ est grand, et pas quand il est petit.

---

## 5.7 Simulations

### S5.1 — Les trois biais, sur la même figure

```python
import numpy as np

rng = np.random.default_rng(5)
N = 400_000

# (a) drag de volatilite : meme esperance, deux volatilites
for mu, s in ((0.08, 0.20), (0.08, 0.40)):
    # rendements log-normaux d'esperance arithmetique mu
    m_log = np.log(1 + mu) - s ** 2 / 2
    R = np.exp(rng.normal(m_log, s, (N, 30))) - 1        # 30 periodes
    print(f"mu={mu:.0%} sigma={s:.0%} : moyenne arithmetique={R.mean():+.4f}"
          f"   croissance geometrique={np.expm1(np.log1p(R).mean()):+.4f}"
          f"   (mu - s^2/2 = {mu - s ** 2 / 2:+.4f})")

# (b) biais de S
from math import lgamma, sqrt, exp
for n in (5, 10, 30, 100):
    X = rng.normal(0, 1, (200_000, n))
    S = X.std(axis=1, ddof=1)
    c4 = sqrt(2 / (n - 1)) * exp(lgamma(n / 2) - lgamma((n - 1) / 2))
    print(f"n={n:>4} : E(S^2)={np.mean(S ** 2):.4f} (attendu 1)"
          f"   E(S)={S.mean():.4f}   c4(n)={c4:.4f}")

# (c) prime de risque, utilite exponentielle
a, mu, s = 2.0, 0.08, 0.20
W = rng.normal(mu, s, N)
CE = -np.log(np.mean(np.exp(-a * W))) / a
print(f"\nequivalent certain simule = {CE:.4f}   theorie mu - a s^2/2 = {mu - a * s ** 2 / 2:.4f}")
```

Les trois blocs vérifient les trois sections. Le (b) est le plus instructif : **$E(S^2)$ tombe sur
1 à la troisième décimale, $E(S)$ non** — le diviseur $n-1$ corrige la variance et rate l'écart
type.

### S5.2 — Le cas d'égalité

```python
c = np.full(N, 1.07)                       # variable constante
print("X constante  :", np.isclose(np.exp(c).mean(), np.exp(c.mean())))
X = rng.normal(1.07, 0.2, N)
print("X non degeneree :", np.isclose(np.exp(X).mean(), np.exp(X.mean())),
      f"   ecart = {np.exp(X).mean() - np.exp(X.mean()):.4f}")
```

L'égalité dans Jensen **caractérise** la variable constante (pour $g$ strictement convexe).
L'écart mesuré est donc un indicateur de dispersion — c'est d'ailleurs, à un facteur près, ce que
mesure $\sigma^2/2$ au § 5.3.

---

## 5.8 Exercices

**E5.1.** Démontrer Jensen pour $g(x)=\lvert x\rvert$, non dérivable en 0, en utilisant une droite
d'appui. *Quelle inégalité classique obtient-on ?*

**E5.2.** Montrer que $E(1/X)\ge1/E(X)$ pour $X>0$, et exhiber une variable où l'écart est
**arbitrairement grand**. *(Piste : une variable qui s'approche de 0 avec une petite
probabilité.)* Conséquence pour un rendement moyen calculé sur des prix.

**E5.3.** Démontrer que pour $X>0$, $E(\log X)\le\log E(X)$, puis en déduire directement
l'inégalité AM $\ge$ GM du [§ 4.2](04-jensen-fini-et-moyennes.md) en prenant $X$ uniforme sur
$\{x_1,\dots,x_n\}$. *Que constate-t-on sur le lien entre les modules 4 et 5 ?*

**E5.4.** Établir $\text{CE}=\mu-\frac a2\sigma^2$ pour $u(x)=-e^{-ax}$ et $W\sim\mathcal N(\mu,\sigma^2)$.
*(Piste : $E(e^{-aW})$ est la FGM de la gaussienne, [§ 7.2 stat](../../statistique/mathematique/07-loi-normale-et-ses-transformees.md).)*
*Pourquoi la richesse initiale n'apparaît-elle pas ?*

**E5.5.** Un fonds affiche « rendement moyen $+12\,\%$ par an sur 10 ans ». Le capital a été
multiplié par 2,3. Ces deux affirmations sont-elles compatibles ? *Calculer la volatilité annuelle
implicite par le drag.*

**E5.6 — orientée finance.** Avec `import_societe.py` :
1. estimer $\mu$ et $\sigma$ quotidiens sur 5 ans ;
2. prédire la performance totale par $(1+\mu)^n$, puis par $e^{n(\mu-\sigma^2/2)}$ ;
3. comparer à la performance réellement observée. *Laquelle des deux formules tombe juste, et
   pourquoi l'autre se trompe-t-elle toujours dans le même sens ?*

---

## 5.9 À retenir

- ⭐ **$E(g(X))\ge g(E(X))$ pour $g$ convexe** ; inversé pour $g$ concave ; **égalité $\iff$ $X$
  constante** (si $g$ est strictement convexe).
- **La démonstration est celle du module 4**, avec $E$ à la place de $\sum\lambda_i$ : elle
  n'utilise que la **linéarité** et la **croissance** de l'espérance.
- **Drag de volatilité** : $g\approx\mu-\frac{\sigma^2}2$. Deux actifs de même espérance n'ont pas
  la même performance réalisée ; l'écart est une fonction de la seule volatilité.
- **Biais de $S$** : $E(S)=c_4(n)\sigma<\sigma$, soit $-2{,}7\,\%$ à $n=10$ et $-0{,}9\,\%$ à
  $n=30$. Aucun diviseur ne le corrige — c'est la racine, pas le $n-1$, qui est en cause.
- **Aversion au risque** : $\pi\approx\frac12\sigma^2A(\mu)$ avec $A=-u''/u'$. Le critère
  moyenne–variance est cette approximation, pas un axiome.
- **Règle générale** : l'absence de biais ne survit à aucune transformation non affine. Jensen
  donne le **sens** du biais, la delta-méthode sa **taille**.

---

⬅️ [Module 4 — Jensen fini et les moyennes](04-jensen-fini-et-moyennes.md) ·
➡️ [Module 6 — Minimisation convexe](06-minimisation-convexe.md) ·
🏠 [Sommaire](README.md)
