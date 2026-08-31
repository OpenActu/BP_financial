#!/usr/bin/env python3
"""
Trace les trois figures du module 2 du cours sur le canal, en SVG.

Dépendance :
    aucune — la série, la régression et le tracé sont en Python pur.

Utilisation :
    python docs/raw/concept/semestre3/canal/figures/generer_figures.py
    python docs/raw/concept/semestre3/canal/figures/generer_figures.py --sortie /tmp
    python docs/raw/concept/semestre3/canal/figures/generer_figures.py --stats

Les trois figures portent sur la MÊME série : une marche aléatoire gaussienne de
100 pas partant de 100, graine 1, dont la recette est publiée au § 2.0 de
../02-les-trois-largeurs.md. Un processus sans tendance, choisi pour que tout ce
que les figures donnent à lire soit un artefact de la mesure, jamais une
propriété du monde.

Le miroir d'exécution est dans generer_figures.md.
"""

import argparse
import math
import re
from pathlib import Path

GRAINE = 1
N = 100
DEPART = 100.0
SIGMA = 1.0

L, H = 1200, 620
X0, X1 = 62, 1104
Y0, Y1 = 74, 574

COURS = "#2a78d6"
RES = "#eb6834"
SUP = "#1baf7a"
GRILLE = "#e1e0d9"
AXE = "#c3c2b7"
ENCRE = "#0b0b0b"
ENCRE2 = "#52514e"
FOND = "#fcfcfb"
FENETRE = "#f2efe4"
DECISION = "#8b5cd6"


# --- La série, et ce qu'on en tire -------------------------------------------


def uniformes(graine, combien):
    """Générateur congruentiel linéaire de Numerical Recipes, en entiers 32 bits."""
    x = graine
    for _ in range(combien):
        x = (1664525 * x + 1013904223) % 2**32
        yield (x + 0.5) / 2**32


def serie():
    """Marche aléatoire gaussienne : V_0 = 100, V_i = V_{i-1} + z_i, z ~ N(0,1)."""
    u = list(uniformes(GRAINE, N))
    valeurs = [DEPART]
    for i in range(0, N, 2):
        r = math.sqrt(-2 * math.log(u[i]))
        z1 = r * math.cos(2 * math.pi * u[i + 1])
        z2 = r * math.sin(2 * math.pi * u[i + 1])
        valeurs.append(valeurs[-1] + SIGMA * z1)
        if len(valeurs) <= N:
            valeurs.append(valeurs[-1] + SIGMA * z2)
    return valeurs[1:N + 1]


def ajuste(v):
    """Droite des moindres carrés sur les rangs 1..n. Rend (a, b, résidus)."""
    n = len(v)
    t = list(range(1, n + 1))
    mt = sum(t) / n
    mv = sum(v) / n
    cov = sum((a - mt) * (b - mv) for a, b in zip(t, v, strict=True)) / n
    var = sum((a - mt) ** 2 for a in t) / n
    b = cov / var
    a = mv - b * mt
    res = [x - (a + b * i) for i, x in zip(t, v, strict=True)]
    return a, b, res


def stats(res):
    """Rend (s sans biais, sigma empirique, plus bas résidu, plus haut résidu)."""
    n = len(res)
    sce = sum(e * e for e in res)
    s = math.sqrt(sce / (n - 2))
    sigma_e = math.sqrt(sce / n)
    return s, sigma_e, min(res), max(res)


def centile(tri, p):
    """Interpolation linéaire sur une liste triée, convention (n-1)p."""
    k = (len(tri) - 1) * p
    i = int(k)
    if i + 1 >= len(tri):
        return tri[-1]
    return tri[i] + (k - i) * (tri[i + 1] - tri[i])


# --- Primitives de tracé ------------------------------------------------------


def fr(texte):
    """Virgule décimale, et espaces multiples rendus insécables (SVG les collapse)."""
    texte = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + "," + m.group(2), texte)
    return re.sub(r"  +", lambda m: "&#160;" * len(m.group()), texte)


