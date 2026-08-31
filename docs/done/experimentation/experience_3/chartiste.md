# Notes de perspective — expérience 3

Une note par valeur et par date de décision, **467 en tout**. Chacune décrit la
figure que la règle a lue ce jour-là : bornes de l'encadrement, position de la
clôture, géométrie des deux droites, épisodes de contact, durée de vie du canal,
momentum et intervalle de confiance de l'alpha.

> ⚠️ **Ces notes sont strictement descriptives de la figure datée du jour.**
> Elles ne contiennent aucune prévision, aucune cible et aucun conseil — la
> charte de l'agent [`chartiste`](../../../../.claude/agents/chartiste.md) le lui
> interdit. C'est aussi ce qui les rend **vérifiables** : chaque nombre cité se
> lit sur la figure `graphiques/{TICKER}/decision-{TICKER}-{DATE}.svg` conservée
> à côté, et sur la ligne correspondante de `criteres.csv`. Une note qui ne dit
> rien de plus que la figure du jour ne peut pas contenir d'information
> postérieure à ce jour.

Le moteur ne fait que la mise en page de ce fichier.

---

## 2021-12-31

### EL.PA
- Canal 158,31 – 183,06 €, large de 24,8 %, clôture à 166,70 € soit 33,9 % de la hauteur : le tiers bas.
- Les deux droites montent au même rythme, +0,310 et +0,315 €/séance — canal rigoureusement parallèle, τ infini.
- Deux épisodes de contact en support seulement : le veto 1 se déclenche, l'appui bas n'est pas certifié.
- Momentum 12-1 de +38,3 %, l'un des plus forts de l'univers ; l'alpha, +2,9 %/an, reste indiscernable de zéro.

### RI.PA
- Canal 173,94 – 186,12 €, étroit — 12,2 % —, clôture à 176,53 € dans le cinquième bas, 21,2 %.
- Support +0,325 contre résistance +0,271 €/séance : convergence lente, τ de 225 séances, bien au-delà de la cadence.
- Sept épisodes de contact en support contre deux en résistance : c'est le plafond qui n'est pas certifié, d'où le veto 1.
- Momentum +31,7 %, alpha +3,7 %/an avec un IC95 de −15,4 à +22,8 : rien de tranché.

### CAP.PA
- Canal 184,72 – 206,95 €, large de 22,2 %, clôture à 194,02 € à 41,8 % — le milieu bas de la figure.
- Support +0,517 contre résistance +0,323 €/séance : le canal se referme, τ de 114 séances.
- Quatre contacts en bas, trois en haut : les deux bornes sont certifiées, aucun veto.
- Momentum de +67,9 %, le deuxième de l'univers ; alpha +14,4 %/an, IC95 encore à cheval sur zéro.

### DSY.PA
- Canal 49,86 – 57,92 €, clôture à 50,43 € : 7,0 % de la hauteur, presque sur le support.
- Deux droites montantes qui convergent doucement, +0,143 et +0,105 €/séance, τ de 210 séances.
- Trois et quatre épisodes : figure lisible des deux côtés, aucun veto.
- Momentum +57,5 %, alpha +19,5 %/an — le plus élevé après Eurofins, mais l'IC95 descend à −8,5.

### OR.PA
- Canal 377,28 – 406,86 €, clôture à 384,53 € à 24,5 % de la hauteur.
- Support +0,931 contre résistance +0,319 €/séance : la convergence est rapide, τ de 48 séances seulement.
- Trois contacts bas, quatre hauts, aucun veto — mais le canal a moins de trois mois d'espérance de vie.
- Momentum +32,0 %, alpha +13,0 %/an, IC95 de −7,1 à +33,0.

### PUB.PA
- Canal 45,09 – 51,19 €, large de 6,1 %, clôture à 47,96 € en plein milieu, 47,0 %.
- Pentes +0,038 et +0,047 €/séance : les droites s'écartent, canal divergent, τ infini.
- Deux épisodes en support : veto 1, l'appui bas repose sur deux points.
- Momentum +37,6 % malgré un alpha négatif de −7,4 %/an — la hausse est celle du marché.

### RMS.PA
- Canal 1 444,96 – 1 726,37 €, très large — 281 € —, clôture à 1 468,46 € à 8,4 % : contre le support.
- Deux droites fortement montantes, +5,249 et +4,151 €/séance, convergentes, τ de 256 séances.
- Quatre contacts de chaque côté : la figure est lisible, mais la tendance courte est négative quand la longue est positive — veto 3.
- **Seul alpha significatif de la date** : +24,9 %/an, IC95 de +4,9 à +44,9, entièrement positif.

### STMPA.PA
- Canal 39,59 – 47,76 €, clôture à 41,52 € à 23,6 % de la hauteur.
- Pentes +0,116 et +0,119 €/séance : divergence, τ infini, le canal ne se referme pas.
- Deux épisodes en support contre cinq en résistance : veto 1 sur l'appui bas.
- Momentum +26,2 %, alpha +20,6 %/an mais un IC95 de −13,5 à +54,7 : la mesure ne porte rien.

### ACA.PA
- Canal 7,98 – 8,51 €, d'une largeur de 0,5 % seulement, clôture à 8,49 € à 95,2 % : collée au plafond.
- Support +0,007 contre résistance −0,014 €/séance : les droites se croisent dans 25 séances.
- Deux contacts de chaque côté : veto 1. Un canal aussi mince rend la position dans la hauteur peu informative.
- Momentum +24,2 %, alpha −10,1 %/an.

### BNP.PA
- Canal 39,99 – 43,85 €, large de 3,9 %, clôture à 43,76 € à 97,7 % — sous la résistance, à neuf centimes.
- Support montant +0,063, résistance descendante −0,035 €/séance : τ de 39 séances.
- Trois contacts bas, deux hauts : veto 1 sur la résistance.
- Momentum +31,6 %, alpha −6,0 %/an malgré la hausse.

### CS.PA
- Canal 18,40 – 19,78 €, clôture à 19,49 € à 79,1 % de la hauteur.
- Pentes +0,026 et +0,004 €/séance, convergence douce, τ de 64 séances.
- Quatre contacts en support, deux en résistance : veto 1.
- Momentum +31,8 %, alpha −5,3 %/an, IC95 de −24,2 à +13,6.

### GLE.PA
- Canal 21,73 – 24,31 €, clôture à 24,16 € à 94,1 % : contre le plafond.
- Support +0,034, résistance −0,009 €/séance, τ de 61 séances.
- Deux épisodes de chaque côté, veto 1 : la figure repose sur quatre points.
- Momentum de +66,1 %, le troisième de l'univers, pour un alpha de −19,9 %/an — la valeur monte moins que son marché.

### LR.PA
- Canal 88,67 – 93,81 €, clôture à 93,22 € à 88,5 % de la hauteur.
- Pentes +0,151 et +0,046 €/séance, τ de 49 séances : le canal se referme avant deux mois.
- Six contacts en résistance mais deux seulement en support : veto 1 sur l'appui bas.
- Momentum +24,0 %, alpha +9,2 %/an, IC95 à cheval sur zéro.

### MC.PA
- Canal 605,29 – 682,84 €, large de 77,5 €, clôture à 662,71 € à 74,0 % : dans le quart haut.
- Support +0,794 contre résistance +0,324 €/séance, τ de 165 séances.
- Quatre et trois épisodes : les deux bornes sont certifiées, aucun veto.
- Momentum +32,9 %, alpha +16,7 %/an, IC95 de −3,4 à +36,8 — à un point d'être significatif.

### SU.PA
- Canal 145,28 – 159,17 €, clôture à 157,43 € à 87,5 %, tout près du plafond.
- Pentes +0,360 et +0,179 €/séance, convergence, τ de 77 séances.
- Trois contacts bas, quatre hauts, aucun veto : la figure est la plus propre du haut de classement.
- Alpha +18,0 %/an, IC95 de −0,4 à +36,3 : il manque quatre dixièmes pour que la borne basse passe au-dessus de zéro.

### TEP.PA
- Canal 300,84 – 334,89 €, clôture à 328,80 € à 82,1 % de la hauteur.
- Support +0,391 contre résistance +0,133 €/séance, τ de 132 séances.
- Deux épisodes seulement en résistance : veto 1.
- Momentum +34,5 %, alpha +22,0 %/an mais un IC95 large de 59 points.

### TTE.PA
- Canal 31,84 – 34,72 €, clôture à 34,00 € à 75,3 %.
- Pentes +0,056 et +0,006 €/séance, τ de 57 séances.
- Cinq contacts en support et six en résistance : la figure la mieux étayée de la date, aucun veto.
- Momentum +19,8 % pour un alpha de −16,2 %/an : la valeur suit le marché de loin.

### VIE.PA
- Canal 23,38 – 26,41 €, clôture à 26,04 € à 87,9 % de la hauteur.
- Pentes +0,041 et +0,036 €/séance, quasi parallèles, τ de 668 séances — le canal survivra à l'année.
- Trois et cinq épisodes, aucun veto.
- Momentum +39,6 %, alpha +8,2 %/an, IC95 de −16,2 à +32,5.

### AI.PA
- Canal 102,46 – 108,49 €, large de 6,0 %, clôture à 105,00 € à 42,1 % : le milieu.
- Pentes +0,155 et +0,041 €/séance, τ de 53 séances.
- Quatre et cinq contacts : figure lisible, aucun veto.
- Momentum de +9,2 % seulement, sous le seuil de +10 % qui vaut deux points au lieu d'un.

### ENGI.PA
- Canal 8,61 – 8,87 €, d'une largeur de 0,3 % — le plus mince de la date —, clôture à 8,79 € à 70,3 %.
- Support +0,016, résistance −0,011 €/séance : **les droites se croisent dans dix séances**, veto 2.
- Un canal qui se referme avant la décision suivante ne dit rien de la position qu'on y lit.
- Momentum de +1,6 %, quasi nul ; alpha −11,9 %/an.

### ML.PA
- Canal 25,36 – 29,79 €, clôture à 29,40 € à 91,3 % de la hauteur.
- Support en légère baisse, −0,011, résistance en légère hausse, +0,002 €/séance : divergence, τ infini.
- Trois contacts bas, deux hauts : veto 1.
- Tendance longue nulle, tendance courte positive ; momentum +25,3 %.

### SAN.PA
- Canal 68,16 – 72,24 €, clôture à 71,49 € à 81,7 %.
- Support +0,053 contre résistance −0,035 €/séance, τ de 46 séances.
- Trois épisodes de chaque côté : le minimum requis, aucun veto.
- Momentum +10,3 %, à peine au-dessus du seuil ; alpha +0,9 %/an, rigoureusement nul.

### DG.PA
- Canal 68,85 – 77,43 €, clôture à 77,43 € : **exactement sur la résistance**, 100,0 % de la hauteur.
- Les deux droites descendent, −0,012 et −0,060 €/séance, τ de 177 séances.
- Trois et quatre contacts, aucun veto : la figure est lisible et la clôture est à son plafond.
- Momentum +8,3 %, alpha −12,9 %/an.

### AIR.PA
- Canal 86,02 – 104,34 €, large de 18,3 %, clôture à 103,08 € à 93,1 %.
- Deux droites descendantes, −0,072 et −0,097 €/séance, τ de 753 séances : la figure ne se refermera pas.
- Deux contacts de chaque côté — veto 1 — et tendance longue négative contre courte positive — veto 3.
- Momentum +12,6 %, alpha −14,8 %/an avec un IC95 de 75 points de large.

### ERF.PA
- Canal 89,31 – 106,30 €, clôture à 101,96 € à 74,4 % de la hauteur.
- Support −0,027, résistance −0,183 €/séance : le canal se referme, τ de 109 séances.
- Deux contacts en support : veto 1 ; tendances de signes opposés : veto 3.
- **Momentum +40,9 % et alpha +33,6 %/an**, le plus élevé de la date — mais l'IC95 va de −5,0 à +72,2.

### KER.PA
- Canal 593,36 – 636,88 €, clôture à 618,32 € à 57,4 % : le milieu haut.
- Support +1,105 contre résistance −0,611 €/séance : convergence franche, τ de 25 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum +20,4 %, alpha +0,7 %/an — exactement nul.

### MT.AS
- Canal 21,13 – 26,85 €, clôture à 25,96 € à 84,5 % de la hauteur.
- Deux droites légèrement descendantes, −0,008 et −0,022 €/séance, τ de 419 séances.
- Deux épisodes en support : veto 1 ; tendances contradictoires : veto 3.
- Momentum +24,2 %, alpha −11,3 %/an, IC95 de 77 points.

### SGO.PA
- Canal 48,77 – 54,02 €, clôture à 53,55 € à 91,0 %.
- Support +0,020, résistance −0,022 €/séance, τ de 126 séances.
- Trois contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum +38,4 %, alpha +5,2 %/an.

### VIV.PA
- Canal 10,24 – 11,00 €, large de 0,8 %, clôture à 10,85 € à 80,0 %.
- Pentes +0,015 et −0,015 €/séance, symétriques : τ de 25 séances, le canal se referme avant la décision suivante.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +13,0 %, alpha +5,2 %/an.

### BN.PA
- Canal 42,37 – 46,49 €, clôture à 46,17 € à 92,3 % de la hauteur.
- Deux droites descendantes, −0,049 et −0,089 €/séance, τ de 101 séances.
- Trois et quatre épisodes : figure lisible, mais tendances de signes opposés, veto 3.
- Momentum de +4,6 % seulement ; alpha −9,7 %/an.

### ORA.PA
- Canal 6,64 – 7,33 €, clôture à 7,10 € à 66,8 %, juste au-dessus du seuil de 65 %.
- Pentes −0,001 et +0,001 €/séance : divergence imperceptible, τ infini.
- Trois contacts bas, deux hauts : veto 1.
- **Momentum négatif, −2,9 %**, le premier de la liste ; alpha −17,9 %/an, IC95 de −38,2 à +2,5.

### CA.PA
- Canal 11,09 – 12,29 €, clôture à 12,29 € : **sur la résistance exactement**, 100,0 %.
- Support plat, 0,000, résistance −0,011 €/séance, τ de 107 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −1,7 %, alpha −3,3 %/an.

### EN.PA
- Canal 22,28 – 24,25 €, clôture à 24,24 € à 99,6 % : au centime sous le plafond.
- Pentes −0,013 et −0,086 €/séance, τ de 27 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −9,9 %, à un dixième du seuil de −10 % qui coûterait un point de plus.

### SAF.PA
- Canal 90,64 – 102,69 €, clôture à 102,69 € : **sur la résistance**, 100,0 %.
- Support −0,077, résistance −0,428 €/séance : convergence rapide, τ de 34 séances.
- Huit contacts en support — le plus étayé de la date — mais deux seulement en résistance : veto 1.
- Momentum −12,0 %, alpha −23,3 %/an.

### ALO.PA
- Canal 27,00 – 33,28 €, large de 6,3 %, clôture à 30,65 € à 58,1 % : le milieu.
- Deux droites descendantes presque parallèles, −0,033 et −0,037 €/séance, τ de 1 532 séances.
- Deux contacts en support : veto 1.
- **Momentum de −33,6 %**, le plus faible de l'univers après Worldline ; alpha −10,5 %/an.

### HO.PA
- Canal 62,26 – 68,50 €, clôture à 67,99 € à 91,8 % de la hauteur.
- Pentes −0,110 et −0,198 €/séance, τ de 71 séances.
- Cinq contacts bas, deux hauts : veto 1.
- **Alpha significativement négatif** : −26,2 %/an, IC95 de −51,8 à −0,6, entièrement sous zéro.

### WLN.PA
- Canal 300,11 – 506,99 €, d'une largeur de 207 % — la figure la plus étirée de la date —, clôture à 506,42 € à 99,7 %.
- Deux droites en chute, −4,338 et −4,147 €/séance, divergentes : τ infini.
- Trois contacts bas, deux hauts : veto 1.
- **Momentum de −37,7 %, le plus faible de l'univers** ; alpha −11,4 %/an.
- Les niveaux en euros de cette série portent le regroupement de 2026 : seules ses quantités relatives sont comparables aux autres.

### RNO.PA
- Canal 23,63 – 25,86 €, clôture à 25,86 € : **sur la résistance**, 100,0 %.
- Support +0,005, résistance −0,124 €/séance : **le canal se referme en 17 séances**, veto 2, avant même la prochaine décision.
- Deux contacts en résistance : veto 1 également.
- **Alpha significativement négatif** : −41,3 %/an, IC95 de −80,0 à −2,6. Momentum −19,9 %.

## 2022-01-31

### DG.PA
- Canal 79,54 – 83,09 €, large de 3,5 %, clôture à 80,55 € à 28,4 % de la hauteur.
- Support +0,325 contre résistance +0,050 €/séance : **les droites se croisent dans 13 séances**, veto 2 — bien avant la décision suivante.
- Deux contacts en support seulement : veto 1 s'ajoute. La position lue dans un canal aussi éphémère ne s'appuie sur rien.
- Momentum +11,4 %, alpha −9,9 %/an.

### CA.PA
- Canal 12,81 – 14,37 €, clôture à 12,91 € à 6,4 % : le bas de la figure, à dix centimes du support.
- Pentes +0,042 et +0,009 €/séance, convergence, τ de 48 séances.
- Quatre contacts bas, deux hauts : veto 1 sur la résistance.
- Momentum +13,8 %, alpha −0,9 %/an, IC95 de 57 points de large.

### SAN.PA
- Canal 71,77 – 76,83 €, clôture à 74,86 € à 61,0 %, juste sous le seuil de 65 %.
- Support +0,114, résistance +0,029 €/séance, τ de 59 séances.
- Cinq contacts en support, deux en résistance : veto 1.
- Momentum +14,2 %, alpha +2,7 %/an — nul.

### ACA.PA
- Canal 8,13 – 9,53 €, clôture à 8,98 € à 61,0 % de la hauteur.
- Deux droites montantes de même pente, +0,007 : canal parallèle, τ infini.
- Deux contacts de chaque côté : veto 1, la figure repose sur quatre points.
- Momentum +31,7 %, alpha −6,7 %/an.

### AI.PA
- Canal 102,61 – 110,54 €, clôture à 103,67 € à 13,4 % : contre le support.
- Pentes +0,116 et +0,052 €/séance, τ de 125 séances.
- Trois et quatre épisodes : figure lisible, mais tendance longue positive contre courte négative — veto 3.
- Momentum +13,7 %, alpha +3,4 %/an.
- Les niveaux en euros de cette série portent les attributions gratuites de 2024 et 2026.

### BNP.PA
- Canal 41,31 – 49,10 €, large de 7,8 %, clôture à 45,37 € à 52,0 % : le milieu exact.
- Pentes +0,063 et +0,074 €/séance : divergence, τ infini.
- Deux contacts en résistance : veto 1.
- **Momentum +45,1 %** pour un alpha de −3,4 %/an : la hausse est celle du secteur.

### CAP.PA
- Canal 169,32 – 198,84 €, clôture à 177,77 € à 28,6 % de la hauteur.
- Support +0,185 contre résistance +0,031 €/séance, τ de 192 séances.
- Trois contacts de chaque côté, aucun veto 1 ; mais tendances de signes opposés, veto 3.
- Momentum +64,2 %, le deuxième de la date ; alpha +11,9 %/an.

