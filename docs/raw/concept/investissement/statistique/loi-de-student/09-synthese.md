# Module 9 — Synthèse et arbre de décision

**Durée : 2 h.** Ce module ne contient rien de nouveau : il rassemble. Il est conçu pour être
**la seule page à rouvrir** une fois le cours terminé.

---

## 9.1 Arbre de décision — quel test pour quelle question

**Étape préalable, avant toute chose :**

```
Les observations sont-elles indépendantes ?
│
├── NON (série chronologique, mesures répétées, grappes)
│   │
│   ├── Racine unitaire ? (ADF + KPSS)
│   │   ├── OUI  → travailler en DIFFÉRENCES ; ne pas tester la tendance sur les niveaux
│   │   └── NON  → écarts-types HAC (Newey-West), ou modèle AR explicite
│   │
│   └── ⚠️ Ne JAMAIS appliquer directement les tests ci-dessous
│
└── OUI → poursuivre
    │
    ├── Question : une moyenne vaut-elle une valeur de référence ?
    │   → test t à UNE population,  ddl = n-1                      [module 5]
    │
    ├── Question : deux moyennes diffèrent-elles ?
    │   │
    │   ├── Les données sont-elles APPARIÉES ?
    │   │   (l'observation i du groupe A correspond-elle
    │   │    à l'observation i du groupe B ?)
    │   │
    │   ├── OUI → test t APPARIÉ sur les différences, ddl = n-1    [module 6 §6.2]
    │   │         ⚠️ ignorer un appariement réel détruit la puissance
    │   │
    │   └── NON → test de WELCH par défaut, ddl = Satterthwaite    [module 6 §6.4]
    │             (ne pas pré-tester l'égalité des variances)
    │
    └── Question : une variable dépend-elle linéairement d'une autre ?
        → test t sur la pente,  ddl = n-2                          [module 7]
          puis : levier, distance de Cook, résidus
```

---

## 9.2 Formulaire

### Loi de Student

| | |
|---|---|
| Définition | $T=\dfrac{Z}{\sqrt{K/\nu}}$, $Z\sim\mathcal N(0,1)$, $K\sim\chi^2(\nu)$, **indépendantes** |
| Espérance | $0$ si $\nu>1$ |
| Variance | $\dfrac{\nu}{\nu-2}$ si $\nu>2$ |
| Moments | d'ordre $k$ définis **ssi** $k<\nu$ |
| Limite | $\mathcal T(\nu)\to\mathcal N(0,1)$ |

### Fisher–Cochran

$$\bar X\sim\mathcal N\!\left(\mu,\tfrac{\sigma^2}{n}\right)
\qquad \frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)
\qquad \bar X\perp\!\!\!\perp S^2$$

### Une moyenne

$$t=\frac{\bar x-\mu_0}{s/\sqrt n}\sim\mathcal T(n-1)
\qquad
\text{IC}=\bar x\pm t_{n-1;\,1-\alpha/2}\frac{s}{\sqrt n}$$

### Deux moyennes, appariées

$$t=\frac{\bar d-\delta_0}{s_d/\sqrt n}\sim\mathcal T(n-1)$$

### Deux moyennes, indépendantes — Welch

$$t=\frac{\bar x_1-\bar x_2}{\sqrt{\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}}}
\qquad
\nu=\frac{\left(\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}\right)^{2}}
{\frac{(s_1^2/n_1)^2}{n_1-1}+\frac{(s_2^2/n_2)^2}{n_2-1}}$$

### Deux moyennes, indépendantes — poolé (à effectifs équilibrés seulement)

$$s_p^2=\frac{(n_1-1)s_1^2+(n_2-1)s_2^2}{n_1+n_2-2}
\qquad
t=\frac{\bar x_1-\bar x_2}{s_p\sqrt{\frac1{n_1}+\frac1{n_2}}}\sim\mathcal T(n_1+n_2-2)$$

### Régression simple

$$r_{\min}=\frac{\operatorname{Cov}(V,T)}{\operatorname{Var}(T)}
\qquad
\hat\sigma^2=\frac{n}{n-2}\operatorname{Var}(V)(1-\rho^2)$$

