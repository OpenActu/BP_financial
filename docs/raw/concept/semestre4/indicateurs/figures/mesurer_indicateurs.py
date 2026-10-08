#!/usr/bin/env python3
"""
Chiffre les dix indicateurs du cours « Soros et Steinhardt », et les lit.

Dépendance :
    yfinance (pandas arrive avec lui). Le script appelle le réseau : Yahoo, la
    BCE, Eurostat, la BRI et l'AMF (via data.gouv.fr), par urllib.

Utilisation :
    python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py
    python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py SU.PA AIR.PA
    python docs/raw/concept/semestre4/indicateurs/figures/mesurer_indicateurs.py KER.PA \
        --isin KER.PA=FR0000121485

Deux relevés, tous deux imprimés :
    A. le contexte, commun à toutes les valeurs — taux et politique monétaire,
       crédit, croissance et inflation, change (indicateurs 2, 3, 8, 9) ;
    B. une fiche par valeur — attentes, multiples, marges, levier, dilution,
       sensibilité au change, positionnement (indicateurs 1, 4 à 8, 10) ;
puis la synthèse : les marqueurs de boom et de bascule déclarés au module 9.

Le miroir d'exécution est dans mesurer_indicateurs.md.
"""

import argparse
import csv
import io
import json
import math
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

VALEURS_DEFAUT = ["AIR.PA", "MC.PA", "OR.PA", "SAN.PA", "TTE.PA", "BNP.PA", "SU.PA", "ORA.PA"]
ISIN = {
    "AIR.PA": "NL0000235190",
    "MC.PA": "FR0000121014",
    "OR.PA": "FR0000120321",
    "SAN.PA": "FR0000120578",
    "TTE.PA": "FR0000120271",
    "BNP.PA": "FR0000131104",
    "SU.PA": "FR0000121972",
    "ORA.PA": "FR0000133308",
}
INDICE = "^FCHI"
CHANGE = "EURUSD=X"
CREDIT_HY = "HYG"
CREDIT_GOV = "IEF"

BCE = "https://data-api.ecb.europa.eu/service/data/"
SERIE_TAUX_10 = "YC/B.U2.EUR.4F.G_N_A.SV_C_YM.SR_10Y"
SERIE_TAUX_3M = "YC/B.U2.EUR.4F.G_N_A.SV_C_YM.SR_3M"
SERIE_DEPOT = "FM/D.U2.EUR.4F.KR.DFR.LEV"
SERIE_PRETS_SNF = "BSI/M.U2.Y.U.A20T.A.I.U2.2240.Z01.A"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
BRI = "https://stats.bis.org/api/v1/data/WS_CREDIT_GAP/Q.FR.P.A.C"
AMF_JEU = "https://www.data.gouv.fr/api/1/datasets/?q=positions%20courtes%20nettes&page_size=5"

DECALAGE = 75            # jours entre clôture d'exercice et publication présumée
TAUX_ACTUALISATION = 0.08
CROISSANCE_LONGUE = 3.0  # % : croissance nominale de long terme, déclarée
HORIZON = 3              # années de la décomposition du rendement
SEMAINES = 156           # trois ans de rendements hebdomadaires
SEUIL_SAUT = 0.50
ALPHA = 0.05
TOLERANCE_BPA = 1.5      # rapport maximal consensus / BPA des douze derniers mois
FENETRE_ACTIONS = 30     # jours : médiane du nombre d'actions, série bruitée
TOLERANCE_DETTE = 2.0    # rapport maximal entre dette annuelle et dette du jour

# Seuils de lecture, déclarés au module 9 du cours avant toute mesure.
S_REVISION = 2.0         # % sur 90 jours
S_DIFFUSION = 0.5
S_DETTE = 3.0            # fois l'EBITDA
S_COUVERTURE = 3.0       # fois les frais financiers
S_DYNAMIQUE = 10.0       # points : croissance de la dette moins celle de l'EBITDA
S_MARGE = 2.0            # points au-dessus de sa propre moyenne
S_DILUTION = 2.0         # % sur 12 mois
S_COURTES = 2.0          # % du capital
S_VOLUME = 1.5
S_ECART_CREDIT = 10.0    # points de PIB, seuil de la BRI