### EL.PA
- Canal 143,81 – 170,00 €, clôture à 148,52 € à 18,0 % : le cinquième bas.
- Support +0,048, résistance −0,071 €/séance : convergence, τ de 221 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum +41,7 %, alpha −0,2 %/an, exactement nul.

### GLE.PA
- Canal 22,43 – 28,35 €, clôture à 26,14 € à 62,8 %.
- Pentes +0,034 et +0,058 €/séance : le canal s'ouvre, τ infini.
- Deux contacts en support : veto 1.
- **Momentum +77,3 %, le plus fort de l'univers** — pour un alpha de −15,4 %/an.

### KER.PA
- Canal 555,94 – 646,57 €, large de 90,6 €, clôture à 576,89 € à 23,1 % de la hauteur.
- Support +0,330 contre résistance −0,078 €/séance, τ de 222 séances.
- Quatre contacts de chaque côté : la figure est bien étayée ; seul le veto 3 se déclenche.
- Momentum +28,3 %, alpha −0,7 %/an.

### LR.PA
- Canal 78,69 – 95,75 €, clôture à 81,35 € à 15,6 % : contre le support.
- Support −0,015 contre résistance +0,056 €/séance : divergence, τ infini.
- Trois contacts bas, six hauts : figure lisible des deux côtés ; veto 3 seul.
- Momentum +34,3 %, alpha +5,2 %/an.

### ML.PA
- Canal 29,61 – 31,96 €, clôture à 30,13 € à 22,1 %.
- Pentes +0,091 et +0,020 €/séance, τ de 33 séances : le canal se referme avant deux mois.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +25,3 %, alpha +2,7 %/an.

### MT.AS
- Canal 23,43 – 30,74 €, clôture à 24,16 € à 10,0 % : le dixième bas.
- Pentes +0,048 et +0,022 €/séance, τ de 288 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +49,6 %, alpha −11,8 %/an avec un IC95 de 76 points.

### OR.PA
- Canal 333,59 – 418,45 €, très large — 84,9 € —, clôture à 347,55 € à 16,4 %.
- Support +0,123 contre résistance +0,413 €/séance : le canal s'ouvre, τ infini.
- Trois et quatre contacts, figure lisible ; veto 3.
- Momentum +34,9 %, alpha +9,8 %/an.

### RI.PA
- Canal 157,29 – 196,78 €, clôture à 157,75 € à **1,2 % de la hauteur** : quasiment sur le support.
- Pentes +0,122 et +0,363 €/séance : divergence marquée, τ infini.
- Trois contacts de chaque côté ; veto 3 seul.
- Momentum +31,2 %, alpha +0,5 %/an.

### RMS.PA
- Canal 1 204,20 – 1 846,34 €, d'une largeur de 642 € — la figure la plus étirée de la date —, clôture à 1 260,53 € à 8,8 %.
- Support +1,035 contre résistance +4,794 €/séance : ouverture rapide, τ infini.
- Trois contacts de chaque côté ; veto 3.
- Momentum +68,5 %, alpha +19,9 %/an, IC95 de −0,4 à +40,2 : à quatre dixièmes de la significativité.

### STLAP.PA
- **Première date où Stellantis entre dans l'univers** : elle vient d'atteindre les 253 séances de volume non nul qu'exige le momentum 12-1.
- Canal 12,05 – 14,16 €, clôture à 12,37 € à 15,2 % de la hauteur.
- Pentes +0,027 et +0,007 €/séance, τ de 108 séances ; deux contacts de chaque côté : veto 1, plus le veto 3.
- Momentum +35,1 % et alpha +43,4 %/an — le plus élevé de la date, mais sur un IC95 de 133 points, c'est-à-dire rien.

### SU.PA
- Canal 132,30 – 167,30 €, clôture à 136,34 € à 11,6 % : contre le support.
- Support +0,100 contre résistance +0,216 €/séance : divergence, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +42,8 %, alpha +13,6 %/an, IC95 de −4,7 à +31,9.

### TTE.PA
- Canal 33,02 – 40,76 €, clôture à 38,84 € à 75,1 % de la hauteur.
- Pentes +0,056 et +0,086 €/séance : le canal s'ouvre, τ infini.
- Quatre contacts bas, trois hauts : **aucun veto**, seule valeur de score +4 dans ce cas.
- Momentum +35,9 % pour un alpha de −10,4 %/an.

### VIE.PA
- Canal 24,97 – 27,64 €, clôture à 25,78 € à 30,1 %.
- Pentes +0,057 et +0,041 €/séance, convergence lente, τ de 160 séances.
- Deux contacts en support contre six en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum +54,1 %, alpha +8,3 %/an.

### CS.PA
- Canal 18,94 – 21,67 €, clôture à 20,81 € à 68,4 %, juste au-dessus du seuil haut.
- Pentes +0,026 et +0,030 €/séance, divergence imperceptible, τ infini.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +44,2 %, alpha −2,0 %/an.

### ENGI.PA
- Canal 8,88 – 9,46 €, large de 0,6 %, clôture à 9,16 € à 47,9 % : le milieu.
- Pentes +0,015 et +0,004 €/séance, τ de 51 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum de +3,5 % seulement ; alpha −9,5 %/an.

### MC.PA
- Canal 605,60 – 701,42 €, clôture à 658,70 € à 55,4 % de la hauteur.
- Pentes +0,604 et +0,555 €/séance, quasi parallèles : τ de 1 958 séances.
- Six contacts en support, quatre en résistance — la figure la mieux étayée de la date ; seul le veto 3 mord.
- Momentum +36,8 %, alpha +16,9 %/an, IC95 de −3,3 à +37,0.

### ORA.PA
- Canal 6,60 – 7,95 €, clôture à 7,86 € à 93,3 % : sous le plafond.
- Support −0,001, résistance +0,006 €/séance : divergence, τ infini.
- Cinq contacts bas, deux hauts : veto 1.
- Momentum +5,0 %, alpha −13,3 %/an.

### PUB.PA
- Canal 45,57 – 50,91 €, clôture à 48,36 € à 52,3 % : le milieu.
- Pentes +0,027 et +0,021 €/séance, τ de 913 séances : le canal survivra largement à l'année.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +32,8 %, alpha −6,1 %/an.

### STMPA.PA
- Canal 36,90 – 43,35 €, clôture à 39,48 € à 40,0 % de la hauteur.
- Support +0,050 contre résistance −0,019 €/séance, τ de 93 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum +26,2 %, alpha +19,6 %/an sur un IC95 de 67 points.

### DSY.PA
- Canal 38,55 – 60,89 €, clôture à 40,92 € à 10,6 % : le dixième bas.
- Support −0,036 contre résistance +0,120 €/séance : le canal s'ouvre, τ infini.
- Deux contacts en support : veto 1.
- Momentum +38,8 %, alpha +12,8 %/an ; la tendance longue est passée à zéro.

### SGO.PA
- Canal 49,31 – 58,37 €, clôture à 51,62 € à 25,5 %.
- Pentes +0,023 et +0,022 €/séance, presque identiques : τ de 7 622 séances, autant dire jamais.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum +49,4 %, alpha +4,8 %/an.

### TEP.PA
- Canal 267,86 – 340,27 €, clôture à 279,65 € à 16,3 % de la hauteur.
- Support −0,130 contre résistance +0,158 €/séance : divergence, τ infini.
- Deux contacts en résistance : veto 1.
- Momentum +37,7 %, alpha +16,9 %/an.

### AIR.PA
- Canal 98,35 – 111,61 €, clôture à 102,86 € à 34,0 %, juste sous le seuil de 35 %.
- Support +0,229 contre résistance +0,028 €/séance, τ de 66 séances.
- Cinq contacts bas, quatre hauts : **aucun veto**, la figure la mieux certifiée de la date.
- Mais les deux tendances sont négatives ; momentum +21,5 %, alpha −13,1 %/an.

### ERF.PA
- Canal 78,23 – 102,46 €, clôture à 83,19 € à 20,5 %.
- Deux droites descendantes presque parallèles, −0,200 et −0,183 €/séance : τ infini.
- Deux contacts en support : veto 1.
- Momentum +36,9 %, alpha +26,7 %/an sur un IC95 de 76 points.

### HO.PA
- Canal 73,31 – 76,39 €, large de 3,1 %, clôture à 74,02 € à 23,0 % de la hauteur.
- Support +0,307 contre résistance −0,022 €/séance : **le canal se referme en 9 séances**, veto 2 — le plus court de la date.
- Tendances de signes opposés : veto 3. Quatre et six contacts pourtant, la figure est étayée mais périmée.
- Momentum −1,9 %, alpha −21,7 %/an.

### RNO.PA
- Canal 23,73 – 31,26 €, clôture à 29,56 € à 77,4 %.
- Pentes +0,005 et +0,028 €/séance : divergence, τ infini.
- Trois et quatre contacts : **aucun veto**.
- **Momentum −23,2 %** et alpha −34,3 %/an : la valeur la plus en retard de la date.

### VIV.PA
- Canal 10,19 – 11,01 €, large de 0,8 %, clôture à 10,59 € à 48,0 % : le milieu.
- Pentes +0,011 et −0,012 €/séance, τ de 35 séances.
- Deux contacts en support : veto 1.
- Momentum +21,2 %, alpha +4,7 %/an ; les deux tendances sont négatives.

### BN.PA
- Canal 38,70 – 48,99 €, clôture à 46,73 € à 78,0 % de la hauteur.
- Deux droites descendantes, −0,109 et −0,052 €/séance : divergence, τ infini.
- Cinq contacts bas, deux hauts : veto 1.
- Momentum +5,6 %, alpha −8,7 %/an.

### SAF.PA
- Canal 89,02 – 108,56 €, clôture à 101,70 € à 64,9 % — un dixième sous le seuil haut.
- Pentes −0,077 et −0,158 €/séance, τ de 241 séances.
- Huit contacts en support, deux en résistance : veto 1, comme le mois dernier.
- Momentum −3,2 %, alpha −21,6 %/an.

### ALO.PA
- Canal 27,69 – 33,89 €, clôture à 28,12 € à 7,0 % : contre le support.
- Support +0,013 contre résistance −0,025 €/séance, τ de 163 séances.
- Deux contacts en support : veto 1.
- **Momentum −28,0 %**, alpha −12,4 %/an ; les deux tendances sont négatives.

### WLN.PA
- Canal 422,86 – 495,03 €, clôture à 441,06 € à 25,2 % de la hauteur.
- Deux droites en chute, −1,048 et −3,089 €/séance, convergentes : τ de 35 séances.
- Cinq contacts bas, deux hauts : veto 1.
- **Momentum −34,5 %**, le plus faible de l'univers ; alpha −14,9 %/an.

### EN.PA
- Canal 20,28 – 24,98 €, clôture à 24,01 € à 79,4 %.
- Deux droites descendantes, −0,052 et −0,044 €/séance : divergence, τ infini.
- Deux contacts en support : veto 1.
- Momentum −1,3 %, alpha −15,2 %/an ; les deux tendances sont négatives.

## 2022-02-28

### DG.PA
- Canal 76,68 – 87,61 €, clôture à 78,77 € à 19,1 % de la hauteur.
- Pentes +0,137 et +0,097 €/séance, convergence lente, τ de 270 séances — le veto 2 du mois dernier a disparu.
- Deux contacts en support : veto 1.
- Momentum +11,3 %, alpha −8,7 %/an.

### KER.PA
- Canal 522,24 – 718,34 €, large de 196 €, clôture à 560,01 € à 19,3 %.
- Support −0,050 contre résistance +1,107 €/séance : le canal s'ouvre franchement, τ infini.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum +16,7 %, alpha −0,2 %/an, rigoureusement nul.

### PUB.PA
- Canal 45,41 – 54,97 €, clôture à 48,31 € à 30,4 % de la hauteur.
- Pentes +0,013 et +0,067 €/séance : divergence, τ infini.
- Deux contacts en support contre cinq en résistance : veto 1.
- Momentum +22,9 %, alpha −4,7 %/an.

### ACA.PA
- Canal 7,63 – 9,75 €, clôture à 7,75 € à 5,8 % : contre le support.
- Pentes +0,001 et +0,008 €/séance, divergence imperceptible, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +14,0 %, alpha −9,4 %/an.

### AI.PA
- Canal 95,33 – 112,87 €, large de 17,6 %, clôture à 101,83 € à 37,1 %.
- Support +0,019 contre résistance +0,086 €/séance : ouverture, τ infini.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum +18,1 %, alpha +3,5 %/an.

### BNP.PA
- Canal 37,12 – 50,58 €, clôture à 37,81 € à 5,1 % : quasiment sur le support.
- Pentes +0,016 et +0,074 €/séance, divergence, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +25,2 %, alpha −7,4 %/an.

### CA.PA
- Canal 13,07 – 13,93 €, large de 0,9 % seulement, clôture à 13,66 € à 68,3 %.
- Support +0,032 contre résistance −0,008 €/séance : τ de 21 séances, le canal se referme presque à la décision suivante.
- Cinq contacts bas, deux hauts : veto 1.
- Momentum +27,7 %, alpha +1,6 %/an.

### CAP.PA
- Canal 158,62 – 199,46 €, clôture à 169,53 € à 26,7 % de la hauteur.
- Pentes +0,039 et +0,031 €/séance, quasi parallèles : τ de 4 839 séances.
- Quatre et trois contacts, figure lisible ; seul le veto 3 mord.
- Momentum +35,9 %, alpha +11,4 %/an.

### CS.PA
- Canal 17,52 – 22,40 €, clôture à 18,07 € à 11,3 % : le bas de la figure.
- Pentes +0,009 et +0,034 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +30,5 %, alpha −5,0 %/an.

### ENGI.PA
- Canal 9,19 – 9,99 €, large de 0,8 %, clôture à 9,64 € à 56,5 % : le milieu.
- Pentes +0,015 et +0,010 €/séance, τ de 159 séances.
- Cinq contacts bas, deux hauts : veto 1.
- Momentum +18,9 %, alpha −6,7 %/an.

### GLE.PA
- Canal 19,86 – 31,07 €, clôture à 20,51 € à 5,8 % : contre le support.
- Support +0,005 contre résistance +0,078 €/séance : ouverture rapide, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- **Momentum +53,9 %** pour un alpha de −20,6 %/an.

### MC.PA
- Canal 570,09 – 712,52 €, clôture à 601,55 € à 22,1 % de la hauteur.
- Support +0,179 contre résistance +0,555 €/séance : le canal s'ouvre, τ infini.
- Quatre et trois contacts, figure lisible ; veto 3 seul.
- Momentum +33,9 %, alpha +14,7 %/an, IC95 de −5,2 à +34,5.

### ML.PA
- Canal 24,41 – 33,12 €, clôture à 25,29 € à 10,2 %.
- Support −0,015 contre résistance +0,042 €/séance : ouverture, τ infini.
- Trois contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum +19,3 %, alpha −1,4 %/an.

### ORA.PA
- Canal 6,57 – 8,50 €, clôture à 8,16 € à 82,3 % de la hauteur.
- Support −0,001 contre résistance +0,013 €/séance, τ infini.
- Quatre contacts bas, cinq hauts : **aucun veto**, la figure la mieux étayée du haut de tableau.
- Momentum +14,6 %, alpha −11,1 %/an.

### SAN.PA
- Canal 71,71 – 77,96 €, clôture à 75,44 € à 59,7 % : sous le seuil haut.
- Pentes +0,076 et +0,055 €/séance, τ de 303 séances.
- **Six contacts en support et quatre en résistance** — la figure la plus étayée de la date, aucun veto.
- Momentum +23,2 %, alpha +3,3 %/an.

### SGO.PA
- Canal 46,58 – 59,84 €, clôture à 48,42 € à 13,9 %.
- Support −0,009 contre résistance +0,053 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +24,8 %, alpha +3,9 %/an.

### STMPA.PA
- Canal 33,42 – 42,98 €, clôture à 36,32 € à 30,4 % de la hauteur.
- Pentes +0,004 et −0,019 €/séance, τ de 410 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +34,8 %, alpha +18,3 %/an sur un IC95 de 66 points.

### TTE.PA
- Canal 34,61 – 42,50 €, clôture à 35,26 € à 8,2 % : contre le support.
- Pentes +0,064 et +0,086 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté ; seul le veto 3 mord.
- Momentum +34,6 %, alpha −11,6 %/an.

### VIE.PA
- Canal 23,77 – 28,63 €, clôture à 25,19 € à 29,4 %.
- Pentes +0,028 et +0,046 €/séance : ouverture, τ infini.
- Trois contacts bas, six hauts : figure lisible ; veto 3.
- Momentum +46,8 %, alpha +8,1 %/an.

### STLAP.PA
- Canal 11,44 – 14,49 €, clôture à 11,94 € à 16,5 % de la hauteur.
- Pentes +0,009 et +0,013 €/séance : quasi parallèles, τ infini.
- Deux contacts de chaque côté : veto 1.
- Momentum +26,4 %, alpha +41,4 %/an mais un IC95 de 130 points : la mesure ne porte rien. Les deux tendances sont passées à zéro.

### AIR.PA
- Canal 97,28 – 110,27 €, clôture à 105,41 € à 62,6 %.
- Support +0,143 contre résistance −0,022 €/séance, τ de 79 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +11,1 %, alpha −10,0 %/an.

### EL.PA
- Canal 135,88 – 168,59 €, clôture à 139,52 € à 11,1 % : le bas de la figure.
- Deux droites descendantes, −0,041 et −0,071 €/séance, τ de 1 104 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +22,0 %, alpha −1,3 %/an.

### MT.AS
- Canal 22,58 – 25,69 €, clôture à 25,55 € à 95,6 % : collée au plafond.
- Support +0,020 contre résistance −0,153 €/séance : **le canal se referme en 18 séances**, veto 2.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3. **Les trois vetos non arithmétiques à la fois.**
- Momentum +22,6 %, alpha −7,6 %/an.

### SU.PA
- Canal 118,72 – 130,57 €, clôture à 127,60 € à 74,9 % de la hauteur.
- Support −0,058 contre résistance −0,858 €/séance : **le canal se referme en 15 séances**, veto 2.
- Tendances opposées : veto 3. Trois contacts de chaque côté, la figure est étayée mais périmée.
- Momentum +20,1 %, alpha +12,3 %/an, IC95 de −5,8 à +30,3.

### VIV.PA
- Canal 10,03 – 10,83 €, large de 0,8 %, clôture à 10,32 € à 36,1 %.
- Pentes +0,008 et −0,010 €/séance, τ de 45 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +9,1 %, sous le seuil de dix ; alpha +4,7 %/an.

### HO.PA
- Canal 73,50 – 96,89 €, large de 23,4 %, clôture à 93,53 € à 85,6 %.
- Pentes +0,188 et +0,174 €/séance, quasi parallèles : τ de 1 740 séances.
- Trois contacts de chaque côté : **aucun veto** — le veto 2 de janvier a disparu.
- Momentum +2,8 %, alpha −11,9 %/an.

