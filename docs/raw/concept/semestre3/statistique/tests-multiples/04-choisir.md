# Module 4 — Choisir : FWER, FDR, et la famille

**Durée : 2 h.** Les modules 2 et 3 contrôlent le FWER. Ce module dit **quand ce
n'est pas le bon risque**, et surtout que la question la plus lourde de
conséquences n'est pas mathématique : c'est celle de la **famille**.

---

## 4.1 Le FWER n'est pas le seul risque possible

Dressons le tableau des issues d'une famille de $m$ tests :

| | Conservées | Rejetées | Total |
|---|---|---|---|
| $H_0$ **vraies** | $U$ | $V$ *(faux positifs)* | $m_0$ |
| $H_0$ **fausses** | $T$ | $S$ *(vraies découvertes)* | $m - m_0$ |
| | | $R$ | $m$ |

Deux façons de contrôler l'erreur :

$$\mathrm{FWER} = P(V \ge 1)
\qquad\qquad
\mathrm{FDR} = \mathbb E\!\left[\frac{V}{\max(R,1)}\right]$$

- Le **FWER** demande : « **au moins une** erreur est-elle probable ? »
- Le **FDR** demande : « quelle **proportion** de mes rejets sont des erreurs ? »

> 🔑 **La différence tient au coût d'un faux positif.** Si un seul faux positif
> ruine la conclusion — un verdict, une règle qu'on va jouer avec de l'argent —,
> c'est le FWER. Si l'on crible dix mille candidats pour en retenir cent à
> vérifier ensuite, une proportion de fausses pistes est le prix normal du
> criblage : c'est le FDR.

## 4.2 Benjamini–Hochberg

> **Procédure BH (montante).** Trier $p_{(1)} \le \dots \le p_{(m)}$. Trouver le
> **plus grand** $k$ tel que
> $$p_{(k)} \le \frac{k}{m}\,\alpha$$
> puis rejeter $H_{(1)}, \dots, H_{(k)}$ — **toutes**, y compris celles dont la
> $p$-valeur dépasse son propre seuil.
>
> Alors $\mathrm{FDR} \le \dfrac{m_0}{m}\alpha \le \alpha$.

Le sens de parcours est l'inverse de celui de Holm, et ce n'est pas un détail :

| | Holm | Benjamini–Hochberg |
|---|---|---|
| Sens | **descendant** — du plus petit $p$ | **montant** — du plus grand $p$ |
| Arrêt | au **premier échec** | au **premier succès** |
| Seuil au rang $i$ | $\dfrac{\alpha}{m-i+1}$ | $\dfrac{i}{m}\alpha$ |
| Contrôle | FWER | FDR |
| Dépendance | **quelconque** | indépendance ou PRDS |
| $p$ ajustée | $\max_{j\le i}\bigl[(m-j+1)p_{(j)}\bigr]$ | $\min_{j\ge i}\bigl[\tfrac{m}{j}p_{(j)}\bigr]$ |

Au rang $m$, BH compare $p_{(m)}$ à $\alpha$ : **aucune correction**. Au rang 1, à
$\alpha/m$ : **exactement Bonferroni**. BH interpole donc entre les deux, et rejette
toujours au moins autant que Holm.

> ⚠️ **BH exige une condition de dépendance que Holm n'exige pas.** La preuve
> originale suppose l'indépendance ; Benjamini–Yekutieli (2001) l'étend à la
> dépendance positive (PRDS), et au cas général **au prix d'un facteur
> $\sum_{i=1}^m 1/i \approx \ln m$** — qui le rend alors plus sévère que Holm. Sur
> des tests dont on ignore la structure de dépendance, cette garantie n'est pas
> acquise.

## 4.3 Quand l'un, quand l'autre

| Situation | Risque à contrôler | Procédure |
|---|---|---|
| Un verdict unique, publié comme tel | FWER | **Holm** |
| Une règle qu'on va jouer avec de l'argent | FWER | **Holm** |
| Un contrôle de validité d'instrument | FWER | **Holm** |
| Criblage de milliers de candidats à revérifier | FDR | BH |
| Exploration déclarée comme telle | FDR | BH |
| $m$ très grand ($10^3$ et plus) | FDR | BH |

> 🔑 **Dans ce dépôt, c'est toujours le FWER.** Les expériences publient des
> verdicts binaires — `UTILE` / `INUTILE` — et un seul faux positif suffit à
> corrompre un verdict. Le criblage à grande échelle, où le FDR prend son sens,
> n'y existe pas : $m$ y vaut 6, 18, ou 20.

## 4.4 Le choix de la famille — le vrai problème

Tout ce qui précède dépend de $m$. Et $m$ dépend d'un découpage qu'aucun théorème
ne fournit. C'est **le point faible de l'édifice**, et il faut le traiter comme
tel : par une déclaration écrite, pas par un calcul.

**Trois règles pratiques :**

1. **La famille se déclare avant de voir les résultats.** Après, tout découpage
   devient un choix intéressé — et il en existe toujours un qui sauve le résultat.
