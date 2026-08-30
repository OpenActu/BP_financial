#!/usr/bin/env python3
"""
Historique des dividendes et des divisions du nominal, depuis les archives
bnains.org, confronte a ce que rend yfinance.

Trois apports que Yahoo ne donne pas : les anciennes composantes du CAC 40 (donc
une prise sur le biais du survivant), la date d'annonce, et la ventilation
acompte / solde / exceptionnel.

Dependance externe :
    yfinance, pour le controle croise. Ni requests, ni beautifulsoup4.

Utilisation :
    python python/import_dividendes.py --index
    python python/import_dividendes.py NL0000235190 --ticker AIR.PA
    python python/import_dividendes.py FR0000125007 FR0000120404
    python python/import_dividendes.py --toutes --delai 2

ATTENTION a la colonne « Dividende brut » de la source : pour les annees a
retenue a la source, elle porte un montant qui en est deja NET, et le commentaire
de la ligne le dit. Le script produit donc MONTANT (tel que publie) et
MONTANT_BRUT (reconstruit depuis le commentaire) ; c'est le second qui se compare
a yfinance.

Ce script ne donne ni cours, ni comptes : il ne resout rien du probleme de
profondeur des ratios de valorisation.
"""

import argparse
import csv
import html as html_module
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

BASE = "https://www.bnains.org/archives/action.php"
AGENT = "BP_financial/1.0 (script de recherche personnel)"
DELAI_MINIMAL = 1.0
REPERTOIRE_DEFAUT = Path("docs/raw/dividendes")

ENTETE_ATTENDUE = [
    "Date annonce",
    "Date détachement",
    "Date versement",
    "Année réf.",
    "Type",
    "Dividende brut",
    "Dividende normalisé",
    "Rendement annuel",
    "Commentaires",
]

COLONNES = [
    "ISIN", "SOCIETE", "ANNONCE", "DETACHEMENT", "VERSEMENT", "ANNEE_REF",
    "TYPE", "MONTANT", "MONTANT_BRUT", "RETENUE_PCT", "NORMALISE",
    "RENDEMENT", "COMMENTAIRE",
]

COLONNES_DIVISIONS = [
    "ISIN", "SOCIETE", "DATE_DIVISION", "DIVISEUR",
    "DATE_DERNIER_COURS", "DERNIER_COURS", "COMMENTAIRE",
]


def _texte(brut):
    """Retire les balises, decode les entites, normalise les espaces."""
    sans_balise = re.sub(r"<[^>]+>", " ", brut)
    decode = html_module.unescape(sans_balise).replace(" ", " ")
    return re.sub(r"\s+", " ", decode).strip()


def telecharger(isin, cache, delai, rafraichir):
    """Requete polie avec cache local. Rend le HTML, ou None en cas d'echec."""
    fichier = cache / f"{isin or 'index'}.html"
    if fichier.exists() and not rafraichir:
        return fichier.read_text(encoding="utf-8", errors="replace")

    url = BASE if isin is None else f"{BASE}?codeISIN={isin}"
    requete = urllib.request.Request(url, headers={"User-Agent": AGENT})
    try:
        with urllib.request.urlopen(requete, timeout=30) as reponse:
            contenu = reponse.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as erreur:
        print(f"{isin} : echec reseau ({erreur.__class__.__name__})", file=sys.stderr)
        return None
    time.sleep(delai)  # apres la requete : on n'attend jamais pour rien
    cache.mkdir(parents=True, exist_ok=True)
    fichier.write_text(contenu, encoding="utf-8")
    return contenu


