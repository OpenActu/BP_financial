"""Moteur de l'experience 8 : Air Liquide seule, une decision par semaine, aucune sortie en perte.

Achete 10 % sous le bord bas quand la pente courte ne baisse pas (regle 3),
achete 10 % de plus si le cours passe 1 s sous ce prix d'achat (regle 4),
renforce une fois de 20 % la semaine suivante (regle 6), et vend au bord haut
(regle 5) — seule sortie de la regle.

Convention d'unites : la REGLE se lit sur la serie AJUSTEE, les QUANTITES, les
especes et la valorisation sur les cours REELS, divisions posterieures retirees.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_8/journal.py
    python docs/done/experimentation/experience_8/journal.py --figures
    python docs/done/experimentation/experience_8/journal.py --markdown
    python docs/done/experimentation/experience_8/journal.py --annee 2023
"""

import argparse
import csv
import datetime
import math
import statistics
import sys
from pathlib import Path

VALEUR = "AI.PA"
SERIE = "AI_PA_2019-01-02_2026-09-11.csv"
QUOTES_DEFAUT = Path("docs/raw/data/quotes")
RAPPORTS = "rapports"
GRAPHIQUES = "graphiques"
BILAN = "bilan.md"

DOTATION = 10000.0
PART_ACHAT = 0.10
PART_RENFORT = 0.20
DEBUT_NARREE = "2022-01-03"
FIN_ETALONNAGE = "2021-12-31"
LONGUE, COURTE, K = 120, 20, 1.0
HORIZON, PAS_ECHANTILLON = 20, 4
COURTAGE, SPREAD, TTF = 0.10, 0.015, 0.30
Z95 = 1.96

VARIANTES = (("declaree", True, True), ("sans regle 4", False, True),
             ("sans regle 6", True, False), ("ni l'une ni l'autre", False, False))
LIBELLE_VARIANTE = {"declaree": "**Déclarée** — règles 4 et 6",
                    "sans regle 4": "Sans la règle 4",
                    "sans regle 6": "Sans la règle 6",
                    "ni l'une ni l'autre": "Ni l'une ni l'autre"}

# Les nombres publies au README avant la fenetre jouee, confrontes au recalcul.
ETALONNAGE_PUBLIE = {
    "declaree": {"base": 100.66, "appariee": 101.71, "alpha": -1.05, "ordres": 11,
                 "frais": 40.29, "part": 6.78, "maximum": 38.7},
    "sans regle 4": {"base": 100.26, "appariee": 101.21, "alpha": -0.95, "ordres": 9,
                     "frais": 30.25, "part": 5.20, "maximum": 28.8},
    "sans regle 6": {"base": 101.14, "appariee": 101.65, "alpha": -0.51, "ordres": 10,
                     "frais": 29.78, "part": 4.44, "maximum": 18.9},
    "ni l'une ni l'autre": {"base": 100.73, "appariee": 101.15, "alpha": -0.41, "ordres": 8,
                            "frais": 19.74, "part": 2.88, "maximum": 10.2},
    "taux": {"decisions": 133, "sous_bas": 29, "sous_bas_pente": 6, "au_dessus": 33,
             "r4_possible": 2, "r6_possible": 1, "meme_semaine": 0, "positions": 4,
             "closes": 4, "te_app": 0.40, "te_det": 21.45},
}

COLONNES = ("Open", "High", "Low", "Close", "E_120", "VAR_120", "CORR_120", "VAL_120",
            "E_20", "VAR_20", "CORR_20", "VAL_20")
ENTETE_DECISIONS = ["DATE", "EXECUTION", "CLOSE_AJUSTE", "CLOSE_REEL", "VAL_120", "S_120",
                    "ECART_S", "TAUX_120", "TAUX_20", "SOUS_BAS", "AU_DESSUS",
                    "SEUIL_FRANCHI", "SIGNAL"]
ENTETE_ORDRES = ["DATE", "DATE_DECISION", "SENS", "QUANTITE", "PRIX_REEL", "BRUT", "FRAIS",
                 "NET", "ECART_S", "TAUX_20", "MOTIF"]
ENTETE_POSITIONS = ["ACHAT", "SORTIE", "MOTIF", "TRANCHES", "QUANTITE", "PRIX_ACHAT",
                    "PRIX_SORTIE", "SEUIL_REGLE_4", "SEANCES", "PLUS_VALUE",
                    "REPLI_CLOTURE", "REPLI_LOW", "CONTRIBUTION"]
ENTETE_PORTEFEUILLE = ["DATE", "ESPECES", "TITRES", "TOTAL", "BASE100", "APPARIEE100",
                       "DETENTION100"]
ENTETE_ISSUES = ["DATE", "SOUS_BAS", "TAUX_20_POSITIF", "AU_DESSUS_HAUT",
                 "SOUS_ECHANTILLON", "RENDEMENT_20"]

NBSP = " "
NL_ = chr(10)
EURO = "€"
MEDIAN = "·"
_OUTILS = {}


def erreur(message):
    print(message, file=sys.stderr)
    sys.exit(1)


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
# La serie, et la de-ajustement des divisions


def charger(quotes):
    chemin = quotes / SERIE
    if not chemin.exists():
        erreur(f"Serie absente : {chemin}\n"
               f"  python python/import_societe.py {VALEUR} --debut 2019-01-02 "
               "--fin 2026-09-13")
    jours, par_jour, splits = [], {}, []
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            if not ligne.get("Close"):
                continue
            jour = ligne["Date"][:10]
            manquantes = [c for c in ("Open", "High", "Low", "Close") if not ligne.get(c)]
            if manquantes:
                erreur(f"{jour} : colonnes absentes de la serie : {', '.join(manquantes)}")
            par_jour[jour] = {c: (float(ligne[c]) if ligne.get(c) else None) for c in COLONNES}
            if float(ligne.get("Stock Splits") or 0):
                splits.append((jour, float(ligne["Stock Splits"])))
            jours.append(jour)
    return {"jours": jours, "par_jour": par_jour, "splits": splits,
            "rang": {j: i for i, j in enumerate(jours)}}