def voisins():
    """Les fonctions déjà écrites ailleurs dans le dépôt : Student, MCO, Holm."""
    racine = Path(__file__).resolve().parents[6]
    sys.path.insert(0, str(racine / "python"))
    sys.path.insert(0, str(racine / "docs/raw/concept/semestre4/macro/figures"))
    from import_societe import p_valeur_student  # noqa: PLC0415 - le depot n'est pas un paquet
    from mesurer_macro import holm, mco  # noqa: PLC0415 - idem

    return p_valeur_student, mco, holm


# --- Mise en forme ------------------------------------------------------------


def fr(x, decimales=2, signe=False, suffixe=""):
    """Nombre à la française ; « — » pour une valeur absente."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    texte = f"{x:+.{decimales}f}" if signe else f"{x:.{decimales}f}"
    return texte.replace(".", ",") + suffixe


def fleche(x, seuil):
    """↑ au-dessus de +seuil, ↓ sous -seuil, → entre les deux, vide si absent."""
    if x is None:
        return " "
    if x >= seuil:
        return "↑"
    if x <= -seuil:
        return "↓"
    return "→"


def nombre(valeur):
    """Un float utilisable, ou None : ni chaîne, ni booléen, ni NaN."""
    if valeur is None or isinstance(valeur, bool):
        return None
    try:
        x = float(valeur)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) else x


def rapport(numerateur, denominateur):
    """Rapport, ou None. Le dénominateur doit être strictement positif."""
    num, den = nombre(numerateur), nombre(denominateur)
    if num is None or den is None or den <= 0:
        return None
    return num / den


def variation(nouveau, ancien):
    """Variation relative en %, ou None si l'ancienne valeur n'est pas positive."""
    r = rapport(nouveau, ancien)
    return None if r is None else 100 * (r - 1)


def signaler(source, erreur):
    """Une panne réseau ne doit jamais se confondre avec une absence de donnée."""
    print(f"   ! {source} : {erreur.__class__.__name__}: {erreur}", file=sys.stderr)


# --- Sources hors Yahoo -------------------------------------------------------


def lire(url):
    requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(requete, timeout=60) as reponse:
        return reponse.read().decode("utf-8")


def serie_bce(cle, debut):
    """[(période, valeur)] d'une série de la BCE, depuis `debut`."""
    texte = lire(f"{BCE}{cle}?format=csvdata&detail=dataonly&startPeriod={debut}")
    lignes = csv.DictReader(io.StringIO(texte))
    return [(ligne["TIME_PERIOD"], float(ligne["OBS_VALUE"]))
            for ligne in lignes if ligne["OBS_VALUE"]]


def serie_eurostat(jeu, filtres):
    """[(période, valeur)] d'une série Eurostat réduite à une seule dimension libre : le temps."""
    texte = lire(f"{EUROSTAT}{jeu}?{urllib.parse.urlencode(filtres)}")
    donnees = json.loads(texte)
    temps = {v: k for k, v in donnees["dimension"]["time"]["category"]["index"].items()}
    return sorted((temps[int(i)], float(v)) for i, v in donnees["value"].items())


def serie_bri(debut):
    """[(trimestre, écart crédit/PIB)] de la France, BRI."""
    texte = lire(f"{BRI}?format=csv&startPeriod={debut}")
    return [(ligne["TIME_PERIOD"], float(ligne["OBS_VALUE"]))
            for ligne in csv.DictReader(io.StringIO(texte)) if ligne["OBS_VALUE"]]


def valeur_au(serie, jour):
    """Dernière observation dont la période commence au plus tard à `jour`."""
    retenues = [(p, v) for p, v in serie if p <= jour]
    return retenues[-1] if retenues else (None, None)


def positions_courtes():
    """Le fichier AMF des positions courtes nettes publiées, en lignes de dict."""
    jeux = json.loads(lire(AMF_JEU))["data"]
    for jeu in jeux:
        for ressource in jeu.get("resources", []):
            if ressource.get("format") == "csv" and "vad" in ressource.get("url", "").lower():
                texte = lire(ressource["url"])
                return list(csv.DictReader(io.StringIO(texte), delimiter=";"))
    raise LookupError("aucun export CSV des positions courtes sur data.gouv.fr")


