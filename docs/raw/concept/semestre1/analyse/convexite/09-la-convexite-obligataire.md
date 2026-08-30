# Module 9 — La convexité obligataire

**Durée : 1 h.** Prérequis : modules [3](03-criteres-differentiels.md) et
[5](05-jensen-probabiliste.md).

> **La question traitée.** Les praticiens des marchés de taux appellent « convexité » un nombre
> précis, qu'ils calculent et qu'ils paient. Est-ce la même notion que celle de ce cours ?

**Réponse courte : oui, exactement.** La « convexité » d'une obligation est la dérivée seconde
normalisée de son prix, et tout ce qu'on en dit sur les marchés — *le prix monte plus qu'il ne
baisse*, *la duration seule sous-estime toujours*, *la convexité se paie* — sont des applications
directes des modules 3 et 5.

---

## 9.1 Le prix est une fonction convexe du taux

Une obligation versant les flux $c_1,\dots,c_T\ge0$ aux dates $1,\dots,T$ vaut, au taux
actuariel $y$ :

$$P(y)=\sum_{t=1}^{T}\frac{c_t}{(1+y)^{t}} .$$

> **Proposition.** Sur $]-1,+\infty[$, $P$ est **strictement décroissante** et **strictement
> convexe** (dès qu'un flux est non nul en $t\ge1$).

*Démonstration.* Chaque terme $y\mapsto c_t(1+y)^{-t}$ a pour dérivées

$$-\,t\,c_t(1+y)^{-t-1}<0,\qquad t(t+1)\,c_t(1+y)^{-t-2}>0 ,$$

donc est décroissant et convexe ; une **somme à coefficients positifs** de fonctions convexes est
convexe ([§ 2.3](02-fonctions-convexes.md)). $\blacksquare$

⚠️ **L'hypothèse $c_t\ge0$ est indispensable** et elle est ce qui distingue une obligation ordinaire
d'un instrument à flux structurés. Un swap, un flux négatif, une option incorporée peuvent détruire
la convexité (§ 9.5).

---

## 9.2 Duration : l'approximation du premier ordre

> **Définitions.**
> $$D_{\text{mod}}=-\frac{P'(y)}{P(y)}\quad(\text{duration modifiée}),\qquad
> D_{\text{Mac}}=(1+y)\,D_{\text{mod}}=\frac{1}{P}\sum_t \frac{t\,c_t}{(1+y)^t}
> \quad(\text{duration de Macaulay}).$$

La duration de Macaulay est la **moyenne pondérée des maturités**, les poids étant les valeurs
actualisées des flux : une combinaison convexe des dates, au sens du
[§ 4.1](04-jensen-fini-et-moyennes.md). Elle est donc comprise entre 1 et $T$.

L'approximation au premier ordre s'écrit

$$\frac{\Delta P}{P}\;\approx\;-D_{\text{mod}}\,\Delta y .$$

C'est la **tangente**. Et l'on sait déjà tout ce qu'il faut en penser :

> 🔑 **La tangente passe sous le graphe** ([§ 3.3](03-criteres-differentiels.md)). Donc
> $$P(y+\Delta y)\;\ge\;P(y)\big(1-D_{\text{mod}}\Delta y\big)\qquad\textbf{pour tout }\Delta y,$$
> **hausse comme baisse**. L'estimation par la duration seule **sous-estime systématiquement le
> prix**, jamais l'inverse. Ce n'est pas un constat empirique : c'est la définition de la
> convexité.

---

## 9.3 Convexité : le terme d'ordre 2

> **Définition.** $\displaystyle C=\frac{P''(y)}{P(y)}=\frac1P\sum_t\frac{t(t+1)\,c_t}{(1+y)^{t+2}}\;>\;0$

Le développement de Taylor à l'ordre 2 donne la formule des praticiens :

$$\boxed{\;\frac{\Delta P}{P}\;\approx\;-D_{\text{mod}}\,\Delta y\;+\;\frac12\,C\,(\Delta y)^2\;}$$

Le second terme est **toujours positif** — c'est $C>0$ — et il **s'ajoute** que le taux monte ou
descende.

### L'exemple chiffré de référence

Obligation à **10 ans**, coupon annuel **3 %**, nominal 100, au taux $y=3\,\%$ (donc au pair) :

$$P=100{,}00,\qquad D_{\text{Mac}}=8{,}786,\qquad D_{\text{mod}}=8{,}530,\qquad C=87{,}07$$

| $\Delta y$ | Prix exact | Duration seule | Erreur | Duration $+$ convexité | Erreur |
|---|---|---|---|---|---|
| $+1\,\%$ | 91,889 | 91,470 | $-0{,}419$ | 91,905 | $+0{,}016$ |
| $-1\,\%$ | 108,983 | 108,530 | $-0{,}452$ | 108,966 | $-0{,}017$ |
| $+2\,\%$ | 84,557 | 82,940 | $-1{,}617$ | 84,681 | $+0{,}124$ |
| $-2\,\%$ | 118,943 | 117,060 | $-1{,}882$ | 118,802 | $-0{,}141$ |

**Trois lectures.**

- **L'erreur de la duration seule est négative dans les quatre lignes** — c'est l'inégalité de la
  tangente, vérifiée à la troisième décimale.
- **L'asymétrie est le fait économique** : $+1\,\%$ de taux fait perdre 8,11 points, $-1\,\%$ en
  fait gagner 8,98. Le porteur gagne plus qu'il ne perd, à variation de taux égale. C'est
  **exactement** ce que la convexité signifie.
- **Le terme d'ordre 2 divise l'erreur par 25 environ**, et le résidu change de signe : il est
  d'ordre 3, gouverné par la dérivée troisième.

---

## 9.4 Le gain de convexité, c'est Jensen

Supposons le taux futur **aléatoire**, d'espérance $y_0$ et de variance $\sigma_y^2$. La convexité
de $P$ donne immédiatement ([module 5](05-jensen-probabiliste.md)) :

$$E\big[P(y)\big]\;\ge\;P\big(E[y]\big)=P(y_0),$$

et le développement au second ordre chiffre l'écart :

$$E\big[P(y)\big]\;\approx\;P(y_0)\Big(1+\tfrac12\,C\,\sigma_y^2\Big).$$

**Sur l'exemple.** Un taux qui vaut $2\,\%$ ou $4\,\%$ avec probabilité $\frac12$ chacun a pour
espérance $3\,\%$ et pour variance $(1\,\%)^2$ :

$$\tfrac12P(2\,\%)+\tfrac12P(4\,\%)=100{,}436\;>\;P(3\,\%)=100{,}000,$$

soit un gain de **$+0{,}436$**, à comparer à la prédiction $\frac12C\sigma_y^2P=0{,}435$. L'accord
est à la troisième décimale.

> 🔑 **La volatilité des taux est une bonne nouvelle pour le porteur d'une obligation ordinaire.**
> C'est le pendant exact du [drag de volatilité](05-jensen-probabiliste.md) — même inégalité, sens
> opposé, parce que la fonction est convexe ici et concave là. **Le signe de l'effet de la
> volatilité est toujours celui de la courbure.**

⚠️ **Ce gain est un effet du second ordre, pas une prédiction de rendement.** Il dit que la
*moyenne des prix* dépasse le *prix au taux moyen* — rien de plus. Il ne dit ni que le prix
montera, ni que la position est profitable.

---

## 9.5 Ce que la convexité coûte, et quand elle disparaît

### Elle se paie

À duration égale, une obligation plus convexe est **plus désirable** : elle gagne davantage quand
les taux baissent et perd moins quand ils montent. Le marché le sait, et l'inclut dans le prix :
à duration égale, **plus de convexité s'échange contre un rendement plus faible**.

| Structure | Duration | Convexité | Lecture |
|---|---|---|---|
| *Bullet* — une seule maturité 10 ans | 8,53 | 87 | Référence |
| *Barbell* — moitié 2 ans, moitié 20 ans | ≈ 8,53 | **plus élevée** | Même sensibilité au premier ordre, meilleur second ordre |

La convexité croît, à duration donnée, avec la **dispersion des maturités** — ce qui est encore une
lecture de Jensen : les flux étant actualisés par une fonction convexe, étaler les dates augmente
la moyenne des actualisations.

### Elle peut devenir négative

⚠️ Trois familles d'instruments ont une **convexité négative** sur une plage de taux, c'est-à-dire
un prix **concave** :

| Instrument | Mécanisme | Conséquence |
|---|---|---|
| Obligation **remboursable par anticipation** | L'émetteur rappelle si les taux baissent | Le prix plafonne : concave |
| Crédits hypothécaires titrisés (**MBS**) | Les emprunteurs remboursent par anticipation | Idem, en plus diffus |
| Positions vendeuses d'options | Le paiement vendu est convexe, donc l'inverse est concave | Perte accélérée |

Sur ces instruments, **toutes les conclusions du § 9.3 s'inversent** : la tangente passe
au-dessus, la duration **surestime** le prix, et la volatilité des taux devient un coût — Jensen
dans l'autre sens. C'est la raison structurelle pour laquelle les portefeuilles de MBS se couvrent
mal avec la seule duration.

---

## 9.6 Simulation

### S9.1 — Duration, convexité, et les deux inégalités du cours

```python
import numpy as np

def flux(T=10, coupon=3.0, nominal=100.0):
    c = np.full(T, coupon)
    c[-1] += nominal
    return np.arange(1, T + 1), c

t, c = flux()

def prix(y):        return (c / (1 + y) ** t).sum()
def d_mod(y):       return (t * c / (1 + y) ** (t + 1)).sum() / prix(y)
def convexite(y):   return (t * (t + 1) * c / (1 + y) ** (t + 2)).sum() / prix(y)

y0 = 0.03
P0, D, C = prix(y0), d_mod(y0), convexite(y0)
print(f"P={P0:.4f}  D_mod={D:.4f}  D_Macaulay={D * (1 + y0):.4f}  C={C:.4f}")

print(f"\n{'dy':>7}{'exact':>10}{'duree':>10}{'erreur':>9}{'+convex':>10}{'erreur':>9}")
for dy in (0.01, -0.01, 0.02, -0.02):
    ex = prix(y0 + dy)
    lin = P0 * (1 - D * dy)
    qua = P0 * (1 - D * dy + 0.5 * C * dy ** 2)
    print(f"{dy:>+7.2%}{ex:>10.3f}{lin:>10.3f}{lin - ex:>+9.3f}{qua:>10.3f}{qua - ex:>+9.3f}")

# la tangente passe sous le graphe : vrai pour TOUT dy
dys = np.linspace(-0.02, 0.05, 7001)
exact = np.array([prix(y0 + d) for d in dys])
tangente = P0 * (1 - D * dys)
print(f"\ntangente sous le graphe partout : {(exact - tangente >= -1e-9).all()}"
      f"   ecart max = {(exact - tangente).max():.3f}")

# Jensen : la moyenne des prix depasse le prix au taux moyen
for s in (0.005, 0.01, 0.02):
    moyenne = 0.5 * prix(y0 - s) + 0.5 * prix(y0 + s)
    print(f"sigma_y={s:.3%} : E[P]={moyenne:.4f}  P(E[y])={P0:.4f}"
          f"  gain={moyenne - P0:+.4f}   prediction 0.5*C*s^2*P={0.5 * C * s ** 2 * P0:.4f}")
```

Sortie attendue : $D_{\text{mod}}=8{,}5302$, $C=87{,}066$, les quatre erreurs de duration
**toutes négatives**, et un gain de Jensen qui suit $\frac12C\sigma_y^2P$ à la troisième décimale.

---

## 9.7 Exercices

**E9.1.** Démontrer que $P$ est convexe **sans** dériver, en utilisant la stabilité par somme et le
fait que $y\mapsto(1+y)^{-t}$ est convexe ([§ 3.4](03-criteres-differentiels.md)).

**E9.2.** Montrer que $D_{\text{Mac}}$ est une combinaison convexe des dates $1,\dots,T$, puis en
déduire $1\le D_{\text{Mac}}\le T$. *Quand y a-t-il égalité à droite ?*

**E9.3.** Vérifier sur l'obligation du § 9.3 que l'erreur de l'approximation à l'ordre 2 change de
signe entre $\Delta y>0$ et $\Delta y<0$. *Quelle dérivée gouverne ce résidu, et quel est son
signe ?*

**E9.4.** Une obligation zéro-coupon de maturité $T$ a $D_{\text{Mac}}=T$. Calculer sa convexité et
montrer qu'elle croît comme $T^2$. *Conséquence pour la couverture d'un passif long par des
obligations courtes.*

**E9.5.** Construire numériquement un *barbell* (2 ans / 20 ans) de même duration modifiée que le
*bullet* 10 ans du § 9.3, et comparer les convexités. *De combien de points de rendement annuel
êtes-vous prêt à payer l'écart, si les taux bougent de $\pm1\,\%$ par an ?*

**E9.6.** Une obligation remboursable par anticipation a un prix plafonné à 102. Tracer
$\min\big(P(y),102\big)$ et montrer que la fonction obtenue **n'est pas convexe**. *(Rappel :
[§ 2.3](02-fonctions-convexes.md) — un min de convexes ne l'est pas.)* Où la duration
sur-estime-t-elle le prix ?

---

## 9.8 À retenir

- **Le prix d'une obligation à flux positifs est une fonction convexe décroissante du taux.** La
  « convexité » des praticiens, $C=P''/P$, est littéralement la courbure du module 3.
- **$\frac{\Delta P}{P}\approx-D_{\text{mod}}\Delta y+\frac12C(\Delta y)^2$**, le second terme
  étant **toujours positif**.
- ⭐ **La duration seule sous-estime toujours le prix**, à la hausse comme à la baisse : c'est
  l'inégalité de la tangente, pas une régularité empirique.
- **Le gain de convexité est un Jensen** : $E[P(y)]\ge P(E[y])$, et l'écart vaut
  $\frac12C\sigma_y^2P$. La volatilité des taux profite au porteur — pendant exact, et de signe
  opposé, du drag de volatilité du [module 5](05-jensen-probabiliste.md).
- **À duration égale, la convexité se paie** en rendement, et croît avec la dispersion des
  maturités.
- ⚠️ **Convexité négative** (obligations rappelables, MBS, ventes d'options) : toutes les
  conclusions s'inversent, y compris le sens de l'effet de la volatilité.

---

⬅️ [Module 8 — Convexité et mesures de risque](08-convexite-et-mesures-de-risque.md) ·
🏠 [Sommaire](README.md) ·
📘 [Cours de statistique](../../../semestre2/statistique/mathematique/README.md) ·
📐 [Cours d'algèbre](../../algebre/README.md)
