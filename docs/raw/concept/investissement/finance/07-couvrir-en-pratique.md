# Module 7 — Couvrir en pratique : les instruments du marché parisien

**Durée : 1 h 15.** Prérequis : modules [5](05-la-vente-a-decouvert.md) et [6](06-la-couverture-optimale.md). Utile : [la convexité obligataire](../analyse/convexite/09-la-convexite-obligataire.md) pour le § 7.4.

> **La question traitée.** Le module 6 donne le **ratio** $h^\star$. Il ne dit pas avec **quoi** vendre. Quatre instruments sont accessibles depuis Paris, et aucun n'est neutre : chacun substitue au risque couvert un risque d'une autre nature.

---

## 7.1 Le cahier des charges

Le module 6 impose cinq exigences, et elles sont en conflit :

| Exigence                                    | D'où elle vient                                                                                           |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Corrélation élevée** avec le portefeuille | $1-\rho^2$ est le risque qui survit ([§ 6.2](06-la-couverture-optimale.md))                               |
| **Granularité** fine                        | L'arrondi est un risque ([§ 6.3](06-la-couverture-optimale.md))                                           |
| **Non-résiliable**                          | Une couverture fermée d'autorité n'en est pas une ([§ 5.5](05-la-vente-a-decouvert.md))                   |
| **Coût de portage faible**                  | Il se paie tous les jours, que la couverture serve ou non                                                 |
| **Pas d'exigence de liquidités**            | L'appel de marge peut forcer à déboucler au pire moment ([module 3](03-marge-appel-de-marge-et-ruine.md)) |

---

## 7.2 Le future CAC 40 — l'instrument de référence

| Caractéristique                        | Valeur                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------- |
| Sous-jacent                            | Indice CAC 40                                                             |
| Multiplicateur                         | 10 € le point (contrat standard) ; il existe un contrat de taille réduite |
| Notionnel à 7 800 points               | 78 000 €                                                                  |
| Dépôt de garantie                      | Une fraction du notionnel, appelée en espèces                             |
| Marge de variation                     | **Quotidienne, en espèces**                                               |
| Dividende                              | **Déjà dans le prix forward** — rien à verser                             |
| Concerné par une interdiction de VAD ? | **Non**                                                                   |

> ⭐ **C'est le seul instrument qui coche la case « non-résiliable ».** Vendre un future n'est pas
> vendre à découvert au sens du règlement : la position n'est pas empruntée, ne peut pas être
> rappelée, et n'entre pas dans le champ des suspensions de VAD. Pour une couverture qui doit
> tenir précisément dans les marchés désordonnés, c'est décisif.

**Ce qu'il coûte.** Le prix forward vaut $F=S\,e^{(r-q)T}$ : le dividende $q$ est déjà déduit.
L'espérance de gain d'une position vendeuse est donc, à l'équilibre,

$$E[F_0-S_T]\;\approx\;-S\times(\text{prime de risque})\times T .$$

Autrement dit le future ne coûte **ni** portage explicite **ni** dividende : il coûte exactement
la **prime de risque abandonnée** — ce que le [§ 6.4](06-la-couverture-optimale.md) avait annoncé. C'est le coût irréductible de toute couverture linéaire.

⚠️ **Sa contrainte est la trésorerie.** La marge de variation est appelée **chaque soir en
espèces**. Une couverture qui perd — c'est-à-dire une couverture qui fonctionne, puisque le
portefeuille monte — consomme du cash tous les jours. Il faut le provisionner, sous peine de
devoir déboucler la couverture au plus mauvais moment.

---

## 7.3 La VAD au SRD

Vendre à découvert un tracker CAC 40, ou un panier de titres, reproduit la couverture avec les
frottements du [module 5](05-la-vente-a-decouvert.md) : portage **et** dividende à verser (7 à 9 % par an), éligibilité limitée, risque de rappel, et **suspension possible par le régulateur**.

