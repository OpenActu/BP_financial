"""Moteur de l'experience 3 : 2022 rejouee sur tout le CAC 40, a sa composition du jour.

Lit l'univers point-in-time de univers.csv, classe a chaque fin de mois a partir
des cinq criteres de la regle du module 3, APPLIQUE ses quatre vetos, en deduit
les ordres, execute a l'ouverture suivante, comptabilise, engendre et depouille
des theses refutables normalisees, conserve les figures de decision, et ecrit les
graphiques.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_3/journal.py --collecter --taches 12
    python docs/done/experimentation/experience_3/journal.py --markdown
    python docs/done/experimentation/experience_3/journal.py --mois 2022-03
"""

import argparse
import csv
import datetime
import math
import os
import re
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REFERENCE = "TR39"
REFERENCE_NUE = "^FCHI"
RAPPORTS = "rapports"
GRAPHIQUES = "graphiques"
ANNEE = "2022"
BILAN = f"bilan-{ANNEE}.md"
DEBUT_SERIE = "2019-01-02"   # premiere seance des CSV, trois ans d'amorce
FIN_SERIE = "2022-12-30"     # derniere seance des CSV
MOIS_AUDIT_DEBUT = "2020-12"     # premiere date de decision de la fenetre d'audit
MOIS_INVESTI_DEBUT = "2021-12"   # premiere date de decision investie
MOIS_ETALONNAGE_FIN = "2021-11"  # derniere date de decision de l'etalonnage
COUPLES_AUDIT = 24
COUPLES_INVESTIS = 12

FENETRE = 120        # piste C1 : parametres d'encadrement DECLARES, pas subis
TOLERANCE = 0.25
VARIANTES = (
    ("VAR-F60", 60, 0.25),
    ("VAR-F180", 180, 0.25),
    ("VAR-T015", 120, 0.15),
    ("VAR-T040", 120, 0.40),
)

SEUIL_BAS = 35.0             # s3 aligne sur la regle du module 3
SEUIL_HAUT = 65.0
SEUIL_BAS_FANTOME = 20.0     # s3 au sens de l'experience 1
SEUIL_HAUT_FANTOME = 50.0
FENETRE_SIGMA = 12           # piste S3 : mois d'ecarts servant a sigma
DEMI_BORNE = 0.5             # piste S3 : bornes de phase, en multiples de sigma
DECALAGES = (1, 2)
CADENCE_ECRITURE = 48   # criteres.csv est depose tous les 48 resultats
TE_DECLAREE = 8.20           # tracking error publiee au README avant la premiere seance
Z95 = 1.96

COURTAGE = 0.10
SPREAD = 0.015
TTF = 0.30
EXEMPTES_TTF = ("AIR.PA", "STLAP.PA", "MT.AS", "STMPA.PA")

# Valeurs dont le fournisseur a repercute RETROACTIVEMENT une division survenue
# APRES FIN_SERIE. Toutes les quantites que la regle calcule sont invariantes
# d'echelle ; le NOMBRE DE TITRES achetables ne l'est pas. Acheter sur un cours
# retro-ajuste serait laisser une operation posterieure faconner le portefeuille.
SPLITS_POSTERIEURS = {
    "AI.PA": "2024-06-10 et 2026-06-08, attributions gratuites 1,1 (facteur 0,826)",
    "ATO.PA": "2025-04-24, regroupement 1 pour 10 000 (facteur 10 000)",
    "WLN.PA": "2026-06-15, regroupement 1 pour 40 (facteur 40)",
}

QUOTES_DEFAUT = Path("docs/raw/data/quotes")
REGLE = Path("python/generer_graph_decision.py")

ENTETE_CRITERES = [
    "DATE", "ROLE", "DATE_EVALUEE", "TICKER", "CLOSE", "TEND_120", "TEND_20",
    "POSITION", "ALPHA", "ALPHA_BAS", "ALPHA_HAUT", "MOMENTUM", "SUPPORT",
    "RESISTANCE", "PENTE_SUP", "PENTE_RES", "PORTEE_SUP", "PORTEE_RES",
    "EPISODES_SUP", "EPISODES_RES", "LARGEUR", "TAU", "VETOS", "VERDICT",
    "DIAGNOSTIC",
]
MESURES = [
    "CLOSE", "TEND_120", "TEND_20", "POSITION", "ALPHA", "ALPHA_BAS",
    "ALPHA_HAUT", "MOMENTUM", "SUPPORT", "RESISTANCE", "PENTE_SUP", "PENTE_RES",
    "PORTEE_SUP", "PORTEE_RES", "EPISODES_SUP", "EPISODES_RES", "LARGEUR",
    "TAU", "VETOS", "VERDICT",
]
ENTETE_CLASSEMENT = [
    "DATE", "RANG", "TICKER", "S1", "S2", "S3", "S4", "S5", "SCORE",
    "POSITION", "MOMENTUM", "TAU", "VETOS", "VERDICT_REGLE",
]
ENTETE_ORDRES = [
    "DATE", "TICKER", "SENS", "QUANTITE", "PRIX", "BRUT", "FRAIS", "NET",
    "RANG", "SCORE", "VETOS", "MOTIF",
]
ENTETE_PORTEFEUILLE = ["DATE", "ESPECES", "TITRES", "TOTAL", "BASE100", "REFERENCE100"]
ENTETE_THESES = [
    "DATE", "TICKER", "TYPE", "PHASE", "ENONCE", "BORNE_BASSE", "BORNE_HAUTE",
    "BORNE_DEMENTI", "SIGMA", "DATE_DEPOUILLEMENT", "VALEUR_CONSTATEE", "VERDICT",
]

NBSP = " "
NL_ = chr(10)
EURO = "€"
MEDIAN = "·"
ABSENTE = "*(section absente)*"
FIGURE_ABSENTE = "*(figure absente)*"

MOIS_TITRE = {
    "01": "Janvier", "02": "Février", "03": "Mars", "04": "Avril",
    "05": "Mai", "06": "Juin", "07": "Juillet", "08": "Août",
    "09": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Décembre",
}

# Les noms d'affichage sont DECLARES ici : univers.csv rend les libelles de la
# source, heterogenes (« AIR LIQUIDE », « Cap Gemini », « Total »), utiles a
# l'appariement et impropres a la publication.
SOCIETES = {
    "ACA.PA": "Crédit Agricole", "AI.PA": "Air Liquide", "AIR.PA": "Airbus",
    "ALO.PA": "Alstom", "ATO.PA": "Atos", "BN.PA": "Danone",
    "BNP.PA": "BNP Paribas", "CA.PA": "Carrefour", "CAP.PA": "Capgemini",
    "CS.PA": "AXA", "DG.PA": "Vinci", "DSY.PA": "Dassault Systèmes",
    "EL.PA": "EssilorLuxottica", "EN.PA": "Bouygues", "ENGI.PA": "Engie",
    "ERF.PA": "Eurofins Scientific", "GLE.PA": "Société Générale",
    "HO.PA": "Thales", "KER.PA": "Kering", "LR.PA": "Legrand", "MC.PA": "LVMH",
    "ML.PA": "Michelin", "MT.AS": "ArcelorMittal", "OR.PA": "L'Oréal",
    "ORA.PA": "Orange", "PUB.PA": "Publicis", "RI.PA": "Pernod Ricard",
    "RMS.PA": "Hermès International", "RNO.PA": "Renault", "SAF.PA": "Safran",
    "SAN.PA": "Sanofi", "SGO.PA": "Saint-Gobain", "STLAP.PA": "Stellantis",
    "STMPA.PA": "STMicroelectronics", "SU.PA": "Schneider Electric",
    "TEP.PA": "Teleperformance", "TTE.PA": "TotalEnergies",
    "VIE.PA": "Veolia", "VIV.PA": "Vivendi", "WLN.PA": "Worldline",
}
LIBELLE_VETO = {
    1: "encadrement illisible (moins de 3 épisodes de contact)",
    2: "canal se refermant en moins de 20 séances",
    3: "critères 1 et 2 de signes opposés",
    4: "historique de moins de 120 séances",
}
ISSUE_VETO = {
    1: "tenue de la thèse `CANAL`",
    2: "tenue de la thèse `CANAL`",
    3: "stabilité de `s3` à d−1",
    4: "*(aucune — veto arithmétique)*",
}
LIBELLE_COMPOSANTE = {
    0: "`s1` — tendance longue `TEND_120`",
    1: "`s2` — tendance courte `TEND_20`",
    2: "`s3` — position dans l'encadrement",
    3: "`s4` — momentum 12-1",
    4: "`s5` — alpha annualisé, IC95",
}


def erreur(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def fr(x, decimales=2):
    """Met en forme un nombre a la francaise : virgule, espace fine insecable."""
    if x is None:
        return "—"
    texte = f"{x:,.{decimales}f}".replace(",", "\x00").replace(".", ",")
    return texte.replace("\x00", NBSP)


def signe(x, decimales=2):
    return "—" if x is None else ("+" if x >= 0 else "") + fr(x, decimales)


def ent(x):
    """Une composante de score sur trois colonnes ; « . » quand elle est vide."""
    return "  ." if x is None else f"{x:+3d}"


def tau_texte(tau):
    """« inf » se lit ∞ ; le reste s'affiche en seances."""
    if tau is None:
        return "—"
    return "∞" if math.isinf(tau) else fr(tau, 1)


def ic95(succes, total):
    """Demi-largeur de l'IC a 95 % d'une proportion, en points."""
    if total <= 0:
        return None
    p = succes / total
    return 100 * Z95 * math.sqrt(p * (1 - p) / total)


def ic95_difference(a, na, b, nb):
    """Demi-largeur de l'IC a 95 % d'une difference de deux proportions, en points."""
    if na <= 0 or nb <= 0:
        return None
    pa, pb = a / na, b / nb
    return 100 * Z95 * math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)


def lendemain(jour):
    """« 2022-12-30 » -> « 2022-12-31 » : --fin est exclusif dans import_societe.py."""
    return (datetime.date.fromisoformat(jour) + datetime.timedelta(days=1)).isoformat()


def nom_fichier(ticker, quotes):
    """Rend le CSV de la plage declaree. Un glob choisirait le mauvais fichier
    des qu'une autre plage du meme ticker traine dans le repertoire."""
    chemin = quotes / f"{ticker.replace('.', '_')}_{DEBUT_SERIE}_{FIN_SERIE}.csv"
    if not chemin.exists():
        erreur(f"Serie absente : {chemin}\n"
               f"  python python/import_societe.py {ticker} "
               f"--debut {DEBUT_SERIE} --fin {lendemain(FIN_SERIE)}")
    return chemin


def charger_serie(chemin):
    """Rend {date: {'open': ..., 'close': ..., 'volume': ...}}, dates au jour."""
    serie = {}
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            if not ligne.get("Close"):
                continue
            ouverture = ligne.get("Open") or ""
            volume = ligne.get("Volume") or ""
            serie[ligne["Date"][:10]] = {
                "open": float(ouverture) if ouverture else float(ligne["Close"]),
                "close": float(ligne["Close"]),
                "volume": float(volume) if volume else 0.0,
            }
    return serie


def charger_univers(repertoire):
    """Rend (univers par date, exclusions par date, tous les tickers retenus)."""
    chemin = repertoire / "univers.csv"
    if not chemin.exists():
        erreur(f"{chemin} absent : l'univers point-in-time ne se devine pas")
    univers, exclusions = {}, {}
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            date = ligne["DATE_DECISION"]
            if ligne["RETENUE"] == "oui":
                univers.setdefault(date, []).append(ligne["TICKER"])
            else:
                exclusions.setdefault(date, []).append(
                    (ligne["NOM"], ligne["TICKER"], ligne["MOTIF"]))
    univers = {date: tuple(sorted(tickers)) for date, tickers in univers.items()}
    tous = sorted({t for tickers in univers.values() for t in tickers})
    manquants = [t for t in tous if t not in SOCIETES]
    if manquants:
        erreur("Tickers sans nom declare dans SOCIETES : " + ", ".join(manquants))
    return univers, exclusions, tuple(tous)


def charger_canaux(repertoire, tous):
    """Rend {ticker: (canal, grandeur)}. Un ticker non declare est fatal."""
    chemin = repertoire / "canaux.csv"
    if not chemin.exists():
        erreur(f"{chemin} absent : la piste S1 exige des canaux declares d'avance")
    canaux = {}
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            canaux[ligne["TICKER"]] = (ligne["CANAL"], ligne["GRANDEUR"])
    absents = [t for t in tous if t not in canaux]
    if absents:
        erreur("Valeurs sans canal declare dans canaux.csv : " + ", ".join(absents)
               + "\n  Un canal non declare serait un canal devine.")
    return canaux


def calendrier(dates):
    """Rend [(date de decision, date d'execution)] : derniere seance du mois m,
    premiere seance du mois m+1."""
    par_mois = {}
    for jour in dates:
        par_mois.setdefault(jour[:7], []).append(jour)
    mois = sorted(par_mois)
    return [(par_mois[cle][-1], par_mois[mois[i + 1]][0])
            for i, cle in enumerate(mois[:-1])]


def ecrire_csv(chemin, entete, lignes):
    """Ecrit un CSV, cellule vide plutot qu'un nombre invente."""
    with chemin.open("w", newline="", encoding="utf-8") as flux:
        plume = csv.DictWriter(flux, fieldnames=entete)
        plume.writeheader()
        for ligne in lignes:
            plume.writerow({c: ("" if ligne.get(c) is None else ligne[c]) for c in entete})


def ecrire_texte(chemin, texte):
    """Ecrit un markdown en LF : .gitattributes impose LF partout sauf .csv et .svg."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline=NL_) as flux:
        flux.write(texte)


# --------------------------------------------------------------------------
# Phase 1 : la collecte des criteres, par le code du depot

MOTIFS = {
    "TEND_120": r"Crit.re 1.*?:\s*([+-]?\d)",
    "TEND_20": r"Crit.re 2.*?:\s*([+-]?\d)",
    "POSITION": r"Crit.re 3.*?:\s*([+-]?[\d,]+)\s*%",
    "ALPHA": r"Crit.re 4.*?:\s*([+-]?[\d\s,  ]+?)\s*%/an",
    "MOMENTUM": r"Crit.re 5.*?:\s*([+-]?[\d\s,  ]+?)\s*%",
}
MOTIF_IC = (
    r"IC95\s*\[\s*([+-]?[\d\s,  ]+?)\s*;"
    r"\s*([+-]?[\d\s,  ]+?)\s*\]"
)


def nombre(texte):
    """Convertit « -11,38 » ou « +1 234,5 » en flottant. Rend None si illisible.

    Retire tout ce qui n'est ni chiffre, ni virgule, ni point, ni signe : les
    espaces fines insecables, le symbole euro et les unites disparaissent donc
    sans qu'il faille les enumerer.
    """
    if texte is None or texte == "":
        return None
    net = re.sub(r"[^\d,.+-]", "", texte).replace(",", ".")
    try:
        return float(net)
    except ValueError:
        return None


def ligne_debutant(sortie, prefixe):
    """Rend le corps (apres les deux-points) de la premiere ligne commencant ainsi."""
    for ligne in sortie.splitlines():
        if ligne.startswith(prefixe) and ":" in ligne:
            return ligne.split(":", 1)[1]
    return None


def encadrement(sortie, prefixe):
    """Tire (pente, portee, episodes, valeur) d'une ligne Support ou Resistance."""
    corps = ligne_debutant(sortie, prefixe)
    if corps is None:
        return None, None, None, None
    morceaux = [m.strip() for m in corps.split(MEDIAN)]
    if len(morceaux) < 4:
        return None, None, None, None
    pente = nombre(morceaux[0].replace("pente", "").split(EURO)[0])
    return pente, nombre(morceaux[1]), nombre(morceaux[2]), nombre(morceaux[3])


def largeur_et_tau(sortie):
    """Tire (largeur, tau) de la ligne « Largeur : 13,19 EUR (16,0 %) · τ = ... »."""
    corps = ligne_debutant(sortie, "Largeur")
    if corps is None:
        return None, None
    morceaux = [m.strip() for m in corps.split(MEDIAN)]
    largeur = nombre(morceaux[0].split("(")[0])
    if len(morceaux) < 2:
        return largeur, None
    reste = morceaux[1].split("=", 1)[-1]
    return largeur, (float("inf") if "∞" in reste else nombre(reste))


def extraire(sortie):
    """Tire les cinq criteres, l'encadrement, les vetos et le verdict de la console."""
    champs = {cle: nombre(t.group(1)) if (t := re.search(motif, sortie)) else None
              for cle, motif in MOTIFS.items()}
    ic = re.search(MOTIF_IC, sortie)
    champs["ALPHA_BAS"] = nombre(ic.group(1)) if ic else None
    champs["ALPHA_HAUT"] = nombre(ic.group(2)) if ic else None

    pente, portee, episodes, valeur = encadrement(sortie, "Support")
    champs.update({"PENTE_SUP": pente, "PORTEE_SUP": portee,
                   "EPISODES_SUP": episodes, "SUPPORT": valeur})
    pente, portee, episodes, valeur = encadrement(sortie, "Résistance")
    champs.update({"PENTE_RES": pente, "PORTEE_RES": portee,
                   "EPISODES_RES": episodes, "RESISTANCE": valeur})

    largeur, tau = largeur_et_tau(sortie)
    champs["LARGEUR"] = largeur
    champs["TAU"] = None if tau is None else ("inf" if math.isinf(tau) else tau)

    vetos = ligne_debutant(sortie, "Vetos")
    champs["VETOS"] = vetos.strip() if vetos else ""
    verdict = re.search(r"VERDICT\s*:\s*(\S+)", sortie)
    champs["VERDICT"] = verdict.group(1) if verdict else ""
    return champs


