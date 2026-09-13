"""Moteur de l'experience 11 : les six regles de l'experience 10, sans sa regle 7.

Memes dix valeurs, meme tirage graine 10, meme dimensionnement, meme fenetre. La
regle 5 redevient la seule sortie.

Sa particularite : le resultat est connu AVANT l'ecriture de ce moteur — c'est la
variante « sans la regle 7 » de l'experience 10. Le moteur doit la retrouver ORDRE
PAR ORDRE, et s'arrete sinon.

Convention d'unites : la REGLE se lit sur la serie AJUSTEE, les QUANTITES, les
especes et la valorisation sur les cours REELS.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_11/journal.py
    python docs/done/experimentation/experience_11/journal.py --figures
    python docs/done/experimentation/experience_11/journal.py --markdown
    python docs/done/experimentation/experience_11/journal.py --annee 2023
"""

import argparse
import csv
import datetime
import importlib.util
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
MOTEUR_EXP_10 = Path("docs/done/experimentation/experience_10/journal.py")
COMMUNES_EXP_9 = ("ENGI.PA", "SAF.PA")

GRAINE = 10
DOTATION = 10000.0
PART_ACHAT, PART_RENFORT = 0.10, 0.20
PLAFOND = 1.0
DEBUT_NARREE = "2022-01-03"
FIN_ETALONNAGE = "2021-12-31"
LONGUE, COURTE, K = 120, 20, 1.0
HORIZON, PAS_ECHANTILLON = 20, 4
COURTAGE, SPREAD, TTF = 0.10, 0.015, 0.30
Z95 = 1.96
TOLERANCE_REPRODUCTION = 5e-4

VARIANTES = (("declaree", True, True), ("sans regle 4", False, True),
             ("sans regle 6", True, False), ("ni regle 4 ni regle 6", False, False))
