# Module 5 — Dérivées partielles, différentielle, gradient

**Durée : 1 h.** Prérequis : [module 1](01-derivee-et-approximation-affine.md).

> **La question traitée.** Comment dérive-t-on une fonction de plusieurs variables — et pourquoi
> « calculer les dérivées partielles » ne suffit-il pas ?

**Ce qui est en jeu.** [`modele.md`](../../../../modele.md) annule deux dérivées partielles pour obtenir les
équations normales. L'opération est correcte, mais elle suppose acquis un point qui ne va pas de
soi : **l'existence des dérivées partielles n'entraîne pas la différentiabilité**, et seule la
seconde autorise les règles de calcul. Ce module installe la distinction, puis le gradient.

---

## 5.1 Dérivées partielles

> **Définition.** Pour $f:\mathbb R^n\to\mathbb R$, la **dérivée partielle** par rapport à $x_j$
> en $a$ est
> $$\partial_jf(a)=\frac{\partial f}{\partial x_j}(a)=\lim_{h\to0}\frac{f(a+he_j)-f(a)}{h}$$
> où $e_j$ est le $j$-ième vecteur de la base canonique.

**C'est une dérivée ordinaire**, celle de la fonction d'une variable
$t\mapsto f(a_1,\dots,t,\dots,a_n)$ obtenue en **gelant** toutes les autres coordonnées. On la
calcule donc avec les règles du [module 1](01-derivee-et-approximation-affine.md), sans rien
apprendre de nouveau.

**Exemple, celui de `modele.md`.** $S(v_0,r)=\frac1n\sum_i(V_i-v_0-rT_i)^2$ :

$$\frac{\partial S}{\partial v_0}=-\frac2n\sum_i\big(V_i-v_0-rT_i\big),
\qquad
\frac{\partial S}{\partial r}=-\frac2n\sum_iT_i\big(V_i-v_0-rT_i\big).$$

Annuler les deux donne les **équations normales** — et le
[§ 7.5](07-calcul-matriciel-des-derivees.md) montrera comment obtenir la même chose en une ligne,
sans jamais écrire de somme.

---

## 5.2 ⚠️ Partielles $\ne$ différentiabilité

> **Définition (différentiabilité).** $f$ est **différentiable** en $a$ s'il existe une
> application **linéaire** $L$ telle que
> $$f(a+h)=f(a)+L(h)+o\big(\lVert h\rVert\big).$$
> $L$ est alors unique, notée $\mathrm df_a$, et $L(h)=\sum_j\partial_jf(a)\,h_j$.

C'est **mot pour mot** la définition B du [module 1](01-derivee-et-approximation-affine.md), avec
$\lVert h\rVert$ à la place de $\lvert h\rvert$. Et c'est une condition **strictement plus forte**
que l'existence des partielles.

**Le contre-exemple à connaître.**

$$f(x,y)=\frac{xy}{x^2+y^2}\ \ \text{si }(x,y)\ne(0,0),\qquad f(0,0)=0 .$$

- Les deux partielles **existent** en $(0,0)$ et valent **0** : sur les axes, $f$ est
  identiquement nulle.
- Pourtant $f$ n'est même pas **continue** en $(0,0)$ : sur la droite $y=x$, $f=\frac12$ partout,
  donc $f(t,t)\to\frac12\ne0$.

> ⚠️ **Deux dérivées partielles nulles, et la fonction ne tend même pas vers sa valeur.** Les
> partielles ne regardent que **deux directions** ; la différentiabilité exige un contrôle
> **uniforme dans toutes les directions**. C'est la raison pour laquelle « j'ai annulé le
> gradient » n'a de sens que si la fonction est différentiable.

**Le théorème qui sauve la pratique :**

> **Théorème (admis).** Si toutes les dérivées partielles existent **et sont continues** au
> voisinage de $a$, alors $f$ est différentiable en $a$. On dit que $f$ est de classe $C^1$.

En pratique, **toutes** les fonctions de ce dépôt (polynômes, exponentielles, logarithmes,
quotients à dénominateur non nul) sont $C^\infty$ : la difficulté ci-dessus ne se rencontre jamais
sur elles. Il faut néanmoins savoir qu'elle existe — c'est ce qui distingue un calcul d'un
théorème.

