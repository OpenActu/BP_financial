# Module 9 — Contraintes réelles, erreur d'estimation, et synthèse ⭐

**Durée : 1 h 15.** Prérequis : modules [4](04-levier-optimal-et-drag.md), [6](06-la-couverture-optimale.md) et [8](08-le-portefeuille-optimal.md).

> **La question traitée.** Le module 8 a donné des formules exactes. Elles supposent $\mu$ et
> $\Sigma$ **connus**. Ils ne le sont pas — et le [§ 4.5](04-levier-optimal-et-drag.md) a déjà montré à quel point $\mu$ est insaisissable. Que devient l'optimisation quand ses entrées sont du bruit, et que reste-t-il de la diversification sur un univers de 40 valeurs corrélées ?

---

## 9.1 Le plancher de diversification

Prenons $N$ titres de même volatilité $\sigma$, équipondérés, de corrélation moyenne $\bar\rho$ :

$$\operatorname{Var}(r_{1/N})=\frac{\sigma^2}{N}+\Bigl(1-\frac1N\Bigr)\bar\rho\,\sigma^2
\;\Longrightarrow\;
\boxed{\;\sigma_{1/N}=\sigma\sqrt{\bar\rho+\frac{1-\bar\rho}{N}}\;\xrightarrow[N\to\infty]{}\;\sigma\sqrt{\bar\rho}\;}$$

Avec $\sigma=28\,\%$ et $\bar\rho=0{,}45$ (ordres de grandeur pour la cote parisienne) :

| $N$      | $\sigma$ du portefeuille | Écart au plancher |
| -------- | ------------------------ | ----------------- |
| 1        | 28,00 %                  | +49,1 %           |
| 2        | 23,84 %                  | +26,9 %           |
| 3        | 22,28 %                  | +18,6 %           |
| 5        | 20,95 %                  | +11,6 %           |
| **10**   | **19,90 %**              | **+5,9 %**        |
| 20       | 19,35 %                  | +3,0 %            |
| 40       | 19,07 %                  | +1,5 %            |
| $\infty$ | **18,78 %**              | —                 |

> ⭐ **Deux conclusions, l'une rassurante et l'autre non.**
>
> **10 à 15 lignes suffisent.** Passer de 10 à 40 titres ne gagne que 0,8 point de volatilité, pour quatre fois plus de lignes à suivre et à arbitrer. L'essentiel de la diversification est acquis très vite — c'est la décroissance en $1/N$ du premier terme.
>
> **Mais le plancher est haut.** Aucune sélection de valeurs du CAC 40, si nombreuse soit-elle, ne
> descend sous ≈ 19 % de volatilité annuelle. Le risque commun ne se diversifie pas : il ne peut
> être que **couvert** ([module 6](06-la-couverture-optimale.md)) ou **dilué** par une part en liquidités ([module 4](04-levier-optimal-et-drag.md), où $L<1$). Ceux qui espèrent réduire le risque en ajoutant des titres du même marché cherchent au mauvais endroit.

⚠️ **Et $\bar\rho$ n'est pas une constante.** En crise, les corrélations convergent vers 1 ([§ 14 du cours de statistique](../../semestre2/statistique/mathematique/14-dependance-et-echec-du-tcl.md)) : le plancher $\sigma\sqrt{\bar\rho}$ remonte vers $\sigma$ au moment précis où l'on comptait dessus. La diversification est une protection **qui s'évapore dans le sinistre** — contrairement à une couverture par future, qui, elle, se renforce.

---

## 9.2 L'erreur d'estimation détruit l'optimisation

Simulation honnête : 10 actifs, $\sigma=28\,\%$, $\bar\rho=0{,}45$, rendements espérés vrais échelonnés de 4 % à 12 %. On **estime** $\hat\mu$ et $\hat\Sigma$ sur 60 mois, on calcule le tangent estimé, et on évalue son Sharpe **vrai**. 4 000 réplications.

| Stratégie                                         | Sharpe réel obtenu |
| ------------------------------------------------- | ------------------ |
| Portefeuille tangent **vrai** (paramètres connus) | **0,463**          |
| Portefeuille tangent **estimé** sur 5 ans         | **0,106**          |
| Équipondéré $1/N$                                 | **0,251**          |
| Proportion de tirages où $1/N$ bat Markowitz      | **81,3 %**         |

> ⭐ **L'optimisation détruit les trois quarts de ce qu'elle promet, et fait deux fois pire que ne
> rien faire.** Ce n'est pas un artefact de simulation : c'est le résultat classique de la littérature (DeMiguel, Garlappi & Uppal, 2009), et il tient à trois causes cumulées :
>
> 1. $\hat\mu$ est du bruit — $\operatorname{SE}=\sigma/\sqrt T$, soit **12,5 %** ici pour des écarts vrais de 8 points ([§ 4.5](04-levier-optimal-et-drag.md)) ;
> 2. $\Sigma^{-1}$ **amplifie** l'erreur : les directions de faible variance, les plus mal estimées, sont celles que l'inverse pondère le plus ;
> 3. l'optimiseur est un **maximiseur d'erreur** — il surpondère par construction les actifs dont
>    le rendement a été surestimé et la variance sous-estimée.

