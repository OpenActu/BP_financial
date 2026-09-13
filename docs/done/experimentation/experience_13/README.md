# Expérience 13 — la droite apporte-t-elle ce que son absence n'apporte pas ?

> Ce qui compte n'est pas de savoir si vous avez raison ou tort, mais combien
> vous gagnez quand vous avez raison et combien vous perdez quand vous avez tort.
> — George Soros

Les expériences 1 à 12 jouent un portefeuille. **Celle-ci n'en joue aucun.** Elle
ne passe aucun ordre, ne détient aucune position, ne mesure aucun alpha. Elle
mesure **une grandeur sur des événements datés**, et elle le fait parce que
l'alpha ne peut rien trancher ici — le dépôt l'a établi assez de fois.

Son objet tient en une question :

> **L'écart réduit à une droite extrapolée porte-t-il une information qu'une
> standardisation _sans droite_ ne porte pas ?**

---

## ⚠️ Ce que cette expérience déclare avant tout

### 1. Le résultat qui l'a fait naître est déjà connu, et il est de catégorie B

Il se publie ici, en tête, plutôt qu'en conclusion — la discipline de
l'[expérience 11](../experience_11/README.md). Sur **2019-2026**, 13 valeurs,
l'agent `chartiste` a mesuré qu'un franchissement de `−3 s` est suivi d'un excès
de **+2,37 points à 60 séances** contre un panier apparié, IC₉₅
**[+0,88 ; +3,94]** sur 57 grappes de mois.

**Cette mesure a produit l'hypothèse ; elle ne peut donc pas la tester.** C'est
une piste de **catégorie B**, au même titre que la coupe à −15 % de
l'[expérience 10](../experience_10/README.md) — qui n'a pas survécu à son univers
inédit. La fenêtre 2019-2026 est **brûlée** et n'apparaît nulle part dans ce qui
suit.

### 2. Le seuil de 3 s n'est identifié par rien

La même mesure rend **1,41 / 1,82 / 2,37 / 2,05** points pour
`k = 2 / 2,5 / 3 / 4`, intervalles largement recouvrants. Il n'y a **pas d'effet
de seuil à 3** : il y a une grandeur continue qui croît avec la distance sous la
droite. Le seuil n'est donc pas l'hypothèse de cette expérience — il n'est qu'un
**échantillonneur d'événements**, et les trois valeurs `k ∈ {2 ; 2,5 ; 3}` sont
jouées et publiées toutes les trois.

### 3. Deux mesures préalables ne se corroborent pas

L'agent `trading`, sur la même période mais en **transversal quotidien**, trouve
le rang d'écart réduit le plus bas associé à **+0,137 point** à 20 séances —
dans le bruit, pour un EMD de ± 1,2. Constructions différentes, donc pas de
contradiction formelle, **mais aucun renfort mutuel non plus**. Une expérience
qui part d'un résultat non répliqué doit le dire.

### 4. Ce qu'elle peut établir, et ce qu'elle ne pourra pas

**EMD publié avant toute issue**, et **mesuré** plutôt qu'extrapolé. L'appel
`mesure.py --dimensionner` compte les événements et les grappes de mois, et
mesure la dispersion **inconditionnelle** de l'issue — sur des dates tirées au
hasard, jamais sur celles qu'un franchissement désigne :

| Cellule                                   | Événements | Grappes de mois | **EMD**    |
| ----------------------------------------- | ---------- | --------------- | ---------- |
| **R, bas, k = 3** *(cellule de décision)* | 1 948      | 92              | **± 2,06** |
| R, bas, k = 2                             | 2 358      | 99              | ± 1,98     |
| R, haut, k = 3                            | 1 785      | 89              | ± 2,09     |
| T1, bas, k = 3                            | 616        | 58              | ± 2,59     |
| **T2, bas, k = 3**                        | 464        | **20**          | **± 4,41** |

