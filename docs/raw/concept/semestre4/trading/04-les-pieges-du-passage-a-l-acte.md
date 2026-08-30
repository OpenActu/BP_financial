# Module 4 — Les pièges du passage à l'acte

**Prérequis :** [module 3](03-la-regle-ecrite-a-l-avance.md).
**Ce qu'on établit ici :** les six façons connues de corrompre un verdict pourtant issu d'une règle correcte — trois d'entre elles sont propres à ce dépôt et se démontrent sur les fichiers du fil rouge.

---

## 4.1 — Le regard en avant a trois portes d'entrée

C'est le piège le plus grave parce qu'il est invisible : le verdict reste
calculable, reproductible, et faux. Sur le fil rouge, il se glisse par trois
portes distinctes.

### a. La date demandée n'est pas une séance

**On veut décider le 1er janvier 2021. Le 1er janvier est férié.** Euronext Paris
est fermé, il n'existe aucune cotation à cette date, et la dernière information
disponible est la clôture du **jeudi 31 décembre 2020**.

Ce n'est pas un détail administratif : c'est la formulation même de la contrainte
de causalité. Une décision datée du jour $J$ ne peut utiliser que des données de
séances $\le J$, et si $J$ n'est pas une séance, la dernière séance strictement
antérieure fait foi. Le verdict du
[module 6](06-cas-pratique.md) est donc, littéralement, *le
verdict du 31 décembre 2020 publié le 1er janvier 2021*.

### b. `--fin` est exclusif

Deuxième porte, purement technique et redoutablement efficace :

```bash
python python/import_societe.py AIR.PA --debut 2019-01-02 --fin 2020-12-31
# -> docs/raw/data/quotes/AIR_PA_2019-01-02_2020-12-30.csv     512 séances

python python/import_societe.py AIR.PA --debut 2019-01-02 --fin 2021-01-01
# -> docs/raw/data/quotes/AIR_PA_2019-01-02_2020-12-31.csv     513 séances
```

`--fin` est transmis à `history(end=...)` de yfinance, où la borne est
**exclusive** ([miroir § 2](../../../../../python/import_societe.md)). Demander
`--fin 2020-12-31` **ampute la séance du 31 décembre**. Le nom du fichier produit
porte les dates réellement obtenues, pas celles demandées : c'est le contrôle à
faire systématiquement.

