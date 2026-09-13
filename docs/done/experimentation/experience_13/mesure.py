#!/usr/bin/env python3
"""La droite apporte-t-elle ce que son absence n'apporte pas ?

Quatre bras sur le CAC 40 point-in-time 2010-2018 : R (regression), T1 (sans
droite), T2 (marche aleatoire), T0 (dates au hasard). Aucun portefeuille, aucun
ordre : le moteur produit des evenements dates et leur issue a 60 seances.

Le miroir d'execution est dans mesure.md, et il fait autorite. Le protocole est
dans README.md, et c'est lui qui fixe la regle.

Utilisation :
    python docs/done/experimentation/experience_13/mesure.py --dimensionner
    python docs/done/experimentation/experience_13/mesure.py
"""

import argparse
import csv
import glob
import math
import random
import statistics
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
QUOTES = Path("docs/raw/data/quotes")
CALENDRIER = "MC.PA"

FENETRE, PROJECTION, HORIZON, RECUL = 250, 250, 60, 20
SEUILS = (2.0, 2.5, 3.0)
K_DECISION = 3.0
TIRAGES, GRAINE = 3000, 2010
FIN_MESURE = "2018-12-31"
PANIER_MIN = 10
SAUT_SCISSION = 0.50

# Mesures de couts_transaction.py, anachroniques et non decisives : voir mesure.md.
COUT_AR = {"FR": 0.00544, "autre": 0.00246}

BRAS = ("R", "T1", "T2")
SENS = (("bas", -1), ("haut", 1))

# Seuils du critere de decision, recopies du README.
SEUIL_EXCES, SEUIL_ROBUSTE = 1.00, 0.50
# Seuil du controle de validite T0, applique a la p AJUSTEE par Holm.
SEUIL_VALIDITE = 0.05

# Les figures. Meme dialecte que les journal.py des autres experiences.
GRAPHIQUES = "graphiques"
MARGE_G = 56
TEINTES_BRAS = {"R": "#1f5f8b", "T1": "#2e7d32", "T2": "#b35c1e"}


def erreur(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def fr(x, decimales=2):
    if x is None:
        return "—"
    return f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")


def signe(x, decimales=2):
    return "—" if x is None else ("+" if x >= 0 else "") + fr(x, decimales)


def ent(texte):
    """Echappe le XML, puis rend tout non-ASCII en entite numerique."""
    texte = texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in texte)


def pas_lisible(amplitude, cibles=8):
    """Un pas de graduation rond, proche de amplitude / cibles."""
    brut = max(amplitude / cibles, 1e-12)
    puissance = 10 ** math.floor(math.log10(brut))
    for multiple in (1, 2, 2.5, 5, 10):
        if multiple * puissance >= brut:
            return multiple * puissance
    return 10 * puissance


# --------------------------------------------------------------------------
# Les donnees


def charger_univers():
    """Rend (ancrages, composition par ancrage, nombre de couples ecartes)."""
    chemin = RACINE / "univers.csv"
    if not chemin.exists():
        erreur(f"Univers introuvable : {chemin}")
    with chemin.open(encoding="utf-8", newline="") as flux:
        lignes = list(csv.DictReader(flux))
    compo, ecartes = {}, 0
    for ligne in lignes:
        if ligne["RETENUE"] != "oui":
            ecartes += 1
            continue
        if not ligne["TICKER"]:
            erreur(f"{ligne['ISIN']} retenue sans ticker : univers incoherent.")
        compo.setdefault(ligne["DATE_ANCRAGE"], []).append((ligne["ISIN"], ligne["TICKER"]))
    return sorted(compo), compo, ecartes


def charger_serie(ticker):
    """Rend (jours, closes, index) pour un ticker, borne a FIN_MESURE."""
    motif = str(QUOTES / f"{ticker.replace('.', '_')}_2009-*.csv")
    fichiers = glob.glob(motif)
    if len(fichiers) != 1:
        erreur(f"{ticker} : {len(fichiers)} fichier(s) pour le motif {motif}, il en faut 1.")
    jours, closes, divisions = [], [], []
    with open(fichiers[0], encoding="utf-8", newline="") as flux:
        for ligne in csv.DictReader(flux):
            jour = ligne["Date"][:10]
            if jour > FIN_MESURE or not ligne["Close"]:
                continue
            jours.append(jour)
            closes.append(float(ligne["Close"]))
            divisions.append(float(ligne.get("Stock Splits") or 0.0))
    for i in range(1, len(closes)):
        variation = closes[i] / closes[i - 1] - 1
        if abs(variation) > SAUT_SCISSION and not divisions[i]:
            erreur(f"{ticker} au {jours[i]} : saut de {100 * variation:+.1f} % sans division "
                   "declaree — operation sur titre presumee, serie irrecevable.", code=2)
    return jours, closes, {j: i for i, j in enumerate(jours)}


