# Revue de l'expérience 1

Revue produite par la skill `/experience-review` : les trois agents du dépôt —
[`chartiste`](../../../../.claude/agents/chartiste.md),
[`trading`](../../../../.claude/agents/trading.md),
[`sorosien`](../../../../.claude/agents/sorosien.md) — ont relu l'expérience
chacun sous son angle, et proposé cinq pistes d'amélioration.

> Cette revue **ne modifie pas l'expérience**. Elle se pose à côté. Appliquer une
> piste, c'est une expérience suivante, avec son propre protocole déclaré avant.

---

## 1. Ce qui a été relu

| Élément | Volume |
|---|---|
| [`README.md`](README.md) — les paramètres d'entrée | univers de 12 valeurs, dotation 10 000 €, score en 5 composantes, seuils 5/7, cadence mensuelle, frais 0,530 % A/R, référence `TR12` |
| [`bilan-2022.md`](bilan-2022.md) | le compte, 14 positions, le contrefactuel, les trois conventions |
| [`rapports/`](rapports/2022-01.md) | 12 journaux mensuels |
| `graphiques/` | 12 SVG en base 100 |
| [`chartiste.md`](chartiste.md) · [`actualites.md`](actualites.md) | 144 notes de perspective · 13 sections de contexte |
| `criteres.csv` · `classement.csv` · `ordres.csv` · `portefeuille.csv` | 144 · 144 · 23 · 257 lignes |
| [`journal.py`](journal.py) · [`journal.md`](journal.md) | le moteur et son miroir |

**Le résultat relu** : 9 156,26 € au 30 décembre 2022, soit **−8,44 %** contre
**−3,94 %** pour `TR12` — un écart de **−4,50 points**. 23 ordres, 116,66 € de
frais, repli maximal −17,89 % au 29 septembre.

---

## 2. La contrainte imposée aux trois agents

L'année 2022 est **passée** et son résultat est connu de qui rédige la revue.
Proposer « il aurait fallu un seuil à 40 % » en le sachant est du
**rétro-ajustement**, pas une amélioration — c'est le premier des
[cinq pièges de l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md).
Chaque piste est donc classée :

- **Catégorie A — indépendante du résultat.** Proposable avant la première
  séance, en lisant le seul protocole : une lacune de mesure, une convention non
  déclarée, un contrôle absent, un biais non corrigé.
- **Catégorie B — suggérée par le résultat.** Recevable **si elle est nommée
  comme telle** et accompagnée du protocole qui permettrait de la tester
  honnêtement — autre période, autre univers, ou en aveugle.

**Décompte : 12 pistes A, 3 pistes B.** Chaque agent en a rendu quatre A et une
B. Une revue qui ne rendrait que des pistes B aurait relu le résultat, pas le
protocole.

---

## 3. `chartiste` — la géométrie et les signaux

> Ce que l'encadrement mesurait, et ce que le score en a gardé.

### Ce qu'il a trouvé

**Le score consomme une fraction de ce que la géométrie produit.** Les 144
encadrements ne sont pas des objets homogènes : largeur de 2,1 % à 35,6 % du
cours (médiane 12,8 %), de 2 à 7 épisodes de contact au support, τ infini dans
27 cas et inférieur à 21 séances dans 18. De tout cela le score ne retient qu'un
ternaire, `s3`, qui pèse **8 %** de la variance du score et se trouve corrélé à
**ρ = +0,62** avec `s2` : les deux tiers de ce que dit la position sont déjà dits
par la tendance courte. Ce n'est pourtant pas un figurant — retirer `s3`
déplacerait 65 rangs, 17 éligibilités et **4 des 23 ordres**.

**⚠️ `s3` a le signe inverse de la règle qu'il cite en source.** La règle du
module 3 achète **position < 35 %** et vend **> 65 %** ; le score donne `+1` à
**≥ 50 %**. Mesuré sur les ordres réellement passés : **12 achats sur 14** à une
position ≥ 35 %, donc dans la zone où la règle du dépôt interdit d'acheter ;
**4 ventes sur 9** à une position ≤ 12 %, donc sur un support, là où elle refuse
de vendre.

