# Module 6b — La loi binomiale

**Durée : 1 h.** Prérequis : [module 6a](06a-loi-de-bernoulli.md).

> **La question traitée.** On répète $n$ fois la même épreuve à deux issues. Combien de succès ?
> La loi de ce **comptage** est la première où les trois chemins de démonstration — combinatoire,
> décomposition, fonction caractéristique — se séparent nettement.

**Ce qui est en jeu.** La binomiale est le premier cas où « somme de variables indépendantes »
cesse d'être un slogan et devient un calcul. Elle est aussi le point de départ des deux
approximations les plus utilisées de la statistique : vers la **Poisson**
([module 6c](06c-loi-de-poisson.md)) quand $p$ est petit, vers la **normale**
([module 12](12-theoreme-central-limite.md)) quand $n$ est grand.

---

## 6b.1 Définition

> **Définition.** $X$ suit une **loi binomiale** de paramètres $n\in\mathbb N^*$ et $p\in[0,1]$,
> notée $X\sim\mathcal B(n,p)$, si $X$ est à valeurs dans $\{0,1,\dots,n\}$ et
> $$P(X=k)=\binom{n}{k}p^k q^{\,n-k},\qquad q=1-p$$

**D'où vient cette formule.** Une suite précise de $n$ résultats comportant $k$ succès a la
probabilité $p^kq^{n-k}$ — c'est l'indépendance qui autorise à multiplier. Il y a
$\binom{n}{k}$ suites de ce type, toutes de même probabilité, et elles sont incompatibles : on
additionne. D'où le produit.

**La lecture qui compte.** Si $X_1,\dots,X_n$ sont i.i.d. $\mathcal B(p)$ :

$$\boxed{\;X=X_1+\dots+X_n\sim\mathcal B(n,p)\;}$$

> 🔑 **Une binomiale n'est rien d'autre qu'une somme de Bernoulli indépendantes.** Toute la suite
> du module consiste à exploiter cette phrase plutôt que la formule de $P(X=k)$.

⚠️ **Ne pas confondre les deux notations.** $\mathcal B(p)$ à un paramètre est une Bernoulli ;
$\mathcal B(n,p)$ à deux paramètres est une binomiale. La première est le cas $n=1$ de la seconde.

---

## 6b.2 Espérance et variance, sans transformée

Deux chemins sont possibles sans jamais écrire $\varphi_X$. Le premier est laborieux, le second
immédiat — et cette différence est instructive.

### Chemin ① — la voie combinatoire, par la définition

**Espérance.** Le terme $k=0$ est nul, on part de $k=1$ :

$$E(X)=\sum_{k=0}^{n}k\binom{n}{k}p^kq^{n-k}
=\sum_{k=1}^{n}k\binom{n}{k}p^kq^{n-k}$$

Tout repose sur une identité de coefficients binomiaux, qui se vérifie en écrivant les
factorielles :

$$k\binom{n}{k}=k\,\frac{n!}{k!\,(n-k)!}=\frac{n!}{(k-1)!\,(n-k)!}
=n\,\frac{(n-1)!}{(k-1)!\,(n-k)!}=n\binom{n-1}{k-1}$$

En l'injectant, puis en posant $j=k-1$ :

$$E(X)=n p\sum_{k=1}^{n}\binom{n-1}{k-1}p^{k-1}q^{n-k}
=np\sum_{j=0}^{n-1}\binom{n-1}{j}p^{j}q^{(n-1)-j}
=np\,\underbrace{(p+q)^{n-1}}_{\textstyle =\,1}=\boxed{\,np\,}$$

La dernière somme est le **binôme de Newton** ; elle vaut 1 parce que $p+q=1$.

**Moment factoriel d'ordre 2.** On ne calcule pas $E(X^2)$ directement : on calcule
$E\bigl(X(X-1)\bigr)$, parce que la même identité s'applique deux fois,

$$k(k-1)\binom{n}{k}=n(n-1)\binom{n-2}{k-2}$$

