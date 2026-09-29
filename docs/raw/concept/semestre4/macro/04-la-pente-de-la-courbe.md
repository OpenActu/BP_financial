# Module 4 — La pente de la courbe des taux

**Prérequis :** [module 1](01-le-taux-d-actualisation.md).
**Ce qu'on établit ici :** que la pente de la courbe des taux est l'un des meilleurs prédicteurs de **récession** connus, et que cela n'en fait pas un prédicteur de **rendement** — la confusion entre les deux étant l'une des plus fréquentes du domaine.

---

## 4.1 — Ce qu'est la pente

La courbe des taux relie, à une date donnée, le taux d'emprunt d'un État à la
durée de l'emprunt. Sa **pente** se résume le plus souvent par un écart :

$$\text{pente}_t = y^{10\text{ ans}}_t - y^{3\text{ mois}}_t$$

D'ordinaire, elle est **positive** : prêter dix ans est plus risqué que prêter
trois mois, et se paie plus cher. Elle devient **négative** (on dit la courbe
« inversée ») quand le marché anticipe des baisses de taux courts, donc, le plus
souvent, un ralentissement.

## 4.2 — Un bon prédicteur de récession

Estrella & Hardouvelis (1991), puis Estrella & Mishkin (1998), montrent que la
pente est l'un des meilleurs indicateurs avancés de récession américaine à un
horizon de **quatre à six trimestres**, meilleur que la plupart des indicateurs
d'activité. C'est l'un des résultats les plus robustes de la macro-finance, et il
a résisté à des décennies de données postérieures à sa publication.

Mais c'est un prédicteur à **décalage long et variable**. L'inversion de
2022-2023, la plus profonde depuis quarante ans, n'a pas été suivie dans les deux
ans de la récession américaine que la règle annonçait. Un prédicteur de récession
qui se trompe une fois reste un bon prédicteur ; il n'est pas un calendrier.

## 4.3 — Un mauvais prédicteur de rendement

La chaîne de raisonnement semble évidente : courbe inversée → récession → baisse
des actions → vendre à l'inversion. Elle casse au premier maillon qui compte :
**le marché lit la courbe lui aussi**. Si l'inversion annonce une récession, cette
annonce est dans les cours dès l'inversion, pas à la récession.

Mesurons-le sur le CAC 40, mois par mois, de 1990 à 2025. On régresse le
rendement du **mois suivant** sur la pente américaine connue à la fin du mois
(relevé D de [`mesurer_macro.py`](figures/mesurer_macro.md)) :

| | Valeur |
|---|---|
| Mois | 429 (1990-03 → 2025-11) |
| $R^2$ dans l'échantillon | **0,29 %** |
| $t$ de la pente | −1,12 |
| p-valeur | 0,264 |
| $R^2$ **hors** échantillon | **−0,43 %** |

*Lecture* : dans l'échantillon, la pente explique 0,29 % de la variance du
rendement mensuel suivant, sans significativité. Hors échantillon (une prévision
par mois à partir du 121ᵉ, chaque fois réestimée sur le seul passé), elle fait
**moins bien que la simple moyenne historique**. Le
[module 10](10-des-facteurs-a-la-prevision.md) définit cette statistique et
l'applique à deux autres variables de taux.

> 🔑 **Prédire une récession et prédire un rendement sont deux problèmes
> différents.** Le premier porte sur une variable que le marché ne fixe pas ; le
> second sur une variable que le marché fixe **en tenant compte** du premier.

## 4.4 — Trois limites de la mesure

- **La pente est américaine.** Le dépôt n'a pas de taux européens (voir le
  [README](README.md)). La pente de la zone euro n'a de toute façon pas d'équivalent
  simple, faute d'un seul émetteur souverain.
- **La variable est un prix de marché**, connu à la clôture, jamais révisé : pas
  de regard en avant. C'est ce qui rend le test honnête, et ce qui le distingue de
  ce qu'on ferait avec le PIB ([module 5](05-la-croissance.md)).
- **Un seul test sur 35 ans ne prouve pas l'absence d'effet.** Il montre qu'un
  effet, s'il existe, est trop petit pour se distinguer du bruit sur cette
  durée, ce qui suffit à écarter toute règle de décision fondée sur lui.

## Ce qu'il faut retenir

1. La pente de la courbe prédit bien les récessions, à 4-6 trimestres, avec un
   décalage variable.
2. Elle ne prédit pas le rendement des actions : sur le CAC 40 de 1990 à 2025,
   $R^2 = 0{,}29\,\%$ dans l'échantillon, **négatif** hors échantillon.
3. Le marché lit la courbe : l'information est dans les prix dès l'inversion.

---

⬅️ [Module 3 — L'inflation](03-l-inflation.md) ·
➡️ [Module 5 — La croissance : PIB et PMI](05-la-croissance.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
