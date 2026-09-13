#!/usr/bin/env python3
"""Cherche la largeur de bande la plus étroite qui encadre encore, et la trace.

Pour chaque longueur de fenêtre n et chaque horizon h, le script mesure ce que la
bande ± k s contient RÉELLEMENT des clôtures à venir, et la largeur qu'il faudrait
lui donner pour en contenir 95 %. C'est cette largeur-là que le balayage minimise.

Deux figures en sortent : la bande ajustée sur l'étalonnage puis prolongée sur
l'année hors échantillon, et la courbe de la largeur fiable en fonction de n.

Dépendance : aucune. Le CSV est lu par le module csv, le SVG écrit à la main.

Utilisation :
    python docs/raw/lab/figures/generer_largeur_fiable.py
    python docs/raw/lab/figures/generer_largeur_fiable.py --table
    python docs/raw/lab/figures/generer_largeur_fiable.py --sortie /tmp

Le miroir d'exécution est dans generer_largeur_fiable.md, et il fait autorité.
"""

import argparse
import bisect
import csv
import itertools
import math
import statistics
import sys
from pathlib import Path

CSV_DEFAUT = Path("docs/raw/data/quotes/MC_PA_2019-01-02_2026-09-11.csv")
FENETRES = "20,40,60,90,120,180,250,375,500,750,1000,1275"
HORIZONS = "1,5,20,60,250"
ANCRAGES_MIN = 100
SAUT_SCISSION = 0.50
CORR_FAIBLE = 0.20

L, H = 1200, 720
X0, X1 = 66, 1104
Y0, Y1 = 92, 524
Y_CART = 566          # le cartouche est SOUS l'aire de trace, jamais dedans

COURS = "#2a78d6"
RES = "#eb6834"
SUP = "#1baf7a"
DECISION = "#8b5cd6"
GRILLE = "#e1e0d9"
AXE = "#c3c2b7"
ENCRE = "#0b0b0b"
ENCRE2 = "#52514e"
FOND = "#fcfcfb"
FENETRE = "#f2efe4"
TEINTES = ("#1baf7a", "#2a78d6", "#8b5cd6", "#eb6834", "#b3123a")
TEINTES_ETALONNAGE = ("#eb6834", "#1baf7a", "#8b5cd6", "#b3123a")


def erreur(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def fr(x, decimales=2):
    """Virgule décimale française, espace insécable étroite pour les milliers."""
    if x is None:
        return "—"
    return f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")


def signe(x, decimales=2):
    return "—" if x is None else ("+" if x >= 0 else "") + fr(x, decimales)


def ent(texte):
    """Échappe le XML, puis rend tout non-ASCII en entité numérique.

    La source du script reste ainsi lisible en français, et le SVG produit ne
    dépend d'aucune déclaration d'encodage.
    """
    texte = texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in texte)


# --------------------------------------------------------------------------
# La donnée


def charger(chemin, debut, fin):
    """Rend (jours, clôtures, divisions) entre debut et fin INCLUSES."""
    jours, closes, divisions = [], [], []
    with chemin.open(encoding="utf-8", newline="") as flux:
        lecteur = csv.DictReader(flux)
        colonnes = lecteur.fieldnames or []
        if "Date" not in colonnes or "Close" not in colonnes:
            erreur(f"{chemin} : colonnes « Date » et « Close » requises.")
        for ligne in lecteur:
            jour = ligne["Date"][:10]
            if jour < debut or jour > fin or not ligne["Close"]:
                continue
            jours.append(jour)
            closes.append(float(ligne["Close"]))
            divisions.append(float(ligne.get("Stock Splits") or 0.0))
    if not closes:
        erreur(f"{chemin} : aucune séance entre {debut} et {fin}.")
    return jours, closes, divisions


def controler_scissions(jours, closes, divisions):
    """Tout saut de plus de 50 % sans division déclarée vaut opération sur titre.

    C'est le contrôle des invariants du dépôt : une scission n'est pas une
    division, le fournisseur ne la répercute pas, et la série devient irrecevable.
    """
    for i in range(1, len(closes)):
        variation = closes[i] / closes[i - 1] - 1
        if abs(variation) > SAUT_SCISSION and not divisions[i]:
            erreur(f"{jours[i]} : saut de {100 * variation:+.1f} % sans division "
                   "déclarée — opération sur titre présumée, série irrecevable.", code=2)


def rang_de(jours, date):
    """Le rang de la dernière séance antérieure ou égale à `date`, sinon None."""
    for i in range(len(jours) - 1, -1, -1):
        if jours[i] <= date:
            return i
    return None


# --------------------------------------------------------------------------
# La droite ajustée, et ce qu'on en tire