def courtes_au(lignes, isin, jour):
    """Somme des positions publiées et en vigueur au `jour`, et nombre de détenteurs.

    Une ligne est en vigueur entre sa date de début de publication (incluse) et
    sa date de fin de publication (exclue, vide si toujours en vigueur). Pour un
    même détenteur, seule la plus récente compte.
    """
    j = jour.isoformat()
    par_detenteur = {}
    for ligne in lignes:
        if ligne["code ISIN"] != isin:
            continue
        debut = ligne["Date de debut de publication position"]
        fin = ligne["Date de fin de publication position"]
        if debut <= j and (not fin or fin > j):
            cle = ligne["Detenteur de la position courte nette"]
            if cle not in par_detenteur or debut > par_detenteur[cle][0]:
                par_detenteur[cle] = (debut, float(ligne["Ratio"].replace(",", ".")))
    return sum(r for _, r in par_detenteur.values()), len(par_detenteur)


# --- Yahoo --------------------------------------------------------------------


def historique(ticker, debut, ajuste):
    h = yf.Ticker(ticker).history(start=debut, auto_adjust=ajuste, actions=True)
    if h.empty:
        raise LookupError(f"aucun historique pour « {ticker} »")
    h.index = pd.DatetimeIndex(h.index.date)
    return h


def controler_saut(ticker, h):
    """Tout saut de clôture > 50 % sans division déclarée rend la série irrecevable."""
    ratio = h["Close"] / h["Close"].shift(1) - 1
    divisions = h.get("Stock Splits", pd.Series(0, index=h.index)).fillna(0)
    suspects = ratio[(ratio.abs() > SEUIL_SAUT) & (divisions == 0)]
    if not suspects.empty:
        jour = suspects.index[0].date()
        raise LookupError(
            f"série irrecevable : {ticker} saute de {suspects.iloc[0]:+.1%} le {jour} "
            "sans division déclarée (opération sur titre présumée)"
        )


def au(serie, jour):
    """Dernière valeur d'une série datée, au plus tard à `jour`."""
    s = serie[serie.index <= pd.Timestamp(jour)].dropna()
    return None if s.empty else float(s.iloc[-1])


def actions_au(serie, jour):
    """Médiane des décomptes des FENETRE_ACTIONS derniers jours, sinon le dernier connu."""
    fin = pd.Timestamp(jour)
    fenetre = serie[(serie.index > fin - pd.Timedelta(days=FENETRE_ACTIONS))
                    & (serie.index <= fin)].dropna()
    return float(fenetre.median()) if not fenetre.empty else au(serie, jour)


def comptes(t):
    """{clôture: {poste: valeur}} des comptes annuels, avec leur publication présumée."""
    postes = {
        "resultat_net": ("income_stmt", "Net Income"),
        "chiffre_affaires": ("income_stmt", "Total Revenue"),
        "resultat_op": ("income_stmt", "Operating Income"),
        "ebitda": ("income_stmt", "EBITDA"),
        "ebit": ("income_stmt", "EBIT"),
        "interets": ("income_stmt", "Interest Expense"),
        "dette": ("balance_sheet", "Total Debt"),
    }
    periodes = {}
    for attribut in ("income_stmt", "balance_sheet"):
        table = getattr(t, attribut)
        if table is None or table.empty:
            continue
        for colonne in table.columns:
            cloture = pd.Timestamp(colonne).tz_localize(None).normalize()
            ligne = periodes.setdefault(cloture, {})
            for poste, (origine, libelle) in postes.items():
                if origine == attribut and libelle in table.index:
                    ligne[poste] = nombre(table.loc[libelle, colonne])
    return periodes


def publies(periodes, jour):
    """Les exercices publiés à `jour` (clôture + DECALAGE ≤ jour), du plus ancien au plus récent."""
    limite = pd.Timestamp(jour) - pd.Timedelta(days=DECALAGE)
    return [(c, periodes[c]) for c in sorted(periodes) if c <= limite]


def serie_actions(t, debut):
    brute = t.get_shares_full(start=debut)
    if brute is None or len(brute) == 0:
        return pd.Series(dtype="float64")
    brute.index = pd.to_datetime(brute.index).tz_localize(None).normalize()
    return brute[~brute.index.duplicated(keep="last")].sort_index().astype("float64")


def hebdo(serie):
    return serie.resample("W-FRI").last()


# --- Relevé A : le contexte ---------------------------------------------------


