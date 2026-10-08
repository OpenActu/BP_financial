# Module 2 — Indicateur 1 : les attentes de bénéfices ⭐

**Prérequis :** [module 1](01-l-ecart-a-l-opinion.md), et le [module 3 du cours fondamentaux](../fondamentaux/03-ce-que-la-comptabilite-laisse-au-choix.md) (ce que la comptabilité laisse au choix).
**Ce qu'on établit ici :** comment chiffrer ce que le marché attend d'un bénéfice, comment ces attentes bougent, pourquoi deux BPA d'une même société ne se comparent pas toujours, et à quoi ressemble une vue divergente écrite.

---

## 2.1 — Le consensus, ou l'opinion chiffrée

Une vingtaine d'analystes suivent chaque grande valeur du CAC 40. Chacun publie
une estimation du **bénéfice par action** (BPA) des exercices à venir. Leur
moyenne est le **consensus**. C'est l'opinion du marché sur le bénéfice, rendue
mesurable — la matière première de Steinhardt, et le meilleur indice du biais
dominant de Soros.

Yahoo en sert quatre tableaux, que le script lit par `yfinance` :

| Tableau | Ce qu'il contient |
|---|---|
| `eps_trend` | le BPA moyen attendu **aujourd'hui**, et ce qu'il valait il y a 7, 30, 60 et 90 jours |
| `eps_revisions` | le nombre d'analystes ayant **relevé** ou **abaissé** leur estimation sur 7 et 30 jours |
| `earnings_estimate` | moyenne, estimation basse, haute, nombre d'analystes |
| `growth_estimates` | croissance attendue de la valeur et de son indice |

Chacun a deux lignes utiles : `0y`, l'**exercice en cours** (2026 au moment du
relevé), et `+1y`, le **suivant** (2027).

> ⚠️ **Le consensus n'a pas d'historique ici.** On connaît sa valeur du jour et
> celle d'il y a au plus 90 jours. Pour savoir ce qu'il valait il y a un an, il
> aurait fallu l'**archiver** soi-même, comme `import_fondamentaux.py --archiver`
> le fait pour les ratios. C'est une limite de source, et c'est elle qui rend
> tout backtest de cet indicateur impossible dans le dépôt.

## 2.2 — Quatre mesures

| Mesure | Formule | Ce qu'elle dit |
|---|---|---|
| **Révision** sur 90 jours | $100 \times \left(\dfrac{\text{BPA}_{\text{auj.}}}{\text{BPA}_{-90\,j}} - 1\right)$ | de combien l'opinion a bougé |
| **Diffusion** sur 30 jours | $\dfrac{h - b}{h + b}$, entre $-1$ et $+1$ | dans quel sens bouge la **majorité** des analystes |
| **Croissance attendue** | $100 \times \left(\dfrac{\text{BPA}_{N+1}}{\text{BPA}_{N}} - 1\right)$ | ce que le consensus croit de l'année prochaine |
| **Dispersion** | $100 \times \dfrac{\text{haut} - \text{bas}}{\lvert\text{moyenne}\rvert}$ | à quel point les analystes sont **d'accord** |

$h$ et $b$ sont les nombres de hausses et de baisses d'estimation sur 30 jours,
additionnés sur les deux exercices.

La révision et la diffusion ne mesurent pas la même chose. La révision est une
**amplitude**, dominée par les analystes qui ont bougé le plus. La diffusion est
une **proportion** : elle dit si le mouvement est général. Une révision forte
avec une diffusion nulle est l'œuvre de quelques analystes. Une diffusion forte
avec une révision faible est un mouvement général mais timide.

**Seuils de lecture**, déclarés au [module 9](09-assembler-la-sequence.md) : une
révision est « en hausse » au-delà de +2 %, « en baisse » en deçà de −2 % ; une
diffusion au-delà de ±0,5.

## 2.3 — Les huit valeurs, le 8 octobre 2026

