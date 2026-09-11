#!/usr/bin/env python3
"""
Trace la figure du § 4.2 du cours d'algèbre, en SVG : Vect(u, v) dans R^3.

Dépendance :
    aucune — la projection et le tracé sont en Python pur.

Utilisation :
    python docs/raw/concept/semestre1/algebre/figures/generer_figures.py
    python docs/raw/concept/semestre1/algebre/figures/generer_figures.py --sortie /tmp

Deux panneaux, le MÊME u. À gauche, v n'est pas colinéaire à u : Vect(u, v) est
un plan. À droite, v = -1,5 u : Vect(u, v) n'est plus que la droite Vect(u). Les
points tracés sont, dans les deux panneaux, les mêmes neuf combinaisons
λu + μv, λ et μ parcourant {-1, 0, 1} — seul v change.

Le miroir d'exécution est dans generer_figures.md.
"""

import argparse
import math
from pathlib import Path

U = (0.0, 2.0, 1.0)
V_LIBRE = (1.0, -1.0, 2.0)
K_COLINEAIRE = -1.5
COEFFICIENTS = (-1, 0, 1)
BORD = 1.5          # morceau de plan tracé : λ, μ dans [-BORD, BORD]
DEMI_DROITE = 2.9   # morceau de droite tracé : t u, t dans [-DEMI_DROITE, DEMI_DROITE]
AXE_LONGUEUR = 3.0

AZIMUT = math.radians(30)
ELEVATION = math.radians(25)
ECHELLE = 54        # pixels par unité

L, H = 1200, 650
CY = 372
CX_GAUCHE, CX_DROITE = 300, 900

VECT_U = "#2a78d6"
VECT_V = "#eb6834"
SOUS_ESPACE = "#8b5cd6"
AXE = "#a9a89e"
GRILLE = "#e1e0d9"
ENCRE = "#0b0b0b"
ENCRE2 = "#52514e"
FOND = "#fcfcfb"


# --- Algèbre ------------------------------------------------------------------


def combinaison(lam, a, mu, b):
    return tuple(lam * x + mu * y for x, y in zip(a, b, strict=True))


def scalaire(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def vectoriel(a, b):
    return (a[1] * b[2] - a[2] * b[1] + 0.0, a[2] * b[0] - a[0] * b[2] + 0.0,
            a[0] * b[1] - a[1] * b[0] + 0.0)


def rang(a, b):
    """Dimension de Vect(a, b) : 2 si le produit vectoriel est non nul, sinon 1 si l'un
    des deux est non nul, sinon 0."""
    if any(abs(c) > 1e-12 for c in vectoriel(a, b)):
        return 2
    return 1 if any(abs(c) > 1e-12 for c in (*a, *b)) else 0


def distincts(a, b):
    """Nombre de points distincts parmi les combinaisons λa + μb, λ, μ ∈ COEFFICIENTS."""
    return len({tuple(round(c, 9) + 0.0 for c in combinaison(lam, a, mu, b))
                for lam in COEFFICIENTS for mu in COEFFICIENTS})


# --- Projection ---------------------------------------------------------------


def vers_camera():
    """Vecteur unitaire pointant de l'origine vers l'observateur."""
    return (math.cos(ELEVATION) * math.cos(AZIMUT), math.cos(ELEVATION) * math.sin(AZIMUT),
            math.sin(ELEVATION))


def ecran(p, cx):
    """Projection orthographique de R^3 sur l'écran, l'origine en (cx, CY)."""
    sa, ca = math.sin(AZIMUT), math.cos(AZIMUT)
    se, ce = math.sin(ELEVATION), math.cos(ELEVATION)
    x = -sa * p[0] + ca * p[1]
    y = -ca * se * p[0] - sa * se * p[1] + ce * p[2]
    return cx + ECHELLE * x, CY - ECHELLE * y


# --- Primitives de tracé ------------------------------------------------------


def nombre(x):
    """Virgule décimale, et le trait d'union remplacé par le vrai signe moins (U+2212)."""
    return f"{x:g}".replace(".", ",").replace("-", "−")


def texte(x, y, contenu, taille=12, couleur=ENCRE2, ancre="start", gras=False,
          serif=False, italique=False):
    attributs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-size="{taille}"', f'fill="{couleur}"']
    if ancre != "start":
        attributs.append(f'text-anchor="{ancre}"')
    if gras:
        attributs.append('font-weight="600"')
    if serif:
        attributs.append('font-family="Georgia,serif"')
    if italique:
        attributs.append('font-style="italic"')
    return f'<text {" ".join(attributs)}>{contenu}</text>'


def segment(p0, p1, couleur, largeur=1.0, tirets=None, opacite=1.0):
    dash = f' stroke-dasharray="{tirets}"' if tirets else ""
    return (f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
            f'stroke="{couleur}" stroke-width="{largeur}" opacity="{opacite}"{dash}/>')


def fleche(p0, p1, couleur, largeur=2.6, pointe=14):
    """Un vecteur de p0 à p1 ; la pointe est un triangle, sans <marker>."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    bx, by = p1[0] - pointe * ux, p1[1] - pointe * uy
    tri = [p1, (bx - 5.5 * uy, by + 5.5 * ux), (bx + 5.5 * uy, by - 5.5 * ux)]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in tri)
    return [segment(p0, (bx, by), couleur, largeur),
            f'<polygon points="{pts}" fill="{couleur}"/>']


def nom_vecteur(p0, p1, nom, couleur, recul=19):
    """Le nom d'un vecteur, posé dans son prolongement, au-delà de la pointe."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = math.hypot(dx, dy)
    return texte(p1[0] + recul * dx / d, p1[1] + recul * dy / d + 6, nom, 20, couleur,
                 "middle", gras=True, serif=True, italique=True)


def point(p, couleur, rayon=3.6):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{rayon}" fill="{couleur}"/>'


def interpole(p, q, t):
    return p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])


