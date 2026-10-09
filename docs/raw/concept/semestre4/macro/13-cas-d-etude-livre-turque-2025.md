# Module 13 — Cas d'étude : la livre turque, 2025

**Prérequis :** [module 12](12-cas-d-etude-livre-sterling-1992.md) (la livre sterling, 1992), [module 2](02-la-politique-monetaire.md) (surprise monétaire).
**Ce qu'on établit ici :** ce qu'est un carry trade, chiffré sur une année réelle ; pourquoi le change à terme n'est pas une prévision ; ce que coûte la queue de distribution qu'un carry trade porte ; et pourquoi la position de 1992 aurait perdu en 2025.

> ⚠️ **Statut des nombres de ce module.** Les **cours de change** sont mesurés sur
> Yahoo (`TRY=X`, dollars en livres turques ; `EURTRY=X`), le **2026-10-01**
> (§ 13.7). Les **taux directeurs, l'inflation, les réserves et les flux** n'y
> figurent pas : ils viennent de sources secondaires (Banque centrale de Turquie,
> TurkStat, presse financière) et sont des **ordres de grandeur**, à vérifier
> avant tout réemploi. Les calculs du § 13.4 sont exacts **à partir de ces
> hypothèses**.

---

## 13.1 — Le dispositif

Le [module 12](12-cas-d-etude-livre-sterling-1992.md) montrait une banque centrale
qui défendait une parité **trop haute** pour son économie, et un spéculateur qui
pariait contre elle. La Turquie de 2025 présente la configuration inverse : une
banque centrale qui offre des **taux très élevés** pour casser une inflation
massive, et qui laisse sa monnaie glisser **moins vite que l'inflation**. Les
spéculateurs ne l'attaquent pas : ils lui **prêtent**.

**L'arrière-plan, mesuré sur `TRY=X` :**

| Année | Dollar en livres, fin d'année | Variation | Contexte (sources secondaires) |
|---|---|---|---|
| 2018 | 5,27 | **+39,6 %** | crise de change d'août, sanctions américaines |
| 2021 | 13,29 | **+80,2 %** | baisses de taux malgré l'inflation (politique « non orthodoxe ») |
| 2022 | 18,70 | +40,7 % | inflation au-delà de **80 %** en octobre |
| 2023 | 29,52 | +57,8 % | retour à l'orthodoxie après les élections de mai ; taux porté de 8,5 % à 42,5 % |
| 2024 | 35,31 | +19,6 % | taux directeur à **50 %** de mars à novembre |
| **2025** | **42,95** | **+21,7 %** | baisses de taux graduelles, interrompues en mars |

Un dollar qui monte de 80 % signifie une livre qui perd $1-1/1{,}802=$ **44 %**
de sa valeur. En 2025, la livre perd $1-1/1{,}217=$ **17,8 %** face au dollar.

**L'année 2025 (taux et inflation : sources secondaires) :**

| Date | Fait | Chiffre |
|---|---|---|
| 31 déc. 2024 | Dollar en livres | **35,31** |
| 23 janv. 2025 | Baisse du taux directeur | 47,5 % → **45 %** |
| 6 mars | Nouvelle baisse | → **42,5 %** |
| 19 mars | Arrestation du maire d'Istanbul, principal opposant | dollar à **40,86** en séance, contre 36,63 la veille |
| 20 mars | Réunion d'urgence : taux de prêt au jour le jour relevé | → **46 %** |
| 17 avril | Taux directeur relevé | → **46 %** |
| 24 juil. | Reprise des baisses | → **43 %** |
| 11 sept. / 23 oct. / 11 déc. | Baisses successives | → **40,5 %**, **39,5 %**, **38 %** |
| déc. 2025 | Inflation sur un an | ≈ **31 %** (≈ 44 % fin 2024) |
| 31 déc. 2025 | Dollar en livres | **42,95** |

## 13.2 — Le diagnostic : une désinflation par le change

La banque centrale suivait une stratégie précise : **taux réel positif** et
**appréciation réelle** de la livre. Ce qu'il faut entendre par là :

| | Valeur 2025 | Calcul |
|---|---|---|
| Taux directeur moyen | ≈ **43 %** | moyenne des niveaux du § 13.1, pondérée par leur durée |
| Inflation de fin d'année | ≈ **31 %** | |
| Taux réel ex post (déc.) | ≈ **+7 pt** | 38 − 31 |
| Écart d'inflation avec les États-Unis | ≈ **27,5 %** | $1{,}31/1{,}027-1$ |
| Dépréciation nominale (dollar en livres) | **+21,7 %** | mesurée |
| **Appréciation réelle de la livre** | ≈ **+4,7 %** | $1{,}275/1{,}217-1$ |

