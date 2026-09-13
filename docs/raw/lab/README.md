# Le laboratoire

Une question, mesurée une fois, sur des données déclarées — et le générateur qui
refait la mesure, versionné à côté d'elle.

C'est le troisième objet de `docs/raw/`, et il ne se confond ni avec l'un ni avec
l'autre des deux premiers :

| | Ce que c'est | Ce qui l'autorise à conclure |
|---|---|---|
| `concept/` | le **cours** | une démonstration, ou une simulation dont la recette est publiée |
| `docs/done/experimentation/` | une **expérience** | un protocole écrit **avant** la première séance, et un portefeuille qui la joue |
| `lab/` | une **mesure** | rien de plus que ce qu'elle a mesuré, sur la série qu'elle nomme |

Un document de laboratoire ne joue aucun portefeuille, ne passe aucun ordre, et
ne rend **aucun verdict d'achat ou de vente**. Il prend une question qui se
tranche par le calcul, la calcule, et publie le résultat — y compris quand le
résultat est que la question ne mène nulle part. C'est même le cas le plus utile :
il coûte moins cher ici qu'au milieu d'une expérience.

## Ce qui s'y applique quand même

Tous les invariants du dépôt, sans exception — et trois en particulier.

**Jamais de regard en avant.** Une mesure qui prétend juger une anticipation
sépare explicitement l'**étalonnage** du **hors échantillon**, et publie la
charnière. Aucune quantité datée du jour `d` ne dépend d'une séance postérieure,
échelles de graphique comprises.

**Le générateur est versionné à côté de ce qu'il produit.** Comme les
`journal.py` des expériences et comme
[`generer_figures.py`](../concept/semestre3/canal/figures/generer_figures.md) : un
chiffre qu'on ne peut pas refaire ne peut pas être corrigé. La règle du miroir
markdown s'y applique — tout `.py` a son `.md` du même nom, et c'est le markdown
qui fait autorité.

**Ce qu'une mesure établit, et ce qu'elle n'établit pas, se publient ensemble.**
Une mesure sur une valeur et une fenêtre est une réalisation, pas une loi. Le
document le dit dans son corps, pas en note de bas de page.

## Les documents

| Document | Question | Réponse |
|---|---|---|
| [`largeur-de-bande-fiable.md`](largeur-de-bande-fiable.md) | Quelle longueur de fenêtre donne la bande la plus étroite qui encadre encore les clôtures à venir ? | Une bande honnête est trop large pour servir : 11 % du cours pour la seule séance du lendemain, 30 % à un mois. Mesuré sur LVMH, sur **deux étalonnages** — le second reproduit les optimums de court horizon et réfute ceux de long horizon. |

Les figures et leurs générateurs sont dans [`figures/`](figures/).
