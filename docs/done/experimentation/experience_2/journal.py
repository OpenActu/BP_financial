"""Moteur de l'experience 2 : la meme regle qu'en 2022, mais auditee.

Classe l'univers declare a chaque fin de mois a partir des cinq criteres de la
regle du module 3, APPLIQUE ses quatre vetos, en deduit les ordres, execute a
l'ouverture suivante, comptabilise, engendre et depouille des theses refutables,
et ecrit les graphiques.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_2/journal.py --collecter
    python docs/done/experimentation/experience_2/journal.py --markdown
    python docs/done/experimentation/experience_2/journal.py --mois 2025-03
"""

import argparse
import csv
import math
import re
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

UNIVERS = (
    "AIR.PA", "MC.PA", "OR.PA", "SAN.PA", "BNP.PA", "TTE.PA",
    "SU.PA", "AI.PA", "DG.PA", "CAP.PA", "RI.PA", "ORA.PA",
)
REFERENCE = "TR12"
REFERENCE_NUE = "^FCHI"
RAPPORTS = "rapports"
ANNEE = "2025"
BILAN = f"bilan-{ANNEE}.md"
DEBUT_SERIE = "2021-01-04"   # premiere seance des CSV, deux ans d'amorce
FIN_SERIE = "2025-12-31"     # derniere seance des CSV
MOIS_AUDIT_DEBUT = "2022-12"     # premiere date de decision de la fenetre d'audit
MOIS_INVESTI_DEBUT = "2024-12"   # premiere date de decision investie
MOIS_ETALONNAGE_FIN = "2024-11"  # derniere date de decision de l'etalonnage
COUPLES_AUDIT = 36
COUPLES_INVESTIS = 12

SEUIL_BAS = 35.0             # s3 aligne sur la regle du module 3
SEUIL_HAUT = 65.0
SEUIL_BAS_FANTOME = 20.0     # s3 au sens de l'experience 1
SEUIL_HAUT_FANTOME = 50.0
TOLERANCE_REFLEXIVE = 5.0    # demi-largeur, en points, de « aucune sequence »
DECALAGES = (1, 2)
CADENCE_ECRITURE = 48   # criteres.csv est depose tous les 48 resultats
TE_DECLAREE = 8.20           # tracking error de l'experience 1, publiee au README
Z95 = 1.96

COURTAGE = 0.10
SPREAD = 0.015
TTF = 0.30
EXEMPTES_TTF = ("AIR.PA",)

QUOTES_DEFAUT = Path("docs/raw/data/quotes")
REGLE = Path("python/generer_graph_decision.py")

ENTETE_CRITERES = [
    "DATE", "ROLE", "DATE_EVALUEE", "TICKER", "CLOSE", "TEND_120", "TEND_20",
    "POSITION", "ALPHA", "ALPHA_BAS", "ALPHA_HAUT", "MOMENTUM", "SUPPORT",
    "RESISTANCE", "PENTE_SUP", "PENTE_RES", "PORTEE_SUP", "PORTEE_RES",
    "EPISODES_SUP", "EPISODES_RES", "LARGEUR", "TAU", "VETOS", "VERDICT",
]
MESURES = ENTETE_CRITERES[5:]
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
    "DATE_DEPOUILLEMENT", "VALEUR_CONSTATEE", "VERDICT",
]

NBSP = " "
NL_ = chr(10)
EURO = "€"
MEDIAN = "·"
ABSENTE = "*(section absente)*"