def dans_polygone(p, poly):
    """Vrai si le point écran p est dans le polygone convexe `poly` (bord compris)."""
    signes = set()
    for k in range(len(poly)):
        (ax, ay), (bx, by) = poly[k], poly[(k + 1) % len(poly)]
        c = (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax)
        if abs(c) > 1e-9:
            signes.add(c > 0)
    return len(signes) <= 1


def axes(cx, normale=None, plan=None):
    """Les trois demi-axes positifs. Rend (derrière, devant) : un demi-axe situé du
    côté du plan opposé à l'observateur passe derrière, et la part que le morceau de
    plan `plan` (polygone écran contenant l'origine) recouvre est tracée en tirets.
    Sans plan, tout est « devant »."""
    derriere, devant = [], []
    o = ecran((0, 0, 0), cx)
    cote_camera = scalaire(normale, vers_camera()) if normale else 0.0
    for k in range(3):
        e = tuple(AXE_LONGUEUR if i == k else 0.0 for i in range(3))
        bout = ecran(e, cx)
        cache = normale is not None and normale[k] * cote_camera < 0
        couche = derriere if cache else devant
        if cache:
            t = max(j / 200 for j in range(201)
                    if dans_polygone(interpole(o, bout, j / 200), plan))
            m = interpole(o, bout, t)
            couche.append(segment(o, m, AXE, 1.2, "4 3"))
            if t < 1:
                couche.append(segment(m, bout, AXE, 1.2))
        else:
            couche.append(segment(o, bout, AXE, 1.2))
        lx, ly = ecran(tuple(1.13 * c for c in e), cx)
        couche.append(f'<text x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="middle" '
                      f'font-size="14" fill="{AXE}" font-family="Georgia,serif" '
                      f'font-style="italic">e<tspan dy="4" font-size="10" font-style="normal" '
                      f'font-family="ui-monospace,Consolas,monospace">{k + 1}</tspan></text>')
    return derriere, devant


def origine(cx):
    """Le « 0 » en chasse fixe : les chiffres elzéviriens de Georgia en font un « o »."""
    o = ecran((0, 0, 0), cx)
    return [point(o, ENCRE, 3.2),
            texte(o[0] - 8, o[1] + 17, "0", 14, ENCRE, "end", gras=True)]


def entete():
    return [
        (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" width="{L}" '
         f'height="{H}" font-family="ui-monospace,Consolas,monospace">'),
        f'<rect width="{L}" height="{H}" fill="{FOND}"/>',
        texte(40, 34, "4.2 — Vect(u, v) : un plan, ou seulement une droite", 19, ENCRE,
              gras=True, serif=True),
        texte(40, 56, "dans ℝ³ · le même u dans les deux panneaux, seul v change · "
              "points : les 9 combinaisons λu + μv, λ et μ parcourant {−1, 0, 1}"),
        segment((600, 84), (600, 580), GRILLE, 1.0),
    ]


def ecrire(sortie, nom, lignes):
    """Écrit le SVG en CRLF explicite — indépendant du système. Voir .gitattributes."""
    lignes.append("</svg>")
    sortie.mkdir(parents=True, exist_ok=True)
    chemin = sortie / nom
    with chemin.open("w", encoding="utf-8", newline="") as flux:
        flux.write("\r\n".join(lignes) + "\r\n")
    print(f"Graphique écrit dans : {chemin}")
    return chemin


# --- Les deux panneaux --------------------------------------------------------


