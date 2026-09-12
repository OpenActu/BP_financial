"""Moteur de l'experience 6 : dix lignes, un achat persistant, un alpha contre son exposition.

Applique la regle de l'experience 4 a dix lignes, en exigeant deux clotures
consecutives sous le bord bas a l'achat ; rejoue la regle de l'experience 4 et
verifie qu'elle est retrouvee ; isole l'effet de chaque changement par les quatre
combinaisons lignes x persistance ; mesure l'alpha officiel contre la reference a
exposition appariee ; et reprend tout l'appareil de mesure de l'experience 5.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_6/journal.py
    python docs/done/experimentation/experience_6/journal.py --figures
    python docs/done/experimentation/experience_6/journal.py --markdown
    python docs/done/experimentation/experience_6/journal.py --mois 2022-03
"""

import argparse
import csv
import datetime
import math
import statistics
import sys
from pathlib import Path

REFERENCE = "TR39"
REFERENCE_NUE = "^FCHI"
RAPPORTS = "rapports"
GRAPHIQUES = "graphiques"
ANNEE = "2022"
BILAN = f"bilan-{ANNEE}.md"
DEBUT_SERIE = "2019-01-02"
FIN_SERIE = "2022-12-30"
DEBUT_AUDIT = "2020-12-31"
DEBUT_NARREE = "2021-12-31"
SEANCES_ETALONNAGE = 258
SEANCES_NARREES = 257

LONGUE = 120
COURTE = 20
TOP = 10
K = 1.0
VARIANTES = (
    ("VAR-TOP5", 5, 1.0),
    ("VAR-TOP20", 20, 1.0),
    ("VAR-K05", 10, 0.5),
    ("VAR-K15", 10, 1.5),
)
HORIZON = 20
PAS_ECHANTILLON = 20
FRAIS_EXPERIENCE_3 = 75.24
Z95 = 1.96

DOTATION = 10000.0
LIGNES = 10                      # piste 4
PERSISTANCE = 2                  # piste 1 : clotures consecutives sous le bord bas
COMBINAISONS = (("L5-P1", 5, 1), ("L10-P1", 10, 1), ("L5-P2", 5, 2), ("L10-P2", 10, 2))
TE_DECLAREE = 5.25               # piste 2 : contre la reference appariee, projetee sur 2021
TE_TR39_PROJETEE = 9.95
FIN_ETALONNAGE = "2021-12-30"    # aucune seance lue au-dela pour les projections
FIN_SEMESTRE = "2022-06-30"      # T2 : borne des deux semestres
FIN_SEMESTRE_2021 = "2021-06-30"
PHASES = 20                      # T1 : les vingt phases du sous-echantillon
SEUIL_PHASES = 11                # T1 : la majorite exigee
RISQUE = 0.05                    # T1 : risque de la famille de Holm
DATES_MIN = 3
TIRAGES_REFERENCE = 20000        # C1
GRAINE_IID = 1
GRAINE_MARCHE = 2
TIRAGES_TEMOIN = 4000            # T2
GRAINE_TEMOIN = 3
RESERVOIR_FOI = "UNIVERS"
CONTROLE = (31, 10051.09)        # le portefeuille de l'experience 4

# Les effectifs et EMD projetes par l'experience 4 (Welch), et par grappes (T1).
PROJECTIONS = {
    "TOP10": ("260 contre 747", 0.9), "CRITERE-2": ("84 contre 176", 1.7),
    "CRITERE-3": ("22 contre 62", 3.1), "VENTE": ("193 contre 814", 1.0),
}
EMD_GRAPPES = {"TOP10": 2.0, "CRITERE-2": 2.9, "CRITERE-3": 5.1, "VENTE": 1.1,
               "PERSISTANCE": None}

# C1 : les references et la matrice observee de 2021, publiees au README.
REFERENCES_PUBLIEES = {
    "iid": {"sous": 15.3, "dans": 69.1, "dessus": 15.6, "bande": 67.5,
            "matrice": ((16.4, 67.2, 16.4), (16.6, 67.5, 15.8), (16.4, 67.4, 16.2))},
    "marche": {"sous": 25.7, "dans": 48.9, "dessus": 25.4, "bande": 47.6,
               "matrice": ((87.7, 12.3, 0.0), (7.5, 84.4, 8.1), (0.0, 12.4, 87.6))},
    "observe_2021": {"matrice": ((85.9, 14.0, 0.1), (6.9, 86.8, 6.3), (0.2, 13.9, 85.9))},
}

# Les grandeurs de 2021 publiees au README de l'experience 6.
PROJECTIONS_PUBLIEES = {
    "L5-P1": {"te": 11.08, "te_app": 9.08, "beta": 0.832, "part": 75.5, "vides": 10,
              "ordres": 34, "frais": 203.65, "duree": 55.5, "ouvertes": 2, "perdus": 75},
    "L10-P1": {"te": 9.82, "te_app": 6.06, "beta": 0.630, "part": 56.4, "vides": 10,
               "ordres": 52, "frais": 145.16, "duree": 54, "ouvertes": 2, "perdus": 5},
    "L5-P2": {"te": 11.02, "te_app": 8.69, "beta": 0.798, "part": 67.1, "vides": 11,
              "ordres": 33, "frais": 183.24, "duree": 53.0, "ouvertes": 1, "perdus": 38},
    "L10-P2": {"te": 9.95, "te_app": 5.25, "beta": 0.509, "part": 44.0, "vides": 11,
               "ordres": 45, "frais": 119.37, "duree": 53.0, "ouvertes": 1, "perdus": 1},
    "SANS-P20": {"te": 9.55, "beta": 0.796, "part": 68.6, "vides": 11, "ordres": 65,
                 "frais": 196.99, "duree": 53, "ouvertes": 7, "perdus": 132},
    "MENSUEL": {"te": 12.60, "beta": 0.120, "part": 10.9, "vides": 61, "ordres": 9,
                "frais": 22.42, "duree": 56.0, "ouvertes": 1, "perdus": 0},
    "paires": {"L10-P1": 3.18, "L5-P2": 6.61, "L5-P1": 8.20, "SANS-P20": 7.14,
               "MENSUEL": 8.28, "MENSUEL_neutralise": 6.19},
    "temoin": {"UNIVERS": 4.72, "TOP10": 3.46},
    "betas_semestres": {"premier": 0.346, "second": 0.642},
    "candidats_persistants": 143,
}

# Les nombres publies au README avant la premiere seance, que le moteur recalcule.
ETALONNAGE_PUBLIE = {
    "evaluations": 9932, "muettes": 0,
    "positifs_min": 22, "positifs_mediane": 33, "positifs_max": 36,
    "entrants_moyenne": 0.17, "jours_entrant": 43,
    "sous_bas": 2346, "au_dessus": 1904, "dans_bande": 5682,
    "top_sous_bas": 746, "top_au_dessus": 293, "places_top": 2580,
    "candidats": 210, "sous_bas_pente_negative": 536, "jours_candidat": 123,
    "bande_suivante": 5499, "bande_total": 9893,
    "sd_quotidien": 6.06, "sd_echantillon": 6.44,
}

COURTAGE = 0.10
SPREAD = 0.015
TTF = 0.30
EXEMPTES_TTF = ("AIR.PA", "STLAP.PA", "MT.AS", "STMPA.PA")

# Divisions survenues APRES FIN_SERIE et repercutees retroactivement : le nombre
# de titres achetables serait faconne par une operation posterieure a l'annee.
SPLITS_POSTERIEURS = {
    "AI.PA": "2024-06-10 et 2026-06-08, attributions gratuites 1,1 (facteur 0,826)",
    "ATO.PA": "2025-04-24, regroupement 1 pour 10 000 (facteur 10 000)",
    "WLN.PA": "2026-06-15, regroupement 1 pour 40 (facteur 40)",
}

QUOTES_DEFAUT = Path("docs/raw/data/quotes")
COLONNES = ("E_120", "VAR_120", "CORR_120", "VAL_120",
            "E_20", "VAR_20", "CORR_20", "VAL_20")

ENTETE_EVALUATIONS = [
    "DATE", "TICKER", "UNIVERS", "CLOSE", "E_120", "VAL_120", "S_120", "TAUX_120",
    "ECART_S", "E_20", "VAL_20", "TAUX_20", "ENV_BAS", "ENV_HAUT", "LARGEUR_ENV_S",
    "RANG", "CANDIDAT", "DIAGNOSTIC",
]
ENTETE_TOP = ["DATE", "RANG", "TICKER", "TAUX_120", "ECART_S", "TAUX_20", "CANDIDAT"]
ENTETE_ORDRES = [
    "DATE", "DATE_DECISION", "TICKER", "SENS", "QUANTITE", "PRIX", "BRUT", "FRAIS",
    "NET", "RANG", "TAUX_120", "ECART_S", "TAUX_20", "ECART_OUVERTURE", "MOTIF",
]
ENTETE_SIGNAUX = ["DATE_DECISION", "TICKER", "RANG", "ECART_S", "TAUX_20", "SORT"]
ENTETE_ISSUES = [
    "DATE", "TICKER", "PHASE", "SOUS_ECHANTILLON", "TOP10", "SOUS_BAS", "AU_DESSUS_HAUT",
    "TAUX_20_POSITIF", "PERSISTANT", "EXCES_20", "BANDE_SUIVANTE",
]
ENTETE_PORTEFEUILLE = ["DATE", "ESPECES", "TITRES", "TOTAL", "BASE100",
                       "REFERENCE100", "LIGNES"]

NBSP = " "
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


def oui(booleen):
    return "oui" if booleen else "non"


def ic95(succes, total):
    """Demi-largeur de l'IC a 95 % d'une proportion, en points."""
    if total <= 0:
        return None
    p = succes / total
    return 100 * Z95 * math.sqrt(p * (1 - p) / total)


def pourcent(n, total, decimales=1):
    return "—" if not total else f"{fr(100 * n / total, decimales)} %"


def lendemain(jour):
    """« 2022-12-30 » -> « 2022-12-31 » : --fin est exclusif dans import_societe.py."""
    return (datetime.date.fromisoformat(jour) + datetime.timedelta(days=1)).isoformat()


def mois_precedent(mois):
    annee, numero = int(mois[:4]), int(mois[5:7])
    return f"{annee - 1}-12" if numero == 1 else f"{annee}-{numero - 1:02d}"


def mois_suivant(mois):
    annee, numero = int(mois[:4]), int(mois[5:7])
    return f"{annee + 1}-01" if numero == 12 else f"{annee}-{numero + 1:02d}"


def ecrire_csv(chemin, entete, lignes):
    """Ecrit un CSV, cellule vide plutot qu'un nombre invente."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
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


def arrondi(x, decimales=6):
    return None if x is None else round(x, decimales)


# --------------------------------------------------------------------------
# Lecture : l'univers, les series, le calendrier


def nom_fichier(ticker, quotes):
    """Le CSV de la plage declaree. Un glob choisirait le mauvais fichier."""
    chemin = quotes / f"{ticker.replace('.', '_')}_{DEBUT_SERIE}_{FIN_SERIE}.csv"
    if not chemin.exists():
        erreur(f"Serie absente : {chemin}\n"
               f"  python python/import_societe.py {ticker} "
               f"--debut {DEBUT_SERIE} --fin {lendemain(FIN_SERIE)}")
    return chemin


def flottant(texte):
    return float(texte) if texte not in (None, "") else None


def charger_serie(chemin):
    """Rend {'jours', 'par_jour', 'rang'} ; une cellule vide vaut None."""
    jours, par_jour = [], {}
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            cloture = flottant(ligne.get("Close"))
            if cloture is None:
                continue
            jour = ligne["Date"][:10]
            seance = {
                "open": flottant(ligne.get("Open")) or cloture,
                "high": flottant(ligne.get("High")) or cloture,
                "low": flottant(ligne.get("Low")) or cloture,
                "close": cloture,
            }
            for colonne in COLONNES:
                seance[colonne] = flottant(ligne.get(colonne))
            jours.append(jour)
            par_jour[jour] = seance
    return {"jours": jours, "par_jour": par_jour,
            "rang": {jour: i for i, jour in enumerate(jours)}}


def charger_univers(repertoire):
    """Rend (lignes retenues, exclusions). L'univers ne se devine pas."""
    chemin = repertoire / "univers.csv"
    if not chemin.exists():
        erreur(f"{chemin} absent : l'univers point-in-time ne se devine pas")
    retenues, exclusions = [], []
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            if ligne["RETENUE"] == "oui":
                retenues.append(ligne)
            else:
                exclusions.append(ligne)
    manquants = [ligne["TICKER"] for ligne in retenues if ligne["TICKER"] not in SOCIETES]
    if manquants:
        erreur("Tickers sans nom declare dans SOCIETES : " + ", ".join(manquants))
    return retenues, exclusions


def univers_du_jour(retenues, jour):
    """Les tickers dans l'indice ET evaluables a `jour`, bornes incluses."""
    return tuple(sorted(
        ligne["TICKER"] for ligne in retenues
        if (not ligne["ENTREE_INDICE"] or ligne["ENTREE_INDICE"] <= jour)
        and (not ligne["SORTIE_INDICE"] or ligne["SORTIE_INDICE"] >= jour)
        and (not ligne["EVALUABLE_DES"] or ligne["EVALUABLE_DES"] <= jour)))


# --------------------------------------------------------------------------
# Phase 1 : l'evaluation de chaque valeur a chaque seance


def variance_temps(n):
    return (n * n - 1) / 12


def enveloppe(serie, jour):
    """Regresse les COURTE clotures finissant a `jour` et rend l'enveloppe des residus.

    Rend (env_bas, env_haut, indice du minimum, indice du maximum), indices de 1
    a COURTE, ou None s'il manque des clotures.
    """
    i = serie["rang"][jour]
    if i + 1 < COURTE:
        return None
    valeurs = [serie["par_jour"][serie["jours"][j]]["close"]
               for j in range(i - COURTE + 1, i + 1)]
    moyenne_t = (COURTE + 1) / 2
    moyenne_v = statistics.fmean(valeurs)
    cov = sum((t - moyenne_t) * (v - moyenne_v)
              for t, v in enumerate(valeurs, start=1)) / COURTE
    pente = cov / variance_temps(COURTE)
    residus = [v - (moyenne_v + pente * (t - moyenne_t))
               for t, v in enumerate(valeurs, start=1)]
    i_bas = min(range(COURTE), key=lambda j: residus[j])
    i_haut = max(range(COURTE), key=lambda j: residus[j])
    return -residus[i_bas], residus[i_haut], i_bas + 1, i_haut + 1


def evaluer(serie, ticker, jour):
    """Rend l'evaluation d'une valeur a la cloture de `jour`, ou une evaluation muette."""
    seance = serie["par_jour"].get(jour)
    muette = {"DATE": jour, "TICKER": ticker, "MUETTE": True,
              "CLOSE": seance["close"] if seance else None}
    if seance is None:
        return {**muette, "DIAGNOSTIC": "aucune seance a cette date"}
    vides = [c for c in COLONNES if seance[c] is None]
    if vides:
        return {**muette, "DIAGNOSTIC": "colonne vide : " + ", ".join(vides)}
    env = enveloppe(serie, jour)
    # Les conditions sont lues dans l'ordre : le diagnostic cite la premiere.
    for defaut, diagnostic in (
            (seance["VAR_120"] <= 0 or seance["VAR_20"] <= 0, "variance glissante nulle"),
            (1 - seance["CORR_120"] ** 2 <= 0,
             "1 - CORR_120^2 nul : bande d'epaisseur nulle"),
            (seance["E_120"] <= 0 or seance["E_20"] <= 0,
             "moyenne glissante non strictement positive"),
            (env is None, f"moins de {COURTE} clotures")):
        if defaut:
            return {**muette, "DIAGNOSTIC": diagnostic}

    r_120 = seance["CORR_120"] * math.sqrt(seance["VAR_120"] / variance_temps(LONGUE))
    s_120 = math.sqrt(LONGUE / (LONGUE - 2) * seance["VAR_120"]
                      * (1 - seance["CORR_120"] ** 2))
    r_20 = seance["CORR_20"] * math.sqrt(seance["VAR_20"] / variance_temps(COURTE))
    s_20 = math.sqrt(COURTE / (COURTE - 2) * seance["VAR_20"]
                     * max(1 - seance["CORR_20"] ** 2, 0.0))
    env_bas, env_haut, i_bas, i_haut = env
    return {
        "DATE": jour, "TICKER": ticker, "MUETTE": False, "DIAGNOSTIC": "",
        "CLOSE": seance["close"], "E_120": seance["E_120"], "VAL_120": seance["VAL_120"],
        "R_120": r_120, "S_120": s_120, "TAUX_120": 100 * r_120 / seance["E_120"],
        "ECART_S": (seance["close"] - seance["VAL_120"]) / s_120,
        "E_20": seance["E_20"], "VAL_20": seance["VAL_20"], "R_20": r_20, "S_20": s_20,
        "TAUX_20": 100 * r_20 / seance["E_20"],
        "ENV_BAS": env_bas, "ENV_HAUT": env_haut, "ENV_I_BAS": i_bas,
        "ENV_I_HAUT": i_haut,
        "LARGEUR_ENV_S": (env_bas + env_haut) / s_20 if s_20 > 0 else None,
    }


def bord_bas(ev, k=K):
    return ev["VAL_120"] - k * ev["S_120"]


def bord_haut(ev, k=K):
    return ev["VAL_120"] + k * ev["S_120"]


# --------------------------------------------------------------------------
# Phase 2 : le TOP 10


def classer(evaluations_jour, univers):
    """Rend {ticker: rang} des pentes STRICTEMENT positives de l'univers du jour."""
    positives = [evaluations_jour[t] for t in univers
                 if not evaluations_jour[t]["MUETTE"] and evaluations_jour[t]["TAUX_120"] > 0]
    positives.sort(key=lambda ev: (-ev["TAUX_120"], ev["TICKER"]))
    return {ev["TICKER"]: rang for rang, ev in enumerate(positives, start=1)}


