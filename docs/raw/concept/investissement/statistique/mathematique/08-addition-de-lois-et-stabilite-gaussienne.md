# Module 8 — Addition de lois et stabilité gaussienne ⭐

**Durée : 1 h.** Prérequis : modules [5](05-fonction-generatrice-des-moments.md) à
[7](07-loi-normale-et-ses-transformees.md).

> **La question traitée.** Soient $Z_1, Z_2$ i.i.d. $\mathcal N(0,1)$ et $a,b\in\mathbb R$.
> Donner la loi de $aZ_1+bZ_2$.

**Ce qui est en jeu.** La réponse — elle est encore gaussienne — n'est **pas** une évidence :
c'est une propriété rare, que très peu de familles de lois possèdent. Et c'est elle qui donne
d'un trait la loi d'échantillonnage $\bar X\sim\mathcal N(\mu,\sigma^2/n)$ dont vit toute
l'inférence des modules 17 à 19.

---

## 8.1 Le résultat

> $$aZ_1+bZ_2\;\sim\;\mathcal N\!\left(0,\;a^2+b^2\right)$$

**Espérance** : par linéarité, $E(aZ_1+bZ_2)=aE(Z_1)+bE(Z_2)=0$. Aucune hypothèse n'est
nécessaire ici.

**Variance** : les $Z_i$ étant **indépendantes**, les covariances croisées s'annulent :
$$\operatorname{Var}(aZ_1+bZ_2)=a^2\operatorname{Var}(Z_1)+b^2\operatorname{Var}(Z_2)=a^2+b^2$$

**Caractère gaussien** : c'est le point non trivial, et il demande une démonstration.

> ⚠️ **Ne confondez pas les deux moitiés.** Espérance et variance d'une combinaison linéaire se
> calculent **pour n'importe quelle loi**. Ce qui est propre à la gaussienne, c'est que la loi du
> résultat appartienne encore à la même famille.

---

## 8.2 La démonstration

C'est le mode d'emploi du § 5.4, appliqué tel quel. Pour $Z\sim\mathcal N(0,1)$ :
$M_Z(t)=e^{t^2/2}$ ([§ 7.2](07-loi-normale-et-ses-transformees.md)).

Les $Z_i$ étant indépendantes, la FGM de la somme est le **produit** des FGM (§ 5.3) :

$$M_{aZ_1+bZ_2}(t)=E\!\left(e^{t(aZ_1+bZ_2)}\right)
=\underbrace{E\!\left(e^{(ta)Z_1}\right)}_{M_Z(ta)}\cdot\underbrace{E\!\left(e^{(tb)Z_2}\right)}_{M_Z(tb)}
=e^{\frac{a^2t^2}{2}}\,e^{\frac{b^2t^2}{2}}=e^{\frac{(a^2+b^2)t^2}{2}}$$

On reconnaît la FGM d'une $\mathcal N(0,a^2+b^2)$. Comme la FGM caractérise la loi (§ 5.3), la
conclusion suit. $\blacksquare$

> 🔑 **L'idée à retenir** : la FGM transforme une **somme** de variables indépendantes en un
> **produit** de fonctions. Et comme la FGM gaussienne est une exponentielle de $t^2$, ce produit
> reste une exponentielle de $t^2$ — la famille gaussienne est **stable** par addition
> d'indépendantes.

**Avec la fonction caractéristique**, c'est le même calcul, et il est plus rigoureux (§ 6.1) :
$\varphi_{aZ_1+bZ_2}(t)=e^{-a^2t^2/2}e^{-b^2t^2/2}=e^{-(a^2+b^2)t^2/2}$.

---

## 8.3 Le cas général

$$X_i\sim\mathcal N(\mu_i,\sigma_i^2)\ \text{indépendantes}
\quad\Longrightarrow\quad
\sum_{i=1}^n a_iX_i\sim\mathcal N\!\left(\sum_i a_i\mu_i,\;\sum_i a_i^2\sigma_i^2\right)$$

