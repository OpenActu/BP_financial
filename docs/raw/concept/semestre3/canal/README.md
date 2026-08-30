# Cours — Le canal de régression

Ce que la droite ajustée de [`modele.md`](../../../modele.md) laisse de côté : **les
résidus**. La droite dit où passe la tendance ; le canal dit de combien le cours
s'en écarte, et c'est cette seconde information qui décide de tout usage
pratique — juger un écart, dater une rupture, dimensionner une attente.

Niveau bac+2. Prérequis : les [étapes 1 à 8 du modèle](../../../modele.md#plan-de-la-preuve),
en particulier la [droite ajustée](../modele/07-droite-ajustee.md) (étape 7) et la
[statistique de test](../modele/08-test-de-tendance.md) (étape 8).

## Pourquoi ce cours

Le tracé d'un canal est l'opération la plus courante de l'analyse graphique, et
la plus souvent faite de travers. Trois confusions reviennent, et ce cours existe
pour les défaire :

| Confusion courante | Ce qu'il en est | Module |
|---|---|---|
| « Le canal a une largeur, point. » | Il y en a **trois** conventions, qui ne garantissent pas la même chose et ne se comparent pas entre fenêtres de longueurs différentes | [02](02-les-trois-largeurs.md) |
| « Les bords sont parallèles à la droite. » | Seule la bande de **dispersion** l'est. Les bandes de confiance et de prédiction sont en **sablier** : la droite est presque deux fois moins sûre à ses extrémités qu'en son milieu | [03](03-epaisseur-variable-et-levier.md) |
| « Le cours est sorti du canal, c'est un signal. » | Sur 20 séances, une sortie à $2\sigma$ survient **6 fois sur 10 par pur hasard** | [04](04-sorties-de-canal.md) |

## Le fil directeur

> 🔑 **Un canal n'est pas une figure, c'est un intervalle.** Tout ce qui suit
> revient à répondre à une seule question : *cet intervalle est censé contenir
> quoi, avec quelle probabilité ?* Trois réponses possibles — les points passés,
> la vraie droite, la prochaine observation — donnent trois canaux différents,
> d'épaisseurs très inégales. Se tromper de réponse, c'est lire un signal là où
> il n'y a que de la géométrie.

## Plan

| # | Module | Ce qu'il établit |
|---|---|---|
| 1 | [Du point à la bande](01-du-point-a-la-bande.md) | Les résidus comme matière première ; le canal pivote au point moyen $(E(T), E(V))$ ; ce que le canal ajoute à `VAL_n` |
| 2 | [Les trois largeurs](02-les-trois-largeurs.md) | Enveloppe, écart-type, quantile ; l'enveloppe s'élargit en $\sqrt{2\ln n}$ et n'est **pas** comparable d'une fenêtre à l'autre ; le canal chartiste par enveloppe convexe |
| 3 | [Épaisseur variable et levier](03-epaisseur-variable-et-levier.md) ⭐ | $h_{ii}$, $\operatorname{Var}(\hat e_i)=\sigma^2(1-h_{ii})$ ; les trois bandes — dispersion, confiance, prédiction — et leurs formes |
| 4 | [Sorties de canal](04-sorties-de-canal.md) ⭐ | Combien de sorties attendre **sous** $H_0$ ; persistance ; ce que l'autocorrélation détruit dans ce comptage |
| 5 | [Le canal glissant](05-canal-glissant.md) | Le canal recalculé à chaque séance : il se repeint ; effet de la longueur de fenêtre ; pas de regard en avant |
| 6 | [Exemple chiffré — Airbus](06-exemple-chiffre-airbus.md) | Les cinq modules sur les 20 séances de l'[étape 9](../modele/09-exemple-complet.md) |

## Notations

Celles du [modèle](../../../modele.md), inchangées : $T_i = i$ (rangs de séance),
$V_i$ les clôtures, $f(t) = v_{0,\min} + r_{\min} t$ la droite ajustée,
$\hat e_i = V_i - f(i)$ les résidus, variances **de population** ($\div n$).

Une seule quantité nouvelle, et c'est la source de toutes les confusions
d'indices : à côté de la variance résiduelle de population

$$\operatorname{Var}(\hat e)_{\min} = \frac1n\sum_i \hat e_i^{\,2}$$

on utilise l'estimateur **sans biais** de la variance du bruit, qui divise par le
nombre de degrés de liberté restants :

$$s^2 = \frac{1}{n-2}\sum_i \hat e_i^{\,2} = \frac{n}{n-2}\operatorname{Var}(\hat e)_{\min}.$$

C'est $s$, et non $\sigma_{\hat e}=\sqrt{\operatorname{Var}(\hat e)_{\min}}$, qui
entre dans toutes les bandes probabilistes des modules 3 et 4. À $n=20$ le
facteur $\sqrt{n/(n-2)} = 1{,}054$ est modeste ; à $n=5$ il vaut $1{,}29$.

## Ce que ce cours alimente

- La colonne `VAL_n` de [`import_societe.py`](../../../../../python/import_societe.md)
  est $f(n)$, le bord central du canal à la séance courante. Le cours explique
  pourquoi c'est exactement là que la droite est la moins bien déterminée.
- L'agent [`chartiste`](../../../../../.claude/agents/chartiste.md) construit ces
  canaux ; les modules 2 et 4 sont les garde-fous qu'il applique.

---

➡️ Commencer par le [module 1 — Du point à la bande](01-du-point-a-la-bande.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
