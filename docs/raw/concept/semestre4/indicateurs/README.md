# Cours — Les dix indicateurs de Soros et Steinhardt

Le [cours fondamentaux](../fondamentaux/README.md) apprend à lire un ratio. Le
[cours macro](../macro/README.md) apprend à mesurer ce qui relie un cours au monde
autour. Aucun des deux ne dit **comment des investisseurs qui ont réussi s'en
servaient**. Ce cours le fait, à partir de deux d'entre eux : George Soros et
Michael Steinhardt. Deux méthodes très différentes, qui partagent pourtant une
même idée : **un fondamental ne vaut rien seul, il vaut par son écart avec ce
que le marché croit.**

Le cours retient **dix indicateurs**. Pour chacun il dit comment le **chiffrer**
avec les sources de ce dépôt, comment le **lire**, et ce qu'il **ne permet pas de
conclure**. Il se termine sur une fiche à remplir, et un script qui la remplit
pour n'importe quelle valeur.

Niveau bac+2. Prérequis : le [cours fondamentaux](../fondamentaux/README.md) en
entier, les modules [1](../macro/01-le-taux-d-actualisation.md),
[4](../macro/04-la-pente-de-la-courbe.md), [6](../macro/06-le-change.md),
[8](../macro/08-le-credit.md) et [10](../macro/10-des-facteurs-a-la-prevision.md)
du cours macro, et le [module 4 du cours alpha](../alpha/04-cinq-pieges.md)
(tests multiples). Aucune connaissance de Soros ni de Steinhardt n'est supposée.

## Pourquoi ce cours

Parce qu'on cite Soros et Steinhardt bien plus souvent qu'on ne les applique,
et que les dix indicateurs qu'on leur prête se mesurent presque tous, mais se
lisent presque toujours mal.

| Ce qu'on croit | Ce qu'il en est | Module |
|---|---|---|
| « Soros et Steinhardt avaient une liste d'indicateurs. » | Aucun des deux n'en a publié. Les dix de ce cours sont **reconstitués** à partir de leurs livres, et une méthode qu'on n'a pas écrite ne se teste pas | [01](01-l-ecart-a-l-opinion.md) |
| « Le consensus monte, c'est un bon signe. » | Les analystes relèvent leur BPA attendu pour Orange de **36,3 %** en 90 jours… avec une dispersion de **88 %** entre l'estimation haute et la basse. Sur une base proche de zéro, une révision ne mesure presque rien | [02](02-les-attentes-de-benefices.md) |
| « Sanofi a un PER de 22 et un PER prévisionnel de 8 : son bénéfice va presque tripler. » | Les deux PER ne divisent pas le même bénéfice. Le premier divise le BPA comptable (**3,25 €**), le second le « BPA des activités » que suit le consensus (**8,60 €**) | [02](02-les-attentes-de-benefices.md) |
| « TotalEnergies a vu son PER passer de 7,1 à 13,0 : le marché s'emballe. » | Son cours a **monté**, mais son bénéfice a **chuté** de 36,1 points de log depuis le sommet de 2022. Le PER d'une valeur cyclique monte quand son bénéfice baisse : c'est le **paradoxe du PER cyclique** | [03](03-le-prix-des-attentes.md) |
| « Un groupe dont le BPA croît de 60 % est un groupe qui croît. » | Une société payée 40 fois ses bénéfices qui en absorbe une payée 10 fois **en émettant des actions** fait croître son BPA de **60 %** sans rien vendre de plus. C'est le mécanisme des conglomérats décrit par Soros | [05](05-levier-et-dilution.md) |
| « Les taux ont monté, le crédit va se tarir. » | Au 8 octobre 2026, la BCE a monté son taux de dépôt de 0,50 point en un an, mais les prêts aux entreprises de la zone euro croissent de **4,2 %**, contre 3,0 % un an plus tôt | [06](06-taux-et-credit.md) |
| « Airbus est un exportateur en dollars, sa sensibilité au change est établie. » | Sur 18 ans, oui ($t = -6{,}16$). Sur les trois dernières années, **non** ($t = -1{,}86$, $p = 0{,}065$) : 156 semaines ne suffisent pas à établir ce que 933 établissent | [07](07-change-croissance-inflation.md) |
| « Aucune position courte publiée : personne ne parie contre la valeur. » | L'AMF ne publie une position qu'à partir de **0,5 %** du capital. Cent vendeurs à 0,4 % chacun restent invisibles | [08](08-le-positionnement.md) |
| « Trois marqueurs de boom sur quatre : la valeur est dans une bulle. » | Un marqueur n'est pas un canal. Sans mécanisme par lequel le **cours nourrit le fondamental**, il n'y a pas de boucle réflexive, seulement une valorisation exigeante | [09](09-assembler-la-sequence.md), [10](10-exemple-chiffre-huit-valeurs.md) |