def ajuster(closes, fin, n):
    """La droite des moindres carrés sur les n clôtures finissant au rang `fin`."""
    vals = closes[fin - n + 1:fin + 1]
    moyenne_t = (n + 1) / 2
    moyenne_v = statistics.fmean(vals)
    var_t = (n * n - 1) / 12
    var_v = sum((v - moyenne_v) ** 2 for v in vals) / n            # ddof = 0
    if var_v <= 0:
        erreur(f"Fenêtre {n} finissant au rang {fin} : variance nulle.", code=2)
    cov = sum((t - moyenne_t) * (v - moyenne_v)
              for t, v in enumerate(vals, start=1)) / n
    pente = cov / var_t
    residus = [v - (moyenne_v + pente * (t - moyenne_t))
               for t, v in enumerate(vals, start=1)]
    sce = sum(e * e for e in residus)
    if sce <= 0:
        erreur(f"Fenêtre {n} finissant au rang {fin} : résidus tous nuls.", code=2)
    return {"n": n, "E": moyenne_v, "pente": pente, "residus": residus,
            "val": moyenne_v + pente * (n - moyenne_t),
            "corr": cov / math.sqrt(var_t * var_v),
            "s": math.sqrt(sce / (n - 2))}


def centile(tri, p):
    """Interpolation linéaire sur une liste TRIÉE, convention (n-1)p."""
    k = (len(tri) - 1) * p
    i = int(k)
    if i + 1 >= len(tri):
        return tri[-1]
    return tri[i] + (k - i) * (tri[i + 1] - tri[i])


def durbin_watson(residus):
    """Somme des carrés des écarts successifs, rapportée à la somme des carrés."""
    numerateur = sum((b - a) ** 2 for a, b in itertools.pairwise(residus))
    return numerateur / sum(e * e for e in residus)


def dedans(residus, s):
    """Les proportions de résidus dans ± 1 s, ± 2 s et ± 3 s, en pourcentage.

    Le troisième niveau n'est pas décoratif : le balayage rend k95 ≈ 2,9 dès
    l'horizon d'une séance, c'est donc ± 3 s qui serait la bande honnête.
    """
    n = len(residus)
    return tuple(100 * sum(1 for e in residus if abs(e) <= k * s) / n
                 for k in (1, 2, 3))


# --------------------------------------------------------------------------
# Le balayage


def balayer(closes, fenetres, horizons, ancrages_min):
    """Pour chaque (n, h) : ce que la bande contient devant elle, et ce qu'il faudrait.

    L'ajustement est fait UNE fois par date d'ancrage, puis réutilisé par tous les
    horizons : c'est ce qui rend le balayage tenable en Python pur.
    """
    n_etal = len(closes)
    ajustement, projection = {}, {}
    for n in fenetres:
        if n >= n_etal:
            continue
        vals, pentes, ss, largeurs = [], [], [], []
        somme1 = somme2 = 0.0
        for t in range(n - 1, n_etal):
            a = ajuster(closes, t, n)
            vals.append(a["val"])
            pentes.append(a["pente"])
            ss.append(a["s"])
            largeurs.append(2 * a["s"] / a["val"])
            d1, d2, _ = dedans(a["residus"], a["s"])
            somme1 += d1
            somme2 += d2
        ajustement[n] = {"largeur": 100 * statistics.median(largeurs),
                         "tau1": somme1 / len(vals), "tau2": somme2 / len(vals)}
        for h in horizons:
            retenus = n_etal - h - n + 1
            if retenus < ancrages_min:
                continue
            ecarts = []
            for k in range(retenus):
                t, val, pente, s = n - 1 + k, vals[k], pentes[k], ss[k]
                ecarts += [abs(closes[t + j] - val - pente * j) / s
                           for j in range(1, h + 1)]
            ecarts.sort()
            largeur = 100 * statistics.median(largeurs[:retenus])
            k95 = centile(ecarts, 0.95)
            projection[(n, h)] = {
                "ancrages": retenus,
                "points": len(ecarts),
                "tau1": 100 * bisect.bisect_right(ecarts, 1.0) / len(ecarts),
                "tau2": 100 * bisect.bisect_right(ecarts, 2.0) / len(ecarts),
                "k95": k95,
                "largeur": largeur,
                "fiable": k95 * largeur,
            }
    if not ajustement:
        erreur("Aucune fenêtre ne tient dans l'étalonnage : rien à balayer.")
    return ajustement, projection


def minimum(projection, fenetres, h):
    """La fenêtre de largeur fiable minimale à l'horizon h, ou None."""
    candidats = [n for n in fenetres if (n, h) in projection]
    if not candidats:
        return None
    return min(candidats, key=lambda n: projection[(n, h)]["fiable"])


# --------------------------------------------------------------------------
# Les primitives de tracé


def pas_lisible(amplitude, cibles=8):
    brut = max(amplitude / cibles, 1e-12)
    puissance = 10 ** math.floor(math.log10(brut))
    for multiple in (1, 2, 2.5, 5, 10):
        if multiple * puissance >= brut:
            return multiple * puissance
    return 10 * puissance


