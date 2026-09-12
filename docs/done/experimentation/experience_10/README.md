# Expérience 10 — une septième règle qui coupe à −15 %, sur dix valeurs tirées au sort

Un portefeuille de **10 000 €** conduit par les six règles de
l'[expérience 9](../experience_9/README.md), **plus une septième** : si le repli
depuis le prix d'achat atteint **−15 %**, la position est vendue. L'univers passe
de cinq à **dix valeurs**, tirées au sort dans le CAC 40 du 2 janvier 2019.

Décision hebdomadaire, du 3 janvier 2022 au 10 septembre 2026.

---

## ⚠️ Ce que cette expérience doit déclarer avant tout le reste

> **Le seuil de −15 % est de catégorie B au sens le plus fort.** Il ne vient pas
> d'une théorie : il vient de l'analyse des replis des 19 positions de
> l'expérience 9, où les lignes bénéficiaires s'arrêtaient à −13,54 % et les
> déficitaires commençaient à −13,89 %. C'est un seuil **lu après avoir vu quelles
> lignes avaient gagné**, et j'écrivais alors qu'en faire une règle de coupe
> serait exactement le rétro-ajustement que le dépôt proscrit.
>
> Le tester n'est légitime qu'à trois conditions, toutes tenues ici :
>
> 1. le dire, **ici, avant de jouer** ;
> 2. le tester sur un univers **qui n'a pas servi à le fabriquer** — d'où le
>    nouveau tirage : **huit des dix valeurs sont inédites** ;
> 3. publier l'étalonnage **avant** la fenêtre jouée, ce que fait la section
>    « Le dimensionnement ».

Deux valeurs, **ENGIE** et **Safran**, appartenaient déjà à l'expérience 9 :
l'univers est inédit à 8 sur 10, pas à 10 sur 10, et c'est dit plutôt que tu.

### Les trois autres limites

1. **Elle reste de catégorie B pour tout le reste aussi.** Les six premières
   règles sont celles de l'expérience 9, et la fenêtre contient 2022, année déjà
   jouée six fois.
2. **Dix valeurs ne sont toujours pas un univers.** Un autre tirage donnerait un
   autre résultat, et cette dispersion n'est pas mesurée.
3. **L'effet minimal détectable reste large** : sur l'étalonnage, la tracking
   error contre la référence appariée vaut 4,10 %/an, soit **± 8,0 points**.

> **Ce qu'elle peut établir** : les **taux de déclenchement** sur 1 330
> évaluations, les **frais** — exacts —, ce que la règle 7 **coupe réellement**,
> et si elle borne la perte qu'elle prétend borner.

---

## Le tirage — déclaré avant d'être fait

| | Convention |
|---|---|
| **Population** | le CAC 40 **à sa composition du 2019-01-02**, soit **40 valeurs**, Air Liquide comprise et **sans privilège** — contrairement à l'expérience 9 |
| **Ordre canonique** | les 40 triées par **code ISIN croissant** |
| **Permutation** | `random.Random(10)` — **graine 10**, le numéro de l'expérience |
| **Sélection** | les **dix premières recevables** dans l'ordre de la permutation |

La recevabilité est celle de l'expérience 9, seuil de scission compris : série en
euros, complète du 2019-01-02 au 2026-09-10, volume positif, et **aucun saut de
clôture supérieur à 50 % en une séance sans division déclarée**.

### Ce que le tirage a donné

| Rang | Valeur | Verdict |
|---|---|---|
| 1 | **ENGIE** (`ENGI.PA`) | retenue — *déjà dans l'expérience 9* |
| 2 | **ACCOR** (`AC.PA`) | retenue |
| 3 | **BOUYGUES** (`EN.PA`) | retenue |
| 4 | Vivendi | ⚠️ **écartée** — scissions non répercutées, [motif établi en expérience 9](../experience_9/README.md) |
| 5 | **Total** (`TTE.PA`) | retenue |
| 6 | **Safran** (`SAF.PA`) | retenue — *déjà dans l'expérience 9* |
| 7 | **Airbus** (`AIR.PA`) | retenue — **société néerlandaise, exemptée de TTF** |
| 8 | **Publicis** (`PUB.PA`) | retenue |
| 9 | Technip | ⚠️ **écartée** — aucune série en euros |
| 10 | **SAINT-GOBAIN** (`SGO.PA`) | retenue |
| 11 | Unibail-Rodamco | ⚠️ **écartée** — aucune série en euros |
| 12 | **LVMH** (`MC.PA`) | retenue |
| 13 | **Cap Gemini** (`CAP.PA`) | retenue, au dixième rang |

Les rangs 14 à 40 n'ont **jamais été examinés**. L'ordre complet est figé dans
[`univers.csv`](univers.csv), et le moteur **rejoue la permutation à chaque
exécution** : il s'arrête si le fichier en diffère.