def echelle(*couvre):
    """Rend (x, y, bas, haut) en englobant toutes les valeurs à couvrir."""
    bas, haut = min(couvre), max(couvre)
    marge = 0.06 * (haut - bas)
    b, h = bas - marge, haut + marge

    def x(i):
        return X0 + (X1 - X0) * (i - 1) / (N - 1)

    def y(v):
        return Y1 - (Y1 - Y0) * (v - b) / (h - b)

    return x, y, b, h


def entete(titre, sous_titre):
    return [
        (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" width="{L}" '
         f'height="{H}" font-family="ui-monospace,Consolas,monospace">'),
        f'<rect width="{L}" height="{H}" fill="{FOND}"/>',
        (f'<text x="{X0}" y="34" font-size="19" font-weight="600" fill="{ENCRE}" '
         f'font-family="Georgia,serif">{titre}</text>'),
        f'<text x="{X0}" y="54" font-size="12" fill="{ENCRE2}">{fr(sous_titre)}</text>',
    ]


def grille(y, bas, haut, pas):
    out = []
    niveau = math.ceil(bas / pas) * pas
    while niveau <= haut:
        yy = y(niveau)
        out.append(f'<line x1="{X0}" y1="{yy:.1f}" x2="{X1}" y2="{yy:.1f}" '
                   f'stroke="{GRILLE}" stroke-width="1"/>')
        out.append(f'<text x="{X0 - 10}" y="{yy + 4:.1f}" text-anchor="end" font-size="11" '
                   f'fill="{ENCRE2}">{niveau:g}</text>')
        niveau += pas
    for i in (1, 20, 40, 60, 80, 100):
        xx = X0 + (X1 - X0) * (i - 1) / (N - 1)
        out.append(f'<line x1="{xx:.1f}" y1="{Y0}" x2="{xx:.1f}" y2="{Y1}" '
                   f'stroke="{GRILLE}" stroke-width="1"/>')
        out.append(f'<text x="{xx:.1f}" y="{Y1 + 20}" text-anchor="middle" font-size="11" '
                   f'fill="{ENCRE2}">{i}</text>')
    out.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{AXE}" stroke-width="1"/>')
    out.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{Y1 + 40}" text-anchor="middle" '
               f'font-size="11" fill="{ENCRE2}">rang de seance</text>')
    return out


def polyligne(x, y, valeurs, couleur, largeur=1.4):
    pts = " ".join(f"{x(i + 1):.1f},{y(v):.1f}" for i, v in enumerate(valeurs))
    return (f'<polyline points="{pts}" fill="none" stroke="{couleur}" '
            f'stroke-width="{largeur}"/>')


def droite(x, y, a, b, i0, i1, couleur, largeur=1.4, tirets=None, opacite=1.0):
    dash = f' stroke-dasharray="{tirets}"' if tirets else ""
    return (f'<line x1="{x(i0):.1f}" y1="{y(a + b * i0):.1f}" x2="{x(i1):.1f}" '
            f'y2="{y(a + b * i1):.1f}" stroke="{couleur}" stroke-width="{largeur}" '
            f'opacity="{opacite}"{dash}/>')


def bande(x, y, a, b, bas, haut, i0, i1, couleur, opacite):
    p = [(x(i0), y(a + b * i0 + haut)), (x(i1), y(a + b * i1 + haut)),
         (x(i1), y(a + b * i1 + bas)), (x(i0), y(a + b * i0 + bas))]
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in p)
    return f'<polygon points="{pts}" fill="{couleur}" opacity="{opacite}"/>'


def occupe(x, y, valeurs, boite, pas=24):
    """Vrai si le tracé de `valeurs` traverse la boîte (bx0, by0, bx1, by1)."""
    bx0, by0, bx1, by1 = boite
    pts = [(x(i + 1), y(v)) for i, v in enumerate(valeurs)]
    for k in range(len(pts) - 1):
        (ax, ay), (cx, cy) = pts[k], pts[k + 1]
        for t in range(pas + 1):
            u = t / pas
            px, py = ax + (cx - ax) * u, ay + (cy - ay) * u
            if bx0 <= px <= bx1 and by0 <= py <= by1:
                return True
    return False