**Le comptage des paramètres explique le reste.** Estimer $\Sigma$ sur $n$ actifs demande $\frac{n(n+1)}2$ nombres : **55** pour 10 actifs, **820** pour les 40 du CAC 40. Avec 60 rendements mensuels, on estime 820 paramètres à partir de 2 400 observations dépendantes. La matrice obtenue est numériquement inversible et statistiquement vide.

---

## 9.3 Les remèdes, par ordre d'efficacité

| Remède                                                       | Mécanisme                                                                                                        | Effet                                                          |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Renoncer à $\mu$** — utiliser $w_{\text{mv}}$              | La variance minimale n'utilise que $\Sigma$, mieux estimée que $\mu$                                             | Le plus rentable des remèdes                                   |
| **Contraindre $w\ge0$**                                      | Interdit les poids extrêmes que produit le bruit                                                                 | Équivaut à un *shrinkage* de $\Sigma$ (Jagannathan & Ma, 2003) |
| **Rétrécir $\Sigma$ (*shrinkage*)**                          | $\hat\Sigma_{\text{shrunk}}=\lambda\,\Sigma_{\text{cible}}+(1-\lambda)\hat\Sigma$, cible = corrélation constante | Stabilise l'inverse                                            |
| **Réduire $n$**                                              | 10 lignes bien choisies plutôt que 40                                                                            | Moins de paramètres, cf. § 9.1                                 |
| **Partir de $1/N$** et n'en dévier qu'avec de bonnes raisons | Aucun paramètre estimé                                                                                           | Difficile à battre                                             |

> 🔑 **La contrainte du PEA est aussi une protection.** Le [§ 8.5](08-le-portefeuille-optimal.md) a chiffré à 18,8 % de Sharpe le coût de l'interdiction de vendre à découvert **quand les paramètres sont connus**. Quand ils sont estimés, cette même contrainte **ajoute** de la performance en bloquant les positions aberrantes. Le coût réel de l'interdiction est donc nettement inférieur à 18,8 %, et peut être négatif.

---

## 9.4 Synthèse du cours : la chaîne de décision

| #   | Décision                  | Outil                                                                        | Résultat sur le cadre parisien                        |
| --- | ------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1   | **Quels titres**          | $1/N$ sur 10–15 lignes, ou $w_{\text{mv}}$ rétréci — pas le tangent estimé   | § 9.2, § 9.3                                          |
| 2   | **Combien de lignes**     | Plancher $\sigma\sqrt{\bar\rho}$ : au-delà de 15, gain marginal nul          | § 9.1                                                 |
| 3   | **Quelle échelle**        | $L^\star=\frac{\mu-c}{\sigma^2}$, appliqué **de moitié**                     | [§ 4.3](04-levier-optimal-et-drag.md) — souvent $L<1$ |
| 4   | **Quelle baisse tolérer** | $L\le\frac1{m+(1-m)d}$                                                       | [§ 3.5](03-marge-appel-de-marge-et-ruine.md)          |
| 5   | **Couvrir ?**             | $h^\star=\beta$, efficacité $\rho^2$ — et seulement si vendre est impossible | [§ 6.4](06-la-couverture-optimale.md)                 |
| 6   | **Avec quoi**             | Future si le montant le permet ; ETF inverse en PEA, tactique seulement      | [§ 7.7](07-couvrir-en-pratique.md)                    |

> 📄 **Cette chaîne est exécutée de bout en bout, avec tous les nombres, au
> [module 10](10-exemple-de-portefeuille.md)** : 60 000 €, dix valeurs du CAC 40, et les six
> décisions prises l'une après l'autre.

**Les trois décisions 3, 4 et 5 convergent** vers la même conclusion arithmétique : sur des actions
parisiennes, financées à 5 % ou plus, le levier profitable est **inférieur à 1**, et la protection la plus efficace n'est ni la couverture ni la diversification, mais la **part non investie**.

> ⭐ **Ce qui reste vrai quand tout le reste change.** Trois résultats de ce cours ne dépendent
> d'aucune estimation, d'aucun paramètre de marché, d'aucune réglementation :
>
> - le gain d'un levier est **linéaire** et son drag **quadratique** ($\Rightarrow$ un optimum existe, et le dépasser est pire que de rester en liquidités) ;
> - $h^\star=\operatorname{Cov}/\operatorname{Var}$ et il subsiste $1-\rho^2$ de variance ($\Rightarrow$ [`modele.md`](../../../modele.md)) ;
> - se tromper par excès coûte le **carré** de ce que coûte se tromper par défaut ($\Rightarrow$ viser en dessous, toujours).
>
> Tout le reste — les taux de couverture, le coût du SRD, la liste du SRD, $\bar\rho$, $\beta$ — est un paramètre qui bougera.

---

## 9.5 Simulation

### S9.1 — Le plancher, et Markowitz contre $1/N$

