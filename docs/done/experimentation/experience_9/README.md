# Expérience 9 — les mêmes six règles, sur cinq valeurs tirées au sort

Un portefeuille de **10 000 €** conduit par la règle à six énoncés de
l'[expérience 8](../experience_8/README.md), **inchangée**, mais appliquée à
**cinq valeurs** au lieu d'une : Air Liquide, plus **quatre tirées au hasard**
dans le CAC 40 tel qu'il était composé le 2 janvier 2019.

La décision reste hebdomadaire, du 3 janvier 2022 au 10 septembre 2026.

> **L'objet déclaré.** L'expérience 8 n'a pas pu juger sa règle : avec **1,39 %
> de part investie moyenne**, son alpha était indiscernable de zéro par
> construction, quel que soit son résultat. L'expérience 9 ne change pas la
> règle — elle change **l'exposition**, en multipliant par cinq le nombre de
> valeurs où le signal peut naître. Sur l'étalonnage, la part investie passe de
> 6,78 % à **21,74 %**. C'est la seule façon de rendre l'alpha mesurable sans
> toucher à ce qu'on mesure.

---

## ⚠️ Ce que cette expérience ne pourra pas établir

1. **Elle reste de catégorie B.** Les six règles sont celles de l'expérience 8,
   proposées en connaissant les sept expériences précédentes, et sa fenêtre
   contient 2022, année déjà jouée cinq fois.
2. **Cinq valeurs ne sont pas un univers.** Le tirage corrige le choix
   arbitraire d'Air Liquide, il ne fait pas de ces cinq valeurs un échantillon
   représentatif du CAC 40. Quatre tirages de quatre valeurs donneraient quatre
   résultats différents, et **cette dispersion n'est pas mesurée ici**.
3. **L'effet minimal détectable reste plus grand que l'effet cherché.** Sur
   l'étalonnage, la tracking error contre la référence appariée vaut 3,39 %/an,
   soit un EMD de **± 6,6 points**. Un alpha de deux ou trois points ne serait
   pas tranché.

> **Ce qu'elle peut établir** : les **taux de déclenchement** sur 665 évaluations
> au lieu de 133, les **frais** — exacts —, ce que la diversification fait à
> l'**exposition**, et si l'ordre de service par l'écart le plus négatif sature
> jamais le plafond d'espèces.

---

## Le tirage, et la règle qui l'encadre — déclarée avant de tirer

L'énoncé demande « quatre autres sociétés du CAC 40 prises au hasard ». Un
tirage que l'on recommencerait jusqu'à ce qu'il plaise ne serait pas un tirage :
tout ce qui suit a donc été **fixé avant de connaître le moindre nom**.

