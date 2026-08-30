# Module 2 — Portée et épisodes de contact

**Prérequis :** [module 1](01-la-droite-qui-ne-coupe-rien.md).
**Ce qu'on établit ici :** laquelle des arêtes retenir, et comment compter les contacts sans les gonfler.

---

Le module 1 laisse un ensemble fini de droites valides. Deux règles chiffrées
suffisent à choisir et à qualifier. Ce sont les deux endroits où l'analyse
graphique ordinaire se trompe le plus souvent.

## 2.1 — La portée, et le piège de la dernière arête

L'instinct dit de prendre la **dernière** arête de la chaîne, celle qui atteint le
bord droit : c'est elle qui encadre le cours aujourd'hui. L'instinct a tort une
fois sur deux.

**Le contre-exemple, en grandeur nature.** Sur les 20 premières séances 2020
d'Airbus (la fenêtre de l'[étape 9](../modele/09-exemple-complet.md)), les chaînes
donnent :

| Chaîne | Arête       | Portée        | Pente               |
| ------ | ----------- | ------------- | ------------------- |
| basse  | $5 \to 18$  | 13 séances    | $+0{,}165$ €/séance |
| basse  | $18 \to 20$ | **2 séances** | $+0{,}460$ €/séance |
| haute  | $1 \to 15$  | 14 séances    | $+0{,}236$ €/séance |
| haute  | $15 \to 17$ | **2 séances** | $+0{,}035$ €/séance |
| haute  | $17 \to 20$ | **3 séances** | $-0{,}740$ €/séance |

Lire les dernières arêtes donne un support à $+0{,}46$ et une résistance à
$-0{,}74$ : un biseau qui se referme violemment, figure spectaculaire — et
entièrement fabriquée par 2 et 3 séances. Les arêtes longues, elles, donnent
$+0{,}165$ et $+0{,}236$, cohérentes entre elles et avec la pente de régression
($+0{,}151$).

> **Règle de portée minimale.** Retenir la dernière arête dont la portée atteint
> $n/4$ séances ; à défaut, remonter d'une arête dans la chaîne. **Citer toujours
> la portée retenue.**

Le seuil $n/4$ n'a rien de sacré — c'est un compromis : assez long pour qu'une
pente ait un sens, assez court pour rester local. Ce qui n'est pas négociable,
c'est de le fixer *avant* de regarder le résultat, et de l'annoncer.

**Sur la fenêtre active d'Airbus** (120 séances, seuil 30), la règle retient une
résistance de portée **102** et un support de portée **43**. L'asymétrie est
elle-même une information : la résistance est une contrainte ancienne, le support
un phénomène des trois derniers mois.

## 2.2 — La tolérance de contact

Une droite d'enveloppe touche exactement deux points *au sens strict*. Mais une
séance qui passe à un centime de la droite l'a touchée, au sens qui intéresse le
lecteur. Il faut donc une tolérance, et elle doit être proportionnée à
l'agitation du titre :

$$\varepsilon = 0{,}25\,\sigma_{\text{Close}}$$

où $\sigma$ est l'écart-type des clôtures **sur la fenêtre considérée**, pas sur
l'historique entier. Une tolérance absolue en euros serait absurde : elle
compterait tout comme contact pendant le krach et rien en régime calme.

Sur la fenêtre active d'Airbus, $\sigma = 4{,}84$ € donne $\varepsilon = 1{,}21$ €,
soit $0{,}9\,\%$ du cours. Pendant le premier bloc de 2020 — le krach —
$\varepsilon$ vaut $8{,}03$ € : la même règle, appliquée à une volatilité près de
sept fois plus forte.

## 2.3 — Compter des contacts, pas des jours

Voici l'erreur la plus commune, et la plus flatteuse pour l'analyste : additionner
les **jours** où le cours est dans la tolérance.

Sur la résistance active d'Airbus, les jours de contact sont :

```
2023-07-25   2023-12-11   2023-12-12   2023-12-13   2023-12-14
```

Cinq jours. Mais du 11 au 14 décembre, ce sont **quatre séances consécutives du
même mouvement** : le cours est venu buter une fois, et y est resté quatre jours.
Compter 5 revient à confondre la durée d'un contact avec leur nombre.

> **Règle d'épisode.** Des jours de contact séparés de moins de **3 séances**
> appartiennent au même épisode. Le nombre d'épisodes est le nombre de contacts.

|                   | Jours de contact | **Épisodes** |
| ----------------- | ---------------- | ------------ |
| Résistance active | 5                | **2**        |
| Support actif     | 7                | **4**        |

Le détail des épisodes du support : `2023-10-23` · `2023-11-09…10` ·
`2023-12-20…22` · `2023-12-29`. Quatre venues distinctes sur trois mois — c'est
cela qui fait une droite, et c'est un fait tout différent de « 7 touches ».

## 2.4 — Combien de contacts pour y croire

L'échelle est grossière, et il faut l'annoncer comme telle : contrairement au
[test de tendance](../modele/08-test-de-tendance.md), rien ici n'est adossé à une
loi de probabilité.

| Épisodes  | Statut              | Lecture                                                                                          |
| --------- | ------------------- | ------------------------------------------------------------------------------------------------ |
| 2         | **non confirmée**   | c'est la définition de l'arête, pas une observation. Deux points définissent toujours une droite |
| 3         | crédible            | le troisième contact est le premier qui apporte de l'information                                 |
| 4 et plus | structure installée | le niveau a été éprouvé plusieurs fois                                                           |

**Appliqué à Airbus :** la résistance (2 épisodes) est **non confirmée** — elle
n'est rien de plus que l'arête qui la définit. Le support (4 épisodes) est une
structure installée. Il serait donc malhonnête de présenter les deux droites au
même titre, alors qu'elles apparaissent identiques sur un graphique.

## 2.5 — La fiche d'identité d'une droite

Récapitulatif de ce qu'il faut publier — omettre l'une de ces lignes rend la
droite invérifiable :

| Champ                   | Exemple (résistance active d'Airbus)             |
| ----------------------- | ------------------------------------------------ |
| Fenêtre                 | 2023-07-13 → 2023-12-29, 120 séances             |
| Ancre                   | 2023-07-25, 130,97 €                             |
| Pente                   | $+0{,}0483$ €/séance, soit $+0{,}037\,\%$/séance |
| Portée                  | 102 séances (seuil : 30)                         |
| Tolérance               | $\varepsilon = 1{,}21$ €                         |
| Épisodes de contact     | 2 — `2023-07-25`, `2023-12-11…14`                |
| Statut                  | non confirmée                                    |
| Valeur au dernier point | 136,33 €                                         |

---

⬅️ [Module 1 — La droite qui ne coupe rien](01-la-droite-qui-ne-coupe-rien.md) ·
➡️ [Module 3 — Segmenter un historique long](03-segmenter-un-historique-long.md)
