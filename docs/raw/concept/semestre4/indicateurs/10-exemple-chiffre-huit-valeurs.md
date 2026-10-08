# Module 10 — Exemple chiffré : huit valeurs du CAC 40

**Prérequis :** les modules [1](01-l-ecart-a-l-opinion.md) à [9](09-assembler-la-sequence.md).
**Ce qu'on établit ici :** les dix indicateurs mesurés le même jour sur huit valeurs, puis lus jusqu'au verdict, y compris là où le verdict de la grille est faux et là où une case reste vide.

---

## 10.1 — La commande

```bash
python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py
```

Relevé du **8 octobre 2026**. Le script interroge Yahoo, la BCE, Eurostat, la
BRI et l'AMF, imprime le contexte, une fiche par valeur et la synthèse des
marqueurs. Tout ce qui suit en est tiré, sans aucun chiffre saisi à la main.

> ⚠️ **Le relevé ne se reproduit pas à l'identique.** Relancé le même jour,
> marché ouvert, il bouge sur la deuxième décimale ; relancé un mois plus tard,
> le consensus aura changé. Ce module enseigne une **lecture**, et c'est elle
> qu'il faut refaire sur le relevé du jour.

## 10.2 — Le contexte

| Indicateur | Grandeur | Valeur | Module |
|---|---|---|---|
| 2 — taux | taux de dépôt BCE | 2,50 %, +0,50 pt sur un an | [6](06-taux-et-credit.md) |
| | 10 ans AAA, pente 10 ans − 3 mois | 3,54 %, **+1,02 pt** | |
| | taux réel ex post | **−0,26 %** | |
| 3 — crédit | prêts aux entreprises, sur un an | **+4,2 %** (+3,0 % un an plus tôt) | [6](06-taux-et-credit.md) |
| | écart crédit/PIB, France | **−15,7 pt** | |
| | HYG − IEF, 13 semaines | +2,12 pt : écarts de crédit qui se resserrent | |
| 8 — change | EURUSD | 1,1199, −3,9 % sur un an | [7](07-change-croissance-inflation.md) |
| 9 — croissance et inflation | PIB réel, inflation | +1,2 %, **3,8 %** (2,2 % un an plus tôt) | [7](07-change-croissance-inflation.md) |

**Lecture.** Un resserrement monétaire qui reste accommodant en termes réels, une
inflation qui accélère, un crédit qui repart d'un niveau bas sans dépasser la
croissance nominale, et des marchés de crédit détendus. **Aucune des conditions
d'un boom du crédit n'est réunie** au niveau agrégé. Ce contexte est le même pour
les huit valeurs : il ne départage aucune d'entre elles.

## 10.3 — Le tableau de bord

| | AIR | MC | OR | SAN | TTE | BNP | SU | ORA |
|---|---|---|---|---|---|---|---|---|
| **1** révision 90 j, exercice en cours | +1,1 % | +1,4 % | −0,3 % | +0,9 % | **+7,2 %** | +1,7 % | **+4,3 %** | **+36,3 %** |
| **1** diffusion 30 j | +0,48 | **−0,58** | 0,00 | +0,14 | **+0,73** | +0,20 | −0,14 | +0,20 |
| **1** dispersion | 14 % | 7 % | 8 % | 9 % | 40 % | 11 % | 17 % | **88 %** |
| **4** PER | 24,85 | 17,54 | 31,71 | 22,00 | 11,30 | 7,97 | 30,74 | 13,38 |
| **4** croissance implicite | **+4,0 %** | +2,3 % | **+4,8 %** | +3,5 %ᵃ | −0,8 % | −4,5 % | **+4,7 %** | +0,5 % |
| **4** part du bénéfice, 3 ans | +23,6 | −19,4 | +8,7 | −2,3 | −36,1 | +28,8 | +18,7 | −138,3 |
| **4** part du multiple, 3 ans | +17,1 | **−44,6** | −14,0 | −33,4 | +61,0ᵇ | +11,3 | **+31,0** | +164,8ᵇ |
| **5** dette/EBITDA | 1,08 | 1,42 | 1,11 | 1,63 | 1,55 | —ᶜ | 2,14 | —ᵈ |
| **5** dynamique de la dette | −13,9 | −6,3 | **+40,1** | −0,0 | **+25,3** | —ᶜ | **+16,9** | —ᵈ |
| **6** marge op. contre sa moyenne | −0,3 | −2,6 | +0,3 | −1,6 | −3,1 | —ᶜ | +0,6 | −2,8 |
| **7** actions sur un an | +0,5 % | −0,8 % | −0,4 % | −1,8 % | +1,4 % | −2,0 % | +0,0 % | −0,8 % |
| **8** $b_F$ ($t$) | −0,48 (−1,86) | −0,20 (−0,72) | +0,32 (+1,31) | +0,27 (+1,01) | −0,39 (−1,41) | +0,16 (+0,66) | +0,40 (+1,44) | +0,12 (+0,51) |
| **10** positions courtes | 0 | 0 | 0 | 0 | 0,77 % | 0 | 0 | 0 |
| **10** volume relatif | 1,00 | 1,20 | 0,85 | 1,02 | 0,91 | 0,99 | 1,18 | 1,26 |