def facteur(serie, jour):
    """Le produit des divisions POSTERIEURES a `jour` : ajuste x facteur = reel."""
    produit = 1.0
    for date, ratio in serie["splits"]:
        if date > jour:
            produit *= ratio
    return produit


def reel(serie, jour, champ):
    return serie["par_jour"][jour][champ] * facteur(serie, jour)


def variance_temps(n):
    return (n * n - 1) / 12


def evaluer(serie, jour):
    """Tout en unites AJUSTEES ; None si la fenetre n'est pas complete."""
    s = serie["par_jour"].get(jour)
    if s is None or any(s[c] is None for c in COLONNES[4:]):
        return None
    if s["VAR_120"] <= 0 or s["VAR_20"] <= 0 or 1 - s["CORR_120"] ** 2 <= 0:
        return None
    if s["E_120"] <= 0 or s["E_20"] <= 0:
        return None
    r120 = s["CORR_120"] * math.sqrt(s["VAR_120"] / variance_temps(LONGUE))
    s120 = math.sqrt(LONGUE / (LONGUE - 2) * s["VAR_120"] * (1 - s["CORR_120"] ** 2))
    r20 = s["CORR_20"] * math.sqrt(s["VAR_20"] / variance_temps(COURTE))
    return {"close": s["Close"], "val": s["VAL_120"], "s120": s120,
            "ecart": (s["Close"] - s["VAL_120"]) / s120,
            "taux120": 100 * r120 / s["E_120"], "taux20": 100 * r20 / s["E_20"],
            "r120": r120, "r20": r20, "val20": s["VAL_20"],
            "s20": math.sqrt(COURTE / (COURTE - 2) * s["VAR_20"]
                             * max(1 - s["CORR_20"] ** 2, 0.0)),
            "e20": s["E_20"]}


