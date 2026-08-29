# Module 6f — La loi normale

**Durée : 1 h.** Prérequis : [module 6e](06e-loi-exponentielle.md).

> **La question traitée.** Établir $E(X)=\mu$ et $\operatorname{Var}(X)=\sigma^2$ — les deux
> égalités les plus utilisées de toute la statistique — puis montrer sur un cas réel ce qu'elles
> permettent, et où elles trompent.

**Ce qui est en jeu.** La normale est la seule loi du chapitre dont les paramètres **sont** ses
deux premiers moments : $\mu$ et $\sigma^2$ ne sont pas des intermédiaires de calcul comme
$\lambda$ ou $p$, ce sont directement l'espérance et la variance. Encore faut-il le démontrer.

> ⚠️ **Ce module ne fait pas double emploi avec le module 7.** Le
> [module 7](07-loi-normale-et-ses-transformees.md) démontre les **transformées**
> $M_Z(t)=e^{t^2/2}$ et $\varphi_Z(t)=e^{-t^2/2}$ ; c'est son objet unique, et le § 6f.3
> se contente d'en **utiliser** le résultat (avec un rappel de trois lignes de la démonstration).
> Ici on traite l'espérance, la variance, les moments et un cas d'usage complet.

---

## 6f.1 Définition

> **Définition.** $X$ suit une **loi normale** de paramètres $\mu\in\mathbb R$ et $\sigma^2>0$,
> notée $X\sim\mathcal N(\mu,\sigma^2)$, si elle admet la densité
> $$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right),
> \qquad x\in\mathbb R$$

**Le cas standard** est $Z\sim\mathcal N(0,1)$, de densité $\phi(z)=e^{-z^2/2}/\sqrt{2\pi}$. Tout
le reste s'en déduit par une transformation affine, et c'est la seule chose à retenir :

$$\boxed{\;X=\mu+\sigma Z\;\Longleftrightarrow\;Z=\frac{X-\mu}{\sigma}\;}$$

**D'où vient le $\sqrt{2\pi}$.** C'est la constante qui fait de $f$ une densité, et elle vient de
l'**intégrale de Gauss** :

$$\int_{-\infty}^{+\infty}e^{-z^2/2}\,dz=\sqrt{2\pi}$$

*(Démonstration classique : élever au carré, lire le produit comme une intégrale double sur
$\mathbb R^2$, passer en coordonnées polaires — l'élément $r\,dr$ rend l'intégrale élémentaire.
On l'admet ici ; le [module 11](11-invariance-par-rotation-et-lemme-de-projection.md) montrera
que cette invariance par rotation n'est pas un artifice de calcul mais **la** propriété
structurante de la gaussienne.)*

⚠️ **La densité n'a pas de primitive élémentaire.** $F(x)=\Phi\!\left(\frac{x-\mu}{\sigma}\right)$
ne s'écrit avec aucune fonction usuelle : on la tabule, ou on appelle `norm.cdf`. C'est la seule
loi du chapitre dans ce cas — et cela ne gêne en rien les calculs de moments qui suivent.

---

## 6f.2 Espérance et variance, sans transformée

Tout se démontre sur $Z\sim\mathcal N(0,1)$ ; le cas général suit par linéarité.

### $E(Z)=0$ — par symétrie, mais pas seulement

**D'abord l'existence.** L'espérance n'est définie que si $E(|Z|)<\infty$
([§ 2.1](02-esperance.md)) :

$$E(|Z|)=2\int_0^{\infty}z\,\frac{e^{-z^2/2}}{\sqrt{2\pi}}\,dz
=\frac{2}{\sqrt{2\pi}}\Bigl[-e^{-z^2/2}\Bigr]_0^{\infty}
=\sqrt{\frac{2}{\pi}}<\infty\quad\checkmark$$

**Ensuite la valeur.** La fonction $z\mapsto z\,\phi(z)$ est **impaire** ($\phi$ est paire), et
son intégrale converge absolument : les deux moitiés se compensent exactement.

$$E(Z)=\int_{-\infty}^{+\infty}z\,\phi(z)\,dz=\boxed{\,0\,}$$

