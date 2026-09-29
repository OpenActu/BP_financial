# Module 10 — Des facteurs à la prévision ⭐

**Prérequis :** modules [1](01-le-taux-d-actualisation.md) à [9](09-la-correlation-actions-obligations.md), [module 4 du cours alpha](../alpha/04-cinq-pieges.md).
**Ce qu'on établit ici :** la différence entre un facteur de risque, qui explique les rendements **en même temps**, et un prédicteur, qui les annonce ; pourquoi presque aucun prédicteur macro ne survit hors échantillon ; et la statistique qui permet de le vérifier.

---

## 10.1 — Deux questions différentes

Les modules 1 à 9 posent deux types de question, qu'il faut maintenant séparer :

| | Facteur | Prédicteur |
|---|---|---|
| Question | le titre **bouge-t-il avec** la variable ? | la variable **annonce-t-elle** le titre ? |
| Régression | $r_t$ sur $x_t$ | $r_{t+1}$ sur $x_t$ |
| $R^2$ typique | 30 à 60 % (marché compris) | < 1 % |
| Utilité | mesurer une exposition, couvrir | décider d'une position |
| Menace principale | l'instabilité ([module 9](09-la-correlation-actions-obligations.md)) | le surapprentissage |

Un facteur n'a pas besoin de prédire pour être utile : savoir qu'Airbus perd
0,6 % quand l'euro gagne 1 % permet de mesurer et de couvrir une exposition. Mais
**il ne dit pas quand acheter**.

## 10.2 — Les facteurs macro : Chen, Roll et Ross

Chen, Roll & Ross (1986) cherchent si des variables macro sont des **facteurs de
risque rémunérés** : les titres qui y sont plus exposés rapportent-ils plus, en
moyenne ? Ils retiennent la production industrielle, l'inflation inattendue,
l'écart de crédit et la pente de la courbe, et trouvent des primes significatives
sur 1958-1984.

Le résultat est fragile. Shanken & Weinstein (2006) le réexaminent avec d'autres
choix de méthode (construction des portefeuilles, estimation des bêtas) : la
plupart des primes perdent leur significativité, sauf celle de la production
industrielle, qui elle-même dépend des choix. Les **sensibilités** existent ; leur
**rémunération** n'est pas établie.

## 10.3 — Le $R^2$ hors échantillon

Pour juger un prédicteur, la seule question qui compte est : aurait-il fait mieux,
**en temps réel**, que la prévision la plus naïve, la moyenne historique ?

On procède mois par mois. Au mois $i$, on estime la régression $r_{t+1} = a + b\,x_t$
**sur le seul passé** (les mois $1 \dots i-1$), on prévoit $\hat r_i$, et on note
aussi la moyenne historique $\bar r_{1..i-1}$. Puis :

$$R^2_{\text{hors}} = 1 - \frac{\sum_i (r_i - \hat r_i)^2}{\sum_i (r_i - \bar r_{1..i-1})^2}$$

C'est la statistique de Campbell & Thompson (2008). Elle vaut :

- **> 0** si le prédicteur a fait mieux que la moyenne historique ;
- **< 0** s'il a fait moins bien : **mieux valait ne rien savoir**.

À la différence du $R^2$ ordinaire, elle peut être négative, et c'est ce qui la
rend utile : elle pénalise l'estimation, en temps réel, d'un coefficient instable.

## 10.4 — Goyal et Welch : presque rien ne survit

Goyal & Welch (2008) appliquent cette statistique aux prédicteurs classiques de la
littérature sur l'indice américain : dividende/prix, rendement des bénéfices, taux
courts, pente de la courbe, écart de crédit, inflation, et d'autres. Leur verdict :
**presque aucun** ne bat la moyenne historique hors échantillon, et beaucoup ont un
$R^2_{\text{hors}}$ négatif. La plupart des résultats publiés tenaient à une
période particulière, souvent les années 1970.

Campbell & Thompson (2008) répondent qu'en imposant des contraintes économiques
(prévision de prime positive, signe du coefficient conforme à la théorie), on
récupère un $R^2_{\text{hors}}$ mensuel de l'ordre de **0,5 %**. C'est positif ; c'est
aussi minuscule. Goyal, Welch & Zafirov (2024) refont l'exercice sur des données
plus récentes et trouvent que la plupart des prédicteurs proposés depuis se
dégradent de la même façon.

Une dernière difficulté touche les prévisions à long horizon, qui paraissent
souvent meilleures : on y régresse des rendements sur **cinq ans glissants**, qui
se chevauchent. Les observations ne sont plus indépendantes, ce qui gonfle les $t$
de Student. Et quand le prédicteur est très persistant, comme le rapport
dividende/prix, son coefficient estimé est lui-même biaisé (Stambaugh 1999).

## 10.5 — Trois prédicteurs de taux sur le CAC 40

Le relevé D de [`mesurer_macro.py`](figures/mesurer_macro.md) applique la méthode au
rendement mensuel du CAC 40, de 1990 à 2025, avec trois variables de taux
américaines connues à la fin de chaque mois. Apprentissage initial : 120 mois.

| Prédicteur | Mois | $R^2$ dans | $t$ | $p$ | $R^2$ hors |
|---|---|---|---|---|---|
| pente 10 ans − 3 mois | 429 | 0,29 % | −1,12 | 0,264 | **−0,43 %** |
| taux à 3 mois | 429 | 0,03 % | +0,33 | 0,740 | **−1,38 %** |
| variation sur 12 mois du 10 ans | 419 | 0,06 % | +0,52 | 0,606 | **−0,27 %** |

Aucun des trois n'est significatif dans l'échantillon. Les trois font **moins
bien que la moyenne historique** hors échantillon. Avec trois tests, la correction
de Holm ne change rien : le plus petit $p$, 0,264, est loin de $0{,}05/3$.

Deux raisons de prendre ce résultat au sérieux :

- **les variables sont des prix de marché**, connus à la clôture et jamais
  révisés : aucun regard en avant, contrairement à ce que ferait le PIB
  ([module 5](05-la-croissance.md)) ;
- **les trois ont été fixées avant le calcul**, et publiées toutes les trois :
  aucune n'a été retenue parce qu'elle marchait.

> 🔑 **Le test honnête d'un prédicteur est hors échantillon, et il se publie
> pour toutes les variables essayées.** Trouver, parmi vingt variables macro,
> celle qui « prédit » le mieux sur le passé, puis la publier seule, c'est le
> piège des tests multiples du [cours alpha](../alpha/04-cinq-pieges.md). C'est
> aussi, mot pour mot, le mécanisme qui a fait échouer les pistes de catégorie B
> des expériences 10 et 13 du dépôt.

## Ce qu'il faut retenir

1. Un **facteur** explique les rendements en même temps que lui ; un **prédicteur**
   les annonce. Le premier est courant, le second rare.
2. Les primes des facteurs macro de Chen-Roll-Ross ne résistent pas à tous les
   choix de méthode.
3. Le $R^2$ hors échantillon compare un prédicteur à la moyenne historique en
   temps réel ; il est **négatif** pour la plupart des prédicteurs classiques.
4. Sur le CAC 40 de 1990 à 2025, trois prédicteurs de taux ont un $R^2_{\text{hors}}$
   de **−0,27 % à −1,38 %**.

---

⬅️ [Module 9 — La corrélation actions-obligations](09-la-correlation-actions-obligations.md) ·
➡️ [Module 11 — Exemple chiffré : huit valeurs du CAC 40](11-exemple-chiffre-huit-valeurs.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