Dispersion inconditionnelle de l'issue à 60 séances : **10,06 points**, sur
12 482 tirages. 1 673 franchissements sont écartés faute des 60 séances d'issue,
et aucun couple ne manque de fenêtre d'ajustement.

> ⚠️ **Cette mesure contredit l'estimation que ce protocole portait d'abord.**
> J'avais extrapolé « ± 1,1 à ± 1,5 point » depuis les 57 grappes de la fenêtre
> brûlée. Le dispositif réel donne **± 2,0 à ± 2,1** sur les cellules de R : la
> dispersion à 60 séances vaut 10,06 points et non les ~6 % supposés, et les
> grappes plafonnent vers 92 au lieu des 110 à 150 espérées — neuf ans de
> franchissements n'occupent qu'une centaine de mois distincts.
>
> **Le critère de décision n'est pas modifié pour autant.** Son plancher reste à
> +1,00 point. L'ajuster après avoir vu la puissance serait la faute que ce dépôt
> proscrit — une règle retouchée après coup ne teste plus rien.

> 🔑 **Conséquence, déclarée avant de jouer : cette expérience est faiblement
> puissante, et son test principal est le plus faible de tous.**
>
> - Un effet de **+2,37 points** — celui qui a fait naître l'hypothèse — est
>   **juste au bord** du détectable (± 2,06), pas confortablement au-dessus.
> - Le plancher de **+1,00 point** de la condition 1 est **inférieur à l'EMD** :
>   un effet réel d'un point satisferait la condition 1 sans jamais satisfaire la
>   condition 2. Les deux peuvent donc se contredire, et c'est **attendu**.
> - Le **test principal** `R − max(T1, T2)` est apparié sur les mois, or T2 à
>   `k = 3` n'occupe que **20 grappes** : c'est lui qui borne la puissance de
>   l'ensemble, à un EMD pire que ± 4.
>
> **L'issue la plus probable de cette expérience est donc « non concluant ».**
> Ce n'est pas un verdict d'inutilité, et je le déclare maintenant pour que la
> zone grise ne soit pas relue après coup comme un échec — ni comme un succès.

### 5. Une correction déclarée, faite après un premier passage

La première exécution s'est **arrêtée d'elle-même** : le témoin T0 à
`(bas, k = 3)` rendait −0,45 avec un IC₉₅ de [−0,86 ; −0,04], excluant zéro. Le
moteur a donc imprimé `DISPOSITIF DEFECTUEUX` et n'a publié aucun verdict, comme
le protocole l'exige.

**La cause est identifiée, et c'est une incohérence du moteur, pas un défaut des
données** : la correction de Holm était appliquée aux 18 cellules principales et
à **aucune** des 6 cellules de T0. Six intervalles à 95 % non corrigés ferment la
vanne **26,5 % du temps sous H₀** — le contrôle de validité se déclenchait donc
plus souvent que le test qu'il protège.

| Contrôle | Valeur |
|---|---|
| T0, toutes cellules confondues | **−0,054 point** sur 12 482 tirages |
| Cellules excluant zéro **sans** correction | une seule, `(bas, k = 3)`, p = 0,0260 |
| Cellules excluant zéro **après Holm** | **aucune** — p ajustée 0,1560 |

**La correction consiste à appliquer Holm à T0 comme partout ailleurs**, sur sa
propre famille de 6 tests. Elle est faite **après** avoir vu le déclenchement, ce
que ce dépôt n'autorise qu'à trois conditions, toutes remplies ici :

1. **rien n'était publié** — le moteur avait précisément refusé de publier ;
2. **la cause est identifiée** et vérifiée par une mesure séparée ;
3. **la correction est neutre sur l'issue**, et c'est démontrable : les 18
   cellules principales sont **toutes** à `p Holm = 1,0000`, et le verdict est
   `INUTILE` avec ou sans la vanne. Une correction qui ne peut pas changer la
   conclusion ne peut pas être soupçonnée de la fabriquer.

