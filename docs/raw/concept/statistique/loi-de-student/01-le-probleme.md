# Module 1 — Le problème que Student résout

**Durée : 2 h.** Objectif : comprendre *pourquoi* une nouvelle loi est nécessaire, avant d'en voir
la construction. Ce module ne contient presque aucune démonstration — il contient une
**expérience**.

---

## 1.1 Le point de départ : le cas confortable

Soit $X_1,\dots,X_n$ i.i.d. $\mathcal N(\mu,\sigma^2)$, avec $\sigma$ **connu**. Alors

$$Z=\frac{\bar X-\mu}{\sigma/\sqrt n}\;\sim\;\mathcal N(0,1)$$

et tout en découle : intervalle de confiance$\bar X \pm 1{,}96\,\sigma/\sqrt n$, test
de$H_0:\mu=\mu_0$,$p$-valeur lue dans la table normale.

Ce résultat est **exact** (pas asymptotique) dès lors que les$X_i$ sont gaussiens, et
approximativement valide sinon, par le TCL.

> ➡️ Ce cas confortable est traité en détail au [module 18 du cours de statistique](../mathematique/18-intervalle-de-confiance.md) : construction du pivot, retournement
> algébrique, origine du 1,96 et interprétation. **Toute la suite du cours n'en est qu'une
> transposition** — même structure, autre loi tabulée.

## 1.2 Le problème : $\sigma$ n'est jamais connu

Dans quelle situation réelle connaît-on la variance de la population sans en connaître la
moyenne ? Pratiquement aucune. On mesure la volatilité d'un titre, la dispersion d'un procédé,
l'écart-type d'une série de rendements — jamais on ne la reçoit d'ailleurs.

Il faut donc l'estimer :

$$S^2=\frac{1}{n-1}\sum_{i=1}^n (X_i-\bar X)^2$$

et former la statistique **calculable**

$$T=\frac{\bar X-\mu}{S/\sqrt n}$$

**Ce n'est plus la même chose.** Dans $Z$, le dénominateur est une constante ; dans $T$, c'est
une **variable aléatoire**. On a introduit une **seconde source d'aléa**, et elle se trouve au
dénominateur — là où elle fait le plus de dégâts.

### L'intuition du mécanisme

Considérez ce qui se passe lorsque, par malchance, $S$ sous-estime $\sigma$ :

- le dénominateur $S/\sqrt n$ est trop petit ;
- le rapport $T$ est donc **gonflé** ;
- et cet événement n'est pas rare : sur un petit échantillon, $S$ est très instable.

Symétriquement, une surestimation de $S$ écrase $T$ vers 0. Mais les deux effets **ne se
compensent pas** : diviser par un nombre trop petit produit un effet bien plus violent que
diviser par un nombre trop grand. Le résultat est une loi **plus dispersée que la normale**,
et surtout à **queues plus épaisses** — les grandes valeurs de $|T|$ y sont nettement plus
probables.

> 🔑 Toute la loi de Student tient dans cette phrase : **elle est la loi normale corrigée du
> fait qu'on a dû estimer le dénominateur.**

---

## 1.3 L'expérience fondatrice — à faire, pas à lire

C'est le cœur du module. Simulez, ne prenez pas le résultat pour acquis.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(1)
MU, SIGMA = 0.0, 1.0

for n in (3, 5, 10, 15, 20, 30, 60, 120):
    X = rng.normal(MU, SIGMA, size=(200_000, n))
    Xbar = X.mean(axis=1)
    S = X.std(axis=1, ddof=1)                 # ddof=1 → diviseur n-1

    Z = (Xbar - MU) / (SIGMA / np.sqrt(n))    # sigma CONNU  → normal
    T = (Xbar - MU) / (S / np.sqrt(n))        # sigma ESTIMÉ → Student

    print(f"n={n:4d} | P(|Z|>1,96) = {np.mean(np.abs(Z) > 1.96):.3f}"
          f" | P(|T|>1,96) = {np.mean(np.abs(T) > 1.96):.3f}"
          f" | t(n-1;0,975) = {stats.t.ppf(0.975, n - 1):.3f}")