| | BPA 2026 | Révision 90 j | BPA 2027 | Révision 90 j | Diffusion (h/b) | Croissance 2027/2026 | Dispersion | Analystes |
|---|---|---|---|---|---|---|---|---|
| **AIR.PA** | 7,27 | +1,1 % | 8,70 | +1,0 % | +0,48 (17/6) | +19,6 % | 14 % | 19 |
| **MC.PA** | 22,26 | +1,4 % | 24,55 | **−4,1 %** ↓ | **−0,58** ↓ (4/15) | +10,3 % | 7 % | 15 |
| **OR.PA** | 13,63 | −0,3 % | 14,93 | +0,6 % | 0,00 (6/6) | +9,5 % | 8 % | 21 |
| **SAN.PA** | 8,60 | +0,9 % | 9,06 | −0,0 % | +0,14 (8/6) | +5,3 % | 9 % | 21 |
| **TTE.PA** | 11,84 | **+7,2 %** ↑ | 10,91 | **+15,2 %** ↑ | **+0,73** ↑ (19/3) | **−7,9 %** | **40 %** | 21 |
| **BNP.PA** | 11,65 | +1,7 % | 13,29 | **+3,2 %** ↑ | +0,20 (6/4) | +14,1 % | 11 % | 12 |
| **SU.PA** | 10,39 | **+4,3 %** ↑ | 12,35 | **+6,8 %** ↑ | −0,14 (3/4) | +18,9 % | 17 % | 19 |
| **ORA.PA** | 1,37 | **+36,3 %** ↑ | 1,15 | −0,2 % | +0,20 (3/2) | −16,0 % | **88 %** | 10 |

Quatre lectures, qui sont quatre leçons.

**TotalEnergies : des révisions qui suivent une matière première.** Les plus
fortes révisions et la diffusion la plus nette du tableau : 19 hausses pour 3
baisses. Mais le consensus attend un bénéfice 2027 **inférieur** à celui de
2026, et ses estimations s'étalent sur 40 % de la moyenne. Pour une pétrolière,
le BPA est d'abord une fonction du prix du baril ; les analystes révisent leurs
hypothèses de Brent, pas leur jugement sur l'entreprise. L'« opinion » qu'on
mesure ici porte sur le pétrole.

**LVMH : un consensus qui se retourne sur l'année prochaine.** Le BPA 2026 est
stable, mais celui de 2027 a perdu 4,1 % en 90 jours, et 15 analystes sur 19 ont
abaissé leur estimation en un mois. C'est la configuration où le biais dominant
se corrige — le [module 3](03-le-prix-des-attentes.md) montrera que le cours a
déjà perdu près de 45 points de multiple en trois ans.

**Schneider : une révision ancienne, une diffusion récente.** Le BPA attendu a
monté de 4,3 % et 6,8 % sur 90 jours, mais le dernier mois est partagé (3 hausses,
4 baisses). La révision porte surtout sur les deux premiers mois de la fenêtre.
Les deux mesures ne se contredisent pas : elles ne regardent pas la même période.

**Orange : l'effet de base.** +36,3 % de révision sur 2026, c'est le chiffre le
plus spectaculaire du tableau, et le moins informatif. Le BPA de référence est
petit (1,37 €), le résultat net 2025 s'est effondré à 538 M€ contre 2 350 M€ en
2024, et les estimations s'étalent sur 88 % de la moyenne avec seulement dix
analystes. Quand le dénominateur est proche de zéro, une variation relative
**explose** sans rien signifier. Le même piège reviendra au [module 3](03-le-prix-des-attentes.md).

> 🔑 **Une révision ne se lit qu'avec sa dispersion et sa base.** Une révision de
> +7 % avec une dispersion de 40 % dit « l'opinion bouge et n'est pas d'accord
> avec elle-même ». Une révision de +36 % sur une base effondrée ne dit presque
> rien.

## 2.4 — Deux BPA pour une même société

Le [README](README.md) le signalait : Sanofi affiche un PER de 21,96 et un PER
prévisionnel de 7,89. Prise au mot, la différence annoncerait un bénéfice
multiplié par 2,8 en un an. Le consensus, lui, n'attend que +5,3 %.

La contradiction se résout en regardant **quel** bénéfice chaque PER divise :