LIBELLE_VARIANTE = {"declaree": "**Déclarée** — règles 4 et 6",
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

# L'etalonnage 2019-2021, publie au protocole. Les trois dernieres variantes sont
# nouvelles : celles de l'experience 10 gardaient sa regle 7.
ETALONNAGE_PUBLIE = {
    "declaree": {"base": 123.01, "detention": 130.39, "appariee": 115.25, "alpha": 7.77,
                 "ordres": 75, "frais": 257.8, "part": 33.84, "maximum": 100.0},
    "sans regle 4": {"base": 120.82, "detention": 130.39, "appariee": 116.07, "alpha": 4.76,
                     "ordres": 61, "frais": 198.19, "part": 25.98, "maximum": 95.8},
    "sans regle 6": {"base": 120.37, "detention": 130.39, "appariee": 112.93, "alpha": 7.44,
                     "ordres": 72, "frais": 222.85, "part": 28.64, "maximum": 95.1},
    "ni regle 4 ni regle 6": {"base": 111.92, "detention": 130.39, "appariee": 107.08,
                              "alpha": 4.84, "ordres": 56, "frais": 141.82, "part": 20.17,
                              "maximum": 57.1},
    "taux": {"decisions": 133, "evaluations": 1330, "sous_bas": 309, "sous_bas_pente": 58,
             "au_dessus": 289, "r4_possible": 16, "r6_possible": 5, "meme_semaine": 0,
             "refus_especes": 2, "positions": 29, "closes": 27, "te_app": 5.71,
             "te_det": 16.28},
}

# Le resultat de la FENETRE JOUEE, publie en tete du protocole parce qu'il etait
# deja connu : aucune experience anterieure ne pouvait se confronter ainsi.
RESULTAT_PUBLIE = {"base": 118.29, "appariee": 128.06, "detention": 176.91, "alpha": -9.77,
                   "ordres": 112, "frais": 387.26, "part": 35.01, "maximum": 99.9,
                   "positions": 41, "closes": 38, "refus_especes": 11}

COLONNES = ("Open", "High", "Low", "Close", "E_120", "VAR_120", "CORR_120", "VAL_120",
            "E_20", "VAR_20", "CORR_20", "VAL_20")
ENTETE_DECISIONS = ["DATE", "TICKER", "EXECUTION", "CLOSE_AJUSTE", "CLOSE_REEL", "VAL_120",
                    "S_120", "ECART_S", "TAUX_120", "TAUX_20", "SOUS_BAS", "AU_DESSUS",
                    "SEUIL_4_FRANCHI", "REPLI_COURANT", "SIGNAL"]
ENTETE_ORDRES = ["DATE", "DATE_DECISION", "TICKER", "SENS", "RANG_SERVICE", "QUANTITE",
                 "PRIX_REEL", "BRUT", "FRAIS", "NET", "ECART_S", "TAUX_20", "MOTIF"]
ENTETE_POSITIONS = ["TICKER", "ACHAT", "SORTIE", "MOTIF", "TRANCHES", "QUANTITE",
                    "PRIX_PREMIERE_TRANCHE", "PRIX_ACHAT", "PRIX_SORTIE", "SEUIL_REGLE_4",
                    "SEANCES", "PLUS_VALUE", "REPLI_PREMIERE", "REPLI_MOYEN", "REPLI_LOW",
                    "CONTRIBUTION"]
ENTETE_PORTEFEUILLE = ["DATE", "ESPECES", "TITRES", "TOTAL", "BASE100", "APPARIEE100",
                       "DETENTION100", "PART_INVESTIE", "LIGNES_OUVERTES"]
ENTETE_ISSUES = ["DATE", "TICKER", "SOUS_BAS", "TAUX_20_POSITIF", "AU_DESSUS_HAUT",
                 "SOUS_ECHANTILLON", "RENDEMENT_20"]

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
# Les trois controles de reproduction


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
    """ENGI.PA et SAF.PA sont communes aux experiences 9, 10 et 11 : elles coincident."""
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


def controler_ordres_experience_10(serie, ordres, fin):
    """Les ordres doivent coincider UN PAR UN avec la variante sans regle 7 de l'exp 10.

    C'est le controle le plus strict du depot : meme univers, meme dimensionnement,
    meme fenetre, donc meme portefeuille — les QUANTITES elles-memes doivent coincider,
    la ou l'experience 9 ne pouvait comparer que des dates a l'experience 8.
    """
    if not MOTEUR_EXP_10.exists():
        return None
    spec = importlib.util.spec_from_file_location("experience_10", MOTEUR_EXP_10)
    voisin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(voisin)
    temoins = voisin.simuler(serie, DEBUT_NARREE, fin, True, True, False)["ordres"]
    if len(temoins) != len(ordres):
        erreur(f"Reproduction rompue : {len(ordres)} ordres ici, {len(temoins)} dans la "
               "variante sans regle 7 de l'experience 10", code=2)
    champs = ("DATE", "TICKER", "SENS", "QUANTITE")
    for rang, (mien, temoin) in enumerate(zip(ordres, temoins, strict=True), start=1):
        for champ in champs:
            if mien[champ] != temoin[champ]:
                erreur(f"Reproduction rompue a l'ordre {rang} : {champ} vaut "
                       f"{mien[champ]} ici et {temoin[champ]} dans l'experience 10", code=2)
        if abs(mien["PRIX_REEL"] - temoin["PRIX_REEL"]) > TOLERANCE_REPRODUCTION:
            erreur(f"Reproduction rompue a l'ordre {rang} : PRIX_REEL vaut "
                   f"{mien['PRIX_REEL']:.6f} ici et {temoin['PRIX_REEL']:.6f} dans "
                   "l'experience 10", code=2)
    return len(temoins)


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


def verdict_du_jour(ev, seuil4=None):
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


def motif_ordre(genre, ticker, ev):
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
    }
    return textes[genre]


def ecrire_ordre(jour, decision, ticker, genre, place, quantite, prix, brut, frais, ev, net):
    return {"DATE": jour, "DATE_DECISION": decision, "TICKER": ticker, "SENS": genre,
            "RANG_SERVICE": place, "QUANTITE": quantite, "PRIX_REEL": prix, "BRUT": brut,
            "FRAIS": frais, "NET": net, "ECART_S": ev["ecart"], "TAUX_20": ev["taux20"],
            "MOTIF": motif_ordre(genre, ticker, ev)}


