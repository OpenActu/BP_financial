# Module 8 — Le portefeuille optimal ⭐

**Durée : 1 h 30.** Prérequis : [module 2](02-l-effet-de-levier.md) (invariance du Sharpe), [covariance et corrélation](../../semestre2/statistique/mathematique/04-covariance-et-correlation.md),
[convexité en dimension $n$](../../semestre1/analyse/convexite/07-convexite-en-dimension-n.md).

> **La question traitée.** Les modules 2 à 7 prennent le portefeuille comme donné : ils règlent
> son **échelle** (levier) et retranchent une **composante** (couverture). Reste la question primitive : quels titres, et en quelle proportion ?

---

## 8.1 Le problème

$n$ actifs de rendements espérés $\mu=(\mu_i)$ et de matrice de covariance $\Sigma$. Un portefeuille est un vecteur de poids $w$ avec $\sum_i w_i=1$, et

$$E[r_w]=w^{\top}\mu,\qquad \operatorname{Var}(r_w)=w^{\top}\Sigma\,w .$$

> 📐 **$w\mapsto w^{\top}\Sigma w$ est convexe** parce que $\Sigma$ est une **matrice de Gram** — celle des produits scalaires entre rendements centrés ([algèbre § 8](../../semestre1/algebre/08-covariance-et-produit-scalaire.md), [convexité § 7](../../semestre1/analyse/convexite/07-convexite-en-dimension-n.md)). Le problème est donc
> **convexe** : tout minimum local est global, et annuler le gradient **suffit** ([convexité § 6](../../semestre1/analyse/convexite/06-minimisation-convexe.md)). C'est ce qui rend le résultat utilisable — sans convexité, un optimum numérique ne prouverait rien.

---

## 8.2 Deux actifs : d'où vient la diversification

Pour $w$ dans le premier actif et $1-w$ dans le second :

$$\operatorname{Var}=w^2\sigma_1^2+(1-w)^2\sigma_2^2+2w(1-w)\rho\sigma_1\sigma_2,$$

minimale en

$$\boxed{\;w^\star=\frac{\sigma_2^2-\rho\sigma_1\sigma_2}{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}\;}$$

Avec $\sigma_1=25\,\%$ et $\sigma_2=30\,\%$ :

| $\rho$ | $w^\star_1$ | $\sigma_{\min}$ | $\sigma$ du 50/50 |
| ------ | ----------- | --------------- | ----------------- |
| −1,0   | 0,545       | **0,00 %**      | 2,50 %            |
| −0,5   | 0,560       | 13,62 %         | 13,92 %           |
| 0,0    | 0,590       | 19,21 %         | 19,53 %           |
| +0,3   | 0,628       | 21,82 %         | 22,22 %           |
| +0,5   | 0,677       | 23,33 %         | 23,85 %           |
| +0,8   | 0,923       | 24,96 %         | 26,10 %           |
| +1,0   | 6,000       | 0,00 %          | 27,50 %           |

**Trois remarques.**

- **La diversification n'exige pas une corrélation négative.** Même à $\rho=+0{,}8$, le mélange
  optimal fait mieux que le meilleur des deux actifs seuls (24,96 % contre 25 %). La condition
  exacte est $\rho<\sigma_1/\sigma_2$ : il suffit que la corrélation soit inférieure au rapport des volatilités.
- **La ligne $\rho=+1$ est un piège** : $w^\star=6$ signifie acheter six fois son capital du premier actif et **vendre à découvert** cinq fois le second. La variance nulle est réelle — deux actifs parfaitement corrélés sont deux échelles du même actif — mais elle exige une VAD
  massive. C'est le premier endroit du cours où l'optimum théorique sort du domaine autorisé.
- **Le gain sur le naïf 50/50 est faible** partout ailleurs (quelques dixièmes de point). Gardez
  ce chiffre en tête pour le [module 9](09-contraintes-reelles-et-estimation.md) : ce que
  l'optimisation ajoute est du même ordre que ce que l'erreur d'estimation retire.

---

## 8.3 $n$ actifs : les deux portefeuilles remarquables

En annulant le gradient sous la contrainte $\mathbf 1^{\top}w=1$
([dérivation § 7](../../semestre1/analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md) pour
la mécanique matricielle) :

$$\boxed{\;w_{\text{mv}}=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^{\top}\Sigma^{-1}\mathbf 1}\;}
\qquad\text{(variance minimale — ne dépend pas de }\mu)$$

$$\boxed{\;w_{\text{tan}}\;\propto\;\Sigma^{-1}(\mu-r_f\mathbf 1)\;}
\qquad\text{(Sharpe maximal)}$$

> ⭐ **Le portefeuille de variance minimale ne fait intervenir que $\Sigma$.** C'est le seul
> portefeuille optimal qui ne demande **aucune** prévision de rendement — et le
> [module 9](09-contraintes-reelles-et-estimation.md) montrera que c'est précisément pour cela
> qu'il se comporte bien en pratique.

---

## 8.4 Un exemple à trois actifs

