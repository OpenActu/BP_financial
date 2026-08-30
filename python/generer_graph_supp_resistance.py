#!/usr/bin/env python3
"""
Trace un cours de bourse et son encadrement par support et résistance, en SVG.

Dépendance :
    pandas (installé avec yfinance) — aucune bibliothèque de tracé.

Utilisation :
    python python/generer_graph_supp_resistance.py
    python python/generer_graph_supp_resistance.py --csv chemin/vers/fichier.csv
    python python/generer_graph_supp_resistance.py --bloc 60 --fenetre 60
    python python/generer_graph_supp_resistance.py --sans-blocs --sortie /tmp/airbus.svg

Seule la colonne Close est utilisée. Les droites sont les arêtes de l'enveloppe
convexe des clôtures, sélectionnées par portée minimale — méthode décrite dans
docs/raw/concept/semestre3/encadrement/.
"""

import argparse
import statistics
import sys
from pathlib import Path

import pandas as pd

REPERTOIRE_QUOTES = Path("docs/raw/quotes")
REPERTOIRE_GRAPHS = Path("docs/raw/graphs")
ECART_EPISODE = 3
BLOC_MINIMAL = 40

COULEUR_COURS = "#2a78d6"
COULEUR_RESISTANCE = "#eb6834"
COULEUR_SUPPORT = "#1baf7a"
COULEUR_GRILLE = "#e1e0d9"
COULEUR_AXE = "#c3c2b7"
COULEUR_ENCRE = "#0b0b0b"
COULEUR_ENCRE_2 = "#52514e"
COULEUR_FOND = "#fcfcfb"


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


