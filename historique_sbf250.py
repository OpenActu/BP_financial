#!/usr/bin/env python3
"""
Récupère l'historique d'un cours de bourse d'une société du SBF 250.

Dépendance :
    pip install yfinance

Utilisation :
    python historique_sbf250.py                       # mode interactif
    python historique_sbf250.py AIR.PA                 # ticker Yahoo Finance
    python historique_sbf250.py AIR.PA --periode 5y    # période
    python historique_sbf250.py AIR.PA --debut 2023-01-01 --fin 2023-12-31
    python historique_sbf250.py AIR.PA --csv airbus.csv

L'historique est toujours enregistré en CSV. Sans --csv, le fichier
est écrit dans docs/raw/quotes/, sous un nom dérivé du ticker et de la
plage de dates (le répertoire est créé si besoin).

Les valeurs françaises de la place de Paris se terminent par le suffixe ".PA".
Exemples : Airbus -> AIR.PA, TotalEnergies -> TTE.PA, LVMH -> MC.PA,
           Sanofi -> SAN.PA, BNP Paribas -> BNP.PA, Air Liquide -> AI.PA.
"""

import argparse
import sys
from pathlib import Path

import yfinance as yf

REPERTOIRE_CSV_DEFAUT = Path("docs/raw/quotes")


def recuperer_historique(ticker, periode="1y", debut=None, fin=None, intervalle="1d"):
    """Retourne un DataFrame pandas avec l'historique du cours."""
    action = yf.Ticker(ticker)

    if debut or fin:
        hist = action.history(start=debut, end=fin, interval=intervalle)
    else:
        hist = action.history(period=periode, interval=intervalle)

    if hist.empty:
        raise ValueError(
            f"Aucune donnée pour « {ticker} ». "
            "Vérifiez le ticker (les valeurs de Paris finissent par .PA, ex : AIR.PA)."
        )
    return hist


def main():
    parser = argparse.ArgumentParser(
        description="Historique d'un cours de bourse d'une société du SBF 250 (via Yahoo Finance)."
    )
    parser.add_argument(
        "ticker",
        nargs="?",
        help="Ticker Yahoo Finance, ex : AIR.PA, MC.PA, TTE.PA",
    )
    parser.add_argument(
        "--periode",
        default="1y",
        help="Période : 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max (défaut : 1y)",
    )
    parser.add_argument("--debut", help="Date de début AAAA-MM-JJ (prioritaire sur --periode)")
    parser.add_argument("--fin", help="Date de fin AAAA-MM-JJ")
    parser.add_argument(
        "--intervalle",
        default="1d",
        help="Intervalle : 1d,1wk,1mo,1h... (défaut : 1d)",
    )
    parser.add_argument(
        "--csv",
        help=(
            "Chemin du fichier CSV de sortie. Par défaut : "
            "docs/raw/quotes/{ticker}_{debut}_{fin}.csv"
        ),
    )
    args = parser.parse_args()

    ticker = args.ticker or input("Ticker (ex AIR.PA) : ").strip()
    if not ticker:
        print("Aucun ticker fourni.", file=sys.stderr)
        sys.exit(1)

    try:
        hist = recuperer_historique(
            ticker,
            periode=args.periode,
            debut=args.debut,
            fin=args.fin,
            intervalle=args.intervalle,
        )
    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

    hist.insert(0, "INDICE", range(1, len(hist) + 1))

    for n in (20, 120):
        fenetre = hist["Close"].rolling(window=n, min_periods=n)
        hist[f"E_{n}"] = fenetre.mean()
        hist[f"VAR_{n}"] = fenetre.var()
        hist[f"CORR_{n}"] = fenetre.corr(hist["INDICE"])
        hist[f"VAL_{n}"] = (
            hist[f"E_{n}"] + (3 * hist[f"VAR_{n}"]) ** 0.5 * hist[f"CORR_{n}"]
        )

    hist["CURR"] = 100.0 * hist["Close"] / hist["Close"].iloc[0]

    ratio = hist["Close"] / hist["Close"].shift(1)
    achete = hist["VAL_120"] < hist["VAL_20"]
    multiplicateur = ratio.where(achete, 1.0)
    multiplicateur.iloc[0] = 1.0
    hist["BUY_120"] = 100.0 * multiplicateur.cumprod()

    cols = [
        c
        for c in [
            "INDICE",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "E_20",
            "VAR_20",
            "CORR_20",
            "VAL_20",
            "E_120",
            "VAR_120",
            "CORR_120",
            "VAL_120",
            "CURR",
            "BUY_120",
        ]
        if c in hist.columns
    ]
    apercu = hist[cols].round(2)

    print(f"\nHistorique de {ticker} — {len(hist)} séances")
    print(f"Du {hist.index.min().date()} au {hist.index.max().date()}\n")
    print(apercu.to_string())

    dernier = hist["Close"].iloc[-1]
    premier = hist["Close"].iloc[0]
    variation = (dernier / premier - 1) * 100
    print(f"\nClôture initiale : {premier:.2f}")
    print(f"Clôture finale   : {dernier:.2f}")
    print(f"Variation        : {variation:+.2f} %")

    debut_str = hist.index.min().date().isoformat()
    fin_str = hist.index.max().date().isoformat()
    if args.csv:
        chemin_csv = Path(args.csv)
    else:
        nom = f"{ticker.replace('.', '_')}_{debut_str}_{fin_str}.csv"
        chemin_csv = REPERTOIRE_CSV_DEFAUT / nom
    chemin_csv.parent.mkdir(parents=True, exist_ok=True)
    hist.to_csv(chemin_csv)
    print(f"\nHistorique enregistré dans : {chemin_csv}")


if __name__ == "__main__":
    main()
