# mesurer_indicateurs.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py`, dans
l'ordre du déroulement. Il fait autorité : toute évolution du script doit
d'abord être décrite ici.

## Rôle

Chiffrer les **dix indicateurs** du [cours Soros et Steinhardt](../README.md) et
les lire selon les seuils **déclarés au [module 9](../09-assembler-la-sequence.md)**.
Deux relevés et une synthèse sont imprimés sur la console :

- **A — le contexte**, commun à toutes les valeurs : politique monétaire et taux
  (indicateur 2), crédit (3), change (8), croissance et inflation (9) ;
- **B — une fiche par valeur** : attentes de bénéfices (1), multiples (4), levier
  (5), marges (6), dilution (7), sensibilité au change (8), positionnement (10) ;
- **la synthèse** : les quatre marqueurs de boom et les trois marqueurs de
  bascule du module 9, valeur par valeur.

Le script est versionné **à côté du cours qu'il chiffre**, comme
[`mesurer_macro.py`](../../macro/figures/mesurer_macro.md) l'est pour le cours
macro. Il ne compte pas parmi les onze utilitaires, **appelle le réseau**, et
**n'écrit aucun fichier**.

## Dépendances

`yfinance`, avec le `pandas` qu'il installe. Les sources hors Yahoo — BCE,
Eurostat, BRI, AMF — sont lues par `urllib`, sans dépendance de plus.

