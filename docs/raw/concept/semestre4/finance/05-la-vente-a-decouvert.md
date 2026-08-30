# Module 5 — La vente à découvert

**Durée : 1 h.** Prérequis : modules [1](01-le-cadre-cac40-et-le-srd.md) à
[3](03-marge-appel-de-marge-et-ruine.md).

> **La question traitée.** Vendre à découvert est présenté comme le symétrique de l'achat : on
> gagne quand ça baisse. La symétrie est-elle réelle ?

**Réponse : non, et sur cinq plans à la fois** — le gain est borné et la perte ne l'est pas, le
portage change de signe, le dividende change de camp, le levier dérive plus vite, et le
régulateur peut fermer la position. Ce module chiffre les cinq, puis dit la seule chose pour
laquelle la VAD est réellement bonne — ce qui ouvre le [module 6](06-la-couverture-optimale.md).

---

## 5.1 Mécanique, au SRD

Vendre à découvert, c'est vendre un titre qu'on ne possède pas, en s'engageant à le livrer plus
tard. Au SRD, le dénouement intervient à la liquidation mensuelle, avec possibilité de
**prorogation**. La position exige une couverture ($m=20/25/40\,\%$ selon le collatéral) et n'est
ouverte que sur les valeurs du **SRD classique** — les valeurs « SRD long only » sont exclues
([§ 1.4](01-le-cadre-cac40-et-le-srd.md)).

| Flux | Acheteur à crédit | Vendeur à découvert |
|---|---|---|
| Variation du cours | $+$ | $-$ |
| Dividende détaché | **reçoit** | **paie** |
| Portage / CRD | paie | paie |
| Rachat forcé possible | non | **oui** (rappel du prêt, *buy-in*, interdiction réglementaire) |

> 🔑 **Le portage ne change pas de signe.** C'est le point que l'intuition rate : le vendeur ne
> « touche » pas d'intérêts sur le produit de la vente, il paie une commission comme l'acheteur.
> Les deux côtés du marché paient le teneur de livre. La VAD n'est donc pas l'achat avec un signe
> moins : c'est l'achat avec un signe moins **et** les mêmes frais.

---

## 5.2 Le rendement d'une vente à découvert

Exposition vendue $E_0=L\,C_0$, coût total de portage $k$ (CRD + report + **dividende détaché**),
variation du cours $R_p$ :

$$\boxed{\;R_{\text{VAD}}=-L\,(R_p+k)\;}$$

Avec $k=8\,\%$ (5 % de portage + 3 % de rendement du dividende, ordre de grandeur parisien) :

| Variation du titre | $L=1$ | $L=2$ | $L=3$ |
|---|---|---|---|
| −40 % | +32,0 % | +64,0 % | +96,0 % |
| −30 % | +22,0 % | +44,0 % | +66,0 % |
| −20 % | +12,0 % | +24,0 % | +36,0 % |
| −10 % | +2,0 % | +4,0 % | +6,0 % |
| **−8 %** | **0,0 %** | **0,0 %** | **0,0 %** |
| 0 % | −8,0 % | −16,0 % | −24,0 % |
| +10 % | −18,0 % | −36,0 % | −54,0 % |
| +30 % | −38,0 % | −76,0 % | −114,0 % |
| +50 % | −58,0 % | −116,0 % | −174,0 % |
| +100 % | −108,0 % | −216,0 % | −324,0 % |

> ⭐ **Le seuil de rentabilité d'une VAD n'est pas zéro, c'est $-k$.** Avoir raison sur le sens et
> perdre quand même est le régime **normal** : il faut que le titre baisse de 8 % dans l'année
> juste pour rentrer dans ses frais. Sur le marché parisien, où le rendement du dividende est
> structurellement élevé, ce seuil est un handicap permanent.

---

## 5.3 L'asymétrie, qui est structurelle et non conjoncturelle

$$\text{gain maximal}=+L\;(\text{le titre tombe à }0),\qquad \text{perte maximale}=-\infty .$$

| Le titre fait | Le vendeur ($L=1$, $k=0$) |
|---|---|
| $-100\,\%$ (faillite) | **+100 %**, et c'est le maximum possible |
| $\times2$ | −100 % |
| $\times3$ | −200 % |
| $\times5$ | −400 % |

Simulation, un an, $\mu=7\,\%$, $\sigma=25\,\%$, $k=8\,\%$, 500 000 tirages log-normaux :

| | $L=1$ | $L=2$ |
|---|---|---|
| Espérance | **−15,27 %** | −30,54 % |
| Médiane | −11,95 % | −23,90 % |
| $P(\text{gain})$ | 31,2 % | 31,2 % |
| $P(\text{perte} > 50\,\%)$ | 10,7 % | 31,9 % |
| Pire centile | −94,0 % | −188,0 % |
| Meilleur centile | +33,9 % | +67,8 % |

