#!/usr/bin/env python3
"""
Mesure l'alpha d'un PANIER de valeurs contre son indice, et non celui d'un titre
isole.

C'est un changement de question, pas d'outillage. L'horizon necessaire vaut
Y = (1,96 * sigma_eps / alpha)^2 : tout se joue sur la volatilite residuelle,
que la diversification abaisse. Mesure sur 2021-2025 contre le CAC 40 :
sigma_eps passe de 18,1 %/an en moyenne sur dix titres isoles a 4,2 %/an pour le
panier des memes dix — l'horizon pour un alpha de 3 % tombe de ~140 ans a 8 ans.

Le gain n'est pas gratuit : quand le panier tend vers l'indice, sigma_eps tend
vers zero et l'alpha aussi. Le script publie donc toujours l'alpha ET son
intervalle, jamais l'horizon seul.

Dependances :
    yfinance seulement si --telecharger. p_valeur_student() de import_societe.py
    et le modele de couts de couts_transaction.py sont reutilises, pas redupliques.

Utilisation :
    python python/evaluer_portefeuille.py AIR.PA OR.PA MC.PA SAN.PA TTE.PA
    python python/evaluer_portefeuille.py AIR.PA OR.PA --rebalancement trimestriel
    python python/evaluer_portefeuille.py --fichier panier.txt --debut 2021-01-01

Ce script ne choisit pas les valeurs, ne dimensionne aucune position et ne
recommande rien.
"""

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path

REPERTOIRE_QUOTES = Path("docs/raw/quotes")
INDICE_DEFAUT = "^FCHI"
SEANCES_MINIMALES = 60
JOURS_AN = 252

REBALANCEMENTS = {
    "quotidien": lambda a, b: True,
    "mensuel": lambda a, b: a[:7] != b[:7],
    "trimestriel": lambda a, b: (a[:4], (int(a[5:7]) - 1) // 3) != (b[:4], (int(b[5:7]) - 1) // 3),
    "annuel": lambda a, b: a[:4] != b[:4],
    "aucun": lambda a, b: False,
}


def fr(x, decimales=2):
    """Nombre au format francais : virgule decimale."""
    return f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")


def _outils():
    """Importe les voisins : le depot n'a pas de structure de paquet."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from couts_transaction import assujetti_ttf
    from import_societe import p_valeur_student

    return p_valeur_student, assujetti_ttf


def _csv_du_ticker(ticker):
    """Les CSV locaux du ticker, du plus recemment modifie au plus ancien."""
    vus, fichiers = set(), []
    for motif in (f"{ticker}_*.csv", f"{ticker.replace('.', '_')}_*.csv"):
        for chemin in REPERTOIRE_QUOTES.glob(motif):
            if chemin not in vus:
                vus.add(chemin)
                fichiers.append(chemin)
    return sorted(fichiers, key=lambda p: p.stat().st_mtime, reverse=True)


def _lire(chemin):
    """Le dictionnaire {date: (cloture, dividende)} d'un CSV de docs/raw/quotes/."""
    with chemin.open(encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))
    if not lignes:
        return {}
    cle = next(iter(lignes[0]))
    serie = {}
    for x in lignes:
        try:
            cours = float(x["Close"])
        except (KeyError, TypeError, ValueError):
            continue
        try:
            dividende = float(x.get("Dividends") or 0.0)
        except (TypeError, ValueError):
            dividende = 0.0
        serie[str(x[cle])[:10]] = (cours, dividende)
    return serie


def charger(ticker, telecharger, debut, fin):
    """La serie de clotures {date: cours}, depuis docs/raw/quotes/ ou telechargee.

    Un CSV qui ne COUVRE PAS la periode demandee est traite comme manquant :
    sans ce controle, un fichier plus court tronquerait l'echantillon commun en
    silence, et le resultat reposerait sur bien moins de seances qu'annonce.
    """
    for chemin in _csv_du_ticker(ticker):
        serie = _lire(chemin)
        if not serie:
            continue
        if debut and min(serie) > debut:
            print(
                f"{ticker} : {chemin.name} ne couvre pas {debut} "
                f"(commence le {min(serie)}), ignore",
                file=sys.stderr,
            )
            continue
        if fin and max(serie) < fin:
            print(
                f"{ticker} : {chemin.name} ne couvre pas {fin} "
                f"(s'arrete le {max(serie)}), ignore",
                file=sys.stderr,
            )
            continue
        return serie

    if not telecharger:
        return None

    import yfinance as yf

    try:
        h = yf.Ticker(ticker).history(start=debut, end=fin)
    except Exception as erreur:  # noqa: BLE001 — signale, puis valeur ignoree
        print(
            f"{ticker} : telechargement impossible ({erreur.__class__.__name__})",
            file=sys.stderr,
        )
        return None
    if not len(h):
        return None
    dividendes = h["Dividends"] if "Dividends" in h.columns else None
    return {
        str(k)[:10]: (float(v), float(dividendes.iloc[i]) if dividendes is not None else 0.0)
        for i, (k, v) in enumerate(h["Close"].items())
    }


