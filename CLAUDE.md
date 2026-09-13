# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Langue

Répondre à l'utilisateur en français. Cela s'applique à tous les échanges
(explications, résumés, questions, messages de commit) dans ce dépôt. Les
messages console et l'aide des CLI sont également en français — garder cette
convention dans toute modification.

## Ce qu'est ce dépôt

Deux choses, également importantes :

1. **Onze utilitaires Python en ligne de commande** qui récupèrent et analysent
   des données de la Bourse de Paris. Pas de paquet, pas de tests, pas de
   `__init__.py` — chaque script se lance depuis la racine du dépôt.
2. **Un cours en quatre semestres**, dans `docs/raw/concept/`, qui démontre tout
   ce que les scripts calculent. Le parcours est décrit par
   [`docs/raw/planning.md`](docs/raw/planning.md).

Les tickers de Paris portent le suffixe `.PA` (`AIR.PA`, `MC.PA`) ; les indices
un `^` initial (`^FCHI`), qui **exige des guillemets** en ligne de commande.

## Règle : miroir Markdown des scripts Python

Tout fichier `.py` doit être accompagné d'un fichier `.md` **du même nom**, placé
à côté de lui (ex. `python/import_societe.py` ⇔ `python/import_societe.md`).

Ce markdown est le **miroir de l'exécution** du script : il décrit, dans l'ordre
du déroulement, ce que le script fait réellement — arguments CLI et valeurs par
défaut, étapes de traitement, formules exactes, colonnes produites, affichage
console, fichiers écrits, codes de sortie, cas limites. Il décrit le
comportement, pas le code.

Le markdown fait autorité : lorsqu'une évolution demande un arbitrage (nom d'une
colonne ou d'un argument, valeur par défaut, gestion des `NaN`, format de sortie,
comportement en cas d'erreur…), **mettre le markdown à jour d'abord**, puis
aligner le script dessus. Jamais l'inverse.

La skill `/python-sync` détecte les markdown modifiés et répercute les
changements dans les scripts correspondants.

## Les onze scripts

| Script | Ce qu'il produit |
|---|---|
| `import_societe.py` | OHLCV + indicateurs glissants + test de tendance → `docs/raw/data/quotes/` |
| `import_fondamentaux.py` | ratios **du jour** + limite 1 du carnet ; `--archiver` empile dans `archive.csv` |
| `reconstituer_fondamentaux.py` | ratios **point-in-time** sur 3 à 4 ans, chaque exercice daté par sa publication |
| `import_dividendes.py` | dividendes et divisions depuis `bnains.org`, confrontés à yfinance |
| `generer_graph_supp_resistance.py` | SVG : encadrement support/résistance sur les **clôtures** |
| `generer_graph_canal.py` | SVG : les **trois derniers encadrements** ancrés à une date — bandes à ± 1 s sur 250 et 120, **enveloppe des résidus** sur 20 |
| `generer_graph_decision.py` | SVG : encadrement sur **High/Low**, cinq critères et verdict |
| `couts_transaction.py` | coût d'exécution d'une règle, et l'alpha qu'il faudrait pour le couvrir |
| `evaluer_portefeuille.py` | alpha d'un **panier** contre son indice, coûts et biais d'indice nu compris |
| `construire_indice_total.py` | un indice de référence **en rendement total**, à partir de composants déclarés |
| `dimensionner_exposition.py` | levier admissible, drag et barrière — et **le rendement qu'il faudrait** pour justifier chaque levier |

**Lire le miroir avant de modifier un script.** Il contient les formules, les
conventions et les pièges déjà rencontrés.

## Invariants, valables partout

- **`yfinance` est la seule dépendance externe** (`pandas` arrive avec lui).
  **Ne pas ajouter `scipy`** — la loi de Student est réimplémentée en Python pur
  dans `import_societe.py` (`p_valeur_student`), à réutiliser plutôt qu'à
  redoubler. Ni `matplotlib` (les SVG sont écrits à la main), ni `requests`
  (`urllib` suffit), ni `beautifulsoup4`.
- **Une cellule vide plutôt qu'un nombre inventé.** Quand ni la valeur ni ses
  composants ne sont disponibles, la colonne reste vide — jamais `nan`, `None`
  ou `0`. Une cellule vide est une information.
