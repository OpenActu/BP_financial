# Module 6a — La loi de Bernoulli

**Durée : 45 min.** Prérequis : modules [2](02-esperance.md), [3](03-variance-et-moments.md),
[5](05-fonction-generatrice-des-moments.md) et [6](06-fonction-caracteristique.md).

> **La question traitée.** Les modules 1 à 6 ont construit des **outils** — espérance, variance,
> transformées — sans jamais les faire tourner sur une loi précise. Ce module et les cinq
> suivants les appliquent aux six lois qui reviennent partout. On commence par la plus simple :
> celle qui ne répond que par oui ou non.

**Ce qui est en jeu.** La Bernoulli est l'**atome** du cours : la binomiale en est une somme
([module 6b](06b-loi-binomiale.md)), la Poisson une limite ([module 6c](06c-loi-de-poisson.md)), et toute probabilité $P(A)$ est l'espérance d'une
Bernoulli. Tout ce qui est démontré ici se propage ensuite sans nouveau calcul.

> 📐 **Le plan des six modules 6a–6f est toujours le même**, et il est volontairement
> répétitif : définition → espérance et variance **sans transformée** → les mêmes **par la
> fonction caractéristique** → propriétés → exemple complet → simulation. La leçon est dans la
> répétition : le second chemin est toujours le même quel que soit la loi, alors que le premier
> change à chaque fois.

---

## 6a.1 Définition

> **Définition.** $X$ suit une **loi de Bernoulli** de paramètre $p\in[0,1]$, notée
> $X\sim\mathcal B(p)$, si
> $$P(X=1)=p,\qquad P(X=0)=q:=1-p$$

C'est le modèle de **l'épreuve à deux issues** : succès/échec, pile/face, hausse/baisse. Sa
portée dépasse largement le jeu de hasard :

> 🔑 **Toute probabilité est une espérance de Bernoulli.** Pour un événement $A$ quelconque, la
> variable indicatrice $\mathbf 1_A$ (qui vaut 1 si $A$ se réalise, 0 sinon) suit
> $\mathcal B\bigl(P(A)\bigr)$, et
> $$E(\mathbf 1_A)=P(A)$$
> C'est ce pont qui permet d'estimer *n'importe quelle* probabilité par une moyenne — tout le
> principe de la simulation de Monte-Carlo ([§ 6d.5](06d-loi-uniforme.md)).

**La propriété qui simplifie tout.** $X$ ne prend que les valeurs 0 et 1, donc $0^k=0$ et
$1^k=1$ :

$$\boxed{\;X^k=X\quad\text{pour tout } k\ge 1\;}$$

Cette identité, triviale, remplace à elle seule la moitié des calculs qui suivent.

---

## 6a.2 Espérance et variance, sans transformée

**Espérance.** Par la définition du [§ 2.1](02-esperance.md), la somme ne comporte que deux
termes :

$$E(X)=\sum_{k\in\{0,1\}}k\,P(X=k)=0\times q+1\times p=\boxed{\,p\,}$$

**Moment d'ordre 2.** C'est ici que $X^2=X$ intervient — aucune somme à recalculer :

$$E(X^2)=E(X)=p$$

**Variance.** Par la formule de König–Huygens ([§ 3.1](03-variance-et-moments.md)),
$\operatorname{Var}(X)=E(X^2)-E(X)^2$ :

$$\operatorname{Var}(X)=p-p^2=p(1-p)=\boxed{\,pq\,}\qquad\blacksquare$$

> 🔑 **La variance est maximale en $p=1/2$**, où elle vaut $1/4$, et **nulle** en $p=0$ et $p=1$.
> C'est cohérent avec le sens du mot : une pièce truquée à 99 % est presque déterministe, donc
> presque sans dispersion. La conséquence pratique est au § 6a.5 : $\sqrt{pq}\le 1/2$ donne une
> majoration de l'erreur type qui ne dépend d'**aucun** paramètre inconnu.

**Moments d'ordre supérieur.** La même identité donne tout d'un coup : $E(X^k)=p$ pour tout
$k\ge1$. D'où l'asymétrie ([§ 3.4](03-variance-et-moments.md)) :

$$\gamma_1=\frac{E\bigl[(X-p)^3\bigr]}{(pq)^{3/2}}=\frac{pq(q-p)}{(pq)^{3/2}}=\frac{1-2p}{\sqrt{pq}}$$

