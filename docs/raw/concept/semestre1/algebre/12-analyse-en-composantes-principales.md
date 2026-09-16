# Module 12 — L'analyse en composantes principales

**Durée : 1 h 30.** Prérequis : modules [1](01-espace-vectoriel.md) à [11](11-covariance-et-produit-scalaire.md). **Module de sortie du cours.**

> **La question traitée.** Le [module 6](06-projection-orthogonale.md) projette sur un sous-espace **donné**. Que devient la question quand le sous-espace est précisément ce que l'on cherche ?

**Ce qui est en jeu.** C'est le seul module du cours dont la réponse n'est pas dans l'énoncé : les onze précédents calculent une quantité sur des objets fournis, celui-ci **choisit** l'objet. Il a un coût — il faut un théorème de plus, le théorème spectral, et ce module le démontre — et un dividende : la matrice de covariance cesse d'être un tableau de nombres pour devenir un nuage de points qu'on regarde sous son meilleur angle. Aucune probabilité n'intervient ici non plus : l'ACP est un problème de moindres carrés, rien d'autre.

---

## 12.1 Le second renversement de perspective

Le [§ 10.1](10-dictionnaire-geometrique-des-statistiques.md) a opéré le premier : une série de $n$ nombres n'est pas un nuage de $n$ points, c'est **un** vecteur de $\mathbb R^n$. Tout le cours vit depuis dans cet espace-là.

Reprenons le tableau du [§ 11.5](11-covariance-et-produit-scalaire.md) — $n$ lignes, $p$ colonnes, centré par colonne :

$$\tilde X\in\mathbb R^{n\times p},\qquad \Sigma=\frac1n\tilde X^{\top}\tilde X\in\mathbb R^{p\times p}$$

et lisons-le **dans l'autre sens**. Ses $p$ colonnes $\tilde x_1,\dots,\tilde x_p$ sont les séries, vecteurs de $\mathbb R^n$ : c'est la lecture des modules 10 et 11. Ses $n$ **lignes** $\tilde x^{(1)},\dots,\tilde x^{(n)}$ sont les **observations** — une date de cotation, un individu —, vecteurs de $\mathbb R^p$.

| Lecture | Un objet est | L'espace | Combien de points |
|---|---|---|---|
| Modules 10–11 | une **série** | $\mathbb R^n$ | $p$ |
| Ce module | une **observation** | $\mathbb R^p$ | $n$ |

> ⚠️ **C'est le même tableau, ce ne sont pas les mêmes points.** Rien de neuf n'entre dans les données au § 12.1 ; ce qui change est l'espace où on les regarde. Le § 12.6 montrera que les deux lectures rendent les **mêmes** nombres, ce qui est le plus court chemin pour se convaincre qu'aucune des deux n'est privilégiée.

Le nuage est donc formé des $n$ lignes, et la question du [§ 6.4](06-projection-orthogonale.md) s'écrit enfin avec ses indices :

> **Le problème.** Trouver le sous-espace $F\subseteq\mathbb R^p$ de dimension $d$ fixée qui minimise
> $$\sum_{i=1}^{n}\bigl\|\tilde x^{(i)}-P_F\bigl(\tilde x^{(i)}\bigr)\bigr\|^2$$

Chaque terme de la somme est ce que le [§ 6.3](06-projection-orthogonale.md) sait rendre minimal **à $F$ fixé**. Ce module résout ce qui reste : le choix de $F$.

### Pourquoi le nuage est centré

Le problème naturel porte sur les sous-espaces **affines** — une droite quelconque du plan, pas seulement celles qui passent par l'origine. Il faudrait donc chercher un point d'ancrage $a$ **et** une direction $F$ :

$$\min_{a,\,F}\ \sum_{i=1}^{n}\bigl\|Q\bigl(x^{(i)}-a\bigr)\bigr\|^2,
\qquad Q=I-P_F\ \text{le projecteur sur }F^{\perp}\ \text{([§ 7](07-supplementaire-orthogonal-et-dimension.md))}$$