- **Un dénominateur nul ou négatif ne produit pas de ratio.** Un multiple
  d'EBITDA négatif ne se compare à rien.
- **Jamais de regard en avant.** Aucune quantité datée du jour `d` ne peut
  dépendre d'une séance postérieure, échelles de graphique comprises.
- ⚠️ **`Close` est ajustée des dividendes, `^FCHI` ne l'est pas.** Comparer les
  deux fabrique de l'alpha à partir de rien : **7,9 points par an** mesurés sur
  24 ans. La sortie propre est `construire_indice_total.py`, qui fabrique un
  indice de même convention. Le signaler en note de bas de page ne suffit pas,
  ce biais renverse les verdicts.
- ⚠️ **Une scission n'est pas une division, et le fournisseur ne la répercute
  pas.** Quand une société distribue les titres d'une **autre** société, la série
  encaisse la chute sans jamais créditer ce qui a été reçu : elle fabrique une
  perte que le porteur n'a pas subie — le même vice que l'indice nu comparé à un
  indice en rendement total. Vivendi perd **77,8 % au 2024-12-09** sans qu'aucune
  division ne soit déclarée, son ouverture à 1,896 € succédant à une clôture de
  8,595 € la veille. Le contrôle qui l'attrape : **tout saut de clôture supérieur
  à 50 % en une séance sans division déclarée** vaut opération sur titre
  présumée, donc **série irrecevable**. Le seuil sépare ce cas des mouvements de
  marché — deux valeurs qui décrochent de 17 % le même jour sont un krach, pas
  une opération sur titre.
- **Une convention ne se devine pas depuis des nombres.** Un indice nu et un
  indice en rendement total sont deux séries de niveaux, formellement
  indiscernables. Quand une convention change un résultat, la faire **déclarer**
  plutôt que tenter de la détecter.
- **Fins de ligne : `.gitattributes` s'en charge, ne rien convertir à la main.**
  La règle est **LF partout**, sauf deux exceptions imposées par leurs
  producteurs : les `.csv` (`csv.writer` émet du CRLF, RFC 4180, Excel) et les
  `.svg` (les générateurs les écrivent ainsi sous Windows). Écrire un fichier
  sans se soucier de ses fins de ligne est donc désormais sans conséquence — et
  un script qui en convertirait d'autorité produirait des diffs de centaines de
  lignes pour zéro changement de contenu.

### Lint

```bash
pip install ruff
python -m ruff check python/ docs/     # doit sortir « All checks passed! »
```

`ruff.toml` fige le jeu de règles à la racine. **L'objectif est zéro
signalement**, et il est tenu : un lint qui rend toujours onze lignes n'est plus
un signal, c'est un bruit de fond qu'on cesse de lire — et c'est ainsi qu'on
manque le douzième.

Les exemptions sont de deux natures, à ne jamais mélanger :

- une règle **contraire à une convention du dépôt** est écartée dans
  `ruff.toml`, motif à l'appui — `DTZ011` parce qu'on travaille en dates
  calendaires locales, `RUF001` parce que la typographie française utilise
  délibérément espaces insécables et tirets demi-cadratins ;
- un **cas particulier justifié** porte un `# noqa: RÈGLE` sur sa ligne, avec sa
  raison. Les six `except Exception` autour des appels réseau sont dans ce cas.

Conséquence à respecter : **ne pas ajouter d'exemption globale pour faire taire
un cas isolé.** Un nouveau `except` aveugle doit rester visible — c'est ce
mécanisme qui a fait trouver quatre gestionnaires qui avalaient l'erreur en
silence dans `reconstituer_fondamentaux.py`.

`ruff format` **n'est pas** appliqué : il reformaterait les six scripts d'un
coup, pour un gain nul.

### Ce qui est suivi par git, et ce qui ne l'est pas

**Toutes les données produites par les scripts vivent sous `docs/raw/data/`** —
`quotes/`, `graphs/`, `fondamentaux/`, `dividendes/`. `docs/raw/` ne contient donc
plus que le cours (`concept/`, `planning.md`, `modele.md`), le laboratoire
(`lab/`) et ce répertoire.