def analyser(closes, a, b, tolerance):
    """Encadrement de la tranche [a, b[ : deux droites, leurs contacts, les contrôles."""
    m = b - a
    portee_min = max(3, m // 4)
    eps = tolerance * statistics.pstdev(closes[a:b])

    resultat = {"a": a, "b": b, "portee_min": portee_min, "eps": eps}
    for nom, inferieure in (("resistance", False), ("support", True)):
        ch = chaine([(i, closes[i]) for i in range(a, b)], inferieure)
        (x1, y1), (x2, y2) = arete_retenue(ch, portee_min)
        pente = (y2 - y1) / (x2 - x1)
        d = droite((x1, y1), pente)
        contacts = [i for i in range(a, b) if abs(closes[i] - d(i)) <= eps]
        if inferieure:
            traversees = sum(1 for i in range(a, b) if closes[i] < d(i) - 1e-9)
        else:
            traversees = sum(1 for i in range(a, b) if closes[i] > d(i) + 1e-9)
        resultat[nom] = {
            "ancre": (x1, y1),
            "pente": pente,
            "portee": x2 - x1,
            "fin": x2,
            "episodes": episodes(contacts),
            "contacts": contacts,
            "traversees": traversees,
            "d": d,
        }
    return resultat


def svg(dates, closes, blocs, actif, titre, largeur=1200, hauteur=620):
    """Assemble le fichier SVG. Aucune dépendance, aucune police externe."""
    n = len(closes)
    mg, md, mh, mb = 62, 96, 74, 46
    pw, ph = largeur - mg - md, hauteur - mh - mb

    bas = min(closes)
    haut = max(closes)
    for c in [*blocs, actif]:
        if c is None:
            continue
        for nom in ("resistance", "support"):
            d = c[nom]["d"]
            depart = c[nom]["ancre"][0]
            bas = min(bas, d(depart), d(c["b"] - 1))
            haut = max(haut, d(depart), d(c["b"] - 1))
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
            f'fill="{COULEUR_ENCRE}" font-family="Georgia,serif">{titre}</text>'
        ),
        (
            f'<text x="{mg}" y="54" font-size="12" fill="{COULEUR_ENCRE_2}">'
            f"{n} séances · {dates[0]} → {dates[-1]} · clôtures uniquement</text>"
        ),
    ]

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

    for c in blocs:
        for nom, couleur in (("resistance", COULEUR_RESISTANCE), ("support", COULEUR_SUPPORT)):
            d, depart = c[nom]["d"], c[nom]["ancre"][0]
            o.append(
                f'<line x1="{X(depart):.1f}" y1="{Y(d(depart)):.1f}" '
                f'x2="{X(c["b"] - 1):.1f}" y2="{Y(d(c["b"] - 1)):.1f}" '
                f'stroke="{couleur}" stroke-width="1.1" stroke-dasharray="5 4" opacity="0.75"/>'
            )

    chemin = "".join(
        ("L" if i else "M") + f"{X(i):.1f} {Y(closes[i]):.1f}" for i in range(n)
    )
    o.append(
        f'<path d="{chemin}" fill="none" stroke="{COULEUR_COURS}" stroke-width="1.4" '
        f'stroke-linejoin="round"/>'
    )

    if actif is not None:
        for nom, couleur in (("resistance", COULEUR_RESISTANCE), ("support", COULEUR_SUPPORT)):
            b = actif[nom]
            d = b["d"]
            depart = b["ancre"][0]
            o.append(
                f'<line x1="{X(depart):.1f}" y1="{Y(d(depart)):.1f}" '
                f'x2="{X(actif["b"] - 1):.1f}" y2="{Y(d(actif["b"] - 1)):.1f}" '
                f'stroke="{couleur}" stroke-width="2.2"/>'
            )
            for ep in b["episodes"]:
                for i in ep:
                    o.append(
                        f'<circle cx="{X(i):.1f}" cy="{Y(closes[i]):.1f}" r="3" '
                        f'fill="{couleur}" stroke="{COULEUR_FOND}" stroke-width="1.5"/>'
                    )
            o.append(
                f'<text x="{mg + pw + 8}" y="{Y(d(actif["b"] - 1)) + 4:.1f}" font-size="12" '
                f'font-weight="600" fill="{couleur}">{d(actif["b"] - 1):.2f} €</text>'
            )

        a = actif
        lignes = [
            f"canal actif · {dates[a['a']]} → {dates[a['b'] - 1]} · {a['b'] - a['a']} séances",
            (
                f"résistance  pente {a['resistance']['pente']:+.4f} €/séance · "
                f"portée {a['resistance']['portee']} · {len(a['resistance']['episodes'])} épisodes"
            ),
            (
                f"support     pente {a['support']['pente']:+.4f} €/séance · "
                f"portée {a['support']['portee']} · {len(a['support']['episodes'])} épisodes"
            ),
        ]
        for k, texte in enumerate(lignes):
            o.append(
                f'<text x="{mg + 12}" y="{mh + 20 + 15 * k}" font-size="11.5" '
                f'fill="{COULEUR_ENCRE_2}">{texte}</text>'
            )

    legende = [(COULEUR_COURS, "clôture"), (COULEUR_RESISTANCE, "résistance"),
               (COULEUR_SUPPORT, "support")]
    for k, (couleur, texte) in enumerate(legende):
        x = mg + k * 150
        o.append(
            f'<line x1="{x}" y1="{hauteur - 16}" x2="{x + 22}" y2="{hauteur - 16}" '
            f'stroke="{couleur}" stroke-width="2.2"/>'
        )
        o.append(
            f'<text x="{x + 30}" y="{hauteur - 12}" font-size="12" '
            f'fill="{COULEUR_ENCRE_2}">{texte}</text>'
        )
    o.append(
        f'<text x="{mg + pw}" y="{hauteur - 12}" text-anchor="end" font-size="11" '
        f'fill="{COULEUR_ENCRE_2}">trait plein : canal actif · pointillé : par bloc</text>'
    )

    o.append("</svg>")
    return "\n".join(o)


