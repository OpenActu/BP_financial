# Module 3 — La règle écrite à l'avance ⭐

**Prérequis :** [module 2](02-d-un-objet-a-un-critere.md).
**Ce qu'on établit ici :** la règle intégrale, l'origine de chacun de ses seuils, la justification de ses quatre vetos, et ce qu'elle donne quand on l'applique jour après jour au lieu de la lire une fois.

---

## 3.1 — Pourquoi « avant »

Un graphique est une machine à confirmer. Sur Airbus au 31 décembre 2020, on peut
raconter deux histoires strictement opposées **avec les mêmes chiffres** :

- *l'histoire haussière* : tendance à 120 séances significative à $10^{-21}$,
  cours à 18 % de la hauteur de son canal, à $2{,}9\,\%$ seulement de son support,
  rebond de $+83\,\%$ depuis le creux du 18 mars ;
- *l'histoire baissière* : tendance à 20 séances significativement **baissière**
  ($p = 0{,}003$), momentum 12-1 à $-33{,}5\,\%$, titre encore à $-33\,\%$ sur
  l'année, canal qui se referme.

Les deux sont vraies. Choisir laquelle raconter **après** avoir vu le graphique,
c'est se donner un degré de liberté qu'aucune donnée ne contraint. Écrire la règle
avant, c'est renoncer à ce degré de liberté.

> 🔑 **Une règle publiée à l'avance n'est pas une garantie de bon résultat, c'est
> une garantie de vérifiabilité.** Elle transforme « je pense que » en « voici le
> critère, voici sa valeur, voici le verdict qu'il produit » — un énoncé que
> quiconque peut refaire et contredire.

## 3.2 — La règle, in extenso

C'est le § 4 de l'agent [`trading`](../../../../../.claude/agents/trading.md),
recopié sans modification. **Il se publie avant tout chiffre.**

### Les cinq critères

