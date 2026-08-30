# Cours — L'alpha

La performance d'une valeur ne veut rien dire seule. `+7,7 %` sur quatre ans est
bon si l'indice a fait `0 %`, médiocre s'il a fait `+25 %`, et la comparaison
elle-même est trompeuse si la valeur a pris deux fois plus de risque pour y
arriver. **L'alpha est ce qui reste de la performance une fois retirée la part
attribuable au marché.**

Niveau bac+2. Prérequis : les [étapes 1 à 8 du modèle](../../modele.md#plan-de-la-preuve)
— l'alpha est **l'ordonnée à l'origine** de la régression qu'elles démontrent — et
le [module 3 du cours canal](../canal/03-epaisseur-variable-et-levier.md) pour son
erreur type.

## Pourquoi ce cours

Parce que l'alpha est la grandeur la plus citée de la gestion et l'une des moins
souvent accompagnée de son incertitude. Ce cours établit quatre choses :

| Ce qu'on croit | Ce qu'il en est | Module |
|---|---|---|
| « Ce fonds fait 2 % d'alpha. » | Il faudrait **216 ans** de données pour distinguer 2 % de zéro à volatilité résiduelle de 15 % | [03](03-l-horizon-necessaire.md) |
| « Prenons des données horaires, on aura plus de points. » | La précision de l'alpha **ne dépend pas** de la fréquence d'échantillonnage, seulement du nombre d'années | [03](03-l-horizon-necessaire.md) |
| « Son excès de rendement moyen est positif, donc elle bat l'indice. » | Faux dès que la volatilité diffère : Airbus affiche $+4{,}1\,\%$ d'excès arithmétique annuel et $+7{,}7\,\%$ contre $+24{,}9\,\%$ en cumulé | [04](04-cinq-pieges.md) |
| « L'alpha mesure le talent. » | Il mesure l'écart à **un modèle donné** : changez d'indice ou ajoutez un facteur, l'alpha change | [01](01-de-quoi-alpha-est-le-nom.md) |

## Le fil directeur

> 🔑 **Le bêta se mesure, l'alpha ne se mesure pas.** Sur la même régression, les
> mêmes données, le même nombre de points, $\beta$ ressort avec un $t$ de $12{,}5$
> et $\alpha$ avec un $t$ de $0{,}006$. Ce n'est pas un accident d'échantillon :
> c'est une propriété structurelle de la régression, que le
> [module 3](03-l-horizon-necessaire.md) chiffre en une formule.

## Plan

| # | Module | Ce qu'il établit |
|---|---|---|
| 1 | [De quoi alpha est le nom](01-de-quoi-alpha-est-le-nom.md) | Le modèle de marché ; $\alpha$ est l'ordonnée à l'origine de l'[étape 1](../modele/01-elimination-de-l-ordonnee.md) ; l'alpha dépend du modèle qui le définit |
| 2 | [Le calcul et ses erreurs types](02-le-calcul-et-ses-erreurs-types.md) | $\alpha$, $\beta$, leurs erreurs types par le levier ; deux tests — $\alpha$ contre 0, $\beta$ contre 1 ; annualisation |
| 3 | [L'horizon nécessaire](03-l-horizon-necessaire.md) ⭐ | $\operatorname{SE}(\alpha_{\text{an}}) = \sigma_\varepsilon/\sqrt{Y}$ ; l'invariance par la fréquence ; les tables d'horizon |
| 4 | [Cinq pièges](04-cinq-pieges.md) ⭐ | Drag de volatilité, indice nu contre rendement total, bêta instable, erreurs non i.i.d., tests multiples |
| 5 | [Exemple chiffré : Airbus contre le CAC 40](05-exemple-chiffre-airbus.md) | Les quatre modules sur 1026 rendements quotidiens |

## Le fil rouge chiffré

**Airbus contre le CAC 40, du 2 janvier 2020 au 29 décembre 2023**,
1027 séances communes donc 1026 rendements quotidiens. Les deux séries sont
produites par [`python/import_societe.py`](../../../../python/import_societe.md) :

```bash
python python/import_societe.py AIR.PA  --debut 2020-01-02 --fin 2023-12-30
python python/import_societe.py '^FCHI' --debut 2020-01-02 --fin 2023-12-30
```

| | Valeur | Lecture |
|---|---|---|
| $\beta$ | **1,5316** | $t = +12{,}46$ contre 1 — le titre est sans ambiguïté plus volatil que son indice |
| $\alpha$ annualisé | $-0{,}08\,\%$ | $t = -0{,}006$, $p = 0{,}996$ |
| **IC95 de $\alpha$** | $[-29{,}3\ ;\ +29{,}1]\,\%$ | 58 points de large : **aucune affirmation possible** |
| $R^2$ | 0,557 | le marché explique 56 % des mouvements du titre |
| Volatilité résiduelle | 29,98 %/an | c'est elle qui fixe la précision de $\alpha$ |

## Ce que ce cours alimente

L'agent [`trading`](../../../../.claude/agents/trading.md) applique ce cours : il
a l'obligation de publier l'IC de tout alpha qu'il calcule, et de conclure à un
alpha indiscernable de zéro plutôt que d'en commenter le signe quand l'intervalle
contient zéro.

---

➡️ Commencer par le [module 1 — De quoi alpha est le nom](01-de-quoi-alpha-est-le-nom.md) ·
🏠 [Sommaire du dépôt](../sommaire/README.md)
