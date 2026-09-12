"""Moteur de l'experience 4 : 2022, une regle reduite a deux bandes, lue a chaque seance.

Lit l'univers quotidien de univers.csv, evalue chaque valeur a la cloture depuis
les colonnes glissantes de import_societe.py, forme le TOP 10 des taux de pente
sur 120 seances, achete sous le bord bas du canal a +/- 1 s quand la pente sur
20 seances monte, vend au-dessus du bord haut, execute a l'ouverture suivante,
comptabilise, confronte chaque element de la regle a son issue declaree,
recalcule les taux d'etalonnage publies, trace les figures et ecrit les journaux.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_4/journal.py
    python docs/done/experimentation/experience_4/journal.py --figures
    python docs/done/experimentation/experience_4/journal.py --markdown
    python docs/done/experimentation/experience_4/journal.py --mois 2022-03
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
TE_DECLAREE = 15.58
FRAIS_EXPERIENCE_3 = 75.24
Z95 = 1.96

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
    "DATE", "TICKER", "SOUS_ECHANTILLON", "TOP10", "SOUS_BAS", "AU_DESSUS_HAUT",
    "TAUX_20_POSITIF", "EXCES_20", "BANDE_SUIVANTE",
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


def simuler(ctx, avec_p20=True):
    """Rend (ordres, signaux, valeurs, journal, positions) pour une comptabilite."""
    args = ctx["args"]
    detenues, especes = {}, args.dotation
    ordres, signaux, valeurs, journal, registre = [], [], {}, {}, []

    for decision in ctx["jours_narres"]:
        execution = ctx["execution"][decision]
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

        creneaux = args.lignes - len(detenues)
        part = especes / creneaux if creneaux > 0 else 0.0
        candidats = sorted(
            (t for t in ctx["univers"][decision]
             if t not in detenues
             and est_candidat(evaluations[t], rangs.get(t), avec_p20=avec_p20)),
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
    echantillon = ctx["sous_echantillon"]
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
                "DATE": jour, "TICKER": ticker, "SOUS_ECHANTILLON": jour in echantillon,
                "TOP10": rang_t is not None and rang_t <= TOP,
                "SOUS_BAS": ev["ECART_S"] < -K, "AU_DESSUS_HAUT": ev["ECART_S"] > K,
                "TAUX_20_POSITIF": ev["TAUX_20"] > 0,
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
                       "jours_top_court", "jours_split_top"), 0)
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
    if ticker in ctx["univers"][jour] and est_candidat(ev, ctx["rangs"][jour].get(ticker)):
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
         f'Experience 4 &#8212; portefeuille contre {REFERENCE}, base 100 au {debut}</text>'),
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
            ("fantôme SANS-P20", [100 * b["valeurs_f"][j][2] / b["dotation"] for j in jours],
             "#8e6bb8", False),
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
        base_f = 100 * b["valeurs_f"][fin_mois][2] / b["dotation"]
        bloc = [
            f"# {MOIS_TITRE[mois[5:7]]} {ANNEE}", "",
            (f"> Journal de l'[expérience 4](../README.md) · exécutions du {premiere} "
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
            f"| Fantôme `SANS-P20`, même base | {fr(base_f)} |",
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
# Phase 8 bis : le bilan

# Les effectifs et effets minimaux detectables PROJETES au README, confrontes au bilan.
PROJECTIONS = {
    "TOP10": ("260 contre 747", 0.9), "CRITERE-2": ("84 contre 176", 1.7),
    "CRITERE-3": ("22 contre 62", 3.1), "VENTE": ("193 contre 814", 1.0),
}


def contient_zero(difference, ic):
    return difference is None or ic is None or abs(difference) <= ic


def verdict_intervalle(difference, ic):
    if difference is None or ic is None:
        return "*non mesurable*"
    return "contient zéro" if contient_zero(difference, ic) else "**exclut zéro**"


def section_compte(b):
    alpha = b["base"] - b["ref_fin"]
    qualite = ("*indiscernable de zéro*" if abs(alpha) <= b["mde"]
               else "*au-delà de l'effet minimal détectable d'un an*")
    lignes_fin = b["valeurs"][b["fin"]][3]
    out = [
        "## 1. Le compte", "", "| | |", "|---|---|",
        f"| Dotation | {fr(b['dotation'])} {EURO} au {b['debut']} |",
        f"| Valeur finale | **{fr(b['total'])} {EURO}** |",
        f"| Performance | **{signe(b['base'] - 100)} %** |",
        f"| {REFERENCE}, même convention | {signe(b['ref_fin'] - 100)} % |",
        f"| **Alpha sur l'année** | **{signe(alpha)} pt** — {qualite} |",
        (f"| Ordres | {len(b['ordres'])} ({b['achats']} achats, "
         f"{len(b['ordres']) - b['achats']} ventes) |"),
        (f"| Frais cumulés | {fr(b['frais'])} {EURO}, soit "
         f"{fr(100 * b['frais'] / b['dotation'])} % de la dotation — expérience 3 : "
         f"{fr(FRAIS_EXPERIENCE_3)} {EURO} |"),
        f"| Repli maximal | {signe(b['repli'])} %, creux au {b['creux']} |",
        f"| Espèces au {b['fin']} | {fr(b['especes_fin'])} {EURO} |",
        f"| Lignes détenues au {b['fin']} | {lignes_fin} |",
        f"| Part investie moyenne | {fr(b['part_investie'], 1)} % |",
        f"| Séances intégralement en espèces | {b['seances_vides']} / {len(b['seances'])} |",
        "", "## 2. Mois par mois", "",
        (f"| Mois | Valeur | Base 100 | Fantôme | {REFERENCE} | Alpha du mois "
         "| Alpha cumulé | Ordres |"),
        "|---|---|---|---|---|---|---|---|",
    ]
    fins = fins_de_mois(b["seances"])
    for mois in sorted(fins):
        fin, veille = fins[mois], fins.get(mois_precedent(mois))
        total = b["valeurs"][fin][2]
        base_p = b["valeurs"][veille][2] if veille else b["dotation"]
        base_r = b["ref100"][veille] if veille else 100.0
        alpha_mois = 100 * (total / base_p - b["ref100"][fin] / base_r)
        combien = sum(1 for o in b["ordres"] if o["DATE"][:7] == mois)
        out.append(
            f"| {MOIS_TITRE[mois[5:7]]} | [{fr(total)} {EURO}]({RAPPORTS}/{mois}.md) "
            f"| {fr(100 * total / b['dotation'])} "
            f"| {fr(100 * b['valeurs_f'][fin][2] / b['dotation'])} | {fr(b['ref100'][fin])} "
            f"| {signe(alpha_mois)} pt | {signe(100 * total / b['dotation'] - b['ref100'][fin])}"
            f" pt | {combien or '—'} |")
    return out


def section_positions(b):
    lignes = b["positions"]
    out = [
        "", "## 3. Les positions", "",
        (f"> Alpha d'une position : son rendement moins celui de {REFERENCE} sur **la même "
         "période de détention**. La contribution est nette des frais des deux sens. Le "
         "repli maximal se mesure du prix d'achat au plus bas atteint pendant la détention."),
        "",
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
    if lignes:
        gagnantes = sum(1 for p in lignes if p["euros"] > 0)
        out += ["", (f"**{gagnantes} positions sur {len(lignes)}** finissent en gain net de "
                     f"frais. La contribution la plus forte est "
                     f"{signe(max(p['euros'] for p in lignes))} {EURO}, la plus faible "
                     f"{signe(min(p['euros'] for p in lignes))} {EURO}.")]
    closes = [p for p in lignes if not p["ouverte"]]
    ouvertes = [p for p in lignes if p["ouverte"]]
    faute = b["par_sort"].get("FAUTE DE CRENEAU", [])
    out += [
        "", "## 4. Le motif unique de vente, mesuré", "",
        ("> Le [protocole](README.md#le-critère-de-vente--un-seul-motif) a déclaré avant la "
         "première séance qu'une ligne qui décroche peut ne jamais être vendue, et qu'on le "
         "mesurerait plutôt que de le corriger."),
        "", "| Mesure | Valeur |", "|---|---|",
        (f"| Positions closes | {len(closes)} — durée médiane "
         f"{fr(statistics.median(p['seances'] for p in closes), 0) if closes else '—'} séances, "
         f"maximale {max((p['seances'] for p in closes), default=0)} |"),
        f"| **Lignes jamais revendues** au {b['fin']} | **{len(ouvertes)}** |",
        (f"| Repli maximal le plus profond, en clôture | "
         f"{signe(min((p['repli_close'] for p in lignes), default=None))} % |"),
        (f"| Repli maximal le plus profond, sur `Low` | "
         f"{signe(min((p['repli_low'] for p in lignes), default=None))} % |"),
        (f"| Séances de silence — ligne détenue, évaluation muette | "
         f"{sum(p['silence'] for p in lignes)} |"),
        (f"| Séances où un candidat n'a pas trouvé de créneau | {b['jours_pleins']} "
         f"/ {len(b['seances'])} |"),
        f"| Signaux perdus faute de créneau | {len(faute)} |",
        (f"| Signaux annulés pour quantité nulle | "
         f"{len(b['par_sort'].get('QUANTITE NULLE', []))} |"),
    ]
    if ouvertes:
        out += ["", ("Les lignes encore détenues au dernier jour, avec leur plus ou "
                     "moins-value latente :"), ""]
        out += [f"- `{p['ticker']}` {SOCIETES[p['ticker']]}, achetée le {p['achat']} à "
                f"{fr(p['prix_achat'])} {EURO} : **{signe(p['pv'])} %** après {p['seances']} "
                "séances." for p in ouvertes]
    return out


def section_univers(ctx, b):
    n = b["narree"]
    out = ["", "## 5. L'univers et la recevabilité des données", "",
           ("> L'univers est la composition réelle de l'indice **à chaque séance**, lue dans "
            "[`univers.csv`](univers.csv) avec les dates exactes d'entrée et de sortie."), "",
           "| Valeur | Entrée dans l'indice | Sortie de l'indice | Évaluable dès |",
           "|---|---|---|---|"]
    for ligne in ctx["retenues"]:
        if ligne["ENTREE_INDICE"] or ligne["SORTIE_INDICE"] or ligne["EVALUABLE_DES"]:
            out.append(f"| `{ligne['TICKER']}` {SOCIETES[ligne['TICKER']]} "
                       f"| {ligne['ENTREE_INDICE'] or '—'} | {ligne['SORTIE_INDICE'] or '—'} "
                       f"| {ligne['EVALUABLE_DES'] or '—'} |")
    out += ["", "Les exclusions déclarées :", "", "| Valeur | Motif |", "|---|---|",
            *(f"| {ligne['NOM']} | {ligne['MOTIF']} |" for ligne in ctx["exclusions"]),
            "", "Les divisions postérieures à la fenêtre, et ce qu'elles ont coûté :", "",
            "| Valeur | Division rétro-appliquée |", "|---|---|",
            *(f"| `{t}` {SOCIETES[t]} | {motif} |" for t, motif in SPLITS_POSTERIEURS.items()),
            "",
            "| Mesure | 2022 |", "|---|---|",
            (f"| Séances où une valeur à division occupe une place du TOP 10 "
             f"| {n['jours_split_top']} / {n['jours']} |"),
            (f"| Signaux d'achat refusés pour division postérieure "
             f"| {len(b['par_sort'].get('REFUSE DIVISION', []))} |"),
            f"| Évaluations muettes | {n['muettes']} / {n['evaluations']} |",
            (f"| Séances où le TOP compte moins de {TOP} valeurs | {n['jours_top_court']} "
             f"/ {n['jours']} — {n['positifs_min']} pentes positives au minimum |"),
            "",
            ("> Un refus n'intervient ni dans le TOP 10, ni dans les signaux, ni dans les "
             "issues : c'est un contrôle de recevabilité des données, pas une condition de la "
             "règle.")]
    return out


def section_etalonnage(b):
    e, n, publie = b["etalonnage"], b["narree"], ETALONNAGE_PUBLIE
    ecarts = {cle for cle, _p, _v in ecarts_etalonnage(b)}

    def cellule(t, cle, base=None, decimales=None):
        v = t[cle]
        texte = fr(v, decimales) if decimales is not None else str(v)
        return f"{texte} — {pourcent(v, t[base])}" if base else texte

    lignes = [
        ("Évaluations", "evaluations", None, None),
        ("Évaluations muettes", "muettes", None, None),
        ("Pentes positives par séance, minimum", "positifs_min", None, None),
        ("… médiane", "positifs_mediane", None, 1),
        ("… maximum", "positifs_max", None, None),
        ("Entrants dans le TOP 10 par séance", "entrants_moyenne", None, 2),
        ("Séances à au moins un entrant", "jours_entrant", "transitions", None),
        ("Clôtures sous le bord bas, univers", "sous_bas", "evaluations", None),
        ("Clôtures au-dessus du bord haut, univers", "au_dessus", "evaluations", None),
        ("Clôtures dans la bande, univers", "dans_bande", "evaluations", None),
        ("Places du TOP 10", "places_top", None, None),
        ("Places du TOP 10 sous le bord bas", "top_sous_bas", "places_top", None),
        ("Places du TOP 10 au-dessus du bord haut", "top_au_dessus", "places_top", None),
        ("Évaluations candidates", "candidats", None, None),
        ("… sous le bord bas, pente courte ≤ 0", "sous_bas_pente_negative", None, None),
        ("Séances à au moins un candidat", "jours_candidat", "jours", None),
        ("Clôture suivante dans la bande prolongée", "bande_suivante", "bande_total", None),
        ("… issues tranchées", "bande_total", None, None),
        ("Écart-type d'`EXCES_20`, quotidien (pt)", "sd_quotidien", None, 2),
        ("… sous-échantillon (pt)", "sd_echantillon", None, 2),
    ]
    out = ["", "## 6. Les taux d'étalonnage, publiés avant, recalculés après", "",
           ("> Le [README](README.md#les-taux-détalonnage--publiés-avant-la-première-séance) a "
            "publié ces nombres avant la première séance, calculés sur 2021 sans aucune séance "
            "postérieure au 2021-12-30. Le moteur les recalcule sous la même convention. "
            "**Un écart est une erreur, du moteur ou du README.**"), "",
           "| Mesure | README | Moteur, 2021 | Concorde | 2022 |", "|---|---|---|---|---|"]
    for libelle, cle, base, decimales in lignes:
        valeur_publiee = publie.get(cle)
        texte_publie = ("—" if valeur_publiee is None else
                        fr(valeur_publiee, 2) if isinstance(valeur_publiee, float)
                        else str(valeur_publiee))
        concorde = "—" if cle not in publie else ("✗" if cle in ecarts else "✓")
        out.append(f"| {libelle} | {texte_publie} | {cellule(e, cle, base, decimales)} "
                   f"| {concorde} | {cellule(n, cle, base, decimales)} |")
    out += ["", (f"**{len(publie) - len(ecarts)} nombres publiés sur {len(publie)}** sont "
                 "retrouvés à l'identique." + ("" if not ecarts else
                                               " Les autres sont marqués ✗, et le README "
                                               "n'est pas corrigé après coup."))]
    return out


def section_issues(b):
    out = ["", "## 7. Chaque élément de la règle, contre l'issue déclarée d'avance", "",
           ("> Une seule issue pour tous : le **rendement excédentaire sur 20 séances contre "
            f"`{REFERENCE}`**, de la clôture de la décision à celle de la vingtième séance "
            "suivante. Le README a projeté les effectifs et les effets minimaux détectables "
            "**avant** la première séance."), "",
           "### Sur le sous-échantillon d'audit — une séance sur vingt, *fait foi*", "",
           ("| Élément | Groupe testé | Témoin | Effectifs projetés | Effectifs | Moyenne testée "
            "| Moyenne témoin | Différence | IC95 | EMD projeté | Verdict |"),
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for cle, libelle, _pop, groupe_a, groupe_b, _p, _g in COMPARAISONS:
        c = b["comparaisons"][cle]["echantillon"]
        projete, emd = PROJECTIONS[cle]
        out.append(f"| {libelle} | {groupe_a} | {groupe_b} | {projete} "
                   f"| {c['na']} contre {c['nb']} | {signe(c['moy_a'])} pt "
                   f"| {signe(c['moy_b'])} pt | **{signe(c['difference'])} pt** "
                   f"| ± {fr(c['ic'])} pt | ± {fr(emd, 1)} pt "
                   f"| {verdict_intervalle(c['difference'], c['ic'])} |")
    # VENTE porte sur tout l'univers : ses non tranchees sont celles du sous-echantillon.
    non_tranchees = b["comparaisons"]["VENTE"]["echantillon"]["non_tranchees"]
    out += ["", (f"{non_tranchees} évaluations du sous-échantillon ont un horizon qui dépasse "
                 f"le {FIN_SERIE} : elles sont **non tranchées** et hors des moyennes."), "",
            "### Sur toutes les séances d'audit — *borne inférieure de l'incertitude*", "",
            ("> Deux évaluations d'une même valeur à un jour d'écart partagent 119 clôtures "
             "sur 120 : ces intervalles sont faussement étroits, et publiés pour qu'on voie "
             "l'écart."), "",
            "| Élément | Effectifs | Différence | IC95 apparent | Verdict apparent |",
            "|---|---|---|---|---|"]
    for cle, libelle, *_reste in COMPARAISONS:
        c = b["comparaisons"][cle]["quotidien"]
        out.append(f"| {libelle} | {c['na']} contre {c['nb']} | {signe(c['difference'])} pt "
                   f"| ± {fr(c['ic'])} pt | {verdict_intervalle(c['difference'], c['ic'])} |")
    out += ["", "### L'énoncé `BANDE` — la bande prolongée contient-elle la clôture suivante ?",
            "", "| Ensemble | Dans la bande | Taux | IC95 | Nominal |", "|---|---|---|---|---|"]
    for libelle, (dans, total) in (("Sous-échantillon d'audit", b["bande_echantillon"]),
                                   ("Toutes les séances d'audit", b["bande_quotidien"])):
        out.append(f"| {libelle} | {dans} / {total} | **{pourcent(dans, total)}** "
                   f"| ± {fr(ic95(dans, total), 1)} pt | 68,3 % |")
    return out


def section_fantome_et_experience_3(b):
    reg, reg_3 = b["regression"], b["regression_3"]
    ecart_3 = b["base"] - b["base_3"]
    return [
        "", "## 8. Le fantôme `SANS-P20` — ce que change le critère 3", "",
        ("> La même règle, **sans la condition de pente courte positive**, sur les mêmes "
         "séances, avec les mêmes coûts et les mêmes créneaux. Elle n'engage pas un euro."), "",
        f"| | Base 100 au {b['fin']} | Performance | Ordres | Frais | Part investie |",
        "|---|---|---|---|---|---|",
        (f"| **Le portefeuille** | **{fr(b['base'])}** | {signe(b['base'] - 100)} % "
         f"| {len(b['ordres'])} | {fr(b['frais'])} {EURO} | {fr(b['part_investie'], 1)} % |"),
        (f"| Le fantôme `SANS-P20` | {fr(b['base_f'])} | {signe(b['base_f'] - 100)} % "
         f"| {len(b['ordres_f'])} | {fr(b['frais_f'])} {EURO} "
         f"| {fr(b['part_investie_f'], 1)} % |"),
        "",
        (f"L'écart vaut **{signe(b['base'] - b['base_f'])} point** sur l'année, pour un "
         f"écart-type annualisé de la différence de {fr(b['te_f'])} %/an, soit un effet minimal "
         f"détectable de ± {fr(b['mde_f'], 1)} points : l'écart "
         f"{'est plus petit que' if abs(b['base'] - b['base_f']) <= b['mde_f'] else 'dépasse'}"
         " son effet minimal détectable."),
        "", "## 9. La comparaison appariée avec l'expérience 3", "",
        ("> Même année, même univers, même référence, mêmes coûts, même dotation, même plafond "
         "de cinq lignes. **Une seule chose change : la règle, et sa cadence.**"), "",
        f"| | Base 100 au {b['fin']} | Part investie | Bêta | Alpha de régression |",
        "|---|---|---|---|---|",
        (f"| **Expérience 4** | **{fr(b['base'])}** | {fr(b['part_investie'], 1)} % "
         f"| {fr(reg['beta'], 3)} | {signe(reg['alpha'])} %/an ± {fr(reg['ic_alpha'], 1)} |"),
        (f"| [Expérience 3](../experience_3/bilan-2022.md) | {fr(b['base_3'])} "
         f"| {fr(b['part_investie_3'], 1)} % | {fr(reg_3['beta'], 3)} "
         f"| {signe(reg_3['alpha'])} %/an ± {fr(reg_3['ic_alpha'], 1)} |"),
        "",
        (f"L'écart apparié vaut **{signe(ecart_3)} point**. L'écart-type annualisé de la "
         f"différence quotidienne est de {fr(b['te_3'])} %/an, soit un effet minimal détectable "
         f"de ± {fr(b['mde_3'], 1)} points : l'écart "
         f"{'est plus petit que' if abs(ecart_3) <= b['mde_3'] else 'dépasse'} son effet "
         "minimal détectable."),
        "",
        ("> Deux règles de même exposition se comparent par leur différence. Deux règles "
         "d'expositions différentes se comparent d'abord par leur bêta : un écart de "
         "performance dans une année qui baisse récompense mécaniquement la moins exposée."),
    ]


def section_sensibilite_conventions(b):
    out = ["", "## 10. La sensibilité aux paramètres — mesurée, pas arbitrée", "",
           ("> Quatre variantes déclarées avant la première séance. Aucun euro, aucun ordre "
            "n'en dépend."), "",
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
        "", "## 11. Les trois conventions", "",
        (f"> ⚠️ `Close` est **ajustée des dividendes**, `{REFERENCE_NUE}` ne l'est pas. "
         "Comparer les deux fabrique de l'alpha à partir de rien."), "",
        f"| Série | Convention | {ANNEE} | Alpha du portefeuille |", "|---|---|---|---|",
        f"| Le portefeuille | rendement total | **{signe(b['base'] - 100)} %** | — |",
        (f"| `{REFERENCE}` | rendement total | {signe(b['ref_fin'] - 100)} % "
         f"| **{signe(b['base'] - b['ref_fin'])} pt** |"),
        (f"| `{REFERENCE_NUE}` | indice **nu** | {signe(b['nue'])} % "
         f"| {signe(b['base'] - 100 - b['nue'])} pt |"),
    ]
    return out


def section_dimensionnement(b):
    reg = b["regression"]
    alpha = b["base"] - b["ref_fin"]
    return [
        "", "## 12. Le dimensionnement, confronté", "",
        "| | Déclaré avant | Réalisé |", "|---|---|---|",
        f"| Tracking error annualisée | {fr(TE_DECLAREE)} %/an | **{fr(b['te'])} %/an** |",
        (f"| Effet minimal détectable sur un an | ± {fr(Z95 * TE_DECLAREE, 1)} pt "
         f"| **± {fr(b['mde'], 1)} pt** |"),
        f"| Alpha mesuré, écart de performance | — | {signe(alpha)} pt |",
        "", "### L'alpha de régression", "", "| | |", "|---|---|",
        f"| Bêta contre `{REFERENCE}` | **{fr(reg['beta'], 3)}** |",
        f"| Alpha de régression, annualisé | **{signe(reg['alpha'])} %/an** |",
        f"| IC95 de cet alpha | ± {fr(reg['ic_alpha'], 1)} pt |",
        f"| Coefficient de détermination R² | {fr(reg['r2'], 3)} |",
        f"| Écart-type du résidu, annualisé | {fr(reg['sigma_residu'])} %/an |",
        f"| Part investie moyenne | {fr(b['part_investie'], 1)} % |",
        "",
        (f"L'écart de performance vaut {signe(alpha)} point pour un effet minimal détectable de "
         f"± {fr(b['mde'], 1)} ; l'alpha de régression vaut {signe(reg['alpha'])} %/an, IC95 "
         f"± {fr(reg['ic_alpha'], 1)}, qui "
         f"{'contient' if contient_zero(reg['alpha'], reg['ic_alpha']) else 'exclut'} zéro."),
    ]


def section_conclusion(b):
    separes = [libelle for cle, libelle, *_r in COMPARAISONS
               if not contient_zero(b["comparaisons"][cle]["echantillon"]["difference"],
                                    b["comparaisons"][cle]["echantillon"]["ic"])]
    plats = [libelle for cle, libelle, *_r in COMPARAISONS if libelle not in separes]
    dans, total = b["bande_echantillon"]
    alpha = b["base"] - b["ref_fin"]
    retrouves = ("sont retrouvés à l'identique" if not ecarts_etalonnage(b)
                 else "ne sont retrouvés qu'en partie")
    etablit = [
        f"- que les taux publiés avant la première séance {retrouves} par le moteur — § 6 ;",
        (f"- que la bande ± {fr(K, 1)} s contient la clôture suivante dans "
         f"**{pourcent(dans, total)}** des cas, ± {fr(ic95(dans, total), 1)} pt, contre 68,3 % "
         "nominal — § 7 ;"),
        ("- **quels éléments de la règle séparent leur issue sur le sous-échantillon** : "
         + (", ".join(separes) if separes else "aucun") + " ; et lesquels ne la séparent pas : "
         + (", ".join(plats) if plats else "aucun") + " — § 7 ;"),
        ("- ce que coûte le motif unique de vente, en lignes jamais revendues, en replis et en "
         "signaux perdus faute de créneau — § 4 ;"),
        "- de combien la règle diffère de celle de l'expérience 3, à exposition mesurée — § 9.",
    ]
    return [
        "", "## 13. Ce que l'expérience établit, et ce qu'elle n'établit pas", "",
        "**Elle établit**, avec les incertitudes publiées :", "", *etablit, "",
        "**Elle n'établit pas** :", "",
        (f"- que la règle est bonne ou mauvaise. L'écart de performance, {signe(alpha)} point, "
         + (f"est plus petit que son effet minimal détectable de ± {fr(b['mde'], 1)} points ;"
            if abs(alpha) <= b["mde"] else
            f"dépasse son effet minimal détectable de ± {fr(b['mde'], 1)} points, mais la règle "
            "a été formulée après avoir vu 2022 : sa performance sur cette année est de "
            "catégorie B, et ne vaut pas preuve ;")),
        ("- qu'un élément qui sépare son issue sur 2021 et 2022 la séparera ailleurs : deux "
         "années, un indice, un régime ;"),
        "- quoi que ce soit sur 2023. Aucune quantité mesurée ici ne se prolonge.",
        "", "---", "",
        (f"[← Protocole](README.md) · [Décembre]({RAPPORTS}/{ANNEE}-12.md) · "
         f"[Janvier]({RAPPORTS}/{ANNEE}-01.md) · [L'expérience 3](../experience_3/bilan-2022.md)"),
    ]


def bilan_annuel(ctx, b):
    out = [
        f"# Bilan de l'année {ANNEE}", "",
        (f"> [Expérience 4](README.md) · dotation {fr(b['dotation'])} {EURO} au {b['debut']}, "
         f"arrêt au {b['fin']} · **{signe(b['base'] - 100)} %** contre "
         f"**{signe(b['ref_fin'] - 100)} %** pour {REFERENCE}"), "",
        ("> ⚠️ **L'alpha de cette ligne ne tranche rien**, et le "
         "[protocole](README.md#le-dimensionnement-publié-avant-la-première-séance) le "
         "déclarait avant la première séance : la règle a été formulée après avoir vu 2022. "
         "Ce que ce bilan établit est dans les sections 4 à 10."), "", "---", "",
        *section_compte(b), *section_positions(b), *section_univers(ctx, b),
        *section_etalonnage(b), *section_issues(b), *section_fantome_et_experience_3(b),
        *section_sensibilite_conventions(b), *section_dimensionnement(b),
        *section_conclusion(b),
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
    jours_evalues = [*jours_audit, FIN_SERIE]
    evaluations = {j: {t: evaluer(series[t], t, j) for t in tickers} for j in jours_evalues}
    univers = {j: univers_du_jour(retenues, j) for j in jours_evalues}
    return {
        "args": args, "tickers": tickers, "retenues": retenues, "exclusions": exclusions,
        "series": series, "reference": reference, "nue": nue,
        "jours_audit": jours_audit, "jours_etalonnage": jours_etalonnage,
        "jours_narres": jours_narres, "jours_evalues": jours_evalues,
        "execution": {j: calendrier[reference["rang"][j] + 1] for j in jours_audit},
        "evaluations": evaluations, "univers": univers,
        "rangs": {j: classer(evaluations[j], univers[j]) for j in jours_evalues},
        "sous_echantillon": set(jours_audit[::PAS_ECHANTILLON]),
    }


def construire_bilan(ctx, simulation, simulation_f, experience_3):
    """Rassemble tout ce que le bilan et la console publient."""
    args = ctx["args"]
    ordres, signaux, valeurs, journal, registre = simulation
    ordres_f, _signaux_f, valeurs_f, _journal_f, registre_f = simulation_f
    seances = [ctx["execution"][d] for d in ctx["jours_narres"]]
    debut, fin = seances[0], seances[-1]
    ref = ctx["reference"]["par_jour"]
    ref100 = {j: 100 * ref[j]["close"] / ref[debut]["close"] for j in seances}
    base = [100 * valeurs[j][2] / args.dotation for j in seances]
    base_f = [100 * valeurs_f[j][2] / args.dotation for j in seances]
    base_3 = [100 * experience_3[j][1] / args.dotation for j in seances]
    indice = [ref100[j] for j in seances]

    pic, repli, creux = -1e18, 0.0, fin
    for jour in seances:
        pic = max(pic, valeurs[jour][2])
        if valeurs[jour][2] / pic - 1 < repli:
            repli, creux = valeurs[jour][2] / pic - 1, jour

    lignes = issues(ctx, ctx["jours_audit"], FIN_SERIE)
    echantillon = [li for li in lignes if li["SOUS_ECHANTILLON"]]
    comparaisons = {
        cle: {"echantillon": comparer(echantillon, population, groupe),
              "quotidien": comparer(lignes, population, groupe)}
        for cle, _l, _p, _a, _b, population, groupe in COMPARAISONS}
    part, vides = exposition(valeurs, seances)
    part_f, _ = exposition(valeurs_f, seances)
    nue = ctx["nue"]["par_jour"]
    par_sort = {}
    for signal in signaux:
        par_sort.setdefault(signal["SORT"], []).append(signal)
    te = ecart_type_ecarts(base, indice)
    te_f = ecart_type_ecarts(base, base_f)
    te_3 = ecart_type_ecarts(base, base_3)
    return {
        "dotation": args.dotation, "debut": debut, "fin": fin, "seances": seances,
        "valeurs": valeurs, "valeurs_f": valeurs_f, "ref100": ref100,
        "experience_3": experience_3,
        "ordres": ordres, "ordres_f": ordres_f, "signaux": signaux, "journal": journal,
        "total": valeurs[fin][2], "base": base[-1], "base_f": base_f[-1],
        "base_3": base_3[-1], "ref_fin": ref100[fin],
        "nue": 100 * (nue[fin]["close"] / nue[debut]["close"] - 1),
        "achats": sum(1 for o in ordres if o["SENS"] == "ACHAT"),
        "frais": sum(o["FRAIS"] for o in ordres),
        "frais_f": sum(o["FRAIS"] for o in ordres_f),
        "repli": 100 * repli, "creux": creux, "especes_fin": valeurs[fin][0],
        "part_investie": part, "part_investie_f": part_f, "seances_vides": vides,
        "part_investie_3": statistics.fmean(
            100 * experience_3[j][0] / experience_3[j][1] for j in seances),
        "positions": positions_annee(ctx, registre, fin),
        "positions_f": positions_annee(ctx, registre_f, fin),
        "par_sort": par_sort,
        "jours_pleins": len({s["DATE_DECISION"]
                             for s in par_sort.get("FAUTE DE CRENEAU", [])}),
        "lignes_issues": lignes, "comparaisons": comparaisons,
        "bande_echantillon": bande(echantillon), "bande_quotidien": bande(lignes),
        "etalonnage": taux_regle(ctx, ctx["jours_etalonnage"], ctx["jours_etalonnage"][-1]),
        "narree": taux_regle(ctx, ctx["jours_narres"], FIN_SERIE),
        "sensibilite": sensibilite(ctx),
        "te": te, "mde": None if te is None else Z95 * te,
        "te_f": te_f, "mde_f": None if te_f is None else Z95 * te_f,
        "te_3": te_3, "mde_3": None if te_3 is None else Z95 * te_3,
        "regression": regression(base, indice),
        "regression_3": regression(base_3, indice),
    }


def ecarts_etalonnage(b):
    """Les nombres du README que le moteur ne retrouve pas."""
    recalcul = b["etalonnage"]
    ecarts = []
    for cle, publie in ETALONNAGE_PUBLIE.items():
        valeur = recalcul[cle]
        if isinstance(publie, float):
            decimales = len(str(publie).split(".")[1])
            identique = valeur is not None and round(valeur, decimales) == publie
        else:
            identique = valeur == publie
        if not identique:
            ecarts.append((cle, publie, valeur))
    return ecarts


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
    decisions = {d for d, e in ((d, b["journal"][d]["execution"]) for d in b["journal"])
                 if e[:7] == mois}
    perdus = [s for s in b["signaux"] if s["DATE_DECISION"] in decisions
              and s["SORT"] != "EXECUTE"]
    for s in perdus:
        lignes.append(f"  non execute {s['DATE_DECISION']} {s['TICKER']:<9s} "
                      f"rang {s['RANG']:2d} {MEDIAN} {s['SORT']}")
    especes, _titres, total, nombre = b["valeurs"][fin_mois]
    lignes += ["", (f"Portefeuille au {fin_mois} : {fr(total)} EUR ({nombre} lignes, "
                    f"especes {fr(especes)}) {MEDIAN} base "
                    f"{fr(100 * total / b['dotation'])} {MEDIAN} {REFERENCE} "
                    f"{fr(b['ref100'][fin_mois])}")]
    return NL_.join(lignes)


def imprimer_bilan(b):
    reg = b["regression"]
    ouvertes = [p for p in b["positions"] if p["ouverte"]]
    print(f"""
