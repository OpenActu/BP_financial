# Module 11 bis — La convergence en loi

**Durée : 1 h 30.** Prérequis : modules [1](01-variable-aleatoire-et-loi.md) (fonction de répartition), [3](03-variance-et-moments.md) (asymétrie), [6](06-fonction-caracteristique.md)
(fonction caractéristique et théorème de Lévy), et le catalogue [6b](06b-loi-binomiale.md)–[6c](06c-loi-de-poisson.md)–[6f](06f-loi-normale.md).

> **La question traitée.** La notation $\xrightarrow{\mathcal L}$ circule depuis le  [§ 6.3](06-fonction-caracteristique.md) sans avoir jamais été définie. Que signifie-t-elle exactement, quelles convergences relient les lois du catalogue entre elles — et surtout : que **garantit** une convergence en loi, que ne garantit-elle pas ?

**Ce qui est en jeu.** Toutes les approximations que la pratique utilise sans y penser —
« binomiale $\approx$ Poisson quand $p$ est petit », « Poisson $\approx$ normale quand $\lambda$ est grand », « tirage sans remise $\approx$ avec remise » — sont **une seule et même affirmation mathématique**, et elles se démontrent toutes par le même geste en cinq lignes. Ce module installe le cadre, puis le fait tourner. Le [module 12](12-theoreme-central-limite.md) en sera alors un énoncé parmi d'autres — le plus profond, mais un parmi d'autres.

> ℹ️ **Pourquoi « 11 bis ».** Ce module ne dépend pas du module 11 : le suffixe marque seulement
> son insertion **avant** le TCL, dont il est le préalable de vocabulaire.

---

## 11bis.1 Trois affirmations qui ont besoin d'un même cadre

| Affirmation courante                                             | Ce qu'elle dit vraiment                                                                 |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| « 1 000 tirages à $p=0{,}005$ : je peux prendre une Poisson(5) » | La loi de $\mathcal B(1000;0{,}005)$ est **proche** de celle de $\mathcal P(5)$         |
| « $\lambda=100$ : je peux prendre une normale »                  | La loi de $\dfrac{X_\lambda-\lambda}{\sqrt\lambda}$ est **proche** de $\mathcal N(0,1)$ |
| « $n=200$ : ma moyenne est à peu près gaussienne »               | La loi de $\dfrac{\bar X_n-\mu}{\sigma/\sqrt n}$ est **proche** de $\mathcal N(0,1)$    |

Trois fois la même structure : *une suite de lois se rapproche d'une loi limite*. Rien n'y
concerne les **valeurs** prises par les variables — seulement leurs lois. C'est exactement ce
que la convergence en loi formalise, et c'est aussi ce qui explique sa faiblesse : une
information sur les lois n'est pas une information sur les nombres observés.

---

## 11bis.2 La définition

> **Définition.** Une suite $(X_n)$ **converge en loi** vers $X$, noté
> $X_n\xrightarrow{\mathcal L}X$, si
> $$F_{X_n}(x)\;\xrightarrow[n\to\infty]{}\;F_X(x)\qquad\text{en tout point }x\text{ où }F_X
> \text{ est continue.}$$

Deux points méritent une attention immédiate.

### ① Pourquoi « en tout point de continuité » — et pas partout

La restriction n'est pas une précaution d'écriture : sans elle, la définition rejetterait des cas
où la convergence est aussi forte que possible.

**Contre-exemple minimal.** $X_n=\frac1n$, constante — une suite qui converge vers $0$ de la
manière la plus brutale qui soit. Pourtant, en $x=0$ :

$$F_{X_n}(0)=P\!\left(\tfrac1n\le 0\right)=0\qquad\text{pour tout }n,
\qquad\text{alors que}\qquad F_{0}(0)=P(0\le 0)=1 .$$

En $x=0$ — le **seul** point de discontinuité de la limite — les fonctions de répartition ne
convergent pas. Partout ailleurs, elles convergent. Exiger la convergence en $x=0$ reviendrait à
déclarer que $\frac1n$ ne tend pas vers $0$.

> 🔑 Les points de discontinuité de $F_X$ sont les **atomes** de la loi limite, c'est-à-dire les
> valeurs $x$ telles que $P(X=x)>0$. Là, une masse ponctuelle peut être approchée « par la
> gauche » ou « par la droite » sans que cela change quoi que ce soit à l'approximation. La
> définition les exclut, et c'est tout.

⚠️ Corollaire pratique : quand la limite est **continue** (une gaussienne, une exponentielle), la
condition porte sur **tout** $\mathbb R$ et l'exception disparaît. C'est le cas de tous les
énoncés de ce cours sauf un — la limite Poisson du § 11bis.6, qui est discrète.

### ② La convergence porte sur les lois, pas sur les variables

> ❌ « $X_n\xrightarrow{\mathcal L}X$ signifie que $X_n$ finit par valoir à peu près $X$. »

Faux, et pas d'un peu. Prenons $X\sim\mathcal N(0,1)$ et posons $X_n=-X$ pour tout $n$. Par
symétrie de la gaussienne, $X_n$ a **exactement** la loi de $X$, donc $X_n\xrightarrow{\mathcal L}X$
trivialement. Mais $|X_n-X|=2|X|$ ne devient petit à aucun moment.