ᵃ sur le BPA comptable ; −4,0 % sur le BPA des activités que suit le consensus
([module 2](02-les-attentes-de-benefices.md)).
ᵇ bénéfice en baisse : paradoxe du PER cyclique ou effet de base
([module 3](03-le-prix-des-attentes.md)).
ᶜ banque : ni EBITDA, ni marge opérationnelle au sens du cours.
ᵈ sources discordantes, dette annuelle 7,5 Md€ contre 56,8 Md€ : cellule vide
([module 5](05-levier-et-dilution.md)).

## 10.4 — Les marqueurs

```
   valeur    B1  B2  B3  B4  boom    R1  R2  R3  bascule   change*
   AIR.PA     ·   ·   ·   ·   0/4     ·   ·   ·      0/3   non
   MC.PA      ·   ·   ·   ·   0/4     ·   ·   ·      0/3   non
   OR.PA      ·   ·   ✓   ·   1/4     ·   ·   ·      0/3   non
   SAN.PA     ·   ·   ·   ·   0/4     ·   ·   ·      0/3   non
   TTE.PA     ✓   ·   ✓   ·   2/4     ·   ·   ·      0/3   non
   BNP.PA     ·   ·   ?   ·   0/4     ·   ?   ·      0/3   non
   SU.PA      ✓   ✓   ✓   ·   3/4     ·   ·   ·      0/3   non
   ORA.PA     ✓   ·   ?   ·   1/4     ·   ·   ·      0/3   non
```

Aucun marqueur de bascule n'est allumé. Aucune valeur n'émet d'actions (B4). Aucune
sensibilité au change n'est établie après Holm.

## 10.5 — Valeur par valeur, jusqu'au verdict

Les règles du [§ 9.3](09-assembler-la-sequence.md), appliquées dans l'ordre, puis
la vérification que la grille exige.

### SU.PA — séquence candidate, canal de la dette

B1, B2, B3. Les révisions montent (+4,3 % et +6,8 % sur 90 jours), le multiple a
porté plus que le bénéfice sur trois ans (+31,0 contre +18,7 points, PER de 25,4 à
34,6), et la dette a crû de 20,6 % en 2025 (14,8 → 17,9 Md€) pour un EBITDA en
hausse de 3,6 %. La croissance implicite (+4,7 %) est exigeante, et le rendement
bénéficiaire passe sous le taux à 10 ans (−0,29 point).

**Ce qui reste à vérifier**, et que le script ne sait pas : ce qu'a financé la
dette. Une acquisition payée au prix fort serait le canal de Soros ; un
investissement de capacité ne le serait pas. Le canal des actions, lui, est
**fermé** : le nombre d'actions est stable.

**Ce que la configuration ne permet pas de dire.** Trois marqueurs sur quatre
parmi huit valeurs, c'est une configuration que le hasard produit environ une
fois sur cinq ([§ 9.4](09-assembler-la-sequence.md)). La lecture est une
**question bien posée**, pas une découverte. Sa forme utilisable est la thèse
réfutable de l'exercice E9.3.

### TTE.PA — séquence candidate pour la grille, rejetée à la vérification

B1 et B3 : la règle 2 s'applique. Et pourtant, les indicateurs eux-mêmes
réfutent la lecture réflexive :

- les révisions suivent le **prix du pétrole**, pas un jugement sur la société :
  dispersion de 40 %, bénéfice 2027 attendu **inférieur** à celui de 2026 ;
- le levier « monte » parce que l'**EBITDA baisse** (−8,1 %, de 42,3 à 38,9 Md€),
  la dette croissant de 17,2 % ;
- le multiple a doublé parce que le bénéfice de 2022 était exceptionnel : le
  paradoxe du PER cyclique.

**Verdict : aucune séquence réflexive identifiable** ; un cycle de matière
première. C'est l'exemple qui justifie le mot « candidate » : une règle
mécanique produit des faux positifs que seule la lecture des composantes
écarte.

### OR.PA — valorisation exigeante

Croissance implicite de 4,8 %, prime négative (−0,38 point), mais un multiple qui a
**baissé** sur trois ans (−14,0 points) : le marché paie L'Oréal moins cher qu'en
2023, tout en la payant cher. B3 est allumé (dette de 8,5 à 11,9 Md€, EBITDA
stable), sans B1 ni B2 : la règle 2 ne s'applique pas, la règle 3 si. La hausse
de la dette est à expliquer dans le rapport annuel, pour elle-même.

### AIR.PA — valorisation exigeante

Croissance implicite de 4,0 %, mais une hausse sur trois ans portée d'abord par
le **bénéfice** (+23,6 contre +17,1 points de multiple) : B2 éteint. Le levier
baisse, aucune action émise. Le consensus attend +19,6 % de BPA en 2027 : le
prix suppose que cette croissance se prolonge au-delà, ce qu'aucun indicateur ne
peut vérifier.

### MC.PA — aucune séquence réflexive identifiable