> ⚠️ **Le seul cas où elle est préférable** est la couverture d'un risque **spécifique** : vendre la valeur elle-même, ou une concurrente très proche, quand l'exposition à neutraliser n'est pas
> le marché mais un secteur ou un titre. Le future n'y peut rien — sa corrélation avec un risque
> idiosyncratique est nulle par définition.

---

## 7.4 Les options — l'assurance, et son tarif

Acheter un put, c'est une couverture **convexe** : elle ne coupe que les baisses et laisse la
hausse intacte. Le prix de cette asymétrie se lit dans la prime. Black–Scholes, $S=7\,800$,
$\sigma=20\,\%$, $r=3\,\%$ :

| Échéance | Strike               | Prime (points) | % du notionnel | Coût annualisé si roulé |
| -------- | -------------------- | -------------- | -------------- | ----------------------- |
| 3 mois   | 7 800 (à la monnaie) | 281,6          | 3,61 %         | **14,44 %**             |
| 3 mois   | 7 410 (−5 %)         | 130,2          | 1,67 %         | 6,68 %                  |
| 3 mois   | 7 020 (−10 %)        | 47,8           | 0,61 %         | **2,45 %**              |
| 6 mois   | 7 800                | 380,8          | 4,88 %         | 9,76 %                  |
| 6 mois   | 7 020 (−10 %)        | 113,8          | 1,46 %         | 2,92 %                  |
| 1 an     | 7 800                | 503,7          | 6,46 %         | 6,46 %                  |
| 1 an     | 7 020 (−10 %)        | 216,0          | 2,77 %         | 2,77 %                  |

**Trois lectures.**

- **Assurer intégralement coûte le rendement espéré du portefeuille.** Rouler un put à la monnaie tous les trimestres coûte 14,4 % par an, soit près du double de la prime de risque des actions. Une couverture permanente par options à la monnaie transforme mécaniquement un portefeuille d'actions en placement à rendement négatif.
- **La franchise est ce qui rend l'assurance abordable** : accepter les 10 premiers pour cent de baisse divise le coût par six. C'est la logique d'une franchise d'assurance, et c'est le seul usage économiquement défendable des puts pour un particulier.
- **La prime courte est plus chère par unité de temps** — 14,4 % annualisés à 3 mois contre 6,5 %
  à 1 an, à strike identique. La valeur temps ne décroît pas linéairement, elle décroît en $\sqrt T$ ; rouler court est la façon la plus onéreuse d'être couvert en permanence.

> 🔑 **Le put est à la couverture ce que la convexité obligataire est au prix d'une obligation** :
> un terme d'ordre 2 qui joue toujours dans le même sens, et qui **se paie** — [§ 9.5 du cours de convexité](../analyse/convexite/09-la-convexite-obligataire.md). Le vendeur d'option encaisse cette prime précisément parce qu'il accepte une position **concave**, comme le vendeur à découvert du [§ 5.3](05-la-vente-a-decouvert.md).

---

## 7.5 Les ETF inverses — la seule couverture accessible en PEA

Les ETF *bear* du marché parisien (type « CAC 40 $\times(-2)$ ») répliquent **deux fois l'inverse
de la variation quotidienne**, et sont éligibles au PEA. Ils n'exigent ni marge, ni compte SRD, et
la perte est plafonnée au montant investi. En contrepartie, ils rebalancent leur levier **chaque
soir** — donc ils subissent le drag du [module 4](04-levier-optimal-et-drag.md), multiplié par $L^2=4$.

| Trajectoire de l'indice       | Indice  | ETF $\times(-2)$ | Attendu naïvement |
| ----------------------------- | ------- | ---------------- | ----------------- |
| +10 % puis −9,09 %            | 0,00 %  | **−5,45 %**      | 0,00 %            |
| −10 % puis +11,11 %           | 0,00 %  | **−6,67 %**      | 0,00 %            |
| 10 séances alternées ±3 %     | −0,45 % | −1,79 %          | +0,90 %           |
| 10 séances alternées ±1 %     | −0,05 % | −0,20 %          | +0,10 %           |
| 10 séances de −1 % (tendance) | −9,56 % | **+21,90 %**     | +19,12 %          |