def est_candidat(ev, rang, taille=TOP, k=K, avec_p20=True):
    """Propriete de la valeur et du jour, independante du portefeuille."""
    return (rang is not None and rang <= taille and not ev["MUETTE"]
            and ev["ECART_S"] < -k and (not avec_p20 or ev["TAUX_20"] > 0))


def sous_bas_veille(ctx, ticker, jour):
    """La cloture de la seance precedant `jour` etait-elle sous le bord bas ?"""
    cle = (ticker, jour)
    if cle not in ctx["veille"]:
        reference = ctx["reference"]
        veille = reference["jours"][reference["rang"][jour] - 1]
        ev = ctx["evaluations"].get(veille, {}).get(ticker)
        if ev is None:
            ev = evaluer(ctx["series"][ticker], ticker, veille)
        ctx["veille"][cle] = not ev["MUETTE"] and ev["ECART_S"] < -K
    return ctx["veille"][cle]


def candidat(ctx, ticker, jour, persistance=PERSISTANCE, avec_p20=True):
    """La regle de l'experience 6 : seule la condition de bande persiste."""
    ev = ctx["evaluations"][jour][ticker]
    if not est_candidat(ev, ctx["rangs"][jour].get(ticker), avec_p20=avec_p20):
        return False
    return persistance == 1 or sous_bas_veille(ctx, ticker, jour)


# --------------------------------------------------------------------------
# Phase 3 : la simulation, seance par seance


def taux_achat(ticker):
    return (COURTAGE + SPREAD + (0.0 if ticker in EXEMPTES_TTF else TTF)) / 100


def taux_vente(_ticker):
    return (COURTAGE + SPREAD) / 100


def seance_execution(ctx, ticker, jour, quoi):
    seance = ctx["series"][ticker]["par_jour"].get(jour)
    if seance is None:
        erreur(f"{ticker} : pas de seance au {jour}, {quoi} impossible")
    return seance


def ordre(ctx, sens, ticker, quantite, decision, execution, rang):
    """Rend un ordre complet, motif engendre et ecart d'ouverture compris."""
    ev = ctx["evaluations"][decision][ticker]
    prix = seance_execution(ctx, ticker, execution, sens.lower())["open"]
    brut = quantite * prix
    frais = brut * (taux_achat(ticker) if sens == "ACHAT" else taux_vente(ticker))
    if sens == "ACHAT":
        motif = (f"clôture {fr(ev['CLOSE'])} {EURO} sous le bord bas "
                 f"{fr(bord_bas(ev))} {EURO} ({signe(ev['ECART_S'])} s), rang {rang}, "
                 f"TAUX_120 {signe(ev['TAUX_120'], 3)} %/séance, "
                 f"TAUX_20 {signe(ev['TAUX_20'], 3)} %/séance")
    else:
        motif = (f"clôture {fr(ev['CLOSE'])} {EURO} au-dessus du bord haut "
                 f"{fr(bord_haut(ev))} {EURO} ({signe(ev['ECART_S'])} s)")
    return {
        "DATE": execution, "DATE_DECISION": decision, "TICKER": ticker, "SENS": sens,
        "QUANTITE": quantite, "PRIX": prix, "BRUT": brut, "FRAIS": frais,
        "NET": brut + frais if sens == "ACHAT" else brut - frais,
        "RANG": rang, "TAUX_120": ev["TAUX_120"], "ECART_S": ev["ECART_S"],
        "TAUX_20": ev["TAUX_20"],
        "ECART_OUVERTURE": 100 * (prix / ev["CLOSE"] - 1), "MOTIF": motif,
    }


def simuler(ctx, decisions, seances, lignes=LIGNES, persistance=PERSISTANCE, avec_p20=True):
    """Rend (ordres, signaux, valeurs, journal, registre) pour une comptabilite.

    Chaque seance de `seances` est valorisee a la cloture ; des ordres n'y sont
    passes que si la seance qui la precede appartient a `decisions`. Avec une
    decision par seance, c'est exactement la simulation de l'experience 4.
    """
    calendrier, rang_cal = ctx["reference"]["jours"], ctx["reference"]["rang"]
    decisions = set(decisions)
    detenues, especes = {}, DOTATION
    ordres, signaux, valeurs, journal, registre = [], [], {}, {}, []

    for execution in seances:
        decision = calendrier[rang_cal[execution] - 1]
        if decision not in decisions:
            titres = sum(ligne["quantite"]
                         * seance_execution(ctx, t, execution, "valorisation")["close"]
                         for t, ligne in detenues.items())
            valeurs[execution] = (especes, titres, especes + titres, len(detenues))
            continue
        evaluations, rangs = ctx["evaluations"][decision], ctx["rangs"][decision]
        du_jour, muettes = [], []

        for ticker in sorted(detenues):
            ev = evaluations[ticker]
            if ev["MUETTE"]:
                muettes.append(ticker)
                detenues[ticker]["silence"] += 1
                continue
            if ev["ECART_S"] > K:
                vente = ordre(ctx, "VENTE", ticker, detenues[ticker]["quantite"],
                              decision, execution, rangs.get(ticker))
                especes += vente["NET"]
                ligne = detenues.pop(ticker)
                ligne.update({"vente": execution, "prix_vente": vente["PRIX"],
                              "frais": ligne["frais"] + vente["FRAIS"]})
                du_jour.append(vente)

        creneaux = lignes - len(detenues)
        part = especes / creneaux if creneaux > 0 else 0.0
        candidats = sorted(
            (t for t in ctx["univers"][decision]
             if t not in detenues and candidat(ctx, t, decision, persistance, avec_p20)),
            key=lambda t: rangs[t])
        pris = 0
        for ticker in candidats:
            ev = evaluations[ticker]
            if ticker in SPLITS_POSTERIEURS:
                sort = "REFUSE DIVISION"
            elif pris >= creneaux:
                sort = "FAUTE DE CRENEAU"
            else:
                pris += 1
                prix = seance_execution(ctx, ticker, execution, "achat")["open"]
                quantite = int(part // (prix * (1 + taux_achat(ticker))))
                if quantite < 1:
                    sort = "QUANTITE NULLE"
                else:
                    sort = "EXECUTE"
                    achat = ordre(ctx, "ACHAT", ticker, quantite, decision, execution,
                                  rangs[ticker])
                    especes -= achat["NET"]
                    ligne = {"ticker": ticker, "achat": execution, "decision": decision,
                             "prix_achat": achat["PRIX"], "quantite": quantite,
                             "frais": achat["FRAIS"], "silence": 0, "vente": None,
                             "prix_vente": None}
                    detenues[ticker] = ligne
                    registre.append(ligne)
                    du_jour.append(achat)
            signaux.append({"DATE_DECISION": decision, "TICKER": ticker,
                            "RANG": rangs[ticker], "ECART_S": ev["ECART_S"],
                            "TAUX_20": ev["TAUX_20"], "SORT": sort})

        titres = sum(ligne["quantite"]
                     * seance_execution(ctx, t, execution, "valorisation")["close"]
                     for t, ligne in detenues.items())
        valeurs[execution] = (especes, titres, especes + titres, len(detenues))
        ordres.extend(du_jour)
        journal[decision] = {"execution": execution, "ordres": du_jour,
                             "muettes": muettes, "lignes": len(detenues),
                             "signaux": [s for s in signaux
                                         if s["DATE_DECISION"] == decision]}
    return ordres, signaux, valeurs, journal, registre


def charger_experience_3(repertoire, seances):
    """Rend {date: (titres, total)} du portefeuille de l'experience 3."""
    chemin = repertoire.parent / "experience_3" / "portefeuille.csv"
    if not chemin.exists():
        erreur(f"{chemin} absent : la comparaison appariee est declaree au protocole")
    table = {}
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            table[ligne["DATE"]] = (float(ligne["TITRES"]), float(ligne["TOTAL"]))
    manquantes = [j for j in seances if j not in table]
    if manquantes:
        erreur(f"{chemin} : {len(manquantes)} seances manquantes, dont {manquantes[0]}")
    return table


# --------------------------------------------------------------------------
# Phase 5 : les issues declarees


def issues(ctx, jours, borne):
    """Une ligne par (seance, ticker de l'univers) non muette. Rien au-dela de `borne`."""
    reference = ctx["reference"]
    calendrier, rang = reference["jours"], reference["rang"]
    phase = ctx["phase"]
    lignes = []
    for jour in jours:
        i = rang[jour]
        horizon = (calendrier[i + HORIZON] if i + HORIZON < len(calendrier)
                   and calendrier[i + HORIZON] <= borne else None)
        suivante = (calendrier[i + 1] if i + 1 < len(calendrier)
                    and calendrier[i + 1] <= borne else None)
        rangs = ctx["rangs"][jour]
        for ticker in ctx["univers"][jour]:
            ev = ctx["evaluations"][jour][ticker]
            if ev["MUETTE"]:
                continue
            serie = ctx["series"][ticker]["par_jour"]
            exces = None
            if horizon and horizon in serie:
                exces = 100 * (serie[horizon]["close"] / ev["CLOSE"]
                               - reference["par_jour"][horizon]["close"]
                               / reference["par_jour"][jour]["close"])
            bande = None
            if suivante and suivante in serie:
                cloture = serie[suivante]["close"]
                bande = (bord_bas(ev) + ev["R_120"] <= cloture
                         <= bord_haut(ev) + ev["R_120"])
            rang_t = rangs.get(ticker)
            lignes.append({
                "DATE": jour, "TICKER": ticker, "PHASE": phase[jour],
                "SOUS_ECHANTILLON": phase[jour] == 0,
                "TOP10": rang_t is not None and rang_t <= TOP,
                "SOUS_BAS": ev["ECART_S"] < -K, "AU_DESSUS_HAUT": ev["ECART_S"] > K,
                "TAUX_20_POSITIF": ev["TAUX_20"] > 0,
                "PERSISTANT": ev["ECART_S"] < -K and sous_bas_veille(ctx, ticker, jour),
                "EXCES_20": exces, "BANDE_SUIVANTE": bande,
            })
    return lignes


COMPARAISONS = (
    ("TOP10", "TOP 10", "l'univers", "les places du TOP 10", "le reste de l'univers",
     lambda li: True, lambda li: li["TOP10"]),
    ("CRITERE-2", "Critère 2 — sous le bord bas", "le TOP 10",
     "TOP 10 sous le bord bas", "reste du TOP 10",
     lambda li: li["TOP10"], lambda li: li["SOUS_BAS"]),
    ("CRITERE-3", "Critère 3 — pente courte positive", "TOP 10 sous le bord bas",
     "candidats", "pente courte nulle ou négative",
     lambda li: li["TOP10"] and li["SOUS_BAS"], lambda li: li["TAUX_20_POSITIF"]),
    ("VENTE", "Vente — au-dessus du bord haut", "l'univers",
     "au-dessus du bord haut", "reste de l'univers",
     lambda li: True, lambda li: li["AU_DESSUS_HAUT"]),
    ("PERSISTANCE", "Persistance — la veille aussi sous le bord bas",
     "candidats de l'expérience 4", "persistants", "non persistants",
     lambda li: li["TOP10"] and li["SOUS_BAS"] and li["TAUX_20_POSITIF"],
     lambda li: li["PERSISTANT"]),
)


def comparer(lignes, population, groupe):
    """Deux groupes d'EXCES_20 : effectifs, moyennes, difference et IC95 (Welch)."""
    retenues = [li for li in lignes if population(li)]
    a = [li["EXCES_20"] for li in retenues if groupe(li) and li["EXCES_20"] is not None]
    b = [li["EXCES_20"] for li in retenues
         if not groupe(li) and li["EXCES_20"] is not None]
    resultat = {
        "na": len(a), "nb": len(b),
        "moy_a": statistics.fmean(a) if a else None,
        "moy_b": statistics.fmean(b) if b else None,
        "difference": None, "ic": None,
        "non_tranchees": sum(1 for li in retenues if li["EXCES_20"] is None),
    }
    if len(a) >= 2 and len(b) >= 2:
        resultat["difference"] = resultat["moy_a"] - resultat["moy_b"]
        resultat["ic"] = Z95 * math.sqrt(statistics.variance(a) / len(a)
                                         + statistics.variance(b) / len(b))
    return resultat


def bande(lignes):
    """(dans la bande prolongee, issues tranchees)."""
    tranchees = [li for li in lignes if li["BANDE_SUIVANTE"] is not None]
    return sum(1 for li in tranchees if li["BANDE_SUIVANTE"]), len(tranchees)


# --------------------------------------------------------------------------
# Phase 6 : les audits


def taux_regle(ctx, jours, borne):
    """Les taux publies au README, recalcules sur `jours`, sans rien lire apres `borne`."""
    t = dict.fromkeys(("evaluations", "muettes", "sous_bas", "au_dessus", "dans_bande",
                       "top_sous_bas", "top_au_dessus", "places_top", "candidats",
                       "sous_bas_pente_negative", "jours_candidat", "jours_entrant",
                       "jours_top_court", "jours_split_top", "candidats_persistants"), 0)
    positifs, entrants, precedent = [], [], None
    for jour in jours:
        evaluations, rangs = ctx["evaluations"][jour], ctx["rangs"][jour]
        for ticker in ctx["univers"][jour]:
            t["evaluations"] += 1
            ev = evaluations[ticker]
            if ev["MUETTE"]:
                t["muettes"] += 1
                continue
            t["sous_bas"] += ev["ECART_S"] < -K
            t["au_dessus"] += ev["ECART_S"] > K
            t["dans_bande"] += -K <= ev["ECART_S"] <= K
        top = [tk for tk, r in rangs.items() if r <= TOP]
        positifs.append(len(rangs))
        t["jours_top_court"] += len(top) < TOP
        t["jours_split_top"] += any(tk in SPLITS_POSTERIEURS for tk in top)
        if precedent is not None:
            nouveaux = len(set(top) - set(precedent))
            entrants.append(nouveaux)
            t["jours_entrant"] += nouveaux > 0
        precedent = top
        candidat = False
        for ticker in top:
            ev = evaluations[ticker]
            t["places_top"] += 1
            t["top_au_dessus"] += ev["ECART_S"] > K
            if ev["ECART_S"] < -K:
                t["top_sous_bas"] += 1
                if ev["TAUX_20"] > 0:
                    t["candidats"] += 1
                    t["candidats_persistants"] += sous_bas_veille(ctx, ticker, jour)
                    candidat = True
                else:
                    t["sous_bas_pente_negative"] += 1
        t["jours_candidat"] += candidat
    lignes = issues(ctx, jours, borne)
    t["bande_suivante"], t["bande_total"] = bande(lignes)
    quotidien = [li["EXCES_20"] for li in lignes if li["EXCES_20"] is not None]
    echantillon = [li["EXCES_20"] for li in lignes
                   if li["EXCES_20"] is not None and li["SOUS_ECHANTILLON"]]
    t.update({
        "jours": len(jours), "positifs_min": min(positifs), "positifs_max": max(positifs),
        "positifs_mediane": statistics.median(positifs),
        "entrants_moyenne": statistics.fmean(entrants) if entrants else None,
        "transitions": len(entrants),
        "sd_quotidien": statistics.stdev(quotidien) if len(quotidien) > 1 else None,
        "n_quotidien": len(quotidien),
        "sd_echantillon": statistics.stdev(echantillon) if len(echantillon) > 1 else None,
        "n_echantillon": len(echantillon),
    })
    return t


def sensibilite(ctx):
    """Les taux sous le jeu declare et les quatre variantes, sur l'audit."""
    resultat = []
    for nom, taille, k in (("déclaré", TOP, K), *VARIANTES):
        evaluees = candidats = ventes = 0
        entrants, precedent = [], None
        for jour in ctx["jours_audit"]:
            evaluations, rangs = ctx["evaluations"][jour], ctx["rangs"][jour]
            for ticker in ctx["univers"][jour]:
                ev = evaluations[ticker]
                if ev["MUETTE"]:
                    continue
                evaluees += 1
                ventes += ev["ECART_S"] > k
                candidats += est_candidat(ev, rangs.get(ticker), taille, k)
            top = {tk for tk, r in rangs.items() if r <= taille}
            if precedent is not None:
                entrants.append(len(top - precedent))
            precedent = top
        resultat.append({"nom": nom, "top": taille, "k": k, "evaluees": evaluees,
                         "candidats": candidats, "ventes": ventes,
                         "entrants": statistics.fmean(entrants)})
    return resultat


def positions_annee(ctx, registre, fin):
    """Chaque position de l'annee : issue, alpha, contribution, repli maximal."""
    reference = ctx["reference"]["par_jour"]
    lignes = []
    for ligne in registre:
        ticker = ligne["ticker"]
        serie = ctx["series"][ticker]["par_jour"]
        sortie = ligne["vente"] or fin
        prix_sortie = ligne["prix_vente"] if ligne["vente"] else serie[fin]["close"]
        jours = [j for j in ctx["series"][ticker]["jours"] if ligne["achat"] <= j <= sortie]
        lignes.append({
            **ligne, "sortie": sortie, "ouverte": ligne["vente"] is None,
            "prix_sortie": prix_sortie, "seances": len(jours),
            "pv": 100 * (prix_sortie / ligne["prix_achat"] - 1),
            "alpha": 100 * (prix_sortie / ligne["prix_achat"]
                            - reference[sortie]["close"] / reference[ligne["achat"]]["close"]),
            "euros": ligne["quantite"] * (prix_sortie - ligne["prix_achat"]) - ligne["frais"],
            "repli_close": 100 * (min(serie[j]["close"] for j in jours)
                                  / ligne["prix_achat"] - 1),
            "repli_low": 100 * (min(serie[j]["low"] for j in jours)
                                / ligne["prix_achat"] - 1),
        })
    lignes.sort(key=lambda x: (x["achat"], x["ticker"]))
    return lignes


def regression(base, indice):
    """Beta, alpha annualise, IC95 de l'alpha, R2 et sigma du residu."""
    rp = [base[i] / base[i - 1] - 1 for i in range(1, len(base))]
    rm = [indice[i] / indice[i - 1] - 1 for i in range(1, len(indice))]
    if len(rp) < 3 or statistics.pvariance(rm) == 0:
        return None
    moy_p, moy_m = statistics.fmean(rp), statistics.fmean(rm)
    cov = sum((rp[i] - moy_p) * (rm[i] - moy_m) for i in range(len(rp))) / len(rp)
    beta = cov / statistics.pvariance(rm)
    alpha_jour = moy_p - beta * moy_m
    residus = [rp[i] - alpha_jour - beta * rm[i] for i in range(len(rp))]
    sigma = statistics.stdev(residus)
    var_p = statistics.pvariance(rp)
    return {"beta": beta, "alpha": 100 * alpha_jour * 252,
            "ic_alpha": 100 * Z95 * sigma / math.sqrt(len(rp)) * 252,
            "r2": 1 - statistics.pvariance(residus) / var_p if var_p else None,
            "sigma_residu": 100 * sigma * math.sqrt(252), "seances": len(rp)}


def ecart_type_ecarts(a, b):
    """Ecart-type annualise, en points, des ecarts de rendements quotidiens."""
    ecarts = [(a[i] / a[i - 1] - 1) - (b[i] / b[i - 1] - 1) for i in range(1, len(a))]
    return statistics.stdev(ecarts) * math.sqrt(252) * 100 if len(ecarts) > 1 else None


def exposition(valeurs, seances):
    """Part investie moyenne et seances integralement en especes."""
    parts = [100 * valeurs[j][1] / valeurs[j][2] if valeurs[j][2] else 0.0 for j in seances]
    return statistics.fmean(parts), sum(1 for j in seances if valeurs[j][1] <= 0)


# --------------------------------------------------------------------------
# Phase 7 : les figures


def echapper(texte):
    return texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pas_lisible(amplitude, cibles=6):
    """Le pas de grille 1, 2, 2,5 ou 5 x 10^p le plus proche de amplitude / cibles."""
    brut = max(amplitude / cibles, 1e-12)
    puissance = 10 ** math.floor(math.log10(brut))
    for multiple in (1, 2, 2.5, 5, 10):
        if multiple * puissance >= brut:
            return multiple * puissance
    return 10 * puissance


def chemin_figure(repertoire, ticker, jour):
    """Une figure propre a une societe va dans un sous-repertoire a son ticker."""
    return repertoire / GRAPHIQUES / ticker / f"canal-{ticker}-{jour}.svg"


def verdict_du_jour(ctx, ticker, jour):
    """Le verdict de la regle a la cloture de `jour`, independant du portefeuille."""
    ev = ctx["evaluations"][jour][ticker]
    if ev["MUETTE"]:
        return "évaluation muette"
    if ticker in ctx["univers"][jour] and candidat(ctx, ticker, jour):
        return "candidate à l'achat"
    if ev["ECART_S"] > K:
        return "au-dessus du bord haut"
    return "sous le bord bas" if ev["ECART_S"] < -K else "dans la bande"


def figure_canal(chemin, ctx, ticker, jour):
    """Ecrit la figure de canal d'une valeur a une seance. Rien apres `jour`."""
    ev = ctx["evaluations"][jour][ticker]
    serie = ctx["series"][ticker]
    i = serie["rang"][jour]
    jours = serie["jours"][max(0, i - LONGUE + 1):i + 1]
    closes = [serie["par_jour"][j]["close"] for j in jours]
    n = len(jours)

    def f120(t):
        return ev["VAL_120"] + ev["R_120"] * (t - n)

    def f20(t):
        return ev["VAL_20"] + ev["R_20"] * (t - n)

    s = K * ev["S_120"]
    debut_20 = n - COURTE + 1
    candidats = [*closes, f120(1) - s, f120(1) + s, f120(n) - s, f120(n) + s,
                 f20(debut_20) - ev["ENV_BAS"], f20(n) - ev["ENV_BAS"],
                 f20(debut_20) + ev["ENV_HAUT"], f20(n) + ev["ENV_HAUT"]]
    bas, haut = min(candidats), max(candidats)
    coussin = (haut - bas) * 0.06 or 1.0
    bas, haut = bas - coussin, haut + coussin

    largeur, hauteur = 900, 470
    marge_g, marge_d, marge_h, marge_b = 72, 22, 78, 58
    aire_l, aire_h = largeur - marge_g - marge_d, hauteur - marge_h - marge_b

    def x(t):
        return marge_g + aire_l * (t - 1) / max(n - 1, 1)

    def y(v):
        return marge_h + aire_h * (haut - v) / (haut - bas)

    rang = ctx["rangs"][jour].get(ticker)
    verdict = verdict_du_jour(ctx, ticker, jour)
    couleur_point = {"candidate à l'achat": "#2e7d32",
                     "au-dessus du bord haut": "#c62828"}.get(verdict, "#1a1a1a")
    classement = (f"rang {rang}" + (" au TOP 10" if rang <= TOP else "")
                  if rang else "pente nulle ou négative, hors classement")
    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{marge_g}" y="26" font-size="15" font-weight="600" fill="#1a1a1a">'
         f'{echapper(SOCIETES[ticker])} ({ticker}) &#8212; canal au {jour}</text>'),
        (f'<text x="{marge_g}" y="46" font-size="11.5" fill="#444444">'
         f'{echapper(classement)} &#183; TAUX_120 {signe(ev["TAUX_120"], 3)} %/s&#233;ance '
         f'&#183; cl&#244;ture {fr(ev["CLOSE"])} &#8364;, {signe(ev["ECART_S"])} s '
         f'&#183; TAUX_20 {signe(ev["TAUX_20"], 3)} %/s&#233;ance</text>'),
        (f'<text x="{marge_g}" y="63" font-size="11.5" fill="#444444">'
         f'bande 120 &#177; {fr(K, 1)} s : {fr(f120(n) - s)} &#8211; {fr(f120(n) + s)} &#8364; '
         f'&#183; enveloppe 20 : {fr(ev["LARGEUR_ENV_S"], 2)} s, '
         f'{fr(100 * (ev["ENV_BAS"] + ev["ENV_HAUT"]) / ev["E_20"], 1)} % '
         f'&#183; verdict : <tspan font-weight="600" fill="{couleur_point}">'
         f'{echapper(verdict)}</tspan></text>'),
    ]
    pas = pas_lisible(haut - bas)
    niveau = math.ceil(bas / pas) * pas
    while niveau <= haut:
        out.append(f'<line x1="{marge_g}" y1="{y(niveau):.1f}" x2="{largeur - marge_d}" '
                   f'y2="{y(niveau):.1f}" stroke="#eeeeee" stroke-width="1"/>')
        out.append(f'<text x="{marge_g - 8}" y="{y(niveau) + 4:.1f}" font-size="10.5" '
                   f'fill="#666666" text-anchor="end">{fr(niveau, 2 if pas < 1 else 0)}</text>')
        niveau += pas
    out.append(
        f'<polygon points="{x(1):.1f},{y(f120(1) + s):.1f} {x(n):.1f},{y(f120(n) + s):.1f} '
        f'{x(n):.1f},{y(f120(n) - s):.1f} {x(1):.1f},{y(f120(1) - s):.1f}" '
        f'fill="#1f5f8b" fill-opacity="0.08"/>')
    for decalage, style in ((s, ' stroke-dasharray="6 4"'), (-s, ' stroke-dasharray="6 4"'),
                            (0.0, "")):
        out.append(f'<line x1="{x(1):.1f}" y1="{y(f120(1) + decalage):.1f}" '
                   f'x2="{x(n):.1f}" y2="{y(f120(n) + decalage):.1f}" stroke="#1f5f8b" '
                   f'stroke-width="1.3"{style}/>')
    for decalage, style in ((ev["ENV_HAUT"], ' stroke-dasharray="4 3"'),
                            (-ev["ENV_BAS"], ' stroke-dasharray="4 3"'), (0.0, "")):
        out.append(f'<line x1="{x(debut_20):.1f}" y1="{y(f20(debut_20) + decalage):.1f}" '
                   f'x2="{x(n):.1f}" y2="{y(f20(n) + decalage):.1f}" stroke="#b35c1e" '
                   f'stroke-width="1.5"{style}/>')
    trace = " ".join(f"{x(t):.1f},{y(v):.1f}" for t, v in enumerate(closes, start=1))
    out.append(f'<polyline points="{trace}" fill="none" stroke="#333333" stroke-width="1.3"/>')
    for indice in (ev["ENV_I_BAS"], ev["ENV_I_HAUT"]):
        t = debut_20 + indice - 1
        out.append(f'<circle cx="{x(t):.1f}" cy="{y(closes[t - 1]):.1f}" r="4.5" '
                   f'fill="none" stroke="#b35c1e" stroke-width="1.5"/>')
    out.append(f'<circle cx="{x(n):.1f}" cy="{y(closes[-1]):.1f}" r="4" '
               f'fill="{couleur_point}"/>')
    out.append(f'<text x="{marge_g}" y="{hauteur - 34}" font-size="10.5" fill="#666666">'
               f'{jours[0]}</text>')
    out.append(f'<text x="{largeur - marge_d}" y="{hauteur - 34}" font-size="10.5" '
               f'fill="#666666" text-anchor="end">{jours[-1]}</text>')
    out.append(
        f'<text x="{marge_g}" y="{hauteur - 12}" font-size="10.5" fill="#444444">'
        f'<tspan fill="#333333">&#9472;</tspan> cl&#244;tures &#183; '
        f'<tspan fill="#1f5f8b">&#9472;</tspan> droite sur {LONGUE} s&#233;ances et bande '
        f'&#177; {fr(K, 1)} s &#183; <tspan fill="#b35c1e">&#9472;</tspan> droite sur '
        f'{COURTE} s&#233;ances et enveloppe des r&#233;sidus, les deux cl&#244;tures qui la '
        f'fixent cercl&#233;es</text>')
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")


