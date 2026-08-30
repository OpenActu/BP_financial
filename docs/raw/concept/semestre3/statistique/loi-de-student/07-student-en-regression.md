# Module 7 — Student en régression ⭐

**Durée : 4 h.** C'est ici que le cours rejoint [`modele.md`](../../../../modele.md). Ce module fournit
exactement ce qui manque à ce document : un **critère de décision**.

---

## 7.1 Le point de départ : ce que `modele.md` établit, et ce qu'il n'établit pas

Le document `modele.md` démontre, sur $n$ couples $(T_i,V_i)$ et **sans aucun modèle
probabiliste**, que le couple minimisant la variance du résidu est

$$r_{\min}=\frac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)},
\qquad v_{0}=E(V)-r_{\min}E(T),$$

avec la variance résiduelle minimale

$$\operatorname{Var}(\beta)_{\min}=\operatorname{Var}(V)\bigl(1-\rho^2\bigr).$$

Ce sont des **identités algébriques**, vraies sur n'importe quels $n$ points. Elles ne peuvent
donc pas répondre à la question de décision :

> $r_{\min}=+0{,}098$. Est-ce une **tendance réelle**, ou le hasard d'échantillonnage produit-il
> couramment de telles pentes sur des données sans tendance ?

Même sans aucune tendance, $r_{\min}$ ne vaut **jamais** exactement 0. Il faut donc connaître sa
loi — ce qui suppose un modèle génératif.

---

## 7.2 Le modèle statistique

> ⚠️ **Hypothèses nouvelles**, non requises par `modele.md` :
> $$V_i = v_0 + r\,T_i + \varepsilon_i, \qquad
> \varepsilon_i \overset{\text{i.i.d.}}{\sim}\mathcal N(0,\sigma^2), \qquad
> T_i \text{ déterministes}, \qquad n\ge 3 .$$
> Soit : **indépendance**, **homoscédasticité**, **normalité**.

**Changement de statut.** $v_0$, $r$ et $\sigma^2$ deviennent des **paramètres inconnus mais
fixes** ; $v_{0,\min}$, $r_{\min}$ et la variance résiduelle deviennent leurs **estimateurs**.
Ce qui était une description devient une inférence.

### Hypothèses du test

Elles portent sur le **paramètre** $r$, jamais sur la statistique $\rho$ — laquelle, calculée sur
un échantillon fini, ne vaut de toute façon jamais exactement 0 :

- $H_0 : r = 0$ — le niveau de la série ne dépend pas du temps ; toute pente observée n'est que
  fluctuation d'échantillonnage.
- $H_1 : r \ne 0$ — bilatérale, le sens de la tendance n'étant pas préjugé.

> **Remarque (acquis de `modele.md`).** L'équivalence
> $$\rho=0 \iff \operatorname{Cov}(V,T)=0 \iff r_{\min}=0$$
> est **déterministe** : elle découle de $r_{\min}=\operatorname{Cov}(V,T)/\operatorname{Var}(T)$
> et de $\operatorname{Var}(T)>0$. Tester la nullité de la pente ou celle de la corrélation, c'est
> donc le **même test** — ce qui autorise à construire la statistique sur $\rho$ tout en énonçant
> les hypothèses sur $r$.

---

## 7.3 D'où viennent les $n-2$ degrés de liberté

C'est la question à traiter en premier, et [Fisher–Cochran](../../../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md)
y répond déjà.

Les deux équations normales imposent au vecteur des résidus $\hat e$ **deux** contraintes
linéaires :

$$\sum_{i=1}^n \hat e_i = 0 \qquad\text{(constante)} \qquad\qquad
\sum_{i=1}^n t_i\,\hat e_i = 0 \qquad\text{(pente)},$$

où $t_i=T_i-E(T)$. Le vecteur $\hat e$ vit donc dans l'orthogonal du plan
$\text{Vect}(\mathbf 1,\,t)$, sous-espace de dimension $n-2$.