**L'objet mesuré ne vit pas aussi longtemps que la cadence qui le lit.** La
clôture du mois *m* tombe hors du canal du mois *m−1* prolongé dans **88 cas sur
132**, écart médian 6,3 %. La moitié des 288 droites publiées sont franchies dans
les 21 séances. Recalculé à la **veille** de chaque décision, `s3` bascule 20
fois sur 144 — record DG.PA au 31 janvier, position **83,1 % → 28,4 % en une
séance** pendant laquelle la clôture a bougé de −0,06 %. C'est l'arête retenue
qui a changé, pas le titre.

**La tolérance de contact n'est pas comparable d'un titre à l'autre.** ε = 0,25 σ
des clôtures, rapporté à la largeur du canal, va de 4 % à **101 %** — facteur 24.
Cas extrême : SAN.PA au 30 septembre, ε = 1,73 € pour un canal large de 1,72 €.
La tolérance dépasse le canal entier, et c'est cette évaluation qui a produit la
vente du 3 octobre.

**`s3` ne peut structurellement jamais signaler une rupture.** L'enveloppe étant
convexe et ancrée à droite, on a toujours support ≤ Low ≤ Close ≤ High ≤
résistance : la position reste dans [0 ; 100]. Toute la partie « ruptures » de la
charte du chartiste — date, ampleur en σ_e, persistance, volume — vit dans les
notes et n'atteint jamais le score.

### Ses cinq pistes

