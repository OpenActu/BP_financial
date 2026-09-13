# Module 2 — Bonferroni

**Durée : 2 h.** La correction la plus simple qui existe, dont la démonstration
tient en une ligne — et dont les deux défauts justifient à eux seuls le module
suivant.

---

## 2.1 L'énoncé

> **Procédure de Bonferroni.** Rejeter $H_i$ si $p_i \le \dfrac{\alpha}{m}$.
>
> Alors $\mathrm{FWER} \le \alpha$.

C'est tout. Pas de tri, pas d'étapes, pas de condition sur les tests.

## 2.2 La démonstration

Notons $\mathcal M_0$ l'ensemble des indices dont l'hypothèse nulle est **vraie**,
et $m_0 = |\mathcal M_0| \le m$. Un faux positif est un $i \in \mathcal M_0$ rejeté.

$$\mathrm{FWER}
= P\Bigl(\bigcup_{i\in\mathcal M_0}\{p_i \le \alpha/m\}\Bigr)
\;\underbrace{\le}_{\text{Boole}}\; \sum_{i\in\mathcal M_0} P(p_i \le \alpha/m)
\;\underbrace{\le}_{p_i \text{ uniforme}}\; m_0\,\frac{\alpha}{m}
\;\le\; \alpha \qquad \blacksquare$$

Deux inégalités, et c'est fini.

- La première est l'**inégalité de Boole** : $P(\bigcup A_i) \le \sum P(A_i)$. Elle
  est vraie pour des événements **quelconques**, dépendants ou non.
- La seconde demande seulement que $p_i$ soit **uniforme sur $[0,1]$ sous $H_0$**,
  ou super-uniforme ($P(p_i\le t)\le t$), ce qui est le cas de toute $p$-valeur
  correctement construite.

## 2.3 Ce que Bonferroni ne suppose pas — et c'est sa force

| Hypothèse | Exigée ? |
|---|---|
| $p_i$ uniforme sous $H_0$ | **oui** |
| Indépendance des tests | **non** |
| Même loi d'un test à l'autre | non |
| Même taille d'échantillon | non |
| Normalité de quoi que ce soit | non |

> 🔑 **La validité sous dépendance arbitraire est ce qui rend Bonferroni — et Holm
> après lui — utilisable en finance.** Les tests qu'on y mène sont massivement
> corrélés : mêmes séries, seuils emboîtés, fenêtres qui se recouvrent. Toute
> procédure exigeant l'indépendance y serait invalide. Boole, elle, ne demande
> rien.

## 2.4 La forme en $p$-valeurs ajustées

Comparer $p_i$ à $\alpha/m$ ou comparer $m\,p_i$ à $\alpha$ est la même chose. On
préfère souvent publier la seconde forme :

$$\tilde p_i = \min(1,\ m\,p_i)$$

**Intérêt** : $\tilde p_i$ se lit comme une $p$-valeur ordinaire, et se compare à
n'importe quel $\alpha$ sans refaire le calcul. C'est la forme que rendent les
moteurs du dépôt, et celle que publient les bilans.

## 2.5 Les deux défauts

### a. Le conservatisme — la perte tient dans une inégalité

Reprenez la démonstration : la dernière étape majore $m_0\alpha/m$ par $\alpha$.
Cette majoration est **exacte seulement si $m_0 = m$**, c'est-à-dire si **aucune**
hypothèse alternative n'est vraie.

Or on teste rarement que du bruit. Si 10 des 20 hypothèses sont fausses, le FWER
réel est majoré par $10\alpha/20 = \alpha/2$ : on s'est protégé **deux fois trop**,
et cette prudence se paie intégralement en **puissance**.

### b. Il traite toutes les $p$-valeurs de la même façon

C'est le défaut structurel, et le module 3 ne corrige que celui-là. Bonferroni
compare **la plus petite** $p$-valeur et **la plus grande** au même seuil
$\alpha/m$. Pourtant, une fois qu'on a rejeté la plus petite, il ne reste plus que
$m-1$ nulles possibles — et rien n'oblige à continuer de diviser par $m$.

> ⚠️ **Le conservatisme n'est pas une sécurité gratuite.** Un test qui ne rejette
> jamais contrôle parfaitement le FWER et n'apprend rien. La question n'est pas
> « suis-je assez prudent ? » mais « **quelle puissance ai-je payée pour cette
> prudence ?** ».

## 2.6 Šidák — la variante qu'on peut oublier

Sous **indépendance**, l'inversion exacte de $1-(1-\alpha_S)^m = \alpha$ donne

$$\alpha_S = 1-(1-\alpha)^{1/m}$$

légèrement plus grand que $\alpha/m$, donc légèrement plus puissant. Le gain :