# --------------------------------------------------------------------------
# Les trois bras


def ajuster(closes, fin, n):
    """Les grandeurs des trois bras sur les n clotures finissant au rang `fin`."""
    vals = closes[fin - n + 1:fin + 1]
    moyenne_t = (n + 1) / 2
    moyenne_v = statistics.fmean(vals)
    var_t = (n * n - 1) / 12
    var_v = sum((v - moyenne_v) ** 2 for v in vals) / n
    if var_v <= 0:
        return None
    cov = sum((t - moyenne_t) * (v - moyenne_v)
              for t, v in enumerate(vals, start=1)) / n
    pente = cov / var_t
    sce = sum((v - (moyenne_v + pente * (t - moyenne_t))) ** 2
              for t, v in enumerate(vals, start=1))
    if sce <= 0:
        return None
    rendements = [vals[i] / vals[i - 1] - 1 for i in range(1, n)]
    sigma_jour = statistics.stdev(rendements)
    if sigma_jour <= 0:
        return None
    return {"val": moyenne_v + pente * (n - moyenne_t), "pente": pente,
            "s": math.sqrt(sce / (n - 2)), "moy": moyenne_v,
            "sd": math.sqrt(var_v), "sigma": sigma_jour}


def ecarts_reduits(ajustement, prix, prix_recul, j):
    """Les trois z du bras R, T1 et T2 a la seance d + j. None si incalculable."""
    a = ajustement
    z_r = (prix - a["val"] - a["pente"] * j) / a["s"]
    z_t1 = (prix - a["moy"]) / a["sd"]
    z_t2 = None
    if prix_recul is not None:
        z_t2 = (prix - prix_recul) / (prix_recul * a["sigma"] * math.sqrt(RECUL))
    return {"R": z_r, "T1": z_t1, "T2": z_t2}


# --------------------------------------------------------------------------
# Les evenements et leur issue


def detecter(cal, compo, series):
    """Le premier franchissement de chaque (ancrage, valeur, bras, k, sens).

    Rend (evenements, compteurs). Un evenement n'est retenu que si HORIZON
    seances le suivent sans depasser FIN_MESURE.
    """
    index_cal = {j: i for i, j in enumerate(cal)}
    dernier = len(cal) - 1
    trouves, compte = [], {"couples": 0, "sans_fenetre": 0, "hors_horizon": 0}
    for ancrage in sorted(compo):
        i_ancrage = index_cal[ancrage]
        for isin, ticker in compo[ancrage]:
            _, closes, index = series[ticker]
            if ancrage not in index or index[ancrage] + 1 < FENETRE:
                compte["sans_fenetre"] += 1
                continue
            compte["couples"] += 1
            a = ajuster(closes, index[ancrage], FENETRE)
            if a is None:
                compte["sans_fenetre"] += 1
                continue
            vus = set()
            for j in range(1, PROJECTION + 1):
                if i_ancrage + j > dernier:
                    break
                date = cal[i_ancrage + j]
                if date not in index:
                    continue
                prix = closes[index[date]]
                recul = cal[i_ancrage + j - RECUL] if i_ancrage + j - RECUL >= 0 else None
                prix_recul = closes[index[recul]] if recul in index else None
                z = ecarts_reduits(a, prix, prix_recul, j)
                for bras in BRAS:
                    if z[bras] is None:
                        continue
                    for nom_sens, orientation in SENS:
                        for k in SEUILS:
                            cle = (bras, nom_sens, k)
                            if cle in vus:
                                continue
                            if orientation * z[bras] <= k:
                                continue
                            vus.add(cle)
                            if i_ancrage + j + HORIZON > dernier:
                                compte["hors_horizon"] += 1
                                continue
                            trouves.append({
                                "ancrage": ancrage, "isin": isin, "ticker": ticker,
                                "bras": bras, "sens": nom_sens, "k": k,
                                "date": date, "j": j, "z": z[bras],
                                "i_cal": i_ancrage + j})
                if len(vus) == len(BRAS) * len(SENS) * len(SEUILS):
                    break
    return trouves, compte


