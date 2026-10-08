# Module 11 — La fiche, à remplir ⭐

**Prérequis :** les modules [1](01-l-ecart-a-l-opinion.md) à [10](10-exemple-chiffre-huit-valeurs.md).
**Ce qu'on établit ici :** une procédure en sept étapes pour ficher n'importe quelle valeur avec les dix indicateurs, un modèle de fiche à copier, et un exercice complet sur une valeur que le cours n'a pas traitée.

---

## 11.1 — La procédure en sept étapes

Compter une heure par valeur la première fois, vingt minutes ensuite. Les
étapes sont dans cet ordre parce que chacune peut **arrêter** les suivantes.

**Étape 1 — Lancer le relevé.**

```bash
python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py TICKER.PA --isin TICKER.PA=ISIN
```

L'ISIN se trouve sur la fiche de la valeur chez Euronext, ou dans
[`experience_9/univers.csv`](../../../../done/experimentation/experience_9/univers.csv)
pour les valeurs du CAC 40. Sans lui, les positions courtes ne sont pas lues.
Noter la **date** du relevé : tout ce qui suit en dépend.

**Étape 2 — Contrôler la recevabilité.** Avant de lire un seul indicateur :

| Contrôle | Où le voir | Si le contrôle échoue |
|---|---|---|
| saut de plus de 50 % sans division | message « série irrecevable » | **arrêter** : opération sur titre présumée |
| définitions du BPA | ligne « attendu / récent » avec ⚠ | ne comparer le PER à rien qui vienne du consensus |
| dette discordante | ⚠ « sources discordantes » | levier non mesurable ; chercher la dette dans le rapport annuel |
| bénéfice négatif | PER et croissance implicite vides | indicateur 4 non mesurable ; la décomposition l'est parfois |
| élément exceptionnel | une marge nette ou un bénéfice qui bouge de plus de 50 points de log en un an | lire toute la fiche comme dominée par un **effet de base** |

**Étape 3 — Situer le contexte** (indicateurs 2, 3, 8, 9). Une phrase, qui
range le moment dans les grilles des modules [6](06-taux-et-credit.md) et
[7](07-change-croissance-inflation.md). Elle vaut pour toutes les valeurs du
même jour : l'écrire une fois.

**Étape 4 — Lire les attentes** (indicateur 1). Révision, diffusion, dispersion,
croissance attendue. Se demander : l'opinion porte-t-elle sur la société, ou sur
une matière première, une devise, un événement ?

**Étape 5 — Lire le prix des attentes** (indicateurs 4 et 6). Croissance
implicite, prime, décomposition sur trois ans, marge contre sa moyenne. Se
demander : une hausse d'opinion se cache-t-elle dans le multiple, et le bénéfice
qui la porte est-il **normal** pour le cycle ?

**Étape 6 — Chercher le canal** (indicateurs 5 et 7). Dynamique de la dette,
nombre d'actions. Si l'un des deux bouge, **ouvrir le rapport annuel** et écrire
en une ligne ce qu'il a financé.

**Étape 7 — Conclure.** Positionnement (indicateur 10), marqueurs, verdict par
les règles ordonnées du [§ 9.3](09-assembler-la-sequence.md), puis vérification
des composantes. Si le verdict n'est pas le défaut, écrire une **thèse
réfutable** datée.

## 11.2 — Le modèle de fiche

À copier, une fiche par valeur et par date.

```markdown
# Fiche — <VALEUR> (<TICKER>) — relevé du <AAAA-MM-JJ>

## Recevabilité
- Série : recevable / irrecevable (motif)
- BPA : attendu / récent = … — définitions cohérentes / différentes
- Dette : cohérente / discordante (… contre … Md€)
- Effet de base : oui (exercice …, motif) / non

## Contexte (commun au jour)
- Régime : <une phrase>

## Ce que la société gagne, et ce qu'on croit
| Indicateur | Valeur | Repère | Lecture |
|---|---|---|---|
| 1 révision 90 j / diffusion / dispersion | | seuils ±2 %, ±0,5 | |
| 1 croissance attendue N+1/N | | | |
| 4 PER / croissance implicite | | 3 % | |
| 4 décomposition 3 ans : bénéfice / multiple | | | |
| 6 marge op. contre sa moyenne | | ±2 pt | |

## Comment elle se finance
| Indicateur | Valeur | Repère | Lecture |
|---|---|---|---|
| 5 dette/EBITDA, couverture, dynamique | | 3 ; 3 ; +10 pt | |
| 7 actions sur un an | | ±2 % | |
| Ce qu'a financé la dette ou l'émission | <rapport annuel, page> | | |

## Ce que croient les autres
| Indicateur | Valeur | Repère | Lecture |
|---|---|---|---|
| 8 b_EURUSD (t) | | EMD ≈ 0,7 sur 3 ans | |
| 10 positions courtes, variation 90 j | | 2 % ; +0,5 pt | |
| 10 volume relatif | | 1,5 | |

## Verdict
- Marqueurs : B1 · B2 · B3 · B4 · R1 · R2 · R3
- Règle appliquée (§ 9.3) : n° …
- Vérification des composantes : <ce qui confirme ou écarte>
- Verdict : <aucune séquence identifiable / valorisation exigeante / séquence candidate (canal) / bascule candidate>

## Thèse réfutable (si le verdict n'est pas le défaut)
- Thèse : <grandeur mesurable par le script, à une date>
- Réfutée si : <valeur>
- Date de jugement : <AAAA-MM-JJ>

## Ce que cette fiche ne dit pas
- Ni achat, ni vente, ni moment. Une configuration, à une date.
```

## 11.3 — L'exercice : Kering