def entete(titre, sous_titre):
    return [
        (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" width="{L}" '
         f'height="{H}" font-family="ui-monospace,Consolas,monospace">'),
        f'<rect width="{L}" height="{H}" fill="{FOND}"/>',
        (f'<text x="{X0}" y="36" font-size="19" font-weight="600" fill="{ENCRE}" '
         f'font-family="Georgia,serif">{ent(titre)}</text>'),
        f'<text x="{X0}" y="58" font-size="12" fill="{ENCRE2}">{ent(sous_titre)}</text>',
    ]


def grille_y(y, bas, haut, unite=""):
    out, pas = [], pas_lisible(haut - bas)
    niveau = math.ceil(bas / pas) * pas
    while niveau <= haut:
        yy = y(niveau)
        out.append(f'<line x1="{X0}" y1="{yy:.1f}" x2="{X1}" y2="{yy:.1f}" '
                   f'stroke="{GRILLE}" stroke-width="1"/>')
        out.append(f'<text x="{X0 - 10}" y="{yy + 4:.1f}" text-anchor="end" font-size="11" '
                   f'fill="{ENCRE2}">{ent(fr(niveau, 0) + unite)}</text>')
        niveau += pas
    out.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{AXE}" '
               f'stroke-width="1"/>')
    return out


def cartouche(lignes, colonnes=2, y=Y_CART):
    """Le cartouche de lecture, posé SOUS l'aire de tracé et non dedans.

    Chercher un coin libre à l'intérieur du cadre ne marche pas ici : un cours
    sur plusieurs années barre toute la largeur de la figure et occupe presque
    toute sa hauteur. Le meilleur des quatre coins masquait encore 105 clôtures
    sur 1 023. Hors du cadre, le recouvrement est nul par construction, quelle
    que soit la série — et les lignes se répartissent en colonnes pour que le
    bandeau reste bas.
    """
    lignes = [ligne for ligne in lignes if ligne[0]]
    rangs = math.ceil(len(lignes) / colonnes)
    large = (X1 - X0) / colonnes
    out = [(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="{18 * rangs + 14}" '
            f'fill="{FOND}" stroke="{AXE}" stroke-width="1"/>')]
    for k, (texte, couleur, gras) in enumerate(lignes):
        poids = ' font-weight="600"' if gras else ""
        out.append(f'<text x="{X0 + 12 + large * (k // rangs):.0f}" '
                   f'y="{y + 21 + 18 * (k % rangs)}" font-size="12" '
                   f'fill="{couleur}"{poids}>{ent(texte)}</text>')
    return out


def ecrire(chemin, lignes):
    """CRLF explicites : la figure est alors identique sur tout système."""
    lignes.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline="") as flux:
        flux.write("\r\n".join(lignes) + "\r\n")
    print(f"Graphique écrit dans : {chemin}")


# --------------------------------------------------------------------------
# La figure de la bande


