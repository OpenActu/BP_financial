# Module 12 — Le théorème central limite : énoncé et démonstration ⭐

**Durée : 2 h.** Prérequis : modules [5](05-fonction-generatrice-des-moments.md) à
[7](07-loi-normale-et-ses-transformees.md), et le
[module 11 bis](11bis-convergence-en-loi.md) pour la notation $\xrightarrow{\mathcal L}$.

> **La question traitée.** Énoncer le TCL précisément, puis le **démontrer** — la démonstration
> étant ce qui rend chaque hypothèse lisible. Puis dire sur quoi il porte exactement : la loi des
> $X_i$, ou celle de $\bar X$ ?

---

## 12.1 Le problème que le TCL résout

Le [module 8](08-addition-de-lois-et-stabilite-gaussienne.md) a établi

$$\bar X\sim\mathcal N\!\left(\mu,\frac{\sigma^2}{n}\right)$$

**exactement**, parce que les $X_i$ étaient supposés **gaussiens**. Mais qui a jamais vérifié
qu'un rendement boursier, une durée de service, un montant de facture ou un nombre de clients
était gaussien ? Aucune de ces grandeurs ne l'est.

Sans un résultat supplémentaire, l'inférence des [modules 17 à 19](17-estimation-et-quantite-pivotale.md)
serait donc restreinte au cas — rarissime — où l'on sait la loi des données gaussienne.

> 🔑 **Le TCL est ce résultat supplémentaire.** Il affirme que la loi de $\bar X$ devient
> gaussienne quand $n$ grandit, **quelle que soit la loi des $X_i$**. C'est ce qui fait passer
> les méthodes de ce cours du statut de curiosité à celui d'outil universel.

---

## 12.2 Énoncé précis

> **Théorème central limite (Lindeberg–Lévy).**
> Soient $X_1, X_2,\dots$ des variables aléatoires **indépendantes**, de **même loi**, admettant
> une espérance $\mu=E(X_1)$ et une variance **finie et non nulle** $\sigma^2=\operatorname{Var}(X_1)$.
> Alors
> $$\frac{\bar X_n-\mu}{\sigma/\sqrt n}\;=\;\frac{\sum_{i=1}^n X_i-n\mu}{\sigma\sqrt n}
> \;\xrightarrow[n\to\infty]{\;\mathcal L\;}\;\mathcal N(0,1),$$
> c'est-à-dire : pour tout $x\in\mathbb R$,
> $$P\!\left(\frac{\bar X_n-\mu}{\sigma/\sqrt n}\le x\right)\;\xrightarrow[n\to\infty]{}\;\Phi(x).$$

### Chaque hypothèse compte

| Hypothèse              | Ce qu'elle interdit                                     | Que se passe-t-il sans elle                   |
| ---------------------- | ------------------------------------------------------- | --------------------------------------------- |
| **Indépendance**       | Séries chronologiques, mesures répétées, grappes        | [Module 14](14-dependance-et-echec-du-tcl.md) — **c'est le cas grave** |
| **Même loi**           | Populations hétérogènes                                 | Relâchable : Lindeberg–Feller ([§ 13.5](13-portee-et-limites-du-tcl.md)) |
| **Variance finie**     | Cauchy, lois $\alpha$-stables, certaines queues lourdes | Aucun TCL — autre normalisation, autre limite |
| **Variance non nulle** | Variable constante                                      | Cas dégénéré, sans intérêt                    |

> ℹ️ La flèche $\xrightarrow{\mathcal L}$ et la ligne qui la traduit en termes de fonctions de
> répartition sont définies au [§ 11bis.2](11bis-convergence-en-loi.md). Ici la limite $\Phi$ est
> **continue**, donc la convergence porte sur tout $\mathbb R$ — sans exception à ménager.

⚠️ Notez ce qui **n'est pas** dans la liste : aucune hypothèse sur la **forme** de la loi. Elle
peut être discrète, asymétrique, bornée, multimodale — cela n'a aucune importance pour la
validité asymptotique.

