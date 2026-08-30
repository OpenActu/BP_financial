# Module 1 — Le cadre : CAC 40, SRD, vente à découvert

**Durée : 1 h.** Aucun prérequis mathématique.

> **La question traitée.** Les trois objets de ce cours — le levier, la couverture, le portefeuille optimal — sont d'abord des théorèmes. Mais un théorème s'applique dans un cadre, et
> le cadre d'un investisseur particulier à Paris n'est **pas** celui des manuels américains. Que
> peut-on réellement faire, et à quel coût ?

**Pourquoi commencer par là.** La théorie de Markowitz autorise les poids négatifs, la théorie du
levier suppose qu'on emprunte au taux sans risque, la théorie de la couverture suppose qu'on vend à découvert n'importe quel titre. Sur le CAC 40, depuis un compte de particulier, **ces trois
suppositions sont fausses**. Les modules suivants démontrent les résultats *puis* les corrigent
de ces frottements ; ce module dit lesquels.

> ⚠️ **Avertissement de péremption.** Taux de couverture, listes d'éligibilité, seuils de
> déclaration et tarifs sont des **paramètres réglementaires et commerciaux**, révisables. Les
> valeurs citées ici sont celles en vigueur à la rédaction et servent d'**ordres de grandeur** :
> toute décision réelle exige de les revérifier auprès d'Euronext, de l'AMF et de son courtier.
> Ce qui ne se périme pas, ce sont les **mécanismes** — et c'est eux que le cours exploite.

---

## 1.1 L'univers : ce que le script télécharge

`import_societe.py` récupère des cours de clôture ajustés pour des tickers `.PA`. Trois
remarques, dont deux coûtent de l'argent.

| Point                                                                                                                | Conséquence                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CAC 40 = 40 valeurs**, pondérées par capitalisation **flottante**, poids plafonné (règle de plafonnement Euronext) | L'indice est un **portefeuille long-only à poids positifs**, révisé trimestriellement — donc un cas particulier du [module 8](08-le-portefeuille-optimal.md), pas une abstraction |
| **Indice « nu » (*price*) vs indice de **rendement global** (*GR*, dividendes réinvestis)                            | Le CAC 40 usuellement cité est le **price index** : il **ampute** la performance du rendement du dividende, année après année                                                     |
| Cours **ajustés** vs cours bruts                                                                                     | Un cours ajusté réinvestit implicitement les dividendes et neutralise les divisions du nominal ; comparer une série ajustée à l'indice nu, c'est comparer deux choses différentes |

> 🔑 **Première erreur de mesure, et elle est systématique.** Comparer la performance d'un
> portefeuille (dividendes encaissés) au CAC 40 *price* revient à s'attribuer chaque année le
> rendement du dividende. Sur un marché comme Paris, où le rendement distribué est structurellement élevé, c'est l'écart le plus grand que vous rencontrerez entre deux façons de
> mesurer la **même** chose. L'exercice E1.1 le chiffre sur vos propres données.

---

## 1.2 Trois enveloppes, trois cadres juridiques

| Enveloppe                         | Levier                                         | Vente à découvert           | Dérivés                                        | Univers                 |
| --------------------------------- | ---------------------------------------------- | --------------------------- | ---------------------------------------------- | ----------------------- |
| **PEA**                           | ❌ Aucun (pas de SRD, pas de découvert espèces) | ❌ Interdite                 | ❌ Ni futures ni options ; ETF à levier tolérés | Titres UE/EEE éligibles |
| **PEA-PME**                       | ❌                                              | ❌                           | ❌                                              | PME/ETI éligibles       |
| **Compte-titres ordinaire (CTO)** | ✅ SRD, ou marge selon le courtier              | ✅ Sur les valeurs éligibles | ✅ Futures, options, warrants, turbos           | Mondial                 |

**Conséquence structurante pour tout le cours.** L'investisseur en PEA est **contraint long-only et sans levier** : pour lui, le portefeuille optimal est celui du [§ 9.2](09-contraintes-reelles-et-estimation.md) (frontière contrainte), la couverture ne peut passer que par des ETF inverses ([§ 7.4](07-couvrir-en-pratique.md)), et le [module 4](04-levier-optimal-et-drag.md) ne lui sert qu'à savoir **ce qu'il perd** à ne pas pouvoir lever — ou ce qu'il gagne à ne pas pouvoir le faire.

---

## 1.3 Le SRD, mécaniquement

Le **Service de Règlement Différé** permet, sur les valeurs éligibles d'Euronext Paris, d'acheter ou de vendre en différant le règlement-livraison à la **liquidation** mensuelle. Il produit mécaniquement deux choses : un **levier** (on paie plus tard, donc on immobilise moins) et une
**vente à découvert** (on livre plus tard, donc on peut vendre ce qu'on n'a pas).

