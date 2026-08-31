# Revue de l'expérience 2

Les trois agents du dépôt — [`chartiste`](../../../../.claude/agents/chartiste.md),
[`trading`](../../../../.claude/agents/trading.md) et
[`sorosien`](../../../../.claude/agents/sorosien.md) — ont relu l'expérience 2
sous leur angle propre, chacun sans connaître les conclusions des deux autres.
Chacun a proposé cinq pistes d'amélioration ; les trois ont ensuite relu
l'ensemble des quinze et voté pour en retenir cinq.

C'est la deuxième revue de cette série. La
[première](../experience_1/review.md) portait sur l'expérience 1, et l'expérience
2 en applique les cinq pistes retenues. Celle-ci juge donc, entre autres, ce qui
a été fait de ces cinq corrections.

---

## 1. Ce qui a été relu

| Fichier | Rôle dans la revue |
|---|---|
| [`README.md`](README.md) | les paramètres d'entrée : univers, score, seuils, vetos, cadence, coûts, référence, dimensionnement |
| [`bilan-2025.md`](bilan-2025.md) | le compte de l'année et les quatre sections d'audit |
| [`rapports/2025-01.md`](rapports/2025-01.md) … [`2025-12.md`](rapports/2025-12.md) | les douze journaux mensuels |
| `graphiques/portefeuille-2025-MM.svg` | les douze courbes du portefeuille contre `TR12` |
| `criteres.csv` | 720 évaluations de la règle — 432 aux dates de décision, 288 aux dates décalées |
| `classement.csv` | le classement et les cinq composantes aux 36 dates d'audit |
| `ordres.csv` | les 11 ordres |
| `theses.csv` | les 864 thèses réfutables et leur dépouillement |
| `portefeuille.csv`, `fantome.csv` | la valeur quotidienne du portefeuille et de son fantôme |
| [`journal.py`](journal.py) et [`journal.md`](journal.md) | le moteur et son miroir d'exécution |
| [`actualites.md`](actualites.md), [`chartiste.md`](chartiste.md) | le texte rédigé à la main, déclaré hors moteur |

Rien ne manque. Le compte de l'année, tel que le bilan le publie :

```
Dotation                10 000,00 EUR au 2025-01-02
Valeur finale           11 251,73 EUR
Performance                 +12,52 %
TR12                        +11,70 %
Alpha sur l'annee            +0,81 pt   (MDE +/- 18,7 pt)

Ordres                  11 (8 achats, 3 ventes)
Frais cumules           67,05 EUR, soit 0,67 % de la dotation
Repli maximal               -9,78 %  (creux au 2025-04-09)
Vetos declenches        287 / 432 evaluations
Theses depouillees      423 confirmees sur 862
```

---

## 2. La contrainte imposée aux trois agents

L'année 2025 est **passée**, et son résultat est connu de qui rédige la revue.
Proposer « il aurait fallu un seuil à 40 % » en sachant ce qu'a fait l'année,
c'est du **rétro-ajustement**, pas une amélioration — c'est le premier des
[cinq pièges de l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md).

> **Chaque piste est classée dans l'une des deux catégories, explicitement.**
>
> - **Catégorie A — indépendante du résultat.** Elle aurait été proposable avant
>   la première séance, en lisant le seul protocole : une lacune de mesure, une
>   convention non déclarée, un contrôle absent, un biais non corrigé.
> - **Catégorie B — suggérée par le résultat.** Elle ne se formule qu'en
>   connaissant ce qui s'est produit. Elle reste **recevable si elle est nommée
>   comme telle** et accompagnée du protocole qui permettrait de la tester
>   honnêtement — sur une autre période, un autre univers, ou en aveugle.
>
> Une piste de catégorie B présentée comme un enseignement est une faute. Une
> piste de catégorie B **déclarée** est une hypothèse pour l'expérience suivante.

**Décompte : 13 pistes A, 2 pistes B.** Les deux seules pistes B — C5 et S5 —
arrivent chacune avec son protocole de test sur une période et un univers
disjoints.

---

## 3. `chartiste` — la géométrie et les signaux

*Son angle : ce que la règle regarde. Fenêtres, encadrements, position dans le
canal, portées, épisodes de contact, τ, ruptures.*

### Ce qu'il a trouvé

**Les trois paramètres qui fabriquent l'encadrement ne sont déclarés nulle
part.** `journal.py` appelle
[`generer_graph_decision.py`](../../../../python/generer_graph_decision.md) sans
`--fenetre` ni `--tolerance` : la fenêtre vaut donc 120 séances, la tolérance de
contact 0,25 σ, l'écart de fusion d'épisodes 3 séances — tous par défaut, et
aucun des trois n'apparaît dans le `README.md`, le `journal.md` ni le bilan. Or
le veto 1, le plus fréquent, en dépend entièrement. Il a relancé les 144
évaluations de l'année narrée sous quatre autres réglages :

| Variante | Veto 1 bascule | `s3` bascule | Évaluations sans aucun veto (base : 46/144) |
|---|---|---|---|
| ε = 0,20 σ | 30/143 — 21,0 % | 0/143 | 40 |
| ε = 0,30 σ | 28/143 — 19,6 % | 0/143 | 49 |
| fenêtre 60 | 59/142 — **41,5 %** | 46/142 — 32,4 % | **21** |
| fenêtre 180 | 36/142 — 25,4 % | 32/142 — 22,5 % | 49 |

Passer la fenêtre de 120 à 60 divise par plus de deux l'ensemble des valeurs
achetables de l'année.

