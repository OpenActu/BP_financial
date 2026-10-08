# Module 6 — Indicateurs 2 et 3 : le prix et la quantité de l'argent

**Prérequis :** [module 5](05-levier-et-dilution.md), et les modules [1](../macro/01-le-taux-d-actualisation.md), [2](../macro/02-la-politique-monetaire.md), [4](../macro/04-la-pente-de-la-courbe.md) et [8](../macro/08-le-credit.md) du cours macro.
**Ce qu'on établit ici :** comment chiffrer le **prix** de l'argent (taux directeur, courbe, taux réel) et sa **quantité** (croissance du crédit, écart du crédit au PIB), pourquoi Soros regardait les deux ensemble, et ce que leur lecture permet de dire d'un marché d'actions — très peu.

---

## 6.1 — Deux indicateurs, une seule question

Le cours macro a mesuré la **sensibilité** des actions au taux. Ce module pose une
autre question, celle de Soros : l'argent est-il **abondant** ou **rare**, et
cette abondance alimente-t-elle une boucle ?

| | Ce qu'on mesure | Pourquoi |
|---|---|---|
| **Indicateur 2 — le prix** | taux directeur, taux à 3 mois et à 10 ans, pente, taux réel | le $r$ de Gordon : toute valorisation en dépend |
| **Indicateur 3 — la quantité** | croissance du crédit aux entreprises, écart du crédit au PIB, écarts de crédit de marché | le carburant des booms : un boom sans crédit qui l'accompagne s'épuise vite |

Les deux ne vont pas toujours ensemble. Un taux qui monte peut coexister avec un
crédit qui accélère : c'est alors la **demande** de crédit qui l'emporte, et c'est
souvent un signe de fin de cycle.

## 6.2 — Indicateur 2 : le prix de l'argent

Le script lit à la BCE, et non plus par procuration américaine comme le cours
macro, quatre séries :

| Grandeur | Source | Au 7 octobre 2026 |
|---|---|---|
| taux de la facilité de dépôt | BCE, `FM` | **2,50 %**, +0,50 pt sur un an |
| taux à 3 mois, courbe AAA | BCE, `YC` | 2,52 % |
| taux à 10 ans, courbe AAA | BCE, `YC` | **3,54 %**, +0,74 pt sur un an |
| **pente** 10 ans − 3 mois | calcul | **+1,02 pt** |

Et un cinquième, qui demande Eurostat :

$$\text{taux réel ex post} = y^{10} - \pi_{12\,\text{mois}} = 3{,}54 - 3{,}80 = -0{,}26\,\%$$

**Ce que dit chaque grandeur.**

- **Le taux directeur** dit ce que fait la banque centrale. Ce qui compte pour les
  cours n'est pas la décision mais la **surprise** ([module 2 du cours
  macro](../macro/02-la-politique-monetaire.md)) : une hausse attendue est déjà
  dans les prix. Le dépôt ne mesure pas les attentes de taux, il ne mesure donc
  pas la surprise.
- **La pente** est positive : la courbe n'est pas inversée. Le
  [module 4 du cours macro](../macro/04-la-pente-de-la-courbe.md) a montré qu'une
  courbe inversée annonce assez bien les récessions et très mal les rendements
  d'actions.
- **Le taux réel** est négatif : l'inflation (3,8 %) dépasse le taux à 10 ans.
  Dans la formule de Gordon, c'est le taux réel qui actualise un bénéfice qui
  croît avec l'inflation. Un taux réel négatif soutient mécaniquement les
  multiples élevés — c'est ce qui rend la prime de L'Oréal ou de Schneider moins
  choquante qu'en nominal ([module 3](03-le-prix-des-attentes.md)).

> ⚠️ **Le taux réel ex post n'est pas le taux réel que le marché anticipe.** Le
> calcul soustrait l'inflation **passée** sur douze mois, alors que le taux à
> 10 ans porte sur l'inflation **attendue** sur dix ans. Le bon terme serait le
> rendement d'une obligation indexée sur l'inflation, que ni Yahoo ni les séries
> lues ici ne servent. L'ex post est une approximation déclarée : elle exagère le
> taux réel négatif quand l'inflation courante dépasse l'inflation anticipée.

**La sensibilité d'un multiple au taux.** Avec $\text{PER} = 1/(r - g)$, un PER
élevé est un PER **sensible** :