`docs/raw/data/quotes/`, `docs/raw/data/graphs/`, les CSV du jour de
`docs/raw/data/fondamentaux/` et le cache HTML de `docs/raw/data/dividendes/` sont
**exclus** : ils se régénèrent d'un appel.

> ⚠️ **`docs/raw/data/fondamentaux/archive.csv` est la seule donnée du dépôt qui ne se
> régénère pas.** Le `.gitignore` l'excepte explicitement. Ne jamais l'écraser :
> le script n'y ajoute que des lignes, et refuse les doublons `(TICKER, DATE)`.

## Les cours

```
docs/raw/planning.md              le parcours, quatre semestres
docs/raw/modele.md                l'énoncé de la démonstration centrale
docs/raw/concept/
├── semestre1/  algèbre · dérivation-intégration · convexité
├── semestre2/  statistique mathématique
├── semestre3/  loi de Student · tests multiples · modèle · canal · encadrement
├── semestre4/  alpha · fondamentaux · trading · finance
└── sommaire/   les index, hors parcours
```

Un répertoire contient **soit** des sous-répertoires, **soit** des fichiers.
Les liens entre cours sont **relatifs** ; après tout déplacement, vérifier qu'ils
résolvent tous.

## Le laboratoire

`docs/raw/lab/` est le troisième objet de `docs/raw/`, et il ne se confond ni avec
le cours ni avec une expérience : **une question, mesurée une fois, sur des
données déclarées**, avec le générateur qui la refait versionné à côté d'elle. Pas
de portefeuille, pas d'ordre, aucun verdict. Le protocole est dans son
[`README.md`](docs/raw/lab/README.md).

- [`largeur-de-bande-fiable.md`](docs/raw/lab/largeur-de-bande-fiable.md) — la
  bande la plus étroite qui **encadre encore**, cherchée en balayant la longueur
  de fenêtre, sur LVMH étalonné 2019-2024 et jugé sur 2025.

> ⚠️ **La convention `± 2 s` n'a pas le taux de couverture qu'elle annonce, et
> l'écart est d'un ordre de grandeur.** Dès la **séance suivante** celle de
> l'ajustement, elle contient 76 à 88 % des clôtures au lieu de 95,5 % : il
> faudrait `± 2,9 s`. Un seuil posé à `± 2 s` ne sélectionne donc pas un événement
> à 4,5 % mais à 12-20 % — ce n'est pas un argument contre les règles des
> expériences 4 à 12, c'est la correction de ce qu'on croit mesurer en les
> appliquant. Et la bande de six ans qui contenait **67,8 %** de son propre
> ajustement — pour 68,3 % attendus, la conformité de manuel — n'a contenu que
> **0,8 %** de l'année suivante. **Compter les points dedans dans la fenêtre qui a
> servi à l'ajuster ne mesure rien.** Et `± 3 s`, la largeur que ce même balayage
> désigne comme honnête, enferme **100,0 %** de l'ajustement pour **29,4 %** de
> l'année suivante : **tripler la largeur ne rend pas fiable, cela déplace le seuil
> où l'on échoue.**
>
> ⚠️ **Un `CORR` élevé n'est pas un permis d'extrapoler.** Des deux bandes
> mesurées sur LVMH, celle qui affichait `CORR` = +0,868 a projeté **0,8 %** de
> l'année suivante dans `± 1 s` ; celle qui affichait +0,244 — à peine au-dessus
> du seuil `CORR_FAIBLE` — en a projeté **15,3 %**. Les deux ont le même `s` à
> 0,2 % près : ce qui les sépare est la **pente**, et la mieux ajustée a
> fidèlement prolongé une tendance qui avait cessé. `CORR_FAIBLE` écarte les
> droites qui n'expliquent rien ; **il ne promeut pas celles qui expliquent
> beaucoup.**
>
> ⚠️ **Changer la date de début déplace la prévision d'une bande entière.** Deux
> étalonnages également défendables de la même série — depuis 2019, depuis 2022 —,
> arrêtés à la **même** charnière, annoncent pour le 2025-12-31 **869,51 €** et
> **725,64 €**, quand le cours cote **634,65 €** : 143,87 € d'écart entre eux, soit
> **88 % de la largeur `± 1 s`**. Un encadrement dont la position dépend à ce point
> du moment où l'on a commencé à regarder n'encadre pas — il enregistre la pente du
> morceau de passé qu'on lui a donné.