### RI.PA
- Canal 154,95 – 164,27 €, clôture à 163,30 € à 89,6 % de la hauteur.
- Support +0,038 contre résistance −0,448 €/séance : **le canal se referme en 19 séances**, veto 2.
- Deux contacts en résistance : veto 1.
- Momentum +23,3 %, alpha +2,1 %/an.

### BN.PA
- Canal 45,30 – 48,73 €, clôture à 45,93 € à 18,5 %.
- Pentes +0,028 et −0,021 €/séance, τ de 70 séances.
- Deux contacts en support : veto 1.
- **Momentum +0,8 %**, le plus faible des valeurs encore positives ; alpha −8,6 %/an.

### LR.PA
- Canal 71,65 – 96,87 €, clôture à 76,84 € à 20,6 % de la hauteur.
- Support −0,083 contre résistance +0,056 €/séance : le canal s'ouvre, τ infini.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum +18,5 %, alpha +4,5 %/an ; mais les deux tendances sont négatives.

### OR.PA
- Canal 302,84 – 328,69 €, clôture à 327,40 € à 95,0 % : sous le plafond.
- Support −0,197 contre résistance −1,804 €/séance : **le canal se referme en 16 séances**, veto 2.
- Quatre et cinq contacts : la figure est bien étayée, mais elle est en train de disparaître.
- Momentum +19,7 %, alpha +8,4 %/an.

### RMS.PA
- Canal 1 098,49 – 1 195,13 €, clôture à 1 189,86 € à 94,5 % de la hauteur.
- Support −0,158 contre résistance −8,325 €/séance : **le canal se referme en 12 séances**, veto 2 — le plus court de la date.
- Trois et quatre contacts : figure étayée mais périmée avant la prochaine décision.
- Momentum +42,9 %, alpha +18,6 %/an, IC95 de −2,0 à +39,2.

### RNO.PA
- Canal 22,86 – 32,44 €, clôture à 24,16 € à 13,5 %.
- Support −0,004 contre résistance +0,036 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- **Momentum −15,3 %** ; alpha −37,7 %/an, IC95 de −75,5 à +0,1 — à un dixième de point d'être significativement négatif.

### DSY.PA
- Canal 36,83 – 42,14 €, clôture à 41,92 € à 95,8 % : contre la résistance.
- Pentes −0,046 et −0,227 €/séance, τ de 29 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum +19,7 %, alpha +14,3 %/an.

### ERF.PA
- Canal 74,24 – 85,84 €, clôture à 84,84 € à 91,4 % de la hauteur.
- Pentes −0,200 et −0,452 €/séance, τ de 46 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum +17,3 %, **alpha +27,4 %/an, le plus élevé de la date** — sur un IC95 de 75 points.

### SAF.PA
- Canal 98,81 – 111,13 €, clôture à 109,40 € à 86,0 %.
- Support +0,142 contre résistance −0,082 €/séance, τ de 55 séances.
- Deux contacts en support : veto 1.
- Momentum −15,3 %, alpha −16,8 %/an.

### TEP.PA
- Canal 255,25 – 279,65 €, clôture à 278,39 € à 94,8 % : sous le plafond.
- Support −0,228 contre résistance −1,478 €/séance : **le canal se referme en 20 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum +9,8 %, alpha +17,3 %/an.

### EN.PA
- Canal 23,52 – 25,35 €, large de 1,8 %, clôture à 24,65 € à 62,0 % de la hauteur.
- Pentes +0,015 et −0,030 €/séance, τ de 41 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum −5,0 %, alpha −12,2 %/an.

### ALO.PA
- Canal 21,18 – 33,76 €, clôture à 22,48 € à 10,3 %.
- Pentes −0,071 et −0,011 €/séance : ouverture vers le bas, τ infini.
- Deux contacts de chaque côté : veto 1.
- **Momentum −32,2 %**, alpha −18,3 %/an.

### WLN.PA
- Canal 401,91 – 503,02 €, clôture à 474,33 € à 71,6 % de la hauteur.
- Deux droites en chute, −1,048 et −2,322 €/séance, τ de 79 séances.
- Six contacts en support, deux en résistance : veto 1 ; tendances opposées : veto 3.
- **Momentum −43,6 %, le plus faible de l'univers** ; alpha −10,3 %/an.

## 2022-03-31

### ORA.PA
- Canal 7,70 – 8,87 €, clôture à 8,08 € à 32,2 % de la hauteur — sous le seuil de 35 %.
- Pentes +0,013 et +0,015 €/séance, quasi parallèles : τ infini.
- Deux contacts en support : veto 1.
- Momentum +14,6 %, alpha −10,5 %/an. Score le plus élevé de la date, et pourtant sous veto.

### TTE.PA
- Canal 34,55 – 37,69 €, clôture à 36,12 € à **50,0 % exactement** : le milieu du canal.
- Support +0,046 contre résistance −0,086 €/séance : τ de 24 séances, le canal se referme presque à la décision suivante.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum +33,0 %, alpha −8,9 %/an.

### CA.PA
- Canal 13,07 – 15,05 €, clôture à 14,99 € à 97,3 % : contre le plafond.
- Pentes +0,023 et +0,014 €/séance, τ de 209 séances.
- Trois contacts bas, deux hauts : veto 1.
- Momentum +21,9 %, alpha +4,9 %/an.

### DG.PA
- Canal 66,81 – 89,94 €, large de 23,1 %, clôture à 77,49 € à 46,2 % : le milieu.
- Support −0,027 contre résistance +0,100 €/séance : le canal s'ouvre, τ infini.
- Deux contacts en support : veto 1.
- Momentum +5,5 %, alpha −8,2 %/an.

### HO.PA
- Canal 77,82 – 114,53 €, clôture à 103,57 € à 70,2 % de la hauteur.
- Pentes +0,188 et +0,324 €/séance : ouverture, τ infini.
- Cinq contacts bas, trois hauts : **aucun veto** — figure lisible et tendances concordantes.
- Momentum +22,9 %, alpha −5,5 %/an.

### MT.AS
- Canal 23,03 – 28,78 €, clôture à 27,02 € à 69,4 %.
- Support +0,020 contre résistance −0,030 €/séance, τ de 115 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +21,1 %, alpha −3,5 %/an sur un IC95 de 76 points.

### SAN.PA
- Canal 69,14 – 78,14 €, clôture à 74,66 € à 61,4 % de la hauteur.
- Pentes +0,033 et +0,030 €/séance, presque identiques : τ de 4 229 séances.
- Deux contacts en support : veto 1 — les six épisodes de février n'ont pas tenu à la refonte de la fenêtre.
- Momentum +12,9 %, alpha +3,3 %/an.

### CS.PA
- Canal 15,27 – 20,00 €, clôture à 19,78 € à 95,4 % : sous le plafond.
- Deux droites descendantes, −0,020 et −0,047 €/séance, τ de 171 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +4,6 %, alpha −1,6 %/an.

### VIE.PA
- Canal 17,91 – 29,96 €, très large — 12,1 % —, clôture à 23,48 € à 46,2 % : le milieu.
- Support −0,031 contre résistance +0,051 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1.
- Momentum +23,5 %, alpha +5,5 %/an ; la tendance longue est retombée à zéro.

### VIV.PA
- Canal 9,17 – 11,09 €, clôture à 10,80 € à 85,1 % de la hauteur.
- Pentes −0,007 et −0,001 €/séance : ouverture lente, τ infini.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +1,9 %, alpha +6,3 %/an.

### AIR.PA
- Canal 81,51 – 109,77 €, clôture à 101,25 € à 69,9 %.
- Pentes −0,071 et −0,022 €/séance : ouverture vers le haut, τ infini.
- Deux contacts en support : veto 1.
- Momentum +11,5 %, alpha −10,2 %/an.

### ENGI.PA
- Canal 6,43 – 10,23 €, d'une largeur de 3,8 % — la figure s'est brutalement élargie —, clôture à 8,06 € à 43,0 %.
- Pentes −0,011 et +0,010 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1.
- Momentum +2,6 %, alpha −11,9 %/an.

### PUB.PA
- Canal 36,93 – 47,25 €, clôture à 44,76 € à 75,9 % de la hauteur.
- Pentes −0,075 et −0,197 €/séance, τ de 84 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +12,4 %, alpha −6,4 %/an.

### AI.PA
- Canal 93,14 – 110,51 €, clôture à 108,83 € à 90,4 % : contre la résistance.
- Support −0,036 contre résistance +0,015 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +7,2 %, sous le seuil de dix ; alpha +5,8 %/an.

### CAP.PA
- Canal 144,76 – 184,30 €, clôture à 182,32 € à 95,0 % de la hauteur.
- Deux droites descendantes, −0,171 et −0,225 €/séance, τ de 728 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +21,8 %, alpha +13,6 %/an.

### DSY.PA
- Canal 35,00 – 44,47 €, clôture à 43,10 € à 85,6 %.
- Pentes −0,075 et −0,114 €/séance, τ de 245 séances.
- Quatre contacts bas, cinq hauts : figure bien étayée ; seul le veto 3 mord.
- Momentum +15,3 %, alpha +15,2 %/an.

### EL.PA
- Canal 114,82 – 153,31 €, large de 38,5 %, clôture à 148,05 € à 86,4 % de la hauteur.
- Deux droites descendantes, −0,229 et −0,294 €/séance, τ de 587 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +10,2 %, alpha +0,4 %/an.

### RI.PA
- Canal 141,05 – 168,77 €, clôture à 166,35 € à 91,3 %.
- Pentes −0,158 et −0,205 €/séance, τ de 582 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +14,8 %, alpha +2,5 %/an.

### RMS.PA
- Canal 985,37 – 1 263,15 €, d'une largeur de 278 €, clôture à 1 237,29 € à 90,7 % de la hauteur.
- Pentes −1,773 et −4,447 €/séance, τ de 104 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +24,6 %, **alpha +18,9 %/an, IC95 de −1,9 à +39,8** — le plus proche de la significativité.

### SGO.PA
- Canal 37,53 – 62,20 €, clôture à 46,97 € à 38,2 %.
- Support −0,115 contre résistance +0,073 €/séance : ouverture franche, τ infini.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +4,3 %, alpha +3,4 %/an.

### STLAP.PA
- Canal 8,34 – 14,99 €, clôture à 10,79 € à 36,8 % de la hauteur.
- Support −0,029 contre résistance +0,017 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +3,9 %, alpha +36,0 %/an sur un IC95 de 128 points.

### STMPA.PA
- Canal 29,72 – 40,19 €, clôture à 37,96 € à 78,7 %.
- Pentes −0,040 et −0,059 €/séance, τ de 559 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +12,8 %, alpha +19,8 %/an.

### BNP.PA
- Canal 29,21 – 38,98 €, clôture à 37,39 € à 83,8 % de la hauteur.
- Pentes −0,101 et −0,287 €/séance, τ de 53 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum +1,5 %, alpha −7,1 %/an.

### ERF.PA
- Canal 69,28 – 87,13 €, clôture à 84,25 € à 83,9 %.
- Pentes −0,203 et −0,277 €/séance, τ de 241 séances.
- Trois contacts bas, quatre hauts : figure lisible ; veto 3 seul.
- Momentum +4,8 %, **alpha +26,5 %/an**, le plus élevé de la date.

### GLE.PA
- Canal 13,22 – 20,40 €, clôture à 19,57 € à 88,3 % de la hauteur.
- Pentes −0,080 et −0,278 €/séance, τ de 36 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +7,8 %, alpha −20,9 %/an.

### LR.PA
- Canal 68,67 – 80,42 €, clôture à 78,25 € à 81,6 %.
- Pentes −0,119 et −0,231 €/séance, τ de 106 séances.
- Quatre contacts bas, trois hauts : figure lisible ; veto 3.
- Momentum +4,4 %, alpha +5,3 %/an.

### MC.PA
- Canal 480,81 – 612,53 €, clôture à 591,97 € à 84,4 % de la hauteur.
- Pentes −0,833 et −1,480 €/séance, τ de 204 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +8,4 %, alpha +13,7 %/an.

### OR.PA
- Canal 291,06 – 345,14 €, clôture à 335,56 € à 82,3 %.
- Pentes −0,353 et −0,859 €/séance, τ de 107 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum +3,7 %, alpha +8,7 %/an.

### SU.PA
- Canal 107,90 – 141,51 €, clôture à 138,90 € à 92,2 % de la hauteur.
- Pentes −0,173 et −0,355 €/séance, τ de 184 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +4,9 %, alpha +14,8 %/an, IC95 de −3,3 à +32,8.

### TEP.PA
- Canal 241,50 – 295,42 €, clôture à 290,47 € à 90,8 %.
- Pentes −0,433 et −0,675 €/séance, τ de 223 séances.
- Quatre contacts bas, trois hauts : figure lisible ; veto 3 seul.
- Momentum +1,4 %, alpha +18,6 %/an.

### EN.PA
- Canal 21,80 – 25,76 €, clôture à 24,35 € à 64,4 % de la hauteur — un dixième sous le seuil haut.
- Pentes −0,009 et −0,018 €/séance, τ de 415 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −4,2 %, alpha −11,2 %/an.

### ACA.PA
- Canal 5,62 – 7,60 €, clôture à 7,36 € à 87,8 %.
- Pentes −0,025 et −0,058 €/séance, τ de 60 séances.
- Trois contacts de chaque côté : figure lisible ; seul le veto 3 mord.
- Momentum −8,8 %, alpha −10,4 %/an.

### BN.PA
- Canal 38,29 – 49,36 €, clôture à 42,31 € à 36,3 % de la hauteur.
- Support −0,060 contre résistance −0,000 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1.
- Momentum −8,3 %, alpha −11,1 %/an.

### ML.PA
- Canal 19,17 – 25,77 €, clôture à 25,08 € à 89,5 %.
- Pentes −0,063 et −0,162 €/séance, τ de 67 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum −3,0 %, alpha −1,7 %/an.

### RNO.PA
- Canal 15,83 – 33,28 €, d'une largeur de 17,4 %, clôture à 20,21 € à 25,1 % de la hauteur.
- Support −0,083 contre résistance +0,036 €/séance : ouverture franche, τ infini.
- Trois et quatre contacts : figure lisible ; veto 3.
- **Alpha significativement négatif** : −41,3 %/an, IC95 de −78,9 à −3,8. Momentum −26,8 %.

### SAF.PA
- Canal 85,91 – 109,25 €, clôture à 102,31 € à 70,2 %.
- Pentes −0,075 et −0,082 €/séance, presque parallèles : τ de 3 247 séances.
- Quatre contacts de chaque côté : figure bien étayée ; veto 3 seul.
- Momentum −6,7 %, alpha −17,6 %/an.

### ALO.PA
- Canal 13,51 – 21,76 €, clôture à 20,88 € à 89,3 % de la hauteur.
- Pentes −0,141 et −0,246 €/séance, τ de 79 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- **Momentum −52,2 %, le plus faible de tout l'univers sur l'année** ; alpha −20,6 %/an.

### WLN.PA
- Canal 359,32 – 449,61 €, clôture à 408,00 € à 53,9 % : le milieu.
- Pentes −1,219 et −2,322 €/séance, τ de 82 séances.
- Six contacts bas, trois hauts : **aucun veto** — la figure la mieux étayée de la date.
- Momentum −41,1 %, alpha −14,6 %/an.

### KER.PA
- **Évaluation impossible.** La règle sort en 2 : son contrôle de non-traversée de l'enveloppe convexe échoue, 88 séances passant du mauvais côté de la résistance.
- Aucun critère n'est publié, et le protocole traite le cas comme un veto : la valeur est exclue du classement, ne reçoit aucun rang, et ne peut ni être achetée ni décaler le rang d'une autre.
- Une figure qu'on ne sait pas calculer n'est pas une figure qu'on peut lire.

## 2022-04-29

### HO.PA
- Canal 109,00 – 123,74 €, clôture à 110,89 € à 12,8 % de la hauteur : contre le support.
- Support +0,788 contre résistance +0,409 €/séance, τ de 39 séances.
- Deux contacts en support : veto 1 — le seul défaut d'une figure par ailleurs franche.
- Momentum +32,9 %, le deuxième de la date ; alpha −3,0 %/an.

### CA.PA
- Canal 14,99 – 16,06 €, large de 1,1 %, clôture à 15,39 € à 37,2 %.
- Pentes +0,063 et +0,024 €/séance, τ de 27 séances : le canal se referme presque à la décision suivante.
- Deux contacts en support : veto 1.
- Momentum +17,9 %, alpha +5,9 %/an.

### AI.PA
- Canal 109,67 – 113,76 €, large de 4,1 %, clôture à 113,23 € à 87,0 % de la hauteur.
- Support +0,442 contre résistance +0,052 €/séance : **le canal se referme en 11 séances**, veto 2.
- Trois et quatre contacts : la figure est étayée mais elle disparaît avant la prochaine décision.
- Momentum +13,1 %, alpha +7,1 %/an.

### MT.AS
- Canal 24,60 – 28,60 €, clôture à 25,93 € à 33,3 % — sous le seuil de 35 %.
- Support +0,047 contre résistance −0,025 €/séance, τ de 56 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +9,7 %, à trois dixièmes du seuil de dix ; alpha −3,9 %/an.

### ORA.PA
- Canal 8,39 – 8,60 €, d'une largeur de 0,2 % — le plus mince de la date —, clôture à 8,54 € à 71,5 %.
- Pentes +0,025 et +0,004 €/séance : **le canal se referme en 10 séances**, veto 2.
- Quatre et trois contacts, mais une figure de 21 centimes de haut ne mesure rien.
- Momentum +10,3 %, alpha −8,3 %/an.

### CS.PA
- Canal 18,89 – 20,23 €, clôture à 18,95 € à 4,7 % : sur le support.
- Support +0,088 contre résistance −0,026 €/séance : **le canal se referme en 12 séances**, veto 2.
- Deux contacts de chaque côté : veto 1 également.
- Momentum +16,3 %, alpha −2,5 %/an ; la tendance longue est retombée à zéro.

### DG.PA
- Canal 66,30 – 80,49 €, clôture à 79,26 € à 91,4 % de la hauteur.
- Pentes −0,027 et −0,123 €/séance, τ de 147 séances.
- Deux contacts en support : veto 1.
- Momentum +1,3 %, alpha −7,0 %/an.

### SAN.PA
- Canal 69,37 – 87,56 €, large de 18,2 %, clôture à 81,66 € à 67,6 %.
- Support +0,022 contre résistance +0,123 €/séance : le canal s'ouvre, τ infini.
- Deux contacts de chaque côté : veto 1.
- Momentum +6,5 %, alpha +6,1 %/an.

### TTE.PA
- Canal 34,64 – 37,50 €, clôture à 37,05 € à 84,5 % de la hauteur.
- Pentes +0,039 et −0,059 €/séance, τ de 29 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +24,1 %, alpha −7,6 %/an.

### VIV.PA
- Canal 10,22 – 11,07 €, clôture à 10,22 € : **exactement sur le support**, 0,0 % de la hauteur.
- Support +0,025 contre résistance −0,001 €/séance, τ de 33 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +4,7 %, alpha +4,7 %/an.