Trois fonctions sont **empruntées au dépôt** plutôt que réécrites, par un import
local après ajout de leur répertoire au chemin (le dépôt n'est pas un paquet,
d'où les `# noqa: PLC0415`) :

| Fonction | Origine |
|---|---|
| `p_valeur_student` | [`python/import_societe.py`](../../../../../../python/import_societe.md) |
| `mco` (moindres carrés, constante en tête) | [`macro/figures/mesurer_macro.py`](../../macro/figures/mesurer_macro.md) |
| `holm` | idem |

## Arguments

| Argument | Défaut | Effet |
|---|---|---|
| `tickers` | `AIR.PA MC.PA OR.PA SAN.PA TTE.PA BNP.PA SU.PA ORA.PA` | les valeurs à ficher — par défaut les huit du [cours fondamentaux](../../fondamentaux/README.md) ; mis en majuscules |
| `--isin TICKER=ISIN` | — | répétable ; donne l'ISIN d'une valeur hors de la table interne, sans quoi ses positions courtes ne sont pas lues. Une valeur sans `=` arrête le script (code 2) |

Il n'y a **pas d'invite interactive** : sans argument, le script fiche les huit
valeurs par défaut.

## Constantes déclarées

| Constante | Valeur | Rôle |
|---|---|---|
| `ISIN` | les huit valeurs par défaut | pour lire le fichier de l'AMF, indexé par ISIN |
| `INDICE`, `CHANGE` | `^FCHI`, `EURUSD=X` | marché (indice **nu**) et change, pour l'indicateur 8 |
| `CREDIT_HY`, `CREDIT_GOV` | `HYG`, `IEF` | la procuration de crédit du [cours macro](../../macro/08-le-credit.md) |
| `SERIE_TAUX_10`, `SERIE_TAUX_3M` | courbe **AAA** de la zone euro, BCE (`YC`) | taux souverains à 10 ans et à 3 mois, en % |
| `SERIE_DEPOT` | taux de la facilité de dépôt, BCE (`FM`) | le taux directeur qui pilote le marché monétaire |
| `SERIE_PRETS_SNF` | prêts aux sociétés non financières, zone euro, BCE (`BSI`) | **taux de croissance annuel**, en % |
| `EUROSTAT` | jeux `prc_hicp_minr` et `namq_10_gdp` | inflation (IPCH, glissement annuel) et PIB réel (glissement annuel), zone euro |
| `BRI` | `WS_CREDIT_GAP`, France | écart du ratio crédit/PIB à sa tendance, en points de PIB |
| `AMF_JEU` | recherche data.gouv.fr | le jeu des positions courtes nettes publiées par l'AMF |
| `DECALAGE` | `75` jours | délai présumé entre clôture d'exercice et publication — le repli de [`reconstituer_fondamentaux.py`](../../../../../../python/reconstituer_fondamentaux.md) |
| `TAUX_ACTUALISATION` | `0.08` | le $r$ de Gordon, celui du [module 4 du cours fondamentaux](../../fondamentaux/04-un-ratio-n-existe-que-relatif.md) |
| `CROISSANCE_LONGUE` | `3.0` % | croissance nominale de long terme au-delà de laquelle une croissance implicite est dite **exigeante** |
| `HORIZON` | `3` ans | fenêtre de la décomposition du rendement et de la dilution longue |
| `SEMAINES` | `156` | nombre maximal de semaines de la régression de change |
| `SEUIL_SAUT` | `0.50` | le contrôle des opérations sur titres |
| `ALPHA` | `0.05` | seuil du test de change et de Holm |
| `TOLERANCE_BPA` | `1.5` | rapport maximal entre BPA attendu de l'exercice et BPA des douze derniers mois |
| `FENETRE_ACTIONS` | `30` jours | fenêtre de la médiane du nombre d'actions |
| `TOLERANCE_DETTE` | `2.0` | écart maximal toléré entre la dette des comptes annuels et celle du jour |

### Seuils de lecture

Déclarés au [module 9](../09-assembler-la-sequence.md), **avant** toute mesure :

| Constante | Valeur | Lecture |
|---|---|---|
| `S_REVISION` | `2.0` % | révision du BPA attendu sur 90 jours : ↑ au-delà de +2 %, ↓ en deçà de −2 % |
| `S_DIFFUSION` | `0.5` | diffusion des révisions : ↑ au-delà de +0,5, ↓ en deçà de −0,5 |
| `S_DETTE` | `3.0` | dette/EBITDA au-delà : « dette lourde » |
| `S_COUVERTURE` | `3.0` | couverture des intérêts en deçà : « couverture tendue » |
| `S_DYNAMIQUE` | `10.0` pt | croissance de la dette moins celle de l'EBITDA au-delà : « levier qui monte » |
| `S_MARGE` | `2.0` pt | marge opérationnelle au-dessus de sa propre moyenne au-delà : « au-dessus de sa moyenne » |
| `S_DILUTION` | `2.0` % | variation du nombre d'actions sur un an : « émet » au-delà de +2 %, « rachète » en deçà de −2 % |
| `S_COURTES` | `2.0` % | positions courtes publiées au-delà : « notable » |
| `S_VOLUME` | `1.5` | volume 20 séances / 250 séances au-delà : « inhabituel » |
| `S_ECART_CREDIT` | `10.0` pt | écart crédit/PIB au-delà : « au-dessus du seuil d'alerte » (seuil de la BRI) |

## Déroulement

### 1. Préparation

Les `--isin` sont fusionnés à la table interne. Les trois fonctions empruntées
sont importées. La date du relevé est `date.today()`, imprimée en tête avec le
rappel du `DECALAGE`.

### 2. Relevé A — le contexte

Chaque bloc est enveloppé d'un `except` qui **imprime l'erreur sur la sortie
d'erreur** (`! source : Type: message`) et laisse le bloc vide. Une panne réseau
ne se confond jamais avec une donnée absente.

**Indicateur 2 — taux.** Séries BCE depuis 372 jours. Pour la **dernière date du
taux à 10 ans** : taux de dépôt et sa variation sur 365 jours, taux à 3 mois,
taux à 10 ans, **pente** $= y^{10} - y^{3M}$ (« courbe inversée » si elle est
négative), variation du 10 ans sur 365 jours. Chaque valeur « au » jour $j$ est la
dernière observation de période $\le j$.

**Indicateur 9 — croissance et inflation.** Eurostat : les 13 derniers mois
d'inflation (unité `RCH_A`, `coicop18=TOTAL`) et les 5 derniers trimestres de PIB
réel (`CLV_PCH_SM`, corrigé des variations saisonnières). Impression de la
dernière inflation et de celle du premier mois reçu (un an plus tôt), du dernier
PIB réel, et de la **croissance nominale approchée** $g + \pi$. Si le taux à
10 ans est connu : **taux réel ex post** $= y^{10} - \pi$.

**Indicateur 3 — crédit.** Trois lignes, chacune indépendante :

- croissance annuelle des prêts aux sociétés non financières, dernière valeur et
  celle de douze observations plus tôt ;
- écart crédit/PIB de la BRI pour la France, dernier trimestre, avec l'alerte
  au-delà de `S_ECART_CREDIT` ;
- **procuration de marché** : $100 \times (P^{HYG}_t/P^{HYG}_{t-13s} - P^{IEF}_t/P^{IEF}_{t-13s})$,
  cours ajustés, négative quand l'écart de crédit s'élargit.

**Indicateur 8 — change.** `EURUSD=X` au jour du relevé et sa variation sur
365 jours.

### 3. Données communes du relevé B

Rendements hebdomadaires (dernière cotation de la semaine close le vendredi) de
`^FCHI` (non ajusté — un indice nu) et de `EURUSD=X`, depuis $366 \times (\text{HORIZON}+1)$
jours. Puis le fichier de l'AMF : le premier jeu data.gouv.fr dont une ressource
est un CSV d'URL contenant `vad`, lu en entier (séparateur `;`). Chacun des deux
peut échouer seul : l'indicateur correspondant reste vide pour toutes les valeurs.

### 4. Relevé B — une fiche par valeur

**Indicateur 1 — attentes.** `info` (lu une fois pour toute la fiche), puis
`eps_trend`, `eps_revisions`, `earnings_estimate`.
Les lignes `0y` (exercice en cours) et `+1y` (suivant) :

| Quantité | Formule |
|---|---|
| révision sur 90 jours | $100 \times (\text{current}/\text{90daysAgo} - 1)$, vide si la valeur d'il y a 90 jours n'est pas positive |
| diffusion sur 30 jours | $(h - b)/(h + b)$, $h$ et $b$ sommés sur `0y` et `+1y` ; vide si $h + b = 0$ |
| croissance attendue N+1/N | $100 \times (\text{BPA}_{+1y}/\text{BPA}_{0y} - 1)$ |
| dispersion | $100 \times (\text{high} - \text{low})/|\text{avg}|$ de `0y` |
| cohérence des définitions | $\text{BPA}_{0y}/\text{trailingEps}$, vide si `trailingEps` n'est pas positif |

Flèches selon `S_REVISION` et `S_DIFFUSION`. Le nombre d'analystes est celui de
`0y`. Une troisième ligne imprime le BPA des douze derniers mois et le rapport de
cohérence ; s'il sort de `[1/TOLERANCE_BPA ; TOLERANCE_BPA]`, elle ajoute
`⚠ définitions probablement différentes` : le consensus et le BPA comptable ne
mesurent sans doute pas le même bénéfice (le cas de Sanofi au
[module 2](../02-les-attentes-de-benefices.md)). Le contrôle n'efface rien : il
prévient que le PER et la croissance implicite, calculés sur le BPA comptable, ne
se comparent pas au consensus.

**Cours, comptes et actions.** Historique **non ajusté des dividendes**
(`auto_adjust=False`, qui garde `Close` corrigée des seules divisions et
`Adj Close` corrigée des dividendes), depuis $366 \times (\text{HORIZON}+1)$ jours ;
contrôle des sauts de plus de 50 % sans division déclarée ; comptes **annuels**
(`income_stmt`, `balance_sheet`) ; `get_shares_full()`. Un échec ici arrête la
fiche après l'indicateur 1 — avec le message d'erreur.

Un exercice est **publié au jour $j$** si sa clôture $\le j - \text{DECALAGE}$.

Le **nombre d'actions au jour $j$** est la **médiane** des observations de
`get_shares_full()` datées de $]j - \text{FENETRE\_ACTIONS} ; j]$, ou, s'il n'y en a
aucune, la dernière observation antérieure. La série du fournisseur mêle des
décomptes avec et sans actions autodétenues : à l'intérieur d'un même mois, elle
varie jusqu'à 4 % pour TotalEnergies, soit deux fois le seuil de dilution. Une
valeur ponctuelle tirerait au sort la lecture.

