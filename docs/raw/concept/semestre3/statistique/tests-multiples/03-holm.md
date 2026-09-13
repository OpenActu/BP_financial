# Module 3 — Holm ⭐

**Durée : 2 h 30.** Le module pivot du cours. Holm (1979) fait strictement mieux
que Bonferroni, sous exactement les mêmes hypothèses, pour le même coût de calcul.
C'est l'un des rares cas où une méthode en **domine** une autre sans contrepartie
— et où continuer d'employer l'ancienne n'a aucune justification.

---

## 3.1 L'idée, en une phrase

Bonferroni divise par $m$ **à chaque comparaison**. Mais une fois la plus petite
$p$-valeur rejetée, il ne reste au plus que $m-1$ hypothèses nulles vraies : rien
n'oblige à continuer de diviser par $m$.

> 🔑 **Holm est Bonferroni appliqué à un $m$ qui décroît.** Toute la procédure
> découle de cette remarque, et toute la démonstration consiste à vérifier qu'on a
> le droit de la faire.

## 3.2 La procédure

Trier les $p$-valeurs : $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$, et noter
$H_{(i)}$ l'hypothèse correspondante.

> **Procédure de Holm (descendante).**
>
> 1. Si $p_{(1)} > \dfrac{\alpha}{m}$ → **on s'arrête, rien n'est rejeté.**
> 2. Sinon rejeter $H_{(1)}$, puis comparer $p_{(2)}$ à $\dfrac{\alpha}{m-1}$.
> 3. Continuer : à l'étape $i$, comparer $p_{(i)}$ à $\dfrac{\alpha}{m-i+1}$.
> 4. **Au premier échec, on s'arrête** : $H_{(i)}$ et **toutes les suivantes** sont
>    conservées, sans être testées.

L'arrêt au premier échec est essentiel : sans lui, la procédure ne contrôlerait
plus rien. On ne « repêche » jamais une hypothèse au-delà du point d'arrêt, même si
sa $p$-valeur passe sous son propre seuil.

| Rang $i$ | Seuil |
|---|---|
| 1 | $\alpha/m$ — identique à Bonferroni |
| 2 | $\alpha/(m-1)$ |
| $\vdots$ | $\vdots$ |
| $m$ | $\alpha/1 = \alpha$ — aucune correction |

## 3.3 La démonstration du contrôle du FWER

C'est la partie qui mérite d'être lue lentement : elle est courte, et elle est la
seule raison d'avoir le droit d'employer la procédure.

Soit $\mathcal M_0$ l'ensemble des **vraies** nulles, $m_0 = |\mathcal M_0| \ge 1$
(si $m_0 = 0$, aucun faux positif n'est possible et il n'y a rien à démontrer).

Supposons qu'**au moins une vraie nulle soit rejetée**, et soit $j$ le **plus petit
rang** tel que $H_{(j)}$ soit une vraie nulle rejetée.

1. Holm ayant rejeté jusqu'au rang $j$, tous les rangs $1,\dots,j-1$ ont été
   rejetés — et par minimalité de $j$, **ce sont tous de fausses nulles.**
2. Il y a $m - m_0$ fausses nulles en tout, donc $j - 1 \le m - m_0$, c'est-à-dire
   $$m - j + 1 \;\ge\; m_0$$
3. Le rejet au rang $j$ exige $p_{(j)} \le \dfrac{\alpha}{m-j+1} \le \dfrac{\alpha}{m_0}$.
4. Or $H_{(j)}$ est une vraie nulle, donc
   $\min_{i \in \mathcal M_0} p_i \le p_{(j)} \le \alpha/m_0$.

L'événement « au moins un faux positif » **implique** donc
$\min_{i\in\mathcal M_0} p_i \le \alpha/m_0$. Par Boole :

$$\mathrm{FWER} \;\le\; P\Bigl(\min_{i\in\mathcal M_0} p_i \le \tfrac{\alpha}{m_0}\Bigr)
\;\le\; \sum_{i\in\mathcal M_0} P\Bigl(p_i \le \tfrac{\alpha}{m_0}\Bigr)
\;\le\; m_0 \cdot \frac{\alpha}{m_0} \;=\; \alpha \qquad \blacksquare$$

> 🔑 **Exactement les mêmes ingrédients que Bonferroni** : Boole, et l'uniformité
> des $p$-valeurs sous $H_0$. **Aucune hypothèse d'indépendance n'est ajoutée.**
> C'est ce qui rend la domination du § 3.5 gratuite : on ne paie rien pour elle.

## 3.4 La forme en $p$-valeurs ajustées

