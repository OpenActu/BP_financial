# Cours — Finance : levier, couverture, portefeuille optimal

Cours dédié aux **trois décisions** qu'un investisseur prend une fois qu'il sait lire une série de
cours : *quelle taille de position ?*, *faut-il se protéger ?*, *quels titres et en quelle
proportion ?* Niveau **bac+2**, entièrement chiffré, et posé dans le cadre réel du marché
parisien — **SRD, vente à découvert restreinte, PEA sans levier**.

## Pourquoi ce cours dans ce dépôt

Les cours existants du dépôt démontrent des outils ; celui-ci les **dépense**. Il ne contient qu'un
seul théorème nouveau (le levier optimal, module 4) : tous les autres résultats sont des
applications d'énoncés déjà prouvés ailleurs dans le dépôt.

| Ce que le cours utilise | D'où cela vient | Où c'est dépensé |
|---|---|---|
| $r_{\min}=\operatorname{Cov}/\operatorname{Var}$ et $\operatorname{Var}(V)(1-\rho^2)$ | [`modele.md`](../../../modele.md), étapes 4–5 | **Module 6** : c'est le ratio de couverture, mot pour mot |
| La forme canonique $\varphi(r)=\operatorname{Var}(T)(r-r_{\min})^2+\operatorname{Var}_{\min}$ | [`modele.md`](../../semestre3/modele/04-forme-canonique.md) | **Module 6** : la pénalité exacte d'une couverture mal dimensionnée |
| $\operatorname{SE}$ de la pente, loi de Student | [Student § 7](../../semestre3/statistique/loi-de-student/07-student-en-regression.md) | **Module 6** : l'intervalle de confiance sur $\beta$ |
| Jensen, $E[\log X]\le\log E[X]$ | [Convexité § 5](../../semestre1/analyse/convexite/05-jensen-probabiliste.md) | **Module 4** : le drag de volatilité |
| $w^{\top}\Sigma w$ convexe, $\Sigma$ matrice de Gram | [Convexité § 7](../../semestre1/analyse/convexite/07-convexite-en-dimension-n.md), [Algèbre § 11](../../semestre1/algebre/11-covariance-et-produit-scalaire.md) | **Module 8** : Markowitz est un problème convexe |
| Projection orthogonale et Pythagore | [Algèbre § 6](../../semestre1/algebre/06-projection-orthogonale.md) | **Module 6** : couvrir, c'est projeter |
| Loi normale, premier passage, queues épaisses | [Statistique § 6f](../../semestre2/statistique/mathematique/06f-loi-normale.md), [§ 13](../../semestre2/statistique/mathematique/13-portee-et-limites-du-tcl.md) | **Module 3** : probabilité d'appel de marge |
| Corrélations en régime de crise | [Statistique § 14](../../semestre2/statistique/mathematique/14-dependance-et-echec-du-tcl.md) | **Modules 3 et 9** : la diversification qui s'évapore |

> 🔑 **La question qui organise tout le cours.** Dans chacun des trois sujets, **le gain est
> linéaire et le coût quadratique** — ou l'inverse. Levier : prime $\propto L$, drag
> $\propto L^2$. Couverture : portage $\propto h$, erreur $\propto (h-h^\star)^2$. Portefeuille :
> rendement $\propto w$, variance $\propto w^{\top}\Sigma w$. **Un optimum intérieur existe donc
> toujours, et il n'est jamais au bout du chemin.**

## Fil directeur

Trois questions, une même structure de réponse :

- **Quelle taille ?** $L^\star=\dfrac{\mu-c}{\sigma^2}$, à prendre **de moitié** — modules 2 à 4.
- **Quelle protection ?** $h^\star=\dfrac{\operatorname{Cov}(V,M)}{\operatorname{Var}(M)}$, et il
  survit $1-\rho^2$ de variance — modules 5 à 7.
- **Quels titres ?** $w\propto\Sigma^{-1}(\mu-r_f\mathbf1)$… sauf que $\mu$ n'est pas
  connaissable — modules 8 et 9.

Et une contrainte transversale : **le cadre parisien**. Le SRD plafonne le levier à $1/m$, la VAD
est restreinte et suspensible, le PEA interdit les trois. Chaque module démontre le résultat
général **puis** le corrige de ces frottements.

## Progression

### Partie 0 — Le terrain

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 1 | [Le cadre : CAC 40, SRD, vente à découvert](01-le-cadre-cac40-et-le-srd.md) | 1 h | Couverture 20/25/40 %, coût de portage $c$, ce que le PEA interdit |