À $F$ fixé, $Q$ est linéaire, et la somme vaut $\sum_i\|Qx^{(i)}-Qa\|^2$ : c'est la somme des carrés des écarts des $Qx^{(i)}$ à un point commun, que le [§ 8.1](08-degres-de-liberte-et-centrage.md) rend minimale au **barycentre**. Or $a=\bar x$ réalise $Qa=\overline{Qx}$, donc convient — quel que soit $F$.

> 🔑 **L'ancrage se résout avant la direction, et il vaut toujours la moyenne.** C'est pourquoi une ACP commence par centrer : non par convention, mais parce que la partie affine du problème est déjà résolue. Sur un nuage non centré, le premier axe serait dépensé à aller chercher le centre de gravité — une dimension gâchée à décrire un niveau.

---

## 12.2 L'inertie, et le pivot du module

> **Définition.** L'**inertie** du nuage est $\;\mathcal I=\dfrac1n\sum_{i=1}^{n}\bigl\|\tilde x^{(i)}\bigr\|^2$.

Elle ne dit rien de neuf. En sommant le tableau des carrés d'abord par lignes, puis par colonnes :

$$\sum_{i=1}^{n}\bigl\|\tilde x^{(i)}\bigr\|^2=\sum_{i=1}^n\sum_{j=1}^p \tilde X_{ij}^{\,2}=\sum_{j=1}^{p}\|\tilde x_j\|^2
\qquad\Longrightarrow\qquad
\boxed{\ \mathcal I=\sum_{j=1}^{p}\operatorname{Var}(x_j)=\operatorname{tr}\Sigma\ }$$

**L'inertie du nuage d'observations est la somme des variances des séries** — le même nombre, lu dans les deux espaces du § 12.1. C'est la première rencontre annoncée.

Vient maintenant le pivot, et il est gratuit : pour chaque $i$, $\tilde x^{(i)}=P_F\tilde x^{(i)}+\bigl(\tilde x^{(i)}-P_F\tilde x^{(i)}\bigr)$ est une décomposition orthogonale ([§ 6.2](06-projection-orthogonale.md)), donc [Pythagore](05-orthogonalite-et-pythagore.md) s'applique ; en sommant sur $i$ :

$$\underbrace{\mathcal I}_{\text{ne dépend pas de }F}
=\underbrace{\frac1n\sum_i\bigl\|P_F\tilde x^{(i)}\bigr\|^2}_{\text{inertie projetée}}
+\underbrace{\frac1n\sum_i\bigl\|\tilde x^{(i)}-P_F\tilde x^{(i)}\bigr\|^2}_{\text{inertie résiduelle}}$$

> ⭐ **Minimiser le résidu, c'est maximiser la projection.** Le total est une constante du nuage : les deux problèmes sont le **même**, et l'on peut choisir celui qui se calcule le mieux. Ce sera le second.

### L'inertie projetée est une trace

Le [§ 6.5](06-projection-orthogonale.md) donne $P^{\top}=P$ et $P^2=P$, donc $\|Pv\|^2=v^{\top}P^{\top}Pv=v^{\top}Pv$. En reconnaissant que $\frac1n\sum_i\tilde x^{(i)}\tilde x^{(i)\top}=\frac1n\tilde X^{\top}\tilde X=\Sigma$ :

$$\frac1n\sum_i\bigl\|P_F\tilde x^{(i)}\bigr\|^2
=\frac1n\sum_i\operatorname{tr}\Bigl(P_F\,\tilde x^{(i)}\tilde x^{(i)\top}\Bigr)
=\operatorname{tr}\bigl(P_F\,\Sigma\bigr)$$

> **Le problème, sous sa forme définitive.** Maximiser $\operatorname{tr}(P\Sigma)$ sur les projecteurs orthogonaux $P$ de rang $d$.

Le nuage a disparu de l'énoncé : **seule $\Sigma$ subsiste.** Deux jeux de données qui ont la même matrice de covariance ont les mêmes axes principaux.

---

## 12.3 La brique manquante : le théorème spectral

Le cours s'en est servi sans l'énoncer — la simulation [S11.3](11-covariance-et-produit-scalaire.md) lit « les valeurs propres de $\Sigma$ » pour vérifier qu'aucune n'est négative. Il est temps de le démontrer, d'autant que **sa démonstration est déjà la solution du § 12.2** : le premier vecteur propre est le maximiseur, et le reste est une récurrence.