def enveloppe(serie, jour):
    """Demi-largeurs de l'enveloppe des COURTE residus, en unites ajustees."""
    i = serie["rang"][jour]
    if i + 1 < COURTE:
        return None
    valeurs = [serie["par_jour"][serie["jours"][j]]["Close"]
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
    """La derniere seance evaluable de chaque semaine civile de la fenetre."""
    par_semaine = {}
    for jour in serie["jours"]:
        if debut <= jour <= fin and evaluer(serie, jour):
            cle = datetime.date.fromisoformat(jour).isocalendar()[:2]
            par_semaine[cle] = jour
    return sorted(par_semaine.values())


def taux_achat():
    return (COURTAGE + SPREAD + TTF) / 100


def taux_vente():
    return (COURTAGE + SPREAD) / 100


# --------------------------------------------------------------------------
# La simulation


def simuler(serie, debut, fin, avec_r4=True, avec_r6=True):
    """Rend les ordres, les valorisations, les positions et les comptes."""
    decisions = decisions_hebdomadaires(serie, debut, fin)
    if not decisions:
        erreur(f"Aucune decision hebdomadaire entre {debut} et {fin}")
    rang = {d: i for i, d in enumerate(decisions)}
    seances = [j for j in serie["jours"] if debut <= j <= fin]
    especes, titres = DOTATION, 0
    ordres, valeurs, positions, signaux = [], {}, [], []
    seuil, decision_achat, r4_fait, r6_fait = None, None, False, False
    compte = dict.fromkeys(("sous_bas", "sous_bas_pente", "au_dessus", "r4_possible",
                            "r6_possible", "meme_semaine", "non_executes"), 0)

    for i, jour in enumerate(seances):
        veille = seances[i - 1] if i else None
        if veille is not None:
            for date, ratio in serie["splits"]:
                if date == jour and titres:
                    titres = int(titres * ratio)
            ev = evaluer(serie, veille)
            a_passer = []
            if veille in rang and ev:
                total = valeurs[veille][2]
                compte["sous_bas"] += ev["ecart"] < -K
                compte["sous_bas_pente"] += ev["ecart"] < -K and ev["taux20"] >= 0
                compte["au_dessus"] += ev["ecart"] > K
                if titres and ev["ecart"] > K:
                    a_passer.append(("VENTE", None))
                elif not titres and ev["ecart"] < -K and ev["taux20"] >= 0:
                    a_passer.append(("ACHAT", PART_ACHAT * total))
                elif titres:
                    r4 = seuil is not None and not r4_fait and ev["close"] < seuil
                    r6 = (not r6_fait and decision_achat is not None
                          and rang[veille] == rang[decision_achat] + 1
                          and ev["ecart"] < -K and ev["taux20"] >= 0)
                    compte["r4_possible"] += r4
                    compte["r6_possible"] += r6
                    compte["meme_semaine"] += r4 and r6
                    if r4 and avec_r4:
                        a_passer.append(("REGLE-4", PART_ACHAT * total))
                    if r6 and avec_r6:
                        a_passer.append(("RENFORT", PART_RENFORT * total))
            for genre, montant in a_passer:
                seance = serie["par_jour"].get(jour)
                if seance is None:
                    erreur(f"{VALEUR} : pas de seance au {jour}, ordre impossible")
                prix = reel(serie, jour, "Open")
                if genre == "VENTE":
                    brut = titres * prix
                    frais = brut * taux_vente()
                    especes += brut - frais
                    ordres.append(ordre_ecrit(jour, veille, genre, titres, prix, brut, frais,
                                              ev, -frais))
                    if positions:
                        positions[-1].update({"sortie": jour, "prix_sortie": prix,
                                              "motif": "VENTE", "frais": positions[-1]["frais"]
                                              + frais, "recu": brut - frais})
                    titres, seuil, decision_achat = 0, None, None
                    r4_fait = r6_fait = False
                    continue
                quantite = int(montant // (prix * (1 + taux_achat())))
                if quantite < 1:
                    compte["non_executes"] += 1
                    signaux.append({"decision": veille, "genre": genre, "motif": "QUANTITE NULLE"})
                    continue
                brut = quantite * prix
                frais = brut * taux_achat()
                especes -= brut + frais
                titres += quantite
                ordres.append(ordre_ecrit(jour, veille, genre, quantite, prix, brut, frais,
                                          ev, brut + frais))
                if genre == "ACHAT":
                    seuil = ev["close"] - ev["s120"]
                    decision_achat, r4_fait, r6_fait = veille, False, False
                    positions.append({"achat": jour, "decision": veille, "quantite": quantite,
                                      "brut": brut, "frais": frais, "investi": brut + frais,
                                      "tranches": 1, "seuil_ajuste": seuil, "sortie": None,
                                      "prix_sortie": None, "motif": None, "recu": None})
                else:
                    if genre == "REGLE-4":
                        r4_fait = True
                    else:
                        r6_fait = True
                    if positions:
                        p = positions[-1]
                        p["quantite"] += quantite
                        p["brut"] += brut
                        p["frais"] += frais
                        p["investi"] += brut + frais
                        p["tranches"] += 1
        titres_valeur = titres * reel(serie, jour, "Close") if titres else 0.0
        valeurs[jour] = (especes, titres_valeur, especes + titres_valeur, titres)
    return {"ordres": ordres, "valeurs": valeurs, "positions": positions, "seances": seances,
            "decisions": decisions, "compte": compte, "signaux": signaux}


def ordre_ecrit(jour, decision, genre, quantite, prix, brut, frais, ev, net):
    motifs = {
        "ACHAT": (f"clôture {fr(ev['close'])} sous le bord bas {fr(ev['val'] - ev['s120'])} "
                  f"({signe(ev['ecart'])} s), TAUX_20 {signe(ev['taux20'], 3)} %/séance"),
        "REGLE-4": (f"clôture {fr(ev['close'])} sous le seuil de la règle 4 "
                    f"({signe(ev['ecart'])} s dans la bande)"),
        "RENFORT": (f"renforcement, clôture {fr(ev['close'])} encore sous le bord bas "
                    f"({signe(ev['ecart'])} s), TAUX_20 {signe(ev['taux20'], 3)} %/séance"),
        "VENTE": (f"clôture {fr(ev['close'])} au-dessus du bord haut "
                  f"{fr(ev['val'] + ev['s120'])} ({signe(ev['ecart'])} s)"),
    }
    return {"DATE": jour, "DATE_DECISION": decision, "SENS": genre, "QUANTITE": quantite,
            "PRIX_REEL": prix, "BRUT": brut, "FRAIS": frais, "NET": net,
            "ECART_S": ev["ecart"], "TAUX_20": ev["taux20"], "MOTIF": motifs[genre]}


# --------------------------------------------------------------------------
# Les deux references


def detention(serie, debut, fin):
    """Tout investi a l'ouverture de la deuxieme seance, garde jusqu'au bout."""
    seances = [j for j in serie["jours"] if debut <= j <= fin]
    prix = reel(serie, seances[1], "Open")
    quantite = int(DOTATION // (prix * (1 + taux_achat())))
    especes = DOTATION - quantite * prix * (1 + taux_achat())
    valeurs = {}
    for i, jour in enumerate(seances):
        if i:
            for date, ratio in serie["splits"]:
                if date == jour:
                    quantite = int(quantite * ratio)
        titres = quantite * reel(serie, jour, "Close")
        valeurs[jour] = (especes, titres, especes + titres, quantite)
    return valeurs


def appariee(valeurs, reference, seances):
    """La detention, detenue dans la proportion ou le portefeuille l'etait la veille."""
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
        sortie = p["sortie"] or fin
        prix_sortie = p["prix_sortie"] or reel(serie, fin, "Close")
        jours = [j for j in serie["jours"] if p["achat"] <= j <= sortie]
        moyen = p["brut"] / p["quantite"]
        recu = p["recu"] if p["recu"] is not None else p["quantite"] * prix_sortie
        lignes.append({
            **p, "sortie_effective": sortie, "prix_sortie_effectif": prix_sortie,
            "ouverte": p["sortie"] is None, "prix_moyen": moyen, "seances": len(jours),
            "plus_value": 100 * (prix_sortie / moyen - 1),
            "repli_close": 100 * (min(reel(serie, j, "Close") for j in jours) / moyen - 1),
            "repli_low": 100 * (min(reel(serie, j, "Low") for j in jours) / moyen - 1),
            "contribution": recu - p["investi"],
        })
    return lignes


# --------------------------------------------------------------------------
# Les issues declarees

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
    """Une ligne par decision : etats, et le rendement des HORIZON seances suivantes."""
    lignes = []
    for indice, jour in enumerate(decisions):
        ev = evaluer(serie, jour)
        if ev is None:
            continue
        i = serie["rang"][jour]
        arrivee = (serie["jours"][i + HORIZON]
                   if i + HORIZON < len(serie["jours"])
                   and serie["jours"][i + HORIZON] <= borne else None)
        rendement = None
        if arrivee:
            rendement = 100 * (serie["par_jour"][arrivee]["Close"] / ev["close"] - 1)
        lignes.append({"DATE": jour, "SOUS_BAS": ev["ecart"] < -K,
                       "TAUX_20_POSITIF": ev["taux20"] >= 0,
                       "AU_DESSUS_HAUT": ev["ecart"] > K,
                       "SOUS_ECHANTILLON": indice % PAS_ECHANTILLON == 0,
                       "RENDEMENT_20": rendement})
    return lignes


def comparer(lignes, population, groupe):
    """Difference des rendements a 20 seances, sur le sous-echantillon sans chevauchement."""
    retenues = [li for li in lignes if li["SOUS_ECHANTILLON"] and population(li)]
    a = [li["RENDEMENT_20"] for li in retenues if groupe(li) and li["RENDEMENT_20"] is not None]
    b = [li["RENDEMENT_20"] for li in retenues
         if not groupe(li) and li["RENDEMENT_20"] is not None]
    resultat = {"na": len(a), "nb": len(b), "moy_a": statistics.fmean(a) if a else None,
                "moy_b": statistics.fmean(b) if b else None, "difference": None, "ic": None,
                "p": None,
                "non_tranchees": sum(1 for li in retenues if li["RENDEMENT_20"] is None)}
    if len(a) < 2 or len(b) < 2:
        return resultat
    resultat["difference"] = resultat["moy_a"] - resultat["moy_b"]
    se = math.sqrt(statistics.variance(a) / len(a) + statistics.variance(b) / len(b))
    ddl = len(a) + len(b) - 2
    if se > 0:
        resultat["ic"] = quantile_student(ddl) * se
        resultat["p"] = p_bilaterale(resultat["difference"] / se, ddl)
    return resultat


# --------------------------------------------------------------------------
# La confrontation de l'etalonnage


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
        "decisions": len(declaree["decisions"]), "sous_bas": compte["sous_bas"],
        "sous_bas_pente": compte["sous_bas_pente"], "au_dessus": compte["au_dessus"],
        "r4_possible": compte["r4_possible"], "r6_possible": compte["r6_possible"],
        "meme_semaine": compte["meme_semaine"], "positions": len(declaree["positions"]),
        "closes": sum(1 for p in declaree["positions"] if p["sortie"]),
        "te_app": declaree["te_app"], "te_det": declaree["te_det"],
    }
    return resultats


def ecarts_publies(resultats):
    ecarts = []
    for nom, publies in ETALONNAGE_PUBLIE.items():
        obtenu = resultats[nom]
        for cle, publie in publies.items():
            calcule = obtenu["n_ordres"] if cle == "ordres" else obtenu.get(cle)
            if cle == "appariee" and nom != "taux":
                calcule = obtenu["appariee"][-1]
            if cle == "base" and nom != "taux":
                calcule = obtenu["base"][-1]
            if not egal(publie, calcule):
                ecarts.append((nom, cle, publie, calcule))
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


def figure_canal(chemin, serie, jour, seuil=None):
    """La figure de canal a une decision : bande 120, enveloppe 20, seuil de la regle 4."""
    ev = evaluer(serie, jour)
    env = enveloppe(serie, jour)
    if ev is None or env is None:
        return False
    i = serie["rang"][jour]
    jours = serie["jours"][max(0, i - LONGUE + 1):i + 1]
    closes = [serie["par_jour"][j]["Close"] for j in jours]
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
    if seuil is not None:
        points.append(seuil)
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

    verdict = verdict_du_jour(ev, seuil)
    couleur = {"candidate à l'achat": "#2e7d32", "au-dessus du bord haut": "#c62828",
               "sous le seuil de la règle 4": "#2e7d32"}.get(verdict, "#1a1a1a")
    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" '
         f'font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{marge_g}" y="26" font-size="15" font-weight="600" fill="#1a1a1a">'
         f'Air Liquide ({VALEUR}) &#8212; canal au {jour}</text>'),
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
                   f'fill="#666666" text-anchor="end">{fr(niveau, 0)}</text>')
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
    if seuil is not None:
        out.append(f'<line x1="{marge_g}" y1="{y(seuil):.1f}" x2="{largeur - marge_d}" '
                   f'y2="{y(seuil):.1f}" stroke="#7b1fa2" stroke-width="1.4" '
                   f'stroke-dasharray="8 4"/>')
        out.append(f'<text x="{largeur - marge_d}" y="{y(seuil) - 5:.1f}" font-size="10.5" '
                   f'fill="#7b1fa2" text-anchor="end">seuil r&#232;gle 4 '
                   f'{fr(seuil)}</text>')
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


