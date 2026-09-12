"""Moteur de l'experience 10 : les six regles de l'experience 9, plus une coupe a -15 %.

Dix valeurs tirees au sort dans le CAC 40 du 2019-01-02 avec la graine 10. La
regle 7 vend des que le repli depuis le PRIX DE LA PREMIERE TRANCHE atteint -15 %,
constate a chaque cloture quotidienne, avec quatre semaines de carence ensuite.

Convention d'unites : la REGLE se lit sur la serie AJUSTEE, les QUANTITES, les
especes et la valorisation sur les cours REELS.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_10/journal.py
    python docs/done/experimentation/experience_10/journal.py --figures
    python docs/done/experimentation/experience_10/journal.py --markdown
    python docs/done/experimentation/experience_10/journal.py --annee 2023
"""

import argparse
import bisect
import csv
import datetime
import math
import random
import statistics
import sys
from pathlib import Path

VALEURS = ("ENGI.PA", "AC.PA", "EN.PA", "TTE.PA", "SAF.PA",
           "AIR.PA", "PUB.PA", "SGO.PA", "MC.PA", "CAP.PA")
EXEMPTES_TTF = frozenset({"AIR.PA"})        # Airbus SE, societe neerlandaise
QUOTES_DEFAUT = Path("docs/raw/data/quotes")
UNIVERS = "univers.csv"
RAPPORTS = "rapports"
GRAPHIQUES = "graphiques"
BILAN = "bilan.md"
DECISIONS_EXP_9 = Path("docs/done/experimentation/experience_9/decisions.csv")
COMMUNES_EXP_9 = ("ENGI.PA", "SAF.PA")

GRAINE = 10
DOTATION = 10000.0
PART_ACHAT, PART_RENFORT = 0.10, 0.20
PLAFOND = 1.0
REPLI_R7 = -0.15
CARENCE = 4
DEBUT_NARREE = "2022-01-03"
FIN_ETALONNAGE = "2021-12-31"
LONGUE, COURTE, K = 120, 20, 1.0
HORIZON, PAS_ECHANTILLON = 20, 4
COURTAGE, SPREAD, TTF = 0.10, 0.015, 0.30
Z95 = 1.96
TOLERANCE_REPRODUCTION = 5e-4

VARIANTES = (("declaree", True, True, True), ("sans regle 7", True, True, False),
             ("sans regle 4", False, True, True), ("sans regle 6", True, False, True),
             ("ni regle 4 ni regle 6", False, False, True))
LIBELLE_VARIANTE = {"declaree": "**Déclarée** — règles 4, 6 et 7",
                    "sans regle 7": "**Sans la règle 7** — la règle de l'expérience 9",
                    "sans regle 4": "Sans la règle 4",
                    "sans regle 6": "Sans la règle 6",
                    "ni regle 4 ni regle 6": "Ni la règle 4 ni la 6"}

# Le CAC 40 au 2019-01-02, servi par bnains.org/archives/histocac/compocac.php.
# Il ne sert qu'a rejouer la permutation et a la confronter a univers.csv.
CAC_2019 = (
    "FR0000120404", "FR0000120073", "NL0000235190", "LU0323134006", "FR0000051732",
    "FR0000120628", "FR0000131104", "FR0000120503", "FR0000125338", "FR0000120172",
    "FR0000045072", "FR0000120644", "FR0000130650", "FR0010208488", "FR0000121667",
    "FR0000052292", "FR0000121485", "FR0000120321", "FR0010307819", "FR0000121014",
    "FR0000121261", "FR0000133308", "FR0000120693", "FR0000121501", "FR0000130577",
    "FR0000131906", "FR0000073272", "FR0000125007", "FR0000120578", "FR0000121972",
    "FR0000130809", "FR0000121220", "NL0000226223", "FR0000131708", "FR0000120271",
    "FR0000124711", "FR0000130338", "FR0000124141", "FR0000125486", "FR0000127771",
)
RANGS_EXAMINES = tuple(range(1, 14))

# Les nombres publies au README avant la fenetre jouee, confrontes au recalcul.
ETALONNAGE_PUBLIE = {
    "declaree": {"base": 126.01, "detention": 130.39, "appariee": 113.63, "alpha": 12.37,
                 "ordres": 76, "frais": 268.1, "part": 26.2, "maximum": 99.9},
    "sans regle 7": {"base": 123.01, "detention": 130.39, "appariee": 115.25, "alpha": 7.77,
                     "ordres": 75, "frais": 257.8, "part": 33.84, "maximum": 100.0},
    "sans regle 4": {"base": 119.09, "detention": 130.39, "appariee": 111.47, "alpha": 7.62,
                     "ordres": 61, "frais": 196.95, "part": 21.7, "maximum": 94.7},
    "sans regle 6": {"base": 120.9, "detention": 130.39, "appariee": 111.03, "alpha": 9.87,
                     "ordres": 71, "frais": 219.83, "part": 21.87, "maximum": 77.5},
    "ni regle 4 ni regle 6": {"base": 112.72, "detention": 130.39, "appariee": 106.17,
                              "alpha": 6.55, "ordres": 56, "frais": 142.41, "part": 16.93,
                              "maximum": 57.0},
    "taux": {"decisions": 133, "evaluations": 1330, "sous_bas": 309, "sous_bas_pente": 58,
             "au_dessus": 289, "r4_possible": 15, "r6_possible": 5, "meme_semaine": 0,
             "refus_especes": 0, "r7_declenchee": 5, "r7_et_r4": 1, "carence_bloquee": 1,
             "positions": 29, "closes": 27, "coupes": 5, "te_app": 4.1, "te_det": 23.62},
}

# Les cinq coupes de l'etalonnage, avec ce que le meme achat devenait sans la regle 7.
COUPES_PUBLIEES = (
    ("TTE.PA", "2020-01-20", "2020-02-26", -14.64, "2020-05-25", -29.37),
    ("MC.PA", "2020-02-24", "2020-03-13", -17.69, "2020-05-25", -6.99),
    ("EN.PA", "2020-03-02", "2020-03-11", -10.78, "2020-06-01", -17.32),
    ("ENGI.PA", "2020-03-02", "2020-03-12", -21.25, "2020-06-01", -12.54),
    ("CAP.PA", "2020-09-07", "2020-10-27", -9.30, "2020-12-21", 2.67),
)

COLONNES = ("Open", "High", "Low", "Close", "E_120", "VAR_120", "CORR_120", "VAL_120",
            "E_20", "VAR_20", "CORR_20", "VAL_20")
ENTETE_DECISIONS = ["DATE", "TICKER", "EXECUTION", "CLOSE_AJUSTE", "CLOSE_REEL", "VAL_120",
                    "S_120", "ECART_S", "TAUX_120", "TAUX_20", "SOUS_BAS", "AU_DESSUS",
                    "SEUIL_4_FRANCHI", "SEUIL_7_FRANCHI", "REPLI_COURANT", "EN_CARENCE",
                    "SIGNAL"]
ENTETE_ORDRES = ["DATE", "DATE_DECISION", "TICKER", "SENS", "RANG_SERVICE", "QUANTITE",
                 "PRIX_REEL", "BRUT", "FRAIS", "NET", "ECART_S", "TAUX_20", "MOTIF"]
ENTETE_POSITIONS = ["TICKER", "ACHAT", "SORTIE", "MOTIF", "TRANCHES", "QUANTITE",
                    "PRIX_PREMIERE_TRANCHE", "PRIX_ACHAT", "PRIX_SORTIE", "SEUIL_REGLE_4",
                    "SEUIL_REGLE_7", "SEANCES", "PLUS_VALUE", "REPLI_PREMIERE",
                    "REPLI_MOYEN", "REPLI_LOW", "CONTRIBUTION"]
ENTETE_PORTEFEUILLE = ["DATE", "ESPECES", "TITRES", "TOTAL", "BASE100", "APPARIEE100",
                       "DETENTION100", "PART_INVESTIE", "LIGNES_OUVERTES"]
ENTETE_ISSUES = ["DATE", "TICKER", "SOUS_BAS", "TAUX_20_POSITIF", "AU_DESSUS_HAUT",
                 "REPLI_SOUS_SEUIL", "SOUS_ECHANTILLON", "RENDEMENT_20"]

NBSP = " "
NL_ = chr(10)
EURO = "€"
MEDIAN = "·"
_OUTILS = {}


def erreur(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def fr(x, decimales=2):
    if x is None:
        return "—"
    texte = f"{x:,.{decimales}f}".replace(",", "\x00").replace(".", ",")
    return texte.replace("\x00", NBSP)


def signe(x, decimales=2):
    return "—" if x is None else ("+" if x >= 0 else "") + fr(x, decimales)


def oui(booleen):
    return "oui" if booleen else "non"


def arrondi(x, decimales=4):
    return None if x is None else round(x, decimales)


def echapper(texte):
    return texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ecrire_csv(chemin, entete, lignes):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", newline="", encoding="utf-8") as flux:
        plume = csv.DictWriter(flux, fieldnames=entete)
        plume.writeheader()
        for ligne in lignes:
            plume.writerow({c: ("" if ligne.get(c) is None else ligne[c]) for c in entete})


def ecrire_texte(chemin, texte):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline=NL_) as flux:
        flux.write(texte)


def p_bilaterale(t, ddl):
    """p-valeur bilaterale de Student, par p_valeur_student() de import_societe.py."""
    if "student" not in _OUTILS:
        sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "python"))
        from import_societe import p_valeur_student  # noqa: PLC0415 - le depot n'est pas un paquet
        _OUTILS["student"] = p_valeur_student
    return _OUTILS["student"](t, ddl)


def quantile_student(ddl):
    """Le t dont la p-valeur bilaterale vaut 0,05, par dichotomie."""
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


# --------------------------------------------------------------------------
# Les dix series, et leur calendrier unique


def charger(quotes):
    par_ticker, calendriers = {}, []
    for ticker in VALEURS:
        chemin = quotes / f"{ticker.replace('.', '_')}_2019-01-02_2026-09-11.csv"
        if not chemin.exists():
            erreur(f"Serie absente : {chemin}\n"
                   f"  python python/import_societe.py {ticker} --debut 2019-01-02 "
                   "--fin 2026-09-13")
        jours, par_jour, splits = [], {}, []
        with chemin.open(encoding="utf-8") as flux:
            for ligne in csv.DictReader(flux):
                if not ligne.get("Close"):
                    continue
                jour = ligne["Date"][:10]
                manquantes = [c for c in ("Open", "High", "Low", "Close") if not ligne.get(c)]
                if manquantes:
                    erreur(f"{ticker} au {jour} : colonnes absentes : {', '.join(manquantes)}")
                par_jour[jour] = {c: (float(ligne[c]) if ligne.get(c) else None)
                                  for c in COLONNES}
                if float(ligne.get("Stock Splits") or 0):
                    splits.append((jour, float(ligne["Stock Splits"])))
                jours.append(jour)
        par_ticker[ticker] = {"jours": jours, "par_jour": par_jour, "splits": splits,
                              "rang": {j: i for i, j in enumerate(jours)}}
        calendriers.append(set(jours))
    commun = set.intersection(*calendriers)
    for ticker, jours in zip(VALEURS, calendriers, strict=True):
        if jours != commun:
            erreur(f"Calendriers divergents : {ticker} differe sur {len(jours ^ commun)} "
                   f"seances, dont {sorted(jours ^ commun)[:5]}", code=2)
    return {"par_ticker": par_ticker, "jours": sorted(commun),
            "rang": {j: i for i, j in enumerate(sorted(commun))}}


