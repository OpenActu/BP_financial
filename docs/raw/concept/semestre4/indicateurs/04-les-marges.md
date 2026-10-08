# Module 4 — Indicateur 6 : les marges

**Prérequis :** [module 3](03-le-prix-des-attentes.md), et le [module 1 du cours fondamentaux](../fondamentaux/01-de-quoi-un-ratio-est-le-rapport.md).
**Ce qu'on établit ici :** ce qu'une marge dit du cycle d'une entreprise, comment séparer une croissance du bénéfice qui vient du volume de celle qui vient de la marge, et pourquoi une marge haute payée par un multiple haut est la configuration la plus fragile.

---

## 4.1 — Trois marges, trois questions

| Marge | Formule | Ce qu'elle mesure |
|---|---|---|
| brute | $(\text{CA} - \text{coût des ventes})/\text{CA}$ | le pouvoir de fixer ses prix face à ses fournisseurs |
| **opérationnelle** | $\text{résultat opérationnel}/\text{CA}$ | ce que l'activité rapporte, avant financement et impôts |
| nette | $\text{résultat net}/\text{CA}$ | ce qui revient aux actionnaires, après tout |

Le cours retient la **marge opérationnelle** comme indicateur, parce qu'elle
ignore la structure de financement (traitée au [module 5](05-levier-et-dilution.md))
et la fiscalité, et la **marge nette** pour la décomposition du § 4.3, parce que
c'est elle qui fait le bénéfice par action.

Une marge ne se compare **qu'à elle-même ou à son secteur**. Les 7,1 % d'Airbus
et les 20,2 % de L'Oréal ne disent pas que L'Oréal est mieux gérée : un
constructeur d'avions et un fabricant de cosmétiques n'ont ni les mêmes coûts
fixes, ni la même intensité capitalistique.

## 4.2 — Pourquoi les marges reviennent à la moyenne

Une marge exceptionnellement haute attire des concurrents, des clients qui
négocient et des fournisseurs qui relèvent leurs prix. Une marge exceptionnellement
basse pousse à couper des coûts, à sortir des activités déficitaires, ou fait
sortir des concurrents. Les deux forces ramènent la rentabilité vers une
moyenne. Fama et French (2000) l'ont mesuré sur les entreprises américaines :
environ un tiers de l'écart à la moyenne se résorbe chaque année.

Il faut ajouter le **levier opérationnel**. Une entreprise dont une grande part
des coûts est fixe voit sa marge **amplifier** les variations de son chiffre
d'affaires : +10 % de ventes peut faire +30 % de résultat opérationnel. Dans une
phase de croissance, la marge monte avec les ventes, et ce mouvement
**s'extrapole très facilement** — c'est l'un des chemins par lesquels un biais
dominant se forme.

> 🔑 **La double extrapolation.** Une marge au sommet de son cycle, payée par un
> multiple au sommet du sien, suppose deux choses à la fois : que la marge
> **reste** exceptionnelle, et que sa croissance **dure**. Si la marge revient à
> sa moyenne, le bénéfice baisse *et* le multiple aussi, car le marché cesse de
> croire à la croissance qu'il payait. Les deux pertes se multiplient. C'est le
> marqueur **R2** du [module 9](09-assembler-la-sequence.md).

## 4.3 — Volume ou marge ?

Puisque résultat net $=$ CA $\times$ marge nette, en logarithmes :

$$\ln\frac{N_1}{N_0} = \underbrace{\ln\frac{CA_1}{CA_0}}_{\text{volume}} + \underbrace{\ln\frac{N_1/CA_1}{N_0/CA_0}}_{\text{marge}}$$

Une croissance du bénéfice portée par le **volume** — vendre plus — est la plus
durable. Une croissance portée par la **marge** — gagner plus sur chaque euro
vendu — est plafonnée : une marge ne monte pas indéfiniment. C'est la question
que se posait Steinhardt avant le consensus : la marge de l'an prochain
sera-t-elle celle que les analystes extrapolent ?

## 4.4 — Les huit valeurs

Exercice 2025, dernier publié au 8 octobre 2026, contre la moyenne des exercices
publiés (2022 à 2025) :

| | Marge op. 2025 | Moyenne 2022-2025 | Écart | Résultat net 2025/2024 : volume | + marge |
|---|---|---|---|---|---|
| **AIR.PA** | 7,1 % | 7,4 % | −0,3 pt | +5,9 | +15,1 |
| **MC.PA** | 21,9 % | 24,5 % | **−2,6 pt** | −4,7 | −9,6 |
| **OR.PA** | 20,2 % | 19,9 % | +0,3 pt | +1,3 | −5,8 |
| **SAN.PA** | 20,5 % | 22,1 % | −1,6 pt | +5,3 | **+28,7** |
| **TTE.PA** | 10,9 % | 14,1 % | **−3,1 pt** | −7,0 | −11,2 |
| **BNP.PA** | — | — | — | +4,4 | +0,1 |
| **SU.PA** | 17,5 % | 16,9 % | +0,6 pt | +5,1 | −7,6 |
| **ORA.PA** | 10,3 % | 13,1 % | −2,8 pt | +0,3 | **−147,8** |

