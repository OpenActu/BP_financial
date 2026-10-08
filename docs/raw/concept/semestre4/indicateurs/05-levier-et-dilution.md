# Module 5 — Indicateurs 5 et 7 : comment la hausse se finance ⭐

**Prérequis :** [module 3](03-le-prix-des-attentes.md), le [module 3 du cours fondamentaux](../fondamentaux/03-ce-que-la-comptabilite-laisse-au-choix.md) (EBITDA), et le [module 8 du cours macro](../macro/08-le-credit.md) (Merton).
**Ce qu'on établit ici :** les deux canaux par lesquels un cours peut **fabriquer** ses propres fondamentaux — la dette adossée à la valeur des actifs, et les actions émises à un prix élevé — et comment les mesurer.

---

## 5.1 — Le canal, ou ce qui distingue une bulle d'un multiple élevé

Le [module 3](03-le-prix-des-attentes.md) s'est arrêté sur une réserve : une
hausse portée par le multiple n'est pas une bulle. Pour Soros, il y a boucle
réflexive quand la hausse du cours **change les fondamentaux** qui sont censés la
justifier. Il faut pour cela un **canal de transmission**, un mécanisme concret
par lequel le prix agit sur la société. Il en existe deux principaux, et ce sont
les indicateurs de ce module :

| Canal | Mécanisme | Indicateur |
|---|---|---|
| **la dette** | la valeur des actifs monte, elle sert de garantie, on emprunte davantage, on achète, la valeur monte | 5 — levier |
| **les actions** | le cours monte, la société paie ses acquisitions en actions, son BPA monte, le cours monte | 7 — dilution |

> 🔑 **Sans canal, pas de réflexivité.** Un multiple élevé sans dette qui monte
> ni actions émises est une **valorisation exigeante** : le marché parie sur
> l'avenir, et il peut se tromper, mais son erreur ne s'auto-entretient pas.
> C'est pourquoi l'agent [`sorosien`](../../../../../.claude/agents/sorosien.md)
> répond par défaut « aucune séquence réflexive identifiable » : la charge de la
> preuve porte sur le canal.

## 5.2 — Indicateur 7 : le conglomérat, chiffré

Le mécanisme que Soros décrit pour les conglomérats américains de la fin des
années 1960 se démontre en une page.

**Avant.** La société A gagne 10 M€, a 10 millions d'actions (BPA 1 €), et le
marché la paie 40 fois ses bénéfices parce qu'il croit à sa croissance : cours
40 €, capitalisation 400 M€. La société B gagne aussi 10 M€, mais n'est payée que
10 fois : elle vaut 100 M€.

**L'opération.** A achète B en émettant $100/40 = 2{,}5$ millions d'actions
nouvelles.

**Après.** A gagne 20 M€ avec 12,5 millions d'actions : **BPA 1,60 €, +60 %**.
Personne n'a vendu un produit de plus.

| | Bénéfice | Actions | BPA | Si le marché garde le PER de 40 | Si le marché paie la moyenne |
|---|---|---|---|---|---|
| A seule | 10 M€ | 10 M | 1,00 € | 40 € | — |
| A + B | 20 M€ | 12,5 M | **1,60 €** | **64 €** | $500/20 = 25$ fois, soit **40 €** |

Si le marché voit une croissance de 60 % et garde son multiple, le cours passe à
64 €, et A peut recommencer avec une monnaie encore plus forte. **Le multiple
élevé a fabriqué la croissance qui le justifie.** S'il paie la moyenne pondérée
des deux sociétés — ce que l'ensemble vaut réellement —, le cours reste à 40 € et
la croissance du BPA n'était qu'un artefact comptable.

La boucle tient tant que le marché confond les deux. Elle se rompt quand les
acquisitions deviennent trop grosses pour entretenir le rythme, ou quand le
multiple baisse : la monnaie d'échange se déprécie, la croissance s'arrête, et le
multiple baisse davantage. C'est la séquence complète du boom-bust, avec son
canal identifié.

**Ce qu'il faut mesurer.** La variation du nombre d'actions :

$$\text{dilution} = 100 \times \left(\frac{\text{actions}_t}{\text{actions}_{t - 1\,\text{an}}} - 1\right)$$

Le marqueur **B4** du [module 9](09-assembler-la-sequence.md) s'allume au-delà de
**+2 %** sur un an. En deçà de −2 %, la société **rachète**.