> **Technip, écartée sur les données.** L'ISIN tiré, `FR0000131708`, est celui de
> Technip SA, absorbée par TechnipFMC. Le fournisseur ne sert **aucune série en
> euros** : `FTI.PA` et `TEC.PA` ne rendent rien, seul `FTI` existe et cote **en
> dollars**. Substituer Technip Energies (`TE.PA`) serait une faute — c'est une
> autre société, née de la scission de 2021. Motif identique à Unibail-Rodamco.

### Ce que les dix valeurs ont en commun

Les dix séries partagent **exactement le même calendrier** : 1 970 séances, aucune
divergence. **Aucune ne porte de division** sur la fenêtre — le dé-ajustement de
l'expérience 8 reste implémenté mais n'a rien à corriger, Air Liquide n'ayant pas
été tirée. Le pire saut de clôture vaut **22,9 %** (Safran, mars 2020), très
en-deçà du seuil de 50 %, et il tombe le même jour que ceux d'Airbus et d'ACCOR :
un krach, pas une opération sur titre.

> **Une séance à volume nul subsiste** dans les dix séries — le 2019-12-25, et
> deux de plus pour Total. Le critère de l'expérience 3 visait les séries
> **synthétiques**, de 523 séances à volume nul ; une à trois séances sur 1 970
> est un jour férié résiduel. C'est déclaré, pas dissimulé.

Neuf valeurs sur dix sont françaises : TTF de 0,300 % à l'achat, soit 0,530 %
l'aller-retour. **Airbus en est exemptée** — 0,230 % l'aller-retour.

---

## Les sept règles

| | Énoncé | Convention retenue |
|---|---|---|
| **1** | **Isolation** | dix valeurs, aucun classement, aucun TOP |
| **2** | **Cadence hebdomadaire** | décision à la clôture de la dernière séance de la semaine civile, exécution à l'ouverture suivante |
| **3** | **Achat à 10 %** | clôture `< VAL_120 − 1 s₁₂₀` **et** `TAUX_20 ≥ 0`, valeur non détenue |
| **4** | **Nouvel achat à 10 %** | seuil figé à `clôture de la décision − 1 s₁₂₀`, **une fois** par position |
| **5** | **Vente** | clôture `> VAL_120 + 1 s₁₂₀` ; vend toute la position |
| **6** | **Renforcement à 20 %** | **une fois** par position, à la décision suivant l'achat |
| **7** | ⚠️ **Vente si le repli atteint −15 %** | **la nouveauté** — conventions ci-dessous |

### Les quatre conventions de la règle 7, déclarées

| | Convention |
|---|---|
| **Depuis quel prix** | le **prix d'exécution de la première tranche**, **figé à l'achat**. Les renforts des règles 4 et 6 **ne déplacent pas** le seuil — celui-ci ne suit ni le prix moyen ni le plus haut |
| **À quel rythme** | constaté à **chaque clôture quotidienne**, exécuté à l'**ouverture suivante**. C'est une **entorse déclarée à la règle 2** : un garde-fou regardé une fois par semaine ne protège pas |
| **Après la coupe** | **carence de quatre décisions hebdomadaires** avant que la règle 3 puisse racheter cette valeur — sans quoi on rachèterait le vendredi ce qu'on vient de couper |
| **En cas de conflit** | la **règle 7 l'emporte** sur les règles 4 et 6 le même jour. On ne renforce pas une ligne que l'on coupe |

Le seuil se lit sur la **série ajustée**, comme tout ce que la règle calcule.

---

## Les deux conventions héritées de l'expérience 9

> **Le capital.** 10 % du portefeuille par valeur (20 % pour la règle 6),
> dimensionné sur la valeur totale **avant tout ordre de la séance**. **Aucun
> ordre ne peut porter la part investie au-delà de 100 %** : pas de levier. Un
> ordre que les espèces ne financent pas est réduit, et refusé s'il n'atteint pas
> un titre.

> **L'ordre de service.** Les ventes d'abord — elles financent —, puis les achats
> par **écart le plus négatif**. La règle 7 passe avant tout le reste.

---

## Les deux références, et l'alpha officiel

| Référence | Ce qu'elle mesure |
|---|---|
| **Référence à exposition appariée** | le **panier équipondéré des dix**, détenu dans la proportion où le portefeuille l'était **la veille**. L'**alpha officiel** est l'écart à cette référence |
| Détention continue du panier | un dixième de la dotation sur chacune, gardé jusqu'au bout. L'écart est l'**écart brut**, publié mais non concluant |

---

## Le dimensionnement, publié avant la fenêtre jouée

