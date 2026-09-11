# Expérience 5 — l'expérience 4, remesurée par les pistes de sa revue

L'expérience 4 **tout entière** — même année 2022, même univers, même règle,
mêmes coûts, même portefeuille —, à laquelle sont appliquées les **cinq pistes
retenues par le vote** de sa [revue](../experience_4/review.md).

Aucune de ces cinq pistes ne touche la règle d'achat ou de vente. Elles
changent **ce que l'expérience mesure, ce qu'elle déclare, et ce qu'elle
s'autorise à conclure**.

| Rang au vote | Piste | Ce qu'elle change |
|---|---|---|
| 1 | **T1** | les intervalles des issues déclarées : grappes de dates, vingt phases, correction de Holm — avec les apports de **C2**, que les trois agents ont proposé d'y fusionner |
| 2 | **T3** | la comparaison avec l'expérience 3 : toutes les différences déclarées, et un portefeuille fictif **`MENSUEL`** qui sépare la règle de sa cadence |
| 3 | **C1** | la bande jugée contre deux références simulées — bruit i.i.d. et marche aléatoire — au lieu de 68,3 % |
| 4 | **T4** | le dimensionnement calculé **sur la règle elle-même**, par simulation de 2021, publié ici |
| 5 | **T2** | l'exposition séparée de la sélection : référence à exposition appariée, bêtas semestriels, témoin aléatoire |

Les dix autres pistes de la revue **ne sont pas appliquées**.

---

## ⚠️ Ce que remesurer 2022 peut établir, et ce qu'il ne peut pas

**Le portefeuille est celui de l'expérience 4, à l'identique, par construction.**
La règle, les données et le calendrier sont les mêmes : 31 ordres, 10 051,09 € au
30 décembre. Le moteur le vérifie contre
[`ordres.csv`](../experience_4/ordres.csv) et
[`portefeuille.csv`](../experience_4/portefeuille.csv) de l'expérience 4, et
**s'arrête** au premier écart. Une remesure qui changerait le mesuré ne serait
plus une remesure.

**L'objet de l'expérience 5 n'est donc pas la performance.** C'est de savoir :

1. quelles conclusions de l'expérience 4 **survivent** à une mesure correcte de
   leur incertitude (T1) ;
2. ce qui, dans l'écart à `TR39` et à l'expérience 3, revient à **l'exposition**,
   à **la sélection** et à **la cadence** (T2, T3) ;
3. où se situe la bande entre **deux hypothèses nulles réalistes** (C1) ;
4. si une règle **dimensionnée sur elle-même** se projette mieux qu'une règle
   dimensionnée sur une autre (T4).

**Ce qui est déjà vu.** La revue a donné un avant-goût de plusieurs résultats sur
2022 : l'intervalle du critère 2 par grappes (± 2,82, p = 0,13), sa stabilité sur
les phases (5 sur 20), le rang du témoin aléatoire (z = +1,96 dans le TOP 10,
+0,60 dans l'univers), la part de l'écart due à l'exposition (6,15 points sur
10,69). **Les conventions ci-dessous sont fixées en connaissant ces aperçus.**
Chaque choix qui y est exposé porte la mention **⚠️ choisi en connaissant**, et
dit pourquoi il ne peut pas avoir été calé sur eux.

> **Conséquence, déclarée avant la première ligne de code.** Les conclusions de
> l'expérience 5 sur 2022 ne sont pas aveugles. Ses **conventions**, elles, sont
> de catégorie A, et elles valent pour une expérience suivante sur une année
> neuve — c'est là qu'elles pourront démontrer quelque chose.

---

## Ce qui est repris de l'expérience 4, sans changement

