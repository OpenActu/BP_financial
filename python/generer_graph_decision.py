#!/usr/bin/env python3
"""
Trace la figure de décision du cours trading : cours, encadrement actif, séance
de décision, les cinq critères et le verdict de la règle — en SVG.

Dépendances :
    pandas (installé avec yfinance) et p_valeur_student() de import_societe.py.
    Aucune bibliothèque de tracé, aucun scipy.

Utilisation :
    python python/generer_graph_decision.py
    python python/generer_graph_decision.py --csv docs/raw/quotes/AIR_PA_2019-01-02_2020-12-31.csv \
                                            --indice docs/raw/quotes/^FCHI_2019-01-02_2020-12-31.csv
    python python/generer_graph_decision.py --date 2020-12-31 --fenetre 120
    python python/generer_graph_decision.py --sans-indice --sortie /tmp/decision.svg

Les chaînes sont construites sur High et Low, comme les modules du cours
encadrement — et non sur Close comme generer_graph_supp_resistance.py.

Le verdict affiché est la sortie d'une règle écrite à l'avance appliquée à des
données passées. Ce n'est pas une recommandation d'investissement.
"""

import argparse
import math
import statistics
import sys
from pathlib import Path

import pandas as pd

REPERTOIRE_QUOTES = Path("docs/raw/quotes")
REPERTOIRE_GRAPHS = Path("docs/raw/graphs")
ECART_EPISODE = 3
JOURS_AN = 252
SEUIL_ACHAT = 35
SEUIL_VENTE = 65
TAU_MINIMAL = 20
EPISODES_MINIMAUX = 3
HISTORIQUE_MINIMAL = 120

COULEUR_COURS = "#2a78d6"
COULEUR_RESISTANCE = "#eb6834"
COULEUR_SUPPORT = "#1baf7a"
COULEUR_GRILLE = "#e1e0d9"
COULEUR_AXE = "#c3c2b7"
COULEUR_ENCRE = "#0b0b0b"
COULEUR_ENCRE_2 = "#52514e"
COULEUR_FOND = "#fcfcfb"
COULEUR_FENETRE = "#f2efe4"
COULEUR_DECISION = "#8b5cd6"
COULEUR_VERDICT = "#5c6670"


