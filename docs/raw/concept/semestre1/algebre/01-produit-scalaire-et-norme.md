# Module 1 — Produit scalaire, norme, distance

**Durée : 45 min.** Point d'entrée du cours. Aucun prérequis au-delà des sommes indicées.

> **La question traitée.** Comment munir $\mathbb R^n$ — l'espace où vit une série de $n$ observations — d'une notion de **longueur** et d'**angle** ?

**Ce qui est en jeu.** Une seule opération, $\langle u,v\rangle=\sum_i u_iv_i$, suffit à produire tout le reste : norme, distance, orthogonalité, projection, degrés de liberté. Les six modules suivants ne font que la développer.

---

## 1.1 Définition

> **Définition.** Pour $u=(u_1,\dots,u_n)$ et $v=(v_1,\dots,v_n)$ dans $\mathbb R^n$ :
> $$\langle u,v\rangle=\sum_{i=1}^n u_iv_i \;=\; u^{\top}v$$

Trois propriétés, et tout le reste en découle :

| Propriété            | Énoncé                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Symétrie**         | $\langle u,v\rangle=\langle v,u\rangle$                                                                       |
| **Bilinéarité**      | $\langle \alpha u+\beta u',\,v\rangle=\alpha\langle u,v\rangle+\beta\langle u',v\rangle$, et de même à droite |
| **Définie positive** | $\langle u,u\rangle\ge 0$, avec égalité **si et seulement si** $u=0$                                          |

Aucune des trois n'est une hypothèse : elles se **démontrent**, et chacune se ramène à une
propriété de l'addition ou de la multiplication dans $\mathbb R$, transportée par la somme
indicée.

> **Symétrie.** Pour tout $i$, $u_iv_i=v_iu_i$ — la multiplication des réels est commutative. En sommant sur $i$ :
> $$\langle u,v\rangle=\sum_{i=1}^n u_iv_i=\sum_{i=1}^n v_iu_i=\langle v,u\rangle\qquad\blacksquare$$

