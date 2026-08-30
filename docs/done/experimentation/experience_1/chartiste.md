# Les notes de perspective chartistes

Une note de cinq lignes au plus par societe, a chacune des douze dates de
decision. Redigees par l'agent `chartiste` du depot, sans aucune seance
posterieure a la date consideree.

Decoupe consommee par `journal.py --markdown` : titres `## AAAA-MM-JJ` puis
`### TICKER`.

---

## 2021-12-31
### AIR.PA
Tendance longue baissière et significative : pente −0,063 €/séance (−0,061 %/séance), R² = 0,27, p = 1,8·10⁻⁹, TEND_120 = −1 sur la fenêtre 19/07→31/12.
Tendance courte inverse : +0,522 €/séance (+0,530 %/séance), R² = 0,57, p = 1,3·10⁻⁴, soit +14,0 % en 20 séances — les deux échelles sont de signes opposés.
Encadrement convexe (120 séances) : support 86,02 € (pente −0,072, portée 94 séances, 2 épisodes : 19-20/07 et 26/11) ; résistance 104,34 € (pente −0,097, portée 35, 2 épisodes : 09-11/11 et 28-31/12).
Position 93,1 % d'un canal large de 18,32 € (17,8 %) : le cours revient buter sur la borne haute, mais 2 épisodes seulement de chaque côté — encadrement non confirmé ; volume du 31/12 à 0,24 fois sa moyenne 20 séances.
Observable ensuite : une clôture au-dessus de 104,3 €, tenue, retirerait la résistance descendante ; un retour sous VAL_120 = 98,74 € replacerait le cours du côté baissier de la droite longue.

### MC.PA
Tendance longue haussière et significative : +0,543 €/séance (+0,089 %/séance), R² = 0,33, p ≈ 10⁻¹¹, TEND_120 = +1.
Tendance courte de même signe : +1,075 €/séance (+0,165 %/séance), p = 6,3·10⁻³, R² = 0,35.
Support 605,29 € (pente +0,794, portée 40, 4 épisodes, dernier le 26/11) ; résistance 682,84 € (pente +0,324, portée 70, 3 épisodes : 12-13/08, 16-22/11, 25/11) — canal haussier légèrement convergent, τ = 165 séances.
Position 74,0 %, largeur 77,55 € (11,7 %), résidu +0,63 σ, aucune sortie de canal ; dispersion des 20 dernières séances 1,62 % contre 5,05 % sur les 100 précédentes, soit un resserrement marqué.
Observable ensuite : une clôture au-dessus du prolongement de la résistance (≈ 683 €) serait un franchissement datable ; sous 605 €, c'est un support à 4 épisodes qui tomberait.

### OR.PA
Tendance longue haussière : +0,264 €/séance (+0,072 %/séance), R² = 0,27, p = 1,5·10⁻⁹, TEND_120 = +1.
Tendance courte indiscernable du bruit : +0,114 €/séance, p = 0,43, IC₉₅ [−0,184 ; +0,412] change de signe, TEND_20 = 0.
Support 377,28 € (pente +0,931, portée 48, 3 épisodes : 11-13/10, 20/10, 20/12) ; résistance 406,86 € (pente +0,319, portée 70, 4 épisodes, dernier le 08/12) : canal fortement convergent, τ = 48 séances.
Position 24,5 %, largeur 29,59 € (7,7 %) : tiers bas d'un canal qui se referme ; dispersion 0,92 % sur 20 séances contre 4,56 % sur les 100 précédentes.
Observable ensuite : une clôture sous 377 € retirerait le support de 3 épisodes ; à défaut, la convergence elle-même annule l'encadrement en une cinquantaine de séances.

### SAN.PA
Tendance longue nulle au sens du test : +0,005 €/séance, R² = 0,006, p = 0,39, IC₉₅ [−0,006 ; +0,015] contient zéro, TEND_120 = 0.
Tendance courte franchement haussière : +0,201 €/séance (+0,286 %/séance), R² = 0,89, p = 5,9·10⁻¹⁰.
Support 68,16 € (pente +0,053, portée 33, 3 épisodes, dernier 03-10/12) ; résistance 72,24 € (pente −0,035, portée 31, 3 épisodes, dernier 28-31/12) — canal convergent, τ = 46 séances.
Position 81,7 % d'un canal étroit de 4,08 € (5,7 %) : la clôture de décision est elle-même le troisième contact de la borne haute.
Observable ensuite : une clôture au-dessus de 72,2 € invaliderait une résistance devenue crédible (3 épisodes) ; sous 68,2 €, c'est le support qui cède.

### BNP.PA
Tendance longue la plus régulière du panier avec RI.PA : +0,065 €/séance (+0,164 %/séance), R² = 0,75, p ≈ 10⁻³⁸.
Tendance courte de même signe : +0,170 €/séance (+0,404 %/séance), p = 1,1·10⁻⁴.
Support 39,99 € (pente +0,063, portée 51, 3 épisodes, dernier le 20/12) ; résistance 43,85 € (pente −0,035, portée 33, 2 épisodes seulement : 15-16/11 et 23-31/12) — borne haute non confirmée, canal convergent τ = 39 séances.
Position 97,7 %, largeur 3,86 € (8,8 %) : la clôture est sur la résistance, mais le volume du jour ne vaut que 0,16 fois sa moyenne 20 séances — le contact n'a aucune contrepartie de volume.
Observable ensuite : au-dessus de 43,9 €, la droite à 2 points cesse d'encadrer ; le support, s'il tient sa pente, passerait à 41,3 € dans 20 séances.

### TTE.PA
Tendance longue haussière et très explicative : +0,067 €/séance (+0,216 %/séance), R² = 0,79, p ≈ 10⁻⁴¹.
Tendance courte de même signe : +0,055 €/séance (+0,161 %/séance), p = 1,1·10⁻³.
Support 31,84 € (pente +0,056, portée 57, 5 épisodes, dernier 26-30/11) ; résistance 34,72 € quasi horizontale (pente +0,006, portée 50, 6 épisodes, dernier 22-31/12) : onze épisodes au total, structure installée des deux côtés.
Position 75,3 %, largeur 2,88 € (8,5 %), canal convergent τ = 57 séances ; dispersion 1,38 % sur 20 séances contre 8,26 % sur les 100 précédentes.
Observable ensuite : la résistance étant plate à ≈ 34,7 €, une clôture au-dessus tenue plus d'une séance serait le premier franchissement depuis octobre ; sous 31,8 €, un support à 5 épisodes cède.

### SU.PA
Tendance longue haussière : +0,180 €/séance (+0,129 %/séance), R² = 0,51, p ≈ 10⁻²⁰.
Tendance courte plus rapide encore : +0,432 €/séance (+0,282 %/séance), R² = 0,64, p = 2,1·10⁻⁵.
Support 145,28 € (pente +0,360, portée 33, 3 épisodes, dernier 26-30/11) ; résistance 159,17 € (pente +0,179, portée 94, 4 épisodes, dernier 23-31/12) — canal haussier convergent, τ = 77 séances.
Position 87,5 %, largeur 13,89 € (8,8 %), résidu +1,26 σ : haut de canal, au plus haut de 120 séances (158,63 € le 28/12).
Observable ensuite : le support monte de 0,36 €/séance, exigeant ; toute clôture sous ≈ 145,3 € l'invaliderait, toute clôture au-dessus de 159,2 € franchirait une résistance à 4 épisodes.

### AI.PA
Tendance longue significative mais peu explicative : +0,022 €/séance (+0,022 %/séance), R² = 0,06, p = 5,4·10⁻³.
Tendance courte muette : −0,056 €/séance, p = 0,32, IC₉₅ [−0,170 ; +0,059] à cheval sur zéro, TEND_20 = 0.
Support 102,46 € (pente +0,155, portée 51, 4 épisodes, dernier le 22/12) ; résistance 108,49 € (pente +0,041, portée 69, 5 épisodes, dernier 14-16/12) : neuf épisodes, encadrement installé mais très serré.
Position 42,1 %, largeur 6,04 € (5,7 %) — le canal le plus étroit du panier — et convergent, τ = 53 séances.
Observable ensuite : le support gagne 0,155 €/séance et rejoindrait le cours actuel en une dizaine de séances sans hausse ; les deux niveaux à surveiller sont 102,5 € et 108,5 €.

### DG.PA
Tendance longue rigoureusement absente : −0,0007 €/séance, R² = 0,000, p = 0,90, TEND_120 = 0.
Tendance courte nettement haussière : +0,304 €/séance (+0,414 %/séance), R² = 0,64, p = 2,6·10⁻⁵, soit +8,9 % en 20 séances.
Support 68,85 € (pente −0,012, portée 51, 3 épisodes, dernier le 30/11) ; résistance 77,43 € (pente −0,060, portée 32, 4 épisodes : 05-08/11, 11/11, 17/11 et 31/12).
Position 100,0 % : la clôture du 31/12 est exactement sur la résistance descendante, dont elle constitue le quatrième épisode ; largeur 8,58 € (11,1 %), résidu +1,41 σ.
Observable ensuite : la résistance perd 0,06 €/séance ; une clôture au-dessus de 77,4 € la ferait tomber, un repli la reconduirait en butée pour la cinquième fois.

### CAP.PA
Tendance longue haussière et bien établie : +0,261 €/séance (+0,149 %/séance), R² = 0,60, p ≈ 10⁻²⁵.
Tendance courte de même signe : +0,655 €/séance (+0,349 %/séance), R² = 0,67, p = 9,4·10⁻⁶.
Support 184,72 € (pente +0,517, portée 49, 4 épisodes, dernier 17-21/12) ; résistance 206,95 € (pente +0,323, portée 76, 3 épisodes, dernier 15-22/11) — canal haussier convergent, τ = 114 séances.
Position 41,8 %, largeur 22,23 € (11,5 %) : milieu de canal, bien que le plus haut de 120 séances (197,26 €) date du 28/12.
Observable ensuite : le support progresse de 0,52 €/séance, soit ≈ 195 € dans 20 séances ; c'est le passage sous cette droite qui invaliderait un support à 4 épisodes.

### RI.PA
Tendance longue la plus linéaire du panier : +0,264 €/séance (+0,162 %/séance), R² = 0,875, p ≈ 10⁻⁵⁵, σ des résidus 2,1 % du niveau.
Tendance courte haussière mais fragile : +0,094 €/séance, p = 0,029, IC₉₅ [+0,011 ; +0,178] frôle zéro.
Support 173,94 € (pente +0,325, portée 86, 7 épisodes, dont 20-21/12, 27/12 et 31/12) ; résistance 186,12 € (pente +0,271, portée 78, 2 épisodes seulement) : support installé, résistance non confirmée.
Position 21,2 %, largeur 12,18 € (6,9 %) : le cours clôture sur son support, dont il forme le septième épisode le jour même.
Observable ensuite : le support monte de 0,32 €/séance ; une clôture sous ≈ 174 € romprait la seule droite réellement documentée de la valeur.

### ORA.PA
Tendance longue non distinguable du bruit : +0,0006 €/séance, R² = 0,02, p = 0,096, IC₉₅ [−0,0001 ; +0,0012] contient zéro, TEND_120 = 0.
Tendance courte haussière et très linéaire : +0,024 €/séance (+0,340 %/séance), R² = 0,87, p = 2,1·10⁻⁹.
Support 6,64 € (pente −0,0005, portée 91, 3 épisodes : 29/07, 03/12, 10/12) ; résistance 7,33 € (pente +0,0012, portée 67, 2 épisodes) : canal quasi horizontal et divergent (τ = ∞), largeur 0,69 € (9,7 %).
Position 66,8 % ; le cours sort d'un creux à 6,65 € le 03/12, marqué à −2,4 σ du canal de régression, sans persistance.
Observable ensuite : la borne haute ne repose que sur 2 points, donc non confirmée ; seule une clôture au-dessus de 7,33 € ou sous 6,64 € trancherait l'alternative.

## 2022-01-31
### AIR.PA
Tendance longue baissière mais marginale : −0,025 €/séance (−0,024 %/séance), R² = 0,04, p = 0,034, IC₉₅ [−0,047 ; −0,002] frôle zéro.
Tendance courte franchement baissière : −0,447 €/séance (−0,422 %/séance), R² = 0,67, p = 1,1·10⁻⁵, soit −3,5 % en 20 séances après le plus haut du 05/01 à 111,10 €.
Support 98,35 € (pente +0,229, portée 42, 5 épisodes, dernier 24-25/01) ; résistance 111,61 € (pente +0,028, portée 72, 4 épisodes, dernier 05-06/01).
Position 34,0 %, largeur 13,26 € (12,9 %), canal convergent τ = 66 séances ; volume du jour 1,09 fois sa moyenne 20 séances, aucune sortie de canal.
Observable ensuite : le support monte de 0,23 €/séance quand la pente courte vaut −0,45 €/séance ; au rythme constaté les deux se croisent en quelques séances, et une clôture sous ≈ 98,5 € invaliderait un support à 5 épisodes.

### MC.PA
Tendance longue haussière et solide : +0,794 €/séance (+0,129 %/séance), R² = 0,62, p ≈ 10⁻²⁶.
Tendance courte baissière : −1,922 €/séance (−0,300 %/séance), R² = 0,26, p = 0,023 — les deux échelles divergent.
Support 605,60 € (pente +0,604, portée 82, 6 épisodes, dernier 24-27/01) ; résistance 701,42 € (pente +0,555, portée 33, 4 épisodes, dernier 05/01) : canal quasi parallèle, τ = 1 958 séances.
Position 55,4 %, largeur 95,81 € (14,5 %) ; repli des 24-25/01 jusqu'à −2,6 σ du canal de régression, volume 1,45 fois la moyenne, mais rebond immédiat et zéro séance dehors à la date.
Observable ensuite : le cours est revenu au milieu du canal ; une clôture sous 606 € romprait le support le mieux documenté du panier ce mois-ci (6 épisodes).

### OR.PA
Tendance longue encore positive mais portée par le début de fenêtre : +0,158 €/séance, R² = 0,08, p = 1,5·10⁻³.
Tendance courte très marquée : −2,714 €/séance (−0,758 %/séance), R² = 0,80, p = 1,0·10⁻⁷, soit −11,5 % en 20 séances.
Support 333,59 € (pente +0,123, portée 77, 3 épisodes, dernier 24-28/01) ; résistance 418,45 € (pente +0,413, portée 66, 4 épisodes, dernier 08/12) : canal divergent, τ = ∞.
Position 16,4 %, largeur 84,86 € soit 24,4 % du cours contre 7,7 % un mois plus tôt — élargissement d'un facteur trois ; résidu −1,45 σ, volume 1,82 fois la moyenne 20 séances.
Observable ensuite : un canal à 24 % de largeur n'encadre plus rien ; le seul événement datable serait une clôture sous 334 €, qui retirerait le support à 3 épisodes.

### SAN.PA
Tendance longue redevenue haussière : +0,037 €/séance (+0,052 %/séance), R² = 0,25, p = 5,1·10⁻⁹, TEND_120 = +1.
Tendance courte de même signe : +0,223 €/séance (+0,305 %/séance), R² = 0,62, p = 4,2·10⁻⁵.
Support 71,77 € (pente +0,114, portée 37, 5 épisodes, dernier 24-25/01) ; résistance 76,83 € (pente +0,029, portée 114, 2 épisodes seulement : 19-23/08 et 27-28/01) — borne haute non confirmée.
Position 61,0 %, largeur 5,06 € (6,8 %), canal convergent τ = 59 séances ; plus haut de 120 séances à 76,80 € le 28/01, c'est-à-dire sur la résistance.
Observable ensuite : une clôture au-dessus de 76,8 € retirerait une droite qui ne tient qu'à deux points distants de cinq mois ; sous 71,8 €, c'est un support à 5 épisodes qui tombe.

### BNP.PA
Tendance longue haussière et très explicative : +0,076 €/séance (+0,183 %/séance), R² = 0,77, p ≈ 10⁻³⁹.
Tendance courte éteinte sans se retourner : −0,062 €/séance, p = 0,19, IC₉₅ [−0,156 ; +0,033] contient zéro, TEND_20 = 0.
Support 41,31 € (pente +0,063, portée 51, 3 épisodes, dernier 17-20/12) ; résistance 49,10 € (pente +0,074, portée 43, 2 épisodes : 15-16/11 et 13-18/01), canal divergent.
Position 52,0 %, largeur 7,79 € soit 17,2 % du cours contre 8,8 % un mois plus tôt : la largeur a doublé, milieu de canal par élargissement plus que par mouvement.
Observable ensuite : la butée réelle est le plus haut du 17/01 à 48,35 € ; côté bas, seule une clôture sous 41,3 € invaliderait le côté à 3 épisodes.

### TTE.PA
Tendance longue haussière et très explicative : +0,082 €/séance (+0,251 %/séance), R² = 0,80, p ≈ 10⁻⁴³.
Tendance courte de même signe et plus rapide : +0,220 €/séance (+0,581 %/séance), R² = 0,71, p = 3,7·10⁻⁶, soit +11,6 % en 20 séances.
Support 33,02 € (pente +0,056, portée 57, 4 épisodes, dernier 26/11-02/12) ; résistance 40,76 € (pente +0,087, portée 72, 3 épisodes, dernier 26-28/01) : canal divergent, largeur 7,75 € (19,9 %) contre 8,5 % au 31/12.
Position 75,1 % : le cours est 17,6 % au-dessus de son support et 4,7 % sous sa résistance, avec un plus haut de 120 séances à 40,59 € le 27/01.
Observable ensuite : l'élargissement rend le support inopérant à court terme ; le seul niveau testable est la résistance à ≈ 40,8 €, appuyée sur 3 épisodes dont deux de janvier.

