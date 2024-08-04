import requests
import json
import time

def read_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            keys[name] = value
    return keys

api_keys = read_api_keys('api_keys.txt')
api_key = api_keys.get("API_KEY")

# Liste des tickers pour 20 entreprises différentes
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "TSLA", "NVDA", "BRK.B", "JNJ", "V", 
    "WMT", "JPM", "MA", "PG", "DIS", 
    "ADBE", "NFLX", "PYPL", "INTC", "KO"
]

# URL de base de l'API
base_url = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2010-01-09/2024-08-02"

# Paramètres de la requête
params = {
    "adjusted": "true",
    "sort": "asc",
    "apiKey": api_key
}

# Itérer sur chaque ticker pour récupérer et sauvegarder les données
for ticker in tickers:
    url = base_url.format(ticker=ticker)
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Data for {ticker}: {data}")
        results = data["results"]
        high_low_time = []
        for result in results:
            high_low_time.append([result["h"], result["l"], result["t"]])
        
        # Sauvegarder les données dans un fichier JSON
        filename = f'high_low_time_{ticker}.json'
        with open(filename, 'w') as json_file:
            json.dump(high_low_time, json_file)
    else:
        print(f"Erreur pour {ticker} : {response.status_code}")
    
    # Attendre 21 secondes avant la prochaine requête pour respecter les limitations de l'API
    time.sleep(21)