**Les murs du canal sont quatre fois plus minces que le bruit qu'ils doivent
contenir.** Rapportée à σ des variations sur 21 séances, la distance de la
clôture au bord le plus proche vaut **0,23 σ** en médiane ; **354 des 430
évaluations, soit 82,3 %**, l'ont à moins de 0,5 σ, et 12 seulement au-delà de
1 σ. Le taux de survie de 36,3 % publié au bilan n'est donc pas une découverte
sur les marchés : c'est ce que rend mécaniquement un objet de cette échelle. La
confirmation de la thèse `CANAL` suit la distance normalisée presque
linéairement — **22,0 %** sous 0,15 σ, 27,6 %, 42,4 %, **72,4 %** au-delà de
0,50 σ — et la largeur relative, de 10,3 % au quartile le plus étroit à 63,0 %
au plus large. Le côté de sortie est dicté par la position de départ : sous 35 %,
la sortie se fait par le bas dans **82,2 %** des démentis ; au-dessus de 65 %,
par le haut dans **84,9 %**.

**Le veto 1 ne sépare rien.** Le comptage d'épisodes ne descend jamais sous 2 —
une arête d'enveloppe convexe touche deux points par construction — si bien que
le veto est un couperet sur la présence d'**un seul** contact supplémentaire.
Confronté à la tenue de la figure qu'il prétend certifier : **42,9 % ± 7,2** sous
veto contre **40,6 % ± 6,9** hors veto, soit un écart de **+2,3 pt ± 10,0**.
Pendant que τ sépare de 51,6 points — 0 % de tenue sous 21 séances, 51,6 % au-delà
de 60.

**La droite elle-même bouge, et le bilan ne le dit pas.** Le § 6 publie les
bascules de `s3` (27/144) et du score (45/144), mais pas que reculer d'une seule
séance change la **pente du support dans 28,2 %** des cas et celle de la
résistance dans 22,5 % (38,0 % et 32,4 % à d−2). La médiane de |Δposition| pour
une séance vaut 6,6 points, sur une échelle où les bandes de `s3` en font 35, 30
et 35. L'instabilité se concentre là où le canal est étroit : 28,2 % de bascule
dans la moitié étroite contre 8,5 % dans la moitié large.

**Le score n'exploite pas la géométrie qu'il calcule.** La règle produit huit
quantités géométriques ; le score en consomme **une seule**, la position,
quantifiée à ±1, pour 8,7 % de la variance. **45 des 185 `s3 = +1` sont à moins
de 1 % du cours de basculer.** Par ailleurs 32,3 % des encadrements sont des
biseaux, et la pente moyenne du canal contredit le signe de `TEND_120` dans
9,8 % des cas — deux contrôles absents.

**Aucune figure d'encadrement n'est publiée.** `journal.py` écrit les 720 SVG de
décision dans un fichier jetable puis les supprime. L'expérience publie douze
graphiques de performance — précisément la quantité qu'elle déclare non
concluante — et **zéro** figure de l'objet géométrique sur lequel elle décide.

Enfin, sur ses propres notes : **11 sur 144** contiennent un futur ou un
conditionnel. C'est conforme à sa charte — il ne prédit pas — mais cela signifie
que la couche rédigée est restée entièrement hors du dispositif de réfutation.

### Ses cinq pistes

| | Titre | Cat. |
|---|---|---|
| **C1** | Déclarer les trois paramètres de l'encadrement, et publier leur sensibilité | **A** |
| **C2** | Rapporter le canal à la volatilité, et qualifier les ruptures | **A** |
| **C3** | Déclarer, pour chaque veto, l'issue contre laquelle il sera jugé | **A** |
| **C4** | Publier la droite, pas seulement ses nombres | **A** |
| **C5** | Un `s3` continu et un veto d'échelle, testés en aveugle | **B** |

**C1** ajoute `--fenetre 120`, `--tolerance 0,25 σ` et `ECART_EPISODE = 3` au
protocole comme paramètres déclarés, et impose deux variantes publiées au bilan.
Coût : 432 évaluations par variante, aucun frais. Mesure : le taux de bascule et
son IC — un IC publié plus étroit que l'incertitude de convention est mesurable
et faux.

**C2** ajoute deux colonnes — largeur et distance au bord, en σ des variations
calculé sur les seules séances antérieures — et fait passer le dépouillement
`CANAL` à trois modalités : `TENUE`, `SORTIE QUALIFIÉE` (≥ 0,5 σ au-delà du bord
et deux clôtures consécutives dehors), `EFFLEUREMENT`. Les 56 thèses à bornes
inversées vont dans une ligne `INCONFIRMABLE À L'ÉCRITURE`. Mesure : le gradient
de survie par quartile de largeur, aujourd'hui de 10,3 % à 63,0 %, doit
disparaître.

**C3** demande que chaque veto se voie assigner **avant la première séance**
l'issue observable contre laquelle il sera jugé, et que le bilan publie taux de
tenue sous veto, hors veto, et leur différence avec son IC. **Le veto reste
bloquant quoi qu'il arrive** — le modifier après l'avoir vu plat serait le
rétro-ajustement même. Mesure : la différence de deux proportions ; il faudrait
≈ 1 500 dépouillements par veto pour séparer 5 points à ± 5 pt.

**C4** conserve les figures de décision qui décident quelque chose — les 11
ordres et les 19 entrées bloquées —, ajoute les pentes recalculées à d−1 et d−2
dans `criteres.csv`, et publie le taux de changement de la droite. Coût : 0,6 Mo
pour 30 figures, aucun calcul nouveau. Il note que sur la partie « publier la
figure », l'amélioration n'est **pas chiffrable** — elle est d'auditabilité — et
il le dit plutôt que de fabriquer une métrique.

