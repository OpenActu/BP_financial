#!/usr/bin/env python3
"""
Mesure les nombres que cite le cours macro, et trace sa figure.

Dépendance :
    yfinance (pandas arrive avec lui). Le script appelle le réseau.

Utilisation :
    python docs/raw/concept/semestre4/macro/figures/mesurer_macro.py
    python docs/raw/concept/semestre4/macro/figures/mesurer_macro.py --stats
    python docs/raw/concept/semestre4/macro/figures/mesurer_macro.py --sortie /tmp

Quatre relevés, tous imprimés :
    A. sensibilités hebdomadaires de huit valeurs du CAC 40 au marché, au taux
       américain à 10 ans, à l'euro-dollar et au Brent, avec correction de Holm ;
    B. la sensibilité au taux, recalculée sur trois sous-périodes ;
    C. les corrélations annuelles du CAC 40 avec chaque variable macro ;
    D. la prévision mensuelle du CAC 40 par trois variables de taux, dans et
       hors échantillon.
Et une figure : les corrélations annuelles CAC 40 / variation du taux (relevé C).

Le miroir d'exécution est dans mesurer_macro.md.
"""

import argparse
import math
import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

VALEURS = {
    "BNP.PA": "BNP Paribas",
    "LI.PA": "Klépierre",
    "ENGI.PA": "Engie",
    "MC.PA": "LVMH",
    "OR.PA": "L'Oréal",
    "AIR.PA": "Airbus",
    "TTE.PA": "TotalEnergies",
    "SAN.PA": "Sanofi",
}
INDICE = "^FCHI"
TAUX_10 = "^TNX"
TAUX_3M = "^IRX"
CHANGE = "EURUSD=X"
PETROLE = "BZ=F"
CREDIT_HY = "HYG"
CREDIT_GOV = "IEF"

DEBUT = "2008-01-01"
FIN = "2026-01-01"
DEBUT_PREVISION = "1990-01-01"
APPRENTISSAGE = 120
SEUIL_SAUT = 0.50
ALPHA = 0.05
EXPLICATIVES = ("MARCHE", "TAUX", "EURUSD", "BRENT")
SOUS_PERIODES = [
    ("2008-2012", "2008-01-01", "2013-01-01"),
    ("2013-2021", "2013-01-01", "2022-01-01"),
    ("2022-2025", "2022-01-01", "2026-01-01"),
]

L, H = 1200, 560
X0, X1 = 80, 1160
Y0, Y1 = 80, 480
POSITIF = "#2a78d6"
NEGATIF = "#eb6834"
GRILLE = "#e1e0d9"
AXE = "#8a8984"
ENCRE = "#0b0b0b"
ENCRE2 = "#52514e"
FOND = "#fcfcfb"


