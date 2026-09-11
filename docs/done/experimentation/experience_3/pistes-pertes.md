# Les deux pertes les plus lourdes de 2022 — ce qu'elles permettent d'établir

> [Expérience 3](README.md) · analyse chartiste des positions `DSY.PA` et
> `KER.PA` du [bilan § 3](bilan-2022.md) · demandée après coup, donc **sous la
> contrainte de catégorie** rappelée au § 5.

> ⚠️ **Aucun conseil en investissement.** Ce document porte sur un protocole,
> jamais sur un titre à acheter ou à vendre. Les deux valeurs analysées sont des
> cas d'étude d'une règle. Aucun dimensionnement de position, aucune prédiction
> de cours.

---

## 0. Les deux cas, et la question posée

| Valeur | Achat | Sortie | Séances | Prix achat | Prix sortie | +/− value | Alpha | Contribution |
|---|---|---|---|---|---|---|---|---|
| `DSY.PA` Dassault Systèmes | 2022-01-03 | 2022-02-01 | 22 | 50,13 € | 41,05 € | −18,12 % | −16,43 pt | **−364,10 €** |
| `KER.PA` Kering | 2022-03-01 | 2022-06-01 | 65 | 558,25 € | 454,99 € | −18,50 % | −20,44 pt | **−318,30 €** |

Deux axes ont été demandés :

1. ne plus utiliser la fenêtre courte de 20 séances comme critère d'entrée ;
2. introduire un stop à l'achat, plafond de perte à 10 % pour commencer.

**Les deux sont réfutés par les chiffres du protocole lui-même, et pour des
raisons différentes.** Ce document donne d'abord les vérifications, puis trois
propositions dont une seule est de catégorie A.

Toute la simulation est reproduite à l'identique par un moteur autonome qui
réutilise les fonctions de [`journal.py`](journal.py) : mêmes 16 ordres, même
valeur finale **9 764,22 €**, même `TR39` à **89,82**. Sans cette vérification,
aucun contrefactuel ci-dessous n'aurait de sens. Le mode d'emploi est au § 6.

---

## 1. Ce qui a été vérifié avant toute proposition

### 1.1 `s2` valait **zéro** aux deux décisions d'achat

C'est le premier fait, et il commande la lecture de l'axe 1.

| Décision | Valeur | Rang | `s1` | `s2` | `s3` | `s4` | `s5` | Score | Position | τ |
|---|---|---|---|---|---|---|---|---|---|---|
| 2021-12-31 | `DSY.PA` | 5 | +2 | **0** | +1 | +2 | 0 | **+5** | 7,0 % | 210,5 |
| 2022-02-28 | `KER.PA` | 2 | +2 | **0** | +1 | +2 | 0 | **+5** | 19,3 % | ∞ |

> **Retirer `s2` ne change le score d'aucune des deux valeurs achetées.** Elles
> gardent +5. L'axe 1 ne peut donc agir que par le **réordonnancement des
> autres valeurs de l'univers** — un effet indirect, qui ne porte pas sur la
> qualité du signal des deux titres incriminés.

### 1.2 Ce que devient le classement des 12 dates narrées sans `s2`

Le [bilan § 5](bilan-2022.md) donne le poids effectif de `s2` : **3,1 %** de la
variance du score sur les 920 évaluations d'audit, contre 48,5 % pour `s1` et
40,1 % pour `s4`. On s'attendrait à un effet marginal. C'est faux.

**Panier achetable (rang ≤ 5, score > 0, aucun veto), 12 dates narrées :**

| Décision | Règle publiée | Sans `s2` | |
|---|---|---|---|
| 2021-12-31 | `CAP.PA`, `DSY.PA` | `DSY.PA`, `OR.PA` | change |
| 2022-01-31 | — | — | |
| 2022-02-28 | **`KER.PA`** | — | change |
| 2022-03-31 | `HO.PA`, `MT.AS` | `HO.PA` | change |
| 2022-04-29 | `MT.AS` | `MT.AS`, `TTE.PA` | change |
| 2022-05-31 | `HO.PA`, `TTE.PA` | `HO.PA`, `TTE.PA` | |
| 2022-06-30 | — | — | |
| 2022-07-29 | `HO.PA`, `BN.PA` | `HO.PA` | change |
| 2022-08-31 | `RMS.PA` | `RMS.PA` | |
| 2022-09-30 | — | — | |
| 2022-10-31 | — | — | |
| 2022-11-30 | `DG.PA` | — | change |

**6 dates sur 12 changent de panier.** Et sur la fenêtre d'**étalonnage** — les
12 fins de mois de 2020-12 à 2021-11, hors année investie, donc un chiffre qui ne
doit rien à 2022 — : **10 dates sur 12**.

> Une composante qui pèse 3,1 % de la variance du score fait basculer le panier
> d'entrée sur **10 dates sur 12**. Ce n'est pas un réglage fin, c'est un
> changement de règle.

**La raison est mécanique, et elle est plus intéressante que le contrefactuel.**
Le score est un entier de faible granularité, avec beaucoup d'*ex aequo*.
Retirer `s2` comprime encore l'échelle et multiplie les égalités, que le tri
départage alors au momentum. Au 2022-02-28 :

| | Valeurs à score +5 | Rang de `KER.PA` |
|---|---|---|
| Règle publiée | 3 | **2** — achetée |
| Sans `s2` | **14** | **12** — non achetée |

Les onze valeurs qui doublent `KER.PA` sont celles dont `s2 = −1` disparaît, qui
passent ainsi de +4 à +5 ; **elles sont toutes sous veto**, donc inachetables. Le
mois se solde par **zéro achat**, les espèces dorment, et la perte est évitée par
un embouteillage de rangs, non par un jugement porté sur `KER.PA`.

**Et sur `DSY.PA`, retirer `s2` ne change rien :** au 2021-12-31, `DSY.PA` passe
du rang 5 au **rang 2** et reste achetée. C'est `CAP.PA` (rang 4 → 7) qui sort du
panier, remplacée par `OR.PA`, laquelle a fait **−10,4 %** en janvier — plus mal
que `CAP.PA` (−5,93 % sur sa détention entière).

