"""Trace un cours sur trois ans et ses trois derniers encadrements, ancres a une date.

Deux bandes a l'ecart-type residuel — 250 et 120 seances — et une enveloppe des
residus sur 20 seances. Une seule largeur par fenetre : la derniere, celle qui se
termine a la date d'observation. Aucun bloc, aucun verdict.

Le miroir d'execution est dans generer_graph_canal.md, et il fait autorite.

Utilisation :
    python python/generer_graph_canal.py
    python python/generer_graph_canal.py --date 2025-12-31
    python python/generer_graph_canal.py --annees 5 --sortie docs/done/graphiques/canal.svg
"""

import argparse
import math
import statistics
import sys
from pathlib import Path

REPERTOIRE_QUOTES = Path("docs/raw/data/quotes")
REPERTOIRE_GRAPHS = Path("docs/raw/data/graphs")
CORR_FAIBLE = 0.20
LARGEUR, HAUTEUR = 1200, 620
MARGE_G, MARGE_D, MARGE_H, MARGE_B = 66, 88, 96, 74

COULEUR_COURS = "#2a78d6"
COULEURS_BANDES = ("#7a8ba6", "#1f5f8b")     # de la plus longue fenetre a la plus courte
COULEUR_ENVELOPPE = "#b35c1e"
NBSP = " "


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


def echapper(texte):
    return texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --------------------------------------------------------------------------
# Les donnees


def charger(chemin):
    """Rend les dates et les clotures, lignes sans Close ecartees."""
    import pandas  # noqa: PLC0415 - dependance lourde, chargee seulement si besoin

    donnees = pandas.read_csv(chemin)
    if "Close" not in donnees.columns or "Date" not in donnees.columns:
        erreur(f"{chemin} : colonnes « Date » et « Close » requises.")
    donnees = donnees[["Date", "Close"]].dropna(subset=["Close"])
    jours = [str(d)[:10] for d in donnees["Date"]]
    closes = [float(c) for c in donnees["Close"]]
    if not closes:
        erreur(f"{chemin} : aucune cloture exploitable.")
    return jours, closes


def csv_par_defaut():
    if not REPERTOIRE_QUOTES.is_dir():
        erreur(f"Repertoire introuvable : {REPERTOIRE_QUOTES}")
    fichiers = [f for f in REPERTOIRE_QUOTES.glob("*.csv") if not f.name.startswith("^")]
    if not fichiers:
        erreur(f"Aucun CSV de valeur dans {REPERTOIRE_QUOTES}/.")
    return max(fichiers, key=lambda f: f.stat().st_mtime)


def rang_observation(jours, date):
    """L'indice de la seance d'observation, en reculant si la date n'en est pas une."""
    if date is None:
        return len(jours) - 1, False
    if date < jours[0]:
        erreur(f"--date {date} precede la premiere seance du CSV ({jours[0]}).")
    for i in range(len(jours) - 1, -1, -1):
        if jours[i] <= date:
            return i, jours[i] != date
    erreur(f"--date {date} : aucune seance avant ou a cette date.")
    return None


# --------------------------------------------------------------------------
# Les trois encadrements


def variance_temps(n):
    return (n * n - 1) / 12


def regression(closes, fin, n):
    """Les six grandeurs de la fenetre n se terminant au rang `fin`, bande a 1 s."""
    vals = closes[fin - n + 1:fin + 1]
    moyenne_t = (n + 1) / 2
    moyenne_v = statistics.fmean(vals)
    var_t = variance_temps(n)
    var_v = sum((v - moyenne_v) ** 2 for v in vals) / n          # ddof = 0
    if var_v <= 0:
        erreur(f"Fenetre {n} : variance nulle, le cours est constant.", code=2)
    cov = sum((t - moyenne_t) * (v - moyenne_v)
              for t, v in enumerate(vals, start=1)) / n
    corr = cov / math.sqrt(var_t * var_v)
    if 1 - corr ** 2 <= 0:
        erreur(f"Fenetre {n} : correlation unitaire, ecart-type residuel nul.", code=2)
    pente = cov / var_t
    val = moyenne_v + pente * (n - moyenne_t)
    s = math.sqrt(n / (n - 2) * var_v * (1 - corr ** 2))
    return {"n": n, "E": moyenne_v, "VAR": var_v, "CORR": corr, "VAL": val,
            "pente": pente, "s": s, "debut": fin - n + 1, "fin": fin,
            "bas": val - s, "haut": val + s, "largeur": 2 * s}


