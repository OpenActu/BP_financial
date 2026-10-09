# Le marché a-t-il lu un rapprochement russo-américain ?

**La question.** Le 2026-10-08 à 19 h 02 (heure de Paris), BFM/AFP reprend une
dépêche Reuters : des responsables russes et américains auraient discuté de
l'entrée d'un investisseur américain dans les gazoducs **Nord Stream**, et la
Maison-Blanche confirme une négociation sur la cession des actifs étrangers de
**Lukoil** à un consortium mené par la DFC. Six supports cotés réagissent-ils,
le lendemain, dans le sens d'un **accord bilatéral entre Washington et Moscou,
l'Union européenne maintenant ses sanctions** — le scénario B ci-dessous — ou
le marché a-t-il ignoré la nouvelle ?

> ⚠️ **Ce document a été écrit en deux temps, et l'ordre est l'objet même de la
> mesure.** La section **Prévision déclarée** a été rédigée le **2026-10-09 à
> 06 h 19**, avant l'ouverture des marchés européens et américains de ce jour.
> Elle ne se modifie plus. La section **Résultat** est ajoutée après la
> publication des cours, par
> [`figures/mesurer_russie.py`](figures/mesurer_russie.md) `evenement`.

Le contexte — les trois scénarios, et pourquoi un rapprochement russo-américain
n'est pas un accord de paix — est dans le
[module 14 du cours macro](../concept/semestre4/macro/14-cas-d-etude-russie-2022-2026.md).

---

## Prévision déclarée — 2026-10-09, 06 h 19

### Les trois scénarios

- **A — paix multilatérale** : l'UE suit, les sanctions s'assouplissent.
- **B — accord russo-américain, l'UE maintient ses sanctions** : les États-Unis
  captent une rente (participation, partage des bénéfices), l'Europe reste
  cliente ; c'est le schéma que décrit l'article.
- **C — échec** : rien ne change.

### Les six supports et le signe attendu sous B

| Support | Ticker Yahoo | Marché de référence | Signe sous B | Pourquoi |
|---|---|---|---|---|
| Gaz européen, mois proche | `TTF=F` | aucun | **↓** | retour possible d'une offre russe |
| BASF | `BAS.DE` | `^STOXX50E` | **↑** | gros consommateur de gaz allemand, actionnaire de Nord Stream via Wintershall Dea |
| Raiffeisen Bank International | `RBI.VI` | `^STOXX50E` | **↑** | levée des sanctions américaines, sortie facilitée de la filiale russe |
| Cheniere | `LNG` | `^GSPC` | **↓** | gaz russe concurrent du GNL américain en Europe |
| Rheinmetall | `RHM.DE` | `^STOXX50E` | **↑** | désengagement américain, réarmement européen |
| ETF Pologne | `EPOL` | `^GSPC` | **↓** | pays en première ligne d'un accord conclu sans l'Europe |

Sous le **scénario A**, `RHM.DE` et `EPOL` prendraient le signe **opposé** ; les
quatre autres garderaient le leur.

### La mesure

- **Séance d'événement principale : 2026-10-09**, sur le marché de chaque
  support. Elle n'était pas ouverte au moment de la déclaration.
- **Fenêtre secondaire : 2026-10-08 et 2026-10-09 cumulées**, parce que l'heure
  de la dépêche Reuters d'origine est inconnue et qu'elle a pu précéder la
  clôture du 8. ⚠️ Pour cinq séries, la séance du 8 a **déjà été vue** avant la
  déclaration : `TTF=F` (+0,98 %), `LNG` (+2,07 %), `EPOL` (−0,37 %), ainsi que
  `BZ=F` et `NG=F`, qui ne sont pas parmi les six. La fenêtre secondaire est donc
  **contaminée** pour `TTF=F`, `LNG` et `EPOL`, et ne sert que d'information.
- **Rendement anormal.** Rendement logarithmique quotidien moins
  $\beta \times$ le rendement du marché de référence, $\beta$ estimé par moindres
  carrés sur les séances du **2025-10-01 au 2026-09-30**. Pour `TTF=F`, sans
  marché de référence, le rendement brut.
- **Rendement réduit** $z$ : rendement anormal divisé par l'écart-type des
  résidus sur la même fenêtre d'estimation.
- **Statistique** : $S$ = moyenne des six $z$ **signés** par le sens attendu
  sous B (un $z$ dans le sens attendu compte positivement).

### Critères, fixés avant la mesure

| Lecture | Condition |
|---|---|
| **B** | $S > +1$ **et** au moins 5 signes sur 6 concordants |
| **A** | `TTF=F`, `BAS.DE` et `RBI.VI` dans le sens attendu, `RHM.DE` **et** `EPOL` dans le sens contraire |
| **Contraire** | $S < -1$ |
| **Ignorée** | aucun des trois cas précédents |

Si les six $z$ étaient indépendants, $S$ aurait un écart-type de
$1/\sqrt 6 \approx 0{,}41$, et $S > 1$ n'arriverait par hasard qu'environ une
fois sur 140. Ils ne le sont pas — les quatre actions européennes partagent plus
que l'Euro Stoxx 50 —, donc ce seuil n'est **pas** une p-valeur et n'est pas
présenté comme telle.

### Ce que la mesure ne pourra pas établir