**C5** rend `s3` continu (`−(position − 50)/50`, borné à ±1) et double le veto 1
d'un veto d'échelle à 0,3 σ, les deux calibrés sur **2016-2019 et douze valeurs
autres**, puis appliqués sans retouche, en portefeuilles fantômes. Il classe la
piste entière **B** parce que la forme du remède sort du gradient qu'il a mesuré
en 2025, et dit explicitement ce qu'on ne saura pas : si la règle en est
meilleure.

---

## 4. `trading` — la performance et la règle

*Son angle : ce que la règle rend. Alpha et son incertitude, bêta, coûts,
construction du score, seuils, cadence, référence, variantes.*

### Ce qu'il a trouvé

**Le portefeuille a un bêta de 0,614, et rien dans le protocole ne le mesure.**
Régression des 254 rendements quotidiens sur `TR12` : β = 0,614, SE = 0,032,
**t = −11,99 contre 1, p < 10⁻⁴**. C'est la seule quantité de cette expérience
qui soit franchement significative, et elle n'est publiée nulle part. L'alpha de
+0,81 pt est un **écart brut** qui additionne deux effets de signes opposés : un
déficit d'exposition très négatif dans une année haussière, et un effet de
sélection positif. L'alpha de régression vaut **+4,98 pt, IC95 [−9,9 ; +19,9]**,
toujours indiscernable de zéro, mais avec un MDE de **± 14,9 pt au lieu de
± 18,7** — la régression retire de la tracking error la part qu'explique le bêta,
soit **36 % de sa variance**. Contrefactuel d'exposition neutre, espèces placées
chaque jour dans `TR12` : **+20,71 %**.

**Les espèces sont le premier poste, et le protocole les traite comme un
reste.** Part investie moyenne **64,7 %** ; **42 séances — 16,5 % de l'année — à
100 % en espèces**. Le README annonce que les rémunérer « demanderait une
convention de plus pour un effet de quelques euros » : mesuré, le manque à gagner
vaut 0,354 × r_f, soit **35 à 89 €** pour r_f entre 1 et 2,5 %/an — du même ordre
que les 67,05 € de frais, que le protocole facture au centime. L'alpha cumulé
était de **−7,44 pt fin février** sans qu'un seul titre soit détenu.

**Le classement est inerte à l'entrée ; c'est le veto qui décide.** Médiane de
**2 valeurs éligibles sur 12** ; le filtre « rang ≤ 5 » n'est contraignant que
**2 fois sur 36** ; sur les 12 dates narrées, 54 créneaux de tête étaient de
score positif et **20 seulement sans veto**. Le seuil de vente « score ≤ −3 » n'a
**jamais pu** se déclencher — le score minimal atteint par une position détenue
est **−1** — et les trois ventes sont toutes parties de « rang 8 ».

D'où une critique de méthode sur les poids effectifs publiés : ils mesurent la
variance du score, alors que la décision ne lit que `signe(score)`. En influence
décisionnelle — annuler une composante renverse-t-elle le signe ? — sur 430
évaluations : `s1` 18,6 %, **`s4` 9,5 %**, `s3` 7,0 %, `s2` 5,6 %, `s5` 0,0 %.
`s4` pèse 37,6 % de la variance et 9,5 % de la décision.

**Deux paramètres non déclarés commandent tout le reste.** Il a refait les 144
évaluations à quatre points de grille :

| Configuration | veto 1 | veto 2 | aucun veto |
|---|---|---|---|
| tol 0,15 · fen 120 | 72,2 % | 17,4 % | **18,8 %** |
| tol 0,25 · fen 90 | 63,2 % | 26,4 % | 22,9 % |
| **tol 0,25 · fen 120 (retenue)** | 53,5 % | 17,4 % | **31,9 %** |
| tol 0,25 · fen 180 | 48,6 % | 9,7 % | 34,7 % |
| tol 0,40 · fen 120 | 36,8 % | 17,4 % | **44,4 %** |

Le taux d'achetabilité varie d'un **facteur 2,4**, et `s3` change dans 17,5 à
22,5 % des cas quand on passe de 120 à 180 ou 90 séances — **aussi souvent que
l'inversion de `s3`, qui est la correction phare de l'expérience.**

**Les trois séries parallèles ne sont pas comparables telles qu'elles sont
publiées.** En reconstruisant leurs séries quotidiennes :

| Série | Base 100 | Part investie | β contre `TR12` | Écart au réel | MDE apparié |
|---|---|---|---|---|---|
| Portefeuille | 112,52 | 64,7 % | 0,614 | — | — |
| Fantôme (`s3` sens exp. 1) | 109,11 | 68,2 % | 0,643 | +3,41 pt | **± 5,3 pt** |
| `--repartition candidats` | 111,71 | 83,0 % | **1,230** | +0,81 pt | **± 34,9 pt** |
| `--sans-veto` | 105,73 | 89,2 % | 0,900 | +6,79 pt | ± 13,5 pt |

L'appariement, qui est toute la raison d'être du fantôme, **est cassé pour les
deux variantes**. Aucun des trois écarts ne dépasse son MDE, mais un seul le dit.

**Sur le procédé de la répartition classée B.** Le déclarer vaut mieux que le
taire, et publier la règle écartée à côté de la règle retenue est honnête. Deux
réserves cependant : la décision B a été appliquée **au portefeuille qui engage
les euros**, alors que la catégorie B implique de l'éprouver sur l'expérience
*suivante* ; et le motif invoqué était **dérivable du protocole seul**, la
fenêtre d'étalonnage ayant publié *avant la première séance* que deux tiers des
évaluations étaient sous veto. Le défaut était de catégorie A ; c'est sa
*découverte* qui a été B. Sa formule : « se classer B est ici plus indulgent
qu'exact ».

