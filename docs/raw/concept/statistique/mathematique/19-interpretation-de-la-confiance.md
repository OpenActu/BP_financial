# Module 19 — Interpréter la confiance ⭐

**Durée : 1 h 15.** Prérequis : module [18](18-intervalle-de-confiance.md).

> **La question traitée.** L'énoncé « il y a 95 % de chances que $\mu$ soit dans cet intervalle »
> est-il correct ?

**Ce qui est en jeu.** La réponse est **non**, et l'erreur est la plus répandue de toute la
statistique appliquée. Ce module en donne la raison, la formulation correcte, et l'argument qui
clôt le débat.

---

## 19.1 Pourquoi c'est faux

> **« Il y a 95 % de chances que $\mu$ soit entre 100,06 et 106,34 » est FAUX.**

Dans le cadre **fréquentiste** — celui de tout ce cours —, une probabilité décrit la fréquence
d'un événement dans une **expérience répétable**. Or :

- $\mu$ est une **constante inconnue**. Elle ne varie pas d'un échantillon à l'autre ; elle n'a
  pas de loi.
- $[100{,}06\;;\;106{,}34]$ est un intervalle **numérique**, entièrement déterminé : il a été
  calculé, il ne contient plus rien d'aléatoire.

Deux constantes : soit $\mu\in[100{,}06\,;\,106{,}34]$, soit $\mu\notin[100{,}06\,;\,106{,}34]$.
La « probabilité » vaut donc **0 ou 1** — on ne sait simplement pas laquelle.

Dire « 95 % de chances » revient à attribuer une probabilité à un fait déjà déterminé. C'est
comme lancer une pièce, la couvrir de la main, et dire qu'il y a 50 % de chances qu'elle soit sur
pile : le résultat est fixé, c'est **notre information** qui est incomplète — et l'incomplétude
de l'information n'est pas une probabilité, dans ce cadre-là.

> 🔑 C'est le [§ 18.1](18-intervalle-de-confiance.md) qui contenait déjà la réponse : le
> retournement algébrique **n'a pas transféré l'aléa sur $\mu$**. Ce sont les bornes qui étaient
> aléatoires, et elles ont cessé de l'être dès qu'on a calculé $\bar x$.

---

## 19.2 La formulation correcte

> **Si l'on répétait l'expérience un grand nombre de fois, 95 % des intervalles ainsi construits
> contiendraient $\mu$.**

Les 95 % qualifient la **procédure**, pas le résultat particulier. On parle parfois d'intervalle
« à 95 % de confiance » plutôt que « de probabilité » précisément pour marquer cette nuance.

### Formulations acceptables et inacceptables

| ❌ À proscrire | ✅ Correct |
|---|---|
| « 95 % de chances que $\mu$ soit dans l'intervalle » | « 95 % des intervalles construits ainsi contiennent $\mu$ » |
| « $\mu$ a 95 % de probabilité d'être proche de 103,2 » | « J'ai une confiance de 95 % dans cet intervalle » |
| « 95 % des observations sont dans l'intervalle » | *(faux et sans rapport — voir § 19.4, erreur n° 1)* |
| « 95 % des échantillons ont une moyenne dans cet intervalle » | *(faux — voir § 19.4, erreur n° 4)* |

### La démonstration par simulation

C'est le seul argument qui convainc vraiment. Voir S19.1 : sur 200 000 répétitions, la
proportion d'intervalles contenant $\mu$ vaut 95 % — **et l'on voit lesquels ratent**. Sur un
graphique de 40 intervalles, un ou deux manquent la cible, et rien ne les distingue des autres
de l'extérieur. C'est exactement la situation où vous êtes avec votre unique intervalle.

---

## 19.3 L'argument décisif : un intervalle dont on SAIT qu'il contient le paramètre

Voici un exemple classique qui clôt le débat (dû à Welch, 1939).

Soient $X_1,X_2$ i.i.d. uniformes sur $[\theta-\tfrac12,\;\theta+\tfrac12]$, et considérons
l'intervalle $\bigl[\min(X_1,X_2),\;\max(X_1,X_2)\bigr]$.

- Sa **couverture est exactement 50 %** : $\theta$ est entre les deux points si et seulement si
  l'un est en dessous et l'autre au-dessus, soit $2\times\frac12\times\frac12=\frac12$. C'est
  donc un intervalle de confiance à 50 %, en toute rigueur.
