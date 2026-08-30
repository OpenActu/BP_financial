#!/usr/bin/env python3
"""
Chiffre ce qu'une regle de decision coute a executer, et le compare a l'alpha
qu'elle devrait produire pour etre rentable.

Les couts ne s'estiment pas, ils se declarent : la TTF est un taux legal, le
courtage une clause de contrat, le spread une donnee observable. Seul l'impact
de marche est estime, et il est signale comme tel.

L'estimateur de spread de Corwin-Schultz a ete essaye puis ecarte : sur AIR.PA
il rend 1,01 % de spread median la ou une grande capitalisation en cote quelques
points de base. Voir le miroir.

Dependance :
    yfinance, pour le pays d'immatriculation et la capitalisation. En mode bareme
    (sans ticker), le script tourne sans reseau et sans CSV.

Utilisation :
    python python/couts_transaction.py
    python python/couts_transaction.py --montant 50000
    python python/couts_transaction.py AIR.PA OR.PA ATO.PA --montant 50000
    python python/couts_transaction.py --courtage 0.02 --spread 0.01 --sans-ttf
"""

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path

REPERTOIRE_QUOTES = Path("docs/raw/data/quotes")
SEUIL_TTF_MDS = 1.0
PAYS_TTF = "France"
COEFFICIENT_IMPACT = 0.5
JOURS_AN = 252

ROTATIONS = [
    ("quotidienne", 252),
    ("hebdomadaire", 52),
    ("mensuelle", 12),
    ("trimestrielle", 4),
    ("annuelle", 1),
    ("triennale", 1 / 3),
]


def fr(x, decimales=2):
    """Nombre au format francais : virgule decimale, espace des milliers."""
    return f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")


def assujetti_ttf(ticker):
    """Les deux conditions cumulatives : immatriculation France ET capi > 1 Md.

    Rend (verdict, motif). Le verdict vaut None quand la donnee manque : le
    script ne tranche pas a la place de l'utilisateur.
    """
    import yfinance as yf

    try:
        info = yf.Ticker(ticker).info or {}
    except Exception as erreur:  # noqa: BLE001 — signale, puis verdict indetermine
        print(
            f"{ticker} : interrogation impossible ({erreur.__class__.__name__})",
            file=sys.stderr,
        )
        return None, "donnees indisponibles"

    pays, capi = info.get("country"), info.get("marketCap")
    if not pays or not capi:
        return None, "pays ou capitalisation absents"

    mds = capi / 1e9
    if pays != PAYS_TTF:
        return False, f"immatriculee {pays}"
    if mds <= SEUIL_TTF_MDS:
        return False, f"capitalisation {fr(mds, 1)} Md < {fr(SEUIL_TTF_MDS, 1)} Md"
    return True, f"{pays}, capitalisation {fr(mds, 1)} Md"


def _csv_du_ticker(ticker):
    """Le CSV le plus recent de docs/raw/data/quotes/ pour ce ticker, ou None."""
    motif = f"{ticker.replace('.', '_')}_*.csv"
    fichiers = sorted(REPERTOIRE_QUOTES.glob(motif), key=lambda p: p.stat().st_mtime)
    return fichiers[-1] if fichiers else None


def impact_marche(ticker, montant, coefficient=COEFFICIENT_IMPACT):
    """Loi en racine carree : Y * sigma_jour * sqrt(Q/V), en %.

    Rend (impact, detail) ou (None, motif) : un impact inconnu n'est pas un
    impact nul, la colonne reste vide.
    """
    chemin = _csv_du_ticker(ticker)
    if chemin is None:
        return None, "aucun CSV dans docs/raw/data/quotes/"

    with chemin.open(encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))
    closes, volumes = [], []
    for x in lignes[-JOURS_AN:]:
        try:
            c, v = float(x["Close"]), float(x["Volume"])
        except (KeyError, TypeError, ValueError):
            continue
        if c > 0 and v > 0:
            closes.append(c)
            volumes.append(v)
    if len(closes) < 30:
        return None, "moins de 30 seances exploitables"

    rendements = [closes[k] / closes[k - 1] - 1 for k in range(1, len(closes))]
    sigma_jour = statistics.pstdev(rendements)
    volume_median = statistics.median(volumes)
    titres = montant / closes[-1]
    part = titres / volume_median
    impact = 100 * coefficient * sigma_jour * math.sqrt(part)
    detail = (
        f"{fr(titres, 0)} titres sur {fr(volume_median, 0)} echanges "
        f"({part * 100:.4f} % du volume)"
    )
    return impact, detail


def aller_retour(ttf, courtage, spread, impact=None):
    """TTF (achat seul) + 2 courtages + 1 spread complet + 2 impacts."""
    return ttf + 2 * courtage + spread + 2 * (impact or 0.0)


def horizon(alpha, sigma_residuel):
    """Annees necessaires pour distinguer `alpha` de zero, a 95 %."""
    if alpha <= 0:
        return None
    return (1.96 * sigma_residuel / alpha) ** 2