```

### Le résultat qui doit surprendre

La colonne $Z$ donne $0{,}050$ partout, comme attendu. La colonne $T$, elle, donne :

| $n$                                  | 3          | 5          | 10    | 15    | 20    | 30    | 60    | 120   |
| ------------------------------------ | ---------- | ---------- | ----- | ----- | ----- | ----- | ----- | ----- |
| **Risque réel** si l'on emploie 1,96 | **18,9 %** | **12,2 %** | 8,2 % | 7,0 % | 6,5 % | 6,0 % | 5,5 % | 5,2 % |
| Quantile correct $t_{n-1;\,0{,}975}$ | 4,303      | 2,776      | 2,262 | 2,145 | 2,093 | 2,045 | 2,001 | 1,980 |

**Lecture.** À $n=5$, croire travailler au risque de 5 % alors qu'on est en réalité à 12,2 % :
le risque d'erreur est **multiplié par 2,4**. À $n=3$, il est multiplié par près de 4.

Notez aussi la **lenteur** de la convergence : il faut $n\approx 60$ pour que l'écart tombe sous
un demi-point, et le quantile vaut encore $1{,}980$ à $n=120$. La règle « au-delà de 30, on peut
prendre la normale » est une commodité, pas un théorème.

### Visualisation complémentaire

```python
import matplotlib.pyplot as plt

n = 5
X = rng.normal(0, 1, size=(200_000, n))
T = X.mean(axis=1) / (X.std(axis=1, ddof=1) / np.sqrt(n))