def enveloppe(closes, fin, n):
    """La droite des moindres carres, ses deux demi-largeurs de residus et ses contacts."""
    vals = closes[fin - n + 1:fin + 1]
    moyenne_t = (n + 1) / 2
    moyenne_v = statistics.fmean(vals)
    cov = sum((t - moyenne_t) * (v - moyenne_v)
              for t, v in enumerate(vals, start=1)) / n
    pente = cov / variance_temps(n)
    residus = [v - (moyenne_v + pente * (t - moyenne_t))
               for t, v in enumerate(vals, start=1)]
    i_bas = min(range(n), key=lambda k: residus[k])
    i_haut = max(range(n), key=lambda k: residus[k])
    val = moyenne_v + pente * (n - moyenne_t)
    demi_bas, demi_haut = -residus[i_bas], residus[i_haut]
    return {"n": n, "E": moyenne_v, "VAL": val, "pente": pente,
            "demi_bas": demi_bas, "demi_haut": demi_haut,
            "bas": val - demi_bas, "haut": val + demi_haut,
            "largeur": demi_bas + demi_haut, "debut": fin - n + 1, "fin": fin,
            "contact_bas": fin - n + 1 + i_bas, "contact_haut": fin - n + 1 + i_haut}


def taux(pente, moyenne):
    """La pente en %/seance, sans dimension : comparable d'une fenetre a l'autre."""
    return 100 * pente / moyenne if moyenne else None


# --------------------------------------------------------------------------
# Le SVG


def pas_lisible(amplitude, cibles=8):
    brut = max(amplitude / cibles, 1e-12)
    puissance = 10 ** math.floor(math.log10(brut))
    for multiple in (1, 2, 2.5, 5, 10):
        if multiple * puissance >= brut:
            return multiple * puissance
    return 10 * puissance