def fins_de_mois(seances):
    """{AAAA-MM: derniere seance du mois}."""
    fins = {}
    for jour in seances:
        fins[jour[:7]] = jour
    return fins


def ecrire_figures(ctx, b):
    """Chaque valeur de l'univers en fin de mois, et chaque ordre a sa decision."""
    a_ecrire = set()
    for fin in fins_de_mois(b["seances"]).values():
        a_ecrire.update((ticker, fin) for ticker in ctx["univers"][fin])
    a_ecrire.update((o["TICKER"], o["DATE_DECISION"]) for o in b["ordres"])
    ecrites = 0
    for ticker, jour in sorted(a_ecrire):
        if ctx["evaluations"][jour][ticker]["MUETTE"]:
            continue
        figure_canal(chemin_figure(ctx["args"].repertoire, ticker, jour), ctx, ticker, jour)
        ecrites += 1
    return ecrites


def svg_portefeuille(chemin, dates, courbes, executions, debut):
    """Courbes en base 100 : [(libelle, valeurs, couleur, pointilles)]. Aucune bibliotheque."""
    largeur, hauteur = 900, 420
    marge_g, marge_d, marge_h, marge_b = 62, 18, 46, 62
    aire_l, aire_h = largeur - marge_g - marge_d, hauteur - marge_h - marge_b
    tout = [v for _l, serie, _c, _p in courbes for v in serie]
    bas, haut = min(tout), max(tout)
    coussin = (haut - bas) * 0.08 or 1.0
    bas, haut = bas - coussin, haut + coussin

    def x(i):
        return marge_g + aire_l * i / max(len(dates) - 1, 1)

    def y(v):
        return marge_h + aire_h * (haut - v) / (haut - bas)

    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{marge_g}" y="24" font-size="15" font-weight="600" fill="#1a1a1a">'
         f'Experience 6 &#8212; portefeuille contre {REFERENCE}, base 100 au {debut}</text>'),
        (f'<text x="{marge_g}" y="40" font-size="11" fill="#666666">{dates[0]} &#8594; '
         f'{dates[-1]} &#183; {len(dates)} seances &#183; traits verticaux : les seances '
         f'd\'execution</text>'),
    ]
    pas = pas_lisible(haut - bas, 8)
    niveau = math.ceil(bas / pas) * pas
    while niveau <= haut:
        gras = abs(niveau - 100) < 1e-9
        out.append(f'<line x1="{marge_g}" y1="{y(niveau):.1f}" x2="{largeur - marge_d}" '
                   f'y2="{y(niveau):.1f}" stroke="{"#c0c0c0" if gras else "#ececec"}" '
                   f'stroke-width="1"/>')
        out.append(f'<text x="{marge_g - 8}" y="{y(niveau) + 4:.1f}" font-size="10.5" '
                   f'fill="#666666" text-anchor="end">{fr(niveau, 0)}</text>')
        niveau += pas
    index = {jour: i for i, jour in enumerate(dates)}
    for jour in sorted(set(executions)):
        if jour in index:
            out.append(f'<line x1="{x(index[jour]):.1f}" y1="{marge_h}" '
                       f'x2="{x(index[jour]):.1f}" y2="{marge_h + aire_h}" stroke="#ded5c4" '
                       f'stroke-width="1" stroke-dasharray="2 3"/>')
    for rang, (libelle, serie, couleur, pointilles) in enumerate(reversed(courbes)):
        trace = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(serie))
        tirets = ' stroke-dasharray="5 4"' if pointilles else ""
        out.append(f'<polyline points="{trace}" fill="none" stroke="{couleur}" '
                   f'stroke-width="1.8"{tirets}/>')
        gauche = marge_g + rang * 230
        out.append(f'<line x1="{gauche}" y1="{hauteur - 18}" x2="{gauche + 24}" '
                   f'y2="{hauteur - 18}" stroke="{couleur}" stroke-width="1.8"{tirets}/>'
                   f'<text x="{gauche + 30}" y="{hauteur - 14}" font-size="10.5" '
                   f'fill="#444444">{libelle} {fr(serie[-1], 1)}</text>')
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Phase 8 : les journaux mensuels


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
    actualites = decouper((repertoire / "actualites.md").read_text(encoding="utf-8"), "## ")
    brut = decouper((repertoire / "chartiste.md").read_text(encoding="utf-8"), "## ")
    return actualites, {date: decouper(corps, "### ") for date, corps in brut.items()}


def note_en_liste(note):
    lignes = [ligne.strip() for ligne in note.split(NL_) if ligne.strip()]
    return NL_.join(ligne if ligne.startswith("- ") else f"- {ligne}" for ligne in lignes)


def fiche(ctx, ticker, jour):
    """La ligne calculee qui accompagne chaque figure : aucun mot ecrit a la main."""
    ev = ctx["evaluations"][jour][ticker]
    rang = ctx["rangs"][jour].get(ticker)
    return (f"> {f'Rang {rang}' if rang else 'Hors classement'} · TAUX_120 "
            f"{signe(ev['TAUX_120'], 3)} %/séance · clôture {fr(ev['CLOSE'])} {EURO} · "
            f"bande {fr(bord_bas(ev))} – {fr(bord_haut(ev))} {EURO} · écart "
            f"{signe(ev['ECART_S'])} s · TAUX_20 {signe(ev['TAUX_20'], 3)} %/séance · "
            f"enveloppe 20 : {fr(ev['LARGEUR_ENV_S'])} s, "
            f"{fr(100 * (ev['ENV_BAS'] + ev['ENV_HAUT']) / ev['E_20'], 1)} % · "
            f"**{verdict_du_jour(ctx, ticker, jour)}**")


def image(ctx, ticker, jour, legende):
    chemin = chemin_figure(ctx["args"].repertoire, ticker, jour)
    if not chemin.exists():
        return FIGURE_ABSENTE
    return f"![{legende}](../{GRAPHIQUES}/{ticker}/canal-{ticker}-{jour}.svg)"


def index_ordres(ordres):
    return {(o["TICKER"], o["DATE"], o["SENS"]): o for o in ordres}


def tenues_a(b, jour):
    """Les positions detenues a la cloture de `jour`."""
    return [p for p in b["positions"]
            if p["achat"] <= jour and (p["vente"] is None or p["vente"] > jour)]


def tableau_exposition(ctx, b, veille):
    tenues = tenues_a(b, veille) if veille else []
    if not tenues:
        return "*Aucune ligne : le portefeuille est intégralement en espèces.*"
    ref = ctx["reference"]["par_jour"]
    out = ["| Valeur | Achetée le | Prix d'achat | Cours | +/− value | Alpha depuis l'achat |",
           "|---|---|---|---|---|---|"]
    for p in tenues:
        cours = ctx["series"][p["ticker"]]["par_jour"][veille]["close"]
        alpha = 100 * (cours / p["prix_achat"]
                       - ref[veille]["close"] / ref[p["achat"]]["close"])
        out.append(
            f"| `{p['ticker']}` {SOCIETES[p['ticker']]} | {p['achat']} "
            f"| {fr(p['prix_achat'])} {EURO} | {fr(cours)} {EURO} "
            f"| **{signe(100 * (cours / p['prix_achat'] - 1))} %** | {signe(alpha)} pt |")
    return NL_.join(out)


def tableau_positions(b, fin_mois):
    """Toutes les positions depuis le debut, closes comme ouvertes, rien apres le mois."""
    lignes = [p for p in b["positions"] if p["achat"] <= fin_mois]
    if not lignes:
        return "*Aucune position prise depuis le début de l'expérience.*"
    out = ["| Société | Prix d'achat | Date d'achat | Prix de vente | Date de vente |",
           "|---|---|---|---|---|"]
    ouvertes = 0
    for p in lignes:
        vendue = p["vente"] is not None and p["vente"] <= fin_mois
        ouvertes += not vendue
        out.append(f"| `{p['ticker']}` {SOCIETES[p['ticker']]} | {fr(p['prix_achat'])} {EURO} "
                   f"| {p['achat']} | {fr(p['prix_vente']) + ' ' + EURO if vendue else ''} "
                   f"| {p['vente'] if vendue else ''} |")
    out += ["", (f"*{len(lignes)} position{'s' if len(lignes) > 1 else ''} depuis le début, "
                 f"dont {ouvertes} encore ouverte{'s' if ouvertes > 1 else ''} : les deux "
                 "dernières colonnes restent vides.*")]
    return NL_.join(out)


