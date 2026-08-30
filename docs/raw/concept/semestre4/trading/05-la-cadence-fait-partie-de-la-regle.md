
# Module 5 — La cadence d'application fait partie de la règle ⭐

**Prérequis :** modules [1](01-ce-que-le-chartiste-produit.md) à [4](04-les-pieges-du-passage-a-l-acte.md).
**Ce qu'on établit ici :** la règle du [module 3](03-la-regle-ecrite-a-l-avance.md) exécutée une fois de bout en bout à une date (§ 5.1), puis la question que le module 3 laisse ouverte — **quand l'exécute-t-on ?** Sur les mêmes cinq années et les mêmes données, quatre cadences donnent quatre histoires différentes, et cinq variantes d'une **même** cadence hebdomadaire vont de « jamais acheté avant 2023 » à « acheté en mars 2021 et jamais ressorti ». **La cadence n'est pas un détail d'exploitation : c'est un paramètre de la règle, aussi décisif que ses seuils, et il n'était écrit nulle part.**

---

## 5.0 — Ce que la règle ne dit pas encore

Le [module 3](03-la-regle-ecrite-a-l-avance.md) fixe cinq critères, trois seuils
numériques et quatre vetos. Il ne dit pas **à quelles dates** on l'évalue — et
cette omission n'est pas anodine :

> 🔑 **Un verdict est daté.** Il ne se propage ni vers l'avant ni vers l'arrière.
> Une règle qui n'est pas évaluée le 4 janvier ne dit **rien** le 4 janvier — pas
> `ATTENTE`, rien. La suite des dates auxquelles on l'interroge est donc une
> composante de la règle au même titre que le seuil de $35\,\%$, et le module 3
> l'omettait.

Ce module nomme cette composante **la cadence**, montre qu'elle change tout, et
en tire ce qu'il faut ajouter à la règle pour qu'elle soit complète.

## 5.1 — Exécuter la règle une fois, de bout en bout

