# Module 8 — Robustesse, limites, alternatives ⭐

**Durée : 3 h.** C'est le module qui distingue l'utilisateur averti de l'utilisateur mécanique.
Tout ce qui précède suppose un modèle ; ce module examine ce qui se passe quand le modèle est
faux.

---

## 8.1 La hiérarchie — et pourquoi elle est l'inverse de celle qu'on enseigne

On présente habituellement la **normalité** comme *la* condition du test de Student. C'est
l'hypothèse la plus citée, et de loin la moins importante.

Voici le classement réel, par nocivité décroissante :

| Rang | Hypothèse | Nocivité | Réparable ? |
|---|---|---|---|
| 1 | **Indépendance** des observations | **Critique** — aucune taille d'échantillon n'y remédie | Oui, en modélisant |
| 2 | **Saisonnalité** / structure non modélisée | Critique en pratique | Oui |
| 3 | Absence de **valeurs aberrantes** | Forte sur petit échantillon | Oui, diagnostics et méthodes robustes |
| 4 | **Homoscédasticité** | Modérée | Oui, écarts-types robustes |
| 5 | **Normalité** | Faible dès $n\gtrsim 20$–30 | Oui, et souvent inutile |

> 🔑 **La raison de ce renversement.** La normalité est protégée par le **théorème central
> limite** : quand $n$ croît, $\bar X$ devient gaussienne quelle que soit la loi de départ, et le
> test redevient valide. **Rien de tel ne protège l'indépendance** : au contraire, plus $n$ croît,
> plus l'erreur s'aggrave. Une hypothèse dont la violation empire avec les données est bien plus
> dangereuse qu'une hypothèse dont la violation s'efface.
>
> ➡️ Ce classement n'est pas empirique : il se **démontre**. Le
> [module 14 du cours de statistique](../mathematique/14-dependance-et-echec-du-tcl.md) établit les deux régimes de dépendance et
> montre pourquoi le TCL répare la non-normalité mais ne peut rien contre une racine unitaire.

---

## 8.2 L'indépendance — le vrai danger

### Ce qui se passe sur une moyenne

Le module 0 (§ 0.4, Q1) l'a déjà établi :
$$\operatorname{Var}(\bar X)=\frac{\sigma^2}{n}
+\frac{2}{n^2}\sum_{i<j}\operatorname{Cov}(X_i,X_j)$$

Sur des données **positivement corrélées** — le cas de toute série chronologique — le second
terme est **positif**. La formule usuelle $\sigma^2/n$ **sous-estime** la vraie variance, donc
$\operatorname{SE}$ est trop petit, donc $t$ est trop grand, donc on rejette trop souvent.

Pour un processus AR(1) de paramètre $\varphi$, le facteur de gonflement de la variance vaut
approximativement
$$\frac{1+\varphi}{1-\varphi}$$
soit $\times 3$ pour $\varphi=0{,}5$ et $\times 9$ pour $\varphi=0{,}8$. On peut le lire comme
une **taille d'échantillon effective** : 100 observations d'un AR(1) à $\varphi=0{,}8$ portent
autant d'information qu'environ **11** observations indépendantes.

### Ce qui se passe sur un test de tendance

C'est le cas qui concerne directement le module 7. Simulation du test de tendance sous $H_0$
**vraie** (aucune tendance), niveau nominal **5 %**, 50 000 réplications :

| Processus | $n=12$ | $n=24$ | $n=48$ | $n=120$ | $n=250$ |
|---|---|---|---|---|---|
| **Bruit i.i.d.** (modèle supposé) | 4,9 % ✅ | 5,1 % ✅ | 5,0 % ✅ | 4,9 % ✅ | 5,0 % ✅ |
| AR(1), $\varphi=0{,}3$ | 12,8 % | 14,0 % | 14,3 % | 15,0 % | 14,7 % |
| AR(1), $\varphi=0{,}5$ | 22,1 % | 24,8 % | 25,5 % | 25,9 % | 25,8 % |
| AR(1), $\varphi=0{,}8$ | 43,0 % | 50,1 % | 52,2 % | 51,8 % | 51,6 % |
| AR(1), $\varphi=0{,}95$ | 55,2 % | 67,4 % | 73,1 % | 76,1 % | 76,2 % |
| **Marche aléatoire** | **59,7 %** | **73,1 %** | **82,1 %** | **89,1 %** | **92,3 %** |

