# Module 6 — Le change

**Prérequis :** [module 1](01-le-taux-d-actualisation.md) (§ 1.4, la régression marché compris).
**Ce qu'on établit ici :** par quels canaux un taux de change touche un cours, pourquoi l'exposition mesurée est plus faible que l'exposition supposée, et ce que cela donne sur quatre valeurs du CAC 40.

---

## 6.1 — Trois canaux

Une entreprise qui publie ses comptes en euros et vend en dollars est exposée à
l'EUR/USD par trois canaux :

| Canal | Mécanisme | Effet d'un euro fort |
|---|---|---|
| **Conversion** | les ventes en dollars valent moins d'euros une fois converties | négatif |
| **Compétitivité** | les coûts en euros rendent le produit plus cher face à un concurrent américain | négatif, si les coûts sont en euros |
| **Couverture** | les contrats de change à terme figent le cours sur un ou deux ans | **amortit** les deux premiers |

Le signe attendu pour un exportateur est donc négatif : un euro qui s'apprécie
pèse sur le cours. L'**amplitude**, elle, dépend de la structure des coûts et de
la politique de couverture, deux choses que le cours ne dit pas.

## 6.2 — Le puzzle de l'exposition

Bartram & Bodnar (2007) passent en revue trois décennies d'études. Le constat est
constant : la proportion d'entreprises dont l'exposition au change est
**statistiquement significative** est bien plus faible que la part de leur
activité internationale ne le laisserait prévoir. C'est le « puzzle de
l'exposition au change ».

Trois raisons :

- **la couverture**, qui fait précisément son travail ;
- **la couverture naturelle** : une usine aux États-Unis produit des coûts en
  dollars qui compensent les ventes en dollars ;
- **le change n'est pas un choc isolé** : un euro fort accompagne souvent une
  demande mondiale forte, qui profite aux mêmes exportateurs.

## 6.3 — La mesure sur quatre valeurs

Même régression qu'au [module 1](01-le-taux-d-actualisation.md) (§ 1.4),
marché compris ; $b_F$ est la sensibilité à la variation hebdomadaire de
l'EUR/USD (positive quand l'euro s'apprécie), sur 2008-2025.

| Valeur | Exposition supposée | $b_F$ | $t$ | Survit à Holm ? |
|---|---|---|---|---|
| Airbus | ventes en dollars, coûts en euros | **−0,607** | **−6,16** | ✅ |
| Sanofi | ventes mondiales, forte part américaine | **−0,317** | **−4,30** | ✅ |
| TotalEnergies | pétrole coté en dollars | −0,152 | −2,42 | ❌ |
| LVMH | forte part hors zone euro | +0,115 | +1,69 | ❌ |

*Lecture* : une semaine où l'euro gagne 1 % contre le dollar, Airbus fait, en
moyenne, **0,61 %** de moins que ce que le marché explique.

Airbus est le cas d'école : coûts en euros, prix en dollars, concurrent
américain. Le signe et l'amplitude sont ceux qu'on attend. LVMH, souvent citée
comme l'exposée type, ne montre **aucune** sensibilité mesurable, et son
coefficient a même le mauvais signe. C'est le puzzle, sur une seule valeur : un
groupe qui produit en Europe mais fixe ses prix localement, se couvre, et vend
davantage quand la demande mondiale est forte, ce qui coïncide souvent avec un
euro fort.

## 6.4 — Le signe change aussi pour l'indice

La corrélation annuelle du CAC 40 avec l'EUR/USD (relevé C de
[`mesurer_macro.py`](figures/mesurer_macro.md)) ne garde pas son signe :

| Période | Corrélation |
|---|---|
| 2008-2013 | positive chaque année, jusqu'à **+0,51** (2011) |
| 2014-2017 | négative chaque année, jusqu'à **−0,46** (2016) |
| 2018-2025 | positive chaque année, de +0,02 (2019) à +0,37 (2024) |
| 2008-2025 | **+0,16** |

En 2011, pendant la crise de la dette souveraine, euro et actions européennes
baissaient ensemble : le change était un **baromètre du risque européen**. En
2015-2016, après le lancement des rachats d'actifs de la BCE, un euro faible
soutenait les exportateurs, et les deux évoluaient en sens contraire. **Le même
facteur a changé de rôle**, et une corrélation moyennée sur 18 ans ne décrit
aucune des deux périodes.

## Ce qu'il faut retenir

1. Trois canaux : conversion, compétitivité, couverture ; le troisième amortit
   les deux premiers.
2. L'exposition mesurée est plus faible que l'exposition supposée : c'est le
   puzzle de Bartram & Bodnar.
3. Airbus : **−0,61**, $t = -6{,}16$. LVMH : **rien de mesurable**.
4. Pour l'indice, le signe de la corrélation au change a changé deux fois
   depuis 2008.

---

⬅️ [Module 5 — La croissance : PIB et PMI](05-la-croissance.md) ·
➡️ [Module 7 — Le pétrole](07-le-petrole.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