Le profil le plus net du tableau, et pourtant le verdict par défaut. Multiple en
forte baisse (−44,6 points), bénéfice en baisse (−19,4), marge sous sa moyenne
(−2,6 points), consensus 2027 révisé à la baisse par 15 analystes sur 19. Cela
**ressemble** au stade 8 — multiple et bénéfice qui baissent ensemble —, mais
aucun canal ne relie la baisse du cours à celle du bénéfice : la dette baisse,
aucune action n'est émise. C'est une **révision de valeur**, pas un krach
réflexif. La distinction compte : un krach réflexif s'auto-entretient, une
révision s'arrête quand le prix rejoint ce que le marché croit désormais.

### SAN.PA — aucune séquence réflexive identifiable

La croissance implicite « exigeante » (+3,5 %) est un artefact de définition :
sur le BPA que suit le consensus, elle vaut −4,0 %. Multiple en forte baisse
(−33,4 points) sur un bénéfice stable : le marché a cessé de croire à une
croissance qu'il payait.

### BNP.PA — aucune séquence réflexive identifiable

La hausse la mieux **validée** du tableau : +28,8 points de bénéfice, +11,3 de
multiple, +22,3 de dividendes. Les cases de levier et de marge sont vides — une
banque ne se lit pas avec ces ratios —, ce qui rend B3 et R2 non mesurables.

### ORA.PA — aucune séquence réflexive identifiable

Tout y est effet de base : un résultat net 2025 effondré par des éléments
exceptionnels fait exploser la révision (+36,3 %), la décomposition (−138,3 et
+164,8 points) et la dispersion (88 %). La dette est laissée vide par le contrôle
de cohérence. Une valeur dont les chiffres de l'année sont **dominés par un
événement** ne se lit pas avec ces indicateurs avant que l'événement soit sorti
de la fenêtre.

## 10.6 — Le bilan du relevé

| Verdict | Valeurs |
|---|---|
| séquence candidate | **SU.PA** (canal de la dette, à vérifier) |
| séquence candidate rejetée à la vérification | TTE.PA |
| valorisation exigeante | OR.PA, AIR.PA |
| aucune séquence réflexive identifiable | MC.PA, SAN.PA, BNP.PA, ORA.PA |

> 🔑 **Le résultat principal de ce relevé est négatif, et c'est le bon.** Sur huit
> grandes valeurs, une seule configuration résiste à la vérification des
> composantes, et elle reste à confirmer dans un rapport annuel. Les autres
> lectures « spectaculaires » — Orange à +36 %, TotalEnergies à 2 sur 4, LVMH en
> chute — s'expliquent par un effet de base, un cycle, ou une révision de valeur.
> C'est exactement ce que dit le défaut de l'agent `sorosien`, et c'est ce qu'un
> lecteur pressé aurait manqué.

## Exercices

**E10.1.** Relancer le script. Pour chaque valeur, noter les marqueurs qui ont
changé depuis le 8 octobre 2026, et dire si le verdict change.

**E10.2.** La règle 2 du § 9.3 aurait-elle dû s'appliquer à TotalEnergies si B3
exigeait aussi une dette en hausse de plus de 10 % **et** un EBITDA en hausse ?
Proposer cette règle, et dire à quelle catégorie (A ou B) elle appartiendrait si
on l'adoptait aujourd'hui.

**E10.3.** Pourquoi le contexte du § 10.2 ne change-t-il aucun verdict ?

### Corrigés

**E10.1.** Pas de corrigé : le contrôle est de distinguer un marqueur qui change
parce que la **grandeur** a changé d'un marqueur qui change parce qu'elle était
**proche du seuil**.

**E10.2.** Non : l'EBITDA de TotalEnergies baisse, B3 serait éteint, et la règle
2 ne s'appliquerait plus. La règle serait de **catégorie B** : elle est suggérée
par le cas de TotalEnergies, observé sur ce relevé. Elle n'est recevable que
déclarée comme telle, avec son mécanisme (un levier qui monte par la chute de son
dénominateur n'est pas un levier qui finance), et éprouvée sur des valeurs
qu'elle n'a pas servi à fabriquer.

**E10.3.** Parce qu'il est commun aux huit valeurs : un indicateur qui prend la
même valeur pour toutes ne peut pas les départager. Il ne pourrait changer un
verdict que par la sensibilité propre de chaque valeur, que le relevé ne
mesure qu'au change.

## Ce qu'il faut retenir

1. Le relevé se lit dans l'ordre : contexte, tableau de bord, marqueurs, puis
   **vérification des composantes** avant tout verdict.
2. Une règle mécanique produit des **faux positifs** (TotalEnergies) que seule la
   lecture des composantes écarte ; une case vide (Orange, BNP) interdit de
   conclure.
3. Au 8 octobre 2026, une seule **séquence candidate** sur huit valeurs, Schneider,
   et elle reste à confirmer par ce qu'a financé sa dette.

---

⬅️ [Module 9 — Assembler : la séquence et la règle écrite](09-assembler-la-sequence.md) ·
➡️ [Module 11 — La fiche, à remplir](11-la-fiche-a-remplir.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
