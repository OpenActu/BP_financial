# Module 2 — La politique monétaire

**Prérequis :** [module 1](01-le-taux-d-actualisation.md).
**Ce qu'on établit ici :** qu'une décision de banque centrale ne fait bouger les cours que par sa part **inattendue**, comment on isole cette part, et pourquoi ce dépôt ne peut pas la mesurer.

---

## 2.1 — Une décision attendue est déjà dans les prix

Le jour où la BCE baisse son taux de 25 points de base, les journaux titrent sur
la baisse, et le CAC 40 monte ou baisse. La tentation est de relier les deux. Elle
néglige un fait : **si la baisse était attendue, elle était déjà dans les
cours** depuis des semaines. Les marchés de taux à court terme la valorisaient, et
les actions avec eux.

Écrivons la décision $i$ comme la somme de ce qui était attendu et de ce qui ne
l'était pas :

$$\Delta i = \underbrace{\mathbb E[\Delta i \mid \text{veille}]}_{\text{attendu}} + \underbrace{\Delta i^{\text{surprise}}}_{\text{inattendu}}$$

> 🔑 **Seule la surprise est une information nouvelle, donc seule elle peut
> déplacer un prix.** Une baisse de 25 pb attendue à 25 pb est une non-nouvelle ;
> une baisse de 25 pb attendue à 50 pb est une **mauvaise** nouvelle pour les
> marchés, bien que ce soit une baisse.

## 2.2 — Mesurer une surprise

Il faut une **attente datée**, c'est-à-dire un prix de marché observé juste avant
l'annonce. Kuttner (2001) la tire des contrats à terme sur le taux des fonds
fédéraux : la variation de leur prix dans une fenêtre étroite autour de l'annonce
est la surprise.

Bernanke & Kuttner (2005) appliquent cette mesure aux actions américaines : une
**baisse surprise de 25 pb** du taux directeur s'accompagne d'une hausse d'environ
**1 %** de l'indice le jour de l'annonce. La réponse à la partie **attendue** est
indiscernable de zéro.

Pour la zone euro, Altavilla, Brugnolini, Gürkaynak, Motto & Ragusa (2019)
publient une base de surprises BCE mesurées en **fenêtres de quelques dizaines de
minutes** autour du communiqué, puis de la conférence de presse. Ils montrent que
la surprise n'a pas une seule dimension : l'annonce déplace le taux du jour, mais
aussi le **chemin** futur attendu (Gürkaynak, Sack & Swanson 2005), et les deux
n'agissent pas de la même façon sur les actions.

## 2.3 — Pourquoi la fenêtre doit être étroite

Sur une journée entière, bien d'autres informations arrivent : statistiques,
résultats d'entreprises, nouvelles géopolitiques. Plus la fenêtre est large, plus
la surprise monétaire se noie dans ce bruit.

| Fenêtre | Ce qu'on mesure |
|---|---|
| 30 minutes autour du communiqué | presque uniquement la décision |
| la séance | la décision, plus tout le reste de la journée |
| la semaine | le bruit l'emporte |

C'est l'inverse du réflexe habituel : ici, **on gagne à réduire l'échantillon
dans le temps**, parce que ce qu'on retire est du bruit, pas du signal.

## 2.4 — Pourquoi ce n'est pas mesurable ici

Trois pièces manquent au dépôt :

| Il faudrait | Ce que le dépôt a |
|---|---|
| des cours **intrajournaliers** autour de chaque annonce | des clôtures quotidiennes |
| une attente de marché datée (contrats à terme sur taux courts) | rien de tel sur Yahoo pour la zone euro |
| le calendrier des réunions de la BCE | aucune source déclarée |

Une étude en clôtures quotidiennes, faite avec ce qu'on a, ne mesurerait pas la
réaction à la politique monétaire : elle mesurerait la réaction à **tout ce qui
s'est passé ces jours-là**. Le cours s'arrête donc à la méthode.

> ⚠️ **« Les marchés ont monté le jour de la baisse de taux » n'est pas une
> mesure.** Sans l'attente de la veille, on ne sait pas si la baisse était une
> surprise, ni dans quel sens.

## Ce qu'il faut retenir

1. Une décision de banque centrale ne déplace les cours que par sa **surprise**.
2. La surprise se mesure par un prix de marché pris **juste avant** l'annonce,
   dans une fenêtre de quelques minutes.
3. Ordre de grandeur (États-Unis) : **−25 pb surprise ≈ +1 %** sur l'indice.
4. Le dépôt n'a ni les données intrajournalières ni les attentes datées : pas de
   mesure ici, seulement la méthode.

---

⬅️ [Module 1 — Le taux d'actualisation](01-le-taux-d-actualisation.md) ·
➡️ [Module 3 — L'inflation](03-l-inflation.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