def facteur(serie, ticker, jour):
    """Le produit des divisions POSTERIEURES a `jour`. Aucune des dix n'en porte."""
    produit = 1.0
    for date, ratio in serie["par_ticker"][ticker]["splits"]:
        if date > jour:
            produit *= ratio
    return produit


def reel(serie, ticker, jour, champ):
    return serie["par_ticker"][ticker]["par_jour"][jour][champ] * facteur(serie, ticker, jour)


# --------------------------------------------------------------------------
# Les deux controles de reproduction


def tirage():
    """Rejoue la permutation declaree : les 40 ISIN tries, graine 10."""
    if len(CAC_2019) != 40 or len(set(CAC_2019)) != 40:
        erreur("La composition du 2019-01-02 doit rendre 40 valeurs distinctes", code=2)
    ordre = sorted(CAC_2019)
    random.Random(GRAINE).shuffle(ordre)
    return ordre


def controler_univers(repertoire):
    """Confronte univers.csv a la permutation : le tirage doit se rejouer a l'identique."""
    chemin = repertoire / UNIVERS
    if not chemin.exists():
        erreur(f"Univers absent : {chemin}")
    with chemin.open(encoding="utf-8") as flux:
        lignes = list(csv.DictReader(flux))
    attendus = {str(rang): isin for rang, isin in enumerate(tirage(), start=1)}
    for ligne in lignes:
        rang = ligne["RANG_TIRAGE"]
        if attendus.get(rang) != ligne["ISIN"]:
            erreur(f"Tirage non reproduit au rang {rang} : univers.csv porte "
                   f"{ligne['ISIN']}, la graine {GRAINE} donne {attendus.get(rang)}", code=2)
    retenues = tuple(li["TICKER"] for li in lignes if li["RETENUE"] == "oui")
    if retenues != VALEURS:
        erreur(f"univers.csv retient {retenues}, le moteur joue {VALEURS}", code=2)
    examines = tuple(int(li["RANG_TIRAGE"]) for li in lignes if li["EXAMINEE"] == "oui")
    if examines != RANGS_EXAMINES:
        erreur(f"Les valeurs examinees doivent etre les rangs {RANGS_EXAMINES[0]} a "
               f"{RANGS_EXAMINES[-1]}, pas {examines}", code=2)
    return lignes


def controler_evaluations_experience_9(serie):
    """ENGI.PA et SAF.PA sont communes aux deux experiences : leurs evaluations coincident.

    Ces quantites ne dependent pas du portefeuille. Un ecart signalerait un defaut de
    chargement ou de formule, pas une difference de regle.
    """
    if not DECISIONS_EXP_9.exists():
        return None
    with DECISIONS_EXP_9.open(encoding="utf-8") as flux:
        lignes = [li for li in csv.DictReader(flux) if li["TICKER"] in COMMUNES_EXP_9]
    compares = 0
    for li in lignes:
        ev = evaluer(serie, li["TICKER"], li["DATE"])
        if ev is None:
            continue
        compares += 1
        for cle, colonne in (("ecart", "ECART_S"), ("taux20", "TAUX_20")):
            if abs(ev[cle] - float(li[colonne])) > TOLERANCE_REPRODUCTION:
                erreur(f"Reproduction rompue : {li['TICKER']} au {li['DATE']}, {colonne} "
                       f"vaut {ev[cle]:.6f} ici et {li[colonne]} dans l'experience 9",
                       code=2)
    return compares


# --------------------------------------------------------------------------
# L'evaluation, en unites ajustees


def variance_temps(n):
    return (n * n - 1) / 12


def evaluer(serie, ticker, jour):
    cle = (ticker, jour)
    if cle in _OUTILS:
        return _OUTILS[cle]
    s = serie["par_ticker"][ticker]["par_jour"].get(jour)
    resultat = None
    if s is not None and not any(s[c] is None for c in COLONNES[4:]):
        conditions = (s["VAR_120"] > 0, s["VAR_20"] > 0, 1 - s["CORR_120"] ** 2 > 0,
                      s["E_120"] > 0, s["E_20"] > 0)
        if all(conditions):
            r120 = s["CORR_120"] * math.sqrt(s["VAR_120"] / variance_temps(LONGUE))
            s120 = math.sqrt(LONGUE / (LONGUE - 2) * s["VAR_120"] * (1 - s["CORR_120"] ** 2))
            r20 = s["CORR_20"] * math.sqrt(s["VAR_20"] / variance_temps(COURTE))
            resultat = {
                "close": s["Close"], "val": s["VAL_120"], "s120": s120,
                "ecart": (s["Close"] - s["VAL_120"]) / s120,
                "taux120": 100 * r120 / s["E_120"], "taux20": 100 * r20 / s["E_20"],
                "r120": r120, "r20": r20, "val20": s["VAL_20"], "e20": s["E_20"],
            }
    _OUTILS[cle] = resultat
    return resultat


def enveloppe(serie, ticker, jour):
    """Demi-largeurs de l'enveloppe des COURTE residus, en unites ajustees."""
    donnees = serie["par_ticker"][ticker]
    i = donnees["rang"][jour]
    if i + 1 < COURTE:
        return None
    valeurs = [donnees["par_jour"][donnees["jours"][j]]["Close"]
               for j in range(i - COURTE + 1, i + 1)]
    moyenne_t = (COURTE + 1) / 2
    moyenne_v = statistics.fmean(valeurs)
    cov = sum((t - moyenne_t) * (v - moyenne_v)
              for t, v in enumerate(valeurs, start=1)) / COURTE
    pente = cov / variance_temps(COURTE)
    residus = [v - (moyenne_v + pente * (t - moyenne_t))
               for t, v in enumerate(valeurs, start=1)]
    bas = min(range(COURTE), key=lambda j: residus[j])
    haut = max(range(COURTE), key=lambda j: residus[j])
    return -residus[bas], residus[haut], bas + 1, haut + 1


def decisions_hebdomadaires(serie, debut, fin):
    """La derniere seance de chaque semaine civile ou les dix sont evaluables."""
    par_semaine = {}
    for jour in serie["jours"]:
        if debut <= jour <= fin and all(evaluer(serie, t, jour) for t in VALEURS):
            cle = datetime.date.fromisoformat(jour).isocalendar()[:2]
            par_semaine[cle] = jour
    return sorted(par_semaine.values())


def taux_achat(ticker):
    """La TTF n'est pas due par une societe etrangere."""
    return (COURTAGE + SPREAD + (0.0 if ticker in EXEMPTES_TTF else TTF)) / 100


def taux_vente():
    return (COURTAGE + SPREAD) / 100


def verdict_du_jour(ev, seuil4=None, seuil7=None):
    if seuil7 is not None and ev["close"] < seuil7:
        return "sous le seuil de la règle 7"
    if ev["ecart"] > K:
        return "au-dessus du bord haut"
    if seuil4 is not None and ev["close"] < seuil4:
        return "sous le seuil de la règle 4"
    if ev["ecart"] < -K:
        return ("candidate à l'achat" if ev["taux20"] >= 0
                else "sous le bord bas, pente courte négative")
    return "dans la bande"


# --------------------------------------------------------------------------
# La simulation


def motif_ordre(genre, ticker, ev, seuil7=None):
    bas, haut = ev["val"] - ev["s120"], ev["val"] + ev["s120"]
    textes = {
        "ACHAT": (f"{ticker} : clôture {fr(ev['close'])} sous le bord bas {fr(bas)} "
                  f"({signe(ev['ecart'])} s), TAUX_20 {signe(ev['taux20'], 3)} %/séance"),
        "REGLE-4": (f"{ticker} : clôture {fr(ev['close'])} sous le seuil de la règle 4 "
                    f"({signe(ev['ecart'])} s dans la bande)"),
        "RENFORT": (f"{ticker} : renforcement, clôture {fr(ev['close'])} encore sous le bord "
                    f"bas ({signe(ev['ecart'])} s), TAUX_20 {signe(ev['taux20'], 3)} %/séance"),
        "VENTE": (f"{ticker} : clôture {fr(ev['close'])} au-dessus du bord haut {fr(haut)} "
                  f"({signe(ev['ecart'])} s)"),
        "REGLE-7": (f"{ticker} : clôture {fr(ev['close'])} sous le seuil de repli "
                    f"{fr(seuil7)}, soit −15 % du prix de la première tranche"),
    }
    return textes[genre]


def ecrire_ordre(jour, decision, ticker, genre, place, quantite, prix, brut, frais, ev,
                 net, seuil7=None):
    return {"DATE": jour, "DATE_DECISION": decision, "TICKER": ticker, "SENS": genre,
            "RANG_SERVICE": place, "QUANTITE": quantite, "PRIX_REEL": prix, "BRUT": brut,
            "FRAIS": frais, "NET": net, "ECART_S": ev["ecart"], "TAUX_20": ev["taux20"],
            "MOTIF": motif_ordre(genre, ticker, ev, seuil7)}


def etat_neuf():
    return {"titres": dict.fromkeys(VALEURS, 0), "seuil4": dict.fromkeys(VALEURS, None),
            "seuil7": dict.fromkeys(VALEURS, None),
            "decision_achat": dict.fromkeys(VALEURS, None),
            "r4_fait": dict.fromkeys(VALEURS, False),
            "r6_fait": dict.fromkeys(VALEURS, False),
            "carence": dict.fromkeys(VALEURS, None),
            "ouverte": dict.fromkeys(VALEURS, None)}


def collecter(serie, etat, veille, rang, total, options, compte, coupees):
    """Les signaux des dix valeurs, sans passer le moindre ordre."""
    avec_r4, avec_r6 = options
    ventes, achats = [], []
    for ticker in VALEURS:
        ev = evaluer(serie, ticker, veille)
        if ev is None:
            continue
        compte["sous_bas"] += ev["ecart"] < -K
        compte["sous_bas_pente"] += ev["ecart"] < -K and ev["taux20"] >= 0
        compte["au_dessus"] += ev["ecart"] > K
        if ticker in coupees:
            continue
        detenue = etat["titres"][ticker] > 0
        if detenue and ev["ecart"] > K:
            ventes.append((ticker, ev))
        elif not detenue and ev["ecart"] < -K and ev["taux20"] >= 0:
            bloquee = etat["carence"][ticker] is not None and rang[veille] < etat["carence"][ticker]
            if bloquee:
                compte["carence_bloquee"] += 1
                continue
            achats.append((ticker, ev, "ACHAT", PART_ACHAT * total))
        elif detenue:
            seuil = etat["seuil4"][ticker]
            r4 = seuil is not None and not etat["r4_fait"][ticker] and ev["close"] < seuil
            achat = etat["decision_achat"][ticker]
            r6 = (not etat["r6_fait"][ticker] and achat is not None
                  and rang[veille] == rang[achat] + 1
                  and ev["ecart"] < -K and ev["taux20"] >= 0)
            compte["r4_possible"] += r4
            compte["r6_possible"] += r6
            compte["meme_semaine"] += r4 and r6
            if r4 and avec_r4:
                achats.append((ticker, ev, "REGLE-4", PART_ACHAT * total))
            if r6 and avec_r6:
                achats.append((ticker, ev, "RENFORT", PART_RENFORT * total))
    achats.sort(key=lambda a: a[1]["ecart"])      # l'ecart le plus negatif d'abord
    return ventes, achats


