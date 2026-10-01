# Module 11 — Exemple chiffré : huit valeurs du CAC 40

**Prérequis :** modules [1](01-le-taux-d-actualisation.md) à [10](10-des-facteurs-a-la-prevision.md).
**Ce qu'on établit ici :** les sensibilités de huit valeurs au taux, au change et au pétrole, lues d'abord brutes puis corrigées des tests multiples, et ce que ces nombres permettent, et ne permettent pas, de conclure.

---

## 11.1 — Le protocole, fixé avant le calcul

```bash
python docs/raw/concept/semestre4/macro/figures/mesurer_macro.py --stats
```

| Élément | Choix | Raison |
|---|---|---|
| Univers | BNP Paribas, Klépierre, Engie, LVMH, L'Oréal, Airbus, TotalEnergies, Sanofi | **une valeur par canal attendu** : banque, foncière, service aux collectivités, luxe, consommation défensive, exportateur, pétrolière, pharmacie |
| Fenêtre | 2008-01-01 → 2026-01-01 exclue | le Brent commence mi-2007 sur la source |
| Fréquence | hebdomadaire, vendredi | atténue le décalage de clôture Paris / New York |
| Régression | $r_i = a + b_M r^{\text{CAC}} + b_T \Delta y + b_F r^{\text{EUR}} + b_P r^{\text{Brent}} + e$ | marché compris : on mesure la sensibilité **propre** |
| Test | Student bilatéral, $\alpha = 5\,\%$, **Holm** sur les 24 coefficients macro | 8 valeurs × 3 variables |
| Contrôle | tout saut de clôture > 50 % sans division déclarée arrête le script | l'invariant du dépôt sur les scissions ; aucune des huit ne le déclenche |

> ⚠️ **L'univers n'est pas tiré au sort.** Il est choisi **pour** représenter des
> canaux, ce qui est légitime pour illustrer une méthode, et interdit pour
> conclure sur le CAC 40 en général. Les huit valeurs sont aussi des
> **survivantes** : elles sont à l'indice en 2026.

## 11.2 — Le tableau brut

933 semaines par valeur. $b_T$ en rendement par **point** de taux ; $b_F$ et $b_P$
en rendement par unité de rendement du change ou du Brent. Un astérisque marque
les coefficients qui survivent à Holm.

| Valeur | $b_M$ | $b_T$ | $t$ | $b_F$ | $t$ | $b_P$ | $t$ | $R^2$ |
|---|---|---|---|---|---|---|---|---|
| BNP Paribas | 1,337 | **+0,0713** | **+7,15*** | +0,249 | +2,60 | −0,070 | −2,85 | 0,592 |
| Klépierre | 1,090 | −0,0170 | −1,36 | −0,031 | −0,26 | −0,024 | −0,78 | 0,336 |
| Engie | 0,950 | −0,0216 | −2,65 | +0,085 | +1,09 | −0,017 | −0,86 | 0,474 |
| LVMH | 1,042 | −0,0042 | −0,59 | +0,115 | +1,69 | −0,032 | −1,84 | 0,598 |
| L'Oréal | 0,756 | **−0,0385** | **−6,24*** | −0,122 | −2,06 | **−0,055** | **−3,59*** | 0,471 |
| Airbus | 1,238 | −0,0016 | −0,16 | **−0,607** | **−6,16*** | −0,026 | −1,02 | 0,494 |
| TotalEnergies | 0,816 | −0,0009 | −0,13 | −0,152 | −2,42 | **+0,226** | **+13,93*** | 0,620 |
| Sanofi | 0,740 | −0,0058 | −0,76 | **−0,317** | **−4,30*** | −0,046 | −2,41 | 0,372 |

La constante $a$ n'est **pas publiée** : `Close` est ajustée des dividendes et
`^FCHI` ne l'est pas, et $a$ serait un alpha fabriqué par cette différence de
convention.

## 11.3 — Lire avec Holm

| | Nombre |
|---|---|
| coefficients macro testés | 24 |
| attendus à tort au seuil de 5 %, si aucun effet n'existait | $24 \times 0{,}05 = 1{,}2$ |
| significatifs **sans** correction | **12** |
| significatifs **après** Holm | **6** |

La correction de Holm trie les 24 p-valeurs et exige de la plus petite
$p \le 0{,}05/24 = 0{,}0021$, de la suivante $p \le 0{,}05/23$, etc. Elle écarte
six coefficients qui passaient le seuil nu : Engie au taux ($t = -2{,}65$), BNP
Paribas au change ($+2{,}60$) et au pétrole ($-2{,}85$), TotalEnergies au change
($-2{,}42$), Sanofi au pétrole ($-2{,}41$) et L'Oréal au change ($-2{,}06$).

Les six qui restent :