> **L'axe 1 n'évite qu'une des deux positions désignées, et par un mécanisme qui
> n'a rien à voir avec la qualité du signal de fenêtre courte.**

### 1.3 Les deux lectures de l'axe 1, et celle qui est retenue

L'axe a été formulé « ne plus utiliser `VAL_20`, uniquement `VAL_120` ». Trois
lectures sont possibles ; elles ne coïncident pas.

| Lecture | Ce qu'elle touche | Effet |
|---|---|---|
| **a. littérale — retirer `VAL_20`** | rien | `VAL_20` n'entre dans **aucun** calcul de la règle. `generer_graph_decision.py` lit `TEND_20` et `TEND_120`, jamais `VAL_n`. Effet **strictement nul** |
| **b. retirer `s2 = TEND_20` du score** | le score | 6/12 dates narrées, 10/12 dates d'étalonnage changent de panier |
| **c. retirer toute la fenêtre 20** | le score **et** le veto 3 | le veto 3 est *« critères 1 et 2 de signes opposés »* : il est entièrement défini par `TEND_20`. Il se déclenche sur **28,4 %** des 923 évaluations |

**Je retiens la lecture b**, et je la nomme dans la proposition. Motif : la
lecture a est vide — `VAL_20` est la droite ajustée évaluée au dernier point de
la fenêtre, un intermédiaire de diagnostic, jamais un critère ; la lecture c
n'est pas « retirer un critère », c'est retirer un critère **et** un veto, deux
changements dont les effets se compensent partiellement et qu'il faudrait alors
mesurer séparément.

Les trois contrefactuels 2022, pour mémoire (et sans valeur probante, § 5) :

| Variante | Valeur finale | Perf. | Alpha brut | Ordres | Frais | Part investie | β | α de Jensen |
|---|---|---|---|---|---|---|---|---|
| **Règle publiée** | 9 764,22 € | −2,36 % | +7,82 pt | 16 | 75,24 € | 45,3 % | 0,382 | +2,29 %/an |
| b. sans `s2` | 10 600,79 € | +6,01 % | +16,19 pt | 11 | 49,27 € | **35,7 %** | **0,219** | +8,61 %/an |
| c. sans `s2` ni veto 3 | 10 532,61 € | +5,33 % | +15,50 pt | 25 | 116,51 € | 59,9 % | 0,504 | +11,12 %/an |
| veto 3 seul retiré | 9 468,05 € | −5,32 % | +4,86 pt | 26 | 119,91 € | — | — | — |

> **Le « gain » de la lecture b est d'abord une sous-exposition.** La part
> investie tombe de 45,3 % à 35,7 %, le bêta de 0,382 à 0,219, et 43 séances se
> passent intégralement en espèces contre 0. Dans une année où `TR39` fait
> −10,18 %, être moins investi paie mécaniquement. L'alpha de régression, qui
> corrige cela, passe de +2,29 à +8,61 %/an, **avec un IC95 de ± 16,8 points :
> les deux sont indiscernables de zéro, et l'un de l'autre.**

### 1.4 Un stop aurait touché **cinq positions sur neuf**, pas deux

Le repli maximal de chaque position, entre l'achat et la sortie, mesuré sur la
clôture et sur le `Low` intraséance :

| Valeur | Issue | Repli max. en clôture | Repli max. sur `Low` |
|---|---|---|---|
| `CAP.PA` | −5,93 % | −22,79 % | −23,88 % |
| `DSY.PA` | **−18,12 %** | −21,04 % | −23,02 % |
| `KER.PA` | **−18,50 %** | −29,14 % | −30,69 % |
| `HO.PA` | **+9,29 %** | −1,73 % | −3,08 % |
| `MT.AS` | **+5,32 %** | −10,82 % | −14,09 % |
| `TTE.PA` | **+11,12 %** | −15,38 % | −15,89 % |
| `BN.PA` | −2,76 % | −2,69 % | −3,66 % |
| `RMS.PA` | **+21,73 %** | −8,12 % | −8,98 % |
| `DG.PA` | −3,88 % | −4,81 % | −5,34 % |

**Nombre de positions coupées selon le seuil**, déclenchement sur clôture :

| Seuil | Positions coupées | Dont gagnantes coupées |
|---|---|---|
| −5 % | 7 / 9 | `MT.AS`, `TTE.PA`, `RMS.PA` |
| **−10 %** | **5 / 9** | **`MT.AS`, `TTE.PA`** |
| −15 % | 4 / 9 | `TTE.PA` |
| −20 % | 3 / 9 | aucune |

Le détail du stop à −10 %, position par position, **avec ce que chacune a fait
après le niveau de déclenchement** :

| Valeur | Déclenchement | Exécution | Réalisé | Sans stop | Écart |
|---|---|---|---|---|---|
| `DSY.PA` | clôture 2022-01-10 | ouverture 2022-01-11 @ 45,67 € | −8,89 % | −18,12 % | **+9,23 pt** |
| `CAP.PA` | clôture 2022-01-24 | ouverture 2022-01-25 @ 173,76 € | −10,52 % | −5,93 % | −4,59 pt |
| `KER.PA` | clôture 2022-03-04 | ouverture 2022-03-07 @ 463,41 € | **−16,99 %** | −18,50 % | **+1,51 pt** |
| `MT.AS` | clôture 2022-05-09 | ouverture 2022-05-10 @ 24,32 € | −9,40 % | +5,32 % | −14,72 pt |
| `TTE.PA` | clôture 2022-06-17 | ouverture 2022-06-20 @ 38,78 € | −10,45 % | +11,12 % | **−21,57 pt** |

**Bilan : 2 positions sauvées pour +10,74 points, 3 coupées à tort pour
−40,88 points.** Un contre quatre.

### 1.5 Sur quelle grandeur, et à quel prix — le gap de `KER.PA`

C'est le point que l'axe 2 ne peut pas éluder.