def simuler(serie, debut, fin, avec_r4=True, avec_r6=True, avec_r7=True):
    decisions = decisions_hebdomadaires(serie, debut, fin)
    if not decisions:
        erreur(f"Aucune decision hebdomadaire entre {debut} et {fin}")
    rang = {d: i for i, d in enumerate(decisions)}
    seances = [j for j in serie["jours"] if debut <= j <= fin]
    etat = etat_neuf()
    especes = DOTATION
    ordres, valeurs, positions, carences = [], {}, [], []
    compte = dict.fromkeys(("sous_bas", "sous_bas_pente", "au_dessus", "r4_possible",
                            "r6_possible", "meme_semaine", "refus_especes", "r7_declenchee",
                            "r7_et_r4", "carence_bloquee"), 0)

    def vendre(ticker, jour, veille, genre, place):
        nonlocal especes
        prix = reel(serie, ticker, jour, "Open")
        quantite = etat["titres"][ticker]
        brut = quantite * prix
        frais = brut * taux_vente()
        especes += brut - frais
        ev = evaluer(serie, ticker, veille)
        ordres.append(ecrire_ordre(jour, veille, ticker, genre, place, quantite, prix, brut,
                                   frais, ev, -frais, etat["seuil7"][ticker]))
        position = etat["ouverte"][ticker]
        if position is not None:
            position.update({"sortie": jour, "prix_sortie": prix, "motif": genre,
                             "recu": brut - frais})
        etat["titres"][ticker] = 0
        etat["seuil4"][ticker] = etat["seuil7"][ticker] = None
        etat["decision_achat"][ticker] = None
        etat["r4_fait"][ticker] = etat["r6_fait"][ticker] = False
        etat["ouverte"][ticker] = None

    for i, jour in enumerate(seances):
        veille = seances[i - 1] if i else None
        if veille is not None:
            for ticker in VALEURS:            # attributions d'actions gratuites
                for date, ratio in serie["par_ticker"][ticker]["splits"]:
                    if date == jour and etat["titres"][ticker]:
                        etat["titres"][ticker] = int(etat["titres"][ticker] * ratio)
            # --- regle 7 : constatee a CHAQUE cloture, avant tout le reste
            coupees = set()
            if avec_r7:
                for ticker in VALEURS:
                    seuil7 = etat["seuil7"][ticker]
                    if not etat["titres"][ticker] or seuil7 is None:
                        continue
                    close = serie["par_ticker"][ticker]["par_jour"][veille]["Close"]
                    if close >= seuil7:
                        continue
                    compte["r7_declenchee"] += 1
                    ev = evaluer(serie, ticker, veille)
                    seuil4 = etat["seuil4"][ticker]
                    if (ev is not None and seuil4 is not None and not etat["r4_fait"][ticker]
                            and ev["close"] < seuil4):
                        compte["r7_et_r4"] += 1
                    vendre(ticker, jour, veille, "REGLE-7", 0)
                    # La regle 7 se constate a chaque cloture : la coupe tombe souvent
                    # hors d'un jour de decision. La carence part alors de la PROCHAINE.
                    depuis = bisect.bisect_left(decisions, veille)
                    etat["carence"][ticker] = depuis + CARENCE
                    carences.append({"ticker": ticker, "depuis": depuis,
                                     "jusqua": depuis + CARENCE, "coupee": jour})
                    coupees.add(ticker)
            if veille in rang:
                total = valeurs[veille][2]
                ventes, achats = collecter(serie, etat, veille, rang, total,
                                           (avec_r4, avec_r6), compte, coupees)
                for place, (ticker, _ev) in enumerate(ventes, start=1):
                    vendre(ticker, jour, veille, "VENTE", place)
                for place, (ticker, ev, genre, montant) in enumerate(achats, start=1):
                    prix = reel(serie, ticker, jour, "Open")
                    unitaire = prix * (1 + taux_achat(ticker))
                    quantite = int(min(montant, especes, PLAFOND * total) // unitaire)
                    if quantite < 1:
                        compte["refus_especes"] += 1
                        continue
                    brut = quantite * prix
                    frais = brut * taux_achat(ticker)
                    especes -= brut + frais
                    etat["titres"][ticker] += quantite
                    ordres.append(ecrire_ordre(jour, veille, ticker, genre, place, quantite,
                                               prix, brut, frais, ev, brut + frais))
                    if genre == "ACHAT":
                        prix1 = prix / facteur(serie, ticker, jour)
                        etat["seuil4"][ticker] = ev["close"] - ev["s120"]
                        etat["seuil7"][ticker] = prix1 * (1 + REPLI_R7)
                        etat["decision_achat"][ticker] = veille
                        etat["r4_fait"][ticker] = etat["r6_fait"][ticker] = False
                        position = {"ticker": ticker, "achat": jour, "decision": veille,
                                    "quantite": quantite, "brut": brut, "frais": frais,
                                    "investi": brut + frais, "tranches": 1, "prix1": prix1,
                                    "seuil4": etat["seuil4"][ticker],
                                    "seuil7": etat["seuil7"][ticker], "sortie": None,
                                    "prix_sortie": None, "motif": None, "recu": None}
                        positions.append(position)
                        etat["ouverte"][ticker] = position
                    else:
                        if genre == "REGLE-4":
                            etat["r4_fait"][ticker] = True
                        else:
                            etat["r6_fait"][ticker] = True
                        position = etat["ouverte"][ticker]
                        if position is not None:
                            position["quantite"] += quantite
                            position["brut"] += brut
                            position["frais"] += frais
                            position["investi"] += brut + frais
                            position["tranches"] += 1
        titres_valeur = sum(etat["titres"][t] * reel(serie, t, jour, "Close") for t in VALEURS)
        ouvertes = sum(1 for t in VALEURS if etat["titres"][t])
        valeurs[jour] = (especes, titres_valeur, especes + titres_valeur, ouvertes)
    return {"ordres": ordres, "valeurs": valeurs, "positions": positions, "seances": seances,
            "decisions": decisions, "compte": compte, "carences": carences}


# --------------------------------------------------------------------------
# Les deux references


def detention(serie, debut, fin):
    """Le panier equipondere des dix, tout investi a la deuxieme seance."""
    seances = [j for j in serie["jours"] if debut <= j <= fin]
    especes, quantites = DOTATION, {}
    for ticker in VALEURS:
        prix = reel(serie, ticker, seances[1], "Open")
        quantites[ticker] = int((DOTATION / len(VALEURS)) // (prix * (1 + taux_achat(ticker))))
        especes -= quantites[ticker] * prix * (1 + taux_achat(ticker))
    valeurs = {}
    for i, jour in enumerate(seances):
        if i:
            for ticker in VALEURS:
                for date, ratio in serie["par_ticker"][ticker]["splits"]:
                    if date == jour:
                        quantites[ticker] = int(quantites[ticker] * ratio)
        titres = sum(quantites[t] * reel(serie, t, jour, "Close") for t in VALEURS)
        valeurs[jour] = (especes, titres, especes + titres, len(VALEURS))
    return valeurs


def appariee(valeurs, reference, seances):
    """Le panier, detenu dans la proportion ou le portefeuille l'etait la veille."""
    base = [100.0]
    for i in range(1, len(seances)):
        veille = valeurs[seances[i - 1]]
        poids = veille[1] / veille[2] if veille[2] else 0.0
        rendement = reference[seances[i]][2] / reference[seances[i - 1]][2] - 1
        base.append(base[-1] * (1 + poids * rendement))
    return base


def ecart_type(a, b):
    """Ecart-type annualise, en points, de la difference des rendements quotidiens."""
    ra = [a[i] / a[i - 1] - 1 for i in range(1, len(a))]
    rb = [b[i] / b[i - 1] - 1 for i in range(1, len(b))]
    ecarts = [x - y for x, y in zip(ra, rb, strict=True)]
    return statistics.stdev(ecarts) * math.sqrt(252) * 100 if len(ecarts) > 1 else None


def resumer(serie, simulation, debut, fin):
    seances, valeurs = simulation["seances"], simulation["valeurs"]
    reference = detention(serie, debut, fin)
    base = [100 * valeurs[j][2] / DOTATION for j in seances]
    ref = [100 * reference[j][2] / DOTATION for j in seances]
    app = appariee(valeurs, reference, seances)
    parts = [100 * valeurs[j][1] / valeurs[j][2] for j in seances]
    genres = {g: sum(1 for o in simulation["ordres"] if o["SENS"] == g)
              for g in ("ACHAT", "REGLE-4", "RENFORT", "VENTE", "REGLE-7")}
    return {**simulation, "base": base, "appariee": app, "detention": ref,
            "reference": reference, "part": statistics.fmean(parts), "maximum": max(parts),
            "frais": sum(o["FRAIS"] for o in simulation["ordres"]),
            "n_ordres": len(simulation["ordres"]), "genres": genres,
            "alpha": base[-1] - app[-1], "brut": base[-1] - ref[-1],
            "te_app": ecart_type(base, app), "te_det": ecart_type(base, ref)}


# --------------------------------------------------------------------------
# Les positions mesurees, et ce que la regle 7 a coupe


def mesurer_positions(serie, simulation, fin):
    lignes = []
    for p in simulation["positions"]:
        ticker = p["ticker"]
        sortie = p["sortie"] or fin
        prix_sortie = p["prix_sortie"] or reel(serie, ticker, fin, "Close")
        jours = [j for j in serie["jours"] if p["achat"] <= j <= sortie]
        moyen = p["brut"] / p["quantite"]
        recu = p["recu"] if p["recu"] is not None else p["quantite"] * prix_sortie
        creux_close = min(serie["par_ticker"][ticker]["par_jour"][j]["Close"] for j in jours)
        creux_low = min(serie["par_ticker"][ticker]["par_jour"][j]["Low"] for j in jours)
        lignes.append({
            **p, "sortie_effective": sortie, "prix_sortie_effectif": prix_sortie,
            "ouverte": p["sortie"] is None, "prix_moyen": moyen, "seances": len(jours),
            "plus_value": 100 * (prix_sortie / moyen - 1),
            "repli_premiere": 100 * (creux_close / p["prix1"] - 1),
            "repli_low": 100 * (creux_low / p["prix1"] - 1),
            "repli_moyen": 100 * (creux_close * facteur(serie, ticker, sortie) / moyen - 1),
            "contribution": recu - p["investi"],
        })
    return lignes


def contrefactuel_r7(serie, declaree, sans_r7, fin):
    """Ce que chaque ligne coupee serait devenue, meme valeur et meme date d'achat."""
    index = {(p["ticker"], p["achat"]): p for p in sans_r7["positions"]}
    lignes = []
    for p in declaree["positions"]:
        if p["motif"] != "REGLE-7":
            continue
        realise = 100 * (p["prix_sortie"] / (p["brut"] / p["quantite"]) - 1)
        gain = p["recu"] - p["investi"]
        q = index.get((p["ticker"], p["achat"]))
        if q is None:
            lignes.append({"ticker": p["ticker"], "achat": p["achat"], "sortie": p["sortie"],
                           "realise": realise, "gain": gain, "sans": None})
            continue
        sortie_q = q["sortie"] or fin
        prix_q = q["prix_sortie"] or reel(serie, q["ticker"], fin, "Close")
        recu_q = q["recu"] if q["recu"] is not None else q["quantite"] * prix_q
        lignes.append({
            "ticker": p["ticker"], "achat": p["achat"], "sortie": p["sortie"],
            "realise": realise, "gain": gain,
            "sans": {"motif": q["motif"] or "ouverte", "sortie": sortie_q,
                     "resultat": 100 * (prix_q / (q["brut"] / q["quantite"]) - 1),
                     "gain": recu_q - q["investi"], "tranches": q["tranches"]}})
    return lignes


def compter_coupes(lignes):
    bonnes = sum(1 for li in lignes if li["sans"] and li["realise"] > li["sans"]["resultat"])
    avec = sum(li["gain"] for li in lignes)
    sans = sum(li["sans"]["gain"] for li in lignes if li["sans"])
    return {"coupes": len(lignes), "bonnes": bonnes, "mauvaises": len(lignes) - bonnes,
            "gain_avec": avec, "gain_sans": sans, "ecart": avec - sans}


# --------------------------------------------------------------------------
# Les issues declarees, par grappes de dates

COMPARAISONS = (
    ("REGLE-3-BANDE", "Règle 3, bande", "sous le bord bas", "les autres",
     lambda li: True, lambda li: li["SOUS_BAS"]),
    ("REGLE-3-PENTE", "Règle 3, pente", "sous le bord bas et `TAUX_20 ≥ 0`",
     "sous le bord bas et `TAUX_20 < 0`",
     lambda li: li["SOUS_BAS"], lambda li: li["TAUX_20_POSITIF"]),
    ("REGLE-5-BANDE", "Règle 5, bande haute", "au-dessus du bord haut", "les autres",
     lambda li: True, lambda li: li["AU_DESSUS_HAUT"]),
    ("REGLE-7-SEUIL", "Règle 7, seuil", "repli au-delà de −15 %", "repli moindre",
     lambda li: li["SOUS_BAS"], lambda li: li["REPLI_SOUS_SEUIL"]),
)


def replis_courants(serie, declaree, fin):
    """Le repli de chaque position ouverte, date par date, depuis sa premiere tranche."""
    table = {}
    for p in declaree["positions"]:
        ticker = p["ticker"]
        sortie = p["sortie"] or fin
        for jour in serie["jours"]:
            if p["achat"] <= jour <= sortie:
                close = serie["par_ticker"][ticker]["par_jour"][jour]["Close"]
                table[(ticker, jour)] = 100 * (close / p["prix1"] - 1)
    return table


def issues(serie, decisions, borne, replis):
    """Une ligne par (decision, valeur) : les etats, et le rendement a 20 seances."""
    lignes = []
    for indice, jour in enumerate(decisions):
        for ticker in VALEURS:
            ev = evaluer(serie, ticker, jour)
            if ev is None:
                continue
            i = serie["rang"][jour]
            arrivee = (serie["jours"][i + HORIZON]
                       if i + HORIZON < len(serie["jours"])
                       and serie["jours"][i + HORIZON] <= borne else None)
            rendement = None
            if arrivee:
                close = serie["par_ticker"][ticker]["par_jour"][arrivee]["Close"]
                rendement = 100 * (close / ev["close"] - 1)
            repli = replis.get((ticker, jour))
            lignes.append({"DATE": jour, "TICKER": ticker, "SOUS_BAS": ev["ecart"] < -K,
                           "TAUX_20_POSITIF": ev["taux20"] >= 0,
                           "AU_DESSUS_HAUT": ev["ecart"] > K,
                           "REPLI_SOUS_SEUIL": repli is not None and repli < 100 * REPLI_R7,
                           "SOUS_ECHANTILLON": indice % PAS_ECHANTILLON == 0,
                           "RENDEMENT_20": rendement})
    return lignes


def comparer(lignes, population, groupe):
    """La date est l'unite : une difference de moyennes par date, puis Student sur ces dates.

    Les dix valeurs d'une meme date partagent le marche du jour : les compter comme
    independantes fabriquerait des intervalles trop etroits (experience 5).
    """
    par_date = {}
    for li in lignes:
        if not li["SOUS_ECHANTILLON"] or li["RENDEMENT_20"] is None or not population(li):
            continue
        par_date.setdefault(li["DATE"], ([], []))[0 if groupe(li) else 1].append(
            li["RENDEMENT_20"])
    differences, moyennes_a, moyennes_b = [], [], []
    for _date, (a, b) in sorted(par_date.items()):
        if a and b:
            differences.append(statistics.fmean(a) - statistics.fmean(b))
            moyennes_a.append(statistics.fmean(a))
            moyennes_b.append(statistics.fmean(b))
    resultat = {"dates": len(differences),
                "dates_ecartees": sum(1 for _d, (a, b) in par_date.items() if not (a and b)),
                "moy_a": statistics.fmean(moyennes_a) if moyennes_a else None,
                "moy_b": statistics.fmean(moyennes_b) if moyennes_b else None,
                "difference": statistics.fmean(differences) if differences else None,
                "ic": None, "p": None}
    if len(differences) < 2:
        return resultat
    ddl = len(differences) - 1
    se = statistics.stdev(differences) / math.sqrt(len(differences))
    if se > 0:
        resultat["ic"] = quantile_student(ddl) * se
        resultat["p"] = p_bilaterale(resultat["difference"] / se, ddl)
    return resultat


# --------------------------------------------------------------------------
# L'etalonnage, confronte


def egal(publie, calcule):
    if calcule is None:
        return False
    if isinstance(publie, float):
        decimales = len(repr(publie).split(".")[1])
        return round(calcule, decimales) == round(publie, decimales)
    return calcule == publie


def etalonnage(serie, debut):
    """Rejoue les cinq variantes sur 2019-2021 et rend les nombres a confronter."""
    resultats = {}
    for nom, avec_r4, avec_r6, avec_r7 in VARIANTES:
        simulation = simuler(serie, debut, FIN_ETALONNAGE, avec_r4, avec_r6, avec_r7)
        resultats[nom] = resumer(serie, simulation, debut, FIN_ETALONNAGE)
    declaree = resultats["declaree"]
    compte = declaree["compte"]
    resultats["coupes"] = contrefactuel_r7(serie, declaree, resultats["sans regle 7"],
                                           FIN_ETALONNAGE)
    resultats["taux"] = {
        "decisions": len(declaree["decisions"]),
        "evaluations": len(declaree["decisions"]) * len(VALEURS),
        "sous_bas": compte["sous_bas"], "sous_bas_pente": compte["sous_bas_pente"],
        "au_dessus": compte["au_dessus"], "r4_possible": compte["r4_possible"],
        "r6_possible": compte["r6_possible"], "meme_semaine": compte["meme_semaine"],
        "refus_especes": compte["refus_especes"], "r7_declenchee": compte["r7_declenchee"],
        "r7_et_r4": compte["r7_et_r4"], "carence_bloquee": compte["carence_bloquee"],
        "positions": len(declaree["positions"]),
        "closes": sum(1 for p in declaree["positions"] if p["sortie"]),
        "coupes": sum(1 for p in declaree["positions"] if p["motif"] == "REGLE-7"),
        "te_app": declaree["te_app"], "te_det": declaree["te_det"],
    }
    return resultats


def ecarts_publies(resultats):
    ecarts = []
    for nom, publies in ETALONNAGE_PUBLIE.items():
        obtenu = resultats[nom]
        for cle, publie in publies.items():
            if nom == "taux":
                calcule = obtenu.get(cle)
            elif cle == "ordres":
                calcule = obtenu["n_ordres"]
            elif cle in ("base", "appariee", "detention"):
                calcule = obtenu[cle][-1]
            else:
                calcule = obtenu.get(cle)
            if not egal(publie, calcule):
                ecarts.append((nom, cle, publie, calcule))
    obtenues = resultats["coupes"]
    for ticker, achat, sortie, realise, sortie_sans, resultat_sans in COUPES_PUBLIEES:
        trouvee = next((li for li in obtenues
                        if li["ticker"] == ticker and li["achat"] == achat), None)
        if trouvee is None:
            ecarts.append(("coupes", f"{ticker} {achat}", "presente", "absente"))
            continue
        if trouvee["sortie"] != sortie or not egal(realise, trouvee["realise"]):
            ecarts.append(("coupes", f"{ticker} {achat}", f"{sortie} {realise}",
                           f"{trouvee['sortie']} {round(trouvee['realise'], 2)}"))
        sans = trouvee["sans"]
        if sans and (sans["sortie"] != sortie_sans or not egal(resultat_sans,
                                                              sans["resultat"])):
            ecarts.append(("coupes", f"{ticker} {achat} sans r7",
                           f"{sortie_sans} {resultat_sans}",
                           f"{sans['sortie']} {round(sans['resultat'], 2)}"))
    if len(obtenues) != len(COUPES_PUBLIEES):
        ecarts.append(("coupes", "nombre", len(COUPES_PUBLIEES), len(obtenues)))
    return ecarts


# --------------------------------------------------------------------------
# Les figures


def pas_lisible(amplitude, cibles=6):
    brut = max(amplitude / cibles, 1e-12)
    puissance = 10 ** math.floor(math.log10(brut))
    for multiple in (1, 2, 2.5, 5, 10):
        if multiple * puissance >= brut:
            return multiple * puissance
    return 10 * puissance


def figure_canal(chemin, serie, ticker, jour, seuil4=None, seuil7=None):
    """Bande 120, enveloppe des residus 20, seuil de la regle 4, seuil de la regle 7."""
    ev = evaluer(serie, ticker, jour)
    env = enveloppe(serie, ticker, jour)
    if ev is None or env is None:
        return False
    donnees = serie["par_ticker"][ticker]
    i = donnees["rang"][jour]
    jours = donnees["jours"][max(0, i - LONGUE + 1):i + 1]
    closes = [donnees["par_jour"][j]["Close"] for j in jours]
    n = len(jours)
    env_bas, env_haut, i_bas, i_haut = env
    debut_20 = n - COURTE + 1

    def f120(t):
        return ev["val"] + ev["r120"] * (t - n)

    def f20(t):
        return ev["val20"] + ev["r20"] * (t - n)

    s = K * ev["s120"]
    points = [*closes, f120(1) - s, f120(1) + s, f120(n) - s, f120(n) + s,
              f20(debut_20) - env_bas, f20(n) + env_haut]
    points += [x for x in (seuil4, seuil7) if x is not None]
    bas, haut = min(points), max(points)
    coussin = (haut - bas) * 0.06 or 1.0
    bas, haut = bas - coussin, haut + coussin
    largeur, hauteur = 900, 470
    marge_g, marge_d, marge_h, marge_b = 72, 22, 78, 58
    aire_l, aire_h = largeur - marge_g - marge_d, hauteur - marge_h - marge_b

    def x(t):
        return marge_g + aire_l * (t - 1) / max(n - 1, 1)

    def y(v):
        return marge_h + aire_h * (haut - v) / (haut - bas)

    verdict = verdict_du_jour(ev, seuil4, seuil7)
    couleur = {"candidate à l'achat": "#2e7d32", "au-dessus du bord haut": "#c62828",
               "sous le seuil de la règle 4": "#2e7d32",
               "sous le seuil de la règle 7": "#b71c1c"}.get(verdict, "#1a1a1a")
    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" '
         f'font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{marge_g}" y="26" font-size="15" font-weight="600" fill="#1a1a1a">'
         f'{echapper(ticker)} &#8212; canal au {jour}</text>'),
        (f'<text x="{marge_g}" y="46" font-size="11.5" fill="#444444">'
         f'cl&#244;ture ajust&#233;e {fr(ev["close"])} &#8364;, {signe(ev["ecart"])} s '
         f'&#183; TAUX_120 {signe(ev["taux120"], 3)} %/s&#233;ance '
         f'&#183; TAUX_20 {signe(ev["taux20"], 3)} %/s&#233;ance</text>'),
        (f'<text x="{marge_g}" y="63" font-size="11.5" fill="#444444">'
         f'bande 120 &#177; 1 s : {fr(f120(n) - s)} &#8211; {fr(f120(n) + s)} '
         f'&#183; verdict : <tspan font-weight="600" fill="{couleur}">'
         f'{echapper(verdict)}</tspan></text>'),
    ]
    pas = pas_lisible(haut - bas)
    niveau = math.ceil(bas / pas) * pas
    while niveau <= haut:
        out.append(f'<line x1="{marge_g}" y1="{y(niveau):.1f}" x2="{largeur - marge_d}" '
                   f'y2="{y(niveau):.1f}" stroke="#eeeeee" stroke-width="1"/>')
        out.append(f'<text x="{marge_g - 8}" y="{y(niveau) + 4:.1f}" font-size="10.5" '
                   f'fill="#666666" text-anchor="end">{fr(niveau, 2)}</text>')
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
    for decalage, style in ((env_haut, ' stroke-dasharray="4 3"'),
                            (-env_bas, ' stroke-dasharray="4 3"'), (0.0, "")):
        out.append(f'<line x1="{x(debut_20):.1f}" y1="{y(f20(debut_20) + decalage):.1f}" '
                   f'x2="{x(n):.1f}" y2="{y(f20(n) + decalage):.1f}" stroke="#b35c1e" '
                   f'stroke-width="1.5"{style}/>')
    for seuil, teinte, libelle in ((seuil4, "#7b1fa2", "seuil r&#232;gle 4"),
                                   (seuil7, "#b71c1c", "seuil r&#232;gle 7, &#8722;15 %")):
        if seuil is None:
            continue
        out.append(f'<line x1="{marge_g}" y1="{y(seuil):.1f}" x2="{largeur - marge_d}" '
                   f'y2="{y(seuil):.1f}" stroke="{teinte}" stroke-width="1.4" '
                   f'stroke-dasharray="8 4"/>')
        out.append(f'<text x="{largeur - marge_d}" y="{y(seuil) - 5:.1f}" font-size="10.5" '
                   f'fill="{teinte}" text-anchor="end">{libelle} {fr(seuil)}</text>')
    trace = " ".join(f"{x(t):.1f},{y(v):.1f}" for t, v in enumerate(closes, start=1))
    out.append(f'<polyline points="{trace}" fill="none" stroke="#333333" stroke-width="1.3"/>')
    for indice in (i_bas, i_haut):
        t = debut_20 + indice - 1
        out.append(f'<circle cx="{x(t):.1f}" cy="{y(closes[t - 1]):.1f}" r="4.5" fill="none" '
                   f'stroke="#b35c1e" stroke-width="1.5"/>')
    out.append(f'<circle cx="{x(n):.1f}" cy="{y(closes[-1]):.1f}" r="4" fill="{couleur}"/>')
    out.append(f'<text x="{marge_g}" y="{hauteur - 34}" font-size="10.5" fill="#666666">'
               f'{jours[0]}</text>')
    out.append(f'<text x="{largeur - marge_d}" y="{hauteur - 34}" font-size="10.5" '
               f'fill="#666666" text-anchor="end">{jours[-1]}</text>')
    out.append(
        f'<text x="{marge_g}" y="{hauteur - 12}" font-size="10.5" fill="#444444">'
        f'<tspan fill="#333333">&#9472;</tspan> cl&#244;tures ajust&#233;es &#183; '
        f'<tspan fill="#1f5f8b">&#9472;</tspan> droite sur {LONGUE} s&#233;ances et bande '
        f'&#177; 1 s &#183; <tspan fill="#b35c1e">&#9472;</tspan> droite sur {COURTE} '
        f's&#233;ances et enveloppe des r&#233;sidus</text>')
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")
    return True