def main():
    parser = argparse.ArgumentParser(
        description="Trace un cours et son encadrement support/résistance en SVG "
        "(clôtures uniquement)."
    )
    parser.add_argument("--csv", help="CSV d'entrée (défaut : le plus récent de docs/raw/quotes/)")
    parser.add_argument("--bloc", type=int, default=120, help="Longueur des blocs (défaut : 120)")
    parser.add_argument(
        "--fenetre", type=int, default=120, help="Fenêtre active ancrée à droite (défaut : 120)"
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.25,
        help="Tolérance de contact, en multiples de l'écart-type (défaut : 0.25)",
    )
    parser.add_argument(
        "--sans-blocs", action="store_true", help="Ne tracer que le canal actif"
    )
    parser.add_argument("--sortie", help="Chemin du SVG produit")
    parser.add_argument("--titre", help="Titre inscrit dans le graphique")
    args = parser.parse_args()

    if args.csv:
        chemin_csv = Path(args.csv)
    else:
        candidats = sorted(
            REPERTOIRE_QUOTES.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True
        )
        if not candidats:
            print(f"Aucun CSV dans {REPERTOIRE_QUOTES}/.", file=sys.stderr)
            sys.exit(1)
        chemin_csv = candidats[0]

    if not chemin_csv.exists():
        print(f"CSV introuvable : {chemin_csv}", file=sys.stderr)
        sys.exit(1)

    brut = pd.read_csv(chemin_csv)
    if "Close" not in brut.columns or "Date" not in brut.columns:
        print(f"{chemin_csv} : colonnes Date et Close attendues.", file=sys.stderr)
        sys.exit(1)

    closes = [float(x) for x in brut["Close"]]
    dates = [str(x)[:10] for x in brut["Date"]]
    n = len(closes)
    if n < args.bloc:
        print(
            f"{n} séances : moins que la longueur de bloc ({args.bloc}).", file=sys.stderr
        )
        sys.exit(1)

    bornes = [(s, min(s + args.bloc, n)) for s in range(0, n, args.bloc)]
    if len(bornes) > 1 and bornes[-1][1] - bornes[-1][0] < BLOC_MINIMAL:
        bornes[-2] = (bornes[-2][0], bornes[-1][1])
        bornes.pop()
    blocs = [analyser(closes, a, b, args.tolerance) for a, b in bornes]
    actif = analyser(closes, max(0, n - args.fenetre), n, args.tolerance)

    traversees = sum(
        c[nom]["traversees"] for c in [*blocs, actif] for nom in ("resistance", "support")
    )
    if traversees:
        print(
            f"Contrôle de non-traversée en échec : {traversees} clôture(s) du mauvais "
            "côté d'une droite retenue.",
            file=sys.stderr,
        )
        sys.exit(2)

    # « AIR_PA_2020-01-02_2023-12-29 » -> « AIR.PA »
    tete = chemin_csv.stem.split("_2")[0]
    titre = args.titre or tete.replace("_", ".")
    contenu = svg(dates, closes, [] if args.sans_blocs else blocs, actif, titre)

    if args.sortie:
        chemin_svg = Path(args.sortie)
    else:
        chemin_svg = REPERTOIRE_GRAPHS / f"{chemin_csv.stem}_supp_resistance.svg"
    chemin_svg.parent.mkdir(parents=True, exist_ok=True)
    chemin_svg.write_text(contenu, encoding="utf-8")

    print(f"\n{titre} — {n} séances, du {dates[0]} au {dates[-1]}")
    print(
        f"Blocs : {len(bornes)} de {args.bloc} séances "
        f"(portée minimale {blocs[0]['portee_min']})"
    )
    print(
        f"\nCANAL ACTIF — {dates[actif['a']]} → {dates[actif['b'] - 1]} "
        f"({actif['b'] - actif['a']} séances, ε = {actif['eps']:.2f} €)"
    )
    dernier = actif["b"] - 1
    for nom in ("resistance", "support"):
        b = actif[nom]
        print(
            f"  {nom:<11} pente {b['pente']:+.4f} €/séance  portée {b['portee']:>3}  "
            f"épisodes {len(b['episodes'])}  → {b['d'](dernier):.2f} €"
        )
    haut = actif["resistance"]["d"](dernier)
    bas = actif["support"]["d"](dernier)
    largeur = haut - bas
    position = 100 * (closes[dernier] - bas) / largeur if largeur else float("nan")
    print(
        f"  clôture {closes[dernier]:.2f} €  |  position dans le canal {position:.0f} %"
        f"  |  largeur {largeur:.2f} € ({100 * largeur / closes[dernier]:.1f} %)"
    )
    for nom, valeur in (("la résistance", haut), ("le support", bas)):
        if abs(closes[dernier] - valeur) < actif["eps"] / 10:
            print(
                f"  ⚠ {nom} passe exactement par la dernière clôture : la dernière "
                "séance est toujours un sommet de l'enveloppe, cet écart nul est "
                "géométrique et non informatif."
            )
    print(f"\nGraphique écrit dans : {chemin_svg}")


if __name__ == "__main__":
    main()