**Indicateur 4 — multiples.**

| Quantité | Formule |
|---|---|
| PER, PER prévisionnel | `trailingPE`, `forwardPE` de Yahoo, tels quels |
| croissance implicite | $100 \times (r - 1/\text{PER})$, payout 100 % ; vide si PER $\le 0$ ; « exigeant » au-delà de `CROISSANCE_LONGUE` |
| rendement bénéficiaire − taux 10 ans | $100/\text{PER} - y^{10}$, en points ; vide sans taux |

Puis la **décomposition du rendement** entre $d_0 = $ aujourd'hui − 3 × 365,25 jours
et aujourd'hui, en points de log :

$$\underbrace{100\ln\frac{P_1}{P_0}}_{\text{prix}} = \underbrace{100\ln\frac{\text{BPA}_1}{\text{BPA}_0}}_{\text{bénéfice}} + \underbrace{100\ln\frac{\text{PER}_1}{\text{PER}_0}}_{\text{multiple}}, \qquad \text{dividendes} = 100\ln\frac{A_1}{A_0} - \text{prix}$$

avec $P$ = `Close`, $A$ = `Adj Close`, $\text{BPA}$ = résultat net du dernier
exercice **publié** à la date, divisé par le nombre d'actions à la date. Le
multiple est obtenu **par différence**. Vide, avec son motif imprimé :