def svg_portefeuille(chemin, dates, courbes, executions, debut):
    largeur, hauteur = 900, 420
    marge_g, marge_d, marge_h, marge_b = 62, 18, 46, 62
    aire_l, aire_h = largeur - marge_g - marge_d, hauteur - marge_h - marge_b
    tout = [v for _l, valeurs, _c, _p in courbes for v in valeurs]
    bas, haut = min(tout), max(tout)
    coussin = (haut - bas) * 0.08 or 1.0
    bas, haut = bas - coussin, haut + coussin

    def x(i):
        return marge_g + aire_l * i / max(len(dates) - 1, 1)

    def y(v):
        return marge_h + aire_h * (haut - v) / (haut - bas)

    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" '
         f'font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{marge_g}" y="24" font-size="15" font-weight="600" fill="#1a1a1a">'
         f'Experience 10 &#8212; portefeuille sur dix valeurs, base 100 au {debut}</text>'),
        (f'<text x="{marge_g}" y="40" font-size="11" fill="#666666">{dates[0]} &#8594; '
         f'{dates[-1]} &#183; {len(dates)} seances &#183; traits verticaux : les '
         f'executions</text>'),
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
    for rang, (libelle, valeurs, couleur, pointilles) in enumerate(reversed(courbes)):
        trace = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(valeurs))
        tirets = ' stroke-dasharray="5 4"' if pointilles else ""
        out.append(f'<polyline points="{trace}" fill="none" stroke="{couleur}" '
                   f'stroke-width="1.8"{tirets}/>')
        gauche = marge_g + rang * 240
        out.append(f'<line x1="{gauche}" y1="{hauteur - 18}" x2="{gauche + 24}" '
                   f'y2="{hauteur - 18}" stroke="{couleur}" stroke-width="1.8"{tirets}/>'
                   f'<text x="{gauche + 30}" y="{hauteur - 14}" font-size="10.5" '
                   f'fill="#444444">{echapper(libelle)} {fr(valeurs[-1], 1)}</text>')
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")


