#!/usr/bin/env python3
"""Dimensionne une exposition — levier et couverture — sans supposer de rendement espere.

Le levier optimal L* = (mu - c) / sigma^2 depend de la seule quantite que le
depot demontre non mesurable. Ce script ne demande donc pas mu : il publie, pour
chaque levier, le mu qu'il faudrait pour justifier ce levier, et le confronte a
l'intervalle de confiance du mu mesure sur la serie.

Miroir d'execution : python/dimensionner_exposition.md — il fait autorite.
"""

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path

import pandas as pd

JOURS_AN = 252
SEANCES_MINIMALES = 250
Z95 = 1.959963985
LEVIERS_DEFAUT = (1.0, 1.5, 2.0, 2.5, 3.0, 4.0)
MARGE_DEFAUT = 0.20
PORTAGE_DEFAUT = 5.0
BAISSE_DEFAUT = 30.0
HORIZON_DEFAUT = 1.0
COUT_AR_DEFAUT = 0.53
ROTATION_DEFAUT = 1.0
BAISSES_TABLE = (10.0, 20.0, 30.0, 40.0, 50.0)
REPERTOIRE_QUOTES = Path("docs/raw/data/quotes")


def erreur(message):
    """Message sur stderr et sortie 1."""
    print(message, file=sys.stderr)
    sys.exit(1)


def fr(x, decimales=2):
    """Nombre au format francais : virgule decimale."""
    return f"{x:.{decimales}f}".replace(".", ",")


def phi(z):
    """Fonction de repartition de la loi normale centree reduite."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def charger(chemin):
    """Lit un CSV de cotations et rend (dates AAAA-MM-JJ, clotures)."""
    try:
        df = pd.read_csv(chemin)
    except OSError:
        erreur(f"Fichier introuvable : {chemin}")
    df.columns = [str(c) for c in df.columns]
    if "Close" not in df.columns:
        erreur(f"Colonne Close absente de {chemin}")
    dates = [str(v)[:10] for v in df[df.columns[0]]]
    closes = [float(v) for v in df["Close"]]
    return dates, closes


def mesures(closes):
    """Derive, volatilite, IC95, repli maximal, et la volatilite par sous-fenetres."""
    rendements = [closes[k] / closes[k - 1] - 1 for k in range(1, len(closes))]
    n = len(rendements)
    sigma = math.sqrt(JOURS_AN) * statistics.pstdev(rendements)
    if sigma <= 0:
        erreur("Volatilite nulle : la serie ne varie pas, il n'y a rien a dimensionner.")

    annees = n / JOURS_AN
    mu = JOURS_AN * statistics.fmean(rendements)
    se = sigma / math.sqrt(annees)

    pic, repli = closes[0], 0.0
    for c in closes:
        pic = max(pic, c)
        repli = min(repli, c / pic - 1)

    def sigma_sur(part):
        tranche = rendements[-max(2, int(n * part)) :]
        return math.sqrt(JOURS_AN) * statistics.pstdev(tranche)

    return {
        "n": n,
        "annees": annees,
        "mu": mu,
        "sigma": sigma,
        "se": se,
        "ic_bas": mu - Z95 * se,
        "ic_haut": mu + Z95 * se,
        "cagr": (closes[-1] / closes[0]) ** (1 / annees) - 1,
        "repli": repli,
        "sigma_moitie": sigma_sur(0.5),
        "sigma_quart": sigma_sur(0.25),
    }


def p_barriere(seuil, mu, sigma, horizon):
    """Probabilite de toucher une baisse `seuil` avant `horizon`, loi du minimum brownien.

    Formule du paragraphe 3.2 du module 3 du cours finance. Rend None quand le
    seuil n'est pas dans ]0 ; 1[ — position deja en defaut, ou barriere absente.
    """
    if not 0 < seuil < 1:
        return None
    a = math.log(1 - seuil)
    nu = mu - sigma**2 / 2
    ecart = sigma * math.sqrt(horizon)
    return phi((a - nu * horizon) / ecart) + math.exp(2 * nu * a / sigma**2) * phi(
        (a + nu * horizon) / ecart
    )


def ligne_levier(levier, m, args, mes):
    """Une ligne du tableau par levier : ce qui est certain, et ce qu'il faudrait."""
    sigma, portage = mes["sigma"], args.portage / 100
    frais = levier * args.rotation * args.cout_ar / 100
    ligne = {
        "levier": levier,
        "drag": -(levier**2) * sigma**2 / 2,
        "frais": frais,
        "seuil": None,
        "baisse_log": None,
        "p": [None, None, None],
        "surcout": None,
        "portage": None,
        "mu_requis": None,
        "verdict": None,
        "h_pour_e1": None,
        "cout_detour": None,
        "defaut": False,
    }
    if levier <= 1:
        return ligne

    seuil = (1 / levier - m) / (1 - m)
    ligne["defaut"] = seuil <= 0
    if not ligne["defaut"]:
        ligne["seuil"] = seuil
        ligne["baisse_log"] = -math.log(1 - seuil)
        ligne["p"] = [
            p_barriere(seuil, mu, sigma, args.horizon)
            for mu in (mes["ic_bas"], mes["mu"], mes["ic_haut"])
        ]

    mu_requis = portage + (levier + 1) * sigma**2 / 2
    ligne["surcout"] = -(levier**2 - 1) * sigma**2 / 2
    ligne["portage"] = (levier - 1) * portage
    ligne["mu_requis"] = mu_requis
    if mu_requis < mes["ic_bas"]:
        ligne["verdict"] = "justifie"
    elif mu_requis > mes["ic_haut"]:
        ligne["verdict"] = "exclu"
    else:
        ligne["verdict"] = "indiscernable"
    ligne["h_pour_e1"] = 1 - 1 / levier
    ligne["cout_detour"] = (levier - 1) * (portage + args.rotation * args.cout_ar / 100)
    return ligne


