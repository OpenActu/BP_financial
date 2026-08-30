# Module 4 — Lire l'encadrement

**Prérequis :** modules 1 à 3.
**Ce qu'on établit ici :** les quatre grandeurs qui se lisent sur un encadrement, la date à laquelle il cesse d'exister, et la frontière entre décrire et conseiller.

---

## 4.1 — Les quatre grandeurs

Un encadrement, une fois construit, se lit avec quatre nombres et pas davantage.
Appliqués au canal actif d'Airbus au 29 décembre 2023 :

| Grandeur                   | Formule                                                         | Valeur                                            |
| -------------------------- | --------------------------------------------------------------- | ------------------------------------------------- |
| **Bornes**                 | $d_{\text{sup}}(t)$, $d_{\text{inf}}(t)$                        | 136,33 € et 130,57 €                              |
| **Largeur relative**       | $(d_{\text{sup}}-d_{\text{inf}})/\text{Close}$                  | 5,76 € soit **4,4 %**                             |
| **Position dans le canal** | $(\text{Close}-d_{\text{inf}})/(d_{\text{sup}}-d_{\text{inf}})$ | **24 %** de la hauteur                            |
| **Distances aux bornes**   | $d/\text{Close} - 1$                                            | $+3{,}3\,\%$ au plafond, $-1{,}0\,\%$ au plancher |

Le canal actif est le trait plein à droite de la
[figure du cours](README.md#la-figure-du-cours) — établie, elle, sur les clôtures
seules, d'où des valeurs voisines mais non identiques.

La **position dans le canal** est la seule des quatre qui soit sans dimension et
comparable d'un titre à l'autre. Elle vaut 0 % sur le support, 100 % sur la
résistance. À 24 %, le cours d'Airbus est dans le bas de son canal — il vient de
toucher son support le jour même (`2023-12-29` est le quatrième épisode de contact
du support, cf. [module 2](02-portee-et-episodes-de-contact.md#23--compter-des-contacts-pas-des-jours)).

**Les distances asymétriques sont l'information la plus concrète** : il y a
$3{,}3\,\%$ de marge avant le plafond et $1{,}0\,\%$ avant le plancher. Ce sont des
grandeurs vérifiables, datées, et qui ne supposent aucun modèle.

## 4.2 — Un canal convergent a une date de péremption

Les deux bords d'un encadrement convexe ont des pentes **indépendantes**
([module 1](01-la-droite-qui-ne-coupe-rien.md#15--ce-que-lobjet-na-pas)). Quand
elles diffèrent, le canal s'évase ou se referme — et s'il se referme, il disparaît
à une date calculable :

$$\tau = \frac{d_{\text{sup}}(t_0) - d_{\text{inf}}(t_0)}{\text{pente}_{\text{inf}} - \text{pente}_{\text{sup}}}$$

Sur Airbus : la résistance monte de $+0{,}0483$ €/séance, le support de
$+0{,}3626$. Le support monte **7,5 fois plus vite**, et l'écart se comble de
$0{,}3143$ € par séance :

$$\tau = \frac{5{,}76}{0{,}3143} = 18{,}3 \text{ séances}$$

> 🔑 **Ce canal cesse d'exister vers la fin janvier 2024.** Toute lecture qui le
> prolonge au-delà décrit un objet vide. Un biseau qui se referme n'est pas une
> figure prédictive : c'est la preuve que les deux droites ont été ajustées sur
> des phénomènes de durées différentes — ici une résistance de portée 102 et un
> support de portée 43.

C'est le contrôle que l'on oublie le plus souvent, et c'est le moins coûteux :
une division.

## 4.3 — Franchissement

Une clôture au-delà d'une borne se qualifie exactement comme une sortie de canal
de régression ([cours canal, module 4](../canal/04-sorties-de-canal.md)), avec une
différence majeure : **il n'y a pas d'échelle probabiliste ici**. On ne peut pas
dire combien de franchissements attendre « sous $H_0$ », parce qu'il n'y a pas de
$H_0$ — une droite d'enveloppe n'est pas un estimateur.

Ce qui reste chiffrable :

| Élément                                         | Ce qu'il apporte                                                                       |
| ----------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Date** de la première clôture au-delà         | ancre l'événement                                                                      |
| **Ampleur** en % du cours, et en $\varepsilon$  | un dépassement inférieur à $\varepsilon$ n'est pas un franchissement, c'est un contact |
| **Persistance** : séances consécutives au-delà  | le discriminant ; une séance isolée ne prouve rien                                     |
| **Volume** rapporté à sa moyenne sur 20 séances | la seule preuve indépendante de la géométrie                                           |

Et deux réserves propres à la méthode :

- **La droite n'existe que sur sa fenêtre.** Un « franchissement » de la
  résistance du bloc 3 en 2023 n'a aucun sens : cette droite décrivait le premier
  semestre 2021.
- **Le franchissement est mécaniquement garanti à terme** dans un canal
  convergent (§ 4.2). Annoncer une « sortie imminente » à 18 séances de la
  fermeture, c'est annoncer une certitude géométrique.

## 4.4 — Ce que l'encadrement n'autorise pas

C'est le module qui compte le plus, et le plus court.

Un encadrement **décrit** : voici deux droites, leurs équations, les dates où le
cours les a touchées, l'écart actuel à chacune. Tout cela est vérifiable et daté.

Il ne dit **pas** :

- **que le cours va rebondir sur le support.** Rien dans la construction ne le
  suggère : la droite passe par des plus-bas *passés*, un point c'est tout. Le
  cours d'Airbus a touché son support le 29 décembre 2023 — cette phrase décrit le
  passé, elle ne contient aucune information sur le 2 janvier 2024.
- **que le niveau est « observé par le marché ».** Une droite d'enveloppe convexe
  est une construction d'analyste, pas un ordre dans un carnet.
- **quoi faire.** L'encadrement fournit des distances et des dates ; il ne
  recommande ni achat, ni vente, ni conservation, et ne dimensionne aucune
  position. Le passage de « le cours est à 1 % de son support » à « donc il faut
  acheter » n'est contenu nulle part dans ce cours — il suppose une vue sur le
  rendement attendu, une tolérance au risque et une situation patrimoniale, qui
  sont hors du champ d'une figure géométrique.

Et la réserve qui les résume toutes, déjà posée au
[§ 9.10 de l'étape 9](../modele/09-exemple-complet.md) : sur les 20 premières
séances de 2020, Airbus offrait une tendance haussière significative à 5 %,
proprement encadrée. Sept semaines plus tard, le titre valait 45 €. Une droite
d'encadrement décrit la fenêtre qui l'a produite. Rien d'autre.

---

⬅️ [Module 3 — Segmenter un historique long](03-segmenter-un-historique-long.md) ·
🏠 [README du cours](README.md)
