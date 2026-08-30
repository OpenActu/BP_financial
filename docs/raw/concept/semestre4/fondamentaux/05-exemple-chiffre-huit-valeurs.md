# Module 5 — Exemple chiffré : huit valeurs du CAC 40

**Prérequis :** les modules 1 à 4.
**Ce qu'on établit ici :** rien de nouveau — les quatre modules appliqués ligne à ligne à un tableau réel, jusqu'à ce qu'on puisse dire de chaque colonne ce qu'elle permet et ce qu'elle interdit.

---

## 5.1 — La commande et le tableau

```bash
python python/import_fondamentaux.py AIR.PA MC.PA OR.PA SAN.PA TTE.PA BNP.PA SU.PA ORA.PA
```

Extrait des 33 colonnes produites, au **30 août 2026** :

| | Secteur | PER | P/B | VE/EBITDA | Rdt FCF | ROE | Marge nette | Dette/EBITDA | VE/Capi |
|---|---|---|---|---|---|---|---|---|---|
| **AIR.PA** | Industrie | 27,04 | 6,21 | 17,99 | 1,95 % | 23,19 % | 7,71 % | 1,59 | 1,008 |
| **MC.PA** | Conso. cyclique | 20,90 | 3,32 | 12,59 | 5,11 % | 16,59 % | 13,66 % | 1,85 | 1,118 |
| **OR.PA** | Conso. défensive | 32,98 | 6,11 | 21,21 | 3,09 % | 19,41 % | 13,90 % | 1,61 | 1,061 |
| **SAN.PA** | Santé | 23,84 | 1,34 | 8,13 | 6,81 % | 5,71 % | 8,09 % | 1,74 | 1,190 |
| **TTE.PA** | Énergie | 10,90 | 1,49 | 5,04 | 8,19 % | 14,48 % | 9,08 % | 1,59 | 1,209 |
| **BNP.PA** | Banque | 8,87 | 0,94 | — | — | 10,48 % | 26,49 % | — | — |
| **SU.PA** | Industrie | 35,58 | 6,94 | 21,86 | 3,17 % | 18,62 % | 11,27 % | 2,44 | 1,098 |
| **ORA.PA** | Télécoms | 10,27 | 1,27 | 7,35 | 15,83 % | 14,16 % | 9,98 % | 4,69 | 2,204 |

## 5.2 — Ce qu'on lit d'abord : les cases vides

Trois cellules vides, toutes sur BNP.PA, toutes **correctes**
([module 3 § 3.5](03-ce-que-la-comptabilite-laisse-au-choix.md)) : une banque n'a
ni valeur d'entreprise, ni EBITDA, ni flux de trésorerie disponible au sens où
ces grandeurs sont définies pour une industrielle.

Et une cellule **remplie** qui est plus dangereuse que les trois vides : la marge
nette de $26{,}49\,\%$, calculée sur un agrégat de produits bancaires. Elle
s'affiche, elle est deux fois supérieure à celle de LVMH, et elle ne se compare à
rien dans cette colonne.

> 🔑 **Première lecture d'un tableau de fondamentaux : chercher ce qui manque, et
> se demander pourquoi.** Une absence justifiée est une information sur la nature
> de l'entreprise. Une présence injustifiée est un piège.

## 5.3 — La colonne qui trie vraiment : VE/Capi

Avant tout classement, on regarde ce que le PER cache
([module 1 § 1.2](01-de-quoi-un-ratio-est-le-rapport.md)) :

- **AIR.PA à 1,008** — dette nette quasi nulle. PER et VE/EBITDA racontent ici la
  même histoire, et on peut les lire ensemble.
- **ORA.PA à 2,204** — la dette nette dépasse la valeur des actions. Tout
  jugement fondé sur son PER est faussé.

