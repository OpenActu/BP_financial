# Module 6d — La loi uniforme

**Durée : 1 h.** Prérequis : [module 6c](06c-loi-de-poisson.md) — et, pour le § 6d.3, le
[§ 1.3](01-variable-aleatoire-et-loi.md) sur les densités.

> **La question traitée.** On passe du discret au continu. La loi uniforme est la première loi à
> densité du chapitre, et la seule dont on puisse tout calculer à la main sans une seule astuce.
> Elle est aussi **la source de toutes les autres** : c'est d'elle que sort chaque nombre
> aléatoire des simulations de ce cours.

**Ce qui est en jeu.** Trois résultats à retenir, d'usages très différents :
$\operatorname{Var}=(b-a)^2/12$ — qui chiffre le bruit d'arrondi d'une cotation ; la
**transformation inverse**, qui fabrique n'importe quelle loi à partir d'une uniforme ; et la
**PIT**, qui retourne l'opération pour valider un modèle.

---

## 6d.1 Définition

> **Définition.** $X$ suit la **loi uniforme** sur $[a,b]$ ($a<b$), notée
> $X\sim\mathcal U(a,b)$, si elle admet la densité
> $$f(x)=\frac{1}{b-a}\ \ \text{si }x\in[a,b],\qquad f(x)=0\ \text{sinon}$$

La densité est **constante** : aucune zone de $[a,b]$ n'est privilégiée. Sa fonction de
répartition est affine sur $[a,b]$ :

$$F(x)=\frac{x-a}{b-a}\quad\text{pour }x\in[a,b],
\qquad F(x)=0\ \text{si }x<a,\qquad F(x)=1\ \text{si }x>b$$

⚠️ **Une densité n'est pas une probabilité** ([§ 1.3](01-variable-aleatoire-et-loi.md)) : sur
$[0\,;0{,}1]$, $f$ vaut $10$. Ce qui doit valoir 1, c'est **l'aire** — ici celle d'un rectangle de
base $b-a$ et de hauteur $1/(b-a)$.

**Le cas de référence.** $\mathcal U(0,1)$ est la brique élémentaire : toute uniforme s'en déduit
par la transformation affine

$$X=a+(b-a)\,U,\qquad U\sim\mathcal U(0,1)$$

C'est cette réduction qui rend inutile de refaire deux fois chaque calcul (§ 6d.4).

---

## 6d.2 Espérance et variance, sans transformée

**Espérance.** Une intégrale de polynôme, rien de plus :

$$E(X)=\int_a^b x\,\frac{dx}{b-a}=\frac{1}{b-a}\left[\frac{x^2}{2}\right]_a^b
=\frac{b^2-a^2}{2(b-a)}=\frac{(b-a)(b+a)}{2(b-a)}=\boxed{\;\frac{a+b}{2}\;}$$

C'est le **milieu** du segment, comme la symétrie de la densité le laissait attendre.

**Moment d'ordre 2.** Même calcul, un degré plus haut, avec l'identité
$b^3-a^3=(b-a)(a^2+ab+b^2)$ :

$$E(X^2)=\int_a^b x^2\,\frac{dx}{b-a}=\frac{b^3-a^3}{3(b-a)}=\frac{a^2+ab+b^2}{3}$$

**Variance.** Par König–Huygens, en réduisant au dénominateur 12 :

$$\operatorname{Var}(X)=\frac{a^2+ab+b^2}{3}-\frac{(a+b)^2}{4}
=\frac{4(a^2+ab+b^2)-3(a+b)^2}{12}
=\frac{a^2-2ab+b^2}{12}
=\boxed{\;\frac{(b-a)^2}{12}\;}\qquad\blacksquare$$

> 🔑 **Le 12 n'est pas décoratif : $\sigma=(b-a)/\sqrt{12}\approx0{,}289\,(b-a)$.** L'écart-type
> d'une uniforme vaut moins de **trois dixièmes** de l'étendue. C'est ce nombre qui,
> au § 6d.5, chiffre l'erreur d'arrondi d'un prix coté.