Trois blocs représentatifs de la cote parisienne : **Luxe**, **Banque**, **Utilities**.

$$\mu=\begin{pmatrix}10\,\%\\4\,\%\\6\,\%\end{pmatrix},\quad
\sigma=\begin{pmatrix}30\,\%\\28\,\%\\18\,\%\end{pmatrix},\quad
\text{corr}=\begin{pmatrix}1&0{,}65&0{,}35\\0{,}65&1&0{,}40\\0{,}35&0{,}40&1\end{pmatrix},\quad
r_f=3\,\% .$$

| Portefeuille | $w_{\text{luxe}}$ | $w_{\text{banque}}$ | $w_{\text{util.}}$ | $E[R]$ | $\sigma$ | Sharpe |
|---|---|---|---|---|---|---|
| Variance minimale | 0,100 | 0,106 | 0,795 | 6,19 % | **17,25 %** | 0,185 |
| **Tangent (VAD permise)** | 1,063 | **−0,814** | 0,752 | 11,88 % | 28,80 % | **0,308** |
| **Tangent long-only** | 0,552 | 0,000 | 0,448 | 8,21 % | 20,81 % | 0,250 |
| Équipondéré 1/3 | 0,333 | 0,333 | 0,333 | 6,67 % | 20,77 % | 0,177 |
| 100 % Luxe | 1,000 | 0,000 | 0,000 | 10,00 % | 30,00 % | 0,233 |
| 100 % Utilities | 0,000 | 0,000 | 1,000 | 6,00 % | 18,00 % | 0,167 |

> ⭐ **Le portefeuille tangent exige de vendre à découvert 81 % du capital en banques.** Ce n'est
> pas une bizarrerie numérique : la banque a le plus mauvais rendement espéré **et** une forte
> corrélation avec le luxe (0,65), donc l'optimiseur s'en sert comme d'une **couverture financée**
> — exactement le raisonnement du [module 6](06-la-couverture-optimale.md), appliqué à l'intérieur
> du portefeuille.
>
> **En PEA, ce portefeuille n'existe pas.** Au SRD, il existe mais coûte 7 à 9 % par an de portage
> sur la jambe vendeuse ([module 5](05-la-vente-a-decouvert.md)) — ce qui suffit, ici, à annuler
> tout son avantage.

**Le coût de la contrainte $w\ge0$** : le Sharpe passe de 0,308 à 0,250, soit **−18,8 %**. La
contrainte fait exactement ce qu'on attend d'elle — elle met à zéro le poids négatif — et ce
qu'on n'attend pas : elle redistribue le reste (le luxe passe de 1,063 à 0,552).

---

## 8.5 Séparation en deux fonds, et jonction avec le levier

Une fois $w_{\text{tan}}$ choisi, **tout** le reste de la décision est un scalaire : la fraction
investie, c'est-à-dire le levier du [module 2](02-l-effet-de-levier.md). Tous les portefeuilles
optimaux sont sur une **droite** :

$$E[R]=r_f+L\bigl(E[R_{\text{tan}}]-r_f\bigr),\qquad \sigma=L\,\sigma_{\text{tan}} .$$

Ciblons $\sigma=20\,\%$ avec les portefeuilles du § 8.4 :

| Point de départ | Levier requis | $E[R]$ obtenue à $\sigma=20\,\%$ |
|---|---|---|
| Tangent non contraint | $L=0{,}69$ | **9,17 %** |
| Tangent long-only | $L=0{,}96$ | 8,01 % |

> ⭐ **La contrainte de vente à découvert coûte 1,16 point de rendement annuel à risque égal.**
> C'est la traduction correcte de « le Sharpe baisse de 18,8 % » : à volatilité fixée, la perte
> est un rendement, pas un ratio. Et c'est le seul chiffrage honnête de ce que le PEA fait perdre
> — à comparer à ce qu'il fait gagner en fiscalité, qui est de l'ordre de plusieurs points.
>
> **Notez aussi que les deux leviers sont inférieurs à 1** : viser 20 % de volatilité avec ces
> actifs demande de détenir des liquidités, pas d'emprunter. Le [module 4](04-levier-optimal-et-drag.md)
> disait la même chose par un autre chemin.

⚠️ **Le CAC 40 n'est pas le portefeuille tangent.** C'est un portefeuille **long-only pondéré par
la capitalisation flottante**, révisé sur des critères de liquidité et de représentativité, pas
d'optimalité. Le prendre comme référence de performance est légitime ; le prendre comme
portefeuille optimal ne l'est pas.

---

## 8.6 Simulation

### S8.1 — Frontière, tangent, contrainte

