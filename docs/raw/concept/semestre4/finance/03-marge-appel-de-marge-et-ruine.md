# Module 3 — Marge, appel de marge et ruine ⭐

**Durée : 1 h 15.** Prérequis : modules [1](01-le-cadre-cac40-et-le-srd.md) et [2](02-l-effet-de-levier.md). Utile : [loi normale](../../semestre2/statistique/mathematique/06f-loi-normale.md).

> **La question traitée.** Le module 2 s'est terminé sur un constat gênant : sans appel de marge,
> le levier n'introduit **aucune** asymétrie de récupération. L'appel de marge est donc le vrai
> sujet. Que fait-il, exactement, au risque d'une position ?

**Réponse en une phrase.** Il transforme une fonction **affine** du prix final en une fonction
**du chemin suivi** — et cette transformation ne se voit presque pas dans l'espérance, alors
qu'elle démolit la médiane.

---

## 3.1 La condition de couverture

Position d'exposition $E$, fonds propres $C$, taux de couverture exigé $m$ ([§ 1.3](01-le-cadre-cac40-et-le-srd.md) : $m=20\,\%$ en espèces, 25 % en obligations, 40 % en actions). Le courtier exige à tout instant

$$\frac{C}{E}\;\ge\;m .$$

Partant de $C_0=E_0/L$, après une baisse de $x$ :

$$C=E_0\Bigl(\frac1L-x\Bigr),\qquad E=E_0(1-x),\qquad
\frac{C}{E}=\frac{\frac1L-x}{1-x}\;\ge\;m .$$

D'où le **seuil d'appel de marge** :

$$\boxed{\;x^\star=\frac{\frac1L-m}{1-m}\;}$$

| $L$ | $m=20\,\%$ (espèces) | $m=25\,\%$ (obligations) | $m=40\,\%$ (actions) |
| --- | -------------------- | ------------------------ | -------------------- |
| 1,5 | 58,33 %              | 55,56 %                  | 44,44 %              |
| 2   | 37,50 %              | 33,33 %                  | 16,67 %              |
| 2,5 | 25,00 %              | 20,00 %                  | **immédiat**         |
| 3   | 16,67 %              | 11,11 %                  | immédiat             |
| 4   | 6,25 %               | immédiat                 | immédiat             |
| 5   | **immédiat**         | immédiat                 | immédiat             |

> ⚠️ **Le levier maximal autorisé est le levier dont le seuil d'appel est nul.** $L_{\max}=1/m$
> est le levier pour lequel **la première baisse, si petite soit-elle, déclenche l'appel**.
> Utiliser le levier maximal du SRD, ce n'est pas prendre « beaucoup » de risque : c'est ouvrir
> une position déjà en défaut. Le seul levier qui laisse respirer est **strictement** inférieur.

---

## 3.2 Quelle probabilité de le toucher ?

Modélisons le prix par un mouvement brownien géométrique de rendement $\mu$ et de volatilité
$\sigma$ ; $X_t=\log S_t/S_0$ est un brownien de dérive $\nu=\mu-\sigma^2/2$. Pour une barrière
$a=\log(1-x^\star)<0$, la loi du minimum donne

$$\boxed{\;P\bigl(\min_{t\le T}X_t\le a\bigr)
=\Phi\!\left(\frac{a-\nu T}{\sigma\sqrt T}\right)
+e^{2\nu a/\sigma^{2}}\,\Phi\!\left(\frac{a+\nu T}{\sigma\sqrt T}\right)\;}$$

Avec $\mu=7\,\%$, $T=1$ an, couverture espèces ($m=20\,\%$) :

| $L$ | Seuil $x^\star$ | Baisse à franchir | $P(\text{appel} <1\text{ an})$, $\sigma=20\,\%$ (indice) | $\sigma=30\,\%$ (ligne unique) |
| --- | --------------- | ----------------- | -------------------------------------------------------- | ------------------------------ |
| 2   | 37,50 %         | 47,00 %           | 1,0 %                                                    | 10,3 %                         |
| 2,5 | 25,00 %         | 28,77 %           | 10,3 %                                                   | 31,1 %                         |
| 3   | 16,67 %         | 18,23 %           | **28,4 %**                                               | **51,6 %**                     |
| 4   | 6,25 %          | 6,45 %            | 68,4 %                                                   | 81,4 %                         |

