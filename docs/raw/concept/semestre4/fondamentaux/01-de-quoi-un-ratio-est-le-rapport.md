# Module 1 — De quoi un ratio est le rapport

**Prérequis :** aucun.
**Ce qu'on établit ici :** qu'un ratio fondamental rapporte toujours une grandeur de **marché** à une grandeur **comptable**, que le choix du numérateur décide si la dette est comptée, et que ce choix suffit à renverser un classement.

---

## 1.1 — Deux mondes dans une seule fraction

Tout ratio fondamental a la même forme :

$$\text{ratio} = \frac{\text{ce que le marché paie}}{\text{ce que la comptabilité constate}}$$

Les deux étages n'ont rien en commun.

| | Numérateur — le marché | Dénominateur — la comptabilité |
|---|---|---|
| **Nature** | un prix d'échange | un agrégat de règles |
| **Fréquence** | continue, chaque seconde de séance | quatre fois par an au mieux |
| **Orientation** | tourné vers l'avenir : il escompte | tourné vers le passé : il constate |
| **Révision** | jamais — un prix passé reste ce qu'il fut | fréquente : retraitements, changements de norme |
| **Liberté** | aucune : c'est un fait observable | large — c'est tout le [module 3](03-ce-que-la-comptabilite-laisse-au-choix.md) |

> 🔑 **Un ratio est donc un taux de change entre une anticipation et un
> constat.** Il ne mesure pas la cherté. Il mesure **de combien** le marché
> s'écarte de ce que les comptes montrent — et cet écart peut être justifié.

## 1.2 — Les deux numérateurs, et c'est là que tout se joue

Il n'existe que deux façons de chiffrer « ce que le marché paie ».