`KER.PA` franchit le seuil de −10 % **en clôture** le 2022-03-04, à 491,01 €,
soit **−12,04 %**. L'ouverture de la séance suivante, le 2022-03-07, est à
**463,41 €**, soit **−16,99 %**. Le gap d'ouverture consomme **près de 5 points**,
et le stop « à −10 % » réalise −16,99 % : il n'économise que **1,51 point** sur
les −18,50 % de la sortie réelle.

Les deux conventions possibles, et ce qu'elles supposent :

| Convention | Grandeur observée | Prix d'exécution | Ce qu'elle suppose |
|---|---|---|---|
| **clôture** | `Close ≤ prix × 0,90` | ouverture de la séance suivante | un ordre passé le soir, exécuté au fixing d'ouverture — **subit le gap en entier** |
| **`Low` intraséance** | `Low ≤ prix × 0,90` | le seuil lui-même | un ordre stop-market posé au marché — **suppose qu'il n'y a pas de gap**, ce qui est faux précisément les jours où il se déclenche |

Sur `KER.PA`, la convention `Low` prétend sortir à 502,43 € alors que le `Low` du
jour est 490,22 € : l'exécution réelle serait quelque part entre les deux, jamais
au seuil. **L'hypothèse « exécution au seuil » est optimiste par construction**,
et je publie les deux jeux plutôt que de choisir le flatteur.

Contrefactuels 2022 complets, toutes conventions et tous seuils :

| Variante | Valeur finale | Perf. | Alpha brut | Ordres | Frais | Stops | Part investie |
|---|---|---|---|---|---|---|---|
| **Règle publiée** | **9 764,22 €** | **−2,36 %** | **+7,82 pt** | 16 | 75,24 € | — | 45,3 % |
| stop clôture −5 % | 9 078,10 € | −9,22 % | +0,96 pt | 19 | 79,95 € | 7 | — |
| **stop clôture −10 %** | **9 206,09 €** | **−7,94 %** | **+2,24 pt** | 17 | 75,59 € | 5 | 25,4 % |
| stop clôture −15 % | 9 236,04 € | −7,64 % | +2,54 pt | 17 | 75,56 € | 4 | — |
| stop clôture −20 % | 9 331,01 € | −6,69 % | +3,49 pt | 16 | 72,81 € | 3 | — |
| stop `Low` −5 % | 9 302,05 € | −6,98 % | +3,20 pt | 20 | 83,32 € | 8 | — |
| stop `Low` −10 % | 9 316,55 € | −6,83 % | +3,34 pt | 17 | 76,08 € | 5 | 24,7 % |
| stop `Low` −15 % | 9 188,48 € | −8,12 % | +2,06 pt | 17 | 75,20 € | 4 | — |
| stop `Low` −20 % | 9 413,75 € | −5,86 % | +4,32 pt | 16 | 73,45 € | 3 | — |

> **Aucun seuil, sous aucune convention, ne fait mieux que l'absence de stop.**
> Le meilleur (`Low` −20 %) coûte 3,50 points ; celui qui était demandé
> (clôture −10 %) en coûte **5,58**.

La quarantaine après stop — interdire le rachat pendant 1, 2 ou 12 mois — ne
change **rien** : aucune valeur stoppée n'est jamais revenue dans le panier
achetable en 2022. Le paramètre est sans effet sur cette fenêtre.

### 1.6 Le stop, jugé sur 884 observations et non sur 9

Neuf positions ne tranchent rien. Le protocole fournit un échantillon bien plus
large : les **24 dates d'audit × tout l'univers**, chacune tenue un mois, de
l'ouverture de la première séance du mois à l'ouverture de la première séance du
mois suivant — soit **884 détentions d'un mois**. Le rendement mensuel moyen y
vaut **+0,95 %**.

| Seuil | Déclenché | « Sauve » | Effet moyen par déclenchement |
|---|---|---|---|
| −5 % | 38,8 % ± 3,2 (343/884) | 48,1 % ± 5,3 | −0,64 pt ± 0,67 |
| **−10 %** | **15,4 % ± 2,4** (136/884) | **40,4 % ± 8,2** | **−1,68 pt ± 1,11** |
| −15 % | 5,0 % ± 1,4 (44/884) | 40,9 % ± 14,5 | −1,79 pt ± 2,11 |
| −20 % | 1,8 % ± 0,9 (16/884) | 25,0 % ± 21,2 | −5,54 pt ± 3,84 |

> « Sauve » = le prix obtenu au stop est supérieur au prix qu'aurait donné la
> sortie mensuelle prévue.

**Un stop à −10 % coupe à tort dans 59,6 % des cas, et son effet moyen par
déclenchement, −1,68 pt ± 1,11, exclut zéro.** C'est la mesure qui tranche, et
elle tranche contre l'axe 2 — avec la réserve d'autocorrélation rappelée au § 4.

Restreint aux seules détentions **achetables** (rang ≤ 5, score > 0, aucun veto),
l'échantillon tombe à 42 et l'incertitude explose : −10 % s'y déclenche 9,5 %
± 8,9 du temps. C'est trop peu pour conclure, et c'est pourquoi le chiffre
d'univers entier est le bon.

Sur la seule fenêtre d'**étalonnage** — 2021, hors année investie, donc sans
regard sur 2022 —, un stop à −10 % se déclenche sur **6,2 %** des 418 détentions,
en sauve 42,3 %, effet **−0,47 pt ± 1,98** : indiscernable de zéro, du même signe.

### 1.7 Les figures de décision ne séparaient pas ces deux achats des sept autres

Les neuf achats de l'année, avec la **géométrie lue le jour de la décision** —
tout est disponible ce jour-là, rien n'est postérieur :