### SU.PA
Tendance longue encore positive : +0,146 €/séance (+0,103 %/séance), R² = 0,34, p ≈ 10⁻¹².
Tendance courte très marquée en sens inverse : −1,338 €/séance (−0,910 %/séance), R² = 0,89, p = 6,5·10⁻¹⁰, soit −14,7 % en 20 séances.
Support 132,30 € (pente +0,100, portée 78, 2 épisodes : 11-13/10 et 27-28/01, donc non confirmé) ; résistance 167,30 € (pente +0,216, portée 99, 3 épisodes, dernier 03-05/01).
Position 11,6 %, largeur 35,00 € soit 25,7 % contre 8,8 % un mois plus tôt ; sortie du canal de régression à −2,04 σ, 2 séances consécutives dehors (28 et 31/01), volume 1,18 fois la moyenne.
Observable ensuite : deux séances dehors à peine au-delà de 2 σ, sans volume marquant, ne qualifient pas une rupture ; une troisième clôture consécutive dehors, ou une clôture sous 132,3 €, la qualifierait.

### AI.PA
Tendance longue haussière : +0,054 €/séance (+0,053 %/séance), R² = 0,28, p = 8,0·10⁻¹⁰.
Tendance courte baissière et nette : −0,249 €/séance (−0,235 %/séance), R² = 0,69, p = 5,3·10⁻⁶.
Support 102,61 € (pente +0,116, portée 78, 3 épisodes, dernier 28-31/01) ; résistance 110,54 € (pente +0,052, portée 89, 4 épisodes, dernier 05-06/01) ; canal convergent, τ = 124 séances.
Position 13,4 %, largeur 7,93 € (7,7 %) : la clôture est à 1,0 % au-dessus du support, dont elle forme le troisième épisode — la droite vient d'atteindre le seuil de crédibilité.
Observable ensuite : le contact est frais ; une clôture sous 102,6 € invaliderait un support à peine confirmé et laisserait la valeur sans borne basse sur la fenêtre.

### DG.PA
Tendance longue haussière modeste : +0,034 €/séance (+0,045 %/séance), R² = 0,17, p = 3,3·10⁻⁶.
Tendance courte de même signe mais imprécise : +0,131 €/séance (+0,163 %/séance), p = 9,9·10⁻³, IC₉₅ [+0,036 ; +0,227].
Support 79,54 € (pente +0,325, portée 30, 2 épisodes seulement : 20/12 et 25-31/01) ; résistance 83,09 € (pente +0,050, portée 98, 3 épisodes, dernier 14-20/01).
Position 28,4 %, mais largeur réduite à 3,54 € (4,4 %) et canal convergent en τ = 12,9 séances : un support à +0,32 €/séance sous une résistance à +0,05 €/séance ne peut pas durer.
Observable ensuite : l'encadrement s'annule de lui-même en une quinzaine de séances ; les deux issues datables sont le franchissement de 83,1 € ou la perte d'un support qui n'a que 2 épisodes.

### CAP.PA
Tendance longue haussière : +0,170 €/séance (+0,095 %/séance), R² = 0,34, p ≈ 10⁻¹².
Tendance courte baissière : −0,709 €/séance (−0,393 %/séance), R² = 0,43, p = 1,8·10⁻³, soit −7,5 % en 20 séances.
Support 169,32 € (pente +0,185, portée 77, 3 épisodes, dernier 24-28/01) ; résistance 198,84 € (pente +0,031, portée 32, 3 épisodes, dernier 04/01).
Position 28,6 %, largeur 29,52 € (16,6 %) contre 11,5 % un mois plus tôt ; un seul dépassement au-delà de 2 σ (25/01, −2,16 σ), non persistant.
Observable ensuite : le support, à 169,3 € et montant de 0,18 €/séance, est le niveau dont la rupture serait datable ; le plus haut du 04/01 à 198,25 € borne le haut de la fenêtre.

### RI.PA
Tendance longue encore haussière mais dégradée : +0,195 €/séance (+0,118 %/séance), R² = 0,54 contre 0,875 un mois plus tôt, p ≈ 10⁻²¹.
Tendance courte très baissière : −0,978 €/séance (−0,587 %/séance), R² = 0,84, p = 1,2·10⁻⁸, soit −10,1 % en 20 séances.
Support 157,29 € (pente +0,122, portée 115, 3 épisodes, dernier 25-31/01) ; résistance 196,78 € (pente +0,363, portée 64, 3 épisodes, dernier 25/11) : canal divergent, largeur 39,49 € (25,0 %) contre 6,9 % au 31/12.
Rupture qualifiée : le résidu atteint −3,00 σ, avec 6 séances consécutives au-delà de −2 σ (24/01→31/01) et un volume à 1,62 fois la moyenne 20 séances — la sortie la mieux documentée du panier à cette date ; position 1,2 %.
Observable ensuite : le canal de régression 120 est rompu par le bas ; ce qui reste vérifiable séance par séance, c'est le maintien ou non de la clôture au-dessus de 157,3 €.

### ORA.PA
Tendance longue devenue significative : +0,0040 €/séance (+0,056 %/séance), R² = 0,33, p ≈ 10⁻¹², TEND_120 = +1.
Tendance courte très linéaire : +0,038 €/séance (+0,512 %/séance), R² = 0,91, p = 7,6·10⁻¹¹, soit +10,6 % en 20 séances.
Support 6,60 € (pente −0,0013, portée 53, 5 épisodes, dernier 09-10/12) ; résistance 7,95 € (pente +0,0064, portée 115, 2 épisodes : 20-23/08 et 27-31/01) — borne haute non confirmée.
Position 93,3 % : sortie par le haut du canal de régression à +2,90 σ, persistante sur 3 séances (27, 28 et 31/01), avec un plus haut de 120 séances à 7,95 € le jour même — mais un volume à 1,00 fois seulement sa moyenne 20 séances.
Observable ensuite : rupture haussière persistante et sans volume ; un retour sous ≈ 7,8 €, borne haute du canal de régression, la refermerait.

## 2022-02-28
### AIR.PA
Tendance longue éteinte : +0,013 €/séance, R² = 0,01, p = 0,26, IC₉₅ [−0,010 ; +0,037] à cheval sur zéro, TEND_120 = 0.
Tendance courte muette également : −0,004 €/séance, p = 0,97, TEND_20 = 0 — aucune direction mesurable aux deux échelles.
Support 97,28 € (pente +0,143, portée 64, 2 épisodes : 26-30/11 et 24/02) ; résistance 110,27 € (pente −0,022, portée 31, 2 épisodes : 05-06/01 et 16-17/02) : encadrement non confirmé des deux côtés.
Position 62,6 %, largeur 12,99 € (12,3 %), résidu +0,39 σ, aucune sortie de canal ; volume du 28/02 à 2,03 fois sa moyenne 20 séances, le plus fort ratio du panier, sans rupture associée.
Observable ensuite : le point bas du 24/02 est le premier contact du support depuis novembre ; une clôture sous 97,3 € ou au-dessus de 110,3 € retirerait l'une des deux droites à 2 points.

### MC.PA
Tendance longue encore haussière : +0,515 €/séance (+0,082 %/séance), R² = 0,31, p ≈ 10⁻¹¹.
Tendance courte fortement baissière : −3,573 €/séance (−0,568 %/séance), R² = 0,84, p = 1,5·10⁻⁸, soit −8,7 % en 20 séances.
Support 570,09 € (pente +0,179, portée 113, 4 épisodes, dernier 24/02) ; résistance 712,52 € (pente +0,555, portée 33, 3 épisodes, dernier 05/01) : canal divergent, largeur 142,43 € (23,7 %) contre 14,5 % un mois plus tôt.
Position 22,1 % ; sortie du canal de régression le 24/02 à −2,82 σ puis le 28/02 à −2,04 σ, volume 1,46 fois la moyenne, mais une seule séance consécutive dehors à la date.
Observable ensuite : la persistance manque pour parler de rupture installée ; le maintien de la clôture au-dessus de 570 €, support à 4 épisodes, est ce qui se vérifie séance par séance.

### OR.PA
Tendance longue disparue en un mois : −0,073 €/séance, R² = 0,01, p = 0,23, IC₉₅ [−0,193 ; +0,046] contient zéro, TEND_120 = 0.
Tendance courte baissière et nette : −1,556 €/séance (−0,468 %/séance), R² = 0,80, p = 1,3·10⁻⁷.
Support 302,84 € (pente −0,197, portée 104, 4 épisodes, dernier 24/02) ; résistance 328,69 € (pente −1,804 soit −0,551 %/séance, portée 38, 5 épisodes, dernier 25-28/02) : canal convergent, τ = 16,1 séances.
Position 95,0 %, largeur 25,85 € (7,9 %) : le cours clôture collé sous une résistance qui perd 1,80 € par séance, après un plus bas de 120 séances à 303,23 € le 24/02.
Observable ensuite : à cette pente la résistance recule d'environ 9 € par semaine ; ou bien elle est franchie dans les jours qui suivent, ou bien elle rejoint le support et l'encadrement cesse d'exister avant vingt séances.

### SAN.PA
Tendance longue haussière et très propre : +0,075 €/séance (+0,105 %/séance), R² = 0,75, p ≈ 10⁻³⁷, σ des résidus 2,1 % du niveau.
Tendance courte indéterminée : +0,036 €/séance, p = 0,32, IC₉₅ [−0,039 ; +0,111] contient zéro, TEND_20 = 0.
Support 71,71 € (pente +0,076, portée 45, 6 épisodes, dernier 24/02) ; résistance 77,96 € (pente +0,055, portée 61, 4 épisodes, dernier 09/02) : dix épisodes, l'encadrement le mieux installé du panier.
Position 59,7 %, largeur 6,25 € (8,3 %), canal presque parallèle (τ = 303 séances) ; résidu +0,11 σ et aucune clôture hors canal sur les 120 séances.
Observable ensuite : c'est la seule valeur dont les deux droites sont confirmées et de pentes voisines ; une clôture hors de l'intervalle 71,7 €–78,0 € serait un événement inédit sur la fenêtre.

### BNP.PA
Tendance longue encore mesurée haussière : +0,059 €/séance (+0,137 %/séance), R² = 0,52, p ≈ 10⁻²⁰ — mais la fin de fenêtre la contredit frontalement.
Tendance courte fortement baissière : −0,372 €/séance (−0,831 %/séance), R² = 0,65, p = 1,7·10⁻⁵, soit −16,7 % en 20 séances.
Support 37,12 € (pente +0,016, portée 115, 2 épisodes : 20-21/09 et 28/02) ; résistance 50,58 € (pente +0,074, portée 43, 3 épisodes, dernier 10/02) : canal divergent, largeur 13,46 € (35,6 %).
Rupture entièrement qualifiée : résidu −4,27 σ, 3 séances consécutives dehors (24, 25 et 28/02), volume à 1,90 fois la moyenne 20 séances ; position 5,1 %.
Observable ensuite : la clôture du 28/02 constitue elle-même le deuxième point du support convexe ; une clôture sous 37,1 € priverait la valeur de toute borne basse sur la fenêtre.

### TTE.PA
Tendance longue haussière et très explicative : +0,078 €/séance (+0,226 %/séance), R² = 0,76, p ≈ 10⁻³⁹.
Tendance courte baissière : −0,140 €/séance (−0,359 %/séance), R² = 0,42, p = 2,0·10⁻³, soit −9,2 % en 20 séances.
Support 34,61 € (pente +0,064, portée 64, 3 épisodes, dernier 28/02) ; résistance 42,50 € (pente +0,087, portée 72, 3 épisodes, dernier 27-28/01) : canal divergent, largeur 7,89 € (22,4 %) contre 8,5 % fin décembre.
Position 8,2 % ; sortie du canal de régression le 28/02 à −2,62 σ, une seule séance, mais sur le plus gros volume relatif du panier (2,20 fois la moyenne 20 séances).
Observable ensuite : une séance isolée ne fait pas une rupture ; c'est une deuxième clôture consécutive sous la borne basse de régression, ou sous 34,6 €, qui la qualifierait.

### SU.PA
Tendance longue devenue marginale : +0,054 €/séance, R² = 0,04, p = 0,031, IC₉₅ [+0,005 ; +0,104] presque au contact de zéro.
Tendance courte baissière et nette : −0,695 €/séance (−0,524 %/séance), R² = 0,76, p = 5,5·10⁻⁷.
Support 118,72 € (pente −0,058, portée 97, 3 épisodes, dernier 22-24/02) ; résistance 130,57 € (pente −0,858 soit −0,672 %/séance, portée 31, 3 épisodes, dernier 16-21/02) : canal convergent, τ = 14,8 séances.
Position 74,9 %, largeur 11,85 € (9,3 %) après 25,7 % un mois plus tôt : le canal s'est refermé de plus de moitié ; plus bas de 120 séances à 118,83 € le 24/02.
Observable ensuite : avec une résistance qui perd 0,86 € par séance, l'encadrement s'annule en une quinzaine de séances ; le franchissement de 130,6 € ou la perte de 118,7 € trancherait avant.

### AI.PA
Tendance longue haussière : +0,056 €/séance (+0,055 %/séance), R² = 0,28, p = 3,6·10⁻¹⁰.
Tendance courte indéterminée : −0,093 €/séance, p = 0,25, IC₉₅ [−0,256 ; +0,071] contient zéro, TEND_20 = 0.
Support 95,33 € (pente +0,019, portée 89, 4 épisodes, dernier 14/02) ; résistance 112,87 € (pente +0,086, portée 81, 3 épisodes, dernier 05-06/01) ; la clôture du 05/01 a effleuré la borne haute (position 100,0 %), unique sortie des 45 dernières séances.
Position 37,1 %, largeur 17,55 € (17,2 %) contre 5,7 % au 31/12 : le canal a triplé de largeur en deux mois.
Observable ensuite : entre 95,3 € et 112,9 €, l'encadrement est trop large pour contraindre quoi que ce soit ; un nouveau test du support donnerait un cinquième épisode et le rendrait de nouveau lisible.

### DG.PA
Tendance longue haussière : +0,078 €/séance (+0,101 %/séance), R² = 0,46, p ≈ 10⁻¹⁷.
Tendance courte indéterminée : −0,142 €/séance, p = 0,13, IC₉₅ [−0,330 ; +0,047] contient zéro, TEND_20 = 0.
Support 76,68 € (pente +0,137, portée 50, 2 épisodes : 20/12 et 24-28/02, donc non confirmé) ; résistance 87,61 € (pente +0,097, portée 98, 4 épisodes, dernier 16-18/02).
Position 19,1 %, largeur 10,94 € (13,9 %) : le cours est à 2,7 % de son support, volume du jour à 1,61 fois sa moyenne 20 séances, aucune sortie au-delà de 2 σ sur la fenêtre.
Observable ensuite : le support se documente en ce moment même ; une clôture sous 76,7 € l'invaliderait avant qu'il atteigne trois épisodes, la résistance à 87,6 € restant le seul côté crédible.

### CAP.PA
Tendance longue réduite à presque rien : +0,059 €/séance, R² = 0,04, p = 0,030, IC₉₅ [+0,006 ; +0,112].
Tendance courte baissière : −0,855 €/séance (−0,496 %/séance), R² = 0,65, p = 1,7·10⁻⁵.
Support 158,62 € (pente +0,039, portée 96, 4 épisodes, dernier 22-24/02) ; résistance 199,46 € (pente +0,031, portée 32, 3 épisodes, dernier 04/01) : canal quasi parallèle, largeur 40,84 € (24,1 %) contre 11,5 % au 31/12.
Position 26,7 %, résidu −1,23 σ, aucune sortie au-delà de 2 σ sur les 45 dernières séances malgré −4,6 % en 20 séances.
Observable ensuite : l'écart entre pente de régression (+0,06 €/séance) et pente courte (−0,86 €/séance) signale un canal mal défini ; le support à 158,6 €, 6,9 % sous le cours, est le seul niveau réellement testable.

### RI.PA
Tendance longue disparue : +0,028 €/séance, R² = 0,02, p = 0,13, IC₉₅ [−0,009 ; +0,065] contient zéro, alors que R² valait 0,875 fin décembre.
Tendance courte également muette : +0,114 €/séance, p = 0,16, IC₉₅ [−0,050 ; +0,278], TEND_20 = 0.
Support 154,95 € (pente +0,038, portée 116, 3 épisodes, dernier 24/02) ; résistance 164,27 € (pente −0,448 soit −0,274 %/séance, portée 37, 2 épisodes : 04-06/01 et 18-28/02) : canal convergent, τ = 19,2 séances.
Position 89,6 %, largeur 9,33 € (5,7 %) : la clôture est à 0,6 % sous une résistance descendante qu'elle longe depuis huit séances.
Observable ensuite : cette résistance n'a que 2 épisodes ; ou bien elle est franchie au-dessus de ≈ 164 €, ou bien elle rejoint le support en une vingtaine de séances et l'encadrement cesse d'exister.

