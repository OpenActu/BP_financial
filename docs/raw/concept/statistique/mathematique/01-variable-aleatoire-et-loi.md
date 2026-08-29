# Module 1 — Variable aléatoire et loi

**Durée : 1 h 15.** Point d'entrée du cours. Aucun prérequis au-delà des sommes et des
intégrales.

> **La question traitée.** Le [cours d'algèbre](../../algebre/README.md) traite une série de $n$ nombres **déjà observés**. Comment décrire ce qui aurait **pu** être observé — et qui le sera demain ?

**Ce qui est en jeu.** C'est le passage du descriptif au génératif, et il tient dans un seul objet :
la **loi**. Tout le reste du cours — espérance, variance, transformées, convergences — n'est que
l'exploitation de cet objet.

---

## 1.1 Le renversement : de la série au modèle

Le [cours d'algèbre](../../algebre/README.md) répond à des questions du type *« quelle est la tendance de ces 250 cours ? »*. La réponse est un nombre, exact, vérifiable, et **définitif** : elle ne dépend d'aucune hypothèse.

Elle ne permet pourtant pas de décider, parce qu'elle ne dit rien de ceci :

> Si l'histoire recommençait, obtiendrais-je à peu près la même tendance — ou une toute autre ?

Répondre exige de considérer les 250 cours observés comme **une réalisation parmi d'autres
possibles**. C'est un ajout au réel, pas une lecture du réel : on **postule** un mécanisme générateur.

|                       | Cours d'algèbre                   | Ce cours                                       |
| --------------------- | --------------------------------- | ---------------------------------------------- |
| Objet                 | $n$ nombres observés              | Un **mécanisme** qui produit des nombres       |
| Statut des résultats  | Identités, toujours vraies        | Énoncés **conditionnels au modèle**            |
| Question typique      | « Combien vaut la corrélation ? » | « Cette corrélation est-elle reproductible ? » |
| Ce qui peut être faux | Rien                              | **Le modèle**                                  |

> ⚠️ **Cette ligne du bas est la plus importante du cours.** Un résultat probabiliste n'est
> jamais vrai « en soi » : il est vrai **si** le modèle l'est. Tout le  [module 14](14-dependance-et-echec-du-tcl.md) consiste à montrer ce qu'il advient quand il ne l'est pas.

---

## 1.2 Variable aléatoire

> **Définition (opérationnelle).** Une **variable aléatoire** $X$ est une grandeur numérique
> dont la valeur dépend d'une expérience dont l'issue n'est pas déterminée : c'est une
> **fonction** de l'issue, pas un nombre.

Trois conventions de notation qu'il faut respecter dès maintenant, sous peine de confusion
permanente dans tout le cours :

| Notation        | Objet                      | Statut                               |
| --------------- | -------------------------- | ------------------------------------ |
| $X$ (majuscule) | La variable aléatoire      | **Non observée** — une fonction      |
| $x$ (minuscule) | Une valeur particulière    | Un **nombre**                        |
| $X_1,\dots,X_n$ | L'échantillon avant tirage | $n$ variables aléatoires             |
| $x_1,\dots,x_n$ | Les données                | $n$ nombres, ceux du cours d'algèbre |

> 🔑 **La distinction majuscule/minuscule porte tout le cours.** $\bar X$ est une variable
> aléatoire — elle a une loi, une espérance, une variance. $\bar x=103{,}2$ est un nombre — il
> n'a rien de tout cela. Confondre les deux est la source de l'erreur d'interprétation du
> [module 19](19-interpretation-de-la-confiance.md).

---

## 1.3 La loi : ce qui décrit entièrement une variable aléatoire

> **Définition.** La **loi** de $X$ est la donnée, pour toute partie $A\subset\mathbb R$, de $P(X\in A)$ — la probabilité que $X$ tombe dans $A$.

C'est **tout** ce qu'on peut savoir de $X$ sans l'observer. Deux variables de même loi sont
interchangeables pour toute question probabiliste, même si elles décrivent des expériences sans
aucun rapport.

⚠️ **La loi n'est pas la valeur.** Connaître la loi ne dit pas ce qui va sortir ; cela dit
seulement avec quelle fréquence chaque issue sortirait si l'on recommençait indéfiniment.

### Les deux familles

|                        | **Discrète**                     | **Continue**                     |
| ---------------------- | -------------------------------- | -------------------------------- |
| Valeurs                | Dénombrables : $\{0,1,2,\dots\}$ | Un intervalle de $\mathbb R$     |
| Décrite par            | $p(k)=P(X=k)$                    | Une **densité** $f$              |
| Normalisation          | $\sum_k p(k)=1$                  | $\int_{\mathbb R} f(x)\,dx=1$    |
| Probabilité d'un point | $p(k)$, souvent $>0$             | **Toujours nulle** : $P(X=x)=0$  |
| Exemples               | Bernoulli, binomiale, Poisson    | Normale, exponentielle, uniforme |

> ⚠️ **Pour une loi continue, $P(X=x)=0$ pour tout $x$** — et pourtant $X$ prend bien une valeur.
> La densité $f(x)$ n'est **pas** une probabilité : c'est une probabilité **par unité de longueur**. Elle peut dépasser 1 (celle d'une uniforme sur $[0;0{,}1]$ vaut 10), ce qu'aucune probabilité ne peut faire.

Seul un **intervalle** a une probabilité :

$$P(a\le X\le b)=\int_a^b f(x)\,dx$$

---

## 1.4 La fonction de répartition

C'est la description qui marche dans les deux cas, et c'est elle que manipulent les tests.

> **Définition.** $F_X(x)=P(X\le x)$, pour $x\in\mathbb R$.

| Propriété                   | Énoncé                                       |
| --------------------------- | -------------------------------------------- |
| Croissante                  | $x\le y\Rightarrow F(x)\le F(y)$             |
| Limites                     | $F(-\infty)=0$, $F(+\infty)=1$               |
| Continue à droite           | Toujours ; **des sauts** dans le cas discret |
| Lien à la densité           | $F'=f$ là où $f$ est continue                |
| Probabilité d'un intervalle | $P(a<X\le b)=F(b)-F(a)$                      |

> 🔑 **$F$ caractérise la loi** : deux variables de même fonction de répartition ont la même loi.
> C'est ce qui rend légitime le **test de Kolmogorov–Smirnov**, employé dans presque toutes les
> simulations de ce cours : il compare deux fonctions de répartition, donc deux lois.

### Le quantile : la fonction de répartition, lue à l'envers

> **Définition.** Le **quantile d'ordre $p$** est $q_p=F^{-1}(p)$ : la valeur telle que $P(X\le q_p)=p$.

C'est l'objet dont vit toute la partie VI. Le fameux **1,96** du [module 18](18-intervalle-de-confiance.md) est le quantile d'ordre $0{,}975$ de la loi normale centrée réduite, et rien d'autre.

| Terme courant                | Ordre $p$               |
| ---------------------------- | ----------------------- |
| Médiane                      | $0{,}5$                 |
| Premier / troisième quartile | $0{,}25$ / $0{,}75$     |
| VaR à 99 %                   | $0{,}01$ sur les pertes |

---

## 1.5 Le vocabulaire de l'échantillon : i.i.d.

Toute la suite du cours porte sur$X_1,\dots,X_n$ **i.i.d.** — abréviation à décomposer, car chaque
lettre est une hypothèse distincte et **séparément réfutable** :

|                   | Signification                      | Ce que sa violation produit                                             |
| ----------------- | ---------------------------------- | ----------------------------------------------------------------------- |
| **i**ndépendantes | Aucune ne renseigne sur les autres | [Module 14](14-dependance-et-echec-du-tcl.md) — **le cas grave**        |
| **i**dentiquement | Toutes de même loi                 | Relâchable (Lindeberg–Feller, [§ 13.5](13-portee-et-limites-du-tcl.md)) |
| **d**istribuées   | —                                  | —                                                                       |

> ⚠️ **« i.i.d. » est une hypothèse sur le mécanisme, jamais une propriété des données.** Aucun
> jeu de nombres n'est « i.i.d. » : c'est le protocole qui le rend plausible ou non. Des cours de
> bourse successifs ne le sont manifestement pas ; des rendements le sont approximativement ;
> des mesures répétées sur le même patient ne le sont pas du tout.

---

## 1.6 Les lois à connaître

Six lois suffisent pour tout le cours. Les colonnes espérance et variance reposent sur les
[modules 2](02-esperance.md) et [3](03-variance-et-moments.md) ; **chacune est démontrée deux fois** — directement puis par la fonction caractéristique — dans le module indiqué en première
colonne.

| Loi                                                             | Paramètres     | Support         | $E(X)$          | $\operatorname{Var}(X)$ | Où elle sert                                        |
| --------------------------------------------------------------- | -------------- | --------------- | --------------- | ----------------------- | --------------------------------------------------- |
| [Bernoulli $\mathcal B(p)$](06a-loi-de-bernoulli.md)            | $p$            | $\{0,1\}$       | $p$             | $p(1-p)$                | Tableau du [§ 13.2](13-portee-et-limites-du-tcl.md) |
| [Binomiale $\mathcal B(n,p)$](06b-loi-binomiale.md)             | $n,p$          | $\{0,\dots,n\}$ | $np$            | $np(1-p)$               | Somme de Bernoulli                                  |
| [Poisson $\mathcal P(\lambda)$](06c-loi-de-poisson.md)          | $\lambda$      | $\mathbb N$     | $\lambda$       | $\lambda$               | Comptages                                           |
| [Uniforme $\mathcal U(a,b)$](06d-loi-uniforme.md)               | $a,b$          | $[a,b]$         | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$    | Contre-exemples, simulation                         |
| [Exponentielle $\mathcal E(\lambda)$](06e-loi-exponentielle.md) | $\lambda$      | $\mathbb R^+$   | $\frac1\lambda$ | $\frac1{\lambda^2}$     | Contre-épreuves du cours                            |
| [**Normale** $\mathcal N(\mu,\sigma^2)$](06f-loi-normale.md)    | $\mu,\sigma^2$ | $\mathbb R$     | $\mu$           | $\sigma^2$              | **Tout le cours**                                   |

Deux lois figurent aussi au programme comme **cas pathologiques**, et il faut savoir pourquoi :

- **Cauchy** — densité $\frac{1}{\pi(1+x^2)}$ : **aucune espérance**, donc aucune variance. Ni
  loi des grands nombres ni TCL ([§ 13.1](13-portee-et-limites-du-tcl.md)).
- **Log-normale** — $e^Z$ avec $Z$ gaussienne : espérance et variance finies, mais **aucune FGM**
  ([§ 5.5](05-fonction-generatrice-des-moments.md)) et une asymétrie de 6,18 qui rend l'approximation normale très lente ([§ 13.2](13-portee-et-limites-du-tcl.md)).

---

## 1.7 Transformer une variable aléatoire

Une fonction d'une variable aléatoire en est une autre. Deux cas suffisent :

**Transformation affine** — la seule utilisée en permanence :

$$Y=aX+b\qquad\Longrightarrow\qquad F_Y(y)=F_X\!\left(\frac{y-b}{a}\right)\ \ (a>0),
\qquad f_Y(y)=\frac1{|a|}f_X\!\left(\frac{y-b}{a}\right)$$

Le facteur $\frac1{|a|}$ est la conservation de la masse totale : étirer l'axe d'un facteur $a$
oblige à écraser la densité d'autant.

**Standardisation** — le cas particulier qui structure tout le cours :

$$Z=\frac{X-\mu}{\sigma}$$

ramène toute variable à espérance 0 et variance 1. C'est l'étape 0 de la démonstration du
[TCL](12-theoreme-central-limite.md), et c'est ce qui permet **une seule table** de quantiles au
lieu d'une par valeur de $(\mu,\sigma)$.

> ⚠️ **Une transformation non linéaire ne se comporte pas ainsi.** $E(g(X))\ne g(E(X))$ en
> général : c'est l'objet du [§ 2.5](02-esperance.md), et la raison pour laquelle
> l'écart-type empirique $S$ est biaisé alors que $S^2$ ne l'est pas.

---

## 1.8 Simulations

### S1.1 — Densité, fonction de répartition, quantile : les trois vues du même objet

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(1)
N = 500_000
X = rng.normal(50, 8, N)

# 1. la densité n'est PAS une probabilité
print(f"densite d'une U(0, 0.1) en 0.05 : {stats.uniform.pdf(0.05, 0, 0.1):.1f}  (> 1 !)")
print(f"P(X = 50) estimee : {np.mean(X == 50.0):.6f}   (nulle, loi continue)")

# 2. seul un intervalle a une probabilité
for a, b in [(42, 58), (34, 66), (26, 74)]:
    emp = np.mean((X >= a) & (X <= b))
    th = stats.norm.cdf(b, 50, 8) - stats.norm.cdf(a, 50, 8)
    print(f"P({a} <= X <= {b}) : empirique {emp:.4f}   theorie {th:.4f}")

# 3. quantile = fonction de repartition lue a l'envers
for p in (0.025, 0.5, 0.975):
    print(f"q_{p} : empirique {np.quantile(X, p):7.3f}   theorie {stats.norm.ppf(p, 50, 8):7.3f}")
```

Les trois blocs sont **le même contenu** lu de trois façons. La dernière ligne donne
$q_{0{,}975}=65{,}68$, soit $50+1{,}96\times 8$ : le fameux 1,96 est déjà là.

### S1.2 — La fonction de répartition caractérise la loi

```python
Y = 8 * rng.standard_normal(N) + 50          # même loi que X, construite autrement
Z = rng.uniform(50 - 8*np.sqrt(3), 50 + 8*np.sqrt(3), N)   # mêmes E et Var, autre loi

print("X vs Y (memes E, Var, meme loi)  : KS p =", round(stats.ks_2samp(X, Y).pvalue, 3))
print("X vs Z (memes E, Var, autre loi) : KS p =", f"{stats.ks_2samp(X, Z).pvalue:.1e}")
print(f"   E : {X.mean():.2f} / {Z.mean():.2f}   ecart-type : {X.std():.2f} / {Z.std():.2f}")
```

**Le point est la troisième ligne** : $X$ et $Z$ ont la même espérance et la même variance à la
deuxième décimale, et pourtant ce ne sont **pas** les mêmes lois. Deux nombres ne résument pas
une loi — c'est précisément ce que les modules 2 et 3 ne pourront pas faire, et ce que la
transformée du [module 5](05-fonction-generatrice-des-moments.md) fera.

### S1.3 — i.i.d. : ce que l'hypothèse recouvre

```python
n = 200
iid  = rng.standard_normal(n)                                  # i.i.d.
dep  = np.cumsum(rng.standard_normal(n)) / np.sqrt(np.arange(1, n+1))   # dépendantes
hetero = rng.normal(0, np.linspace(0.2, 3.0, n))               # non identiquement distribuées

for nom, s in [("i.i.d.", iid), ("dependante", dep), ("heterogene", hetero)]:
    autocorr = np.corrcoef(s[:-1], s[1:])[0, 1]
    ratio = s[n//2:].std() / s[:n//2].std()
    print(f"{nom:12s} autocorr(1) = {autocorr:+.3f}   std(2e moitie)/std(1re) = {ratio:.2f}")
```

Les trois séries ont la même allure sur un graphique. Les **deux diagnostics** les séparent :
l'autocorrélation détecte le défaut d'indépendance, le rapport d'écarts-types détecte le défaut
d'homogénéité. Aucun des deux ne se lit à l'œil.

---

## 1.9 Exercices

**E1.1.** Distinguer, dans chacune des phrases suivantes, ce qui relève de $X$ et de $x$ :
« la taille moyenne vaut 172 cm » ; « la moyenne d'un échantillon de 100 personnes a un
écart-type de 0,8 cm » ; « j'ai mesuré 173,2 cm ».

**E1.2.** Montrer que $F$ est croissante et que $P(a<X\le b)=F(b)-F(a)$. *Pourquoi la seconde
formule est-elle vraie dans le cas discret **comme** continu ?*

**E1.3.** La densité d'une $\mathcal U(0;0{,}1)$ vaut 10. Est-ce contradictoire avec le fait
qu'une probabilité soit $\le 1$ ? *Justifier en une phrase.*

**E1.4.** Calculer $F$ pour une loi exponentielle de paramètre $\lambda$, puis en déduire son
quantile d'ordre $p$. *(Réponse : $F(x)=1-e^{-\lambda x}$, $q_p=-\frac{\ln(1-p)}{\lambda}$.)*

**E1.5.** Soit $X\sim\mathcal N(\mu,\sigma^2)$ et $Z=(X-\mu)/\sigma$. Montrer que
$f_Z(z)=\frac{1}{\sqrt{2\pi}}e^{-z^2/2}$ à partir de la règle du § 1.7.

**E1.6.** Pour chacune de ces situations, dire laquelle des trois lettres de « i.i.d. » est en
défaut : (a) températures quotidiennes d'une même ville ; (b) tailles d'élèves de CP et de
terminale mélangés ; (c) résultats de 100 lancers d'une même pièce ; (d) cours de clôture d'une
action.

**E1.7 — orientée finance.** Sur une série obtenue avec `historique_sbf250.py` :
1. tracer la fonction de répartition empirique des rendements quotidiens ;
2. la comparer à celle d'une normale de mêmes espérance et écart-type ;
3. lire sur le graphique le quantile d'ordre $0{,}01$ — la VaR à 99 % — dans les deux cas.
*Lequel des deux est le plus grand en valeur absolue, et qu'est-ce que cela dit du risque d'un
modèle gaussien ?*

---

## 1.10 À retenir

- **Une variable aléatoire n'est pas un nombre** : c'est une fonction de l'issue. $X$ a une loi ;
  $x$ est une valeur.
- **La loi est tout ce qu'on peut savoir sans observer.** Elle se décrit par $p(k)$ (discret),
  une **densité** $f$ (continu), ou — dans les deux cas — la **fonction de répartition** $F$.
- ⚠️ **Une densité n'est pas une probabilité** : elle peut dépasser 1, et $P(X=x)=0$ en continu.
- **$F$ caractérise la loi** ; son inverse est le **quantile**, dont le 1,96 est un cas
  particulier.
- **i.i.d. est une hypothèse sur le mécanisme**, jamais une propriété des nombres — et ses deux
  moitiés se violent séparément.
- ⭐ **Un résultat probabiliste est conditionnel au modèle.** C'est la seule chose que le cours
  d'algèbre n'avait pas à supposer, et c'est ce qui peut être faux.

---

➡️ [Module 2 — L'espérance](02-esperance.md) ·
🏠 [Sommaire](README.md)