| Valeur | Décision | Issue | Position | Largeur / cours | τ | Momentum | Épisodes S/R | Volatilité 120 j |
|---|---|---|---|---|---|---|---|---|
| `CAP.PA` | 2021-12-31 | −5,93 % | 41,8 % | 11,5 % | 114,3 | +67,9 % | 4 / 3 | 23,6 % |
| `DSY.PA` | 2021-12-31 | **−18,12 %** | 7,0 % | 16,0 % | 210,5 | +57,5 % | 3 / 4 | 23,1 % |
| `KER.PA` | 2022-02-28 | **−18,50 %** | 19,3 % | 35,0 % | ∞ | +16,7 % | 4 / 3 | 31,4 % |
| `HO.PA` | 2022-03-31 | +9,29 % | 70,2 % | 35,4 % | ∞ | +22,9 % | 5 / 3 | 33,2 % |
| `MT.AS` | 2022-03-31 | +5,32 % | 69,4 % | 21,3 % | 114,7 | +21,1 % | 3 / 3 | 48,0 % |
| `TTE.PA` | 2022-05-31 | +11,12 % | 96,5 % | 20,1 % | ∞ | +25,1 % | 5 / 4 | 32,2 % |
| `BN.PA` | 2022-07-29 | −2,76 % | 25,5 % | 7,6 % | 40,8 | −12,0 % | 3 / 3 | 28,3 % |
| `RMS.PA` | 2022-08-31 | +21,73 % | 3,3 % | 11,8 % | 28,1 | +3,8 % | 3 / 4 | 34,8 % |
| `DG.PA` | 2022-11-30 | −3,88 % | 95,5 % | 19,0 % | ∞ | +11,9 % | 5 / 5 | 21,8 % |

Les deux figures incriminées étaient **propres et sans veto**, comme les sept
autres : au moins 3 épisodes de contact des deux côtés, τ long ou infini,
position franche dans le canal. Je confirme les chiffres de l'énoncé —
`DSY.PA` à 7,0 % d'un canal 49,86–57,92 €, τ = 210,5 séances, 3/4 épisodes ;
`KER.PA` à 19,3 % d'un canal 522,24–718,34 €, τ infini, 4/3 épisodes. Figures
conservées :
[`graphiques/DSY.PA/decision-DSY.PA-2021-12-31.svg`](graphiques/DSY.PA/decision-DSY.PA-2021-12-31.svg)
et
[`graphiques/KER.PA/decision-KER.PA-2022-02-28.svg`](graphiques/KER.PA/decision-KER.PA-2022-02-28.svg).

J'ai balayé, sur chacune des neuf grandeurs du tableau, **tous** les seuils
possibles dans les deux sens, en cherchant un filtre univarié qui écarte
`DSY.PA` et `KER.PA` sans écarter aucune des quatre gagnantes :

| Grandeur | Meilleur filtre écartant les deux | Gagnantes perdues |
|---|---|---|
| Position dans le canal | ≤ 19,3 % | 1 — `RMS.PA` (+21,73 %) |
| Alpha | ≥ −0,24 | 1 — `RMS.PA` |
| τ | ≥ 210,5 | 2 — `HO.PA`, `TTE.PA` |
| Borne haute de l'IC de l'alpha | ≥ 24,31 | 2 — `MT.AS`, `RMS.PA` |
| Largeur relative | ≤ 35,0 % | 3 — `MT.AS`, `RMS.PA`, `TTE.PA` |
| Momentum | ≥ 11,88 % | 3 — `HO.PA`, `MT.AS`, `TTE.PA` |
| Épisodes de contact | ≤ 3 | 3 — `HO.PA`, `MT.AS`, `RMS.PA` |
| Pente du support | ≤ 0,284 %/séance | 3 — `HO.PA`, `MT.AS`, `TTE.PA` |
| **Volatilité 120 j** | **≤ 31,354 %** | **0** ← le seul « filtre parfait » |

> **Résultat, et c'en est un : aucune grandeur de la figure ne distingue les deux
> achats perdants des sept autres, sauf une — et cette exception est un
> sur-ajustement démontrable.**

Le « filtre parfait » consiste à ne garder que les valeurs de volatilité
**supérieure** à 31,354 % — exactement la volatilité de `KER.PA`, au troisième
chiffre. Confronté aux 884 détentions de la fenêtre d'audit :

```
corrélation volatilité 120 j / rendement du mois suivant : rho = +0,0052
t = +0,154 à 882 ddl, p bilatérale = 0,878
vol > 31,4 % : 326 obs, rendement mensuel moyen +0,76 %
vol ≤ 31,4 % : 558 obs, rendement mensuel moyen +1,06 %
différence −0,30 pt, IC95 ± 1,27 pt        ← de signe contraire au filtre
```

Le filtre qui explique parfaitement neuf observations explique **zéro** sur 884,
et sa différence pointe dans l'autre sens. C'est le premier des
[cinq pièges de l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md)
pris sur le fait, et c'est la raison pour laquelle aucune des trois propositions
qui suivent n'est un filtre calé sur ces deux cas.

### 1.8 Deux découvertes de protocole faites en chemin

Elles ne viennent pas des deux pertes : elles viennent de la lecture du
protocole, et se voient sans connaître 2022.

**(i) `KER.PA` a été détenue deux mois de plus parce que la règle était en panne
sur elle.** Sur les 923 évaluations de la fenêtre d'audit, **trois** n'ont produit
aucun critère. Deux sont `KER.PA`, aux deux dates de décision de sa détention :

```
2022-03-31  KER.PA  code 2 : Contrôle de non-traversée en échec :  88 séances du mauvais côté de la résistance.
2022-04-29  KER.PA  code 2 : Contrôle de non-traversée en échec : 108 séances du mauvais côté de la résistance.
2021-10-29  TEP.PA  code 2 : Contrôle de non-traversée en échec :  78 séances du mauvais côté de la résistance.
```

Or le protocole est **asymétrique** : une évaluation en échec est *« traitée
comme un veto »*, donc bloque l'**entrée** ; mais à la sortie, une ligne détenue
absente du classement est *« conservée sans ordre »*, au motif que *« la règle
n'a rien dit d'elle »*. Résultat : `KER.PA` traverse **43 des 65 séances** de sa
détention sans qu'aucun signal ne soit calculable, du 2022-04-01 au 2022-06-01,
période pendant laquelle elle passe de −9,04 % à −18,50 %.