*(« baisse à franchir » = $-a$ en log, toujours supérieure à $x^\star$ en pourcentage)*

> 🔑 **Le chiffre à retenir est celui de la dernière colonne.** Une ligne du CAC 40 à levier 3 sur
> un an : **plus d'une chance sur deux** de subir un appel de marge. Le même levier sur l'indice :
> une chance sur quatre. La différence n'est pas dans le levier — il est identique — mais dans la
> volatilité, et c'est déjà tout l'argument du [module 8](08-le-portefeuille-optimal.md) : la diversification est ce qui rend le levier tenable.

⚠️ **Cette formule suppose un brownien : trajectoire continue, volatilité constante, pas de saut.**
Les trois hypothèses sont fausses aux moments qui comptent — un *gap* d'ouverture franchit la
barrière sans la toucher, la volatilité explose en crise, et les queues sont plus épaisses que
gaussiennes ([§ 13](../../semestre2/statistique/mathematique/13-portee-et-limites-du-tcl.md) et[§ 14](../../semestre2/statistique/mathematique/14-dependance-et-echec-du-tcl.md)). Les probabilités ci-dessus sont donc des **planchers**.

---

## 3.3 Ce que l'appel de marge coûte vraiment

Deux réponses possibles à l'appel : **apporter** des fonds (augmenter $C$) ou **liquider** (réduire $E$). La seconde est celle qui s'impose quand on n'a plus de liquidités — c'est-à-dire exactement dans le scénario où l'on est déjà en perte.

Simulation, 200 000 trajectoires journalières, $\mu=7\,\%$, $c=5\,\%$, $m=20\,\%$, un an :

| $L$ | $P(\text{appel})$ | $E[R_L]$ **sans** barrière | $E[R_L]$ **avec** liquidation | **Médiane** avec | $P(R_L<0)$ |
| --- | ----------------- | -------------------------- | ----------------------------- | ---------------- | ---------- |
| 2   | 0,9 %             | +9,62 %                    | +9,62 %                       | +5,35 %          | 44,9 %     |
| 2,5 | 9,5 %             | +10,77 %                   | +10,72 %                      | +5,33 %          | 46,0 %     |
| 3   | 26,6 %            | +11,92 %                   | +11,39 %                      | +2,25 %          | 48,8 %     |
| 4   | 65,1 %            | +14,23 %                   | +10,32 %                      | **−26,01 %**     | 68,6 %     |

*(σ = 20 % ; les $P(\text{appel})$ mesurées, à surveillance journalière, sont légèrement inférieures aux valeurs continues du § 3.2 — une barrière n'est franchie qu'aux instants où on la regarde.)*

**Trois lectures, dont une contre-intuitive.**

- **L'espérance ne voit presque rien.** À $L=3$, la liquidation forcée ne coûte que 0,53 point d'espérance. Si l'on ne regarde que $E[R_L]$, le levier 4 paraît encore le meilleur des quatre.
- **La médiane, elle, s'effondre** : +5,35 % à $L=2$, −26,01 % à $L=4$. L'espérance est portée par une queue droite de plus en plus mince et de plus en plus haute — c'est exactement le
  phénomène que le [module 4](04-levier-optimal-et-drag.md) va formaliser.
- ⭐ **Plus de la moitié des liquidations sont des erreurs *ex post*.** Parmi les trajectoires qui
  touchent le seuil à $L=3$, **53,8 %** terminent l'année **au-dessus** de ce seuil. La position aurait survécu ; c'est la contrainte, pas le marché, qui l'a tuée.

> 🔑 **L'appel de marge détruit la propriété centrale du [§ 2.5](02-l-effet-de-levier.md) :** le droit d'attendre. Sans lui, le rendement ne dépend que du prix final ; avec lui, il dépend du **minimum atteint en chemin**. Deux trajectoires de même point d'arrivée n'ont plus le même résultat.

---

## 3.4 La spirale, et pourquoi elle est un mécanisme et non une malchance

Quatre effets se composent, tous dans le même sens :

