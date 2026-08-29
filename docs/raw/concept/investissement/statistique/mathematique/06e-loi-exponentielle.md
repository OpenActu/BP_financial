# Module 6e — La loi exponentielle

**Durée : 1 h.** Prérequis : [module 6d](06d-loi-uniforme.md), et le
[module 6c](06c-loi-de-poisson.md) pour le § 6e.4.

> **La question traitée.** La Poisson compte les événements ; l'exponentielle mesure **le temps
> qui les sépare**. Ce sont les deux faces exactes du même modèle, et le § 6e.4 le démontre en
> deux lignes.

**Ce qui est en jeu.** L'exponentielle possède une propriété qu'aucune autre loi continue ne
possède : elle est **sans mémoire**. Cette propriété est à la fois son principal usage — elle
formalise « le passé ne dit rien de l'avenir » — et le moyen le plus simple de la réfuter sur des
données de marché.

---

## 6e.1 Définition

> **Définition.** $T$ suit une **loi exponentielle** de paramètre $\lambda>0$, notée
> $T\sim\mathcal E(\lambda)$, si elle admet la densité
> $$f(x)=\lambda e^{-\lambda x}\ \ \text{pour }x\ge0,\qquad f(x)=0\ \text{pour }x<0$$

Sa fonction de répartition, et surtout sa **fonction de survie**, s'obtiennent d'une primitive :

$$F(x)=1-e^{-\lambda x},\qquad
\boxed{\;P(T>x)=e^{-\lambda x}\;}\qquad(x\ge0)$$

> 🔑 **C'est la fonction de survie qu'il faut retenir, pas la densité.** $P(T>x)=e^{-\lambda x}$
> se lit directement — « la probabilité d'attendre encore décroît géométriquement » — et c'est
> elle qui donne les trois quarts des résultats du module, y compris l'espérance (§ 6e.2).

**L'unité de $\lambda$.** C'est un **taux** : $\lambda$ événements par unité de temps. Son inverse
$1/\lambda$ est une **durée** — l'attente moyenne, comme le § 6e.2 va l'établir. Confondre les
deux est l'erreur la plus fréquente sur cette loi.

---

## 6e.2 Espérance et variance, sans transformée

### Chemin ① — par intégration par parties

**Espérance.** On intègre par parties en dérivant $x$ et en primitivant $\lambda e^{-\lambda x}$ :

$$E(T)=\int_0^{\infty}x\,\lambda e^{-\lambda x}\,dx
=\underbrace{\Bigl[-x\,e^{-\lambda x}\Bigr]_0^{\infty}}_{\textstyle =\,0}
+\int_0^{\infty}e^{-\lambda x}\,dx
=\left[-\frac{e^{-\lambda x}}{\lambda}\right]_0^{\infty}
=\boxed{\;\frac1\lambda\;}$$

Le crochet s'annule parce que l'exponentielle l'emporte sur le polynôme : $xe^{-\lambda x}\to0$.

**Moment d'ordre 2.** Même manœuvre, en réutilisant le résultat précédent :

$$E(T^2)=\int_0^{\infty}x^2\lambda e^{-\lambda x}dx
=\underbrace{\Bigl[-x^2e^{-\lambda x}\Bigr]_0^{\infty}}_{=\,0}
+\frac{2}{\lambda}\underbrace{\int_0^{\infty}x\,\lambda e^{-\lambda x}dx}_{\textstyle =\,E(T)\,=\,1/\lambda}
=\frac{2}{\lambda^2}$$

**Variance.**

$$\operatorname{Var}(T)=\frac{2}{\lambda^2}-\frac{1}{\lambda^2}
=\boxed{\;\frac{1}{\lambda^2}\;}\qquad\blacksquare$$

### Chemin ② — par la fonction de survie, sans aucune IPP

Pour toute variable **positive**, l'espérance est l'aire sous la courbe de survie :

$$E(T)=\int_0^\infty P(T>x)\,dx$$

*(Démonstration : $T=\int_0^\infty\mathbf 1_{\{T>x\}}dx$ ; on prend l'espérance et on échange
avec l'intégrale, tout étant positif — c'est Tonelli. Le pont
$E(\mathbf 1_A)=P(A)$ est celui du [§ 6a.1](06a-loi-de-bernoulli.md).)*

Ici, aucune IPP n'est nécessaire :

$$E(T)=\int_0^\infty e^{-\lambda x}dx=\frac1\lambda\;\checkmark$$

