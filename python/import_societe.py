#!/usr/bin/env python3
"""
Récupère l'historique d'un cours de bourse d'une société du SBF 250.

Dépendance :
    pip install yfinance

Utilisation :
    python python/import_societe.py                       # mode interactif
    python python/import_societe.py AIR.PA                # ticker Yahoo Finance
    python python/import_societe.py AIR.PA --periode 5y   # période
    python python/import_societe.py AIR.PA --debut 2023-01-01 --fin 2023-12-31
    python python/import_societe.py AIR.PA --csv airbus.csv
    python python/import_societe.py AIR.PA --alpha 0.01   # test plus exigeant

L'historique est toujours enregistré en CSV. Sans --csv, le fichier
est écrit dans docs/raw/quotes/, sous un nom dérivé du ticker et de la
plage de dates (le répertoire est créé si besoin).

Les valeurs françaises de la place de Paris se terminent par le suffixe ".PA".
Exemples : Airbus -> AIR.PA, TotalEnergies -> TTE.PA, LVMH -> MC.PA,
           Sanofi -> SAN.PA, BNP Paribas -> BNP.PA, Air Liquide -> AI.PA.
"""

import argparse
import math
import sys
from pathlib import Path

import yfinance as yf

REPERTOIRE_CSV_DEFAUT = Path("docs/raw/quotes")


def _beta_incomplete_reg(x, a, b):
    """Fonction bêta incomplète régularisée I_x(a, b), par fraction continue.

    Évaluation par l'algorithme de Lentz. La relation de symétrie
    I_x(a, b) = 1 - I_{1-x}(b, a) est appliquée quand x > (a+1)/(a+b+2),
    domaine où la fraction continue converge mal.
    """
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _beta_incomplete_reg(1.0 - x, b, a)

    prefacteur = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log1p(-x)
    )

    minuscule = 1e-300
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1.0)
    if abs(d) < minuscule:
        d = minuscule
    d = 1.0 / d
    h = d

    for m in range(1, 301):
        m2 = 2 * m
        for terme in (
            m * (b - m) * x / ((a + m2 - 1.0) * (a + m2)),
            -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1.0)),
        ):
            d = 1.0 + terme * d
            if abs(d) < minuscule:
                d = minuscule
            c = 1.0 + terme / c
            if abs(c) < minuscule:
                c = minuscule
            d = 1.0 / d
            ecart = d * c
            h *= ecart
        if abs(ecart - 1.0) < 1e-14:
            break

    return prefacteur * h / a


def p_valeur_student(t, ddl):
    """p-valeur bilatérale Pr(|T| > |t|) pour une Student à `ddl` degrés de liberté."""
    if t is None or math.isnan(t):
        return float("nan")
    if math.isinf(t):
        return 0.0
    return _beta_incomplete_reg(ddl / (ddl + t * t), ddl / 2.0, 0.5)


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
        "--alpha",
        type=float,
        default=0.05,
        help="Seuil du test de tendance bilatéral (défaut : 0.05)",
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
        hist[f"VAR_{n}"] = fenetre.var(ddof=0)
        hist[f"CORR_{n}"] = fenetre.corr(hist["INDICE"])
        # Droite ajustée f(t) = E(V) + phi(V)(2t - n - 1) évaluée à t = n,
        # avec phi(V) = CORR * sqrt(3 * VAR / (n^2 - 1)) — cf. le modèle,
        # docs/raw/concept/modele/07-droite-ajustee.md.
        hist[f"VAL_{n}"] = hist[f"E_{n}"] + hist[f"CORR_{n}"] * (n - 1) * (
            3 * hist[f"VAR_{n}"] / (n**2 - 1)
        ) ** 0.5

        # Test bilatéral de tendance H0 : r = 0, statistique de Student à n-2
        # degrés de liberté — docs/raw/concept/modele/08-test-de-tendance.md.
        ddl = n - 2
        rho = hist[f"CORR_{n}"]
        hist[f"T_{n}"] = rho * (ddl / (1.0 - rho**2)) ** 0.5
        hist[f"P_{n}"] = hist[f"T_{n}"].map(lambda t: p_valeur_student(t, ddl))
        significatif = hist[f"P_{n}"] < args.alpha
        hist[f"TEND_{n}"] = (significatif & (rho > 0)).astype(int) - (
            significatif & (rho < 0)
        ).astype(int)

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
            "T_20",
            "P_20",
            "TEND_20",
            "E_120",
            "VAR_120",
            "CORR_120",
            "VAL_120",
            "T_120",
            "P_120",
            "TEND_120",
        ]
        if c in hist.columns
    ]
    arrondis = {c: (4 if c.startswith("P_") else 2) for c in cols}
    apercu = hist[cols].round(arrondis)

    print(f"\nHistorique de {ticker} — {len(hist)} séances")
    print(f"Du {hist.index.min().date()} au {hist.index.max().date()}")
    print(f"Test de tendance bilatéral au seuil alpha = {args.alpha}\n")
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