def etude_chartiste(ctx, b, mois, fin_mois, notes):
    evaluations, rangs = ctx["evaluations"][fin_mois], ctx["rangs"][fin_mois]
    univers = ctx["univers"][fin_mois]
    classes = sorted((t for t in univers if t in rangs), key=rangs.get)
    autres = sorted((t for t in univers if t not in rangs and not evaluations[t]["MUETTE"]),
                    key=lambda t: -evaluations[t]["TAUX_120"])
    muettes = sorted(t for t in univers if evaluations[t]["MUETTE"])
    out = []
    for ticker in [*classes, *autres, *muettes]:
        rang = rangs.get(ticker)
        titre = f"{rang}. `{ticker}`" if rang else f"`{ticker}`"
        out += [f"### {titre} — {SOCIETES[ticker]}", ""]
        if evaluations[ticker]["MUETTE"]:
            out += [FIGURE_ABSENTE, "",
                    f"> Évaluation muette : {evaluations[ticker]['DIAGNOSTIC']}.", ""]
        else:
            out += [image(ctx, ticker, fin_mois, f"Canal de {ticker} au {fin_mois}"), "",
                    fiche(ctx, ticker, fin_mois), ""]
        out += [note_en_liste(notes.get(ticker, "")) or ABSENTE, ""]
    ordres = [o for o in b["ordres"] if o["DATE"][:7] == mois]
    out += ["### Les figures des ordres du mois", ""]
    if not ordres:
        out += ["*Aucun ordre ce mois-ci.*", ""]
    for o in ordres:
        out += [(f"#### {o['DATE']} — {o['SENS'].capitalize()} `{o['TICKER']}` "
                 f"{SOCIETES[o['TICKER']]}, décision au {o['DATE_DECISION']}"), "",
                image(ctx, o["TICKER"], o["DATE_DECISION"],
                      f"Canal de {o['TICKER']} au {o['DATE_DECISION']}"), "",
                fiche(ctx, o["TICKER"], o["DATE_DECISION"]), ""]
    return out


def top_du_mois(ctx, mois, fin_mois):
    rangs = ctx["rangs"][fin_mois]
    top = sorted((t for t, r in rangs.items() if r <= TOP), key=rangs.get)
    out = ["| Rang | Valeur | TAUX_120 | Écart | TAUX_20 | Verdict |", "|---|---|---|---|---|---|"]
    for ticker in top:
        ev = ctx["evaluations"][fin_mois][ticker]
        out.append(f"| {rangs[ticker]} | `{ticker}` {SOCIETES[ticker]} "
                   f"| {signe(ev['TAUX_120'], 3)} %/séance | {signe(ev['ECART_S'])} s "
                   f"| {signe(ev['TAUX_20'], 3)} %/séance "
                   f"| {verdict_du_jour(ctx, ticker, fin_mois)} |")
    if len(top) < TOP:
        out += ["", (f"*Le TOP ne compte que {len(top)} valeurs : moins de {TOP} pentes "
                     "sont strictement positives ce jour-là.*")]
    jours = ctx["jours_evalues"]
    mouvements = []
    for i, jour in enumerate(jours):
        if jour[:7] != mois or i == 0:
            continue
        avant = {t for t, r in ctx["rangs"][jours[i - 1]].items() if r <= TOP}
        apres = {t for t, r in ctx["rangs"][jour].items() if r <= TOP}
        if avant != apres:
            entrees = ", ".join(f"`{t}`" for t in sorted(apres - avant)) or "—"
            sorties = ", ".join(f"`{t}`" for t in sorted(avant - apres)) or "—"
            mouvements.append(f"| {jour} | {entrees} | {sorties} |")
    out += ["", "**Entrées et sorties du TOP 10 au fil du mois**", ""]
    out += (["| Séance | Entrées | Sorties |", "|---|---|---|", *mouvements] if mouvements
            else ["*Aucune : le TOP 10 est resté le même à chaque séance du mois.*"])
    return out


def tableau_ordres(b, mois):
    ordres = [o for o in b["ordres"] if o["DATE"][:7] == mois]
    if not ordres:
        return "*Aucun ordre : aucune valeur n'a franchi un bord de sa bande.*"
    out = [("| Exécution | Sens | Valeur | Quantité | Prix | Brut | Frais "
            "| Écart d'ouverture | Motif |"), "|---|---|---|---|---|---|---|---|---|"]
    for o in ordres:
        out.append(f"| {o['DATE']} | **{o['SENS'].capitalize()}** | `{o['TICKER']}` "
                   f"{SOCIETES[o['TICKER']]} | {o['QUANTITE']} | {fr(o['PRIX'])} {EURO} "
                   f"| {fr(o['BRUT'])} {EURO} | {fr(o['FRAIS'])} {EURO} "
                   f"| {signe(o['ECART_OUVERTURE'])} % "
                   f"| décision au {o['DATE_DECISION']} : {o['MOTIF']} |")
    return NL_.join(out)


def decisions_du_mois(b, mois):
    return {d for d, etape in b["journal"].items() if etape["execution"][:7] == mois}


def tableau_signaux(b, mois):
    decisions = decisions_du_mois(b, mois)
    perdus = [s for s in b["signaux"] if s["DATE_DECISION"] in decisions
              and s["SORT"] != "EXECUTE"]
    if not perdus:
        return "*Aucun : chaque candidat du mois a été acheté.*"
    out = ["| Décision | Valeur | Rang | Écart | TAUX_20 | Sort |", "|---|---|---|---|---|---|"]
    for s in perdus:
        out.append(f"| {s['DATE_DECISION']} | `{s['TICKER']}` {SOCIETES[s['TICKER']]} "
                   f"| {s['RANG']} | {signe(s['ECART_S'])} s | {signe(s['TAUX_20'], 3)} %/séance "
                   f"| {s['SORT']} |")
    return NL_.join(out)


def contributions(ctx, b, veille, fin_mois):
    """Contribution en euros de chaque position sur le mois, lignes vendues comprises."""
    index = index_ordres(b["ordres"])
    apports = []
    for p in b["positions"]:
        if p["achat"] > fin_mois or (p["vente"] is not None and veille and p["vente"] <= veille):
            continue
        serie = ctx["series"][p["ticker"]]["par_jour"]
        if veille and p["achat"] <= veille:
            depart, frais = serie[veille]["close"], 0.0
        else:
            depart, frais = p["prix_achat"], index[(p["ticker"], p["achat"], "ACHAT")]["FRAIS"]
        if p["vente"] is not None and p["vente"] <= fin_mois:
            arrivee = p["prix_vente"]
            frais += index[(p["ticker"], p["vente"], "VENTE")]["FRAIS"]
        else:
            arrivee = serie[fin_mois]["close"]
        apports.append((p["ticker"], p["quantite"] * (arrivee - depart) - frais))
    return apports


def lecture_du_mois(ctx, b, mois, veille, fin_mois, alpha_mois):
    """Un paragraphe entierement calcule : aucun recit ecrit apres coup."""
    phrases = []
    apports = sorted(contributions(ctx, b, veille, fin_mois), key=lambda a: a[1])
    if apports:
        (bas_t, bas_e), (haut_t, haut_e) = apports[0], apports[-1]
        phrases.append(f"Sur le mois, la meilleure contribution vient de `{haut_t}` "
                       f"({SOCIETES[haut_t]}) pour **{signe(haut_e)} {EURO}**, la moins bonne "
                       f"de `{bas_t}` ({SOCIETES[bas_t]}) pour **{signe(bas_e)} {EURO}**.")
    else:
        phrases.append("Aucune ligne détenue sur le mois.")
    ordres = [o for o in b["ordres"] if o["DATE"][:7] == mois]
    if ordres:
        frais = sum(o["FRAIS"] for o in ordres)
        phrases.append(f"Les {len(ordres)} ordres du mois ont coûté **{fr(frais)} {EURO}** "
                       f"de frais, soit {fr(100 * frais / b['dotation'], 3)} % de la dotation.")
    else:
        phrases.append("Aucun ordre, donc aucun frais.")
    cote = "devant" if alpha_mois >= 0 else "derrière"
    phrases.append(f"Le portefeuille termine le mois **{cote} {REFERENCE}** de "
                   f"{fr(abs(alpha_mois))} point.")
    decisions = decisions_du_mois(b, mois)
    pleins = {s["DATE_DECISION"] for s in b["signaux"]
              if s["DATE_DECISION"] in decisions and s["SORT"] == "FAUTE DE CRENEAU"}
    if pleins:
        phrases.append(f"Sur {len(pleins)} séance{'s' if len(pleins) > 1 else ''} de décision, "
                       "un candidat n'a pas pu être acheté faute de créneau.")
    return " ".join(phrases)


def ecrire_rapports(ctx, b, textes):
    """Ecrit les douze journaux mensuels et leurs courbes."""
    actualites, notes = textes
    rep, seances = ctx["args"].repertoire, b["seances"]
    fins = fins_de_mois(seances)
    liste = sorted(fins)
    executions = [o["DATE"] for o in b["ordres"]]
    for rang, mois in enumerate(liste):
        fin_mois = fins[mois]
        veille = fins.get(mois_precedent(mois))
        jours = [j for j in seances if j <= fin_mois]
        base = [100 * b["valeurs"][j][2] / b["dotation"] for j in jours]
        svg_portefeuille(rep / GRAPHIQUES / f"portefeuille-{mois}.svg", jours, [
            ("portefeuille", base, "#1f5f8b", False),
            ("règle 4 (L5-P1)",
             [100 * b["combinaisons"]["L5-P1"]["valeurs"][j][2] / b["dotation"] for j in jours],
             "#8e6bb8", False),
            ("référence appariée", [b["appariee_par_jour"][j] for j in jours],
             "#c0782c", True),
            (REFERENCE, [b["ref100"][j] for j in jours], "#9aa5b1", True)],
            executions, b["debut"])
        base_p = b["valeurs"][veille][2] if veille else b["dotation"]
        base_r = b["ref100"][veille] if veille else 100.0
        total = b["valeurs"][fin_mois][2]
        alpha_mois = 100 * (total / base_p - b["ref100"][fin_mois] / base_r)
        alpha_global = base[-1] - b["ref100"][fin_mois]
        navigation = []
        if rang > 0:
            navigation.append(f"[← {MOIS_TITRE[liste[rang - 1][5:7]]}]({liste[rang - 1]}.md)")
        navigation.append("[Protocole](../README.md)")
        if rang + 1 < len(liste):
            navigation.append(f"[{MOIS_TITRE[liste[rang + 1][5:7]]} →]({liste[rang + 1]}.md)")
        ordres = [o for o in b["ordres"] if o["DATE"][:7] == mois]
        premiere = jours_du(seances, mois)[0]
        base_app = b["appariee_par_jour"][fin_mois]
        base_4 = 100 * b["combinaisons"]["L5-P1"]["valeurs"][fin_mois][2] / b["dotation"]
        bloc = [
            f"# {MOIS_TITRE[mois[5:7]]} {ANNEE}", "",
            (f"> Journal de l'[expérience 6](../README.md) · exécutions du {premiere} "
             f"au {fin_mois} · **{len(ordres)} ordre{'s' if len(ordres) > 1 else ''}**"),
            (f"> Portefeuille au {fin_mois} : **{fr(total)} {EURO}** (base {fr(base[-1])}) · "
             f"{REFERENCE} {fr(b['ref100'][fin_mois])} · alpha du mois **{signe(alpha_mois)} pt**"
             f" · depuis janvier **{signe(alpha_global)} pt**"),
            "", "---", "",
            "## 1. Les actualités du mois précédent", "", actualites.get(mois) or ABSENTE, "",
            (f"## 2. L'exposition héritée au {veille}" if veille
             else "## 2. L'exposition héritée"), "",
            tableau_exposition(ctx, b, veille), "",
            f"## 3. Le portefeuille depuis le {b['debut']}", "",
            f"![Évolution du portefeuille au {fin_mois}](../{GRAPHIQUES}/portefeuille-{mois}.svg)",
            "", "| | |", "|---|---|",
            f"| Dotation initiale | {fr(b['dotation'])} {EURO} au {b['debut']} |",
            f"| Titres au {fin_mois} | {fr(b['valeurs'][fin_mois][1])} {EURO} |",
            f"| Espèces | {fr(b['valeurs'][fin_mois][0])} {EURO} |",
            f"| Lignes détenues | {b['valeurs'][fin_mois][3]} |",
            f"| **Total** | **{fr(total)} {EURO}** |",
            f"| Base 100 | **{fr(base[-1])}** |",
            f"| Référence à exposition appariée, même base | {fr(base_app)} |",
            f"| **Alpha officiel depuis janvier** | **{signe(base[-1] - base_app)} pt** |",
            f"| Règle de l'expérience 4 (`L5-P1`), même base | {fr(base_4)} |",
            f"| {REFERENCE}, même base | {fr(b['ref100'][fin_mois])} |",
            f"| Écart depuis janvier | **{signe(alpha_global)} pt** |",
            "", "### Toutes les positions depuis le début de l'expérience", "",
            (f"> Closes comme ouvertes. Aucune séance postérieure au {fin_mois} n'entre dans "
             "ce tableau."), "",
            tableau_positions(b, fin_mois), "",
            f"## 4. L'étude chartiste au {fin_mois}", "",
            (f"> Une entrée par société de l'univers, sous la figure de canal lue à la clôture "
             f"du {fin_mois}. La ligne en retrait est **calculée** ; la note qui suit est "
             "celle de l'agent `chartiste`, rédigée sans aucune séance postérieure."), "",
            *etude_chartiste(ctx, b, mois, fin_mois, notes.get(fin_mois, {})),
            f"## 5. Le TOP 10 au {fin_mois}", "",
            *top_du_mois(ctx, mois, fin_mois), "",
            "## 6. Les ordres exécutés", "",
            ("> À l'**ouverture** de la séance qui suit la décision, jamais à la clôture qui "
             "l'a déclenchée. L'écart d'ouverture est subi, et publié."), "",
            tableau_ordres(b, mois), "",
            "## 7. Les signaux non exécutés", "",
            tableau_signaux(b, mois), "",
            "## 8. La lecture du mois", "",
            lecture_du_mois(ctx, b, mois, veille, fin_mois, alpha_mois), "",
        ]
        if rang + 1 == len(liste):
            bloc += ["---", "", ("L'expérience s'arrête ici. Le compte de l'année, les issues "
                                 f"et le dimensionnement confronté sont dans le **[bilan]"
                                 f"(../{BILAN})**."), ""]
        bloc += ["---", "", " · ".join(navigation)]
        ecrire_texte(rep / RAPPORTS / f"{mois}.md", NL_.join(bloc) + NL_)


def jours_du(seances, mois):
    return [j for j in seances if j[:7] == mois]




# --------------------------------------------------------------------------
# Les pistes de la revue : T1, C1, T2, T3, T4

_OUTILS = {}


def p_bilaterale(t, ddl):
    """p-valeur bilaterale de Student, par p_valeur_student() de import_societe.py."""
    if "student" not in _OUTILS:
        sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "python"))
        from import_societe import p_valeur_student  # noqa: PLC0415 - le depot n'est pas un paquet
        _OUTILS["student"] = p_valeur_student
    return _OUTILS["student"](t, ddl)


def quantile_student(ddl):
    """Le t dont la p-valeur bilaterale vaut 0,05, par dichotomie sur 80 iterations."""
    cle = ("quantile", ddl)
    if cle not in _OUTILS:
        bas, haut = 0.0, 100.0
        for _ in range(80):
            milieu = (bas + haut) / 2
            if p_bilaterale(milieu, ddl) > 0.05:
                bas = milieu
            else:
                haut = milieu
        _OUTILS[cle] = (bas + haut) / 2
    return _OUTILS[cle]


def decisions_mensuelles(ctx, jours):
    """La derniere seance de chaque mois dont l'execution tombe le mois suivant."""
    retenues = [d for d in jours if ctx["execution"][d][:7] != d[:7]]
    if len(retenues) != 12:
        erreur(f"{len(retenues)} decisions mensuelles au lieu de 12, de {jours[0]} a {jours[-1]}")
    return retenues


# --- T1 : grappes de dates, phases, Holm, verdict


def grappes(lignes, population, groupe):
    """Difference des moyennes d'EXCES_20, erreur type par grappes de dates."""
    retenues = [li for li in lignes if population(li)]
    a = [li for li in retenues if groupe(li) and li["EXCES_20"] is not None]
    b = [li for li in retenues if not groupe(li) and li["EXCES_20"] is not None]
    ya, yb = [li["EXCES_20"] for li in a], [li["EXCES_20"] for li in b]
    r = {"na": len(a), "nb": len(b),
         "moy_a": statistics.fmean(ya) if ya else None,
         "moy_b": statistics.fmean(yb) if yb else None,
         "difference": None, "se": None, "G": len({li["DATE"] for li in a + b}),
         "ddl": None, "ic": None, "p": None, "ic_welch": None,
         "non_tranchees": sum(1 for li in retenues if li["EXCES_20"] is None)}
    if len(a) < 2 or len(b) < 2:
        return r
    r["difference"] = r["moy_a"] - r["moy_b"]
    r["ic_welch"] = Z95 * math.sqrt(statistics.variance(ya) / len(ya)
                                    + statistics.variance(yb) / len(yb))
    if r["G"] < DATES_MIN:
        return r
    u = {}
    for li in a:
        u[li["DATE"]] = u.get(li["DATE"], 0.0) + (li["EXCES_20"] - r["moy_a"]) / len(a)
    for li in b:
        u[li["DATE"]] = u.get(li["DATE"], 0.0) - (li["EXCES_20"] - r["moy_b"]) / len(b)
    g = len(u)
    se = math.sqrt(g / (g - 1) * sum(v * v for v in u.values()))
    p = (p_bilaterale(r["difference"] / se, g - 1) if se > 0
         else (0.0 if r["difference"] else 1.0))
    r.update({"se": se, "ddl": g - 1, "ic": quantile_student(g - 1) * se, "p": p})
    return r