def verdict_du_jour(ev, seuil=None):
    if ev["ecart"] > K:
        return "au-dessus du bord haut"
    if seuil is not None and ev["close"] < seuil:
        return "sous le seuil de la règle 4"
    if ev["ecart"] < -K:
        return ("candidate à l'achat" if ev["taux20"] >= 0
                else "sous le bord bas, pente courte négative")
    return "dans la bande"


def svg_portefeuille(chemin, dates, courbes, executions, debut):
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
         f'viewBox="0 0 {largeur} {hauteur}" '
         f'font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{marge_g}" y="24" font-size="15" font-weight="600" fill="#1a1a1a">'
         f'Experience 8 &#8212; portefeuille sur {VALEUR}, base 100 au {debut}</text>'),
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
    for rang, (libelle, serie, couleur, pointilles) in enumerate(reversed(courbes)):
        trace = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(serie))
        tirets = ' stroke-dasharray="5 4"' if pointilles else ""
        out.append(f'<polyline points="{trace}" fill="none" stroke="{couleur}" '
                   f'stroke-width="1.8"{tirets}/>')
        gauche = marge_g + rang * 240
        out.append(f'<line x1="{gauche}" y1="{hauteur - 18}" x2="{gauche + 24}" '
                   f'y2="{hauteur - 18}" stroke="{couleur}" stroke-width="1.8"{tirets}/>'
                   f'<text x="{gauche + 30}" y="{hauteur - 14}" font-size="10.5" '
                   f'fill="#444444">{echapper(libelle)} {fr(serie[-1], 1)}</text>')
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")


def chemin_figure(repertoire, jour):
    return repertoire / GRAPHIQUES / f"canal-{VALEUR}-{jour}.svg"


def ecrire_figures(repertoire, serie, b):
    """Une figure a chaque decision qui produit un ordre, et a chaque fin d'annee."""
    seuils = {}
    for p in b["positions"]:
        seuils[p["decision"]] = None
        for o in b["ordres"]:
            if o["DATE_DECISION"] >= p["decision"] and o["SENS"] in ("REGLE-4", "RENFORT"):
                seuils[o["DATE_DECISION"]] = p["seuil_ajuste"]
    dates = {o["DATE_DECISION"] for o in b["ordres"]}
    for annee in b["annees"]:
        derniere = [j for j in b["seances"] if j[:4] == annee][-1]
        dates.add(derniere)
    ecrites = 0
    for jour in sorted(dates):
        if figure_canal(chemin_figure(repertoire, jour), serie, jour, seuils.get(jour)):
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
    out = [("| Premier achat | Sortie | Tranches | Titres | Prix moyen | Prix de sortie "
            "| +/− value | Repli max. | Contribution | Séances |"),
           "|---|---|---|---|---|---|---|---|---|---|"]
    for p in lignes:
        sortie = f"{p['sortie_effective']} *(ouverte)*" if p["ouverte"] else p["sortie_effective"]
        out.append(f"| {p['achat']} | {sortie} | {p['tranches']} | {p['quantite']} "
                   f"| {fr(p['prix_moyen'])} {EURO} | {fr(p['prix_sortie_effectif'])} {EURO} "
                   f"| **{signe(p['plus_value'])} %** | {signe(p['repli_close'])} % "
                   f"| {signe(p['contribution'])} {EURO} | {p['seances']} |")
    return out


