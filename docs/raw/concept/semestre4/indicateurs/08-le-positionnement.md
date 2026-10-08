# Module 8 — Indicateur 10 : ce que croient les autres

**Prérequis :** [module 2](02-les-attentes-de-benefices.md), et le [module 5 du cours finance](../finance/05-la-vente-a-decouvert.md) (la vente à découvert).
**Ce qu'on établit ici :** pourquoi le positionnement des investisseurs est l'indicateur décisif chez Soros comme chez Steinhardt, ce que l'on peut en mesurer à Paris — les positions courtes publiées par l'AMF et le volume relatif —, et pourquoi presque tout le reste est invisible.

---

## 8.1 — La seconde moitié de la boucle

Les indicateurs 1 à 9 mesurent des **fondamentaux** et des **opinions déclarées**.
Aucun ne dit combien d'argent est engagé derrière ces opinions. Or c'est ce qui
fait bouger les prix :

- chez Soros, la boucle réflexive a deux moitiés : les fondamentaux qui
  agissent sur les perceptions, et les perceptions qui agissent sur les prix
  **par les positions prises**. Un biais qui n'est pas investi ne déplace rien ;
- chez Steinhardt, une vue divergente rapporte quand le consensus **se
  retourne**. Elle rapporte d'autant plus que le consensus était investi : ceux
  qui doivent défaire leurs positions font le mouvement.

Une position très partagée — un « trade encombré » — est fragile pour une raison
mécanique : à la première déception, tous veulent sortir par la même porte.

> 🔑 **C'est l'indicateur décisif, et le moins mesurable.** Les positions des
> fonds, des banques et des particuliers ne sont publiques que par fragments,
> avec retard, et au-dessus de seuils élevés. Ce module dit ce qu'on en voit, et
> surtout ce qu'on n'en voit pas.

## 8.2 — Les positions courtes publiées

Depuis le règlement européen sur la vente à découvert (2012), toute **position
courte nette** sur une action cotée doit être :

- **notifiée** à l'autorité de marché dès 0,1 % du capital ;
- **publiée** dès **0,5 %**, puis à chaque palier de 0,1 point.

L'AMF publie l'historique complet de ces positions depuis novembre 2012, en
données ouvertes sur data.gouv.fr. Chaque ligne donne le détenteur, l'émetteur,
l'ISIN, le ratio en pourcentage du capital, la date de la position, sa **date de
début de publication**, et sa date de fin de publication.

**Ces dates de publication font de ce fichier une source point-in-time**, ce
qu'aucune source fondamentale du dépôt n'est. Pour savoir ce qui était public au
jour $j$, il suffit de garder les lignes publiées au plus tard à $j$ et pas encore
retirées, puis, pour chaque détenteur, **la plus récente** :

$$\text{courtes}(j) = \sum_{\text{détenteurs}} \text{ratio de la dernière ligne publiée} \le j$$

Une position qui repasse sous 0,5 % fait l'objet d'une dernière publication à son
nouveau niveau (par exemple 0,35 %), que l'AMF retire ensuite : sa date de fin de
publication la fait sortir du calcul.

**Au 8 octobre 2026** :

| | Positions publiées | Détenteurs | Sur 90 jours |
|---|---|---|---|
| **TTE.PA** | **0,77 %** du capital | 1 | −0,11 pt |
| les sept autres | 0,00 % | 0 | — |

Le seul détenteur publié sur TotalEnergies est Elliott Investment Management,
dont la position publiée est passée de 0,88 % (mai) à 0,77 % (fin août). Les sept autres
valeurs n'ont **aucune** position publiée en vigueur. Le seuil de lecture
déclaré — « notable » à partir de 2 % du capital — n'est atteint nulle part.

## 8.3 — Ce qui ne se voit pas

L'absence de position publiée n'est pas une absence de vendeurs.

| Invisible | Pourquoi |
|---|---|
| les positions entre 0,1 % et 0,5 % | notifiées au régulateur, pas publiées. Cent fonds à 0,4 % chacun font 40 % du capital, et zéro ligne |
| les positions **longues** | publiques seulement aux franchissements de seuils de détention (5 %, 10 %…), par d'autres déclarations |
| le **sens** d'une position courte | une vente à découvert peut couvrir une obligation convertible, un panier, une paire de valeurs : ce n'est pas forcément un pari contre la société |
| les particuliers et les fonds indiciels | aucun seuil ne les rend visibles, et ce sont souvent eux qui achètent en fin de boom |

> ⚠️ **Le cas d'Elliott le montre.** Un fonds activiste qui est aussi créancier,
> porteur d'options ou engagé dans un arbitrage peut porter une position courte
> nette sans parier sur une baisse de la société. Le chiffre dit qu'une position
> existe ; il ne dit pas pourquoi.

