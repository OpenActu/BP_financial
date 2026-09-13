# Expérience 11 — les six règles seules, sans la coupe à −15 %

Le portefeuille de l'[expérience 10](../experience_10/README.md), **à l'identique**
— mêmes dix valeurs, même tirage, même dimensionnement, même fenêtre — mais
**sans la règle 7**. Six règles, décision hebdomadaire, du 3 janvier 2022 au
10 septembre 2026.

---

## ⚠️ Ce que cette expérience est, et ce qu'elle n'est pas

> **Elle ne prédit rien, et ne peut rien prédire.** Son résultat était **déjà
> calculé et déjà publié** avant qu'une ligne de ce protocole soit écrite : c'est
> la variante « sans la règle 7 » du [bilan de l'expérience
> 10](../experience_10/bilan.md#5-ce-quajoute-chaque-règle), commit `7fef344`.
> Base 118,29, alpha officiel −9,77 point.
>
> Prétendre le contraire — publier un dimensionnement « avant la fenêtre jouée »,
> puis dévoiler un résultat que je connais — serait une mise en scène, et
> exactement le premier des [cinq pièges de
> l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md). Le chiffre est
> donc **donné d'emblée, en tête de ce protocole**, et non ménagé pour la fin.

**Ce qu'elle apporte, et que l'expérience 10 n'apportait pas.** Là-bas, cette
règle tenait en **une ligne de tableau**. Ici elle est dépliée : ses 41 positions
une par une, ses cinq journaux annuels, sa répartition par valeur, ses issues par
grappes de dates, ses figures de canal. Et surtout, une **comparaison position
par position** avec l'expérience 10, qui montre ce que la règle 7 a déplacé
au-delà de ses neuf coupes.

**Ce qu'elle ne peut pas établir** : rien de nouveau sur la performance. Une
mesure republiée n'est pas une mesure indépendante, et l'effet minimal détectable
reste de ± 9,2 points.

---

## Le résultat, donné d'emblée

| | Sans la règle 7 — **cette expérience** | Avec elle — [expérience 10](../experience_10/bilan.md) |
|---|---|---|
| Portefeuille | **118,29** | 99,14 |
| Référence à exposition appariée | 128,06 | 112,90 |
| **Alpha officiel** | **−9,77 pt** | −13,77 pt |
| Effet minimal détectable | ± 9,2 pt | ± 8,2 pt |
| Écart brut à la détention | −58,62 pt | −77,77 pt |
| Ordres · frais | 112 · 387,26 € | 116 · 345,30 € |
| Part investie moyenne · maximum | 35,01 % · 99,9 % | 30,28 % · 99,9 % |
| Positions · closes · ouvertes | 41 · 38 · 3 | 43 · 40 · 3 |
| Ordres refusés faute d'espèces | **11** | 1 |

> **L'alpha dépasse son effet minimal détectable, et il est négatif.** Comme en
> [expérience 9](../experience_9/README.md), la règle à six énoncés fait moins
> bien que sa propre exposition. Retirer la règle 7 récupère 4,00 points d'alpha
> sans rendre la règle bonne pour autant.

Deux effets de second ordre, qui ne se lisaient pas dans l'expérience 10 :

- **les frais sont plus élevés sans la règle 7** — 387,26 € contre 345,30 € — pour
  *moins* d'ordres (112 contre 116). Une coupe précoce solde une ligne avant
  qu'elle n'appelle d'autres tranches, et une vente ne paie pas la TTF ;
- **onze ordres sont refusés faute d'espèces**, contre un seul avec la règle 7 :
  sans coupe, le portefeuille reste investi à 35 % et manque plus souvent de
  liquidités au moment où un signal se présente.

---

## Les six règles — inchangées

| | Énoncé | Convention retenue |
|---|---|---|
| **1** | **Isolation** | les dix mêmes valeurs, aucun classement, aucun TOP |
| **2** | **Cadence hebdomadaire** | décision à la clôture de la dernière séance de la semaine civile, exécution à l'ouverture suivante |
| **3** | **Achat à 10 %** | clôture `< VAL_120 − 1 s₁₂₀` **et** `TAUX_20 ≥ 0`, valeur non détenue |
| **4** | **Nouvel achat à 10 %** | seuil figé à `clôture de la décision − 1 s₁₂₀`, **une fois** par position |
| **5** | **Vente** | clôture `> VAL_120 + 1 s₁₂₀` ; vend toute la position |
| **6** | **Renforcement à 20 %** | **une fois** par position, à la décision suivant l'achat |
| ~~7~~ | ~~vente si le repli atteint −15 %~~ | **retirée** — c'est l'objet de cette expérience |

La règle 5 redevient donc **la seule sortie**, comme en expériences 8 et 9 : une
position qui ne revient pas dans sa bande reste ouverte indéfiniment. Il n'y a
plus ni seuil de repli, ni carence de rachat.

Les deux conventions héritées sont inchangées : **10 % du portefeuille par
valeur** (20 % pour la règle 6), dimensionnés sur la valeur totale avant tout
ordre, **aucun levier** ; et l'ordre de service par **écart le plus négatif**, les
ventes passant d'abord.

---

## L'univers — identique, et revérifié

Les dix valeurs sont celles de l'expérience 10, issues du même tirage :
population des **40** valeurs du CAC 40 au 2019-01-02, ordre canonique par ISIN
croissant, permutation par `random.Random(10)`, dix premières recevables.

**ENGIE, ACCOR, BOUYGUES, Total, Safran, Airbus, Publicis, SAINT-GOBAIN, LVMH,
Cap Gemini.** Trois valeurs tirées ont été écartées sur leurs seules données —
Vivendi (rang 4, scissions non répercutées), Technip (rang 9) et Unibail
(rang 11), faute de série en euros.

[`univers.csv`](univers.csv) est le même fichier, et le moteur **rejoue la
permutation à chaque exécution** : il s'arrête si le fichier en diffère. Airbus,
société néerlandaise, reste **exemptée de TTF**.

---

## L'étalonnage 2019-2021, recalculé sans la règle 7

L'expérience 10 publiait quatre variantes, mais ses variantes « sans la règle 4 »
et « sans la règle 6 » **gardaient la règle 7**. Les trois dernières lignes
ci-dessous sont donc nouvelles : elles n'existaient nulle part.

**133 décisions**, du 2019-06-21 au 2021-12-31, soit **1 330 évaluations**.

| Variante | Base 100 | Appariée | **Alpha officiel** | EMD | Ordres | Frais | Part investie | Maximum |
|---|---|---|---|---|---|---|---|---|
| **Déclarée** — règles 4 et 6 | 123,01 | 115,25 | **+7,77 pt** | ± 11,2 | 75 | 257,80 € | 33,84 % | 100,0 % |
| Sans la règle 4 | 120,82 | 116,07 | +4,76 pt | ± 7,8 | 61 | 198,19 € | 25,98 % | 95,8 % |
| Sans la règle 6 | 120,37 | 112,93 | +7,44 pt | ± 9,3 | 72 | 222,85 € | 28,64 % | 95,1 % |
| Ni la règle 4 ni la 6 | 111,92 | 107,08 | +4,84 pt | ± 5,5 | 56 | 141,82 € | 20,17 % | 57,1 % |

| Grandeur, étalonnage | Valeur |
|---|---|
| Détention continue du panier | 130,39 |
| Tracking error contre l'appariée · **EMD** | 5,71 %/an · **± 11,2 pt** |
| Évaluations **sous le bord bas** · dont `TAUX_20 ≥ 0` | 309 sur 1 330 · **58** |
| Évaluations **au-dessus du bord haut** | 289 sur 1 330 |
| Règle 4 · règle 6 possibles | 16 · 5 |
| Ordres refusés faute d'espèces | **2** |
| Positions ouvertes · closes · encore ouvertes | 29 · 27 · 2 |

> **Un compteur qui se lit de travers, et qu'il faut donc expliquer.**
> Dans la variante « sans la règle 4 », `règle 4 possible` vaut **89** et non 16.
> Ce n'est pas une anomalie : le compteur mesure les semaines où la règle *aurait
> pu* jouer. Quand elle joue, elle est marquée faite et cesse d'être comptée ;
> quand elle est désactivée, la position reste sous son seuil semaine après
> semaine et **chaque semaine est recomptée**. Les deux nombres ne mesurent donc
> pas la même chose, et seul celui de la variante déclarée — **16** — est un taux
> de déclenchement.

> **Ce que l'étalonnage montre déjà.** L'ordre des variantes est le même qu'en
> [expérience 9](../experience_9/README.md) : la règle 4 et la règle 6 **ajoutent
> de l'exposition et des frais** — part investie de 20,17 % à 33,84 %, frais de
> 141,82 € à 257,80 € — pour un alpha qui ne les suit pas. Aucun de ces écarts ne
> dépasse son EMD.

---

## Les issues déclarées

Identiques à celles de l'expérience 9 : le **rendement du cours sur les 20 séances
suivant la décision**, sur un sous-échantillon d'une décision sur quatre, avec des
intervalles **par grappes de dates** — la date est l'unité, jamais la valeur.
L'issue « règle 7, seuil » de l'expérience 10 **disparaît**, faute de règle 7.

| Élément | Groupe testé | Témoin |
|---|---|---|
| **Règle 3, bande** | évaluations sous le bord bas | les autres |
| **Règle 3, pente** | sous le bord bas et `TAUX_20 ≥ 0` | sous le bord bas et `TAUX_20 < 0` |
| **Règle 5, bande haute** | évaluations au-dessus du bord haut | les autres |

---

## Les trois contrôles de reproduction

| Contrôlé — le moteur s'arrête sinon | Portée |
|---|---|
| la permutation se rejoue depuis la graine 10 et redonne `univers.csv` | le tirage |
| les évaluations d'`ENGI.PA` et `SAF.PA` coïncident avec l'[expérience 9](../experience_9/README.md) | 490 comparaisons |
| ⚠️ **les 112 ordres sont identiques, un par un, à la variante « sans la règle 7 » de l'expérience 10** | date, valeur, sens, quantité, prix |

Le troisième est **le contrôle le plus strict du dépôt à ce jour**, et il n'est
possible que parce que cette expérience est rigoureusement la même simulation :
même univers, même dimensionnement, même fenêtre, même portefeuille. Là où
l'expérience 9 ne pouvait comparer que des **dates** à l'expérience 8 — les
quantités dépendant d'un portefeuille différent —, ici **les quantités elles-mêmes
doivent coïncider**. Un seul ordre qui diffère arrête le moteur.

---

## La comparaison position par position avec l'expérience 10

Le bilan publie ce que la règle 7 a déplacé, et le fait est net : **les 41 achats
de cette expérience se retrouvent tous à l'identique dans l'expérience 10**, qui
n'en compte que deux de plus.

La règle 7 n'a donc **pas décalé les entrées** — elle n'a fait que modifier neuf
sorties et autoriser deux rachats après purge de sa carence. C'est ce qui rend la
comparaison lisible : à entrées égales, tout l'écart de 4,00 points d'alpha tient
aux **sorties**.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| [`univers.csv`](univers.csv) | les 40 valeurs dans l'ordre du tirage, et le motif des trois rejets |
| `bilan.md` | le bilan de la fenêtre jouée, et la comparaison avec l'expérience 10 |
| `rapports/2022.md` … `2026.md` | un journal par année |
| [`journal.md`](journal.md) · `journal.py` | le miroir d'exécution, puis le moteur |
| `decisions.csv` | une ligne par (décision, valeur) : bandes, écart, taux, seuil, signal |
| `ordres.csv` · `positions.csv` | les ordres et les positions, avec leur motif de sortie |
| `portefeuille.csv` | la valorisation quotidienne, et les deux références |
| `issues.csv` | les trois issues déclarées, leur grappe de date et le sous-échantillon |
| `graphiques/{TICKER}/canal-{DATE}.svg` | la figure de canal, rangée par valeur |
| `graphiques/portefeuille-{ANNEE}.svg` | la courbe du portefeuille et de ses deux références |

**Aucun texte n'est rédigé à la main** : tous les chiffres sortent du moteur.

---

## Ce que l'expérience 11 ne fait pas

- **Aucun levier, aucune couverture, aucune vente à découvert, aucun ordre stop.**
- **Aucune prédiction** : son résultat était publié avant elle, et le dit.
- **Aucune mesure indépendante de la performance** : republier un nombre ne le
  confirme pas.
- **Aucune prédiction de cours, aucun conseil en investissement.**

## Pour aller plus loin

- [L'expérience 10](../experience_10/README.md) — la même règle plus la coupe à −15 %, et ce qu'elle a coûté
- [L'expérience 9](../experience_9/README.md) — les six règles sur cinq valeurs
- [L'expérience 8](../experience_8/README.md) — la règle 4, qui renforce à la baisse là où la règle 7 coupait
- [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md) · [Semestre 3 · canal](../../../raw/concept/semestre3/canal/README.md)