*(à comparer : détenir le même titre sans levier rapporte, sur les mêmes hypothèses, **+10,25 %**
en espérance — 7,25 % de cours et 3 % de dividende)*

> ⚠️ **Une VAD « nue » a une espérance de rendement négative par construction**, et ce n'est pas
> une opinion de marché : c'est la somme de trois termes négatifs — la dérive positive du
> sous-jacent, le portage, le dividende. Le vendeur à découvert ne parie pas contre une
> entreprise, il parie contre **la dérive, le temps et le dividende** simultanément. Il faut donc
> avoir *beaucoup* plus que raison.
>
> **Notez le meilleur centile : +33,9 %.** Même dans les 1 % de scénarios les plus favorables, le
> gain reste modeste, tandis que le pire centile approche l'effacement total. C'est la
> **concavité** du profil : la queue qui compte n'est pas du côté où l'on gagne.

---

## 5.4 Le levier vendeur dérive plus vite

Comme au [§ 2.4](02-l-effet-de-levier.md), mais dans l'autre sens : ce qui fait mal, c'est la
**hausse**, et la hausse **augmente** l'exposition au lieu de la réduire.

$$L'=L\,\frac{1+x}{1-Lx}\qquad(\text{après une hausse } x)$$

| Hausse $x$ | $L_0=1$ | $L_0=2$ | $L_0=3$ |
|---|---|---|---|
| 5 % | 1,11 | 2,33 | 3,71 |
| 10 % | 1,22 | 2,75 | 4,71 |
| 20 % | 1,50 | 4,00 | 9,00 |
| 30 % | 1,86 | 6,50 | 39,00 |
| 50 % | 3,00 | ruine | ruine |

Le seuil d'appel de marge devient, avec la même contrainte $C/E\ge m$ :

$$x^\star_{\text{VAD}}=\frac{\frac1L-m}{1+m}\qquad
\begin{array}{l}L=1:\;66{,}67\,\%\\ L=2:\;25{,}00\,\%\\ L=3:\;11{,}11\,\%\end{array}\quad(m=20\,\%)$$

> ⚠️ **Comparez au [§ 3.1](03-marge-appel-de-marge-et-ruine.md) :** à levier 2, l'acheteur tient
> jusqu'à −37,5 %, le vendeur casse à +25,0 %. Le dénominateur $1+m$ au lieu de $1-m$ dit tout :
> l'exposition du vendeur **grossit** dans le mouvement qui lui est défavorable. C'est le
> mécanisme du *short squeeze*, avant même toute considération de rareté du titre.

---

## 5.5 Les risques qui ne sont pas dans les formules

| Risque | Contenu | Parade |
|---|---|---|
| **Squeeze** | Les rachats forcés des autres vendeurs alimentent la hausse | Limiter la taille par rapport au flottant et au volume quotidien |
| **Rappel du prêt / *buy-in*** | Le prêteur récupère ses titres ; rachat imposé au prix du marché | Aucune, sinon éviter les titres à faible flottant |
| **Interdiction réglementaire** | Suspension de la VAD par le régulateur ([§ 1.4](01-le-cadre-cac40-et-le-srd.md)) | Utiliser un **future**, non concerné — [§ 7.2](07-couvrir-en-pratique.md) |
| **OST** | OPA, distribution exceptionnelle, division : dénouement anticipé | Surveiller le calendrier |
| **Dividende exceptionnel** | Le vendeur le paie, sans plafond | Sortir avant détachement |

> 🔑 **Le risque dominant d'une VAD n'est pas le prix, c'est la contrainte.** Un acheteur qui a
> tort peut attendre dix ans ; un vendeur qui a tort est délogé par l'appel de marge, le rappel du
> prêt ou le régulateur. Le [module 3](03-marge-appel-de-marge-et-ruine.md) a montré que
> l'impossibilité d'attendre est ce qui coûte cher — ici elle est la règle.

---

## 5.6 À quoi la VAD sert réellement

Puisque l'espérance nue est négative, la VAD n'est pas un instrument de pari directionnel pour un
particulier. Elle a en revanche **deux emplois défendables**, tous deux fondés sur une
**différence**, pas sur un niveau :

1. **Couvrir** — annuler la composante commune d'un portefeuille qu'on veut conserver. C'est
   l'objet du [module 6](06-la-couverture-optimale.md) : ce qui est vendu à découvert n'est pas
   un pari, c'est un facteur de risque dont on ne veut pas.
2. **Financer une position longue** — une paire *long/short* dans le même secteur ne parie que sur
   l'**écart** entre deux titres. La dérive de marché, qui pénalise une VAD nue, se compense entre
   les deux jambes ; il reste le portage et le différentiel de dividende.

