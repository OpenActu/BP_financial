# Module 2 — Les quatre dates d'un ratio ⭐

**Prérequis :** [module 1](01-de-quoi-un-ratio-est-le-rapport.md).
**Ce qu'on établit ici :** qu'un ratio fondamental porte quatre dates distinctes, que la source n'en fournit que deux, et que l'absence de la troisième interdit tout backtest — pas le rend difficile : l'interdit.

---

## 2.1 — Les quatre dates

Écrivons le PER avec toutes ses dates apparentes :

$$\text{PER} = \frac{P(t_{\text{cours}})}{E(t_{\text{exercice}})} \quad\text{connu depuis } t_{\text{publication}},\ \text{lu à } t_{\text{lecture}}$$

| # | Date | Ce qu'elle est | Rythme |
|---|---|---|---|
| 1 | **$t_{\text{cours}}$** | l'instant du prix au numérateur | continu |
| 2 | **$t_{\text{exercice}}$** | la fin de la période que le dénominateur résume | trimestriel ou annuel |
| 3 | **$t_{\text{publication}}$** | le jour où ce dénominateur est devenu **public** | 4 à 10 semaines après 2 |
| 4 | **$t_{\text{lecture}}$** | le jour où l'on interroge la source | l'appel |

Elles ne coïncident jamais. Un PER lu aujourd'hui rapporte un prix de ce matin à
un bénéfice d'un exercice clos il y a des mois, publié il y a des semaines.

> 🔑 **La seule date qui décide de ce qu'un investisseur savait, et quand, est la
> troisième.** Les deux premières se lisent partout ; la troisième est celle qui
> gouverne toute étude rétrospective — et c'est précisément celle que la source
> ne donne pas.

## 2.2 — Ce que la source fournit, et ce qu'elle tait

[`import_fondamentaux.py`](../../../../../python/import_fondamentaux.md) écrit une
colonne `DATE`. Elle vaut $t_{\text{lecture}}$ — la date de l'appel, rien d'autre.

| Date | Fournie ? |
|---|---|
| $t_{\text{cours}}$ | ✅ implicitement, c'est le jour de l'appel en séance |
| $t_{\text{exercice}}$ | ⚠️ jamais explicitement ; « trailing » signifie *douze mois glissants*, sans dire lesquels |
| $t_{\text{publication}}$ | ❌ **absente** |
| $t_{\text{lecture}}$ | ✅ colonne `DATE` |

Deux sur quatre. C'est suffisant pour décrire une entreprise **aujourd'hui**, et
insuffisant pour dire quoi que ce soit d'hier.

## 2.3 — Pourquoi cela interdit le backtest

Un écran *value* rétrospectif demanderait : *quel était le PER de cette valeur au
31 décembre 2020, tel qu'un investisseur pouvait le connaître ce jour-là ?*
Il faudrait pour cela le bénéfice **publié avant** cette date. La source ne rend
que le dernier connu, celui d'aujourd'hui.

Utiliser le ratio d'aujourd'hui pour trancher une décision de 2020, c'est
**donner au passé la connaissance du futur** — le regard en avant décrit au
[§ 4.1 du cours trading](../trading/04-les-pieges-du-passage-a-l-acte.md), mais
dans sa version la plus grossière : non pas une séance d'avance, plusieurs
années.

> ⚠️ **Ce biais ne se corrige pas par prudence, il ne se corrige pas du tout.**
> Un écran fondamental construit sur ces données donnera d'excellents résultats
> rétrospectifs par pure construction : les sociétés dont on connaît aujourd'hui
> les bons comptes sont celles qui ont bien traversé la période. Le résultat
> mesure la sélection, pas la stratégie.

Deux aggravations, à nommer ensemble :

- **Le biais du survivant.** Un univers de tickers constitué aujourd'hui exclut
  les faillites et les radiations. Aucune des huit valeurs du fil rouge n'a
  disparu — c'est précisément pourquoi on peut les interroger.
- **La révision des comptes.** Un chiffre publié puis retraité n'existe plus dans
  la source sous sa forme d'origine. On lit la version corrigée, jamais celle sur
  laquelle le marché avait réagi.

## 2.4 — « Trailing » et « forward » : un fait et une opinion

La source rend deux PER, et ils ne sont pas de même nature.

| Colonne | Dénominateur | Statut |
|---|---|---|
| `PER` | bénéfice des douze derniers mois **constatés** | un fait comptable, daté |
| `PER_PREV` | bénéfice **attendu** des douze prochains mois | une **moyenne d'opinions d'analystes** |

Sur AIR.PA au 30 août 2026 : `PER` = **27,04**, `PER_PREV` = **23,31**.