Le renversement du module 1 se relit sur ce tableau : Orange affiche le **PER le
plus bas des sept valeurs non financières** (10,27, devant TotalEnergies à
10,90), mais repasse **derrière** TotalEnergies sur VE/EBITDA (7,35 contre 5,04).
Le classement dépend entièrement du numérateur choisi.

## 5.4 — Lire chaque ratio comme une hypothèse

En appliquant le [module 4](04-un-ratio-n-existe-que-relatif.md), $r = 8\,\%$,
payout 100 % :

| | $g$ implicite | À confronter à |
|---|---|---|
| SU.PA | +5,19 % | une croissance perpétuelle supérieure au PIB nominal |
| OR.PA | +4,97 % | idem |
| AIR.PA | +4,30 % | un carnet de commandes long, mais cyclique |
| BNP.PA | −3,27 % | un déclin perpétuel — ou un $r$ bien supérieur à 8 % pour une banque |

La dernière ligne est la plus instructive. Un $g$ implicite de $-3{,}3\,\%$ est
peu crédible ; l'explication la plus simple est que $r = 8\,\%$ est **faux pour
une banque**, dont le coût des fonds propres est structurellement plus élevé.
C'est le modèle qu'il faut corriger, pas l'entreprise qu'il faut juger.

## 5.5 — La seule comparaison solide

Deux industrielles, même secteur, ratios homogènes :

| | PER | P/B | VE/EBITDA | Rdt FCF | ROE | Dette/EBITDA |
|---|---|---|---|---|---|---|
| **AIR.PA** | 27,04 | 6,21 | 17,99 | 1,95 % | **23,19 %** | **1,59** |
| **SU.PA** | 35,58 | 6,94 | 21,86 | 3,17 % | 18,62 % | 2,44 |

Schneider se paie plus cher sur **les trois multiples** — PER, P/B, VE/EBITDA —
avec un ROE inférieur de 4,6 points et une dette rapportée à l'EBITDA supérieure
de 53 %.

Ce que cela autorise à dire : *au 30 août 2026, sur ces six mesures, le marché
valorise Schneider plus généreusement qu'Airbus alors que les comptes publiés
montrent une rentabilité moindre et un endettement supérieur.*

Ce que cela n'autorise **pas** à dire :

- que Schneider est surévaluée — le marché peut anticiper une croissance
  supérieure, que ces colonnes ne mesurent pas ;
- qu'Airbus est un meilleur achat — aucun horizon, aucun risque, aucun coût de
  transaction n'entre dans ce tableau ;
- que l'écart va se refermer — rien ici ne porte sur l'avenir ;
- que la même lecture valait il y a un an, ou vaudra dans un mois
  ([module 2](02-les-quatre-dates-d-un-ratio.md)).

Noter aussi que l'écart de rendement du FCF joue en sens inverse des multiples :
Airbus, moins chère sur les trois multiples, convertit **moins** bien son bénéfice en
trésorerie ($1{,}95\,\%$ contre $3{,}17\,\%$). Un tableau de fondamentaux ne
converge presque jamais vers un classement unique — et lorsqu'il paraît le faire,
c'est en général qu'on n'a regardé que les colonnes qui allaient dans le même
sens.

## 5.6 — Ce que ce module ne couvre pas

- **Aucune valorisation absolue.** Rien ici ne dit ce que vaut une entreprise ;
  tout est comparatif et instantané.
- **Aucun historique**, donc aucune tendance de marge, de dette ou de ROE — qui
  seraient pourtant plus informatives que leur niveau.
- **Aucun élément qualitatif** : gouvernance, concurrence, réglementation,
  contentieux, concentration client. Ces facteurs décident souvent davantage que
  les ratios.
- **Aucun conseil.** Ce module lit des colonnes ; il ne recommande ni achat, ni
  vente, ni conservation, et ne tient compte d'aucune situation personnelle.

---

⬅️ [Module 4 — Un ratio n'existe que relatif](04-un-ratio-n-existe-que-relatif.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md) ·
📘 [README du cours](README.md)