- **Mais** si l'on observe $|X_1-X_2|>\tfrac12$, alors $\theta$ est **certainement** dedans. En
  effet, si les deux points étaient du même côté de $\theta$, ils seraient tous deux dans un
  intervalle de longueur $\tfrac12$, et leur écart ne pourrait pas dépasser $\tfrac12$.

On a donc un intervalle « à 50 % de confiance » dont on peut, dans certains cas, être **sûr à
100 %** qu'il contient le paramètre — et dans d'autres cas moins sûr.

> 🔑 **Conclusion.** Le « 95 % » (ou le « 50 % ») est une propriété de la **procédure**, moyennée
> sur tous les échantillons possibles. Ce n'est pas une propriété de **l'intervalle que vous avez
> sous les yeux**. Confondre les deux, c'est l'erreur d'interprétation la plus répandue en
> statistique.

### La réconciliation bayésienne

Cette gêne n'est pas une subtilité gratuite : elle vient de ce que **l'intuition des gens est
bayésienne** alors que la formule enseignée ne l'est pas.

Dans le cadre bayésien, $\mu$ **est** traité comme une variable aléatoire, munie d'une loi
*a priori*. On calcule alors sa loi *a posteriori* et l'on construit un **intervalle de
crédibilité** — pour lequel la phrase « il y a 95 % de probabilité que $\mu$ soit dedans » est
**parfaitement correcte**.

Le fait remarquable : avec un *a priori* non informatif sur $\mu$ et $\sigma$ connu, l'intervalle
de crédibilité bayésien à 95 % est **numériquement identique** à l'IC fréquentiste du
[§ 18.4](18-intervalle-de-confiance.md), soit $[100{,}06\;;\;106{,}34]$. Mêmes bornes,
interprétations différentes.

⚠️ Cette coïncidence ne vaut **pas** en général — elle dépend de l'*a priori* choisi et du modèle.
Elle ne justifie donc pas d'employer la formulation bayésienne pour un résultat fréquentiste :
tant que vous travaillez dans ce cadre, dites « 95 % des intervalles ».

---

## 19.4 Cinq erreurs fréquentes

| # | Erreur | Pourquoi c'est faux |
|---|---|---|
| 1 | « 95 % des **observations** sont dans l'IC » | L'IC encadre $\mu$, pas les $X_i$. Sur l'exemple il a une largeur de 6,3 alors que les observations ont un écart-type de 8 : la plupart tombent **hors** de l'IC |
| 2 | Utiliser $\sigma$ au lieu de $\sigma/\sqrt n$ | Confondre dispersion des données et dispersion de la moyenne. C'est l'erreur de calcul la plus courante |
| 3 | Prendre $z_{0{,}95}=1{,}645$ pour un IC à 95 % | Oubli du caractère **bilatéral** : c'est $\alpha/2$ dans chaque queue |
| 4 | « 95 % des futures moyennes tomberont dans cet IC » | Non : cet intervalle est centré sur $\bar x$, pas sur $\mu$. La bonne notion est l'**intervalle de prédiction** |
| 5 | Comparer deux IC qui se chevauchent et conclure « pas de différence » | Faux raisonnement : deux IC peuvent se chevaucher alors que la différence est significative. Il faut construire l'IC **de la différence** |

---

## 19.5 Simulations

### S19.1 — Voir les intervalles qui ratent

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(42)
MU, SIGMA, n = 100.0, 8.0, 25
marge = stats.norm.ppf(0.975) * SIGMA / np.sqrt(n)

k = 40
xb = rng.normal(MU, SIGMA, size=(k, n)).mean(axis=1)
touche = np.abs(xb - MU) <= marge

fig, ax = plt.subplots(figsize=(6, 8))
for i, (m, ok) in enumerate(zip(xb, touche)):
    ax.plot([m - marge, m + marge], [i, i], color="tab:blue" if ok else "tab:red", lw=2)
    ax.plot(m, i, "o", color="tab:blue" if ok else "tab:red", ms=3)