def panneau_plan(u, v):
    """Gauche — v non colinéaire à u : le morceau de plan [-BORD, BORD]², sa grille
    aux coefficients entiers, les neuf combinaisons."""
    cx = CX_GAUCHE
    n = vectoriel(u, v)
    r = rang(u, v)
    coins = [ecran(combinaison(a, u, b, v), cx)
             for a, b in ((-BORD, -BORD), (BORD, -BORD), (BORD, BORD), (-BORD, BORD))]
    derriere, devant = axes(cx, n, coins)
    out = [texte(40, 104, "v non colinéaire à u  →  Vect(u, v) est un plan", 14, ENCRE,
                 gras=True),
           texte(40, 124, f"9 combinaisons, {distincts(u, v)} points, non alignés : "
                 f"dimension {r}")]
    out += derriere

    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in coins)
    out.append(f'<polygon points="{pts}" fill="{SOUS_ESPACE}" fill-opacity="0.10" '
               f'stroke="{SOUS_ESPACE}" stroke-width="1.4" stroke-opacity="0.8"/>')
    for c in COEFFICIENTS:
        out.append(segment(ecran(combinaison(c, u, -BORD, v), cx),
                           ecran(combinaison(c, u, BORD, v), cx), SOUS_ESPACE, 1.0, "4 4", 0.45))
        out.append(segment(ecran(combinaison(-BORD, u, c, v), cx),
                           ecran(combinaison(BORD, u, c, v), cx), SOUS_ESPACE, 1.0, "4 4", 0.45))
    out += devant

    lx, ly = coins[3]
    out.append(texte(lx, ly - 34, "Vect(u, v)", 16, SOUS_ESPACE, gras=True, serif=True))
    for lam in COEFFICIENTS:
        for mu in COEFFICIENTS:
            out.append(point(ecran(combinaison(lam, u, mu, v), cx), SOUS_ESPACE))
    s = ecran(combinaison(1, u, 1, v), cx)
    out.append(texte(s[0] + 9, s[1] - 8, "u + v", 13, SOUS_ESPACE, serif=True, italique=True))

    o = ecran((0, 0, 0), cx)
    pu, pv = ecran(u, cx), ecran(v, cx)
    out += fleche(o, pu, VECT_U) + fleche(o, pv, VECT_V)
    out += [nom_vecteur(o, pu, "u", VECT_U), nom_vecteur(o, pv, "v", VECT_V)]
    out += origine(cx)
    return out, r, n


def panneau_droite(u, k):
    """Droite — v = k u : les neuf combinaisons (λ + k μ) u, toutes sur Vect(u)."""
    cx = CX_DROITE
    v = tuple(k * c + 0.0 for c in u)  # + 0.0 : pas de « -0.0 » à l'affichage
    r = rang(u, v)
    _, devant = axes(cx)
    out = [texte(640, 104, f"v = {nombre(k)} u  →  Vect(u, v) est la droite Vect(u)", 14,
                 ENCRE, gras=True),
           texte(640, 124, f"λu + μv = (λ {nombre(k)[0]} {nombre(abs(k))} μ) u : "
                 f"{distincts(u, v)} points, tous alignés — dimension {r}")]
    out += devant

    a = ecran(combinaison(-DEMI_DROITE, u, 0, u), cx)
    b = ecran(combinaison(DEMI_DROITE, u, 0, u), cx)
    out.append(segment(a, b, SOUS_ESPACE, 2.0, opacite=0.8))
    out.append(texte(b[0], b[1] - 20, "Vect(u, v) = Vect(u)", 16, SOUS_ESPACE, "end",
                     gras=True, serif=True))
    for lam in COEFFICIENTS:
        for mu in COEFFICIENTS:
            out.append(point(ecran(combinaison(lam, u, mu, v), cx), SOUS_ESPACE))
    s = ecran(combinaison(1, u, 1, v), cx)
    out.append(texte(s[0] + 4, s[1] + 26, f"u + v = {nombre(1 + k)} u", 13, SOUS_ESPACE))

    o = ecran((0, 0, 0), cx)
    pu, pv = ecran(u, cx), ecran(v, cx)
    out += fleche(o, pv, VECT_V) + fleche(o, pu, VECT_U)
    out += [nom_vecteur(o, pu, "u", VECT_U), nom_vecteur(o, pv, "v", VECT_V)]
    out += origine(cx)
    return out, r, v


def figure_vect(sortie):
    """§ 4.2 — le cas d = 2 : deux générateurs, un plan ou une droite."""
    out = entete()
    gauche, r_plan, n = panneau_plan(U, V_LIBRE)
    droite, r_droite, v_col = panneau_droite(U, K_COLINEAIRE)
    out += gauche + droite
    out.append(texte(600, 612, "deux générateurs dans les deux panneaux, et pourtant "
                     f"dimension {r_plan} à gauche, {r_droite} à droite", 13, ENCRE, "middle",
                     gras=True))
    out.append(texte(600, 632, "le nombre de générateurs majore la dimension, il ne la "
                     "donne pas", 13, ENCRE2, "middle"))
    ecrire(sortie, "vect-plan-ou-droite.svg", out)
    return r_plan, n, r_droite, v_col


def main():
    parser = argparse.ArgumentParser(
        description="Trace la figure du § 4.2 du cours d'algèbre : Vect(u, v) dans R^3.")
    parser.add_argument("--sortie", type=Path, default=Path(__file__).resolve().parent,
                        help="repertoire ou ecrire le SVG (defaut : celui du script)")
    args = parser.parse_args()

    r_plan, n, r_droite, v_col = figure_vect(args.sortie)
    print(f"\ngauche  u = {U}  v = {V_LIBRE}  u x v = {n}  rang {r_plan}  "
          f"{distincts(U, V_LIBRE)} points distincts")
    print(f"droite  u = {U}  v = {v_col}  u x v = {vectoriel(U, v_col)}  rang {r_droite}  "
          f"{distincts(U, v_col)} points distincts")


if __name__ == "__main__":
    main()