**La voie symétrique, plus courte.** En écrivant $X=\frac{a+b}{2}+(b-a)V$ avec
$V\sim\mathcal U(-\tfrac12,\tfrac12)$ : $E(V)=0$ **par symétrie**, sans calcul, et

$$\operatorname{Var}(V)=E(V^2)=\int_{-1/2}^{1/2}v^2\,dv=\left[\frac{v^3}{3}\right]_{-1/2}^{1/2}=\frac{1}{12}$$

d'où $\operatorname{Var}(X)=(b-a)^2\operatorname{Var}(V)=(b-a)^2/12$ par la propriété
$\operatorname{Var}(cV)=c^2\operatorname{Var}(V)$ ([§ 3.2](03-variance-et-moments.md)). **Centrer
avant de calculer économise la moitié du travail** — c'est le même réflexe qu'au module 7 avec
$X=\mu+\sigma Z$.

**Les moments de forme.** La densité étant symétrique, $\gamma_1=0$. Le kurtosis vaut
$\beta_2=9/5=1{,}8$, soit un **excès de $-1{,}2$** : la loi la plus « à queues courtes » du
chapitre — normal, elle n'a pas de queue du tout. C'est pourquoi le
[§ 13.1](13-portee-et-limites-du-tcl.md) note que $n=5$ suffit à la normaliser.

---

## 6d.3 Espérance et variance, par la fonction caractéristique

### La fonction caractéristique

Première intégrale complexe du chapitre — et elle est immédiate, l'exponentielle étant sa propre
primitive :

$$\varphi_X(t)=\int_a^b e^{itx}\,\frac{dx}{b-a}
=\frac{1}{b-a}\left[\frac{e^{itx}}{it}\right]_a^b
=\boxed{\;\frac{e^{itb}-e^{ita}}{it\,(b-a)}\;}\qquad(t\ne0),\qquad \varphi_X(0)=1$$

Deux cas particuliers, à connaître :

| Loi | $\varphi(t)$ |
|---|---|
| $\mathcal U(0,1)$ | $\dfrac{e^{it}-1}{it}$ |
| $\mathcal U(-c,c)$ | $\dfrac{\sin(ct)}{ct}$ — **réelle**, car la loi est symétrique (exercice E6.1) |

⚠️ **Le point $t=0$ est une singularité apparente** : le quotient est de la forme $0/0$, mais la
limite vaut 1. Dériver ce quotient en 0 est possible mais pénible ; il existe bien mieux.

### La dérivation par la série — la vraie méthode

Plutôt que de dériver, on **développe** et on identifie coefficient par coefficient. Sur
$\mathcal U(0,1)$ :

$$\varphi_U(t)=\frac{e^{it}-1}{it}
=\frac{1}{it}\sum_{k\ge1}\frac{(it)^k}{k!}
=\sum_{k\ge1}\frac{(it)^{k-1}}{k!}
\overset{m=k-1}{=}\sum_{m\ge0}\frac{(it)^m}{(m+1)!}$$

Or (§ 6a.3) le développement générique d'une fonction caractéristique est
$\varphi_U(t)=\sum_m E(U^m)\dfrac{(it)^m}{m!}$. **Deux séries entières égales ont les mêmes
coefficients** :

$$\frac{E(U^m)}{m!}=\frac{1}{(m+1)!}
\qquad\Longrightarrow\qquad
\boxed{\;E(U^m)=\frac{m!}{(m+1)!}=\frac{1}{m+1}\;}$$

**Tous les moments d'un coup**, et c'est le résultat le plus élégant du chapitre. Il donne
directement

$$E(U)=\frac12\;\checkmark,\qquad
E(U^2)=\frac13,\qquad
\operatorname{Var}(U)=\frac13-\frac14=\frac{1}{12}\;\checkmark,\qquad
E(U^4)=\frac15$$

et l'on retrouve $\beta_2=E(V^4)/\operatorname{Var}(V)^2$ annoncé au § 6d.2 (exercice E6d.2).