**Coûts et horizon.** 11 ordres, 22 063 € traités, 67,05 € de frais, soit
0,304 % du volume, pour une rotation de 1,04×/an. Le README calculait 189 ans
pour établir que la règle couvre ses frais ; avec les chiffres réalisés, la même
formule donne **773 ans**, ou 491 avec l'erreur-type de régression. Le bilan § 9
ne rejoue pas cette ligne.

### Ses cinq pistes

| | Titre | Cat. |
|---|---|---|
| **T1** | Publier un alpha de régression, et décomposer l'écart en exposition et sélection | **A** |
| **T2** | Déclarer `--fenetre` et `--tolerance`, et publier leur grille de sensibilité | **A** |
| **T3** | Auditer l'influence décisionnelle des composantes, pas leur variance | **A** |
| **T4** | Traiter les espèces comme une position, et non comme un reste | **A** |
| **T5** | Geler la liste des variantes avant la première séance, et les publier appariées | **A** |

**T1** fait publier β et son test contre 1, l'alpha de régression et son IC95, R²,
la volatilité résiduelle, la décomposition TE² = (1−β)²σ_m² + σ_ε², et la série à
exposition neutralisée. Coût nul — deux colonnes déjà présentes et la
`p_valeur_student()` du dépôt. Gain vérifiable sur l'expérience elle-même : 20 %
de puissance sans toucher à la règle.

**T2** déclare les deux paramètres et publie la grille aux quatre autres points.
Coût : 576 sous-processus, ≈ 4 minutes à 10 tâches parallèles. Mesure :
l'amplitude de la grille, ici 25,6 points, contre une incertitude
d'échantillonnage de ± 4,7.

**T3** publie, à côté de la table de variance, une table d'influence
décisionnelle, plus deux diagnostics de saturation — nombre d'éligibles par date,
et fréquence à laquelle chaque seuil est atteignable. Coût nul.

**T4** impose, à défaut de rémunérer les espèces, que le bilan publie part
investie moyenne, séances à 100 % espèces et drag sous forme de coefficient ×
r_f, et que la part investie entre dans le tableau mensuel **à côté de l'alpha du
mois**. Il recommande la version gratuite, qui rend la convention visible sans
l'abandonner. C'est, dit-il, la seule des cinq pistes dont l'effet soit **exact
et sans incertitude**.

**T5** gèle la liste des variantes avant la première séance — toute règle
découverte en faisant tourner le moteur entre dans cette liste, **jamais dans la
règle qui engage les euros** —, publie leurs séries quotidiennes avec β et MDE
apparié, et signale comme **non appariée** toute variante dont le β s'écarte trop.
Le moteur calcule déjà ces séries et n'en garde que le point d'arrivée.

---

## 5. `sorosien` — la réflexivité

*Son angle : le protocole voit-il les séquences auto-renforçantes entre cours et
fondamentaux ? C'est sa piste S4 de l'expérience 1 qui a produit le registre des
thèses ; il juge ici ce qu'on en a fait.*

### Ce qu'il a trouvé

**Le verrou n'a jamais été posé.** Le mot « canal » revient partout dans le
protocole, mais jamais au sens de Soros : il y désigne l'objet géométrique
support/résistance. Le **canal de transmission** — le mécanisme par lequel le
cours agit sur les affaires — n'est nommé nulle part, ni pour l'univers, ni
valeur par valeur, ni même comme une lacune. Or l'univers déclaré est à peu près
le moins réflexif qu'on puisse construire à Paris : douze mégacapitalisations
autofinancées, dont une seule — `BNP.PA` — a un canal vivant et documentable. Le
seul canal mesurable pour les autres est l'émission au titre des plans salariés,
et sur la série point-in-time d'Airbus déjà présente dans le dépôt, le nombre
d'actions varie de **+0,50 % en 3,5 ans**.

**Le registre mesure de la volatilité, pas de la réflexivité.** Il a appliqué
chaque clause aux 432 observations **sans regarder l'étiquette** :

| Clause | Sous son étiquette | Appliquée aux 432 | Apport de l'étiquette |
|---|---|---|---|
| `AUTO-RENFORCEMENT` — écart ≥ 0 | 24/60 = 40,0 % ± 12,4 | 217/432 = 50,2 % | **−10,2 pt** |
| `RETOURNEMENT` — écart ≤ 0 | 19/32 = 59,4 % ± 17,0 | 215/432 = 49,8 % | +9,6 pt |
| `AUCUNE SEQUENCE` — \|écart\| ≤ 5 | 224/340 = 65,9 % ± 5,0 | 292/432 = 67,6 % | −1,7 pt |

Des étiquettes tirées au hasard, de mêmes fréquences, auraient produit **275,9
confirmations sur 432, soit 63,9 %**. Le registre en a produit 267, soit 61,8 % :
**le dispositif fait 2,1 points de moins que le hasard.** Trois preuves
convergentes que la clause mesure l'échelle et non la phase — le taux
d'`AUCUNE SEQUENCE` suit sa base inconditionnelle à quatre horizons (67/44/31/19 %
contre 69/45/31/20 %) ; il est corrélé **−0,84** à l'écart-type propre de la
valeur (`AI.PA` 88,9 % pour σ = 2,74, `RI.PA` 44,0 % pour σ = 5,61) ; et il
dément `RI.PA`, seule trajectoire de l'univers qui ressemble à un bust
(**−62,2 %** depuis son plus haut du 2023-04-25, jamais effacé), pour la raison
exactement inverse de celle qu'on croit.