⚠️ **Dans les deux cas, ce qu'on vend n'est pas choisi pour baisser, mais pour ressembler à ce
qu'on détient.** C'est un changement complet de critère : on ne cherche plus un rendement espéré,
on cherche une **corrélation**. Et un critère de ressemblance, cela s'écrit
$\operatorname{Cov}/\operatorname{Var}$ — c'est-à-dire exactement l'objet de
[`modele.md`](../../../modele.md).

---

## 5.7 Simulation

### S5.1 — Le vendeur à découvert, sans illusion

```python
import numpy as np

rng = np.random.default_rng(3)
mu, sig, k, B = 0.07, 0.25, 0.08, 500_000

ST = np.exp((mu - sig ** 2 / 2) + sig * rng.standard_normal(B))
Rp = ST - 1                       # variation du cours, hors dividende

for L in (1, 2):
    R = -L * (Rp + k)
    print(f"VAD L={L}: E={R.mean():+.2%}  mediane={np.median(R):+.2%}  "
          f"P(gain)={(R > 0).mean():.1%}  P(perte>50%)={(R < -0.5).mean():.1%}  "
          f"centiles [{np.quantile(R, 0.01):+.1%} ; {np.quantile(R, 0.99):+.1%}]")

print(f"detention simple : E={(Rp + 0.03).mean():+.2%}")

# derive du levier vendeur et seuil d'appel
for L in (1, 2, 3):
    print(f"L={L}  appel de marge a +{(1 / L - 0.20) / 1.20:.2%}  "
          + "  ".join(f"L'({x:.0%})={L * (1 + x) / (1 - L * x):.2f}"
                      for x in (0.05, 0.10, 0.20) if 1 - L * x > 0))
```

Sortie attendue : les deux tables du § 5.3 et du § 5.4, et une espérance de VAD **négative à tous
les leviers** — le levier ne fait que multiplier un nombre négatif.

---

## 5.8 Exercices

**E5.1.** Établir $R_{\text{VAD}}=-L(R_p+k)$ à partir du bilan (dette en titres, actif en
espèces). *Où passe le produit de la vente, et pourquoi ne rapporte-t-il rien au particulier ?*

**E5.2.** Démontrer $x^\star_{\text{VAD}}=\frac{1/L-m}{1+m}$ et comparer terme à terme avec le
$x^\star$ de l'acheteur. *D'où vient le changement de signe au dénominateur ?*

**E5.3.** Un titre du CAC 40 verse 4 % de dividende et coûte 5 % de portage. Quelle baisse
annuelle faut-il pour que la VAD rapporte 10 % ? *Comparer à la baisse annuelle moyenne observée
sur ce titre.*

**E5.4.** Reprendre la simulation avec $\mu=0$ (marché sans dérive). *L'espérance de la VAD
devient-elle positive ? Pourquoi le seuil $-k$ subsiste-t-il ?*

**E5.5.** Construire une paire long/short sur deux valeurs du même secteur du CAC 40 (par exemple
deux bancaires). Calculer la volatilité de l'écart et la comparer à celle de chaque jambe.
*De combien la corrélation réduit-elle le risque, et que reste-t-il à financer ?*

**E5.6.** Simuler un squeeze : hausse de 30 % en cinq séances sur une position $L=2$. *À quelle
séance l'appel de marge tombe-t-il, et quel est le capital restant ?*

---

## 5.9 À retenir

- **$R_{\text{VAD}}=-L(R_p+k)$** : le seuil de rentabilité est $-k$, pas $0$. Il faut que le titre
  **baisse** d'au moins le portage plus le dividende.
- ⭐ **Le portage ne change pas de signe et le dividende change de camp.** Sur le marché parisien,
  cela fait 7 à 9 points par an à rattraper avant de gagner un euro.
- ⭐ **L'espérance d'une VAD nue est négative** (−15,3 % dans l'exemple), avec un gain plafonné à
  $+L$ et une perte non bornée. Ce n'est pas un pari symétrique de l'achat.
- ⭐ **Le levier vendeur dérive dans le mauvais sens** : $L'=L\frac{1+x}{1-Lx}$, et l'appel de
  marge tombe à $+25\,\%$ dès $L=2$ contre $-37{,}5\,\%$ pour l'acheteur.
- **Les risques décisifs sont non financiers** : rappel du prêt, *buy-in*, interdiction du
  régulateur. Une couverture qui peut être fermée d'autorité n'est pas une couverture.
- ⭐ **La VAD ne vaut que dans une différence** : couvrir un facteur commun (module 6) ou jouer un
  écart. Ce qu'on vend est alors choisi pour **ressembler**, non pour baisser — et « ressembler »
  se mesure par $\operatorname{Cov}/\operatorname{Var}$.

---

⬅️ [Module 4 — Levier optimal et drag de volatilité](04-levier-optimal-et-drag.md) ·
➡️ [Module 6 — La couverture optimale](06-la-couverture-optimale.md) ·
🏠 [Sommaire](README.md)