### EL.PA
- Canal 142,19 – 154,69 €, clôture à 145,83 € à 29,1 %.
- Support +0,628 contre résistance −0,207 €/séance : **le canal se referme en 15 séances**, veto 2.
- Deux contacts de chaque côté : veto 1 également.
- Momentum +23,7 %, alpha +0,1 %/an.

### EN.PA
- Canal 21,63 – 26,07 €, clôture à 25,29 € à 82,4 % de la hauteur.
- Pentes −0,009 et +0,004 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1.
- Momentum −9,1 %, à neuf dixièmes du seuil de −10 % ; alpha −9,3 %/an.

### ERF.PA
- Canal 81,97 – 92,09 €, clôture à 83,14 € à 11,5 % : contre le support.
- Support +0,270 contre résistance −0,174 €/séance, τ de 23 séances.
- Deux contacts en support : veto 1.
- Momentum +14,6 %, **alpha +26,0 %/an**, le plus élevé de la date.

### AIR.PA
- Canal 94,20 – 100,94 €, clôture à 98,21 € à 59,5 % de la hauteur.
- Support +0,311 contre résistance −0,193 €/séance : **le canal se referme en 13 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum +15,4 %, alpha −10,4 %/an.

### RMS.PA
- Canal 1 122,22 – 1 215,69 €, clôture à 1 141,79 € à 20,9 %.
- Support +2,964 contre résistance −4,049 €/séance : **le canal se referme en 13 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum +23,6 %, alpha +16,4 %/an, IC95 de −4,5 à +37,3.

### STMPA.PA
- Canal 32,87 – 39,07 €, clôture à 34,26 € à 22,4 % de la hauteur.
- Support +0,066 contre résistance −0,059 €/séance, τ de 50 séances.
- Trois contacts de chaque côté : **aucun veto**.
- **Momentum +38,3 %, le plus fort de la date** ; alpha +16,8 %/an, mais les deux tendances sont négatives.

### SU.PA
- Canal 120,46 – 137,83 €, clôture à 125,70 € à 30,2 %.
- Support +0,256 contre résistance −0,317 €/séance, τ de 30 séances.
- Deux contacts en support : veto 1.
- Momentum +18,2 %, alpha +11,7 %/an.

### VIE.PA
- Canal 21,92 – 23,47 €, clôture à 22,52 € à 39,0 % de la hauteur.
- Support +0,093 contre résistance −0,066 €/séance : **le canal se referme en 10 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum +17,9 %, alpha +4,4 %/an.

### DSY.PA
- Canal 37,05 – 43,22 €, clôture à 41,00 € à 64,0 % — un point sous le seuil haut.
- Pentes +0,001 et −0,103 €/séance, τ de 60 séances.
- Quatre contacts bas, cinq hauts : **aucun veto**, la figure la mieux étayée de la date.
- Momentum +24,4 %, alpha +13,7 %/an.

### GLE.PA
- Canal 18,26 – 18,79 €, d'une largeur de 0,5 %, clôture à 18,53 € à 51,0 %.
- Support +0,097 contre résistance −0,210 €/séance : **le canal se referme en moins de deux séances**, τ = 1,7. Veto 2, le plus court de toute l'année.
- Trois contacts bas, deux hauts : veto 1 également. Une figure de 53 centimes de haut, périmée à l'écriture.
- Momentum +3,6 %, alpha −21,5 %/an.

### ML.PA
- Canal 23,43 – 24,92 €, clôture à 24,28 € à 57,3 % de la hauteur.
- Support +0,084 contre résistance −0,120 €/séance : **le canal se referme en 7 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum +4,1 %, alpha −2,3 %/an.

### PUB.PA
- Canal 34,22 – 47,39 €, large de 13,2 %, clôture à 46,64 € à 94,3 %.
- Pentes −0,110 et −0,125 €/séance, quasi parallèles : τ de 836 séances.
- Quatre contacts bas, trois hauts : figure lisible ; seul le veto 3 mord.
- Momentum +6,3 %, alpha −4,7 %/an.

### SGO.PA
- Canal 34,93 – 50,28 €, clôture à 48,75 € à 90,0 % de la hauteur.
- Pentes −0,126 et −0,106 €/séance : ouverture lente, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +5,8 %, alpha +4,8 %/an.

### TEP.PA
- Canal 228,74 – 295,09 €, large de 66,3 €, clôture à 290,26 € à 92,7 %.
- Pentes −0,559 et −0,521 €/séance : ouverture imperceptible, τ infini.
- Cinq contacts bas, trois hauts : **aucun veto**.
- Momentum +10,1 %, alpha +18,4 %/an.

### BNP.PA
- Canal 26,98 – 36,78 €, clôture à 35,79 € à 90,0 % de la hauteur.
- Pentes −0,109 et −0,227 €/séance, τ de 83 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +2,1 %, alpha −7,8 %/an.

### CAP.PA
- Canal 164,82 – 182,64 €, clôture à 176,55 € à 65,8 % : à peine au-dessus du seuil haut.
- Support +0,459 contre résistance −0,193 €/séance, τ de 27 séances.
- Deux contacts en support : veto 1.
- Momentum +31,9 %, alpha +12,6 %/an.

### LR.PA
- Canal 63,85 – 78,50 €, clôture à 76,78 € à 88,3 %.
- Pentes −0,181 et −0,200 €/séance, τ de 788 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum +5,8 %, alpha +4,8 %/an.

### MC.PA
- Canal 559,54 – 592,27 €, clôture à 571,21 € à 35,7 % de la hauteur.
- Support +1,722 contre résistance −1,349 €/séance : **le canal se referme en 11 séances**, veto 2.
- Deux contacts en support : veto 1 également, malgré six épisodes en résistance.
- Momentum +8,0 %, alpha +12,6 %/an.

### OR.PA
- Canal 311,98 – 334,47 €, clôture à 326,40 € à 64,2 %.
- Support +0,393 contre résistance −0,789 €/séance : **le canal se referme en 19 séances**, veto 2.
- Trois et quatre contacts : la figure est lisible, mais périmée avant la décision suivante.
- Momentum +4,8 %, alpha +7,9 %/an.

### RI.PA
- Canal 159,78 – 167,21 €, clôture à 164,97 € à 69,8 % de la hauteur.
- Support +0,446 contre résistance −0,176 €/séance : **le canal se referme en 12 séances**, veto 2.
- Trois contacts de chaque côté : la figure est étayée, la géométrie ne tient pas.
- Momentum +12,6 %, alpha +2,5 %/an.

### STLAP.PA
- Canal 9,55 – 10,51 €, large de 1,0 %, clôture à 10,24 € à 71,3 %.
- Support +0,019 contre résistance −0,051 €/séance : **le canal se referme en 14 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum +2,0 %, alpha +33,7 %/an sur un IC95 de 125 points.

### BN.PA
- Canal 37,15 – 48,99 €, clôture à 48,75 € à 97,9 % : contre le plafond.
- Pentes −0,060 et −0,005 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −10,0 %, exactement au seuil ; alpha −6,4 %/an.

### ENGI.PA
- Canal 5,65 – 8,40 €, clôture à 8,23 € à 93,8 % de la hauteur.
- Pentes −0,026 et −0,033 €/séance, τ de 422 séances.
- Quatre contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- **Momentum −0,4 %**, quasi nul ; alpha −10,7 %/an.

### SAF.PA
- Canal 97,20 – 104,09 €, clôture à 98,42 € à 17,7 %.
- Support +0,269 contre résistance −0,154 €/séance : **le canal se referme en 16 séances**, veto 2.
- Trois contacts de chaque côté : figure étayée, géométrie périmée.
- Momentum −12,1 %, alpha −17,9 %/an.

### ACA.PA
- Canal 5,07 – 7,08 €, clôture à 7,02 € à 96,9 % de la hauteur.
- Pentes −0,027 et −0,048 €/séance, τ de 98 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −9,8 %, alpha −11,2 %/an.

### ALO.PA
- Canal 19,88 – 21,17 €, large de 1,3 %, clôture à 20,73 € à 65,9 %.
- Support +0,103 contre résistance −0,187 €/séance : **le canal se referme en 4,5 séances**, veto 2.
- Quatre contacts bas, trois hauts : la figure est étayée et pourtant sans avenir.
- **Momentum −51,5 %**, le plus faible de la date ; alpha −20,1 %/an.

### RNO.PA
- Canal 18,07 – 20,32 €, clôture à 19,96 € à 83,9 % de la hauteur.
- Support +0,020 contre résistance −0,249 €/séance : **le canal se referme en 8 séances**, veto 2.
- Quatre et trois contacts : figure étayée, géométrie périmée.
- **Alpha significativement négatif** : −40,2 %/an, IC95 de −77,2 à −3,2. Momentum −27,2 %.

### WLN.PA
- Canal 333,00 – 400,92 €, clôture à 391,10 € à 85,5 %.
- Pentes −1,307 et −2,424 €/séance, τ de 61 séances.
- **Sept contacts en support et trois en résistance** — la figure la mieux étayée de la date, aucun veto.
- **Momentum −44,0 %**, alpha −15,1 %/an. Score −6, le plus bas de la date.

### KER.PA
- **Évaluation impossible pour le deuxième mois consécutif.** La règle sort en 2 : 108 séances passent du mauvais côté de la résistance, contre 88 en mars.
- Aucun critère n'est publié ; la valeur reste hors du classement et hors d'atteinte de tout ordre.
- Une position détenue sur cette valeur ne serait pas vendue pour autant : la règle n'ayant rien dit, elle ne commande rien.

## 2022-05-31

### SAN.PA
- Canal 82,47 – 87,85 €, clôture à 83,44 € à 18,1 % de la hauteur : le cinquième bas.
- Support +0,236 contre résistance +0,052 €/séance, τ de 29 séances.
- Deux contacts en résistance : veto 1.
- Momentum +16,8 %, alpha +6,6 %/an. Meilleur score de la date, et pourtant sous veto.

### AI.PA
- Canal 110,19 – 115,99 €, clôture à 113,55 € à 57,8 % : le milieu haut.
- Pentes +0,283 et +0,063 €/séance, τ de 26 séances.
- Deux contacts en support contre six en résistance : veto 1.
- Momentum +14,8 %, alpha +6,9 %/an.

### HO.PA
- Canal 105,03 – 149,26 €, large de 44,2 % — la figure la plus ouverte de la date —, clôture à 105,03 € : **exactement sur le support**, 0,0 %.
- Support +0,465 contre résistance +0,694 €/séance : le canal s'ouvre, τ infini.
- Quatre contacts bas, trois hauts : **aucun veto**.
- **Momentum +41,3 %, le plus fort de la date** ; alpha −4,5 %/an.

### CA.PA
- Canal 14,25 – 16,58 €, clôture à 14,52 € à 11,6 % de la hauteur.
- Pentes +0,027 et +0,024 €/séance, quasi parallèles : τ de 656 séances.
- Trois contacts bas, cinq hauts : figure lisible ; seul le veto 3 mord.
- Momentum +18,9 %, alpha +4,1 %/an.

### TTE.PA
- Canal 35,17 – 43,92 €, clôture à 43,62 € à 96,5 % : contre le plafond.
- Pentes +0,026 et +0,039 €/séance : ouverture, τ infini.
- Cinq contacts bas, quatre hauts : **aucun veto** — la figure la mieux étayée de la date.
- Momentum +25,1 %, alpha −2,8 %/an.

### ORA.PA
- Canal 8,04 – 9,04 €, clôture à 8,79 € à 74,5 % de la hauteur.
- Pentes +0,011 et +0,009 €/séance, τ de 472 séances.
- Cinq contacts bas, trois hauts : **aucun veto**.
- Momentum +15,5 %, alpha −7,1 %/an.

### CS.PA
- Canal 18,27 – 19,65 €, clôture à 18,67 € à 28,7 %.
- Support +0,045 contre résistance −0,026 €/séance : **le canal se referme en 19 séances**, veto 2.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3. **Les trois vetos non arithmétiques.**
- Momentum +12,1 %, alpha −2,9 %/an.

### CAP.PA
- Canal 158,20 – 178,40 €, clôture à 162,51 € à 21,3 % de la hauteur.
- Support +0,176 contre résistance −0,193 €/séance, τ de 55 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum +27,3 %, alpha +9,7 %/an ; la tendance longue est négative.

### EN.PA
- Canal 24,72 – 26,91 €, clôture à 26,20 € à 67,5 % : au-dessus du seuil haut.
- Pentes +0,047 et +0,016 €/séance, τ de 70 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −5,0 %, alpha −7,9 %/an.

### MT.AS
- Canal 23,22 – 28,95 €, clôture à 28,04 € à 84,1 % de la hauteur.
- Pentes +0,010 et −0,015 €/séance, τ de 222 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +2,9 %, alpha −1,6 %/an ; la tendance longue est retombée à zéro.

### RI.PA
- Canal 145,97 – 164,99 €, clôture à 152,32 € à 33,4 % — sous le seuil de 35 %.
- Support +0,039 contre résistance −0,160 €/séance, τ de 96 séances.
- Quatre contacts de chaque côté : **aucun veto**, figure bien étayée.
- Momentum +10,6 %, alpha −0,1 %/an, rigoureusement nul.

### BN.PA
- Canal 47,56 – 49,80 €, clôture à 47,95 € à 17,5 % de la hauteur.
- Support +0,151 contre résistance +0,004 €/séance : **le canal se referme en 15 séances**, veto 2.
- Deux contacts en résistance : veto 1 également.
- Momentum −2,6 %, alpha −6,7 %/an.

### EL.PA
- Canal 126,42 – 150,13 €, clôture à 135,87 € à 39,9 %.
- Support +0,127 contre résistance −0,207 €/séance, τ de 71 séances.
- Deux contacts en résistance : veto 1.
- Momentum +10,3 %, alpha −2,0 %/an.

### STMPA.PA
- Canal 31,38 – 36,65 €, clôture à 35,70 € à 82,0 % de la hauteur.
- Support +0,016 contre résistance −0,085 €/séance, τ de 52 séances.
- Trois contacts de chaque côté : figure lisible ; seul le veto 3 mord.
- Momentum +14,8 %, alpha +17,4 %/an.

### DG.PA
- Canal 74,66 – 79,17 €, clôture à 76,57 € à 42,3 % : le milieu.
- Support +0,125 contre résistance −0,103 €/séance : **le canal se referme en 20 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum −1,8 %, alpha −7,7 %/an.

### ERF.PA
- Canal 75,01 – 83,06 €, clôture à 81,36 € à 78,9 % de la hauteur.
- Support +0,043 contre résistance −0,327 €/séance, τ de 22 séances : le canal ne passera pas le mois.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum +3,2 %, **alpha +24,8 %/an**, le plus élevé de la date.

### PUB.PA
- Canal 40,09 – 45,56 €, clôture à 41,22 € à 20,6 %.
- Support +0,031 contre résistance −0,113 €/séance, τ de 38 séances.
- Deux contacts en support : veto 1.
- Momentum +4,7 %, alpha −8,3 %/an.

### SU.PA
- Canal 111,18 – 123,32 €, clôture à 120,53 € à 77,0 % de la hauteur.
- Support +0,003 contre résistance −0,516 €/séance, τ de 23 séances.
- Trois contacts de chaque côté : figure lisible ; veto 3 seul.
- Momentum +0,9 %, alpha +10,1 %/an.

### TEP.PA
- Canal 250,66 – 283,63 €, clôture à 261,46 € à 32,8 % — sous le seuil de 35 %.
- Support +0,031 contre résistance −0,521 €/séance, τ de 60 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum +6,4 %, alpha +14,7 %/an ; mais les deux tendances sont négatives.

### VIE.PA
- Canal 20,18 – 22,02 €, clôture à 21,02 € à 45,8 % de la hauteur.
- Support +0,029 contre résistance −0,066 €/séance : **le canal se referme en 19 séances**, veto 2.
- Trois contacts bas, cinq hauts : la figure est étayée, la géométrie ne tient pas.
- Momentum +8,9 %, alpha +2,0 %/an.

### VIV.PA
- Canal 9,42 – 11,05 €, clôture à 10,35 € à 57,3 % : le milieu.
- Pentes +0,002 et −0,001 €/séance, quasi plates : τ de 532 séances.
- Deux contacts en support : veto 1.
- Momentum +1,2 %, alpha +5,0 %/an.

### AIR.PA
- Canal 96,64 – 105,23 €, clôture à 101,23 € à 53,4 % de la hauteur.
- Support +0,235 contre résistance −0,073 €/séance, τ de 28 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −4,6 %, alpha −9,3 %/an.

### DSY.PA
- Canal 34,38 – 39,44 €, clôture à 37,94 € à 70,4 %.
- Pentes −0,039 et −0,143 €/séance, τ de 49 séances.
- Cinq contacts bas, quatre hauts : **aucun veto**, figure très bien étayée.
- Momentum +9,8 %, à deux dixièmes du seuil de dix ; alpha +10,9 %/an.

### ENGI.PA
- Canal 8,07 – 9,35 €, clôture à 9,08 € à 79,0 % de la hauteur.
- Support +0,025 contre résistance −0,008 €/séance, τ de 39 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum −1,6 %, alpha −7,5 %/an.

### ML.PA
- Canal 23,79 – 25,98 €, clôture à 25,69 € à 86,8 %.
- Support +0,059 contre résistance −0,071 €/séance : **le canal se referme en 17 séances**, veto 2.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3. **Les trois vetos.**
- Momentum −9,6 %, alpha −0,7 %/an.

### ACA.PA
- Canal 6,82 – 7,78 €, large de 0,9 %, clôture à 7,69 € à 91,3 % de la hauteur.
- Support +0,013 contre résistance −0,025 €/séance, τ de 26 séances.
- Cinq contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −15,6 %, alpha −8,2 %/an.

### ALO.PA
- Canal 20,50 – 25,76 €, clôture à 24,93 € à 84,2 %.
- Support +0,075 contre résistance −0,091 €/séance, τ de 32 séances.
- Quatre contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- **Momentum −53,6 %, le plus faible de toute l'année** ; alpha −13,9 %/an.

### BNP.PA
- Canal 36,68 – 42,23 €, clôture à 41,05 € à 78,7 % de la hauteur.
- Support +0,096 contre résistance −0,089 €/séance, τ de 30 séances.
- Quatre contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −10,8 %, alpha −3,6 %/an.

### GLE.PA
- Canal 18,51 – 21,82 €, clôture à 21,39 € à 86,8 %.
- Support +0,065 contre résistance −0,109 €/séance : **le canal se referme en 19 séances**, veto 2.
- Quatre contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3. **Les trois vetos.**
- Momentum −13,3 %, alpha −16,7 %/an.

### LR.PA
- Canal 69,22 – 75,86 €, clôture à 74,47 € à 79,1 % de la hauteur.
- Pentes −0,027 et −0,183 €/séance, τ de 43 séances.
- Cinq contacts bas, quatre hauts : **aucun veto**.
- Momentum −5,7 %, alpha +3,7 %/an.