Par le [lemme de projection](../../../semestre2/statistique/mathematique/11-invariance-par-rotation-et-lemme-de-projection.md) (§ 11.3) :

$$\frac{1}{\sigma^2}\sum_{i=1}^n \hat e_i^{\,2}\;\sim\;\chi^2(n-2)
\qquad\text{et}\qquad
\hat r \;\perp\!\!\!\perp\; \sum_i \hat e_i^{\,2}$$

> 🔑 **Le « $n-2$ » n'est pas une règle à mémoriser** : c'est $n$ moins la dimension du
> sous-espace sur lequel on a projeté. Avec $p$ paramètres, ce serait $n-p$. C'est exactement la
> même géométrie que dans Fisher–Cochran, avec une direction de plus.

---

## 7.4 La statistique de test

### Estimateur de la variance résiduelle

⚠️ Attention au changement de normalisation entre `modele.md` (diviseur $n$) et l'inférence
(diviseur $n-2$) :

$$\hat\sigma^2=\frac{1}{n-2}\sum_{i=1}^n \hat e_i^{\,2}
=\frac{n}{n-2}\,\operatorname{Var}(\beta)_{\min}
=\frac{n}{n-2}\,\operatorname{Var}(V)\bigl(1-\rho^2\bigr)$$

Le facteur $\frac{n}{n-2}$ est le **débiaisage** : sans lui, $\hat\sigma^2$ sous-estimerait
$\sigma^2$, exactement comme au [§ 15.4 du cours de statistique](../../../semestre2/statistique/mathematique/15-loi-du-chi2.md).

### Erreur type de la pente

$$\operatorname{Var}(\hat r)=\frac{\sigma^2}{\sum_i t_i^2}=\frac{\sigma^2}{n\operatorname{Var}(T)}
\qquad\Longrightarrow\qquad
\boxed{\;\operatorname{SE}(\hat r)=\sqrt{\frac{\operatorname{Var}(V)\bigl(1-\rho^2\bigr)}{(n-2)\operatorname{Var}(T)}}\;}$$

et, dans le cas $T_i=i$ traité par `modele.md` (où $\operatorname{Var}(T)=\frac{n^2-1}{12}$) :

$$\operatorname{SE}(\hat r)=\sqrt{\frac{12\,\operatorname{Var}(V)\bigl(1-\rho^2\bigr)}{(n-2)\,(n^2-1)}}$$

> 🔑 **Lire cette formule est instructif en soi.** Le dénominateur contient $n^2-1$ : la précision
> de la pente s'améliore en $n^{-3/2}$, bien plus vite que celle d'une moyenne ($n^{-1/2}$).
> Allonger la fenêtre d'observation est **très** rentable pour estimer une tendance — à condition
> que le modèle reste valable sur toute la fenêtre, ce qui est une tout autre affaire.

### Le théorème

> Sous $H_0$, la statistique
> $$\boxed{\;t=\frac{\hat r}{\operatorname{SE}(\hat r)}=\rho\sqrt{\frac{n-2}{1-\rho^{2}}}\;}$$
> suit **exactement** une loi de Student à $n-2$ degrés de liberté.

**Démonstration de l'égalité des deux écritures** — un calcul de trois lignes qu'il faut avoir
fait une fois :

$$\frac{\hat r}{\operatorname{SE}(\hat r)}
=\frac{\operatorname{Cov}(V,T)/\operatorname{Var}(T)}
{\sqrt{\dfrac{\operatorname{Var}(V)(1-\rho^2)}{(n-2)\operatorname{Var}(T)}}}
=\operatorname{Cov}(V,T)\sqrt{\frac{n-2}{\operatorname{Var}(T)\operatorname{Var}(V)(1-\rho^2)}}
=\rho\sqrt{\frac{n-2}{1-\rho^2}}$$