C'est ce résultat qui donne immédiatement, avec $a_i=1/n$ :

$$\boxed{\;\bar X\sim\mathcal N\!\left(\mu,\frac{\sigma^2}{n}\right)\;}$$

> 🔑 **Toute la loi d'échantillonnage des modules 17 à 19 est un corollaire d'une ligne de ce
> module-ci.** Et notez bien qu'elle est **exacte**, sans le moindre recours au théorème central
> limite — voir [§ 12.1](12-theoreme-central-limite.md). Le TCL ne servira que si les $X_i$ ne
> sont **pas** gaussiens.

---

## 8.4 La stabilité est une propriété rare

Additionner deux lois indépendantes, c'est **convoler** leurs densités. Le résultat sort en
général de la famille de départ : deux uniformes donnent une loi triangulaire, deux
exponentielles une loi Gamma, deux Student une loi qui n'est pas de Student.

| Famille | Stable par somme d'indépendantes ? |
|---|---|
| Normale | ✅ $\mathcal N(\mu_1,\sigma_1^2)+\mathcal N(\mu_2,\sigma_2^2)=\mathcal N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$ |
| Poisson | ✅ $\mathcal P(\lambda_1)+\mathcal P(\lambda_2)=\mathcal P(\lambda_1+\lambda_2)$ |
| $\chi^2$ | ✅ [module 15](15-loi-du-chi2.md) — la stabilité y sera une propriété de **comptage** |
| Cauchy | ✅ mais sans renormalisation : la moyenne de $n$ Cauchy est une Cauchy |
| Uniforme | ❌ donne une loi triangulaire |
| Exponentielle | ❌ donne une loi Gamma |

Ce qui distingue les familles stables se lit sur la transformée : une famille est stable quand la
**forme** de $\log\varphi$ est préservée par addition. Pour la gaussienne, $\log\varphi=-\sigma^2t^2/2$
— l'addition ne fait qu'ajouter les $\sigma^2$.

---

## 8.5 ⚠️ L'hypothèse qui traîne : la stabilité exige plus qu'on ne croit

Le résultat « une combinaison linéaire de gaussiennes est gaussienne » est **faux** si les $X_i$
sont gaussiennes mais **dépendantes de façon quelconque**.

Le contre-exemple du [§ 9.3](09-vecteur-gaussien.md) exhibe deux variables parfaitement
gaussiennes dont la somme **n'est pas** gaussienne — et dont la corrélation est pourtant nulle.

Ce qu'il faut, c'est ou bien l'**indépendance** (utilisée au § 8.2 pour factoriser la FGM), ou
bien — plus général — que le vecteur $(X_1,\dots,X_n)$ soit un **vecteur gaussien**. C'est
l'objet du [module 9](09-vecteur-gaussien.md).

---

## 8.6 Simulations

### S8.1 — La stabilité, et la loi d'échantillonnage qui en découle

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(4)
N = 400_000
a, b = 1.5, -2.0

Z1, Z2 = rng.standard_normal(N), rng.standard_normal(N)
W = a * Z1 + b * Z2
print(f"Var(W) = {W.var():.4f}   (theorie {a**2 + b**2})")
print("W gaussienne ? KS p =", round(stats.kstest(W / np.sqrt(a**2+b**2), "norm").pvalue, 3))

# le corollaire : Xbar ~ N(mu, sigma²/n), EXACTEMENT
MU, SG, n = 17.0, 2.5, 9
Xb = rng.normal(MU, SG, (N, n)).mean(axis=1)
print(f"\nE(Xbar)   = {Xb.mean():.4f}   (theorie {MU})")
print(f"std(Xbar) = {Xb.std():.4f}   (theorie {SG/np.sqrt(n):.4f})")
print("Xbar gaussienne ? KS p =",
      round(stats.kstest((Xb - MU) / (SG / np.sqrt(n)), "norm").pvalue, 3))