$$\operatorname{SE}(\hat r)=\sqrt{\frac{\operatorname{Var}(V)(1-\rho^2)}{(n-2)\operatorname{Var}(T)}}
\qquad
t=\frac{\hat r}{\operatorname{SE}(\hat r)}=\rho\sqrt{\frac{n-2}{1-\rho^2}}\sim\mathcal T(n-2)$$

$$t^2\sim\mathcal F(1,n-2)
\qquad
\text{cas } T_i=i:\;\operatorname{SE}(\hat r)=\sqrt{\frac{12\operatorname{Var}(V)(1-\rho^2)}{(n-2)(n^2-1)}}$$

### Prédiction en $t_0$ ($S_{tt}=n\operatorname{Var}(T)$)

$$\text{droite : } \hat\sigma\sqrt{\frac1n+\frac{(t_0-E(T))^2}{S_{tt}}}
\qquad
\text{prédiction : } \hat\sigma\sqrt{1+\frac1n+\frac{(t_0-E(T))^2}{S_{tt}}}$$

### Diagnostics

$$h_{ii}=\frac1n+\frac{(T_i-E(T))^2}{S_{tt}}\;\;(\textstyle\sum_i h_{ii}=p)
\qquad
D_i=\frac{\hat e_i^{\,2}h_{ii}}{p\,\hat\sigma^2(1-h_{ii})^2}$$

### Dimensionnement

$$n\approx\frac{(z_{1-\alpha/2}+z_{1-\beta})^2}{d^2}
\qquad d=\frac{|\mu-\mu_0|}{\sigma}
\qquad (\alpha=5\,\%,\ 1-\beta=80\,\%\;\Rightarrow\;n\approx 7{,}85/d^2)$$

---

## 9.3 Table des quantiles $t_{\nu;\,p}$

| $\nu$ | 0,900 | 0,950 | 0,975 | 0,990 | 0,995 |
|---|---|---|---|---|---|
| 1 | 3,078 | 6,314 | 12,706 | 31,821 | 63,657 |
| 2 | 1,886 | 2,920 | 4,303 | 6,965 | 9,925 |
| 3 | 1,638 | 2,353 | 3,182 | 4,541 | 5,841 |
| 4 | 1,533 | 2,132 | 2,776 | 3,747 | 4,604 |
| 5 | 1,476 | 2,015 | 2,571 | 3,365 | 4,032 |
| 6 | 1,440 | 1,943 | 2,447 | 3,143 | 3,707 |
| 7 | 1,415 | 1,895 | 2,365 | 2,998 | 3,499 |
| 8 | 1,397 | 1,860 | 2,306 | 2,896 | 3,355 |
| 9 | 1,383 | 1,833 | 2,262 | 2,821 | 3,250 |
| 10 | 1,372 | 1,812 | 2,228 | 2,764 | 3,169 |
| 11 | 1,363 | 1,796 | 2,201 | 2,718 | 3,106 |
| 12 | 1,356 | 1,782 | 2,179 | 2,681 | 3,055 |
| 13 | 1,350 | 1,771 | 2,160 | 2,650 | 3,012 |
| 14 | 1,345 | 1,761 | 2,145 | 2,624 | 2,977 |
| 15 | 1,341 | 1,753 | 2,131 | 2,602 | 2,947 |
| 16 | 1,337 | 1,746 | 2,120 | 2,583 | 2,921 |
| 17 | 1,333 | 1,740 | 2,110 | 2,567 | 2,898 |
| 18 | 1,330 | 1,734 | 2,101 | 2,552 | 2,878 |
| 19 | 1,328 | 1,729 | 2,093 | 2,539 | 2,861 |
| 20 | 1,325 | 1,725 | 2,086 | 2,528 | 2,845 |
| 22 | 1,321 | 1,717 | 2,074 | 2,508 | 2,819 |
| 24 | 1,318 | 1,711 | 2,064 | 2,492 | 2,797 |
| 26 | 1,315 | 1,706 | 2,056 | 2,479 | 2,779 |
| 28 | 1,313 | 1,701 | 2,048 | 2,467 | 2,763 |
| 30 | 1,310 | 1,697 | 2,042 | 2,457 | 2,750 |
| 40 | 1,303 | 1,684 | 2,021 | 2,423 | 2,704 |
| 50 | 1,299 | 1,676 | 2,009 | 2,403 | 2,678 |
| 60 | 1,296 | 1,671 | 2,000 | 2,390 | 2,660 |
| 80 | 1,292 | 1,664 | 1,990 | 2,374 | 2,639 |
| 100 | 1,290 | 1,660 | 1,984 | 2,364 | 2,626 |
| 120 | 1,289 | 1,658 | 1,980 | 2,358 | 2,617 |
| $\infty$ | 1,282 | 1,645 | **1,960** | 2,326 | 2,576 |

