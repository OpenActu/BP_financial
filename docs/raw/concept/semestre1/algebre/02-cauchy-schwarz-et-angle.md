# Module 2 — Cauchy–Schwarz et l'angle

**Durée : 45 min.** Prérequis : [module 1](01-produit-scalaire-et-norme.md).

> **La question traitée.** Le quotient $\dfrac{\langle u,v\rangle}{\|u\|\,\|v\|}$ a-t-il un sens géométrique ? Autrement dit : peut-on parler d'**angle** entre deux vecteurs de $\mathbb R^n$,  alors que rien dans la définition du § 1.1 ne mentionne d'angle ?

**Ce qui est en jeu.** La réponse est oui, et elle repose sur une unique inégalité. C'est elle
qui, transposée aux données, donne $|\rho|\le 1$ — et qui explique ce que signifie *exactement*
le cas d'égalité.

---

## 2.1 L'inégalité

> **Inégalité de Cauchy–Schwarz.**
> $$|\langle u,v\rangle|\;\le\;\|u\|\,\|v\|$$
> avec **égalité si et seulement si** $u$ et $v$ sont colinéaires.

**Démonstration (le trinôme).** Pour $v\ne 0$ et tout $t\in\mathbb R$, développons par
l'identité du § 1.2 :

$$P(t)=\|u+tv\|^2=\|v\|^2\,t^2+2\langle u,v\rangle\,t+\|u\|^2\;\ge\;0$$

$P$ est un trinôme du second degré (son coefficient dominant $\|v\|^2$ est non nul) de signe
constant : son discriminant est donc $\le 0$.

$$4\langle u,v\rangle^2-4\|u\|^2\|v\|^2\le 0
\quad\Longrightarrow\quad \langle u,v\rangle^2\le\|u\|^2\|v\|^2$$

L'égalité correspond à un discriminant nul, donc à une racine double $t_0$ telle que
$\|u+t_0v\|=0$, c'est-à-dire $u=-t_0v$ : colinéarité. $\blacksquare$

> 🔑 **La positivité du trinôme n'est rien d'autre que la propriété « définie positive » du
> § 1.1.** Toute l'inégalité tient dans le fait qu'un carré de norme ne peut pas être négatif.

---

## 2.2 L'angle est bien défini

Le quotient $\dfrac{\langle u,v\rangle}{\|u\|\|v\|}$ appartient à $[-1,1]$ pour $u,v$ non nuls :
il existe donc un **unique** $\theta\in[0,\pi]$ tel que

$$\langle u,v\rangle=\|u\|\,\|v\|\cos\theta$$

C'est la **définition** de l'angle entre deux vecteurs de $\mathbb R^n$ — et non un théorème
importé de la géométrie du plan. En dimension 2 elle redonne l'angle usuel ; en dimension $n$
elle l'étend sans rien changer aux formules.

| $\cos\theta$ | $\theta$ | Lecture                                                                |
| ------------ | -------- | ---------------------------------------------------------------------- |
| $1$          | $0°$     | même direction, même sens                                              |
| $0{,}71$     | $45°$    | —                                                                      |
| $0$          | $90°$    | **orthogonaux** — voir le [module 3](03-orthogonalite-et-pythagore.md) |
| $-1$         | $180°$   | même direction, sens opposé                                            |

---

## 2.3 Ce que l'inégalité devient sur des données

> 📐 **Préambule — ce qui autorise cette section.** Traduire une inégalité **vectorielle** en
> énoncé **statistique** n'est licite que si la covariance *est* un produit scalaire, au sens
> exact des trois propriétés du [§ 1.1](01-produit-scalaire-et-norme.md). Ce n'est ni une
> analogie ni une commodité de notation, et la vérification réserve une surprise : la covariance
> est bien symétrique et bilinéaire, mais seulement **positive** — pas *définie* positive, son
> noyau étant la droite des séries constantes. Le
> [**module 8**](08-covariance-et-produit-scalaire.md) lui est entièrement consacré ; la présente
> section en admet le résultat pour montrer tout de suite ce que Cauchy–Schwarz devient une fois
> traduit.

> ⚠️ **C'est exactement l'origine de $|\rho|\le 1$.** Appliquée aux vecteurs **centrés**
> $\tilde x=x-\bar x\mathbf 1$ et $\tilde y=y-\bar y\mathbf 1$, Cauchy–Schwarz donne
> $$\operatorname{Cov}(x,y)^2\le\operatorname{Var}(x)\operatorname{Var}(y)$$
> et le cas d'égalité — colinéarité de $\tilde x$ et $\tilde y$ — signifie que les points sont
> **exactement alignés**.

