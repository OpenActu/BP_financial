#!/usr/bin/env python3
"""
Reconstitue une série historique de ratios fondamentaux, séance par séance.

Règle unique : à la séance d, on n'utilise que le dernier exercice dont la date
de PUBLICATION est <= d. Jamais celui qui sera publié demain, même s'il porte
sur une période déjà close.

Dépendances :
    yfinance et pandas (installé avec lui). Ni scipy, ni bibliothèque de tracé.

Utilisation :
    python python/reconstituer_fondamentaux.py AIR.PA
    python python/reconstituer_fondamentaux.py AIR.PA BNP.PA --debut 2022-01-01
    python python/reconstituer_fondamentaux.py AIR.PA --trimestriel --mensuel
    python python/reconstituer_fondamentaux.py AIR.PA --decalage 90

Trois biais survivent à la reconstruction et doivent accompagner toute série
produite ici : le contenu des comptes n'est pas garanti conforme au publié (voir
le § 10 du miroir : chiffre d'affaires et résultat net concordent au centime,
l'EBIT s'écarte de 19,3 %), le biais du survivant, et une profondeur plafonnée à
4-5 exercices.
"""

import argparse
import csv
import math
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

REPERTOIRE_DEFAUT = Path("docs/raw/fondamentaux")
DECALAGE_DEFAUT = 75
LIMITE_ANNONCES = 100  # plafond impose par la source : au-dela, ValueError

# correspondance colonne produite -> (etat financier, libelle de ligne yfinance)
POSTES = {
    "resultat_net": ("income", "Net Income"),
    "chiffre_affaires": ("income", "Total Revenue"),
    "ebitda": ("income", "EBITDA"),
    "resultat_operationnel": ("income", "Operating Income"),
    "fonds_propres": ("bilan", "Stockholders Equity"),
    "dette": ("bilan", "Total Debt"),
    "tresorerie": ("bilan", "Cash And Cash Equivalents"),
    "fcf": ("flux", "Free Cash Flow"),
}

COLONNES = [
    "DATE", "TICKER", "CLOTURE", "ACTIONS", "CAPI", "VE",
    "PER", "P_B", "VE_EBITDA", "REND_FCF",
    "ROE", "MARGE_NETTE", "MARGE_OP", "DETTE_EBITDA",
    "EXERCICE", "PUBLICATION", "PUBLICATION_ESTIMEE",
]

DECIMALES = {
    "CLOTURE": 4,
    "PER": 2, "P_B": 2, "VE_EBITDA": 2, "DETTE_EBITDA": 2,
    "REND_FCF": 2, "ROE": 2, "MARGE_NETTE": 2, "MARGE_OP": 2,
}


def _nombre(valeur):
    """Rend un float utilisable, ou None : ni chaine, ni booleen, ni NaN."""
    if valeur is None or isinstance(valeur, bool):
        return None
    try:
        x = float(valeur)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) else x


def _rapport(numerateur, denominateur):
    """Rapport, ou None. Le denominateur doit etre strictement positif.

    Un multiple sur benefice, fonds propres ou EBITDA negatif ne se compare a
    rien : on prefere une cellule vide.
    """
    num, den = _nombre(numerateur), _nombre(denominateur)
    if num is None or den is None or den <= 0:
        return None
    return num / den