def placer(x, y, valeurs, largeur, hauteur, marge=10):
    """Rend le premier des quatre coins libres, sinon celui du bas à gauche."""
    coins = [(X0 + 14, Y0 + 14), (X1 - largeur - 14, Y0 + 14),
             (X0 + 14, Y1 - hauteur - 14), (X1 - largeur - 14, Y1 - hauteur - 14)]
    for cx, cy in coins:
        if not occupe(x, y, valeurs, (cx - marge, cy - marge,
                                      cx + largeur + marge, cy + hauteur + marge)):
            return cx, cy
    return coins[2]


def cartouche(lignes, x, y, largeur):
    out = [(f'<rect x="{x}" y="{y}" width="{largeur}" height="{18 * len(lignes) + 14}" '
            f'fill="{FOND}" stroke="{AXE}" stroke-width="1" opacity="0.94"/>')]
    for k, (texte, couleur, gras) in enumerate(lignes):
        poids = ' font-weight="600"' if gras else ""
        out.append(f'<text x="{x + 12}" y="{y + 21 + 18 * k}" font-size="12" '
                   f'fill="{couleur}"{poids}>{fr(texte)}</text>')
    return out


def points(x, y, valeurs, couleur, rayon, indices):
    return [f'<circle cx="{x(i + 1):.1f}" cy="{y(v):.1f}" r="{rayon}" fill="{couleur}"/>'
            for i, v in enumerate(valeurs) if (i + 1) in indices]


def ecrire(sortie, nom, lignes):
    """Écrit le SVG en CRLF explicite — indépendant du système. Voir .gitattributes."""
    lignes.append("</svg>")
    sortie.mkdir(parents=True, exist_ok=True)
    chemin = sortie / nom
    with chemin.open("w", encoding="utf-8", newline="") as flux:
        flux.write("\r\n".join(lignes) + "\r\n")
    print(f"Graphique écrit dans : {chemin}")
    return chemin


# --- Les trois figures --------------------------------------------------------


def figure_enveloppe(v, sortie):
    """2.1 — le même processus sur deux fenêtres, deux largeurs d'enveloppe."""
    a, b, res = ajuste(v)
    s, _, lo, hi = stats(res)
    a20, b20, res20 = ajuste(v[-20:])
    s20, _, lo20, hi20 = stats(res20)
    a20g = a20 - b20 * 80

    x, y, bas, haut = echelle(
        min(v), max(v),
        a + b * 1 + lo, a + b * N + hi, a + b * 1 + hi, a + b * N + lo,
        a20g + b20 * 81 + lo20, a20g + b20 * 100 + hi20)
    out = entete(
        "2.1 &#8212; L&#8217;enveloppe des r&#233;sidus, et ce que n lui fait",
        "marche al&#233;atoire gaussienne, 100 pas, graine 1 &#183; "
        "m&#234;me processus, deux fen&#234;tres, deux largeurs")
    xa, xb = x(81), x(100)
    out.append(f'<rect x="{xa:.1f}" y="{Y0}" width="{xb - xa:.1f}" height="{Y1 - Y0}" '
               f'fill="{FENETRE}" opacity="0.75"/>')
    out += grille(y, bas, haut, 2)
    out.append(bande(x, y, a, b, lo, hi, 1, N, COURS, 0.07))
    out.append(droite(x, y, a, b, 1, N, ENCRE2, 1.2, "6 4"))
    out.append(droite(x, y, a + hi, b, 1, N, RES, 1.6))
    out.append(droite(x, y, a + lo, b, 1, N, SUP, 1.6))
    out.append(droite(x, y, a20g + hi20, b20, 81, 100, DECISION, 1.6))
    out.append(droite(x, y, a20g + lo20, b20, 81, 100, DECISION, 1.6))
    out.append(droite(x, y, a20g, b20, 81, 100, DECISION, 1.0, "4 3", 0.7))
    out.append(polyligne(x, y, v, COURS, 1.5))
    out += points(x, y, v, RES, 3.6, {res.index(hi) + 1})
    out += points(x, y, v, SUP, 3.6, {res.index(lo) + 1})
    cartes = [
        (f"enveloppe sur n = 100     demi-largeur  {(hi - lo) / 2 / s:.2f} s", ENCRE, True),
        (f"enveloppe sur n = 20      demi-largeur  {(hi20 - lo20) / 2 / s20:.2f} s",
         DECISION, True),
        ("attendu en moyenne : 2,50 s &#224; n = 100,  1,87 s &#224; n = 20", ENCRE2, False),
        ((f"s = {s:.2f} sur 100 pas,  s = {s20:.2f} sur les 20 derniers &#8212; "
          "d&#8217;o&#249; la lecture en unit&#233;s de s"), ENCRE2, False),
        ("les deux points marqu&#233;s fixent &#224; eux seuls toute la largeur",
         ENCRE2, False)]
    out += cartouche(cartes, *placer(x, y, v, 620, 5 * 18 + 14), 620)
    out.append(f'<text x="{xa + 6:.1f}" y="{Y1 - 10}" font-size="11" fill="{DECISION}" '
               f'font-weight="600">fen&#234;tre de 20</text>')
    ecrire(sortie, "brownien-enveloppe.svg", out)
    return (hi - lo) / 2 / s, (hi20 - lo20) / 2 / s20