def cel(valeur, largeur, decimales=2, suffixe="", facteur=1.0):
    """Cellule alignee a droite ; un tiret quand la valeur n'existe pas."""
    if valeur is None:
        return "-".rjust(largeur)
    return (fr(valeur * facteur, decimales) + suffixe).rjust(largeur)


def afficher_serie(nom, dates, mes, args):
    """Ce que la serie dit, et ce qu'elle ne dit pas."""
    print(
        f"Serie            : {nom} ({len(dates)} seances, {dates[0]} -> {dates[-1]}, "
        f"{fr(mes['annees'])} ans)"
    )
    print(
        f"Volatilite       : {fr(100 * mes['sigma'])} %/an   "
        f"(derniere moitie {fr(100 * mes['sigma_moitie'])} % - "
        f"dernier quart {fr(100 * mes['sigma_quart'])} %)"
    )
    print(f"Repli maximal    : {fr(100 * mes['repli'], 1)} %")
    print(f"CAGR             : {fr(100 * mes['cagr'])} %/an")
    print(
        f"Derive mesuree   : mu = {fr(100 * mes['mu'])} %/an - SE {fr(100 * mes['se'])} pt - "
        f"IC95 [{fr(100 * mes['ic_bas'])} ; {fr(100 * mes['ic_haut'])}] %"
    )
    largeur = 100 * (mes["ic_haut"] - mes["ic_bas"])
    zero = " - indiscernable de zero" if mes["ic_bas"] <= 0 <= mes["ic_haut"] else ""
    print(f"                   intervalle large de {fr(largeur, 1)} points{zero}")
    if nom.startswith("^"):
        print(
            "Rappel           : le nom du fichier commence par ^ ; s'il s'agit d'un indice nu,\n"
            "                   mu est sous-estime du rendement du dividende."
        )
    print()
    print(
        f"Parametres declares : marge {fr(100 * args.marge, 0)} % - "
        f"portage {fr(args.portage)} %/an - "
        f"rotation {fr(args.rotation)} A/R/an a {fr(args.cout_ar, 3)} %"
    )