### Partie I — Le levier

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 2 | [L'effet de levier](02-l-effet-de-levier.md) | 1 h | $R_L=LR-(L-1)c$ ; le Sharpe est invariant ; le levier dérive tout seul |
| 3 | [**Marge, appel de marge et ruine**](03-marge-appel-de-marge-et-ruine.md) ⭐ | 1 h 30 | $x^\star=\frac{1/L-m}{1-m}$ ; l'espérance ment, la médiane s'effondre ; **le stop est la même barrière, choisie** |
| 4 | [**Levier optimal et drag de volatilité**](04-levier-optimal-et-drag.md) ⭐ | 1 h 15 | $L^\star=\frac{\mu-c}{\sigma^2}$, le demi-Kelly, et pourquoi $L^\star<1$ au SRD |

### Partie II — La couverture

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 5 | [La vente à découvert](05-la-vente-a-decouvert.md) | 1 h | Seuil de rentabilité $-k$ ; espérance nue négative ; le squeeze est mécanique |
| 6 | [**La couverture optimale**](06-la-couverture-optimale.md) ⭐ | 1 h 15 | $h^\star=\beta$, efficacité $\rho^2$ — `modele.md` appliqué tel quel |
| 7 | [Couvrir en pratique](07-couvrir-en-pratique.md) | 1 h 30 | Future, VAD, put, ETF inverse, **ordre stop** : cinq instruments, cinq défauts |

### Partie III — Le portefeuille

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 8 | [**Le portefeuille optimal**](08-le-portefeuille-optimal.md) ⭐ | 1 h 30 | $w_{\text{mv}}$, $w_{\text{tan}}$, séparation en deux fonds, coût de $w\ge0$ |
| 9 | [**Contraintes réelles et estimation**](09-contraintes-reelles-et-estimation.md) ⭐ | 1 h 15 | Le plancher $\sigma\sqrt{\bar\rho}$ ; $1/N$ bat Markowitz 4 fois sur 5 |

### Partie IV — Le cas complet

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 10 | [**Un portefeuille complet, chiffré**](10-exemple-de-portefeuille.md) ⭐ | 1 h 30 | 60 000 €, 10 valeurs : les neuf modules exécutés, tous les nombres publiés |

**Volume total** : ≈ 12 h 45, à répartir sur 3 à 4 semaines. Les modules se lisent **dans
l'ordre** : chacun n'utilise que les précédents, et le module 6 exige d'avoir lu
[`modele.md`](../../../modele.md).

## Parcours

| Objectif | Modules |
|---|---|
| Savoir si je peux utiliser le SRD | 1 → 2 → 3 |
| Choisir une taille de position | 2 → 3 → 4 |
| Protéger un portefeuille existant | 6 → 7 (puis 5 si VAD envisagée) |
| Construire un portefeuille de zéro | 8 → 9 → 4 |
| Le minimum vital, en 3 h | 3 → 4 → 6 |
| Lire ce cours depuis un PEA | 1 → 4 → 8 → 9, puis § 7.5 |
| **Voir à quoi tout cela sert** | **10 seul**, puis remonter aux modules qu'il cite |
| Dimensionner sur une série réelle | § 3.5 → § 4.5, puis [`dimensionner_exposition.py`](../../../../../python/dimensionner_exposition.md) |
| Poser un stop, et savoir ce qu'il coûte | § 3.5 → § 7.6, puis le [module 7 du cours trading](../trading/07-le-stop-une-sortie-sans-verdict.md) |

## Les six modules décisifs

- **Module 3 — L'appel de marge.** Celui qui montre que le risque du levier n'est pas dans les
  formules du module 2 : il est dans la **barrière**, qui rend le résultat dépendant du chemin et
  liquide plus d'une position sur deux **à tort**. Le § 3.5 montre qu'un **stop-loss** est la même
  barrière, posée volontairement, et qu'elle se paie de 1 à 4 points d'espérance par an.
- **Module 4 — Le levier optimal.** Celui qui explique pourquoi l'espérance monte pendant que la
  médiane s'effondre, et pourquoi, avec un portage à 5 %, le levier optimal sur des actions
  parisiennes est **inférieur à 1**.
- **Module 6 — La couverture optimale.** Celui qui ne démontre rien : il **reconnaît** que le
  théorème de [`modele.md`](../../../modele.md) répond à une deuxième question, et que
  $\operatorname{Cov}/\operatorname{Var}$ est le ratio de couverture.
- **Module 8 — Markowitz.** Celui qui montre que l'optimum théorique **exige de vendre à
  découvert**, donc n'existe pas en PEA, et chiffre ce que l'interdiction coûte.
- **Module 9 — L'estimation.** Celui qui retire au module 8 la moitié de ce qu'il a promis, et
  explique pourquoi $1/N$ est si difficile à battre.
- **Module 10 — Le cas chiffré.** Celui qui exécute les neuf autres sur 60 000 € et dix valeurs du
  CAC 40, et arrive à une position très ordinaire — dix lignes équipondérées, aucun levier, aucune
  couverture — en montrant **pourquoi** c'est l'optimum ici, et à quelles conditions précises il
  cesse de l'être.

## Ce que ce cours ne contient pas

- **La valorisation** : pas de modèle de dividendes actualisés, pas d'analyse de bilan, pas de
  multiples. Le cours prend $\mu$ et $\Sigma$ comme des entrées, et le module 9 explique
  précisément à quel point cette prise est fragile.
- **Le *pricing* d'options** : Black–Scholes n'apparaît qu'au [§ 7.4](07-couvrir-en-pratique.md),
  comme **tarif** d'une couverture, sans démonstration. Ni grecques, ni volatilité implicite, ni
  couverture dynamique.
- **La fiscalité** : elle est mentionnée là où elle change une décision (PEA contre CTO), jamais
  chiffrée.
- **Le *market timing*, l'analyse technique, les stratégies de facteurs.**
- **La théorie de l'utilité** : le cours utilise deux critères explicites — variance et croissance
  logarithmique — sans les dériver d'une fonction d'utilité générale.

## Ce que les autres cours du dépôt apportent à celui-ci

| Cours | Ce qu'il fournit |
|---|---|
| [`modele.md`](../../../modele.md) | **Le module 6 en entier** : ratio de couverture, variance résiduelle, pénalité quadratique |
| [Algèbre linéaire](../../semestre1/algebre/README.md) | Le produit scalaire, la projection (couvrir = projeter), $\Sigma$ matrice de Gram |
| [Convexité](../../semestre1/analyse/convexite/README.md) | Jensen (drag de volatilité), minimisation convexe, convexité de $w^{\top}\Sigma w$ |
| [Dérivation et intégration](../../semestre1/analyse/derivation-et-integration/README.md) | Le calcul matriciel des dérivées, derrière les formules de Markowitz |
| [Statistique mathématique](../../semestre2/statistique/mathematique/README.md) | Loi normale, corrélation, queues, échec du TCL en dépendance |
| [Loi de Student](../../semestre3/statistique/loi-de-student/README.md) | L'incertitude sur $\beta$ et sur $\mu$ — le cœur des modules 4 et 9 |

## Outillage

```bash
pip install numpy matplotlib yfinance
```

Les simulations n'utilisent que `numpy` (la fonction de répartition normale est écrite à la main
avec `math.erf`) ; `yfinance` sert uniquement au module 1, pour alimenter le cours avec vos
propres données via [`import_societe.py`](../../../../../python/import_societe.py).