def etat_neuf():
    return {"titres": dict.fromkeys(VALEURS, 0), "seuil4": dict.fromkeys(VALEURS, None),
            "decision_achat": dict.fromkeys(VALEURS, None),
            "r4_fait": dict.fromkeys(VALEURS, False),
            "r6_fait": dict.fromkeys(VALEURS, False),
            "ouverte": dict.fromkeys(VALEURS, None)}


def collecter(serie, etat, veille, rang, total, options, compte):
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
        detenue = etat["titres"][ticker] > 0
        if detenue and ev["ecart"] > K:
            ventes.append((ticker, ev))
        elif not detenue and ev["ecart"] < -K and ev["taux20"] >= 0:
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


def simuler(serie, debut, fin, avec_r4=True, avec_r6=True):
    decisions = decisions_hebdomadaires(serie, debut, fin)
    if not decisions:
        erreur(f"Aucune decision hebdomadaire entre {debut} et {fin}")
    rang = {d: i for i, d in enumerate(decisions)}
    seances = [j for j in serie["jours"] if debut <= j <= fin]
    etat = etat_neuf()
    especes = DOTATION
    ordres, valeurs, positions = [], {}, []
    compte = dict.fromkeys(("sous_bas", "sous_bas_pente", "au_dessus", "r4_possible",
                            "r6_possible", "meme_semaine", "refus_especes"), 0)

    for i, jour in enumerate(seances):
        veille = seances[i - 1] if i else None
        if veille is not None:
            for ticker in VALEURS:            # attributions d'actions gratuites
                for date, ratio in serie["par_ticker"][ticker]["splits"]:
                    if date == jour and etat["titres"][ticker]:
                        etat["titres"][ticker] = int(etat["titres"][ticker] * ratio)
            if veille in rang:
                total = valeurs[veille][2]
                ventes, achats = collecter(serie, etat, veille, rang, total,
                                           (avec_r4, avec_r6), compte)
                for place, (ticker, ev) in enumerate(ventes, start=1):
                    prix = reel(serie, ticker, jour, "Open")
                    quantite = etat["titres"][ticker]
                    brut = quantite * prix
                    frais = brut * taux_vente()
                    especes += brut - frais
                    ordres.append(ecrire_ordre(jour, veille, ticker, "VENTE", place,
                                               quantite, prix, brut, frais, ev, -frais))
                    position = etat["ouverte"][ticker]
                    if position is not None:
                        position.update({"sortie": jour, "prix_sortie": prix,
                                         "motif": "VENTE", "recu": brut - frais})
                    etat["titres"][ticker] = 0
                    etat["seuil4"][ticker] = None
                    etat["decision_achat"][ticker] = None
                    etat["r4_fait"][ticker] = etat["r6_fait"][ticker] = False
                    etat["ouverte"][ticker] = None
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
                        etat["seuil4"][ticker] = ev["close"] - ev["s120"]
                        etat["decision_achat"][ticker] = veille
                        etat["r4_fait"][ticker] = etat["r6_fait"][ticker] = False
                        position = {"ticker": ticker, "achat": jour, "decision": veille,
                                    "quantite": quantite, "brut": brut, "frais": frais,
                                    "investi": brut + frais, "tranches": 1,
                                    "prix1": prix / facteur(serie, ticker, jour),
                                    "seuil4": etat["seuil4"][ticker], "sortie": None,
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
            "decisions": decisions, "compte": compte}


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
              for g in ("ACHAT", "REGLE-4", "RENFORT", "VENTE")}
    return {**simulation, "base": base, "appariee": app, "detention": ref,
            "reference": reference, "part": statistics.fmean(parts), "maximum": max(parts),
            "frais": sum(o["FRAIS"] for o in simulation["ordres"]),
            "n_ordres": len(simulation["ordres"]), "genres": genres,
            "alpha": base[-1] - app[-1], "brut": base[-1] - ref[-1],
            "te_app": ecart_type(base, app), "te_det": ecart_type(base, ref)}


# --------------------------------------------------------------------------
# Les positions mesurees


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
)