d'où, en partant de $k=2$ et en posant $j=k-2$ :

$$E\bigl(X(X-1)\bigr)=n(n-1)p^2\sum_{j=0}^{n-2}\binom{n-2}{j}p^jq^{(n-2)-j}=n(n-1)p^2$$

**Variance.** On remonte à $E(X^2)=E\bigl(X(X-1)\bigr)+E(X)=n(n-1)p^2+np$, puis :

$$\operatorname{Var}(X)=n(n-1)p^2+np-(np)^2
=n^2p^2-np^2+np-n^2p^2=np(1-p)=\boxed{\,npq\,}\qquad\blacksquare$$

### Chemin ② — la voie de la décomposition

Puisque $X=\sum_{i=1}^n X_i$ avec $X_i\sim\mathcal B(p)$ indépendantes, et que le
[module 6a](06a-loi-de-bernoulli.md) a établi $E(X_i)=p$, $\operatorname{Var}(X_i)=pq$ :

$$E(X)\overset{\text{linéarité}}{=}\sum_{i=1}^n E(X_i)=np$$

$$\operatorname{Var}(X)\overset{\perp\!\!\!\perp}{=}\sum_{i=1}^n \operatorname{Var}(X_i)=npq$$

Deux lignes contre une page.

> ⚠️ **Les deux égalités n'ont pas le même statut, et c'est le point le plus important du
> module.** La première est vraie **sans aucune hypothèse** — la linéarité de l'espérance
> ([§ 2.3](02-esperance.md)) ne demande rien. La seconde exige que les termes croisés
> $\operatorname{Cov}(X_i,X_j)$ soient nuls ([§ 4.2](04-covariance-et-correlation.md)) : elle
> **tombe** si les épreuves sont corrélées. Une binomiale « avec dépendance » garde $E(X)=np$ et
> perd $\operatorname{Var}(X)=npq$.

---

## 6b.3 Espérance et variance, par la fonction caractéristique

### La fonction caractéristique

Par (P2) et le corollaire du [§ 6.2 bis](06-fonction-caracteristique.md), la f.c. d'une somme de
$n$ variables i.i.d. est la puissance $n$-ième de la f.c. commune. Avec
$\varphi_{X_1}(t)=q+pe^{it}$ (§ 6a.3) :

$$\boxed{\;\varphi_X(t)=\left(q+p\,e^{it}\right)^{n}\;}$$

Le calcul direct — $\sum_k e^{itk}\binom nk p^kq^{n-k}$, reconnu comme le binôme de Newton de
$(q+pe^{it})^n$ — donne évidemment la même chose, et c'est un bon contrôle (exercice E6b.1).

### Les deux dérivations

Posons $u(t)=q+pe^{it}$, de sorte que $u(0)=1$ et $u'(t)=ipe^{it}$, $u'(0)=ip$.

$$\varphi_X'(t)=n\,u(t)^{n-1}u'(t)
\;\Longrightarrow\;\varphi_X'(0)=n\cdot 1\cdot ip=inp
\;\Longrightarrow\;E(X)=-i\times inp=\boxed{\,np\,}\;\checkmark$$

Pour la dérivée seconde, on dérive un produit :

$$\varphi_X''(t)=n(n-1)u(t)^{n-2}u'(t)^2+n\,u(t)^{n-1}u''(t),\qquad u''(t)=i^2pe^{it}$$

$$\varphi_X''(0)=n(n-1)(ip)^2+n(-p)=-n(n-1)p^2-np$$

$$E(X^2)=-\varphi_X''(0)=n(n-1)p^2+np
\qquad\Longrightarrow\qquad \operatorname{Var}(X)=npq\;\checkmark\qquad\blacksquare$$

**Les trois chemins, comparés.**