## 5.3 — Le rachat d'actions, ou la même mécanique à l'envers

Une société qui rachète ses actions réduit leur nombre : son BPA monte sans que
son bénéfice change. Le rachat est **relutif** — il augmente le BPA — si ce qu'il
rapporte dépasse ce qu'il coûte :

$$\text{rachat relutif} \iff \frac{1}{\text{PER}} > \text{rendement après impôt de la trésorerie employée}$$

À un PER de 30, le rendement bénéficiaire est de 3,3 % ; si la trésorerie
rapportait 2,5 % avant impôt, le rachat est à peine relutif. À un PER de 8, le
rachat rapporte 12,5 %, et il l'est nettement. **Un rachat est d'autant plus
favorable aux actionnaires qui restent que l'action est bon marché** — c'est le
miroir exact du conglomérat, qui émet d'autant plus volontiers que l'action est
chère.

## 5.4 — Mesurer le nombre d'actions : une série bruitée

Yahoo sert une série du nombre d'actions (`get_shares_full`) qui mêle des
décomptes avec et sans les actions autodétenues. Pour TotalEnergies, en
octobre 2025, elle oscille entre 2 160 et 2 285 millions **dans le même mois** —
un écart de 5,7 %, près de trois fois le seuil de lecture.

Le script prend donc la **médiane des 30 derniers jours** plutôt que la dernière
valeur. Ce choix n'est pas un détail :

| | Dilution sur un an, valeur ponctuelle | Avec la médiane |
|---|---|---|
| **BNP.PA** | −5,5 % (« rachète ») | **−2,0 %** |
| **MC.PA**, sur trois ans | −1,3 % | **−6,3 %** |

> ⚠️ **Un indicateur dont la lecture change avec l'estimateur n'est pas robuste.**
> Les 5,5 % de rachat de BNP qu'affichait la première version reposaient sur un
> seul décompte. La parade est double : une médiane pour réduire le bruit, et la
> vérification des **rachats annoncés** dans les communiqués de la société avant
> de conclure. Le chiffre du fournisseur oriente ; le communiqué établit.

## 5.5 — Indicateur 5 : le levier

Trois mesures, sur le dernier exercice publié :

| Mesure | Formule | Seuil déclaré |
|---|---|---|
| **dette/EBITDA** | dette totale / EBITDA | « dette lourde » au-delà de **3** |
| **couverture des intérêts** | EBIT / frais financiers | « couverture tendue » en deçà de **3** |
| **dynamique** | croissance de la dette − croissance de l'EBITDA, sur un exercice | « levier qui monte » au-delà de **+10 points** |

Les deux premières décrivent un **état**, la troisième un **mouvement**. Pour la
lecture réflexive, c'est le mouvement qui compte : une dette qui croît plus vite
que ce qui la rembourse finance quelque chose — une acquisition, un rachat, un
investissement —, et il faut savoir quoi.

Le lien avec le [module 8 du cours macro](../macro/08-le-credit.md) est direct :
chez Merton, l'action est une option sur les actifs, de prix d'exercice la dette.
Plus la dette est lourde, plus l'action **amplifie** les variations de la valeur
des actifs, dans les deux sens.

## 5.6 — Les huit valeurs

| | Dette/EBITDA | Couverture | Dynamique | Actions sur un an | sur trois ans |
|---|---|---|---|---|---|
| **AIR.PA** | 1,08 | 9,2 | −13,9 pt | +0,5 % | −2,9 % |
| **MC.PA** | 1,42 | 15,5 | −6,3 pt | −0,8 % | −6,3 % |
| **OR.PA** | 1,11 | 23,7 | **+40,1 pt** | −0,4 % | −1,5 % |
| **SAN.PA** | 1,63 | 10,9 | −0,0 pt | −1,8 % | −4,5 % |
| **TTE.PA** | 1,55 | 9,8 | **+25,3 pt** | +1,4 % | −8,2 % |
| **BNP.PA** | — | — | — | −2,0 % | −6,9 % |
| **SU.PA** | 2,14 | 12,4 | **+16,9 pt** | +0,0 % | −0,7 % |
| **ORA.PA** | — ⚠ | **2,6** | — ⚠ | −0,8 % | −0,1 % |

**Aucune des huit valeurs n'émet d'actions.** Le canal du conglomérat est
fermé partout ; la plupart rachètent au contraire, modestement.

