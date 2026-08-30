# Module 3 — Segmenter un historique long

**Prérequis :** modules [1](01-la-droite-qui-ne-coupe-rien.md) et [2](02-portee-et-episodes-de-contact.md).
**Ce qu'on établit ici :** pourquoi l'enveloppe convexe appliquée d'un bloc à quatre ans ne produit rien d'exploitable, et par quoi la remplacer.

---

## 3.1 — L'échec, mesuré

Appliquons littéralement le module 1 aux **1027 séances** d'Airbus, sans
découpage. La chaîne supérieure compte 5 sommets, donc 4 arêtes :

| Arête                       | Portée           | Pente               |
| --------------------------- | ---------------- | ------------------- |
| 2020-01-02 → 2020-01-22     | 14 séances       | $+0{,}236$ €/séance |
| 2020-01-22 → 2020-01-24     | 2 séances        | $+0{,}037$          |
| **2020-01-24 → 2023-12-14** | **1001 séances** | $+0{,}008$          |
| 2023-12-14 → 2023-12-29     | 9 séances        | $-0{,}373$          |

Et la chaîne inférieure, 6 arêtes, dont une de **616 séances** et une de 271.

Le verdict est sans appel. Une arête de 1001 séances relie janvier 2020 à
décembre 2023 en passant au-dessus du krach, du rebond et de trois années de
cotation : c'est une contrainte géométrique exacte et une information nulle. Sa
pente, $+0{,}008$ €/séance, ne décrit aucun régime qui ait jamais existé.

> ⚠️ **L'enveloppe convexe est un objet global.** Plus la fenêtre est longue, plus
> ses arêtes sont longues et plus elles ignorent ce qui se passe entre leurs
> extrémités. Le nombre d'arêtes croît en $O(\log n)$ pour des données aléatoires,
> pas en $O(n)$ : quadrupler l'historique n'ajoute qu'une poignée de droites.

C'est exactement le défaut symétrique de celui du
[canal glissant](../canal/05-canal-glissant.md) : là-bas, une fenêtre trop longue
estimait très précisément une pente périmée ; ici, elle produit une droite exacte
et vide.

## 3.2 — La partition en blocs

La réponse est de découper l'historique en blocs consécutifs et d'appliquer les
modules 1 et 2 **dans chaque bloc**.

```
BLOC = 120                                    # une fenêtre semestrielle
blocs = [(s, min(s + BLOC, n)) for s in range(0, n, BLOC)]
if blocs[-1][1] - blocs[-1][0] < 40:          # reliquat trop court
    blocs[-2] = (blocs[-2][0], blocs[-1][1])  # fusionné avec le précédent
    blocs.pop()
```

Sur Airbus : **9 blocs**, huit de 120 séances et un dernier de 67. Chaque bloc
reçoit son propre seuil de portée ($n/4$, donc 30 pour un bloc plein, 16 pour le
dernier) et sa propre tolérance $\varepsilon$.

Résultat — les 18 droites, une paire par bloc :

| Bloc | Période           | Résistance : pente / portée / épisodes | Support : pente / portée / épisodes | Largeur finale |
| ---- | ----------------- | -------------------------------------- | ----------------------------------- | -------------- |
| 1    | 2020-01 → 2020-06 | $-0{,}611$ / 81 / 3                    | $+0{,}002$ / 38 / 4                 | 45,8 %         |
| 2    | 2020-06 → 2020-12 | $+0{,}216$ / 118 / 7                   | $-0{,}033$ / 64 / 6                 | 43,3 %         |
| 3    | 2020-12 → 2021-05 | $+0{,}082$ / 64 / 2                    | $+0{,}142$ / 76 / 3                 | 13,9 %         |
| 4    | 2021-05 → 2021-11 | $-0{,}042$ / 74 / 4                    | $+0{,}051$ / 79 / 3                 | 8,7 %          |
| 5    | 2021-11 → 2022-05 | $-0{,}193$ / 43 / 3                    | $+0{,}311$ / 34 / 2                 | 5,8 %          |
| 6    | 2022-05 → 2022-10 | $-0{,}188$ / 45 / 2                    | $-0{,}035$ / 64 / 4                 | 15,8 %         |
| 7    | 2022-10 → 2023-04 | $+0{,}022$ / 31 / 4                    | $+0{,}130$ / 105 / 2                | 8,9 %          |
| 8    | 2023-04 → 2023-09 | $-0{,}046$ / 32 / 2                    | $+0{,}020$ / 97 / 2                 | 11,8 %         |
| 9    | 2023-09 → 2023-12 | $+0{,}274$ / 54 / 8                    | $+0{,}363$ / 43 / 10                | 5,9 %          |

