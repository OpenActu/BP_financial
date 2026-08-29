# Module 18 — L'intervalle de confiance ⭐

**Durée : 1 h 30.** Prérequis : module [17](17-estimation-et-quantite-pivotale.md).

> **La question traitée.** Un échantillon gaussien de taille $n=25$ donne $\bar x = 103{,}2$ ;
> on sait que $\sigma = 8$. Construire l'IC à 95 % de $\mu$ et **justifier le 1,96**.

**Ce qui est en jeu.** La construction menée ici — pivot, retournement, intervalle — est
**la maquette de toute l'inférence classique**. Elle sera reprise à l'identique avec $S$ à la
place de $\sigma$ et Student à la place de la normale.

---

## 18.1 Construction : le retournement

### Le point de départ

Par définition du quantile $z_{1-\alpha/2}$ de la loi normale centrée réduite :

$$P\Bigl(-z_{1-\alpha/2}\;\le\;Z\;\le\;z_{1-\alpha/2}\Bigr)=1-\alpha$$

### Le retournement algébrique

Substituons le [pivot du § 17.3](17-estimation-et-quantite-pivotale.md) et **isolons $\mu$**.
Chaque ligne est une équivalence, pas une approximation :

$$-z\;\le\;\frac{\bar X-\mu}{\sigma/\sqrt n}\;\le\;z$$

$$\iff\quad -z\frac{\sigma}{\sqrt n}\;\le\;\bar X-\mu\;\le\;z\frac{\sigma}{\sqrt n}
\qquad\text{(multiplication par } \sigma/\sqrt n>0)$$

$$\iff\quad -\bar X-z\frac{\sigma}{\sqrt n}\;\le\;-\mu\;\le\;-\bar X+z\frac{\sigma}{\sqrt n}
\qquad\text{(soustraction de } \bar X)$$

