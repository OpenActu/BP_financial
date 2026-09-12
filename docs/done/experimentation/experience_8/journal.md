# journal.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/done/experimentation/experience_8/journal.py`, étape par étape, dans
l'ordre du déroulement. Il fait autorité : toute évolution du script doit
d'abord être décrite ici.

Le **protocole** — les six règles, la dé-ajustement des divisions, les deux
références, les issues déclarées — est dans [`README.md`](README.md).

## Rôle

Conduire mécaniquement un portefeuille de 10 000 € sur **Air Liquide seule**, à
raison d'**une décision par semaine**, du 2022-01-03 au 2026-09-10 : acheter 10 %
sous le bord bas quand la pente courte ne baisse pas, acheter 10 % de plus si le
cours passe 1 s sous ce prix d'achat, renforcer une fois de 20 %, et vendre au
bord haut.

> 🔑 **La règle 4 achète, elle ne coupe pas.** C'est l'inverse de l'ordre stop que
> l'[analyse des pertes de l'expérience 3](../experience_3/pistes-pertes.md) avait
> réfuté. **La règle 5 est donc la seule sortie** : le moteur doit publier ce que
> cela coûte quand une position ne revient jamais dans sa bande.

Le moteur ne reprend **rien** des expériences 4 à 6 en matière d'univers, de
classement ou de TOP : la règle 1 les supprime. Il en reprend les conventions de
bande, de coûts, d'exécution à l'ouverture, et la référence à exposition appariée.

> ⚠️ **Aucune décision n'est prise à la main, et aucun texte n'est rédigé à la
> main.** Il n'y a ni `actualites.md` ni `chartiste.md` : tous les mots des
> journaux sont engendrés.

## Dépendances

- Modules standard : `argparse`, `csv`, `datetime`, `math`, `statistics`, `sys`,
  `pathlib`.
- `p_valeur_student()` de [`python/import_societe.py`](../../../../python/import_societe.md),
  importée **localement** dans `p_bilaterale()` après ajout de `python/` au
  chemin — le dépôt n'a pas de structure de paquet. Cet import charge `yfinance` ;
  aucune fonction réseau n'est appelée.
- Aucune bibliothèque de tracé : les SVG sont écrits à la main.

## Invocation

```bash
python docs/done/experimentation/experience_8/journal.py
python docs/done/experimentation/experience_8/journal.py --figures
python docs/done/experimentation/experience_8/journal.py --markdown
python docs/done/experimentation/experience_8/journal.py --annee 2023
```

| Argument | Défaut | Rôle |
|---|---|---|
| `--figures` | — | écrit les figures de canal |
| `--markdown` | — | écrit les figures, les journaux annuels, les courbes et le bilan |
| `--annee` | — | n'affiche en console que cette année (`AAAA`) |
| `--repertoire` | le répertoire du script | où lire et écrire |
| `--quotes` | `docs/raw/data/quotes` | où est la série |

La dotation, les parts d'achat et les seuils sont des **constantes** : ce sont les
six règles, pas des réglages. `--annee` hors de la fenêtre jouée : sortie **1**.

## Les constantes déclarées

| Constante | Valeur | Rôle |
|---|---|---|
| `VALEUR` | `AI.PA` | règle 1 : l'isolation |
| `SERIE` | `AI_PA_2019-01-02_2026-09-11.csv` | la plage déclarée, jamais devinée par glob |
| `DOTATION` | `10000.0` | |
| `PART_ACHAT` · `PART_RENFORT` | `0.10` · `0.20` | règles 3 et 4 · règle 6 |
| `DEBUT_NARREE` · `FIN_ETALONNAGE` | `2022-01-03` · `2021-12-31` | les deux fenêtres |
| `LONGUE` · `COURTE` · `K` | `120` · `20` · `1.0` | les bandes |
| `HORIZON` · `PAS_ECHANTILLON` | `20` séances · `4` décisions | les issues sans chevauchement |
| `COURTAGE` · `SPREAD` · `TTF` | `0.10` · `0.015` · `0.30` | Air Liquide n'est pas exemptée de TTF |
| `VARIANTES` | `sans règle 4`, `sans règle 6`, `ni l'une ni l'autre` | elles ne décident rien |
| `ETALONNAGE_PUBLIE` | les nombres publiés au README | confrontés au recalcul, un par un |
| `Z95` | `1.96` | |

