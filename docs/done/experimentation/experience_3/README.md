# Expérience 3 — 2022 rejouée sur tout le CAC 40

> *« Il ne s'agit pas de savoir si vous avez raison ou tort, mais de combien vous
> gagnez quand vous avez raison et de combien vous perdez quand vous avez tort. »*
> — George Soros, **L'Alchimie de la finance**, 1987

Un portefeuille de **10 000 €** au 3 janvier 2022, conduit jusqu'au 30 décembre
2022 par une règle écrite à l'avance, sur **tout le CAC 40** — la composition
réelle de l'indice à chaque date de décision, et non un sous-ensemble constitué
aujourd'hui.

C'est la troisième de la série, et elle rejoue **la même année que
l'[expérience 1](../experience_1/README.md)**. Ce n'est pas une répétition :
l'expérience 1 tournait sur douze valeurs choisies à la main et se comparait à un
`TR12` bâti sur ces mêmes douze. En gardant l'année et en changeant l'univers, la
référence et cinq points de protocole, on isole ce que ces changements font.

Les cinq points corrigés sont les cinq pistes retenues par le vote de la
[revue de l'expérience 2](../experience_2/review.md).

---

## ⚠️ Ce que rejouer 2022 coûte, et pourquoi on le fait quand même

L'année 2022 a déjà été jouée, publiée et relue deux fois dans ce dépôt. Quiconque
la rejoue en la connaissant s'expose au premier des
[cinq pièges de l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md),
et les trois agents ont mis en garde contre exactement cela lors de la revue de
l'expérience 1.

**La contrepartie est un plan d'expérience que ni l'une ni l'autre des deux
premières ne permettait.** L'expérience 1 et l'expérience 3 partagent l'année,
les coûts, la cadence et la famille de règle ; elles diffèrent par l'univers (12
valeurs choisies contre tout l'indice), par la référence (`TR12` contre `TR39`)
et par les cinq corrections. **Ce qui les sépare est donc attribuable**, ce qui
n'est vrai d'aucune paire d'années différentes.

Deux garde-fous, déclarés ici :

- **rien n'a été ajusté sur 2022.** Les seuils, les vetos, les bornes et les
  paramètres d'encadrement sont repris tels quels de l'expérience 2, qui portait
  sur 2025 ;
- **la performance reste déclarée non concluante avant d'être connue**, pour la
  raison chiffrée au § suivant. Aucune section de cette expérience ne s'appuie
  dessus.

---

## Le dimensionnement, publié avant la première séance

C'est la piste **T1** de la première revue, appliquée pour la deuxième fois, et
elle commande le reste. La tracking error mesurée sur l'expérience 1 vaut
**8,20 %/an**, celle de l'expérience 2 **9,52 %/an**. En retenant la plus
favorable :

| Horizon | SE de l'alpha annuel | Effet minimal détectable |
|---|---|---|
| 1 an | 8,20 pt | **± 16,1 pt** |
| 3 ans | 4,73 pt | ± 9,3 pt |
| 65 ans | 1,02 pt | ± 2,0 pt |
| **189 ans** | 0,60 pt | **± 1,17 pt** ← les frais d'une année |

> **Déclaré avant la première séance : la performance de l'expérience 3 ne
> tranchera rien.** Elle sera publiée telle qu'elle sort. Ce que l'expérience
> mesure utilement est ailleurs — dans les taux, dont l'univers élargi triple
> l'échantillon.

L'élargissement de douze à trente-neuf valeurs change précisément cela :

| Quantité publiée | Expérience 2 | Expérience 3 | Incertitude 95 % |
|---|---|---|---|
| Évaluations de la règle | 432 | **923** | ± 3,2 pt |
| Thèses `CANAL` | 432 | **923** | ± 3,2 pt |
| Thèses `REFLEXIVE` | 432 | **240** | ± 6,3 pt |
| Couples de stabilité à d−1 | 144 | **467** | ± 4,5 pt |
| Alpha du portefeuille | 1 an | 1 an | ± 16,1 pt |

Ces comptes sont **exacts, pas arrondis** : ils se lisent dans
[`univers.csv`](univers.csv), qui fige la composition de l'indice aux 24 dates.
Les thèses `REFLEXIVE` sont les seules à reculer, et c'est voulu — la piste S1
les réserve aux onze valeurs à canal de transmission déclaré.

**Sur les taux, l'incertitude tombe à ± 3,2 points ; sur l'alpha, elle reste à
± 16,1.** Le rapport passe de trois et demi contre un dans l'expérience 2 à
**cinq contre un** ici.

---

## Le protocole, déclaré avant la première séance

### La dotation et les contraintes

| | |
|---|---|
| Dotation | **10 000 €**, en espèces, au 3 janvier 2022 |
| Lignes détenues | **5 au maximum**, simultanément |
| Levier · Couverture · Vente à découvert | **aucun** |
| Fin de l'expérience | 30 décembre 2022, dernière séance de l'année |

Le solde non investi dort en espèces, sans rémunération. Conformément à la piste
T4 de la revue de l'expérience 2 — non retenue par le vote, mais dont le constat
est gratuit —, le bilan publie la **part investie moyenne** et le **nombre de
séances à 100 % en espèces**, pour qu'aucun alpha ne se lise sans son exposition.

### L'univers — tout le CAC 40, à sa composition du jour

L'univers n'est plus une liste. C'est **la composition réelle de l'indice à
chaque date de décision**, reconstruite depuis
[`bnains.org`](https://www.bnains.org/archives/histocac/compocac.php) et figée
dans [`univers.csv`](univers.csv), une ligne par (date, valeur), avec son ISIN,
son ticker et, le cas échéant, le motif de son exclusion.

C'est la correction du **biais du survivant**, que les deux premières expériences
déclaraient sans le corriger. Sur la fenêtre, l'indice bouge deux fois :

| Date de décision | Sortie | Entrée |
|---|---|---|
| 2021-01-29 | Peugeot | Stellantis |
| 2021-09-30 | Atos | Eurofins Scientific |

**Trois valeurs sont exclues, chacune avec son motif**, et le tableau les nomme
plutôt que de les taire :

| Valeur | Dates concernées | Motif |
|---|---|---|
| **Unibail-Rodamco** | toutes | le fournisseur ne sert **aucune série en euros** — seul `UNBLF`, en dollars, existe, et mêler deux devises fabriquerait du rendement de change |
| **Peugeot** | la seule décision du 2020-12-31 | radiée après la fusion Stellantis, aucune série servie |
| **Stellantis** | les décisions de 2021 | **sa série antérieure au 2021-01-18 est synthétique** — 523 séances à 3,31 € exactement, volume nul. Elle entre dans l'univers dès qu'elle a les 253 séances réelles que le momentum 12-1 exige, soit à partir de la décision du 2022-01-31 |

> ⚠️ **Une série à volume nul n'est pas un cours.** Sur une telle série, la
> variance est nulle, l'encadrement a une épaisseur nulle et le momentum vaut
> exactement 0 % : la règle rendrait des nombres, tous faux. Le protocole exige
> donc **253 séances de volume strictement positif** avant d'admettre une valeur,
> ce qui est le seuil que le critère 5 réclame déjà.

**L'univers effectif vaut 38 valeurs aux treize décisions du 2020-12-31 au
2021-12-31, et 39 aux onze décisions de 2022** — soit **923 évaluations** sur la
fenêtre d'audit et **467** sur l'année narrée, dont la première décision, celle
du 2021-12-31, porte encore sur 38 valeurs.

### Les divisions postérieures à la fenêtre

Trois séries portent une division d'actions survenue **après** le 30 décembre
2022, que le fournisseur répercute rétroactivement sur tout l'historique :

| Valeur | Division | Cours de 2022 multipliés par |
|---|---|---|
| **Air Liquide** | attributions d'actions gratuites de 2024 et 2026, 1,1 chacune | 0,826 |
| **Atos** | regroupement du 2025-04-24, 1 pour 10 000 | 10 000 |
| **Worldline** | regroupement du 2026-06-15, 1 pour 40 | 40 |

> ⚠️ **Une division rétroactive est un regard en avant sur le nombre de titres.**
> Tout ce que la règle calcule est invariant d'échelle — position dans le canal,
> momentum, alpha, tendances, τ, largeur relative. Le **nombre de titres
> achetables** ne l'est pas : un créneau de 2 000 € sur une valeur affichée à
> 506 € achète 3 titres et laisse 481 € oisifs, là où le cours réel de l'époque
> en achèterait dix fois plus et n'en laisserait que trente. Le portefeuille
> serait alors façonné par une opération de 2026.

Le protocole ne les exclut pas de l'univers : elles n'entrent que dans des
quantités invariantes d'échelle — taux de veto, stabilité, registre des thèses.
Il **interdit en revanche qu'un ordre porte sur l'une d'elles** : le moteur
vérifie après simulation et **s'arrête** le cas échéant, plutôt que de publier un
portefeuille que le seul nombre de titres aurait déformé.

Ce n'est pas un cinquième veto — un veto changerait la règle. C'est un contrôle
de recevabilité des données, et sa sortie est publiée au bilan. **Sur cette
fenêtre, aucune des trois n'est jamais achetée.**

### La référence — `TR39`, et pourquoi ce nom

La performance est mesurée contre **`TR39`**, indice **en rendement total**
construit par
[`python/construire_indice_total.py`](../../../../python/construire_indice_total.md)
sur les **39 valeurs de l'univers de l'année narrée**, équipondérées.

Le nom dit le nombre, comme le veut ce script : ce n'est pas un `TR40`, puisque
la quarantième valeur de l'indice n'a pas de série en euros. Écrire `TR40` sur un
panier de trente-neuf serait précisément le genre de convention devinée que le
dépôt s'interdit.

```
TR39 (rendement total)      CAGR   13,09 %/an   sur 2019-2022
^FCHI (nu)                  CAGR    8,23 %/an
ecart                               4,85 points/an
```

Cet écart mélange dividendes, composition et pondération ; le lire comme un
rendement de dividende serait une erreur. Le bilan republie les trois conventions
côte à côte.

### Les trois fenêtres

| Fenêtre | Dates de décision | Ce qu'elle sert |
|---|---|---|
| **Étalonnage** | les 12 fins de mois de 2020-12 à 2021-11 | les poids effectifs et les taux de veto, publiés **avant** la première séance de 2022 |
| **Narrée et investie** | les 12 fins de mois de 2021-12 à 2022-11 | le portefeuille, les douze journaux, le bilan |
| **Audit** | les 24 fins de mois de 2020-12 à 2022-11 | les taux : vetos, survie du canal, dépouillement des thèses |

Les séries commencent le **2019-01-02**, trois ans avant la première décision.

### Le calendrier

- **Date de décision** : la dernière séance du mois précédent.
- **Date d'exécution** : la première séance du mois, au cours d'**ouverture**.

---

## Les paramètres de l'encadrement — piste C1

C'est la **première piste retenue** par le vote, avec 13 points et les trois
soutiens. Les deux expériences précédentes appelaient
[`generer_graph_decision.py`](../../../../python/generer_graph_decision.md) sans
préciser ses paramètres géométriques, laissant agir des défauts que ni le
protocole, ni le miroir, ni le bilan ne citaient. Or l'agent `chartiste` a mesuré
que passer la fenêtre de 120 à 60 séances **divise par plus de deux** l'ensemble
des valeurs achetables, et l'agent `trading` que le taux d'achetabilité varie
d'un **facteur 2,4** sur une grille que rien n'excluait.

> **Déclaration.** Les trois paramètres de l'encadrement sont
> `--fenetre 120`, `--tolerance 0,25 σ_Close` et `ECART_EPISODE = 3`. Ce sont
> des **paramètres du protocole**, pas des défauts d'un script, et ils ne
> changent pas en cours d'année.

Le moteur relance en outre la collecte sous **quatre variantes déclarées
d'avance** — fenêtre 60 et 180, tolérance 0,15 σ et 0,40 σ — et le bilan publie,
pour chacune, le taux de déclenchement de chaque veto et le taux de bascule de
`s3`. Ces variantes ne décident rien : elles mesurent de combien l'incertitude de
convention dépasse l'incertitude d'échantillonnage.

---

## La règle dérivée, et ses quatre vetos

Le score n'est **pas** la règle du
[module 3](../../../raw/concept/semestre4/trading/03-la-regle-ecrite-a-l-avance.md) :
c'est une **règle dérivée**, qui en emprunte les cinq critères et les quatre
vetos, et qui rend un score entier et un classement au lieu de trois verdicts.

| | Critère | Valeurs possibles |
|---|---|---|
| `s1` | tendance longue `TEND_120` | `+2` / `0` / `−2` |
| `s2` | tendance courte `TEND_20` | `+1` / `0` / `−1` |
| `s3` | position dans l'encadrement | `+1` si < 35 %, `0` de 35 à 65 %, `−1` si > 65 % |
| `s4` | momentum 12-1 | `+2` si > +10 %, `+1` si 0 à +10 %, `−1` si −10 à 0 %, `−2` si < −10 % |
| `s5` | alpha annualisé, IC95 | `+1` si entièrement positif, `−1` si entièrement négatif, `0` sinon |

`s3` garde le sens **aligné** sur les seuils du module 3, arrêté par l'expérience
2 : on achète bas dans le canal. Le sens de l'expérience 1 continue de tourner en
**portefeuille fantôme**, sans engager un euro.

### Les quatre vetos, et l'issue contre laquelle chacun sera jugé — piste C3

Troisième piste retenue, 9 points et les trois soutiens. Les deux expériences
précédentes mesuraient le **taux de déclenchement** de chaque veto sans jamais
demander s'il **sépare** quoi que ce soit. L'agent `chartiste` a mesuré que le
veto 1, qui écarte pourtant près de la moitié des évaluations, ne sépare que
**+2,3 pt ± 10,0** sur la tenue de la figure qu'il prétend certifier.

> **Déclaration, écrite avant la première séance.** Chaque veto est confronté au
> bilan à l'issue observable nommée ci-dessous, et le bilan publie le taux sous
> veto, le taux hors veto, leur différence et son IC95.

| # | Veto | Déclenché quand | **Issue contre laquelle il est jugé** |
|---|---|---|---|
| 1 | encadrement illisible | moins de 3 épisodes de contact d'un côté | la **tenue de la thèse `CANAL`** : un encadrement dit lisible doit tenir plus souvent qu'un encadrement dit illisible |
| 2 | canal se refermant | $\tau < 20$ séances | la **tenue de la thèse `CANAL`** également : un canal qui va se refermer doit tenir moins souvent |
| 3 | tendances contradictoires | critères 1 et 2 de signes opposés | la **stabilité de `s3` à d−1** : une configuration contradictoire doit être plus instable qu'une configuration franche |
| 4 | historique trop court | moins de 120 séances | aucune — le veto est arithmétique, il ne prétend rien séparer, et le bilan le dit |

**Le veto reste bloquant quoi qu'il arrive.** Le modifier après l'avoir vu plat
serait le rétro-ajustement même. Ce qui change est qu'il devient, à partir de
cette expérience, un **énoncé réfutable** au lieu d'un couperet non discuté.

Un veto interdit l'**entrée** ; il ne force pas la sortie. Et une évaluation que
la règle n'a pas su produire — code de sortie 2, contrôle de non-traversée en
échec — est traitée comme un veto : une figure qu'on ne sait pas calculer n'est
pas une figure qu'on peut acheter.

### Les règles d'entrée et de sortie

- **Entrée** : rang **≤ 5**, score **strictement positif**, **aucun veto**, pas
  déjà détenue, et une place libre.
- **Sortie** : rang **au-delà de 7**, ou score **≤ −3**. Les vetos n'y entrent pas.
- **Répartition** : les espèces disponibles divisées par le **nombre de créneaux
  libres**, convention arrêtée par l'expérience 2.
- **Titres entiers**, aucun rebalancement.

> ⚠️ **Le rang d'entrée n'a pas la même sélectivité qu'en 2022.** « Rang ≤ 5 sur
> 12 » retenait les 42 % du haut ; « rang ≤ 5 sur 39 » retient les 13 %. Le seuil
> est **volontairement inchangé**, pour que la comparaison avec l'expérience 1
> porte sur l'univers et non sur deux réglages à la fois — mais la sélectivité
> change, et c'est déclaré ici plutôt que découvert au bilan.

### Les coûts

| | Achat | Vente |
|---|---|---|
| Courtage | 0,100 % | 0,100 % |
| Demi-spread | 0,015 % | 0,015 % |
| Taxe sur les transactions financières | 0,300 % | — |

Soit **0,530 % l'aller-retour**. La TTF française ne frappe que les sociétés dont
le siège est en France : en sont exemptées **Airbus** et **Stellantis**
(Pays-Bas), **ArcelorMittal** (Luxembourg) et **STMicroelectronics** (Pays-Bas).

---

## Le registre des thèses réfutables

Deux thèses par valeur et par date de décision, engendrées mécaniquement et
dépouillées à la date suivante. La revue de l'expérience 2 a montré que le
registre, tel qu'il était, **faisait 2,1 points de moins que des étiquettes
tirées au hasard**. Deux des cinq pistes retenues le corrigent.

### Le canal de transmission, déclaré avant toute thèse — piste S1

Quatrième piste retenue, 4 points. L'expérience 2 a écrit 432 thèses estampillées
« au sens de Soros » sans avoir déclaré par quel mécanisme le cours agirait sur
les affaires. Or, sans canal de transmission, il n'y a pas de réflexivité — il y
a une corrélation.

> **Déclaration.** [`canaux.csv`](canaux.csv) donne, pour chacune des 40 valeurs
> passées par l'univers sur la fenêtre d'audit — les 39 de l'année narrée, plus
> Atos, retirée de l'indice au 2021-09-30 —, et **avant la première séance**,
> son canal de transmission ou la mention `aucun`, avec la grandeur qui
> l'instrumente. **Onze en portent un, vingt-neuf n'en portent aucun.**
>
> **Une valeur sans canal ne reçoit pas de thèse `REFLEXIVE`.** Elle reçoit le
> verdict `HORS CHAMP REFLEXIF`, qui dit *« la théorie ne s'applique pas »* — un
> énoncé différent d'`AUCUNE SEQUENCE`, qui dit *« elle s'applique et il ne se
> passe rien »*. L'expérience 2 confondait les deux dans une seule case pesant
> 340 thèses sur 432.

La perte de puissance est annoncée d'avance et assumée : elle réduit le nombre de
thèses réflexives à celles dont l'énoncé a un sens.

### La clause, normalisée — piste S3

Cinquième piste retenue, 2 points. L'expérience 2 posait une bande fixe de ± 5
points, facile pour une valeur calme et dure pour une valeur agitée : le taux de
confirmation y était corrélé **−0,84** à l'écart-type propre de la valeur. Et les
bornes d'`AUTO-RENFORCEMENT` et de `RETOURNEMENT` tombaient sur le **mode** de la
distribution, si bien que neuf verdicts sur soixante se jouaient à moins d'un
demi-point.

> **Déclaration.** La demi-largeur d'`AUCUNE SEQUENCE` devient $\hat\sigma_d$,
> écart-type des **12 écarts mensuels précédents de la valeur** — tous connus à
> la date $d$, donc sans regard en avant. Les bornes d'`AUTO-RENFORCEMENT` et de
> `RETOURNEMENT` sont portées à $\pm 0{,}5\,\hat\sigma_d$ au lieu de zéro, et la
> zone morte ainsi créée reçoit le verdict **`ZONE MORTE`**, compté à part.
>
> `ZONE MORTE` et `NON TRANCHEE` sont **deux verdicts distincts**, et les
> confondre serait perdre l'information que la piste apporte : le premier dit
> *« la clause a été évaluée, et l'écart est trop petit pour trancher »*, le
> second *« il manque une donnée »*. Un taux de confirmation se lit sur les
> seules thèses réellement tranchées.

Coût déclaré : un amorçage de douze mois. **Il ne coûte ici aucune date d'audit**,
parce que les séries commencent le 2019-01-02 et que la première décision est
celle du 2020-12-31 : les douze écarts mensuels précédents sont tous disponibles,
et tous antérieurs à la date qu'ils servent. Ce serait faux d'une expérience dont
les séries commenceraient à la première décision, et c'est pourquoi le protocole
exige les deux ans d'amorce.

**Si les douze écarts ne sont pas tous disponibles, aucune thèse `REFLEXIVE`
n'est écrite** — la clause n'aurait pas d'échelle. Le cas ne se présente pas sur
cette fenêtre, et le bilan publie le compte pour qu'on le vérifie plutôt que pour
qu'on le croie.

### Les deux thèses

**`CANAL`** — la figure tient : à la décision suivante, distante de $k$ séances,
la clôture restera entre $\text{support}(d) + k\,\text{pente}_{\text{sup}}$ et
$\text{résistance}(d) + k\,\text{pente}_{\text{rés}}$. Si $\tau < k$, les bornes
s'inversent et la thèse est **inconfirmable à l'écriture** : elle est comptée
dans une ligne à part, et non parmi les démenties.

**`REFLEXIVE`** — la phase, pour les seules valeurs à canal déclaré :

| Phase | Condition à $d$ | Clause sur $[d, d']$ |
|---|---|---|
| `AUTO-RENFORCEMENT` | `TEND_120` = +1, `TEND_20` = +1, position > 65 % | écart contre `TR39` **≥ +0,5 σ̂** |
| `RETOURNEMENT` | `TEND_120` = −1, `TEND_20` = −1, position < 35 % | écart contre `TR39` **≤ −0,5 σ̂** |
| `AUCUNE SEQUENCE` | tous les autres cas | écart contre `TR39` **dans ± σ̂** |
| `HORS CHAMP REFLEXIF` | valeur sans canal déclaré | *(aucune thèse)* |

---

## Ce que contient chaque markdown mensuel

Douze fichiers, [`rapports/2022-01.md`](rapports/2022-01.md) à
[`rapports/2022-12.md`](rapports/2022-12.md) :

1. Les **actualités** du mois précédent.
2. Le **dépouillement des thèses** écrites le mois d'avant.
3. L'**exposition héritée** à la date de décision.
4. **Le portefeuille depuis le 3 janvier 2022** — les données générales, le
   graphique, puis **le tableau de toutes les positions prises depuis le début de
   l'expérience**, closes comme ouvertes : société, prix et date d'achat, prix et
   date de vente. Une position ouverte laisse les deux dernières colonnes vides.
5. **L'étude chartiste** — une note de cinq lignes au plus **par société de
   l'univers du jour** — 38 en janvier, 39 ensuite, **467 en tout** —,
   **chacune accompagnée de la figure de décision qui la justifie**.
   La figure est celle que la règle a lue ce jour-là ; elle porte les cinq
   critères, les vetos et le verdict, et se recoupe donc avec le classement du § 6.
6. Le **classement**, avec les cinq composantes, les vetos et τ.
7. Les **ordres exécutés**, chacun avec son motif chiffré.
8. La **lecture du mois**, entièrement calculée.
9. Les **thèses écrites** ce mois-ci, à dépouiller le mois suivant.

> Le graphique du fichier de mars s'arrête fin mars, et le classement de mars a
> été calculé fin février. Aucune décision, aucune figure et aucune échelle ne
> s'appuie sur une séance postérieure à sa date de décision.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| [`bilan-2022.md`](bilan-2022.md) | le bilan, entièrement calculé, audits compris |
| `rapports/2022-01.md` … `2022-12.md` | les douze journaux mensuels |
| [`journal.py`](journal.py) · [`journal.md`](journal.md) | le moteur et son miroir d'exécution |
| [`univers.csv`](univers.csv) | la composition de l'indice aux 24 dates, exclusions motivées |
| [`canaux.csv`](canaux.csv) | le canal de transmission déclaré de chaque valeur |
| [`actualites.md`](actualites.md) · [`chartiste.md`](chartiste.md) | le texte rédigé à la main |
| `criteres.csv` | les évaluations de la règle, décalages et variantes compris |
| `classement.csv` · `ordres.csv` · `theses.csv` | classement, ordres, registre |
| `portefeuille.csv` · `fantome.csv` | les valorisations quotidiennes |
| `graphiques/portefeuille-2022-MM.svg` | les douze courbes |
| `graphiques/{TICKER}/decision-{TICKER}-{DATE}.svg` | les 467 figures de décision de l'année narrée, une société par répertoire |

---

## Ce que l'expérience 3 ne fait toujours pas

- **Aucun levier, aucune couverture, aucun ordre stop, aucune vente à découvert.**
- **Aucun fondamental dans le score.** Les ratios point-in-time n'entrent que
  dans la déclaration des canaux de transmission, jamais dans le classement.
- **Aucune prédiction de cours.** Les thèses portent sur des écarts relatifs
  normalisés et sur la tenue d'une figure.
- **Aucun conseil en investissement.** C'est la sortie d'une règle, consignée.

## Pour aller plus loin

- [L'expérience 1](../experience_1/README.md) — même année, douze valeurs, `TR12`
- [L'expérience 2](../experience_2/README.md) et [sa revue](../experience_2/review.md) — d'où viennent les cinq corrections
- [Semestre 4 · trading](../../../raw/concept/semestre4/trading/README.md) · [alpha](../../../raw/concept/semestre4/alpha/README.md) · [finance](../../../raw/concept/semestre4/finance/README.md)
