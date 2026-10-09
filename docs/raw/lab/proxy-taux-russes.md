# Un support légal suit-il les taux russes ?

**La question.** La Banque de Russie a porté son taux directeur à **21 %** en
octobre 2024, puis l'a ramené à **14 %** en dix baisses, de juin 2025 à juillet
2026. Les obligations d'État russes, le rouble au comptant et les actions cotées
à Moscou sont hors d'atteinte depuis l'Union européenne. Existe-t-il un support
**légal et accessible** qui suive le rouble ou ce cycle de taux d'assez près pour
en tenir lieu ?

Mesuré du **2023-01-01 au 2026-09-30**, sur onze supports et deux séries du
rouble. Le générateur est
[`figures/mesurer_russie.py`](figures/mesurer_russie.md), sous-commande `taux`,
et il refait tous les nombres de ce document d'un appel. Le taux directeur est
une **donnée déclarée**,
[`figures/taux-directeur-russie.csv`](figures/taux-directeur-russie.csv),
relevée sur le site de la Banque de Russie.

> ⚠️ **Ce que la question ne permet pas.** Un instrument dont le sous-jacent est
> russe — dérivé, produit structuré, fonds logeant des titres russes hors de
> Russie — tombe sous l'article 12 du règlement UE 833/2014, qui interdit de
> participer sciemment à une opération ayant **pour objet ou pour effet** de
> contourner les sanctions. La question porte donc sur des actifs **non russes**
> qui seraient corrélés, et sur eux seuls.

---

## La réponse, en tête

**Aucun.** Aucun support ne suit le rouble, aucun ne suit le taux directeur, et
**le rouble lui-même ne suit pas le taux directeur.**

| Mesure | Meilleur support | Après Holm |
|---|---|---|
| Corrélation hebdomadaire avec le rouble | tenge, $r = +0{,}175$, soit **3,1 %** de variance commune | p = 0,160 |
| Rendement mensuel contre variation du taux | EEM, $r = -0{,}296$ | p = 0,566 |
| Rendement le jour des dix baisses | Kazatomprom, **−1,74 %**, dans le mauvais sens | p = 0,340 |
| Le rouble contre le taux, au mois | $r = -0{,}034$ | p = 1,000 |

Le plus corrélé des supports, le tenge, ne reproduirait que **3,1 %** de la
variance du rouble. Une position prise sur lui serait à **97 % un pari sur autre
chose**.

---

## 1. Les données

| Rôle | Séries |
|---|---|
| Rouble, **référence** | `EURRUB=X`, inversé : + = rouble qui s'apprécie |
| Rouble, **contrôle** | `RUB=X`, inversé de même |
| Banques exposées à la Russie | `RBI.VI` (Raiffeisen), `OTP.BD` (OTP) |
| Kazakhstan | `KSPI` (Kaspi), `HSBK.IL` (Halyk), `KAP.IL` (Kazatomprom), tenge `KZT=X` |
| Géorgie | `TBCG.L` (TBC), `BGEO.L` (Bank of Georgia) |
| Pétrole, marchés | `BZ=F` (Brent), `^FCHI` (CAC 40), `EEM` (actions émergentes) |

**Deux séries ne passent pas le contrôle.** `IMOEX.ME`, l'indice de la Bourse de
Moscou, n'est plus publié par Yahoo. Et `RUB=X` est **irrecevable** : sa clôture
tombe à **0,066** fois sa valeur le 2023-03-16 et y remonte le lendemain. C'est
le contrôle des scissions du dépôt — tout saut de plus de 50 % sans division
déclarée —, et il attrape ici une **erreur de fournisseur**, pas une opération
sur titre. Sans lui, cette séance pèserait à elle seule plus que toutes les
autres réunies, et chacune des corrélations qui suivent serait celle d'une
erreur de saisie.

---

## 2. Le rouble et les supports, semaine par semaine

Les clôtures de Yahoo ne tombent pas à la même heure d'une place à l'autre : au
pas quotidien, ce décalage écrase les corrélations vers zéro. La mesure se fait
donc à la semaine, 195 semaines.

| Support | $r$ | $t$ | $\rho^2$ | Glissante 26 semaines |
|---|---|---|---|---|
| tenge | **+0,175** | +2,47 | 3,1 % | [−0,35 ; +0,61] |
| OTP | +0,119 | +1,66 | 1,4 % | [−0,08 ; +0,59] |
| Bank of Georgia | +0,086 | +1,21 | 0,7 % | [−0,20 ; +0,55] |
| Kazatomprom | +0,055 | +0,76 | 0,3 % | [−0,40 ; +0,49] |
| TBC | +0,036 | +0,50 | 0,1 % | [−0,31 ; +0,40] |
| EEM | −0,001 | −0,01 | 0,0 % | [−0,50 ; +0,37] |
| Raiffeisen | −0,011 | −0,16 | 0,0 % | **[−0,62 ; +0,35]** |
| CAC 40 | −0,011 | −0,15 | 0,0 % | [−0,57 ; +0,38] |
| Halyk | −0,053 | −0,73 | 0,3 % | [−0,26 ; +0,53] |
| Kaspi (141 sem.) | −0,054 | −0,64 | 0,3 % | [−0,31 ; +0,16] |
| Brent | −0,058 | −0,80 | 0,3 % | [−0,55 ; +0,31] |

Un seul coefficient passe le seuil de 5 % — le tenge, p = 0,015 —, et il ne
survit pas à Holm sur onze tests (0,160).