$$\frac{\partial \ln \text{PER}}{\partial r} = -\frac{1}{r - g} = -\text{PER}$$

Une hausse de 0,5 point de $r$ fait perdre environ $0{,}005 \times 30 = 15\,\%$ à
un PER de 30, et $0{,}005 \times 8 = 4\,\%$ à un PER de 8. C'est la **duration**
d'une action du [module 1 du cours macro](../macro/01-le-taux-d-actualisation.md),
et la raison pour laquelle les valeurs à multiple élevé sont celles dont un
biais de taux se paie le plus cher.

## 6.3 — Indicateur 3 : la quantité d'argent

**La croissance du crédit.** La BCE publie le taux de croissance annuel des prêts
aux sociétés non financières de la zone euro :

| | Août 2025 | Août 2026 |
|---|---|---|
| prêts aux entreprises, sur un an | +3,0 % | **+4,2 %** |
| croissance nominale approchée, PIB réel + inflation | — | **5,0 %** |

Le repère est la croissance **nominale** de l'économie. Un crédit qui croît plus
vite qu'elle fait monter le ratio crédit/PIB : l'économie s'endette **plus vite
qu'elle ne produit**. Ici, le crédit accélère, mais reste sous la croissance
nominale : le ratio baisse encore.

**L'écart du crédit au PIB.** La Banque des règlements internationaux (BRI)
publie, pour chaque pays, l'écart du ratio crédit privé/PIB à sa **tendance de
long terme** :

$$\text{écart} = \frac{\text{crédit}}{\text{PIB}} - \text{tendance}\left(\frac{\text{crédit}}{\text{PIB}}\right)$$

Le seuil de 10 points est celui que les régulateurs bancaires utilisent pour
demander aux banques un coussin de fonds propres contracyclique : au-delà, les
crises bancaires passées ont souvent suivi. Pour la France, au premier
trimestre 2026 : **−15,7 points**, très en dessous de la tendance.

> ⚠️ **Une tendance estimée sur le passé hérite de ses excès.** La tendance de la
> BRI est un filtre statistique qui ne regarde que le passé. Les prêts garantis
> par l'État de 2020 ont gonflé le ratio, donc la tendance ; leur remboursement
> fait apparaître un écart très négatif qui dit autant « la tendance est trop
> haute » que « le crédit est rare ». Un écart se lit avec l'histoire du ratio,
> pas seul.

**Le crédit de marché.** Le script reprend la procuration du
[module 8 du cours macro](../macro/08-le-credit.md), l'écart de rendement entre
un fonds d'obligations à haut rendement (`HYG`) et un fonds d'obligations d'État
(`IEF`), sur 13 semaines : **+2,12 points**. Positif, il signifie que les
emprunteurs risqués ont fait mieux que l'État : les écarts de crédit se
resserrent, l'appétit pour le risque est fort.

## 6.4 — La boucle du collatéral

Soros consacre une partie de *L'Alchimie de la finance* au boom des prêts
bancaires internationaux des années 1970, qui s'est terminé par la crise de la
dette latino-américaine de 1982. Le mécanisme est réflexif :

1. Les banques prêtent à des pays dont les ratios d'endettement paraissent sains.
2. Ces prêts financent de la croissance, qui **améliore** les ratios.
3. Les ratios améliorés justifient de nouveaux prêts.
4. Jusqu'à ce que le coût de la dette dépasse la croissance qu'elle finance — et
   la boucle se retourne : moins de prêts, moins de croissance, ratios dégradés,
   encore moins de prêts.

> 🔑 **Le critère de solvabilité dépend lui-même du crédit accordé.** C'est ce qui
> rend la boucle invisible de l'intérieur : chaque prêteur juge sur des ratios
> que l'ensemble des prêteurs fabrique. Le même mécanisme vaut pour l'immobilier
> (le prix du bien sert de garantie au prêt qui fait monter le prix) et pour les
> actions achetées à crédit.

Ce que les indicateurs 2 et 3 permettent de repérer, c'est la **condition** de
cette boucle : un crédit qui croît **plus vite** que la production, pendant
longtemps, avec un écart au PIB qui se creuse vers le haut. Au 8 octobre 2026, en
zone euro et en France, aucune des trois conditions n'est remplie.

## 6.5 — Lire les deux ensemble