| # | Critère | Source |
|---|---|---|
| 1 | Tendance longue : `TEND_120` | [`import_societe.py`](../../../../../python/import_societe.md) |
| 2 | Tendance courte : `TEND_20` | idem |
| 3 | Position dans l'encadrement actif, en % de la hauteur | [encadrement 04](../../semestre3/encadrement/04-lire-l-encadrement.md) |
| 4 | Alpha annualisé et son IC95 contre l'indice | [alpha 02](../alpha/02-le-calcul-et-ses-erreurs-types.md) |
| 5 | Momentum 12-1 | [module 2 § 2.4](02-d-un-objet-a-un-critere.md#24--le-momentum-12-1-et-le-trou-du-dernier-mois) |

### Le verdict

- **ACHAT** — critères 1 et 2 à $+1$, position $< 35\,\%$ de la hauteur du canal,
  momentum 12-1 positif, et borne haute de l'IC de l'alpha $> 0$.
- **VENTE** — critères 1 et 2 à $-1$, position $> 65\,\%$, momentum 12-1 négatif.
- **ATTENTE** — dans **tous** les autres cas.

`ATTENTE` est le défaut, et il est **obligatoire** dès que l'une de ces conditions
est réunie, quels que soient les cinq critères :

1. l'encadrement actif compte moins de 3 épisodes de contact d'un côté ;
2. le canal converge et se referme dans moins de 20 séances ;
3. les critères 1 et 2 sont de signes opposés ;
4. l'historique compte moins de 120 séances.

## 3.3 — D'où viennent les quatre vetos

Aucun n'est un réglage : chacun traduit un résultat démontré ailleurs.

| Veto | Ce qu'il empêche | Résultat invoqué |
|---|---|---|
| **1. Moins de 3 épisodes** | décider sur une droite qui n'est que la définition de son arête — deux points définissent **toujours** une droite | [encadrement 02 § 2.4](../../semestre3/encadrement/02-portee-et-episodes-de-contact.md#24--combien-de-contacts-pour-y-croire) |
| **2. Fermeture en $< 20$ séances** | lire une position dans un canal qui n'existera plus dans un mois ; dans un biseau convergent le franchissement est **géométriquement certain** | [encadrement 04 § 4.2](../../semestre3/encadrement/04-lire-l-encadrement.md#42--un-canal-convergent-a-une-date-de-péremption) |
| **3. Signes opposés** | trancher entre deux tests significatifs qui se contredisent — la donnée dit qu'il y a **deux régimes**, pas une direction | [canal 05](../../semestre3/canal/05-canal-glissant.md), l'arbitrage de longueur de fenêtre |
| **4. Moins de 120 séances** | calculer `TEND_120`, un momentum 12-1 ou un alpha sur un historique qui ne les contient pas | [alpha 03](../alpha/03-l-horizon-necessaire.md) |

Le veto 3 mérite un mot de plus. Quand `TEND_120 = +1` et `TEND_20 = −1`, les deux
tests sont valides et significatifs : la fenêtre longue mesure une pente réelle sur
six mois, la fenêtre courte une pente réelle sur un mois. Il n'y a pas de
contradiction logique, seulement **deux échelles de temps qui divergent**. Aucun
critère de ce cours ne permet d'arbitrer entre elles ; la règle refuse donc de
choisir. C'est le cas d'Airbus au 31 décembre 2020
([module 5](05-exemple-date-1er-janvier-2021.md)).

## 3.4 — L'asymétrie achat / vente est délibérée

`ACHAT` exige **cinq** conditions, `VENTE` seulement **trois**. Ce n'est ni une
coquetterie ni un biais optimiste :

- la condition d'alpha ne figure pas dans `VENTE` parce qu'elle serait vide de
  sens : demander que la borne **basse** de l'IC soit $< 0$ est vrai
  pour à peu près toute valeur sur deux ans (ici $-49\,\%$) ;
- le momentum figure dans les deux, avec des signes opposés, parce qu'il est le
  seul critère de persistance ;
- surtout, `VENTE` s'entend ici comme **sortie d'une position existante**, pas
  comme vente à découvert. Le dimensionnement, le levier et la VAD relèvent du
  [cours finance](../finance/README.md) et sont explicitement hors du champ de
  cette règle.

## 3.5 — Le vrai danger : les degrés de liberté de l'analyste

La règle a 5 critères et 3 seuils numériques ($35\,\%$, $65\,\%$, $0$ pour le
momentum), plus 4 vetos dont 2 chiffrés (3 épisodes, 20 séances). Si l'on
s'autorisait à faire varier chacun ne serait-ce que sur cinq valeurs, on
disposerait de $5^5 \approx 3000$ règles — et il en existerait forcément une
brillante sur Airbus 2019-2020.

C'est le [piège des tests multiples](../alpha/04-cinq-pieges.md) transposé du
domaine statistique à celui de la construction de règle. Trois protections, et
elles sont procédurales, pas mathématiques :

1. **Publier les seuils avant les chiffres**, comme au § 3.2 ;
2. **Publier les variantes essayées**, s'il y en a eu, avec la raison du choix ;
3. **Ne jamais réajuster un seuil après avoir vu le verdict** — un seuil déplacé
   pour changer un verdict n'est plus une règle, c'est une opinion habillée.

## 3.6 — Ce que la règle donne appliquée tous les jours

Une règle ne se juge pas sur une date. Appliquons-la à Airbus contre le CAC 40 à
**chacune** des 515 séances du 2 janvier 2020 au 31 décembre 2021, chaque jour
avec les seules données disponibles ce jour-là :

| Verdict | Occurrences | Part |
|---|---|---|
| **ATTENTE** | **512** | **99,4 %** |
| ACHAT | 3 | 0,6 % |
| VENTE | 0 | 0,0 % |

Les trois séances `ACHAT` : **2021-03-05, 2021-04-20, 2021-11-19**.

Et la ventilation des motifs d'`ATTENTE`, dans l'ordre où la règle les évalue :

| Motif | Occurrences |
|---|---|
| Veto 1 — moins de 3 épisodes de contact d'un côté | 256 |
| Aucun jeu complet de conditions `ACHAT` ou `VENTE` | 163 |
| Veto 3 — `TEND_20` et `TEND_120` de signes opposés | 49 |
| Veto 2 — canal se refermant en moins de 20 séances | 44 |

> 🔑 **Une règle honnête est presque toujours silencieuse.** Sur deux ans, elle
> s'exprime trois fois. La moitié des jours, elle refuse même de regarder les
> critères parce que la géométrie n'est pas confirmée. C'est le comportement
> attendu, pas un défaut : le coût d'une règle bavarde est un enchaînement d'ordres
> mangés par les frais, que ce dépôt **ne modélise pas** — le CSV ne contient ni
> spread ni commission.

Deux réserves sur ce comptage lui-même, et elles sont sérieuses :

- **Ce n'est pas un backtest.** Aucun rendement n'a été calculé, aucune position
  n'a été simulée, aucun coût n'a été déduit. C'est un simple dénombrement de
  verdicts.
- **Un seul titre, une seule période.** Deux ans sur Airbus ne disent rien du
  comportement de la règle ailleurs. Le
  [biais du survivant](../alpha/04-cinq-pieges.md) et l'[encombrement du
  facteur](../alpha/04-cinq-pieges.md) resteraient à traiter sur un univers réel.

## 3.7 — Ce qu'un verdict n'est pas

| Le verdict dit | Le verdict ne dit pas |
|---|---|
| que cinq critères publiés prennent, à une date, des valeurs mesurées | ce que le cours fera ensuite |
| qu'un jeu de conditions écrit à l'avance est satisfait ou non | combien acheter, avec quel levier, quel stop |
| lequel des vetos a éventuellement mordu | si l'opération est fiscalement ou patrimonialement pertinente |
| sur quelle fenêtre et à quelle date il a été calculé | ce qu'il faut faire |

Et la phrase qui doit accompagner toute publication d'un verdict, sans exception :

> *Ceci est la sortie d'une règle écrite appliquée à des données passées, pas une
> recommandation.*

---

⬅️ [Module 2 — D'un objet à un critère](02-d-un-objet-a-un-critere.md) ·
➡️ [Module 4 — Les pièges du passage à l'acte](04-les-pieges-du-passage-a-l-acte.md)