> 🔑 **La livre a perdu 18 % de sa valeur nominale et gagné près de 5 % en
> valeur réelle.** Elle glissait, mais moins vite que les prix turcs ne montaient
> par rapport aux prix américains. Une livre qui s'apprécie en termes réels rend
> les importations moins chères, ce qui freine l'inflation : c'est
> l'**instrument** de la désinflation, pas un accident.

Cette stratégie a un coût et une condition :

- **le coût** : les exportateurs perdent en compétitivité, et la banque
  centrale doit accumuler, puis parfois vendre, des réserves pour tenir la
  trajectoire ;
- **la condition** : que les capitaux étrangers continuent à venir chercher le
  taux. S'ils sortent ensemble, la banque centrale doit vendre ses réserves ou
  laisser la livre décrocher, et la désinflation s'interrompt.

C'est le trilemme du [§ 12.2](12-cas-d-etude-livre-sterling-1992.md), sous une
autre forme : capitaux libres et change piloté imposent la politique monétaire.
La différence avec 1992 est que les taux allaient **dans le sens** dont
l'économie avait besoin, la désinflation. La promesse était soutenable tant que
la confiance politique tenait.

## 13.3 — Le carry trade, pièce par pièce

Un investisseur en dollars emprunte des dollars, les convertit en livres, place
les livres au taux turc, puis reconvertit à l'échéance. Sur une durée $t$, son
rendement excédentaire vaut

$$R=\frac{S_0}{S_1}\,(1+i_{\text{TRY}}\,t)-(1+i_{\text{USD}}\,t)$$

où $S$ est le dollar en livres. Trois termes, trois risques :

| Terme | Ce qu'il rapporte ou coûte | En 2025 |
|---|---|---|
| $i_{\text{TRY}}$ | le taux turc, encaissé | ≈ **43 %** |
| $i_{\text{USD}}$ | le coût du financement en dollars | ≈ **4,2 %** |
| $S_0/S_1$ | la perte de change, si la livre baisse | $35{,}31/42{,}95=$ **0,822** |

**Facteurs favorables à la position acheteuse de livres :**

| Facteur | Pourquoi il comptait |
|---|---|
| Écart de taux énorme | ≈ 39 points par an : la livre pouvait perdre plus d'un quart de sa valeur avant que la position ne perde |
| Glissement piloté | la banque centrale lissait la trajectoire : volatilité **hors mars** de **2,1 %** par an, mesurée |
| Taux réel positif | la banque centrale signalait qu'elle ne referait pas 2021 |
| Équipe économique crédible | le ministre des finances et la banque centrale en place depuis 2023 avaient tenu un taux de 50 % pendant huit mois |

**Défavorables :**

| Facteur | Ce qu'il pouvait coûter |
|---|---|
| Risque politique | une décision politique peut retourner la confiance en une séance : c'est arrivé le 19 mars |
| Sortie collective | tout le monde porte la même position ; si tout le monde sort, la sortie est étroite |
| Réserves limitées | la défense consomme des réserves, et le marché les compte |
| Baisses de taux | chaque baisse réduit le portage ; une baisse trop rapide rappelle 2021 |
| Précédents | 2018 et 2021 : la livre a perdu 28 % et 44 % de sa valeur dans l'année |

## 13.4 — Les compléments chiffrés

### Le rendement de l'année

Avec les hypothèses du § 13.3, sur un an ($t=1$) :

$$R=0{,}822\times1{,}43-1{,}042=1{,}1755-1{,}042\approx\mathbf{+13{,}3\ \%}$$

Le taux turc rapportait 43 %, la livre en a perdu 17,8 %, le financement en a
coûté 4,2 : il reste environ **13 points**. C'est l'ordre de grandeur des
rendements annoncés pour le carry turc en 2025, sous réserve des taux
effectivement obtenus — un étranger passe le plus souvent par des **swaps de
change**, dont le taux implicite s'écarte du taux directeur.

### Le change à terme n'est pas une prévision

Le cours à terme à un an est fixé par l'**absence d'arbitrage** :

$$F=S_0\,\frac{1+i_{\text{TRY}}}{1+i_{\text{USD}}}=35{,}31\times\frac{1{,}43}{1{,}042}\approx\mathbf{48{,}5}$$

| | Dollar en livres | Écart au comptant de départ |
|---|---|---|
| Comptant, 31 déc. 2024 | 35,31 | — |
| **À terme**, échéance fin 2025 | ≈ **48,5** | +37 % |
| Réalisé, 31 déc. 2025 | **42,95** | +21,7 % |
| Réalisé, 30 sept. 2026 | **49,01** | +38,8 % |

Le cours à terme annonçait 48,5 pour fin 2025 ; le comptant y est arrivé
**neuf mois plus tard**. Le gain du carry trade est exactement cet écart :
$48{,}5/42{,}95-1\approx13\ \%$.