def issues(serie, decisions, borne):
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
            lignes.append({"DATE": jour, "TICKER": ticker, "SOUS_BAS": ev["ecart"] < -K,
                           "TAUX_20_POSITIF": ev["taux20"] >= 0,
                           "AU_DESSUS_HAUT": ev["ecart"] > K,
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
# L'etalonnage et le resultat, confrontes


def egal(publie, calcule):
    if calcule is None:
        return False
    if isinstance(publie, float):
        decimales = len(repr(publie).split(".")[1])
        return round(calcule, decimales) == round(publie, decimales)
    return calcule == publie


def etalonnage(serie, debut):
    """Rejoue les quatre variantes sur 2019-2021 et rend les nombres a confronter."""
    resultats = {}
    for nom, avec_r4, avec_r6 in VARIANTES:
        simulation = simuler(serie, debut, FIN_ETALONNAGE, avec_r4, avec_r6)
        resultats[nom] = resumer(serie, simulation, debut, FIN_ETALONNAGE)
    declaree = resultats["declaree"]
    compte = declaree["compte"]
    resultats["taux"] = {
        "decisions": len(declaree["decisions"]),
        "evaluations": len(declaree["decisions"]) * len(VALEURS),
        "sous_bas": compte["sous_bas"], "sous_bas_pente": compte["sous_bas_pente"],
        "au_dessus": compte["au_dessus"], "r4_possible": compte["r4_possible"],
        "r6_possible": compte["r6_possible"], "meme_semaine": compte["meme_semaine"],
        "refus_especes": compte["refus_especes"],
        "positions": len(declaree["positions"]),
        "closes": sum(1 for p in declaree["positions"] if p["sortie"]),
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
    return ecarts


def ecarts_resultat(b):
    """Le resultat de la fenetre jouee etait connu : il se confronte comme l'etalonnage."""
    d = b["variantes"]["declaree"]
    closes = sum(1 for p in b["mesurees"] if not p["ouverte"])
    obtenus = {"base": d["base"][-1], "appariee": d["appariee"][-1],
               "detention": d["detention"][-1], "alpha": d["alpha"],
               "ordres": d["n_ordres"], "frais": d["frais"], "part": d["part"],
               "maximum": d["maximum"], "positions": len(b["mesurees"]), "closes": closes,
               "refus_especes": d["compte"]["refus_especes"]}
    return [(cle, publie, obtenus[cle]) for cle, publie in RESULTAT_PUBLIE.items()
            if not egal(publie, obtenus[cle])]


# --------------------------------------------------------------------------
# Les figures


def pas_lisible(amplitude, cibles=6):
    brut = max(amplitude / cibles, 1e-12)
    puissance = 10 ** math.floor(math.log10(brut))
    for multiple in (1, 2, 2.5, 5, 10):
        if multiple * puissance >= brut:
            return multiple * puissance
    return 10 * puissance


def figure_canal(chemin, serie, ticker, jour, seuil4=None):
    """Bande 120, enveloppe des residus 20, seuil de la regle 4. Aucun seuil rouge."""
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
    if seuil4 is not None:
        points.append(seuil4)
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

    verdict = verdict_du_jour(ev, seuil4)
    couleur = {"candidate à l'achat": "#2e7d32", "au-dessus du bord haut": "#c62828",
               "sous le seuil de la règle 4": "#2e7d32"}.get(verdict, "#1a1a1a")
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
    if seuil4 is not None:
        out.append(f'<line x1="{marge_g}" y1="{y(seuil4):.1f}" x2="{largeur - marge_d}" '
                   f'y2="{y(seuil4):.1f}" stroke="#7b1fa2" stroke-width="1.4" '
                   f'stroke-dasharray="8 4"/>')
        out.append(f'<text x="{largeur - marge_d}" y="{y(seuil4) - 5:.1f}" font-size="10.5" '
                   f'fill="#7b1fa2" text-anchor="end">seuil r&#232;gle 4 '
                   f'{fr(seuil4)}</text>')
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
         f'Experience 11 &#8212; les six regles seules, base 100 au {debut}</text>'),
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
    """Le seuil de la regle 4 de chaque position, rattache aux decisions qu'il a servies."""
    seuils = {}
    for p in b["positions"]:
        for o in b["ordres"]:
            if (o["TICKER"] == p["ticker"] and o["SENS"] in ("REGLE-4", "RENFORT")
                    and o["DATE_DECISION"] >= p["decision"]
                    and (p["sortie"] is None or o["DATE"] <= p["sortie"])):
                seuils[(p["ticker"], o["DATE_DECISION"])] = p["seuil4"]
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
        chemin = repertoire / GRAPHIQUES / ticker / f"canal-{jour}.svg"
        if figure_canal(chemin, serie, ticker, jour, seuils.get((ticker, jour))):
            ecrites += 1
    return ecrites


# --------------------------------------------------------------------------
# Les markdown


def tableau_variantes(b):
    out = [("| Variante | Base 100 | Appariée | **Alpha officiel** | Ordres | Frais "
            "| Part investie | Maximum |"),
           "|---|---|---|---|---|---|---|---|"]
    for nom, _r4, _r6 in VARIANTES:
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


def tableau_par_valeur(b):
    out = ["| Valeur | Ordres | Positions | Contribution | Séances détenue |",
           "|---|---|---|---|---|"]
    for ticker in VALEURS:
        ordres = [o for o in b["ordres"] if o["TICKER"] == ticker]
        positions = [p for p in b["mesurees"] if p["ticker"] == ticker]
        out.append(f"| `{ticker}` | {len(ordres)} | {len(positions)} "
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
    bloc = [
        f"# {annee}", "",
        (f"> Journal de l'[expérience 11](../README.md) · {len(seances)} séances · "
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
             lecture_annuelle(b, ordres, positions, total, depart, app), ""]
    navigation = []
    if precedente:
        navigation.append(f"[← {precedente}]({precedente}.md)")
    navigation.append("[Protocole](../README.md)")
    if suivante:
        navigation.append(f"[{suivante} →]({suivante}.md)")
    bloc += ["---", "", " · ".join(navigation)]
    ecrire_texte(repertoire / RAPPORTS / f"{annee}.md", NL_.join(bloc) + NL_)


def lecture_annuelle(b, ordres, positions, total, depart, app):
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


def bilan(b, compares, ordres_confrontes):
    d = b["variantes"]["declaree"]
    ni = b["variantes"]["ni regle 4 ni regle 6"]
    mde_app = Z95 * d["te_app"]
    ouvertes = [p for p in b["mesurees"] if p["ouverte"]]
    closes = [p for p in b["mesurees"] if not p["ouverte"]]
    compte = d["compte"]
    ecarts = ecarts_publies(b["etalonnage"])
    ecarts_r = ecarts_resultat(b)
    qualite = ("*indiscernable de zéro*" if abs(d["alpha"]) <= mde_app
               else "*au-delà de son effet minimal détectable*")
    out = [
        "# Bilan de l'expérience 11", "",
        (f"> [Expérience 11](README.md) · les six règles seules, sans la coupe à −15 % · "
         f"**{signe(d['base'][-1] - 100)} %** · alpha officiel "
         f"**{signe(d['alpha'])} pt**"), "",
        ("> ⚠️ **Ce résultat était connu avant que ce moteur soit écrit** : c'est la "
         "variante « sans la règle 7 » de l'[expérience 10](../experience_10/bilan.md). "
         "Le [protocole](README.md#️-ce-que-cette-expérience-est-et-ce-quelle-nest-pas) le "
         "publie en tête, et le § 8 confronte le moteur à ce chiffre publié."),
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
        (f"| **Ordres refusés faute d'espèces** | **{compte['refus_especes']}** |"),
        (f"| Décisions · évaluations | {len(d['decisions'])} · "
         f"{len(d['decisions']) * len(VALEURS)} |"),
        (f"| Positions · closes · encore ouvertes | {len(b['mesurees'])} · "
         f"{len(closes)} · {len(ouvertes)} |"),
        "", "## 2. Les positions", "", *tableau_positions(b["mesurees"]),
        "", "## 3. Ce que chaque valeur a apporté", "", *tableau_par_valeur(b),
        "", "## 4. Ce que coûte l'absence de sortie en perte", "",
        ("> La règle 5 est redevenue la seule sortie : une position qui ne revient pas dans "
         "sa bande reste ouverte."), "",
        "| Mesure | Valeur |", "|---|---|",
        f"| **Lignes jamais revendues** au {b['fin']} | **{len(ouvertes)}** |",
        (f"| Repli maximal le plus profond, depuis la 1<sup>re</sup> tranche | "
         f"{signe(min((p['repli_premiere'] for p in b['mesurees']), default=None))} % |"),
        (f"| Durée médiane d'une position close | "
         f"{fr(statistics.median([p['seances'] for p in closes]), 0) if closes else '—'} "
         "séances |"),
        ("| Valeurs encore détenues | "
         + (", ".join(f"`{p['ticker']}`" for p in ouvertes) if ouvertes else "—") + " |"),
        "", "## 5. Ce qu'ajoutent les règles 4 et 6", "", *tableau_variantes(b), "",
        (f"Ensemble, elles portent la part investie de {fr(ni['part'], 2)} % à "
         f"{fr(d['part'], 2)} %, les frais de {fr(ni['frais'])} {EURO} à "
         f"{fr(d['frais'])} {EURO}, et le maximum de {fr(ni['maximum'], 1)} % à "
         f"{fr(d['maximum'], 1)} %."),
        "", "## 6. Les taux de déclenchement", "",
        (f"> Sur {len(d['decisions'])} décisions et "
         f"{len(d['decisions']) * len(VALEURS)} évaluations de valeur."), "",
        "| Règle | Déclenchée | Exécutée |", "|---|---|---|",
        (f"| **3** — sous le bord bas et `TAUX_20 ≥ 0` | {compte['sous_bas_pente']} "
         f"| {d['genres']['ACHAT']} |"),
        f"| **4** — sous le seuil figé | {compte['r4_possible']} | {d['genres']['REGLE-4']} |",
        f"| **6** — renforcement | {compte['r6_possible']} | {d['genres']['RENFORT']} |",
        f"| **5** — au-dessus du bord haut | {compte['au_dessus']} | {d['genres']['VENTE']} |",
        "",
        ("> **Un compteur qui se lit de travers.** Dans les variantes où la règle 4 est "
         "désactivée, `règle 4 possible` enfle — le compteur mesure les semaines où elle "
         "*aurait pu* jouer, et une règle qui ne joue pas laisse la position sous son seuil "
         "semaine après semaine, chacune étant recomptée. Seul le nombre de la variante "
         "déclarée est un taux de déclenchement."),
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
        "", "## 8. L'étalonnage et le résultat, publiés avant, recalculés après", "",
        ("| Variante | Base publiée | Base recalculée | Alpha publié | Alpha recalculé "
         "| Concorde |"),
        "|---|---|---|---|---|---|",
    ]
    for nom, _r4, _r6 in VARIANTES:
        publie = ETALONNAGE_PUBLIE[nom]
        obtenu = b["etalonnage"][nom]
        manque = any(e[0] == nom for e in ecarts)
        out.append(f"| {LIBELLE_VARIANTE[nom]} | {fr(publie['base'])} "
                   f"| {fr(obtenu['base'][-1])} | {signe(publie['alpha'])} pt "
                   f"| {signe(obtenu['alpha'])} pt | {'✗' if manque else '✓'} |")
    total_publies = sum(len(v) for v in ETALONNAGE_PUBLIE.values()) + len(RESULTAT_PUBLIE)
    out += [
        "",
        (f"**{total_publies - len(ecarts) - len(ecarts_r)} nombres publiés sur "
         f"{total_publies}** sont retrouvés à l'identique — l'étalonnage 2019-2021 **et** "
         "le résultat de la fenêtre jouée, que le protocole publiait en tête."
         if not ecarts and not ecarts_r else
         f"**{len(ecarts) + len(ecarts_r)} nombres publiés sur {total_publies} ne sont pas "
         "retrouvés.** Les écarts sont listés en console."),
        "", "### Les trois contrôles de reproduction", "",
        "| Contrôle | Résultat |", "|---|---|",
        f"| La permutation se rejoue depuis la graine {GRAINE} | ✓ |",
        (f"| Les évaluations d'`ENGI.PA` et `SAF.PA` contre l'expérience 9 | "
         f"**{compares} comparées, 0 écart** |" if compares
         else "| Les évaluations contre l'expérience 9 | *`decisions.csv` absent* |"),
        (f"| ⚠️ **Les ordres, un par un, contre l'expérience 10** | "
         f"**{ordres_confrontes} confrontés, 0 écart** |" if ordres_confrontes
         else "| Les ordres contre l'expérience 10 | *contrôle sauté, moteur absent* |"),
        "", "## 9. Ce que l'expérience établit, et ce qu'elle n'établit pas", "",
        "**Elle établit** :", "",
        (f"- le détail que l'expérience 10 résumait en une ligne : {len(b['mesurees'])} "
         f"positions, {d['n_ordres']} ordres, la contribution de chaque valeur — § 2 et 3 ;"),
        (f"- que **{compte['refus_especes']} ordres ont été refusés faute d'espèces**, "
         "contre un seul avec la règle 7 : sans coupe, le portefeuille manque de "
         "liquidités au moment où un signal se présente — § 1 ;"),
        (f"- ce que l'absence de sortie en perte laisse ouvert : {len(ouvertes)} ligne"
         f"{'s' if len(ouvertes) > 1 else ''} jamais revendue"
         f"{'s' if len(ouvertes) > 1 else ''} — § 4 ;"),
        ("- que le moteur reproduit **ordre par ordre** la variante de l'expérience 10 — "
         "§ 8."),
        "", "**Elle n'établit pas** :", "",
        ("- quoi que ce soit de neuf sur la performance : **republier un nombre ne le "
         "confirme pas**, et ce résultat était connu avant l'écriture du moteur ;"),
        (f"- que la règle bat la détention : l'alpha officiel vaut {signe(d['alpha'])} point "
         f"pour un effet minimal détectable de ± {fr(mde_app, 1)} ;"),
        ("- que retirer la règle 7 rend la règle bonne : elle récupère 4,00 points d'alpha "
         "et reste au-dessous de son exposition."),
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
    for nom, avec_r4, avec_r6 in VARIANTES:
        simulation = simuler(serie, DEBUT_NARREE, fin, avec_r4, avec_r6)
        variantes[nom] = resumer(serie, simulation, DEBUT_NARREE, fin)
    declaree = variantes["declaree"]
    lignes_issues = issues(serie, declaree["decisions"], fin)
    return {
        **declaree, "variantes": variantes, "debut": declaree["seances"][0], "fin": fin,
        "index": {j: i for i, j in enumerate(declaree["seances"])},
        "mesurees": mesurer_positions(serie, declaree, fin),
        "replis": replis_courants(serie, declaree, fin),
        "issues": lignes_issues,
        "comparaisons": {cle: comparer(lignes_issues, pop, grp)
                         for cle, _l, _a, _b, pop, grp in COMPARAISONS},
        "etalonnage": etalonnage(serie, debut_evaluable),
        "annees": sorted({j[:4] for j in declaree["seances"]}),
    }


def ecrire_csvs(repertoire, serie, b):
    seuils = {}
    for p in b["positions"]:
        seuils.setdefault(p["ticker"], []).append(
            (p["decision"], p["sortie"] or b["fin"], p["seuil4"]))
    lignes = []
    for jour in b["decisions"]:
        i = serie["rang"][jour]
        execution = serie["jours"][i + 1] if i + 1 < len(serie["jours"]) else None
        for ticker in VALEURS:
            ev = evaluer(serie, ticker, jour)
            if ev is None:
                continue
            franchi = any(s4 is not None and debut <= jour <= sortie and ev["close"] < s4
                          for debut, sortie, s4 in seuils.get(ticker, []))
            lignes.append({
                "DATE": jour, "TICKER": ticker, "EXECUTION": execution,
                "CLOSE_AJUSTE": arrondi(ev["close"]),
                "CLOSE_REEL": arrondi(reel(serie, ticker, jour, "Close")),
                "VAL_120": arrondi(ev["val"]), "S_120": arrondi(ev["s120"]),
                "ECART_S": arrondi(ev["ecart"]), "TAUX_120": arrondi(ev["taux120"]),
                "TAUX_20": arrondi(ev["taux20"]), "SOUS_BAS": oui(ev["ecart"] < -K),
                "AU_DESSUS": oui(ev["ecart"] > K), "SEUIL_4_FRANCHI": oui(franchi),
                "REPLI_COURANT": arrondi(b["replis"].get((ticker, jour))),
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
         "SEUIL_REGLE_4": arrondi(p["seuil4"]), "SEANCES": p["seances"],
         "PLUS_VALUE": arrondi(p["plus_value"]),
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


def imprimer_bilan(b, compares, ordres_confrontes):
    d = b["variantes"]["declaree"]
    ni = b["variantes"]["ni regle 4 ni regle 6"]
    compte = d["compte"]
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
{MEDIAN} refus faute d'especes {compte['refus_especes']}
  Positions               {len(b['mesurees'])} dont {ouvertes} ouverte(s)
  Sans les regles 4 et 6  base {fr(ni['base'][-1])} {MEDIAN} alpha {signe(ni['alpha'])} pt \
{MEDIAN} part investie {fr(ni['part'], 2)} %
  Declenchements          sous le bord bas {compte['sous_bas']}, dont pente >= 0 \
{compte['sous_bas_pente']} {MEDIAN} au-dessus {compte['au_dessus']}""")
    print("  Par valeur :")
    for ticker in VALEURS:
        ordres = [o for o in d["ordres"] if o["TICKER"] == ticker]
        positions = [p for p in b["mesurees"] if p["ticker"] == ticker]
        print(f"    {ticker:<9s} {len(ordres):2d} ordres {MEDIAN} {len(positions)} positions "
              f"{MEDIAN} contribution {signe(sum(p['contribution'] for p in positions))} EUR")
    print("  Issues, par grappes de dates :")
    for cle, libelle, *_r in COMPARAISONS:
        c = b["comparaisons"][cle]
        print(f"    {libelle:<22s} {c['dates']:3d} dates {MEDIAN} "
              f"{signe(c['difference'])} +/- {fr(c['ic'])} pt")
    print("  Controles de reproduction :")
    print(f"    experience 9  : {compares} evaluations, 0 ecart" if compares
          else "    experience 9  : decisions.csv absent, controle saute")
    print(f"    experience 10 : {ordres_confrontes} ordres confrontes un par un, 0 ecart"
          if ordres_confrontes
          else "    experience 10 : moteur absent, controle saute")
    for nom, cle, publie, calcule in ecarts_publies(b["etalonnage"]):
        print(f"  ECART ETALONNAGE {nom} {cle} : publie {publie}, moteur {calcule}")
    for cle, publie, calcule in ecarts_resultat(b):
        print(f"  ECART RESULTAT {cle} : publie {publie}, moteur {calcule}")
    print()


def analyser_arguments():
    ici = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Journal de l'experience 11 : les six regles seules, sans la coupe.")
    parser.add_argument("--figures", action="store_true", help="Ecrire les figures de canal")
    parser.add_argument("--markdown", action="store_true",
                        help="Ecrire les figures, les journaux annuels et le bilan")
    parser.add_argument("--annee", help="N'afficher que cette annee (AAAA)")
    parser.add_argument("--repertoire", type=Path, default=ici, help="Ou lire et ecrire")
    parser.add_argument("--quotes", type=Path, default=QUOTES_DEFAUT, help="Ou sont les series")
    parser.add_argument("--sans-controle-10", action="store_true",
                        help="Sauter le controle ordre par ordre contre l'experience 10")
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
    ordres_confrontes = (None if args.sans_controle_10
                         else controler_ordres_experience_10(serie, b["ordres"], b["fin"]))
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
        ecrire_texte(args.repertoire / BILAN, bilan(b, compares, ordres_confrontes))
        ecrits += [f"{RAPPORTS}/AAAA.md ({len(b['annees'])} journaux)",
                   f"{GRAPHIQUES}/portefeuille-AAAA.svg", BILAN]
    for annee in b["annees"]:
        if not args.annee or args.annee == annee:
            print(bloc_annuel(b, annee))
    imprimer_bilan(b, compares, ordres_confrontes)
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