def seuils_par_decision(b):
    """Les deux seuils armes de chaque position, rattaches aux decisions qu'ils ont servies."""
    seuils = {}
    for p in b["positions"]:
        for o in b["ordres"]:
            if (o["TICKER"] == p["ticker"] and o["SENS"] in ("REGLE-4", "RENFORT", "REGLE-7")
                    and o["DATE_DECISION"] >= p["decision"]
                    and (p["sortie"] is None or o["DATE"] <= p["sortie"])):
                seuils[(p["ticker"], o["DATE_DECISION"])] = (p["seuil4"], p["seuil7"])
    return seuils


def ecrire_figures(repertoire, serie, b):
    """Une figure a chaque decision qui produit un ordre, et a chaque fin d'annee."""
    seuils = seuils_par_decision(b)
    dates = {(o["TICKER"], o["DATE_DECISION"]) for o in b["ordres"]}
    for annee in b["annees"]:
        derniere = [d for d in b["decisions"] if d[:4] == annee][-1]
        for ticker in VALEURS:
            dates.add((ticker, derniere))
    ecrites = 0
    for ticker, jour in sorted(dates):
        seuil4, seuil7 = seuils.get((ticker, jour), (None, None))
        chemin = repertoire / GRAPHIQUES / ticker / f"canal-{jour}.svg"
        if figure_canal(chemin, serie, ticker, jour, seuil4, seuil7):
            ecrites += 1
    return ecrites


# --------------------------------------------------------------------------
# Les markdown


def tableau_variantes(b):
    out = [("| Variante | Base 100 | Appariée | **Alpha officiel** | Ordres | Frais "
            "| Part investie | Maximum |"),
           "|---|---|---|---|---|---|---|---|"]
    for nom, _r4, _r6, _r7 in VARIANTES:
        v = b["variantes"][nom]
        out.append(f"| {LIBELLE_VARIANTE[nom]} | {fr(v['base'][-1])} "
                   f"| {fr(v['appariee'][-1])} | **{signe(v['alpha'])} pt** | {v['n_ordres']} "
                   f"| {fr(v['frais'])} {EURO} | {fr(v['part'], 2)} % "
                   f"| {fr(v['maximum'], 1)} % |")
    return out