2. **Appartiennent à la même famille les tests entre lesquels on aurait arbitré.**
   Si vous n'auriez publié que le meilleur des $m$, les $m$ forment une famille.
3. **Deux questions différentes font deux familles.** Fondre des tests qui ne
   répondent pas à la même question dilue la correction de ceux qui comptent.

> ⚠️ **Le découpage le plus fin annule la correction.** $m$ familles d'un test,
> c'est aucune correction du tout, et cette option est toujours disponible. C'est
> pourquoi la déclaration préalable n'est pas une formalité : elle est la seule
> chose qui empêche la procédure d'être vide.

## 4.5 Le garde-fou se corrige comme le test

L'[expérience 13](../../../../../done/experimentation/experience_13/README.md) en
donne le contre-exemple exemplaire. Elle corrigeait par Holm ses **18 cellules de
mesure** — et **pas** les **6 cellules** de son témoin nul, chargé de vérifier que
l'instrument n'était pas faussé.

Résultat : six intervalles à 95 % non corrigés se déclenchent
$1-0{,}95^6 = 26{,}5\,\%$ du temps. Le contrôle s'est déclenché, l'expérience s'est
arrêtée, et **c'était une fausse alerte** : après Holm sur cette seconde famille,
$6 \times 0{,}030667 = 0{,}1840$, rien n'excluait zéro.

> 🔑 **Un contrôle de validité est une famille de tests comme une autre.** Non
> corrigé, il se déclenche plus souvent que le test qu'il protège — et il devient
> alors la première cause d'échec de l'expérience, devant le phénomène étudié.

## 4.6 Arbre de décision

```
Combien de tests dans la famille ?
│
├── 1 ......................... aucune correction
│
└── m ≥ 2
    │
    ├── Un seul faux positif ruine-t-il la conclusion ?
    │   │
    │   ├── OUI → contrôler le FWER
    │   │         └── HOLM, toujours.
    │   │             (Bonferroni : jamais meilleur, parfois pire)
    │   │
    │   └── NON, je crible pour revérifier ensuite → contrôler le FDR
    │       │
    │       ├── indépendance ou dépendance positive → BH
    │       └── dépendance inconnue → Benjamini-Yekutieli, ou Holm
    │
    └── Dans tous les cas : la famille a-t-elle été DÉCLARÉE avant ?
        └── NON → aucune correction ne rattrapera ce m-là.
```

## 4.7 Exercices

**E4.1.** Sur `p = [0.005, 0.011, 0.02, 0.30, 0.60]` et $\alpha = 5\,\%$, appliquer
BH. Combien de rejets ? Comparer à Bonferroni (1) et Holm (2).
*(Réponse : **3**. Les seuils BH valent $0{,}01\ ;\ 0{,}02\ ;\ 0{,}03\ ;\ 0{,}04\ ;
\ 0{,}05$ ; le plus grand $k$ tel que $p_{(k)} \le k\alpha/m$ est $k=3$, puisque
$0{,}02 \le 0{,}03$. **1 / 2 / 3** : les trois procédures se classent exactement
dans l'ordre de leur sévérité.)*

**E4.2.** Montrer qu'au rang 1 le seuil de BH vaut $\alpha/m$ et qu'au rang $m$ il
vaut $\alpha$. En déduire l'encadrement de BH entre Bonferroni et l'absence de
correction.

**E4.3.** Simuler $m=1000$ tests dont 100 portent un effet. Comparer le nombre de
vraies découvertes de Holm et de BH, ainsi que leurs $V$ respectifs. Conclure sur
le domaine de chacun.

**E4.4.** Une équipe teste 6 contrôles de validité et 18 mesures. Calculer la
probabilité qu'au moins un contrôle se déclenche à tort si aucun n'est corrigé.
Refaire le calcul en corrigeant. *(C'est l'exercice de l'expérience 13.)*

**E4.5 — le plus important.** Prenez une analyse que vous avez déjà faite.
Énumérez honnêtement toutes les variantes que vous **auriez** essayées si la
première n'avait rien donné. Combien vaut votre $m$ réel ? Votre conclusion y
survit-elle ?

## 4.8 À retenir

- **FWER** = probabilité d'au moins un faux positif. **FDR** = proportion attendue
  de faux parmi les rejets. Le choix dépend du **coût d'un faux positif**.
- **Benjamini–Hochberg** est montant, s'arrête au premier succès, contrôle le FDR
  — mais exige l'indépendance ou une dépendance positive, que Holm n'exige pas.
- **Dans ce dépôt, c'est toujours le FWER, donc toujours Holm** : les verdicts sont
  binaires et $m$ est petit.
- **La famille n'est pas donnée par les mathématiques.** Elle se déclare avant, et
  le découpage le plus fin annule toujours la correction.
- **Un contrôle de validité est une famille comme une autre.** Non corrigé, il
  devient la première cause d'échec de l'expérience.

---

⬅️ [Module 3 — Holm](03-holm.md) ·
🏠 [Sommaire](README.md)
