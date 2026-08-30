#!/usr/bin/env python3
"""
Construit un indice de reference EN RENDEMENT TOTAL, a partir de composants
declares.

Le probleme resolu est chiffre : Close est ajustee des dividendes, ^FCHI est un
indice nu, et l'ecart vaut 6,22 points d'alpha par an sur 24 ans. Les deux series
comparees doivent etre de meme convention.

CE N'EST PAS LE CAC 40. C'est un panier de valeurs declarees, pondere selon une
regle declaree, constitue aujourd'hui — donc sans les valeurs radiees. L'ecart
mesure contre ^FCHI melange dividendes, composition et ponderation ; le lire
comme un rendement de dividende serait une erreur.

Dependance :
    yfinance seulement si --telecharger.

Utilisation :
    python python/construire_indice_total.py AIR.PA OR.PA MC.PA SAN.PA TTE.PA
    python python/construire_indice_total.py --fichier univers.txt --debut 2001-09-04
    python python/evaluer_portefeuille.py AIR.PA OR.PA --indice TR10
"""

import argparse
import csv
import statistics
import sys
from pathlib import Path

REPERTOIRE_QUOTES = Path("docs/raw/data/quotes")
BASE = 1000.0
SEANCES_MINIMALES = 250
VALEURS_MINIMALES = 2
JOURS_AN = 252