def figure_ecart_type(v, sortie):
    """2.2 — les bandes ± 1 s et ± 2 s, et les proportions observées."""
    a, b, res = ajuste(v)
    s, sigma_e, _, _ = stats(res)
    d1 = sum(1 for e in res if abs(e) <= s)
    d2 = sum(1 for e in res if abs(e) <= 2 * s)
    dehors2 = {i + 1 for i, e in enumerate(res) if abs(e) > 2 * s}

    x, y, bas, haut = echelle(
        min(v), max(v),
        a + b * 1 - 2 * s, a + b * N + 2 * s, a + b * 1 + 2 * s, a + b * N - 2 * s)
    out = entete(
        "2.2 &#8212; La bande &#177; k s, la seule comparable d&#8217;une fen&#234;tre "
        "&#224; l&#8217;autre",
        f"m&#234;me s&#233;rie, 100 pas &#183; s = {s:.3f}, estimateur sans biais "
        "(somme des carr&#233;s divis&#233;e par n&#8722;2)")
    out += grille(y, bas, haut, 2)
    out.append(bande(x, y, a, b, -2 * s, 2 * s, 1, N, COURS, 0.09))
    out.append(bande(x, y, a, b, -s, s, 1, N, COURS, 0.13))
    out.append(droite(x, y, a + 2 * s, b, 1, N, RES, 1.6))
    out.append(droite(x, y, a - 2 * s, b, 1, N, SUP, 1.6))
    out.append(droite(x, y, a + s, b, 1, N, ENCRE2, 1.2, "7 4"))
    out.append(droite(x, y, a - s, b, 1, N, ENCRE2, 1.2, "7 4"))
    out.append(droite(x, y, a, b, 1, N, ENCRE2, 1.2, "6 4"))
    out.append(polyligne(x, y, v, COURS, 1.5))
    out += points(x, y, v, RES, 3.6, dehors2)
    out += cartouche([
        (f"&#177; 1 s    {d1} / 100 dedans    &#8212; attendu 68,3 %", ENCRE, True),
        (f"&#177; 2 s    {d2} / 100 dedans    &#8212; attendu 95,5 %", ENCRE, True),
        ((f"s = {s:.4f}     &#963;&#234; = {sigma_e:.4f}     "
          f"&#233;cart {100 * (s / sigma_e - 1):.1f} %"), ENCRE2, False),
        ("la proportion ne d&#233;pend pas de n : c&#8217;est tout l&#8217;int&#233;r&#234;t",
         ENCRE2, False),
    ], *placer(x, y, v, 570, 4 * 18 + 14), 570)
    ecrire(sortie, "brownien-ecart-type.svg", out)
    return d1, d2, s, sigma_e