**Trois lectures :**

1. **Une autocorrélation même modeste suffit.** À $\varphi=0{,}3$ — valeur qu'on qualifierait de
   « faible » — le risque réel est déjà **triple** du risque annoncé.
2. **Pour un AR(1) stationnaire, l'erreur se stabilise.** Elle est grave mais bornée : le test
   est mal calibré, pas divergent.
3. **Pour une marche aléatoire, l'erreur EMPIRE avec $n$.** C'est le point décisif. À 250
   observations, le test conclut « série tendancielle » dans **92 % des cas** sur des données
   **sans aucune tendance**.

### Pourquoi la marche aléatoire est un cas à part

Une marche aléatoire $V_i=V_{i-1}+\eta_i$ n'est **pas** stationnaire : ses chocs
s'**accumulent** au lieu de se dissiper. Sur un tel processus :

- $\rho^2$ ne tend pas vers 0 quand $n\to\infty$ — il converge vers une **variable aléatoire
  non dégénérée** ;
- la statistique $t$ **diverge en $\sqrt n$** au lieu de converger vers une loi fixe ;
- la loi asymptotique n'est pas une Student mais une fonctionnelle de mouvement brownien.

C'est la **régression fallacieuse** (*spurious regression*), mise en évidence par
**Granger et Newbold (1974)** puis formalisée par **Phillips (1986)**. Elle a valu à Granger le
prix Nobel d'économie 2003, conjointement avec Engle.

> ⚠️ **Un cours de bourse est très proche d'une marche aléatoire.** L'exercice E7.6 du module 7
> était un piège délibéré : la majorité des fenêtres y ressortent « significatives ». Ce n'est pas
> que les marchés soient tendanciels — c'est que le test est inapplicable tel quel.

### Que faire

| Situation | Remède |
|---|---|
| Autocorrélation faible à modérée, série stationnaire | Écarts-types **HAC** (Newey–West) — $\hat r$ inchangé, seul $\operatorname{SE}$ est corrigé |
| Structure connue | Modéliser explicitement : régression avec erreurs AR(1) (Cochrane–Orcutt, Prais–Winsten) |
| Suspicion de racine unitaire | **Trancher d'abord** : tests **ADF** (H₀ = racine unitaire) et **KPSS** (H₀ = stationnarité) — ils sont complémentaires, pas redondants |
| Racine unitaire confirmée | Travailler **en différences** ($\Delta V_i$), ou en cointégration si plusieurs séries |
| Diagnostic minimal | **Durbin–Watson** ou **Ljung–Box** sur les résidus |

> 🔑 **La question « tendance déterministe ou marche aléatoire ? » est PRÉALABLE au test de
> pente, pas postérieure.** Appliquer un test de tendance sans avoir tranché ce point, c'est
> supposer la réponse à la question qu'on prétend poser.

---

## 8.3 La saisonnalité

C'est de l'autocorrélation déguisée, et c'est le piège pratique n° 1 sur données mensuelles ou
trimestrielles.

**Deux effets distincts :**

1. **Gonflement du risque**, par la corrélation induite entre observations distantes de 12 mois.
2. **Pente purement artefactuelle** si la fenêtre ne couvre pas un **nombre entier de cycles**.
   Une série mensuelle observée de mars à décembre (10 mois) sur un commerce saisonnier produira
   une « tendance » qui n'est que la montée vers les fêtes.

**Remèdes** : désaisonnaliser au préalable, inclure des indicatrices mensuelles dans la
régression, comparer d'une année sur l'autre à mois identique, ou utiliser un test de tendance
**saisonnier** (Mann–Kendall saisonnier).

⚠️ Toujours cadrer la fenêtre sur un nombre entier de cycles quand c'est possible. C'est gratuit
et cela supprime l'effet 2.

---

## 8.4 Valeurs aberrantes et petits échantillons

$\bar X$, $S$ et $\rho$ sont tous des statistiques **non robustes** : une seule observation
extrême les déplace arbitrairement.