| Effet                               | Mécanisme                                                                             | Où c'est démontré                                                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Le levier monte quand ça baisse** | $L'=L\frac{1-x}{1-Lx}$                                                                | [§ 2.4](02-l-effet-de-levier.md)                                                                                             |
| **Le seuil se rapproche**           | $x^\star$ décroît en $L$ ; à levier dérivé, le seuil suivant est plus proche          | § 3.1                                                                                                                        |
| **Le courtier relève $m$**          | Les exigences de couverture montent avec la volatilité réalisée                       | [§ 1.3](01-le-cadre-cac40-et-le-srd.md)                                                                                      |
| **Les corrélations montent**        | En crise, $\bar\rho\to1$ : le collatéral actions baisse en même temps que la position | [§ 9.1](09-contraintes-reelles-et-estimation.md), [§ 14 stat.](../../semestre2/statistique/mathematique/14-dependance-et-echec-du-tcl.md) |

⚠️ **Le cas le plus dangereux du SRD est la couverture en actions** ($m=40\,\%$). Le collatéral et
la position sont alors le *même* facteur de risque : une baisse de marché réduit simultanément le
numérateur et le dénominateur de la contrainte. C'est un levier caché, qui s'ajoute au levier déclaré.

> **Rapprochement utile.** Une position à barrière a un profil de gain **concave** en le prix
> (plafonnée en bas par la liquidation, tronquée dans les scénarios de reprise). Le
> [module 8 du cours de convexité](../../semestre1/analyse/convexite/08-convexite-et-mesures-de-risque.md)  explique pourquoi une mesure de risque comme la VaR, qui ne regarde qu'un quantile, ne capture rien de ce phénomène : ce qui se passe **au-delà** du seuil est précisément ce qui compte ici.

---

## 3.5 Dimensionner une position pour survivre

Renversons le problème : au lieu de subir $x^\star$, **choisissons-le**. Si l'on veut supporter
une baisse de $d$ sans appel de marge, le levier maximal admissible est

$$\boxed{\;L\;\le\;\frac{1}{m+(1-m)\,d}\;}$$

| Baisse $d$ à supporter | $m=20\,\%$ | $m=40\,\%$ |
| ---------------------- | ---------- | ---------- |
| 10 %                   | 3,57       | 2,17       |
| 20 %                   | 2,78       | 1,92       |
| 30 %                   | 2,27       | 1,72       |
| 50 %                   | 1,67       | 1,43       |

*(inverse exact de la formule du § 3.1 ; se vérifie en une ligne)*

> ⭐ **C'est la seule façon correcte de choisir un levier à ce stade du cours.** Non pas « quel
> rendement je vise » mais « quelle baisse je dois pouvoir traverser sans être liquidé ». Le
> [module 4](04-levier-optimal-et-drag.md) donnera l'autre critère — la croissance à long terme — et les deux convergeront vers des valeurs étonnamment proches, toutes deux bien en dessous des plafonds réglementaires.

---

## 3.6 Simulation

### S3.1 — Barrière, espérance, médiane

```python
import numpy as np, math

rng = np.random.default_rng(1)
mu, sig, c, m, T, n, B = 0.07, 0.20, 0.05, 0.20, 1.0, 252, 200_000
dt = T / n

seuil = lambda L: (1 / L - m) / (1 - m)

Z = rng.standard_normal((B, n))
S = np.exp(np.cumsum((mu - sig ** 2 / 2) * dt + sig * math.sqrt(dt) * Z, axis=1))
mini = np.minimum.accumulate(S, axis=1)

print(f"{'L':>5}{'seuil':>9}{'P(appel)':>10}{'E sans':>9}{'E avec':>9}{'mediane':>10}{'P(perte)':>10}")
for L in (2, 2.5, 3, 4):
    x, bar = seuil(L), 1 - seuil(L)
    touche = mini[:, -1] <= bar
    R0 = L * (S[:, -1] - 1) - (L - 1) * c                 # sans appel de marge
    frac = np.where(touche, np.argmax(S <= bar, axis=1) / n, 1.0)
    R1 = np.where(touche, -L * x - (L - 1) * c * frac, R0)  # liquidation au seuil
    print(f"{L:>5}{x:>9.2%}{touche.mean():>10.1%}{R0.mean():>+9.2%}{R1.mean():>+9.2%}"
          f"{np.median(R1):>+10.2%}{(R1 < 0).mean():>10.1%}")
    if touche.any():
        print(f"      -> liquidees qui finissent AU-DESSUS du seuil : "
              f"{(S[touche, -1] > bar).mean():.1%}")

# formule analytique du paragraphe 3.2, a comparer
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
nu = mu - sig ** 2 / 2
for L in (2, 2.5, 3, 4):
    a = math.log(1 - seuil(L))
    p = Phi((a - nu * T) / (sig * math.sqrt(T))) + math.exp(2 * nu * a / sig ** 2) * Phi(
        (a + nu * T) / (sig * math.sqrt(T)))
    print(f"L={L:<4} P analytique (continu) = {p:.1%}")
```

