# Module 0 — Mise à niveau et auto-diagnostic

**Durée : 2 h.** Ce module ne s'apprend pas, il se **vérifie**. Son objet est de déterminer si
vous pouvez aborder le [théorème de Fisher–Cochran](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md) — le
cœur de l'édifice — sans être bloqué par un prérequis.

---

## 0.1 Les quatre acquis indispensables

Traitez les quatre questions suivantes **sans consulter de cours**. Les corrigés sont en fin de
module. Si l'une d'elles bloque, la section 0.3 indique quoi réviser.

### Q1 — Moments de la moyenne empirique

Soit $X_1,\dots,X_n$ i.i.d. d'espérance $\mu$ et de variance $\sigma^2$. Démontrer :
$$E(\bar X)=\mu \qquad\text{et}\qquad \operatorname{Var}(\bar X)=\frac{\sigma^2}{n}$$
Préciser **où exactement** l'hypothèse d'indépendance est utilisée.

### Q2 — Intervalle de confiance à $\sigma$ connu

Un échantillon gaussien de taille $n=25$ donne $\bar x = 103{,}2$ ; on sait que $\sigma = 8$.
Construire l'IC à 95 % de $\mu$ et **justifier le 1,96**.

Puis répondre : l'énoncé « il y a 95 % de chances que $\mu$ soit dans cet intervalle » est-il
correct ?

### Q3 — Théorème central limite

Énoncer le TCL précisément. Puis dire ce qu'il **ne dit pas** — en particulier :
- porte-t-il sur la loi des $X_i$ ou sur celle de $\bar X$ ?
- que devient l'approximation si les $X_i$ ne sont pas indépendants ?

### Q4 — Combinaison linéaire de gaussiennes

Soient $Z_1, Z_2$ i.i.d. $\mathcal N(0,1)$ et $a,b\in\mathbb R$. Donner la loi de $aZ_1+bZ_2$.
Puis : $Z_1+Z_2$ et $Z_1-Z_2$ sont-elles indépendantes ? Justifier.

---

## 0.2 Le prérequis d'algèbre linéaire

C'est le maillon faible le plus fréquent, et il est **rédhibitoire pour Fisher–Cochran**. Vous devez
être à l'aise avec :