### ORA.PA
Tendance longue haussière et explicative : +0,0113 €/séance (+0,156 %/séance), R² = 0,70, p ≈ 10⁻³².
Tendance courte de même signe : +0,021 €/séance (+0,262 %/séance), R² = 0,57, p = 1,1·10⁻⁴ — seule valeur du panier dont les deux échelles restent haussières à cette date.
Support 6,57 € (pente −0,0013, portée 53, 4 épisodes, dernier 02-13/12) ; résistance 8,50 € (pente +0,0135, portée 113, 5 épisodes, dernier 17-23/02) : neuf épisodes, encadrement installé mais divergent (τ = ∞), largeur 1,93 € (23,7 %).
Position 82,3 %, plus haut de 120 séances à 8,42 € le 18/02, volume du jour à 0,98 fois sa moyenne 20 séances ; aucune clôture hors canal sur les 45 dernières séances.
Observable ensuite : la résistance monte de 0,0135 €/séance et a été testée deux fois en février ; une clôture au-dessus de ≈ 8,50 € serait le premier franchissement de la fenêtre.
## 2022-03-31
### AIR.PA
Tendance longue nulle : pente 120 séances de −0,011 €/séance (−0,01 %/séance), p = 0,43, R² = 0,005 — aucune direction distinguable du bruit (TEND_120 = 0).
Tendance courte franchement haussière : +0,73 €/séance (+0,76 %/séance), p < 10⁻⁴, R² = 0,80, IC₉₅ [0,55 ; 0,91], depuis le creux du 7 mars (82,79).
Encadrement convexe sur 120 séances : support 81,5 (pente −0,071, portée 71 séances, ancres 26/11/2021 et 07/03/2022), résistance 109,8 (−0,022, portée 31) ; largeur 28,2 € soit 27,9 %, cours à 69,9 % de la hauteur.
Contacts : 3 épisodes en résistance (04/01, 12/01, 16/02) — crédible ; 2 seulement au support — non confirmé. Le canal court (support +1,06 €/séance sur 17 séances) passe à 101,1, le cours est 0,2 % dessus.
Observable ensuite : une clôture sous 101 invaliderait la droite de rebond ; au-dessus de 109,8, la résistance de 120 séances cesserait d'encadrer.

### MC.PA
Baisse longue significative mais peu explicative : −0,507 €/séance (−0,081 %/séance), p < 10⁻⁴, R² = 0,22, IC₉₅ [−0,68 ; −0,33].
Rebond court net : +4,35 €/séance (+0,77 %/séance), p < 10⁻⁴, R² = 0,79 ; les deux horizons sont de signes opposés.
Encadrement 120 séances : support 480,8 (−0,83 €/séance, portée 100), résistance 612,5 (−1,48, portée 39) ; largeur 131,7 € soit 22,3 %, position 84,4 % — haut de canal.
Contacts : 3 épisodes en résistance (28/01, 08/02, 29/03), 2 au support ; canal faiblement convergent (croisement théorique à 204 séances).
Observable ensuite : le plafond recule de 1,5 €/séance ; le cours doit progresser d'autant pour se maintenir en haut de canal, et une clôture au-dessus de 612 romprait un plafond en place depuis fin janvier.

### OR.PA
Baisse longue nette : −0,528 €/séance (−0,148 %/séance), p < 10⁻⁴, R² = 0,49, IC₉₅ [−0,63 ; −0,43], jackknife stable [−0,551 ; −0,522].
Rebond court : +1,33 €/séance (+0,41 %/séance), p = 0,0002, R² = 0,55.
Encadrement 120 séances : support 291,1 (−0,354, portée 99, 3 épisodes : 15/10, 24/02, 07/03), résistance 345,1 (−0,859, portée 60, 2 épisodes : 03/01, 29/03) ; largeur 54,1 € soit 16,1 %, position 82,3 %.
Le canal se referme (croisement à 107 séances) ; le support est confirmé, la résistance non.
Observable ensuite : le plafond descend de 0,86 €/séance depuis le 3 janvier ; une clôture au-dessus le romprait, une clôture sous 291 casserait un support à 3 épisodes.

### SAN.PA
Hausse longue régulière et la mieux ajustée du panier avec ORA : +0,0596 €/séance (+0,082 %/séance), p < 10⁻⁴, R² = 0,63, IC₉₅ [0,051 ; 0,068], σ_e = 1,57 € (2,2 %).
Tendance courte non significative : +0,103 €/séance, p = 0,061 — TEND_20 = 0, la borne basse de l'IC₉₅ passe sous zéro.
Encadrement 120 séances : support 69,1 (+0,033, portée 99), résistance 78,1 (+0,030, portée 30, 3 épisodes : 27/01, 09/02, 10/03) ; largeur 9,00 € soit 12,1 %, position 61,4 %.
Canal quasi parallèle (pentes à 0,003 €/séance l'une de l'autre) : aucune convergence à horizon utile.
Observable ensuite : le plus haut des 120 séances est 77,71 (11/03) ; au-dessus, la résistance à 3 contacts serait franchie. Sous 69, la pente longue serait démentie.

### BNP.PA
Baisse longue significative mais faible : −0,0275 €/séance (−0,065 %/séance), p = 0,0025, R² = 0,075 seulement ; σ_e = 3,35 € (7,9 %), canal de régression large de 35,4 % — le plus lâche du panier.
Rebond court : +0,202 €/séance (+0,55 %/séance), p = 0,0017, R² = 0,43.
Encadrement 120 séances : support 29,2 (−0,101, portée 101, 4 épisodes : 15/10, 28/10, 30/11, 07/03 — structure installée), résistance 38,98 (−0,287, portée 33, 2 épisodes).
Largeur 9,78 € soit 26,1 %, position 83,8 %, convergence à 53 séances.
Observable ensuite : le cours est 1,6 € sous une résistance qui recule de 0,29 €/séance ; le support, seul côté confirmé, est 8,2 € plus bas — une clôture sous 29,2 romprait quatre épisodes de contact.

### TTE.PA
Les deux horizons haussiers et significatifs : 120 séances +0,047 €/séance (+0,133 %/séance), p < 10⁻⁴, R² = 0,42 ; 20 séances +0,101 €/séance (+0,281 %/séance), p < 10⁻⁴, R² = 0,65.
Encadrement 120 séances le plus resserré du panier : support 34,55 (+0,046, portée 69, 4 épisodes : 26/11, 01/03, 04/03, 15/03), résistance 37,69 (−0,086, portée 31, 2 épisodes) ; largeur 3,14 € soit 8,7 %.
Position exactement au milieu (50,0 %), mais le canal court est très étroit (1,66 € soit 4,6 %) et le cours en occupe le bas (1,3 %).
Le canal long converge en 24 séances : support montant contre résistance descendante, l'encadrement cessera géométriquement d'exister d'ici un mois.
Observable ensuite : la sortie du biseau se datera à la première clôture hors de [34,6 ; 37,7], indépendamment du sens.

### SU.PA
Baisse longue significative mais très peu explicative : −0,084 €/séance (−0,060 %/séance), p = 0,0012, R² = 0,085 ; σ_e = 9,54 € (6,8 %).
Rebond court vif : +0,937 €/séance (+0,70 %/séance), p < 10⁻⁴, R² = 0,63, soit +11,8 % en 20 séances.
Encadrement 120 séances : support 107,9 (−0,173, portée 97, 2 épisodes), résistance 141,5 (−0,355, portée 59, 3 épisodes : 03/01, 17/03, 29/03) ; largeur 33,6 € soit 24,2 %.
Position 92,2 % — le cours est à 1,9 % sous une résistance à 3 contacts, au sommet de son encadrement ; le support n'est pas confirmé.
Observable ensuite : la résistance recule de 0,36 €/séance ; une clôture au-dessus romprait un plafond installé depuis le 3 janvier.

### AI.PA
Tendance longue non significative : +0,0163 €/séance, p = 0,057, R² = 0,03, IC₉₅ [−0,0005 ; 0,033] — la borne basse contient zéro, aucune affirmation directionnelle possible.
Tendance courte la mieux ajustée du panier : +0,746 €/séance (+0,72 %/séance), p < 10⁻⁴, R² = 0,91.
Encadrement 120 séances : support 93,1 (−0,036, portée 100, 3 épisodes), résistance 110,5 (+0,015, portée 59, 3 épisodes : 05/01, 13/01, 25/03) ; largeur 17,4 € soit 16,0 %, les deux côtés crédibles.
Position 90,4 %, résidu de +1,53 σ_e sur la droite longue ; le plus haut des 120 séances (110,48) date du 29/03, deux séances plus tôt.
Observable ensuite : une clôture au-dessus de 110,5 sortirait de l'encadrement par le haut ; le retour sous 108 ramènerait le cours dans le corps du canal.

### DG.PA
Hausse longue faible mais significative : +0,0375 €/séance (+0,049 %/séance), p = 0,0002, R² = 0,11, IC₉₅ [0,018 ; 0,057].
Hausse courte : +0,369 €/séance (+0,49 %/séance), p = 0,0001, R² = 0,60.
Encadrement 120 séances : support 66,8 (−0,027, portée 69, 2 épisodes), résistance 89,9 (+0,100, portée 69, 3 épisodes : 05/11, 09/02, 16/02) ; canal divergent, largeur 23,1 € soit 29,9 % — le plus large du panier.
Position 46,2 % : le cours est au milieu, à 12,4 € sous la résistance et 10,7 € au-dessus du support. Aucun bord n'est en contact.
Observable ensuite : un encadrement aussi large n'impose rien à court terme ; seule une clôture hors de [66,8 ; 89,9] serait qualifiable, et rien n'en approche.

### CAP.PA
Baisse longue significative : −0,152 €/séance (−0,085 %/séance), p < 10⁻⁴, R² = 0,26, IC₉₅ [−0,199 ; −0,105].
Le rebond court le plus vif du panier : +1,570 €/séance (+0,94 %/séance), p < 10⁻⁴, R² = 0,88, soit +10,1 % en 20 séances.
Encadrement 120 séances : support 144,8 (−0,171, portée 97, 2 épisodes), résistance 184,3 (−0,225, portée 62, 3 épisodes : 28/12, 04/01, 29/03) ; largeur 39,5 € soit 21,7 %.
Position 95,0 % — au contact de la résistance, touchée le 29/03 ; résidu +1,41 σ_e sur la droite longue.
Observable ensuite : une clôture au-dessus de 184,3 (droite qui recule de 0,23 €/séance) romprait le plafond de janvier ; un repli sous 176 ramènerait le cours au corps du canal.

### RI.PA
Baisse longue significative : −0,148 €/séance (−0,089 %/séance), p < 10⁻⁴, R² = 0,41 ; σ_e = 6,16 € (3,7 %).
Rebond court : +0,837 €/séance (+0,54 %/séance), p < 10⁻⁴, R² = 0,73 ; le cours occupe 81 % de son canal court.
Encadrement 120 séances : support 141,1 (−0,158, portée 101), résistance 168,8 (−0,205, portée 61) ; largeur 27,7 € soit 16,7 %, position 91,3 %.
Les deux droites n'ont que 2 épisodes de contact : encadrement géométriquement valide mais non confirmé ; la séance du 31/03 est elle-même une ancre de la résistance.
Observable ensuite : le cours est au contact du plafond qu'il vient de définir ; une clôture au-dessus de 168,8 le romprait, faute de quoi la droite reste une contrainte à deux points.

### ORA.PA
La tendance longue la plus régulière du panier : +0,0129 €/séance (+0,173 %/séance), p < 10⁻⁴, R² = 0,77, IC₉₅ [0,0116 ; 0,0142], jackknife pratiquement invariant.
Tendance courte de même sens : +0,0179 €/séance (+0,22 %/séance), p < 10⁻⁴, R² = 0,77, mais le cours est en bas de son canal court (11,7 % de la hauteur, z = −1,71).
Encadrement 120 séances : support 7,70 (+0,0132, portée 61, 2 épisodes), résistance 8,87 (+0,0154, portée 85, 3 épisodes : 15/10, 10/11, 08/02) ; canal montant légèrement divergent, largeur 1,16 € soit 14,4 %.
Position 32,2 % : le titre est revenu dans le tiers bas de son canal alors que la pente reste positive — l'écart entre les deux horizons vient du repli des 20 dernières séances (−0,2 %).
Observable ensuite : une clôture sous 7,70 romprait le support ascendant ; le maintien au-dessus laisserait le cours dans un canal dont la géométrie n'a pas changé depuis octobre.

## 2022-04-29
### AIR.PA
Tendance longue à la limite de la significativité : −0,0288 €/séance (−0,03 %/séance), p = 0,047, R² = 0,033, IC₉₅ [−0,057 ; −0,0004] — la borne haute frôle zéro ; TEND_120 bascule à −1 sur un test dont l'autocorrélation gonfle le taux de rejet.
Tendance courte nulle : −0,122 €/séance, p = 0,199, R² = 0,09.
Encadrement 120 séances resserré en un mois : support 94,2 (+0,311 €/séance, portée 34, ancres 07/03 et 27/04), résistance 100,9 (−0,193, portée 43, 3 épisodes) ; largeur 6,74 € soit 6,9 %, contre 27,9 % au 31 mars.
Le biseau converge en 13 séances ; position 59,5 %, mais le support n'a que 2 épisodes de contact.
Observable ensuite : les deux droites se croisent avant la mi-mai ; la première clôture hors de [94,2 ; 100,9] datera la sortie.

### MC.PA
Les deux horizons baissiers et significatifs : 120 séances −0,895 €/séance (−0,145 %/séance), p < 10⁻⁴, R² = 0,60 ; 20 séances −1,288 €/séance (−0,222 %/séance), p = 0,0065, R² = 0,35.
La pente longue s'est aggravée depuis fin mars (−0,507 → −0,895 €/séance).
Encadrement 120 séances : support 559,5 (+1,72, portée 35), résistance 592,3 (−1,35, portée 54, 6 épisodes : 05/01, 28/01, 08/02, 29/03, 21/04, 29/04) — plafond très installé ; largeur 32,7 € soit 5,7 % seulement.
Convergence en 11 séances ; position 35,7 % ; le 29/04 est lui-même une touche de la résistance en séance.
Observable ensuite : biseau presque fermé — une clôture sous 559 ou au-dessus de 592 tranchera dans les deux semaines.

### OR.PA
Baisse longue franche : −0,666 €/séance (−0,190 %/séance), p < 10⁻⁴, R² = 0,73, IC₉₅ [−0,74 ; −0,59].
Baisse courte confirmée : −1,262 €/séance (−0,381 %/séance), p < 10⁻⁴, R² = 0,69 ; le cours est pourtant au sommet de son canal court (100 %).
Encadrement 120 séances : support 312,0 (+0,393, portée 34, 3 épisodes), résistance 334,5 (−0,789, portée 65, 4 épisodes : 03/01, 29/03, 21/04, 28/04) — plafond installé ; largeur 22,5 € soit 6,9 %.
Convergence en 19 séances, position 64,2 % ; le canal s'est refermé de 16,1 % à 6,9 % de largeur en un mois.
Observable ensuite : la résistance recule de 0,79 €/séance ; une clôture au-dessus romprait quatre mois de plafond, une clôture sous 312 romprait un support à 3 contacts.

### SAN.PA
Hausse longue qui s'accélère : +0,0986 €/séance (+0,133 %/séance), p < 10⁻⁴, R² = 0,71, IC₉₅ [0,087 ; 0,110], contre +0,060 un mois plus tôt.
Hausse courte : +0,298 €/séance (+0,37 %/séance), p = 0,0046, R² = 0,37, mais le cours est en bas du canal court (14,8 %).
Encadrement 120 séances : support 69,4 (+0,022, portée 66), résistance 87,6 (+0,123, portée 104) — canal montant divergent, largeur 18,2 € soit 22,3 %, position 67,6 %. Deux épisodes de chaque côté : géométriquement valide, non confirmé.
Épisode de sortie haute du 08 au 13/04, maximum +3,11 σ_e le 11/04 (plus haut 120 séances à 86,08), résorbé depuis : trois séances, non persistant.
Observable ensuite : un retour sous 80 replacerait le cours au milieu du canal ; sous 69,4, la pente longue et son support seraient contredits ensemble.

### BNP.PA
Baisse longue confirmée et renforcée : −0,070 €/séance (−0,170 %/séance), p < 10⁻⁴, R² = 0,33, contre −0,0275 fin mars.
Tendance courte nulle : +0,026 €/séance, p = 0,574, R² = 0,018 — le rebond de mars s'est éteint.
Encadrement 120 séances : support 26,98 (−0,109, portée 69, 2 épisodes), résistance 36,78 (−0,227, portée 48, 2 épisodes) ; largeur 9,79 € soit 27,4 %, position 90,0 %.
Le support qui comptait 4 épisodes fin mars n'en a plus que 2 : la fenêtre a glissé et l'encadrement s'est dé-confirmé des deux côtés.
Observable ensuite : le cours est 1 € sous une résistance qui recule de 0,23 €/séance et n'a pas été franchie depuis le 10/02 ; une clôture au-dessus la romprait.

### TTE.PA
Hausse longue significative : +0,0338 €/séance (+0,094 %/séance), p < 10⁻⁴, R² = 0,24, mais en retrait sur le mois (+0,047 fin mars).
Tendance courte plate : −0,008 €/séance, p = 0,78 ; le cours occupe pourtant 98,9 % de la hauteur de son canal court.
Encadrement 120 séances : support 34,64 (+0,039, portée 103, 3 épisodes : 26/11, 07/03, 25/04), résistance 37,50 (−0,059, portée 45, 3 épisodes : 08/02, 19/04, 29/04) — les deux côtés crédibles ; largeur 2,85 € soit 7,7 %.
Convergence en 29 séances, position 84,5 %, et le 29/04 touche la résistance.
Observable ensuite : une clôture au-dessus de 37,5 romprait un plafond à 3 contacts ; le plus haut des 120 séances reste 40,60 (11/02).

