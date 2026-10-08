# Module 3 — Indicateur 4 : le prix des attentes ⭐

**Prérequis :** [module 2](02-les-attentes-de-benefices.md), le [module 4 du cours fondamentaux](../fondamentaux/04-un-ratio-n-existe-que-relatif.md) (Gordon), et le [module 3 du cours macro](../macro/03-l-inflation.md) (le « modèle de la Fed »).
**Ce qu'on établit ici :** comment traduire un multiple en hypothèse, comment séparer ce qu'une hausse doit au bénéfice et ce qu'elle doit au multiple, et pourquoi le PER d'une valeur cyclique se lit à l'envers.

---

## 3.1 — Ce que le multiple suppose

Le [module 4 du cours fondamentaux](../fondamentaux/04-un-ratio-n-existe-que-relatif.md)
a établi la traduction de Gordon : avec un taux d'actualisation $r$ et tout le
bénéfice distribué,

$$g_{\text{implicite}} = r - \frac{1}{\text{PER}}$$

C'est la croissance perpétuelle que le marché doit attendre pour que le prix soit
justifié. Le script la calcule avec $r = 8\,\%$, la convention du cours
fondamentaux, et la déclare **exigeante** au-delà de **3 %**, une croissance
nominale de long terme plausible pour une grande entreprise européenne.

| | PER | $g$ implicite | Lecture |
|---|---|---|---|
| **OR.PA** | 31,71 | **+4,8 %** | exigeante |
| **SU.PA** | 30,74 | **+4,7 %** | exigeante |
| **AIR.PA** | 24,85 | **+4,0 %** | exigeante |
| **SAN.PA** | 22,00 | +3,5 % | exigeante — mais voir ci-dessous |
| **MC.PA** | 17,54 | +2,3 % | |
| **ORA.PA** | 13,38 | +0,5 % | |
| **TTE.PA** | 11,30 | −0,8 % | |
| **BNP.PA** | 7,97 | −4,5 % | |

Sanofi rappelle le [module 2](02-les-attentes-de-benefices.md) : son PER de 22,00
divise un BPA comptable. Sur le BPA des activités que suit le consensus, il vaut
8,30, et la croissance implicite tombe à $8 - 100/8{,}30 = -4{,}0\,\%$. **La même
action « suppose » +3,5 % ou −4,0 % selon le bénéfice qu'on choisit.** C'est la
meilleure démonstration que $g_{\text{implicite}}$ expose une hypothèse sans
jamais la trancher.

## 3.2 — Le multiple contre le taux

Le **rendement bénéficiaire** est l'inverse du PER, $E/P$ : ce que rapporterait
l'action si tout son bénéfice était versé. Le comparer au taux souverain à
10 ans donne une **prime de rendement** :

$$\text{prime} = \frac{100}{\text{PER}} - y^{10}$$

Avec le taux à 10 ans de la courbe AAA de la zone euro au 7 octobre 2026,
$y^{10} = 3{,}54\,\%$ :

| | OR | SU | AIR | SAN | ORA | MC | TTE | BNP |
|---|---|---|---|---|---|---|---|---|
| Prime (pt) | **−0,38** | **−0,29** | +0,49 | +1,01 | +3,94 | +2,16 | +5,31 | +9,00 |

Pour L'Oréal et Schneider, le rendement bénéficiaire est **inférieur** au taux
sans risque : au bénéfice actuel, l'action rapporte moins qu'une obligation
d'État, et ne fait mieux que si son bénéfice croît. C'est une autre façon
d'écrire la croissance implicite du § 3.1.

> ⚠️ **Cette prime n'est pas une prime de risque, et le cours macro a dit
> pourquoi.** Comparer $E/P$ à un taux **nominal**, c'est le « modèle de la Fed »
> critiqué au [module 3 du cours macro](../macro/03-l-inflation.md) : un bénéfice
> croît avec l'inflation, un coupon d'obligation non. Le terme à comparer serait
> le taux **réel**, $-0{,}26\,\%$ à la même date ([module 6](06-taux-et-credit.md)).
> La prime nominale sert à **classer** les valeurs entre elles à une même date,
> pas à dire si le marché est cher.

## 3.3 — Décomposer une hausse

Puisque $P = \text{PER} \times \text{BPA}$, en logarithmes :

$$\ln\frac{P_1}{P_0} = \ln\frac{\text{BPA}_1}{\text{BPA}_0} + \ln\frac{\text{PER}_1}{\text{PER}_0}$$

L'égalité est exacte. Le rendement du cours est la somme d'une part
**bénéfice** — ce que l'entreprise a réellement gagné de plus — et d'une part
**multiple** — ce que le marché a accepté de payer de plus pour chaque euro de
bénéfice. En ajoutant les dividendes, mesurés comme l'écart entre la série
ajustée et la série brute, on obtient le rendement total.

