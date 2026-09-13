# Module 1 — Le risque n'est pas où l'on croit

**Durée : 1 h 30.** Ce module ne contient aucune procédure. Il pose la seule chose
qui compte : **de quel risque parle-t-on ?** Tant que cette question n'est pas
tranchée, corriger ou ne pas corriger sont deux gestes également arbitraires.

---

## 1.1 Deux risques qu'on confond

Un test au niveau $\alpha = 5\,\%$ garantit ceci, et rien d'autre :

$$P(\text{rejeter } H_0 \mid H_0 \text{ vraie}) \le 0{,}05$$

**C'est une garantie par test.** Elle ne dit rien de ce qui arrive quand on en
mène plusieurs. Deux grandeurs distinctes apparaissent alors :

| Grandeur | Définition | Ce qu'elle vaut si l'on ne fait rien |
|---|---|---|
| Risque **par test** | $P(\text{faux positif sur le test } i)$ | $\alpha$ — inchangé, toujours |
| **FWER** *(family-wise error rate)* | $P(\text{au moins un faux positif dans la famille})$ | croît avec $m$ |

> 🔑 **Rien ne se dégrade au niveau d'un test.** Chaque test reste exactement aussi
> fiable qu'avant. Ce qui change, c'est la question qu'on lui pose : on ne demande
> plus « ce test-ci s'est-il trompé ? » mais « **l'un quelconque** de mes tests
> s'est-il trompé ? ». La seconde question est plus exigeante, et c'est la seule
> qui vaille dès qu'on publie le meilleur résultat d'un lot.

## 1.2 La table — et l'hypothèse qu'elle cache

Si les $m$ tests sont **indépendants** et que toutes les nulles sont vraies, la
probabilité qu'aucun ne rejette vaut $(1-\alpha)^m$, donc

$$\mathrm{FWER} = 1-(1-\alpha)^m$$

| $m$ | 1 | 5 | 10 | 18 | 20 | 100 |
|---|---|---|---|---|---|---|
| FWER à $\alpha=5\,\%$ | 5 % | 23 % | 40 % | **60 %** | **64 %** | **99,4 %** |

Vingt tests sur du bruit pur produisent presque à coup sûr un « résultat
significatif ».

> ⚠️ **Cette formule suppose l'indépendance, et on l'oublie presque toujours.**
> Sous dépendance **arbitraire**, on ne sait encadrer le FWER que par
> $$\alpha \;\le\; \mathrm{FWER} \;\le\; \min(m\alpha,\ 1)$$
> Les deux bornes sont atteintes : $m$ tests **identiques** (dépendance parfaite)
> donnent $\mathrm{FWER}=\alpha$ — les corriger serait une perte sèche ; $m$ tests
> disjoints donnent la borne haute. La table ci-dessus est donc un **cas
> particulier**, pas une loi générale.
>
> C'est précisément pourquoi les procédures des modules 2 et 3 sont construites
> sur la **borne supérieure** $m\alpha$ : elle, au moins, ne suppose rien.

## 1.3 Qu'est-ce qu'une famille ?

La correction dépend de $m$. Donc tout dépend de ce qu'on met dans la famille — et
**ce choix n'est pas donné par les mathématiques.**

Trois découpages du même jeu de 24 tests :

| Découpage | $m$ retenu | Effet |
|---|---|---|
| Une seule famille de 24 | 24 | le plus sévère |
| Deux familles (18 + 6) | 18 et 6 | intermédiaire |
| 24 familles d'un test | 1 | aucune correction |

Le troisième découpage est toujours disponible, et il annule la correction. C'est
ce qui rend le choix de la famille **le point faible de tout l'édifice** : il se
déclare, il se justifie, et il se fixe **avant** de voir les résultats.

**Le critère usuel** : appartiennent à la même famille les tests qui répondent à
**une même question**, et parmi lesquels on serait prêt à retenir « le meilleur ».
Si vous n'auriez publié qu'un seul des $m$ résultats — celui qui sort —, alors les
$m$ sont une famille.

> ℹ️ **Un exemple réel, dans ce dépôt.** L'[expérience 13](../../../../../done/experimentation/experience_13/README.md)
> déclare **deux** familles : 18 cellules de mesure (3 bras × 2 sens × 3 seuils) et
> 6 cellules de **contrôle de validité**. Deux familles parce que deux questions :
> l'une demande « l'effet existe-t-il ? », l'autre « l'instrument est-il
> faussé ? ». Les fondre en une seule aurait dilué la correction de la première
> avec des tests qui n'y répondent pas.

## 1.4 Le test multiple implicite — le cas le plus fréquent

Le problème ne se pose pas seulement quand on annonce $m$ tests. Il se pose,
identique, quand on en fait $m$ et qu'on n'en rapporte **qu'un** :

