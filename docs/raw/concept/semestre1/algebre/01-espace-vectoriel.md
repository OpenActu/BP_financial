# Module 1 — L'espace vectoriel $\mathbb R^n$

**Durée : 45 min.** Aucun prérequis. **Point d'entrée du cours.**

> **La question traitée.** Tout ce cours parle de « vecteurs de $\mathbb R^n$ ». Qu'est-ce qu'un vecteur, quelles opérations a-t-on le droit d'écrire sur eux — et pourquoi une série de $n$ clôtures en est-elle un ?

**Ce qui est en jeu.** Le geste fondateur de tout le dépôt est de regarder une série de $n$ nombres non pas comme $n$ nombres, mais comme **un seul objet**. Une fois ce pas franchi, « la longueur d'une série », « l'angle entre deux séries », « la série la plus proche » deviennent des phrases sensées — et ce sont exactement la variance, la corrélation et la droite des moindres carrés. Ce module ne démontre presque rien : il rend ce geste légitime, et fixe le vocabulaire que les dix modules suivants emploient sans le redéfinir.

---

## 1.1 Un vecteur, c'est une série vue comme un point

> **Définition.** $\mathbb R^n$ est l'ensemble des **$n$-uplets** de réels :
> $$\mathbb R^n=\bigl\{u=(u_1,u_2,\dots,u_n)\ :\ u_i\in\mathbb R\bigr\}$$
> Ses éléments sont appelés **vecteurs**, et les $u_i$ leurs **coordonnées**. L'entier $n$ est la **dimension** de $\mathbb R^n$ — la notion générale de dimension, valable pour un sous-espace quelconque, vient au [module 7](07-supplementaire-orthogonal-et-dimension.md).

Cinq clôtures consécutives d'une valeur, $98{,}4$ — $99{,}1$ — $97{,}6$ — $100{,}2$ — $101{,}0$, ne sont donc pas cinq nombres : c'est **un** vecteur
$$x=(98{,}4,\ 99{,}1,\ 97{,}6,\ 100{,}2,\ 101{,}0)\in\mathbb R^5$$
L'indice $i$ y désigne la séance, et $n$ la taille de la fenêtre — les $20$ ou $120$ jours de `import_societe.py`.

> ⚠️ **L'ordre des coordonnées fait partie du vecteur.** $(1,2)$ et $(2,1)$ sont deux vecteurs distincts de $\mathbb R^2$. C'est ce qui permet à l'indice $i$ de porter le temps : le vecteur $t=(1,2,\dots,n)$, qui reviendra constamment, n'a de sens que parce que la $i$-ième coordonnée est la $i$-ième séance.

> ⚠️ **Deux séries de longueurs différentes ne vivent pas dans le même espace.** $\mathbb R^5$ et $\mathbb R^{20}$ sont des ensembles disjoints, et aucune opération de ce cours ne relie un vecteur de l'un à un vecteur de l'autre. C'est la raison pour laquelle toute comparaison de deux valeurs exige d'abord des **dates alignées** — un jour férié d'un seul côté suffit à rendre l'addition impossible, et le § 1.6 le montre à l'exécution.

---

## 1.2 Les deux opérations, et seulement elles

Un espace vectoriel n'est pas seulement un ensemble : c'est un ensemble muni de **deux** opérations.

> **Définition (addition et multiplication par un scalaire).** Pour $u,v\in\mathbb R^n$ et $\lambda\in\mathbb R$ :
> $$u+v=(u_1+v_1,\ \dots,\ u_n+v_n)\qquad\text{et}\qquad \lambda u=(\lambda u_1,\ \dots,\ \lambda u_n)$$
> Tout se fait **coordonnée par coordonnée**. Le réel $\lambda$ est appelé un **scalaire**, par opposition au vecteur.

Le vecteur $\mathbf 0=(0,\dots,0)$ est le **vecteur nul**, et $-u=(-1)u$ l'**opposé** de $u$. On note $u-v$ pour $u+(-v)$.

