# Expérience 8 — une seule valeur, une décision par semaine, et aucune sortie en perte

Un portefeuille de **10 000 €** sur **Air Liquide seule**, conduit par une règle à
six énoncés, décidée **une fois par semaine**, du 3 janvier 2022 au 10 septembre
2026.

C'est la première expérience du dépôt à porter sur une valeur unique, à
dimensionner ses achats **en part du portefeuille**, et à **renforcer une baisse**
au lieu de la couper : sa règle 4 achète 10 % de plus quand le cours passe 1 s
sous le prix d'achat.

---

## ⚠️ Ce que cette expérience ne pourra pas établir

1. **Elle est de catégorie B.** Ses six règles sont proposées en connaissant les
   six expériences précédentes, et sa fenêtre contient 2022, année déjà jouée
   quatre fois. Aucun de ses résultats de performance ne vaut preuve.
2. **Elle prend très peu de positions.** Sur les 133 décisions de la fenêtre
   d'étalonnage, elle a ouvert **4 positions**. La fenêtre jouée en comptera
   quelques-unes de plus.
3. **Elle est presque toujours en espèces** : part investie moyenne de **6,78 %**
   sur l'étalonnage. L'écart à la détention continue d'Air Liquide mesurerait
   donc surtout une exposition absente — c'est la leçon de l'[expérience 6](../experience_6/README.md),
   et la raison pour laquelle l'alpha officiel se mesure ici **contre une
   référence à exposition appariée**.

> **Ce qu'elle peut établir** : les **taux de déclenchement** de chaque règle, les
> **frais** — exacts —, ce que les règles 4 et 6 ajoutent en ordres, en frais et
> en exposition, et **le risque que crée l'absence de sortie en perte**.

### Le risque que la règle 4 crée, nommé avant de jouer

En inversant le stop, la règle 8 supprime **toute sortie en perte** : la seule
vente est celle de la règle 5, au bord haut. Une position qui baisse et ne revient
jamais dans sa bande reste ouverte indéfiniment, jusqu'à **40 % du portefeuille**
— 10 % par la règle 3, 10 % par la règle 4, 20 % par la règle 6. Sur
l'étalonnage, l'exposition a atteint **38,7 %**, donc ce plafond n'est pas
théorique.

Le bilan publie, pour cette raison : les **lignes jamais revendues**, le **repli
maximal** de chaque position entre son premier achat et sa sortie, et la **durée**
de chaque détention.

---

## Les six règles, telles qu'elles sont déclarées

| | Énoncé | Convention retenue |
|---|---|---|
| **1** | **Isolation** : une seule valeur, Air Liquide (`AI.PA`) | aucun univers, aucun classement, aucun TOP |
| **2** | **Cadence hebdomadaire** | décision à la **clôture de la dernière séance de chaque semaine civile**, exécution à l'**ouverture de la séance suivante** |
| **3** | **Achat à 10 %** — cours sous 1 s de `E_120`, taux `E_20 ≥ 0` | clôture `< VAL_120 − 1 s₁₂₀` **et** `TAUX_20 ≥ 0`, aucune position ouverte |
| **4** | **Nouvel achat à 10 %** — cours sous 1 s de la valeur d'achat de la règle 3 | seuil = **clôture de la décision d'achat − 1 s₁₂₀ de cette décision**, figé ; testé **aux décisions hebdomadaires** ; **une seule fois** par position |
| **5** | **Vente** — cours au-dessus de 1 s de `E_120` | clôture `> VAL_120 + 1 s₁₂₀` ; vend **toute** la position, tranches comprises |
| **6** | **Renforcement à 20 %** — cours sous 1 s, achat de la semaine précédente | **une seule fois** par position, à la décision **immédiatement suivante** de l'achat, si la clôture est encore `< VAL_120 − 1 s₁₂₀` et `TAUX_20 ≥ 0` |

**Exposition maximale : 40 %** du portefeuille. Le solde dort en espèces, sans
rémunération.

> **Cumul déclaré.** Si les règles 4 et 6 sont remplies la **même semaine**, les
> deux s'exécutent — 10 % puis 20 %, soit 30 % d'un coup —, toutes deux
> dimensionnées sur la **même** valeur de portefeuille, celle de la clôture de la
> décision, sans composition. Le cas ne s'est **jamais** présenté sur
> l'étalonnage : la convention est déclarée pour ne pas être improvisée.
>
> Les règles 4 et 6 ne peuvent jamais entrer en conflit avec la règle 5 : l'une
> exige une clôture sous le bord bas, l'autre au-dessus du bord haut.

Les bandes sont celles de toutes les expériences depuis la quatrième :
`VAL_120 ± 1 s₁₂₀`, avec
$s_{120} = \sqrt{\tfrac{120}{118}\,\texttt{VAR\_120}\,(1-\texttt{CORR\_120}^2)}$,
et $\texttt{TAUX\_20} = 100\,r_{20}/\texttt{E\_20}$. Le seuil de la règle 3 est
`≥ 0` — pas `> 0` — comme l'énoncé le demande.

### Les coûts