Le dictionnaire qui autorise cette traduction est dressé au
[module 7](07-dictionnaire-geometrique-des-statistiques.md) et démontré au
[module 8](08-covariance-et-produit-scalaire.md) ; le résultat est annoncé ici parce qu'il est la
seule raison d'être de ce module dans un cours orienté statistique.

> 🔑 Le document [`modele.md`](../../../modele.md) obtient $|\rho|\le 1$ à son étape 6 par un argument
> de variance positive. C'est la **même démonstration** que celle du § 2.1, écrite deux fois :
> « une variance est positive » et « un carré de norme est positif » sont le même énoncé.

---

## 2.4 Simulation

### S2.1 — L'inégalité, le cas d'égalité, et l'angle

```python
import numpy as np

rng = np.random.default_rng(2)
n = 50
u, v = rng.normal(size=n), rng.normal(size=n)

nu, nv = np.linalg.norm(u), np.linalg.norm(v)
print("Cauchy-Schwarz :", abs(u @ v) <= nu * nv)
print(f"   |<u,v>| = {abs(u @ v):.3f}   ‖u‖‖v‖ = {nu * nv:.3f}")

# cas d'égalité : v colinéaire à u
w = -3.7 * u
print("égalité si colinéaires :", np.isclose(abs(u @ w), nu * np.linalg.norm(w)))

# 10 000 tirages : à quel point l'inégalité est-elle "serrée" en dimension 50 ?
cos = np.array([(lambda a, b: a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))(
                 rng.normal(size=n), rng.normal(size=n)) for _ in range(10_000)])
print(f"|cos| max observé sur 10 000 tirages : {np.abs(cos).max():.3f}")
print(f"angle moyen à l'orthogonalité : {np.degrees(np.arccos(np.abs(cos))).mean():.1f}°")
```

**Le résultat est contre-intuitif et vaut le détour** : en dimension 50, deux vecteurs tirés au
hasard sont presque toujours **quasi orthogonaux**. Sur 10 000 tirages, $|\cos\theta|$ ne dépasse
pas $0{,}50$ et l'angle reste en moyenne à moins de $7°$ de la perpendiculaire. Relancez avec
`n = 2`, puis `n = 500` : plus la dimension monte, plus l'inégalité de Cauchy–Schwarz est loin
d'être atteinte.

> ⚠️ **Conséquence directe en finance.** Une corrélation de $0{,}30$ mesurée sur $n$ points est
> d'autant moins remarquable que $n$ est petit : c'est l'angle qu'on obtiendrait souvent par pur
> hasard. C'est le point de départ du module 8 du
> [cours sur la loi de Student](../../semestre3/statistique/loi-de-student/08-robustesse-et-limites.md).

---

## 2.5 Exercices

**E2.1.** Refaire la démonstration du § 2.1 en traitant explicitement le cas $v=0$. *Pourquoi
faut-il l'écarter, et pourquoi l'inégalité reste-t-elle vraie ?*

**E2.2.** Déduire de Cauchy–Schwarz l'**inégalité triangulaire** $\|u+v\|\le\|u\|+\|v\|$.
*(Piste : partir de l'identité de développement du § 1.2 et majorer le terme croisé.)*

**E2.3.** Deux séries de rendements ont une corrélation de $0{,}30$. Quel angle sépare leurs
vecteurs centrés ? Et pour $0{,}90$ ? *Commenter l'écart entre l'intuition « 0,9 c'est presque
1 » et la réalité géométrique.* **(Réponses : $72{,}5°$ et $25{,}8°$.)**

**E2.4.** Appliquer Cauchy–Schwarz à $u=x$ et $v=\mathbf 1$. Quelle inégalité classique entre
$\sum_i x_i$ et $\sum_i x_i^2$ obtient-on ? *Quand y a-t-il égalité, et que cela signifie-t-il
sur les données ?*

---

## 2.6 À retenir

- **$|\langle u,v\rangle|\le\|u\|\|v\|$**, démonstration par le discriminant d'un trinôme
  positif.
- **Égalité $\iff$ colinéarité** — c'est le cas d'égalité qui porte l'information, pas
  l'inégalité.
- **L'angle est défini par $\cos\theta=\frac{\langle u,v\rangle}{\|u\|\|v\|}$**, licite
  précisément parce que ce quotient est dans $[-1,1]$.
- Transposé aux vecteurs centrés : **$|\rho|\le1$**, avec égalité ⟺ alignement parfait.

---

⬅️ [Module 1 — Produit scalaire, norme, distance](01-produit-scalaire-et-norme.md) ·
➡️ [Module 3 — Orthogonalité et Pythagore](03-orthogonalite-et-pythagore.md) ·
🏠 [Sommaire](README.md)