| | Convention |
|---|---|
| **Population** | le CAC 40 **à sa composition du 2019-01-02**, lue sur [`bnains.org`](https://www.bnains.org/archives/histocac/compocac.php) — 40 valeurs, moins Air Liquide, soit **39 candidates** |
| **Ordre canonique** | les 39 triées par **code ISIN croissant**, pour que le tirage ne dépende pas de l'ordre d'affichage de la source |
| **Permutation** | `random.Random(9).shuffle()` — **graine 9**, le numéro de l'expérience |
| **Sélection** | les **quatre premières recevables** dans l'ordre de la permutation |
| **Date de la composition** | 2019-01-02, **avant** la fenêtre d'étalonnage comme avant la fenêtre jouée : aucun regard en avant, et aucun biais du survivant |

La composition est prise **au début de la série**, et non à l'entrée de la
fenêtre jouée : une valeur tirée qui quitterait l'indice en cours de route est
**gardée** — la règle 1 isole cinq valeurs, elle ne suit pas un indice.

### La recevabilité, déclarée elle aussi avant le tirage

Une candidate est écartée, et **remplacée par la suivante de la permutation**,
si l'une de ces conditions manque. Ce sont les contrôles de l'[expérience
3](../experience_3/README.md#lunivers--tout-le-cac-40-à-sa-composition-du-jour),
plus un :

1. le fournisseur sert une **série en euros** ;
2. la série est **complète** du 2019-01-02 au 2026-09-10 et son **volume est
   strictement positif** — une série synthétique n'est pas un cours ;
3. ⚠️ **aucun saut de clôture supérieur à 50 % en une séance sans division
   déclarée.** Un tel saut est une **opération sur titre** que la série
   n'enregistre pas.

> **Pourquoi ce troisième contrôle, et pourquoi à 50 %.** Une scission distribue
> à l'actionnaire les titres d'une **autre** société. Le fournisseur ne la
> répercute pas : la série encaisse la chute sans jamais créditer ce qui a été
> reçu, et fabrique une perte que le porteur n'a pas subie. C'est exactement le
> vice de l'indice nu comparé à un indice en rendement total, l'invariant le plus
> lourd du dépôt. Le seuil de 50 % sépare ce cas des mouvements de marché : les
> six séances de Safran à plus de 15 % en mars 2020 sont le krach Covid, et
> ENGIE décroche de 17,2 % **le même jour** — deux valeurs qui tombent ensemble
> sont un marché, pas une opération sur titre.

### Ce que le tirage a donné

| Rang | Valeur | Verdict |
|---|---|---|
| 1 | **Vivendi** (`VIV.PA`) | ⚠️ **écartée** — voir ci-dessous |
| 2 | **Kering** (`KER.PA`) | retenue |
| 3 | **Orange** (`ORA.PA`) | retenue |
| 4 | **Safran** (`SAF.PA`) | retenue |
| 5 | **ENGIE** (`ENGI.PA`) | retenue, en remplacement de Vivendi |

Les rangs 6 à 39 n'ont **jamais été examinés** : la règle s'arrête dès que
quatre valeurs sont retenues. L'ordre complet de la permutation est figé dans
[`univers.csv`](univers.csv), avec le rang de chaque candidate, pour que le
tirage se rejoue et se vérifie.

> **Vivendi, écartée sur les données et non sur un résultat.** Le 2024-12-09, la
> clôture perd **77,8 %** et **aucune division n'est déclarée** ; le 2021-09-21,
> elle perd 17,0 %. Ce sont les distributions d'Universal Music Group, puis de
> Canal+, Havas et Louis Hachette. La signature est sans appel : le 2024-12-09,
> le titre **ouvre à 1,896 €** quand il avait clôturé à **8,595 €** la veille —
> il n'a jamais coté entre les deux, et le volume vaut quatre fois sa médiane.
>
> **Aucune règle n'a été jouée sur Vivendi avant de l'écarter** : le motif est un
> contrôle de recevabilité des données, mesurable sans simuler quoi que ce soit,
> donc de catégorie A.

### Ce que les cinq valeurs ont en commun, et ce qui les sépare

Les cinq séries partagent **exactement le même calendrier** : 1 970 séances du
2019-01-02 au 2026-09-10, aucune séance manquante chez l'une et présente chez
l'autre. Une seule porte des divisions : **Air Liquide**, ses quatre attributions
d'actions gratuites de 1,1 (2019-10-07, 2022-06-06, 2024-06-10, 2026-06-08),
traitées comme dans l'expérience 8 — `cours réel = Close × Π(divisions
postérieures)`, titres crédités à leur date. Les quatre autres n'en ont aucune,
leur cours réel est donc leur cours ajusté.

Les cinq sont des **sociétés françaises** : la TTF de 0,300 % est due à l'achat
sur chacune. Coût inchangé, **0,530 % l'aller-retour**.

---

## Les six règles — inchangées, et ce que cinq valeurs y ajoutent

| | Énoncé | Ce que cinq valeurs changent |
|---|---|---|
| **1** | **Isolation** | cinq valeurs au lieu d'une ; **aucun classement, aucun TOP** — chacune est suivie pour elle-même |
| **2** | **Cadence hebdomadaire** | décision à la clôture de la dernière séance de chaque semaine civile, exécution à l'ouverture de la suivante — **commune aux cinq** |
| **3** | **Achat à 10 %** | 10 % du portefeuille **par valeur** ; au plus **une position ouverte par valeur**, donc jusqu'à cinq lignes |
| **4** | **Nouvel achat à 10 %** | seuil figé à l'achat, propre à chaque valeur, **une seule fois par position** |
| **5** | **Vente** | vend toute la position de **cette** valeur, tranches comprises |
| **6** | **Renforcement à 20 %** | une seule fois par position, à la décision immédiatement suivante de l'achat |

### Les deux conventions que cinq valeurs obligent à déclarer

> **Le capital.** Chaque ligne vaut **10 % du portefeuille** (20 % pour la
> règle 6), dimensionnée sur la valeur **totale avant tout ordre de la séance**.
> Cinq valeurs pleinement engagées atteindraient 200 % : **aucun ordre ne peut
> porter la part investie au-delà de 100 %.** Aucun levier, aucun découvert. Un
> ordre que les espèces ne financent pas est **réduit** à ce qu'elles permettent,
> et **refusé et compté** s'il n'atteint pas un titre.
>
> Sur l'étalonnage, **ce plafond n'a jamais mordu** : 0 refus, exposition
> maximale 57,1 %. La convention est déclarée pour ne pas être improvisée dans la
> fenêtre jouée.

> **L'ordre de service.** Quand plusieurs valeurs signalent la même semaine, les
> **ventes passent d'abord** — elles financent —, puis les achats dans l'ordre de
> l'**écart le plus négatif**, c'est-à-dire la valeur la plus enfoncée sous son
> bord bas. Départage mécanique, calculable à la date de décision, et qui ne
> regarde aucune séance postérieure.

---

## Les deux références, et l'alpha officiel

| Référence | Ce qu'elle mesure |
|---|---|
| **Référence à exposition appariée** | le **panier équipondéré des cinq**, détenu dans la proportion où le portefeuille l'était **la veille**. L'**alpha officiel** est l'écart à cette référence. |
| Détention continue du panier | un cinquième de la dotation sur chacune à la première exécution, gardé jusqu'au bout. L'écart est l'**écart brut**, publié mais non concluant. |

La référence appariée reste la seule honnête : elle neutralise l'exposition, qui
est précisément ce que cette expérience a changé. La comparer à l'expérience 8
sur l'écart brut n'aurait aucun sens — c'est la leçon de l'[expérience
6](../experience_6/README.md).

---

## Le dimensionnement, publié avant la fenêtre jouée

Tout ce qui suit est mesuré sur l'**étalonnage 2019-2021 seul**, sans lire une
séance postérieure au 2021-12-31. **133 décisions**, du 2019-06-21 au
2021-12-31, soit **665 évaluations** de valeur.

| Variante | Base 100 | Détention | Appariée | **Alpha officiel** | EMD | Ordres | Frais | Part investie | Maximum |
|---|---|---|---|---|---|---|---|---|---|
| **Déclarée** — règles 4 et 6 | 104,11 | 106,64 | 109,80 | **−5,69 pt** | ± 6,6 | 38 | 128,45 € | **21,74 %** | 57,1 % |
| Sans la règle 4 | 99,89 | 106,64 | 104,15 | −4,26 pt | ± 4,9 | 30 | 90,28 € | 16,84 % | 46,3 % |
| Sans la règle 6 | 103,35 | 106,64 | 106,01 | −2,66 pt | ± 5,3 | 36 | 108,61 € | 15,74 % | 54,3 % |
| Ni l'une ni l'autre | 99,15 | 106,64 | 100,36 | −1,21 pt | ± 2,9 | 28 | 70,05 € | 10,62 % | 29,9 % |

| Grandeur, étalonnage | Valeur |
|---|---|
| Tracking error contre la référence appariée · **EMD** | 3,39 %/an · **± 6,6 pt** |
| Tracking error contre la détention continue | 16,42 %/an · ± 32,2 pt |
| Évaluations **sous le bord bas** | **158** sur 665 |
| … **dont `TAUX_20 ≥ 0`** — les seules achetables | **20** |
| Évaluations **au-dessus du bord haut** | 160 sur 665 |
| Semaines où la **règle 4** était possible · exécutée | 8 · **8** |
| Semaines où la **règle 6** était possible · exécutée | 2 · **2** |
| Semaines où les deux l'étaient | **0** |
| Ordres **refusés faute d'espèces** | **0** |
| Positions ouvertes · closes · sorties par la règle 5 | 14 · 14 · **14** |
| Ordres par valeur | AI.PA 11 · KER.PA 9 · ENGI.PA 8 · ORA.PA 8 · SAF.PA 2 |

> **Ce que l'étalonnage dit déjà, et qu'il faut lire avant les résultats.**
>
> - **La diversification a fait ce qu'on lui demandait.** Part investie de
>   21,74 % contre 6,78 % pour l'expérience 8, 38 ordres contre 11, 14 positions
>   contre 4. La règle est enfin exposée assez pour être jugée.
> - ⚠️ **L'alpha officiel se dégrade de façon monotone à mesure qu'on ajoute les
>   règles 4 et 6** : −1,21 sans elles, −2,66 avec la seule règle 4, −4,26 avec
>   la seule règle 6, **−5,69 avec les deux**. L'expérience 8 ne pouvait pas
>   voir cet ordre — ses quatre variantes tenaient dans un point. Aucun de ces
>   écarts ne dépasse son EMD, mais **leur monotonie est un fait, et elle est
>   publiée avant la fenêtre jouée**.
> - **La pente courte reste le filtre décisif** : elle écarte **138 des 158**
>   évaluations passées sous le bord bas.
> - **Les frais ont presque doublé par rapport à l'expérience 8** en part de
>   dotation : 1,28 point contre 0,40. C'est le prix mécanique de cinq lignes.
> - **Les quatre positions d'Air Liquide sont exactement celles de l'expérience
>   8** — mêmes dates d'achat et de vente — mais **pas les mêmes quantités**,
>   parce qu'elles se dimensionnent sur un portefeuille différent. Voir le
>   contrôle de reproduction ci-dessous.

### Le contrôle de reproduction, et sa limite déclarée

L'[expérience 6](../experience_6/README.md) exigeait de sa variante `L5-P1`
qu'elle retrouve l'expérience 4 **ordre par ordre**, et s'arrêtait sinon. Ici,
**cette exigence serait fausse** : la règle 3 dimensionne en part du
portefeuille, et le portefeuille de l'expérience 9 n'est pas celui de
l'expérience 8. Les quantités diffèrent nécessairement.

Ce qui est donc contrôlé, et ce qui ne peut pas l'être :

| Contrôlé — le moteur s'arrête sinon | Non contrôlable |
|---|---|
| les **dates** de décision d'Air Liquide sont identiques à celles de l'expérience 8 | les **quantités**, qui dépendent de la valeur du portefeuille |
| la permutation du tirage se rejoue depuis la graine et redonne `univers.csv` | le **résultat** de chaque position, qui suit les quantités |

Sur l'étalonnage, les quatre positions d'Air Liquide donnent ainsi +7,82 %,
+4,58 %, **−1,92 %** et +3,28 %, contre +7,82 %, +4,58 %, −1,84 % et +3,28 % en
expérience 8 : mêmes dates, écart de 8 centièmes de point sur la troisième.

---

## Les issues déclarées

Comme en expérience 8, l'issue est le **rendement du cours sur les 20 séances
suivant la décision**, sur un **sous-échantillon sans chevauchement** — une
décision hebdomadaire sur quatre. Avec cinq valeurs, chaque décision retenue
fournit **cinq observations**, une par valeur.

> ⚠️ **Et c'est là que cinq valeurs changent la statistique.** Les cinq
> observations d'une même date **ne sont pas indépendantes** : elles partagent le
> marché du jour. C'est exactement la faute que l'[expérience
> 5](../experience_5/README.md) a corrigée. Les intervalles sont donc calculés
> **par grappes de dates** — la date est l'unité, pas la valeur.

| Élément | Groupe testé | Témoin |
|---|---|---|
| **Règle 3, bande** | évaluations sous le bord bas | les autres |
| **Règle 3, pente** | sous le bord bas et `TAUX_20 ≥ 0` | sous le bord bas et `TAUX_20 < 0` |
| **Règle 5, bande haute** | évaluations au-dessus du bord haut | les autres |

Les intervalles sont ceux de Student, par `p_valeur_student()` de
[`python/import_societe.py`](../../../../python/import_societe.md), aux degrés de
liberté que donne le **nombre de dates**, non le nombre d'observations.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| [`univers.csv`](univers.csv) | les 39 candidates dans l'ordre du tirage, leur rang, et le motif de rejet de Vivendi |
| `bilan.md` | le bilan de la fenêtre jouée |
| `rapports/2022.md` … `2026.md` | un journal par année |
| [`journal.md`](journal.md) · `journal.py` | le miroir d'exécution, puis le moteur |
| `decisions.csv` | une ligne par (décision, valeur) : bandes, écart, taux, signal |
| `ordres.csv` · `positions.csv` | les ordres et les positions, avec leur valeur et leurs tranches |
| `portefeuille.csv` | la valorisation quotidienne, et les deux références |
| `issues.csv` | les trois issues déclarées, leur grappe de date et le sous-échantillon |
| `graphiques/{TICKER}/canal-{DATE}.svg` | la figure de canal à chaque décision d'ordre, rangée par valeur |
| `graphiques/portefeuille-{ANNEE}.svg` | la courbe du portefeuille et de ses deux références |

**Aucun texte n'est rédigé à la main** : tous les chiffres des journaux sortent
du moteur.

---

## Ce que l'expérience 9 ne fait pas

- **Aucun levier, aucune couverture, aucune vente à découvert, aucun ordre stop.**
- **Aucun classement entre les cinq valeurs** : l'écart le plus négatif sert
  d'ordre de service quand les espèces manquent, jamais de critère de sélection.
- **Aucune mesure de la dispersion du tirage** : un seul tirage a été fait, et
  refaire l'expérience sur d'autres tirages est une expérience à part entière.
- **Aucune prédiction de cours, aucun conseil en investissement.**

## Pour aller plus loin

- [L'expérience 8](../experience_8/README.md) — la même règle sur une seule valeur, et pourquoi son alpha ne pouvait rien établir
- [L'expérience 5](../experience_5/README.md) — d'où vient l'intervalle par grappes de dates
- [L'expérience 6](../experience_6/README.md) — d'où vient la référence à exposition appariée
- [Semestre 3 · canal](../../../raw/concept/semestre3/canal/README.md) · [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md)