**On se place au 1er janvier 2021.** Ce jour est férié : Euronext Paris est fermé,
il n'existe pas de cotation. La dernière séance disponible est le jeudi
**31 décembre 2020**, et c'est elle qui porte le verdict
([§ 4.1a](04-les-pieges-du-passage-a-l-acte.md#a-la-date-demandée-nest-pas-une-séance)).

```bash
python python/import_societe.py AIR.PA  --debut 2019-01-02 --fin 2021-01-01
python python/import_societe.py '^FCHI' --debut 2019-01-02 --fin 2021-01-01

python python/generer_graph_decision.py \
  --csv docs/raw/data/quotes/AIR_PA_2019-01-02_2020-12-31.csv \
  --indice 'docs/raw/data/quotes/^FCHI_2019-01-02_2020-12-31.csv' \
  --date 2021-01-01
```

```
Le 2021-01-01 n'est pas une séance ; décision au 2020-12-31.
Valeur           : AIR.PA (513 séances, 2019-01-02 → 2020-12-31)
Décision         : 2020-12-31
Fenêtre active   : 2020-07-16 → 2020-12-31 (120 séances, ε = 2,62 €)
Résistance       : pente +0,2306 €/séance · portée 83 · 6 épisodes · 93,18 €
Support          : pente +0,5820 €/séance · portée 37 · 3 épisodes · 79,99 €
Largeur          : 13,19 € (16,0 %) · τ = 37,5 séances

Critère 1  tendance longue — TEND_120        : +1
Critère 2  tendance courte — TEND_20         : -1
Critère 3  position dans l'encadrement actif : 18,0 % de la hauteur
Critère 4  alpha annualisé contre l'indice   : -0,29 %/an · IC95 [-49,44 ; +48,85] % · indiscernable de zéro
Critère 5  momentum 12-1                     : -33,47 %

Vetos            : veto 3 : critères 1 et 2 de signes opposés
VERDICT          : ATTENTE
```

![Airbus, les cinq critères et le verdict au 1er janvier 2021](figures/airbus-decision-2021-01-01.svg)

> ## `ATTENTE`
>
> **Condition déclenchante : veto 3** — `TEND_120 = +1` et `TEND_20 = −1` sont de
> signes opposés. Deux tests significatifs qui pointent dans des directions
> contraires sur deux échelles de temps ; la règle refuse d'arbitrer entre elles.

Le verdict se confirme de deux façons indépendantes, ce qui est utile à publier :

| Verdict testé | Conditions | Résultat |
|---|---|---|
| **ACHAT** | 1 et 2 à $+1$ · position $< 35\,\%$ · momentum $> 0$ · borne haute IC $> 0$ | échoue sur `TEND_20` $=-1$ **et** sur le momentum $-33{,}5\,\%$ (position $18{,}0\,\%$ ✓, borne haute $+48{,}9\,\%$ ✓) |
| **VENTE** | 1 et 2 à $-1$ · position $> 65\,\%$ · momentum $< 0$ | échoue sur `TEND_120` $=+1$ **et** sur la position $18{,}0\,\%$ (momentum $< 0$ ✓) |

Deux critères plaidaient l'achat, deux plaidaient la vente, le cinquième était
muet : c'est exactement la situation qu'`ATTENTE` est faite pour couvrir.

**Voilà l'exécution complète, et elle tient en une page.** Tout le reste du module
consiste à la répéter — et à constater que le choix des dates de répétition pèse
davantage que tout ce qui précède.

## 5.2 — Une date choisie par le calendrier n'est pas une séance

Première conséquence, immédiate et mesurable. Sur les cinq années 2021-2025, si
l'on fixe les dates de décision au calendrier plutôt qu'au tableau de cotation :

| Cadence | Dates de décision | Hors séance | Part |
|---|---|---|---|
| Quotidienne | 1281 séances | 0 | $0\,\%$ |
| Hebdomadaire, le vendredi | 261 | 7 | $3\,\%$ |
| Hebdomadaire, le lundi | 261 | 9 | $3\,\%$ |
| **Mensuelle, fin de mois** | **60** | **17** | **$28\,\%$** |
| Trimestrielle | 20 | 5 | $25\,\%$ |

Les sept vendredis non cotés sont le 1er janvier 2021, les cinq Vendredis saints
de 2021 à 2025, et le 26 décembre 2025. Les fins de mois, elles, tombent hors
séance **plus d'une fois sur quatre** — les week-ends suffisent à l'expliquer.

La règle du [§ 4.1a](04-les-pieges-du-passage-a-l-acte.md#a-la-date-demandée-nest-pas-une-séance)
s'applique alors : le script recule à la dernière séance **antérieure ou égale**.
Ce n'est pas un contournement, c'est la seule lecture qui n'introduise pas de
regard en avant — mais elle déplace la date de décision, et le § 5.4 montre ce
qu'un déplacement d'un jour peut coûter.

## 5.3 — La même règle, quatre cadences

Les verdicts sont ceux du [module 6](06-cas-pratique.md) — la règle appliquée à
chacune des 1 281 séances de 2021 à 2025 sur Airbus contre le CAC 40. Une cadence
plus lente ne recalcule rien : elle **sous-échantillonne** cette même suite, et
chaque verdict retenu n'utilise que les données antérieures à sa propre date.

À ces quatre cadences on applique la convention de cycle du
[§ 6.1.2](06-cas-pratique.md#612--la-convention-de-cycle-qui-nest-pas-dans-la-règle) :
entrée au premier `ACHAT`, sortie à la première `VENTE` postérieure, un seul
aller-retour.

| Cadence | Séances évaluées | `ACHAT` vus | `VENTE` vus | Ce que la convention produit |
|---|---|---|---|---|
| **Quotidienne** | 1281 | 25 | **2** | **cycle fermé** : 2021-03-05 à 87,54 € → 2022-10-04 à 88,13 €, $+0{,}67\,\%$ |
| Hebdomadaire (vendredi) | 260 | 8 | **0** | entrée le 2021-03-05 à 87,54 €, **jamais ressorti** |
| Mensuelle (fin de mois) | 60 | 1 | **0** | entrée le 2023-05-31 à 115,66 €, **jamais ressorti** |
| Trimestrielle | 20 | **0** | **0** | **aucun signal en cinq ans**, jamais en position |

> ⚠️ **Aucune de ces trois cadences ne voit la sortie.** L'unique fenêtre de
> `VENTE` des cinq années est large de **deux séances**, les mardi 4 et mercredi
> 5 octobre 2022 ([§ 6.5](06-cas-pratique.md#65--la-sortie--mardi-4-octobre-2022)).
> Une grille hebdomadaire calée sur le vendredi passe à côté par construction ;
> une grille mensuelle a une chance sur dix de tomber dessus. **La cadence ne
> filtre pas le bruit, elle décide de ce qui existe.**

Noter aussi le cas trimestriel : sur vingt relevés, la règle ne parle **jamais**.
Un lecteur qui l'interrogerait quatre fois par an conclurait, en toute bonne foi,
qu'elle est muette — alors qu'elle a rendu 27 verdicts non-`ATTENTE` sur la
période.

## 5.4 — Le jour de la semaine décide du cycle

C'est le résultat central du module. On garde **la même cadence hebdomadaire** —
un relevé tous les sept jours, cinquante-deux par an — et on ne change qu'une
chose : **le jour choisi**.

| Jour retenu | Dates au calendrier | Hors séance | `ACHAT` | `VENTE` | Ce que la convention produit |
|---|---|---|---|---|---|
| Lundi | 261 | 9 | 4 | 0 | entrée le 2023-05-29, position ouverte |
| **Mardi** | 261 | 1 | 4 | **1** | **cycle fermé** : 2021-04-20 → 2022-10-04, **$-1{,}91\,\%$** |
| Mercredi | 261 | 3 | 3 | 1 | la `VENTE` du 2022-10-05 arrive **avant** son premier `ACHAT` : ignorée, entrée le 2023-05-31 |
| Jeudi | 260 | 3 | 6 | 0 | entrée le 2023-06-22, position ouverte |
| **Vendredi** | 261 | 7 | 8 | 0 | entrée le **2021-03-05**, position ouverte |

*Les dates hors séance reculent à la séance précédente et ne disparaissent pas —
sauf le vendredi 1er janvier 2021, qui n'a aucune séance avant lui **dans la
période** : la grille du vendredi évalue donc 260 séances pour 261 dates.*

> 🔑 **Cinq exécutions de la même règle, à la même fréquence, sur les mêmes
> données — et cinq histoires sans rapport.** L'une ferme un cycle en perte,
> trois n'achètent qu'en 2023, une achète en mars 2021 et ne ressort jamais. Rien
> n'a changé que le jour de la semaine, un paramètre que personne n'écrit et que
> le module 3 ne mentionne pas.

Le mercredi mérite un mot : sa grille **voit** une `VENTE`, celle du 5 octobre
2022, mais elle arrive alors qu'il n'est pas en position — la convention 3 la
rend inopérante. La cadence ne change donc pas seulement ce qu'on voit, elle
change **l'ordre** dans lequel on le voit, et un signal vu hors contexte est un
signal perdu.

## 5.5 — Pourquoi : un signal est un épisode, une cadence est une grille

L'explication est entièrement combinatoire, et elle se vérifie.

Les 25 séances `ACHAT` de la période forment **12 épisodes**, dont voici
l'étendue en séances :

$$1,\ 1,\ 1,\ 1,\ 3,\ 3,\ 1,\ 3,\ 1,\ 4,\ 1,\ 7$$

**La médiane vaut 1.** Un épisode d'une séance est vu par une grille
hebdomadaire une fois sur cinq, et par une grille mensuelle une fois sur vingt et
une — c'est arithmétique, pas empirique.

La vérification est exacte du côté de la vente. L'unique épisode de `VENTE` dure
**deux séances consécutives**, un mardi et un mercredi : sur les cinq grilles
hebdomadaires possibles, **exactement deux** le contiennent — celles du § 5.4 qui
affichent une `VENTE`. Du côté de l'achat, la grille du vendredi voit **7 des
12 épisodes**.

> ⚠️ **Une règle qui exige beaucoup produit des signaux courts, et des signaux
> courts sont invisibles à une grille lâche.** Les deux propriétés sont liées :
> plus les conditions sont sévères, plus rarement elles sont toutes réunies, et
> plus brève est la fenêtre où elles le sont. **Durcir une règle sans resserrer
> sa cadence revient à la faire taire**, et le § 5.3 en donne le cas limite avec
> les vingt relevés trimestriels.

## 5.6 — Et si l'on autorisait plusieurs cycles

La convention du module 6 s'arrête au premier aller-retour. Elle avantage
mécaniquement les cadences qui ne trouvent jamais leur sortie, puisqu'elles
restent investies. Il faut donc refaire le compte sans elle : **cycles répétés**,
tout ou rien, position finale valorisée à la clôture du 31 décembre 2025, coûts
de $0{,}243\,\%$ par aller-retour ([§ 6.6](06-cas-pratique.md#66--le-compte-du-cycle)).

| Cadence | Entrées | Brut | Net | Détail |
|---|---|---|---|---|
| Quotidienne | 2 | $+80{,}70\,\%$ | $+79{,}82\,\%$ | cycle fermé à $+0{,}7\,\%$, puis réentrée le 2023-01-27, **ouverte** |
| Hebdo. lundi | 1 | $+64{,}75\,\%$ | $+64{,}35\,\%$ | ouverte depuis le 2023-05-29 |
| Hebdo. mardi | 2 | $+62{,}68\,\%$ | $+61{,}89\,\%$ | cycle fermé à $-1{,}9\,\%$, puis réentrée, **ouverte** |
| Hebdo. mercredi | 1 | $+68{,}42\,\%$ | $+68{,}02\,\%$ | ouverte depuis le 2023-05-31 |
| Hebdo. jeudi | 1 | $+61{,}70\,\%$ | $+61{,}31\,\%$ | ouverte depuis le 2023-06-22 |
| **Hebdo. vendredi** | 1 | **$+122{,}53\,\%$** | **$+121{,}99\,\%$** | ouverte depuis le 2021-03-05 |
| Mensuelle | 1 | $+68{,}42\,\%$ | $+68{,}02\,\%$ | ouverte depuis le 2023-05-31 |
| **Trimestrielle** | **0** | **$0{,}00\,\%$** | **$0{,}00\,\%$** | jamais investie |
| *pour mémoire* — le titre conservé | — | $+136{,}21\,\%$ | — | jamais vendu |

**L'écart va de $0$ à $+122\,\%$**, et il ne tient qu'à la cadence. La conclusion
du § 5.4 survit donc au changement de convention : elle ne venait pas de la
convention.

> ⚠️ **Aucune de ces lignes n'est une performance.** Sept des huit se terminent
> sur une **position ouverte**, valorisée à une date arbitraire — le 31 décembre
> 2025 — et dont le résultat n'existera qu'à la sortie. Une plus-value latente
> n'est pas un résultat, c'est un prix du jour. La seule ligne dont le compte soit
> clos est le cycle du module 6 : $+0{,}67\,\%$ brut.

## 5.7 — La cadence est un degré de liberté, pas un détail

Le [§ 3.5](03-la-regle-ecrite-a-l-avance.md#35--le-vrai-danger--les-degrés-de-liberté-de-lanalyste)
comptait les degrés de liberté de l'analyste : 5 critères, 3 seuils, 4 vetos —
environ 3 000 règles si on laisse chacun varier sur cinq valeurs. **Il en
manquait un**, et les tableaux ci-dessus le chiffrent : à règle strictement
identique, huit cadences produisent huit résultats séparés de 122 points.

La protection est la même, et elle est procédurale :

1. **Publier la cadence avec la règle**, avant tout chiffre, au même endroit que
   les seuils ;
2. **Publier les cadences essayées**, s'il y en a eu, avec la raison du choix ;
3. **Ne jamais choisir la cadence au vu du résultat.** Retenir le vendredi après
   avoir lu le § 5.4 n'est pas une méthode, c'est le
   [piège des tests multiples](../alpha/04-cinq-pieges.md) — un seuil déplacé
   pour changer un verdict n'est plus une règle, c'est une opinion habillée.

### Ce que la cadence coûte, et ce qu'elle ne coûte pas

On attendrait qu'une cadence rapide se paie en frais. Ici, non — et c'est une
information :

| | Aller-retours en 5 ans | Frais cumulés | Freinage annuel |
|---|---|---|---|
| Cadence quotidienne, cycles répétés | **2** | $0{,}49\,\%$ | $0{,}10\,\%$/an |
| *pour comparaison* — rotation mensuelle | 60 | $14{,}6\,\%$ | $2{,}92\,\%$/an |

*Aller-retour à $0{,}243\,\%$, le tarif d'Airbus, exemptée de TTF. Au barème
général de $0{,}530\,\%$, la même rotation mensuelle coûte $6{,}36\,\%$/an — le
chiffre que publie la table de rotation de*
[*`couts_transaction.py`*](../../../../../python/couts_transaction.md)*.*

Cette table décrit une règle que celle-ci **n'est pas** : évaluée tous les jours,
elle ne négocie que deux fois en cinq ans, parce que les vetos la font taire
$97{,}9\,\%$ du temps.

> 🔑 **Évaluer souvent n'est pas négocier souvent.** Les deux se confondent dans
> l'intuition et se séparent dans les chiffres : la cadence fixe ce que la règle
> *voit*, la règle fixe ce qu'elle *dit*. Une cadence quotidienne sur une règle
> silencieuse coûte $0{,}10\,\%$/an ; la même cadence sur une règle qui bascule au
> gré de `TEND_20` coûterait, au barème, plus de $27\,\%$/an. Le prix ne vient
> jamais de la cadence seule.

## 5.8 — Ce qu'il faut ajouter à la règle du module 3

Trois lignes, à publier avec les cinq critères et les quatre vetos :

| # | Ce qui doit être déclaré | Exemple, celui du module 6 |
|---|---|---|
| 1 | **La cadence** : la suite des dates auxquelles la règle est évaluée | quotidienne, à chaque séance cotée |
| 2 | **Le traitement des dates hors séance** | recul à la dernière séance antérieure ou égale ([§ 4.1a](04-les-pieges-du-passage-a-l-acte.md#a-la-date-demandée-nest-pas-une-séance)) |
| 3 | **Ce qui se passe entre deux dates d'évaluation** | rien : aucun verdict, aucune action, aucun stop — le [module 7](07-le-stop-une-sortie-sans-verdict.md) mesure ce qu'un stop y changerait |

La troisième ligne est la moins intuitive et la plus lourde de conséquences : le
[§ 6.4](06-cas-pratique.md#64--dix-neuf-mois-de-détention-et-le-silence-de-la-règle)
montre une position qui traverse un repli de $25{,}8\,\%$ pendant 224 séances sans
qu'un seul verdict soit rendu. Ce silence est **conforme** — il est la ligne 3
appliquée — et il faut l'avoir écrit avant pour ne pas le découvrir en cours de
route.

## 5.9 — Ce que ce module ne montre pas

- **Un titre, une période, huit cadences.** Rien ici ne dit ce qu'il en est
  ailleurs, ni si l'ordre des cadences se reproduirait sur un autre titre. Huit
  résultats ne sont pas une distribution.
- **Sept des huit lignes du § 5.6 sont des positions ouvertes.** Leur valorisation
  au 31 décembre 2025 dépend d'une date choisie par le calendrier, pas par la
  règle. Comparer une position ouverte à un cycle clos est une commodité de
  présentation, pas une mesure.
- **Le classement des cadences est un artefact.** Le vendredi ne « marche » pas
  mieux : il se trouve qu'un signal d'achat de 2021 est tombé un vendredi et
  qu'aucune sortie n'est venue le contredire. Un signal décalé d'un jour aurait
  inversé le tableau.
- **Aucun coût de suivi n'est compté.** Interroger une règle 1 281 fois plutôt
  que 20 a un coût de traitement et d'attention, que ce dépôt ne modélise pas.
- **La cadence n'épuise pas le sujet.** L'heure d'évaluation dans la séance, le
  délai entre verdict et ordre, et le comportement en cas de suspension de
  cotation restent hors champ ; le
  [§ 6.6](06-cas-pratique.md#66--le-compte-du-cycle) ne chiffre que le deuxième de
  ces trois.

> *Ceci est la sortie d'une règle écrite appliquée à des données passées, pas une
> recommandation.*

---

⬅️ [Module 4 — Les pièges du passage à l'acte](04-les-pieges-du-passage-a-l-acte.md) ·
➡️ [Module 6 — Cas pratique : un cycle `ACHAT` → `VENTE`, 2021-2025](06-cas-pratique.md)