def afficher_admissible(m, args):
    """Le seul dimensionnement exact du script : il ne depend que de m et de d."""
    borne = lambda d: 1 / (m + (1 - m) * d)  # noqa: E731 — formule d'une ligne, § 3.5
    print()
    print(
        f"Levier admissible pour supporter {fr(-args.baisse, 1)} % sans appel : "
        f"L <= {fr(borne(args.baisse / 100))}"
    )
    cellules = [f"{fr(-d, 0)} %  L <= {fr(borne(d / 100))}".ljust(22) for d in BAISSES_TABLE]
    for k in range(0, len(cellules), 3):
        print(("   " + "".join(cellules[k : k + 3])).rstrip())


def afficher_tableau(lignes):
    """Le tableau par levier : coût certain a gauche, mu necessaire a droite."""
    print()
    print(
        " levier    seuil   baisse      P(appel) bas/mu/haut      drag  surcout"
        "  portage    frais     mu requis  verdict"
    )
    for li in lignes:
        seuil = "defaut".rjust(9) if li["defaut"] else cel(li["seuil"], 9, 2, " %", 100)
        cases = [
            cel(li["levier"], 7),
            seuil,
            cel(li["baisse_log"], 9, 2, " %", 100),
            *[cel(p, 8, 1, " %", 100) for p in li["p"]],
            cel(li["drag"], 10, 2, " %", 100),
            cel(li["surcout"], 9, 2, " %", 100),
            cel(li["portage"], 9, 2, " %", 100),
            cel(li["frais"], 9, 2, " %", 100),
            cel(li["mu_requis"], 13, 2, " %/an", 100),
            "  " + (li["verdict"] or "-"),
        ]
        print("".join(cases))


def afficher_exposition(lignes):
    """e = L (1 - h) : couvrir un actif par lui-meme ne fait que baisser l'exposition."""
    couvrables = [li for li in lignes if li["h_pour_e1"] is not None]
    if not couvrables:
        return
    print()
    print("Exposition nette e = L (1 - h) : couvrir un actif par lui-meme ne fait que baisser e")
    print(" levier   h pour e = 1   cout annuel de ce detour")
    for li in couvrables:
        print(
            cel(li["levier"], 7)
            + cel(li["h_pour_e1"], 15, 3)
            + cel(li["cout_detour"], 27, 2, " %/an", 100)
        )


def ecrire_csv(chemin, lignes):
    """Une ligne par levier ; cellule vide plutot qu'un nombre invente."""
    chemin = Path(chemin)
    if chemin.parent != Path():
        chemin.parent.mkdir(parents=True, exist_ok=True)
    pc = lambda v, d=2: "" if v is None else f"{100 * v:.{d}f}"  # noqa: E731 — mise en forme
    with chemin.open("w", newline="", encoding="utf-8") as flux:
        w = csv.writer(flux)
        w.writerow(
            [
                "LEVIER", "SEUIL_APPEL", "BAISSE_LOG", "P_APPEL_BAS", "P_APPEL_MU",
                "P_APPEL_HAUT", "DRAG", "SURCOUT", "PORTAGE", "FRAIS", "MU_REQUIS",
                "VERDICT", "H_POUR_E1", "COUT_DETOUR",
            ]
        )
        for li in lignes:
            w.writerow(
                [
                    f"{li['levier']:.2f}",
                    "" if li["defaut"] else pc(li["seuil"]),
                    pc(li["baisse_log"]),
                    *[pc(p, 1) for p in li["p"]],
                    pc(li["drag"]),
                    pc(li["surcout"]),
                    pc(li["portage"]),
                    pc(li["frais"]),
                    pc(li["mu_requis"]),
                    li["verdict"] or "",
                    "" if li["h_pour_e1"] is None else f"{li['h_pour_e1']:.3f}",
                    pc(li["cout_detour"]),
                ]
            )
    print(f"\nTableau ecrit dans : {chemin}")


