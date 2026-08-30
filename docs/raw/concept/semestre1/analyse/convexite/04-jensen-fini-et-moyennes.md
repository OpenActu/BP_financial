# Module 4 — Jensen fini et les moyennes

**Durée : 1 h.** Prérequis : [module 3](03-criteres-differentiels.md).

> **La question traitée.** Que devient l'inégalité de convexité quand on combine non plus deux
> points, mais $n$ ? Et quelles inégalités classiques en tombent ?

**Ce qui est en jeu.** Ce module est encore **entièrement déterministe** : il n'y est question que
de $n$ nombres et de poids. Toutes les inégalités qu'on y démontre — moyennes, Hölder, Minkowski —
deviendront au [module 5](05-jensen-probabiliste.md) des énoncés sur des espérances, sans une
ligne de calcul supplémentaire.

---

## 4.1 L'inégalité de Jensen finie

> **Théorème (Jensen, forme finie).** Soit $f$ convexe sur un intervalle $I$, soient
> $x_1,\dots,x_n\in I$ et $\lambda_1,\dots,\lambda_n\ge0$ avec $\sum_i\lambda_i=1$. Alors
> $$\boxed{\;f\Big(\sum_{i=1}^n\lambda_i x_i\Big)\;\le\;\sum_{i=1}^n\lambda_i f(x_i)\;}$$
> Si $f$ est **strictement** convexe, l'égalité a lieu **si et seulement si** tous les $x_i$
> associés à un $\lambda_i>0$ sont égaux.

### Démonstration ① — par la tangente (deux lignes)

Posons $\bar x=\sum_i\lambda_ix_i$, qui appartient à $I$ puisque $I$ est convexe. L'inégalité de
la tangente ([§ 3.3](03-criteres-differentiels.md)) au point $\bar x$ donne, pour chaque $i$ :

$$f(x_i)\;\ge\;f(\bar x)+f'(\bar x)\,(x_i-\bar x).$$

Multiplions par $\lambda_i\ge0$ et sommons. Le terme linéaire disparaît :

$$\sum_i\lambda_i f(x_i)\;\ge\;f(\bar x)+f'(\bar x)\underbrace{\Big(\sum_i\lambda_ix_i-\bar x\Big)}_{=\,0}
=f(\bar x). \qquad\blacksquare$$

> 🔑 **Toute la démonstration tient dans une annulation.** Le terme de premier ordre s'annule
> *parce que* $\bar x$ est la moyenne pondérée — c'est-à-dire exactement le point où le
> « centre de gravité » des écarts est nul. Ce sera mot pour mot la démonstration du
> [§ 5.2](05-jensen-probabiliste.md), avec $E(X)$ à la place de $\bar x$.

### Démonstration ② — par récurrence (sans dérivabilité)