**Pourquoi c'est bien une Student** — les trois conditions du module 4 sont réunies :
- $\dfrac{\hat r - r}{\sigma/\sqrt{n\operatorname{Var}(T)}}\sim\mathcal N(0,1)$ ($\hat r$ est une
  combinaison linéaire de gaussiennes) ;
- $\dfrac{(n-2)\hat\sigma^2}{\sigma^2}\sim\chi^2(n-2)$ (§ 7.3) ;
- les deux sont **indépendants** (§ 7.3).

> ⚠️ **La statistique est une Student, pas une normale.** La noter $z$ conduirait à chercher
> $1{,}96$ dans une table normale ; à $n=11$ le quantile correct est $t_{9;\,0{,}975}=2{,}262$.

---

## 7.5 Le lien avec Fisher et l'ANOVA

De façon équivalente,
$$t^2=\frac{(n-2)\,\rho^2}{1-\rho^2}\;\sim\;\mathcal F(1,\,n-2).$$

Cette écriture révèle ce que la statistique **est** :

$$t^{2}=(n-2)\,\frac{\text{variance expliquée}}{\text{variance résiduelle}}$$

c'est-à-dire le $R^2$ de `modele.md`, mis à l'échelle pour être comparable à une loi tabulée.
La statistique n'est pas un objet nouveau : c'est la décomposition de variance, corrigée des
degrés de liberté consommés.

**Tableau d'analyse de la variance** (sommes de carrés non normalisées, $\text{SC}=n\times\text{Var}$) :

| Source | Somme des carrés | ddl | Carré moyen | $F$ |
|---|---|---|---|---|
| Expliquée (régression) | $\text{SCE}=n\,r_{\min}^2\operatorname{Var}(T)$ | $1$ | $\text{SCE}/1$ | $\dfrac{\text{SCE}}{\hat\sigma^2}$ |
| Résiduelle | $\text{SCR}=n\operatorname{Var}(\beta)_{\min}$ | $n-2$ | $\hat\sigma^2=\text{SCR}/(n-2)$ | |
| **Totale** | $\text{SCT}=n\operatorname{Var}(V)$ | $n-1$ | | |

> 🔑 **Un test de Student bilatéral est un test de Fisher à 1 degré de liberté au numérateur.**
> Cette identité est la porte d'entrée vers l'ANOVA et la régression multiple, où le test $F$
> permet de tester **plusieurs** coefficients à la fois — ce qu'un $t$ ne sait pas faire.

---

## 7.6 Ce qu'il faut publier : les intervalles

### Intervalle de confiance de la pente

$$\text{IC}_{1-\alpha}(r)=r_{\min}\;\pm\;t_{n-2;\,1-\alpha/2}\cdot\operatorname{SE}(r_{\min})$$

**À préférer systématiquement au seul verdict binaire.** Il donne l'**ampleur** de la tendance et
sa **précision** — c'est-à-dire ce sur quoi une décision se prend. Un non-rejet de $H_0$ n'est
**pas** une preuve d'absence de tendance : c'est le constat que l'échantillon ne permet pas de la
distinguer du bruit.

### Intervalle de confiance de la droite, et intervalle de prédiction

En un point $t_0$, avec $S_{tt}=\sum_i t_i^2=n\operatorname{Var}(T)$ :

$$\text{IC de la moyenne : } f(t_0)\pm t_{n-2;\,1-\alpha/2}\;\hat\sigma
\sqrt{\frac{1}{n}+\frac{\bigl(t_0-E(T)\bigr)^2}{S_{tt}}}$$

$$\text{Intervalle de PRÉDICTION : } f(t_0)\pm t_{n-2;\,1-\alpha/2}\;\hat\sigma
\sqrt{1+\frac{1}{n}+\frac{\bigl(t_0-E(T)\bigr)^2}{S_{tt}}}$$