def contexte(aujourdhui):
    """Indicateurs 2, 3, 8 et 9 : communs à toutes les valeurs."""
    c = {}
    il_y_a_un_an = (aujourdhui - timedelta(days=372)).isoformat()
    print("\nA. Le contexte, commun à toutes les valeurs")

    print("\n   2. Politique monétaire et taux — zone euro, courbe AAA de la BCE")
    try:
        dix = serie_bce(SERIE_TAUX_10, il_y_a_un_an)
        trois = serie_bce(SERIE_TAUX_3M, il_y_a_un_an)
        depot = serie_bce(SERIE_DEPOT, il_y_a_un_an)
        jour, t10 = dix[-1]
        _, t3 = valeur_au(trois, jour)
        un_an_avant = (date.fromisoformat(jour) - timedelta(days=365)).isoformat()
        _, t10_avant = valeur_au(dix, un_an_avant)
        _, dfr = valeur_au(depot, jour)
        _, dfr_avant = valeur_au(depot, un_an_avant)
        c.update(taux_10=t10, pente=t10 - t3)
        print(f"      au {jour} : taux de dépôt {fr(dfr)} % ({fr(dfr - dfr_avant, signe=True)} pt "
              f"sur un an), 3 mois {fr(t3)} %, 10 ans {fr(t10)} %")
        print(f"      pente 10 ans − 3 mois : {fr(t10 - t3, signe=True)} pt"
              f"{'  ← courbe inversée' if t10 < t3 else ''} ; "
              f"10 ans sur un an : {fr(t10 - t10_avant, signe=True)} pt")
    except Exception as erreur:  # noqa: BLE001 - signale, puis bloc vide
        signaler("BCE, taux", erreur)

    print("\n   9. Croissance et inflation — Eurostat")
    try:
        infl = serie_eurostat("prc_hicp_minr", {"geo": "EA", "unit": "RCH_A",
                                                "coicop18": "TOTAL", "lastTimePeriod": 13})
        pib = serie_eurostat("namq_10_gdp", {"geo": "EA", "unit": "CLV_PCH_SM", "s_adj": "SCA",
                                             "na_item": "B1GQ", "lastTimePeriod": 5})
        mois, pi = infl[-1]
        trimestre, g = pib[-1]
        c.update(inflation=pi, croissance_nominale=g + pi)
        print(f"      inflation sur un an ({mois}) : {fr(pi, 1)} % ; "
              f"un an plus tôt : {fr(infl[0][1], 1)} %")
        print(f"      PIB réel sur un an ({trimestre}) : {fr(g, 1)} % ; "
              f"croissance nominale approchée : {fr(g + pi, 1)} %")
        if "taux_10" in c:
            c["taux_reel"] = c["taux_10"] - pi
            print(f"      taux réel à 10 ans, ex post : {fr(c['taux_reel'], signe=True)} %")
    except Exception as erreur:  # noqa: BLE001 - signale, puis bloc vide
        signaler("Eurostat", erreur)

    print("\n   3. Crédit — BCE, BRI, et procuration de marché")
    try:
        prets = serie_bce(SERIE_PRETS_SNF, (aujourdhui - timedelta(days=500)).isoformat()[:7])
        mois, croissance = prets[-1]
        _, avant = valeur_au(prets, prets[-13][0]) if len(prets) >= 13 else (None, None)
        c["credit"] = croissance
        print(f"      prêts aux sociétés non financières, sur un an ({mois}) : "
              f"{fr(croissance, 1, signe=True)} % ; douze mois plus tôt : "
              f"{fr(avant, 1, signe=True)} %")
    except Exception as erreur:  # noqa: BLE001 - signale, puis ligne vide
        signaler("BCE, crédit", erreur)
    try:
        ecart = serie_bri(str(aujourdhui.year - 3))
        trimestre, gap = ecart[-1]
        c["ecart_credit"] = gap
        alerte = "  ← au-dessus du seuil d'alerte" if gap > S_ECART_CREDIT else ""
        print(f"      écart crédit/PIB à sa tendance, France ({trimestre}) : "
              f"{fr(gap, 1, signe=True)} pt{alerte}")
    except Exception as erreur:  # noqa: BLE001 - signale, puis ligne vide
        signaler("BRI", erreur)
    try:
        debut = (aujourdhui - timedelta(days=120)).isoformat()
        hy = historique(CREDIT_HY, debut, True)["Close"]
        gov = historique(CREDIT_GOV, debut, True)["Close"]
        r = 100 * ((au(hy, aujourdhui) / au(hy, aujourdhui - timedelta(weeks=13)))
                   - (au(gov, aujourdhui) / au(gov, aujourdhui - timedelta(weeks=13))))
        print(f"      HYG − IEF sur 13 semaines : {fr(r, signe=True)} pt "
              "(négatif quand l'écart de crédit s'élargit)")
    except Exception as erreur:  # noqa: BLE001 - signale, puis ligne vide
        signaler("Yahoo, crédit", erreur)

    print("\n   8. Change")
    try:
        eur = historique(CHANGE, (aujourdhui - timedelta(days=400)).isoformat(), True)["Close"]
        maintenant = au(eur, aujourdhui)
        un_an = variation(maintenant, au(eur, aujourdhui - timedelta(days=365)))
        print(f"      EURUSD : {fr(maintenant, 4)} ; sur un an : {fr(un_an, signe=True)} %")
    except Exception as erreur:  # noqa: BLE001 - signale, puis ligne vide
        signaler("Yahoo, change", erreur)
    return c