> ⚠️ **L'ordre des deux arguments n'est pas négociable.** La loi de **Cauchy** est elle aussi
> parfaitement symétrique, et pourtant $E(X)$ **n'existe pas** — parce que l'intégrale ne converge
> pas absolument ([§ 13.1](13-portee-et-limites-du-tcl.md)). « Symétrique donc d'espérance nulle »
> est un raisonnement faux ; « intégrable **et** symétrique, donc d'espérance nulle » est correct.

### $\operatorname{Var}(Z)=1$ — par intégration par parties

Puisque $E(Z)=0$, $\operatorname{Var}(Z)=E(Z^2)$. Tout repose sur une remarque : la densité
gaussienne est sa propre dérivée, au facteur $-z$ près,

$$\phi'(z)=-z\,\phi(z)\qquad\Longleftrightarrow\qquad z\,\phi(z)=-\phi'(z)$$

On écrit alors $z^2\phi(z)=z\times\bigl(z\phi(z)\bigr)$ et on intègre par parties en dérivant le
premier $z$ :

$$E(Z^2)=\int_{-\infty}^{+\infty}z\cdot z\phi(z)\,dz
=\underbrace{\Bigl[-z\,\phi(z)\Bigr]_{-\infty}^{+\infty}}_{\textstyle =\,0}
+\int_{-\infty}^{+\infty}\phi(z)\,dz
=\boxed{\,1\,}\qquad\blacksquare$$

Le crochet s'annule parce que $z\,e^{-z^2/2}\to0$ ; l'intégrale restante vaut 1 **parce que
$\phi$ est une densité** — c'est le $\sqrt{2\pi}$ du § 6f.1 qui paie.

> 🔑 **L'identité $\phi'=-z\phi$ est le seul outil du module.** Elle donne la variance ci-dessus,
> tous les moments d'ordre pair par récurrence (exercice E6f.1), et c'est encore elle qui, au
> [§ 7.3](07-loi-normale-et-ses-transformees.md), produit l'équation différentielle
> $\varphi'=-t\varphi$. Une seule ligne de calcul différentiel, trois usages.

### Le cas général, sans nouveau calcul

Avec $X=\mu+\sigma Z$, la linéarité de l'espérance ([§ 2.3](02-esperance.md)) et la propriété
$\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X)$ ([§ 3.2](03-variance-et-moments.md)) donnent
immédiatement :

$$E(X)=\mu+\sigma\underbrace{E(Z)}_{0}=\boxed{\,\mu\,},\qquad
\operatorname{Var}(X)=\sigma^2\underbrace{\operatorname{Var}(Z)}_{1}=\boxed{\,\sigma^2\,}$$

> 🔑 **Les paramètres sont les moments — et c'est un privilège.** Pour la Poisson, $\lambda$ est
> à la fois moyenne et variance ; pour l'exponentielle, $\lambda$ n'est ni l'une ni l'autre mais
> leur inverse ; pour la binomiale, il faut deux paramètres pour deux moments **liés** ($npq$
> dépend de $np$). La normale est la seule où $(\mu,\sigma^2)$ se lisent directement, et **où l'on
> peut fixer la moyenne et la variance séparément**.

---

## 6f.3 Espérance et variance, par la fonction caractéristique

### Le résultat, et son rappel de démonstration

> **Proposition ([§ 7.3](07-loi-normale-et-ses-transformees.md)).** Pour $Z\sim\mathcal N(0,1)$,
> $$\varphi_Z(t)=e^{-t^2/2}$$

**Rappel en trois lignes.** On dérive sous l'intégrale, puis on intègre par parties avec la même
identité $z\phi(z)=-\phi'(z)$ qu'au § 6f.2 :