Décomposition en points de log.

**Aucune marge n'est au-dessus de sa moyenne de plus de 2 points.** La double
extrapolation du § 4.2 ne se présente donc sur aucune des huit valeurs. Ce n'est
pas un résultat rassurant ni inquiétant : c'est une absence, et elle tient en
partie à la fenêtre. La moyenne de TotalEnergies inclut 2022, année de marges
exceptionnelles ; sa marge 2025 est « basse » contre un sommet, pas contre un
cycle.

**LVMH** perd sur les deux tableaux : moins de ventes (−4,7) et moins de marge
(−9,6). Une marge qui baisse **plus vite** que les ventes, c'est le levier
opérationnel qui joue à l'envers. Avec un consensus 2027 en révision à la baisse
([module 2](02-les-attentes-de-benefices.md)), les trois indicateurs racontent
la même histoire.

**Sanofi** et **Orange** rappellent l'effet de base : +28,7 et −147,8 points de
marge nette en un an ne mesurent pas une rentabilité qui change, mais des
éléments exceptionnels — des dépréciations — qui tombent dans un exercice et pas
dans l'autre. La marge **opérationnelle** de Sanofi est d'ailleurs sous sa
moyenne. La marge nette, plus bas dans le compte de résultat, accumule tous les éléments
non récurrents.

**BNP Paribas** n'a pas de marge opérationnelle au sens de ce module : le
« chiffre d'affaires » d'une banque est son produit net bancaire, et la notion de
marge ne s'y transpose pas. Une cellule vide, pas un zéro — c'est l'invariant du
dépôt, et le [module 3 du cours fondamentaux](../fondamentaux/03-ce-que-la-comptabilite-laisse-au-choix.md)
l'a justifié pour VE/EBITDA.

## 4.5 — Ce que l'indicateur ne dit pas

- **Une marge sous sa moyenne n'annonce pas une remontée.** Le retour à la
  moyenne est une tendance statistique sur des milliers d'entreprises, pas une
  loi pour une entreprise. Une marge peut baisser parce que le modèle économique
  s'est dégradé pour de bon.
- **Quatre exercices ne font pas un cycle.** Un cycle industriel dure de cinq à
  dix ans. « Au-dessus de sa moyenne » signifie ici « au-dessus de sa moyenne
  récente », et la profondeur doit être dite.
- **La marge de l'an prochain est ce qui compte**, et elle n'est pas dans les
  comptes. Elle est dans le consensus, en creux : un BPA attendu en forte hausse
  avec un chiffre d'affaires attendu stable est une hypothèse de marge.

## Exercices

**E4.1.** Une société réalise 1 000 M€ de chiffre d'affaires, avec 600 M€ de
coûts fixes et des coûts variables de 30 % des ventes. Calculer la marge
opérationnelle. Que devient-elle si les ventes montent de 10 % ? De combien a
monté le résultat opérationnel ?

**E4.2.** Le résultat net passe de 200 à 260 M€, le chiffre d'affaires de 2 000
à 2 100 M€. Décomposer en volume et marge (en points de log). Quelle part de la
croissance est plafonnée ?

**E4.3.** Pourquoi la marge **nette** est-elle plus exposée à l'effet de base que
la marge opérationnelle ?

### Corrigés

**E4.1.** Résultat : $1\,000 - 600 - 300 = 100$ M€, marge **10 %**. À 1 100 M€ :
$1\,100 - 600 - 330 = 170$ M€, marge **15,5 %**. Le résultat monte de **70 %**
pour 10 % de ventes : c'est le levier opérationnel.

**E4.2.** Total : $100\ln(260/200) = 26{,}2$. Volume : $100\ln(2\,100/2\,000) = 4{,}9$.
Marge : $26{,}2 - 4{,}9 = 21{,}4$ points (de 10 % à 12,4 %). Plus des quatre
cinquièmes de la croissance viennent de la marge, la part plafonnée.

**E4.3.** Elle se lit tout en bas du compte de résultat, après les dépréciations,
les plus ou moins-values de cession, les charges de restructuration et la
fiscalité. Chacun de ces éléments peut être exceptionnel, et la marge nette les
accumule tous.

## Ce qu'il faut retenir

1. La marge **opérationnelle** se compare à sa propre histoire ou à son secteur,
   jamais d'un secteur à l'autre.
2. Les marges **reviennent à la moyenne** ; le levier opérationnel les fait
   monter vite dans une phase de croissance, et cette hausse s'extrapole.
3. $\ln(N_1/N_0) = $ volume $+$ marge : une croissance portée par la marge est
   plafonnée.
4. Marge haute **et** multiple haut : la double extrapolation, marqueur R2.
   Aucune des huit valeurs ne la présente au 8 octobre 2026.

---

⬅️ [Module 3 — Le prix des attentes](03-le-prix-des-attentes.md) ·
➡️ [Module 5 — Comment la hausse se finance](05-levier-et-dilution.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