Pour publier un résultat comparable à n'importe quel $\alpha$ :

$$\tilde p_{(i)} = \max_{j \le i} \Bigl[(m-j+1)\,p_{(j)}\Bigr], \qquad
\text{plafonnée à } 1$$

Le $\max$ n'est pas cosmétique : il force la suite $\tilde p$ à être **croissante**,
ce qui traduit exactement la règle d'arrêt du § 3.2. Sans lui, une $p$-valeur
tardive pourrait ressortir « significative » après un arrêt — et la procédure
perdrait son contrôle.

**Rejeter $H_i$ si $\tilde p_i \le \alpha$** est alors rigoureusement équivalent à
la procédure séquentielle.

## 3.5 Pourquoi Bonferroni est périmé

Pour tout rang $i$ :

$$\frac{\alpha}{m-i+1} \;\ge\; \frac{\alpha}{m}$$

Le seuil de Holm est donc **toujours au moins aussi grand** que celui de
Bonferroni, et strictement plus grand dès $i \ge 2$.

| | Bonferroni | Holm |
|---|---|---|
| Contrôle le FWER | ✅ | ✅ |
| Hypothèses | $p$ uniformes | $p$ uniformes — **les mêmes** |
| Valide sous dépendance quelconque | ✅ | ✅ |
| Seuil au rang 1 | $\alpha/m$ | $\alpha/m$ — **identique** |
| Seuil aux rangs suivants | $\alpha/m$ | $\alpha/(m-i+1)$ — **plus grand** |
| Coût de calcul | $O(m)$ | $O(m\log m)$ — un tri |

> 🔑 **Holm rejette tout ce que Bonferroni rejette, et parfois davantage.** Jamais
> moins. C'est une **domination uniforme**, et elle ne coûte qu'un tri. Il n'existe
> aucune situation où préférer Bonferroni soit justifié autrement que par
> l'habitude.

## 3.6 Le code

```python
def holm(p, alpha=0.05):
    """Rend (p ajustees, rejets), dans l'ordre d'entree."""
    m = len(p)
    ordre = sorted(range(m), key=lambda i: p[i])
    ajustees, precedent = [0.0] * m, 0.0
    for rang, i in enumerate(ordre):
        precedent = min(1.0, max(precedent, (m - rang) * p[i]))
        ajustees[i] = precedent
    return ajustees, [a <= alpha for a in ajustees]
```

Le `max(precedent, …)` est la monotonie du § 3.4 ; le `min(1.0, …)` le plafond.
C'est, à l'identique, la fonction `holm()` du moteur de
l'[expérience 13](../../../../../done/experimentation/experience_13/mesure.md).

**Contrôle** — `statsmodels` doit rendre la même chose :

```python
from statsmodels.stats.multitest import multipletests
p = [0.005, 0.011, 0.02, 0.30, 0.60]
print(holm(p)[0])                                        # [0.025, 0.044, 0.06, 0.6, 0.6]
print(multipletests(p, alpha=0.05, method="holm")[1])    # identique
```

Sur ce jeu, Holm rejette **2** hypothèses là où Bonferroni n'en rejetait qu'**une**
(module 2, E2.3) : le rang 2 est comparé à $\alpha/4 = 0{,}0125$, et $0{,}011$ y
passe.

## 3.7 Le cas chiffré de l'expérience 13

L'[expérience 13](../../../../../done/experimentation/experience_13/bilan.md) du
dépôt mesure **18 cellules** et trouve **exactement une** $p$-valeur sous 5 % :
$p = 0{,}02533$. Le module 1 avait annoncé le chiffre attendu sous $H_0$ :
$18 \times 0{,}05 = 0{,}9$, soit environ une.

| | Valeur |
|---|---|
| $p$ brute, la plus petite des 18 | 0,02533 |
| Seuil de Holm au rang 1 | $0{,}05/18 = 0{,}00278$ |
| $p$ ajustée | $18 \times 0{,}02533 = \mathbf{0{,}4560}$ |

Il lui aurait fallu être **dix fois plus petite**. Holm dit : c'est ce que le
hasard produit quand on pose dix-huit questions.

### Le contre-exemple qui vaut le cours

La même expérience a d'abord **échoué** parce que son **contrôle de validité** —
six cellules d'un témoin nul — était comparé à des intervalles à 95 %
**non corrigés**. Or six tests non corrigés se déclenchent à tort

$$1 - 0{,}95^6 = \mathbf{26{,}5\,\%} \text{ du temps}$$