def figure_bande(chemin, jours, closes, charniere, bande, mesures, ticker):
    """La bande ajustée sur l'étalonnage, prolongée en pointillé hors échantillon."""
    total = len(closes)
    s = bande["s"]

    def x(i):
        return X0 + (X1 - X0) * i / (total - 1)

    def niveau(i, k):
        return bande["val"] + bande["pente"] * (i - charniere) + k * s

    bas = min(*closes, niveau(0, -3), niveau(total - 1, -3))
    haut = max(*closes, niveau(0, 3), niveau(total - 1, 3))
    marge = 0.06 * (haut - bas)
    bas, haut = bas - marge, haut + marge

    def y(v):
        return Y1 - (Y1 - Y0) * (v - bas) / (haut - bas)

    out = entete(
        f"{ticker} — la bande ajustée sur {jours[0][:4]}-{jours[charniere][:4]}, "
        f"prolongée sur {jours[-1][:4]}",
        f"droite des moindres carrés sur {charniere + 1} séances · bandes ± 1 s et "
        f"± 2 s · à droite de la charnière, plus aucune séance n'a servi à l'ajuster")

    if charniere < total - 1:
        xa = x(charniere)
        out.append(f'<rect x="{xa:.1f}" y="{Y0}" width="{X1 - xa:.1f}" '
                   f'height="{Y1 - Y0}" fill="{FENETRE}" opacity="0.85"/>')
    out += grille_y(y, bas, haut, " €")

    for i in range(1, total):
        if jours[i][:4] == jours[i - 1][:4]:
            continue
        out.append(f'<line x1="{x(i):.1f}" y1="{Y0}" x2="{x(i):.1f}" y2="{Y1}" '
                   f'stroke="{GRILLE}" stroke-width="1"/>')
        out.append(f'<text x="{x(i) + 5:.1f}" y="{Y1 + 18:.1f}" font-size="11" '
                   f'fill="{ENCRE2}">{jours[i][:4]}</text>')

    for k, opacite in ((3, 0.05), (2, 0.07), (1, 0.09)):
        points = [(x(0), y(niveau(0, k))), (x(total - 1), y(niveau(total - 1, k))),
                  (x(total - 1), y(niveau(total - 1, -k))), (x(0), y(niveau(0, -k)))]
        pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
        out.append(f'<polygon points="{pts}" fill="{COURS}" opacity="{opacite}"/>')

    # Chaque bord en deux morceaux : plein sur l'ajustement, pointille sur la
    # projection. Le tiret portant deja cette distinction, les +- 3 s se
    # demarquent par un trait fin estompe, jamais par un motif de plus.
    bords = ((3, RES, 1.1, 0.5), (2, RES, 1.8, 1.0), (1, DECISION, 1.6, 1.0),
             (0, ENCRE2, 1.2, 1.0), (-1, DECISION, 1.6, 1.0),
             (-2, SUP, 1.8, 1.0), (-3, SUP, 1.1, 0.5))
    for k, couleur, epaisseur, opacite in bords:
        for i0, i1, tirets in ((0, charniere, "6 5" if k == 0 else None),
                               (charniere, total - 1, "3 4")):
            if i1 <= i0:
                continue
            dash = f' stroke-dasharray="{tirets}"' if tirets else ""
            out.append(f'<line x1="{x(i0):.1f}" y1="{y(niveau(i0, k)):.1f}" '
                       f'x2="{x(i1):.1f}" y2="{y(niveau(i1, k)):.1f}" stroke="{couleur}" '
                       f'stroke-width="{epaisseur}" opacity="{opacite}"{dash}/>')

    trace = [(x(i), y(c)) for i, c in enumerate(closes)]
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in trace)
    out.append(f'<polyline points="{pts}" fill="none" stroke="{COURS}" stroke-width="1.4"/>')

    for i in range(charniere + 1, total):
        if abs(closes[i] - niveau(i, 0)) > 2 * s:
            out.append(f'<circle cx="{x(i):.1f}" cy="{y(closes[i]):.1f}" r="2.6" '
                       f'fill="{RES}"/>')
    out.append(f'<circle cx="{x(charniere):.1f}" cy="{y(closes[charniere]):.1f}" r="4.2" '
               f'fill="{FOND}" stroke="{ENCRE}" stroke-width="1.6"/>')

    if charniere < total - 1:
        out.append(f'<text x="{x(charniere) + 8:.1f}" y="{Y0 + 18:.1f}" font-size="11" '
                   f'fill="{ENCRE}" font-weight="600">'
                   f'{ent("hors échantillon — " + jours[charniere + 1] + " →")}</text>')

    manque = mesures["h2"] is not None and mesures["h2"] < 95.5
    lignes = [
        ((f"fenêtre {bande['n']} séances   pente "
          f"{signe(100 * bande['pente'] / bande['E'], 4)} %/séance   "
          f"CORR {signe(bande['corr'], 3)}"), ENCRE, True),
        ((f"s = {fr(s)} €   bande ± 1 s large de {fr(2 * s)} € "
          f"({fr(mesures['largeur'])} % du cours)"), ENCRE, True),
        ((f"Durbin-Watson {fr(mesures['dw'], 3)}   "
          f"(2 = indépendance, 0 = autocorrélation parfaite)"), ENCRE2, False),
        ("", ENCRE2, False),
        ((f"dedans à l'ajustement    ± 1 s {fr(mesures['a1'], 1)} %   "
          f"± 2 s {fr(mesures['a2'], 1)} %   ± 3 s {fr(mesures['a3'], 1)} %"),
         ENCRE, True),
        ((f"dedans hors échantillon  ± 1 s {fr(mesures['h1'], 1)} %   "
          f"± 2 s {fr(mesures['h2'], 1)} %   ± 3 s {fr(mesures['h3'], 1)} %"),
         RES if manque else ENCRE, True),
        (("attendu sous loi normale ± 1 s 68,3 %   ± 2 s 95,5 %   ± 3 s 99,7 %"),
         ENCRE2, False),
        (f"écart réduit au {jours[-1]} : {signe(mesures['ecart'])} s", ENCRE, True),
    ]
    out += cartouche(lignes)

    out.append(f'<text x="{X0}" y="{H - 34}" font-size="11" fill="{ENCRE2}">'
               f'<tspan fill="{COURS}">&#9472;</tspan> clôtures &#183; '
               f'<tspan fill="{DECISION}">&#9472;</tspan> ± 1 s &#183; '
               f'<tspan fill="{RES}">&#9472;</tspan> + 2 s &#183; '
               f'<tspan fill="{SUP}">&#9472;</tspan> &#8722; 2 s &#183; '
               f'± 3 s en trait fin estompé &#183; '
               f'trait plein = ajusté, pointillé = projeté &#183; '
               f'<tspan fill="{RES}">&#9679;</tspan> clôture hors échantillon sortie '
               f'de ± 2 s</text>'.replace("±", "&#177;"))
    note = ("Figure descriptive : aucun verdict, aucune règle, aucun conseil en "
            "investissement. La droite n'existe que sur sa fenêtre — à droite de la "
            "charnière, elle est une extrapolation.")
    out.append(f'<text x="{X0}" y="{H - 16}" font-size="10.5" fill="#999999">'
               f'{ent(note)}</text>')
    ecrire(chemin, out)


# --------------------------------------------------------------------------
# La figure du balayage


