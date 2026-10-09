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

## Résultat

*À compléter après la publication des cours du 2026-10-09, par le générateur.
Aucune ligne de la section précédente ne se modifie.*
