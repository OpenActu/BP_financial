# journal.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/done/experimentation/experience_6/journal.py`, étape par étape, dans
l'ordre du déroulement. Il fait autorité : toute évolution du script doit
d'abord être décrite ici.

Le **protocole** — la règle de l'expérience 4 à dix lignes et à achat
persistant, l'alpha officiel contre la référence à exposition appariée, les
frais jugés d'abord — est dans [`README.md`](README.md). Le moteur est celui de
l'[expérience 5](../experience_5/journal.md), dont ce miroir ne rappelle que ce
qui change.

## Rôle

Conduire mécaniquement le portefeuille de l'expérience 6, **rejouer la règle de
l'expérience 4 et vérifier qu'elle est retrouvée**, isoler l'effet de chacun
des deux changements de règle, puis tout remesurer avec l'appareil de
l'expérience 5.

| Piste | Ce que le moteur fait en plus de l'expérience 5 |
|---|---|
| **1 — les frais** | la persistance à l'achat ; les frais de chaque comptabilité en euros et en points de dotation, projetés puis réalisés ; l'effet de chaque changement sur les ordres et les frais |
| **2 — l'alpha séparé du bêta** | l'alpha **officiel** est l'écart à la référence à exposition appariée, avec son effet minimal détectable |
| **4 — plus de lignes** | dix lignes ; les quatre combinaisons lignes × persistance, et leurs écarts appariés |

> ⚠️ **Aucune décision n'est prise à la main.** Le seul texte rédigé à la main
> est dans [`actualites.md`](actualites.md) et [`chartiste.md`](chartiste.md),
> repris de l'expérience 5.

## Dépendances

Celles de l'expérience 5 : modules standard, `p_valeur_student()` importée
localement depuis `python/import_societe.py`, aucune bibliothèque de tracé,
aucun sous-processus.

## Invocation

```bash
python docs/done/experimentation/experience_6/journal.py
python docs/done/experimentation/experience_6/journal.py --figures
python docs/done/experimentation/experience_6/journal.py --markdown
python docs/done/experimentation/experience_6/journal.py --mois 2022-03
```

Arguments identiques à l'expérience 5 : `--figures`, `--markdown`, `--mois`,
`--repertoire`, `--quotes`. La dotation, le nombre de lignes et la persistance
sont des **constantes**.

## Les constantes

Reprises de l'expérience 5 sans changement : univers, séries, fenêtres,
`LONGUE`, `COURTE`, `TOP`, `K`, `VARIANTES`, `HORIZON`, `PAS_ECHANTILLON`,
`ETALONNAGE_PUBLIE`, coûts, `SPLITS_POSTERIEURS`, `SOCIETES`, `FIN_ETALONNAGE`,
`FIN_SEMESTRE`, `PHASES`, `SEUIL_PHASES`, `RISQUE`, `DATES_MIN`, les paramètres
des références simulées et du témoin, `REFERENCES_PUBLIEES`. Nouvelles ou
changées :

| Constante | Valeur | Rôle |
|---|---|---|
| `LIGNES` | `10` | **piste 4** |
| `PERSISTANCE` | `2` | **piste 1** : clôtures consécutives sous le bord bas exigées à l'achat |
| `COMBINAISONS` | `L5-P1`, `L10-P1`, `L5-P2`, `L10-P2` | les quatre couples (lignes, persistance) ; `L5-P1` est la règle de l'expérience 4, `L10-P2` celle de l'expérience 6 |
| `TE_DECLAREE` | `5.25` | **piste 2** : la tracking error projetée **contre la référence appariée** |
| `TE_TR39_PROJETEE` | `9.95` | la tracking error projetée contre `TR39`, pour mémoire |
| `CONTROLE` | `31` ordres · `10051.09` € | ce que `L5-P1` doit rendre sur 2022 |
| `PROJECTIONS_PUBLIEES` | les grandeurs de 2021 du README | confrontées au recalcul et au réalisé |
| `EMD_GRAPPES` | celles de l'expérience 5, plus `PERSISTANCE` | les EMD projetés par grappes |