Pour $n=2$, c'est la définition. Supposons le résultat vrai au rang $n-1$ et prenons
$\lambda_n<1$ (sinon il n'y a rien à montrer). Posons $\mu_i=\frac{\lambda_i}{1-\lambda_n}$ pour
$i\le n-1$, de somme 1. Alors

$$f\Big(\sum_{i=1}^n\lambda_ix_i\Big)
=f\Big((1-\lambda_n)\sum_{i=1}^{n-1}\mu_ix_i+\lambda_nx_n\Big)
\;\le\;(1-\lambda_n)\,f\Big(\sum_{i=1}^{n-1}\mu_ix_i\Big)+\lambda_nf(x_n),$$

puis l'hypothèse de récurrence sur le premier terme conclut. $\blacksquare$

> 📐 **Deux démonstrations, deux portées.** La première exige $f$ dérivable mais s'étend
> **directement** aux espérances (module 5) ; la seconde ne suppose rien mais reste confinée aux
> sommes finies. Garder les deux : la version « tangente » est celle qui se généralise, la version
> « récurrence » est celle qui couvre $\lvert x\rvert$ et $\max(0,x)$.

---

## 4.2 Les trois moyennes

Pour $x_1,\dots,x_n>0$ et des poids $\lambda_i$ :

$$\underbrace{\text{HM}=\Big(\sum_i\tfrac{\lambda_i}{x_i}\Big)^{-1}}_{\text{harmonique}}\;\le\;
\underbrace{\text{GM}=\prod_i x_i^{\lambda_i}}_{\text{géométrique}}\;\le\;
\underbrace{\text{AM}=\sum_i\lambda_ix_i}_{\text{arithmétique}}$$

**Démonstration de GM $\le$ AM.** Appliquons Jensen à $f=-\log$, strictement convexe
([§ 3.4](03-criteres-differentiels.md)) :

$$-\log\Big(\sum_i\lambda_ix_i\Big)\;\le\;-\sum_i\lambda_i\log x_i
\;\Longleftrightarrow\;
\log\Big(\sum_i\lambda_ix_i\Big)\;\ge\;\sum_i\lambda_i\log x_i=\log\prod_ix_i^{\lambda_i}.$$

L'exponentielle étant croissante, AM $\ge$ GM, avec **égalité si et seulement si tous les $x_i$
sont égaux** (stricte convexité de $-\log$). $\blacksquare$

**Démonstration de HM $\le$ GM.** Appliquer le résultat précédent à $1/x_i$ et inverser.
$\blacksquare$

### Ce que cela dit d'une série de rendements

Sur cinq périodes de rendements $+12\,\%$, $-8\,\%$, $+25\,\%$, $-15\,\%$, $+6\,\%$, les facteurs
de capitalisation sont $1{,}12$ ; $0{,}92$ ; $1{,}25$ ; $0{,}85$ ; $1{,}06$ :

| Moyenne | Valeur du facteur | Rendement équivalent |
|---|---|---|
| Arithmétique (AM) | 1,040000 | $+4{,}00\,\%$ |
| **Géométrique (GM)** | 1,030216 | $\mathbf{+3{,}02\,\%}$ |
| Harmonique (HM) | 1,020475 | $+2{,}05\,\%$ |

**Le capital réellement obtenu** est le produit des facteurs : $1{,}16049$, soit exactement
$\text{GM}^5$. Capitaliser la moyenne **arithmétique** aurait annoncé $1{,}04^5=1{,}21665$ —
**5,7 points de trop sur cinq périodes**.

> 🔑 **La moyenne arithmétique des rendements n'est pas la performance.** La performance est la
> moyenne **géométrique**, et l'écart entre les deux est garanti par Jensen : il est toujours dans
> le même sens, et il croît avec la dispersion. Le [§ 5.3](05-jensen-probabiliste.md) le chiffre :
> l'écart vaut environ $\sigma^2/2$.

---

## 4.3 Young, Hölder, Minkowski

Trois inégalités qui structurent tout le calcul de normes — et qui sont toutes des Jensen
déguisés.

### Inégalité de Young

Pour $a,b>0$ et $p,q>1$ avec $\frac1p+\frac1q=1$ :

$$ab\;\le\;\frac{a^p}{p}+\frac{b^q}{q}$$

*Démonstration.* Concavité du $\log$ appliquée aux poids $\frac1p,\frac1q$ :
$\log\big(\frac{a^p}p+\frac{b^q}q\big)\ge\frac1p\log a^p+\frac1q\log b^q=\log(ab)$. $\blacksquare$

### Inégalité de Hölder

$$\sum_{i=1}^n\lvert u_iv_i\rvert\;\le\;\Big(\sum_i\lvert u_i\rvert^p\Big)^{1/p}
\Big(\sum_i\lvert v_i\rvert^q\Big)^{1/q}$$

*Démonstration.* Normaliser $u$ et $v$ pour que les deux facteurs de droite valent 1, appliquer
Young terme à terme, sommer : le membre de droite devient $\frac1p+\frac1q=1$. $\blacksquare$

> 🔑 **Le cas $p=q=2$ est Cauchy–Schwarz** — donc $\lvert\rho\rvert\le1$, démontré au
> [module 2 d'algèbre](../../algebre/02-cauchy-schwarz-et-angle.md) par le discriminant. Deux
> chemins, un seul théorème : le discriminant est la trace de la **convexité** de
> $t\mapsto\lVert u+tv\rVert^2$, qui est une parabole de coefficient dominant positif.

### Inégalité de Minkowski — la norme est convexe

$$\Big(\sum_i\lvert u_i+v_i\rvert^p\Big)^{1/p}\le\Big(\sum_i\lvert u_i\rvert^p\Big)^{1/p}
+\Big(\sum_i\lvert v_i\rvert^p\Big)^{1/p}
\qquad\text{c'est-à-dire}\qquad \lVert u+v\rVert_p\le\lVert u\rVert_p+\lVert v\rVert_p$$

C'est l'**inégalité triangulaire**. Jointe à
l'homogénéité$\lVert\alpha u\rVert=\lvert\alpha\rvert \lVert u\rVert$, elle donne :

> **Proposition.** Toute norme est une fonction **convexe**.
> $$\lVert\lambda u+(1-\lambda)v\rVert\le\lambda\lVert u\rVert+(1-\lambda)\lVert v\rVert$$

> 🔑 **Cette proposition est le socle du module 8.** L'écart type d'un portefeuille est une norme
> ([module 8 d'algèbre](../../algebre/08-covariance-et-produit-scalaire.md) : $\Sigma$ est une
> matrice de Gram, donc $\sigma(w)=\sqrt{w^{\top}\Sigma w}$ est la norme d'un vecteur). **Donc
> $\sigma$ est convexe** — et « la diversification ne peut pas augmenter le risque au-delà de la
> moyenne des risques » est un théorème, pas un slogan.

---

## 4.4 Simulation

### S4.1 — Les trois moyennes, et l'écart qui grandit avec la dispersion

```python
import numpy as np

rng = np.random.default_rng(4)

def moyennes(f):                       # f : facteurs de capitalisation, tous > 0
    return f.mean(), np.exp(np.log(f).mean()), 1 / np.mean(1 / f)

r = np.array([0.12, -0.08, 0.25, -0.15, 0.06])
am, gm, hm = moyennes(1 + r)
print(f"AM={am:.6f}  GM={gm:.6f}  HM={hm:.6f}   ordre respecte : {hm <= gm <= am}")
print(f"capital realise = {np.prod(1 + r):.6f}   GM^5 = {gm ** 5:.6f}"
      f"   AM^5 = {am ** 5:.6f}")

# l'ecart AM - GM croit comme la variance
print("\n sigma    AM-GM      sigma^2/2")
for s in (0.05, 0.10, 0.20, 0.40, 0.60):
    x = rng.normal(0, s, 2_000_000)
    f = np.exp(x)                       # facteurs log-normaux, moyenne des log = 0
    am, gm, _ = moyennes(f)
    print(f"{s:5.2f}  {np.log(am) - np.log(gm):8.5f}    {s ** 2 / 2:8.5f}")
```

La seconde partie montre le résultat que le [§ 5.3](05-jensen-probabiliste.md) démontrera :
$\log(\text{AM})-\log(\text{GM})\to\sigma^2/2$. **L'écart n'est pas un artefact de
l'échantillon : c'est une fonction de la volatilité seule.**

### S4.2 — Jensen à $n$ points, et son cas d'égalité

```python
lam = rng.dirichlet(np.ones(6))
x = rng.uniform(0.1, 4.0, 6)
for nom, f in [("exp", np.exp), ("-log", lambda t: -np.log(t)), ("x^2", lambda t: t ** 2)]:
    print(f"{nom:>6} : f(moyenne)={f(lam @ x):10.4f}  <=  moyenne des f={lam @ f(x):10.4f}")

egaux = np.full(6, 2.7)                # tous les x_i egaux -> egalite
print("cas d'egalite :", np.isclose(np.exp(lam @ egaux), lam @ np.exp(egaux)))
```

---

## 4.5 Exercices

**E4.1.** Démontrer Jensen fini par récurrence en détaillant le cas $\lambda_n=1$, puis identifier
l'endroit **exact** où la convexité du domaine est utilisée.

**E4.2.** Démontrer AM $\ge$ GM dans le cas non pondéré ($\lambda_i=1/n$) et écrire l'énoncé
obtenu pour $n=2$ : *que reconnaît-on ?*

**E4.3.** Montrer que la moyenne harmonique est la bonne moyenne pour un **PER** (rapport
cours/bénéfice) agrégé au niveau d'un indice. *(Piste : le PER d'un panier est le rapport de la
somme des capitalisations à la somme des bénéfices.)* En déduire que la moyenne arithmétique des
PER surestime toujours le PER du panier.

**E4.4.** Déduire Cauchy–Schwarz de Hölder, puis retrouver $\lvert\rho\rvert\le1$. *Comparer avec
la démonstration par le discriminant du
[module 2 d'algèbre](../../algebre/02-cauchy-schwarz-et-angle.md) : laquelle donne le cas d'égalité
le plus vite ?*

**E4.5.** Montrer que $w\mapsto\lVert w\rVert_1=\sum_i\lvert w_i\rvert$ est convexe. *(C'est la
pénalité **lasso** ; sa convexité est la raison pour laquelle la sélection de variables par lasso
est un problème convexe, alors que « au plus $k$ variables non nulles » ne l'est pas —
[E1.5](01-ensembles-convexes.md).)*

**E4.6 — orientée finance.** Sur une série de rendements quotidiens obtenue avec
`import_societe.py` :
1. calculer AM et GM des facteurs $1+r_t$ et vérifier l'ordre ;
2. comparer $\text{GM}^n$ au rapport $P_{\text{fin}}/P_{\text{début}}$ — que constatez-vous ?
3. vérifier que $\log(\text{AM})-\log(\text{GM})\approx\hat\sigma^2/2$.

---

## 4.6 À retenir

- **Jensen fini** : $f\big(\sum\lambda_ix_i\big)\le\sum\lambda_if(x_i)$ pour des poids
  $\lambda_i\ge0$ de somme 1. Deux démonstrations : par la **tangente** (qui se généralisera aux
  espérances) et par **récurrence** (qui n'exige aucune dérivabilité).
- **Égalité $\iff$ tous les $x_i$ égaux**, dès que $f$ est strictement convexe. C'est ce cas
  d'égalité qui rendra les inégalités du module 5 **utilisables** : on saura quand l'écart est nul.
- ⭐ **HM $\le$ GM $\le$ AM**, par $-\log$ : la performance réalisée d'une série de rendements est
  la moyenne **géométrique**, jamais l'arithmétique.
- **Young $\Rightarrow$ Hölder $\Rightarrow$ Minkowski** : trois Jensen enchaînés, dont le cas
  $p=q=2$ est Cauchy–Schwarz.
- ⭐ **Toute norme est convexe.** L'écart type d'un portefeuille en étant une, la diversification
  ne peut jamais faire pire que la moyenne pondérée des risques.

---

⬅️ [Module 3 — Les critères différentiels](03-criteres-differentiels.md) ·
➡️ [Module 5 — Jensen probabiliste](05-jensen-probabiliste.md) ·
🏠 [Sommaire](README.md)