def figure_quantile(v, sortie):
    """2.3 — les résidus de l'ajustement à 100 points. Une seule chose varie d'une
    bande à l'autre : le nombre de points sur lequel le quantile est calculé."""
    _, _, res = ajuste(v)
    s, _, _, _ = stats(res)
    tri = sorted(res)
    q05, q95 = centile(tri, 0.05), centile(tri, 0.95)
    gauss = 1.645 * s

    fenetres = []
    for i0 in (1, 41, 81):
        sous = sorted(res[i0 - 1:i0 + 19])
        fenetres.append((i0, centile(sous, 0.05), centile(sous, 0.95)))

    x, y, bas, haut = echelle(min(res), max(res), -gauss, gauss, q05, q95,
                              *[val for _, c5, c95 in fenetres for val in (c5, c95)])
    out = entete(
        "2.3 &#8212; Le quantile empirique : asym&#233;trique, robuste, "
        "et instable &#224; n petit",
        "r&#233;sidus de la m&#234;me droite ajust&#233;e &#183; 5&#170; et 95&#170; "
        "centiles &#183; seul le nombre de points varie d&#8217;une bande &#224; l&#8217;autre")
    for i0, _, _ in fenetres:
        xa, xb = x(i0), x(i0 + 19)
        out.append(f'<rect x="{xa:.1f}" y="{Y0}" width="{xb - xa:.1f}" height="{Y1 - Y0}" '
                   f'fill="{FENETRE}" opacity="0.8"/>')
    out += grille(y, bas, haut, 2)
    out.append(bande(x, y, 0, 0, q05, q95, 1, N, COURS, 0.10))
    out.append(droite(x, y, q95, 0, 1, N, RES, 1.8))
    out.append(droite(x, y, q05, 0, 1, N, SUP, 1.8))
    out.append(droite(x, y, gauss, 0, 1, N, ENCRE2, 1.2, "7 4"))
    out.append(droite(x, y, -gauss, 0, 1, N, ENCRE2, 1.2, "7 4"))
    out.append(droite(x, y, 0, 0, 1, N, ENCRE2, 1.0, "3 3", 0.8))
    etiquette = []
    for i0, c5, c95 in fenetres:
        out.append(droite(x, y, c95, 0, i0, i0 + 19, DECISION, 2.2))
        out.append(droite(x, y, c5, 0, i0, i0 + 19, DECISION, 2.2))
        etiquette.append((i0, c5, c95))
    out.append(polyligne(x, y, res, COURS, 1.5))
    for i0, c5, c95 in etiquette:
        cx = x(i0 + 9.5)
        haut_libre = not occupe(x, y, res, (cx - 90, y(c95) - 24, cx + 90, y(c95) - 4))
        yy = y(c95) - 8 if haut_libre else y(c5) + 18
        libelle = fr(f"{i0}&#8211;{i0 + 19} : |q95|/|q05| = {abs(c95) / abs(c5):.2f}")
        out.append(f'<text x="{cx:.1f}" y="{yy:.1f}" text-anchor="middle" font-size="11" '
                   f'fill="{DECISION}" font-weight="600">{libelle}</text>')
    out += points(x, y, res, RES, 3.6, {res.index(max(res)) + 1})
    out += points(x, y, res, SUP, 3.6, {res.index(min(res)) + 1})
    out += cartouche([
        ((f"quantiles sur n = 100   [{q05 / s:+.2f} s ; {q95 / s:+.2f} s]   "
          f"|q95|/|q05| = {abs(q95) / abs(q05):.2f}"), ENCRE, True),
        (("&#177; 1,645 s, m&#234;me proportion sous loi normale   "
          "[&#8722;1,65 s ; +1,65 s]   1,00"), ENCRE2, False),
        ("le processus est sym&#233;trique : cette asym&#233;trie de 1,13 est du bruit",
         ENCRE, True),
        (("&#224; n = 20, le m&#234;me bruit va de 0,45 &#224; 3,96 &#8212; "
          "un facteur 9 sur la m&#234;me s&#233;rie"), DECISION, True),
    ], *placer(x, y, res, 700, 4 * 18 + 14), 700)
    ecrire(sortie, "brownien-quantile.svg", out)
    return q05, q95, s, fenetres