def exclut_zero(c, signe_reference):
    return (c["ic"] is not None and signe_reference != 0 and abs(c["difference"]) > c["ic"]
            and (c["difference"] > 0) == (signe_reference > 0))


def phases(lignes):
    """Les quatre comparaisons sur les vingt phases du sous-echantillon."""
    par_phase = {k: [li for li in lignes if li["PHASE"] == k] for k in range(PHASES)}
    resultat = {}
    for cle, *_r, population, groupe in COMPARAISONS:
        serie = [grappes(par_phase[k], population, groupe) for k in range(PHASES)]
        reference = serie[0]["difference"]
        signe_reference = 0 if not reference else (1 if reference > 0 else -1)
        exclut = [exclut_zero(c, signe_reference) for c in serie]
        differences = [c["difference"] for c in serie if c["difference"] is not None]
        resultat[cle] = {"phases": serie, "exclut": exclut, "n_exclut": sum(exclut),
                         "min": min(differences, default=None),
                         "max": max(differences, default=None)}
    return resultat


def holm(p_valeurs):
    """Rejets de Holm au risque RISQUE ; une p-valeur absente sort de la famille."""
    mesurables = sorted((p, cle) for cle, p in p_valeurs.items() if p is not None)
    rejet = dict.fromkeys(p_valeurs, False)
    m = len(mesurables)
    for j, (p, cle) in enumerate(mesurables, start=1):
        if p > RISQUE / (m - j + 1):
            break
        rejet[cle] = True
    return rejet


def verdict_t1(resultat, rejete):
    if resultat["phases"][0]["ic"] is None:
        return "non mesurable"
    return "sépare" if rejete and resultat["n_exclut"] >= SEUIL_PHASES else "ne sépare pas"


def verdict_experience_4(c):
    """Le verdict qu'imprimait l'experience 4 : l'intervalle de Welch de la phase 0."""
    if c["difference"] is None or c["ic_welch"] is None:
        return "non mesurable"
    return "exclut zéro" if abs(c["difference"]) > c["ic_welch"] else "contient zéro"


def proportion_grappes(lignes, valeur):
    """Proportion et IC95 par grappes de dates ; `valeur` rend True, False ou None."""
    tranchees = [(li["DATE"], valeur(li)) for li in lignes if valeur(li) is not None]
    total = len(tranchees)
    vrais = sum(1 for _d, x in tranchees if x)
    r = {"n": vrais, "total": total, "taux": 100 * vrais / total if total else None,
         "ic": None, "G": 0}
    if not total:
        return r
    p = vrais / total
    u = {}
    for date, x in tranchees:
        u[date] = u.get(date, 0.0) + ((1.0 if x else 0.0) - p) / total
    r["G"] = len(u)
    if r["G"] >= DATES_MIN:
        r["ic"] = 100 * quantile_student(r["G"] - 1) * math.sqrt(
            r["G"] / (r["G"] - 1) * sum(v * v for v in u.values()))
    return r


# --- C2, fusionnee dans T1 : episodes, sejours, duree d'episode a l'achat


def episodes(ctx, predicat):
    """(episodes, places, places du sous-echantillon, episodes touchant le sous-echantillon)."""
    nombre = places = places_ech = episodes_ech = 0
    for ticker in ctx["tickers"]:
        en_cours = touche = False
        for jour in ctx["jours_audit"]:
            vrai = ticker in ctx["univers"][jour] and predicat(ticker, jour)
            if vrai:
                places += 1
                if not en_cours:
                    nombre += 1
                    touche = False
                if ctx["phase"][jour] == 0:
                    places_ech += 1
                    if not touche:
                        episodes_ech += 1
                        touche = True
            en_cours = vrai
    return nombre, places, places_ech, episodes_ech


def duree_a_l_achat(ctx, o):
    """(seances consecutives sous le bord bas, seances consecutives candidate), decision incluse."""
    jours = ctx["jours_evalues"]
    fin = jours.index(o["DATE_DECISION"])
    ticker = o["TICKER"]
    sous = seances_candidat = 0
    suite_sous = suite_candidat = True
    for jour in reversed(jours[:fin + 1]):
        ev = ctx["evaluations"][jour][ticker]
        if suite_sous:
            if not ev["MUETTE"] and ev["ECART_S"] < -K:
                sous += 1
            else:
                suite_sous = False
        if suite_candidat:
            if ticker in ctx["univers"][jour] and candidat(ctx, ticker, jour):
                seances_candidat += 1
            else:
                suite_candidat = False
        if not (suite_sous or suite_candidat):
            break
    return sous, seances_candidat


# --- C1 : les references simulees de la bande


def normales(graine):
    """Generateur congruentiel du module 2 et Box-Muller par paires."""
    x = graine
    while True:
        x = (1664525 * x + 1013904223) % 2**32
        u1 = (x + 0.5) / 2**32
        x = (1664525 * x + 1013904223) % 2**32
        u2 = (x + 0.5) / 2**32
        rayon = math.sqrt(-2 * math.log(u1))
        yield rayon * math.cos(2 * math.pi * u2)
        yield rayon * math.sin(2 * math.pi * u2)


def uniformes(graine):
    x = graine
    while True:
        x = (1664525 * x + 1013904223) % 2**32
        yield (x + 0.5) / 2**32


def etat(ecart):
    """0 sous le bord bas, 1 dans la bande, 2 au-dessus du bord haut."""
    return 0 if ecart < -K else (2 if ecart > K else 1)


def reference_bande(marche, graine):
    """Matrice 3 x 3 des etats, sur TIRAGES_REFERENCE tirages de 121 valeurs."""
    tirage = normales(graine)
    n, mt = LONGUE, (LONGUE + 1) / 2
    vt = variance_temps(LONGUE)
    matrice = [[0] * 3 for _ in range(3)]
    for _ in range(TIRAGES_REFERENCE):
        z = [next(tirage) for _ in range(n + 1)]
        if marche:
            valeurs, cumul = [], 0.0
            for x in z:
                cumul += x
                valeurs.append(cumul)
        else:
            valeurs = z
        moyenne = sum(valeurs[:n]) / n
        pente = sum((i + 1 - mt) * (valeurs[i] - moyenne) for i in range(n)) / n / vt
        residuelle = sum((valeurs[i] - moyenne - pente * (i + 1 - mt)) ** 2
                         for i in range(n)) / n
        s = math.sqrt(n / (n - 2) * residuelle)
        centre = moyenne + pente * (n - mt)
        matrice[etat((valeurs[n - 1] - centre) / s)][etat((valeurs[n] - centre - pente) / s)] += 1
    return matrice


def matrice_bande(ctx, jours, borne):
    """La matrice observee : etat a la decision, etat de la cloture suivante."""
    calendrier, rang = ctx["reference"]["jours"], ctx["reference"]["rang"]
    matrice = [[0] * 3 for _ in range(3)]
    for jour in jours:
        i = rang[jour]
        if i + 1 >= len(calendrier) or calendrier[i + 1] > borne:
            continue
        suivante = calendrier[i + 1]
        for ticker in ctx["univers"][jour]:
            ev = ctx["evaluations"][jour][ticker]
            serie = ctx["series"][ticker]["par_jour"]
            if ev["MUETTE"] or suivante not in serie:
                continue
            ecart = (serie[suivante]["close"] - ev["VAL_120"] - ev["R_120"]) / ev["S_120"]
            matrice[etat(ev["ECART_S"])][etat(ecart)] += 1
    return matrice


def lire_matrice(matrice):
    effectifs = [sum(ligne) for ligne in matrice]
    total = sum(effectifs)
    return {
        "total": total, "effectifs": effectifs,
        "sous": 100 * effectifs[0] / total, "dans": 100 * effectifs[1] / total,
        "dessus": 100 * effectifs[2] / total,
        "bande": 100 * sum(ligne[1] for ligne in matrice) / total,
        "lignes": [[100 * x / effectifs[i] if effectifs[i] else None for x in ligne]
                   for i, ligne in enumerate(matrice)],
    }


# --- T4 et T3 : resumes de simulation et ecarts apparies


def resumer(ctx, simulation, seances):
    ordres, signaux, valeurs, _journal, registre = simulation
    ref = ctx["reference"]["par_jour"]
    base = [100 * valeurs[j][2] / DOTATION for j in seances]
    indice = [100 * ref[j]["close"] / ref[seances[0]]["close"] for j in seances]
    reg = regression(base, indice)
    part, vides = exposition(valeurs, seances)
    positions = positions_annee(ctx, registre, seances[-1])
    closes = [p["seances"] for p in positions if not p["ouverte"]]
    return {
        "seances": seances, "base": base, "indice": indice, "valeurs": valeurs,
        "ordres": ordres, "signaux": signaux, "positions": positions, "regression": reg,
        "te": ecart_type_ecarts(base, indice), "beta": reg["beta"], "part": part,
        "vides": vides, "n_ordres": len(ordres), "frais": sum(o["FRAIS"] for o in ordres),
        "duree": statistics.median(closes) if closes else None,
        "ouvertes": sum(1 for p in positions if p["ouverte"]),
        "perdus": sum(1 for s in signaux if s["SORT"] == "FAUTE DE CRENEAU"),
    }


def ecart_apparie(a, b, indice=None):
    """Ecart-type annualise de la difference ; avec `indice`, son beta et son residu."""
    ra = [a[i] / a[i - 1] - 1 for i in range(1, len(a))]
    rb = [b[i] / b[i - 1] - 1 for i in range(1, len(b))]
    difference = [x - y for x, y in zip(ra, rb, strict=True)]
    r = {"te": statistics.stdev(difference) * math.sqrt(252) * 100}
    if indice is None:
        return r
    rm = [indice[i] / indice[i - 1] - 1 for i in range(1, len(indice))]
    mm, md = statistics.fmean(rm), statistics.fmean(difference)
    beta = (sum((rm[i] - mm) * (difference[i] - md) for i in range(len(rm)))
            / sum((x - mm) ** 2 for x in rm))
    alpha_jour = md - beta * mm
    residus = [difference[i] - alpha_jour - beta * rm[i] for i in range(len(rm))]
    sigma = statistics.stdev(residus)
    r.update({"beta": beta, "te_residu": sigma * math.sqrt(252) * 100,
              "alpha": 100 * alpha_jour * 252,
              "ic_alpha": 100 * Z95 * sigma / math.sqrt(len(residus)) * 252})
    return r


# --- T2 : exposition appariee, semestres, temoin aleatoire


def reference_appariee(ctx, valeurs, seances):
    """TR39 detenue dans la proportion ou le portefeuille etait investi la veille."""
    ref = ctx["reference"]["par_jour"]
    base = [100.0]
    for i in range(1, len(seances)):
        veille = valeurs[seances[i - 1]]
        rendement = ref[seances[i]]["close"] / ref[seances[i - 1]]["close"] - 1
        base.append(base[-1] * (1 + veille[1] / veille[2] * rendement))
    return base


def betas_semestres(base, indice, seances, borne):
    premier = [i for i, j in enumerate(seances) if j <= borne]
    second = list(range(premier[-1], len(seances)))
    return (regression([base[i] for i in premier], [indice[i] for i in premier])["beta"],
            regression([base[i] for i in second], [indice[i] for i in second])["beta"])


def gain_net(ctx, ticker, achat, vente, brut, fin):
    """Le gain net d'un montant brut investi a l'ouverture d'`achat`."""
    serie = ctx["series"][ticker]["par_jour"]
    rapport = (serie[vente]["open"] if vente else serie[fin]["close"]) / serie[achat]["open"]
    frais_vente = brut * rapport * taux_vente(ticker) if vente else 0.0
    return brut * (rapport - 1) - brut * taux_achat(ticker) - frais_vente


def temoin(ctx, positions, fin, valeur_finale, reservoir):
    """TIRAGES_TEMOIN portefeuilles aux memes dates et montants, valeurs tirees au hasard."""
    def brut(p):
        return p["quantite"] * p["prix_achat"]

    reel = DOTATION + sum(gain_net(ctx, p["ticker"], p["achat"], p["vente"], brut(p), fin)
                          for p in positions)
    if abs(reel - valeur_finale) > 0.01:
        erreur(f"Temoin : la formule rend {reel:.2f} EUR pour un portefeuille valant "
               f"{valeur_finale:.2f} EUR au {fin}")
    tirage = uniformes(GRAINE_TEMOIN)
    finaux = []
    for _ in range(TIRAGES_TEMOIN):
        tenues, total = [], DOTATION
        for p in positions:
            tenues = [(t, v) for t, v in tenues if v is None or v > p["achat"]]
            d = p["decision"]
            if reservoir == "UNIVERS":
                bassin = {t for t in ctx["univers"][d] if not ctx["evaluations"][d][t]["MUETTE"]}
            else:
                bassin = {t for t, r in ctx["rangs"][d].items() if r <= TOP}
            bassin = sorted(bassin - {t for t, _v in tenues})
            ticker = bassin[int(next(tirage) * len(bassin))] if bassin else p["ticker"]
            tenues.append((ticker, p["vente"]))
            total += gain_net(ctx, ticker, p["achat"], p["vente"], brut(p), fin)
        finaux.append(100 * total / DOTATION)
    base_reelle = 100 * reel / DOTATION
    moyenne, ecart = statistics.fmean(finaux), statistics.stdev(finaux)
    return {"reservoir": reservoir, "finaux": finaux, "moyenne": moyenne, "sd": ecart,
            "reel": base_reelle, "emd": Z95 * ecart,
            "rang": 100 * sum(1 for f in finaux if f < base_reelle) / len(finaux),
            "z": (base_reelle - moyenne) / ecart}


# --- Le controle de reproduction


def controler_reproduction(repertoire, ordres, valeurs):
    """Sort en 1 si le portefeuille differe de celui de l'experience 4."""
    dossier = repertoire.parent / "experience_4"
    for nom in ("ordres.csv", "portefeuille.csv"):
        if not (dossier / nom).exists():
            erreur(f"{dossier / nom} absent : le controle de reproduction ne se contourne pas")
    with (dossier / "ordres.csv").open(encoding="utf-8") as flux:
        publies = list(csv.DictReader(flux))
    if len(publies) != len(ordres):
        erreur(f"{len(ordres)} ordres contre {len(publies)} dans l'experience 4")
    for i, (publie, o) in enumerate(zip(publies, ordres, strict=True), start=1):
        attendu = (publie["DATE"], publie["DATE_DECISION"], publie["TICKER"], publie["SENS"],
                   int(publie["QUANTITE"]), round(float(publie["PRIX"]), 4))
        obtenu = (o["DATE"], o["DATE_DECISION"], o["TICKER"], o["SENS"], o["QUANTITE"],
                  round(o["PRIX"], 4))
        if attendu != obtenu:
            erreur(f"Ordre {i} different de l'experience 4 : {attendu} contre {obtenu}")
    with (dossier / "portefeuille.csv").open(encoding="utf-8") as flux:
        for publie in csv.DictReader(flux):
            jour = publie["DATE"]
            if jour not in valeurs or abs(valeurs[jour][2] - float(publie["TOTAL"])) > 0.005:
                erreur(f"Valorisation du {jour} differente de l'experience 4")
    fin = max(valeurs)
    if (len(ordres), round(valeurs[fin][2], 2)) != CONTROLE:
        erreur(f"Controle : {len(ordres)} ordres et {valeurs[fin][2]:.2f} EUR, "
               f"au lieu de {CONTROLE[0]} et {CONTROLE[1]:.2f}")
    return len(ordres), valeurs[fin][2]




# --------------------------------------------------------------------------
# Phase 8 bis : le bilan

# Les ecarts apparies qui isolent chaque changement de regle.
EFFETS = (
    ("persistance_10", "la **persistance**, à dix lignes", "L10-P2", "L10-P1"),
    ("persistance_5", "la persistance, à cinq lignes", "L5-P2", "L5-P1"),
    ("lignes_2", "les **dix lignes**, à persistance 2", "L10-P2", "L5-P2"),
    ("lignes_1", "les dix lignes, sans persistance", "L10-P1", "L5-P1"),
    ("total", "les deux, contre la règle de l'expérience 4", "L10-P2", "L5-P1"),
)
CHAMPS = (("Tracking error contre `TR39` (%/an)", "te", 2),
          ("Tracking error contre la référence appariée (%/an)", "te_app", 2),
          ("Bêta", "beta", 3), ("Part investie (%)", "part", 1),
          ("Séances en espèces", "vides", None), ("Ordres", "ordres", None),
          ("Frais (€)", "frais", 2), ("Durée médiane (séances)", "duree", 1),
          ("Lignes détenues en fin d'année", "ouvertes", None),
          ("Signaux perdus faute de créneau", "perdus", None))


def contient_zero(difference, ic):
    return difference is None or ic is None or abs(difference) <= ic


def egal(publie, calcule):
    """Egalite a la precision publiee : les decimales du nombre publie font foi."""
    if calcule is None:
        return False
    if isinstance(publie, float):
        decimales = len(repr(publie).split(".")[1])
        return round(calcule, decimales) == round(publie, decimales)
    return calcule == publie


def valeur_resume(resume, cle):
    return resume["n_ordres"] if cle == "ordres" else resume.get(cle)


def texte_nombre(valeur, decimales):
    return str(valeur) if decimales is None or valeur is None else fr(valeur, decimales)