def main():
    parser = argparse.ArgumentParser(
        description="Cout d'execution d'une regle, et alpha qu'il faudrait pour le couvrir."
    )
    parser.add_argument("tickers", nargs="*", help="Valeurs a chiffrer (defaut : bareme seul)")
    parser.add_argument(
        "--ttf", type=float, default=0.30, help="TTF en %%, a l'achat (defaut : 0.30)"
    )
    parser.add_argument(
        "--courtage", type=float, default=0.10, help="Courtage en %%, par sens (defaut : 0.10)"
    )
    parser.add_argument(
        "--spread", type=float, default=0.03, help="Spread complet en %% (defaut : 0.03)"
    )
    parser.add_argument(
        "--montant", type=float, default=10000, help="Taille de l'ordre en euros (defaut : 10000)"
    )
    parser.add_argument("--sans-ttf", action="store_true", help="Ignorer la TTF")
    parser.add_argument(
        "--sigma-residuel",
        type=float,
        default=30.0,
        help="Volatilite residuelle en %%/an, pour l'horizon (defaut : 30)",
    )
    parser.add_argument("--csv", help="Ecrire le tableau des rotations")
    args = parser.parse_args()

    if min(args.ttf, args.courtage, args.spread, args.montant, args.sigma_residuel) < 0:
        print("Les parametres ne peuvent pas etre negatifs.", file=sys.stderr)
        sys.exit(1)

    ttf_bareme = 0.0 if args.sans_ttf else args.ttf
    cout = aller_retour(ttf_bareme, args.courtage, args.spread)

    print("Bareme, par aller-retour")
    print(f"  {'TTF (achat)':<30}{fr(ttf_bareme, 3):>9} %"
          + ("   [desactivee]" if args.sans_ttf else ""))
    print(f"  {'Courtage (2 sens)':<30}{fr(2 * args.courtage, 3):>9} %")
    print(f"  {'Spread (1 spread complet)':<30}{fr(args.spread, 3):>9} %")
    print(f"  {'Impact de marche':<30}{'non calcule':>11}   (mode bareme)")
    print("  " + "─" * 41)
    print(f"  {'Aller-retour':<30}{fr(cout, 3):>9} %")

    print("\nFreinage annuel, et alpha qu'il faudrait pour le couvrir")
    print(f"  volatilite residuelle retenue : {fr(args.sigma_residuel, 1)} %/an\n")
    print(f"  {'rotation':<16}{'A/R par an':>11}{'freinage':>11}{'annees pour le prouver':>24}")
    lignes_csv = []
    for nom, n in ROTATIONS:
        drag = n * cout
        ans = horizon(drag, args.sigma_residuel)
        ans_txt = "—" if ans is None else (fr(ans, 1) if ans < 1000 else fr(ans, 0))
        print(f"  {nom:<16}{fr(n, 2):>11}{fr(drag, 2) + ' %':>11}{ans_txt:>24}")
        lignes_csv.append(
            {
                "ROTATION": nom,
                "ALLERS_RETOURS_AN": round(n, 4),
                "COUT_ALLER_RETOUR_PCT": round(cout, 4),
                "FREINAGE_ANNUEL_PCT": round(drag, 4),
                "ALPHA_SEUIL_PCT": round(drag, 4),
                "ANNEES_POUR_PROUVER": None if ans is None else round(ans, 1),
            }
        )

    print(
        "\n  Lecture : plus la rotation est rapide, plus l'alpha de seuil est eleve —"
        "\n  donc plus facile a detecter, mais absurdement grand. Plus elle est lente,"
        "\n  plus le seuil devient atteignable, mais il passe sous le plancher du"
        "\n  mesurable. Abaisser la volatilite residuelle par la diversification est"
        "\n  la seule sortie."
    )

    for ticker in args.tickers:
        verdict, motif = (False, "--sans-ttf") if args.sans_ttf else assujetti_ttf(ticker)
        impact, detail = impact_marche(ticker, args.montant)
        if verdict is None:
            etiquette = "INDETERMINE — TTF retenue par prudence"
            ttf_valeur = args.ttf
        elif verdict:
            etiquette = f"assujettie ({motif})"
            ttf_valeur = args.ttf
        else:
            etiquette = f"exemptee ({motif})"
            ttf_valeur = 0.0

        total = aller_retour(ttf_valeur, args.courtage, args.spread, impact)
        print(f"\n{ticker}")
        print(f"  TTF               : {etiquette}")
        if impact is None:
            print(f"  Impact de marche  : non calcule — {detail}")
        else:
            print(f"  Impact de marche  : {fr(impact, 4)} % par sens — {detail}")
        print(f"  Aller-retour      : {fr(total, 3)} % pour un ordre de {fr(args.montant, 0)} €")

    if args.csv:
        chemin = Path(args.csv)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        with chemin.open("w", encoding="utf-8-sig", newline="") as f:
            redacteur = csv.DictWriter(f, fieldnames=list(lignes_csv[0]))
            redacteur.writeheader()
            for ligne in lignes_csv:
                redacteur.writerow({k: ("" if v is None else v) for k, v in ligne.items()})
        print(f"\nTableau ecrit dans : {chemin}")


if __name__ == "__main__":
    main()