> **Théorème spectral.** Soit $A$ une matrice **symétrique** réelle $p\times p$. Il existe une base orthonormée $(w_1,\dots,w_p)$ de $\mathbb R^p$ et des réels $\lambda_1\ge\lambda_2\ge\dots\ge\lambda_p$ tels que $Aw_k=\lambda_kw_k$. De façon équivalente, $A=W\Lambda W^{\top}=\sum_k\lambda_k\,w_kw_k^{\top}$ avec $W$ orthogonale ([§ 9.2](09-bases-orthonormees-et-isometries.md)).

**Démonstration.** Posons $q(w)=w^{\top}Aw$ sur la sphère unité $S=\{\|w\|=1\}$. La fonction est continue, $S$ est fermée et bornée : le maximum est atteint, en un point $w_1$, et l'on note $\lambda_1=q(w_1)$.

*Le maximiseur est un vecteur propre.* Soit $u$ unitaire orthogonal à $w_1$. Le chemin $w(\theta)=\cos\theta\,w_1+\sin\theta\,u$ reste sur $S$ ([§ 5.2](05-orthogonalite-et-pythagore.md) : $\|w(\theta)\|^2=\cos^2\theta+\sin^2\theta=1$), et la symétrie de $A$ donne $w_1^{\top}Au=\langle Aw_1,u\rangle$, d'où

$$q\bigl(w(\theta)\bigr)=\cos^2\theta\,\lambda_1+2\cos\theta\sin\theta\,\langle Aw_1,u\rangle+\sin^2\theta\,q(u)$$

Cette fonction d'une variable est dérivable et maximale en $\theta=0$ ; sa dérivée y est donc nulle, et elle vaut $2\langle Aw_1,u\rangle$. Ainsi $Aw_1\perp u$ pour **tout** $u\perp w_1$, c'est-à-dire $Aw_1\in\bigl(w_1^{\perp}\bigr)^{\perp}=\text{Vect}(w_1)$ ([§ 7](07-supplementaire-orthogonal-et-dimension.md)). Donc $Aw_1=\lambda w_1$, et $\lambda=w_1^{\top}Aw_1=\lambda_1$.

*La récurrence.* L'hyperplan $E=w_1^{\perp}$, de dimension $p-1$, est **stable** par $A$ : si $u\perp w_1$, alors $\langle Au,w_1\rangle=\langle u,Aw_1\rangle=\lambda_1\langle u,w_1\rangle=0$. La restriction de $A$ à $E$ est encore symétrique ; on recommence dans $E$, et ainsi de suite. Les vecteurs obtenus sont orthogonaux deux à deux par construction, et les maxima sont pris sur des ensembles de plus en plus petits, d'où $\lambda_1\ge\lambda_2\ge\dots$ $\blacksquare$

**Et pour une matrice de covariance, les valeurs propres sont positives.** $\lambda_k=w_k^{\top}\Sigma w_k\ge0$ : c'est la semi-définie positivité du [§ 11.5](11-covariance-et-produit-scalaire.md), autrement dit le fait qu'aucun portefeuille n'a de variance négative. La ligne de S11.3 n'était donc pas une observation empirique, c'était un théorème.

---

## 12.4 Le théorème de l'ACP

> **Théorème.** Pour tout sous-espace $F$ de dimension $d$,
> $$\operatorname{tr}\bigl(P_F\Sigma\bigr)\;\le\;\lambda_1+\dots+\lambda_d$$
> avec égalité pour $F=\text{Vect}(w_1,\dots,w_d)$. Les $w_k$ s'appellent les **axes principaux**.

**Démonstration.** Injectons $\Sigma=\sum_k\lambda_kw_kw_k^{\top}$ dans la trace, et utilisons de nouveau $w^{\top}Pw=\|Pw\|^2$ :

$$\operatorname{tr}(P_F\Sigma)=\sum_{k=1}^{p}\lambda_k\,w_k^{\top}P_Fw_k=\sum_{k=1}^{p}\lambda_k\,c_k,
\qquad c_k=\bigl\|P_Fw_k\bigr\|^2$$

Ces $p$ coefficients obéissent à deux contraintes, et à deux seulement :

