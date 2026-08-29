# Module 2 — L'effet de levier

**Durée : 1 h.** Prérequis : [module 1](01-le-cadre-cac40-et-le-srd.md).

> **La question traitée.** « Le levier multiplie les gains et les pertes. » C'est vrai, c'est trivial, et c'est **faux** dès qu'on y regarde de près : il y a un coût qui ne se multiplie pas, un levier qui dérive tout seul, et une asymétrie qui n'est pas là où on la cherche.

---

## 2.1 Le bilan, et rien d'autre

Capital propre $C_0$, levier $L\ge0$, exposition $E_0=L\,C_0$, dette $(L-1)C_0$ au taux de portage $c$ (le $c$ du [§ 1.3](01-le-cadre-cac40-et-le-srd.md) : CRD + report + spread).

| Actif             | Passif             |
| ----------------- | ------------------ |
| Titres : $L\,C_0$ | Dette : $(L-1)C_0$ |
|                   | Capital : $C_0$    |

Sur un an, le titre fait $R$. L'actif devient $LC_0(1+R)$, la dette $(L-1)C_0(1+c)$, d'où le capital final et le **rendement des fonds propres** :

$$\boxed{\;R_L \;=\; L\,R \;-\; (L-1)\,c\;}$$

C'est une **fonction affine de $R$**, de pente $L$ et d'ordonnée $-(L-1)c$. Tout ce que le levier fait — le bon comme le mauvais — est contenu dans ces deux nombres.

---

## 2.2 La table

$c=5\,\%$, horizon un an.

| $R$ (le titre) | $L=1$    | $L=2$    | $L=3$         | $L=5$     |
| -------------- | -------- | -------- | ------------- | --------- |
| $-30\,\%$      | −30,00 % | −65,00 % | **−100,00 %** | −170,00 % |
| $-20\,\%$      | −20,00 % | −45,00 % | −70,00 %      | −120,00 % |
| $-10\,\%$      | −10,00 % | −25,00 % | −40,00 %      | −70,00 %  |
| $0\,\%$        | 0,00 %   | −5,00 %  | −10,00 %      | −20,00 %  |
| $+10\,\%$      | +10,00 % | +15,00 % | +20,00 %      | +30,00 %  |
| $+20\,\%$      | +20,00 % | +35,00 % | +50,00 %      | +80,00 %  |
| $+30\,\%$      | +30,00 % | +55,00 % | +80,00 %      | +130,00 % |

Deux seuils se lisent directement sur la formule :

$$R_0=c\Bigl(1-\frac1L\Bigr)\quad(\text{seuil de rentabilité}),\qquad
R_{\text{ruine}}=\frac{-1+(L-1)c}{L}\quad(R_L=-100\,\%).$$

| $L$ | Volatilité | Seuil $R_0$ | Ruine à      |
| --- | ---------- | ----------- | ------------ |
| 1   | $\sigma$   | 0,00 %      | −100,00 %    |
| 2   | $2\sigma$  | +2,50 %     | −47,50 %     |
| 3   | $3\sigma$  | +3,33 %     | −30,00 %     |
| 4   | $4\sigma$  | +3,75 %     | −21,25 %     |
| 5   | $5\sigma$  | +4,00 %     | **−16,00 %** |

> 🔑 **Lecture.** À levier 5, une baisse de 16 % du titre efface la totalité des fonds propres.
> Le CAC 40 a connu des baisses de 16 % en quelques séances plus d'une fois par décennie. Et la
> ruine n'est même pas le premier événement à survenir : l'appel de marge arrive **avant**
> ([module 3](03-marge-appel-de-marge-et-ruine.md)).

---

## 2.3 Ce que la formule dit vraiment

### a) La volatilité, elle, se multiplie exactement

$R_L$ est affine en $R$, donc

$$E[R_L]=L\,E[R]-(L-1)c,\qquad \sigma(R_L)=L\,\sigma(R),\qquad
\text{Sharpe}(R_L)=\frac{L\bigl(E[R]-c\bigr)}{L\,\sigma(R)}=\frac{E[R]-c}{\sigma(R)} .$$

> ⭐ **Le levier ne change pas le ratio de Sharpe.** Il déplace le portefeuille **le long** de la droite qui joint le taux de financement au portefeuille sous-jacent — il ne l'améliore jamais.  Toute la question du [module 8](08-le-portefeuille-optimal.md) est donc : *sur quelle droite se place-t-on avant de la parcourir ?* Choisir le portefeuille est une décision de **qualité**, choisir le levier une décision d'**échelle**. Les confondre est l'erreur la plus courante.