Le module 7, § 7.8/f l'a montré sur un cas réel : avec $n=11$, **le retrait d'un seul point
renversait la conclusion** ($p$ de 0,014 à 0,072) — et le diagnostic de Cook l'avait annoncé.

**Marche à suivre :**

1. **Toujours tracer les données.** Le quatuor d'Anscombe (1973) — quatre jeux de données aux
   statistiques descriptives *identiques* mais aux formes radicalement différentes — reste la
   démonstration la plus efficace de cette règle.
2. Calculer **levier** $h_{ii}$ et **distance de Cook** $D_i$ (module 7, § 7.7).
3. **Ne jamais supprimer un point au seul motif qu'il gêne.** Une valeur extrême est soit une
   erreur de mesure (à corriger ou écarter, avec justification écrite), soit une observation
   authentique — auquel cas c'est souvent **la plus informative du jeu**.
4. En cas de doute, **publier les deux analyses**, avec et sans le point. La transparence vaut
   mieux qu'un arbitrage caché.

---

## 8.5 Homoscédasticité

Une variance résiduelle non constante ne biaise **pas** les estimateurs $\hat r$ et $\hat v_0$ —
ils restent sans biais. Elle fausse en revanche leurs **erreurs types**, donc les tests et les
intervalles.

**Signaux** : résidus en entonnoir sur le graphique $\hat e$ vs $\hat V$ ; en finance, périodes
calmes alternant avec des périodes agitées (*volatility clustering*).

**Remèdes** : écarts-types robustes à l'hétéroscédasticité (**White**, dits HC0–HC3 ; préférer
HC3 sur petit échantillon), transformation stabilisatrice (log), ou modélisation explicite de la
variance (GARCH en finance).

---

## 8.6 Normalité — l'hypothèse surestimée

**Ce que protège le TCL.** Dès que $n$ dépasse quelques dizaines, le test de Student conserve
approximativement son niveau, quelle que soit la loi des données — à condition que la variance
soit **finie**.

**Ce que le TCL ne protège pas :**

- **$n$ petit ET loi très asymétrique.** Un test à $n=8$ sur des données log-normales peut
  afficher un niveau réel de 8 à 10 %.
- **Variance infinie.** Sur une loi à queue très lourde ($\mathcal T(\nu)$ avec $\nu\le 2$,
  certaines distributions de sinistres), le TCL ne s'applique pas du tout.
- **La puissance.** Le niveau est préservé, mais le test peut devenir très inefficace : sur des
  données à queues lourdes, un test de rang détecte un effet que Student manque.

⚠️ **Ne pas pré-tester la normalité** (Shapiro–Wilk, Kolmogorov–Smirnov) pour décider du test à
appliquer, pour les mêmes raisons qu'au module 6 § 6.4 — le test final perd son niveau nominal.
De plus, ces tests sont **inutiles quand $n$ est petit** (aucune puissance) et **trop sensibles
quand $n$ est grand** (ils rejettent des écarts sans conséquence pratique). Préférez un examen
graphique (droite de Henry / QQ-plot) et un jugement sur l'ordre de grandeur de l'écart.

---

## 8.7 Alternatives

| Méthode | Quand l'employer | Prix à payer |
|---|---|---|
| **Wilcoxon signé** (une population, apparié) | Non-normalité, petits effectifs | Teste la médiane, pas la moyenne ; ~5 % de puissance en moins sous normalité |
| **Mann–Whitney** (deux populations) | Idem, échantillons indépendants | Hypothèse implicite de même forme de distribution |
| **Mann–Kendall** + **pente de Sen** | Tendance, données non normales ou avec aberrants | Suppose toujours l'**indépendance** — sauf variante **Hamed–Rao** |
| **Bootstrap** | Loi inconnue, statistique complexe | Suppose l'indépendance ; existe en version *block bootstrap* pour séries |
| **Test de permutation** | Petits effectifs, niveau exact souhaité | Nécessite l'échangeabilité sous $H_0$ |
| **Régression robuste** (Huber, LTS) | Aberrants dans une régression | Inférence plus délicate |