def dates_a_evaluer(audit, investis, dates_ref, univers):
    """Rend [(date de decision, role, date evaluee, fenetre, tolerance, ticker)].

    Les decalages vont vers l'ARRIERE : reculer d'une seance n'utilise que des
    seances deja connues a la date de decision. Avancer supposerait une seance
    posterieure, ce que le depot interdit partout.
    """
    rang = {jour: i for i, jour in enumerate(dates_ref)}
    taches = []
    for decision, _ in audit:
        for ticker in univers[decision]:
            taches.append((decision, "DECISION", decision, FENETRE, TOLERANCE, ticker))
    for decision, _ in investis:
        for pas in DECALAGES:
            i = rang[decision] - pas
            if i < 0:
                continue
            for ticker in univers[decision]:
                taches.append((decision, f"DECALE-{pas}", dates_ref[i],
                               FENETRE, TOLERANCE, ticker))
    for role, fenetre, tolerance in VARIANTES:
        for decision, _ in audit:
            for ticker in univers[decision]:
                taches.append((decision, role, decision, fenetre, tolerance, ticker))
    return taches


def chemin_figure(repertoire, ticker, date):
    """Une figure propre a une societe va dans un sous-repertoire a son ticker.

    A plat, 467 fichiers dans un meme repertoire ne se parcourent ni par societe
    ni dans le temps, et l'on ne voit pas ce qui manque apres une collecte
    interrompue. Le ticker reste dans le nom du fichier : un SVG deplace demeure
    identifiable. Les courbes du portefeuille, elles, restent a la racine.
    """
    return repertoire / GRAPHIQUES / ticker / f"decision-{ticker}-{date}.svg"