def ecarts_publies(b):
    """Tous les nombres publies au README que le moteur ne retrouve pas."""
    ecarts = []

    def confronter(groupe, cle, publie, calcule):
        if not egal(publie, calcule):
            ecarts.append((groupe, cle, publie, calcule))

    for cle, publie in ETALONNAGE_PUBLIE.items():
        confronter("etalonnage", cle, publie, b["etalonnage"][cle])
    confronter("etalonnage", "candidats_persistants",
               PROJECTIONS_PUBLIEES["candidats_persistants"],
               b["etalonnage"]["candidats_persistants"])
    for nom, resume in b["projections"].items():
        for cle, publie in PROJECTIONS_PUBLIEES[nom].items():
            confronter(f"projection {nom}", cle, publie, valeur_resume(resume, cle))
    for cle, publie in PROJECTIONS_PUBLIEES["paires"].items():
        confronter("projection paires", cle, publie, b["paires_p"][cle])
    for reservoir, publie in PROJECTIONS_PUBLIEES["temoin"].items():
        confronter("projection temoin", reservoir, publie, b["temoins_p"][reservoir]["sd"])
    for i, cle in enumerate(("premier", "second")):
        confronter("projection betas", cle, PROJECTIONS_PUBLIEES["betas_semestres"][cle],
                   b["betas_p"][i])
    for modele in ("iid", "marche"):
        publie, calcule = REFERENCES_PUBLIEES[modele], b["references"][modele]
        for cle in ("sous", "dans", "dessus", "bande"):
            confronter(f"reference {modele}", cle, publie[cle], calcule[cle])
        for i in range(3):
            for j in range(3):
                confronter(f"reference {modele}", f"matrice {i}{j}", publie["matrice"][i][j],
                           calcule["lignes"][i][j])
    for i in range(3):
        for j in range(3):
            confronter("reference observe_2021", f"matrice {i}{j}",
                       REFERENCES_PUBLIEES["observe_2021"]["matrice"][i][j],
                       b["matrices"]["etalonnage"]["lignes"][i][j])
    return ecarts


def survie(verdict_4, verdict_6):
    if verdict_4 == "exclut zéro":
        return "survit" if verdict_6 == "sépare" else "**tombe**"
    if verdict_4 == "contient zéro":
        return "**apparaît**" if verdict_6 == "sépare" else "confirmé"
    return "—"


def rotation(resume):
    """Le montant brut echange, rapporte a l'actif moyen."""
    actif = statistics.fmean(resume["valeurs"][j][2] for j in resume["seances"])
    return sum(o["BRUT"] for o in resume["ordres"]) / actif


def section_compte(b):
    alpha = b["base"] - b["base_app"]
    qualite = ("*indiscernable de zéro*" if abs(alpha) <= b["mde_app"]
               else "*au-delà de son effet minimal détectable*")
    nombre, valeur = b["controle"]
    out = [
        "## 1. Le compte", "", "| | |", "|---|---|",
        (f"| **Contrôle de reproduction** | `L5-P1` rend {nombre} ordres et {fr(valeur)} {EURO} "
         "au " + b["fin"] + " : **la règle de l'expérience 4 est retrouvée**, ordre par ordre |"),
        f"| Dotation | {fr(b['dotation'])} {EURO} au {b['debut']} |",
        f"| Valeur finale | **{fr(b['total'])} {EURO}** |",
        f"| Performance | **{signe(b['base'] - 100)} %** |",
        f"| Référence à exposition appariée | {signe(b['base_app'] - 100)} % |",
        f"| {REFERENCE}, même convention | {signe(b['ref_fin'] - 100)} % |",
        (f"| **Alpha officiel — contre la référence appariée** | **{signe(alpha)} pt** — "
         f"{qualite}, effet minimal détectable ± {fr(b['mde_app'], 1)} pt |"),
        (f"| Écart brut à `{REFERENCE}` | {signe(b['base'] - b['ref_fin'])} pt, dont "
         f"{signe(b['base_app'] - b['ref_fin'])} pt d'exposition |"),
        (f"| Ordres | {len(b['ordres'])} ({b['achats']} achats, "
         f"{len(b['ordres']) - b['achats']} ventes) |"),
        (f"| Frais cumulés | {fr(b['frais'])} {EURO}, soit "
         f"{fr(100 * b['frais'] / b['dotation'])} pt de dotation |"),
        f"| Repli maximal | {signe(b['repli'])} %, creux au {b['creux']} |",
        f"| Part investie moyenne | {fr(b['part_investie'], 1)} % |",
        f"| Séances intégralement en espèces | {b['seances_vides']} / {len(b['seances'])} |",
        "", "## 2. Mois par mois", "",
        (f"| Mois | Valeur | Base 100 | Appariée | {REFERENCE} | `L5-P1` | Alpha officiel du mois "
         "| Alpha officiel cumulé | Ordres |"),
        "|---|---|---|---|---|---|---|---|---|",
    ]
    app, l5 = b["appariee_par_jour"], b["combinaisons"]["L5-P1"]["valeurs"]
    fins = fins_de_mois(b["seances"])
    for mois in sorted(fins):
        fin, veille = fins[mois], fins.get(mois_precedent(mois))
        total = b["valeurs"][fin][2]
        base_p = b["valeurs"][veille][2] if veille else b["dotation"]
        app_p = app[veille] if veille else 100.0
        alpha_mois = 100 * (total / base_p - app[fin] / app_p)
        combien = sum(1 for o in b["ordres"] if o["DATE"][:7] == mois)
        out.append(
            f"| {MOIS_TITRE[mois[5:7]]} | [{fr(total)} {EURO}]({RAPPORTS}/{mois}.md) "
            f"| {fr(100 * total / b['dotation'])} | {fr(app[fin])} | {fr(b['ref100'][fin])} "
            f"| {fr(100 * l5[fin][2] / b['dotation'])} | {signe(alpha_mois)} pt "
            f"| {signe(100 * total / b['dotation'] - app[fin])} pt | {combien or '—'} |")
    return out


