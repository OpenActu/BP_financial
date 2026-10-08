# Module 7 — Indicateurs 8 et 9 : le monde autour

**Prérequis :** [module 6](06-taux-et-credit.md), les modules [3](../macro/03-l-inflation.md), [5](../macro/05-la-croissance.md), [6](../macro/06-le-change.md) et [12](../macro/12-cas-d-etude-livre-sterling-1992.md) du cours macro, et le [module 3 du cours alpha](../alpha/03-l-horizon-necessaire.md) (horizon et puissance).
**Ce qu'on établit ici :** comment mesurer l'exposition d'une valeur au change, pourquoi trois ans de données ne suffisent pas à l'établir, et comment situer croissance et inflation sans regarder en avant.

---

## 7.1 — Indicateur 8 : le change

Chez Soros, le change est un objet central : la livre sterling en 1992 (le
[module 12 du cours macro](../macro/12-cas-d-etude-livre-sterling-1992.md)), et
le « cercle impérial » des années 1980 qu'il décrit dans *L'Alchimie de la
finance* — un dollar fort attire des capitaux, qui financent le déficit
américain, qui soutient l'activité, qui attire des capitaux, jusqu'au
retournement. Une tendance de change peut être **réflexive** parce que les flux
de capitaux qu'elle attire la renforcent.

Ces flux ne sont pas mesurables avec les sources du dépôt. Ce qui l'est, c'est
l'**exposition** d'une valeur au change, par la régression du
[module 6 du cours macro](../macro/06-le-change.md), le marché compris :

$$r_w = a + b_M\,\text{MARCHÉ}_w + b_F\,\text{EURUSD}_w + e_w$$

`EURUSD` est le prix d'un euro en dollars : quand il monte, l'euro se renforce.
Un $b_F$ **négatif** signifie que la valeur baisse quand l'euro monte — le profil
d'un exportateur qui facture en dollars et produit en euros.

Le script l'estime sur les **156 dernières semaines**, trois ans, en rendements
de cours non ajustés des dividendes contre l'indice nu : même convention des
deux côtés. La constante $a$ n'est pas lue.

## 7.2 — Les huit valeurs, sur trois ans

| | $b_M$ | $b_F$ | $t$ | $p$ |
|---|---|---|---|---|
| **AIR.PA** | 1,14 | **−0,48** | −1,86 | 0,065 |
| **SU.PA** | 1,33 | +0,40 | +1,44 | 0,152 |
| **TTE.PA** | 0,27 | −0,39 | −1,41 | 0,162 |
| **OR.PA** | 0,67 | +0,32 | +1,31 | 0,193 |
| **SAN.PA** | 0,70 | +0,27 | +1,01 | 0,316 |
| **MC.PA** | 1,43 | −0,20 | −0,72 | 0,471 |
| **BNP.PA** | 1,31 | +0,16 | +0,66 | 0,510 |
| **ORA.PA** | 0,14 | +0,12 | +0,51 | 0,612 |

**Aucun $b_F$ n'est significatif**, ni au seuil de 5 % pris isolément, ni a
fortiori après la correction de Holm sur huit tests que le script applique.

Le cours macro trouvait pourtant, sur 2008-2025 (933 semaines), une sensibilité
d'Airbus de **−0,61** avec $t = -6{,}16$, et une sensibilité de Sanofi de
**−0,32**, significative elle aussi. Sur trois ans, Airbus garde le bon signe et
un ordre de grandeur voisin, mais n'est plus significatif ; Sanofi change de
signe.

## 7.3 — Pourquoi trois ans ne suffisent pas

L'erreur type d'un coefficient se lit dans le rapport $b/t$. Pour Airbus :
$0{,}48/1{,}86 = 0{,}26$. Un effet n'est détecté à coup sûr — test bilatéral à
5 %, puissance de 80 % — que s'il dépasse environ **2,8 erreurs types** :

$$\text{EMD} \approx 2{,}8 \times 0{,}26 = 0{,}72$$

Sur 156 semaines, on ne peut donc établir qu'une sensibilité au change supérieure
à **0,7** en valeur absolue — plus forte que celle du plus exportateur des
groupes du CAC 40. L'erreur type décroît comme $1/\sqrt{n}$ : sur 933 semaines,
elle est divisée par $\sqrt{933/156} = 2{,}45$, et l'EMD tombe à **0,30**. C'est
pourquoi le cours macro établissait ce que ce relevé ne peut pas établir.

> 🔑 **Une absence de significativité sur une courte fenêtre n'est pas une
> absence d'effet.** C'est l'**effet minimal détectable**, la notion que le dépôt
> publie avant chaque expérience. Le relevé sur trois ans sert à voir si
> l'exposition a **changé de signe** récemment ; il ne sert pas à l'établir. Pour
> l'établir, il faut la fenêtre longue du cours macro, et la stabilité qu'il
> vérifie sur trois sous-périodes.

Ce que l'indicateur 8 apporte à la lecture de Soros et de Steinhardt est donc
modeste : il dit **quel pari de change** une valeur porte, que l'investisseur le
veuille ou non. Avec un euro qui a perdu 3,9 % face au dollar en un an
(1,1199 au 8 octobre 2026), un exportateur au $b_F$ établi de −0,6 en aura
bénéficié d'environ $0{,}6 \times 3{,}9 = 2{,}3$ points, toutes choses égales par
ailleurs.