Cette asymétrie est lisible dans le protocole seul. C'est la proposition **P3**.

**(ii) 77 des 120 places du top-5 sont occupées par des valeurs sous veto.** Le
rang est calculé sur le classement **complet**, vetos compris ; le filtre
« rang ≤ 5 » s'applique ensuite ; le veto écarte en dernier. Une valeur sous veto
occupe donc une place d'entrée qu'elle ne peut pas utiliser et qu'elle interdit à
une autre. Sur les 24 dates d'audit : **77 places sur 120 — 64,2 %**, et **51
occasions** d'achat seraient rendues si le rang était compté après retrait des
vetos.

Le contrefactuel 2022 de cette correction — la nommer `R1` — donne −11,86 %, part
investie 88,4 %, bêta 0,782, 50 ordres et 218,56 € de frais. C'est **pire** sur
cette année, pour une raison entièrement attribuable au régime : `TR39` fait
−10,18 %, et doubler l'exposition dans un marché baissier coûte. **Ce chiffre ne
juge pas la correction** ; il montre seulement que la corriger changerait
l'expérience de fond en comble, ce qui interdit de l'ajouter en cours de route.
Je la consigne ici sans en faire une proposition, faute d'une mesure qui la
tranche : sa question est *« le rang doit-il se compter avant ou après le
veto ? »*, et elle mérite une déclaration propre, écrite avant sa première
séance, dans une expérience qui l'aurait pour objet.

---

## 2. Les trois propositions

### P1 · `SANS-S2` — retirer la composante de fenêtre courte du score

| | |
|---|---|
| **Identifiant** | `SANS-S2` |
| **Catégorie** | **B — suggérée par le résultat** |

**Justification du classement.** L'axe vient de deux positions désignées *parce
qu'elles ont perdu*. Et le § 1.1 montre que le lien est encore plus ténu qu'il
n'y paraît : `s2 = 0` aux deux décisions d'achat, donc la composante incriminée
n'a joué **aucun rôle** dans les deux entrées qu'on lui reproche. La piste est
donc B, et faiblement motivée.

**Un élément de la proposition est cependant de catégorie A**, et je le sépare :
le taux de bascule du panier — 10 dates sur 12 sur la fenêtre d'**étalonnage**,
antérieure à l'année investie — est mesurable sans connaître 2022. Il établit que
`s2`, à 3,1 % de la variance du score, **n'est pas une composante marginale mais
un départageur**, et que le bilan publie donc un poids effectif qui sous-estime
largement son rôle réel. Ce constat-là mérite d'être repris tel quel dans le
prochain protocole, indépendamment de la suite.

**Ce qu'elle change exactement.**