def comptes(ticker, trimestriel=False):
    """Les trois etats financiers, en {date de cloture: {poste: valeur}}."""
    t = yf.Ticker(ticker)
    prefixe = "quarterly_" if trimestriel else ""
    tables = {}
    for cle, attribut in (
        ("income", "income_stmt"),
        ("bilan", "balance_sheet"),
        ("flux", "cashflow"),
    ):
        try:
            tables[cle] = getattr(t, prefixe + attribut)
        except Exception as erreur:  # noqa: BLE001 — signale, puis poste laisse vide
            # ne jamais avaler : une panne reseau se confondrait avec une
            # absence de donnee, et la serie basculerait sur le repli du § 3
            print(
                f"{ticker} : {prefixe + attribut} a echoue "
                f"({erreur.__class__.__name__}: {erreur})",
                file=sys.stderr,
            )
            tables[cle] = None

    periodes = {}
    for cle, table in tables.items():
        if table is None or table.empty:
            continue
        for colonne in table.columns:
            cloture = pd.Timestamp(colonne).tz_localize(None).normalize()
            periodes.setdefault(cloture, {})
            for poste, (origine, libelle) in POSTES.items():
                if origine == cle and libelle in table.index:
                    periodes[cloture][poste] = _nombre(table.loc[libelle, colonne])

    # Les trois etats n'ont pas la meme profondeur : une periode presente dans un
    # seul d'entre eux et dont tous les postes sont vides ne produirait que des
    # lignes creuses. On l'ecarte ; une periode partiellement renseignee reste.
    return {
        cloture: postes
        for cloture, postes in periodes.items()
        if any(v is not None for v in postes.values())
    }


def publications(ticker):
    """Les dates d'annonce PASSEES : celles dont l'EPS est effectivement publie.

    Les annonces a venir sont ecartees — les utiliser serait le regard en avant
    sous sa forme la plus directe.
    """
    try:
        table = yf.Ticker(ticker).get_earnings_dates(limit=LIMITE_ANNONCES)
    except Exception as erreur:  # noqa: BLE001 — signale, puis repli du § 3
        # ne jamais avaler : sans ce message, toutes les dates basculeraient
        # silencieusement sur le repli, et la serie perdrait son interet
        print(
            f"{ticker} : get_earnings_dates a echoue "
            f"({erreur.__class__.__name__}: {erreur})",
            file=sys.stderr,
        )
        return []
    if table is None or table.empty or "Reported EPS" not in table.columns:
        return []
    passees = table[table["Reported EPS"].notna()]
    return sorted(pd.to_datetime(passees.index).tz_localize(None).normalize())


def apparier(periodes, dates_publication, decalage):
    """Pour chaque cloture, sa date de publication et si elle est estimee."""
    apparie = {}
    for cloture in sorted(periodes):
        suivantes = [d for d in dates_publication if d > cloture]
        if suivantes:
            apparie[cloture] = (suivantes[0], False)
        else:
            apparie[cloture] = (cloture + pd.Timedelta(days=decalage), True)
    return apparie


def serie_actions(ticker, calendrier):
    """get_shares_full() reporte en avant sur le calendrier des seances.

    Pas de report en arriere : les seances anterieures au premier point connu
    restent vides plutot que d'inventer un nombre d'actions.
    """
    try:
        brute = yf.Ticker(ticker).get_shares_full(
            start=(calendrier.min() - timedelta(days=400)).date().isoformat()
        )
    except Exception as erreur:  # noqa: BLE001 — signale, puis colonne ACTIONS vide
        print(
            f"{ticker} : get_shares_full a echoue "
            f"({erreur.__class__.__name__}: {erreur}) — colonne ACTIONS vide",
            file=sys.stderr,
        )
        return pd.Series(index=calendrier, dtype="float64")
    if brute is None or len(brute) == 0:
        return pd.Series(index=calendrier, dtype="float64")
    brute.index = pd.to_datetime(brute.index).tz_localize(None).normalize()
    brute = brute[~brute.index.duplicated(keep="last")].sort_index()
    return brute.reindex(calendrier.union(brute.index)).ffill().reindex(calendrier)