➡️ Le § 12.3 montre à quelle **ligne exacte** de la démonstration chacune de ces hypothèses
intervient — et pourquoi la forme de la loi, elle, n'y apparaît nulle part.

### La normalisation par $\sqrt n$

Elle n'est pas arbitraire. $\operatorname{Var}(\bar X_n)=\sigma^2/n$ tend vers 0 : sans
renormalisation, $\bar X_n$ converge vers la constante $\mu$ (c'est la **loi des grands
nombres**), et la loi limite serait dégénérée — un point, sans information.

Diviser par $\sigma/\sqrt n$ **fixe l'échelle** : la variable standardisée a une variance de 1
pour tout $n$. Le TCL décrit ce qui reste quand on regarde les fluctuations **à la bonne
loupe** — celle qui grossit d'un facteur $\sqrt n$.

> 🔑 Loi des grands nombres et TCL sont **complémentaires** : la première dit *où* $\bar X_n$ va
> (vers $\mu$), le second dit *à quelle vitesse* et *sous quelle forme* il y va
> (en $1/\sqrt n$, gaussiennement).

---

## 12.3 La démonstration

Elle tient en quatre étapes et mérite d'être lue pour une raison précise : **elle rend chaque
hypothèse visible**. On y voit la ligne exacte où sert l'indépendance, la ligne exacte où sert la
variance finie, et l'endroit où la forme de la loi disparaît du calcul.

### L'outil

C'est la **fonction caractéristique** du [module 6](06-fonction-caracteristique.md), et non la
FGM du module 5 — pour la raison exposée au [§ 5.5](05-fonction-generatrice-des-moments.md) :
$E(e^{tX})$ peut être infinie pour tout $t>0$, comme sur une log-normale, alors que
$E(e^{itX})$ existe toujours. **Un théorème qui prétend valoir quelle que soit la loi ne peut pas
reposer sur un outil qui n'existe pas toujours.**

On utilisera les propriétés (P1) à (P4) du [§ 6.2](06-fonction-caracteristique.md) et le
**théorème de continuité de Lévy** du [§ 6.3](06-fonction-caracteristique.md).

### La démonstration proprement dite

**Étape 0 — standardiser.** Posons $Y_i=\dfrac{X_i-\mu}{\sigma}$ : les $Y_i$ sont i.i.d., centrées,
de variance 1 *(c'est ici, et uniquement ici, que sert $\sigma^2\neq 0$)*. La quantité à étudier
s'écrit

$$Z_n=\frac{\bar X_n-\mu}{\sigma/\sqrt n}=\frac{1}{\sqrt n}\sum_{i=1}^n Y_i .$$

Il suffit donc de prouver $\varphi_{Z_n}(t)\to e^{-t^2/2}$ pour tout $t$.

**Étape 1 — l'indépendance transforme la somme en produit.** Par (P3) puis (P2) :

$$\varphi_{Z_n}(t)=E\!\left(e^{\,i\frac{t}{\sqrt n}\sum_i Y_i}\right)
=\prod_{i=1}^{n}E\!\left(e^{\,i\frac{t}{\sqrt n}Y_i}\right)
=\left[\varphi_Y\!\left(\frac{t}{\sqrt n}\right)\right]^{n}$$

⬅️ **L'indépendance sert exactement ici** (l'espérance du produit devient le produit des espérances),
et l'hypothèse de **même loi** juste après (les $n$ facteurs sont identiques, d'où la puissance).

**Étape 2 — la variance finie autorise le développement.** À $t$ **fixé**, $t/\sqrt n\to 0$ : on est
au voisinage de 0, là où (P4) s'applique. Avec $E(Y)=0$ et $E(Y^2)=1$ :

$$\varphi_Y\!\left(\frac{t}{\sqrt n}\right)=1-\frac{t^2}{2n}+o\!\left(\frac1n\right)$$

⬅️ **La variance finie sert exactement ici**, et nulle part ailleurs.