def evaluer_un(travail, quotes, chemin_reference, series, repertoire, narrees):
    """Lance la regle sur un couple (valeur, date) et rend sa ligne de criteres.

    L'environnement du fils porte PYTHONIOENCODING=utf-8 : sans lui, il ecrit sa
    console en cp1252 sous Windows, le pere la decode en utf-8, les expressions
    regulieres echouent sur les espaces fines et les « · », et TOUTES les lignes
    ressortent vides avec VERDICT = ERREUR, sans qu'aucun message ne le dise.
    """
    numero, (decision, role, evaluee, fenetre, tolerance, ticker) = travail
    conserver = role == "DECISION" and decision in narrees
    if conserver:
        sortie_svg = chemin_figure(repertoire, ticker, decision)
    else:
        sortie_svg = quotes.parent / GRAPHIQUES / f"_jetable_{numero % 64}.svg"
    sortie_svg.parent.mkdir(parents=True, exist_ok=True)
    issue = subprocess.run(
        [sys.executable, str(REGLE),
         "--csv", str(nom_fichier(ticker, quotes)),
         "--indice", str(chemin_reference),
         "--date", evaluee,
         "--fenetre", str(fenetre),
         "--tolerance", str(tolerance),
         "--sortie", str(sortie_svg)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )
    diagnostic = ""
    if issue.returncode != 0:
        champs = dict.fromkeys(MESURES)
        champs["VETOS"] = ""
        champs["VERDICT"] = "ERREUR"
        detail = [ligne.strip() for ligne in issue.stderr.splitlines() if ligne.strip()]
        diagnostic = f"code {issue.returncode}"
        if detail:
            diagnostic += " : " + detail[-1][:160]
    else:
        champs = extraire(issue.stdout)
    seance = series[ticker].get(evaluee)
    return {
        "DATE": decision, "ROLE": role, "DATE_EVALUEE": evaluee, "TICKER": ticker,
        "CLOSE": seance["close"] if seance else None,
        **{cle: champs.get(cle) for cle in MESURES if cle != "CLOSE"},
        "DIAGNOSTIC": diagnostic,
    }


def collecter(taches, quotes, repertoire, series, parallele, narrees, reprendre=True):
    """Lance la regle du depot sur chaque tache et ecrit criteres.csv.

    Les sous-processus tournent en parallele — l'essentiel de leur duree est
    l'import de pandas, pas le calcul. L'ordre des lignes ecrites est celui des
    taches, jamais celui des retours : criteres.csv est identique d'une
    execution a l'autre, quel que soit --taches.

    La collecte est REPRENABLE : les lignes deja presentes sont conservees, et
    le fichier est redepose tous les CADENCE_ECRITURE resultats.
    """
    chemin = repertoire / "criteres.csv"
    connus = {}
    if reprendre and chemin.exists():
        with chemin.open(encoding="utf-8") as flux:
            for ligne in csv.DictReader(flux):
                connus[(ligne["DATE"], ligne["ROLE"], ligne["TICKER"])] = ligne

    chemin_reference = nom_fichier(REFERENCE, quotes)

    def cle(travail):
        return (travail[0], travail[1], travail[5])

    def deposer():
        """Depot ATOMIQUE : on ecrit a cote, puis on remplace.

        Une collecte de 5 549 evaluations dure une demi-heure et sera interrompue.
        Ecrire en place exposerait criteres.csv a etre tronque au milieu d'un
        depot — et un fichier tronque se relit sans erreur, en silence.
        """
        provisoire = chemin.with_suffix(".csv.partiel")
        ecrire_csv(provisoire, ENTETE_CRITERES,
                   [connus[cle(t)] for t in taches if cle(t) in connus])
        provisoire.replace(chemin)

    manquants = [t for t in taches if cle(t) not in connus]
    if not manquants:
        print(f"  {len(connus)} evaluations deja presentes dans {chemin}")
        return
    print(f"  {len(connus)} deja connues, {len(manquants)} a evaluer")

    fait = 0
    with ThreadPoolExecutor(max_workers=parallele) as vivier:
        for ligne in vivier.map(
                lambda t: evaluer_un(t, quotes, chemin_reference, series,
                                     repertoire, narrees),
                enumerate(manquants)):
            connus[(ligne["DATE"], ligne["ROLE"], ligne["TICKER"])] = ligne
            fait += 1
            print(f"  [{fait:4d}/{len(manquants)}] {ligne['TICKER']:9s} "
                  f"{ligne['DATE_EVALUEE']} {ligne['ROLE']:10s}", end="\r")
            if fait % CADENCE_ECRITURE == 0:
                deposer()
    print(" " * 78, end="\r")
    for jetable in (quotes.parent / GRAPHIQUES).glob("_jetable_*.svg"):
        jetable.unlink()

    deposer()
    rates = sum(1 for ligne in connus.values() if ligne["VERDICT"] == "ERREUR")
    print(f"  {len(connus)} evaluations ecrites dans {chemin} · {rates} en erreur")


# --------------------------------------------------------------------------
# Phase 2 : le score, les vetos, le classement


def lire_tau(texte):
    """« inf » -> +infini ; une cellule vide -> None."""
    if texte is None or texte == "":
        return None
    return float("inf") if texte.strip() == "inf" else nombre(texte)


def s3_aligne(position):
    """Le sens de la regle du module 3 : on achete BAS dans le canal."""
    if position is None:
        return None
    if position < SEUIL_BAS:
        return 1
    return -1 if position > SEUIL_HAUT else 0


def s3_fantome(position):
    """Le sens de l'experience 1, conserve pour le portefeuille fantome."""
    if position is None:
        return None
    if position >= SEUIL_HAUT_FANTOME:
        return 1
    return 0 if position >= SEUIL_BAS_FANTOME else -1


def composantes(ligne, sens):
    """Rend (s1, s2, s3, s4, s5, score) a partir d'une ligne de criteres.csv."""
    tend_120, tend_20 = nombre(ligne["TEND_120"]), nombre(ligne["TEND_20"])
    position, momentum = nombre(ligne["POSITION"]), nombre(ligne["MOMENTUM"])
    bas, haut = nombre(ligne["ALPHA_BAS"]), nombre(ligne["ALPHA_HAUT"])

    s1 = None if tend_120 is None else 2 * int(tend_120)
    s2 = None if tend_20 is None else int(tend_20)
    s3 = s3_aligne(position) if sens == "aligne" else s3_fantome(position)

    if momentum is None:
        s4 = None
    elif momentum > 10:
        s4 = 2
    elif momentum > 0:
        s4 = 1
    elif momentum >= -10:
        s4 = -1
    else:
        s4 = -2

    s5 = None if bas is None or haut is None else (
        1 if bas > 0 else -1 if haut < 0 else 0)

    return s1, s2, s3, s4, s5, sum(0 if s is None else s for s in (s1, s2, s3, s4, s5))


def vetos_actifs(texte):
    """Rend l'ensemble des numeros de veto cites. « aucun » rend l'ensemble vide."""
    if not texte:
        return set()
    return {int(n) for n in re.findall(r"veto\s+(\d)", texte)}


def index_criteres(criteres):
    """Rend {(role, date, ticker): ligne}."""
    return {(ligne["ROLE"], ligne["DATE"], ligne["TICKER"]): ligne
            for ligne in criteres}


def classer(criteres, date, sens, univers_jour):
    """Rend les valeurs de l'univers du jour, ERREUR exclues, de la meilleure a la pire.

    Une ligne ERREUR n'occupe AUCUN rang : la regle n'a rien produit, elle ne peut
    donc ni faire acheter, ni — en decalant les rangs — faire vendre. C'est un
    changement declare par rapport a l'experience 2.
    """
    lignes = []
    retenus = set(univers_jour)
    for ligne in criteres:
        if (ligne["DATE"] != date or ligne["ROLE"] != "DECISION"
                or ligne["TICKER"] not in retenus or ligne["VERDICT"] == "ERREUR"):
            continue
        s1, s2, s3, s4, s5, score = composantes(ligne, sens)
        lignes.append({
            "DATE": date, "TICKER": ligne["TICKER"],
            "S1": s1, "S2": s2, "S3": s3, "S4": s4, "S5": s5, "SCORE": score,
            "POSITION": nombre(ligne["POSITION"]), "MOMENTUM": nombre(ligne["MOMENTUM"]),
            "TAU": lire_tau(ligne["TAU"]), "VETOS": ligne["VETOS"],
            "ACTIFS": vetos_actifs(ligne["VETOS"]),
            "VERDICT_REGLE": ligne["VERDICT"], "CLOSE": nombre(ligne["CLOSE"]),
        })
    lignes.sort(key=lambda x: (-x["SCORE"], -(x["MOMENTUM"] if x["MOMENTUM"] is not None
                                              else -999), x["TICKER"]))
    for rang, ligne in enumerate(lignes, start=1):
        ligne["RANG"] = rang
    return lignes


def non_classees(criteres, date, univers_jour, index):
    """Rend [(ticker, motif)] pour les valeurs de l'univers absentes du classement."""
    manquantes = []
    for ticker in univers_jour:
        ligne = index.get(("DECISION", date, ticker))
        if ligne is None:
            manquantes.append((ticker, "aucune evaluation dans criteres.csv"))
        elif ligne["VERDICT"] == "ERREUR":
            manquantes.append((ticker, ligne["DIAGNOSTIC"] or "regle en echec"))
    return manquantes


# --------------------------------------------------------------------------
# Phase 3 : les ordres


def taux_achat(ticker):
    return (COURTAGE + SPREAD + (0.0 if ticker in EXEMPTES_TTF else TTF)) / 100


def taux_vente(_ticker):
    return (COURTAGE + SPREAD) / 100


def vendre(positions, classement, date_exec, series, args):
    """Rend (ordres de vente, lignes gardees faute de classement). Ne modifie rien.

    Une ligne detenue absente du classement — sortie de l'indice, ou evaluation en
    echec — est CONSERVEE sans ordre : la regle n'a rien dit d'elle, elle ne peut
    donc pas commander sa vente. C'est une decision de protocole, declaree.
    """
    rangs = {ligne["TICKER"]: ligne for ligne in classement}
    ordres, gardees = [], []
    for ticker in sorted(positions):
        ligne = rangs.get(ticker)
        if ligne is None:
            gardees.append((ticker, "hors classement du jour : conservee sans ordre"))
            continue
        if ligne["RANG"] > args.rang_sortie:
            motif = f"rang {ligne['RANG']} au-dela de {args.rang_sortie}"
        elif ligne["SCORE"] <= -3:
            motif = f"score {ligne['SCORE']:+d}, au plancher de -3"
        else:
            continue
        seance = series[ticker].get(date_exec)
        if seance is None:
            erreur(f"{ticker} : pas de seance au {date_exec}, vente impossible")
        brut = positions[ticker]["quantite"] * seance["open"]
        frais = brut * taux_vente(ticker)
        ordres.append({
            "DATE": date_exec, "TICKER": ticker, "SENS": "VENTE",
            "QUANTITE": positions[ticker]["quantite"], "PRIX": seance["open"],
            "BRUT": brut, "FRAIS": frais, "NET": brut - frais,
            "RANG": ligne["RANG"], "SCORE": ligne["SCORE"],
            "VETOS": ligne["VETOS"], "MOTIF": motif,
        })
    return ordres, gardees


def acheter(positions, classement, date_exec, series, especes, args,
            vetos_appliques, repartition):
    """Rend les ordres d'achat, especes reparties a parts egales. Ne modifie rien.

    Un veto interdit l'entree ; il ne force pas la sortie. Un veto dit « la
    figure n'est pas lisible », pas « la position est mauvaise ».

    La repartition divise les especes par le nombre de CRENEAUX LIBRES, pas par
    le nombre de candidats : sans quoi un mois a candidat unique mettrait tout le
    portefeuille sur une seule ligne, ce qui viderait de son sens le plafond de
    cinq lignes. `--repartition candidats` retablit la regle de l'experience 1.
    """
    candidats = [ligne for ligne in classement
                 if ligne["RANG"] <= args.rang_entree and ligne["SCORE"] > 0
                 and ligne["TICKER"] not in positions
                 and not (vetos_appliques and ligne["ACTIFS"])]
    creneaux = max(args.lignes - len(positions), 0)
    candidats = candidats[:creneaux]
    if not candidats or especes <= 0:
        return []
    part = especes / (len(candidats) if repartition == "candidats" else creneaux)
    ordres = []
    for ligne in candidats:
        ticker = ligne["TICKER"]
        seance = series[ticker].get(date_exec)
        if seance is None:
            erreur(f"{ticker} : pas de seance au {date_exec}, achat impossible")
        prix, taux = seance["open"], taux_achat(ticker)
        quantite = int(part // (prix * (1 + taux)))
        if quantite < 1:
            continue
        brut = quantite * prix
        frais = brut * taux
        ordres.append({
            "DATE": date_exec, "TICKER": ticker, "SENS": "ACHAT", "QUANTITE": quantite,
            "PRIX": prix, "BRUT": brut, "FRAIS": frais, "NET": brut + frais,
            "RANG": ligne["RANG"], "SCORE": ligne["SCORE"], "VETOS": ligne["VETOS"],
            "MOTIF": f"rang {ligne['RANG']}, score {ligne['SCORE']:+d}, aucun veto",
        })
    return ordres


# --------------------------------------------------------------------------
# Phase 4 : la simulation


def derniere_seance(seances, mois):
    jours = [j for j in seances if j[:7] == mois]
    return jours[-1] if jours else None


def mois_precedent(mois):
    """« 2022-03 » -> « 2022-02 », « 2022-01 » -> « 2021-12 »."""
    annee, numero = int(mois[:4]), int(mois[5:7])
    return f"{annee - 1}-12" if numero == 1 else f"{annee}-{numero - 1:02d}"


def suivant(mois):
    """« 2022-11 » -> « 2022-12 », « 2022-12 » -> « 2023-01 »."""
    annee, numero = int(mois[:4]), int(mois[5:7])
    return f"{annee + 1}-01" if numero == 12 else f"{annee}-{numero + 1:02d}"


def simuler(couples, criteres, series, reference, seances, args, sens, univers,
            vetos_appliques=True, repartition=None):
    """Rend (ordres, valeurs, historique) pour une variante declaree.

    Les trois leviers — le sens de s3, l'application des vetos et la regle de
    repartition — sont des parametres, ce qui permet de faire tourner les
    variantes declarees au README sans dupliquer une ligne de comptabilite.
    """
    repartition = repartition or args.repartition
    positions, especes = {}, args.dotation
    ordres_tous, valeurs, historique = [], {}, []

    for i, (date_decision, date_exec) in enumerate(couples):
        classement = classer(criteres, date_decision, sens, univers[date_decision])
        mois = date_exec[:7]
        precedent = derniere_seance(seances, mois_precedent(date_decision[:7]))

        etat_avant = {}
        for ticker, info in positions.items():
            cours = series[ticker][date_decision]["close"]
            plein = bool(precedent) and info["date"] <= precedent
            base_mois = series[ticker][precedent]["close"] if plein else info["prix"]
            ref_mois = (reference[precedent]["close"] if plein
                        else reference[info["date"]]["close"])
            etat_avant[ticker] = {
                "date": info["date"], "prix": info["prix"],
                "quantite": info["quantite"],
                "pv": 100 * (cours / info["prix"] - 1),
                "alpha_mois": 100 * (cours / base_mois
                                     - reference[date_decision]["close"] / ref_mois),
                "alpha_global": 100 * (cours / info["prix"]
                                       - reference[date_decision]["close"]
                                       / reference[info["date"]]["close"]),
                "partiel": "" if plein else " (partiel)",
            }

        ordres, gardees = vendre(positions, classement, date_exec, series, args)
        for ordre in ordres:
            especes += ordre["NET"]
            del positions[ordre["TICKER"]]
        achats = acheter(positions, classement, date_exec, series, especes, args,
                         vetos_appliques, repartition)
        for ordre in achats:
            especes -= ordre["NET"]
            positions[ordre["TICKER"]] = {"quantite": ordre["QUANTITE"],
                                          "prix": ordre["PRIX"], "date": date_exec}
        ordres += achats
        ordres_tous.extend(ordres)

        fin_segment = couples[i + 1][1] if i + 1 < len(couples) else None
        for jour in seances:
            if jour < date_exec or (fin_segment and jour >= fin_segment):
                continue
            titres = sum(p["quantite"] * series[t][jour]["close"]
                         for t, p in positions.items())
            valeurs[jour] = (especes, titres, especes + titres)

        historique.append({
            "mois": mois, "date_decision": date_decision, "date_exec": date_exec,
            "classement": classement, "ordres": ordres, "etat_avant": etat_avant,
            "gardees": gardees, "tenues": dict(positions),
        })
    return ordres_tous, valeurs, historique


# --------------------------------------------------------------------------
# Phase 5 : les theses, ecrites puis depouillees


def ecarts_mensuels(serie, reference, dates_ref):
    """Rend {fin de mois: ecart du mois, en points, contre la reference}.

    Un mois dont l'une des deux bornes n'a pas de seance a volume STRICTEMENT
    POSITIF est ecarte : une serie synthetique — 523 seances au meme prix, volume
    nul, comme Stellantis avant le 2021-01-18 — n'est pas un cours, et l'ecart
    qu'on en tirerait ne mesurerait rien.
    """
    fins = []
    par_mois = {}
    for jour in dates_ref:
        par_mois.setdefault(jour[:7], []).append(jour)
    for mois in sorted(par_mois):
        fins.append(par_mois[mois][-1])
    ecarts = {}
    for i in range(1, len(fins)):
        depart, arrivee = fins[i - 1], fins[i]
        a, b = serie.get(depart), serie.get(arrivee)
        if a is None or b is None or a["volume"] <= 0 or b["volume"] <= 0:
            continue
        if depart not in reference or arrivee not in reference:
            continue
        ecarts[arrivee] = 100 * (b["close"] / a["close"]
                                 - reference[arrivee]["close"]
                                 / reference[depart]["close"])
    return ecarts


def sigma_mensuel(ecarts, date):
    """Ecart-type des FENETRE_SIGMA ecarts mensuels ANTERIEURS a `date`.

    Rend None s'il en manque un seul, ou si l'ecart-type est nul : une clause
    d'epaisseur nulle ne serait pas refutable, elle serait fausse par
    construction.
    """
    precedents = [ecarts[jour] for jour in sorted(ecarts) if jour < date]
    if len(precedents) < FENETRE_SIGMA:
        return None
    sigma = statistics.stdev(precedents[-FENETRE_SIGMA:])
    return sigma if sigma > 0 else None


def phase_reflexive(ligne, sigma):
    """Rend (phase, borne basse, borne haute, borne de dementi) ou None.

    None quand l'etat n'est pas lisible : une evaluation ratee ne devient pas une
    these par defaut. L'experience 2 les rangeait toutes dans AUCUNE SEQUENCE.
    """
    tend_120, tend_20 = nombre(ligne["TEND_120"]), nombre(ligne["TEND_20"])
    position = nombre(ligne["POSITION"])
    if None in (tend_120, tend_20, position):
        return None
    demi = DEMI_BORNE * sigma
    if tend_120 == 1 and tend_20 == 1 and position > SEUIL_HAUT:
        return "AUTO-RENFORCEMENT", demi, None, -demi
    if tend_120 == -1 and tend_20 == -1 and position < SEUIL_BAS:
        return "RETOURNEMENT", None, -demi, demi
    return "AUCUNE SEQUENCE", -sigma, sigma, None


def depouiller(basse, haute, dementi, constatee):
    """Quatre verdicts. Une borne vide vaut l'infini du bon cote.

    ZONE MORTE et NON TRANCHEE sont distincts : le premier dit « evaluee, mais
    l'ecart est trop petit pour trancher », le second « il manque une donnee ».
    """
    if constatee is None:
        return "NON TRANCHEE"
    dans = ((basse is None or constatee >= basse)
            and (haute is None or constatee <= haute))
    if dans:
        return "CONFIRMEE"
    if dementi is None:
        return "DEMENTIE"
    if basse is not None:      # AUTO-RENFORCEMENT : dementi par le bas
        return "DEMENTIE" if constatee <= dementi else "ZONE MORTE"
    return "DEMENTIE" if constatee >= dementi else "ZONE MORTE"


def these_canal(ligne, date, suivante, ticker, k, arrivee):
    """Rend la these CANAL d'une evaluation, deja depouillee."""
    support, resistance = nombre(ligne["SUPPORT"]), nombre(ligne["RESISTANCE"])
    pente_sup, pente_res = nombre(ligne["PENTE_SUP"]), nombre(ligne["PENTE_RES"])
    basse = None if support is None or pente_sup is None else support + k * pente_sup
    haute = (None if resistance is None or pente_res is None
             else resistance + k * pente_res)
    constatee = arrivee["close"] if arrivee else None
    if basse is not None and haute is not None and basse > haute:
        verdict = "INCONFIRMABLE"
        enonce = (f"encadrement ferme avant le {suivante} : les bornes prolongees "
                  f"se croisent, la thèse est inconfirmable à l'écriture")
    else:
        verdict = depouiller(basse, haute, None, constatee)
        enonce = (f"clôture entre {fr(basse)} {EURO} et {fr(haute)} {EURO} "
                  f"au {suivante}")
    return {
        "DATE": date, "TICKER": ticker, "TYPE": "CANAL", "PHASE": "",
        "ENONCE": enonce, "BORNE_BASSE": basse, "BORNE_HAUTE": haute,
        "BORNE_DEMENTI": None, "SIGMA": None,
        "DATE_DEPOUILLEMENT": suivante, "VALEUR_CONSTATEE": constatee,
        "VERDICT": verdict,
    }


def these_reflexive(ligne, date, suivante, ticker, sigma, ecart):
    """Rend la these REFLEXIVE d'une evaluation, ou None si elle n'a pas lieu d'etre."""
    trouve = phase_reflexive(ligne, sigma)
    if trouve is None:
        return None
    phase, basse, haute, dementi = trouve
    clause = {
        "AUTO-RENFORCEMENT": (f"écart contre {REFERENCE} au-dessus de "
                              f"+{fr(DEMI_BORNE * sigma)} pt (0,5 σ̂)"),
        "RETOURNEMENT": (f"écart contre {REFERENCE} au-dessous de "
                         f"−{fr(DEMI_BORNE * sigma)} pt (0,5 σ̂)"),
        "AUCUNE SEQUENCE": (f"écart contre {REFERENCE} dans "
                            f"± {fr(sigma)} pt (σ̂)"),
    }[phase]
    return {
        "DATE": date, "TICKER": ticker, "TYPE": "REFLEXIVE", "PHASE": phase,
        "ENONCE": f"{phase} : {clause}, au {suivante}",
        "BORNE_BASSE": basse, "BORNE_HAUTE": haute, "BORNE_DEMENTI": dementi,
        "SIGMA": round(sigma, 4),
        "DATE_DEPOUILLEMENT": suivante, "VALEUR_CONSTATEE": ecart,
        "VERDICT": depouiller(basse, haute, dementi, ecart),
    }


def ecrire_theses(criteres, dates_decision, dates_depouillement, series, reference,
                  dates_ref, univers, canaux):
    """Rend les theses de chaque date, deja depouillees a la date suivante.

    Une valeur sans canal de transmission declare ne recoit AUCUNE these
    REFLEXIVE : elle est hors du champ de la theorie, ce qui n'est pas la meme
    chose que « la theorie s'applique et il ne se passe rien ».
    """
    rang = {jour: i for i, jour in enumerate(dates_ref)}
    index = index_criteres(criteres)
    ecarts = {t: ecarts_mensuels(series[t], reference, dates_ref) for t in series}
    theses, hors_champ, non_evaluables = [], 0, 0
    for date, suivante in zip(dates_decision, dates_depouillement, strict=True):
        k = rang[suivante] - rang[date]
        for ticker in univers[date]:
            ligne = index.get(("DECISION", date, ticker))
            if ligne is None:
                continue
            arrivee = series[ticker].get(suivante)
            theses.append(these_canal(ligne, date, suivante, ticker, k, arrivee))

            if canaux[ticker][0] == "aucun":
                hors_champ += 1
                continue
            sigma = sigma_mensuel(ecarts[ticker], date)
            depart = series[ticker].get(date)
            ecart = None
            if depart and arrivee and date in reference and suivante in reference:
                ecart = 100 * (arrivee["close"] / depart["close"]
                               - reference[suivante]["close"] / reference[date]["close"])
            these = (these_reflexive(ligne, date, suivante, ticker, sigma, ecart)
                     if sigma is not None else None)
            if these is None:
                non_evaluables += 1
            else:
                theses.append(these)
    return theses, hors_champ, non_evaluables


# --------------------------------------------------------------------------
# Phase 6 : les audits


def lignes_decision(criteres, dates, univers):
    """Les lignes DECISION des dates demandees, restreintes a l'univers du jour."""
    return [ligne for ligne in criteres
            if ligne["ROLE"] == "DECISION" and ligne["DATE"] in dates
            and ligne["TICKER"] in univers.get(ligne["DATE"], ())]


def poids_effectifs(criteres, dates, sens, univers):
    """Part de variance expliquee par chaque composante : Cov(si, score)/Var(score).

    La somme vaut exactement 1 : c'est une decomposition, pas une ponderation
    declaree. Une composante de variance nulle rend 0 — elle ne distingue rien.
    """
    colonnes, scores = {i: [] for i in range(5)}, []
    for ligne in lignes_decision(criteres, dates, univers):
        if ligne["VERDICT"] == "ERREUR":
            continue
        parts = composantes(ligne, sens)
        for i in range(5):
            colonnes[i].append(0 if parts[i] is None else parts[i])
        scores.append(parts[5])
    if len(scores) < 2:
        return {i: None for i in range(5)}, len(scores)
    var = statistics.pvariance(scores)
    if var == 0:
        return dict.fromkeys(range(5), 0.0), len(scores)
    moyenne_score = statistics.fmean(scores)
    poids = {}
    for i in range(5):
        moyenne = statistics.fmean(colonnes[i])
        cov = sum((colonnes[i][j] - moyenne) * (scores[j] - moyenne_score)
                  for j in range(len(scores))) / len(scores)
        poids[i] = 100 * cov / var
    return poids, len(scores)


def occurrences_s5(criteres, dates, sens, univers):
    """Rend (positives, negatives, calculables, {ticker: (positives, negatives)}).

    L'experience 2 portait dans son moteur un paragraphe affirmant « toutes a -1 ».
    C'etait vrai de son annee et faux du code : la phrase est desormais engendree.
    """
    positives, negatives, calculables, detail = 0, 0, 0, {}
    for ligne in lignes_decision(criteres, dates, univers):
        if ligne["VERDICT"] == "ERREUR":
            continue
        valeur = composantes(ligne, sens)[4]
        if valeur is None:
            continue
        calculables += 1
        if valeur == 0:
            continue
        haut, bas = detail.get(ligne["TICKER"], (0, 0))
        if valeur > 0:
            positives += 1
            detail[ligne["TICKER"]] = (haut + 1, bas)
        else:
            negatives += 1
            detail[ligne["TICKER"]] = (haut, bas + 1)
    return positives, negatives, calculables, detail


def taux_vetos(criteres, dates, univers):
    """Rend ({numero: compte}, evaluations sans veto, total, erreurs)."""
    compte, aucun, total, erreurs = dict.fromkeys((1, 2, 3, 4), 0), 0, 0, 0
    for ligne in lignes_decision(criteres, dates, univers):
        total += 1
        if ligne["VERDICT"] == "ERREUR":
            erreurs += 1
            continue
        actifs = vetos_actifs(ligne["VETOS"])
        if not actifs:
            aucun += 1
        for numero in actifs:
            compte[numero] += 1
    return compte, aucun, total, erreurs


def occasions_bloquees(historique, args):
    """Les OCCASIONS ou un veto a ecarte une valeur bien classee et non detenue.

    Ce n'est PAS un compte d'achats : il ne regarde pas s'il restait un creneau
    libre. L'experience 2 publiait ce nombre-la sous le nom d'« entrees
    bloquees », ce qui le surestimait.
    """
    compte, tenues = 0, set()
    for etape in historique:
        for ligne in etape["classement"]:
            if (ligne["RANG"] <= args.rang_entree and ligne["SCORE"] > 0
                    and ligne["ACTIFS"] and ligne["TICKER"] not in tenues):
                compte += 1
        tenues = set(etape["tenues"])
    return compte


def achats_bloques(ordres_sans_veto):
    """Les achats que la regle SANS veto a passes sur une valeur alors sous veto.

    C'est la difference exacte, en ordres, entre la regle appliquee et celle de
    2022 — la seule mesure que le protocole puisse appeler « entree bloquee ».
    """
    return sum(1 for ordre in ordres_sans_veto
               if ordre["SENS"] == "ACHAT" and vetos_actifs(ordre["VETOS"]))


def stabilite(criteres, dates, args, univers):
    """Compare la decision a d, d-1 et d-2 : bascules de s3, de score, de tete."""
    index = index_criteres(criteres)
    resultat = {}
    for pas in DECALAGES:
        role = f"DECALE-{pas}"
        bascules_s3, changements_score, couples, tetes = 0, 0, 0, 0
        detail_s3 = {}
        for date in dates:
            reference_tete = {ligne["TICKER"]
                              for ligne in classer(criteres, date, "aligne",
                                                   univers[date])
                              if ligne["RANG"] <= args.rang_entree}
            decalee = []
            for ticker in univers[date]:
                base = index.get(("DECISION", date, ticker))
                autre = index.get((role, date, ticker))
                if base is None or autre is None:
                    continue
                if base["VERDICT"] == "ERREUR" or autre["VERDICT"] == "ERREUR":
                    continue
                couples += 1
                a = composantes(base, "aligne")
                b = composantes(autre, "aligne")
                bascule = a[2] != b[2]
                bascules_s3 += bascule
                if a[5] != b[5]:
                    changements_score += 1
                detail_s3[(date, ticker)] = bascule
                decalee.append({"TICKER": ticker, "SCORE": b[5],
                                "MOMENTUM": nombre(autre["MOMENTUM"])})
            decalee.sort(key=lambda x: (-x["SCORE"],
                                        -(x["MOMENTUM"] if x["MOMENTUM"] is not None
                                          else -999), x["TICKER"]))
            if {ligne["TICKER"] for ligne in decalee[:args.rang_entree]} != reference_tete:
                tetes += 1
        resultat[pas] = {"s3": bascules_s3, "score": changements_score,
                         "couples": couples, "tetes": tetes, "dates": len(dates),
                         "detail": detail_s3}
    return resultat


def survie_encadrement(theses, criteres, dates, dates_depouillement, dates_ref,
                       univers):
    """Taux de dementi du canal, part des tau plus courts que la cadence, mediane."""
    canal = [t for t in theses if t["TYPE"] == "CANAL"]
    inconfirmables = sum(1 for t in canal if t["VERDICT"] == "INCONFIRMABLE")
    dementies = sum(1 for t in canal if t["VERDICT"] == "DEMENTIE")
    tranchees = sum(1 for t in canal if t["VERDICT"] in ("DEMENTIE", "CONFIRMEE"))

    rang = {jour: i for i, jour in enumerate(dates_ref)}
    ecarts = {date: rang[suivante] - rang[date]
              for date, suivante in zip(dates, dates_depouillement, strict=True)}
    taus, courts, total = [], 0, 0
    for ligne in lignes_decision(criteres, set(ecarts), univers):
        tau = lire_tau(ligne["TAU"])
        if tau is None:
            continue
        total += 1
        if not math.isinf(tau):
            taus.append(tau)
            if tau < ecarts[ligne["DATE"]]:
                courts += 1
    return {
        "dementies": dementies, "tranchees": tranchees, "total": len(canal),
        "inconfirmables": inconfirmables,
        "courts": courts, "mesures": total, "infinis": total - len(taus),
        "mediane": statistics.median(taus) if taus else None,
        "cadence": statistics.median(ecarts.values()) if ecarts else None,
    }


def taux_theses(theses, type_, phase=None):
    """Rend (confirmees, tranchees, zone morte, non tranchees, inconfirmables)."""
    retenues = [t for t in theses if t["TYPE"] == type_
                and (phase is None or t["PHASE"] == phase)]
    confirmees = sum(1 for t in retenues if t["VERDICT"] == "CONFIRMEE")
    dementies = sum(1 for t in retenues if t["VERDICT"] == "DEMENTIE")
    return (confirmees, confirmees + dementies,
            sum(1 for t in retenues if t["VERDICT"] == "ZONE MORTE"),
            sum(1 for t in retenues if t["VERDICT"] == "NON TRANCHEE"),
            sum(1 for t in retenues if t["VERDICT"] == "INCONFIRMABLE"))


def jugement_vetos(theses, criteres, stab):
    """Piste C3 : confronte chaque veto a l'issue DECLAREE contre laquelle il se juge.

    Vetos 1 et 2 : la these CANAL tient-elle plus souvent hors veto que sous veto ?
    Veto 3 : s3 bascule-t-il plus souvent sous veto qu'hors veto, a d-1 ?
    Veto 4 : rien. Il est arithmetique et ne pretend rien separer.
    """
    index = index_criteres(criteres)
    resultat = {}

    for numero in (1, 2):
        sous = [0, 0]   # [confirmees, tranchees]
        hors = [0, 0]
        for these in theses:
            if these["TYPE"] != "CANAL" or these["VERDICT"] not in (
                    "CONFIRMEE", "DEMENTIE"):
                continue
            ligne = index.get(("DECISION", these["DATE"], these["TICKER"]))
            if ligne is None:
                continue
            cible = sous if numero in vetos_actifs(ligne["VETOS"]) else hors
            cible[1] += 1
            cible[0] += these["VERDICT"] == "CONFIRMEE"
        resultat[numero] = {
            "libelle": "tenue de `CANAL`", "sous": tuple(sous), "hors": tuple(hors),
            "difference": (100 * (sous[0] / sous[1] - hors[0] / hors[1])
                           if sous[1] and hors[1] else None),
            "ic": ic95_difference(sous[0], sous[1], hors[0], hors[1]),
            "sens": "un encadrement dit lisible doit tenir plus souvent",
        }

    detail = stab[1]["detail"]
    sous, hors = [0, 0], [0, 0]
    for (date, ticker), bascule in detail.items():
        ligne = index.get(("DECISION", date, ticker))
        if ligne is None:
            continue
        cible = sous if 3 in vetos_actifs(ligne["VETOS"]) else hors
        cible[1] += 1
        cible[0] += bascule
    resultat[3] = {
        "libelle": "bascule de `s3` à d−1", "sous": tuple(sous), "hors": tuple(hors),
        "difference": (100 * (sous[0] / sous[1] - hors[0] / hors[1])
                       if sous[1] and hors[1] else None),
        "ic": ic95_difference(sous[0], sous[1], hors[0], hors[1]),
        "sens": "une configuration contradictoire doit être plus instable",
    }
    resultat[4] = {"libelle": None, "sous": None, "hors": None,
                   "difference": None, "ic": None, "sens": None}
    return resultat


def sensibilite(criteres, dates, univers):
    """Piste C1 : les taux sous les cinq jeux de parametres declares."""
    reference_s3 = {}
    for ligne in lignes_decision(criteres, dates, univers):
        if ligne["VERDICT"] != "ERREUR":
            reference_s3[(ligne["DATE"], ligne["TICKER"])] = composantes(
                ligne, "aligne")[2]

    resultat = []
    jeux = [("DECISION", FENETRE, TOLERANCE), *VARIANTES]
    for role, fenetre, tolerance in jeux:
        compte, aucun, total, erreurs, bascules, compares = (
            dict.fromkeys((1, 2, 3, 4), 0), 0, 0, 0, 0, 0)
        for ligne in criteres:
            if (ligne["ROLE"] != role or ligne["DATE"] not in dates
                    or ligne["TICKER"] not in univers.get(ligne["DATE"], ())):
                continue
            total += 1
            if ligne["VERDICT"] == "ERREUR":
                erreurs += 1
                continue
            actifs = vetos_actifs(ligne["VETOS"])
            if not actifs:
                aucun += 1
            for numero in actifs:
                compte[numero] += 1
            attendu = reference_s3.get((ligne["DATE"], ligne["TICKER"]))
            if attendu is not None:
                compares += 1
                bascules += composantes(ligne, "aligne")[2] != attendu
        resultat.append({
            "role": role, "fenetre": fenetre, "tolerance": tolerance,
            "compte": compte, "aucun": aucun, "total": total, "erreurs": erreurs,
            "bascules": bascules, "compares": compares,
        })
    return resultat


def regression(base, indice):
    """Rend beta, alpha annualise, R2, sigma du residu et l'IC95 de l'alpha.

    L'ecart de performance suppose un beta de 1 ; la regression ne le suppose pas.
    Un portefeuille souvent en especes a un beta bien inferieur a 1, et l'ecart de
    performance lui attribue alors une prudence que la regression separe.
    """
    rp = [base[i] / base[i - 1] - 1 for i in range(1, len(base))]
    rm = [indice[i] / indice[i - 1] - 1 for i in range(1, len(indice))]
    if len(rp) < 3:
        return None
    moy_p, moy_m = statistics.fmean(rp), statistics.fmean(rm)
    var_m = statistics.pvariance(rm)
    if var_m == 0:
        return None
    cov = sum((rp[i] - moy_p) * (rm[i] - moy_m) for i in range(len(rp))) / len(rp)
    beta = cov / var_m
    alpha_jour = moy_p - beta * moy_m
    residus = [rp[i] - alpha_jour - beta * rm[i] for i in range(len(rp))]
    sigma_eps = statistics.stdev(residus)
    var_p = statistics.pvariance(rp)
    return {
        "beta": beta,
        "alpha": 100 * alpha_jour * 252,
        "ic_alpha": 100 * Z95 * sigma_eps / math.sqrt(len(rp)) * 252,
        "r2": 1 - statistics.pvariance(residus) / var_p if var_p else None,
        "sigma_residu": 100 * sigma_eps * math.sqrt(252),
        "seances": len(rp),
    }


def dimensionnement(valeurs, ref100, valeurs_f, seances, dotation):
    """La tracking error realisee, l'effet minimal detectable, l'ecart apparie."""
    base = [100 * valeurs[j][2] / dotation for j in seances]
    fantome = [100 * valeurs_f[j][2] / dotation for j in seances]
    indice = [ref100[j] for j in seances]
    ecarts = [(base[i] / base[i - 1] - 1) - (indice[i] / indice[i - 1] - 1)
              for i in range(1, len(seances))]
    apparies = [(base[i] / base[i - 1] - 1) - (fantome[i] / fantome[i - 1] - 1)
                for i in range(1, len(seances))]
    te = statistics.stdev(ecarts) * math.sqrt(252) * 100 if len(ecarts) > 1 else None
    te_paire = (statistics.stdev(apparies) * math.sqrt(252) * 100
                if len(apparies) > 1 else None)
    return {
        "seances": len(seances), "te": te, "te_paire": te_paire,
        "mde": None if te is None else Z95 * te,
        "mde_paire": None if te_paire is None else Z95 * te_paire,
        "alpha": base[-1] - indice[-1],
        "ecart_fantome": base[-1] - fantome[-1],
        "regression": regression(base, indice),
    }


def verifier_splits(ordres):
    """Sort en 1 si un ordre porte sur une valeur a division retro-ajustee.

    Ce n'est pas un filtre — un filtre changerait la regle et agirait comme un
    cinquieme veto. C'est une verification : si le cas se presente, il faut
    retelecharger une serie non retro-ajustee, pas publier un portefeuille que
    le nombre de titres, seul, aurait deforme.
    """
    touches = sorted({o["TICKER"] for o in ordres if o["TICKER"] in SPLITS_POSTERIEURS})
    if touches:
        detail = NL_.join(f"  {t} : {SPLITS_POSTERIEURS[t]}" for t in touches)
        erreur("Ordre passe sur une valeur a division posterieure a la fenetre :"
               + NL_ + detail + NL_
               + "  Le nombre de titres achetables serait faconne par une"
                 " operation posterieure a l'annee jouee." + NL_
               + "  Reprendre une serie non retro-ajustee.")
    return sorted(SPLITS_POSTERIEURS)


def exposition(valeurs, seances):
    """Part investie moyenne et nombre de seances integralement en especes."""
    parts, vides = [], 0
    for jour in seances:
        _especes, titres, total = valeurs[jour]
        parts.append(100 * titres / total if total else 0.0)
        vides += titres <= 0
    return statistics.fmean(parts) if parts else None, vides


# --------------------------------------------------------------------------
# Phase 7 : le graphique


def pas_de_grille(amplitude):
    for pas in (0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100):
        if amplitude / pas <= 8:
            return pas
    return 200


def svg(chemin, dates, portefeuille, reference, executions, debut):
    """Ecrit un graphique a deux courbes en base 100. Aucune bibliotheque."""
    largeur, hauteur = 900, 420
    marge_g, marge_d, marge_h, marge_b = 62, 18, 46, 46
    aire_l, aire_h = largeur - marge_g - marge_d, hauteur - marge_h - marge_b

    bas, haut = min(portefeuille + reference), max(portefeuille + reference)
    if haut - bas < 1e-9:
        bas, haut = bas - 1, haut + 1
    coussin = (haut - bas) * 0.08
    bas, haut = bas - coussin, haut + coussin

    def x(i):
        return marge_g + aire_l * i / max(len(dates) - 1, 1)

    def y(v):
        return marge_h + aire_h * (haut - v) / (haut - bas)

    def trace(serie):
        return " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(serie))

    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" '
         f'height="{hauteur}" viewBox="0 0 {largeur} {hauteur}" '
         f'font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{marge_g}" y="24" font-size="15" font-weight="600" '
         f'fill="#1a1a1a">Experience 3 &#8212; portefeuille contre {REFERENCE}, '
         f'base 100 au {debut}</text>'),
        (f'<text x="{marge_g}" y="40" font-size="11" fill="#666666">'
         f'{dates[0]} &#8594; {dates[-1]} &#183; {len(dates)} seances &#183; '
         f'traits verticaux : les executions</text>'),
    ]

    pas = pas_de_grille(haut - bas)
    niveau = int(bas / pas) * pas
    while niveau <= haut:
        if niveau >= bas:
            gras = abs(niveau - 100) < 1e-9
            out.append(
                f'<line x1="{marge_g}" y1="{y(niveau):.1f}" x2="{largeur - marge_d}" '
                f'y2="{y(niveau):.1f}" stroke="{"#c0c0c0" if gras else "#ececec"}" '
                f'stroke-width="1"/>')
            out.append(
                f'<text x="{marge_g - 8}" y="{y(niveau) + 4:.1f}" font-size="10.5" '
                f'fill="#666666" text-anchor="end">{fr(niveau, 0)}</text>')
        niveau += pas

    index = {jour: i for i, jour in enumerate(dates)}
    for jour in executions:
        if jour in index:
            out.append(
                f'<line x1="{x(index[jour]):.1f}" y1="{marge_h}" '
                f'x2="{x(index[jour]):.1f}" y2="{marge_h + aire_h}" stroke="#ded5c4" '
                f'stroke-width="1" stroke-dasharray="2 3"/>')

    out.append(f'<polyline points="{trace(reference)}" fill="none" stroke="#9aa5b1" '
               f'stroke-width="1.6" stroke-dasharray="5 4"/>')
    out.append(f'<polyline points="{trace(portefeuille)}" fill="none" stroke="#1f5f8b" '
               f'stroke-width="2.1"/>')

    out.append(f'<text x="{marge_g}" y="{hauteur - 16}" font-size="10.5" fill="#666666">'
               f'{dates[0]}</text>')
    out.append(f'<text x="{largeur - marge_d}" y="{hauteur - 16}" font-size="10.5" '
               f'fill="#666666" text-anchor="end">{dates[-1]}</text>')
    out.append(f'<line x1="{largeur - 250}" y1="{hauteur - 31}" x2="{largeur - 224}" '
               f'y2="{hauteur - 31}" stroke="#1f5f8b" stroke-width="2.1"/>'
               f'<text x="{largeur - 218}" y="{hauteur - 27}" font-size="10.5" '
               f'fill="#444444">portefeuille {fr(portefeuille[-1], 1)}</text>')
    out.append(f'<line x1="{largeur - 250}" y1="{hauteur - 15}" x2="{largeur - 224}" '
               f'y2="{hauteur - 15}" stroke="#9aa5b1" stroke-width="1.6" '
               f'stroke-dasharray="5 4"/>'
               f'<text x="{largeur - 218}" y="{hauteur - 11}" font-size="10.5" '
               f'fill="#444444">{REFERENCE} {fr(reference[-1], 1)}</text>')
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Phase 8 : la console