---

## Déroulé d'exécution

### 1. La lecture de la série, et la dé-ajustement

`charger()` lit le CSV et rend trois choses : la liste ordonnée des séances, un
dictionnaire par jour — `Open`, `High`, `Low`, `Close` et les huit colonnes
glissantes —, et la liste des **divisions** lues dans `Stock Splits`. Une ligne
sans `Close` est ignorée : la dernière du fichier, encore incomplète, l'est.

`facteur(jour)` rend le produit des divisions **strictement postérieures** à
`jour`. `reel(jour, champ) = colonne × facteur(jour)` donne le cours réellement
coté ce jour-là.

> 🔑 **La convention d'unités, et elle est la clé du moteur.** La **règle** se lit
> entièrement sur la série **ajustée** — bandes, écarts, seuil de la règle 4 —
> parce que tout y est invariant d'échelle. Les **quantités, les espèces et la
> valorisation** se calculent sur les cours **réels**. Mélanger les deux dans une
> même comparaison serait une faute ; le moteur ne convertit qu'au moment de
> passer un ordre ou de valoriser.

### 2. L'évaluation

`evaluer(jour)` rend, en unités ajustées, ou `None` si une colonne manque, si une
variance est nulle ou si $1-\texttt{CORR\_120}^2$ ne l'est pas strictement :

| Champ | Formule |
|---|---|
| `s120` | $\sqrt{\tfrac{120}{118}\,\texttt{VAR\_120}\,(1-\texttt{CORR\_120}^2)}$ |
| `ecart` | $(\texttt{Close} - \texttt{VAL\_120})/s_{120}$ |
| `taux120` | $100\,\texttt{CORR\_120}\sqrt{\texttt{VAR\_120}/V_T(120)}\,/\,\texttt{E\_120}$ |
| `taux20` | la même chose sur la fenêtre de 20 séances |

La première évaluation possible est celle du **2019-06-21**.

### 3. Le calendrier hebdomadaire

`decisions_hebdomadaires(debut, fin)` rend la **dernière séance évaluable de
chaque semaine civile** — clé `(année ISO, semaine ISO)` — dans la fenêtre. La
séance d'exécution est la **suivante dans le calendrier**, jamais la même.

### 4. La simulation

`simuler(debut, fin, avec_r4, avec_r6)` parcourt les séances dans l'ordre. À
chaque séance `jour`, dont la veille est `veille` :

1. **Attributions.** Si `jour` porte une division, la quantité détenue devient
   `int(titres × ratio)` ; le reliquat fractionnaire est perdu, et c'est déclaré.
2. **Si `veille` est une décision hebdomadaire évaluable**, les signaux sont
   collectés dans cet ordre :
   - **vente** — règle 5 — si une position est ouverte et `ecart > K` ; elle
     exclut tout achat ce jour-là, les conditions étant incompatibles ;
   - **achat** — règle 3 — si aucune position n'est ouverte, `ecart < −K` et
     `taux20 ≥ 0` ;
   - **règle 4** — si une position est ouverte, qu'elle n'a pas déjà été
     complétée à ce titre, et que la **clôture ajustée** est sous le seuil figé ;
   - **règle 6** — si une position est ouverte, qu'elle n'a pas déjà été
     renforcée, que `veille` est la décision **immédiatement suivante** de celle
     de l'achat, et que `ecart < −K` et `taux20 ≥ 0`.

   Les règles 4 et 6 peuvent être remplies **la même semaine** : les deux ordres
   sont alors passés, dans cet ordre, et **tous deux dimensionnés sur la même
   valeur de portefeuille** — celle de la clôture de `veille` —, sans composition.
3. **Exécution** à l'**ouverture réelle** de `jour`. La quantité vaut
   `int(montant // (prix × (1 + taux_achat)))` ; nulle, l'ordre est annulé et la
   séance est comptée comme un signal non exécuté.
4. **Armement du seuil de la règle 4**, au seul achat de la règle 3 :
   `seuil = clôture ajustée de la décision − s120 de la décision`, **figé** pour
   toute la vie de la position. Ni la règle 4 ni la règle 6 ne le déplacent.
5. **Valorisation** à la clôture réelle de `jour` : espèces, titres, total.

Une **position** agrège ses tranches : quantité, brut, frais, montant investi,
nombre de tranches, seuil, dates. Son **prix d'achat** publié est le prix
**moyen** des tranches, et sa contribution est `reçu − investi`, frais des deux
sens compris.