## Le fil directeur

> 🔑 **Un fondamental se lit en écart, jamais en niveau.** Steinhardt appelait
> *variant perception* le fait d'avoir une vue fondée et **sensiblement
> différente** du consensus. Soros appelait *biais dominant* ce que le marché
> croit, et cherchait le moment où la réalité s'en écarte. Les deux reviennent à
> la même opération : mesurer ce que le cours **suppose**, mesurer ce qui
> **est**, et s'intéresser à la différence. Un PER de 30 ne dit rien ; un PER de
> 30 qui suppose une croissance de 4,7 % par an pour toujours, quand le
> consensus n'en voit que pour deux ans, dit quelque chose.

Les dix indicateurs se rangent en quatre questions :

| Question | Indicateurs | Modules |
|---|---|---|
| Que gagne l'entreprise, et que croit-on qu'elle gagnera ? | 1 attentes · 4 multiples · 6 marges | [02](02-les-attentes-de-benefices.md), [03](03-le-prix-des-attentes.md), [04](04-les-marges.md) |
| Comment finance-t-elle sa croissance ? | 5 levier · 7 dilution | [05](05-levier-et-dilution.md) |
| Dans quel monde ? | 2 taux · 3 crédit · 8 change · 9 croissance et inflation | [06](06-taux-et-credit.md), [07](07-change-croissance-inflation.md) |
| Que croient les autres ? | 10 positionnement | [08](08-le-positionnement.md) |

## Plan

