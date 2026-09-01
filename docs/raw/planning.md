# Planning — les dix cours en quatre semestres

Ce document organise le parcours. Les cours de [`concept/`](concept/sommaire/README.md)
sont autonomes et pouvaient jusqu'ici se lire dans n'importe quel ordre ; ce
n'était pas un service rendu au lecteur. **L'arborescence porte désormais le
parcours** : chaque cours vit sous le semestre où il doit être suivi.

```
concept/
├── semestre1/   les outils mathématiques
├── semestre2/   l'aléatoire
├── semestre3/   l'inférence et le modèle
├── semestre4/   la décision
└── sommaire/    les index (hors parcours)
```

## Le principe d'ordonnancement

Un seul, et il est contraignant : **aucun cours ne commence avant que ses
prérequis déclarés soient acquis.** Chaque README annonce les siens ; le
graphe ci-dessous n'est que leur mise à plat.

```
algèbre ─────────────┐
                     ├──► modèle (étapes 1→7) ──► canal ──► encadrement ──┐
dérivation ──┬───────┘                             │                      │
             │                                     ▼                      ▼
             └──► stat. mathématique ──► Student ──► modèle (étape 8)   trading
                                            │                             ▲
convexité ──────────────────────────────────┼──► alpha ───────────────────┤
                                            │      │                      │
                                            └──► finance                  │
                                                   fondamentaux ──────────┘
      S1                    S2                  S3                  S4
```

Deux conséquences qu'il faut accepter d'emblée :

- **La statistique se poursuit d'un semestre sur l'autre.** `statistique/`
  apparaît sous `semestre2/` (mathématique) et sous `semestre3/` (Student).
  Ce n'est pas une erreur de rangement : ce sont deux cours distincts, et le
  second ne peut pas commencer avant que le premier soit fini.
- **Le modèle est à cheval sur ses propres prérequis.** Ses étapes 1 à 7 ne
  demandent que l'algèbre ; son étape 8 demande Student. Il est donc placé en
  semestre 3, après Student, quitte à ce que ses sept premières étapes soient
  lisibles bien plus tôt.

## Vue d'ensemble

| Semestre | Thème | Cours | Modules | Volume |
|---|---|---|---|---|
| **1** | Les outils mathématiques | algèbre, dérivation-intégration, convexité | 26 | ≈ 27 h 30 |
| **2** | L'aléatoire | statistique mathématique | 26 | ≈ 32 h |
| **3** | L'inférence et le modèle | Student, modèle, canal, encadrement | 27 | ≈ 38 h |
| **4** | La décision | alpha, fondamentaux, trading, finance | 27 | ≈ 29 h 45 |
| | | **10 cours** | **106** | **≈ 127 h** |

> ℹ️ **Le nombre de modules est presque constant — 26, 26, 27, 27 — mais pas le
> volume.** Le semestre 3 est le plus dense, parce que la loi de Student pèse
> 24 h à elle seule et ne se coupe pas en deux. En compensation, ses neuf étapes
> du modèle sont courtes et se relisent vite : elles enchaînent une démonstration
> déjà énoncée dans [`modele.md`](modele.md).

---

## Semestre 1 — Les outils mathématiques

**Ce qu'on cherche :** disposer du vocabulaire géométrique et analytique sans
lequel tout le reste se lit comme une suite de recettes.

| Ordre | Cours | Modules | Volume |
|---|---|---|---|
| 1 | [Algèbre linéaire euclidienne](concept/semestre1/algebre/README.md) | 8 | 7 h 30 |
| 2 | [Dérivation et intégration](concept/semestre1/analyse/derivation-et-integration/README.md) | 9 | 10 h |
| 3 | [La convexité](concept/semestre1/analyse/convexite/README.md) | 9 | 10 h |

L'algèbre d'abord : elle donne le produit scalaire et la projection orthogonale,
dont tout le dépôt se sert ensuite sans les redémontrer. La dérivation ensuite,
parce que la convexité s'énonce avec des dérivées secondes.

> 🔑 **À la fin du semestre 1, on sait lire une régression comme une projection**
> — pas encore la démontrer, pas encore la tester, mais voir de quoi il s'agit.
> C'est le module
> [Dictionnaire géométrique des statistiques](concept/semestre1/algebre/07-dictionnaire-geometrique-des-statistiques.md)
> qui fait cette bascule ; c'est le plus important du semestre.

---

## Semestre 2 — L'aléatoire

**Ce qu'on cherche :** passer d'une description de données à un modèle de leur
production, seul cadre où une phrase comme « ce résultat est significatif » ait
un sens.

| Ordre | Cours | Modules | Volume |
|---|---|---|---|
| 1 | [Statistique mathématique](concept/semestre2/statistique/mathematique/README.md) | 26 | 32 h |

