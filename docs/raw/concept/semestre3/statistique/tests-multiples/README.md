# Cours — Tests multiples : Bonferroni et Holm

Cours complet sur le contrôle du risque d'erreur quand on ne pose **pas une seule**
question statistique, mais plusieurs. Rédigé pour un niveau **bac+2 en
statistique**.

## Pourquoi ce cours dans ce dépôt

Le [module 8 du cours sur la loi de Student](../loi-de-student/08-robustesse-et-limites.md#88-tests-multiples)
consacre dix-huit lignes au problème : il donne la table de $1-0{,}95^m$, **nomme**
Bonferroni, Holm et Benjamini–Hochberg, et passe à autre chose. Le
[module 4 du cours sur l'alpha](../../../semestre4/alpha/04-cinq-pieges.md) fait de
même. Aucun des deux ne construit ces procédures, ne les démontre, ni ne dit
comment choisir entre elles.

Or le dépôt les **emploie** : les expériences 5, 6 et 13 corrigent toutes par Holm.
L'[expérience 13](../../../../../done/experimentation/experience_13/README.md) en
particulier y a joué deux fois son sort — une fois sur ses dix-huit cellules, une
fois sur son témoin nul, où l'absence de correction avait **arrêté l'expérience à
tort**. Un outil dont dépend un verdict doit être démontré quelque part.

> 🔑 **Le déplacement que ce cours opère tient en une phrase :** le risque de 5 %
> n'est pas attaché à un test, il est attaché à **une famille de tests**. Tout le
> reste — Bonferroni, Šidák, Holm, Benjamini–Hochberg — n'est que la comptabilité
> de ce déplacement.

## Fil directeur

Le cours est construit à l'envers de l'ordre historique. On pose d'abord **le
risque qu'on veut contrôler** (module 1), on en déduit la correction la plus
grossière qui y parvienne (module 2), puis on montre qu'elle est **inutilement
sévère** et qu'une procédure séquentielle fait strictement mieux **sans rien
supposer de plus** (module 3). Le module 4 dit quand ce risque-là n'est pas le bon.

C'est un cours où la démonstration compte plus que la recette : les quatre
procédures tiennent en trois lignes de code chacune, et les écrire ne coûte rien.
Ce qui coûte, c'est de savoir **laquelle**, et **sur quelle famille**.

## Prérequis

| Cours | Ce qu'il apporte ici |
|---|---|
| [**Statistique mathématique**](../../../semestre2/statistique/mathematique/README.md) | La notion de loi, de test, et surtout de **$p$-valeur** ; l'[intervalle de confiance](../../../semestre2/statistique/mathematique/18-intervalle-de-confiance.md) et son [interprétation](../../../semestre2/statistique/mathematique/19-interpretation-de-la-confiance.md) |

**La loi de Student n'est pas un prérequis.** Ce cours ne dépend d'aucune loi
particulière : il prend des $p$-valeurs en entrée, d'où qu'elles viennent —
Student, bootstrap, permutation, ou table. C'est pourquoi il est autonome, et
lisible avant comme après le cours de Student.

⚠️ Une seule propriété est exigée des $p$-valeurs en entrée : que sous $H_0$ elles
soient **uniformes sur $[0,1]$**, ou au moins stochastiquement plus grandes. Le
module 2 montre que toute la validité de Bonferroni et de Holm repose là-dessus,
et nulle part ailleurs.

## Progression

| # | Module | Durée | Sortie attendue |
|---|---|---|---|
| 1 | [Le risque n'est pas où l'on croit](01-le-probleme.md) | 1 h 30 | Savoir distinguer risque par test et risque par famille |
| 2 | [Bonferroni](02-bonferroni.md) | 2 h | La démonstration en une ligne, et ses deux limites |
| 3 | [**Holm**](03-holm.md) ⭐ | 2 h 30 | La procédure, sa preuve, et pourquoi Bonferroni est périmé |
| 4 | [Choisir : FWER, FDR, et la famille](04-choisir.md) | 2 h | Savoir quelle correction, sur quel ensemble |

**Volume total** : ≈ 8 h.

## Le module décisif

- **Module 3 — Holm.** Parce qu'il est **uniformément meilleur** que Bonferroni,
  sous exactement les mêmes hypothèses, pour le même coût de calcul. C'est un des
  rares cas, en statistique, où une méthode en domine une autre sans contrepartie
  — et où continuer d'employer l'ancienne n'a donc aucune justification.

## Outillage

Python. Les quatre procédures s'écrivent à la main en quelques lignes, et c'est
ainsi qu'il faut les aborder :

```bash
pip install numpy scipy statsmodels
```

> ⚠️ `statsmodels.stats.multitest.multipletests` fait tout cela d'un appel. Ne
> l'utilisez qu'**après** avoir écrit la procédure vous-même, et servez-vous-en
> comme d'un contrôle — c'est exactement l'usage qu'en fait le module 3.

> ℹ️ **`scipy` et `statsmodels` ne sont pas installés dans l'environnement de ce
> dépôt, et ne doivent pas l'être** : c'est un
> [invariant](../../../../../../CLAUDE.md) — la loi de Student y est réimplémentée
> en Python pur. Les simulations de ce cours se lancent donc dans un environnement
> séparé. Les deux morceaux qui comptent vraiment — la simulation du FWER au
> module 1 et **la procédure de Holm elle-même** au module 3 — n'en ont pas besoin :
> `numpy` suffit à la première, la bibliothèque standard à la seconde.

## Notations retenues dans tout le cours

| Symbole | Sens |
|---|---|
| $m$ | Nombre de tests de la famille |
| $m_0$ | Nombre d'hypothèses nulles **vraies** (inconnu) |
| $\alpha$ | Risque que l'on veut contrôler, **au niveau de la famille** |
| $p_i$ | $p$-valeur brute du $i$-ème test |
| $p_{(1)} \le \dots \le p_{(m)}$ | Les mêmes, triées par ordre croissant |
| $\tilde p_i$ | $p$-valeur **ajustée**, comparable à $\alpha$ telle quelle |
| **FWER** | *Family-Wise Error Rate* — $P(\text{au moins un faux positif})$ |
| **FDR** | *False Discovery Rate* — proportion attendue de faux parmi les rejets |

## Ce que ce cours ne traite pas

- **Les tests de comparaisons multiples spécifiques à l'ANOVA** — Tukey, Dunnett,
  Scheffé. Ils exploitent la structure du modèle ; les procédures d'ici ne
  supposent rien et s'appliquent à n'importe quelles $p$-valeurs.
- **La correction de la dépendance elle-même.** Holm reste valide sous dépendance
  arbitraire, mais il ne la corrige pas : une famille de tests très corrélés reste
  une famille de tests très corrélés. Pour cela, voir le
  [module 8 de Student](../loi-de-student/08-robustesse-et-limites.md).
- **Le choix de $\alpha$.** Il est conventionnel, et ce cours ne le discute pas.

## Références

| Usage | Référence |
|---|---|
| Source de l'inégalité | C. E. Bonferroni, *Teoria statistica delle classi e calcolo delle probabilità*, 1936 |
| **La procédure séquentielle** | S. Holm, *A simple sequentially rejective multiple test procedure*, Scandinavian Journal of Statistics, 1979 |
| Variante sous indépendance | Z. Šidák, *Rectangular confidence regions…*, JASA, 1967 |
| Le taux de fausses découvertes | Y. Benjamini & Y. Hochberg, *Controlling the false discovery rate*, JRSS-B, 1995 |
| Panorama moderne | Efron & Hastie, *Computer Age Statistical Inference*, ch. 15 |
| Le problème en pratique | A. Gelman & E. Loken, *The garden of forking paths*, 2013 |

---

🏠 [Sommaire — Statistique](../../../sommaire/statistique.md)