Mesuré sur l'**étalonnage 2019-2021 seul**, sans lire une séance postérieure au
2021-12-31. **133 décisions**, du 2019-06-21 au 2021-12-31, soit **1 330
évaluations**.

| Variante | Base 100 | Appariée | **Alpha officiel** | EMD | Ordres | Frais | Part investie | Maximum |
|---|---|---|---|---|---|---|---|---|
| **Déclarée** — règles 4, 6 et 7 | 126,01 | 113,63 | **+12,37 pt** | ± 8,0 | 76 | 268,10 € | 26,20 % | 99,9 % |
| **Sans la règle 7** — la règle de l'expérience 9 | 123,01 | 115,25 | **+7,77 pt** | ± 11,2 | 75 | 257,80 € | 33,84 % | 100,0 % |
| Sans la règle 4 | 119,09 | 111,47 | +7,62 pt | ± 6,3 | 61 | 196,95 € | 21,70 % | 94,7 % |
| Sans la règle 6 | 120,90 | 111,03 | +9,87 pt | ± 6,3 | 71 | 219,83 € | 21,87 % | 77,5 % |
| Ni la règle 4 ni la 6 | 112,72 | 106,17 | +6,55 pt | ± 4,5 | 56 | 142,41 € | 16,93 % | 57,0 % |

| Grandeur, étalonnage | Valeur |
|---|---|
| Détention continue du panier | 130,39 |
| Tracking error contre l'appariée · **EMD** | 4,10 %/an · **± 8,0 pt** |
| Évaluations **sous le bord bas** · dont `TAUX_20 ≥ 0` | 309 sur 1 330 · **58** |
| Évaluations **au-dessus du bord haut** | 289 sur 1 330 |
| **Règle 7 déclenchée** | **5** |
| … dont la règle 4 aurait renforcé la même semaine | **1** |
| Achats bloqués par la carence | **1** |
| Règle 4 · règle 6 possibles · exécutées | 15 · 5 — toutes exécutées |
| Ordres refusés faute d'espèces | 0 |
| Positions ouvertes · closes · **coupées par la règle 7** | 29 · 27 · **5** |

> ⚠️ **Cet étalonnage a été corrigé une fois, avant de jouer la fenêtre, et voici
> pourquoi.** Le premier simulateur n'armait la carence que lorsque la coupe
> tombait un jour de décision ; or la règle 7 se constate à **chaque clôture**, et
> quatre de ses cinq coupes tombent un mardi ou un mercredi. La carence était donc
> inopérante dans presque tous les cas. Le défaut a été trouvé par le moteur
> lui-même, qui a refusé de retrouver les nombres publiés.
>
> Ce qui change : **1 achat bloqué** au lieu de 0, donc une position de moins
> (29 au lieu de 30), deux ordres de moins, et un alpha de **+12,37** au lieu de
> +12,45. **Les cinq coupes et leurs contrefactuels sont inchangés.**
>
> Corriger un étalonnage n'est légitime que parce que **rien n'était encore
> publié ni joué**, et que la cause est un **défaut de calcul identifié**, non une
> divergence de mesure. Après la fenêtre jouée, ce même écart ne se corrigerait
> pas : il se publierait.

### ⚠️ Ce que l'étalonnage dit de la règle 7, et qu'il faut lire avant les résultats

**1. Elle n'a été éprouvée que sur un seul épisode de marché.** Quatre de ses
cinq déclenchements tombent entre le 26 février et le 13 mars 2020 — le krach
Covid. Le cinquième est Cap Gemini, en octobre 2020. **Un garde-fou testé sur un
seul krach n'est pas testé.**

**2. Elle ne borne pas la perte à −15 %.** Le repli est constaté en clôture et
exécuté à l'ouverture suivante : en mars 2020, ENGIE sort après un repli de
**−30,75 %** et réalise **−21,25 %**. Sur les cinq coupes, le repli réalisé va de
−10,06 % à **−21,25 %**, médiane −16,26 %. Le seuil déclenche à −15 %, il ne
protège pas à −15 %.

**3. Et surtout : les cinq coupes ont coûté de l'argent.** Voici ce que chaque
ligne coupée serait devenue si la règle 7 n'avait pas existé — même achat, même
date :

| Valeur | Achat | Coupée le | Réalisé | Sans la règle 7 |
|---|---|---|---|---|
| `TTE.PA` | 2020-01-20 | 2020-02-26 | −14,64 % | vente au 2020-05-25, **−29,37 %** — *bonne coupe* |
| `MC.PA` | 2020-02-24 | 2020-03-13 | −17,69 % | vente au 2020-05-25, **−6,99 %** |
| `EN.PA` | 2020-03-02 | 2020-03-11 | −10,78 % | vente au 2020-06-01, **−17,32 %** — *bonne coupe* |
| `ENGI.PA` | 2020-03-02 | 2020-03-12 | −21,25 % | vente au 2020-06-01, **−12,54 %** |
| `CAP.PA` | 2020-09-07 | 2020-10-27 | −9,30 % | vente au 2020-12-21, **+2,67 %** |