### MC.PA
- Canal 495,59 – 567,25 €, clôture à 550,65 € à 76,8 %.
- Pentes −0,004 et −1,292 €/séance, τ de 56 séances.
- Trois contacts bas, six hauts : **aucun veto**.
- Momentum −7,0 %, alpha +11,1 %/an.

### OR.PA
- Canal 279,17 – 315,80 €, clôture à 307,37 € à 77,0 % de la hauteur.
- Pentes −0,309 et −0,823 €/séance, τ de 71 séances.
- Quatre contacts de chaque côté : **aucun veto**, figure bien étayée.
- Momentum −9,7 %, alpha +5,7 %/an.

### RMS.PA
- Canal 941,74 – 1 097,84 €, large de 156 €, clôture à 1 068,17 € à 81,0 %.
- Pentes −1,272 et −4,977 €/séance, τ de 42 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −2,7 %, alpha +13,9 %/an.

### SAF.PA
- Canal 87,57 – 100,71 €, clôture à 92,27 € à 35,7 % de la hauteur — à peine au-dessus du seuil bas.
- Pentes +0,005 et −0,154 €/séance, τ de 82 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −20,1 %, alpha −19,4 %/an.

### SGO.PA
- Canal 45,40 – 48,52 €, clôture à 47,69 € à 73,3 %.
- Support +0,098 contre résistance −0,100 €/séance : **le canal se referme en 16 séances**, veto 2.
- Quatre contacts de chaque côté : figure étayée, géométrie périmée.
- Momentum −1,9 %, alpha +4,0 %/an.

### STLAP.PA
- Canal 9,96 – 11,15 €, large de 1,2 %, clôture à 10,96 € à 84,0 % de la hauteur.
- Support +0,019 contre résistance −0,032 €/séance, τ de 24 séances.
- Cinq contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −21,0 %, alpha +34,6 %/an sur un IC95 de 122 points : la mesure ne porte rien.

### WLN.PA
- Canal 289,29 – 416,68 €, d'une largeur de 127 % — la plus étirée de la date —, clôture à 392,76 € à 81,2 %.
- Pentes −1,565 et −1,393 €/séance : ouverture, τ infini.
- Cinq contacts bas, trois hauts : figure lisible ; seul le veto 3 mord.
- **Momentum −51,0 %** ; alpha −14,7 %/an.

### KER.PA
- **La règle publie de nouveau des critères** après deux mois d'échec du contrôle de non-traversée.
- Canal 366,13 – 456,69 €, clôture à 455,71 € à 98,9 % : contre le plafond, au plus haut du canal.
- Pentes −1,598 et −2,016 €/séance, τ de 217 séances ; deux contacts en support contre sept en résistance : veto 1.
- Momentum −31,9 %, alpha −5,9 %/an. Score −5.

### RNO.PA
- Canal 18,12 – 21,86 €, clôture à 21,63 € à 93,9 % de la hauteur.
- Support +0,013 contre résistance −0,148 €/séance, τ de 23 séances.
- Six contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- **Alpha significativement négatif** : −36,8 %/an, IC95 de −73,1 à −0,5. Momentum −32,8 %.

## 2022-06-30

### ORA.PA
- Canal 8,21 – 9,24 €, clôture à 8,77 € à 54,6 % : le milieu.
- Pentes +0,009 et +0,009 €/séance, rigoureusement identiques : τ de 3 226 séances, le canal est parallèle.
- Deux contacts en support : veto 1.
- Momentum +26,7 %, alpha −5,4 %/an. Meilleur score de la date.

### SAN.PA
- Canal 79,21 – 88,98 €, clôture à 80,89 € à 17,1 % de la hauteur.
- Pentes +0,132 et +0,052 €/séance, τ de 122 séances.
- Deux contacts de chaque côté : veto 1 — les six épisodes du mois dernier n'ont pas survécu au décalage de la fenêtre.
- Momentum +18,6 %, alpha +6,8 %/an.

### CA.PA
- Canal 12,82 – 17,53 €, large de 4,7 %, clôture à 13,24 € à 8,9 % : contre le support.
- Support +0,003 contre résistance +0,032 €/séance : le canal s'ouvre, τ infini.
- Quatre contacts bas, six hauts : figure bien étayée ; seul le veto 3 mord.
- Momentum +18,0 %, alpha +2,9 %/an.

### TTE.PA
- Canal 38,07 – 45,76 €, clôture à 40,05 € à 25,7 % de la hauteur.
- Pentes +0,075 et +0,048 €/séance, τ de 280 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- **Momentum +51,5 %, le plus fort de la date** ; alpha −1,8 %/an.

### AI.PA
- Canal 97,73 – 119,24 €, large de 21,5 %, clôture à 98,27 € à **2,5 %** : sur le support.
- Support +0,050 contre résistance +0,088 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté : figure lisible ; veto 3 seul.
- Momentum +9,9 %, à un dixième du seuil de dix ; alpha +4,6 %/an.

### EN.PA
- Canal 23,65 – 27,25 €, clôture à 23,94 € à 8,1 % : contre le support.
- Pentes +0,021 et +0,016 €/séance, τ de 728 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +6,4 %, alpha −6,8 %/an.

### HO.PA
- Canal 104,21 – 109,51 €, clôture à 108,22 € à 75,6 % de la hauteur.
- Support +0,340 contre résistance −0,186 €/séance : **le canal se referme en 10 séances**, veto 2.
- Quatre contacts bas, six hauts : la figure est la mieux étayée de la date, et elle disparaît avant la décision suivante.
- Momentum +30,5 %, alpha −1,0 %/an.

### BNP.PA
- Canal 34,25 – 40,26 €, clôture à 35,06 € à 13,6 %.
- Pentes +0,040 et −0,089 €/séance, τ de 47 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +14,5 %, alpha −3,9 %/an.

### CAP.PA
- Canal 148,50 – 166,21 €, clôture à 149,14 € à **3,6 %** : quasiment sur le support.
- Support +0,008 contre résistance −0,333 €/séance, τ de 52 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +6,8 %, alpha +10,1 %/an.

### CS.PA
- Canal 16,93 – 19,07 €, clôture à 17,20 € à 12,4 % de la hauteur.
- Pentes +0,016 et −0,026 €/séance, τ de 50 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +14,9 %, alpha −1,9 %/an.

### ENGI.PA
- Canal 7,83 – 9,18 €, clôture à 7,97 € à 10,2 % : contre le support.
- Pentes +0,015 et −0,008 €/séance, τ de 59 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +15,7 %, alpha −8,3 %/an.

### MT.AS
- Canal 19,69 – 28,76 €, clôture à 20,13 € à 4,9 % de la hauteur.
- Pentes −0,032 et −0,014 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +14,4 %, alpha −5,7 %/an sur un IC95 de 73 points.

### STMPA.PA
- Canal 28,15 – 34,86 €, clôture à 28,82 € à 10,0 %.
- Pentes −0,028 et −0,084 €/séance, τ de 121 séances.
- Deux contacts en support : veto 1.
- Momentum +15,9 %, alpha +14,9 %/an.

### DG.PA
- Canal 70,94 – 76,91 €, clôture à 72,54 € à 26,8 % de la hauteur.
- Pentes +0,045 et −0,103 €/séance, τ de 40 séances.
- Trois contacts bas, cinq hauts : **aucun veto**.
- **Momentum +0,4 %**, quasi nul ; alpha −5,3 %/an.

### GLE.PA
- Canal 17,54 – 20,35 €, clôture à 17,87 € à 11,6 %.
- Pentes +0,035 et −0,100 €/séance, τ de 21 séances : le canal ne passera pas le mois.
- Deux contacts en support : veto 1.
- Momentum +8,1 %, alpha −16,4 %/an.

### VIE.PA
- Canal 18,13 – 20,76 €, clôture à 18,80 € à 25,5 % de la hauteur.
- Pentes −0,004 et −0,064 €/séance, τ de 44 séances.
- Trois contacts bas et **sept en résistance** — la figure la mieux étayée de la date, aucun veto.
- Momentum +3,6 %, alpha +1,5 %/an.

### BN.PA
- Canal 44,18 – 50,05 €, clôture à 46,66 € à 42,3 % : le milieu.
- Pentes +0,061 et +0,006 €/séance, τ de 106 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −4,7 %, alpha −5,7 %/an ; la tendance longue est retombée à zéro.

### RI.PA
- Canal 138,67 – 150,39 €, clôture à 146,31 € à 65,2 % — à deux dixièmes au-dessus du seuil haut.
- Pentes −0,063 et −0,424 €/séance, τ de 33 séances.
- Deux contacts de chaque côté : veto 1.
- **Momentum +0,4 %** ; alpha +0,5 %/an — les deux quasiment nuls.

### ACA.PA
- Canal 6,39 – 7,27 €, large de 0,9 %, clôture à 6,51 € à 13,3 % de la hauteur.
- Pentes +0,004 et −0,024 €/séance, τ de 31 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum −5,2 %, alpha −8,7 %/an.

### AIR.PA
- Canal 83,90 – 103,62 €, clôture à 86,03 € à 10,8 % : contre le support.
- Pentes +0,014 et −0,073 €/séance, τ de 227 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −2,6 %, alpha −8,9 %/an.

### ML.PA
- Canal 21,46 – 25,06 €, clôture à 22,01 € à 15,4 % de la hauteur.
- Pentes +0,014 et −0,064 €/séance, τ de 46 séances.
- Trois contacts bas, deux hauts : veto 1.
- Momentum −8,1 %, alpha −2,0 %/an.

### PUB.PA
- Canal 35,98 – 43,07 €, clôture à 37,80 € à 25,6 %.
- Pentes −0,028 et −0,113 €/séance, τ de 84 séances.
- Trois contacts bas, cinq hauts : **aucun veto**.
- Momentum −3,6 %, alpha −7,5 %/an.

### SGO.PA
- Canal 35,53 – 48,74 €, clôture à 36,48 € à 7,2 % : contre le support.
- Pentes −0,050 et −0,079 €/séance, τ de 455 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −5,3 %, alpha −0,1 %/an.

### STLAP.PA
- Canal 9,15 – 10,80 €, clôture à 9,27 € à 7,2 % de la hauteur.
- Pentes +0,004 et −0,029 €/séance, τ de 51 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −7,3 %, alpha +30,8 %/an sur un IC95 de 120 points.

### SU.PA
- Canal 102,11 – 115,19 €, clôture à 105,46 € à 25,6 %.
- Pentes −0,110 et −0,462 €/séance, τ de 37 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −4,7 %, alpha +9,2 %/an.

### VIV.PA
- Canal 8,86 – 10,51 €, clôture à 9,04 € à 11,0 % de la hauteur.
- Pentes −0,005 et −0,009 €/séance, quasi plates : τ de 429 séances.
- Deux contacts en support : veto 1.
- **Momentum −0,6 %**, quasi nul ; alpha +3,0 %/an.

### ALO.PA
- Canal 20,75 – 25,69 €, clôture à 21,19 € à 9,0 %.
- Support +0,058 contre résistance −0,074 €/séance, τ de 37 séances.
- Trois contacts bas, deux hauts : veto 1.
- **Momentum −32,1 %** ; alpha −15,5 %/an.

### DSY.PA
- Canal 31,49 – 36,29 €, clôture à 34,00 € à 52,2 % : le milieu.
- Pentes −0,061 et −0,143 €/séance, τ de 59 séances.
- Quatre contacts bas, cinq hauts : **aucun veto**.
- Momentum −8,5 %, alpha +9,4 %/an.

### EL.PA
- Canal 120,37 – 133,38 €, clôture à 129,39 € à 69,3 % de la hauteur.
- Support +0,018 contre résistance −0,451 €/séance, τ de 28 séances.
- Deux contacts en support : veto 1.
- Momentum −2,3 %, alpha −0,7 %/an.

### LR.PA
- Canal 61,79 – 73,38 €, clôture à 65,14 € à 28,9 %.
- Pentes −0,112 et −0,152 €/séance, τ de 288 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −11,7 %, alpha +2,5 %/an.

### MC.PA
- Canal 492,95 – 552,42 €, clôture à 536,36 € à 73,0 % de la hauteur.
- Pentes −0,035 et −1,161 €/séance, τ de 53 séances.
- Quatre contacts bas, six hauts : **aucun veto**, figure très bien étayée.
- Momentum −8,3 %, alpha +13,2 %/an.

### RNO.PA
- Canal 19,35 – 22,40 €, clôture à 20,14 € à 25,9 %.
- Pentes +0,040 et −0,107 €/séance, τ de 21 séances : le canal ne passera pas le mois.
- Cinq contacts bas, trois hauts : **aucun veto**.
- Momentum −21,8 %, alpha −32,7 %/an, IC95 de −69,0 à +3,6.

### WLN.PA
- Canal 322,89 – 400,81 €, clôture à 365,58 € à 54,8 % : le milieu.
- Pentes −0,492 et −1,227 €/séance, τ de 106 séances.
- Trois contacts de chaque côté : **aucun veto**.
- **Momentum −52,9 %, le plus faible de la date** ; alpha −13,0 %/an.

### ERF.PA
- Canal 65,17 – 76,17 €, clôture à 70,36 € à 47,2 % de la hauteur.
- Pentes −0,093 et −0,322 €/séance, τ de 48 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −16,1 %, **alpha +21,7 %/an**, le plus élevé de la date.

### OR.PA
- Canal 272,36 – 320,44 €, clôture à 308,07 € à 74,3 %.
- Pentes −0,309 et −0,444 €/séance, τ de 357 séances.
- Cinq contacts bas, trois hauts : **aucun veto**.
- Momentum −12,2 %, alpha +7,7 %/an.

### RMS.PA
- Canal 908,09 – 1 046,46 €, large de 138 €, clôture à 1 026,79 € à 85,8 % de la hauteur.
- Pentes −1,343 et −3,881 €/séance, τ de 55 séances.
- Quatre contacts bas, cinq hauts : **aucun veto**.
- Momentum −10,5 %, alpha +14,8 %/an.

### SAF.PA
- Canal 83,69 – 93,26 €, clôture à 90,31 € à 69,2 %.
- Pentes −0,044 et −0,235 €/séance, τ de 50 séances.
- Deux contacts en support : veto 1.
- Momentum −19,0 %, alpha −14,8 %/an.

### KER.PA
- Canal 330,98 – 454,09 €, large de 123 €, clôture à 438,18 € à 87,1 % de la hauteur.
- Pentes −1,598 et −1,567 €/séance, quasi parallèles : τ infini.
- Deux contacts en support contre cinq en résistance : veto 1.
- Momentum −28,7 %, alpha −3,6 %/an. Score −6, le plus bas de la date avec Teleperformance.

### TEP.PA
- Canal 228,42 – 249,07 €, clôture à 248,42 € à 96,9 % : contre le plafond, alors que tout le canal descend.
- Pentes −0,256 et −1,046 €/séance, τ de 26 séances.
- Deux contacts en support contre cinq en résistance : veto 1.
- Momentum −12,5 %, alpha +15,2 %/an.

## 2022-07-29

### HO.PA
- Canal 107,23 – 115,57 €, clôture à 112,19 € à 59,5 % de la hauteur.
- Support +0,302 contre résistance −0,050 €/séance, τ de 24 séances : le canal se referme presque à la décision suivante.
- Trois contacts bas, quatre hauts : **aucun veto**.
- **Momentum +36,9 %, le plus fort de la date** ; alpha −1,8 %/an.

### SAN.PA
- Canal 81,52 – 84,63 €, large de 3,1 %, clôture à 81,62 € à **3,2 %** : sur le support.
- Support +0,127 contre résistance −0,065 €/séance : **le canal se referme en 16 séances**, veto 2.
- **Six contacts en support et quatre en résistance** — la figure la mieux étayée de la date, et elle disparaît avant la décision suivante.
- Momentum +15,1 %, alpha +6,0 %/an.

### ORA.PA
- Canal 7,61 – 9,42 €, clôture à 7,81 € à 11,4 % de la hauteur.
- Support +0,001 contre résistance +0,009 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +26,0 %, alpha −9,3 %/an.

### TTE.PA
- Canal 36,79 – 39,73 €, clôture à 39,56 € à 94,5 % : contre le plafond.
- Support +0,033 contre résistance −0,148 €/séance : **le canal se referme en 16 séances**, veto 2.
- Deux contacts en résistance : veto 1 également.
- **Momentum +41,5 %**, le deuxième de la date ; alpha −4,3 %/an.

### BN.PA
- Canal 46,23 – 49,83 €, clôture à 47,15 € à 25,5 % de la hauteur.
- Pentes +0,086 et −0,003 €/séance, τ de 41 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −12,0 %, alpha −6,5 %/an.

### ALO.PA
- Canal 21,94 – 26,95 €, clôture à 22,95 € à 20,1 %.
- Pentes +0,058 et +0,004 €/séance, τ de 94 séances.
- Trois contacts de chaque côté : **aucun veto** — première figure propre d'Alstom depuis décembre.
- **Momentum −38,5 %**, le plus faible de la date ; alpha −15,0 %/an.

### CA.PA
- Canal 12,82 – 13,47 €, large de 0,7 %, clôture à 13,05 € à 35,0 % : exactement au seuil bas.
- Support +0,002 contre résistance −0,054 €/séance : **le canal se referme en 12 séances**, veto 2.
- Six contacts bas, trois hauts : figure étayée, géométrie périmée.
- Momentum +5,3 %, alpha +1,3 %/an.

### ENGI.PA
- Canal 7,47 – 8,99 €, clôture à 8,77 € à 85,6 % de la hauteur.
- Pentes +0,008 et −0,009 €/séance, τ de 90 séances.
- Deux contacts en support : veto 1.
- Momentum +1,2 %, alpha −7,5 %/an.

### AI.PA
- Canal 93,93 – 103,58 €, clôture à 102,87 € à 92,7 % : sous le plafond.
- Support +0,002 contre résistance −0,361 €/séance, τ de 27 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum −2,5 %, alpha +4,1 %/an.

### EN.PA
- Canal 22,42 – 24,18 €, clôture à 24,05 € à 93,0 % de la hauteur.
- Pentes +0,004 et −0,061 €/séance, τ de 27 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −7,0 %, alpha −9,0 %/an.

### VIV.PA
- Canal 8,43 – 9,35 €, clôture à 8,64 € à 22,1 %.
- Pentes −0,008 et −0,034 €/séance, τ de 36 séances.
- Trois contacts de chaque côté : figure lisible ; seul le veto 3 mord.
- Momentum −16,6 %, alpha +0,5 %/an.

### CS.PA
- Canal 16,26 – 17,94 €, clôture à 17,83 € à 93,4 % de la hauteur.
- Pentes +0,006 et −0,035 €/séance, τ de 41 séances.
- Trois contacts bas, quatre hauts : figure lisible ; veto 3.
- Momentum −2,8 %, alpha −3,3 %/an.

### DG.PA
- Canal 71,53 – 80,24 €, clôture à 79,72 € à 94,1 % : contre le plafond.
- Pentes +0,042 et −0,055 €/séance, τ de 91 séances.
- Trois contacts de chaque côté : figure lisible ; veto 3.
- Momentum −2,1 %, alpha −5,3 %/an.