def figure_balayage(chemin, fenetres, horizons, projection, ticker, etendue):
    """La largeur fiable L(n, h), une polyligne par horizon, minimum marqué."""
    valeurs = [projection[(n, h)]["fiable"] for n in fenetres for h in horizons
               if (n, h) in projection]
    bas, haut = 0.0, max(valeurs) * 1.12

    def x(k):
        return X0 + (X1 - X0) * k / max(len(fenetres) - 1, 1)

    def y(v):
        return Y1 - (Y1 - Y0) * (v - bas) / (haut - bas)

    out = entete(
        f"{ticker} — la largeur qu'il faut vraiment donner à la bande",
        f"{etendue} · largeur relative contenant 95 % des clôtures projetées, "
        f"par longueur de fenêtre et par horizon · abscisse à pas constant, "
        f"les fenêtres ne sont pas régulièrement espacées")
    out += grille_y(y, bas, haut, " %")

    for k, n in enumerate(fenetres):
        out.append(f'<line x1="{x(k):.1f}" y1="{Y0}" x2="{x(k):.1f}" y2="{Y1}" '
                   f'stroke="{GRILLE}" stroke-width="1"/>')
        out.append(f'<text x="{x(k):.1f}" y="{Y1 + 18:.1f}" text-anchor="middle" '
                   f'font-size="11" fill="{ENCRE2}">{n}</text>')
    out.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{Y1 + 38:.0f}" text-anchor="middle" '
               f'font-size="11" fill="{ENCRE2}">{ent("longueur de la fenêtre, en séances")}'
               f'</text>')

    legende = []
    for rang, h in enumerate(horizons):
        teinte = TEINTES[rang % len(TEINTES)]
        couples = [(k, projection[(n, h)]["fiable"])
                   for k, n in enumerate(fenetres) if (n, h) in projection]
        if not couples:
            continue
        pts = " ".join(f"{x(k):.1f},{y(v):.1f}" for k, v in couples)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{teinte}" '
                   f'stroke-width="1.8"/>')
        k_min, v_min = min(couples, key=lambda c: c[1])
        out.append(f'<circle cx="{x(k_min):.1f}" cy="{y(v_min):.1f}" r="4.4" '
                   f'fill="{teinte}"/>')
        k_fin, v_fin = couples[-1]
        out.append(f'<text x="{x(k_fin) + 8:.1f}" y="{y(v_fin) + 4:.1f}" font-size="11" '
                   f'fill="{teinte}" font-weight="600">{ent(f"h = {h}")}</text>')
        legende.append(((f"horizon {h:>3} séances   minimum à n = {fenetres[k_min]:>4}   "
                         f"largeur fiable {fr(v_min)} %"), teinte, True))

    out += cartouche(legende)
    note = ("Les dates d'ancrage se recouvrent massivement : ces proportions sont "
            "descriptives, elles ne portent aucun intervalle de confiance.")
    out.append(f'<text x="{X0}" y="{H - 16}" font-size="10.5" fill="#999999">'
               f'{ent(note)}</text>')
    ecrire(chemin, out)


# --------------------------------------------------------------------------
# Les prolongements, dans la seule zone hors échantillon