Kering ne figure pas parmi les huit valeurs du cours. C'est la valeur sur
laquelle le script a révélé le défaut de R1, corrigé avant publication : un
dernier rappel qu'une grille se met à l'épreuve sur des valeurs qu'elle n'a pas
servi à construire.

```bash
python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py KER.PA --isin KER.PA=FR0000121485
```

**Consigne.** Remplir la fiche du § 11.2 sur le relevé du jour. Puis la comparer
au corrigé ci-dessous, établi sur le relevé du **8 octobre 2026** : les chiffres
auront bougé, la **démarche** doit rester la même. Pour chaque écart de verdict,
dire si c'est la donnée qui a changé ou la lecture.

### Corrigé, relevé du 8 octobre 2026

**Recevabilité.** Série recevable. BPA des douze derniers mois **négatif**
(−2,98 €) : PER, croissance implicite et prime sont **vides**, et le rapport de
cohérence aussi. Dette cohérente. **Effet de base massif** : le résultat net a
perdu 261,6 points de log de marge nette en un an.

**Attentes.** Révision −3,0 % ↓ sur l'exercice en cours, diffusion −0,50 ↓
(4 hausses, 12 baisses), dispersion 44 % sur 23 analystes. Le consensus attend
**+54,8 %** de BPA en 2027 : un rebond depuis une base effondrée, donc un chiffre
de même nature que la révision d'Orange au [module 2](02-les-attentes-de-benefices.md).

**Prix des attentes.** Décomposition sur trois ans : bénéfice **−387,6**, multiple
**+315,7**, dividendes +8,7 : total −63,2 points de log, soit un cours divisé par
deux ($e^{-0{,}719} = 0{,}49$). Le « multiple » qui monte de 315,7 points est le
paradoxe du PER cyclique poussé à l'extrême : un PER de 352,8 sur l'exercice 2025
ne mesure aucune opinion. Marge opérationnelle 11,1 % contre 19,3 % de moyenne :
**−8,2 points**, la plus forte chute de tout le cours.

**Financement.** Dette/EBITDA **5,82** (« dette lourde »), couverture des
intérêts **1,7** (« tendue »), dette en hausse de 20,8 points de plus que
l'EBITDA. Nombre d'actions stable.

**Positionnement.** Une position courte publiée de 0,50 % du capital, apparue
dans les 90 jours ; volume relatif 1,17. Sensibilité au change non mesurable
($t = -0{,}28$).

**Marqueurs.** B3 seul. R1 éteint depuis sa correction (le cours a baissé).
R2 non mesurable (croissance implicite vide).

**Verdict.** Règle 1 : non (aucune séquence candidate antérieure). Règle 2 :
non (ni B1 ni B2). Règle 3 : non (ni B2, ni croissance implicite mesurable).
**Aucune séquence réflexive identifiable.**

**Ce que le verdict ne dit pas — et que la fiche dit.** Le défaut ne signifie
pas que tout va bien. Il signifie que la grille de Soros, qui cherche des
**booms** auto-entretenus, n'en voit pas. La fiche, elle, montre une société
dont le bénéfice s'est effondré, dont la marge a perdu huit points, et dont le
levier est lourd et monte. Chez Merton ([module 8 du cours macro](../macro/08-le-credit.md)),
c'est la configuration où l'action amplifie le plus les variations de la valeur
des actifs. C'est un profil de **fragilité financière**, pas de bulle : une
autre question, que le [cours finance](../finance/README.md) apprend à
dimensionner.

> 🔑 **Une grille répond à la question pour laquelle elle a été construite.**
> Celle-ci cherche des boucles entre cours et fondamentaux. Elle n'est ni une
> mesure de risque, ni une mesure de qualité, ni une mesure de cherté. Remplir la
> fiche en entier, et pas seulement la ligne des marqueurs, c'est ce qui évite de
> lui faire dire ce qu'elle ne mesure pas.

## 11.4 — Ce qu'on sait faire à la fin du cours

| On sait… | Avec… |
|---|---|
| traduire un prix en hypothèse de croissance, et la discuter | la croissance implicite, la prime, la décomposition |
| lire un consensus sans se laisser abuser par une base faible ou une définition | révision, diffusion, dispersion, contrôle de cohérence |
| reconnaître un PER cyclique | la décomposition, le bénéfice contre sa moyenne |
| chercher un canal réflexif, et dire quand il n'y en a pas | levier, dilution, rapport annuel |
| situer le régime monétaire et le crédit | BCE, Eurostat, BRI |
| savoir ce qu'une courte fenêtre ne peut pas établir | l'effet minimal détectable |
| lire ce qui est public du positionnement, et ce qui ne l'est pas | AMF, volume relatif |
| conclure sans sur-conclure | les règles ordonnées, le défaut, la thèse réfutable |

## Ce qu'il faut retenir

1. Sept étapes, dans l'ordre : relevé, **recevabilité**, contexte, attentes, prix
   des attentes, **canal**, conclusion.
2. La recevabilité peut arrêter la fiche ; un effet de base la domine entière.
3. Le verdict se tire des règles ordonnées, **puis** se vérifie sur les
   composantes ; une thèse réfutable datée le rend utile.
4. Une grille répond à sa question : celle-ci cherche des boucles réflexives, pas
   le risque — Kering n'a pas de boom, et c'est une société fragile.

> ⚠️ **Ce cours ne donne aucun conseil en investissement.** Une fiche remplie
> décrit une configuration à une date ; elle ne dit ni d'acheter, ni de vendre,
> ni d'attendre.

---

⬅️ [Module 10 — Exemple chiffré : huit valeurs du CAC 40](10-exemple-chiffre-huit-valeurs.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
