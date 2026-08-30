# Module 5 — Inférence sur une moyenne

**Durée : 4 h.** Premier module d'application. Tout y découle du résultat du module 4 :
$$\frac{\bar X-\mu}{S/\sqrt n}\;\sim\;\mathcal T(n-1).$$

---

## 5.1 Intervalle de confiance

### Construction

La statistique est **pivotale** : sa loi ne dépend d'aucun paramètre inconnu. La construction qui
suit est **exactement** celle du [module 18 du cours de statistique](../../../semestre2/statistique/mathematique/18-intervalle-de-confiance.md), à deux
substitutions près — $S$ au lieu de $\sigma$, et $t_{n-1;\,1-\alpha/2}$ au lieu de $1{,}96$. On
écrit donc, pour tout $\mu$,

$$P\left(-t_{n-1;\,1-\alpha/2}\;\le\;\frac{\bar X-\mu}{S/\sqrt n}\;\le\;t_{n-1;\,1-\alpha/2}\right)=1-\alpha$$

puis **isoler $\mu$** au centre :

$$\boxed{\;\text{IC}_{1-\alpha}(\mu)=\left[\;\bar X - t_{n-1;\,1-\alpha/2}\frac{S}{\sqrt n}
\;;\;\bar X + t_{n-1;\,1-\alpha/2}\frac{S}{\sqrt n}\;\right]}$$

La demi-largeur $t_{n-1;\,1-\alpha/2}\frac{S}{\sqrt n}$ s'appelle la **marge d'erreur**.

### Trois lectures utiles

1. **Elle décroît en $1/\sqrt n$.** Diviser la marge par 2 exige de **quadrupler** l'effectif.
   C'est la loi d'airain de toute collecte de données.
2. **Elle est aléatoire deux fois** : par $\bar X$ (position) et par $S$ (largeur). Sur petit
   échantillon, deux échantillons peuvent produire des intervalles de largeurs très différentes.
3. **Le quantile de Student la gonfle** par rapport au cas$\sigma$ connu — d'un
  facteur$2{,}26/1{,}96 = 1{,}15$ à$n=10$, et$4{,}30/1{,}96=2{,}20$ à$n=3$.

### ⚠️ Interprétation — l'erreur la plus répandue en statistique

> **« Il y a 95 % de chances que $\mu$ soit dans cet intervalle » est FAUX.**

Dans le cadre fréquentiste, $\mu$ est une **constante inconnue**, pas une variable aléatoire :
une fois l'intervalle calculé, soit il contient $\mu$, soit il ne le contient pas. Il n'y a plus
aucune probabilité en jeu.

La formulation correcte porte sur la **procédure** : *si l'on répétait l'expérience un grand
nombre de fois, 95 % des intervalles ainsi construits contiendraient $\mu$.* Ce qui est aléatoire,
c'est l'intervalle — pas $\mu$.

**À vérifier par simulation** (§ 5.6, S5.1) : le taux de couverture doit valoir 95 % ; c'est la
seule justification opérationnelle de la formule.

---

## 5.2 Test de Student à une population

### Dispositif

| Élément | Contenu |
|---|---|
| Hypothèses | $H_0:\mu=\mu_0$ contre $H_1:\mu\ne\mu_0$ (bilatéral), $\mu>\mu_0$ ou $\mu<\mu_0$ (unilatéral) |
| Statistique | $\displaystyle t_{\text{obs}}=\frac{\bar x-\mu_0}{s/\sqrt n}$ |
| Loi sous $H_0$ | $\mathcal T(n-1)$ |
| Rejet (bilatéral) | $\lvertt_{\text{obs}}\rvert>t_{n-1;\,1-\alpha/2}$ |
| Rejet (unilatéral droit) | $t_{\text{obs}}>t_{n-1;\,1-\alpha}$ |
| $p$-valeur (bilatérale) | $p=2\,P\bigl(\mathcal T(n-1)>\lvertt_{\text{obs}}\rvert\bigr)$ |

### Dualité test / intervalle de confiance

> **Rejeter $H_0:\mu=\mu_0$ au risque $\alpha$ (bilatéral) $\iff$ $\mu_0\notin\text{IC}_{1-\alpha}(\mu)$.**

Ce n'est pas une coïncidence mais une **identité algébrique** : les deux expressions manipulent
la même inégalité. À vérifier une fois numériquement — cela clarifie durablement le lien entre
les deux objets.