Sortie attendue : la table du § 3.3, une part de liquidations « inutiles » supérieure à 50 %, et
des probabilités analytiques **au-dessus** des probabilités simulées — l'écart entre surveillance
continue et surveillance journalière.

---

## 3.7 Exercices

**E3.1.** Démontrer $x^\star=\frac{1/L-m}{1-m}$ et vérifier qu'il s'annule en $L=1/m$. *Que vaut
$x^\star$ pour $L>1/m$, et qu'est-ce que cela signifie ?*

**E3.2.** Inverser la relation pour obtenir $L\le\frac{1}{m+(1-m)d}$ du § 3.5, et retrouver la
table.

**E3.3.** Reprendre la simulation avec un $m$ qui passe de 20 % à 30 % dès que la volatilité
réalisée sur 20 séances dépasse 30 % annualisés. *De combien la probabilité d'appel augmente-t-elle ?*

**E3.4.** Ajouter des sauts : remplacer 1 % des rendements journaliers par un choc de $-7\,\%$.
*Comparer la probabilité d'appel à celle du brownien pur. Le brownien sous-estime-t-il beaucoup ?*

**E3.5.** Un investisseur couvre sa position SRD avec des actions du CAC 40 ($m=40\,\%$) dont le
$\beta$ vaut 1. Écrire la contrainte de couverture en tenant compte du fait que **le collatéral
baisse aussi**. *Quel est le levier effectif ?*

**E3.6.** Sur 20 ans de données du CAC 40, compter les épisodes de baisse supérieure à 18,23 %
depuis un plus haut (le seuil de $L=3$). *Comparer la fréquence empirique à la probabilité
brownienne du § 3.2.*

---

## 3.8 À retenir

- **Le seuil d'appel est $x^\star=\frac{1/L-m}{1-m}$** — et il vaut **zéro** au levier maximal
  autorisé. Le plafond réglementaire n'est pas un objectif, c'est une frontière de défaut.
- ⭐ **À levier 3 sur une ligne du CAC 40, un appel de marge dans l'année est plus probable
  qu'improbable** (≈ 52 %). Sur l'indice, ≈ 28 %. La volatilité, pas le levier, fait la
  différence.
- ⭐ **L'appel de marge se voit à peine dans l'espérance et démolit la médiane.** À $L=4$ :
  espérance +10,3 %, médiane −26,0 %. Juger un levier sur son rendement moyen est une erreur de
  statistique, pas d'optimisme.
- ⭐ **Plus de la moitié des liquidations sont démenties par la suite** : le titre finit au-dessus
  du seuil. La contrainte a détruit la position, pas le marché.
- **La barrière rend le résultat dépendant du chemin.** Toutes les formules affines du module 2
  cessent de valoir.
- **Dimensionner par la baisse tolérée** : $L\le\frac{1}{m+(1-m)d}$. Supporter −30 % avec une
  couverture espèces, c'est $L\le2{,}27$.
- ⚠️ **La couverture en actions est un levier caché** : collatéral et position partagent le même
  facteur de risque.

---

⬅️ [Module 2 — L'effet de levier](02-l-effet-de-levier.md) ·
➡️ [Module 4 — Levier optimal et drag de volatilité](04-levier-optimal-et-drag.md) ·
🏠 [Sommaire](README.md)