```python
import numpy as np

mu = np.array([0.10, 0.04, 0.06])
sig = np.array([0.30, 0.28, 0.18])
C = np.array([[1, 0.65, 0.35], [0.65, 1, 0.40], [0.35, 0.40, 1]])
S = np.outer(sig, sig) * C
rf, un = 0.03, np.ones(3)

inv = np.linalg.inv(S)
w_mv = inv @ un / (un @ inv @ un)
w_t = inv @ (mu - rf); w_t /= w_t.sum()

def stats(w):
    m, v = w @ mu, w @ S @ w
    return m, np.sqrt(v), (m - rf) / np.sqrt(v)

for nom, w in (("variance min", w_mv), ("tangent", w_t), ("1/3", un / 3)):
    m, s, sh = stats(w)
    print(f"{nom:<14}" + "".join(f"{x:>8.3f}" for x in w) + f"{m:>8.2%}{s:>8.2%}{sh:>8.3f}")

# tangent long-only : balayage du simplexe (le probleme est convexe, le maximum est unique)
best = max(((stats(np.array([a, b, 1 - a - b])), np.array([a, b, 1 - a - b]))
            for a in np.linspace(0, 1, 401)
            for b in np.linspace(0, 1 - a, int(round((1 - a) * 400)) + 1)),
           key=lambda t: t[0][2])
(m, s, sh), w = best
print(f"{'tangent w>=0':<14}" + "".join(f"{x:>8.3f}" for x in w) + f"{m:>8.2%}{s:>8.2%}{sh:>8.3f}")

# cout de la contrainte, exprime en rendement a volatilite egale
for nom, (m_, s_, sh_) in (("non contraint", stats(w_t)), ("long-only", (m, s, sh))):
    L = 0.20 / s_
    print(f"{nom:<14} levier pour sigma=20% : {L:.2f}  ->  E[R] = {rf + L * (m_ - rf):.2%}")
```

Sortie attendue : les tables des § 8.4 et 8.5, dont le poids **−0,814** sur la banque et l'écart
de 1,16 point entre les deux dernières lignes.

---

## 8.7 Exercices

**E8.1.** Démontrer la formule de $w^\star$ à deux actifs, et en déduire la condition
$\rho<\sigma_1/\sigma_2$ pour que la diversification abaisse la variance sous $\sigma_1$.

**E8.2.** Vérifier que $w_{\text{mv}}$ ne dépend pas de $\mu$, et expliquer pourquoi c'est une
**bonne nouvelle** au vu du [§ 4.5](04-levier-optimal-et-drag.md).

**E8.3.** Montrer que le portefeuille tangent est celui dont le rapport
$\frac{\mu_i-r_f}{(\Sigma w)_i}$ est le **même pour tous les actifs**. *Interpréter : que
signifie « le rendement marginal par unité de risque marginal est égalisé » ?*

**E8.4.** Reprendre le § 8.4 en ajoutant un coût de portage de 8 % sur la jambe vendeuse.
*Le tangent non contraint reste-t-il meilleur que le tangent long-only ?*

**E8.5.** Sur les données du script, estimer $\mu$, $\sigma$ et $\Sigma$ pour 10 valeurs du
CAC 40 sur 5 ans, puis calculer $w_{\text{tan}}$. *Combien de poids sont négatifs ? Quelle est la
somme des poids négatifs, et est-elle finançable au SRD ?*

**E8.6.** Comparer, sur les mêmes données, $w_{\text{mv}}$, $w_{\text{tan}}$, $1/N$ et l'indice
pondéré par capitalisation. *Sur la période suivante, lequel a le meilleur Sharpe réalisé ?*
(C'est la question du [module 9](09-contraintes-reelles-et-estimation.md).)

---

## 8.8 À retenir

- **Minimiser $w^{\top}\Sigma w$ est un problème convexe** parce que $\Sigma$ est une matrice de
  Gram. C'est ce qui garantit qu'un optimum est *l'*optimum.
- **La diversification ne demande pas de corrélation négative**, seulement $\rho<\sigma_1/\sigma_2$.
- **Deux portefeuilles remarquables** : $w_{\text{mv}}\propto\Sigma^{-1}\mathbf1$ (aucune
  prévision de rendement) et $w_{\text{tan}}\propto\Sigma^{-1}(\mu-r_f\mathbf1)$ (Sharpe maximal).
- ⭐ **Le tangent contient presque toujours des poids négatifs** : l'optimiseur utilise les actifs
  médiocres et corrélés comme **couvertures financées**. C'est le module 6 appliqué à l'intérieur
  du portefeuille.
- ⭐ **Interdire la VAD coûte, sur l'exemple, 18,8 % de Sharpe — soit 1,16 point de rendement
  annuel à volatilité égale.** C'est le prix du PEA, à mettre en regard de son avantage fiscal.
- **Séparation en deux fonds** : choisir le portefeuille (qualité) et choisir le levier (échelle)
  sont deux décisions indépendantes. Le module 4 traite la seconde.
- ⚠️ **Le CAC 40 n'est pas le portefeuille tangent** : c'est un long-only pondéré par
  capitalisation, construit pour représenter, pas pour optimiser.

---

⬅️ [Module 7 — Couvrir en pratique](07-couvrir-en-pratique.md) ·
➡️ [Module 9 — Contraintes réelles, estimation et synthèse](09-contraintes-reelles-et-estimation.md) ·
🏠 [Sommaire](README.md)