Ces deux opérations ont une lecture immédiate sur des données :

| Écriture             | Ce qu'elle fait à une série                                                        |
| -------------------- | ----------------------------------------------------------------------------------- |
| $x+y$                | additionne deux séries séance par séance — deux lignes d'un même portefeuille      |
| $\lambda x$          | change d'unité ou de taille de position — passer de 1 à 3 titres, d'euros à cents  |
| $x-\bar x\mathbf 1$  | retranche une constante à chaque terme : le **centrage**, omniprésent à partir du [module 8](08-degres-de-liberte-et-centrage.md) |

> ⚠️ **Il n'y a pas de multiplication de deux vecteurs ici.** La structure d'espace vectoriel n'en fournit pas, et le **produit scalaire** du [module 2](02-produit-scalaire-et-norme.md) n'en est pas une : il prend deux vecteurs et rend un **nombre**, pas un vecteur. C'est une structure supplémentaire, qu'on ajoute par choix — et c'est précisément ce choix qui fabrique la géométrie de tout le cours. Tout ce que le présent module établit vaut **avant** ce choix.

---

## 1.3 Les huit règles

Les deux opérations obéissent à huit règles, qu'on vérifie coordonnée par coordonnée depuis les propriétés des réels. Elles sont fastidieuses à lire une fois, et jamais rouvertes ensuite — mais ce sont elles, et rien d'autre, qui autorisent les manipulations de tout le cours.

| # | Règle                                     | Énoncé                                   |
| - | ----------------------------------------- | ---------------------------------------- |
| 1 | Associativité de $+$                      | $(u+v)+w=u+(v+w)$                        |
| 2 | Commutativité de $+$                      | $u+v=v+u$                                |
| 3 | Élément neutre                            | $u+\mathbf 0=u$                          |
| 4 | Opposé                                    | $u+(-u)=\mathbf 0$                       |
| 5 | Distributivité sur les vecteurs           | $\lambda(u+v)=\lambda u+\lambda v$       |
| 6 | Distributivité sur les scalaires          | $(\lambda+\mu)u=\lambda u+\mu u$         |
| 7 | Associativité mixte                       | $\lambda(\mu u)=(\lambda\mu)u$           |
| 8 | Neutre scalaire                           | $1\,u=u$                                 |

> **Définition.** Un ensemble muni de deux telles opérations vérifiant ces huit règles est un **espace vectoriel réel**. $\mathbb R^n$ en est un ; ce cours ne travaillera que dans celui-là.

**Ces règles servent, et voici comment.** Rien dans la liste ne dit que $0\,u=\mathbf 0$ — c'est une **conséquence**, pas une neuvième règle. Par la règle 6 appliquée à $\lambda=\mu=0$ :
$$0\,u=(0+0)\,u=0\,u+0\,u$$
En ajoutant $-(0\,u)$ aux deux membres (règles 1, 3 et 4), il reste $\mathbf 0=0\,u$. Le même schéma donne $(-1)u=-u$ et $\lambda\mathbf 0=\mathbf 0$ (exercices E1.2 et E1.3).

> 🔑 **Tout ce qui se démontre à partir de ces huit règles vaut dans n'importe quel espace vectoriel.** Les polynômes, les fonctions continues sur un intervalle, les matrices de taille fixée en sont aussi. Ce cours reste dans $\mathbb R^n$ parce que c'est là que vivent les données — mais **aucun résultat n'y est propre**, et c'est pourquoi les mêmes théorèmes se retrouveront, mot pour mot, en statistique et en finance.

---

## 1.4 La combinaison linéaire

C'est l'unique opération que le cours pratiquera, et toutes les autres n'en sont que des habillages.

> **Définition.** Une **combinaison linéaire** de $u_1,\dots,u_d$ est un vecteur de la forme
> $$\lambda_1u_1+\lambda_2u_2+\dots+\lambda_du_d,\qquad \lambda_1,\dots,\lambda_d\in\mathbb R$$