def bloc_mensuel(mois, etape, etat_apres, valeurs, seances, manquantes):
    """Rend le bloc console d'un mois."""
    lignes = [
        "",
        (f"=== {mois} {MEDIAN} decision au {etape['date_decision']}"
         f" {MEDIAN} execution au {etape['date_exec']} ==="),
        "",
        "Classement au " + etape["date_decision"],
        "  rang  valeur      s1  s2  s3  s4  s5  score   position       tau  vetos",
    ]
    for ligne in etape["classement"]:
        actifs = sorted(ligne["ACTIFS"])
        lignes.append(
            f"  {ligne['RANG']:4d}  {ligne['TICKER']:<10s}"
            f"  {ent(ligne['S1'])} {ent(ligne['S2'])} {ent(ligne['S3'])}"
            f" {ent(ligne['S4'])} {ent(ligne['S5'])}  {ligne['SCORE']:+5d}"
            f"  {fr(ligne['POSITION'], 1):>7s} %  {tau_texte(ligne['TAU']):>8s}"
            f"  {','.join(str(v) for v in actifs) if actifs else '-'}")
    for ticker, motif in manquantes:
        lignes.append(f"     -  {ticker:<10s}  non classee : {motif}")

    lignes += ["", f"Exposition heritee au {etape['date_decision']}"]
    if not etape["etat_avant"]:
        lignes.append("  aucune ligne — le portefeuille est integralement en especes")
    for ticker, info in sorted(etape["etat_avant"].items()):
        lignes.append(
            f"  {ticker:<10s} achetee le {info['date']} a {fr(info['prix'])} EUR"
            f"  {MEDIAN}  {signe(info['pv'], 2):>8s} %"
            f"  {MEDIAN}  alpha du mois {signe(info['alpha_mois'], 2):>7s} pt"
            f"{info['partiel']}"
            f"  {MEDIAN}  alpha global {signe(info['alpha_global'], 2):>7s} pt")

    lignes += ["", f"Ordres executes au {etape['date_exec']}"]
    if not etape["ordres"]:
        lignes.append("  aucun ordre")
    for ordre in etape["ordres"]:
        lignes.append(
            f"  {ordre['SENS']:<6s} {ordre['TICKER']:<10s} {ordre['QUANTITE']:4d} titres"
            f" a {fr(ordre['PRIX']):>9s} EUR  {MEDIAN}  brut {fr(ordre['BRUT']):>10s}"
            f"  frais {fr(ordre['FRAIS']):>6s}  {MEDIAN}  {ordre['MOTIF']}")
    for ticker, motif in etape["gardees"]:
        lignes.append(f"  GARDEE {ticker:<10s} {motif}")

    fin_mois = derniere_seance(seances, mois)
    especes, titres, total = valeurs[fin_mois]
    lignes += ["", f"Portefeuille au {fin_mois}"]
    lignes.append(
        f"  especes {fr(especes)} EUR {MEDIAN} titres {fr(titres)} EUR "
        f"{MEDIAN} total {fr(total)} EUR")
    lignes.append(
        f"  base 100 : portefeuille {fr(etat_apres['base'], 2)}"
        f" {MEDIAN} {REFERENCE} {fr(etat_apres['reference'], 2)}")
    lignes.append(
        f"  alpha du mois {signe(etat_apres['alpha_mois'], 2)} pt"
        f" {MEDIAN} alpha depuis janvier {signe(etat_apres['alpha_global'], 2)} pt")
    return NL_.join(lignes)


# --------------------------------------------------------------------------
# Phase 8 : les markdown


def decouper(texte, prefixe):
    """Rend {titre: corps} pour les sections dont la ligne commence par `prefixe`."""
    sections, titre, corps = {}, None, []
    for ligne in texte.split(NL_):
        if ligne.startswith(prefixe) and not ligne.startswith(prefixe + "#"):
            if titre is not None:
                sections[titre] = NL_.join(corps).strip()
            titre, corps = ligne[len(prefixe):].strip(), []
        elif titre is not None:
            corps.append(ligne)
    if titre is not None:
        sections[titre] = NL_.join(corps).strip()
    return sections


def charger_textes(repertoire):
    """Rend (actualites par mois, notes chartistes par date puis par ticker)."""
    for nom in ("actualites.md", "chartiste.md"):
        if not (repertoire / nom).exists():
            erreur(f"{repertoire / nom} absent : requis par --markdown")
    actualites = decouper((repertoire / "actualites.md").read_text(encoding="utf-8"),
                          "## ")
    brut = decouper((repertoire / "chartiste.md").read_text(encoding="utf-8"), "## ")
    return actualites, {date: decouper(corps, "### ") for date, corps in brut.items()}


def tableau_exposition(etat_avant, gardees):
    """Le tableau des lignes heritees, ou la mention d'absence."""
    if not etat_avant:
        return "*Aucune ligne : le portefeuille est intégralement en espèces.*"
    lignes = [("| Valeur | Achetée le | Prix d'achat | +/− value "
               "| Alpha du mois | Alpha global |"),
              "|---|---|---|---|---|---|"]
    for ticker, info in sorted(etat_avant.items()):
        partiel = " *(partiel)*" if info["partiel"] else ""
        lignes.append(
            f"| `{ticker}` {SOCIETES[ticker]} | {info['date']} "
            f"| {fr(info['prix'])} {EURO} | **{signe(info['pv'])} %** "
            f"| {signe(info['alpha_mois'])} pt{partiel} "
            f"| {signe(info['alpha_global'])} pt |")
    if gardees:
        lignes += ["", "Lignes **conservées sans ordre**, faute de classement :", ""]
        lignes += [f"- `{ticker}` {SOCIETES[ticker]} — {motif}"
                   for ticker, motif in gardees]
    return NL_.join(lignes)


def positions_a_date(ordres, jusqu_a):
    """Toutes les positions prises depuis le debut, closes comme ouvertes.

    N'utilise AUCUNE seance posterieure a `jusqu_a` : le tableau de mars ne
    connait pas avril.
    """
    ouvertes, closes = {}, []
    for ordre in sorted(ordres, key=lambda o: (o["DATE"], o["SENS"], o["TICKER"])):
        if ordre["DATE"] > jusqu_a:
            continue
        ticker = ordre["TICKER"]
        if ordre["SENS"] == "ACHAT":
            ouvertes[ticker] = ordre
        elif ticker in ouvertes:
            closes.append((ouvertes.pop(ticker), ordre))
    lignes = [{"ticker": a["TICKER"], "prix_achat": a["PRIX"], "date_achat": a["DATE"],
               "prix_vente": v["PRIX"] if v else None,
               "date_vente": v["DATE"] if v else None}
              for a, v in [*closes, *((a, None) for a in ouvertes.values())]]
    lignes.sort(key=lambda x: (x["date_achat"], x["ticker"]))
    return lignes


def tableau_positions(lignes):
    """Le tableau demande : societe, prix et date d'achat, prix et date de vente."""
    if not lignes:
        return "*Aucune position prise depuis le début de l'expérience.*"
    out = ["| Société | Prix d'achat | Date d'achat | Prix de vente | Date de vente |",
           "|---|---|---|---|---|"]
    for ligne in lignes:
        vendue = ligne["date_vente"] is not None
        out.append(
            f"| `{ligne['ticker']}` {SOCIETES[ligne['ticker']]} "
            f"| {fr(ligne['prix_achat'])} {EURO} | {ligne['date_achat']} "
            f"| {fr(ligne['prix_vente']) + ' ' + EURO if vendue else ''} "
            f"| {ligne['date_vente'] or ''} |")
    ouvertes = sum(1 for ligne in lignes if ligne["date_vente"] is None)
    out += ["",
            (f"*{len(lignes)} position{'s' if len(lignes) > 1 else ''} depuis le début, "
             f"dont {ouvertes} encore ouverte{'s' if ouvertes > 1 else ''} : "
             "les deux dernières colonnes restent vides.*")]
    return NL_.join(out)