def tableau_positions(lignes):
    out = [("| Valeur | Achat | Sortie | Motif | Tr. | Titres | Prix moyen | Sortie "
            "| +/− value | Repli / 1<sup>re</sup> | Contribution | Séances |"),
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for p in lignes:
        sortie = (f"{p['sortie_effective']} *(ouverte)*" if p["ouverte"]
                  else p["sortie_effective"])
        out.append(f"| `{p['ticker']}` | {p['achat']} | {sortie} "
                   f"| {p['motif'] or 'ouverte'} | {p['tranches']} | {p['quantite']} "
                   f"| {fr(p['prix_moyen'])} {EURO} | {fr(p['prix_sortie_effectif'])} {EURO} "
                   f"| **{signe(p['plus_value'])} %** | {signe(p['repli_premiere'])} % "
                   f"| {signe(p['contribution'])} {EURO} | {p['seances']} |")
    return out


def tableau_coupes(lignes):
    if not lignes:
        return [("*La règle 7 ne s'est **jamais** déclenchée sur la fenêtre jouée. "
                 "C'est en soi un résultat : le seuil de −15 %, calibré sur l'expérience 9, "
                 "n'a rencontré aucune position pour le franchir.*")]
    out = ["| Valeur | Achat | Coupée le | Réalisé | Le même achat, sans la règle 7 |",
           "|---|---|---|---|---|"]
    for li in lignes:
        if li["sans"] is None:
            reste = "*aucune position correspondante*"
        else:
            s = li["sans"]
            bonne = " — *bonne coupe*" if li["realise"] > s["resultat"] else ""
            reste = (f"{s['motif'].lower()} au {s['sortie']}, **{signe(s['resultat'])} %**"
                     f"{bonne}")
        out.append(f"| `{li['ticker']}` | {li['achat']} | {li['sortie']} "
                   f"| {signe(li['realise'])} % | {reste} |")
    return out


def tableau_par_valeur(b):
    out = ["| Valeur | Ordres | Positions | Coupes | Contribution | Séances détenue |",
           "|---|---|---|---|---|---|"]
    for ticker in VALEURS:
        ordres = [o for o in b["ordres"] if o["TICKER"] == ticker]
        positions = [p for p in b["mesurees"] if p["ticker"] == ticker]
        coupes = sum(1 for p in positions if p["motif"] == "REGLE-7")
        out.append(f"| `{ticker}` | {len(ordres)} | {len(positions)} | {coupes} "
                   f"| {signe(sum(p['contribution'] for p in positions))} {EURO} "
                   f"| {sum(p['seances'] for p in positions)} |")
    return out


def journal_annuel(repertoire, b, annee, precedente, suivante):
    seances = [j for j in b["seances"] if j[:4] == annee]
    fin = seances[-1]
    veille = [j for j in b["seances"] if j < seances[0]]
    depart = b["valeurs"][veille[-1]][2] if veille else DOTATION
    ordres = [o for o in b["ordres"] if o["DATE"][:4] == annee]
    jusqua = [j for j in b["seances"] if j <= fin]
    svg_portefeuille(
        repertoire / GRAPHIQUES / f"portefeuille-{annee}.svg", jusqua,
        [("portefeuille", [100 * b["valeurs"][j][2] / DOTATION for j in jusqua],
          "#1f5f8b", False),
         ("référence appariée", [b["appariee"][b["index"][j]] for j in jusqua],
          "#c0782c", True),
         ("détention du panier", [b["detention"][b["index"][j]] for j in jusqua],
          "#9aa5b1", True)],
        [o["DATE"] for o in b["ordres"]], b["debut"])
    total = b["valeurs"][fin][2]
    especes_fin, titres_fin = b["valeurs"][fin][0], b["valeurs"][fin][1]
    part_annee = statistics.fmean(100 * b["valeurs"][j][1] / b["valeurs"][j][2]
                                  for j in seances)
    app = b["appariee"][b["index"][fin]]
    det = b["detention"][b["index"][fin]]
    positions = [p for p in b["mesurees"]
                 if p["achat"][:4] == annee or p["sortie_effective"][:4] == annee]
    coupes = [li for li in b["coupes"] if li["sortie"][:4] == annee]
    bloc = [
        f"# {annee}", "",
        (f"> Journal de l'[expérience 10](../README.md) · {len(seances)} séances · "
         f"**{len(ordres)} ordre{'s' if len(ordres) > 1 else ''}** sur dix valeurs"),
        (f"> Portefeuille au {fin} : **{fr(total)} {EURO}** (base "
         f"{fr(100 * total / DOTATION)}) · appariée {fr(app)} · détention du panier "
         f"{fr(det)}"),
        "", "---", "",
        f"## Le portefeuille depuis le {b['debut']}", "",
        f"![Portefeuille au {fin}](../{GRAPHIQUES}/portefeuille-{annee}.svg)", "",
        "| | |", "|---|---|",
        f"| Valeur au 1er jour de l'année | {fr(depart)} {EURO} |",
        f"| Valeur au {fin} | **{fr(total)} {EURO}** |",
        f"| Variation de l'année | **{signe(100 * (total / depart - 1))} %** |",
        f"| Espèces · titres | {fr(especes_fin)} {EURO} · {fr(titres_fin)} {EURO} |",
        f"| Part investie moyenne de l'année | {fr(part_annee, 2)} % |",
        f"| Lignes ouvertes au {fin} | {b['valeurs'][fin][3]} sur {len(VALEURS)} |",
        f"| Coupes de la règle 7 dans l'année | **{len(coupes)}** |",
        "", "## Les ordres", "",
    ]
    if ordres:
        bloc += [("| Exécution | Décision | Valeur | Sens | Rang | Quantité | Prix réel "
                  "| Frais | Motif |"),
                 "|---|---|---|---|---|---|---|---|---|"]
        for o in ordres:
            bloc.append(f"| {o['DATE']} | {o['DATE_DECISION']} | `{o['TICKER']}` "
                        f"| **{o['SENS']}** | {o['RANG_SERVICE']} | {o['QUANTITE']} "
                        f"| {fr(o['PRIX_REEL'])} {EURO} | {fr(o['FRAIS'])} {EURO} "
                        f"| {o['MOTIF']} |")
    else:
        bloc.append("*Aucun ordre : aucune clôture n'a franchi une borne.*")
    if coupes:
        bloc += ["", "## Ce que la règle 7 a coupé cette année", "", *tableau_coupes(coupes)]
    bloc += ["", "## Les positions touchant l'année", ""]
    bloc += (tableau_positions(positions) if positions
             else ["*Aucune position ouverte ni close dans l'année.*"])
    decisions = [d for d in b["decisions"] if d[:4] == annee]
    sous = sum(1 for li in b["issues"] if li["DATE"][:4] == annee and li["SOUS_BAS"])
    pente = sum(1 for li in b["issues"] if li["DATE"][:4] == annee and li["SOUS_BAS"]
                and li["TAUX_20_POSITIF"])
    dessus = sum(1 for li in b["issues"] if li["DATE"][:4] == annee and li["AU_DESSUS_HAUT"])
    bloc += ["", "## Les décisions de l'année", "", "| Mesure | Valeur |", "|---|---|",
             f"| Décisions hebdomadaires | {len(decisions)} |",
             f"| Évaluations, dix valeurs | {len(decisions) * len(VALEURS)} |",
             f"| Sous le bord bas | {sous} |",
             f"| … dont `TAUX_20 ≥ 0`, donc achetables | **{pente}** |",
             f"| Au-dessus du bord haut | {dessus} |", "",
             "## La lecture de l'année", "",
             lecture_annuelle(b, ordres, positions, coupes, total, depart, app), ""]
    navigation = []
    if precedente:
        navigation.append(f"[← {precedente}]({precedente}.md)")
    navigation.append("[Protocole](../README.md)")
    if suivante:
        navigation.append(f"[{suivante} →]({suivante}.md)")
    bloc += ["---", "", " · ".join(navigation)]
    ecrire_texte(repertoire / RAPPORTS / f"{annee}.md", NL_.join(bloc) + NL_)


def lecture_annuelle(b, ordres, positions, coupes, total, depart, app):
    phrases = [(f"Le portefeuille termine l'année à {fr(total)} {EURO}, soit "
                f"{signe(100 * (total / depart - 1))} % sur l'année.")]
    if ordres:
        frais = sum(o["FRAIS"] for o in ordres)
        touchees = sorted({o["TICKER"] for o in ordres})
        phrases.append(f"Les {len(ordres)} ordres ont porté sur {len(touchees)} valeur"
                       f"{'s' if len(touchees) > 1 else ''} — {', '.join(touchees)} — "
                       f"pour {fr(frais)} {EURO} de frais.")
    else:
        phrases.append("Aucun ordre, donc aucun frais.")
    if coupes:
        bonnes = sum(1 for li in coupes if li["sans"] and li["realise"] > li["sans"]["resultat"])
        phrases.append(f"La règle 7 a coupé {len(coupes)} ligne"
                       f"{'s' if len(coupes) > 1 else ''}, dont {bonnes} l'"
                       f"{'ont' if bonnes > 1 else 'a'} été à bon escient.")
    else:
        phrases.append("La règle 7 ne s'est pas déclenchée.")
    ouvertes = [p for p in positions if p["ouverte"]]
    if ouvertes:
        detail = ", ".join(f"{p['ticker']} ({signe(p['plus_value'])} %)" for p in ouvertes)
        phrases.append(f"{len(ouvertes)} position{'s' if len(ouvertes) > 1 else ''} "
                       f"reste{'nt' if len(ouvertes) > 1 else ''} ouverte"
                       f"{'s' if len(ouvertes) > 1 else ''} : {detail}.")
    ecart = 100 * total / DOTATION - app
    phrases.append(f"Depuis le début, le portefeuille est "
                   f"{'devant' if ecart >= 0 else 'derrière'} sa référence à exposition "
                   f"appariée de {fr(abs(ecart))} point.")
    return " ".join(phrases)


def bilan(b, compares):
    d = b["variantes"]["declaree"]
    sans_r7 = b["variantes"]["sans regle 7"]
    ni = b["variantes"]["ni regle 4 ni regle 6"]
    mde_app = Z95 * d["te_app"]
    ouvertes = [p for p in b["mesurees"] if p["ouverte"]]
    closes = [p for p in b["mesurees"] if not p["ouverte"]]
    compte = d["compte"]
    ecarts = ecarts_publies(b["etalonnage"])
    bilan_coupes = compter_coupes(b["coupes"])
    qualite = ("*indiscernable de zéro*" if abs(d["alpha"]) <= mde_app
               else "*au-delà de son effet minimal détectable*")
    out = [
        "# Bilan de l'expérience 10", "",
        (f"> [Expérience 10](README.md) · dix valeurs tirées au sort, coupe à −15 % · "
         f"**{signe(d['base'][-1] - 100)} %** · alpha officiel "
         f"**{signe(d['alpha'])} pt**"), "",
        ("> ⚠️ **Le seuil de −15 % est de catégorie B** : il a été lu sur les replis de "
         "l'[expérience 9](../experience_9/README.md). Le "
         "[protocole](README.md#-ce-que-cette-expérience-doit-déclarer-avant-tout-le-reste) "
         "le déclare, et l'a testé sur un univers inédit à 8 valeurs sur 10."),
        "", "---", "", "## 1. Le compte", "", "| | |", "|---|---|",
        f"| Dotation | {fr(DOTATION)} {EURO} au {b['debut']} |",
        f"| Valeur finale au {b['fin']} | **{fr(d['valeurs'][b['fin']][2])} {EURO}** |",
        f"| Performance | **{signe(d['base'][-1] - 100)} %** |",
        f"| Référence à exposition appariée | {signe(d['appariee'][-1] - 100)} % |",
        f"| Détention continue du panier | {signe(d['detention'][-1] - 100)} % |",
        (f"| **Alpha officiel** | **{signe(d['alpha'])} pt** — {qualite}, effet minimal "
         f"détectable ± {fr(mde_app, 1)} pt |"),
        f"| Écart brut à la détention | {signe(d['brut'])} pt |",
        (f"| Ordres | {d['n_ordres']} — "
         + ", ".join(f"{n} {g.lower()}" for g, n in d["genres"].items() if n) + " |"),
        (f"| Frais cumulés | {fr(d['frais'])} {EURO}, soit "
         f"{fr(100 * d['frais'] / DOTATION, 2)} pt de dotation |"),
        f"| Part investie moyenne · maximum | {fr(d['part'], 2)} % · {fr(d['maximum'], 1)} % |",
        f"| Ordres refusés faute d'espèces | {compte['refus_especes']} |",
        f"| Achats bloqués par la carence | {compte['carence_bloquee']} |",
        (f"| Décisions · évaluations | {len(d['decisions'])} · "
         f"{len(d['decisions']) * len(VALEURS)} |"),
        (f"| Positions · closes · encore ouvertes | {len(b['mesurees'])} · "
         f"{len(closes)} · {len(ouvertes)} |"),
        "", "## 2. Ce que la règle 7 a coupé — et ce que ces lignes seraient devenues", "",
        ("> C'est la mesure qui décide si la règle 7 protège ou coûte. Chaque ligne coupée "
         "est rapprochée du **même achat, à la même date**, dans la variante sans règle 7."),
        "",
        *tableau_coupes(b["coupes"]),
    ]
    if b["coupes"]:
        out += [
            "", "| | |", "|---|---|",
            f"| Coupes | **{bilan_coupes['coupes']}** |",
            (f"| Dont **bonnes** · **mauvaises** | {bilan_coupes['bonnes']} · "
             f"**{bilan_coupes['mauvaises']}** |"),
            (f"| Contribution cumulée **avec** la règle 7 | "
             f"{signe(bilan_coupes['gain_avec'])} {EURO} |"),
            (f"| Contribution cumulée **sans** elle | "
             f"{signe(bilan_coupes['gain_sans'])} {EURO} |"),
            (f"| **Ce que la protection a coûté** | "
             f"**{signe(bilan_coupes['ecart'])} {EURO}** |"),
            "",
            (f"Le repli réalisé à la sortie va de "
             f"{signe(min(li['realise'] for li in b['coupes']))} % à "
             f"{signe(max(li['realise'] for li in b['coupes']))} % : **le seuil déclenche à "
             "−15 %, il ne borne pas la perte à −15 %**, puisque le repli est constaté en "
             "clôture et exécuté à l'ouverture suivante."),
        ]
    out += [
        "", "## 3. Les positions", "", *tableau_positions(b["mesurees"]),
        "", "## 4. Ce que chaque valeur a apporté", "", *tableau_par_valeur(b),
        "", "## 5. Ce qu'ajoute chaque règle", "", *tableau_variantes(b), "",
        (f"**La comparaison qui compte est la deuxième ligne** : sans la règle 7, c'est "
         f"exactement la règle de l'expérience 9. L'écart d'alpha vaut "
         f"**{signe(d['alpha'] - sans_r7['alpha'])} pt**, pour "
         f"{d['n_ordres'] - sans_r7['n_ordres']} ordres et "
         f"{signe(d['frais'] - sans_r7['frais'])} {EURO} de frais de plus, et une part "
         f"investie de {fr(d['part'], 2)} % contre {fr(sans_r7['part'], 2)} %."),
        "", "| Écart apparié | Base 100 | Écart-type de la différence | EMD |",
        "|---|---|---|---|",
    ]
    for nom, _r4, _r6, _r7 in VARIANTES[1:]:
        v = b["variantes"][nom]
        te = ecart_type(d["base"], v["base"])
        out.append(f"| déclarée − {LIBELLE_VARIANTE[nom].replace('**', '')} "
                   f"| **{signe(d['base'][-1] - v['base'][-1])} pt** | {fr(te)} %/an "
                   f"| ± {fr(Z95 * te, 1)} pt |")
    out += [
        "", "## 6. Les taux de déclenchement", "",
        (f"> Sur {len(d['decisions'])} décisions et "
         f"{len(d['decisions']) * len(VALEURS)} évaluations de valeur."), "",
        "| Règle | Déclenchée | Exécutée |", "|---|---|---|",
        (f"| **3** — sous le bord bas et `TAUX_20 ≥ 0` | {compte['sous_bas_pente']} "
         f"| {d['genres']['ACHAT']} |"),
        f"| **4** — sous le seuil figé | {compte['r4_possible']} | {d['genres']['REGLE-4']} |",
        f"| **6** — renforcement | {compte['r6_possible']} | {d['genres']['RENFORT']} |",
        f"| **5** — au-dessus du bord haut | {compte['au_dessus']} | {d['genres']['VENTE']} |",
        (f"| **7** — repli au-delà de −15 % | {compte['r7_declenchee']} "
         f"| {d['genres']['REGLE-7']} |"),
        "",
        (f"La règle 7 et la règle 4 étaient remplies la même semaine sur la même valeur "
         f"**{compte['r7_et_r4']} fois** — autant de renforcements que la coupe a empêchés. "
         f"{compte['sous_bas']} évaluations sont passées sous le bord bas, dont "
         f"{compte['sous_bas_pente']} avec une pente courte positive."),
        "", "## 7. Les issues déclarées, par grappes de dates", "",
        ("> Rendement du cours sur les 20 séances suivant la décision, sur une décision "
         f"hebdomadaire sur {PAS_ECHANTILLON}. **La date est l'unité, pas la valeur.**"), "",
        ("| Élément | Groupe testé | Témoin | Dates | Moyennes | Différence | IC95 "
         "| Verdict |"),
        "|---|---|---|---|---|---|---|---|",
    ]
    for cle, libelle, groupe_a, groupe_b, _pop, _grp in COMPARAISONS:
        c = b["comparaisons"][cle]
        verdict = ("*non mesurable*" if c["ic"] is None else
                   ("**exclut zéro**" if abs(c["difference"]) > c["ic"] else "contient zéro"))
        out.append(f"| {libelle} | {groupe_a} | {groupe_b} | {c['dates']} "
                   f"| {signe(c['moy_a'])} % contre {signe(c['moy_b'])} % "
                   f"| **{signe(c['difference'])} pt** | ± {fr(c['ic'])} pt | {verdict} |")
    out += [
        "", "## 8. L'étalonnage, publié avant, recalculé après", "",
        ("| Variante | Base publiée | Base recalculée | Alpha publié | Alpha recalculé "
         "| Concorde |"),
        "|---|---|---|---|---|---|",
    ]
    for nom, _r4, _r6, _r7 in VARIANTES:
        publie = ETALONNAGE_PUBLIE[nom]
        obtenu = b["etalonnage"][nom]
        manque = any(e[0] == nom for e in ecarts)
        out.append(f"| {LIBELLE_VARIANTE[nom]} | {fr(publie['base'])} "
                   f"| {fr(obtenu['base'][-1])} | {signe(publie['alpha'])} pt "
                   f"| {signe(obtenu['alpha'])} pt | {'✗' if manque else '✓'} |")
    total_publies = sum(len(v) for v in ETALONNAGE_PUBLIE.values()) + len(COUPES_PUBLIEES)
    out += [
        "",
        (f"**{total_publies - len(ecarts)} nombres publiés sur {total_publies}** sont "
         "retrouvés à l'identique, les cinq coupes de l'étalonnage comprises."
         if not ecarts else
         f"**{len(ecarts)} nombres publiés sur {total_publies} ne sont pas retrouvés.** Le "
         "README n'est pas corrigé après coup ; les écarts sont listés en console."),
        "", "### Les deux contrôles de reproduction", "",
        "| Contrôle | Résultat |", "|---|---|",
        f"| La permutation se rejoue depuis la graine {GRAINE} | ✓ |",
        (f"| Les évaluations d'`ENGI.PA` et `SAF.PA` contre l'expérience 9 | "
         f"**{compares} comparées, 0 écart** |" if compares
         else "| Les évaluations contre l'expérience 9 | *`decisions.csv` absent* |"),
        "", "## 9. Ce que l'expérience établit, et ce qu'elle n'établit pas", "",
        "**Elle établit** :", "",
        (f"- **ce que la règle 7 coupe réellement** : {bilan_coupes['coupes']} lignes, dont "
         f"{bilan_coupes['mauvaises']} à tort, pour "
         f"{signe(bilan_coupes['ecart'])} {EURO} — § 2 ;" if b["coupes"]
         else "- que la règle 7 **ne s'est jamais déclenchée** sur la fenêtre jouée — § 2 ;"),
        (f"- ce que chaque règle coûte en frais — {fr(d['frais'])} {EURO} contre "
         f"{fr(ni['frais'])} {EURO} sans les règles 4 et 6 — § 5 ;"),
        (f"- les taux de déclenchement des sept règles sur "
         f"{len(d['decisions']) * len(VALEURS)} évaluations — § 6 ;"),
        (f"- ce que la carence a bloqué : {compte['carence_bloquee']} achats — § 1."),
        "", "**Elle n'établit pas** :", "",
        (f"- que la règle 7 améliore la règle : l'écart d'alpha vaut "
         f"{signe(d['alpha'] - sans_r7['alpha'])} pt, à comparer à un EMD de "
         f"± {fr(mde_app, 1)} pt ;"),
        ("- que le seuil de −15 % est le bon : il n'a pas été fait varier, et le faire "
         "varier jusqu'à trouver mieux serait la faute que le protocole s'interdit ;"),
        ("- que ces dix valeurs représentent le CAC 40 : un seul tirage, dont la dispersion "
         "n'est pas mesurée."),
        "", "---", "",
        (f"[← Protocole](README.md) · [{b['annees'][0]}]({RAPPORTS}/{b['annees'][0]}.md) · "
         f"[{b['annees'][-1]}]({RAPPORTS}/{b['annees'][-1]}.md)"),
    ]
    return NL_.join(out) + NL_


# --------------------------------------------------------------------------
# Assemblage


def construire(serie):
    debut_evaluable = next(j for j in serie["jours"]
                           if all(evaluer(serie, t, j) for t in VALEURS))
    fin = serie["jours"][-1]
    variantes = {}
    for nom, avec_r4, avec_r6, avec_r7 in VARIANTES:
        simulation = simuler(serie, DEBUT_NARREE, fin, avec_r4, avec_r6, avec_r7)
        variantes[nom] = resumer(serie, simulation, DEBUT_NARREE, fin)
    declaree = variantes["declaree"]
    replis = replis_courants(serie, declaree, fin)
    lignes_issues = issues(serie, declaree["decisions"], fin, replis)
    return {
        **declaree, "variantes": variantes, "debut": declaree["seances"][0], "fin": fin,
        "index": {j: i for i, j in enumerate(declaree["seances"])},
        "mesurees": mesurer_positions(serie, declaree, fin),
        "coupes": contrefactuel_r7(serie, declaree, variantes["sans regle 7"], fin),
        "replis": replis, "issues": lignes_issues,
        "comparaisons": {cle: comparer(lignes_issues, pop, grp)
                         for cle, _l, _a, _b, pop, grp in COMPARAISONS},
        "etalonnage": etalonnage(serie, debut_evaluable),
        "annees": sorted({j[:4] for j in declaree["seances"]}),
    }


def ecrire_csvs(repertoire, serie, b):
    seuils = {}
    for p in b["positions"]:
        seuils.setdefault(p["ticker"], []).append(
            (p["decision"], p["sortie"] or b["fin"], p["seuil4"], p["seuil7"]))
    carences = {}
    for c in b["carences"]:
        carences.setdefault(c["ticker"], []).append((c["depuis"], c["jusqua"]))
    lignes = []
    for indice, jour in enumerate(b["decisions"]):
        i = serie["rang"][jour]
        execution = serie["jours"][i + 1] if i + 1 < len(serie["jours"]) else None
        for ticker in VALEURS:
            ev = evaluer(serie, ticker, jour)
            if ev is None:
                continue
            actifs = [(s4, s7) for debut, sortie, s4, s7 in seuils.get(ticker, [])
                      if debut <= jour <= sortie]
            franchi4 = any(s4 is not None and ev["close"] < s4 for s4, _s7 in actifs)
            franchi7 = any(s7 is not None and ev["close"] < s7 for _s4, s7 in actifs)
            en_carence = any(depuis <= indice < jusqua
                             for depuis, jusqua in carences.get(ticker, []))
            lignes.append({
                "DATE": jour, "TICKER": ticker, "EXECUTION": execution,
                "CLOSE_AJUSTE": arrondi(ev["close"]),
                "CLOSE_REEL": arrondi(reel(serie, ticker, jour, "Close")),
                "VAL_120": arrondi(ev["val"]), "S_120": arrondi(ev["s120"]),
                "ECART_S": arrondi(ev["ecart"]), "TAUX_120": arrondi(ev["taux120"]),
                "TAUX_20": arrondi(ev["taux20"]), "SOUS_BAS": oui(ev["ecart"] < -K),
                "AU_DESSUS": oui(ev["ecart"] > K), "SEUIL_4_FRANCHI": oui(franchi4),
                "SEUIL_7_FRANCHI": oui(franchi7),
                "REPLI_COURANT": arrondi(b["replis"].get((ticker, jour))),
                "EN_CARENCE": oui(en_carence),
                "SIGNAL": verdict_du_jour(ev)})
    ecrire_csv(repertoire / "decisions.csv", ENTETE_DECISIONS, lignes)
    ecrire_csv(repertoire / "ordres.csv", ENTETE_ORDRES, [
        {**o, "PRIX_REEL": arrondi(o["PRIX_REEL"]), "BRUT": arrondi(o["BRUT"]),
         "FRAIS": arrondi(o["FRAIS"]), "NET": arrondi(o["NET"]),
         "ECART_S": arrondi(o["ECART_S"]), "TAUX_20": arrondi(o["TAUX_20"])}
        for o in b["ordres"]])
    ecrire_csv(repertoire / "positions.csv", ENTETE_POSITIONS, [
        {"TICKER": p["ticker"], "ACHAT": p["achat"], "SORTIE": p["sortie"],
         "MOTIF": p["motif"] or "ouverte", "TRANCHES": p["tranches"],
         "QUANTITE": p["quantite"], "PRIX_PREMIERE_TRANCHE": arrondi(p["prix1"]),
         "PRIX_ACHAT": arrondi(p["prix_moyen"]),
         "PRIX_SORTIE": arrondi(p["prix_sortie_effectif"]),
         "SEUIL_REGLE_4": arrondi(p["seuil4"]), "SEUIL_REGLE_7": arrondi(p["seuil7"]),
         "SEANCES": p["seances"], "PLUS_VALUE": arrondi(p["plus_value"]),
         "REPLI_PREMIERE": arrondi(p["repli_premiere"]),
         "REPLI_MOYEN": arrondi(p["repli_moyen"]), "REPLI_LOW": arrondi(p["repli_low"]),
         "CONTRIBUTION": arrondi(p["contribution"])}
        for p in b["mesurees"]])
    ecrire_csv(repertoire / "portefeuille.csv", ENTETE_PORTEFEUILLE, [
        {"DATE": j, "ESPECES": round(b["valeurs"][j][0], 2),
         "TITRES": round(b["valeurs"][j][1], 2), "TOTAL": round(b["valeurs"][j][2], 2),
         "BASE100": round(100 * b["valeurs"][j][2] / DOTATION, 4),
         "APPARIEE100": round(b["appariee"][i], 4),
         "DETENTION100": round(b["detention"][i], 4),
         "PART_INVESTIE": round(100 * b["valeurs"][j][1] / b["valeurs"][j][2], 4),
         "LIGNES_OUVERTES": b["valeurs"][j][3]}
        for i, j in enumerate(b["seances"])])
    ecrire_csv(repertoire / "issues.csv", ENTETE_ISSUES, [
        {**li, "SOUS_BAS": oui(li["SOUS_BAS"]),
         "TAUX_20_POSITIF": oui(li["TAUX_20_POSITIF"]),
         "AU_DESSUS_HAUT": oui(li["AU_DESSUS_HAUT"]),
         "REPLI_SOUS_SEUIL": oui(li["REPLI_SOUS_SEUIL"]),
         "SOUS_ECHANTILLON": oui(li["SOUS_ECHANTILLON"]),
         "RENDEMENT_20": arrondi(li["RENDEMENT_20"])}
        for li in b["issues"]])


def bloc_annuel(b, annee):
    seances = [j for j in b["seances"] if j[:4] == annee]
    fin = seances[-1]
    ordres = [o for o in b["ordres"] if o["DATE"][:4] == annee]
    lignes = ["", f"=== {annee} {MEDIAN} {len(seances)} seances ===", ""]
    lignes.append("Ordres" if ordres else "Aucun ordre")
    for o in ordres:
        lignes.append(f"  {o['DATE']} {o['TICKER']:<8s} {o['SENS']:<8s} "
                      f"{o['QUANTITE']:5d} titres a {fr(o['PRIX_REEL']):>9s} EUR "
                      f"{MEDIAN} frais {fr(o['FRAIS']):>7s}")
    total = b["valeurs"][fin][2]
    lignes += ["", (f"Portefeuille au {fin} : {fr(total)} EUR {MEDIAN} base "
                    f"{fr(100 * total / DOTATION)} {MEDIAN} appariee "
                    f"{fr(b['appariee'][b['index'][fin]])} {MEDIAN} detention "
                    f"{fr(b['detention'][b['index'][fin]])}")]
    return NL_.join(lignes)


def imprimer_bilan(b, compares):
    d = b["variantes"]["declaree"]
    sans_r7 = b["variantes"]["sans regle 7"]
    compte = d["compte"]
    coupes = compter_coupes(b["coupes"])
    ouvertes = sum(1 for p in b["mesurees"] if p["ouverte"])
    print(f"""
=== Bilan au {b['fin']} ===

  Performance             {signe(d['base'][-1] - 100)} %  (appariee \
{signe(d['appariee'][-1] - 100)} %, detention {signe(d['detention'][-1] - 100)} %)
  Alpha officiel          {signe(d['alpha'])} pt (TE {fr(d['te_app'])} %/an, \
MDE +/- {fr(Z95 * d['te_app'], 1)} pt)
  Ecart brut              {signe(d['brut'])} pt
  Ordres                  {d['n_ordres']} {d['genres']} {MEDIAN} frais {fr(d['frais'])} EUR
  Part investie           {fr(d['part'], 2)} % {MEDIAN} maximum {fr(d['maximum'], 1)} % \
{MEDIAN} refus especes {compte['refus_especes']} {MEDIAN} bloques par carence \
{compte['carence_bloquee']}
  Positions               {len(b['mesurees'])} dont {ouvertes} ouverte(s)
  REGLE 7                 {coupes['coupes']} coupes, dont {coupes['bonnes']} bonnes et \
{coupes['mauvaises']} mauvaises {MEDIAN} cout {signe(coupes['ecart'])} EUR
                          declenchee {compte['r7_declenchee']} {MEDIAN} en meme temps que \
la regle 4 {compte['r7_et_r4']}
  Sans la regle 7         base {fr(sans_r7['base'][-1])} {MEDIAN} alpha \
{signe(sans_r7['alpha'])} pt {MEDIAN} part investie {fr(sans_r7['part'], 2)} % \
{MEDIAN} ecart d'alpha {signe(d['alpha'] - sans_r7['alpha'])} pt
  Declenchements          sous le bord bas {compte['sous_bas']}, dont pente >= 0 \
{compte['sous_bas_pente']} {MEDIAN} au-dessus {compte['au_dessus']}""")
    print("  Par valeur :")
    for ticker in VALEURS:
        ordres = [o for o in d["ordres"] if o["TICKER"] == ticker]
        positions = [p for p in b["mesurees"] if p["ticker"] == ticker]
        coupees = sum(1 for p in positions if p["motif"] == "REGLE-7")
        print(f"    {ticker:<9s} {len(ordres):2d} ordres {MEDIAN} {len(positions)} positions "
              f"{MEDIAN} {coupees} coupe(s) {MEDIAN} contribution "
              f"{signe(sum(p['contribution'] for p in positions))} EUR")
    print("  Issues, par grappes de dates :")
    for cle, libelle, *_r in COMPARAISONS:
        c = b["comparaisons"][cle]
        print(f"    {libelle:<22s} {c['dates']:3d} dates {MEDIAN} "
              f"{signe(c['difference'])} +/- {fr(c['ic'])} pt")
    print(f"  Reproduction : {compares} evaluations confrontees a l'experience 9, 0 ecart"
          if compares else "  Reproduction : decisions.csv de l'experience 9 absent")
    for nom, cle, publie, calcule in ecarts_publies(b["etalonnage"]):
        print(f"  ECART ETALONNAGE {nom} {cle} : publie {publie}, moteur {calcule}")
    print()


def analyser_arguments():
    ici = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Journal de l'experience 10 : dix valeurs tirees au sort, "
                    "et une coupe a -15 %.")
    parser.add_argument("--figures", action="store_true", help="Ecrire les figures de canal")
    parser.add_argument("--markdown", action="store_true",
                        help="Ecrire les figures, les journaux annuels et le bilan")
    parser.add_argument("--annee", help="N'afficher que cette annee (AAAA)")
    parser.add_argument("--repertoire", type=Path, default=ici, help="Ou lire et ecrire")
    parser.add_argument("--quotes", type=Path, default=QUOTES_DEFAUT, help="Ou sont les series")
    args = parser.parse_args()
    if not args.quotes.is_dir():
        erreur(f"Repertoire introuvable : {args.quotes}")
    return args


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    args = analyser_arguments()
    controler_univers(args.repertoire)
    serie = charger(args.quotes)
    compares = controler_evaluations_experience_9(serie)
    b = construire(serie)
    if args.annee and args.annee not in b["annees"]:
        erreur(f"--annee doit etre l'une de : {', '.join(b['annees'])}")
    ecrire_csvs(args.repertoire, serie, b)
    ecrits = ["decisions.csv", "ordres.csv", "positions.csv", "portefeuille.csv", "issues.csv"]
    if args.figures or args.markdown:
        ecrits.append(f"{ecrire_figures(args.repertoire, serie, b)} figures de canal")
    if args.markdown:
        for i, annee in enumerate(b["annees"]):
            journal_annuel(args.repertoire, b, annee, b["annees"][i - 1] if i else None,
                           b["annees"][i + 1] if i + 1 < len(b["annees"]) else None)
        ecrire_texte(args.repertoire / BILAN, bilan(b, compares))
        ecrits += [f"{RAPPORTS}/AAAA.md ({len(b['annees'])} journaux)",
                   f"{GRAPHIQUES}/portefeuille-AAAA.svg", BILAN]
    for annee in b["annees"]:
        if not args.annee or args.annee == annee:
            print(bloc_annuel(b, annee))
    imprimer_bilan(b, compares)
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