def journal_annuel(repertoire, serie, b, annee, precedente, suivante):
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
         ("détention continue", [b["detention"][b["index"][j]] for j in jusqua],
          "#9aa5b1", True)],
        [o["DATE"] for o in b["ordres"]], b["debut"])
    total = b["valeurs"][fin][2]
    especes_fin, titres_fin = b["valeurs"][fin][0], b["valeurs"][fin][1]
    part_annee = statistics.fmean(100 * b["valeurs"][j][1] / b["valeurs"][j][2] for j in seances)
    app = b["appariee"][b["index"][fin]]
    det = b["detention"][b["index"][fin]]
    positions = [p for p in b["mesurees"] if p["achat"][:4] == annee
                 or (p["sortie_effective"][:4] == annee)]
    bloc = [
        f"# {annee}", "",
        (f"> Journal de l'[expérience 8](../README.md) · {len(seances)} séances · "
         f"**{len(ordres)} ordre{'s' if len(ordres) > 1 else ''}**"),
        (f"> Portefeuille au {fin} : **{fr(total)} {EURO}** (base "
         f"{fr(100 * total / DOTATION)}) · appariée {fr(app)} · détention continue {fr(det)}"),
        "", "---", "",
        f"## Le portefeuille depuis le {b['debut']}", "",
        f"![Portefeuille au {fin}](../{GRAPHIQUES}/portefeuille-{annee}.svg)", "",
        "| | |", "|---|---|",
        f"| Valeur au 1er jour de l'année | {fr(depart)} {EURO} |",
        f"| Valeur au {fin} | **{fr(total)} {EURO}** |",
        f"| Variation de l'année | **{signe(100 * (total / depart - 1))} %** |",
        f"| Espèces · titres | {fr(especes_fin)} {EURO} · {fr(titres_fin)} {EURO} |",
        f"| Part investie moyenne de l'année | {fr(part_annee, 2)} % |",
        "", "## Les ordres", "",
    ]
    if ordres:
        bloc += [("| Exécution | Décision | Sens | Quantité | Prix réel | Frais | Motif |"),
                 "|---|---|---|---|---|---|---|"]
        for o in ordres:
            bloc.append(f"| {o['DATE']} | {o['DATE_DECISION']} | **{o['SENS']}** "
                        f"| {o['QUANTITE']} | {fr(o['PRIX_REEL'])} {EURO} "
                        f"| {fr(o['FRAIS'])} {EURO} | {o['MOTIF']} |")
    else:
        bloc.append("*Aucun ordre : aucune clôture hebdomadaire n'a franchi une borne.*")
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
             f"| Sous le bord bas | {sous} |",
             f"| … dont `TAUX_20 ≥ 0`, donc achetables | **{pente}** |",
             f"| Au-dessus du bord haut | {dessus} |", "",
             "## La lecture de l'année", "",
             lecture_annuelle(b, annee, ordres, positions, total, depart, app), ""]
    navigation = []
    if precedente:
        navigation.append(f"[← {precedente}]({precedente}.md)")
    navigation.append("[Protocole](../README.md)")
    if suivante:
        navigation.append(f"[{suivante} →]({suivante}.md)")
    bloc += ["---", "", " · ".join(navigation)]
    ecrire_texte(repertoire / RAPPORTS / f"{annee}.md", NL_.join(bloc) + NL_)


def lecture_annuelle(b, annee, ordres, positions, total, depart, app):
    phrases = []
    variation = 100 * (total / depart - 1)
    phrases.append(f"Le portefeuille termine l'année à {fr(total)} {EURO}, "
                   f"soit {signe(variation)} % sur l'année.")
    if ordres:
        frais = sum(o["FRAIS"] for o in ordres)
        genres = {g: sum(1 for o in ordres if o["SENS"] == g)
                  for g in ("ACHAT", "REGLE-4", "RENFORT", "VENTE")}
        detail = ", ".join(f"{n} {g.lower()}" for g, n in genres.items() if n)
        phrases.append(f"Les {len(ordres)} ordres de l'année — {detail} — ont coûté "
                       f"{fr(frais)} {EURO} de frais.")
    else:
        phrases.append("Aucun ordre, donc aucun frais.")
    ouvertes = [p for p in positions if p["ouverte"]]
    if ouvertes:
        p = ouvertes[0]
        phrases.append(f"Une position reste ouverte au terme de l'année, "
                       f"{p['tranches']} tranche{'s' if p['tranches'] > 1 else ''} à "
                       f"{fr(p['prix_moyen'])} {EURO} de moyenne, "
                       f"{signe(p['plus_value'])} % au dernier cours.")
    ecart = 100 * total / DOTATION - app
    sens = "devant" if ecart >= 0 else "derrière"
    phrases.append(f"Depuis le début, le portefeuille est {sens} sa référence à exposition "
                   f"appariée de {fr(abs(ecart))} point.")
    return " ".join(phrases)