def figure_prolongements(chemin, jours, closes, charniere, bandes, ticker):
    """Les bandes ± 3 s de plusieurs étalonnages, chacune sur sa fenêtre puis projetée.

    Tout l'historique chargé est affiché, et la charnière le coupe en deux. Chaque
    bande ne commence qu'à SA propre date de départ — une droite d'encadrement
    n'existe pas hors de la fenêtre qui l'a produite — en trait plein jusqu'à la
    charnière, puis en pointillé sur la zone ombrée, où elle n'est plus qu'une
    extrapolation.
    """
    total = len(closes)

    def x(i):
        return X0 + (X1 - X0) * i / max(total - 1, 1)

    def niveau(bande, i, k):
        return bande["val"] + bande["pente"] * (i - charniere) + k * bande["s"]

    # Chaque bande ne pese sur l'echelle que sur l'etendue ou elle est tracee.
    bornes = [niveau(b, i, k) for b in bandes for i in (b["i0"], total - 1)
              for k in (-3, 3)]
    bas, haut = min(*closes, *bornes), max(*closes, *bornes)
    marge = 0.06 * (haut - bas)
    bas, haut = bas - marge, haut + marge

    def y(v):
        return Y1 - (Y1 - Y0) * (v - bas) / (haut - bas)

    out = entete(
        f"{ticker} — encadrements ± 3 s, chacun sur sa fenêtre, prolongés sur "
        f"{jours[-1][:4]}",
        f"ajustés jusqu'au {jours[charniere]} · trait plein = ajusté, pointillé sur "
        f"fond ombré = projeté · {total} séances du {jours[0]} au {jours[-1]}")

    if charniere < total - 1:
        xa = x(charniere)
        out.append(f'<rect x="{xa:.1f}" y="{Y0}" width="{X1 - xa:.1f}" '
                   f'height="{Y1 - Y0}" fill="{FENETRE}" opacity="0.85"/>')
    out += grille_y(y, bas, haut, " €")

    # Reperes annuels si l'affichage couvre deux ans ou plus, mensuels en deca :
    # sans cette bascule, un affichage d'un an ne porterait aucun repere.
    mensuel = total < 2 * 250
    for i in range(1, total):
        coupure = (jours[i][5:7] != jours[i - 1][5:7] if mensuel
                   else jours[i][:4] != jours[i - 1][:4])
        if not coupure:
            continue
        out.append(f'<line x1="{x(i):.1f}" y1="{Y0}" x2="{x(i):.1f}" y2="{Y1}" '
                   f'stroke="{GRILLE}" stroke-width="1"/>')
        out.append(f'<text x="{x(i) + 4:.1f}" y="{Y1 + 18:.1f}" font-size="11" '
                   f'fill="{ENCRE2}">{jours[i][5:7] if mensuel else jours[i][:4]}</text>')

    # Seuls les +- 3 s sont traces : c'est la largeur que le balayage designe comme
    # honnete (k95 = 2,9 des l'horizon d'une seance), et cette figure ne pose qu'une
    # question — meme celle-la tient-elle ? Les +- 1 s et +- 2 s restent chiffres au
    # cartouche. Plus rien n'etant a en distinguer, le trait redevient plein.
    for rang, bande in enumerate(bandes):
        teinte = TEINTES_ETALONNAGE[rang % len(TEINTES_ETALONNAGE)]
        i0 = bande["i0"]
        coins = [(x(i0), y(niveau(bande, i0, 3))),
                 (x(total - 1), y(niveau(bande, total - 1, 3))),
                 (x(total - 1), y(niveau(bande, total - 1, -3))),
                 (x(i0), y(niveau(bande, i0, -3)))]
        pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in coins)
        out.append(f'<polygon points="{pts}" fill="{teinte}" opacity="0.07"/>')
        for k in (3, -3):
            for ia, ib, tirets in ((i0, charniere, None),
                                   (charniere, total - 1, "3 4")):
                if ib <= ia:
                    continue
                dash = f' stroke-dasharray="{tirets}"' if tirets else ""
                out.append(f'<line x1="{x(ia):.1f}" '
                           f'y1="{y(niveau(bande, ia, k)):.1f}" '
                           f'x2="{x(ib):.1f}" '
                           f'y2="{y(niveau(bande, ib, k)):.1f}" stroke="{teinte}" '
                           f'stroke-width="1.8"{dash}/>')

    pts = " ".join(f"{x(i):.1f},{y(c):.1f}" for i, c in enumerate(closes))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{COURS}" '
               f'stroke-width="1.4"/>')
    out.append(f'<circle cx="{x(charniere):.1f}" cy="{y(closes[charniere]):.1f}" '
               f'r="4.2" fill="{FOND}" stroke="{ENCRE}" stroke-width="1.6"/>')

    lignes = []
    for rang, bande in enumerate(bandes):
        teinte = TEINTES_ETALONNAGE[rang % len(TEINTES_ETALONNAGE)]
        m = bande["mesures"]
        lignes += [
            ((f"{bande['debut']} → {jours[charniere]}   {bande['n']} séances   "
              f"CORR {signe(bande['corr'], 3)}"), teinte, True),
            ((f"pente {signe(100 * bande['pente'] / bande['E'], 4)} %/séance   "
              f"s {fr(bande['s'])} €   ± 1 s = {fr(m['largeur'])} % du cours"),
             teinte, False),
            ((f"hors échantillon : ± 1 s {fr(m['h1'], 1)} %   "
              f"± 2 s {fr(m['h2'], 1)} %   ± 3 s {fr(m['h3'], 1)} %"), teinte, True),
            (f"écart réduit de la dernière clôture : {signe(m['ecart'])} s",
             teinte, False),
        ]
    out += cartouche(lignes, colonnes=len(bandes))

    out.append(f'<text x="{X0}" y="{H - 34}" font-size="11" fill="{ENCRE2}">'
               f'<tspan fill="{COURS}">&#9472;</tspan> cl&#244;tures &#183; '
               f'une bande &#177; 3 s par &#233;talonnage, trac&#233;e depuis sa '
               f'propre date de d&#233;part &#183; trait plein = ajust&#233;, '
               f'pointill&#233; sur fond ombr&#233; = projet&#233;</text>')
    note = ("Les proportions du cartouche portent sur la seule zone ombrée. Une droite "
            "d'encadrement n'existe pas hors de la fenêtre qui l'a produite, et au-delà "
            "de la charnière elle n'est plus qu'une extrapolation. Aucun verdict, "
            "aucune règle, aucun conseil.")
    out.append(f'<text x="{X0}" y="{H - 16}" font-size="10.5" fill="#999999">'
               f'{ent(note)}</text>')
    ecrire(chemin, out)


# --------------------------------------------------------------------------
# Le relevé console