def tableau_classement(classement, manquantes):
    """Les valeurs de l'univers du jour, de la plus interessante a la plus a fuir."""
    lignes = [("| Rang | Valeur | `s1` | `s2` | `s3` | `s4` | `s5` | Score "
               "| Position | Momentum | τ | Vetos |"),
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for ligne in classement:
        ticker = ligne["TICKER"]
        actifs = sorted(ligne["ACTIFS"])
        lignes.append(
            f"| {ligne['RANG']} | `{ticker}` {SOCIETES[ticker]} "
            f"| {ent(ligne['S1']).strip()} | {ent(ligne['S2']).strip()} "
            f"| {ent(ligne['S3']).strip()} | {ent(ligne['S4']).strip()} "
            f"| {ent(ligne['S5']).strip()} | **{ligne['SCORE']:+d}** "
            f"| {fr(ligne['POSITION'], 1)} % | {signe(ligne['MOMENTUM'], 1)} % "
            f"| {tau_texte(ligne['TAU'])} "
            f"| {' '.join(str(v) for v in actifs) if actifs else '—'} |")
    if manquantes:
        lignes += ["", "**Non classées** — la règle n'a rien produit :", ""]
        lignes += [f"- `{ticker}` {SOCIETES[ticker]} — {motif}"
                   for ticker, motif in manquantes]
    return NL_.join(lignes)


def note_en_liste(note):
    """Rend les lignes d'une note en puces."""
    lignes = [ligne.strip() for ligne in note.split(NL_) if ligne.strip()]
    if not lignes:
        return ""
    return NL_.join(ligne if ligne.startswith("- ") else f"- {ligne}"
                    for ligne in lignes)


def tableau_ordres(ordres):
    """Les ordres du mois, ou la mention d'absence."""
    if not ordres:
        return "*Aucun ordre : le classement ne déclenche ni entrée ni sortie.*"
    lignes = ["| Sens | Valeur | Quantité | Prix d'exécution | Brut | Frais | Motif |",
              "|---|---|---|---|---|---|---|"]
    for ordre in ordres:
        ticker = ordre["TICKER"]
        lignes.append(
            f"| **{ordre['SENS'].capitalize()}** | `{ticker}` {SOCIETES[ticker]} "
            f"| {ordre['QUANTITE']} | {fr(ordre['PRIX'])} {EURO} "
            f"| {fr(ordre['BRUT'])} {EURO} | {fr(ordre['FRAIS'])} {EURO} "
            f"| {ordre['MOTIF']} |")
    return NL_.join(lignes)


MARQUE_VERDICT = {
    "CONFIRMEE": "**confirmée**", "DEMENTIE": "démentie",
    "NON TRANCHEE": "*non tranchée*", "ZONE MORTE": "*zone morte*",
    "INCONFIRMABLE": "*inconfirmable à l'écriture*",
}


def tableau_depouillement(theses):
    """Les theses du mois precedent, avec leur verdict."""
    if not theses:
        return "*Aucune thèse à dépouiller : c'est la première date du registre.*"
    lignes = ["| Valeur | Thèse | Énoncé | Constaté | Verdict |",
              "|---|---|---|---|---|"]
    for these in theses:
        unite = EURO if these["TYPE"] == "CANAL" else "pt"
        lignes.append(
            f"| `{these['TICKER']}` | {these['TYPE'].capitalize()} "
            f"| {these['ENONCE']} "
            f"| {fr(these['VALEUR_CONSTATEE'])} {unite} "
            f"| {MARQUE_VERDICT[these['VERDICT']]} |")
    return NL_.join(lignes)


def tableau_theses(theses):
    """Les theses ecrites ce mois-ci, qui seront depouillees le mois prochain."""
    lignes = ["| Valeur | Thèse | Énoncé, à dépouiller au mois suivant |",
              "|---|---|---|"]
    for these in theses:
        lignes.append(
            f"| `{these['TICKER']}` | {these['TYPE'].capitalize()} "
            f"| {these['ENONCE']} |")
    return NL_.join(lignes)


def lecture_du_mois(apports, ordres, alpha_mois, depouillees, dotation):
    """Un paragraphe entierement calcule : aucun recit ecrit apres coup.

    Le perimetre des contributions comprend les lignes VENDUES dans le mois :
    l'experience 2 ne regardait que celles encore detenues a la fin, si bien
    qu'une ligne vendue le 2 et suivie d'une chute etait invisible.
    """
    phrases = []
    if apports:
        ordonnes = sorted(apports, key=lambda a: a["euros"])
        haut, bas = ordonnes[-1], ordonnes[0]
        phrases.append(
            f"Sur le mois, la meilleure contribution vient de `{haut['ticker']}` "
            f"({SOCIETES[haut['ticker']]}) pour **{signe(haut['euros'])} {EURO}**, "
            f"la moins bonne de `{bas['ticker']}` ({SOCIETES[bas['ticker']]}) pour "
            f"**{signe(bas['euros'])} {EURO}**.")
    else:
        phrases.append("Aucune ligne détenue sur le mois.")
    frais = sum(o["FRAIS"] for o in ordres)
    if ordres:
        phrases.append(
            f"Les {len(ordres)} ordres du mois ont coûté **{fr(frais)} {EURO}** de "
            f"frais, soit {fr(100 * frais / dotation, 3)} % de la dotation initiale.")
    else:
        phrases.append("Aucun ordre, donc aucun frais : le classement, l'hystérésis ou "
                       "les vetos ont retenu le portefeuille en l'état.")
    sens = "devant" if alpha_mois >= 0 else "derrière"
    phrases.append(
        f"Le portefeuille termine le mois **{sens} {REFERENCE}** de "
        f"{fr(abs(alpha_mois))} point.")
    confirmees, tranchees = depouillees
    if tranchees:
        phrases.append(
            f"Sur les {tranchees} thèses du mois précédent qui ont pu être "
            f"tranchées, **{confirmees} sont confirmées** — "
            f"{fr(100 * confirmees / tranchees, 1)} %.")
    return " ".join(phrases)


def journal_mensuel(mois, c):
    """Rend le texte complet d'un journal mensuel."""
    bloc = [
        f"# {MOIS_TITRE[mois[5:7]]} {ANNEE}",
        "",
        (f"> Journal de l'[expérience 3](../README.md) · **décision au "
         f"{c['date_decision']}** · **exécution au {c['date_exec']}**"),
        (f"> Portefeuille au {c['fin_mois']} : **{fr(c['total'])} {EURO}** "
         f"(base {fr(c['base'])}) · {REFERENCE} {fr(c['reference'])} · alpha "
         f"du mois **{signe(c['alpha_mois'])} pt** · depuis janvier "
         f"**{signe(c['alpha_global'])} pt**"),
        "",
        "---",
        "",
        "## 1. Les actualités du mois précédent",
        "",
        c["actualites"] or ABSENTE,
        "",
        f"## 2. Le dépouillement des thèses écrites au {c['date_precedente']}",
        "",
        ("> Piste **S4**. Ces énoncés ont été écrits le mois dernier, avant de "
         "connaître ce mois-ci. Aucun n'a été retouché ; le verdict est calculé."),
        "",
        tableau_depouillement(c["depouillement"]),
        "",
        f"## 3. L'exposition héritée au {c['date_decision']}",
        "",
        tableau_exposition(c["etat_avant"], c["gardees"]),
        "",
        f"## 4. Le portefeuille depuis le {c['debut']}",
        "",
        (f"![Évolution du portefeuille au {c['fin_mois']}]"
         f"(../{GRAPHIQUES}/portefeuille-{mois}.svg)"),
        "",
        "| | |",
        "|---|---|",
        f"| Dotation initiale | {fr(c['dotation'])} {EURO} au {c['debut']} |",
        f"| Titres au {c['fin_mois']} | {fr(c['titres'])} {EURO} |",
        f"| Espèces | {fr(c['especes'])} {EURO} |",
        f"| **Total** | **{fr(c['total'])} {EURO}** |",
        f"| Base 100 | **{fr(c['base'])}** |",
        f"| {REFERENCE}, même base | {fr(c['reference'])} |",
        f"| Écart depuis janvier | **{signe(c['alpha_global'])} pt** |",
        "",
        "### Toutes les positions depuis le début de l'expérience",
        "",
        ("> Closes comme ouvertes. Une position encore ouverte laisse les deux "
         "dernières colonnes vides. Aucune séance postérieure au "
         f"{c['fin_mois']} n'entre dans ce tableau."),
        "",
        tableau_positions(c["positions"]),
        "",
        f"## 5. L'étude chartiste au {c['date_decision']}",
        "",
        (f"> Notes rédigées sans aucune séance postérieure au "
         f"{c['date_decision']}, par l'agent `chartiste`. Cinq lignes au plus par "
         f"société, **chacune sous la figure de décision qui la justifie** — celle "
         f"que la règle a lue ce jour-là, portant les cinq critères, les vetos et "
         f"le verdict."),
        "",
    ]
    titres = [(f"{ligne['RANG']}. `{ligne['TICKER']}` — {SOCIETES[ligne['TICKER']]}",
               ligne["TICKER"]) for ligne in c["classement"]]
    # Une valeur non classee reste dans l'univers du jour : la taire ferait
    # disparaitre du journal une societe que le protocole declare etudier.
    titres += [(f"`{ticker}` — {SOCIETES[ticker]} — *hors classement*", ticker)
               for ticker, _motif in c["manquantes"]]
    for titre, ticker in titres:
        bloc += [f"### {titre}", ""]
        if ticker in c["figures"]:
            bloc += [(f"![Figure de décision {ticker} au {c['date_decision']}]"
                      f"(../{GRAPHIQUES}/{ticker}/decision-{ticker}-"
                      f"{c['date_decision']}.svg)"),
                     ""]
        else:
            bloc += [FIGURE_ABSENTE, ""]
        bloc += [note_en_liste(c["notes"].get(ticker, "")) or ABSENTE, ""]

    bloc += [
        f"## 6. Le classement au {c['date_decision']}",
        "",
        ("> De la valeur la plus intéressante à détenir à celle qu'il faut fuir. "
         "La colonne **τ** donne la date de péremption du canal en séances, la "
         "colonne **Vetos** les numéros déclenchés. Une valeur sous veto ne peut "
         "pas être achetée."),
        "",
        tableau_classement(c["classement"], c["manquantes"]),
        "",
        f"## 7. Les ordres exécutés au {c['date_exec']}",
        "",
        (f"> À l'**ouverture** de la séance, jamais à la clôture "
         f"du {c['date_decision']}."),
        "",
        tableau_ordres(c["ordres"]),
        "",
        "## 8. La lecture du mois",
        "",
        c["lecture"],
        "",
        f"## 9. Les thèses écrites au {c['date_decision']}",
        "",
        ("> Elles seront dépouillées à la prochaine date de décision, dans le "
         "fichier du mois suivant. Elles sont engendrées mécaniquement par les "
         "règles du [protocole](../README.md#le-registre-des-thèses-réfutables) — "
         "aucune n'est rédigée à la main."),
        "",
        tableau_theses(c["theses"]),
        "",
    ]
    if c.get("dernier"):
        bloc += ["---", "",
                 ("L'expérience s'arrête ici. Le compte complet de l'année, les "
                  "audits et la confrontation du dimensionnement sont dans "
                  f"le **[bilan de l'année](../{BILAN})**."),
                 ""]
    bloc += ["---", "", c["navigation"]]
    return NL_.join(bloc) + NL_


def positions_de_lannee(ordres, series, reference, fin):
    """Reconstitue chaque position ouverte dans l'annee, close ou non."""
    ouvertes, closes = {}, []
    for ordre in ordres:
        ticker = ordre["TICKER"]
        if ordre["SENS"] == "ACHAT":
            ouvertes[ticker] = ordre
        elif ticker in ouvertes:
            closes.append((ouvertes.pop(ticker), ordre))
    lignes = []
    for achat, vente in [*closes, *((a, None) for a in ouvertes.values())]:
        ticker = achat["TICKER"]
        sortie = vente["DATE"] if vente else fin
        prix_sortie = vente["PRIX"] if vente else series[ticker][fin]["close"]
        frais = achat["FRAIS"] + (vente["FRAIS"] if vente else 0.0)
        seances = sum(1 for j in series[ticker] if achat["DATE"] <= j <= sortie)
        lignes.append({
            "ticker": ticker, "achat": achat["DATE"], "vente": sortie,
            "ouverte": vente is None, "quantite": achat["QUANTITE"],
            "prix_achat": achat["PRIX"], "prix_vente": prix_sortie,
            "seances": seances,
            "pv": 100 * (prix_sortie / achat["PRIX"] - 1),
            "alpha": 100 * (prix_sortie / achat["PRIX"]
                            - reference[sortie]["close"]
                            / reference[achat["DATE"]]["close"]),
            "euros": achat["QUANTITE"] * (prix_sortie - achat["PRIX"]) - frais,
        })
    lignes.sort(key=lambda x: (x["achat"], x["ticker"]))
    return lignes


def janvier_tenu(ordres, series, dotation, debut, fin):
    """Le contrefactuel : le portefeuille du premier mois, garde sans un ordre."""
    premiers = [o for o in ordres if o["DATE"] == debut and o["SENS"] == "ACHAT"]
    especes = dotation - sum(o["NET"] for o in premiers)
    titres = sum(o["QUANTITE"] * series[o["TICKER"]][fin]["close"] for o in premiers)
    return especes + titres


# --------------------------------------------------------------------------
# Les sections du bilan


def section_univers(b):
    """Section 4 du bilan — l'univers point-in-time et ses mouvements."""
    out = [
        "",
        "## 4. L'univers, et ce qu'il a coûté au biais du survivant",
        "",
        ("> L'expérience 1 et l'expérience 2 tournaient sur douze valeurs choisies "
         "parmi celles qui étaient au CAC 40 en 2022, et les y retrouver ensuite "
         "n'avait rien d'un hasard. Ici l'univers est **la composition réelle de "
         "l'indice à chaque date de décision**, lue dans "
         "[`univers.csv`](univers.csv)."),
        "",
        "| | |",
        "|---|---|",
        f"| Dates de décision | {b['dates_audit']} |",
        f"| Valeurs distinctes passées par l'univers | {b['tickers_distincts']} |",
        f"| Évaluations de la règle sur la fenêtre d'audit | **{b['vetos'][2]}** |",
        f"| Évaluations sur l'année narrée | {b['evaluations_narrees']} |",
        "",
    ]
    mouvements = b["mouvements"]
    if mouvements:
        out += [("Les mouvements de **l'univers effectif** — celui que la règle "
                 "évalue, exclusions déduites. Un mouvement de l'indice portant "
                 "sur une valeur jamais retenue n'y figure pas, faute d'avoir "
                 "changé quoi que ce soit :"),
                "",
                "| Date de décision | Sortie | Entrée |", "|---|---|---|"]
        for date, sorties, entrees in mouvements:
            out.append(f"| {date} | {', '.join(sorties) or '—'} "
                       f"| {', '.join(entrees) or '—'} |")
        out.append("")
    out += [
        ("Les **divisions postérieures à la fenêtre**, et le contrôle qu'elles "
         "imposent :"),
        "",
        "| Valeur | Division rétro-appliquée par le fournisseur |",
        "|---|---|",
        *(f"| `{ticker}` {SOCIETES.get(ticker, ticker)} | {motif} |"
          for ticker, motif in sorted(SPLITS_POSTERIEURS.items())),
        "",
        ("> Tout ce que la règle calcule est invariant d'échelle ; le **nombre de "
         "titres achetables** ne l'est pas. Un ordre passé sur l'une de ces valeurs "
         "laisserait une opération postérieure à l'année façonner le portefeuille. "
         "Le moteur le **vérifie après simulation et s'arrête** le cas échéant — ce "
         "n'est pas un cinquième veto, c'est un contrôle de recevabilité des "
         "données."),
        "",
        (f"**Contrôle passé** : aucun des {len(b['ordres'])} ordres de l'année ne "
         "porte sur l'une d'elles."),
        "",
    ]
    exclusions = b["exclusions_resume"]
    if exclusions:
        out += ["Les exclusions déclarées, avec leur motif :", "",
                "| Valeur | Dates concernées | Motif |", "|---|---|---|"]
        for nom, combien, motif in exclusions:
            out.append(f"| {nom} | {combien} | {motif} |")
        out.append("")
    return out


def section_audit_regle(b):
    """Section 5 du bilan — les vetos appliques et les poids effectifs."""
    compte, aucun, total, erreurs = b["vetos"]
    out = [
        "",
        "## 5. L'audit de la règle — les vetos et les poids effectifs",
        "",
        ("> Une valeur sous veto ne peut pas entrer. Voici à quelle fréquence les "
         f"quatre vetos se déclenchent, sur les **{total} évaluations** de la "
         "fenêtre d'audit."),
        "",
        "| Veto | Ce qu'il dit | Déclenchements | Taux | IC95 |",
        "|---|---|---|---|---|",
    ]
    for numero in (1, 2, 3, 4):
        n = compte[numero]
        out.append(
            f"| **{numero}** | {LIBELLE_VETO[numero]} | {n} / {total} "
            f"| {fr(100 * n / total, 1)} % | ± {fr(ic95(n, total), 1)} pt |")
    out += [
        "",
        (f"**{aucun} évaluations sur {total}** — {fr(100 * aucun / total, 1)} %, "
         f"± {fr(ic95(aucun, total), 1)} pt — ne déclenchent aucun veto. Ce sont les "
         "seules où un achat était possible."),
        "",
        (f"**{erreurs} évaluations sur {total}** n'ont produit aucun critère. Elles "
         "sont **exclues du classement** : elles n'occupent aucun rang, ne décalent "
         "donc le rang d'aucune autre, et ne peuvent ni faire acheter ni faire "
         "vendre. La colonne `DIAGNOSTIC` de `criteres.csv` en donne la cause, code "
         "de retour compris."),
        "",
        (f"Les vetos ont écarté **{b['occasions']} occasions** — une valeur de rang "
         f"{b['rang_entree']} ou mieux, de score strictement positif, non détenue, "
         "mais sous veto. Ce compte ne regarde pas s'il restait un créneau libre "
         "pour l'acheter : ce n'est pas un compte d'achats. Le compte d'achats, "
         f"lui, vaut **{b['achats_bloques']}** — les ordres que la règle sans veto a "
         "réellement passés sur une valeur alors sous veto."),
        "",
        ("> L'expérience 2 publiait le premier de ces deux nombres sous le nom du "
         "second. Les séparer était la seule façon de rendre le chiffre vérifiable."),
        "",
        "### Les poids effectifs du score",
        "",
        ("> Part de variance expliquée par chaque composante — la covariance de la "
         "composante avec le score, divisée par la variance du score, dont la somme "
         "fait exactement 100 %. Un score à cinq composantes n'a pas cinq axes."),
        "",
        (f"| Composante | Poids sur l'étalonnage ({b['poids_etalonnage'][1]}) "
         f"| Poids sur l'audit ({b['poids_audit'][1]}) |"),
        "|---|---|---|",
    ]
    etalon, _ = b["poids_etalonnage"]
    audit, _ = b["poids_audit"]
    for i in range(5):
        out.append(f"| {LIBELLE_COMPOSANTE[i]} | {fr(etalon[i], 1)} % "
                   f"| {fr(audit[i], 1)} % |")
    out += ["", *phrase_s5(b)]
    return out


def phrase_s5(b):
    """La phrase sur s5, ENGENDREE — jamais ecrite d'avance dans le moteur."""
    positives, negatives, calculables, detail = b["s5"]
    non_nuls = positives + negatives
    if calculables == 0:
        return ["**`s5` n'a été calculable sur aucune évaluation.**"]
    if non_nuls == 0:
        return [(f"**`s5` vaut `0` sur les {calculables} évaluations calculables.** "
                 "L'intervalle de confiance de l'alpha d'une valeur contient zéro "
                 "partout : la composante ne distingue rien sur cette fenêtre. La "
                 "retirer maintenant qu'on l'a vue serait l'ajustement rétrospectif "
                 "que ce protocole s'interdit.")]
    detaille = ", ".join(
        f"`{t}` {haut + bas} fois" for t, (haut, bas) in sorted(detail.items()))
    if positives and negatives:
        repartition = (f"**{positives} fois à `+1`** et **{negatives} fois à `−1`**")
    elif positives:
        repartition = f"**{positives} fois, toutes à `+1`**"
    else:
        repartition = f"**{negatives} fois, toutes à `−1`**"
    return [(f"Sur les {calculables} évaluations calculables de la fenêtre d'audit, "
             f"`s5` est non nulle {repartition} — soit "
             f"{fr(100 * non_nuls / calculables, 1)} % des évaluations, réparties "
             f"sur {len(detail)} valeurs : {detaille}.")]


def section_jugement_vetos(b):
    """Section 6 du bilan — piste C3 : chaque veto contre son issue declaree."""
    jug = b["jugement"]
    out = [
        "",
        "## 6. Chaque veto contre l'issue déclarée avant la première séance",
        "",
        ("> Piste **C3**. Les deux expériences précédentes mesuraient le **taux de "
         "déclenchement** de chaque veto sans jamais demander s'il **sépare** quoi "
         "que ce soit. Le [protocole](README.md#les-quatre-vetos-et-lissue-contre-"
         "laquelle-chacun-sera-jugé) a nommé, avant la première séance, l'issue "
         "observable contre laquelle chacun se juge."),
        "",
        ("| Veto | Issue déclarée | Sous veto | Hors veto | Différence | IC95 de la "
         "différence |"),
        "|---|---|---|---|---|---|",
    ]
    for numero in (1, 2, 3, 4):
        info = jug[numero]
        if info["libelle"] is None:
            out.append(f"| **{numero}** | {ISSUE_VETO[numero]} | — | — | — | — |")
            continue
        sous, hors = info["sous"], info["hors"]
        taux_sous = (f"{fr(100 * sous[0] / sous[1], 1)} % ({sous[0]}/{sous[1]})"
                     if sous[1] else "—")
        taux_hors = (f"{fr(100 * hors[0] / hors[1], 1)} % ({hors[0]}/{hors[1]})"
                     if hors[1] else "—")
        out.append(
            f"| **{numero}** | {ISSUE_VETO[numero]} | {taux_sous} | {taux_hors} "
            f"| **{signe(info['difference'], 1)} pt** "
            f"| ± {fr(info['ic'], 1)} pt |")
    muets = [numero for numero in (1, 2, 3)
             if jug[numero]["difference"] is None]
    if muets:
        out += ["", *[
            (f"**Le veto {numero} n'a pas pu être confronté à son issue** : le "
             f"groupe « {'sous veto' if jug[numero]['sous'][1] == 0 else 'hors veto'} "
             f"» ne contient aucune thèse tranchée. Ce n'est pas une mesure "
             "manquante, c'est une mesure impossible — et c'en est une "
             "information.") for numero in muets]]
        if 2 in muets:
            out += [
                "",
                ("La raison est **structurelle**, et elle se lit au § 9. Le veto 2 "
                 "se déclenche quand τ est inférieur à 20 séances ; la cadence "
                 "médiane entre deux décisions est du même ordre. Or une thèse "
                 "`CANAL` dont τ est plus court que la cadence voit ses bornes "
                 "prolongées se croiser, reçoit le verdict `INCONFIRMABLE` et sort "
                 "du dénominateur. **Le groupe « sous veto 2 » est donc vide par "
                 "construction : le veto et l'issue déclarée sont le même énoncé.**"),
                "",
                ("C'est le genre de découverte que la piste C3 était faite pour "
                 "produire. Le protocole avait déclaré, avant la première séance, "
                 "contre quoi ce veto serait jugé ; l'expérience montre que cette "
                 "déclaration était **circulaire**. Elle ne pouvait pas se voir "
                 "sans être écrite d'abord, et corriger l'issue maintenant qu'on "
                 "la sait vide relèverait d'une expérience suivante, avec sa propre "
                 "déclaration écrite avant."),
            ]
    out += [
        "",
        ("Le veto **4** ne figure au tableau que pour mémoire : il est arithmétique "
         "— moins de 120 séances d'historique — et le protocole a déclaré qu'il ne "
         "prétend séparer aucune issue. L'y confronter serait fabriquer une question "
         "à laquelle il n'a jamais promis de répondre."),
        "",
        ("> **Un veto dont la différence contient zéro n'est pas retiré ici.** Le "
         "protocole l'a déclaré bloquant avant la première séance, et le retirer "
         "après l'avoir vu plat serait le rétro-ajustement même. Le chiffre est "
         "publié ; une expérience suivante en fera ce qu'elle voudra, **par une "
         "déclaration écrite avant sa propre première séance**."),
    ]
    return out


def section_sensibilite(b):
    """Section 7 du bilan — piste C1 : les cinq jeux de parametres."""
    out = [
        "",
        "## 7. La sensibilité aux paramètres de l'encadrement",
        "",
        ("> Piste **C1**. Les deux expériences précédentes appelaient la règle sans "
         "préciser ses paramètres géométriques, laissant agir des défauts que ni le "
         "protocole, ni le miroir, ni le bilan ne citaient. Ici ils sont "
         f"**déclarés** — `--fenetre {FENETRE}`, `--tolerance {fr(TOLERANCE)}` — et "
         "la collecte est relancée sous quatre variantes, elles aussi déclarées "
         "avant la première séance."),
        "",
        ("| Jeu | Fenêtre | Tolérance | Veto 1 | Veto 2 | Veto 3 | Veto 4 "
         "| Aucun veto | `s3` différent du jeu déclaré |"),
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for jeu in b["sensibilite"]:
        total = jeu["total"]
        if total == 0:
            continue
        marque = "**déclaré**" if jeu["role"] == "DECISION" else f"`{jeu['role']}`"
        taux = " | ".join(f"{fr(100 * jeu['compte'][n] / total, 1)} %"
                          for n in (1, 2, 3, 4))
        bascule = ("—" if jeu["role"] == "DECISION" or not jeu["compares"]
                   else f"{fr(100 * jeu['bascules'] / jeu['compares'], 1)} % "
                        f"({jeu['bascules']}/{jeu['compares']})")
        out.append(
            f"| {marque} | {jeu['fenetre']} | {fr(jeu['tolerance'])} | {taux} "
            f"| {fr(100 * jeu['aucun'] / total, 1)} % | {bascule} |")
    ecarts = [jeu for jeu in b["sensibilite"] if jeu["role"] != "DECISION"
              and jeu["total"]]
    if ecarts:
        declare = next(j for j in b["sensibilite"] if j["role"] == "DECISION")
        base = 100 * declare["aucun"] / declare["total"]
        extremes = [100 * j["aucun"] / j["total"] for j in ecarts]
        out += [
            "",
            (f"La part d'évaluations **achetables** — aucun veto — vaut "
             f"{fr(base, 1)} % sous les paramètres déclarés, et s'étend de "
             f"{fr(min(extremes), 1)} % à {fr(max(extremes), 1)} % sur les quatre "
             "variantes."),
            "",
            ("> C'est le chiffre à retenir de cette section : **l'incertitude de "
             "convention se compare directement à l'incertitude d'échantillonnage** "
             f"de ± {fr(ic95(declare['aucun'], declare['total']), 1)} points. "
             "Quand la première dépasse la seconde, publier la seconde seule "
             "reviendrait à annoncer une précision que le protocole n'a pas."),
            "",
            ("Ces variantes **ne décident rien** : aucun euro, aucun classement et "
             "aucune thèse n'en dépend. Elles mesurent, elles n'arbitrent pas."),
        ]
    return out


def section_sens_s3(b):
    """Section 8 du bilan — le sens de s3 et son portefeuille fantome."""
    dim = b["dimension"]
    return [
        "",
        "## 8. Le sens de `s3` — l'aligné contre le fantôme",
        "",
        ("> `s3` suit la règle citée : on achète **bas** dans le canal, pas haut. Le "
         "sens de l'expérience 1 tourne en parallèle, sans engager un euro, et il a "
         "été déclaré avant la première séance."),
        "",
        f"| | Base 100 au {b['fin']} | Performance | Ordres | Frais |",
        "|---|---|---|---|---|",
        (f"| **`s3` aligné** — le portefeuille | **{fr(b['base'])}** "
         f"| {signe(b['base'] - 100)} % | {len(b['ordres'])} "
         f"| {fr(b['frais'])} {EURO} |"),
        (f"| `s3` au sens de l'expérience 1 — le fantôme | {fr(b['base_fantome'])} "
         f"| {signe(b['base_fantome'] - 100)} % | {len(b['ordres_fantome'])} "
         f"| {fr(b['frais_fantome'])} {EURO} |"),
        *(f"| {libelle} | {fr(base)} | {signe(base - 100)} % | {combien} "
          f"| {fr(frais)} {EURO} |" for libelle, base, combien, frais in b["variantes"]),
        "",
        (f"L'écart entre le portefeuille et son fantôme vaut "
         f"**{signe(dim['ecart_fantome'])} point** sur l'année."),
        "",
        ("Ce chiffre est le seul de ce bilan dont l'incertitude soit favorable, et "
         "c'est pourquoi le fantôme existe : les deux portefeuilles partagent "
         "l'univers, les dates et les coûts, si bien que l'écart-type de leur "
         "**différence** est plus faible que celui de chacun contre la référence :"),
        "",
        "| Écart mesuré | Écart-type annualisé | Effet minimal détectable |",
        "|---|---|---|",
        (f"| Portefeuille contre `{REFERENCE}` | {fr(dim['te'])} %/an "
         f"| ± {fr(dim['mde'], 1)} pt |"),
        (f"| Portefeuille contre son fantôme | {fr(dim['te_paire'])} %/an "
         f"| ± {fr(dim['mde_paire'], 1)} pt |"),
        "",
        ("> Ce que le fantôme **ne** dit **pas** : quel sens est le bon. Un an reste "
         "un an. Il dit de combien les deux sens divergent, et à quelle vitesse — "
         "ce qui permet de dimensionner l'expérience qui, elle, pourrait trancher."),
    ]


def section_encadrement(b):
    """Section 9 du bilan — la duree de vie du canal contre la cadence."""
    s, stab = b["survie"], b["stabilite"]
    out = [
        "",
        "## 9. La durée de vie de l'encadrement contre la cadence",
        "",
        ("> Le score lit une position dans un canal. Encore faut-il que le canal "
         "existe encore au moment où l'on relit."),
        "",
        "| Mesure | Valeur |",
        "|---|---|",
        f"| Cadence médiane entre deux décisions | {fr(s['cadence'], 0)} séances |",
        f"| τ médian, canaux convergents | {fr(s['mediane'], 1)} séances |",
        (f"| Canaux parallèles ou divergents (τ infini) | {s['infinis']} / "
         f"{s['mesures']} |"),
        (f"| Canaux se refermant **avant** la décision suivante | {s['courts']} / "
         f"{s['mesures']} — {fr(100 * s['courts'] / s['mesures'], 1)} % |"),
        (f"| Thèses `CANAL` **inconfirmables à l'écriture** | "
         f"{s['inconfirmables']} / {s['total']} |"),
        (f"| Clôtures **sorties** de l'encadrement prolongé | {s['dementies']} / "
         f"{s['tranchees']} — {fr(100 * s['dementies'] / s['tranchees'], 1)} % "
         f"± {fr(ic95(s['dementies'], s['tranchees']), 1)} pt |"),
        "",
        ("> Les thèses **inconfirmables** — celles dont `τ` est plus court que la "
         "cadence, si bien que les bornes prolongées se croisent — sont comptées à "
         "part et **retirées du dénominateur** du taux de démenti. L'expérience 2 "
         "les rangeait parmi les démenties, ce qui gonflait son propre taux."),
        "",
        "### La stabilité rétrospective, à une et deux séances",
        "",
        ("> La décision est recalculée à **d−1** et **d−2 séances**, vers l'arrière "
         "uniquement. Si `s3` bascule quand on décale la décision d'une séance, la "
         "composante mesure du bruit de calendrier, pas une configuration."),
        "",
        ("| Décalage | Bascules de `s3` | Changements de score "
         "| Têtes de classement modifiées |"),
        "|---|---|---|---|",
    ]
    for pas in DECALAGES:
        r = stab[pas]
        if not r["couples"]:
            continue
        out.append(
            f"| **d−{pas}** | {r['s3']} / {r['couples']} "
            f"— {fr(100 * r['s3'] / r['couples'], 1)} % "
            f"| {r['score']} / {r['couples']} "
            f"— {fr(100 * r['score'] / r['couples'], 1)} % "
            f"| {r['tetes']} / {r['dates']} |")
    return out


def section_theses(b):
    """Section 10 du bilan — le registre, ses canaux declares et sa zone morte."""
    theses = b["theses"]
    out = [
        "",
        "## 10. Le registre des thèses réfutables",
        "",
        (f"> **{len(theses)} thèses**, engendrées mécaniquement et dépouillées à la "
         "date suivante. Aucune n'a été rédigée à la main, aucune n'a été retirée."),
        "",
        ("| Thèse | Confirmées | Taux | IC95 | Zone morte | Non tranchées "
         "| Inconfirmables |"),
        "|---|---|---|---|---|---|---|",
    ]
    for libelle, type_, phase in (
        ("`CANAL` — la figure tient", "CANAL", None),
        ("`REFLEXIVE` — toutes phases", "REFLEXIVE", None),
        ("└ `AUTO-RENFORCEMENT`", "REFLEXIVE", "AUTO-RENFORCEMENT"),
        ("└ `RETOURNEMENT`", "REFLEXIVE", "RETOURNEMENT"),
        ("└ `AUCUNE SEQUENCE`", "REFLEXIVE", "AUCUNE SEQUENCE"),
    ):
        confirmees, tranchees, morte, non_tr, incon = taux_theses(theses, type_, phase)
        if not tranchees:
            out.append(f"| {libelle} | — | *aucune tranchée* | — | {morte} "
                       f"| {non_tr} | {incon} |")
            continue
        out.append(
            f"| {libelle} | {confirmees} / {tranchees} "
            f"| {fr(100 * confirmees / tranchees, 1)} % "
            f"| ± {fr(ic95(confirmees, tranchees), 1)} pt "
            f"| {morte} | {non_tr} | {incon} |")
    out += [
        "",
        "### Le champ de la théorie, déclaré avant — piste S1",
        "",
        ("L'expérience 2 a écrit 432 thèses estampillées « au sens de Soros » sans "
         "avoir déclaré par quel mécanisme le cours agirait sur les affaires. Ici, "
         "[`canaux.csv`](canaux.csv) donne le canal de transmission de chaque valeur "
         "**avant la première séance**, ou la mention `aucun`."),
        "",
        "| | |",
        "|---|---|",
        f"| Valeurs à canal de transmission déclaré | {b['avec_canal']} |",
        f"| Valeurs déclarées hors du champ réflexif | {b['sans_canal']} |",
        (f"| Évaluations `HORS CHAMP REFLEXIF` — aucune thèse écrite | "
         f"{b['hors_champ']} |"),
        (f"| Évaluations à canal, mais sans état lisible ou sans σ̂ | "
         f"{b['non_evaluables']} |"),
        "",
        ("> `HORS CHAMP REFLEXIF` dit *« la théorie ne s'applique pas »* ; "
         "`AUCUNE SEQUENCE` dit *« elle s'applique, et il ne se passe rien »*. "
         "L'expérience 2 confondait les deux dans une seule case pesant 340 thèses "
         "sur 432, et son registre faisait dès lors 2,1 points de moins que des "
         "étiquettes tirées au hasard."),
        "",
        "### La clause, normalisée — piste S3",
        "",
        (f"La demi-largeur d'`AUCUNE SEQUENCE` n'est plus une bande fixe : c'est "
         f"$\\hat\\sigma_d$, l'écart-type des {FENETRE_SIGMA} écarts mensuels "
         "précédents de la valeur, tous antérieurs à la date de décision. Une "
         "valeur calme est jugée sur une bande étroite, une valeur agitée sur une "
         "bande large, et le taux de confirmation cesse d'être une mesure de la "
         "volatilité déguisée en mesure de théorie."),
        "",
        (f"Les bornes d'`AUTO-RENFORCEMENT` et de `RETOURNEMENT` sont portées à "
         f"± {fr(DEMI_BORNE, 1)} σ̂ au lieu de zéro. La **zone morte** ainsi créée "
         "reçoit un verdict propre, `ZONE MORTE`, distinct de `NON TRANCHEE` : le "
         "premier dit que la clause a été évaluée et que l'écart est trop petit "
         "pour trancher, le second qu'il manque une donnée. Les deux colonnes du "
         "tableau ci-dessus les séparent."),
    ]
    return out


def section_dimensionnement(b):
    """Section 12 du bilan — piste T1 : le dimensionnement declare, confronte."""
    dim = b["dimension"]
    reg = dim["regression"]
    out = [
        "",
        "## 12. Le dimensionnement, confronté",
        "",
        ("> Piste **T1**. Le "
         "[protocole](README.md#le-dimensionnement-publié-avant-la-première-séance) "
         "a publié **avant la première séance** une tracking error attendue de "
         f"{fr(TE_DECLAREE)} %/an et l'effet minimal détectable qui en découlait. "
         "Voici ce qui s'est réellement produit."),
        "",
        "| | Déclaré avant | Réalisé |",
        "|---|---|---|",
        (f"| Tracking error annualisée | {fr(TE_DECLAREE)} %/an "
         f"| **{fr(dim['te'])} %/an** |"),
        (f"| Effet minimal détectable sur un an | ± {fr(Z95 * TE_DECLAREE, 1)} pt "
         f"| **± {fr(dim['mde'], 1)} pt** |"),
        f"| Alpha mesuré, écart de performance | — | {signe(dim['alpha'])} pt |",
        "",
    ]
    if reg:
        out += [
            "### L'alpha de régression, et pourquoi il diffère",
            "",
            ("> L'écart de performance suppose un bêta de 1. La régression ne le "
             "suppose pas : elle sépare ce que le portefeuille doit à son exposition "
             "de ce qu'il doit au reste. Un portefeuille souvent en espèces a un "
             "bêta nettement inférieur à 1, et l'écart de performance lui attribue "
             "alors une prudence que la régression rend à ce qu'elle est."),
            "",
            "| | |",
            "|---|---|",
            f"| Bêta contre `{REFERENCE}` | **{fr(reg['beta'], 3)}** |",
            f"| Alpha de régression, annualisé | **{signe(reg['alpha'])} %/an** |",
            f"| IC95 de cet alpha | ± {fr(reg['ic_alpha'], 1)} pt |",
            f"| Coefficient de détermination R² | {fr(reg['r2'], 3)} |",
            f"| Écart-type du résidu, annualisé | {fr(reg['sigma_residu'])} %/an |",
            f"| Séances de rendement | {reg['seances']} |",
            f"| Part investie moyenne | {fr(b['part_investie'], 1)} % |",
            (f"| Séances intégralement en espèces | {b['seances_vides']} / "
             f"{len(b['seances'])} |"),
            "",
            ("**Les deux alphas ne mesurent pas la même chose, et aucun des deux ne "
             f"tranche.** L'écart de performance vaut {signe(dim['alpha'])} point "
             f"pour un effet minimal détectable de ± {fr(dim['mde'], 1)} ; l'alpha de "
             f"régression vaut {signe(reg['alpha'])} %/an pour un IC95 de "
             f"± {fr(reg['ic_alpha'], 1)}. Les publier séparément est la seule façon "
             "de ne pas faire passer une exposition pour un talent."),
            "",
        ]
    out += [
        (f"L'alpha de l'année vaut {signe(dim['alpha'])} point pour un effet minimal "
         f"détectable de ± {fr(dim['mde'], 1)} points. **Il est indiscernable de "
         "zéro**, et il était déclaré comme tel avant la première séance."),
        "",
        "## 13. Ce que l'expérience établit, et ce qu'elle n'établit pas",
        "",
        "**Elle établit**, avec les incertitudes publiées :",
        "",
        (f"- à quelle fréquence chacun des quatre vetos se déclenche — § 5, sur "
         f"{b['vetos'][2]} évaluations, contre 432 dans l'expérience 2 ;"),
        ("- **si chaque veto sépare l'issue contre laquelle il a été déclaré "
         "jugeable** — § 6, et c'est la question que les deux expériences "
         "précédentes ne posaient pas ;"),
        ("- **de combien les taux publiés dépendent de paramètres que personne "
         "n'avait déclarés** — § 7 ;"),
        ("- à quelle fréquence l'encadrement ne survit pas d'une décision à la "
         "suivante — § 9 ;"),
        ("- à quelle fréquence `s3` bascule quand on décale la décision d'une seule "
         "séance — § 9, propriété de la composante et non de l'année ;"),
        ("- à quelle fréquence les thèses sont démenties, par type et par phase, "
         "**sur le seul champ où la théorie prétend s'appliquer** — § 10."),
        "",
        "**Elle n'établit pas** :",
        "",
        (f"- que la règle est bonne ou mauvaise. L'écart de performance, "
         f"{signe(dim['alpha'])} point, est plus petit que son propre effet minimal "
         f"détectable de ± {fr(dim['mde'], 1)} points ;"),
        ("- quel sens de `s3` est le bon. L'écart apparié au fantôme est mesuré, son "
         "incertitude aussi, et l'un ne dépasse pas l'autre en un an ;"),
        ("- qu'une des cinq corrections appliquées a **amélioré** quoi que ce soit. "
         "Elles rendent des quantités mesurables ou ferment des failles de "
         "déclaration ; c'est le critère du vote qui les a retenues, et ce n'est "
         "pas un critère de performance ;"),
        "- quoi que ce soit sur 2023. Aucune quantité mesurée ici ne se prolonge.",
        "",
        ("Ce qui reste acquis est de nature différente : **les lignes du tableau de "
         "dimensionnement ont été écrites avant de regarder l'année, et ce sont "
         "exactement celles que l'expérience a pu remplir.**"),
        "",
        "---",
        "",
        (f"[← Protocole](README.md) · [Décembre]({RAPPORTS}/{ANNEE}-12.md) · "
         f"[Janvier]({RAPPORTS}/{ANNEE}-01.md) · "
         f"[La revue de l'expérience 2](../experience_2/review.md)"),
    ]
    return out


def bilan_annuel(b):
    """Rend le document complet du bilan de l'annee."""
    out = [
        f"# Bilan de l'année {ANNEE}",
        "",
        (f"> [Expérience 3](README.md) · dotation {fr(b['dotation'])} {EURO} au "
         f"{b['debut']}, arrêt au {b['fin']} · **{signe(b['base'] - 100)} %** contre "
         f"**{signe(b['ref_fin'] - 100)} %** pour {REFERENCE}"),
        "",
        ("> ⚠️ **L'alpha de cette ligne ne tranche rien**, et le "
         "[protocole](README.md#le-dimensionnement-publié-avant-la-première-séance) "
         "le déclarait avant la première séance. Ce que ce bilan établit est dans "
         "les sections 4 à 10."),
        "",
        "---",
        "",
        "## 1. Le compte",
        "",
        "| | |",
        "|---|---|",
        f"| Dotation | {fr(b['dotation'])} {EURO} au {b['debut']} |",
        f"| Valeur finale | **{fr(b['total'])} {EURO}** |",
        f"| Performance | **{signe(b['base'] - 100)} %** |",
        f"| {REFERENCE}, même convention | {signe(b['ref_fin'] - 100)} % |",
        (f"| **Alpha sur l'année** | **{signe(b['base'] - b['ref_fin'])} pt** "
         "— *indiscernable de zéro* |"),
        (f"| Ordres | {len(b['ordres'])} ({b['achats']} achats, "
         f"{len(b['ordres']) - b['achats']} ventes) |"),
        (f"| Frais cumulés | {fr(b['frais'])} {EURO}, soit "
         f"{fr(100 * b['frais'] / b['dotation'])} % de la dotation |"),
        f"| Repli maximal | {signe(100 * b['repli'])} %, creux au {b['creux']} |",
        f"| Espèces au {b['fin']} | {fr(b['especes_fin'])} {EURO} |",
        f"| Part investie moyenne | {fr(b['part_investie'], 1)} % |",
        (f"| Séances intégralement en espèces | {b['seances_vides']} / "
         f"{len(b['seances'])} |"),
        "",
        "## 2. Mois par mois",
        "",
        (f"| Mois | Valeur | Base 100 | {REFERENCE} | Alpha du mois "
         "| Alpha cumulé | Ordres |"),
        "|---|---|---|---|---|---|---|",
    ]
    valeurs, ref100, seances = b["valeurs"], b["ref100"], b["seances"]
    for mois in sorted({j[:7] for j in seances}):
        borne = derniere_seance(seances, mois)
        veille = derniere_seance(seances, mois_precedent(mois))
        base_p = valeurs[veille][2] if veille else b["dotation"]
        base_r = ref100[veille] if veille else 100.0
        alpha_mois = 100 * (valeurs[borne][2] / base_p - ref100[borne] / base_r)
        combien = sum(1 for o in b["ordres"] if o["DATE"][:7] == mois)
        out.append(
            f"| {MOIS_TITRE[mois[5:7]]} | [{fr(valeurs[borne][2])} {EURO}]"
            f"({RAPPORTS}/{mois}.md) | {fr(100 * valeurs[borne][2] / b['dotation'])} "
            f"| {fr(ref100[borne])} | {signe(alpha_mois)} pt "
            f"| {signe(100 * valeurs[borne][2] / b['dotation'] - ref100[borne])} pt "
            f"| {combien or '—'} |")

    lignes = b["positions"]
    out += [
        "",
        "## 3. Les positions",
        "",
        (f"> Alpha d'une position : son rendement moins celui de {REFERENCE} sur "
         "**la même période de détention**. La contribution en euros est nette des "
         "frais des deux sens."),
        "",
        ("| Valeur | Achat | Sortie | Séances | Prix d'achat | Prix de sortie "
         "| +/− value | Alpha | Contribution |"),
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for ligne in lignes:
        sortie = (f"{ligne['vente']} *(ouverte)*" if ligne["ouverte"]
                  else ligne["vente"])
        out.append(
            f"| `{ligne['ticker']}` {SOCIETES[ligne['ticker']]} | {ligne['achat']} "
            f"| {sortie} | {ligne['seances']} | {fr(ligne['prix_achat'])} {EURO} "
            f"| {fr(ligne['prix_vente'])} {EURO} | **{signe(ligne['pv'])} %** "
            f"| {signe(ligne['alpha'])} pt | {signe(ligne['euros'])} {EURO} |")
    if lignes:
        gagnantes = sum(1 for ligne in lignes if ligne["euros"] > 0)
        out += [
            "",
            (f"**{gagnantes} positions sur {len(lignes)}** finissent en gain net de "
             "frais. La contribution la plus forte est "
             f"{signe(max(ligne['euros'] for ligne in lignes))} {EURO}, la plus faible "
             f"{signe(min(ligne['euros'] for ligne in lignes))} {EURO}."),
            "",
            (("Le contrefactuel « garder le portefeuille de janvier jusqu'au bout » "
              "**n'existe pas cette année** : aucun achat n'a eu lieu à la première "
              "séance. Le tenir aurait donc voulu dire rester en espèces douze "
              f"mois, pour {fr(100 * b['tenu'] / b['dotation'])} en base 100.")
             if b["achats_debut"] == 0 else
             ("Le contrefactuel qui isole l'apport des ordres suivant janvier : "
              "**garder le portefeuille de janvier jusqu'au bout** aurait rendu "
              f"{fr(100 * b['tenu'] / b['dotation'])} au lieu de {fr(b['base'])}, soit "
              f"**{signe(b['base'] - 100 * b['tenu'] / b['dotation'])} point**.")),
        ]
    else:
        out += ["", "*Aucune position ouverte sur l'année.*"]

    out += section_univers(b)
    out += section_audit_regle(b)
    out += section_jugement_vetos(b)
    out += section_sensibilite(b)
    out += section_sens_s3(b)
    out += section_encadrement(b)
    out += section_theses(b)
    out += [
        "",
        "## 11. Les trois conventions",
        "",
        ("> ⚠️ `Close` est **ajustée des dividendes**, "
         f"`{REFERENCE_NUE}` ne l'est pas. Comparer les deux fabrique de l'alpha à "
         "partir de rien."),
        "",
        f"| Série | Convention | {ANNEE} | Alpha du portefeuille |",
        "|---|---|---|---|",
        f"| Le portefeuille | rendement total | **{signe(b['base'] - 100)} %** | — |",
        (f"| `{REFERENCE}` | rendement total | {signe(b['ref_fin'] - 100)} % "
         f"| **{signe(b['base'] - b['ref_fin'])} pt** |"),
        (f"| `{REFERENCE_NUE}` | indice **nu** | {signe(b['nue'])} % "
         f"| {signe(b['base'] - 100 - b['nue'])} pt |"),
        "",
        (f"L'écart de convention vaut **{fr(abs(b['ref_fin'] - 100 - b['nue']))} "
         "points** sur l'année. Il est déclaré, pas deviné : c'est pour cela que la "
         f"référence est `{REFERENCE}` et non `{REFERENCE_NUE}`."),
    ]
    out += section_dimensionnement(b)
    return NL_.join(out) + NL_


# --------------------------------------------------------------------------
# Assemblage


def analyser_arguments(taille_univers):
    parser = argparse.ArgumentParser(
        description=f"Journal de l'experience 3 : 10 000 EUR sur {ANNEE}, "
                    "tout le CAC 40 a sa composition du jour.")
    ici = Path(__file__).resolve().parent
    parser.add_argument("--collecter", action="store_true", help="Relancer la collecte")
    parser.add_argument("--repertoire", type=Path, default=ici, help="Ou lire et ecrire")
    parser.add_argument("--quotes", type=Path, default=QUOTES_DEFAUT,
                        help="Ou sont les series")
    parser.add_argument("--dotation", type=float, default=10000.0,
                        help="Dotation en euros")
    parser.add_argument("--lignes", type=int, default=5,
                        help="Lignes detenues au maximum")
    parser.add_argument("--rang-entree", type=int, default=5, help="Rang d'achat")
    parser.add_argument("--rang-sortie", type=int, default=7, help="Rang de vente")
    parser.add_argument("--mois", help="N'afficher que ce mois (AAAA-MM)")
    parser.add_argument("--markdown", action="store_true",
                        help="Ecrire aussi les journaux mensuels et le bilan")
    parser.add_argument("--repartition", choices=("creneaux", "candidats"),
                        default="creneaux",
                        help="Diviser les especes par creneaux libres ou par candidats")
    parser.add_argument("--recollecter", action="store_true",
                        help="Repartir de zero au lieu de completer criteres.csv")
    parser.add_argument("--taches", type=int, default=8,
                        help="Sous-processus simultanes pendant la collecte")
    parser.add_argument("--sans-veto", action="store_true",
                        help="Diagnostic : afficher aussi la regle vetos jetes")
    args = parser.parse_args()
    if args.rang_sortie < args.rang_entree:
        erreur("--rang-sortie doit etre superieur ou egal a --rang-entree (hysteresis)")
    if args.dotation <= 0:
        erreur("--dotation doit etre strictement positive")
    if not 1 <= args.lignes <= taille_univers:
        erreur(f"--lignes doit etre entre 1 et {taille_univers}")
    if not 1 <= args.taches <= 32:
        erreur("--taches doit etre entre 1 et 32")
    return args


def apports_du_mois(etape, contexte, veille, fin_mois):
    """Contributions en euros du mois, LIGNES VENDUES COMPRISES.

    L'experience 2 ne regardait que les lignes encore detenues a la fin du mois :
    une ligne vendue le 2 et suivie d'une chute y etait invisible.
    """
    apports = []
    for ordre in etape["ordres"]:
        if ordre["SENS"] != "VENTE":
            continue
        info = etape["etat_avant"].get(ordre["TICKER"])
        if info is None:
            continue
        base = (series_close(contexte, ordre["TICKER"], veille)
                if veille and info["date"] <= veille else info["prix"])
        apports.append({
            "ticker": ordre["TICKER"],
            "euros": ordre["QUANTITE"] * (ordre["PRIX"] - base) - ordre["FRAIS"],
        })
    frais_achat = {o["TICKER"]: o["FRAIS"] for o in etape["ordres"]
                   if o["SENS"] == "ACHAT"}
    for ticker, info in etape["tenues"].items():
        base = (series_close(contexte, ticker, veille)
                if veille and info["date"] <= veille else info["prix"])
        apports.append({
            "ticker": ticker,
            "euros": (info["quantite"] * (series_close(contexte, ticker, fin_mois) - base)
                      - frais_achat.get(ticker, 0.0)),
        })
    return apports


def ecrire_rapports(args, contexte, historique, theses_par_date, textes, univers,
                    index, ordres):
    """Ecrit les douze journaux mensuels."""
    actualites, notes = textes
    valeurs, ref100 = contexte["valeurs"], contexte["ref100"]
    seances = contexte["seances"]
    executions = [etape["date_exec"] for etape in historique]
    debut = contexte["debut"]

    for rang, etape in enumerate(historique):
        mois, date_decision = etape["mois"], etape["date_decision"]
        fin_mois = derniere_seance(seances, mois)
        jours = [j for j in seances if j <= fin_mois]
        courbe = [100 * valeurs[j][2] / args.dotation for j in jours]
        svg(args.repertoire / GRAPHIQUES / f"portefeuille-{mois}.svg",
            jours, courbe, [ref100[j] for j in jours], executions, debut)

        veille = derniere_seance(seances, mois_precedent(mois))
        base_p = valeurs[veille][2] if veille else args.dotation
        base_r = ref100[veille] if veille else 100.0
        alpha_mois = 100 * (valeurs[fin_mois][2] / base_p - ref100[fin_mois] / base_r)

        apports = apports_du_mois(etape, contexte, veille, fin_mois)
        precedente = contexte["date_precedente"][date_decision]
        depouillement = theses_par_date.get(precedente, [])
        confirmees = sum(1 for t in depouillement if t["VERDICT"] == "CONFIRMEE")
        tranchees = sum(1 for t in depouillement
                        if t["VERDICT"] in ("CONFIRMEE", "DEMENTIE"))

        precedent_mois, suivant_mois = mois_precedent(mois), suivant(mois)
        navigation = []
        if rang > 0:
            navigation.append(f"[← {MOIS_TITRE[precedent_mois[5:7]]}]"
                              f"({precedent_mois}.md)")
        navigation.append("[Protocole](../README.md)")
        if rang + 1 < len(historique):
            navigation.append(f"[{MOIS_TITRE[suivant_mois[5:7]]} →]"
                              f"({suivant_mois}.md)")

        figures = {ligne["TICKER"] for ligne in etape["classement"]
                   if chemin_figure(args.repertoire, ligne["TICKER"],
                                    date_decision).exists()}

        contexte_mois = {
            "date_decision": date_decision, "date_exec": etape["date_exec"],
            "date_precedente": precedente, "fin_mois": fin_mois, "debut": debut,
            "dotation": args.dotation,
            "especes": valeurs[fin_mois][0], "titres": valeurs[fin_mois][1],
            "total": valeurs[fin_mois][2],
            "base": courbe[-1], "reference": ref100[fin_mois],
            "alpha_mois": alpha_mois,
            "alpha_global": courbe[-1] - ref100[fin_mois],
            "actualites": actualites.get(mois, ""),
            "notes": notes.get(date_decision, {}),
            "etat_avant": etape["etat_avant"], "gardees": etape["gardees"],
            "classement": etape["classement"],
            "manquantes": non_classees(contexte["criteres"], date_decision,
                                       univers[date_decision], index),
            "positions": positions_a_date(ordres, fin_mois),
            "figures": figures,
            "ordres": etape["ordres"],
            "depouillement": depouillement,
            "theses": theses_par_date.get(date_decision, []),
            "lecture": lecture_du_mois(apports, etape["ordres"], alpha_mois,
                                       (confirmees, tranchees), args.dotation),
            "navigation": " · ".join(navigation),
            "dernier": rang + 1 == len(historique),
        }
        ecrire_texte(args.repertoire / RAPPORTS / f"{mois}.md",
                     journal_mensuel(mois, contexte_mois))


def series_close(contexte, ticker, jour):
    return contexte["series"][ticker][jour]["close"]


def mouvements_indice(univers, dates):
    """Rend [(date, sorties, entrees)] pour les dates ou l'univers change."""
    out = []
    for i in range(1, len(dates)):
        avant, apres = set(univers[dates[i - 1]]), set(univers[dates[i]])
        sorties, entrees = sorted(avant - apres), sorted(apres - avant)
        if sorties or entrees:
            out.append((dates[i],
                        [SOCIETES.get(t, t) for t in sorties],
                        [SOCIETES.get(t, t) for t in entrees]))
    return out


def resumer_exclusions(exclusions):
    """Rend [(nom, nombre de dates, motif)], motifs regroupes."""
    compte = {}
    for lignes in exclusions.values():
        for nom, _ticker, motif in lignes:
            # Le motif des series trop courtes cite le nombre de seances, qui
            # change a chaque date : le regrouper sur ce nombre produirait une
            # ligne par date au lieu d'une par cause.
            racine = "seances-reelles" if "seances reelles" in motif else motif
            cle = (nom, racine)
            compte[cle] = compte.get(cle, 0) + 1
    resume = []
    for (nom, motif), combien in sorted(compte.items()):
        libelle = ("moins de 253 séances de volume strictement positif"
                   if motif == "seances-reelles" else motif)
        resume.append((nom, f"{combien} date{'s' if combien > 1 else ''}", libelle))
    return resume


def construire_bilan(args, criteres, series, reference, nue, valeurs, valeurs_f,
                     valeurs_c, valeurs_l, ordres, ordres_f, ordres_c, ordres_l,
                     historique, theses, univers, exclusions, canaux,
                     dates_audit, dates_depouillement, dates_ref, etalonnage,
                     seances, ref100, debut, fin, hors_champ, non_evaluables):
    """Rassemble tout ce que le bilan publie."""
    pic, repli, creux = -1e9, 0.0, fin
    for jour in seances:
        pic = max(pic, valeurs[jour][2])
        if valeurs[jour][2] / pic - 1 < repli:
            repli, creux = valeurs[jour][2] / pic - 1, jour

    dates_investies = [etape["date_decision"] for etape in historique]
    stab = stabilite(criteres, dates_investies, args, univers)
    part_investie, seances_vides = exposition(valeurs, seances)
    tickers = sorted({t for tickers in univers.values() for t in tickers})

    return {
        "dotation": args.dotation, "debut": debut, "fin": fin,
        "rang_entree": args.rang_entree,
        "total": valeurs[fin][2], "base": 100 * valeurs[fin][2] / args.dotation,
        "base_fantome": 100 * valeurs_f[fin][2] / args.dotation,
        "ref_fin": ref100[fin],
        "nue": 100 * (nue[fin]["close"] / nue[debut]["close"] - 1),
        "ordres": ordres, "ordres_fantome": ordres_f,
        "achats": sum(1 for o in ordres if o["SENS"] == "ACHAT"),
        "frais": sum(o["FRAIS"] for o in ordres),
        "frais_fantome": sum(o["FRAIS"] for o in ordres_f),
        "variantes": [
            ("`--repartition candidats` — la répartition de l'expérience 1",
             100 * valeurs_c[fin][2] / args.dotation, len(ordres_c),
             sum(o["FRAIS"] for o in ordres_c)),
            ("`--sans-veto` — les vetos calculés mais jetés, comme en 2022",
             100 * valeurs_l[fin][2] / args.dotation, len(ordres_l),
             sum(o["FRAIS"] for o in ordres_l)),
        ],
        "repli": repli, "creux": creux, "especes_fin": valeurs[fin][0],
        "valeurs": valeurs, "ref100": ref100, "seances": seances,
        "part_investie": part_investie, "seances_vides": seances_vides,
        "positions": positions_de_lannee(ordres, series, reference, fin),
        "tenu": janvier_tenu(ordres, series, args.dotation, debut, fin),
        "achats_debut": sum(1 for o in ordres
                            if o["DATE"] == debut and o["SENS"] == "ACHAT"),
        "dates_audit": len(dates_audit),
        "tickers_distincts": len(tickers),
        "evaluations_narrees": sum(len(univers[d]) for d in dates_investies),
        "mouvements": mouvements_indice(univers, dates_audit),
        "exclusions_resume": resumer_exclusions(exclusions),
        "vetos": taux_vetos(criteres, set(dates_audit), univers),
        "occasions": occasions_bloquees(historique, args),
        "achats_bloques": achats_bloques(ordres_l),
        "poids_etalonnage": poids_effectifs(criteres, {d for d, _ in etalonnage},
                                            "aligne", univers),
        "poids_audit": poids_effectifs(criteres, set(dates_audit), "aligne", univers),
        "s5": occurrences_s5(criteres, set(dates_audit), "aligne", univers),
        "stabilite": stab,
        "jugement": jugement_vetos(theses, criteres, stab),
        "sensibilite": sensibilite(criteres, set(dates_audit), univers),
        "survie": survie_encadrement(theses, criteres, dates_audit,
                                     dates_depouillement, dates_ref, univers),
        "theses": theses,
        "hors_champ": hors_champ, "non_evaluables": non_evaluables,
        "avec_canal": sum(1 for t in tickers if canaux[t][0] != "aucun"),
        "sans_canal": sum(1 for t in tickers if canaux[t][0] == "aucun"),
        "dimension": dimensionnement(valeurs, ref100, valeurs_f, seances,
                                     args.dotation),
    }


def imprimer_bilan(b, args, fin, debut, theses):
    """Le bloc console de fin d'execution."""
    dim = b["dimension"]
    reg = dim["regression"]
    confirmees = sum(1 for t in theses if t["VERDICT"] == "CONFIRMEE")
    tranchees = sum(1 for t in theses if t["VERDICT"] in ("CONFIRMEE", "DEMENTIE"))
    compte, aucun, total, erreurs = b["vetos"]
    ligne_reg = ("  Alpha de regression     "
                 f"{signe(reg['alpha'])} %/an  (beta {fr(reg['beta'], 3)}, "
                 f"IC95 +/- {fr(reg['ic_alpha'], 1)} pt)" if reg else "")
    print(f"""
=== Bilan au {fin} ===

  Dotation                {fr(args.dotation)} EUR au {debut}
  Valeur finale           {fr(b['total'])} EUR
  Performance             {signe(b['base'] - 100)} %
  {REFERENCE}                    {signe(b['ref_fin'] - 100)} %
  Alpha sur l'annee       {signe(b['base'] - b['ref_fin'])} pt \
(non concluant : MDE +/- {fr(dim['mde'], 1)} pt)
{ligne_reg}
  Part investie moyenne   {fr(b['part_investie'], 1)} % \
{MEDIAN} {b['seances_vides']} seances integralement en especes
  Fantome (s3 exp. 1)     {fr(b['base_fantome'])} base 100 \
{MEDIAN} ecart appari {signe(dim['ecart_fantome'])} pt \
(MDE +/- {fr(dim['mde_paire'], 1)} pt)
  Ordres                  {len(b['ordres'])} ({b['achats']} achats, \
{len(b['ordres']) - b['achats']} ventes)
  Frais cumules           {fr(b['frais'])} EUR, soit \
{fr(100 * b['frais'] / args.dotation)} % de la dotation
  Vetos declenches        {total - aucun} / {total} evaluations \
(1:{compte[1]} 2:{compte[2]} 3:{compte[3]} 4:{compte[4]}) \
{MEDIAN} {erreurs} evaluations impossibles
  Occasions bloquees      {b['occasions']} \
{MEDIAN} achats bloques {b['achats_bloques']}
  Theses                  {len(theses)} ecrites, {confirmees} confirmees \
sur {tranchees} tranchees
  Hors champ reflexif     {b['hors_champ']} \
{MEDIAN} sans etat lisible ou sans sigma {b['non_evaluables']}
""")


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")

    ici = Path(__file__).resolve().parent
    univers, exclusions, tous = charger_univers(ici)
    args = analyser_arguments(max(len(v) for v in univers.values()))
    if args.repertoire != ici:
        univers, exclusions, tous = charger_univers(args.repertoire)
    canaux = charger_canaux(args.repertoire, tous)
    if not args.quotes.is_dir():
        erreur(f"Repertoire introuvable : {args.quotes}")

    series = {t: charger_serie(nom_fichier(t, args.quotes)) for t in tous}
    reference = charger_serie(nom_fichier(REFERENCE, args.quotes))
    nue = charger_serie(nom_fichier(REFERENCE_NUE, args.quotes))
    dates_ref = sorted(reference)

    couples = calendrier(dates_ref)
    audit = [c for c in couples if c[0][:7] >= MOIS_AUDIT_DEBUT]
    investis = [c for c in audit if c[0][:7] >= MOIS_INVESTI_DEBUT]
    etalonnage = [c for c in audit if c[0][:7] <= MOIS_ETALONNAGE_FIN]
    if len(audit) != COUPLES_AUDIT or len(investis) != COUPLES_INVESTIS:
        erreur(f"Calendrier incomplet : {len(audit)} dates d'audit et "
               f"{len(investis)} investies, au lieu de {COUPLES_AUDIT} et "
               f"{COUPLES_INVESTIS}")
    absentes = [d for d, _ in audit if d not in univers]
    if absentes:
        erreur("Dates de decision absentes de univers.csv : " + ", ".join(absentes))

    narrees = {d for d, _ in investis}
    if args.collecter or args.recollecter:
        print("Collecte des criteres par python/generer_graph_decision.py")
        collecter(dates_a_evaluer(audit, investis, dates_ref, univers), args.quotes,
                  args.repertoire, series, args.taches, narrees,
                  reprendre=not args.recollecter)

    chemin_criteres = args.repertoire / "criteres.csv"
    if not chemin_criteres.exists():
        erreur(f"{chemin_criteres} absent : relancer avec --collecter")
    with chemin_criteres.open(encoding="utf-8") as flux:
        criteres = list(csv.DictReader(flux))
    index = index_criteres(criteres)

    debut, fin = investis[0][1], dates_ref[-1]
    seances = [d for d in dates_ref if debut <= d <= fin]
    ref100 = {j: 100 * reference[j]["close"] / reference[debut]["close"]
              for j in seances}

    ordres, valeurs, historique = simuler(investis, criteres, series, reference,
                                          seances, args, "aligne", univers)
    ordres_f, valeurs_f, _ = simuler(investis, criteres, series, reference,
                                     seances, args, "fantome", univers)
    ordres_c, valeurs_c, _ = simuler(investis, criteres, series, reference, seances,
                                     args, "aligne", univers,
                                     repartition="candidats")
    ordres_l, valeurs_l, _ = simuler(investis, criteres, series, reference, seances,
                                     args, "aligne", univers, vetos_appliques=False)
    verifier_splits(ordres)

    dates_audit = [decision for decision, _ in audit]
    dates_depouillement = [*dates_audit[1:], fin]
    theses, hors_champ, non_evaluables = ecrire_theses(
        criteres, dates_audit, dates_depouillement, series, reference, dates_ref,
        univers, canaux)
    theses_par_date = {}
    for these in theses:
        theses_par_date.setdefault(these["DATE"], []).append(these)

    classements = []
    for date in dates_audit:
        for ligne in classer(criteres, date, "aligne", univers[date]):
            classements.append({**ligne, "TAU": tau_texte(ligne["TAU"])})

    ecrire_csv(args.repertoire / "classement.csv", ENTETE_CLASSEMENT, classements)
    ecrire_csv(args.repertoire / "ordres.csv", ENTETE_ORDRES, ordres)
    ecrire_csv(args.repertoire / "theses.csv", ENTETE_THESES, theses)
    for nom, table in (("portefeuille.csv", valeurs), ("fantome.csv", valeurs_f)):
        ecrire_csv(args.repertoire / nom, ENTETE_PORTEFEUILLE, [
            {"DATE": j, "ESPECES": round(table[j][0], 2),
             "TITRES": round(table[j][1], 2), "TOTAL": round(table[j][2], 2),
             "BASE100": round(100 * table[j][2] / args.dotation, 4),
             "REFERENCE100": round(ref100[j], 4)} for j in seances])

    contexte = {
        "valeurs": valeurs, "ref100": ref100, "seances": seances, "series": series,
        "debut": debut, "criteres": criteres,
        "date_precedente": {decision: dates_audit[i - 1] if i > 0 else ""
                            for i, decision in enumerate(dates_audit)},
    }

    if args.markdown:
        textes = charger_textes(args.repertoire)
        ecrire_rapports(args, contexte, historique, theses_par_date, textes,
                        univers, index, ordres)

    b = construire_bilan(args, criteres, series, reference, nue, valeurs, valeurs_f,
                         valeurs_c, valeurs_l, ordres, ordres_f, ordres_c, ordres_l,
                         historique, theses, univers, exclusions, canaux,
                         dates_audit, dates_depouillement, dates_ref, etalonnage,
                         seances, ref100, debut, fin, hors_champ, non_evaluables)

    if args.markdown:
        ecrire_texte(args.repertoire / BILAN, bilan_annuel(b))

    for etape in historique:
        mois = etape["mois"]
        if args.mois and args.mois != mois:
            continue
        fin_mois = derniere_seance(seances, mois)
        veille = derniere_seance(seances, mois_precedent(mois))
        base_p = valeurs[veille][2] if veille else args.dotation
        base_r = ref100[veille] if veille else 100.0
        etat_apres = {
            "base": 100 * valeurs[fin_mois][2] / args.dotation,
            "reference": ref100[fin_mois],
            "alpha_mois": 100 * (valeurs[fin_mois][2] / base_p
                                 - ref100[fin_mois] / base_r),
            "alpha_global": (100 * valeurs[fin_mois][2] / args.dotation
                             - ref100[fin_mois]),
        }
        manquantes = non_classees(criteres, etape["date_decision"],
                                  univers[etape["date_decision"]], index)
        print(bloc_mensuel(mois, etape, etat_apres, valeurs, seances, manquantes))

    if args.sans_veto:
        print(f"""
=== Diagnostic --sans-veto ===

  Avec vetos              {fr(b['base'])} base 100, {len(ordres)} ordres
  Sans vetos              {fr(100 * valeurs_l[fin][2] / args.dotation)} \
base 100, {len(ordres_l)} ordres
  Occasions bloquees      {b['occasions']}
  Achats bloques          {b['achats_bloques']}
""")

    imprimer_bilan(b, args, fin, debut, theses)

    ecrits = ["classement.csv", "ordres.csv", "theses.csv", "portefeuille.csv",
              "fantome.csv"]
    if args.markdown:
        ecrits += [f"{GRAPHIQUES}/portefeuille-{ANNEE}-MM.svg ({len(historique)} mois)",
                   f"{RAPPORTS}/{ANNEE}-MM.md ({len(historique)} rapports)", BILAN]
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