ax.axvline(MU, color="k", ls="--", label="vrai μ")
ax.set_title(f"{k} intervalles — {(~touche).sum()} ratent la cible")
ax.legend(); plt.tight_layout(); plt.show()
```

Environ 2 intervalles sur 40 manquent $\mu$. **Rien ne les distingue des autres** : ils ne sont
ni plus larges, ni visiblement anormaux. Vu de l'intérieur — c'est-à-dire sans connaître $\mu$ —
ils sont indiscernables. C'est exactement votre situation avec votre unique intervalle.

### S19.2 — La couverture conditionnelle (l'exemple de Welch)

```python
rng2 = np.random.default_rng(7)
N = 500_000
theta = 0.0
X = rng2.uniform(theta - 0.5, theta + 0.5, size=(N, 2))
lo, hi = X.min(axis=1), X.max(axis=1)
couvre = (lo < theta) & (theta < hi)
large = (hi - lo) > 0.5

print(f"couverture globale                      : {couvre.mean():.4f}   (théorie 0,50)")
print(f"couverture quand l'écart dépasse 0,5    : {couvre[large].mean():.4f}   (théorie 1,00)")
print(f"couverture quand l'écart est sous 0,5   : {couvre[~large].mean():.4f}")
print(f"proportion de cas 'écart > 0,5'         : {large.mean():.4f}")
```

Un intervalle « à 50 % » qui, dans un sous-ensemble identifiable des cas, contient le paramètre
**avec certitude**. C'est la preuve par l'exemple que le niveau de confiance qualifie la
procédure, pas l'intervalle obtenu.

### S19.3 — L'erreur n° 1 du § 19.4

```python
X = rng.normal(MU, SIGMA, size=n)
xb = X.mean(); lo, hi = xb - marge, xb + marge
part = np.mean((X >= lo) & (X <= hi))
print(f"IC = [{lo:.2f}, {hi:.2f}]  (largeur {hi-lo:.2f})")
print(f"proportion des OBSERVATIONS dans l'IC : {part:.2f}")
```

Environ **30 %** seulement. L'IC encadre la **moyenne**, pas les observations — et il est bien
plus étroit que la dispersion des données.

---

## 19.6 Exercices

**E19.1.** Un collègue affirme : « mon IC à 95 % est [100 ; 106], donc si je refais l'expérience,
la nouvelle moyenne aura 95 % de chances d'être dans cet intervalle. » Réfuter en deux phrases,
puis calculer par simulation la vraie probabilité. *(Elle vaut environ 83 % — l'intervalle est
centré sur $\bar x$, pas sur $\mu$, et la nouvelle moyenne porte son propre aléa.)*

**E19.2.** Reprendre l'exemple de Welch (§ 19.3) et démontrer les deux affirmations : couverture
$1/2$, et couverture certaine quand $|X_1-X_2|>1/2$.

**E19.3.** Deux traitements ont pour IC à 95 % $[2{,}1\,;\,5{,}9]$ et $[5{,}4\,;\,9{,}2]$. Ils se
chevauchent. Peut-on conclure à l'absence de différence significative ? *(Erreur n° 5 du § 19.4 —
justifier.)*

**E19.4.** Pourquoi la largeur d'un IC est-elle sans rapport avec la dispersion des observations ?
*Illustrer avec la simulation S19.3.*

**E19.5.** Dans quel cadre la phrase « il y a 95 % de probabilité que $\mu$ soit dedans »
devient-elle correcte ? *Que faut-il ajouter au modèle pour cela ?*

---

## 19.7 À retenir

- ⚠️ **« 95 % de chances que $\mu$ soit dedans » est faux.** $\mu$ est une constante, l'intervalle
  calculé aussi : la probabilité vaut 0 ou 1.
- **La formulation correcte** : « 95 % des intervalles construits ainsi contiennent $\mu$ ». Les
  95 % qualifient la **procédure**, pas le résultat.
- ⭐ **L'exemple de Welch** clôt le débat : un IC « à 50 % » peut, dans des cas identifiables,
  contenir le paramètre à coup sûr.
- **L'intuition des gens est bayésienne.** L'intervalle de **crédibilité** autorise la phrase
  interdite — mais c'est un autre cadre, et la coïncidence numérique n'est pas générale.
- **Cinq erreurs à connaître**, dont la plus fréquente : confondre l'IC de la moyenne avec la
  dispersion des observations.

---

⬅️ [Module 18 — L'intervalle de confiance](18-intervalle-de-confiance.md) ·
🏠 [Sommaire](README.md) ·
➡️ **Suite** : [Cours sur la loi de Student](../loi-de-student/README.md)