Courtage 0,100 %, demi-spread 0,015 %, **TTF 0,300 %** à l'achat — Air Liquide
est une société française, elle n'en est pas exemptée. Soit **0,530 %**
l'aller-retour.

---

## La donnée : une division postérieure, et comment elle est traitée

Air Liquide est l'une des trois valeurs que les expériences 3 à 6 **refusaient
d'acheter** : le fournisseur répercute rétroactivement ses attributions d'actions
gratuites, si bien que le **nombre de titres achetables** serait façonné par une
opération postérieure. Une expérience qui ne porte que sur elle ne peut pas se
contenter de ce refus.

> **Déclaration.** Les cours d'exécution et de valorisation sont **dé-ajustés des
> seules divisions** : `cours réel = Close × Π(divisions postérieures)`. Les
> quatre attributions de la fenêtre — 2019-10-07, 2022-06-06, 2024-06-10,
> 2026-06-08, chacune de 1,1 — **créditent des titres** à leur date, de sorte que
> la valeur du portefeuille reste continue. La **règle**, elle, se lit entièrement
> sur la série ajustée : bandes, écarts et seuil de la règle 4 y sont invariants
> d'échelle.

Les cours restent **ajustés des dividendes**, comme dans toutes les expériences
précédentes : `Close` est une série en rendement total, et les dividendes n'y sont
donc pas crédités en espèces une seconde fois.

**Le contrôle qui valide la dé-ajustement** : les dividendes de la colonne
`Dividends`, multipliés par le même facteur, redonnent exactement les dividendes
versés par Air Liquide — 2,65 · 2,70 · 2,75 · 2,90 · 2,95 · 3,20 · 3,30 · 3,70 €
par action de 2019 à 2026. Et la clôture du 2022-01-03 redevient **140,83 €**, le
cours réellement coté, au lieu des 105,81 € affichés après rétro-ajustement.

---

## Les deux fenêtres

| Fenêtre | Décisions | Ce qu'elle sert |
|---|---|---|
| **Étalonnage** | **133**, du 2019-06-21 au 2021-12-31 | les taux et le dimensionnement, publiés **ci-dessous, avant la fenêtre jouée** |
| **Narrée et investie** | du 2022-01-03 au 2026-09-10 | le portefeuille, les journaux annuels, le bilan |

La série commence le 2019-01-02 ; la première évaluation possible est celle du
**2019-06-21**, quand la fenêtre de 120 séances est complète.

---

## Les deux références, et l'alpha officiel

| Référence | Ce qu'elle mesure |
|---|---|
| **Référence à exposition appariée** | Air Liquide détenue dans la proportion où le portefeuille l'était **la veille**. L'**alpha officiel** est l'écart du portefeuille à cette référence. |
| Détention continue d'Air Liquide | tout investi à la première exécution, gardé jusqu'au bout. L'écart à cette référence est l'**écart brut**, publié mais non concluant. |

> ⚠️ **La précision de l'alpha officiel est trompeuse si on ne dit pas sa portée.**
> Sur l'étalonnage, sa tracking error vaut 0,40 %/an, soit un effet minimal
> détectable de ± 0,8 point — non parce que la mesure est puissante, mais parce
> que **les deux côtés sont en espèces 93 % du temps**. L'alpha officiel ne juge
> que les semaines où la règle est investie, et c'est tout ce qu'il prétend faire.

---

## Le dimensionnement, publié avant la fenêtre jouée

Tout ce qui suit est mesuré sur l'**étalonnage 2019-2021 seul**, sans lire une
séance postérieure au 2021-12-31.

| Variante | Base 100 | Appariée | **Alpha officiel** | Ordres | Frais | Part investie | Maximum |
|---|---|---|---|---|---|---|---|
| **Déclarée** — règles 4 et 6 | 100,66 | 101,71 | **−1,05 pt** | 11 | 40,29 € | 6,78 % | **38,7 %** |
| Sans la règle 4 | 100,26 | 101,21 | −0,95 pt | 9 | 30,25 € | 5,20 % | 28,8 % |
| Sans la règle 6 | 101,14 | 101,65 | −0,51 pt | 10 | 29,78 € | 4,44 % | 18,9 % |
| Ni l'une ni l'autre | 100,73 | 101,15 | −0,41 pt | 8 | 19,74 € | 2,88 % | 10,2 % |

| Grandeur, étalonnage | Valeur |
|---|---|
| Tracking error contre la référence appariée · **EMD** | 0,40 %/an · **± 0,8 pt** |
| Tracking error contre la détention continue | 21,45 %/an · ± 42,0 pt |
| Décisions passant **sous le bord bas** | **29** sur 133 |
| … **dont `TAUX_20 ≥ 0`** — les seules achetables | **6** |
| Décisions **au-dessus du bord haut** | 33 sur 133 |
| Semaines où la **règle 4** était possible · exécutée | 2 · **2** |
| Semaines où la **règle 6** était possible · exécutée | 1 · **1** |
| Semaines où les deux l'étaient | **0** |
| Positions ouvertes · closes · sorties par la règle 5 | 4 · 4 · **4** |

