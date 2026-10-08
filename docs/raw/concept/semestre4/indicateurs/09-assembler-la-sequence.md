# Module 9 — Assembler : la séquence et la règle écrite ⭐

**Prérequis :** les modules [1](01-l-ecart-a-l-opinion.md) à [8](08-le-positionnement.md), le [module 4 du cours alpha](../alpha/04-cinq-pieges.md) (tests multiples), et le [module 3 du cours trading](../trading/03-la-regle-ecrite-a-l-avance.md) si on l'a déjà lu.
**Ce qu'on établit ici :** comment passer de dix indicateurs isolés à une lecture de la séquence boom-bust, avec des seuils écrits **avant** la mesure ; ce qu'une combinaison de marqueurs permet de dire, et la liste, plus longue, de ce qu'elle ne permet pas.

---

## 9.1 — Les huit stades du boom-bust

Soros décrit dans *L'Alchimie de la finance* un boom-bust type en huit stades.
Les voici, traduits en ce que les indicateurs du cours peuvent en voir :

| Stade | Ce qui se passe | Ce que les indicateurs montrent |
|---|---|---|
| 1. Tendance non reconnue | les fondamentaux s'améliorent, le marché ne le voit pas | bénéfice qui monte, multiple bas ; consensus en retard |
| 2. Début de l'auto-renforcement | la tendance est reconnue, le biais l'amplifie | **révisions en hausse** (B1) ; la part du bénéfice domine encore |
| 3. Épreuve réussie | une correction est surmontée, la conviction en sort renforcée | visible dans le prix seul |
| 4. Accélération | l'écart entre attentes et réalité se creuse ; le prix finance la hausse | **multiple qui porte la hausse** (B2), **levier qui monte** (B3), **émissions** (B4), crédit au-dessus du PIB |
| 5. Moment de vérité | la réalité ne suit plus les attentes | **révisions en baisse** alors que le multiple a porté la hausse (R1) ; marge haute et croissance implicite exigeante (R2) |
| 6. Crépuscule | on continue sans y croire | prix qui stagne, volume élevé, **positions courtes en hausse** (R3) |
| 7. Point de bascule | le biais s'inverse | le multiple commence à baisser |
| 8. Krach | l'auto-renforcement joue à la baisse | multiple **et** bénéfice en baisse, le canal fonctionnant à l'envers |

Deux remarques avant de s'en servir.

- **Les stades se reconnaissent après coup.** Soros les a tirés de cas terminés.
  Au moment où l'on est au stade 4, rien ne dit qu'il ne s'agit pas du stade 2
  d'une tendance qui durera dix ans.
- **Tous les cycles ne passent pas par tous les stades**, et beaucoup de hausses
  ne sont pas des booms : elles s'arrêtent sans krach, parce qu'aucun canal ne
  les rendait auto-entretenues.

## 9.2 — Les marqueurs, et leurs seuils écrits à l'avance

Le script [`mesurer_indicateurs.py`](figures/mesurer_indicateurs.md) traduit les
stades 2, 4, 5 et 6 en **sept marqueurs**, chacun défini par un seuil :

| | Marqueur | Condition | Stade |
|---|---|---|---|
| **B1** | révisions en hausse | révision du BPA de l'exercice en cours sur 90 jours $\ge +2\,\%$ | 2 |
| **B2** | hausse portée par le multiple | sur 3 ans : cours en hausse, bénéfice en hausse, et part du multiple $>$ part du bénéfice | 4 |
| **B3** | levier qui monte | croissance de la dette − croissance de l'EBITDA $> +10$ points | 4 |
| **B4** | émission | nombre d'actions sur un an $> +2\,\%$ | 4 |
| **R1** | moment de vérité | révision $\le -2\,\%$, **et**, sur 3 ans, cours en hausse et part du multiple $> 0$ | 5 |
| **R2** | double extrapolation | marge op. $> 2$ points au-dessus de sa moyenne **et** croissance implicite $> 3\,\%$ | 5 |
| **R3** | vendeurs en hausse | positions courtes publiées en hausse de plus de 0,5 point sur 90 jours | 6 |

Les seuils sont **ronds**, et ils le sont exprès : 2 %, 10 points, 0,5 point. Ils
n'ont été optimisés sur rien. On ne pourrait d'ailleurs pas les optimiser : le
consensus n'a pas d'historique dans le dépôt, les comptes n'en ont que quatre
ans. Un seuil qu'on ne peut pas étalonner doit être une **convention déclarée**,
et non un nombre qu'on ajuste jusqu'à ce que le résultat plaise.