- **Une date ne mesure rien de général.** Le résultat dira comment le marché a
  lu **cette** dépêche, pas comment il lit les nouvelles de paix.
- **Une autre nouvelle du même jour** peut porter les mêmes supports. Le
  rendement de `^STOXX50E`, de `^GSPC` et de `BZ=F` sera publié à côté, et toute
  nouvelle majeure connue du 9 signalée, sans être retirée.
- **`TTF=F` est un contrat à échéance.** Un changement de contrat le 9
  fabriquerait un saut sans rapport ; il sera vérifié et déclaré.

---

## Fiche des supports — relevé du 2026-10-09, 06 h 44

> Cette section a été ajoutée **après** la prévision déclarée, et ne la modifie
> pas. Elle n'entre dans aucun critère : elle situe les supports, elle ne les
> classe pas, et elle ne désigne aucun titre à acheter ou à vendre.

| Nom | ISIN | Dernier cours | VE par action | Dernier dividende par action | PER (rendement bénéficiaire) | Si paix multilatérale | Si accord États-Unis–Russie seul |
|---|---|---|---|---|---|---|---|
| Raiffeisen Bank International | AT0000606306 | 57,75 € (07/10) | *(banque)* | 1,60 € (2026) | 8,0× (12,6 %) | ↑ | ↑ |
| OTP Bank | HU0000061726 | 39 900 HUF (07/10) | *(banque)* | ≈ 1 129 HUF (2026) | 9,2× (10,9 %) | ↑ | ↑ faible |
| BASF | DE000BASF111 | 51,18 € (07/10) | 73,24 € | 2,25 € (2026) | 21,3× (4,7 %) | ↑ | ↑ faible |
| Rheinmetall | DE0007030033 | 926,20 € (07/10) | 1 010,33 € | 11,50 € (2026) | 36,0× (2,8 %) ⚠️ | ≈ / ↓ | **↑** |
| Cheniere Energy | US16411R2085 | 277,88 $ (08/10) | 427,87 $ | 0,555 $ par trimestre (2026) | 21,0× (4,8 %) | ↓ | ambigu |
| iShares MSCI Poland ETF | US46429B6065 | 43,44 $ (08/10) | *(fonds)* | 0,302 $ par semestre (2026) | 13,3× (7,5 %), selon Yahoo | ↑ | **↓** |
| Gaz européen TTF (contrat à terme) | — | 78,85 €/MWh (08/10) | *(sans objet)* | *(sans objet)* | *(sans objet)* | ↓ | ↓ |

**Sources et calculs.** Tout vient de `yfinance`, relevé le 2026-10-09 à
06 h 44. Ces champs décrivent l'instant du relevé et ne se retrouvent pas plus
tard : c'est un **relevé daté**, pas une mesure refaisable.

| Colonne | Champ Yahoo, calcul |
|---|---|
| Dernier cours | dernière clôture de `history()` |
| VE par action | `enterpriseValue / sharesOutstanding`, au cours le plus récent connu de Yahoo |
| Dernier dividende | dernière ligne de `dividends`, datée par son détachement |
| PER | dernier cours / `trailingEps`, bénéfice des douze derniers mois ; rendement bénéficiaire = 1 / PER |
| Deux dernières colonnes | sens attendus, repris de la prévision déclarée et du [module 14](../concept/semestre4/macro/14-cas-d-etude-russie-2022-2026.md) ; **pas des prévisions de cours** |

**Contrôles.**

- **Nombre d'actions** : `sharesOutstanding` égale `marketCap` ÷ cours à moins
  de 0,01 % près pour BASF, Rheinmetall et Cheniere.
- **VE** : capitalisation + dette − trésorerie retrouve la VE publiée à 0,3 %
  près pour BASF (64,6 contre 64,8 Md€), à 1,7 % pour Rheinmetall (46,4 contre
  47,1 Md€) et à 4,9 % pour Cheniere (84,2 contre 88,4 Md$). L'écart restant est
  vraisemblablement fait d'intérêts minoritaires, sans que ce soit vérifié.
- **Banques** : la cellule VE reste **vide**. Les dépôts y sont une matière
  première, pas un financement, et les composantes publiées par Yahoo ne
  s'additionnent pas : pour OTP, la VE dépasse la capitalisation alors que dette
  et trésorerie s'annulent.
- ⚠️ **Rheinmetall** : le bénéfice par action attendu (`forwardEps`, 53,22 €)
  vaut **2,07 fois** le bénéfice récent (25,75 €). Sur le bénéfice attendu, le PER
  tombe à 17,6×. Le 36× est le passé, le 17,6× est une prévision du consensus.
- **ISIN** : ceux de Cheniere et de l'ETF Pologne sont donnés par Yahoo. Ceux de
  RBI, OTP, BASF et Rheinmetall sont **saisis de mémoire**, parce que Yahoo n'en
  fournit pas de fiable : il rend pour OTP un ISIN français qui n'est pas le sien.
  À vérifier avant tout réemploi.
- **OTP** : le dividende publié, 1 129,085 HUF, porte des décimales qui
  trahissent un ajustement du fournisseur ; le montant voté est à confirmer.

---

## Résultat

*À compléter après la publication des cours du 2026-10-09, par le générateur.
Aucune ligne de la section précédente ne se modifie.*