- si une **division** d'actions tombe après $d_0$ — le nombre d'actions est réel,
  `Close` est rétro-ajustée, les deux ne se comparent plus ;
- si l'un des deux BPA est **négatif ou absent**.

La ligne suivante donne les deux exercices utilisés et le PER implicite à chaque
bout, $P/\text{BPA}$.

**Indicateur 5 — levier**, sur le dernier exercice publié :

| Quantité | Formule |
|---|---|
| dette/EBITDA | `Total Debt / EBITDA`, vide si EBITDA $\le 0$ |
| couverture des intérêts | `EBIT / Interest Expense`, vide si frais $\le 0$ |
| dynamique | variation de la dette sur un exercice moins variation de l'EBITDA, en points |

Alertes selon `S_DETTE`, `S_COUVERTURE`, `S_DYNAMIQUE`.

**Contrôle de cohérence de la dette.** La dette du dernier exercice publié est
confrontée au `totalDebt` du jour (`info`, la définition de
[`import_fondamentaux.py`](../../../../../../python/import_fondamentaux.md)). Si
leur rapport sort de `[1/TOLERANCE_DETTE ; TOLERANCE_DETTE]`, la ligne imprime
les deux montants en milliards, avec `⚠ sources discordantes`, et **dette/EBITDA
comme dynamique restent vides** : l'un des deux chiffres est faux, et le script
ne sait pas lequel. Sans `totalDebt` du jour, le contrôle n'a pas lieu.

**Indicateur 6 — marges.** Marge opérationnelle `Operating Income / Total Revenue`
de chaque exercice publié ; dernière, moyenne, écart. Puis, sur les deux derniers
exercices publiés, si les quatre montants sont positifs :

