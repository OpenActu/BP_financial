# mesurer_russie.py — miroir d'exécution

Ce document décrit **exactement** ce que fait
`docs/raw/lab/figures/mesurer_russie.py`, dans l'ordre du déroulement. Il fait
autorité : toute évolution du script doit d'abord être décrite ici.

## Rôle

Refaire les nombres de deux documents du laboratoire, un par sous-commande :

| Sous-commande | Document | Question |
|---|---|---|
| `taux` | [`../proxy-taux-russes.md`](../proxy-taux-russes.md) | Un support légal accessible depuis l'Union européenne suit-il le rouble ou le taux directeur de la Banque de Russie ? |
| `evenement` | [`../annonce-nord-stream.md`](../annonce-nord-stream.md) | Six supports ont-ils réagi, le 2026-10-09, dans le sens d'un accord russo-américain ? |

Le script **n'écrit rien** : il imprime un relevé. Aucune figure, aucun CSV.

> ⚠️ **Ce script ne rend aucun verdict d'achat ou de vente.** Il mesure des
> corrélations et des rendements anormaux. Il ne désigne aucun support à
> détenir, et la conclusion du premier document est justement qu'aucun ne
> remplit l'office qu'on lui prêterait.

> ⚠️ **Aucune série n'est russe.** Les supports sont cotés à Vienne, Budapest,
> Londres, Francfort, New York ou sur ICE ; le rouble n'y entre que comme cours
> de change publié par Yahoo, lu et jamais traité. Un instrument dont le
> sous-jacent serait russe n'a rien à faire ici (règlement UE 833/2014, art. 12).

## Dépendances