| Grandeur | Valeur | Définition |
|---|---|---|
| BPA des douze derniers mois (`trailingEps`) | **3,25 €** | comptable, normes IFRS |
| BPA 2026 du consensus (`epsCurrentYear`) | **8,60 €** | « BPA des activités », hors amortissement des actifs incorporels acquis et éléments exceptionnels |
| Cours | 71,38 € | |

Sanofi publie elle-même un BPA « des activités », et c'est lui que suivent les
analystes. Il ignore notamment l'amortissement des brevets achetés avec les
sociétés acquises — une charge comptable très lourde dans la pharmacie. Le PER
comptable est donc $71{,}38/3{,}25 = 21{,}96$ ; le PER sur consensus est
$71{,}38/8{,}60 = 8{,}30$. Les deux sont exacts. Ils ne mesurent pas le même
bénéfice.

**Le contrôle à faire systématiquement** : rapporter le BPA attendu pour
l'exercice en cours au BPA des douze derniers mois.

| | AIR | MC | BNP | OR | SU | ORA | TTE | SAN |
|---|---|---|---|---|---|---|---|---|
| $\text{BPA}_{2026}/\text{BPA}_{12\,\text{mois}}$ | 0,97 | 1,01 | 1,04 | 1,16 | 1,25 | 1,28 | **1,73** | **2,65** |

Pour six valeurs, le rapport reste dans ce qu'une année de croissance explique.
Pour TotalEnergies et Sanofi, il ne l'est pas. Le script imprime ce rapport sous
chaque fiche, avec ⚠ quand il sort de l'intervalle $[1/1{,}5 ; 1{,}5]$. TotalEnergies publie aussi un
résultat « ajusté » (hors effets de stock et éléments exceptionnels) que suit le
consensus.

> ⚠️ **Ne jamais diviser un consensus par un bénéfice comptable, ni l'inverse.**
> Une croissance calculée entre un BPA IFRS et un BPA ajusté est un artefact de
> définition. La règle pratique : tout calcul d'attente se fait **à l'intérieur
> du consensus** — révision, croissance N+1/N, dispersion — et tout calcul
> comptable **à l'intérieur des comptes**. C'est la leçon du
> [module 3 des fondamentaux](../fondamentaux/03-ce-que-la-comptabilite-laisse-au-choix.md)
> appliquée aux attentes.

Le PER prévisionnel de Yahoo (`forwardPE`) ajoute une difficulté : son BPA
(`forwardEps`, 9,68 € pour TotalEnergies) ne correspond ni au consensus 2026
(11,84 €) ni à celui de 2027 (10,91 €). Sa définition n'est pas documentée. Le
cours ne s'en sert donc que pour être comparé, jamais pour un calcul.

## 2.5 — La surprise

La **surprise** est l'écart entre le bénéfice publié et ce que le consensus
attendait la veille :

$$\text{surprise} = \frac{\text{BPA publié} - \text{consensus}}{\lvert\text{consensus}\rvert}$$

C'est le moment où la réalité rencontre l'opinion. Depuis Ball et Brown (1968),
la littérature documente une **dérive après l'annonce** : les cours continuent
de bouger plusieurs semaines dans le sens de la surprise, comme si le marché
mettait du temps à réviser son biais. C'est l'une des anomalies les mieux
documentées, et l'une de celles dont l'ampleur a le plus diminué depuis sa
publication.

Le dépôt ne la mesure pas : les dates et BPA publiés de Yahoo
(`get_earnings_dates`) exigent la bibliothèque `lxml`, qui n'est pas une
dépendance du dépôt, et le consensus de la veille n'est pas archivé. La surprise
reste donc une **définition** dans ce cours, pas une mesure.

## 2.6 — Écrire une vue divergente

Pour Steinhardt, l'indicateur 1 n'est pas le consensus : c'est **l'écart entre sa
propre estimation et le consensus**. Le dépôt fournit le second terme ; le
premier demande un modèle de la société. Ce qui peut en revanche s'apprendre ici,
c'est la **forme** qu'une vue divergente doit prendre pour être utilisable :