> 🔑 **$\sigma(T)=1/\lambda=E(T)$ : l'écart-type égale la moyenne.** Le coefficient de variation
> vaut exactement **1**. C'est la signature de l'exponentielle, l'analogue du
> $E=\operatorname{Var}=\lambda$ de la Poisson — et, comme lui, un test de modèle en deux calculs
> (§ 6e.5).

**Les moments de forme.** $\gamma_1=2$ et $\beta_2=9$ (excès $+6$) : une loi **fortement
asymétrique à droite**, sans aucune valeur négative et à queue lourde. C'est la ligne
« exponentielle » du [§ 13.2](13-portee-et-limites-du-tcl.md), où le TCL est notablement lent.

Conséquence pratique immédiate — **la médiane est bien inférieure à la moyenne** :

$$F(m)=\tfrac12\iff m=\frac{\log 2}{\lambda}=\frac{0{,}693}{\lambda}<\frac1\lambda$$

Une attente « typique » est **30 % plus courte** que l'attente moyenne.

---

## 6e.3 Espérance et variance, par la fonction caractéristique

### La fonction caractéristique

L'intégrale est celle d'une exponentielle complexe, et elle converge parce que la partie réelle
de l'exposant reste $-\lambda<0$ :

$$\varphi_T(t)=\int_0^{\infty}e^{itx}\lambda e^{-\lambda x}dx
=\lambda\int_0^{\infty}e^{-(\lambda-it)x}dx
=\lambda\left[\frac{-e^{-(\lambda-it)x}}{\lambda-it}\right]_0^{\infty}
=\boxed{\;\frac{\lambda}{\lambda-it}\;}$$

⚠️ **Comparez avec la FGM** ([§ 5.5](05-fonction-generatrice-des-moments.md)) :
$M_T(t)=\lambda/(\lambda-t)$, qui n'existe **que pour $t<\lambda$** et explose en $t=\lambda$. La
f.c., elle, est définie partout : $|\lambda-it|=\sqrt{\lambda^2+t^2}\ge\lambda>0$, donc
$|\varphi_T(t)|\le1$. La différence entre les deux outils est ici visible sur une seule formule.

### Les deux dérivations

Avec $\varphi_T(t)=\lambda(\lambda-it)^{-1}$ :

$$\varphi_T'(t)=\lambda\,i\,(\lambda-it)^{-2}
\;\Longrightarrow\;\varphi_T'(0)=\frac{i\lambda}{\lambda^2}=\frac{i}{\lambda}
\;\Longrightarrow\;E(T)=-i\times\frac{i}{\lambda}=\boxed{\;\frac1\lambda\;}\;\checkmark$$

$$\varphi_T''(t)=\lambda i\times 2i\,(\lambda-it)^{-3}=-2\lambda(\lambda-it)^{-3}
\;\Longrightarrow\;\varphi_T''(0)=-\frac{2\lambda}{\lambda^3}=-\frac{2}{\lambda^2}$$

$$E(T^2)=-\varphi_T''(0)=\frac{2}{\lambda^2}
\qquad\Longrightarrow\qquad
\operatorname{Var}(T)=\frac{1}{\lambda^2}\;\checkmark\qquad\blacksquare$$

### Le raccourci : la série géométrique

Comme au [§ 6d.3](06d-loi-uniforme.md), développer vaut mieux que dériver. Pour $|t|<\lambda$ :

$$\varphi_T(t)=\frac{1}{1-\dfrac{it}{\lambda}}=\sum_{m\ge0}\left(\frac{it}{\lambda}\right)^{m}
=\sum_{m\ge0}\frac{m!}{\lambda^m}\cdot\frac{(it)^m}{m!}
\qquad\Longrightarrow\qquad
\boxed{\;E(T^m)=\frac{m!}{\lambda^m}\;}$$

**Tous les moments d'un coup**, par identification des séries : $E(T)=1/\lambda$,
$E(T^2)=2/\lambda^2$, $E(T^3)=6/\lambda^3$, $E(T^4)=24/\lambda^4$ — de quoi obtenir $\gamma_1=2$
et $\beta_2=9$ sans une seule intégrale (exercice E6e.2).

| | Sans transformée | Par $\varphi_T$ |
|---|---|---|
| Espérance | Une IPP (ou la survie) | Une dérivation |
| Moment d'ordre $m$ | $m$ intégrations par parties | ⭐ **Gratuit** : $m!/\lambda^m$ |
| Loi de la somme de $n$ | Convolutions | ⭐ $(\lambda/(\lambda-it))^n$ : une Gamma |

---

## 6e.4 Les trois propriétés qui font l'exponentielle

### ① L'absence de mémoire — et son unicité