=== Bilan au {b['fin']} ===

  Dotation                {fr(b['dotation'])} EUR au {b['debut']}
  Valeur finale           {fr(b['total'])} EUR
  Performance             {signe(b['base'] - 100)} %
  {REFERENCE}                    {signe(b['ref_fin'] - 100)} %
  Alpha sur l'annee       {signe(b['base'] - b['ref_fin'])} pt (MDE +/- {fr(b['mde'], 1)} pt)
  Alpha de regression     {signe(reg['alpha'])} %/an (beta {fr(reg['beta'], 3)}, \
IC95 +/- {fr(reg['ic_alpha'], 1)} pt)
  Part investie moyenne   {fr(b['part_investie'], 1)} % {MEDIAN} \
{b['seances_vides']} seances en especes
  Fantome SANS-P20        {fr(b['base_f'])} base 100 {MEDIAN} {len(b['ordres_f'])} ordres
  Experience 3            {fr(b['base_3'])} base 100 {MEDIAN} ecart apparie \
{signe(b['base'] - b['base_3'])} pt (MDE +/- {fr(b['mde_3'], 1)} pt)
  Ordres                  {len(b['ordres'])} ({b['achats']} achats, \
{len(b['ordres']) - b['achats']} ventes) {MEDIAN} frais {fr(b['frais'])} EUR
  Lignes jamais revendues {len(ouvertes)} / {len(b['positions'])}
  Signaux faute de creneau {len(b['par_sort'].get('FAUTE DE CRENEAU', []))} \
