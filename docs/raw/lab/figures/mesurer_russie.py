#!/usr/bin/env python3
"""Mesure deux questions du laboratoire sur la Russie, sans aucune série russe.

    taux       un support légal suit-il le rouble ou le taux directeur russe ?
    evenement  six supports ont-ils lu, le 2026-10-09, un accord russo-américain ?

Le script n'écrit rien : il imprime un relevé. Aucun verdict d'achat ou de vente.

Utilisation :
    python docs/raw/lab/figures/mesurer_russie.py taux
    python docs/raw/lab/figures/mesurer_russie.py evenement

Le miroir d'exécution est dans mesurer_russie.md, et il fait autorité.
"""

import argparse
import csv
import math
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

ICI = Path(__file__).resolve().parent
TAUX_DEFAUT = ICI / "taux-directeur-russie.csv"
SEUIL_SAUT = 0.50

REFERENCE = "EURRUB=X"
CONTROLE = "RUB=X"
SUPPORTS = ["RBI.VI", "OTP.BD", "KSPI", "HSBK.IL", "TBCG.L", "BGEO.L", "KAP.IL",
            "BZ=F", "^FCHI", "EEM", "KZT=X"]
CHANGES = {REFERENCE, CONTROLE, "KZT=X"}   # inversés : + = devise locale forte

# support : (sens attendu sous le scénario B, marché de référence)
EVENEMENT = {
    "TTF=F": (-1, None),
    "BAS.DE": (+1, "^STOXX50E"),
    "RBI.VI": (+1, "^STOXX50E"),
    "LNG": (-1, "^GSPC"),
    "RHM.DE": (+1, "^STOXX50E"),
    "EPOL": (-1, "^GSPC"),
}
CONTEXTE = ["^STOXX50E", "^GSPC", "BZ=F"]


