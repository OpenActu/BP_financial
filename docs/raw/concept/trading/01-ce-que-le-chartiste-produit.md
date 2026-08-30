# Module 1 — Ce que le chartiste produit

**Prérequis :** les [cours canal](../canal/README.md) et [encadrement](../encadrement/README.md), au moins leurs README.
**Ce qu'on établit ici :** l'inventaire exhaustif des objets disponibles avant toute décision, chacun rattaché au module qui le définit, et le tri entre ceux qui portent une incertitude et ceux qui n'en portent pas.

---

## 1.1 — Dix objets, pas un de plus

Une décision ne peut s'appuyer que sur ce qui a été construit. L'agent
[`chartiste`](../../../../.claude/agents/chartiste.md) et le script
[`import_societe.py`](../../../../python/import_societe.md) produisent, ensemble,
exactement dix objets. Les voici, avec leur définition d'origine :

| # | Objet | Ce que c'est | Défini dans |
|---|---|---|---|
| A | **Droite ajustée** $f(t) = v_0 + r\,t$ | la tendance des moindres carrés sur la fenêtre | [modele 07](../modele/07-droite-ajustee.md) |
| B | **`VAL_n`** | $f(n)$, la droite évaluée à la séance courante | [miroir § 4](../../../../python/import_societe.md) |
| C | **`T_n`, `P_n`, `TEND_n`** | test de Student de $H_0 : r = 0$, verdict signé | [modele 08](../modele/08-test-de-tendance.md) |
| D | **Canal de régression** | $f(t) + \min \hat e$ … $f(t) + \max\hat e$, ou $f(t)\pm k s$ | [canal 01](../canal/01-du-point-a-la-bande.md), [canal 02](../canal/02-les-trois-largeurs.md) |
| E | **Bandes de confiance et de prédiction** | les deux sabliers, d'épaisseur $\propto\sqrt{h_{ii}}$ et $\sqrt{1+h_{ii}}$ | [canal 03](../canal/03-epaisseur-variable-et-levier.md) |
| F | **Sorties de canal** | date, ampleur en $s$, persistance, volume | [canal 04](../canal/04-sorties-de-canal.md) |
| G | **Support et résistance convexes** | arêtes des chaînes inférieure et supérieure de l'enveloppe | [encadrement 01](../encadrement/01-la-droite-qui-ne-coupe-rien.md) |
| H | **Portée et épisodes de contact** | les deux nombres sans lesquels une droite n'est qu'un trait | [encadrement 02](../encadrement/02-portee-et-episodes-de-contact.md) |
| I | **Canal actif** | la paire support/résistance sur une fenêtre **ancrée à droite** | [encadrement 03](../encadrement/03-segmenter-un-historique-long.md) |
| J | **Position, largeur, $\tau$** | les lectures sans dimension du canal actif | [encadrement 04](../encadrement/04-lire-l-encadrement.md) |

À quoi s'ajoutent, hors géométrie, les deux objets du contexte de marché :

| # | Objet | Ce que c'est | Défini dans |
|---|---|---|---|
| K | **$\beta$ et son test contre 1** | la sensibilité au marché | [alpha 02](../alpha/02-le-calcul-et-ses-erreurs-types.md) |
| L | **$\alpha$ et son IC95** | ce qui reste après le marché, **avec** son intervalle | [alpha 02](../alpha/02-le-calcul-et-ses-erreurs-types.md), [alpha 03](../alpha/03-l-horizon-necessaire.md) |

## 1.2 — Le tri qui compte : qui porte une incertitude ?

C'est la partition la plus utile de la liste, et la moins souvent faite. Certains
de ces objets sont des **estimateurs**, adossés à un modèle probabiliste : on peut
leur attacher une erreur type, un intervalle, une $p$-valeur. Les autres sont des
**constructions géométriques exactes** : elles ne se trompent pas, et pour cette
raison même elles ne disent rien sur ce qui n'a pas été observé.

| Objet | Statut | Incertitude disponible |
|---|---|---|
| A, B — droite ajustée, `VAL_n` | estimateur | $\operatorname{SE}(r)$, bandes de confiance ([canal 03](../canal/03-epaisseur-variable-et-levier.md)) |
| C — `TEND_n` | test | $p$-valeur exacte sous $H_0$, sous réserve d'i.i.d. |
| D, E — canaux de régression | estimateur | oui, et c'est tout leur intérêt |
| F — sorties | test | on sait **combien** en attendre sous $H_0$ ([canal 04](../canal/04-sorties-de-canal.md)) |
| G, H, I, J — encadrement convexe | **géométrie exacte** | **aucune** — il n'y a pas de $H_0$ ([encadrement 04 § 4.3](../encadrement/04-lire-l-encadrement.md)) |
| K — $\beta$ | estimateur | $\operatorname{SE}(\beta)$, et il est **précis** |
| L — $\alpha$ | estimateur | $\operatorname{SE}(\alpha)$, et il est **désespérément large** |