def esc(texte):
    """Échappe les caractères réservés du XML."""
    return (
        str(texte).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def fr(x, decimales=2):
    """Nombre au format français : virgule décimale, espace fine des milliers."""
    return f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")


def signe(x, decimales=2):
    """Nombre au format français, signe toujours explicite."""
    return ("+" if x >= 0 else "") + fr(x, decimales)


def chaine(points, inferieure=True):
    """Chaîne inférieure (support) ou supérieure (résistance) de l'enveloppe convexe.

    points : liste de couples (rang de séance, prix). Balayage de Andrew.
    """
    s = 1 if inferieure else -1
    pile = []
    for p in sorted(points):
        while len(pile) >= 2:
            (x1, y1), (x2, y2) = pile[-2], pile[-1]
            # produit vectoriel : on dépile tant que le dernier sommet
            # n'est plus extrémal une fois p connu
            if s * ((x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)) < 0:
                pile.pop()
            else:
                break
        pile.append(p)
    return pile


def arete_retenue(ch, portee_min):
    """Dernière arête dont la portée atteint portee_min, en remontant la chaîne."""
    for k in range(len(ch) - 2, -1, -1):
        if ch[k + 1][0] - ch[k][0] >= portee_min:
            return ch[k], ch[k + 1]
    return ch[0], ch[-1]


def episodes(indices, ecart=ECART_EPISODE):
    """Regroupe les séances de contact distantes de moins de `ecart` en un contact."""
    if not indices:
        return []
    groupes, courant = [], [indices[0]]
    for i in indices[1:]:
        if i - courant[-1] < ecart:
            courant.append(i)
        else:
            groupes.append(courant)
            courant = [i]
    groupes.append(courant)
    return groupes


def droite(ancre, pente):
    x1, y1 = ancre
    return lambda t: y1 + pente * (t - x1)


def quantile_student(ddl, niveau=0.975):
    """Quantile de Student par dichotomie sur p_valeur_student().

    p_valeur_student rend la p-valeur bilatérale ; le quantile bilatéral de
    niveau `niveau` est le t tel que p(t) = 2 * (1 - niveau).

    Import local : le dépôt n'a pas de structure de paquet, il faut donc ajouter
    le répertoire du script au chemin avant d'importer son voisin.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from import_societe import p_valeur_student

    cible = 2 * (1 - niveau)
    bas, haut = 0.0, 100.0
    for _ in range(80):
        milieu = (bas + haut) / 2
        if p_valeur_student(milieu, ddl) > cible:
            bas = milieu
        else:
            haut = milieu
    return (bas + haut) / 2


def encadrement(hauts, bas, closes, a, b, tolerance):
    """Encadrement de la tranche [a, b[ : deux droites, leurs contacts, les contrôles.

    Résistance sur les High (chaîne supérieure), support sur les Low (chaîne
    inférieure) — la convention des modules du cours encadrement.
    """
    m = b - a
    portee_min = max(3, m // 4)
    eps = tolerance * statistics.pstdev(closes[a:b])

    resultat = {"a": a, "b": b, "portee_min": portee_min, "eps": eps}
    for nom, inferieure, serie in (
        ("resistance", False, hauts),
        ("support", True, bas),
    ):
        ch = chaine([(i, serie[i]) for i in range(a, b)], inferieure)
        (x1, y1), (x2, y2) = arete_retenue(ch, portee_min)
        pente = (y2 - y1) / (x2 - x1)
        d = droite((x1, y1), pente)
        # les contacts se comptent sur la série qui a construit la droite —
        # sur Close, le comptage s'effondre (voir le miroir, § 3)
        contacts = [i for i in range(a, b) if abs(serie[i] - d(i)) <= eps]
        if inferieure:
            traversees = sum(1 for i in range(a, b) if serie[i] < d(i) - 1e-9)
        else:
            traversees = sum(1 for i in range(a, b) if serie[i] > d(i) + 1e-9)
        resultat[nom] = {
            "ancre": (x1, y1),
            "pente": pente,
            "portee": x2 - x1,
            "episodes": episodes(contacts),
            "points": {i: serie[i] for i in contacts},
            "traversees": traversees,
            "d": d,
        }
    return resultat


def alpha_beta(dates_v, closes_v, dates_i, closes_i):
    """Régression des rendements de la valeur sur ceux de l'indice, dates communes.

    Rend alpha et beta quotidiens, l'alpha annualisé, son IC95 annualisé, R² et
    le nombre de rendements. Taux sans risque nul.
    """
    serie_v = dict(zip(dates_v, closes_v))
    serie_i = dict(zip(dates_i, closes_i))
    communes = sorted(set(serie_v) & set(serie_i))
    if len(communes) < 3:
        return None

    ri = [serie_v[communes[k]] / serie_v[communes[k - 1]] - 1 for k in range(1, len(communes))]
    rm = [serie_i[communes[k]] / serie_i[communes[k - 1]] - 1 for k in range(1, len(communes))]
    n = len(ri)

    e_i, e_m = statistics.fmean(ri), statistics.fmean(rm)
    var_m = statistics.pvariance(rm, e_m)
    cov = sum((x - e_m) * (y - e_i) for x, y in zip(rm, ri)) / n
    beta = cov / var_m
    alpha = e_i - beta * e_m

    residus = [y - (alpha + beta * x) for x, y in zip(rm, ri)]
    sce = sum(r * r for r in residus)
    s = math.sqrt(sce / (n - 2))
    se_alpha = s * math.sqrt(1 / n + e_m**2 / (n * var_m))
    se_beta = s / math.sqrt(n * var_m)

    t = quantile_student(n - 2, 0.975)
    alpha_an = JOURS_AN * alpha
    se_an = JOURS_AN * se_alpha
    var_i = statistics.pvariance(ri, e_i)

    return {
        "n": n,
        "dates_communes": len(communes),
        "beta": beta,
        "t_beta": (beta - 1) / se_beta,
        "alpha_an": alpha_an * 100,
        "ic_bas": (alpha_an - t * se_an) * 100,
        "ic_haut": (alpha_an + t * se_an) * 100,
        "r2": cov**2 / (var_m * var_i) if var_i else 0.0,
        "vol_residuelle": s * math.sqrt(JOURS_AN) * 100,
    }


def verdict(criteres, vetos):
    """Applique la règle du module 3 : les vetos d'abord, les conditions ensuite."""
    if vetos:
        return "ATTENTE", ["veto déclenché"]

    c1, c2 = criteres["tend_120"], criteres["tend_20"]
    position, momentum, alpha = criteres["position"], criteres["momentum"], criteres["alpha"]
    ic_haut = alpha["ic_haut"] if alpha else None

    manquantes = []
    if not (c1 == 1 and c2 == 1):
        manquantes.append("tendances non toutes deux à +1")
    if position is None or position >= SEUIL_ACHAT:
        manquantes.append(f"position ≥ {SEUIL_ACHAT} %")
    if momentum is None or momentum <= 0:
        manquantes.append("momentum 12-1 non positif")
    if ic_haut is None or ic_haut <= 0:
        manquantes.append("borne haute de l'IC de l'alpha non calculée ou ≤ 0")
    if not manquantes:
        return "ACHAT", []

    manquantes_vente = []
    if not (c1 == -1 and c2 == -1):
        manquantes_vente.append("tendances non toutes deux à -1")
    if position is None or position <= SEUIL_VENTE:
        manquantes_vente.append(f"position ≤ {SEUIL_VENTE} %")
    if momentum is None or momentum >= 0:
        manquantes_vente.append("momentum 12-1 non négatif")
    if not manquantes_vente:
        return "VENTE", []

    return "ATTENTE", manquantes + manquantes_vente


def svg(dates, closes, actif, criteres, mot, vetos, meta, titre, largeur=1200, hauteur=700):
    """Assemble le fichier SVG. Aucune dépendance, aucune police externe."""
    n = len(closes)
    mg, md, mh = 62, 96, 74
    pw, ph = largeur - mg - md, 340

    bas, haut = min(closes), max(closes)
    for nom in ("resistance", "support"):
        d = actif[nom]["d"]
        # seuls les segments réellement tracés comptent : de l'ancre à la
        # décision. Prolonger vers la gauche plongerait l'échelle très bas.
        for t in (actif[nom]["ancre"][0], n - 1):
            bas, haut = min(bas, d(t)), max(haut, d(t))
    y0 = (int(bas) // 20) * 20
    y1 = -(-int(haut + 1) // 20) * 20

    def X(i):
        return mg + (i / (n - 1)) * pw

    def Y(v):
        return mh + ph - ((v - y0) / (y1 - y0)) * ph

    o = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
            f'width="{largeur}" height="{hauteur}" font-family="ui-monospace,Consolas,monospace">'
        ),
        f'<rect width="{largeur}" height="{hauteur}" fill="{COULEUR_FOND}"/>',
        (
            f'<text x="{mg}" y="34" font-size="19" font-weight="600" '
            f'fill="{COULEUR_ENCRE}" font-family="Georgia,serif">{esc(titre)}</text>'
        ),
        f'<text x="{mg}" y="54" font-size="12" fill="{COULEUR_ENCRE_2}">{esc(meta)}</text>',
    ]

    o.append(
        f'<rect x="{X(actif["a"]):.1f}" y="{mh}" width="{X(n - 1) - X(actif["a"]):.1f}" '
        f'height="{ph}" fill="{COULEUR_FENETRE}"/>'
    )
    for v in range(y0, y1 + 1, 20):
        yy = Y(v)
        o.append(
            f'<line x1="{mg}" y1="{yy:.1f}" x2="{mg + pw}" y2="{yy:.1f}" '
            f'stroke="{COULEUR_GRILLE}" stroke-width="1"/>'
        )
        o.append(
            f'<text x="{mg - 10}" y="{yy + 4:.1f}" text-anchor="end" font-size="11" '
            f'fill="{COULEUR_ENCRE_2}">{v}</text>'
        )
    for i in range(1, n):
        if dates[i][:4] != dates[i - 1][:4]:
            xx = X(i)
            o.append(
                f'<line x1="{xx:.1f}" y1="{mh}" x2="{xx:.1f}" y2="{mh + ph}" '
                f'stroke="{COULEUR_GRILLE}" stroke-width="1"/>'
            )
            o.append(
                f'<text x="{xx:.1f}" y="{mh + ph + 20}" text-anchor="middle" '
                f'font-size="11" fill="{COULEUR_ENCRE_2}">{dates[i][:4]}</text>'
            )
    o.append(
        f'<line x1="{mg}" y1="{mh + ph}" x2="{mg + pw}" y2="{mh + ph}" '
        f'stroke="{COULEUR_AXE}" stroke-width="1"/>'
    )
    o.append(
        f'<text x="{X(actif["a"]) + 6:.1f}" y="{mh + 16}" font-size="11" '
        f'fill="{COULEUR_ENCRE_2}">fenêtre active · {actif["b"] - actif["a"]} séances</text>'
    )

    chemin = "".join(
        ("L" if i else "M") + f"{X(i):.1f} {Y(closes[i]):.1f}" for i in range(n)
    )
    o.append(
        f'<path d="{chemin}" fill="none" stroke="{COULEUR_COURS}" stroke-width="1.4" '
        f'stroke-linejoin="round"/>'
    )

    for nom, couleur in (("resistance", COULEUR_RESISTANCE), ("support", COULEUR_SUPPORT)):
        b = actif[nom]
        d, depart = b["d"], b["ancre"][0]
        o.append(
            f'<line x1="{X(depart):.1f}" y1="{Y(d(depart)):.1f}" '
            f'x2="{X(n - 1):.1f}" y2="{Y(d(n - 1)):.1f}" '
            f'stroke="{couleur}" stroke-width="2.2"/>'
        )
        for ep in b["episodes"]:
            for i in ep:
                o.append(
                    f'<circle cx="{X(i):.1f}" cy="{Y(b["points"][i]):.1f}" r="3" '
                    f'fill="{couleur}" stroke="{COULEUR_FOND}" stroke-width="1.5"/>'
                )
        o.append(
            f'<text x="{mg + pw + 8}" y="{Y(d(n - 1)) + 4:.1f}" font-size="12" '
            f'font-weight="600" fill="{couleur}">{fr(d(n - 1))} €</text>'
        )

    o.append(
        f'<line x1="{X(n - 1):.1f}" y1="{mh}" x2="{X(n - 1):.1f}" y2="{mh + ph}" '
        f'stroke="{COULEUR_DECISION}" stroke-width="1.2" stroke-dasharray="4 3"/>'
    )
    o.append(
        f'<circle cx="{X(n - 1):.1f}" cy="{Y(closes[-1]):.1f}" r="4.5" '
        f'fill="{COULEUR_DECISION}" stroke="{COULEUR_FOND}" stroke-width="1.8"/>'
    )
    # étiquette en haut à droite : à côté du disque, les deux droites la traversent
    o.append(
        f'<text x="{X(n - 1) - 8:.1f}" y="{mh + 34}" text-anchor="end" '
        f'font-size="12" font-weight="600" fill="{COULEUR_DECISION}">'
        f'décision {dates[-1]} · {fr(closes[-1])} €</text>'
    )

    y = mh + ph + 62
    o.append(
        f'<text x="{mg}" y="{y}" font-size="12.5" font-weight="600" '
        f'fill="{COULEUR_ENCRE}">Les cinq critères</text>'
    )
    for k, (num, libelle, valeur, sens) in enumerate(criteres):
        yy = y + 24 + 21 * k
        pastille = {"achat": "↑", "vente": "↓", "neutre": "–"}[sens]
        couleur = {
            "achat": COULEUR_SUPPORT,
            "vente": COULEUR_RESISTANCE,
            "neutre": COULEUR_ENCRE_2,
        }[sens]
        o.append(
            f'<text x="{mg}" y="{yy}" font-size="12" fill="{COULEUR_ENCRE_2}">{num}</text>'
        )
        o.append(
            f'<text x="{mg + 26}" y="{yy}" font-size="12" fill="{COULEUR_ENCRE_2}">'
            f"{esc(libelle)}</text>"
        )
        o.append(
            f'<text x="{mg + 300}" y="{yy}" font-size="12.5" font-weight="600" '
            f'fill="{COULEUR_ENCRE}">{esc(valeur)}</text>'
        )
        o.append(
            f'<text x="{mg + pw}" y="{yy}" text-anchor="end" font-size="13" '
            f'fill="{couleur}">{pastille}</text>'
        )

    yb = hauteur - 74
    o.append(
        f'<rect x="{mg}" y="{yb}" width="{pw}" height="40" rx="4" '
        f'fill="{COULEUR_VERDICT}" opacity="0.09"/>'
    )
    o.append(
        f'<text x="{mg + 14}" y="{yb + 26}" font-size="17" font-weight="700" '
        f'fill="{COULEUR_VERDICT}" font-family="Georgia,serif">{mot}</text>'
    )
    motif = " · ".join(vetos) if vetos else "aucun veto ; conditions non réunies"
    o.append(
        f'<text x="{mg + 120}" y="{yb + 26}" font-size="12" fill="{COULEUR_ENCRE_2}">'
        f"{esc(motif)}</text>"
    )
    o.append(
        f'<text x="{mg}" y="{hauteur - 16}" font-size="11" fill="{COULEUR_ENCRE_2}">'
        f"Sortie d'une règle écrite à l'avance appliquée à des données passées. "
        f"Ni prédiction, ni recommandation d'investissement.</text>"
    )

    o.append("</svg>")
    return "\n".join(o)


def charger(chemin, colonnes):
    """Lit un CSV de docs/raw/quotes/ et rend (dates AAAA-MM-JJ, colonnes demandées)."""
    try:
        df = pd.read_csv(chemin)
    except OSError:
        print(f"Fichier introuvable : {chemin}", file=sys.stderr)
        sys.exit(1)
    df.columns = [str(c) for c in df.columns]
    colonne_date = df.columns[0]
    manquantes = [c for c in colonnes if c not in df.columns]
    if manquantes:
        print(f"Colonnes absentes de {chemin} : {', '.join(manquantes)}", file=sys.stderr)
        sys.exit(1)
    dates = [str(v)[:10] for v in df[colonne_date]]
    return dates, {c: list(df[c]) for c in colonnes}


def main():
    parser = argparse.ArgumentParser(
        description="Trace la figure de décision du cours trading : encadrement actif, "
        "cinq critères et verdict de la règle."
    )
    parser.add_argument("--csv", help="CSV de la valeur (défaut : le plus récent de docs/raw/quotes/)")
    parser.add_argument("--indice", help="CSV de l'indice de référence, pour le critère 4")
    parser.add_argument("--sans-indice", action="store_true", help="Ne pas calculer le critère 4")
    parser.add_argument("--date", help="Séance de décision AAAA-MM-JJ (défaut : dernière séance)")
    parser.add_argument("--fenetre", type=int, default=120, help="Fenêtre active (défaut : 120)")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.25,
        help="Tolérance de contact, en multiples de l'écart-type (défaut : 0.25)",
    )
    parser.add_argument("--sortie", help="Chemin du SVG produit")
    parser.add_argument("--titre", help="Titre inscrit dans le SVG")
    args = parser.parse_args()

    if args.indice and args.sans_indice:
        print("--indice et --sans-indice sont incompatibles.", file=sys.stderr)
        sys.exit(1)

    if args.csv:
        chemin_csv = Path(args.csv)
    else:
        candidats = [p for p in REPERTOIRE_QUOTES.glob("*.csv") if not p.name.startswith("^")]
        if not candidats:
            print("Aucun CSV de valeur dans docs/raw/quotes/.", file=sys.stderr)
            sys.exit(1)
        chemin_csv = max(candidats, key=lambda p: p.stat().st_mtime)

    dates, cols = charger(chemin_csv, ["High", "Low", "Close", "TEND_20", "TEND_120"])

    fin = len(dates) - 1
    ferie = None
    if args.date:
        eligibles = [k for k, d in enumerate(dates) if d <= args.date]
        if not eligibles:
            print(f"Aucune séance avant ou au {args.date}.", file=sys.stderr)
            sys.exit(1)
        fin = eligibles[-1]
        if dates[fin] != args.date:
            ferie = args.date
            print(f"Le {args.date} n'est pas une séance ; décision au {dates[fin]}.")

    dates = dates[: fin + 1]
    hauts = [float(v) for v in cols["High"][: fin + 1]]
    bas = [float(v) for v in cols["Low"][: fin + 1]]
    closes = [float(v) for v in cols["Close"][: fin + 1]]
    n = len(closes)

    if n < args.fenetre:
        print(f"Historique de {n} séances, plus court que la fenêtre {args.fenetre}.", file=sys.stderr)
        sys.exit(1)

    actif = encadrement(hauts, bas, closes, n - args.fenetre, n, args.tolerance)
    for nom in ("resistance", "support"):
        if actif[nom]["traversees"]:
            print(
                f"Contrôle de non-traversée en échec : {actif[nom]['traversees']} "
                f"séances du mauvais côté de la {nom}.",
                file=sys.stderr,
            )
            sys.exit(2)

    def lire_tendance(colonne):
        v = cols[colonne][fin]
        return 0 if pd.isna(v) else int(v)

    tend_120, tend_20 = lire_tendance("TEND_120"), lire_tendance("TEND_20")
    r_fin = actif["resistance"]["d"](n - 1)
    s_fin = actif["support"]["d"](n - 1)
    largeur_canal = r_fin - s_fin
    position = 100 * (closes[-1] - s_fin) / largeur_canal

    momentum = None
    if n >= JOURS_AN + 1 + 21:
        momentum = 100 * (closes[-22] / closes[-JOURS_AN - 1] - 1)

    alpha = None
    if args.indice:
        dates_i, cols_i = charger(Path(args.indice), ["Close"])
        alpha = alpha_beta(dates, closes, dates_i, [float(v) for v in cols_i["Close"]])
        if alpha is None:
            print("Aucune date commune avec l'indice ; critère 4 non calculé.", file=sys.stderr)

    ecart_pentes = actif["support"]["pente"] - actif["resistance"]["pente"]
    tau = largeur_canal / ecart_pentes if ecart_pentes > 0 else float("inf")

    vetos = []
    if min(len(actif["resistance"]["episodes"]), len(actif["support"]["episodes"])) < EPISODES_MINIMAUX:
        vetos.append(f"veto 1 : moins de {EPISODES_MINIMAUX} épisodes de contact d'un côté")
    if tau < TAU_MINIMAL:
        vetos.append(f"veto 2 : canal se refermant en {tau:.1f} séances")
    if tend_120 * tend_20 < 0:
        vetos.append("veto 3 : critères 1 et 2 de signes opposés")
    if n < HISTORIQUE_MINIMAL:
        vetos.append(f"veto 4 : historique de {n} séances")

    mot, manquantes = verdict(
        {"tend_120": tend_120, "tend_20": tend_20, "position": position,
         "momentum": momentum, "alpha": alpha},
        vetos,
    )

    def sens(valeur_achat, valeur_vente):
        return "achat" if valeur_achat else ("vente" if valeur_vente else "neutre")

    texte_alpha = "non calculé"
    if alpha:
        zero = alpha["ic_bas"] <= 0 <= alpha["ic_haut"]
        texte_alpha = (
            f"{signe(alpha['alpha_an'])} %/an · IC95 [{signe(alpha['ic_bas'])} ; {signe(alpha['ic_haut'])}] %"
            + (" · indiscernable de zéro" if zero else "")
        )
    texte_position = f"{fr(position, 1)} % de la hauteur" + (
        " · hors canal" if position < 0 or position > 100 else ""
    )
    lignes_criteres = [
        ("1", "tendance longue — TEND_120", f"{tend_120:+d}", sens(tend_120 > 0, tend_120 < 0)),
        ("2", "tendance courte — TEND_20", f"{tend_20:+d}", sens(tend_20 > 0, tend_20 < 0)),
        ("3", "position dans l'encadrement actif", texte_position,
         sens(position < SEUIL_ACHAT, position > SEUIL_VENTE)),
        ("4", "alpha annualisé contre l'indice", texte_alpha,
         sens(bool(alpha) and alpha["ic_haut"] > 0, False)),
        ("5", "momentum 12-1", "non calculé" if momentum is None else f"{signe(momentum)} %",
         sens(momentum is not None and momentum > 0, momentum is not None and momentum < 0)),
    ]

    ticker = chemin_csv.stem.split("_20")[0].replace("_", ".")
    titre = args.titre or f"{ticker} — les cinq critères au {dates[-1]}"
    meta = (
        f"{n} séances · {dates[0]} → {dates[-1]} · fenêtre active {dates[actif['a']]} "
        f"→ {dates[-1]} · ε = {fr(actif['eps'])} €"
        + (f" · décision demandée au {ferie}, jour non coté" if ferie else "")
    )
    sortie = Path(args.sortie) if args.sortie else REPERTOIRE_GRAPHS / f"{chemin_csv.stem}_decision.svg"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(
        svg(dates, closes, actif, lignes_criteres, mot, vetos, meta, titre),
        encoding="utf-8",
    )

    print(f"Valeur           : {ticker} ({n} séances, {dates[0]} → {dates[-1]})")
    print(f"Décision         : {dates[-1]}")
    print(
        f"Fenêtre active   : {dates[actif['a']]} → {dates[-1]} "
        f"({actif['b'] - actif['a']} séances, ε = {fr(actif['eps'])} €)"
    )
    for nom, valeur in (("Résistance", r_fin), ("Support", s_fin)):
        b = actif[nom.lower().replace("é", "e")]
        print(
            f"{nom:<17}: pente {'+' if b['pente'] >= 0 else ''}{fr(b['pente'], 4)} €/séance · portée {b['portee']} · "
            f"{len(b['episodes'])} épisodes · {fr(valeur)} €"
        )
    print(f"Largeur          : {fr(largeur_canal)} € ({fr(100 * largeur_canal / closes[-1], 1)} %)"
          f" · τ = {'∞' if tau == float('inf') else fr(tau, 1)} séances")
    print()
    for num, libelle, valeur, _ in lignes_criteres:
        print(f"Critère {num}  {libelle:<34}: {valeur}")
    print()
    print(f"Vetos            : {'; '.join(vetos) if vetos else 'aucun'}")
    if not vetos and manquantes:
        print(f"Conditions       : {'; '.join(manquantes)}")
    print(f"VERDICT          : {mot}")
    print()
    print("Sortie d'une règle écrite à l'avance, pas une recommandation.")
    print(f"Graphique écrit dans : {sortie}")


if __name__ == "__main__":
    main()