La [figure du cours](README.md#la-figure-du-cours) montre ces droites : neuf paires
en pointillé, chacune bornée à son bloc. On y voit d'un coup d'œil ce que le tableau
énumère — l'effondrement de la largeur du canal après 2020, et les pentes qui
changent de signe d'un bloc au suivant.

*(Contrôle : les 18 droites donnent 0 traversée, comme l'exige le
[§ 1.4](01-la-droite-qui-ne-coupe-rien.md#14--les-deux-contrôles-à-exécuter).)*

Deux lectures que la version globale rendait impossibles :

- **La largeur relative du canal chute de 45,8 % à 5,8 %** entre le krach et le
  début 2022, puis remonte. C'est une mesure de régime de volatilité, lisible
  directement.
- **Les pentes changent de signe** d'un bloc à l'autre. Aucune droite unique ne
  pouvait rendre cela.

## 3.3 — Les blocs ne sont pas le canal actif

Piège suivant, et il est subtil : le dernier bloc de la partition **n'est pas** le
canal en vigueur aujourd'hui.

Sur Airbus, le dernier bloc va du 2023-09-26 au 2023-12-29 et ne compte que
**67 séances** — parce que 1027 n'est pas un multiple de 120, pas parce qu'un
régime aurait commencé fin septembre. Sa découpe est un artefact du point de
départ de la partition.

> **Règle du canal actif.** Pour lire la situation courante, ne pas prendre le
> dernier bloc : recalculer sur une fenêtre **ancrée à droite**, les $N$ dernières
> séances, quelle que soit la partition.

Ancrée sur les 120 dernières séances (2023-07-13 → 2023-12-29), la fenêtre active
donne un canal **différent** de celui du bloc 9 :

|                     | Bloc 9 (67 séances) | **Fenêtre active (120 séances)** |
| ------------------- | ------------------- | -------------------------------- |
| Résistance : pente  | $+0{,}274$          | $+0{,}048$                       |
| Résistance : portée | 54                  | 102                              |
| Support : pente     | $+0{,}363$          | $+0{,}363$                       |

Le support est le même — c'est la même arête, ancrée au 23 octobre. La résistance,
elle, est tout autre : la fenêtre longue voit le sommet du 25 juillet, que le
bloc 9 ignore parce qu'il commence après. **Une résistance dépend d'un sommet que
la fenêtre contient ou non** ; c'est la fragilité principale de la méthode, et la
raison de toujours publier la fenêtre.

## 3.4 — Choisir la longueur de bloc

Le même arbitrage biais–variance que pour le
[canal glissant](../canal/05-canal-glissant.md#53--choisir-la-longueur-de-fenêtre),
mais sans la formule : ici, rien ne se précise en $n^{-3/2}$, parce qu'il n'y a
pas d'estimateur.

| Longueur       | Effet                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------ |
| Courte (20–60) | beaucoup de blocs, arêtes courtes, pentes instables ; la portée minimale devient très permissive |
| Moyenne (120)  | un régime semestriel par bloc ; retenu ici                                                       |
| Longue (250+)  | on retombe vers le défaut du § 3.1 : peu d'arêtes, très longues                                  |

Le seul garde-fou général : **la longueur de bloc se fixe avant de regarder les
résultats**, et se publie. Ajuster la découpe jusqu'à obtenir la figure voulue est
la façon la plus simple de fabriquer n'importe quelle conclusion à partir de
n'importe quelle série.

---

⬅️ [Module 2 — Portée et épisodes de contact](02-portee-et-episodes-de-contact.md) ·
➡️ [Module 4 — Lire l'encadrement](04-lire-l-encadrement.md)