def rendement(series, ticker, cal, debut, fin):
    """Le rendement d'une valeur entre deux rangs de calendrier, ou None."""
    _, closes, index = series[ticker]
    a, b = cal[debut], cal[fin]
    if a not in index or b not in index:
        return None
    return closes[index[b]] / closes[index[a]] - 1


def panier(series, compo, cal, ancrage, debut, fin, cache):
    """Somme et effectif du panier equipondere de l'ancrage, entre deux rangs."""
    cle = (ancrage, debut)
    if cle not in cache:
        total, effectif, parts = 0.0, 0, {}
        for _, ticker in compo[ancrage]:
            r = rendement(series, ticker, cal, debut, fin)
            if r is None:
                continue
            parts[ticker] = r
            total += r
            effectif += 1
        cache[cle] = (total, effectif, parts)
    return cache[cle]


def cout(isin):
    return COUT_AR["FR"] if isin.startswith("FR") else COUT_AR["autre"]


def issues(evenements, series, compo, cal):
    """Ajoute a chaque evenement son exces brut, son exces net et la taille du panier."""
    cache, gardes, ecartes = {}, [], 0
    for e in evenements:
        debut, fin = e["i_cal"], e["i_cal"] + HORIZON
        propre = rendement(series, e["ticker"], cal, debut, fin)
        if propre is None:
            ecartes += 1
            continue
        total, effectif, parts = panier(series, compo, cal, e["ancrage"], debut, fin, cache)
        if e["ticker"] in parts:
            total -= parts[e["ticker"]]
            effectif -= 1
        if effectif < PANIER_MIN:
            ecartes += 1
            continue
        e["exces"] = 100 * (propre - total / effectif)
        e["exces_net"] = e["exces"] - 100 * cout(e["isin"])
        e["panier"] = effectif
        gardes.append(e)
    return gardes, ecartes


def temoin_nul(evenements, series, compo, cal, alea):
    """Le bras T0 : meme nombre d'evenements que R, aux dates tirees au hasard."""
    pool = []
    index_cal = {j: i for i, j in enumerate(cal)}
    for ancrage in sorted(compo):
        base = index_cal[ancrage]
        for isin, ticker in compo[ancrage]:
            for j in range(1, PROJECTION + 1):
                if base + j + HORIZON > len(cal) - 1:
                    break
                pool.append((ancrage, isin, ticker, base + j))
    resultats = {}
    cache = {}
    for nom_sens, _ in SENS:
        for k in SEUILS:
            combien = sum(1 for e in evenements
                          if e["bras"] == "R" and e["sens"] == nom_sens and e["k"] == k)
            tires, faits = [], 0
            for ancrage, isin, ticker, i_cal in alea.sample(pool, min(combien * 3, len(pool))):
                if faits >= combien:
                    break
                propre = rendement(series, ticker, cal, i_cal, i_cal + HORIZON)
                if propre is None:
                    continue
                total, effectif, parts = panier(series, compo, cal, ancrage,
                                                i_cal, i_cal + HORIZON, cache)
                if ticker in parts:
                    total -= parts[ticker]
                    effectif -= 1
                if effectif < PANIER_MIN:
                    continue
                tires.append({"date": cal[i_cal], "isin": isin,
                              "exces": 100 * (propre - total / effectif)})
                faits += 1
            resultats[(nom_sens, k)] = tires
    return resultats


# --------------------------------------------------------------------------
# L'agregation par grappes de mois


def par_mois(evenements):
    """Somme et effectif des exces, par mois calendaire.

    On agrege des le depart plutot que de garder les listes : un tirage du
    bootstrap redevient alors O(nombre de mois) au lieu de O(nombre
    d'evenements), pour une moyenne rigoureusement identique.
    """
    groupes = {}
    for e in evenements:
        somme, effectif = groupes.get(e["date"][:7], (0.0, 0))
        groupes[e["date"][:7]] = (somme + e["exces"], effectif + 1)
    return groupes


def moyenne(groupes, mois):
    """Moyenne des exces sur une liste de mois, en mettant tout en commun."""
    somme = 0.0
    effectif = 0
    for m in mois:
        s, n = groupes.get(m, (0.0, 0))
        somme += s
        effectif += n
    return somme / effectif if effectif else None