> ⚠️ **Aucune de ces méthodes ne règle le problème n° 1.** Wilcoxon, Mann–Kendall et le bootstrap
> classique supposent tous l'indépendance. Elles remplacent la normalité, pas l'indépendance.
> Pour des données corrélées, il faut des outils spécifiques : HAC, block bootstrap,
> Hamed–Rao.

---

## 8.8 Tests multiples

Si l'on teste $m$ hypothèses au risque de 5 %, la probabilité d'au moins un faux positif est
$1-0{,}95^m$ :

| $m$ | 1 | 5 | 10 | 20 | 100 |
|---|---|---|---|---|---|
| $P(\ge 1$ faux positif$)$ | 5 % | 23 % | 40 % | **64 %** | **99,4 %** |

Vingt tests sur du bruit pur produisent presque à coup sûr un « résultat significatif ».

**Corrections** : **Bonferroni** ($\alpha/m$ — simple, très conservateur),
**Holm–Bonferroni** (uniformément meilleur, aucune raison de lui préférer Bonferroni),
**Benjamini–Hochberg** (contrôle le taux de fausses découvertes, adapté aux grands $m$).

⚠️ Le problème se pose aussi de façon **implicite** : essayer plusieurs fenêtres, plusieurs
transformations, plusieurs sous-périodes, et ne rapporter que le résultat significatif, c'est
faire du test multiple sans le déclarer. C'est le *p-hacking*. Le remède est de **fixer le
protocole avant de voir les données**.

---

## 8.9 Simulations

### S8.1 — Reproduire le tableau du § 8.2

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(8)
N = 50_000

def taux_de_rejet(n, generateur):
    """Proportion de rejets du test de tendance, sous H0 vraie."""
    V = generateur(n, N)
    T = np.arange(1, n + 1); Tc = T - T.mean(); Stt = (Tc ** 2).sum()
    r = (V * Tc).sum(axis=1) / Stt
    e = V - (V.mean(axis=1, keepdims=True) + r[:, None] * Tc)
    s2 = (e ** 2).sum(axis=1) / (n - 2)
    t = r / np.sqrt(s2 / Stt)
    return np.mean(np.abs(t) > stats.t.ppf(0.975, n - 2))

def iid(n, N): return rng.standard_normal((N, n))
def marche(n, N): return np.cumsum(rng.standard_normal((N, n)), axis=1)
def ar1(phi):
    def g(n, N):
        e = rng.normal(0, np.sqrt(1 - phi ** 2), (N, n))
        x = np.empty((N, n)); x[:, 0] = rng.standard_normal(N)
        for i in range(1, n):
            x[:, i] = phi * x[:, i - 1] + e[:, i]
        return x
    return g

ns = [12, 24, 48, 120, 250]
print(f"{'processus':<20}" + "".join(f"{n:>9}" for n in ns))
for nom, g in [("bruit i.i.d.", iid), ("AR(1) phi=0,3", ar1(.3)),
               ("AR(1) phi=0,5", ar1(.5)), ("AR(1) phi=0,8", ar1(.8)),
               ("AR(1) phi=0,95", ar1(.95)), ("marche aléatoire", marche)]:
    print(f"{nom:<20}" + "".join(f"{100*taux_de_rejet(n, g):8.1f}%" for n in ns))
```

### S8.2 — Voir une régression fallacieuse

```python
n = 200
V = np.cumsum(rng.standard_normal(n))          # marche aléatoire pure
lr = stats.linregress(np.arange(n), V)
print(f"pente={lr.slope:+.4f}  R²={lr.rvalue**2:.3f}  p={lr.pvalue:.2e}")
```

Relancez plusieurs fois. Vous obtiendrez régulièrement des $R^2$ de 0,5 à 0,9 et des $p$-valeurs
de l'ordre de $10^{-30}$ — sur des données **sans aucune tendance**. C'est l'expérience la plus
troublante du cours, et elle doit l'être.

### S8.3 — La correction HAC

```python
import statsmodels.api as sm

