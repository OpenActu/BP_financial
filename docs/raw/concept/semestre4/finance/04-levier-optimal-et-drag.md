# Module 4 — Levier optimal et drag de volatilité ⭐

**Durée : 1 h 15.** Prérequis : modules [2](02-l-effet-de-levier.md) et
[3](03-marge-appel-de-marge-et-ruine.md), et
[Jensen probabiliste](../../semestre1/analyse/convexite/05-jensen-probabiliste.md).

> **La question traitée.** Le module 2 a montré que l'espérance de rendement **croît linéairement**
> avec le levier : $E[R_L]=L(E[R]-c)+c$. Si c'était le dernier mot, il faudrait toujours prendre
> le levier maximal. Le module 3 a montré que la médiane, elle, s'effondre. Quel est le levier qui
> maximise ce que l'on touche **réellement** ?

---

## 4.1 Deux critères qui ne disent pas la même chose

Un capital qui subit des rendements successifs se **multiplie** ; il ne s'additionne pas :

$$W_T=W_0\prod_{i=1}^{T}(1+R_i).$$

Ce qui gouverne le résultat à long terme n'est donc pas $E[R]$ mais $E[\log(1+R)]$, le **taux de
croissance logarithmique**. Or $\log$ est **concave**, donc ([Jensen](../../semestre1/analyse/convexite/05-jensen-probabiliste.md)) :

$$E\bigl[\log(1+R)\bigr]\;\le\;\log\bigl(1+E[R]\bigr).$$

> 🔑 **Cet écart a un nom : le *drag* de volatilité.** Il n'est pas une friction, un coût de
> transaction ou une imperfection de marché : c'est une **inégalité mathématique**, et elle est de
> signe constant. Le [module 5 du cours de convexité](../../semestre1/analyse/convexite/05-jensen-probabiliste.md)
> la démontre ; ce module la paie.

En modélisation continue (rendement instantané $\mu$, volatilité $\sigma$) :

$$\boxed{\;g\;=\;E\Bigl[\tfrac{d\log W}{dt}\Bigr]\;=\;\mu-\frac{\sigma^2}{2}\;}$$

Un actif à $\mu=8\,\%$ et $\sigma=20\,\%$ ne compose donc pas à 8 % mais à **6 %**. Deux points
par an, perdus sans qu'aucune contrepartie ne les encaisse.

---

## 4.2 La croissance d'une position levée

Avec $dW/W = L\,dS/S-(L-1)c\,dt$ et $dS/S=\mu\,dt+\sigma\,dB$, la position levée a pour dérive
$L\mu-(L-1)c$ et pour volatilité $L\sigma$. En appliquant la formule précédente :

$$\boxed{\;g(L)\;=\;\underbrace{c}_{\text{si }L=0}\;+\;\underbrace{L(\mu-c)}_{\text{prime empruntée}}\;-\;\underbrace{\frac{L^2\sigma^2}{2}}_{\text{drag, quadratique}}\;}$$

⚠️ **L'asymétrie des exposants est tout le module** : le gain est **linéaire** en $L$, le drag est
**quadratique**. Doubler le levier double la prime et **quadruple** la pénalité. Il existe donc
un maximum, et il est unique — $g$ est une parabole concave, cas d'école du
[module 6 de convexité](../../semestre1/analyse/convexite/06-minimisation-convexe.md).

---

## 4.3 Le levier optimal

$$g'(L)=(\mu-c)-L\sigma^2=0\;\Longrightarrow\;
\boxed{\;L^\star=\frac{\mu-c}{\sigma^{2}}\;},\qquad
g(L^\star)=c+\frac{(\mu-c)^2}{2\sigma^{2}} .$$

C'est le critère de Kelly, sous sa forme continue (Merton). Quatre jeux de paramètres :

| $\mu$ | $\sigma$ | $c$ | $L^\star$ | $g(L^\star)$ | Zone de destruction $L>2L^\star$ |
|---|---|---|---|---|---|
| 8 % | 20 % | **5 %** (SRD) | **0,75** | 6,13 % | $L>1{,}50$ |
| 8 % | 20 % | 0 % (sans dette) | 2,00 | 8,00 % | $L>4{,}00$ |
| 8 % | 30 % | 5 % | 0,33 | 5,50 % | $L>0{,}67$ |
| 12 % | 20 % | 5 % | 1,75 | 11,13 % | $L>3{,}50$ |

