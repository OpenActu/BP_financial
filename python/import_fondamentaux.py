#!/usr/bin/env python3
"""
Indicateurs fondamentaux et de marché d'une ou plusieurs valeurs, via Yahoo Finance.

Complément de import_societe.py, qui ne rend que de l'OHLCV : valorisation
(PER, P/B, VE/EBITDA, rendement du FCF), rentabilité (ROE, marges), structure
(dette/EBITDA), taille (capitalisation, flottant) et première limite du carnet.

Dépendance :
    yfinance

Utilisation :
    python python/import_fondamentaux.py AIR.PA
    python python/import_fondamentaux.py AIR.PA MC.PA OR.PA SAN.PA
    python python/import_fondamentaux.py AIR.PA --csv airbus_fonda.csv
    python python/import_fondamentaux.py AIR.PA --json

La PROFONDEUR du carnet d'ordres n'est pas accessible par Yahoo Finance : la
source expose au mieux la limite 1 (meilleur acheteur, meilleur vendeur). Les
limites 2 à 10 relèvent des données de niveau 2, payantes chez Euronext ou un
courtier. Ce script ne produit donc aucune colonne de profondeur.

Toute valeur est reprise de la source ou calculée depuis ses composants. Quand ni
le ratio ni ses composants ne sont disponibles, la cellule reste vide.
"""

import argparse
import csv
import json
import math
import sys
from datetime import date
from pathlib import Path

import yfinance as yf

REPERTOIRE_DEFAUT = Path("docs/raw/fondamentaux")
ARCHIVE = REPERTOIRE_DEFAUT / "archive.csv"
TYPES_SANS_FONDAMENTAUX = {"INDEX", "ETF", "CURRENCY", "MUTUALFUND"}

COLONNES = [
    "TICKER", "NOM", "DEVISE", "SECTEUR", "TYPE", "DATE", "COURS",
    "PER", "PER_PREV", "P_B", "VE_EBITDA", "REND_FCF",
    "ROE", "MARGE_BRUTE", "MARGE_OP", "MARGE_NETTE", "DETTE_EBITDA",
    "CAPI", "VE", "EBITDA", "DETTE", "FCF", "ACTIONS", "FLOTTANT", "FLOTTANT_PCT",
    "BID", "ASK", "BID_TAILLE", "ASK_TAILLE", "SPREAD", "SPREAD_PCT",
    "VOLUME", "VOLUME_MOY_3M",
]

DECIMALES = {
    "COURS": 4, "BID": 4, "ASK": 4, "SPREAD": 4,
    "PER": 2, "PER_PREV": 2, "P_B": 2, "VE_EBITDA": 2, "DETTE_EBITDA": 2,
    "REND_FCF": 2, "ROE": 2, "MARGE_BRUTE": 2, "MARGE_OP": 2, "MARGE_NETTE": 2,
    "FLOTTANT_PCT": 2, "SPREAD_PCT": 2,
}


def _nombre(valeur):
    """Rend un float utilisable, ou None : ni chaîne, ni booléen, ni NaN."""
    if valeur is None or isinstance(valeur, bool):
        return None
    try:
        x = float(valeur)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) else x


def _ratio(direct, numerateur, denominateur):
    """Champ direct s'il existe, sinon le calcul, sinon None.

    Le dénominateur doit être strictement positif : un multiple d'EBITDA négatif
    n'a pas de sens économique et ne doit pas être écrit.
    """
    valeur = _nombre(direct)
    if valeur is not None:
        return valeur
    num, den = _nombre(numerateur), _nombre(denominateur)
    if num is None or den is None or den <= 0:
        return None
    return num / den


def _pourcentage(valeur):
    """Fraction de la source (0,2319) en pourcentage (23,19)."""
    x = _nombre(valeur)
    return None if x is None else 100 * x