`simuler()` est appelée **quatre fois** sur chaque fenêtre : la règle déclarée,
puis les trois variantes — sans la règle 4, sans la règle 6, sans les deux.
**Seule la première engage des euros.**

### 5. Les deux références

- `detention(debut, fin)` : tout investi à l'ouverture de la deuxième séance de
  la fenêtre, gardé jusqu'au bout, attributions créditées, mêmes coûts à l'achat.
- `appariee(valeurs, reference, seances)` : la détention, détenue dans la
  proportion où le portefeuille l'était **la veille** —
  $B_d = B_{d-1}(1 + w_{d-1} R^{\text{det}}_d)$ avec
  $w_{d-1} = \text{titres}_{d-1}/\text{total}_{d-1}$.

**L'alpha officiel** est l'écart des bases 100 entre le portefeuille et la
référence appariée. L'**écart brut** est celui à la détention continue.
`ecart_type(a, b)` rend l'écart-type annualisé de la différence des rendements
quotidiens ; l'effet minimal détectable vaut `Z95 ×` cet écart-type.

### 6. Les issues déclarées

`issues(decisions, borne)` rend une ligne par décision hebdomadaire : `SOUS_BAS`,
`TAUX_20_POSITIF`, `AU_DESSUS_HAUT`, et `RENDEMENT_20` — le rendement de la
clôture ajustée sur les `HORIZON` séances suivantes, en points, **vide** si
l'horizon dépasse la borne.

> 🔑 **Un rendement, et non un excédent.** Sur une valeur unique, l'excédent
> contre la détention continue de cette même valeur serait identiquement nul. Ce
> sont les **groupes de décisions** qui se comparent, pas la valeur à un indice.

`comparer(lignes, population, groupe)` ne retient qu'**une décision sur
`PAS_ECHANTILLON`**, pour que deux observations ne partagent aucune séance, et
rend effectifs, moyennes, différence, et l'intervalle de Student à `n − 1` degrés
de liberté par `p_bilaterale()`. Les trois comparaisons déclarées sont celles du
README. Une comparaison dont un groupe compte moins de deux observations est
**non mesurable**.

### 7. Ce que coûte l'absence de sortie en perte

Publié par le bilan, puisque la règle 5 est la seule sortie :

- les **lignes jamais revendues** à la dernière séance, avec leur moins-value
  latente et leur durée ;
- le **repli maximal** de chaque position entre son premier achat et sa sortie,
  en clôture et sur le `Low`, rapporté à son prix moyen ;
- la **durée** de chaque détention, et le nombre de tranches.

### 8. Ce qu'ajoutent les règles 4 et 6

Il se lit dans la **comparaison des variantes**, non dans un contrefactuel
inventé : chaque variante est le même portefeuille, au même calendrier, privé
d'une règle. Le bilan publie, pour les quatre, la base 100, l'alpha officiel, les
ordres, les frais, la part investie moyenne et son maximum, et l'écart apparié à
la règle déclarée avec son effet minimal détectable.

### 9. La confrontation de l'étalonnage

`taux(fenetre)` recalcule sur 2019-2021 les nombres publiés au README — bases,
alphas, ordres, frais, parts investies et maximums des quatre variantes, comptes
de déclenchement, positions et tranches — et les confronte à `ETALONNAGE_PUBLIE`.
Un écart imprime `ECART ETALONNAGE` en console et une croix au bilan ; le README
n'est pas corrigé après coup.

### 10. Les figures

- `figure_canal(chemin, jour)` : les 120 dernières clôtures **ajustées**, la
  droite sur 120 séances et sa bande ± 1 s, la droite sur 20 séances et son
  enveloppe des résidus, la clôture du jour pointée, le **seuil de la règle 4**
  en vigueur s'il y en a un, et une ligne portant écart, `TAUX_20` et verdict.
  Écrite pour **chaque décision qui produit un ordre** et pour **chaque dernière
  séance d'année**.
- `svg_portefeuille(chemin, annee)` : le portefeuille, la référence appariée et
  la détention continue, en base 100, du début de la fenêtre jouée à la fin de
  l'année, avec un trait vertical à chaque exécution.

L'échelle de chaque figure ne lit aucune séance postérieure à sa date.

### 11. Les markdown

