# Module 13 — Portée et limites du TCL

**Durée : 1 h 30.** Prérequis : module [12](12-theoreme-central-limite.md).

> **La question traitée.** Le TCL est un énoncé **asymptotique**. Que garantit-il à $n$ fini ?
> Et sur quels terrains ne garantit-il rien du tout ?

**Ce qui est en jeu.** La règle « $n\ge 30$ » n'est pas un théorème. Ce module donne le vrai
critère — l'asymétrie en $\gamma_1/\sqrt n$ — et l'inventaire des cas où le TCL ne s'applique
pas.

---

## 13.1 Cinq malentendus

### ① Il ne dit rien pour un $n$ donné

Le TCL est un énoncé **asymptotique** : il porte sur une limite. Il n'affirme **rien** sur la
qualité de l'approximation à $n=30$, $n=100$ ou $n=10\,000$. C'est un théorème d'existence de
limite, pas une garantie chiffrée — voir
[§ 12.5 ④](12-theoreme-central-limite.md) pour la raison technique.

### ② « $n\ge 30$ » n'est pas un théorème

C'est une **règle empirique**, sans fondement mathématique, et souvent fausse. Le $n$ nécessaire
dépend de l'**asymétrie** de la loi : le tableau du § 13.2 montre qu'à $n=30$, la moyenne d'une
loi log-normale est encore franchement dissymétrique.

À l'inverse, pour une loi symétrique et bornée comme l'uniforme, $n=5$ suffit largement.

### ③ Il ne dit rien sur la vitesse — sauf par un autre théorème

La vitesse relève de l'inégalité de **Berry–Esseen** (§ 13.3), qui est un résultat distinct et
qui exige une hypothèse de plus.

### ④ Il exige une variance finie

Sur une loi de **Cauchy**, la moyenne de $n$ tirages suit… une loi de Cauchy, **identique quel
que soit $n$**. Moyenner n'apporte strictement rien : ni loi des grands nombres, ni TCL. (Le
calcul tient en une ligne : exercice E6.3.)

Plus généralement, pour une loi $\alpha$-stable avec $\alpha<2$, la normalisation correcte est
$n^{1/\alpha}$ et non $\sqrt n$, et la limite est une loi stable, pas une gaussienne. Ce n'est pas
une curiosité théorique : certains modèles de rendements extrêmes et de sinistres relèvent de ce
cas.

### ⑤ Il ne vaut pas dans les queues extrêmes

Le TCL contrôle la convergence des probabilités $P(Z_n\le x)$ pour $x$ **fixé**. Il ne dit rien
des événements dont la probabilité tend vers 0 avec $n$ — le domaine des **grandes déviations**.

Conséquence pratique majeure : approcher $P(Z_n > 5)$ par la queue gaussienne peut être faux de
plusieurs **ordres de grandeur**. C'est exactement l'erreur commise dans les modèles de risque
financier qui calculent une VaR à 99,9 % en supposant la normalité.

> ⚠️ Le sixième malentendu — l'indépendance — est assez grave pour occuper le
> [module 14](14-dependance-et-echec-du-tcl.md) entier.

---

## 13.2 La qualité de l'approximation : ce qu'on observe vraiment

Simulation : couverture réelle de l'intervalle nominal à 95 % construit sur l'approximation
normale ($\sigma$ supposé connu), pour diverses lois. 500 000 réplications.

> ℹ️ Le script du § 13.4 n'en fait que 200 000, pour rester rapide : les écarts avec ce tableau
> se situent dans la **troisième décimale** et ne changent aucune des lectures ci-dessous.

| Loi | $n$ | Couverture bilatérale | Queue **gauche** (cible 2,5 %) | Queue **droite** (cible 2,5 %) | Asymétrie de $\bar X$ |
|---|---|---|---|---|---|
| **Normale** | 5 | 0,9504 | 0,0248 | 0,0247 | 0 |
| | 30 | 0,9498 | 0,0250 | 0,0252 | 0 |
| **Uniforme** | 5 | 0,9529 | 0,0235 | 0,0236 | 0 |
| | 30 | 0,9502 | 0,0248 | 0,0249 | 0 |
| **Exponentielle** | 5 | 0,9561 | **0,0004** | **0,0435** | 0,894 |
| | 30 | 0,9520 | 0,0139 | 0,0341 | 0,365 |
| | 100 | 0,9502 | 0,0193 | 0,0306 | 0,200 |
| | 1000 | 0,9503 | 0,0233 | 0,0264 | 0,063 |
| **Log-normale** | 5 | 0,9568 | **0,0000** | **0,0432** | 2,766 |
| | 30 | 0,9565 | 0,0026 | 0,0409 | 1,129 |
| | 100 | 0,9533 | 0,0098 | 0,0369 | 0,618 |
| | 1000 | 0,9507 | 0,0196 | 0,0297 | 0,196 |
| **Bernoulli 5 %** | 5 | 0,9773 | 0,0000 | 0,0227 | 1,847 |
| | 30 | **0,9394** | 0,0000 | **0,0606** | 0,754 |
| | 100 | 0,9660 | 0,0061 | 0,0279 | 0,413 |
| | 1000 | 0,9506 | 0,0211 | 0,0283 | 0,131 |

