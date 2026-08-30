# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Langue

Répondre à l'utilisateur en français. Cela s'applique à tous les échanges (explications, résumés, questions, messages de commit) dans ce dépôt.

## Overview

Single-file Python utility (`python/import_societe.py`) that fetches stock price history for SBF 250 (Paris stock exchange) companies via Yahoo Finance using the `yfinance` library. CLI-driven, no package structure, no tests.

User-facing messages and CLI help are in French — keep that convention in any edits. Paris tickers carry the `.PA` suffix (e.g. `AIR.PA`, `MC.PA`).

## Règle : miroir Markdown des scripts Python

Tout fichier `.py` doit être accompagné d'un fichier `.md` **du même nom**, placé
à côté de lui (ex. `python/import_societe.py` ⇔ `python/import_societe.md`).

Ce markdown est le **miroir de l'exécution** du script : il décrit, dans l'ordre
du déroulement, ce que le script fait réellement — arguments CLI et valeurs par
défaut, étapes de traitement, formules exactes, colonnes produites, affichage
console, fichiers écrits, codes de sortie, cas limites. Il décrit le
comportement, pas le code.

Le markdown fait autorité : lorsqu'une évolution demande un arbitrage (nom d'une
colonne ou d'un argument, valeur par défaut, gestion des `NaN`, format de sortie,
comportement en cas d'erreur…), **mettre le markdown à jour d'abord**, puis
aligner le script dessus. Jamais l'inverse.

La skill `/python-sync` détecte les markdown modifiés et répercute les
changements dans les scripts correspondants.

## Agents

- `chartiste` (`.claude/agents/chartiste.md`) — lit la tendance d'une valeur
  cotée à partir d'un CSV de `docs/raw/quotes/` : droite ajustée, pentes
  d'encadrement (canal de régression et canal par enveloppe convexe), test de
  significativité, ruptures de canal. Ne donne pas de conseil d'investissement.
- `trading` (`.claude/agents/trading.md`) — évalue la performance d'un indice ou
  d'une valeur, calcule alpha et bêta contre un indice de référence (`^FCHI`,
  `^SBF120`), connaît les techniques de sélection et ce qui est calculable depuis
  l'OHLCV, et rend un verdict achat/vente/attente issu d'une règle écrite à
  l'avance. Ne donne pas de conseil d'investissement personnalisé.
- `sorosien` (`.claude/agents/sorosien.md`) — lecture réflexive au sens de Soros :
  cherche un canal de transmission entre cours et fondamentaux, situe la valeur
  dans le cycle boom-bust en huit phases, et répond « aucune séquence réflexive
  identifiable » par défaut. Ne donne pas de conseil d'investissement.

## Setup & run

```bash
pip install yfinance
python python/import_societe.py AIR.PA --periode 5y
python python/import_societe.py AIR.PA --debut 2023-01-01 --fin 2023-12-31 --csv airbus.csv
```

Running with no ticker argument drops into an interactive prompt.

## Architecture

`main()` augments the OHLCV frame with an `INDICE` counter (1, 2, …) and, for each rolling
window `n` in {20, 120} on `Close`: `E_n` (mean), `VAR_n` (population variance, `ddof=0`),
`CORR_n` (correlation with `INDICE`), `VAL_n` (the least-squares fitted line evaluated at the
window's last point), plus a two-sided Student trend test — `T_n`, `P_n` and the signed verdict
`TEND_n` at threshold `--alpha` (default 0.05). Indicator cells stay empty for the first `n-1`
rows (NaN written as empty in CSV).

Functions:
- `recuperer_historique(ticker, periode, debut, fin, intervalle)` — wraps `yf.Ticker(...).history(...)`. Date range (`debut`/`fin`) takes precedence over `periode`. Raises `ValueError` when the result is empty (typically a bad ticker, e.g. missing `.PA` suffix).
- `_beta_incomplete_reg(x, a, b)` and `p_valeur_student(t, ddl)` — the regularised incomplete beta function (Lentz continued fraction) and the two-sided Student p-value, in pure Python so that `yfinance` stays the only dependency. **Do not add `scipy`.**
- `main()` — argparse CLI. CSV export is always written; default path is `docs/raw/quotes/{ticker}_{debut}_{fin}.csv` (directory auto-created), overridable via `--csv`. That directory is gitignored.

The exact formulas, their derivation and every edge case live in `python/import_societe.md`
(the mirror) and in `docs/raw/modele.md` (the proof). Read the mirror before editing the script.