### SU.PA
Baisse longue nette : −0,209 €/séance (−0,149 %/séance), p < 10⁻⁴, R² = 0,48.
Baisse courte franche : −0,772 €/séance (−0,588 %/séance), p < 10⁻⁴, R² = 0,72, soit −9,8 % en 20 séances — le rebond de mars est effacé.
Encadrement 120 séances : support 120,5 (+0,256, portée 35, 2 épisodes), résistance 137,8 (−0,317, portée 64, 3 épisodes : 03/01, 29/03, 01/04) ; largeur 17,4 € soit 13,8 %, convergence en 30 séances.
Position 30,2 % : le cours est descendu dans le tiers bas de son encadrement, à 0,8 % au-dessus du support ascendant.
Observable ensuite : une clôture sous 120,5 romprait ce support (2 épisodes seulement, donc non confirmé) ; le plus bas de référence en dessous est 111,00 (07/03).

### AI.PA
Hausse longue significative mais peu explicative : +0,0381 €/séance (+0,036 %/séance), p = 0,0001, R² = 0,12.
Hausse courte : +0,094 €/séance (+0,085 %/séance), p = 0,028, R² = 0,24 ; le cours est au résidu maximal de la fenêtre 120 (z = +1,71, position 100 %).
Encadrement 120 séances : support 109,7 (+0,442, portée 32), résistance 113,76 (+0,052, portée 80, 4 épisodes : 08/12, 05/01, 11/04, 29/04) ; largeur 4,09 € soit 3,6 % — le canal le plus étroit du panier.
Convergence en 10 séances ; le 29/04 établit le plus haut des 120 séances (113,76) et touche la résistance.
Observable ensuite : un biseau de 3,6 % ne survit pas dix séances ; une clôture au-dessus de 113,8 sortirait par le haut d'un plafond à 4 contacts.

### DG.PA
Hausse longue faible et fragile : +0,0242 €/séance (+0,031 %/séance), p = 0,021, R² = 0,044, IC₉₅ [0,004 ; 0,045] — la borne basse est très proche de zéro.
Hausse courte : +0,234 €/séance (+0,31 %/séance), p = 0,0064, R² = 0,35.
Encadrement 120 séances : support 66,30 (−0,027, portée 69, 2 épisodes), résistance 80,49 (−0,123, portée 47, 3 épisodes : 10/02, 16/02, 26/04) ; largeur 14,2 € soit 17,9 %, position 91,4 %.
Le cours est 1,2 € sous une résistance qui descend de 0,12 €/séance ; le support est 13 € plus bas, hors de portée utile.
Observable ensuite : franchir 80,5 romprait le plafond de février ; à défaut, le repli vers le corps du canal reste sans contrainte basse identifiable.

### CAP.PA
Baisse longue confirmée : −0,199 €/séance (−0,112 %/séance), p < 10⁻⁴, R² = 0,47, IC₉₅ [−0,238 ; −0,160].
Baisse courte : −0,449 €/séance (−0,258 %/séance), p = 0,016, R² = 0,28 ; le cours est néanmoins à 94 % du canal court (z = +1,70).
Encadrement 120 séances : support 164,8 (+0,459, portée 35, 2 épisodes), résistance 182,6 (−0,193, portée 64, 4 épisodes : 28/12, 04/01, 31/03, 29/04) — plafond installé ; largeur 17,8 € soit 10,1 %, contre 21,7 % fin mars.
Convergence en 27 séances, position 65,8 % ; la séance du 29/04 est le 4ᵉ épisode de contact haut.
Observable ensuite : sortie par le haut au-dessus de 182,6 (droite en recul de 0,19 €/séance), par le bas sous 164,8 (droite en hausse de 0,46 €/séance) — les deux se rejoignent d'ici début juin.

### RI.PA
Baisse longue nette : −0,162 €/séance (−0,098 %/séance), p < 10⁻⁴, R² = 0,49.
Baisse courte : −0,299 €/séance (−0,182 %/séance), p = 0,0014, R² = 0,44 ; le cours est pourtant au sommet de son canal court (100 %).
Encadrement 120 séances : support 159,8 (+0,446, portée 32, 3 épisodes), résistance 167,2 (−0,176, portée 65, 3 épisodes : 04/01, 31/03, 28/04) ; largeur 7,43 € soit 4,5 %, convergence en 12 séances, position 69,8 %.
Rupture antérieure documentée : 6 séances consécutives sous −2 σ_e du 07 au 15/03, jusqu'à −3,05 σ_e — persistante à l'époque, entièrement résorbée depuis.
Observable ensuite : le biseau se referme sous quinze séances ; une clôture hors de [159,8 ; 167,2] départagera support et résistance, tous deux à 3 contacts.

### ORA.PA
Les deux horizons alignés et très ajustés : 120 séances +0,0144 €/séance (+0,188 %/séance), p < 10⁻⁴, R² = 0,83 ; 20 séances +0,0245 €/séance (+0,294 %/séance), p < 10⁻⁴, R² = 0,83.
Encadrement 120 séances : support 8,39 (+0,025, portée 33, 4 épisodes : 07/03, 30/03, 12/04, 21/04 — installé), résistance 8,60 (+0,004, portée 47, 3 épisodes).
Largeur 0,20 € soit 2,4 % : inférieure à un seul σ_e de la droite longue (3,0 %) — l'encadrement est plus étroit que la dispersion normale du titre.
Convergence en 10 séances, position 71,5 % ; plus haut des 120 séances à 8,59 le 28/04.
Observable ensuite : un canal de 2,4 % ne contient pas la volatilité mesurée ; la sortie se lira au premier écart de 0,20 € et devra être qualifiée par sa persistance, pas par la seule séance de franchissement.

## 2022-05-31
### AIR.PA
Baisse longue significative mais faible : −0,052 €/séance (−0,05 %/séance), p = 0,0001, R² = 0,13.
Hausse courte fragile : +0,207 €/séance (+0,21 %/séance), p = 0,029, R² = 0,24, IC₉₅ [0,024 ; 0,389] — la borne basse est presque nulle.
Encadrement 120 séances : support 96,64 (+0,235, portée 54, 2 épisodes : 07/03, 24/05), résistance 105,23 (−0,073, portée 70, 2 épisodes : 16/02, 27/05) ; largeur 8,59 € soit 8,5 %, convergence en 28 séances.
Position 53,4 % — milieu de canal ; aucun côté n'a plus de 2 épisodes de contact : encadrement non confirmé, à traiter comme une contrainte géométrique.
Observable ensuite : seule une clôture hors de [96,6 ; 105,2] serait qualifiable ; un cours au milieu d'un canal à deux points ne dit rien.

### MC.PA
Baisse longue qui se renforce de mois en mois : −1,204 €/séance (−0,202 %/séance), p < 10⁻⁴, R² = 0,73, IC₉₅ [−1,34 ; −1,07], contre −0,51 fin mars et −0,89 fin avril.
Tendance courte nulle : +0,79 €/séance, p = 0,224, R² = 0,08.
Encadrement 120 séances : support 495,6 quasi horizontal (−0,004 €/séance, portée 55, 3 épisodes : 07/03, 09/05, 23/05), résistance 567,3 (−1,29, portée 81, 6 épisodes dont le 30/05) ; largeur 71,7 € soit 13,0 %.
Configuration en triangle descendant au sens strict : base plate mesurée à −0,001 %/séance, plafond en recul de 0,24 %/séance, convergence en 56 séances ; position 76,8 %. Plus bas des 120 séances : 495,60 le 25/05.
Observable ensuite : une clôture sous 495,6 romprait un support à 3 contacts ; au-dessus de 567, un plafond à 6 contacts installé depuis janvier.

### OR.PA
Baisse longue la plus marquée en pourcentage : −0,708 €/séance (−0,211 %/séance), p < 10⁻⁴, R² = 0,75, IC₉₅ [−0,78 ; −0,63].
Tendance courte plate : −0,116 €/séance, p = 0,751 ; le canal court est large (27,3 € soit 9,1 %) et le cours en occupe 89,6 %.
Encadrement 120 séances confirmé des deux côtés : support 279,2 (−0,309, portée 43, 4 épisodes : 24/02, 07/03, 09/05, 19/05), résistance 315,8 (−0,823, portée 37, 4 épisodes dont le 30/05) ; largeur 36,6 € soit 11,9 %, convergence en 71 séances, position 77,0 %.
Volume du jour à 3,3 fois sa moyenne 20 séances — effet de fin de mois visible sur l'ensemble du panier, pas un signal propre au titre.
Observable ensuite : plafond descendant touché le 30/05 ; une clôture au-dessus le romprait, une clôture sous 279,2 romprait un support à 4 contacts.

### SAN.PA
Hausse longue qui s'accélère encore : +0,128 €/séance (+0,167 %/séance), p < 10⁻⁴, R² = 0,83, IC₉₅ [0,118 ; 0,139] — progression mensuelle 0,060 → 0,099 → 0,128.
Hausse courte significative : +0,307 €/séance (+0,37 %/séance), p < 10⁻⁴, R² = 0,66, mais le cours est au résidu minimal de la fenêtre (z = −2,65, position 0 %).
Encadrement 120 séances : support 82,47 (+0,236, portée 59, 4 épisodes : 07/03, 14/03, 12/05, 30/05 — installé), résistance 87,85 (+0,052, portée 30, 2 épisodes) ; largeur 5,38 € soit 6,4 %, position 18,1 %.
La séance du 31/05 est elle-même l'ancre droite du support : le cours est posé dessus, volume 2,7 fois la moyenne.
Observable ensuite : une clôture sous 82,5 romprait un support ascendant à 4 épisodes, seul élément confirmé de la figure.

### BNP.PA
Baisse longue nette : −0,082 €/séance (−0,202 %/séance), p < 10⁻⁴, R² = 0,43.
La droite courte la mieux ajustée du panier : +0,301 €/séance (+0,78 %/séance), p < 10⁻⁴, R² = 0,92, σ_e = 0,51 €, soit +11,1 % en 20 séances — horizons de signes opposés.
Encadrement 120 séances : support 36,68 (+0,096, portée 38, 4 épisodes : 07/03, 06/04, 28/04, 09/05 — installé), résistance 42,23 (−0,089, portée 75, 2 épisodes : 09/02, 27/05) ; largeur 5,54 € soit 13,5 %, convergence en 30 séances, position 78,7 %.
Le cours est 1,18 € (2,9 %) sous une résistance qui recule de 0,09 €/séance ; résidu long de +1,63 σ_e.
Observable ensuite : franchir 42,2 romprait un plafond en place depuis février ; le canal court (largeur 4,5 %) est trop étroit pour encadrer 20 séances de plus.

### TTE.PA
Hausse longue significative : +0,0341 €/séance (+0,091 %/séance), p < 10⁻⁴, R² = 0,23 ; hausse courte très marquée : +0,291 €/séance (+0,715 %/séance), p < 10⁻⁴, R² = 0,87, soit +13,9 % en 20 séances.
Encadrement 120 séances confirmé des deux côtés : support 35,17 (+0,026, portée 89, 5 épisodes), résistance 43,92 (+0,039, portée 86, 4 épisodes dont le 26/05) ; canal montant légèrement divergent, largeur 8,75 € soit 20,1 %, position 96,5 %.
Sortie en cours par le haut : clôture du 31/05 à +2,00 σ_e au-dessus de la droite ajustée 120, première séance dehors, volume 1,8 fois la moyenne 20 séances.
Une séance à 2,0 σ_e n'est pas une rupture : ampleur juste au seuil, persistance de 1, volume ordinaire pour un 31 mai. Le plus haut des 120 séances (43,92) est posé le jour même.
Observable ensuite : c'est le maintien au-dessus de 43,9 sur plusieurs séances consécutives, et non le franchissement du jour, qui distinguerait la sortie du bruit.

### SU.PA
Baisse longue la plus forte du panier : −0,318 €/séance (−0,235 %/séance), p < 10⁻⁴, R² = 0,73, IC₉₅ [−0,353 ; −0,282].
Hausse courte marginale : +0,206 €/séance (+0,18 %/séance), p = 0,036, R² = 0,22, IC₉₅ [0,015 ; 0,397] — borne basse quasi nulle, conclusion directionnelle non tenable.
Encadrement 120 séances : support 111,2 strictement plat (+0,003 €/séance, portée 43, 3 épisodes : 07/03, 09/05, 25/05), résistance 123,3 (−0,516, portée 36, 3 épisodes dont le 30/05) ; largeur 12,15 € soit 10,1 %, position 77,0 %.
Convergence en 23 séances : l'encadrement cessera d'exister à cet horizon, quelle que soit l'évolution du cours.
Observable ensuite : une clôture au-dessus de 123,3 ou sous 111,0 romprait l'un des deux côtés, tous deux à 3 contacts.

### AI.PA
Hausse longue qui se raffermit : +0,0778 €/séance (+0,073 %/séance), p < 10⁻⁴, R² = 0,34 — progression mensuelle 0,016 → 0,038 → 0,078.
Hausse courte : +0,264 €/séance (+0,24 %/séance), p = 0,0009, R² = 0,46.
Encadrement 120 séances : support 110,2 (+0,283, portée 45, 2 épisodes), résistance 115,99 (+0,063, portée 101, 6 épisodes : 05/01, 13/01, 11/04, 29/04, 05/05, 27/05) — plafond parmi les mieux établis du panier ; largeur 5,80 € soit 5,1 %, convergence en 26 séances.
Position 57,8 % ; plus haut des 120 séances 115,93 le 30/05, volume du jour 2,9 fois la moyenne.
Observable ensuite : le titre bute depuis janvier dans une bande de 5 % ; une clôture au-dessus de 116 romprait six épisodes de contact, une clôture sous 110,2 un support qui n'en a que deux.

### DG.PA
Aucun des deux horizons ne se distingue du bruit : 120 séances −0,0047 €/séance, p = 0,615, R² = 0,002 ; 20 séances +0,013 €/séance, p = 0,770, R² = 0,005 — TEND_120 et TEND_20 tous deux à 0.
Encadrement 120 séances : support 74,66 (+0,125, portée 53, 2 épisodes), résistance 79,17 (−0,103, portée 68, 4 épisodes : 10/02, 16/02, 17/05, 26/05) ; largeur 4,51 € soit 5,9 %, convergence en 20 séances, position 42,3 %.
Le canal de régression sur la même fenêtre est presque quatre fois plus large (17,4 € soit 22,3 %) : l'encadrement convexe ne décrit que les deux derniers mois, pas les six.
Volume du jour 3,5 fois la moyenne 20 séances, sans mouvement de prix associé (−3,3 % sur 20 séances).
Observable ensuite : le biseau se referme en 20 séances ; la sortie sera datable, mais aucune tendance mesurée ne l'oriente.

### CAP.PA
Baisse longue confirmée : −0,188 €/séance (−0,108 %/séance), p < 10⁻⁴, R² = 0,44.
Tendance courte nulle : −0,034 €/séance, p = 0,806, malgré −7,0 % en 20 séances — la droite courte ne capte pas un mouvement en dents de scie (σ_e court 3,32 €).
Encadrement 120 séances : support 158,2 (+0,176, portée 51, 3 épisodes : 07/03, 12/05, 19/05), résistance 178,4 (−0,193, portée 64, 4 épisodes : 28/12, 04/01, 31/03, 29/04) ; largeur 20,2 € soit 12,4 %, convergence en 55 séances.
Position 21,3 % — bas d'encadrement ; le cours est au contact de la droite basse de son canal court (162,51, position 0 %).
Observable ensuite : une clôture sous 158,2 romprait un support à 3 contacts ; le plafond à 178,4 n'a plus été approché depuis le 29/04.

### RI.PA
Baisse longue significative : −0,164 €/séance (−0,101 %/séance), p < 10⁻⁴, R² = 0,47, IC₉₅ [−0,195 ; −0,132].
Tendance courte non significative : −0,324 €/séance, p = 0,066, R² = 0,18, malgré −8,0 % sur les 20 séances — l'IC₉₅ [−0,672 ; 0,024] change de signe.
Encadrement 120 séances confirmé des deux côtés : support 145,97 quasi plat (+0,039, portée 54, 4 épisodes : 07/03, 11/03, 09/05, 19/05), résistance 164,99 (−0,160, portée 82, 4 épisodes : 04/01, 06/04, 28/04, 03/05) ; largeur 19,0 € soit 12,5 %.
Convergence lente (96 séances), position 33,4 % : le cours redescend vers la base plate après avoir été rejeté du plafond début mai.
Observable ensuite : une clôture sous 146 romprait la seule structure installée du titre ; le plus bas des 120 séances est 143,73 (08/03).

### ORA.PA
La tendance longue la plus régulière du panier : +0,0156 €/séance (+0,195 %/séance), p < 10⁻⁴, R² = 0,89, IC₉₅ [0,0146 ; 0,0166], soit +30,5 % sur 120 séances.
La hausse courte s'est arrêtée : +0,0041 €/séance, p = 0,082, R² = 0,16, +1,7 % seulement en 20 séances.
Encadrement 120 séances : support 8,04 (+0,011, portée 98, 5 épisodes : 13/12, 20/12, 07/01, 07/03, 02/05), résistance 9,04 (+0,0089, portée 66, 3 épisodes : 09/02, 04/05, 24/05) ; canal montant quasi parallèle, largeur 1,00 € soit 11,4 %, position 74,5 %.
Les deux côtés sont installés, sur des portées de 98 et 66 séances : c'est l'encadrement le mieux confirmé des douze valeurs. Plus haut des 120 séances 9,01 le 25/05, volume du jour 2,4 fois la moyenne.
Observable ensuite : le support monte de 0,011 €/séance ; une clôture sous 8,04 romprait cinq épisodes de contact étalés sur six mois, et c'est le seul événement qui invaliderait la figure.
## 2022-06-30
### AIR.PA
Tendance longue baissière et significative : pente 120 s = −0,108 €/séance (−0,117 %/s), p = 2,6·10⁻¹⁴, R² = 0,39, IC₉₅ [−0,133 ; −0,084] ; tendance courte plus raide, 20 s = −0,932 €/s (−1,13 %/s), p = 4,3·10⁻⁷, R² = 0,77.
Canal de régression 120 s : largeur 24,77 € (25,1 % du niveau moyen), cours à 35 % de hauteur, z = −1,34 ; dans le canal 20 s il est à 92 %, mais d'un canal fortement descendant.
Support par enveloppe convexe quasi horizontal, +0,014 €/s, portée 81 séances (07/03 → 30/06), 5 touches : 07/03, 08/03, 23/06, 24/06 et 30/06 — palier 83-84 € retesté le jour même.
Résistance oblique −0,073 €/s, portée 70 s, 7 touches, niveau 103,62 € : cours 17,0 % en dessous. Dispersion en hausse, σ_e(20) × 1,56 par rapport aux 20 séances précédentes.
Une clôture sous 82,74 € (plus-bas du 07/03) invaliderait le palier à 5 touches ; un retour au-dessus de 103,6 € casserait la résistance descendante.