grille = np.linspace(-6, 6, 600)
plt.hist(T, bins=400, range=(-6, 6), density=True, alpha=.4, label=f"T simulé, n={n}")
plt.plot(grille, stats.norm.pdf(grille), label="N(0,1)")
plt.plot(grille, stats.t.pdf(grille, n - 1), "--", label=f"Student({n-1})")
plt.yscale("log")        # ⚠️ échelle log : sans elle, les queues sont invisibles
plt.legend(); plt.show()
```

⚠️ **L'échelle logarithmique n'est pas un détail.** En échelle linéaire, la densité de Student
et celle de la normale paraissent presque confondues : la différence se joue dans les queues,
où les densités sont petites — et ce sont précisément les queues qui déterminent les valeurs
critiques d'un test. C'est une leçon générale : *un test se juge sur ses queues, pas sur son
centre.*

---

## 1.4 Ce que Fisher–Cochran devra établir

L'expérience montre que $T$ suit une loi bien définie, tabulée, indépendante de $\mu$ et de
$\sigma$. Encore faut-il la **démontrer**. Il faudra pour cela trois résultats :

1. quelle est la loi de $S^2$ ? → **[module 15 du cours de statistique](../mathematique/15-loi-du-chi2.md)** (loi du $\chi^2$) ;
2. $\bar X$ et $S^2$ sont-ils indépendants ? → **[module 16](../mathematique/16-theoreme-de-fisher-cochran.md)** (Fisher–Cochran) ;
3. quelle est la loi du rapport ainsi formé ? → **[module 4](04-construction-et-proprietes.md)** de ce cours-ci.

Le point 2 est le plus surprenant : $\bar X$ et $S^2$ sont calculés sur les **mêmes données**.
Rien ne laisse présager leur indépendance — et elle est pourtant la clé de tout l'édifice.

---

## 1.5 Repère historique

L'auteur est **William Sealy Gosset** (1876–1937), chimiste puis statisticien à la brasserie
**Guinness**, à Dublin. Il publie en 1908 dans *Biometrika* un article de quinze pages,
*The probable error of a mean*, sous le pseudonyme **« Student »** — Guinness interdisait à ses
employés de publier, après qu'un salarié eut divulgué un secret de fabrication.

Le problème de Gosset était strictement industriel : juger la qualité d'un lot d'orge ou de
houblon sur **quatre ou cinq mesures**, parce qu'analyser davantage coûtait trop cher. Les
méthodes de son époque, calibrées sur les grands échantillons de l'astronomie et de la
démographie, y étaient inutilisables.

C'est **R. A. Fisher** qui, à partir de 1912, donnera la démonstration rigoureuse et introduira
la formulation en degrés de liberté que nous utilisons aujourd'hui. La notation $t$ est de
Fisher ; le nom « Student » est resté.

> 🔑 **La morale est méthodologique.** Student est né d'une **contrainte de petits effectifs**,
> pas d'un raffinement théorique. Chaque fois que vous disposez de peu d'observations — une
> série mensuelle sur un an, quelques mesures coûteuses, un historique court — vous êtes dans
> la situation de Gosset, et la correction est indispensable.

---

## 1.6 Exercices

**E1.1.** Reproduire le tableau du § 1.3. Ajouter une colonne donnant le facteur de gonflement
du risque (risque réel ÷ 0,05).

**E1.2.** À $n=10$, quelle valeur critique faudrait-il employer avec la table normale pour
obtenir un risque réel de 5 % ? Comparer à $t_{9;\,0{,}975}=2{,}262$. *(Réponse : il faut
précisément ce quantile — c'est la définition même de la table de Student.)*

**E1.3.** Reprendre l'expérience du § 1.3 avec des $X_i$ **non gaussiens** (exponentiels
centrés, par exemple). Le risque réel avec $t_{n-1;\,0{,}975}$ vaut-il encore 5 % ? Observer que
l'écart se résorbe quand $n$ croît. *Ce résultat est repris au module 8 : la normalité est
l'hypothèse la moins critique du dispositif.* ⚠️ Regardez les **deux queues séparément** : la
couverture bilatérale masque des erreurs qui se compensent — voir
[module 13 du cours de statistique](../mathematique/13-portee-et-limites-du-tcl.md), § 9.2.

**E1.4 — orientée finance.** Prendre une série de rendements quotidiens (via
`historique_sbf250.py`) et calculer, sur des fenêtres glissantes de 5, 20 et 60 séances, le
rapport $\bar X/(S/\sqrt n)$. Sur quelle fenêtre l'écart entre quantile normal et quantile de
Student change-t-il matériellement la conclusion ?

---

## 1.7 À retenir

- Remplacer $\sigma$ par $S$ **change la loi** de la statistique : ce n'est pas une
  approximation négligeable sur petit échantillon.
- La loi obtenue est symétrique, centrée, mais **à queues plus épaisses** que la normale.
- L'erreur consistant à employer $1{,}96$ au lieu de $t_{n-1;\,0{,}975}$ **augmente toujours le
  risque de première espèce** — elle rend le test trop permissif, jamais trop prudent.
- L'écart est **négligeable pour $n$ grand**, mais la convergence est lente.

---

⬅️ [Module 0 — Mise à niveau](00-mise-a-niveau.md) ·
➡️ [Module 4 — Construction et propriétés](04-construction-et-proprietes.md)

> 📐 **Détour requis avant le module 4.** La loi du $\chi^2$ et le théorème de Fisher–Cochran,
> qui sont les deux outils de la construction, appartiennent au cours de statistique —
> [modules 15](../mathematique/15-loi-du-chi2.md) et
> [16](../mathematique/16-theoreme-de-fisher-cochran.md).

---

⬅️ [Module 0 — Mise à niveau](00-mise-a-niveau.md) ·
➡️ [Outils : loi du $\chi^2$](../mathematique/15-loi-du-chi2.md) et [Fisher–Cochran](../mathematique/16-theoreme-de-fisher-cochran.md) ·
🏠 [Sommaire](README.md)