- $0\le c_k\le1$, car $\|P_Fw_k\|\le\|w_k\|=1$ (exercice [E6.3](06-projection-orthogonale.md)) ;
- $\sum_k c_k=\sum_k w_k^{\top}P_Fw_k=\operatorname{tr}(P_F)=d$, car $(w_k)$ est une base orthonormée et que **la trace d'un projecteur est sa dimension** ([§ 6.5](06-projection-orthogonale.md)).

Il ne reste qu'à borner. Avec $\lambda_k\ge\lambda_d$ pour $k\le d$ et $\lambda_k\le\lambda_d$ pour $k>d$ :

$$\sum_k\lambda_kc_k-\sum_{k\le d}\lambda_k
=\underbrace{\sum_{k\le d}\lambda_k(c_k-1)}_{\le\ \lambda_d\sum_{k\le d}(c_k-1)}
+\underbrace{\sum_{k>d}\lambda_kc_k}_{\le\ \lambda_d\sum_{k>d}c_k}
\;\le\;\lambda_d\Bigl(\sum_kc_k-d\Bigr)=0$$

*(Les deux majorations changent de sens pour la même raison : $c_k-1\le0$ d'un côté, $c_k\ge0$ de l'autre.)* Enfin, pour $F=\text{Vect}(w_1,\dots,w_d)$ on a $c_k=1$ si $k\le d$ et $c_k=0$ sinon, ce qui atteint la borne. $\blacksquare$

Trois conséquences immédiates :

- **Les sous-espaces optimaux sont emboîtés** : $F_1\subset F_2\subset\dots$. Passer de $d$ à $d+1$ ajoute un axe sans remettre en cause les précédents — c'est une propriété du problème, pas une commodité de calcul.
- **L'inertie résiduelle vaut $\lambda_{d+1}+\dots+\lambda_p$** : ce que l'on perd est la somme des valeurs propres qu'on a laissées.
- **Le meilleur plan contient la meilleure droite.** Rien n'obligeait à cela : c'est faux pour bien d'autres critères d'approximation.

### Les composantes principales

Projeter le nuage sur l'axe $w_k$ et lire la coordonnée définit une nouvelle **série** de $n$ nombres, $c_k=\tilde Xw_k\in\mathbb R^n$ — retour dans l'espace des modules 10 et 11. Deux faits, tous deux en une ligne :

$$\operatorname{Var}(c_k)=\frac1n\|\tilde Xw_k\|^2=w_k^{\top}\Sigma w_k=\lambda_k,
\qquad
\operatorname{Cov}(c_j,c_k)=w_j^{\top}\Sigma w_k=\lambda_k\,\langle w_j,w_k\rangle=0\ \ (j\ne k)$$

> 🔑 **L'ACP fabrique $p$ séries décorrélées, de variances $\lambda_1\ge\dots\ge\lambda_p$ et de même inertie totale.** Dans le dictionnaire du [module 10](10-dictionnaire-geometrique-des-statistiques.md), décorrélé signifie orthogonal : l'ACP est donc un **changement de base orthonormée** ([module 9](09-bases-orthonormees-et-isometries.md)), c'est-à-dire une rotation du nuage — celle qui aligne les axes de coordonnées sur les directions d'allongement. Une isométrie ne change ni les longueurs ni les angles : elle ne crée aucune information, elle en change la présentation.

---

## 12.5 Ce que l'éboulis dit, et ce qu'il ne dit pas

La **part d'inertie** de l'axe $k$ est $\lambda_k/\operatorname{tr}\Sigma$, et l'on trace la suite décroissante des $\lambda_k$ — l'**éboulis des valeurs propres**.

> ⚠️ **« 90 % de l'inertie » n'est pas « 90 % de l'information ».** L'inertie est une somme de variances, donc de carrés de longueurs ; elle ignore tout ce qui, dans les données, ne se voit pas comme une dispersion. Une variable rare mais décisive pèse peu dans $\operatorname{tr}\Sigma$ et sera rangée dans les derniers axes.

### Le choix des unités, qui n'en est pas un

C'est le point qui décide du résultat, et il précède tout calcul.

$$\operatorname{Cov}(ax_j,\,x_k)=a\operatorname{Cov}(x_j,x_k)\qquad\text{([E11.4](11-covariance-et-produit-scalaire.md))}$$