### La couverture exigée

L'ordre SRD n'est accepté que si le compte présente une **couverture** — un actif nanti — proportionnelle à la position :

| Actifs déposés en couverture   | Taux exigé | Levier maximal $L_{\max}=1/m$ |
| ------------------------------ | ---------- | ----------------------------- |
| Espèces, OPCVM monétaires      | **20 %**   | **5,0**                       |
| Obligations, titres de créance | **25 %**   | **4,0**                       |
| Actions, OPCVM actions         | **40 %**   | **2,5**                       |

⚠️ **Ces taux sont des minima ;** un courtier peut exiger davantage, et **modifier** son exigence
en cours de vie de la position — typiquement quand la volatilité monte, c'est-à-dire au pire
moment. Le [module 3](03-marge-appel-de-marge-et-ruine.md) montre que ce seul détail change la nature du risque.

### Le calendrier et les coûts

| Élément                                   | Mécanique                                                              | Ordre de grandeur                            |
| ----------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------- |
| **Liquidation**                           | Quelques séances avant la fin de mois boursier                         | Mensuelle                                    |
| **Prorogation (report)**                  | Reporter la position au mois suivant                                   | Commission de report, + taux de portage      |
| **CRD** (commission de règlement différé) | Facturée sur le montant de la position                                 | Quelques dizaines de points de base par mois |
| **Dividende détaché**                     | L'**acheteur** SRD le perçoit ; le **vendeur** à découvert le **paie** | Rendement du titre                           |
| **Opérations sur titres**                 | Souvent forcent le dénouement anticipé                                 | Ponctuel                                     |

> 🔑 **Le coût de portage est le paramètre central du cours.** Notez-le $c$ : c'est le taux annuel
> total (CRD + report + spread de financement). Il apparaît dans **toutes** les formules des  modules 2 à 5, et c'est lui qui fait que le levier optimal du [module 4](04-levier-optimal-et-drag.md) est bien plus faible que ce que les manuels laissent croire. Un ordre de grandeur réaliste pour un particulier : **4 % à 8 % par an**.

---

## 1.4 La vente à découvert, juridiquement

Vendre un titre qu'on ne détient pas est **licite mais encadré** en droit européen :

| Règle                                        | Contenu                                                                                                                                                                                  |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Interdiction du *naked short***            | Il faut avoir emprunté le titre, ou avoir un accord de localisation, **avant** de vendre (règlement UE 236/2012)                                                                         |
| **Déclaration des positions courtes nettes** | Notification au régulateur à partir d'un seuil faible de capital (ordre de grandeur : 0,1 %), **publication** au-delà d'un seuil supérieur                                               |
| **Interdictions temporaires**                | Le régulateur peut suspendre la VAD — cela s'est produit sur les financières en 2008 et sur l'ensemble du marché français en mars 2020                                                   |
| **Éligibilité SRD**                          | La VAD n'est possible que sur les valeurs du SRD « classique » ; les valeurs du **SRD long only** sont, comme leur nom l'indique, achetables à crédit mais **non vendables à découvert** |

> ⚠️ **La conséquence la plus importante n'est pas le coût, c'est la discontinuité.** Un
> interdit réglementaire peut fermer votre couverture au moment exact où elle sert. Une stratégie qui *exige* la vente à découvert pour tenir n'est pas une stratégie robuste sur ce marché : c'est une stratégie qui fonctionne sauf les jours où elle compte.

---

## 1.5 Ce que le cadre fait aux trois questions du cours

| Question                | Réponse des manuels                        | Réponse dans ce cadre                                                                                                                                                     |
| ----------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Quel levier ?**       | $L$ libre, financé au taux sans risque $r$ | $L\le 5$ (souvent $\le 2{,}5$), financé à $c\gg r$, avec **appel de marge** — modules [2](02-l-effet-de-levier.md) à [4](04-levier-optimal-et-drag.md)                    |
| **Comment couvrir ?**   | Vendre à découvert le facteur commun       | Futures CAC 40, VAD SRD, options, ETF inverse — chacun avec son défaut, module [7](07-couvrir-en-pratique.md)                                                             |
| **Quel portefeuille ?** | Poids réels, positifs ou négatifs          | $w_i\ge0$ en PEA, univers de 40 valeurs très corrélées, $\Sigma$ mal estimée — modules [8](08-le-portefeuille-optimal.md) et [9](09-contraintes-reelles-et-estimation.md) |

---

## 1.6 Simulation

### S1.1 — Fabriquer les entrées des modules suivants

