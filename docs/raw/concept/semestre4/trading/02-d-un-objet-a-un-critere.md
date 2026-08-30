# Module 2 — D'un objet à un critère ⭐

**Prérequis :** [module 1](01-ce-que-le-chartiste-produit.md).
**Ce qu'on établit ici :** les trois exigences qu'un objet graphique doit satisfaire pour entrer dans une règle, la généalogie des cinq critères retenus, et pourquoi les autres objets en sont écartés.

---

Un objet graphique n'est pas un critère. `VAL_120 = 81{,}61` € est un objet ;
« la tendance à 120 séances est haussière au seuil de 5 % » est un critère. Le
passage de l'un à l'autre suppose trois opérations, et chacune peut se rater.

## 2.1 — Les trois exigences

**a. Sans dimension.** Un critère exprimé en euros n'est comparable ni d'un titre
à l'autre, ni d'une époque à l'autre du même titre. « Le cours est à 2,38 € de son
support » ne veut rien dire ; « le cours est à $2{,}9\,\%$ de son support » se
compare. C'est exactement l'argument du
[§ 4.1 du cours encadrement](../../semestre3/encadrement/04-lire-l-encadrement.md) : *la
position dans le canal est la seule des quatre grandeurs qui soit sans dimension.*

**b. Daté.** Un critère se cite avec la séance à laquelle il a été mesuré et la
fenêtre sur laquelle il a été calculé. Un canal se **repeint** à chaque nouvelle
séance ([canal 05](../../semestre3/canal/05-canal-glissant.md)) ; un critère non daté est
invérifiable.

**c. Borné, ou muni d'un seuil publiable.** Il faut pouvoir écrire une inégalité
dessus **avant** de connaître sa valeur. `TEND_n` vaut $-1$, $0$ ou $+1$ : c'est
le cas idéal. La position dans le canal vit dans $[0, 1]$ hors franchissement.
L'alpha, lui, n'est pas borné — d'où le traitement particulier du § 2.5.

## 2.2 — La généalogie des cinq critères