def svg(chemin, titre, jours, closes, depart, depart_zoom, obs, bandes, env):
    """Assemble le fichier.

    `depart` est le premier rang de CONSTRUCTION : il fixe l'echelle verticale.
    `depart_zoom` est le premier rang AFFICHE. Le graphique est donc bati a
    l'identique sur la fenetre complete, PUIS tronque a gauche — l'echelle n'est
    jamais recalculee sur la portion visible, sans quoi ce serait un autre
    graphique et non une troncature.
    """
    construits = list(range(depart, obs + 1))
    visibles = list(range(depart_zoom, obs + 1))
    bornes = [b["bas"] for b in bandes] + [b["haut"] for b in bandes]
    bornes += [env["bas"], env["haut"]]
    valeurs = [closes[i] for i in construits]
    bas, haut = min(valeurs + bornes), max(valeurs + bornes)
    coussin = (haut - bas) * 0.07 or 1.0
    bas, haut = bas - coussin, haut + coussin
    aire_l = LARGEUR - MARGE_G - MARGE_D
    aire_h = HAUTEUR - MARGE_H - MARGE_B

    def x(i):
        return MARGE_G + aire_l * (i - depart_zoom) / max(obs - depart_zoom, 1)

    def y(v):
        return MARGE_H + aire_h * (haut - v) / (haut - bas)

    def droite(objet, cle):
        """Les deux extremites d'une ligne de l'objet, tracee sur sa seule fenetre.

        Bornee a gauche par la troncature : une droite qui commence avant le cadre
        y entre par le bord, elle n'est pas prolongee au-dela.
        """
        depart_visible = max(objet["debut"], depart_zoom)
        ecart = objet["fin"] - depart_visible
        return ((x(depart_visible), y(objet[cle] - objet["pente"] * ecart)),
                (x(objet["fin"]), y(objet[cle])))

    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARGEUR}" height="{HAUTEUR}" '
         f'viewBox="0 0 {LARGEUR} {HAUTEUR}" '
         f'font-family="Segoe UI, Helvetica, sans-serif">'),
        f'<rect width="{LARGEUR}" height="{HAUTEUR}" fill="#fbfbfa"/>',
        (f'<text x="{MARGE_G}" y="30" font-size="17" font-weight="600" fill="#1a1a1a">'
         f'{echapper(titre)}</text>'),
        (f'<text x="{MARGE_G}" y="50" font-size="11.5" fill="#666666">'
         f'{jours[depart_zoom]} &#8594; {jours[obs]} &#183; {len(visibles)} '
         f's&#233;ances affich&#233;es'
         + (f' (&#233;chelle construite sur {len(construits)}, depuis le '
            f'{jours[depart]})' if depart_zoom > depart else '')
         + f' &#183; cl&#244;ture {fr(closes[obs])} &#8364;</text>'),
    ]

    pas = pas_lisible(haut - bas)
    niveau = math.ceil(bas / pas) * pas
    while niveau <= haut:
        out.append(f'<line x1="{MARGE_G}" y1="{y(niveau):.1f}" x2="{LARGEUR - MARGE_D}" '
                   f'y2="{y(niveau):.1f}" stroke="#ececec" stroke-width="1"/>')
        out.append(f'<text x="{MARGE_G - 8}" y="{y(niveau) + 4:.1f}" font-size="10.5" '
                   f'fill="#888888" text-anchor="end">{fr(niveau, 0)}</text>')
        niveau += pas

    # Le pas des reperes s'adapte : annuel sur deux ans ou plus, mensuel en deca.
    # Sans cette bascule, un affichage d'un an ne porterait aucun repere.
    mensuel = len(visibles) < 2 * 250
    for i in visibles[1:]:
        coupure = jours[i][:7] != jours[i - 1][:7] if mensuel else \
            jours[i][:4] != jours[i - 1][:4]
        if not coupure:
            continue
        premier_mois = jours[i][5:7] == "01"
        teinte = "#c8c8c8" if (not mensuel or premier_mois) else "#e6e6e6"
        etiquette = jours[i][:4] if (not mensuel or premier_mois) else jours[i][5:7]
        out.append(f'<line x1="{x(i):.1f}" y1="{MARGE_H}" x2="{x(i):.1f}" '
                   f'y2="{MARGE_H + aire_h}" stroke="{teinte}" stroke-width="1" '
                   f'stroke-dasharray="3 4"/>')
        out.append(f'<text x="{x(i) + 4:.1f}" y="{MARGE_H + aire_h + 16:.1f}" '
                   f'font-size="10.5" fill="#888888">{etiquette}</text>')

    # Les bandes a l'ecart-type, de la plus large a la plus etroite.
    for rang, bande in enumerate(bandes):
        teinte = COULEURS_BANDES[min(rang, len(COULEURS_BANDES) - 1)]
        (xh1, yh1), (xh2, yh2) = droite(bande, "haut")
        (xb1, yb1), (xb2, yb2) = droite(bande, "bas")
        out.append(f'<polygon points="{xh1:.1f},{yh1:.1f} {xh2:.1f},{yh2:.1f} '
                   f'{xb2:.1f},{yb2:.1f} {xb1:.1f},{yb1:.1f}" fill="{teinte}" '
                   f'fill-opacity="{0.06 if rang == 0 else 0.08}"/>')
        for cle, style in (("haut", ' stroke-dasharray="6 4"'),
                           ("bas", ' stroke-dasharray="6 4"'), ("VAL", "")):
            (x1, y1), (x2, y2) = droite(bande, cle)
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{teinte}" stroke-width="1.5"{style}/>')

    # L'enveloppe des residus : pas de remplissage, elle est asymetrique.
    for cle, style in (("haut", ' stroke-dasharray="4 3"'),
                       ("bas", ' stroke-dasharray="4 3"'), ("VAL", "")):
        (x1, y1), (x2, y2) = droite(env, cle)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="{COULEUR_ENVELOPPE}" stroke-width="1.8"{style}/>')

    trace = " ".join(f"{'M' if k == 0 else 'L'}{x(i):.1f} {y(closes[i]):.1f}"
                     for k, i in enumerate(visibles))
    out.append(f'<path d="{trace}" fill="none" stroke="{COULEUR_COURS}" '
               f'stroke-width="1.4"/>')

    for indice in (env["contact_bas"], env["contact_haut"]):
        out.append(f'<circle cx="{x(indice):.1f}" cy="{y(closes[indice]):.1f}" r="4.5" '
                   f'fill="none" stroke="{COULEUR_ENVELOPPE}" stroke-width="1.6"/>')
    out.append(f'<circle cx="{x(obs):.1f}" cy="{y(closes[obs]):.1f}" r="4.5" '
               f'fill="{COULEUR_COURS}"/>')

    etiquettes = []
    for rang, bande in enumerate(bandes):
        teinte = COULEURS_BANDES[min(rang, len(COULEURS_BANDES) - 1)]
        etiquettes += [(bande["haut"], teinte), (bande["bas"], teinte)]
    etiquettes += [(env["haut"], COULEUR_ENVELOPPE), (env["bas"], COULEUR_ENVELOPPE)]
    for valeur, teinte in etiquettes:
        out.append(f'<text x="{LARGEUR - MARGE_D + 6}" y="{y(valeur) + 3.5:.1f}" '
                   f'font-size="10.5" fill="{teinte}">{fr(valeur)}</text>')

    out += cartouche(bandes, env, closes[obs], jours)
    out.append(
        f'<text x="{MARGE_G}" y="{HAUTEUR - 30}" font-size="10.5" fill="#555555">'
        f'<tspan fill="{COULEUR_COURS}">&#9472;</tspan> cl&#244;tures &#183; '
        f'<tspan fill="{COULEURS_BANDES[0]}">&#9472;</tspan> bande '
        f'{bandes[0]["n"]} &#177; 1 s &#183; '
        f'<tspan fill="{COULEURS_BANDES[1]}">&#9472;</tspan> bande '
        f'{bandes[1]["n"]} &#177; 1 s &#183; '
        f'<tspan fill="{COULEUR_ENVELOPPE}">&#9472;</tspan> enveloppe des r&#233;sidus '
        f'sur {env["n"]} s&#233;ances (asym&#233;trique, deux contacts)</text>')
    out.append(
        f'<text x="{MARGE_G}" y="{HAUTEUR - 14}" font-size="10" fill="#999999">'
        f'Figure descriptive : aucun verdict, aucune r&#232;gle, aucun conseil en '
        f'investissement. Chaque droite n\'existe que sur sa fen&#234;tre.</text>')
    out.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(out) + "\n", encoding="utf-8")