MOIS_TITRE = {
    "01": "Janvier", "02": "Février", "03": "Mars", "04": "Avril",
    "05": "Mai", "06": "Juin", "07": "Juillet", "08": "Août",
    "09": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Décembre",
}
SOCIETES = {
    "AIR.PA": "Airbus", "MC.PA": "LVMH", "OR.PA": "L'Oréal",
    "SAN.PA": "Sanofi", "BNP.PA": "BNP Paribas", "TTE.PA": "TotalEnergies",
    "SU.PA": "Schneider Electric", "AI.PA": "Air Liquide", "DG.PA": "Vinci",
    "CAP.PA": "Capgemini", "RI.PA": "Pernod Ricard", "ORA.PA": "Orange",
}
LIBELLE_VETO = {
    1: "encadrement illisible (moins de 3 épisodes de contact)",
    2: "canal se refermant en moins de 20 séances",
    3: "critères 1 et 2 de signes opposés",
    4: "historique de moins de 120 séances",
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
        return "-"
    texte = f"{x:,.{decimales}f}".replace(",", "\x00").replace(".", ",")
    return texte.replace("\x00", NBSP)


def signe(x, decimales=2):
    return "-" if x is None else ("+" if x >= 0 else "") + fr(x, decimales)


def ent(x):
    """Une composante de score sur trois colonnes ; « . » quand elle est vide."""
    return "  ." if x is None else f"{x:+3d}"


def tau_texte(tau):
    """« inf » se lit ∞ ; le reste s'affiche en seances."""
    if tau is None:
        return "-"
    return "∞" if math.isinf(tau) else fr(tau, 1)


def ic95(succes, total):
    """Demi-largeur de l'intervalle de confiance a 95 % d'une proportion, en points."""
    if total <= 0:
        return None
    p = succes / total
    return 100 * Z95 * math.sqrt(p * (1 - p) / total)


def nom_fichier(ticker, quotes):
    """Rend le CSV de la plage declaree. Un glob choisirait le mauvais fichier
    des qu'une autre plage du meme ticker traine dans le repertoire."""
    chemin = quotes / f"{ticker.replace('.', '_')}_{DEBUT_SERIE}_{FIN_SERIE}.csv"
    if not chemin.exists():
        erreur(f"Serie absente : {chemin}\n"
               f"  python python/import_societe.py {ticker} "
               f"--debut {DEBUT_SERIE} --fin 2026-01-02")
    return chemin


def charger_serie(chemin):
    """Rend {date: {'open': float, 'close': float}}, dates tronquees au jour."""
    serie = {}
    with chemin.open(encoding="utf-8") as flux:
        for ligne in csv.DictReader(flux):
            if not ligne.get("Close"):
                continue
            ouverture = ligne.get("Open") or ""
            serie[ligne["Date"][:10]] = {
                "open": float(ouverture) if ouverture else float(ligne["Close"]),
                "close": float(ligne["Close"]),
            }
    return serie


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
    r"IC95\s*\[\s*([+-]?[\d\s,  ]+?)\s*;\s*([+-]?[\d\s,  ]+?)\s*\]"
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
    """Tire (pente, portee, episodes, valeur) d'une ligne Support ou Resistance.

    La ligne a la forme « pente +0,2306 EUR/seance · portee 83 · 6 episodes ·
    93,18 EUR ». On la decoupe sur le point median plutot que d'ecrire une
    expression reguliere qui devrait connaitre chaque unite.
    """
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


def dates_a_evaluer(audit, investis, dates_ref):
    """Rend [(date de decision, role, date reellement evaluee)].

    Les decalages vont vers l'ARRIERE : reculer d'une seance n'utilise que des
    seances deja connues a la date de decision. Avancer supposerait une seance
    posterieure, ce que le depot interdit partout.
    """
    rang = {jour: i for i, jour in enumerate(dates_ref)}
    taches = [(decision, "DECISION", decision) for decision, _ in audit]
    for decision, _ in investis:
        for pas in DECALAGES:
            i = rang[decision] - pas
            if i >= 0:
                taches.append((decision, f"DECALE-{pas}", dates_ref[i]))
    return taches


def evaluer_un(travail, quotes, chemin_reference, series):
    """Lance la regle sur un couple (valeur, date) et rend sa ligne de criteres."""
    numero, (decision, role, evaluee, ticker) = travail
    jetable = quotes.parent / "graphs" / f"_jetable_{numero % 64}.svg"
    jetable.parent.mkdir(parents=True, exist_ok=True)
    issue = subprocess.run(
        [sys.executable, str(REGLE),
         "--csv", str(nom_fichier(ticker, quotes)),
         "--indice", str(chemin_reference),
         "--date", evaluee,
         "--sortie", str(jetable)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        check=False,
    )
    if issue.returncode != 0:
        champs = dict.fromkeys(MESURES)
        champs["VETOS"] = ""
        champs["VERDICT"] = "ERREUR"
    else:
        champs = extraire(issue.stdout)
    seance = series[ticker].get(evaluee)
    return {
        "DATE": decision, "ROLE": role, "DATE_EVALUEE": evaluee, "TICKER": ticker,
        "CLOSE": seance["close"] if seance else None,
        **{cle: champs.get(cle) for cle in MESURES if cle != "CLOSE"},
    }


def collecter(taches, quotes, repertoire, series, parallele, reprendre=True):
    """Lance la regle du depot sur chaque (valeur, date) et ecrit criteres.csv.

    Les sous-processus tournent en parallele — l'essentiel de leur duree est
    l'import de pandas, pas le calcul. L'ordre des lignes ecrites est celui des
    taches, jamais celui des retours : criteres.csv est identique d'une
    execution a l'autre, quel que soit --taches.

    La collecte est REPRENABLE. Les lignes deja presentes dans criteres.csv sont
    conservees et leurs evaluations ne sont pas relancees ; le fichier est
    reecrit tous les CADENCE_ECRITURE resultats. Une collecte interrompue reprend
    donc ou elle en etait, au lieu de tout perdre. `--recollecter` repart de
    zero : c'est ce qu'il faut faire des que la regle elle-meme a change.
    """
    chemin = repertoire / "criteres.csv"
    connus = {}
    if reprendre and chemin.exists():
        with chemin.open(encoding="utf-8") as flux:
            for ligne in csv.DictReader(flux):
                connus[(ligne["DATE"], ligne["ROLE"], ligne["TICKER"])] = ligne

    chemin_reference = nom_fichier(REFERENCE, quotes)
    travaux = [(decision, role, evaluee, ticker)
               for decision, role, evaluee in taches for ticker in UNIVERS]

    def cle(travail):
        return (travail[0], travail[1], travail[3])

    def deposer():
        ecrire_csv(chemin, ENTETE_CRITERES,
                   [connus[cle(t)] for t in travaux if cle(t) in connus])

    manquants = [t for t in travaux if cle(t) not in connus]
    if not manquants:
        print(f"  {len(connus)} evaluations deja presentes dans {chemin}")
        return
    print(f"  {len(connus)} deja connues, {len(manquants)} a evaluer")

    fait = 0
    with ThreadPoolExecutor(max_workers=parallele) as vivier:
        for ligne in vivier.map(
                lambda t: evaluer_un(t, quotes, chemin_reference, series),
                enumerate(manquants)):
            connus[(ligne["DATE"], ligne["ROLE"], ligne["TICKER"])] = ligne
            fait += 1
            print(f"  [{fait:3d}/{len(manquants)}] {ligne['TICKER']:8s} "
                  f"{ligne['DATE_EVALUEE']} {ligne['ROLE']:10s}", end="\r")
            if fait % CADENCE_ECRITURE == 0:
                deposer()
    print(" " * 78, end="\r")
    for jetable in (quotes.parent / "graphs").glob("_jetable_*.svg"):
        jetable.unlink()

    deposer()
    print(f"  {len(connus)} evaluations ecrites dans {chemin}")


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


def classer(criteres, date, sens):
    """Rend les douze valeurs du jour, de la plus interessante a la moins."""
    lignes = []
    for ligne in criteres:
        if ligne["DATE"] != date or ligne["ROLE"] != "DECISION":
            continue
        s1, s2, s3, s4, s5, score = composantes(ligne, sens)
        lignes.append({
            "DATE": date, "TICKER": ligne["TICKER"],
            "S1": s1, "S2": s2, "S3": s3, "S4": s4, "S5": s5, "SCORE": score,
            "POSITION": nombre(ligne["POSITION"]), "MOMENTUM": nombre(ligne["MOMENTUM"]),
            "TAU": lire_tau(ligne["TAU"]), "VETOS": ligne["VETOS"],
            "ACTIFS": vetos_actifs(ligne["VETOS"]),
            "ERREUR": ligne["VERDICT"] == "ERREUR",
            "VERDICT_REGLE": ligne["VERDICT"], "CLOSE": nombre(ligne["CLOSE"]),
        })
    lignes.sort(key=lambda x: (-x["SCORE"], -(x["MOMENTUM"] if x["MOMENTUM"] is not None
                                              else -999), x["TICKER"]))
    for rang, ligne in enumerate(lignes, start=1):
        ligne["RANG"] = rang
    return lignes


# --------------------------------------------------------------------------
# Phase 3 : les ordres


def taux_achat(ticker):
    return (COURTAGE + SPREAD + (0.0 if ticker in EXEMPTES_TTF else TTF)) / 100


def taux_vente(_ticker):
    return (COURTAGE + SPREAD) / 100


def vendre(positions, classement, date_exec, series, args):
    """Rend les ordres de vente du mois. Les vetos n'y entrent pas. Ne modifie rien."""
    rangs = {ligne["TICKER"]: ligne for ligne in classement}
    ordres = []
    for ticker in sorted(positions):
        ligne = rangs[ticker]
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
    return ordres


def acheter(positions, classement, date_exec, series, especes, args,
            vetos_appliques, repartition):
    """Rend les ordres d'achat, especes reparties a parts egales. Ne modifie rien.

    Un veto interdit l'entree ; il ne force pas la sortie. Un veto dit « la
    figure n'est pas lisible », pas « la position est mauvaise ».

    La repartition divise les especes par le nombre de CRENEAUX LIBRES, pas par
    le nombre de candidats : sans quoi un mois a candidat unique — cas frequent
    des que les vetos s'appliquent — mettrait tout le portefeuille sur une seule
    ligne, ce qui viderait de son sens le plafond de cinq lignes.
    `--repartition candidats` retablit la regle de l'experience 1.
    """
    candidats = [ligne for ligne in classement
                 if ligne["RANG"] <= args.rang_entree and ligne["SCORE"] > 0
                 and ligne["TICKER"] not in positions and not ligne["ERREUR"]
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
# Phase 4 : la simulation, deux fois


def derniere_seance(seances, mois):
    jours = [j for j in seances if j[:7] == mois]
    return jours[-1] if jours else None


def mois_precedent(mois):
    """« 2025-03 » -> « 2025-02 », « 2025-01 » -> « 2024-12 »."""
    annee, numero = int(mois[:4]), int(mois[5:7])
    return f"{annee - 1}-12" if numero == 1 else f"{annee}-{numero - 1:02d}"


def simuler(couples, criteres, series, reference, seances, args, sens,
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
        classement = classer(criteres, date_decision, sens)
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
                "pv": 100 * (cours / info["prix"] - 1),
                "alpha_mois": 100 * (cours / base_mois
                                     - reference[date_decision]["close"] / ref_mois),
                "alpha_global": 100 * (cours / info["prix"]
                                       - reference[date_decision]["close"]
                                       / reference[info["date"]]["close"]),
                "partiel": "" if plein else " (partiel)",
            }

        ordres = vendre(positions, classement, date_exec, series, args)
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
            "tenues": dict(positions),
        })
    return ordres_tous, valeurs, historique


# --------------------------------------------------------------------------
# Phase 5 : les theses, ecrites puis depouillees


def phase_reflexive(ligne):
    """Rend (phase, borne basse, borne haute) a partir de l'etat constate."""
    tend_120, tend_20 = nombre(ligne["TEND_120"]), nombre(ligne["TEND_20"])
    position = nombre(ligne["POSITION"])
    if None in (tend_120, tend_20, position):
        return "AUCUNE SEQUENCE", -TOLERANCE_REFLEXIVE, TOLERANCE_REFLEXIVE
    if tend_120 == 1 and tend_20 == 1 and position > SEUIL_HAUT:
        return "AUTO-RENFORCEMENT", 0.0, None
    if tend_120 == -1 and tend_20 == -1 and position < SEUIL_BAS:
        return "RETOURNEMENT", None, 0.0
    return "AUCUNE SEQUENCE", -TOLERANCE_REFLEXIVE, TOLERANCE_REFLEXIVE


def depouiller(basse, haute, constatee):
    """Le meme test pour les deux types de these : une borne vide vaut l'infini."""
    if constatee is None or (basse is None and haute is None):
        return "NON TRANCHEE"
    if basse is not None and constatee < basse:
        return "DEMENTIE"
    if haute is not None and constatee > haute:
        return "DEMENTIE"
    return "CONFIRMEE"


def ecrire_theses(criteres, dates_decision, dates_depouillement, series, reference,
                  dates_ref):
    """Rend les 2 x 12 theses de chaque date, deja depouillees a la date suivante."""
    rang = {jour: i for i, jour in enumerate(dates_ref)}
    index = {(ligne["DATE"], ligne["TICKER"]): ligne for ligne in criteres
             if ligne["ROLE"] == "DECISION"}
    theses = []
    for date, suivante in zip(dates_decision, dates_depouillement, strict=True):
        k = rang[suivante] - rang[date]
        for ticker in UNIVERS:
            ligne = index.get((date, ticker))
            if ligne is None:
                continue
            support, resistance = nombre(ligne["SUPPORT"]), nombre(ligne["RESISTANCE"])
            pente_sup, pente_res = nombre(ligne["PENTE_SUP"]), nombre(ligne["PENTE_RES"])
            basse = None if support is None or pente_sup is None else support + k * pente_sup
            haute = (None if resistance is None or pente_res is None
                     else resistance + k * pente_res)
            arrivee = series[ticker].get(suivante)
            constatee = arrivee["close"] if arrivee else None
            theses.append({
                "DATE": date, "TICKER": ticker, "TYPE": "CANAL", "PHASE": "",
                "ENONCE": (f"clôture entre {fr(basse)} {EURO} et {fr(haute)} {EURO} "
                           f"au {suivante}"),
                "BORNE_BASSE": basse, "BORNE_HAUTE": haute,
                "DATE_DEPOUILLEMENT": suivante, "VALEUR_CONSTATEE": constatee,
                "VERDICT": depouiller(basse, haute, constatee),
            })

            phase, b_basse, b_haute = phase_reflexive(ligne)
            depart = series[ticker].get(date)
            ecart = None
            if depart and arrivee and date in reference and suivante in reference:
                ecart = 100 * (arrivee["close"] / depart["close"]
                               - reference[suivante]["close"] / reference[date]["close"])
            clause = {
                "AUTO-RENFORCEMENT": f"écart contre {REFERENCE} positif ou nul",
                "RETOURNEMENT": f"écart contre {REFERENCE} négatif ou nul",
                "AUCUNE SEQUENCE": (f"écart contre {REFERENCE} dans "
                                    f"± {fr(TOLERANCE_REFLEXIVE, 0)} points"),
            }[phase]
            theses.append({
                "DATE": date, "TICKER": ticker, "TYPE": "REFLEXIVE", "PHASE": phase,
                "ENONCE": f"{phase} : {clause}, au {suivante}",
                "BORNE_BASSE": b_basse, "BORNE_HAUTE": b_haute,
                "DATE_DEPOUILLEMENT": suivante, "VALEUR_CONSTATEE": ecart,
                "VERDICT": depouiller(b_basse, b_haute, ecart),
            })
    return theses


# --------------------------------------------------------------------------
# Phase 6 : les audits


def poids_effectifs(criteres, dates, sens):
    """Part de variance expliquee par chaque composante : Cov(si, score)/Var(score).

    La somme vaut exactement 1 : c'est une decomposition, pas une ponderation
    declaree. Une composante de variance nulle rend 0 — elle ne distingue rien.
    """
    colonnes, scores = {i: [] for i in range(5)}, []
    for ligne in criteres:
        if ligne["ROLE"] != "DECISION" or ligne["DATE"] not in dates:
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


def occurrences_s5(criteres, dates, sens):
    """Rend (occurrences non nulles de s5, evaluations calculables, tickers).

    La composante s5 est celle dont l'experience 1 disait qu'elle valait 0 aux
    144 evaluations de son annee. Compter ses reveils est le seul moyen de savoir
    si elle est inerte ou seulement rare.
    """
    non_nuls, calculables, tickers = 0, 0, {}
    for ligne in criteres:
        if ligne["ROLE"] != "DECISION" or ligne["DATE"] not in dates:
            continue
        valeur = composantes(ligne, sens)[4]
        if valeur is None:
            continue
        calculables += 1
        if valeur != 0:
            non_nuls += 1
            tickers[ligne["TICKER"]] = tickers.get(ligne["TICKER"], 0) + 1
    return non_nuls, calculables, tickers


def taux_vetos(criteres, dates):
    """Rend ({numero: compte}, evaluations sans veto, total)."""
    compte, aucun, total, erreurs = dict.fromkeys((1, 2, 3, 4), 0), 0, 0, 0
    for ligne in criteres:
        if ligne["ROLE"] != "DECISION" or ligne["DATE"] not in dates:
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
    return compte, aucun, total, erreurs


def stabilite(criteres, dates, args):
    """Compare la decision a d, d-1 et d-2 : bascules de s3, de score, de tete."""
    index = {(ligne["ROLE"], ligne["DATE"], ligne["TICKER"]): ligne
             for ligne in criteres}
    resultat = {}
    for pas in DECALAGES:
        role = f"DECALE-{pas}"
        bascules_s3, changements_score, couples, tetes = 0, 0, 0, 0
        for date in dates:
            reference_tete = {ligne["TICKER"] for ligne in classer(criteres, date, "aligne")
                              if ligne["RANG"] <= args.rang_entree}
            decalee = []
            for ticker in UNIVERS:
                base = index.get(("DECISION", date, ticker))
                autre = index.get((role, date, ticker))
                if base is None or autre is None:
                    continue
                couples += 1
                a = composantes(base, "aligne")
                b = composantes(autre, "aligne")
                if a[2] != b[2]:
                    bascules_s3 += 1
                if a[5] != b[5]:
                    changements_score += 1
                decalee.append({"TICKER": ticker, "SCORE": b[5],
                                "MOMENTUM": nombre(autre["MOMENTUM"])})
            decalee.sort(key=lambda x: (-x["SCORE"],
                                        -(x["MOMENTUM"] if x["MOMENTUM"] is not None
                                          else -999), x["TICKER"]))
            if {ligne["TICKER"] for ligne in decalee[:args.rang_entree]} != reference_tete:
                tetes += 1
        resultat[pas] = {"s3": bascules_s3, "score": changements_score,
                         "couples": couples, "tetes": tetes, "dates": len(dates)}
    return resultat


def survie_encadrement(theses, criteres, dates, dates_depouillement, dates_ref):
    """Taux de dementi du canal, part des tau plus courts que la cadence, mediane."""
    canal = [t for t in theses if t["TYPE"] == "CANAL"]
    dementies = sum(1 for t in canal if t["VERDICT"] == "DEMENTIE")
    tranchees = sum(1 for t in canal if t["VERDICT"] != "NON TRANCHEE")

    rang = {jour: i for i, jour in enumerate(dates_ref)}
    ecarts = {date: rang[suivante] - rang[date]
              for date, suivante in zip(dates, dates_depouillement, strict=True)}
    taus, courts, total = [], 0, 0
    for ligne in criteres:
        if ligne["ROLE"] != "DECISION" or ligne["DATE"] not in ecarts:
            continue
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
        "courts": courts, "mesures": total, "infinis": total - len(taus),
        "mediane": statistics.median(taus) if taus else None,
        "cadence": statistics.median(ecarts.values()) if ecarts else None,
    }


