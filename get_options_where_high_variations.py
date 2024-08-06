from datetime import datetime, timedelta
from get_data_options import fetch_option_data, fetch_stock_data
import os
import json
from dateutil.relativedelta import relativedelta, FR
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

tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "TSLA", "JNJ", "V", 
    "JPM", "MA", "PG", "DIS", 
    "ADBE", "NFLX", "PYPL", "INTC", "KO"
]

folder_path = 'mean_2std'

def correct_maturity(input_date):
    first_day_next_month = (input_date + relativedelta(day=1, months=1))
    third_friday = first_day_next_month + relativedelta(weekday=FR(3))
    return third_friday

def nearest_strike_price(price):
    if price < 10:
        interval = 1
    elif 10 <= price < 100:
        interval = 5
    elif 100 <= price < 200:
        interval = 10
    elif 200 <= price < 500:
        interval = 10
    else:
        interval = 10
    nearest_strike = round(price / interval) * interval
    return nearest_strike

def extract_open_prices_and_timestamps(data, option_symbol):
    extracted_data = []
    if 'results' in data:
        for result in data['results']:
            open_price = result.get('o')
            timestamp = result.get('t')
            if open_price is not None and timestamp is not None:
                extracted_data.append({'timestamp': timestamp, 'open_price': open_price})
    
    output_file = f'{ticker}{maturity_str}P{strike_price_str}'+'.json'
    with open(output_file, 'w') as json_file:
        json.dump(extracted_data, json_file)
    
    # output_file = f'{option_symbol}.json'
    # with open(output_file, 'w') as json_file:
    #     json.dump(extracted_data, json_file, indent=4)
    print(f"Data successfully saved to {output_file}")

# Process each ticker
for ticker in tickers:
    print(f"Processing {ticker}...")

    file_name = f'filtered_high_low_changes_{ticker}.json'
    file_path = os.path.join(folder_path, file_name)
    
    if not os.path.exists(file_path):
        print(f"No data file for {ticker}")
        continue

    with open(file_path, 'r') as json_file:
        filtered_data = json.load(json_file)

    if not filtered_data:
        print(f"No data available for {ticker}")
        continue

    j1 = filtered_data[0]["timestamp"]
    date_only = datetime.strptime(j1, '%Y-%m-%dT%H:%M:%S').date()
    maturity = correct_maturity(date_only)
    strike_price = round((filtered_data[0]["high"] + filtered_data[0]["low"]) / 2, 2)
    strike_price = nearest_strike_price(strike_price)
    print(f"Nearest Strike Price: {strike_price}")

    maturity_str = maturity.strftime('%y%m%d')
    strike_price_str = f'{int(strike_price * 1000):08d}'
    option_symbol = f'O:{ticker}{maturity_str}P{strike_price_str}'

    start_date = date_only.strftime('%Y-%m-%d')
    end_date = (date_only + relativedelta(days=10)).strftime('%Y-%m-%d')

    print(f"Fetching data for {option_symbol} from {start_date} to {end_date}...")

    try:
        data = fetch_option_data(api_key, option_symbol, 1, 'day', '2010-01-09', '2024-08-02')
        print(data)
        extract_open_prices_and_timestamps(data, option_symbol)
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
    
    # Sleep to avoid hitting API rate limits
    time.sleep(21)