```python
import numpy as np, math

# --- plancher de diversification
s, rb = 0.28, 0.45
for N in (1, 2, 3, 5, 10, 20, 40):
    print(f"N={N:>3}  sigma={math.sqrt(s ** 2 * (rb + (1 - rb) / N)):.2%}")
print(f"plancher = {s * math.sqrt(rb):.2%}")

# --- erreur d'estimation
rng = np.random.default_rng(0)
K, T, B = 10, 60, 4000
sigs = np.full(K, 0.28 / math.sqrt(12))
Ctrue = np.full((K, K), 0.45); np.fill_diagonal(Ctrue, 1.0)
Strue = np.outer(sigs, sigs) * Ctrue
mus = np.linspace(0.04, 0.12, K) / 12
rf = 0.03 / 12
L = np.linalg.cholesky(Strue)

sharpe = lambda w: (w @ mus - rf) / math.sqrt(w @ Strue @ w) * math.sqrt(12)

w_vrai = np.linalg.solve(Strue, mus - rf); w_vrai /= w_vrai.sum()
mk, eq = [], []
for _ in range(B):
    X = mus + rng.standard_normal((T, K)) @ L.T          # 60 mois observes
    wh = np.linalg.solve(np.cov(X, rowvar=False), X.mean(0) - rf)
    wh /= wh.sum()
    mk.append(sharpe(wh)); eq.append(sharpe(np.ones(K) / K))

mk, eq = np.array(mk), np.array(eq)
print(f"\ntangent vrai   : {sharpe(w_vrai):.3f}")
print(f"tangent estime : {mk.mean():.3f}")
print(f"1/N            : {eq.mean():.3f}")
print(f"1/N gagne dans {(eq > mk).mean():.1%} des tirages")
```

Sortie attendue : le plancher à 18,78 %, et un tangent estimé (0,106) **deux fois moins bon** que
l'équipondéré (0,251), lui-même deux fois moins bon que le tangent vrai (0,463).

---

## 9.6 Exercices

**E9.1.** Démontrer $\sigma_{1/N}=\sigma\sqrt{\bar\rho+(1-\bar\rho)/N}$ et en déduire le nombre de lignes nécessaire pour être à moins de 5 % du plancher. *Le résultat dépend-il de $\sigma$ ?*

**E9.2.** Sur les données du script, estimer $\bar\rho$ sur le CAC 40 en périodes calmes et en périodes de forte volatilité. *De combien le plancher remonte-t-il en crise ?*

**E9.3.** Refaire la simulation du § 9.2 avec $T=120$ et $T=240$ mois. *Combien d'années faudrait-il pour que le tangent estimé batte $1/N$ ?*

**E9.4.** Ajouter la contrainte $w\ge0$ dans la simulation. *De combien le Sharpe réalisé s'améliore-t-il ? Retrouve-t-on l'effet de shrinkage annoncé au § 9.3 ?*

**E9.5.** Comparer $w_{\text{mv}}$ estimé et $w_{\text{tan}}$ estimé sur les mêmes tirages. *Lequel résiste le mieux, et pourquoi était-ce prévisible ?*

**E9.6.** Construire, sur données réelles, le portefeuille des six premières décisions du § 9.4
et le suivre sur 3 ans. *Comparer au CAC 40 GR, en volatilité réalisée et en perte maximale.*

---

## 9.7 À retenir

- ⭐ **Le plancher de diversification est $\sigma\sqrt{\bar\rho}$** — ≈ 19 % sur la cote
  parisienne. Dix à quinze lignes en capturent l'essentiel ; les vingt-cinq suivantes n'ajoutent
  rien.
- **Le risque commun ne se diversifie pas.** Il se couvre (module 6) ou se dilue en liquidités
  (module 4). Ajouter des titres du même marché ne l'atteint pas.
- ⚠️ **$\bar\rho$ monte en crise**, donc la diversification s'affaiblit exactement quand elle
  sert. La couverture, elle, ne s'affaiblit pas.
- ⭐ **Markowitz estimé fait deux fois pire que $1/N$**, et perd dans 81 % des tirages. Le tangent
  est un maximiseur d'erreur, et $\Sigma^{-1}$ amplifie le bruit.
- **Remèdes, par ordre d'efficacité** : renoncer à $\mu$ (variance minimale), contraindre
  $w\ge0$, rétrécir $\Sigma$, réduire $n$, partir de $1/N$.
- 🔑 **La contrainte long-only du PEA coûte moins qu'elle ne paraît** — 18,8 % de Sharpe en
  théorie, souvent rien en pratique, car elle bloque les positions que le bruit engendre.
- ⭐ **La conclusion pratique du cours entier** : sur des actions parisiennes financées à 5 % ou
  plus, le levier optimal est inférieur à 1, la couverture permanente est une vente déguisée, et
  ce qui protège le mieux est la part qu'on n'a pas investie.

---

⬅️ [Module 8 — Le portefeuille optimal](08-le-portefeuille-optimal.md) ·
➡️ [Module 10 — Un portefeuille complet, chiffré](10-exemple-de-portefeuille.md) ·
🏠 [Sommaire](README.md) ·
📄 [`modele.md`](../../../modele.md) ·
📘 [Cours de statistique](../../semestre2/statistique/mathematique/README.md)
