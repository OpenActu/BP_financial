"""Moteur de l'experience 1 : un portefeuille de 10 000 EUR sur l'annee 2022.

Classe l'univers declare a chaque fin de mois a partir des cinq criteres de la
regle du module 3, en deduit les ordres, execute a l'ouverture suivante,
comptabilise, et ecrit les graphiques.

Le protocole est dans README.md, le miroir d'execution dans journal.md.

Utilisation :
    python docs/done/experimentation/experience_1/journal.py --collecter
    python docs/done/experimentation/experience_1/journal.py
    python docs/done/experimentation/experience_1/journal.py --mois 2022-03
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

UNIVERS = (
    "AIR.PA", "MC.PA", "OR.PA", "SAN.PA", "BNP.PA", "TTE.PA",
    "SU.PA", "AI.PA", "DG.PA", "CAP.PA", "RI.PA", "ORA.PA",
)
REFERENCE = "TR12"
REFERENCE_NUE = "^FCHI"
RAPPORTS = "rapports"
BILAN = "bilan-2022.md"
DEBUT_SERIE = "2020-01-02"   # premiere seance des CSV, deux ans d'amorce
FIN_SERIE = "2022-12-30"     # derniere seance des CSV
DEBUT = "2022-01-03"
FIN = "2022-12-30"
PREMIERE_DECISION = "2021-12-31"

COURTAGE = 0.10
SPREAD = 0.015
TTF = 0.30
EXEMPTES_TTF = ("AIR.PA",)

QUOTES_DEFAUT = Path("docs/raw/data/quotes")
REGLE = Path("python/generer_graph_decision.py")

ENTETE_CRITERES = [
    "DATE", "TICKER", "CLOSE", "TEND_120", "TEND_20", "POSITION",
    "ALPHA", "ALPHA_BAS", "ALPHA_HAUT", "MOMENTUM", "VETOS", "VERDICT",
]
ENTETE_CLASSEMENT = [
    "DATE", "RANG", "TICKER", "S1", "S2", "S3", "S4", "S5", "SCORE",
    "POSITION", "MOMENTUM", "VERDICT_REGLE",
]
ENTETE_ORDRES = [
    "DATE", "TICKER", "SENS", "QUANTITE", "PRIX", "BRUT", "FRAIS", "NET",
    "RANG", "SCORE", "MOTIF",
]
ENTETE_PORTEFEUILLE = ["DATE", "ESPECES", "TITRES", "TOTAL", "BASE100", "REFERENCE100"]

NBSP = " "

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
ABSENTE = "*(section absente)*"
NL_ = chr(10)
EURO = "\u20ac"


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


def nom_fichier(ticker, quotes):
    """Rend le CSV de la plage declaree. Un glob choisirait le mauvais fichier
    des qu'une autre plage du meme ticker traine dans le repertoire."""
    chemin = quotes / f"{ticker.replace('.', '_')}_{DEBUT_SERIE}_{FIN_SERIE}.csv"
    if not chemin.exists():
        erreur(f"Serie absente : {chemin}\n"
               f"  python python/import_societe.py {ticker} "
               f"--debut {DEBUT_SERIE} --fin 2023-01-01")
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
    """Rend [(date de decision, date d'execution)] pour les douze mois de 2022."""
    par_mois = {}
    for jour in dates:
        par_mois.setdefault(jour[:7], []).append(jour)
    mois = sorted(par_mois)
    couples = []
    for i, cle in enumerate(mois[:-1]):
        if PREMIERE_DECISION[:7] <= cle < FIN[:7]:
            couples.append((par_mois[cle][-1], par_mois[mois[i + 1]][0]))
    return couples


# --------------------------------------------------------------------------
# Phase 1 : la collecte des criteres, par le code du depot

MOTIFS = {
    "TEND_120": r"Crit.re 1.*?:\s*([+-]?\d)",
    "TEND_20": r"Crit.re 2.*?:\s*([+-]?\d)",
    "POSITION": r"Crit.re 3.*?:\s*([+-]?[\d,]+)\s*%",
    "ALPHA": r"Crit.re 4.*?:\s*([+-]?[\d   ,]+?)\s*%/an",
    "MOMENTUM": r"Crit.re 5.*?:\s*([+-]?[\d   ,]+?)\s*%",
}
MOTIF_IC = (
    r"IC95\s*\[\s*([+-]?[\d   ,]+?)\s*;\s*([+-]?[\d   ,]+?)\s*\]"
)