def bootstrap(groupes, alea, tirages=TIRAGES):
    """Rend (moyenne, borne basse, borne haute, p bilaterale) par grappes de mois."""
    mois = sorted(groupes)
    if not mois:
        return None, None, None, None
    observee = moyenne(groupes, mois)
    tires = []
    for _ in range(tirages):
        echantillon = [alea.choice(mois) for _ in mois]
        m = moyenne(groupes, echantillon)
        if m is not None:
            tires.append(m)
    tires.sort()
    if not tires:
        return observee, None, None, None
    bas = tires[int(0.025 * (len(tires) - 1))]
    haut = tires[int(0.975 * (len(tires) - 1))]
    sous = sum(1 for t in tires if t <= 0) / len(tires)
    p = min(1.0, 2 * min(sous, 1 - sous))
    return observee, bas, haut, p


def bootstrap_apparie(groupes_r, groupes_t1, groupes_t2, alea, tirages=TIRAGES):
    """L'ecart R - max(T1, T2), reechantillonne sur LES MEMES mois."""
    mois = sorted(set(groupes_r) | set(groupes_t1) | set(groupes_t2))
    if not mois:
        return None, None, None, None

    def ecart(echantillon):
        r = moyenne(groupes_r, echantillon)
        t1 = moyenne(groupes_t1, echantillon)
        t2 = moyenne(groupes_t2, echantillon)
        temoins = [t for t in (t1, t2) if t is not None]
        if r is None or not temoins:
            return None
        return r - max(temoins)

    observee = ecart(mois)
    tires = [e for e in (ecart([alea.choice(mois) for _ in mois]) for _ in range(tirages))
             if e is not None]
    tires.sort()
    if not tires:
        return observee, None, None, None
    bas = tires[int(0.025 * (len(tires) - 1))]
    haut = tires[int(0.975 * (len(tires) - 1))]
    sous = sum(1 for t in tires if t <= 0) / len(tires)
    return observee, bas, haut, min(1.0, 2 * min(sous, 1 - sous))


def holm(pvaleurs):
    """Correction de Holm. Rend {cle: p ajustee}."""
    valides = sorted((p, c) for c, p in pvaleurs.items() if p is not None)
    ajustees, precedent = {}, 0.0
    for rang, (p, cle) in enumerate(valides):
        ajustee = min(1.0, max(precedent, (len(valides) - rang) * p))
        ajustees[cle] = ajustee
        precedent = ajustee
    for cle, p in pvaleurs.items():
        if p is None:
            ajustees[cle] = None
    return ajustees


def par_annee(evenements):
    """Les exces regroupes par annee, pour le controle de robustesse."""
    groupes = {}
    for e in evenements:
        groupes.setdefault(e["date"][:4], []).append(e)
    return groupes


# --------------------------------------------------------------------------
# Les sorties


def imprimer_cellules(evenements, ajustees, resume):
    print(f"\n{'bras':>4} {'sens':>5} {'k':>4} {'evts':>6} {'mois':>5} "
          f"{'exces':>9} {'IC95':>22} {'p':>8} {'p Holm':>8}")
    print("-" * 82)
    for bras in BRAS:
        for nom_sens, _ in SENS:
            for k in SEUILS:
                cle = (bras, nom_sens, k)
                m, bas, haut, p = resume[cle]
                n = sum(1 for e in evenements
                        if (e["bras"], e["sens"], e["k"]) == cle)
                mois = len({e["date"][:7] for e in evenements
                            if (e["bras"], e["sens"], e["k"]) == cle})
                ic = f"[{signe(bas)} ; {signe(haut)}]" if bas is not None else "—"
                print(f"{bras:>4} {nom_sens:>5} {fr(k, 1):>4} {n:>6} {mois:>5} "
                      f"{signe(m):>9} {ic:>22} {fr(p, 4) if p is not None else '—':>8} "
                      f"{fr(ajustees[cle], 4) if ajustees[cle] is not None else '—':>8}")


def entete_svg(largeur, hauteur, titre, sous_titre):
    """L'en-tete commun aux figures, dans le style des journal.py des experiences."""
    return [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" '
         f'font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{largeur}" height="{hauteur}" fill="#ffffff"/>',
        (f'<text x="{MARGE_G}" y="26" font-size="15" font-weight="600" fill="#1a1a1a">'
         f'{ent(titre)}</text>'),
        f'<text x="{MARGE_G}" y="46" font-size="11" fill="#666666">{ent(sous_titre)}</text>',
    ]