> ⚠️ **Le « 1 + » n'est pas un détail : c'est toute la différence.** Le premier intervalle
> encadre la **position de la droite** ; le second encadre une **observation future**, qui porte
> en plus son propre aléa $\varepsilon$. Le second est toujours nettement plus large, et il ne se
> resserre **pas** vers 0 quand $n\to\infty$ — il tend vers $\pm t\hat\sigma$. Confondre les deux
> conduit à annoncer des prévisions bien plus précises qu'elles ne le sont.

Les deux intervalles sont **d'autant plus larges qu'on s'éloigne de $E(T)$** : la droite pivote
autour du point moyen. Extrapoler loin de la fenêtre observée est donc doublement risqué — par
l'élargissement mécanique de l'intervalle, et parce que rien ne garantit que le modèle linéaire
vaille encore.

---

## 7.7 Diagnostics : levier et influence

Sur petit échantillon, une seule observation peut porter la conclusion. Deux outils le détectent.

**Levier** — position du point sur l'axe des $T$, indépendante de $V$ :
$$h_{ii}=\frac{1}{n}+\frac{\bigl(T_i-E(T)\bigr)^2}{S_{tt}},
\qquad \sum_i h_{ii}=2, \qquad \text{seuil d'alerte : } h_{ii}>\frac{2p}{n}=\frac{4}{n}$$

Le levier est **maximal aux extrémités de la fenêtre** — ce qui, pour une série chronologique,
signifie : **la première et la dernière observation pèsent le plus lourd**.

**Distance de Cook** — influence effective, qui combine levier et résidu :
$$D_i=\frac{\hat e_i^{\,2}\,h_{ii}}{p\,\hat\sigma^2\,(1-h_{ii})^2}\quad (p=2)$$

Un $D_i$ nettement supérieur aux autres signale un point dont le retrait déplacerait sensiblement
la droite.

---

## 7.8 Exemple travaillé complet

Reprenons la série de 11 points utilisée dans les notes de `modele.md`, avec $T_i=i$ :

$$V=\{9{,}9;\;10{,}2;\;11{,}0;\;10{,}5;\;10{,}4;\;11{,}2;\;10{,}9;\;11{,}1;\;10{,}5;\;11{,}1;\;11{,}3\}$$

### a) Moments et estimateurs

| Grandeur | Exact | ≈ |
|---|---|---|
| $E(T)=\frac{n+1}{2}$ | $6$ | 6 |
| $\operatorname{Var}(T)=\frac{n^2-1}{12}$ | $10$ | 10 |
| $E(V)$ | $\frac{1181}{110}$ | 10,736364 |
| $\operatorname{Var}(V)$ | $\frac{579}{3025}$ | 0,191405 |
| $\operatorname{Cov}(V,T)$ | $\frac{54}{55}$ | 0,981818 |
| $r_{\min}$ | $\frac{27}{275}$ | **0,098182** |
| $v_{0,\min}$ | $\frac{5581}{550}$ | **10,147273** |
| $\operatorname{Var}(\beta)_{\min}$ | $\frac{1437}{15125}$ | 0,095008 |
| $\rho^2$ | $\frac{486}{965}$ | 0,503627 |
| $\rho$ | — | **+0,709667** |

Droite ajustée : $f(t)=10{,}147273+0{,}098182\,t$.

### b) Table d'analyse de la variance

| Source | SC | ddl | CM | $F$ |
|---|---|---|---|---|
| Expliquée | 1,060364 | 1 | 1,060364 | **9,1315** |
| Résiduelle | 1,045091 | 9 | $\hat\sigma^2=0{,}116121$ | |
| **Totale** | 2,105455 | 10 | | |

$\hat\sigma=0{,}340766$ ; $R^2=50{,}4\,\%$.

### c) Le test

$$\operatorname{SE}(r_{\min})=\sqrt{\frac{12\times0{,}191405\times0{,}496373}{9\times120}}=0{,}032491$$

$$t=\frac{0{,}098182}{0{,}032491}=\rho\sqrt{\frac{9}{1-\rho^2}}=\mathbf{3{,}0218}$$

| Élément | Valeur |
|---|---|
| Loi sous $H_0$ | $\mathcal T(9)$ |
| Valeur critique bilatérale à 5 % | $2{,}2622$ |
| **Décision** | $3{,}0218 > 2{,}2622$ → **rejet de $H_0$** |
| $p$-valeur | $0{,}0144$ |
| Contrôle par $F$ | $t^2=9{,}1315 > F_{0{,}95}(1,9)=5{,}117$ ✓ |
| $\text{IC}_{95\%}(r)$ | $[\,0{,}0247\;;\;0{,}1717\,]$ |

### d) Prédiction en $t_0=12$

$$f(12)=11{,}3255$$

| Intervalle | Borne basse | Borne haute | Demi-largeur |
|---|---|---|---|
| IC de la **droite** | 10,827 | 11,824 | ±0,499 |
| Intervalle de **prédiction** | 10,407 | 12,243 | ±0,918 |

L'intervalle de prédiction est **presque deux fois plus large**. C'est lui qu'il faut annoncer si
la question est « quelle sera la prochaine valeur ? ».

### e) Levier et influence

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $\hat e_i$ | −0,346 | −0,144 | +0,558 | −0,040 | −0,238 | +0,464 | +0,065 | +0,167 | −0,531 | −0,029 | +0,073 |
| $h_{ii}$ | **0,318** | 0,236 | 0,173 | 0,127 | 0,100 | 0,091 | 0,100 | 0,127 | 0,173 | 0,236 | **0,318** |
| $D_i$ (Cook) | **0,352** | 0,036 | 0,339 | 0,001 | 0,030 | 0,102 | 0,002 | 0,020 | 0,306 | 0,002 | 0,016 |

Les leviers sont maximaux en $i=1$ et $i=11$ (0,318, contre un seuil d'alerte à $4/11=0{,}364$),
et **la distance de Cook est maximale en $i=1$**.

### f) Analyse de sensibilité — le résultat décisif

Régression refaite en retirant chaque point tour à tour :

| Point retiré | $r_{\min}$ | $R^2$ | $t$ | $p$ | Décision à 5 % |
|---|---|---|---|---|---|
| **$i=1$ ($V=9{,}9$)** | 0,0752 | 0,349 | **2,070** | **0,0722** | ❌ **non significatif** |
| $i=2$ | 0,0913 | 0,431 | 2,461 | 0,0392 | ✅ |
| $i=3$ | 0,1166 | 0,671 | 4,035 | 0,0038 | ✅ |
| $i=4$ | 0,0973 | 0,490 | 2,770 | 0,0243 | ✅ |
| $i=5$ | 0,0958 | 0,504 | 2,853 | 0,0214 | ✅ |
| $i=6$ | 0,0982 | 0,567 | 3,239 | 0,0119 | ✅ |
| $i=7$ | 0,0975 | 0,499 | 2,822 | 0,0224 | ✅ |
| $i=8$ | 0,0947 | 0,483 | 2,735 | 0,0257 | ✅ |
| $i=9$ | 0,1157 | 0,655 | 3,901 | 0,0045 | ✅ |
| $i=10$ | 0,0996 | 0,467 | 2,649 | 0,0293 | ✅ |
| $i=11$ | 0,0933 | 0,409 | 2,354 | 0,0464 | ✅ |

⚠️ **Le retrait de la première observation suffit à faire basculer la conclusion** ($p$ passe de
0,014 à 0,072). Le diagnostic de Cook l'avait annoncé. Le verdict « série tendancielle » est
**exact au vu des 11 points**, mais **fragile** : il ne survivrait pas à la découverte que la
première mesure est erronée.

### g) Diagnostics complémentaires

| Contrôle | Valeur | Lecture |
|---|---|---|
| Durbin–Watson | 2,240 | Pas d'autocorrélation positive ($\hat\rho_1=-0{,}180$) — l'hypothèse critique est **satisfaite** |
| Mann–Kendall (non paramétrique) | $S=31$, $z=2{,}350$, $p=0{,}0188$ | **Même conclusion**, sans hypothèse de normalité |
| Pente de Sen (robuste) | 0,1143 | Cohérente avec $r_{\min}=0{,}0982$ |

La convergence des trois approches est le véritable argument. Si Student rejetait et que
Mann–Kendall ne rejetait pas, on saurait que le résultat tient à la normalité plutôt qu'aux
données.

### h) Conclusion rédigée

> La série est **tendanciellement croissante** au seuil de 5 % ($t=3{,}02$, $p=0{,}014$,
> $R^2=50{,}4\,\%$), avec une pente estimée de **$+0{,}098$ par période** — soit environ
> $+0{,}91\,\%$ du niveau moyen.
>
> **Trois réserves.** ① L'IC va de 0,025 à 0,172, un **facteur 7** entre les bornes : on peut
> affirmer *qu'il y a* une hausse, pas *de combien*. ② La conclusion **tient à une seule
> observation** (§ f). ③ Le rejet dit que le modèle « niveau constant + bruit i.i.d. » explique
> mal ces données ; il ne dit **pas** que la tendance est linéaire, ni qu'elle se poursuivra. La
> série pourrait décrire un palier vers 10,5 suivi d'un second vers 11,1 — avec 11 points, on ne
> départage pas les deux modèles.

---

## 7.9 Simulations

```python
import numpy as np, math
from scipy import stats

V = np.array([9.9, 10.2, 11.0, 10.5, 10.4, 11.2, 10.9, 11.1, 10.5, 11.1, 11.3])
n = len(V); T = np.arange(1, n + 1)

# --- à la main, selon modele.md (moments normalisés par n) ---
ET, EV = T.mean(), V.mean()
VarT, VarV = T.var(), V.var()                    # ddof=0 : convention modele.md
Cov = ((T - ET) * (V - EV)).mean()
r, v0 = Cov / VarT, EV - Cov / VarT * ET
rho2 = Cov**2 / (VarV * VarT)
SE = math.sqrt(VarV * (1 - rho2) / ((n - 2) * VarT))
t = r / SE
print(f"r={r:.6f}  v0={v0:.6f}  R2={rho2:.6f}")
print(f"SE={SE:.6f}  t={t:.4f}  p={2*stats.t.sf(abs(t), n-2):.4f}")
tc = stats.t.ppf(0.975, n - 2)
print(f"IC(r) = [{r - tc*SE:.4f}, {r + tc*SE:.4f}]")

# --- contrôle par la bibliothèque ---
lr = stats.linregress(T, V)
print(f"contrôle : pente={lr.slope:.6f}  SE={lr.stderr:.6f}  p={lr.pvalue:.4f}")

# --- levier et Cook ---
e = V - (v0 + r * T); s2 = (e**2).sum() / (n - 2); Stt = ((T - ET)**2).sum()
h = 1/n + (T - ET)**2 / Stt
D = e**2 * h / (2 * s2 * (1 - h)**2)
for i in range(n):
    print(f"i={i+1:2d}  e={e[i]:+.3f}  h={h[i]:.3f}  Cook={D[i]:.3f}")

# --- sensibilité : retrait d'un point ---
for k in range(n):
    m = np.arange(n) != k
    lrk = stats.linregress(T[m], V[m])
    flag = "OK " if lrk.pvalue < .05 else "NON"
    print(f"sans i={k+1:2d} : pente={lrk.slope:.4f}  p={lrk.pvalue:.4f}  {flag}")
```

**S7.1 — Vérifier la loi sous $H_0$.** Simuler 200 000 séries sans tendance
($V_i=\varepsilon_i$), calculer $t$ à chaque fois, et vérifier par Kolmogorov–Smirnov
l'ajustement à $\mathcal T(n-2)$. Contrôler que le taux de rejet vaut bien 5 %.

**S7.2 — Courbe de puissance.** Pour $n\in\{10,20,50\}$ et diverses pentes réelles $r$,
estimer la probabilité de rejet. Constater que la puissance croît **très vite** avec $n$ —
conséquence du $n^2-1$ au dénominateur de $\operatorname{SE}(\hat r)$.

**S7.3 — La couverture des deux intervalles.** Vérifier que l'IC de la droite couvre $f(t_0)$
dans 95 % des cas et l'intervalle de prédiction couvre une **observation nouvelle** dans 95 %
des cas. Vérifier aussi que l'IC de la droite **ne couvre pas** l'observation nouvelle à 95 % —
c'est l'erreur que le « 1 + » du § 7.6 prévient.

---

## 7.10 Exercices

**E7.1.** Démontrer $\operatorname{Var}(\hat r)=\frac{\sigma^2}{\sum_i t_i^2}$ en écrivant
$\hat r$ comme combinaison linéaire des $V_i$ : $\hat r=\sum_i c_i V_i$ avec
$c_i=\frac{t_i}{\sum_j t_j^2}$.

**E7.2.** Vérifier algébriquement l'égalité des deux écritures de $t$ (§ 7.4) sans passer par les
valeurs numériques.

**E7.3.** Montrer que $t^2=\frac{\text{SCE}/1}{\text{SCR}/(n-2)}$, c'est-à-dire que la
statistique $F$ du tableau d'ANOVA **est** le carré de la statistique de Student.

**E7.4.** Pourquoi $\sum_i h_{ii}=2$ ? Généraliser à une régression à $p$ paramètres.
*(Réponse : la trace de la matrice de projection vaut la dimension du sous-espace projeté.)*

**E7.5.** Reprendre l'exemple du § 7.8 en ajoutant une 12ᵉ observation $V_{12}=11{,}5$.
Recalculer $t$, $p$ et l'IC. La conclusion se renforce-t-elle ? De combien l'IC se resserre-t-il ?

**E7.6 — orientée finance.** Sur un cours de clôture du SBF 250 (via `import_societe.py`),
appliquer ce test de tendance sur des fenêtres de 20, 60 et 250 séances. Combien de fenêtres sont
« significatives » à 5 % ?

> ⚠️ **Ne concluez rien de cet exercice avant d'avoir lu le module 8.** Un cours de bourse est
> proche d'une **marche aléatoire**, et le test y rejette à tort dans la grande majorité des cas.
> E7.6 est un piège délibéré : il est là pour que vous constatiez le phénomène avant qu'on ne
> vous l'explique.

---

## 7.11 À retenir

- $t=\dfrac{\hat r}{\operatorname{SE}(\hat r)}=\rho\sqrt{\dfrac{n-2}{1-\rho^2}}\sim\mathcal T(n-2)$
  sous $H_0:r=0$.
- Le **$n-2$** vient de deux contraintes linéaires sur les résidus — même géométrie que dans
  Fisher–Cochran.
- $t^2\sim\mathcal F(1,n-2)$ : un test de Student bilatéral **est** un test de Fisher.
- **Publier l'IC de la pente**, pas seulement la $p$-valeur ; distinguer IC de la droite et
  intervalle de **prédiction**.
- Sur petit échantillon, **contrôler levier et distance de Cook** : les points extrêmes de la
  fenêtre pèsent le plus.
- Ce test suppose des résidus **indépendants**. Sur une série chronologique, c'est l'hypothèse
  qui casse — module 8.

---

⬅️ [Module 6 — Comparaison de deux moyennes](06-comparaison-de-deux-moyennes.md) ·
➡️ [Module 8 — Robustesse et limites](08-robustesse-et-limites.md) ·
🏠 [Sommaire](README.md)