| | ① Combinatoire | ② Décomposition | ③ Par $\varphi_X$ |
|---|---|---|---|
| Ce qu'il faut savoir | $k\binom nk=n\binom{n-1}{k-1}$, deux fois | $E$ et $\operatorname{Var}$ d'une Bernoulli | (P2) et deux dérivations |
| Longueur | Une page | Deux lignes | Cinq lignes |
| Donne la **loi** de la somme | Non (elle est supposée) | Non | ⭐ **Oui** — par (P1) |
| Résiste à des $X_i$ non identiques | Non | $E$ oui, $\operatorname{Var}$ oui si $\perp\!\!\!\perp$ | ⭐ Oui : $\prod_i \varphi_{X_i}$ |

> 🔑 **Ce que seule la voie ③ apporte.** Les chemins ① et ② supposent connue la loi de $X$ et n'en
> calculent que deux résumés. La voie ③ **démontre la loi elle-même** : $(q+pe^{it})^n$ est la
> f.c. d'une $\mathcal B(n,p)$, donc par (P1) la somme *est* une binomiale. Aucune convolution
> n'a été écrite — c'est le mode d'emploi du [§ 5.4](05-fonction-generatrice-des-moments.md).

---

## 6b.4 Les propriétés à connaître

| Propriété | Énoncé | Démonstration |
|---|---|---|
| **Stabilité** ⭐ | $X\sim\mathcal B(n,p)$, $Y\sim\mathcal B(m,p)$, $X\perp\!\!\!\perp Y$ $\Rightarrow$ $X+Y\sim\mathcal B(n+m,p)$ | $(q+pe^{it})^n(q+pe^{it})^m=(q+pe^{it})^{n+m}$ |
| **Symétrie** | $n-X\sim\mathcal B(n,q)$ | Échanger succès et échec |
| **Asymétrie** | $\gamma_1=\dfrac{1-2p}{\sqrt{npq}}$ | $\kappa_3=npq(q-p)$, additivité des cumulants |
| **Limite Poisson** | $n\to\infty$, $p\to0$, $np\to\lambda$ $\Rightarrow$ $\mathcal B(n,p)\to\mathcal P(\lambda)$ | [§ 6c.4](06c-loi-de-poisson.md) |
| **Limite normale** | $\dfrac{X-np}{\sqrt{npq}}\xrightarrow{\mathcal L}\mathcal N(0,1)$ | [Module 12](12-theoreme-central-limite.md) ; laquelle des deux limites choisir : [§ 11bis.6](11bis-convergence-en-loi.md) |