⚠️ Elle **explose** quand $p\to 0$ : pour $p=5\,\%$, $\gamma_1\approx 4{,}13$. C'est exactement la
ligne « Bernoulli 5 % » du [§ 13.2](13-portee-et-limites-du-tcl.md), et la raison pour laquelle
l'approximation normale y est si lente.

---

## 6a.3 Espérance et variance, par la fonction caractéristique

### Le mode d'emploi, valable pour toutes les lois

C'est la recette qui sera reprise à l'identique dans les cinq modules suivants. Elle découle de
(P4) ([§ 6.2](06-fonction-caracteristique.md)) : quand $E(X^2)<\infty$, on peut dériver deux fois
sous l'espérance, et

$$\varphi_X'(t)=E\!\left(iX\,e^{itX}\right),\qquad \varphi_X''(t)=E\!\left(-X^2e^{itX}\right)$$

En évaluant en $t=0$, où $e^{i\cdot 0\cdot X}=1$ :

> **Mode d'emploi.**
> $$\boxed{\;E(X)=\frac{\varphi_X'(0)}{i}=-\,i\,\varphi_X'(0),
> \qquad E(X^2)=-\,\varphi_X''(0),
> \qquad \operatorname{Var}(X)=-\varphi_X''(0)+\varphi_X'(0)^2\;}$$

Plus généralement $E(X^k)=i^{-k}\varphi_X^{(k)}(0)$ — la fonction caractéristique **engendre les
moments** exactement comme la FGM du [§ 5.2](05-fonction-generatrice-des-moments.md), au facteur
$i^k$ près.

### La fonction caractéristique de la Bernoulli

$$\varphi_X(t)=E\!\left(e^{itX}\right)
=e^{it\cdot 0}\,P(X=0)+e^{it\cdot 1}\,P(X=1)
=\boxed{\;q+p\,e^{it}\;}$$

Aucune intégrale : la loi ne charge que deux points. (La FGM s'obtient de la même façon :
$M_X(t)=q+pe^{t}$, finie pour tout $t$ — c'est l'exercice E5.1.)

### Les deux dérivations

$$\varphi_X'(t)=ip\,e^{it}\;\Longrightarrow\;\varphi_X'(0)=ip
\qquad\Longrightarrow\qquad E(X)=-i\times ip=p\;\checkmark$$

$$\varphi_X''(t)=i^2p\,e^{it}=-p\,e^{it}\;\Longrightarrow\;\varphi_X''(0)=-p
\qquad\Longrightarrow\qquad E(X^2)=-(-p)=p\;\checkmark$$

$$\operatorname{Var}(X)=p-p^2=pq\qquad\blacksquare$$

**Comparaison des deux chemins.**

| | Sans transformée | Par $\varphi_X$ |
|---|---|---|
| Ce qu'il faut trouver | L'astuce $X^2=X$, propre à la Bernoulli | Rien : on dérive |
| Effort | Minimal **ici** | Deux dérivations |
| Généralisation | Aucune — l'astuce ne resservira pas | ⭐ La même recette pour les six lois |
| Donne aussi | — | La somme d'indépendantes ([§ 6b](06b-loi-binomiale.md)) |

> 🔑 **Sur la Bernoulli, la voie directe gagne ; c'est la dernière fois.** Dès la binomiale, la
> voie directe demande une identité combinatoire, et sur la normale une intégration par parties.
> La fonction caractéristique, elle, coûte toujours exactement deux dérivations. **C'est pour
> cela qu'on l'apprend sur les cas où elle ne sert à rien.**

### Les cumulants

$K_X(t)=\log\!\left(q+pe^{it}\right)$, d'où ([§ 6.4](06-fonction-caracteristique.md))
$\kappa_1=p$, $\kappa_2=pq$, $\kappa_3=pq(q-p)$. Aucun n'est nul au-delà de l'ordre 2 dès que
$p\ne 1/2$ : la Bernoulli est **loin** d'une gaussienne, et le module 13 chiffre exactement ce
« loin ».

---

## 6a.4 Les trois propriétés à connaître

| Propriété | Énoncé | Où elle sert |
|---|---|---|
| **Somme** ⭐ | $n$ Bernoulli i.i.d. $\Rightarrow$ leur somme est une $\mathcal B(n,p)$ | [Module 6b](06b-loi-binomiale.md) |
| **Symétrie** | $1-X\sim\mathcal B(1-p)$ | Échanger succès et échec |
| **Variance bornée** | $pq\le 1/4$ | Majoration universelle de l'erreur type |

La première se lit d'une ligne avec (P2) : si $X_1,\dots,X_n$ sont i.i.d. $\mathcal B(p)$,

$$\varphi_{X_1+\dots+X_n}(t)=\left(q+pe^{it}\right)^{n}$$

et le [module 6b](06b-loi-binomiale.md) ne fera que reconnaître ce que cette expression décrit.

---

## 6a.5 Exemple complet — la proportion de séances haussières

**Les données.** Sur les 252 séances d'une année, une action du SBF 250 a clôturé **138 fois** en
hausse. La question du gérant : *cette action monte-t-elle plus souvent qu'elle ne baisse, ou
est-ce du bruit ?*

**① Le modèle.** On pose, pour la séance $t$,

$$X_t=\mathbf 1_{\{r_t>0\}}\sim\mathcal B(p),\qquad X_1,\dots,X_{252}\ \text{i.i.d.}$$

⚠️ **Les deux hypothèses ne se valent pas.** « Même $p$ toutes les séances » est raisonnable sur
un an. « Indépendantes » est l'hypothèse forte, et le [module 14](14-dependance-et-echec-du-tcl.md)
montre ce qu'elle coûte si elle est fausse. On la retient ici, en sachant qu'on la retient.

**② L'estimation.** L'estimateur naturel est la moyenne empirique, qui est ici une proportion :

$$\hat p=\bar X=\frac{1}{252}\sum_{t=1}^{252}X_t=\frac{138}{252}=0{,}5476$$

Il est **sans biais** : $E(\hat p)=E(X_1)=p$ par la seule linéarité de l'espérance
([§ 2.3](02-esperance.md)) — aucune hypothèse d'indépendance n'est requise pour ce point.

**③ La précision.** Là, l'indépendance sert. Par le [§ 3.3](03-variance-et-moments.md),

$$\operatorname{Var}(\hat p)=\frac{\operatorname{Var}(X_1)}{n}=\frac{p(1-p)}{n}
\qquad\Longrightarrow\qquad
\widehat{\operatorname{se}}(\hat p)=\sqrt{\frac{\hat p(1-\hat p)}{n}}
=\sqrt{\frac{0{,}5476\times0{,}4524}{252}}=0{,}0314$$

C'est ici, et uniquement ici, que le calcul de variance du § 6a.2 est utilisé.

**④ L'intervalle de confiance.** La somme de 252 Bernoulli étant très bien approchée par une
normale ([module 12](12-theoreme-central-limite.md)), l'intervalle à 95 %
([module 18](18-intervalle-de-confiance.md)) est

$$\hat p\pm 1{,}96\times\widehat{\operatorname{se}}
=0{,}5476\pm 1{,}96\times 0{,}0314
=[\,0{,}486\;;\;0{,}609\,]$$

**⑤ La conclusion.** **L'intervalle contient $0{,}5$.** Sur une année de données, on ne peut pas
distinguer cette action d'une pièce équilibrée. 138 hausses sur 252 « ont l'air » d'un avantage ;
la variance de la Bernoulli dit que non.

**⑥ Le contrôle sans paramètre.** Puisque $pq\le 1/4$, on a **toujours**

$$\operatorname{se}(\hat p)\le\frac{1}{2\sqrt n}=\frac{1}{2\sqrt{252}}=0{,}0315$$

Presque la valeur estimée — parce que $\hat p$ est proche de $1/2$, là où la borne est atteinte.
Cette majoration est ce qui permet de **dimensionner un échantillon avant de l'avoir** : pour une
marge de $\pm 1\,\%$ à 95 %, il faut $1{,}96/(2\sqrt n)\le 0{,}01$, soit $n\ge 9\,604$.

> 🔑 **La leçon de l'exemple.** Le nombre 0,5476 ne dit rien tout seul. C'est
> $\operatorname{Var}(X)=pq$ — deux lignes du § 6a.2 — qui transforme une proportion en une
> **affirmation défendable**, ou, comme ici, en un aveu d'ignorance.

---

## 6a.6 Simulation

### S6a.1 — Vérifier $E$, $\operatorname{Var}$, $\varphi$, et la couverture de l'intervalle

```python
import numpy as np

rng = np.random.default_rng(6)
p, N = 0.5476, 1_000_000
X = (rng.random(N) < p).astype(float)          # une Bernoulli(p) écrite à la main

print(f"E(X)   empirique = {X.mean():.4f}   theorie p    = {p:.4f}")
print(f"Var(X) empirique = {X.var():.4f}   theorie p(1-p) = {p*(1-p):.4f}")
print(f"E(X^2) empirique = {(X**2).mean():.4f}   theorie p  = {p:.4f}   (car X^2 = X)")

# la fonction caracteristique, valeur par valeur
for t in (0.3, 1.0, 2.5):
    emp = np.mean(np.exp(1j * t * X))
    the = (1 - p) + p * np.exp(1j * t)
    print(f"t={t}: phi empirique = {emp:+.4f}   theorie q+p e^(it) = {the:+.4f}")

# la couverture reelle de l'intervalle du § 6a.5
n, M = 252, 20_000
S = rng.binomial(n, p, M) / n                  # M annees independantes
se = np.sqrt(S * (1 - S) / n)
couvre = (np.abs(S - p) <= 1.96 * se).mean()
print(f"\ncouverture de l'IC 95% sur {M} echantillons : {couvre:.1%}")
```

La couverture tombe autour de 94–95 % : l'intervalle du § 6a.5 tient sa promesse, **parce que
$p$ est proche de $1/2$**. Refaites tourner avec `p = 0.02` : la couverture s'effondre, pour la
raison chiffrée au [§ 13.2](13-portee-et-limites-du-tcl.md) — $\gamma_1=(1-2p)/\sqrt{pq}$ explose.

---

## 6a.7 Exercices

**E6a.1.** Démontrer $E(X^k)=p$ pour tout $k\ge1$ **sans calcul**, puis retrouver
$\varphi_X(t)=q+pe^{it}$ en développant $e^{itX}=\sum_k (it)^kX^k/k!$. *Les deux résultats sont
le même.*

**E6a.2.** Montrer que $p\mapsto p(1-p)$ est maximale en $p=1/2$. *En déduire la taille
d'échantillon nécessaire pour une marge de $\pm 3\,\%$ à 95 %, sans connaître $p$.*

**E6a.3.** Calculer $\kappa_3=pq(q-p)$ à partir de $K_X(t)=\log(q+pe^{it})$, puis retrouver
$\gamma_1=(1-2p)/\sqrt{pq}$. *Pour quelle valeur de $p$ l'asymétrie s'annule-t-elle ? Que devient
alors la vitesse du TCL ?*

**E6a.4.** Soit $Y=2X-1$, à valeurs dans $\{-1,+1\}$. Calculer $E(Y)$, $\operatorname{Var}(Y)$ et
$\varphi_Y$. *Vérifier avec (P3) et la propriété affine. Pour quel $p$ la fonction $\varphi_Y$
est-elle réelle ? Relier à l'exercice E6.1.*

**E6a.5.** On observe 138 hausses sur 252 séances, mais les séances sont **corrélées** :
$\rho(X_t,X_{t+1})=0{,}1$. *Sans refaire le calcul complet, dire dans quel sens l'intervalle du
§ 6a.5 est faux, et pourquoi le [module 14](14-dependance-et-echec-du-tcl.md) qualifie cette
erreur de plus coûteuse que la non-normalité.*

---

## 6a.8 À retenir

- **$E(X)=p$, $\operatorname{Var}(X)=pq$** — et $X^2=X$ rend la démonstration directe immédiate.
- **$\varphi_X(t)=q+pe^{it}$**, d'où les mêmes résultats par deux dérivations : c'est la recette
  générique $E(X)=-i\varphi'(0)$, $E(X^2)=-\varphi''(0)$, reprise dans les cinq modules suivants.
- ⭐ **$\mathbf 1_A$ est une Bernoulli et $E(\mathbf 1_A)=P(A)$** : estimer une probabilité, c'est
  toujours moyenner une Bernoulli.
- **$pq\le 1/4$** donne une erreur type majorée par $1/(2\sqrt n)$ **sans connaître $p$** — de quoi
  dimensionner un échantillon à l'avance.
- ⚠️ **$\gamma_1=(1-2p)/\sqrt{pq}$ explose pour $p$ extrême** : c'est la loi sur laquelle
  l'approximation normale est la plus lente.

---

⬅️ [Module 6 — La fonction caractéristique](06-fonction-caracteristique.md) ·
➡️ [Module 6b — La loi binomiale](06b-loi-binomiale.md) ·
🏠 [Sommaire](README.md)
