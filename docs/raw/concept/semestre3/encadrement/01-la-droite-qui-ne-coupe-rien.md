# Module 1 — La droite qui ne coupe rien

**Prérequis :** aucun au-delà de la géométrie du plan.
**Ce qu'on établit ici :** la définition exacte d'une droite de support ou de résistance, et l'algorithme qui les produit toutes.

---

## 1.1 — Ce qu'on demande à une droite de résistance

Un chartiste trace une résistance en posant sa règle sur les sommets. Formalisons
l'exigence, elle est double :

> **Définition.** Une **droite de résistance** sur une fenêtre de $n$ séances est
> une droite $d$ telle que
> 1. $\text{High}_i \le d(i)$ pour **tout** $i$ de la fenêtre — elle ne traverse
>    aucun plus-haut ;
> 2. $\text{High}_i = d(i)$ pour au moins **deux** valeurs de $i$ — elle est
>    tendue contre le nuage, pas flottante au-dessus.
>
> La **droite de support** est la définition symétrique sur les $\text{Low}_i$,
> avec $\text{Low}_i \ge d(i)$.

La condition 1 est ce qui distingue une résistance d'une régression : la droite
ajustée du [cours canal](../canal/01-du-point-a-la-bande.md) traverse le nuage,
c'est même sa raison d'être. Une résistance, non.

La condition 2 élimine l'infinité de droites qu'on pourrait poser au-dessus du
nuage sans le toucher. Ensemble, les deux conditions ne laissent qu'un nombre
**fini** de droites — et il se trouve qu'on sait les énumérer toutes.

## 1.2 — Ce sont exactement les arêtes de l'enveloppe convexe

> **Théorème.** Les droites vérifiant les deux conditions sont exactement les
> droites portant les **arêtes de la chaîne supérieure de l'enveloppe convexe**
> des points $(i, \text{High}_i)$.

*Justification.* Une droite qui laisse tous les points d'un côté est une droite
d'appui du nuage ; les droites d'appui d'un ensemble fini touchant au moins deux
points sont précisément les droites portant les arêtes de son enveloppe convexe.
La condition « au-dessus » sélectionne la moitié supérieure de cette enveloppe,
sa **chaîne supérieure** — le trajet du point le plus à gauche au point le plus à
droite en passant par le haut.

Trois conséquences pratiques, qui font tout l'intérêt de la formulation :

- **Il n'y a pas de choix arbitraire.** L'ensemble des résistances valides est
  déterminé par les données seules. Le seul jugement restant porte sur *laquelle*
  retenir, et le [module 2](02-portee-et-episodes-de-contact.md) le réduit à une
  règle chiffrée.
- **Le nombre d'arêtes est petit.** Sur les 1027 séances d'Airbus, la chaîne
  supérieure ne compte que **5 sommets**, donc 4 arêtes — 4 résistances
  candidates pour quatre années de cotation.
- **Les pentes sont monotones le long de la chaîne.** C'est la convexité : les
  pentes de la chaîne supérieure décroissent, celles de la chaîne inférieure
  croissent. Un contrôle gratuit de l'implémentation.

## 1.3 — Le balayage de Andrew

L'algorithme tient en quinze lignes, sans dépendance, en $O(n\log n)$ — et le tri
est déjà fait puisque les séances arrivent en ordre chronologique.

```python
def chaine(points, inferieure=True):
    """Chaîne inférieure (support) ou supérieure (résistance) de l'enveloppe convexe.

    points : liste de couples (rang de séance, prix).
    """
    s = 1 if inferieure else -1
    pile = []
    for p in sorted(points):
        while len(pile) >= 2:
            (x1, y1), (x2, y2) = pile[-2], pile[-1]
            # produit vectoriel : on dépile tant que le dernier sommet
            # n'est plus extrémal une fois p connu
            if s * ((x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)) < 0:
                pile.pop()
            else:
                break
        pile.append(p)
    return pile
```

Le cœur est le **produit vectoriel** $(P_2-P_1) \wedge (P-P_1)$ : son signe dit de
quel côté de la droite $P_1P_2$ tombe le point $P$. S'il indique que $P_2$ n'est
plus sur l'enveloppe une fois $P$ connu, on dépile. Chaque point est empilé et
dépilé au plus une fois : le balayage est linéaire après le tri.

Pour l'arête $(x_1,y_1) \to (x_2,y_2)$, la droite s'écrit

$$d(t) = y_1 + \frac{y_2-y_1}{x_2-x_1}\,(t-x_1).$$

## 1.4 — Les deux contrôles à exécuter

Une implémentation d'enveloppe convexe se trompe silencieusement : elle rend une
liste de points plausible même quand le signe est inversé. Deux vérifications
suffisent, et elles doivent être exécutées, pas supposées.

**Contrôle 1 — aucune traversée.** Pour la droite retenue, compter les $i$ tels
que $\text{High}_i > d(i)$. Le résultat doit être **0**, exactement. Sur les
9 blocs d'Airbus du [module 3](03-segmenter-un-historique-long.md), les 18 droites
produites donnent toutes 0 violation.

C'est vérifiable à l'œil sur la [figure du cours](README.md#la-figure-du-cours) :
aucune des vingt droites ne coupe la courbe bleue.

**Contrôle 2 — monotonie des pentes.** Calculer les pentes successives de la
chaîne : croissantes pour la chaîne inférieure, décroissantes pour la supérieure.
Sur la fenêtre active d'Airbus, la chaîne supérieure donne des pentes strictement
décroissantes, la chaîne inférieure strictement croissantes.

Un signe inversé dans le produit vectoriel casse le contrôle 2 avant le
contrôle 1 : c'est le plus sensible des deux.

## 1.5 — Ce que l'objet n'a pas

Il faut être clair sur ce que cette construction ne fournit pas, parce que la
comparaison avec le [canal de régression](../canal/README.md) est instructive :

|                          | Canal de régression                             | Encadrement convexe                               |
| ------------------------ | ----------------------------------------------- | ------------------------------------------------- |
| Utilise                  | toutes les clôtures                             | les extrêmes de séance seulement                  |
| Bords                    | parallèles par construction                     | **deux pentes indépendantes**                     |
| Échelle d'incertitude    | oui — $s$, bandes de confiance et de prédiction | **aucune**                                        |
| Sensibilité à un point   | diluée sur $n$ points                           | **totale** : déplacer un sommet déplace la droite |
| Test statistique associé | oui (étape 8)                                   | **non**                                           |

La dernière ligne est la plus importante. Une droite d'enveloppe convexe est un
objet **géométrique**, pas statistique : on ne peut pas lui associer de $p$-valeur,
ni dire qu'un contact est « significatif ». Tout ce qu'on peut chiffrer à son
sujet, c'est sa portée et son nombre d'épisodes de contact — l'objet du
[module 2](02-portee-et-episodes-de-contact.md).

---

⬅️ [README du cours](README.md) ·
➡️ [Module 2 — Portée et épisodes de contact](02-portee-et-episodes-de-contact.md)