Un seul cours, et c'est le plus long du parcours. Il se traverse en trois temps :
variable aléatoire et moments, puis le catalogue des lois usuelles, puis les
théorèmes limites et l'inférence.

> ⚠️ **Le théorème central limite est le sommet du semestre, et le module qui le
> suit compte autant.** [Portée et limites du TCL](concept/semestre2/statistique/mathematique/13-portee-et-limites-du-tcl.md)
> et [Dépendance et échec du TCL](concept/semestre2/statistique/mathematique/14-dependance-et-echec-du-tcl.md)
> expliquent pourquoi il ne s'applique **pas** à une série de cours de bourse.
> Sauter ces deux modules, c'est perdre d'avance tout le semestre 4.

---

## Semestre 3 — L'inférence et le modèle

**Ce qu'on cherche :** savoir tester, puis appliquer ce test à l'objet du dépôt —
la droite de tendance et les bandes qui l'entourent.

| Ordre | Cours | Modules | Volume |
|---|---|---|---|
| 1 | [La loi de Student](concept/semestre3/statistique/loi-de-student/README.md) | 8 | 24 h |
| 2 | [Le modèle](concept/semestre3/modele/01-elimination-de-l-ordonnee.md) — les 9 étapes | 9 | ≈ 4 h |
| 3 | [Le canal de régression](concept/semestre3/canal/README.md) | 6 | 6 h |
| 4 | [L'encadrement](concept/semestre3/encadrement/README.md) | 4 | 4 h |

L'ordre est ici une contrainte stricte : le canal cite les étapes 7 et 8 du
modèle, et l'encadrement cite le module 2 du canal.

> 🔑 **C'est le semestre où le dépôt devient exécutable.** À la fin, les colonnes
> `E_n`, `VAR_n`, `CORR_n`, `VAL_n`, `T_n`, `P_n`, `TEND_n` produites par
> [`import_societe.py`](../../python/import_societe.md) sont toutes comprises,
> démonstration comprise, et l'agent
> [`chartiste`](../../.claude/agents/chartiste.md) devient lisible.

---

## Semestre 4 — La décision

**Ce qu'on cherche :** ce qu'on a le droit de conclure — et la liste, plus
longue, de ce qu'on n'a pas le droit de conclure.

| Ordre | Cours | Modules | Volume |
|---|---|---|---|
| 1 | [L'alpha](concept/semestre4/alpha/README.md) | 5 | 5 h |
| 2 | [Les fondamentaux](concept/semestre4/fondamentaux/README.md) | 5 | 5 h |
| 3 | [De la figure à la décision](concept/semestre4/trading/README.md) | 7 | 7 h |
| 4 | [Finance](concept/semestre4/finance/README.md) | 10 | 12 h 45 |

L'alpha d'abord : le cours fondamentaux s'appuie sur son module 4, et le cours
trading sur ses modules 2 à 4. La finance en dernier — c'est le seul cours qui
parle de **dimensionner** une position, et il n'a de sens qu'une fois su tout ce
qui précède sur l'incertitude.

> ⚠️ **Le semestre 4 est celui des résultats négatifs, et c'est voulu.** L'alpha
> n'est pas mesurable sur quelques années ; les fondamentaux n'ont pas
> d'historique donc pas de backtest ; la règle de décision rend `ATTENTE`
> 512 fois sur 515. Un lecteur qui traverse ce semestre en espérant une méthode
> pour gagner de l'argent l'aura mal lu.

---

## Comment suivre un semestre

- **Le README d'un cours se lit en entier avant son premier module.** Il contient
  le fil directeur et le tableau des idées fausses que le cours défait.
- **Les modules marqués ⭐** dans les plans sont ceux qui portent le cours. En
  cas de temps compté, ce sont eux et les exemples chiffrés.
- **Les exemples chiffrés se refont.** Chaque cours en a un dernier module ; les
  commandes sont dans le texte et les données se régénèrent avec
  [`import_societe.py`](../../python/import_societe.md) et
  [`import_fondamentaux.py`](../../python/import_fondamentaux.md).
- **Un semestre d'environ 30 h se tient en 13 semaines à 2 h 30**, README compris.
- **Ce qui est acquis se coche** dans
  [`avancement.md`](concept/sommaire/avancement.md) : un module par ligne, dans l'ordre ci-dessus.

## Ce que ce planning ne prétend pas être

- Ni un programme officiel, ni une équivalence avec un cursus existant. Les
  volumes sont des estimations portées par les README des cours, pas des heures
  d'enseignement mesurées.
- Ni un ordre unique. Un lecteur qui maîtrise déjà la statistique peut entrer
  directement au semestre 3 ; les prérequis de chaque README restent la référence,
  et ce document n'en est que la mise en séquence.

---

🏠 [Sommaire des cours](concept/sommaire/README.md) ·
📐 [`modele.md`](modele.md), le document de référence
