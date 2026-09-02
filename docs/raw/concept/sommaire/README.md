# Concepts — les mathématiques derrière `import_societe.py`

Dix cours autonomes, plus le document de référence [`modele.md`](../../modele.md). Ils
répondent, dans l'ordre, aux questions que pose une droite de régression tracée sur une série de
cours — la dernière étant : *et maintenant, qu'en fait-on ?*

| Question | Cours | Volume |
|---|---|---|
| Que **calcule**-t-on, géométriquement ? | [Algèbre linéaire euclidienne](../semestre1/algebre/README.md) | 9 h 30 |
| Comment **dérive**-t-on et **intègre**-t-on ces quantités ? | [Analyse](analyse.md) | 20 h |
| Le résultat est-il **réel**, ou du hasard d'échantillonnage ? | [Statistique](statistique.md) | 56 h |
| Quelle **décision** en tirer — taille, protection, composition ? | [Finance](../semestre4/finance/README.md) | 12 h 45 |
| De combien le cours **s'écarte**-t-il de sa tendance ? | [Canal de régression](../semestre3/canal/README.md) | 6 h |
| Entre quelles **bornes** le cours évolue-t-il ? | [Encadrement](../semestre3/encadrement/README.md) | 4 h |
| Ce rendement doit-il quelque chose au **talent** ou au marché ? | [L'alpha](../semestre4/alpha/README.md) | 5 h |
| Comment passer d'une **figure** à une décision publiable ? | [De la figure à la décision](../semestre4/trading/README.md) | 7 h |
| Que valent les **comptes** derrière le cours ? | [Les fondamentaux](../semestre4/fondamentaux/README.md) | 5 h |

> 🗓️ **L'ordre dans lequel les suivre est dans [`planning.md`](../../planning.md)**, qui répartit les dix cours en quatre
> semestres. L'arborescence ci-dessous porte ce découpage.

> ☑️ **L'avancement se coche dans [`avancement.md`](avancement.md)**, qui reprend les 109 modules
> ligne à ligne, dans l'ordre du parcours.

## Arborescence

```
concept/
├── semestre1/                           les outils mathématiques
│   ├── algebre/                         11 modules — espace vectoriel, produit scalaire, projection, dimension
│   └── analyse/
│       ├── derivation-et-integration/   9 modules — Taylor, intégrale, jacobien
│       └── convexite/                   9 modules — Jensen, minimisation, mesures de risque
│
├── semestre2/                           l'aléatoire
│   └── statistique/
│       └── mathematique/                26 modules — loi, moments, TCL, χ², inférence
│
├── semestre3/                           l'inférence et le modèle
│   ├── statistique/
│   │   └── loi-de-student/              8 modules — le cours dédié, à σ inconnu
│   ├── modele/                          9 étapes — la démonstration (l'énoncé est dans docs/raw/modele.md)
│   ├── canal/                           6 modules — largeurs, levier, sorties, canal glissant
│   └── encadrement/                     4 modules — enveloppe convexe, portée, segmentation
│
├── semestre4/                           la décision
│   ├── alpha/                           5 modules — modèle de marché, horizon de mesure, pièges
│   ├── fondamentaux/                    5 modules — PER, P/B, VE/EBITDA, ROE : ce qu'ils disent et ce qu'ils taisent
│   ├── trading/                         7 modules — des objets du chartiste à la règle écrite et son verdict
│   └── finance/                         10 modules — levier, couverture, portefeuille optimal
│
└── sommaire/                            les index, hors parcours
    ├── README.md                        ← ce fichier
    ├── analyse.md                       sommaire de la partie analyse
    └── statistique.md                   sommaire de la partie statistique
```

> ℹ️ **Règle d'arborescence.** Un répertoire contient **soit** des sous-répertoires, **soit** des
> fichiers, jamais les deux. Les répertoires de regroupement (`analyse/`, `statistique/`) ne
> portent donc aucun fichier ; leurs sommaires vivent dans [`sommaire/`](README.md), et le
> document de référence dans [`modele/`](../../modele.md).


## Les deux sommaires de partie

| Partie | Sommaire | Contenu |
|---|---|---|
| Analyse | [`analyse.md`](analyse.md) | Dérivation et intégration · Convexité |
| Statistique | [`statistique.md`](statistique.md) | Statistique mathématique · Loi de Student |

## Dans quel ordre les lire

Aucun de ces cours n'exige les autres en entier ; chacun indique en tête ce qu'il emprunte.

**Le chemin le plus court vers `modele.md`** — comprendre ce que le script calcule :

```
algèbre 1→6  →  analyse/dérivation 1, 5, 7  →  modele.md
```

**Le chemin complet** — pouvoir défendre un résultat :

```
algèbre 1→10  →  analyse/dérivation 1→9  →  statistique/mathématique 1→19  →  analyse/convexité 1→9  →  Student 0→9
```

**Le chemin de la décision** — passer du résultat à une position :

```
modele.md  →  finance 1→4 (levier)  →  finance 5→7 (couverture)  →  finance 8→9 (portefeuille)  →  finance 10 (le cas complet)
```

**Par question posée :**

| Ce que vous cherchez | Où aller |
|---|---|
| Pourquoi le diviseur $n-1$ | [Algèbre § 8](../semestre1/algebre/08-degres-de-liberte-et-centrage.md) puis [Statistique § 16](../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md) |
| D'où vient le $1{,}96$ | [Statistique § 18](../semestre2/statistique/mathematique/18-intervalle-de-confiance.md) |
| Quand l'approximation normale tient | [Statistique § 11 bis](../semestre2/statistique/mathematique/11bis-convergence-en-loi.md) et [§ 13](../semestre2/statistique/mathematique/13-portee-et-limites-du-tcl.md) |
| Pourquoi la moyenne des rendements ment | [Analyse/convexité § 5](../semestre1/analyse/convexite/05-jensen-probabiliste.md) |
| Pourquoi la VaR est une mauvaise mesure | [Analyse/convexité § 8](../semestre1/analyse/convexite/08-convexite-et-mesures-de-risque.md) |
| D'où vient une densité | [Analyse/dérivation § 9](../semestre1/analyse/derivation-et-integration/09-changement-de-variable-et-densites.md) |
| Comment dériver en notation matricielle | [Analyse/dérivation § 7](../semestre1/analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md) |
| Quelle taille de position prendre | [Finance § 3](../semestre4/finance/03-marge-appel-de-marge-et-ruine.md) et [§ 4](../semestre4/finance/04-levier-optimal-et-drag.md) |
| Comment couvrir un portefeuille, et avec quoi | [Finance § 6](../semestre4/finance/06-la-couverture-optimale.md) et [§ 7](../semestre4/finance/07-couvrir-en-pratique.md) |
| Ce que le SRD, le PEA et la VAD autorisent | [Finance § 1](../semestre4/finance/01-le-cadre-cac40-et-le-srd.md) |
| Pourquoi $1/N$ bat l'optimisation | [Finance § 9](../semestre4/finance/09-contraintes-reelles-et-estimation.md) |
| Un portefeuille complet, chiffré de bout en bout | [Finance § 10](../semestre4/finance/10-exemple-de-portefeuille.md) |

## Ce que les cours se doivent les uns aux autres

| Fournisseur | Client | Ce qui transite |
|---|---|---|
| Algèbre | Statistique | Projection, orthogonalité, dimension → degrés de liberté, Fisher–Cochran |
| Algèbre | Analyse/convexité | $\Sigma$ matrice de Gram → convexité de $w^{\top}\Sigma w$ |
| Analyse/dérivation | Analyse/convexité | Différentiabilité, gradient, Hessienne |
| Analyse/dérivation | Statistique | Le jacobien → toutes les densités ; $\Gamma$ ; l'intégrale de Gauss |
| Analyse/convexité | Statistique | Jensen → biais de $S$, drag de volatilité |
| Statistique | Loi de Student | $\chi^2$, Fisher–Cochran, intervalle de confiance |
| `modele.md` | Finance | $\operatorname{Cov}/\operatorname{Var}$ et $1-\rho^2$ → **le ratio de couverture** (finance § 6) |
| Analyse/convexité | Finance | Jensen → le drag de volatilité ; $w^{\top}\Sigma w$ convexe → Markowitz |
| Algèbre | Finance | Projection orthogonale → couvrir, c'est projeter |
| Loi de Student | Finance | L'incertitude sur $\beta$ et sur $\mu$ → demi-Kelly, échec de Markowitz estimé |
| Canal · Encadrement · Alpha | Trading | Objets graphiques, position dans le canal et IC de l'alpha → les cinq critères de la règle |
| Modèle · Alpha | Fondamentaux | La régression de l'étape 7 → $P/B$ contre ROE ; les tests multiples → les réserves sur un échantillon de huit valeurs |

## Conventions communes

| Point | Règle |
|---|---|
| Langue | Français, y compris les commentaires de code |
| Structure d'un module | Question traitée → contenu → **simulation** → exercices → à retenir |
| Navigation | Pied de page `⬅️ précédent · ➡️ suivant · 🏠 sommaire` |
| ⭐ | Marque les modules décisifs, dans le titre **et** dans le sommaire du cours |
| Simulations | `numpy`, `scipy`, `matplotlib` ; à écrire soi-même, corrigés donnés |
| Chiffres | Tout tableau numérique publié a été produit par le code qui l'accompagne |

```bash
pip install numpy scipy matplotlib
```

## Divergence de convention à connaître

[`modele.md`](../../modele.md) normalise les moments par $n$ ; le cours de statistique utilise $n-1$ pour
la variance d'échantillon. Ce n'est pas une incohérence : $n$ est l'estimateur du **maximum de
vraisemblance** ([Analyse/dérivation § 7.4](../semestre1/analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md)),
$n-1$ est celui **sans biais** ([Statistique § 16](../semestre2/statistique/mathematique/16-theoreme-de-fisher-cochran.md)).
Deux critères, deux diviseurs.