### RI.PA
- Canal 137,35 – 163,20 €, clôture à 161,26 € à 92,5 % de la hauteur.
- Pentes −0,063 et −0,083 €/séance, quasi parallèles : τ de 1 292 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −5,4 %, alpha +1,9 %/an.

### AIR.PA
- Canal 82,73 – 99,20 €, clôture à 97,60 € à 90,3 %.
- Pentes −0,001 et −0,139 €/séance, τ de 119 séances.
- Quatre contacts bas, trois hauts : figure lisible ; veto 3 seul.
- Momentum −18,3 %, alpha −8,5 %/an.

### BNP.PA
- Canal 31,48 – 36,01 €, clôture à 35,55 € à 90,0 % de la hauteur.
- Pentes +0,004 et −0,144 €/séance, τ de 31 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −7,7 %, alpha −6,4 %/an.

### CAP.PA
- Canal 138,73 – 169,54 €, clôture à 169,13 € à 98,7 % : à quarante centimes du plafond.
- Pentes −0,089 et −0,200 €/séance, τ de 279 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −12,9 %, alpha +11,1 %/an.

### DSY.PA
- Canal 30,21 – 40,75 €, clôture à 40,34 € à 96,1 % de la hauteur.
- Pentes −0,061 et −0,051 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté : figure lisible ; veto 3.
- Momentum −26,5 %, alpha +12,3 %/an.

### EL.PA
- Canal 120,74 – 142,71 €, clôture à 138,04 € à 78,8 %.
- Support +0,018 contre résistance −0,186 €/séance, τ de 108 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −12,5 %, alpha −0,8 %/an.

### ERF.PA
- Canal 63,21 – 77,97 €, clôture à 72,20 € à 60,9 % de la hauteur.
- Pentes −0,093 et −0,210 €/séance, τ de 126 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −34,7 %, **alpha +20,9 %/an**, le plus élevé de la date.

### GLE.PA
- Canal 16,40 – 18,87 €, clôture à 18,68 € à 92,1 %.
- Pentes +0,017 et −0,095 €/séance, τ de 22 séances.
- Trois contacts de chaque côté : figure lisible ; veto 3.
- Momentum −19,0 %, alpha −18,4 %/an.

### KER.PA
- Canal 436,26 – 504,79 €, clôture à 497,91 € à 90,0 % de la hauteur.
- Support +0,899 contre résistance −0,834 €/séance, τ de 40 séances.
- Cinq contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −36,1 %, alpha −2,4 %/an.

### LR.PA
- Canal 59,44 – 74,84 €, clôture à 73,84 € à 93,5 %.
- Pentes −0,112 et −0,094 €/séance : ouverture, τ infini.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum −24,3 %, alpha +4,0 %/an.

### MC.PA
- Canal 492,21 – 627,09 €, large de 135 €, clôture à 622,39 € à 96,5 % de la hauteur.
- Pentes −0,035 et −0,228 €/séance, τ de 700 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum −15,3 %, alpha +14,7 %/an, IC95 de −4,3 à +33,7.

### ML.PA
- Canal 21,14 – 23,99 €, clôture à 23,02 € à 66,0 % — juste au-dessus du seuil haut.
- Pentes +0,008 et −0,062 €/séance, τ de 41 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −24,0 %, alpha −3,0 %/an.

### MT.AS
- Canal 18,63 – 22,52 €, clôture à 22,38 € à 96,5 % de la hauteur.
- Pentes −0,036 et −0,175 €/séance, τ de 28 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −26,1 %, alpha −6,3 %/an sur un IC95 de 72 points.

### OR.PA
- Canal 265,86 – 348,95 €, large de 83,1 %, clôture à 344,37 € à 94,5 %.
- Support −0,309 contre résistance +0,023 €/séance : ouverture, τ infini.
- Cinq contacts bas, trois hauts : figure bien étayée ; seul le veto 3 mord.
- Momentum −16,3 %, alpha +9,1 %/an.

### PUB.PA
- Canal 34,47 – 45,11 €, clôture à 44,33 € à 92,6 % de la hauteur.
- Pentes −0,037 et −0,076 €/séance, τ de 274 séances.
- Quatre contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −13,8 %, alpha −5,3 %/an.

### RMS.PA
- Canal 879,89 – 1 309,23 €, d'une largeur de 429 € — la figure la plus étirée de la date —, clôture à 1 283,73 € à 94,1 %.
- Support −1,343 contre résistance +0,547 €/séance : ouverture franche, τ infini.
- Trois contacts bas, quatre hauts : figure lisible ; veto 3.
- Momentum −19,5 %, alpha +18,8 %/an, IC95 de −2,0 à +39,6.

### RNO.PA
- Canal 19,32 – 24,86 €, clôture à 24,33 € à 90,5 % de la hauteur.
- Pentes +0,025 et −0,065 €/séance, τ de 62 séances.
- **Sept contacts en support** contre deux en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum −29,2 %, alpha −30,5 %/an.

### SAF.PA
- Canal 82,76 – 102,94 €, clôture à 102,55 € à 98,1 % : contre le plafond.
- Pentes −0,044 et −0,077 €/séance, τ de 613 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −14,0 %, alpha −14,2 %/an.

### SGO.PA
- Canal 33,92 – 40,80 €, clôture à 40,39 € à 93,9 % de la hauteur.
- Pentes −0,056 et −0,254 €/séance, τ de 35 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −34,1 %, alpha rigoureusement nul, −0,0 %/an.

### STLAP.PA
- Canal 8,77 – 11,00 €, clôture à 10,96 € à 98,2 % : à quatre centimes du plafond.
- Pentes −0,001 et −0,016 €/séance, τ de 148 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −29,1 %, alpha +33,0 %/an sur un IC95 de 117 points.

### STMPA.PA
- Canal 25,46 – 35,88 €, clôture à 35,48 € à 96,1 % de la hauteur.
- Pentes −0,049 et −0,051 €/séance, quasi parallèles : τ de 4 090 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −17,3 %, alpha +17,4 %/an.

### SU.PA
- Canal 99,80 – 127,13 €, clôture à 125,67 € à 94,7 %.
- Pentes −0,110 et −0,195 €/séance, τ de 322 séances.
- Trois contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −21,8 %, alpha +11,5 %/an.

### TEP.PA
- Canal 223,05 – 282,43 €, clôture à 276,37 € à 89,8 % de la hauteur.
- Pentes −0,256 et −0,195 €/séance : ouverture, τ infini.
- Trois contacts bas et **sept en résistance** : figure bien étayée ; seul le veto 3 mord.
- Momentum −17,5 %, alpha +16,3 %/an.

### VIE.PA
- Canal 18,04 – 20,64 €, clôture à 20,55 € à 96,4 % : contre le plafond.
- Pentes −0,004 et −0,053 €/séance, τ de 53 séances.
- Trois contacts bas, cinq hauts : figure lisible ; veto 3.
- Momentum −12,0 %, alpha +1,7 %/an.

### WLN.PA
- Canal 312,56 – 445,66 €, clôture à 444,32 € à 99,0 % : à un centime du plafond, en base rétro-ajustée.
- Pentes −0,492 et −0,585 €/séance, τ de 1 436 séances.
- Trois contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- **Momentum −55,3 %, le plus faible de toute l'année** ; alpha −9,8 %/an.

### ACA.PA
- Canal 6,03 – 6,73 €, d'une largeur de 0,7 %, clôture à 6,70 € à 94,6 % de la hauteur.
- Pentes −0,000 et −0,025 €/séance, τ de 29 séances.
- Trois contacts de chaque côté : **aucun veto** — figure lisible, tendances concordantes, et pourtant le score le plus bas de la date, −5.
- Momentum −21,6 %, alpha −10,7 %/an.

## 2022-08-31

### ENGI.PA
- Canal 8,62 – 9,60 €, clôture à 8,63 € à **0,3 % de la hauteur** : sur le support, au centime près.
- Support +0,033 contre résistance +0,003 €/séance, τ de 33 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +12,1 %, alpha −6,6 %/an. Meilleur score de la date, et sous veto.

### HO.PA
- Canal 109,47 – 118,75 €, clôture à 111,08 € à 17,4 %.
- Support +0,187 contre résistance −0,005 €/séance, τ de 48 séances.
- Deux contacts de chaque côté : veto 1 — les épisodes se sont raréfiés depuis juillet.
- **Momentum +53,9 %, le plus fort de la date** ; alpha −0,9 %/an.

### TTE.PA
- Canal 37,55 – 43,56 €, clôture à 40,30 € à 45,8 % : le milieu.
- Pentes +0,033 et −0,025 €/séance, τ de 103 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +38,7 %, alpha −2,2 %/an.

### RMS.PA
- Canal 1 229,36 – 1 374,75 €, clôture à 1 234,17 € à 3,3 % : sur le support.
- Support +6,203 contre résistance +1,033 €/séance : convergence rapide, τ de 28 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum +3,8 %, alpha +18,3 %/an, IC95 de −2,2 à +38,8 — le plus proche de la significativité.

### MC.PA
- Canal 597,03 – 656,58 €, clôture à 597,03 € : **exactement sur le support**, 0,0 %.
- Support +1,995 contre résistance +0,377 €/séance, τ de 37 séances.
- Trois contacts bas, quatre hauts : figure lisible ; seul le veto 3 mord.
- Momentum +4,8 %, alpha +14,5 %/an.

### RNO.PA
- Canal 22,97 – 26,79 €, clôture à 24,22 € à 32,7 % de la hauteur — sous le seuil bas.
- Pentes +0,115 et +0,044 €/séance, τ de 54 séances.
- Trois contacts bas, quatre hauts : figure lisible ; veto 3.
- Momentum +2,0 %, alpha −27,6 %/an, IC95 de −62,8 à +7,6.

### DG.PA
- Canal 77,42 – 81,75 €, clôture à 78,76 € à 31,0 %.
- Pentes +0,162 et +0,013 €/séance, τ de 29 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum +4,8 %, alpha −3,9 %/an ; la tendance longue est retombée à zéro.

### BN.PA
- Canal 45,25 – 49,77 €, clôture à 46,01 € à 16,7 % de la hauteur.
- Pentes +0,033 et −0,003 €/séance, τ de 127 séances.
- Quatre contacts bas, trois hauts : figure lisible ; seul le veto 3 mord.
- Momentum −6,9 %, alpha −6,3 %/an.

### RI.PA
- Canal 154,57 – 165,08 €, clôture à 154,57 € : **exactement sur le support**, 0,0 %.
- Support +0,310 contre résistance −0,046 €/séance, τ de 30 séances.
- Deux contacts en support : veto 1.
- Momentum +2,8 %, alpha +1,5 %/an.

### SAF.PA
- Canal 96,84 – 109,11 €, clôture à 97,68 € à 6,9 % : contre le support.
- Pentes +0,242 et +0,032 €/séance, τ de 58 séances.
- Quatre contacts de chaque côté : **aucun veto**, figure bien étayée.
- Momentum +2,7 %, alpha −13,3 %/an.

### ALO.PA
- Canal 20,11 – 25,06 €, clôture à 20,38 € à 5,5 % de la hauteur.
- Pentes +0,014 et −0,029 €/séance, τ de 115 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −28,2 %, alpha −16,6 %/an.

### SAN.PA
- Canal 62,92 – 83,14 €, large de 20,2 %, clôture à 69,00 € à 30,1 %.
- Pentes −0,090 et −0,065 €/séance : ouverture, τ infini.
- Trois contacts bas, cinq hauts : **aucun veto**.
- Momentum +21,1 %, alpha +2,2 %/an. La chute d'août a fait passer la tendance longue à −1.

### OR.PA
- Canal 317,14 – 349,48 €, clôture à 321,12 € à 12,3 % de la hauteur.
- Support +0,668 contre résistance +0,023 €/séance, τ de 50 séances.
- Deux contacts en support : veto 1.
- Momentum −7,2 %, alpha +7,9 %/an.

### ORA.PA
- Canal 7,53 – 8,00 €, d'une largeur de 0,5 %, clôture à 7,89 € à 76,7 %.
- Pentes −0,003 et −0,022 €/séance, τ de 25 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum +14,0 %, alpha −8,2 %/an.

### STLAP.PA
- Canal 10,50 – 11,95 €, clôture à 10,50 € : **exactement sur le support**, 0,0 %.
- Pentes +0,042 et +0,006 €/séance, τ de 40 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum −7,6 %, alpha +31,9 %/an sur un IC95 de 115 points.

### STMPA.PA
- Canal 33,37 – 37,18 €, clôture à 33,38 € à **0,1 %** : sur le support au centime.
- Support +0,172 contre résistance −0,029 €/séance : **le canal se referme en 19 séances**, veto 2.
- Deux contacts de chaque côté : veto 1 également.
- **Momentum +0,6 %**, quasi nul ; alpha +17,0 %/an.

### WLN.PA
- Canal 414,45 – 473,38 €, clôture à 442,15 € à 47,0 % : le milieu.
- Support +2,217 contre résistance +0,249 €/séance, τ de 30 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- **Momentum −39,3 %, le plus faible de la date** ; alpha −8,2 %/an. La tendance longue est repassée à +1.

### CA.PA
- Canal 12,32 – 13,41 €, clôture à 13,05 € à 66,7 % — juste au-dessus du seuil haut.
- Pentes −0,010 et −0,038 €/séance, τ de 38 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum +8,9 %, alpha +2,0 %/an.

### CS.PA
- Canal 15,13 – 19,67 €, clôture à 18,68 € à 78,2 % de la hauteur.
- Pentes −0,025 et −0,008 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1.
- Momentum +1,3 %, alpha −0,6 %/an.

### GLE.PA
- Canal 18,26 – 20,26 €, clôture à 18,89 € à 31,5 %.
- Pentes +0,061 et −0,030 €/séance, τ de 22 séances.
- Deux contacts en support : veto 1.
- Momentum −12,4 %, alpha −15,5 %/an.

### KER.PA
- Canal 449,72 – 508,63 €, clôture à 449,72 € : **exactement sur le support**, 0,0 %.
- Support +0,796 contre résistance −0,239 €/séance, τ de 57 séances.
- Cinq contacts bas, trois hauts : **aucun veto** — la figure la mieux étayée de la date.
- Momentum −20,2 %, alpha −3,7 %/an.

### AI.PA
- Canal 96,03 – 103,53 €, clôture à 96,03 € : **sur le support**, 0,0 % de la hauteur.
- Support +0,052 contre résistance −0,228 €/séance, τ de 27 séances.
- Deux contacts en résistance : veto 1.
- **Momentum −1,6 %** ; alpha +3,0 %/an.

### AIR.PA
- Canal 91,05 – 102,95 €, clôture à 91,10 € à 0,4 % : sur le support.
- Pentes +0,203 et −0,035 €/séance, τ de 50 séances.
- Deux contacts en support : veto 1.
- Momentum −9,5 %, alpha −8,2 %/an.

### BNP.PA
- Canal 34,98 – 38,69 €, clôture à 35,93 € à 25,5 % de la hauteur.
- Pentes +0,108 et −0,054 €/séance, τ de 23 séances.
- Deux contacts en support : veto 1.
- Momentum −4,7 %, alpha −4,2 %/an.

### CAP.PA
- Canal 157,86 – 174,61 €, clôture à 157,86 € : **sur le support**, 0,0 %.
- Support +0,427 contre résistance −0,108 €/séance, τ de 31 séances.
- Deux contacts en résistance : veto 1.
- **Momentum −0,8 %**, quasi nul ; alpha +10,2 %/an.

### EL.PA
- Canal 134,87 – 149,44 €, clôture à 135,14 € à 1,9 % : sur le support.
- Pentes +0,271 et −0,069 €/séance, τ de 43 séances.
- Deux contacts en résistance : veto 1.
- Momentum −7,2 %, alpha −0,2 %/an.

### EN.PA
- Canal 23,48 – 24,94 €, large de 1,5 %, clôture à 23,89 € à 28,0 % de la hauteur.
- Pentes +0,033 et −0,029 €/séance, τ de 24 séances.
- Deux contacts en résistance : veto 1.
- Momentum −14,7 %, alpha −7,5 %/an.

### PUB.PA
- Canal 41,34 – 44,13 €, clôture à 41,64 € à 10,6 %.
- Support +0,151 contre résistance −0,043 €/séance : **le canal se referme en 14 séances**, veto 2.
- Quatre contacts bas, six hauts : la figure est très bien étayée, et elle disparaît avant la décision suivante.
- Momentum −6,2 %, alpha −5,5 %/an.

### VIE.PA
- Canal 18,43 – 21,69 €, clôture à 18,78 € à 10,8 % de la hauteur.
- Pentes +0,005 et −0,024 €/séance, τ de 115 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum −7,8 %, alpha +0,6 %/an.

### ACA.PA
- Canal 6,73 – 7,52 €, large de 0,8 %, clôture à 6,85 € à 15,4 %.
- Pentes +0,021 et −0,004 €/séance, τ de 31 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −18,5 %, alpha −8,1 %/an.

### DSY.PA
- Canal 37,13 – 41,69 €, clôture à 37,35 € à 4,8 % : contre le support.
- Pentes +0,100 et −0,031 €/séance, τ de 35 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −14,4 %, alpha +10,8 %/an.

### ERF.PA
- Canal 64,70 – 73,13 €, clôture à 65,63 € à 11,0 % de la hauteur.
- Pentes −0,021 et −0,210 €/séance, τ de 44 séances.
- Deux contacts en support : veto 1.
- Momentum −38,8 %, **alpha +18,5 %/an**, le plus élevé de la date après Hermès.

### LR.PA
- Canal 66,16 – 74,83 €, clôture à 66,82 € à 7,6 % : contre le support.
- Pentes +0,078 et −0,064 €/séance, τ de 61 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum −16,3 %, alpha +2,3 %/an.

### ML.PA
- Canal 20,02 – 22,74 €, clôture à 20,60 € à 21,3 % de la hauteur.
- Pentes −0,024 et −0,056 €/séance, τ de 85 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −20,1 %, alpha −4,7 %/an.

### SGO.PA
- Canal 35,36 – 39,54 €, clôture à 35,95 € à 14,1 %.
- Pentes +0,011 et −0,176 €/séance, τ de 22 séances.
- Deux contacts en résistance : veto 1.
- Momentum −25,9 %, alpha −1,6 %/an.

### SU.PA
- Canal 110,74 – 127,27 €, clôture à 110,95 € à 1,2 % : sur le support.
- Pentes +0,195 et −0,150 €/séance, τ de 48 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum −11,2 %, alpha +9,2 %/an.

### TEP.PA
- Canal 236,75 – 278,02 €, clôture à 240,80 € à 9,8 % de la hauteur.
- Pentes +0,136 et −0,194 €/séance, τ de 125 séances.
- Deux contacts en support contre six en résistance : veto 1.
- Momentum −13,1 %, alpha +13,2 %/an.

