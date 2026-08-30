# Module 5 — Exemple chiffré : Airbus contre le CAC 40

**Prérequis :** modules 1 à 4.
**Ce qu'on établit ici :** rien de nouveau — les quatre modules exécutés de bout en bout sur 1026 rendements.

---

## 5.1 — Les données

```bash
python python/import_societe.py AIR.PA  --debut 2020-01-02 --fin 2023-12-30
python python/import_societe.py '^FCHI' --debut 2020-01-02 --fin 2023-12-30
```

Deux séries de 1027 séances, du 2 janvier 2020 au 29 décembre 2023.
L'intersection des dates en compte **1027**, donc $n = 1026$ rendements
arithmétiques quotidiens et $Y = 1026/252 = 4{,}071$ ans.

Taux sans risque posé à $r_f = 0$ — choix discutable sur 2022-2023, à retenir
comme réserve ([module 2](02-le-calcul-et-ses-erreurs-types.md#21--préparer-les-séries)).

## 5.2 — Les deux performances, séparément

| | CAC 40 | AIR.PA |
|---|---|---|
| Performance totale | $+24{,}86\,\%$ | $+7{,}70\,\%$ |
| CAGR | $+5{,}60\,\%$ | $+1{,}84\,\%$ |
| Volatilité annualisée | $21{,}94\,\%$ | $45{,}02\,\%$ |
| Sharpe ($r_f = 0$) | $+0{,}255$ | $+0{,}041$ |
| Repli maximal | $-38{,}6\,\%$ | $-64{,}7\,\%$ |
| Séances positives | $53{,}6\,\%$ | $51{,}8\,\%$ |

Le titre fait **trois fois moins bien** que son indice avec **deux fois plus** de
volatilité. Tout le reste du module consiste à dire si cela constitue un alpha
négatif — et la réponse va être non.

## 5.3 — La régression

| Grandeur | Valeur |
|---|---|
| $\beta$ | $1{,}5316$ |
| $t_\beta = (\beta-1)/\operatorname{SE}(\beta)$ | $+12{,}46$, $p < 10^{-4}$ |
| $\alpha$ quotidien | $-0{,}00033\,\%$ |
| $\operatorname{SE}(\alpha)$ quotidienne | $0{,}05898\,\%$ |
| $t_\alpha$ | $-0{,}0056$, $p = 0{,}9955$ |
| $R^2$ | $0{,}5573$ ($\rho = 0{,}7465$) |
| Volatilité résiduelle | $29{,}98\,\%$/an |

Annualisé, avec $t_{1024;\,0{,}975} = 1{,}962$ :

$$\alpha_{\text{an}} = -0{,}08\,\%, \qquad
\operatorname{SE}(\alpha_{\text{an}}) = 14{,}86\,\%, \qquad
\text{IC}_{95\%} = [-29{,}25\ ;\ +29{,}08]\,\%$$

*Contrôle du [module 3](03-l-horizon-necessaire.md)* :
$\sigma_\varepsilon/\sqrt Y = 29{,}98/\sqrt{4{,}071} = 14{,}86\,\%$ ✓ — la formule
en trois symboles retrouve exactement l'erreur type du calcul complet.

## 5.4 — La lecture

**Sur le bêta : conclusion nette.** $\beta = 1{,}53$ avec $t = +12{,}5$ contre 1.
Airbus amplifie son indice de moitié, et ce n'est pas discutable. Cela explique à
soi seul l'essentiel de l'écart de volatilité : $1{,}53 \times 21{,}94 = 33{,}6\,\%$
de volatilité de marché, à quoi s'ajoutent $29{,}98\,\%$ de volatilité propre —
$\sqrt{33{,}6^2 + 30{,}0^2} = 45{,}0\,\%$, la volatilité observée. ✓

**Sur l'alpha : aucune conclusion.** $-0{,}08\,\%$ par an, $p = 0{,}996$. Il faut
résister à deux tentations symétriques :

- dire « l'alpha est négatif » — il ne l'est pas au sens statistique, $-0{,}08$
  n'est pas distinguable de $0$ ;
- dire « l'alpha est nul, donc le titre n'a rien détruit » — on n'a pas non plus
  établi cela.

La seule phrase exacte : **on n'a rien mesuré.** L'intervalle va de $-29\,\%$ à
$+29\,\%$ par an ; il contient aussi bien un désastre qu'un talent exceptionnel.
Le [§ 3.4](03-l-horizon-necessaire.md#34--le-plus-petit-alpha-détectable) l'avait
annoncé avant tout calcul : à 30 % de volatilité résiduelle sur 4 ans, seul un
alpha dépassant $29{,}4\,\%$/an aurait pu être établi.

**Le paradoxe apparent, résolu.** Comment le titre peut-il faire $+7{,}7\,\%$
contre $+24{,}9\,\%$ tout en ayant un alpha nul ? Parce qu'avec $\beta = 1{,}53$,
son rendement *attendu* n'était pas celui de l'indice. Le CAC ayant progressé de
$+0{,}0313\,\%$ par séance, l'attendu est
$1{,}53 \times 0{,}0313 = 0{,}0479\,\%$ par séance en arithmétique — et le titre a
délivré à peu près cela. Sa sous-performance cumulée vient du **drag de
volatilité** ([module 4](04-cinq-pieges.md#41--le-drag-de-volatilité)), pas d'un
défaut de rendement moyen.

## 5.5 — Les réserves, appliquées

| Piège du [module 4](04-cinq-pieges.md) | S'applique ici ? |
|---|---|
| Drag de volatilité | ✅ **au premier chef** — c'est l'explication du § 5.4 |
| Indice nu | ✅ `^FCHI` est un indice de prix, `Close` est ajustée : l'alpha est surestimé d'environ 3 points/an |
| Bêta instable | ✅ la période contient un krach, une reprise et un cycle de taux |
| Erreurs non i.i.d. | ✅ l'IC de 58 points est en réalité plus large encore |
| Tests multiples | ❌ un seul titre testé, sur une période fixée d'avance |

Trois de ces réserves élargissent l'intervalle ou en décalent le centre. Aucune
ne peut le rétrécir. **La conclusion « rien de mesurable » est donc solide, et
c'est la seule qui le soit.**

## 5.6 — Synthèse

| Question | Réponse |
|---|---|
| Le titre a-t-il battu son indice ? | Non : $+7{,}7\,\%$ contre $+24{,}9\,\%$ |
| Est-ce dû à un défaut de rendement propre ? | **Non établi** — l'alpha est indiscernable de zéro |
| A-t-il pris plus de risque ? | Oui, sans ambiguïté : $\beta = 1{,}53$, $t = +12{,}5$ |
| D'où vient l'écart cumulé ? | Essentiellement du drag de volatilité : $45\,\%$ contre $22\,\%$ |
| Que faudrait-il pour trancher sur l'alpha ? | Environ **35 ans** de données à cette volatilité résiduelle pour détecter $10\,\%$/an ([§ 3.3](03-l-horizon-necessaire.md#33--combien-dannées-pour-détecter-un-alpha)) |

---

⬅️ [Module 4 — Cinq pièges](04-cinq-pieges.md) ·
🏠 [README du cours](README.md)
