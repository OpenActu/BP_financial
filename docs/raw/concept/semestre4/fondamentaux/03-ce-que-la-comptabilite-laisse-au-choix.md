# Module 3 — Ce que la comptabilité laisse au choix ⭐

**Prérequis :** [module 1](01-de-quoi-un-ratio-est-le-rapport.md).
**Ce qu'on établit ici :** que le dénominateur d'un ratio n'est pas une mesure physique mais le résultat de conventions, que certaines de ces conventions ont changé récemment, et que pour certains secteurs le ratio n'est pas seulement fragile — il est **indéfini**.

---

## 3.1 — L'EBITDA n'est défini par aucune norme

L'EBITDA — bénéfice avant intérêts, impôts, dépréciations et amortissements —
n'apparaît ni dans les IFRS, ni dans les US GAAP. **Aucun texte ne dit comment le
calculer.** Chaque société le publie selon sa propre définition, et les
fournisseurs de données recomposent la leur.

Conséquence directe : deux sources donnent deux VE/EBITDA différents pour la même
entreprise le même jour, sans qu'aucune ait tort.

> ⚠️ **Un multiple d'EBITDA n'est comparable qu'à l'intérieur d'une même source.**
> Ne mets jamais côte à côte un VE/EBITDA lu ici et un autre lu ailleurs.

## 3.2 — IFRS 16 : quand une norme déplace les ratios sans rien changer au réel

Depuis le 1ᵉʳ janvier 2019, IFRS 16 impose de porter les contrats de location au
bilan : un droit d'utilisation à l'actif, une dette de loyer au passif.

Le loyer, jusque-là charge opérationnelle, s'est scindé en **amortissement** et
**charge d'intérêt** — deux postes situés *sous* l'EBITDA.

| Grandeur | Effet mécanique du changement de norme |
|---|---|
| EBITDA | **augmente** — le loyer n'en est plus déduit |
| Dette | **augmente** — la dette de loyer apparaît |
| VE | **augmente** — elle contient la dette |
| Bénéfice net | à peu près inchangé |

Aucune entreprise n'a gagné un euro de plus le 1ᵉʳ janvier 2019. Pourtant
`VE/EBITDA` et `DETTE/EBITDA` ont sauté, d'autant plus que l'entreprise loue :
distribution, transport aérien, hôtellerie, télécoms.

**La leçon dépasse IFRS 16** : un ratio peut bouger parce que la règle a changé.
Comparer un multiple d'aujourd'hui à un multiple « historique » lu dans un manuel
antérieur à 2019, c'est comparer deux définitions.

## 3.3 — Fonds propres : ce que le P/B ne voit pas

Le $B$ du P/B est la valeur **comptable** des capitaux propres. Elle enregistre
ce qui a été payé, pas ce qui vaut.

| Situation | Effet sur $B$ | Effet sur le P/B |
|---|---|---|
| Marque développée en interne | **non inscrite** — les dépenses sont passées en charges | $B$ faible → P/B **artificiellement élevé** |
| Marque acquise | inscrite en goodwill | $B$ élevé → P/B plus bas, à activité identique |
| Rachats d'actions | $B$ **diminue** | P/B monte mécaniquement |
| Dépréciation de goodwill | $B$ chute d'un coup | P/B bondit sans qu'aucun flux ne change |
| Pertes accumulées | $B$ peut devenir **négatif** | P/B **dépourvu de sens** |

Deux entreprises rigoureusement identiques, l'une ayant construit sa marque,
l'autre l'ayant rachetée, affichent des P/B très différents. C'est pourquoi
L'Oréal et Airbus peuvent afficher $6{,}11$ et $6{,}21$ sans que cela dise quoi
que ce soit de commun sur leur valorisation.

> **Le P/B n'est interprétable que là où le bilan est l'outil de production** :
> banques, assurances, foncières, industries lourdes. Sur une société de
> services ou de logiciel, il est presque vide de contenu.

## 3.4 — Le ROE monte avec la dette

La décomposition de DuPont écrit le ROE comme un produit de trois facteurs :

$$\text{ROE} = \underbrace{\frac{\text{résultat net}}{\text{CA}}}_{\text{marge}} \times \underbrace{\frac{\text{CA}}{\text{actif}}}_{\text{rotation}} \times \underbrace{\frac{\text{actif}}{\text{fonds propres}}}_{\text{levier}}$$

Le troisième facteur n'est pas une performance : c'est un **choix de
financement**. À marge et rotation constantes, s'endetter augmente le ROE.

> ⚠️ **Un ROE élevé peut être un énoncé sur la dette, pas sur la rentabilité.**
> Il faut donc toujours lire le ROE **à côté** de `DETTE_EBITDA`. Sur le fil
> rouge, ORA.PA affiche un ROE de $14{,}16\,\%$, proche de celui de TTE.PA
> ($14{,}48\,\%$) — mais avec une dette/EBITDA de **4,69** contre **1,59**. Les
> deux nombres ne décrivent pas la même réussite.

C'est aussi ce qui rend le ROE **circulaire** avec le P/B : tous deux ont les
fonds propres au dénominateur. Le [module 4](04-un-ratio-n-existe-que-relatif.md)
en tire les conséquences.

## 3.5 — Les ratios indéfinis : le cas des banques

Sur le fil rouge, BNP.PA a deux cellules vides : `VE_EBITDA` et `REND_FCF`.
Ce ne sont **pas** des données manquantes.

- **La valeur d'entreprise n'a pas de sens pour une banque.** La dette n'est pas
  un mode de financement de l'outil : c'est la **matière première**. Les dépôts
  sont au passif ; les soustraire ou les ajouter à une valeur d'entreprise ne
  correspond à rien.
- **L'EBITDA non plus.** Les intérêts sont le cœur de l'activité, pas une charge
  de financement à neutraliser. Un « bénéfice avant intérêts » bancaire est un
  contresens.
- **Le flux de trésorerie disponible** d'une banque est dominé par les variations
  de bilan et ne mesure pas ce qu'il mesure ailleurs.

Le script laisse donc ces cases vides, conformément à la règle du miroir : *une
cellule vide est une information ; un nombre plausible n'en est pas une.*

⚠️ Une case du tableau **n'est pas** vide et devrait alerter : la marge nette de
BNP.PA, $26{,}49\,\%$, calculée sur un agrégat de produits bancaires qui n'est pas
le chiffre d'affaires d'un industriel. Le nombre s'affiche, il est simplement
**incomparable** aux autres lignes de la colonne. C'est le cas le plus dangereux :
non pas la donnée absente, mais la donnée présente et hors sujet.

Ce qui reste lisible sur une banque : **PER**, **P/B** — et le P/B y est même
plus informatif qu'ailleurs, puisque le bilan *est* l'activité.

## Ce qu'il faut retenir

1. L'EBITDA n'est pas normé : les multiples ne sont comparables qu'à l'intérieur
   d'une source.
2. Un changement de norme — IFRS 16 — déplace les ratios sans que le réel bouge.
3. Le P/B dépend de l'histoire d'acquisition, pas seulement de la valeur.
4. Le ROE contient le levier ; il se lit toujours à côté de la dette.
5. Pour une banque, VE/EBITDA et rendement du FCF ne sont pas manquants : ils
   n'existent pas. Et une marge affichée peut être plus trompeuse qu'une case
   vide.

---

⬅️ [Module 2 — Les quatre dates d'un ratio](02-les-quatre-dates-d-un-ratio.md) ·
➡️ [Module 4 — Un ratio n'existe que relatif](04-un-ratio-n-existe-que-relatif.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