**Trois valeurs voient leur levier monter**, et aucune n'est lourdement endettée.
Celle de L'Oréal passe de 8,5 à 11,9 Md€ (+40 %) quand son EBITDA reste à
10,7 Md€ : la dynamique est forte, le niveau reste faible (1,11). La question à
poser n'est pas « est-ce dangereux ? » mais « **qu'a financé cette dette ?** » —
et la réponse est dans le rapport annuel, pas dans un ratio.

**Orange montre ce qu'un contrôle de cohérence attrape.** Dans les comptes
annuels 2025 servis par Yahoo, la ligne « dette totale » ne contient que les
**loyers** (7,5 Md€) : la dette financière y manque. Le même fournisseur annonce
par ailleurs 56,8 Md€, soit une dette/EBITDA de **4,69**, au-dessus du seuil. La
première version du script affichait **0,62**, sans un mot. Le script confronte
désormais les deux sources et laisse la cellule **vide** quand elles diffèrent
de plus d'un facteur deux, comme le décrit son
[miroir](figures/mesurer_indicateurs.md). Sa couverture des intérêts, 2,6, est
elle mesurable, et tendue : l'EBIT 2025 a été amputé d'éléments exceptionnels.

**BNP Paribas n'a pas de levier au sens de ce module.** La dette d'une banque est
sa matière première — les dépôts, les émissions obligataires —, et elle n'a pas
d'EBITDA. Son levier se mesure par des ratios réglementaires de fonds propres,
que Yahoo ne sert pas.

## Exercices

**E5.1.** La société C est payée 25 fois ses bénéfices de 20 M€ (20 millions
d'actions). Elle achète D, qui gagne 5 M€ et vaut 8 fois ses bénéfices, en
actions. Calculer le BPA avant et après, et le cours si le marché garde le PER
de C. Quel PER paie-t-on réellement pour l'ensemble ?

**E5.2.** Une société au PER de 12 consacre 500 M€ de trésorerie, qui rapportait
3 % avant un impôt de 25 %, à racheter ses actions. Le rachat est-il relutif ? Et
au PER de 45 ?

**E5.3.** Une société a une dette de 4 Md€ et un EBITDA de 2 Md€. L'année suivante,
la dette passe à 5 Md€ et l'EBITDA à 2,1 Md€. Calculer les deux ratios et la
dynamique. Quel marqueur s'allume ?

### Corrigés

**E5.1.** Avant : BPA 1 €, cours 25 €, capitalisation 500 M€. D vaut 40 M€, payés
avec 1,6 million d'actions. Après : 25 M€ pour 21,6 millions d'actions, BPA
**1,157 €** (+15,7 %). À PER constant de 25 : cours **28,94 €**. L'ensemble vaut
en réalité $540/25 = 21{,}6$ fois ses bénéfices, soit un cours de 25 € : la
hausse à 28,94 € est entièrement due à la confusion entre croissance du BPA et
croissance de l'entreprise.

**E5.2.** Rendement après impôt de la trésorerie : $3 \times 0{,}75 = 2{,}25\,\%$.
À un PER de 12, $1/12 = 8{,}3\,\%$ : nettement relutif. À un PER de 45,
$1/45 = 2{,}2\,\%$ : légèrement **dilutif** — le rachat fait baisser le BPA.

**E5.3.** Dette/EBITDA : 2,00 puis 2,38. Dynamique : $+25\,\% - 5\,\% = +20$ points,
au-delà du seuil de 10 : **B3** s'allume, sans que la dette soit « lourde ».

## Ce qu'il faut retenir

1. Il n'y a de boucle réflexive qu'avec un **canal** : la dette adossée à la
   valeur des actifs, ou les actions émises à un prix élevé.
2. Une société payée cher qui achète en actions une société payée moins cher fait
   croître son BPA **sans croître** : le conglomérat de Soros, chiffré.
3. Un rachat est relutif si $1/\text{PER}$ dépasse le rendement après impôt de la
   trésorerie : il profite d'une action bon marché, comme l'émission profite
   d'une action chère.
4. Les séries du fournisseur se **contrôlent** : nombre d'actions bruité (médiane
   sur 30 jours), dette annuelle incomplète (confrontation des sources). Au
   8 octobre 2026, aucune des huit valeurs n'émet d'actions.

---

⬅️ [Module 4 — Les marges](04-les-marges.md) ·
➡️ [Module 6 — Le prix et la quantité de l'argent](06-taux-et-credit.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