V = ar1(0.7)(60, 1)[0]
X = sm.add_constant(np.arange(60, dtype=float))
ols = sm.OLS(V, X).fit()
hac = sm.OLS(V, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
print(f"MCO  : pente={ols.params[1]:+.4f}  SE={ols.bse[1]:.4f}  p={ols.pvalues[1]:.4f}")
print(f"HAC  : pente={hac.params[1]:+.4f}  SE={hac.bse[1]:.4f}  p={hac.pvalues[1]:.4f}")
```

La pente est **identique** ; seule l'erreur type change — et avec elle la conclusion. C'est
exactement ce qu'annonçait le § 8.2.

### S8.4 — Racine unitaire : ADF et KPSS

```python
from statsmodels.tsa.stattools import adfuller, kpss

for nom, serie in [("stationnaire (AR 0,5)", ar1(0.5)(200, 1)[0]),
                   ("marche aléatoire", np.cumsum(rng.standard_normal(200)))]:
    p_adf = adfuller(serie, regression="ct")[1]
    p_kpss = kpss(serie, regression="ct", nlags="auto")[1]
    print(f"{nom:24s} ADF p={p_adf:.3f}   KPSS p={p_kpss:.3f}")
```

**Comment les lire ensemble** — les deux tests ont des hypothèses nulles **opposées** :

| ADF (H₀ : racine unitaire) | KPSS (H₀ : stationnarité) | Conclusion |
|---|---|---|
| rejette | ne rejette pas | **Stationnaire** — le test de tendance est applicable |
| ne rejette pas | rejette | **Racine unitaire** — travailler en différences |
| ne rejette pas | ne rejette pas | Données non concluantes (souvent : $n$ trop petit) |
| rejette | rejette | Structure plus complexe (rupture, tendance non linéaire) |

---

## 8.10 Exercices

**E8.1.** Démontrer la formule du facteur de gonflement $\frac{1+\varphi}{1-\varphi}$ pour la
variance de la moyenne d'un AR(1) (asymptotiquement). Vérifier par simulation à $\varphi=0{,}6$.

**E8.2.** Reproduire le tableau du § 8.2 et y ajouter une ligne AR(1) à $\varphi=-0{,}5$.
Le risque est-il gonflé ou **réduit** ? Expliquer. *(Réponse : réduit — une autocorrélation
négative rend le test conservateur. C'est le cas le moins dangereux, et le plus rare.)*

**E8.3.** Sur la série de 11 points du module 7, calculer Durbin–Watson et Ljung–Box (5 retards).
Les diagnostics valident-ils le test qui y a été mené ?

**E8.4.** Simuler une série mensuelle avec **saisonnalité pure** et sans tendance, observée sur
10 mois (mars→décembre). Quelle proportion de fenêtres ressort « significative » ? Recommencer
sur 12 et 24 mois. Conclure sur l'importance du cadrage.

**E8.5 — orientée finance, le cœur du module.** Reprendre E7.6 (test de tendance sur un cours de
bourse). Puis :
1. appliquer ADF et KPSS au cours ;
2. refaire le test sur les **rendements** (différences des log-prix) au lieu des prix ;
3. comparer les $p$-valeurs obtenues avec et sans correction HAC.

**Ce que vous devez constater** : sur les **prix**, presque tout est « significatif » — artefact
de la marche aléatoire. Sur les **rendements**, presque plus rien ne l'est. C'est la
démonstration pratique la plus importante du cours.

---

## 8.11 À retenir

- **L'indépendance est l'hypothèse critique**, et la seule dont la violation **empire** quand $n$
  augmente. La normalité est la moins importante, protégée par le TCL.
- Une autocorrélation de 0,3 triple déjà le risque réel ; une marche aléatoire le porte à **73 %
  à $n=24$** et **92 % à $n=250$** pour 5 % annoncés.
- **Trancher « stationnaire ou racine unitaire » AVANT** de tester une tendance (ADF + KPSS).
- **Toujours tracer les données** et examiner les résidus. Levier et Cook sur petit échantillon.
- **Ne pas pré-tester** normalité ni égalité des variances pour choisir son test.
- Vingt tests à 5 % produisent presque à coup sûr un faux positif : fixer le protocole d'avance.

---

⬅️ [Module 7 — Student en régression](07-student-en-regression.md) ·
➡️ [Module 9 — Synthèse](09-synthese.md) ·
🏠 [Sommaire](README.md)