def cartouche(bandes, env, close, jours):
    """Le recapitulatif en haut a gauche : une ligne par fenetre."""
    out, y0 = [], 70
    out.append(f'<rect x="{MARGE_G - 6}" y="{y0 - 12}" width="470" height="{18 * 4 + 10}" '
               f'fill="#ffffff" fill-opacity="0.82" stroke="#e4e4e4"/>')
    out.append(f'<text x="{MARGE_G}" y="{y0}" font-size="10.5" fill="#888888">'
               f'fen&#234;tre &#183; encadrement &#183; largeur &#183; pente &#183; '
               f'&#233;cart r&#233;duit</text>')
    for rang, bande in enumerate(bandes):
        teinte = COULEURS_BANDES[min(rang, len(COULEURS_BANDES) - 1)]
        ecart = (close - bande["VAL"]) / bande["s"]
        faible = " (CORR faible)" if abs(bande["CORR"]) < CORR_FAIBLE else ""
        out.append(
            f'<text x="{MARGE_G}" y="{y0 + 18 * (rang + 1)}" font-size="11" fill="{teinte}">'
            f'{bande["n"]:>3d} &#177; 1 s : {fr(bande["bas"])} &#8211; {fr(bande["haut"])} '
            f'&#8364; &#183; {fr(bande["largeur"])} &#8364; '
            f'({fr(100 * bande["largeur"] / close)} %) &#183; '
            f'{signe(taux(bande["pente"], bande["E"]), 4)} %/s&#233;ance &#183; '
            f'{signe(ecart)} s{faible}</text>')
    out.append(
        f'<text x="{MARGE_G}" y="{y0 + 18 * 3}" font-size="11" fill="{COULEUR_ENVELOPPE}">'
        f'{env["n"]:>3d} enveloppe : {fr(env["bas"])} &#8211; {fr(env["haut"])} &#8364; '
        f'&#183; {fr(env["largeur"])} &#8364; ({fr(100 * env["largeur"] / close)} %) &#183; '
        f'{signe(taux(env["pente"], env["E"]), 4)} %/s&#233;ance &#183; contacts '
        f'{jours[env["contact_bas"]]} / {jours[env["contact_haut"]]}</text>')
    return out


