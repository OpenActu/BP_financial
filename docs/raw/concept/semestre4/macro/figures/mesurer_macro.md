# mesurer_macro.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/raw/concept/semestre4/macro/figures/mesurer_macro.py`, dans l'ordre du
déroulement. Il fait autorité : toute évolution du script doit d'abord être
décrite ici.

## Rôle

Produire les nombres que cite le [cours macro](../README.md), et sa seule figure.
Quatre relevés sont imprimés sur la console :

- **A** : les sensibilités hebdomadaires de huit valeurs du CAC 40 ;
- **B** : la sensibilité au taux, recalculée sur trois sous-périodes ;
- **C** : les corrélations annuelles du CAC 40 avec quatre variables macro ;
- **D** : la prévision du rendement mensuel suivant, dans l'échantillon et hors
  échantillon.

La figure trace la première colonne du relevé C.

Le script est versionné **à côté de ce qu'il produit**, comme
[`generer_figures.py`](../../../semestre3/canal/figures/generer_figures.md) l'est
pour le cours canal. Il ne compte pas parmi les onze utilitaires et, à la
différence de ce dernier, **il appelle le réseau**.

## Dépendances

`yfinance`, avec le `pandas` qu'il installe. La p-valeur de Student est celle du
dépôt, `p_valeur_student` de
[`import_societe.py`](../../../../../../python/import_societe.md). Elle est importée
**localement**, après ajout de `python/` au chemin, parce que le dépôt n'est pas
un paquet (d'où le `# noqa: PLC0415`). Les moindres carrés et l'inversion de
matrice sont écrits en Python pur.

## Arguments

| Argument | Défaut | Effet |
|---|---|---|
| `--sortie RÉPERTOIRE` | le répertoire du script | où écrire `correlation-actions-taux.svg` ; créé s'il n'existe pas |
| `--stats` | absent | imprime les quatre relevés **sans écrire la figure** |

Il n'y a **pas d'invite interactive**. Sans argument, le script imprime tout et
réécrit la figure.

## Constantes déclarées

| Constante | Valeur | Rôle |
|---|---|---|
| `VALEURS` | `BNP.PA`, `LI.PA`, `ENGI.PA`, `MC.PA`, `OR.PA`, `AIR.PA`, `TTE.PA`, `SAN.PA` | une valeur par canal attendu : banque, foncière, service aux collectivités, luxe, consommation défensive, exportateur en dollars, pétrolière, pharmacie |
| `INDICE` | `^FCHI` | le marché (indice **nu**) |
| `TAUX_10`, `TAUX_3M` | `^TNX`, `^IRX` | taux américains à 10 ans et à 13 semaines, **en pourcentage** |
| `CHANGE` | `EURUSD=X` | dollars pour un euro |
| `PETROLE` | `BZ=F` | Brent, contrat à terme le plus proche |
| `CREDIT_HY`, `CREDIT_GOV` | `HYG`, `IEF` | fonds obligataires américains, haut rendement et Trésor 7-10 ans |
| `DEBUT`, `FIN` | `2008-01-01`, `2026-01-01` | fenêtre des relevés A à C ; `FIN` est **exclue** |
| `DEBUT_PREVISION` | `1990-01-01` | début de la fenêtre du relevé D |
| `APPRENTISSAGE` | `120` | mois d'apprentissage avant la première prévision hors échantillon |
| `SEUIL_SAUT` | `0.50` | le contrôle des opérations sur titres |
| `ALPHA` | `0.05` | seuil des tests et de Holm |
| `SOUS_PERIODES` | `2008-2012`, `2013-2021`, `2022-2025` | fenêtres du relevé B, bornes de fin exclues |

**Pourquoi le taux américain.** Yahoo ne publie aucun taux souverain de la zone
euro exploitable (Bund, OAT, €STR). Le taux à 10 ans américain ne capte donc le
canal européen **que par procuration**. Le cours le déclare au
[module 1](../01-le-taux-d-actualisation.md).

## Déroulement

### 1. Téléchargement

`telecharger(ticker, debut, fin)` appelle
`yf.Ticker(ticker).history(start, end, auto_adjust=True, actions=True)`. L'index
est ramené à des **dates calendaires sans fuseau**. Une série vide arrête le
script, avec le message `Aucune donnée pour « TICKER ».`

### 2. Contrôle de recevabilité des huit valeurs

`controler_saut` calcule, séance par séance, `Close_t / Close_{t-1} − 1`. Si une
variation dépasse **50 % en valeur absolue** un jour où `Stock Splits` est nul, le
script s'arrête sur :

```
Série irrecevable : TICKER saute de ±x % le AAAA-MM-JJ sans division déclarée (opération sur titre présumée).
```

C'est l'invariant du dépôt sur les scissions. Aucune des huit valeurs ne le
déclenche sur la fenêtre.

### 3. Passage à la semaine

Chaque série est échantillonnée à la **dernière cotation de la semaine close le
vendredi** (`resample("W-FRI").last()`). Le pas hebdomadaire atténue le décalage
horaire : Paris clôt à 17 h 30, New York cinq heures et demie plus tard, et un
choc de taux américain de l'après-midi n'arrive dans le cours de Paris que le
lendemain.

Les variables construites :

| Colonne | Formule | Unité |
|---|---|---|
| `MARCHE` | $P^{\text{FCHI}}_w / P^{\text{FCHI}}_{w-1} - 1$ | rendement |
| `TAUX` | $y^{10}_w - y^{10}_{w-1}$ | **points de pourcentage** : +1 signifie de 4 % à 5 % |
| `EURUSD` | variation relative du cours | rendement : > 0 quand l'euro s'apprécie |
| `BRENT` | variation relative du prix | rendement |
| `CREDIT` | $r^{\text{HYG}}_w - r^{\text{IEF}}_w$ | rendement : < 0 quand l'écart de crédit s'élargit |
| une colonne par valeur | variation relative de `Close` (ajustée) | rendement |

Les variations sont calculées **sans combler** les semaines manquantes
(`fill_method=None`). La première semaine, sans variation, est retirée, ainsi que
la semaine à cheval sur `FIN`, dont l'étiquette tombe l'année suivante et qui
serait incomplète.

### 4. Relevé A — sensibilités, marché compris

Pour chaque valeur, sur les semaines où les cinq variables existent :

$$r_{i,w} = a + b_M\,\text{MARCHE}_w + b_T\,\text{TAUX}_w + b_F\,\text{EURUSD}_w + b_P\,\text{BRENT}_w + e_w$$

par moindres carrés ordinaires (`mco`). $X^\top X$ est inversée par Gauss-Jordan
à pivot partiel (`inverser`). Pour chaque coefficient :

$$t_j = \frac{b_j}{\sqrt{s^2\,[(X^\top X)^{-1}]_{jj}}}, \qquad s^2 = \frac{\text{SCR}}{n-k}, \qquad \text{ddl} = n - k$$

avec $k = 5$. Les erreurs types supposent des résidus i.i.d. : aucune correction
d'hétéroscédasticité ni d'autocorrélation n'est appliquée, et le cours le
signale.

Les **24 coefficients macro** (8 valeurs × 3 variables) sont soumis à la
**correction de Holm** au seuil 5 % (`holm`) : les p-valeurs sont triées par
ordre croissant, et la $r$-ième (à partir de 0) est rejetée tant que
$p \le 0{,}05/(24 - r)$ ; au premier échec, on s'arrête.

Affichage : une ligne par valeur, avec `n`, `b_MARCHE`, puis chaque coefficient
macro suivi de son `t` et d'un `*` s'il survit à Holm, et enfin le `R²`. Suivent
le nombre de coefficients significatifs sans correction et après Holm.

> ⚠️ **La constante $a$ n'est jamais publiée.** `Close` est ajustée des
> dividendes et `^FCHI` ne l'est pas : $a$ serait un alpha fabriqué par la
> convention. Les pentes, calculées sur des variations hebdomadaires, n'en sont
> presque pas affectées.

### 5. Relevé B — sous-périodes

La même régression, restreinte à chacune des trois `SOUS_PERIODES`. Seuls
`b_TAUX` et son `t` sont imprimés, au format `+0,0000 (+0,00)`. Aucune correction
de multiplicité n'est appliquée : ce relevé mesure une **instabilité**, il ne teste
rien.

### 6. Relevé C — corrélations annuelles

Pour chaque année civile, la corrélation de Pearson de `MARCHE` avec `TAUX`,
`EURUSD`, `BRENT` et `CREDIT`, sur les semaines où les cinq existent. Une ligne
`total` donne les mêmes corrélations sur toute la fenêtre. La fonction rend la
liste `(année, corrélation avec TAUX)`, qui sert à la figure.

Lecture du signe : `TAUX` monte quand le prix des obligations baisse. Une
corrélation **positive** entre actions et variation du taux signifie donc que
**actions et obligations évoluent en sens contraire**.

### 7. Relevé D — la prévision

Séries **mensuelles** (dernière cotation du mois, `resample("ME")`) de `^FCHI`,
`^TNX` et `^IRX`, depuis `DEBUT_PREVISION` jusqu'à `FIN` exclue. La variable
expliquée est le rendement du **mois suivant** : $r_{m+1}$. Trois prédicteurs,
chacun connu à la fin du mois $m$ :

| Prédicteur | Formule |
|---|---|
| pente 10 ans − 3 mois | $y^{10}_m - y^{3M}_m$ |
| taux à 3 mois | $y^{3M}_m$ |
| variation 12 mois du 10 ans | $y^{10}_m - y^{10}_{m-12}$ |

Aucune de ces trois variables n'est révisée ni publiée avec retard : ce sont des
**prix de marché**, connus à la clôture. Le regard en avant qui menace les
séries macro publiées ([§ 5.3 du cours](../05-la-croissance.md)) ne s'applique donc pas ici.

Pour chaque prédicteur :

1. **Dans l'échantillon** : régression de $r_{m+1}$ sur le prédicteur, sur toute
   la fenêtre ; on imprime le `R²`, le `t` de la pente et sa p-valeur.
2. **Hors échantillon** : pour chaque mois $i$ à partir du 121ᵉ, la régression
   est réestimée sur les mois $1 \dots i-1$ seulement, et elle prévoit $r_i$. La
   référence est la moyenne historique des mêmes mois. Le script imprime

$$R^2_{\text{hors}} = 1 - \frac{\sum_i (r_i - \hat r_i)^2}{\sum_i (r_i - \bar r_{1..i-1})^2}$$

C'est la statistique de Campbell & Thompson (2008). Elle est **négative** quand la
moyenne historique aurait mieux prévu que le prédicteur.

Affichage : `prédicteur`, `n`, premier et dernier mois (`de`, `à`), `R² dans`, `t`,
`p`, `R² hors`.

### 8. Figure

Sauf avec `--stats`, le script écrit `correlation-actions-taux.svg` dans
`--sortie` : 1200 × 560, une barre par année, bleue au-dessus de zéro et orange
en dessous, sur une échelle fixe de −0,8 à +0,8, avec la valeur écrite au bout de
chaque barre. Le chemin écrit est imprimé.

## Codes de sortie

| Code | Cas |
|---|---|
| 0 | tout s'est déroulé |
| 1 | `SystemExit` avec message : série vide ou série irrecevable |
| autre | exception non rattrapée (réseau, fournisseur) : aucun `except` n'enveloppe les appels réseau, l'erreur remonte telle quelle |

## Reproductibilité

Les relevés dépendent de ce que sert le fournisseur **le jour de l'appel**. Les
cours ajustés sont réécrits à chaque dividende, ce qui déplace légèrement les
pentes d'un appel à l'autre. Les nombres cités par le cours ont été obtenus le
**2026-09-29**.
