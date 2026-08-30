# Expérience 2 — la même règle, mais auditée

> *« Le fait que la thèse soit fausse ne signifie pas qu'il ne fallait pas la
> formuler. Au contraire : c'est en la formulant qu'on a pu s'en apercevoir. »*
> — d'après George Soros, **L'Alchimie de la finance**, 1987

Un portefeuille de **10 000 €** au 2 janvier 2025, conduit jusqu'au 31 décembre
2025 par une règle écrite à l'avance, sur les douze mêmes valeurs que
[l'expérience 1](../experience_1/README.md).

Ce n'est pas une reprise. L'expérience 1 a été relue par les trois agents du
dépôt, qui ont proposé quinze pistes puis voté pour cinq
([`review.md`](../experience_1/review.md)). **Les cinq pistes retenues sont ici
appliquées, et elles changent la nature de l'expérience** : l'expérience 1
demandait *« que rend cette règle ? »* — une question à laquelle douze mois ne
répondent pas. L'expérience 2 demande *« cette règle fait-elle ce qu'elle
déclare faire ? »* — une question à laquelle douze mois répondent très bien.

---

## Les cinq corrections, et où elles se trouvent

| Piste | Titre | Ce qu'elle devient ici |
|---|---|---|
| **T1** | Dimensionner l'expérience avant de la lancer | [§ Le dimensionnement](#le-dimensionnement-publié-avant-la-première-séance) — l'effet minimal détectable est publié **avant**, et il commande le reste du protocole |
| **T3** | Déclarer que le score n'est pas la règle du module 3 | [§ La règle dérivée](#la-règle-dérivée-ce-quelle-emprunte-et-ce-quelle-écarte) — les quatre vetos sont désormais **appliqués**, et les poids effectifs du score sont mesurés avant |
| **C3** | Déclarer le sens de `s3`, ou l'aligner | [§ Le sens de `s3`](#le-sens-de-s3-aligné-et-son-portefeuille-fantôme) — `s3` est **inversé** pour suivre la règle citée, et l'ancien sens tourne en parallèle |
| **C4** | Confronter la durée de vie de l'encadrement à la cadence | [§ La durée de vie](#la-durée-de-vie-de-lencadrement-contre-la-cadence) — τ, survie du canal et stabilité à une séance près |
| **S4** | Registre de thèses réfutables, dépouillé chaque mois | [§ Le registre](#le-registre-des-thèses-réfutables) — deux thèses par valeur et par mois, **dépouillées mécaniquement** le mois suivant |

---

## Le dimensionnement, publié avant la première séance

⚠️ C'est la piste **T1**, et elle vient en premier parce qu'elle décide de tout le
reste. Avant de lancer une expérience, on doit savoir ce qu'elle pourra
conclure. L'expérience 1 ne l'avait pas fait, et a produit un chiffre — *−4,50
points d'alpha* — qu'aucune de ses 257 séances ne permettait de distinguer de
zéro.

### Ce que l'expérience 1 a laissé mesurer

La **tracking error** du portefeuille contre sa référence, recalculée sur
[`experience_1/portefeuille.csv`](../experience_1/portefeuille.csv) :

```
ecart de rendement quotidien portefeuille - TR12, 256 observations
ecart-type annualise (x racine de 252)     TE = 8,20 %/an
```

De là, tout se déduit. L'erreur-type de l'alpha annuel sur $Y$ années vaut
$\operatorname{SE} = \text{TE}/\sqrt{Y}$, et l'**effet minimal détectable** à
95 %, bilatéral, vaut $1{,}96 \times \operatorname{SE}$ :

| Horizon | SE de l'alpha annuel | Effet minimal détectable |
|---|---|---|
| 1 an | 8,20 pt | **± 16,1 pt** |
| 3 ans | 4,73 pt | ± 9,3 pt |
| 10 ans | 2,59 pt | ± 5,1 pt |
| 65 ans | 1,02 pt | ± 2,0 pt |
| **189 ans** | 0,60 pt | **± 1,17 pt** ← les frais d'une année |

La dernière ligne est le verdict : **il faudrait 189 ans pour établir que cette
règle couvre ses propres frais.** L'alpha mesuré en 2022, −4,50 pt, demandait
13 ans pour être distingué de zéro ; il a été mesuré sur un an.

> **Conséquence, déclarée avant la première séance de 2025 : la performance de
> l'expérience 2 ne tranchera rien.** Elle sera publiée telle qu'elle sort,
> parce qu'un protocole qui cache son résultat n'en est pas un — mais elle est
> déclarée non concluante **avant** d'être connue, et aucune section de cette
> expérience ne s'appuiera dessus.

### Ce que douze mois mesurent, en revanche, très bien

Le raisonnement qui rend l'alpha indécidable rend décidables les taux. Une
proportion $p$ estimée sur $n$ observations a une erreur-type
$\sqrt{p(1-p)/n} \le 1/(2\sqrt n)$ ; l'expérience 2 collecte
**432 évaluations** de la règle et **864 dépouillements** de thèses — 432 par
type —, là où elle n'a qu'**un** point de performance annuelle.

| Quantité publiée | Observations | Incertitude 95 % | Concluante ? |
|---|---|---|---|
| Alpha du portefeuille sur l'année | 1 an | ± 16,1 pt | **non**, déclaré avant |
| Écart apparié règle alignée ↔ fantôme | 1 an, deux séries corrélées | publiée au bilan | à établir |
| Taux de déclenchement de chaque veto | 432 | ≤ ± 4,7 pt | **oui** |
| Taux de sortie de l'encadrement prolongé | 432 | ≤ ± 4,7 pt | **oui** |
| Taux de confirmation d'une thèse, par type | 432 | ≤ ± 4,7 pt | **oui** |
| Taux de bascule de `s3` à une séance près | 144 | ≤ ± 8,2 pt | **oui**, grossièrement |

**Le rapport de puissance est de trente contre un**, et il était calculable avant
de regarder la moindre séance de 2025. C'est pourquoi l'expérience 2 place son
objet déclaré sur les six dernières lignes du tableau, et non sur la première.

---

## Le protocole, déclaré avant la première séance

### La dotation et les contraintes — inchangées

| | |
|---|---|
| Dotation | **10 000 €**, en espèces, à la première séance de 2025 |
| Lignes détenues | **5 au maximum**, simultanément |
| Levier | **aucun** |
| Couverture | **aucune** |
| Vente à découvert | **aucune** |
| Fin de l'expérience | 31 décembre 2025, dernière séance de l'année |

Le solde non investi dort en espèces, sans rémunération, pour la même raison
qu'en 2022 : rémunérer les espèces demanderait de déclarer un support et un
calendrier de versement, soit une convention de plus pour un effet de quelques
euros. On ne le fait pas, et on le dit.

### L'univers — inchangé, et le biais avec

Les douze mêmes valeurs du CAC 40, dans le même ordre, sans aucune substitution :

| Ticker | Société | Secteur |
|---|---|---|
| `AIR.PA` | Airbus | aéronautique |
| `MC.PA` | LVMH | luxe |
| `OR.PA` | L'Oréal | cosmétiques |
| `SAN.PA` | Sanofi | santé |
| `BNP.PA` | BNP Paribas | banque |
| `TTE.PA` | TotalEnergies | énergie |
| `SU.PA` | Schneider Electric | équipement électrique |
| `AI.PA` | Air Liquide | gaz industriels |
| `DG.PA` | Vinci | concessions et construction |
| `CAP.PA` | Capgemini | services numériques |
| `RI.PA` | Pernod Ricard | spiritueux |
| `ORA.PA` | Orange | télécommunications |

> ⚠️ **Le biais du survivant est entier, et il est ici aggravé.** Ces douze
> sociétés ont été choisies en 2022 parmi celles qui appartenaient alors au
> CAC 40 ; les retrouver au CAC 40 en 2025 n'a donc rien d'un hasard. Garder le
> même univers permet de comparer les deux expériences terme à terme ; le prix
> à payer est que l'univers a survécu trois ans de plus. Le biais joue en faveur
> de l'expérience, il n'est pas corrigé, il est signalé.

### Les trois fenêtres

Une expérience qui mesure des taux a besoin de plus de dates que le portefeuille
n'en traverse. Les trois fenêtres sont déclarées avant, et elles ne se recouvrent
pas de la même façon :

| Fenêtre | Dates de décision | Ce qu'elle sert |
|---|---|---|
| **Étalonnage** | les 24 fins de mois de 2022-12 à 2024-11 | mesurer les **poids effectifs** du score et publier les taux de veto **avant** la première séance de 2025 |
| **Narrée et investie** | les 12 fins de mois de 2024-12 à 2025-11 | le portefeuille, les douze journaux, le bilan |
| **Audit** | les 36 fins de mois de 2022-12 à 2025-11 | les taux de la piste T1 : vetos, survie du canal, dépouillement des thèses |

> 🔑 **La fenêtre d'étalonnage est entièrement antérieure au 2 janvier 2025.**
> C'est ce qui autorise à en publier les résultats dans ce protocole sans
> enfreindre l'interdiction du regard en avant. La fenêtre d'audit, elle,
> englobe l'année narrée : ses chiffres sont des **mesures postérieures**,
> publiées au bilan, et aucune décision ne s'y appuie.

Les séries de cours commencent le **2021-01-04**, deux ans avant la première
décision : le momentum 12-1 exige 253 séances d'historique, le critère de
tendance longue en exige 120.

### Le calendrier — la cadence fait toujours partie de la règle

Inchangé, et pour la même raison :
[le module 5 du cours de trading](../../../raw/concept/semestre4/trading/05-la-cadence-fait-partie-de-la-regle.md)
montre qu'une même règle rend des résultats opposés selon qu'on l'évalue chaque
jour ou chaque mois.

- **Date de décision** : la **dernière séance du mois précédent**, à partir des
  seules séances jusqu'à cette date incluse.
- **Date d'exécution** : la **première séance du mois**, au cours d'**ouverture**.

L'expérience 2 ajoute une question à celle-là, qui est la piste **C4** : *l'objet
que la règle regarde survit-il d'une décision à la suivante ?* Voir plus bas.

---

## La règle dérivée, ce qu'elle emprunte et ce qu'elle écarte

C'est la piste **T3**. L'expérience 1 présentait son score comme une application
de
[la règle du module 3](../../../raw/concept/semestre4/trading/03-la-regle-ecrite-a-l-avance.md).
Il n'en était rien : elle en reprenait les cinq critères, mais en jetait les
quatre vetos et en inversait un seuil. La règle du module 3 rendait `ATTENTE`
aux **144 évaluations** de 2022 ; le score, lui, a déclenché 23 ordres.

> **Déclaration.** Le score employé ici n'est **pas** la règle du module 3. C'est
> une **règle dérivée**, qui emprunte ses cinq critères et son mécanisme de veto,
> et qui s'en écarte sur trois points, listés ci-dessous. Chacun de ces écarts
> est une décision de protocole, pas une lecture du module 3.

| | Règle du module 3 | Règle dérivée de l'expérience 2 |
|---|---|---|
| Sortie | trois verdicts : `ACHAT`, `VENTE`, `ATTENTE` | un **score entier** de `−7` à `+7`, et un **classement** |
| Décision | absolue, valeur par valeur | **relative** : on achète le rang 5 ou mieux, on vend au-delà du rang 7 |
| Vetos | quatre, bloquants | **les quatre, appliqués** — voir ci-dessous |
| Seuil de position | `ACHAT` sous 35 %, `VENTE` au-dessus de 65 % | `s3` **aligné** sur ces deux seuils (piste C3) |

### Les quatre vetos, désormais appliqués

L'expérience 1 les calculait et les jetait. Ici ils s'appliquent, avec une
convention déclarée :

| # | Veto | Déclenché quand |
|---|---|---|
| 1 | encadrement illisible | moins de 3 épisodes de contact d'un côté |
| 2 | canal se refermant | $\tau < 20$ séances |
| 3 | tendances contradictoires | critères 1 et 2 de signes opposés |
| 4 | historique trop court | moins de 120 séances |

> **Un veto interdit l'entrée ; il ne force pas la sortie.** Un veto dit *« la
> figure n'est pas lisible »*, pas *« la position est mauvaise »*. Forcer une
> vente sur une illisibilité ferait payer un aller-retour pour un motif que la
> règle n'énonce pas. Cette asymétrie est une décision de protocole, déclarée
> ici, et elle est la seule.

**Un cinquième cas, qui n'est pas un veto** : il arrive que
`generer_graph_decision.py` sorte en **2**, son contrôle de non-traversée de
l'enveloppe convexe ayant échoué — la règle refuse alors de publier des critères
qu'elle sait faux. La ligne reste **vide** dans `criteres.csv`, avec le verdict
`ERREUR`, et le protocole la traite comme un veto : *une figure qu'on ne sait pas
calculer n'est pas une figure qu'on peut acheter*. Ces évaluations sont comptées
**à part** au bilan, et jamais rangées dans l'un des quatre vetos qu'elles n'ont
pas déclenchés.

Conséquence mécanique, à déclarer aussi : **le veto rend le portefeuille plus
lent**. Il ne peut que réduire le nombre d'achats, jamais l'augmenter. Si
l'expérience 2 passe moins d'ordres que l'expérience 1, ce n'est donc pas un
résultat — c'est la définition de ce qu'on a ajouté.

### Les poids effectifs du score, mesurés sur la fenêtre d'étalonnage

Un score à cinq composantes n'a pas cinq axes. La part de variance que chaque
composante explique — $\operatorname{Cov}(s_i, \text{score}) /
\operatorname{Var}(\text{score})$, dont la somme fait exactement 1 — se mesure
sur les 288 évaluations de la fenêtre d'étalonnage, **avant** la première séance
de 2025 :

| Composante | Part de la variance du score |
|---|---|
| `s1` — tendance longue `TEND_120` | **51,0 %** |
| `s2` — tendance courte `TEND_20` | 5,9 % |
| `s3` — position dans l'encadrement | 8,3 % |
| `s4` — momentum 12-1 | **34,7 %** |
| `s5` — alpha annualisé, IC95 | **0,0 %** |

**Deux composantes font 86 % du score, et une cinquième n'en fait rien.** `s5`
vaut `0` aux **287 évaluations calculables** de l'étalonnage — la 288ᵉ est celle
que la règle n'a pas su produire : l'IC95 de l'alpha d'une valeur contient zéro
à chaque fois, ce que le dépôt répète partout.

La composante est conservée telle quelle — la retirer après l'avoir vue inutile
serait un ajustement rétrospectif —, mais on sait désormais, **avant** la
première séance, que le score n'a que deux axes et demi. Le bilan dira si elle
s'est réveillée en 2025.

### Le score, en cinq composantes

| | Critère | Valeurs possibles |
|---|---|---|
| `s1` | tendance longue `TEND_120` | `+2` / `0` / `−2` |
| `s2` | tendance courte `TEND_20` | `+1` / `0` / `−1` |
| `s3` | position dans l'encadrement actif | **`+1` si < 35 %**, `0` de 35 à 65 %, **`−1` si > 65 %** |
| `s4` | momentum 12-1 | `+2` si > +10 %, `+1` si 0 à +10 %, `−1` si −10 à 0 %, `−2` si < −10 % |
| `s5` | alpha annualisé contre la référence | `+1` si l'IC95 est entièrement positif, `−1` s'il est entièrement négatif, `0` sinon |

**Score = s1 + s2 + s3 + s4 + s5.** Départage : score, puis momentum, puis ordre
alphabétique — le classement reste déterministe.

Chaque composante est lue dans la sortie de
[`python/generer_graph_decision.py`](../../../../python/generer_graph_decision.md),
jamais réimplémentée.

---

## Le sens de `s3` aligné, et son portefeuille fantôme

C'est la piste **C3**, et c'est la seule correction qui change une décision.

L'expérience 1 donnait `s3 = +1` à une valeur **haute** dans son canal, quand la
règle qu'elle citait n'achète qu'en dessous de 35 % de la hauteur. Conséquence
mesurée par l'agent `chartiste` : **12 achats sur 14** ont eu lieu dans la zone
où la règle citée interdit d'acheter, et **4 ventes sur 9** sur un support.

> **Déclaration.** `s3` est aligné sur les seuils du module 3 : `+1` en dessous
> de 35 %, `−1` au-dessus de 65 %. C'est une **inversion** par rapport à
> l'expérience 1, et elle est déclarée avant la première séance.

Cette inversion n'est pas une contradiction avec `s4`, qui reste un critère de
momentum : la règle du module 3 achète **une valeur en tendance haussière sur un
repli** — critères 1 et 2 positifs, position basse. `s3` et `s4` tirent en sens
opposés par construction, et c'est le dessin de la règle citée, pas un défaut.

### Le portefeuille fantôme

Déclarer une inversion ne la mesure pas. L'expérience 2 fait donc tourner en
parallèle un **portefeuille fantôme**, identique en tout point sauf `s3`, qui y
garde le sens de l'expérience 1 (`+1` si ≥ 50 %, `0` de 20 à 50 %, `−1` si
< 20 %).

- Il est déclaré **avant** la première séance, avec son sens.
- Il n'engage aucun euro : c'est une comptabilité parallèle, publiée au bilan.
- Son intérêt est statistique : les deux portefeuilles partagent l'univers, les
  dates, les coûts et la plus grande part de leur exposition. **L'écart apparié
  entre deux séries fortement corrélées a une erreur-type bien plus faible que
  l'alpha de chacune** — c'est la seule comparaison de cette expérience qui ait
  une chance d'être lisible sur douze mois. Son erreur-type sera publiée au
  bilan, mesurée, et non promise ici.

> Ce que le fantôme **ne** dira **pas** : quel sens est le bon. Un an reste un
> an. Il dira de combien les deux sens divergent, et à quelle vitesse — ce qui
> permet de dimensionner l'expérience qui, elle, pourrait trancher.

---

## La durée de vie de l'encadrement contre la cadence

C'est la piste **C4**. Le score lit une position dans un canal ; encore faut-il
que le canal existe encore au moment où l'on relit. Trois quantités sont donc
publiées à chaque décision, pour les douze valeurs :

1. **τ, la date de péremption du canal**, en séances — le nombre de séances au
   bout duquel support et résistance se croisent. À comparer aux **≈ 21 séances**
   qui séparent deux décisions. Un canal dont $\tau < 21$ n'existera plus quand
   on relira sa position.
2. **La survie de l'encadrement prolongé** : à la décision suivante, la clôture
   est-elle restée entre le support et la résistance **prolongés de leurs propres
   pentes** ? C'est exactement la thèse `CANAL` du registre ci-dessous, et son
   taux de démenti est le taux de mortalité de l'encadrement à un mois.
3. **La stabilité rétrospective** : le score et `s3` recalculés à **d−1** et
   **d−2 séances**. Si `s3` bascule quand on décale la décision d'une séance,
   la composante mesure du bruit de calendrier, pas une configuration.

> Le décalage se fait **vers l'arrière**, jamais vers l'avant. Recalculer à
> d+1 supposerait de connaître une séance postérieure à la décision, ce que le
> dépôt interdit partout, y compris pour un diagnostic.

L'expérience 1 donnait, sur ses 144 évaluations : `s3` bascule **20 fois** quand
la décision est décalée d'une séance, et **88 clôtures sur 132** sortent de
l'encadrement prolongé du mois précédent. L'expérience 2 mesure les mêmes
quantités sur 432 et 420 observations, avec les incertitudes du tableau de
dimensionnement.

---

## Le registre des thèses réfutables

C'est la piste **S4**, et c'est la partie la plus proche de Soros. Son journal
de 1985 ne vaut pas par ses gains : il vaut parce que chaque thèse y est écrite
**avant**, dans des termes qui permettent de constater qu'elle était fausse.

L'expérience 1 a produit 144 notes chartistes contenant autant de propositions
réfutables, et n'en a dépouillé aucune.

### Les deux thèses, engendrées mécaniquement

À chaque date de décision $d$, pour chacune des douze valeurs, le moteur écrit
**deux thèses**. Elles ne sont pas rédigées à la main : elles se déduisent de
l'état constaté à $d$, par les règles ci-dessous, déclarées avant.

**Thèse `CANAL`** — la figure tient.

> À la prochaine date de décision $d'$, distante de $k$ séances, la clôture
> restera comprise entre
> $\text{support}(d) + k \times \text{pente}_{\text{support}}$ et
> $\text{résistance}(d) + k \times \text{pente}_{\text{résistance}}$.

Si le canal converge assez pour se croiser avant $d'$ — c'est-à-dire si
$\tau < k$ — les deux bornes s'inversent et la thèse est **mécaniquement
démentie**. Ce n'est pas un défaut du dépouillement : c'est précisément ce que
la piste C4 demande de compter.

**Thèse `REFLEXIVE`** — la phase, au sens de Soros.

La phase se déduit de trois quantités constatées à $d$, et d'elles seules :

| Phase déclarée | Condition à $d$ | Clause réfutable sur $[d, d']$ |
|---|---|---|
| `AUTO-RENFORCEMENT` | `TEND_120` = +1, `TEND_20` = +1, position > 65 % | l'écart de rendement contre `TR12` sera **positif ou nul** |
| `RETOURNEMENT` | `TEND_120` = −1, `TEND_20` = −1, position < 35 % | l'écart de rendement contre `TR12` sera **négatif ou nul** |
| `AUCUNE SÉQUENCE` | tous les autres cas | l'écart de rendement contre `TR12` restera **dans ± 5 points** |

Les trois clauses ont la même forme — *l'écart reste entre une borne basse et une
borne haute*, l'une des deux pouvant être infinie — ce qui permet de les
dépouiller toutes par le même test, sans cas particulier à écrire.

Le troisième cas est le défaut de charte de l'agent
[`sorosien`](../../../../.claude/agents/sorosien.md) — *« aucune séquence
réflexive identifiable »* — et il est ici rendu **réfutable** : dire qu'il ne se
passe rien, c'est prédire que l'écart restera petit, et cela se dément.

### Le dépouillement

À chaque date de décision, le moteur **dépouille les thèses du mois précédent
avant d'écrire celles du mois courant**, et publie le verdict —
`CONFIRMÉE`, `DÉMENTIE`, ou `NON TRANCHÉE` quand la donnée manque. Le registre
complet est dans [`theses.csv`](theses.csv) ; chaque journal mensuel en porte le
dépouillement ; le bilan en publie les taux.

> Aucune thèse n'est rédigée après coup, aucune n'est retirée, et le
> dépouillement d'un mois est écrit dans le fichier du mois suivant — pas dans
> celui où la thèse a été formulée.

---

## Les règles d'entrée et de sortie

- **Entrée** : classé au **rang 5 ou mieux**, score **strictement positif**,
  **aucun veto déclenché**, pas déjà détenu, et une place libre parmi les cinq.
- **Sortie** : rang **au-delà de 7**, ou score **≤ −3**. Les vetos n'y entrent
  pas.
- **Hystérésis** : on entre à 5, on sort à 7. Sans cet écart, une valeur qui
  oscille entre les rangs 5 et 6 paierait un aller-retour chaque mois — 0,53 %,
  soit plus de 6 % par an pour une seule ligne indécise.
- **Aucun rebalancement** : on n'achète que les entrées, on ne vend que les
  sorties. Les poids dérivent, et c'est voulu.
- **Répartition** : les espèces disponibles après les ventes sont divisées par
  le **nombre de créneaux libres**, et non par le nombre de valeurs qui entrent.
- **Titres entiers.** Le reliquat retourne aux espèces.

> ⚠️ **La répartition change par rapport à l'expérience 1, et c'est une décision
> de catégorie B — déclarée comme telle.** L'expérience 1 divisait par le nombre
> de valeurs entrantes ; avec les vetos, il arrive qu'une seule valeur soit
> achetable, et cette règle lui aurait donné **100 % du portefeuille**, ce qui
> vide de son sens le plafond de cinq lignes.
>
> Honnêteté du procédé : ce cas ne m'est pas apparu en lisant le protocole, mais
> à un premier essai du moteur, qui a mis tout le portefeuille sur une seule
> ligne pendant neuf mois. C'est donc une correction **suggérée par un
> résultat**, au sens exact de la catégorie B de
> [la revue](../experience_1/review.md) — recevable parce qu'elle est nommée
> comme telle, et parce que la règle écartée est publiée à côté de la règle
> retenue, ci-dessous.

### Les deux variantes déclarées

Deux choix de règle que l'expérience aurait pu faire autrement sont **calculés en
parallèle et publiés au bilan**, sans jamais engager un euro :

| Variante | Ce qu'elle change |
|---|---|
| `--repartition candidats` | divise les espèces par le nombre d'entrants, comme l'expérience 1 |
| `--sans-veto` | calcule les quatre vetos et les jette, comme l'expérience 1 |

Elles ne décident rien. Elles chiffrent ce que coûte ou rapporte chacun des deux
écarts au protocole de 2022, ce qui est la seule façon de ne pas avoir à en
débattre.

## Les coûts, appliqués à chaque ordre

Barème inchangé, de
[`python/couts_transaction.py`](../../../../python/couts_transaction.md) :

| | Achat | Vente |
|---|---|---|
| Courtage | 0,100 % | 0,100 % |
| Demi-spread | 0,015 % | 0,015 % |
| Taxe sur les transactions financières | 0,300 % | — |
| **Total** | **0,415 %** | **0,115 %** |

Soit **0,530 % l'aller-retour** — et **0,230 %** pour Airbus, immatriculée aux
Pays-Bas et donc hors du champ de la TTF française.

## La référence — `TR12`, et pourquoi ce n'est pas le CAC 40

Inchangée : **`TR12`**, indice **en rendement total** construit par
[`python/construire_indice_total.py`](../../../../python/construire_indice_total.md)
sur les douze mêmes valeurs, équipondérées.

`Close` est ajustée des dividendes, `^FCHI` ne l'est pas ; comparer les deux
fabrique de l'alpha à partir de rien. Sur la seule année 2022, l'écart de
convention valait **6,36 points** — davantage que l'alpha mesuré. Le bilan de
2025 republie les trois conventions côte à côte.

---

## Ce que contient chaque markdown mensuel

Douze fichiers, [`rapports/2025-01.md`](rapports/2025-01.md) à
[`rapports/2025-12.md`](rapports/2025-12.md), bâtis sur le même plan qu'en 2022,
plus deux sections nouvelles :

1. **Les actualités du mois précédent** — le contexte tel qu'il était connu à la
   date de décision.
2. **Le dépouillement des thèses du mois précédent** — *(nouveau, piste S4)* les
   vingt-quatre thèses écrites le mois d'avant, avec leur verdict.
3. **L'exposition héritée** — date d'achat, plus ou moins-value, alpha du mois,
   alpha global.
4. **La valeur du portefeuille** rapportée au 2 janvier 2025, base 100, et le
   **graphique** de l'évolution.
5. **L'étude chartiste** — une note de perspective de cinq lignes au plus par
   société, sans aucune séance postérieure à la date de décision.
6. **Le classement** des douze valeurs, avec le détail des cinq composantes,
   **les vetos déclenchés** et **τ** — *(nouveau, pistes T3 et C4)*.
7. **Les ordres exécutés**, chacun avec son motif chiffré.
8. **La lecture du mois** — un paragraphe **entièrement calculé** : meilleure et
   moins bonne contribution, frais, écart à `TR12`, et taux de confirmation des
   thèses dépouillées. Aucun récit rédigé après coup.
9. **Les thèses du mois** — les vingt-quatre énoncés qui seront dépouillés le
   mois suivant.

> Le graphique du fichier de mars s'arrête fin mars, et le classement de mars a
> été calculé fin février. Le premier **rend compte**, le second **décide** :
> aucune décision ne s'appuie sur une séance postérieure à sa date de décision,
> échelles de graphique comprises.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| [`bilan-2025.md`](bilan-2025.md) | **le bilan**, entièrement calculé, audits compris |
| `rapports/2025-01.md` … `2025-12.md` | les douze journaux mensuels |
| [`journal.py`](journal.py) | le moteur : classement, vetos, ordres, thèses, comptabilité, graphiques |
| [`journal.md`](journal.md) | son miroir d'exécution, au sens de la règle du dépôt |
| [`actualites.md`](actualites.md) | le contexte macroéconomique de chaque mois, rédigé à la main |
| [`chartiste.md`](chartiste.md) | les 144 notes de perspective, rédigées par l'agent `chartiste` |
| `criteres.csv` | les évaluations de la règle : 432 décisions + 288 décalages |
| `classement.csv` | le classement et les cinq composantes, aux 36 dates d'audit |
| `theses.csv` | les 864 thèses et leur dépouillement |
| `ordres.csv` | les ordres de l'année, avec prix, frais et motif |
| `portefeuille.csv` | la valeur quotidienne du portefeuille réel |
| `fantome.csv` | la valeur quotidienne du portefeuille fantôme (piste C3) |
| `graphiques/` | les douze SVG, janvier → fin du mois |

### Reproduire l'expérience

```bash
# 1. les series, avec deux ans d'amorce avant la premiere decision
for t in AIR.PA MC.PA OR.PA SAN.PA BNP.PA TTE.PA SU.PA AI.PA DG.PA CAP.PA RI.PA ORA.PA; do
  python python/import_societe.py "$t" --debut 2021-01-04 --fin 2026-01-02
done
python python/import_societe.py "^FCHI" --debut 2021-01-04 --fin 2026-01-02

# 2. la reference en rendement total
python python/construire_indice_total.py AIR.PA MC.PA OR.PA SAN.PA BNP.PA TTE.PA \
    SU.PA AI.PA DG.PA CAP.PA RI.PA ORA.PA \
    --debut 2021-01-04 --fin 2025-12-31 --nom TR12

# 3. le journal — la collecte lance 720 evaluations en sous-processus paralleles
python docs/done/experimentation/experience_2/journal.py --collecter --taches 10
python docs/done/experimentation/experience_2/journal.py --markdown
python docs/done/experimentation/experience_2/journal.py --mois 2025-03
```

Le moteur est déterministe : relancé, il réécrit exactement les mêmes fichiers.

---

## Ce que l'expérience 2 ne fait toujours pas

- **Aucun levier, aucune couverture.** Le
  [module 4 du cours de finance](../../../raw/concept/semestre4/finance/04-levier-optimal-et-drag.md)
  montre que le levier optimal dépend d'un rendement espéré qu'on ne sait pas
  mesurer. Le tableau de dimensionnement ci-dessus le redit dans les termes de
  cette expérience : douze mois ne donnent pas $\mu$ à ± 16 points près.
- **Aucun ordre stop.** Ce serait une variante de plus, et rien ici ne permet
  de trancher entre variantes.
- **Aucun fondamental.** Le score reste entièrement chartiste. Les ratios
  point-in-time du dépôt
  ([`reconstituer_fondamentaux.py`](../../../../python/reconstituer_fondamentaux.md))
  feraient une expérience 3 légitime — et le tableau de dimensionnement dit
  d'avance ce qu'elle pourrait conclure.
- **Aucune prédiction de cours.** Les thèses du registre portent sur des écarts
  relatifs et sur la tenue d'une figure, jamais sur un niveau de cours à venir.
- **Aucun conseil en investissement.** C'est la sortie d'une règle, consignée.

---

## Pour aller plus loin

- [L'expérience 1](../experience_1/README.md) et [sa revue](../experience_1/review.md) — d'où viennent les cinq corrections
- [`docs/raw/planning.md`](../../../raw/planning.md) — le parcours complet
- [Semestre 4 · trading](../../../raw/concept/semestre4/trading/README.md) — la règle et ses pièges
- [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md) — pourquoi l'alpha se mesure si mal