### MC.PA
Baisse longue nette et bien ajustée : 120 s = −1,050 €/s (−0,206 %/s), p = 3,4·10⁻²⁹, R² = 0,66 ; mais la pente 20 s (−1,07 €/s) a p = 0,24 avec IC₉₅ [−2,91 ; +0,77] — plus aucune direction courte affirmable.
Cours à 85 % du canal de régression 120 s (largeur 139,8 €, soit 24,4 %), c'est-à-dire près du bord haut d'un canal descendant.
Résistance convexe −1,161 €/s (−0,210 %/s), portée 101 séances (02/02 → 27/06), 16 touches, niveau 552,42 € : le cours clôture 2,9 % dessous.
Support convexe quasi plat (−0,035 €/s), portée 71 s (07/03 → 16/06), 15 touches dont 09, 10, 12 et 24/05, niveau 492,95 € — appui de 493 € éprouvé.
Une clôture au-dessus de 552 € romprait une résistance de cinq mois ; un retour vers 493 € remettrait à l'épreuve le plancher du 16/06.

### OR.PA
Longue baisse significative : 120 s = −0,449 €/s (−0,153 %/s), p = 4,0·10⁻²⁸, R² = 0,64 ; à 20 s la pente redevient positive (+0,361 €/s) mais p = 0,39, IC₉₅ [−0,50 ; +1,22] — stabilisation, pas retournement.
Cours à 80 % du canal 120 s (largeur 51,58 €, 16,1 %), z = +1,22 : partie haute du canal descendant.
Résistance convexe −0,444 €/s (−0,139 %/s), portée 57 séances (05/04 → 27/06), 11 touches, niveau 320,44 € : cours 3,9 % dessous.
Le support convexe 120 s est lointain (272,36 €, +13,1 %) ; l'appui utile est le support quasi horizontal de la fenêtre 60 s, 280,81 €, 7 touches dont 14, 15 et 16/06.
Un franchissement de 320 € invaliderait la résistance descendante ; une clôture sous 281 € confirmerait au contraire le canal baissier long.

### SAN.PA
Une des deux seules hausses longues nettes de l'univers : 120 s = +0,103 €/s (+0,121 %/s), p = 1,5·10⁻²⁹, R² = 0,66, IC₉₅ [+0,090 ; +0,117] ; à 20 s la pente est nulle (−0,026 €/s, p = 0,76).
Cours à 13 % du canal 120 s (largeur 12,18 €, 15,5 %), z = −1,55 : bord bas d'un canal haussier.
Support convexe ascendant +0,132 €/s (+0,166 %/s), portée 71 séances (07/03 → 16/06), 8 touches dont 15, 16, 17, 20 et 21/06, niveau 79,21 € : cours 2,1 % dessus, appui travaillé toute la seconde quinzaine de juin.
Résistance convexe +0,052 €/s, 6 touches, niveau 88,98 € : cours 9,1 % dessous ; canal large et régulier, aucune sortie au-delà de 2 σ_e depuis le 16/06.
Une clôture sous 79,2 € romprait un support ascendant à 8 touches et contredirait la pente longue.

### BNP.PA
Baisse aux deux horizons : 120 s = −0,074 €/s (−0,210 %/s), p = 1,6·10⁻¹³, R² = 0,37 ; 20 s = −0,227 €/s (−0,639 %/s), p = 6,0·10⁻⁵, R² = 0,60.
Canal de régression 120 s le plus large de l'univers : 14,09 €, soit 35,6 % du niveau moyen — un encadrement de cette amplitude ne contraint presque rien ; cours à 60 % de hauteur, z = −0,03, plein milieu.
Le support convexe ne repose que sur 2 points (07/03 et 30/06), niveau 34,25 € : droite géométriquement valide mais **non confirmée**.
Résistance −0,089 €/s (−0,222 %/s), portée 75 séances, 11 touches, niveau 40,26 € : cours 12,9 % dessous. σ_e(20) a doublé (× 2,00) : élargissement net de la dispersion.
Une clôture sous 31,01 € (plus-bas du 07/03) ferait disparaître le seul appui de la fenêtre ; volume du jour 1,96 fois la moyenne 20 séances.

### TTE.PA
Signes opposés : 120 s = +0,030 €/s (+0,075 %/s), p = 1,6·10⁻⁶ mais R² = 0,18 seulement ; 20 s = −0,258 €/s (−0,667 %/s), p = 1,5·10⁻⁵, R² = 0,66.
Cours à 46 % du canal 120 s (largeur 8,83 €, 22,9 %) : milieu de canal ; à 95 % du canal 20 s, descendant.
Support convexe ascendant +0,075 €/s (+0,198 %/s), portée 43 séances (26/04 → 24/06), 5 touches dont 23 et 24/06, niveau 38,07 € : cours 5,2 % dessus.
Résistance +0,048 €/s, portée 93 séances (27/01 → 09/06), 10 touches, niveau 45,76 € : cours 12,5 % dessous ; le plus-haut 120 s (45,05 €) date du 09/06.
Un retour sous 38,1 € casserait le support ascendant et alignerait l'horizon court sur le long ; σ_e(20) × 1,49.

### SU.PA
La baisse longue la mieux ajustée de l'univers : 120 s = −0,276 €/s (−0,249 %/s), p = 4,6·10⁻³³, R² = 0,71, IC₉₅ [−0,308 ; −0,243] ; 20 s = −0,844 €/s (−0,814 %/s), p = 1,6·10⁻⁶.
Cours à 32 % du canal 120 s (largeur 30,13 €, 23,7 %), z = −0,85 : moitié basse.
Support convexe descendant −0,110 €/s (−0,108 %/s), portée 75 séances (07/03 → 22/06), 5 touches : 07/03, 20/06, 22/06, 23/06 et 30/06 — appui touché le jour même.
Résistance −0,462 €/s (−0,401 %/s), 13 touches, niveau 115,19 € : cours 8,5 % dessous ; le plus-bas 120 s (102,77 €) est du 22/06, à 2,5 % du cours.
Une clôture sous 102,77 € prolongerait le canal descendant sans figure d'appui restante dans la fenêtre.

### AI.PA
Configuration contradictoire : 120 s = +0,054 €/s (+0,049 %/s), p = 3,8·10⁻⁵ mais R² = 0,14 — pente longue faible ; 20 s = −0,716 €/s (−0,734 %/s), p = 5,9·10⁻⁶, R² = 0,69.
**Rupture par le bas du canal ±2 σ_e (120 s)** : z = −2,34 ce jour, après −2,0 le 17/06, −2,4 le 20/06 et −2,0 le 23/06 — quatre sorties en dix séances, volume du jour 1,67 fois la moyenne 20 s ; persistance encore d'une séance consécutive seulement.
Cours à 1 % du canal de régression 120 s : plancher de l'encadrement.
Support convexe ascendant +0,050 €/s, portée 72 séances (08/03 → 20/06), 6 touches dont 20, 22, 23 et 30/06, niveau 97,73 € : le cours clôture 0,6 % dessus, collé à la droite.
Deux clôtures consécutives sous 97,7 € rompraient ce support ; le +1 de la tendance longue deviendrait alors intenable.

### DG.PA
Baisse modérée aux deux horizons : 120 s = −0,062 €/s (−0,084 %/s), p = 1,1·10⁻¹³, R² = 0,38 ; 20 s = −0,223 €/s (−0,308 %/s), p = 0,0035, R² = 0,39.
Cours à 56 % du canal 120 s (largeur 16,34 €, 21,0 %), z = −0,54 : milieu.
Support convexe légèrement ascendant +0,045 €/s, portée 75 séances (07/03 → 22/06), 4 touches (07/03, 08/03, 22/06, 30/06), niveau 70,94 € : cours 2,3 % dessus.
Résistance −0,103 €/s (−0,134 %/s), portée 77 séances, 14 touches, niveau 76,91 € : cours 5,7 % dessous — les deux droites convergent, l'encadrement se referme.
Une clôture sous 70,9 € romprait le support à 4 touches ; au-dessus de 76,9 €, c'est la résistance à 14 touches qui cède. La convergence impose une sortie par l'un des deux bords.

### CAP.PA
Baisse longue significative : 120 s = −0,157 €/s (−0,099 %/s), p = 2,0·10⁻¹⁴, R² = 0,39 ; à 20 s la pente (−0,315 €/s) a p = 0,12 et un IC₉₅ [−0,72 ; +0,09] qui change de signe — aucune direction courte affirmable.
Cours à 31 % du canal 120 s (largeur 37,96 €, 22,5 %) et à 10 % du canal 20 s : bord bas de l'encadrement court.
Support convexe quasi horizontal +0,008 €/s, portée 81 séances (07/03 → 30/06), 4 touches (07/03, 08/03, 16/06, 30/06), niveau 148,50 € : cours 0,4 % dessus.
Résistance −0,333 €/s (−0,201 %/s), 5 touches, niveau 166,21 € : cours 10,3 % dessous ; σ_e(20) × 1,78, volume du jour 1,68 fois la moyenne.
Une clôture sous 147,83 € (plus-bas du 07/03) invaliderait ce palier horizontal, seul appui identifié de la fenêtre.

### RI.PA
Baisse longue confirmée et qui s'intensifie : 120 s = −0,135 €/s (−0,091 %/s), p = 3,9·10⁻¹⁵, R² = 0,41 ; sur 60 s, −0,396 €/s (−0,279 %/s) avec R² = 0,76 ; à 20 s, p = 0,24, non significatif.
Cours à 47 % du canal 120 s (largeur 27,28 €, 17,4 %) : milieu de canal, z = −0,43.
Support convexe −0,063 €/s, portée 74 séances (08/03 → 22/06), 7 touches dont 16, 17, 20 et 21/06, niveau 138,67 € : cours 5,5 % dessus.
Résistance −0,424 €/s (−0,282 %/s), portée 40 séances (03/05 → 28/06), 5 touches dont 24, 27, 28 et 29/06, niveau 150,39 € : le cours bute dessous depuis quatre séances.
Un franchissement de 150,4 € casserait une résistance testée cette semaine même ; une clôture sous 139,05 € (plus-bas du 22/06) validerait la continuation.

### ORA.PA
La hausse longue la plus régulière de l'univers : 120 s = +0,0101 €/s (+0,113 %/s), p = 9,3·10⁻³⁹, R² = 0,76, IC₉₅ [+0,0090 ; +0,0111] ; 20 s = +0,0106 €/s (+0,122 %/s), p = 0,013.
Canal de régression 120 s le plus étroit : 0,68 €, soit 8,2 % du niveau moyen ; cours à 32 % de hauteur, **aucune sortie au-delà de 2 σ_e sur les 120 séances**.
Support convexe ascendant +0,0092 €/s (+0,112 %/s), niveau 8,21 €, mais 2 touches seulement (07/03 et 02/05) : droite non confirmée.
Résistance +0,0089 €/s (+0,096 %/s), portée 66 séances (18/02 → 25/05), 14 touches, niveau 9,24 € : borne haute solide, cours 5,1 % dessous.
Une clôture hors de la bande 8,21-9,24 €, dans un sens ou dans l'autre, trancherait un encadrement respecté depuis six mois.

## 2022-07-29
### AIR.PA
Retournement court franc : 20 s = +0,727 €/s (+0,721 %/s), p = 2,6·10⁻⁷, R² = 0,78 ; la pente longue reste négative mais s'affaiblit, 120 s = −0,080 €/s (−0,087 %/s), p = 3,1·10⁻⁸, R² tombé de 0,39 à 0,23.
Cours à 84 % du canal 120 s et à 16 % du canal 20 s (ascendant) ; σ_e(20) ramené à 0,68 fois celui des 20 séances antérieures : resserrement.
Le support convexe est devenu strictement plat (−0,0006 €/s), portée 84 séances (07/03 → 05/07), 6 touches, niveau 82,73 € : le rebond part du double appui du 07/03 et du 05/07.
Résistance descendante −0,139 €/s (−0,140 %/s), portée 39 séances (30/05 → 22/07), 13 touches, niveau 99,20 € : cours 1,6 % dessous.
Une clôture au-dessus de 99,2 € casserait une résistance à 13 touches ; en deçà, le rebond reste borné par elle.

### MC.PA
Sursaut court très significatif : 20 s = +3,460 €/s (+0,573 %/s), p = 1,3·10⁻⁸, R² = 0,84 ; la pente longue reste négative (−0,394 €/s) mais son R² a chuté de 0,66 à 0,16 en un mois.
**Sortie par le haut du canal ±2 σ_e (120 s)** : z = +2,74 ce jour après +2,4 le 28/07 — deux séances consécutives dehors, volume 1,68 fois la moyenne 20 s. Ampleur et persistance suffisantes pour être qualifiées.
Cours à 100 % des canaux de régression 20 s et 120 s.
La dernière arête haute de l'enveloppe convexe passe par le cours du jour mais ne repose que sur 2 points (10/02 et 29/07), niveau 627,09 € : **droite non confirmée**, à ne pas tenir pour une résistance établie.
Une troisième clôture au-dessus de 627 € confirmerait la sortie ; un retour sous 566 € (support convexe 60 s, 7 touches) la ramènerait au rang de dépassement passager.

### OR.PA
Reprise courte nette : 20 s = +1,379 €/s (+0,411 %/s), p = 4,4·10⁻⁶, R² = 0,70 ; la pente longue reste −0,161 €/s (p = 6,3·10⁻⁵) mais avec R² = 0,13 seulement — elle n'explique presque plus rien.
**Sortie par le haut du canal 120 s** : z = +2,60, première séance dehors, volume 1,84 fois la moyenne — une seule séance, donc pas encore une rupture qualifiée.
Cours à 100 % du canal 120 s, 79 % du canal 20 s ; plus-haut des 120 séances inscrit ce jour en séance, 348,95 €.
Résistance convexe quasi horizontale +0,023 €/s, portée 81 séances (05/04 → 29/07), 6 touches, niveau 348,95 € : atteinte exactement aujourd'hui.
Une clôture au-dessus de 349 € casserait le plafond d'avril-juillet ; le support ascendant de la fenêtre 60 s est à 319,63 € (8 touches).

### SAN.PA
Hausse longue toujours significative mais qui s'érode : 120 s = +0,086 €/s (+0,100 %/s), p = 6,0·10⁻²², R² revenu de 0,66 à 0,55 ; 20 s = −0,019 €/s, p = 0,62, strictement plat.
Cours à 15 % du canal 120 s et à 12 % du canal 20 s : bord bas des deux encadrements.
Support convexe ascendant +0,127 €/s (+0,156 %/s), portée 102 séances (07/03 → 29/07), 11 touches, niveau 81,52 € : le cours clôture 0,1 % dessus, à même la droite.
Résistance convexe descendante −0,065 €/s, portée 45 séances (26/05 → 28/07), 12 touches, niveau 84,63 € : les deux bords convergent, largeur ramenée à 3,1 €.
Une clôture sous 81,5 € romprait un support à 11 touches ; la convergence des deux droites impose de toute façon une sortie à brève échéance.

### BNP.PA
Baisse longue modeste : 120 s = −0,043 €/s (−0,124 %/s), p = 4,5·10⁻⁸, R² = 0,23 ; à 20 s, +0,030 €/s avec p = 0,43 et IC₉₅ [−0,048 ; +0,108] qui change de signe — aucune direction courte affirmable.
Canal 120 s large de 14,57 €, soit 39,0 % du niveau moyen : le plus lâche de l'univers, il ne contraint rien ; cours à 50 % de hauteur, mais à 99 % du canal 20 s.
Support convexe presque plat (+0,005 €/s), portée 92 séances, 3 touches (07/03, 14/07, 15/07), niveau 31,48 € : crédible mais très en retrait, 13,0 % sous le cours.
Résistance −0,144 €/s (−0,400 %/s), portée 39 séances (06/06 → 29/07), 8 touches, niveau 36,01 € : cours 1,3 % dessous, butée du jour.
Une clôture au-dessus de 36,0 € casserait la résistance de juin-juillet ; sous 31,4 € (plus-bas du 15/07), le support à 3 touches tomberait.