- Score : `s = s1 + s3 + s4 + s5` au lieu de `s1 + s2 + s3 + s4 + s5`.
- Le **veto 3 est conservé** — il reste défini par `TEND_20`, et le retirer serait
  un second changement (cf. § 1.3, lecture c, dont l'effet 2022 est d'ailleurs
  opposé sur le nombre d'ordres : 25 contre 11).
- Rien d'autre : mêmes seuils d'entrée et de sortie, même moment d'exécution,
  mêmes vetos, même répartition.
- **`VAL_20` n'est pas concernée** : elle n'entre dans aucun calcul de la règle,
  et la retirer serait une opération vide.

**Coût.** Aucune donnée nouvelle. Aucun calcul nouveau — la colonne `TEND_20`
reste produite par `import_societe.py` et reste nécessaire au veto 3. Aucun frais
d'exécution supplémentaire : le changement ne touche pas le moment d'exécution.
Coût réel : **une ligne de `composantes()`**, et l'obligation de republier tous
les classements.

**Comment on saurait qu'elle améliore quelque chose.**

| Mesure | Ce qu'elle vaut | Observations nécessaires |
|---|---|---|
| Alpha annuel | TE 15,58 %/an → EMD **± 30,5 pt** | l'effet plausible est de l'ordre de ± 5 pt/an, soit **37 ans** |
| Alpha contre un fantôme partageant l'univers | écart-type de la différence ≈ 8,3 %/an → EMD ± 16,3 pt | ≈ 10 ans pour 5 pt |
| **Taux de bascule du panier achetable** | 10/12 étalonnage, 6/12 narré | **directement mesurable, dès la première année** |
| Part investie et bêta | 35,7 % vs 45,3 %, β 0,219 vs 0,382 | mesurables sur une année |

> **L'effet attendu de `SANS-S2` sur l'alpha est plus petit que l'effet minimal
> détectable sur un an.** Il n'est donc **pas testable sur une année**, et le dire
> est plus utile que de publier un contrefactuel. Ce qui est testable est la
> bascule du panier et l'exposition, qui se mesurent en une année et qui
> caractérisent la règle, pas le régime. Le protocole d'une expérience suivante
> devrait donc faire tourner `SANS-S2` en **portefeuille fantôme**, comme le `s3`
> de l'expérience 3, et publier l'écart de leur **différence** — dont
> l'incertitude est deux fois plus faible que celle de chacun contre l'indice.

**Contrefactuel 2022 — connaissant l'année, donc sans valeur probante.**
`SANS-S2` aurait rendu **+6,01 %** au lieu de −2,36 %, soit **+8,37 points**, avec
11 ordres au lieu de 16 et 49,27 € de frais au lieu de 75,24 €. **Ce chiffre est
trompeur pour trois raisons, toutes chiffrées :** la part investie tombe à 35,7 %
et le bêta à 0,219 dans une année qui baisse de 10,18 % ; l'alpha de régression,
qui corrige l'exposition, passe de +2,29 à +8,61 %/an avec un IC95 de ± 16,8
points, donc indiscernable ; et la variante **n'aurait pas évité `DSY.PA`**, la
plus lourde des deux pertes, qui serait montée du rang 5 au rang 2.

---

### P2 · `STOP-10` — plafond de perte à 10 % du prix d'achat

| | |
|---|---|
| **Identifiant** | `STOP-10` |
| **Catégorie** | **B — suggérée par le résultat** |

**Justification du classement.** Sans les deux pertes, personne n'aurait proposé
un stop : les sept autres positions ne l'appellent pas, et la plus grosse
gagnante de l'année (`RMS.PA`, +21,73 %) est passée à −8,12 % en cours de route.
La piste est B sans ambiguïté.

**Je la présente parce qu'elle a été demandée, et parce qu'elle est réfutable —
et réfutée.** La formuler proprement et publier le chiffre qui la contredit vaut
mieux que de l'écarter en silence.

**Ce qu'elle change exactement.**

- **Grandeur observée** : la **clôture**, pas le `Low`. Motif au § 1.5 : la
  convention `Low` suppose une exécution au seuil, ce que le gap de `KER.PA`
  interdit précisément les jours où le stop sert.
- **Déclenchement** : première séance, postérieure à l'achat, où
  `Close ≤ prix d'achat × 0,90`. Le seuil est fixe, calé sur le prix d'achat, et
  n'est **jamais relevé** — un stop suiveur serait un troisième paramètre.
- **Exécution** : à l'**ouverture de la séance suivante**, comme tout ordre du
  protocole. Le gap est subi et publié.
- **Rachat** : libre à la décision suivante si la valeur redevient achetable. Le
  § 1.5 montre que le paramètre de quarantaine (1, 2 ou 12 mois) est sans effet
  sur cette fenêtre — aucune valeur stoppée n'est jamais revenue au panier.
- **C'est un changement de protocole, pas un réglage** : le protocole actuel
  n'exécute qu'à l'ouverture de la première séance du mois. `STOP-10` introduit
  une **exécution en cours de mois**, ce qui oblige à surveiller la clôture de
  chacune des 257 séances de l'année pour chaque ligne détenue, et non plus 12
  dates.

**Coût.**

- *Données* : aucune nouvelle — `Close` suffit. Le choix de la clôture évite
  d'avoir à se fier au `Low`, dont l'exécutabilité au seuil n'est pas vérifiable
  a posteriori.
- *Calcul* : une comparaison par ligne détenue et par séance, soit environ 580
  comparaisons sur l'année, contre 12 aujourd'hui.
- *Frais* : **0,115 % à la vente** (courtage 0,100 % + demi-spread 0,015 %) et,
  si la valeur est rachetée, **0,415 %** de plus à l'achat — soit **0,530 %**
  l'aller-retour, TTF comprise, pour toute position stoppée puis reprise. En 2022,
  `STOP-10` porte le compte d'ordres de 16 à **17** et les frais de 75,24 € à
  **75,59 €** : les stops **remplacent** des ventes mensuelles au lieu de s'y
  ajouter, et aucun rachat n'a lieu. Le surcoût direct est donc de **+0,35 €**,
  négligeable. **Le coût du stop n'est pas dans ses frais, il est dans ce qu'il
  coupe.**

**Comment on saurait qu'elle améliore quelque chose.**

| Mesure | Ce qu'elle vaut | Observations nécessaires |
|---|---|---|
| Alpha annuel | EMD ± 30,5 pt | effet attendu ≈ −1 à −6 pt/an → **37 à 930 ans** |
| **Taux de « sauvetage » parmi les déclenchements** | **40,4 % ± 8,2** sur 136 déclenchements | **déjà mesuré** |
| **Effet moyen par déclenchement** | **−1,68 pt ± 1,11** | **déjà mesuré, exclut zéro** |
| Taux de déclenchement | 15,4 % ± 2,4 sur 884 détentions | déjà mesuré |

> **La mesure existe déjà et conclut contre la piste.** Sur les 884 détentions
> d'un mois de la fenêtre d'audit, un stop à −10 % coupe à tort **59,6 %** du
> temps, pour un effet moyen de **−1,68 point par déclenchement**, IC95 ± 1,11.
> Sur la seule fenêtre d'étalonnage, hors année investie, l'effet vaut
> −0,47 pt ± 1,98 : même signe, indiscernable de zéro.
>
> **La réserve du § 4 s'applique à ces IC** : les 884 détentions se chevauchent
> par date et partagent un facteur de marché commun ; elles ne sont pas
> indépendantes, et l'intervalle est plus étroit que la réalité. Un IC de ± 1,11
> point est donc une borne inférieure de l'incertitude.

**Contrefactuel 2022 — connaissant l'année, donc sans valeur probante.**
`STOP-10` aurait rendu **−7,94 %** au lieu de −2,36 %, soit **−5,58 points**. Il
sauve `DSY.PA` (+9,23 pt) et à peine `KER.PA` (+1,51 pt, le gap ayant mangé le
reste), et coupe `CAP.PA` (−4,59 pt), `MT.AS` (−14,72 pt) et `TTE.PA`
(−21,57 pt). **Aucun des huit couples (seuil, convention) testés ne fait mieux que
l'absence de stop.**

**Reformulation proposée.** Le problème que l'axe 2 croit viser — une position qui
perd 18 % sans qu'on puisse rien faire — n'est pas un problème de seuil ; c'est un
problème de **cadence** et de **silence de la règle**. `DSY.PA` a été vendue à la
première date où la règle pouvait parler, et aucun stop n'était nécessaire pour
cela : le protocole avait déjà réagi. `KER.PA`, elle, a été gardée **parce que la
règle ne pouvait rien dire**. C'est l'objet de `P3`, qui traite le même symptôme
sans introduire d'exécution en cours de mois, sans paramètre de seuil, et sans
coûter un ordre.

---

### P3 · `MUETTE-SORTIE` — une évaluation en échec commande la sortie, comme elle interdit l'entrée

| | |
|---|---|
| **Identifiant** | `MUETTE-SORTIE` |
| **Catégorie** | **A — indépendante du résultat** |

**Justification du classement.** Cette proposition ne se déduit pas de la perte de
`KER.PA` : elle se déduit de la lecture du protocole. Le README déclare, avant la
première séance, qu'*« une évaluation que la règle n'a pas su produire […] est
traitée comme un veto : une figure qu'on ne sait pas calculer n'est pas une figure
qu'on peut acheter »*, tandis que `vendre()` déclare qu'*« une ligne détenue
absente du classement est CONSERVÉE sans ordre »*. **Les deux énoncés se
contredisent** : une figure qu'on ne sait pas calculer n'est pas non plus une
figure qu'on peut *conserver*, puisque la conserver est exactement la décision que
le classement était censé prendre. L'asymétrie se voit dans le texte du protocole,
sans ouvrir un seul CSV, et donc sans connaître 2022.

Que `KER.PA` en soit le cas d'espèce est une coïncidence heureuse pour
l'illustration, pas la source de la piste — et je publie ci-dessous le
contrefactuel avec la même réserve que pour les deux autres.

**Ce qu'elle change exactement.**

- **Règle de sortie**, un troisième motif s'ajoute aux deux existants (rang > 7,
  score ≤ −3) : *une ligne détenue dont l'évaluation à la date de décision est en
  échec — code de sortie non nul, contrôle de non-traversée en échec, colonne
  `VERDICT = ERREUR` — est vendue à l'ouverture de la date d'exécution.*