# --------------------------------------------------------------------------
# Le resume console


def resumer(titre, jours, closes, depart, depart_zoom, obs, bandes, env, recule, chemin):
    close = closes[obs]
    print(f"{titre} — {obs - depart_zoom + 1} séances affichées, du "
          f"{jours[depart_zoom]} au {jours[obs]}")
    if depart_zoom > depart:
        print(f"  tronqué : échelle construite sur {obs - depart + 1} séances, "
              f"depuis le {jours[depart]}")
    if recule:
        print(f"  la date demandée n'est pas une séance : reculée au {jours[obs]}")
    print(f"Clôture au {jours[obs]} : {fr(close)} €\n")
    for bande in bandes:
        ecart = (close - bande["VAL"]) / bande["s"]
        print(f"  bande {bande['n']:>3d}   {fr(bande['bas'])} – {fr(bande['haut'])} €"
              f"   largeur {fr(bande['largeur'])} € "
              f"({fr(100 * bande['largeur'] / close)} %)"
              f"   pente {signe(bande['pente'], 4)} €/séance "
              f"({signe(taux(bande['pente'], bande['E']), 4)} %/séance)")
        print(f"              droite {fr(bande['VAL'])} €   CORR "
              f"{signe(bande['CORR'], 4)}   écart réduit {signe(ecart)} s")
        if abs(bande["CORR"]) < CORR_FAIBLE:
            print(f"    ⚠ CORR = {signe(bande['CORR'], 3)} : la droite n'explique presque "
                  "rien, cette bande est une dispersion et non un canal.")
        if abs(close - bande["bas"]) < bande["s"] / 10 or \
                abs(close - bande["haut"]) < bande["s"] / 10:
            print("    ⚠ la clôture touche une borne : lire cette coïncidence avec "
                  "prudence.")
    print(f"  enveloppe {env['n']:>2d}  {fr(env['bas'])} – {fr(env['haut'])} €"
          f"   largeur {fr(env['largeur'])} € ({fr(100 * env['largeur'] / close)} %)"
          f"   pente {signe(env['pente'], 4)} €/séance "
          f"({signe(taux(env['pente'], env['E']), 4)} %/séance)")
    print(f"              droite {fr(env['VAL'])} €   contacts bas "
          f"{jours[env['contact_bas']]}, haut {jours[env['contact_haut']]}"
          f"   asymétrie {fr(env['demi_bas'])} bas / {fr(env['demi_haut'])} haut")
    print(f"\nGraphique écrit dans : {chemin}")