La littérature, surtout américaine, trouve qu'une forte proportion de titres
vendus à découvert précède en moyenne des rendements plus faibles (Desai et
al., 2002 ; Asquith, Pathak et Ritter, 2005) : les vendeurs à découvert sont en
moyenne mieux informés. Mais cette moyenne porte sur des milliers de valeurs et
sur des positions totales, pas sur les seules positions publiées d'un grand
groupe parisien.

## 8.4 — Le volume relatif

Une mesure plus grossière, mais disponible pour toute valeur : le volume échangé
récemment, rapporté à son volume habituel.

$$\text{volume relatif} = \frac{\text{moyenne des volumes des 20 dernières séances}}{\text{moyenne des volumes des 250 dernières séances}}$$

| | AIR | MC | OR | SAN | TTE | BNP | SU | ORA |
|---|---|---|---|---|---|---|---|---|
| Volume relatif | 1,00 | 1,20 | 0,85 | 1,02 | 0,91 | 0,99 | 1,18 | **1,26** |

Aucune valeur ne dépasse le seuil déclaré de **1,5**. Un volume inhabituel signale
qu'un groupe d'investisseurs **change de position** — qu'il entre ou qu'il
sorte : le volume ne dit pas le sens. Combiné au sens du cours et à celui des
révisions, il dit si un mouvement est **large** ou porté par peu d'échanges.

## 8.5 — Le signal fort : la divergence

Aucun de ces chiffres ne se lit en niveau. Ce qui intéresse Soros et Steinhardt,
c'est la **divergence** entre ce que font les prix et ce que disent les autres
indicateurs :

| Divergence | Ce qu'elle suggère |
|---|---|
| le cours monte, les révisions baissent | le prix suit le biais, la réalité ne le suit plus : le stade 5 du boom-bust ([module 9](09-assembler-la-sequence.md)) |
| les positions courtes montent sur une valeur au multiple élevé | des investisseurs informés parient contre la croissance supposée : marqueur **R3** |
| fort volume sur une baisse après une longue hausse | les détenteurs sortent : la porte se rétrécit |
| le cours baisse, les révisions montent | le prix doute de ce que les analystes voient : la situation inverse, où Steinhardt cherchait ses achats |

Au 8 octobre 2026, aucune des huit valeurs ne présente l'une de ces
configurations avec une netteté que les seuils déclarés retiennent. LVMH s'en
approche (cours en forte baisse sur trois ans, révisions 2027 en baisse), mais
c'est une divergence **dans le même sens**, pas une divergence entre prix et
opinion.

## Exercices

**E8.1.** Le fichier de l'AMF contient, pour un même ISIN, ces lignes (date de
début de publication, détenteur, ratio, fin de publication) : 2026-03-02, A,
0,62, — ; 2026-05-10, A, 0,71, — ; 2026-06-01, B, 0,55, — ; 2026-08-15, B, 0,38,
— ; 2026-09-01, C, 0,50, —. Calculer les positions publiées au 2026-07-01 et au
2026-10-01.

**E8.2.** Pourquoi le volume relatif ne suffit-il pas à dire si des investisseurs
**entrent** ou **sortent** ?

**E8.3.** Un analyste écrit : « aucune position courte n'est publiée sur Airbus,
le marché est unanimement optimiste ». Relever les deux erreurs.

### Corrigés

**E8.1.** Au 2026-07-01 : A 0,71 (sa plus récente) + B 0,55 = **1,26 %**, deux
détenteurs. Au 2026-10-01 : A 0,71 + B 0,38 (dernière publication, sous le seuil)
+ C 0,50 = **1,59 %**, trois lignes en vigueur. La position de B à 0,38 % est sa
publication de sortie : elle est comptée telle quelle, ce que fait le script.

**E8.2.** Chaque échange a un acheteur et un vendeur. Le volume mesure
l'intensité du changement de mains, pas le camp qui l'emporte. Le sens se lit
dans le prix pendant ces échanges.

**E8.3.** (1) Les positions sous 0,5 % ne sont pas publiées : l'absence de ligne
ne prouve pas l'absence de vendeurs. (2) Les positions courtes ne disent rien
des longues ; « unanimement optimiste » demanderait de connaître les positions
de tous les détenteurs.

## Ce qu'il faut retenir

1. Le positionnement est la **seconde moitié** de la boucle réflexive : un biais
   n'agit sur les prix que s'il est investi.
2. Les positions courtes nettes de l'AMF sont publiées à partir de **0,5 %**, avec
   leurs dates : c'est une source **point-in-time**, rare dans le dépôt. Au
   8 octobre 2026, seule TotalEnergies en porte une (0,77 %).
3. L'essentiel est **invisible** : les positions sous le seuil, les positions
   longues, le motif des positions courtes.
4. Le signal se lit dans la **divergence** entre le prix et les autres
   indicateurs, jamais dans un niveau.

---

⬅️ [Module 7 — Le monde autour](07-change-croissance-inflation.md) ·
➡️ [Module 9 — Assembler : la séquence et la règle écrite](09-assembler-la-sequence.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
