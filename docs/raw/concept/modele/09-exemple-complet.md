# Étape 9 — Exemple complet d'évaluation

**Prérequis :** [étapes 1 à 8](../../modele.md#plan-de-la-preuve).
**Ce qu'on établit ici :** rien de nouveau — les huit étapes précédentes, exécutées sur une série de $11$ points, contrôles croisés et diagnostics compris.

---

Série observée, avec $T_i = i$ pour $i=1,\dots,11$ (donc $n=11$, cas de l'[étape 6](06-instants-regulierement-espaces.md)) :

$$V=\{9{,}9;\;10{,}2;\;11{,}0;\;10{,}5;\;10{,}4;\;11{,}2;\;10{,}9;\;11{,}1;\;10{,}5;\;11{,}1;\;11{,}3\}$$

## 9.1 — Moments empiriques

| Grandeur                                 | Valeur exacte      | Valeur approchée |
| ---------------------------------------- | ------------------ | ---------------- |
| $E(T)=\frac{n+1}{2}$                     | $6$                | $6$              |
| $\operatorname{Var}(T)=\frac{n^2-1}{12}$ | $10$               | $10$             |
| $E(V)$                                   | $\frac{1181}{110}$ | $10{,}736364$    |
| $\operatorname{Var}(V)$                  | $\frac{579}{3025}$ | $0{,}191405$     |
| $\sigma_V$                               | —                  | $0{,}437499$     |
| $\operatorname{Cov}(V,T)$                | $\frac{54}{55}$    | $0{,}981818$     |

## 9.2 — [Étape 4](04-forme-canonique.md) : pente, ordonnée, variance résiduelle

$$r_{\min}=\frac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)}=\frac{54/55}{10}=\frac{27}{275}\approx 0{,}098182$$
$$v_{0,\min}=E(V)-r_{\min}E(T)=\frac{1181}{110}-6\cdot\frac{27}{275}=\frac{5581}{550}\approx 10{,}147273$$
$$\operatorname{Var}(\hat e)_{\min}=\operatorname{Var}(V)-\frac{\operatorname{Cov}(V,T)^2}{\operatorname{Var}(T)}=0{,}191405-0{,}096397=\frac{1437}{15125}\approx 0{,}095008$$

## 9.3 — [Étape 5](05-coefficient-de-correlation.md) : corrélation et décomposition

$$\rho_{V,T}^{2}=\frac{0{,}096397}{0{,}191405}=\frac{486}{965}\approx 0{,}503627 \qquad\Longrightarrow\qquad \rho_{V,T}\approx +0{,}709667$$

*Contrôle par la voie de l'étape 5 :*
$\operatorname{Var}(V)\bigl(1-\rho^2\bigr)=0{,}191405\times0{,}496373=0{,}095008$ ✓

$$\underbrace{0{,}191405}_{\text{totale}} \;=\; \underbrace{r_{\min}^{2}\operatorname{Var}(T)=0{,}096397}_{\text{expliquée},\;R^2=50{,}4\,\%} \;+\; \underbrace{0{,}095008}_{\text{résiduelle}}$$

La tendance explique à peine la moitié de la dispersion ; l'autre moitié reste du bruit.

## 9.4 — [Étape 6](06-instants-regulierement-espaces.md) : forme en $\phi(V)$

$$\phi(V)=\rho_{V,T}\sqrt{\frac{3\operatorname{Var}(V)}{n^2-1}} = 0{,}709667\times\sqrt{\frac{3\times0{,}191405}{120}} = 0{,}709667\times 0{,}069175 \approx 0{,}049091=\tfrac{27}{550}$$

*Contrôles croisés :* $r_{\min}=2\phi=0{,}098182$ ✓ et $v_{0,\min}=E(V)-\phi\,(n+1)=10{,}736364-12\times0{,}049091=10{,}147273$ ✓

## 9.5 — [Étape 7](07-droite-ajustee.md) : droite ajustée et résidus

$$f(t)=10{,}147273+0{,}098182\,t \;=\; 10{,}736364+0{,}049091\,(2t-12)$$

| $i$        | 1      | 2      | 3          | 4      | 5      | 6      | 7      | 8      | 9          | 10     | 11     |
| ---------- | ------ | ------ | ---------- | ------ | ------ | ------ | ------ | ------ | ---------- | ------ | ------ |
| $V_i$      | 9,90   | 10,20  | 11,00      | 10,50  | 10,40  | 11,20  | 10,90  | 11,10  | 10,50      | 11,10  | 11,30  |
| $f(i)$     | 10,25  | 10,34  | 10,44      | 10,54  | 10,64  | 10,74  | 10,83  | 10,93  | 11,03      | 11,13  | 11,23  |
| $\hat e_i$ | −0,346 | −0,144 | **+0,558** | −0,040 | −0,238 | +0,464 | +0,065 | +0,167 | **−0,531** | −0,029 | +0,073 |