def nombre(texte):
    """Convertit « -11,38 » ou « +1 234,5 » en flottant. Rend None si illisible."""
    if texte is None or texte == "":
        return None
    net = texte.replace(NBSP, "").replace(" ", "").replace(" ", "").replace(",", ".")
    try:
        return float(net)
    except ValueError:
        return None


def extraire(sortie):
    """Tire les cinq criteres, les vetos et le verdict de la console de la regle."""
    champs = {cle: nombre(t.group(1)) if (t := re.search(motif, sortie)) else None
              for cle, motif in MOTIFS.items()}
    ic = re.search(MOTIF_IC, sortie)
    champs["ALPHA_BAS"] = nombre(ic.group(1)) if ic else None
    champs["ALPHA_HAUT"] = nombre(ic.group(2)) if ic else None
    vetos = re.search(r"Vetos\s*:\s*(.+)", sortie)
    champs["VETOS"] = vetos.group(1).strip() if vetos else ""
    verdict = re.search(r"VERDICT\s*:\s*(\S+)", sortie)
    champs["VERDICT"] = verdict.group(1) if verdict else ""
    return champs


def collecter(couples, quotes, repertoire, series):
    """Lance la regle du depot sur chaque couple (valeur, date) et ecrit criteres.csv."""
    jetable = repertoire / "graphiques" / "_jetable.svg"
    jetable.parent.mkdir(parents=True, exist_ok=True)
    chemin_reference = nom_fichier(REFERENCE, quotes)
    lignes = []
    total = len(couples) * len(UNIVERS)
    for date_decision, _ in couples:
        for ticker in UNIVERS:
            print(f"  [{len(lignes) + 1:3d}/{total}] {ticker:8s} {date_decision}", end="\r")
            issue = subprocess.run(
                [sys.executable, str(REGLE),
                 "--csv", str(nom_fichier(ticker, quotes)),
                 "--indice", str(chemin_reference),
                 "--date", date_decision,
                 "--sortie", str(jetable)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                check=False,
            )
            if issue.returncode != 0:
                champs = {cle: None for cle in ENTETE_CRITERES[3:]}
                champs["VETOS"] = ""
                champs["VERDICT"] = "ERREUR"
            else:
                champs = extraire(issue.stdout)
            seance = series[ticker].get(date_decision)
            lignes.append({
                "DATE": date_decision, "TICKER": ticker,
                "CLOSE": seance["close"] if seance else None,
                **{cle: champs.get(cle) for cle in ENTETE_CRITERES[3:]},
            })
    print(" " * 64, end="\r")
    if jetable.exists():
        jetable.unlink()

    chemin = repertoire / "criteres.csv"
    ecrire_csv(chemin, ENTETE_CRITERES, lignes)
    print(f"  {len(lignes)} evaluations ecrites dans {chemin}")


def ecrire_csv(chemin, entete, lignes):
    """Ecrit un CSV, cellule vide plutot qu'un nombre invente."""
    with chemin.open("w", newline="", encoding="utf-8") as flux:
        plume = csv.DictWriter(flux, fieldnames=entete)
        plume.writeheader()
        for ligne in lignes:
            plume.writerow({c: ("" if ligne.get(c) is None else ligne[c]) for c in entete})


# --------------------------------------------------------------------------
# Phase 2 : le score et le classement


def composantes(ligne):
    """Rend (s1, s2, s3, s4, s5, score) a partir d'une ligne de criteres.csv."""
    tend_120, tend_20 = nombre(ligne["TEND_120"]), nombre(ligne["TEND_20"])
    position, momentum = nombre(ligne["POSITION"]), nombre(ligne["MOMENTUM"])
    bas, haut = nombre(ligne["ALPHA_BAS"]), nombre(ligne["ALPHA_HAUT"])

    s1 = None if tend_120 is None else 2 * int(tend_120)
    s2 = None if tend_20 is None else int(tend_20)

    s3 = None if position is None else (
        1 if position >= 50 else 0 if position >= 20 else -1)

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


def classer(criteres, date):
    """Rend les douze valeurs du jour, de la plus interessante a la moins."""
    lignes = []
    for ligne in criteres:
        if ligne["DATE"] != date:
            continue
        s1, s2, s3, s4, s5, score = composantes(ligne)
        lignes.append({
            "DATE": date, "TICKER": ligne["TICKER"],
            "S1": s1, "S2": s2, "S3": s3, "S4": s4, "S5": s5, "SCORE": score,
            "POSITION": nombre(ligne["POSITION"]), "MOMENTUM": nombre(ligne["MOMENTUM"]),
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
    """Rend les ordres de vente du mois. Ne modifie rien."""
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
            "RANG": ligne["RANG"], "SCORE": ligne["SCORE"], "MOTIF": motif,
        })
    return ordres


def acheter(positions, classement, date_exec, series, especes, args):
    """Rend les ordres d'achat, especes reparties a parts egales. Ne modifie rien."""
    candidats = [ligne for ligne in classement
                 if ligne["RANG"] <= args.rang_entree and ligne["SCORE"] > 0
                 and ligne["TICKER"] not in positions]
    candidats = candidats[:max(args.lignes - len(positions), 0)]
    if not candidats or especes <= 0:
        return []
    part = especes / len(candidats)
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
            "RANG": ligne["RANG"], "SCORE": ligne["SCORE"],
            "MOTIF": f"rang {ligne['RANG']}, score {ligne['SCORE']:+d}",
        })
    return ordres