REBALANCEMENTS = {
    "mensuel": lambda a, b: a[:7] != b[:7],
    "trimestriel": lambda a, b: (a[:4], (int(a[5:7]) - 1) // 3) != (b[:4], (int(b[5:7]) - 1) // 3),
    "annuel": lambda a, b: a[:4] != b[:4],
    "aucun": lambda a, b: False,
}


def fr(x, decimales=2):
    """Nombre au format francais : virgule decimale."""
    return f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")


def _evaluateur():
    """Reutilise le chargement et l'alignement de evaluer_portefeuille.py."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from evaluer_portefeuille import aligner, charger

    return charger, aligner


def poids_initiaux(tickers, ponderation):
    """Les poids cibles. `capi` lit la capitalisation DU JOUR — regard en avant."""
    if ponderation == "egale":
        return {t: 1 / len(tickers) for t in tickers}, tickers

    import yfinance as yf

    print(
        "ATTENTION : --ponderation capi utilise la capitalisation d'AUJOURD'HUI pour\n"
        "ponderer tout le passe. C'est un regard en avant caracterise : les valeurs\n"
        "qui ont reussi pesent lourd des la premiere seance. `egale` est le defaut.",
        file=sys.stderr,
    )
    capis, retenus = {}, []
    for t in tickers:
        try:
            c = (yf.Ticker(t).info or {}).get("marketCap")
        except Exception as erreur:  # noqa: BLE001 — signale, puis valeur ecartee
            print(f"{t} : capitalisation illisible ({erreur.__class__.__name__})", file=sys.stderr)
            c = None
        if not c:
            print(f"{t} : capitalisation absente, valeur ecartee de l'univers", file=sys.stderr)
            continue
        capis[t] = float(c)
        retenus.append(t)
    total = sum(capis.values())
    return {t: capis[t] / total for t in retenus}, retenus


def construire(dates, rendements, tickers, poids_cible, declencheur):
    """La serie de l'indice, base 1000, poids derivant entre rebalancements."""
    poids = [poids_cible[t] for t in tickers]
    niveau = BASE
    serie = {dates[0]: niveau}
    for j in range(len(dates) - 1):
        r = [rendements[t][j] for t in tickers]
        rp = sum(w * x for w, x in zip(poids, r, strict=True))
        niveau *= 1 + rp
        serie[dates[j + 1]] = niveau

        total = sum(w * (1 + x) for w, x in zip(poids, r, strict=True))
        poids = [w * (1 + x) / total for w, x in zip(poids, r, strict=True)]
        if declencheur(dates[j + 1], dates[j]):
            poids = [poids_cible[t] for t in tickers]
    return serie


def cagr(serie, dates):
    """Performance annualisee, en %."""
    annees = len(dates) / JOURS_AN
    return 100 * ((serie[dates[-1]] / serie[dates[0]]) ** (1 / annees) - 1)


def main():
    parser = argparse.ArgumentParser(
        description="Indice de reference en rendement total, a partir de composants declares."
    )
    parser.add_argument("tickers", nargs="*", help="Univers de reference")
    parser.add_argument("--fichier", help="Fichier texte, un ticker par ligne")
    parser.add_argument("--debut", help="Date de debut AAAA-MM-JJ")
    parser.add_argument("--fin", help="Date de fin AAAA-MM-JJ")
    parser.add_argument(
        "--ponderation", default="egale", choices=("egale", "capi"), help="Defaut : egale"
    )
    parser.add_argument(
        "--rebalancement",
        default="annuel",
        choices=sorted(REBALANCEMENTS),
        help="Defaut : annuel",
    )
    parser.add_argument("--nom", help="Nom de l'indice (defaut : TR{N})")
    parser.add_argument("--comparer", default="^FCHI", help="Indice nu de comparaison")
    parser.add_argument(
        "--telecharger", action="store_true", help="Recuperer les series manquantes"
    )
    args = parser.parse_args()

    tickers = [t.upper() for t in args.tickers]
    if args.fichier:
        for brute in Path(args.fichier).read_text(encoding="utf-8").splitlines():
            ligne = brute.split("#")[0].strip()
            if ligne:
                tickers.append(ligne.upper())
    if not tickers:
        saisie = input("Univers de reference (ex. AIR.PA OR.PA MC.PA) : ").strip()
        tickers = [t.upper() for t in saisie.replace(",", " ").split() if t]
    if len(tickers) < VALEURS_MINIMALES:
        print(f"Il faut au moins {VALEURS_MINIMALES} valeurs.", file=sys.stderr)
        sys.exit(1)

    charger, aligner = _evaluateur()
    poids_cible, tickers = poids_initiaux(tickers, args.ponderation)
    if len(tickers) < VALEURS_MINIMALES:
        print(f"Moins de {VALEURS_MINIMALES} valeurs exploitables.", file=sys.stderr)
        sys.exit(1)

    series, manquants = {}, []
    a_charger = list(tickers) + ([args.comparer] if args.comparer else [])
    for t in a_charger:
        s = charger(t, args.telecharger, args.debut, args.fin)
        if s is None:
            manquants.append(t)
        else:
            series[t] = s
    if args.comparer in manquants:
        print(f"{args.comparer} indisponible : comparaison omise.", file=sys.stderr)
        manquants.remove(args.comparer)
        series.pop(args.comparer, None)
    if manquants:
        print("Series absentes de docs/raw/data/quotes/ :", file=sys.stderr)
        for t in manquants:
            g = "'" if t.startswith("^") else ""
            print(f"  python python/import_societe.py {g}{t}{g}", file=sys.stderr)
        print("  (ou relancer avec --telecharger)", file=sys.stderr)
        sys.exit(1)

    dates = aligner(series, args.debut, args.fin)
    if len(dates) < SEANCES_MINIMALES:
        print(
            f"{len(dates)} seances communes : moins de {SEANCES_MINIMALES}, "
            f"l'objet produit ne meriterait pas le nom d'indice.",
            file=sys.stderr,
        )
        sys.exit(1)

    rendements = {
        t: [
            series[t][dates[k]][0] / series[t][dates[k - 1]][0] - 1
            for k in range(1, len(dates))
        ]
        for t in tickers
    }
    indice = construire(
        dates, rendements, tickers, poids_cible, REBALANCEMENTS[args.rebalancement]
    )
    nom = args.nom or f"TR{len(tickers)}"

    print(
        f"\nIndice {nom} · {len(tickers)} valeurs · ponderation {args.ponderation}"
        f" · rebalancement {args.rebalancement}"
    )
    print(f"  {len(dates)} seances du {dates[0]} au {dates[-1]}")
    print(f"  base {fr(BASE, 0)} -> {fr(indice[dates[-1]], 1)}")
    if args.rebalancement == "aucun":
        print("  (sans rebalancement : l'indice cesse d'etre equipondere)")

    perf = cagr(indice, dates)
    print(f"\n  {nom + ' (rendement total)':<28}CAGR {fr(perf):>7} %/an")
    if args.comparer in series:
        nu = {d: series[args.comparer][d][0] for d in dates}
        perf_nu = cagr(nu, dates)
        print(f"  {args.comparer + ' (nu)':<28}CAGR {fr(perf_nu):>7} %/an")
        print(f"  {'ecart':<28}     {fr(perf - perf_nu):>7} points/an")
        print(
            "  Cet ecart melange dividendes, composition et ponderation."
            "\n  Le lire comme un rendement de dividende serait une erreur."
        )

    chemin = REPERTOIRE_QUOTES / f"{nom}_{dates[0]}_{dates[-1]}.csv"
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline="") as f:
        redacteur = csv.writer(f)
        redacteur.writerow(["Date", "Close", "Dividends"])
        for d in dates:
            # Dividends a 0 : l'indice les integre deja, la correction prudente
            # de evaluer_portefeuille.py ne doit pas s'appliquer deux fois
            redacteur.writerow([d, f"{indice[d]:.6f}", "0"])
    print(f"\n  Ecrit dans : {chemin}")
    print(f"  Utilisable tel quel : python python/evaluer_portefeuille.py ... --indice {nom}")
    print(
        f"\n  Rappel : {nom} n'est PAS le CAC 40. Univers declare et constitue aujourd'hui"
        f"\n  (biais du survivant entier), ponderation {args.ponderation}, {len(tickers)} valeurs."
    )
    moyenne_poids = statistics.fmean(poids_cible.values())
    if args.ponderation == "capi":
        print(f"  Poids moyen {fr(100 * moyenne_poids)} % — capitalisations du jour.")


if __name__ == "__main__":
    main()