---

## 5.3 Gradient, plan tangent, direction de plus forte pente

> **Définition.** Le **gradient** est le vecteur **colonne** des dérivées partielles :
> $$\nabla f(a)=\begin{pmatrix}\partial_1f(a)\\\vdots\\\partial_nf(a)\end{pmatrix}
> \qquad\text{de sorte que}\qquad \mathrm df_a(h)=\big\langle\nabla f(a),h\big\rangle .$$

L'approximation affine s'écrit alors

$$\boxed{\;f(a+h)=f(a)+\big\langle\nabla f(a),\,h\big\rangle+o(\lVert h\rVert)\;}$$

et le graphe de $h\mapsto f(a)+\langle\nabla f(a),h\rangle$ est le **plan tangent**.

**Trois lectures du gradient**, toutes utiles :

| Lecture | Énoncé | Conséquence |
|---|---|---|
| **Dérivée directionnelle** | $\partial_uf(a)=\langle\nabla f(a),u\rangle$ pour $\lVert u\rVert=1$ | Une seule quantité donne toutes les directions |
| **Plus forte pente** | Le maximum de $\langle\nabla f,u\rangle$ est atteint en $u=\frac{\nabla f}{\lVert\nabla f\rVert}$ | Par **Cauchy–Schwarz** ([algèbre § 3](../../algebre/03-cauchy-schwarz-et-angle.md)) |
| **Orthogonalité** | $\nabla f(a)\perp$ la ligne de niveau passant par $a$ | Les courbes de niveau coupent le gradient à angle droit |

> 🔑 **La direction de plus forte pente est un cas d'égalité de Cauchy–Schwarz.** Le gradient
> n'indique pas seulement *combien* $f$ varie, mais *dans quelle direction elle varie le plus* — et
> la démonstration est celle du module 2 d'algèbre, sans un mot de plus.

⚠️ **Le gradient dépend du produit scalaire choisi.** Avec le produit scalaire canonique, c'est le
vecteur des partielles ; avec un autre, ce serait autre chose. Dans tout ce cours, le produit
scalaire est celui de l'[algèbre](../../algebre/02-produit-scalaire-et-norme.md) : $\sum_iu_iv_i$.

---

## 5.4 Dérivées d'ordre 2 et Hessienne

> **Définition.** $H_f(a)=\big(\partial_i\partial_jf(a)\big)_{1\le i,j\le n}$.

> **Théorème de Schwarz (admis).** Si $f$ est de classe $C^2$, alors
> $\partial_i\partial_jf=\partial_j\partial_if$ : **la Hessienne est symétrique.**

C'est cette symétrie qui autorise le [cours de convexité](../convexite/07-convexite-en-dimension-n.md)
à parler de $H_f\succeq0$ : « semi-définie positive » n'a de sens que pour une matrice symétrique.

**Le développement à l'ordre 2** devient

$$f(a+h)=f(a)+\langle\nabla f(a),h\rangle+\tfrac12\,h^{\top}H_f(a)\,h+o\big(\lVert h\rVert^2\big),$$

qui est le Taylor du [module 2](02-taylor-et-approximations.md) avec une **forme quadratique** à
la place de $\frac{f''(a)}2h^2$.

| Objet | Dimension 1 | Dimension $n$ |
|---|---|---|
| Ordre 1 | $f'(a)h$ | $\langle\nabla f(a),h\rangle$ |
| Ordre 2 | $\frac12f''(a)h^2$ | $\frac12h^{\top}H_f(a)h$ |
| Convexité | $f''\ge0$ | $H_f\succeq0$ |

---

## 5.5 Vérification numérique

### S5.1 — Gradient analytique contre différences finies

```python
import numpy as np

rng = np.random.default_rng(5)

def gradient_num(f, x, h=1e-6):
    g = np.zeros_like(x, dtype=float)
    for j in range(x.size):
        e = np.zeros_like(x, dtype=float); e[j] = h
        g[j] = (f(x + e) - f(x - e)) / (2 * h)
    return g

# la fonction de modele.md, en (v0, r)
n = 40
T = np.arange(1., n + 1)
V = 100 + 0.8 * T + rng.normal(0, 3, n)
S = lambda p: np.mean((V - p[0] - p[1] * T) ** 2)
grad_S = lambda p: np.array([-2 * np.mean(V - p[0] - p[1] * T),
                             -2 * np.mean(T * (V - p[0] - p[1] * T))])

p = np.array([95.0, 1.1])
print("gradient analytique :", np.round(grad_S(p), 8))
print("differences finies  :", np.round(gradient_num(S, p), 8))
print("ecart max           :", np.abs(grad_S(p) - gradient_num(S, p)).max())
```