- **Moment d'exécution inchangé** : première séance du mois, à l'ouverture. Aucune
  exécution en cours de mois, contrairement à `STOP-10`.
- **Aucun seuil, aucun paramètre.** C'est la levée d'une asymétrie, pas
  l'introduction d'un réglage — donc rien à calibrer, rien à sur-ajuster.
- Reste intacte la distinction avec le cas *« sortie de l'indice »* : une valeur
  qui quitte l'univers n'est pas une valeur dont la règle a échoué. Le motif de
  vente doit citer le **diagnostic**, comme les ordres actuels citent leur rang.

**Coût.**

- *Données* : aucune. La colonne `DIAGNOSTIC` de `criteres.csv` existe déjà et
  porte le code de retour.
- *Calcul* : un test dans `vendre()`.
- *Frais* : **0,115 % à la vente**, aux mêmes dates que les ventes existantes. En
  2022, le compte d'ordres reste à **16** — la vente anticipée de `KER.PA`
  remplace celle du 2022-06-01 — et les frais passent de 75,24 € à **75,66 €**,
  soit **+0,42 €** sur l'année, entièrement dus au fait que la vente a lieu à un
  cours plus élevé.

**Comment on saurait qu'elle améliore quelque chose.**

| Mesure | Ce qu'elle vaut | Observations nécessaires |
|---|---|---|
| **Taux d'évaluations en échec** | **3 / 923 = 0,32 % ± 0,37 pt** | mesurable, mais **rarissime** |
| Détentions concernées par an | 1 sur 9 positions en 2022 | ≈ 1 par an à ce taux |
| Alpha annuel | EMD ± 30,5 pt | effet attendu ≈ +1,6 pt/an → **≈ 360 ans** |
| Cohérence du protocole | binaire | **immédiate, et c'est le vrai critère** |

> **Cette proposition ne sera jamais tranchée par une mesure de performance**, et
> il faut le dire franchement : elle porte sur **0,32 %** des évaluations, soit
> environ une position par an. Son effet annuel, de l'ordre de +1,6 point, est
> vingt fois plus petit que l'effet minimal détectable. **Elle ne se juge pas sur
> un rendement mais sur une cohérence** : le protocole affirme deux choses
> incompatibles sur le même événement, et l'une des deux doit céder.
>
> Ce qui **est** mesurable, et devrait être publié : le **taux d'évaluations en
> échec** (3/923 ici, ± 0,37 pt), le **nombre de séances de détention passées sans
> signal** (43 sur 65 pour `KER.PA`, soit 66 % de sa détention), et la **durée
> médiane du silence** — trois taux, du genre de ceux sur lesquels l'expérience 3
> a déclaré vouloir porter son objet.

**Contrefactuel 2022 — connaissant l'année, donc sans valeur probante.**
`MUETTE-SORTIE` aurait vendu `KER.PA` le **2022-04-01 à 507,80 €** (−9,04 %) au
lieu du 2022-06-01 à 454,99 € (−18,50 %) : **+9,46 points sur la position**. Le
portefeuille finit à **9 921,45 €**, soit **−0,79 %** au lieu de −2,36 %, un écart
de **+1,57 point**, à **nombre d'ordres identique** (16) et pour **+0,42 €** de
frais. C'est le meilleur rapport effet / perturbation des trois propositions, et
c'est aussi celui dont l'effet est le plus difficile à établir statistiquement.

Combinée à `SANS-S2`, elle est sans effet supplémentaire — `SANS-S2` n'achète
jamais `KER.PA` — et le portefeuille finit à 10 600,79 €, comme `SANS-S2` seule.

---

### Récapitulatif

| Id | Titre | Cat. | Axe | Ce qu'elle change | Contrefactuel 2022 | Testable en 1 an ? |
|---|---|---|---|---|---|---|
| `SANS-S2` | Retirer la composante de fenêtre courte du score | **B** | 1 | `s = s1+s3+s4+s5` ; veto 3 conservé | +6,01 % (+8,37 pt) | Non sur l'alpha ; **oui** sur la bascule du panier |
| `STOP-10` | Plafond de perte à 10 % du prix d'achat, sur clôture | **B** | 2 | exécution **en cours de mois** | −7,94 % (**−5,58 pt**) | Non sur l'alpha ; **déjà tranché** par le taux de sauvetage |
| `MUETTE-SORTIE` | Une évaluation en échec commande la sortie | **A** | issu des deux | 3ᵉ motif de vente, même moment d'exécution | −0,79 % (+1,57 pt) | **Non** — 0,32 % des évaluations |

---

## 3. La contrainte de catégorie, rappelée

Ces deux valeurs ont été désignées **parce qu'elles ont perdu**. Toute piste qui
en découle est donc de **catégorie B — suggérée par le résultat**, et n'est
recevable qu'à la condition d'être nommée comme telle, ce qui est fait au § 2 pour
`SANS-S2` et `STOP-10`.