def imprimer_balayage(fenetres, horizons, ajustement, projection):
    print("\n--- dans la fenêtre d'ajustement, pour mémoire ---")
    print(f"{'n':>6}   {'largeur':>9}   {'dedans ±1 s':>12}   {'dedans ±2 s':>12}")
    for n in fenetres:
        if n not in ajustement:
            continue
        a = ajustement[n]
        print(f"{n:>6}   {fr(a['largeur']) + ' %':>9}   {fr(a['tau1'], 1) + ' %':>12}   "
              f"{fr(a['tau2'], 1) + ' %':>12}")
    print("  attendu sous loi normale : 68,3 % et 95,5 % — et ces séances ont servi "
          "à poser la droite.")

    for h in horizons:
        publies = [n for n in fenetres if (n, h) in projection]
        if not publies:
            print(f"\n--- horizon {h} séances : aucune fenêtre ne réunit assez "
                  "d'ancrages ---")
            continue
        print(f"\n--- horizon {h} séances ---")
        print(f"{'n':>6}   {'ancrages':>8}   {'largeur':>9}   {'k95':>6}   "
              f"{'dedans ±1 s':>12}   {'dedans ±2 s':>12}   {'largeur fiable':>14}")
        for n in fenetres:
            if (n, h) not in projection:
                print(f"{n:>6}   {'—':>8}")
                continue
            p = projection[(n, h)]
            print(f"{n:>6}   {p['ancrages']:>8}   {fr(p['largeur']) + ' %':>9}   "
                  f"{fr(p['k95']):>6}   {fr(p['tau1'], 1) + ' %':>12}   "
                  f"{fr(p['tau2'], 1) + ' %':>12}   {fr(p['fiable']) + ' %':>14}")
        n_min = minimum(projection, fenetres, h)
        p = projection[(n_min, h)]
        print(f"  minimum : n = {n_min}, largeur fiable {fr(p['fiable'])} % "
              f"(nominale {fr(p['largeur'])} %, k95 = {fr(p['k95'])})")


def imprimer_bande(jours, charniere, bande, mesures):
    print(f"\n--- bande ajustée sur {bande['n']} séances, du {bande['debut']} au "
          f"{jours[charniere]} ---")
    print(f"  droite {fr(bande['val'])} €   pente "
          f"{signe(100 * bande['pente'] / bande['E'], 4)} %/séance   "
          f"CORR {signe(bande['corr'], 3)}   s {fr(bande['s'])} €")
    print(f"  largeur ± 1 s : {fr(2 * bande['s'])} € ({fr(mesures['largeur'])} %)   "
          f"Durbin-Watson {fr(mesures['dw'], 3)}")
    print(f"  dedans à l'ajustement   ±1 s {fr(mesures['a1'], 1)} %   "
          f"±2 s {fr(mesures['a2'], 1)} %   ±3 s {fr(mesures['a3'], 1)} %")
    print(f"  dedans hors échantillon ±1 s {fr(mesures['h1'], 1)} %   "
          f"±2 s {fr(mesures['h2'], 1)} %   ±3 s {fr(mesures['h3'], 1)} %")
    print(f"  écart réduit au {jours[-1]} : {signe(mesures['ecart'])} s")
    if abs(bande["corr"]) < CORR_FAIBLE:
        print(f"  ⚠ CORR = {signe(bande['corr'], 3)} : la droite n'explique presque rien, "
              "cette bande est une dispersion et non un canal.")
    if mesures["dw"] < 1.0:
        print(f"  ⚠ Durbin-Watson = {fr(mesures['dw'], 3)} : les résidus sont fortement "
              "autocorrélés, aucune garantie gaussienne ne tient.")


# --------------------------------------------------------------------------