Avec `--markdown`. `journal_annuel(annee)` écrit `rapports/{ANNEE}.md` : le compte
de l'année, la courbe, les ordres avec leur motif engendré, les positions ouvertes
et closes, les décisions notables — sous le bord bas, au-dessus du bord haut,
seuil de la règle 4 franchi — et la lecture de l'année, entièrement calculée.

`bilan()` écrit `bilan.md` : le compte, les positions et leurs tranches, les
frais, l'alpha officiel et l'écart brut avec leurs effets minimaux détectables, ce
qu'ajoutent les règles 4 et 6, ce que coûte l'absence de sortie en perte, les taux
de déclenchement des six règles, les trois issues, la confrontation de
l'étalonnage, et ce que l'expérience établit ou n'établit pas.

> 🔑 **Toute phrase conclusive est engendrée** par la valeur qu'elle résume :
> « indiscernable de zéro » n'est imprimé que si l'intervalle contient zéro.

### 12. La console

Un bloc par année — ordres, positions, valeur de fin d'année contre les deux
références — puis le bloc de bilan : alpha officiel et son EMD, écart brut, frais,
part investie et maximum, déclenchements des six règles, apport des règles 4 et 6,
issues, et toute ligne `ECART ETALONNAGE`.

## Les fichiers écrits

| Fichier | Colonnes |
|---|---|
| `decisions.csv` | `DATE, EXECUTION, CLOSE_AJUSTE, CLOSE_REEL, VAL_120, S_120, ECART_S, TAUX_120, TAUX_20, SOUS_BAS, AU_DESSUS, SEUIL_FRANCHI, SIGNAL` |
| `ordres.csv` | `DATE, DATE_DECISION, SENS, QUANTITE, PRIX_REEL, BRUT, FRAIS, NET, ECART_S, TAUX_20, MOTIF` — `SENS` vaut `ACHAT`, `REGLE-4`, `RENFORT` ou `VENTE` |
| `positions.csv` | `ACHAT, SORTIE, MOTIF, TRANCHES, QUANTITE, PRIX_ACHAT, PRIX_SORTIE, SEUIL_REGLE_4, SEANCES, PLUS_VALUE, REPLI_CLOTURE, REPLI_LOW, CONTRIBUTION` — `PRIX_ACHAT` est le prix **moyen** des tranches, et `SEUIL_REGLE_4` est converti en **cours réel du jour de la décision d'achat**, donc comparable à lui |
| `portefeuille.csv` | `DATE, ESPECES, TITRES, TOTAL, BASE100, APPARIEE100, DETENTION100` |
| `issues.csv` | `DATE, SOUS_BAS, TAUX_20_POSITIF, AU_DESSUS_HAUT, SOUS_ECHANTILLON, RENDEMENT_20` |

Les CSV sont écrits par `csv.DictWriter`, donc en CRLF ; les markdown en LF ; les
SVG comme les générateurs du dépôt. Les booléens s'écrivent `oui` / `non`, et une
cellule vide vaut mieux qu'un nombre inventé.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | exécution complète |
| `1` | série absente, colonne glissante absente de la série, aucune décision hebdomadaire dans une fenêtre, séance d'exécution manquante pour un ordre, argument invalide |

## Cas limites

- **Une position encore ouverte à la dernière séance** : valorisée à la clôture,
  sans frais de vente, signalée comme ouverte, et comptée au § 7 du bilan. C'est
  le cas que la règle 4 rend possible en supprimant toute sortie en perte.
- **Les règles 4 et 6 la même semaine** : les deux ordres sont passés, 10 % puis
  20 %, dimensionnés sur la même valeur de portefeuille. Le cas ne s'est pas
  présenté sur l'étalonnage.
- **Une division le jour d'une exécution** : les titres sont crédités avant que
  l'ordre du jour ne soit passé, et les cours du jour sont déjà dé-ajustés au bon
  facteur.
- **Une quantité nulle** — montant trop faible devant le cours, ou espèces
  épuisées : l'ordre est annulé, la règle est comptée comme déclenchée mais non
  exécutée, et le bilan publie les deux comptes séparément.
- **Un horizon d'issue qui dépasse la dernière séance** : `RENDEMENT_20` vide, et
  l'issue est comptée comme non tranchée.
- **Aucune position sur toute une année** : le journal de l'année le dit, et sa
  lecture est engendrée en conséquence.
