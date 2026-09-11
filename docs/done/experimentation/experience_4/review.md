# Revue de l'expérience 4

> Relue par les trois agents du dépôt — [`chartiste`](../../../../.claude/agents/chartiste.md),
> [`trading`](../../../../.claude/agents/trading.md) et
> [`sorosien`](../../../../.claude/agents/sorosien.md) —, chacun sous son angle,
> puis soumise à leur vote. Quinze pistes, cinq retenues.

> ⚠️ **Aucune de ces pistes n'est un conseil en investissement.** Elles portent
> toutes sur le protocole — ce qu'il mesure, ce qu'il déclare, ce qu'il permet de
> conclure —, jamais sur un titre à acheter ou à vendre.

---

## 1. Ce qui a été relu

| Fichier | Rôle dans la revue |
|---|---|
| [`README.md`](README.md) | les paramètres d'entrée : univers quotidien point-in-time, TOP 10 des `TAUX_120`, achat sous `VAL_120 − 1 s` si `TAUX_20 > 0`, vente au-dessus de `VAL_120 + 1 s`, une décision par séance, coûts, `TR39`, issues déclarées, dimensionnement, taux d'étalonnage 2021 |
| [`bilan-2022.md`](bilan-2022.md) | le compte, les positions, le motif unique de vente, l'étalonnage recalculé, les issues, le fantôme, la comparaison avec l'expérience 3 |
| [`rapports/2022-01.md`](rapports/2022-01.md) … [`2022-12.md`](rapports/2022-12.md) | les douze journaux mensuels |
| `graphiques/` | 12 courbes de portefeuille et 499 figures de canal |
| `evaluations.csv` · `top10.csv` · `ordres.csv` · `signaux.csv` · `issues.csv` · `portefeuille.csv` · `fantome.csv` · [`univers.csv`](univers.csv) | les données brutes |
| [`journal.py`](journal.py) · [`journal.md`](journal.md) | le moteur et son miroir |
| [`chartiste.md`](chartiste.md) · [`actualites.md`](actualites.md) | les textes rédigés à la main |

Aucun fichier ne manquait.

### Les chiffres clés du bilan

| | |
|---|---|
| Performance 2022 | **+0,51 %** contre −10,18 % pour `TR39` |
| Alpha, écart de performance | +10,69 pt, effet minimal détectable ± 25,7 pt |
| Alpha de régression · bêta | +8,12 %/an ± 22,4 · 0,705 |
| Part investie moyenne | 68,0 % |
| Ordres · frais | 31 · 160,48 €, contre 75,24 € pour l'expérience 3 |
| Écart apparié à l'expérience 3 | +2,87 pt, EMD ± 27,2 pt |
| Écart au fantôme `SANS-P20` | +7,41 pt, EMD ± 16,7 pt |
| Taux d'étalonnage retrouvés | 20 sur 20 |
| `BANDE`, sous-échantillon | 55,0 % ± 3,1 pt, contre 68,3 % nominal |
| Critère 2 — sous le bord bas, dans le TOP 10 | +2,25 ± 2,16 pt sur 20 séances, « exclut zéro » |
| Lignes jamais revendues · signaux perdus faute de créneau | 1 · 23 sur 18 séances |
| Tracking error déclarée · réalisée | 15,58 · 13,13 %/an |

---

## 2. La contrainte A/B

Une expérience porte sur une période **passée**, dont le résultat est connu de qui
rédige la revue. Proposer « il aurait fallu un seuil à 40 % » en sachant ce qu'a
fait l'année, c'est du rétro-ajustement — le premier des
[cinq pièges de l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md).

> **Chaque piste doit être classée dans l'une des deux catégories, explicitement.**
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

La contrainte pèse double ici : **la règle de l'expérience 4 a elle-même été
formulée après avoir vu 2022**, et le README le déclare.

---

## 3. `chartiste` — la géométrie et les signaux

*Son angle : la bande à l'écart-type, la clôture lue au bord droit du canal
glissant, la linéarité de la droite de 120 séances, ce que les figures montrent
et masquent.*

### Ce qu'il a trouvé

- **L'explication du README par le levier est fausse.** Simulé avec le même
  estimateur `s`, un bruit i.i.d. donne 15,7 % de clôtures sous le bord bas et
  67,0 % dans la bande le lendemain ; une marche aléatoire, 25,7 % et 47,0 %. Le
  levier du dernier point **réduit** les sorties ; seule l'autocorrélation joue —
  celle d'`ECART_S` vaut 0,947 à une séance.
- **`BANDE` mesure surtout la persistance** : 86,9 % de maintien dans la bande
  depuis l'intérieur, 14,0 % de retour depuis le bord bas.
- **Le critère 2 ne tient pas date par date** : +1,86 ± 2,17 en retirant la
  moyenne de chaque date, +1,39 ± 2,67 (p = 0,29) en différences date par date.
  Ses 76 observations tiennent sur 21 dates, dont 10 le 2021-10-12.
