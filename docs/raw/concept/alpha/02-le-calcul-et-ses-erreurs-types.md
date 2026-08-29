# Module 2 — Le calcul et ses erreurs types

**Prérequis :** [module 1](01-de-quoi-alpha-est-le-nom.md), et le [module 3 du cours canal](../canal/03-epaisseur-variable-et-levier.md) pour le levier.
**Ce qu'on établit ici :** les formules complètes, les deux tests à conduire, et l'annualisation.

---

## 2.1 — Préparer les séries

Trois précautions, chacune source d'erreurs silencieuses.

**Aligner les calendriers.** Un titre et son indice n'ont pas nécessairement les
mêmes séances : jours fériés locaux, suspensions de cotation. Il faut prendre
l'**intersection des dates**, jamais supposer que les deux fichiers ont la même
longueur. Sur AIR.PA et `^FCHI` en 2020-2023, les deux séries font 1027 séances
et l'intersection en fait 1027 — mais c'est à vérifier, pas à postuler.

**Choisir les rendements.** Arithmétiques, $r_t = P_t/P_{t-1} - 1$. Les rendements
logarithmiques se somment mieux dans le temps, mais l'alpha du modèle de marché
est défini sur des rendements arithmétiques : mélanger les deux fausse le résultat.
$n$ rendements pour $n+1$ prix.

**Traiter le taux sans risque.** La formule porte sur des rendements **excédentaires**
$r_i - r_f$. Poser $r_f = 0$ est acceptable sur une période de taux nuls, ne l'est
plus depuis 2022. Deux règles : appliquer $r_f$ **aux deux** séries, et **annoncer**
la valeur retenue même quand elle est nulle. Poser $r_f = 0$ décale $\alpha$ de
$(\beta - 1)\,r_f$ — donc de $+1{,}5\,\%$ par an pour $\beta = 1{,}5$ et
$r_f = 3\,\%$, ce qui n'est pas négligeable.

## 2.2 — Les deux coefficients

Moments de population ($\div n$), convention du modèle :

$$\beta = \frac{\operatorname{Cov}(r_i, r_m)}{\operatorname{Var}(r_m)}
\qquad\qquad
\alpha = E(r_i) - \beta\,E(r_m)$$

Résidus $\hat e_t = r_{i,t} - (\alpha + \beta\,r_{m,t})$, de somme nulle
([étape 1](../modele/01-elimination-de-l-ordonnee.md)), et estimateur sans biais
de la variance du bruit :

$$s^2 = \frac{1}{n-2}\sum_t \hat e_t^{\,2}$$

C'est le $s$ du [cours canal](../canal/README.md#notations), pas
$\sigma_{\hat e}$ : on divise par $n-2$, deux paramètres ayant été consommés.

## 2.3 — Les erreurs types viennent du levier

Le [module 3 du cours canal](../canal/03-epaisseur-variable-et-levier.md) définit
le levier d'un point $x$ dans une régression :

$$h(x) = \frac1n + \frac{\bigl(x - E(x)\bigr)^2}{n\operatorname{Var}(x)}$$

et donne $\operatorname{SE}$ de la valeur ajustée en $x$ comme $s\sqrt{h(x)}$.
Or $\alpha$ **est** la valeur ajustée en $r_m = 0$ : c'est ce que rapporterait le
titre une séance où l'indice ne bouge pas. D'où, directement :

$$\boxed{\;\operatorname{SE}(\alpha) = s\sqrt{h(0)} = s\sqrt{\frac1n + \frac{E(r_m)^2}{n\operatorname{Var}(r_m)}}\;}$$

$$\boxed{\;\operatorname{SE}(\beta) = \frac{s}{\sqrt{n\operatorname{Var}(r_m)}}\;}$$

**Une simplification qui vaut d'être notée.** Le levier se met en facteur :

$$h(0) = \frac1n\left(1 + \frac{E(r_m)^2}{\operatorname{Var}(r_m)}\right)$$

et sur des rendements quotidiens, $E(r_m)$ est minuscule devant $\sigma(r_m)$.
Sur le CAC 40 en 2020-2023 : $E(r_m) = 0{,}0313\,\%$ et $\sigma(r_m) = 1{,}3821\,\%$,
donc $E(r_m)^2/\operatorname{Var}(r_m) = 5{,}1\cdot10^{-4}$. Le facteur correctif
vaut $1{,}00051$ : **$h(0)$ dépasse $1/n$ de 0,05 %**, écart sans conséquence.

