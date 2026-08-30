# Module 7 — Le stop, une sortie qui n'attend pas de verdict ⭐

**Prérequis :** modules [1](01-ce-que-le-chartiste-produit.md) à [6](06-cas-pratique.md).
**Ce qu'on établit ici :** un ordre stop est une **sortie conditionnelle au prix**, qui ne consulte aucun critère et n'attend pas la cadence. C'est donc un ajout à la règle, à déclarer avant tout chiffre comme tout le reste (§ 7.2). Mesuré sur le fil rouge, le résultat est net : les stops **fixes** usuels ne se déclenchent jamais, les stops **suiveurs** se déclenchent tous et **détruisent le résultat** — de $+80{,}70\,\%$ sans stop à $-12{,}49\,\%$ avec un stop suiveur à $10\,\%$. La cause est arithmétique et se lit en cinq lignes (§ 7.6) : **les cinq réentrées se sont faites plus haut que la sortie, cinq fois sur cinq.**

---

## 7.0 — D'où vient la question

Le [§ 6.4](06-cas-pratique.md#64--dix-neuf-mois-de-détention-et-le-silence-de-la-règle)
laisse une position ouverte traverser un repli de $25{,}8\,\%$ pendant **224 séances
sans qu'un seul verdict soit rendu**. Ce silence est conforme à la règle — c'est la
ligne 3 du [§ 5.8](05-la-cadence-fait-partie-de-la-regle.md#58--ce-quil-faut-ajouter-à-la-règle-du-module-3),
« entre deux dates d'évaluation, rien ne se passe » — et c'est précisément ce que
le lecteur trouve intolérable.

L'objection est légitime, et elle a un nom : **le stop**. Ce module la prend au
sérieux, la déclare correctement, et la mesure.

> ⚠️ **La règle du [module 3](03-la-regle-ecrite-a-l-avance.md) n'est pas modifiée,
> et ne le sera pas.** Ajouter un stop après avoir vu le repli de 2022 serait
> exactement l'ajustement après coup que le
> [§ 3.5](03-la-regle-ecrite-a-l-avance.md#35--le-vrai-danger--les-degrés-de-liberté-de-lanalyste)
> interdit. Ce qui suit est une **variante déclarée** — règle inchangée *plus* un
> stop — dont toutes les versions sont publiées au § 7.2 **avant** le premier
> chiffre, et dont **aucune** ne sera retenue au vu des résultats.

## 7.1 — Ce qu'est un stop, dans le vocabulaire de ce cours

Un ordre stop est une instruction de vente qui se déclenche lorsque le cours
**touche** un seuil. Trois différences avec un verdict, et toutes les trois
comptent :

| | Un verdict de la règle | Un stop |
|---|---|---|
| **Ce qu'il regarde** | cinq critères calculés sur des clôtures | **un seul nombre** : le prix, en séance |
| **Quand il agit** | aux dates de la cadence ([module 5](05-la-cadence-fait-partie-de-la-regle.md)) | **à tout instant**, y compris entre deux dates |
| **Ce qu'il peut dire** | `ACHAT`, `VENTE` ou `ATTENTE` | **sortir**, et rien d'autre |

Le stop est donc **asymétrique par construction**, comme la condition `VENTE` du
[§ 3.4](03-la-regle-ecrite-a-l-avance.md#34--lasymétrie-achat--vente-est-délibérée) :
il ne fait sortir, jamais entrer. Et il est **le seul élément de tout ce cours qui
lise le prix en cours de séance** — les cinq critères, eux, ne connaissent que des
clôtures.

> 🔑 **Un stop n'est pas un critère de plus, c'est un canal de décision
> parallèle.** Il court-circuite la règle, la cadence et les vetos. Une position
> peut donc être fermée un jour où la règle, si on l'avait interrogée, aurait
> répondu `ATTENTE` — et c'est le cas des sept sorties mesurées plus bas.

## 7.2 — Les quatre choses à déclarer, avant tout chiffre

| # | À déclarer | Pourquoi il n'y a pas de valeur par défaut |
|---|---|---|
| 1 | **Le type** : fixe, suiveur, ou indexé sur la volatilité | ils ne mesurent pas la même chose : une perte depuis l'entrée, un abandon depuis le sommet, ou un écart anormal |
| 2 | **Le niveau**, en % ou en multiples d'écart-type | c'est un seuil libre, exactement comme les $35\,\%$ du critère 3 |
| 3 | **La référence de déclenchement** : clôture ou plus bas de séance | un stop sur clôture ne se déclenche pas les mêmes jours qu'un stop en séance |
| 4 | **La règle de réentrée** | **la plus oubliée, et celle qui décide de tout** (§ 7.6) |

Les variantes mesurées dans ce module, publiées ici et closes :

> **Type A — stop fixe** : niveau $= P_{\text{entrée}} \times (1-p)$, avec
> $p \in \{5, 10, 15, 20\}\,\%$, fixé une fois pour toutes à l'entrée.
>
> **Type B — stop suiveur** : niveau $= \max(\text{clôtures depuis l'entrée})
> \times (1-p)$, avec $p \in \{10, 15, 20\}\,\%$, recalculé chaque séance.
>
> **Type C — stop de volatilité** : niveau $= \max(\text{clôtures}) - k\,
> \sigma_{20}$, avec $k \in \{2, 3, 4\}$ et $\sigma_{20} = \sqrt{\texttt{VAR\_20}}$,
> l'écart-type des clôtures sur 20 séances produit par
> [`import_societe.py`](../../../../../python/import_societe.md).
>
> **Déclenchement** : en séance, dès que $\text{Low}_t \le \text{niveau}$, le
> niveau étant calculé sur les seules données antérieures à la séance $t$.
>
> **Exécution** : au niveau du stop ; **sauf si la séance ouvre en dessous**,
> auquel cas l'ordre devient un ordre au marché et s'exécute à l'ouverture
> ([finance § 7.6](../finance/07-couvrir-en-pratique.md)).
>
> **Réentrée** : au premier `ACHAT` postérieur à la sortie, cadence quotidienne —
> la même convention que le [§ 6.1.2](06-cas-pratique.md#612--la-convention-de-cycle-qui-nest-pas-dans-la-règle).

## 7.3 — Ce que chaque stop aurait fait au cycle de 2021-2022

Le cycle du [module 6](06-cas-pratique.md) : entrée le **2021-03-05 à 87,54 €**,
sortie de la règle le **2022-10-04 à 88,13 €**, soit $+0{,}67\,\%$ en 408 séances.
Pendant ces 408 séances, le titre est monté à 110,46 € (le 2022-01-05) puis
descendu à 81,98 € (le 2022-09-29).

| Stop | Niveau | Déclenché | Prix obtenu | Résultat du cycle |
|---|---|---|---|---|
| **Fixe $-5\,\%$** | 83,16 € | **2022-03-07** | 83,16 € | **$-5{,}00\,\%$** |
| Fixe $-10\,\%$ | 78,79 € | **jamais** | — | $+0{,}67\,\%$ *(la règle sort la première)* |
| Fixe $-15\,\%$ | 74,41 € | **jamais** | — | $+0{,}67\,\%$ |
| Fixe $-20\,\%$ | 70,03 € | **jamais** | — | $+0{,}67\,\%$ |
| Suiveur $-10\,\%$ | mobile | 2021-05-13 | 85,61 € | $-2{,}21\,\%$ |
| **Suiveur $-15\,\%$** | mobile | 2021-11-26 | 91,28 € | **$+4{,}28\,\%$** *(gap)* |
| Suiveur $-20\,\%$ | mobile | 2022-03-07 | 83,95 € | $-4{,}11\,\%$ *(gap)* |
| Volatilité $k=2$ | mobile | 2021-03-22 | 89,31 € | $+2{,}02\,\%$ *(gap)* |
| Volatilité $k=3$ | mobile | 2021-03-23 | 88,17 € | $+0{,}71\,\%$ *(gap)* |
| Volatilité $k=4$ | mobile | 2021-03-24 | 85,86 € | $-1{,}93\,\%$ |

Trois lectures, aucune consolante :

1. **Les stops fixes usuels ne servent à rien ici.** Le titre n'est jamais descendu
   à $-10\,\%$ du prix d'entrée : sur ce cycle, le stop à $-10\,\%$ — le plus
   répandu de tous — est un ordre qui n'a jamais existé. Seul le $-5\,\%$ a mordu,
   et il a transformé $+0{,}67\,\%$ en $-5{,}00\,\%$.
2. **Les stops de volatilité sortent en trois séances.** $\sigma_{20}$ valait moins
   de 4 € en mars 2021 : $3\sigma_{20}$ place le seuil à $8\,\%$ sous le sommet,
   c'est-à-dire dans le bruit courant d'un titre à $35\,\%$ de volatilité annuelle.
3. **L'écart entre variantes est de 9 points** — de $-5{,}00$ à $+4{,}28\,\%$ —
   là où la règle seule rendait $+0{,}67\,\%$. **Le stop pèse plus que la règle
   qu'il complète**, et son seuil n'est écrit nulle part dans le module 3.

## 7.4 — Deux sorties sur trois se font par un gap

Le mot *(gap)* du tableau n'est pas un détail d'exécution, c'est le cœur du sujet.

| | Suiveur $-15\,\%$ | Suiveur $-20\,\%$ |
|---|---|---|
| Sommet de référence | 108,26 € | 110,46 € |
| **Niveau du stop** | **92,02 €** | **88,37 €** |
| Clôture de la veille | 102,99 € | 89,08 € |
| **Ouverture du jour** | **91,28 € ($-11{,}37\,\%$)** | **83,95 € ($-5{,}77\,\%$)** |
| Prix réellement obtenu | 91,28 € | 83,95 € |
| **Écart au niveau demandé** | **$-0{,}80\,\%$** | **$-5{,}00\,\%$** |

Le 26 novembre 2021, le cours passe de 102,99 € à 91,28 € **sans coter entre les
deux** : le stop à 92,02 € n'a pas été touché, il a été **enjambé**. L'ordre
devient alors un ordre au marché, et le prix obtenu est celui de l'ouverture.

> ⚠️ **Un stop fixe un déclencheur, jamais un prix.** Les cinq plus fortes
> ouvertures en baisse de la période de détention valent $-11{,}37$, $-5{,}77$,
> $-5{,}00$, $-3{,}54$ et $-2{,}95\,\%$. Un stop placé dans cet intervalle est
> franchi sans être servi à son niveau. La mécanique de l'ordre — seuil de
> déclenchement, plage de déclenchement, ce qui se passe à l'ouverture — est
> traitée au [§ 7.6 du cours finance](../finance/07-couvrir-en-pratique.md), et
> elle n'est pas facultative pour qui pose un stop.

## 7.5 — Sur les cinq années entières

On applique maintenant chaque variante à toute la période, avec la convention de
réentrée du § 7.2 : cadence quotidienne, cycles répétés, position finale valorisée
au 31 décembre 2025, coûts de $0{,}243\,\%$ par aller-retour
([§ 6.6](06-cas-pratique.md#66--le-compte-du-cycle)).

| Variante | Entrées | Sorties par stop | Brut | **Net** |
|---|---|---|---|---|
| **Règle seule, sans stop** | 2 | — | $+80{,}70\,\%$ | **$+79{,}82\,\%$** |
| Règle + fixe $-10\,\%$ | 2 | **0** | $+80{,}70\,\%$ | $+79{,}82\,\%$ |
| Règle + fixe $-20\,\%$ | 2 | **0** | $+80{,}70\,\%$ | $+79{,}82\,\%$ |
| Règle + suiveur $-15\,\%$ | 4 | 3 | $+30{,}52\,\%$ | $+29{,}26\,\%$ |
| Règle + suiveur $-20\,\%$ | 4 | 3 | $+0{,}77\,\%$ | $-0{,}21\,\%$ |
| Règle + volatilité $k=3$ | 9 | **9** | $+1{,}87\,\%$ | $-0{,}33\,\%$ |
| **Règle + suiveur $-10\,\%$** | **6** | **6** | **$-12{,}49\,\%$** | **$-13{,}76\,\%$** |
| *pour mémoire* — le titre conservé | — | — | $+136{,}21\,\%$ | — |

> 🔑 **Aucun stop n'améliore le résultat, et le plus serré le divise par rien —
> il le rend négatif.** Sur cinq ans, la règle sans stop rend $+79{,}82\,\%$ net ;
> avec un stop suiveur à $10\,\%$, elle rend $-13{,}76\,\%$. **93 points d'écart**,
> pour un paramètre que personne ne considère comme faisant partie de la règle.

Et le résultat symétrique, tout aussi net : les deux stops fixes n'ont **jamais**
été atteints en cinq ans. Ils n'ont donc **rien** coûté et **rien** protégé. Un
stop qui ne se déclenche jamais n'est pas une protection prudente, c'est une ligne
de plus dans un document.

## 7.6 — Pourquoi : les cinq réentrées se sont faites plus haut

Le mécanisme est arithmétique, et il tient dans un tableau. Voici les cinq
sorties du stop suiveur à $10\,\%$ et les réentrées qui les ont suivies :

| Sortie au stop | Réentrée au premier `ACHAT` | Écart |
|---|---|---|
| 2021-05-13 à 85,61 € | 2021-11-19 à 100,37 € | **$+17{,}2\,\%$** |
| 2021-11-26 à 91,28 € | 2023-01-27 à 108,53 € | **$+18{,}9\,\%$** |
| 2023-09-25 à 115,88 € | 2024-04-05 à 158,58 € | **$+36{,}8\,\%$** |
| 2024-06-07 à 144,87 € | 2025-02-20 à 158,52 € | **$+9{,}4\,\%$** |
| 2025-04-03 à 149,78 € | 2025-08-25 à 177,26 € | **$+18{,}3\,\%$** |

**Cinq fois sur cinq, le titre a été racheté plus cher qu'il n'avait été vendu.**
Composé, cet écart vaut $+147\,\%$ : c'est exactement la hausse que la variante
avec stop a laissée hors de sa position, et c'est ce qui sépare $-12{,}49\,\%$ de
$+80{,}70\,\%$.

La raison n'est pas la malchance, elle est structurelle et double :

- **Un stop tronque la trajectoire par le bas, mais la réentrée la tronque par le
  haut.** La règle du module 3 n'achète que dans le bas d'un canal
  (critère 3 $< 35\,\%$) et **ne rachète donc jamais tout de suite** : entre la
  sortie et le signal suivant, il s'écoule 6 mois en médiane.
- **Le titre est haussier sur la période** ($+136\,\%$). Toute interruption d'une
  position longue dans une tendance haussière se paie, et se paie d'autant plus
  que l'interruption dure.

> ⚠️ **Ce raisonnement ne vaut que dans ce sens.** Sur une trajectoire baissière,
> les mêmes stops auraient protégé, et le tableau du § 7.5 serait renversé. **On ne
> peut donc rien conclure sur la valeur générale des stops à partir d'un titre qui
> a triplé** — et c'est bien pour cela que le § 7.9 refuse la conclusion que le
> § 7.5 semble offrir.

## 7.7 — Ce qu'un stop ne garantit pas

| Ce qu'on croit qu'un stop fait | Ce qu'il fait |
|---|---|
| Il limite la perte à $p\,\%$ | Il **déclenche** à $p\,\%$. Le prix obtenu est celui du marché à cet instant, $5\,\%$ plus bas le 7 mars 2022 (§ 7.4) |
| Il protège d'un krach | Un krach arrive par **gaps** : le stop est enjambé, pas touché |
| Il ne coûte rien tant qu'il n'est pas touché | Il coûte un aller-retour à chaque déclenchement, et **le droit d'attendre** ([finance § 3.3](../finance/03-marge-appel-de-marge-et-ruine.md)) |
| Il est prudent par nature | Un stop à $-10\,\%$ sur un titre à $30\,\%$ de volatilité est touché **7 fois sur 10 en un an** par le seul bruit ([finance § 3.5](../finance/03-marge-appel-de-marge-et-ruine.md)) |

Les deux dernières lignes sont démontrées dans le cours finance, et pas ici :
**le stop est un appel de marge qu'on se donne à soi-même**, avec la même
mathématique de barrière — le [§ 3.5 de finance](../finance/03-marge-appel-de-marge-et-ruine.md)
en donne la probabilité, et le [§ 7.6](../finance/07-couvrir-en-pratique.md) la
mécanique d'ordre à Euronext Paris.

## 7.8 — Ce qu'il faut déclarer, récapitulé

Le [§ 5.8](05-la-cadence-fait-partie-de-la-regle.md#58--ce-quil-faut-ajouter-à-la-règle-du-module-3)
demandait trois lignes ; il en faut **cinq** pour qu'une règle soit exécutable :

| # | Ce qui doit être déclaré | Module |
|---|---|---|
| 1 | Les critères, les seuils et les vetos | [3](03-la-regle-ecrite-a-l-avance.md) |
| 2 | La cadence, et le traitement des dates hors séance | [5](05-la-cadence-fait-partie-de-la-regle.md) |
| 3 | Ce qui se passe entre deux dates d'évaluation | [5](05-la-cadence-fait-partie-de-la-regle.md) |
| 4 | La convention de cycle et l'hypothèse d'exécution | [6](06-cas-pratique.md) |
| 5 | **Le stop : type, niveau, référence, et règle de réentrée** | **7** |

> 🔑 **Les trois dernières lignes ne sont pas dans la règle du module 3, et elles
> pèsent plus lourd que lui.** La cadence vaut 122 points d'écart
> ([§ 5.6](05-la-cadence-fait-partie-de-la-regle.md#56--et-si-lon-autorisait-plusieurs-cycles)),
> le stop 93, l'hypothèse d'exécution retourne le signe d'un cycle
> ([§ 6.6](06-cas-pratique.md#66--le-compte-du-cycle)). **Une règle publiée sans
> elles n'est pas une règle incomplète : c'est une règle dont les paramètres les
> plus influents sont restés implicites.**

## 7.9 — Ce que ce module ne montre pas

- **Un titre, une période, dix variantes.** Airbus a été multiplié par 2,4 sur la
  période. Sur une trajectoire baissière, les mêmes stops auraient protégé, et il
  n'y a **aucune** raison de généraliser le § 7.5. Ce module montre qu'un stop
  **change beaucoup**, pas qu'il nuit.
- **Retenir le stop fixe à $-10\,\%$ parce qu'il ne s'est jamais déclenché serait
  la faute exacte du [§ 3.5](03-la-regle-ecrite-a-l-avance.md#35--le-vrai-danger--les-degrés-de-liberté-de-lanalyste).**
  Il ne s'est pas déclenché *sur ces cinq années-là* ; c'est un fait daté, pas une
  propriété.
- **Le déclenchement est mesuré sur le `Low` de séance**, une donnée de fin de
  journée. Un stop réel est évalué en continu, sur des prix que les CSV de ce dépôt
  ne contiennent pas ; les dates de déclenchement sont donc exactes, les heures
  inconnues.
- **L'exécution au niveau du stop hors gap est optimiste** : elle suppose une
  contrepartie immédiate au seuil, sans glissement en séance.
- **Aucun stop d'achat, aucun stop suiveur asymétrique, aucun stop temporel.**
  Sortir au bout de $n$ séances est une variante courante ; elle n'est pas
  mesurée ici.
- **La taille de position reste hors champ**, et c'est elle qui donne son sens au
  stop : un stop à $-10\,\%$ sur $2\,\%$ du portefeuille et sur $50\,\%$ ne
  protègent pas la même chose ([finance § 3.5](../finance/03-marge-appel-de-marge-et-ruine.md)).

> *Ceci est la sortie d'une règle écrite appliquée à des données passées, pas une
> recommandation.*

---

⬅️ [Module 6 — Cas pratique : un cycle `ACHAT` → `VENTE`, 2021-2025](06-cas-pratique.md) ·
🏠 [README du cours](README.md)