- **Les effectifs sont gonflés par la persistance** : 284 évaluations candidates
  pour 120 épisodes ; 254 places du TOP 10 du sous-échantillon pour 75 séjours.
- **14 achats sur 16** ont lieu à la première séance hors bande.
- **Les ventes se lisent dans un canal qui a tourné** : sur 15 ventes, 9 à pente
  longue négative ou nulle, 8 dont le bord haut du jour est sous le prix
  d'achat, 10 sous le bord bas du canal de l'achat prolongé.
- **La droite de 120 séances est rarement une droite** : un saut unique décrit
  mieux la fenêtre dans 41,0 % des places du TOP 10 en 2021 et 81,1 % en 2022,
  contre 58,7 % pour une marche aléatoire de pente comparable ; Durbin–Watson
  médian 0,14.
- **`TAUX_120` favorise la volatilité** : `s_120/E_120` médian de 4,63 % dans le
  TOP 10, contre 3,79 % pour les autres pentes positives.

### Ses cinq pistes

#### C1 · Comparer la bande à une marche aléatoire, pas à 68,3 % — **A**

- **Classement** : l'erreur de sens du levier se voit dans le cours seul
  ([module 4, § 4.3](../../../raw/concept/semestre3/canal/04-sorties-de-canal.md)),
  sans aucune séance de 2022.
- **Ce qui change** : chaque taux de bande est publié avant la première séance à
  côté de deux références simulées (i.i.d. et marche aléatoire, même estimateur
  `s`) ; `BANDE` devient une matrice de passage 3 × 3 selon l'état de la veille ;
  la phrase « inférieure de 12,7 points à la garantie nominale » est remplacée.
- **Coût** : 40 000 tirages en Python pur, quelques secondes, aucun frais.
- **Mesure** : où tombe le taux observé entre les deux références. 55,0 %, IC
  date par date ± 6,1 pt sur 26 dates : les écarts de 8,0 pt à la marche aléatoire
  et de 12,0 pt au bruit i.i.d. sont tous deux hors de l'intervalle. Aucun effet
  sur la performance : la piste corrige une lecture.

#### C2 · Compter en épisodes et en dates, pas en évaluations — **A**

- **Classement** : le sous-échantillon traite le chevauchement dans le temps ;
  le regroupement par date et la persistance des états se lisent dans le
  protocole.
- **Ce qui change** : IC par différences date par date, Student à `dates − 1`
  degrés de liberté (`p_valeur_student()`) ; effectifs publiés aussi en épisodes
  et en séjours au TOP 10 ; durée de l'épisode publiée à l'achat.
- **Coût** : quelques dizaines de lignes dans `comparer()`. Le vrai coût est
  statistique : ramener le critère 2 à ± 1,7 pt demanderait environ cinq ans.
- **Mesure** : un test placebo par permutation à l'intérieur des dates — une
  convention juste « exclut zéro » près de 5 % du temps.

#### C3 · Publier le canal de l'achat à la vente — **A**

- **Classement** : « le canal tracé à la séance τ n'est valable qu'en τ »
  ([module 5, § 5.1](../../../raw/concept/semestre3/canal/05-canal-glissant.md)) ;
  acheter et vendre dans deux canaux différents se lit dans le texte de la règle.
- **Ce qui change** : pour chaque vente, `TAUX_120` à l'achat et à la vente, écart
  dans le canal de l'achat prolongé, bord haut du jour contre prix d'achat, et ce
  canal tracé en pointillés sur la figure ; l'issue `VENTE` mesurée sur la
  population réellement vendable (1 077 contre 3 246 sur l'audit).
- **Coût** : données déjà dans `evaluations.csv`, une couche SVG, aucun frais.
- **Mesure** : grandeurs descriptives sans erreur d'échantillonnage ; l'issue
  restreinte (63 contre 176 sur le sous-échantillon) a un EMD d'environ
  ± 2,0 pt, davantage date par date.

#### C4 · Vérifier que la droite de 120 séances est une droite — **A**

- **Classement** : le cours prescrit le contrôle de Durbin–Watson et avertit
  qu'« une pente longue peut ne plus exister » ; `TAUX_120 = r/E` favorise la
  volatilité par construction.
- **Ce qui change** : `DW_120`, R² d'un saut moins R² de la droite, date du saut,
  signe de la pente des 60 dernières séances et `r/s` dans `evaluations.csv` et
  sur les figures, publiés en distribution contre la marche aléatoire ; issue
  déclarée « mieux décrite par un saut », seuil zéro ; variante `VAR-RS`.
- **Coût** : environ 20 000 fenêtres en sommes cumulées, quelques secondes.
- **Mesure** : sur une fenêtre, le diagnostic ne sépare pas un saut d'une marche
  aléatoire (58,7 % de faux signalements) ; en distribution, 81,1 % contre 58,7 %
  sur 2 440 places. Issue séparée : EMD ≈ ± 1,8 pt.

#### C5 · Sortie lue dans le canal figé à l'achat — **B, déclarée**

- **Classement** : l'idée vient des 15 ventes de 2022 (9 à pente ≤ 0, dont 8
  pertes ; 6 à pente > 0, 6 gains) — un contraste en partie **mécanique**, la
  pente du jour de vente étant calculée sur la détention elle-même.