def taux_theses(theses, type_, phase=None):
    """Rend (confirmees, tranchees) pour un type, et une phase si elle est donnee."""
    retenues = [t for t in theses if t["TYPE"] == type_
                and (phase is None or t["PHASE"] == phase)]
    tranchees = [t for t in retenues if t["VERDICT"] != "NON TRANCHEE"]
    return sum(1 for t in tranchees if t["VERDICT"] == "CONFIRMEE"), len(tranchees)


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
    }


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
         f'fill="#1a1a1a">Experience 2 &#8212; portefeuille contre {REFERENCE}, '
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
# Phase 8 : la console et les markdown


def bloc_mensuel(mois, etape, etat_apres, valeurs, seances):
    """Rend le bloc console d'un mois."""
    lignes = [
        "",
        (f"=== {mois} · decision au {etape['date_decision']}"
         f" · execution au {etape['date_exec']} ==="),
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

    lignes += ["", f"Exposition heritee au {etape['date_decision']}"]
    if not etape["etat_avant"]:
        lignes.append("  aucune ligne — le portefeuille est integralement en especes")
    for ticker, info in sorted(etape["etat_avant"].items()):
        lignes.append(
            f"  {ticker:<10s} achetee le {info['date']} a {fr(info['prix'])} EUR"
            f"  ·  {signe(info['pv'], 2):>8s} %"
            f"  ·  alpha du mois {signe(info['alpha_mois'], 2):>7s} pt{info['partiel']}"
            f"  ·  alpha global {signe(info['alpha_global'], 2):>7s} pt")

    lignes += ["", f"Ordres executes au {etape['date_exec']}"]
    if not etape["ordres"]:
        lignes.append("  aucun ordre")
    for ordre in etape["ordres"]:
        lignes.append(
            f"  {ordre['SENS']:<6s} {ordre['TICKER']:<10s} {ordre['QUANTITE']:4d} titres"
            f" a {fr(ordre['PRIX']):>9s} EUR  ·  brut {fr(ordre['BRUT']):>10s}"
            f"  frais {fr(ordre['FRAIS']):>6s}  ·  {ordre['MOTIF']}")

    fin_mois = derniere_seance(seances, mois)
    especes, titres, total = valeurs[fin_mois]
    lignes += ["", f"Portefeuille au {fin_mois}"]
    lignes.append(
        f"  especes {fr(especes)} EUR · titres {fr(titres)} EUR · total {fr(total)} EUR")
    lignes.append(
        f"  base 100 : portefeuille {fr(etat_apres['base'], 2)}"
        f" · {REFERENCE} {fr(etat_apres['reference'], 2)}")
    lignes.append(
        f"  alpha du mois {signe(etat_apres['alpha_mois'], 2)} pt"
        f" · alpha depuis janvier {signe(etat_apres['alpha_global'], 2)} pt")
    return NL_.join(lignes)


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


def tableau_exposition(etat_avant):
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
    return NL_.join(lignes)


def tableau_classement(classement):
    """Les douze valeurs, du plus interessant a detenir au plus a fuir."""
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
    return NL_.join(lignes)


def note_en_liste(note):
    """Rend les lignes d'une note en puces : cinq lignes ecrites, cinq lignes lues."""
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


def tableau_depouillement(theses):
    """Les theses du mois precedent, avec leur verdict."""
    if not theses:
        return "*Aucune thèse à dépouiller : c'est la première date du registre.*"
    lignes = ["| Valeur | Thèse | Énoncé | Constaté | Verdict |",
              "|---|---|---|---|---|"]
    for these in theses:
        unite = EURO if these["TYPE"] == "CANAL" else "pt"
        marque = {"CONFIRMEE": "**confirmée**", "DEMENTIE": "démentie",
                  "NON TRANCHEE": "*non tranchée*"}[these["VERDICT"]]
        lignes.append(
            f"| `{these['TICKER']}` | {these['TYPE'].capitalize()} "
            f"| {these['ENONCE']} "
            f"| {fr(these['VALEUR_CONSTATEE'])} {unite} | {marque} |")
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
    """Un paragraphe entierement calcule : aucun recit ecrit apres coup."""
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
            f"Les {len(ordres)} ordres du mois ont coûté **{fr(frais)} {EURO}** de frais, "
            f"soit {fr(100 * frais / dotation, 3)} % de la dotation initiale.")
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
            f"dépouillées, **{confirmees} sont confirmées** — "
            f"{fr(100 * confirmees / tranchees, 1)} %.")
    return " ".join(phrases)