| $m$ | $\alpha/m$ | $\alpha_S$ | Gain |
|---|---|---|---|
| 5 | 0,010000 | 0,010206 | +2,1 % |
| 18 | 0,002778 | 0,002846 | **+2,4 %** |
| 100 | 0,000500 | 0,000513 | +2,6 % |

> 🔑 **Deux pour cent de seuil, contre l'hypothèse d'indépendance.** C'est un
> mauvais marché, et c'est pourquoi Šidák ne se rencontre presque jamais en
> pratique. Retenez-le pour savoir le reconnaître, pas pour l'employer.

## 2.7 Simulation

### S2.1 — Vérifier que le FWER est bien contrôlé

```python
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(2)

def p_valeurs(m, m0, N=100_000, effet=3.5):
    """m tests, dont m0 vraies nulles ; les m-m0 autres portent un vrai effet."""
    z = rng.standard_normal((N, m))
    z[:, m0:] += effet                      # les alternatives, decalees
    return 2 * norm.sf(np.abs(z))

alpha, m = 0.05, 20
for m0 in (20, 15, 10, 5):
    p = p_valeurs(m, m0)
    faux = (p[:, :m0] <= alpha / m).any(axis=1)      # au moins un faux positif
    vrais = (p[:, m0:] <= alpha / m).mean()          # puissance par test
    print(f"m0={m0:>3}  FWER={faux.mean():.4f}  (vise <= {alpha})  "
          f"puissance={vrais:.3f}")
```

**Ce que vous devez constater** : le FWER vaut ~0,05 quand $m_0 = m$, et **chute
bien en dessous** quand $m_0$ diminue. C'est le conservatisme du § 2.5a, mesuré.

### S2.2 — Bonferroni à la main

```python
def bonferroni(p, alpha=0.05):
    p = np.asarray(p, dtype=float)
    return np.minimum(1.0, len(p) * p), (len(p) * p <= alpha)

p = [0.005, 0.011, 0.02, 0.30, 0.60]
ajustees, rejets = bonferroni(p)
print(np.round(ajustees, 4), rejets)
# [0.025 0.055 0.1   1.    1.   ]  ->  un seul rejet
```

## 2.8 Exercices

**E2.1.** Démontrer l'inégalité de Boole par récurrence sur le nombre
d'événements.

**E2.2.** Montrer que $\alpha_S = 1-(1-\alpha)^{1/m} \ge \alpha/m$ pour tout
$m \ge 1$, et que le rapport tend vers une limite quand $m\to\infty$. Laquelle ?
*(Réponse : $\alpha_S \to -\ln(1-\alpha)/m$, soit un rapport de
$-\ln(1-\alpha)/\alpha \approx 1{,}026$ à $\alpha = 5\,\%$.)*

**E2.3.** Sur le jeu `p = [0.005, 0.011, 0.02, 0.30, 0.60]`, appliquer Bonferroni à
$\alpha = 5\,\%$. Combien de rejets ? Combien en obtiendrait-on sans correction ?
*(Réponse : **1** contre 3 — seul $0{,}005$ passe sous $\alpha/m = 0{,}01$. Ce même
jeu servira aux modules 3 et 4 : retenez le chiffre.)*

**E2.4.** Un analyste teste $m = 18$ hypothèses et obtient une plus petite
$p$-valeur de $0{,}0253$. Bonferroni la rejette-t-il ? Quelle valeur lui
aurait-il fallu ?

**E2.5 — le piège.** Deux laboratoires testent la même hypothèse, chacun de son
côté, et publient chacun $p = 0{,}03$. Faut-il corriger par $m=2$ ? Discuter en
s'appuyant sur le § 1.3.

## 2.9 À retenir

- **Bonferroni : rejeter si $p_i \le \alpha/m$.** $\mathrm{FWER}\le\alpha$,
  démontré par Boole en une ligne.
- Il ne suppose **rien sur la dépendance** — c'est ce qui le rend applicable à des
  tests corrélés, donc à la finance.
- Forme ajustée : $\tilde p_i = \min(1, m\,p_i)$.
- Son conservatisme vient de la majoration $m_0 \le m$ : plus il y a d'effets
  réels, plus on s'est protégé pour rien.
- Son défaut structurel est de comparer **toutes** les $p$-valeurs au même seuil.
  Le module 3 corrige exactement cela, **sans rien supposer de plus**.
- **Šidák** gagne 2,4 % de seuil contre l'hypothèse d'indépendance : mauvais
  marché.

---

⬅️ [Module 1 — Le risque n'est pas où l'on croit](01-le-probleme.md) ·
➡️ [Module 3 — Holm](03-holm.md) ·
🏠 [Sommaire](README.md)
