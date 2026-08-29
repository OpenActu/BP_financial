# Cours — Statistique mathématique

Cours de statistique probabiliste générale : variable aléatoire, moments, transformées d'une loi,
loi normale, vecteur gaussien, convergences, lois d'échantillonnage, inférence par intervalle.
Niveau **bac+2**.

## Pourquoi ce cours dans ce dépôt

Le document [`modele.md`](../../modele/modele.md) et le script `historique_sbf250.py` produisent des
quantités purement **descriptives** : une moyenne, une variance, une corrélation, une pente. Le
[cours d'algèbre linéaire](../../algebre/README.md) montre que ce sont des objets **géométriques**,
vrais sur n'importe quels $n$ points.

Ni l'un ni l'autre ne permet de répondre à la question qui décide :

> La tendance que je viens de calculer est-elle **réelle**, ou n'est-elle que le produit du
> hasard d'échantillonnage ?

Répondre exige un **modèle génératif** — c'est-à-dire des probabilités. Ce cours construit
l'appareil complet : à quoi ressemble la loi d'une moyenne, d'une variance, d'une somme de
carrés ; ce que le hasard garantit et ce qu'il ne garantit pas.

## Fil directeur

Un unique mécanisme, décliné : **transformer une somme de variables indépendantes en un produit
de fonctions**. Il donne successivement la stabilité gaussienne (module 8), le théorème central
limite (module 12), et — combiné à la géométrie — l'indépendance de $\bar X$ et $S^2$
(module 16).

En amont, une seule ligne de partage structure la partie I : l'espérance est **linéaire sans
condition**, la variance ne l'est **que sous décorrélation**. Toute la fragilité de l'inférence
tient dans cet écart.

## Progression

### Partie 0 — Fondations

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 1 | [Variable aléatoire et loi](01-variable-aleatoire-et-loi.md) | 1 h 15 | Loi, densité, répartition, quantile, i.i.d. |
| 2 | [**L'espérance**](02-esperance.md) ⭐ | 1 h 15 | La linéarité, qui n'exige rien ; $E(\bar X)=\mu$ |
| 3 | [**Variance et moments**](03-variance-et-moments.md) ⭐ | 1 h 15 | L'erreur type $\sigma/\sqrt n$ ; asymétrie et kurtosis |
| 4 | [**Covariance et corrélation**](04-covariance-et-correlation.md) ⭐ | 1 h 15 | $w^{\top}\Sigma w$, et les quatre cécités de $\rho$ |

### Partie I — Transformées d'une loi

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 5 | [La fonction génératrice des moments](05-fonction-generatrice-des-moments.md) | 1 h | Somme → produit, et pourquoi la FGM ne suffit pas |
| 6 | [La fonction caractéristique](06-fonction-caracteristique.md) | 1 h | (P1)–(P4) démontrées, Lévy, cumulants |

### Partie I bis — Le catalogue des lois usuelles

Six modules de même plan : définition → espérance et variance **sans transformée** → les mêmes
**par la fonction caractéristique** → propriétés → **exemple complet** chiffré → simulation. Ils
font tourner les outils des parties 0 et I sur les six lois qui reviennent partout.

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 6a | [La loi de Bernoulli](06a-loi-de-bernoulli.md) | 45 min | $p$, $pq$ ; $\mathbf 1_A$ et $E(\mathbf 1_A)=P(A)$ ; $pq\le1/4$ |
| 6b | [La loi binomiale](06b-loi-binomiale.md) | 1 h | $np$, $npq$ par trois chemins ; correction de continuité |
| 6c | [La loi de Poisson](06c-loi-de-poisson.md) | 1 h | $E=\operatorname{Var}=\lambda$ ; tous les cumulants ; limite binomiale |
| 6d | [La loi uniforme](06d-loi-uniforme.md) | 1 h | $(b-a)^2/12$ ; transformation inverse et PIT |
| 6e | [La loi exponentielle](06e-loi-exponentielle.md) | 1 h | $1/\lambda$, $1/\lambda^2$ ; absence de mémoire ; dualité Poisson |
| 6f | [La loi normale](06f-loi-normale.md) | 1 h | $\mu$, $\sigma^2$ ; $E(Z^{2k})=(2k-1)!!$ ; VaR et ses limites |

> 🔑 **Ce que ces six modules ajoutent au reste du cours : une signature testable par loi.**
> $pq\le1/4$, $E=\operatorname{Var}=\lambda$, coefficient de variation $=1$, $\beta_2=3$. Ajuster
> un modèle demande deux paramètres ; le **valider** demande de vérifier sa signature — et c'est
> la seule partie du travail qui protège.

### Partie II — La loi normale

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 7 | [**La loi normale et ses transformées**](07-loi-normale-et-ses-transformees.md) ⭐ | 1 h | $M_Z=e^{t^2/2}$, $\varphi_Z=e^{-t^2/2}$, $E(Z^4)=3$ |
| 8 | [**Addition de lois et stabilité gaussienne**](08-addition-de-lois-et-stabilite-gaussienne.md) ⭐ | 1 h | $\bar X\sim\mathcal N(\mu,\sigma^2/n)$, exactement |

### Partie III — Le vecteur gaussien

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 9 | [Le vecteur gaussien](09-vecteur-gaussien.md) | 1 h | Marges gaussiennes ≠ vecteur gaussien |
| 10 | [**Décorrélation et indépendance**](10-decorrelation-et-independance.md) ⭐ | 1 h | L'équivalence, privilège de la gaussienne |
| 11 | [**Invariance par rotation et lemme de projection**](11-invariance-par-rotation-et-lemme-de-projection.md) ⭐ | 1 h 15 | L'outil du module 16 |

### Partie IV — Convergences

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 11 bis | [La convergence en loi](11bis-convergence-en-loi.md) | 1 h 30 | La définition, Slutsky, et le triangle $\mathcal B\to\mathcal P\to\mathcal N$ |
| 12 | [**Le théorème central limite**](12-theoreme-central-limite.md) ⭐ | 2 h | Énoncé, démonstration, ce sur quoi il porte |
| 13 | [Portée et limites du TCL](13-portee-et-limites-du-tcl.md) | 1 h 30 | $\gamma_1/\sqrt n$ au lieu de « $n\ge30$ » |
| 14 | [**Dépendance et échec du TCL**](14-dependance-et-echec-du-tcl.md) ⭐ | 1 h 15 | Les deux régimes, et le renversement |

> ℹ️ **Le module 11 bis est un préalable de vocabulaire**, pas une suite du module 11 : il ne
> dépend que des modules 1, 3 et 6. Le suffixe marque son insertion **avant** le TCL, dont il
> définit la notation $\xrightarrow{\mathcal L}$ et dont il fournit les outils de transport
> (Slutsky, delta-méthode) utilisés en partie VI.

### Partie V — Lois d'échantillonnage

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 15 | [La loi du $\chi^2$](15-loi-du-chi2.md) | 1 h 30 | $\chi^2$ = carré de norme ; d'où vient le $n-1$ |
| 16 | [**Théorème de Fisher–Cochran**](16-theoreme-de-fisher-cochran.md) ⭐ | 2 h | $\bar X \perp\!\!\!\perp S^2$ démontré |

### Partie VI — Inférence

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 17 | [Estimation et quantité pivotale](17-estimation-et-quantite-pivotale.md) | 1 h | Le pivot, mécanisme central |
| 18 | [**L'intervalle de confiance**](18-intervalle-de-confiance.md) ⭐ | 1 h 30 | Le retournement, et le 1,96 |
| 19 | [**Interpréter la confiance**](19-interpretation-de-la-confiance.md) ⭐ | 1 h 15 | Pourquoi « 95 % de chances » est faux |

**Volume total** : ≈ 32 h (dont 5 h 45 pour le catalogue 6a–6f), à répartir sur 7 à 9
semaines.

## Parcours

Les modules se lisent **dans l'ordre** : chacun n'utilise que les précédents. Six raccourcis
sont possibles selon l'objectif :

| Objectif | Modules |
|---|---|
| Réviser les fondations seules | 1 → 2 → 3 → 4 |
| Maîtriser les lois usuelles et leurs preuves | 5 → 6 → 6a → … → 6f |
| Comprendre d'où vient le $n-1$ | 7 → 9 → 10 → 11 → 15 → 16 |
| Savoir quand l'approximation normale tient | 3 → 11 bis → 12 → 13 → 14 |
| Choisir entre binomiale, Poisson et normale | 6b → 6c → 11 bis |
| Construire et interpréter un intervalle | 2 → 3 → 8 → 17 → 18 → 19 |

Le catalogue **6a–6f** peut aussi se lire à la carte, une loi à la fois, en cours de route : seuls
les modules 6b (qui suppose 6a) et 6e (qui suppose 6c) s'enchaînent réellement.

⚠️ Le module 11 suppose acquis les
[modules 4 à 6 du cours d'algèbre](../../algebre/README.md) — projection orthogonale,
$\mathbb R^n=F\oplus F^\perp$, bases orthonormées. Si ces objets sont flous, traitez-les d'abord :
le § 11.3 devient alors une formalité.

## Les cinq modules décisifs

- **Module 2 — L'espérance.** Sa linéarité **n'exige aucune hypothèse** — cas unique dans tout le
  cours. Voir précisément ce qu'elle protège, et ce qu'elle ne protège pas, évite la moitié des
  erreurs qui suivent.
- **Module 4 — La covariance.** Celui qui installe le terme croisé dont vivent la diversification,
  la matrice $\Sigma$, et l'écart entre décorrélation et indépendance.
- **Module 11 — Le lemme de projection.** Celui qui fournit un véritable **outil** plutôt qu'une
  mise en contexte. Le module 16 se borne à l'appliquer.
- **Module 14 — La dépendance.** Celui dont l'absence coûte le plus cher en pratique : augmenter
  $n$ répare la non-normalité et **aggrave** la dépendance.
- **Module 19 — L'interprétation.** Celui dont l'oubli produit l'erreur la plus répandue de toute
  la statistique appliquée.

## Ce que ce cours ne contient pas

La **loi de Student** elle-même — sa construction, ses propriétés, son emploi en test et en
régression — fait l'objet d'un [cours dédié](../loi-de-student/README.md), qui commence exactement
là où celui-ci s'arrête : au moment où l'on remplace le $\sigma$ connu du module 18 par la
variable aléatoire $S$.

De même, la **géométrie euclidienne** sous-jacente (projection, orthogonalité, degrés de liberté
comme dimension) relève du [cours d'algèbre linéaire](../../algebre/README.md), qui est purement
déterministe.

Les **calculs de densité par jacobien** — celui du vecteur gaussien ([§ 9.4](09-vecteur-gaussien.md)),
celui du $\chi^2(1)$ ([§ 15.3](15-loi-du-chi2.md)), la transformation inverse et la PIT
([§ 6d.4](06d-loi-uniforme.md)) — relèvent du
[cours de dérivation et intégration](../../analyse/derivation-et-integration/README.md), qui les démontre tous
à partir d'un seul théorème de changement de variables.

L'**inégalité de Jensen**, énoncée et admise au [§ 2.5](02-esperance.md), relève quant à elle du
[cours d'analyse sur la convexité](../../analyse/convexite/README.md) : elle y est démontrée
([module 5](../../analyse/convexite/05-jensen-probabiliste.md)), ainsi que ses conséquences chiffrées — le
biais de $S$, le drag de volatilité, la prime de risque.

> 📐 **Le module 4 a un jumeau déterministe.** Le
> [module 8 du cours d'algèbre](../../algebre/08-covariance-et-produit-scalaire.md) traite la
> covariance **empirique** — celle de $n$ nombres déjà observés — et démontre qu'elle est un
> produit scalaire. Le module 4 ci-dessus traite la covariance **théorique**, celle de deux
> variables aléatoires. Mêmes propriétés, mêmes conséquences, deux objets distincts : ne les
> confondez pas, mais lisez-les ensemble.

## Principe pédagogique

Chaque module se conclut par une **simulation à écrire soi-même**. La probabilité en dimension
$n$ est un domaine où l'intuition trompe — décorrélation qui n'est pas indépendance, couverture
bilatérale qui masque deux queues fausses, dépendance qui empire avec les données — et la
simulation est le seul garde-fou fiable à ce niveau. Les corrigés sont donnés, mais la valeur est
dans l'écriture, pas dans la lecture.

```bash
pip install numpy scipy matplotlib
```

> ⚠️ Écrivez les simulations **vous-même** plutôt que d'appeler les fonctions toutes faites.
> Reconstruire une statistique à la main est ce qui fait passer le cours de la lecture à la
> compréhension.

## Notations retenues dans tout le cours

| Symbole | Sens |
|---|---|
| $X$ / $x$ | Variable aléatoire (non observée) / valeur observée |
| $n$, $k$ | Taille de l'échantillon, degrés de liberté |
| $\mu,\ \sigma^2$ | Espérance et variance **théoriques** (paramètres inconnus) |
| $\bar X,\ S^2$ | Moyenne et variance **empiriques** (statistiques calculables) |
| $f$, $F$, $q_p$ | Densité, fonction de répartition, quantile d'ordre $p$ |
| $M_X(t)$, $\varphi_X(t)$ | FGM $E(e^{tX})$ et fonction caractéristique $E(e^{itX})$ |
| $\kappa_j$, $\gamma_1$, $\beta_2$ | Cumulant d'ordre $j$, asymétrie, kurtosis |
| $\operatorname{Cov}$, $\rho$, $\Sigma$ | Covariance, corrélation, matrice de covariance |
| $\Phi$, $z_p$ | Fonction de répartition de $\mathcal N(0,1)$ et son quantile d'ordre $p$ |
| $\mathcal N_n(\boldsymbol\mu,\Sigma)$ | Vecteur gaussien de $\mathbb R^n$ |
| $\chi^2(k)$ | Loi du khi-deux à $k$ degrés de liberté |
| $\xrightarrow{\mathcal L}$, $\perp\!\!\!\perp$ | Convergence en loi, indépendance |
| $\xrightarrow{P}$, $\xrightarrow{p.s.}$ | Convergence en probabilité, convergence presque sûre |

> ⚠️ **Divergence de convention avec `modele.md`.** Ce document-là normalise les moments par
> $n$ (moments de population). Le présent cours utilise, pour la variance d'échantillon,
> le diviseur $n-1$ :
> $$S^2=\frac{1}{n-1}\sum_i (X_i-\bar X)^2$$
> Ce n'est pas une incohérence mais un **changement de finalité** : le diviseur $n-1$ rend
> l'estimateur sans biais, ce qui n'a de sens que dans un cadre probabiliste. Le
> [module 16](16-theoreme-de-fisher-cochran.md) explique précisément d'où il vient.

## Références

| Usage | Référence |
|---|---|
| Cours général, français | G. Saporta, *Probabilités, analyse des données et statistique*, Technip |
| Théorie rigoureuse | Casella & Berger, *Statistical Inference* — ch. 1–2 (fondations), 5 (Fisher–Cochran) |
| Concis et moderne | Wasserman, *All of Statistics* — ch. 2–4 pour la partie 0, ch. 5 pour les convergences |
| Probabilités, référence | Billingsley, *Probability and Measure* — TCL, Lévy, Donsker |
| Gratuit et accessible | *OpenIntro Statistics* — openintro.org |
