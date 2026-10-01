# Module 12 — Cas d'étude : la livre sterling, 16 septembre 1992

**Prérequis :** modules [2](02-la-politique-monetaire.md) (surprise monétaire) et [6](06-le-change.md) (le change).
**Ce qu'on établit ici :** comment se construit une position macro sur une parité fixe, quels facteurs la rendaient favorable, lesquels la menaçaient, combien elle coûtait à porter, pourquoi ce n'était **pas** un carry trade, et ce qu'un cas célèbre ne permet pas de conclure.

> ⚠️ **Statut des nombres de ce module.** Contrairement aux modules 1 et 6 à 11,
> aucun chiffre ici ne sort de [`mesurer_macro.py`](figures/mesurer_macro.md) :
> Yahoo ne fournit ni la parité livre/mark, ni le change d'avant 2003. Les
> données historiques — taux, parités, dates — viennent de sources secondaires
> (Banque d'Angleterre, Trésor britannique, récits des protagonistes) et sont
> des **ordres de grandeur**. Les tailles de position et les gains de Quantum
> n'ont jamais été audités publiquement. Les calculs du § 12.4, eux, sont
> exacts **à partir de ces hypothèses**, et on peut les refaire à la main.

---

## 12.1 — Le dispositif

| Date | Fait | Chiffre |
|---|---|---|
| 8 oct. 1990 | Le Royaume-Uni entre dans le **mécanisme de change européen** (MCE) | cours pivot **2,95 DM**, marge **± 6 %** |
| — | Plancher et plafond de la livre | **2,778 DM** et **3,132 DM** |
| oct. 1990 | Inflation britannique (RPI) à l'entrée | **≈ 10,9 %** |
| 16 juil. 1992 | La Bundesbank relève son taux Lombard | **9,75 %** (escompte 8,75 %) |
| 5 mai 1992 | Taux de base britannique | **10 %** |
| 2 juin 1992 | Référendum danois sur Maastricht | **non à 50,7 %** |
| 3 sept. 1992 | Le Trésor emprunte en devises pour défendre la livre | **≈ 10 Md d'écus** (≈ 7,25 Md £) |
| 13 sept. 1992 | Réalignement : la lire est dévaluée | **≈ 7 %** |
| 14 sept. 1992 | La Bundesbank baisse légèrement ses taux | Lombard **9,50 %**, escompte **8,25 %** |
| 15 sept. 1992 | Interview du président Schlesinger : d'autres réalignements ne sont pas exclus | — |
| 16 sept. 1992 | Taux de base porté à **12 %** à 11 h, **15 %** annoncés à 14 h 15 ; suspension de la participation au MCE le soir | — |
| 20 sept. 1992 | Référendum français | **oui à 51,0 %** |

Une parité fixe à marges est une **promesse conditionnelle** : la banque centrale
s'engage à acheter sa monnaie au plancher, aussi longtemps qu'elle a des réserves
et la volonté politique de monter ses taux. Toute la position porte sur cette
condition.

## 12.2 — Le diagnostic : le trilemme

Le **trilemme de Mundell** énonce qu'un pays ne peut avoir à la fois :

1. un change fixe ;
2. la libre circulation des capitaux ;
3. une politique monétaire autonome.

Dans le MCE, avec des capitaux libres depuis 1979, le Royaume-Uni avait renoncé
au troisième terme : ses taux devaient suivre ceux de la Bundesbank. Or les deux
économies étaient à des **points opposés du cycle** :

| | Royaume-Uni | Allemagne |
|---|---|---|
| Situation | récession 1990-1992, chômage ≈ **10 %** | surchauffe de la réunification |
| Taux nominal court | **10 %** | ≈ **9,7 %** (marché monétaire à 3 mois) |
| Inflation 1992 | ≈ **3,6 %** (août) | ≈ **4 %** |
| **Taux réel** | ≈ **+6,4 %** | ≈ **+5,7 %** |
| Ce qu'il fallait | **baisser** les taux | **monter** les taux |

> 🔑 **Le problème n'était pas le niveau des prix, c'était le cycle.** En 1992
> l'inflation britannique était passée **sous** l'inflation allemande : l'argument
> d'une livre « surévaluée » tenait au cours d'entrée de 1990, pas à une dérive
> depuis. Ce qui rendait la parité intenable était un taux réel de plus de 6 %
> en pleine récession, dans un pays où les crédits immobiliers sont **à taux
> variable** — chaque hausse se transmet aux ménages dès le mois suivant.

C'est la grille du [module 2](02-la-politique-monetaire.md) retournée : il ne
s'agissait pas de deviner la décision d'une banque centrale, mais de juger si sa
**promesse** était soutenable.

## 12.3 — Facteurs favorables et défavorables

**Favorables à la vente de livres :**

| Facteur | Pourquoi il comptait |
|---|---|
| Taux réel insoutenable | défendre le plancher exigeait de **monter** les taux, ce que la récession rendait politiquement impossible au-delà de quelques jours |
| Bundesbank non coopérative | son mandat était l'inflation allemande ; la baisse du 14 septembre (−25 pb de Lombard) était symbolique, et l'interview Schlesinger signalait qu'elle n'irait pas au-delà |
| Contagion en cours | une parité réputée irrévocable venait de céder (la lire) ; le référendum français pouvait faire tomber les autres |
| Asymétrie | la livre cotait au plancher : la perte possible était bornée, le gain non (§ 12.4) |
| Réflexivité | chaque vente consommait les réserves et rendait la défense moins crédible — l'attaque fabriquait son propre résultat |

**Défavorables :**

| Facteur | Ce qu'il pouvait coûter |
|---|---|
| Engagement politique public | le gouvernement répétait qu'il n'y aurait pas de dévaluation ; l'emprunt de 10 Md d'écus en montrait les moyens |
| Squeeze par les taux | un taux à 15 % — et des taux au jour le jour bien plus hauts — rend coûteux d'emprunter des livres pour les vendre |
| Intervention concertée | une défense commune des banques centrales du MCE aurait pu tenir le plancher |
| Réalignement ordonné ou « oui » français net | la confiance revenue, la livre remonte dans sa marge |
| Taille | à ≈ 10 Md $, sortir d'une position perdante aurait elle-même fait monter la livre |

## 12.4 — Les compléments chiffrés

On travaille en **livres vendues contre marks**, au plancher $S_0 = 2{,}778$ DM.
Toutes les pertes et tous les gains sont en pourcentage du nominal.

### Le profil de gain

| Scénario | Cours de la livre | Résultat du vendeur |
|---|---|---|
| La parité tient, la livre reste au plancher | 2,778 DM | ≈ **0 %**, moins le portage |
| La parité tient, la livre remonte au pivot | 2,95 DM | $-\dfrac{2{,}95-2{,}778}{2{,}778}=$ **−6,2 %** |
| La parité casse, livre à 2,50 DM | 2,50 DM | $+\dfrac{2{,}778-2{,}50}{2{,}778}=$ **+10,0 %** |
| La parité casse, livre à 2,40 DM | 2,40 DM | **+13,6 %** |

Le scénario « remontée au pivot » est le pire **réaliste** : rien n'indiquait
qu'une livre défendue à grand-peine reviendrait au milieu de sa marge en quelques
semaines. Le plafond, à 3,132 DM, aurait coûté −12,7 %, mais aucun scénario ne
le rendait plausible.

### La probabilité qui rend la position rentable

Avec un gain $G$ si la parité casse (probabilité $p$) et une perte $L$ sinon,
l'espérance est positive dès que

$$p\,G > (1-p)\,L \quad\Longleftrightarrow\quad p > \frac{L}{G+L}$$

| Perte si la parité tient | Gain si elle casse | Seuil de probabilité |
|---|---|---|
| 6,2 % (retour au pivot) | 10 % | **38 %** |
| 1 % (léger rebond) | 10 % | **9 %** |
| 0,1 % (portage seul, un mois) | 10 % | **1 %** |

> 🔑 **C'est cette ligne qu'il faut lire.** Il n'était pas nécessaire de croire
> la dévaluation **probable** : il suffisait de la juger plus probable que 10 %
> environ, parce que la livre, collée à son plancher, ne pouvait guère monter.
> L'asymétrie fait la position bien plus que la conviction.

### Le coût de portage

Vendre des livres à terme, c'est emprunter des livres pour détenir des marks.
Avec ≈ 10,1 % à Londres et ≈ 9,7 % à Francfort (3 mois) :

| Situation | Écart payé | Coût sur 10 Md $ |
|---|---|---|
| Régime normal, un mois | ≈ 0,4 pt / an × 1/12 = **0,03 %** | ≈ **3 M$** |
| Journée à 15 % | (15 − 9,7) pt / 365 = **0,015 %** | ≈ **1,5 M$** |
| Gain si la livre perd 10 % | — | ≈ **1 000 M$** |

Le portage coûtait **plus de trois cents fois moins** que le gain visé. Même la
hausse à 15 % — l'arme ultime de la Banque d'Angleterre — ne coûtait au vendeur
que deux millièmes environ de ce qu'il espérait, par journée de défense. C'est pourquoi la
hausse des taux, au lieu d'effrayer les vendeurs, les a confirmés : elle montrait
que la banque centrale employait son dernier argument.

### Ce qui s'est passé

| Grandeur | Avant | Après |
|---|---|---|
| Livre contre mark | 2,778 DM (plancher) | ≈ 2,50 DM fin septembre, ≈ **2,40** en octobre, soit **≈ −14 %** |
| Livre contre dollar | ≈ 2,00 $ début septembre | ≈ 1,50 $ début 1993, soit **≈ −25 %** |
| Taux de base | 10 % → 12 % → 15 % (annoncé) | 12 % le 17 sept., 10 % le 22 sept., puis 9 %, 8 %, 7 % (janv. 1993), **6 %** (nov. 1993) |
| Coût pour le Trésor | — | **≈ 3,3 Md £** (estimation du Trésor, publiée en 2005) |
| Position de Quantum | ≈ **10 Md $** vendeurs de livres | gain ≈ **1 Md $** sur la livre |

Le gain annoncé se recoupe avec le profil du tableau : 10 Md $ × ≈ 10 % ≈ 1 Md $.
Les positions annexes rapportées — obligations allemandes, actions et emprunts
d'État britanniques, pariant sur la baisse des taux qui suivrait la sortie — sont
moins bien documentées.

Le 8 octobre 1992, trois semaines après, le Royaume-Uni adopte une **cible
d'inflation** (1 à 4 %), le régime qui sert encore de modèle aux banques
centrales. La croissance repart en 1993. La parité qui devait garantir la
stabilité était devenue l'obstacle ; sa chute a libéré la politique monétaire.

## 12.5 — Était-ce un carry trade ? Non, c'était l'inverse

Un **carry trade** emprunte dans la devise à taux bas, place dans la devise à taux
haut, et **encaisse l'écart en pariant que le change tient**. Son profil est
celui d'un vendeur d'assurance : petit gain régulier, grosse perte rare.

| | Carry trade (« convergence play ») | Position de Soros |
|---|---|---|
| Emprunte | DM ou dollars | livres |
| Détient | livres, lires, pesetas | marks |
| Portage | **positif** | **négatif**, ≈ −0,4 pt / an |
| Pari | la parité tient jusqu'à l'euro | la parité casse |
| Profil | petit gain régulier, perte rare et forte | petite perte régulière, gain rare et fort |

En 1992, le carry trade était **dans le camp d'en face** : de nombreux
investisseurs avaient emprunté en marks ou en dollars pour acheter des devises du
MCE à rendement élevé, en comptant sur une convergence garantie par le traité de
Maastricht. Le « non » danois a remis la garantie en question, et **leur sortie
précipitée** a fourni une bonne part des ventes de livres. Le carry trade n'a pas
été la stratégie de Soros ; il a été le **carburant** de la crise.

> 🔑 **Les deux positions sont la même option, vue des deux côtés.** Le porteur de
> carry vend une assurance contre la dévaluation et touche une prime de
> 0,4 pt par an ; le vendeur de livres l'achète. En septembre 1992, la prime
> était dérisoire au regard du risque qu'elle couvrait : le marché sous-évaluait
> la probabilité de rupture.

## 12.6 — La lecture réflexive

C'est le cas d'école de Soros lui-même, et il illustre le cadre de l'agent
[`sorosien`](../../../../../.claude/agents/sorosien.md) mieux qu'une bulle
boursière :

1. **Le fondamental dépend du prix.** La « valeur » de la parité n'existe pas
   indépendamment des opérateurs : elle tient tant qu'on croit qu'elle tiendra.
2. **La boucle.** Ventes → réserves consommées → hausse de taux → récession
   aggravée → défense moins crédible → nouvelles ventes.
3. **Le point de rupture est politique**, pas économique : il est atteint quand
   le coût de la défense pour l'électorat dépasse le coût de l'abandon.

Ce n'est **pas** un cycle boom-bust complet : il n'y a ni emballement initial des
cours, ni tendance auto-entretenue sur des années. C'est un **équilibre loin de
l'équilibre** — un prix maintenu artificiellement, dont la rupture est brutale.

## 12.7 — Ce que le cas ne permet pas de conclure

> ⚠️ **Un cas célèbre est sélectionné par son résultat.** On étudie 1992 parce
> que la position a gagné. C'est le **biais du survivant** du
> [module 4 du cours alpha](../alpha/04-cinq-pieges.md) : les attaques contre
> des parités qui ont tenu — et les fonds qui les ont menées — ne figurent dans
> aucun manuel. Le même Quantum a perdu de l'ordre de 2 Md $ en Russie en 1998,
> et ses gérants ont reconnu d'autres revers lourds.

- **Un épisode ne mesure rien.** Un seul événement ne permet ni d'estimer une
  probabilité de rupture, ni de tester une règle. C'est la leçon de
  l'[expérience 10](../../../../done/experimentation/experience_10/README.md) :
  un garde-fou éprouvé sur un unique épisode n'est pas éprouvé.
- **Le raisonnement est reproductible, pas le résultat.** Ce qu'on peut retenir
  est une **méthode de diagnostic** — une promesse de change contredite par le
  taux réel qu'elle impose — et une **méthode de calcul** — le seuil
  $p > L/(G+L)$. Ni l'une ni l'autre ne dit quand une parité cède.
- **Le calendrier a été décidé par des faits imprévisibles** : l'interview
  Schlesinger, le référendum danois. Un diagnostic juste en 1991 aurait porté
  un an de portage négatif sans aucun gain.
- **La taille n'est pas transposable.** Une position de 10 Md $ influe sur le
  prix qu'elle parie ; c'est une partie de ce qui l'a fait gagner. Le
  dimensionnement relève du [cours finance](../finance/README.md), pas d'un récit.

## Exercices

**E12.1.** Recalculer le seuil de probabilité du § 12.4 si la livre ne tombe qu'à
2,65 DM après la rupture, la perte en cas de maintien restant de 1 %.
*Que devient l'asymétrie ?*

**E12.2.** Un porteur de carry détient des lires financées en marks, avec un
écart de taux de 3 pt par an. La lire perd 7 % le 13 septembre. Combien d'années
de portage cette journée efface-t-elle ? *Rapprocher du profil « vendeur
d'assurance » du § 12.5.*

**E12.3.** Avec le taux de 15 % maintenu tout un mois, que coûte le portage sur
10 Md $ ? Combien de mois une telle défense devrait-elle durer pour égaler le gain
visé ? *Pourquoi la menace n'était-elle pas crédible ?*

## Ce qu'il faut retenir

1. Une parité fixe est une **promesse conditionnelle** ; la position porte sur sa
   soutenabilité, que le **taux réel** imposé permet de juger.
2. Au plancher, le profil est **asymétrique** : perte bornée à quelques
   pourcents, gain de 10 à 15 %. Un seuil de probabilité d'environ **10 %**
   suffisait.
3. Le portage était **négatif mais négligeable** : ≈ 0,03 % par mois contre
   ≈ 10 % visés.
4. Ce n'était **pas** un carry trade, mais son inverse ; le carry trade était
   le carburant de la crise.
5. Un cas unique et célèbre **n'établit rien** : il illustre un raisonnement,
   il ne valide pas une règle.

> ⚠️ **Ce module ne donne aucun conseil en investissement.** Il décrit une
> position historique et le raisonnement qui la sous-tendait ; il ne dit ni
> quelle parité attaquer, ni quand.

---

⬅️ [Module 11 — Exemple chiffré : huit valeurs du CAC 40](11-exemple-chiffre-huit-valeurs.md) ·
➡️ [Module 13 — Cas d'étude : la livre turque, 2025](13-cas-d-etude-livre-turque-2025.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
