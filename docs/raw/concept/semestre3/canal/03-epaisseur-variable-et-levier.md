# Module 3 — Épaisseur variable et levier

**Prérequis :** [module 2](02-les-trois-largeurs.md), [étape 8](../modele/08-test-de-tendance.md) (le modèle génératif).
**Ce qu'on établit ici :** les résidus n'ont pas tous la même variance ; il existe **trois** bandes distinctes, dont deux ne sont pas parallèles à la droite.

> ⚠️ Ce module quitte le terrain déterministe. Tout ce qui suit suppose le modèle
> de l'[étape 8](../modele/08-test-de-tendance.md) :
> $V_i = v_0 + rT_i + \varepsilon_i$ avec $\varepsilon_i$ i.i.d. $\mathcal N(0,\sigma^2)$.
> Les modules 1 et 2 étaient, eux, purement algébriques.

---

## 3.1 — Le levier

À chaque instant $t$ on associe le **levier**

$$h(t) \;=\; \frac1n + \frac{\bigl(t-E(T)\bigr)^2}{n\operatorname{Var}(T)}
\qquad\overset{T_i=i}{=}\qquad \frac1n + \frac{3\,(2t-n-1)^2}{n\,(n^2-1)} .$$

On retrouve le facteur $(2t-n-1)$ de l'[étape 7](../modele/07-droite-ajustee.md) :
c'est la même coordonnée centrée qui gouverne la droite et son incertitude.

Deux propriétés, immédiates depuis la formule :

- $h$ est **minimal au centre** de la fenêtre, où il vaut $1/n$, et croît comme
  le carré de la distance au centre.
- $\sum_i h(i) = 2$, soit une moyenne de $2/n$ — le nombre de paramètres estimés
  divisé par le nombre de points. C'est général : la somme des leviers vaut
  toujours le nombre de paramètres.

**Au dernier point de la fenêtre**, celui qui nous intéresse le plus puisque
c'est la séance courante :

$$h(n) = \frac1n + \frac{3(n-1)}{n(n+1)} = \boxed{\;\frac{4n-2}{n(n+1)}\;}$$

À $n=20$ : $h(20) = 78/420 = 0{,}1857$, soit **1,86 fois le levier moyen**.

## 3.2 — Les résidus n'ont pas tous la même variance

C'est le résultat que le module 1 annonçait, et il surprend toujours :

$$\boxed{\;\operatorname{Var}(\hat e_i) = \sigma^2\bigl(1 - h(i)\bigr)\;}$$

Les erreurs $\varepsilon_i$ sont, elles, homoscédastiques par hypothèse. Ce sont
les **résidus** qui ne le sont pas : aux extrémités, la droite est tirée vers le
point, qui laisse donc un résidu artificiellement petit.

Un point extrême de fenêtre est ainsi doublement piégeux : il influence le plus
la droite, et il apparaît le mieux ajusté. À $n=20$, l'écart-type d'un résidu de
bord vaut $\sqrt{1-0{,}1857} = 0{,}902$ fois celui du bruit, contre $0{,}975$ au
centre.

**Le résidu studentisé** corrige ce biais et rend les points comparables :

$$\hat e_i^{\,*} = \frac{\hat e_i}{s\sqrt{1-h(i)}}$$

C'est lui, et non $\hat e_i$, qu'il faut comparer à $2$ pour juger d'une sortie.
Sans cette correction, on sous-détecte systématiquement les anomalies de bord —
c'est-à-dire les plus récentes.

## 3.3 — Trois bandes, trois questions

Voici le cœur du cours. Le même dessin peut porter trois bandes de largeurs très
différentes, selon ce qu'on cherche à encadrer.

### a. Bande de dispersion

$$f(t) \;\pm\; k\,s$$

**Largeur constante**, bords parallèles à la droite. C'est le canal du
[module 2](02-les-trois-largeurs.md#22--lécart-type). Il décrit la
dispersion observée. C'est le seul des trois qui soit un « canal » au sens
graphique usuel.

### b. Bande de confiance

$$f(t) \;\pm\; t_{n-2;\,1-\alpha/2}\;s\,\sqrt{h(t)}$$

Elle encadre non pas les points, mais l'**espérance** $v_0 + rt$, dont $f$ n'est
qu'une estimation. Elle est **beaucoup plus étroite** que la précédente et a la
forme d'un **sablier** : resserrée au centre, évasée aux extrémités.

Le rapport entre ses demi-largeurs aux bords et au centre vaut

$$\sqrt{\frac{h(n)}{1/n}} = \sqrt{\frac{4n-2}{n+1}} \;\xrightarrow[n\to\infty]{}\; 2 .$$

> 🔑 **La droite ajustée est presque exactement deux fois moins bien déterminée à
> ses extrémités qu'en son milieu** — $1{,}93$ fois à $n=20$, et la limite est $2$
> quelle que soit la longueur de fenêtre. Or `VAL_n` est évaluée **au bord droit**.
> C'est le prix structurel de vouloir une valeur de tendance à la séance courante.

### c. Bande de prédiction

$$f(t) \;\pm\; t_{n-2;\,1-\alpha/2}\;s\,\sqrt{1 + h(t)}$$

Le $1$ supplémentaire est la variance du bruit de la nouvelle observation, qui
s'ajoute à l'incertitude sur la droite. C'est la bande **la plus large des
trois** — au centre, $\sqrt{1+1/n}\approx 1$ contre $\sqrt{1/n}$, soit un facteur
$\sqrt n$.

Sa forme est un sablier lui aussi, mais très aplati : $\sqrt{1+h}$ varie peu
quand $h$ passe de $0{,}05$ à $0{,}19$.

### Récapitulatif

| Bande | Demi-largeur | Forme | Encadre |
|---|---|---|---|
| Dispersion | $k\,s$ | parallèle | les points **observés** |
| Confiance | $t_{n-2}\,s\sqrt{h(t)}$ | sablier marqué | la **vraie droite** |
| Prédiction | $t_{n-2}\,s\sqrt{1+h(t)}$ | sablier aplati | la **prochaine observation** |

À $n=20$ et $\alpha=5\,\%$, au dernier point de la fenêtre :

| Bande | Demi-largeur en unités de $s$ |
|---|---|
| Confiance | $2{,}101 \times 0{,}431 = 0{,}906$ |
| Dispersion ($k=2$) | $2{,}000$ |
| Prédiction | $2{,}101 \times 1{,}089 = 2{,}288$ |

**Un facteur 2,5 entre la plus étroite et la plus large.** Présenter une bande de
confiance en la nommant « canal » revient à afficher une précision deux fois et
demie supérieure à la réalité de ce qu'on peut anticiper.

## 3.4 — Laquelle tracer

- Pour **décrire** la fenêtre passée et juger si un écart est grand : bande de
  **dispersion**. C'est le canal du chartiste.
- Pour dire si la **tendance** elle-même est établie : bande de **confiance**,
  ou plus directement l'intervalle de confiance sur la pente de l'[étape 8](../modele/08-test-de-tendance.md).
- Pour dire ce que vaudra la **prochaine séance** : bande de **prédiction**, et
  elle est le plus souvent si large qu'elle décourage l'exercice. C'est une
  information, pas un échec du calcul.

---

⬅️ [Module 2 — Les trois largeurs](02-les-trois-largeurs.md) ·
➡️ [Module 4 — Sorties de canal](04-sorties-de-canal.md)