> ⚠️ **Un seul taux ici, deux dans la vraie vie.** $g(L)$ suppose qu'on **prête** et qu'on
> **emprunte** au même taux $c$. En pratique la part non investie rapporte $r_f$ (3 %) et la dette
> coûte $c$ (5 %) : il y a alors **deux** formules, $L^\star=\frac{\mu-r_f}{\sigma^2}$ en dessous
> de 1 et $L^\star=\frac{\mu-c}{\sigma^2}$ au-dessus, et il arrive que **ni l'une ni l'autre ne
> tombe dans son domaine** : l'optimum est alors le point anguleux $L=1$. Le
> [§ 10.4](10-exemple-de-portefeuille.md) montre que c'est le cas le plus fréquent en pratique.

> ⭐ **Le résultat central pour un particulier au SRD.** Avec des paramètres réalistes pour le
> CAC 40 — $\mu=8\,\%$, $\sigma=20\,\%$ — et un coût de portage de 5 %, le levier optimal vaut
> **0,75**. Autrement dit : non seulement il ne faut pas emprunter, mais il faudrait détenir un
> quart du portefeuille en liquidités. Le levier profitable n'apparaît que si $\mu-c$ est
> nettement positif, c'est-à-dire si l'on gagne **le pari sur la prime de risque nette du coût du
> crédit** — et $c$ est ici cinq à huit fois le taux sans risque des manuels.

---

## 4.4 La table complète, et l'illusion de l'espérance

$\mu=8\,\%$, $\sigma=20\,\%$, $c=5\,\%$, horizon 20 ans, capital initial 100 :

| $L$ | $E[R_L]$ | Volatilité | $g(L)$ | **Médiane** $W_{20}$ | $E[W_{20}]$ |
|---|---|---|---|---|---|
| 0,00 | 5,00 % | 0 % | 5,00 % | 271,8 | 271,8 |
| 0,50 | 6,50 % | 10 % | 6,00 % | 332,0 | 366,9 |
| **0,75** | 7,25 % | 15 % | **6,13 %** | **340,4** | 426,3 |
| 1,00 | 8,00 % | 20 % | 6,00 % | 332,0 | 495,3 |
| 1,50 | 9,50 % | 30 % | 5,00 % | 271,8 | 668,6 |
| 2,00 | 11,00 % | 40 % | 3,00 % | 182,2 | 902,5 |
| 3,00 | 14,00 % | 60 % | −4,00 % | 44,9 | 1 644,5 |
| 4,00 | 17,00 % | 80 % | −15,00 % | **5,0** | 2 996,4 |

**Trois faits dans cette table.**

- **Les deux dernières colonnes vont en sens opposés.** $E[W_{20}]$ est croissante en $L$ —
  jusqu'à 3 000 à levier 4 — pendant que la médiane tombe à **5**. L'espérance est portée par des
  trajectoires de probabilité infime et de gain colossal ; l'investisseur médian, lui, est ruiné.
- ⭐ **$g(2L^\star)=g(0)=c$**, et la parabole est symétrique : à levier $1{,}5$ ici, on obtient
  **exactement** ce qu'on aurait eu en restant en liquidités, en ayant supporté 30 % de
  volatilité. Au-delà, on paie pour perdre.
- **À $L=3$, la croissance est négative** : la position converge vers zéro presque sûrement,
  alors même que $E[R_L]=14\,\%$. C'est le paradoxe le plus coûteux de la finance de particulier.

> ⚠️ **Et ce tableau ignore l'appel de marge.** Le [module 3](03-marge-appel-de-marge-et-ruine.md)
> montre que les colonnes de droite sont encore optimistes : à $L\ge3$, la position est liquidée
> bien avant d'avoir eu le temps de converger vers zéro.

---

## 4.5 Pourquoi viser en dessous : $L^\star$ n'est pas connu

$L^\star=(\mu-c)/\sigma^2$ suppose $\mu$ **connu**. Or $\mu$ est le paramètre le plus mal estimé
de toute la finance : sur $T$ années, $\operatorname{SE}(\hat\mu)=\sigma/\sqrt T$
([§ 18 du cours de statistique](../../semestre2/statistique/mathematique/18-intervalle-de-confiance.md)).