**Le cas général** s'obtient sans nouveau calcul, par la propriété affine
($\varphi_{a+cU}(t)=e^{iat}\varphi_U(ct)$, qui combine (P3) et un décalage) :

$$X=a+(b-a)U\ \Longrightarrow\ E(X)=a+(b-a)\tfrac12=\frac{a+b}{2},\qquad
\operatorname{Var}(X)=(b-a)^2\times\frac1{12}$$

> 🔑 **Sur une loi à densité, la f.c. change de rôle.** Sur la Bernoulli, elle refaisait un calcul
> déjà trivial. Ici elle produit **la suite complète des moments** en trois lignes, là où la voie
> directe demanderait une intégrale par moment. Et sur la normale
> ([module 6f](06f-loi-normale.md)), elle sera carrément plus simple que la voie directe.

---

## 6d.4 Les deux propriétés qui font de l'uniforme la source du hasard

> 📐 **Les deux résultats de cette section sont démontrés** au
> [§ 9.5 du cours de dérivation et intégration](../../analyse/derivation-et-integration/09-changement-de-variable-et-densites.md) :
> ce sont des changements de variable où le jacobien $F'=f$ s'annule contre la densité.

### ① La transformation inverse — fabriquer n'importe quelle loi

> **Théorème.** Soit $F$ une fonction de répartition **continue et strictement croissante** sur
> son support, et $U\sim\mathcal U(0,1)$. Alors
> $$X=F^{-1}(U)\quad\text{a pour fonction de répartition } F$$

**Démonstration.** $F$ étant strictement croissante, $F^{-1}(u)\le x\iff u\le F(x)$. Donc, pour
tout $x$ :

$$P(X\le x)=P\bigl(F^{-1}(U)\le x\bigr)=P\bigl(U\le F(x)\bigr)=F(x)$$

la dernière égalité parce que $P(U\le u)=u$ sur $[0,1]$ et que $F(x)\in[0,1]$. $\blacksquare$

**Exemple immédiat**, repris au [module 6e](06e-loi-exponentielle.md) : pour l'exponentielle,
$F(x)=1-e^{-\lambda x}$ s'inverse en $F^{-1}(u)=-\log(1-u)/\lambda$, d'où le générateur

$$T=-\frac{\log(1-U)}{\lambda}\ \sim\ \mathcal E(\lambda)$$

> 🔑 **Toutes les simulations de ce cours reposent sur ce théorème.** `rng.exponential`,
> `rng.normal`, `rng.binomial` ne savent produire qu'une chose — des uniformes sur $[0,1]$ — et
> les transforment. La loi uniforme n'est pas une loi parmi d'autres : c'est **le format
> universel du hasard**.

### ② La PIT — retourner l'opération pour valider un modèle

> **Théorème (probability integral transform).** Si $X$ a pour fonction de répartition $F$
> **continue**, alors $F(X)\sim\mathcal U(0,1)$.

**Démonstration.**
Pour$u\in[0,1]$,$P\bigl(F(X)\le u\bigr)=P\bigl(X\le F^{-1}(u)\bigr) =F\bigl(F^{-1}(u)\bigr)=u$.
C'est la fonction de répartition d'une$\mathcal U(0,1)$.
$\blacksquare$

**L'usage.** Un modèle prédit une loi $F_t$ pour le rendement de demain. On calcule, jour après
jour, $u_t=F_t(r_t)$. **Si le modèle est correct, les $u_t$ sont uniformes sur $[0,1]$** — et
tester l'uniformité d'un échantillon est facile. C'est le principe des contrôles de modèles de
VaR ([§ 6f.5](06f-loi-normale.md)).

### ③ Ce que l'uniforme n'est pas : stable

$\mathcal U(0,1)+\mathcal U(0,1)$ **n'est pas uniforme** : c'est une loi **triangulaire** sur
$[0,2]$. Le produit $\left(\frac{e^{it}-1}{it}\right)^2$ n'est la f.c. d'aucune uniforme. Le
[§ 8.3](08-addition-de-lois-et-stabilite-gaussienne.md) en fait le contre-exemple de référence :
la stabilité gaussienne est un privilège rare.