## Les expériences

`docs/done/experimentation/` consigne des **expériences datées**, inspirées du
journal en temps réel de la deuxième partie de *L'Alchimie de la finance*.

- `experience_1/` — un portefeuille de 10 000 € sur l'année 2022, douze journaux
  mensuels, univers de douze valeurs du CAC 40 déclaré à l'avance. Le protocole
  est dans son [`README.md`](docs/done/experimentation/experience_1/README.md).
- `experience_2/` — la **même règle sur 2025, mais auditée** : les cinq pistes
  retenues par le vote de
  [`experience_1/review.md`](docs/done/experimentation/experience_1/review.md) y
  sont appliquées. Les quatre vetos de la règle du module 3 sont **appliqués**,
  `s3` est **aligné** sur les seuils qu'elle cite (avec un portefeuille fantôme
  gardant l'ancien sens), et un **registre de thèses réfutables** est engendré
  puis dépouillé chaque mois. Le protocole est dans son
  [`README.md`](docs/done/experimentation/experience_2/README.md).
- `experience_3/` — **2022 rejouée sur tout le CAC 40**, à sa composition réelle
  à chaque date de décision, lue dans
  [`univers.csv`](docs/done/experimentation/experience_3/univers.csv). C'est la
  correction du **biais du survivant** que les deux premières déclaraient sans le
  corriger, et les cinq pistes retenues par
  [`experience_2/review.md`](docs/done/experimentation/experience_2/review.md) y
  sont appliquées. Le protocole est dans son
  [`README.md`](docs/done/experimentation/experience_3/README.md). L'analyse
  après coup de ses deux plus lourdes pertes est dans
  [`pistes-pertes.md`](docs/done/experimentation/experience_3/pistes-pertes.md).
- `experience_4/` — **2022, une règle réduite à deux bandes, lue à chaque
  séance** : TOP 10 des taux de pente sur 120 séances, achat sous
  `VAL_120 − 1 s` si la pente sur 20 séances monte, vente au-dessus de
  `VAL_120 + 1 s`. La règle a été formulée après avoir vu 2022, et le protocole
  la déclare de catégorie B. Son [`review.md`](docs/done/experimentation/experience_4/review.md)
  a retenu cinq pistes, toutes de catégorie A. Le protocole est dans son
  [`README.md`](docs/done/experimentation/experience_4/README.md).
- `experience_5/` — **l'expérience 4 remesurée** par ces cinq pistes : même
  portefeuille, vérifié ordre par ordre, mais intervalles par grappes de dates,
  vingt phases et correction de Holm, portefeuille fictif `MENSUEL` séparant la
  règle de sa cadence, bande jugée contre deux références simulées, dimensionnement
  projeté sur la règle elle-même, témoin aléatoire. Le protocole est dans son
  [`README.md`](docs/done/experimentation/experience_5/README.md).
- `experience_6/` — la même règle **à dix lignes, avec un achat persistant** —
  deux clôtures consécutives sous le bord bas —, et un **alpha officiel mesuré
  contre une référence à exposition appariée**. Trois pistes tirées des cinq
  bilans : réduire les frais, séparer l'alpha du bêta, diluer le risque propre.
  Les quatre combinaisons lignes × persistance tournent en parallèle, et
  `L5-P1` **doit retrouver la règle de l'expérience 4 ordre par ordre**, sinon le
  moteur s'arrête. Le protocole est dans son
  [`README.md`](docs/done/experimentation/experience_6/README.md).