def section_positions(b):
    lignes = b["positions"]
    out = [
        "", "## 3. Les positions", "",
        (f"> La contribution est **nette des frais payés** : une position encore ouverte n'a "
         "pas payé ses frais de vente. L'alpha d'une position rapporte son écart de **prix "
         f"d'exécution** à l'écart des **clôtures** de {REFERENCE}, qui n'a pas de cours "
         "d'ouverture : c'est une convention, déclarée."), "",
        ("| Valeur | Achat | Sortie | Séances | Prix d'achat | Prix de sortie | +/− value "
         "| Alpha | Contribution | Repli max. clôture | Repli max. `Low` |"),
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p in lignes:
        sortie = f"{p['sortie']} *(ouverte)*" if p["ouverte"] else p["sortie"]
        out.append(
            f"| `{p['ticker']}` {SOCIETES[p['ticker']]} | {p['achat']} | {sortie} "
            f"| {p['seances']} | {fr(p['prix_achat'])} {EURO} | {fr(p['prix_sortie'])} {EURO} "
            f"| **{signe(p['pv'])} %** | {signe(p['alpha'])} pt | {signe(p['euros'])} {EURO} "
            f"| {signe(p['repli_close'])} % | {signe(p['repli_low'])} % |")
    closes = [p for p in lignes if not p["ouverte"]]
    ouvertes = [p for p in lignes if p["ouverte"]]
    mediane = fr(statistics.median(p["seances"] for p in closes), 0) if closes else "—"
    out += [
        "", "## 4. Le motif unique de vente, et la durée des épisodes à l'achat", "",
        "| Mesure | Valeur |", "|---|---|",
        (f"| Positions closes | {len(closes)} — durée médiane {mediane} séances, maximale "
         f"{max((p['seances'] for p in closes), default=0)} |"),
        f"| **Lignes jamais revendues** au {b['fin']} | **{len(ouvertes)}** |",
        (f"| Repli maximal le plus profond, en clôture · sur `Low` | "
         f"{signe(min((p['repli_close'] for p in lignes), default=None))} % · "
         f"{signe(min((p['repli_low'] for p in lignes), default=None))} % |"),
        f"| Séances de silence | {sum(p['silence'] for p in lignes)} |",
        (f"| Signaux perdus faute de créneau | "
         f"{len(b['par_sort'].get('FAUTE DE CRENEAU', []))}, sur {b['jours_pleins']} séances |"),
        "",
        "| Valeur | Décision | Séances sous le bord bas | Séances candidate |",
        "|---|---|---|---|",
    ]
    for o, sous, cand in b["durees"]:
        out.append(f"| `{o['TICKER']}` {SOCIETES[o['TICKER']]} | {o['DATE_DECISION']} "
                   f"| {sous} | {cand} |")
    deuxiemes = sum(1 for _o, sous, _c in b["durees"] if sous == PERSISTANCE)
    out += ["", (f"**{deuxiemes} achats sur {len(b['durees'])}** sont décidés à la "
                 f"{PERSISTANCE}ᵉ séance sous le bord bas, la première que la règle autorise.")]
    return out


def section_univers(ctx, b):
    n = b["narree"]
    out = ["", "## 5. L'univers et la recevabilité des données", "",
           "| Valeur | Entrée dans l'indice | Sortie de l'indice | Évaluable dès |",
           "|---|---|---|---|"]
    for ligne in ctx["retenues"]:
        if ligne["ENTREE_INDICE"] or ligne["SORTIE_INDICE"] or ligne["EVALUABLE_DES"]:
            out.append(f"| `{ligne['TICKER']}` {SOCIETES[ligne['TICKER']]} "
                       f"| {ligne['ENTREE_INDICE'] or '—'} | {ligne['SORTIE_INDICE'] or '—'} "
                       f"| {ligne['EVALUABLE_DES'] or '—'} |")
    out += ["", "| Mesure | 2022 |", "|---|---|",
            (f"| Séances où une valeur à division occupe une place du TOP 10 "
             f"| {n['jours_split_top']} / {n['jours']} |"),
            (f"| Signaux d'achat refusés pour division postérieure "
             f"| {len(b['par_sort'].get('REFUSE DIVISION', []))} |"),
            f"| Évaluations muettes | {n['muettes']} / {n['evaluations']} |",
            (f"| Séances où le TOP compte moins de {TOP} valeurs | {n['jours_top_court']} "
             f"/ {n['jours']} |")]
    return out


def section_etalonnage(b):
    e, n = b["etalonnage"], b["narree"]
    ecarts = {cle for groupe, cle, _p, _v in ecarts_publies(b) if groupe == "etalonnage"}
    publie = {**ETALONNAGE_PUBLIE,
              "candidats_persistants": PROJECTIONS_PUBLIEES["candidats_persistants"]}
    lignes = [
        ("Évaluations", "evaluations"), ("Clôtures sous le bord bas, univers", "sous_bas"),
        ("Places du TOP 10 sous le bord bas", "top_sous_bas"),
        ("Évaluations candidates, au sens de l'expérience 4", "candidats"),
        ("… **dont persistantes**, au sens de l'expérience 6", "candidats_persistants"),
        ("Clôture suivante dans la bande prolongée", "bande_suivante"),
    ]
    out = ["", "## 6. Les taux d'étalonnage, recalculés", "",
           "| Mesure | Publié | Moteur, 2021 | Concorde | 2022 |", "|---|---|---|---|---|"]
    for libelle, cle in lignes:
        out.append(f"| {libelle} | {publie[cle]} | {e[cle]} | {'✗' if cle in ecarts else '✓'} "
                   f"| {n[cle]} |")
    out += ["", (f"**{len(publie) - len(ecarts)} nombres publiés sur {len(publie)}** sont "
                 "retrouvés à l'identique ; le tableau en reprend six, tous sont confrontés.")]
    return out


def section_frais(b):
    out = [
        "", "## 7. Les frais — piste 1", "",
        ("> La seule composante de l'alpha qui se mesure **exactement**. Les frais de 2021 "
         "ont été publiés au [protocole](README.md#les-frais-projetés) avant la première "
         "séance."), "",
        ("| Comptabilité | Lignes | Persistance | Ordres 2021 · **2022** | Frais 2021 "
         "| **Frais 2022** | En points de dotation | Brut échangé / actif moyen |"),
        "|---|---|---|---|---|---|---|---|",
    ]
    for nom, lignes, persistance in COMBINAISONS:
        r, p = b["combinaisons"][nom], b["projections"][nom]
        marque = "**" if nom == "L10-P2" else ""
        out.append(f"| {marque}`{nom}`{marque} | {lignes} | {persistance} "
                   f"| {p['n_ordres']} · **{r['n_ordres']}** | {fr(p['frais'])} {EURO} "
                   f"| **{fr(r['frais'])} {EURO}** | {fr(100 * r['frais'] / DOTATION)} pt "
                   f"| {fr(rotation(r))} |")
    out += ["", "| Effet de | Ordres | Frais | En points de dotation |", "|---|---|---|---|"]
    for _cle, libelle, a, c in EFFETS:
        ra, rc = b["combinaisons"][a], b["combinaisons"][c]
        out.append(f"| {libelle} | {ra['n_ordres'] - rc['n_ordres']:+d} "
                   f"| {signe(ra['frais'] - rc['frais'])} {EURO} "
                   f"| {signe(100 * (ra['frais'] - rc['frais']) / DOTATION)} pt |")
    r6, r4 = b["combinaisons"]["L10-P2"], b["combinaisons"]["L5-P1"]
    ecart = 100 * (r6["frais"] - r4["frais"]) / DOTATION
    out += ["", (
        f"Le portefeuille a payé **{fr(r6['frais'])} {EURO}** de frais, contre "
        f"{fr(r4['frais'])} {EURO} pour la règle de l'expérience 4 : "
        f"**{signe(ecart)} point de dotation**, "
        f"{'gagné' if ecart < 0 else 'perdu'} avec certitude.")]
    return out


def section_alpha(b):
    t_u, t_t = b["temoins"]["UNIVERS"], b["temoins"]["TOP10"]
    exposition_pt, selection_pt = b["base_app"] - b["ref_fin"], b["base"] - b["base_app"]
    reg = b["regression"]
    lecture = ("**indiscernable** d'un choix de valeurs au hasard" if abs(t_u["z"]) <= Z95
               else "**au-delà** de ce que le hasard donne à 95 %")
    out = [
        "", "## 8. L'alpha séparé du bêta — piste 2", "",
        f"| | Base 100 au {b['fin']} |", "|---|---|",
        f"| `{REFERENCE}` | {fr(b['ref_fin'])} |",
        f"| Référence à exposition appariée | {fr(b['base_app'])} |",
        f"| **Le portefeuille** | **{fr(b['base'])}** |",
        "",
        (f"Sur les {signe(b['base'] - b['ref_fin'])} points d'écart brut à `{REFERENCE}`, "
         f"{signe(exposition_pt)} points reviennent à l'exposition. **L'alpha officiel vaut "
         f"{signe(selection_pt)} points**, pour une tracking error réalisée de "
         f"{fr(b['te_app'])} %/an contre la référence appariée — déclarée "
         f"{fr(TE_DECLAREE)} — soit un effet minimal détectable de ± {fr(b['mde_app'], 1)} "
         f"points : l'alpha officiel "
         f"{'reste dans' if abs(selection_pt) <= b['mde_app'] else 'dépasse'} son effet "
         "minimal détectable."),
        "", "| | Premier semestre | Second semestre |", "|---|---|---|",
        f"| Bêta, 2022 | {fr(b['betas'][0], 3)} | {fr(b['betas'][1], 3)} |",
        f"| Bêta, 2021 recalculé | {fr(b['betas_p'][0], 3)} | {fr(b['betas_p'][1], 3)} |",
        "", "### Le témoin aléatoire", "",
        ("| Réservoir | Fait foi | Moyenne des témoins | Écart-type | EMD | Portefeuille "
         "| Rang | z |"),
        "|---|---|---|---|---|---|---|---|",
    ]
    for t in (t_u, t_t):
        foi = "**oui**" if t["reservoir"] == RESERVOIR_FOI else "non"
        out.append(f"| `{t['reservoir']}` | {foi} | {fr(t['moyenne'])} | {fr(t['sd'])} pt "
                   f"| ± {fr(t['emd'], 1)} pt | {fr(t['reel'])} | {fr(t['rang'], 1)} % "
                   f"| {signe(t['z'])} |")
    out += [
        "", (f"Le portefeuille dépasse **{fr(t_u['rang'], 1)} %** des témoins du réservoir qui "
             f"fait foi (z = {signe(t_u['z'])}) : il est {lecture} aux mêmes dates et montants."),
        "", "| Alpha de régression contre `TR39` | Bêta | IC95 |", "|---|---|---|",
        f"| {signe(reg['alpha'])} %/an | {fr(reg['beta'], 3)} | ± {fr(reg['ic_alpha'], 1)} |",
    ]
    return out


def section_combinaisons(b):
    comb = b["combinaisons"]
    noms = [nom for nom, _l, _p in COMBINAISONS]
    lignes_table = (
        ("Base 100 au " + b["fin"], lambda r: fr(r["base"][-1])),
        ("**Alpha officiel**", lambda r: f"**{signe(r['alpha_officiel'])} pt**"),
        ("Tracking error contre la référence appariée", lambda r: f"{fr(r['te_app'])} %/an"),
        ("Tracking error contre `TR39`", lambda r: f"{fr(r['te'])} %/an"),
        ("Bêta", lambda r: fr(r["beta"], 3)),
        ("Part investie", lambda r: f"{fr(r['part'], 1)} %"),
        ("Ordres · frais", lambda r: f"{r['n_ordres']} · {fr(r['frais'])} {EURO}"),
        ("Signaux perdus faute de créneau", lambda r: str(r["perdus"])),
    )
    out = ["", "## 9. Les lignes et la persistance — les quatre combinaisons", "",
           ("> Quatre comptabilités qui ne diffèrent que par le nombre de lignes et la "
            "persistance. `L5-P1` est la règle de l'expérience 4, `L10-P2` le portefeuille."), "",
           "| Grandeur, 2022 | " + " | ".join(f"`{n}`" for n in noms) + " |",
           "|---|" + "---|" * len(noms)]
    for libelle, rendu in lignes_table:
        out.append(f"| {libelle} | " + " | ".join(rendu(comb[n]) for n in noms) + " |")
    out += ["", ("| Écart | Ce qu'il isole | Base 100 | Écart-type de la différence | EMD "
                 "| Bêta de la différence |"),
            "|---|---|---|---|---|---|"]
    for cle, libelle, a, c in EFFETS:
        e = b["effets"][cle]
        ecart = comb[a]["base"][-1] - comb[c]["base"][-1]
        out.append(f"| `{a}` − `{c}` | {libelle} | **{signe(ecart)} pt** | {fr(e['te'])} %/an "
                   f"| ± {fr(Z95 * e['te'], 1)} pt | {fr(e['beta'], 3)} |")
    interaction = ((comb["L10-P2"]["base"][-1] - comb["L5-P2"]["base"][-1])
                   - (comb["L10-P1"]["base"][-1] - comb["L5-P1"]["base"][-1]))
    persistance = b["effets"]["persistance_10"]
    ecart_p = comb["L10-P2"]["base"][-1] - comb["L10-P1"]["base"][-1]
    out += ["", (
        f"L'interaction — l'effet des lignes à persistance 2 moins leur effet sans persistance — "
        f"vaut {signe(interaction)} points. À dix lignes, la persistance déplace la base 100 de "
        f"{signe(ecart_p)} points, ce qui "
        f"{'reste dans' if abs(ecart_p) <= Z95 * persistance['te'] else 'dépasse'} son effet "
        f"minimal détectable de ± {fr(Z95 * persistance['te'], 1)} points ; elle déplace la part "
        f"investie de {signe(comb['L10-P2']['part'] - comb['L10-P1']['part'], 1)} points.")]
    return out


def section_issues(b):
    ph, rejets, verdicts, verdicts_4 = b["phases"], b["holm"], b["verdicts"], b["verdicts_4"]
    out = [
        "", "## 10. Les issues remesurées, persistance comprise", "",
        ("> Convention de l'[expérience 5](../experience_5/README.md#le-verdict-et-sa-règle) : "
         "grappes de dates, vingt phases, Holm sur cinq comparaisons ; une comparaison sépare "
         f"son issue si Holm la rejette et si au moins {SEUIL_PHASES} phases sur {PHASES} "
         "excluent zéro avec le même signe."), "",
        ("| Élément | Effectifs | Différence | IC95 Welch | IC95 par grappes | G | p | Holm "
         "| Phases excluant zéro | Verdict de l'expérience 4 | **Verdict** | Survie |"),
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for cle, libelle, *_r in COMPARAISONS:
        c = ph[cle]["phases"][0]
        out.append(
            f"| {libelle} | {c['na']} contre {c['nb']} | **{signe(c['difference'])} pt** "
            f"| ± {fr(c['ic_welch'])} pt | ± {fr(c['ic'])} pt | {c['G']} | {fr(c['p'], 3)} "
            f"| {'rejetée' if rejets[cle] else 'non rejetée'} "
            f"| {ph[cle]['n_exclut']} / {PHASES} | {verdicts_4[cle]} | **{verdicts[cle]}** "
            f"| {survie(verdicts_4[cle], verdicts[cle])} |")
    out += ["", ("| Élément | EMD projeté par grappes | IC95 réalisé par grappes "
                 "| IC95 par grappes, toutes séances |"), "|---|---|---|---|"]
    for cle, libelle, *_r in COMPARAISONS:
        projete = EMD_GRAPPES.get(cle)
        texte = f"± {fr(projete, 1)} pt" if projete else "non mesurable"
        out.append(f"| {libelle} | {texte} "
                   f"| ± {fr(ph[cle]['phases'][0]['ic'])} pt "
                   f"| ± {fr(b['quotidien'][cle]['ic'])} pt |")
    separent = [lib for cle, lib, *_r in COMPARAISONS if verdicts[cle] == "sépare"]
    cand, cand_places, _pe, _ee = b["episodes_candidats"]
    out += ["", (f"Sous la règle de l'expérience 6, les {cand_places} évaluations candidates de "
                 f"l'audit forment **{cand} épisodes**."), "",
            ("**Ce qui sépare son issue, sous la convention déclarée : "
             + (", ".join(separent) if separent else "aucun élément de la règle") + ".**")]
    return out


def section_bande(b):
    ref, mat, etats = b["references"], b["matrices"], b["etats"]
    be, bq = b["bande_echantillon"], b["bande_quotidien"]

    def ic(p):
        return f" ± {fr(p['ic'], 1)}" if p["ic"] is not None else ""

    out = ["", "## 11. La bande contre ses deux références", "",
           "| | Sous le bord bas | Dans la bande | Au-dessus du bord haut | `BANDE` |",
           "|---|---|---|---|---|"]
    for nom, cle in (("Bruit i.i.d.", "iid"), ("Marche aléatoire", "marche")):
        r = ref[cle]
        out.append(f"| {nom} | {fr(r['sous'], 1)} % | {fr(r['dans'], 1)} % "
                   f"| {fr(r['dessus'], 1)} % | {fr(r['bande'], 1)} % |")
    out += [
        (f"| **Observé, sous-échantillon d'audit** | {fr(etats['sous']['taux'], 1)} %"
         f"{ic(etats['sous'])} | {fr(etats['dans']['taux'], 1)} %{ic(etats['dans'])} "
         f"| {fr(etats['dessus']['taux'], 1)} %{ic(etats['dessus'])} "
         f"| **{fr(be['taux'], 1)} %{ic(be)}** |"),
        (f"| Observé, toutes les séances d'audit | {fr(mat['audit']['sous'], 1)} % "
         f"| {fr(mat['audit']['dans'], 1)} % | {fr(mat['audit']['dessus'], 1)} % "
         f"| {fr(bq['taux'], 1)} %{ic(bq)} |"),
        "", ("La bande ne dépend pas de la règle : ces nombres sont ceux de l'expérience 5, "
             "recalculés."),
    ]
    return out


def section_fantomes(b):
    out = ["", "## 12. Les fantômes `SANS-P20` et `MENSUEL`", "",
           ("| | Base 100 | Part investie | Bêta | Ordres | Frais | Écart-type de la "
            "différence | EMD |"),
           "|---|---|---|---|---|---|---|---|",
           (f"| **Le portefeuille** | **{fr(b['base'])}** | {fr(b['part_investie'], 1)} % "
            f"| {fr(b['regression']['beta'], 3)} | {len(b['ordres'])} | {fr(b['frais'])} {EURO} "
            "| — | — |")]
    for nom, cle in (("`SANS-P20`", "r_f"), ("`MENSUEL`", "r_m")):
        r = b[cle]
        te = b["paires_fantomes"][cle]["te"]
        out.append(f"| {nom} | {fr(r['base'][-1])} | {fr(r['part'], 1)} % | {fr(r['beta'], 3)} "
                   f"| {r['n_ordres']} | {fr(r['frais'])} {EURO} | {fr(te)} %/an "
                   f"| ± {fr(Z95 * te, 1)} pt |")
    return out


def section_sensibilite_conventions(b):
    out = ["", "## 13. La sensibilité aux paramètres — au sens de l'expérience 4", "",
           ("| Jeu | TOP | K | Candidats par évaluation | Au-dessus du bord haut "
            "| Entrants dans le TOP par séance |"),
           "|---|---|---|---|---|---|"]
    for jeu in b["sensibilite"]:
        nom = "**déclaré**" if jeu["nom"] == "déclaré" else f"`{jeu['nom']}`"
        out.append(f"| {nom} | {jeu['top']} | {fr(jeu['k'], 1)} "
                   f"| {jeu['candidats']} / {jeu['evaluees']} — "
                   f"{pourcent(jeu['candidats'], jeu['evaluees'], 2)} "
                   f"| {pourcent(jeu['ventes'], jeu['evaluees'])} | {fr(jeu['entrants'], 2)} |")
    out += [
        "", "## 14. Les trois conventions", "",
        f"| Série | Convention | {ANNEE} | Écart du portefeuille |", "|---|---|---|---|",
        f"| Le portefeuille | rendement total | **{signe(b['base'] - 100)} %** | — |",
        (f"| Référence appariée | rendement total, exposition du portefeuille "
         f"| {signe(b['base_app'] - 100)} % | **{signe(b['base'] - b['base_app'])} pt** |"),
        (f"| `{REFERENCE}` | rendement total | {signe(b['ref_fin'] - 100)} % "
         f"| {signe(b['base'] - b['ref_fin'])} pt |"),
        (f"| `{REFERENCE_NUE}` | indice **nu** | {signe(b['nue'])} % "
         f"| {signe(b['base'] - 100 - b['nue'])} pt |"),
    ]
    return out


def section_dimensionnement(b):
    ecarts = {(g, c) for g, c, _p, _v in ecarts_publies(b) if g.startswith("projection")}
    realises = {**b["combinaisons"], "SANS-P20": b["r_f"], "MENSUEL": b["r_m"]}
    out = ["", "## 15. Le dimensionnement, confronté", ""]
    for nom in [*b["combinaisons"], "SANS-P20", "MENSUEL"]:
        out += [f"### `{nom}`", "",
                "| Grandeur | Publié, 2021 | Recalculé, 2021 | Concorde | Réalisé, 2022 |",
                "|---|---|---|---|---|"]
        for libelle, cle, decimales in CHAMPS:
            if cle not in PROJECTIONS_PUBLIEES[nom]:
                continue
            publie = PROJECTIONS_PUBLIEES[nom][cle]
            recalc = valeur_resume(b["projections"][nom], cle)
            realise = valeur_resume(realises[nom], cle)
            out.append(f"| {libelle} | {texte_nombre(publie, decimales)} "
                       f"| {texte_nombre(recalc, decimales)} "
                       f"| {'✗' if (f'projection {nom}', cle) in ecarts else '✓'} "
                       f"| {texte_nombre(realise, decimales)} |")
        out.append("")
    erreur_app = abs(math.log(b["te_app"] / TE_DECLAREE))
    erreur_tr = abs(math.log(b["te"] / TE_TR39_PROJETEE))
    out += [
        "### Les tracking errors déclarées", "",
        "| | Déclarée | Réalisée | Écart relatif, en logarithme |", "|---|---|---|---|",
        (f"| **Contre la référence appariée — l'alpha officiel** | {fr(TE_DECLAREE)} %/an "
         f"| {fr(b['te_app'])} %/an | {fr(erreur_app, 3)} |"),
        (f"| Contre `{REFERENCE}` | {fr(TE_TR39_PROJETEE)} %/an | {fr(b['te'])} %/an "
         f"| {fr(erreur_tr, 3)} |"),
        "",
        (f"L'effet minimal détectable de l'alpha officiel, déclaré ± {fr(Z95 * TE_DECLAREE, 1)} "
         f"points, est réalisé à ± {fr(b['mde_app'], 1)} points. La confrontation n'est pas "
         "aveugle : 2022 est connue."),
    ]
    return out


def section_conclusion(b):
    separent = [lib for cle, lib, *_r in COMPARAISONS if b["verdicts"][cle] == "sépare"]
    t_u = b["temoins"]["UNIVERS"]
    r6, r4 = b["combinaisons"]["L10-P2"], b["combinaisons"]["L5-P1"]
    alpha = b["base"] - b["base_app"]
    nb_ecarts = len(ecarts_publies(b))
    return [
        "", "## 16. Ce que l'expérience établit, et ce qu'elle n'établit pas", "",
        "**Elle établit**, avec les incertitudes publiées :", "",
        "- que `L5-P1` retrouve la règle de l'expérience 4, ordre par ordre — § 1 ;",
        (f"- **ce que les deux changements font aux frais** : {fr(r6['frais'])} {EURO} contre "
         f"{fr(r4['frais'])} {EURO}, soit "
         f"{signe(100 * (r6['frais'] - r4['frais']) / DOTATION)} point de dotation, sans "
         "incertitude — § 7 ;"),
        (f"- ce qu'ils font à l'exposition : part investie {fr(r6['part'], 1)} % contre "
         f"{fr(r4['part'], 1)} %, bêta {fr(r6['beta'], 3)} contre {fr(r4['beta'], 3)} — § 9 ;"),
        (f"- que la tracking error contre la référence appariée vaut {fr(b['te_app'])} %/an, "
         f"contre {fr(r4['te_app'])} %/an pour la règle de l'expérience 4 — § 8, 9 ;"),
        ("- ce qui sépare son issue sous la convention déclarée : "
         + (", ".join(separent) if separent else "aucun élément de la règle") + " — § 10 ;"),
        ("- que les nombres publiés avant la première séance "
         + ("sont tous retrouvés par le moteur" if not nb_ecarts
            else f"sont retrouvés à {nb_ecarts} écarts près, publiés") + " — § 6, 15."),
        "", "**Elle n'établit pas** :", "",
        (f"- que l'alpha a été amélioré : l'alpha officiel vaut {signe(alpha)} points pour un "
         f"effet minimal détectable de ± {fr(b['mde_app'], 1)} ;"),
        (f"- que la règle sélectionne mieux que le hasard : rang {fr(t_u['rang'], 1)} %, "
         f"z = {signe(t_u['z'])}"
         + (" ;" if abs(t_u["z"]) <= Z95 else
            " — au-delà du hasard à 95 %, mais sur une règle choisie après avoir vu 2022 ;")),
        ("- quoi que ce soit d'aveugle : la règle est de catégorie B, et 2022 était connue "
         "quatre fois."),
        "", "---", "",
        (f"[← Protocole](README.md) · [Décembre]({RAPPORTS}/{ANNEE}-12.md) · "
         f"[Janvier]({RAPPORTS}/{ANNEE}-01.md) · [L'expérience 5](../experience_5/bilan-2022.md)"),
    ]


def bilan_annuel(ctx, b):
    out = [
        f"# Bilan de l'année {ANNEE}", "",
        (f"> [Expérience 6](README.md) · dix lignes, achat persistant · "
         f"**{signe(b['base'] - 100)} %** · alpha officiel "
         f"**{signe(b['base'] - b['base_app'])} pt**"), "",
        ("> ⚠️ **La règle est de catégorie B** et 2022 était connue : le "
         "[protocole](README.md#-ce-que-rejouer-2022-une-quatrième-fois-coûte) le déclarait "
         "avant la première séance. Ce que ce bilan établit est aux sections 7 à 9."), "",
        "---", "",
        *section_compte(b), *section_positions(b), *section_univers(ctx, b),
        *section_etalonnage(b), *section_frais(b), *section_alpha(b),
        *section_combinaisons(b), *section_issues(b), *section_bande(b),
        *section_fantomes(b), *section_sensibilite_conventions(b),
        *section_dimensionnement(b), *section_conclusion(b),
    ]
    return NL_.join(out) + NL_


# --------------------------------------------------------------------------
# Assemblage


def construire_contexte(args):
    """Lit tout, construit le calendrier, evalue chaque valeur a chaque seance."""
    retenues, exclusions = charger_univers(args.repertoire)
    tickers = sorted({ligne["TICKER"] for ligne in retenues})
    series = {t: charger_serie(nom_fichier(t, args.quotes)) for t in tickers}
    reference = charger_serie(nom_fichier(REFERENCE, args.quotes))
    nue = charger_serie(nom_fichier(REFERENCE_NUE, args.quotes))
    calendrier = reference["jours"]
    if calendrier[-1] != FIN_SERIE:
        erreur(f"{REFERENCE} s'arrete au {calendrier[-1]}, pas au {FIN_SERIE}")
    jours_audit = [j for j in calendrier if DEBUT_AUDIT <= j < FIN_SERIE]
    jours_etalonnage = [j for j in jours_audit if j < DEBUT_NARREE]
    jours_narres = [j for j in jours_audit if j >= DEBUT_NARREE]
    if (len(jours_etalonnage) != SEANCES_ETALONNAGE
            or len(jours_narres) != SEANCES_NARREES):
        erreur(f"Calendrier incomplet : {len(jours_etalonnage)} seances d'etalonnage et "
               f"{len(jours_narres)} narrees, au lieu de {SEANCES_ETALONNAGE} et "
               f"{SEANCES_NARREES}")
    if PERSISTANCE not in (1, 2):
        erreur("PERSISTANCE doit valoir 1 ou 2")
    jours_evalues = [*jours_audit, FIN_SERIE]
    evaluations = {j: {t: evaluer(series[t], t, j) for t in tickers} for j in jours_evalues}
    univers = {j: univers_du_jour(retenues, j) for j in jours_evalues}
    return {
        "args": args, "tickers": tickers, "retenues": retenues, "exclusions": exclusions,
        "series": series, "reference": reference, "nue": nue,
        "jours_audit": jours_audit, "jours_etalonnage": jours_etalonnage,
        "jours_narres": jours_narres, "jours_evalues": jours_evalues,
        "jours_projection": [j for j in jours_etalonnage if j < FIN_ETALONNAGE],
        "execution": {j: calendrier[reference["rang"][j] + 1] for j in jours_audit},
        "evaluations": evaluations, "univers": univers,
        "rangs": {j: classer(evaluations[j], univers[j]) for j in jours_evalues},
        "phase": {j: i % PHASES for i, j in enumerate(jours_audit)},
        "veille": {},
    }


def completer(ctx, resume, seances):
    """Ajoute a un resume sa reference appariee, sa tracking error contre elle et son alpha."""
    resume["app"] = reference_appariee(ctx, resume["valeurs"], seances)
    resume["te_app"] = ecart_apparie(resume["base"], resume["app"])["te"]
    resume["alpha_officiel"] = resume["base"][-1] - resume["app"][-1]
    return resume


def construire_bilan(ctx):
    """Joue les dix comptabilites, controle la regle 4, remesure tout."""
    narres, projection = ctx["jours_narres"], ctx["jours_projection"]
    seances = [ctx["execution"][d] for d in narres]
    seances_p = [ctx["execution"][d] for d in projection]
    debut, fin = seances[0], seances[-1]

    simulations, combinaisons, projections = {}, {}, {}
    for nom, lignes, persistance in COMBINAISONS:
        simulations[nom] = simuler(ctx, narres, seances, lignes, persistance)
        combinaisons[nom] = completer(ctx, resumer(ctx, simulations[nom], seances), seances)
        projections[nom] = completer(ctx, resumer(
            ctx, simuler(ctx, projection, seances_p, lignes, persistance), seances_p), seances_p)
    controle = controler_reproduction(ctx["args"].repertoire, simulations["L5-P1"][0],
                                      simulations["L5-P1"][2])
    ordres, signaux, valeurs, journal, _registre = simulations["L10-P2"]
    r = combinaisons["L10-P2"]
    r_f = resumer(ctx, simuler(ctx, narres, seances, avec_p20=False), seances)
    r_m = resumer(ctx, simuler(ctx, decisions_mensuelles(ctx, narres), seances), seances)
    projections["SANS-P20"] = resumer(ctx, simuler(ctx, projection, seances_p, avec_p20=False),
                                      seances_p)
    projections["MENSUEL"] = resumer(
        ctx, simuler(ctx, decisions_mensuelles(ctx, projection), seances_p), seances_p)

    p6 = projections["L10-P2"]
    paires_p = {nom: ecart_apparie(p6["base"], projections[nom]["base"])["te"]
                for nom in ("L10-P1", "L5-P2", "L5-P1", "SANS-P20")}
    mensuel_p = ecart_apparie(p6["base"], projections["MENSUEL"]["base"], p6["indice"])
    paires_p.update({"MENSUEL": mensuel_p["te"], "MENSUEL_neutralise": mensuel_p["te_residu"]})

    base, indice = r["base"], r["indice"]
    pic, repli, creux = -1e18, 0.0, fin
    for jour in seances:
        pic = max(pic, valeurs[jour][2])
        if valeurs[jour][2] / pic - 1 < repli:
            repli, creux = valeurs[jour][2] / pic - 1, jour

    lignes_issues = issues(ctx, ctx["jours_audit"], FIN_SERIE)
    echantillon = [li for li in lignes_issues if li["SOUS_ECHANTILLON"]]
    resultat_phases = phases(lignes_issues)
    rejets = holm({cle: resultat_phases[cle]["phases"][0]["p"] for cle, *_r in COMPARAISONS})
    verdicts_4 = {cle: verdict_experience_4(resultat_phases[cle]["phases"][0])
                  for cle, *_r in COMPARAISONS}
    verdicts_4["PERSISTANCE"] = "—"
    par_sort = {}
    for signal in signaux:
        par_sort.setdefault(signal["SORT"], []).append(signal)
    nue = ctx["nue"]["par_jour"]
    rgs = ctx["rangs"]
    te_app = r["te_app"]

    return {
        "dotation": DOTATION, "debut": debut, "fin": fin, "seances": seances,
        "valeurs": valeurs, "valeurs_f": r_f["valeurs"], "valeurs_m": r_m["valeurs"],
        "ref100": dict(zip(seances, indice, strict=True)), "controle": controle,
        "ordres": ordres, "signaux": signaux, "journal": journal,
        "r": r, "r_f": r_f, "r_m": r_m, "combinaisons": combinaisons,
        "projections": projections, "paires_p": paires_p,
        "total": valeurs[fin][2], "base": base[-1], "base_app": r["app"][-1],
        "appariee_par_jour": dict(zip(seances, r["app"], strict=True)),
        "te_app": te_app, "mde_app": Z95 * te_app, "ref_fin": indice[-1],
        "nue": 100 * (nue[fin]["close"] / nue[debut]["close"] - 1),
        "achats": sum(1 for o in ordres if o["SENS"] == "ACHAT"), "frais": r["frais"],
        "repli": 100 * repli, "creux": creux, "part_investie": r["part"],
        "seances_vides": r["vides"], "positions": r["positions"], "par_sort": par_sort,
        "jours_pleins": len({s["DATE_DECISION"] for s in par_sort.get("FAUTE DE CRENEAU", [])}),
        "lignes_issues": lignes_issues, "phases": resultat_phases, "holm": rejets,
        "verdicts": {cle: verdict_t1(resultat_phases[cle], rejets[cle])
                     for cle, *_r in COMPARAISONS},
        "verdicts_4": verdicts_4,
        "quotidien": {cle: grappes(lignes_issues, pop, grp)
                      for cle, *_r, pop, grp in COMPARAISONS},
        "bande_echantillon": proportion_grappes(echantillon, lambda li: li["BANDE_SUIVANTE"]),
        "bande_quotidien": proportion_grappes(lignes_issues, lambda li: li["BANDE_SUIVANTE"]),
        "etats": {
            "sous": proportion_grappes(echantillon, lambda li: li["SOUS_BAS"]),
            "dessus": proportion_grappes(echantillon, lambda li: li["AU_DESSUS_HAUT"]),
            "dans": proportion_grappes(
                echantillon, lambda li: not (li["SOUS_BAS"] or li["AU_DESSUS_HAUT"])),
        },
        "references": {"iid": lire_matrice(reference_bande(False, GRAINE_IID)),
                       "marche": lire_matrice(reference_bande(True, GRAINE_MARCHE))},
        "matrices": {
            "etalonnage": lire_matrice(matrice_bande(ctx, ctx["jours_etalonnage"],
                                                     FIN_ETALONNAGE)),
            "audit": lire_matrice(matrice_bande(ctx, ctx["jours_audit"], FIN_SERIE)),
        },
        "etalonnage": taux_regle(ctx, ctx["jours_etalonnage"], ctx["jours_etalonnage"][-1]),
        "narree": taux_regle(ctx, narres, FIN_SERIE),
        "sensibilite": sensibilite(ctx),
        "te": r["te"], "regression": r["regression"],
        "effets": {cle: ecart_apparie(combinaisons[a]["base"], combinaisons[c]["base"], indice)
                   for cle, _l, a, c in EFFETS},
        "paires_fantomes": {"r_f": ecart_apparie(base, r_f["base"]),
                            "r_m": ecart_apparie(base, r_m["base"], indice)},
        "betas": betas_semestres(base, indice, seances, FIN_SEMESTRE),
        "betas_p": betas_semestres(p6["base"], p6["indice"], seances_p, FIN_SEMESTRE_2021),
        "temoins": {res: temoin(ctx, r["positions"], fin, valeurs[fin][2], res)
                    for res in ("UNIVERS", "TOP10")},
        "temoins_p": {res: temoin(ctx, p6["positions"], seances_p[-1],
                                  p6["valeurs"][seances_p[-1]][2], res)
                      for res in ("UNIVERS", "TOP10")},
        "episodes_candidats": episodes(ctx, lambda t, j: candidat(ctx, t, j)),
        "episodes_top": episodes(ctx, lambda t, j: (rgs[j].get(t) or TOP + 1) <= TOP),
        "durees": [(o, *duree_a_l_achat(ctx, o)) for o in ordres if o["SENS"] == "ACHAT"],
    }


def bloc_mensuel(b, mois):
    """Le bloc console d'un mois d'executions."""
    jours = [j for j in b["seances"] if j[:7] == mois]
    fin_mois = jours[-1]
    lignes = ["", f"=== {mois} {MEDIAN} {len(jours)} seances d'execution ===", ""]
    ordres = [o for o in b["ordres"] if o["DATE"][:7] == mois]
    lignes.append("Ordres executes" if ordres else "Aucun ordre")
    for o in ordres:
        lignes.append(f"  {o['DATE']} {o['SENS']:<6s} {o['TICKER']:<9s} {o['QUANTITE']:5d}"
                      f" a {fr(o['PRIX']):>10s} EUR {MEDIAN} {o['MOTIF']}")
    decisions = {d for d, etape in b["journal"].items() if etape["execution"][:7] == mois}
    for s in b["signaux"]:
        if s["DATE_DECISION"] in decisions and s["SORT"] != "EXECUTE":
            lignes.append(f"  non execute {s['DATE_DECISION']} {s['TICKER']:<9s} "
                          f"rang {s['RANG']:2d} {MEDIAN} {s['SORT']}")
    especes, _titres, total, nombre = b["valeurs"][fin_mois]
    base = 100 * total / b["dotation"]
    lignes += ["", (f"Portefeuille au {fin_mois} : {fr(total)} EUR ({nombre} lignes, "
                    f"especes {fr(especes)}) {MEDIAN} base {fr(base)} {MEDIAN} appariee "
                    f"{fr(b['appariee_par_jour'][fin_mois])} {MEDIAN} {REFERENCE} "
                    f"{fr(b['ref100'][fin_mois])}")]
    return NL_.join(lignes)


def imprimer_bilan(b):
    nombre, valeur = b["controle"]
    comb = b["combinaisons"]
    print(f"""
=== Bilan au {b['fin']} ===

  Controle L5-P1          {nombre} ordres, {fr(valeur)} EUR, la regle de l'experience 4
  Performance             {signe(b['base'] - 100)} %  ({REFERENCE} {signe(b['ref_fin'] - 100)} %, \
appariee {signe(b['base_app'] - 100)} %)
  Alpha officiel          {signe(b['base'] - b['base_app'])} pt (MDE +/- {fr(b['mde_app'], 1)} pt, \
TE {fr(b['te_app'])} %/an, declaree {fr(TE_DECLAREE)})
  Ecart brut a {REFERENCE}       {signe(b['base'] - b['ref_fin'])} pt""")
    print("  Combinaisons            base 100 / alpha officiel / part investie / ordres / frais :")
    for nom, _l, _p in COMBINAISONS:
        r = comb[nom]
        print(f"    {nom:<7s} {fr(r['base'][-1]):>7s} {MEDIAN} {signe(r['alpha_officiel']):>7s} pt "
              f"{MEDIAN} {fr(r['part'], 1):>5s} % {MEDIAN} {r['n_ordres']:3d} {MEDIAN} "
              f"{fr(r['frais'])} EUR")
    print("  Issues, grappes, phase 0 :")
    for cle, *_r in COMPARAISONS:
        c = b["phases"][cle]["phases"][0]
        print(f"    {cle:<11s} {signe(c['difference'])} +/- {fr(c['ic'])} pt {MEDIAN} "
              f"phases {b['phases'][cle]['n_exclut']}/{PHASES} {MEDIAN} {b['verdicts'][cle]}")
    for reservoir, t in b["temoins"].items():
        print(f"  Temoin {reservoir:<16s} rang {fr(t['rang'], 1)} % {MEDIAN} z {signe(t['z'])}"
              f" {MEDIAN} EMD +/- {fr(t['emd'], 1)} pt")
    for groupe, cle, publie, calcule in ecarts_publies(b):
        print(f"  ECART {groupe.upper()} {cle} : publie {publie}, moteur {calcule}")
    print()


def lignes_evaluations(ctx):
    lignes = []
    for jour in ctx["jours_evalues"]:
        rangs, univers = ctx["rangs"][jour], set(ctx["univers"][jour])
        for ticker in ctx["tickers"]:
            ev = ctx["evaluations"][jour][ticker]
            ligne = {"DATE": jour, "TICKER": ticker, "UNIVERS": oui(ticker in univers),
                     "CLOSE": ev["CLOSE"], "DIAGNOSTIC": ev["DIAGNOSTIC"]}
            if not ev["MUETTE"]:
                ligne.update({c: arrondi(ev[c]) for c in (
                    "E_120", "VAL_120", "S_120", "TAUX_120", "ECART_S", "E_20", "VAL_20",
                    "TAUX_20", "ENV_BAS", "ENV_HAUT", "LARGEUR_ENV_S")})
                ligne["RANG"] = rangs.get(ticker)
                ligne["CANDIDAT"] = oui(ticker in univers and candidat(ctx, ticker, jour))
            lignes.append(ligne)
    return lignes


def lignes_top(ctx):
    lignes = []
    for jour in ctx["jours_audit"]:
        rangs = ctx["rangs"][jour]
        for ticker in sorted((t for t, r in rangs.items() if r <= TOP), key=rangs.get):
            ev = ctx["evaluations"][jour][ticker]
            lignes.append({"DATE": jour, "RANG": rangs[ticker], "TICKER": ticker,
                           "TAUX_120": arrondi(ev["TAUX_120"]),
                           "ECART_S": arrondi(ev["ECART_S"]),
                           "TAUX_20": arrondi(ev["TAUX_20"]),
                           "CANDIDAT": oui(candidat(ctx, ticker, jour))})
    return lignes


def lignes_arrondies(lignes, champs, decimales=6):
    return [{**li, **{c: arrondi(li[c], decimales) for c in champs}} for li in lignes]


def ecrire_csvs(ctx, b):
    rep = ctx["args"].repertoire
    ecrire_csv(rep / "evaluations.csv", ENTETE_EVALUATIONS, lignes_evaluations(ctx))
    ecrire_csv(rep / "top10.csv", ENTETE_TOP, lignes_top(ctx))
    ecrire_csv(rep / "ordres.csv", ENTETE_ORDRES, lignes_arrondies(
        b["ordres"], ("PRIX", "BRUT", "FRAIS", "NET", "TAUX_120", "ECART_S", "TAUX_20",
                      "ECART_OUVERTURE"), 4))
    ecrire_csv(rep / "signaux.csv", ENTETE_SIGNAUX,
               lignes_arrondies(b["signaux"], ("ECART_S", "TAUX_20")))
    ecrire_csv(rep / "issues.csv", ENTETE_ISSUES, [
        {**li, "EXCES_20": arrondi(li["EXCES_20"], 4),
         **{c: oui(li[c]) for c in ("SOUS_ECHANTILLON", "TOP10", "SOUS_BAS",
                                    "AU_DESSUS_HAUT", "TAUX_20_POSITIF", "PERSISTANT")},
         "BANDE_SUIVANTE": None if li["BANDE_SUIVANTE"] is None
         else oui(li["BANDE_SUIVANTE"])}
        for li in b["lignes_issues"]])
    for nom, table in (("portefeuille.csv", b["valeurs"]), ("fantome.csv", b["valeurs_f"]),
                       ("mensuel.csv", b["valeurs_m"])):
        ecrire_csv(rep / nom, ENTETE_PORTEFEUILLE, [
            {"DATE": j, "ESPECES": round(table[j][0], 2), "TITRES": round(table[j][1], 2),
             "TOTAL": round(table[j][2], 2),
             "BASE100": round(100 * table[j][2] / b["dotation"], 4),
             "REFERENCE100": round(b["ref100"][j], 4), "LIGNES": table[j][3]}
            for j in b["seances"]])
    noms = [nom for nom, _l, _p in COMBINAISONS]
    ecrire_csv(rep / "combinaisons.csv", ["DATE", *noms, "APPARIEE", "REFERENCE100"], [
        {"DATE": j, **{n: round(100 * b["combinaisons"][n]["valeurs"][j][2] / DOTATION, 4)
                       for n in noms},
         "APPARIEE": round(b["appariee_par_jour"][j], 4),
         "REFERENCE100": round(b["ref100"][j], 4)}
        for j in b["seances"]])
    ecrire_csv(rep / "phases.csv", ["COMPARAISON", "PHASE", "NA", "NB", "DIFFERENCE", "SE",
                                    "G", "IC", "P", "EXCLUT_ZERO"], [
        {"COMPARAISON": cle, "PHASE": k, "NA": c["na"], "NB": c["nb"],
         "DIFFERENCE": arrondi(c["difference"], 4), "SE": arrondi(c["se"], 4), "G": c["G"],
         "IC": arrondi(c["ic"], 4), "P": arrondi(c["p"], 4),
         "EXCLUT_ZERO": oui(b["phases"][cle]["exclut"][k])}
        for cle, *_r in COMPARAISONS for k, c in enumerate(b["phases"][cle]["phases"])])
    ecrire_csv(rep / "temoin.csv", ["TIRAGE", "UNIVERS", "TOP10"], [
        {"TIRAGE": i + 1, "UNIVERS": round(u, 4), "TOP10": round(t, 4)}
        for i, (u, t) in enumerate(zip(b["temoins"]["UNIVERS"]["finaux"],
                                       b["temoins"]["TOP10"]["finaux"], strict=True))])


def analyser_arguments():
    ici = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description=f"Journal de l'experience 6 : {ANNEE}, dix lignes, achat persistant.")
    parser.add_argument("--figures", action="store_true",
                        help="Ecrire les figures de canal de l'annee narree")
    parser.add_argument("--markdown", action="store_true",
                        help="Ecrire les figures, les journaux mensuels et le bilan")
    parser.add_argument("--mois", help="N'afficher que ce mois (AAAA-MM)")
    parser.add_argument("--repertoire", type=Path, default=ici, help="Ou lire et ecrire")
    parser.add_argument("--quotes", type=Path, default=QUOTES_DEFAUT,
                        help="Ou sont les series")
    args = parser.parse_args()
    if args.mois and not (args.mois[:4] == ANNEE and len(args.mois) == 7
                          and "01" <= args.mois[5:] <= "12"):
        erreur(f"--mois doit etre un mois de {ANNEE}, au format AAAA-MM")
    if not args.quotes.is_dir():
        erreur(f"Repertoire introuvable : {args.quotes}")
    return args


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    args = analyser_arguments()
    ctx = construire_contexte(args)
    b = construire_bilan(ctx)
    ecrire_csvs(ctx, b)
    ecrits = ["evaluations.csv", "top10.csv", "ordres.csv", "signaux.csv", "issues.csv",
              "portefeuille.csv", "fantome.csv", "mensuel.csv", "combinaisons.csv",
              "phases.csv", "temoin.csv"]
    if args.figures or args.markdown:
        combien = ecrire_figures(ctx, b)
        ecrits.append(f"{combien} figures de canal")
    if args.markdown:
        textes = charger_textes(args.repertoire)
        ecrire_rapports(ctx, b, textes)
        ecrire_texte(args.repertoire / BILAN, bilan_annuel(ctx, b))
        ecrits += [f"{RAPPORTS}/{ANNEE}-MM.md", f"{GRAPHIQUES}/portefeuille-{ANNEE}-MM.svg",
                   BILAN]
    for mois in sorted({j[:7] for j in b["seances"]}):
        if not args.mois or args.mois == mois:
            print(bloc_mensuel(b, mois))
    imprimer_bilan(b)
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