# --------------------------------------------------------------------------


def analyser_arguments():
    parser = argparse.ArgumentParser(
        description="Trace un cours et ses trois derniers encadrements, ancres a une date.")
    parser.add_argument("--csv", type=Path, help="CSV de la valeur (Date et Close requis)")
    parser.add_argument("--date", help="Date d'observation AAAA-MM-JJ")
    parser.add_argument("--annees", type=int, default=3,
                        help="Annees de construction : fixent l'echelle (defaut 3)")
    parser.add_argument("--zoom", type=int,
                        help="Annees affichees apres troncature (defaut : --annees)")
    parser.add_argument("--fenetres", default="250,120",
                        help="Fenetres encadrees a l'ecart-type (defaut 250,120)")
    parser.add_argument("--enveloppe", type=int, default=20,
                        help="Fenetre encadree par l'enveloppe des residus (defaut 20)")
    parser.add_argument("--sortie", type=Path, help="Chemin du SVG produit")
    parser.add_argument("--titre", help="Titre inscrit dans le SVG")
    args = parser.parse_args()
    try:
        args.liste_fenetres = sorted(
            (int(f) for f in args.fenetres.split(",") if f.strip()), reverse=True)
    except ValueError:
        erreur(f"--fenetres : « {args.fenetres} » n'est pas une liste d'entiers.")
    if not args.liste_fenetres:
        erreur("--fenetres : au moins une fenetre est requise.")
    if min(args.liste_fenetres) < 3 or args.enveloppe < 3:
        erreur("Une fenetre doit compter au moins 3 seances.")
    if args.annees < 1:
        erreur("--annees doit valoir au moins 1.")
    if args.zoom is None:
        args.zoom = args.annees
    if args.zoom < 1:
        erreur("--zoom doit valoir au moins 1.")
    if args.zoom > args.annees:
        erreur(f"--zoom {args.zoom} depasse --annees {args.annees} : on tronque une "
               "fenetre de construction, on ne l'etend pas.")
    return args


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    args = analyser_arguments()
    chemin_csv = args.csv or csv_par_defaut()
    if not chemin_csv.exists():
        erreur(f"CSV introuvable : {chemin_csv}")
    jours, closes = charger(chemin_csv)

    obs, recule = rang_observation(jours, args.date)
    besoin = max(*args.liste_fenetres, args.enveloppe)
    if obs + 1 < besoin:
        erreur(f"{obs + 1} seances jusqu'au {jours[obs]}, il en faut {besoin} pour la "
               "plus longue fenetre.")

    bandes = [regression(closes, obs, n) for n in args.liste_fenetres]
    env = enveloppe(closes, obs, args.enveloppe)

    def premier_rang(annees):
        limite = f"{int(jours[obs][:4]) - annees}{jours[obs][4:]}"
        return next((i for i, j in enumerate(jours) if j > limite), 0)

    # La fenetre de CONSTRUCTION fixe l'echelle ; elle est elargie si une droite
    # deborde, pour qu'aucun encadrement ne soit tronque a gauche.
    depart = min(premier_rang(args.annees), *(b["debut"] for b in bandes))
    # La fenetre AFFICHEE tronque ensuite, sans jamais depasser la construction.
    depart_zoom = max(premier_rang(args.zoom), depart)

    ticker = chemin_csv.stem.split("_20")[0].replace("_", ".")
    titre = args.titre or f"{ticker} — canal au {jours[obs]}"
    sortie = args.sortie or (REPERTOIRE_GRAPHS /
                             f"{chemin_csv.stem}_canal_{jours[obs]}.svg")
    svg(sortie, titre, jours, closes, depart, depart_zoom, obs, bandes, env)
    resumer(titre, jours, closes, depart, depart_zoom, obs, bandes, env, recule, sortie)


if __name__ == "__main__":
    main()
