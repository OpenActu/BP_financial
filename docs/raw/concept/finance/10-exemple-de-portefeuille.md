# Module 10 — Un portefeuille complet, chiffré ⭐

**Durée : 1 h 30.** Prérequis : modules [1](01-le-cadre-cac40-et-le-srd.md) à
[9](09-contraintes-reelles-et-estimation.md).

> **La question traitée.** Aucune. Ce module n'établit rien de nouveau : il **exécute** les neuf
> précédents, dans l'ordre, sur un cas unique, et publie tous les nombres intermédiaires — comme
> l'[étape 9 de `modele.md`](../modele/09-exemple-complet.md) exécute les huit étapes de la
> démonstration sur onze points.

**L'énoncé.** Un investisseur dispose de **60 000 €**, d'un horizon de **20 ans**, d'un PEA et
d'un compte-titres donnant accès au SRD. Il veut détenir des actions du CAC 40. Combien de
lignes, lesquelles, en quelle proportion, avec quel levier, et faut-il couvrir ?

---

## 10.1 Les données de départ

Dix valeurs, un modèle à un facteur : $r_i=\alpha_i+\beta_i\,r_M+\varepsilon_i$, avec
$\sigma_M=20\,\%$, $r_f=3\,\%$, prime de risque $4{,}5\,\%$, coût de portage SRD $c=5\,\%$,
couverture espèces $m=20\,\%$.

| Ticker | Secteur | $\beta_i$ | $\sigma_{\varepsilon_i}$ | $\sigma_i$ | $\mu_i=r_f+\beta_i\times4{,}5\,\%$ |
|---|---|---|---|---|---|
| Airbus | Aéronautique | 1,05 | 22 % | 30,4 % | 7,72 % |
| MC.PA | Luxe | 1,15 | 20 % | 30,5 % | 8,17 % |
| OR.PA | Cosmétique | 0,85 | 16 % | 23,3 % | 6,83 % |
| SAN.PA | Pharmacie | 0,65 | 17 % | 21,4 % | 5,92 % |
| TTE.PA | Énergie | 0,95 | 19 % | 26,9 % | 7,27 % |
| BNP.PA | Banque | 1,35 | 21 % | 34,2 % | 9,07 % |
| SU.PA | Électrique | 1,10 | 18 % | 28,4 % | 7,95 % |
| VIE.PA | Services aux collectivités | 0,75 | 15 % | 21,2 % | 6,38 % |
| ORA.PA | Télécoms | 0,60 | 17 % | 20,8 % | 5,70 % |
| RI.PA | Spiritueux | 0,90 | 19 % | 26,2 % | 7,05 % |

$$\Sigma=\sigma_M^2\,\beta\beta^{\top}+\operatorname{diag}(\sigma^2_{\varepsilon})$$

Ce modèle **produit** la corrélation au lieu de la postuler : $\rho_{ij}=\beta_i\beta_j\sigma_M^2/(\sigma_i\sigma_j)$.

| Grandeur | Valeur |
|---|---|
| Corrélation moyenne $\bar\rho$ | **0,4927** (de 0,350 à 0,611) |
| Volatilité moyenne d'une ligne | 26,33 % |
| Plancher de diversification $\bar\sigma\sqrt{\bar\rho}$ | **18,48 %** |

