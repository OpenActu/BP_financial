# Module 7 — La loi normale et ses transformées ⭐

**Durée : 1 h.** Prérequis : modules [5](05-fonction-generatrice-des-moments.md),
[6](06-fonction-caracteristique.md) et [6f](06f-loi-normale.md).

> **La question traitée.** Démontrer les deux transformées de la loi normale : sa **fonction
> génératrice des moments** $M_Z(t)=e^{t^2/2}$ et sa **fonction caractéristique**
> $\varphi_Z(t)=e^{-t^2/2}$. Puis dire pourquoi la seconde ne s'obtient pas en remplaçant
> naïvement $t$ par $it$ dans la première.

**Où ces deux valeurs servent :**

| Module | Ce qui en dépend |
|---|---|
| [8](08-addition-de-lois-et-stabilite-gaussienne.md) | La stabilité gaussienne : $aZ_1+bZ_2\sim\mathcal N(0,a^2+b^2)$, d'où $\bar X\sim\mathcal N(\mu,\sigma^2/n)$ |
| [12](12-theoreme-central-limite.md) | L'étape 4 du TCL : reconnaître $e^{-t^2/2}$ comme la f.c. d'une $\mathcal N(0,1)$ |
| [15](15-loi-du-chi2.md) | Le calcul de $E(Z^4)=3$, d'où $\operatorname{Var}(\chi^2(k))=2k$ |

---

## 7.1 Le résultat

> **Proposition.** Pour $Z\sim\mathcal N(0,1)$ :
> $$M_Z(t)=E\!\left(e^{tZ}\right)=e^{t^2/2} \qquad\text{et}\qquad \varphi_Z(t)=E\!\left(e^{itZ}\right)=e^{-t^2/2}.$$

## 7.2 La FGM, par mise sous forme canonique

Par définition,

$$M_Z(t)=\int_{-\infty}^{+\infty}e^{tz}\,\frac{1}{\sqrt{2\pi}}\,e^{-z^2/2}\,dz
=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^{+\infty}e^{\,tz-\frac{z^2}{2}}\,dz .$$

Tout est dans l'exposant. On y **complète le carré** :

$$tz-\frac{z^2}{2}=-\frac{1}{2}\left(z^2-2tz\right)=-\frac{1}{2}\left(z-t\right)^2+\frac{t^2}{2}$$

Le terme $t^2/2$ ne dépend pas de $z$ : il sort de l'intégrale.

$$M_Z(t)=e^{t^2/2}\underbrace{\int_{-\infty}^{+\infty}\frac{1}{\sqrt{2\pi}}\,e^{-\frac{(z-t)^2}{2}}\,dz}_{\textstyle =\,1}=e^{t^2/2}
\qquad\blacksquare$$

L'intégrale restante vaut 1 parce que c'est **la densité d'une $\mathcal N(t,1)$ intégrée sur
$\mathbb R$** — aucun calcul n'est nécessaire, seulement de la reconnaître.

> 🔑 **Le mécanisme est celui de la translation.** Multiplier la densité gaussienne par $e^{tz}$
> revient à **décaler sa moyenne de $t$** sans changer sa forme, au facteur $e^{t^2/2}$ près. C'est
> cette stabilité par translation qui rend la famille gaussienne si maniable — et c'est elle qui,
> au [module 8](08-addition-de-lois-et-stabilite-gaussienne.md), fait qu'une somme de gaussiennes
> indépendantes reste gaussienne.

**Le cas général** s'en déduit sans nouveau calcul : si $X=\mu+\sigma Z\sim\mathcal N(\mu,\sigma^2)$,
la propriété affine du § 5.3 donne

$$M_X(t)=E\!\left(e^{t(\mu+\sigma Z)}\right)=e^{\mu t}M_Z(\sigma t)=e^{\,\mu t+\frac{\sigma^2t^2}{2}}$$

## 7.3 La fonction caractéristique, par équation différentielle

On ne peut pas remplacer naïvement $t$ par $it$ dans le calcul précédent : « compléter le
carré » avec un nombre complexe déplace le chemin d'intégration dans le plan complexe, ce qui
demande un argument d'analyse complexe. Il existe un chemin purement réel, plus court.

Dérivons sous l'intégrale — licite, la domination étant assurée par $|z|e^{-z^2/2}$, qui est
intégrable :

$$\varphi_Z'(t)=\int_{-\infty}^{+\infty} iz\,e^{itz}\,\frac{e^{-z^2/2}}{\sqrt{2\pi}}\,dz$$

On intègre par parties en remarquant que $z\,e^{-z^2/2}=-\frac{d}{dz}\!\left(e^{-z^2/2}\right)$ :

$$\varphi_Z'(t)=\frac{i}{\sqrt{2\pi}}\left(\underbrace{\Bigl[-e^{itz}e^{-z^2/2}\Bigr]_{-\infty}^{+\infty}}_{\textstyle =\,0}
+\int_{-\infty}^{+\infty} it\,e^{itz}\,e^{-z^2/2}\,dz\right)=-t\,\varphi_Z(t)$$

Reste une équation différentielle linéaire du premier ordre, $\varphi'=-t\varphi$, avec la condition
initiale $\varphi_Z(0)=1$. Sa solution est unique :

$$\varphi_Z(t)=e^{-t^2/2}\qquad\blacksquare$$

> ⚠️ **Le signe est la seule différence, et il n'est pas anodin.** $M_Z$ **explose** en
> $e^{+t^2/2}$, $\varphi_Z$ **décroît** en $e^{-t^2/2}$ — et $|\varphi_Z|\le 1$, comme pour toute
> fonction caractéristique. C'est exactement pourquoi l'étape 3 de la démonstration du TCL
> ([module 12](12-theoreme-central-limite.md)) pourra conclure : la limite $e^{-t^2/2}$ est
> bornée, continue en 0, donc éligible au théorème de Lévy.