*Contrôles :* $\sum_i \hat e_i = 0$ exactement ([étape 1](01-elimination-de-l-ordonnee.md)) ✓ et $\frac1{11}\sum_i \hat e_i^{\,2} = 0{,}095008$ ✓

## 9.6 — [Étape 8](08-test-de-tendance.md) : le test

$$t = \rho_{V,T}\sqrt{\frac{n-2}{1-\rho_{V,T}^{2}}} = 0{,}709667\times\sqrt{\frac{9}{0{,}496373}} = 0{,}709667\times 4{,}258085 = \mathbf{3{,}0218}$$

| Élément                          | Valeur                                      |
| -------------------------------- | ------------------------------------------- |
| Loi sous $H_0$                   | Student à $n-2=9$ ddl                       |
| Valeur critique bilatérale à 5 % | $t_{9;\,0{,}975}=2{,}2622$                  |
| **Décision**                     | $3{,}0218 > 2{,}2622$ → **rejet de $H_0$**  |
| $p$-valeur bilatérale            | $0{,}0144$                                  |
| Forme $F$                        | $t^{2}=9{,}131 > F_{0{,}95}(1,9)=5{,}117$ ✓ |

**Intervalle de confiance sur la pente** — la partie qui compte :

$$\operatorname{SE}(r_{\min})=\sqrt{\frac{12\times0{,}191405\times0{,}496373}{9\times120}}=0{,}032491$$
$$\text{IC}_{95\%}(r) = 0{,}098182 \pm 2{,}2622\times0{,}032491 = [\,0{,}0247\;;\;0{,}1717\,]$$

## 9.7 — Diagnostics

| Contrôle | Valeur | Lecture |
|---|---|---|
| Durbin–Watson | $2{,}240$ | Pas d'autocorrélation positive ($\hat\rho_1=-0{,}180$) — l'hypothèse critique de l'étape 8 est **satisfaite** |
| Mann–Kendall (non paramétrique) | $S=31$, $z=2{,}350$, $p=0{,}0188$ | **Même conclusion**, sans hypothèse de normalité |
| Pente de Sen (robuste) | $0{,}1143$ | Cohérente avec $r_{\min}=0{,}0982$ |

La convergence des trois approches est le véritable argument : si Student rejetait et que Mann–Kendall ne rejetait pas, on saurait que le résultat tient à la normalité plutôt qu'aux données.

## 9.8 — Analyse de sensibilité (retrait d'un point)

Avec $n=11$, il est indispensable de vérifier qu'aucune observation ne porte à elle seule la conclusion. Régression refaite en retirant chaque point tour à tour :

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

⚠️  **Résultat central de cette section.** Le retrait de la **première observation suffit à faire basculer la conclusion** ($p$ passe de $0{,}014$ à $0{,}072$). C'est le point de plus fort **effet de levier** — extrémité de la fenêtre — et c'est aussi la valeur la plus basse de la série. Deux autres retraits ($i=2$, $i=11$) laissent $p$ juste sous $0{,}05$.

Le verdict « série tendancielle » est donc **exact au vu des 11 points**, mais **fragile** : il ne survivrait pas à la découverte que la première mesure est entachée d'erreur.

## 9.9 — Conclusion et réserves

**Conclusion.** La série est **tendanciellement croissante** au seuil de 5 % ($t=3{,}02$, $p=0{,}014$, $R^2=50{,}4\,\%$). La pente estimée est de **$+0{,}098$ par période**, soit environ **$+0{,}91\,\%$ par période** rapporté au niveau moyen de $10{,}74$. Sur les $10$ intervalles observés, cela représente une progression totale de $\approx +0{,}98$, du même ordre que l'amplitude de la série elle-même ($9{,}9 \to 11{,}3$).

**Réserve 1 — la pente est mal déterminée.** L'IC va de $0{,}025$ à $0{,}172$ : un **facteur 7** entre les deux bornes, soit entre $+0{,}23\,\%$ et $+1{,}60\,\%$ par période. On peut affirmer *qu'il y a* une hausse ; on ne peut pas dire *de combien*. C'est le prix de $n=11$, et c'est exactement pourquoi l'IC vaut mieux que le seul $p=0{,}014$, qui donnerait l'illusion d'un résultat net.

**Réserve 2 — la conclusion tient à une observation.** Voir § 9.8 : sans le point $i=1$, le test ne rejette plus. À reconfirmer sur données supplémentaires avant d'en tirer une décision.

**Réserve 3 — ce qu'on ne peut pas conclure.** Le rejet dit que le modèle « niveau constant + bruit i.i.d. » explique mal ces données. Il ne dit **pas** que la tendance est *linéaire*, ni qu'elle se poursuivra. La série pourrait tout aussi bien décrire un palier vers $10{,}5$ suivi d'un second vers $11{,}1$ : avec 11 points, on ne départage pas les deux modèles.

---

⬅️ [Étape 8 — Position du problème et statistique de test](08-test-de-tendance.md) ·
🏠 [Sommaire](../../modele.md)