**Étape 3 — passer à la limite.** On utilise le lemme classique : si $c_n\to c$ dans $\mathbb C$,
alors $\left(1+\frac{c_n}{n}\right)^{n}\to e^{c}$. Ici $c_n=-\frac{t^2}{2}+o(1)\to-\frac{t^2}{2}$, donc

$$\varphi_{Z_n}(t)\;\xrightarrow[n\to\infty]{}\;e^{-t^2/2}\qquad\text{pour tout }t\in\mathbb R .$$

**Étape 4 — conclure.** $e^{-t^2/2}$ est la fonction caractéristique de $\mathcal N(0,1)$
([§ 7.3](07-loi-normale-et-ses-transformees.md)), et elle est continue en 0 : le théorème de Lévy
donne $Z_n\xrightarrow{\mathcal L}\mathcal N(0,1)$. $\blacksquare$

### Où sert chaque hypothèse — le tableau qui résume tout

| Hypothèse | Étape | Ce qui casse sans elle |
|---|---|---|
| **Variance non nulle** | 0 — standardisation | Division par 0 : rien à normaliser |
| **Indépendance** | 1 — $E(\prod)=\prod E$ | La factorisation tombe, et **rien ne la remplace** ([module 14](14-dependance-et-echec-du-tcl.md)) |
| **Même loi** | 1 — puissance $n$-ième | Le produit reste, mais ses facteurs diffèrent : Lindeberg–Feller |
| **Variance finie** | 2 — DL d'ordre 2 | Plus de terme en $t^2$ : autre normalisation, autre limite |

### La variante par la FGM — plus simple, mais insuffisante

Quand $M_Y(t)=E(e^{tY})$ existe au voisinage de 0, la même mécanique se lit en calcul **réel** :

$$\log M_{Z_n}(t)=n\log M_Y\!\left(\frac{t}{\sqrt n}\right)
=n\left(\frac{t^2}{2n}+o\!\left(\frac1n\right)\right)\longrightarrow\frac{t^2}{2}$$

soit $M_{Z_n}(t)\to e^{t^2/2}$, la FGM de $\mathcal N(0,1)$.

> ⚠️ **Ce n'est pas une démonstration du théorème**, seulement du cas où la FGM existe. La
> log-normale a une variance finie — le TCL s'y applique, le
> [§ 13.2](13-portee-et-limites-du-tcl.md) le vérifie numériquement — et pourtant sa FGM est
> infinie pour tout $t>0$. Utile pour comprendre le mécanisme, hors sujet pour conclure.

---

## 12.4 La lecture en cumulants

Reprenons les cumulants du [§ 6.4](06-fonction-caracteristique.md), $K_Y(t)=\log\varphi_Y(t)$.
L'étape 1 dit $K_{Z_n}(t)=n\,K_Y\!\left(t/\sqrt n\right)$, d'où immédiatement

$$\boxed{\;\kappa_j(Z_n)=\frac{\kappa_j(Y)}{n^{\,j/2-1}}\;}$$

| $j$ | 1 | 2 | 3 | 4 | $\ge 3$ |
|---|---|---|---|---|---|
| $\kappa_j(Z_n)$ | 0 | 1 | $\gamma_1/\sqrt n$ | $\kappa_4/n$ | $\to 0$ |

Trois choses se lisent d'un coup :