def bilan(serie, b):
    d = b["variantes"]["declaree"]
    sans_r4 = b["variantes"]["sans regle 4"]
    sans_r6 = b["variantes"]["sans regle 6"]
    ni = b["variantes"]["ni l'une ni l'autre"]
    mde_app = Z95 * d["te_app"]
    ouvertes = [p for p in b["mesurees"] if p["ouverte"]]
    closes = [p for p in b["mesurees"] if not p["ouverte"]]
    ecarts = ecarts_publies(b["etalonnage"])
    compte = d["compte"]
    qualite = ("*indiscernable de zéro*" if abs(d["alpha"]) <= mde_app
               else "*au-delà de son effet minimal détectable*")
    out = [
        "# Bilan de l'expérience 8", "",
        (f"> [Expérience 8](README.md) · Air Liquide seule, une décision par semaine · "
         f"**{signe(d['base'][-1] - 100)} %** · alpha officiel "
         f"**{signe(d['alpha'])} pt**"), "",
        ("> ⚠️ **La règle est de catégorie B**, et sa fenêtre contient des années déjà jouées : "
         "le [protocole](README.md#-ce-que-cette-expérience-ne-pourra-pas-établir) le "
         "déclarait avant la fenêtre jouée. Ce que ce bilan établit est aux sections 3 à 6."),
        "", "---", "", "## 1. Le compte", "", "| | |", "|---|---|",
        f"| Dotation | {fr(DOTATION)} {EURO} au {b['debut']} |",
        f"| Valeur finale au {b['fin']} | **{fr(d['valeurs'][b['fin']][2])} {EURO}** |",
        f"| Performance | **{signe(d['base'][-1] - 100)} %** |",
        f"| Référence à exposition appariée | {signe(d['appariee'][-1] - 100)} % |",
        f"| Détention continue d'Air Liquide | {signe(d['detention'][-1] - 100)} % |",
        (f"| **Alpha officiel** | **{signe(d['alpha'])} pt** — {qualite}, effet minimal "
         f"détectable ± {fr(mde_app, 1)} pt |"),
        f"| Écart brut à la détention | {signe(d['brut'])} pt |",
        (f"| Ordres | {d['n_ordres']} — "
         + ", ".join(f"{n} {g.lower()}" for g, n in d["genres"].items() if n) + " |"),
        (f"| Frais cumulés | {fr(d['frais'])} {EURO}, soit "
         f"{fr(100 * d['frais'] / DOTATION, 2)} pt de dotation |"),
        f"| Part investie moyenne · maximum | {fr(d['part'], 2)} % · {fr(d['maximum'], 1)} % |",
        f"| Décisions hebdomadaires | {len(d['decisions'])} |",
        "", "## 2. Les positions", "",
        *tableau_positions(b["mesurees"]),
        "", "## 3. Ce que coûte l'absence de sortie en perte", "",
        ("> La règle 5 est la seule sortie : une position qui ne revient pas dans sa bande "
         "reste ouverte."), "",
        "| Mesure | Valeur |", "|---|---|",
        f"| Positions · dont closes | {len(b['mesurees'])} · {len(closes)} |",
        f"| **Lignes jamais revendues** au {b['fin']} | **{len(ouvertes)}** |",
        (f"| Repli maximal le plus profond, en clôture · sur `Low` | "
         f"{signe(min((p['repli_close'] for p in b['mesurees']), default=None))} % · "
         f"{signe(min((p['repli_low'] for p in b['mesurees']), default=None))} % |"),
        (f"| Durée médiane d'une position close | "
         f"{fr(statistics.median([p['seances'] for p in closes]), 0) if closes else '—'} "
         "séances |"),
        ("| Durée d'une position encore ouverte | "
         + (" · ".join(f"{p['seances']} séances" for p in ouvertes) if ouvertes else "—")
         + " |"),
        "", "## 4. Ce qu'ajoutent les règles 4 et 6", "",
        *tableau_variantes(b),
        "",
        (f"La règle 4 ajoute {d['n_ordres'] - sans_r4['n_ordres']} ordres et "
         f"{signe(d['frais'] - sans_r4['frais'])} {EURO} de frais ; la règle 6, "
         f"{d['n_ordres'] - sans_r6['n_ordres']} ordres et "
         f"{signe(d['frais'] - sans_r6['frais'])} {EURO}. Ensemble, elles portent la part "
         f"investie de {fr(ni['part'], 2)} % à {fr(d['part'], 2)} %, et son maximum de "
         f"{fr(ni['maximum'], 1)} % à {fr(d['maximum'], 1)} %."),
        "", "| Écart apparié | Base 100 | Écart-type de la différence | EMD |",
        "|---|---|---|---|",
    ]
    for nom in ("sans regle 4", "sans regle 6", "ni l'une ni l'autre"):
        v = b["variantes"][nom]
        te = ecart_type(d["base"], v["base"])
        out.append(f"| déclarée − {LIBELLE_VARIANTE[nom].replace('**', '')} "
                   f"| **{signe(d['base'][-1] - v['base'][-1])} pt** | {fr(te)} %/an "
                   f"| ± {fr(Z95 * te, 1)} pt |")
    out += [
        "", "## 5. Les taux de déclenchement", "", "| Règle | Déclenchée | Exécutée |",
        "|---|---|---|",
        (f"| **3** — sous le bord bas et `TAUX_20 ≥ 0` | {compte['sous_bas_pente']} "
         f"| {d['genres']['ACHAT']} |"),
        f"| **4** — sous le seuil figé | {compte['r4_possible']} | {d['genres']['REGLE-4']} |",
        f"| **6** — renforcement | {compte['r6_possible']} | {d['genres']['RENFORT']} |",
        f"| **5** — au-dessus du bord haut | {compte['au_dessus']} | {d['genres']['VENTE']} |",
        "",
        (f"Les règles 4 et 6 ont été remplies la même semaine **{compte['meme_semaine']} "
         f"fois**. {compte['sous_bas']} décisions sont passées sous le bord bas, dont "
         f"{compte['sous_bas_pente']} avec une pente courte positive : c'est la pente qui "
         "filtre, pas la bande."),
        "", "## 6. Les issues déclarées", "",
        ("> Rendement du cours sur les 20 séances suivant la décision, sur une décision "
         f"hebdomadaire sur {PAS_ECHANTILLON} pour que deux observations ne partagent aucune "
         "séance."), "",
        ("| Élément | Groupe testé | Témoin | Effectifs | Moyennes | Différence | IC95 "
         "| Verdict |"),
        "|---|---|---|---|---|---|---|---|",
    ]
    for cle, libelle, groupe_a, groupe_b, _pop, _grp in COMPARAISONS:
        c = b["comparaisons"][cle]
        verdict = ("*non mesurable*" if c["ic"] is None else
                   ("**exclut zéro**" if abs(c["difference"]) > c["ic"] else "contient zéro"))
        out.append(f"| {libelle} | {groupe_a} | {groupe_b} | {c['na']} contre {c['nb']} "
                   f"| {signe(c['moy_a'])} % contre {signe(c['moy_b'])} % "
                   f"| **{signe(c['difference'])} pt** | ± {fr(c['ic'])} pt | {verdict} |")
    out += [
        "", "## 7. L'étalonnage, publié avant, recalculé après", "",
        "| Variante | Base publiée | Base recalculée | Alpha publié | Alpha recalculé | Concorde |",
        "|---|---|---|---|---|---|",
    ]
    for nom, _r4, _r6 in VARIANTES:
        publie = ETALONNAGE_PUBLIE[nom]
        obtenu = b["etalonnage"][nom]
        manque = any(e[0] == nom for e in ecarts)
        out.append(f"| {LIBELLE_VARIANTE[nom]} | {fr(publie['base'])} "
                   f"| {fr(obtenu['base'][-1])} | {signe(publie['alpha'])} pt "
                   f"| {signe(obtenu['alpha'])} pt | {'✗' if manque else '✓'} |")
    total_publies = sum(len(v) for v in ETALONNAGE_PUBLIE.values())
    out += [
        "",
        (f"**{total_publies - len(ecarts)} nombres publiés sur {total_publies}** sont retrouvés "
         "à l'identique par le moteur."
         if not ecarts else
         f"**{len(ecarts)} nombres publiés sur {total_publies} ne sont pas retrouvés.** Le "
         "README n'est pas corrigé après coup ; les écarts sont listés en console."),
        "", "## 8. Ce que l'expérience établit, et ce qu'elle n'établit pas", "",
        "**Elle établit** :", "",
        (f"- ce que les règles 4 et 6 coûtent en frais — {fr(d['frais'])} {EURO} contre "
         f"{fr(ni['frais'])} {EURO} sans elles, sans aucune incertitude — § 4 ;"),
        (f"- ce qu'elles font à l'exposition : part investie {fr(d['part'], 2)} % contre "
         f"{fr(ni['part'], 2)} %, maximum {fr(d['maximum'], 1)} % contre "
         f"{fr(ni['maximum'], 1)} % — § 4 ;"),
        (f"- les taux de déclenchement des six règles sur {len(d['decisions'])} décisions "
         "— § 5 ;"),
        (f"- ce que l'absence de sortie en perte laisse ouvert : {len(ouvertes)} ligne"
         f"{'s' if len(ouvertes) > 1 else ''} jamais revendue"
         f"{'s' if len(ouvertes) > 1 else ''} — § 3."),
        "", "**Elle n'établit pas** :", "",
        (f"- que la règle bat la détention : l'alpha officiel vaut {signe(d['alpha'])} point "
         f"pour un effet minimal détectable de ± {fr(mde_app, 1)} ;"),
        ("- que l'inversion du stop est une amélioration : la comparaison est faite sur une "
         "seule valeur, sur une fenêtre qui contient des années déjà jouées, et la règle est "
         "de catégorie B ;"),
        ("- quoi que ce soit de généralisable : une valeur, un régime, et une part investie "
         f"moyenne de {fr(d['part'], 2)} %."),
        "", "---", "",
        (f"[← Protocole](README.md) · [{b['annees'][0]}]({RAPPORTS}/{b['annees'][0]}.md) · "
         f"[{b['annees'][-1]}]({RAPPORTS}/{b['annees'][-1]}.md)"),
    ]
    return NL_.join(out) + NL_


