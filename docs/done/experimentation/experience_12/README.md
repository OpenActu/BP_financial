# Expérience 12 — la même règle, sans le veto de pente

Les six règles de l'[expérience 11](../experience_11/README.md), sur les **dix
mêmes valeurs**, avec une seule modification de fond : **la règle 3 n'exige plus
`TAUX_20 ≥ 0`**. Elle achète désormais sous le bord bas quelle que soit la pente
courte.

La modification vient de l'analyse des quatorze arbitrages étiquetés sur Airbus,
consignée dans [`arbitrages.md`](../experience_11/arbitrages.md) : c'était la
**seule information nouvelle** que ces étiquettes contenaient.

---

## ⚠️ Ce que cette expérience déclare avant tout

**1. Elle reste de catégorie B, et la condition de promotion n'est pas remplie.**
`arbitrages.md` posait que la suppression du veto serait promouvable en A si elle
était déclarée **avant une fenêtre non jouée**. Or 2022-2026 a déjà été jouée par
les expériences 10 et 11. La condition n'est **pas** tenue, et la modification
reste **B**.

**2. Mais son résultat, lui, est inconnu.** Contrairement à l'expérience 11 — dont
le chiffre était publié avant qu'elle soit écrite —, la variante sans veto sur les
**dix valeurs** n'a jamais été calculée. Elle ne l'a été que sur Airbus seule. Le
protocole ci-dessous a donc été rédigé **avant** de jouer la fenêtre, et
l'étalonnage publié sans connaître le résultat.

**3. L'alpha est le résultat principal déclaré — et il ne tranchera rien.** C'est
le choix retenu pour cette expérience, et il est tenu : l'alpha figure en tête du
bilan. Mais l'écart-type de la différence avec l'expérience 11 vaut **6,92 %/an**,
soit un effet minimal détectable de **± 13,6 points**. Il faudrait **184 ans** pour
établir un écart d'un point par an. Tout écart inférieur à 13,6 points est du
bruit, et le bilan le répétera à côté du chiffre.

> **Ce qu'elle peut établir** : les **taux de déclenchement** sur 1 330
> évaluations, les **frais** — exacts —, le nombre de positions et de refus, et
> **ce que le veto écartait réellement**.

---

## Les deux modifications, et pourquoi il y en a deux

| | Modification | Motif |
|---|---|---|
| **1** | La **règle 3** n'exige plus `TAUX_20 ≥ 0` | l'objet même de l'expérience |
| **2** | Les tranches passent de 10 / 20 % à **5 / 10 %** | **neutraliser** l'effet de la première sur l'exposition |

La seconde n'est pas une amélioration : c'est une **correction de comparabilité**,
et elle doit être lue comme telle. Sans elle, retirer le veto ferait passer la
part investie de 33,8 % à **57,2 %**, et l'écart mesuré mêlerait le veto et
l'exposition — le piège que `CLAUDE.md` nomme « un écart brut à l'indice n'est pas
un alpha ». Avec elle, la part investie tombe à **32,58 %**, contre 33,84 % pour
l'expérience 11 : **1,26 point d'écart**, et la comparaison porte sur le veto seul.

> **Ce que l'appariement rapporte, mesuré.** Aux tranches d'origine,
> l'écart-type de la différence avec l'expérience 11 vaut **15,36 %/an** ; aux
> tranches appariées, **6,92 %/an**. **Neutraliser l'exposition divise
> l'incertitude de la comparaison par 2,2.** C'est un résultat de méthode, acquis
> avant la fenêtre jouée.

### Ce qui ne change pas

**La règle 6 conserve son veto.** `arbitrages.md` ne supprime le filtre que de la
règle 3 ; l'étendre à la règle 6 serait une troisième modification, non demandée.
La règle 4 n'a jamais porté ce filtre — c'est précisément l'asymétrie qui motive
l'expérience.