> ⚠️ **Le critère de décision, lui, n'a pas bougé d'une virgule** — ni son
> plancher de +1,00 point, ni ses quatre conditions, ni le choix de `k = 3`. Seul
> le contrôle de validité a été rendu cohérent avec le reste du moteur.

---

## L'univers — le CAC 40 point-in-time, et le trou qu'il laisse

**115 dates d'ancrage**, une toutes les 20 séances du **2010-01-04** au
**2018-11-30**, calendrier de séance pris sur MC.PA — membre de l'indice sur
toute la période. À chaque date, la composition **réelle** de l'indice, lue sur
[`bnains.org`](https://www.bnains.org/archives/histocac/compocac.php) et figée
dans [`univers.csv`](univers.csv) : **4 596 couples (date, valeur), 53 valeurs
distinctes**.

Que la source honore bien la date est vérifié et non supposé : entre 2010 et
2018, **8 sorties et 8 entrées**. Quatre ancrages de 2018 ne rendent que
**39 valeurs** — l'indice y a réellement tourné à 39, la page le dit dans son
propre titre.

### Les dix valeurs écartées, et pourquoi c'est grave

| Valeur          | Ancrages | Motif, strictement factuel                             |
| --------------- | -------- | ------------------------------------------------------ |
| Technip         | 115      | aucune série servie (candidat `TEC.PA`)                |
| Unibail-Rodamco | 115      | aucune série en euros (`UL.PA`, `URW.AS`)              |
| LafargeHolcim   | 108      | servie **en CHF seulement** (`HOLN.SW`, 2 514 séances) |
| Peugeot S.A.    | 83       | aucune série servie (`UG.PA`)                          |
| EDF             | 77       | aucune série servie (`EDF.PA`)                         |
| Alcatel         | 65       | aucune série servie (`ALU.PA`)                         |
| Gemalto         | 28       | aucune série servie (`GTO.AS`)                         |
| Suez            | 26       | aucune série servie (`SEV.PA`)                         |
| Natixis         | 12       | aucune série servie (`KN.PA`)                          |
| Dexia           | 10       | aucune série servie (`DEXB.BR`)                        |

**639 couples sur 4 596, soit 13,9 % de l'univers.**

Mesuré avant toute issue : il reste **32 à 37 valeurs recevables par ancrage** —
le minimum de 32 tombe au début de 2010. Le panier apparié compte donc toujours
au moins **31 valeurs**, et la garde « panier de moins de 10 » du moteur ne peut
pas se déclencher. Autre effet de bord, mesuré lui aussi avant : le calendrier ne
laisse que **19 séances après le dernier ancrage**, si bien que les **trois
derniers ancrages ne peuvent produire aucun événement retenu** — il leur faudrait
61 séances.

> ⚠️ **Ce trou n'est pas aléatoire : c'est le biais du survivant en personne.**
> Ces dix-là sont les faillites, les fusions et les rachats — précisément les
> valeurs dont l'absence flatte tout résultat. L'expérience **ne corrige donc
> pas** le biais du survivant ; elle le **déclare et le chiffre**, ce qu'aucune
> note de bas de page ne remplace.
>
> **Ce qui sauve le plan d'expérience**, c'est que le résultat principal est un
> **écart entre bras mesurés sur les mêmes valeurs, aux mêmes dates**. Une valeur
> absente pénalise les quatre bras à l'identique. Le biais mordrait une
> affirmation de rendement absolu ; il s'annule très largement dans une
> différence de bras. **Aucun rendement absolu n'est donc publié comme résultat.**

Mélanger deux devises fabriquerait du rendement de change : LafargeHolcim est
écartée pour cette seule raison, sa série existant. C'est l'invariant du dépôt,
appliqué sans exception.

---

## La règle, écrite avant la première mesure

### Les quatre bras

À chaque date d'ancrage `d` et pour chaque valeur recevable de l'indice ce
jour-là, sur les **250 séances closes en `d`** — jamais une de plus :

| Bras   | Grandeur, à la séance `d + j`                                               |
| ------ | --------------------------------------------------------------------------- |
| **R**  | `z = (C − VAL₂₅₀ − r·j) / s₂₅₀` — la bande de régression, gelée à l'ancrage |
| **T1** | `z = (C − E₂₅₀) / sd(C₂₅₀)` — **sans droite ni pente**                      |
| **T2** | `z = (C_{d+j} − C_{d+j−20}) / (σ_journalier·√20)` — marche aléatoire        |
| **T0** | dates tirées au hasard, même nombre d'événements, `random.Random(2010)`     |

`VAL₂₅₀`, `r` et `s₂₅₀` sont ceux de [`modele.md`](../../../raw/modele.md) :
moindres carrés sur les rangs de séance, variance de population, `s` sans biais.
**T1 est le témoin que réclamait le § 9 de
[`largeur-de-bande-fiable.md`](../../../raw/lab/largeur-de-bande-fiable.md)** : si
T1 rend le même excès que R, la droite n'apporte rien.

### L'événement, l'issue

- **Événement** : la **première** séance `j ≥ 1` où `z < −k` (bras bas) ou
  `z > +k` (bras haut). Un couple (ancrage, valeur, bras) produit **au plus un**
  événement. Les séances suivantes du même épisode ne comptent pas.
- **Issue** : l'excès de rendement à **h = 60 séances** contre le **panier
  équipondéré des autres valeurs recevables de l'indice à cette date**, la valeur
  percée exclue.
- Un **événement** n'est retenu que si ses `h = 60` séances d'issue tiennent
  **avant le 2018-12-31** ; sinon il est écarté et compté. C'est cette borne — et
  non une borne sur l'ancrage — qui garantit qu'aucune séance de 2019, la fenêtre
  brûlée, n'entre dans un résultat. Le nombre d'écartés est publié **par année** :
  l'effet de bord est réel sur 2018 et doit se lire, pas se supposer négligeable.
- `k ∈ {2 ; 2,5 ; 3}`, les trois joués, les trois publiés.

### Le critère de décision

**Le critère s'évalue à `k = 3`** — le niveau avec lequel l'hypothèse est arrivée.
`k = 2` et `k = 2,5` sont joués et publiés comme **sensibilité**, et ne peuvent
pas décider à sa place : les lire pour trancher serait choisir le seuil après
avoir vu les trois.

> **L'écart réduit à une droite est déclaré UTILE si, et seulement si, les quatre
> conditions tiennent ensemble :**
>
> 1. l'excès moyen à `h = 60` après franchissement **bas** est **≥ +1,00 point** ;
> 2. son **IC₉₅ par grappes de mois calendaires** exclut zéro ;
> 3. **— test principal —** l'écart `R − max(T1, T2)` est **positif** et son IC₉₅
>    par grappes exclut zéro ;
> 4. **aucune année seule ne porte l'effet** : le retrait de l'année la plus
>    favorable laisse l'excès **≥ +0,50 point**.
>
> **Sinon : INUTILE**, et le verdict est publié tel quel.

La condition 3 est la seule qui porte sur **la droite** plutôt que sur la sortie
de bande. C'est pourquoi elle est le test principal, et elle est désignée comme
tel **avant** toute mesure.

**Contrôles de validité du dispositif**, à vérifier avant de lire quoi que ce
soit : T0 doit rendre un résultat **compatible avec zéro**, et le bras **haut**
de R doit être publié à côté du bras bas. Si T0 s'écarte de zéro, le dispositif
est déclaré défectueux et **rien n'est publié**.

**Bootstrap** par blocs de mois calendaires, 3 000 tirages, `random.Random(2010)`
déclarée. **Correction de Holm** sur la famille des tests : 3 bras × 2 sens × 3
valeurs de `k`.

---

## Ce que cette expérience ne pourra pas établir

- **Que 3 s soit le bon seuil.** La monotonie en `k` dit qu'aucun ne l'est.
- **Une régularité par valeur.** Sur la fenêtre brûlée, la dispersion entre
  titres allait de **−7,3 à +6,5 points**. Une moyenne de panier ne dit rien
  d'une ligne.
- **Que la bande fonctionne comme intervalle.** Cette question est déjà tranchée,
  négativement et deux fois : la bande `± 2 s` ne couvre que 76 à 88 % dès la
  séance suivante, et un témoin sans droite est **mieux calibré** qu'elle
  (`k₉₅` de 1,79 à 2,08 contre 2,8 à 3,0).
- **Une causalité.** L'excès mesuré est une association de calendrier.
- **Que l'effet survive aux coûts et à l'exécution.** L'excès net des frais est
  publié à côté du brut, mais **aucune position n'est dimensionnée**, et le coût
  retenu est une **approximation déclarée**, jamais un élément du verdict.

  > ⚠️ **Les coûts sont mesurés sur le marché d'aujourd'hui, pas sur 2010-2018.**
  > `couts_transaction.py` rend **0,544 %** l'aller-retour pour LVMH (droit
  > français, 204,7 Md) et **0,246 %** pour Airbus (droit néerlandais, TTF
  > exemptée) — et **0,687 %** pour Vallourec, dont la capitalisation de 4,9 Md
  > fait exploser l'impact de marché. Appliquer ces trois chiffres à des séances
  > de 2010 est un **anachronisme assumé** : les volumes et les capitalisations de
  > l'époque n'étaient pas ceux-là. Le moteur retient donc **un taux plat par pays
  > d'émetteur**, ce qui **flatte les petites capitalisations**. Comme le critère
  > de décision se joue à +1,00 point et non au coût, cette approximation ne peut
  > pas changer le verdict.
