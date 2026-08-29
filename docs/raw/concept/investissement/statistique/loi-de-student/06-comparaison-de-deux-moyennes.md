# Module 6 — Comparaison de deux moyennes

**Durée : 4 h.** Trois tests portent le nom de « test de Student » et sont régulièrement
confondus. Ce module les distingue et donne la règle de choix.

---

## 6.1 Le tableau d'orientation

| Situation | Test | Degrés de liberté |
|---|---|---|
| Mesures **appariées** (deux mesures sur le même individu) | $t$ apparié — c'est un test à **une** moyenne sur les différences | $n-1$ |
| Échantillons **indépendants**, variances supposées **égales** | $t$ à variance poolée | $n_1+n_2-2$ |
| Échantillons **indépendants**, variances **quelconques** | **Welch** | Satterthwaite (non entier) |

> 🔑 **La première question à se poser n'est pas « les variances sont-elles égales ? » mais
> « les données sont-elles appariées ? »** C'est la question qui change le plus le résultat,
> et de loin — le § 6.2 le montre chiffres à l'appui.

---

## 6.2 Le test apparié

### Principe

Si chaque unité $i$ fournit **deux** mesures $(A_i, B_i)$, on forme les différences
$D_i=B_i-A_i$ et l'on applique **exactement** le test du module 5 à cet unique échantillon :

$$t=\frac{\bar D-\delta_0}{S_D/\sqrt n}\;\sim\;\mathcal T(n-1) \quad\text{sous } H_0:\delta=\delta_0$$

Il n'y a **rien de nouveau à apprendre** : le test apparié est le test à une moyenne appliqué aux
différences.

### Pourquoi l'appariement est si puissant

Sur données appariées,
$$\operatorname{Var}(D)=\operatorname{Var}(A)+\operatorname{Var}(B)-2\operatorname{Cov}(A,B).$$

Si $A$ et $B$ sont fortement **corrélées positivement** — ce qui est le cas dès qu'un facteur
individuel commun agit sur les deux mesures — la covariance est grande et
$\operatorname{Var}(D)$ **s'effondre**. La variabilité inter-individus, qui est du bruit pour la
question posée, disparaît entièrement.

### Exemple travaillé — le contraste est spectaculaire

Dix titres, rendement (%) sous deux stratégies, mesuré sur les **mêmes** titres :

| Titre | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Stratégie A | 3,1 | −2,4 | 5,8 | 0,9 | −1,2 | 4,4 | 2,0 | −0,5 | 6,1 | 1,7 |
| Stratégie B | 3,7 | −1,5 | 6,2 | 2,0 | −0,5 | 4,7 | 3,0 | 0,3 | 6,6 | 2,6 |
| **$D=B-A$** | 0,6 | 0,9 | 0,4 | 1,1 | 0,7 | 0,3 | 1,0 | 0,8 | 0,5 | 0,9 |

Statistiques : $\bar A=1{,}99$ ($s_A=2{,}89$), $\bar B=2{,}71$ ($s_B=2{,}72$),
$\bar D=0{,}72$ ($s_D=0{,}27$), et $\operatorname{Corr}(A,B)=0{,}997$.

| Analyse | $t$ | ddl | $p$ | Conclusion |
|---|---|---|---|---|
| **Apparié** (correct) | **8,565** | 9 | **0,000013** | Différence hautement significative |
| Indépendant / Welch (incorrect ici) | 0,573 | ≈ 18 | 0,574 | Rien du tout |

**Le même jeu de données, deux conclusions opposées.** La différence moyenne est de $+0{,}72$
point avec un IC à 95 % de $[+0{,}53\;;\;+0{,}91]$ — extrêmement précis. Traité comme deux
échantillons indépendants, ce signal parfaitement net est **entièrement noyé** dans la
dispersion inter-titres ($s\approx 2{,}9$), qui n'a pourtant aucun rapport avec la question.

> ⚠️ **Ignorer un appariement existant est l'erreur la plus coûteuse de ce module** : elle
> détruit la puissance du test. L'erreur inverse — apparier des données qui ne le sont pas —
> est tout aussi grave mais plus rare, car elle suppose un lien de correspondance qui n'existe
> pas.