def journal_mensuel(mois, c):
    """Rend le texte complet d'un journal mensuel."""
    bloc = [
        f"# {MOIS_TITRE[mois[5:7]]} {ANNEE}",
        "",
        (f"> Journal de l'[expérience 2](../README.md) · **décision au "
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
        tableau_exposition(c["etat_avant"]),
        "",
        f"## 4. Le portefeuille depuis le {c['debut']}",
        "",
        (f"![Évolution du portefeuille au {c['fin_mois']}]"
         f"(../graphiques/portefeuille-{mois}.svg)"),
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
        f"## 5. L'étude chartiste au {c['date_decision']}",
        "",
        (f"> Notes rédigées sans aucune séance postérieure au "
         f"{c['date_decision']}, par l'agent `chartiste`. "
         f"Cinq lignes au plus par société."),
        "",
    ]
    for ligne in c["classement"]:
        ticker = ligne["TICKER"]
        bloc += [f"### {ligne['RANG']}. `{ticker}` — {SOCIETES[ticker]}", "",
                 note_en_liste(c["notes"].get(ticker, "")) or ABSENTE, ""]

    bloc += [
        f"## 6. Le classement au {c['date_decision']}",
        "",
        ("> De la valeur la plus intéressante à détenir à celle qu'il faut fuir. "
         "La colonne **τ** donne la date de péremption du canal en séances "
         "(piste C4), la colonne **Vetos** les numéros déclenchés (piste T3). "
         "Une valeur sous veto ne peut pas être achetée."),
        "",
        tableau_classement(c["classement"]),
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
                  "quatre audits et la confrontation du dimensionnement sont dans "
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
            continue
        achat = ouvertes.pop(ticker)
        closes.append((achat, ordre))
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


def section_audit_regle(b):
    """Section 4 du bilan — piste T3 : les vetos appliques et les poids effectifs."""
    compte, aucun, total, erreurs = b["vetos"]
    out = [
        "## 4. L'audit de la règle — les vetos et les poids effectifs",
        "",
        ("> Piste **T3**. L'expérience 1 calculait les quatre vetos de la règle du "
         "module 3 et les jetait. Ici ils s'appliquent : une valeur sous veto ne "
         "peut pas entrer. Voici à quelle fréquence ils se déclenchent, sur les "
         f"**{total} évaluations** de la fenêtre d'audit."),
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
        (f"**{erreurs} évaluations sur {total}** n'ont produit aucun critère : le "
         "contrôle de non-traversée de l'enveloppe convexe y échoue, et "
         "`generer_graph_decision.py` sort en 2. Le protocole les traite comme un "
         "veto de plus — une figure qu'on ne sait pas calculer n'est pas une figure "
         "qu'on peut acheter — et elles sont comptées à part plutôt que rangées "
         "dans l'un des quatre vetos, qu'elles n'ont pas déclenchés."),
        "",
        (f"Les vetos ont bloqué **{b['bloques']} entrées** qui auraient eu lieu sans "
         "eux : une valeur classée au rang 5 ou mieux, de score strictement positif, "
         "non détenue, mais sous veto. C'est la différence exacte, sur ce point, "
         "entre la règle de l'expérience 2 et celle de l'expérience 1."),
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
    non_nuls, calculables, tickers = b["s5"]
    detail = ", ".join(f"`{t}` {n} fois" for t, n in sorted(tickers.items()))
    out += [
        "",
        (f"**`s5` s'est réveillée.** L'expérience 1 constatait qu'elle valait `0` "
         "à ses 144 évaluations, et en concluait que l'alpha d'une valeur ne se "
         f"mesure pas sur quelques mois. Sur les {calculables} évaluations "
         f"calculables de la fenêtre d'audit, elle est non nulle **{non_nuls} "
         f"fois** — {detail} — toutes dans l'année narrée, et toutes à `−1` : "
         "l'intervalle de confiance de l'alpha y est **entièrement négatif**."),
        "",
        ("C'est le seul cas de trois ans où la composante distingue quelque chose, "
         "et il va dans un seul sens. Une composante qui ne sait dire que du mal, "
         "et seulement d'une valeur sur douze, n'est pas pour autant à retirer : "
         "la retirer maintenant qu'on l'a vue serait exactement l'ajustement "
         "rétrospectif que ce protocole s'interdit."),
    ]
    return out


def section_sens_s3(b):
    """Section 5 du bilan — piste C3 : le sens de s3 et son portefeuille fantome."""
    dim = b["dimension"]
    return [
        "",
        "## 5. Le sens de `s3` — l'aligné contre le fantôme",
        "",
        ("> Piste **C3**. `s3` a été inversé pour suivre la règle citée : on achète "
         "**bas** dans le canal, pas haut. Le sens de l'expérience 1 tourne en "
         "parallèle, sans engager un euro, et il a été déclaré avant la première "
         "séance."),
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
        ("Les deux dernières lignes sont les **variantes déclarées** du "
         "[protocole](README.md#les-deux-variantes-déclarées) : elles ne décident "
         "rien, elles chiffrent ce que valent deux choix de règle que l'expérience "
         "aurait pu faire autrement."),
        "",
        (f"L'écart entre les deux vaut **{signe(dim['ecart_fantome'])} point** sur "
         "l'année."),
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
    """Section 6 du bilan — piste C4 : la duree de vie du canal contre la cadence."""
    s, stab = b["survie"], b["stabilite"]
    out = [
        "",
        "## 6. La durée de vie de l'encadrement contre la cadence",
        "",
        ("> Piste **C4**. Le score lit une position dans un canal. Encore faut-il "
         "que le canal existe encore au moment où l'on relit."),
        "",
        "| Mesure | Valeur |",
        "|---|---|",
        f"| Cadence médiane entre deux décisions | {fr(s['cadence'], 0)} séances |",
        f"| τ médian, canaux convergents | {fr(s['mediane'], 1)} séances |",
        (f"| Canaux parallèles ou divergents (τ infini) | {s['infinis']} / "
         f"{s['mesures']} |"),
        (f"| Canaux se refermant **avant** la décision suivante | {s['courts']} / "
         f"{s['mesures']} — {fr(100 * s['courts'] / s['mesures'], 1)} % |"),
        (f"| Clôtures **sorties** de l'encadrement prolongé | {s['dementies']} / "
         f"{s['tranchees']} — {fr(100 * s['dementies'] / s['tranchees'], 1)} % "
         f"± {fr(ic95(s['dementies'], s['tranchees']), 1)} pt |"),
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
        out.append(
            f"| **d−{pas}** | {r['s3']} / {r['couples']} "
            f"— {fr(100 * r['s3'] / r['couples'], 1)} % "
            f"| {r['score']} / {r['couples']} "
            f"— {fr(100 * r['score'] / r['couples'], 1)} % "
            f"| {r['tetes']} / {r['dates']} |")
    return out


def section_theses(b):
    """Section 7 du bilan — piste S4 : le registre et ses taux de confirmation."""
    theses = b["theses"]
    out = [
        "",
        "## 7. Le registre des thèses réfutables",
        "",
        ("> Piste **S4**. Deux thèses par valeur et par date de décision, "
         f"**{len(theses)} en tout**, engendrées mécaniquement et dépouillées à la "
         "date suivante. Aucune n'a été rédigée à la main, aucune n'a été retirée."),
        "",
        "| Thèse | Confirmées | Taux | IC95 |",
        "|---|---|---|---|",
    ]
    for libelle, type_, phase in (
        ("`CANAL` — la figure tient", "CANAL", None),
        ("`REFLEXIVE` — toutes phases", "REFLEXIVE", None),
        ("└ `AUTO-RENFORCEMENT`", "REFLEXIVE", "AUTO-RENFORCEMENT"),
        ("└ `RETOURNEMENT`", "REFLEXIVE", "RETOURNEMENT"),
        ("└ `AUCUNE SEQUENCE`", "REFLEXIVE", "AUCUNE SEQUENCE"),
    ):
        confirmees, tranchees = taux_theses(theses, type_, phase)
        if not tranchees:
            out.append(f"| {libelle} | — | *aucune occurrence* | — |")
            continue
        out.append(
            f"| {libelle} | {confirmees} / {tranchees} "
            f"| {fr(100 * confirmees / tranchees, 1)} % "
            f"| ± {fr(ic95(confirmees, tranchees), 1)} pt |")
    out += [
        "",
        ("La ligne `AUCUNE SEQUENCE` est celle qui compte le plus. C'est le défaut "
         "de charte de l'agent [`sorosien`](../../../../.claude/agents/sorosien.md) "
         "— *« aucune séquence réflexive identifiable »* — rendu réfutable : dire "
         "qu'il ne se passe rien, c'est prédire que l'écart contre "
         f"`{REFERENCE}` restera dans ± {fr(TOLERANCE_REFLEXIVE, 0)} points sur le "
         "mois. Le taux ci-dessus dit à quelle fréquence ce défaut prudent est quand "
         "même démenti."),
    ]
    return out


def section_dimensionnement(b):
    """Section 9 du bilan — piste T1 : le dimensionnement declare, confronte."""
    dim = b["dimension"]
    return [
        "",
        "## 9. Le dimensionnement, confronté",
        "",
        ("> Piste **T1**. Le "
         "[protocole](README.md#le-dimensionnement-publié-avant-la-première-séance) "
         "a publié **avant la première séance** une tracking error attendue de "
         f"{fr(TE_DECLAREE)} %/an, mesurée sur l'expérience 1, et l'effet minimal "
         "détectable qui en découlait. Voici ce qui s'est réellement produit."),
        "",
        "| | Déclaré avant | Réalisé |",
        "|---|---|---|",
        (f"| Tracking error annualisée | {fr(TE_DECLAREE)} %/an "
         f"| **{fr(dim['te'])} %/an** |"),
        (f"| Effet minimal détectable sur un an | ± {fr(Z95 * TE_DECLAREE, 1)} pt "
         f"| **± {fr(dim['mde'], 1)} pt** |"),
        f"| Alpha mesuré | — | {signe(dim['alpha'])} pt |",
        "",
        (f"L'alpha de l'année vaut {signe(dim['alpha'])} point pour un effet minimal "
         f"détectable de ± {fr(dim['mde'], 1)} points. **Il est indiscernable de "
         "zéro**, et il était déclaré comme tel avant la première séance — ce qui est "
         "toute la différence avec l'expérience 1, qui a publié le sien comme un "
         "résultat."),
        "",
        "## 10. Ce que l'expérience établit, et ce qu'elle n'établit pas",
        "",
        "**Elle établit**, avec les incertitudes publiées :",
        "",
        (f"- à quelle fréquence chacun des quatre vetos de la règle se déclenche — "
         f"§ 4, sur {b['vetos'][2]} évaluations ;"),
        ("- à quelle fréquence l'encadrement que le score lit ne survit pas d'une "
         "décision à la suivante — § 6 ;"),
        ("- à quelle fréquence `s3` bascule quand on décale la décision d'une seule "
         "séance — § 6, et c'est une propriété de la composante, pas de l'année ;"),
        ("- à quelle fréquence les thèses engendrées par la règle sont démenties, "
         "par type et par phase — § 7."),
        "",
        "**Elle n'établit pas** :",
        "",
        (f"- que la règle est bonne ou mauvaise. L'alpha de l'année, "
         f"{signe(dim['alpha'])} point, est plus petit que son propre effet minimal "
         f"détectable de ± {fr(dim['mde'], 1)} points ;"),
        ("- quel sens de `s3` est le bon. L'écart apparié au fantôme est mesuré, son "
         "incertitude aussi, et l'un ne dépasse pas l'autre en un an ;"),
        "- quoi que ce soit sur 2026. Aucune quantité mesurée ici ne se prolonge.",
        "",
        ("Ce qui reste acquis est de nature différente : **les lignes du tableau de "
         "dimensionnement ont été écrites avant de regarder l'année, et ce sont "
         "exactement celles que l'expérience a pu remplir.** C'est ce qu'une "
         "expérience sur une année passée peut honnêtement offrir."),
        "",
        "---",
        "",
        (f"[← Protocole](README.md) · [Décembre]({RAPPORTS}/{ANNEE}-12.md) · "
         f"[Janvier]({RAPPORTS}/{ANNEE}-01.md) · "
         f"[La revue de l'expérience 1](../experience_1/review.md)"),
    ]


def bilan_annuel(b):
    """Rend le document complet du bilan de l'annee."""
    out = [
        f"# Bilan de l'année {ANNEE}",
        "",
        (f"> [Expérience 2](README.md) · dotation {fr(b['dotation'])} {EURO} au "
         f"{b['debut']}, arrêt au {b['fin']} · **{signe(b['base'] - 100)} %** contre "
         f"**{signe(b['ref_fin'] - 100)} %** pour {REFERENCE}"),
        "",
        ("> ⚠️ **L'alpha de cette ligne ne tranche rien**, et le "
         "[protocole](README.md#le-dimensionnement-publié-avant-la-première-séance) "
         "le déclarait avant la première séance. Ce que ce bilan établit est dans "
         "les sections 4 à 7."),
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
            "",
            (("Le contrefactuel « garder le portefeuille de janvier jusqu'au bout » "
              "**n'existe pas cette année** : aucun achat n'a eu lieu à la première "
              "séance, les vetos ayant écarté les deux seules valeurs de score "
              "positif. Le tenir aurait donc voulu dire rester en espèces douze "
              f"mois, pour {fr(100 * b['tenu'] / b['dotation'])} en base 100.")
             if b["achats_debut"] == 0 else
             ("Le contrefactuel qui isole l'apport des ordres suivant janvier : "
              "**garder le portefeuille de janvier jusqu'au bout** aurait rendu "
              f"{fr(100 * b['tenu'] / b['dotation'])} au lieu de {fr(b['base'])}, soit "
              f"**{signe(b['base'] - 100 * b['tenu'] / b['dotation'])} point**.")),
        ]
    else:
        out += ["", "*Aucune position ouverte sur l'année.*"]

    out += ["", *section_audit_regle(b)]
    out += section_sens_s3(b)
    out += section_encadrement(b)
    out += section_theses(b)
    out += [
        "",
        "## 8. Les trois conventions",
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


def entrees_bloquees(historique, args):
    """Compte les entrees qu'un veto a interdites — la difference exacte avec l'exp. 1."""
    bloquees, tenues = 0, set()
    for etape in historique:
        for ligne in etape["classement"]:
            if (ligne["RANG"] <= args.rang_entree and ligne["SCORE"] > 0
                    and ligne["ACTIFS"] and ligne["TICKER"] not in tenues):
                bloquees += 1
        tenues = set(etape["tenues"])
    return bloquees


def analyser_arguments():
    parser = argparse.ArgumentParser(
        description=f"Journal de l'experience 2 : 10 000 EUR sur {ANNEE}, regle auditee.")
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
                        help="Diagnostic : simuler aussi sans appliquer les vetos")
    args = parser.parse_args()
    if args.rang_sortie < args.rang_entree:
        erreur("--rang-sortie doit etre superieur ou egal a --rang-entree (hysteresis)")
    if args.dotation <= 0:
        erreur("--dotation doit etre strictement positive")
    if not 1 <= args.lignes <= len(UNIVERS):
        erreur(f"--lignes doit etre entre 1 et {len(UNIVERS)}")
    if not 1 <= args.taches <= 32:
        erreur("--taches doit etre entre 1 et 32")
    return args


def ecrire_rapports(args, contexte, historique, theses_par_date, textes):
    """Ecrit les douze journaux mensuels."""
    actualites, notes = textes
    valeurs, ref100, seances = contexte["valeurs"], contexte["ref100"], contexte["seances"]
    executions = [etape["date_exec"] for etape in historique]
    debut = contexte["debut"]

    for rang, etape in enumerate(historique):
        mois, date_decision = etape["mois"], etape["date_decision"]
        fin_mois = derniere_seance(seances, mois)
        jours = [j for j in seances if j <= fin_mois]
        courbe = [100 * valeurs[j][2] / args.dotation for j in jours]
        svg(args.repertoire / "graphiques" / f"portefeuille-{mois}.svg",
            jours, courbe, [ref100[j] for j in jours], executions, debut)

        veille = derniere_seance(seances, mois_precedent(mois))
        base_p = valeurs[veille][2] if veille else args.dotation
        base_r = ref100[veille] if veille else 100.0
        alpha_mois = 100 * (valeurs[fin_mois][2] / base_p - ref100[fin_mois] / base_r)

        apports = []
        for ticker, info in etape["tenues"].items():
            base_prix = (series_close(contexte, ticker, veille)
                         if veille and info["date"] <= veille else info["prix"])
            apports.append({
                "ticker": ticker,
                "euros": info["quantite"] * (series_close(contexte, ticker, fin_mois)
                                             - base_prix),
            })

        precedente = contexte["date_precedente"][date_decision]
        depouillement = theses_par_date.get(precedente, [])
        confirmees = sum(1 for t in depouillement if t["VERDICT"] == "CONFIRMEE")
        tranchees = sum(1 for t in depouillement if t["VERDICT"] != "NON TRANCHEE")

        precedent_mois, suivant_mois = mois_precedent(mois), suivant(mois)
        navigation = []
        if rang > 0:
            navigation.append(f"[← {MOIS_TITRE[precedent_mois[5:7]]}]"
                              f"({precedent_mois}.md)")
        navigation.append("[Protocole](../README.md)")
        if rang + 1 < len(historique):
            navigation.append(f"[{MOIS_TITRE[suivant_mois[5:7]]} →]"
                              f"({suivant_mois}.md)")

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
            "etat_avant": etape["etat_avant"], "classement": etape["classement"],
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


def suivant(mois):
    """« 2025-11 » -> « 2025-12 », « 2025-12 » -> « 2026-01 »."""
    annee, numero = int(mois[:4]), int(mois[5:7])
    return f"{annee + 1}-01" if numero == 12 else f"{annee}-{numero + 1:02d}"


def series_close(contexte, ticker, jour):
    return contexte["series"][ticker][jour]["close"]


def main():
    args = analyser_arguments()
    if not args.quotes.is_dir():
        erreur(f"Repertoire introuvable : {args.quotes}")

    series = {t: charger_serie(nom_fichier(t, args.quotes)) for t in UNIVERS}
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

    if args.collecter or args.recollecter:
        print("Collecte des criteres par python/generer_graph_decision.py")
        collecter(dates_a_evaluer(audit, investis, dates_ref), args.quotes,
                  args.repertoire, series, args.taches,
                  reprendre=not args.recollecter)

    chemin_criteres = args.repertoire / "criteres.csv"
    if not chemin_criteres.exists():
        erreur(f"{chemin_criteres} absent : relancer avec --collecter")
    with chemin_criteres.open(encoding="utf-8") as flux:
        criteres = list(csv.DictReader(flux))

    debut, fin = investis[0][1], dates_ref[-1]
    seances = [d for d in dates_ref if debut <= d <= fin]
    ref100 = {j: 100 * reference[j]["close"] / reference[debut]["close"] for j in seances}

    ordres, valeurs, historique = simuler(investis, criteres, series, reference,
                                          seances, args, "aligne")
    ordres_f, valeurs_f, _ = simuler(investis, criteres, series, reference,
                                     seances, args, "fantome")
    ordres_c, valeurs_c, _ = simuler(investis, criteres, series, reference, seances,
                                     args, "aligne", repartition="candidats")
    ordres_l, valeurs_l, _ = simuler(investis, criteres, series, reference, seances,
                                     args, "aligne", vetos_appliques=False)

    dates_audit = [decision for decision, _ in audit]
    dates_depouillement = [*dates_audit[1:], fin]
    theses = ecrire_theses(criteres, dates_audit, dates_depouillement, series,
                           reference, dates_ref)
    theses_par_date = {}
    for these in theses:
        theses_par_date.setdefault(these["DATE"], []).append(these)

    classements = []
    for date in dates_audit:
        for ligne in classer(criteres, date, "aligne"):
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
        "debut": debut,
        "date_precedente": {decision: dates_audit[i - 1] if i > 0 else ""
                            for i, decision in enumerate(dates_audit)},
    }

    if args.markdown:
        textes = charger_textes(args.repertoire)
        ecrire_rapports(args, contexte, historique, theses_par_date, textes)

    pic, repli, creux = -1e9, 0.0, fin
    for jour in seances:
        pic = max(pic, valeurs[jour][2])
        if valeurs[jour][2] / pic - 1 < repli:
            repli, creux = valeurs[jour][2] / pic - 1, jour

    b = {
        "dotation": args.dotation, "debut": debut, "fin": fin,
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
        "positions": positions_de_lannee(ordres, series, reference, fin),
        "tenu": janvier_tenu(ordres, series, args.dotation, debut, fin),
        "achats_debut": sum(1 for o in ordres
                            if o["DATE"] == debut and o["SENS"] == "ACHAT"),
        "vetos": taux_vetos(criteres, set(dates_audit)),
        "bloques": entrees_bloquees(historique, args),
        "poids_etalonnage": poids_effectifs(criteres,
                                            {d for d, _ in etalonnage}, "aligne"),
        "poids_audit": poids_effectifs(criteres, set(dates_audit), "aligne"),
        "s5": occurrences_s5(criteres, set(dates_audit), "aligne"),
        "stabilite": stabilite(criteres, [etape["date_decision"] for etape in historique],
                               args),
        "survie": survie_encadrement(theses, criteres, dates_audit,
                                     dates_depouillement, dates_ref),
        "theses": theses,
        "dimension": dimensionnement(valeurs, ref100, valeurs_f, seances, args.dotation),
    }

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
        print(bloc_mensuel(mois, etape, etat_apres, valeurs, seances))

    if args.sans_veto:
        ordres_libres, valeurs_libres, _ = simuler(
            investis, criteres, series, reference, seances, args, "aligne",
            vetos_appliques=False)
        print(f"""
=== Diagnostic --sans-veto ===

  Avec vetos              {fr(b['base'])} base 100, {len(ordres)} ordres
  Sans vetos              {fr(100 * valeurs_libres[fin][2] / args.dotation)} \
base 100, {len(ordres_libres)} ordres
  Entrees bloquees        {b['bloques']}
""")

    dim = b["dimension"]
    confirmees, tranchees = 0, 0
    for these in theses:
        if these["VERDICT"] != "NON TRANCHEE":
            tranchees += 1
            confirmees += these["VERDICT"] == "CONFIRMEE"
    compte, aucun, total, erreurs = b["vetos"]
    print(f"""
=== Bilan au {fin} ===

  Dotation                {fr(args.dotation)} EUR au {debut}
  Valeur finale           {fr(valeurs[fin][2])} EUR
  Performance             {signe(b['base'] - 100)} %
  {REFERENCE}                    {signe(ref100[fin] - 100)} %
  Alpha sur l'annee       {signe(b['base'] - ref100[fin])} pt \
(non concluant : MDE +/- {fr(dim['mde'], 1)} pt)

  Fantome (s3 exp. 1)     {fr(b['base_fantome'])} base 100 \
· ecart appari {signe(dim['ecart_fantome'])} pt (MDE +/- {fr(dim['mde_paire'], 1)} pt)
  Ordres                  {len(ordres)} ({b['achats']} achats, \
{len(ordres) - b['achats']} ventes)
  Frais cumules           {fr(b['frais'])} EUR, soit \
{fr(100 * b['frais'] / args.dotation)} % de la dotation
  Vetos declenches        {total - aucun} / {total} evaluations \
(1:{compte[1]} 2:{compte[2]} 3:{compte[3]} 4:{compte[4]}) · {erreurs} evaluations impossibles
  Entrees bloquees        {b['bloques']}
  Theses depouillees      {confirmees} confirmees sur {tranchees}
""")
    ecrits = ["classement.csv", "ordres.csv", "theses.csv", "portefeuille.csv",
              "fantome.csv"]
    if args.markdown:
        ecrits += [f"graphiques/portefeuille-{ANNEE}-MM.svg ({len(historique)} mois)",
                   f"{RAPPORTS}/{ANNEE}-MM.md ({len(historique)} rapports)", BILAN]
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