Multiplier une colonne par $a$ n'est **pas** une isométrie : cela déforme le nuage dans une direction et déplace ses axes principaux. Une ACP faite sur des cours en centimes ne donne pas les mêmes axes que sur les mêmes cours en euros.

| | Ce qu'on diagonalise | Ce que cela suppose |
|---|---|---|
| ACP **non normée** | $\Sigma$ | Les unités sont comparables, et l'échelle est l'information |
| ACP **normée** | $R$, la corrélation ([§ 11.6](11-covariance-et-produit-scalaire.md)) | Seule la forme compte ; chaque série pèse pareil |

L'ACP normée revient à diviser chaque série par son écart-type : $\operatorname{tr}R=p$, chaque variable apporte exactement $1$ d'inertie, et un axe « vaut mieux qu'une variable moyenne » quand $\lambda_k>1$ — règle empirique commode, **jamais un test**.

> ⚠️ **Sur des rendements, les deux choix sont défendables, et ils ne disent pas la même chose.** Toutes les séries sont dans la même unité, donc la normalisation n'est pas imposée ; mais s'en abstenir donne le premier axe aux valeurs les plus volatiles — ce qui est légitime si l'objet est le risque en euros, et trompeur si l'objet est la structure des mouvements. Comme partout dans ce dépôt : **une convention ne se devine pas depuis des nombres**, elle se déclare.

---

## 12.6 La dualité : les deux matrices de Gram

Le § 12.1 annonçait deux lectures. Chacune a sa matrice de Gram ([§ 11.5](11-covariance-et-produit-scalaire.md)) :

$$\Sigma=\frac1n\tilde X^{\top}\tilde X\ \ (p\times p,\ \text{entre séries})
\qquad\text{et}\qquad
G=\frac1n\tilde X\tilde X^{\top}\ \ (n\times n,\ \text{entre observations})$$

> **Proposition.** $\Sigma$ et $G$ ont les mêmes valeurs propres **non nulles**, et si $\Sigma w=\lambda w$ avec $\lambda\ne0$, alors $\tilde Xw$ est vecteur propre de $G$ pour la même valeur propre.

**Démonstration.** $G(\tilde Xw)=\frac1n\tilde X\tilde X^{\top}\tilde Xw=\tilde X\Sigma w=\lambda\,\tilde Xw$, et $\tilde Xw\ne0$ puisque $\|\tilde Xw\|^2=n\,w^{\top}\Sigma w=n\lambda\|w\|^2\ne0$. On échange les rôles de $\tilde X$ et $\tilde X^{\top}$ pour la réciproque. $\blacksquare$

**Le vecteur propre de $G$ est la composante principale** $c=\tilde Xw$ : projeter les observations sur les axes des séries, ou les séries sur les axes des observations, produit les mêmes nombres. Aucune des deux lectures n'est la bonne.

### Le rang, et une limite qu'aucune donnée ne franchit

Les colonnes de $\tilde X$ sont centrées, donc vivent dans l'hyperplan $H=\text{Vect}(\mathbf 1)^{\perp}$, de dimension $n-1$ ([§ 8.1](08-degres-de-liberte-et-centrage.md)). D'où

$$\operatorname{rang}\Sigma=\operatorname{rang}\tilde X\;\le\;\min(n-1,\ p)$$

> ⚠️ **Avec plus de séries que d'observations, $\Sigma$ a des valeurs propres nulles — nécessairement.** Au moins $p-(n-1)$ d'entre elles. Ce n'est pas un défaut des données ni un accident numérique : c'est la dimension de $H$, et le $-1$ est le prix du centrage compté au [module 8](08-degres-de-liberte-et-centrage.md). C'est exactement l'exercice [E11.8](11-covariance-et-produit-scalaire.md), relu dans l'autre espace.

---

## 12.7 Ce que l'ACP ne fait pas

Quatre limites, dont trois sont des invariants du dépôt.