def ecrire_svg(chemin, out):
    """Ferme et ecrit. write_text rend du CRLF sous Windows : voir .gitattributes."""
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Graphique ecrit dans : {chemin}")


def svg_cellules(chemin, resume, ajustees, principal):
    """Le graphe en foret : un intervalle par cellule, et le test principal."""
    largeur, hauteur = 920, 580
    marge_h, marge_b, aire_g, aire_d = 74, 54, 168, 86
    aire_l = largeur - aire_g - aire_d
    lignes = [(bras, sens, k) for bras in BRAS for sens, _ in SENS for k in SEUILS]
    bornes = [v for cle in lignes for v in resume[cle][1:3] if v is not None]
    bornes += [v for v in principal[1:3] if v is not None]
    bas, haut = min(*bornes, 0.0), max(*bornes, 0.0)
    coussin = (haut - bas) * 0.10 or 1.0
    bas, haut = bas - coussin, haut + coussin
    pas_ligne = (hauteur - marge_h - marge_b) / (len(lignes) + 2)

    def x(v):
        return aire_g + aire_l * (v - bas) / (haut - bas)

    def y(rang):
        return marge_h + pas_ligne * (rang + 0.5)

    out = entete_svg(largeur, hauteur,
                     "Expérience 13 — les 18 cellules et leur intervalle à 95 %",
                     f"excès à {HORIZON} séances contre panier apparié · bootstrap par "
                     f"grappes de mois · aucune cellule n'exclut zéro après Holm")
    pas = pas_lisible(haut - bas)
    niveau = math.ceil(bas / pas) * pas
    while niveau <= haut:
        zero = abs(niveau) < 1e-9
        out.append(f'<line x1="{x(niveau):.1f}" y1="{marge_h}" x2="{x(niveau):.1f}" '
                   f'y2="{hauteur - marge_b:.1f}" stroke="{"#9e9e9e" if zero else "#ececec"}" '
                   f'stroke-width="{1.6 if zero else 1}"/>')
        out.append(f'<text x="{x(niveau):.1f}" y="{hauteur - marge_b + 16:.1f}" '
                   f'font-size="10.5" fill="#666666" text-anchor="middle">'
                   f'{ent(signe(niveau, 0))}</text>')
        niveau += pas

    for rang, cle in enumerate(lignes):
        bras, sens, k = cle
        moyenne, borne_b, borne_h, _ = resume[cle]
        teinte = TEINTES_BRAS[bras]
        decision = cle == ("R", "bas", K_DECISION)
        epaisseur = 3.0 if decision else 1.8
        if borne_b is not None:
            out.append(f'<line x1="{x(borne_b):.1f}" y1="{y(rang):.1f}" '
                       f'x2="{x(borne_h):.1f}" y2="{y(rang):.1f}" stroke="{teinte}" '
                       f'stroke-width="{epaisseur}" stroke-linecap="round"/>')
        if moyenne is not None:
            out.append(f'<circle cx="{x(moyenne):.1f}" cy="{y(rang):.1f}" '
                       f'r="{4.6 if decision else 3.4}" fill="{teinte}"/>')
        poids = ' font-weight="600"' if decision else ""
        out.append(f'<text x="{aire_g - 10}" y="{y(rang) + 4:.1f}" font-size="11" '
                   f'fill="#444444" text-anchor="end"{poids}>'
                   f'{ent(f"{bras}  {sens}  k = {fr(k, 1)}")}</text>')
        ajustee = ajustees[cle]
        out.append(f'<text x="{largeur - aire_d + 8}" y="{y(rang) + 4:.1f}" font-size="10.5" '
                   f'fill="#888888">'
                   f'{ent("p " + (fr(ajustee, 3) if ajustee is not None else "—"))}</text>')

    filet = marge_h + pas_ligne * (len(lignes) + 0.4)
    out.append(f'<line x1="{aire_g - 150}" y1="{filet:.1f}" x2="{largeur - aire_d + 60}" '
               f'y2="{filet:.1f}" stroke="#cccccc" stroke-width="1"/>')
    rang = len(lignes) + 0.9
    if principal[1] is not None:
        out.append(f'<line x1="{x(principal[1]):.1f}" y1="{y(rang):.1f}" '
                   f'x2="{x(principal[2]):.1f}" y2="{y(rang):.1f}" stroke="#7b1fa2" '
                   f'stroke-width="3.0" stroke-linecap="round"/>')
        out.append(f'<circle cx="{x(principal[0]):.1f}" cy="{y(rang):.1f}" r="4.6" '
                   f'fill="#7b1fa2"/>')
    out.append(f'<text x="{aire_g - 10}" y="{y(rang) + 4:.1f}" font-size="11" '
               f'fill="#7b1fa2" text-anchor="end" font-weight="600">'
               f'{ent("R − max(T1,T2)  [PRINCIPAL]")}</text>')
    out.append(f'<text x="{MARGE_G}" y="{hauteur - 14}" font-size="10.5" fill="#666666">'
               f'{ent("Excès moyen en points, et son intervalle à 95 % par grappes de mois. "
                      "La verticale grise est le zéro : un intervalle qui la franchit ne "
                      "conclut rien.")}</text>')
    ecrire_svg(chemin, out)