**Trois coupes sur cinq sont mauvaises**, et le cumul est défavorable :
**−1 512,71 €** avec la règle 7 contre **−1 304,35 €** sans elle, soit
**208 € perdus** par la protection elle-même.

> **D'où vient alors le gain d'alpha de +4,60 points ?** Pas de la protection —
> elle coûte 208 €. Il vient de ce que la règle 7 **réduit l'exposition au pire
> moment du krach** : la part investie tombe de 33,84 % à 26,20 %, et cinq lignes
> quittent le marché entre le 26 février et le 13 mars 2020. L'alpha se mesurant
> **contre l'exposition appariée**, une sortie qui coûte en euros peut rapporter
> en points — c'est ce qui se produit ici. **Le mérite apparent de la règle 7
> n'est pas celui qu'on lui prête**, et l'expérience doit être lue en le sachant.
>
> Ce mérite tient d'ailleurs à **un seul krach**. Rien ne dit qu'il se
> reproduise, et la fenêtre jouée est là pour l'éprouver.

---

## Les issues déclarées

Comme en expérience 9 : le **rendement du cours sur les 20 séances suivant la
décision**, sur un sous-échantillon d'une décision sur quatre, et des intervalles
**par grappes de dates** — la date est l'unité, jamais la valeur, puisque les dix
observations d'un même jour partagent le marché de ce jour.

| Élément | Groupe testé | Témoin |
|---|---|---|
| **Règle 3, bande** | évaluations sous le bord bas | les autres |
| **Règle 3, pente** | sous le bord bas et `TAUX_20 ≥ 0` | sous le bord bas et `TAUX_20 < 0` |
| **Règle 5, bande haute** | évaluations au-dessus du bord haut | les autres |
| **Règle 7, seuil** | évaluations dont le repli dépasse −15 % | sous le bord bas, repli moindre |

---

## Les deux contrôles de reproduction

| Contrôlé — le moteur s'arrête sinon | Résultat |
|---|---|
| la permutation se rejoue depuis la graine 10 et redonne `univers.csv` | — |
| les **évaluations** d'`ENGI.PA` et `SAF.PA` coïncident avec celles de l'expérience 9 | **490 comparées, 0 écart** |

Les évaluations ne dépendent pas du portefeuille : elles **doivent** coïncider.
Les quantités et les dates d'ordre, elles, ne le peuvent pas — le portefeuille
diffère, comme l'expérience 9 le déclarait déjà face à l'expérience 8.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| [`univers.csv`](univers.csv) | les 40 valeurs dans l'ordre du tirage, leur rang, et le motif des trois rejets |
| `bilan.md` | le bilan de la fenêtre jouée |
| `rapports/2022.md` … `2026.md` | un journal par année |
| [`journal.md`](journal.md) · `journal.py` | le miroir d'exécution, puis le moteur |
| `decisions.csv` | une ligne par (décision, valeur) : bandes, écart, taux, seuils, signal |
| `ordres.csv` · `positions.csv` | les ordres et les positions, avec leur motif de sortie |
| `portefeuille.csv` | la valorisation quotidienne, et les deux références |
| `issues.csv` | les quatre issues déclarées, leur grappe de date et le sous-échantillon |
| `graphiques/{TICKER}/canal-{DATE}.svg` | la figure de canal, rangée par valeur |
| `graphiques/portefeuille-{ANNEE}.svg` | la courbe du portefeuille et de ses deux références |

**Aucun texte n'est rédigé à la main** : tous les chiffres sortent du moteur.

---

## Ce que l'expérience 10 ne fait pas

- **Aucun levier, aucune couverture, aucune vente à découvert.**
- **Aucun seuil ajusté après coup** : −15 % est publié ici, et ne bougera pas.
- **Aucune mesure de la dispersion du tirage** ni de la sensibilité au seuil :
  faire varier −15 % jusqu'à trouver mieux serait la faute que ce protocole
  s'interdit.
- **Aucune prédiction de cours, aucun conseil en investissement.**

## Pour aller plus loin

- [L'expérience 9](../experience_9/README.md) — les six règles, et l'analyse des replis d'où sort le seuil de −15 %
- [L'expérience 8](../experience_8/README.md) — la règle 4, qui renforce là où la règle 7 coupe
- [L'analyse des pertes de l'expérience 3](../experience_3/pistes-pertes.md) — où un ordre stop a déjà été mesuré, et réfuté
- [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md) · [Semestre 3 · canal](../../../raw/concept/semestre3/canal/README.md)