Une cellule sur six est effectivement sortie, à $p = 0{,}030667$, et le moteur a
déclaré le dispositif défectueux — **à tort**. Après Holm sur cette seconde
famille : $6 \times 0{,}030667 = \mathbf{0{,}1840}$, et le témoin redevient
compatible avec zéro, comme sa construction l'exigeait (moyenne $-0{,}054$ point
sur 12 482 tirages).

> ⚠️ **Un garde-fou non corrigé n'est pas un garde-fou.** Il se déclenchait plus
> souvent que le test qu'il protégeait. Une correction de multiplicité s'applique
> à **toute famille de tests**, y compris — et surtout — à ceux qui servent à
> valider l'instrument.

## 3.8 Simulation

### S3.1 — Holm contrôle bien le FWER, et rejette plus

```python
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(3)

def compare(m, m0, N=50_000, alpha=0.05, effet=3.5):
    z = rng.standard_normal((N, m)); z[:, m0:] += effet
    p = 2 * norm.sf(np.abs(z))
    bonf = p <= alpha / m
    rang = np.argsort(p, axis=1)
    trie = np.take_along_axis(p, rang, axis=1)
    seuils = alpha / (m - np.arange(m))
    passe = np.cumprod(trie <= seuils, axis=1).astype(bool)   # arret au 1er echec
    holm = np.zeros_like(passe)
    np.put_along_axis(holm, rang, passe, axis=1)
    return (bonf[:, :m0].any(1).mean(), holm[:, :m0].any(1).mean(),
            bonf[:, m0:].mean(), holm[:, m0:].mean())

for m0 in (20, 15, 10, 5):
    fb, fh, pb, ph = compare(20, m0)
    print(f"m0={m0:>3}  FWER bonf={fb:.4f} holm={fh:.4f}   "
          f"puissance bonf={pb:.3f} holm={ph:.3f}")
```

**Ce que vous devez constater** : les deux FWER restent sous 0,05, et la puissance
de Holm est **toujours ≥** celle de Bonferroni, l'écart croissant quand $m_0$
diminue.

## 3.9 Exercices

**E3.1.** Refaire la démonstration du § 3.3 en explicitant où l'arrêt au premier
échec est utilisé. Que se passerait-il si l'on continuait de tester après un
échec ?

**E3.2.** Sur `p = [0.005, 0.011, 0.02, 0.30, 0.60]` et $\alpha = 5\,\%$ :
appliquer Bonferroni puis Holm à la main. Combien de rejets chacun ?
*(Réponse : Bonferroni **1**, Holm **2** — le rang 2 est comparé à
$0{,}05/4 = 0{,}0125$, que $0{,}011$ franchit. Le rang 3 échoue à
$0{,}05/3 = 0{,}0167$, et la procédure s'arrête là.)*

**E3.3.** Montrer que si $p_{(1)} > \alpha/m$, Holm et Bonferroni rejettent tous
deux l'ensemble vide. En déduire que la domination est **large**, jamais stricte
partout.

**E3.4.** Vérifier sur un exemple que les $\tilde p$ du § 3.4 sont bien croissantes,
et construire un jeu de $p$ où le `max` change effectivement une valeur.

**E3.5 — orienté dépôt.** L'expérience 13 déclare deux familles (18 et 6). Calculer
les $p$ ajustées de sa plus petite valeur dans les trois découpages du § 1.3 : une
famille de 24, deux familles (18 + 6), 24 familles d'un test. Que change le
découpage sur la conclusion ?

## 3.10 À retenir

- **Holm = Bonferroni à $m$ décroissant**, avec arrêt au premier échec.
- Seuil au rang $i$ : $\alpha/(m-i+1)$. Le rang 1 est identique à Bonferroni.
- La démonstration n'ajoute **aucune hypothèse** : Boole et l'uniformité, comme
  Bonferroni. **Valide sous dépendance arbitraire.**
- Forme ajustée : $\tilde p_{(i)} = \max_{j\le i}[(m-j+1)p_{(j)}]$, plafonnée à 1.
  Le `max` encode l'arrêt.
- **Domination uniforme** : jamais moins de rejets que Bonferroni, souvent plus,
  pour le prix d'un tri. Il n'y a pas de raison de préférer Bonferroni.
- Une correction s'applique à **toute** famille de tests — y compris aux contrôles
  de validité, sous peine d'un garde-fou qui se déclenche 26,5 % du temps.

---

⬅️ [Module 2 — Bonferroni](02-bonferroni.md) ·
➡️ [Module 4 — Choisir : FWER, FDR, et la famille](04-choisir.md) ·
🏠 [Sommaire](README.md)