| # | Module | Ce qu'il établit |
|---|---|---|
| 1 | [L'écart à l'opinion](01-l-ecart-a-l-opinion.md) ⭐ | Réflexivité et biais dominant chez Soros, *variant perception* chez Steinhardt ; ce qui est documenté et ce qui est reconstitué ; les trois écarts qui donnent un sens à un chiffre ; la fiche type d'un indicateur |
| 2 | [Indicateur 1 — Les attentes de bénéfices](02-les-attentes-de-benefices.md) ⭐ | Consensus, révision, diffusion, dispersion, surprise ; deux définitions du BPA ; l'effet de base ; ce que serait une vue divergente chiffrée |
| 3 | [Indicateur 4 — Le prix des attentes](03-le-prix-des-attentes.md) ⭐ | Croissance implicite, prime de rendement, décomposition du rendement en bénéfice, multiple et dividendes ; le paradoxe du PER cyclique |
| 4 | [Indicateur 6 — Les marges](04-les-marges.md) | Marge contre sa moyenne ; volume contre marge ; retour à la moyenne ; la double extrapolation |
| 5 | [Indicateurs 5 et 7 — Comment la hausse se finance](05-levier-et-dilution.md) ⭐ | Dette/EBITDA, couverture des intérêts, dynamique du levier ; dilution et rachats ; le conglomérat chiffré, ou la croissance fabriquée par le cours |
| 6 | [Indicateurs 2 et 3 — Le prix et la quantité de l'argent](06-taux-et-credit.md) | Taux directeur, pente, taux réel, prime de rendement ; croissance du crédit contre croissance nominale ; l'écart crédit/PIB de la BRI ; la boucle du collatéral |
| 7 | [Indicateurs 8 et 9 — Le monde autour](07-change-croissance-inflation.md) | Sensibilité au change sur trois ans et sur dix-huit ; Holm ; croissance nominale, inflation et millésimes |
| 8 | [Indicateur 10 — Ce que croient les autres](08-le-positionnement.md) | Les positions courtes publiées de l'AMF et leur seuil ; le volume relatif ; pourquoi l'indicateur décisif est le moins mesurable |
| 9 | [Assembler : la séquence et la règle écrite](09-assembler-la-sequence.md) ⭐ | Les huit stades du boom-bust traduits en marqueurs ; seuils déclarés avant la mesure ; ce qu'une combinaison ne permet pas de dire ; la thèse réfutable |
| 10 | [Exemple chiffré : huit valeurs du CAC 40](10-exemple-chiffre-huit-valeurs.md) | Les dix indicateurs mesurés le 8 octobre 2026 et lus valeur par valeur, y compris les cases vides |
| 11 | [La fiche, à remplir](11-la-fiche-a-remplir.md) ⭐ | La procédure en sept étapes, le modèle de fiche, et un exercice sur une valeur que le cours n'a pas traitée |

**11 modules · 11 h.**

## Le fil rouge chiffré

Tous les nombres du cours sortent d'un seul script, versionné à côté de lui :
[`figures/mesurer_indicateurs.py`](figures/mesurer_indicateurs.md).

```bash
python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py
python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py SU.PA AIR.PA
python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py KER.PA --isin KER.PA=FR0000121485
```

Sans argument, il fiche les **huit valeurs du cours fondamentaux** — Airbus, LVMH,
L'Oréal, Sanofi, TotalEnergies, BNP Paribas, Schneider Electric, Orange — à
partir de cinq sources :

| Source | Ce qu'elle fournit | Indicateurs |
|---|---|---|
| Yahoo (`yfinance`) | cours, comptes annuels, nombre d'actions, consensus des analystes | 1, 4, 5, 6, 7, 8, 10 |
| BCE | taux de dépôt, courbe des taux AAA de la zone euro, prêts aux entreprises | 2, 3 |
| Eurostat | inflation et PIB de la zone euro | 9 |
| BRI | écart du crédit au PIB à sa tendance, France | 3 |
| AMF (data.gouv.fr) | positions courtes nettes publiées, avec leurs dates | 10 |

> ⚠️ **Les chiffres du cours datent du 8 octobre 2026 et ne se reproduisent pas à
> l'identique.** Le consensus change chaque semaine, les cours à chaque séance,
> les comptes à chaque publication. Ce sont les **relations** et les **lectures**
> qu'il faut retenir, pas les valeurs. Relancer le script donne la fiche du jour.

> ℹ️ **Le cours macro mesurait le taux américain par procuration** : Yahoo ne
> sert aucun taux de la zone euro. Ce cours va les chercher **à la BCE**, par
> `urllib`. Le taux à 10 ans cité ici est donc celui de la courbe AAA de la zone
> euro.

## Ce que ce cours alimente

- L'**agent [`sorosien`](../../../../../.claude/agents/sorosien.md)** : le canal de
  transmission qu'il cherche entre cours et fondamentaux se lit dans les
  indicateurs 5 et 7 ([module 5](05-levier-et-dilution.md)), et sa réponse par
  défaut, « aucune séquence réflexive identifiable », est justifiée au
  [module 9](09-assembler-la-sequence.md).
- L'**agent [`trading`](../../../../../.claude/agents/trading.md)** : le
  [module 9](09-assembler-la-sequence.md) dit pourquoi ces indicateurs ne
  deviennent pas une règle d'achat, et sous quelle forme ils peuvent entrer dans
  un registre de thèses.
- Le [cours trading](../trading/README.md), qui suit : il construit une règle sur
  des critères de **prix**. Ce cours montre ce qu'il faudrait pour y ajouter un
  critère fondamental, et pourquoi ce n'est pas faisable ici.

> ⚠️ **Ce cours ne donne aucun conseil en investissement.** Il explique comment
> chiffrer et lire dix indicateurs, et surtout ce qu'ils ne permettent pas de
> conclure. Aucun des chiffres qu'il contient ne désigne une valeur à acheter ou
> à vendre, ni un moment pour le faire. Soros et Steinhardt ont aussi perdu de
> l'argent avec ces indicateurs.

---

➡️ Commencer par le [module 1 — L'écart à l'opinion](01-l-ecart-a-l-opinion.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
