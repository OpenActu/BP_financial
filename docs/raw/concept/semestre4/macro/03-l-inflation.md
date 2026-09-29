# Module 3 — L'inflation

**Prérequis :** [module 1](01-le-taux-d-actualisation.md).
**Ce qu'on établit ici :** pourquoi l'idée que les actions protègent de l'inflation est fausse à court terme, d'où vient l'erreur la plus répandue sur ce sujet, et ce qu'il en reste à long terme.

---

## 3.1 — L'argument de la protection

Une action est un droit sur des actifs **réels** : usines, marques, stocks. Si
tous les prix montent de 5 %, le chiffre d'affaires et les bénéfices nominaux
devraient suivre, et le cours avec eux. L'action serait donc une protection
naturelle contre l'inflation, contrairement à une obligation, dont les coupons
sont fixés en euros.

L'argument est juste en théorie **si** l'inflation ne change rien d'autre. Elle
change presque tout le reste.

## 3.2 — Ce qu'on mesure : une relation négative

Fama & Schwert (1977) régressent les rendements des actions américaines sur
l'inflation, attendue et inattendue, en données mensuelles et trimestrielles. Les
deux coefficients sont **négatifs** : quand l'inflation monte, les actions
baissent, précisément quand elles devraient protéger.

Trois explications, non exclusives :

| Explication | Mécanisme |
|---|---|
| **Le taux d'actualisation** | l'inflation fait monter les taux nominaux (Fisher), donc $r$, donc le prix baisse ([module 1](01-le-taux-d-actualisation.md)) |
| **L'activité** (Fama 1981) | une inflation élevée annonce une croissance réelle plus faible ; c'est la croissance qui fait baisser les actions, l'inflation n'en est que le signal |
| **L'illusion monétaire** (Modigliani & Cohn 1979) | les investisseurs actualisent des flux **réels** à un taux **nominal**, ce qui sous-évalue les actions quand l'inflation est haute |

## 3.3 — L'illusion monétaire et le « modèle de la Fed »

La troisième explication mérite qu'on s'y arrête, parce qu'elle est à l'origine
d'une règle encore très citée : le **« modèle de la Fed »**. Il compare le
rendement des bénéfices, $E/P$ (l'inverse du PER), au taux nominal à 10 ans $y$ :

$$\text{actions « bon marché » si } \frac{E}{P} > y$$

Le défaut est dans les unités. $E/P$ est un rendement **réel** : les bénéfices
croissent avec l'inflation. $y$ est un rendement **nominal**. Les comparer, c'est
exactement l'erreur que décrivent Modigliani et Cohn. Quand l'inflation monte, $y$
monte, et la règle déclare les actions chères, alors que leurs bénéfices futurs
montent aussi.

Asness (2003) montre que la relation qu'on croit voir entre $E/P$ et $y$ dans
l'histoire américaine est bien réelle, mais qu'elle **décrit** l'illusion au lieu de
la corriger : elle dit ce que le marché fait, pas ce qu'il devrait faire. Et son
pouvoir de prévision des rendements futurs est nul.

> 🔑 **Comparer un rendement réel à un rendement nominal est une faute d'unité, pas
> une opinion de marché.** C'est la même faute, dans un autre domaine, que
> comparer un cours ajusté des dividendes à un indice nu.

## 3.4 — À long terme, une protection partielle

Boudoukh & Richardson (1993) reprennent la question sur deux siècles de données
américaines et britanniques, à des horizons de **cinq ans**. La relation devient
positive : sur longue période, les actions compensent en partie l'inflation.

Deux précautions, que le [cours alpha](../alpha/03-l-horizon-necessaire.md)
permet de nommer :

- à cinq ans d'horizon, deux siècles ne font que **40 observations
  indépendantes** ;
- les régressions sur des périodes qui se chevauchent ont des erreurs types trop
  optimistes, et le biais de Stambaugh (1999) s'y ajoute dès que le prédicteur
  est persistant (voir le [module 10](10-des-facteurs-a-la-prevision.md)).

## 3.5 — Pourquoi ce n'est pas mesurable ici

L'inflation est une **statistique publiée** : l'indice des prix de mars paraît à
la mi-avril, puis il peut être révisé. Il faudrait l'indice **tel que publié** à
chaque date, et une mesure de l'inflation **attendue** pour en isoler la surprise.
Le dépôt n'a ni l'un ni l'autre, et le [module 5](05-la-croissance.md) explique
pourquoi une étude sur la série révisée regarderait en avant.

## Ce qu'il faut retenir

1. À court terme, actions et inflation sont **négativement** liées (Fama &
   Schwert 1977).
2. Le « modèle de la Fed » compare un rendement réel à un rendement nominal :
   c'est une faute d'unité (Modigliani & Cohn 1979, Asness 2003).
3. La protection n'apparaît, partiellement, qu'à plusieurs années d'horizon, là
   où les observations indépendantes deviennent rares.
4. Aucune mesure ici : ni la série publiée, ni l'inflation attendue.

---

⬅️ [Module 2 — La politique monétaire](02-la-politique-monetaire.md) ·
➡️ [Module 4 — La pente de la courbe des taux](04-la-pente-de-la-courbe.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