| Historique | $\operatorname{SE}(\hat\mu)$ | IC 95 % sur $L^\star$ (pour $\hat L^\star=0{,}75$) |
|---|---|---|
| 5 ans | 8,94 % | $[-3{,}63\;;\;+5{,}13]$ |
| 10 ans | 6,32 % | $[-2{,}35\;;\;+3{,}85]$ |
| 20 ans | 4,47 % | $[-1{,}44\;;\;+2{,}94]$ |
| 50 ans | 2,83 % | $[-0{,}64\;;\;+2{,}14]$ |

> 🔑 **Vingt ans de données ne suffisent pas à savoir s'il faut lever ou vendre à découvert.**
> L'intervalle contient zéro **et** contient 2. Ce n'est pas un défaut d'échantillon : c'est le
> rapport signal/bruit d'un rendement d'actions, qui exige des siècles pour être tranché
> ([§ 19](../../semestre2/statistique/mathematique/19-interpretation-de-la-confiance.md)).

**La conséquence pratique est l'asymétrie de la parabole autour de son sommet** :

| Levier retenu | $g(L)$ | Écart à $g(L^\star)$ |
|---|---|---|
| $0$ (liquidités) | 5,000 % | −1,125 pt |
| $L^\star/2=0{,}375$ | 5,844 % | **−0,281 pt** |
| $L^\star=0{,}75$ | 6,125 % | — |
| $1{,}5\,L^\star$ | 5,844 % | −0,281 pt |
| $2\,L^\star$ | 5,000 % | −1,125 pt |
| $3\,L^\star$ | 1,625 % | **−4,500 pt** |

> ⭐ **Se tromper par le bas coûte peu, se tromper par le haut coûte tout.** Sous-lever de moitié
> coûte 0,28 point de croissance annuelle ; sur-lever d'un facteur 3 en coûte 4,5. C'est la
> justification, en une ligne, du **demi-Kelly** : puisque $L^\star$ est incertain d'un facteur 2
> ou 3, se placer à $L^\star/2$ ne perd presque rien et met à l'abri du côté où l'erreur est
> ruineuse.

---

## 4.6 Ce que cela dit des ETF à levier

Un ETF « CAC 40 x2 » (ou $\times(-2)$, comme les ETF *bear* du marché parisien) rebalance son
levier **quotidiennement** : c'est, par construction, une position à levier **constant**, donc
exactement l'objet $g(L)$ de ce module. Sa croissance est amputée de $\frac{L^2\sigma^2}{2}$ et
non de $\frac{\sigma^2}{2}$ — soit, à $L=2$, **quatre fois** le drag de l'indice.

⚠️ **C'est pourquoi un ETF à levier ne réplique pas $L$ fois la performance de l'indice sur
plusieurs séances**, et l'écart n'est ni une erreur de suivi ni des frais : c'est le drag. Le
[§ 7.5](07-couvrir-en-pratique.md) le chiffre sur des trajectoires précises, et c'est le
principal argument contre l'usage d'un ETF *bear* comme couverture **durable**.

---

## 4.7 Simulation

### S4.1 — La parabole, l'espérance trompeuse, et le demi-Kelly

```python
import numpy as np, math

mu, sig, c, T = 0.08, 0.20, 0.05, 20

g = lambda L: c + L * (mu - c) - L ** 2 * sig ** 2 / 2
L_star = (mu - c) / sig ** 2
print(f"L* = {L_star:.3f}   g(L*) = {g(L_star):.4%}   g(2L*) = {g(2 * L_star):.4%} = c")

print(f"\n{'L':>6}{'E[R]':>9}{'vol':>8}{'g(L)':>9}{'mediane':>10}{'E[W]':>10}")
for L in (0, 0.5, 0.75, 1, 1.5, 2, 3, 4):
    esp = L * mu - (L - 1) * c if L > 0 else c
    print(f"{L:>6.2f}{esp:>9.2%}{L * sig:>8.0%}{g(L):>9.2%}"
          f"{100 * math.exp(g(L) * T):>10.1f}{100 * math.exp(esp * T):>10.1f}")

# verification par simulation : la mediane suit g, pas l'esperance
rng = np.random.default_rng(2)
B, n = 100_000, 252 * T
dt = 1 / 252
for L in (0.75, 1, 2, 3):
    Z = rng.standard_normal((B, n))
    dW = (L * mu - (L - 1) * c - (L * sig) ** 2 / 2) * dt + L * sig * math.sqrt(dt) * Z
    W = 100 * np.exp(dW.sum(axis=1))
    print(f"L={L:<5} mediane simulee {np.median(W):>8.1f}  theorie {100 * math.exp(g(L) * T):>8.1f}"
          f"   moyenne simulee {W.mean():>9.1f}  P(W<100) = {(W < 100).mean():.1%}")
```