Tous les modules à venir consomment trois quantités : une volatilité annualisée $\sigma$, une
corrélation moyenne $\bar\rho$, et un rendement du dividende. Elles se calculent sur les données
que le script du dépôt télécharge déjà.

```python
import numpy as np, yfinance as yf

TICKERS = ["AI.PA","AIR.PA","BNP.PA","BN.PA","CA.PA","CS.PA","DG.PA","EN.PA",
           "GLE.PA","KER.PA","MC.PA","OR.PA","ORA.PA","RI.PA","SAN.PA","SU.PA",
           "TTE.PA","VIE.PA","SGO.PA","STLAP.PA"]

px = yf.download(TICKERS + ["^FCHI"], period="5y", interval="1mo",
                 auto_adjust=True, progress=False)["Close"].dropna()
r = np.log(px / px.shift(1)).dropna()

idx = r["^FCHI"]
act = r[TICKERS]

vol = act.std(ddof=0) * np.sqrt(12)
print("volatilite annualisee : mediane %.1f%%  min %.1f%%  max %.1f%%"
      % (100 * vol.median(), 100 * vol.min(), 100 * vol.max()))

C = act.corr().values
hors_diag = C[~np.eye(len(TICKERS), dtype=bool)]
print("correlation moyenne entre lignes : %.3f" % hors_diag.mean())

beta = np.array([np.cov(act[t], idx, ddof=0)[0, 1] / np.var(idx, ddof=0) for t in TICKERS])
print("beta : mediane %.2f  etendue [%.2f ; %.2f]" % (np.median(beta), beta.min(), beta.max()))

# le plancher de diversification du module 9, avec VOS chiffres
s, rb = vol.median(), hors_diag.mean()
print("plancher sigma*sqrt(rho_bar) = %.1f%%" % (100 * s * np.sqrt(rb)))
```

Conservez ces trois nombres : ils remplacent, dans tous les exemples des modules 2 à 9, les
valeurs de référence utilisées ici ($\sigma=28\,\%$ pour une ligne, $\bar\rho=0{,}45$, $\sigma_{\text{CAC}}\approx20\,\%$).

---

## 1.7 Exercices

**E1.1.** Télécharger le CAC 40 *price* (CAC 40) et les cours **ajustés** d'un panier de 20 valeurs sur 10 ans. Comparer la performance annualisée du panier équipondéré à celle de l'indice nu. *Quelle part de l'écart est attribuable aux dividendes, et non à la sélection ?*

**E1.2.** Un compte dispose de 20 000 € en espèces. Calculer l'exposition SRD maximale, puis la
recalculer si la couverture est constituée d'actions déjà détenues pour 20 000 €. *Pourquoi le
second cas est-il doublement dangereux ?*

**E1.3.** Établir la liste des valeurs du CAC 40 qui sont au SRD « classique » et celles qui sont
en « long only ». *Sur combien de valeurs de l'indice une couverture par VAD directe est-elle
réellement possible ?*

**E1.4.** Reprendre l'annonce d'interdiction de la VAD du 17 mars 2020 et le parcours du CAC 40
les 20 séances suivantes. *Un portefeuille couvert par VAD à cette date aurait-il pu maintenir sa
couverture ? Et par future ?*

**E1.5.** Estimer le coût de portage $c$ chez votre courtier : CRD mensuel, commission de report,
taux appliqué. *Convertir en taux annuel équivalent et le comparer aux 5 % utilisés dans ce cours.*

---

## 1.8 À retenir

- **Le CAC 40 usuel est un indice nu** : le comparer à un portefeuille qui encaisse ses dividendes
  est un biais systématique, en votre faveur, et de l'ordre du rendement distribué.
- **Le PEA interdit levier, VAD et dérivés.** Tout ce cours y est donc lu en mode contraint : les
  modules 2 à 7 y servent surtout à savoir ce qu'on ne peut pas faire, et pourquoi c'est parfois
  une protection.
- ⭐ **Le SRD donne un levier plafonné à $1/m$** — 5 avec une couverture espèces, 2,5 avec une
  couverture actions — et ce plafond est **révisable par le courtier en cours de position**.
- ⭐ **Le coût de portage $c$ (4 % à 8 % par an) est le paramètre qui détruit le levier.** Il est
  dans toutes les formules des modules 2 à 5.
- **La vente à découvert est licite mais fragile** : éligibilité restreinte, dividende à payer,
  déclaration, et **suspension possible par le régulateur** — précisément dans les marchés où elle protège.
- **Aucun de ces frottements n'est un détail d'exécution** : chacun change le résultat théorique
  du module correspondant, et le cours les réintroduit un par un.

---

🏠 [Sommaire](README.md) ·
➡️ [Module 2 — L'effet de levier](02-l-effet-de-levier.md)