# --- Relevé statistique -------------------------------------------------------


def releve(v):
    """Imprime les nombres cités par le § 2.0 et les trois sections du module."""
    print(f"n = {len(v)}   V1 = {v[0]:.4f}   V50 = {v[49]:.4f}   V100 = {v[-1]:.4f}")
    print(f"min {min(v):.3f}   max {max(v):.3f}")
    for nom, sous in (("100 points", v), ("20 derniers", v[-20:]), ("20 premiers", v[:20])):
        a, b, res = ajuste(sous)
        s, sigma_e, lo, hi = stats(res)
        tri = sorted(res)
        q05, q95 = centile(tri, 0.05), centile(tri, 0.95)
        n = len(sous)
        d1 = sum(1 for e in res if abs(e) <= s)
        d2 = sum(1 for e in res if abs(e) <= 2 * s)
        dq = sum(1 for e in res if q05 <= e <= q95)
        print(f"\n--- {nom} (n = {n}) ---")
        print(f"  droite      a = {a:.4f}   b = {b:+.5f} / seance")
        print(f"  dispersion  s = {s:.4f}   sigma_e = {sigma_e:.4f}")
        print(f"  enveloppe   [{lo:+.3f} ; {hi:+.3f}]   etendue {hi - lo:.3f} = "
              f"{(hi - lo) / s:.2f} s   demi-largeur {(hi - lo) / 2 / s:.2f} s")
        print(f"  +/- 1 s     {d1}/{n} dedans = {100 * d1 / n:.1f} % (attendu 68,3 %)")
        print(f"  +/- 2 s     {d2}/{n} dedans = {100 * d2 / n:.1f} % (attendu 95,5 %)")
        print(f"  quantiles   [{q05:+.3f} ; {q95:+.3f}] soit [{q05 / s:+.2f} s ; "
              f"{q95 / s:+.2f} s]   largeur {(q95 - q05) / s:.2f} s")
        print(f"  asymetrie   |q95| / |q05| = {abs(q95) / abs(q05):.2f}")
        print(f"  dedans      {dq}/{n} = {100 * dq / n:.1f} % (vise 90 %)")


def main():
    parser = argparse.ArgumentParser(
        description="Trace les trois figures du module 2 du cours sur le canal.")
    parser.add_argument("--sortie", type=Path, default=Path(__file__).resolve().parent,
                        help="repertoire ou ecrire les SVG (defaut : celui du script)")
    parser.add_argument("--stats", action="store_true",
                        help="imprimer le releve statistique sans ecrire de figure")
    args = parser.parse_args()

    v = serie()
    if args.stats:
        releve(v)
        return

    e100, e20 = figure_enveloppe(v, args.sortie)
    d1, d2, s, sigma_e = figure_ecart_type(v, args.sortie)
    q05, q95, s_q, fenetres = figure_quantile(v, args.sortie)

    print(f"\n2.1  demi-largeur  {e100:.2f} s sur n = 100,  {e20:.2f} s sur n = 20")
    print(f"2.2  {d1}/100 dans +/- 1 s,  {d2}/100 dans +/- 2 s   "
          f"(s = {s:.4f}, sigma_e = {sigma_e:.4f})")
    print(f"2.3  quantiles n = 100 : [{q05 / s_q:+.2f} s ; {q95 / s_q:+.2f} s]   "
          f"asymetrie {abs(q95) / abs(q05):.2f}")
    for i0, c5, c95 in fenetres:
        print(f"       rangs {i0}-{i0 + 19} : [{c5 / s_q:+.2f} s ; {c95 / s_q:+.2f} s]   "
              f"asymetrie {abs(c95) / abs(c5):.2f}")


if __name__ == "__main__":
    main()