**La phase n'a aucune mémoire.** Sur les 420 transitions d'un mois au suivant :
`AUTO-RENFORCEMENT` compte **51 épisodes de 1,18 mois en moyenne**, 82 % ne
durant qu'un mois ; la persistance vaut **15,3 % contre une base inconditionnelle
de 14,3 %** — l'étiquette est un tirage indépendant ; et il y a **zéro transition
`AUTO-RENFORCEMENT` → `RETOURNEMENT` sur 420**. Un dispositif qui prétend suivre
le cycle boom-bust et n'a pas vu une seule fois un boom suivi d'un bust n'a pas
observé de cycle.

**La clause est réfutable au mauvais endroit, deux fois.** Sur l'échelle, une
demi-largeur fixe de ± 5 points est facile pour une valeur calme et dure pour une
valeur agitée. Sur le point, les bornes d'`AUTO-RENFORCEMENT` et de
`RETOURNEMENT` sont posées à **zéro**, c'est-à-dire au mode de la distribution
(médiane +0,02 pt) : **9 verdicts sur 60** se jouent à moins de 0,5 point, et
déplacer la borne d'un dixième d'écart-type fait passer le taux de **40,0 % à
53,3 %**.

**Deux incohérences internes que le bilan ne relève pas.** `phase_reflexive()`
lit la position issue d'un encadrement sans jamais consulter les vetos : **48,4 %
des phases sont nommées sur une figure que la règle déclare illisible**, et
**52,2 % des 92 phases « séquence » portent au moins un veto**. Le protocole
refuse d'acheter sur cette figure et accepte d'y lire un état réflexif : les deux
ne peuvent pas être vrais ensemble. Par ailleurs `Volume` apparaît **0 fois**
dans `journal.py`, alors que les 60 étiquettes `AUTO-RENFORCEMENT` sont posées
sur un volume relatif médian de **0,92×** — un auto-renforcement sur volume
décroissant est, dans sa grille, le contraire d'un auto-renforcement.

Enfin, la seule phase affirmable sur les prix seuls — le **test réussi** —
n'existe pas dans la taxonomie à trois étiquettes. Un détecteur strict appliqué
aux douze mêmes séries de 2023 à 2025 rend **29 tests réussis et 11 replis jamais
effacés**. Le registre n'en enregistre aucun.

**Sa conclusion d'angle, qu'il déclare admissible : aucune séquence réflexive
identifiable** sur cet univers, ces dates et ces mesures. Ce n'est pas un échec de
l'expérience — c'est le résultat qu'elle aurait dû publier à la place de 432
étiquettes de phase.

### Ses cinq pistes

| | Titre | Cat. |
|---|---|---|
| **S1** | Poser le verrou : nommer le canal de transmission avant toute thèse réflexive | **A** |
| **S2** | Faire porter la clause réflexive sur le canal, pas sur l'écart de cours | **A** |
| **S3** | Normaliser la clause par la volatilité propre, et écarter la borne du mode | **A** |
| **S4** | Donner une mémoire à la phase : test réussi à l'entrée, rupture volumique à la sortie | **A** |
| **S5** | L'asymétrie de `RETOURNEMENT` à horizon long : hypothèse, et protocole en aveugle | **B** |

**S1** impose un tableau déclaré avant la première séance, une ligne par valeur,
avec l'un des sept canaux ou la mention « aucun », et la grandeur du dépôt qui
l'instrumente. Les valeurs sans canal reçoivent `HORS CHAMP RÉFLEXIF` — un
énoncé différent d'`AUCUNE SEQUENCE`, que le protocole actuel confond dans une
case pesant 340 thèses sur 432. Coût : douze appels à
`reconstituer_fondamentaux.py`. Il annonce d'avance la **perte de puissance** :
1 ou 2 canaux vivants sur 12, donc 36 à 72 thèses au lieu de 432, IC de ± 11 à
16 pt au lieu de ± 4,7. « Le gain n'est pas statistique, il est de validité. »

**S2** fait porter la clause sur la grandeur du canal déclaré en S1 — le nombre
d'actions, la dette sur EBITDA — au lieu de l'écart de rendement, avec la même
mécanique à deux bornes, donc sans code nouveau. Le test de réussite est celui
qui a démoli le registre actuel : publier le taux sous étiquette et le taux
inconditionnel côte à côte.

**S3** remplace la demi-largeur fixe par l'écart-type des 12 écarts mensuels
précédents de la valeur — tous déjà dans le registre à la date d, donc sans
regard en avant —, écarte les bornes du mode à ± 0,5 σ, et crée une zone morte
explicitement `NON TRANCHEE`. Coût : un amorçage de 12 mois, soit 144
observations sur 432. Il dit lui-même que l'amélioration est **partielle** : sur
les 288 observations amorçables, la dispersion entre valeurs tombe de 44,9 à
37,5 points, et normaliser par la volatilité passée ne corrige pas les changements
de régime — précisément les moments intéressants.

**S4** fait de la phase un **état** avec date d'entrée et critère de sortie
écrits : entrée sur un test réussi documenté, sortie sur rupture du support long
accompagnée d'un volume ≥ 1,5× la moyenne 250 séances, phases 5 et 6 interdites
explicitement. Coût : ≈ 30 lignes, `Volume` étant déjà dans les séries. Trois
mesures, toutes indépendantes du rendement : durée médiane d'un épisode (1 mois
aujourd'hui), persistance conditionnelle (15,3 % contre 14,3 %), et nombre de
séquences complètes (0 sur 420).

**S5** pré-enregistre l'hypothèse que le taux de `RETOURNEMENT` dépouillé à
12 mois dépasse de plus de 15 points sa base — les taux observés montent avec
l'horizon, 56/58/76/77 % contre une base plate de 49 à 51 % — sur un **univers et
une période disjoints**, une seule hypothèse déposée, le dépouillement à 12 mois
écrit avant la collecte. Il classe **B** sans réserve : sur n = 22, l'IC95 vaut
± 17,6 points et englobe la base. Et il dit d'avance qu'**une année n'y suffira
pas** : il faut ≈ 500 observations, soit 42 mois × 12 valeurs.