def aligner(series, debut, fin):
    """L'intersection des dates, bornee par --debut et --fin."""
    communes = set.intersection(*[set(s) for s in series.values()])
    if debut:
        communes = {d for d in communes if d >= debut}
    if fin:
        communes = {d for d in communes if d <= fin}
    return sorted(communes)


def regression(rp, rm, p_valeur_student):
    """Regression des rendements du panier sur ceux de l'indice.

    Rend alpha annualise, son IC95, beta, R2 et la volatilite residuelle.
    """
    n = len(rp)
    ep, em = statistics.fmean(rp), statistics.fmean(rm)
    vm, vp = statistics.pvariance(rm, em), statistics.pvariance(rp, ep)
    cov = sum((x - em) * (y - ep) for x, y in zip(rm, rp, strict=True)) / n
    beta = cov / vm
    alpha = ep - beta * em

    residus = [y - (alpha + beta * x) for x, y in zip(rm, rp, strict=True)]
    s = math.sqrt(sum(r * r for r in residus) / (n - 2))
    se_alpha = s * math.sqrt(1 / n + em**2 / (n * vm))

    # quantile de Student a n-2 ddl, par dichotomie sur la p-valeur bilaterale
    bas, haut = 0.0, 100.0
    for _ in range(80):
        milieu = (bas + haut) / 2
        if p_valeur_student(milieu, n - 2) > 0.05:
            bas = milieu
        else:
            haut = milieu
    t = (bas + haut) / 2

    return {
        "n": n,
        "beta": beta,
        "alpha_an": 100 * JOURS_AN * alpha,
        "ic_bas": 100 * JOURS_AN * (alpha - t * se_alpha),
        "ic_haut": 100 * JOURS_AN * (alpha + t * se_alpha),
        "r2": cov**2 / (vm * vp) if vp else 0.0,
        "sigma_eps": 100 * s * math.sqrt(JOURS_AN),
    }


def horizon(alpha, sigma):
    """Annees necessaires pour distinguer `alpha` de zero, a 95 %."""
    return None if alpha <= 0 else (1.96 * sigma / alpha) ** 2


def serie_panier(dates, rendements, tickers, declencheur, cout_ar):
    """Serie du panier equipondere, poids derivant entre rebalancements.

    Rend (brute, nette, rotations). La rotation d'un evenement est
    0,5 * somme |w_avant - 1/N| : la fraction reellement vendue puis rachetee.
    """
    n = len(tickers)
    poids = [1 / n] * n
    brute, nette, rotations = [], [], []
    for j in range(len(dates) - 1):
        r = [rendements[t][j] for t in tickers]
        rp = sum(w * x for w, x in zip(poids, r, strict=True))
        brute.append(rp)

        total = sum(w * (1 + x) for w, x in zip(poids, r, strict=True))
        poids = [w * (1 + x) / total for w, x in zip(poids, r, strict=True)]

        cout = 0.0
        if declencheur(dates[j + 1], dates[j]):
            rotation = 0.5 * sum(abs(w - 1 / n) for w in poids)
            rotations.append(rotation)
            cout = rotation * cout_ar / 100
            poids = [1 / n] * n
        nette.append(rp - cout)
    return brute, nette, rotations