### TTE.PA
Hausse longue significative mais peu explicative : 120 s = +0,036 €/s (+0,088 %/s), p = 8,3·10⁻⁹, R² = 0,25 ; 20 s = −0,019 €/s, p = 0,63 — court terme plat.
Cours à 30 % du canal 120 s (largeur 8,66 €, 22,5 %) : tiers bas ; 64 % du canal 20 s.
Résistance convexe −0,148 €/s (−0,372 %/s), portée 36 séances (09/06 → 29/07), touches les 26, 27, 28 **et** 29/07 : quatre séances consécutives de butée sur 39,73 €.
Support convexe ascendant +0,033 €/s (+0,090 %/s), portée 57 séances (26/04 → 14/07), 6 touches, niveau 36,79 € : cours 7,5 % dessus.
Une clôture au-dessus de 39,73 € romprait un plafond testé quatre jours de suite ; sous 36,8 €, c'est le support d'avril-juillet qui céderait.

### SU.PA
Contradiction franche entre horizons : 120 s = −0,230 €/s (−0,212 %/s), p = 3,0·10⁻²⁴, R² = 0,58 ; 20 s = +0,958 €/s (+0,788 %/s), p = 3,0·10⁻⁸, R² = 0,83.
**Sortie par le haut du canal 120 s** : z = +2,58 ce jour après +2,6 le 28/07 — deux séances consécutives dehors, volume 1,44 fois la moyenne 20 s.
Cours à 100 % du canal 120 s et 89 % du canal 20 s ; il a repris 22,3 % depuis le plus-bas du 22/06 (102,77 €).
Résistance convexe descendante −0,195 €/s (−0,153 %/s), portée 81 séances (05/04 → 29/07), 9 touches, niveau 127,13 € : cours 1,1 % dessous.
Une clôture au-dessus de 127,1 € casserait la résistance d'avril-juillet ; à défaut, la sortie de canal reste un simple contact de bord.

### AI.PA
Pente longue devenue indistinguable du bruit : 120 s = −0,018 €/s, p = 0,24, IC₉₅ [−0,049 ; +0,012], TEND_120 = 0 ; 20 s = +0,234 €/s (+0,233 %/s), p = 4,9·10⁻⁴, R² = 0,50.
Cours à 47 % du canal 120 s (largeur 22,30 €, 21,2 %) : milieu exact ; 100 % du canal 20 s. Plus aucune sortie au-delà de 2 σ_e — la rupture basse du 30/06 a été résorbée.
Résistance convexe −0,361 €/s (−0,349 %/s), portée 39 séances (06/06 → 29/07), 3 touches (06/06, 28/07, 29/07), niveau 103,58 € : contact du jour, droite tout juste crédible.
Support convexe plat (+0,002 €/s), portée 83 séances, 6 touches, niveau 93,93 € : cours 9,5 % dessus.
Une clôture au-dessus de 103,6 € romprait la résistance de juin ; entre 94 et 104 €, aucune direction longue n'est lisible.

### DG.PA
Redressement court net : 20 s = +0,303 €/s (+0,388 %/s), p = 5,4·10⁻⁷, R² = 0,76 ; la pente longue reste négative, 120 s = −0,041 €/s (−0,056 %/s), p = 2,7·10⁻⁷, R² = 0,20.
Cours à 94 % du canal 120 s (z = +1,95, juste sous le bord haut sans le franchir) et à 97 % du canal 20 s.
Résistance convexe de très longue portée, 113 séances (18/02 → 29/07), pente −0,055 €/s, 5 touches dont celle du jour, niveau 80,24 € : le cours clôture 0,6 % dessous.
Support convexe ascendant +0,042 €/s, portée 84 séances (07/03 → 05/07), 5 touches, niveau 71,53 € ; σ_e(20) ramené à 0,60 fois celui du mois précédent.
Une clôture au-dessus de 80,2 € casserait un plafond de cinq mois et demi, ce que quatre contacts n'ont pas fait depuis février.

### CAP.PA
Rebond court marqué : 20 s = +0,791 €/s (+0,496 %/s), p = 1,9·10⁻⁵, R² = 0,65 ; pente longue toujours nette, 120 s = −0,170 €/s (−0,110 %/s), p = 1,3·10⁻¹⁴, R² = 0,40.
**Sortie par le haut**, le même jour, des deux canaux : z = +2,13 (120 s) et +2,92 (20 s), première séance dehors, volume 2,05 fois la moyenne 20 s — le plus élevé de l'univers ce jour.
Cours à 95 % du canal 120 s et 100 % du canal 20 s.
Résistance convexe −0,200 €/s (−0,118 %/s), portée 82 séances (04/04 → 29/07), 5 touches, niveau 169,54 € : contact exact du jour.
Une seconde clôture au-dessus de 169,5 € confirmerait la rupture ; une séance isolée, fût-elle sur volume double, n'en est pas une.

### RI.PA
Droite courte la mieux ajustée de l'univers : 20 s = +0,711 €/s (+0,444 %/s), p = 1,7·10⁻¹¹, R² = 0,92 ; pente longue encore négative, 120 s = −0,099 €/s, p = 1,7·10⁻⁸, R² = 0,24.
Cours à 100 % du canal 120 s sans le franchir (z = +1,95) ; σ_e(20) divisé par trois (× 0,33) : baisse de dispersion très marquée.
Résistance convexe −0,083 €/s, portée 80 séances (06/04 → 29/07), 8 touches, niveau 163,20 € : cours 1,2 % dessous.
Support ascendant du rebond +0,556 €/s, 10 touches depuis le 22/06, mais **portée 17 séances seulement** sur une fenêtre de 60 : pente locale, non extrapolable ; l'appui robuste reste 137,35 € (7 touches, portée 74 s).
Une clôture au-dessus de 163,2 € casserait le plafond d'avril, testé huit fois.

### ORA.PA
Hausse longue très affaiblie : 120 s = +0,0033 €/s (+0,039 %/s), p = 2,8·10⁻⁵ mais R² effondré de 0,76 à 0,14 en un mois ; 20 s = −0,0455 €/s (−0,583 %/s), p = 3,0·10⁻¹⁰, R² = 0,90.
**Rupture basse qualifiée** : trois clôtures consécutives sous −2 σ_e (27/07 z = −2,2 ; 28/07 z = −2,8 ; 29/07 z = −2,7), quatre depuis le 22/07 ; volume 1,29 fois la moyenne — persistance réelle, ampleur modérée.
Cours à 4 % du canal 120 s : plancher de l'encadrement, dont la largeur a doublé (0,68 € en juin, 1,31 € aujourd'hui, soit 15,6 %).
Support convexe à 2 touches seulement (07/03 et 28/07), niveau 7,61 € : droite non confirmée ; résistance courte descendante à 7,88 €, 10 touches, mais portée 18 séances.
Une clôture sous 7,61 € supprimerait le dernier appui de la fenêtre ; au-dessus de 7,88 €, la pente courte de −0,58 %/séance serait invalidée.

## 2022-08-31
### AIR.PA
Les trois horizons ne concordent pas : 120 s = −0,029 €/s, p = 0,020 mais R² = 0,045 et IC₉₅ [−0,054 ; −0,005] — pente longue à peine distincte de zéro ; 60 s = +0,196 €/s (R² = 0,44) ; 20 s = −0,341 €/s (−0,361 %/s), p = 0,0020.
Cours à 44 % du canal 120 s (largeur 20,76 €, 21,6 %) et à 10 % du canal 20 s.
Support convexe ascendant +0,203 €/s (+0,223 %/s), portée 41 séances (05/07 → 31/08), mais **2 touches seulement** : droite non confirmée, niveau 91,05 €, le cours clôture 0,1 % dessus.
Résistance −0,035 €/s, portée 56 séances, 5 touches (27, 30/05, 06/06, 16 et 17/08), niveau 102,95 € : cours 11,5 % dessous. Volume du jour 2,26 fois la moyenne 20 s.
Une clôture sous 91,0 € laisserait la fenêtre sans support constitué jusqu'au plus-bas du 05/07 (82,74 €).

### MC.PA
TEND_120 est repassé à +1 : 120 s = +0,462 €/s (+0,077 %/s), p = 8,3·10⁻⁶, R² = 0,16 ; 60 s = +2,562 €/s (+0,391 %/s), R² = 0,85 ; mais 20 s = −1,394 €/s (−0,225 %/s), p = 0,0060 — l'été monte, le mois d'août rend.
Cours à 53 % du canal 120 s (largeur 140,45 €, 24,7 %) et à 0 % du canal 20 s : bord bas exact de l'encadrement court.
Support convexe ascendant +1,995 €/s (+0,334 %/s), portée 50 séances (22/06 → 31/08), 10 touches, niveau 597,03 € : le cours clôture exactement dessus.
Résistance +0,377 €/s, portée 100 séances (29/03 → 18/08), 14 touches, niveau 656,58 € : cours 9,1 % dessous ; plus-haut 120 s le 18/08 à 653,18 €.
Une clôture sous 597 € romprait un support à 10 touches, seul appui de la fenêtre depuis le 22/06.

### OR.PA
Pente longue redevenue nulle : 120 s = +0,059 €/s, p = 0,198, IC₉₅ [−0,031 ; +0,149], TEND_120 = 0 ; 60 s = +0,856 €/s (R² = 0,72) ; 20 s = −0,748 €/s (−0,228 %/s), p = 7,2·10⁻⁴.
Cours à 54 % du canal 120 s (largeur 66,01 €, 20,7 %) et à 10 % du canal 20 s.
Support convexe ascendant +0,668 €/s (+0,211 %/s), portée 54 séances (16/06 → 31/08), 7 touches dont le 30/08, niveau 317,14 € : cours 1,3 % dessus, appui testé hier.
Résistance quasi horizontale +0,023 €/s, portée 81 séances, 11 touches, niveau 349,48 € : cours 8,1 % dessous, le plus-haut 120 s (348,95 €) reste celui du 29/07.
Une clôture sous 317 € romprait le support de l'été ; volume du jour 2,19 fois la moyenne 20 séances.

### SAN.PA
Inversion complète : la hausse longue de juin-juillet est éteinte, 120 s = −0,040 €/s (−0,051 %/s), p = 0,0022, R² = 0,077, TEND_120 passé de +1 à −1 ; 20 s = −0,691 €/s (−1,055 %/s), p = 6,0·10⁻⁶, R² = 0,69.
**Élargissement majeur** : σ_e(20) triplé, de 0,90 € à 2,68 € (× 2,99) ; le plus-bas des 120 séances a été inscrit le 11/08 à 64,19 €, contre 87,64 € le 25/05.
Le support ascendant du 29/07 (81,52 €, 11 touches) a été cassé ; la chaîne inférieure donne désormais une droite descendante −0,091 €/s, portée 105 séances, niveau 62,92 €.
Cours à 10 % du canal 120 s, mais à 93 % du canal 20 s — rebond technique à l'intérieur d'un canal court fortement baissier.
Une clôture au-dessus de 70,17 € invaliderait la résistance descendante à 7 touches formée depuis le 04/08.

### BNP.PA
Aucune direction lisible : 120 s = −0,012 €/s, p = 0,025, R² = 0,042, IC₉₅ [−0,023 ; −0,002] — significative mais sans portée pratique ; 60 s = +0,006 €/s, p = 0,68 ; 20 s = −0,151 €/s (−0,423 %/s), p = 1,7·10⁻⁴.
Canal 120 s large de 9,79 €, soit 26,6 % du niveau moyen ; cours à 47 % de hauteur, z = −0,07 : milieu, encadrement peu contraignant.
Support convexe ascendant +0,108 €/s (+0,308 %/s), portée 31 séances (15/07 → 29/08), 3 touches : crédible mais jeune, niveau 34,98 €.
Résistance −0,054 €/s (−0,140 %/s), portée 57 séances (30/05 → 17/08), 7 touches dont 12, 15, 16 et 17/08, niveau 38,69 €.
Une clôture sous 34,98 € ou au-dessus de 38,69 € trancherait un encadrement aujourd'hui indécis ; entre les deux, rien n'est décidable.

### TTE.PA
Seule valeur de l'univers dont les deux horizons montent : 120 s = +0,042 €/s (+0,101 %/s), p = 1,1·10⁻¹², R² = 0,35 ; 20 s = +0,178 €/s (+0,414 %/s), p = 1,4·10⁻⁴, R² = 0,56.
Le cours sort par le bas du canal 20 s ce jour même (z = −2,96, volume 1,66 fois la moyenne), mais **une seule séance sans persistance : ce n'est pas une rupture**, c'est un écart à noter.
Cours à 25 % du canal 120 s (largeur 8,80 €, 22,4 %) et 0 % du canal 20 s.
Support convexe court +0,108 €/s, portée 18 séances seulement sur 60 : sous le seuil du quart de fenêtre, non extrapolable ; l'appui robuste est celui de la fenêtre 120 s, +0,033 €/s, 5 touches, niveau 37,55 €.
Une deuxième clôture sous 39,81 € changerait le statut de la séance du jour ; résistance à 43,56 €, 7 touches dont 23-29/08.

### SU.PA
Le rebond de juillet est effacé : 120 s = −0,158 €/s (−0,141 %/s), p = 8,3·10⁻¹¹, R² = 0,30 ; 60 s = +0,299 €/s ; 20 s = −0,635 €/s (−0,547 %/s), p = 1,1·10⁻⁴, R² = 0,57.
Cours à 48 % du canal 120 s (largeur 29,49 €, 24,4 %) mais à 0 % du canal 20 s : bord bas exact de l'encadrement court ; aucune sortie au-delà de 2 σ_e sur la fenêtre longue.
Support convexe ascendant +0,195 €/s (+0,176 %/s), portée 34 séances (14/07 → 31/08), 11 touches, niveau 110,74 € : le cours clôture 0,2 % dessus.
Résistance −0,150 €/s (−0,118 %/s), portée 95 séances (05/04 → 18/08), 13 touches, niveau 127,27 € : cours 12,8 % dessous. Volume du jour 2,68 fois la moyenne, le plus élevé de l'univers.
Une clôture sous 110,7 € romprait un support à 11 touches, sans autre appui identifié dans la fenêtre avant le plus-bas du 22/06 (102,77 €).

### AI.PA
La pente longue, nulle fin juillet, est redevenue nettement négative : 120 s = −0,102 €/s (−0,103 %/s), p = 1,2·10⁻¹⁴, R² = 0,40 ; 20 s = −0,303 €/s (−0,305 %/s), p = 5,5·10⁻⁴ ; 60 s = +0,001 €/s, p = 0,97 — trois mois strictement plats.
Cours à 35 % du canal 120 s (largeur 19,34 €, 18,3 %) et à 0 % du canal 20 s.
Support convexe ascendant +0,052 €/s, portée 41 séances (05/07 → 31/08), 8 touches (05, 06, 13, 14, 15, 19/07 puis 31/08), niveau 96,03 € : le cours clôture exactement sur la droite.
Résistance −0,228 €/s (−0,220 %/s), portée 54 séances (06/06 → 19/08), 7 touches dont 15 au 19/08, niveau 103,53 € : cours 7,2 % dessous.
Une clôture sous 96,0 € romprait un support à 8 touches ; l'encadrement se referme entre 96 et 103,5 €.

### DG.PA
Aucune direction affirmable à l'un ou l'autre bout : 120 s = +0,011 €/s, p = 0,087, IC₉₅ [−0,002 ; +0,024] qui change de signe ; 20 s = −0,056 €/s, p = 0,096 ; seul le 60 s tranche, +0,144 €/s (+0,179 %/s), R² = 0,73.
Canal 120 s le plus étroit après ORA : 10,18 €, soit 13,3 % du niveau moyen ; cours à 74 % de hauteur, 40 % du canal 20 s.
Support convexe ascendant +0,162 €/s (+0,209 %/s), portée 39 séances (05/07 → 29/08), 3 touches, niveau 77,42 € : cours 1,7 % dessus.
Résistance quasi horizontale +0,013 €/s, portée 79 séances (28/04 → 17/08), 5 touches, niveau 81,75 € ; plus-haut 120 s le 17/08 à 81,62 €.
Une sortie de la bande 77,4-81,8 €, dans un sens ou dans l'autre, serait le premier fait graphique lisible ; à l'intérieur, l'encadrement ne dit rien.

### CAP.PA
La meilleure droite courte de l'univers, orientée à la baisse : 20 s = −0,775 €/s (−0,482 %/s), p = 5,4·10⁻⁸, R² = 0,81 ; 120 s = −0,120 €/s (−0,076 %/s), p = 2,8·10⁻⁷, R² = 0,20 ; 60 s = +0,310 €/s.
σ_e(20) divisé par deux (4,37 € → 2,14 €) : repli ordonné, peu dispersé ; cours à 59 % du canal 120 s mais 3 % du canal 20 s.
Support convexe ascendant +0,427 €/s (+0,271 %/s), portée 41 séances (05/07 → 31/08), 7 touches dont 29 et 30/08, niveau 157,86 € : le cours clôture dessus au centime près, troisième contact en trois séances.
Résistance −0,108 €/s, portée 86 séances (04/04 → 04/08), 11 touches, niveau 174,61 € : cours 9,6 % dessous.
Une clôture sous 157,9 € romprait le support de l'été au moment même où il est testé trois jours de suite.

### RI.PA
Pente longue redevenue nulle : 120 s = −0,020 €/s, p = 0,29, IC₉₅ [−0,058 ; +0,017], TEND_120 = 0 ; 60 s = +0,384 €/s (+0,232 %/s), R² = 0,77 ; 20 s = −0,367 €/s (−0,232 %/s), p = 5,1·10⁻⁴.
Cours à 55 % du canal 120 s (largeur 27,08 €, 17,4 %) et à 0 % du canal 20 s ; σ_e(20) presque doublé (× 1,76).
Support convexe ascendant +0,310 €/s (+0,201 %/s), portée 50 séances (22/06 → 31/08), 5 touches dont 29, 30 et 31/08, niveau 154,57 € : le cours clôture exactement dessus, troisième contact consécutif.
Résistance quasi plate −0,046 €/s, portée 89 séances (06/04 → 11/08), 17 touches — le plus grand nombre de contacts de l'univers —, niveau 165,08 € : cours 6,4 % dessous.
Une clôture sous 154,6 € romprait le support ascendant de l'été ; au-dessus de 165,1 €, c'est un plafond à 17 touches qui céderait.