| # | Critère | Objet source (module 1) | Défini dans | Sans dimension ? |
|---|---|---|---|---|
| 1 | **Tendance longue** `TEND_120` | C | [modele 08](../../semestre3/modele/08-test-de-tendance.md) | oui, ternaire |
| 2 | **Tendance courte** `TEND_20` | C | idem | oui, ternaire |
| 3 | **Position dans l'encadrement actif** | I, J | [encadrement 04](../../semestre3/encadrement/04-lire-l-encadrement.md) | oui, $[0,1]$ |
| 4 | **Alpha annualisé et son IC95** | L | [alpha 02](../alpha/02-le-calcul-et-ses-erreurs-types.md) | oui, %/an |
| 5 | **Momentum 12-1** | prix bruts | [ce module § 2.4](#24--le-momentum-12-1-et-le-trou-du-dernier-mois) | oui, % |

Deux critères de **tendance** (un long, un court), un critère de **position**, un
critère de **contexte de marché**, un critère de **persistance**. Aucun n'est
redondant avec un autre, et c'est le seul argument qui justifie leur présence :
ajouter un sixième critère fortement corrélé aux cinq premiers n'ajouterait pas
d'information, seulement une occasion de plus de bricoler les seuils
([module 3 § 3.5](03-la-regle-ecrite-a-l-avance.md)).

## 2.3 — La position : deux canaux, deux réponses

Piège majeur, et il est spécifique à ce dépôt : le chartiste produit **deux**
encadrements, et ils ne donnent pas la même position.

Sur Airbus, fenêtre active de 120 séances (2020-07-16 → 2020-12-31), clôture
$82{,}37$ € :

| | Support | Résistance | Largeur | **Position** |
|---|---|---|---|---|
| **Encadrement convexe** ([encadrement 01](../../semestre3/encadrement/01-la-droite-qui-ne-coupe-rien.md)) | 79,99 € | 93,18 € | 13,19 € — 16,0 % | **18,0 %** |
| Canal de régression ([canal 02](../../semestre3/canal/02-les-trois-largeurs.md)) | 66,23 € | 92,41 € | 26,18 € — 31,8 % | 61,6 % |

**Même titre, même jour, même fenêtre : 18 % ou 62 %.** L'écart n'est pas une
erreur, c'est la définition des deux objets : l'enveloppe convexe s'appuie sur les
extrêmes de séance (`High`, `Low`) et suit le rebond récent ; le canal de
régression enveloppe les **résidus** autour d'une droite unique et porte encore la
mémoire du creux d'octobre à $54{,}73$ €.

> ⚠️ **Une règle doit nommer lequel des deux elle utilise, et ne jamais en
> changer.** La règle du [module 3](03-la-regle-ecrite-a-l-avance.md) utilise
> l'**encadrement convexe actif**, parce que c'est le seul dont les bornes sont
> des prix réellement atteints et dont on peut compter les épisodes de contact.
> Choisir le canal de régression serait tout aussi défendable — le choisir *après*
> avoir vu que 62 % arrange mieux ne le serait pas.

## 2.4 — Le momentum 12-1, et le trou du dernier mois

Le critère de persistance le plus documenté de la littérature factorielle :
rendement sur douze mois, **le dernier mois exclu**.

$$\text{mom}_{12\text{-}1}(t) = \frac{P_{t-21}}{P_{t-252}} - 1$$

en séances : 252 séances par an, 21 par mois. Le trou d'un mois n'est pas une
coquetterie — il neutralise l'effet de **retournement à court terme**, empiriquement
de signe opposé au momentum, qui polluerait la mesure.

**Sur Airbus au 31 décembre 2020**, dernière séance d'indice 513 :

| Fenêtre | Bornes | Clôtures | Rendement |
|---|---|---|---|
| 12-1 | 2020-01-08 → 2020-12-01 | 123,28 → 82,02 € | **$-33{,}47\,\%$** |
| Dernier mois exclu | 2020-12-01 → 2020-12-31 | 82,02 → 82,37 € | $+0{,}43\,\%$ |
| 12 mois pleins | 2020-01-08 → 2020-12-31 | 123,28 → 82,37 € | $-33{,}19\,\%$ |

Ici le trou ne change presque rien ($0{,}3$ point) parce que décembre 2020 fut
plat sur le titre. Ce n'est pas toujours le cas, et le principe reste : **le trou
se décide avant de constater qu'il est inutile.**

*Repère de comparaison :* le momentum 12-1 du CAC 40 sur la même fenêtre vaut
$-7{,}45\,\%$. Airbus a donc perdu 26 points de plus que son indice sur la période
de mesure du critère.

## 2.5 — L'alpha entre par sa borne, jamais par son signe

L'alpha est le seul des cinq critères dont **la valeur ponctuelle est inutilisable**.
Le [cours alpha](../alpha/03-l-horizon-necessaire.md) le démontre en une formule :

$$\operatorname{SE}(\alpha_{\text{an}}) = \frac{\sigma_\varepsilon}{\sqrt Y}$$

Sur le fil rouge — Airbus contre le CAC 40, 511 rendements quotidiens, $Y = 2{,}03$
ans, $\sigma_\varepsilon = 35{,}60\,\%$/an :

| | Valeur |
|---|---|
| $\alpha$ annualisé | $-0{,}29\,\%$ |
| $\operatorname{SE}(\alpha_{\text{an}})$ | $25{,}01\,\%$ |
| $t$ | $-0{,}012$, $p = 0{,}991$ |
| **IC95** | $[-49{,}44\ ;\ +48{,}85]\,\%$ |
| Plus petit alpha détectable $1{,}96\,\sigma_\varepsilon/\sqrt Y$ | $49{,}0\,\%$/an |

Un intervalle large de **98 points**. Dire « l'alpha est négatif » serait un
contresens : l'alpha est **indiscernable de zéro**, et il le resterait pour toute
valeur comprise entre $-49$ et $+49\,\%$ par an.

> 🔑 **D'où la seule forme utilisable du critère 4 : une condition sur une borne
> de l'intervalle, pas sur la valeur.** La règle du module 3 demande que la borne
> **haute** de l'IC soit $> 0$ pour autoriser un achat. C'est une condition
> volontairement faible : elle ne dit pas « le titre produit de l'alpha », elle dit
> « les données n'excluent pas un alpha positif ». Sur un historique de deux ans,
> presque aucune valeur ne la viole — et c'est précisément ce qu'il faut savoir.

Le bêta, lui, se mesure très bien sur les mêmes données :
$\beta = 1{,}6592$, $\operatorname{SE} = 0{,}0637$, IC95 $[1{,}534\ ;\ 1{,}784]$,
$t = +10{,}35$ contre 1 ($p = 7\cdot 10^{-23}$). **Airbus est sans ambiguïté plus
volatile que son indice.** Ce n'est pas un critère de décision de la règle, mais
c'est une information que tout verdict doit accompagner : le même verdict n'a pas
la même portée sur un titre de bêta $0{,}6$ et sur un titre de bêta $1{,}66$.

## 2.6 — Les objets écartés, et pourquoi

Publier ce qu'on n'a pas retenu fait partie de l'honnêteté de la règle.

| Objet écarté | Raison |
|---|---|
| E — bandes de prédiction | elles concernent la **prochaine observation** ; la règle ne prédit rien |
| F — sorties de canal | comptage utile en diagnostic, mais [6 sorties sur 10 sont du hasard](../../semestre3/canal/04-sorties-de-canal.md) sur 20 séances |
| K — $\beta$ | c'est une mesure de risque, pas un signal directionnel ; il qualifie le verdict, il ne le produit pas |
| Volatilité réalisée, écran « faible volatilité » | calculable, mais c'est un **autre** écran ; le mélanger reviendrait à tester deux règles |
| Volume | disponible, mais aucune règle publiée à l'avance dans ce dépôt ne s'en sert |

> ⚠️ **« Calculable » n'est pas « à mettre dans la règle ».** Chaque critère
> ajouté multiplie le nombre de règles possibles et donc la probabilité d'en
> trouver une qui marche sur le passé. Cinq critères et trois seuils, c'est déjà
> beaucoup.

---

⬅️ [Module 1 — Ce que le chartiste produit](01-ce-que-le-chartiste-produit.md) ·
➡️ [Module 3 — La règle écrite à l'avance](03-la-regle-ecrite-a-l-avance.md)