### MT.AS
- Canal 21,13 – 22,81 €, large de 1,7 %, clôture à 22,23 € à 65,5 % — juste au-dessus du seuil haut.
- Support +0,047 contre résistance −0,103 €/séance : **le canal se referme en 11 séances**, veto 2.
- Quatre contacts de chaque côté : figure très étayée, géométrie périmée.
- Momentum −15,6 %, alpha −4,1 %/an. Score −6, le plus bas de la date.

### VIV.PA
- Canal 8,20 – 8,57 €, d'une largeur de 0,4 % — la figure la plus mince de la date —, clôture à 8,44 € à 66,9 %.
- Pentes −0,009 et −0,034 €/séance : **le canal se referme en 15 séances**, veto 2.
- Trois contacts bas, cinq hauts : la figure est étayée, mais trente-sept centimes de haut ne mesurent rien.
- Momentum −28,6 %, alpha +0,7 %/an. Score −6.

## 2022-09-30

### ENGI.PA
- Canal 8,55 – 9,79 €, clôture à 8,61 € à 4,8 % de la hauteur : sur le support.
- Support +0,020 contre résistance +0,004 €/séance, τ de 81 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +9,9 %, à un dixième du seuil de dix ; alpha −4,6 %/an. Meilleur score de la date.

### MC.PA
- Canal 550,78 – 672,45 €, large de 122 €, clôture à 562,82 € à 9,9 %.
- Pentes +0,756 et +0,622 €/séance, τ de 902 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +1,8 %, alpha +14,8 %/an.

### RMS.PA
- Canal 1 122,05 – 1 405,04 €, d'une largeur de 283 €, clôture à 1 171,14 € à 17,3 % de la hauteur.
- Pentes +2,639 et +1,285 €/séance, τ de 209 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum +2,6 %, **alpha +18,1 %/an**, le plus élevé de la date, IC95 de −2,3 à +38,4.

### HO.PA
- Canal 99,95 – 118,65 €, clôture à 104,47 € à 24,2 %.
- Pentes −0,019 et −0,005 €/séance : ouverture imperceptible, τ infini.
- Cinq contacts bas, deux hauts : veto 1.
- **Momentum +41,8 %, le plus fort de la date** ; alpha −0,8 %/an.

### TTE.PA
- Canal 37,28 – 43,01 €, clôture à 38,93 € à 28,8 % de la hauteur.
- Pentes +0,024 et −0,025 €/séance, τ de 116 séances.
- Deux contacts en résistance : veto 1.
- Momentum +18,5 %, alpha −0,8 %/an.

### CS.PA
- Canal 17,66 – 20,54 €, clôture à 17,84 € à 6,5 % : contre le support.
- Pentes +0,024 et +0,001 €/séance, τ de 127 séances.
- Deux contacts en résistance : veto 1.
- Momentum +3,0 %, alpha +0,5 %/an.

### DG.PA
- Canal 69,45 – 83,16 €, clôture à 71,01 € à 11,4 % de la hauteur.
- Support −0,017 contre résistance +0,023 €/séance : ouverture, τ infini.
- Cinq contacts bas, deux hauts : veto 1.
- Momentum +4,3 %, alpha −4,1 %/an.

### OR.PA
- Canal 299,57 – 334,08 €, clôture à 308,96 € à 27,2 %.
- Support +0,243 contre résistance −0,330 €/séance, τ de 60 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −3,6 %, alpha +8,2 %/an.

### RI.PA
- Canal 152,93 – 164,50 €, clôture à 159,03 € à 52,7 % : le milieu.
- Pentes +0,193 et −0,034 €/séance, τ de 51 séances.
- Deux contacts en support : veto 1.
- Momentum −5,1 %, alpha +3,4 %/an.

### RNO.PA
- Canal 22,88 – 28,33 €, clôture à 23,68 € à 14,7 % de la hauteur.
- Pentes +0,068 et +0,058 €/séance, τ de 571 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum −12,7 %, alpha −24,1 %/an, IC95 de −59,0 à +10,9.

### KER.PA
- Canal 399,07 – 517,72 €, large de 119 €, clôture à 409,98 € à 9,2 %.
- Pentes +0,120 et +0,220 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté : figure lisible ; seul le veto 3 mord.
- Momentum −20,7 %, alpha −3,8 %/an.

### ORA.PA
- Canal 7,21 – 7,85 €, clôture à 7,23 € à 2,5 % : sur le support.
- Pentes −0,005 et −0,017 €/séance, τ de 56 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +14,9 %, alpha −9,3 %/an.

### SAF.PA
- Canal 85,75 – 110,26 €, large de 24,5 %, clôture à 90,12 € à 17,8 % de la hauteur.
- Pentes +0,020 et +0,045 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −13,6 %, alpha −12,0 %/an.

### WLN.PA
- Canal 402,76 – 501,53 €, clôture à 420,35 € à 17,8 %.
- Pentes +1,117 et +0,896 €/séance, τ de 447 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- **Momentum −35,9 %**, le plus faible de la date ; alpha −7,1 %/an.

### AI.PA
- Canal 87,87 – 98,52 €, clôture à 90,17 € à 21,6 % de la hauteur.
- Pentes −0,096 et −0,228 €/séance, τ de 81 séances.
- Deux contacts en résistance : veto 1.
- **Momentum +0,0 %**, rigoureusement nul ; alpha +2,7 %/an.

### CA.PA
- Canal 10,83 – 12,99 €, clôture à 11,14 € à 14,6 %.
- Pentes −0,028 et −0,034 €/séance, τ de 350 séances.
- Deux contacts en support : veto 1.
- Momentum +9,1 %, alpha −1,3 %/an.

### EL.PA
- Canal 124,32 – 147,92 €, clôture à 127,09 € à 11,7 % de la hauteur.
- Pentes +0,054 et −0,069 €/séance, τ de 192 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −6,3 %, alpha −0,1 %/an.

### STMPA.PA
- Canal 30,05 – 38,27 €, clôture à 31,03 € à 11,9 %.
- Pentes +0,059 et +0,013 €/séance, τ de 180 séances.
- Deux contacts en support : veto 1.
- Momentum −4,3 %, alpha +17,4 %/an.

### ACA.PA
- Canal 6,10 – 7,42 €, clôture à 6,24 € à 10,5 % de la hauteur.
- Pentes +0,001 et −0,004 €/séance, quasi plates : τ de 249 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −22,3 %, alpha −7,7 %/an.

### DSY.PA
- Canal 33,05 – 42,20 €, clôture à 34,60 € à 16,9 %.
- Pentes +0,013 et +0,005 €/séance, τ de 1 154 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −14,1 %, alpha +9,9 %/an.

### GLE.PA
- Canal 17,18 – 21,03 €, clôture à 17,46 € à 7,3 % : contre le support.
- Pentes +0,017 et −0,013 €/séance, τ de 126 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −16,8 %, alpha −13,8 %/an.

### PUB.PA
- Canal 39,83 – 46,69 €, clôture à 41,76 € à 28,2 % de la hauteur.
- Pentes +0,074 et −0,012 €/séance, τ de 79 séances.
- Deux contacts en support : veto 1.
- Momentum −11,2 %, alpha −3,3 %/an.

### STLAP.PA
- Canal 9,49 – 12,16 €, clôture à 9,66 € à 6,5 % : contre le support.
- Pentes +0,011 et +0,009 €/séance, τ de 1 060 séances.
- Deux contacts en support : veto 1.
- Momentum −15,8 %, alpha +30,3 %/an sur un IC95 de 112 points.

### BN.PA
- Canal 41,44 – 49,71 €, clôture à 42,55 € à 13,5 % de la hauteur.
- Pentes −0,016 et −0,003 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1.
- Momentum −4,8 %, alpha −7,1 %/an.

### CAP.PA
- Canal 138,85 – 174,14 €, clôture à 151,01 € à 34,5 % — à un demi-point du seuil bas.
- Pentes −0,024 et −0,061 €/séance, τ de 938 séances.
- Deux contacts en support : veto 1.
- Momentum −1,6 %, alpha +10,8 %/an.

### AIR.PA
- Canal 80,71 – 102,17 €, clôture à 82,72 € à 9,4 % de la hauteur.
- Pentes −0,032 et −0,035 €/séance, quasi parallèles : τ de 7 058 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum −15,4 %, alpha −7,4 %/an.

### ALO.PA
- Canal 15,87 – 24,42 €, clôture à 16,60 € à 8,5 %.
- Pentes −0,028 et −0,029 €/séance, presque identiques : τ de 6 039 séances.
- Deux contacts de chaque côté : veto 1.
- **Momentum −33,5 %** ; alpha −19,9 %/an.

### BNP.PA
- Canal 32,53 – 38,96 €, clôture à 33,70 € à 18,2 % de la hauteur.
- Pentes +0,020 et −0,038 €/séance, τ de 111 séances.
- Deux contacts en support : veto 1.
- Momentum −13,9 %, alpha −3,0 %/an.

### EN.PA
- Canal 21,50 – 24,88 €, clôture à 21,89 € à 11,7 %.
- Pentes −0,014 et −0,022 €/séance, τ de 415 séances.
- Deux contacts en résistance : veto 1.
- Momentum −11,3 %, alpha −7,4 %/an.

### ERF.PA
- Canal 54,68 – 70,56 €, clôture à 58,05 € à 21,2 % de la hauteur.
- Pentes −0,153 et −0,169 €/séance, τ de 1 008 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −35,9 %, **alpha +15,9 %/an**.

### LR.PA
- Canal 59,53 – 73,86 €, clôture à 61,62 € à 14,6 %.
- Pentes −0,040 et −0,050 €/séance, τ de 1 337 séances.
- Deux contacts en support : veto 1.
- Momentum −18,0 %, alpha +1,8 %/an.

### ML.PA
- Canal 18,87 – 21,51 €, clôture à 19,62 € à 28,6 % de la hauteur.
- Pentes −0,034 et −0,056 €/séance, τ de 119 séances.
- **Six contacts en support** et trois en résistance : **aucun veto**, la figure la mieux étayée de la date.
- Momentum −23,6 %, alpha −3,8 %/an.

### SAN.PA
- Canal 64,72 – 66,44 €, d'une largeur de 1,7 %, clôture à 65,83 € à 64,4 % — un demi-point sous le seuil haut.
- Support +0,015 contre résistance −0,400 €/séance : **le canal se referme en 4 séances**, veto 2 — le plus court de la date.
- Deux contacts en support : veto 1 également.
- **Momentum −0,3 %**, quasi nul ; alpha +1,8 %/an.

### SU.PA
- Canal 103,84 – 125,84 €, clôture à 109,23 € à 24,5 % de la hauteur.
- Pentes +0,015 et −0,090 €/séance, τ de 209 séances.
- Deux contacts en résistance : veto 1.
- Momentum −13,0 %, alpha +10,7 %/an.

### TEP.PA
- Canal 210,72 – 273,75 €, large de 63,0 €, clôture à 220,98 € à 16,3 %.
- Pentes −0,267 et −0,194 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −15,0 %, alpha +12,1 %/an.

### VIE.PA
- Canal 15,84 – 21,19 €, clôture à 16,62 € à 14,5 % de la hauteur.
- Pentes −0,031 et −0,023 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1.
- Momentum −13,7 %, alpha −0,8 %/an.

### VIV.PA
- Canal 7,22 – 7,99 €, clôture à 7,44 € à 28,3 %.
- Pentes −0,020 et −0,032 €/séance, τ de 63 séances.
- Quatre contacts bas, six hauts : **aucun veto**.
- Momentum −18,7 %, alpha −1,5 %/an.

### MT.AS
- Canal 18,14 – 21,31 €, clôture à 19,34 € à 37,9 % de la hauteur.
- Pentes −0,018 et −0,094 €/séance, τ de 42 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −13,9 %, alpha −4,2 %/an. Score −5.

### SGO.PA
- Canal 31,29 – 36,09 €, clôture à 33,01 € à 35,9 % — à peine au-dessus du seuil bas.
- Pentes −0,058 et −0,171 €/séance, τ de 42 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum −32,2 %, alpha −1,4 %/an. Score −5, le plus bas de la date avec ArcelorMittal.

## 2022-10-31

### ENGI.PA
- Canal 8,40 – 9,64 €, clôture à 9,56 € à 93,3 % de la hauteur : sous le plafond.
- Pentes +0,013 et −0,003 €/séance, τ de 79 séances.
- Deux contacts de chaque côté : veto 1.
- **Momentum +0,2 %**, quasi nul ; alpha −3,9 %/an. Meilleur score de la date, et sous veto.

### HO.PA
- Canal 99,42 – 119,88 €, clôture à 118,94 € à 95,4 %.
- Support −0,025 contre résistance +0,016 €/séance : ouverture, τ infini.
- Cinq contacts bas, deux hauts : veto 1.
- **Momentum +38,6 %, le plus fort de la date** ; alpha +0,8 %/an.

### TTE.PA
- Canal 37,55 – 44,99 €, clôture à 44,44 € à 92,5 % de la hauteur.
- Pentes +0,015 et −0,001 €/séance, τ de 489 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum +17,4 %, alpha +0,3 %/an.

### CS.PA
- Canal 17,65 – 19,95 €, clôture à 19,85 € à 95,5 % : contre le plafond.
- Pentes +0,018 et −0,017 €/séance, τ de 67 séances.
- Quatre contacts bas, deux hauts : veto 1.
- Momentum −5,5 %, alpha +0,6 %/an.

### MC.PA
- Canal 556,75 – 610,01 €, clôture à 589,19 € à 60,9 % de la hauteur.
- Support +0,654 contre résistance −0,841 €/séance, τ de 36 séances.
- Trois contacts bas, deux hauts : veto 1.
- Momentum −12,3 %, alpha +13,1 %/an.

### RI.PA
- Canal 144,34 – 170,10 €, clôture à 149,64 € à 20,6 %.
- Pentes +0,057 et +0,077 €/séance : ouverture, τ infini.
- Quatre contacts bas, trois hauts : figure lisible ; seul le veto 3 mord.
- Momentum −6,4 %, alpha +0,4 %/an.

### RMS.PA
- Canal 1 177,46 – 1 319,46 €, clôture à 1 261,12 € à 58,9 % de la hauteur.
- Support +2,639 contre résistance −0,922 €/séance, τ de 40 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −15,0 %, **alpha +17,6 %/an**, le plus élevé de la date, IC95 de −2,7 à +37,9.

### RNO.PA
- Canal 24,30 – 28,34 €, clôture à 26,39 € à 51,5 % : le milieu.
- Pentes +0,068 et +0,038 €/séance, τ de 134 séances.
- Quatre contacts bas, cinq hauts : **aucun veto**.
- Momentum −16,9 %, alpha −24,4 %/an.

### EL.PA
- Canal 125,44 – 151,22 €, clôture à 145,20 € à 76,6 % de la hauteur.
- Pentes +0,054 et +0,017 €/séance, τ de 713 séances.
- Deux contacts en résistance : veto 1.
- Momentum −22,7 %, alpha +1,2 %/an.

### PUB.PA
- Canal 41,39 – 50,39 €, clôture à 48,46 € à 78,5 %.
- Pentes +0,074 et +0,039 €/séance, τ de 257 séances.
- Deux contacts en support : veto 1.
- Momentum −10,4 %, alpha −1,9 %/an.

### SAF.PA
- Canal 86,16 – 109,80 €, clôture à 108,06 € à 92,6 % de la hauteur.
- Pentes +0,020 et +0,019 €/séance, quasi identiques : **τ de 46 839 séances** — deux siècles, autant dire un canal parallèle.
- Deux contacts de chaque côté : veto 1.
- Momentum −21,7 %, alpha −10,6 %/an.

### WLN.PA
- Canal 426,23 – 472,68 €, clôture à 457,96 € à 68,3 %.
- Support +1,117 contre résistance −0,444 €/séance, τ de 30 séances.
- Deux contacts en support : veto 1.
- Momentum −18,7 %, alpha −7,3 %/an.

### DG.PA
- Canal 68,68 – 79,84 €, clôture à 79,55 € à 97,4 % de la hauteur : contre le plafond.
- Pentes −0,021 et −0,089 €/séance, τ de 166 séances.
- **Six contacts en support** contre deux en résistance : veto 1.
- Momentum −9,2 %, alpha −3,9 %/an.

### ORA.PA
- Canal 6,94 – 7,56 €, clôture à 7,53 € à 95,1 %.
- Pentes −0,010 et −0,016 €/séance, τ de 98 séances.
- Trois contacts de chaque côté : figure lisible ; seul le veto 3 mord.
- Momentum +2,6 %, alpha −9,1 %/an.

### STMPA.PA
- Canal 29,24 – 33,56 €, clôture à 30,41 € à 26,9 % de la hauteur.
- Pentes +0,035 et −0,073 €/séance, τ de 40 séances.
- Trois contacts bas, cinq hauts : **aucun veto**.
- Momentum −26,7 %, alpha +13,5 %/an ; les deux tendances sont retombées à zéro.

### OR.PA
- Canal 284,59 – 327,15 €, clôture à 297,59 € à 30,5 %.
- Pentes +0,036 et −0,330 €/séance, τ de 116 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum −19,2 %, alpha +5,3 %/an.

### STLAP.PA
- Canal 9,45 – 10,79 €, clôture à 10,74 € à 95,8 % de la hauteur.
- Pentes +0,008 et −0,021 €/séance, τ de 47 séances.
- Deux contacts en résistance : veto 1.
- Momentum −24,0 %, alpha +30,5 %/an sur un IC95 de 110 points.

### SU.PA
- Canal 104,17 – 124,62 €, clôture à 119,80 € à 76,5 %.
- Pentes +0,015 et −0,077 €/séance, τ de 221 séances.
- **Six contacts en support** contre deux en résistance : veto 1.
- Momentum −22,4 %, alpha +10,2 %/an.

### CA.PA
- Canal 10,25 – 12,83 €, clôture à 12,77 € à 97,6 % de la hauteur : contre le plafond.
- Pentes −0,028 et −0,029 €/séance, quasi identiques : τ de 1 761 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −7,5 %, alpha +1,1 %/an.

### SAN.PA
- Canal 65,03 – 73,94 €, clôture à 73,32 € à 93,1 %.
- Pentes +0,015 et −0,161 €/séance, τ de 51 séances.
- Trois contacts bas, quatre hauts : figure lisible ; veto 3 seul.
- Momentum −8,0 %, alpha +3,6 %/an.

### ACA.PA
- Canal 6,05 – 6,89 €, large de 0,8 %, clôture à 6,85 € à 95,1 % de la hauteur.
- Pentes +0,000 et −0,013 €/séance, τ de 61 séances.
- Trois contacts de chaque côté : figure lisible ; veto 3.
- **Momentum −29,6 %**, le deuxième plus faible de la date ; alpha −8,2 %/an.

### AI.PA
- Canal 85,85 – 102,83 €, clôture à 101,48 € à 92,0 %.
- Pentes −0,096 et −0,141 €/séance, τ de 373 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum −12,8 %, alpha +3,8 %/an.

### AIR.PA
- Canal 79,82 – 102,35 €, clôture à 101,97 € à 98,3 % : à trente-huit centimes du plafond.
- Pentes −0,035 et −0,027 €/séance : ouverture, τ infini.
- Quatre contacts de chaque côté : figure bien étayée ; seul le veto 3 mord.
- Momentum −22,5 %, alpha −5,5 %/an.