def cellules(source, identifiant=None):
    """Les <td> d'un tableau, decodes. identifiant=None : le premier sans id."""
    if identifiant:
        motif = rf'<table id="{identifiant}".*?</table>'
    else:
        motif = r'<table class="table table-hover[^"]*"\s+style.*?</table>'
    trouve = re.search(motif, source, re.DOTALL)
    if not trouve:
        return []
    return [_texte(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", trouve.group(0), re.DOTALL)]


def decouper(liste, largeur):
    """Groupes de `largeur` cellules, en-tete exclu. Ignore un reste partiel."""
    corps = liste[largeur:]
    return [corps[i : i + largeur] for i in range(0, len(corps) - largeur + 1, largeur)]


def verifier_entete(entete):
    """Garde-fou : la source peut changer sa mise en page sans prevenir."""
    normalise = [re.sub(r"\s+", " ", c).strip() for c in entete]
    return normalise == ENTETE_ATTENDUE


def date_iso(texte):
    """JJ/MM/AAAA -> AAAA-MM-JJ. Vide pour '-', '?' et l'absence de date."""
    trouve = re.match(r"(\d{2})/(\d{2})/(\d{4})", texte.strip())
    if not trouve:
        return None
    jour, mois, annee = trouve.groups()
    return f"{annee}-{mois}-{jour}"


def montant(texte):
    """« 3.200 € » -> 3.2. Accepte la virgule decimale."""
    trouve = re.search(r"(-?[\d]+[.,]?[\d]*)", texte.replace(" ", ""))
    if not trouve:
        return None
    try:
        return float(trouve.group(1).replace(",", "."))
    except ValueError:
        return None


def brut_et_retenue(commentaire):
    """Extrait le montant brut reel et le taux de retenue annonces en clair."""
    brut = re.search(r"[Dd]ividende brut\s*=\s*([\d]+[.,]?[\d]*)", commentaire)
    retenue = re.search(r"(\d+)\s*%\s*de retenue", commentaire)
    return (
        float(brut.group(1).replace(",", ".")) if brut else None,
        int(retenue.group(1)) if retenue else None,
    )


def societe(source):
    """Le nom de la societe, depuis le titre de la page."""
    trouve = re.search(r"<title>(.*?)</title>", source, re.DOTALL)
    if not trouve:
        return ""
    titre = _texte(trouve.group(1))
    # « Historique des dividendes et divisions de l'action Airbus Group » -> « Airbus Group »
    return re.sub(r"^.*?\bde l'action\s+|^Historique des dividendes\s*", "", titre).strip()


def lire_index(source):
    """Les couples (ISIN, societe) de la page d'index, sans doublon."""
    vus = {}
    for isin, libelle in re.findall(
        r"action\.php\?codeISIN=([A-Z0-9]+)[^>]*>(.*?)</a>", source, re.DOTALL
    ):
        nom = _texte(libelle)
        if nom and nom != isin:
            vus[isin] = nom
        vus.setdefault(isin, isin)
    return sorted(vus.items(), key=lambda x: x[1])


def analyser(isin, source):
    """Rend (lignes de dividendes, lignes de divisions, nom de societe)."""
    nom = societe(source)
    brutes = cellules(source, "table_dividendes")
    if not brutes:
        return [], [], nom
    if not verifier_entete(brutes[:9]):
        print(
            f"{isin} : en-tete inattendu {brutes[:9]} — la source a change de "
            f"mise en page, analyse interrompue",
            file=sys.stderr,
        )
        sys.exit(2)

    lignes = []
    for g in decouper(brutes, 9):
        commentaire = g[8].replace(";", ",")
        valeur = montant(g[5])
        brut, retenue = brut_et_retenue(commentaire)
        lignes.append(
            {
                "ISIN": isin,
                "SOCIETE": nom,
                "ANNONCE": date_iso(g[0]),
                "DETACHEMENT": date_iso(g[1]),
                "VERSEMENT": date_iso(g[2]),
                "ANNEE_REF": g[3].strip() or None,
                "TYPE": g[4].strip() or None,
                "MONTANT": valeur,
                # a defaut de mention explicite, le publie est deja le brut
                "MONTANT_BRUT": brut if brut is not None else valeur,
                "RETENUE_PCT": retenue,
                "NORMALISE": montant(g[6]),
                "RENDEMENT": montant(g[7]) if "%" in g[7] else None,
                "COMMENTAIRE": commentaire or None,
            }
        )

    divisions = []
    for g in decouper(cellules(source), 5):
        if not date_iso(g[0]):
            continue
        divisions.append(
            {
                "ISIN": isin,
                "SOCIETE": nom,
                "DATE_DIVISION": date_iso(g[0]),
                "DIVISEUR": montant(g[1]),
                "DATE_DERNIER_COURS": date_iso(g[2]),
                "DERNIER_COURS": montant(g[3]),
                "COMMENTAIRE": g[4].replace(";", ",") or None,
            }
        )
    return lignes, divisions, nom


def controler(lignes, ticker):
    """Confronte les MONTANT_BRUT, par date de detachement, a yfinance."""
    import yfinance as yf

    try:
        serie = yf.Ticker(ticker).dividends
    except Exception as erreur:  # noqa: BLE001 — controle facultatif : on signale et on continue
        print(f"{ticker} : controle impossible ({erreur.__class__.__name__})", file=sys.stderr)
        return None
    if serie is None or len(serie) == 0:
        return None
    cote = {str(k)[:10]: float(v) for k, v in serie.items()}

    # la source separe solde et exceptionnel la ou yfinance agrege
    source = {}
    retenues = {}
    for ligne in lignes:
        jour = ligne["DETACHEMENT"]
        if not jour or ligne["MONTANT_BRUT"] is None:
            continue
        source[jour] = source.get(jour, 0.0) + ligne["MONTANT_BRUT"]
        if ligne["RETENUE_PCT"]:
            retenues[jour] = ligne["RETENUE_PCT"]

    verdicts = {"identique": 0, "retenue": 0, "ecart": 0, "orpheline": 0}
    details = []
    for jour in sorted(set(source) | set(cote)):
        a, b = source.get(jour), cote.get(jour)
        if a is None or b is None or b == 0:
            verdicts["orpheline"] += 1
            details.append((jour, a, b, "presente d'un seul cote"))
            continue
        rapport = a / b
        if abs(rapport - 1) < 0.005:
            verdicts["identique"] += 1
        elif jour in retenues and abs(rapport - (1 - retenues[jour] / 100)) < 0.005:
            verdicts["retenue"] += 1
            details.append((jour, a, b, f"retenue {retenues[jour]}%"))
        else:
            verdicts["ecart"] += 1
            details.append((jour, a, b, f"ECART rapport {rapport:.4f}"))
    return verdicts, details


def ecrire(chemin, colonnes, lignes):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8-sig", newline="") as f:
        redacteur = csv.writer(f)
        redacteur.writerow(colonnes)
        for ligne in lignes:
            redacteur.writerow(
                ["" if ligne.get(c) is None else ligne[c] for c in colonnes]
            )


def main():
    parser = argparse.ArgumentParser(
        description="Historique des dividendes depuis bnains.org, confronte a yfinance."
    )
    parser.add_argument("isins", nargs="*", help="Codes ISIN, ex : NL0000235190")
    parser.add_argument("--index", action="store_true", help="Lister les valeurs disponibles")
    parser.add_argument("--toutes", action="store_true", help="Traiter tout l'index")
    parser.add_argument("--ticker", help="Ticker Yahoo pour le controle croise")
    parser.add_argument("--divisions", action="store_true", help="Ecrire aussi les divisions")
    parser.add_argument(
        "--delai",
        type=float,
        default=1.5,
        help=f"Secondes entre deux requetes (plancher : {DELAI_MINIMAL})",
    )
    parser.add_argument("--rafraichir", action="store_true", help="Ignorer le cache local")
    parser.add_argument("--csv", help="Chemin du CSV de sortie")
    args = parser.parse_args()

    delai = args.delai
    if delai < DELAI_MINIMAL:
        print(f"Delai releve de {delai} a {DELAI_MINIMAL} s : on interroge un tiers.")
        delai = DELAI_MINIMAL

    cache = REPERTOIRE_DEFAUT / "cache"
    if args.index or args.toutes:
        source = telecharger(None, cache, delai, args.rafraichir)
        if source is None:
            sys.exit(1)
        valeurs = lire_index(source)
        if args.index:
            print(f"{len(valeurs)} valeurs proposees par la source :\n")
            for isin, nom in valeurs:
                print(f"  {isin}  {nom}")
            return
        isins = [isin for isin, _ in valeurs]
    else:
        isins = [i.upper() for i in args.isins]
        if not isins:
            saisie = input("Code(s) ISIN (ex. NL0000235190) : ").strip()
            isins = [i.upper() for i in saisie.replace(",", " ").split() if i]

    if not isins:
        print("Aucun ISIN fourni.", file=sys.stderr)
        sys.exit(1)
    if args.ticker and len(isins) > 1:
        print("--ticker n'a de sens que pour un seul ISIN.", file=sys.stderr)
        sys.exit(1)

    toutes, toutes_divisions = [], []
    for isin in isins:
        source = telecharger(isin, cache, delai, args.rafraichir)
        if source is None:
            continue
        lignes, divisions, nom = analyser(isin, source)
        if not lignes:
            print(f"{isin} : aucun tableau de dividendes", file=sys.stderr)
            continue
        toutes.extend(lignes)
        toutes_divisions.extend(divisions)

        annees = [x["ANNEE_REF"] for x in lignes if x["ANNEE_REF"]]
        types = {}
        for x in lignes:
            types[x["TYPE"]] = types.get(x["TYPE"], 0) + 1
        avec_retenue = sum(1 for x in lignes if x["RETENUE_PCT"])
        print(f"\n{nom or isin:<38}{isin}")
        print(
            f"  {len(lignes)} dividendes de {min(annees)} a {max(annees)}"
            f" · {len(divisions)} division(s)"
        )
        print("  types : " + " · ".join(f"{t} {n}" for t, n in sorted(types.items())))
        if avec_retenue:
            print(f"  retenue a la source signalee sur {avec_retenue} ligne(s)")

        if args.ticker:
            resultat = controler(lignes, args.ticker)
            if resultat:
                verdicts, details = resultat
                print(
                    f"  controle {args.ticker} : {verdicts['identique']} identiques · "
                    f"{verdicts['retenue']} expliques par la retenue · "
                    f"{verdicts['ecart']} ecart(s) · {verdicts['orpheline']} orpheline(s)"
                )
                for jour, a, b, motif in details:
                    a_txt = "—" if a is None else f"{a:.3f}"
                    b_txt = "—" if b is None else f"{b:.3f}"
                    print(f"      {jour}  source {a_txt:>7}  yfinance {b_txt:>7}  {motif}")

    if not toutes:
        print("Aucune valeur exploitable.", file=sys.stderr)
        sys.exit(1)

    chemin = (
        Path(args.csv)
        if args.csv
        else REPERTOIRE_DEFAUT / f"dividendes_{date.today().isoformat()}.csv"
    )
    ecrire(chemin, COLONNES, toutes)
    print(f"\n{len(toutes)} dividendes ecrits dans : {chemin}")

    if args.divisions:
        chemin_div = chemin.with_name(chemin.name.replace("dividendes_", "divisions_"))
        ecrire(chemin_div, COLONNES_DIVISIONS, toutes_divisions)
        print(f"{len(toutes_divisions)} divisions ecrites dans : {chemin_div}")


if __name__ == "__main__":
    main()
