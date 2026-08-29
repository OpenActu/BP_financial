# Module 7 — Le dictionnaire géométrique des statistiques ⭐

**Durée : 1 h.** Prérequis : modules [1](01-produit-scalaire-et-norme.md) à
[6](06-bases-orthonormees-et-isometries.md). C'est ici que l'algèbre linéaire devient de la
statistique ; le [module 8](08-covariance-et-produit-scalaire.md) démontre ensuite que la
traduction est légitime.

> **La question traitée.** Moyenne, variance, covariance, corrélation : ces quatre formules
> sont-elles quatre recettes distinctes, ou une seule et même géométrie écrite quatre fois ?

**Ce qui est en jeu.** C'est **la section à lire deux fois** de tout le cours. Tant que ce
dictionnaire n'est pas automatique, les démonstrations du
[cours sur la loi de Student](../statistique/loi-de-student/README.md) paraissent magiques ; une fois acquis,
Fisher–Cochran se lit comme un théorème de Pythagore.

---

## 7.1 Le renversement de perspective

Prenons $n$ observations $x=(x_1,\dots,x_n)$, vues comme **un seul point de $\mathbb R^n$** — et
non comme $n$ points de $\mathbb R$.

C'est tout le renversement : l'objet d'étude n'est plus un nuage de $n$ nombres, mais **un
vecteur unique** dans un espace de grande dimension. Les statistiques usuelles deviennent alors
des mesures géométriques sur ce vecteur.

Posons $\mathbf 1=(1,\dots,1)$, dont la norme vaut $\|\mathbf 1\|^2=n$, et notons
$\tilde x = x-\bar x\,\mathbf 1$ le **vecteur centré** — le résidu de la projection du
[module 5](05-supplementaire-orthogonal-et-dimension.md).

---

## 7.2 Le dictionnaire ⭐

| Statistique             | Écriture géométrique                                                                         |
| ----------------------- | -------------------------------------------------------------------------------------------- |
| Somme                   | $\sum_i x_i=\langle x,\mathbf 1\rangle$                                                      |
| Moyenne                 | $\bar x=\dfrac{\langle x,\mathbf 1\rangle}{\lVert\mathbf 1\rVert^2}$                                 |
| Variance (diviseur $n$) | $\operatorname{Var}(x)=\dfrac{\lVert\tilde x\rVert^2}{n}$                                            |
| Variance d'échantillon  | $s^2=\dfrac{\lVert\tilde x\rVert^2}{n-1}$                                                            |
| Covariance              | $\operatorname{Cov}(x,y)=\dfrac{\langle \tilde x,\tilde y\rangle}{n}$                        |
| Corrélation             | $\rho_{x,y}=\dfrac{\langle \tilde x,\tilde y\rangle}{\lVert\tilde x\rVert\,\lVert\tilde y\rVert}=\cos\theta$ |

Trois lectures s'imposent immédiatement :

1. **La moyenne est un produit scalaire** — plus précisément, à un facteur près, la coordonnée de
   $x$ sur la direction $\mathbf 1$ ([module 5](05-supplementaire-orthogonal-et-dimension.md)).
2. **La variance est un carré de longueur** — celle du vecteur centré. « Dispersion » et
   « distance à la moyenne » sont littéralement le même mot.
3. **La corrélation est un cosinus d'angle** ([module 2](02-cauchy-schwarz-et-angle.md)). Deux
   séries décorrélées sont deux vecteurs centrés **perpendiculaires**. $\rho=\pm1$ signifie
   **colinéaires**.

> 📐 **Ce tableau est une liste d'égalités, pas de définitions.** Que la ligne « Covariance » ait
> le droit d'être lue comme un **produit scalaire** — bilinéarité comprise — se *démontre*, et
> c'est l'objet du [module 8](08-covariance-et-produit-scalaire.md), qui prolonge directement
> cette section.