$$\varphi_Z'(t)=\int iz\,e^{itz}\phi(z)\,dz
=i\int e^{itz}\bigl(-\phi'(z)\bigr)dz
=i\left(0+\int it\,e^{itz}\phi(z)\,dz\right)=-t\,\varphi_Z(t)$$

Avec $\varphi_Z(0)=1$, l'équation $\varphi'=-t\varphi$ a pour unique solution $e^{-t^2/2}$. (Le
module 7 détaille chaque étape et explique pourquoi on ne peut **pas** obtenir ce résultat en
remplaçant naïvement $t$ par $it$ dans la FGM.)

### Les deux dérivations

$$\varphi_Z'(t)=-t\,e^{-t^2/2}\;\Longrightarrow\;\varphi_Z'(0)=0
\qquad\Longrightarrow\qquad E(Z)=-i\times0=\boxed{\,0\,}\;\checkmark$$

$$\varphi_Z''(t)=\left(t^2-1\right)e^{-t^2/2}\;\Longrightarrow\;\varphi_Z''(0)=-1
\qquad\Longrightarrow\qquad E(Z^2)=-(-1)=\boxed{\,1\,}\;\checkmark$$

$$\operatorname{Var}(Z)=1-0^2=1\qquad\blacksquare$$

Deux dérivations d'une exponentielle, contre une IPP et une discussion d'intégrabilité. **Ici la
voie transformée est franchement la plus courte** — l'inverse exact de ce qu'on observait sur la
Bernoulli.

### Tous les moments, par la série

Comme au [§ 6d.3](06d-loi-uniforme.md), on développe au lieu de dériver :

$$\varphi_Z(t)=e^{-t^2/2}=\sum_{k\ge0}\frac{(-1)^k\,t^{2k}}{2^k\,k!}$$

En identifiant avec $\varphi_Z(t)=\sum_m E(Z^m)\dfrac{(it)^m}{m!}$ et en notant que
$(it)^{2k}=(-1)^kt^{2k}$ :

$$\boxed{\;E(Z^{2k})=\frac{(2k)!}{2^k\,k!}=(2k-1)!!\;},\qquad E(Z^{2k+1})=0$$

Les moments impairs sont nuls **parce que la série ne contient aucune puissance impaire de $t$** —
la symétrie de la loi, lue sur sa transformée. Les premiers :

| $m$ | 1 | 2 | 3 | 4 | 6 |
|---|---|---|---|---|---|
| $E(Z^m)$ | 0 | 1 | 0 | **3** | 15 |

> 🔑 **$E(Z^4)=3$ tombe ici gratuitement**, alors que le calcul direct demanderait deux
> intégrations par parties. C'est ce nombre qui donne $\beta_2=3$ — la référence de tous les
> kurtosis du cours ([§ 3.4](03-variance-et-moments.md)) — et
> $\operatorname{Var}\bigl(\chi^2(k)\bigr)=2k$ au [module 15](15-loi-du-chi2.md).

### Le cas général et les cumulants

Par la propriété affine, $\varphi_X(t)=e^{i\mu t}\varphi_Z(\sigma t)$, soit

$$\varphi_X(t)=\exp\!\left(i\mu t-\frac{\sigma^2t^2}{2}\right)
\qquad\Longrightarrow\qquad
K_X(t)=\log\varphi_X(t)=i\mu t-\frac{\sigma^2t^2}{2}$$

**Le logarithme est un polynôme de degré 2.** Donc, dans le développement
$K_X(t)=\sum_j\kappa_j(it)^j/j!$ :

$$\kappa_1=\mu,\qquad \kappa_2=\sigma^2,\qquad \kappa_j=0\ \text{ pour tout } j\ge3$$

C'est la caractérisation annoncée au [§ 6.4](06-fonction-caracteristique.md) : **la gaussienne est
l'unique loi dont tous les cumulants d'ordre $\ge3$ sont nuls.** Comparez avec la Poisson, où
*tous* valaient $\lambda$ : deux lois, deux signatures, même outil.

---

## 6f.4 Les propriétés à connaître

| Propriété | Énoncé | Démonstration |
|---|---|---|
| **Affine** | $aX+b\sim\mathcal N(a\mu+b,\,a^2\sigma^2)$ | $\varphi$ affine |
| **Stabilité** ⭐ | $\mathcal N(\mu_1,\sigma_1^2)+\mathcal N(\mu_2,\sigma_2^2)=\mathcal N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$ | [Module 8](08-addition-de-lois-et-stabilite-gaussienne.md) |
| **Moyenne** ⭐ | $\bar X\sim\mathcal N\!\left(\mu,\sigma^2/n\right)$, **exactement** | Corollaire de la stabilité |
| **Universalité** | Limite de toute somme normalisée de variance finie | [Module 12](12-theoreme-central-limite.md) |
| **Décorrélation = indépendance** | Vrai **dans un vecteur gaussien** seulement | [Module 10](10-decorrelation-et-independance.md) |

**Les quantiles à connaître par cœur** — ce sont eux qui apparaissent dans tout calcul de risque :

| $p$ | 1 % | 2,5 % | 5 % | 95 % | 97,5 % | 99 % |
|---|---|---|---|---|---|---|
| $z_p$ | $-2{,}326$ | $-1{,}960$ | $-1{,}645$ | $1{,}645$ | $1{,}960$ | $2{,}326$ |

d'où la règle des **68 – 95 – 99,7 %** pour $\mu\pm\sigma$, $\mu\pm2\sigma$, $\mu\pm3\sigma$.

⚠️ **La stabilité vaut pour des variables indépendantes — ou, plus finement, pour un couple
gaussien.** Deux marges gaussiennes dépendantes peuvent donner une somme non gaussienne : c'est
tout l'objet du [module 9](09-vecteur-gaussien.md), et la faute la plus coûteuse de la gestion de
portefeuille.

---

## 6f.5 Exemple complet — la VaR à 99 % d'une position de 1 M€

**Les données.** Une position de $V=1$ M€ sur une action du SBF 250. Sur les 252 derniers
rendements quotidiens : $\hat\mu=0{,}04\,\%$ par jour, $\hat\sigma=1{,}40\,\%$ par jour.

**① Le modèle.** $r\sim\mathcal N(\mu,\sigma^2)$, rendements quotidiens i.i.d. La **VaR à 99 % à
1 jour** est la perte dépassée une fois sur cent :

$$P\bigl(r<-\text{VaR}\bigr)=1\,\%
\qquad\Longleftrightarrow\qquad
-\text{VaR}=\mu+\sigma\,z_{1\%}$$

C'est exactement l'usage de $X=\mu+\sigma Z$ : **on lit un quantile de la loi standard, on le
renvoie à l'échelle des données.**

**② Le calcul.**

$$\text{VaR}_{99\%}=-\left(0{,}0004+0{,}0140\times(-2{,}326)\right)
=-\left(0{,}0004-0{,}03257\right)=0{,}0322$$

$$\boxed{\text{VaR}_{99\%}=3{,}22\,\%\ \text{du nominal}=32\,200\ \text{€}}$$

Notez la structure : le terme de dérive ($0{,}04\,\%$) est **négligeable** devant le terme de
risque ($3{,}26\,\%$). À l'horizon d'un jour, $\mu$ ne compte pas — et le point ③ dit pourquoi.

**③ Le passage à 10 jours — la racine carrée, et sa justification.** Le régulateur demande la VaR
à 10 jours. La somme $r_1+\dots+r_{10}$ de rendements **indépendants et gaussiens** est gaussienne
(stabilité, § 6f.4) :

$$r_{1:10}\sim\mathcal N\!\left(10\mu,\;10\sigma^2\right)
\qquad\Longrightarrow\qquad
\text{VaR}_{10j}=-\left(10\mu+\sqrt{10}\,\sigma z_{1\%}\right)
=9{,}90\,\%=99\,000\ \text{€}$$

> 🔑 **L'espérance s'ajoute en $n$, l'écart-type en $\sqrt n$.** C'est toute la « règle de la
> racine du temps » : $10\times0{,}04\,\% = 0{,}40\,\%$ de dérive contre
> $\sqrt{10}\times1{,}40\,\% = 4{,}43\,\%$ de risque. **Plus l'horizon s'allonge, plus la dérive
> pèse** — elle finit par rattraper le risque, à un horizon de l'ordre de
> $(\sigma/\mu)^2\approx1\,200$ jours. C'est la même arithmétique $n$ contre $\sqrt n$ qu'au
> [§ 3.3](03-variance-et-moments.md), appliquée dans l'autre sens.

⚠️ La racine carrée **suppose l'indépendance des rendements successifs** — hypothèse qu'on vient
de voir prise en défaut au [§ 6d.5](06d-loi-uniforme.md) (bruit d'arrondi) et au
[module 14](14-dependance-et-echec-du-tcl.md) (regroupement de volatilité).

**④ Le test qui met le modèle en difficulté.** Que dit la normale d'une chute de 5 % en un jour ?

$$P(r<-5\,\%)=\Phi\!\left(\frac{-0{,}05-0{,}0004}{0{,}014}\right)=\Phi(-3{,}60)
=1{,}6\times10^{-4}$$

Soit **une séance sur 6 285**, c'est-à-dire une fois tous les **25 ans**. Or, sur à peu près
n'importe quelle action du SBF 250, on compte plusieurs chutes de 5 % par décennie — et le
[§ 6c.5](06c-loi-de-poisson.md) en dénombrait 21 au-delà de 4 % en 5 ans.

> ⚠️ **La normale ne se trompe pas au centre, elle se trompe dans la queue — là où on l'utilise.**
> Le kurtosis empirique des rendements quotidiens vaut couramment 6 à 10, contre **3** pour la
> gaussienne (§ 6f.3). Ce n'est pas un détail de forme : c'est un facteur 10 à 50 sur la
> probabilité des pertes extrêmes.

**⑤ Le contrôle formel : compter les dépassements.** La procédure standard des régulateurs
combine trois modules. Sur $n=250$ jours, chaque dépassement de la VaR à 99 % est une **Bernoulli**
de paramètre $p=1\,\%$ ([§ 6a.1](06a-loi-de-bernoulli.md)) ; leur nombre suit une **binomiale**
$\mathcal B(250\,;0{,}01)$ ([§ 6b.1](06b-loi-binomiale.md)), d'espérance $2{,}5$ et d'écart-type
$\sqrt{250\times0{,}01\times0{,}99}=1{,}57$ ; et l'uniformité des $u_t=F_t(r_t)$ est le test de
PIT du [§ 6d.4](06d-loi-uniforme.md).

Observer **8 dépassements** au lieu de 2,5 donne $z=(8-2{,}5)/1{,}57=3{,}5$ : le modèle est
rejeté. C'est ainsi que le modèle gaussien est réfuté en pratique — non par un argument
théorique, mais par un comptage de Bernoulli.

**⑥ Ce qu'on garde, ce qu'on jette.**

| Usage | Verdict |
|---|---|
| $E(\bar X)=\mu$, $\operatorname{Var}(\bar X)=\sigma^2/n$ | ✅ Robuste — ne dépend pas de la normalité |
| Intervalle de confiance sur $\mu$ | ✅ Justifié par le TCL, pas par la normalité des données |
| VaR à 99 %, pertes extrêmes | ❌ Sous-estimation systématique |
| Échelle en $\sqrt{n}$ | ⚠️ Valable si et seulement si les rendements sont décorrélés |

> 🔑 **La leçon des six modules.** Chaque loi vient avec une **signature testable** : $pq\le1/4$
> pour la Bernoulli, $E=\operatorname{Var}$ pour la Poisson, $\text{CV}=1$ pour l'exponentielle,
> $\beta_2=3$ pour la normale. Ajuster un modèle, c'est estimer deux paramètres ; **le valider,
> c'est vérifier sa signature** — et c'est la seule partie du travail qui protège.

---

## 6f.6 Simulation

### S6f.1 — Moments, quantiles, racine du temps, et l'échec en queue

```python
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(6)
mu, sg, N = 0.0004, 0.014, 2_000_000
X = rng.normal(mu, sg, N)

print(f"E(X)   = {X.mean():.6f}   theorie mu       = {mu}")
print(f"Var(X) = {X.var():.3e}   theorie sigma^2  = {sg**2:.3e}")

Z = (X - mu) / sg
for m in (1, 2, 3, 4, 6):
    print(f"E(Z^{m}) = {(Z**m).mean():7.4f}   theorie = "
          f"{0 if m % 2 else np.prod(np.arange(m-1, 0, -2)):7.4f}")

for t in (0.5, 2.0):
    print(f"t={t}: phi_Z empirique = {np.mean(np.exp(1j*t*Z)):+.4f}"
          f"   theorie e^(-t^2/2) = {np.exp(-t**2/2):+.4f}")

# la VaR du § 6f.5, et sa verification par comptage
VaR = -(mu + sg * norm.ppf(0.01))
print(f"\nVaR 99% = {VaR:.4%}   depassements observes = {(X < -VaR).mean():.4%} (cible 1%)")

# la racine du temps : somme de 10 rendements
S10 = rng.normal(mu, sg, (N // 10, 10)).sum(axis=1)
print(f"sd(10 jours) = {S10.std():.4%}   theorie sqrt(10)*sigma = {np.sqrt(10)*sg:.4%}")

# ce que la normale rate : queues epaisses a variance IDENTIQUE
t5 = rng.standard_t(5, N)
t5 = mu + sg * t5 / t5.std()                    # meme moyenne, meme ecart-type
print(f"\nP(r < -5%) gaussien  = {(X  < -0.05).mean():.2e}   (theorie {norm.cdf(-3.6):.2e})")
print(f"P(r < -5%) Student 5 = {(t5 < -0.05).mean():.2e}   <- meme sigma, autre queue")
print(f"depassements de la VaR 99% sous Student : {(t5 < -VaR).mean():.4%}")
```

Le dernier bloc est le plus important : **à moyenne et écart-type rigoureusement identiques**, la
probabilité d'une chute de 5 % passe de $1{,}6\times10^{-4}$ à $2{,}8\times10^{-3}$ — près de
**vingt fois** plus, et les dépassements de la VaR à 99 % passent de 1,0 % à 1,5 % des séances.
La variance ne dit rien des queues —
c'est le [§ 3.4](03-variance-et-moments.md), vu là où il coûte de l'argent.

---

## 6f.7 Exercices

**E6f.1.** Démontrer par récurrence, à partir de $\phi'=-z\phi$ et d'une IPP, que
$E(Z^{m})=(m-1)\,E(Z^{m-2})$. *En déduire $E(Z^4)=3$ et $E(Z^6)=15$, et comparer à la méthode par
la série du § 6f.3 : laquelle préférez-vous, et pourquoi ?*

**E6f.2.** Retrouver $\varphi_X(t)=e^{i\mu t-\sigma^2t^2/2}$ à partir de $\varphi_Z$ et de la
propriété affine, puis en déduire $E(X)$ et $\operatorname{Var}(X)$ par dérivation. *Vérifier que
$|\varphi_X(t)|\le1$, conformément au § 6.1.*

**E6f.3.** Montrer que $K_X$ est un polynôme de degré 2 **si et seulement si** tous les cumulants
d'ordre $\ge3$ sont nuls. *Quelle propriété du module 12 cette caractérisation permet-elle de
formuler en une phrase ?*

**E6f.4.** Recalculer la VaR du § 6f.5 avec $\hat\sigma=1{,}40\,\%$ mais un kurtosis de 9, en
utilisant une loi de Student à 5 degrés de liberté renormalisée (dont$\beta_2=3+6/(\nu-4)=9$). *De
combien la VaR gaussienne
sous-estime-t-elle la perte au seuil 99 % ? au seuil 99,9 % ?*

**E6f.5.** Sur $n=250$ jours, un modèle de VaR à 99 % produit 8 dépassements. *Calculer la
$p$-valeur exacte avec la loi binomiale du [§ 6b.5](06b-loi-binomiale.md), puis avec
l'approximation normale et sa correction de continuité. Le modèle est-il rejeté à 5 % ?*

---

## 6f.8 À retenir

- **$E(X)=\mu$ et $\operatorname{Var}(X)=\sigma^2$** : la normale est la seule loi du chapitre où
  les paramètres **sont** les deux premiers moments, réglables séparément.
- **Tout passe par $X=\mu+\sigma Z$** : une seule loi à connaître, la standard.
- **L'identité $\phi'(z)=-z\phi(z)$** donne la variance par IPP, tous les moments pairs par
  récurrence, et l'équation $\varphi'=-t\varphi$ du module 7.
- **$\varphi_X(t)=e^{i\mu t-\sigma^2t^2/2}$**, dont le développement livre
  $E(Z^{2k})=(2k-1)!!$ — en particulier **$E(Z^4)=3$**, la référence de tous les kurtosis.
- **$K_X$ est un polynôme de degré 2** : cumulants d'ordre $\ge3$ **nuls**, caractérisation qui
  donnera au module 12 sa lecture la plus courte.
- ⚠️ **Sur des rendements financiers, la normale est correcte au centre et fausse dans la
  queue** — kurtosis observé 6 à 10 contre 3. Elle sous-estime précisément ce que la VaR
  prétend mesurer.

---

⬅️ [Module 6e — La loi exponentielle](06e-loi-exponentielle.md) ·
➡️ [Module 7 — La loi normale et ses transformées](07-loi-normale-et-ses-transformees.md) ·
🏠 [Sommaire](README.md)
