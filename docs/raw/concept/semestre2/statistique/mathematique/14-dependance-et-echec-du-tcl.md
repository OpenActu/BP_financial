# Module 14 — Dépendance et échec du TCL ⭐

**Durée : 1 h 15.** Prérequis : modules [12](12-theoreme-central-limite.md) et
[13](13-portee-et-limites-du-tcl.md).

> **La question traitée.** Que devient l'approximation normale si les $X_i$ ne sont **pas
> indépendants** ?

**Ce qui est en jeu.** L'indépendance n'intervient qu'une fois dans la démonstration du TCL
([étape 1, § 12.3](12-theoreme-central-limite.md)) — mais elle la porte tout entière. Ce module
montre que sa violation produit **deux régimes sans rapport**, et que dans le second, augmenter
$n$ **aggrave** le problème au lieu de le réparer. C'est le renversement le plus important de
tout le cours.

---

## 14.1 Régime 1 — dépendance faible : le TCL survit, mais la variance change

Pour un processus **stationnaire** dont la dépendance s'atténue assez vite (mélange,
$m$-dépendance, AR/ARMA stationnaires), il existe encore un TCL — mais la variance asymptotique
n'est plus $\sigma^2$ :

$$\sqrt n\,(\bar X_n-\mu)\;\xrightarrow{\mathcal L}\;\mathcal N(0,\sigma^2_{LR}),
\qquad
\sigma^2_{LR}=\sigma^2+2\sum_{k=1}^{\infty}\operatorname{Cov}(X_1,X_{1+k})$$

$\sigma^2_{LR}$ s'appelle la **variance de long terme**. Pour un AR(1) de paramètre $\varphi$ :

$$\sigma^2_{LR}=\sigma^2\,\frac{1+\varphi}{1-\varphi}$$

> ⚠️ **La forme du théorème est préservée, la constante ne l'est pas.** Utiliser $\sigma^2/n$ au
> lieu de $\sigma^2_{LR}/n$ ne produit pas une erreur qui s'estompe : elle **persiste à l'infini**.

Simulation — couverture réelle de l'intervalle nominal à 95 % calculé naïvement avec $\sigma/\sqrt n$
sur un AR(1) de variance marginale 1 :

| $\varphi$ | $n=25$ | $n=100$ | $n=400$ | $n=1600$ | $\frac{1+\varphi}{1-\varphi}$ | Couverture **corrigée** ($\sigma_{LR}$), $n=400$ |
|---|---|---|---|---|---|---|
| 0,00 | 0,9486 | 0,9513 | 0,9509 | 0,9506 | 1,00 | 0,9500 ✅ |
| 0,30 | 0,8532 | 0,8527 | 0,8500 | 0,8541 | 1,86 | 0,9488 ✅ |
| 0,50 | 0,7572 | 0,7498 | 0,7456 | 0,7408 | 3,00 | 0,9512 ✅ |
| 0,80 | 0,5264 | 0,4988 | 0,4875 | 0,4829 | 9,00 | 0,9509 ✅ |
| 0,95 | 0,3668 | 0,2762 | 0,2528 | 0,2455 | 39,00 | 0,9525 ✅ |

**Lecture.** L'erreur **se stabilise** — elle est grave mais **bornée** —, et surtout elle **se
corrige entièrement** dès qu'on utilise la bonne variance. C'est exactement ce que font les
écarts-types **HAC (Newey–West)** : ils estiment $\sigma^2_{LR}$ à partir des autocovariances
empiriques.

**Taille d'échantillon effective.** On peut lire le même phénomène ainsi :
$$n_{\text{eff}}=\frac{n}{\sigma^2_{LR}/\sigma^2}=n\,\frac{1-\varphi}{1+\varphi}$$
À $\varphi=0{,}8$, **100 observations n'en valent que 11**. Le reste est de la redondance.

---