| Prix de l'argent | Quantité | Lecture |
|---|---|---|
| bas ou en baisse | crédit qui accélère au-dessus du PIB | phase où les booms se forment |
| en hausse | crédit qui accélère encore | la demande l'emporte : fin de cycle possible |
| en hausse | crédit qui ralentit | resserrement qui mord |
| en baisse | crédit qui ralentit malgré tout | l'argent est offert mais pas demandé : désendettement |

Au 8 octobre 2026 : taux directeur en hausse de 0,5 point, taux réel négatif,
crédit qui accélère (+3,0 % → +4,2 %) **sous** la croissance nominale, écart au
PIB très négatif, écarts de crédit qui se resserrent. C'est un resserrement
monétaire qui reste **accommodant en termes réels**, avec un crédit qui repart
d'un niveau bas. Ce n'est pas la configuration d'un boom du crédit.

> ⚠️ **Ce que cette lecture ne dit pas.** Le [module 10 du cours
> macro](../macro/10-des-facteurs-a-la-prevision.md) l'a mesuré : la pente, le
> taux court et leurs variations n'ont **aucun** pouvoir de prévision hors
> échantillon sur le rendement mensuel du CAC 40. Les indicateurs 2 et 3 disent
> dans quel **régime** on se trouve ; ils ne disent pas ce que fera le marché, ni
> quand. Et ils sont **communs à toutes les valeurs** : ils ne départagent
> aucune action d'une autre, sinon par sa sensibilité ($\partial \ln \text{PER}/\partial r$).

## Exercices

**E6.1.** Un an plus tôt, le taux à 10 ans valait $3{,}54 - 0{,}74 = 2{,}80\,\%$ et
l'inflation 2,2 %. Calculer le taux réel ex post à cette date. Le taux réel
a-t-il monté ou baissé sur un an ?

**E6.2.** Le crédit privé représente 140 % du PIB. Il croît de 4,2 % et le PIB
nominal de 5,0 %. De combien de points le ratio varie-t-il en un an ?

**E6.3.** Avec $g = 4{,}7\,\%$, de combien baisse le PER de Schneider si $r$ passe de
8 % à 8,5 % ? Et celui de BNP Paribas ($g = -4{,}5\,\%$) ? Comparer à
l'approximation $-\text{PER} \times \Delta r$.

### Corrigés

**E6.1.** $2{,}80 - 2{,}20 = +0{,}60\,\%$. Il est passé de +0,60 % à −0,26 % : il a
**baissé** de 0,86 point alors que le taux nominal montait de 0,74 point,
parce que l'inflation a monté davantage (+1,6 point). Le resserrement nominal
est un assouplissement réel.

**E6.2.** Nouveau ratio : $140 \times 1{,}042/1{,}050 = 138{,}9\,\%$, soit **−1,1 point**.

**E6.3.** Schneider : $1/(0{,}080 - 0{,}047) = 30{,}3$ puis $1/(0{,}085 - 0{,}047) = 26{,}3$,
soit **−13,2 %** ; l'approximation donne $-30{,}3 \times 0{,}5\,\% = -15{,}2\,\%$. BNP :
$1/0{,}125 = 8{,}0$ puis $1/0{,}130 = 7{,}69$, soit **−3,8 %** ; l'approximation,
$-4{,}0\,\%$. L'approximation linéaire exagère d'autant plus que le PER est élevé :
la relation est **convexe** en $r$, comme la duration d'une obligation.

## Ce qu'il faut retenir

1. L'indicateur 2 est le **prix** de l'argent, l'indicateur 3 sa **quantité** ; un
   boom réflexif demande le second, et se nourrit d'un premier bas.
2. Le taux réel actualise les bénéfices : négatif au 8 octobre 2026 (−0,26 %
   ex post), il soutient les multiples élevés, qui sont aussi les plus sensibles
   au taux ($\partial \ln \text{PER}/\partial r = -\text{PER}$).
3. Le crédit se compare à la **croissance nominale** ; l'écart crédit/PIB de la
   BRI alerte au-delà de +10 points, mais sa tendance hérite des excès passés.
4. Ces indicateurs situent un **régime**, communs à toutes les valeurs ; ils ne
   prévoient pas le marché.

---

⬅️ [Module 5 — Comment la hausse se finance](05-levier-et-dilution.md) ·
➡️ [Module 7 — Le monde autour](07-change-croissance-inflation.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