- essayer plusieurs fenêtres (20, 60, 120, 250 séances) et publier la meilleure ;
- essayer plusieurs seuils, plusieurs sous-périodes, plusieurs transformations ;
- retirer « le point aberrant » et refaire le test ;
- s'arrêter de collecter dès que $p$ passe sous 0,05.

C'est le ***p-hacking***, et sa forme la plus insidieuse est le **jardin aux
sentiers qui bifurquent** (Gelman & Loken, 2013) : l'analyste n'essaie **qu'une**
analyse, mais il l'aurait choisie différemment si les données avaient été autres.
Le $m$ effectif est alors invisible, y compris à celui qui analyse.

> 🔑 **Le seul remède est procédural, pas statistique.** Aucune correction ne
> rattrape un $m$ qu'on ignore. Il faut **fixer le protocole avant de voir les
> données** — ce que les expériences de ce dépôt appellent une piste de
> [catégorie A](../../../../../done/experimentation/experience_13/README.md), par
> opposition à une piste B, suggérée par le résultat.

## 1.5 Simulations

### S1.1 — Voir le FWER gonfler

```python
import numpy as np
rng = np.random.default_rng(1)
Z95 = 1.959964          # quantile a 97,5 % : rejeter si |z| le depasse

def fwer(m, rho=0.0, N=200_000):
    """Proportion de familles contenant au moins un faux positif, sous H0 vraie.

    rho = 0 : tests independants. rho -> 1 : tests de plus en plus semblables.
    On teste |z| > Z95 plutot que p < alpha : c'est la meme chose, sans scipy.
    """
    commun = rng.standard_normal((N, 1))
    propre = rng.standard_normal((N, m))
    z = np.sqrt(rho) * commun + np.sqrt(1 - rho) * propre
    return np.mean((np.abs(z) > Z95).any(axis=1))

for m in (1, 5, 10, 18, 20, 100):
    print(f"m={m:>3}  independants {fwer(m):.3f}   attendu {1-0.95**m:.3f}")
```

### S1.2 — L'effet de la dépendance

```python
for rho in (0.0, 0.5, 0.9, 0.99):
    print(f"m=20  rho={rho:.2f}  FWER={fwer(20, rho):.3f}")
```

**Ce que vous devez constater**, à $m = 20$ :

| $\rho$ | 0 | 0,50 | 0,90 | 0,99 |
|---|---|---|---|---|
| FWER mesuré | **64,2 %** | 41,8 % | 15,5 % | **7,5 %** |

**La dépendance protège**, et massivement — mais on ne la connaît jamais, et c'est
pourquoi on corrige comme si elle était nulle. Notez qu'elle ne ramène pas le FWER
à 5 % : il y faudrait $\rho = 1$, c'est-à-dire $m$ fois le même test.

## 1.6 Exercices

**E1.1.** Démontrer $\mathrm{FWER}=1-(1-\alpha)^m$ sous indépendance, et vérifier
que $1-(1-\alpha)^m \le m\alpha$ pour tout $m\ge 1$. *(Indication : convexité, ou
inégalité de Bernoulli.)*

**E1.2.** Construire deux tests **parfaitement dépendants** (le même test écrit
deux fois). Que vaut le FWER ? Que vaudrait la correction de Bonferroni ? Conclure
sur ce qu'on perd à corriger une famille redondante.

**E1.3.** Un analyste teste 40 valeurs d'un indice et publie les 2 dont
$p < 0{,}05$. Combien en attendait-on **sous $H_0$ vraie partout** ? Sa
publication est-elle une découverte ?

**E1.4 — orientée dépôt.** L'[expérience 13](../../../../../done/experimentation/experience_13/bilan.md)
mesure 18 cellules et en trouve **exactement une** sous 0,05 ($p = 0{,}0253$).
Était-ce surprenant ? Calculer le nombre attendu de cellules sous 0,05 si aucune
n'avait d'effet.

## 1.7 À retenir

- Le niveau $\alpha$ est une garantie **par test** ; le FWER est une garantie **par
  famille**. Corriger, c'est passer de l'une à l'autre.
- $1-(1-\alpha)^m$ **suppose l'indépendance**. Sous dépendance quelconque, le FWER
  est seulement encadré par $[\alpha,\ \min(m\alpha, 1)]$.
- **18 tests à 5 % : 60 % de chances d'au moins un faux positif**, et environ
  **0,9 faux positif attendu** — soit à peu près un.
- La **famille** n'est pas donnée par les mathématiques. Elle se déclare avant,
  sous peine de pouvoir toujours la réduire à un test.
- Le test multiple **implicite** — plusieurs fenêtres essayées, une seule publiée —
  est le cas le plus fréquent et le seul qu'aucune correction ne rattrape.

---

➡️ [Module 2 — Bonferroni](02-bonferroni.md) ·
🏠 [Sommaire](README.md)