def _carnet(info):
    """Limite 1 du carnet et spread. Hors séance, la source rend 0.0 : c'est absent.

    Rend le dictionnaire des colonnes et un avertissement éventuel.
    """
    bid, ask = _nombre(info.get("bid")), _nombre(info.get("ask"))
    if bid is not None and bid <= 0:
        bid = None
    if ask is not None and ask <= 0:
        ask = None

    # une taille nulle n'est pas une quantité, c'est une absence de cotation
    tailles = {}
    for colonne, champ in (("BID_TAILLE", "bidSize"), ("ASK_TAILLE", "askSize")):
        taille = _nombre(info.get(champ))
        tailles[colonne] = None if taille is None or taille <= 0 else taille

    colonnes = {"BID": bid, "ASK": ask, "SPREAD": None, "SPREAD_PCT": None, **tailles}
    if bid is None or ask is None:
        return colonnes, "carnet indisponible — bid ou ask absent (hors séance ?)"
    if ask < bid:
        return colonnes, "carnet croisé (ask < bid), artefact de données différées"
    colonnes["SPREAD"] = ask - bid
    colonnes["SPREAD_PCT"] = 100 * (ask - bid) / ((ask + bid) / 2)
    return colonnes, None


def recuperer_fondamentaux(ticker, avec_carnet=True):
    """Interroge Yahoo pour un ticker. Rend (colonnes, composants, avertissements)."""
    avertissements = []
    try:
        info = yf.Ticker(ticker).info or {}
    except Exception as erreur:  # réseau, ticker rejeté, réponse illisible
        return (
            {"TICKER": ticker, "DATE": date.today().isoformat()},
            {},
            [f"{ticker} : échec de la récupération ({erreur.__class__.__name__})"],
        )

    quote_type = info.get("quoteType")
    cours = _ratio(info.get("currentPrice"), None, None)
    if cours is None:
        cours = _ratio(info.get("regularMarketPrice"), None, None)
    if cours is None:
        cours = _ratio(info.get("previousClose"), None, None)

    if not info.get("shortName") and cours is None:
        avertissements.append(f"{ticker} : aucune donnée — suffixe de place manquant ?")

    colonnes = {
        "TICKER": ticker,
        "NOM": info.get("shortName"),
        "DEVISE": info.get("currency"),
        "SECTEUR": info.get("sector"),
        "TYPE": quote_type,
        "DATE": date.today().isoformat(),
        "COURS": cours,
        "VOLUME": _nombre(info.get("volume")),
        "VOLUME_MOY_3M": _nombre(info.get("averageDailyVolume3Month")),
    }

    if quote_type in TYPES_SANS_FONDAMENTAUX:
        avertissements.append(f"{ticker} : {quote_type}, sans fondamentaux")
    else:
        capi = _nombre(info.get("marketCap"))
        actions = _nombre(info.get("sharesOutstanding"))
        ebitda = _nombre(info.get("ebitda"))
        valeur_comptable = _nombre(info.get("bookValue"))
        colonnes.update(
            {
                "PER": _ratio(info.get("trailingPE"), cours, info.get("trailingEps")),
                "PER_PREV": _ratio(info.get("forwardPE"), cours, info.get("forwardEps")),
                "P_B": _ratio(
                    info.get("priceToBook"),
                    capi,
                    valeur_comptable * actions
                    if valeur_comptable is not None and actions is not None
                    else None,
                ),
                "VE_EBITDA": _ratio(
                    info.get("enterpriseToEbitda"), info.get("enterpriseValue"), ebitda
                ),
                "REND_FCF": (
                    None
                    if _ratio(None, info.get("freeCashflow"), capi) is None
                    else 100 * _ratio(None, info.get("freeCashflow"), capi)
                ),
                "ROE": _pourcentage(info.get("returnOnEquity")),
                "MARGE_BRUTE": _pourcentage(info.get("grossMargins")),
                "MARGE_OP": _pourcentage(info.get("operatingMargins")),
                "MARGE_NETTE": _pourcentage(info.get("profitMargins")),
                "DETTE_EBITDA": _ratio(None, info.get("totalDebt"), ebitda),
                "CAPI": capi,
                "VE": _nombre(info.get("enterpriseValue")),
                "EBITDA": ebitda,
                "DETTE": _nombre(info.get("totalDebt")),
                "FCF": _nombre(info.get("freeCashflow")),
                "ACTIONS": actions,
                "FLOTTANT": _nombre(info.get("floatShares")),
                "FLOTTANT_PCT": (
                    None
                    if _ratio(None, info.get("floatShares"), actions) is None
                    else 100 * _ratio(None, info.get("floatShares"), actions)
                ),
            }
        )

    if avec_carnet:
        colonnes_carnet, avertissement = _carnet(info)
        colonnes.update(colonnes_carnet)
        if avertissement:
            avertissements.append(f"{ticker} : {avertissement}")

    composants = {
        c: info.get(c)
        for c in (
            "trailingPE", "forwardPE", "trailingEps", "forwardEps", "priceToBook",
            "bookValue", "enterpriseToEbitda", "enterpriseValue", "ebitda",
            "totalDebt", "freeCashflow", "returnOnEquity", "grossMargins",
            "operatingMargins", "profitMargins", "marketCap", "sharesOutstanding",
            "floatShares", "bid", "ask", "bidSize", "askSize",
        )
        if info.get(c) is not None
    }
    return colonnes, composants, avertissements