## 14.2 Régime 2 — dépendance forte : il n'y a plus de TCL du tout

Pour une **marche aléatoire** $V_i=V_{i-1}+\eta_i$, la somme $\sum_k \operatorname{Cov}$ **diverge** :
il n'existe aucune variance de long terme finie, donc aucun TCL au sens du § 14.1.

Simulation — couverture du même intervalle naïf :

| $n$ | 25 | 100 | 400 | 1600 |
|---|---|---|---|---|
| Couverture réelle | 0,1061 | 0,0276 | 0,0060 | 0,0016 |

**La couverture tend vers 0.** Elle ne se stabilise pas à un mauvais niveau : elle **s'effondre**,
et d'autant plus vite que $n$ est grand.

**Ce qui remplace le TCL ici.** Le bon cadre est le **principe d'invariance de Donsker** : la
trajectoire renormalisée $\frac{1}{\sqrt n}V_{\lfloor nt\rfloor}$ converge, non pas vers un nombre
gaussien, mais vers un **mouvement brownien** — un processus aléatoire entier. Les statistiques
construites dessus ont alors pour limite des **fonctionnelles de brownien**, non tabulées par la
table normale. C'est de là que viennent les lois non standard des tests de racine unitaire
(Dickey–Fuller).

---

## 14.3 Le renversement ⭐

> 🔑 **Face à la non-normalité, augmenter $n$ répare (TCL). Face à une dépendance forte,
> augmenter $n$ aggrave.**

| | Non-normalité | Dépendance faible | Dépendance forte |
|---|---|---|---|
| Effet de $n\nearrow$ | **Répare** | Neutre (erreur stable) | **Aggrave** |
| Correction possible | Inutile | Oui — HAC / $\sigma_{LR}$ | Non — changer de modèle |
| Couverture à $n$ grand | $\to 0{,}95$ | Plafonne sous 0,95 | $\to 0$ |

Une hypothèse dont la violation **empire avec les données** est incomparablement plus dangereuse
qu'une hypothèse dont la violation **s'efface**. C'est pourquoi tout classement sérieux des
hypothèses d'un test place l'**indépendance en tête** et la **normalité en queue** — voir le
[module 8 du cours sur Student](../../../semestre3/statistique/loi-de-student/08-robustesse-et-limites.md).

⚠️ **En finance, la distinction est concrète et coûteuse** : les **rendements** sont
faiblement dépendants (régime 1, corrigeable) ; les **prix** sont une marche aléatoire
(régime 2, rien ne tient). Travailler sur la mauvaise série ne produit pas une erreur de
quelques pourcents, mais un résultat entièrement dépourvu de sens.

---

## 14.4 Simulation

### S14.1 — Reproduire les deux tableaux

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(11)
z = stats.norm.ppf(0.975)

def ar1(n, N, phi):
    e = rng.normal(0, np.sqrt(1 - phi**2), (N, n))
    x = np.empty((N, n)); x[:, 0] = rng.standard_normal(N)
    for i in range(1, n):
        x[:, i] = phi * x[:, i-1] + e[:, i]
    return x

N = 40_000
print(f"{'phi':>6}" + "".join(f"{f'n={n}':>9}" for n in (25, 100, 400, 1600))
      + f"{'sigma2_LR':>11}{'corrigee':>10}")
for phi in (0.0, 0.3, 0.5, 0.8, 0.95):
    brut = [np.mean(np.abs(ar1(n, N, phi).mean(axis=1)) <= z / np.sqrt(n))
            for n in (25, 100, 400, 1600)]
    lr = (1 + phi) / (1 - phi)
    corr = np.mean(np.abs(ar1(400, N, phi).mean(axis=1)) <= z * np.sqrt(lr / 400))
    print(f"{phi:>6.2f}" + "".join(f"{b:>9.4f}" for b in brut) + f"{lr:>11.2f}{corr:>10.4f}")