`PERSISTANCE` ne peut valoir que 1 ou 2 : la persistance porte sur la clôture de
la décision et sur celle de la séance qui la précède.

---

## Déroulé d'exécution

### 1. L'univers, les séries, l'évaluation, le TOP 10

Repris de l'expérience 5 sans changement.

### 2. La persistance

`sous_bas_veille(ctx, ticker, jour)` prend la séance qui précède `jour` dans le
calendrier de `TR39`, lit l'évaluation de `ticker` à cette séance — dans le
contexte si elle y est, sinon par `evaluer()`, puisque la veille du 2020-12-31
n'est pas évaluée d'office — et rend vrai si elle n'est pas muette et que son
`ECART_S` est `< −K`. Le résultat est mis en cache.

`candidat(ctx, ticker, jour, persistance, avec_p20)` rend vrai si
`est_candidat()` l'est à `jour` **et**, quand `persistance` vaut 2, si
`sous_bas_veille()` l'est aussi. **Seule la condition de bande persiste** : le
TOP 10 et la pente courte se lisent le jour de la décision seulement.

`candidat()` avec les constantes du protocole remplace `est_candidat()` partout
où la règle de l'expérience 6 s'applique : la simulation, la colonne `CANDIDAT`
de `evaluations.csv` et de `top10.csv`, le verdict des figures, les épisodes.
`taux_regle()` garde `est_candidat()`, pour confronter les taux d'étalonnage
publiés par l'expérience 4 sous leur propre définition, et compte en plus les
candidats persistants.

### 3. La simulation

`simuler(ctx, decisions, seances, lignes, persistance, avec_p20)` est celle de
l'expérience 5, avec deux paramètres de plus : le nombre de créneaux vaut
`lignes`, et le filtre d'achat est `candidat()`. Elle est appelée **dix fois** :

| Comptabilité | Décisions | Lignes | Persistance | `avec_p20` |
|---|---|---|---|---|
| **le portefeuille** (`L10-P2`) | narrées, quotidiennes | 10 | 2 | oui |
| `L5-P1` — la règle de l'expérience 4 | narrées, quotidiennes | 5 | 1 | oui |
| `L10-P1` | narrées, quotidiennes | 10 | 1 | oui |
| `L5-P2` | narrées, quotidiennes | 5 | 2 | oui |
| `SANS-P20` | narrées, quotidiennes | 10 | 2 | non |
| `MENSUEL` | narrées, mensuelles | 10 | 2 | oui |
| projections 2021 | les six mêmes, sur 2021 | | | |

Les projections portent sur les décisions du 2020-12-31 au 2021-12-29.

### 4. Le contrôle de reproduction

`controler_reproduction()` est celui de l'expérience 5, appliqué à **`L5-P1`** :
ses ordres et ses valorisations doivent retrouver `../experience_4/ordres.csv` et
`../experience_4/portefeuille.csv`, et `CONTROLE`. Tout écart est une sortie 1.
C'est ce qui garantit que les deux changements de règle sont les seuls.

### 5. L'alpha officiel — piste 2

`reference_appariee()` est calculée sur le portefeuille. Le bilan définit :

- **alpha officiel** = base 100 du portefeuille − base 100 de la référence
  appariée, en fin d'année et mois par mois ;
- **son effet minimal détectable** = $1{,}96 \times$ la tracking error
  annualisée du portefeuille contre la référence appariée ;
- **l'écart brut** = portefeuille − `TR39`, décomposé en exposition et sélection.

Les bêtas semestriels, le témoin aléatoire et l'alpha de régression sont repris
de l'expérience 5.

### 6. Les frais — piste 1

`frais(resume)` rend, pour une comptabilité : ordres, achats, ventes, frais en
euros, frais en points de dotation, et **montant brut échangé** rapporté à
l'actif moyen. Il est appliqué aux six comptabilités de 2022 et aux six
projections de 2021.