> ⚠️ **Les deux variances diffèrent par le seul diviseur.** $\|\tilde x\|^2$ est la même quantité
> géométrique dans les deux lignes ; $n$ ou $n-1$ relève d'une finalité — décrire ou estimer — et
> non de la géométrie. Le [module 5](05-supplementaire-orthogonal-et-dimension.md) explique
> pourquoi $n-1$ est la dimension effective ; le document [`modele.md`](../modele/modele.md), purement
> descriptif, normalise par $n$.

---

## 7.3 Ce que chaque théorème du cours devient

| Résultat d'algèbre | Traduction statistique |
|---|---|
| Cauchy–Schwarz ([m. 2](02-cauchy-schwarz-et-angle.md)) | $\lvert\rho\rvert\le 1$, égalité ⟺ points alignés |
| Pythagore ([m. 3](03-orthogonalite-et-pythagore.md)) | Décomposition de la variance, table d'ANOVA |
| Projection = point le plus proche ([m. 4](04-projection-orthogonale.md)) | Moindres carrés |
| $p(x)=\bar x\mathbf 1$ ([m. 5](05-supplementaire-orthogonal-et-dimension.md)) | $\bar x=\arg\min_c\sum_i(x_i-c)^2$ |
| $\dim\text{Vect}(\mathbf 1)^\perp=n-1$ ([m. 5](05-supplementaire-orthogonal-et-dimension.md)) | Degrés de liberté |
| $\operatorname{tr}(P)=\dim F$ ([m. 4](04-projection-orthogonale.md)) | Degrés de liberté lus sur une matrice |
| BON adaptée, isométrie ([m. 6](06-bases-orthonormees-et-isometries.md)) | Transformation de Helmert, invariance gaussienne |

> 🔑 **Aucune de ces traductions n'est une analogie.** Ce sont des égalités : le membre de gauche
> et le membre de droite désignent le même nombre.

---

## 7.4 Où cela resurgit

| Objet géométrique | Objet statistique | Où |
|---|---|---|
| $\langle x,\mathbf 1\rangle/n$ | Moyenne $\bar x$ | Partout |
| $\lVert\tilde x\rVert^2$ | Somme des carrés des écarts | [Loi du $\chi^2$](../statistique/mathematique/15-loi-du-chi2.md) |
| $\mathbb R^n=\text{Vect}(\mathbf 1)\oplus\text{Vect}(\mathbf 1)^\perp$ | Séparation moyenne / dispersion | [Fisher–Cochran](../statistique/mathematique/16-theoreme-de-fisher-cochran.md) |
| $\dim\text{Vect}(\mathbf 1)^\perp=n-1$ | Degrés de liberté | Tout le cours sur Student |
| Pythagore | Décomposition de la variance | [Student en régression](../statistique/loi-de-student/07-student-en-regression.md) |
| Projection = point le plus proche | Moindres carrés | [`modele.md`](../modele/modele.md) |
| $\cos\theta$ | Corrélation $\rho$ | [`modele.md`](../modele/modele.md) étape 6 |
| Base orthonormée adaptée | Transformation de Helmert | [Vecteurs gaussiens](../statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md) |
| Isométrie $O$ | Invariance par rotation de la gaussienne | [Vecteurs gaussiens](../statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md) |

**Ce cours est purement déterministe.** Aucune probabilité n'y intervient : tout ce qui précède
vaut sur $n$ nombres quelconques, sans le moindre modèle. C'est précisément ce qui rend la suite
possible — le cours sur Student ajoute **un seul ingrédient**, l'hypothèse gaussienne, à une
figure déjà entièrement construite.

---

## 7.5 Simulation

### S7.1 — Le dictionnaire du § 7.2, vérifié terme à terme

