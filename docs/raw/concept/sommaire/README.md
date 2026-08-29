# Concepts — les mathématiques derrière `historique_sbf250.py`

Cinq cours autonomes, plus le document de référence [`modele.md`](../../modele.md). Ils
répondent, dans l'ordre, aux questions que pose une droite de régression tracée sur une série de
cours — la dernière étant : *et maintenant, qu'en fait-on ?*

| Question | Cours | Volume |
|---|---|---|
| Que **calcule**-t-on, géométriquement ? | [Algèbre linéaire euclidienne](../algebre/README.md) | 7 h 30 |
| Comment **dérive**-t-on et **intègre**-t-on ces quantités ? | [Analyse](analyse.md) | 20 h |
| Le résultat est-il **réel**, ou du hasard d'échantillonnage ? | [Statistique](statistique.md) | 56 h |
| Quelle **décision** en tirer — taille, protection, composition ? | [Finance](../finance/README.md) | 12 h 15 |

## Arborescence

```
investissement/
├── sommaire/                            les index
│   ├── README.md                        ← ce fichier
│   ├── analyse.md                       sommaire de la partie analyse
│   └── statistique.md                   sommaire de la partie statistique
│
├── modele/                              le document de référence : variance résiduelle minimale
│   ├── modele.md                        énoncé, théorème et plan de la preuve
│   └── 01..09-*.md                      une page par étape de la démonstration
│
├── algebre/                             8 modules — produit scalaire, projection, dimension
│
├── analyse/
│   ├── convexite/                       9 modules — Jensen, minimisation, mesures de risque
│   └── derivation-et-integration/       9 modules — Taylor, intégrale, jacobien
│
├── statistique/
│   ├── mathematique/                    25 modules — loi, moments, TCL, χ², inférence
│   └── loi-de-student/                  8 modules — le cours dédié, à σ inconnu
│
└── finance/                             10 modules — levier, couverture, portefeuille optimal
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
algèbre 1→4  →  analyse/dérivation 1, 5, 7  →  modele.md
```

**Le chemin complet** — pouvoir défendre un résultat :

```
algèbre 1→8  →  analyse/dérivation 1→9  →  statistique/mathématique 1→19  →  analyse/convexité 1→9  →  Student 0→9
```

**Le chemin de la décision** — passer du résultat à une position :

```
modele.md  →  finance 1→4 (levier)  →  finance 5→7 (couverture)  →  finance 8→9 (portefeuille)  →  finance 10 (le cas complet)
```

**Par question posée :**

| Ce que vous cherchez | Où aller |
|---|---|
| Pourquoi le diviseur $n-1$ | [Algèbre § 5](../algebre/05-supplementaire-orthogonal-et-dimension.md) puis [Statistique § 16](../statistique/mathematique/16-theoreme-de-fisher-cochran.md) |
| D'où vient le $1{,}96$ | [Statistique § 18](../statistique/mathematique/18-intervalle-de-confiance.md) |
| Quand l'approximation normale tient | [Statistique § 11 bis](../statistique/mathematique/11bis-convergence-en-loi.md) et [§ 13](../statistique/mathematique/13-portee-et-limites-du-tcl.md) |
| Pourquoi la moyenne des rendements ment | [Analyse/convexité § 5](../analyse/convexite/05-jensen-probabiliste.md) |
| Pourquoi la VaR est une mauvaise mesure | [Analyse/convexité § 8](../analyse/convexite/08-convexite-et-mesures-de-risque.md) |
| D'où vient une densité | [Analyse/dérivation § 9](../analyse/derivation-et-integration/09-changement-de-variable-et-densites.md) |
| Comment dériver en notation matricielle | [Analyse/dérivation § 7](../analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md) |
| Quelle taille de position prendre | [Finance § 3](../finance/03-marge-appel-de-marge-et-ruine.md) et [§ 4](../finance/04-levier-optimal-et-drag.md) |
| Comment couvrir un portefeuille, et avec quoi | [Finance § 6](../finance/06-la-couverture-optimale.md) et [§ 7](../finance/07-couvrir-en-pratique.md) |
| Ce que le SRD, le PEA et la VAD autorisent | [Finance § 1](../finance/01-le-cadre-cac40-et-le-srd.md) |
| Pourquoi $1/N$ bat l'optimisation | [Finance § 9](../finance/09-contraintes-reelles-et-estimation.md) |
| Un portefeuille complet, chiffré de bout en bout | [Finance § 10](../finance/10-exemple-de-portefeuille.md) |

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
vraisemblance** ([Analyse/dérivation § 7.4](../analyse/derivation-et-integration/07-calcul-matriciel-des-derivees.md)),
$n-1$ est celui **sans biais** ([Statistique § 16](../statistique/mathematique/16-theoreme-de-fisher-cochran.md)).
Deux critères, deux diviseurs.