---

## 6d.5 Exemple complet — le pas de cotation, ou combien vaut un arrondi

**Le problème.** Une action cote autour de $P=50$ € avec un **pas de cotation** (tick) de
$\delta=0{,}01$ €. Le prix affiché est donc le vrai prix, arrondi. Cet arrondi est-il négligeable
quand on mesure la volatilité ?

**① Le modèle du bruit.** L'erreur d'arrondi est, par construction, comprise entre $-\delta/2$ et
$+\delta/2$, sans raison de privilégier une valeur :

$$\tilde P_t=P_t+U_t,\qquad U_t\sim\mathcal U\!\left(-\tfrac\delta2,\tfrac\delta2\right)
\ \text{i.i.d., indépendants de } P_t$$

C'est l'archétype de l'usage de l'uniforme : **on ne sait rien de l'erreur, sauf ses bornes.**

**② Le calcul de base.** Par le § 6d.2, avec une étendue $b-a=\delta$ :

$$E(U_t)=0,\qquad
\operatorname{Var}(U_t)=\frac{\delta^2}{12}=\frac{10^{-4}}{12}=8{,}33\times10^{-6}
\qquad\Longrightarrow\qquad
\sigma_U=\frac{\delta}{\sqrt{12}}=0{,}00289\ \text{€}$$

Un tiers de centime. **Sur le prix lui-même, c'est dérisoire** : $0{,}00289/50=0{,}0058\,\%$.

**③ Le passage aux rendements — là où le bruit se réveille.** Le rendement mesuré est

$$\tilde r_t=\log\tilde P_t-\log\tilde P_{t-1}\approx r_t+\frac{U_t-U_{t-1}}{P}$$

Les trois termes étant indépendants, les variances s'ajoutent
([§ 4.2](04-covariance-et-correlation.md)) — et **le bruit compte deux fois**, une par extrémité :

$$\operatorname{Var}(\tilde r_t)=\sigma^2+\frac{2\operatorname{Var}(U)}{P^2}
=\sigma^2+\frac{\delta^2}{6P^2}
=\sigma^2+6{,}67\times10^{-9}$$

L'écart-type ajouté vaut $\sqrt{6{,}67\times10^{-9}}=8{,}2\times10^{-5}$, soit
**0,0082 % par observation** — un nombre fixe, qui ne dépend pas de la fréquence.

**④ Le verdict dépend de la fréquence d'échantillonnage.** C'est tout l'intérêt du calcul :

| Fréquence | $\sigma$ vraie | $\delta^2/(6P^2)$ rapporté à $\sigma^2$ | Volatilité surestimée de |
|---|---|---|---|
| **Quotidienne** | 1,40 % | $0{,}003\,\%$ | $+0{,}002\,\%$ — négligeable |
| **1 minute** | 0,05 % | $2{,}7\,\%$ | $+1{,}3\,\%$ |
| **1 seconde** (≈ 0,006 %) | 0,006 % | $185\,\%$ | $+69\,\%$ — le bruit domine |

> ⚠️ **La volatilité vraie décroît avec l'horizon ; le bruit d'arrondi, non.** En $\sqrt{\Delta t}$
> pour la première, constant pour le second : il existe donc une fréquence en dessous de laquelle
> **on ne mesure plus que l'arrondi**. C'est le problème dit du *bruit de microstructure*, et
> $(b-a)^2/12$ en donne le montant exact.

**⑤ La signature qui trahit le bruit.** Le terme $U_t$ apparaît dans $\tilde r_t$ (avec le
signe $+$) **et** dans $\tilde r_{t+1}$ (avec le signe $-$). Ces deux rendements successifs sont
donc **négativement corrélés**, alors même que les vrais rendements ne le sont pas :

$$\operatorname{Cov}(\tilde r_t,\tilde r_{t+1})=-\frac{\operatorname{Var}(U)}{P^2}
=-3{,}33\times10^{-9}
\qquad\Longrightarrow\qquad
\rho_1=\frac{-3{,}33\times10^{-9}}{2{,}57\times10^{-7}}=-1{,}3\,\%\ \text{en 1 minute}$$