**Comment reconnaître un appariement ?** Posez-vous : *l'observation $i$ du groupe A et
l'observation $i$ du groupe B ont-elles un lien qui disparaîtrait si je permutais l'ordre d'un
des deux groupes ?* Si oui, c'est apparié. Cas typiques : avant/après sur le même sujet, deux
méthodes sur le même échantillon, deux gérants sur le même univers de titres, deux mois
consécutifs pour les mêmes magasins.

---

## 6.3 Deux échantillons indépendants

### Le test à variance poolée

Sous l'hypothèse $\sigma_1=\sigma_2=\sigma$, on estime cette variance commune en fusionnant
l'information des deux échantillons :

$$S_p^2=\frac{(n_1-1)S_1^2+(n_2-1)S_2^2}{n_1+n_2-2}$$

$$t=\frac{\bar X_1-\bar X_2}{S_p\sqrt{\frac{1}{n_1}+\frac{1}{n_2}}}\;\sim\;\mathcal T(n_1+n_2-2)$$

Le nombre de degrés de liberté est $n_1+n_2-2$ : deux moyennes ont été estimées, donc deux
degrés consommés — la règle de [Fisher–Cochran](../mathematique/16-theoreme-de-fisher-cochran.md).

### Le test de Welch

Sans supposer l'égalité des variances, on estime séparément :

$$t=\frac{\bar X_1-\bar X_2}{\sqrt{\dfrac{S_1^2}{n_1}+\dfrac{S_2^2}{n_2}}}$$

La loi n'est plus exactement une Student, mais l'**approximation de Welch–Satterthwaite** la
rapproche d'une $\mathcal T(\nu)$ avec

$$\nu=\frac{\left(\dfrac{S_1^2}{n_1}+\dfrac{S_2^2}{n_2}\right)^{\!2}}
{\dfrac{\left(S_1^2/n_1\right)^2}{n_1-1}+\dfrac{\left(S_2^2/n_2\right)^2}{n_2-1}}$$

⚠️ Ce $\nu$ est **fractionnaire**. Ce n'est pas une erreur de calcul : la densité du $\chi^2$
([cours de statistique](../mathematique/15-loi-du-chi2.md), § 15.6) est définie pour tout réel positif. On
l'utilise tel quel, sans arrondir.

---

## 6.4 Lequel choisir — la règle et sa justification

> **Règle : utiliser Welch par défaut.**

C'est le comportement par défaut de `t.test` en R et de `stats.ttest_ind(..., equal_var=False)`
en Python. Justification, chiffrée par simulation ($200\,000$ réplications, $H_0$ **vraie**,
niveau nominal 5 %) :

| $n_1$ | $n_2$ | $\sigma_1$ | $\sigma_2$ | Niveau réel — **poolé** | Niveau réel — **Welch** |
|---|---|---|---|---|---|
| 10 | 10 | 1 | 1 | 0,050 ✅ | 0,048 ✅ |
| 10 | 10 | 1 | 3 | 0,059 | 0,051 ✅ |
| 20 | 20 | 1 | 4 | 0,055 | 0,050 ✅ |
| 10 | 30 | 1 | 3 | **0,004** ❌ | 0,050 ✅ |
| 30 | 10 | 1 | 3 | **0,211** ❌ | 0,051 ✅ |
| 10 | 30 | 3 | 1 | **0,211** ❌ | 0,051 ✅ |

**Lecture, en trois points :**

1. **À effectifs égaux, l'inégalité des variances est bénigne** — 5,9 % au lieu de 5 %. Les deux
   tests donnent d'ailleurs alors *la même statistique* $t$ ; seuls les degrés de liberté
   diffèrent.
2. **À effectifs inégaux, le test poolé est catastrophique**, et dans les deux sens :
   - si le **grand** échantillon a la **petite** variance → niveau réel **21 %**, soit quatre
     fois le risque annoncé (test beaucoup trop permissif) ;
   - si le **grand** échantillon a la **grande** variance → niveau réel **0,4 %**, soit un test
     tellement conservateur qu'il ne détecte plus rien.
3. **Welch tient 5 % dans tous les cas**, et son coût quand les variances sont réellement égales
   est négligeable (quelques degrés de liberté perdus, soit une perte de puissance de l'ordre du
   pourcent).

### ⚠️ Ne pas pré-tester l'égalité des variances

