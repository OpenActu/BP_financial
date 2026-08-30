# Module 6 — Exemple chiffré : Airbus, 20 séances

**Prérequis :** modules 1 à 5, et l'[étape 9](../modele/09-exemple-complet.md) qui régresse cette même série.
**Ce qu'on établit ici :** rien de nouveau — les cinq modules exécutés de bout en bout.

---

## 6.1 — Les données et la droite

Mêmes 20 clôtures qu'à l'[étape 9](../modele/09-exemple-complet.md) : Airbus, du
2 au 29 janvier 2020, cours arrondis au centime, $T_i = i$.

L'étape 9 fournit tout ce dont on a besoin :

$$f(t) = 122{,}367526 + 0{,}151045\,t, \qquad \operatorname{Var}(\hat e)_{\min} = 1{,}957456$$

D'où l'écart-type sans biais du bruit, celui qui sert dans toutes les bandes
([README](README.md#notations)) :

$$s = \sqrt{\tfrac{20}{18}\times 1{,}957456} = \sqrt{2{,}174952} = 1{,}474772
\qquad (\sigma_{\hat e} = 1{,}399091,\ \text{soit } 5{,}1\,\% \text{ de moins})$$

## 6.2 — Résidus, levier, studentisation

$$h(i) = \frac1{20} + \frac{3\,(2i-21)^2}{20\times 399}$$

| $i$ | Date | $V_i$ | $f(i)$ | $\hat e_i$ | $h(i)$ | $\hat e_i^{\,*}$ |
|---|---|---|---|---|---|---|
| 1 | 2020-01-02 | 122,50 | 122,52 | −0,019 | 0,1857 | −0,014 |
| 2 | 2020-01-03 | 122,97 | 122,67 | +0,300 | 0,1586 | +0,222 |
| 3 | 2020-01-06 | 122,44 | 122,82 | −0,381 | 0,1346 | −0,277 |
| 4 | 2020-01-07 | 121,10 | 122,97 | −1,872 | 0,1135 | −1,348 |
| 5 | 2020-01-08 | 123,28 | 123,12 | +0,157 | 0,0955 | +0,112 |
| 6 | 2020-01-09 | 123,78 | 123,27 | +0,506 | 0,0805 | +0,358 |
| 7 | 2020-01-10 | 123,32 | 123,42 | −0,105 | 0,0684 | −0,074 |
| 8 | 2020-01-13 | 123,96 | 123,58 | +0,384 | 0,0594 | +0,269 |
| 9 | 2020-01-14 | 123,95 | 123,73 | +0,223 | 0,0534 | +0,155 |
| 10 | 2020-01-15 | 123,17 | 123,88 | −0,708 | 0,0504 | −0,493 |
| 11 | 2020-01-16 | 122,39 | 124,03 | −1,639 | 0,0504 | −1,140 |
| 12 | 2020-01-17 | 125,49 | 124,18 | +1,310 | 0,0534 | +0,913 |
| 13 | 2020-01-20 | 126,51 | 124,33 | +2,179 | 0,0594 | +1,523 |
| 14 | 2020-01-21 | 125,14 | 124,48 | +0,658 | 0,0684 | +0,462 |
| 15 | 2020-01-22 | 126,59 | 124,63 | +1,957 | 0,0805 | +1,384 |
| 16 | 2020-01-23 | 124,59 | 124,78 | −0,194 | 0,0955 | −0,138 |
| 17 | 2020-01-24 | 127,52 | 124,94 | +2,585 | 0,1135 | +1,861 |
| 18 | 2020-01-27 | 121,93 | 125,09 | **−3,156** | 0,1346 | **−2,301** |
| 19 | 2020-01-28 | 123,16 | 125,24 | −2,077 | 0,1586 | −1,536 |
| 20 | 2020-01-29 | 125,28 | 125,39 | −0,108 | 0,1857 | −0,081 |

*Contrôles :* $\sum_i h(i) = 2{,}000000$ ✓ (module 3) et $\sum_i \hat e_i = 0$ ✓
(module 1). Le levier vaut $0{,}0504$ au centre contre $0{,}1857$ aux deux bords,
soit **3,7 fois plus** — et il est symétrique, comme la formule l'impose.

## 6.3 — Les trois largeurs (module 2)

| Convention | Demi-largeur | En unités de $s$ |
|---|---|---|
| Enveloppe | $-3{,}156$ / $+2{,}585$ | largeur totale $3{,}89\,s$ |
| $\pm 2s$ | $2{,}949$ | $2{,}00\,s$ |

**Contrôle de vraisemblance.** Pour $n=20$ gaussien, l'étendue attendue est
$3{,}74\,s$ ([module 2](02-les-trois-largeurs.md#21--lenveloppe-des-résidus)).
On observe $3{,}89\,s$ : parfaitement ordinaire. **Aucun élargissement anormal du
canal sur cette fenêtre.**

Le canal-enveloppe mesure $5{,}74$ € de large, soit $4{,}6\,\%$ du niveau moyen —
c'est cette forme relative qu'il faut retenir, la seule qui se transporte d'un
titre à l'autre.

## 6.4 — Les trois bandes à la séance courante (module 3)

En $t = 20$, où $h(20) = 0{,}1857$ et $f(20) = 125{,}388$ — c'est exactement la
valeur de `VAL_20` du CSV :

| Bande | Demi-largeur | Intervalle |
|---|---|---|
| **Confiance** à 95 % sur la droite | $2{,}101 \times 1{,}475 \times \sqrt{0{,}1857} = 1{,}335$ | $[124{,}05\ ;\ 126{,}72]$ |
| **Dispersion** $\pm 2s$ | $2{,}949$ | $[122{,}44\ ;\ 128{,}34]$ |
| **Prédiction** à 95 % pour $t=21$ | $2{,}101 \times 1{,}475 \times \sqrt{1{,}1857} = 3{,}416$ | $[122{,}12\ ;\ 128{,}96]$ |

Trois lectures, dans l'ordre de largeur croissante :

- On sait où passe la tendance à $\pm 1{,}34$ € près.
- Les clôtures passées s'en écartent typiquement de $\pm 2{,}95$ €.
- On ne sait pas où sera la clôture du lendemain à mieux que $\pm 3{,}42$ €, soit
  **une fourchette de $6{,}83$ € — $5{,}5\,\%$ du cours — pour une prévision à une
  séance.** C'est le résultat le plus instructif de ce module.

**L'effet de bord, chiffré.** La demi-bande de confiance vaut $0{,}693$ € au
centre de la fenêtre contre $1{,}335$ € en $t=20$ : un rapport de $1{,}93$,
conforme à $\sqrt{(4n-2)/(n+1)} = \sqrt{78/21}$ du
[module 3](03-epaisseur-variable-et-levier.md#b-bande-de-confiance).
`VAL_20` est lue là où la droite est la moins sûre.

## 6.5 — Sorties de canal (module 4)

**Un seul point sort de $\pm 2s$ : $i=18$**, le 27 janvier, avec
$\hat e^{\,*} = -2{,}30$.

| Critère | Constat | Verdict |
|---|---|---|
| Nombre de sorties | 1 | attendu sous $H_0$ : **0,91**. Rigoureusement conforme |
| $\Pr(\ge 1 \text{ sortie})$ sous $H_0$ | — | **60,6 %** : l'événement le plus banal qui soit |
| Ampleur studentisée | $-2{,}30$ | modeste |
| **Persistance** | 1 séance ; $i=19$ revient à $-1{,}54$, dedans | ❌ **pas de rupture** |
| Volume | $1{,}80$ M contre $1{,}05$ M en moyenne, soit $\times 1{,}71$ | seul indice en faveur |

**Conclusion : ce n'est pas une rupture de canal.** Le volume est le seul élément
qui plaide pour, et il ne suffit pas seul. Une paire consécutive du même côté
n'aurait été attendue que dans $2\,\%$ des fenêtres
([module 4](04-sorties-de-canal.md#42--le-bon-critère--la-persistance)) — c'est
ce constat-là qui aurait été informatif, et il ne s'est pas produit.

Noter aussi le point $i=17$ : résidu brut $+2{,}585$, en dessous de $2s = 2{,}949$
donc « dedans », mais studentisé $+1{,}86$. Les deux lectures concordent ici. Sur
un résidu de bord plus fort, elles auraient divergé — c'est le biais décrit au
[§ 4.3.b](04-sorties-de-canal.md#b-sans-studentisation-les-sorties-de-bord-sont-manquées).

## 6.6 — Le canal chartiste (module 2, § 2.5)

Enveloppe convexe des `Low` et des `High` :

- chaîne basse : $(1;121{,}12) \to (5;119{,}73) \to (18;121{,}87) \to (20;122{,}79)$
- chaîne haute : $(1;124{,}51) \to (15;127{,}82) \to (17;127{,}89) \to (20;125{,}67)$

| Arête | Portée | Pente | Retenue ? |
|---|---|---|---|
| support $5 \to 18$ | 13 séances | $+0{,}165$ | ✅ |
| support $18 \to 20$ | 2 séances | $+0{,}460$ | ❌ portée $< n/4 = 5$ |
| résistance $1 \to 15$ | 14 séances | $+0{,}236$ | ✅ |
| résistance $15 \to 17$ | 2 séances | $+0{,}035$ | ❌ |
| résistance $17 \to 20$ | 3 séances | $-0{,}740$ | ❌ |

> ⚠️ **Le piège, en grandeur nature.** Lire naïvement les *dernières* arêtes
> donnerait un support à $+0{,}46$ et une résistance à $-0{,}74$ : un biseau qui
> se referme violemment, figure spectaculaire et **entièrement artificielle**,
> construite sur 2 et 3 séances. La règle de portée minimale
> ([§ 2.5](02-les-trois-largeurs.md#25--lautre-canal--lenveloppe-convexe))
> l'élimine.

**Avec les arêtes retenues, les trois pentes concordent :**

| Méthode | Pente (€/séance) |
|---|---|
| Régression | $+0{,}151$ |
| Support convexe | $+0{,}165$ |
| Résistance convexe | $+0{,}236$ |

Même signe, même ordre de grandeur. La résistance monte un peu plus vite que le
support : le canal chartiste **s'évase** légèrement, là où le canal de régression
est parallèle par construction. C'est la situation d'accord décrite au
[§ 2.5](02-les-trois-largeurs.md#25--lautre-canal--lenveloppe-convexe), la seule
où un canal mérite qu'on s'y fie.

## 6.7 — Canal fixe ou canal glissant ? (module 5)

Ce canal est ajusté sur les séances 1 à 20 et lu en $t=20$. C'est **la seule date
où canal fixe et canal glissant coïncident** : en $t=20$, la fenêtre glissante de
longueur 20 est exactement $[1, 20]$.

Toute lecture de ce canal à une date **antérieure** — « le cours touchait le
support le 15 janvier » — est du regard en avant : le canal du 15 janvier aurait
été ajusté sur les séances $-4$ à $15$, qu'on n'a pas.

## 6.8 — Synthèse

| Question | Réponse chiffrée |
|---|---|
| Y a-t-il une tendance ? | Oui, $+0{,}151$ €/séance, $p = 0{,}017$ ([étape 9](../modele/09-exemple-complet.md)) |
| De quelle largeur est le canal ? | $\pm 2{,}95$ € en dispersion, $4{,}6\,\%$ du cours en enveloppe |
| Le canal est-il anormalement large ? | Non : $3{,}89\,s$ contre $3{,}74\,s$ attendus |
| Où passe la tendance en $t=20$ ? | $125{,}39 \pm 1{,}34$ € |
| Que vaudra la séance 21 ? | Entre $122{,}12$ et $128{,}96$ € — soit rien d'utile |
| Y a-t-il eu rupture ? | Non : une sortie isolée, attendue 6 fois sur 10 sous $H_0$ |

Et la réserve qui prime toutes les autres, celle du
[§ 9.10](../modele/09-exemple-complet.md) : sept semaines après la fin de cette
fenêtre, Airbus cotait $45{,}01$ €. Un canal décrit la fenêtre sur laquelle il est
ajusté. Rien d'autre.

---

⬅️ [Module 5 — Le canal glissant](05-canal-glissant.md) ·
🏠 [README du cours](README.md)