### Trois enseignements, dont un contre-intuitif

**① La couverture bilatérale est trompeuse.** À $n=5$ sur une loi exponentielle, elle vaut
0,9561 — apparemment excellente. Mais les deux queues valent **0,04 %** et **4,35 %** : les
erreurs, de sens opposés, **se compensent**. L'intervalle est presque entièrement décalé d'un
côté, et le résumé bilatéral le masque complètement.

> 🔑 **Conséquence directe : un test unilatéral est bien plus exposé qu'un test bilatéral.**
> Sur cette loi à $n=5$, un test unilatéral droit annoncé à 2,5 % opère en réalité à 4,35 %,
> soit un risque **multiplié par 17** dans l'autre sens. Toujours contrôler les **deux queues
> séparément**, jamais la seule couverture globale.

**② La quantité qui gouverne tout est l'asymétrie de $\bar X$**, et elle obéit à une règle simple :

$$\boxed{\;\gamma_1(\bar X_n)=\frac{\gamma_1(X)}{\sqrt n}\;}$$

C'est cette formule — et non « $n\ge 30$ » — qu'il faut retenir pour juger si l'approximation
tient. Elle sort directement du calcul des cumulants du
[§ 12.4](12-theoreme-central-limite.md). À qualité d'approximation égale, l'effectif requis est
proportionnel à $\gamma_1^2$ : la log-normale ($\gamma_1=6{,}18$) exige donc environ
$\left(\frac{6{,}18}{2}\right)^2\approx \mathbf{10}$ **fois plus d'observations** que
l'exponentielle ($\gamma_1=2$).

Le tableau le confirme directement : l'exponentielle atteint $\gamma_1(\bar X)=0{,}200$ à
$n=100$, la log-normale $0{,}196$ à $n=1000$ — un facteur 10, exactement.

**③ La convergence n'est pas monotone pour les lois discrètes.** Regardez la Bernoulli 5 % :
0,9773 à $n=5$, puis **0,9394** à $n=30$, puis 0,9660 à $n=100$. La couverture oscille au lieu de
s'améliorer régulièrement. C'est un effet de **discrétisation** : le support de $\sum X_i$ est
constitué d'entiers, et les sauts de la fonction de répartition tombent tantôt d'un côté, tantôt
de l'autre de la valeur critique. Ne jamais conclure « ça converge » en observant deux valeurs
de $n$.

---

## 13.3 La vitesse de convergence : Berry–Esseen

> **Inégalité de Berry–Esseen.** Si $\rho=E|X-\mu|^3<\infty$, alors pour tout $n$ :
> $$\sup_{x\in\mathbb R}\bigl|F_n(x)-\Phi(x)\bigr|\;\le\;\frac{C\,\rho}{\sigma^3\sqrt n},
> \qquad C\le 0{,}4748 \;\text{(Shevtsova, 2011)}$$

Trois lectures :

- **La vitesse est en $1/\sqrt n$**, comme la marge d'erreur d'un intervalle de confiance
  ([§ 18.3](18-intervalle-de-confiance.md)). Diviser l'erreur d'approximation par 2 coûte
  $\times 4$ en effectif.
- **La borne est universelle mais très lâche.** Pour une loi exponentielle,
  $\rho=E|X-1|^3=2{,}4146$, donc à $n=30$ la borne vaut $0{,}209$ — alors que l'écart réel n'est
  que de **0,025**, huit fois moindre. La borne garantit ; elle ne prédit pas.
- **Elle exige un moment d'ordre 3.** Sur une loi à queue lourde sans moment d'ordre 3, le TCL
  peut valoir sans que Berry–Esseen s'applique, et la convergence est alors plus lente.