Sortie attendue : $L^\star=0{,}750$, $g(2L^\star)=g(0)=5\,\%$, et une médiane simulée qui colle à
$100e^{g(L)T}$ pendant que la moyenne s'en écarte de plus en plus.

---

## 4.8 Exercices

**E4.1.** Démontrer $g(L)=c+L(\mu-c)-\frac{L^2\sigma^2}{2}$ à partir du lemme d'Itô, ou par
développement limité de $E[\log(1+R_L)]$ à l'ordre 2. *Quelle hypothèse fait-on sur les moments
d'ordre 3 ?*

**E4.2.** Montrer que $g(2L^\star)=g(0)$ **sans** calculer $g(L^\star)$, en utilisant la seule
symétrie de la parabole.

**E4.3.** Un investisseur estime $\mu$ sur 10 ans et applique $\hat L^\star$ chaque année.
Simuler la croissance réalisée sur 30 ans et la comparer à celle du demi-Kelly. *Lequel gagne, et
dans quelle proportion des tirages ?*

**E4.4.** Reprendre la table du § 4.4 en ajoutant la barrière d'appel de marge du
[module 3](03-marge-appel-de-marge-et-ruine.md). *À partir de quel levier la médiane devient-elle
négative — avant, ou après, le seuil $2L^\star$ ?*

**E4.5.** Sur les données du CAC 40, estimer $\mu$ et $\sigma$ sur 20 ans, puis calculer $L^\star$
pour $c\in\{2\,\%,4\,\%,6\,\%,8\,\%\}$. *Pour quelle valeur de $c$ le levier optimal
passe-t-il sous 1 ?*

**E4.6.** Montrer que le drag $\frac{L^2\sigma^2}{2}$ explique **entièrement** l'écart entre un
ETF $\times2$ et le double de l'indice sur un an de marché sans tendance. *Le vérifier
numériquement.*

---

## 4.9 À retenir

- **La richesse se multiplie**, donc c'est $E[\log(1+R)]$ qui gouverne, pas $E[R]$. L'écart entre
  les deux est le **drag de volatilité**, conséquence directe de Jensen.
- **$g=\mu-\frac{\sigma^2}{2}$ sans levier ; $g(L)=c+L(\mu-c)-\frac{L^2\sigma^2}{2}$ avec.** Le
  gain est linéaire, le drag quadratique : d'où un optimum.
- ⭐ **$L^\star=\dfrac{\mu-c}{\sigma^{2}}$**. Avec $\mu=8\,\%$, $\sigma=20\,\%$ et un portage SRD
  à 5 % : $L^\star=0{,}75$ — **inférieur à 1**. Le levier n'est pas rentable par défaut ; il l'est
  quand $\mu-c$ est grand devant $\sigma^2$.
- ⭐ **Au-delà de $2L^\star$, on fait moins bien qu'en restant en liquidités** ; au-delà encore, la
  croissance devient négative alors que l'espérance continue de monter. Espérance et médiane
  divergent, et c'est la médiane qu'on vit.
- ⭐ **$L^\star$ est inconnaissable** : 20 ans de données donnent un IC 95 % de $[-1{,}44;2{,}94]$.
  Puisque l'erreur par excès coûte 4 à 16 fois l'erreur par défaut, **viser $L^\star/2$**.
- **Un ETF à levier est une position à levier constant** : son drag est $L^2$ fois celui de
  l'indice. Ce n'est pas un défaut du produit, c'est sa définition.

---

⬅️ [Module 3 — Marge, appel de marge et ruine](03-marge-appel-de-marge-et-ruine.md) ·
➡️ [Module 5 — La vente à découvert](05-la-vente-a-decouvert.md) ·
🏠 [Sommaire](README.md)