---

## 6. La synthèse

### Les quinze pistes

| Id | Titre | Cat. | Coût |
|---|---|---|---|
| **T1** | Alpha de régression, décomposition exposition / sélection | A | nul |
| **T3** | Influence décisionnelle des composantes, pas leur variance | A | nul |
| **T4** | Les espèces traitées comme une position | A | nul |
| **T5** | Liste des variantes gelée avant, publiées appariées | A | nul |
| **C3** | Chaque veto jugé contre une issue déclarée | A | nul |
| **S3** | Clause normalisée par la volatilité propre, borne écartée du mode | A | 144 observations d'amorçage |
| **C2** | Canal rapporté à la volatilité, ruptures qualifiées | A | nul |
| **C4** | La droite publiée, pas seulement ses nombres | A | 0,6 Mo |
| **S4** | Une mémoire pour la phase | A | ≈ 30 lignes |
| **C1** | Les trois paramètres de l'encadrement déclarés, sensibilité publiée | A | 432 évaluations par variante |
| **T2** | `--fenetre` et `--tolerance` déclarés, grille publiée | A | 576 sous-processus |
| **S2** | Clause portée sur le canal, pas sur l'écart de cours | A | 12 séries point-in-time |
| **S1** | Le canal de transmission nommé avant toute thèse | A | 12 appels réseau |
| **C5** | `s3` continu et veto d'échelle, calibrés hors échantillon | **B** | 12 séries 2016-2019 + 288 évaluations |
| **S5** | Asymétrie de `RETOURNEMENT`, pré-enregistrée | **B** | fenêtre allongée d'un an |

**13 pistes A, 2 pistes B.** Aucune ne touche l'exécution : **aucune ne coûte un
euro de frais**.

### Ce sur quoi plusieurs agents convergent

**Trois paramètres non déclarés dominent tous les intervalles publiés.**
`chartiste` et `trading` l'ont trouvé indépendamment, par des mesures
différentes : 46 → 21 valeurs achetables quand la fenêtre passe de 120 à 60 chez
l'un, taux d'achetabilité de 18,8 % à 44,4 % sur la grille chez l'autre. La
conséquence est la même : l'IC de ± 4,7 pt publié au bilan est **plus étroit que
l'incertitude de convention qui le domine**. C'est la convergence la plus forte
de la revue, et elle a produit les deux premières places du vote.

**Le veto est le mécanisme qui décide, et rien ne le juge.** `trading` le montre
par le haut — médiane de 2 éligibles sur 12, « rang ≤ 5 » contraignant 2 fois sur
36, seuil de vente jamais atteignable, et un bêta de 0,614 qui en découle.
`chartiste` le montre par le bas — le veto 1, qui écarte 48,4 % des évaluations,
sépare de **+2,3 pt ± 10,0** sur la tenue de la figure qu'il prétend certifier.
`sorosien` ajoute qu'il est simultanément ignoré là où il compterait : 52,2 % des
phases « séquence » sont nommées sur une figure sous veto.

**Une convention d'échelle unique manque partout.** `chartiste` mesure que la
survie du canal suit la distance normalisée (22 % → 72 %) ; `sorosien` mesure que
la confirmation des thèses suit l'écart-type propre de la valeur (ρ = −0,84). Ce
sont deux instances du même défaut, et les deux agents proposent le même remède
sur deux objets différents — d'où la fusion C2 + S3 proposée par deux voix, et la
formulation retenue par `trading` : *tout seuil s'exprime en unités de σ propre*.

**L'exposition n'est mesurée nulle part.** `trading` en fait sa T1 ; `sorosien` la
place première de son bulletin bien qu'elle ne soit pas de son angle. Un bêta de
0,614 et une part investie de 64,7 % sont, dit-il, deux lectures du même fait.

### Un désaccord chiffré, signalé plutôt que tranché

Les deux agents qui ont recalculé le taux de tenue de la thèse `CANAL` **hors les
56 bornes inversées** ne s'accordent pas sur le dénominateur : `chartiste` publie
**156/374 = 41,7 % ± 5,0**, `sorosien` **156/376 = 41,5 %**. L'écart tient à ce
qu'on retranche les 56 de 430 dépouillements tranchés ou de 432 thèses écrites.
Le numérateur, lui, est le même. La revue ne tranche pas : un désaccord chiffré
est une information, et il porte ici sur la définition du dénominateur, pas sur
la mesure.

---

## 7. Le vote

### Le critère, déclaré avant le dépouillement

> **On ne vote pas sur le gain espéré.** Personne ne connaît le gain d'une piste
> non testée, et voter dessus réintroduirait le rétro-ajustement par la porte de
> la synthèse.
>
> Le critère est : **quelle piste rend l'expérience suivante la plus capable de
> démontrer quelque chose ?** Une piste qui ferme une faille de déclaration, qui
> rend une quantité mesurable, ou qui empêche une conclusion abusive, l'emporte
> sur une piste qui promet un meilleur résultat.

### Le barème

Chaque agent classe **exactement cinq** pistes parmi les quinze : 5, 4, 3, 2 et
1 point. Trois bulletins, **45 points distribués**. Un agent peut voter pour ses
propres pistes à condition que le bulletin le montre. Départage : total des
points, puis nombre d'agents distincts, puis **A avant B**, puis identifiant
alphabétique.

### Les trois bulletins

**`chartiste`** — vote pour trois des siennes, et le déclare.