| Coefficient | $t$ | Conforme au canal attendu ? |
|---|---|---|
| TotalEnergies / Brent | +13,93 | ✅ une pétrolière |
| BNP Paribas / taux | +7,15 | ✅ marge d'intérêt ([module 1](01-le-taux-d-actualisation.md)) |
| L'Oréal / taux | −6,24 | ✅ duration élevée |
| Airbus / EUR-USD | −6,16 | ✅ coûts en euros, prix en dollars ([module 6](06-le-change.md)) |
| Sanofi / EUR-USD | −4,30 | ✅ forte part de ventes en dollars |
| L'Oréal / Brent | −3,59 | ⚠️ canal indirect (emballages, transport), non déclaré avant |

Cinq des six confirment un canal **nommé à l'avance** dans le choix de l'univers.
Le sixième est significatif sans avoir été prévu : il faut le publier, et le
traiter comme une piste à éprouver ailleurs, pas comme un résultat.

Trois canaux attendus **ne sortent pas** : Klépierre au taux, Engie au taux (qui
ne survit pas à Holm), LVMH au change. C'est aussi un résultat, et il se publie
au même titre que les autres.

## 11.4 — Recalculer par sous-période

Le relevé B recalcule $b_T$ sur trois sous-périodes :

| Valeur | 2008-2012 | 2013-2021 | 2022-2025 |
|---|---|---|---|
| BNP Paribas | +0,062 (+2,37) | **+0,105 (+8,40)** | +0,043 (+2,92) |
| Klépierre | −0,010 (−0,47) | −0,000 (−0,01) | **−0,044 (−3,05)** |
| Engie | −0,029 (−1,68) | **−0,045 (−3,66)** | −0,001 (−0,05) |
| LVMH | +0,006 (+0,41) | +0,002 (+0,14) | −0,003 (−0,21) |
| L'Oréal | −0,011 (−0,84) | **−0,051 (−5,73)** | **−0,038 (−3,10)** |
| Airbus | −0,037 (−1,71) | **+0,041 (+2,44)** | −0,010 (−0,69) |
| TotalEnergies | +0,006 (+0,55) | −0,026 (−2,30) | +0,011 (+0,97) |
| Sanofi | −0,008 (−0,52) | −0,029 (−2,47) | +0,014 (+0,90) |

Seule BNP Paribas garde le même signe **et** un $t$ supérieur à 2 dans les trois
sous-périodes. L'Oréal est stable depuis 2013. Pour les autres, le coefficient
de toute la période est une moyenne de régimes qui ne se ressemblent pas : le
[module 9](09-la-correlation-actions-obligations.md) en donne l'explication.

## 11.5 — Ce que ces nombres permettent de conclure

| Énoncé | Licite ? |
|---|---|
| « Sur 2008-2025, BNP Paribas a réagi positivement aux hausses du taux américain, marché compris. » | ✅ mesuré, survit à Holm, stable sur trois sous-périodes |
| « Airbus est exposée à l'euro-dollar. » | ✅ mesuré, survit à Holm |
| « LVMH n'est pas exposée au change. » | ❌ on n'a pas **montré l'absence** d'effet, seulement l'échec à le détecter |
| « Klépierre est sensible aux taux depuis 2022. » | ⚠️ un seul coefficient d'un relevé non corrigé, sur une charnière choisie après coup |
| « Les taux vont monter, donc BNP Paribas va surperformer. » | ❌ deux fautes : une prévision de taux, et une sensibilité passée prise pour une loi |
| « Cette valeur a un alpha de … » | ❌ la constante n'est pas publiée, et le [cours alpha](../alpha/03-l-horizon-necessaire.md) dit pourquoi elle serait de toute façon indiscernable de zéro |

> 🔑 **Une sensibilité macro est une description du passé, pas une recette.** Elle
> dit comment un titre a encaissé les chocs d'une période ; elle ne dit ni quels
> chocs viendront, ni si le titre les encaissera de la même façon. C'est tout ce
> que ce cours permet de mesurer, et c'est déjà beaucoup.

## 11.6 — Reproduire

Les nombres de ce module ont été obtenus le **2026-09-29**. Les cours ajustés sont
réécrits par le fournisseur à chaque dividende : un nouvel appel déplacera
légèrement les coefficients, sans changer, sauf erreur, les conclusions du
§ 11.3. Si elles changeaient, ce serait à publier, pas à corriger.

## Ce qu'il faut retenir

1. Sur 24 sensibilités, 12 passent le seuil nu et **6 survivent à Holm**, dont
   cinq sur un canal nommé à l'avance.
2. Trois canaux attendus ne sortent pas, dont celui de LVMH au change.
3. Seule BNP Paribas garde sa sensibilité au taux dans les trois sous-périodes.
4. Aucun de ces nombres n'est un alpha, ni une prévision.

---

⬅️ [Module 10 — Des facteurs à la prévision](10-des-facteurs-a-la-prevision.md) ·
➡️ [Module 12 — Cas d'étude : la livre sterling, 1992](12-cas-d-etude-livre-sterling-1992.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