- **Ce qui change, pour une expérience suivante** : fantôme `CANAL-FIGE`, seuil de
  vente `VAL_120(achat) + r_120(achat)·Δ + s_120(achat)` ; publication d'abord du
  nombre de lignes jamais revendues.
- **Coût** : composition point-in-time 2019-2020 via `compocac.php` ; calcul
  négligeable ; 2020 est un seul régime.
- **Test honnête** : sur 2019-07 → 2020-11 ; seule la coupe transversale
  (`VENTE` séparée par signe de `TAUX_120`, ≈ ± 1,8 à 3,4 pt) a une chance ; le
  fantôme contre le portefeuille (± 16,7 pt/an) est non tranchable.

---

## 4. `trading` — la performance et la règle

*Son angle : alpha, bêta et exposition, coûts et cadence, construction de la
règle, validité des intervalles, dimensionnement.*

### Ce qu'il a trouvé

- **Le moteur est juste** : un rejeu indépendant retrouve au centime les 31
  ordres, la valeur finale, les frais, la part investie et les signaux perdus.
- **L'alpha de régression** est confirmé : t = 0,71, p = 0,48, ± 21,9 à 22,6 en
  erreurs Newey-West.
- **Le bêta n'est pas constant** : 0,860 ± 0,079 au premier semestre, 0,406
  ± 0,100 au second.
- **L'exposition explique l'essentiel** : une référence à exposition appariée
  fait −4,03 % ; l'exposition seule rend 6,15 des 10,69 pt, la sélection 4,54 pt.
- **La comparaison avec l'expérience 3 est plus bruitée que l'alpha brut** :
  13,86 %/an d'écart-type de la différence contre 13,13 pour la tracking error,
  avec un bêta résiduel de 0,323 ± 0,069.
- **« Une seule chose change » est faux** : admission à 120 contre 253 séances,
  divisions refusées au lieu d'arrêter le moteur, et état de départ — 4 séances à
  100 % en espèces contre 38,6 % en titres dès le 3 janvier pour l'expérience 3.
- **Le critère 2 ne tient pas** : ± 2,82 par grappes de dates (t = 1,56, p = 0,13,
  24 ddl) ; 5 phases sur 20 seulement excluent zéro ; +4,97 ± 3,05 en 2021,
  −1,01 ± 2,84 en 2022 ; une comparaison sur quatre.
- **Les lignes ont passé 294 de leurs 883 séances de détention** avec une pente
  longue négative.

### Ses cinq pistes

#### T1 · Des intervalles qui résistent à la date, à la phase et au nombre de tests — **A**

- **Classement** : 26 dates × 39 valeurs mesurées contre le même `TR39`, une phase
  parmi 20, quatre comparaisons plus `BANDE` au seuil de 5 % — tout se lit dans le
  README.
- **Ce qui change** : erreurs types par grappes de dates (Student à `G − 1`),
  publication des 20 phases, correction de Holm, EMD reprojetés avec l'effet de
  grappe ; « exclut zéro » imprimé seulement s'il tient sous les trois contrôles.
- **Coût** : aucune donnée, environ vingt fois la boucle de `comparer()`.
- **Mesure** : le rapport des erreurs types par grappes à Welch — 1,74 pour le
  TOP 10, 1,31 pour le critère 2, 1,17 pour le critère 3, 0,93 pour la vente — et
  la stabilité du verdict d'une phase à l'autre.

#### T2 · Séparer exposition et sélection — **A**

- **Classement** : le README écrit « aucun alpha ne se lit sans son exposition »
  mais ne publie qu'une part investie moyenne et un bêta unique, pour un
  portefeuille dont l'exposition varie par construction.
- **Ce qui change** : référence à exposition appariée et décomposition, bêta par
  semestre ; témoin aléatoire de 4 000 tirages aux mêmes dates et montants dans
  **deux réservoirs déclarés d'avance** (TOP 10 du jour ; univers) ; bêta de la
  différence avec l'expérience 3.
- **Coût** : aucune donnée, aucun frais, quelques secondes.
- **Mesure** : la largeur du témoin — EMD ± 10,2 pt dans le TOP 10, ± 15,4 dans
  l'univers, contre ± 25,7 pour l'alpha brut. Son résultat illustratif sur 2022
  est donné par l'agent **sans valeur probante**, et c'est pourquoi le réservoir
  qui fait foi doit être désigné avant.