> ⭐ **Lecture, et c'est la table la plus utile du module.** L'indice revient à son point de
> départ et l'ETF a perdu 5 à 7 % : la couverture a coûté sans avoir rien couvert. En revanche,
> dans une **baisse tendancielle** — le scénario pour lequel on se couvre — l'effet joue en
> faveur du porteur : +21,9 % contre +19,1 % attendus. Le rebalancement quotidien est une
> stratégie qui **vend en baisse et achète en hausse** : elle gagne dans les tendances et perd
> dans les marchés hachés.
>
> **Conclusion pratique :** un ETF inverse est un instrument de couverture **tactique et court**.
> Le tenir six mois « au cas où » coûte cher et ne protège pas de ce qu'on croit.

---

## 7.6 Tableau de synthèse

|                         | Future CAC 40             | VAD SRD    | Put               | ETF $\times(-2)$                   |
| ----------------------- | ------------------------- | ---------- | ----------------- | ---------------------------------- |
| Éligible PEA            | ❌                         | ❌          | ❌                 | ✅                                  |
| Corrélation à l'indice  | Quasi parfaite            | Élevée     | Non linéaire      | Élevée à 1 jour, dérive ensuite    |
| Granularité             | Grossière (78 000 €)      | Fine       | Moyenne           | **Fine**                           |
| Coût de portage         | Prime de risque seule     | 7 à 9 %/an | 2,5 à 14 %/an     | Drag $\propto L^2\sigma^2$ + frais |
| Appel de marge          | **Quotidien, en espèces** | Oui        | Non (prime payée) | Non                                |
| Perte maximale          | Non bornée                | Non bornée | **Prime**         | Montant investi                    |
| Résiliable par un tiers | Non                       | **Oui**    | Non               | Non                                |
| Conserve la hausse      | ❌                         | ❌          | **✅**             | ❌                                  |

> 🔑 **Aucune ligne « meilleur choix ».** Le future est le plus propre et le plus exigeant en
> trésorerie ; le put est le seul qui garde la hausse et le plus cher ; l'ETF inverse est le seul
> accessible en PEA et le seul qui se dégrade tout seul ; la VAD est la seule qui couvre un risque
> **spécifique** et la seule qu'un tiers peut fermer.

---

## 7.7 Et la couverture partielle ?

Rien n'oblige à prendre $h=h^\star$. La forme canonique du [§ 6.1](06-la-couverture-optimale.md)
chiffre exactement ce que coûte un $h$ plus faible :

$$\operatorname{Var}(h)=\operatorname{Var}_{\min}+\operatorname{Var}(r_M)(h-h^\star)^2,$$

tandis que le coût de portage, lui, est **linéaire** en $h$. Réduire de moitié la couverture
divise le coût par deux et n'ajoute que $\operatorname{Var}(r_M)\,(h^\star/2)^2$ de variance : sur
le portefeuille $P$ du [§ 6.2](06-la-couverture-optimale.md), passer de $h^\star$ à $h^\star/2$
fait remonter la volatilité résiduelle de 0,94 % à 4,13 % annualisés, contre 8,09 % non couvert —
soit **75 % de la réduction de variance** obtenue pour la moitié du coût.

> ⭐ **La moitié du coût achète les trois quarts de la réduction de risque.** Comme partout dans ce
> cours, le critère est quadratique d'un côté et linéaire de l'autre — donc l'optimum coût/risque
> n'est presque jamais au bout du chemin.

---

## 7.8 Simulation

### S7.1 — Le prix de l'assurance et le drag de l'ETF inverse