### ORA.PA
Retournement long confirmé : 120 s = −0,0032 €/s (−0,039 %/s), p = 3,5·10⁻⁴, R² = 0,10, TEND_120 passé à −1 — la pente était +0,0101 €/s avec R² = 0,76 fin juin ; 20 s = +0,0043 €/s, p = 0,24, plat.
Cours à 27 % du canal 120 s (largeur 1,11 €, 13,3 %) et 16 % du canal 20 s ; **aucune sortie au-delà de 2 σ_e** sur la fenêtre : la rupture basse de fin juillet est résorbée.
Résistance convexe descendante −0,0223 €/s (−0,279 %/s), portée 42 séances (04/07 → 31/08), 10 touches dont 17 au 23/08, niveau 8,00 € : cours 1,4 % dessous.
Support convexe −0,0032 €/s, portée 95 séances (15/03 → 28/07), 8 touches, niveau 7,53 € : cours 4,9 % dessus ; plus-bas 120 s le 28/07 à 7,61 €.
Une clôture au-dessus de 8,00 € casserait la résistance de juillet-août ; l'encadrement se resserre entre 7,53 et 8,00 €.
## 2022-09-30
### AIR.PA
Tendance longue baissière et significative : pente 120 séances de −0,079 €/séance (−0,084 %/séance), p = 4,3 × 10⁻⁸, R² = 0,225, IC₉₅ [−0,105 ; −0,052] ; tendance courte baissière et beaucoup plus raide, −0,463 €/séance (−0,53 %/séance), R² = 0,826.
Encadrement convexe sur 120 séances : support ancré au 05/07/2022 de pente −0,032 €/séance, à 80,71 € ce jour ; résistance ancrée au 30/05/2022, pente −0,035 €/séance, à 102,17 € ; largeur 21,46 € soit 23,5 % du niveau moyen.
Le cours clôture à 82,72 €, position 9,4 % de la hauteur du canal, contre le support — descente continue depuis 70 % le 25/08.
Le support est confirmé, quatre épisodes de contact : 23/06, 30/06, 05/07 et 28-30/09, ce dernier en cours ; la résistance en compte trois (27-30/05, 06-08/06, 16-17/08).
Configuration à surveiller : une clôture sous 80,7 € invaliderait ce support à quatre épisodes, le plus bas des 120 séances (81,98 €) étant déjà entamé.

### MC.PA
Divergence des deux horizons : pente 120 séances de +0,669 €/séance (+0,117 %/séance), p = 1,2 × 10⁻¹¹, R² = 0,324, contre une pente 20 séances de −2,198 €/séance (−0,38 %/séance), R² = 0,600 — les critères 1 et 2 sont de signes opposés.
Encadrement ascendant : support de pente +0,756 €/séance ancré au 16/06/2022 (portée 74 séances), à 550,78 € ; résistance de pente +0,622 ancrée au 21/04, à 672,45 € ; largeur 121,67 €, soit 19,9 %.
Clôture 562,82 €, position 9,9 % : le cours est venu au contact du support après avoir été à 80 % le 22/08.
Le support ne compte que deux épisodes (14-23/06 et 23-30/09) : droite non confirmée, à traiter comme une contrainte géométrique et non comme une figure ; la résistance en a trois.
Un retour sous 550,8 € romprait un support qui ne tient qu'à deux points de contact.

### OR.PA
Pente longue positive mais peu explicative : +0,183 €/séance (+0,058 %/séance), p = 6,7 × 10⁻⁶, R² = 0,158 ; pente courte franchement négative, −1,161 €/séance (−0,37 %/séance), R² = 0,715.
Canal convergent : support +0,243 €/séance à 299,57 € (portée 74, deux épisodes seulement), résistance −0,330 €/séance à 334,08 € (portée 32, trois épisodes) ; largeur 34,51 € soit 10,9 %, refermeture théorique en 60 séances.
Clôture 308,96 €, position 27,2 %, dans le tiers bas après un contact du support les 28-30/09.
La convergence des deux droites, et non le cours, est le fait dominant : le canal perd 0,57 € de hauteur par séance.
Une clôture sous 299,6 €, ou au-dessus de 334,1 €, résoudrait un encadrement qui se referme de lui-même d'ici deux à trois mois.

### SAN.PA
La droite longue est la plus nette du panier : −0,164 €/séance (−0,210 %/séance), p = 3,7 × 10⁻³⁰, R² = 0,670 ; la pente courte confirme, −0,169 €/séance (−0,25 %/séance).
L'encadrement convexe est ici sans contenu : largeur 1,72 €, soit 2,6 % du niveau, avec une résistance en pente −0,400 €/séance contre un support à +0,015 — refermeture en 4,1 séances.
La position affichée de 64,4 % dans un canal de 2,6 % ne distingue rien ; c'est le pincement qu'il faut lire, pas la position.
Le cours clôture à 65,83 €, au plus bas des 120 séances (65,02 € atteint), après −21,1 % en 60 séances.
La configuration impose une sortie mécanique du canal en moins d'une semaine de bourse, par le haut ou par le bas.

### BNP.PA
Baisse longue significative mais très faiblement explicative : −0,014 €/séance (−0,039 %/séance), p = 0,010, R² = 0,055 — la droite n'explique que 5 % du mouvement ; pente courte −0,170 €/séance (−0,46 %/séance), R² = 0,291, IC₉₅ [−0,301 ; −0,039] qui frôle zéro.
Encadrement : support +0,020 €/séance à 32,53 €, résistance −0,038 €/séance à 38,96 € (portée 76, trois épisodes) ; largeur 6,43 €, soit 18,0 %.
Clôture 33,70 €, position 18,2 %, après avoir touché 94 % le 12/09 : l'aller-retour d'un bord à l'autre a pris treize séances.
Le support n'a que deux épisodes de contact (14-15/07 et 29-30/09) : il n'est pas confirmé.
Une clôture sous 32,5 € invaliderait cette ligne basse ; à ce stade la largeur du canal, 18 %, rend toute lecture de position peu contraignante.

### TTE.PA
Tendance longue indiscernable du bruit : pente +0,009 €/séance, p = 0,094, R² = 0,024, IC₉₅ [−0,0015 ; +0,0196] qui contient zéro — aucune affirmation directionnelle n'est possible sur 120 séances.
Tendance courte baissière et nette : −0,150 €/séance (−0,38 %/séance), R² = 0,606.
Encadrement légèrement convergent : support +0,024 €/séance à 37,28 € (portée 109, trois épisodes : 25-27/04, 14/07, 23-29/09), résistance −0,025 €/séance à 43,01 € (deux épisodes) ; largeur 5,72 € soit 14,3 %.
Clôture 38,93 €, position 28,8 %, remontée de 6 % le 23/09 à 29 % le 30/09.
Une clôture sous 37,3 € romprait le seul côté crédible de l'encadrement, celui à trois épisodes.

### SU.PA
Baisse longue significative mais marginale en explication : −0,061 €/séance (−0,052 %/séance), p = 0,0011, R² = 0,086 ; baisse courte plus marquée, −0,489 €/séance (−0,44 %/séance), R² = 0,406.
Le support est la droite la mieux installée du dossier : pente +0,015 €/séance, à 103,84 €, quatre épisodes de contact (22-23/06, 30/06-05/07, 14/07, 21-29/09).
La résistance, à 125,84 € et de pente −0,090, n'a que deux épisodes (21/04, 15-19/08) : elle n'est pas confirmée.
Clôture 109,23 €, position 24,5 %, largeur du canal 21,99 € soit 19,2 % — le cours évolue dans le quart bas depuis le 16/09.
Une clôture sous 103,8 € invaliderait un support à quatre épisodes, seul élément structurant de la figure.

### AI.PA
Baisse longue très nette : −0,176 €/séance (−0,171 %/séance), p = 1,4 × 10⁻³⁴, R² = 0,722 — la droite explique près des trois quarts du mouvement sur 120 séances ; la pente courte, −0,296 €/séance (−0,32 %/séance), va dans le même sens.
Canal descendant des deux côtés : support −0,096 €/séance à 87,87 € (trois épisodes : 05-06/07, 14/07, 21-30/09), résistance −0,228 €/séance à 98,52 € (deux épisodes seulement) ; largeur 10,66 €, soit 11,4 %.
Clôture 90,17 €, position 21,6 %, à 1,4 € du plus bas des 120 séances (88,74 €).
Le contact bas est en cours depuis le 21/09, sans écart supérieur à 2 σ_e sur les dix dernières séances : pas de rupture, une pression.
Une clôture sous 87,9 € romprait le support ; la pente de celui-ci étant négative, le canal accompagne la baisse plutôt qu'il ne la freine.