*Test bilatéral au risque $\alpha$ → colonne $1-\alpha/2$. Test unilatéral au risque $\alpha$ →
colonne $1-\alpha$.*

> En pratique : `scipy.stats.t.ppf(p, nu)` ou, en R, `qt(p, nu)`. Cette table est là pour l'ordre
> de grandeur et le contrôle mental, pas pour le calcul.

---

## 9.4 Les dix pièges

| # | Piège | Correction |
|---|---|---|
| 1 | Employer $1{,}96$ au lieu de $t_{\nu;\,0{,}975}$ | Le risque réel monte à 12 % pour $n=5$ (module 1) |
| 2 | Confondre $z$ et $t$ dans la rédaction | Le nom oriente vers la mauvaise table |
| 3 | Se tromper de degrés de liberté | $\nu = n$ − nombre de paramètres estimés |
| 4 | « 95 % de chances que $\mu$ soit dedans » | C'est **l'intervalle** qui est aléatoire, pas $\mu$ |
| 5 | Lire la $p$-valeur comme $P(H_0)$ | C'est $P(\text{données}\mid H_0)$, en sens inverse |
| 6 | Conclure à l'absence d'effet sur un non-rejet | Sans puissance, un non-rejet ne dit rien |
| 7 | Confondre significativité et ampleur | Publier l'**IC**, pas la seule $p$-valeur |
| 8 | Ignorer un appariement | Détruit la puissance (module 6, § 6.2) |
| 9 | Pré-tester variances ou normalité | Invalide le niveau du test final |
| 10 | **Ignorer l'autocorrélation** | Le plus coûteux : 5 % annoncés, 73 % réels (module 8) |

---

## 9.5 Les six phrases à retenir du cours entier

1. **Student est la loi normale corrigée du fait qu'on a dû estimer le dénominateur.**
2. **Les degrés de liberté sont une dimension géométrique** : $n$ moins le nombre de contraintes
   imposées aux résidus par l'estimation.
3. **L'indépendance de $\bar X$ et $S^2$ est propre à la gaussienne** — c'est le seul endroit où
   la normalité est réellement indispensable.
4. **L'hypothèse critique n'est pas la normalité, c'est l'indépendance** — et sa violation
   s'aggrave quand $n$ augmente, au lieu de s'effacer.
5. **Un intervalle de confiance vaut mieux qu'une $p$-valeur** : il porte le verdict, l'ampleur
   et la précision.
6. **Toujours tracer les données** avant de tester quoi que ce soit.

---

## 9.6 Auto-évaluation finale

Vous maîtrisez le cours si vous savez répondre, sans notes :

**Théorie**
1. Pourquoi la loi de Student existe-t-elle ? (une phrase)
2. D'où viennent les $n-1$ degrés de liberté ? Donner l'argument **géométrique**.
3. Pourquoi $\bar X\perp\!\!\!\perp S^2$ ? Où la normalité intervient-elle exactement ?
4. Pourquoi $\operatorname{Var}(\mathcal T(\nu))>1$ ?
5. Pourquoi $\mathcal T(1)$ n'a-t-elle pas d'espérance, et quelle conséquence pratique ?

**Pratique**
6. Deux échantillons de tailles 8 et 40, variances très différentes : quel test ? Pourquoi ?
7. Données avant/après sur les mêmes sujets : quel test, et que coûte l'erreur inverse ?
8. Un test de tendance sur 60 mois donne $p=0{,}003$. Quelles trois vérifications avant de
   conclure ?