$$\iff\quad \bar X-z\frac{\sigma}{\sqrt n}\;\le\;\mu\;\le\;\bar X+z\frac{\sigma}{\sqrt n}
\qquad\text{(⚠️ multiplication par } -1 : \textbf{les inégalités s'inversent)}$$

D'où :

$$\boxed{\;\text{IC}_{1-\alpha}(\mu)=\left[\;\bar X-z_{1-\alpha/2}\frac{\sigma}{\sqrt n}
\;;\;\bar X+z_{1-\alpha/2}\frac{\sigma}{\sqrt n}\;\right]}$$

La quantité $z_{1-\alpha/2}\frac{\sigma}{\sqrt n}$ s'appelle la **marge d'erreur**.

### ⚠️ Ce que le retournement a et n'a pas fait

L'algèbre a déplacé $\mu$ au centre de l'inégalité. **Elle n'a pas transféré l'aléa sur $\mu$.**

Dans la ligne de départ, ce qui est aléatoire est $\bar X$ ; dans la ligne d'arrivée, c'est
**encore** $\bar X$ — il apparaît simplement aux deux bornes. $\mu$ n'est jamais devenu une
variable aléatoire : c'est une constante inconnue, avant comme après.

> 🔑 **Retenez ce point : il contient à lui seul tout le
> [module 19](19-interpretation-de-la-confiance.md).** Ce sont les **bornes** qui sont aléatoires,
> pas le centre.

---

## 18.2 D'où vient le 1,96

### La définition

On cherche $z$ tel que $P(-z\le Z\le z)=0{,}95$ avec $Z\sim\mathcal N(0,1)$.

Par symétrie de la densité, les 5 % restants se répartissent en **deux queues de 2,5 %** :

$$P(Z>z)=0{,}025 \qquad\text{et}\qquad P(Z<-z)=0{,}025$$

Donc $P(Z\le z)=1-0{,}025=0{,}975$, c'est-à-dire

$$z=\Phi^{-1}(0{,}975)=z_{0{,}975}=\mathbf{1{,}959964\ldots}$$

où $\Phi$ est la fonction de répartition de $\mathcal N(0,1)$.

```python
from scipy import stats
stats.norm.ppf(0.975)      # 1.9599639845400545
```

### Les trois erreurs à ne pas commettre

1. **Chercher $\Phi^{-1}(0{,}95)$** au lieu de $\Phi^{-1}(0{,}975)$ — cela donne $1{,}645$, qui
   est le quantile du test **unilatéral** ou de l'IC à 90 %. Le $\alpha/2$ vient du caractère
   **bilatéral** de l'intervalle : deux bornes, donc deux queues.
2. **Croire que 1,96 est universel.** Il est attaché au **niveau 95 %** et à la **loi normale**.
   Changer l'un ou l'autre change le nombre.
3. **Confondre avec le « 2 » des règles mentales.** $P(|Z|<2)=0{,}9545$ : la règle des deux
   écarts-types donne 95,45 %, pas 95 %. C'est une commodité, pas la valeur exacte.

### Les quantiles à connaître

| Niveau de confiance | $\alpha$ | $\alpha/2$ | $z_{1-\alpha/2}$ | Marge sur l'exemple |
| ------------------- | -------- | ---------- | ---------------- | ------------------- |
| 90 %                | 0,10     | 0,05       | **1,645**        | ±2,632              |
| 95 %                | 0,05     | 0,025      | **1,960**        | ±3,136              |
| 99 %                | 0,01     | 0,005      | **2,576**        | ±4,121              |

Passer de 95 % à 99 % **élargit l'intervalle de 31 %**. Il n'y a pas de repas gratuit : plus de
confiance signifie moins de précision.

---

## 18.3 Lecture de la formule : les trois leviers

$$\text{marge}=z_{1-\alpha/2}\cdot\frac{\sigma}{\sqrt n}$$

| Levier                    | Effet                                     | Maîtrisable ?                                        |
| ------------------------- | ----------------------------------------- | ---------------------------------------------------- |
| $z_{1-\alpha/2}$ (niveau) | Plus de confiance → intervalle plus large | Oui, mais c'est un **choix**, pas un gain            |
| $\sigma$ (dispersion)     | Propre au phénomène étudié                | Rarement — sauf en améliorant le protocole de mesure |
| $n$ (effectif)            | Marge en $1/\sqrt n$                      | **Oui — c'est le seul vrai levier**                  |

### La loi en $1/\sqrt n$ et son coût

Diviser la marge par 2 exige de **quadrupler** l'effectif. Par 3, de le **multiplier par 9**.

Sur l'exemple ($\sigma=8$, niveau 95 %) :

| $n$   | 25     | 100    | 400    | 1600   |
| ----- | ------ | ------ | ------ | ------ |
| Marge | ±3,136 | ±1,568 | ±0,784 | ±0,392 |

> 🔑 **C'est la loi d'airain de toute collecte de données**, et elle explique le rendement
> décroissant des grandes enquêtes : les 75 premières observations supplémentaires font gagner
> 1,57 point de marge, les 1 200 suivantes n'en font gagner que 0,39.

⚠️ La même vitesse $1/\sqrt n$ gouverne la
[convergence du TCL](13-portee-et-limites-du-tcl.md). Ce n'est pas une coïncidence : les deux
viennent du $\sqrt n$ de l'erreur type.

---

## 18.4 L'exemple numérique, complet

**Données** : $n=25$, $\bar x=103{,}2$, $\sigma=8$ (connu), population gaussienne.

**Étape 1 — erreur type.**
$$\sigma_{\bar X}=\frac{\sigma}{\sqrt n}=\frac{8}{\sqrt{25}}=\frac{8}{5}=1{,}6$$

**Étape 2 — quantile.** Niveau 95 % bilatéral → $z_{0{,}975}=1{,}96$.

**Étape 3 — marge.**
$$1{,}96\times 1{,}6=3{,}1359\;\approx\;3{,}14$$

**Étape 4 — intervalle.**
$$\text{IC}_{95\%}(\mu)=[\,103{,}2-3{,}14\;;\;103{,}2+3{,}14\,]=\boxed{[\,100{,}06\;;\;106{,}34\,]}$$

**Récapitulatif aux trois niveaux :**

| Niveau | $z$ | Marge | Intervalle | Largeur |
|---|---|---|---|---|
| 90 % | 1,645 | ±2,632 | [100,57 ; 105,83] | 5,26 |
| **95 %** | **1,960** | **±3,136** | **[100,06 ; 106,34]** | **6,27** |
| 99 % | 2,576 | ±4,121 | [99,08 ; 107,32] | 8,24 |

**Rédaction de la conclusion** — la formulation compte autant que le calcul :

> Au niveau de confiance de 95 %, la moyenne de la population est estimée à 103,2, avec une marge
> d'erreur de ±3,1 (intervalle [100,1 ; 106,3]).

Notez ce qui est **absent** de cette phrase : aucune probabilité n'est attribuée à $\mu$. Le
[module 19](19-interpretation-de-la-confiance.md) dit pourquoi.

---

## 18.5 Variantes

### Intervalle unilatéral

Quand seule une borne intéresse (« le rendement est-il au moins de… ? », « la teneur dépasse-t-elle
le seuil ? »), on met les 5 % **d'un seul côté** :

$$\text{minorant à 95 % : } \left[\bar X-z_{0{,}95}\frac{\sigma}{\sqrt n};\;+\infty\right)
\qquad\text{avec } z_{0{,}95}=1{,}645$$

Sur l'exemple : $[103{,}2-1{,}645\times1{,}6\;;\;+\infty)=[100{,}57\;;\;+\infty)$. La borne
inférieure est **plus haute** que celle de l'IC bilatéral (100,06) : on gagne en précision d'un
côté ce qu'on abandonne de l'autre.

⚠️ **Le choix unilatéral/bilatéral se fait AVANT de voir les données.** Basculer en unilatéral
après avoir constaté le signe de l'écart double en réalité le risque annoncé. Et rappelez-vous du
[§ 13.2 ①](13-portee-et-limites-du-tcl.md) : sur données non gaussiennes, un unilatéral est bien
plus exposé qu'un bilatéral.

### Dimensionnement de l'échantillon

Pour garantir une marge $m$ au niveau $1-\alpha$ :

$$z_{1-\alpha/2}\frac{\sigma}{\sqrt n}\le m
\qquad\Longleftrightarrow\qquad
\boxed{\;n\;\ge\;\left(\frac{z_{1-\alpha/2}\,\sigma}{m}\right)^{2}}$$

Sur l'exemple ($\sigma=8$, niveau 95 %) :

| Marge visée $m$ | $n$ minimal | Marge obtenue |
|---|---|---|
| 3,136 | 25 | 3,136 |
| 2,0 | **62** | 1,991 |
| 1,568 | **100** | 1,568 |
| 1,0 | **246** | 1,000 |

⚠️ **Toujours arrondir à l'entier supérieur** : $n=61$ donnerait une marge de 2,008, au-dessus de
la cible. Et notez la circularité pratique : ce calcul exige de connaître $\sigma$ *avant* de
collecter. On utilise en pratique une étude pilote, un historique, ou une majoration prudente.

---

## 18.6 Simulation

### S18.1 — Le taux de couverture (la simulation décisive)

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
MU, SIGMA, n, N = 100.0, 8.0, 25, 200_000
z = stats.norm.ppf(0.975)

X = rng.normal(MU, SIGMA, size=(N, n))
xbar = X.mean(axis=1)
marge = z * SIGMA / np.sqrt(n)                 # CONSTANTE : sigma est connu
dedans = np.abs(xbar - MU) <= marge

print(f"couverture      : {dedans.mean():.4f}   (cible 0,9500)")
print(f"marge           : ±{marge:.4f}")
print(f"largeur         : {2*marge:.4f}  — la MÊME pour tous les échantillons")
```

> 🔑 **Observation à ne pas manquer** : ici, tous les intervalles ont **exactement la même
> largeur**, puisque $\sigma$ est connu. Seule leur **position** varie. Gardez ce fait en tête :
> quand $\sigma$ est estimé par $S$, la largeur devient elle aussi aléatoire — et c'est
> précisément ce qui rend la loi de Student nécessaire.

### S18.2 — Le dimensionnement, vérifié

```python
for m in (3.136, 2.0, 1.568, 1.0):
    n_min = int(np.ceil((z * SIGMA / m) ** 2))
    print(f"marge visee {m:>6} -> n = {n_min:>4}  (marge obtenue {z*SIGMA/np.sqrt(n_min):.4f})")
```

---

## 18.7 Exercices

**E18.1.** Refaire l'exemple aux niveaux 90 % et 99 %. Vérifier les valeurs du tableau du
§ 18.4. De quel pourcentage l'intervalle s'élargit-il en passant de 95 % à 99 % ?

**E18.2.** Un procédé industriel a un écart-type connu $\sigma=2{,}5$ mm. Sur $n=16$ pièces,
$\bar x=48{,}3$ mm. Donner l'IC à 95 % de la longueur moyenne. Combien de pièces faudrait-il
mesurer pour une marge de ±0,5 mm ? *(Réponse : $n\ge(1{,}96\times2{,}5/0{,}5)^2=96{,}04$, soit
**97** pièces.)*

**E18.3.** Démontrer que la largeur de l'IC ne dépend **pas** des données quand $\sigma$ est
connu. En quoi cela change-t-il quand $\sigma$ est estimé ?

**E18.4.** On veut diviser par 3 la marge de l'exemple. Quel $n$ faut-il ? Le résultat vous
paraît-il coûteux ? *(Réponse : $25\times 9=225$.)*

**E18.5.** Refaire le retournement du § 18.1 pour l'intervalle **unilatéral**. *À quelle ligne la
démarche diffère-t-elle ?*

**E18.6 — orientée finance.** Sur 60 rendements mensuels d'écart-type supposé connu
$\sigma=4\,\%$, quelle est la marge d'erreur à 95 % sur le rendement moyen mensuel ? Convertir en
rendement annuel. Sur combien d'années faudrait-il observer pour ramener la marge annuelle sous
1 point ? *(L'ordre de grandeur obtenu est le vrai enseignement.)*

---

## 18.8 À retenir

- **Construction en trois temps** : pivot → **retournement** algébrique → intervalle. Aucune
  approximation à aucune ligne.
- ⚠️ **Le retournement ne transfère pas l'aléa sur $\mu$** : ce sont les **bornes** qui sont
  aléatoires.
- $1{,}96=\Phi^{-1}(0{,}975)$ — le $/2$ vient des **deux** queues d'un intervalle bilatéral.
- **Marge en $1/\sqrt n$** : diviser la précision par 2 coûte $\times 4$ en effectif ;
  $n\ge\left(\frac{z\sigma}{m}\right)^2$ pour une marge visée.
- Quand $\sigma$ est connu, **tous les intervalles ont la même largeur**. C'est ce qui cessera
  dès qu'il est estimé, et c'est de là que naît la loi de Student.

---

⬅️ [Module 17 — Estimation et quantité pivotale](17-estimation-et-quantite-pivotale.md) ·
➡️ [Module 19 — Interpréter la confiance](19-interpretation-de-la-confiance.md) ·
🏠 [Sommaire](README.md)