Deux vecteurs de $\mathbb R^n$ reviendront sans cesse, et ils suffisent à produire tout ce dont `import_societe.py` a besoin :
$$\mathbf 1=(1,1,\dots,1)\qquad\text{et}\qquad t=(1,2,\dots,n)$$

| Combinaison linéaire | La série qu'elle produit                                      |
| -------------------- | ------------------------------------------------------------- |
| $\lambda\mathbf 1$   | la série **constante** $(\lambda,\dots,\lambda)$              |
| $a\mathbf 1+b\,t$    | la série **affine** $(a+b\,i)_{i=1,\dots,n}$ — une **droite** |

> 🔑 **Une droite ajustée est une combinaison linéaire de deux vecteurs.** « Ajuster $\hat x_i=a+b\,i$ à une série » ne veut rien dire d'autre que : *choisir $a$ et $b$ de façon que $a\mathbf 1+b\,t$ soit le plus proche possible de $x$*. Ce qui manque encore est le sens de « le plus proche » — c'est le [module 2](02-produit-scalaire-et-norme.md) qui le donnera, et le [module 6](06-projection-orthogonale.md) qui le résoudra. L'ensemble de toutes ces combinaisons est l'objet du [module 4](04-sous-espaces-et-familles-generatrices.md).

---

## 1.5 Ce que cela devient sur des données

| Objet du dépôt                                   | Le vecteur                                                              |
| ------------------------------------------------ | ----------------------------------------------------------------------- |
| $n$ clôtures d'une fenêtre glissante             | $x\in\mathbb R^n$                                                       |
| les rendements correspondants                    | $r\in\mathbb R^{n-1}$ — **un espace différent**, une observation en moins |
| la moyenne `E_20`, répétée à chaque séance       | $\bar x\,\mathbf 1\in\mathbb R^n$                                       |
| les écarts à la moyenne                          | $x-\bar x\,\mathbf 1\in\mathbb R^n$                                     |
| la droite ajustée d'où sort `VAL_20`             | $a\mathbf 1+b\,t\in\mathbb R^n$                                         |
| les poids d'un portefeuille de $p$ titres        | $w\in\mathbb R^p$ — encore un autre espace                              |

> ⚠️ **Les rendements ne vivent pas dans l'espace des cours.** $n$ clôtures donnent $n-1$ rendements : $x$ et $r$ n'ont ni la même longueur ni la même unité, et les additionner n'a aucun sens. Cette trivialité est la source d'erreurs la plus banale du dépôt, et c'est aussi ce qui rend indispensable la déclaration explicite de la fenêtre (`--debut`, `--fin`) avant toute comparaison.

---

## 1.6 Simulation

### S1.1 — Les huit règles, et le piège des longueurs

```python
import numpy as np

# cinq clôtures : UN vecteur de R^5, pas cinq nombres
x = np.array([98.4, 99.1, 97.6, 100.2, 101.0])
y = np.array([12.0, 12.5, 11.8, 13.1, 13.0])

print("x + y :", x + y)      # coordonnée par coordonnée
print("3 * x :", 3 * x)      # chaque coordonnée est multipliée

rng = np.random.default_rng(1)
u, v, w = rng.normal(size=(3, 5))
a, b = 2.5, -1.3
zero = np.zeros(5)

regles = {
    "1  (u+v)+w = u+(v+w)": ((u + v) + w, u + (v + w)),
    "2  u+v = v+u":         (u + v, v + u),
    "3  u+0 = u":           (u + zero, u),
    "4  u+(-u) = 0":        (u + (-u), zero),
    "5  a(u+v) = au+av":    (a * (u + v), a * u + a * v),
    "6  (a+b)u = au+bu":    ((a + b) * u, a * u + b * u),
    "7  a(bu) = (ab)u":     (a * (b * u), (a * b) * u),
    "8  1u = u":            (1 * u, u),
}
for nom, (gauche, droite) in regles.items():
    print(f"{nom:22} {np.allclose(gauche, droite)}")

# conséquence, pas neuvième règle
print("0·u = 0 :", np.allclose(0 * u, zero), " (-1)u = -u :", np.allclose(-1 * u, -u))

# le piège : R^5 et R^3 ne communiquent pas
try:
    x + np.array([1.0, 2.0, 3.0])
except ValueError as e:
    print("R^5 + R^3 :", e)
```

