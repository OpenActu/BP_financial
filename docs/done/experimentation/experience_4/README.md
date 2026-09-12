# Expérience 4 — 2022, une règle réduite à deux bandes

Un portefeuille de **10 000 €** au 3 janvier 2022, conduit jusqu'au 30 décembre
2022 sur **tout le CAC 40** en composition point-in-time — comme
l'[expérience 3](../experience_3/README.md) —, mais par une règle **simplifiée**,
lue **à chaque séance** :

- le **TOP 10** des valeurs dont la pente du canal de 120 séances a le taux le
  plus positif ;
- on **achète** une valeur du TOP 10 qui clôture **sous le bord bas** de son canal
  de 120 séances à ± 1 s, pendant que son canal de 20 séances **monte** ;
- on **vend** une ligne qui clôture **au-dessus du bord haut** de ce même canal.

Plus de score, plus de vetos, plus d'encadrement convexe, plus de calendrier
mensuel. Tout le reste du dispositif est **repris à l'identique** de
l'expérience 3 : univers, référence, coûts, dotation, nombre de lignes,
recevabilité des données, dimensionnement publié avant, décision mécanique.

> ⚠️ **Ordre de rédaction.** Ce README et [`univers.csv`](univers.csv) ont été
> figés avant la première séance. Le miroir [`journal.md`](journal.md) a été
> écrit d'après ce protocole, puis [`journal.py`](journal.py) d'après son
> miroir — jamais l'inverse. Aucune séance de 2022 n'a été lue pour rédiger ce
> document : les chiffres cités portent tous sur la fenêtre d'étalonnage, 2021,
> ou sur des expériences déjà publiées. Le résultat est dans le
> [bilan](bilan-2022.md), qui confronte chacun de ces chiffres à son recalcul.

---

## ⚠️ Ce que rejouer 2022 coûte ici — plus cher qu'à l'expérience 3

L'expérience 3 rejouait 2022 avec une règle **arrêtée sur 2025**. L'expérience 4
la rejoue avec une règle **formulée après**
l'[analyse des deux pertes les plus lourdes de 2022](../experience_3/pistes-pertes.md).
La simplification n'y a été calée sur aucun chiffre, mais elle a été pensée par
quelqu'un qui connaissait l'année. **Dans sa genèse, la règle est donc de
catégorie B**, et elle est déclarée comme telle.

Conséquence : **sa performance en 2022 ne vaudra rien comme preuve**, et c'est
écrit avant de la connaître. L'expérience garde trois usages, qui ne dépendent
pas de la performance :

1. **Les taux de la règle**, qui sont des propriétés de la règle et non de
   l'année. Ils sont mesurés sur l'étalonnage 2021, **publiés ci-dessous avant la
   première séance**, puis remesurés sur 2022.
2. **La comparaison appariée avec l'expérience 3.** Les deux partagent l'année,
   l'univers, la référence, les coûts, la dotation et le plafond de cinq lignes.
   **Ce qui les sépare, c'est la règle et sa cadence**, et rien d'autre. Aucune
   paire d'années différentes ne permet cela.
3. **La confrontation de chaque élément de la règle à une issue déclarée
   d'avance**, sur un échantillon de valeurs et de dates bien plus large que les
   positions du portefeuille.

Deux garde-fous :

- **les quatre paramètres de la règle — 10, 120, 20 et 1 s — sont ceux de son
  énoncé.** Aucun balayage n'en a été fait dans ce dépôt, ni sur 2022 ni
  ailleurs. Les variantes du § « Sensibilité » mesurent, elles ne choisissent
  pas ;
- **la règle ne change pas en cours d'année**, pas plus que ce protocole.

---

## Le dimensionnement, publié avant la première séance

### L'alpha : la tracking error la plus défavorable

L'expérience 3 avait déclaré 8,20 %/an, la plus favorable des mesures
antérieures, et en a réalisé **15,58**. Elle a montré qu'un dimensionnement
publié d'avance pouvait être **trop optimiste d'un facteur deux**. La leçon est
appliquée : on retient ici **la plus élevée des tracking errors mesurées**.

| Horizon | SE de l'alpha annuel | Effet minimal détectable |
|---|---|---|
| 1 an | 15,58 pt | **± 30,5 pt** |
| 4 ans | 7,79 pt | ± 15,3 pt |
| 9,3 ans | 5,11 pt | ± 10,0 pt |
| 37,3 ans | 2,55 pt | ± 5,0 pt |