Les logarithmes ont une propriété que les pourcentages n'ont pas : **ils
s'additionnent**. +18,7 points de bénéfice et +31,0 points de multiple font
49,7 points de prix, soit $e^{0{,}497} - 1 = +64{,}4\,\%$ ; un calcul en
pourcentages n'aurait pas donné une somme.

> 🔑 **C'est la décomposition qui rend le biais de Soros mesurable.** Une hausse
> portée par le **bénéfice** est une hausse que la réalité a validée. Une hausse
> portée par le **multiple** est une hausse de l'**opinion** : le marché paie plus
> cher la même chose. Le second cas n'est pas forcément une bulle, mais c'est le
> seul où une bulle peut se loger.

**Dater correctement.** Le script prend $d_0$ = trois ans avant le relevé, et, à
chaque bout, le résultat net du dernier exercice **publié** à la date —
clôture plus 75 jours —, divisé par le nombre d'actions à la date. Au
8 octobre 2023, le dernier exercice publié était 2022 ; au 8 octobre 2026, c'est
2025. Prendre l'exercice 2023 pour $d_0$ serait utiliser un bénéfice que
personne ne connaissait encore.

## 3.4 — Les huit valeurs sur trois ans

En points de log, du 8 octobre 2023 au 8 octobre 2026 :

| | Prix | = bénéfice | + multiple | Dividendes | Total | PER |
|---|---|---|---|---|---|---|
| **SU.PA** | +49,7 | +18,7 | **+31,0** | +4,8 | +54,5 | 25,4 → 34,6 |
| **AIR.PA** | +40,7 | +23,6 | +17,1 | +5,8 | +46,5 | 23,8 → 28,3 |
| **BNP.PA** | +40,1 | +28,8 | +11,3 | +22,3 | +62,4 | 7,2 → 8,0 |
| **ORA.PA** | +26,5 | **−138,3** | **+164,8** | +17,8 | +44,3 | 13,6 → 70,7 |
| **TTE.PA** | +24,9 | **−36,1** | **+61,0** | +15,9 | +40,8 | 7,1 → 13,0 |
| **OR.PA** | −5,3 | +8,7 | −14,0 | +5,3 | −0,1 | 37,4 → 32,5 |
| **SAN.PA** | −35,7 | −2,3 | −33,4 | +13,8 | −21,9 | 15,3 → 11,0 |
| **MC.PA** | −64,0 | −19,4 | **−44,6** | +6,7 | −57,3 | 27,2 → 17,4 |

Trois profils se dégagent.

- **La hausse validée** — BNP Paribas : le bénéfice porte l'essentiel, le
  multiple reste bas, et les dividendes ajoutent 22 points. Rien ici que
  l'opinion ait inventé.
- **La hausse d'opinion** — Schneider : le multiple porte **plus** que le
  bénéfice, et le PER passe de 25 à 35. Airbus est intermédiaire.
- **La baisse d'opinion** — LVMH et Sanofi : le multiple perd plus que le
  bénéfice. Pour LVMH, le bénéfice recule de 19,4 points, mais le marché a
  retiré 44,6 points de multiple en plus : il ne croit plus à la croissance
  qu'il payait en 2023.

Et deux lignes qu'il faut lire à part.

## 3.5 — Le paradoxe du PER cyclique

TotalEnergies : le cours monte de 24,9 points, le multiple de 61,0, et le PER
passe de 7,1 à 13,0. Lu naïvement, c'est la plus forte hausse d'opinion du
tableau après Orange. C'est l'inverse.

En 2022, la guerre en Ukraine a porté le prix du gaz et du pétrole à des niveaux
exceptionnels, et le bénéfice de l'exercice 2022 avec eux. Le marché savait que
ce bénéfice était **exceptionnel**, et ne l'a payé que 7,1 fois. Le bénéfice est
ensuite revenu vers la normale (−36,1 points), le cours a monté modérément, et le
PER a mécaniquement doublé. **Le multiple n'a pas monté parce que le marché
payait plus cher : il a monté parce que son dénominateur est tombé.**

> 🔑 **Pour une valeur cyclique, un PER bas signale souvent un bénéfice au
> sommet, et un PER haut un bénéfice au creux.** Le marché paie un bénéfice
> **normal** sur le cycle, pas le bénéfice de l'année. Le PER courant se lit donc
> à l'envers de l'intuition, et la décomposition attribue au « multiple » ce qui
> est en réalité un retour du bénéfice vers sa moyenne.

Orange pousse le même mécanisme à l'extrême. Son résultat net 2025 s'est
effondré à 538 M€ (2 146 M€ en 2022), ce qui donne −138,3 points de bénéfice et
un PER annuel de 70,7 — alors que le PER sur les douze derniers mois, qui inclut
déjà le redressement de 2026, n'est que de 13,4. Une charge exceptionnelle dans
un seul exercice suffit à faire exploser les deux termes de la décomposition, en
sens contraire, sans que l'opinion ait changé.