> ⚠️ **Deux corrections ont été faites, et elles se déclarent.** La première
> version de B2 ne demandait pas un bénéfice en hausse. Au premier relevé, elle
> s'est allumée sur TotalEnergies et Orange, deux valeurs dont le bénéfice
> s'était **effondré** : le paradoxe du PER cyclique du [module 3](03-le-prix-des-attentes.md).
> R1, lui, ne demandait pas de hausse du cours ; il s'est allumé sur Kering, dont
> le cours **baissait** et dont le bénéfice s'était effondré. Dans le vocabulaire
> de la [revue d'expérience](../../../../done/experimentation/experience_1/review.md),
> ce sont des corrections de **catégorie B** : suggérées par un résultat. Elles
> restent recevables pour trois raisons, qui sont la règle du dépôt : rien
> n'avait été publié, la **cause** est identifiée (un mécanisme, le même dans les
> deux cas, pas une préférence), et chaque correction est consignée dans le
> [miroir du script](figures/mesurer_indicateurs.md). La seconde a d'ailleurs été
> trouvée sur une valeur que le cours n'avait pas servi à construire.

## 9.3 — Quatre verdicts, et un défaut

Les marqueurs ne disent rien un par un. La lecture qui en tire quelque chose
suit le [module 5](05-levier-et-dilution.md) : **sans canal, pas de boucle**.

Les règles s'appliquent **dans l'ordre**, et la première qui s'applique donne le
verdict :

| Ordre | Configuration | Verdict |
|---|---|---|
| 1 | R1 ou R2, sur une valeur déjà jugée « séquence candidate » | **bascule candidate** |
| 2 | (B1 ou B2) **et** (B3 ou B4) | **séquence candidate**, canal à vérifier : dette (B3) ou actions (B4) |
| 3 | B2, ou croissance implicite exigeante | **valorisation exigeante** — sans boucle mesurée |
| 4 | tout le reste | **aucune séquence réflexive identifiable** — le défaut |

Un marqueur `?` — non mesurable — ne compte ni pour ni contre : il interdit
seulement de conclure à partir de lui.

Le mot important est **candidate**. Un marqueur B3 dit que la dette a crû plus
vite que l'EBITDA ; il ne dit pas qu'elle a financé la hausse du cours, ni même
quoi que ce soit lié au cours. Pour passer de « candidate » à « identifiée », il
faut lire le **rapport annuel** : qu'a financé la dette ? Une acquisition payée
au prix fort ? Un rachat d'actions ? Un investissement industriel ordinaire ?
Seule la première réponse ressemble au mécanisme de Soros.

> 🔑 **Le défaut est l'absence de séquence.** C'est la réponse de l'agent
> [`sorosien`](../../../../../.claude/agents/sorosien.md), et ce n'est pas de la
> prudence de principe. La plupart des hausses ne sont pas réflexives, et un
> cadre qui en voit partout ne distingue plus rien.

## 9.4 — Ce qu'une combinaison ne permet pas de dire

**Pas de date.** Une séquence candidate peut durer des années. Soros lui-même
distinguait le diagnostic — « c'est un boom » — de la position, qui dépend du
moment, du coût de portage et de la taille, et relève du
[cours finance](../finance/README.md).

**Pas de significativité.** Sept marqueurs sur huit valeurs, ce sont 56 tests
lus en même temps. Le hasard en allume. Un calcul simple le montre : si chacun
des quatre marqueurs de boom s'allumait **au hasard**, indépendamment, avec une
probabilité de 20 %, la probabilité qu'une valeur en montre au moins trois sur
quatre vaudrait

$$4 \times 0{,}2^3 \times 0{,}8 + 0{,}2^4 = 0{,}0272$$

et la probabilité qu'**au moins une** des huit valeurs y parvienne

$$1 - (1 - 0{,}0272)^8 \approx 19{,}8\,\%$$

Une fois sur cinq, sans aucun signal. La probabilité de 20 % est une hypothèse
d'école, pas une mesure. Mais elle dit l'ordre de grandeur, et elle dit pourquoi
une valeur à « 3 sur 4 » dans un tableau de huit n'est pas une découverte. C'est
la leçon du [module 4 du cours alpha](../alpha/04-cinq-pieges.md), et celle de
l'[expérience 13](../../../../done/experimentation/experience_13/bilan.md) : un
garde-fou non corrigé se déclenche plus souvent que ce qu'il protège.

**Pas de backtest.** On ne peut pas vérifier que ces marqueurs annoncent quoi que
ce soit : il faudrait leur historique, et le consensus n'en a pas ici. Chaque
lecture est un **instantané** du jour.

**Pas de conseil.** Un verdict de séquence candidate ne dit pas d'acheter, de
vendre ni d'attendre. Il dit où chercher.

## 9.5 — De la lecture à la thèse réfutable

Ce qui transforme cette grille en connaissance, c'est la même discipline que
pour la vue divergente du [module 2](02-les-attentes-de-benefices.md) : écrire,
**avant**, ce qui donnerait tort.

| Rubrique | Contenu |
|---|---|
| **Lecture** | le verdict du § 9.3, avec les marqueurs qui le fondent |
| **Canal** | ce qu'a financé la dette ou l'émission, d'après le rapport annuel |
| **Thèse** | une affirmation sur une grandeur **mesurable** à une date fixée |
| **Réfutation** | la valeur de cette grandeur qui donnerait tort |
| **Date** | quand on relancera le script pour juger |

