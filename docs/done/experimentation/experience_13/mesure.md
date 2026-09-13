# mesure.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/done/experimentation/experience_13/mesure.py`, dans l'ordre du déroulement.
Il fait autorité : toute évolution du moteur doit d'abord être décrite ici.

Le protocole, lui, est dans [`README.md`](README.md), et c'est **lui** qui fixe la
règle. Ce miroir dit comment elle est exécutée.

## Rôle

Mesurer, sur le CAC 40 point-in-time de 2010 à 2018, si l'écart réduit à une
**droite extrapolée** porte une information qu'une standardisation **sans droite**
ne porte pas. Le moteur ne tient aucun portefeuille, ne passe aucun ordre et ne
calcule aucun alpha : il produit des **événements datés** et leur **issue**.

## Dépendances

**Aucune, hors bibliothèque standard.** Les CSV sont lus par le module `csv`, les
régressions et le bootstrap sont en Python pur. `p_valeur_student()` n'est pas
requise : les intervalles viennent du **bootstrap par grappes**, pas de la loi de
Student — sur des dates groupées, elle serait fausse.

## Les entrées

| Source | Rôle |
|---|---|
| [`univers.csv`](univers.csv) | les 4 596 couples (ancrage, valeur), avec `RETENUE` et `TICKER` |
| `docs/raw/data/quotes/{TICKER}_2009-*.csv` | les 43 séries recevables, `Date` et `Close` |

> ⚠️ **Les fichiers de cours sont trouvés par motif, jamais par nom exact.** Les
> places ne partagent pas le même calendrier — `MT.AS` sert 2 558 séances,
> `NOKIA.HE` 2 513, `AC.PA` 2 556 —, donc la plage inscrite dans le nom de fichier
> diffère d'un ticker à l'autre. Chercher `AC_PA_2009-01-02_2018-12-31.csv` en dur
> échouerait sur Amsterdam et Helsinki.

**Le calendrier de séance est celui de `MC.PA`**, membre de l'indice sur toute la
période. Toutes les dates d'ancrage et tous les décalages `j` se comptent dessus.
Une valeur dont une séance manque à une date donnée est **absente ce jour-là**,
jamais interpolée.

## Constantes

| Constante | Valeur | Rôle |
|---|---|---|
| `FENETRE` | `250` | séances d'ajustement, closes à l'ancrage |
| `PROJECTION` | `250` | séances pendant lesquelles l'événement est cherché |
| `HORIZON` | `60` | séances sur lesquelles l'issue est mesurée |
| `SEUILS` | `(2.0, 2.5, 3.0)` | les trois `k`, tous joués, tous publiés |
| `RECUL` | `20` | décalage du bras T2 |
| `TIRAGES` | `3000` | rééchantillonnages du bootstrap |
| `GRAINE` | `2010` | graine unique, du bootstrap **et** du bras T0 |
| `FIN_MESURE` | `2018-12-31` | aucune séance postérieure n'entre dans un calcul |

## Déroulé d'exécution

### 1. Lecture et contrôles de recevabilité

`univers.csv` est lu, les lignes `RETENUE = non` sont **écartées et comptées**.
Les 43 séries sont chargées, lignes sans `Close` ignorées.

Trois contrôles, chacun **bloquant** :

1. toute valeur `RETENUE = oui` doit avoir un ticker et une série — sinon
   **sortie 1** ;
2. le contrôle d'**opération sur titre** des invariants du dépôt : tout saut de
   clôture supérieur à **50 %** d'une séance à l'autre sans division déclarée rend
   la série irrecevable — **sortie 2**, avec la valeur et la date ;
3. aucune date lue ne dépasse `FIN_MESURE`.

### 2. Les quatre bras, à chaque couple (ancrage, valeur)

Sur les `FENETRE` dernières clôtures closes à l'ancrage `d`, rangs
$T_i = i,\ i = 1..250$ :

$$r = \frac{\operatorname{cov}(T, C)}{V_T}, \quad V_T = \frac{n^2-1}{12}, \quad
\operatorname{VAL} = \bar C + r\Bigl(n - \tfrac{n+1}{2}\Bigr), \quad
s = \sqrt{\frac{\sum \varepsilon_i^2}{n-2}}$$