**Comment s'en protéger** :

1. **Exiger un bénéfice en hausse** avant de parler d'emballement du multiple.
   C'est la correction qu'a subie le marqueur B2 du script, déclarée dans
   [son miroir](figures/mesurer_indicateurs.md) : sa première version
   s'allumait sur TotalEnergies et Orange.
2. **Regarder le bénéfice sur un cycle**, pas sur un exercice. Avec quatre
   exercices, le dépôt ne le peut pas ; c'est l'idée du CAPE de Shiller, qui
   divise le prix par dix ans de bénéfices moyens.
3. **Vérifier qu'aucun exercice ne porte un élément exceptionnel** avant de lire
   une décomposition — le rapport annuel le dit, Yahoo non.

## 3.6 — Ce que l'indicateur ne dit pas

- **Un multiple élevé n'annonce pas une baisse.** L'Oréal se paie plus de 30 fois
  ses bénéfices depuis des années. Le multiple dit ce qui est supposé, pas quand
  la supposition sera démentie.
- **Une hausse portée par le multiple n'est pas une bulle.** Elle peut traduire
  une baisse des taux (le $r$ de Gordon baisse, le PER monte), ou une
  amélioration réelle des perspectives que les bénéfices n'ont pas encore
  montrée. Soros parle de bulle quand le multiple **finance** la hausse du
  bénéfice — c'est le [module 5](05-levier-et-dilution.md).
- **Trois ans, c'est un point de départ choisi.** Avec $d_0$ un an plus tôt ou
  plus tard, les parts changent. Le [laboratoire](../../../lab/largeur-de-bande-fiable.md)
  a montré la même dépendance pour les bandes : ce qu'on mesure dépend du moment
  où l'on a commencé à regarder.

## Exercices

**E3.1.** Un cours passe de 50 € à 65 €, le BPA de 2,50 € à 2,75 €. Calculer, en
points de log, la part du bénéfice et celle du multiple. Le marqueur B2 du
[module 9](09-assembler-la-sequence.md) est-il allumé ?

**E3.2.** Un minier affiche un PER de 5 au sommet du cycle des métaux. Le bénéfice
retombe de moitié l'année suivante et le cours ne bouge pas. Que devient le PER ?
Que dirait une lecture naïve ?

**E3.3.** Avec $r = 8\,\%$, quel PER correspond à une croissance implicite de 3 % ?
De 5 % ?

**E3.4.** Calculer la prime de rendement de L'Oréal contre le taux **réel**
($-0{,}26\,\%$). Pourquoi la conclusion change-t-elle ?

### Corrigés

**E3.1.** Prix : $100 \ln(65/50) = +26{,}2$. Bénéfice : $100 \ln(2{,}75/2{,}50) = +9{,}5$.
Multiple : $26{,}2 - 9{,}5 = +16{,}7$ (PER de 20 à 23,6). Prix et bénéfice en hausse,
multiple supérieur au bénéfice : **B2 allumé**.

**E3.2.** PER = 10 : il double sans que l'opinion change. La lecture naïve verrait
un emballement ; c'est le bénéfice au sommet qui retombe vers la normale.

**E3.3.** $1/\text{PER} = r - g$ : $1/0{,}05 = 20$ pour 3 %, $1/0{,}03 = 33{,}3$ pour 5 %.
Un PER passe de 20 à 33 quand la croissance supposée gagne deux points : le
multiple est **très** sensible à $g$ quand $g$ approche $r$.

**E3.4.** $100/31{,}71 - (-0{,}26) = 3{,}15 + 0{,}26 = +3{,}41$ points, contre −0,38 en
nominal. Un bénéfice croît avec l'inflation ; à inflation élevée (3,8 %), le
comparer au taux nominal pénalise artificiellement les actions.

## Ce qu'il faut retenir

1. Un multiple se traduit en **croissance implicite** ; la même action peut en
   supposer deux très différentes selon le BPA choisi.
2. $\ln(P_1/P_0) = \ln(\text{BPA}_1/\text{BPA}_0) + \ln(\text{PER}_1/\text{PER}_0)$ :
   une hausse se partage exactement entre **bénéfice** et **multiple**, et seule
   la seconde peut loger un biais.
3. Pour une **valeur cyclique**, un PER bas signale un bénéfice au sommet ; la
   décomposition prend un retour du bénéfice à la normale pour une hausse
   d'opinion. Exiger un bénéfice en hausse avant de parler d'emballement.
4. La prime $E/P - y^{10}$ **classe** les valeurs ; comparée à un taux nominal,
   elle ne mesure pas une prime de risque.

---

⬅️ [Module 2 — Les attentes de bénéfices](02-les-attentes-de-benefices.md) ·
➡️ [Module 4 — Les marges](04-les-marges.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