# --------------------------------------------------------------------------
# Phase 5 : le graphique


def pas_de_grille(amplitude):
    for pas in (0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100):
        if amplitude / pas <= 8:
            return pas
    return 200


def svg(chemin, dates, portefeuille, reference, executions):
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
         f'fill="#1a1a1a">Experience 1 &#8212; portefeuille contre {REFERENCE}, '
         f'base 100 au {DEBUT}</text>'),
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
# Phase 4 : la comptabilite, et l'affichage


def derniere_seance(seances, mois):
    jours = [j for j in seances if j[:7] == mois]
    return jours[-1] if jours else None


def mois_precedent(mois):
    """« 2022-03 » -> « 2022-02 », « 2022-01 » -> « 2021-12 »."""
    annee, numero = int(mois[:4]), int(mois[5:7])
    return f"{annee - 1}-12" if numero == 1 else f"{annee}-{numero - 1:02d}"


def bloc_mensuel(mois, date_decision, date_exec, classement, ordres,
                 etat_avant, etat_apres, valeurs, seances):
    """Rend le bloc console d'un mois, pret a etre repris dans le markdown."""
    lignes = [
        "",
        f"=== {mois} · decision au {date_decision} · execution au {date_exec} ===",
        "",
        "Classement au " + date_decision,
        "  rang  valeur      s1  s2  s3  s4  s5  score   position   momentum  regle",
    ]
    for ligne in classement:
        lignes.append(
            f"  {ligne['RANG']:4d}  {ligne['TICKER']:<10s}"
            f"  {ent(ligne['S1'])} {ent(ligne['S2'])} {ent(ligne['S3'])}"
            f" {ent(ligne['S4'])} {ent(ligne['S5'])}  {ligne['SCORE']:+5d}"
            f"  {fr(ligne['POSITION'], 1):>7s} %  {signe(ligne['MOMENTUM'], 1):>8s} %"
            f"  {ligne['VERDICT_REGLE']}")

    lignes += ["", f"Exposition heritee au {date_decision}"]
    if not etat_avant:
        lignes.append("  aucune ligne — le portefeuille est integralement en especes")
    for ticker, info in sorted(etat_avant.items()):
        lignes.append(
            f"  {ticker:<10s} achetee le {info['date']} a {fr(info['prix'])} EUR"
            f"  ·  {signe(info['pv'], 2):>8s} %"
            f"  ·  alpha du mois {signe(info['alpha_mois'], 2):>7s} pt{info['partiel']}"
            f"  ·  alpha global {signe(info['alpha_global'], 2):>7s} pt")

    lignes += ["", f"Ordres executes au {date_exec}"]
    if not ordres:
        lignes.append("  aucun ordre")
    for ordre in ordres:
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
        f" · alpha depuis le {DEBUT} {signe(etat_apres['alpha_global'], 2)} pt")
    return "\n".join(lignes)


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
               "| Position | Momentum 12-1 |"),
              "|---|---|---|---|---|---|---|---|---|---|"]
    for ligne in classement:
        ticker = ligne["TICKER"]
        lignes.append(
            f"| {ligne['RANG']} | `{ticker}` {SOCIETES[ticker]} "
            f"| {ent(ligne['S1']).strip()} | {ent(ligne['S2']).strip()} "
            f"| {ent(ligne['S3']).strip()} | {ent(ligne['S4']).strip()} "
            f"| {ent(ligne['S5']).strip()} | **{ligne['SCORE']:+d}** "
            f"| {fr(ligne['POSITION'], 1)} % | {signe(ligne['MOMENTUM'], 1)} % |")
    return NL_.join(lignes)