> **Propriété.** Pour tous $s,t\ge0$ :
> $$P(T>s+t\mid T>s)=P(T>t)$$

**Démonstration.** Par définition de la probabilité conditionnelle, et parce que
$\{T>s+t\}\subset\{T>s\}$ :

$$P(T>s+t\mid T>s)=\frac{P(T>s+t)}{P(T>s)}
=\frac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}=P(T>t)\qquad\blacksquare$$

> 🔑 **« Avoir déjà attendu » n'apporte aucune information.** Une exponentielle ne vieillit pas :
> après 8 mois sans incident, la loi du temps restant est **identique** à celle du premier jour.
> C'est la formalisation exacte de l'absence d'effet mémoire — et le § 6e.5 en tire la réfutation
> de l'erreur du joueur.

⚠️ **Réciproque vraie, et c'est rare.** L'exponentielle est **la seule** loi continue sans
mémoire (la géométrique est son analogue discret). Modéliser une attente par une exponentielle,
c'est donc **affirmer** l'absence de mémoire, pas seulement choisir une forme commode.

### ② Le lien exact avec la Poisson

> **Théorème.** Si les événements arrivent selon un processus de Poisson d'intensité $\lambda$ —
> c'est-à-dire si le nombre $N(t)$ d'événements sur $[0,t]$ suit $\mathcal P(\lambda t)$ — alors
> le temps d'attente $T$ du premier événement suit $\mathcal E(\lambda)$.

**Démonstration** — une ligne, et elle relie les deux modules :

$$P(T>t)=P\bigl(\text{aucun événement sur }[0,t]\bigr)=P\bigl(N(t)=0\bigr)
=e^{-\lambda t}\frac{(\lambda t)^0}{0!}=e^{-\lambda t}\qquad\blacksquare$$

C'est exactement la fonction de survie d'une $\mathcal E(\lambda)$. **Compter et attendre sont le
même modèle**, vu de deux côtés :

| | [Module 6c](06c-loi-de-poisson.md) | Module 6e |
|---|---|---|
| Objet | $N$ = nombre d'événements par an | $T$ = temps entre deux événements |
| Loi | $\mathcal P(\lambda)$ | $\mathcal E(\lambda)$ |
| Signature | $E=\operatorname{Var}=\lambda$ | $\sigma=E=1/\lambda$ |
| Ce que le rejet signifie | Regroupement temporel | Attentes **à mémoire** |

### ③ Somme et minimum

| Opération | Résultat | Démonstration |
|---|---|---|
| **Somme** de $n$ i.i.d. | $\Gamma(n,\lambda)$ — **pas** exponentielle | $\varphi^n=\bigl(\lambda/(\lambda-it)\bigr)^n$ |
| **Minimum** de $n$ indép. | $\mathcal E(\lambda_1+\dots+\lambda_n)$ | $P(\min>t)=\prod_i e^{-\lambda_i t}$ |

⚠️ **L'exponentielle n'est pas stable par addition** — c'est le contre-exemple du
[§ 8.3](08-addition-de-lois-et-stabilite-gaussienne.md), déjà rencontré en simulation au
[§ 5.6](05-fonction-generatrice-des-moments.md) sous la forme $1/(1-2t)^2$. Le **minimum**, lui,
reste exponentiel : le premier de plusieurs risques indépendants à se réaliser suit encore une
exponentielle, de taux la **somme** des taux.

---

## 6e.5 Exemple complet — combien de temps avant la prochaine secousse ?

On reprend les données du [§ 6c.5](06c-loi-de-poisson.md) : une action connaît en moyenne
$\lambda=4{,}2$ séances de variation $\ge4\,\%$ par an.

**① Le modèle.** Par le § 6e.4, si le comptage annuel est $\mathcal P(4{,}2)$, alors le temps
$T$ (en années) entre deux secousses suit $\mathcal E(4{,}2)$. **Aucun paramètre nouveau à
estimer** : c'est le même $\lambda$.

**② Les trois nombres qui répondent aux questions du gérant.**

$$E(T)=\frac{1}{4{,}2}=0{,}238\ \text{an}=\boxed{2{,}9\ \text{mois}}
\qquad\text{attente moyenne}$$

$$m=\frac{\log2}{4{,}2}=0{,}165\ \text{an}=2{,}0\ \text{mois}
\qquad\text{attente médiane — 30 \% de moins}$$

$$\sigma(T)=\frac{1}{4{,}2}=2{,}9\ \text{mois}
\qquad\text{écart-type = moyenne, coefficient de variation }=1$$

