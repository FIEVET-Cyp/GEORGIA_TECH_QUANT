import requests

def read_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            keys[name] = value
    return keys

def fetch_option_data(api_key, ticker, multiplier, timespan, start_date, end_date, adjusted=True, sort='asc'):
    base_url = 'https://api.polygon.io/v2/aggs/ticker'
    url = (f'{base_url}/{ticker}/range/{multiplier}/{timespan}/'
           f'{start_date}/{end_date}?adjusted={str(adjusted).lower()}&sort={sort}&apiKey={api_key}')
    response = requests.get(url)
    return response.json()

# Lecture de la clé API depuis le fichier
api_keys = read_api_keys('api_keys.txt')
api_key = api_keys.get("API_KEY")

# Exemple d'appel de la fonction
# data = fetch_option_data(api_key, 'O:TSLA230113C00015000', 1, 'day', '2023-01-01', '2023-01-11')
# print(data)



def fetch_stock_data(api_key, ticker, start_date, end_date, adjusted=True, sort='asc', sleep_time=21):
    base_url = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}"
    params = {
        "adjusted": str(adjusted).lower(),
        "sort": sort,
        "apiKey": api_key
    }

    url = base_url.format(ticker=ticker, start=start_date, end=end_date)
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        high_low_time = [[res["h"], res["l"], res["t"]] for res in results]
        return high_low_time
    else:
        print(f"Erreur pour {ticker} : {response.status_code}")
        return None
    