Covariance et variance **de population** (`ddof = 0`), `s` sans biais : ce sont
exactement les conventions de [`modele.md`](../../../raw/modele.md) et de
[`generer_largeur_fiable.py`](../../../raw/lab/figures/generer_largeur_fiable.md).

Puis, à chaque séance `d + j` :

| Bras | Écart réduit |
|---|---|
| **R** | $z = \bigl(C_{d+j} - \operatorname{VAL} - r\,j\bigr)/s$ |
| **T1** | $z = \bigl(C_{d+j} - \bar C_{250}\bigr)/\operatorname{sd}(C_{250})$, `sd` de population |
| **T2** | $z = \bigl(C_{d+j} - C_{d+j-20}\bigr)/\bigl(\sigma_{\text{jour}}\sqrt{20}\bigr)$ |

$\sigma_{\text{jour}}$ est l'écart-type des 249 rendements quotidiens de la
fenêtre d'ajustement. **Aucune des trois grandeurs ne lit une séance postérieure à
`d + j`** : T2 regarde 20 séances en arrière, jamais en avant.

> **Ce que chaque bras retire.** R porte une droite **et** une pente ; T1 garde le
> niveau moyen et la dispersion mais **supprime la pente** ; T2 supprime aussi le
> niveau et ne garde qu'un déplacement rapporté à sa volatilité. Lire les trois
> ensemble isole donc **ce que la droite ajoute**, et rien d'autre.

### 3. L'événement

Pour chaque couple (ancrage, valeur, bras, `k`), l'événement est la **première**
séance `j ∈ [1, PROJECTION]` telle que `z < −k` (bras **bas**) ou `z > +k` (bras
**haut**). Un couple produit **au plus un** événement par bras et par sens : les
séances suivantes du même épisode ne comptent pas.

> ⚠️ **Un événement n'est retenu que si son horizon tient dans la fenêtre.** Il
> faut `HORIZON` séances après la date d'événement, **sans dépasser
> `FIN_MESURE`** ; sinon l'événement est **écarté et compté** comme tel. C'est la
> borne qui garantit qu'aucune séance de 2019 — fenêtre brûlée par la mesure qui a
> produit l'hypothèse — n'entre dans un résultat.
>
> Ce rejet introduit une sélection : les événements tardifs de 2018 disparaissent.
> Le nombre d'écartés est **publié par année**, pour que l'effet de bord soit
> lisible plutôt que supposé négligeable.

### 4. L'issue

Pour un événement daté `e` :

$$\text{excès} = \underbrace{\frac{C_{e+60}}{C_e} - 1}_{\text{la valeur percée}}
\;-\; \underbrace{\frac{1}{m}\sum_{v} \left(\frac{C^v_{e+60}}{C^v_e} - 1\right)}_{\text{le panier apparié}}$$

Le panier est **équipondéré**, composé des **autres valeurs recevables de la
composition de l'ancrage**, la valeur percée exclue, sur **exactement les mêmes
séances**. Une valeur du panier à laquelle une des deux séances manque est
retirée du panier pour cet événement, et `m` diminue d'autant.

> **Pourquoi la composition de l'ancrage et non celle du jour de l'événement.**
> `univers.csv` ne donne la composition qu'aux 115 ancrages ; prendre celle de `e`
> exigerait d'interroger la source à des dates que le protocole n'a pas déclarées.
> Le panier suit donc l'indice tel qu'il était **quand la bande a été posée**.

L'excès **net** est publié à côté du brut : le moteur retranche un aller-retour
plat, choisi sur le **préfixe de l'ISIN** — `FR` contre le reste — aux valeurs
mesurées par `couts_transaction.py` : **0,544 %** (LVMH, droit français) et
**0,246 %** (Airbus, droit néerlandais, TTF exemptée).