# --- Relevé B : une fiche par valeur ------------------------------------------


def fiche(ticker, isin, ctx, marche, amf, aujourdhui, outils):
    """Indicateurs 1, 4, 5, 6, 7, 8 et 10 pour une valeur. Rend un dict de résultats."""
    p_valeur_student, mco, _ = outils
    t = yf.Ticker(ticker)
    res = {"ticker": ticker}
    print(f"\n── {ticker} " + "─" * (70 - len(ticker)))

    try:
        info = t.info
    except Exception as erreur:  # noqa: BLE001 - signale, puis champs du jour vides
        signaler(f"{ticker}, info", erreur)
        info = {}

    # 1. Attentes
    try:
        tendance = t.eps_trend
        revisions = t.eps_revisions
        estimation = t.earnings_estimate
        an, suivant = tendance.loc["0y"], tendance.loc["+1y"]
        rev0 = variation(an["current"], an["90daysAgo"])
        rev1 = variation(suivant["current"], suivant["90daysAgo"])
        hausses = sum(nombre(revisions.loc[p, "upLast30days"]) or 0 for p in ("0y", "+1y"))
        baisses = sum(nombre(revisions.loc[p, "downLast30days"]) or 0 for p in ("0y", "+1y"))
        diffusion = (hausses - baisses) / (hausses + baisses) if hausses + baisses else None
        attendue = variation(suivant["current"], an["current"])
        e0 = estimation.loc["0y"]
        dispersion = (100 * (nombre(e0["high"]) - nombre(e0["low"])) / abs(nombre(e0["avg"]))
                      if nombre(e0["avg"]) else None)
        res.update(revision=rev0, diffusion=diffusion)
        print(f"   1. BPA attendu, exercice en cours : {fr(nombre(an['current']))} "
              f"(90 j : {fr(rev0, 1, signe=True)} % {fleche(rev0, S_REVISION)}) ; "
              f"suivant : {fr(nombre(suivant['current']))} ({fr(rev1, 1, signe=True)} % "
              f"{fleche(rev1, S_REVISION)})")
        print(f"      diffusion 30 j : {fr(diffusion, signe=True)} "
              f"{fleche(diffusion, S_DIFFUSION)} "
              f"({int(hausses)} hausses, {int(baisses)} baisses) ; croissance attendue N+1/N : "
              f"{fr(attendue, 1, signe=True)} % ; dispersion : {fr(dispersion, 0)} % "
              f"sur {int(nombre(e0['numberOfAnalysts']) or 0)} analystes")
        recent = nombre(info.get("trailingEps"))
        coherence = rapport(nombre(an["current"]), recent)
        alerte = ("  ⚠ définitions probablement différentes"
                  if coherence and not 1 / TOLERANCE_BPA <= coherence <= TOLERANCE_BPA else "")
        print(f"      BPA des douze derniers mois : {fr(recent)} ; attendu / récent : "
              f"{fr(coherence)}{alerte}")
    except Exception as erreur:  # noqa: BLE001 - signale, puis bloc vide
        signaler(f"{ticker}, consensus", erreur)

    # Cours, comptes, actions : la matière des indicateurs 4 à 7
    debut = (aujourdhui - timedelta(days=366 * (HORIZON + 1))).isoformat()
    try:
        brut = historique(ticker, debut, False)
        controler_saut(ticker, brut)
        periodes = comptes(t)
        actions = serie_actions(t, debut)
    except Exception as erreur:  # noqa: BLE001 - signale, puis fiche réduite
        signaler(f"{ticker}, cours et comptes", erreur)
        return res
    cours = au(brut["Close"], aujourdhui)
    passe = aujourdhui - timedelta(days=round(365.25 * HORIZON))
    exercices = publies(periodes, aujourdhui)

    # 4. Multiples
    per = nombre(info.get("trailingPE"))
    per_prev = nombre(info.get("forwardPE"))
    g_impl = None if per is None or per <= 0 else 100 * (TAUX_ACTUALISATION - 1 / per)
    prime = (None if per is None or per <= 0 or "taux_10" not in ctx
             else 100 / per - ctx["taux_10"])
    res.update(per=per, g_implicite=g_impl)
    exigeant = ("  ← au-dessus de la croissance longue"
                if g_impl and g_impl > CROISSANCE_LONGUE else "")
    print(f"   4. PER {fr(per)} · PER prévisionnel {fr(per_prev)} · croissance implicite "
          f"{fr(g_impl, 1, signe=True)} %{exigeant}")
    print(f"      rendement bénéficiaire − taux 10 ans : {fr(prime, signe=True)} pt")
    divisions = brut.loc[brut.index > pd.Timestamp(passe), "Stock Splits"].fillna(0)
    avant = publies(periodes, passe)
    if (divisions != 0).any():
        print(f"      décomposition sur {HORIZON} ans : division d'actions dans la fenêtre — vide")
    elif avant and exercices:
        n0 = avant[-1][1].get("resultat_net")
        n1 = exercices[-1][1].get("resultat_net")
        a0, a1 = actions_au(actions, passe), actions_au(actions, aujourdhui)
        p0 = au(brut["Close"], passe)
        tr0, tr1 = au(brut["Adj Close"], passe), au(brut["Adj Close"], aujourdhui)
        bpa0, bpa1 = rapport(n0, a0), rapport(n1, a1)
        if None in (bpa0, bpa1, p0, cours) or bpa0 <= 0 or bpa1 <= 0:
            print(f"      décomposition sur {HORIZON} ans : bénéfice négatif ou absent — vide")
        else:
            prix = 100 * math.log(cours / p0)
            benefice = 100 * math.log(bpa1 / bpa0)
            multiple = prix - benefice
            dividendes = 100 * math.log(tr1 / tr0) - prix
            res.update(part_prix=prix, part_benefice=benefice, part_multiple=multiple)
            print(f"      décomposition sur {HORIZON} ans, en points de log : bénéfice "
                  f"{fr(benefice, 1, signe=True)} + multiple {fr(multiple, 1, signe=True)} "
                  f"+ dividendes {fr(dividendes, 1, signe=True)} = "
                  f"{fr(benefice + multiple + dividendes, 1, signe=True)}")
            print(f"      (exercice {avant[-1][0].year} contre {exercices[-1][0].year}, "
                  f"PER {fr(p0 / bpa0, 1)} → {fr(cours / bpa1, 1)})")

    # 5. Levier
    if exercices:
        cloture, dernier = exercices[-1]
        dette_ebitda = rapport(dernier.get("dette"), dernier.get("ebitda"))
        couverture = rapport(dernier.get("ebit"), dernier.get("interets"))
        dynamique = None
        if len(exercices) >= 2:
            precedent = exercices[-2][1]
            vd = variation(dernier.get("dette"), precedent.get("dette"))
            ve = variation(dernier.get("ebitda"), precedent.get("ebitda"))
            dynamique = None if vd is None or ve is None else vd - ve
        du_jour = nombre(info.get("totalDebt"))
        annuelle = nombre(dernier.get("dette"))
        discordance = ""
        if du_jour and annuelle and not (
            1 / TOLERANCE_DETTE <= annuelle / du_jour <= TOLERANCE_DETTE
        ):
            discordance = (f"  ⚠ sources discordantes : dette annuelle {fr(annuelle / 1e9, 1)} "
                           f"Md, dette du jour {fr(du_jour / 1e9, 1)} Md")
            dette_ebitda = dynamique = None
        res.update(dette_ebitda=dette_ebitda, couverture=couverture, dynamique=dynamique)
        alertes = [m for m, test in (
            ("dette lourde", dette_ebitda is not None and dette_ebitda > S_DETTE),
            ("couverture tendue", couverture is not None and couverture < S_COUVERTURE),
            ("levier qui monte", dynamique is not None and dynamique > S_DYNAMIQUE),
        ) if test]
        print(f"   5. exercice {cloture.year} : dette/EBITDA {fr(dette_ebitda)} · couverture des "
              f"intérêts {fr(couverture, 1)} · dette − EBITDA sur un an "
              f"{fr(dynamique, 1, signe=True)} pt"
              + (f"  ← {', '.join(alertes)}" if alertes else "") + discordance)

        # 6. Marges
        marges = [100 * m for _, p in exercices
                  if (m := rapport(p.get("resultat_op"), p.get("chiffre_affaires"))) is not None]
        if marges:
            moyenne = sum(marges) / len(marges)
            ecart = marges[-1] - moyenne
            res["ecart_marge"] = ecart
            haute = "  ← au-dessus de sa moyenne" if ecart > S_MARGE else ""
            print(f"   6. marge opérationnelle {fr(marges[-1], 1)} % · moyenne de "
                  f"{len(marges)} exercices {fr(moyenne, 1)} % · écart "
                  f"{fr(ecart, 1, signe=True)} pt{haute}")
        if len(exercices) >= 2:
            p0_, p1_ = exercices[-2][1], exercices[-1][1]
            n0, n1 = p0_.get("resultat_net"), p1_.get("resultat_net")
            ca0, ca1 = p0_.get("chiffre_affaires"), p1_.get("chiffre_affaires")
            if all(v is not None and v > 0 for v in (n0, n1, ca0, ca1)):
                volume = 100 * math.log(ca1 / ca0)
                marge = 100 * math.log(n1 / n0) - volume
                print(f"      résultat net sur un an, en points de log : chiffre d'affaires "
                      f"{fr(volume, 1, signe=True)} + marge nette {fr(marge, 1, signe=True)}")

    # 7. Dilution
    if (divisions != 0).any():
        print("   7. division d'actions dans la fenêtre — dilution laissée vide")
    else:
        maintenant = actions_au(actions, aujourdhui)
        d1 = variation(maintenant, actions_au(actions, aujourdhui - timedelta(days=365)))
        d3 = variation(maintenant, actions_au(actions, passe))
        res["dilution"] = d1
        lecture = ("  ← émet" if d1 is not None and d1 > S_DILUTION
                   else "  ← rachète" if d1 is not None and d1 < -S_DILUTION else "")
        print(f"   7. nombre d'actions sur un an {fr(d1, 1, signe=True)} % · sur {HORIZON} ans "
              f"{fr(d3, 1, signe=True)} %{lecture}")

    # 8. Sensibilité au change, marché compris
    if marche is not None:
        r = hebdo(brut["Close"]).pct_change(fill_method=None).rename("VALEUR")
        d = pd.concat([r, marche], axis=1).dropna().tail(SEMAINES)
        b, tt, ddl, _ = mco(list(d["VALEUR"]), [list(d["MARCHE"]), list(d["EURUSD"])])
        p = p_valeur_student(tt[2], ddl)
        res.update(b_change=b[2], p_change=p)
        print(f"   8. sur {len(d)} semaines : bêta {fr(b[1])} · b_EURUSD {fr(b[2], signe=True)} "
              f"(t = {fr(tt[2], signe=True)}, p = {fr(p, 4)})")

    # 10. Positionnement
    v = brut["Volume"].replace(0, float("nan")).dropna()
    volume = (v.tail(20).mean() / v.tail(250).mean()) if len(v) >= 250 else None
    res["volume"] = volume
    courtes = ""
    if amf is not None and isin:
        maintenant, n = courtes_au(amf, isin, aujourdhui)
        avant_, _ = courtes_au(amf, isin, aujourdhui - timedelta(days=90))
        res.update(courtes=maintenant, courtes_var=maintenant - avant_)
        courtes = (f"positions courtes publiées {fr(maintenant)} % du capital, {n} détenteur(s), "
                   f"{fr(maintenant - avant_, signe=True)} pt sur 90 j"
                   + ("  ← notable" if maintenant >= S_COURTES else "") + " · ")
    elif amf is not None:
        courtes = "ISIN inconnu, positions courtes non lues (--isin) · "
    print(f"  10. {courtes}volume 20 j / 250 j {fr(volume)}"
          + ("  ← inhabituel" if volume and volume > S_VOLUME else ""))
    return res


