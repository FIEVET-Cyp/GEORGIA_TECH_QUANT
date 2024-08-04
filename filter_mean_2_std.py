import json
import pandas as pd
from datetime import datetime

def process_ticker_data(ticker):
    # Nom du fichier JSON à ouvrir
    filename = f'high_low_time_{ticker}.json'

    # Charger les données depuis le fichier JSON
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    # Extraire les prix les plus hauts (high), les plus bas (low) et les timestamps
    highs = [entry[0] for entry in data]  # Les prix les plus hauts
    lows = [entry[1] for entry in data]   # Les prix les plus bas
    timestamps = [datetime.fromtimestamp(entry[2] / 1000) for entry in data]  # Les timestamps convertis en datetime

    # Calculer les pourcentages d'écart entre le prix le plus haut et le prix le plus bas
    percentage_changes = []
    filtered_data = []

    for high, low, timestamp in zip(highs, lows, timestamps):
        if low != 0:  # Éviter la division par zéro
            percentage_change = ((high - low) / low) * 100
            percentage_changes.append(percentage_change)

    # Convertir en série Pandas pour faciliter les calculs
    df = pd.Series(percentage_changes)
    mean = df.mean()
    std_dev = df.std()
    threshold = mean + 2 * std_dev

    # Filtrer les données au-delà du seuil
    for i, change in enumerate(percentage_changes):
        if change > threshold:
            filtered_data.append({
                "high": highs[i],
                "low": lows[i],
                "percentage_change": change,
                "timestamp": timestamps[i].isoformat()
            })

    # Sauvegarder les données filtrées dans un fichier JSON
    filtered_filename = f'filtered_high_low_changes_{ticker}.json'
    with open(filtered_filename, 'w') as json_file:
        json.dump(filtered_data, json_file)

    print(f"Data beyond mean + 2 std dev saved to {filtered_filename} for {ticker}")

# Liste des tickers pour 20 entreprises différentes
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "TSLA", "NVDA", "BRK.B", "JNJ", "V", 
    "WMT", "JPM", "MA", "PG", "DIS", 
    "ADBE", "NFLX", "PYPL", "INTC", "KO"
]

# Traiter chaque ticker
for ticker in tickers:
    process_ticker_data(ticker)
