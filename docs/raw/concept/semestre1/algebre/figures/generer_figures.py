#!/usr/bin/env python3
"""
Trace les figures du cours d'algèbre, en SVG : Vect(u, v) dans R^3 (§ 4.2), et
l'orthogonal de 1 dans R^3 (exercice E5.2).

Dépendance :
    aucune — la projection et le tracé sont en Python pur.

Utilisation :
    python docs/raw/concept/semestre1/algebre/figures/generer_figures.py
    python docs/raw/concept/semestre1/algebre/figures/generer_figures.py --sortie /tmp

Deux panneaux, le MÊME u. À gauche, v n'est pas colinéaire à u : Vect(u, v) est
un plan. À droite, v = -1,5 u : Vect(u, v) n'est plus que la droite Vect(u). Les
points tracés sont, dans les deux panneaux, les mêmes neuf combinaisons
λu + μv, λ et μ parcourant {-1, 0, 1} — seul v change.

E5.2 : le plan H = {u : u1 + u2 + u3 = 0}, orthogonal à la droite Vect(1), et une
série x envoyée dans H par le centrage x ↦ x - x̄ 1.

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

# Une vue : (azimut, élévation, pixels par unité, ordonnée écran de l'origine).
VUE_VECT = (math.radians(30), math.radians(25), 54, 372)

L, H = 1200, 650

# E5.2 : la série, et une vue par-dessous H, où Vect(1) monte presque droit.
SERIE = (0.0, 4.0, 2.0)
BORD_H = 3.4        # morceau de H tracé : s a + t b, s et t dans [-BORD_H, BORD_H]
UN_BAS, UN_HAUT = 2.0, 3.0  # morceau de Vect(1) tracé : t 1, t dans [-UN_BAS, UN_HAUT]
ANGLE_DROIT = 0.35  # côté du repère d'angle droit, en unités
VUE_CENTRES = (math.radians(35), math.radians(-15), 70, 390)
L_CENTRES, H_CENTRES = 900, 680
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


def vers_camera(vue=VUE_VECT):
    """Vecteur unitaire pointant de l'origine vers l'observateur."""
    azimut, elevation = vue[0], vue[1]
    return (math.cos(elevation) * math.cos(azimut), math.cos(elevation) * math.sin(azimut),
            math.sin(elevation))


def ecran(p, cx, vue=VUE_VECT):
    """Projection orthographique de R^3 sur l'écran, l'origine en (cx, cy)."""
    azimut, elevation, echelle, cy = vue
    sa, ca = math.sin(azimut), math.cos(azimut)
    se, ce = math.sin(elevation), math.cos(elevation)
    x = -sa * p[0] + ca * p[1]
    y = -ca * se * p[0] - sa * se * p[1] + ce * p[2]
    return cx + echelle * x, cy - echelle * y


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


def axes(cx, normale=None, plan=None, vue=VUE_VECT):
    """Les trois demi-axes positifs. Rend (derrière, devant) : un demi-axe situé du
    côté du plan opposé à l'observateur passe derrière, et la part que le morceau de
    plan `plan` (polygone écran contenant l'origine) recouvre est tracée en tirets.
    Sans plan, tout est « devant »."""
    derriere, devant = [], []
    o = ecran((0, 0, 0), cx, vue)
    cote_camera = scalaire(normale, vers_camera(vue)) if normale else 0.0
    for k in range(3):
        e = tuple(AXE_LONGUEUR if i == k else 0.0 for i in range(3))
        bout = ecran(e, cx, vue)
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
        lx, ly = ecran(tuple(1.13 * c for c in e), cx, vue)
        couche.append(f'<text x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="middle" '
                      f'font-size="14" fill="{AXE}" font-family="Georgia,serif" '
                      f'font-style="italic">e<tspan dy="4" font-size="10" font-style="normal" '
                      f'font-family="ui-monospace,Consolas,monospace">{k + 1}</tspan></text>')
    return derriere, devant


def origine(cx, vue=VUE_VECT):
    """Le « 0 » en chasse fixe : les chiffres elzéviriens de Georgia en font un « o »."""
    o = ecran((0, 0, 0), cx, vue)
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


# --- § 5.6, E5.2 : l'orthogonal de 1 -----------------------------------------


def moyenne(x):
    return sum(x) / len(x)


def norme(a):
    return math.sqrt(scalaire(a, a))


def unitaire(a):
    return tuple(c / norme(a) for c in a)


def figure_centres(sortie):
    """E5.2 — H = {u : u ⊥ 1} dans R^3, et le centrage x ↦ x - x̄ 1 qui y envoie x."""
    vue, cx = VUE_CENTRES, L_CENTRES / 2
    un = (1.0, 1.0, 1.0)
    x_bar = moyenne(SERIE)
    moy = tuple(x_bar * c for c in un)
    centre = tuple(xi - x_bar for xi in SERIE)
    a, b = unitaire((-1.0, 1.0, 0.0)), unitaire((1.0, 1.0, -2.0))  # base orthonormée de H

    def e(p):
        return ecran(p, cx, vue)

    coins = [e(combinaison(s, a, t, b))
             for s, t in ((-BORD_H, -BORD_H), (BORD_H, -BORD_H), (BORD_H, BORD_H),
                          (-BORD_H, BORD_H))]
    derriere, devant = axes(cx, un, coins, vue)
    o = e((0, 0, 0))

    out = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L_CENTRES} {H_CENTRES}" '
         f'width="{L_CENTRES}" height="{H_CENTRES}" '
         f'font-family="ui-monospace,Consolas,monospace">'),
        f'<rect width="{L_CENTRES}" height="{H_CENTRES}" fill="{FOND}"/>',
        texte(40, 34, "E5.2 — les vecteurs orthogonaux à 1 sont les vecteurs centrés", 19,
              ENCRE, gras=True, serif=True),
        texte(40, 56, "dans ℝ³ · H = { u : u₁ + u₂ + u₃ = 0 } est le plan orthogonal "
              "à la droite Vect(1)"),
    ]
    out += derriere

    # Vect(1), moitié négative : derrière H, masquée tant qu'elle est sous le plan.
    bas = e(tuple(-UN_BAS * c for c in un))
    t = max(j / 200 for j in range(201) if dans_polygone(interpole(o, bas, j / 200), coins))
    m = interpole(o, bas, t)
    out.append(segment(o, m, VECT_U, 2.0, "5 4", 0.6))
    if t < 1:
        out.append(segment(m, bas, VECT_U, 2.0, opacite=0.8))

    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in coins)
    out.append(f'<polygon points="{pts}" fill="{SOUS_ESPACE}" fill-opacity="0.10" '
               f'stroke="{SOUS_ESPACE}" stroke-width="1.4" stroke-opacity="0.8"/>')
    out += devant
    lx, ly = max(coins, key=lambda c: c[0] + c[1])  # le coin en bas à droite
    out.append(texte(lx - 12, ly - 30, "H = Vect(1)⊥", 16, SOUS_ESPACE, "end", gras=True,
                     serif=True))
    out.append(texte(lx - 12, ly - 12, "somme nulle · moyenne nulle", 12, SOUS_ESPACE,
                     "end"))

    # Vect(1), moitié positive : devant H.
    haut = e(tuple(UN_HAUT * c for c in un))
    out.append(segment(o, haut, VECT_U, 2.0, opacite=0.8))
    out.append(texte(haut[0] + 10, haut[1] + 4, "Vect(1)", 16, VECT_U, gras=True, serif=True))

    # Le rectangle 0, x̄ 1, x, x̃ : le centrage glisse x parallèlement à 1 jusqu'à H.
    px, pm, pc = e(SERIE), e(moy), e(centre)
    out.append(segment(pm, px, ENCRE2, 1.2, "4 3"))
    out += fleche(px, interpole(px, pc, 0.93), ENCRE2, 1.4, 11)
    milieu = interpole(px, pc, 0.5)
    out.append(texte(milieu[0] + 10, milieu[1] - 6, f"− x̄ 1 = − {nombre(x_bar)} · 1", 13,
                     ENCRE2))

    # L'angle droit en 0, entre Vect(1) et x̃.
    c1, c2 = unitaire(un), unitaire(centre)
    q1, q2 = e(tuple(ANGLE_DROIT * c for c in c1)), e(tuple(ANGLE_DROIT * c for c in c2))
    q3 = e(combinaison(ANGLE_DROIT, c1, ANGLE_DROIT, c2))
    out.append(f'<polyline points="{q1[0]:.1f},{q1[1]:.1f} {q3[0]:.1f},{q3[1]:.1f} '
               f'{q2[0]:.1f},{q2[1]:.1f}" fill="none" stroke="{ENCRE}" stroke-width="1.2"/>')

    out += fleche(o, pm, VECT_U) + fleche(o, pc, VECT_V) + fleche(o, px, ENCRE)
    serie = ", ".join(nombre(c) for c in SERIE)
    out.append(texte(px[0] + 12, px[1] - 4, f"x = ({serie})", 16, ENCRE, gras=True,
                     serif=True))
    out.append(texte(pm[0] - 40, pm[1] + 5, f"x̄ 1 = ({', '.join(nombre(c) for c in moy)})",
                     15, VECT_U, "end", gras=True, serif=True))
    out.append(texte(pc[0] - 6, pc[1] + 26,
                     f"x̃ = ({', '.join(nombre(c) for c in centre)})", 16, VECT_V, "end",
                     gras=True, serif=True))
    out += origine(cx, vue)

    somme = " + ".join(f"({nombre(c)})" if c < 0 else nombre(c) for c in centre)
    produit = scalaire(centre, un)
    out.append(texte(L_CENTRES / 2, H_CENTRES - 48,
                     f"⟨x̃, 1⟩ = {somme} = {nombre(produit)} : x̃ ∈ H, et tout u ∈ H est son "
                     "propre centré", 13, ENCRE, "middle", gras=True))
    out.append(texte(L_CENTRES / 2, H_CENTRES - 28,
                     "centrer, c'est glisser parallèlement à 1 jusqu'à H — "
                     "une équation, une dimension de moins : dim H = 3 − 1 = 2", 13, ENCRE2,
                     "middle"))
    ecrire(sortie, "orthogonal-a-un.svg", out)
    return x_bar, centre, produit


def main():
    parser = argparse.ArgumentParser(
        description="Trace les figures du cours d'algèbre : Vect(u, v) dans R^3 (§ 4.2), "
                    "l'orthogonal de 1 (E5.2).")
    parser.add_argument("--sortie", type=Path, default=Path(__file__).resolve().parent,
                        help="repertoire ou ecrire les SVG (defaut : celui du script)")
    args = parser.parse_args()

    r_plan, n, r_droite, v_col = figure_vect(args.sortie)
    x_bar, centre, produit = figure_centres(args.sortie)
    print(f"\ngauche  u = {U}  v = {V_LIBRE}  u x v = {n}  rang {r_plan}  "
          f"{distincts(U, V_LIBRE)} points distincts")
    print(f"droite  u = {U}  v = {v_col}  u x v = {vectoriel(U, v_col)}  rang {r_droite}  "
          f"{distincts(U, v_col)} points distincts")
    print(f"E5.2    x = {SERIE}  moyenne {x_bar:g}  centré {centre}  <centré, 1> = {produit:g}")


if __name__ == "__main__":
    main()