| Rubrique | Exemple, sur TotalEnergies |
|---|---|
| **Estimation** | BPA 2027 = 9,80 € |
| **Consensus** | 10,91 € |
| **Écart** | −10,2 % |
| **Mécanisme** | un Brent moyen de 60 $ en 2027 au lieu des ≈ 70 $ que supposent les analystes |
| **Ce que le prix suppose** | à 77,34 €, le marché paie 7,09 fois le BPA 2027 du consensus |
| **Conséquence si la vue est juste et le multiple tient** | $9{,}80 \times 7{,}09 = 69{,}5$ €, soit −10,2 % |
| **Réfutation** | Brent moyen supérieur à 68 $ sur le premier semestre 2027 |
| **Date de jugement** | publication des résultats annuels 2027 |

Les chiffres de l'estimation et du mécanisme sont **inventés pour l'exemple** :
c'est la forme qui compte. Trois propriétés la rendent utilisable :

1. **Elle est chiffrée**, donc on saura si elle était juste.
2. **Elle nomme son mécanisme**, donc on saura *pourquoi* elle était juste ou
   fausse — une vue juste pour une mauvaise raison n'enseigne rien.
3. **Elle se donne une date et une condition de réfutation**, avant de connaître
   le résultat.

C'est exactement le **registre de thèses réfutables** de
l'[expérience 2](../../../../done/experimentation/experience_2/README.md). Et la
ligne « si le multiple tient » rappelle qu'une vue juste sur le bénéfice ne
suffit pas : le [module 3](03-le-prix-des-attentes.md) montre que le multiple a
souvent plus bougé que le bénéfice.

## Exercices

**E2.1.** Sur 30 jours, 9 analystes relèvent leur estimation 2026 et 2 l'abaissent ;
sur 2027, 5 la relèvent et 6 l'abaissent. Calculer la diffusion. Est-elle « en
hausse » au sens du seuil déclaré ?

**E2.2.** Un consensus passe de 0,20 € à 0,30 € en 90 jours. Calculer la révision.
Que faudrait-il vérifier avant d'en tirer quoi que ce soit ?

**E2.3.** Le BPA des douze derniers mois d'une société est de 4,10 € et son
consensus pour l'exercice en cours de 4,40 €. Un site affiche un PER prévisionnel
de 9 pour un cours de 60 €. Que soupçonner ?

**E2.4.** Rédiger, sur le modèle du § 2.6, une vue divergente sur une valeur de son
choix. On pourra inventer l'estimation, mais pas le consensus : le lire avec le
script.

### Corrigés

**E2.1.** $h = 14$, $b = 8$ : diffusion $= (14-8)/22 = +0{,}27$. Positive, mais
sous le seuil de +0,5 : flèche →.

**E2.2.** $100 \times (0{,}30/0{,}20 - 1) = +50\,\%$. Vérifier la **dispersion** et
le nombre d'analystes, et chercher la cause de la faiblesse de la base
(élément exceptionnel, perte l'année précédente) : c'est le cas d'Orange.

**E2.3.** $60/9 = 6{,}67$ € de BPA sous-jacent, soit 1,52 fois le consensus de
l'année en cours et 1,63 fois le BPA récent. Aucune croissance d'un an ne
l'explique : le PER prévisionnel ne divise pas le même bénéfice. Il faut le
recalculer sur le consensus : $60/4{,}40 = 13{,}6$.

**E2.4.** Pas de corrigé : le contrôle est que les sept rubriques soient remplies,
et que la condition de réfutation soit **observable** à une date donnée.

## Ce qu'il faut retenir

1. Le consensus est l'opinion du marché rendue mesurable ; le dépôt n'en connaît
   que **90 jours** d'histoire.
2. **Révision** (amplitude), **diffusion** (proportion), **croissance attendue** et
   **dispersion** se lisent ensemble ; une révision sur une base proche de zéro
   ne dit presque rien.
3. Un BPA comptable et un BPA « des activités » ne se divisent pas l'un par
   l'autre : rapporter le consensus au BPA récent attrape le mélange.
4. Une vue divergente utilisable est **chiffrée**, **motivée** et **réfutable à une
   date** — le format du registre de thèses de l'expérience 2.

---

⬅️ [Module 1 — L'écart à l'opinion](01-l-ecart-a-l-opinion.md) ·
➡️ [Module 3 — Le prix des attentes](03-le-prix-des-attentes.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