### DG.PA
La tendance longue est nulle au sens du test : pente +0,007 €/séance, p = 0,358, IC₉₅ [−0,008 ; +0,022] — rien à affirmer sur 120 séances ; en revanche la pente courte est franche, −0,606 €/séance (−0,79 %/séance), R² = 0,778.
Encadrement large et quasi horizontal : support −0,017 €/séance à 69,45 €, avec cinq épisodes de contact (14/06, 22/06, 05/07, 26/09, 29/09) ; résistance +0,023 €/séance à 83,16 €, deux épisodes ; largeur 13,71 €, soit 18,0 %.
Clôture 71,01 €, position 11,4 %, effondrée depuis 96 % le 12/09 — l'amplitude complète du canal parcourue en treize séances.
Débordement bas du canal de régression : trois séances consécutives au-delà de −2 σ_e (26, 29 et 30/09, jusqu'à −2,4 σ), avec un volume à 1,24 fois la moyenne 20 séances — persistance réelle, mais ampleur modeste.
Une clôture sous 69,45 € invaliderait le support à cinq épisodes, la seule structure installée de la figure.

### CAP.PA
Baisse longue significative, explication faible : −0,101 €/séance (−0,063 %/séance), p = 1,2 × 10⁻⁵, R² = 0,151 ; baisse courte marquée, −1,121 €/séance (−0,73 %/séance), R² = 0,662, mais sensible — retirer la seule séance du 30/09 la porte à −1,267.
Encadrement : support −0,024 €/séance à 138,85 € (deux épisodes : 04-05/07 et 23-28/09), résistance −0,061 €/séance à 174,14 € (trois épisodes) ; largeur 35,29 €, soit 22,6 % — le canal est trop large pour contraindre quoi que ce soit à court terme.
Clôture 151,01 €, position 34,5 %, remontée de 7 % le 23/09.
Les deux droites sont quasi parallèles, la refermeture théorique est hors de portée (938 séances).
Une clôture sous 138,9 € invaliderait un support qui ne repose que sur deux épisodes de contact.

### RI.PA
Tendance longue haussière mais tout juste significative : +0,039 €/séance (+0,025 %/séance), p = 0,020, R² = 0,045, IC₉₅ [+0,006 ; +0,073] dont la borne basse frôle zéro ; tendance courte non significative, p = 0,171, IC₉₅ [−0,245 ; +0,047] à cheval sur zéro.
Canal convergent, refermeture théorique en 51 séances : support +0,193 €/séance à 152,93 € (deux épisodes), résistance −0,034 €/séance à 164,50 € (trois épisodes) ; largeur 11,56 €, soit 7,3 % — le canal le plus étroit du panier après SAN.PA.
Clôture 159,03 €, position 52,7 % : milieu de canal exact, après un rebond depuis 21 % le 29/09.
Aucune des deux tendances ne permet d'affirmation directionnelle ; seule la géométrie du pincement est lisible.
Une clôture sous 152,9 € ou au-dessus de 164,5 € trancherait une figure que le test de Student ne tranche pas.

### ORA.PA
Baisse longue parmi les plus nettes du panier : −0,0104 €/séance (−0,125 %/séance), p = 1,1 × 10⁻³⁴, R² = 0,723 ; baisse courte encore plus raide, −0,0377 €/séance (−0,49 %/séance), R² = 0,820.
Le cours clôture à 7,229 €, exactement au plus bas des 120 séances, à −1,97 σ_e de la droite ajustée, position 2,5 % dans un canal de 0,64 € (8,5 %).
Support à 7,21 € de pente −0,0055 €/séance, mais deux épisodes seulement (02/05 et 29-30/09) : la ligne basse n'est pas confirmée ; résistance à 7,85 €, deux épisodes également.
Le volume de la séance vaut 1,73 fois la moyenne 20 séances — le plus élevé du panier ce jour, sur un point bas.
Une clôture sous 7,21 € ferait sortir le cours par le bas d'un encadrement déjà orienté à la baisse des deux côtés.

## 2022-10-31
### AIR.PA
Les deux horizons s'opposent : pente 120 séances toujours négative, −0,056 €/séance (−0,060 %/séance), p = 2,8 × 10⁻⁴, R² = 0,106 ; pente 20 séances fortement positive, +0,858 €/séance (+0,93 %/séance), R² = 0,919, p = 2,8 × 10⁻¹¹, soit +22,8 % en vingt séances.
Clôture 101,97 €, position 98,3 % : le cours est collé à la résistance, à 102,35 €, de pente −0,027 €/séance et de portée 110 séances.
Cette résistance est désormais une structure installée, quatre épisodes : 27-30/05, 06-08/06, 16-17/08 et 28-31/10.
Le canal de régression déborde par le haut : deux séances au-dessus de +2 σ_e (28/10 à +2,2 σ, 31/10 à +2,1 σ), volume à 1,02 fois la moyenne — débordement court et sans volume, à ne pas compter comme une rupture.
Une clôture au-dessus de 102,4 € constituerait un franchissement d'une droite à quatre points de contact ; en deçà, le 31/10 reste un contact de plus.

### MC.PA
Les deux pentes sont positives : +0,607 €/séance sur 120 séances (+0,105 %/séance), p = 1,7 × 10⁻¹⁰, R² = 0,293 ; +1,277 €/séance sur 20 (+0,218 %/séance), mais p = 0,013 et R² = 0,299 seulement, IC₉₅ [+0,31 ; +2,24] très large.
Le fait dominant est le resserrement de l'encadrement : la largeur passe de 121,67 € au 30/09 à 53,26 € au 31/10, soit 9,1 % du niveau, la résistance ayant basculé sur une arête descendante (−0,841 €/séance, ancrée au 19/08, portée 49) face à un support ascendant (+0,654).
La refermeture théorique intervient dans 35,6 séances : le canal est convergent, sa lecture a une date de péremption.
Clôture 589,19 €, position 60,9 %, après un contact de la résistance les 25-27/10 ; le support compte trois épisodes, la résistance deux.
Une clôture au-dessus de 610 € sortirait par le haut avant la refermeture ; sinon la convergence tranchera d'elle-même d'ici mi-décembre.

### OR.PA
La tendance longue est repassée à zéro au sens du test : pente +0,080 €/séance, p = 0,056, IC₉₅ [−0,002 ; +0,162] qui contient zéro — un mois plus tôt elle était déclarée haussière, l'inversion tient à peu.
Tendance courte baissière et nette : −0,948 €/séance (−0,31 %/séance), R² = 0,635.
Encadrement convergent (refermeture théorique en 116 séances) : support quasi horizontal à 284,59 €, quatre épisodes (19/05, 25/05, 14-17/06, 25/10) ; résistance −0,330 €/séance à 327,15 €, trois épisodes.
Clôture 297,59 €, position 30,5 %, dans le tiers bas d'un canal large de 42,56 € (13,9 %).
Une clôture sous 284,6 € invaliderait un support désormais confirmé par quatre épisodes.

### SAN.PA
Tendance longue baissière, la mieux ajustée du panier : −0,188 €/séance (−0,248 %/séance), p = 3,6 × 10⁻³⁹, R² = 0,767 ; tendance courte haussière, +0,231 €/séance (+0,34 %/séance), R² = 0,675 — signes opposés.
Le rebond de +9,4 % en vingt séances porte la clôture à 73,32 €, soit +2,46 σ_e au-dessus de la droite ajustée, l'écart le plus grand du panier.
Position 93,1 % : le cours est sur la résistance, 73,94 €, de pente −0,161 €/séance, dont il constitue le quatrième épisode de contact (18-20/07, 26-29/07, 03-08/08, 28-31/10).
Deux séances consécutives au-dessus de +2 σ_e (28/10 : +2,1 σ ; 31/10 : +2,5 σ), volume à 1,15 fois la moyenne : débordement naissant du canal de régression, encore trop court pour être qualifié de rupture.
Une clôture au-dessus de 73,9 € franchirait une résistance à quatre épisodes en contradiction directe avec une droite longue à R² = 0,77.

### BNP.PA
Tendance longue baissière, mieux marquée qu'un mois plus tôt : −0,029 €/séance (−0,078 %/séance), p = 4,4 × 10⁻⁷, R² = 0,195 ; tendance courte haussière et nette, +0,187 €/séance (+0,53 %/séance), R² = 0,687.
Clôture 36,71 €, position 96,1 % : le cours est sur la résistance à 36,89 €, de pente −0,075 €/séance et de portée 34 séances, dont il forme le troisième épisode (12-15/09, 20/09, 25-31/10).
Le support, à 32,23 €, compte trois épisodes également ; largeur du canal 4,66 €, soit 13,5 %, en réduction depuis 18,0 % au 30/09.
Le canal est convergent, refermeture théorique en 54 séances.
Une clôture au-dessus de 36,9 € franchirait la résistance ; à défaut, le cours reste dans un canal qui se resserre à 0,086 € par séance.

### TTE.PA
Tendance longue strictement nulle au sens du test : pente +0,002 €/séance, p = 0,689, R² = 0,001, IC₉₅ [−0,008 ; +0,011] — sur 120 séances, aucune direction n'est établie.
Tendance courte haussière et nette : +0,151 €/séance (+0,36 %/séance), R² = 0,659.
La clôture, 44,44 €, est le plus haut des 120 séances ; position 92,5 %, résidu +2,00 σ_e, exactement à la limite du canal de déviation standard.
La résistance, à 44,99 €, est quasi horizontale (−0,0005 €/séance) et de portée 102 séances, mais ne compte que deux épisodes (09/06 et 28-31/10) : droite non confirmée, à ne pas lire comme une figure.
Une clôture au-dessus de 45,0 € porterait le cours au-delà d'une borne qui n'a été testée que deux fois en six mois.

### SU.PA
Tendance longue nulle : pente +0,006 €/séance, p = 0,738 — la droite 120 séances n'apporte rien ; tendance courte haussière, +0,526 €/séance (+0,45 %/séance), R² = 0,636.
Le support, à 104,17 €, compte six épisodes de contact (22-23/06, 30/06-05/07, 14/07, 21-23/09, 28/09, 03/10) : c'est la structure la mieux installée du panier ce jour.
La résistance, à 124,62 € et de pente −0,077 €/séance, n'a que deux épisodes (16-19/08, 25-26/10) et n'est pas confirmée.
Clôture 119,80 €, position 76,5 %, après un pic à 95 % le 26/10 ; largeur 20,45 €, soit 17,9 %.
Une clôture au-dessus de 124,6 € sortirait par le haut, un retour sous 104,2 € invaliderait un support à six épisodes.

### AI.PA
Tendance longue toujours baissière et bien ajustée : −0,153 €/séance (−0,153 %/séance), p = 2,7 × 10⁻²⁴, R² = 0,585 ; tendance courte haussière, +0,595 €/séance (+0,63 %/séance) — signes opposés.
Clôture 101,48 €, position 92,0 %, sur une résistance à 102,83 € de pente −0,141 €/séance, mais qui ne compte que deux épisodes (06/06 et 25-31/10).
Débordement le plus net du panier : cinq séances consécutives au-dessus de +2 σ_e, du 25 au 31/10, de +2,2 à +2,6 σ — la persistance est là, mais le volume de la dernière séance ne vaut que 0,82 fois la moyenne 20 séances.
Le support, à 85,85 €, compte quatre épisodes et reste la seule droite confirmée.
Une clôture au-dessus de 102,8 € porterait le cours au-dessus d'un encadrement dont les deux droites descendent encore.

### DG.PA
Tendance longue nulle : pente −0,005 €/séance, p = 0,573, IC₉₅ [−0,022 ; +0,012] ; tendance courte haussière et très ajustée, +0,498 €/séance (+0,67 %/séance), R² = 0,818.
Clôture 79,55 €, position 97,4 %, contre une résistance à 79,84 € de pente −0,089 €/séance — mais deux épisodes seulement (12-13/09 et 27-31/10) : la borne haute n'est pas confirmée.
Le support, à 68,68 €, en compte six (14/06, 22/06, 05/07, 26/09, 03/10, 06-10/10) : la dissymétrie entre les deux côtés est complète.
Largeur 11,17 €, soit 15,0 % ; le cours a parcouru 2 % à 97 % de la hauteur en dix-sept séances.
Une clôture au-dessus de 79,8 € franchirait la résistance ; le passage de 2 % à 97 % du canal en trois semaines dit surtout que la largeur retenue est peu contraignante.

### CAP.PA
Tendance longue baissière et faible : −0,073 €/séance (−0,046 %/séance), p = 9,0 × 10⁻⁴, R² = 0,090 ; tendance courte non significative, p = 0,397, IC₉₅ [−0,211 ; +0,509] à cheval sur zéro — aucune direction courte affirmable.
Encadrement convergent (refermeture en 78 séances) : support −0,024 €/séance à 138,35 € (trois épisodes), résistance −0,290 €/séance à 159,18 € (quatre épisodes, dont 25-31/10) ; largeur 20,82 €, soit 14,0 %, contre 22,6 % un mois plus tôt.
Clôture 151,70 €, position 64,1 %, en repli depuis 94 % le 26/10.
La résistance, à quatre épisodes, est la droite la mieux établie ; elle descend de 0,29 € par séance.
Une clôture au-dessus de 159,2 € franchirait cette droite ; en deçà, le canal continue de se pincer de 0,27 € par séance.

### RI.PA
Tendance longue haussière et faible : +0,052 €/séance (+0,034 %/séance), p = 9,7 × 10⁻⁴, R² = 0,088 ; tendance courte baissière et nette, −0,412 €/séance (−0,27 %/séance), R² = 0,480 — signes opposés.
Encadrement ascendant et divergent : support +0,057 €/séance à 144,34 €, quatre épisodes (16-22/06, 13/10, 21-24/10, 28/10) ; résistance +0,077 €/séance à 170,10 €, trois épisodes ; largeur 25,76 €, soit 16,4 %.
Clôture 149,64 €, position 20,6 %, avec trois contacts du support en trois semaines — la partie basse du canal est activement testée.
Le canal ne se referme pas : les deux pentes divergent légèrement, aucune date de péremption.
Une clôture sous 144,3 € invaliderait un support à quatre épisodes, le seul élément confirmé de la figure.

### ORA.PA
Tendance longue baissière, la plus significative de l'univers : −0,0139 €/séance (−0,172 %/séance), p = 7,0 × 10⁻⁵⁷, R² = 0,883 ; tendance courte haussière, +0,0118 €/séance (+0,16 %/séance), R² = 0,489.
Clôture 7,528 €, position 95,1 %, sur une résistance à 7,56 € de pente −0,016 €/séance et de portée 85 séances, dont c'est le troisième épisode (29/06-05/07, 12-16/09, 28-31/10).
Le support, à 6,94 € et de pente −0,010 €/séance, compte trois épisodes également : les deux côtés sont confirmés, et tous deux descendent.
Le résidu vaut +1,69 σ_e : rebond marqué à l'intérieur d'un canal descendant, sans débordement.
Une clôture au-dessus de 7,56 € franchirait une résistance à trois épisodes, en contradiction avec une droite longue à R² = 0,88.

## 2022-11-30
### AIR.PA
Retournement du verdict long : la pente 120 séances passe à +0,093 €/séance (+0,099 %/séance), p = 1,7 × 10⁻⁷, R² = 0,207, après deux mois de verdict baissier ; la pente courte n'est plus significative, p = 0,053, IC₉₅ [−0,276 ; +0,002].
L'encadrement s'est effondré en largeur : 8,23 €, soit 7,8 % du niveau, contre 24,7 % au 31/10, avec un support ascendant de +0,482 €/séance (portée 40, deux épisodes) et une résistance de +0,074 (trois épisodes).
Refermeture théorique en 20,2 séances : la figure a une date de péremption courte.
Clôture 101,62 €, position 10,7 %, après un décrochage brutal — de 78 % le 22/11 à 1 % le 28/11, soit toute la hauteur du canal en trois séances.
Une clôture sous 100,7 € romprait un support qui ne repose que sur deux épisodes ; à défaut, la convergence tranchera avant fin décembre.

### MC.PA
Les deux horizons concordent à la hausse : +0,611 €/séance sur 120 séances (+0,103 %/séance), p = 1,2 × 10⁻¹⁰, R² = 0,298 ; +3,037 €/séance sur 20 (+0,48 %/séance), R² = 0,645.
La clôture, 679,83 €, est le plus haut des 120 séances et se pose exactement sur la résistance (679,83 €), droite ascendante de +0,360 €/séance et de portée 74 séances, dont c'est le troisième épisode (04-08/08, 11-19/08, 30/11) — position 100,0 %.
Le support, +0,654 €/séance à 571,14 €, compte trois épisodes ; largeur 108,69 €, soit 17,4 %.
Le volume du 30/11 vaut 3,85 fois la moyenne 20 séances, le plus élevé du panier ce jour ; le résidu est de +1,54 σ_e, donc encore à l'intérieur du canal de régression.
Une clôture au-dessus de 679,8 € constituerait un franchissement d'une résistance à trois épisodes ; en deçà, le 30/11 n'est qu'un contact de plus.

### OR.PA
Tendance longue non significative : pente −0,061 €/séance, p = 0,119, IC₉₅ [−0,137 ; +0,016] ; tendance courte haussière et nette, +1,805 €/séance (+0,57 %/séance), R² = 0,704, soit +15,2 % en vingt séances.
Clôture 331,92 €, position 96,9 %, sur une résistance à 333,53 € de pente −0,175 €/séance, dont c'est le quatrième épisode (29/07-02/08, 05/08, 19/08, 28-30/11) : structure installée.
Le support, quasi horizontal à 281,36 €, compte trois épisodes ; largeur 52,17 €, soit 17,0 %.
Volume à 1,65 fois la moyenne 20 séances ; résidu +1,26 σ_e, sans débordement du canal de régression.
Une clôture au-dessus de 333,5 € franchirait une résistance testée quatre fois en quatre mois.

### SAN.PA
Tendance longue toujours baissière et bien ajustée, mais moins pentue qu'au 31/10 : −0,121 €/séance (−0,165 %/séance) contre −0,188, p = 1,2 × 10⁻¹⁶, R² = 0,443 ; tendance courte non significative, p = 0,383.
Clôture 72,61 €, position 77,0 %, sous une résistance à 74,77 € de pente −0,112 €/séance qui compte six épisodes de contact — la droite la plus confirmée du dossier, dont le dernier épisode court du 25 au 30/11.
Le support, à 65,35 €, en compte trois ; largeur 9,42 €, soit 13,5 %, canal convergent avec refermeture théorique en 74,7 séances.
Volume à 2,24 fois la moyenne 20 séances, résidu +1,31 σ_e : pas de débordement du canal de régression.
Une clôture au-dessus de 74,8 € franchirait une résistance à six épisodes, ce que quatre mois de séances n'ont pas fait.

### BNP.PA
Retournement du verdict long : la pente 120 séances passe à +0,032 €/séance (+0,087 %/séance), p = 3,4 × 10⁻⁸, R² = 0,228 ; la pente courte est nette, +0,147 €/séance (+0,37 %/séance), R² = 0,846.
L'encadrement n'a plus de contenu : largeur 0,85 €, soit 2,1 % du niveau, avec un support de +0,256 €/séance contre une résistance de +0,028 — refermeture théorique en 3,7 séances.
La position affichée, 43,6 %, ne distingue rien dans un canal de 2,1 % : la lire comme un milieu de canal serait une erreur de mesure.
La résistance compte quatre épisodes (21-23/06, 12-17/08, 18-21/11, 24-30/11), le support deux seulement.
La configuration impose une sortie mécanique de l'encadrement sous quatre séances, dans un sens ou dans l'autre.

### TTE.PA
Tendance longue haussière et solide : +0,063 €/séance (+0,153 %/séance), p = 4,2 × 10⁻²⁵, R² = 0,598 ; tendance courte haussière mais fragile, +0,071 €/séance, p = 0,017, R² = 0,280, et le retrait de la seule séance du 30/11 la ramène à +0,045 — conclusion courte suspendue à un point.
La clôture, 48,64 €, est le plus haut des 120 séances et se pose sur la résistance (48,74 €, pente +0,055, portée 119, quatre épisodes) ; position 95,9 %.
Le support, +0,199 €/séance à 46,16 €, monte plus vite que la résistance : canal convergent, refermeture en 17,9 séances, largeur réduite à 2,58 €, soit 5,4 %.
Volume à 1,85 fois la moyenne 20 séances, résidu +1,92 σ_e — juste sous le seuil de débordement.
Une clôture au-dessus de 48,7 € franchirait la résistance ; sinon le pincement résoudra la figure avant fin décembre.

### SU.PA
Les deux horizons sont haussiers : +0,138 €/séance sur 120 séances (+0,118 %/séance), p = 5,8 × 10⁻¹², R² = 0,332 ; +0,461 €/séance sur 20 (+0,36 %/séance), R² = 0,485.
Encadrement légèrement divergent, sans date de péremption : support +0,015 €/séance à 104,50 € (quatre épisodes), résistance +0,081 €/séance à 134,77 € (quatre épisodes) ; largeur 30,27 €, soit 25,3 % — le canal le plus large du panier.
Clôture 129,76 €, position 83,4 % : le cours longe la résistance depuis le 10/11 sans la franchir, épisode de contact de treize séances.
Volume à 1,99 fois la moyenne 20 séances ; aucun débordement au-delà de 2 σ_e sur les 120 séances.
Une clôture au-dessus de 134,8 € franchirait une résistance à quatre épisodes, longée sans succès depuis trois semaines.

### AI.PA
Tendance longue non significative : pente +0,009 €/séance, p = 0,491, IC₉₅ [−0,017 ; +0,036] ; tendance courte haussière et bien ajustée, +0,312 €/séance (+0,30 %/séance), R² = 0,719.
L'encadrement est en fermeture rapide : largeur 3,11 €, soit 2,9 % du niveau, support de +0,537 €/séance contre une résistance de +0,039 — refermeture théorique en 6,2 séances.
Clôture 106,02 €, position 0,0 % : le cours est exactement sur le support ascendant, deux séances après un contact de la résistance (24-29/11).
Les deux droites comptent quatre épisodes chacune, mais un canal de 2,9 % de largeur ne discrimine plus grand-chose.
La convergence force une résolution en une semaine et demie de bourse ; une clôture sous 106,0 € la produirait par le bas.

### DG.PA
Les deux horizons sont haussiers et confirmés : +0,047 €/séance sur 120 séances (+0,061 %/séance), p = 1,9 × 10⁻⁶, R² = 0,175 ; +0,181 €/séance sur 20 (+0,22 %/séance), R² = 0,822.
C'est le seul dossier du panier dont les deux bornes sont installées : support à 68,21 € avec cinq épisodes, résistance à 84,08 € (pente +0,022) avec cinq épisodes également, dont un contact long du 21 au 30/11.
Clôture 83,37 €, position 95,5 %, contre la borne haute depuis le 21/11 ; largeur 15,88 €, soit 20,9 %, canal légèrement divergent, sans date de péremption.
Volume à 1,96 fois la moyenne 20 séances, résidu +0,97 σ_e : aucune sortie du canal de régression.
Une clôture au-dessus de 84,1 € franchirait une résistance à cinq épisodes, la mieux documentée de l'univers ce jour.

### CAP.PA
Tendance longue non significative : pente −0,013 €/séance, p = 0,573, IC₉₅ [−0,057 ; +0,032] ; tendance courte haussière mais fragile, +0,707 €/séance (+0,44 %/séance), p = 0,006, R² = 0,350, et +0,876 si l'on retire la dernière séance.
Encadrement : support −0,024 €/séance à 137,84 € (trois épisodes), résistance −0,131 €/séance à 165,68 € (trois épisodes, dont 11-17/11 et 24-28/11) ; largeur 27,85 €, soit 18,3 %, refermeture théorique lointaine (260 séances).
Clôture 156,03 €, position 65,3 %, en repli depuis 96 % le 15/11 — deux contacts hauts manqués en trois semaines.
Volume à 2,34 fois la moyenne 20 séances ; aucun débordement au-delà de 2 σ_e sur la fenêtre.
Une clôture au-dessus de 165,7 € franchirait une résistance descendante testée trois fois ; un retour sous 137,8 € invaliderait le support.

### RI.PA
Tendance longue haussière mais à la limite du bruit : +0,032 €/séance (+0,021 %/séance), p = 0,035, R² = 0,037, IC₉₅ [+0,002 ; +0,062] dont la borne basse frôle zéro ; tendance courte nette, +0,510 €/séance (+0,33 %/séance), R² = 0,753.
Clôture 161,28 €, position 99,2 %, sur une résistance à 161,41 € de pente −0,055 €/séance, dont c'est le troisième épisode (08-22/08, 13/09, 24-30/11).
Le support, +0,057 €/séance à 145,59 €, compte quatre épisodes : canal convergent, refermeture théorique en 142 séances, largeur 15,82 € soit 10,3 %.
Volume à 2,02 fois la moyenne 20 séances, résidu +0,79 σ_e — le cours est sur sa borne haute sans excès par rapport à la droite ajustée.
Une clôture au-dessus de 161,4 € franchirait une résistance à trois épisodes, jamais dépassée depuis août.

### ORA.PA
Tendance longue baissière et fortement ajustée : −0,0098 €/séance (−0,125 %/séance), p = 6,3 × 10⁻²⁹, R² = 0,654 ; tendance courte haussière, +0,0071 €/séance (+0,09 %/séance), R² = 0,499 — signes opposés.
Clôture 7,636 €, position 86,4 %, contre une résistance à 7,78 € de pente −0,011 €/séance et de portée 104 séances, mais qui ne compte que deux épisodes (29/06-04/07 et 21-30/11) : droite non confirmée.
Le support, à 6,72 € et de pente −0,010 €/séance, compte quatre épisodes ; les deux droites descendent presque parallèlement, largeur 1,06 € soit 14,6 %.
Volume à 2,46 fois la moyenne 20 séances, le plus élevé du panier ce jour ; résidu +1,42 σ_e, sans débordement.
Une clôture au-dessus de 7,78 € porterait le cours au-dessus d'une borne testée seulement deux fois en six mois, dans une tendance longue qui reste baissière à R² = 0,65.