> ⚠️ **Vérifier le nom du fichier, pas la ligne de commande.** Ici l'erreur est
> conservatrice — elle retire de l'information — mais son symétrique
> (`--fin 2021-01-05` « pour être sûr d'avoir tout ») injecte trois séances de
> 2021 dans un verdict daté du 1er janvier. C'est un regard en avant complet.

### c. Les deux séries n'ont pas le même calendrier

Troisième porte, et celle qu'on oublie le plus :

| Série | Séances | Période |
|---|---|---|
| Airbus | **513** | 2019-01-02 → 2020-12-31 |
| CAC 40 | **512** | 2019-01-02 → 2020-12-31 |
| Dates communes | **512** | — |

La date orpheline est le **25 décembre 2019**, présente pour Airbus, absente pour
l'indice. Et voici la ligne, décimales tronquées :

```
2019-12-24,252,122.147,122.514,121.395,122.147,214381
2019-12-25,253,122.147,122.147,122.147,122.147,0
2019-12-27,254,122.459,123.744,121.799,122.276,693498
```

Volume **nul**, et `Open = High = Low = Close` exactement égaux à la clôture de la
veille : c'est une séance fantôme, un artefact de la source. Deux conséquences si
l'on ne l'élimine pas :

- elle injecte un rendement **exactement nul** dans la série du titre, ce qui
  réduit artificiellement sa volatilité mesurée ;
- surtout, si l'on apparie les deux séries **par position** au lieu de les
  apparier **par date**, tout ce qui suit le 25 décembre 2019 est décalé d'une
  séance — soit 260 rendements du titre confrontés au rendement du **lendemain**
  de l'indice. C'est un regard en avant d'un jour, appliqué à la moitié de
  l'échantillon.

> 🔑 **Aligner par date, jamais par rang.** La régression du
> [module 2 du cours alpha](../alpha/02-le-calcul-et-ses-erreurs-types.md) se fait
> sur les séances **communes** aux deux séries. Ici : 512 dates communes, donc
> **511 rendements**, et non 512.

### d. Le rappel de fond

Ces trois portes sont des cas particuliers de la règle générale du
[module 5 du cours canal](../../semestre3/canal/05-canal-glissant.md) : *une fenêtre glissante
ne doit jamais lire l'avenir.* Tout indicateur de `import_societe.py` la respecte
par construction — `E_n`, `VAL_n`, `TEND_n` à la ligne $i$ n'utilisent que les
lignes $i-n+1$ à $i$. Le seul endroit où l'analyste peut la violer, c'est en
choisissant sa fenêtre de téléchargement.

## 4.2 — Le canal se repeint

Le canal actif du 31 décembre 2020 n'existait pas le 30 décembre et n'existera pas
le 4 janvier. C'est un objet **recalculé à chaque séance**
([canal 05](../../semestre3/canal/05-canal-glissant.md)), et sa lecture rétrospective donne
toujours l'illusion d'une structure stable qui n'a jamais été observable en temps
réel.

Deux conséquences pratiques :

- un verdict est attaché à **une** séance ; le republier tel quel une semaine plus
  tard est une faute ;
- comparer un canal tracé aujourd'hui à un canal tracé il y a trois mois compare
  deux objets différents, pas deux états du même objet.

## 4.3 — Le drag de volatilité, sur le fil rouge

Piège classique et complètement contre-intuitif : **un excès de rendement moyen
positif n'implique pas d'avoir battu l'indice.**

Airbus contre le CAC 40, 2 janvier 2019 → 31 décembre 2020 :

| | Airbus | CAC 40 |
|---|---|---|
| Rendement arithmétique moyen, annualisé | $+18{,}61\,\%$ | $+11{,}42\,\%$ |
| **Performance cumulée** | **$+8{,}17\,\%$** | **$+18{,}38\,\%$** |
| CAGR | $+3{,}94\,\%$ | $+8{,}68\,\%$ |
| Volatilité annualisée | $54{,}27\,\%$ | $24{,}75\,\%$ |
| Écart moyenne − CAGR | **14,67 pts** | 2,74 pts |
| $\sigma^2/2$ | **14,73 %** | 3,06 % |
| Repli maximal | $-64{,}70\,\%$ (2020-03-18) | $-38{,}56\,\%$ (2020-03-18) |

L'écart entre moyenne arithmétique et performance réalisée est prédit au dixième
de point par $\sigma^2/2$ — c'est le drag de volatilité du
[cours finance, module 4](../finance/04-levier-optimal-et-drag.md), conséquence
directe de l'inégalité de Jensen.

Et les indicateurs relatifs sont **positifs** alors que le titre a perdu 10 points
contre son indice :

| | Valeur |
|---|---|
| Excès de rendement arithmétique annualisé | $+7{,}23\,\%$ |
| Tracking error | $39{,}13\,\%$/an |
| **Ratio d'information** | **$+0{,}185$** |

> ⚠️ **Ne jamais conclure d'un ratio d'information positif qu'une valeur a battu
> son indice.** Ici : ratio d'information $+0{,}19$, et $+8{,}2\,\%$ contre
> $+18{,}4\,\%$ en cumulé. Le cours alpha documente le même phénomène sur
> 2020-2023 ; ce module montre qu'il n'a rien d'exceptionnel — il apparaît sur
> toute fenêtre où la volatilité du titre écrase celle de l'indice.

## 4.4 — Les tests multiples, côté analyste

Traité au [module 3 § 3.5](03-la-regle-ecrite-a-l-avance.md). Deux compléments
propres au passage à l'acte :

- **Biais du survivant.** Un univers de titres constitué aujourd'hui exclut les
  faillites et les radiations. Une règle testée sur les composants actuels du
  CAC 40 est testée sur des gagnants sélectionnés par le futur.
- **Encombrement du facteur.** Le momentum 12-1 est documenté depuis les années
  1990 et massivement exploité. Un facteur publié et suivi cesse souvent de payer,
  et rien dans une série de prix ne permet de le détecter.

## 4.5 — Ce que le CSV ne contient pas et qui décide de tout

| Absent des données | Effet sur un verdict |
|---|---|
| Spread, commissions, droits de garde | une règle qui tourne vite est mangée avant d'avoir produit quoi que ce soit |
| Profondeur du carnet, impact de marché | un ordre de taille non négligeable ne s'exécute pas au dernier cours |
| Fiscalité, enveloppe (PEA, CTO), horizon | change le résultat net du tout au tout |
| Taux sans risque $r_f$ | posé à **zéro** dans tous les chiffres de ce cours |

Le dernier point mérite d'être dit explicitement plutôt que caché : **tous les
Sharpe et tous les alphas de ce cours sont calculés avec $r_f = 0$.** Ce n'est pas
une valeur neutre, c'est une hypothèse, et le dépôt ne contient aucune série de
taux permettant de faire autrement. Un $r_f$ non nul déplace l'alpha de
$(\beta - 1)\,r_f$ et modifie tous les Sharpe. **Annoncer $r_f$, même nul, fait
partie du résultat.**

## 4.6 — La checklist avant publication

| # | Contrôle | Sur le fil rouge |
|---|---|---|
| 1 | La date du verdict est-elle une séance ? | non — 1er janvier férié, on prend le 31/12/2020 |
| 2 | Le fichier téléchargé s'arrête-t-il bien à cette séance ? | oui, `..._2019-01-02_2020-12-31.csv` |
| 3 | Les deux séries sont-elles alignées **par date** ? | oui, 512 communes, 511 rendements |
| 4 | Les seuils ont-ils été publiés avant les chiffres ? | oui, [module 3 § 3.2](03-la-regle-ecrite-a-l-avance.md#32--la-règle-in-extenso) |
| 5 | L'IC de l'alpha est-il publié ? | oui, $[-49{,}4\ ;\ +48{,}9]\,\%$ |
| 6 | $r_f$ est-il annoncé ? | oui, $r_f = 0$ |
| 7 | Les vetos ont-ils été évalués **avant** les critères ? | oui, veto 3 mord |
| 8 | La phrase de qualification accompagne-t-elle le verdict ? | oui |

---

⬅️ [Module 3 — La règle écrite à l'avance](03-la-regle-ecrite-a-l-avance.md) ·
➡️ [Module 5 — La cadence d'application fait partie de la règle](05-la-cadence-fait-partie-de-la-regle.md)
