# Module 5 — La croissance : PIB et PMI

**Prérequis :** [module 2 du cours fondamentaux](../fondamentaux/02-les-quatre-dates-d-un-ratio.md).
**Ce qu'on établit ici :** que le marché anticipe l'activité au lieu de la suivre, qu'une statistique macro publiée porte plusieurs dates comme un ratio comptable, et qu'une étude faite sur la série révisée regarde en avant.

---

## 5.1 — Le marché avance, le PIB suit

Le PIB mesure l'activité d'un trimestre écoulé. Le cours d'une action actualise
les bénéfices **à venir**. Il n'y a donc aucune raison que le second suive le
premier : c'est plutôt l'inverse. Le marché baisse **avant** que la récession soit
constatée, et remonte **avant** qu'elle soit terminée.

Conséquence : la corrélation entre la croissance publiée d'un trimestre et le
rendement du même trimestre est faible, et celle entre la croissance publiée et le
rendement **suivant** encore plus faible. L'information est dans les prix avant
d'être dans la statistique.

## 5.2 — Le PMI : plus rapide, pas plus prédictif

Les indices des directeurs d'achat (PMI) sont des **enquêtes** : chaque mois, des
entreprises disent si leur activité, leurs commandes et leurs prix montent ou
baissent. Ils sont publiés dans les premiers jours du mois suivant, bien avant le
PIB, et ne sont presque pas révisés.

C'est un avantage réel pour **suivre** l'économie. Ce n'en est pas un pour
**prévoir** les actions : le marché intègre le PMI le jour de sa publication, et
seule la **surprise** par rapport au consensus fait bouger les cours, comme pour
la politique monétaire ([module 2](02-la-politique-monetaire.md)). Une fois connu,
le PMI n'a plus de pouvoir prédictif notable sur les rendements.

## 5.3 — Les dates d'une statistique

Le [module 2 du cours fondamentaux](../fondamentaux/02-les-quatre-dates-d-un-ratio.md)
distingue quatre dates dans un ratio comptable. Une statistique macro en a autant,
et la même qui manque :

| Date | Pour le PIB du 1er trimestre |
|---|---|
| période mesurée | janvier à mars |
| **première publication** | fin avril (estimation « flash ») |
| révisions | fin mai, puis chaque année pendant plusieurs années |
| lecture | le jour où l'on télécharge la série |

Une série téléchargée aujourd'hui donne pour chaque trimestre sa **dernière**
valeur révisée. Ce n'est pas celle que le marché a lue en avril. L'écart n'est pas
un détail : une révision peut changer le signe d'une croissance trimestrielle, donc
transformer après coup un trimestre « de récession » en trimestre de croissance.

> ⚠️ **Tester une règle sur la série révisée, c'est lui donner la connaissance du
> futur.** C'est l'interdit du dépôt « jamais de regard en avant », dans sa
> version macroéconomique. Il se corrige de la même façon que pour les comptes :
> en utilisant la valeur **telle que publiée** à chaque date.

## 5.4 — Les millésimes

Les bases qui conservent chaque version publiée d'une série s'appellent des bases
de **millésimes** (*vintages*, ou *real-time data*). Croushore & Stark (2001) ont
construit la première de référence pour les États-Unis ; la Fed de Saint-Louis en
maintient une, ALFRED, pour des milliers de séries.

Une étude honnête d'un lien entre croissance publiée et rendement demande donc :

1. la série **millésimée**, pas la série révisée ;
2. la **date de publication** de chaque valeur, pour ne l'utiliser qu'à partir
   de ce jour ;
3. le **consensus** de la veille, pour en extraire la surprise.

Le dépôt n'a aucune des trois. Yahoo ne diffuse pas de séries macro publiées. Ce
module ne contient donc aucun chiffre mesuré ici, et c'est délibéré : un chiffre
calculé sur une série révisée serait pire que pas de chiffre.

## Ce qu'il faut retenir

1. Le marché anticipe la croissance : le PIB publié est en retard sur les cours.
2. Le PMI est plus rapide que le PIB, mais seule sa surprise fait bouger les cours.
3. Une statistique macro est publiée puis **révisée** : la série d'aujourd'hui
   n'est pas celle qu'on connaissait alors.
4. Étudier un lien avec la croissance exige des **millésimes**. Sans eux, on
   regarde en avant.

---

⬅️ [Module 4 — La pente de la courbe des taux](04-la-pente-de-la-courbe.md) ·
➡️ [Module 6 — Le change](06-le-change.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