- `experience_8/` — **une seule valeur, Air Liquide, une décision par semaine**, et
  six règles dont la quatrième **supprime toute sortie en perte** : sous
  `prix d'achat − 1 s`, la règle n'allège pas, elle **rachète** 10 %. La seule
  vente est celle du bord haut. La règle se lit sur la série **ajustée**, mais les
  quantités, les espèces et la valorisation passent en **cours réels**, divisions
  postérieures retirées. Les quatre variantes — avec et sans les règles 4 et 6 —
  sont **étalonnées sur 2019-2021 et publiées au protocole avant de jouer
  2022-2026** ; le moteur les recalcule et signale tout écart. Le protocole est
  dans son [`README.md`](docs/done/experimentation/experience_8/README.md).

  Il n'y a **pas d'`experience_7/`** : elle portait les mêmes règles avec un
  **ordre stop**, et a été supprimée avant d'être jouée — l'expérience 8 la
  remplace par son inversion.
- `experience_9/` — **les six règles de l'expérience 8, inchangées, sur cinq
  valeurs** : Air Liquide, plus quatre **tirées au sort** dans le CAC 40 du
  2019-01-02. Le tirage est déclaré avant d'être fait — 39 candidates triées par
  ISIN croissant, `random.Random(9)`, **les quatre premières recevables** — et le
  moteur **rejoue la permutation à chaque exécution**, s'arrêtant si
  [`univers.csv`](docs/done/experimentation/experience_9/univers.csv) en diffère.
  Chaque ligne vaut 10 % du portefeuille, aucun levier, et l'**écart le plus
  négatif est servi le premier** quand les espèces manquent. Vivendi, tirée au
  rang 1, a été **écartée sur ses données** — voir l'invariant sur les scissions
  — et ENGIE l'a remplacée, comme la règle le prévoyait. Le protocole est dans
  son [`README.md`](docs/done/experimentation/experience_9/README.md).
- `experience_10/` — les six règles de l'expérience 9 **plus une septième, qui
  vend dès que le repli depuis le prix d'achat atteint −15 %**, sur **dix valeurs**
  tirées avec la graine 10. Le seuil sort de l'analyse des replis de
  l'expérience 9 : c'est une piste de **catégorie B**, et le protocole la soumet à
  un univers **inédit à huit valeurs sur dix**. La règle 7 se constate à **chaque
  clôture** — entorse déclarée à la cadence hebdomadaire —, depuis le prix de la
  **première tranche**, figé, avec **quatre semaines de carence** avant tout
  rachat. Trois valeurs tirées sont écartées sur leurs seules données : Vivendi,
  Technip et Unibail, faute de série exploitable en euros. Le protocole est dans
  son [`README.md`](docs/done/experimentation/experience_10/README.md).
- `experience_11/` — **l'expérience 10 privée de sa règle 7** : mêmes dix valeurs,
  même tirage, même dimensionnement, six règles au lieu de sept, et la règle 5
  redevenue seule sortie. Son résultat était **déjà publié** — c'est la variante
  « sans la règle 7 » du bilan de l'expérience 10 —, aussi le protocole le **donne
  en tête** plutôt que de le ménager pour la fin. Ce qu'elle ajoute est le détail
  que l'autre résumait en une ligne, et un **contrôle de reproduction ordre par
  ordre** : ses 112 ordres sont confrontés un par un à ceux du moteur voisin,
  quantités et prix compris. Le protocole est dans son
  [`README.md`](docs/done/experimentation/experience_11/README.md).
- `experience_13/` — **la première qui ne joue aucun portefeuille.** Elle ne passe
  aucun ordre et ne mesure aucun alpha : elle mesure une **grandeur sur des
  événements datés**, parce que l'alpha ne peut rien trancher sur un an. Objet :
  l'écart réduit à une droite extrapolée porte-t-il ce qu'une standardisation
  **sans droite** ne porte pas ? Quatre bras — régression, sans droite, marche
  aléatoire, dates au hasard — sur le **CAC 40 point-in-time 2010-2018**, 115
  ancrages, 28 911 événements. Le protocole est dans son
  [`README.md`](docs/done/experimentation/experience_13/README.md), le verdict
  dans son [`bilan.md`](docs/done/experimentation/experience_13/bilan.md).