1. **Elle ne teste rien.** Aucune loi, aucune $p$-valeur, aucun seuil : l'ACP est un calcul déterministe sur un tableau, au même titre qu'une moyenne. « Le premier axe porte 62 % de l'inertie » est une description, pas un résultat significatif.
2. **Un axe n'est pas une cause.** Nommer le deuxième axe « l'opposition cyclique / défensif » est une **lecture** ajoutée par l'analyste ; la matrice, elle, n'a produit qu'une direction. Rien n'interdit à un axe de n'avoir aucune interprétation.
3. ⚠️ **Le premier axe d'un panier d'actions est toujours « le marché », et ce n'est pas une découverte.** Dès que toutes les corrélations sont positives, le premier vecteur propre a toutes ses composantes de même signe : l'ACP retrouve la moyenne pondérée des valeurs, c'est-à-dire l'indice, et par là le $\beta$ du [cours d'alpha](../../semestre4/alpha/README.md). Le cas $\rho$ commun de l'exercice E12.4 le montre en une ligne.
4. ⚠️ **Les axes sont estimés sur une fenêtre ; les y appliquer est un regard en avant.** Projeter les données de la fenêtre sur les axes que cette même fenêtre a fabriqués ne mesure rien — c'est le vice exact que le [laboratoire](../../../lab/README.md) documente pour les bandes de régression : une bande qui contenait 67,8 % de son propre ajustement n'a contenu que 0,8 % de l'année suivante. Un éboulis se lit hors de la fenêtre qui l'a produit, ou ne se lit pas.

**Et une mise en garde d'estimation.** Sur $p$ séries **indépendantes** observées $n$ fois, l'éboulis empirique n'est pas plat : le plus grand $\lambda$ dépasse largement $1$ dès que $p/n$ n'est pas négligeable. La simulation S12.4 le montre en huit lignes — et c'est le fond du § 9.2 du [module sur l'estimation en finance](../../semestre4/finance/09-contraintes-reelles-et-estimation.md), où 820 paramètres sont estimés sur 60 rendements mensuels.

---

## 12.8 Simulations

### S12.1 — Le meilleur axe, cherché à la main

Dans l'esprit de [S6.1](06-projection-orthogonale.md) : on balaye toutes les directions et on regarde laquelle gagne.

```python
import numpy as np

rng = np.random.default_rng(12)
n = 400
u = rng.normal(0, 1, n)
X = np.column_stack([2.0 * u + rng.normal(0, 0.5, n),      # deux series correlees
                     1.0 * u + rng.normal(0, 0.5, n)])
Xt = X - X.mean(axis=0)
Sigma = Xt.T @ Xt / n

# balayage : inertie projetee sur la droite d'angle theta
theta = np.linspace(0, np.pi, 20_001)
W = np.column_stack([np.cos(theta), np.sin(theta)])
inertie = np.einsum("ij,jk,ik->i", W, Sigma, W)          # w^T Sigma w

lam, vec = np.linalg.eigh(Sigma)                          # eigh : matrice symetrique
lam, vec = lam[::-1], vec[:, ::-1]                        # par valeur propre decroissante

print(f"balayage  : theta = {np.degrees(theta[inertie.argmax()]):.3f} deg"
      f"   inertie = {inertie.max():.5f}")
print(f"eigh      : theta = {np.degrees(np.arctan2(vec[1, 0], vec[0, 0])) % 180:.3f} deg"
      f"   lambda1 = {lam[0]:.5f}")
print(f"inertie totale = {np.trace(Sigma):.5f}   somme des lambda = {lam.sum():.5f}")
```

Le maximum du balayage tombe sur le premier vecteur propre, à la maille près, et sa valeur est $\lambda_1$. **Le théorème du § 12.4 n'a rien ajouté au problème** : il a seulement évité d'avoir à balayer — ce qui devient impossible dès la dimension 3.

### S12.2 — L'axe principal n'est pas la droite des moindres carrés

```python
pente_acp = vec[1, 0] / vec[0, 0]
pente_mco = (Xt[:, 0] @ Xt[:, 1]) / (Xt[:, 0] @ Xt[:, 0])     # regression de x2 sur x1
print(f"axe principal : {pente_acp:.4f}      moindres carres : {pente_mco:.4f}")

# la seconde est equivariante par changement d'unite, la premiere non
Y = Xt * np.array([1.0, 100.0])                                # x2 en centimes
Sy = Y.T @ Y / n
vy = np.linalg.eigh(Sy)[1][:, ::-1]
print(f"apres x100  ->  acp : {vy[1, 0] / vy[0, 0] / 100:.4f}"
      f"   mco : {(Y[:, 0] @ Y[:, 1]) / (Y[:, 0] @ Y[:, 0]) / 100:.4f}")
```