> **Bilinéarité.** Soient $\alpha,\beta\in\mathbb R$ et $u,u',v\in\mathbb R^n$. La $i$-ème composante de $\alpha u+\beta u'$ vaut $\alpha u_i+\beta u'_i$ ; en développant par distributivité, puis en scindant la somme :
> $$\langle \alpha u+\beta u',\,v\rangle
> =\sum_{i=1}^n(\alpha u_i+\beta u'_i)v_i
> =\alpha\sum_{i=1}^n u_iv_i+\beta\sum_{i=1}^n u'_iv_i
> =\alpha\langle u,v\rangle+\beta\langle u',v\rangle$$
> La linéarité **à droite** ne se redémontre pas : elle se déduit de la précédente en passant deux fois par la symétrie, $\langle u,\alpha v+\beta v'\rangle=\langle \alpha v+\beta v',u\rangle=\alpha\langle v,u\rangle+\beta\langle v',u\rangle=\alpha\langle u,v\rangle+\beta\langle u,v'\rangle$. Symétrique **plus** linéaire à gauche suffit donc : la moitié droite est offerte. $\blacksquare$

> **Définie positive.** $\langle u,u\rangle=\sum_i u_i^2$ est une somme de carrés de réels, donc de
> termes tous $\ge 0$ : la somme est $\ge 0$. Restent les deux sens du cas d'égalité. **Sens direct** :
> si $u=0$, chaque $u_i$ est nul, donc chaque $u_i^2$ aussi, et la somme vaut $0$. **Réciproque** :
> supposons $\sum_i u_i^2=0$ et qu'un indice $j$ vérifie $u_j\ne 0$ ; tous les termes étant $\ge 0$, on
> peut minorer la somme par n'importe lequel d'entre eux, $\sum_i u_i^2\ge u_j^2>0$, ce qui contredit
> l'hypothèse. Donc $u_i=0$ pour tout $i$, soit $u=0$. $\blacksquare$

> ⚠️ **C'est la réciproque du dernier point qui fait tout le travail dans la suite.** « Somme de carrés nulle $\Rightarrow$ vecteur nul » est ce qui autorise à conclure d'une **quantité scalaire** — un résidu, une variance — à une **égalité de vecteurs**. On s'en sert au [module 2](02-cauchy-schwarz-et-angle.md) pour le cas d'égalité de Cauchy–Schwarz — une racine double $t_0$ y donne $\|u+t_0v\|^2=0$, donc $u+t_0v=0$, donc la colinéarité — et au
> [module 4](04-projection-orthogonale.md) pour le cas d'égalité qui caractérise la projection.

> 🔑 **La bilinéarité est l'outil de travail.** Les trois quarts des démonstrations de ce cours
> consistent à développer un produit scalaire par bilinéarité, puis à constater qu'un terme
> s'annule. Rien de plus.

---

## 1.2 Norme et distance

La troisième propriété — définie positive — permet de définir la **norme** :

$$\|u\|=\sqrt{\langle u,u\rangle}=\sqrt{\textstyle\sum_i u_i^2},
\qquad\text{et la distance}\qquad d(u,v)=\|u-v\|$$

L'identité de développement, utilisée en permanence dans toute la suite :

$$\|u+v\|^2=\|u\|^2+2\langle u,v\rangle+\|v\|^2$$

Elle se démontre en une ligne par bilinéarité :
$\langle u+v,u+v\rangle=\langle u,u\rangle+\langle u,v\rangle+\langle v,u\rangle+\langle v,v\rangle$, et les deux termes centraux sont égaux par symétrie.

> ⚠️ **Le terme croisé $2\langle u,v\rangle$ est le personnage principal du cours.** Le
> [module 3](03-orthogonalite-et-pythagore.md) est tout entier consacré au cas où il s'annule ;
> le [module 2](02-cauchy-schwarz-et-angle.md) au cas où il est maximal.

---

## 1.3 Norme et produit scalaire disent la même chose

La norme se déduit du produit scalaire par définition. La réciproque est vraie, et c'est
l'**identité de polarisation** :

$$\langle u,v\rangle=\tfrac12\bigl(\|u+v\|^2-\|u\|^2-\|v\|^2\bigr)$$

Elle s'obtient en isolant le terme croisé dans l'identité de développement du § 1.2.

> 🔑 **Géométrie des longueurs et géométrie des angles sont le même sujet.** Connaître toutes les longueurs, c'est connaître tous les angles. C'est la raison pour laquelle un résultat portant
> sur des sommes de carrés — une variance, par exemple — porte en réalité aussi sur des
> corrélations.

---

## 1.4 Simulation

### S1.1 — Les trois propriétés, vérifiées numériquement

```python
import numpy as np

rng = np.random.default_rng(1)
n = 10
u, v, w = rng.normal(size=n), rng.normal(size=n), rng.normal(size=n)
a, b = 2.5, -1.3

ps = lambda x, y: x @ y

print("symétrie     :", np.allclose(ps(u, v), ps(v, u)))
print("bilinéarité  :", np.allclose(ps(a*u + b*w, v), a*ps(u, v) + b*ps(w, v)))
print("définie pos. :", ps(u, u) > 0 and np.isclose(ps(np.zeros(n), np.zeros(n)), 0))

print("norme        :", np.allclose(np.sqrt(ps(u, u)), np.linalg.norm(u)))
print("développement:", np.allclose(ps(u+v, u+v), ps(u,u) + 2*ps(u,v) + ps(v,v)))
print("polarisation :", np.allclose(ps(u, v),
      0.5 * (np.linalg.no\ rm(u+v)**2 - np.linalg.norm(u)**2 - np.linalg.norm(v)**2)))
```

Les six tests affichent `True`. **Refaites-les en dimension 2** et dessinez les vecteurs : rien de ce qui suit n'est propre à la grande dimension, tout se voit déjà dans le plan.

---

## 1.5 Exercices

**E1.1.** Démontrer l'identité de polarisation du § 1.3 à partir de la seule identité de développement. *Quelle propriété du produit scalaire a-t-on utilisée pour égaler les deux termes croisés ?*

**E1.2.** Démontrer l'identité du parallélogramme $\|u+v\|^2+\|u-v\|^2=2\bigl(\|u\|^2+\|v\|^2\bigr)$. Puis l'appliquer à $u=(a,b)$, $v=(b,a)$ et interpréter. *(Piste : on retrouve $\operatorname{Var}$ et $\operatorname{Cov}$ de deux observations — voir le [module 7](07-dictionnaire-geometrique-des-statistiques.md).)*

**Preuve** : $\|u+v\|^2+\|u-v\|^2=2(\|u\|^2+\|v\|^2)$ par calcul direct ; $\|u\|^2=\langle u,u \rangle = a^2+b^2=\|v\|^2$
d'où $\|u+v\|^2+\|u-v\|^2=4(a^2+b^2)=4\|u\|$

**E1.3.** Montrer que $\|u\|=0\iff u=0$, et que $\|\lambda u\|=|\lambda|\,\|u\|$. *Laquelle des trois propriétés du § 1.1 chaque point utilise-t-il ?*

**Preuve :** 
* Soit $u=0$, supposons $u_i$ différent de 0, alors $\sum_i u_i^2 > 0$ et $\|u\| >0$ . cela  implique que seul $u=0 \implies \|u\|=0$
* Soit $\|u\|=0 = \sqrt{\sum_i u_i^2}$,supposons $w \neq 0$ tel que $\|w\|=0$ , alors $\sqrt{\sum_i w_i^2} > 0 > \|w\|$ ce qui contredit l'hypothèse et donc $\|u\|=0 \implies u=0$

**E1.4.** Soit $\mathbf 1=(1,\dots,1)\in\mathbb R^n$. Calculer $\|\mathbf 1\|^2$ et $\langle x,\mathbf 1\rangle$ pour $x$ quelconque. *Ces deux quantités, d'apparence anodine, sont tout ce dont le [module 5](05-supplementaire-orthogonal-et-dimension.md) aura besoin.*

**Calcul** :
* $\|\mathbf 1\|^2 = \langle1,1\rangle=\sum_i^n{1^2}=n$
* $\langle x, 1 \rangle=\sum_i^n x_i *1=n \bar x$
---

## 1.6 À retenir

- **$\langle u,v\rangle=\sum_i u_iv_i$** : symétrique, bilinéaire, définie positive.
- **$\|u\|=\sqrt{\langle u,u\rangle}$**, $d(u,v)=\|u-v\|$.
- **$\|u+v\|^2=\|u\|^2+2\langle u,v\rangle+\|v\|^2$** — l'identité qui sert partout ; tout le
  cours consiste à examiner le terme croisé.
- **Polarisation** : la norme détermine entièrement le produit scalaire.

---

➡️ [Module 2 — Cauchy–Schwarz et l'angle](02-cauchy-schwarz-et-angle.md) ·
🏠 [Sommaire](README.md)