# --- Synthèse -----------------------------------------------------------------


def synthese(resultats, outils):
    """Marqueurs de boom et de bascule, au sens du module 9 ; Holm sur b_EURUSD."""
    _, _, holm = outils
    avec_change = [r for r in resultats if "p_change" in r]
    rejets = dict(zip((r["ticker"] for r in avec_change),
                      holm([r["p_change"] for r in avec_change]), strict=True))
    print("\nSynthèse — marqueurs déclarés au module 9 (✓ présent, · absent, ? non mesurable)")
    print(f"   {'valeur':<8} {'B1':>3} {'B2':>3} {'B3':>3} {'B4':>3}  {'boom':>4}   "
          f"{'R1':>3} {'R2':>3} {'R3':>3}  {'bascule':>7}   change*")

    def marque(valeurs, test):
        if any(x is None for x in valeurs):
            return "?"
        return "✓" if test(*valeurs) else "·"

    for r in resultats:
        g = r.get
        boom = [
            marque([g("revision")], lambda x: x >= S_REVISION),
            marque([g("part_prix"), g("part_benefice"), g("part_multiple")],
                   lambda p, b, m: p > 0 and b > 0 and m > b),
            marque([g("dynamique")], lambda x: x > S_DYNAMIQUE),
            marque([g("dilution")], lambda x: x > S_DILUTION),
        ]
        bascule = [
            marque([g("revision"), g("part_prix"), g("part_multiple")],
                   lambda x, p, m: x <= -S_REVISION and p > 0 and m > 0),
            marque([g("ecart_marge"), g("g_implicite")],
                   lambda e, gi: e > S_MARGE and gi > CROISSANCE_LONGUE),
            marque([g("courtes_var")], lambda x: x > 0.5),
        ]
        change = "oui" if rejets.get(r["ticker"]) else ("non" if r["ticker"] in rejets else "?")
        print(f"   {r['ticker']:<8} {boom[0]:>3} {boom[1]:>3} {boom[2]:>3} {boom[3]:>3}  "
              f"{boom.count('✓'):>2}/4   {bascule[0]:>3} {bascule[1]:>3} {bascule[2]:>3}  "
              f"{bascule.count('✓'):>5}/3   {change}")
    print("   B1 révisions ↑ · B2 hausse du cours et du bénéfice, le multiple en portant la plus "
          "grande part · B3 dette plus vite que l'EBITDA · B4 émission d'actions")
    print("   R1 révisions ↓ alors que le multiple a contribué à la hausse · R2 marge haute et "
          "croissance implicite exigeante · R3 positions courtes en hausse")
    print(f"   * b_EURUSD significatif après Holm sur {len(avec_change)} valeurs, "
          f"au seuil de {fr(100 * ALPHA, 0)} %.")
    print("   Un marqueur n'est pas un signal : le module 9 dit ce qu'une combinaison permet de "
          "dire, et surtout ce qu'elle ne permet pas.")