L'écart de 3,7 points ne dit rien de l'entreprise. Il dit que le consensus
d'analystes attend une hausse du bénéfice d'environ $27{,}04/23{,}31 - 1 = 16\,\%$.
C'est une prévision, avec tout ce que le [cours alpha](../alpha/README.md) apprend
à en penser :

- elle n'est accompagnée d'aucun intervalle ;
- elle est produite par des analystes dont les incitations ne sont pas neutres ;
- elle est **révisée en continu**, donc un `PER_PREV` d'aujourd'hui n'est pas
  celui d'il y a un mois, sans que rien ne l'indique.

> **Un `PER_PREV` bas n'est pas une valeur bon marché : c'est une valeur dont les
> analystes attendent une forte croissance.** Ce sont deux affirmations très
> différentes, et la seconde peut être fausse.

## 2.5 — Ce qui reste possible

Tout n'est pas perdu — mais le domaine du licite est étroit et il faut le dire :

| Usage | Licite ? |
|---|---|
| Décrire une entreprise **aujourd'hui** | ✅ |
| Comparer plusieurs entreprises **au même instant** (§ [module 4](04-un-ratio-n-existe-que-relatif.md)) | ✅ — c'est le seul usage vraiment solide |
| Construire une série et **la constituer soi-même**, appel après appel, en horodatant | ✅ `import_fondamentaux.py --archiver` — mais il faut commencer aujourd'hui |
| Reconstituer un ratio passé | ⚠️ § 2.6 — possible sur **3 à 4 ans**, là où la couverture existe |
| Backtester un écran fondamental | ⚠️ sur cette profondeur seulement : de quoi illustrer une méthode, pas valider un facteur |
| Dater un franchissement de seuil de valorisation | ⚠️ idem |

La troisième ligne est la seule voie honnête vers un historique : **archiver**
les appels au fil du temps, chacun daté de son $t_{\text{lecture}}$. C'est
laborieux et lent, et cela ne donne rien avant plusieurs années — mais c'est la
différence entre une base de données et une illusion.


## 2.6 — Aller chercher la troisième date

La conclusion du § 2.3 mérite d'être nuancée : la source en dit plus qu'il n'y
paraît. `get_earnings_dates()` rend les **dates d'annonce réelles** des
résultats — c'est exactement la troisième date, celle qui manquait.

[`reconstituer_fondamentaux.py`](../../../../../python/reconstituer_fondamentaux.md)
s'en sert pour apparier chaque exercice à sa publication, puis n'utilise à chaque
séance que le dernier exercice **déjà public**. Sur Airbus, le basculement tombe
le jour même de l'annonce, et non à la clôture de l'exercice :

| Séance | PER | Exercice utilisé |
|---|---|---|
| 2025-02-19 | 33,76 | 2023-12-31 |
| **2025-02-20** | **30,25** | **2024-12-31** |

Trois limites, à publier avec toute série ainsi reconstituée :

- **La couverture est inégale.** Airbus a 88 publications depuis 2004, BNP
  Paribas 87 — **LVMH aucune**. Sans elles, le script retombe sur un décalage
  conventionnel, et le signale dans une colonne dédiée.
- **La profondeur reste celle des comptes** : 4 exercices annuels, soit environ
  trois ans et demi de série.
- **Les retraitements survivent.** La source sert la version *actuelle* des
  comptes passés. La reconstruction corrige le regard en avant sur la **date**,
  pas sur le **contenu** — et le biais du survivant reste entier.

> 🔑 **Deux voies, à mener ensemble.** L'archivage horodate le présent, sans
> aucune approximation mais sans rien donner avant des années. La reconstruction
> donne trois ans tout de suite, au prix d'hypothèses qu'il faut nommer. Aucune
> ne remplace une base *point-in-time* professionnelle ; ensemble, elles font
> passer le sujet de « impossible » à « possible, et daté ».

## Ce qu'il faut retenir

1. Quatre dates, dont la plus importante — la publication — est absente.
2. L'absence n'est pas une gêne, c'est une interdiction : aucun backtest
   fondamental n'est possible avec cette source.
3. `PER` est un constat, `PER_PREV` une opinion d'analystes sans intervalle.
4. Le seul usage solide est la **comparaison transversale à un instant donné**.

---

⬅️ [Module 1 — De quoi un ratio est le rapport](01-de-quoi-un-ratio-est-le-rapport.md) ·
➡️ [Module 3 — Ce que la comptabilité laisse au choix](03-ce-que-la-comptabilite-laisse-au-choix.md) ·
🏠 [Sommaire du dépôt](../../sommaire/README.md)