```python
import numpy as np

rng = np.random.default_rng(7)
n = 12
x, y = rng.normal(100, 15, n), rng.normal(50, 4, n)
un = np.ones(n)

xb = x @ un / (un @ un)                      # moyenne = produit scalaire
xt, yt = x - x.mean(), y - y.mean()          # vecteurs centrés

print("moyenne    :", np.allclose(xb, x.mean()))
print("variance   :", np.allclose(xt @ xt / n, x.var()))
print("covariance :", np.allclose(xt @ yt / n, np.cov(x, y, bias=True)[0, 1]))

cos = (xt @ yt) / (np.linalg.norm(xt) * np.linalg.norm(yt))
print("corrélation = cosinus :", np.allclose(cos, np.corrcoef(x, y)[0, 1]))
print(f"angle entre les séries : {np.degrees(np.arccos(cos)):.1f}°")
```

Les quatre tests affichent `True`. La dernière ligne est la plus instructive : **une corrélation
est un angle**. Ici l'angle vaut $108{,}1°$ — obtus, donc corrélation négative. Repères à
mémoriser : $\rho=1\to 0°$, $\rho=0\to 90°$, $\rho=-1\to 180°$, et $\rho=0{,}71\to 45°$.

---

## 7.6 Exercices

**E7.1.** Démontrer chaque ligne du dictionnaire du § 7.2 à partir des définitions statistiques
usuelles. *Aucune ne demande plus de deux lignes.*

**E7.2 — orientée finance.** Le script `historique_sbf250.py` calcule `CORR_20`, corrélation
glissante entre la colonne `Close` et le compteur `INDICE` sur 20 séances.
1. Montrer que `CORR_20` est le **cosinus de l'angle** entre le vecteur des 20 cours **centrés**
   et le vecteur $(1,\dots,20)$ **centré**.
2. Le recalculer à la main par produits scalaires sur un fichier produit par le script, et
   vérifier l'accord avec la colonne.
3. Le vecteur temps centré étant **fixe**, quelle est la conséquence pour l'interprétation ? *(La
   corrélation ne mesure ici que l'alignement des cours sur une direction déterminée d'avance :
   c'est une mesure d'alignement, non un estimateur — voir l'étape 7 de
   [`modele.md`](../modele/modele.md).)*

**E7.3.** Le script calcule aussi `VAL_20 = E_20 + sqrt(3·VAR_20)·CORR_20`. Réécrire cette formule
entièrement en langage géométrique (produits scalaires, normes, cosinus). *Que mesure-t-elle,
lue ainsi ?*

**E7.4.** Deux séries ont même moyenne et même variance mais une corrélation de $0$. Que peut-on
dire de leurs vecteurs dans $\mathbb R^n$ ? *Faire un dessin en dimension 3 avec
$\text{Vect}(\mathbf 1)$ comme axe vertical.*

**E7.5.** Montrer que $\rho$ est invariante par transformation affine croissante
$x\mapsto ax+b$ ($a>0$). *(Piste : que deviennent $\tilde x$ et son angle ?) Quelle propriété
géométrique du § 6.2 est en jeu ?*

---

## 7.7 À retenir

- **Une série de $n$ observations est UN vecteur de $\mathbb R^n$**, pas $n$ nombres.
- **Le dictionnaire** : moyenne = produit scalaire avec $\mathbf 1$ ; variance = carré de longueur
  du vecteur centré ; covariance = produit scalaire des centrés ; corrélation = **cosinus
  d'angle**. Décorrélé = **perpendiculaire**.
- Chaque théorème d'algèbre du cours a une **traduction exacte** — non une analogie — en
  statistique.
- Tout ce cours est **déterministe** : il vaut sur des nombres quelconques. La probabilité
  n'intervient qu'ensuite, et n'ajoute qu'un ingrédient.

---

⬅️ [Module 6 — Bases orthonormées et isométries](06-bases-orthonormees-et-isometries.md) ·
➡️ [Module 8 — La covariance comme produit scalaire](08-covariance-et-produit-scalaire.md) ·
🏠 [Sommaire](README.md)