⚠️ **Le Sharpe n'est invariant que si le financement se fait à $c$ pour tout le monde et à tout
moment.** En pratique $c$ dépend du courtier, monte avec les taux, et l'appel de marge introduit
une non-linéarité que le ratio de Sharpe ne voit pas.

### b) Le coût ne se multiplie pas, il s'ajoute

L'ordonnée $-(L-1)c$ est un **prélèvement fixe**, indépendant de $R$. À $L=3$ et $c=5\,\%$, la position perd 10 % par an si le titre stagne. Sur trois ans de marché plat, les fonds propres sont amputés de plus d'un quart sans qu'aucune prévision n'ait été fausse.

### c) Le point fixe est $R=c$

$R_L=R$ exactement quand $R=c$. En dessous, lever **détruit** ; au-dessus, lever **crée**. Le
levier n'est donc pas un pari sur la hausse : c'est un pari sur le fait que le titre fasse mieux
que **le taux auquel on l'emprunte**.

---

## 2.4 Le levier dérive tout seul

Une position SRD non rebalancée ne conserve **pas** son levier. Après une baisse de $x$ :

$$C=C_0(1-Lx),\qquad E=E_0(1-x),\qquad
\boxed{\;L'=\frac{E}{C}=L\,\frac{1-x}{1-Lx}\;>\;L\quad(x>0)}$$

| Baisse $x$ | $L_0=2$ | $L_0=3$ | $L_0=5$ |
| ---------- | ------- | ------- | ------- |
| 5 %        | 2,11    | 3,35    | 6,33    |
| 10 %       | 2,25    | 3,86    | 9,00    |
| 15 %       | 2,43    | 4,64    | 17,00   |
| 20 %       | 2,67    | 6,00    | ruine   |
| 30 %       | 3,50    | 21,00   | ruine   |

> ⚠️ **C'est le mécanisme, pas la psychologie, qui augmente le risque après une perte.** Une
> position à levier 5 qui perd 15 % se retrouve à levier **17** : la séance suivante, un mouvement
> de 6 % l'efface. Ne rien faire n'est pas rester neutre — c'est **augmenter** le levier.

---

## 2.5 L'asymétrie n'est pas où on croit

Le sophisme habituel : « à levier 3, perdre 30 % puis gagner 30 % ne ramène pas au point de
départ ». Vérifions, sans rebalancement :

| Baisse du titre | $L=1$   | $L=2$   | $L=3$   | $L=5$   |
| --------------- | ------- | ------- | ------- | ------- |
| 5 %             | +5,3 %  | +5,3 %  | +5,3 %  | +5,3 %  |
| 10 %            | +11,1 % | +11,1 % | +11,1 % | +11,1 % |
| 20 %            | +25,0 % | +25,0 % | +25,0 % | jamais  |
| 30 %            | +42,9 % | +42,9 % | +42,9 % | jamais  |

*(hausse du **titre** nécessaire pour que les fonds propres retrouvent $C_0$, coût de portage mis à part)*

> 🔑 **La colonne est constante — et c'est le résultat du module.** Sans rebalancement, le prix de
> retour à l'équilibre ne dépend **pas** du levier : la position redevient entière quand le titre
> redevient ce qu'il était. L'asymétrie destructrice du levier ne vient donc **ni** de l'arithmétique des pourcentages, **ni** du levier en soi. Elle vient de trois choses, et de trois seulement :
>
> 1. le **coût de portage** qui court pendant l'attente (§ 2.3 b) ;
> 2. l'**appel de marge**, qui interdit d'attendre — [module 3](03-marge-appel-de-marge-et-ruine.md) ;
> 3. le **rebalancement à levier constant**, qui vend en baisse et achète en hausse — [module 4](04-levier-optimal-et-drag.md).
>
> La colonne « jamais » à $L=5$ est le point 2 déguisé en point 1 : les fonds propres ont été
> détruits avant.

---

## 2.6 Simulation

### S2.1 — Les trois tables du module, et la dérive

```python
import numpy as np

c = 0.05

def r_levier(R, L, c=c):
    return L * R - (L - 1) * c

print(f"{'R':>7}" + "".join(f"{'L=' + str(L):>10}" for L in (1, 2, 3, 5)))
for R in (-0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30):
    print(f"{R:>+7.0%}" + "".join(f"{r_levier(R, L):>+10.2%}" for L in (1, 2, 3, 5)))

print("\nseuils")
for L in (1, 2, 3, 4, 5):
    print(f"L={L}  rentabilite {c * (1 - 1 / L):>+7.2%}   ruine {(-1 + (L - 1) * c) / L:>+8.2%}")

print("\nderive du levier apres une baisse (sans rebalancement)")
for x in (0.05, 0.10, 0.15, 0.20, 0.30):
    ligne = f"{x:>6.0%}"
    for L in (2, 3, 5):
        eq = 1 - L * x
        ligne += f"{L * (1 - x) / eq:>10.2f}" if eq > 0 else f"{'ruine':>10}"
    print(ligne)

# invariance du Sharpe : verification par simulation
rng = np.random.default_rng(0)
R = rng.normal(0.08, 0.20, 200_000)
for L in (1, 2, 3, 5):
    RL = r_levier(R, L)
    print(f"L={L}  E={RL.mean():>+7.2%}  sigma={RL.std():>6.2%}  "
          f"Sharpe={(RL.mean() - c) / RL.std():.4f}")
```

Sortie attendue : les deux premières tables du module, et un **ratio de Sharpe identique à la
troisième décimale** pour les quatre leviers — l'invariance du § 2.3 a.

---

## 2.7 Exercices

**E2.1.** Démontrer $R_L = L R-(L-1)c$ à partir du bilan, en supposant que le portage est payé en
fin de période. *Que devient la formule si le portage est prélevé mensuellement et capitalisé ?*

**E2.2.** Tracer $R\mapsto R_L$ pour $L\in\{1,2,3,5\}$ et vérifier graphiquement que les quatre
droites se coupent en $R=c$. *Interpréter ce point d'intersection en une phrase.*

**E2.3.** Montrer que $L'=L\frac{1-x}{1-Lx}$ est croissante en $x$ sur $[0,1/L[$ et diverge en
$x\to1/L$. *Quel est le sens financier de cette divergence ?*

**E2.4.** Un investisseur veut un rendement espéré de 12 % sur un titre dont $E[R]=8\,\%$, avec
$c=5\,\%$. Quel levier ? Quelle volatilité en résulte si $\sigma=25\,\%$ ? *Comparer à la
volatilité d'une ligne unique du CAC 40 non levée.*

**E2.5.** Reprendre la table du § 2.5 en **incluant** le coût de portage sur un an d'attente.
*De combien la colonne $L=3$ s'écarte-t-elle alors de la colonne $L=1$ ?*

**E2.6.** Sur les données du script, mesurer combien de fois en 20 ans le CAC 40 a baissé de plus
de 16 % depuis un plus haut. *Conclusion pour un levier 5 maintenu en permanence.*

---

## 2.8 À retenir

- **$R_L=LR-(L-1)c$** : affine, pente $L$, ordonnée $-(L-1)c$. Tout le module tient là.
- ⭐ **Le levier ne modifie pas le ratio de Sharpe** : il change l'échelle du risque, pas la
  qualité du portefeuille. La qualité se décide au [module 8](08-le-portefeuille-optimal.md).
- **Le coût de portage est un prélèvement fixe**, pas un multiplicateur : à $L=3$, $c=5\,\%$, un
  marché plat coûte 10 % par an.
- **Le point fixe est $R=c$** : lever, c'est parier que le titre bat le taux d'emprunt, pas qu'il
  monte.
- ⭐ **Le levier dérive à la hausse quand la position perd** : $L'=L\frac{1-x}{1-Lx}$. Ne rien
  faire, c'est augmenter le risque.
- ⚠️ **Sans rebalancement ni appel de marge, le levier n'introduit aucune asymétrie de
  récupération.** L'asymétrie vient du **portage**, de l'**appel de marge** (module 3) et du
  **rebalancement** (module 4) — pas de l'arithmétique des pourcentages.

---

⬅️ [Module 1 — Le cadre](01-le-cadre-cac40-et-le-srd.md) ·
➡️ [Module 3 — Marge, appel de marge et ruine](03-marge-appel-de-marge-et-ruine.md) ·
🏠 [Sommaire](README.md)