def main():
    parser = argparse.ArgumentParser(
        description="Chiffre les dix indicateurs du cours « Soros et Steinhardt » et les lit."
    )
    parser.add_argument("tickers", nargs="*", default=VALEURS_DEFAUT,
                        help="tickers Yahoo (défaut : les huit valeurs du cours fondamentaux)")
    parser.add_argument("--isin", action="append", default=[], metavar="TICKER=ISIN",
                        help="ISIN d'une valeur hors table, pour lire ses positions courtes")
    args = parser.parse_args()

    isin = dict(ISIN)
    for couple in args.isin:
        ticker, _, code = couple.partition("=")
        if not code:
            parser.error(f"--isin attend TICKER=ISIN, pas « {couple} »")
        isin[ticker.strip().upper()] = code.strip().upper()

    outils = voisins()
    aujourdhui = date.today()
    print(f"Relevé du {aujourdhui.isoformat()} — les comptes sont réputés publiés "
          f"{DECALAGE} jours après la clôture.")
    ctx = contexte(aujourdhui)

    print("\nB. Une fiche par valeur")
    debut = (aujourdhui - timedelta(days=366 * (HORIZON + 1))).isoformat()
    try:
        marche = pd.DataFrame({
            "MARCHE": hebdo(historique(INDICE, debut, False)["Close"]).pct_change(fill_method=None),
            "EURUSD": hebdo(historique(CHANGE, debut, True)["Close"]).pct_change(fill_method=None),
        })
    except Exception as erreur:  # noqa: BLE001 - signale, puis indicateur 8 vide
        signaler("Yahoo, marché et change", erreur)
        marche = None
    try:
        amf = positions_courtes()
    except Exception as erreur:  # noqa: BLE001 - signale, puis positions courtes vides
        signaler("AMF, positions courtes", erreur)
        amf = None

    resultats = [fiche(tk.upper(), isin.get(tk.upper()), ctx, marche, amf, aujourdhui, outils)
                 for tk in args.tickers]
    synthese(resultats, outils)
    return 0


if __name__ == "__main__":
    sys.exit(main())
