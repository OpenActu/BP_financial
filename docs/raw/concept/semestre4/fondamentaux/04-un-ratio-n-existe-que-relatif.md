# Module 4 — Un ratio n'existe que relatif ⭐

**Prérequis :** [module 1](01-de-quoi-un-ratio-est-le-rapport.md) et les [étapes 1 à 8 du modèle](../../../modele.md#plan-de-la-preuve).
**Ce qu'on établit ici :** qu'un ratio pris seul ne signifie rien, qu'il se traduit en une hypothèse de croissance, et que le P/B est en grande partie une reformulation du ROE — avec une régression qui le montre, et dont la forme est pourtant fausse.

---

## 4.1 — Traduire un PER en hypothèse de croissance

Le modèle de Gordon suppose un dividende croissant au taux constant $g$, escompté
au taux $r$. Il donne

$$P = \frac{D}{r-g} \qquad\Longrightarrow\qquad \text{PER} = \frac{\text{payout}}{r-g}$$

Renversée, la formule livre la **croissance implicite** : ce que le marché doit
attendre pour que le prix actuel soit justifié.

$$g = r - \frac{\text{payout}}{\text{PER}}$$

Avec $r = 8\,\%$ et un payout de 100 % — hypothèses grossières, assumées, et
identiques pour tous, ce qui rend la colonne comparable même si aucune valeur
n'est juste isolément :

| | PER | $g$ implicite | Ce que le marché doit croire |
|---|---|---|---|
| SU.PA | 35,58 | **+5,19 %** | croissance perpétuelle de 5,2 %/an |
| OR.PA | 32,98 | +4,97 % | — |
| AIR.PA | 27,04 | +4,30 % | — |
| SAN.PA | 23,84 | +3,81 % | — |
| MC.PA | 20,90 | +3,22 % | — |
| TTE.PA | 10,90 | **−1,17 %** | déclin perpétuel de 1,2 %/an |
| ORA.PA | 10,27 | −1,74 % | — |
| BNP.PA | 8,87 | **−3,27 %** | déclin perpétuel de 3,3 %/an |

> 🔑 **Voilà ce qu'un PER dit réellement.** « Schneider a un PER de 35 » est
> illisible ; « le marché paie Schneider comme si son bénéfice croissait de 5 %
> par an pour toujours » est une affirmation que l'on peut discuter, et
> éventuellement contredire. Un ratio devient une question quand on le traduit.

⚠️ **Une croissance perpétuelle de 5,2 % est énorme** — supérieure à la
croissance nominale de long terme d'une économie développée. Cela ne dit pas que
Schneider est surévaluée : cela dit que la forme du modèle (croissance unique,
constante, éternelle) est trop pauvre pour un PER élevé. Le modèle ne sert pas à
trancher, il sert à **exposer l'hypothèse**.

## 4.2 — Le P/B est surtout une reformulation du ROE

Le même modèle, écrit en fonds propres plutôt qu'en dividendes, donne :

$$\frac{P}{B} = \frac{\text{ROE} - g}{r - g}$$

Deux conséquences immédiates, avant tout chiffre :

- à $g = 0$, $P/B = \text{ROE}/r$ — le P/B est **proportionnel au ROE** ;
- $P/B = 1$ **exactement** quand $\text{ROE} = r$, quel que soit $g$. Une société
  qui rapporte tout juste son coût du capital vaut ses fonds propres, ni plus ni
  moins.

Testons. Régression de $P/B$ sur le ROE, méthode des
[étapes 6 à 8 du modèle](../../semestre3/modele/07-droite-ajustee.md), sur les huit valeurs du
fil rouge :

$$\widehat{P/B} = -2{,}456 + 0{,}3854 \times \text{ROE}\,[\%]$$

| Contrôle | Valeur |
|---|---|
| $\rho$ | **+0,8194** |
| $R^2$ | **0,6715** |
| $t$ à 6 ddl | **+3,502** |
| $p$ bilatérale | **0,0128** |
| ROE tel que $\widehat{P/B} = 1$ | **8,97 %** |

Deux choses méritent d'être relevées :

- **Le ROE explique 67 % de la variance du P/B.** Un P/B bas est d'abord
  l'énoncé d'un ROE bas. En croire lire une décote, c'est le plus souvent lire
  une rentabilité.
- **La droite croise $P/B = 1$ à un ROE de 8,97 %**, ce que la théorie identifie
  au coût des fonds propres $r$. Obtenir une valeur aussi plausible sans l'avoir
  cherchée est le résultat le plus intéressant de ce module.

## 4.3 — Pourquoi ce beau résultat est quand même faux

Le [contrôle de sensibilité du chartiste](../../../../../.claude/agents/chartiste.md)
est rassurant : retirer n'importe laquelle des huit valeurs laisse la pente entre
$0{,}343$ et $0{,}555$ et la $p$-valeur entre $0{,}009$ et $0{,}041$. La relation
ne tient donc pas à un point.

Et pourtant, il faut refuser de la publier telle quelle. **Les résidus le
disent :**

| | ROE | $P/B$ observé | $\widehat{P/B}$ | Résidu |
|---|---|---|---|---|
| SAN.PA | 5,71 % | 1,34 | **−0,26** | **+1,60** |
| BNP.PA | 10,48 % | 0,94 | 1,58 | −0,64 |
| ORA.PA | 14,16 % | 1,27 | 3,00 | **−1,73** |
| TTE.PA | 14,48 % | 1,49 | 3,12 | −1,63 |
| MC.PA | 16,59 % | 3,32 | 3,94 | −0,62 |
| SU.PA | 18,62 % | 6,94 | 4,72 | **+2,22** |
| OR.PA | 19,41 % | 6,11 | 5,03 | +1,08 |
| AIR.PA | 23,19 % | 6,21 | 6,48 | −0,27 |

> ⚠️ **La droite prédit un $P/B$ de $-0{,}26$ pour Sanofi.** Un prix négatif pour
> des fonds propres positifs n'est pas une approximation médiocre : c'est une
> impossibilité. La forme **linéaire** est fausse, alors même que la corrélation
> est significative à 5 %.

C'est la leçon centrale du module, et elle vaut bien au-delà des fondamentaux :

> 🔑 **Significatif ne veut pas dire correct.** Le test de l'[étape 8](../../semestre3/modele/08-test-de-tendance.md)
> répond à « la pente se distingue-t-elle de zéro ? », jamais à « la droite est-elle
> la bonne courbe ? ». Ici la théorie donne $P/B = (\text{ROE}-g)/(r-g)$, une
> famille d'hyperboles passant par $(r, 1)$ — pas une droite. La droite ajustée
> attrape la pente moyenne sur l'intervalle observé, et devient absurde dès qu'on
> en sort.

Un indice supplémentaire du même défaut : à $g = 0$ la théorie impose une pente
de $1/r \approx 0{,}125$ et une ordonnée à l'origine nulle. On observe $0{,}3854$,
trois fois plus raide, avec une ordonnée fortement négative — la signature d'une
croissance $g$ non nulle et **corrélée au ROE**, que le modèle linéaire écrase en
un seul coefficient.

Trois réserves, enfin, dans l'esprit du [module 4 du cours alpha](../alpha/04-cinq-pieges.md) :

- **$n = 8$.** Huit points pour deux paramètres. L'intervalle de confiance de la
  pente est large et le cours ne le publie pas — ce serait déjà un abus.
- **Univers choisi.** Huit grandes capitalisations du CAC 40, sélectionnées pour
  illustrer, pas tirées au sort.
- **Paire choisie après avoir regardé.** $P/B$ contre ROE est le couple dont on
  savait qu'il fonctionnerait. C'est exactement le piège des tests multiples,
  appliqué à sa propre curiosité.

## 4.4 — Le secteur avant la cherté

Comparer TTE.PA (PER 10,90) à OR.PA (PER 32,98) et conclure que la première est
trois fois moins chère, c'est comparer une compagnie pétrolière à un groupe de
cosmétiques. Les écarts de PER entre secteurs reflètent des différences de
croissance attendue, de cyclicité, d'intensité capitalistique et de risque
réglementaire, bien davantage que des différences d'appréciation.

**La seule comparaison qui tienne est intra-secteur.** Sur le fil rouge, deux
industrielles :

| | PER | P/B | VE/EBITDA | ROE | Dette/EBITDA |
|---|---|---|---|---|---|
| **AIR.PA** | 27,04 | 6,21 | 17,99 | **23,19 %** | **1,59** |
| **SU.PA** | 35,58 | 6,94 | 21,86 | 18,62 % | 2,44 |

Là, la comparaison a un sens : même secteur, ratios homogènes, et Schneider se
paie plus cher sur les trois multiples — PER, P/B, VE/EBITDA — tout en affichant
un ROE inférieur et une dette supérieure. **Ce n'est toujours pas un verdict** — il faudrait examiner les
carnets de commandes, les positions, la croissance attendue — mais c'est une
question bien posée, ce que la comparaison Total/L'Oréal n'était pas.

## Ce qu'il faut retenir

1. Un PER se traduit en croissance implicite ; c'est sous cette forme qu'il
   devient discutable.
2. Le P/B est en grande partie une reformulation du ROE — 67 % de variance
   expliquée sur nos huit valeurs.
3. La régression est significative **et** de forme fausse : elle prédit un P/B
   négatif. Significatif ≠ correct.
4. Un ratio ne se compare qu'à l'intérieur d'un secteur.

---

⬅️ [Module 3 — Ce que la comptabilité laisse au choix](03-ce-que-la-comptabilite-laisse-au-choix.md) ·
➡️ [Module 5 — Exemple chiffré : huit valeurs du CAC 40](05-exemple-chiffre-huit-valeurs.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