def reconstituer(ticker, debut, fin, trimestriel, decalage):
    """Assemble le panel seance par seance. Rend (lignes, diagnostic)."""
    periodes = comptes(ticker, trimestriel)
    if not periodes:
        return [], {"erreur": "aucun compte disponible"}

    dates_publication = publications(ticker)
    apparie = apparier(periodes, dates_publication, decalage)
    premiere = min(p for p, _ in apparie.values())

    depart = max(pd.Timestamp(debut), premiere) if debut else premiere
    arrivee = pd.Timestamp(fin) if fin else pd.Timestamp(date.today())
    if depart > arrivee:
        return [], {"erreur": f"rien de publie avant le {arrivee.date()}"}

    cours = yf.Ticker(ticker).history(
        start=depart.date().isoformat(),
        end=(arrivee + pd.Timedelta(days=1)).date().isoformat(),
    )
    if cours.empty:
        return [], {"erreur": "aucun cours sur la periode"}
    cours.index = pd.to_datetime(cours.index).tz_localize(None).normalize()
    actions = serie_actions(ticker, cours.index)

    # (publication, cloture) triees : a la seance d on prend la derniere publiee
    calendrier = sorted(
        ((pub, cloture) for cloture, (pub, _) in apparie.items()), key=lambda x: x[0]
    )

    lignes = []
    for jour, cloture_cours in cours["Close"].items():
        prix = _nombre(cloture_cours)
        if prix is None:
            continue  # jour en cours, cotation suspendue : pas de ligne creuse
        connues = [(pub, exo) for pub, exo in calendrier if pub <= jour]
        if not connues:
            continue
        pub, exercice = connues[-1]
        p = periodes[exercice]
        nb = _nombre(actions.get(jour))
        capi = prix * nb if prix is not None and nb is not None else None

        dette, tresorerie = _nombre(p.get("dette")), _nombre(p.get("tresorerie"))
        ve = None
        if capi is not None and dette is not None:
            ve = capi + dette - (tresorerie or 0.0)

        lignes.append(
            {
                "DATE": jour.date().isoformat(),
                "TICKER": ticker,
                "CLOTURE": prix,
                "ACTIONS": nb,
                "CAPI": capi,
                "VE": ve,
                "PER": _rapport(capi, p.get("resultat_net")),
                "P_B": _rapport(capi, p.get("fonds_propres")),
                "VE_EBITDA": _rapport(ve, p.get("ebitda")),
                "REND_FCF": (
                    None
                    if _rapport(p.get("fcf"), capi) is None
                    else 100 * _rapport(p.get("fcf"), capi)
                ),
                "ROE": (
                    None
                    if _rapport(p.get("resultat_net"), p.get("fonds_propres")) is None
                    else 100 * _rapport(p.get("resultat_net"), p.get("fonds_propres"))
                ),
                "MARGE_NETTE": (
                    None
                    if _rapport(p.get("resultat_net"), p.get("chiffre_affaires")) is None
                    else 100
                    * _rapport(p.get("resultat_net"), p.get("chiffre_affaires"))
                ),
                "MARGE_OP": (
                    None
                    if _rapport(p.get("resultat_operationnel"), p.get("chiffre_affaires"))
                    is None
                    else 100
                    * _rapport(
                        p.get("resultat_operationnel"), p.get("chiffre_affaires")
                    )
                ),
                "DETTE_EBITDA": _rapport(p.get("dette"), p.get("ebitda")),
                "EXERCICE": exercice.date().isoformat(),
                "PUBLICATION": pub.date().isoformat(),
                "PUBLICATION_ESTIMEE": 1 if apparie[exercice][1] else 0,
            }
        )

    diagnostic = {
        "periodes": len(periodes),
        "reelles": sum(1 for _, estimee in apparie.values() if not estimee),
        "estimees": sum(1 for _, estimee in apparie.values() if estimee),
        "publications": len(dates_publication),
        "actions_min": _nombre(actions.min()),
        "actions_max": _nombre(actions.max()),
    }
    return lignes, diagnostic


def formater(valeur, colonne):
    """Arrondi a l'ecriture. Chaine vide si la valeur manque."""
    if valeur is None:
        return ""
    if isinstance(valeur, str):
        return valeur
    return f"{valeur:.{DECIMALES.get(colonne, 0)}f}"


def mediane(lignes, colonne):
    valeurs = sorted(x[colonne] for x in lignes if x[colonne] is not None)
    if not valeurs:
        return None
    milieu = len(valeurs) // 2
    if len(valeurs) % 2:
        return valeurs[milieu]
    return (valeurs[milieu - 1] + valeurs[milieu]) / 2