$$h(0) \simeq \frac1n \qquad\Longrightarrow\qquad \operatorname{SE}(\alpha) \simeq \frac{s}{\sqrt n}$$

C'est cette approximation qui donne au [module 3](03-l-horizon-necessaire.md) sa
formule d'horizon. Elle cesse d'être bonne sur des rendements mensuels ou annuels,
où $E(r_m)$ n'est plus négligeable.

## 2.4 — Deux tests, pas un

À $n-2$ degrés de liberté, avec `p_valeur_student()` de
[`python/import_societe.py`](../../../../python/import_societe.md) — la loi est
celle de l'[étape 8](../modele/08-test-de-tendance.md) :

| Test | Statistique | Question |
|---|---|---|
| **Alpha** | $t_\alpha = \dfrac{\alpha}{\operatorname{SE}(\alpha)}$ | le rendement inexpliqué est-il distinguable de zéro ? |
| **Bêta** | $t_\beta = \dfrac{\beta - 1}{\operatorname{SE}(\beta)}$ | le titre est-il plus ou moins volatil que son indice ? |

> ⚠️ **Le test sur $\beta$ se fait contre 1, pas contre 0.** Tester $\beta = 0$
> demande si le titre a un lien avec le marché — question sans intérêt pour une
> action cotée, et qui rejette toujours. La question utile est $\beta = 1$ :
> le titre suit-il son indice, ou l'amplifie-t-il ?

Sur AIR.PA : $t_\beta = +12{,}46$ ($p < 10^{-4}$) contre $t_\alpha = -0{,}006$
($p = 0{,}996$). **Le même jeu de données tranche complètement sur $\beta$ et pas
du tout sur $\alpha$** — le [module 3](03-l-horizon-necessaire.md) explique
pourquoi c'est structurel.

## 2.5 — Annualiser

$\alpha$ est un rendement par période ; on le publie par an. L'annualisation est
**linéaire**, et s'applique aussi à son erreur type et à son intervalle :

$$\alpha_{\text{an}} = 252\,\alpha, \qquad
\operatorname{SE}(\alpha_{\text{an}}) = 252\operatorname{SE}(\alpha), \qquad
\text{IC}_{95\%} = \alpha_{\text{an}} \pm t_{n-2;\,0{,}975}\operatorname{SE}(\alpha_{\text{an}})$$

$\beta$ est un rapport de rendements : il **ne s'annualise pas**.

Le multiplicateur 252 est le nombre conventionnel de séances par an ; sur les
1027 séances d'AIR.PA, le compte réel donne $1026/252 = 4{,}07$ ans.

## 2.6 — Les compléments à publier

Un alpha seul est incomplet. Cinq grandeurs l'accompagnent :

| Grandeur | Formule | Ce qu'elle ajoute |
|---|---|---|
| $R^2$ | $\rho^2$ ([étape 5](../modele/05-coefficient-de-correlation.md)) | part des mouvements expliquée par l'indice |
| Volatilité résiduelle | $s\sqrt{252}$ | **la grandeur qui fixe la précision de $\alpha$** |
| Tracking error | $\sigma(r_i - r_m)\sqrt{252}$ | écart type de la surperformance brute |
| Ratio d'information | $252\,E(r_i - r_m)/\text{TE}$ | surperformance brute rapportée à son risque |
| Nombre d'observations | $n$, et $Y = n/252$ | sans quoi rien n'est interprétable |

> ⚠️ Le ratio d'information porte sur la surperformance **brute**, non corrigée du
> bêta : ce n'est pas un alpha rapporté à son risque. Sur AIR.PA il vaut $+0{,}128$
> alors que l'alpha est nul et que le titre a fait trois fois moins bien que
> l'indice en cumulé — voir le [module 4](04-cinq-pieges.md#41--le-drag-de-volatilité).

---

⬅️ [Module 1 — De quoi alpha est le nom](01-de-quoi-alpha-est-le-nom.md) ·
➡️ [Module 3 — L'horizon nécessaire](03-l-horizon-necessaire.md)
