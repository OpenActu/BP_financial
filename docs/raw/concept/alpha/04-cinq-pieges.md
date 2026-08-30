# Module 4 — Cinq pièges

**Prérequis :** modules 1 à 3.
**Ce qu'on établit ici :** cinq façons d'obtenir un alpha faux sans commettre d'erreur de calcul.

---

Aucun de ces pièges ne se voit dans les formules. Tous se voient dans les
données, à condition de les regarder.

## 4.1 — Le drag de volatilité

**Le piège.** Conclure d'un excès de rendement moyen positif que la valeur a
battu son indice.

**Pourquoi il mord.** La moyenne arithmétique des rendements et la performance
réellement réalisée divergent d'autant plus que la volatilité est forte. Pour un
rendement composé, ce qui compte est la moyenne **géométrique**, inférieure à
l'arithmétique d'environ $\sigma^2/2$ — c'est l'inégalité de Jensen, démontrée au
[module 5 du cours convexité](../analyse/convexite/05-jensen-probabiliste.md) et
exploitée au [module 4 du cours finance](../finance/04-levier-optimal-et-drag.md).

**En grandeur nature.** Airbus contre le CAC 40, 2020-2023 :

| | Valeur |
|---|---|
| Excès de rendement **arithmétique** annualisé | $+4{,}11\,\%$ |
| Ratio d'information | $+0{,}128$ |
| Performance **cumulée** du titre | $+7{,}70\,\%$ |
| Performance **cumulée** de l'indice | $+24{,}86\,\%$ |

Le titre gagne en moyenne quotidienne et perd de 17 points en cumulé. L'écart
vient des volatilités : $45{,}0\,\%$ contre $21{,}9\,\%$, soit un drag
$\sigma^2/2$ de $10{,}1\,\%$ contre $2{,}4\,\%$ — près de 8 points par an de
différence, qui suffisent à retourner la conclusion.

> 🔑 **Un ratio d'information positif ne signifie pas qu'une valeur a battu son
> indice.** Publier toujours la performance cumulée à côté.

## 4.2 — L'indice nu contre l'indice de rendement total

**Le piège.** Comparer une série de cours **ajustée des dividendes** à un indice
qui ne l'est pas.

**Pourquoi il mord.** La colonne `Close` de `import_societe.py` vient de yfinance
et est ajustée des dividendes et des divisions du nominal : c'est une performance
*totale*, dividendes réinvestis. Or le CAC 40 est un indice de prix **nu** :
ses dividendes ne sont pas réintégrés. La version rendement total est un
indice distinct.

Comparer les deux attribue au titre un avantage égal au rendement du dividende de
l'indice, de l'ordre de 3 %/an sur le CAC 40 — un biais **systématiquement
favorable** à l'alpha mesuré, et qui n'a rien à voir avec le titre.

> ⚠️ Ce biais n'est pas corrigé dans les chiffres de ce cours. L'alpha d'Airbus
> y est donc surestimé d'environ 3 points par an — ce qui, l'intervalle de
> confiance faisant 58 points de large, ne change aucune conclusion, mais devrait
> être corrigé sur une comparaison qui prétendrait trancher.

**Comment s'en sortir.** Utiliser un indice de rendement total, ou retirer le
dividende du titre. Dans les deux cas : **dire lequel a été fait.**

## 4.3 — Le bêta n'est pas constant

**Le piège.** Estimer un $\beta$ unique sur quatre ans et le traiter comme une
propriété stable du titre.

**Pourquoi il mord.** Le bêta varie avec le régime de marché, et augmente
typiquement dans les crises — au moment précis où la diversification devrait
protéger. La période 2020-2023 contient un krach, une reprise et un cycle de
hausse des taux : supposer un $\beta$ constant sur cet ensemble est une
approximation forte.

Un $\beta$ instable contamine directement $\alpha$, puisque
$\alpha = E(r_i) - \beta E(r_m)$ : une erreur $\Delta\beta$ déplace l'alpha
annualisé de $-252\,\Delta\beta\,E(r_m)$, soit $-7{,}9\,\%$ par an par unité de
$\Delta\beta$ avec $E(r_m) = 0{,}0313\,\%$.

**Le contrôle minimal :** réestimer sur des sous-périodes et comparer. Si les
bêtas diffèrent nettement, l'alpha global n'a pas de sens.

## 4.4 — Des erreurs qui ne sont pas i.i.d.

**Le piège.** Prendre la $p$-valeur au pied de la lettre.

**Pourquoi il mord.** Toutes les erreurs types du
[module 2](02-le-calcul-et-ses-erreurs-types.md) reposent sur l'hypothèse de
l'[étape 8](../modele/08-test-de-tendance.md) : $\varepsilon_t$ i.i.d. gaussiennes.
Sur des rendements, deux violations sont systématiques :

- **La volatilité arrive en grappes.** Les grandes variations se suivent — c'est
  le fait stylisé le mieux établi des séries financières. Les résidus sont donc
  hétéroscédastiques, et $\operatorname{SE}(\alpha)$ est **sous-estimée**.
- **Les queues sont épaisses.** Les rendements ne sont pas gaussiens ; les
  extrêmes sont bien plus fréquents que la loi normale ne le prévoit
  ([statistique, § 13](../statistique/mathematique/13-portee-et-limites-du-tcl.md)).

L'effet va toujours dans le même sens : **les intervalles publiés sont trop
étroits et les $p$-valeurs trop petites.** Un intervalle déjà large de 58 points
l'est donc en réalité davantage.

**Les corrections usuelles :** écarts-types robustes de White ou HAC
(Newey–West), qui laissent $\alpha$ et $\beta$ inchangés et ne retouchent que
leurs erreurs types — exactement comme au § *Portée et limites* de l'étape 8.

## 4.5 — Tests multiples et biais du survivant

**Le piège.** Chercher l'alpha dans un univers de candidats et publier le
meilleur.

**Pourquoi il mord.** Avec un seuil à 5 %, tester 100 titres sans aucun alpha réel
en produit **5 significatifs** par pur hasard. C'est le même problème que les
sorties de canal du [module 4 du cours canal](../canal/04-sorties-de-canal.md),
transposé aux titres : on ne teste pas une hypothèse, on en teste $N$ et on retient
la meilleure.

S'y ajoute le **biais du survivant** : un univers constitué aujourd'hui ne
contient que les entreprises encore cotées. Les faillites et les radiations en
sont absentes, ce qui remonte mécaniquement la performance mesurée de l'ensemble.

**Ce qu'il faut faire :** annoncer le nombre de titres testés, corriger le seuil
en conséquence (Bonferroni, ou taux de fausses découvertes), et construire
l'univers **à la date de début** de l'étude, pas à celle de l'analyse.

## Récapitulatif

| Piège | Sens du biais sur l'alpha publié | Contrôle |
|---|---|---|
| Drag de volatilité | fait paraître bon un titre volatil perdant | publier la performance cumulée |
| Indice nu | **surestime** d'environ le rendement du dividende | indice de rendement total |
| Bêta instable | indéterminé, potentiellement large | réestimer par sous-période |
| Erreurs non i.i.d. | intervalles **trop étroits** | écarts-types HAC |
| Tests multiples | **surestime** le meilleur du lot | annoncer $N$, corriger le seuil |

Trois des cinq poussent dans le même sens : **l'alpha publié est plus souvent
trop beau que trop laid.**

---

⬅️ [Module 3 — L'horizon nécessaire](03-l-horizon-necessaire.md) ·
➡️ [Module 5 — Exemple chiffré : Airbus contre le CAC 40](05-exemple-chiffre-airbus.md)