La dernière ligne est la plus utile des huit : elle est le seul garde-fou automatique contre l'addition de deux séries dont les dates ne coïncident pas. Quand les longueurs coïncident **par accident**, plus rien n'avertit — d'où l'alignement explicite des fenêtres.

---

## 1.7 Exercices

**E1.1.** Montrer que le vecteur nul est **unique** : si $e$ vérifie $u+e=u$ pour tout $u$, alors $e=\mathbf 0$. *Puis montrer que chaque $u$ n'a qu'un seul opposé. (Piste : les règles 1 à 4 suffisent, aucune coordonnée n'intervient.)*

**E1.2.** Démontrer $0\,u=\mathbf 0$ et $\lambda\mathbf 0=\mathbf 0$ à partir des huit règles seulement. *Comparer avec la vérification coordonnée par coordonnée : laquelle des deux vaut encore pour un espace de fonctions ?*

**E1.3.** Démontrer $(-1)u=-u$. *(Piste : calculer $u+(-1)u$ avec la règle 6.)*

**E1.4.** L'ensemble des séries de $\mathbb R^n$ dont **toutes les coordonnées sont positives** est-il stable par les deux opérations ? *(Réponse : non.) Laquelle des deux met en défaut, et pourquoi cela disqualifie-t-il « les cours possibles » comme cadre de travail ? Le [module 4](04-sous-espaces-et-familles-generatrices.md) tirera les conséquences de cet exemple.*

**E1.5.** Écrire $(4,7,10,13)$ comme combinaison linéaire de $\mathbf 1$ et $t=(1,2,3,4)$. *Les coefficients sont-ils uniques ? Et si l'on ajoute $(2,4,6,8)$ à la liste des vecteurs disponibles ?*

**E1.6 — orientée finance.** À partir d'un CSV de `docs/raw/data/quotes/`, charger la colonne `Close` sur une fenêtre, puis la série des rendements $r_i=(x_{i+1}-x_i)/x_i$. *Vérifier que les deux tableaux n'ont pas la même longueur, et que leur somme échoue. Que faudrait-il déclarer pour comparer deux valeurs dont les calendriers de cotation diffèrent ?*

---

## 1.8 À retenir

- **Un vecteur de $\mathbb R^n$ est une série de $n$ nombres vue comme un seul objet** — l'ordre des coordonnées en fait partie, et $\mathbb R^n$ ne communique pas avec $\mathbb R^m$ pour $m\ne n$.
- **Deux opérations, coordonnée par coordonnée** : l'addition de deux vecteurs et la multiplication par un scalaire. **Pas de multiplication de deux vecteurs** ; le produit scalaire du module 2 rend un nombre et sera une structure ajoutée.
- **Huit règles**, jamais rouvertes après ce module, mais qui autorisent tout le reste — et dont on tire $0\,u=\mathbf 0$ et $(-1)u=-u$ plutôt que de les postuler.
- **La combinaison linéaire $\sum_j\lambda_ju_j$ est l'unique opération du cours.** $\lambda\mathbf 1$ est une série constante, $a\mathbf 1+b\,t$ une droite : ajuster une tendance, c'est choisir $a$ et $b$.
- **Rien de ce module n'est propre à $\mathbb R^n$** : les huit règles définissent un espace vectoriel quelconque, et tout ce qui s'en déduit vaut partout ailleurs.

---

➡️ [Module 2 — Produit scalaire, norme, distance](02-produit-scalaire-et-norme.md) ·
🏠 [Sommaire](README.md)