`yfinance` (et `pandas`, qu'il embarque). La p-valeur de Student est celle de
[`python/import_societe.py`](../../../../python/import_societe.md)
(`p_valeur_student`), importée par chemin : le dépôt n'est pas un paquet.

## La donnée déclarée : `taux-directeur-russie.csv`

Le taux directeur de la Banque de Russie n'est pas dans `yfinance`. Il est
**versionné à côté du script**, relevé le **2026-10-09** sur la page officielle
`cbr.ru/eng/hd_base/KeyRate/` (série quotidienne depuis le 2022-06-01).

| Colonne | Contenu |
|---|---|
| `decision` | Date de la réunion qui a décidé le changement. **Vide** sur la première ligne, qui ne porte que le niveau en vigueur au début de la série. |
| `effet` | Premier jour où la page officielle affiche le nouveau taux. |
| `taux` | Taux directeur en pour cent, à compter de `effet`. |

La page officielle donne `effet` et `taux` ; elle ne donne pas `decision`. Les
dates de décision sont **déduites** par une règle : le dernier vendredi avant
`effet` — décisions annoncées le vendredi à 13 h 30, heure de Moscou —, sauf la
réunion **extraordinaire du 2023-08-15** (un mardi, effet le jour même). Le
2022-06-14 est un mardi parce que le lundi 13 était férié en Russie.

Le script contrôle que les dates `effet` sont strictement croissantes et que
chaque `decision` non vide est antérieure ou égale à son `effet` ; sinon il
s'arrête, code 1.

> ⚠️ **Seuls les changements de taux sont déclarés.** Les réunions qui
> maintiennent le taux n'y figurent pas, si bien que l'étude d'événement ne voit
> pas les **surprises de maintien**. C'est une limite de la donnée, pas un choix
> de méthode.

## Invocation

```bash
python docs/raw/lab/figures/mesurer_russie.py taux
python docs/raw/lab/figures/mesurer_russie.py evenement
python docs/raw/lab/figures/mesurer_russie.py taux --debut 2024-01-01
```

### Arguments de `taux`

| Argument | Défaut | Rôle |
|---|---|---|
| `--debut` | `2023-01-01` | Première séance retenue, incluse. |
| `--fin` | `2026-09-30` | Dernière séance retenue, **incluse**. |
| `--taux` | `taux-directeur-russie.csv`, à côté du script | Donnée déclarée du taux directeur. |

### Arguments de `evenement`

| Argument | Défaut | Rôle |
|---|---|---|
| `--date` | `2026-10-09` | Séance d'événement principale. |
| `--veille` | `2026-10-08` | Première séance de la fenêtre secondaire. |
| `--estimation-debut` | `2025-10-01` | Début de la fenêtre d'estimation des $\beta$, incluse. |
| `--estimation-fin` | `2026-09-30` | Fin de la fenêtre d'estimation, incluse. |

Les valeurs par défaut de `evenement` sont **celles déclarées** dans
[`../annonce-nord-stream.md`](../annonce-nord-stream.md) le 2026-10-09 à
06 h 19. Les changer produit une autre mesure, pas celle du document.

> ⚠️ **Toutes les bornes de dates sont INCLUSIVES**, comme dans
> [`generer_largeur_fiable.py`](generer_largeur_fiable.md) et à l'inverse de
> `import_societe.py`.

## Étapes communes

1. **Téléchargement.** Chaque série par `yf.Ticker(t).history(auto_adjust=True,
   actions=True)`, de dix jours avant la première borne au lendemain de la
   dernière (`end` de Yahoo est exclusif). L'index est ramené à la **date
   calendaire**, sans fuseau. Une série vide est **signalée et écartée**, sans
   arrêter le script.
2. **Contrôle de saut.** Tout saut de clôture supérieur à **50 %** en une
   séance, sans division déclarée, rend la série **irrecevable** : elle est
   signalée avec sa date et son saut, puis écartée. C'est l'invariant des
   scissions du dépôt, appliqué aussi aux cours de change, où il attrape des
   **erreurs de fournisseur** : `RUB=X` tombe à **0,066** fois sa valeur le
   2023-03-16, et y remonte le lendemain.
   Si la série de **référence** est irrecevable, le script s'arrête, code 1.
3. **Rendements logarithmiques** $r_t = \ln(P_t / P_{t-1})$, sur les séances où
   la série est cotée.

## Sous-commande `taux`

### Les séries

| Rôle | Tickers |
|---|---|
| **Référence** | `EURRUB=X`, inversé : $1/P$, donc **+ = rouble qui s'apprécie** |
| **Contrôle** | `RUB=X`, inversé de même — attendu irrecevable (étape 2) |
| **Supports** | `RBI.VI`, `OTP.BD`, `KSPI`, `HSBK.IL`, `TBCG.L`, `BGEO.L`, `KAP.IL`, `BZ=F`, `^FCHI`, `EEM`, et `KZT=X` inversé |

`IMOEX.ME` (Bourse de Moscou) n'est pas demandé : Yahoo ne le publie plus depuis
2022.

### Mesure 1 — corrélation hebdomadaire avec le rouble

Prix au dernier jour coté de chaque semaine close le vendredi, rendements
logarithmiques hebdomadaires, appariés aux semaines où la référence et le support
existent tous deux. Pour chaque support, publiés :

- $n$, le nombre de semaines ;
- $r$, le coefficient de corrélation de Pearson ;
- $t = r\sqrt{(n-2)/(1-r^2)}$ et sa p-valeur de Student bilatérale à $n-2$
  degrés de liberté ;
- $\rho^2 = r^2$, l'**efficacité d'une couverture croisée** au sens du
  [module 6 du cours finance](../../concept/semestre4/finance/06-la-couverture-optimale.md) :
  la part de variance du rouble qu'une position sur ce support reproduit ;
- le **minimum et le maximum** de la corrélation glissante sur 26 semaines.

Puis la p-valeur **corrigée de Holm** sur l'ensemble des supports recevables.

Les mesures 2 et 3 portent sur les mêmes supports **plus la référence
elle-même** : la question de savoir si le rouble réagit au taux directeur précède
celle de savoir si un support le suit.

Le pas hebdomadaire est choisi parce que les clôtures de Yahoo ne tombent pas à
la même heure d'un marché à l'autre, ni pour les changes : au pas quotidien, ce
décalage écrase les corrélations vers zéro.

### Mesure 2 — rendement mensuel contre variation du taux directeur

Prix et taux au dernier jour de chaque mois civil ; le taux d'un jour est celui
de la dernière ligne dont `effet` lui est antérieure ou égale. Pour chaque
support : $n$, $r$ entre le rendement logarithmique du mois et la variation du
taux en points, $t$, p-valeur, p-valeur de Holm, et la **pente** de la droite des
moindres carrés en **% de rendement par point de taux**. Un pari sur la baisse
des taux voudrait $r < 0$.

### Mesure 3 — rendement le jour des baisses

Pour chaque ligne dont `decision` tombe dans la fenêtre et dont le taux
**baisse**, le rendement du support **à la séance datée `decision`**. Si le
support n'a pas coté ce jour-là, la cellule reste **vide** — jamais le rendement
d'une autre séance.

Une décision annoncée à 13 h 30, heure de Moscou, tombe pendant la séance de
toutes les places retenues ; la clôture du jour la contient donc.

Pour chaque support : $k$ le nombre de baisses où il a coté, la moyenne
$\bar r$ de ces rendements, l'écart-type $\sigma$ de **tous** ses rendements
quotidiens sur la fenêtre, et
$z = \bar r / (\sigma/\sqrt k)$, avec sa p-valeur de Student à
$N-1$ degrés de liberté ($N$ séances) et sa p-valeur de Holm. Le tableau
détaillé, décision par décision, est imprimé avant, hausses comprises.

> ⚠️ **Une baisse attendue n'est pas une surprise.** Le
> [module 2 du cours macro](../../concept/semestre4/macro/02-la-politique-monetaire.md)
> le démontre : seule la part inattendue d'une décision déplace les cours. Sans
> consensus des économistes, cette mesure mêle les baisses attendues et
> inattendues, et un $z$ nul ne prouve pas qu'un support est insensible à une
> **surprise**.

## Sous-commande `evenement`

### Les séries

| Support | Sens sous B | Marché de référence |
|---|---|---|
| `TTF=F` | −1 | aucun |
| `BAS.DE` | +1 | `^STOXX50E` |
| `RBI.VI` | +1 | `^STOXX50E` |
| `LNG` | −1 | `^GSPC` |
| `RHM.DE` | +1 | `^STOXX50E` |
| `EPOL` | −1 | `^GSPC` |

Sont aussi téléchargés, pour information seulement : `^STOXX50E`, `^GSPC`,
`BZ=F`.

### Étapes

1. **Présence de la séance.** Si `--date` manque pour l'un des six supports ou
   l'un des deux marchés, le script imprime la liste des séries manquantes et
   s'arrête, **code 2** : les cours ne sont pas encore publiés, il faut relancer
   plus tard. Aucun résultat partiel n'est imprimé.
2. **Bêta.** Sur les séances de la fenêtre d'estimation où le support et son
   marché cotent tous deux : $\beta = \operatorname{Cov}(r, r_m) / \operatorname{Var}(r_m)$,
   et l'écart-type des résidus
   $s = \sqrt{\sum (r - \bar r - \beta (r_m - \bar r_m))^2 / (n-2)}$.
   Pour `TTF=F`, $\beta = 0$ et $s$ est l'écart-type de ses rendements
   ($n-1$ au dénominateur).
3. **Rendement anormal** à la séance `--date` : $RA = r - \beta\, r_m$, et
   $z = RA / s$. Le $z$ **signé** vaut $\text{sens} \times z$.
4. **Fenêtre secondaire** : $RA$ de `--veille` plus $RA$ de `--date`, et
   $z_2 = (RA_{\text{veille}} + RA_{\text{date}}) / (s\sqrt 2)$. Une cellule
   reste vide si l'une des deux séances manque. ⚠️ Contaminée pour `TTF=F`,
   `LNG` et `EPOL`, dont la séance du 8 avait été vue avant la déclaration.
5. **Statistique** $S$ : moyenne des six $z$ signés de la séance principale, et
   **nombre de signes concordants** (z signé strictement positif).
6. **Lecture**, dans cet ordre, la première condition remplie l'emporte :

   | Lecture | Condition |
   |---|---|
   | **B** | $S > 1$ et au moins 5 signes concordants sur 6 |
   | **A** | `TTF=F`, `BAS.DE` et `RBI.VI` concordants, `RHM.DE` et `EPOL` discordants |
   | **Contraire** | $S < -1$ |
   | **Ignorée** | sinon |

7. **Contexte imprimé** : rendements bruts de `^STOXX50E`, `^GSPC` et `BZ=F` à la
   séance principale.

> ⚠️ **`TTF=F` est le contrat du mois proche.** Le contrat de novembre 2026 ne
> cesse de coter que deux jours ouvrés avant le 1ᵉʳ novembre : aucun changement
> d'échéance ne tombe le 2026-10-08 ni le 2026-10-09. Le script ne le vérifie pas
> lui-même ; c'est déclaré ici.

## Affichage console

Tous les nombres sont imprimés avec la virgule décimale. Une valeur indisponible
s'imprime `—`, jamais `nan`.

## Codes de sortie

| Code | Cas |
|---|---|
| 0 | Relevé imprimé. |
| 1 | Donnée déclarée invalide, ou série de référence irrecevable ou vide. |
| 2 | `evenement` : la séance demandée n'est pas encore publiée pour au moins une série. |