def p_valeur(t, ddl):
    """La loi de Student du dépôt, réimplémentée dans import_societe.py."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "python"))
    from import_societe import p_valeur_student  # noqa: PLC0415 - le depot n'est pas un paquet

    return p_valeur_student(t, ddl)


# --- Données ------------------------------------------------------------------


def telecharger(ticker, debut, fin):
    """Historique quotidien ajusté, index en dates calendaires sans fuseau."""
    h = yf.Ticker(ticker).history(start=debut, end=fin, auto_adjust=True, actions=True)
    if h.empty:
        raise SystemExit(f"Aucune donnée pour « {ticker} ».")
    h.index = pd.DatetimeIndex(h.index.date)
    return h


def controler_saut(ticker, h):
    """Tout saut de clôture > 50 % sans division déclarée rend la série irrecevable."""
    ratio = h["Close"] / h["Close"].shift(1) - 1
    divisions = h.get("Stock Splits", pd.Series(0, index=h.index)).fillna(0)
    suspects = ratio[(ratio.abs() > SEUIL_SAUT) & (divisions == 0)]
    if not suspects.empty:
        jour = suspects.index[0].date()
        raise SystemExit(
            f"Série irrecevable : {ticker} saute de {suspects.iloc[0]:+.1%} le {jour} "
            "sans division déclarée (opération sur titre présumée)."
        )


def hebdomadaire(serie):
    """Dernière valeur de chaque semaine close le vendredi."""
    return serie.resample("W-FRI").last()


# --- Moindres carrés ----------------------------------------------------------


def inverser(m):
    """Inverse d'une petite matrice carrée, par Gauss-Jordan à pivot partiel."""
    k = len(m)
    a = [list(ligne) + [1.0 if i == j else 0.0 for j in range(k)] for i, ligne in enumerate(m)]
    for c in range(k):
        p = max(range(c, k), key=lambda r, c=c: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        pivot = a[c][c]
        a[c] = [v / pivot for v in a[c]]
        for r in range(k):
            if r != c:
                f = a[r][c]
                a[r] = [v - f * w for v, w in zip(a[r], a[c], strict=True)]
    return [ligne[k:] for ligne in a]


def mco(y, colonnes):
    """Régression de y sur une constante et les colonnes.

    Rend (coefficients, t de Student, ddl, R²), la constante en tête.
    """
    n = len(y)
    x = [[1.0, *ligne] for ligne in zip(*colonnes, strict=True)]
    k = len(x[0])
    xtx = [[sum(r[i] * r[j] for r in x) for j in range(k)] for i in range(k)]
    xty = [sum(r[i] * v for r, v in zip(x, y, strict=True)) for i in range(k)]
    inv = inverser(xtx)
    b = [sum(inv[i][j] * xty[j] for j in range(k)) for i in range(k)]
    ajuste = [sum(bi * xi for bi, xi in zip(b, r, strict=True)) for r in x]
    residus = [v - a for v, a in zip(y, ajuste, strict=True)]
    ssr = sum(e * e for e in residus)
    moy = sum(y) / n
    sst = sum((v - moy) ** 2 for v in y)
    ddl = n - k
    s2 = ssr / ddl
    t = [b[i] / math.sqrt(s2 * inv[i][i]) for i in range(k)]
    return b, t, ddl, 1 - ssr / sst


def holm(p_valeurs, alpha=ALPHA):
    """Rejets de Holm, dans l'ordre des p-valeurs fournies."""
    ordre = sorted(range(len(p_valeurs)), key=lambda i: p_valeurs[i])
    m = len(p_valeurs)
    rejet = [False] * m
    for rang, i in enumerate(ordre):
        if p_valeurs[i] > alpha / (m - rang):
            break
        rejet[i] = True
    return rejet


# --- Relevés ------------------------------------------------------------------


def facteurs_hebdo(debut, fin):
    """Variables explicatives hebdomadaires, sur leurs semaines communes."""
    fchi = hebdomadaire(telecharger(INDICE, debut, fin)["Close"])
    tnx = hebdomadaire(telecharger(TAUX_10, debut, fin)["Close"])
    eur = hebdomadaire(telecharger(CHANGE, debut, fin)["Close"])
    brent = hebdomadaire(telecharger(PETROLE, debut, fin)["Close"])
    hy = hebdomadaire(telecharger(CREDIT_HY, debut, fin)["Close"])
    gov = hebdomadaire(telecharger(CREDIT_GOV, debut, fin)["Close"])
    return pd.DataFrame({
        "MARCHE": fchi.pct_change(fill_method=None),
        "TAUX": tnx.diff(),                 # en points de pourcentage
        "EURUSD": eur.pct_change(fill_method=None),
        "BRENT": brent.pct_change(fill_method=None),
        "CREDIT": hy.pct_change(fill_method=None) - gov.pct_change(fill_method=None),
    })


def releve_a(donnees):
    """Sensibilités de chaque valeur, marché compris, et correction de Holm."""
    lignes = []
    for ticker in VALEURS:
        d = donnees[[ticker, *EXPLICATIVES]].dropna()
        b, t, ddl, r2 = mco(list(d[ticker]), [list(d[c]) for c in EXPLICATIVES])
        p = [p_valeur(v, ddl) for v in t]
        lignes.append((ticker, len(d), b, t, p, r2))
    macro = [ligne[4][i] for ligne in lignes for i in (2, 3, 4)]
    rejets = holm(macro)
    print("\nA. Sensibilités hebdomadaires, marché compris")
    print(f"   {'valeur':<9} {'n':>4} {'b_MARCHE':>9} {'b_TAUX':>8} {'t':>6} "
          f"{'b_EURUSD':>9} {'t':>6} {'b_BRENT':>8} {'t':>6} {'R²':>6}")
    for j, (ticker, n, b, t, _, r2) in enumerate(lignes):
        marque = ["*" if rejets[3 * j + i] else " " for i in range(3)]
        print(f"   {ticker:<9} {n:>4} {b[1]:>9.3f} {b[2]:>+8.4f} {t[2]:>+6.2f}{marque[0]}"
              f"{b[3]:>+9.3f} {t[3]:>+6.2f}{marque[1]}{b[4]:>+8.3f} {t[4]:>+6.2f}{marque[2]}"
              f"{r2:>6.3f}")
    bruts = sum(p < ALPHA for p in macro)
    print(f"   {len(macro)} coefficients macro : {bruts} au seuil de 5 % sans correction, "
          f"{sum(rejets)} après Holm (marqués *).")
    print("   b_TAUX : rendement hebdomadaire pour +1 point de taux ; "
          "constante non publiée (Close ajustée contre indice nu).")


def releve_b(donnees):
    """La sensibilité au taux, par sous-période."""
    print("\nB. b_TAUX par sous-période (t entre parenthèses), marché compris")
    print("   " + f"{'valeur':<9}" + "".join(f"{nom:>20}" for nom, _, _ in SOUS_PERIODES))
    for ticker in VALEURS:
        cellules = []
        for _, debut, fin in SOUS_PERIODES:
            d = donnees.loc[debut:fin, [ticker, *EXPLICATIVES]].dropna()
            d = d[d.index < fin]
            b, t, _, _ = mco(list(d[ticker]), [list(d[c]) for c in EXPLICATIVES])
            cellules.append(f"{b[2]:+.4f} ({t[2]:+.2f})")
        print("   " + f"{ticker:<9}" + "".join(f"{c:>20}" for c in cellules))


def releve_c(donnees):
    """Corrélations annuelles du marché avec chaque variable macro."""
    print("\nC. Corrélation annuelle du CAC 40 (rendements hebdomadaires) avec :")
    print(f"   {'année':<6} {'n':>3} {'Δ taux':>8} {'EURUSD':>8} {'Brent':>8} {'crédit':>8}")
    annees = []
    for annee, groupe in donnees.groupby(donnees.index.year):
        d = groupe[["MARCHE", "TAUX", "EURUSD", "BRENT", "CREDIT"]].dropna()
        c = [d["MARCHE"].corr(d[v]) for v in ("TAUX", "EURUSD", "BRENT", "CREDIT")]
        annees.append((annee, c[0]))
        print(f"   {annee:<6} {len(d):>3} {c[0]:>+8.3f} {c[1]:>+8.3f} {c[2]:>+8.3f} {c[3]:>+8.3f}")
    d = donnees[["MARCHE", "TAUX", "EURUSD", "BRENT", "CREDIT"]].dropna()
    c = [d["MARCHE"].corr(d[v]) for v in ("TAUX", "EURUSD", "BRENT", "CREDIT")]
    print(f"   {'total':<6} {len(d):>3} {c[0]:>+8.3f} {c[1]:>+8.3f} {c[2]:>+8.3f} {c[3]:>+8.3f}")
    print("   Δ taux > 0 avec le marché ⇔ actions et obligations évoluent en sens contraire.")
    return annees


def releve_d(fin):
    """Prévision du rendement mensuel suivant, dans et hors échantillon."""
    fchi = telecharger(INDICE, DEBUT_PREVISION, fin)["Close"].resample("ME").last()
    tnx = telecharger(TAUX_10, DEBUT_PREVISION, fin)["Close"].resample("ME").last()
    irx = telecharger(TAUX_3M, DEBUT_PREVISION, fin)["Close"].resample("ME").last()
    rendement_suivant = fchi.pct_change(fill_method=None).shift(-1)
    predicteurs = {
        "pente 10 ans - 3 mois": tnx - irx,
        "taux à 3 mois": irx,
        "variation 12 mois du 10 ans": tnx.diff(12),
    }
    print(f"\nD. Prévision du rendement mensuel suivant du CAC 40 "
          f"(apprentissage initial : {APPRENTISSAGE} mois, fenêtre croissante)")
    print(f"   {'prédicteur':<28} {'n':>4} {'de':>8} {'à':>8} {'R² dans':>9} {'t':>6} {'p':>7} "
          f"{'R² hors':>9}")
    for nom, x in predicteurs.items():
        d = pd.DataFrame({"r": rendement_suivant, "x": x}).dropna()
        r, xs = list(d["r"]), list(d["x"])
        _, t, ddl, r2 = mco(r, [xs])
        p = p_valeur(t[1], ddl)
        num = den = 0.0
        for i in range(APPRENTISSAGE, len(r)):
            b, _, _, _ = mco(r[:i], [xs[:i]])
            prevu = b[0] + b[1] * xs[i]
            moyenne = sum(r[:i]) / i
            num += (r[i] - prevu) ** 2
            den += (r[i] - moyenne) ** 2
        print(f"   {nom:<28} {len(r):>4} {d.index[0]:%Y-%m} {d.index[-1]:%Y-%m} "
              f"{r2:>9.4f} {t[1]:>+6.2f} {p:>7.3f} {1 - num / den:>+9.4f}")
    print("   R² hors < 0 : la moyenne historique aurait mieux prévu que le prédicteur.")


# --- Figure -------------------------------------------------------------------


def figure(annees, chemin):
    """Barres annuelles de la corrélation CAC 40 / variation du taux à 10 ans."""
    n = len(annees)
    pas = (X1 - X0) / n
    largeur = pas * 0.62

    def y(v):
        return Y0 + (0.8 - v) / 1.6 * (Y1 - Y0)

    s = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" '
         f'font-family="Helvetica, Arial, sans-serif">'),
        f'<rect width="{L}" height="{H}" fill="{FOND}"/>',
        (f'<text x="{X0}" y="36" font-size="22" fill="{ENCRE}" font-weight="bold">'
         "Corrélation annuelle : CAC 40 et variation du taux américain à 10 ans</text>"),
        (f'<text x="{X0}" y="60" font-size="15" fill="{ENCRE2}">'
         "Rendements hebdomadaires. Au-dessus de zéro, actions et obligations "
         "évoluent en sens contraire.</text>"),
    ]
    for g in (-0.8, -0.4, 0.0, 0.4, 0.8):
        couleur = AXE if g == 0 else GRILLE
        s.append(f'<line x1="{X0}" x2="{X1}" y1="{y(g):.1f}" y2="{y(g):.1f}" '
                 f'stroke="{couleur}" stroke-width="{1.5 if g == 0 else 1}"/>')
        s.append(f'<text x="{X0 - 10}" y="{y(g) + 5:.1f}" font-size="14" fill="{ENCRE2}" '
                 f'text-anchor="end">{g:+.1f}'.replace(".", ",") + "</text>")
    for i, (annee, v) in enumerate(annees):
        cx = X0 + pas * (i + 0.5)
        haut, bas = (y(v), y(0)) if v >= 0 else (y(0), y(v))
        couleur = POSITIF if v >= 0 else NEGATIF
        s.append(f'<rect x="{cx - largeur / 2:.1f}" y="{haut:.1f}" width="{largeur:.1f}" '
                 f'height="{bas - haut:.1f}" fill="{couleur}" rx="2"/>')
        ty = haut - 8 if v >= 0 else bas + 18
        s.append(f'<text x="{cx:.1f}" y="{ty:.1f}" font-size="13" fill="{ENCRE}" '
                 f'text-anchor="middle">{v:+.2f}'.replace(".", ",") + "</text>")
        s.append(f'<text x="{cx:.1f}" y="{Y1 + 26}" font-size="14" fill="{ENCRE2}" '
                 f'text-anchor="middle">{annee}</text>')
    s.append(f'<text x="{X0}" y="{H - 18}" font-size="13" fill="{ENCRE2}">'
             "Source : ^FCHI et ^TNX (Yahoo Finance), généré par mesurer_macro.py</text>")
    s.append("</svg>")
    chemin.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(f"\nFigure écrite : {chemin}")


def main():
    parser = argparse.ArgumentParser(description="Mesures et figure du cours macro.")
    parser.add_argument("--sortie", type=Path, default=Path(__file__).resolve().parent,
                        help="répertoire de la figure (défaut : celui du script)")
    parser.add_argument("--stats", action="store_true",
                        help="imprime les relevés sans écrire la figure")
    args = parser.parse_args()

    print(f"Fenêtre des relevés A à C : {DEBUT} → {FIN} (exclu), semaines closes le vendredi.")
    donnees = facteurs_hebdo(DEBUT, FIN)
    for ticker in VALEURS:
        h = telecharger(ticker, DEBUT, FIN)
        controler_saut(ticker, h)
        donnees[ticker] = hebdomadaire(h["Close"]).pct_change(fill_method=None)
    donnees = donnees.iloc[1:]
    donnees = donnees[donnees.index < FIN]  # la semaine à cheval sur FIN est incomplète

    releve_a(donnees)
    releve_b(donnees)
    annees = releve_c(donnees)
    releve_d(FIN)

    if not args.stats:
        args.sortie.mkdir(parents=True, exist_ok=True)
        figure(annees, args.sortie / "correlation-actions-taux.svg")


if __name__ == "__main__":
    main()