- $j=2$ est **invariant** : c'est ce que la normalisation en $\sqrt n$ était chargée de fixer ;
- $j=3$ donne **exactement** la formule $\gamma_1(\bar X_n)=\gamma_1(X)/\sqrt n$ qui gouvernera
  toute la [qualité de l'approximation](13-portee-et-limites-du-tcl.md) — elle n'est donc pas un
  résultat annexe, mais le premier terme que la démonstration écrase ;
- tous les cumulants d'ordre $\ge 3$ s'effacent, et la gaussienne est **l'unique loi** dont ils sont
  tous nuls. La limite ne pouvait être qu'elle.

> 🔑 En une phrase : **le TCL est l'effacement de tous les cumulants d'ordre $\ge 3$**, à la vitesse
> $n^{1-j/2}$. Le plus lent d'entre eux — l'asymétrie, en $1/\sqrt n$ — est celui qui gouverne la
> qualité de l'approximation à $n$ fini.

---

## 12.5 Quatre choses que la démonstration explique

**① Pourquoi la forme de la loi ne compte pas.** Tout ce que la loi des $X_i$ apporte au calcul tient
dans **deux nombres** : $E(Y)=0$ et $E(Y^2)=1$ après standardisation. Asymétrie, kurtosis, caractère
discret ou borné, multimodalité — rien de tout cela n'apparaît nulle part ; c'est parti dans le
$o(1/n)$ de l'étape 2. C'est la justification formelle du ⚠️ du § 12.2.

**② Pourquoi $\sqrt n$, et pas autre chose.** La normalisation est **dictée par l'exposant 2** du
développement : pour que $n$ facteurs valant $1-\frac{c\,t^2}{2n}$ donnent une limite non triviale,
il faut que le terme d'ordre 2 soit en $1/n$, donc que l'échelle soit en $1/\sqrt n$. Si la variance
est infinie et que la loi est $\alpha$-stable, le développement commence par $1-c|t|^\alpha$ : la
normalisation devient $n^{1/\alpha}$ et la limite $e^{-c|t|^\alpha}$, une loi stable.

**③ Pourquoi la dépendance est le cas grave.** L'indépendance n'intervient qu'une fois, mais elle
porte **toute** la démonstration : sans elle, $\varphi_{Z_n}$ n'est plus un produit et il n'y a plus
de calcul du tout. C'est l'objet du [module 14](14-dependance-et-echec-du-tcl.md).

**④ Pourquoi l'énoncé est asymptotique et jamais chiffré.** Le $o(1/n)$ de l'étape 2 n'est contrôlé
par **rien** : (P4) en garantit l'existence, pas la taille. Deux lois de mêmes moyenne et variance
peuvent avoir des restes d'ordres de grandeur très différents. Chiffrer exige un **moment
supplémentaire** : c'est exactement ce que demande
[Berry–Esseen](13-portee-et-limites-du-tcl.md).

---

## 12.6 Sur quoi le TCL porte exactement

> **Le TCL porte-t-il sur la loi des $X_i$ ou sur celle de $\bar X$ ?**

**Sur celle de $\bar X$**, exclusivement — et plus précisément sur celle de $\bar X$
**standardisée**.

**La loi des $X_i$ ne change jamais.** Elle est ce qu'elle est : si vous tirez des variables
exponentielles, elles restent exponentielles, que $n$ vaille 5 ou 5 millions. Le TCL ne
« normalise » rien du tout — il décrit le comportement d'une **fonction** des données, la moyenne.

### L'erreur à ne surtout pas commettre

> ❌ « Grâce au TCL, mes données deviennent normales quand $n$ est grand. »

C'est faux et cela a des conséquences concrètes. Deux illustrations :

- Un histogramme de 10 000 rendements quotidiens ne ressemblera **pas** à une gaussienne : il
  restera à queues épaisses. Ce qui devient gaussien, c'est la loi de la **moyenne** de ces
  rendements — un objet qu'on n'observe qu'une fois.
- Un test de normalité (Shapiro–Wilk) appliqué aux données **rejettera de plus en plus
  massivement** à mesure que $n$ grandit, alors même que le TCL rend l'inférence sur la moyenne
  de plus en plus valide. Les deux ne parlent pas du même objet.

### La bonne formulation en une phrase

> Le TCL ne rend pas les données normales ; il rend **la moyenne** des données approximativement
> normale — et c'est suffisant, car toutes les procédures de ce cours ne dépendent des données
> qu'à travers leur moyenne.

Cette dernière proposition est la clé : $\bar X$, $S^2$, une pente de régression sont tous des
**moyennes** (la variance est une moyenne de carrés, la pente une moyenne pondérée). C'est
pourquoi le TCL protège l'ensemble de l'édifice.

---

## 12.7 Simulations

### S12.1 — Voir la convergence, et voir ce qui ne converge pas

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(11)
N = 200_000
MU, SG = 1.0, 1.0                      # exponentielle de paramètre 1

fig, axes = plt.subplots(2, 4, figsize=(15, 6))
for j, n in enumerate((1, 5, 30, 200)):
    X = rng.exponential(1.0, size=(N, n))
    Z = (X.mean(axis=1) - MU) / (SG / np.sqrt(n))
    axes[0, j].hist(Z, bins=200, range=(-4, 4), density=True, alpha=.45)
    g = np.linspace(-4, 4, 400)
    axes[0, j].plot(g, stats.norm.pdf(g), "k")
    axes[0, j].set_title(f"moyenne standardisée, n={n}")
    # ⚠️ la ligne du bas : la loi des DONNÉES, qui ne bouge pas
    axes[1, j].hist(X[:, 0], bins=200, range=(0, 6), density=True, alpha=.45, color="tab:red")
    axes[1, j].set_title("loi des $X_i$ — inchangée")
plt.tight_layout(); plt.show()
```

**Le point de la figure est la ligne du bas.** Elle est strictement identique dans les quatre
colonnes : la loi des données ne se normalise jamais. Seule la ligne du haut converge.

### S12.2 — La démonstration à l'œuvre : voir converger la fonction caractéristique

Aucun tirage aléatoire ici — le calcul est **exact**. Pour une exponentielle centrée réduite,
$\varphi_Y(t)=\dfrac{e^{-it}}{1-it}$, et l'étape 1 donne
$\varphi_{Z_n}(t)=\left[\varphi_Y(t/\sqrt n)\right]^n$.

```python
def phi_Zn(t, n):                              # exponentielle(1) centrée réduite
    u = t / np.sqrt(n)
    return (np.exp(-1j * u) / (1 - 1j * u)) ** n

t = np.linspace(-8, 8, 4001)
cible = np.exp(-t**2 / 2)
for n in (1, 5, 30, 200, 5000):
    e = np.abs(phi_Zn(t, n) - cible)
    print(f"n={n:>5} : ecart max={e.max():.4f} atteint en t={t[e.argmax()]:+.2f}"
          f"   ecart x sqrt(n) = {e.max() * np.sqrt(n):.3f}")

# contre-épreuve : sur une loi en réseau, la convergence n'est PAS uniforme
p, sg = 0.05, np.sqrt(0.05 * 0.95)
for n in (30, 200, 5000):
    u = 2 * np.pi * sg                          # ici u/sg = 2*pi : le facteur revient à 1
    phi = (np.exp(-1j * p * u / sg) * (1 - p + p * np.exp(1j * u / sg))) ** n
    t0 = u * np.sqrt(n)
    print(f"Bernoulli n={n:>5} : |phi_Zn({t0:6.2f})| = {abs(phi):.3f}"
          f"   cible = {np.exp(-t0**2 / 2):.1e}")
```

| $n$ | 1 | 5 | 30 | 200 | 5000 |
|---|---|---|---|---|---|
| Écart max à $e^{-t^2/2}$ | 0,3791 | 0,1736 | 0,0707 | 0,0273 | 0,0055 |
| Écart $\times\sqrt n$ | 0,379 | 0,388 | 0,387 | 0,387 | **0,386** |

**Trois lectures.**

- **L'écart décroît exactement en $1/\sqrt n$** — le produit par $\sqrt n$ est constant à la
  troisième décimale. C'est la vitesse de [Berry–Esseen](13-portee-et-limites-du-tcl.md), et pour
  la raison qu'on a vue au § 12.4 : le premier terme négligé à l'étape 2 est le cumulant
  $\kappa_3(Z_n)=\gamma_1/\sqrt n$.
- **Le maximum est atteint vers $|t|\approx 1{,}7$** (2,1 à $n=1$), jamais en 0 — où les deux
  fonctions valent 1 par construction. Regarder l'approximation au voisinage de 0 ne renseigne
  sur rien.
- **La contre-épreuve Bernoulli est le point important.** En $t=2\pi\sigma\sqrt n$, le module de
  $\varphi_{Z_n}$ revient **exactement à 1**, alors que la cible y vaut $10^{-13}$, puis
  $10^{-82}$, puis 0. La convergence de l'étape 3 est **simple, jamais uniforme sur $\mathbb R$** :
  le point de désaccord existe toujours, il s'éloigne seulement à l'infini quand $n$ grandit.
  C'est la signature analytique de la discrétisation, et la raison pour laquelle le TCL ne dit
  rien des queues extrêmes ([§ 13.1](13-portee-et-limites-du-tcl.md)).

---

## 12.8 Exercices

**E12.1.** Énoncer le TCL de mémoire, avec **toutes** ses hypothèses. Pour chacune, donner un
contre-exemple où sa violation invalide la conclusion.

**E12.2.** Refaire l'étape 1 en détaillant l'usage de (P2) et (P3). *À quel moment exact
l'hypothèse « même loi » est-elle utilisée ?*

**E12.3.** La loi de Cauchy standard a pour fonction caractéristique $\varphi(t)=e^{-|t|}$.
Calculer $\varphi_{\bar X_n}$ et en déduire en **une ligne** que la moyenne de $n$ Cauchy est une
Cauchy. Puis identifier l'étape exacte du § 12.3 qui échoue, et dire pourquoi le lemme
$\left(1+\frac{c_n}{n}\right)^n\to e^{c}$ ne peut pas s'appliquer ici.

**E12.4.** Démontrer $\gamma_1(\bar X_n)=\gamma_1(X)/\sqrt n$ pour des $X_i$ i.i.d.
*Indication : le moment centré d'ordre 3 d'une somme d'indépendantes est la somme des moments
centrés d'ordre 3. Retrouver ensuite le résultat par le § 12.4.*

**E12.5.** Expliquer, en s'appuyant sur l'étape 2, pourquoi une loi bornée et une loi à queue
lourde de mêmes moyenne et variance ne convergent pas à la même vitesse. *Quelle quantité, absente
de l'énoncé, fait la différence ?*

**E12.6 — orientée finance.** Sur une série de rendements quotidiens obtenue avec
`import_societe.py` :
1. tracer l'histogramme des rendements, puis celui des moyennes sur 5, 20 et 60 séances ;
2. estimer l'asymétrie et le kurtosis de chacun, et vérifier la règle en $1/\sqrt n$ ;
3. dire lequel des deux histogrammes le TCL prétend normaliser.

---

## 12.9 À retenir

- **Énoncé** : $X_i$ i.i.d., **indépendantes**, variance **finie** non nulle
  $\Rightarrow \frac{\bar X_n-\mu}{\sigma/\sqrt n}\xrightarrow{\mathcal L}\mathcal N(0,1)$.
- Il porte sur la loi de **$\bar X$ standardisée**, jamais sur celle des $X_i$ — qui ne change
  pas. Le TCL **ne normalise pas les données**.
- **La démonstration** tient en deux gestes : l'indépendance transforme la somme en **produit**
  de fonctions caractéristiques, la variance finie autorise le **DL d'ordre 2** de chaque
  facteur — et $\left[1-\frac{t^2}{2n}+o(1/n)\right]^n\to e^{-t^2/2}$.
- Elle explique tout le reste : seuls les **deux premiers moments** survivent au calcul (d'où
  l'indifférence à la forme de la loi), les cumulants d'ordre $j\ge 3$ s'effacent en
  $n^{1-j/2}$ (d'où $\gamma_1(\bar X_n)=\gamma_1(X)/\sqrt n$), et le reste $o(1/n)$ n'est
  contrôlé par rien (d'où un énoncé asymptotique, jamais chiffré).

---

⬅️ [Module 11 bis — La convergence en loi](11bis-convergence-en-loi.md) ·
➡️ [Module 13 — Portée et limites du TCL](13-portee-et-limites-du-tcl.md) ·
🏠 [Sommaire](README.md)
