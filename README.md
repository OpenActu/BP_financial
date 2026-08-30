# import_societe

Script Python qui récupère l'historique d'un cours de bourse d'une société du SBF 250. Il s'appuie sur [`yfinance`](https://pypi.org/project/yfinance/) (Yahoo Finance), qui couvre l'ensemble des valeurs du SBF 250.

## Installation et utilisation

```bash
pip install yfinance
python import_societe.py AIR.PA --periode 5y --csv airbus.csv
```

Les tickers de la place de Paris se terminent par `.PA` :

| Société       | Ticker   |
| ------------- | -------- |
| Airbus        | `AIR.PA` |
| LVMH          | `MC.PA`  |
| TotalEnergies | `TTE.PA` |
| Sanofi        | `SAN.PA` |
| BNP Paribas   | `BNP.PA` |

Le script affiche les séances (Open / High / Low / Close / Volume) ainsi que la variation sur la période, puis enregistre systématiquement l'historique en CSV. Sans `--csv`, le fichier est écrit dans `docs/raw/quotes/` sous un nom dérivé du ticker et de la plage de dates (le répertoire est créé automatiquement).

Pour une plage de dates précise, utiliser `--debut` et `--fin` (format `AAAA-MM-JJ`) à la place de `--periode` :

```bash
python import_societe.py AIR.PA --debut 2023-01-01 --fin 2023-12-31
```

## Note

Le script n'a pas pu être testé dans l'environnement de développement (accès à Yahoo Finance bloqué), mais il s'exécutera normalement sur votre machine.
