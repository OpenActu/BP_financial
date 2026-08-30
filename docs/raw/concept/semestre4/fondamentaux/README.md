# Cours — Les fondamentaux

Les huit cours précédents ne regardent que le **prix** : sa tendance, sa
dispersion, ses bornes, son excès sur l'indice. Aucun ne demande jamais ce que
l'entreprise gagne. Ce cours-ci ouvre l'autre moitié du dossier — PER, P/B,
VE/EBITDA, rendement du FCF, ROE, marges, dette/EBITDA — et il commence par une
mauvaise nouvelle : **un ratio fondamental est un rapport entre deux nombres qui
ne parlent ni du même moment, ni du même objet, ni avec la même liberté.**

Niveau bac+2. Prérequis : les [étapes 1 à 8 du modèle](../../../modele.md#plan-de-la-preuve)
pour la régression du [module 4](04-un-ratio-n-existe-que-relatif.md), et le
[module 4 du cours alpha](../alpha/04-cinq-pieges.md) pour les tests multiples.
Aucune connaissance comptable préalable.

## Pourquoi ce cours

Parce que les ratios sont les grandeurs les plus faciles à calculer et les plus
faciles à mal lire de toute la finance.

| Ce qu'on croit | Ce qu'il en est | Module |
|---|---|---|
| « Cette valeur a un PER de 10, elle est moins chère que celle à 11. » | Orange (PER **10,27**) est **46 % plus chère** que TotalEnergies (PER **10,90**) une fois la dette comptée : VE/EBITDA **7,35** contre **5,04** | [01](01-de-quoi-un-ratio-est-le-rapport.md) |
| « J'ai les fondamentaux, je peux backtester un écran *value*. » | Un ratio a **quatre dates** et la source n'en donne que deux. La date de publication manque — celle qui décide de ce qu'on savait, et quand | [02](02-les-quatre-dates-d-un-ratio.md) |
| « L'EBITDA est un fait comptable. » | Il n'est **défini par aucune norme**. IFRS 16 l'a fait bondir en 2019 sans qu'aucune entreprise ne gagne un euro de plus | [03](03-ce-que-la-comptabilite-laisse-au-choix.md) |
| « Un P/B faible signale une valeur décotée. » | Sur nos huit valeurs, le ROE explique **67 %** de la variance du P/B. Un P/B bas est d'abord l'énoncé d'un ROE bas | [04](04-un-ratio-n-existe-que-relatif.md) |
| « Une case vide, c'est une donnée manquante à combler. » | Pour BNP Paribas, VE/EBITDA n'est pas manquant : il est **dépourvu de sens**. Une banque n'a ni valeur d'entreprise ni EBITDA | [03](03-ce-que-la-comptabilite-laisse-au-choix.md) |

## Le fil directeur

> 🔑 **Un ratio n'est pas une mesure, c'est une question posée au marché.** Un
> PER de 33 ne dit pas « cher » : il dit que le marché paie 33 ans de bénéfice
> courant, donc qu'il en attend bien davantage. Tout le cours consiste à traduire
> chaque ratio dans l'hypothèse qu'il contient — sur la croissance, sur la dette,
> sur la durée — puis à demander si cette hypothèse est vérifiable avec les
> données dont on dispose. Le plus souvent, elle ne l'est pas, et c'est cela
> qu'il faut publier.

## Plan

| # | Module | Ce qu'il établit |
|---|---|---|
| 1 | [De quoi un ratio est le rapport](01-de-quoi-un-ratio-est-le-rapport.md) | Numérateur de marché, dénominateur comptable ; capitalisation contre valeur d'entreprise ; pourquoi le PER se renverse quand on compte la dette ; bénéfice contre trésorerie |
| 2 | [Les quatre dates d'un ratio](02-les-quatre-dates-d-un-ratio.md) ⭐ | Date de cours, de clôture d'exercice, de publication, de récupération ; ce que la source donne et ce qu'elle tait ; pourquoi aucun backtest fondamental n'est possible ici |
| 3 | [Ce que la comptabilité laisse au choix](03-ce-que-la-comptabilite-laisse-au-choix.md) ⭐ | EBITDA hors norme et effet IFRS 16 ; goodwill et fonds propres ; le ROE gonflé par le levier (DuPont) ; les ratios **indéfinis** pour les banques |
| 4 | [Un ratio n'existe que relatif](04-un-ratio-n-existe-que-relatif.md) ⭐ | Gordon : $\text{PER} = \text{payout}/(r-g)$ ; croissance implicite ; $P/B$ contre ROE, régression et **échec de la forme linéaire** ; l'effet secteur |
| 5 | [Exemple chiffré — huit valeurs du CAC 40](05-exemple-chiffre-huit-valeurs.md) | Les quatre modules appliqués ligne à ligne, y compris les deux cases vides et la comparaison intra-secteur |

## Le fil rouge chiffré

**Huit valeurs du CAC 40, au 30 août 2026**, produites par
[`python/import_fondamentaux.py`](../../../../../python/import_fondamentaux.md) :

```bash
python python/import_fondamentaux.py AIR.PA MC.PA OR.PA SAN.PA TTE.PA BNP.PA SU.PA ORA.PA
```

| | Secteur | PER | P/B | VE/EBITDA | Rdt FCF | ROE | Dette/EBITDA |
|---|---|---|---|---|---|---|---|
| **AIR.PA** | Industrie | 27,04 | 6,21 | 17,99 | 1,95 % | 23,19 % | 1,59 |
| **MC.PA** | Conso. cyclique | 20,90 | 3,32 | 12,59 | 5,11 % | 16,59 % | 1,85 |
| **OR.PA** | Conso. défensive | 32,98 | 6,11 | 21,21 | 3,09 % | 19,41 % | 1,61 |
| **SAN.PA** | Santé | 23,84 | 1,34 | 8,13 | 6,81 % | 5,71 % | 1,74 |
| **TTE.PA** | Énergie | 10,90 | 1,49 | 5,04 | 8,19 % | 14,48 % | 1,59 |
| **BNP.PA** | Banque | 8,87 | 0,94 | — | — | 10,48 % | — |
| **SU.PA** | Industrie | 35,58 | 6,94 | 21,86 | 3,17 % | 18,62 % | 2,44 |
| **ORA.PA** | Télécoms | 10,27 | 1,27 | 7,35 | 15,83 % | 14,16 % | 4,69 |

> ⚠️ **Ces chiffres sont datés du jour de l'appel et ne sont pas reproductibles
> à l'identique.** Ils changent à chaque cotation pour le numérateur, à chaque
> publication de comptes pour le dénominateur. Le tableau ci-dessus est un
> instantané qui sert d'illustration, pas une base de données. Les relations que
> le cours en tire — pas les valeurs — sont ce qu'il faut retenir.

## Ce que ce cours alimente

- Le **§ 3 de l'agent [`trading`](../../../../../.claude/agents/trading.md)** :
  les familles *valeur*, *qualité* et *taille* de son tableau de sélection
  reposent entièrement sur ce cours, et sur l'interdiction du
  [module 2](02-les-quatre-dates-d-un-ratio.md) de s'en servir en backtest.
- Le miroir de
  [`import_fondamentaux.py`](../../../../../python/import_fondamentaux.md) décrit
  *comment* les colonnes sont produites ; ce cours dit *ce qu'elles veulent
  dire* et quand elles ne veulent rien dire.
- Le [cours trading](../trading/README.md) construit une règle sur cinq critères
  de **prix**. Ce cours explique pourquoi aucun critère fondamental n'y figure.

> ⚠️ **Ce cours ne donne aucun conseil en investissement.** Il explique comment
> lire un ratio et ce qu'il ne permet pas de conclure. Aucun des chiffres qu'il
> contient ne désigne une valeur à acheter ou à vendre.

---

➡️ Commencer par le [module 1 — De quoi un ratio est le rapport](01-de-quoi-un-ratio-est-le-rapport.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