**Le raffinement utile en pratique** est le **développement d'Edgeworth**, dont le premier terme
fait apparaître explicitement l'asymétrie :

$$F_n(x)\;\approx\;\Phi(x)-\frac{\gamma_1}{6\sqrt n}\,(x^2-1)\,\varphi(x)$$

C'est la justification théorique de la règle du § 13.2 : le terme d'erreur dominant est
proportionnel à $\gamma_1/\sqrt n$, c'est-à-dire à l'asymétrie de $\bar X_n$. Notez que ce terme
correctif est **antisymétrique** en $x$ — ce qui explique pourquoi les deux queues se
compensent et pourquoi la couverture bilatérale paraît bonne alors que chaque queue est fausse.

---

## 13.4 Simulations

### S13.1 — Reproduire le tableau du § 13.2

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(11)
z = stats.norm.ppf(0.975)
E = np.e
lois = {
    "normale":       (lambda s: rng.normal(0, 1, s),            0.0,           1.0,                   0.0),
    "uniforme":      (lambda s: rng.uniform(-1, 1, s),          0.0,           1/np.sqrt(3),          0.0),
    "exponentielle": (lambda s: rng.exponential(1, s),          1.0,           1.0,                   2.0),
    "log-normale":   (lambda s: rng.lognormal(0, 1, s),         np.sqrt(E),    np.sqrt(E**2 - E),     (E+2)*np.sqrt(E-1)),
    "Bernoulli 5%":  (lambda s: (rng.random(s) < .05) * 1.0,    .05,           np.sqrt(.0475),        .9/np.sqrt(.0475)),
}
print(f"{'loi':<15}{'n':>6}{'bilat':>9}{'queue G':>9}{'queue D':>9}{'skew(Xb)':>10}")
for nom, (g, MU, SG, sk) in lois.items():
    for n in (5, 30, 100, 1000):
        Z = (g((200_000, n)).mean(axis=1) - MU) / (SG / np.sqrt(n))
        print(f"{nom if n == 5 else '':<15}{n:>6}{np.mean(np.abs(Z) <= z):>9.4f}"
              f"{np.mean(Z < -z):>9.4f}{np.mean(Z > z):>9.4f}{sk/np.sqrt(n):>10.3f}")
    print()
```

⚠️ **Regardez les colonnes de queues, pas la couverture bilatérale.** C'est là que se voit le
problème.

### S13.2 — La loi de Cauchy : ni LGN, ni TCL

```python
rng_c = np.random.default_rng(3)