**Tous les tableaux numériques de ce cours ont été produits par le code qui les accompagne.**

## Notations retenues dans tout le cours

| Symbole | Sens |
|---|---|
| $L$, $L^\star$ | Levier, levier optimal ($=$ exposition / fonds propres) |
| $c$ | Coût de portage annuel total (CRD + report + spread) |
| $m$ | Taux de couverture exigé (20 %, 25 %, 40 % selon le collatéral) |
| $x^\star$ | Baisse déclenchant l'appel de marge |
| $g(L)$ | Taux de croissance logarithmique d'une position levée |
| $k$ | Coût de portage d'une vente à découvert, **dividende inclus** |
| $h$, $h^\star$ | Ratio de couverture, ratio de variance minimale ($=\beta$) |
| $\rho^2$ | Efficacité de couverture ; part de variance annulée |
| $w$, $\Sigma$, $\mu$, $r_f$ | Poids, covariance, rendements espérés, taux sans risque |
| $\bar\rho$ | Corrélation moyenne entre lignes d'un même marché |
| $N$ | Nombre de lignes, ou nombre de contrats à terme |

## Références

| Usage | Référence |
|---|---|
| Le portefeuille | Markowitz, « Portfolio Selection », *J. of Finance*, 1952 |
| La droite de marché | Sharpe, « Capital Asset Prices », *J. of Finance*, 1964 |
| Le levier optimal | Kelly, « A New Interpretation of Information Rate », 1956 ; Merton, « Lifetime Portfolio Selection », 1969 |
| Le demi-Kelly en pratique | Thorp, « The Kelly Criterion in Blackjack, Sports Betting and the Stock Market », 2006 |
| L'échec de l'optimisation estimée | DeMiguel, Garlappi & Uppal, « Optimal Versus Naive Diversification », *RFS*, 2009 |
| La contrainte comme shrinkage | Jagannathan & Ma, « Risk Reduction in Large Portfolios », *J. of Finance*, 2003 |
| Le shrinkage de $\Sigma$ | Ledoit & Wolf, « Honey, I Shrunk the Sample Covariance Matrix », *JPM*, 2004 |
| Futures et options | Hull, *Options, Futures and Other Derivatives* — ch. 3 (couverture) et 12 |
| Le cadre réglementaire | Euronext (spécifications SRD et contrats FCE), AMF (positions courtes nettes), règlement UE 236/2012 |

---

🏠 [Sommaire général](../../sommaire/README.md) ·
📄 [`modele.md`](../../../modele.md) ·
➡️ [Module 1 — Le cadre](01-le-cadre-cac40-et-le-srd.md)