Les quatre positions de l'étalonnage, pour mémoire :

| Premier achat | Sortie | Tranches | Titres | Prix moyen | Résultat | Séances |
|---|---|---|---|---|---|---|
| 2019-08-05 | 2019-09-23 | 1 | 9 | 105,64 € | **+7,82 %** | 36 |
| 2019-10-28 | 2019-11-25 | 1 | 9 | 101,97 € | **+4,58 %** | 21 |
| 2020-09-14 | 2021-01-11 | **3** | 31 | 124,44 € | −1,84 % | 84 |
| 2021-08-02 | 2021-11-08 | **2** | 14 | 132,33 € | **+3,28 %** | 71 |

> **Ce que l'étalonnage dit déjà, et qu'il faut lire avant les résultats.**
>
> - **La pente courte est le filtre décisif** : elle écarte 23 des 29 semaines
>   passées sous le bord bas. Sans elle, la règle 3 se déclencherait cinq fois
>   plus souvent.
> - **L'inversion du stop change la nature des positions perdantes.** Les deux
>   positions des 2020-09-14 et 2021-08-02 sont celles qu'un stop aurait coupées à
>   −4,76 % et −3,23 % ; en moyennant à la baisse, elles ressortent par la règle 5
>   à −1,84 % et +3,28 %, après 84 et 71 séances. **Les quatre positions sortent
>   par la règle 5** : aucune n'est abandonnée.
> - **Mais le gain net est nul, et les frais doublent.** 100,66 avec les règles 4
>   et 6, 100,73 sans elles, pour 40,29 € de frais contre 19,74 €. Ce que les deux
>   règles apportent en durée de détention, elles le rendent en frais.
> - **Elles achètent surtout de l'exposition** : la part investie passe de 2,88 %
>   à 6,78 %, et le maximum de 10,2 % à 38,7 %.

---

## Les issues déclarées

Chaque élément de la règle est confronté à une issue observable : le **rendement
du cours sur les 20 séances suivant la décision**, mesuré sur un
**sous-échantillon sans chevauchement** — une décision hebdomadaire sur quatre,
soit une tous les 20 jours de bourse.

> **Pourquoi un rendement, et non un excédent.** Les expériences 3 à 6 mesuraient
> un rendement *excédentaire* contre un indice. Ici, la règle 1 impose une valeur
> unique : contre la détention continue de cette même valeur, l'excédent serait
> **identiquement nul**. L'issue est donc le rendement du titre lui-même, et ce
> sont les **groupes de décisions** qui se comparent entre eux.

| Élément | Groupe testé | Témoin |
|---|---|---|
| **Règle 3, bande** | décisions sous le bord bas | les autres |
| **Règle 3, pente** | sous le bord bas et `TAUX_20 ≥ 0` | sous le bord bas et `TAUX_20 < 0` |
| **Règle 5, bande haute** | décisions au-dessus du bord haut | les autres |

Les intervalles sont ceux de Student à `n − 1` degrés de liberté, calculés sur ce
sous-échantillon, par `p_valeur_student()` de
[`python/import_societe.py`](../../../../python/import_societe.md). Avec une
trentaine d'observations indépendantes par groupe sur la fenêtre jouée, **aucune
de ces trois comparaisons ne devrait trancher**, et c'est déclaré ici.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| `bilan.md` | le bilan de la fenêtre jouée |
| `rapports/2022.md` … `2026.md` | un journal par année |
| [`journal.md`](journal.md) · `journal.py` | le miroir d'exécution, puis le moteur |
| `decisions.csv` | une ligne par décision hebdomadaire : bandes, écart, taux, signal |
| `ordres.csv` · `positions.csv` | les ordres et les positions, avec leurs tranches |
| `portefeuille.csv` | la valorisation quotidienne, et les deux références |
| `issues.csv` | les trois issues déclarées, et le sous-échantillon |
| `graphiques/canal-AI.PA-{DATE}.svg` | la figure de canal à chaque décision d'ordre et à chaque fin d'année |
| `graphiques/portefeuille-{ANNEE}.svg` | la courbe du portefeuille et de ses deux références |

**Aucun texte n'est rédigé à la main** : ni actualités, ni notes chartistes. Tous
les chiffres des journaux sortent du moteur.

---

## Ce que l'expérience 8 ne fait pas

- **Aucun levier, aucune couverture, aucune vente à découvert, et désormais aucun
  ordre stop.**
- **Aucune diversification** : c'est l'objet de la règle 1, et cela rend la
  tracking error contre la détention continue inexploitable.
- **Aucune prédiction de cours, aucun conseil en investissement.**

## Pour aller plus loin

- [L'analyse des pertes de l'expérience 3](../experience_3/pistes-pertes.md) — où l'ordre stop, que la règle 4 inverse, a été mesuré et réfuté
- [L'expérience 6](../experience_6/README.md) — d'où vient la référence à exposition appariée
- [Semestre 3 · canal](../../../raw/concept/semestre3/canal/README.md) · [Semestre 4 · finance](../../../raw/concept/semestre4/finance/README.md)
