# Module 6 — La couverture optimale ⭐

**Durée : 1 h 15.** Prérequis : [module 5](05-la-vente-a-decouvert.md) et surtout
[`modele.md`](../modele/modele.md), dont ce module est une **application directe**.

> **La question traitée.** On détient un portefeuille $V$ qu'on ne veut pas vendre, et on veut
> réduire son risque en prenant une position vendeuse de taille $h$ sur un instrument $M$ (indice,
> future, ETF). Quelle taille $h$ ?

**Réponse : celle que `modele.md` a déjà démontrée.** Ce module ne contient aucun théorème
nouveau — il contient la reconnaissance qu'un théorème déjà prouvé répond à une deuxième question.

---

## 6.1 Le problème, écrit proprement

Le portefeuille couvert, sur une période, rapporte

$$r_{\text{couvert}} = r_V - h\,r_M .$$

On cherche le $h$ qui minimise sa variance :

$$\min_h \;\operatorname{Var}(r_V-h\,r_M)
= \operatorname{Var}(r_V) - 2h\operatorname{Cov}(r_V,r_M) + h^2\operatorname{Var}(r_M).$$

> 🔑 **C'est le trinôme de l'[étape 3 de `modele.md`](../modele/03-developpement-du-carre.md)**, à
> un changement de nom près : $V\to V$, $T\to M$, $r\to h$. La mise sous forme canonique de
> l'[étape 4](../modele/04-forme-canonique.md) donne immédiatement, **sans dériver** :

$$\boxed{\;h^\star=\frac{\operatorname{Cov}(r_V,r_M)}{\operatorname{Var}(r_M)}=\beta,\qquad
\operatorname{Var}_{\min}=\operatorname{Var}(r_V)\bigl(1-\rho^2_{V,M}\bigr)\;}$$

et, ce qui servira au § 6.5, la **pénalité exacte** d'une couverture mal dimensionnée :

$$\boxed{\;\operatorname{Var}(r_V-h\,r_M)=\underbrace{\operatorname{Var}(r_V)(1-\rho^2)}_{\text{irréductible}}
+\underbrace{\operatorname{Var}(r_M)\,(h-h^\star)^2}_{\text{erreur de couverture}}\;}$$

| Objet de `modele.md` | Nom en couverture |
|---|---|
| Pente $r_{\min}=\operatorname{Cov}/\operatorname{Var}$ | **Ratio de couverture** $h^\star$, alias $\beta$ |
| Variance résiduelle $\operatorname{Var}(V)(1-\rho^2)$ | **Risque spécifique**, non couvrable |
| $\rho^2$ ([étape 5](../modele/05-coefficient-de-correlation.md)) | **Efficacité de couverture** — la part de variance annulée |
| Résidus centrés ([étape 1](../modele/01-elimination-de-l-ordonnee.md)) | La couverture ne biaise pas la moyenne |
| Projection orthogonale ([lecture géométrique](../modele/05-coefficient-de-correlation.md)) | On **retranche la composante commune**, on garde l'orthogonale |

> ⭐ **Couvrir, c'est projeter.** Le portefeuille couvert est le **résidu** de la projection
> orthogonale de $r_V$ sur $r_M$ ([algèbre § 4](../algebre/04-projection-orthogonale.md)). Ce qui
> reste est, par construction, **non corrélé** à l'instrument de couverture : c'est la définition
> même de « avoir enlevé le marché ».

---

## 6.2 Ce qui se couvre, et ce qui ne se couvre pas

Le théorème dit que $1-\rho^2$ de la variance **survit à la meilleure couverture possible**. Deux
exemples sur 12 rendements mensuels, avec le même indice
($\sigma_M=2{,}12\,\%$ mensuel, soit **7,33 %** annualisé) :

| Mois | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Indice $r_M$ | +2,0 | −1,5 | +3,0 | +0,5 | −2,5 | +1,0 | +4,0 | −3,0 | +1,5 | 0,0 | −1,0 | +2,5 |
| Ligne unique $r_A$ | +2,4 | −2,0 | +2,1 | −2,3 | −3,7 | +1,6 | +6,8 | −0,9 | +5,2 | −2,4 | −4,1 | +4,6 |
| Portefeuille $r_P$ (15 lignes) | +2,1 | −2,3 | +3,3 | +0,7 | −2,6 | +1,3 | +4,3 | −3,3 | +1,5 | −0,3 | −0,6 | +2,8 |