> 🔑 $X_n\xrightarrow{\mathcal L}X$ est un énoncé sur **$F_{X_n}$ et $F_X$**, pas sur l'écart
> $X_n-X$. Les variables n'ont même pas besoin d'être définies sur le même espace probabilisé.
> On écrit d'ailleurs indifféremment $X_n\xrightarrow{\mathcal L}\mathcal N(0,1)$ — une **loi** à
> droite de la flèche, ce qui serait absurde pour toute autre convergence.

---

## 11bis.3 Trois caractérisations équivalentes

Prouver une convergence en loi par la définition — établir la limite de $F_{X_n}(x)$ pour chaque
$x$ — est presque toujours impraticable. D'où l'intérêt des formulations équivalentes.

| # | Caractérisation | Quand elle sert |
|---|---|---|
| (C1) | $F_{X_n}(x)\to F_X(x)$ en tout point de continuité | La définition ; sert à **conclure** (calcul d'une probabilité) |
| (C2) | $E\big(g(X_n)\big)\to E\big(g(X)\big)$ pour toute $g$ **bornée continue** | La forme théorique ; source de la continuité (§ 11bis.5) |
| (C3) | ⭐ $\varphi_{X_n}(t)\to\varphi_X(t)$ pour tout $t$, la limite étant continue en 0 | La forme **calculatoire** : c'est le théorème de Lévy |

**(C3) est celle qu'on utilise**, sans exception, dans tout ce cours : elle échange un problème de
lois contre un calcul de limite de fonctions ordinaires ([§ 6.3](06-fonction-caracteristique.md)).

⚠️ Dans (C2), les trois mots comptent. **Bornée** : sinon la convergence des moments serait
incluse dans la définition — et elle est fausse (§ 11bis.8). **Continue** : sinon
$g=\mathbf 1_{\{x\le 0\}}$ serait admise, ce qui redonnerait la convergence en tout point,
exclue au § 11bis.2.

### Deux conditions suffisantes commodes

- **Cas discret sur un même support.** Si $P(X_n=k)\to P(X=k)$ pour tout $k$ de
  $\mathbb Z$, alors $X_n\xrightarrow{\mathcal L}X$ — et même, par le **lemme de Scheffé**,
  $\sum_k|P(X_n=k)-P(X=k)|\to0$ : la convergence est alors bien plus forte que celle des seules
  fonctions de répartition. C'est le cas de la limite Poisson.
- **Cas à densité.** Si $f_{X_n}(x)\to f_X(x)$ pour presque tout $x$, même conclusion.

⚠️ Ces conditions sont **suffisantes, jamais nécessaires**. La binomiale standardisée converge
vers $\mathcal N(0,1)$ *sans jamais avoir de densité* : elle reste discrète pour tout $n$, ses
masses ponctuelles tendent toutes vers $0$, et pourtant sa fonction de répartition converge vers
$\Phi$. **Une suite de lois discrètes peut parfaitement converger vers une loi continue** — c'est
même le cas le plus utile de tout le cours.

---

## 11bis.4 La hiérarchie des convergences

Trois convergences coexistent en probabilité, et les confondre est une source d'erreurs durables.

| Convergence | Définition | Ce qu'elle affirme |
|---|---|---|
| **Presque sûre** $\xrightarrow{p.s.}$ | $P\big(\lim_n X_n=X\big)=1$ | Chaque trajectoire, sauf un ensemble négligeable, finit par coller à $X$ |
| **En probabilité** $\xrightarrow{P}$ | $\forall\varepsilon>0,\ P(\lvertX_n-X\rvert>\varepsilon)\to0$ | L'écart est grand de moins en moins **souvent** |
| **En loi** $\xrightarrow{\mathcal L}$ | $F_{X_n}\to F_X$ aux points de continuité | Seule la **forme de la loi** se rapproche |

$$\boxed{\;X_n\xrightarrow{p.s.}X\;\Longrightarrow\;X_n\xrightarrow{P}X\;\Longrightarrow\;
X_n\xrightarrow{\mathcal L}X\;}$$

**Les réciproques sont fausses**, et il y a une exception, une seule :

> **Théorème.** Si la limite est une **constante** $c$, alors
> $X_n\xrightarrow{\mathcal L}c\iff X_n\xrightarrow{P}c$.

*Pourquoi.* Converger en loi vers la constante $c$ signifie que toute la masse s'accumule au
point $c$ ; il ne reste plus de place pour un écart. Dès que la limite est **non dégénérée**,
l'équivalence tombe : c'est le contre-exemple $X_n=-X$ du § 11bis.2, qui converge en loi vers
$\mathcal N(0,1)$ et en probabilité vers rien du tout.

### La lecture qui compte pour la suite

| Résultat | Convergence | Ce qu'il dit |
|---|---|---|
| Loi **faible** des grands nombres | $\bar X_n\xrightarrow{P}\mu$ | La moyenne se concentre en $\mu$ |
| Loi **forte** des grands nombres | $\bar X_n\xrightarrow{p.s.}\mu$ | Une trajectoire donnée y converge |
| **TCL** ([module 12](12-theoreme-central-limite.md)) | $\sqrt n\,\frac{\bar X_n-\mu}{\sigma}\xrightarrow{\mathcal L}\mathcal N(0,1)$ | La **forme** des fluctuations autour de $\mu$ |

> 🔑 La loi des grands nombres et le TCL ne sont pas deux résultats du même type : la première est
> une convergence **vers un point** (donc en probabilité, voire p.s.), le second une convergence
> **vers une loi**. Le second ne devient possible qu'après renormalisation par $\sqrt n$ —
> précisément parce que sans elle, la limite serait la constante $\mu$ et n'apprendrait rien
> ([§ 12.2](12-theoreme-central-limite.md)).

---

## 11bis.5 La boîte à outils

Quatre théorèmes suffisent à produire toutes les convergences en loi de ce cours et du
[cours de Student](../loi-de-student/README.md).

### (T1) Lévy — le dictionnaire

$\varphi_{X_n}(t)\to\psi(t)$ pour tout $t$, $\psi$ continue en 0 $\Rightarrow$ $\psi$ est une
fonction caractéristique et $X_n\xrightarrow{\mathcal L}$ la loi correspondante
([§ 6.3](06-fonction-caracteristique.md)). **C'est l'outil de démonstration ; les trois autres
sont des outils de transport.**

### (T2) Théorème de l'application continue

> Si $X_n\xrightarrow{\mathcal L}X$ et $g$ est **continue**, alors
> $g(X_n)\xrightarrow{\mathcal L}g(X)$.

Conséquence immédiate, et qui sert au [module 15](15-loi-du-chi2.md) : si
$Z_n\xrightarrow{\mathcal L}\mathcal N(0,1)$, alors $Z_n^2\xrightarrow{\mathcal L}\chi^2(1)$.

### (T3) Slutsky — celui qui autorise l'inférence réelle

> Si $X_n\xrightarrow{\mathcal L}X$ et $Y_n\xrightarrow{P}c$ (une **constante**), alors
> $$X_n+Y_n\xrightarrow{\mathcal L}X+c,\qquad X_nY_n\xrightarrow{\mathcal L}cX,\qquad
> \frac{X_n}{Y_n}\xrightarrow{\mathcal L}\frac Xc\ \ (c\ne0).$$

⚠️ **L'hypothèse « constante » est indispensable.** Avec $X_n=X\sim\mathcal N(0,1)$ et $Y_n=-X$ :
$X_n\xrightarrow{\mathcal L}\mathcal N(0,1)$, $Y_n\xrightarrow{\mathcal L}\mathcal N(0,1)$, mais
$X_n+Y_n=0$, très loin de la $\mathcal N(0,2)$ qu'on aurait « déduite ». **Deux convergences en
loi ne s'additionnent pas** — elles ne disent rien de la dépendance entre les deux suites.

**Ce que Slutsky permet, et c'est considérable.** Le TCL donne la loi limite du pivot à $\sigma$
**connu**. Or on ne connaît jamais $\sigma$ ; on dispose de $S$. Écrivons :

$$\frac{\bar X_n-\mu}{S/\sqrt n}
=\underbrace{\frac{\bar X_n-\mu}{\sigma/\sqrt n}}_{\xrightarrow{\mathcal L}\ \mathcal N(0,1)
\ \text{(TCL)}}\times\underbrace{\frac{\sigma}{S}}_{\xrightarrow{P}\ 1\ \text{(LGN)}}
\qquad\Longrightarrow\qquad
\frac{\bar X_n-\mu}{S/\sqrt n}\;\xrightarrow{\mathcal L}\;\mathcal N(0,1).$$

> 🔑 **Une ligne, et tout l'édifice de la partie VI tient.** Remplacer le paramètre inconnu
> $\sigma$ par son estimateur $S$ ne change **rien** à la loi limite. C'est ce qui rend les
> [intervalles de confiance](18-intervalle-de-confiance.md) calculables.
> ⚠️ Mais c'est un résultat **asymptotique** : à $n$ fini, le remplacement coûte quelque chose, et
> ce quelque chose porte un nom — la [loi de Student](../loi-de-student/README.md).

### (T4) La delta-méthode — transporter une limite à travers une fonction

> Si $\sqrt n\,(T_n-\theta)\xrightarrow{\mathcal L}\mathcal N(0,\sigma^2)$ et si $g$ est
> dérivable en $\theta$ avec $g'(\theta)\ne0$, alors
> $$\sqrt n\,\big(g(T_n)-g(\theta)\big)\;\xrightarrow{\mathcal L}\;
> \mathcal N\big(0,\;g'(\theta)^2\sigma^2\big).$$

*Démonstration en deux lignes.* Taylor : $g(T_n)-g(\theta)=g'(\theta)(T_n-\theta)+R_n$ avec
$R_n$ négligeable devant $|T_n-\theta|$ ; multiplier par $\sqrt n$ et appliquer (T2) puis (T3).

**Deux usages.**

- **Stabilisation de variance.** Pour des comptages Poisson, $\operatorname{Var}=\lambda$ dépend
  du niveau. Avec $g=\sqrt{\ \cdot\ }$, $g'(\lambda)=\frac1{2\sqrt\lambda}$ et la variance
  asymptotique devient $\frac{1}{4\lambda}\cdot\lambda=\frac14$ — **constante**. C'est pourquoi
  on trace des racines de comptages, pas des comptages.
- **Passage aux rendements logarithmiques.** $g=\log$ donne $g'(\theta)=1/\theta$ : une erreur
  **absolue** sur un prix devient une erreur **relative** sur son log. C'est la justification
  asymptotique de la convention de `modele.md`.

---

## 11bis.6 Le triangle binomiale – Poisson – normale

Trois lois, trois flèches, et une subtilité qui décide de laquelle utiliser.

```
                  B(n, p)
                 /        \
   np → λ       /          \     n → ∞, p fixé
   (p → 0)     /            \    (de Moivre–Laplace)
              ↓              ↓
           P(λ)  ─────────→  N(0,1)      standardisées
                   λ → ∞
```

### ① Binomiale $\to$ Poisson — la loi des événements rares

Démontrée au [§ 6c.4](06c-loi-de-poisson.md) : si $np_n\to\lambda$, alors
$\mathcal B(n,p_n)\xrightarrow{\mathcal L}\mathcal P(\lambda)$. Le développement est d'ordre **1**,
là où le TCL en demandera un d'ordre 2.

Cette convergence-ci a un privilège rare : **elle est chiffrée**.

> **Inégalité de Le Cam.** $\displaystyle d_{TV}\big(\mathcal B(n,p),\mathcal P(np)\big)\;\le\;np^2 .$

où $d_{TV}=\frac12\sum_k\big|P(X=k)-P(Y=k)\big|$ majore l'erreur commise sur **n'importe quel**
événement — pas seulement sur les $F(x)$. À $\lambda=np$ fixé, la borne vaut $\lambda p$ : elle
tend vers 0 **quand $p$ tend vers 0**, jamais quand $n$ seul grandit. Le § 11bis.9 vérifie que
l'erreur réelle vaut environ $np^2/20$.

### ② Binomiale $\to$ normale — de Moivre–Laplace

À $p$ **fixé**, $\frac{X-np}{\sqrt{npq}}\xrightarrow{\mathcal L}\mathcal N(0,1)$ : c'est le TCL
appliqué à une somme de Bernoulli ([§ 6b.1](06b-loi-binomiale.md)) — historiquement, c'est
même le premier TCL démontré, un siècle avant le cas général.

⚠️ La loi de départ est **discrète**, la limite est **continue** : la
[correction de continuité](06b-loi-binomiale.md) n'est pas une coquetterie, elle vaut un ordre de
grandeur (§ 11bis.9).

### ③ Poisson $\to$ normale

> **Théorème.** Si $X_\lambda\sim\mathcal P(\lambda)$, alors
> $\dfrac{X_\lambda-\lambda}{\sqrt\lambda}\xrightarrow[\lambda\to\infty]{\mathcal L}\mathcal N(0,1)$.

**Démonstration.** $\varphi_{X_\lambda}(t)=e^{\lambda(e^{it}-1)}$
([§ 6c.3](06c-loi-de-poisson.md)). Pour $Y_\lambda=(X_\lambda-\lambda)/\sqrt\lambda$, (P2) donne

$$\log\varphi_{Y_\lambda}(t)=\lambda\Big(e^{\,it/\sqrt\lambda}-1\Big)-it\sqrt\lambda
=\lambda\left(\frac{it}{\sqrt\lambda}-\frac{t^2}{2\lambda}
+O\!\big(\lambda^{-3/2}\big)\right)-it\sqrt\lambda
=-\frac{t^2}{2}+O\!\left(\frac{1}{\sqrt\lambda}\right).$$

Les termes en $\sqrt\lambda$ se compensent exactement — c'est le centrage — et il reste
$\varphi_{Y_\lambda}(t)\to e^{-t^2/2}$, continue en 0. Lévy conclut. $\blacksquare$

> 🔑 **Trois remarques sur cette démonstration.**
> - Elle est **le TCL en miniature** : centrer, développer à l'ordre 2, reconnaître, appliquer
>   Lévy. Comparez ligne à ligne avec le [§ 12.3](12-theoreme-central-limite.md).
> - Pour $\lambda$ **entier**, on pourrait invoquer le TCL directement, puisque
>   $\mathcal P(\lambda)$ est la somme de $\lambda$ lois $\mathcal P(1)$ indépendantes
>   ([§ 6c.4](06c-loi-de-poisson.md)). Le calcul ci-dessus a l'avantage de valoir pour $\lambda$
>   **réel**, ce que le TCL ne couvre pas littéralement.
> - Le reste est en $1/\sqrt\lambda$ — soit exactement $\gamma_1=1/\sqrt\lambda$, l'asymétrie de
>   la Poisson ([§ 6c.3](06c-loi-de-poisson.md)). On retrouvera ce nombre au § 11bis.9 comme
>   **la** mesure de l'erreur.

### La subtilité : les deux flèches ne commutent pas

Partant d'une $\mathcal B(n,p)$, on peut faire tendre $n$ vers l'infini de deux façons — et elles
ne donnent pas la même limite :

| Régime | Ce qui reste fixe | Limite | Pourquoi |
|---|---|---|---|
| $p\to0$, $np\to\lambda$ | l'**espérance** $\lambda$ | $\mathcal P(\lambda)$ — discrète | Le nombre d'occurrences reste petit |
| $p$ fixé, $n\to\infty$ | la **probabilité** $p$ | $\mathcal N(0,1)$ après standardisation | $npq\to\infty$ : beaucoup d'occurrences |

Autrement dit : **ce n'est pas $n$ qui décide, c'est $npq$.** Une binomiale à $n=10\,000$ et
$p=0{,}0005$ a $n$ énorme et une approximation normale **franchement mauvaise**, parce que
$npq\approx5$. Le § 11bis.9 le montre chiffres en main : à $\lambda=5$ fixé, l'erreur de
l'approximation normale **ne diminue pas** quand $n\to\infty$ — elle plafonne à 0,029.

### La règle de décision

| Situation | Approximation | Erreur attendue sur $F$ |
|---|---|---|
| $p\le0{,}05$ et $np\lesssim10$ | $\mathcal P(np)$ | $\approx np^2/20$ (Le Cam) |
| $npq\gtrsim10$ | $\mathcal N(np,npq)$ **avec** correction de continuité | $\approx0{,}066\,\gamma_1$, $\gamma_1=\frac{1-2p}{\sqrt{npq}}$ |
| $\lambda\gtrsim10$ | $\mathcal N(\lambda,\lambda)$ **avec** correction | $\approx0{,}066/\sqrt\lambda$ |
| Aucune des deux | Calcul exact — il tient en une ligne de code | — |

> 🔑 **Le vrai critère n'est ni « $n\ge30$ » ni « $npq\ge10$ » : c'est $\gamma_1$.** Le premier
> terme négligé dans le développement d'Edgeworth vaut $\frac{\gamma_1}{6}(z^2-1)\phi(z)$, dont
> le maximum en $z$ est $\frac{\gamma_1}{6}\phi(0)=\frac{\gamma_1}{6\sqrt{2\pi}}\approx0{,}066\,\gamma_1$.
> C'est **exactement** le message du [module 13](13-portee-et-limites-du-tcl.md), ici vérifiable
> à la troisième décimale (§ 11bis.9).

---

## 11bis.7 Les autres convergences classiques

Le triangle n'épuise pas le sujet. Toutes les lignes ci-dessous se démontrent par (T1), en
quelques lignes chacune.

| Convergence | Condition | Usage | Démonstration |
|---|---|---|---|
| Hypergéométrique $\to$ $\mathcal B(n,K/N)$ | $N\to\infty$, $K/N\to p$ | Tirage **sans** remise $\approx$ avec remise si $n/N\le10\,\%$ | Rapport de factorielles |
| $\mathcal B\to\mathcal P$ | $np\to\lambda$, $p\to0$ | Événements rares | [§ 6c.4](06c-loi-de-poisson.md) |
| $\mathcal P\to\mathcal N$ | $\lambda\to\infty$ | Comptages massifs | § 11bis.6 ③ |
| $p\,G_p\to\mathcal E(1)$ | $p\to0$, $G_p$ géométrique | L'exponentielle comme limite continue de l'attente discrète | $P(pG_p>x)=(1-p)^{\lceil x/p\rceil}\to e^{-x}$ |
| $\dfrac{K-k}{\sqrt{2k}}\to\mathcal N(0,1)$ | $k\to\infty$, $K\sim\chi^2(k)$ | Grands degrés de liberté | [Module 15](15-loi-du-chi2.md) : $\chi^2(k)=\sum_1^k Z_i^2$, puis TCL |
| $\mathcal T(k)\to\mathcal N(0,1)$ | $k\to\infty$ | Pourquoi Student « redevient » normale | [Cours Student](../loi-de-student/README.md), via (T3) |
| $M_n-\ln n\to$ **Gumbel** | $X_i$ i.i.d. $\mathcal E(1)$, $M_n=\max X_i$ | Valeurs extrêmes | $\left(1-\frac{e^{-x}}{n}\right)^n\to e^{-e^{-x}}$ |

> ⚠️ **La dernière ligne est la plus instructive.** Elle porte sur un **maximum**, pas sur une
> somme : la convergence en loi n'est pas la propriété des moyennes, c'est un cadre général. Et
> sa limite n'est **pas gaussienne** — la théorie des valeurs extrêmes (Fisher–Tippett–Gnedenko)
> a ses trois lois propres. Un TCL sur les moyennes ne dit **rien** sur les maxima : c'est
> l'origine de l'erreur la plus coûteuse en gestion du risque
> ([§ 13.1](13-portee-et-limites-du-tcl.md)).

---

## 11bis.8 Ce qu'une convergence en loi ne donne pas

Quatre limitations, dont trois causent des dégâts réels.

### ① Elle ne donne pas la convergence des moments

**Contre-exemple.** $P(X_n=n^2)=\frac1n$ et $P(X_n=0)=1-\frac1n$. Alors :

$$X_n\xrightarrow{\mathcal L}0\quad\text{(la masse file vers 0)},\qquad\text{mais}\qquad
E(X_n)=\frac{n^2}{n}=n\;\longrightarrow\;+\infty .$$

La loi converge vers la constante $0$ ; l'espérance diverge. Une masse minuscule placée
très loin ne se voit pas dans $F$, et pèse tout le poids dans $E$.

> ⚠️ **Conséquence pratique.** Approcher la loi d'une statistique par sa limite ne légitime
> **jamais** d'approcher son espérance ou sa variance par celles de la limite. Il y faut une
> hypothèse supplémentaire (l'*uniforme intégrabilité*), qui ne se lit pas sur la convergence en
> loi. Voir aussi l'exercice E11bis.5.

### ② Elle ne donne aucune erreur chiffrée

$F_n\to F$ ne dit rien de $|F_n-F|$ à $n$ fini : c'est la même limitation qu'au
[§ 12.5](12-theoreme-central-limite.md). Chiffrer exige un théorème **supplémentaire** :
Berry–Esseen pour le TCL ([module 13](13-portee-et-limites-du-tcl.md)), Le Cam pour la limite
Poisson. Aucun des deux ne se déduit de la convergence.

### ③ L'erreur est uniforme en valeur absolue, jamais en valeur relative

Il y a une bonne nouvelle : **théorème de Pólya** — si la limite $F$ est **continue**, la
convergence simple des $F_n$ est automatiquement **uniforme** :
$\sup_x|F_n(x)-F(x)|\to0$. C'est ce qui justifie de mesurer l'erreur par un $\sup$ dans tous les
tableaux de ce module.

Mais une erreur absolue uniformément petite peut être une erreur relative catastrophique là où
les probabilités sont minuscules. Pour $X\sim\mathcal P(25)$, l'approximation normale (avec
correction) donne :

| Seuil $k$ | $\lambda+\sqrt\lambda$ | $+2\sqrt\lambda$ | $+3\sqrt\lambda$ | $+4\sqrt\lambda$ | $+5\sqrt\lambda$ |
|---|---|---|---|---|---|
| $P(X\ge k)$ **exact** | $1{,}82\cdot10^{-1}$ | $3{,}38\cdot10^{-2}$ | $3{,}44\cdot10^{-3}$ | $2{,}00\cdot10^{-4}$ | $6{,}95\cdot10^{-6}$ |
| Approximation normale | $1{,}84\cdot10^{-1}$ | $2{,}87\cdot10^{-2}$ | $1{,}87\cdot10^{-3}$ | $4{,}81\cdot10^{-5}$ | $4{,}79\cdot10^{-7}$ |
| **Rapport** | 1,01 | 0,85 | **0,54** | **0,24** | **0,07** |

À 5 écarts-types, la normale sous-estime la vraie probabilité d'un facteur **14**. En valeur
absolue l'erreur est pourtant de $6{,}5\cdot10^{-6}$ — invisible dans n'importe quel $\sup$.

> 🔑 **C'est exactement le terrain de la VaR et des tests de résistance.** Un quantile à
> 99,9 % vit dans la zone où le rapport vaut 0,2, pas 1. Toutes les approximations de ce module
> sont bonnes **au centre** et fausses **dans les queues** — voir
> [§ 6f.5](06f-loi-normale.md) et [§ 13.1](13-portee-et-limites-du-tcl.md).

### ④ Elle ne préserve pas la nature de la loi

Approcher une $\mathcal B(n,p)$ par une normale supprime deux propriétés que le modèle avait :
le support **entier** et le support **positif**. Une normale ajustée sur des comptages accorde
une probabilité non nulle à $-3$ occurrences. Sur un comptage à faible $\lambda$, cela peut peser
plusieurs pour cent.

> 🔑 L'approximation Poisson, elle, préserve la nature discrète **et** la signature
> $E=\operatorname{Var}$ ([§ 6c.3](06c-loi-de-poisson.md)). Quand les deux approximations sont
> défendables, préférer celle qui conserve les propriétés **réfutables** du modèle : elle reste
> testable.

---

## 11bis.9 Simulations

### S11bis.1 — Le triangle, et la non-commutation des deux limites

Aucun tirage : tout est **exact**.

```python
import numpy as np
from scipy import stats

print(f"{'n':>7}{'p':>9}{'sup|F_B-F_P|':>14}{'d_TV':>10}{'np^2':>9}"
      f"{'sup|F_B-N cc|':>15}{'sans cc':>10}")
for n, p in [(10, .5), (20, .25), (50, .1), (100, .05), (500, .01),
             (1000, .005), (10_000, .0005)]:
    lam, k = n * p, np.arange(0, n + 1)
    Fb = stats.binom.cdf(k, n, p)
    d_tv = .5 * np.abs(stats.binom.pmf(k, n, p) - stats.poisson.pmf(k, lam)).sum()
    mu, sd = n * p, np.sqrt(n * p * (1 - p))
    print(f"{n:>7}{p:>9}{np.abs(Fb - stats.poisson.cdf(k, lam)).max():>14.5f}"
          f"{d_tv:>10.5f}{n * p * p:>9.5f}"
          f"{np.abs(Fb - stats.norm.cdf((k + .5 - mu) / sd)).max():>15.5f}"
          f"{np.abs(Fb - stats.norm.cdf((k - mu) / sd)).max():>10.5f}")
```

**Résultat — $\lambda=np=5$ dans toute la colonne.**

| $n$ | 10 | 50 | 100 | 1 000 | 10 000 |
|---|---|---|---|---|---|
| $p$ | 0,5 | 0,1 | 0,05 | 0,005 | 0,0005 |
| $\sup\lvert F_B-F_P\rvert$ | 0,0932 | 0,0147 | 0,0072 | 0,0007 | **0,00007** |
| $d_{TV}$ (Le Cam $\le np^2$) | 0,172 | 0,026 | 0,0126 | 0,0012 | 0,00012 |
| $np^2$ | 2,50 | 0,50 | 0,25 | 0,025 | 0,0025 |
| $\sup\lvert F_B-\mathcal N\rvert$ (avec cc) | 0,0027 | 0,0244 | 0,0267 | 0,0287 | **0,0289** |
| $\sup\lvert F_B-\mathcal N\rvert$ (sans cc) | 0,123 | 0,116 | 0,116 | 0,116 | 0,116 |

**Quatre lectures, et la troisième est le cœur du module.**

- **La borne de Le Cam tient**, et du bon ordre : $d_{TV}\approx np^2/20$ sur toute la colonne.
  Elle est conservatrice d'un facteur 20, jamais fausse.
- **La correction de continuité vaut un facteur 4 à 40.** Sans elle, l'erreur plafonne à 0,116 et
  ne descend **jamais** : c'est un demi-pas de la grille discrète, un biais systématique que $n$
  ne corrige pas.
- ⭐ **L'approximation normale ne s'améliore pas quand $n$ croît** : 0,0027 puis 0,024 puis
  0,029 — elle **empire**, puis se stabilise à la distance qui sépare $\mathcal P(5)$ de la
  normale. C'est la non-commutation du § 11bis.6 : à $\lambda$ fixé, $\mathcal B(n,p)$ ne
  converge pas vers une gaussienne, elle converge vers $\mathcal P(5)$, laquelle n'est pas
  gaussienne. **Un grand $n$ ne justifie pas une approximation normale.**
- **Les deux colonnes vont en sens inverse** : la Poisson est de mieux en mieux, la normale de
  moins en moins. Le critère de choix n'est pas $n$, c'est $npq$.

### S11bis.2 — Poisson $\to$ normale : l'erreur est l'asymétrie

```python
for lam in (1, 5, 10, 25, 100, 400):
    k = np.arange(0, int(lam + 12 * np.sqrt(lam)) + 20)
    Fp = stats.poisson.cdf(k, lam)
    e_cc = np.abs(Fp - stats.norm.cdf((k + .5 - lam) / np.sqrt(lam))).max()
    e_0 = np.abs(Fp - stats.norm.cdf((k - lam) / np.sqrt(lam))).max()
    g1 = 1 / np.sqrt(lam)
    print(f"lam={lam:>5}  gamma1={g1:.3f}  sup|F-Phi| cc={e_cc:.5f}"
          f"  sans cc={e_0:.5f}   erreur/gamma1={e_cc / g1:.4f}")
```

| $\lambda$ | 1 | 5 | 10 | 25 | 100 | 400 |
|---|---|---|---|---|---|---|
| $\gamma_1=1/\sqrt\lambda$ | 1,000 | 0,447 | 0,316 | 0,200 | 0,100 | 0,050 |
| $\sup\lvert F-\Phi\rvert$ **avec** cc | 0,0593 | 0,0290 | 0,0208 | 0,0132 | 0,0066 | 0,0033 |
| sans cc | 0,236 | 0,116 | 0,083 | 0,053 | 0,027 | 0,013 |
| **erreur $/\gamma_1$** | 0,059 | 0,065 | 0,066 | 0,066 | **0,066** | **0,066** |

La dernière ligne est constante à partir de $\lambda=10$, et vaut exactement
$\frac1{6\sqrt{2\pi}}=0{,}0665$ — la constante d'Edgeworth annoncée au § 11bis.6.

> 🔑 **L'erreur n'est pas une fonction de $\lambda$, c'est une fonction de $\gamma_1$**, et le
> même $0{,}066$ gouverne la binomiale (à vérifier en E11bis.4). Retenir un seuil chiffré
> — « $\lambda\ge10$ » — c'est retenir un cas particulier d'une formule qui tient en une ligne :
> $$\sup_x|F_n(x)-\Phi(x)|\;\approx\;0{,}066\,|\gamma_1| .$$
> Pour une erreur inférieure à 1 %, il faut donc $|\gamma_1|\le0{,}15$, soit $\lambda\ge45$ —
> quatre fois le seuil habituellement enseigné.

### S11bis.3 — Ce que la convergence en loi ne donne pas

```python
rng = np.random.default_rng(7)

# (a) la loi converge, l'espérance diverge
for n in (10, 100, 1000, 10_000):
    X = np.where(rng.random(200_000) < 1 / n, n ** 2, 0.0)
    print(f"n={n:>6}  P(X>1) = {(X > 1).mean():.5f} -> 0 "
          f"    moyenne empirique = {X.mean():>10.1f}  (theorie : {n})")

# (b) la queue : erreur absolue minuscule, erreur relative catastrophique
lam = 25
for z in (1, 2, 3, 4, 5):
    k = round(lam + z * np.sqrt(lam))
    exact = stats.poisson.sf(k - 1, lam)
    appro = stats.norm.sf((k - .5 - lam) / np.sqrt(lam))
    print(f"k={k:>3} (z={z})  exact={exact:.3e}  normale={appro:.3e}"
          f"  rapport={appro / exact:.3f}  ecart absolu={abs(appro - exact):.2e}")
```

La partie (a) reproduit le contre-exemple du § 11bis.8 ① : $P(X_n>1)\to0$ — la loi converge vers
la constante 0 — pendant que la moyenne empirique grimpe avec $n$. La partie (b) reproduit le
tableau des queues : l'écart **absolu** décroît jusqu'à $6\cdot10^{-6}$ tandis que le **rapport**
tombe à 0,07.

---

## 11bis.10 Exercices

**E11bis.1.** Soit $X_n$ uniforme sur $\{0,\frac1n,\frac2n,\dots,1\}$. Montrer que
$X_n\xrightarrow{\mathcal L}\mathcal U(0,1)$. *La suite a-t-elle une densité ? La limite en
a-t-elle une ? Quelle caractérisation du § 11bis.3 utilisez-vous, et pourquoi pas l'autre ?*

**E11bis.2.** $X\sim\mathcal N(0,1)$, $X_n=(-1)^nX$. Montrer que $X_n\xrightarrow{\mathcal L}X$ et
que $(X_n)$ ne converge en probabilité vers rien. *Puis expliquer pourquoi cela n'a aucune
incidence sur l'usage qu'on fait du TCL.*

**E11bis.3.** Démontrer $p\,G_p\xrightarrow{\mathcal L}\mathcal E(1)$ quand $p\to0$, où
$G_p$ suit la loi géométrique de paramètre $p$ sur $\{1,2,\dots\}$. *Deux voies : par la fonction
de répartition, ou par la fonction caractéristique. Faire les deux et comparer.*

**E11bis.4.** Vérifier numériquement, pour $\mathcal B(n,p)$ avec $p\in\{0{,}05\,;0{,}2\}$ et
$n\in\{25,100,400\}$, que $\sup_x|F(x)-\Phi_{cc}(x)|\approx0{,}066\,\gamma_1$ avec
$\gamma_1=\frac{1-2p}{\sqrt{npq}}$. *Que se passe-t-il à $p=0{,}5$, et pourquoi ? Quel est alors
l'ordre de l'erreur en $n$ ?*

**E11bis.5.** Reprendre le contre-exemple du § 11bis.8 ①. Le modifier pour obtenir une suite qui
converge en loi vers $\mathcal N(0,1)$ tout en ayant une variance qui diverge. *En déduire une
mise en garde d'une phrase sur l'estimation d'une variance asymptotique.*

**E11bis.6.** Une salle de marché reçoit en moyenne 3 ordres erronés par jour ouvré.
1. Sur 250 séances, quelle loi pour le total ? Justifier par une convergence, pas par analogie.
2. Calculer $P(\text{total}\ge800)$ exactement, puis par approximation normale avec et sans
   correction de continuité. Commenter les trois chiffres à la lumière du § 11bis.9.
3. La direction demande le quantile à 99,9 %. Que répondez-vous, et avec quelle réserve ?

**E11bis.7 — orientée finance.** Sur une série obtenue avec `import_societe.py` :
1. compter les séances de baisse supérieure à 3 % par mois, et ajuster une $\mathcal P(\lambda)$ ;
2. tester la signature $E=\operatorname{Var}$ ([§ 6c.3](06c-loi-de-poisson.md)) ;
3. si elle échoue, dire laquelle des hypothèses de la limite binomiale $\to$ Poisson est
   violée — $p$ petit, ou **indépendance** des séances ? Relier au
   [module 14](14-dependance-et-echec-du-tcl.md).

---

## 11bis.11 À retenir

- **Définition** : $X_n\xrightarrow{\mathcal L}X$ signifie $F_{X_n}(x)\to F_X(x)$ **en tout point
  de continuité de $F_X$** — restriction indispensable dès que la limite a des atomes.
- C'est un énoncé sur les **lois**, pas sur les variables : $|X_n-X|$ peut ne jamais devenir
  petit, et les variables peuvent même vivre sur des espaces différents.
- **Hiérarchie** : $p.s.\Rightarrow P\Rightarrow\mathcal L$, aucune réciproque — sauf lorsque la
  limite est une **constante**, où $\mathcal L$ et $P$ coïncident.
- **La boîte à outils** : Lévy pour démontrer, application continue pour transporter, **Slutsky**
  pour remplacer $\sigma$ par $S$ sans changer la loi limite, delta-méthode pour passer une
  limite à travers une fonction dérivable.
- **Le triangle** $\mathcal B\to\mathcal P\to\mathcal N$ : ce n'est pas $n$ qui décide de
  l'approximation, c'est $npq$. À $\lambda=np$ fixé, l'approximation normale **ne s'améliore
  jamais**, quel que soit $n$.
- **L'erreur, quand la limite est normale**, vaut $\approx0{,}066\,|\gamma_1|$ — avec correction
  de continuité, sans laquelle un biais de un demi-pas subsiste indéfiniment. Le vrai critère est
  l'asymétrie, jamais un seuil sur $n$ ou $\lambda$.
- **Ce qu'une convergence en loi ne donne pas** : la convergence des moments, une erreur chiffrée,
  une erreur **relative** contrôlée dans les queues (facteur 14 à $5\sigma$ sur une Poisson), ni
  la conservation du support. Les approximations sont bonnes au centre et fausses aux extrêmes.

---

⬅️ [Module 11 — Invariance par rotation et lemme de projection](11-invariance-par-rotation-et-lemme-de-projection.md) ·
➡️ [Module 12 — Le théorème central limite](12-theoreme-central-limite.md) ·
🏠 [Sommaire](README.md)