> **Déclaré avant la première séance : l'alpha de l'expérience 4 ne tranchera
> rien.** Rien ne permet de supposer une tracking error plus faible qu'à
> l'expérience 3. La règle détient au plus cinq lignes, comme elle, et elle peut
> désormais les garder toute l'année.

### Les taux : dix fois plus d'évaluations, mais qui se chevauchent

Passer à une décision par séance multiplie les évaluations par vingt environ.
**L'information ne suit pas.** Deux évaluations de la même valeur à un jour
d'écart partagent 119 des 120 clôtures de leur fenêtre : elles ne sont pas deux
observations. Des intervalles calculés sur les comptes quotidiens seraient
**faussement étroits**, d'un facteur de l'ordre de √20.

> **Déclaration.** Chaque taux est publié deux fois : sur les **évaluations
> quotidiennes**, et sur un **sous-échantillon sans chevauchement**, fait d'une
> séance de décision sur vingt, compté à partir de la première séance de la
> fenêtre d'audit, le 2020-12-31. **Seul l'intervalle du sous-échantillon fait
> foi.** Celui des comptes quotidiens est une borne inférieure de l'incertitude,
> publiée pour qu'on voie l'écart.

Ces comptes sont **exacts**. Ils se déduisent de [`univers.csv`](univers.csv) et
du calendrier des séances de `TR39` :

| Quantité | Étalonnage | Narrée | Audit | IC95 d'une proportion, audit |
|---|---|---|---|---|
| Séances de décision | 258 | 257 | **515** | — |
| Évaluations quotidiennes | 9 932 | 10 023 | **19 955** | ± 0,69 pt *(borne inférieure)* |
| Dates du sous-échantillon | 13 | 13 | **26** | — |
| Évaluations du sous-échantillon | 500 | 507 | **1 007** | **± 3,1 pt** |
| Places de TOP 10 du sous-échantillon | 130 | 130 | **260** | **± 6,1 pt** |
| Alpha du portefeuille | — | 1 an | — | ± 30,5 pt |

Les intervalles sont donnés au pire cas, p = 0,5.

---

## Le protocole

### La dotation et les contraintes

| | |
|---|---|
| Dotation | **10 000 €**, en espèces, au 3 janvier 2022 |
| Lignes détenues | **5 au maximum**, simultanément |
| Levier · Couverture · Vente à découvert · Ordre stop | **aucun** |
| Fin de l'expérience | 30 décembre 2022, dernière séance de l'année |

Le solde non investi dort en espèces, sans rémunération. Le bilan publie la
**part investie moyenne**, le **bêta** et le **nombre de séances à 100 % en
espèces**. Aucun alpha ne se lit sans son exposition.

### L'univers — tout le CAC 40, à sa composition du jour

C'est l'univers de l'expérience 3, avec une différence : il est désormais lu **à
chaque séance**, et non plus en fin de mois. [`univers.csv`](univers.csv) ne
donne donc plus une ligne par (date, valeur), mais une ligne par valeur, avec ses
**dates exactes** d'entrée et de sortie de l'indice, lues dans
[`bnains.org/archives/histocac/histocac.php`](https://www.bnains.org/archives/histocac/histocac.php).
Les ISIN, les tickers et les exclusions sont repris de
l'[`univers.csv` de l'expérience 3](../experience_3/univers.csv), qui les lisait
dans `compocac.php`.

| Colonne | Sens |
|---|---|
| `ENTREE_INDICE` | première séance dans l'indice ; vide si la valeur y est déjà à l'ouverture de la fenêtre |
| `SORTIE_INDICE` | dernière séance dans l'indice ; vide si la valeur y est encore au 2022-12-30 |
| `EVALUABLE_DES` | première séance où la règle peut être calculée ; vide si c'est dès l'entrée |
| `RETENUE` · `MOTIF` | exclusion, et son motif |

**Une valeur appartient à l'univers de la séance `d`** si `d` est comprise entre
son entrée et sa sortie, bornes incluses, et si elle est évaluable à `d`. Les
mouvements de la fenêtre d'audit :

| Dernière séance du sortant | Sortie | Entrée | Première séance de l'entrant |
|---|---|---|---|
| 2021-01-15 | Peugeot | Stellantis | 2021-01-18 |
| 2021-09-17 | Atos | Eurofins Scientific | 2021-09-20 |

