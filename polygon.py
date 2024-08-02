import requests



def read_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            keys[name] = value
    return keys

api_keys = read_api_keys('api_key.txt')

api_key = api_keys.get("API_KEY")

# URL de l'API
url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2023-01-09/2023-02-10"
# Clé API

# Paramètres de la requête
params = {
    "adjusted": "true",
    "sort": "asc",
    "apiKey": api_key
}

# Effectuer la requête
response = requests.get(url, params=params)

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Erreur : {response.status_code}")
