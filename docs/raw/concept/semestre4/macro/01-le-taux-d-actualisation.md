# Module 1 — Le taux d'actualisation ⭐

**Prérequis :** [module 4 du cours fondamentaux](../fondamentaux/04-un-ratio-n-existe-que-relatif.md) (Gordon), [module 2 du cours alpha](../alpha/02-le-calcul-et-ses-erreurs-types.md) (régression sur un facteur).
**Ce qu'on établit ici :** pourquoi un taux d'intérêt entre dans le prix de toute action, pourquoi certaines y sont plus sensibles que d'autres, et ce que mesure, sur des données réelles, une sensibilité au taux.

---

## 1.1 — Le canal : l'actualisation

Une action donne droit à une suite de dividendes futurs. Son prix est la valeur
présente de cette suite, actualisée à un taux $r$. Si le dividende $D$ croît à un
taux constant $g < r$, la somme se ferme (Gordon) :

$$P = \frac{D}{r - g}$$

Le taux d'actualisation est la somme d'un **taux sans risque** $r_f$ et d'une
**prime de risque** $\pi$ : $r = r_f + \pi$. Toute hausse du taux sans risque, à
prime et croissance inchangées, fait donc baisser le prix.

*Exemple* : $D = 3$ €, $r = 8\,\%$, $g = 4\,\%$ donnent $P = 3/0{,}04 = 75$ €. Si
$r_f$ monte d'un point, $r = 9\,\%$ et $P = 3/0{,}05 = 60$ € : **−20 %**.

## 1.2 — La duration d'une action

La sensibilité relative du prix au taux se calcule en dérivant :

$$D_{\text{action}} = -\frac{1}{P}\frac{\partial P}{\partial r} = \frac{1}{r - g}$$

C'est la **duration** de l'action, au sens où l'on parle de celle d'une
obligation. Elle vaut ici $1/0{,}04 = 25$ ans. Refaisons le calcul avec une
croissance plus forte, $g = 6\,\%$ :

| | $g = 4\,\%$ | $g = 6\,\%$ |
|---|---|---|
| Prix à $r = 8\,\%$ | 75 € | 150 € |
| Prix à $r = 9\,\%$ | 60 € | 100 € |
| Variation | **−20 %** | **−33 %** |
| Duration $1/(r-g)$ | 25 ans | 50 ans |

> 🔑 **Plus la croissance attendue est forte, plus la valeur est lointaine, et
> plus elle est sensible au taux.** C'est l'argument qui fait dire que les
> valeurs de croissance « souffrent » quand les taux montent. Dechow, Sloan &
> Soliman (2004) mesurent cette duration implicite ; Lettau & Wachter (2007) en
> font une explication de la prime *value*.

Le modèle néglige un fait qui compte : **le taux ne bouge presque jamais seul.**
Une hausse de taux accompagne souvent une révision à la hausse de la croissance,
donc de $g$. Si $r$ et $g$ montent ensemble, $r - g$ bouge peu, et le prix aussi.
C'est pourquoi la sensibilité mesurée s'écarte de celle que la formule annonce.

## 1.3 — Les secteurs : le signe est connu, pas l'amplitude

Le canal d'actualisation touche toutes les actions. Deux familles ont un canal
**supplémentaire** :

| Famille | Canal propre | Signe attendu |
|---|---|---|
| Foncières, services aux collectivités | flux stables, dette élevée : se comportent comme des **quasi-obligations** | négatif |
| Banques | la marge d'intérêt s'élargit quand les taux longs montent | **positif** (English, Van den Heuvel & Zakrajšek 2018) |

Le signe est bien documenté ; l'amplitude, elle, dépend de la couverture du
risque de taux au bilan de chaque entreprise, et ne se devine pas.

## 1.4 — Ce que mesure $b_{\text{TAUX}}$

On estime, en rendements hebdomadaires sur 2008-2025
([module 11](11-exemple-chiffre-huit-valeurs.md)) :

$$r_{i,w} = a + b_M\,r^{\text{CAC}}_w + b_{\text{TAUX}}\,\Delta y_w + \dots + e_w$$

où $\Delta y_w$ est la variation hebdomadaire du taux à 10 ans, **en points**.
Deux choix à comprendre :

- **On régresse sur la variation, pas sur le niveau.** Le niveau du taux dérive
  sur des décennies ; le régresser contre un rendement produirait une corrélation
  fallacieuse, le défaut des séries non stationnaires.
- **Le marché est dans la régression.** $b_{\text{TAUX}}$ mesure donc la
  sensibilité **au-delà** de celle que le titre hérite de l'indice. Sans $b_M$,
  on mesurerait surtout la corrélation de l'indice lui-même avec les taux
  ([module 9](09-la-correlation-actions-obligations.md)).

**Résultat sur quatre valeurs** (le tableau complet est au module 11) :

| Valeur | Canal attendu | $b_{\text{TAUX}}$ | $t$ | Survit à Holm ? |
|---|---|---|---|---|
| BNP Paribas | banque, **positif** | **+0,0713** | **+7,15** | ✅ |
| L'Oréal | défensive, valorisation élevée | **−0,0385** | **−6,24** | ✅ |
| Klépierre | foncière, **négatif** | −0,0170 | −1,36 | ❌ |
| LVMH | « croissance » | −0,0042 | −0,59 | ❌ |

*Lecture* : une semaine où le taux à 10 ans monte de 25 points de base
($\Delta y = 0{,}25$) s'accompagne, toutes choses égales par ailleurs, d'un
rendement de BNP Paribas supérieur de $0{,}0713 \times 0{,}25 = 1{,}8\,\%$ à ce que
le marché explique, et de celui de L'Oréal inférieur de $0{,}96\,\%$.

Trois leçons :

1. **Le signe de la banque est retrouvé, et nettement.** C'est le deuxième lien
   le plus fort des 24 testés au module 11, après TotalEnergies au Brent.
2. **La foncière ne sort pas sur toute la période.** Klépierre ne devient
   sensible qu'en 2022-2025 ($t = -3{,}05$) : la sensibilité dépend du régime, et
   c'est l'objet du [module 9](09-la-correlation-actions-obligations.md).
3. **« Valeur de croissance » n'est pas une mesure.** LVMH, qu'on range
   spontanément parmi elles, ne montre **aucune** sensibilité propre au taux.
   L'Oréal, rangée parmi les « défensives », en montre une forte. Le classement
   intuitif ne remplace pas la régression.

> ⚠️ **Le taux utilisé est américain.** Aucun taux de la zone euro n'est
> exploitable sur la source. $b_{\text{TAUX}}$ mesure la sensibilité au taux
> américain, qui est corrélé au taux européen sans lui être égal : un lien au
> Bund serait vraisemblablement plus fort, et on ne peut pas le vérifier ici.

## Ce qu'il faut retenir

1. Le taux entre dans le prix par l'actualisation : $P = D/(r-g)$.
2. La duration d'une action vaut $1/(r-g)$ : plus la croissance est forte, plus
   le prix est sensible au taux, **en théorie**.
3. On mesure la sensibilité sur les **variations** de taux, marché compris.
4. Sur 2008-2025, le signe bancaire est retrouvé ($t = +7{,}15$) ; l'étiquette
   « croissance » de LVMH ne l'est pas ($t = -0{,}59$).

---

🏠 [Le cours](README.md) ·
➡️ [Module 2 — La politique monétaire](02-la-politique-monetaire.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
