---
name: python-sync
description: Synchronise les scripts Python avec leur markdown miroir. Détecte les modifications des fichiers .md du répertoire python/ et répercute les changements dans le .py correspondant. Utiliser quand l'utilisateur invoque /python-sync, ou après avoir édité un markdown miroir d'un script Python.
---

# python-sync

Le dépôt applique la règle **un `.py` ⇔ un `.md` du même nom**, côte à côte dans
`python/`. Le markdown est le **miroir de l'exécution** du script : il décrit,
dans l'ordre, ce que le script fait réellement. Le markdown fait autorité.

Cette skill propage les modifications du markdown vers le script.

## Procédure

### 1. Détecter les markdown modifiés

```bash
git status --porcelain -- 'python/*.md'
git diff -- 'python/*.md'          # modifications non indexées
git diff --cached -- 'python/*.md' # modifications indexées
```

Si rien n'apparaît, comparer aussi avec le dernier commit qui a touché le `.py`
correspondant (`git log -1 --format=%H -- python/<nom>.py`) : un markdown peut
avoir été modifié puis commité sans que le script suive.

S'il n'y a aucune divergence : le dire et s'arrêter.

### 2. Vérifier l'appariement

Pour chaque `python/<nom>.py`, il doit exister `python/<nom>.md`, et
réciproquement.

- `.py` sans `.md` → créer le markdown miroir à partir du script (§ Format).
- `.md` sans `.py` → **ne pas créer de script en silence** : signaler à
  l'utilisateur et demander si le markdown décrit un nouveau script à écrire.

### 3. Lire le diff et classer chaque changement

Pour chaque markdown modifié, lire le diff **et** le script actuel, puis classer
chaque écart :

- **Reformulation** — le markdown dit la même chose autrement, le script est déjà
  conforme → aucune modification du script.
- **Correction du miroir** — le markdown était faux, le script a raison → corriger
  le markdown, pas le script. Le signaler explicitement.
- **Changement de comportement non ambigu** — le markdown décrit un comportement
  que le script n'a pas encore et il n'existe qu'une seule façon raisonnable de
  l'implémenter → modifier le script.
- **Changement de comportement demandant un arbitrage** — voir § 4.

### 4. Arbitrages : le markdown d'abord

Un changement relève d'un arbitrage dès que plusieurs implémentations sont
défendables : nom d'une colonne ou d'un argument, valeur par défaut, gestion des
`NaN` et des bornes, ordre des colonnes, comportement en cas d'erreur, format de
sortie, rétro-compatibilité du CSV…

Dans ce cas, **dans cet ordre** :

1. Trancher (poser la question à l'utilisateur si le choix l'engage vraiment).
2. **Écrire la décision dans le markdown** — la formulation ambiguë est remplacée
   par la spécification précise retenue.
3. **Seulement ensuite**, modifier le script pour qu'il corresponde au markdown
   mis à jour.

Ne jamais coder d'abord et documenter après.

### 5. Appliquer et vérifier

- Modifier le `.py` pour qu'il corresponde ligne à ligne au déroulé du markdown.
- Messages utilisateur et aide CLI **en français** (convention du dépôt).
- Vérifier la syntaxe : `python -m py_compile python/<nom>.py`.
- Relire le markdown de bout en bout : chaque section doit encore décrire ce que
  le script fait maintenant (numéros d'étapes, formules, colonnes, codes de
  sortie, chemins par défaut).

### 6. Rendre compte

Résumer en français : markdown détectés comme modifiés, changements propagés,
arbitrages tranchés et comment, écarts laissés de côté et pourquoi.

## Format attendu d'un markdown miroir

Reprendre la structure de `python/historique_sbf250.md` :

1. Titre `# <nom>.py — miroir d'exécution` et rôle en une ou deux phrases.
2. Dépendances.
3. Invocation + tableau des arguments CLI (défauts, priorités entre eux).
4. **Déroulé d'exécution** numéroté, dans l'ordre réel du code : une section par
   étape, avec les formules exactes et le traitement des cas limites.
5. Sorties : affichage console (gabarit littéral), fichiers écrits, chemins par
   défaut.
6. Codes de sortie.
7. Constantes et chemins.

Décrire le comportement, pas le code : pas de copie de source, mais des formules,
des noms de colonnes, des valeurs par défaut et des cas limites vérifiables.