Une piste B présentée comme un enseignement serait le premier des
[cinq pièges de l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md) :
choisir l'échantillon après avoir vu le résultat. Le § 1.7 en donne la
démonstration numérique sur ce document même — un filtre qui sépare parfaitement
neuf observations et n'explique rien sur 884.

Une seule des trois propositions est de **catégorie A** : `MUETTE-SORTIE`, parce
qu'elle se dérive de la contradiction interne du protocole écrit, sans qu'aucun
cours de 2022 soit nécessaire pour la voir. Et c'est aussi, ironiquement, celle
dont l'effet est le plus petit et le moins mesurable. **C'est le cas général : les
corrections défendables sont rarement celles qui rapportent, et les corrections
qui rapportent sur une année connue sont rarement défendables.**

---

## 4. Ce que cette analyse ne peut pas établir

**Elle ne peut pas établir qu'une des trois propositions améliore la
performance.** L'expérience 3 a une tracking error réalisée de **15,58 %/an**,
donc un effet minimal détectable de **± 30,5 points d'alpha annuel**. Les trois
effets attendus sont plus petits que cela, souvent d'un ordre de grandeur :

| Effet supposé | Années nécessaires pour le détecter |
|---|---|
| 30,5 pt/an | 1,0 |
| 15 pt/an | 4,1 |
| 10 pt/an | 9,3 |
| 5 pt/an | 37,3 |
| 2 pt/an | 233 |
| 1 pt/an | 933 |

**Elle ne peut pas établir que les deux positions analysées étaient
identifiables.** Le § 1.7 le montre au contraire : aucune des neuf grandeurs de la
figure de décision ne les sépare des sept autres, et la seule qui semble le faire
— la volatilité — a une corrélation de **+0,005** avec le rendement du mois suivant
sur 884 observations (p = 0,878), et sa différence de rendement est **de signe
contraire** au filtre qu'elle suggère.

**Elle ne peut pas s'appuyer sans réserve sur les intervalles publiés.** Les 884
détentions du § 1.6 se chevauchent par date et partagent un facteur de marché
commun ; elles ne sont pas i.i.d. Le test de tendance sous-jacent
([étape 8](../../../raw/concept/semestre3/modele/08-test-de-tendance.md)) suppose
des erreurs indépendantes, hypothèse fausse sur une série de cours, où
l'autocorrélation fait rejeter $H_0$ bien plus souvent que le seuil nominal. Les
IC95 donnés ici sont donc des **bornes inférieures** de l'incertitude réelle.

**Elle ne peut pas généraliser hors de 2022 et hors du CAC 40.** Une seule année,
un seul indice, un seul régime — et un régime baissier de 10,18 %, dans lequel
toute variante qui réduit l'exposition paraît bonne et toute variante qui
l'augmente paraît mauvaise. C'est exactement ce qui se lit dans les bêtas : 0,219
pour `SANS-S2`, 0,166 pour `STOP-10`, 0,782 pour `R1`, contre 0,382 pour la règle
publiée. **Aucun de ces chiffres ne dit si la règle est bonne ; ils disent tous à
quel point elle était exposée.**

**Elle ne peut pas être appliquée à l'expérience 3 rétroactivement.** Modifier un
protocole après avoir vu son résultat est le rétro-ajustement même, et le
[bilan § 6](bilan-2022.md) l'a déjà refusé pour un veto dont la différence
contient zéro. Les trois propositions sont des **candidates pour la déclaration
écrite avant la première séance d'une expérience suivante**, pas des correctifs.

**Elle ne peut pas trancher la question du rang compté avant ou après le veto**
(§ 1.8-ii), qui est pourtant le constat de catégorie A le plus lourd de ce
document : 77 places sur 120 des top-5 sont occupées par des valeurs sous veto, et
51 occasions d'achat en découlent. Son contrefactuel 2022 est mauvais (−11,86 %),
mais pour une raison de régime et non de règle. Elle appelle sa propre expérience,
avec son propre dimensionnement publié d'avance.

**Enfin, elle ne dit rien sur `DSY.PA` ni sur `KER.PA` en tant que valeurs.**
Aucune conclusion de ce document ne porte sur ces sociétés, sur leur cours à venir,
ni sur l'opportunité de les détenir. Elles sont ici deux sorties d'une règle, et
rien d'autre.

---

## 5. Comment refaire les calculs

Tous les chiffres viennent d'un moteur autonome qui importe
[`journal.py`](journal.py) comme module et réutilise ses fonctions
(`charger_univers`, `charger_serie`, `calendrier`, `composantes`, `taux_achat`,
`taux_vente`), plus `p_valeur_student()` de
[`python/import_societe.py`](../../../../python/import_societe.md) pour le test du
§ 1.7. Aucune dépendance ajoutée : `pandas` (via `yfinance`) et la bibliothèque
standard suffisent.

**Contrôle de reproduction, à faire passer avant tout contrefactuel :** le moteur
doit rendre les **16 ordres** de [`ordres.csv`](ordres.csv) à l'identique, la
valeur finale **9 764,22 €** et `TR39` à **89,82**. Il les rend.

Les séries nécessaires, si elles manquent :

```bash
python python/import_societe.py DSY.PA --debut 2019-01-02 --fin 2022-12-31
python python/import_societe.py KER.PA --debut 2019-01-02 --fin 2022-12-31
```

Les variantes se paramètrent par sept leviers indépendants, tous déclarés :
`sans_s2`, `sans_veto3`, `stop` (seuil en %), `base_stop` (`close` ou `low`),
`quarantaine` (en mois), `rang_apres_veto`, `sortir_si_muette`.

> ⚠️ **Un piège rencontré, et corrigé.** Une première version du moteur ré-armait
> le stop à chaque séance sous le seuil, si bien que l'exécution était repoussée
> jusqu'à la première séance de rebond — ce qui faisait sortir `KER.PA` à 489,95 €
> (−12,23 %) au lieu de 463,41 € (−16,99 %), et **flattait le stop de près de 5
> points sur la position la plus défavorable**. Le stop doit s'armer **une seule
> fois**, à la première clôture sous le seuil. Tous les chiffres de ce document
> sont postérieurs à la correction.