- **Que l'effet existe hors des régimes de krach et de rebond.** 2010-2018
  contient 2011 et 2015 ; le panier apparié retire le niveau du marché, il ne
  retire pas le régime.

---

## Les fichiers

| Fichier                      | Contenu                                                                            |
| ---------------------------- | ---------------------------------------------------------------------------------- |
| [`univers.csv`](univers.csv) | les 4 596 couples (date, valeur) : ISIN, Sicovam, nom, ticker, recevabilité, motif |
| `mesure.py` · `mesure.md`    | le moteur et son **miroir d'exécution**, qui fait autorité                         |
| `evenements.csv`             | un événement par ligne : ancrage, valeur, bras, `k`, date, `z`, excès à 60 séances |
| `graphiques/`                | deux figures SVG : le **graphe en forêt** des 18 cellules, et les **événements par mois** |
| `bilan.md`                   | le verdict, rendu par le critère ci-dessus                                         |

> Le moteur ne s'appelle pas `journal.py` comme ceux des douze autres : il ne
> tient aucun journal, puisqu'il n'y a **ni portefeuille ni mois à raconter**. La
> règle du miroir markdown s'applique néanmoins telle quelle — `mesure.py` ⇔
> `mesure.md` —, et le markdown fait autorité.

## Reproduction

```bash
python python/import_societe.py MC.PA --debut 2009-01-01 --fin 2019-01-02   # calendrier
python docs/done/experimentation/experience_13/mesure.py --dimensionner      # sans les issues
python docs/done/experimentation/experience_13/mesure.py                     # la mesure
```

Les 43 séries recevables se régénèrent par le même appel, une par ticker de
[`univers.csv`](univers.csv). `docs/raw/data/quotes/` est exclu de git : ces
données se refont d'un appel, contrairement à `univers.csv`, qui est **figé et
suivi** parce qu'il dépend d'une source extérieure susceptible de changer.