> 🔑 **Conséquence pratique** : l'IC contient toute l'information du test, **et davantage**. Il
> donne le verdict (le $\mu_0$ testé est-il dedans ?) *et* l'ampleur *et* la précision. C'est
> pourquoi ce cours recommandera systématiquement de publier l'IC plutôt que la seule
> $p$-valeur.

### ⚠️ Quatre pièges sur la $p$-valeur

1. **Ce n'est pas $P(H_0 \mid \text{données})$.** C'est $P(\text{données au moins aussi extrêmes}\mid H_0)$
   — le conditionnement est en sens inverse.
2. **Ce n'est pas une mesure de l'ampleur de l'effet.** Un effet minuscule devient significatif
   avec $n$ assez grand ; un effet énorme reste non significatif si $n$ est petit.
3. **Un non-rejet n'est pas une preuve de $H_0$.** « Absence de preuve » ≠ « preuve d'absence ».
   Sans calcul de puissance, un non-rejet ne dit rien.
4. **Le seuil de 0,05 n'a aucun fondement théorique.** C'est une convention de Fisher, choisie
   pour la commodité des tables. Rien ne distingue $p=0{,}049$ de $p=0{,}051$.

---

## 5.3 Exemple travaillé — rendement mensuel d'un portefeuille

**Données.** 24 rendements mensuels ; moyenne $\bar x = +0{,}80\,\%$, écart-type
$s = 3{,}20\,\%$. Question : le rendement moyen est-il significativement différent de zéro ?

**Calcul.**

$$\text{SE}=\frac{s}{\sqrt n}=\frac{0{,}0320}{\sqrt{24}}=0{,}006532
\qquad
t_{\text{obs}}=\frac{0{,}0080}{0{,}006532}=1{,}2247$$

| Élément | Valeur |
|---|---|
| Degrés de liberté | $23$ |
| Valeur critique bilatérale à 5 % | $t_{23;\,0{,}975}=2{,}0687$ |
| **Décision** | $1{,}22 < 2{,}07$ → **on ne rejette pas $H_0$** |
| $p$-valeur | $0{,}233$ |
| $\text{IC}_{95\%}(\mu)$ | $[-0{,}55\,\% \;;\; +2{,}15\,\%]$ |

**Lecture — et ce qu'il ne faut pas en conclure.**

L'IC contient 0, cohérent avec le non-rejet (dualité du § 5.2). Mais il faut lire l'intervalle
**en entier** : il va de $-0{,}55\,\%$ à $+2{,}15\,\%$ par mois, soit, annualisé, d'environ
$-6\,\%$ à $+29\,\%$.

> ⚠️ **Conclure « ce portefeuille ne rapporte rien » serait une faute.** Les données sont
> compatibles avec une performance nulle, mais **tout autant** avec une performance annuelle de
> 25 %. Le test ne tranche pas : il constate que 24 mois ne suffisent pas à trancher.

**Combien faudrait-il d'observations ?** Pour détecter un effet de cette taille
($d=\bar x/s=0{,}25$) avec 80 % de puissance au risque de 5 %, il faut environ **128 mois**,
soit plus de **dix ans**. La puissance réelle à $n=24$ n'est que de **22 %** : dans 78 % des cas,
un tel test manquerait un effet pourtant réel.

> 🔑 **C'est le résultat le plus utile de ce module pour un usage financier.** La performance
> d'un fonds est une grandeur extraordinairement difficile à établir statistiquement, parce que
> le rapport signal/bruit des rendements est très faible. La plupart des « track records » de
> trois à cinq ans ne permettent, statistiquement, de conclure à rien.

---

## 5.4 Puissance et taille d'échantillon

### Définitions

| Notion | Sens |
|---|---|
| Risque de 1ʳᵉ espèce $\alpha$ | Rejeter $H_0$ alors qu'elle est vraie (**faux positif**) |
| Risque de 2ᵈᵉ espèce $\beta$ | Ne pas rejeter $H_0$ alors qu'elle est fausse (**faux négatif**) |
| **Puissance** $1-\beta$ | Probabilité de détecter un effet qui existe réellement |
| Taille d'effet | $d=\dfrac{\lvert\mu-\mu_0\rvert}{\sigma}$ (*d* de Cohen) |

### Loi sous $H_1$

Sous $H_1$, la statistique ne suit **plus** une loi de Student centrale mais une **loi de Student
décentrée** $\mathcal T(n-1,\,\delta)$, de paramètre de décentrage $\delta=d\sqrt n$.