*(en %, moments normalisés par $n$ comme dans `modele.md`)*

| | Ligne unique $A$ | Portefeuille $P$ |
|---|---|---|
| $\sigma$ annualisée, non couverte | 12,21 % | 8,09 % |
| $h^\star=\beta$ | **1,3614** | **1,0965** |
| $\rho^2$ (efficacité) | **66,79 %** | **98,65 %** |
| $\sigma$ résiduelle annualisée | **7,04 %** | **0,94 %** |
| Réduction de variance | −66,8 % | −98,6 % |

Variance résiduelle en fonction de $h$ (mensuelle) :

| $h$ | Ligne $A$ | Portefeuille $P$ |
|---|---|---|
| 0,00 (non couvert) | 12,21 % | 8,09 % |
| 0,50 | 9,45 % | 4,47 % |
| 0,75 | 8,34 % | 2,71 % |
| 1,00 | 7,52 % | 1,18 % |
| **$h^\star$** | **7,04 %** | **0,94 %** |
| 1,25 | 7,08 % | 1,47 % |
| 1,50 | 7,11 % | 3,10 % |
| 2,00 | 8,45 % | 6,69 % |

*(volatilités annualisées du portefeuille couvert)*

> ⭐ **Le résultat du module.** Sur une **ligne unique**, la meilleure couverture possible ne
> supprime que les deux tiers de la variance : il reste 7 % de volatilité annualisée, purement
> spécifique à l'entreprise — résultat de bénéfices, litige, changement de dirigeant. Sur un
> **portefeuille diversifié**, elle en supprime 98,6 %.
>
> **On ne couvre pas une action, on couvre un portefeuille.** Vendre l'indice contre une ligne
> unique, c'est troquer un risque de marché contre un risque idiosyncratique presque aussi grand,
> en payant le portage des deux côtés.

---

## 6.3 Passage aux quantités réelles

$h^\star$ est un ratio ; il faut le convertir en **contrats** ou en **euros**.

$$N=\frac{h^\star\times V_{\text{portefeuille}}}{\text{indice}\times\text{multiplicateur}}$$

Exemple : portefeuille de 250 000 €, $\beta=1{,}15$, CAC 40 à 7 800 points, contrat FCE à
10 € le point (valeur notionnelle **78 000 €**) :

$$N=\frac{1{,}15\times250\,000}{7\,800\times10}=3{,}686\ \text{contrats}.$$

| Choix | Exposition résiduelle | En % du portefeuille |
|---|---|---|
| $N=3$ | +53 500 € | **+21,4 %** |
| $N=4$ | −24 500 € | **−9,8 %** |
| Contrat *mini* (1 € le point), $N=37$ | −1 100 € | −0,44 % |

> ⚠️ **La granularité est un risque en soi.** Sur un portefeuille de 250 000 €, le contrat
> standard ne permet pas de couvrir mieux qu'à ±10 % près : l'erreur d'arrondi est du même ordre
> que le risque résiduel qu'on cherche à éliminer. En dessous de ~80 000 € de portefeuille, le
> contrat standard est **inutilisable** pour une couverture fine — d'où le recours aux contrats de
> taille réduite, aux ETF ou aux options ([module 7](07-couvrir-en-pratique.md)).

---

## 6.4 Couvrir supprime aussi le rendement

C'est l'angle mort du sujet. Le portefeuille couvert a pour espérance

$$E[r_V]-h^\star E[r_M],$$

et si le portefeuille n'a pas de performance propre au-delà de son exposition au marché
(hypothèse du MEDAF : $\alpha=0$), cette espérance vaut approximativement le **taux sans risque**
— dont il faut encore retrancher le **portage** de la couverture.