def archiver(lignes):
    """Ajoute les lignes du jour a l'archive, sans jamais dupliquer (TICKER, DATE).

    L'archive est le seul fichier regenerable de nulle part : on n'y ecrase rien.
    """
    deja = set()
    if ARCHIVE.exists():
        with ARCHIVE.open(encoding="utf-8-sig", newline="") as f:
            for ligne in csv.DictReader(f):
                deja.add((ligne.get("TICKER"), ligne.get("DATE")))

    nouvelles = [l for l in lignes if (l.get("TICKER"), l.get("DATE")) not in deja]
    for l in lignes:
        if (l.get("TICKER"), l.get("DATE")) in deja:
            print(f"{l.get('TICKER')} : deja archive au {l.get('DATE')}, ignore")

    if not nouvelles:
        return 0
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    premiere = not ARCHIVE.exists()
    with ARCHIVE.open("a", encoding="utf-8-sig", newline="") as f:
        redacteur = csv.writer(f)
        if premiere:
            redacteur.writerow(COLONNES)
        for ligne in nouvelles:
            redacteur.writerow([formater(ligne.get(c), c) for c in COLONNES])
    return len(nouvelles)


def formater(valeur, colonne):
    """Arrondi à l'écriture. Chaîne vide si la valeur manque — jamais nan ni 0."""
    if valeur is None:
        return ""
    if isinstance(valeur, str):
        return valeur
    decimales = DECIMALES.get(colonne, 0)
    return f"{valeur:.{decimales}f}"


def abreger(x, decimales=2):
    """Md / M / k, pour la console uniquement."""
    if x is None:
        return "—"
    for seuil, suffixe in ((1e9, " Md"), (1e6, " M"), (1e3, " k")):
        if abs(x) >= seuil:
            return f"{x / seuil:.{decimales}f}{suffixe}"
    return f"{x:.{decimales}f}"