def note_en_liste(note):
    """Rend les lignes d'une note en puces : cinq lignes ecrites, cinq lignes lues.

    Sans cela, des lignes consecutives fusionnent en un seul paragraphe au rendu
    markdown, et la contrainte des cinq lignes devient invisible.
    """
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


def lecture_du_mois(apports, ordres, alpha_mois):
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
            f"soit {fr(100 * frais / 10000, 3)} % de la dotation initiale.")
    else:
        phrases.append("Aucun ordre, donc aucun frais : l'hystérésis a retenu le "
                       "portefeuille en l'état.")
    sens = "devant" if alpha_mois >= 0 else "derrière"
    phrases.append(
        f"Le portefeuille termine le mois **{sens} {REFERENCE}** de "
        f"{fr(abs(alpha_mois))} point.")
    return " ".join(phrases)


def journal_mensuel(mois, c):
    """Rend le texte complet d'un journal mensuel."""
    bloc = [
        f"# {MOIS_TITRE[mois[5:7]]} 2022",
        "",
        (f"> Journal de l'[expérience 1](../README.md) · **décision au "
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
        f"## 2. L'exposition héritée au {c['date_decision']}",
        "",
        tableau_exposition(c["etat_avant"]),
        "",
        "## 3. Le portefeuille depuis le 3 janvier 2022",
        "",
        (f"![Évolution du portefeuille au {c['fin_mois']}]"
         f"(../graphiques/portefeuille-{mois}.svg)"),
        "",
        "| | |",
        "|---|---|",
        f"| Dotation initiale | {fr(c['dotation'])} {EURO} au 2022-01-03 |",
        f"| Titres au {c['fin_mois']} | {fr(c['titres'])} {EURO} |",
        f"| Espèces | {fr(c['especes'])} {EURO} |",
        f"| **Total** | **{fr(c['total'])} {EURO}** |",
        f"| Base 100 | **{fr(c['base'])}** |",
        f"| {REFERENCE}, même base | {fr(c['reference'])} |",
        f"| Écart depuis janvier | **{signe(c['alpha_global'])} pt** |",
        "",
        f"## 4. L'étude chartiste au {c['date_decision']}",
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
        f"## 5. Le classement au {c['date_decision']}",
        "",
        ("> De la valeur la plus intéressante à détenir à celle qu'il faut "
         "fuir. Le détail des cinq composantes est dans le "
         "[protocole](../README.md#le-score-en-cinq-composantes)."),
        "",
        tableau_classement(c["classement"]),
        "",
        f"## 6. Les ordres exécutés au {c['date_exec']}",
        "",
        (f"> À l'**ouverture** de la séance, jamais à la clôture "
         f"du {c['date_decision']}."),
        "",
        tableau_ordres(c["ordres"]),
        "",
        "## 7. La lecture du mois",
        "",
        c["lecture"],
        "",
    ]
    if c.get("dernier"):
        bloc += ["---", "",
                 ("L'expérience s'arrête ici. Le compte complet de l'année — mois "
                  "par mois, position par position, avec ce que la rotation a "
                  f"coûté — est dans le **[bilan de l'année](../{BILAN})**."),
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
    for achat, vente in closes + [(a, None) for a in ouvertes.values()]:
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


def janvier_tenu(ordres, series, args, fin):
    """Le contrefactuel : le portefeuille du premier mois, garde sans un ordre."""
    premiers = [o for o in ordres if o["DATE"] == DEBUT and o["SENS"] == "ACHAT"]
    especes = args.dotation - sum(o["NET"] for o in premiers)
    titres = sum(o["QUANTITE"] * series[o["TICKER"]][fin]["close"] for o in premiers)
    return especes + titres


def bilan_annuel(args, valeurs, ref100, ordres, seances, series, reference, nue):
    """Rend le document complet du bilan de l'annee."""
    fin = seances[-1]
    total = valeurs[fin][2]
    base = 100 * total / args.dotation
    frais = sum(o["FRAIS"] for o in ordres)
    achats = sum(1 for o in ordres if o["SENS"] == "ACHAT")
    pic, repli, creux = -1e9, 0.0, fin
    for jour in seances:
        pic = max(pic, valeurs[jour][2])
        if valeurs[jour][2] / pic - 1 < repli:
            repli, creux = valeurs[jour][2] / pic - 1, jour

    out = [
        "# Bilan de l'année 2022",
        "",
        (f"> [Expérience 1](README.md) · dotation {fr(args.dotation)} {EURO} au "
         f"{DEBUT}, arrêt au {fin} · **{signe(base - 100)} %** contre "
         f"**{signe(ref100[fin] - 100)} %** pour {REFERENCE}"),
        "",
        "---",
        "",
        "## 1. Le compte",
        "",
        "| | |",
        "|---|---|",
        f"| Dotation | {fr(args.dotation)} {EURO} au {DEBUT} |",
        f"| Valeur finale | **{fr(total)} {EURO}** |",
        f"| Performance | **{signe(base - 100)} %** |",
        f"| {REFERENCE}, même convention | {signe(ref100[fin] - 100)} % |",
        f"| **Alpha sur l'année** | **{signe(base - ref100[fin])} pt** |",
        f"| Ordres | {len(ordres)} ({achats} achats, {len(ordres) - achats} ventes) |",
        (f"| Frais cumulés | {fr(frais)} {EURO}, soit "
         f"{fr(100 * frais / args.dotation)} % de la dotation |"),
        f"| Repli maximal | {signe(100 * repli)} %, creux au {creux} |",
        f"| Espèces au {fin} | {fr(valeurs[fin][0])} {EURO} |",
        "",
        "## 2. Mois par mois",
        "",
        (f"| Mois | Valeur | Base 100 | {REFERENCE} | Alpha du mois "
         "| Alpha cumulé | Ordres |"),
        "|---|---|---|---|---|---|---|",
    ]
    for mois in sorted({j[:7] for j in seances}):
        borne = derniere_seance(seances, mois)
        veille = derniere_seance(seances, mois_precedent(mois))
        base_p = valeurs[veille][2] if veille else args.dotation
        base_r = ref100[veille] if veille else 100.0
        alpha_mois = 100 * (valeurs[borne][2] / base_p - ref100[borne] / base_r)
        nombre = sum(1 for o in ordres if o["DATE"][:7] == mois)
        out.append(
            f"| {MOIS_TITRE[mois[5:7]]} | [{fr(valeurs[borne][2])} {EURO}]"
            f"({RAPPORTS}/{mois}.md) | {fr(100 * valeurs[borne][2] / args.dotation)} "
            f"| {fr(ref100[borne])} | {signe(alpha_mois)} pt "
            f"| {signe(100 * valeurs[borne][2] / args.dotation - ref100[borne])} pt "
            f"| {nombre or '—'} |")

    lignes = positions_de_lannee(ordres, series, reference, fin)
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
    gagnantes = sum(1 for ligne in lignes if ligne["euros"] > 0)
    out += [
        "",
        (f"**{gagnantes} positions sur {len(lignes)}** finissent en gain net de "
         f"frais. La contribution la plus forte est "
         f"{signe(max(ligne['euros'] for ligne in lignes))} {EURO}, la plus faible "
         f"{signe(min(ligne['euros'] for ligne in lignes))} {EURO}."),
    ]

    tenu = janvier_tenu(ordres, series, args, fin)
    frais_janvier = sum(o["FRAIS"] for o in ordres if o["DATE"] == DEBUT)
    out += [
        "",
        "## 4. Ce que la rotation a coûté",
        "",
        (f"Les {len(ordres)} ordres ont prélevé **{fr(frais)} {EURO}**, soit "
         f"{fr(100 * frais / args.dotation)} % de la dotation — dont "
         f"{fr(frais_janvier)} {EURO} pour la seule constitution du portefeuille "
         "en janvier, incompressible."),
        "",
        ("Reste le contrefactuel qui isole l'apport des ordres suivants : **garder "
         "le portefeuille de janvier jusqu'au bout**, sans un seul arbitrage."),
        "",
        "| | Valeur au " + fin + " | Base 100 | Écart |",
        "|---|---|---|---|",
        (f"| Le portefeuille de l'expérience | {fr(total)} {EURO} | {fr(base)} | — |"),
        (f"| Janvier tenu toute l'année | {fr(tenu)} {EURO} "
         f"| {fr(100 * tenu / args.dotation)} "
         f"| **{signe(100 * (total - tenu) / args.dotation)} pt** |"),
        "",
        ("Ce nombre est le prix net des vingt-deux ordres passés après janvier, "
         "frais et arbitrages confondus. Il ne dit pas que la rotation est mauvaise "
         "en général : il dit ce qu'elle a rendu sur ces douze mois-là."),
        "",
        "## 5. Les trois conventions",
        "",
        ("> ⚠️ Le point le plus important du bilan. `Close` est **ajustée des "
         f"dividendes**, `{REFERENCE_NUE}` ne l'est pas. Comparer les deux fabrique "
         "de l'alpha à partir de rien."),
        "",
        "| Série | Convention | 2022 | Alpha du portefeuille |",
        "|---|---|---|---|",
        (f"| Le portefeuille | rendement total | **{signe(base - 100)} %** | — |"),
        (f"| `{REFERENCE}` | rendement total | {signe(ref100[fin] - 100)} % "
         f"| **{signe(base - ref100[fin])} pt** |"),
        (f"| `{REFERENCE_NUE}` | indice **nu** | {signe(nue)} % "
         f"| {signe(base - 100 - nue)} pt |"),
        "",
        (f"Le même portefeuille est en retard de {fr(abs(base - ref100[fin]))} point "
         f"contre `{REFERENCE}` et en avance de "
         f"{fr(abs(base - 100 - nue))} point contre `{REFERENCE_NUE}`. "
         f"**Le choix de la référence renverse le signe du verdict** : c'est "
         "pourquoi il devait être déclaré avant, et non choisi après."),
        "",
        "## 6. Ce que l'expérience établit, et ce qu'elle n'établit pas",
        "",
        "**Elle établit** :",
        "",
        ("- que cette règle-là, sur cet univers-là, en 2022, a rendu "
         f"{signe(base - ref100[fin])} point contre sa référence ;"),
        ("- que les frais d'exécution, souvent négligés, pèsent "
         f"{fr(100 * frais / args.dotation)} point sur une seule année à cette "
         "cadence ;"),
        ("- que le choix de la convention d'indice déplace le résultat de "
         f"{fr(abs(ref100[fin] - 100 - nue))} points, davantage que l'écart mesuré "
         "lui-même."),
        "",
        "**Elle n'établit pas** :",
        "",
        ("- que la règle est mauvaise. Un an est **un point**. Le cours de finance "
         "montre qu'il faudrait des siècles pour distinguer un rendement moyen de "
         "zéro ; douze mois ne distinguent rien du tout ;"),
        ("- qu'une autre cadence, un autre univers ou d'autres seuils feraient "
         "mieux. Les essayer maintenant, en connaissant 2022, ne produirait qu'un "
         "ajustement rétrospectif ;"),
        ("- quoi que ce soit sur 2023. Aucune quantité mesurée ici ne se prolonge."),
        "",
        ("Ce qui reste acquis est de nature différente : le protocole a été **écrit "
         "avant**, il n'a pas bougé, et le résultat est publié tel qu'il est sorti. "
         "C'est la seule chose qu'une expérience sur une année passée puisse "
         "honnêtement offrir."),
        "",
        "---",
        "",
        (f"[← Protocole](README.md) · [Décembre]({RAPPORTS}/2022-12.md) · "
         f"[Janvier]({RAPPORTS}/2022-01.md)"),
    ]
    return NL_.join(out) + NL_


def analyser_arguments():
    parser = argparse.ArgumentParser(
        description="Journal de l'experience 1 : un portefeuille de 10 000 EUR sur 2022.")
    ici = Path(__file__).resolve().parent
    parser.add_argument("--collecter", action="store_true", help="Relancer la collecte")
    parser.add_argument("--repertoire", type=Path, default=ici, help="Ou lire et ecrire")
    parser.add_argument("--quotes", type=Path, default=QUOTES_DEFAUT, help="Ou sont les series")
    parser.add_argument("--dotation", type=float, default=10000.0, help="Dotation en euros")
    parser.add_argument("--lignes", type=int, default=5, help="Lignes detenues au maximum")
    parser.add_argument("--rang-entree", type=int, default=5, help="Rang d'achat")
    parser.add_argument("--rang-sortie", type=int, default=7, help="Rang de vente")
    parser.add_argument("--mois", help="N'afficher que ce mois (AAAA-MM)")
    parser.add_argument("--markdown", action="store_true",
                        help="Ecrire aussi les douze journaux mensuels")
    args = parser.parse_args()
    if args.rang_sortie < args.rang_entree:
        erreur("--rang-sortie doit etre superieur ou egal a --rang-entree (hysteresis)")
    if args.dotation <= 0:
        erreur("--dotation doit etre strictement positive")
    if not 1 <= args.lignes <= len(UNIVERS):
        erreur(f"--lignes doit etre entre 1 et {len(UNIVERS)}")
    return args


def main():
    args = analyser_arguments()
    if not args.quotes.is_dir():
        erreur(f"Repertoire introuvable : {args.quotes}")

    series = {t: charger_serie(nom_fichier(t, args.quotes)) for t in UNIVERS}
    reference = charger_serie(nom_fichier(REFERENCE, args.quotes))
    nue = charger_serie(nom_fichier(REFERENCE_NUE, args.quotes))
    couples = calendrier(sorted(reference))
    if len(couples) != 12:
        erreur(f"Calendrier incomplet : {len(couples)} mois au lieu de 12")

    if args.collecter:
        print("Collecte des criteres par python/generer_graph_decision.py")
        collecter(couples, args.quotes, args.repertoire, series)

    chemin_criteres = args.repertoire / "criteres.csv"
    if not chemin_criteres.exists():
        erreur(f"{chemin_criteres} absent : relancer avec --collecter")
    with chemin_criteres.open(encoding="utf-8") as flux:
        criteres = list(csv.DictReader(flux))

    seances = [d for d in sorted(reference) if DEBUT <= d <= FIN]
    ref100 = {j: 100 * reference[j]["close"] / reference[DEBUT]["close"] for j in seances}

    positions, especes = {}, args.dotation
    classements, ordres_tous, valeurs, historique = [], [], {}, []

    for i, (date_decision, date_exec) in enumerate(couples):
        classement = classer(criteres, date_decision)
        classements.extend(classement)

        # etat herite, mesure a la cloture de la date de decision ; la base du
        # mois est la derniere seance du mois qui PRECEDE cette date
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
        achats = acheter(positions, classement, date_exec, series, especes, args)
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

        historique.append((mois, date_decision, date_exec, classement, ordres,
                           etat_avant, dict(positions)))

    ecrire_csv(args.repertoire / "classement.csv", ENTETE_CLASSEMENT, classements)
    ecrire_csv(args.repertoire / "ordres.csv", ENTETE_ORDRES, ordres_tous)
    ecrire_csv(args.repertoire / "portefeuille.csv", ENTETE_PORTEFEUILLE, [
        {"DATE": j, "ESPECES": round(valeurs[j][0], 2), "TITRES": round(valeurs[j][1], 2),
         "TOTAL": round(valeurs[j][2], 2),
         "BASE100": round(100 * valeurs[j][2] / args.dotation, 4),
         "REFERENCE100": round(ref100[j], 4)} for j in seances])

    actualites, notes = charger_textes(args.repertoire) if args.markdown else ({}, {})
    executions = [h[2] for h in historique]

    for mois, date_decision, date_exec, classement, ordres, etat_avant, tenues \
            in historique:
        fin_mois = derniere_seance(seances, mois)
        jours = [j for j in seances if j <= fin_mois]
        courbe = [100 * valeurs[j][2] / args.dotation for j in jours]
        svg(args.repertoire / "graphiques" / f"portefeuille-{mois}.svg",
            jours, courbe, [ref100[j] for j in jours], executions)

        veille = derniere_seance(seances, mois_precedent(mois))
        base_p = valeurs[veille][2] if veille else args.dotation
        base_r = ref100[veille] if veille else 100.0
        etat_apres = {
            "base": courbe[-1], "reference": ref100[fin_mois],
            "alpha_mois": 100 * (valeurs[fin_mois][2] / base_p - ref100[fin_mois] / base_r),
            "alpha_global": courbe[-1] - ref100[fin_mois],
        }
        if args.markdown:
            apports = []
            for ticker, info in tenues.items():
                debut_mois = (veille if veille and info["date"] <= veille
                              else info["date"])
                base_prix = (series[ticker][veille]["close"]
                             if veille and info["date"] <= veille else info["prix"])
                apports.append({
                    "ticker": ticker,
                    "euros": info["quantite"] * (series[ticker][fin_mois]["close"]
                                                 - base_prix),
                })
                del debut_mois
            precedent_mois = mois_precedent(mois)
            suivant_mois = f"{mois[:4]}-{int(mois[5:7]) + 1:02d}"
            navigation = []
            if precedent_mois >= "2022-01":
                navigation.append(f"[← {MOIS_TITRE[precedent_mois[5:7]]}]"
                                  f"({precedent_mois}.md)")
            navigation.append("[Protocole](../README.md)")
            if suivant_mois <= "2022-12":
                navigation.append(f"[{MOIS_TITRE[suivant_mois[5:7]]} →]"
                                  f"({suivant_mois}.md)")
            contexte = {
                "date_decision": date_decision, "date_exec": date_exec,
                "fin_mois": fin_mois, "dotation": args.dotation,
                "especes": valeurs[fin_mois][0], "titres": valeurs[fin_mois][1],
                "total": valeurs[fin_mois][2], "base": etat_apres["base"],
                "reference": etat_apres["reference"],
                "alpha_mois": etat_apres["alpha_mois"],
                "alpha_global": etat_apres["alpha_global"],
                "actualites": actualites.get(mois, ""),
                "notes": notes.get(date_decision, {}),
                "etat_avant": etat_avant, "classement": classement, "ordres": ordres,
                "lecture": lecture_du_mois(apports, ordres, etat_apres["alpha_mois"]),
                "navigation": " · ".join(navigation),
                "dernier": mois == FIN[:7],
            }
            chemin = args.repertoire / RAPPORTS / f"{mois}.md"
            chemin.parent.mkdir(parents=True, exist_ok=True)
            chemin.write_text(journal_mensuel(mois, contexte), encoding="utf-8")

        if args.mois and args.mois != mois:
            continue
        print(bloc_mensuel(mois, date_decision, date_exec, classement, ordres,
                           etat_avant, etat_apres, valeurs, seances))

    fin = seances[-1]
    if args.markdown:
        variation_nue = 100 * (nue[fin]["close"] / nue[DEBUT]["close"] - 1)
        (args.repertoire / BILAN).write_text(
            bilan_annuel(args, valeurs, ref100, ordres_tous, seances, series,
                         reference, variation_nue),
            encoding="utf-8")
    frais_total = sum(o["FRAIS"] for o in ordres_tous)
    achats = sum(1 for o in ordres_tous if o["SENS"] == "ACHAT")
    print(f"""
=== Bilan au {fin} ===

  Dotation                {fr(args.dotation)} EUR au {DEBUT}
  Valeur finale           {fr(valeurs[fin][2])} EUR
  Performance             {signe(100 * valeurs[fin][2] / args.dotation - 100)} %
  {REFERENCE}                    {signe(ref100[fin] - 100)} %
  Alpha sur l'annee       {signe(100 * valeurs[fin][2] / args.dotation - ref100[fin])} pt

  Ordres                  {len(ordres_tous)} ({achats} achats, \
{len(ordres_tous) - achats} ventes)
  Frais cumules           {fr(frais_total)} EUR, soit \
{fr(100 * frais_total / args.dotation)} % de la dotation
  Especes au {fin}   {fr(valeurs[fin][0])} EUR
""")
    ecrits = ["classement.csv", "ordres.csv", "portefeuille.csv",
              f"graphiques/portefeuille-2022-MM.svg ({len(historique)} mois)"]
    if args.markdown:
        ecrits += [f"{RAPPORTS}/2022-MM.md ({len(historique)} rapports)", BILAN]
    print("Ecrits : " + ", ".join(ecrits))


if __name__ == "__main__":
    main()