| | Piste | Pts | |
|---|---|---|---|
| 1 | **C1** | 5 | *(sienne)* fusionnée avec T2 ; deux agents l'ont trouvée indépendamment, et aucun IC publié n'est aujourd'hui opposable |
| 2 | **T1** | 4 | seule quantité franchement significative de l'expérience, publiée nulle part |
| 3 | **C3** | 3 | *(sienne)* sans elle, la prochaine expérience remettra un couperet qui bloque 48,4 % des évaluations sans qu'on ait demandé s'il sépare quelque chose |
| 4 | **T3** | 2 | une règle de sortie qui ne pouvait jamais se déclencher est un défaut de déclaration pur |
| 5 | **C2** | 1 | *(sienne)* fusionnée avec S3 ; un taux de tenue doit mesurer la figure, pas son échelle |

**`trading`** — vote pour deux des siennes, et le déclare.

| | Piste | Pts | |
|---|---|---|---|
| 1 | **C1** | 5 | tant que les trois paramètres restent des défauts, chaque taux publié est une propriété d'un réglage et non de la règle |
| 2 | **C3** | 4 | le veto est le mécanisme qui décide réellement ; lui assigner son issue à l'avance transforme le plus gros levier en énoncé réfutable |
| 3 | **T1** | 3 | *(sienne)* l'alpha annoncé additionne un déficit d'exposition et un effet de sélection de signes opposés |
| 4 | **S3** | 2 | 432 dépouillements qui font 2,1 points de moins que le hasard : la normalisation décide s'ils mesurent une thèse ou une volatilité |
| 5 | **T5** | 1 | *(sienne)* ferme la porte par laquelle le protocole a modifié sa règle vivante après un essai du moteur |

**`sorosien`** — vote pour deux des siennes, et le déclare.

| | Piste | Pts | |
|---|---|---|---|
| 1 | **T1** | 5 | transforme un bilan qui déclare ne rien conclure en un bilan qui conclut sur l'exposition |
| 2 | **S1** | 4 | *(sienne)* empêche la conclusion la plus abusive du document : 432 thèses « au sens de Soros » sans qu'un seul canal soit nommé |
| 3 | **C1** | 3 | trois paramètres libres qui font varier l'achetabilité d'un facteur 2,4 rendent aucun taux opposable — les siens compris |
| 4 | **C3** | 2 | rend falsifiable un filtre qui écarte 48,4 % des évaluations en ne séparant que +2,3 pt ± 10,0 |
| 5 | **S4** | 1 | *(sienne)* convertit « aucune séquence réflexive identifiable » d'une case par défaut en un résultat compté |

### Le classement des quinze

| Rang | Piste | Cat. | `chartiste` | `trading` | `sorosien` | **Total** | Soutiens |
|---|---|---|---|---|---|---|---|
| **1** | **C1** | A | 5 | 5 | 3 | **13** | **3** |
| **2** | **T1** | A | 4 | 3 | 5 | **12** | **3** |
| **3** | **C3** | A | 3 | 4 | 2 | **9** | **3** |
| **4** | **S1** | A | — | — | 4 | **4** | 1 |
| **5** | **S3** | A | — | 2 | — | **2** | 1 |
| 6 | T3 | A | 2 | — | — | 2 | 1 |
| 7 | C2 | A | 1 | — | — | 1 | 1 |
| 8 | S4 | A | — | — | 1 | 1 | 1 |
| 9 | T5 | A | — | 1 | — | 1 | 1 |
| 10 | C4 | A | — | — | — | 0 | 0 |
| 11 | S2 | A | — | — | — | 0 | 0 |
| 12 | T2 | A | — | — | — | 0 | 0 |
| 13 | T4 | A | — | — | — | 0 | 0 |
| 14 | C5 | **B** | — | — | — | 0 | 0 |
| 15 | S5 | **B** | — | — | — | 0 | 0 |

**Total : 45 points sur 45.** S3 et T3 sont à égalité de points (2) et de
soutiens (1), toutes deux de catégorie A : le départage se fait à l'identifiant
alphabétique, et **S3 passe devant T3**.

Trois choses méritent d'être relevées.

**Les trois premières pistes ont chacune les trois soutiens.** Aucune des douze
autres n'en a plus d'un. La hiérarchie n'est donc pas un classement de
préférences, c'est un accord.

**Les deux pistes de catégorie B ont recueilli zéro voix** — comme lors de la
revue de l'expérience 1. Appliquant le critère déclaré, les agents n'ont donné
aucun poids à ce que le résultat leur avait suggéré, y compris à leurs propres
pistes B.

**`trading` a retiré sa propre T2 au profit de C1**, jugeant que la piste du
`chartiste` la contient strictement. C'est ce retrait qui explique le zéro de T2,
et non un désintérêt : la piste est au contraire première du classement, sous
l'autre identifiant.

### Les cinq pistes retenues

**1. C1 — Déclarer les trois paramètres de l'encadrement, et publier leur
sensibilité** *(13 points, 3 soutiens, A)*

`--fenetre 120`, `--tolerance 0,25 σ` et `ECART_EPISODE = 3` entrent au protocole
comme paramètres déclarés, et le moteur publie au bilan le taux de bascule de
chaque veto sous deux variantes déclarées d'avance. **Retenue parce que c'est la
seule piste dont dépendent toutes les autres mesures** : tant que ces trois
nombres restent des défauts de script, les taux publiés — 48,4 % de veto 1,
63,7 % de sorties, 36,3 % de survie — sont des propriétés d'un réglage, et leur
IC de ± 4,7 pt est plus étroit que l'incertitude de convention qui les domine.

**2. T1 — Publier un alpha de régression, et décomposer l'écart en exposition et
sélection** *(12 points, 3 soutiens, A)*