Restent inchangés : la cadence hebdomadaire, l'exécution à l'ouverture suivante,
le plafond de 100 % sans levier, l'ordre de service par écart le plus négatif, le
service partiel des ordres quand les espèces manquent, et les dix valeurs.

---

## Les six règles

| | Énoncé | Change ? |
|---|---|---|
| **1** | **Isolation** — dix valeurs, aucun classement | non |
| **2** | **Cadence hebdomadaire**, exécution à l'ouverture suivante | non |
| **3** | **Achat à 5 %** — clôture `< VAL_120 − 1 s₁₂₀` | ⚠️ **plus de condition de pente** ; tranche 10 % → 5 % |
| **4** | **Nouvel achat à 5 %** — seuil figé, une fois par position | tranche seule |
| **5** | **Vente** — clôture `> VAL_120 + 1 s₁₂₀`, solde tout | non |
| **6** | **Renforcement à 10 %** — une fois, à la décision suivante, **`TAUX_20 ≥ 0` conservé** | tranche seule |

La règle 5 reste la **seule sortie** : ni coupe, ni stop.

---

## L'univers — identique, et revérifié

Les dix valeurs du tirage de l'expérience 10, graine 10 : **ENGIE, ACCOR,
BOUYGUES, Total, Safran, Airbus, Publicis, SAINT-GOBAIN, LVMH, Cap Gemini**.
Trois valeurs tirées avaient été écartées sur leurs seules données — Vivendi,
Technip, Unibail. [`univers.csv`](univers.csv) est le même fichier, et le moteur
**rejoue la permutation** à chaque exécution. Airbus reste exemptée de TTF.

---

## Le dimensionnement, publié avant la fenêtre jouée

Étalonnage **2019-06-21 → 2021-12-31**, 133 décisions, **1 330 évaluations**.

| Variante | Base 100 | Appariée | **Alpha** | EMD | Ordres | Frais | Part investie | Maximum |
|---|---|---|---|---|---|---|---|---|
| **Déclarée** — règles 4 et 6 | 113,11 | 109,67 | **+3,45 pt** | ± 5,5 | 138 | 208,40 € | **32,58 %** | 82,2 % |
| Sans la règle 4 | 111,52 | 108,00 | +3,52 pt | ± 3,9 | 109 | 145,57 € | 22,83 % | 52,7 % |
| Sans la règle 6 | 110,49 | 107,93 | +2,56 pt | ± 5,1 | 135 | 192,46 € | 30,60 % | 82,2 % |
| Ni la règle 4 ni la 6 | 108,96 | 106,38 | +2,59 pt | ± 3,5 | 106 | 130,30 € | 20,95 % | 43,0 % |
| *Témoin — [expérience 11](../experience_11/README.md), veto conservé* | *123,01* | *115,25* | *+7,77 pt* | *± 11,2* | *75* | *257,80 €* | *33,84 %* |  |

| Grandeur, étalonnage | Valeur |
|---|---|
| Détention continue du panier | 130,39 |
| Évaluations **sous le bord bas** · dont `TAUX_20 ≥ 0` | 309 sur 1 330 · 58 |
| … donc **achetables en plus**, veto retiré | **251** |
| Évaluations au-dessus du bord haut | 289 |
| Règle 4 · règle 6 possibles | 29 · 3 |
| Ordres refusés faute d'espèces | **10** |
| Positions ouvertes · closes | **56** · 50 |
| **Écart-type de la différence** avec l'expérience 11 | **6,92 %/an** → EMD **± 13,6 pt** |