### 7. Les quatre combinaisons — pistes 1 et 4

`ecart_apparie()` sur les couples :

| Écart | Ce qu'il isole |
|---|---|
| `L10-P2` − `L5-P2` | l'effet des **lignes**, à persistance 2 |
| `L10-P1` − `L5-P1` | l'effet des lignes, à persistance 1 |
| `L10-P2` − `L10-P1` | l'effet de la **persistance**, à dix lignes |
| `L5-P2` − `L5-P1` | l'effet de la persistance, à cinq lignes |
| `L10-P2` − `L5-P1` | les deux, contre la règle de l'expérience 4 |

Chacun avec la différence de base 100 en fin d'année, l'écart-type annualisé de
la différence, son effet minimal détectable, son bêta contre `TR39` et
l'écart-type du résidu. L'**interaction** est la différence des deux effets des
lignes.

### 8. Les issues — T1

Repris de l'expérience 5, avec une comparaison de plus dans `COMPARAISONS` :

| Élément | Population | Groupe testé | Témoin |
|---|---|---|---|
| `PERSISTANCE` | les candidats au sens de l'expérience 4 | la veille aussi sous le bord bas | les autres |

`issues()` ajoute le champ `PERSISTANT`. La famille de Holm compte **cinq**
comparaisons. Le verdict de l'expérience 4 n'existe pas pour `PERSISTANCE` : sa
survie s'écrit `—`.

### 9. La bande, le témoin, les projections

Repris de l'expérience 5 : références simulées et matrices (C1), témoin
aléatoire sur les positions du portefeuille (T2), confrontation des projections
publiées (T4) — pour les six comptabilités.

### 10. Les figures et les markdown

- **Figures de canal** reprises ; leur verdict est celui de `candidat()`.
- **Courbes du portefeuille** : le portefeuille, `L5-P1`, la référence appariée
  et `TR39`.
- **Journaux mensuels** : ceux de l'expérience 5, étiquetés « expérience 6 » ;
  le tableau du portefeuille porte `L5-P1`, la référence appariée et l'alpha
  officiel depuis janvier.

`bilan_annuel()` écrit `bilan-2022.md`, seize sections :

1. le compte — **alpha officiel** d'abord, contrôle de reproduction ;
2. mois par mois, avec la référence appariée et l'alpha officiel ;
3. les positions ;
4. le motif unique de vente et la durée des épisodes à l'achat ;
5. l'univers et la recevabilité ;
6. les taux d'étalonnage de l'expérience 4, recalculés ;
7. **les frais** — piste 1 ;
8. **l'alpha séparé du bêta** — piste 2 ;
9. **les lignes et la persistance** — les quatre combinaisons ;
10. les issues remesurées, `PERSISTANCE` comprise ;
11. la bande contre ses références ;
12. les fantômes `SANS-P20` et `MENSUEL` ;
13. la sensibilité ;
14. les trois conventions ;
15. le dimensionnement confronté ;
16. ce que l'expérience établit, et ce qu'elle n'établit pas.

Toute phrase conclusive est engendrée par la valeur qu'elle résume.

## Les fichiers écrits

Ceux de l'expérience 5, sauf que `fantome.csv` porte `SANS-P20` à dix lignes et
que la comparaison à l'expérience 3 n'est plus faite. S'ajoute :

| Fichier | Colonnes |
|---|---|
| `combinaisons.csv` | `DATE, L5-P1, L10-P1, L5-P2, L10-P2, APPARIEE, REFERENCE100` — bases 100 |

## Codes de sortie

Ceux de l'expérience 5. `L5-P1` non reproduit est une sortie 1.

## Cas limites

Ceux de l'expérience 5, plus :

- **Une veille muette** : la valeur n'est pas persistante, donc pas candidate.
- **La veille du 2020-12-31** : évaluée à la demande par `evaluer()`, sur les
  seules séances antérieures.
- **Plus de créneaux que de candidats** : les espèces restent oisives ; la part
  investie baisse, et le bilan le publie.