Le bilan publie β et son test contre 1, l'alpha de régression et son IC95, la
décomposition de la tracking error, et la série à exposition neutralisée.
**Retenue parce qu'elle empêche la seule conclusion abusive qui reste ouverte** :
lire +0,81 pt comme de la sélection quand un bêta de 0,614 l'explique. Elle
resserre en outre le MDE de ± 18,7 à ± 14,9 pt sans toucher à la règle, pour un
coût nul.

**3. C3 — Déclarer, pour chaque veto, l'issue contre laquelle il sera jugé**
*(9 points, 3 soutiens, A)*

Chaque veto se voit assigner avant la première séance l'issue observable qui le
jugera, et le bilan publie taux de tenue sous veto, hors veto, et leur différence
avec son IC. **Retenue parce qu'elle transforme le plus gros levier de
l'expérience en énoncé réfutable** : le veto décide plus que le classement, et
rien dans les deux expériences n'a jamais demandé s'il sépare quelque chose. Le
veto reste bloquant quoi qu'il arrive — le modifier après l'avoir vu plat serait
le rétro-ajustement même.

**4. S1 — Poser le verrou : nommer le canal de transmission avant toute thèse
réflexive** *(4 points, 1 soutien, A)*

Un tableau déclaré avant la première séance, une ligne par valeur, avec son canal
de transmission ou la mention « aucun » ; les valeurs sans canal reçoivent `HORS
CHAMP RÉFLEXIF` et non `AUCUNE SEQUENCE`. **Retenue parce qu'elle est la
condition d'application de tout le registre** : l'expérience a écrit 432 thèses
« au sens de Soros » sans avoir déclaré par quel mécanisme le cours agirait sur
les affaires. Elle assume une perte de puissance chiffrée d'avance — de 432
thèses à 36 ou 72 — au profit de la validité.

**5. S3 — Normaliser la clause par la volatilité propre, et écarter la borne du
mode** *(2 points, 1 soutien, A)*

La demi-largeur fixe de ± 5 points devient l'écart-type des 12 écarts mensuels
précédents de la valeur, les bornes s'écartent du mode à ± 0,5 σ, et la zone
morte reçoit un verdict `NON TRANCHEE` compté à part. **Retenue parce qu'elle
décide si les 432 dépouillements — le bloc d'observations le plus nombreux du
dispositif — mesurent une thèse ou la volatilité de la valeur.** Son auteur
déclare lui-même l'amélioration partielle : la dispersion entre valeurs tombe de
44,9 à 37,5 points, et la normalisation par le passé ne corrige pas les
changements de régime.

### Les fusions proposées

Les trois agents proposent des fusions, et deux d'entre elles sont soutenues par
plusieurs voix :

| Fusion | Proposée par | Motif |
|---|---|---|
| **C1 + T2** | les trois | même constat, même remède ; `trading` a retiré T2 de son bulletin en conséquence |
| **C2 + S3** | `chartiste`, `trading` | même principe sur deux objets ; `trading` propose la formulation unique *« tout seuil s'exprime en unités de σ propre »* |
| **T1 + T4** | `trading`, `sorosien` | un β de 0,614 et une part investie de 64,7 % sont deux lectures du même fait |
| **S1 + S2**, S3 absorbée | `sorosien` | le verrou sans la clause ne fait que retirer des thèses ; la clause sans le verrou porte sur rien |

**Le barème déclaré ne prévoyait pas de fusion**, et le classement ci-dessus le
respecte tel quel. L'effet des fusions est publié ici à titre indicatif, et il ne
change pas les trois premières places : C1 + T2 resterait première à 13 points ;
T1 + T4 resterait deuxième à 12 ; C2 + S3 monterait à 3 points et 2 soutiens,
donc au cinquième rang à la place de S3 seule. Comme dans la revue de
l'expérience 1, **la règle déclarée l'emporte sur l'unanimité constatée après
coup** : changer le barème une fois les bulletins connus serait exactement la
faute que ce dispositif s'emploie à éviter.

---

## 8. Ce que cette revue ne peut pas établir

- **Qu'une piste appliquée aurait amélioré le résultat.** Il faudrait rejouer
  2025 en la connaissant, ce qui est le premier des cinq pièges de l'alpha. Les
  cinq pistes retenues rendent l'expérience suivante plus capable de démontrer
  quelque chose ; aucune ne promet un meilleur rendement, et aucune n'a été votée
  sur cette base.
- **Que les cinq corrections de l'expérience 1 ont fonctionné.** Deux ont tenu
  franchement — le dimensionnement publié avant, qui a interdit de conclure sur
  un alpha de +0,81 pt, et l'application des vetos, qui a été mesurée. Une
  troisième, le registre des thèses, a produit un dispositif qui fait 2,1 points
  de moins que le hasard. Mais un an ne dit pas si c'est la piste qui était
  mauvaise ou sa mise en œuvre.
- **Quel sens de `s3` est le bon.** L'écart apparié au fantôme vaut +3,41 pt pour
  un MDE de ± 5,3 pt. C'est la comparaison la mieux dimensionnée de l'expérience,
  et elle ne tranche pas.
- **Quoi que ce soit sur une autre période ou un autre univers.** Les taux
  mesurés ici sont des propriétés de cette règle sur ces douze valeurs, à ces
  trente-six dates, sous des paramètres d'encadrement que la piste C1 demande
  précisément de déclarer avant de les croire.

---

*Aucune ligne de cette revue n'est un conseil en investissement. Aucun titre
n'est recommandé, aucune position dimensionnée, aucun cours prédit. Les trois
agents ont relu un protocole de mesure ; ils n'ont pas évalué si la règle vaut
d'être suivie.*

[← Le protocole](README.md) · [Le bilan de l'année](bilan-2025.md) ·
[La revue de l'expérience 1](../experience_1/review.md)