def svg_grappes(chemin, evenements):
    """Les evenements par mois : pourquoi l'unite independante est la grappe."""
    largeur, hauteur = 920, 420
    marge_h, marge_b, aire_g, aire_d = 74, 62, 56, 22
    aire_l, aire_h = largeur - aire_g - aire_d, hauteur - marge_h - marge_b
    series = (("R", "#1f5f8b"), ("T2", "#b35c1e"))
    comptes = {}
    for bras, _ in series:
        sel = [e for e in evenements
               if e["bras"] == bras and e["sens"] == "bas" and e["k"] == K_DECISION]
        compte = {}
        for e in sel:
            compte[e["date"][:7]] = compte.get(e["date"][:7], 0) + 1
        comptes[bras] = compte
    mois = sorted({m for c in comptes.values() for m in c})
    if not mois:
        return
    sommet = max(max(c.values(), default=0) for c in comptes.values())

    def x(i):
        return aire_g + aire_l * i / max(len(mois), 1)

    def y(v):
        return marge_h + aire_h * (1 - v / sommet)

    out = entete_svg(largeur, hauteur,
                     "Expérience 13 — les événements se groupent par mois",
                     f"bras R et T2, sens bas, k = {fr(K_DECISION, 1)} · "
                     f"{len(comptes['R'])} grappes pour R, {len(comptes['T2'])} pour T2 — "
                     f"c'est T2 qui borne la puissance du test principal")
    pas = max(1, int(pas_lisible(sommet, 5)))
    for niveau in range(0, sommet + 1, pas):
        out.append(f'<line x1="{aire_g}" y1="{y(niveau):.1f}" x2="{largeur - aire_d}" '
                   f'y2="{y(niveau):.1f}" stroke="#ececec" stroke-width="1"/>')
        out.append(f'<text x="{aire_g - 8}" y="{y(niveau) + 4:.1f}" font-size="10.5" '
                   f'fill="#666666" text-anchor="end">{niveau}</text>')
    largeur_mois = aire_l / max(len(mois), 1)
    for i, m in enumerate(mois):
        if m[5:7] == "01":
            out.append(f'<text x="{x(i):.1f}" y="{hauteur - marge_b + 18:.1f}" '
                       f'font-size="10.5" fill="#666666">{m[:4]}</text>')
        for rang, (bras, teinte) in enumerate(series):
            valeur = comptes[bras].get(m, 0)
            if not valeur:
                continue
            large = max(1.4, largeur_mois / 2 - 0.6)
            gauche = x(i) + rang * (large + 0.6)
            out.append(f'<rect x="{gauche:.1f}" y="{y(valeur):.1f}" width="{large:.1f}" '
                       f'height="{marge_h + aire_h - y(valeur):.1f}" fill="{teinte}"/>')
    for rang, (bras, teinte) in enumerate(series):
        gauche = aire_g + rang * 300
        out.append(f'<rect x="{gauche}" y="{hauteur - 30}" width="14" height="10" '
                   f'fill="{teinte}"/>')
        out.append(f'<text x="{gauche + 20}" y="{hauteur - 21}" font-size="10.5" '
                   f'fill="#444444">{ent(f"{bras}, bas, k = {fr(K_DECISION, 1)} — "
                                          f"{len(comptes[bras])} mois occupés")}</text>')
    ecrire_svg(chemin, out)