def analyser_arguments():
    parser = argparse.ArgumentParser(
        description="La largeur de bande la plus étroite qui encadre encore.")
    parser.add_argument("--csv", type=Path, default=CSV_DEFAUT, help="CSV d'entrée")
    parser.add_argument("--debut", default="2019-01-01", help="première séance, incluse")
    parser.add_argument("--charniere", default="2024-12-31",
                        help="dernière séance de l'étalonnage, incluse")
    parser.add_argument("--fin", default="2025-12-31", help="dernière séance affichée, incluse")
    parser.add_argument("--fenetres", default=FENETRES, help="longueurs balayées")
    parser.add_argument("--horizons", default=HORIZONS, help="horizons de projection")
    parser.add_argument("--ancrages-min", type=int, default=ANCRAGES_MIN,
                        help="en deçà, le couple (n, h) n'est pas publié")
    parser.add_argument("--prolonger", default="",
                        help="étalonnages supplémentaires : dates de début, "
                             "séparées par des virgules, même charnière")
    parser.add_argument("--sortie", type=Path, default=Path(__file__).resolve().parent,
                        help="répertoire où écrire les SVG")
    parser.add_argument("--table", action="store_true",
                        help="imprimer le relevé sans écrire de figure")
    args = parser.parse_args()

    def entiers(texte, nom, mini):
        try:
            valeurs = sorted({int(v) for v in texte.split(",") if v.strip()})
        except ValueError:
            erreur(f"{nom} : « {texte} » n'est pas une liste d'entiers.")
        if not valeurs or valeurs[0] < mini:
            erreur(f"{nom} : au moins une valeur, et jamais moins de {mini}.")
        return valeurs

    # Une fenêtre a besoin de trois séances (la division par n-2) ; un horizon d'une.
    args.liste_fenetres = entiers(args.fenetres, "--fenetres", 3)
    args.liste_horizons = entiers(args.horizons, "--horizons", 1)
    if not args.debut <= args.charniere <= args.fin:
        erreur("Il faut --debut <= --charniere <= --fin.")

    # Un etalonnage supplementaire partage la charniere : seul son debut recule.
    args.liste_prolonger = [d.strip() for d in args.prolonger.split(",") if d.strip()]
    for date in args.liste_prolonger:
        if not args.debut <= date <= args.charniere:
            erreur(f"--prolonger {date} : hors de [{args.debut}, {args.charniere}].")
    return args


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    args = analyser_arguments()
    if not args.csv.exists():
        erreur(f"CSV introuvable : {args.csv}\n"
               "Le régénérer : python python/import_societe.py MC.PA "
               "--debut 2019-01-01 --fin 2026-09-12")
    jours, closes, divisions = charger(args.csv, args.debut, args.fin)
    controler_scissions(jours, closes, divisions)

    charniere = rang_de(jours, args.charniere)
    if charniere is None:
        erreur(f"--charniere {args.charniere} précède la première séance ({jours[0]}).")
    if charniere + 1 < min(args.liste_fenetres):
        erreur(f"{charniere + 1} séances d'étalonnage, il en faut au moins "
               f"{min(args.liste_fenetres)}.")

    ticker = args.csv.stem.split("_20")[0].replace("_", ".")
    print(f"{ticker} — {len(closes)} séances, du {jours[0]} au {jours[-1]}")
    print(f"  étalonnage       {charniere + 1} séances, du {jours[0]} au {jours[charniere]}")
    if charniere < len(closes) - 1:
        print(f"  hors échantillon {len(closes) - charniere - 1} séances, du "
              f"{jours[charniere + 1]} au {jours[-1]}")
    else:
        print("  hors échantillon aucune séance")

    ajustement, projection = balayer(closes[:charniere + 1], args.liste_fenetres,
                                     args.liste_horizons, args.ancrages_min)
    imprimer_balayage(args.liste_fenetres, args.liste_horizons, ajustement, projection)

    def bande_depuis(i0):
        """La bande ajustée du rang i0 à la charnière, et ce qu'elle donne après."""
        b = ajuster(closes, charniere, charniere - i0 + 1)
        a1, a2, a3 = dedans(b["residus"], b["s"])
        suite = [closes[i] - b["val"] - b["pente"] * (i - charniere)
                 for i in range(charniere + 1, len(closes))]
        h1, h2, h3 = dedans(suite, b["s"]) if suite else (None, None, None)
        b["debut"], b["i0"] = jours[i0], i0
        b["mesures"] = {
            "largeur": 200 * b["s"] / b["val"], "dw": durbin_watson(b["residus"]),
            "a1": a1, "a2": a2, "a3": a3, "h1": h1, "h2": h2, "h3": h3,
            "ecart": (suite[-1] if suite else b["residus"][-1]) / b["s"]}
        return b

    bandes = [bande_depuis(0)]
    for date in args.liste_prolonger:
        i0 = next((i for i, j in enumerate(jours) if j >= date), None)
        if i0 is None or charniere - i0 + 1 < 3:
            erreur(f"--prolonger {date} : moins de 3 séances jusqu'au {jours[charniere]}.")
        bandes.append(bande_depuis(i0))
    for b in bandes:
        imprimer_bande(jours, charniere, b, b["mesures"])

    if args.table:
        return
    # Les deux noms portent l'etalonnage : plusieurs charnieres coexistent dans le
    # meme repertoire, et une figure ne doit jamais en ecraser une autre.
    court = ticker.lower().replace(".", "-")
    base = f"{court}-{jours[0][:4]}-{jours[charniere][:4]}"
    figure_bande(args.sortie / f"{base}-bande.svg",
                 jours, closes, charniere, bandes[0], bandes[0]["mesures"], ticker)
    etendue = f"étalonnage {jours[0]} → {jours[charniere]}, {charniere + 1} séances"
    figure_balayage(args.sortie / f"{base}-largeur-fiable.svg", args.liste_fenetres,
                    args.liste_horizons, projection, ticker, etendue)
    # La figure des prolongements n'a de sens qu'a plusieurs etalonnages, et que
    # s'il reste une zone hors echantillon ou les confronter.
    if len(bandes) > 1 and charniere < len(closes) - 1:
        figure_prolongements(
            args.sortie / f"{court}-prolongements-{jours[charniere + 1][:4]}.svg",
            jours, closes, charniere, bandes, ticker)


if __name__ == "__main__":
    main()