**L'indice ne bouge pas en 2022.** Le mouvement suivant date du 2023-06-16. Les
39 valeurs retenues forment donc l'univers de chacune des 257 séances de
l'année narrée.

**L'admission exige 120 séances de volume strictement positif**, et non plus 253.
Les 253 séances de l'expérience 3 venaient du momentum 12-1, que la règle
n'utilise plus ; la plus longue fenêtre qu'elle lit en compte 120. La série de
Stellantis est synthétique avant le 2021-01-18 — 523 séances à 3,31 €, volume
nul —, et sa 120ᵉ séance réelle tombe le **2021-07-06**. Ce seuil ne change rien
à l'année narrée.

**Deux valeurs sont exclues**, avec leur motif :

| Valeur | Motif |
|---|---|
| **Unibail-Rodamco** | le fournisseur ne sert **aucune série en euros** — seul `UNBLF`, en dollars |
| **Peugeot** | radiée après la fusion Stellantis, aucune série servie |

L'univers effectif compte **38 valeurs** du 2020-12-31 au 2021-07-05, puis
**39** jusqu'au bout.

### Les divisions postérieures à la fenêtre

Les trois séries repérées par l'expérience 3 portent toujours une division
survenue après le 30 décembre 2022, que le fournisseur répercute sur tout
l'historique :

| Valeur | Division | Cours de 2022 multipliés par |
|---|---|---|
| **Air Liquide** | attributions d'actions gratuites de 2024 et 2026, 1,1 chacune | 0,826 |
| **Atos** | regroupement du 2025-04-24, 1 pour 10 000 | 10 000 |
| **Worldline** | regroupement du 2026-06-15, 1 pour 40 | 40 |

Tout ce que la règle lit est invariant d'échelle : un taux de pente en %/séance,
une position de la clôture en unités de `s`, un signe de pente. **Le nombre de
titres achetables ne l'est pas.**

> **Déclaration.** Ces valeurs restent dans l'univers, dans le TOP 10 et dans
> tous les taux. **Tout ordre d'achat qui les viserait est refusé**, et le
> créneau revient au candidat suivant de la même séance. Le refus est un
> **contrôle de recevabilité des données**, pas une condition de la règle : il
> intervient **après** le calcul du TOP 10, qui n'est jamais recalculé sans
> elles. Le bilan publie le nombre de séances où l'une d'elles occupait une place
> du TOP 10, et le nombre de signaux d'achat refusés.

L'expérience 3 arrêtait le moteur au premier ordre de ce genre, et le cas ne
s'est jamais présenté sur ses 12 dates. Sur 257 séances, il est attendu.
L'arrêt rendrait l'expérience otage d'une donnée ; refuser l'ordre la conduit à
son terme, sans qu'une opération de 2026 façonne le portefeuille.

### La référence — `TR39`

Même référence que l'expérience 3 : **`TR39`**, indice **en rendement total**
construit par
[`python/construire_indice_total.py`](../../../../python/construire_indice_total.md)
sur les 39 valeurs de l'année narrée, équipondérées. Le bilan republie les trois
conventions côte à côte — portefeuille, `TR39`, `^FCHI` nu.

### Les trois fenêtres

| Fenêtre | Séances de décision | Ce qu'elle sert |
|---|---|---|
| **Étalonnage** | du 2020-12-31 au 2021-12-30 — 258 | les taux publiés **dans ce README**, avant la première séance |
| **Narrée et investie** | du 2021-12-31 au 2022-12-29 — 257 | le portefeuille, les douze journaux, le bilan |
| **Audit** | les deux — 515 | les taux et les issues déclarées |

Les séries commencent le **2019-01-02**. La première fenêtre de 120 séances est
donc complète bien avant la première décision.

### Le calendrier — chaque séance

- **Décision** : à la **clôture** de chaque séance `d`, sur les seules données
  datées de `d` ou avant.
- **Exécution** : à l'**ouverture** de la séance suivante.
- Première décision le 2021-12-31, exécutée le 2022-01-03. Dernière décision le
  2022-12-29, exécutée le 2022-12-30. **Aucune décision n'est prise sur la
  clôture du 2022-12-30** : elle s'exécuterait en 2023.

Un ordre décidé s'exécute à l'ouverture **quel que soit l'écart d'ouverture**,
qui est subi et publié. La règle ne revérifie pas son critère sur le prix
d'ouverture : ce serait lire une séance postérieure à la décision.

---

## La règle

### Les trois grandeurs, calculées depuis les colonnes de `import_societe.py`