#### T3 · Séparer la règle de la cadence — **A**

- **Classement** : le README écrit lui-même « la règle et sa cadence » — deux
  facteurs pour une comparaison — et trois autres différences ne sont pas
  déclarées.
- **Ce qui change** : un tableau de toutes les différences avec l'expérience 3,
  publié avant ; un portefeuille fictif « règle 4 à cadence mensuelle ». La
  quatrième combinaison (règle 3 quotidienne, ≈ 20 000 appels) est déclarée hors
  champ.
- **Coût** : une boucle de simulation, frais fictifs. En exécution réelle, la
  cadence coûte 160,48 € contre 75,24 €.
- **Mesure** : sur 2021 seul, la même règle donne 47,0 % investi à cadence
  mensuelle et 75,4 % à cadence quotidienne — 28 points, davantage que les 22,7
  qui séparent les expériences 3 et 4. L'effet sur l'alpha a un EMD de ± 17,0 pt,
  à écrire avant.

#### T4 · Dimensionner la règle sur elle-même — **A**

- **Classement** : la tracking error de 15,58 est empruntée à une autre règle et
  à une autre cadence ; l'exposition, le bêta, les frais et les EMD appariés ne
  sont pas projetés, alors que le moteur disposait déjà de 2021.
- **Ce qui change** : `simuler()` lancé sur les 258 séances d'étalonnage, et
  publication avant la première séance de toutes ces grandeurs, en fourchette.
- **Coût** : quelques secondes pour 2021 ; ajouter 2020 exige son univers.
- **Mesure** : projeté contre réalisé — tracking error 11,13 contre 13,13, part
  investie 75,4 contre 68,0 %, bêta 0,823 contre 0,705, frais 203,65 contre
  160,48 €. L'agent le dit : la tracking error n'est **pas mieux projetée**
  (écart relatif 0,165 contre 0,171) ; le gain porte sur les grandeurs qui
  n'étaient pas projetées du tout.

#### T5 · « La règle simplifiée fait mieux » : à tester sur des années neuves — **B, déclarée**

- **Classement** : ne se formule qu'à la lecture du résultat, sur une règle née
  de 2022 ; l'effet « établi » du critère 2 change de signe entre 2021 et 2022.
- **Ce qui change** : les codes des expériences 3 et 4 figés par empreinte
  **avant** d'importer 2023-2024, rejoués en parallèle, univers point-in-time,
  dimensionnement publié avant ; objet déclaré = les taux et une seule issue
  primaire, le critère 2 par grappes.
- **Coût** : séries 2023-2024, deux univers, deux `TR39`.
- **Test honnête** : performance appariée **non testable** (± 23,6 pt sur un an,
  ≈ 22 ans pour 5 pt/an) ; critère 2 testable à ≈ ± 2,8 pt sur 20 séances.

---

## 5. `sorosien` — la réflexivité

*Son angle : le protocole voit-il les séquences auto-renforçantes entre cours et
fondamentaux, et qu'a coûté l'abandon du registre réflexif ?*

### Ce qu'il a trouvé

- **La règle ne s'exerce presque jamais dans le champ réflexif** déclaré par
  [`canaux.csv`](../experience_3/canaux.csv) de l'expérience 3 : 1 achat sur 16,
  13 signaux sur 40, 18,3 % des places du TOP 10 en 2022 contre 31,9 % en 2021,
  pour une part stable de l'univers (26,0 puis 25,6 %).
- **La grille de phases de l'expérience 3 ne peut pas contenir un candidat** :
  sur 284, 230 hors champ, 50 `AUCUNE SEQUENCE`, 4 `AUTO-RENFORCEMENT`,
  0 `RETOURNEMENT` — `AUTO-RENFORCEMENT` exige une position au-dessus de 65 % et
  `RETOURNEMENT` une `TEND_120` négative.
- **Trois grandeurs ne sont jamais mesurées** : la `GRANDEUR` du canal, chargée par
  le moteur de l'expérience 3 mais jamais lue ; le volume, absent du moteur de
  l'expérience 4 ; les fondamentaux de 2021-2022, absents du dépôt.
- **Le repli acheté n'est pas un test** : repli médian de −3,2 % depuis le plus
  haut sur 120 séances pour les candidats de 2021, 2 sur 210 à −10 % ; volume
  relatif médian de 0,75× en 2021.
- **Deux des trois valeurs refusées pour division** (`ATO.PA`, `WLN.PA`) ont un
  canal déclaré — une information postérieure à ne pas lire comme un signal.
- **Conclusion retenue : aucune séquence réflexive identifiable.** Il manquerait
  la grandeur du canal, le volume, une phase datée par un test réussi, et les
  fondamentaux de la période.

### Ses cinq pistes