> L'expérience 13 a **réfuté** la piste qui l'avait fait naître : +2,37 points
> mesurés sur 2019-2026 deviennent **+0,11, IC₉₅ [−0,84 ; +1,03]**, sur les neuf
> années précédentes — l'intervalle **exclut** l'effet annoncé. **Aucune des
> dix-huit cellules ne survit à Holm.** C'est le second échec de réplication d'une
> piste de **catégorie B** après la coupe à −15 % de l'expérience 10, et le
> mécanisme est le même : une piste mesurée sur les données qui l'ont suggérée ne
> survit pas à un univers qu'elle n'a pas servi à fabriquer.
>
> ⚠️ **Elle a aussi montré qu'un contrôle de validité se corrige comme un test.**
> Son témoin nul a d'abord fermé la vanne et arrêté l'expérience : six intervalles
> à 95 % **sans correction de multiplicité** se déclenchent à tort **26,5 % du
> temps**, soit plus souvent que le test qu'ils protègent. Le témoin valait
> −0,054 point sur 12 482 tirages — nul, comme sa construction l'exige. **Un
> garde-fou non corrigé n'est pas un garde-fou**, et la correction ne fut
> recevable que parce qu'elle était démontrablement **neutre sur le verdict**.

> L'expérience 11 a ajouté deux disciplines que les suivantes reprennent. **Quand
> le résultat est connu avant d'écrire l'expérience, il se publie en tête du
> protocole** : le ménager pour la fin serait mimer une prédiction qu'on ne fait
> pas. Et **quand deux expériences partagent le même portefeuille, la reproduction
> s'exige sur les quantités, pas seulement sur les dates** — 112 ordres confrontés
> un par un, zéro écart, là où l'expérience 9 ne pouvait comparer que des dates à
> l'expérience 8. Elle a aussi rendu visible un coût qu'aucun tableau de synthèse
> ne montrait : **11 ordres refusés faute d'espèces** contre un seul avec la
> règle 7, parce qu'un portefeuille qui ne coupe jamais reste investi et manque de
> liquidités au moment où un signal se présente.

> L'expérience 10 a soumis une piste de **catégorie B** au seul test qui vaille —
> un univers qu'elle n'avait pas servi à fabriquer — et **la piste n'y a pas
> survécu**. Le seuil de coupe à −15 %, lu sur les replis de l'expérience 9, a
> produit **9 coupes dont 8 mauvaises, pour −1 783 €**, et coûté **4,00 points
> d'alpha**. Son mérite apparent à l'étalonnage — +4,60 pt — ne venait pas de la
> protection, qui y coûtait déjà 208 €, mais d'une **exposition réduite pendant un
> seul krach**, celui de mars 2020. **Un garde-fou éprouvé sur un unique épisode
> n'est pas éprouvé**, et un gain d'alpha peut n'être qu'une absence du marché au
> bon moment.

> L'expérience 9 a rendu mesurable ce que l'expérience 8 ne pouvait pas juger, en
> portant la part investie de 1,39 % à 18,19 % : son alpha officiel de
> **−9,61 pt dépasse son effet minimal détectable de ± 7,7**. C'est le premier
> verdict tranché du dépôt, et il est **défavorable à la règle**. Surtout,
> l'ordre des quatre variantes annoncé par l'étalonnage s'est **reproduit à
> l'identique** sur des données qu'il n'avait pas vues — −0,89, −2,80, −7,98,
> −9,61 à mesure qu'on ajoute les achats à la baisse. **Moyenner à la baisse
> achète de l'exposition, pas de l'alpha** : les mêmes règles qui coûtent sept
> points d'alpha *ajoutent* +3,89 points de performance brute.

> L'expérience 8 a joué **245 décisions pour 10 ordres**, et sa règle 6 ne s'est
> **jamais** déclenchée : la variante « sans la règle 6 » est rigoureusement
> identique à la règle déclarée, au centime. **Un contrefactuel qui ne diffère
> d'aucun chiffre mesure une règle morte, pas une règle neutre** — encore
> faut-il compter les déclenchements pour s'en apercevoir. Et avec **1,39 % de
> part investie moyenne**, son alpha officiel de +0,17 pt est indiscernable de
> zéro (EMD ± 0,5) : **une règle si peu exposée ne peut rien démontrer, quel que
> soit son résultat.**