### ALO.PA
- Canal 14,38 – 21,00 €, clôture à 20,68 € à 95,2 % de la hauteur.
- Pentes −0,069 et −0,080 €/séance, τ de 627 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- **Momentum −47,0 %**, le plus faible de la date ; alpha −16,2 %/an.

### BN.PA
- Canal 40,59 – 44,25 €, clôture à 44,11 € à 95,9 %.
- Pentes −0,031 et −0,082 €/séance, τ de 71 séances.
- Trois contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −12,1 %, alpha −7,3 %/an.

### BNP.PA
- Canal 32,23 – 36,89 €, clôture à 36,71 € à 96,1 % de la hauteur.
- Pentes +0,011 et −0,075 €/séance, τ de 54 séances.
- Trois contacts de chaque côté : figure lisible ; veto 3 seul.
- Momentum −20,5 %, alpha −3,9 %/an.

### CAP.PA
- Canal 138,35 – 159,18 €, clôture à 151,70 € à 64,1 % — un point sous le seuil haut.
- Pentes −0,024 et −0,290 €/séance, τ de 78 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum −21,0 %, alpha +8,2 %/an.

### DSY.PA
- Canal 31,08 – 35,10 €, clôture à 32,87 € à 44,6 % : le milieu.
- Pentes −0,011 et −0,129 €/séance, τ de 34 séances.
- Deux contacts de chaque côté : veto 1.
- Momentum −34,5 %, alpha +6,6 %/an.

### EN.PA
- Canal 20,74 – 23,68 €, clôture à 23,55 € à 95,6 % de la hauteur.
- Pentes −0,020 et −0,044 €/séance, τ de 121 séances.
- Quatre contacts bas, deux hauts : veto 1 ; tendances opposées : veto 3.
- Momentum −14,8 %, alpha −7,9 %/an.

### ERF.PA
- Canal 51,46 – 62,65 €, clôture à 61,53 € à 90,0 %.
- Pentes −0,153 et −0,231 €/séance, τ de 145 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −39,7 %, **alpha +15,6 %/an**.

### GLE.PA
- Canal 16,98 – 20,75 €, clôture à 19,86 € à 76,6 % de la hauteur.
- Pentes +0,010 et −0,013 €/séance, τ de 163 séances.
- Trois contacts de chaque côté : figure lisible ; veto 3 seul.
- Momentum −26,0 %, alpha −13,9 %/an.

### LR.PA
- Canal 58,70 – 72,75 €, clôture à 71,31 € à 89,8 %.
- Pentes −0,040 et −0,051 €/séance, τ de 1 193 séances.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −28,1 %, alpha +3,3 %/an.

### ML.PA
- Canal 18,12 – 22,15 €, clôture à 21,87 € à 93,1 % de la hauteur.
- Pentes −0,034 et −0,039 €/séance, τ de 914 séances.
- **Six contacts en support** contre deux en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum −28,9 %, alpha −3,4 %/an.

### MT.AS
- Canal 17,77 – 21,81 €, clôture à 21,20 € à 84,9 %.
- Pentes −0,018 et −0,070 €/séance, τ de 78 séances.
- Trois contacts de chaque côté : figure lisible ; veto 3.
- Momentum −24,4 %, alpha −5,4 %/an.

### SGO.PA
- Canal 30,08 – 37,16 €, clôture à 36,89 € à 96,1 % de la hauteur.
- Pentes −0,058 et −0,125 €/séance, τ de 105 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −37,1 %, alpha −1,5 %/an.

### TEP.PA
- Canal 204,77 – 233,43 €, clôture à 229,79 € à 87,3 %.
- Pentes −0,271 et −0,779 €/séance, τ de 56 séances.
- Quatre contacts de chaque côté : figure bien étayée ; seul le veto 3 mord.
- Momentum −26,3 %, alpha +10,9 %/an.

### VIE.PA
- Canal 15,20 – 19,31 €, clôture à 19,05 € à 93,7 % de la hauteur.
- Pentes −0,031 et −0,048 €/séance, τ de 237 séances.
- Deux contacts de chaque côté : veto 1 ; tendances opposées : veto 3.
- Momentum −30,4 %, alpha +0,4 %/an.

### KER.PA
- Canal 380,86 – 423,83 €, clôture à 414,58 € à 78,5 %.
- Pentes −0,116 et −1,745 €/séance, τ de 26 séances.
- Deux contacts en support : veto 1.
- Momentum −31,3 %, alpha −6,1 %/an. Score −5.

### VIV.PA
- Canal 6,76 – 7,76 €, clôture à 7,73 € à 97,0 % de la hauteur : contre le plafond.
- Pentes −0,022 et −0,028 €/séance, τ de 164 séances.
- Quatre contacts de chaque côté : **aucun veto** — figure bien étayée, et pourtant le score le plus bas de la date, −5.
- Momentum −25,7 %, alpha −2,0 %/an.

## 2022-11-30

> Le rebond de novembre a resserré la plupart des encadrements : **treize valeurs
> déclenchent le veto 2** à cette date, contre deux ou trois les mois précédents.
> Une fenêtre de 120 séances qui vient de changer de régime produit des droites
> fortement montantes en support et presque plates en résistance, donc des canaux
> qui se croisent dans les jours qui suivent.

### CS.PA
- Canal 21,34 – 22,02 €, d'une largeur de 0,7 %, clôture à 21,45 € à 16,9 % de la hauteur.
- Support +0,104 contre résistance +0,027 €/séance : **le canal se referme en 9 séances**, veto 2.
- Trois contacts bas, quatre hauts : la figure est étayée, la géométrie ne passera pas la semaine.
- Momentum +5,9 %, alpha +1,0 %/an. Meilleur score de la date.

### ENGI.PA
- Canal 10,44 – 10,77 €, large de 0,3 %, clôture à 10,56 € à 34,2 % — juste sous le seuil bas.
- Support +0,065 contre résistance +0,016 €/séance : **le canal se referme en 7 séances**, veto 2.
- Trois contacts bas, cinq hauts : figure étayée, canal de 33 centimes de haut.
- Momentum +9,4 %, alpha −2,6 %/an.

### PUB.PA
- Canal 52,97 – 55,95 €, clôture à 53,29 € à 10,9 % de la hauteur.
- Support +0,300 contre résistance +0,123 €/séance : **le canal se referme en 17 séances**, veto 2.
- Quatre contacts bas, trois hauts : figure bien étayée, géométrie périmée.
- Momentum +4,6 %, alpha −1,0 %/an.

### AIR.PA
- Canal 100,74 – 108,97 €, clôture à 101,62 € à 10,7 % : contre le support.
- Support +0,482 contre résistance +0,074 €/séance, τ de 20 séances — au seuil exact du veto 2, qui ne se déclenche pas.
- Deux contacts en support : veto 1.
- Momentum +8,2 %, alpha −7,6 %/an.

### DG.PA
- Canal 68,21 – 84,08 €, clôture à 83,37 € à 95,5 % de la hauteur.
- Pentes −0,021 et +0,022 €/séance : ouverture, τ infini.
- **Cinq contacts de chaque côté** : **aucun veto**, la figure la mieux étayée de la date.
- Momentum +11,9 %, alpha −4,4 %/an.

### TTE.PA
- Canal 46,16 – 48,74 €, clôture à 48,64 € à 95,9 % : contre le plafond.
- Support +0,199 contre résistance +0,055 €/séance : **le canal se referme en 18 séances**, veto 2.
- Quatre contacts de chaque côté : figure très étayée, géométrie périmée.
- **Momentum +36,1 %, le deuxième de la date** ; alpha +1,1 %/an.

### RNO.PA
- Canal 25,39 – 30,13 €, clôture à 29,47 € à 86,0 % de la hauteur.
- Pentes +0,064 et +0,050 €/séance, τ de 347 séances.
- Quatre contacts bas, cinq hauts : **aucun veto**.
- Momentum +6,6 %, alpha −23,4 %/an.

### SAF.PA
- Canal 110,98 – 113,18 €, d'une largeur de 2,2 %, clôture à 112,56 € à 72,1 %.
- Support +0,561 contre résistance +0,058 €/séance : **le canal se referme en 4,4 séances**, veto 2 — le plus court de la date.
- Quatre contacts bas, trois hauts : figure étayée, canal évanescent.
- Momentum +7,6 %, alpha −11,4 %/an.

### GLE.PA
- Canal 20,33 – 21,83 €, clôture à 20,52 € à 12,4 % de la hauteur.
- Support +0,085 contre résistance +0,010 €/séance : **le canal se referme en 20 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum −14,2 %, alpha −15,1 %/an.

### ACA.PA
- Canal 7,13 – 7,31 €, d'une largeur de 0,2 % — la figure la plus mince de la date —, clôture à 7,17 € à 19,6 %.
- Support +0,032 contre résistance −0,003 €/séance : **le canal se referme en 5 séances**, veto 2.
- Deux contacts en support : veto 1 également. Dix-huit centimes de haut ne mesurent rien.
- Momentum −16,7 %, alpha −8,8 %/an.

### AI.PA
- Canal 106,02 – 109,12 €, clôture à 106,02 € : **exactement sur le support**, 0,0 % de la hauteur.
- Support +0,536 contre résistance +0,038 €/séance : **le canal se referme en 6 séances**, veto 2.
- Quatre contacts de chaque côté : figure très étayée, géométrie sans lendemain.
- Momentum −4,7 %, alpha +3,8 %/an.

### BNP.PA
- Canal 40,93 – 41,78 €, large de 0,8 %, clôture à 41,30 € à 43,6 % : le milieu.
- Support +0,256 contre résistance +0,028 €/séance : **le canal se referme en 3,7 séances**, veto 2.
- Deux contacts en support : veto 1 également.
- Momentum −10,6 %, alpha −2,8 %/an.

### HO.PA
- Canal 98,88 – 120,24 €, clôture à 112,93 € à 65,8 % — à peine au-dessus du seuil haut.
- Pentes −0,025 et +0,016 €/séance : ouverture, τ infini.
- Quatre contacts bas, deux hauts : veto 1.
- **Momentum +76,2 %, le plus fort de toute l'année** ; alpha −1,4 %/an.

### MC.PA
- Canal 571,14 – 679,83 €, clôture à 679,83 € : **exactement sur la résistance**, 100,0 %.
- Pentes +0,654 et +0,360 €/séance, τ de 370 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −7,9 %, alpha +14,8 %/an.

### STLAP.PA
- Canal 11,38 – 11,75 €, large de 0,4 %, clôture à 11,71 € à 90,6 % de la hauteur.
- Support +0,057 contre résistance −0,002 €/séance : **le canal se referme en 6 séances**, veto 2.
- Quatre contacts bas, trois hauts : figure étayée, canal de trente-sept centimes.
- Momentum −9,5 %, alpha +30,9 %/an sur un IC95 de 108 points.

### WLN.PA
- Canal 449,84 – 497,74 €, clôture à 464,47 € à 30,5 %.
- Support +1,108 contre résistance +0,167 €/séance, τ de 51 séances.
- Deux contacts en résistance : veto 1.
- Momentum −10,1 %, alpha −8,4 %/an. Premier score positif de Worldline depuis le début de l'année.

### EL.PA
- Canal 126,62 – 161,68 €, large de 35,0 %, clôture à 160,54 € à 96,8 % de la hauteur.
- Pentes +0,054 et +0,148 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1.
- Momentum −11,7 %, alpha +2,3 %/an.

### MT.AS
- Canal 17,38 – 24,78 €, clôture à 24,16 € à 91,6 %.
- Pentes −0,018 et +0,000 €/séance : ouverture, τ infini.
- Deux contacts en résistance : veto 1.
- Momentum −10,2 %, alpha −4,5 %/an.

### ORA.PA
- Canal 6,72 – 7,78 €, clôture à 7,64 € à 86,4 % de la hauteur.
- Pentes −0,010 et −0,011 €/séance, quasi identiques : τ de 1 119 séances.
- Deux contacts en résistance : veto 1 ; tendances opposées : veto 3.
- Momentum +13,3 %, alpha −9,3 %/an.

### RI.PA
- Canal 145,59 – 161,41 €, clôture à 161,28 € à 99,2 % : à treize centimes du plafond.
- Pentes +0,057 et −0,055 €/séance, τ de 142 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum −14,0 %, alpha +1,3 %/an.

### RMS.PA
- Canal 1 235,50 – 1 518,70 €, d'une largeur de 283 €, clôture à 1 484,37 € à 87,9 % de la hauteur.
- Pentes +2,639 et +2,085 €/séance, τ de 512 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum −14,7 %, **alpha +20,1 %/an, IC95 de −0,1 à +40,3** — à un dixième de point d'être significativement positif, le plus près de toute l'année.

### STMPA.PA
- Canal 29,85 – 36,50 €, clôture à 34,69 € à 72,9 %.
- Pentes +0,033 et −0,015 €/séance, τ de 139 séances.
- Quatre contacts bas, trois hauts : **aucun veto**.
- Momentum −25,3 %, alpha +14,5 %/an.

### SU.PA
- Canal 104,50 – 134,77 €, large de 30,3 %, clôture à 129,76 € à 83,4 % de la hauteur.
- Pentes +0,015 et +0,081 €/séance : ouverture, τ infini.
- Quatre contacts de chaque côté : **aucun veto**, figure bien étayée.
- Momentum −20,9 %, alpha +10,4 %/an.

### VIE.PA
- Canal 20,44 – 21,29 €, large de 0,8 %, clôture à 20,72 € à 33,7 % — sous le seuil bas.
- Support +0,131 contre résistance −0,009 €/séance : **le canal se referme en 6 séances**, veto 2.
- Deux contacts de chaque côté : veto 1 également.
- Momentum −22,4 %, alpha +1,0 %/an.

### BN.PA
- Canal 43,69 – 44,52 €, large de 0,8 %, clôture à 43,88 € à 22,7 % de la hauteur.
- Support +0,080 contre résistance −0,059 €/séance : **le canal se referme en 6 séances**, veto 2.
- **Sept contacts en support** contre deux en résistance : veto 1 ; tendances opposées : veto 3. **Les trois vetos à la fois.**
- Momentum −2,0 %, alpha −8,0 %/an.

### CA.PA
- Canal 12,78 – 13,04 €, d'une largeur de 0,3 %, clôture à 12,88 € à 38,0 %.
- Support +0,045 contre résistance −0,014 €/séance : **le canal se referme en 4,6 séances**, veto 2.
- Trois contacts de chaque côté : figure étayée, vingt-six centimes de haut.
- Momentum +9,8 %, alpha +0,5 %/an.

### CAP.PA
- Canal 137,84 – 165,68 €, clôture à 156,03 € à 65,3 % — trois dixièmes au-dessus du seuil haut.
- Pentes −0,024 et −0,131 €/séance, τ de 260 séances.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −18,4 %, alpha +7,2 %/an.

### EN.PA
- Canal 20,31 – 25,12 €, clôture à 24,10 € à 78,8 % de la hauteur.
- Pentes −0,020 et −0,003 €/séance : ouverture, τ infini.
- Trois contacts bas, cinq hauts : **aucun veto**.
- Momentum +1,9 %, alpha −8,7 %/an.

### KER.PA
- Canal 363,53 – 511,23 €, d'une largeur de 148 €, clôture à 507,30 € à 97,3 %.
- Support −0,551 contre résistance +0,006 €/séance : ouverture, τ infini.
- Cinq contacts bas, trois hauts : **aucun veto**.
- Momentum −31,3 %, alpha −2,6 %/an.

### LR.PA
- Canal 57,83 – 75,08 €, clôture à 71,63 € à 80,0 % de la hauteur.
- Pentes −0,040 et −0,008 €/séance : ouverture, τ infini.
- Deux contacts en support : veto 1.
- Momentum −21,6 %, alpha +2,0 %/an.

### OR.PA
- Canal 281,36 – 333,53 €, clôture à 331,92 € à 96,9 % : contre le plafond.
- Pentes +0,002 et −0,175 €/séance, τ de 294 séances.
- Trois contacts bas, quatre hauts : **aucun veto**.
- Momentum −23,1 %, alpha +6,9 %/an.

### SAN.PA
- Canal 65,35 – 74,77 €, clôture à 72,61 € à 77,0 % de la hauteur.
- Pentes +0,015 et −0,112 €/séance, τ de 75 séances.
- Trois contacts bas, **six en résistance** : **aucun veto**.
- Momentum +7,4 %, alpha +2,7 %/an.

### SGO.PA
- Canal 28,81 – 40,76 €, clôture à 38,98 € à 85,1 %.
- Pentes −0,058 et −0,024 €/séance : ouverture, τ infini.
- Trois contacts de chaque côté : **aucun veto**.
- Momentum −30,1 %, alpha −2,0 %/an.

### ML.PA
- Canal 22,32 – 22,87 €, d'une largeur de 0,6 %, clôture à 22,65 € à 60,0 % de la hauteur.
- Support +0,106 contre résistance −0,015 €/séance : **le canal se referme en 4,5 séances**, veto 2 ; tendances opposées : veto 3.
- Quatre contacts bas, trois hauts : figure étayée, cinquante-cinq centimes de haut.
- Momentum −25,8 %, alpha −3,9 %/an.

### ALO.PA
- Canal 12,62 – 25,58 €, d'une largeur de 13,0 %, clôture à 24,64 € à 92,8 %.
- Support −0,075 contre résistance +0,002 €/séance : ouverture franche, τ infini.
- Deux contacts en support : veto 1 ; tendances opposées : veto 3.
- Momentum −32,2 %, alpha −12,8 %/an.

### DSY.PA
- Canal 30,85 – 35,81 €, clôture à 33,97 € à 63,0 % de la hauteur.
- Pentes −0,011 et −0,082 €/séance, τ de 70 séances.
- Trois contacts de chaque côté : **aucun veto**.
- **Momentum −37,7 %** ; alpha +6,2 %/an.

### VIV.PA
- Canal 6,28 – 8,12 €, clôture à 8,00 € à 93,7 %.
- Pentes −0,022 et −0,018 €/séance : ouverture, τ infini.
- Quatre contacts bas, trois hauts : figure lisible ; seul le veto 3 mord.
- Momentum −24,4 %, alpha −2,1 %/an.

### ERF.PA
- Canal 48,09 – 67,50 €, large de 19,4 %, clôture à 63,08 € à 77,2 % de la hauteur.
- Pentes −0,153 et −0,124 €/séance : ouverture, τ infini.
- Deux contacts de chaque côté : veto 1.
- **Momentum −39,2 %** ; alpha +14,9 %/an. Score −5.

### TEP.PA
- Canal 126,49 – 219,51 €, d'une largeur de 93,0 % — la figure la plus étirée de la date, après l'effondrement d'octobre —, clôture à 182,44 € à 60,2 %.
- Pentes −0,900 et −0,741 €/séance : ouverture, τ infini.
- Deux contacts en support contre cinq en résistance : veto 1.
- Momentum −28,8 %, alpha +6,3 %/an. Score −5, le plus bas de la date avec Eurofins.
