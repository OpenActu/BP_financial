# Module 5 — La fonction génératrice des moments

**Durée : 1 h.** Prérequis : modules [1](01-variable-aleatoire-et-loi.md) à
[4](04-covariance-et-correlation.md) — en particulier le **théorème de transfert**
([§ 2.3](02-esperance.md)), dont ce module n'est qu'une application, et
$E(XY)=E(X)E(Y)$ sous indépendance ([§ 2.4](02-esperance.md)), qui en est le moteur.

> **La question traitée.** Comment ramener l'étude d'une **somme** de variables aléatoires
> indépendantes — objet difficile, dont la loi est une convolution — à un simple **produit** de
> fonctions ?

**Ce qui est en jeu.** C'est l'outil qui rend démontrables la stabilité gaussienne
([module 8](08-addition-de-lois-et-stabilite-gaussienne.md)) et, dans sa version complexe, le
théorème central limite ([module 12](12-theoreme-central-limite.md)). Ce module en établit le
mécanisme et — tout aussi important — **ses limites**.

---

## 5.1 Définition

> **Définition.** La **fonction génératrice des moments** (FGM) de $X$ est
> $$M_X(t)=E\!\left(e^{tX}\right),\qquad t\in\mathbb R$$
> définie pour les $t$ tels que cette espérance est **finie**.

⚠️ La réserve n'est pas de style : $e^{tX}$ croît très vite, et l'espérance peut être infinie.
Le § 5.5 montre que ce cas n'a rien d'exotique.

Deux valeurs immédiates : $M_X(0)=1$ toujours, et $M_X$ est positive.

---

## 5.2 Pourquoi « génératrice des moments »

En développant $e^{tX}=\sum_k \frac{(tX)^k}{k!}$ et en intervertissant (licite quand la FGM est
finie sur un voisinage de 0) :

$$M_X(t)=\sum_{k\ge 0}\frac{E(X^k)}{k!}\,t^k$$

Les moments sont donc les coefficients de Taylor — d'où le nom. En pratique on les extrait par
dérivation en 0 :

$$\boxed{\;E(X^k)=M_X^{(k)}(0)\;}$$

| $k$ | Ce qu'on obtient                                                                                 |
| --- | ------------------------------------------------------------------------------------------------ |
| 1   | $M_X'(0)=E(X)$                                                                                   |
| 2   | $M_X^{(2)}(0)=E(X^2)$, d'où $\operatorname{Var}(X)=M_X^{(2)}(0)-M_X'(0)^2$                       |
| 4   | $M_X^{(4)}(0)=E(X^4)$ — sert au [module 15](15-loi-du-chi2.md) pour $\operatorname{Var}(\chi^2)$ |

> 🔑 **Un calcul d'intégrale remplace une infinité de calculs d'intégrales.** Une seule fonction
> encode tous les moments à la fois.

---

## 5.3 Les trois propriétés qui font tout le travail

| Propriété                   | Énoncé                                                                          | Où elle sert                                               |
| --------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Transformation affine**   | $M_{aX+b}(t)=e^{bt}M_X(at)$                                                     | Standardiser                                               |
| **Somme d'indépendantes** ⭐ | $X\perp\!\!\!\perp Y\ \Rightarrow\ M_{X+Y}=M_X\,M_Y$                            | [Module 8](08-addition-de-lois-et-stabilite-gaussienne.md) |
| **Caractérisation**         | Si $M_X=M_Y$ finies sur un voisinage de 0, alors $X$ et $Y$ ont **la même loi** | Identifier une loi limite                                  |

**Démonstration de la deuxième** — une ligne, et c'est toute la puissance de l'outil :

$$M_{X+Y}(t)=E\!\left(e^{t(X+Y)}\right)=E\!\left(e^{tX}e^{tY}\right)
\overset{\perp\!\!\!\perp}{=}E\!\left(e^{tX}\right)E\!\left(e^{tY}\right)=M_X(t)M_Y(t)$$

⬅️ **L'indépendance sert exactement ici**, et nulle part ailleurs : c'est elle qui autorise
$E(UV)=E(U)E(V)$.

> 🔑 **La FGM transforme une somme en produit.** La loi d'une somme est une **convolution** —
> une intégrale pénible. Sa FGM est un **produit** — une multiplication. Tout le reste du cours
> exploite ce changement de terrain.

La troisième propriété est celle qui permet de **conclure** : après avoir calculé la FGM d'une
somme, il suffit de la reconnaître pour connaître la loi.

---

## 5.4 Le mode d'emploi, en trois temps

C'est le schéma que reprendront les modules 8 et 12 :

1. **Calculer** la FGM de chaque terme ;
2. **Multiplier** — l'indépendance le permet ;
3. **Reconnaître** le résultat — la caractérisation permet de conclure.

Aucune convolution n'est jamais écrite.

---

## 5.5 ⚠️ La limite de l'outil : la FGM n'existe pas toujours

C'est le point que l'on omet le plus souvent, et il est décisif.

| Loi | FGM |
|---|---|
| Normale, exponentielle, uniforme, Bernoulli | Finie sur un voisinage de 0 ✅ |
| **Log-normale** | **Infinie pour tout $t>0$** ❌ — alors que sa variance est finie |
| **Cauchy** | **Infinie pour tout $t\ne 0$** ❌ — elle n'a même pas d'espérance |