$$100\ln\frac{N_1}{N_0} = \underbrace{100\ln\frac{CA_1}{CA_0}}_{\text{chiffre d'affaires}} + \underbrace{100\ln\frac{N_1/CA_1}{N_0/CA_0}}_{\text{marge nette}}$$

**Indicateur 7 — dilution.** Variation du nombre d'actions sur 365 jours et sur
`HORIZON` ans ; lecture selon `S_DILUTION`. Vide si une division tombe dans la
fenêtre.

**Indicateur 8 — change.** Sur les `SEMAINES` dernières semaines communes,
régression du rendement hebdomadaire de `Close` (non ajustée des dividendes,
**même convention que l'indice nu**) :

$$r_w = a + b_M\,\text{MARCHÉ}_w + b_F\,\text{EURUSD}_w + e_w$$

Impression de $b_M$, $b_F$, de son $t$ et de sa $p$-valeur bilatérale. La
constante $a$ n'est **pas** imprimée.

**Indicateur 10 — positionnement.**

- **Positions courtes publiées** au jour $j$ : pour l'ISIN, les lignes dont la
  date de début de publication $\le j$ et la date de fin de publication est vide
  ou $> j$ ; pour chaque détenteur, **seule la plus récente** ; somme des ratios
  et nombre de détenteurs. Calculé au jour du relevé et 90 jours plus tôt.
- **Volume relatif** : moyenne des 20 derniers volumes non nuls sur celle des
  250 derniers ; vide s'il y en a moins de 250.

### 5. Synthèse

Les $p$-valeurs de $b_F$ des valeurs qui en ont une passent par **Holm** au seuil
`ALPHA`. Puis, pour chaque valeur, sept marqueurs : `✓` présent, `·` absent, `?`
si l'une des grandeurs nécessaires est vide.

| Marqueur | Condition |
|---|---|
| **B1** révisions ↑ | révision 90 j de `0y` $\ge$ `S_REVISION` |
| **B2** hausse portée par le multiple | prix $> 0$, bénéfice $> 0$ **et** multiple $>$ bénéfice, dans la décomposition |
| **B3** levier qui monte | dynamique $>$ `S_DYNAMIQUE` |
| **B4** émission | dilution sur un an $>$ `S_DILUTION` |
| **R1** révisions ↓ sur multiple gonflé | révision $\le -$`S_REVISION`, **et** prix $> 0$ **et** multiple $> 0$ dans la décomposition |
| **R2** double extrapolation | écart de marge $>$ `S_MARGE` **et** croissance implicite $>$ `CROISSANCE_LONGUE` |
| **R3** positions courtes en hausse | variation sur 90 jours $> 0{,}5$ point |

La colonne `change*` vaut `oui` si $b_F$ est rejeté par Holm, `non` sinon, `?`
s'il n'a pas été estimé.

> ⚠️ **Correction déclarée de B2, avant toute publication.** La première version
> de B2 ne demandait que « multiple $> 0$ et multiple $>$ bénéfice ». Au premier
> relevé, elle s'est allumée sur TotalEnergies et Orange — deux valeurs dont le
> **bénéfice s'est effondré** (−34,5 et −138,3 points de log), le cours tenant.
> Un PER qui monte parce que son dénominateur tombe n'est pas un emballement du
> prix : c'est le **paradoxe du PER cyclique**, que le [module 3](../03-le-prix-des-attentes.md)
> développe. B2 exige depuis une hausse **du cours et du bénéfice**. La cause est
> identifiée, rien n'avait été publié : la correction est permise, et elle se
> déclare ici.

> ⚠️ **Pourquoi ce contrôle existe.** Au premier relevé, Orange affichait une
> dette/EBITDA de **0,62**. Dans les comptes annuels 2025 servis par Yahoo, la
> ligne `Total Debt` ne contenait que les **obligations locatives** (7,5 Md€) :
> la dette financière y manquait, alors que le `totalDebt` du même fournisseur
> annonçait 56,8 Md€, soit un ratio de 4,69. Un ratio sept fois trop bas, sans
> aucun message : c'est le cas que le contrôle attrape désormais.

> ⚠️ **Seconde correction déclarée, de R1.** R1 ne demandait d'abord que
> « révision en baisse et multiple $> 0$ ». En rédigeant la fiche du
> [module 11](../11-la-fiche-a-remplir.md), le script lancé sur **Kering** — qui
> n'est pas l'une des huit valeurs du cours — l'a allumé : son bénéfice avait
> perdu 387,6 points de log, son multiple en gagnait 315,7 par simple
> effondrement du dénominateur, et son cours **baissait**. « Le multiple a porté
> la hausse » suppose une hausse : R1 exige depuis un prix en hausse. Même
> mécanisme que B2, même discipline : cause identifiée, rien de publié,
> correction consignée ici.

## Codes de sortie

| Code | Cas |
|---|---|
| 0 | relevé imprimé, même partiellement |
| 2 | `--isin` mal formé (erreur d'`argparse`) |

Aucune panne de source n'arrête le script : chacune est imprimée sur la sortie
d'erreur et laisse vide ce qu'elle devait nourrir.

## Reproductibilité

Tout dépend de ce que servent les sources **le jour de l'appel** : le consensus
change chaque semaine, les cours à chaque séance, les comptes à chaque
publication. Deux appels le même jour, marché ouvert, diffèrent sur la deuxième
décimale. Les nombres cités par le cours ont été obtenus le **2026-10-08**.