$$1-\beta = P\bigl(|\mathcal T(n-1,\,\delta)| > t_{n-1;\,1-\alpha/2}\bigr)$$

### Formule approchée de dimensionnement

$$n \;\approx\; \frac{\bigl(z_{1-\alpha/2}+z_{1-\beta}\bigr)^2}{d^{\,2}}$$

Pour $\alpha=5\,\%$ et une puissance de 80 % : $n\approx\dfrac{(1{,}96+0{,}84)^2}{d^2}=\dfrac{7{,}85}{d^2}$.

| Taille d'effet $d$ | 0,20 (faible) | 0,25 | 0,50 (moyen) | 0,80 (fort) |
|---|---|---|---|---|
| $n$ approché (formule) | 196 | 126 | 31 | 12 |
| $n$ exact (Student décentrée) | 199 | 128 | 34 | 15 |

⚠️ L'approximation normale **sous-estime** systématiquement l'effectif nécessaire — d'autant plus
que $n$ est petit, c'est-à-dire précisément là où le dimensionnement compte le plus. Pour un
calcul exact, utiliser la loi décentrée (`scipy.stats.nct`).

> 🔑 **Le calcul de puissance se fait AVANT la collecte, jamais après.** La « puissance
> observée », calculée a posteriori sur l'effet estimé, est une quantité sans contenu
> informatif : elle est une fonction monotone de la $p$-valeur et ne dit rien de plus qu'elle.

---

## 5.5 Conditions d'application

| Condition | Rôle | Que faire si elle est violée |
|---|---|---|
| **Indépendance** des $X_i$ | **Critique** | Modéliser la dépendance, ou corriger l'effectif effectif (module 8) |
| **Normalité** | Faible impact dès $n\gtrsim 20$–30 (TCL) | Wilcoxon, bootstrap ; ou rien si $n$ est grand |
| Absence de valeurs aberrantes | Modéré à fort | Examiner, ne **pas** supprimer sans justification ; test robuste |
| Échantillonnage aléatoire | Critique pour la portée des conclusions | Aucun remède statistique |

⚠️ **Le classement usuel est trompeur.** On enseigne souvent la normalité comme *la* condition du
test de Student. En pratique, c'est **l'indépendance** qui casse presque toujours en premier, et
c'est elle qui fait le plus de dégâts. Le module 8 chiffre l'écart.

---

## 5.6 Simulations

### S5.1 — Le taux de couverture de l'IC

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(5)
MU, SIGMA, n, N = 12.0, 3.0, 9, 200_000

X = rng.normal(MU, SIGMA, size=(N, n))
xbar, s = X.mean(axis=1), X.std(axis=1, ddof=1)
demi_t = stats.t.ppf(0.975, n - 1) * s / np.sqrt(n)
demi_z = 1.96 * s / np.sqrt(n)              # erreur volontaire : quantile normal

print(f"couverture avec Student : {np.mean(np.abs(xbar-MU) <= demi_t):.4f}  (cible 0,95)")
print(f"couverture avec 1,96    : {np.mean(np.abs(xbar-MU) <= demi_z):.4f}  (trop faible !)")
print(f"largeur moyenne Student : {2*demi_t.mean():.3f}")
print(f"largeur : min={2*demi_t.min():.2f}  max={2*demi_t.max():.2f}  "
      "→ l'intervalle est aléatoire en LARGEUR aussi")
```

### S5.2 — Le niveau réel du test

```python
alpha, n = 0.05, 12
X = rng.normal(0, 1, size=(200_000, n))
t = X.mean(axis=1) / (X.std(axis=1, ddof=1) / np.sqrt(n))
print("niveau réel :", np.mean(np.abs(t) > stats.t.ppf(1 - alpha/2, n - 1)))   # ≈ 0,05
```

### S5.3 — Courbe de puissance

```python
import matplotlib.pyplot as plt

def puissance(n, d, alpha=0.05):
    """Puissance exacte du test bilatéral, via la loi de Student décentrée."""
    df, nc = n - 1, d * np.sqrt(n)
    tc = stats.t.ppf(1 - alpha / 2, df)
    return stats.nct.sf(tc, df, nc) + stats.nct.cdf(-tc, df, nc)

d = np.linspace(0, 1.5, 200)
for n in (5, 10, 24, 50, 128):
    plt.plot(d, [puissance(n, dd) for dd in d], label=f"n={n}")