> 🔑 **Si le cours à terme prévoyait le comptant futur, le carry trade ne
> rapporterait rien en moyenne.** C'est l'**hypothèse de parité non couverte des
> taux d'intérêt**, et elle échoue : Fama (1984) montre que les monnaies à taux
> élevé se déprécient en moyenne **moins** que l'écart de taux, voire
> s'apprécient. Ce « puzzle de la prime à terme » est la source du rendement
> moyen du carry trade. Le prix de ce rendement est la queue de distribution.

### La queue de distribution : le 19 mars

| Mesure (`TRY=X`) | Valeur |
|---|---|
| Volatilité annuelle 2025 | **4,0 %** |
| Volatilité annuelle 2025, **hors 19-20 mars** | **2,1 %** |
| Plus forte hausse du dollar en une clôture | **+3,5 %** (log), le 20 mars |
| Hausse en séance, 19 mars | 36,63 → **40,86**, soit **+11,5 %** |

**Deux journées font la moitié de la volatilité de l'année.** Une série qui
glisse de 0,4 % par semaine pendant des mois, puis saute de 11 % en quelques
heures, n'est pas décrite par son écart-type : c'est l'avertissement du
[module 4 de l'alpha](../alpha/04-cinq-pieges.md) sur les mesures de risque
calculées sans l'événement rare.

Ce que le choc a coûté, en jours de portage. Le portage net vaut
$(42{,}5-4{,}2)/365\approx$ **0,105 % par jour** :

| Sortie | Perte de change | Jours de portage effacés |
|---|---|---|
| Clôture du 20 mars | $37{,}99/36{,}63-1=$ **+3,7 %** | ≈ **35 jours** |
| Au pire de la séance du 19 mars | **+11,5 %** | ≈ **110 jours**, près de **quatre mois** |

> 🔑 **Le profil du vendeur d'assurance, mesuré.** Un rendement régulier
> d'environ 0,1 % par jour, et une seule séance qui peut en effacer quatre mois.
> Le porteur qui a tenu a fini l'année à +13 % ; celui qui a dû vendre au pire
> du 19 mars, par appel de marge ou par limite de risque, a réalisé la perte. Le
> résultat dépend moins du diagnostic que de la **capacité à ne pas être forcé
> de sortir**.

La banque centrale a tenu la livre en vendant ses réserves : de l'ordre de
**25 Md $** dans les premiers jours, davantage sur les semaines suivantes, selon
les estimations de marché. C'est ce qui a ramené le dollar de 40,86 à 38 en
séance. Sans cette défense, la sortie des porteurs aurait fixé le prix.

### Et la position de 1992, appliquée à 2025 ?

Vendre la livre turque, c'est payer le portage au lieu de l'encaisser. Une
vente ouverte au 18 mars — la veille du choc, le meilleur moment de l'année —
et tenue jusqu'au 31 décembre, soit 0,79 an :

$$R=\frac{42{,}95}{36{,}63}\times\frac{1+0{,}042\times0{,}79}{1+0{,}43\times0{,}79}-1=1{,}1725\times\frac{1{,}033}{1{,}340}-1\approx\mathbf{-9{,}6\ \%}$$

| | Sterling 1992 | Livre turque 2025 |
|---|---|---|
| Position gagnante | vendre la devise | **acheter** la devise |
| Portage du vendeur | ≈ −0,4 pt / an | ≈ **−39 pt / an** |
| Dépréciation nécessaire pour qu'un vendeur gagne | quelques dixièmes de point | ≈ **37 %** dans l'année |
| Banque centrale | défend une parité contre son cycle | pilote un glissement **conforme** à son objectif |
| Issue | la parité casse | la défense tient, le carry gagne |

> 🔑 **La même idée — « cette monnaie va baisser » — était juste dans les deux
> cas, et n'a payé qu'en 1992.** La livre turque a bien baissé, de 18 %. Mais un
> pari directionnel se juge contre le **cours à terme**, pas contre le comptant :
> la baisse était déjà dans les prix, et au-delà. En 1992, le portage était
> négligeable et la baisse ne l'était pas ; en 2025, c'était l'inverse.

## 13.5 — La lecture réflexive

Le cadre de l'agent [`sorosien`](../../../../../.claude/agents/sorosien.md)
s'applique, avec le signe retourné :

1. **Phase auto-renforçante.** Les capitaux entrent pour le taux, la livre
   glisse lentement, la banque centrale accumule des réserves, la désinflation
   progresse, la confiance attire de nouveaux capitaux.
2. **Le point fragile n'est pas économique.** La boucle tenait sur les
   fondamentaux ; elle a vacillé sur un fait **politique**, comme en 1992 le
   point de rupture était politique.
3. **Le test.** Une séquence réflexive se juge à sa réaction au choc : en mars
   2025, la banque centrale a eu les réserves et la volonté de remonter les
   taux, et la boucle a repris. **Elle n'a pas cassé**, ce qui la distingue de
   1992 — et ce qui ne dit rien de la prochaine fois.

## 13.6 — Ce que le cas ne permet pas de conclure

> ⚠️ **Une année qui finit bien ne mesure pas une stratégie à queue épaisse.** Le
> carry turc a gagné en 2024 et en 2025. Il a perdu massivement en 2018 et en
> 2021, quand la livre a perdu 28 % et 44 % de sa valeur avec des taux bien plus
> bas qu'en 2025. Un rendement de 13 % pour une volatilité de 4 % donne un ratio
> de Sharpe proche de **3** : c'est précisément le chiffre que produit une
> stratégie qui vend une assurance contre un événement **qui ne s'est pas
> produit en entier** dans l'échantillon.

- **Un an, un choc.** Mars 2025 a été absorbé par la banque centrale ; rien
  n'établit qu'un choc suivant le serait. C'est le piège de l'[expérience
  10](../../../../done/experimentation/experience_10/README.md) retourné : une
  résistance éprouvée sur un seul épisode n'est pas éprouvée.
- **Le taux encaissé n'est pas le taux directeur.** Un investisseur étranger
  passe par des swaps, des dépôts ou des titres d'État, dont les rendements
  diffèrent ; les 13 % du § 13.4 sont un ordre de grandeur, pas une mesure.
- **Le cas est choisi après coup.** On l'étudie parce qu'il illustre le carry
  trade sur une année récente, et parce qu'il fait contraste avec le module 12.
  C'est un choix pédagogique, pas un échantillon.
- **Le risque de change ne se diversifie pas dans la même devise.** Toutes les
  positions en livres turques encaissent le même choc le même jour : l'erreur
  type du [cours alpha](../alpha/02-le-calcul-et-ses-erreurs-types.md) se
  compte par dates, pas par positions.

## 13.7 — Reproduire

Les cours de change de ce module ont été obtenus le **2026-10-01** :

```python
import yfinance as yf

d = yf.download("TRY=X", start="2017-12-01", end="2026-10-01", auto_adjust=False)
```

- **Variations annuelles** : dernière clôture de l'année sur dernière clôture de
  l'année précédente.
- **Volatilité** : écart-type des rendements logarithmiques quotidiens de 2025,
  multiplié par $\sqrt{252}$.
- **Séance du 19 mars** : colonne `High` du 19 mars, comparée à la clôture du
  18 mars.

⚠️ L'horodatage des clôtures de change sur Yahoo est décalé : la clôture datée
du 19 mars (36,70) précède le choc, qui apparaît dans la clôture du 20 mars
(37,99). Seul le plus haut de la séance du 19 mars en garde la trace.

## Exercices

**E13.1.** Recalculer le rendement du carry de 2025 si l'investisseur ne
touchait que 38 % par an, le taux de fin d'année. *À partir de quel taux turc la
position aurait-elle été nulle ?*

**E13.2.** Un porteur de carry finance sa position avec un levier de 5. Quelle
perte subit-il sur ses fonds propres au pire de la séance du 19 mars ? *Pourquoi
le levier transforme-t-il un rendement annuel positif en une faillite possible ?*

**E13.3.** Avec $i_{\text{TRY}}=43\ \%$ et $i_{\text{USD}}=4{,}2\ \%$, quelle
dépréciation annuelle de la livre annule exactement le gain du carry ? Comparer
au cours à terme du § 13.4. *Que conclure sur ce que « contient » un cours à
terme ?*

## Ce qu'il faut retenir

1. En 2025, la livre turque a perdu **17,8 %** face au dollar, et gagné environ
   **5 %** en termes réels : un glissement piloté, instrument de la
   désinflation.
2. Le carry trade a rapporté de l'ordre de **+13 %** : 43 points de taux, moins
   18 de change, moins 4 de financement.
3. Le cours à terme annonçait **48,5** ; le comptant finit à **42,95**. Le gain
   du carry est cet écart, et il existe parce que la parité non couverte des
   taux **échoue**.
4. **Deux séances** font la moitié de la volatilité de l'année ; le choc du
   19 mars pouvait effacer **quatre mois** de portage.
5. La vente de la livre, juste en 1992, aurait perdu environ **10 %** en 2025 :
   un pari directionnel se juge contre le cours à terme, pas contre le comptant.

> ⚠️ **Ce module ne donne aucun conseil en investissement.** Il décrit une
> position historique et la mécanique qui en a fait le résultat ; il ne dit ni
> quelle devise acheter ou vendre, ni quand.

---

⬅️ [Module 12 — Cas d'étude : la livre sterling, 1992](12-cas-d-etude-livre-sterling-1992.md) ·
➡️ [Module 14 — Cas d'étude : la Russie, 2022-2026](14-cas-d-etude-russie-2022-2026.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
