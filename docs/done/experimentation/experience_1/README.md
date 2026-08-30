# Expérience 1 — un portefeuille de 10 000 € sur l'année 2022

> *« Mon approche fonctionne non pas en prédisant les événements, mais en
> permettant de les comprendre au fur et à mesure qu'ils se déroulent. »*
> — George Soros, **L'Alchimie de la finance**, 1987

Ce répertoire consigne, mois par mois, la conduite d'un portefeuille doté de
**10 000 €** au 3 janvier 2022 et suivi jusqu'au 30 décembre 2022.

La forme est empruntée à la deuxième partie de *L'Alchimie de la finance* : le
**journal en temps réel**. Soros y tient, d'août 1985 à novembre 1986, un carnet
où il écrit ses hypothèses **avant** de les jouer, puis constate. La valeur du
procédé ne tient pas aux gains obtenus ; elle tient à ce que la thèse est écrite
avant le résultat, et qu'on ne peut plus la réécrire après coup.

---

## ⚠️ Ce que cette expérience peut, et ne peut pas, démontrer

L'année 2022 est **passée**. Quiconque écrit aujourd'hui « j'aurais acheté
TotalEnergies en janvier » ne démontre rien du tout : il rejoue un match dont il
connaît le score. Ce piège a un nom dans le cours — c'est le premier des
[cinq pièges de l'alpha](../../../raw/concept/semestre4/alpha/04-cinq-pieges.md).

Une seule parade existe, et elle est appliquée ici sans exception :

> **Aucune décision de cette expérience n'est prise à la main.**
> Toutes découlent d'un **score écrit à l'avance**, calculé mécaniquement par
> [`journal.py`](journal.py) à partir des cinq critères de la règle du dépôt.
> Le score, les seuils, l'univers et le calendrier sont fixés avant la première
> séance et **ne changent jamais** en cours d'année.

Ce que l'expérience mesure est donc : *que rend cette règle-là, sur cet
univers-là, cette année-là, coûts compris ?* Ce qu'elle ne mesure pas, et ne
prétend pas mesurer : le talent d'un gérant, ni ce que rendrait la règle une
autre année. **Un an, c'est un point.** Le cours de finance montre qu'il faudrait
des siècles pour distinguer un rendement moyen de zéro ; douze mois ne
distinguent rien.

Ce n'est **pas** un conseil en investissement. C'est la sortie d'une règle,
consignée.

---

## Le protocole, déclaré avant la première séance

### La dotation et les contraintes

| | |
|---|---|
| Dotation | **10 000 €**, en espèces, au 3 janvier 2022 |
| Lignes détenues | **5 au maximum**, simultanément |
| Levier | **aucun** |
| Couverture | **aucune** |
| Vente à découvert | **aucune** |
| Fin de l'expérience | 30 décembre 2022, dernière séance de l'année |

Le solde non investi dort en espèces, sans rémunération. En 2022 le taux de la
facilité de dépôt de la BCE passe de −0,50 % à +2,00 % : rémunérer les espèces
supposerait de déclarer un support et un calendrier de versement, ce qui
ajouterait une convention pour un effet de l'ordre de quelques euros. On ne le
fait pas, et on le dit.

### L'univers, fixé une fois pour toutes

Douze valeurs du CAC 40, choisies pour couvrir des secteurs distincts, arrêtées
**avant** de regarder quoi que ce soit de 2022 et jamais modifiées ensuite :

| Ticker | Société | Secteur |
|---|---|---|
| `AIR.PA` | Airbus | aéronautique |
| `MC.PA` | LVMH | luxe |
| `OR.PA` | L'Oréal | cosmétiques |
| `SAN.PA` | Sanofi | santé |
| `BNP.PA` | BNP Paribas | banque |
| `TTE.PA` | TotalEnergies | énergie |
| `SU.PA` | Schneider Electric | équipement électrique |
| `AI.PA` | Air Liquide | gaz industriels |
| `DG.PA` | Vinci | concessions et construction |
| `CAP.PA` | Capgemini | services numériques |
| `RI.PA` | Pernod Ricard | spiritueux |
| `ORA.PA` | Orange | télécommunications |

> ⚠️ **Biais du survivant, entier.** Ces douze sociétés sont au CAC 40
> aujourd'hui, et l'étaient déjà en 2022. Un univers constitué en 2021 aurait pu
> contenir des valeurs sorties de l'indice depuis. Le biais joue en faveur de
> l'expérience et n'est pas corrigé ; il est signalé.

### Le calendrier — la cadence fait partie de la règle

La cadence est **mensuelle**, déclarée avant tout, parce que
[le module 5 du cours de trading](../../../raw/concept/semestre4/trading/05-la-cadence-fait-partie-de-la-regle.md)
montre qu'une même règle rend des résultats opposés selon qu'on l'évalue chaque
jour ou chaque mois. La cadence n'est pas un détail d'exécution : c'est un degré
de liberté, et un degré de liberté non déclaré est un degré de liberté qu'on
s'autorisera après coup.

- **Date de décision** : la **dernière séance du mois précédent**. Le classement,
  le score et les ordres en découlent, à partir des seules séances jusqu'à cette
  date incluse.
- **Date d'exécution** : la **première séance du mois**, au cours d'**ouverture**.

On ne peut pas décider après la clôture et être servi à cette clôture. Le module
[Cas pratique](../../../raw/concept/semestre4/trading/06-cas-pratique.md) chiffre
ce que coûte cet écart d'une séance : il y renversait le signe du résultat.

### Le score, en cinq composantes

À chaque date de décision, les douze valeurs reçoivent un score, somme de cinq
petits entiers tirés des cinq critères de
[la règle du module 3](../../../raw/concept/semestre4/trading/03-la-regle-ecrite-a-l-avance.md).
Chaque composante est calculée par
[`python/generer_graph_decision.py`](../../../../python/generer_graph_decision.md),
jamais réimplémentée.

| | Critère | Valeurs possibles |
|---|---|---|
| `s1` | tendance longue `TEND_120` | `+2` / `0` / `−2` |
| `s2` | tendance courte `TEND_20` | `+1` / `0` / `−1` |
| `s3` | position dans l'encadrement actif | `+1` si ≥ 50 %, `0` de 20 à 50 %, `−1` si < 20 % |
| `s4` | momentum 12-1 | `+2` si > +10 %, `+1` si 0 à +10 %, `−1` si −10 à 0, `−2` si < −10 % |
| `s5` | alpha annualisé contre la référence | `+1` si l'IC95 est entièrement positif, `−1` s'il est entièrement négatif, `0` sinon |

**Score = s1 + s2 + s3 + s4 + s5**, entre `−7` et `+7`. Départage : score, puis
momentum, puis ordre alphabétique — le classement est déterministe.

> La colonne `s5` vaut **`0` aux 144 évaluations de l'année**. Ce n'est pas un
> bug : l'IC95 de l'alpha contient zéro à chaque fois. C'est exactement ce que
> le dépôt répète — l'alpha d'une valeur ne se mesure pas sur quelques mois.
> La composante est conservée telle quelle, à titre de constat.

### Les règles d'entrée et de sortie

- **Entrée** : classé au **rang 5 ou mieux**, score **strictement positif**, pas
  déjà détenu, et une place libre parmi les cinq.
- **Sortie** : rang **au-delà de 7**, ou score **≤ −3**.
- **Hystérésis** : on entre à 5, on sort à 7. Sans cet écart, une valeur qui
  oscille entre les rangs 5 et 6 paierait un aller-retour chaque mois — 0,53 %,
  soit plus de 6 % par an pour une seule ligne indécise.
- **Aucun rebalancement** : on n'achète que les entrées, on ne vend que les
  sorties. Les poids dérivent, et c'est voulu : rééquilibrer tous les mois
  coûterait des frais pour un effet que douze mois ne permettent pas de mesurer.
- **Répartition** : les espèces disponibles après les ventes sont réparties à
  parts égales entre les valeurs qui entrent.
- **Titres entiers.** Le reliquat retourne aux espèces. C'est ce qui explique
  qu'une ligne LVMH à 669 € l'unité laisse plusieurs centaines d'euros oisives.

### Les coûts, appliqués à chaque ordre

Barème de [`python/couts_transaction.py`](../../../../python/couts_transaction.md) :

| | Achat | Vente |
|---|---|---|
| Courtage | 0,100 % | 0,100 % |
| Demi-spread | 0,015 % | 0,015 % |
| Taxe sur les transactions financières | 0,300 % | — |
| **Total** | **0,415 %** | **0,115 %** |

Soit **0,530 % l'aller-retour** — et **0,230 %** pour Airbus, immatriculée aux
Pays-Bas et donc hors du champ de la TTF française.

### La référence, et pourquoi ce n'est pas le CAC 40

La performance est mesurée contre **`TR12`**, un indice **en rendement total**
construit par
[`python/construire_indice_total.py`](../../../../python/construire_indice_total.md)
sur les douze mêmes valeurs, équipondérées.

C'est la conséquence directe de l'avertissement central du dépôt : la colonne
`Close` de `yfinance` est **ajustée des dividendes**, alors que `^FCHI` est un
indice **nu**. Comparer les deux fabrique de l'alpha à partir de rien. Sur cette
seule année 2022, l'écart de convention vaut **6,36 points** :

```
^FCHI (nu)          -10,30 %
TR12 (rdt total)     -3,94 %
                    ────────
ecart                +6,36 pt   ← entierement du a la convention
```

Se comparer au CAC 40 nu aurait transformé un retard de 4,5 points en une avance
de 1,9 point. **Le choix de la référence renverse le verdict** : il devait donc
être déclaré, pas deviné.

---

## Ce que contient chaque markdown mensuel

Douze fichiers, [`rapports/2022-01.md`](rapports/2022-01.md) à
[`rapports/2022-12.md`](rapports/2022-12.md). Chacun est bâti sur le même plan :

1. **Les actualités du mois précédent** — le contexte macroéconomique et
   sectoriel tel qu'il était connu à la date de décision.
2. **L'exposition héritée** — pour chaque ligne détenue : date d'achat, plus ou
   moins-value en %, alpha du mois écoulé, alpha global depuis l'achat.
3. **La valeur du portefeuille** rapportée au 3 janvier 2022, base 100.
4. **Le graphique** de l'évolution, du 3 janvier à la fin du mois courant.
5. **L'étude chartiste** — une note de perspective de cinq lignes au plus par
   société, rédigée par l'agent [`chartiste`](../../../../.claude/agents/chartiste.md)
   sans aucune séance postérieure à la date de décision.
6. **Le classement** des douze valeurs, de la plus intéressante à détenir à celle
   qu'il faut fuir, avec le détail des cinq composantes.
7. **Les ordres exécutés**, chacun avec son motif chiffré.

> Le graphique du fichier de mars s'arrête fin mars, et le classement de mars a
> été calculé fin février. Le premier **rend compte**, le second **décide** :
> aucune décision ne s'appuie sur une séance postérieure à sa date de décision,
> échelles de graphique comprises.

---

## Le résultat

```
Dotation                10 000,00 EUR au 2022-01-03
Valeur finale            9 156,26 EUR
Performance                  -8,44 %
TR12                         -3,94 %
Alpha sur l'annee            -4,50 pt

Ordres                  23 (14 achats, 9 ventes)
Frais cumules           116,66 EUR, soit 1,17 % de la dotation
Repli maximal               -17,89 %  (creux au 2022-09-29)
```

**La règle a perdu 4,5 points contre sa propre référence.** Elle a fait moins
bien que détenir les douze valeurs à parts égales sans rien faire — et 1,17 point
de ce retard est payé en frais purs, pour vingt-trois ordres.

C'est un résultat, pas un échec de l'expérience. Il est cohérent avec ce que le
dépôt démontre ailleurs : une règle de suivi de tendance qui commute sur douze
dates paie ses commutations, et douze mois ne suffisent jamais à établir qu'elle
les rentabilise.

> Le contrefactuel le chiffre exactement : **garder le portefeuille de janvier
> jusqu'au 30 décembre, sans un seul arbitrage, aurait rendu 95,96 au lieu de
> 91,56** — les vingt-deux ordres passés ensuite ont coûté 4,40 points.

**[→ Le bilan complet de l'année](bilan-2022.md)** : mois par mois, position par
position, les trois conventions de référence, et ce que l'expérience établit ou
n'établit pas.

---

## Les fichiers

| Fichier | Contenu |
|---|---|
| [`bilan-2022.md`](bilan-2022.md) | **le bilan de l'année**, entièrement calculé |
| `rapports/2022-01.md` … `2022-12.md` | les douze journaux mensuels |
| [`journal.py`](journal.py) | le moteur : classement, ordres, comptabilité, graphiques, rapports |
| [`journal.md`](journal.md) | son miroir d'exécution, au sens de la règle du dépôt |
| [`actualites.md`](actualites.md) | le contexte macroéconomique de chaque mois, rédigé à la main |
| [`chartiste.md`](chartiste.md) | les 144 notes de perspective, rédigées par l'agent `chartiste` |
| `criteres.csv` | les 144 évaluations de la règle (12 valeurs × 12 dates) |
| `classement.csv` | le classement et les cinq composantes, à chaque date |
| `ordres.csv` | les 23 ordres, avec prix, frais et motif |
| `portefeuille.csv` | la valeur quotidienne, en euros et en base 100 |
| `graphiques/` | les douze SVG, janvier → fin du mois |

### Reproduire l'expérience

```bash
# 1. les series, avec deux ans d'amorce avant 2022
for t in AIR.PA MC.PA OR.PA SAN.PA BNP.PA TTE.PA SU.PA AI.PA DG.PA CAP.PA RI.PA ORA.PA; do
  python python/import_societe.py "$t" --debut 2020-01-02 --fin 2023-01-01
done
python python/import_societe.py "^FCHI" --debut 2020-01-02 --fin 2023-01-01

# 2. la reference en rendement total
python python/construire_indice_total.py AIR.PA MC.PA OR.PA SAN.PA BNP.PA TTE.PA \
    SU.PA AI.PA DG.PA CAP.PA RI.PA ORA.PA \
    --debut 2020-01-02 --fin 2022-12-30 --nom TR12

# 3. le journal — la collecte prend deux a trois minutes
python docs/done/experimentation/experience_1/journal.py --collecter
python docs/done/experimentation/experience_1/journal.py --markdown
python docs/done/experimentation/experience_1/journal.py --mois 2022-03
```

Le moteur est déterministe : relancé, il réécrit exactement les mêmes fichiers.

---

## Ce que l'expérience ne fait pas

- **Aucun levier, aucune couverture.** Le
  [module 4 du cours de finance](../../../raw/concept/semestre4/finance/04-levier-optimal-et-drag.md)
  montre que le levier optimal dépend d'un rendement espéré qu'on ne sait pas
  mesurer ; [`python/dimensionner_exposition.py`](../../../../python/dimensionner_exposition.md)
  le confirme sur données réelles. Une expérience d'un an n'a rien à en dire.
- **Aucun ordre stop.** Le
  [module 7 du cours de trading](../../../raw/concept/semestre4/trading/07-le-stop-une-sortie-sans-verdict.md)
  mesure qu'un stop suiveur à −10 % aurait coûté 93 points sur cinq ans dans le
  cas étudié. En ajouter un ici demanderait de déclarer une variante de plus,
  sans moyen de trancher entre elles sur douze mois.
- **Aucun fondamental.** Le score est entièrement chartiste. Les ratios
  point-in-time existent dans le dépôt
  ([`reconstituer_fondamentaux.py`](../../../../python/reconstituer_fondamentaux.md))
  et feraient une expérience 2 légitime.
- **Aucune prédiction.** Les notes de perspective décrivent une configuration
  observable à une date, jamais un cours à venir.

---

## Pour aller plus loin

- [`docs/raw/planning.md`](../../../raw/planning.md) — le parcours complet
- [Semestre 4 · trading](../../../raw/concept/semestre4/trading/README.md) — la règle et ses pièges
- [Semestre 4 · alpha](../../../raw/concept/semestre4/alpha/README.md) — pourquoi l'alpha se mesure si mal
- [Semestre 4 · finance](../../../raw/concept/semestre4/finance/README.md) — levier, marge, couverture