def ecrire_evenements(chemin, evenements):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline="") as flux:
        redacteur = csv.writer(flux)
        redacteur.writerow(["ANCRAGE", "ISIN", "TICKER", "BRAS", "K", "SENS",
                            "DATE_EVENEMENT", "J", "Z", "EXCES", "EXCES_NET",
                            "TAILLE_PANIER"])
        for e in sorted(evenements, key=lambda x: (x["bras"], x["sens"], x["k"],
                                                   x["date"], x["isin"])):
            redacteur.writerow([e["ancrage"], e["isin"], e["ticker"], e["bras"],
                                f"{e['k']:.1f}", e["sens"], e["date"], e["j"],
                                f"{e['z']:.4f}", f"{e['exces']:.4f}",
                                f"{e['exces_net']:.4f}", e["panier"]])
    print(f"\nEvenements ecrits dans : {chemin}")


# --------------------------------------------------------------------------


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="L'ecart reduit a une droite apporte-t-il ce que son absence n'apporte pas ?")
    parser.add_argument("--dimensionner", action="store_true",
                        help="compter les evenements et l'EMD, sans calculer d'issue")
    parser.add_argument("--sortie", type=Path, default=RACINE, help="repertoire de sortie")
    args = parser.parse_args()

    ancrages, compo, ecartes = charger_univers()
    tickers = sorted({t for valeurs in compo.values() for _, t in valeurs})
    series = {t: charger_serie(t) for t in tickers}
    cal = series[CALENDRIER][0]
    if cal[-1] > FIN_MESURE:
        erreur(f"Le calendrier depasse {FIN_MESURE}.")

    print(f"Experience 13 — {len(ancrages)} ancrages, du {ancrages[0]} au {ancrages[-1]}")
    print(f"  {len(tickers)} valeurs recevables, {ecartes} couples ecartes de l'univers")
    print(f"  calendrier {CALENDRIER} : {len(cal)} seances, du {cal[0]} au {cal[-1]}")

    evenements, compte = detecter(cal, compo, series)
    print(f"\n  couples (ancrage, valeur) exploites : {compte['couples']}")
    print(f"  ecartes faute de fenetre de {FENETRE} seances : {compte['sans_fenetre']}")
    print(f"  franchissements sans horizon de {HORIZON} seances : {compte['hors_horizon']}")

    if args.dimensionner:
        alea = random.Random(GRAINE)
        echantillon = temoin_nul(evenements, series, compo, cal, alea)
        toutes = [x["exces"] for tires in echantillon.values() for x in tires]
        sigma = statistics.stdev(toutes) if len(toutes) > 1 else None
        print(f"\nDispersion INCONDITIONNELLE de l'issue a {HORIZON} seances : "
              f"{fr(sigma)} points, sur {len(toutes)} tirages au hasard")
        print(f"\n{'bras':>4} {'sens':>5} {'k':>4} {'evts':>6} {'mois':>5} {'EMD +/-':>9}")
        print("-" * 40)
        for bras in BRAS:
            for nom_sens, _ in SENS:
                for k in SEUILS:
                    sel = [e for e in evenements
                           if (e["bras"], e["sens"], e["k"]) == (bras, nom_sens, k)]
                    mois = len({e["date"][:7] for e in sel})
                    emd = 1.96 * sigma / math.sqrt(mois) if sigma and mois else None
                    print(f"{bras:>4} {nom_sens:>5} {fr(k, 1):>4} {len(sel):>6} "
                          f"{mois:>5} {fr(emd):>9}")
        print("\nAucune issue d'evenement n'a ete calculee. Rien n'a ete ecrit.")
        return

    evenements, sans_issue = issues(evenements, series, compo, cal)
    print(f"  evenements sans issue calculable : {sans_issue}")
    print(f"  evenements retenus : {len(evenements)}")

    alea = random.Random(GRAINE)
    resume, pvaleurs = {}, {}
    for bras in BRAS:
        for nom_sens, _ in SENS:
            for k in SEUILS:
                cle = (bras, nom_sens, k)
                sel = [e for e in evenements if (e["bras"], e["sens"], e["k"]) == cle]
                resume[cle] = bootstrap(par_mois(sel), alea)
                pvaleurs[cle] = resume[cle][3]
    ajustees = holm(pvaleurs)
    imprimer_cellules(evenements, ajustees, resume)

    temoins = temoin_nul(evenements, series, compo, cal, random.Random(GRAINE))
    # Le controle de validite subit la MEME correction de multiplicite que les
    # cellules principales. Six intervalles a 95 % non corriges declenchent une
    # fausse alerte 26,5 % du temps : sans Holm, la vanne se ferme sur du bruit.
    resume_t0, p_t0 = {}, {}
    for nom_sens, _ in SENS:
        for k in SEUILS:
            cle = (nom_sens, k)
            resume_t0[cle] = bootstrap(par_mois(temoins[cle]), alea)
            p_t0[cle] = resume_t0[cle][3]
    ajustees_t0 = holm(p_t0)
    print(f"\n{'T0 sens':>8} {'k':>4} {'tires':>6} {'exces':>9} {'IC95':>22} "
          f"{'p':>8} {'p Holm':>8}")
    print("-" * 72)
    defectueux = []
    for nom_sens, _ in SENS:
        for k in SEUILS:
            cle = (nom_sens, k)
            m, bas, haut, p = resume_t0[cle]
            ajustee = ajustees_t0[cle]
            ic = f"[{signe(bas)} ; {signe(haut)}]" if bas is not None else "—"
            print(f"{nom_sens:>8} {fr(k, 1):>4} {len(temoins[cle]):>6} {signe(m):>9} "
                  f"{ic:>22} {fr(p, 4) if p is not None else '—':>8} "
                  f"{fr(ajustee, 4) if ajustee is not None else '—':>8}")
            if ajustee is not None and ajustee < SEUIL_VALIDITE:
                defectueux.append(cle)

    print(f"\n--- test principal : R − max(T1, T2), bras bas, k = {fr(K_DECISION, 1)} ---")
    groupes = {}
    for bras in BRAS:
        sel = [e for e in evenements
               if e["bras"] == bras and e["sens"] == "bas" and e["k"] == K_DECISION]
        groupes[bras] = par_mois(sel)
    principal = bootstrap_apparie(groupes["R"], groupes["T1"], groupes["T2"], alea)
    ic = f"[{signe(principal[1])} ; {signe(principal[2])}]" if principal[1] is not None else "—"
    print(f"  ecart {signe(principal[0])} points   IC95 {ic}   p {fr(principal[3], 4)}")

    if defectueux:
        print(f"\nDISPOSITIF DEFECTUEUX : le temoin T0 s'ecarte de zero sur {defectueux}.")
        print("Aucun verdict n'est publie.")
        ecrire_evenements(args.sortie / "evenements.csv", evenements)
        sys.exit(3)

    cle = ("R", "bas", K_DECISION)
    exces, bas, _, _ = resume[cle]
    annees = par_annee([e for e in evenements
                        if (e["bras"], e["sens"], e["k"]) == cle])
    sans_meilleure = None
    if annees:
        pires = {a: statistics.fmean([x["exces"] for x in v]) for a, v in annees.items()}
        meilleure = max(pires, key=lambda a: pires[a])
        reste = [e for a, v in annees.items() if a != meilleure for e in v]
        sans_meilleure = statistics.fmean([e["exces"] for e in reste]) if reste else None

    conditions = [
        (f"1. exces moyen ≥ +{fr(SEUIL_EXCES)} point",
         exces is not None and exces >= SEUIL_EXCES, signe(exces)),
        ("2. IC95 par grappes exclut zero",
         bas is not None and bas > 0, signe(bas)),
        ("3. R − max(T1,T2) > 0 et IC95 exclut zero  [PRINCIPAL]",
         principal[1] is not None and principal[1] > 0, signe(principal[0])),
        (f"4. retrait de la meilleure annee laisse ≥ +{fr(SEUIL_ROBUSTE)}",
         sans_meilleure is not None and sans_meilleure >= SEUIL_ROBUSTE,
         signe(sans_meilleure)),
    ]
    print("\n--- le critere de decision, recopie du README ---")
    for libelle, tenue, valeur in conditions:
        print(f"  [{'X' if tenue else ' '}] {libelle:<52} {valeur:>9}")
    verdict = "UTILE" if all(t for _, t, _ in conditions) else "INUTILE"
    print(f"\nVERDICT : l'ecart reduit a une droite est declare {verdict}.")

    ecrire_evenements(args.sortie / "evenements.csv", evenements)
    svg_cellules(args.sortie / GRAPHIQUES / "cellules.svg", resume, ajustees, principal)
    svg_grappes(args.sortie / GRAPHIQUES / "grappes.svg", evenements)


if __name__ == "__main__":
    main()