**La capitalisation** $\text{Capi} = \text{cours} \times \text{nombre d'actions}$
est le prix des **actions seules**. Elle ignore la dette.

**La valeur d'entreprise** est le prix de l'**outil industriel entier**, quel que
soit qui le finance :

$$\text{VE} = \text{Capi} + \text{dette nette}$$

Racheter une entreprise, c'est acheter ses actions **et** reprendre sa dette. La
VE est le chèque total ; la capitalisation n'en est que la part payée aux
actionnaires.

D'où la partition décisive des ratios :

| Numérateur | Ratios concernés | La dette est… |
|---|---|---|
| Capitalisation | **PER**, **P/B**, **rendement du FCF**, rendement du dividende | …ignorée |
| Valeur d'entreprise | **VE/EBITDA**, VE/CA, VE/FCF | …comptée |

Le rapport $\text{VE}/\text{Capi}$ mesure d'un coup d'œil ce que le premier
groupe passe sous silence. Sur le fil rouge :

| | VE / Capi | Lecture |
|---|---|---|
| AIR.PA | **1,008** | dette nette quasi nulle : PER et VE/EBITDA racontent la même histoire |
| SU.PA | 1,098 | — |
| MC.PA | 1,118 | — |
| TTE.PA | 1,209 | — |
| **ORA.PA** | **2,204** | **la dette nette dépasse la valeur des actions** |

## 1.3 — Le renversement : TotalEnergies contre Orange

Voici pourquoi cette partition n'est pas une subtilité d'école.

| | PER | Classement | VE/EBITDA | Classement | Dette/EBITDA |
|---|---|---|---|---|---|
| **TTE.PA** | 10,90 | 2ᵉ | **5,04** | **1ᵉʳ** | 1,59 |
| **ORA.PA** | **10,27** | **1ᵉʳ** | 7,35 | 2ᵉ | 4,69 |

Au PER, Orange est la moins chère des deux. À la valeur d'entreprise, elle est
**46 % plus chère**. Les deux calculs sont exacts ; ils ne portent simplement pas
sur le même objet.

L'explication tient en une phrase : le PER d'Orange est bas **parce que** son
bénéfice est calculé après des charges d'intérêt élevées, sur un capital
actionnarial qui ne représente qu'un tiers du financement total. On ne peut pas
se réjouir d'un PER bas obtenu par l'endettement, puis ignorer l'endettement.

> ⚠️ **Ne classe jamais des sociétés au PER si leurs niveaux d'endettement
> diffèrent.** Le classement obtenu mesure le levier autant que la valorisation.
> Dette/EBITDA de 4,69 contre 1,59 : ce sont deux structures financières
> différentes, pas deux prix comparables.

## 1.4 — Les quatre dénominateurs usuels

| Dénominateur | Ratio | Ce qu'il capture | Ce qu'il laisse passer |
|---|---|---|---|
| **Bénéfice net** ($E$) | PER | le résultat revenant à l'actionnaire | le plus manipulable : il vient après amortissements, provisions, impôt et éléments exceptionnels |
| **Fonds propres** ($B$) | P/B | le capital comptable accumulé | ignore tout actif immatériel non acquis ; voir [module 3](03-ce-que-la-comptabilite-laisse-au-choix.md) |
| **EBITDA** | VE/EBITDA | la génération opérationnelle avant financement et amortissement | **n'est pas une norme comptable** ; ignore l'intensité capitalistique |
| **Flux de trésorerie disponible** (FCF) | Rendement du FCF | l'argent réellement encaissé | très volatil d'un exercice à l'autre |

## 1.5 — Bénéfice contre trésorerie : l'écart qui informe

Le **rendement du bénéfice** $1/\text{PER}$ et le **rendement du FCF** répondent à
la même question — « combien l'entreprise rapporte-t-elle, rapporté à son
prix ? » — l'un en comptabilité d'engagement, l'autre en caisse. Leur écart est
un signal en soi.

| | $1/\text{PER}$ | Rdt FCF | Écart |
|---|---|---|---|
| AIR.PA | 3,70 % | 1,95 % | **−1,75 pt** |
| TTE.PA | 9,17 % | 8,19 % | −0,98 pt |
| OR.PA | 3,03 % | 3,09 % | +0,06 pt |
| MC.PA | 4,78 % | 5,11 % | +0,33 pt |
| SU.PA | 2,81 % | 3,17 % | +0,36 pt |
| SAN.PA | 4,19 % | 6,81 % | +2,62 pts |
| ORA.PA | 9,74 % | 15,83 % | **+6,09 pts** |

Les deux extrêmes se lisent de façon opposée, et aucun des deux n'est un verdict :

- **Écart négatif** (AIR.PA) : le bénéfice comptable ne se transforme pas
  intégralement en trésorerie sur l'exercice. Besoin en fonds de roulement,
  investissement, stocks — courant dans l'industrie à cycle long.
- **Écart largement positif** (ORA.PA) : les amortissements pèsent lourd sur le
  bénéfice sans sortie de caisse correspondante. C'est structurel chez un
  opérateur télécom, dont le réseau est amorti pendant des années après avoir
  été payé.

> **Ce que l'écart ne dit pas.** Il ne dit pas laquelle des deux mesures est la
> « vraie ». Le FCF d'une année où l'on n'investit pas paraît excellent, et
> prépare une année suivante médiocre. Un écart se lit sur plusieurs exercices —
> ce que la source de ce dépôt **ne permet pas** ([module 2](02-les-quatre-dates-d-un-ratio.md)).

## Ce qu'il faut retenir

1. Un ratio rapporte une anticipation de marché à un constat comptable.
2. Le choix du numérateur décide si la dette est comptée — et suffit à renverser
   un classement, comme entre TotalEnergies et Orange.
3. $\text{VE}/\text{Capi}$ dit en un nombre ce que le PER passe sous silence.
4. L'écart entre rendement du bénéfice et rendement du FCF décrit un modèle
   économique ; il ne le juge pas.

---

⬅️ [README du cours](README.md) ·
➡️ [Module 2 — Les quatre dates d'un ratio](02-les-quatre-dates-d-un-ratio.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