**Écrire cette vérification avant de faire confiance à un gradient calculé à la main** est la
règle du cours. Elle détecte en trois lignes un signe oublié, un facteur 2 manquant, une somme mal
indexée.

### S5.2 — Le contre-exemple des partielles

```python
def f(x, y):
    return np.where((x == 0) & (y == 0), 0.0, x * y / (x ** 2 + y ** 2 + 1e-300))

h = np.array([1e-1, 1e-2, 1e-3, 1e-6])
print("le long de l'axe x :", f(h, 0 * h))       # -> 0 : la partielle existe et vaut 0
print("le long de l'axe y :", f(0 * h, h))       # -> 0
print("le long de y = x   :", f(h, h))           # -> 0.5 : pas de limite en (0,0)
```

Deux partielles nulles, une fonction discontinue. **La différentiabilité n'est pas la conjonction
de deux dérivées à une variable.**

---

## 5.6 Exercices

**E5.1.** Calculer les deux dérivées partielles de $S(v_0,r)$ et retrouver les équations normales
de [`modele.md`](../../../../modele.md), étape 1. *Vérifier que la première donne bien « les résidus sont
de moyenne nulle ».*

**E5.2.** Montrer que $f(x,y)=\frac{xy}{x^2+y^2}$ (prolongée par 0) admet des dérivées partielles
en $(0,0)$ mais n'y est pas continue. *Quelle hypothèse du théorème du § 5.2 est violée ?*

**E5.3.** Démontrer, par Cauchy–Schwarz, que la dérivée directionnelle est maximale dans la
direction du gradient et vaut alors $\lVert\nabla f\rVert$.

**E5.4.** Calculer $\nabla f$ et $H_f$ pour $f(w)=w^{\top}\Sigma w$ avec $\Sigma$ symétrique.
*Comparer au [§ 7.3 du cours de convexité](../convexite/07-convexite-en-dimension-n.md).*

**E5.5.** Soit $f(x,y)=e^{x}\log(1+y)$. Vérifier le théorème de Schwarz en calculant
$\partial_x\partial_yf$ et $\partial_y\partial_xf$.

**E5.6.** Écrire une fonction `hessienne_num(f, x, h=1e-4)` par différences finies d'ordre 2 et la
tester sur $f(x,y)=x^2+3xy+2y^2$. *Pourquoi un pas $h$ plus grand qu'au § 5.5 est-il ici
préférable ?*

---

## 5.7 À retenir

- **Dérivée partielle** = dérivée ordinaire, les autres variables **gelées**.
- ⚠️ **Partielles $\ne$ différentiabilité** : $\frac{xy}{x^2+y^2}$ a deux partielles nulles en
  l'origine sans y être continue. Ce qui sauve la pratique : **partielles continues $\Rightarrow$
  différentiable** ($C^1$).
- ⭐ **$f(a+h)=f(a)+\langle\nabla f(a),h\rangle+o(\lVert h\rVert)$** : c'est la définition B du
  module 1, transportée telle quelle.
- **Le gradient** donne les dérivées directionnelles, pointe la **plus forte pente** (cas
  d'égalité de Cauchy–Schwarz) et est **orthogonal aux lignes de niveau**.
- **Hessienne symétrique** (Schwarz) $\Rightarrow$ l'ordre 2 s'écrit $\frac12h^{\top}H_fh$, et
  « $H_f\succeq0$ » a un sens.
- **Toujours vérifier un gradient par différence finie centrée** avant de s'en servir.

---

⬅️ [Module 4 — Intégrales généralisées, $\Gamma$, et les moments](04-integrales-generalisees-et-moments.md) ·
➡️ [Module 6 — La matrice jacobienne](06-la-matrice-jacobienne.md) ·
🏠 [Sommaire](README.md)
