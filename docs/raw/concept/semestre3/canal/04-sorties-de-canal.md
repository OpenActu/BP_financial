# Module 4 — Sorties de canal

**Prérequis :** [module 3](03-epaisseur-variable-et-levier.md).
**Ce qu'on établit ici :** combien de sorties de canal attendre **quand il ne se passe rien**, et pourquoi c'est la persistance, non la sortie, qui porte l'information.

---

## 4.1 — Le comptage de référence

Une « sortie de canal » est une observation dont le résidu studentisé dépasse $k$
en valeur absolue. Avant de lui prêter un sens, il faut savoir combien il en
survient **sous $H_0$**, c'est-à-dire quand la série est exactement « tendance
linéaire + bruit i.i.d. gaussien » et qu'aucun événement ne s'est produit.

Pour un point, $\Pr(|\hat e^{\,*}| > k) = \operatorname{erfc}(k/\sqrt2)$. Sur $n$
points supposés indépendants, la probabilité d'en voir **au moins un** sortir est
$1-(1-p)^n$ :

| $k$ | $p$ par point | $n=20$ : sorties attendues | $n=20$ : $\Pr(\ge 1)$ | $n=120$ : sorties attendues | $n=120$ : $\Pr(\ge 1)$ |
|---|---|---|---|---|---|
| 2 | 0,0455 | 0,91 | **60,6 %** | 5,46 | **99,6 %** |
| 2,5 | 0,0124 | 0,25 | 22,1 % | 1,49 | 77,7 % |
| 3 | 0,0027 | 0,05 | 5,3 % | 0,32 | 27,7 % |

> 🔑 **Sur 20 séances, une sortie de canal à $2\sigma$ arrive 6 fois sur 10 par
> pur hasard. Sur 120 séances, elle est quasi certaine — 99,6 %.** Annoncer une
> « rupture » sur ce seul constat, c'est annoncer un événement qui se produit
> presque toujours.

C'est le problème des comparaisons multiples, sous sa forme la plus élémentaire :
on ne teste pas un point, on en teste $n$ et on retient le pire.

## 4.2 — Le bon critère : la persistance

Deux sorties **consécutives** sont, elles, beaucoup plus rares. Sous
indépendance, la probabilité d'une paire adjacente vaut $p^2$, et $p^2/2$ pour
une paire du même côté :

| $k$ | $n=20$ : paires consécutives attendues | dont du même côté | $n=120$ | dont du même côté |
|---|---|---|---|---|
| 2 | 0,039 | **0,020** | 0,246 | 0,123 |
| 2,5 | 0,003 | 0,001 | 0,018 | 0,009 |

Deux clôtures consécutives au-delà de $2\sigma$ du même côté surviennent par
hasard dans **2 % des fenêtres de 20 séances**. Là, l'observation devient
informative — d'un facteur 30 par rapport à la sortie isolée.

**Règle pratique.** Une sortie de canal se qualifie par quatre éléments, jamais
par le seul franchissement :

| Élément | Ce qu'il apporte |
|---|---|
| **Date** de la première clôture hors canal | ancre l'événement |
| **Ampleur** en résidu **studentisé** (module 3) | comparable d'un point à l'autre |
| **Persistance** : nombre de séances consécutives dehors | le discriminant principal |
| **Volume** rapporté à sa moyenne sur 20 séances | une preuve indépendante de la géométrie |

Une sortie d'une séance, d'ampleur inférieure à $2$, sans volume, n'est pas une
rupture : c'est le bruit qu'on doit attendre.

## 4.3 — Trois raisons pour lesquelles ce comptage reste optimiste

Le tableau du § 4.1 est un **plancher** de fausses alertes. Trois effets le
dégradent, tous dans le même sens.

### a. Le canal est ajusté sur les points qu'on teste

Les résidus vérifient $\sum \hat e_i = 0$ et $\sum \hat e_i T_i = 0$
([module 1](01-du-point-a-la-bande.md#14--les-résidus-ne-sont-pas-libres)) : ils
ne sont ni indépendants, ni libres. Le canal a été tiré vers les points, y
compris vers celui qu'on déclare aberrant. Un vrai décrochage se trouve donc en
partie absorbé par la droite qu'il a lui-même déplacée, et la sortie mesurée est
**sous-estimée**.

### b. Sans studentisation, les sorties de bord sont manquées

Un résidu situé au bord de la fenêtre a un écart-type de $0{,}902\,\sigma$ contre
$0{,}975$ au centre ($n=20$). Comparé brutalement à $2s$, il devrait atteindre
$2{,}22$ en studentisé pour être signalé — **on rate les anomalies de bord,
c'est-à-dire les plus récentes**, les seules qui pourraient servir.

### c. L'autocorrélation, encore

C'est la réserve centrale de l'[étape 8](../modele/08-test-de-tendance.md#portée-et-limites),
et elle frappe ici avec une force particulière. Tout le § 4.2 repose sur
l'indépendance : c'est elle qui rend une paire consécutive $1/p$ fois plus rare
qu'une sortie isolée.

Si les résidus sont positivement autocorrélés — cas ordinaire d'une série de
cours, et cas garanti si le processus est une marche aléatoire — **les sorties
arrivent en paquets**. Le critère de persistance perd alors précisément ce qui en
faisait la valeur : les paires consécutives cessent d'être rares.

> ⚠️ **Vérifier Durbin–Watson sur les résidus avant d'utiliser le critère de
> persistance.** Un DW nettement inférieur à 2 invalide le § 4.2. Et un DW
> calculé sur 20 points a une puissance faible : ne pas détecter d'autocorrélation
> n'est pas prouver qu'il n'y en a pas.

## 4.4 — Ce qu'une sortie de canal ne dit pas

Le canal est un **résumé de la fenêtre passée**. Une sortie signifie exactement
ceci : *l'observation nouvelle est mal expliquée par la droite ajustée sur les
séances précédentes.* Elle ne dit pas :

- que la tendance a changé de signe — pour cela, refaire l'estimation et
  regarder l'intervalle de confiance sur la pente ;
- que le mouvement va se poursuivre — le canal n'a aucun contenu prédictif au
  delà de la [bande de prédiction](03-epaisseur-variable-et-levier.md#c-bande-de-prédiction),
  dont la largeur décourage l'exercice ;
- qu'un seuil « psychologique » a été franchi — le canal est une construction
  statistique, pas un niveau observé par le marché.

---

⬅️ [Module 3 — Épaisseur variable et levier](03-epaisseur-variable-et-levier.md) ·
➡️ [Module 5 — Le canal glissant](05-canal-glissant.md)