Relues dans l'unité de départ, la pente des moindres carrés est **inchangée** ; celle de l'axe principal a bougé. C'est l'avertissement du [§ 6.4](06-projection-orthogonale.md) : les deux droites ne répondent pas à la même question, et une seule des deux ignore les unités.

### S12.3 — Trace, décorrélation, reconstruction

```python
p = 5
Z = rng.normal(size=(n, p)) @ rng.normal(size=(p, p))
Zt = Z - Z.mean(axis=0)
S = Zt.T @ Zt / n
lam, W = np.linalg.eigh(S)
lam, W = lam[::-1], W[:, ::-1]

C = Zt @ W                                                     # composantes principales
print("Var(c_k) = lambda_k :", np.allclose(C.var(axis=0), lam))
print("composantes decorrelees :", np.allclose(np.cov(C.T, bias=True) - np.diag(lam), 0, atol=1e-10))

for d in range(1, p + 1):
    P = W[:, :d] @ W[:, :d].T                                  # projecteur de rang d
    projetee = np.trace(P @ S)
    residuelle = ((Zt - Zt @ P) ** 2).sum() / n
    print(f"d={d}  trace(P)={np.trace(P):.4f}  projetee={projetee:9.4f}"
          f"  residuelle={residuelle:9.4f}  somme={projetee + residuelle:9.4f}"
          f"  part={projetee / np.trace(S):6.2%}")
```

La colonne `somme` ne bouge pas d'une décimale : c'est le Pythagore du § 12.2. Et `trace(P)` vaut exactement $d$ — le [§ 6.5](06-projection-orthogonale.md), devenu un outil de contrôle.

### S12.4 — L'éboulis du bruit pur, et le rang qui plafonne

```python
for (n_obs, p_ser) in ((2000, 10), (60, 10), (30, 40)):
    B = rng.normal(size=(n_obs, p_ser))                        # series INDEPENDANTES
    R = np.corrcoef(B.T)
    v = np.linalg.eigvalsh(R)[::-1]
    print(f"n={n_obs:5d}  p={p_ser:3d}  ->  lambda1 = {v[0]:.3f}"
          f"   lambda_min = {v[-1]:.3f}   rang = {np.linalg.matrix_rank(R)}"
          f"   (borne : {min(n_obs - 1, p_ser)})")
```

Les séries sont indépendantes : l'éboulis **devrait** être plat à $\lambda_k=1$. Il ne l'est qu'avec beaucoup d'observations. Sur la dernière ligne, $p$ dépasse $n-1$ et le rang plafonne exactement où le § 12.6 l'annonce — **la matrice est singulière avant même d'avoir regardé les données**.

---

## 12.9 Exercices

**E12.1.** Démontrer que l'inertie totale ne dépend pas de $F$, et en déduire l'équivalence « minimiser le résidu $\Leftrightarrow$ maximiser la projection ». *Quel théorème du [module 5](05-orthogonalite-et-pythagore.md) est utilisé, et combien de fois ?*

**E12.2.** Soit $(f_1,\dots,f_d)$ une base orthonormée quelconque de $F$. Montrer que $\operatorname{tr}(P_F\Sigma)=\sum_j f_j^{\top}\Sigma f_j$. *Pourquoi ce nombre ne dépend-il pas de la base choisie — et où retrouve-t-on l'encadré 🔑 du [§ 6.4](06-projection-orthogonale.md) ?*