La dernière colonne est la plus instructive. **Raiffeisen**, le « proxy Russie »
le plus cité en Europe, a affiché **−0,62** sur un semestre et **+0,35** sur un
autre : quiconque l'aurait jugé sur six mois aurait conclu à un lien fort, de
l'un ou l'autre signe. C'est l'avertissement du
[laboratoire sur la largeur de bande](largeur-de-bande-fiable.md), sous une autre
forme : **une corrélation mesurée sur une fenêtre ne dit rien de la suivante.**

**Ce que $\rho^2$ veut dire ici.** Prendre une exposition à un actif à travers un
autre est une **couverture croisée**, et le
[module 6 du cours finance](../concept/semestre4/finance/06-la-couverture-optimale.md)
démontre que la meilleure position possible ne reproduit que la fraction
$\rho^2$ de la variance visée ; le reste, $1-\rho^2$, est un risque propre au
support. À 3,1 %, « très corrélé » ne décrit aucun des candidats.

---

## 3. Le taux directeur, mois par mois

44 mois. Un pari sur la baisse des taux voudrait un support qui **monte quand le
taux baisse**, donc $r < 0$.

| Support | $r$ | $t$ | Holm | Pente, % par point de taux |
|---|---|---|---|---|
| EEM | **−0,296** | −2,01 | 0,566 | −1,50 |
| CAC 40 | −0,215 | −1,42 | 1,000 | −0,81 |
| Halyk | −0,190 | −1,26 | 1,000 | −1,58 |
| tenge | −0,160 | −1,05 | 1,000 | −0,47 |
| Raiffeisen | −0,142 | −0,93 | 1,000 | −1,37 |
| Brent | −0,129 | −0,85 | 1,000 | −1,64 |
| **rouble** | **−0,034** | −0,22 | 1,000 | −0,21 |
| les cinq autres | de +0,006 à +0,076 | | 1,000 | |

Aucun coefficient ne survit à Holm. Le plus fort appartient à **EEM** — les
actions émergentes **mondiales**, dont la Russie est sortie en 2022 : c'est une
coïncidence de calendrier, les baisses russes de 2025-2026 ayant accompagné une
hausse générale des émergents, pas un lien russe.

Et le **rouble** lui-même est indifférent au taux directeur, $r = -0{,}034$.
C'est le résultat qui ferme la question : sous contrôle des capitaux, avec des
ventes de devises imposées aux exportateurs, le change ne transmet pas l'écart
de taux. Un support qui suivrait le rouble ne suivrait toujours pas les taux.

Ce lien mensuel est contemporain, et il est du premier genre du
[cours macro](../concept/semestre4/macro/README.md) — « ce qui bouge ensemble ».
Même ce genre-là, le plus facile à établir, n'est pas établi ici.

---

## 4. Le jour des dix baisses

À la séance de chaque décision, annoncée le vendredi à 13 h 30, heure de
Moscou, pendant la séance de toutes les places retenues.

| Support | $k$ | Moyenne | $\sigma$ quotidien | $z$ | Holm |
|---|---|---|---|---|---|
| Kazatomprom | 10 | **−1,74 %** | 2,55 % | −2,16 | 0,340 |
| OTP | 9 | −0,97 % | 1,57 % | −1,85 | 0,641 |
| rouble | 10 | −0,29 % | 1,29 % | −0,71 | 1,000 |
| les neuf autres | 9-10 | de −0,31 % à +0,27 % | | \|z\| ≤ 0,80 | 1,000 |

Le seul $z$ au-delà de 2 est **dans le mauvais sens** — Kazatomprom **baisse** les
jours où le taux russe baisse — et il ne survit pas à Holm. OTP a $k = 9$ parce
que Yahoo ne publie aucune séance de Budapest le 2025-10-24 : la cellule reste vide,
elle n'est pas remplacée par la séance voisine.

**Ce que cette mesure ne dit pas.** Le
[module 2 du cours macro](../concept/semestre4/macro/02-la-politique-monetaire.md)
le démontre : seule la **surprise** d'une décision déplace les cours, et une
baisse que tout le monde attendait n'en contient aucune. Sans consensus des
économistes, ces dix baisses mêlent l'attendu et l'inattendu ; un $z$ nul ne
prouve pas qu'un support est insensible à une surprise russe, il prouve qu'on ne
peut pas le voir ainsi. Et les réunions qui **maintiennent** le taux, qui
peuvent surprendre aussi, ne figurent pas dans la donnée déclarée.

---

## Ce que la mesure établit, et ce qu'elle n'établit pas

**Elle établit**, sur cette fenêtre et ces séries : qu'aucun des onze supports
n'a partagé plus de 3,1 % de variance hebdomadaire avec le rouble ; qu'aucun lien
mensuel avec le taux directeur ne survit à la correction des tests multiples ;
que le rouble lui-même ne réagit pas au taux au pas mensuel ; et que la série
`RUB=X` de Yahoo est inutilisable sans contrôle.

**Elle n'établit pas** qu'aucun proxy n'existe hors de cette liste, ni que ces
supports sont insensibles à une **surprise** de politique monétaire russe, ni
que les liens seraient nuls dans un autre régime — avant 2022, sans contrôle des
capitaux, le rouble suivait le pétrole et les taux.

Le contexte de cette question — pourquoi les secteurs russes les plus contraints
sont aussi les plus inaccessibles, et pourquoi un pari sur la paix n'en est pas
un sur les taux — est dans le
[module 14 du cours macro](../concept/semestre4/macro/14-cas-d-etude-russie-2022-2026.md).

## Refaire la mesure

```bash
pip install yfinance
python docs/raw/lab/figures/mesurer_russie.py taux
```

Les séries de Yahoo sont révisées de temps à autre : une réexécution peut décaler
un coefficient à la troisième décimale. Si elle déplace une conclusion, c'est la
réexécution qui fait foi, et ce document qui se corrige.