Une procédure encore enseignée consiste à tester d'abord $H_0:\sigma_1=\sigma_2$ (test de
Fisher, de Levene, de Bartlett), puis à choisir le test de moyennes en fonction du résultat.

**C'est une mauvaise pratique**, pour trois raisons :

- Le test final n'a plus le niveau annoncé : le conditionnement à un premier test aléatoire
  déforme la loi de la statistique. C'est un problème d'**inférence conditionnelle**, pas un
  détail.
- Le pré-test a lui-même une puissance faible sur petit échantillon — précisément là où le choix
  compte. Il conclut donc « variances égales » par manque de données, au moment où c'est le plus
  dangereux.
- Le test de Fisher d'égalité des variances est **très sensible à la non-normalité**, beaucoup
  plus que le test de moyennes qu'il est censé protéger.

Utiliser Welch d'emblée dispense de tout cela.

---

## 6.5 Exemple travaillé — deux stratégies, échantillons indépendants

Deux stratégies évaluées sur des **périodes différentes** (donc pas d'appariement possible) :

| | $n$ | moyenne | écart-type |
|---|---|---|---|
| Stratégie A | 15 | +1,20 % | 2,00 % |
| Stratégie B | 15 | +0,40 % | 4,50 % |

**Welch :**
$$\text{SE}=\sqrt{\frac{2{,}00^2}{15}+\frac{4{,}50^2}{15}}=1{,}2715
\qquad t=\frac{1{,}20-0{,}40}{1{,}2715}=0{,}629$$
$$\nu=\frac{(0{,}2667+1{,}3500)^2}{\frac{0{,}2667^2}{14}+\frac{1{,}3500^2}{14}}=19{,}32
\qquad p=0{,}537$$

$$\text{IC}_{95\%}(\mu_A-\mu_B)=0{,}80\pm 2{,}091\times 1{,}2715=[-1{,}86\;;\;+3{,}46]$$

**Conclusion.** On ne rejette pas $H_0$. Mais l'IC va de $-1{,}9$ à $+3{,}5$ points : les données
sont compatibles avec une nette supériorité de A **comme** avec une nette supériorité de B. Le
test ne dit pas que les stratégies se valent ; il dit que 15 observations chacune ne permettent
pas d'en juger.

**Remarque instructive.** Les effectifs étant égaux, le test poolé donne ici la **même**
statistique ($t=0{,}629$) et une $p$-valeur presque identique ($0{,}534$ avec 28 ddl contre
$0{,}537$ avec 19,3 ddl). C'est l'illustration du point 1 du § 6.4 : **c'est le déséquilibre des
effectifs, et non l'inégalité des variances en soi, qui rend le test poolé dangereux.**

---

## 6.6 Simulations

### S6.1 — Reproduire le tableau des niveaux réels

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(6)
N = 200_000

def niveaux(n1, n2, s1, s2):
    X = rng.normal(0, s1, size=(N, n1))     # H0 est VRAIE : mêmes espérances
    Y = rng.normal(0, s2, size=(N, n2))
    _, p_pool = stats.ttest_ind(X, Y, axis=1, equal_var=True)
    _, p_welch = stats.ttest_ind(X, Y, axis=1, equal_var=False)
    return np.mean(p_pool < .05), np.mean(p_welch < .05)

print(f"{'n1':>3} {'n2':>3} {'s1':>3} {'s2':>3} | {'poolé':>7} {'Welch':>7}")
for c in [(10,10,1,1), (10,10,1,3), (20,20,1,4),
          (10,30,1,3), (30,10,1,3), (10,30,3,1)]:
    a, b = niveaux(*c)
    print(f"{c[0]:3d} {c[1]:3d} {c[2]:3d} {c[3]:3d} | {a:7.4f} {b:7.4f}")
```

### S6.2 — Le gain de puissance de l'appariement

```python
def comparer(n, rho, delta, N=100_000):
    """n paires, corrélation rho entre A et B, vrai écart delta."""
    Z = rng.multivariate_normal([0, delta], [[1, rho], [rho, 1]], size=(N, n))
    A, B = Z[:, :, 0], Z[:, :, 1]
    _, p_pair = stats.ttest_rel(B, A, axis=1)
    _, p_ind = stats.ttest_ind(B, A, axis=1, equal_var=False)
    return np.mean(p_pair < .05), np.mean(p_ind < .05)

print(f"{'rho':>5} | {'apparié':>8} {'indép.':>8}")
for rho in (0.0, 0.3, 0.6, 0.9, 0.99):
    a, b = comparer(n=10, rho=rho, delta=0.5)
    print(f"{rho:5.2f} | {a:8.3f} {b:8.3f}")
```

**Ce que vous devez observer.** La puissance du test indépendant **ne dépend pas** de $\rho$ —
il ignore l'appariement, par construction. Celle du test apparié **croît fortement** avec $\rho$
et devient écrasante au-delà de 0,9. À $\rho=0$, l'appariement fait légèrement perdre (un degré
de liberté sacrifié pour rien) : c'est le seul cas où il coûte quelque chose.

### S6.3 — Contrôler que Welch reste valide sous non-normalité

```python
for loi, tirage in [("normale", lambda s: rng.normal(0, 1, s)),
                    ("exponentielle centrée", lambda s: rng.exponential(1, s) - 1),
                    ("Student(3)", lambda s: stats.t.rvs(3, size=s, random_state=7))]:
    for n in (5, 15, 50):
        X, Y = tirage((50_000, n)), tirage((50_000, n))
        _, p = stats.ttest_ind(X, Y, axis=1, equal_var=False)
        print(f"{loi:22s} n={n:3d} → niveau réel {np.mean(p < .05):.4f}")
```

L'écart au niveau nominal se résorbe quand $n$ croît : c'est le TCL à l'œuvre. **La normalité
est bien l'hypothèse la moins critique** — conclusion développée au module 8.

---

## 6.7 Exercices

**E6.1.** Vérifier à la main que, pour $n_1=n_2=n$, la statistique poolée et la statistique de
Welch sont **égales**. En déduire que seule la $p$-valeur diffère, par les degrés de liberté.

**E6.2.** Refaire l'exemple du § 6.2 intégralement à la main, puis vérifier avec
`stats.ttest_rel`. Calculer aussi la corrélation entre A et B et commenter son rôle.

**E6.3.** Calculer les degrés de liberté de Welch pour $n_1=8$, $s_1=1$, $n_2=25$, $s_2=6$.
Comparer à $n_1+n_2-2=31$. Que traduit l'écart ?

**E6.4.** Montrer que $\nu_{\text{Welch}}$ est toujours compris entre
$\min(n_1,n_2)-1$ et $n_1+n_2-2$. Dans quel cas atteint-il chacune de ces bornes ?

**E6.5.** Un jeu de données de 12 magasins donne le chiffre d'affaires **avant** et **après** une
opération commerciale. Un collègue propose de comparer « la moyenne d'avant à la moyenne
d'après » par un test à deux échantillons indépendants. Expliquer en trois phrases pourquoi c'est
une erreur, et ce qu'elle coûte.

**E6.6 — orientée finance.** Comparer les rendements mensuels de deux titres du SBF 250 sur la
**même** période. Le test doit-il être apparié ou indépendant ? *(Réponse : apparié — les deux
titres subissent le même facteur de marché sur les mêmes mois, et c'est précisément ce facteur
commun qu'on veut éliminer.)* Faire les deux et comparer les $p$-valeurs.

---

## 6.8 À retenir

- **Apparié ou indépendant ?** C'est la première question, et celle qui change le plus le
  résultat. Ignorer un appariement réel détruit la puissance.
- **Welch par défaut** pour deux échantillons indépendants. Le test poolé n'est dangereux
  qu'à effectifs déséquilibrés — mais il l'est alors gravement (niveau réel de 0,4 % à 21 %
  pour 5 % annoncés).
- **Ne jamais pré-tester l'égalité des variances** pour choisir le test.
- Les degrés de liberté de Welch sont **fractionnaires** : c'est normal.
- Comme au module 5 : publier l'**intervalle de confiance de la différence**, pas seulement la
  $p$-valeur.

---

⬅️ [Module 5 — Inférence sur une moyenne](05-inference-sur-une-moyenne.md) ·
➡️ [Module 7 — Student en régression](07-student-en-regression.md) ·
🏠 [Sommaire](README.md)