> **Ce que l'étalonnage dit déjà, et qu'il faut lire avant les résultats.**
>
> - ⚠️ **Retirer le veto dégrade l'alpha de 4,32 points** — +3,45 contre +7,77 —
>   et la base de 9,90 points. L'écart reste **sous son EMD de ± 13,6 pt**, donc
>   indiscernable, mais le signe est publié avant la fenêtre.
> - **Le veto écartait 81 % des candidats** : 251 évaluations sur 309 deviennent
>   achetables. Les positions passent de 29 à **56**, les ordres de 75 à **138**.
> - **Et pourtant les frais baissent** — 208,40 € contre 257,80 € — parce que les
>   tranches sont deux fois plus petites. Deux fois plus d'ordres, un cinquième
>   de frais en moins.
> - **La règle 4 n'apporte rien** : son retrait *améliore* l'alpha (+3,52 contre
>   +3,45). Elle coûte 29 ordres et 62,83 € pour un effet nul.
> - **La règle 6 ne se déclenche presque plus** : 3 occasions contre 5, parce
>   qu'elle exige une pente positive que les nouveaux achats n'ont pas.

---

## Les issues déclarées

Inchangées : rendement du cours sur les **20 séances suivant la décision**, sur un
sous-échantillon d'une décision sur quatre, intervalles **par grappes de dates** —
la date est l'unité, jamais la valeur.

| Élément | Groupe testé | Témoin |
|---|---|---|
| **Règle 3, bande** | évaluations sous le bord bas | les autres |
| **Règle 3, pente** | sous le bord bas et `TAUX_20 ≥ 0` | sous le bord bas et `TAUX_20 < 0` |
| **Règle 5, bande haute** | évaluations au-dessus du bord haut | les autres |

La deuxième est celle qui porte l'objet de l'expérience. L'expérience 11 l'a
mesurée à **−1,81 pt ± 2,89** : le point estimé est négatif — le groupe que le
veto laissait passer a fait *moins* bien — mais l'intervalle contient zéro. **La
mesure n'arbitrait pas**, et c'est pourquoi cette expérience existe.

---

## Les deux contrôles de reproduction

| Contrôlé — le moteur s'arrête sinon | Portée |
|---|---|
| la permutation se rejoue depuis la graine 10 et redonne `univers.csv` | le tirage |
| les **évaluations** coïncident avec celles de l'expérience 11, valeur par valeur | écart réduit et `TAUX_20` |

Les **ordres** ne peuvent pas être contrôlés : retirer le veto change l'état du
portefeuille dès la première décision, et les quantités suivent des tranches
différentes. C'est la limite que l'expérience 11 n'avait pas — elle, pouvait
exiger la coïncidence ordre par ordre.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| [`univers.csv`](univers.csv) | les 40 valeurs dans l'ordre du tirage, et le motif des trois rejets |
| `bilan.md` | le bilan de la fenêtre jouée, et la comparaison avec l'expérience 11 |
| `rapports/2022.md` … `2026.md` | un journal par année |
| [`journal.md`](journal.md) · `journal.py` | le miroir d'exécution, puis le moteur |
| `decisions.csv` · `ordres.csv` · `positions.csv` | les décisions, les ordres, les positions |
| `portefeuille.csv` · `issues.csv` | la valorisation quotidienne, les trois issues |
| `graphiques/{TICKER}/canal-{DATE}.svg` | la figure de canal, rangée par valeur |
| `graphiques/portefeuille-{ANNEE}.svg` | le portefeuille et ses deux références |

**Aucun texte n'est rédigé à la main** : tous les chiffres sortent du moteur.

---

## Ce que l'expérience 12 ne fait pas

- **Aucun levier, aucune couverture, aucune vente à découvert, aucun stop.**
- **Aucune promotion abusive en catégorie A** : la fenêtre a déjà été jouée.
- **Aucun réglage du seuil** : `± 1 s` est hérité, et ne bouge pas.
- **Aucune prédiction de cours, aucun conseil en investissement.**

## Pour aller plus loin

- [Les arbitrages étiquetés sur Airbus](../experience_11/arbitrages.md) — d'où vient la suppression du veto
- [L'expérience 11](../experience_11/README.md) — la même règle, veto conservé
- [L'expérience 10](../experience_10/README.md) — la coupe à −15 %, et ce qu'elle a coûté
- [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md) · [Semestre 3 · canal](../../../raw/concept/semestre3/canal/README.md)