> ⚠️ **La moyenne est un mauvais résumé ici.** Avec $\gamma_1=2$ et $\sigma=E$, l'attente typique
> (2,0 mois) et l'attente moyenne (2,9 mois) diffèrent de 45 %. Annoncer « une secousse tous les
> 2,9 mois en moyenne » laisse croire à une régularité qui n'existe pas.

**③ Les probabilités utiles.**

| Question | Calcul | Réponse |
|---|---|---|
| Rien pendant 6 mois ? | $e^{-4{,}2\times0{,}5}$ | $12{,}2\,\%$ |
| Rien de toute l'année ? | $e^{-4{,}2}$ | $1{,}5\,\%$ |
| Au moins une dans le mois ? | $1-e^{-4{,}2/12}$ | $29{,}5\,\%$ |

**Le contrôle de cohérence.** $P(T>1\ \text{an})=e^{-4{,}2}=1{,}5\,\%$ est **exactement**
$P(N=0)=0{,}015$ calculé au § 6c.5 par la loi de Poisson. Deux modules, deux formules, un seul
nombre : c'est le théorème du § 6e.4 vérifié sur les données.

**④ L'usage décisif : tuer l'erreur du joueur.** Le gérant observe que **rien ne s'est passé
depuis 8 mois** et demande : *« une secousse est-elle imminente ? »* Réponse par l'absence de
mémoire :

$$P\bigl(T>8+6\ \text{mois}\;\bigm|\;T>8\ \text{mois}\bigr)=P(T>6\ \text{mois})=12{,}2\,\%$$

**Strictement la même probabilité qu'au premier jour.** L'attente écoulée ne rend pas
l'événement « dû ». Toute stratégie fondée sur « ça fait longtemps, donc ça va arriver » suppose
une loi qui n'est **pas** exponentielle — et il faut alors le dire et le démontrer, pas
l'espérer.

**⑤ Le test du modèle, et son échec.** Comme pour la Poisson, la signature se vérifie. Sur les
20 intervalles observés entre les 21 secousses :

$$\text{coefficient de variation}=\frac{\hat\sigma(T)}{\hat E(T)}
\quad\text{doit valoir}\quad 1$$

Sur ces données, il vaut **environ 2** : les attentes sont **beaucoup plus dispersées** que ne
l'autorise l'exponentielle — de très longues périodes calmes, puis des rafales très rapprochées.

> 🔑 **C'est le même rejet qu'au § 6c.5, lu dans l'autre sens.** Surdispersion des comptages
> $\iff$ coefficient de variation $>1$ des attentes $\iff$ **les secousses ont de la mémoire**.
> Le modèle exponentiel ne se contente pas d'être imprécis : il affirme exactement ce que les
> données démentent. Le [module 14](14-dependance-et-echec-du-tcl.md) explique pourquoi cet échec
> est la règle sur les séries financières.

**⑥ Ce qui reste utilisable.** L'espérance $1/\lambda$ est robuste : sur 5 ans, « environ une
secousse tous les 2,9 mois en moyenne » reste vrai. Ce sont les **probabilités de queue**
($P(T>6\text{ mois})$) et l'absence de mémoire qui sont fausses — c'est-à-dire précisément ce
dont on avait besoin.

---

## 6e.6 Simulation

### S6e.1 — Moments, absence de mémoire, dualité Poisson, et la réfutation

```python
import numpy as np

rng = np.random.default_rng(6)
lam, N = 4.2, 1_000_000
T = rng.exponential(1/lam, N)              # attention : numpy parametre par l'echelle 1/lambda

print(f"E(T)   = {T.mean():.4f}   theorie 1/lambda   = {1/lam:.4f}")
print(f"sd(T)  = {T.std():.4f}   theorie 1/lambda   = {1/lam:.4f}   (CV = 1)")
print(f"E(T^3) = {(T**3).mean():.4f}   theorie 6/lambda^3 = {6/lam**3:.4f}")
print(f"mediane = {np.median(T):.4f}   theorie log2/lambda = {np.log(2)/lam:.4f}")

for t in (0.5, 2.0):
    emp, the = np.mean(np.exp(1j*t*T)), lam/(lam - 1j*t)
    print(f"t={t}: phi empirique = {emp:+.4f}   theorie lambda/(lambda-it) = {the:+.4f}")

# absence de memoire : la loi du reste ne depend pas de l'attente deja ecoulee
s = 8/12
reste = T[T > s] - s
print(f"\nP(T>0.5)        = {(T > 0.5).mean():.4f}")
print(f"P(T>s+0.5|T>s)  = {(reste > 0.5).mean():.4f}   <- identiques")

# dualite avec la Poisson : compter les evenements d'une annee construite par attentes
cum = np.cumsum(rng.exponential(1/lam, (20_000, 30)), axis=1)
N_an = (cum <= 1.0).sum(axis=1)
print(f"\ncomptage annuel : E = {N_an.mean():.3f}   Var = {N_an.var():.3f}   theorie lambda = {lam}")

# et la refutation : des attentes groupees (melange calme / rafale)
rafale = rng.random(N) < 0.60                      # meme moyenne 0.238 an, mais deux regimes
T2 = np.where(rafale, rng.exponential(0.01, N), rng.exponential(0.58, N))
print(f"\nattentes groupees : E = {T2.mean():.3f}   CV = {T2.std()/T2.mean():.2f}"
      f"   (exponentielle : CV = 1,00)")
```