Toutes se déduisent des colonnes glissantes que produit
[`python/import_societe.py`](../../../../python/import_societe.md). Aucune ne
demande une dépendance nouvelle. Pour une fenêtre de $n$ séances,
$\operatorname{Var}(T) = (n^2-1)/12$.

**1. Le taux de pente du canal de 120 séances** — la pente de la droite ajustée,
rapportée au niveau moyen de la fenêtre :

$$r_{120} = \texttt{CORR\_120}\,\sqrt{\frac{\texttt{VAR\_120}}{\operatorname{Var}(T)}}, \qquad \texttt{TAUX\_120} = \frac{r_{120}}{\texttt{E\_120}} \quad \text{en \%/séance}$$

C'est le taux, et non la pente en euros, qui se compare d'une valeur à l'autre.
Il est invariant d'échelle, donc insensible aux divisions rétroactives.

**2. La largeur à l'écart-type du canal de 120 séances** —
[module 2, § 2.2](../../../raw/concept/semestre3/canal/02-les-trois-largeurs.md#22--lécart-type) :

$$s_{120} = \sqrt{\frac{n}{n-2}\;\texttt{VAR\_120}\,\bigl(1-\texttt{CORR\_120}^2\bigr)}, \qquad \text{bande} = \texttt{VAL\_120} \pm s_{120}$$

$\texttt{VAR\_120}(1-\texttt{CORR\_120}^2)$ est la variance résiduelle minimale
de l'[étape 5](../../../raw/concept/semestre3/modele/05-coefficient-de-correlation.md).
Le facteur $n/(n-2)$ en fait l'estimateur sans biais $s^2$. La bande est lue **à
la séance courante**, au bord droit du canal glissant, là où la droite vaut
`VAL_120`.

**3. Le canal de 20 séances, à largeur d'enveloppe des résidus** —
[module 2, § 2.1](../../../raw/concept/semestre3/canal/02-les-trois-largeurs.md#21--lenveloppe-des-résidus) :

- sa **pente** $r_{20}$, et son taux $\texttt{TAUX\_20} = r_{20}/\texttt{E\_20}$,
  du signe de `CORR_20` ;
- son **enveloppe** : les demi-largeurs $a = -\min_i \hat e_i$ et
  $b = \max_i \hat e_i$ des 20 résidus de la droite ajustée, calculées depuis les
  20 dernières clôtures.

> ⚠️ **L'enveloppe est tracée et publiée, elle n'est pas lue par la règle.**
> Seul le signe de la pente entre dans le critère d'achat. La largeur de
> l'enveloppe figure sur chaque figure et dans chaque note, en unités de $s_{20}$
> et en % de `E_20`. Elle n'entre dans aucune décision, pour la raison que donne
> le module 2 : sur 20 points, sa demi-largeur fluctue de ± 0,19 s d'un tirage à
> l'autre, et c'est **un nombre qu'on ne peut ni comparer, ni prendre au pied de
> la lettre**.

Une évaluation est **calculable** quand `CORR_120`, `VAR_120`, `E_120`,
`VAL_120`, `CORR_20`, `E_20` et la clôture existent à `d`, et que
$1-\texttt{CORR\_120}^2 > 0$. Sinon elle est **muette** : elle ne produit aucun
ordre ce jour-là, ni achat ni vente, et elle est comptée.

### Le TOP 10

À chaque séance `d`, parmi les évaluations calculables de l'univers du jour :

1. ne garder que les valeurs de `TAUX_120` **strictement positif** ;
2. les trier par `TAUX_120` décroissant ;
3. retenir les **dix premières**. Le rang est la position dans ce tri.

**Le TOP 10 peut compter moins de dix valeurs.** C'est le cas quand moins de dix
pentes sont positives, et on ne complète pas avec des pentes négatives : « le
taux le plus positif » d'une pente négative n'a pas de sens. Sur l'étalonnage
2021, le cas ne s'est jamais produit, avec 22 pentes positives au minimum et 33
en médiane. Sur 2022, le bilan publie le nombre de séances concernées.

### Le critère d'achat

Une valeur est **candidate** à la séance `d` si les quatre conditions sont
réunies :

| # | Condition | Grandeur |
|---|---|---|
| 1 | elle est dans le **TOP 10** | `TAUX_120` |
| 2 | sa clôture est **sous le bord bas** du canal de 120 séances | $\texttt{Close}_d < \texttt{VAL\_120} - s_{120}$ |
| 3 | son canal de 20 séances **monte** | $\texttt{TAUX\_20} > 0$ |
| 4 | elle n'est pas déjà détenue | — |

Les candidats sont servis **dans l'ordre du TOP 10**, tant qu'il reste un
créneau. Un candidat refusé pour une division postérieure cède son créneau au
suivant.

- **Répartition** : les espèces disponibles, ventes du jour comprises, divisées
  par le **nombre de créneaux libres**. C'est la convention des expériences 2 et
  3.
- **Titres entiers**, reliquat aux espèces. Une quantité nulle annule l'ordre.
- **Aucun rebalancement**, aucun renforcement d'une ligne détenue.
- **Le rachat d'une valeur vendue est libre** dès qu'elle redevient candidate.

### Le critère de vente — un seul motif

Une ligne détenue est **vendue** à la séance `d` si

$$\texttt{Close}_d > \texttt{VAL\_120} + s_{120}.$$

**C'est le seul motif.** Une ligne n'est vendue ni parce qu'elle sort du TOP 10,
ni parce que sa pente devient négative, ni parce qu'elle quitte l'indice, ni
parce que son évaluation est muette.

> ⚠️ **Conséquence déclarée avant la première séance : une ligne qui décroche
> peut ne jamais être vendue.** Si sa pente se retourne, son canal descend, et
> la clôture a alors peu de chances de repasser au-dessus du bord haut. La ligne
> occupe un créneau jusqu'au 30 décembre. C'est un choix de la règle, et il n'est
> pas corrigé. **Il est mesuré.** Le bilan publie :
>
> - la **durée** de chaque détention, et sa distribution ;
> - les **lignes jamais revendues** au 2022-12-30, avec leur moins-value latente ;
> - le **repli maximal** de chaque ligne entre l'achat et la sortie, en clôture
>   et sur le `Low` ;
> - les **signaux perdus faute de créneau** : séances où les cinq créneaux sont
>   pris alors qu'un candidat existe, et le nombre de ces candidats ;
> - les **séances de silence** : séances de détention où l'évaluation de la
>   ligne est muette.

Deux propositions de l'[analyse des pertes](../experience_3/pistes-pertes.md)
touchaient la sortie. Aucune n'est reprise :

| Proposition | Pourquoi elle n'est pas reprise |
|---|---|
| `STOP-10` — plafond de perte à 10 % | réfutée par sa propre mesure : sur 884 détentions d'un mois, effet moyen de −1,68 pt ± 1,11 par déclenchement |
| `MUETTE-SORTIE` — vendre une ligne dont l'évaluation échoue | ajouterait un second motif de vente là où la règle n'en déclare qu'un. **Sa mesure est reprise** : les séances de silence ci-dessus |

### L'ordre des opérations à chaque séance

1. Lire l'univers du jour, puis évaluer chaque valeur à la **clôture** de `d`.
2. Classer : le TOP 10.
3. Décider les **ventes**, sur les lignes détenues.
4. Décider les **achats**, sur les créneaux libérés par ces ventes compris.
5. Exécuter ventes puis achats à l'**ouverture** de la séance suivante.
6. Valoriser le portefeuille à chaque clôture.

### Ce que la règle ne contient plus

| Élément de l'expérience 3 | Expérience 4 |
|---|---|
| score entier à cinq composantes `s1`…`s5` | **supprimé** — un TOP 10 et deux conditions |
| quatre vetos | **supprimés** |
| encadrement par enveloppe convexe, `generer_graph_decision.py`, τ, épisodes de contact | **supprimés** — la règle lit un canal de régression |
| momentum 12-1, alpha annualisé et son IC | **supprimés** |
| entrée au rang ≤ 5, sortie au rang > 7 ou au score ≤ −3 | entrée par le TOP 10 **et** la bande, sortie par la bande seule |
| une décision par mois | **une décision par séance** |

### Les coûts

| | Achat | Vente |
|---|---|---|
| Courtage | 0,100 % | 0,100 % |
| Demi-spread | 0,015 % | 0,015 % |
| Taxe sur les transactions financières | 0,300 % | — |

Soit **0,530 % l'aller-retour**. Sont exemptées de TTF **Airbus** et
**Stellantis** (Pays-Bas), **ArcelorMittal** (Luxembourg) et
**STMicroelectronics** (Pays-Bas).

> Une cadence quotidienne ne multiplie pas les ordres par vingt : un ordre
> n'est passé que lorsqu'une condition **bascule**. Mais rien ne borne leur
> nombre d'avance. Le bilan publie les frais cumulés et leur part de la dotation,
> à côté de ceux de l'expérience 3 (75,24 €).

---

## Les taux d'étalonnage — publiés avant la première séance

Mesurés sur les **258 séances de décision de 2021**, sur les séries telles
qu'elles sont servies, sans aucune séance postérieure au 2021-12-30. Le moteur
les recalculera, et le bilan les republiera à côté de ceux de 2022. **Un écart
entre les deux calculs est une erreur, du moteur ou de ce document.**

| Mesure | 2021 |
|---|---|
| Évaluations | 9 932, **aucune muette** |
| Pentes à `TAUX_120` > 0 par séance | 22 au minimum, 33 en médiane, 36 au maximum |
| Entrants dans le TOP 10 par séance | **0,17** en moyenne ; au moins un entrant sur 43 séances sur 257 |
| Clôtures **sous** $\texttt{VAL\_120} - s_{120}$, univers | 2 346 — **23,6 %** |
| Clôtures **au-dessus** de $\texttt{VAL\_120} + s_{120}$, univers | 1 904 — **19,2 %** |
| Clôtures **dans** la bande, univers | 5 682 — **57,2 %** |
| Places du TOP 10 sous le bord bas | 746 / 2 580 — **28,9 %** |
| Places du TOP 10 au-dessus du bord haut | 293 / 2 580 — 11,4 % |
| **Évaluations candidates** (TOP 10, sous le bord bas, `TAUX_20` > 0) | **210** |
| … dont la pente courte est nulle ou négative | 536 |
| Séances comptant au moins un candidat | 123 / 258 |
| Clôture de la séance suivante **dans la bande prolongée d'un pas** | 5 499 / 9 893 — **55,6 %** |
| Écart-type du rendement excédentaire sur 20 séances contre `TR39` | 6,06 pt au quotidien ; **6,44 pt** sur le sous-échantillon |

**Trois constats de catégorie A**, acquis sans avoir lu 2022 :

> **1. « Sous 1 s » n'est pas un événement à 15,9 %.** Sous l'hypothèse
> gaussienne i.i.d. du [module 2](../../../raw/concept/semestre3/canal/02-les-trois-largeurs.md#22--lécart-type),
> une clôture sort sous le bord bas une fois sur six ; elle le fait ici **une
> fois sur quatre** dans l'univers, et **plus d'une fois sur quatre** dans le
> TOP 10. Deux raisons, toutes deux dans le cours : la clôture courante est au
> **levier maximal** de sa fenêtre
> ([module 3](../../../raw/concept/semestre3/canal/03-epaisseur-variable-et-levier.md)),
> et les résidus d'un cours sont **autocorrélés**
> ([module 4, § 4.3](../../../raw/concept/semestre3/canal/04-sorties-de-canal.md#43--trois-raisons-pour-lesquelles-ce-comptage-reste-optimiste)).
> Le critère 2 est donc bien moins sélectif que son énoncé ne le laisse croire.
>
> **2. La bande ± 1 s ne contient pas 68,3 % des clôtures du lendemain, mais
> 55,6 %.** C'est la question qui décide selon le module 2 — *« le prochain
> point sera-t-il dedans ? »* —, et la réponse est inférieure de 12,7 points à
> la garantie nominale.
>
> **3. Le critère 3 écarte près des trois quarts des cas.** Sur les 746 places du
> TOP 10 sous le bord bas, 536 ont une pente courte nulle ou négative : c'est le
> cas ordinaire d'une valeur qui vient de baisser. Le fantôme `SANS-P20` mesure
> ce que cette condition change.

---

## Chaque élément de la règle, contre l'issue déclarée d'avance

C'est le principe de la piste C3 de l'expérience 3 : un critère n'est pas un
couperet non discuté, c'est un **énoncé réfutable**. Chacun est confronté à
**une seule issue, la même pour tous** : le **rendement excédentaire sur 20
séances contre `TR39`**, de la clôture de `d` à celle de `d + 20`. Le bilan
publie, pour chaque ligne, les deux moyennes, leur différence et l'IC95 de cette
différence, sur le sous-échantillon d'audit.

Les **effets minimaux détectables** ci-dessous sont projetés à partir des
proportions et de l'écart-type de l'étalonnage. Ils sont publiés **avant**, pour
qu'on sache ce que chaque ligne peut établir.

| Élément | Groupe testé | Groupe témoin | Effectifs projetés, audit | EMD sur 20 séances |
|---|---|---|---|---|
| **TOP 10** | les places du TOP 10 | le reste de l'univers | 260 contre 747 | **± 0,9 pt** |
| **Critère 2** — sous le bord bas | TOP 10 sous le bord bas | reste du TOP 10 | 84 contre 176 | ± 1,7 pt |
| **Critère 3** — pente courte positive | candidats | TOP 10 sous le bord bas, pente ≤ 0 | **22 contre 62** | **± 3,1 pt** |
| **Vente** — au-dessus du bord haut | univers au-dessus du bord haut | reste de l'univers | 193 contre 814 | ± 1,0 pt |

S'y ajoute une issue sans groupe, celle que le module 2 désigne comme décisive :

| Énoncé | Mesure | Référence | IC95, audit |
|---|---|---|---|
| **`BANDE`** — la bande prolongée d'un pas contient la clôture suivante | proportion | 68,3 % nominal, 55,6 % à l'étalonnage | ± 3,1 pt |

> **Déclaré avant la première séance : le critère 3 ne sera pas tranché.** Avec
> une vingtaine de candidats indépendants sur deux ans, son effet minimal
> détectable vaut ± 3,1 points **sur 20 séances**, soit l'ordre de ± 40 points
> annualisés. La ligne est publiée quand même, avec son intervalle. Une ligne
> vide aurait laissé croire qu'on n'avait pas cherché.

Une issue dont l'horizon dépasse le 2022-12-30 est **non tranchée**, et comptée
à part. Cela concerne la dernière date du sous-échantillon d'audit.

---

## Le fantôme, la comparaison appariée, la sensibilité

### Le fantôme `SANS-P20`

Un portefeuille parallèle applique la même règle **sans le critère 3**. Il a les
mêmes coûts, la même dotation, les mêmes créneaux, et n'engage pas un euro. Sur
l'étalonnage, il aurait eu **746 évaluations candidates au lieu de 210**, trois
fois et demie plus. Le bilan publie l'écart entre les deux portefeuilles, et
l'écart-type annualisé de leur **différence**, qui est plus faible que celui de
chacun contre `TR39`.

### La comparaison appariée avec l'expérience 3

Le [`portefeuille.csv` de l'expérience 3](../experience_3/portefeuille.csv)
valorise chaque séance de 2022 dans le même univers, contre la même référence et
avec les mêmes coûts. Le bilan publie séance par séance l'écart entre les deux
portefeuilles, l'écart-type annualisé de cette différence, et les deux
expositions : part investie et bêta. **C'est la comparaison la mieux posée de la
série** : une seule chose change, la règle.

### La sensibilité aux paramètres — mesurée, pas arbitrée

Comme les variantes C1 de l'expérience 3, quatre variantes déclarées ici
**ne décident rien**. Aucun euro, aucun ordre n'en dépend. Elles rendent le taux
de candidats, le taux de signaux de vente et la rotation du TOP 10 :

| Variante | Ce qui change |
|---|---|
| `VAR-TOP5` | TOP **5** au lieu de 10 |
| `VAR-TOP20` | TOP **20** |
| `VAR-K05` | bande à **± 0,5 s** |
| `VAR-K15` | bande à **± 1,5 s** |

Les deux fenêtres, 20 et 120, ne varient pas : ce sont les colonnes que produit
`import_societe.py`.

---

## Pourquoi le registre des thèses n'est pas reconduit

Les thèses `CANAL` et `REFLEXIVE` de l'expérience 3 dépendent de la valeur, de la
date et de l'encadrement convexe, pas de la règle d'achat. Sur la même année,
les mêmes valeurs et les mêmes fins de mois, **elles seraient identiques, thèse
pour thèse, au [registre déjà publié](../experience_3/theses.csv)**. Les
réécrire ne mesurerait rien de nouveau. Le registre de cette expérience, ce sont
les **issues déclarées** du § précédent : elles portent sur ce que la règle
suppose, et l'énoncé `BANDE` est la thèse que la règle engage à chaque séance.

`canaux.csv` n'est pas repris pour la même raison.

---

## Ce que contient chaque markdown mensuel

Douze fichiers, `rapports/2022-01.md` à `rapports/2022-12.md`. La décision est
quotidienne, le journal reste mensuel.

1. Les **actualités** du mois précédent.
2. L'**exposition héritée** au premier jour du mois.
3. **Le portefeuille depuis le 3 janvier 2022** : les données générales, le
   graphique, puis **le tableau de toutes les positions prises depuis le début de
   l'expérience**, closes comme ouvertes — société, prix et date d'achat, prix et
   date de vente. Une position ouverte laisse les deux dernières colonnes vides.
4. **L'étude chartiste** : une note de cinq lignes au plus **par société de
   l'univers**, soit 39 par mois, **chacune accompagnée de sa figure** lue à la
   dernière séance du mois. Chaque ordre du mois reçoit en outre la figure lue à
   **sa** séance de décision.
5. Le **TOP 10** à la dernière séance du mois, avec taux, écart de la clôture en
   unités de $s_{120}$ et signe de la pente courte, suivi des **entrées et
   sorties du TOP 10** au fil du mois, datées.
6. Les **ordres exécutés**, chacun avec son motif chiffré : séances de décision
   et d'exécution, clôture, `VAL_120`, $s_{120}$, écart en unités de $s$, rang,
   `TAUX_120`, `TAUX_20`, écart d'ouverture subi.
7. Les **signaux non exécutés** du mois : faute de créneau, ou refusés pour
   division postérieure.
8. La **lecture du mois**, entièrement calculée.

### La figure de canal

Elle est écrite à la main en SVG par le moteur, sans `matplotlib`, dans
`graphiques/{TICKER}/canal-{TICKER}-{DATE}.svg`. Elle porte :

- les **120 dernières clôtures** jusqu'à `d` incluse ;
- la droite ajustée sur 120 séances et sa bande **± 1 s**, avec la clôture de `d`
  et son écart en unités de $s_{120}$ ;
- la droite ajustée sur 20 séances et son **enveloppe des résidus**, avec les
  deux points qui la fixent ;
- le rang au TOP 10, `TAUX_120`, `TAUX_20`, et le verdict du jour : candidat,
  vente, ou rien.

> Le graphique et la figure d'une séance `d` s'arrêtent à `d`. **Aucune
> décision, aucune figure et aucune échelle ne s'appuie sur une séance
> postérieure à sa date de décision.**

---

## Les fichiers

| Fichier | Contenu | État |
|---|---|---|
| `README.md` | ce protocole | **figé** |
| [`univers.csv`](univers.csv) | les 42 valeurs passées par l'indice sur la fenêtre, dates exactes, exclusions motivées | **figé** |
| [`journal.md`](journal.md) · [`journal.py`](journal.py) | le miroir d'exécution, puis le moteur | écrits, dans cet ordre |
| [`actualites.md`](actualites.md) · [`chartiste.md`](chartiste.md) | le texte rédigé à la main — actualités reprises de l'expérience 3, notes de l'agent `chartiste` | écrits |
| `evaluations.csv` | les évaluations quotidiennes de l'audit, variantes comprises | produit |
| `top10.csv` · `ordres.csv` · `signaux.csv` · `issues.csv` | TOP 10 quotidien, ordres, sort de chaque candidat, issues déclarées | produits |
| `portefeuille.csv` · `fantome.csv` | les valorisations quotidiennes | produits |
| `bilan-2022.md` · `rapports/2022-MM.md` | le bilan et les douze journaux | produits |
| `graphiques/portefeuille-2022-MM.svg` | les douze courbes | produites |
| `graphiques/{TICKER}/canal-{TICKER}-{DATE}.svg` | les figures de canal, une société par répertoire | produites |

**Aucun chiffre des journaux n'est saisi à la main.**

---

## Ce que l'expérience 4 ne fait toujours pas

- **Aucun levier, aucune couverture, aucun ordre stop, aucune vente à découvert.**
- **Aucun fondamental**, nulle part.
- **Aucune prédiction de cours.** Les issues portent sur des rendements relatifs
  et sur la couverture d'une bande.
- **Aucun conseil en investissement.** C'est la sortie d'une règle, consignée.

## Pour aller plus loin

- [L'expérience 3](../experience_3/README.md) et son [bilan](../experience_3/bilan-2022.md) — même année, même univers, l'autre règle
- [L'analyse des deux pertes les plus lourdes de 2022](../experience_3/pistes-pertes.md) — d'où vient la simplification, et pourquoi elle est de catégorie B
- [Semestre 3 · canal](../../../raw/concept/semestre3/canal/README.md) — les trois largeurs, les sorties de canal, le canal glissant
- [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md) · [trading](../../../raw/concept/semestre4/trading/README.md)