> ⚠️ **Deux approximations, toutes deux déclarées.** Ces taux sont calculés sur
> les volumes et capitalisations **d'aujourd'hui**, et appliqués à des séances de
> 2010 à 2018 : c'est un **anachronisme**. Et un taux plat par pays **flatte les
> petites capitalisations** — Vallourec mesure **0,687 %** contre 0,544 % pour
> LVMH, parce que l'impact de marché passe de 0,0069 % à 0,0783 % par sens. Le
> net est donc **indicatif** ; le critère de décision se joue à +1,00 point, pas
> au coût, et aucune position n'est dimensionnée.

### 5. Le bras T0

Même **nombre** d'événements que le bras R au même `k` et au même sens, mais aux
dates **tirées au hasard** parmi tous les couples (valeur, séance) où l'issue est
calculable, `random.Random(GRAINE)`. C'est le témoin nul de
[l'expérience 5](../experience_5/README.md) : il mesure ce que rend le dispositif
quand l'événement ne porte rien.

### 6. L'agrégation, par grappes de dates

Pour chaque (bras, sens, `k`) : nombre d'événements, **nombre de grappes de mois
calendaires occupées**, excès moyen, et intervalle à 95 % par **bootstrap sur
blocs de mois** — `TIRAGES` rééchantillonnages avec remise **des mois**, jamais
des événements.

> 🔑 **C'est la leçon de l'[expérience 5](../experience_5/README.md), et elle est
> structurante ici.** Les franchissements arrivent en paquets : sur la fenêtre
> brûlée, les 5 mois les plus chargés portaient 29 % des événements. Un
> intervalle calculé sur le nombre d'**événements** serait trois à quatre fois
> trop étroit. L'unité indépendante est le **mois**, et c'est lui qu'on
> rééchantillonne.

Le **test principal** est l'écart `R − max(T1, T2)`, rééchantillonné **sur les
mêmes mois** que R et les témoins — appariement par bloc, pas deux bootstraps
indépendants.

**Correction de Holm** sur la famille des 18 tests (3 bras × 2 sens × 3 `k`), le
test principal étant désigné avant toute mesure. Le témoin T0 forme une **seconde
famille**, de 6 tests, corrigée séparément : il ne mesure pas la même chose et ne
doit pas diluer la correction des cellules principales.

### 7. Le verdict

Les quatre conditions du [`README.md`](README.md#le-critère-de-décision) sont
évaluées dans l'ordre et **toutes** publiées, y compris celles qui échouent. Le
verdict est `UTILE` si les quatre tiennent, `INUTILE` sinon.

**Avant de le lire**, le moteur vérifie que T0 est compatible avec zéro. S'il ne
l'est pas, il imprime `DISPOSITIF DEFECTUEUX`, n'écrit **aucun** verdict et sort
en **3**.

> ⚠️ **Ce contrôle subit la même correction de Holm que les cellules
> principales**, sur sa propre famille de 6 tests (2 sens × 3 `k`), et c'est la
> `p` **ajustée** qui est comparée à `SEUIL_VALIDITE = 0,05`. Sans cette
> correction, six intervalles à 95 % ferment la vanne **26,5 % du temps sous
> H₀** — le contrôle de validité déclencherait alors plus souvent que le test
> qu'il protège. Voir la correction déclarée au [`README.md`](README.md).

### 8. Les deux figures

Écrites dans `graphiques/`, seulement en mode normal — jamais sous
`--dimensionner`, qui ne calcule aucune issue et n'aurait donc rien à tracer.

**`cellules.svg` — le graphe en forêt.** Une ligne par cellule, dans l'ordre du
tableau : l'intervalle à 95 % en trait, la moyenne en disque, une teinte par bras,
et la **verticale à zéro** en trait appuyé. La cellule de décision — `R, bas,
k = 3` — est tracée plus épaisse et nommée en gras ; le **test principal**
`R − max(T1, T2)` figure en bas, séparé par un filet, parce qu'il ne se lit pas sur
la même échelle de sens. La marge droite porte la `p` **ajustée par Holm**.

> C'est le bilan en une image : si aucun intervalle ne franchit la verticale, le
> verdict est acquis avant d'avoir lu un chiffre.

**`grappes.svg` — les événements par mois.** Deux séries de barres sur les mois
calendaires de la fenêtre : `R, bas, k = 3` et `T2, bas, k = 3`. Elle ne sert qu'à
une chose, mais décisive : **montrer que l'unité indépendante est le mois et non
l'événement**, et pourquoi T2 — 20 grappes contre 92 — borne la puissance du test
principal. Un lecteur qui doute du bootstrap par blocs la regarde.

**Conventions de tracé**, alignées sur les `journal.py` des autres expériences :
`viewBox` et dimensions explicites, police `Segoe UI`, fond blanc, accents en
entités HTML, et écriture par `Path.write_text()` — qui rend du CRLF sous Windows,
conforme au [`.gitattributes`](../../../../.gitattributes). **Aucune bibliothèque de
tracé** : `matplotlib` n'est pas installé et ne doit pas l'être.

## Arguments

| Argument | Défaut | Effet |
|---|---|---|
| `--dimensionner` | absent | compte les événements et les grappes, mesure la dispersion **inconditionnelle** de l'issue et en déduit l'EMD ; **ne calcule l'issue d'aucun événement** et n'écrit aucun fichier |
| `--sortie` | le répertoire du script | où écrire `evenements.csv` |
| `--seuils` | `2,2.5,3` | les `k` joués |
| `--horizon` | `60` | séances de l'issue |

> `--dimensionner` existe pour que le **nombre d'événements soit connu avant les
> issues**. C'est la seule mesure que le protocole autorise à faire sur 2010-2018
> avant de figer le critère — elle ne dépend d'aucun résultat de la règle.
>
> La dispersion qu'il mesure est **inconditionnelle** : elle porte sur des couples
> (valeur, séance) **tirés au hasard**, graine `GRAINE`, jamais sur les dates
> qu'un franchissement a désignées. C'est la matière du bras T0, et c'est ce qui
> la rend licite : un écart-type d'issue sur dates quelconques ne dit rien de ce
> que la règle produira. L'EMD publié vaut
> $1{,}96\,\sigma/\sqrt{N_{\text{grappes}}}$, cellule par cellule.

## Fichiers écrits

| Fichier | Contenu |
|---|---|
| `evenements.csv` | une ligne par événement : `ANCRAGE`, `ISIN`, `TICKER`, `BRAS`, `K`, `SENS`, `DATE_EVENEMENT`, `J`, `Z`, `EXCES`, `EXCES_NET`, `TAILLE_PANIER` |
| `graphiques/cellules.svg` | le graphe en forêt des 18 cellules et du test principal |
| `graphiques/grappes.svg` | les événements par mois, pour `R` et `T2` au seuil de décision |

Les deux figures sont **réécrites à chaque exécution** et idempotentes : le moteur
étant déterministe jusqu'à la graine du bootstrap, une régénération ne laisse aucun
diff.

`bilan.md` est **écrit à la main** à partir de la sortie console, comme dans les
douze autres expériences : aucun chiffre du bilan n'est saisi autrement que
recopié du moteur.

## Codes de sortie

| Code | Cause |
|---|---|
| `0` | Exécution complète. |
| `1` | `univers.csv` ou une série recevable introuvable. |
| `2` | Saut de clôture supérieur à 50 % sans division déclarée : série irrecevable. |
| `3` | Le témoin T0 s'écarte de zéro : dispositif défectueux, aucun verdict publié. |

## Cas limites

- **Moins de 250 séances avant l'ancrage** — le couple est écarté et compté. Le
  premier ancrage dispose de 256 séances : la fenêtre tient de justesse, et c'est
  pour cela que les séries partent de **2009**.
- **Aucun événement pour un (bras, sens, k)** — la ligne est publiée à vide, pas
  omise : une règle qui ne se déclenche jamais est un résultat.
- **Panier réduit à moins de 10 valeurs** — l'événement est écarté et compté ; un
  panier trop maigre n'apparie rien.
- **Variance nulle** sur une fenêtre — cours constant : le couple est écarté.
- **Exécution répétée** — idempotente à l'octet près, le bras T0 compris, puisque
  sa graine est fixée.