def main():
    parser = argparse.ArgumentParser(
        description="Alpha d'un panier de valeurs contre son indice, avec ses couts."
    )
    parser.add_argument("tickers", nargs="*", help="Valeurs du panier")
    parser.add_argument("--fichier", help="Fichier texte, un ticker par ligne")
    parser.add_argument(
        "--indice", default=INDICE_DEFAUT, help=f"Indice (defaut : {INDICE_DEFAUT})"
    )
    parser.add_argument("--debut", help="Date de debut AAAA-MM-JJ")
    parser.add_argument("--fin", help="Date de fin AAAA-MM-JJ")
    parser.add_argument(
        "--rebalancement",
        default="mensuel",
        choices=sorted(REBALANCEMENTS),
        help="Periodicite du rebalancement (defaut : mensuel)",
    )
    parser.add_argument(
        "--telecharger", action="store_true", help="Recuperer les series manquantes"
    )
    parser.add_argument("--sans-couts", action="store_true", help="N'appliquer aucun cout")
    parser.add_argument("--ttf", type=float, default=0.30, help="TTF en %% (defaut : 0.30)")
    parser.add_argument(
        "--courtage", type=float, default=0.10, help="Courtage en %% par sens"
    )
    parser.add_argument("--spread", type=float, default=0.03, help="Spread complet en %%")
    parser.add_argument("--csv", help="Ecrire le tableau des resultats")
    args = parser.parse_args()

    tickers = [t.upper() for t in args.tickers]
    if args.fichier:
        for brute_ligne in Path(args.fichier).read_text(encoding="utf-8").splitlines():
            ligne = brute_ligne.split("#")[0].strip()
            if ligne:
                tickers.append(ligne.upper())
    if not tickers:
        saisie = input("Valeurs du panier (ex. AIR.PA OR.PA MC.PA) : ").strip()
        tickers = [t.upper() for t in saisie.replace(",", " ").split() if t]
    if not tickers:
        print("Panier vide.", file=sys.stderr)
        sys.exit(1)

    p_valeur_student, assujetti_ttf = _outils()

    series, manquants = {}, []
    for t in [*tickers, args.indice]:
        s = charger(t, args.telecharger, args.debut, args.fin)
        if s is None:
            manquants.append(t)
        else:
            series[t] = s
    if manquants:
        print("Series absentes de docs/raw/quotes/ :", file=sys.stderr)
        for t in manquants:
            guillemets = "'" if t.startswith("^") else ""
            print(
                f"  python python/import_societe.py {guillemets}{t}{guillemets}"
                f" --debut {args.debut or 'AAAA-MM-JJ'} --fin {args.fin or 'AAAA-MM-JJ'}",
                file=sys.stderr,
            )
        print("  (ou relancer avec --telecharger)", file=sys.stderr)
        sys.exit(1)

    dates = aligner(series, args.debut, args.fin)
    if len(dates) < SEANCES_MINIMALES:
        print(
            f"{len(dates)} seances communes : moins de {SEANCES_MINIMALES}, "
            f"une regression n'y dirait rien.",
            file=sys.stderr,
        )
        sys.exit(1)

    rendements = {
        t: [
            series[t][dates[k]][0] / series[t][dates[k - 1]][0] - 1
            for k in range(1, len(dates))
        ]
        for t in series
    }

    # § 4bis : rendement du dividende du panier, pour l'alpha prudent
    duree_an = len(dates) / JOURS_AN
    rendements_div = []
    for t in tickers:
        verses = sum(series[t][d][1] for d in dates)
        moyen = statistics.fmean(series[t][d][0] for d in dates)
        if moyen > 0:
            rendements_div.append(100 * verses / moyen / duree_an)
    dividende_panier = statistics.fmean(rendements_div) if rendements_div else 0.0
    rm = rendements[args.indice]

    # cout d'un aller-retour, TTF evaluee valeur par valeur
    cout_ar, detail_ttf = 0.0, {}
    if not args.sans_couts:
        assujetties = 0
        for t in tickers:
            verdict, motif = assujetti_ttf(t)
            detail_ttf[t] = (verdict, motif)
            if verdict is not False:  # None inclus : TTF retenue par prudence
                assujetties += 1
        part = assujetties / len(tickers)
        cout_ar = part * args.ttf + 2 * args.courtage + args.spread

    declencheur = REBALANCEMENTS[args.rebalancement]
    brute, nette, rotations = serie_panier(dates, rendements, tickers, declencheur, cout_ar)

    print(
        f"\nPanier de {len(tickers)} valeur(s) · indice {args.indice} · "
        f"{len(dates)} seances communes ({dates[0]} -> {dates[-1]})"
    )
    duree = len(dates) / JOURS_AN
    if rotations:
        print(
            f"Rebalancement {args.rebalancement} · {len(rotations)} evenements · "
            f"rotation moyenne {fr(100 * statistics.fmean(rotations))} % par evenement"
        )
    else:
        print(f"Rebalancement {args.rebalancement} · aucun evenement · poids libres")

    print("\nTitre par titre")
    entete = f"  {'ticker':<10}{'beta':>7}{'sigma_eps':>12}"
    print(entete + f"{'alpha/an':>11}{'IC95':>24}")
    individuels, lignes_csv = [], []
    for t in tickers:
        g = regression(rendements[t], rm, p_valeur_student)
        individuels.append(g["sigma_eps"])
        print(
            f"  {t:<10}{fr(g['beta']):>7}{fr(g['sigma_eps'], 1) + ' %':>12}"
            f"{fr(g['alpha_an'], 1) + ' %':>11}"
            f"{'[' + fr(g['ic_bas'], 1) + ' ; ' + fr(g['ic_haut'], 1) + ']':>24}"
        )
        lignes_csv.append({"PERIMETRE": t, **{k: round(v, 4) for k, v in g.items()}})

    gb = regression(brute, rm, p_valeur_student)
    gn = regression(nette, rm, p_valeur_student)
    lignes_csv.append({"PERIMETRE": "PANIER_BRUT", **{k: round(v, 4) for k, v in gb.items()}})
    lignes_csv.append({"PERIMETRE": "PANIER_NET", **{k: round(v, 4) for k, v in gn.items()}})

    def qualifier(g):
        contient_zero = g["ic_bas"] <= 0 <= g["ic_haut"]
        return "indiscernable de zero" if contient_zero else "distinguable de zero"

    print("\nPanier equipondere")
    print(
        f"  beta {fr(gn['beta'])} · R2 {fr(gn['r2'], 3)} · "
        f"sigma_eps {fr(gn['sigma_eps'], 1)} %/an"
    )
    for etiquette, g in (("alpha brut", gb), ("alpha net ", gn)):
        print(
            f"  {etiquette}  {fr(g['alpha_an'], 2):>7} %/an   "
            f"IC95 [{fr(g['ic_bas'], 2)} ; {fr(g['ic_haut'], 2)}]   {qualifier(g)}"
        )
    if args.sans_couts:
        print("  (brut : --sans-couts, aucun cout applique)")
    else:
        freinage = gb["alpha_an"] - gn["alpha_an"]
        print(f"  couts       {fr(-freinage, 2):>7} %/an   aller-retour {fr(cout_ar, 3)} %")

    alpha_prudent = gn["alpha_an"] - dividende_panier
    ic_bas_prudent = gn["ic_bas"] - dividende_panier
    ic_haut_prudent = gn["ic_haut"] - dividende_panier
    prudent_zero = ic_bas_prudent <= 0 <= ic_haut_prudent
    print(
        f"  alpha prudent {fr(alpha_prudent, 2):>7} %/an   "
        f"IC95 [{fr(ic_bas_prudent, 2)} ; {fr(ic_haut_prudent, 2)}]   "
        + ("indiscernable de zero" if prudent_zero else "distinguable de zero")
    )
    print(
        f"    dont {fr(dividende_panier, 2)} %/an d'ecart de traitement des dividendes :"
        f"\n    le panier est ajuste, l'indice {args.indice} est nu. Borne basse,"
        f" volontairement sur-corrigee."
    )

    moyenne = statistics.fmean(individuels)
    print(
        f"\n  Gain de diversification : sigma_eps {fr(moyenne, 1)} % "
        f"-> {fr(gn['sigma_eps'], 1)} %/an"
        + ("" if len(tickers) > 1 else "   (une seule valeur : aucun gain possible)")
    )
    ans = horizon(alpha_prudent, gn["sigma_eps"])
    if ans is None:
        print("  Alpha prudent negatif : aucun horizon ne le rendrait significatif.")
    else:
        print(
            f"  Horizon pour prouver cet alpha : {fr(ans, 1)} ans"
            f" — echantillon de {fr(duree, 1)} ans"
        )
        if prudent_zero or ans > duree:
            print(
                f"  VERDICT : echantillon {fr(ans / duree, 1)} fois trop court. "
                f"Ce n'est pas un resultat."
            )
        else:
            print("  VERDICT : echantillon suffisant pour cet alpha-la.")

    print(
        "\n  Le verdict porte sur l'alpha PRUDENT, jamais sur le brut."
        "\n  Ce script mesure un panier fourni ; il ne le choisit pas et ne recommande rien."
    )

    if args.csv:
        chemin = Path(args.csv)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        with chemin.open("w", encoding="utf-8-sig", newline="") as f:
            redacteur = csv.DictWriter(f, fieldnames=list(lignes_csv[0]))
            redacteur.writeheader()
            redacteur.writerows(lignes_csv)
        print(f"\nResultats ecrits dans : {chemin}")


if __name__ == "__main__":
    main()
