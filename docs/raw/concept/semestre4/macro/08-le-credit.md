# Module 8 — Le crédit

**Prérequis :** [module 1](01-le-taux-d-actualisation.md).
**Ce qu'on établit ici :** pourquoi action et dette d'une même entreprise réagissent au même risque, pourquoi c'est le lien le plus stable du cours, et pourquoi sa stabilité ne le rend pas utile pour prévoir.

---

## 8.1 — L'action et la dette sur le même actif

Merton (1974) modélise une entreprise dont les actifs valent $V$ et qui doit
rembourser une dette $F$ à une date donnée. À l'échéance :

- si $V > F$, les créanciers reçoivent $F$ et les actionnaires le reste, $V - F$ ;
- si $V < F$, l'entreprise fait défaut : les créanciers reçoivent $V$, les
  actionnaires rien.

L'action est donc une **option d'achat** sur les actifs, de prix d'exercice $F$.
La dette vaut une obligation sans risque **moins** une option de vente sur les
mêmes actifs. Quand le risque sur $V$ augmente, la valeur de l'action baisse et
l'écart de crédit (le supplément de taux exigé par les créanciers) s'élargit. Les
deux sont **deux lectures du même risque**.

## 8.2 — Une mesure indirecte

L'écart de crédit européen n'est pas disponible sur la source. On le remplace par
une **procuration** déclarée : l'écart de rendement hebdomadaire entre deux fonds
obligataires américains,

$$\text{CRÉDIT}_w = r^{\text{HYG}}_w - r^{\text{IEF}}_w$$

`HYG` détient des obligations d'entreprises à haut rendement, `IEF` des
obligations du Trésor de même durée approximative. Leur écart de rendement
**baisse** quand l'écart de crédit s'élargit. Une corrélation **positive** avec le
CAC 40 signifie donc : actions et crédit se dégradent ensemble.

## 8.3 — Le lien le plus stable du cours

Corrélation hebdomadaire du CAC 40 avec cette procuration, année par année
(relevé C) :

| | Minimum | Maximum | 2008-2025 |
|---|---|---|---|
| Corrélation | **+0,350** (2024) | **+0,832** (2010) | **+0,672** |

Elle est **positive les dix-huit années**, jamais sous +0,35, et c'est la plus
forte des quatre variables du relevé. À comparer avec le taux, dont le signe
s'inverse en 2022 ([module 9](09-la-correlation-actions-obligations.md)), le change
qui en change deux fois ([module 6](06-le-change.md)), et le pétrole ([module 7](07-le-petrole.md)).

La raison est celle du § 8.1 : ce n'est pas un facteur **extérieur** aux actions,
c'est le même risque d'entreprise lu sur un autre marché. Collin-Dufresne,
Goldstein & Martin (2001) montrent d'ailleurs que les variations d'écarts de
crédit sont dominées par un facteur commun que les variables macro classiques
n'expliquent pas.

## 8.4 — Stable ne veut pas dire utile

Une corrélation contemporaine forte et stable ne donne **aucune** avance. Si le
crédit et les actions réagissent la même semaine au même choc, observer l'un ne
dit rien de l'autre qu'on ne sache déjà.

La question utile serait : le crédit **annonce-t-il** les actions ? La
littérature trouve que certaines mesures fines de l'écart de crédit annoncent
l'**activité** (Gilchrist & Zakrajšek 2012), comme la pente de la courbe annonce
les récessions ([module 4](04-la-pente-de-la-courbe.md)). Pour les
**rendements** d'actions, le [module 10](10-des-facteurs-a-la-prevision.md)
rappelle que l'écart de crédit figure parmi les prédicteurs que Goyal & Welch
(2008) trouvent inopérants hors échantillon.

> ⚠️ **La procuration est américaine, et ce sont des fonds, pas des écarts.** Les
> fonds ont des frais, des durées qui ne coïncident pas exactement, et leurs
> cours de clôture sont ceux de New York. La mesure donne un ordre de grandeur et
> une stabilité ; elle n'est pas l'écart de crédit européen.

## Ce qu'il faut retenir

1. Chez Merton, l'action est une option sur les actifs : action et dette
   réagissent au même risque.
2. La corrélation CAC 40 / crédit est **positive les dix-huit années**, +0,67 en
   moyenne : c'est le lien le plus stable du cours.
3. Stable et contemporain ne veut pas dire prédictif : observer l'un ne dit rien
   de l'autre qu'on ne sache déjà.

---

⬅️ [Module 7 — Le pétrole](07-le-petrole.md) ·
➡️ [Module 9 — La corrélation actions-obligations](09-la-correlation-actions-obligations.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
