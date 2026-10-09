# Cours — Le cours et la macroéconomie

Les cours précédents expliquent un cours de bourse par lui-même (sa tendance, sa
dispersion, ses bornes), par l'indice ([alpha](../alpha/README.md)) ou par les
comptes de l'entreprise ([fondamentaux](../fondamentaux/README.md)). Aucun ne
regarde **le monde autour** : taux d'intérêt, inflation, croissance, change,
pétrole, crédit. Ce cours le fait, **un facteur par module**, et il pose d'emblée
la distinction qui organise tout le reste :

- **ce qui bouge ensemble** : le cours réagit la même semaine qu'un choc de taux,
  de change ou de pétrole. Ce lien est souvent robuste, et il se mesure ;
- **ce qui annonce** : une variable connue aujourd'hui prédit le rendement de
  demain. Ce lien est presque toujours instable, et il échoue le plus souvent
  hors de l'échantillon qui l'a fait découvrir.

Niveau bac+2. Prérequis : l'[étape 8 du modèle](../../semestre3/modele/08-test-de-tendance.md)
(test de Student), les modules [2](../alpha/02-le-calcul-et-ses-erreurs-types.md)
à [4](../alpha/04-cinq-pieges.md) du cours alpha (régression sur un facteur,
horizon, tests multiples), et le
[module 2 du cours fondamentaux](../fondamentaux/02-les-quatre-dates-d-un-ratio.md)
(les dates d'une donnée publiée). Aucune connaissance macroéconomique préalable.

## Pourquoi ce cours

Parce que la macroéconomie est le domaine où l'on entend le plus d'affirmations
causales sur les cours, et où l'on en vérifie le moins.

| Ce qu'on croit | Ce qu'il en est | Module |
|---|---|---|
| « LVMH est une valeur de croissance, elle souffre quand les taux montent. » | Marché compris, sa sensibilité au taux vaut **−0,0042** par point, $t = -0{,}59$ : **rien de mesurable** sur 2008-2025. Celle de L'Oréal vaut **−0,0385**, $t = -6{,}24$ | [01](01-le-taux-d-actualisation.md) |
| « Quand les taux montent, les actions baissent. » | Sur 2008-2021, la corrélation hebdomadaire du CAC 40 avec la variation du taux à 10 ans est **positive chaque année**, jusqu'à **+0,70**. Elle ne devient négative qu'en **2022 et 2023** | [09](09-la-correlation-actions-obligations.md) |
| « La BCE a baissé ses taux, le marché va monter. » | Une décision attendue est déjà dans les prix. Seule la **surprise** fait bouger le cours, et elle se mesure en minutes, pas en semaines | [02](02-la-politique-monetaire.md) |
| « Les actions protègent de l'inflation. » | À court terme, la relation est **négative** (Fama & Schwert 1977). La protection n'apparaît, partiellement, qu'à des horizons de plusieurs années | [03](03-l-inflation.md) |
| « La courbe s'est inversée, il faut vendre. » | La pente prédit assez bien les **récessions** ; sur 1990-2025, elle explique **0,29 %** du rendement mensuel suivant du CAC 40, et fait **moins bien que la moyenne historique** hors échantillon | [04](04-la-pente-de-la-courbe.md), [10](10-des-facteurs-a-la-prevision.md) |
| « Le PIB est un fait. » | Il est publié six semaines après le trimestre, puis **révisé** pendant des années. Le chiffre qu'on lit aujourd'hui n'est pas celui auquel le marché a réagi | [05](05-la-croissance.md) |
| « Un euro fort pénalise les exportateurs. » | Vrai pour Airbus (**−0,61**, $t = -6{,}16$) et Sanofi (**−0,32**) ; **non mesurable** pour LVMH (**+0,12**, $t = +1{,}69$), pourtant l'exemple que tout le monde cite | [06](06-le-change.md) |
| « Le pétrole monte, les marchés baissent. » | La corrélation du CAC 40 avec le Brent vaut **+0,66** en 2010 et **−0,21** en 2022. Le signe dépend de l'**origine** du choc | [07](07-le-petrole.md) |
| « J'ai trouvé une variable macro qui explique mes valeurs. » | Sur 24 sensibilités testées, **12** passent le seuil de 5 %, mais seulement **6** survivent à Holm | [11](11-exemple-chiffre-huit-valeurs.md) |
| « Soros a gagné en 1992 grâce à un carry trade. » | C'était l'**inverse** : un portage négatif d'environ 0,4 point par an, contre un gain visé de 10 %. Le carry trade était dans le camp d'en face | [12](12-cas-d-etude-livre-sterling-1992.md) |
| « La livre turque baisse chaque année, il suffit de la vendre. » | En 2025 elle perd **17,8 %** face au dollar, mais la vendre coûtait ≈ 39 points de portage : une vente ouverte au meilleur moment perd ≈ **10 %**. Le carry trade, lui, rapporte ≈ **+13 %** | [13](13-cas-d-etude-livre-turque-2025.md) |
| « Pour parier sur la baisse des taux russes, il suffit d'un support très corrélé. » | Sur onze proxys légaux, le meilleur partage **3,1 %** de variance avec le rouble, et **le rouble lui-même ne suit pas le taux directeur** ($r = -0{,}034$). Et un rapprochement russo-américain n'est pas une paix : la défense européenne y **monte** | [14](14-cas-d-etude-russie-2022-2026.md) |

## Le fil directeur

> 🔑 **Une sensibilité macro se mesure ; une prévision macro se prétend.** Un
> coefficient contemporain, estimé sur quinze ans et corrigé des tests multiples,
> dit quelque chose de vérifiable sur la façon dont un titre encaisse un choc.
> Une prévision dit quelque chose sur l'avenir, et l'histoire de la discipline
> est celle de prévisions qui marchaient dans l'échantillon et ont cessé de
> marcher ensuite. Chaque module demande donc : **ce lien est-il du premier
> genre ou du second ?** Et, quand il est du premier : **est-il stable ?**

## Plan

| # | Module | Ce qu'il établit |
|---|---|---|
| 1 | [Le taux d'actualisation](01-le-taux-d-actualisation.md) ⭐ | Gordon, duration d'une action, pourquoi la croissance amplifie la sensibilité ; banques et foncières ; ce que mesure un $b_{\text{TAUX}}$ |
| 2 | [La politique monétaire](02-la-politique-monetaire.md) | Décision attendue contre surprise ; mesurer une surprise ; Bernanke-Kuttner ; pourquoi ce n'est pas mesurable ici |
| 3 | [L'inflation](03-l-inflation.md) | Fama-Schwert ; l'illusion monétaire de Modigliani-Cohn ; le « modèle de la Fed » et ses défauts ; horizon court contre horizon long |
| 4 | [La pente de la courbe des taux](04-la-pente-de-la-courbe.md) | Ce que dit une courbe inversée ; un bon prédicteur de récession, un mauvais prédicteur de rendement |
| 5 | [La croissance : PIB et PMI](05-la-croissance.md) | Le marché anticipe l'activité ; publication, révision, millésimes ; pourquoi toute étude sur la série révisée regarde en avant |
| 6 | [Le change](06-le-change.md) | Les trois canaux (conversion, compétitivité, couverture) ; le « puzzle de l'exposition » ; Airbus contre LVMH |
| 7 | [Le pétrole](07-le-petrole.md) | Choc d'offre contre choc de demande (Kilian-Park) ; pourquoi aucune corrélation stable n'est à attendre ; 2010 contre 2022 |
| 8 | [Le crédit](08-le-credit.md) | Merton : l'action et la dette sur le même actif ; le lien le plus stable du cours ; ce qu'il ne permet pas de conclure |
| 9 | [La corrélation actions-obligations](09-la-correlation-actions-obligations.md) ⭐ | Un signe qui dépend du régime d'inflation ; son renversement de 2022 mesuré sur le CAC 40 |
| 10 | [Des facteurs à la prévision](10-des-facteurs-a-la-prevision.md) ⭐ | Chen-Roll-Ross ; Goyal-Welch ; le $R^2$ hors échantillon ; trois prédicteurs de taux testés sur 35 ans |
| 11 | [Exemple chiffré : huit valeurs du CAC 40](11-exemple-chiffre-huit-valeurs.md) | Les sensibilités au taux, au change et au pétrole, corrigées par Holm, puis recalculées sur trois sous-périodes |
| 12 | [Cas d'étude : la livre sterling, 1992](12-cas-d-etude-livre-sterling-1992.md) | Une position macro sur une parité fixe : trilemme, asymétrie, seuil de probabilité, coût de portage ; pourquoi ce n'était pas un carry trade |
| 13 | [Cas d'étude : la livre turque, 2025](13-cas-d-etude-livre-turque-2025.md) | Un carry trade chiffré sur une année réelle : rendement, cours à terme et parité non couverte, coût du choc du 19 mars ; la position de 1992 retournée |
| 14 | [Cas d'étude : la Russie, 2022-2026](14-cas-d-etude-russie-2022-2026.md) | Une politique monétaire qu'on ne peut pas jouer : baisse des taux contre croissance, secteurs sous contrainte, ce que vaut un proxy ($ho^2$), et trois scénarios au lieu d'un « accord de paix » |

**14 modules · 13 h.**

## Le fil rouge chiffré

Tous les nombres du cours sortent d'un seul script, versionné à côté de lui :
[`figures/mesurer_macro.py`](figures/mesurer_macro.md). Seule exception, le
[module 14](14-cas-d-etude-russie-2022-2026.md) : ses mesures sont celles du
[laboratoire](../../../lab/proxy-taux-russes.md), refaites par
[`mesurer_russie.py`](../../../lab/figures/mesurer_russie.md).

```bash
python docs/raw/concept/semestre4/macro/figures/mesurer_macro.py
```

Il couvre **huit valeurs du CAC 40**, une par canal attendu, en rendements
hebdomadaires sur **2008-2025** (933 semaines), contre quatre variables :

| Variable | Ticker | Ce qu'elle représente |
|---|---|---|
| Marché | `^FCHI` | le CAC 40, indice nu |
| Taux | `^TNX` | taux américain à 10 ans, variation en points |
| Change | `EURUSD=X` | dollars pour un euro |
| Pétrole | `BZ=F` | Brent |
| Crédit | `HYG` − `IEF` | haut rendement moins Trésor, fonds américains |

> ⚠️ **Deux limites de source, à garder en tête dans tout le cours.**
> 1. **Aucun taux de la zone euro** n'est exploitable sur Yahoo : ni Bund, ni
>    OAT, ni €STR. Le taux américain sert de **procuration**, et un lien mesuré
>    sur lui sous-estime probablement le lien au taux européen.
> 2. **Aucune série macro publiée** (inflation, PIB, PMI, taux directeurs,
>    surprises monétaires) n'est disponible, et encore moins ses **millésimes**.
>    Les modules 2, 3 et 5 sont donc des modules de méthode, sans chiffre du
>    dépôt : ils disent ce qu'il faudrait pour mesurer, et pourquoi on ne le fait
>    pas.

## Ce que ce cours alimente

- Le **§ 3 de l'agent [`trading`](../../../../../.claude/agents/trading.md)** : une
  sensibilité macro est un **bêta de plus**, pas une source d'alpha. Le cours dit
  quand elle est mesurable.
- Le [cours finance](../finance/README.md) : une couverture contre un facteur
  suppose une sensibilité **stable**. Le [module 9](09-la-correlation-actions-obligations.md)
  montre ce qui arrive à une couverture actions-obligations quand elle ne l'est
  pas.
- Le [module 4 du cours alpha](../alpha/04-cinq-pieges.md) : chercher « la »
  variable macro qui explique un titre est un problème de tests multiples, et le
  [module 11](11-exemple-chiffre-huit-valeurs.md) le montre sur 24 coefficients.

> ⚠️ **Ce cours ne donne aucun conseil en investissement.** Il explique ce qui
> relie les cours aux variables macroéconomiques, et surtout ce que ces liens ne
> permettent pas de conclure. Aucun des chiffres qu'il contient ne désigne une
> valeur à acheter ou à vendre, ni un moment pour le faire.

---

➡️ Commencer par le [module 1 — Le taux d'actualisation](01-le-taux-d-actualisation.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