⚠️ **La stabilité exige le même $p$.** $\mathcal B(n,p)+\mathcal B(m,p')$ avec $p\ne p'$ n'est
**pas** binomiale : le produit $(q+pe^{it})^n(q'+p'e^{it})^m$ ne se factorise pas. C'est la même
mise en garde qu'au [§ 8.3](08-addition-de-lois-et-stabilite-gaussienne.md) : la stabilité est un
privilège, pas une règle.

> 🔑 **L'asymétrie décroît en $1/\sqrt n$.** Comparez avec le § 6a.2 : la Bernoulli seule a
> $\gamma_1=(1-2p)/\sqrt{pq}$, la somme de $n$ Bernoulli a la même chose divisée par $\sqrt n$.
> C'est **exactement** le mécanisme du [module 13](13-portee-et-limites-du-tcl.md), et il est ici
> visible à l'œil nu.

---

## 6b.5 Exemple complet — 138 hausses sur 252 séances sont-elles anormales ?

On reprend les données du [§ 6a.5](06a-loi-de-bernoulli.md), mais on pose maintenant la question
**exactement** : sous l'hypothèse d'une action qui monte une séance sur deux, quelle est la
probabilité d'observer un écart au moins aussi grand que celui constaté ?

**① L'hypothèse à tester.**

$$H_0:\;p=0{,}5\qquad\text{contre}\qquad H_1:\;p\ne0{,}5$$

Sous $H_0$, le nombre de séances haussières suit $X\sim\mathcal B(252\,;\,0{,}5)$.

**② Ce que prédit $H_0$.** Les deux formules du module :

$$E(X)=np=126,\qquad
\sigma(X)=\sqrt{npq}=\sqrt{252\times0{,}25}=\sqrt{63}=7{,}94$$

L'observation est $138$, soit un écart de $+12$, c'est-à-dire $12/7{,}94=1{,}51$ écart-type.

**③ Le calcul exact.** La loi binomiale se somme directement :

$$P(X\ge 138)=\sum_{k=138}^{252}\binom{252}{k}\left(\tfrac12\right)^{252}=0{,}0736$$

La question étant bilatérale (« plus souvent **ou** moins souvent »), la $p$-valeur est le double,
par symétrie de $\mathcal B(n,1/2)$ :

$$p\text{-valeur}=2\times0{,}0736=\boxed{0{,}147}$$

**④ Le calcul approché, et la correction qui manque.** L'approximation normale du module 12
donne, sans précaution :

$$z=\frac{138-126}{7{,}94}=1{,}51\qquad\Longrightarrow\qquad
p\text{-valeur}\approx 2\bigl(1-\Phi(1{,}51)\bigr)=0{,}131$$

L'écart avec 0,147 vient de ce qu'on approche une loi **discrète** par une loi continue. La
**correction de continuité** consiste à remplacer $138$ par $137{,}5$ — la frontière réelle entre
137 et 138 :

$$z_{\text{corr}}=\frac{137{,}5-126}{7{,}94}=1{,}449\qquad\Longrightarrow\qquad
p\text{-valeur}\approx 0{,}147$$

| Méthode | $p$-valeur |
|---|---|
| Binomiale exacte | **0,1472** |
| Normale, sans correction | 0,1306 |
| Normale, **avec** correction de continuité | 0,1474 |

> 🔑 **Un demi-point de discrétisation vaut plus que 252 observations.** L'erreur de
> l'approximation brute (0,131 contre 0,147, soit 11 %) est presque entièrement due à l'oubli du
> $-0{,}5$, pas à la taille de l'échantillon. Sur les lois de comptage, la correction de
> continuité est le premier réflexe, avant toute discussion sur « $n$ est-il assez grand ».

**⑤ La conclusion.** $p$-valeur $=0{,}147$ : au seuil usuel de 5 %, **on ne rejette pas $H_0$**.
La conclusion est identique à celle du § 6a.5 — l'intervalle de confiance contenait $0{,}5$ —
et ce n'est pas un hasard : intervalle et test sont deux lectures du même calcul, ce
qu'établit le [module 18](18-intervalle-de-confiance.md).

**⑥ Ce que l'exemple ne dit pas.** Ne pas rejeter n'est pas prouver que $p=0{,}5$. Avec
$n=252$, la procédure ne détecterait un vrai $p=0{,}55$ qu'environ une fois sur trois. Pour
trancher, il faut $n$ grand — et le § 6a.5 a montré comment le calculer à l'avance.

---

## 6b.6 Simulation

### S6b.1 — Les deux moments, la stabilité, et l'exact contre l'approché

```python
import numpy as np
from math import comb
from scipy.stats import norm

rng = np.random.default_rng(6)
n, p, N = 252, 0.5, 200_000

X = rng.binomial(n, p, N)
print(f"E(X)   = {X.mean():8.3f}   theorie np  = {n*p:8.3f}")
print(f"Var(X) = {X.var():8.3f}   theorie npq = {n*p*(1-p):8.3f}")

# stabilite : B(n,p) + B(m,p) = B(n+m,p), verifiee sur la f.c.
m = 100
A, B = rng.binomial(n, p, N), rng.binomial(m, p, N)
for t in (0.05, 0.2):
    g = np.mean(np.exp(1j * t * (A + B)))
    d = ((1 - p) + p * np.exp(1j * t)) ** (n + m)
    print(f"t={t}: phi_(A+B)={g:+.4f}   theorie B(n+m,p)={d:+.4f}")

# exact contre approche, avec et sans correction de continuite
exact = 2 * sum(comb(n, k) for k in range(138, n + 1)) / 2**n
sd = np.sqrt(n * p * (1 - p))
brut = 2 * (1 - norm.cdf((138 - n*p) / sd))
corr = 2 * (1 - norm.cdf((137.5 - n*p) / sd))
print(f"\np-valeur exacte      = {exact:.4f}")
print(f"normale sans correction = {brut:.4f}")
print(f"normale avec correction = {corr:.4f}")
```

La troisième partie reproduit le tableau du § 6b.5. **Faites varier $p$ vers 0,02** : l'exact et
l'approché divergent alors franchement, et c'est le signal qu'il faut changer d'approximation —
c'est l'objet du [module 6c](06c-loi-de-poisson.md).

---

## 6b.7 Exercices

**E6b.1.** Retrouver $\varphi_X(t)=(q+pe^{it})^n$ **directement**, en calculant
$\sum_k e^{itk}\binom nk p^kq^{n-k}$ par le binôme de Newton. *Comparer avec la démonstration par
(P2) : laquelle utilise l'indépendance, et où ?*

**E6b.2.** Démontrer $k(k-1)\binom nk=n(n-1)\binom{n-2}{k-2}$, puis refaire le calcul de
$E\bigl(X(X-1)\bigr)$ du chemin ①. *Pourquoi passe-t-on par $X(X-1)$ plutôt que par $X^2$ ?*

**E6b.3.** Deux traders exécutent respectivement $n=40$ et $m=60$ ordres, chacun réussi avec la
même probabilité $p$, tous indépendants. *Quelle est la loi du nombre total de réussites ?
Justifier par les fonctions caractéristiques, sans convolution.* **Puis** : si le second a un
taux $p'\ne p$, que reste-t-il de vrai pour $E$ et pour $\operatorname{Var}$ ?

**E6b.4.** Montrer que $\kappa_3\bigl(\mathcal B(n,p)\bigr)=npq(q-p)$ en utilisant l'additivité
des cumulants ([§ 6.4](06-fonction-caracteristique.md)) et le résultat E6a.3. *En déduire
$\gamma_1=(1-2p)/\sqrt{npq}$ et le $n$ nécessaire pour que $\gamma_1<0{,}1$ quand $p=0{,}05$.*

**E6b.5.** Sur les données du § 6b.5, calculer la $p$-valeur exacte si l'on avait observé 138
hausses sur **126** séances… puis expliquer pourquoi la question n'a pas de sens. *Vérifier que
l'approximation normale, elle, produirait un nombre sans broncher.*

---

## 6b.8 À retenir

- **$E(X)=np$, $\operatorname{Var}(X)=npq$** — trois démonstrations, dont une seule (la f.c.)
  démontre aussi **que la somme est binomiale**.
- ⚠️ **$E(X)=np$ ne demande rien ; $\operatorname{Var}(X)=npq$ demande l'indépendance.** C'est la
  ligne de partage du cours entier, ici sur un cas concret.
- **$\varphi_X(t)=(q+pe^{it})^n$** : tout le module tient dans cette puissance $n$-ième, y compris
  la stabilité $\mathcal B(n,p)+\mathcal B(m,p)=\mathcal B(n+m,p)$ — **à $p$ identique**.
- **$\gamma_1=(1-2p)/\sqrt{npq}$** : l'asymétrie de la Bernoulli, divisée par $\sqrt n$. Le TCL
  en action, avant même d'être énoncé.
- ⭐ **Sur une loi discrète, appliquer la correction de continuité** : $-0{,}5$ vaut ici plus que
  toute discussion sur la taille de l'échantillon.

---

⬅️ [Module 6a — La loi de Bernoulli](06a-loi-de-bernoulli.md) ·
➡️ [Module 6c — La loi de Poisson](06c-loi-de-poisson.md) ·
🏠 [Sommaire](README.md)