## 7.4 Les moments de la gaussienne

Développer $e^{t^2/2}=\sum_k \frac{t^{2k}}{2^k k!}$ et identifier avec
$M_Z(t)=\sum_j \frac{E(Z^j)}{j!}t^j$ (§ 5.2) donne d'un coup **tous** les moments :

$$\boxed{\;E(Z^{2k})=(2k-1)!!=1\cdot3\cdot5\cdots(2k-1)\qquad\text{et}\qquad E(Z^{2k+1})=0\;}$$

| $k$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $E(Z^k)$ | 0 | **1** | 0 | **3** |

$E(Z^4)=3$ est la valeur dont le [module 15](15-loi-du-chi2.md) a besoin : elle donne
$\operatorname{Var}(Z^2)=3-1=2$, donc $\operatorname{Var}(\chi^2(k))=2k$. Le **kurtosis** de la
gaussienne vaut donc 3 — c'est la référence à laquelle on compare toutes les autres lois.

---

## 7.5 Vérification numérique

Les deux formules se contrôlent en trois lignes — utile pour ne pas se tromper de signe.

```python
import numpy as np
rng = np.random.default_rng(7)
Z = rng.standard_normal(2_000_000)
for t in (0.5, 1.0, 2.0, 3.0):
    M = np.mean(np.exp(t * Z))
    phi = np.mean(np.exp(1j * t * Z))
    print(f"t={t:>4} : M={M:9.4f} (theorie {np.exp(t**2/2):9.4f})"
          f"   phi={phi.real:+7.4f} (theorie {np.exp(-t**2/2):7.4f})")

print("moments :", [round(np.mean(Z**k), 4) for k in (1, 2, 3, 4)], " (theorie 0, 1, 0, 3)")
```

| $t$ | $M_Z$ estimé | $e^{t^2/2}$ | $\varphi_Z$ estimé | $e^{-t^2/2}$ |
|---|---|---|---|---|
| 0,5 | 1,1328 | 1,1331 | 0,8826 | 0,8825 |
| 1,0 | 1,6472 | 1,6487 | 0,6067 | 0,6065 |
| 2,0 | 7,3660 | 7,3891 | 0,1359 | 0,1353 |
| 3,0 | **95,62** | **90,02** | 0,0118 | 0,0111 |

⚠️ **La colonne FGM se dégrade, la colonne fonction caractéristique non** — et c'est exactement
le phénomène annoncé au [§ 5.5](05-fonction-generatrice-des-moments.md). $E(e^{tZ})$ est dominée
par les rares tirages où $Z$ est grand : à $t=3$, l'estimation est fausse de 6 %, tantôt
au-dessus tantôt en dessous selon la graine, sur deux millions de tirages. $E(e^{itZ})$ moyenne
des quantités de **module 5** : trois décimales justes partout, sans effort.

---

## 7.6 Exercices

**E7.1.** Démontrer directement, sans passer par la standardisation, que
$X\sim\mathcal N(\mu,\sigma^2)$ a pour FGM $M_X(t)=e^{\mu t+\sigma^2t^2/2}$. *Indication : mettre
sous forme canonique l'exposant $tx-\frac{(x-\mu)^2}{2\sigma^2}$.*

**E7.2.** Reprendre la démonstration du § 7.3 en justifiant les deux points admis : la dérivation
sous l'intégrale et l'annulation du terme tout intégré.

**E7.3.** Retrouver $E(Z^{2k})=(2k-1)!!$ par développement en série des deux membres de
$M_Z(t)=e^{t^2/2}$. *(Vérification : $E(Z^4)=3$, d'où un kurtosis de 3.)*

**E7.4.** Calculer $E(Z^6)$ et $E(Z^8)$. *À quelle vitesse les moments de la gaussienne
croissent-ils ?*

**E7.5.** Que vaut $\varphi_X(t)$ pour $X\sim\mathcal N(\mu,\sigma^2)$ ? *En déduire, avec (P2) du
§ 6.2, la loi de $X_1+X_2$ pour deux gaussiennes indépendantes — c'est le
[module 8](08-addition-de-lois-et-stabilite-gaussienne.md) en une ligne.*

---

## 7.7 À retenir

- $Z\sim\mathcal N(0,1)$ : $M_Z(t)=e^{t^2/2}$, $\varphi_Z(t)=e^{-t^2/2}$ — **seul le signe
  change**, et il change tout : l'une explose, l'autre est bornée par 1.
- $X\sim\mathcal N(\mu,\sigma^2)$ : $M_X(t)=e^{\mu t+\sigma^2t^2/2}$, obtenu sans nouveau calcul
  par $X=\mu+\sigma Z$.
- **Le mécanisme du § 7.2 est la translation** : multiplier la densité gaussienne par $e^{tz}$
  décale sa moyenne sans changer sa forme. De là vient la stabilité de la famille gaussienne par
  somme d'indépendantes.
- **Le mécanisme du § 7.3 est l'équation différentielle** $\varphi'=-t\varphi$, obtenue par
  intégration par parties. Il évite le déplacement de contour dans le plan complexe qu'exigerait
  la substitution $t\mapsto it$.
- **$E(Z^{2k})=(2k-1)!!$**, moments impairs nuls, **$E(Z^4)=3$** — kurtosis de référence.

---

⬅️ [Module 6f — La loi normale](06f-loi-normale.md) ·
➡️ [Module 8 — Addition de lois et stabilité gaussienne](08-addition-de-lois-et-stabilite-gaussienne.md) ·
🏠 [Sommaire](README.md)