**E12.3.** En dimension 2, avec $\Sigma=\begin{pmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\\rho\sigma_1\sigma_2&\sigma_2^2\end{pmatrix}$, calculer $\lambda_1,\lambda_2$ et le premier axe. *Traiter à part le cas $\sigma_1=\sigma_2$ : que vaut l'angle du premier axe, et pourquoi ne dépend-il pas de $\rho$ ? Comparer à la pente des moindres carrés $\rho\sigma_2/\sigma_1$.*

**E12.4.** Soit $R=(1-\rho)I_p+\rho\,\mathbf 1\mathbf 1^{\top}$, la corrélation commune de l'exercice [E11.6](11-covariance-et-produit-scalaire.md). Montrer que ses valeurs propres sont $1+(p-1)\rho$ **une fois** et $1-\rho$ **$p-1$ fois**, et que le premier axe est $\mathbf 1/\sqrt p$. *En déduire le point 3 du § 12.7 : la part d'inertie du premier axe, et pourquoi il vaut l'indice équipondéré. Retrouver enfin $\rho\ge-\frac1{p-1}$ par la positivité des valeurs propres.*

**E12.5.** Montrer que les composantes principales sont décorrélées **et** que l'on passe des données à elles par une isométrie ([module 9](09-bases-orthonormees-et-isometries.md)). *Quelle quantité est donc conservée, et pourquoi cela interdit-il de parler d'information « créée » par une ACP ?*

**E12.6.** Reprendre la reconstruction tronquée de S12.3 et démontrer que $\hat X_d=\tilde XW_dW_d^{\top}$ minimise $\|\tilde X-Y\|_F^2=\sum_{i,j}(\tilde X-Y)_{ij}^2$ parmi les matrices $Y$ de rang $\le d$. *(Piste : la norme de Frobenius est la norme euclidienne du tableau vu comme un vecteur de $\mathbb R^{np}$, et $\sum_{i,j}$ se regroupe par lignes.)*

**E12.7 — orientée finance.** À partir de dix séries obtenues avec [`import_societe.py`](../../../../../python/import_societe.md) :
1. construire les rendements quotidiens, puis $\Sigma$ et $R$ ;
2. faire l'ACP normée et tracer l'éboulis. *Quelle part porte le premier axe ?*
3. calculer la corrélation entre la première composante et le rendement de l'indice reconstruit par [`construire_indice_total.py`](../../../../../python/construire_indice_total.md). *Que reste-t-il de « découverte » dans le premier axe ?*
4. refaire l'ACP **sans** normer. *Quelles valeurs prennent le premier plan, et pourquoi ?*
5. estimer les axes sur le premier semestre, les appliquer au second, et comparer les parts d'inertie. *Commenter à la lumière du point 4 du § 12.7.*

---

## 12.10 À retenir

- **L'ACP est le [module 6](06-projection-orthogonale.md) retourné** : le sous-espace n'est plus donné, il est **cherché**. Le § 6.3 résout le problème à $F$ fixé ; l'ACP choisit $F$.
- **Le nuage est celui des observations**, dans $\mathbb R^p$ — le second renversement de perspective après celui du [§ 10.1](10-dictionnaire-geometrique-des-statistiques.md).
- **On centre parce que la partie affine est déjà résolue** : le meilleur ancrage est le barycentre, quel que soit $F$.
- ⭐ **Minimiser le résidu, c'est maximiser l'inertie projetée** — Pythagore, et le total ne dépend pas de $F$.
- ⭐ **Le problème s'écrit $\max\operatorname{tr}(P\Sigma)$ à rang fixé**, et sa solution est donnée par le **théorème spectral** : les $d$ premiers vecteurs propres de $\Sigma$, pour une inertie de $\lambda_1+\dots+\lambda_d$.
- **Les sous-espaces optimaux sont emboîtés**, et les composantes principales sont **décorrélées**, de variances les $\lambda_k$ : une ACP est une **rotation**.
- ⚠️ **Le résultat dépend des unités** : $\Sigma$ ou $R$ est un choix à déclarer, jamais à deviner.
- **$\operatorname{rang}\Sigma\le\min(n-1,p)$** : plus de séries que d'observations, et des valeurs propres nulles sont garanties — le $-1$ est le coût du centrage.
- ⚠️ **L'ACP ne teste rien, un axe n'est pas une cause, et un éboulis lu dans sa propre fenêtre d'ajustement ne mesure rien.**

---

⬅️ [Module 11 — La covariance comme produit scalaire](11-covariance-et-produit-scalaire.md) ·
🏠 [Sommaire](README.md) ·
➡️ **Suite** : [Cours de statistique mathématique](../../semestre2/statistique/mathematique/README.md)