La log-normale est le cas gênant : c'est une loi parfaitement ordinaire, de variance finie, à
laquelle le [théorème central limite](12-theoreme-central-limite.md) s'applique — et pourtant sa
FGM ne sert à rien.

> ⚠️ **Conséquence directe.** Un théorème qui prétend valoir *quelle que soit la loi* ne peut pas
> reposer sur un outil qui n'existe pas toujours. C'est pour cette raison, et pour elle seule,
> que le module 12 démontre le TCL avec la **fonction caractéristique**
> ([module 6](06-fonction-caracteristique.md)) et non avec la FGM. Le mécanisme est identique ;
> seule l'existence change.

**Le second défaut, numérique.** $E(e^{tX})$ est dominée par les rares tirages où $X$ est grand :
l'estimation par simulation est instable dès que $t$ dépasse 2 ou 3. Le
[§ 7.4](07-loi-normale-et-ses-transformees.md) le montre sur deux millions de tirages.

---

## 5.6 Simulations

### S5.1 — Les moments par dérivation, et la somme qui devient produit

```python
import numpy as np

rng = np.random.default_rng(1)
N = 2_000_000
X = rng.exponential(2.0, N)          # E(X)=2, Var(X)=4 ; M_X(t)=1/(1-2t) pour t<1/2

M = lambda t: np.mean(np.exp(t * X))
h = 1e-4
print(f"M'(0)  = {(M(h) - M(-h)) / (2*h):.4f}   (theorie E(X)   = 2)")
print(f"M''(0) = {(M(h) - 2*M(0) + M(-h)) / h**2:.4f}   (theorie E(X^2) = 8)")

# somme d'indépendantes : la FGM se multiplie
Y = rng.exponential(2.0, N)
for t in (0.1, 0.2, 0.3):
    gauche = np.mean(np.exp(t * (X + Y)))
    droite = np.mean(np.exp(t * X)) * np.mean(np.exp(t * Y))
    print(f"t={t}: M_(X+Y)={gauche:8.4f}   M_X*M_Y={droite:8.4f}   theorie={1/(1-2*t)**2:8.4f}")
```

La deuxième partie est le cœur : **la FGM d'une somme est le produit des FGM**, et le résultat
$1/(1-2t)^2$ est la FGM d'une loi Gamma — la somme de deux exponentielles indépendantes.

### S5.2 — La FGM qui n'existe pas

```python
for nom, tirage in [("exponentielle", lambda n: rng.exponential(1.0, n)),
                    ("log-normale",   lambda n: rng.lognormal(0, 1, n))]:
    print(f"\n{nom} :")
    for t in (0.2, 0.5, 1.0):
        vals = [np.mean(np.exp(t * tirage(500_000))) for _ in range(5)]
        print(f"  t={t}: 5 estimations = {[round(v, 2) for v in vals]}")
```

Pour l'exponentielle, les cinq estimations coïncident. Pour la log-normale, **elles divergent
entre elles d'un facteur parfois supérieur à 10** : l'espérance est infinie, et la simulation ne
converge vers rien. C'est le § 5.5, vu en pratique.

---

## 5.7 Exercices

**E5.1.** Calculer la FGM d'une loi de Bernoulli de paramètre $p$, puis d'une binomiale
$\mathcal B(n,p)$ **sans convolution**, en utilisant la propriété de la somme.

**E5.2.** Calculer la FGM d'une loi exponentielle de paramètre $\lambda$. Pour quels $t$ est-elle
finie ? En déduire $E(X)$ et $\operatorname{Var}(X)$ par dérivation.

**E5.3.** Montrer que $M_{aX+b}(t)=e^{bt}M_X(at)$. *Application : en déduire la FGM de
$\mathcal N(\mu,\sigma^2)$ à partir de celle de $\mathcal N(0,1)$ — c'est le § 7.2.*

**E5.4.** Deux variables ont la même FGM sur un voisinage de 0. Ont-elles nécessairement les
mêmes moments ? La même loi ? *Justifier avec les propriétés du § 5.3.*

**E5.5.** Pourquoi la loi de Cauchy n'a-t-elle pas de FGM finie ? *(Piste : regarder la décroissance de sa
densité en $1/x^2$ et la comparer à la croissance de $e^{tx}$.) Quelle conséquence pour le
[module 12](12-theoreme-central-limite.md) ?*

---

## 5.8 À retenir

- **$M_X(t)=E(e^{tX})$**, quand c'est fini — et **ce n'est pas toujours le cas**.
- **Les moments sont les dérivées en 0** : $E(X^k)=M_X^{(k)}(0)$.
- ⭐ **Somme d'indépendantes ⟹ produit des FGM.** C'est la propriété pour laquelle l'outil
  existe.
- **La FGM caractérise la loi** (quand elle est finie près de 0) : calculer, multiplier,
  reconnaître.
- ⚠️ **Log-normale et Cauchy n'ont pas de FGM.** C'est ce défaut qui impose la
  [fonction caractéristique](06-fonction-caracteristique.md) dès qu'un théorème doit valoir pour
  toute loi.

---

➡️ [Module 6 — La fonction caractéristique](06-fonction-caracteristique.md) ·
🏠 [Sommaire](README.md)