def main():
    parser = argparse.ArgumentParser(
        description="Reconstitue une serie historique de ratios fondamentaux, en "
        "n'utilisant a chaque date que ce qui etait publie a cette date."
    )
    parser.add_argument("tickers", nargs="*", help="Tickers Yahoo, ex : AIR.PA BNP.PA")
    parser.add_argument("--debut", help="Date de debut AAAA-MM-JJ")
    parser.add_argument("--fin", help="Date de fin AAAA-MM-JJ (defaut : aujourd'hui)")
    parser.add_argument(
        "--trimestriel", action="store_true", help="Comptes trimestriels au lieu d'annuels"
    )
    parser.add_argument(
        "--mensuel", action="store_true", help="Ne garder que la derniere seance de chaque mois"
    )
    parser.add_argument(
        "--decalage",
        type=int,
        default=DECALAGE_DEFAUT,
        help=f"Decalage de repli en jours quand aucune publication reelle "
        f"n'est trouvee (defaut : {DECALAGE_DEFAUT})",
    )
    parser.add_argument("--csv", help="Chemin de sortie (un fichier par ticker)")
    args = parser.parse_args()

    tickers = args.tickers
    if not tickers:
        saisie = input("Ticker(s) Yahoo (ex. AIR.PA BNP.PA) : ").strip()
        tickers = [t for t in saisie.replace(",", " ").split() if t]
    tickers = [t.upper() for t in tickers]
    if not tickers:
        print("Aucun ticker fourni.", file=sys.stderr)
        sys.exit(1)

    reussis = 0
    for ticker in tickers:
        lignes, diag = reconstituer(
            ticker, args.debut, args.fin, args.trimestriel, args.decalage
        )
        if not lignes:
            print(f"{ticker} : {diag.get('erreur', 'aucune ligne')}", file=sys.stderr)
            continue
        if args.mensuel:
            garde = {}
            for ligne in lignes:
                garde[ligne["DATE"][:7]] = ligne
            lignes = [garde[m] for m in sorted(garde)]

        nom = f"historique_{ticker.replace('.', '_')}_{lignes[0]['DATE']}_{lignes[-1]['DATE']}.csv"
        chemin = Path(args.csv) if args.csv else REPERTOIRE_DEFAUT / nom
        chemin.parent.mkdir(parents=True, exist_ok=True)
        with chemin.open("w", encoding="utf-8-sig", newline="") as f:
            redacteur = csv.writer(f)
            redacteur.writerow(COLONNES)
            for ligne in lignes:
                redacteur.writerow([formater(ligne.get(c), c) for c in COLONNES])

        reussis += 1
        estimees = sum(1 for x in lignes if x["PUBLICATION_ESTIMEE"])
        print(f"{ticker:<9}{len(lignes)} lignes du {lignes[0]['DATE']} au {lignes[-1]['DATE']}")
        print(
            f"{'':<9}{diag['periodes']} periodes, {diag['reelles']} publications reelles, "
            f"{diag['estimees']} estimee(s) — {estimees} lignes concernees"
        )
        if diag["actions_min"] is not None:
            mini = f"{diag['actions_min']:,.0f}".replace(",", " ")
            maxi = f"{diag['actions_max']:,.0f}".replace(",", " ")
            print(f"{'':<9}actions : {mini} -> {maxi} (serie brute, non corrigee)")
        med_per, med_pb = mediane(lignes, "PER"), mediane(lignes, "P_B")
        print(
            f"{'':<9}PER median {formater(med_per, 'PER')} · "
            f"P/B median {formater(med_pb, 'P_B')}"
        )
        print(f"{'':<9}ecrit dans {chemin}")

    if not reussis:
        print("Aucun ticker exploitable.", file=sys.stderr)
        sys.exit(1)

    print(
        "\nReserves : le contenu des comptes n'est pas garanti conforme au publie "
        "(PER et marges solides,\nmultiples d'EBITDA et FCF beaucoup moins), l'univers "
        "exclut les valeurs radiees,\net la profondeur est plafonnee par la source."
    )


if __name__ == "__main__":
    main()