## 7.4 — Indicateur 9 : croissance et inflation

| | Dernière valeur | Période | Un an plus tôt |
|---|---|---|---|
| PIB réel de la zone euro, sur un an | **+1,2 %** | 2ᵉ trimestre 2026 | — |
| inflation de la zone euro, sur un an | **3,8 %** | septembre 2026 | 2,2 % |
| croissance nominale approchée | **5,0 %** | | |

Source : Eurostat, lu par `urllib`. La croissance nominale est approchée par la
somme de la croissance réelle et de l'inflation ; le déflateur du PIB, qui est le
terme exact, diffère de l'indice des prix à la consommation.

**La grille des quatre régimes.** Le [module 3 du cours macro](../macro/03-l-inflation.md)
a établi que la relation entre actions et inflation dépend de l'horizon. À court
terme, une grille simple aide à situer le régime :

| | Inflation en baisse | Inflation en hausse |
|---|---|---|
| **Croissance en hausse** | le régime le plus favorable aux actions | croissance qui s'emballe, banque centrale qui resserre |
| **Croissance en baisse** | désinflation, taux qui baissent | stagflation, le régime le plus défavorable |

Au 8 octobre 2026, l'inflation est en nette hausse (de 2,2 % à 3,8 %) et la
croissance réelle modeste. La grille situe le régime entre la case
« resserrement » et la case « stagflation » — sans dire laquelle, car il
faudrait la **tendance** de la croissance, et une seule valeur trimestrielle ne
la donne pas.

**Le lien avec les multiples.** Les bénéfices agrégés ne peuvent croître
durablement plus vite que la croissance nominale de l'économie. C'est le repère
du seuil de **3 %** de croissance implicite du [module 3](03-le-prix-des-attentes.md) :
une croissance nominale de **long terme**, pas celle de l'année. Les 5,0 %
d'aujourd'hui doivent beaucoup à une inflation de 3,8 % qui n'a pas vocation à
durer.

## 7.5 — Le piège des millésimes

Le [module 5 du cours macro](../macro/05-la-croissance.md) l'a établi : le PIB est
publié environ 30 jours après le trimestre en estimation rapide, puis **révisé**
pendant des années. Le script lit la **dernière** version publiée. Pour un
relevé du jour, c'est la bonne : c'est ce que le marché sait aujourd'hui.

> ⚠️ **Pour une date passée, ce n'est plus la bonne.** Reconstituer ce que
> l'indicateur 9 valait au 8 octobre 2023 avec la série d'aujourd'hui, c'est
> utiliser des révisions publiées après 2023 : un regard en avant. Il faudrait
> les **millésimes** — la série telle qu'elle était publiée à chaque date —, que
> la BCE et Eurostat archivent en partie, mais que ce script ne lit pas. C'est
> l'une des raisons pour lesquelles le relevé est un **instantané**, et jamais
> une série.

## Exercices

**E7.1.** Une valeur a $b_F = -0{,}35$ avec $t = -2{,}5$ sur 156 semaines. Calculer
son erreur type et l'EMD. Le coefficient est-il significatif au seuil de 5 % pris
isolément ? Le serait-il encore après Holm sur huit tests, si c'est le plus petit
des huit $p$ ?

**E7.2.** Combien de semaines faudrait-il pour que l'EMD d'Airbus tombe à 0,40,
l'erreur type par semaine restant la même ?

**E7.3.** Classer dans la grille des régimes : croissance réelle de 2,5 % en
hausse, inflation de 1,5 % en baisse. Puis : croissance réelle de −0,5 % en
baisse, inflation de 4 % en hausse.

### Corrigés

**E7.1.** Erreur type $0{,}35/2{,}5 = 0{,}14$, EMD $\approx 0{,}39$. À $t = -2{,}5$ et
153 ddl, $p \approx 0{,}013$ : significatif isolément. Holm compare le plus petit
$p$ à $0{,}05/8 = 0{,}00625$ : **non rejeté**.

**E7.2.** Il faut une erreur type de $0{,}40/2{,}8 = 0{,}143$, soit $0{,}26/0{,}143 = 1{,}82$
fois plus petite, donc $1{,}82^2 = 3{,}3$ fois plus de semaines : environ **515
semaines**, près de dix ans.

**E7.3.** Le premier est le régime le plus favorable. Le second est la
stagflation.

## Ce qu'il faut retenir

1. L'indicateur 8 mesure le **pari de change** qu'une valeur porte ; les flux de
   capitaux, central chez Soros, ne sont pas mesurables ici.
2. Sur 156 semaines, aucune sensibilité au change n'est établie : l'**EMD** y est
   d'environ 0,7, contre 0,3 sur les 933 semaines du cours macro. Une courte
   fenêtre ne réfute rien.
3. L'indicateur 9 situe un **régime** (croissance × inflation) ; au
   8 octobre 2026, une inflation en nette hausse (3,8 %) pour une croissance
   réelle de 1,2 %.
4. Le relevé du jour lit la dernière version publiée ; une date passée exigerait
   les **millésimes**.

---

⬅️ [Module 6 — Le prix et la quantité de l'argent](06-taux-et-credit.md) ·
➡️ [Module 8 — Ce que croient les autres](08-le-positionnement.md) ·
🏠 [Le cours](README.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