def analyser_arguments():
    """Ligne de commande, et controle du domaine de chaque parametre."""
    parser = argparse.ArgumentParser(
        description="Dimensionne une exposition a partir d'une volatilite mesuree, "
        "sans supposer de rendement espere."
    )
    parser.add_argument("--csv", help="CSV de la serie (defaut : le plus recent de quotes/)")
    parser.add_argument("--fenetre", type=int, help="Seances retenues, ancrees a droite")
    parser.add_argument(
        "-m", "--marge", type=float, default=MARGE_DEFAUT, help="Couverture exigee (defaut : 0.20)"
    )
    parser.add_argument(
        "-c", "--portage", type=float, default=PORTAGE_DEFAUT,
        help="Cout du levier en %%/an (defaut : 5.0)",
    )
    parser.add_argument(
        "-d", "--baisse", type=float, default=BAISSE_DEFAUT,
        help="Baisse a supporter sans appel, en %% (defaut : 30.0)",
    )
    parser.add_argument(
        "--leviers", type=float, nargs="+", default=list(LEVIERS_DEFAUT), help="Leviers examines"
    )
    parser.add_argument(
        "--horizon", type=float, default=HORIZON_DEFAUT, help="Annees, pour P(appel)"
    )
    parser.add_argument(
        "--cout-ar", type=float, default=COUT_AR_DEFAUT, help="Cout d'un aller-retour, en %%"
    )
    parser.add_argument(
        "--rotation", type=float, default=ROTATION_DEFAUT, help="Aller-retours par an"
    )
    parser.add_argument("--sortie", help="CSV du tableau par levier")
    args = parser.parse_args()

    if not 0 < args.marge < 1:
        erreur("--marge doit etre dans ]0 ; 1[.")
    if not 0 < args.baisse < 100:
        erreur("--baisse doit etre dans ]0 ; 100[.")
    if args.horizon <= 0:
        erreur("--horizon doit etre strictement positif.")
    if args.rotation < 0 or args.cout_ar < 0:
        erreur("--rotation et --cout-ar doivent etre positifs ou nuls.")
    if any(levier <= 0 for levier in args.leviers):
        erreur("Les leviers doivent etre strictement positifs.")
    return args


def main():
    args = analyser_arguments()

    if args.csv:
        chemin = Path(args.csv)
    else:
        candidats = list(REPERTOIRE_QUOTES.glob("*.csv"))
        if not candidats:
            erreur("Aucun CSV dans docs/raw/data/quotes/ ; preciser --csv.")
        chemin = max(candidats, key=lambda p: p.stat().st_mtime)

    dates, closes = charger(chemin)
    if args.fenetre:
        dates, closes = dates[-args.fenetre :], closes[-args.fenetre :]
    if len(closes) < SEANCES_MINIMALES:
        erreur(
            f"{len(closes)} seances retenues : moins de {SEANCES_MINIMALES}. "
            "Une volatilite estimee sur moins d'un an ne merite pas d'etre publiee."
        )

    mes = mesures(closes)
    nom = chemin.stem.split("_20")[0].replace("_", ".")  # convention de generer_graph_decision

    afficher_serie(nom, dates, mes, args)
    afficher_admissible(args.marge, args)
    lignes = [ligne_levier(levier, args.marge, args, mes) for levier in sorted(args.leviers)]
    afficher_tableau(lignes)
    afficher_exposition(lignes)

    if args.sortie:
        ecrire_csv(args.sortie, lignes)

    print()
    print(
        "Aucun levier n'est recommande : ce script rend ce qui est admissible, ce qui est\n"
        "certain, et ce qu'il faudrait. Le rapprochement des trois est un dimensionnement,\n"
        "pas un conseil."
    )


if __name__ == "__main__":
    main()