def p_valeur(t, ddl):
    """La loi de Student du dépôt, réimplémentée dans import_societe.py."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "python"))
    from import_societe import p_valeur_student  # noqa: PLC0415 - le depot n'est pas un paquet

    return p_valeur_student(t, ddl)


def fr(x, decimales=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"{x:,.{decimales}f}".replace(",", " ").replace(".", ",")


def signe(x, decimales=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return ("+" if x >= 0 else "") + fr(x, decimales)


def nom(t):
    return f"{t} (fort)" if t in CHANGES else t


# --- Données ------------------------------------------------------------------


def lire_taux(chemin):
    """Lit la donnée déclarée et contrôle sa cohérence."""
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    effets, taux, decisions = [], [], []
    for ligne in lignes:
        effet = date.fromisoformat(ligne["effet"])
        decision = date.fromisoformat(ligne["decision"]) if ligne["decision"] else None
        if effets and effet <= effets[-1]:
            raise SystemExit(f"Donnée invalide : dates d'effet non croissantes au {effet}.")
        if decision and decision > effet:
            raise SystemExit(f"Donnée invalide : décision du {decision} après son effet.")
        effets.append(effet)
        taux.append(float(ligne["taux"]))
        decisions.append(decision)
    niveau = pd.Series(taux, index=pd.DatetimeIndex(effets))
    changements = [
        (decisions[i], taux[i - 1], taux[i]) for i in range(1, len(taux)) if decisions[i]
    ]
    return niveau, changements


def telecharger(tickers, debut, fin):
    """Clôtures ajustées, index en dates calendaires ; écarte les séries vides."""
    series, divisions = {}, {}
    for t in tickers:
        h = yf.Ticker(t).history(start=debut - timedelta(days=10), end=fin + timedelta(days=1),
                                 auto_adjust=True, actions=True)
        if h.empty:
            print(f"  ⚠️ {t} : aucune donnée, série écartée.")
            continue
        h.index = pd.DatetimeIndex(h.index.date)
        h = h[~h.index.duplicated(keep="last")]
        series[t] = h["Close"]
        divisions[t] = h.get("Stock Splits", pd.Series(0.0, index=h.index)).fillna(0)
    return series, divisions


def controler_saut(series, divisions, obligatoires=()):
    """Saut > 50 % sans division déclarée : série irrecevable, écartée."""
    for t in list(series):
        p = series[t].dropna()
        ratio = p / p.shift(1) - 1
        suspects = ratio[(ratio.abs() > SEUIL_SAUT) & (divisions[t].reindex(ratio.index) == 0)]
        if suspects.empty:
            continue
        jour = suspects.index[0].date()
        facteur = 1 + suspects.iloc[0]
        print(f"  ⚠️ {t} : irrecevable, clôture multipliée par {fr(facteur, 3)} le {jour} "
              "sans division déclarée.")
        if t in obligatoires:
            raise SystemExit(f"La série {t} est indispensable : arrêt.")
        del series[t]


def log_rendements(p):
    p = p.dropna()
    return (p / p.shift(1)).apply(math.log).dropna()


# --- Statistiques --------------------------------------------------------------


def correlation(x, y):
    d = pd.concat([x, y], axis=1).dropna()
    n = len(d)
    if n < 3:
        return n, float("nan")
    return n, float(d.iloc[:, 0].corr(d.iloc[:, 1]))


def student_r(r, n):
    if n < 3 or math.isnan(r) or abs(r) >= 1:
        return float("nan"), float("nan")
    t = r * math.sqrt((n - 2) / (1 - r * r))
    return t, p_valeur(t, n - 2)


def holm(p):
    """p-valeurs corrigées de Holm, dans l'ordre d'entrée ; NaN conservés."""
    valides = sorted((v, i) for i, v in enumerate(p) if not math.isnan(v))
    m = len(valides)
    sortie = [float("nan")] * len(p)
    courant = 0.0
    for rang, (v, i) in enumerate(valides):
        courant = max(courant, min(1.0, (m - rang) * v))
        sortie[i] = courant
    return sortie


# --- Sous-commande taux --------------------------------------------------------


def mesurer_taux(args):
    niveau, changements = lire_taux(args.taux)
    debut, fin = date.fromisoformat(args.debut), date.fromisoformat(args.fin)
    print(f"Fenêtre : {debut} → {fin}, bornes incluses.\n\nTéléchargement…")
    series, divisions = telecharger([REFERENCE, CONTROLE, *SUPPORTS], debut, fin)
    if REFERENCE not in series:
        raise SystemExit(f"La série {REFERENCE} est indispensable : arrêt.")
    controler_saut(series, divisions, obligatoires=(REFERENCE,))
    prix = {}
    for t, brut in series.items():
        p = brut[(brut.index >= pd.Timestamp(debut)) & (brut.index <= pd.Timestamp(fin))].dropna()
        prix[t] = 1 / p if t in CHANGES else p
    supports = [t for t in [CONTROLE, *SUPPORTS] if t in prix]
    avec_ref = [*supports, REFERENCE]   # le rouble lui-même, aux mesures 2 et 3

    # Mesure 1
    hebdo = {t: log_rendements(p.resample("W-FRI").last()) for t, p in prix.items()}
    ref = hebdo[REFERENCE]
    lignes = []
    for t in supports:
        n, r = correlation(hebdo[t], ref)
        tt, p = student_r(r, n)
        d = pd.concat([hebdo[t], ref], axis=1).dropna()
        glis = d.iloc[:, 0].rolling(26).corr(d.iloc[:, 1]).dropna()
        lignes.append([t, n, r, tt, p, glis.min(), glis.max()])
    ph = holm([ligne[4] for ligne in lignes])
    print(f"\n1) Corrélation HEBDOMADAIRE avec {nom(REFERENCE)}")
    print(f"   {'support':16s} {'n':>4s} {'r':>7s} {'t':>7s} {'p':>7s} {'Holm':>7s}"
          f" {'rho²':>7s}   glissante 26 sem.")
    for (t, n, r, tt, p, lo, hi), q in zip(lignes, ph, strict=True):
        print(f"   {nom(t):16s} {n:4d} {signe(r, 3):>7s} {signe(tt):>7s} {fr(p, 3):>7s}"
              f" {fr(q, 3):>7s} {fr(100 * r * r, 1):>6s} %   [{signe(lo)} ; {signe(hi)}]")

    # Mesure 2
    mois = pd.date_range(pd.Timestamp(debut), pd.Timestamp(fin), freq="ME")
    taux_mois = niveau.reindex(niveau.index.union(mois)).ffill().reindex(mois)
    dtaux = taux_mois.diff().dropna()
    lignes = []
    for t in avec_ref:
        m = log_rendements(prix[t].resample("ME").last())
        d = pd.concat([m, dtaux], axis=1).dropna()
        n, r = len(d), float(d.iloc[:, 0].corr(d.iloc[:, 1])) if len(d) > 2 else float("nan")
        tt, p = student_r(r, n)
        x, y = d.iloc[:, 1], d.iloc[:, 0]
        pente = 100 * float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())
        lignes.append([t, n, r, tt, p, pente])
    ph = holm([ligne[4] for ligne in lignes])
    print("\n2) Rendement MENSUEL contre variation du taux directeur (r < 0 : monte quand le taux"
          " baisse)")
    print(f"   {'support':16s} {'n':>4s} {'r':>7s} {'t':>7s} {'p':>7s} {'Holm':>7s}"
          "   pente (% par point)")
    for (t, n, r, tt, p, pente), q in zip(lignes, ph, strict=True):
        print(f"   {nom(t):16s} {n:4d} {signe(r, 3):>7s} {signe(tt):>7s} {fr(p, 3):>7s}"
              f" {fr(q, 3):>7s}   {signe(pente)}")

    # Mesure 3
    quotid = {t: log_rendements(prix[t]) for t in avec_ref}
    dans = [(d, a, b) for d, a, b in changements if debut <= d <= fin]
    print("\n3) Rendement à la séance de décision, en % (cellule vide : pas de cotation ce jour)")
    print("   " + f"{'décision':10s} {'taux':>12s} " + " ".join(f"{t[:8]:>8s}" for t in avec_ref))
    for d, a, b in dans:
        cellules = []
        for t in avec_ref:
            v = quotid[t].get(pd.Timestamp(d))
            cellules.append(f"{signe(100 * v) if v is not None else '':>8s}")
        print(f"   {d}  {fr(a):>5s}→{fr(b):<5s} " + " ".join(cellules))
    baisses = [d for d, a, b in dans if b < a]
    lignes = []
    for t in avec_ref:
        jours = [quotid[t].get(pd.Timestamp(d)) for d in baisses]
        jours = [v for v in jours if v is not None]
        k, sigma, nq = len(jours), float(quotid[t].std()), len(quotid[t])
        moy = sum(jours) / k if k else float("nan")
        z = moy / (sigma / math.sqrt(k)) if k else float("nan")
        lignes.append([t, k, moy, sigma, z, p_valeur(z, nq - 1) if k else float("nan")])
    ph = holm([ligne[5] for ligne in lignes])
    print(f"\n   {len(baisses)} baisses. Rendement moyen à la séance de décision :")
    print(f"   {'support':16s} {'k':>3s} {'moyenne':>9s} {'sigma':>7s} {'z':>7s} {'p':>7s}"
          f" {'Holm':>7s}")
    for (t, k, moy, sigma, z, p), q in zip(lignes, ph, strict=True):
        print(f"   {nom(t):16s} {k:3d} {signe(100 * moy):>8s}% {fr(100 * sigma):>6s}%"
              f" {signe(z):>7s} {fr(p, 3):>7s} {fr(q, 3):>7s}")


# --- Sous-commande evenement ---------------------------------------------------


def mesurer_evenement(args):
    jour, veille = pd.Timestamp(args.date), pd.Timestamp(args.veille)
    e0, e1 = pd.Timestamp(args.estimation_debut), pd.Timestamp(args.estimation_fin)
    marches = sorted({m for _, m in EVENEMENT.values() if m})
    tickers = list(dict.fromkeys([*EVENEMENT, *marches, *CONTEXTE]))
    print("Téléchargement…")
    series, divisions = telecharger(tickers, e0.date(), jour.date() + timedelta(days=3))
    controler_saut(series, divisions)
    rend = {t: log_rendements(p) for t, p in series.items()}
    manquants = [t for t in [*EVENEMENT, *marches] if t not in rend or jour not in rend[t].index]
    if manquants:
        print(f"\nSéance du {jour.date()} absente pour : {', '.join(manquants)}.")
        print("Les cours ne sont pas encore publiés : relancer plus tard.")
        sys.exit(2)

    print(f"\nBêta estimés du {e0.date()} au {e1.date()} ; séance principale {jour.date()},"
          f" fenêtre secondaire {veille.date()} + {jour.date()}.\n")
    print(f"   {'support':8s} {'sens':>4s} {'bêta':>6s} {'s':>6s} {'brut':>7s} {'RA':>7s}"
          f" {'z':>6s} {'z signé':>8s}   {'z2 (8+9)':>9s}")
    signes, concord = {}, 0
    for t, (sens, marche) in EVENEMENT.items():
        r = rend[t]
        fen = r[(r.index >= e0) & (r.index <= e1)]
        if marche:
            rm = rend[marche]
            d = pd.concat([fen, rm], axis=1, join="inner")
            x, y = d.iloc[:, 1], d.iloc[:, 0]
            beta = float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())
            resid = y - y.mean() - beta * (x - x.mean())
            s = math.sqrt(float((resid ** 2).sum()) / (len(d) - 2))
        else:
            rm, beta, s = None, 0.0, float(fen.std())

        def anormal(j, r=r, rm=rm, beta=beta):
            if j not in r.index or (rm is not None and j not in rm.index):
                return None
            return float(r[j]) - (beta * float(rm[j]) if rm is not None else 0.0)

        ra, ra_v = anormal(jour), anormal(veille)
        z = ra / s
        zs = sens * z
        z2 = (ra + ra_v) / (s * math.sqrt(2)) if ra_v is not None else float("nan")
        signes[t] = zs
        concord += zs > 0
        print(f"   {t:8s} {'+' if sens > 0 else '−':>4s} {fr(beta):>6s} {fr(100 * s):>5s}%"
              f" {signe(100 * float(r[jour])):>6s}% {signe(100 * ra):>6s}% {signe(z):>6s}"
              f" {signe(zs):>8s}   {signe(z2):>9s}")

    S = sum(signes.values()) / len(signes)
    if S > 1 and concord >= 5:
        lecture = "B — accord russo-américain, l'UE maintenant ses sanctions"
    elif (all(signes[t] > 0 for t in ("TTF=F", "BAS.DE", "RBI.VI"))
          and all(signes[t] < 0 for t in ("RHM.DE", "EPOL"))):
        lecture = "A — paix multilatérale"
    elif S < -1:
        lecture = "contraire au scénario B"
    else:
        lecture = "ignorée"
    print(f"\n   S = {signe(S)}   signes concordants : {concord} sur {len(signes)}")
    print(f"   Lecture : {lecture}")
    print(f"\n   Contexte, rendements bruts du {jour.date()} :")
    for t in CONTEXTE:
        v = rend.get(t, pd.Series(dtype=float)).get(jour)
        print(f"   {t:10s} {signe(100 * v) + ' %' if v is not None else '—'}")


def main():
    parser = argparse.ArgumentParser(
        description="Mesures du laboratoire sur la Russie : proxys du taux directeur, "
                    "et réaction à l'annonce du 2026-10-08.")
    sous = parser.add_subparsers(dest="commande", required=True)
    pt = sous.add_parser("taux", help="corrélations au rouble et au taux directeur")
    pt.add_argument("--debut", default="2023-01-01", help="première séance, incluse")
    pt.add_argument("--fin", default="2026-09-30", help="dernière séance, incluse")
    pt.add_argument("--taux", type=Path, default=TAUX_DEFAUT, help="donnée déclarée du taux")
    pe = sous.add_parser("evenement", help="rendements anormaux à la séance déclarée")
    pe.add_argument("--date", default="2026-10-09", help="séance principale")
    pe.add_argument("--veille", default="2026-10-08", help="début de la fenêtre secondaire")
    pe.add_argument("--estimation-debut", default="2025-10-01", help="début d'estimation, inclus")
    pe.add_argument("--estimation-fin", default="2026-09-30", help="fin d'estimation, incluse")
    args = parser.parse_args()
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    if args.commande == "taux":
        mesurer_taux(args)
    else:
        mesurer_evenement(args)


if __name__ == "__main__":
    main()