> L'expérience 6 a réduit les frais de 0,77 point de dotation — le seul gain
> certain — et perdu son alpha : **+4,54 pt d'alpha officiel pour la règle de
> l'expérience 4, −3,65 pt pour elle.** Surtout, son écart brut à l'indice reste
> positif, +4,32 points, alors que l'exposition à elle seule en explique +7,97 :
> **un écart brut à l'indice n'est pas un alpha**, et une règle moins exposée
> paraît bonne dans une année qui baisse.

> L'expérience 5 a fait tomber le seul résultat positif de l'expérience 4 : un
> écart « significatif » mesuré sur 39 valeurs **le même jour contre le même
> indice** ne l'est plus quand on compte les dates, pas les valeurs. **Un
> intervalle d'issue se calcule par grappes de dates**, et se publie sur toutes
> les phases du sous-échantillon.

⚠️ **L'univers d'une expérience est le CAC 40 entier, en composition
point-in-time.** Une liste de valeurs choisies aujourd'hui parmi celles qui
étaient à l'indice dans l'année jouée est un biais du survivant, quoi qu'en dise
la note de bas de page. La composition historique se reconstruit depuis
[`bnains.org/archives/histocac/compocac.php`](https://www.bnains.org/archives/histocac/compocac.php),
qui rend exactement quarante valeurs par date, alias déjà résolus — le rejeu des
mouvements depuis 1987 par `histocac.php` échoue sur les changements de nom.

⚠️ **Le dimensionnement se publie avant la première séance, pas après.** Une
expérience d'un an sur ce dispositif a une tracking error de **8 à 16 %/an**
selon l'année, donc un effet minimal détectable de **± 16 à ± 30 points d'alpha
annuel** : sa performance ne tranche rien, et il faudrait des siècles pour
établir qu'une telle règle couvre ses propres frais. Les taux, eux, se mesurent —
923 évaluations donnent une proportion à ± 3 points près. Une expérience nouvelle
doit donc porter son objet déclaré sur ce qu'elle peut établir, et le dire
**avant**.

> L'expérience 3 a mesuré 15,6 %/an là où elle en déclarait 8,2 : **le
> dimensionnement publié avant peut être trop optimiste d'un facteur deux.** Le
> publier reste ce qui permet de s'en apercevoir.

> L'expérience 10 a montré à quoi sert vraiment ce contrôle. En refusant de
> retrouver ses propres nombres publiés, il a rendu **37 écarts** qui menaient
> tous à un bug : une carence de rachat armée uniquement les jours de décision,
> alors que la règle se constatait à chaque clôture. **Un étalonnage confronté
> attrape des défauts de logique, pas seulement des divergences de mesure.**
> Corriger l'étalonnage reste permis tant que **rien n'est publié ni joué** et que
> la **cause est identifiée** — et la correction se déclare. Après la fenêtre
> jouée, un tel écart ne se corrige plus : il se publie.

⚠️ **Une série ajustée peut porter une opération postérieure à la fenêtre.** Les
divisions et regroupements d'actions sont répercutés rétroactivement par le
fournisseur : tout ce que la règle calcule reste invariant d'échelle, mais **le
nombre de titres achetables ne l'est pas**, et acheter sur un cours rétro-ajusté
laisserait une opération future façonner le portefeuille. Déclarer les valeurs
concernées et **refuser tout ordre sur elles** — un contrôle de recevabilité des
données, jamais un veto de plus.

> Sur un univers d'une seule valeur, l'expérience 8 pousse la parade plus loin :
> elle **retire les divisions postérieures** — `réel = ajusté × Π(ratios
> postérieurs)` — pour acheter au cours réellement coté, et ne garde la série
> ajustée que pour ce que la règle **lit**. Séparer les deux unités est ce qui
> permet d'acheter une valeur qui se divise, au lieu de l'exclure ; mais le seuil
> d'une règle doit alors être comparé dans la même unité que ce qu'il seuille —
> c'est exactement la faute trouvée dans l'expérience 7 avant qu'elle soit jouée.

⚠️ **Une expérience porte sur une année passée, donc tout y est décidé
mécaniquement** : le classement, les ordres et les dates sortent d'un score écrit
avant la première séance, jamais d'un choix rétrospectif. C'est la seule parade
au premier des cinq pièges de l'alpha. Le texte rédigé à la main — actualités,
notes chartistes — est rangé dans des fichiers séparés (`actualites.md`,
`chartiste.md`) dont le moteur ne fait que la mise en page : **aucun chiffre du
journal n'est saisi à la main.**

**La skill `/experience-review`** fait relire une expérience par les trois agents
— `chartiste`, `trading`, `sorosien` — et rassemble leurs quinze pistes
d'amélioration dans un `review.md` posé à la racine de l'expérience. Elle impose
à chaque piste d'être classée **A** (indépendante du résultat, donc proposable
avant la première séance) ou **B** (suggérée par le résultat, donc recevable
seulement si elle est nommée comme telle). Une revue qui ne rend que des pistes B
a relu le résultat, pas le protocole.