> ➡️ **Si l'une de ces six lignes vous arrête, traitez le
> [cours d'algèbre linéaire euclidienne](../../../semestre1/algebre/README.md)** — cours séparé, 6 h 15 en sept
> modules. Il part du produit scalaire $\langle u,v\rangle=\sum_i u_iv_i$ et va jusqu'à la base
> orthonormée adaptée, en établissant au passage que **moyenne = projection**, **variance = carré
> de longueur** et **corrélation = cosinus d'angle**. ⚠️ Il est à traiter **avant les modules 5 à 7
> du [cours de statistique](../../../semestre2/statistique/mathematique/README.md)**,
> qui suppose tout cela acquis.
>
> Si une seule ligne vous arrête, le module correspondant suffit :

| Ligne du tableau ci-dessous | Module d'algèbre |
|---|---|
| Produit scalaire | [1 — Produit scalaire, norme, distance](../../../semestre1/algebre/01-produit-scalaire-et-norme.md) |
| Sous-espace vectoriel, dimension | [5 — Supplémentaire orthogonal, noyau, rang](../../../semestre1/algebre/05-supplementaire-orthogonal-et-dimension.md) |
| Projection orthogonale | [4 — La projection orthogonale](../../../semestre1/algebre/04-projection-orthogonale.md) |
| Supplémentaire orthogonal | [5 — Supplémentaire orthogonal, noyau, rang](../../../semestre1/algebre/05-supplementaire-orthogonal-et-dimension.md) |
| Degrés de liberté, le $n-1$ | [6 — Degrés de liberté : le cas Vect(1)](../../../semestre1/algebre/06-degres-de-liberte-et-centrage.md) |
| Théorème de Pythagore | [3 — Orthogonalité et Pythagore](../../../semestre1/algebre/03-orthogonalite-et-pythagore.md) |
| Base orthonormée, isométrie | [7 — Bases orthonormées et isométries](../../../semestre1/algebre/07-bases-orthonormees-et-isometries.md) |

| Notion                              | Ce qu'il faut savoir faire                                                                   |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| Produit scalaire dans $\mathbb R^n$ | Calculer $\langle u,v\rangle=\sum_i u_iv_i$, caractériser l'orthogonalité                    |
| Sous-espace vectoriel               | Reconnaître $\text{Vect}(\mathbf 1)$ où $\mathbf 1=(1,\dots,1)$, en donner la dimension      |
| Projection orthogonale              | Projeter $x$ sur $\text{Vect}(u)$ : $p(x)=\frac{\langle x,u\rangle}{\lVertu\rVert^2}u$               |
| Supplémentaire orthogonal           | $\mathbb R^n = F \oplus F^\perp$, avec $\dim F^\perp = n - \dim F$                           |
| Théorème de Pythagore               | $\lVertx\rVert^2=\lVertp(x)\rVert^2+\lVertx-p(x)\rVert^2$                                                            |
| Base orthonormée                    | Savoir qu'une isométrie transforme un vecteur gaussien standard en vecteur gaussien standard |

### Exercice de contrôle (à faire absolument)

Dans $\mathbb R^n$, soit $\mathbf 1=(1,\dots,1)$ et $x=(x_1,\dots,x_n)$.

1. Montrer que la projection orthogonale de $x$ sur $\text{Vect}(\mathbf 1)$ est
   $\bar x\,\mathbf 1$, où $\bar x = \frac1n\sum_i x_i$.
2. En déduire que le vecteur des écarts $(x_i - \bar x)_i$ appartient à
   $\text{Vect}(\mathbf 1)^\perp$.
3. Quelle est la dimension de ce sous-espace ?

> 🔑 **Ce troisième point est la réponse à la question « pourquoi $n-1$ ? »** que tout le cours
> va décliner. Si vous répondez « $n-1$ » et que vous voyez *pourquoi*, Fisher–Cochran se passera
> bien. Si le résultat vous paraît arbitraire, relisez cette section avant de continuer : c'est
> une **contrainte géométrique**, pas une convention de calcul.

> ➡️ Le corrigé complet de cet exercice — les trois points, la figure d'ensemble et la lecture de
> Pythagore qui en découle — est au § 6.1 du
> [module 6 du cours d'algèbre](../../../semestre1/algebre/06-degres-de-liberte-et-centrage.md).

---

## 0.3 Que réviser en cas de blocage

| Question ratée | À réviser | Où |
|---|---|---|
| Q1 | Linéarité de l'espérance, variance d'une somme de v.a. indépendantes | Saporta ch. 3 |
| **Q2** | Estimation, quantité pivotale, construction et **interprétation** d'un intervalle de confiance | ➡️ **[Cours de statistique, modules 17 à 19](../../../semestre2/statistique/mathematique/17-estimation-et-quantite-pivotale.md)** — 3 h 45 |
| **Q3** | Convergence en loi, TCL, ses hypothèses et ses limites | ➡️ **[Cours de statistique, modules 12 à 14](../../../semestre2/statistique/mathematique/12-theoreme-central-limite.md)** — 4 h 45 |
| **Q4** | Vecteur gaussien, stabilité par transformation linéaire, décorrélation vs indépendance | ➡️ **[Cours de statistique, modules 8 à 11](../../../semestre2/statistique/mathematique/08-addition-de-lois-et-stabilite-gaussienne.md)** — 4 h 15 |
| **Exercice 0.2** | Produit scalaire, orthogonalité, projection, degrés de liberté comme **dimension** | ➡️ **[Cours d'algèbre linéaire](../../../semestre1/algebre/README.md)** — cours séparé, 6 h 15, **à traiter avant les modules 5 à 7 du [cours de statistique](../../../semestre2/statistique/mathematique/README.md)** |

---

## 0.4 Corrigés

### Q1

$$E(\bar X)=E\!\left(\frac1n\sum_i X_i\right)=\frac1n\sum_i E(X_i)=\frac1n\cdot n\mu=\mu$$

Cette première égalité n'utilise **que la linéarité de l'espérance** — elle reste vraie même si
les $X_i$ sont dépendants.

$$\operatorname{Var}(\bar X)=\frac{1}{n^2}\operatorname{Var}\!\left(\sum_i X_i\right)
=\frac{1}{n^2}\sum_i \operatorname{Var}(X_i)=\frac{n\sigma^2}{n^2}=\frac{\sigma^2}{n}$$

⚠️ **C'est ici, et seulement ici, qu'intervient l'indépendance** : la variance d'une somme n'est
la somme des variances que si les covariances croisées sont nulles. En toute généralité,
$$\operatorname{Var}\!\left(\sum_i X_i\right)=\sum_i\operatorname{Var}(X_i)+2\sum_{i<j}\operatorname{Cov}(X_i,X_j).$$

**Retenir ceci** : sur des données corrélées positivement — le cas de toute série chronologique —
les covariances sont positives, donc $\operatorname{Var}(\bar X) > \sigma^2/n$. La moyenne est
**moins précise** que la formule usuelle ne le laisse croire. Le module 8 montrera que c'est la
cause n° 1 des tests faussement significatifs.

### Q2

$$\text{IC}_{95\%}(\mu)=\left[\bar x - 1{,}96\frac{\sigma}{\sqrt n}\;;\;
\bar x + 1{,}96\frac{\sigma}{\sqrt n}\right]
= \left[103{,}2 - 1{,}96\cdot\frac{8}{5}\;;\; 103{,}2+1{,}96\cdot\frac{8}{5}\right]
= [\,100{,}06\;;\;106{,}34\,]$$

Le $1{,}96$ est le quantile d'ordre $0{,}975$ de $\mathcal N(0,1)$ : il vérifie
$P(-1{,}96 \le Z \le 1{,}96)=0{,}95$.

**Non, l'énoncé est incorrect.** Dans le cadre fréquentiste, $\mu$ est une constante inconnue,
pas une variable aléatoire : elle est dans l'intervalle ou elle n'y est pas, sans probabilité
intermédiaire. C'est l'**intervalle** qui est aléatoire, car il dépend de $\bar X$. La
formulation correcte est : *si l'on répétait l'expérience un grand nombre de fois, 95 % des
intervalles ainsi construits contiendraient $\mu$.*

> ➡️ **Ce point mérite mieux qu'un corrigé de trois lignes** — c'est l'erreur d'interprétation la
> plus répandue en statistique, et la construction elle-même est la **maquette de tout le cours**.
> Les [modules 17 à 19 du cours de statistique](../../../semestre2/statistique/mathematique/17-estimation-et-quantite-pivotale.md) lui sont entièrement consacrés :
> quantité pivotale, retournement algébrique, origine du 1,96, et trois simulations dont une qui
> exhibe un intervalle « à 50 % de confiance » dont on sait avec **certitude** qu'il contient le
> paramètre.

### Q3

**TCL.** Si $X_1,\dots,X_n$ sont i.i.d. d'espérance $\mu$ et de variance $\sigma^2$ finie, alors
$$\frac{\bar X_n - \mu}{\sigma/\sqrt n}\;\xrightarrow[n\to\infty]{\mathcal L}\;\mathcal N(0,1).$$

Ce qu'il **ne dit pas** :
- Il ne dit **rien sur la loi des $X_i$**, qui reste ce qu'elle est. Il porte exclusivement sur
  la loi de la **moyenne standardisée**.
- Il ne vaut **pas sans indépendance**. Il existe des TCL pour données dépendantes, mais sous des
  conditions de mélange, et avec une variance asymptotique différente (celle de Q1).
- Il ne donne **aucune vitesse** de convergence : « $n\ge 30$ » est une règle empirique, pas un
  résultat. Sur une loi très asymétrique, $n=30$ est nettement insuffisant.
- Il suppose $\sigma^2$ **finie**. Sur une loi à queue lourde (Cauchy, certains rendements
  financiers), il ne s'applique pas.

> ➡️ Les [modules 12 à 14 du cours de statistique](../../../semestre2/statistique/mathematique/12-theoreme-central-limite.md) développent chacun de ces points, et répondent en
> détail aux deux sous-questions. Il montre notamment, chiffres à l'appui, **les deux régimes de
> dépendance** : dépendance faible → le TCL survit avec une autre variance (corrigible) ;
> dépendance forte → il n'y a **plus de TCL du tout** et la couverture d'un intervalle tend
> vers 0. C'est ce contraste qui fonde tout le module 8.

### Q4

$aZ_1+bZ_2 \sim \mathcal N(0,\,a^2+b^2)$ : une combinaison linéaire de gaussiennes indépendantes
est gaussienne, de variance $a^2\cdot 1 + b^2\cdot 1$.

$Z_1+Z_2$ et $Z_1-Z_2$ : leur covariance vaut
$$\operatorname{Cov}(Z_1+Z_2,\,Z_1-Z_2)=\operatorname{Var}(Z_1)-\operatorname{Var}(Z_2)=1-1=0.$$

Comme $(Z_1+Z_2,\,Z_1-Z_2)$ est un **vecteur gaussien** (image de $(Z_1,Z_2)$ par une application
linéaire), la nullité de la covariance **entraîne ici l'indépendance**.

> 🔑 **Ce résultat est la maquette exacte du théorème de Fisher–Cochran.** Deux fonctions des
> mêmes données, décorrélées parce que construites sur des directions orthogonales
> ($(1,1)$ et $(1,-1)$), et donc indépendantes **parce que le vecteur de départ est gaussien**.
> Retenez cette structure : [Fisher–Cochran](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md) la reproduit
> en dimension $n$, avec $\bar X$ à la place
> de $Z_1+Z_2$ et $S^2$ à la place de $(Z_1-Z_2)^2$.

⚠️ Sans normalité, covariance nulle **n'implique pas** l'indépendance. C'est précisément pour
cette raison que l'hypothèse gaussienne est indispensable à Fisher–Cochran — et pour cette raison
seulement.

> ➡️ Les [modules 8 à 11 du cours de statistique](../../../semestre2/statistique/mathematique/08-addition-de-lois-et-stabilite-gaussienne.md) développent entièrement cette question. Ils donnent le
> contre-exemple à connaître — deux variables **parfaitement gaussiennes**, **décorrélées** et
> pourtant **dépendantes** — et établissent le **lemme de projection** que Fisher–Cochran se
> contente d'appliquer en dimension $n$. ⚠️ **Le [module 11](../../../semestre2/statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md)
> est le plus important des quatre** : il fournit l'outil, là où les autres posent le décor.

---

## 0.5 Vérification par simulation

Pour finir le module, vérifiez numériquement Q4. Le code doit produire une corrélation
quasi nulle **et** deux histogrammes conditionnels superposables.

```python
import numpy as np

rng = np.random.default_rng(0)
Z = rng.standard_normal((200_000, 2))
S, D = Z[:, 0] + Z[:, 1], Z[:, 0] - Z[:, 1]

print("corrélation :", np.corrcoef(S, D)[0, 1])          # ≈ 0

# L'indépendance est plus forte que la décorrélation : la loi de D
# doit être la même quelle que soit la valeur de S.
for lo, hi in [(-0.5, 0.5), (1.5, 2.5), (-2.5, -1.5)]:
    m = (S > lo) & (S < hi)
    print(f"S∈[{lo:+.1f},{hi:+.1f}] → écart-type de D = {D[m].std():.3f}")  # tous ≈ √2
```

**Puis refaites la même chose avec une loi exponentielle** au lieu de la gaussienne :

```python
X = rng.exponential(size=(200_000, 2))
S, D = X[:, 0] + X[:, 1], X[:, 0] - X[:, 1]
print("corrélation :", np.corrcoef(S, D)[0, 1])          # ≈ 0 également !
for lo, hi in [(0.5, 1.0), (2.0, 2.5), (4.0, 4.5)]:
    m = (S > lo) & (S < hi)
    print(f"S∈[{lo:.1f},{hi:.1f}] → écart-type de D = {D[m].std():.3f}")  # ils DIFFÈRENT
```

La corrélation est nulle dans les deux cas, mais l'indépendance **ne tient que pour la
gaussienne**. C'est l'expérience la plus utile de ce module 0 : elle fixe pour de bon la
différence entre décorrélation et indépendance.

---

⬅️ [🏠 Sommaire](README.md) ·
➡️ [Module 1 — Le problème que Student résout](01-le-probleme.md)