def main():
    parser = argparse.ArgumentParser(
        description="Indicateurs fondamentaux et de marché d'une ou plusieurs valeurs "
        "(via Yahoo Finance). La profondeur du carnet n'est pas accessible par cette source."
    )
    parser.add_argument(
        "tickers",
        nargs="*",
        help="Tickers Yahoo Finance, ex : AIR.PA MC.PA TTE.PA",
    )
    parser.add_argument(
        "--csv",
        help=(
            "Chemin du fichier CSV de sortie. Par défaut : "
            "docs/raw/fondamentaux/fondamentaux_{AAAA-MM-JJ}.csv"
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Écrit aussi un .json de même nom : valeurs non arrondies et composants",
    )
    parser.add_argument(
        "--sans-carnet",
        action="store_true",
        help="N'interroge pas la limite 1 du carnet d'ordres",
    )
    parser.add_argument(
        "--archiver",
        action="store_true",
        help="Ajoute les lignes du jour a docs/raw/fondamentaux/archive.csv",
    )
    args = parser.parse_args()

    tickers = args.tickers
    if not tickers:
        saisie = input("Ticker(s) Yahoo (ex. AIR.PA MC.PA) : ").strip()
        tickers = [t for t in saisie.replace(",", " ").split() if t]
    tickers = [t.upper() for t in tickers]
    if not tickers:
        print("Aucun ticker fourni.", file=sys.stderr)
        sys.exit(1)

    lignes, details, avertissements = [], {}, []
    for ticker in tickers:
        colonnes, composants, messages = recuperer_fondamentaux(ticker, not args.sans_carnet)
        lignes.append(colonnes)
        details[ticker] = {"valeurs": colonnes, "composants": composants}
        avertissements.extend(messages)

    if all(ligne.get("COURS") is None for ligne in lignes):
        for message in avertissements:
            print(message, file=sys.stderr)
        print("Aucune valeur récupérée.", file=sys.stderr)
        sys.exit(1)

    chemin = (
        Path(args.csv)
        if args.csv
        else REPERTOIRE_DEFAUT / f"fondamentaux_{date.today().isoformat()}.csv"
    )
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8-sig", newline="") as f:
        redacteur = csv.writer(f)
        redacteur.writerow(COLONNES)
        for ligne in lignes:
            redacteur.writerow([formater(ligne.get(c), c) for c in COLONNES])

    entete = (
        f"{'Valeur':<10}{'Cours':>10}{'PER':>9}{'P/B':>7}{'VE/EBITDA':>11}"
        f"{'Rdt FCF':>9}{'ROE':>8}{'Marge op.':>11}{'Dette/EBITDA':>14}"
        f"{'Capi':>14}{'Flottant':>11}"
    )
    print(entete)
    def q(ligne, colonne, decimales=2):
        valeur = ligne.get(colonne)
        return "—" if valeur is None else f"{valeur:.{decimales}f}"

    for ligne in lignes:
        print(
            f"{ligne['TICKER']:<10}{q(ligne, 'COURS'):>10}{q(ligne, 'PER'):>9}{q(ligne, 'P_B'):>7}"
            f"{q(ligne, 'VE_EBITDA'):>11}{q(ligne, 'REND_FCF'):>9}{q(ligne, 'ROE'):>8}{q(ligne, 'MARGE_OP'):>11}"
            f"{q(ligne, 'DETTE_EBITDA'):>14}{abreger(ligne.get('CAPI')):>14}"
            f"{(q(ligne, 'FLOTTANT_PCT', 1) + ' %') if ligne.get('FLOTTANT_PCT') is not None else '—':>11}"
        )

    devises = {ligne.get("DEVISE") for ligne in lignes if ligne.get("DEVISE")}
    if len(devises) > 1:
        print(
            f"\nDevises mélangées ({', '.join(sorted(devises))}) : "
            f"les montants ne sont pas convertis et ne s'additionnent pas."
        )

    print()
    for message in avertissements:
        print(message)
    if not args.sans_carnet:
        print(
            "Profondeur du carnet : non fournie par Yahoo Finance "
            "(données de niveau 2, payantes chez Euronext ou un courtier)."
        )

    if args.archiver:
        n = archiver(lignes)
        etat = f"{n} ligne(s) ajoutée(s)" if n else "rien à ajouter"
        print(f"\nArchive                  : {etat} dans {ARCHIVE}")

    if args.json:
        chemin_json = chemin.with_suffix(".json")
        chemin_json.write_text(
            json.dumps(details, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        print(f"\nDétail écrit dans        : {chemin_json}")
    print(f"Fondamentaux écrits dans : {chemin}")


if __name__ == "__main__":
    main()