sur {b['jours_pleins']} seances {MEDIAN} refuses division \
{len(b['par_sort'].get('REFUSE DIVISION', []))}""")
    print("  Issues, sous-echantillon :")
    for cle, _libelle, _p, _a, _b, _pop, _grp in COMPARAISONS:
        c = b["comparaisons"][cle]["echantillon"]
        print(f"    {cle:<10s} {c['na']:4d} contre {c['nb']:4d} {MEDIAN} difference "
              f"{signe(c['difference'])} pt +/- {fr(c['ic'])}")
    dans, total = b["bande_echantillon"]
    print(f"    BANDE      {dans} / {total} = {pourcent(dans, total)}")
    for cle, publie, valeur in ecarts_etalonnage(b):
        print(f"  ECART ETALONNAGE {cle} : README {publie}, moteur {valeur}")
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
                ligne["CANDIDAT"] = oui(ticker in univers
                                        and est_candidat(ev, rangs.get(ticker)))
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
                           "CANDIDAT": oui(est_candidat(ev, rangs[ticker]))})
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
                                    "AU_DESSUS_HAUT", "TAUX_20_POSITIF")},
         "BANDE_SUIVANTE": None if li["BANDE_SUIVANTE"] is None
         else oui(li["BANDE_SUIVANTE"])}
        for li in b["lignes_issues"]])
    for nom, table in (("portefeuille.csv", b["valeurs"]), ("fantome.csv", b["valeurs_f"])):
        ecrire_csv(rep / nom, ENTETE_PORTEFEUILLE, [
            {"DATE": j, "ESPECES": round(table[j][0], 2), "TITRES": round(table[j][1], 2),
             "TOTAL": round(table[j][2], 2),
             "BASE100": round(100 * table[j][2] / b["dotation"], 4),
             "REFERENCE100": round(b["ref100"][j], 4), "LIGNES": table[j][3]}
            for j in b["seances"]])


def analyser_arguments():
    ici = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description=f"Journal de l'experience 4 : 10 000 EUR sur {ANNEE}, tout le CAC 40, "
                    "une decision par seance.")
    parser.add_argument("--figures", action="store_true",
                        help="Ecrire les figures de canal de l'annee narree")
    parser.add_argument("--markdown", action="store_true",
                        help="Ecrire les figures, les journaux mensuels et le bilan")
    parser.add_argument("--mois", help="N'afficher que ce mois (AAAA-MM)")
    parser.add_argument("--repertoire", type=Path, default=ici, help="Ou lire et ecrire")
    parser.add_argument("--quotes", type=Path, default=QUOTES_DEFAUT,
                        help="Ou sont les series")
    parser.add_argument("--dotation", type=float, default=10000.0, help="Dotation en euros")
    parser.add_argument("--lignes", type=int, default=5, help="Lignes detenues au maximum")
    args = parser.parse_args()
    if args.dotation <= 0:
        erreur("--dotation doit etre strictement positive")
    if not 1 <= args.lignes <= 39:
        erreur("--lignes doit etre entre 1 et 39")
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
    simulation = simuler(ctx, avec_p20=True)
    simulation_f = simuler(ctx, avec_p20=False)
    seances = [ctx["execution"][d] for d in ctx["jours_narres"]]
    b = construire_bilan(ctx, simulation, simulation_f,
                         charger_experience_3(args.repertoire, seances))
    ecrire_csvs(ctx, b)
    ecrits = ["evaluations.csv", "top10.csv", "ordres.csv", "signaux.csv", "issues.csv",
              "portefeuille.csv", "fantome.csv"]
    if args.figures or args.markdown:
        combien = ecrire_figures(ctx, b)
        ecrits.append(f"{combien} figures de canal")
    if args.markdown:
        textes = charger_textes(args.repertoire)
        ecrire_rapports(ctx, b, textes)
        ecrire_texte(args.repertoire / BILAN, bilan_annuel(ctx, b))
        ecrits += [f"{RAPPORTS}/{ANNEE}-MM.md", f"{GRAPHIQUES}/portefeuille-{ANNEE}-MM.svg",
                   BILAN]
    for mois in sorted({j[:7] for j in seances}):
        if not args.mois or args.mois == mois:
            print(bloc_mensuel(b, mois))
    imprimer_bilan(b)
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