> 🔑 **Un encadrement convexe ne se teste pas.** L'enveloppe convexe est un objet
> déterministe : la droite passe par des points, un point c'est tout. Aucune loi
> ne dit combien de « franchissements » attendre par hasard, contrairement aux
> sorties de canal de régression. C'est pourquoi le
> [module 3](03-la-regle-ecrite-a-l-avance.md) ne fait jamais reposer un verdict
> sur la seule géométrie : il l'accompagne toujours d'au moins un objet testé.

## 1.3 — Les trois nombres qui accompagnent chaque droite

Le [cours encadrement](../encadrement/02-portee-et-episodes-de-contact.md) l'énonce
comme une règle de publication ; ici c'est une **condition d'admissibilité** :

$$\text{une droite} = (\text{pente},\ \text{portée},\ \text{épisodes de contact})$$

Une droite dont l'un de ces trois nombres manque ne peut pas entrer dans une
règle de décision, parce qu'on ne peut pas écrire de seuil dessus.

**Illustration sur le fil rouge.** Fenêtre active d'Airbus, les 120 dernières
séances au 31 décembre 2020 (2020-07-16 → 2020-12-31). Les arêtes de la chaîne
supérieure, telles que le balayage de Andrew les produit :

| Arête (résistance) | Portée | Pente |
|---|---|---|
| 2020-07-16 → 2020-08-11 | 18 séances | $+0{,}3476$ €/séance |
| **2020-08-11 → 2020-12-04** | **83 séances** | $+0{,}2306$ |
| 2020-12-04 → 2020-12-09 | 3 séances | $-0{,}1651$ |
| 2020-12-09 → 2020-12-29 | 13 séances | $-0{,}2159$ |
| 2020-12-29 → 2020-12-30 | 1 séance | $-0{,}4220$ |
| **2020-12-30 → 2020-12-31** | **1 séance** | $-1{,}5321$ |

La dernière arête, celle qui atteint le bord droit, enjambe **une séance** et
donne une pente de $-1{,}53$ €/séance, soit $-1{,}9\,\%$ par jour. Extrapolée sur
un mois, elle annonce un titre à $50$ €. C'est le
[piège de la dernière arête](../encadrement/02-portee-et-episodes-de-contact.md#21--la-portée-et-le-piège-de-la-dernière-arête)
dans sa version la plus caricaturale, et la règle de portée minimale
($n/4 = 30$ séances) l'élimine mécaniquement au profit de l'arête à 83 séances.

Même exercice sur la chaîne inférieure : la dernière arête (2020-12-21 →
2020-12-31, 7 séances, $+0{,}9214$ €/séance) est écartée au profit de celle du
2020-10-29 → 2020-12-21, de portée **37**.

> ⚠️ **La règle de portée doit être fixée avant de voir les arêtes.** Ici, sans
> elle, on aurait obtenu un support à $+0{,}92$ et une résistance à $-1{,}53$ :
> un biseau qui se referme en trois séances, figure spectaculaire et entièrement
> fabriquée par huit jours de cotation.

## 1.4 — Ce que l'inventaire ne contient pas

Aussi important que la liste : ce qui n'y figure pas et ne peut donc entrer dans
aucune règle construite depuis ce dépôt.

| Absent | Pourquoi |
|---|---|
| PER, P/B, VE/EBITDA, rendement du FCF | les CSV ne contiennent que de l'OHLCV — aucun fondamental |
| ROE, marge, dette/EBITDA | idem |
| Capitalisation, flottant | il faudrait le nombre d'actions |
| Carnet d'ordres, spread, profondeur | absent, donc **aucun coût de transaction modélisé** |
| Consensus, révisions, positionnement | absent |

> ⚠️ **Ne jamais fabriquer un chiffre fondamental.** Si une règle en demande un,
> la règle n'est pas applicable ici — et c'est la seule réponse honnête.

---

⬅️ [README du cours](README.md) ·
➡️ [Module 2 — D'un objet à un critère](02-d-un-objet-a-un-critere.md)