Le bloc « absence de mémoire » est le cœur : les deux probabilités coïncident à la troisième
décimale. Le dernier bloc montre à quoi ressemble un jeu d'attentes **avec** mémoire — même
moyenne, coefficient de variation deux fois trop grand, exactement comme les données du § 6e.5.

---

## 6e.7 Exercices

**E6e.1.** Démontrer $E(T)=\int_0^\infty P(T>x)\,dx$ pour une variable positive quelconque, puis
l'appliquer à l'exponentielle **et** à une loi de Pareto de survie $P(T>x)=x^{-\alpha}$
($x\ge1$). *Pour quels $\alpha$ l'espérance existe-t-elle ?*

**E6e.2.** À partir de $E(T^m)=m!/\lambda^m$, calculer $\gamma_1$ et $\beta_2$. *Vérifier
$\gamma_1=2$, valeur utilisée au [§ 13.2](13-portee-et-limites-du-tcl.md), et constater qu'elles
ne dépendent pas de $\lambda$ — pourquoi était-ce prévisible ?*

**E6e.3.** Montrer que si $T_1,\dots,T_n$ sont indépendantes de taux $\lambda_i$, alors
$\min_i T_i\sim\mathcal E\bigl(\sum_i\lambda_i\bigr)$. *Application : trois systèmes de
couverture tombent en panne au taux 0,5, 0,3 et 0,2 par an ; quelle est l'attente moyenne avant
la première panne ?*

**E6e.4.** Calculer $\varphi$ de la somme de $n$ exponentielles i.i.d., puis $E$ et
$\operatorname{Var}$ de cette somme **sans** connaître la densité de la loi Gamma. *Comparer à la
simulation S5.1, où $1/(1-2t)^2$ apparaissait déjà.*

**E6e.5.** Une loi de Weibull a pour survie $P(T>x)=e^{-(\lambda x)^{k}}$. *Montrer qu'elle est
sans mémoire si et seulement si $k=1$. Pour $k>1$, le risque instantané augmente-t-il ou
diminue-t-il avec l'attente écoulée ? Laquelle des deux formes modéliserait le clustering du
§ 6e.5 ?*

---

## 6e.8 À retenir

- **$E(T)=1/\lambda$, $\operatorname{Var}(T)=1/\lambda^2$** : l'écart-type **égale** la moyenne,
  coefficient de variation 1 — signature testable.
- **$\varphi_T(t)=\dfrac{\lambda}{\lambda-it}$**, définie partout, alors que la FGM
  $\lambda/(\lambda-t)$ explose en $t=\lambda$. Son développement géométrique donne
  $E(T^m)=m!/\lambda^m$ d'un coup.
- ⭐ **Absence de mémoire** : $P(T>s+t\mid T>s)=P(T>t)$, et l'exponentielle est **la seule** loi
  continue à la vérifier. La choisir, c'est l'affirmer.
- ⭐ **Dualité Poisson–exponentielle** : compter avec $\mathcal P(\lambda)$ ou attendre avec
  $\mathcal E(\lambda)$, c'est le même modèle — $P(T>t)=P(N(t)=0)=e^{-\lambda t}$.
- **Somme non stable** (Gamma), **minimum stable** ($\mathcal E$ de taux la somme des taux).
- ⚠️ **Médiane $=0{,}693/\lambda<$ moyenne** ($\gamma_1=2$) : sur cette loi, « en moyenne » induit
  systématiquement en erreur.

---

⬅️ [Module 6d — La loi uniforme](06d-loi-uniforme.md) ·
➡️ [Module 6f — La loi normale](06f-loi-normale.md) ·
🏠 [Sommaire](README.md)
