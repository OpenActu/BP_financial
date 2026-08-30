# Module 2 — Les trois largeurs

**Prérequis :** [module 1](01-du-point-a-la-bande.md).
**Ce qu'on établit ici :** les trois conventions de demi-largeur, ce que chacune garantit, et pourquoi l'une d'elles interdit toute comparaison entre fenêtres.

---

Trois conventions coexistent. Elles produisent des dessins voisins et des
affirmations très différentes.

## 2.1 — L'enveloppe des résidus

Le canal le plus étroit qui contienne **tous** les points de la fenêtre, à pente
fixée. Connu sous le nom de *canal de Raff*.

**Ce qu'il garantit :** exactement ce qu'on lui a demandé — les $n$ points sont
dedans, par construction. C'est une propriété descriptive, pas probabiliste.

**Le piège, et il est sévère.** Sa largeur est l'**étendue** des résidus, une
statistique d'extrême : elle croît mécaniquement avec le nombre de points, même
si le processus est rigoureusement inchangé. Pour $n$ tirages gaussiens
d'écart-type $\sigma$ :

| $n$ | $\mathbb E[\text{étendue}]$ | Demi-largeur |
|---|---|---|
| 10 | $3{,}08\,\sigma$ | $1{,}54\,\sigma$ |
| 20 | $3{,}74\,\sigma$ | $1{,}87\,\sigma$ |
| 60 | $4{,}64\,\sigma$ | $2{,}32\,\sigma$ |
| 120 | $5{,}14\,\sigma$ | $2{,}57\,\sigma$ |
| 250 | $5{,}64\,\sigma$ | $2{,}82\,\sigma$ |

*(valeurs Monte-Carlo, 200 000 tirages ; la table classique donne $3{,}735$ pour
$n=20$)*

La croissance est en $2\sqrt{2\ln n}$ — lente, mais suffisante pour tout fausser :

> ⚠️ **Un canal-enveloppe sur 120 séances est ~37 % plus large qu'un canal-enveloppe
> sur 20 séances tirées du même processus.** Conclure « le titre est devenu plus
> volatil » de cette comparaison est une erreur de lecture, pas une observation.
> **Les largeurs d'enveloppe ne se comparent qu'à $n$ égal.**

## 2.2 — L'écart-type

La convention probabiliste. $s$ est l'estimateur sans biais de l'écart-type du
bruit ([README](README.md#notations)), $k$ est choisi — $1$, $2$, parfois $2{,}5$.

**Ce qu'elle garantit :** sous les hypothèses de l'[étape 8](../modele/08-test-de-tendance.md)
— erreurs i.i.d. gaussiennes — une proportion attendue de points à l'intérieur,
indépendante de $n$ :

| $k$ | Points attendus dedans | Points attendus dehors sur 20 |
|---|---|---|
| 1 | 68,3 % | 6,3 |
| 2 | 95,5 % | 0,9 |
| 2,5 | 98,8 % | 0,25 |
| 3 | 99,7 % | 0,05 |

**C'est la seule des trois conventions comparable d'une fenêtre à l'autre**, et
c'est la raison de la préférer par défaut. Son coût : elle n'a de sens que sous
des hypothèses que le [module 4](04-sorties-de-canal.md) montre fragiles sur un
cours de bourse.

> **Attention à $\sigma_{\hat e}$ contre $s$.** Utiliser
> $\sigma_{\hat e} = \sqrt{\operatorname{Var}(\hat e)_{\min}}$ au lieu de $s$
> rétrécit le canal du facteur $\sqrt{(n-2)/n}$ : $-5{,}1\,\%$ à $n=20$,
> $-0{,}8\,\%$ à $n=120$. Négligeable sur fenêtre longue, à ne pas ignorer sur
> fenêtre courte.

## 2.3 — Le quantile empirique

$a$ et $b$ sont les quantiles empiriques des résidus à $\alpha/2$ et
$1-\alpha/2$ — par exemple les 5ᵉ et 95ᵉ centiles.

**Ce qu'il garantit :** la proportion voulue de points dedans, **sans hypothèse
de loi**. C'est l'option robuste, et elle capture les canaux asymétriques, chose
que $\pm ks$ ne peut pas faire par construction.

**Sa limite est le nombre de points.** Un 5ᵉ centile sur 20 observations est
déterminé par un seul point : il est aussi instable que l'enveloppe. Cette
convention ne devient raisonnable qu'à partir de 60 à 100 séances.

## 2.4 — Récapitulatif

| | Enveloppe | $\pm k\,s$ | Quantile |
|---|---|---|---|
| Garantit | 100 % des points dedans | une proportion, **sous hypothèse gaussienne** | une proportion, sans hypothèse |
| Comparable entre fenêtres | ❌ croît en $\sqrt{2\ln n}$ | ✅ | ✅ si $n$ suffisant |
| Asymétrie du canal | ✅ capturée | ❌ symétrique par construction | ✅ capturée |
| Sensibilité à un point extrême | maximale | modérée | faible |
| $n$ minimum utile | 10 | 15–20 | 60 |
| Usage recommandé | illustration, jamais comparaison | **par défaut** | fenêtres longues, résidus asymétriques |

## 2.5 — L'autre canal : l'enveloppe convexe

L'analyse graphique traditionnelle ne trace pas un canal de régression. Elle fait
passer une droite **par les plus-bas** et une autre **par les plus-hauts** — un
objet différent, qu'il faut savoir construire proprement pour le comparer.

La construction rigoureuse est l'**enveloppe convexe** :

- **support** : chaîne inférieure de l'enveloppe convexe des points $(i, \text{Low}_i)$ ;
- **résistance** : chaîne supérieure de celle des $(i, \text{High}_i)$.

Chaque arête d'une chaîne est une droite qui touche exactement deux points sans
en traverser aucun — c'est précisément ce qu'un chartiste cherche à tracer à la
main. Le balayage de Andrew la donne en $O(n\log n)$.

**Ce qui distingue les deux objets :**

| | Canal de régression | Enveloppe convexe |
|---|---|---|
| Bords | parallèles (une seule pente) | **deux pentes indépendantes** — le canal peut converger ou diverger |
| Basé sur | les clôtures | les extrêmes de séance (`Low`, `High`) |
| Sensibilité | tous les points comptent | seuls les points extrêmes comptent |
| Prolongeable | oui, avec une incertitude calculable | oui, mais sans échelle d'incertitude |

> ⚠️ **Le piège de la dernière arête.** La chaîne se termine souvent par une
> arête très courte, de pente aberrante. Sur les 20 premières séances 2020
> d'Airbus, la dernière arête haute n'enjambe que 3 séances et donne $-0{,}74$
> €/séance, soit $-0{,}6\,\%$ par jour extrapolé sur rien. **Exiger une portée
> d'au moins $n/4$ séances, et toujours citer la portée retenue.**

Les deux canaux **doivent** être produits ensemble : leur désaccord — pentes très
différentes, ou enveloppe convexe qui diverge quand la régression reste
parallèle — signale un canal mal défini ou un retournement en cours. Leur accord
est la seule situation où un canal mérite qu'on s'y fie.

---

⬅️ [Module 1 — Du point à la bande](01-du-point-a-la-bande.md) ·
➡️ [Module 3 — Épaisseur variable et levier](03-epaisseur-variable-et-levier.md)
