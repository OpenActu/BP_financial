---
name: experience-review
description: Passe une expérience de docs/done/experimentation/ en revue par les trois agents du dépôt — chartiste, trading, sorosien. Chacun étudie les paramètres d'entrée, les rapports mensuels, les graphiques et le bilan, puis propose cinq pistes d'amélioration. Le résultat est écrit dans review.md, à la racine de l'expérience. Utiliser quand l'utilisateur invoque /experience-review, ou demande de relire, critiquer ou améliorer une expérience.
---

# experience-review

`docs/done/experimentation/` consigne des expériences datées : un protocole
déclaré avant la première séance, des rapports mensuels, des graphiques, un
bilan. Cette skill les fait relire par les **trois agents du dépôt**, chacun sous
son angle propre, et rassemble leurs conclusions dans un `review.md`.

## ⚠️ Le piège que cette skill doit éviter

Une expérience porte sur une période **passée**, dont le résultat est connu de
qui rédige la revue. Proposer « il aurait fallu un seuil à 40 % » en sachant ce
qu'a fait l'année, c'est du **rétro-ajustement**, pas une amélioration — c'est
même le premier des [cinq pièges de l'alpha](../../../docs/raw/concept/semestre4/alpha/04-cinq-pieges.md).

D'où la contrainte, à imposer aux trois agents et à rappeler dans `review.md` :

> **Chaque piste doit être classée dans l'une des deux catégories, explicitement.**
>
> - **Catégorie A — indépendante du résultat.** Elle aurait été proposable avant
>   la première séance, en lisant le seul protocole : une lacune de mesure, une
>   convention non déclarée, un contrôle absent, un biais non corrigé.
> - **Catégorie B — suggérée par le résultat.** Elle ne se formule qu'en
>   connaissant ce qui s'est produit. Elle reste **recevable si elle est nommée
>   comme telle** et accompagnée du protocole qui permettrait de la tester
>   honnêtement — sur une autre période, un autre univers, ou en aveugle.
>
> Une piste de catégorie B présentée comme un enseignement est une faute. Une
> piste de catégorie B **déclarée** est une hypothèse pour l'expérience suivante.

Le décompte A/B doit apparaître dans la synthèse : une revue qui ne rend que des
pistes B a relu le résultat, pas le protocole.

## Procédure

### 1. Localiser l'expérience et en dresser l'inventaire

L'argument est un chemin (par défaut, la plus récente de
`docs/done/experimentation/`). Vérifier que s'y trouvent au minimum :

| Fichier | Rôle dans la revue |
|---|---|
| `README.md` | **les paramètres d'entrée** : univers, dotation, score, seuils, cadence, coûts, référence |
| `bilan-2022.md` (ou équivalent) | le compte de l'année, les positions, les contrefactuels |
| `rapports/*.md` | les décisions mois par mois, avec leur justification |
| `graphiques/*.svg` | l'évolution tracée, jalonnée aux dates d'exécution |
| `*.csv` | les données brutes : critères, classement, ordres, valorisation |
| le moteur `.py` et son miroir `.md` | ce que le protocole fait réellement |

Si l'un manque, le dire et poursuivre sans lui — ne rien inventer.

### 2. Lancer les trois agents, en parallèle

Un seul message, trois appels — les trois lectures sont indépendantes.
**Donner à chacun le chemin de l'expérience, la liste des fichiers, et la
contrainte A/B ci-dessus, recopiée.** Demander à chacun **exactement cinq
pistes**, numérotées, chacune avec :

1. un titre court ;
2. **A** ou **B**, et la justification du classement ;
3. ce qu'elle change concrètement dans le protocole ;
4. ce qu'elle coûterait — en données, en calcul, en frais si elle touche
   l'exécution ;
5. **comment on saurait qu'elle améliore quelque chose** — la mesure, et son
   incertitude. Une piste dont l'effet n'est pas mesurable doit le dire.

Les angles, à ne pas laisser se recouvrir :

- **`chartiste`** — la géométrie et les signaux. Les fenêtres 20/120, les
  encadrements, la position dans le canal, les ruptures, la qualité des droites
  (portée, épisodes de contact), ce que les graphiques montrent et ce qu'ils
  masquent. Il a produit les notes de perspective : il peut dire lesquelles ont
  été contredites, et si le score exploite bien ce qu'il mesure.
- **`trading`** — la performance et la règle. Alpha et son incertitude, bêta,
  coûts d'exécution, construction du score, seuils d'entrée et de sortie,
  hystérésis, cadence, choix de la référence, biais de l'univers, et ce que
  douze mois permettent ou non de conclure.
- **`sorosien`** — la réflexivité. Le protocole voit-il les séquences
  auto-renforçantes entre cours et fondamentaux ? Une règle purement chartiste
  peut-elle capter un cycle boom-bust ? Où l'expérience se rend-elle aveugle à
  ce qu'elle prétend suivre ? **« Aucune séquence réflexive identifiable » reste
  une conclusion admissible** — s'il la retient, il doit dire ce qui manquerait
  pour en identifier une.

Rappeler à chacun sa limite de charte : **aucun conseil en investissement,
aucun dimensionnement de position, aucune prédiction.** Une piste d'amélioration
porte sur le protocole, jamais sur un titre à acheter.

### 3. Assembler `review.md`

À écrire à la **racine de l'expérience**, à côté du `README.md`. Plan :

1. **Ce qui a été relu** — l'inventaire du § 1, avec les chiffres clés du bilan,
   pour qu'on lise la revue sans rouvrir le reste.
2. **La contrainte A/B**, recopiée : le lecteur doit savoir dès le début à quelle
   aune juger les pistes.
3. **Une section par agent** — son angle en une phrase, ce qu'il a trouvé, puis
   ses cinq pistes.
4. **La synthèse** — les quinze pistes en un tableau, triées par catégorie puis
   par ce qu'elles coûtent ; le décompte A/B ; et les convergences entre agents,
   qui valent plus qu'une piste isolée.
5. **Ce que cette revue ne peut pas établir** — au minimum : qu'une piste
   appliquée aurait amélioré le résultat, ce qui demanderait de rejouer l'année
   en la connaissant.

Les chiffres cités doivent venir des fichiers de l'expérience, jamais d'une
mémoire d'agent. En cas de désaccord entre deux agents sur un nombre, **le
signaler plutôt que de trancher** : un désaccord chiffré est une information.

### 4. Vérifier

- Les liens relatifs de `review.md` résolvent (`README.md`, `bilan-*.md`,
  `rapports/*.md`) ;
- aucun chiffre du bilan n'est recopié de travers — les recouper une fois ;
- le décompte A/B annoncé correspond aux pistes listées ;
- la revue ne contient **aucune recommandation d'achat ou de vente**.

Puis le dire à l'utilisateur : le chemin du fichier, le décompte A/B, et les
deux ou trois pistes sur lesquelles les agents convergent.

## Ce que cette skill ne fait pas

- **Elle ne modifie pas l'expérience.** Une revue se pose à côté ; appliquer une
  piste, c'est une expérience suivante, avec son propre protocole déclaré avant.
- **Elle ne re-lance pas le moteur** ni ne recalcule le bilan. Si les chiffres
  paraissent faux, elle le signale — elle ne les corrige pas.
- **Elle ne classe pas les pistes par gain espéré.** Personne ne connaît le gain
  d'une piste non testée, et l'ordonner par gain supposé reviendrait à réintroduire
  le rétro-ajustement par la porte de la synthèse.