| # | Piste | Cat. |
|---|---|---|
| C1 | Déclarer et consigner l'objet géométrique — fenêtre et tolérance passées en argument, onze colonnes de plus dans `criteres.csv`, les 144 SVG de décision conservés au lieu d'être effacés | **A** |
| C2 | Rendre le comptage des contacts comparable — publier ε rapporté à la largeur, et un veto de dégénérescence si ε ≥ ⅓ de la largeur (4 cas sur 144) | **A** |
| C3 | Déclarer le sens de `s3`, ou l'aligner sur la règle citée en source | **A** |
| C4 | Confronter la durée de vie de l'encadrement à la cadence — publier τ, l'exigence du support (médiane +1,0 % sur l'horizon), et le taux de survie des droites | **A** |
| C5 | Tester en aveugle si c'est le bas de canal qui portait l'information — sur 2018-2019 et 2023-2024, les deux conventions en parallèle | **B** |

---

## 4. `trading` — la performance et la règle

> Ce que douze mois permettent de conclure, et ce qu'ils n'en permettent pas.

### Ce qu'il a trouvé

**Le −4,50 pt du bilan n'est pas un alpha.** C'est un écart de performance
cumulée, non corrigé du risque. Régression des 257 rendements du portefeuille sur
`TR12` :

| Grandeur | Valeur | Incertitude |
|---|---|---|
| Bêta | **0,862** | IC95 [0,814 ; 0,909] · $t(\beta-1) = -5{,}70$, $p < 10^{-4}$ |
| Alpha annualisé | **−5,18 %/an** | IC95 **[−20,2 ; +9,8] pt** · $t = -0{,}68$, $p = 0{,}50$ |
| $R^2$ · vol. résiduelle · TE · IR | 0,832 · 7,72 % · **8,17 %/an** · **−0,60** | — |

Le bêta est significativement inférieur à 1 ; l'IC95 de l'alpha est large de
**30 points** et contient zéro sans ambiguïté. Robuste à l'autocorrélation
(Newey-West, 5 et 10 retards). Corrigé du bêta, l'écart est **plus** défavorable
que le brut : −5,04 pt, la sous-exposition ayant mécaniquement rapporté +0,55 pt
dans une année de baisse.

**Le chiffre le plus important de la revue.** À une tracking error de 8,17 %/an,
l'**effet minimal détectable sur un an est de ±16,0 points**. L'écart observé est
3,6 fois trop petit pour être vu.

| Écart annuel à établir | Années nécessaires (95 %) |
|---|---|
| −4,50 pt, celui de 2022 | **12,7 ans** |
| 1,17 pt, les frais payés | **187 ans** |

**Il faudrait 187 ans de cette règle pour établir qu'elle rentabilise ses propres
frais.** Les frais, eux, se mesurent à l'euro près : 116,66 €, rotation 164,7 %/an,
freinage 1,26 % de la valeur moyenne. **Le rapport entre l'incertitude de l'alpha
et la certitude des frais est de 26 pour 1**, et il ne dépend pas de 2022.

**Le témoin que le protocole n'a pas posé.** Énumération des **792 paniers** de 5
valeurs parmi 12, tenus toute l'année sans frais : moyenne −3,73 %, écart-type de
tirage 6,04 pt, dispersion à 95 % de **±11,8 pt**. Le portefeuille de
l'expérience est au **percentile 25** ; le contrefactuel « janvier tenu » du
bilan, au **percentile 49** — rigoureusement médian, donc il ne mesure pas la
qualité de la sélection initiale.

**`s5` est un poids mort, et le constat vaut plus que la composante.** Décomposition
de la variance du score : `s1` 45,3 %, `s4` 34,5 %, `s2` 12,3 %, `s3` 7,9 %,
**`s5` 0,0 %**. Le score annoncé « entre −7 et +7 » vaut en réalité entre −6 et +6,
et il est porté à 80 % par deux composantes corrélées à +0,42 — deux lectures de
la même tendance longue. Cinq critères déclarés, **deux axes effectifs**.

**Deux écarts entre le protocole déclaré et la règle dont il se réclame** : le
sens de `s3` (voir § 3), et les **quatre vetos collectés puis ignorés**.

**Le biais du survivant n'est pas « entier ».** Le README écrit qu'il « joue en
faveur de l'expérience ». C'est vrai contre `^FCHI`, **faux contre `TR12`** : la
référence est bâtie sur les douze mêmes valeurs, donc elle porte le même biais,
qui s'annule au premier ordre dans l'écart de −4,50 pt. En revanche `TR12` est
rebalancé **sans coûts**, ce qui lui donne ~0,4 pt d'avance non gagnée.

### Ses cinq pistes

| # | Piste | Cat. |
|---|---|---|
| T1 | Dimensionner l'expérience avant de la lancer — publier la TE attendue, l'effet minimal détectable et l'horizon requis, avant la première séance | **A** |
| T2 | Mesurer l'écart comme un alpha — régression, bêta testé contre 1, IC95, TE, IR ; réserver le mot « alpha » à l'ordonnée à l'origine | **A** |
| T3 | Déclarer que le score n'est pas la règle du module 3 — sens de `s3`, vetos non appliqués avec leurs taux, poids **effectifs** du score | **A** |
| T4 | Sortir `s5` du score, la garder comme diagnostic déclaré, avec la condition de réintégration | **A** |
| T5 | Pré-enregistrer une grille de cadences — mensuelle, trimestrielle, semestrielle en parallèle, sur une période non lue | **B** |

---

## 5. `sorosien` — la réflexivité

> Le protocole revendique *L'Alchimie de la finance* et n'utilise aucun de ses
> instruments.

### Ce qu'il a trouvé

**Aucune séquence réflexive identifiable — et c'était écrivable avant la première
séance.** Passées au filtre des sept canaux par lesquels un cours peut agir sur
les fondamentaux, **onze des douze valeurs n'ont aucun canal nommable** ; la
douzième, `BNP.PA`, en a un en théorie (collatéral et crédit) et rien en 2022 ne
montre le mécanisme en marche. Un univers de méga-capitalisations autofinancées
est **par construction** le terrain le plus pauvre en réflexivité qui soit.

**Le gagnant de l'année n'est pas une boucle.** `TTE.PA` fait +33,42 % en
portefeuille. La fonction cognitive a opéré — les participants ont compris que
l'énergie était rare ; la fonction participante n'a pas opéré — acheter l'action
ne fait monter ni le prix du gaz ni les résultats. **C'est un choc exogène**, et
`actualites.md` en contient déjà l'explication complète.

**Le score est structurellement un anti-détecteur de la phase de test.** Pendant
un repli, `s2` bascule à −1 et `s3` tombe sous 20 % → −1, pendant que `s1` reste
à +2 : un test réussi coûte **jusqu'à 2 points sur 7**, au moment précis où le
cadre de Soros dit que biais et tendance se renforcent. La démonstration tient
dans le tableau des composantes du README, sans aucune donnée.

**Au changement de régime, le classement est au plus fragile et au plus mobile.**
Au 28 février, quatre séances après l'invasion, `s4` vaut +2 pour les douze
valeurs (le momentum 12-1 s'arrête avant l'invasion) et `s5` vaut 0 pour les
douze : le score n'a plus que trois composantes vivantes, sa dispersion tombe à
son minimum de l'année (σ = 1,18) — et la somme des |Δ rang| atteint **48**, son
maximum des onze transitions.

**Le volume, seule confirmation disponible, n'entre dans aucune composante.**

**Le journal écrit des thèses réfutables et n'en réfute jamais aucune.** Les 144
notes se terminent toutes par une clause du type « *une clôture sous 7,70
romprait le support ascendant* ». **Aucune n'est dépouillée le mois suivant.**
C'est le paradoxe central : l'expérience a raison d'affirmer qu'« un an, c'est un
point » pour l'alpha — mais douze mois lui ont fourni **144 énoncés datés et
vérifiables**. Ce n'est pas un point, c'est un échantillon, et elle le jette.

**⚠️ Un regard en avant dans la prose.** `actualites.md` § 2022-10, qui alimente
le préambule de la décision du 30 septembre, écrit « le CAC 40 inscrit son point
bas **annuel** le 29 septembre » — inconnaissable ce jour-là. La section 2022-07
tient au contraire la convention : « point bas annuel **provisoire** ». Sans
conséquence sur les nombres, puisque ce texte ne nourrit pas le moteur — mais
c'est précisément le problème : *un texte qui ne nourrit rien n'est pas
contraint, et un texte non contraint dérive.*

### Ses cinq pistes

| # | Piste | Cat. |
|---|---|---|
| S1 | Une fiche de canal de transmission par ticker, écrite avant l'univers — et remplacer l'exergue de Soros par une déclaration de portée | **A** |
| S2 | Mesurer que le score est un anti-détecteur de la phase de test, dans un **journal parallèle** jamais substitué au principal | **A** |
| S3 | Publier le volume relatif en mesure rapportée, non en composante — en déclarant que la fenêtre 20/250 est trop plate pour discriminer | **A** |
| S4 | Un registre daté de thèses réfutables, **dépouillé chaque mois** — biais dominant contre tendance sous-jacente, et le verdict des 144 clauses | **A** |
| S5 | Registre des séquences réflexives **hors univers** — gilts de septembre, appels de marge gaziers | **B** |

---

## 6. Synthèse

### Les quinze pistes

| # | Piste | Cat. | Touche l'exécution ? |
|---|---|---|---|
| C1 | Déclarer et consigner l'objet géométrique | A | non |
| C2 | Rendre le comptage des contacts comparable | A | marginalement (4 cas) |
| C3 | Déclarer le sens de `s3`, ou l'aligner | A | **oui** |
| C4 | Durée de vie de l'encadrement contre cadence | A | partiellement |
| T1 | Dimensionner l'expérience avant de la lancer | A | non |
| T2 | Mesurer l'écart comme un alpha, avec bêta et IC | A | non |
| T3 | Déclarer que le score n'est pas la règle du module 3 | A | non |
| T4 | Sortir `s5` du score | A | non — effet **exactement nul** |
| S1 | Fiche de canal par ticker, et déclaration de portée | A | non |
| S2 | Journal parallèle mesurant l'anti-détection de la phase de test | A | non |
| S3 | Le volume en mesure rapportée | A | non |
| S4 | Registre de thèses réfutables, dépouillé chaque mois | A | non |
| C5 | Tester en aveugle le sens de la position | **B** | non |
| T5 | Grille de cadences pré-enregistrée | **B** | par construction |
| S5 | Registre des séquences réflexives hors univers | **B** | non |

**Douze pistes A, trois pistes B.** Onze des quinze ne touchent pas l'exécution :
ce sont des lacunes de **déclaration et de mesure**, pas de règle.

### Là où les agents convergent

Trois constats ont été trouvés indépendamment par au moins deux agents. Ils
valent plus qu'une piste isolée.

1. **Le sens de `s3` est inversé par rapport à la règle citée en source**
   (`chartiste` C3, `trading` T3). Vérifié : `generer_graph_decision.py:240`
   achète sous 35 %, le score donne +1 au-dessus de 50 %. **12 achats sur 14** ont
   eu lieu dans la zone d'achat interdite par la règle dont le README se réclame.
   C'est le défaut le plus net de la revue, et il était lisible avant la première
   séance.
2. **Les quatre vetos sont calculés puis jetés** (`chartiste`, `trading`).
   Recompté : veto 1 dans **75/144**, veto 3 dans **41/144**, veto 2 dans
   **17/144**, 41 lignes sans veto, 30 lignes cumulant au moins deux vetos. Le
   verdict de la règle du dépôt est **`ATTENTE` aux 144 évaluations** — et
   l'expérience a passé 23 ordres. Ce n'est pas illégitime, c'est une autre
   règle : le README ne le dit nulle part.
3. **Le score déclare cinq composantes et n'en fait vivre que deux**
   (`trading` T4, `chartiste` C1, `sorosien` S2). `s5` pèse 0,0 % de la variance,
   `s3` 7,9 %, et `s1`+`s4` — deux lectures de la même tendance longue, corrélées
   à +0,42 — en portent 80 %.

Une quatrième convergence, plus diffuse : **les trois agents rapportent que
l'expérience mesure moins que ce qu'elle produit.** Le chartiste sur la géométrie
(dix quantités par note, une seule consommée), le sorosien sur le volume et les
144 clauses réfutables jamais dépouillées, le trading sur le bêta et les
intervalles jamais publiés.

### Deux désaccords chiffrés, signalés plutôt que tranchés

- **Veto 2** : `trading` annonce 15 occurrences, `chartiste` 17. Mon recomptage
  direct sur `criteres.csv` donne **17**. L'écart n'est pas expliqué.
- **Rangs départagés par le momentum** : `sorosien` annonce 65 sur 144 (45 %), un
  recomptage direct donne 104 (72 %). **Les deux sont justes sous des définitions
  différentes** — 104 lignes appartiennent à un groupe d'ex æquo, réparties en 39
  groupes, donc 104 − 39 = **65 rangs effectivement décidés par le départage**.

### Un défaut à corriger, hors pistes

Le regard en avant de `actualites.md` § 2022-10 (« point bas **annuel** »)
contrevient à la règle la plus stricte du dépôt. Il n'affecte aucun nombre, mais
il se corrige en un mot — celui qu'emploie déjà la section 2022-07.

---

## 7. Le vote — les trois agents relisent les quinze et en retiennent cinq

Les trois agents ont relu **l'ensemble des quinze pistes**, chacun découvrant les
dix qu'il n'avait pas écrites.

### Le critère et le barème, déclarés avant le dépouillement

> **On ne vote pas sur le gain espéré.** Personne ne connaît le gain d'une piste
> non testée, et voter dessus réintroduirait le rétro-ajustement par la porte de
> la synthèse.
>
> Le critère est : **quelle piste rend l'expérience suivante la plus capable de
> démontrer quelque chose ?** Une piste qui ferme une faille de déclaration, qui
> rend une quantité mesurable, ou qui empêche une conclusion abusive, l'emporte
> sur une piste qui promet un meilleur résultat.

Chaque agent classe **exactement cinq** pistes : **5, 4, 3, 2, 1 point**. Trois
bulletins, 45 points. Un agent peut voter pour les siennes, à condition de le
dire. **Départage** : total, puis nombre d'agents distincts, puis A avant B, puis
identifiant alphabétique.

### Les trois bulletins

| Rang | `chartiste` | `trading` | `sorosien` |
|---|---|---|---|
| 1 (5 pts) | T1 | T1 *(la sienne)* | T1 |
| 2 (4 pts) | T3 | C3 | T3 |
| 3 (3 pts) | C1 *(la sienne)* | S4 | S4 *(la sienne)* |
| 4 (2 pts) | S4 | T2 *(la sienne)* | S1 *(la sienne)* |
| 5 (1 pt) | C4 *(la sienne)* | C4 | C4 |

Fait notable : **le `chartiste` a voté contre sa propre C3**, au motif que T3 la
contient et couvre en plus les vetos et les poids effectifs.

### Le classement des quinze

| Rang | Piste | Cat. | `chartiste` | `trading` | `sorosien` | **Total** | Soutiens |
|---|---|---|---|---|---|---|---|
| **1** | **T1** Dimensionner l'expérience avant de la lancer | A | 5 | 5 | 5 | **15** | **3** |
| **2** | **S4** Registre de thèses réfutables, dépouillé chaque mois | A | 2 | 3 | 3 | **8** | **3** |
| **3** | **T3** Déclarer que le score n'est pas la règle du module 3 | A | 4 | — | 4 | **8** | 2 |
| **4** | **C3** Déclarer le sens de `s3`, ou l'aligner | A | — | 4 | — | **4** | 1 |
| **5** | **C4** Durée de vie de l'encadrement contre cadence | A | 1 | 1 | 1 | **3** | **3** |
| 6 | C1 Déclarer et consigner l'objet géométrique | A | 3 | — | — | 3 | 1 |
| 7 | S1 Fiche de canal par ticker, déclaration de portée | A | — | — | 2 | 2 | 1 |
| 8 | T2 Mesurer l'écart comme un alpha | A | — | 2 | — | 2 | 1 |
| 9-12 | C2 · S2 · S3 · T4 | A | — | — | — | 0 | 0 |
| 13-15 | C5 · S5 · T5 | **B** | — | — | — | 0 | 0 |

**Les trois pistes de catégorie B n'ont recueilli aucune voix.** Appliquant le
critère déclaré, les agents n'ont donné aucun poids aux pistes que le résultat
avait suggérées. Les cinq retenues sont toutes des **A**.

### Les cinq pistes retenues

**1. `T1` — Dimensionner l'expérience avant de la lancer** · 15 pts, 3 soutiens

Publier, avant la première séance, la tracking error attendue, l'**effet minimal
détectable** et l'horizon qu'il faudrait. Ici : TE 8,17 %/an, MDE **±16,0 points
sur un an** quand l'écart observé vaut 4,50 — et **187 ans** pour établir que la
règle couvre ses propres frais. *Retenue à l'unanimité et en tête des trois
bulletins* : sans ce chiffre, aucune des quatorze autres pistes ne permet de
conclure quoi que ce soit, et l'expérience suivante rejouerait le même
non-résultat sans savoir qu'elle était incapable de voir.

**2. `S4` — Un registre daté de thèses réfutables, dépouillé chaque mois**
· 8 pts, 3 soutiens

Chaque mois, un énoncé réfutable daté — biais dominant contre tendance
sous-jacente — et le **dépouillement** de ceux du mois précédent, verdict
confirmé / démenti / non tranché. *Retenue par les trois* comme la seule sortie
du mur chiffré par T1 : là où douze mois ne fournissent qu'**un point** d'alpha,
ils fournissent **144 énoncés datés et vérifiables**, déjà écrits, que
l'expérience jette.

**3. `T3` — Déclarer que le score n'est pas la règle du module 3** · 8 pts,
2 soutiens

Nommer le score « règle dérivée », déclarer l'inversion de `s3`, publier les
quatre vetos non appliqués avec leurs taux (**`ATTENTE` aux 144 évaluations**) et
les **poids effectifs** du score (45 / 12 / 8 / 35 / 0 % de la variance).
*Retenue* parce qu'une expérience qui annonce dériver d'une règle dont elle
inverse un critère et jette les vetos ne démontre rien sur cette règle.

**4. `C3` — Déclarer le sens de `s3`, ou l'aligner sur la règle citée**
· 4 pts, 1 soutien

Le versant chiffré du même défaut : la règle achète sous 35 %, le score donne
`+1` au-dessus de 50 %, et **12 achats sur 14** ont eu lieu dans la zone d'achat
interdite par la règle citée en source, **4 ventes sur 9** sur un support.

**5. `C4` — Confronter la durée de vie de l'encadrement à la cadence** · 3 pts,
**3 soutiens**

Publier τ, l'exigence du support, et le taux de survie des droites. *Classée
cinquième par les trois agents* — le plus large consensus après T1. Une
composante qui bascule **20 fois sur 144** en décalant la décision d'une seule
séance, et un encadrement dont **88 clôtures sur 132** sortent d'un mois sur
l'autre, ne sont pas un critère : c'est du bruit, et le savoir d'avance
conditionne toute la construction du score.

### Les fusions proposées

**`C3` et `T3` doivent fusionner** — proposé par **les trois agents**, seul point
d'unanimité de cette étape. C'est le même constat vu depuis la géométrie et
depuis la règle ; les publier séparément laisserait croire à deux défauts
distincts.

> Le barème déclaré n'ayant pas prévu de fusion, **le classement ci-dessus reste
> celui qui fait foi** : changer la règle après avoir vu les bulletins serait
> exactement la faute que toute cette revue s'emploie à éviter. Pour information,
> fusionnées, `C3 + T3` totaliseraient **12 points et 3 soutiens**, prendraient le
> deuxième rang, et libéreraient la cinquième place au profit de `C1`.

Autres fusions proposées, sans unanimité : `T4` dans `T3` (`chartiste`,
`trading`), `C2` dans `C1` (`chartiste`) ou dans `C4` (`trading`), `C4` dans `S4`
(`chartiste`), `S2` sous `S4` (`sorosien`), `T1` avec `T2` (`sorosien`) — que le
`trading` refuse explicitement, l'une étant le dimensionnement *avant* et l'autre
la mesure *après*.

---

## 8. Ce que cette revue ne peut pas établir

- **Qu'une piste appliquée aurait amélioré le résultat.** Cela demanderait de
  rejouer 2022 en la connaissant, ce qui est exactement l'erreur que le protocole
  de l'expérience était bâti pour éviter, et que le classement A/B est là pour
  empêcher de commettre en la déguisant en enseignement.
- **Que la règle est bonne ou mauvaise.** L'alpha mesuré est de −5,18 %/an avec
  un IC95 de [−20,2 ; +9,8] : **indiscernable de zéro**. Douze mois ne tranchent
  rien, et aucune des quinze pistes ne changerait cela.
- **Que les quinze pistes valent quelque chose.** Aucune n'a été testée. Elles ne
  sont pas classées par gain espéré, et ne doivent pas l'être : ordonner par gain
  supposé réintroduirait le rétro-ajustement par la porte de la synthèse.

Ce qui est établi, et c'est de nature différente : **onze des quinze pistes
portent sur ce que l'expérience déclare et mesure, pas sur ce qu'elle décide.**
Une expérience peut être rigoureuse dans sa conduite — celle-ci l'est — et rester
lacunaire dans ce qu'elle publie de ses propres instruments.

---

*Aucune ligne de cette revue n'est un conseil en investissement. Aucun titre
n'est recommandé, aucune position dimensionnée, aucune mesure prolongée au-delà
de la fenêtre où elle a été calculée.*

[← Protocole](README.md) · [Bilan de l'année](bilan-2022.md)