def moyennes_cauchy(n, N, bloc=2_000_000):
    """N moyennes de n tirages de Cauchy, calculées par blocs pour tenir en mémoire."""
    par_bloc, res, reste = max(1, bloc // n), [], N
    while reste > 0:
        k = min(par_bloc, reste)
        res.append(rng_c.standard_cauchy((k, n)).mean(axis=1))
        reste -= k
    return np.concatenate(res)

for n, N in [(1, 20_000), (10, 20_000), (100, 20_000), (10_000, 5_000), (1_000_000, 500)]:
    C = moyennes_cauchy(n, N)
    print(f"n={n:>9,} : quartiles de la moyenne = "
          f"{np.percentile(C, 25):+8.3f} {np.percentile(C, 50):+8.3f} {np.percentile(C, 75):+8.3f}")
```

La dispersion **ne diminue pas** : la moyenne d'un million de Cauchy est aussi dispersée qu'un
seul tirage. Moyenner n'apporte rien. Comparez avec la même boucle sur une loi normale, où
l'écart interquartile est divisé par $\sqrt n$.

### S13.3 — Berry–Esseen, borne contre réalité

```python
from scipy import integrate
rho = integrate.quad(lambda x: abs(x - 1)**3 * np.exp(-x), 0, 60)[0]
print(f"exponentielle : rho = {rho:.4f}")
for n in (5, 30, 100, 1000):
    X = rng.exponential(1.0, size=(200_000, n))
    Z = (X.mean(axis=1) - 1) / (1 / np.sqrt(n))
    grille = np.linspace(-4, 4, 801)
    reel = max(abs(np.mean(Z <= t) - stats.norm.cdf(t)) for t in grille)
    print(f"  n={n:>5} : borne={0.4748*rho/np.sqrt(n):.4f}   réel={reel:.4f}")
```

La borne est vraie partout et **huit fois trop grande** partout. C'est le prix d'un résultat
universel.

---

## 13.5 Extensions (culture, non exigibles)

| Extension | Ce qu'elle relâche | Idée |
|---|---|---|
| **Lindeberg–Feller** | La même loi | Les $X_i$ peuvent avoir des lois différentes, si aucune ne domine les autres (condition de Lindeberg) |
| **Condition de Lyapunov** | Idem | Version plus simple à vérifier : $\sum E\lvertX_i-\mu_i\rvert^{2+\delta}$ négligeable |
| **TCL multivarié** | La dimension 1 | $\sqrt n(\bar{\mathbf X}-\boldsymbol\mu)\to\mathcal N_p(0,\Sigma)$ ; c'est lui qui fonde la régression multiple |
| **Méthode delta** | La linéarité | Si $\sqrt n(\hat\theta-\theta)\to\mathcal N(0,\sigma^2)$ et $g$ est dérivable, alors $\sqrt n\bigl(g(\hat\theta)-g(\theta)\bigr)\to\mathcal N\bigl(0,g'(\theta)^2\sigma^2\bigr)$ |
| **Donsker** | Le passage à la limite ponctuel | Convergence de la **trajectoire** vers un mouvement brownien — voir [module 14](14-dependance-et-echec-du-tcl.md) |
| **TCL généralisé** | La variance finie | Limite $\alpha$-stable, normalisation en $n^{1/\alpha}$ |

> 🔑 La **méthode delta** mérite une mention particulière : c'est elle qui permet d'étendre le TCL
> à des grandeurs qui ne sont pas des moyennes — un ratio, un logarithme de rendement, un
> coefficient de corrélation. Elle explique pourquoi l'approximation normale se retrouve
> absolument partout en statistique appliquée.

---

## 13.6 Exercices

**E13.1.** Une loi a une asymétrie de 3. Quel $n$ faut-il pour que l'asymétrie de $\bar X$ tombe
sous 0,2 ? Comparer à la règle « $n\ge 30$ ». *(Réponse : $n\ge 225$.)*

**E13.2.** Sur une loi exponentielle à $n=5$, un test **unilatéral droit** annoncé à 2,5 % opère
en réalité à 4,35 % (§ 13.2). Un test **unilatéral gauche** annoncé à 2,5 % opère à 0,04 %.
Lequel des deux est le plus grave, et pourquoi la réponse dépend-elle de ce qu'on cherche à
démontrer ?

**E13.3.** Calculer $\gamma_1$ pour une loi exponentielle et pour une log-normale
$\mathcal{LN}(0,1)$. *Vérifier le facteur 10 annoncé au § 13.2 ②.*

**E13.4.** Pourquoi la borne de Berry–Esseen ne s'applique-t-elle pas à une loi de Pareto
d'exposant 2,5 ? *Le TCL, lui, s'applique-t-il ?*

**E13.5.** Expliquer, à partir du terme d'Edgeworth du § 13.3, pourquoi les deux queues sont
fausses de sens opposés. *(Piste : $(x^2-1)\varphi(x)$ est paire, mais le terme complet change de
signe avec le sens de l'inégalité.)*

**E13.6 — orientée finance.** Sur les rendements quotidiens d'un titre :
1. estimer $\gamma_1$ et en déduire le $n$ nécessaire pour que $\gamma_1(\bar X)<0{,}1$ ;
2. comparer à la durée correspondante en séances de bourse ;
3. refaire le calcul sur les rendements **hebdomadaires**. *Que constatez-vous, et pourquoi ?*

---

## 13.7 À retenir

- **« $n\ge 30$ » n'est pas un théorème.** Le bon critère est
  $\gamma_1(\bar X_n)=\gamma_1(X)/\sqrt n$ — et l'effectif requis croît en $\gamma_1^2$.
- **Contrôler les deux queues séparément** : la couverture bilatérale masque des erreurs
  compensées, et un test unilatéral est bien plus exposé.
- **Lois discrètes** : la convergence n'est pas monotone. Ne jamais conclure sur deux valeurs
  de $n$.
- **Berry–Esseen** donne la vitesse $1/\sqrt n$, au prix d'un moment d'ordre 3 — et sa borne est
  universelle mais très lâche. **Edgeworth** explique la compensation des queues.
- **Pas de variance finie, pas de TCL** (Cauchy). **Pas de garantie dans les queues extrêmes**
  non plus.

---

⬅️ [Module 12 — Le théorème central limite](12-theoreme-central-limite.md) ·
➡️ [Module 14 — Dépendance et échec du TCL](14-dependance-et-echec-du-tcl.md) ·
🏠 [Sommaire](README.md)