> ⚠️ **Ces $\beta$ et ces $\sigma$ sont des ordres de grandeur plausibles, pas des mesures.**
> Aucun cours n'a été téléchargé pour les produire. La simulation
> [S10.1](#1010-simulation) montre comment les remplacer par les vôtres via
> `import_societe.py` ; le [§ 10.9](#109-réserves) dit ce qui change quand on le fait.
> Les $\mu_i$, eux, sont **construits** par le MEDAF — ce n'est pas une prévision, c'est une
> hypothèse de neutralité assumée, dont le § 10.4 montre l'effet radical.

---

## 10.2 Combien de lignes ? (module 9)

Volatilité d'un portefeuille équipondéré de $N$ lignes, **moyennée sur les
$\binom{10}{N}$ paniers possibles** :

| $N$ | $\sigma$ moyenne | Le meilleur panier | Le pire |
|---|---|---|---|
| 1 | 26,33 % | 20,81 % | 34,21 % |
| 2 | 22,84 % | 17,34 % | 28,90 % |
| 3 | 21,55 % | 16,34 % | 26,60 % |
| 5 | 20,45 % | 16,79 % | 24,13 % |
| 8 | 19,81 % | 18,27 % | 21,32 % |
| **10** | **19,60 %** | — | — |

> 🔑 **La colonne « meilleur panier » est plus instructive que la moyenne.** À $N=3$, le meilleur
> trio (16,34 %) fait mieux que les dix lignes réunies (19,60 %) — parce qu'il concentre les
> titres à faible $\beta$. La diversification naïve n'est donc pas la meilleure façon de réduire
> le risque : **choisir des $\beta$ faibles** en réduit davantage. Mais cela réduit aussi le
> rendement espéré, puisque $\mu_i$ croît avec $\beta_i$ — c'est le § 10.3.
>
> **Et l'écart entre le meilleur et le pire panier se referme avec $N$** : 8 points d'écart à
> $N=3$, 3 points à $N=8$. Au-delà de 8 lignes, le choix des titres cesse de gouverner le risque.

---

## 10.3 Quel portefeuille ? (module 8)

| Portefeuille | $E[R]$ | $\sigma$ | Sharpe | $\beta$ |
|---|---|---|---|---|
| Équipondéré $1/N$ | 7,21 % | 19,60 % | 0,215 | 0,93 |
| Variance minimale, $w\ge0$ | 6,10 % | **16,15 %** | 0,192 | 0,69 |
| Variance minimale, poids libres | 5,57 % | 15,42 % | 0,167 | 0,57 |
| Tangent (poids libres) | 7,28 % | 19,89 % | 0,215 | 0,95 |
| Pondéré par capitalisation¹ | 7,30 % | 20,08 % | 0,214 | 0,96 |
| **Indice CAC 40 (ETF)** | 7,50 % | 20,00 % | **0,225** | 1,00 |

*(¹ poids indiciels approximatifs de ces dix lignes, renormalisés à 100 % — voir le code du
§ 10.10)*

Poids de la variance minimale sous contrainte $w\ge0$ :

| ORA.PA | SAN.PA | VIE.PA | OR.PA | RI.PA | les 5 autres |
|---|---|---|---|---|---|
| 33,2 % | 28,4 % | 24,2 % | 10,6 % | 3,7 % | **0 %** |

**Trois résultats, dont deux désagréables.**

- ⭐ **L'indice bat les six constructions.** Ce n'est pas un accident numérique : le portefeuille
  de dix lignes porte un risque **spécifique** ($1-\rho^2=8{,}9\,\%$ de sa variance) que le MEDAF
  ne rémunère pas. Sous les hypothèses posées, **acheter un ETF CAC 40 domine toute sélection de
  dix titres** — et c'est la conclusion la plus solide de tout ce module, parce qu'elle ne dépend
  d'aucune prévision.
- **Le tangent n'a aucun poids négatif.** Il vaut presque exactement $1/N$. C'est logique : si les
  $\mu_i$ sont **construits** par le MEDAF, l'optimiseur n'a rien à exploiter, et le portefeuille
  optimal est le marché. Les poids négatifs spectaculaires du
  [§ 8.4](08-le-portefeuille-optimal.md) venaient d'un $\mu$ qui s'**écartait** du MEDAF.
- **La variance minimale abandonne la moitié de l'univers** et concentre 86 % du capital sur trois
  défensives. Elle réduit bien la volatilité (16,15 %), mais son Sharpe est inférieur : elle
  achète de la sécurité au prix du rendement, pas gratuitement.

### Ce qu'une seule opinion suffit à produire

Supposons que l'investisseur estime BNP.PA moins bien que le marché — **3 points** de rendement
espéré en moins, soit une vue modeste au regard de l'incertitude du
[§ 4.5](04-levier-optimal-et-drag.md) :

| | Poids BNP.PA | Poids maximal | Somme des poids négatifs | Sharpe |
|---|---|---|---|---|
| Aucune vue (MEDAF pur) | +0,11 | +0,12 | 0,00 | 0,215 |
| BNP à −3 points | **−0,36** | +0,19 | **−0,36** | 0,238 |

> ⭐ **Une vue de 3 points transforme un poids de +11 % en un poids de −36 %.** L'optimiseur
> répond à une variation d'entrée par une variation de sortie **quinze fois plus grande** : c'est
> le mécanisme, montré à nu, de l'échec constaté au [§ 9.2](09-contraintes-reelles-et-estimation.md).
> Et cette position vendeuse de 21 600 € coûterait 7 à 9 % de portage par an
> ([module 5](05-la-vente-a-decouvert.md)) — de quoi effacer le gain de Sharpe affiché.
>
> **Décision retenue : $1/N$ sur les dix lignes**, ou l'ETF si l'on accepte de renoncer au plaisir
> de choisir. La suite du module utilise $1/N$ ($\mu_p=7{,}21\,\%$, $\sigma_p=19{,}60\,\%$,
> $\beta_p=0{,}93$).

---

## 10.4 Quel levier ? (modules 3 et 4)

Ici, une précision que le [module 4](04-levier-optimal-et-drag.md) avait laissée de côté :
l'investisseur **prête** à $r_f=3\,\%$ et **emprunte** à $c=5\,\%$. Il y a donc deux formules,
chacune valide dans son domaine :

$$L^\star_{\text{prêt}}=\frac{\mu_p-r_f}{\sigma_p^2}=\frac{0{,}0721-0{,}03}{0{,}0384}=1{,}096\;(>1,\ \text{hors domaine}),$$
$$L^\star_{\text{emprunt}}=\frac{\mu_p-c}{\sigma_p^2}=\frac{0{,}0721-0{,}05}{0{,}0384}=0{,}575\;(<1,\ \text{hors domaine}).$$

> ⭐ **Les deux optima sont chacun hors de leur domaine de validité : l'optimum est donc le point
> anguleux $L=1$** — ni liquidités, ni emprunt. Le *spread* entre le taux prêteur et le taux
> emprunteur crée une **zone morte** où la réponse est « tout investi, rien emprunté ». Ce n'est
> pas une approximation de prudence : c'est le maximum exact de $g$.

| $L$ | $E[R]$ | $\sigma$ | $g(L)$ | $W_{20}/W_0$ |
|---|---|---|---|---|
| 0,00 | 3,00 % | 0,00 % | 3,00 % | 1,82 |
| 0,50 | 5,10 % | 9,80 % | 4,62 % | 2,52 |
| 0,75 | 6,16 % | 14,70 % | 5,08 % | 2,76 |
| **1,00** | **7,21 %** | **19,60 %** | **5,29 %** | **2,88** |
| 1,25 | 7,76 % | 24,49 % | 4,76 % | 2,59 |
| 1,50 | 8,31 % | 29,39 % | 3,99 % | 2,22 |
| 2,00 | 9,41 % | 39,19 % | 1,74 % | 1,41 |
| 2,50 | 10,52 % | 48,99 % | **−1,48 %** | 0,74 |

*(pour $L\le1$ la part non investie rapporte $r_f$ ; au-delà, la dette coûte $c$ — d'où la
cassure de pente en $L=1$)*

**Sensibilité au seul paramètre incertain, $\mu_p$ :**

| $\mu_p$ | $L^\star_{\text{prêt}}$ | $L^\star_{\text{emprunt}}$ | Décision |
|---|---|---|---|
| 5,21 % | 0,575 | 0,055 | $L=0{,}58$ — **42 % de liquidités** |
| 6,21 % | 0,836 | 0,315 | $L=0{,}84$ — 16 % de liquidités |
| **7,21 %** | 1,096 | 0,575 | **$L=1$** — point anguleux |
| 8,21 % | 1,356 | 0,836 | $L=1$ — point anguleux |
| 9,21 % | 1,617 | 1,096 | $L=1{,}10$ — emprunt marginal |
| 11,21 % | 2,137 | 1,617 | $L=1{,}62$ |

> 🔑 **Il faut croire à 9,2 % de rendement espéré pour que le SRD commence à se justifier**, et à
> plus de 11 % pour un levier significatif. Or l'IC à 95 % sur $\mu_p$, avec 20 ans de données,
> a une demi-largeur de l'ordre de **8 points** ([§ 4.5](04-levier-optimal-et-drag.md)) : la
> décision « lever ou non » n'est pas décidable par les données. Le point anguleux $L=1$ est le
> seul choix qui soit robuste à cette ignorance — et il est **gratuit**.

---

## 10.5 Quelle baisse faut-il pouvoir traverser ? (module 3)

Marché à $-30\,\%$, 60 000 € de fonds propres, couverture espèces ($m=20\,\%$) :

| $L$ | Exposition | Dette | Valeur après −30 % | Fonds propres | Perte | Appel de marge ? |
|---|---|---|---|---|---|---|
| 1,0 | 60 000 € | 0 € | 42 000 € | 42 000 € | −30 % | non |
| 1,5 | 90 000 € | 30 000 € | 63 000 € | 33 000 € | −45 % | non ($x^\star=58{,}3\,\%$) |
| 2,0 | 120 000 € | 60 000 € | 84 000 € | 24 000 € | −60 % | non ($x^\star=37{,}5\,\%$) |
| 2,5 | 150 000 € | 90 000 € | 105 000 € | 15 000 € | −75 % | **OUI** ($x^\star=25{,}0\,\%$) |

Et le critère inverse du [§ 3.5](03-marge-appel-de-marge-et-ruine.md) :

| Baisse à supporter | Levier maximal |
|---|---|
| 20 % | 2,78 |
| 30 % | 2,27 |
| 40 % | 1,92 |

> ⭐ **Les deux critères ne coïncident pas, et c'est le plus contraignant qui décide.** Le critère
> de survie autorise $L\le2{,}27$ pour traverser un $-30\,\%$ ; le critère de croissance impose
> $L=1$. **La contrainte qui mord n'est pas réglementaire, elle est arithmétique** : bien avant
> d'être liquidé, on a cessé de gagner quoi que ce soit à emprunter.

---

## 10.6 Faut-il couvrir ? (modules 6 et 7)

Le portefeuille $1/N$ a $\beta_p=0{,}935$ contre l'indice, donc

$$h^\star=\beta_p=0{,}935,\qquad \rho^2=\frac{\beta_p^2\sigma_M^2}{\sigma_p^2}=\mathbf{91{,}1\,\%},
\qquad \sigma_{\text{résiduelle}}=\sigma_p\sqrt{1-\rho^2}=\mathbf{5{,}86\,\%} .$$

**Combien de contrats**, avec le CAC 40 à 7 800 points :

| Instrument | Notionnel | $N$ exact | Choix réaliste | Exposition résiduelle |
|---|---|---|---|---|
| Contrat standard (10 €/pt) | 78 000 € | **0,72** | $N=1$ | **−21 900 € = −36,5 %** |
| Contrat de taille réduite (1 €/pt) | 7 800 € | 7,19 | $N=7$ | +1 500 € = **+2,5 %** |

> ⚠️ **Sur 60 000 €, le contrat standard est inutilisable** : un seul contrat sur-couvre le
> portefeuille de 36,5 %, c'est-à-dire crée une position vendeuse nette. La couverture
> « précise » du module 6 devient, à cette taille, une source de risque plus grande que celle
> qu'elle élimine.

**Ce qu'elle coûte, et l'alternative :**

| | Rendement espéré | Volatilité |
|---|---|---|
| Portefeuille nu | 7,21 % | 19,60 % |
| Couvert à $h^\star$ | **3,00 %** (≈ $r_f$, avant frais) | 5,86 % |
| **Vendre 70 % et garder 29,9 %** | **4,26 %** | 5,86 % |

> ⭐ **À risque strictement égal, vendre rapporte 1,26 point de plus que couvrir** — et ne coûte
> ni marge de variation, ni granularité, ni risque de base. Le coût annuel de la couverture,
> $\beta_p\times\text{prime}\times V=4{,}21\,\%$, soit **2 524 € par an**, est exactement la
> prime de risque qu'on renonce à percevoir ([§ 7.2](07-couvrir-en-pratique.md)).
>
> **Décision : ne pas couvrir.** La couverture ne redeviendrait rationnelle que si vendre était
> impossible ou coûteux — plus-values latentes lourdes en compte-titres, titres illiquides, ou
> événement daté à neutraliser sur quelques semaines.

---

## 10.7 Le résultat, sur 20 ans

| Choix | $\sigma$ | $g$ | $W_{20}$ (départ 60 000 €) |
|---|---|---|---|
| **$1/N$, $L=1$ (PEA ou CTO)** | 19,60 % | **5,29 %** | **172 752 €** |
| Variance minimale, $L=1$ | 16,15 % | 4,79 % | 156 425 € |
| $1/N$ à $L=1{,}5$ au SRD | 29,39 % | 3,99 % | **133 302 €** |

> 🔑 **Le levier 1,5 coûte 39 450 € sur vingt ans**, tout en multipliant la volatilité par 1,5 et
> en exposant à un appel de marge. Il n'achète strictement rien. C'est le
> [module 4](04-levier-optimal-et-drag.md) traduit en euros, et c'est la ligne la plus utile de ce
> cours.

---

## 10.8 La décision, en six lignes

| # | Question | Réponse chiffrée | Module |
|---|---|---|---|
| 1 | Combien de lignes ? | 8 à 10 ; au-delà, gain nul | [9](09-contraintes-reelles-et-estimation.md) |
| 2 | Lesquelles, en quelle proportion ? | $1/N$ — ou un ETF indiciel, qui fait mieux (Sharpe 0,225 contre 0,215) | [8](08-le-portefeuille-optimal.md) |
| 3 | Quel levier ? | $L=1$ : point anguleux entre 3 % prêteur et 5 % emprunteur | [4](04-levier-optimal-et-drag.md) |
| 4 | Quelle baisse traverser ? | −30 % coûte 30 % des fonds propres, sans appel de marge | [3](03-marge-appel-de-marge-et-ruine.md) |
| 5 | Couvrir ? | Non : vendre rapporte 1,26 pt de plus à risque égal | [6](06-la-couverture-optimale.md) |
| 6 | Avec quoi, si l'on couvrait ? | Contrats de taille réduite uniquement ($N=7$) ; le standard sur-couvre de 36 % | [7](07-couvrir-en-pratique.md) |

> ⭐ **Le cours entier converge vers une position très ordinaire** : dix lignes équipondérées ou un
> ETF, aucun levier, aucune couverture. Ce n'est pas un aveu d'inutilité — c'est le **résultat**.
> Les neuf modules précédents ne servent pas à trouver une position exotique, ils servent à
> **savoir pourquoi** l'ordinaire est optimal ici, et à reconnaître les cas — $\mu_p>9\,\%$,
> vente impossible, événement daté — où il cesse de l'être.

---

## 10.9 Réserves

**Réserve 1 — les $\mu_i$ sont construits, pas estimés.** Poser $\mu_i=r_f+\beta_i\times4{,}5\,\%$
revient à supposer le MEDAF exact, donc à **garantir** qu'aucune sélection ne batte l'indice : le
§ 10.3 ne démontre pas la supériorité de l'ETF, il la suppose. Ce que le module démontre, c'est
autre chose et c'est vrai indépendamment : le portefeuille de dix lignes porte 8,9 % de variance
spécifique, et il faut une **vue** pour espérer en être payé.

**Réserve 2 — un facteur, pas deux.** Un modèle à facteur unique impose $\rho_{ij}>0$ partout et
sous-estime la corrélation intra-sectorielle (les deux bancaires, les deux titres du luxe). La
diversification réelle du § 10.2 est donc **moins bonne** que celle affichée.

**Réserve 3 — les paramètres sont stationnaires ici, et ne le sont pas ailleurs.** $\beta_p$,
$\bar\rho$ et $\sigma_M$ sont traités comme des constantes. En crise, les trois montent ensemble
([§ 9.1](09-contraintes-reelles-et-estimation.md)) : le plancher de diversification remonte, le
$\beta$ dérive, et l'appel de marge du § 10.5 arrive plus tôt que la table ne l'annonce.

**Réserve 4 — la sensibilité est concentrée sur $\mu_p$.** Le § 10.4 le montre : un point de
rendement espéré en plus ou en moins déplace le levier optimal de 0,58 à 1,10. Toutes les autres
conclusions ($L\le1$, ne pas couvrir, 8 à 10 lignes) sont, elles, **stables** sur toute la plage
plausible — ce qui est la seule raison de les retenir.

**Réserve 5 — la fiscalité est absente.** Elle change au moins deux décisions : l'arbitrage
PEA/CTO (§ 10.7 les traite comme équivalents, ce qu'ils ne sont pas après impôt) et le choix
« couvrir plutôt que vendre » (§ 10.6), dont tout l'intérêt réel est de **ne pas déclencher** la
plus-value.

---

## 10.10 Simulation

### S10.1 — Le module entier, reproductible, et branchable sur vos données

```python
import numpy as np, math
from itertools import combinations

noms = ["AIR.PA","MC.PA","OR.PA","SAN.PA","TTE.PA","BNP.PA","SU.PA","VIE.PA","ORA.PA","RI.PA"]
beta = np.array([1.05, 1.15, 0.85, 0.65, 0.95, 1.35, 1.10, 0.75, 0.60, 0.90])
idio = np.array([0.22, 0.20, 0.16, 0.17, 0.19, 0.21, 0.18, 0.15, 0.17, 0.19])
sigM, rf, prime, c, m, V0 = 0.20, 0.03, 0.045, 0.05, 0.20, 60_000

n = len(noms)
mu = rf + beta * prime
S = np.outer(beta, beta) * sigM ** 2 + np.diag(idio ** 2)
sig = np.sqrt(np.diag(S))

def stats(w):
    e, v = w @ mu, w @ S @ w
    return e, math.sqrt(v), (e - rf) / math.sqrt(v), w @ beta

C = S / np.outer(sig, sig)
hd = C[~np.eye(n, dtype=bool)]
print(f"rho_bar={hd.mean():.4f}  plancher={sig.mean() * math.sqrt(hd.mean()):.2%}")

# 10.2 — diversification, moyenne sur TOUS les paniers de taille N
for N in (1, 2, 3, 5, 8, 10):
    v = [stats(np.array([1 / N if i in cb else 0 for i in range(n)]))[1]
         for cb in combinations(range(n), N)]
    print(f"N={N:>2}  moyenne={np.mean(v):.2%}  [{min(v):.2%} ; {max(v):.2%}]")

# 10.3 — les portefeuilles
inv = np.linalg.inv(S); un = np.ones(n)
w_eq = un / n
w_t = inv @ (mu - rf); w_t /= w_t.sum()

def simplexe(v):                       # projection euclidienne sur {w>=0, somme=1}
    u = np.sort(v)[::-1]; css = np.cumsum(u)
    r = np.nonzero(u * np.arange(1, len(v) + 1) > css - 1)[0][-1]
    return np.maximum(v - (css[r] - 1) / (r + 1), 0)

w_mv = un / n
for _ in range(200_000):               # gradient projete ; le probleme est convexe (convexite 6-7)
    w_mv = simplexe(w_mv - 0.5 * (2 * S @ w_mv))

w_mvl = inv @ un / (un @ inv @ un)                  # variance minimale, poids libres
w_cap = np.array([.06, .13, .12, .11, .10, .09, .08, .05, .05, .06]); w_cap /= w_cap.sum()

for nom, w in (("1/N", w_eq), ("var. min. w>=0", w_mv), ("var. min. libre", w_mvl),
               ("tangent", w_t), ("ponderee capi", w_cap)):
    e, s, sh, b = stats(w)
    print(f"{nom:<16}{e:>8.2%}{s:>8.2%}{sh:>8.3f}{b:>7.2f}")
print(f"{'indice':<16}{rf + prime:>8.2%}{sigM:>8.2%}{prime / sigM:>8.3f}{1.0:>7.2f}")
print("  poids var.min. :", "  ".join(f"{noms[i]}={w_mv[i]:.1%}" for i in np.argsort(-w_mv)))

# 10.3 bis — une vue de -3 points sur BNP
mu2 = mu.copy(); mu2[5] -= 0.03
w2 = inv @ (mu2 - rf); w2 /= w2.sum()
print(f"vue BNP -3pts -> poids BNP {w2[5]:+.2f} (contre {w_t[5]:+.2f} sans vue)")

# 10.4 — levier, deux taux
mp, sp, _, bp = stats(w_eq)
print(f"L*_pret={(mp - rf) / sp ** 2:.3f}   L*_emprunt={(mp - c) / sp ** 2:.3f}")
for L in (0, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5):
    t = rf if L <= 1 else c
    g = t + L * (mp - t) - L ** 2 * sp ** 2 / 2
    print(f"L={L:>4.2f}  E={t + L * (mp - t):>7.2%}  sigma={L * sp:>7.2%}  "
          f"g={g:>7.2%}  W20={V0 * math.exp(g * 20):>10,.0f}")

# 10.5 — stress
for L in (1, 1.5, 2, 2.5):
    eq = L * V0 * 0.70 - (L - 1) * V0
    print(f"L={L}: apres -30% -> {eq:>8,.0f} EUR ({eq / V0 - 1:+.0%})  "
          f"appel de marge : {'OUI' if 0.30 > (1 / L - m) / (1 - m) else 'non'}")

# 10.6 — couverture
rho2 = (bp * sigM) ** 2 / sp ** 2
sres = sp * math.sqrt(1 - rho2)
print(f"h*={bp:.3f}  rho2={rho2:.1%}  residuelle={sres:.2%}")
for mult in (10, 1):
    N = bp * V0 / (7800 * mult)
    k = round(N)
    print(f"  {mult:>2} EUR/pt : N={N:.2f} -> N={k}, residuel "
          f"{(bp * V0 - k * 7800 * mult) / V0:+.1%}")
print(f"couvert : E={rf:.2%} pour sigma={sres:.2%}  |  "
      f"vendre : E={rf + sres / sp * (mp - rf):.2%} pour la meme sigma")
print(f"cout annuel de la couverture = {bp * prime:.2%} = {bp * prime * V0:,.0f} EUR")

# 10.7 — les trois trajectoires a 20 ans
for nom, w, L in (("1/N, L=1", w_eq, 1.0), ("var. min., L=1", w_mv, 1.0), ("1/N, L=1,5", w_eq, 1.5)):
    e, sg, _, _ = stats(w)
    t = rf if L <= 1 else c
    g = t + L * (e - t) - L ** 2 * sg ** 2 / 2
    print(f"{nom:<16} sigma={L * sg:>7.2%}  g={g:>6.2%}  W20={V0 * math.exp(g * 20):>10,.0f} EUR")
```

> 💡 **Pour brancher vos propres données**, remplacez le bloc `beta`/`idio` par une régression des
> rendements de chaque ligne sur ceux du CAC 40 — c'est exactement le calcul de
> [`modele.md`](../../modele.md), et la simulation
> [S1.1](01-le-cadre-cac40-et-le-srd.md) en donne le code. Tout le reste du script est inchangé.

---

## 10.11 À retenir

- **La diversification sature à 8–10 lignes** ; au-delà, le choix des titres ne gouverne plus le
  risque. Et le meilleur trio bat les dix lignes réunies — en abaissant $\beta$, donc le
  rendement.
- ⭐ **Sous MEDAF, l'ETF indiciel domine toute sélection** : dix lignes portent 8,9 % de variance
  spécifique non rémunérée. Battre l'indice exige une **vue**, pas une méthode.
- ⭐ **Une vue de 3 points fait passer un poids de +11 % à −36 %.** L'optimiseur amplifie l'erreur
  d'un facteur 15 ; c'est l'échec du [§ 9.2](09-contraintes-reelles-et-estimation.md) rendu
  visible.
- ⭐ **Avec un taux prêteur de 3 % et un taux emprunteur de 5 %, l'optimum est le point anguleux
  $L=1$** — ni liquidités, ni SRD. Il faudrait croire à $\mu_p>9\,\%$ pour que lever commence à
  payer.
- **Le levier 1,5 coûte 39 450 € sur vingt ans** et n'achète rien. La contrainte qui mord est
  arithmétique, pas réglementaire.
- ⭐ **Couvrir rapporte 1,26 point de moins que vendre, à risque égal** — et sur 60 000 €, le
  contrat standard sur-couvre de 36,5 %.
- ⚠️ **Ce qui est fragile ici, c'est $\mu_p$, et lui seul.** Les conclusions « $L\le1$ », « ne pas
  couvrir », « 8 à 10 lignes » tiennent sur toute la plage plausible ; c'est pourquoi ce sont
  celles qu'on retient.

---

⬅️ [Module 9 — Contraintes réelles et estimation](09-contraintes-reelles-et-estimation.md) ·
🏠 [Sommaire](README.md) ·
📄 [`modele.md`](../../modele.md)