# --------------------------------------------------------------------------
# Assemblage


def construire(serie):
    debut_evaluable = next(j for j in serie["jours"] if evaluer(serie, j))
    fin = serie["jours"][-1]
    variantes = {}
    for nom, avec_r4, avec_r6 in VARIANTES:
        simulation = simuler(serie, DEBUT_NARREE, fin, avec_r4, avec_r6)
        variantes[nom] = resumer(serie, simulation, DEBUT_NARREE, fin)
    declaree = variantes["declaree"]
    lignes_issues = issues(serie, declaree["decisions"], fin)
    b = {
        **declaree, "variantes": variantes, "debut": declaree["seances"][0], "fin": fin,
        "index": {j: i for i, j in enumerate(declaree["seances"])},
        "mesurees": mesurer_positions(serie, declaree, fin),
        "issues": lignes_issues,
        "comparaisons": {cle: comparer(lignes_issues, pop, grp)
                         for cle, _l, _a, _b, pop, grp in COMPARAISONS},
        "etalonnage": etalonnage(serie, debut_evaluable),
        "annees": sorted({j[:4] for j in declaree["seances"]}),
    }
    return b


def ecrire_csvs(repertoire, serie, b):
    seuils = {p["decision"]: p["seuil_ajuste"] for p in b["positions"]}
    lignes = []
    for jour in b["decisions"]:
        ev = evaluer(serie, jour)
        i = serie["rang"][jour]
        execution = serie["jours"][i + 1] if i + 1 < len(serie["jours"]) else None
        signal = verdict_du_jour(ev)
        lignes.append({
            "DATE": jour, "EXECUTION": execution, "CLOSE_AJUSTE": arrondi(ev["close"]),
            "CLOSE_REEL": arrondi(reel(serie, jour, "Close")),
            "VAL_120": arrondi(ev["val"]), "S_120": arrondi(ev["s120"]),
            "ECART_S": arrondi(ev["ecart"]), "TAUX_120": arrondi(ev["taux120"]),
            "TAUX_20": arrondi(ev["taux20"]), "SOUS_BAS": oui(ev["ecart"] < -K),
            "AU_DESSUS": oui(ev["ecart"] > K),
            "SEUIL_FRANCHI": oui(any(ev["close"] < s for s in seuils.values() if s)),
            "SIGNAL": signal})
    ecrire_csv(repertoire / "decisions.csv", ENTETE_DECISIONS, lignes)
    ecrire_csv(repertoire / "ordres.csv", ENTETE_ORDRES, [
        {**o, "PRIX_REEL": arrondi(o["PRIX_REEL"]), "BRUT": arrondi(o["BRUT"]),
         "FRAIS": arrondi(o["FRAIS"]), "NET": arrondi(o["NET"]),
         "ECART_S": arrondi(o["ECART_S"]), "TAUX_20": arrondi(o["TAUX_20"])}
        for o in b["ordres"]])
    ecrire_csv(repertoire / "positions.csv", ENTETE_POSITIONS, [
        {"ACHAT": p["achat"], "SORTIE": p["sortie"], "MOTIF": p["motif"] or "ouverte",
         "TRANCHES": p["tranches"], "QUANTITE": p["quantite"],
         "PRIX_ACHAT": arrondi(p["prix_moyen"]),
         "PRIX_SORTIE": arrondi(p["prix_sortie_effectif"]),
         "SEUIL_REGLE_4": arrondi(p["seuil_ajuste"] * facteur(serie, p["decision"])),
         "SEANCES": p["seances"], "PLUS_VALUE": arrondi(p["plus_value"]),
         "REPLI_CLOTURE": arrondi(p["repli_close"]), "REPLI_LOW": arrondi(p["repli_low"]),
         "CONTRIBUTION": arrondi(p["contribution"])}
        for p in b["mesurees"]])
    ecrire_csv(repertoire / "portefeuille.csv", ENTETE_PORTEFEUILLE, [
        {"DATE": j, "ESPECES": round(b["valeurs"][j][0], 2),
         "TITRES": round(b["valeurs"][j][1], 2), "TOTAL": round(b["valeurs"][j][2], 2),
         "BASE100": round(100 * b["valeurs"][j][2] / DOTATION, 4),
         "APPARIEE100": round(b["appariee"][i], 4),
         "DETENTION100": round(b["detention"][i], 4)}
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
        lignes.append(f"  {o['DATE']} {o['SENS']:<8s} {o['QUANTITE']:4d} titres a "
                      f"{fr(o['PRIX_REEL']):>9s} EUR {MEDIAN} frais {fr(o['FRAIS']):>6s}")
    total = b["valeurs"][fin][2]
    lignes += ["", (f"Portefeuille au {fin} : {fr(total)} EUR {MEDIAN} base "
                    f"{fr(100 * total / DOTATION)} {MEDIAN} appariee "
                    f"{fr(b['appariee'][b['index'][fin]])} {MEDIAN} detention "
                    f"{fr(b['detention'][b['index'][fin]])}")]
    return NL_.join(lignes)


def imprimer_bilan(b):
    d = b["variantes"]["declaree"]
    ni = b["variantes"]["ni l'une ni l'autre"]
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
  Part investie           {fr(d['part'], 2)} % {MEDIAN} maximum {fr(d['maximum'], 1)} %
  Positions               {len(b['mesurees'])} dont {ouvertes} jamais revendue(s)
  Declenchements          sous le bord bas {compte['sous_bas']}, dont pente >= 0 \
{compte['sous_bas_pente']} {MEDIAN} au-dessus {compte['au_dessus']}
                          regle 4 {compte['r4_possible']} {MEDIAN} regle 6 \
{compte['r6_possible']} {MEDIAN} meme semaine {compte['meme_semaine']}
  Sans les regles 4 et 6  base {fr(ni['base'][-1])} {MEDIAN} frais {fr(ni['frais'])} EUR \
{MEDIAN} part investie {fr(ni['part'], 2)} %""")
    print("  Issues :")
    for cle, libelle, *_r in COMPARAISONS:
        c = b["comparaisons"][cle]
        print(f"    {libelle:<22s} {c['na']:3d} contre {c['nb']:3d} {MEDIAN} "
              f"{signe(c['difference'])} +/- {fr(c['ic'])} pt")
    for nom, cle, publie, calcule in ecarts_publies(b["etalonnage"]):
        print(f"  ECART ETALONNAGE {nom} {cle} : publie {publie}, moteur {calcule}")
    print()


def analyser_arguments():
    ici = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Journal de l'experience 8 : Air Liquide seule, une decision par semaine.")
    parser.add_argument("--figures", action="store_true", help="Ecrire les figures de canal")
    parser.add_argument("--markdown", action="store_true",
                        help="Ecrire les figures, les journaux annuels et le bilan")
    parser.add_argument("--annee", help="N'afficher que cette annee (AAAA)")
    parser.add_argument("--repertoire", type=Path, default=ici, help="Ou lire et ecrire")
    parser.add_argument("--quotes", type=Path, default=QUOTES_DEFAUT, help="Ou est la serie")
    args = parser.parse_args()
    if not args.quotes.is_dir():
        erreur(f"Repertoire introuvable : {args.quotes}")
    return args


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    args = analyser_arguments()
    serie = charger(args.quotes)
    b = construire(serie)
    if args.annee and args.annee not in b["annees"]:
        erreur(f"--annee doit etre l'une de : {', '.join(b['annees'])}")
    ecrire_csvs(args.repertoire, serie, b)
    ecrits = ["decisions.csv", "ordres.csv", "positions.csv", "portefeuille.csv", "issues.csv"]
    if args.figures or args.markdown:
        ecrits.append(f"{ecrire_figures(args.repertoire, serie, b)} figures de canal")
    if args.markdown:
        for i, annee in enumerate(b["annees"]):
            journal_annuel(args.repertoire, serie, b, annee,
                           b["annees"][i - 1] if i else None,
                           b["annees"][i + 1] if i + 1 < len(b["annees"]) else None)
        ecrire_texte(args.repertoire / BILAN, bilan(serie, b))
        ecrits += [f"{RAPPORTS}/AAAA.md ({len(b['annees'])} journaux)",
                   f"{GRAPHIQUES}/portefeuille-AAAA.svg", BILAN]
    for annee in b["annees"]:
        if not args.annee or args.annee == annee:
            print(bloc_annuel(b, annee))
    imprimer_bilan(b)
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