Sur les données du § 6.2 (l'indice fait +6,50 % annualisé sur la période) :

| | Non couvert | Couvert à $h^\star$ |
|---|---|---|
| Ligne $A$ | +7,30 % annualisé | **−1,55 %** |
| Portefeuille $P$ | +6,90 % annualisé | **−0,23 %** |

> 🔑 **Une couverture permanente n'est pas une amélioration du portefeuille, c'est une sortie
> déguisée** — plus chère, car elle paie le portage et laisse le risque résiduel. Si l'on veut
> durablement moins de risque de marché, **détenir moins d'actions** est strictement supérieur :
> même effet, sans frais, sans appel de marge et sans risque de base.
>
> La couverture se justifie quand la vente est **impossible ou coûteuse** : plus-values latentes à
> ne pas déclencher, titres non liquides, participation qu'on veut conserver pour des raisons
> autres que financières, ou horizon très court sur lequel on veut neutraliser un événement daté
> (résultat, élection, décision de banque centrale).

---

## 6.5 $h^\star$ est estimé, et le minimum est plat

Le [module 7 du cours de Student](../statistique/loi-de-student/07-student-en-regression.md) donne
l'écart type de la pente estimée ; appliqué à nos deux exemples ($n=12$, $t_{10;0{,}975}=2{,}228$) :

| | $h^\star$ | $\operatorname{SE}$ | IC 95 % | $t$ |
|---|---|---|---|---|
| Ligne $A$ | 1,3614 | 0,3036 | **[0,685 ; 2,038]** | 4,48 |
| Portefeuille $P$ | 1,0965 | 0,0406 | [1,006 ; 1,187] | 26,99 |

**Un an de données mensuelles ne permet pas de savoir si le $\beta$ d'une ligne vaut 0,7 ou 2,0.**
Heureusement, la forme canonique dit exactement ce que cette incertitude coûte :

$$\operatorname{Var}(r_V-h\,r_M)=\operatorname{Var}_{\min}+\operatorname{Var}(r_M)(h-h^\star)^2 .$$

| Erreur sur $h$ | Variance résiduelle, ligne $A$ | Variance résiduelle, portefeuille $P$ |
|---|---|---|
| ±0,10 | ×1,011 | ×1,606 |
| ±0,25 | ×1,068 | ×4,787 |
| ±0,50 | ×1,271 | ×16,150 |

> ⭐ **Paradoxe apparent, et il est important.** L'erreur d'estimation est **grande** là où elle
> ne coûte presque rien (ligne unique : le résidu domine déjà) et **petite** là où elle coûte
> très cher (portefeuille bien couvert : le résidu est minuscule, donc toute erreur le multiplie).
> Une couverture efficace est une couverture **fragile** : elle exige un $\beta$ à jour, donc un
> réajustement régulier — et chaque réajustement coûte des frais et déclenche des plus-values.

⚠️ **Et $\beta$ n'est pas constant.** Il dérive avec le secteur, le levier de l'entreprise, le
régime de volatilité — et il **monte en crise**, exactement quand la couverture sert. Estimer sur
une fenêtre glissante, et se rappeler que l'[étape 8 de `modele.md`](../modele/08-test-de-tendance.md)
suppose une indépendance des résidus que des rendements en régimes n'ont pas.

---

## 6.6 Simulation

### S6.1 — Le ratio optimal, la parabole, l'intervalle de confiance

```python
import numpy as np, math

rM = np.array([2.0, -1.5, 3.0, 0.5, -2.5, 1.0, 4.0, -3.0, 1.5, 0.0, -1.0, 2.5]) / 100
rA = np.array([2.4, -2.0, 2.1, -2.3, -3.7, 1.6, 6.8, -0.9, 5.2, -2.4, -4.1, 4.6]) / 100
rP = np.array([2.1, -2.3, 3.3, 0.7, -2.6, 1.3, 4.3, -3.3, 1.5, -0.3, -0.6, 2.8]) / 100
n, t975 = 12, 2.2281                       # t de Student a n-2 = 10 ddl

def moments(x, m):
    Vm = ((m - m.mean()) ** 2).mean()
    Vx = ((x - x.mean()) ** 2).mean()
    C = ((m - m.mean()) * (x - x.mean())).mean()
    return Vm, Vx, C

for nom, x in (("ligne A", rA), ("portefeuille P", rP)):
    Vm, Vx, C = moments(x, rM)
    h = C / Vm                              # = r_min de modele.md, etape 4
    rho2 = C ** 2 / (Vm * Vx)               # = efficacite de couverture, etape 5
    se = math.sqrt(Vx * (1 - rho2) / ((n - 2) * Vm))
    print(f"\n{nom}: h*={h:.4f}  rho2={rho2:.2%}  "
          f"sigma non couverte={math.sqrt(Vx * 12):.2%}  "
          f"residuelle={math.sqrt(Vx * (1 - rho2) * 12):.2%}")
    print(f"   IC95(h*) = [{h - t975 * se:.3f} ; {h + t975 * se:.3f}]")
    for hh in (0, 0.5, 0.75, 1.0, h, 1.25, 1.5, 2.0):
        direct = Vx - 2 * hh * C + hh ** 2 * Vm
        canon = Vx * (1 - rho2) + Vm * (hh - h) ** 2      # forme canonique, etape 4
        assert abs(direct - canon) < 1e-15
        print(f"   h={hh:>6.3f}  sigma annualisee={math.sqrt(direct * 12):>6.2%}")

# conversion en contrats
V, beta, idx, mult = 250_000, 1.15, 7800, 10
N = beta * V / (idx * mult)
print(f"\nN exact = {N:.3f} ; arrondi a 3 : {beta * V - 3 * idx * mult:+.0f} EUR residuels ; "
      f"a 4 : {beta * V - 4 * idx * mult:+.0f} EUR")
```

L'`assert` est le cœur de la simulation : il vérifie, à la quinzième décimale, que la **forme
canonique de l'étape 4 de `modele.md`** décrit exactement la pénalité de couverture.

---

## 6.7 Exercices

**E6.1.** Déduire $h^\star$ et $\operatorname{Var}_{\min}$ de la
[forme canonique](../modele/04-forme-canonique.md) **sans dériver**, en recopiant l'étape 4 avec
les nouveaux noms.

**E6.2.** Montrer que $\operatorname{Cov}(r_V-h^\star r_M,\;r_M)=0$. *Quelle propriété
géométrique cela exprime-t-il, et quel § de `modele.md` l'établit ?*

**E6.3.** Un portefeuille a $\rho^2=0{,}80$ contre l'indice et $\sigma=25\,\%$. Quelle volatilité
subsiste après couverture parfaite ? *Est-ce moins que la volatilité de l'indice lui-même ?*

**E6.4.** Sur les données du script, calculer le $\beta$ de cinq valeurs du CAC 40 sur fenêtres
glissantes de 24 mois, sur 10 ans. *Tracer les cinq trajectoires : le $\beta$ est-il une
constante ?*

**E6.5.** Reprendre E6.4 en séparant les mois où l'indice baisse de plus de 3 % et les autres.
*Le $\beta$ de baisse est-il le même que le $\beta$ de hausse ? Conséquence pour une couverture.*

**E6.6.** Un portefeuille de 60 000 € doit être couvert avec le contrat standard (78 000 € de
notionnel). *Quelles sont les options, et laquelle laisse le moins de risque résiduel ?*

**E6.7.** Démontrer que couvrir à $h^\star$ puis lever la position couverte d'un facteur $L$
donne la même variance que couvrir directement une position levée. *Le levier et la couverture
commutent-ils ? Et les appels de marge ?*

---

## 6.8 À retenir

- ⭐ **Le ratio de couverture de variance minimale est $h^\star=\operatorname{Cov}/\operatorname{Var}=\beta$**,
  et la variance qui survit est $\operatorname{Var}(r_V)(1-\rho^2)$. C'est
  [`modele.md`](../modele/modele.md) mot pour mot ; il n'y a pas de second théorème.
- **$\rho^2$ est l'efficacité de couverture**, et $1-\rho^2$ ce qu'aucune couverture par $M$ ne
  peut atteindre.
- ⭐ **Couvrir une ligne unique ne supprime que ~2/3 de sa variance** ; couvrir un portefeuille
  diversifié en supprime ~99 %. La diversification est un **préalable** à la couverture, pas une
  alternative.
- **La pénalité d'une erreur de dimensionnement est $\operatorname{Var}(r_M)(h-h^\star)^2$** —
  quadratique, donc indulgente près de l'optimum, et d'autant plus visible que la couverture est
  bonne.
- ⚠️ **Une couverture efficace est fragile** : le résidu est petit, donc toute erreur sur $\beta$
  le multiplie. Et $\beta$ est mal estimé, non constant, et augmente en crise.
- ⭐ **Couvrir supprime le rendement en même temps que le risque.** Une couverture permanente est
  une vente coûteuse ; elle ne se justifie que si vendre est impossible, fiscalement coûteux, ou
  si l'horizon est court et l'événement daté.
- **La granularité des contrats est un risque réel** en dessous de quelques centaines de milliers
  d'euros.

---

⬅️ [Module 5 — La vente à découvert](05-la-vente-a-decouvert.md) ·
➡️ [Module 7 — Couvrir en pratique](07-couvrir-en-pratique.md) ·
🏠 [Sommaire](README.md) ·
📄 [`modele.md`](../modele/modele.md)