9. Un IC à 95 % de la pente vaut $[-0{,}01\;;\;+0{,}42]$. Que peut-on affirmer ? Que ne peut-on
   pas ?
10. Pourquoi ne faut-il pas tester la normalité avant de choisir son test ?

**Le test décisif**

> Un collègue vous montre une régression du chiffre d'affaires mensuel sur le temps, sur 36 mois,
> avec $R^2=0{,}72$ et $p<0{,}001$. Il en conclut à une croissance solide et l'extrapole sur trois
> ans.
>
> **Citez au moins quatre objections.**

*Éléments de réponse* : ① les résidus sont-ils autocorrélés (Durbin–Watson) ? ② la série est-elle
stationnaire ou à racine unitaire (ADF/KPSS) — un $R^2$ élevé sur une série de niveau est
suspect, module 8 ; ③ la saisonnalité est-elle traitée, et la fenêtre couvre-t-elle un nombre
entier de cycles (36 mois : oui, bon point) ; ④ l'extrapolation sur 36 mois hors fenêtre est-elle
légitime, et publie-t-il un intervalle de **prédiction** (module 7, § 7.6) ; ⑤ levier et Cook :
quelques mois portent-ils la pente ; ⑥ combien de spécifications a-t-il essayées avant celle-ci
(module 8, § 8.8) ; ⑦ le modèle linéaire est-il le bon, ou observe-t-on des paliers ?

---

## 9.7 Pour aller plus loin

| Direction | Contenu | Référence |
|---|---|---|
| **Régression multiple** | Plusieurs prédicteurs, tests $F$ partiels, colinéarité | Faraway, *Linear Models with R* |
| **Modèle linéaire général** | ANOVA, ANCOVA, plans d'expérience — même géométrie, $n-p$ ddl | Saporta, ch. 17–18 |
| **Séries chronologiques** | ARIMA, cointégration, tests de racine unitaire | Hamilton, *Time Series Analysis* |
| **Méthodes robustes** | Bootstrap, permutation, M-estimateurs | Efron & Tibshirani, *An Introduction to the Bootstrap* |
| **Approche bayésienne** | La loi de Student comme *a posteriori* d'une moyenne à variance inconnue — elle réapparaît, mais avec une interprétation où « 95 % de chances que $\mu$ soit dedans » devient enfin **correcte** | Gelman et al., *Bayesian Data Analysis* |

> 🔑 Cette dernière ligne mérite un mot. Dans le cadre bayésien, avec un *a priori* non informatif
> sur $(\mu,\sigma^2)$, la loi a posteriori de $\mu$ **est** une loi de Student à $n-1$ degrés de
> liberté centrée sur $\bar x$. L'intervalle numérique obtenu est **identique** à l'IC
> fréquentiste — mais son interprétation change du tout au tout : l'intervalle de crédibilité
> bayésien porte bien une probabilité sur $\mu$. Le piège n° 4 du § 9.4 vient précisément de ce
> que l'intuition des gens est bayésienne alors que la formule qu'on leur enseigne ne l'est pas.

---

## 9.8 Retour au point de départ

Le cours a commencé par une question posée sur [`modele.md`](../../modele/modele.md) :

> La tendance $r_{\min}$ que je viens de calculer est-elle réelle ?

La réponse tient maintenant en une procédure :

1. Tracer la série. Regarder.
2. Vérifier la stationnarité (ADF + KPSS). Si racine unitaire → différencier.
3. Calculer $r_{\min}$, $\rho$, $\hat\sigma$ selon `modele.md` et le module 7.
4. Calculer $t=\rho\sqrt{\frac{n-2}{1-\rho^2}}$ et le comparer à $t_{n-2;\,0{,}975}$.
5. Contrôler les résidus : Durbin–Watson, levier, Cook.
6. **Publier l'intervalle de confiance de la pente**, pas la seule $p$-valeur.
7. Énoncer ce qu'on ne peut pas conclure.

L'étape 7 n'est pas une précaution oratoire. C'est elle qui distingue un résultat statistique
d'une affirmation.

---

⬅️ [Module 8 — Robustesse et limites](08-robustesse-et-limites.md) ·
🏠 [Sommaire](README.md)