print("\nmarche aléatoire (même intervalle naïf) :")
for n in (25, 100, 400, 1600):
    m = np.cumsum(rng.standard_normal((20_000, n)), axis=1).mean(axis=1)
    print(f"  n={n:>5} -> {np.mean(np.abs(m) <= z / np.sqrt(n)):.4f}")
```

**La comparaison des deux blocs est le cœur du module** : l'AR(1) se stabilise et se corrige, la
marche aléatoire s'effondre. Lisez la colonne `corrigee` : elle revient à 0,95 dans tous les cas
du régime 1, y compris à $\varphi=0{,}95$.

---

## 14.5 Exercices

**E14.1.** Démontrer $\sigma^2_{LR}=\sigma^2\frac{1+\varphi}{1-\varphi}$ pour un AR(1) stationnaire.
*(Piste : $\operatorname{Cov}(X_1,X_{1+k})=\sigma^2\varphi^k$, puis sommer la série
géométrique.)*

**E14.2.** Pour un AR(1) à $\varphi=0{,}6$, calculer $\sigma^2_{LR}/\sigma^2$ et la taille
effective de 250 observations. *(Réponse : facteur 4 ; $n_{\text{eff}}=62{,}5$.)*

**E14.3.** Que devient $\sigma^2_{LR}$ pour un AR(1) à $\varphi$ **négatif** ? *La dépendance
peut-elle rendre l'inférence **plus** précise que l'indépendance ? Interpréter.*

**E14.4.** Expliquer en quatre phrases pourquoi la non-normalité est « réparée » par un $n$ plus
grand alors que la dépendance forte est « aggravée ». *Relier au tableau du § 14.3.*

**E14.5.** Pourquoi la série $\sum_k\operatorname{Cov}(V_1,V_{1+k})$ diverge-t-elle pour une
marche aléatoire ? *(Piste : $\operatorname{Cov}(V_i,V_j)=\sigma^2\min(i,j)$ — elle ne décroît
même pas.)*

**E14.6 — orientée finance.** Sur une série obtenue avec `import_societe.py` :
1. estimer l'autocorrélation d'ordre 1 des **rendements**, en déduire $n_{\text{eff}}$ pour un an
   de données ;
2. refaire l'estimation sur les **prix** (colonne `Close` brute) ;
3. dire laquelle des deux séries relève du régime 1 et laquelle du régime 2.

**Question de synthèse** : le TCL vous autorise-t-il à traiter la moyenne annuelle de rendements
comme gaussienne ? *(Réponse attendue : la non-normalité, oui, largement ; l'autocorrélation des
rendements est en général faible, donc acceptable ; mais si vous travaillez sur les **prix** et
non sur les rendements, vous êtes dans le régime 2 et rien ne tient.)*

---

## 14.6 À retenir

- **Sans indépendance, deux régimes sans rapport.**
- **Dépendance faible** : le TCL tient, mais avec $\sigma^2_{LR}=\sigma^2+2\sum_k\operatorname{Cov}$.
  L'erreur est grave, **bornée**, et **entièrement corrigible** (HAC / Newey–West).
- **Dépendance forte** (marche aléatoire) : **plus de TCL du tout**, la couverture tend vers 0,
  et il faut changer de cadre (Donsker, mouvement brownien).
- ⭐ **Le renversement** : augmenter $n$ **répare** la non-normalité et **aggrave** la dépendance.
  C'est ce qui justifie de classer l'indépendance avant la normalité dans toute liste
  d'hypothèses.
- **$n_{\text{eff}}=n\frac{1-\varphi}{1+\varphi}$** : à $\varphi=0{,}8$, 100 observations n'en
  valent que 11.

---

⬅️ [Module 13 — Portée et limites du TCL](13-portee-et-limites-du-tcl.md) ·
➡️ [Module 15 — La loi du $\chi^2$](15-loi-du-chi2.md) ·
🏠 [Sommaire](README.md)