#### S1 · Le verrou comme variable de découpage, pas comme registre — **A**

- **Classement** : le README pose lui-même que les thèses ne dépendent pas de la
  règle ; ce qui manque est ce qui en dépend, le croisement — visible avant 2022.
- **Ce qui change** : une colonne `CHAMP` (canal / aucun) sur évaluations, TOP 10,
  signaux, ordres et issues ; les issues du bilan découpées par champ.
- **Coût** : une jointure sur un fichier du dépôt, aucun frais.
- **Mesure** : des comptes exacts ; EMD projetés ± 1,7 pt (TOP 10), ± 2,9 pt (sous
  le bord bas), ± 9,4 pt pour les candidats, **à déclarer non tranchable**. Gain en
  validité, pas en puissance.

#### S2 · Mesurer la grandeur du canal déclaré — **A**

- **Classement** : `GRANDEUR` déclarée puis jamais lue — reprise de la piste S2 de
  la [revue de l'expérience 2](../experience_2/review.md), jamais appliquée.
- **Ce qui change** : `ACTIONS` point-in-time et sa variation sur 250 séances,
  `DETTE_EBITDA` et `P_B` quand disponibles ; verdict « observé », « non
  observé » ou « champ déclaré, canal non vérifiable ».
- **Coût** : onze appels `get_shares_full` ; les ratios 2021-2022 resteront
  probablement vides.
- **Mesure** : binaire par valeur. **Non mesurable au sens d'un intervalle**, et
  déclaré comme tel.

#### S3 · Le volume comme covariable — **A**

- **Classement** : `Volume` est dans chaque série et jamais lu ; les phases de
  confirmation s'y lisent.
- **Ce qui change** : volume relatif 20/250 publié dans `evaluations.csv`, dans
  chaque motif et chaque note, comme covariable des issues, jamais comme
  condition ; seuil 1,5× déclaré **vide en année calme** (0 sur 746 en 2021).
- **Coût** : calcul sur des colonnes existantes ; cas limite de Stellantis avant
  sa 250ᵉ séance réelle.
- **Mesure** : corrélation de rang avec `EXCES_20`, IC ≈ ± 0,23 sur les places sous
  le bord bas, ± 0,13 sur le TOP 10.

#### S4 · Le test réussi comme seule phase affirmable — **A**

- **Classement** : les phases de l'expérience 3 ne peuvent pas contenir un
  candidat, ce qui se voit dans leurs définitions.
- **Ce qui change** : épisodes de candidature ; repli depuis le plus haut sur 120
  séances ; issue déclarée « test réussi » (nouveau plus haut dans 60 séances),
  « rupture » (`TEND_120` = −1 pendant 20 séances), « ni l'un ni l'autre » ou
  « non tranchée » ; découpage par champ — hors champ, c'est du momentum.
- **Coût** : calcul sur les séries existantes.
- **Mesure** : ≈ 60 épisodes sur l'audit, ± 12,7 pt ; ≈ 15 dans le champ, ± 25 pt,
  non tranchable et déclaré.

#### S5 · Le TOP 10 sort-il du champ quand les pentes positives se raréfient ? — **B, déclarée**

- **Classement** : né du contraste 2021-2022 (31,9 puis 18,3 % des places ; 33
  puis 14 pentes positives en médiane).
- **Ce qui change, pour une expérience suivante** : une seule hypothèse, sur des
  années jamais rejouées, testée par corrélation continue sans seuil ;
  `canaux.csv` redéclaré pour tout nouvel entrant avant la première séance.
- **Coût** : environ 40 séries et les compositions des nouvelles années.
- **Test honnête** : IC ≈ ± 10,5 pt en places indépendantes, mais l'unité honnête
  est la date — **deux ans ne trancheront probablement pas** ; en viser quatre.

---

## 6. La synthèse

### Les quinze pistes

Triées par catégorie, puis par coût croissant.

| Id | Titre | Cat. | Coût | Mesurable ? |
|---|---|---|---|---|
| S1 | Le verrou comme variable de découpage | A | une jointure | comptes exacts ; candidats non tranchables |
| C3 | Le canal de l'achat publié à la vente | A | colonnes existantes, une couche SVG | descriptif ; `VENTE` restreinte ≈ ± 2,0 pt |
| C1 | La bande contre une marche aléatoire | A | quelques secondes de simulation | oui, ± 6,1 pt date par date |
| C2 | Compter en épisodes et en dates | A | quelques lignes ; cinq ans pour ± 1,7 pt | oui, par placebo |
| T1 | Intervalles par grappes, phases et Holm | A | vingt fois une boucle | oui, rapport des erreurs types |
| S3 | Le volume comme covariable | A | colonnes existantes | IC de rang ± 0,13 à ± 0,23 |
| C4 | La droite est-elle une droite ? | A | quelques secondes | en distribution ; issue ≈ ± 1,8 pt |
| S4 | Le test réussi, par épisode | A | séries existantes | ± 12,7 pt ; ± 25 pt dans le champ |
| T2 | Exposition contre sélection, témoin aléatoire | A | quelques secondes | EMD ± 10,2 à ± 15,4 pt |
| T4 | Dimensionner la règle sur elle-même | A | une simulation 2021 | projeté contre réalisé |
| T3 | Séparer la règle de la cadence | A | un portefeuille fictif | exposition oui ; alpha ± 17,0 pt |
| S2 | Mesurer la grandeur du canal | A | onze appels réseau, données partielles | **non**, binaire |
| C5 | Fantôme `CANAL-FIGE` | **B** | univers 2019-2020 | coupe transversale seulement |
| S5 | Largeur du marché et champ réflexif | **B** | séries d'années neuves | deux ans insuffisants |
| T5 | Rejeu des deux règles, code figé | **B** | séries et univers 2023-2024 | critère 2 oui ; performance non |

### Le décompte

**12 pistes A, 3 pistes B** — quatre A et une B par agent. Les trois pistes B sont
déclarées comme telles et accompagnées d'un protocole de test sur une autre
période.

### Les convergences

- **Le seul résultat positif du bilan ne tient pas.** `chartiste` et `trading`,
  par deux méthodes différentes, trouvent que le critère 2 cesse d'exclure zéro
  dès qu'on tient compte du regroupement par date. Le § 13 du bilan écrit pourtant
  qu'il « établit » ce que ce critère sépare.
- **La dépendance entre observations n'est traitée qu'à moitié.** C2 et T1
  décrivent le même défaut : le sous-échantillon règle le chevauchement dans le
  temps, pas la corrélation entre valeurs d'une même date ni la persistance des
  états.
- **Une piste B de rejeu sur années neuves, code figé avant l'import** : C5 et T5
  convergent sur le même protocole.
- **Le canal glissant tourne sous la règle.** `chartiste` (9 ventes sur 15 à pente
  ≤ 0) et `trading` (294 séances de détention sur 883 à pente négative) mesurent
  le même phénomène par deux bouts.
- **Le repli acheté est peu profond** : `chartiste` (achat à la première séance
  hors bande, 14 sur 16) et `sorosien` (repli médian −3,2 % en 2021) le constatent
  chacun sous son angle.

### Désaccords chiffrés, signalés sans trancher

| Grandeur | `chartiste` | `trading` | Bilan |
|---|---|---|---|
| Critère 2, intervalle tenant compte des dates | +1,39 ± 2,67 pt (différences date par date, 20 dates, p = 0,29) ; +1,86 ± 2,17 (moyenne de date retirée) | +2,25 ± 2,82 pt (grappes de dates, 24 ddl, p = 0,13) | +2,25 ± 2,16 pt |
| `BANDE`, IC du sous-échantillon | ± 6,1 pt, date par date | — | ± 3,1 pt |

Les méthodes diffèrent, les conclusions concordent : aucune ne laisse le critère 2
exclure zéro. La version retenue de T1 devra **déclarer une seule convention avant
le dépouillement**, comme `trading` l'a demandé en votant.

### Erreurs signalées dans l'expérience, non corrigées

La revue les consigne ; elle ne modifie pas l'expérience.

| Où | Signalé par | Ce qui est signalé |
|---|---|---|
| [README](README.md#les-taux-détalonnage--publiés-avant-la-première-séance), premier constat de l'étalonnage | `chartiste` | l'excès de sorties sous le bord bas est attribué au levier maximal ; le levier les **réduit**, seule l'autocorrélation joue |
| [Bilan § 13](bilan-2022.md#13-ce-que-lexpérience-établit-et-ce-quelle-nétablit-pas) | `chartiste`, `trading` | « établit » que le critère 2 sépare son issue, sur un intervalle qui ne résiste pas au regroupement par date |
| [Bilan § 9](bilan-2022.md#9-la-comparaison-appariée-avec-lexpérience-3) et README | `trading` | « une seule chose change » : l'admission, le traitement des divisions et l'état de départ changent aussi |
| [Bilan § 3](bilan-2022.md#3-les-positions) | `trading` | la contribution de la ligne encore ouverte n'intègre pas ses frais de vente (≈ 2,7 €) ; l'alpha par position rapporte une ouverture à ouverture à un `TR39` de clôture à clôture |
| Étalonnage 2021 | `trading` | les issues de 2021 sont mesurées contre un `TR39` composé des 39 valeurs de 2022 : Eurofins y figure avant son entrée, Atos en est absente |

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

Chaque agent classe **exactement cinq** pistes : 5, 4, 3, 2 et 1 point. Trois
bulletins, 45 points. Un agent peut voter pour ses propres pistes, et son
bulletin le montre. Départage : total, puis nombre d'agents distincts, puis A
avant B, puis identifiant alphabétique.

### Les trois bulletins

**`chartiste`** — une piste propre sur cinq

| Rang | Piste | Points | Pourquoi |
|---|---|---|---|
| 1 | T1 | 5 | la seule qui fait tomber une conclusion déjà écrite : 5 phases sur 20, +4,97 en 2021, −1,01 en 2022 |
| 2 | T3 | 4 | ferme une faille dans la déclaration centrale « une seule chose change » |
| 3 | T4 | 3 | un dimensionnement calculé sur la règle même rend l'écart projeté/réalisé mesurable |
| 4 | T2 | 2 | empêche de lire comme sélection ce qui vient de l'exposition |
| 5 | C1 *(propre)* | 1 | rend réfutable la seule affirmation que la règle engage à chaque séance |

**`trading`** — trois pistes propres sur cinq

| Rang | Piste | Points | Pourquoi |
|---|---|---|---|
| 1 | T1 *(propre)* | 5 | empêche dès le prochain bilan une conclusion déjà publiée à tort |
| 2 | T3 *(propre)* | 4 | sans le portefeuille à cadence mensuelle, la comparaison appariée n'attribue rien à la règle |
| 3 | C1 | 3 | donne à `BANDE` une référence nulle honnête et corrige une explication fausse |
| 4 | T2 *(propre)* | 2 | rend la sélection mesurable, deux à trois fois plus précisément que l'alpha brut |
| 5 | C3 | 1 | l'issue `VENTE` est testée sur tout l'univers alors que la règle ne vend que des lignes détenues |

Il écarte T4, sa propre piste : sa projection de la tracking error n'était pas
meilleure que celle déclarée.

**`sorosien`** — aucune piste propre, volontairement

| Rang | Piste | Points | Pourquoi |
|---|---|---|---|
| 1 | T1 | 5 | s'attaque à la seule conclusion positive du bilan avant que la suivante la reprenne |
| 2 | T3 | 4 | la comparaison « la mieux posée de la série » repose sur une affirmation fausse |
| 3 | T4 | 3 | comble un trou de déclaration : le dimensionnement était emprunté |
| 4 | C1 | 2 | 68,3 % n'est justifié par aucune hypothèse nulle réaliste |
| 5 | T2 | 1 | l'exposition explique déjà 6,15 des 10,69 points |

Il écarte ses propres pistes : S1 ferme une faille que ce protocole n'ouvre pas —
l'expérience 4 ne revendique aucune réflexivité — ; S2 n'est pas mesurable ; S3 et
S4 portent sur des effectifs trop petits dans le champ.

### Le tableau des quinze

| Rang | Piste | Cat. | `chartiste` | `trading` | `sorosien` | **Total** | Soutiens |
|---|---|---|---|---|---|---|---|
| 1 | **T1** | A | 5 | 5 | 5 | **15** | 3 |
| 2 | **T3** | A | 4 | 4 | 4 | **12** | 3 |
| 3 | **C1** | A | 1 | 3 | 2 | **6** | 3 |
| 4 | **T4** | A | 3 | — | 3 | **6** | 2 |
| 5 | **T2** | A | 2 | 2 | 1 | **5** | 3 |
| 6 | C3 | A | — | 1 | — | 1 | 1 |
| 7 | C2 | A | — | — | — | 0 | 0 |
| 8 | C4 | A | — | — | — | 0 | 0 |
| 9 | S1 | A | — | — | — | 0 | 0 |
| 10 | S2 | A | — | — | — | 0 | 0 |
| 11 | S3 | A | — | — | — | 0 | 0 |
| 12 | S4 | A | — | — | — | 0 | 0 |
| 13 | C5 | B | — | — | — | 0 | 0 |
| 14 | S5 | B | — | — | — | 0 | 0 |
| 15 | T5 | B | — | — | — | 0 | 0 |
| | | | **15** | **15** | **15** | **45** | |

C1 et T4 sont à égalité de points ; C1 passe devant par ses trois soutiens contre
deux.

### Les cinq pistes retenues

#### 1. T1 — Des intervalles qui résistent à la date, à la phase et au nombre de tests · 15 points, 3 soutiens, A

**Ce qu'elle change** : les issues déclarées se jugent sur des erreurs types par
grappes de dates, sur les 20 phases possibles du sous-échantillon et après
correction de Holm ; « exclut zéro » n'est imprimé que s'il tient sous les trois.

**Pourquoi retenue** : la seule conclusion positive du bilan — le critère 2 —
repose sur un intervalle qui ne résiste ni aux dates, ni à la phase, ni au nombre
de tests. Les trois agents la placent en tête : elle empêche une conclusion
abusive de passer dans l'expérience suivante.

#### 2. T3 — Séparer la règle de la cadence · 12 points, 3 soutiens, A

**Ce qu'elle change** : un tableau de toutes les différences avec l'expérience 3,
publié avant, et un portefeuille fictif « règle 4 à cadence mensuelle » qui
sépare l'effet de la règle de celui de la cadence.

**Pourquoi retenue** : la comparaison appariée, présentée comme la mieux posée de
la série, mêle au moins cinq différences dont trois non déclarées ; sur 2021, la
cadence seule déplace l'exposition de 28 points.

#### 3. C1 — Comparer la bande à une marche aléatoire, pas à 68,3 % · 6 points, 3 soutiens, A

**Ce qu'elle change** : les taux de bande et `BANDE` sont publiés avant la première
séance contre deux références simulées — bruit i.i.d. et marche aléatoire — et
`BANDE` devient une matrice de passage selon l'état de la veille.

**Pourquoi retenue** : `BANDE` est la seule affirmation que la règle engage à
chaque séance, et elle était jugée contre une valeur qu'aucune série de cours ne
respecte, avec une explication de sens contraire à la réalité.

#### 4. T4 — Dimensionner la règle sur elle-même · 6 points, 2 soutiens, A

**Ce qu'elle change** : la règle est simulée sur la fenêtre d'étalonnage avant la
première séance, et sa tracking error, son bêta, son exposition, ses frais et les
EMD de ses comparaisons appariées sont publiés en fourchette, puis confrontés au
réalisé.

**Pourquoi retenue** : le dimensionnement de l'expérience 4 était emprunté à une
autre règle et à une autre cadence. La projection de la tracking error n'en est
pas meilleure, et `trading` l'a écartée pour cette raison ; le gain porte sur les
grandeurs qui n'étaient pas projetées du tout.

#### 5. T2 — Séparer exposition et sélection · 5 points, 3 soutiens, A

**Ce qu'elle change** : une référence à exposition appariée, un bêta par semestre,
et un témoin aléatoire aux mêmes dates et montants dans un réservoir **désigné
avant** la première séance.

**Pourquoi retenue** : l'exposition rend 6,15 des 10,69 points d'écart ; sans
témoin, aucun écart ne s'attribue à la sélection, et le témoin est deux à trois
fois plus précis que l'alpha brut.

### Les fusions proposées

| Fusion | Proposée par | Ce qu'elle garde |
|---|---|---|
| **C2 dans T1** | les trois agents | les grappes, les phases et Holm de T1 ; les effectifs en épisodes et en séjours au TOP 10 et la durée d'épisode à l'achat de C2 — avec **une seule convention d'intervalle**, déclarée avant |
| **C5 dans T5** | les trois agents | un seul rejeu B à code figé par empreinte ; `CANAL-FIGE` comme fantôme déclaré à l'intérieur. `trading` note que 2019-07 → 2020-11 sert d'historique à l'étalonnage 2021 et est donc moins neuve que 2023-2024 |
| S3 dans S4 | `sorosien` | le volume relatif sert à qualifier la « rupture » |
| S2 subordonnée à S1 | `sorosien` | on ne mesure pas un canal sur une valeur dont le champ n'est pas déclaré |

Recouvrements partiels, sans fusion : T3 et T4 peuvent partager la même
simulation d'étalonnage ; C3 mesure le canal de l'achat que C5 transforme en
règle.

**Aucune des cinq pistes retenues ne touche la règle d'achat ou de vente.** Toutes
portent sur ce que l'expérience suivante pourra démontrer, et toutes sont de
catégorie A.

---

## 8. Ce que cette revue ne peut pas établir

- **Qu'une piste appliquée aurait amélioré le résultat.** Il faudrait rejouer 2022
  en la connaissant, ce qui est le rétro-ajustement même. Les cinq pistes retenues
  ne promettent d'ailleurs aucun gain : elles rendent des conclusions plus sûres ou
  plus rares.
- **Quelle convention d'intervalle est la bonne.** `chartiste` et `trading`
  proposent deux calculs qui rendent des chiffres différents ; les deux concordent
  sur la conclusion, et la revue ne tranche pas entre eux.
- **Que les chiffres recalculés par les agents sont exacts.** Ils viennent de
  scripts écrits pour cette revue, hors du dépôt, et n'ont pas été recoupés entre
  eux au-delà des désaccords signalés au § 6.
- **Que la règle est bonne ou mauvaise.** L'alpha reste plus petit que son effet
  minimal détectable, et la règle a été formulée après avoir vu l'année qu'elle
  joue.
- **Qu'aucune séquence réflexive n'existait en 2022.** `sorosien` conclut qu'aucune
  n'est *identifiable* avec ce que le dépôt contient ; il nomme ce qui manquerait
  pour en identifier une.

---

[← Protocole](README.md) · [Bilan](bilan-2022.md) · [Janvier](rapports/2022-01.md) · [Décembre](rapports/2022-12.md) · [Revue de l'expérience 2](../experience_2/review.md)