La thèse doit porter sur ce que le script mesure, pas sur le cours : « au
8 octobre 2027, la part du multiple dans la décomposition sur trois ans sera
inférieure à la part du bénéfice » se vérifie d'une commande. « L'action va
baisser » ne dit ni de combien, ni quand, ni pourquoi.

C'est le **registre de thèses** de l'[expérience 2](../../../../done/experimentation/experience_2/README.md),
appliqué aux fondamentaux. Son intérêt n'est pas de gagner, mais de **compter** :
au bout de vingt thèses, on sait combien étaient justes, et la grille cesse
d'être une opinion.

## 9.6 — Pourquoi ce n'est pas une règle de trading

Le [cours trading](../trading/README.md) construit une règle sur des critères de
prix, et le [module 2 du cours fondamentaux](../fondamentaux/02-les-quatre-dates-d-un-ratio.md)
explique déjà pourquoi aucun critère fondamental n'y figure. Ce cours ajoute deux
raisons :

1. **Le consensus n'a pas d'historique** : aucune règle fondée sur B1 ou R1 ne peut
   être testée sur le passé, ni même rejouée.
2. **L'effet minimal détectable** : avec une tracking error de 8 à 16 % par an,
   une règle jouée sur un an ne peut établir un alpha inférieur à ±16 à ±30
   points (invariant du dépôt, mesuré par les expériences). Une grille de dix
   indicateurs ne change rien à cette arithmétique.

Ces indicateurs servent donc à **poser des questions** et à **écrire des thèses**,
pas à passer des ordres.

## Exercices

**E9.1.** Donner le verdict du § 9.3 pour chaque configuration : (a) B1 seul ;
(b) B2 et B4 ; (c) croissance implicite de 5 %, aucun marqueur ; (d) B1, B3, puis,
six mois plus tard, R1 ; (e) croissance implicite de 5 % et B3, sans B1 ni B2.

**E9.2.** Refaire le calcul du § 9.4 avec une probabilité de 10 % par marqueur.
Puis avec 20 % et **quarante** valeurs.

**E9.3.** Réécrire en thèse réfutable : « Schneider est trop chère ».

**E9.4.** Pourquoi un seuil qu'on ne peut pas étalonner doit-il être rond ?

### Corrigés

**E9.1.** (a) aucune séquence identifiable — une révision sans canal. (b) séquence
candidate, canal des actions, à vérifier dans les communiqués d'acquisition.
(c) valorisation exigeante. (d) séquence candidate puis bascule candidate — à
condition d'avoir vérifié le canal entre-temps. (e) valorisation exigeante : la
dette monte, mais aucune hausse d'opinion mesurée ne l'accompagne — la règle 2
ne s'applique pas, la règle 3 si. C'est le cas de L'Oréal au
[module 10](10-exemple-chiffre-huit-valeurs.md).

**E9.2.** À 10 % : $4 \times 0{,}001 \times 0{,}9 + 0{,}0001 = 0{,}0037$ par valeur, et
$1 - 0{,}9963^8 \approx 2{,}9\,\%$ sur huit valeurs. À 20 % sur quarante valeurs :
$1 - 0{,}9728^{40} \approx 67\,\%$ — deux fois sur trois, au moins une valeur du
CAC 40 montre trois marqueurs sur quatre **sans aucun signal**.

**E9.3.** Par exemple : « Au 8 octobre 2027, la croissance implicite de Schneider
calculée par le script sera inférieure à 4 % ». Réfutée si elle est $\ge 4\,\%$.
Date : 8 octobre 2027. Elle dit ce que « trop chère » voulait dire — une
croissance supposée excessive — sous une forme qui peut être fausse.

**E9.4.** Un seuil précis (2,37 %) laisse supposer qu'il a été ajusté, et invite à
le réajuster. Un seuil rond affiche qu'il est une convention, ce qui empêche de
le déplacer sans le dire.

## Ce qu'il faut retenir

1. Les **huit stades** de Soros se traduisent en sept marqueurs, dont les seuils
   sont **déclarés avant** la mesure et ronds parce qu'ils ne peuvent pas être
   étalonnés.
2. **Sans canal, pas de boucle** : le verdict par défaut est « aucune séquence
   réflexive identifiable » ; une séquence n'est que **candidate** tant que le
   rapport annuel n'a pas dit ce que la dette ou l'émission a financé.
3. 56 marqueurs lus ensemble s'allument **par hasard** : une valeur à 3 sur 4
   parmi huit arrive une fois sur cinq sans signal.
4. La grille sert à écrire des **thèses réfutables** sur des grandeurs mesurables,
   pas à décider d'une position.

---

⬅️ [Module 8 — Ce que croient les autres](08-le-positionnement.md) ·
➡️ [Module 10 — Exemple chiffré : huit valeurs du CAC 40](10-exemple-chiffre-huit-valeurs.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