contre $-0{,}002\,\%$ en quotidien. **Une autocorrélation d'ordre 1 légèrement négative sur des
données haute fréquence n'est donc pas un signal de retournement** : c'est un artefact d'arrondi,
et le module 6d permet de le chiffrer avant de bâtir une stratégie dessus.

**⑥ Ce qu'on en fait.** Deux corrections, selon le contexte : échantillonner moins souvent (la
solution du gérant), ou **retrancher le biais connu** $\delta^2/(6P^2)$ de la variance mesurée (la
solution de l'économètre). Dans les deux cas, c'est le $12$ du § 6d.2 qui fournit le nombre.

---

## 6d.6 Simulation

### S6d.1 — Les moments, la f.c., la transformation inverse et le bruit d'arrondi

```python
import numpy as np

rng = np.random.default_rng(6)
N = 1_000_000
a, b = 2.0, 5.0
X = rng.uniform(a, b, N)

print(f"E(X)   = {X.mean():.4f}   theorie (a+b)/2   = {(a+b)/2:.4f}")
print(f"Var(X) = {X.var():.4f}   theorie (b-a)^2/12 = {(b-a)**2/12:.4f}")

# tous les moments de U(0,1) valent 1/(m+1)  (§ 6d.3)
U = rng.random(N)
print("\nmoments de U(0,1), empirique contre 1/(m+1) :")
for m in (1, 2, 3, 4):
    print(f"  m={m} : {(U**m).mean():.4f}   theorie {1/(m+1):.4f}")

# la fonction caracteristique
for t in (0.5, 2.0):
    emp = np.mean(np.exp(1j * t * U))
    the = (np.exp(1j * t) - 1) / (1j * t)
    print(f"t={t}: phi empirique = {emp:+.4f}   theorie (e^(it)-1)/(it) = {the:+.4f}")

# transformation inverse : fabriquer une exponentielle a partir d'uniformes
lam = 4.2
T = -np.log(1 - rng.random(N)) / lam
print(f"\ntransformation inverse : E(T) = {T.mean():.4f}   theorie 1/lambda = {1/lam:.4f}")
print(f"                          P(T>0.5) = {(T > 0.5).mean():.4f}"
      f"   theorie e^(-lambda/2) = {np.exp(-lam/2):.4f}")

# le § 6d.5 : arrondi au centime sur un prix a 50 EUR, rendements 1 minute
# (4000 seances independantes de 500 minutes : le prix reste au voisinage de 50)
P0, d, sigma, M, L = 50.0, 0.01, 5e-4, 4_000, 500
vrai = P0 * np.exp(np.cumsum(rng.normal(0, sigma, (M, L)), axis=1))
cote = np.round(vrai / d) * d                  # le prix tel qu'il est affiche
r_vrai = np.diff(np.log(vrai), axis=1)
r_cote = np.diff(np.log(cote), axis=1)
print(f"\nvar(r) vraie = {r_vrai.var():.3e}")
print(f"var(r) cotee = {r_cote.var():.3e}   theorie + d^2/(6 P^2)"
      f" = {r_vrai.var() + d**2/(6*P0**2):.3e}")
rho1 = np.corrcoef(r_cote[:, :-1].ravel(), r_cote[:, 1:].ravel())[0, 1]
print(f"rho_1 cotee  = {rho1:+.4f}   theorie -(d^2/12)/(P^2 var) ="
      f" {-(d**2/12)/P0**2/r_cote.var():+.4f}")
```

La dernière partie est la plus instructive : **on n'a rien ajouté au signal, on a seulement
arrondi**, et l'autocorrélation d'ordre 1 devient négative — environ $-1{,}4\,\%$, tout près de
la prédiction $-1{,}3\,\%$ du § 6d.5. Refaites tourner avec `sigma = 0.014` (quotidien) : elle
disparaît dans le bruit d'estimation.

> ⚠️ **Le modèle « bruit uniforme additif » est une approximation de l'arrondi.** L'erreur
> d'arrondi a bien la loi $\mathcal U(-\delta/2,\delta/2)$ et la bonne variance, mais elle est une
> **fonction déterministe** du prix, donc pas rigoureusement indépendante de lui. La variance
> prédite tombe très juste ; il reste un écart de quelques pour cent sur l'autocorrélation, et il
> vient de là. C'est la bonne façon de mesurer la portée d'un modèle : le confronter à ce qu'il
> prétend décrire.

⚠️ **Le découpage en 4 000 trajectoires courtes n'est pas cosmétique.** Sur une seule trajectoire
de 2 millions de pas, le prix s'éloigne durablement de 50 € ; comme le bruit relatif vaut
$\delta/P$, la variance ajoutée n'est plus celle du § 6d.5. La formule
$\delta^2/(6P^2)$ suppose **un prix stable au voisinage de $P$** — hypothèse vraie à l'échelle
d'une séance, fausse à l'échelle d'une décennie.

---

## 6d.7 Exercices

**E6d.1.** Retrouver $E(X)$ et $\operatorname{Var}(X)$ pour $\mathcal U(a,b)$ en partant de
$X=a+(b-a)U$ et des seuls résultats sur $\mathcal U(0,1)$. *Combien d'intégrales avez-vous
calculées ?*

**E6d.2.** Déduire de $E(U^m)=1/(m+1)$ le kurtosis de $\mathcal U(-\tfrac12,\tfrac12)$ et
vérifier $\beta_2=1{,}8$. *Pourquoi une loi « sans queues » a-t-elle un kurtosis inférieur à 3 ?*

**E6d.3.** Montrer que $\varphi_{\mathcal U(-c,c)}(t)=\sin(ct)/(ct)$, puis retrouver
$\operatorname{Var}=c^2/3$ par le développement en série de $\sin$. *Vérifier la cohérence avec
$(b-a)^2/12$.*

**E6d.4.** Écrire la transformation inverse pour la loi de **Cauchy**, dont
$F(x)=\tfrac12+\tfrac1\pi\arctan x$. *En déduire un générateur en une ligne, et vérifier par
simulation que la moyenne empirique ne converge vers rien
([§ 13.1](13-portee-et-limites-du-tcl.md)).*

**E6d.5.** Un modèle de VaR produit chaque jour une prévision $F_t$. Sur 250 jours, on calcule
$u_t=F_t(r_t)$ et l'on observe que 22 valeurs dépassent 0,95. *Sous un modèle correct, quelle est
la loi du nombre de dépassements ? Ce 22 est-il compatible ?* (Piste : PIT + module 6b — et
c'est exactement le test de Kupiec des régulateurs bancaires.)

---

## 6d.8 À retenir

- **$E(X)=\dfrac{a+b}{2}$, $\operatorname{Var}(X)=\dfrac{(b-a)^2}{12}$** — soit un écart-type de
  $0{,}289\,(b-a)$ : c'est le chiffre du bruit d'arrondi.
- **$\varphi_U(t)=\dfrac{e^{it}-1}{it}$**, dont le développement en série donne **tous** les
  moments d'un coup : $E(U^m)=1/(m+1)$. Développer vaut mieux que dériver.
- ⭐ **Transformation inverse** : $F^{-1}(U)$ a pour loi $F$. Toute simulation du cours en
  descend.
- ⭐ **PIT** : $F(X)\sim\mathcal U(0,1)$ si $F$ est continue. C'est le contrôle de modèle par
  excellence.
- ⚠️ **L'uniforme n'est pas stable** : la somme de deux uniformes est triangulaire.
- **Kurtosis $1{,}8$, asymétrie nulle** : la loi la plus « facile » pour le TCL — $n=5$ suffit.

---

⬅️ [Module 6c — La loi de Poisson](06c-loi-de-poisson.md) ·
➡️ [Module 6e — La loi exponentielle](06e-loi-exponentielle.md) ·
🏠 [Sommaire](README.md)