Les `journal.py` des expériences sont des scripts du dépôt hors de `python/`. La
règle du miroir markdown s'y applique comme partout ailleurs (`journal.py` ⇔
`journal.md`), et ils sont couverts par le lint :

```bash
python -m ruff check python/ docs/
```

Les deux autres scripts hors `python/` sont
[`concept/semestre3/canal/figures/generer_figures.py`](docs/raw/concept/semestre3/canal/figures/generer_figures.md),
qui trace les trois figures du module 2 sur le canal, et
[`lab/figures/generer_largeur_fiable.py`](docs/raw/lab/figures/generer_largeur_fiable.md),
qui balaie les largeurs de bande et trace les trois figures du laboratoire. Même
principe que les `journal.py` : **le générateur est versionné à côté de ce qu'il
produit**, parce qu'une figure qu'on ne peut pas refaire ne peut pas être
corrigée. Aucun des deux ne compte parmi les onze utilitaires — le premier ne lit
aucune donnée de marché, le second lit un CSV de `quotes/` mais n'appelle jamais
le réseau.

## Agents

- `chartiste` (`.claude/agents/chartiste.md`) — lit la tendance d'une valeur à
  partir d'un CSV de `docs/raw/data/quotes/` : droite ajustée, canal de régression,
  encadrement par enveloppe convexe, test de significativité, ruptures.
- `trading` (`.claude/agents/trading.md`) — performance, alpha et bêta contre un
  indice de référence, techniques de sélection et ce qui est calculable ici,
  verdict achat/vente/attente issu d'une règle **écrite à l'avance**.
- `sorosien` (`.claude/agents/sorosien.md`) — lecture réflexive au sens de Soros :
  canal de transmission entre cours et fondamentaux, phase du cycle boom-bust, et
  « aucune séquence réflexive identifiable » par défaut.

**Aucun des trois ne donne de conseil en investissement**, ne dimensionne une
position ni ne prédit un cours. Cette limite est structurante : ne pas la relâcher
sans demande explicite.

## Setup & run

```bash
pip install yfinance

python python/import_societe.py AIR.PA --periode 5y
python python/import_societe.py AIR.PA --debut 2023-01-01 --fin 2024-01-01
python python/import_fondamentaux.py AIR.PA MC.PA --archiver
python python/reconstituer_fondamentaux.py AIR.PA --mensuel
python python/import_dividendes.py --index
```

> ⚠️ **`--fin` est exclusif** : `--fin 2023-12-31` s'arrête à la séance du 30.

Sans argument, chaque script bascule dans une invite interactive.

## Ce que produit `import_societe.py`

Le cœur du dépôt. À l'OHLCV il ajoute un compteur `INDICE` (1, 2, …) puis, pour
chaque fenêtre glissante `n` ∈ {20, 120} sur `Close` : `E_n` (moyenne), `VAR_n`
(variance de population, `ddof=0`), `CORR_n` (corrélation avec `INDICE`), `VAL_n`
(la droite des moindres carrés évaluée au dernier point de la fenêtre), et le test
de Student bilatéral — `T_n`, `P_n` et le verdict signé `TEND_n` au seuil
`--alpha` (0,05 par défaut). Les `n-1` premières lignes restent vides.

Les formules, leur démonstration et tous les cas limites sont dans
[`python/import_societe.md`](python/import_societe.md) et
[`docs/raw/modele.md`](docs/raw/modele.md).