Le protocole complet et ses justifications sont dans le
[README de l'expérience 4](../experience_4/README.md). Rien n'y est retouché.

| | |
|---|---|
| Dotation · lignes | **10 000 €** au 3 janvier 2022 · **5** au maximum |
| Univers | tout le CAC 40 à sa composition **du jour**, [`univers.csv`](univers.csv), repris à l'identique |
| Référence | `TR39`, rendement total ; `^FCHI` nu pour mémoire |
| Fenêtres | étalonnage 258 séances de 2021 · narrée 257 séances de 2022 · audit 515 |
| Calendrier | décision à la **clôture** de chaque séance, exécution à l'**ouverture** suivante |
| TOP 10 | les dix `TAUX_120` strictement positifs les plus élevés de l'univers du jour |
| Achat | TOP 10, **clôture sous `VAL_120 − 1 s`**, **`TAUX_20 > 0`**, non détenue ; espèces divisées par les créneaux libres ; titres entiers |
| Vente | **clôture au-dessus de `VAL_120 + 1 s`**, motif unique |
| Coûts | 0,530 % l'aller-retour, TTF exemptée pour Airbus, Stellantis, ArcelorMittal, STMicroelectronics |
| Divisions postérieures | Air Liquide, Atos, Worldline : ordre d'achat **refusé**, créneau rendu au candidat suivant |
| Issues | rendement excédentaire sur 20 séances contre `TR39` ; énoncé `BANDE` |
| Fantôme | `SANS-P20` |
| Variantes mesurées | `VAR-TOP5`, `VAR-TOP20`, `VAR-K05`, `VAR-K15` |
| Figures · notes · actualités | redessinées aux mêmes dates ; [`chartiste.md`](chartiste.md) et [`actualites.md`](actualites.md) repris de l'expérience 4 |

---

## T1 — Une convention d'intervalle, déclarée une fois

C'est la première piste du vote, classée en tête par les trois agents : le seul
résultat positif du bilan de l'expérience 4 — le critère 2, +2,25 ± 2,16 points —
reposait sur un intervalle qui suppose indépendantes 39 valeurs mesurées le même
jour contre le même `TR39`.

### L'erreur type par grappes de dates

Pour une comparaison entre un groupe testé $A$ et un groupe témoin $B$ d'une même
population, de moyennes $\bar y_A$ et $\bar y_B$, la différence est
$\Delta = \bar y_A - \bar y_B$, et chaque date $g$ du sous-échantillon apporte

$$u_g = \sum_{i \in A \cap g} \frac{y_i - \bar y_A}{n_A} - \sum_{i \in B \cap g} \frac{y_i - \bar y_B}{n_B}.$$

$$\widehat{\operatorname{Var}}(\Delta) = \frac{G}{G-1}\sum_{g=1}^{G} u_g^2, \qquad
\text{IC95} = \Delta \pm t_{G-1;\,0{,}975}\sqrt{\widehat{\operatorname{Var}}(\Delta)}$$

où $G$ est le nombre de dates portant **au moins une** issue tranchée dans la
population comparée. La p-valeur bilatérale et le quantile viennent de
`p_valeur_student()` de [`python/import_societe.py`](../../../../python/import_societe.md),
réutilisée et non réécrite. L'intervalle de Welch de l'expérience 4 reste publié
en regard, étiqueté comme tel.

> ⚠️ **Choisi en connaissant.** La revue a proposé deux conventions : ces grappes
> (T1) et les différences calculées date par date (C2). Les deux aperçus
> concordent — aucune ne laisse le critère 2 exclure zéro —, donc le choix ne
> peut pas avoir été fait pour le sauver ou pour le perdre. Les grappes sont
> retenues parce qu'elles **gardent la question de l'expérience 4** — la
> différence des moyennes regroupées — et ne corrigent que son incertitude ; les
> différences date par date pondèrent chaque date également, ce qui change la
> question.

### Les vingt phases

Le sous-échantillon d'une séance sur vingt peut commencer à l'une de vingt
séances. La **phase 0** est celle de l'expérience 4, qui commence le 2020-12-31 ;
c'est elle qui donne le nombre publié. **Les vingt phases** sont calculées et
publiées : étendue des différences, et nombre de phases dont l'intervalle exclut
zéro avec le signe de la phase 0.

### La correction de Holm

Les quatre comparaisons déclarées — `TOP10`, `CRITERE-2`, `CRITERE-3`, `VENTE` —
forment une famille, au risque global de 5 %. Leurs p-valeurs de la phase 0 sont
ordonnées, $p_{(1)} \le \dots \le p_{(4)}$, et $p_{(k)}$ est rejetée tant que
$p_{(j)} \le 0{,}05/(5-j)$ pour tout $j \le k$. L'énoncé `BANDE` n'en fait pas
partie : il se juge contre ses références (C1), pas contre zéro.

### Le verdict, et sa règle

> **Déclaration.** Une comparaison **sépare son issue** si et seulement si les deux
> conditions sont réunies :
>
> 1. elle est **rejetée par Holm** à la phase 0, avec l'erreur type par grappes ;
> 2. son intervalle par grappes **exclut zéro, avec le même signe, dans au moins
>    11 phases sur 20**.
>
> Sinon elle **ne sépare pas**. Une comparaison dont un groupe a moins de deux
> observations, ou moins de trois dates, est **non mesurable**.

> ⚠️ **Choisi en connaissant.** L'aperçu donne au critère 2 cinq phases sur vingt.
> N'importe quel seuil supérieur à cinq le fait échouer ; il faudrait descendre à
> cinq ou moins pour le faire passer. Le seuil de onze est la **majorité**, le
> seul qui ne se choisisse pas : un verdict qui s'inverse selon le jour où l'on
> commence à compter n'est pas un résultat.

### Les apports de C2

Publiés, sans entrer dans aucun verdict :

- les effectifs en **épisodes** — une suite ininterrompue de séances d'audit où la
  valeur est candidate — et en **séjours** au TOP 10 ;
- pour chaque achat, la **durée de l'épisode** au jour de la décision : séances
  consécutives sous le bord bas, et séances consécutives de candidature.

### Les effets minimaux détectables, reprojetés

Calculés sur la phase 0 de l'étalonnage 2021 — douze dates tranchées —, puis
projetés sur les quelque vingt-quatre dates de l'audit par
$\text{EMD} \approx t_{25} \cdot \text{SE}_{2021}/\sqrt 2$ :

| Élément | EMD projeté par l'expérience 4 | Rapport grappes / Welch, 2021 | **EMD projeté par grappes** |
|---|---|---|---|
| `TOP10` | ± 0,9 pt | 1,87 | **± 2,0 pt** |
| `CRITERE-2` | ± 1,7 pt | 1,25 | **± 2,9 pt** |
| `CRITERE-3` | ± 3,1 pt | 1,23 | **± 5,1 pt** |
| `VENTE` | ± 1,0 pt | 1,09 | **± 1,1 pt** |

> Le TOP 10 est l'élément que le regroupement par date frappe le plus — ses dix
> places d'une même date bougent ensemble — et son effet minimal détectable
> **double**. Le déclarer avant évite de découvrir au bilan qu'un écart « séparé »
> n'était que la séance commune.

---

## T3 — La règle et sa cadence, séparées

Le bilan de l'expérience 4 écrivait de la comparaison avec l'expérience 3 :
« une seule chose change ». **C'est faux**, et la revue l'a établi.

### Toutes les différences entre les expériences 3 et 4, déclarées

| Élément | Expérience 3 | Expériences 4 et 5 | Effet sur 2022 |
|---|---|---|---|
| **Règle** | score à cinq composantes, quatre vetos, rang ≤ 5 / > 7 | TOP 10 et bande ± 1 s, motif unique de vente | — |
| **Cadence** | une décision par mois | une décision par séance | — |
| **Lecture géométrique** | encadrement convexe, fenêtre 120, tolérance 0,25 σ | canal de régression, fenêtres 120 et 20 | — |
| **Admission** | 253 séances de volume positif | 120 séances | Stellantis évaluable dès la décision du 2021-12-31 ici, dès celle du 2022-01-31 là-bas |
| **Divisions postérieures** | le moteur **s'arrête** au premier ordre | l'ordre est **refusé** | aucun ordre concerné en expérience 3 ; un refus en expérience 4 |
| **Univers** | composition aux fins de mois | composition du jour, dates exactes | aucun mouvement en 2022 |
| **Registre des thèses** | `CANAL` et `REFLEXIVE` | non reconduit | aucun sur les ordres |
| **État de départ** | 38,6 % investi à la clôture du 2022-01-03 | intégralement en espèces jusqu'au 2022-01-07 | **conséquence** de la règle et de la cadence, pas un paramètre |

### Le portefeuille fictif `MENSUEL`

La **règle de l'expérience 4**, appliquée au **calendrier de l'expérience 3** :
décision à la dernière séance de chaque mois, du 2021-12-31 au 2022-11-30,
exécution à l'ouverture de la première séance du mois suivant. Tout le reste est
identique : TOP 10, critères, vente, créneaux, coûts, refus des divisions. Il
n'engage pas un euro.

| Écart | Ce qu'il mesure |
|---|---|
| **Expérience 5 − `MENSUEL`** | l'effet de la **cadence**, à règle égale |
| **`MENSUEL` − expérience 3** | l'effet de la **règle**, avec l'admission et le traitement des divisions, **inséparables** sur cette fenêtre |

La quatrième combinaison — la règle de l'expérience 3 à cadence quotidienne —
demanderait environ 20 000 appels à `generer_graph_decision.py`. Elle est
**déclarée hors champ**.

---

## C1 — La bande contre deux références honnêtes

### La correction d'une explication fausse

Le README de l'expérience 4 attribuait l'excès de clôtures sous le bord bas —
23,6 % au lieu de 15,9 % — **au levier maximal** de la séance courante et à
l'autocorrélation. **Le levier joue en sens inverse.** Un résidu de bord a un
écart-type plus petit que les autres
([module 4, § 4.3 b](../../../raw/concept/semestre3/canal/04-sorties-de-canal.md#b-sans-studentisation-les-sorties-de-bord-sont-manquées)),
et sort donc **moins** souvent. Seule l'autocorrélation
([§ 4.3 c](../../../raw/concept/semestre3/canal/04-sorties-de-canal.md#c-lautocorrélation-encore))
explique l'excès. La simulation ci-dessous le montre : sous bruit i.i.d., 15,3 %
des clôtures sortent par le bas — un peu moins que les 15,9 % d'une loi normale.

### Les deux références, simulées avec l'estimateur du protocole

Chaque tirage produit 121 valeurs gaussiennes, régresse les 120 premières sur
$t = 1 \dots 120$, calcule $s_{120}$ comme le protocole, lit l'état de la 120ᵉ
valeur dans sa bande et celui de la 121ᵉ dans la bande prolongée d'un pas.
**20 000 tirages** par référence, générateur congruentiel linéaire du
[module 2](../../../raw/concept/semestre3/canal/02-les-trois-largeurs.md#20--la-série-qui-sert-aux-trois-figures),
**graine 1** pour le bruit i.i.d., **graine 2** pour la marche aléatoire sans
dérive. Incertitude de Monte-Carlo : ± 0,7 point sur une proportion.

| | Sous le bord bas | Dans la bande | Au-dessus du bord haut | `BANDE` |
|---|---|---|---|---|
| **Bruit i.i.d.** | 15,3 % | 69,1 % | 15,6 % | **67,5 %** |
| **Marche aléatoire** | 25,7 % | 48,9 % | 25,4 % | **47,6 %** |
| *Observé, étalonnage 2021* | *23,6 %* | *57,2 %* | *19,2 %* | *55,6 %* |

### `BANDE` en matrice de passage

La ligne est l'état de la clôture de la décision dans **sa** bande ; la colonne,
l'état de la clôture suivante dans la bande **prolongée**. Chaque ligne somme à
100 %.

| Depuis | Bruit i.i.d. : sous · dans · dessus | Marche aléatoire : sous · dans · dessus | *Observé 2021* |
|---|---|---|---|
| **sous le bord bas** | 16,4 · 67,2 · 16,4 | 87,7 · 12,3 · 0,0 | *85,9 · 14,0 · 0,1* |
| **dans la bande** | 16,6 · 67,5 · 15,8 | 7,5 · 84,4 · 8,1 | *6,9 · 86,8 · 6,3* |
| **au-dessus du bord haut** | 16,4 · 67,4 · 16,2 | 0,0 · 12,4 · 87,6 | *0,2 · 13,9 · 85,9* |

> **Ce que cette table dit déjà, avant la première séance.** Sous bruit i.i.d.,
> l'état de la veille ne dit rien du lendemain ; sous marche aléatoire, il dit
> presque tout. Les clôtures de 2021 ressemblent **à la marche aléatoire**, pas au
> bruit : une valeur sous le bord bas y reste le lendemain 85,9 fois sur 100. Le
> taux de 55,6 % n'est pas « 12,7 points sous la garantie » — il est **entre** les
> deux références, plus près de celle qui décrit un cours de bourse.

Le bilan publie `BANDE`, les trois états et la matrice sur 2022 et sur l'audit,
avec leur intervalle **par grappes de dates**, et leur écart à chaque référence.

---

## T4 — Le dimensionnement de la règle, par elle-même

L'expérience 4 empruntait sa tracking error à l'expérience 3 — une autre règle, à
une autre cadence. Ici, la règle est **simulée sur la fenêtre d'étalonnage** :
décisions du 2020-12-31 au 2021-12-29, exécutions du 2021-01-04 au 2021-12-30,
**aucune séance lue au-delà**. Le moteur refait ce calcul et le bilan confronte
chaque nombre à son recalcul, puis au réalisé.

| Grandeur, 2021 | **Expérience 5** | `MENSUEL` | `SANS-P20` |
|---|---|---|---|
| Tracking error contre `TR39` | **11,08 %/an** | 10,40 %/an | 12,52 %/an |
| Bêta | 0,832 | 0,515 | 1,040 |
| Part investie moyenne | 75,5 % | 47,1 % | 87,8 % |
| Séances intégralement en espèces | 10 | 40 | 10 |
| Ordres | 34 | 14 | 36 |
| Frais | 203,65 € | 80,18 € | 230,64 € |
| Durée médiane d'une position close | 55,5 séances | 66,5 séances | 61,5 séances |
| Lignes encore détenues en fin d'année | 2 | 2 | 4 |
| Signaux perdus faute de créneau | 75 | 0 | 431 |

| Écart apparié, 2021 | Écart-type de la différence | EMD sur un an |
|---|---|---|
| Expérience 5 contre `SANS-P20` | 10,00 %/an | ± 19,6 pt |
| Expérience 5 contre `MENSUEL` — **la cadence** | 9,76 %/an ; **8,68 %/an** bêta neutralisé (bêta de la différence 0,316) | ± 19,1 pt ; **± 17,0 pt** |
| Expérience 5 contre la référence à exposition appariée (T2) | 9,08 %/an | ± 17,8 pt |

> **Déclaration.** La tracking error déclarée de l'expérience 5 est **11,08 %/an**,
> soit un effet minimal détectable de **± 21,7 points d'alpha** sur un an.
>
> ⚠️ **La confrontation n'est pas aveugle** : la tracking error réalisée de 2022,
> 13,13 %/an, est connue depuis l'expérience 4. Ce qui se mesure honnêtement est
> l'écart relatif entre projeté et réalisé, publié pour qu'il s'accumule d'une
> expérience à l'autre.

**La cadence déplace l'exposition de 28,4 points** sur 2021 — 75,5 % contre 47,1 % —,
à règle égale. C'est davantage que les 22,7 points qui séparent les expériences 3
et 4 en 2022, et c'est une quantité qui se mesure en un an.

**Limites, déclarées.**

- **Une seule année de projection.** La composition point-in-time de 2020 n'est pas
  reconstruite : pas de fourchette, un point.
- **La comparaison à l'expérience 3 ne se projette pas** : elle n'a pas de
  portefeuille en 2021.
- **`TR39` porte sur 2021 la composition de 2022** — Eurofins avant son entrée,
  Atos absente. La revue l'a signalé ; ce n'est pas une piste retenue, et la
  limite est donc déclarée plutôt que corrigée.

---

## T2 — L'exposition séparée de la sélection

### La référence à exposition appariée

Chaque séance, elle détient `TR39` dans la proportion où le portefeuille était
investi **la veille** :

$$R^{\text{app}}_d = w_{d-1}\,R^{\text{TR39}}_d, \qquad w_{d-1} = \frac{\text{titres}_{d-1}}{\text{total}_{d-1}}.$$

Le bilan publie la décomposition
**exposition** = référence appariée − `TR39`, **sélection** = portefeuille −
référence appariée, et la tracking error contre la référence appariée — 9,08 %/an
projetée sur 2021.

### Les bêtas par semestre

Régression du portefeuille sur `TR39`, séparément sur le premier semestre —
séances jusqu'au 30 juin — et le second. Sur 2021 : **0,766** puis **0,883**.
Un bêta unique ne se publie plus sans eux.

### Le témoin aléatoire

**4 000 portefeuilles témoins**, générateur congruentiel **graine 3**. Chacun
reprend **toutes les positions réelles** — mêmes séances de décision, d'achat et de
sortie, même montant brut —, mais la valeur est tirée au hasard dans un
**réservoir**, parmi celles que le témoin ne détient pas déjà ce jour-là. Les
quantités sont fractionnaires, les frais ceux de la valeur tirée ; une position
réelle encore ouverte au 30 décembre est valorisée à la clôture, sans frais de
vente, comme la réelle. La valeur finale d'un témoin est la dotation plus la
somme de ses gains nets ; celle du portefeuille réel, calculée par la même
formule, retombe exactement sur sa valorisation.

| Réservoir | Ce qu'il teste | Écart-type 2021 | EMD 2021 |
|---|---|---|---|
| **`UNIVERS`** — l'univers du jour, évaluations non muettes | **toute la règle** : TOP 10 et critères | 9,81 pt | **± 19,2 pt** |
| `TOP10` — les places du TOP 10 du jour | les critères 2 et 3 seulement | 8,11 pt | ± 15,9 pt |

> **Déclaration.** **Le réservoir `UNIVERS` fait foi.** Le bilan publie, pour
> chacun, le rang du portefeuille réel parmi les 4 000 témoins, son z, et la
> moyenne des témoins.
>
> ⚠️ **Choisi en connaissant.** L'aperçu de la revue place le portefeuille à
> z = +1,96 dans le `TOP10` et +0,60 dans l'`UNIVERS` sur 2022 ; l'étalonnage
> donne l'inverse sur 2021, z = −0,29 et +0,95. Aucun réservoir n'est donc
> favorable « à coup sûr ». `UNIVERS` est retenu parce qu'il est le seul à tester
> **la règle entière** : le TOP 10 est une décision de la règle, et un témoin qui
> le reprend teste la règle sans son premier étage.

Les dates de sortie étant reprises, le témoin teste **le choix de la valeur**, pas
le calendrier des ventes. C'est déclaré, et c'est la limite de la méthode.

### La différence avec l'expérience 3, neutralisée

La différence quotidienne des rendements des expériences 5 et 3 est régressée sur
`TR39`. Le bilan publie son bêta, l'alpha de cette régression et son intervalle,
et la tracking error du résidu : un écart apparié qui garde un bêta de 0,3 compare
deux expositions, pas deux règles.

---

## Les corrections de publication

La revue a relevé dans le bilan de l'expérience 4 des erreurs de rédaction qui ne
relèvent d'aucune piste. L'expérience 5 les corrige **dans sa propre
publication**, sans rien changer à un calcul :

| Signalé | Correction |
|---|---|
| « contribution nette des frais des deux sens » pour une position encore ouverte | « nette des frais payés » — une position ouverte n'a pas payé ses frais de vente |
| l'alpha d'une position rapporte une ouverture à ouverture à un `TR39` de clôture à clôture | la convention est **déclarée** : `TR39` n'a pas de cours d'ouverture, l'alpha d'une position est donc un écart de prix d'exécution contre un écart de clôtures |
| « une seule chose change » | remplacé par le tableau de T3 |
| l'explication par le levier | corrigée par C1 |
| la composition de `TR39` en 2021 | déclarée comme limite (T4) |

---

## Ce que l'expérience 5 peut établir

| Quantité | Incertitude déclarée |
|---|---|
| Alpha du portefeuille | ± 21,7 pt — **ne tranchera rien** |
| Sélection contre la référence appariée | ± 17,8 pt |
| Rang parmi les témoins `UNIVERS` | ± 19,2 pt |
| Effet de la cadence, bêta neutralisé | ± 17,0 pt |
| **Effet de la cadence sur l'exposition** | **mesurable en un an** |
| Chaque issue, par grappes | ± 1,1 à ± 5,1 pt sur 20 séances |
| `BANDE` contre ses deux références | intervalle par grappes, et ± 0,7 pt de Monte-Carlo |
| **Survie des conclusions de l'expérience 4** | **binaire, déclarée par la règle du verdict** |

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| `bilan-2022.md` · `rapports/2022-MM.md` | le bilan et les douze journaux |
| [`journal.md`](journal.md) · [`journal.py`](journal.py) | le miroir d'exécution, puis le moteur |
| [`univers.csv`](univers.csv) · [`actualites.md`](actualites.md) · [`chartiste.md`](chartiste.md) | repris de l'expérience 4 |
| `evaluations.csv` · `top10.csv` · `ordres.csv` · `signaux.csv` · `issues.csv` | comme l'expérience 4 |
| `portefeuille.csv` · `fantome.csv` · `mensuel.csv` | les trois comptabilités quotidiennes |
| `phases.csv` | les quatre comparaisons sur les vingt phases, par grappes |
| `temoin.csv` | la valeur finale de chaque témoin, par réservoir |
| `graphiques/portefeuille-2022-MM.svg` · `graphiques/{TICKER}/canal-*.svg` | les courbes et les figures de canal |

---

## Ce que l'expérience 5 ne fait toujours pas

- **Aucun levier, aucune couverture, aucun ordre stop, aucune vente à découvert.**
- **Aucune modification de la règle** : c'est l'objet même de l'expérience.
- **Aucune année neuve** : les pistes B de la revue, qui le demandaient, ne sont
  pas retenues.
- **Aucune prédiction de cours, aucun conseil en investissement.** C'est la sortie
  d'une règle, remesurée.

## Pour aller plus loin

- [L'expérience 4](../experience_4/README.md), son [bilan](../experience_4/bilan-2022.md) et sa [revue](../experience_4/review.md) — d'où viennent les cinq pistes
- [L'expérience 3](../experience_3/README.md) — l'autre terme de la comparaison appariée
- [Semestre 3 · canal](../../../raw/concept/semestre3/canal/README.md) · [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md)