```

Le second bloc est le plus important : **à $n=9$, la loi est déjà exacte**, pas approchée. Aucun
TCL n'intervient.

### S8.2 — La contre-épreuve : les familles qui ne sont pas stables

```python
for nom, tirage in [("normale",       lambda s: rng.standard_normal(s)),
                    ("uniforme",      lambda s: rng.uniform(-1, 1, s)),
                    ("exponentielle", lambda s: rng.exponential(1.0, s))]:
    X = tirage((N, 2))
    S = X.sum(axis=1)
    # la somme suit-elle la MEME famille, à l'échelle près ?
    ref = tirage(N) * np.sqrt(2) if nom != "exponentielle" else tirage(N) * 2
    print(f"{nom:14s} KS(somme vs meme famille rescalee) p = "
          f"{stats.ks_2samp(S, ref).pvalue:.2e}")
```

Seule la normale passe le test. Pour l'uniforme et l'exponentielle, la $p$-valeur est
astronomiquement petite : **la somme a changé de famille**.

---

## 8.7 Exercices

**E8.1.** Refaire la démonstration du § 8.2 avec la **fonction caractéristique**
$\varphi_Z(t)=e^{-t^2/2}$. *Pourquoi est-elle préférable en toute rigueur ?* **(Réponse : elle
existe toujours, alors que la FGM peut être infinie — voir § 5.5.)**

**E8.2.** Démontrer le cas général du § 8.3 par récurrence sur $n$.

**E8.3.** Soient $X_1\sim\mathcal N(0,1)$ et $X_2\sim\mathcal N(0,4)$ indépendantes. Donner la loi
de $X_1+X_2$, celle de $X_1-X_2$, et celle de $2X_1-\tfrac12X_2$.

**E8.4.** Montrer que la somme de deux Poisson indépendantes est une Poisson, par la même
méthode. *(FGM d'une $\mathcal P(\lambda)$ : $e^{\lambda(e^t-1)}$.)*

**E8.5.** Deux uniformes indépendantes sur $[0,1]$ : quelle est la densité de leur somme ?
*Vérifier par simulation, et constater qu'elle est triangulaire — donc non uniforme.*

**E8.6 — orientée finance.** Un portefeuille pèse $w$ sur un titre de rendement
$R_1\sim\mathcal N(\mu_1,\sigma_1^2)$ et $1-w$ sur $R_2\sim\mathcal N(\mu_2,\sigma_2^2)$.
1. Donner la loi du rendement du portefeuille sous hypothèse d'indépendance.
2. Que devient la variance si $\operatorname{Cov}(R_1,R_2)=\rho\sigma_1\sigma_2$ ?
3. Quelle hypothèse du § 8.5 faut-il alors ajouter pour que le résultat reste **gaussien** ?
*(Réponse au [module 9](09-vecteur-gaussien.md) — et c'est précisément l'hypothèse que les
krachs mettent en défaut.)*

---

## 8.8 À retenir

- **$aZ_1+bZ_2\sim\mathcal N(0,a^2+b^2)$** — la famille gaussienne est **stable** par combinaison
  linéaire d'indépendantes.
- **La démonstration est le mode d'emploi du § 5.4** : calculer, multiplier, reconnaître.
- **Cas général** : $\sum_i a_iX_i\sim\mathcal N(\sum a_i\mu_i,\sum a_i^2\sigma_i^2)$, d'où
  ⭐ **$\bar X\sim\mathcal N(\mu,\sigma^2/n)$, exactement**.
- **La stabilité est rare** : uniforme et exponentielle ne l'ont pas.
- ⚠️ **L'indépendance est indispensable** — ou, à défaut, la structure de **vecteur gaussien**.
  Des marges gaussiennes ne suffisent pas.

---

⬅️ [Module 7 — La loi normale et ses transformées](07-loi-normale-et-ses-transformees.md) ·
➡️ [Module 9 — Le vecteur gaussien](09-vecteur-gaussien.md) ·
🏠 [Sommaire](README.md)