plt.axhline(0.8, ls=":", c="k"); plt.axhline(0.05, ls=":", c="r")
plt.xlabel("taille d'effet d"); plt.ylabel("puissance"); plt.legend(); plt.show()

print("puissance de l'exemple du § 5.3 :", round(puissance(24, 0.25), 3))   # ≈ 0,22
```

### S5.4 — La violation qui compte : l'autocorrélation

```python
def ar1(n, phi, N, rng):
    """N trajectoires AR(1) centrées, de variance marginale 1."""
    e = rng.normal(0, np.sqrt(1 - phi**2), size=(N, n))
    x = np.empty((N, n)); x[:, 0] = rng.normal(0, 1, N)
    for i in range(1, n):
        x[:, i] = phi * x[:, i-1] + e[:, i]
    return x

n = 30
for phi in (0.0, 0.3, 0.6, 0.9):
    X = ar1(n, phi, 100_000, rng)          # espérance nulle : H0 est VRAIE
    t = X.mean(axis=1) / (X.std(axis=1, ddof=1) / np.sqrt(n))
    taux = np.mean(np.abs(t) > stats.t.ppf(0.975, n - 1))
    print(f"phi={phi:.1f} → niveau réel = {taux:.3f}   (nominal 0,050)")
```

**Résultat attendu** : le niveau réel grimpe très au-dessus de 5 % dès que $\varphi$ est
sensiblement positif. Le test devient **beaucoup trop permissif** — et aucune augmentation de $n$
n'y remédie. Gardez ce chiffre en tête : il est développé au module 8.

---

## 5.7 Exercices

**E5.1.** Refaire entièrement l'exemple du § 5.3 à la main, puis vérifier avec
`stats.ttest_1samp`. Reconstruire la $p$-valeur à partir de `stats.t.sf`.

**E5.2.** Vérifier numériquement la dualité test/IC : tirer un échantillon, balayer $\mu_0$ sur
une grille, et constater que l'ensemble des $\mu_0$ non rejetés à 5 % **coïncide exactement**
avec l'IC à 95 %.

**E5.3.** Un contrôle qualité impose un poids moyen de 500 g. Sur $n=16$ paquets :
$\bar x=496{,}2$ g, $s=7{,}4$ g. Tester $H_0:\mu=500$ au risque de 5 %, en bilatéral puis en
unilatéral gauche. Les conclusions diffèrent-elles ? Laquelle est légitime — et pourquoi le choix
doit-il être **fait avant** de voir les données ?

**E5.4.** Reprendre E5.3 et calculer la puissance du test bilatéral pour détecter un écart réel
de 4 g. Combien de paquets faudrait-il pour atteindre 90 % de puissance ?

**E5.5 — orientée finance.** Avec `import_societe.py`, extraire les rendements mensuels d'un
titre sur 5 ans ($n=60$). Tester $H_0$ : rendement moyen nul. Donner l'IC. Puis répondre : sur
combien d'années faudrait-il observer ce titre pour détecter une surperformance annuelle réelle
de 3 % ? *(L'ordre de grandeur obtenu — plusieurs décennies — est le vrai enseignement de
l'exercice.)*

**E5.6.** Sur ces mêmes rendements, calculer l'autocorrélation d'ordre 1. Est-elle assez forte
pour que le § 5.6/S5.4 s'applique ? Que devient votre confiance dans l'IC de E5.5 ?

---

## 5.8 À retenir

- $\text{IC}=\bar X \pm t_{n-1;\,1-\alpha/2}\frac{S}{\sqrt n}$ ; marge en $1/\sqrt n$ ;
  **l'aléa est dans l'intervalle, pas dans $\mu$**.
- Test et IC sont **duaux** : l'IC contient toute l'information du test, et l'ampleur en plus.
- La $p$-valeur n'est ni $P(H_0)$, ni une mesure d'effet, ni une preuve quand elle est grande.
- **Dimensionner avant de collecter.** La puissance a posteriori ne dit rien.
- L'hypothèse qui casse en premier n'est pas la normalité : c'est **l'indépendance**.

---

⬅️ [Module 4 — Construction et propriétés](04-construction-et-proprietes.md) ·
➡️ [Module 6 — Comparaison de deux moyennes](06-comparaison-de-deux-moyennes.md) ·
🏠 [Sommaire](README.md)