```python
import numpy as np, math

Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))

def put(S, K, r, sig, T):
    d1 = (math.log(S / K) + (r + sig ** 2 / 2) * T) / (sig * math.sqrt(T))
    return K * math.exp(-r * T) * Phi(-(d1 - sig * math.sqrt(T))) - S * Phi(-d1)

S = 7800
for T in (0.25, 0.5, 1.0):
    for m in (1.00, 0.95, 0.90):
        p = put(S, S * m, 0.03, 0.20, T)
        print(f"T={T:>4}  K={m:.0%}S  prime={p:>7.1f} pts = {p / S:>6.2%}  "
              f"annualise si roule : {p / S / T:>6.2%}")

def etf(chemin, L=-2):
    v = 1.0
    for r in chemin:
        v *= 1 + L * r
    return v - 1

chemins = {
    "+10% puis -9,09%": [0.10, -1 / 11],
    "-10% puis +11,11%": [-0.10, 1 / 9],
    "10 seances +/-3%": [0.03, -0.03] * 5,
    "10 seances +/-1%": [0.01, -0.01] * 5,
    "10 seances de -1%": [-0.01] * 10,
}
for nom, ch in chemins.items():
    idx = np.prod([1 + r for r in ch]) - 1
    print(f"{nom:<20} indice {idx:>+7.2%}   ETF -2x {etf(ch):>+7.2%}   naif {-2 * idx:>+7.2%}")
```

Sortie attendue : les deux tables des § 7.4 et 7.5 — dont les deux lignes « retour au point de
départ » où l'ETF perd 5 à 7 % pour un indice inchangé.

---

## 7.9 Exercices

**E7.1.** Vérifier que $F=Se^{(r-q)T}$ implique qu'une couverture par future ne coûte **pas** le
dividende. *Où est-il passé ?*

**E7.2.** Un portefeuille de 250 000 € est couvert par 4 contrats FCE. L'indice monte de 15 % en
un mois. *Quelle marge de variation faut-il avoir provisionnée ? Le portefeuille, lui, a monté —
est-ce un problème ?*

**E7.3.** Comparer, sur une baisse de 25 % puis un retour au point de départ en un an, les quatre
instruments du § 7.6. *Lequel a le meilleur résultat final ? Lequel a le meilleur résultat au
creux ?*

**E7.4.** Montrer que le coût annualisé d'un put à la monnaie roulé varie comme $1/\sqrt T$.
*Combien de fois plus cher est un roulement mensuel qu'un roulement annuel ?*

**E7.5.** Démontrer que la valeur d'un ETF à levier $L$ quotidien vaut, en continu,
$\bigl(S_T/S_0\bigr)^{L}\exp\bigl(-\tfrac{L(L-1)\sigma^2 T}{2}\bigr)$. *Retrouver le drag du
module 4 et expliquer le signe pour $L=-2$.*

**E7.6.** Sur 10 ans de CAC 40, calculer la performance d'un ETF $\times(-2)$ simulé, détenu en
continu. *Comparer à $-2$ fois la performance de l'indice, et décomposer l'écart.*

---

## 7.10 À retenir

- **Le future est l'instrument de référence** : corrélation quasi parfaite, pas de dividende à
  payer, **non résiliable par un tiers**. Ses défauts sont la granularité (78 000 €) et la marge
  de variation **quotidienne en espèces**.
- **La VAD ne se justifie que pour un risque spécifique** — et reste exposée au rappel du prêt et
  à l'interdiction réglementaire.
- ⭐ **Le put garde la hausse, et c'est ce qu'on paie** : 14,4 % par an à la monnaie roulé
  trimestriellement, 2,5 % avec une franchise de 10 %. Assurer intégralement un portefeuille
  d'actions coûte plus que ce que les actions rapportent.
- ⭐ **L'ETF inverse est le seul outil de couverture en PEA**, et sa mécanique de rebalancement
  quotidien lui fait perdre 5 à 7 % sur un aller-retour d'indice. Instrument **tactique**, jamais
  permanent.
- **Aucun instrument n'est neutre** : chacun échange le risque couvert contre un risque de
  trésorerie, de contrepartie, de chemin, ou de prime payée.
- **La couverture partielle est souvent le bon compromis** : coût linéaire, risque quadratique.

---

⬅️ [Module 6 — La couverture optimale](06-la-couverture-optimale.md) ·
➡️ [Module 8 — Le portefeuille optimal](08-le-portefeuille-optimal.md) ·
🏠 [Sommaire](README.md)
