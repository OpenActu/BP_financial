# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Langue

Répondre à l'utilisateur en français. Cela s'applique à tous les échanges (explications, résumés, questions, messages de commit) dans ce dépôt.

## Overview

Single-file Python utility (`historique_sbf250.py`) that fetches stock price history for SBF 250 (Paris stock exchange) companies via Yahoo Finance using the `yfinance` library. CLI-driven, no package structure, no tests.

User-facing messages and CLI help are in French — keep that convention in any edits. Paris tickers carry the `.PA` suffix (e.g. `AIR.PA`, `MC.PA`).

## Setup & run

```bash
pip install yfinance
python historique_sbf250.py AIR.PA --periode 5y
python historique_sbf250.py AIR.PA --debut 2023-01-01 --fin 2023-12-31 --csv airbus.csv
```

Running with no ticker argument drops into an interactive prompt.

## Architecture

Two functions:
- `recuperer_historique(ticker, periode, debut, fin, intervalle)` — wraps `yf.Ticker(...).history(...)`. Date range (`debut`/`fin`) takes precedence over `periode`. Raises `ValueError` when the result is empty (typically a bad ticker, e.g. missing `.PA` suffix).
- `main()` — argparse CLI. Augments the OHLCV frame with an `INDICE` counter (1, 2, …) and rolling 20-day indicators on `Close` (`E_20` mean, `VAR_20` variance, `CORR_20` correlation with `INDICE`, `VAL_20 = E_20 + sqrt(3·VAR_20)·CORR_20`). Indicator cells stay empty for the first 19 rows (NaN written as empty in CSV). CSV export is always written; default path is `docs/raw/quotes/{ticker}_{debut}_{fin}.csv` (directory auto-created), overridable via `--csv`.
