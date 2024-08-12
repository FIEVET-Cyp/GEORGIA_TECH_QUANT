import os
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, FR
import time
from get_data_options import fetch_option_data, fetch_stock_data

def read_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            keys[name] = value
    return keys

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

def extract_open_prices_and_timestamps(data):
    extracted_data = []
    if 'results' in data:
        for result in data['results']:
            open_price = result.get('o')
            timestamp = result.get('t')
            if open_price is not None and timestamp is not None:
                extracted_data.append({'timestamp': timestamp, 'open_price': open_price})
    return extracted_data

def calculate_time_until_maturity(maturity_date, current_date):
    time_until_maturity = maturity_date - current_date
    return time_until_maturity.days

# Load API keys
api_keys = read_api_keys('api_keys.txt')
api_key = api_keys.get("API_KEY")

# List of tickers
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "TSLA", "JNJ", "V", 
    "JPM", "MA", "PG", "DIS", 
    "ADBE", "NFLX", "PYPL", "INTC", "KO"
]

# Directory containing the JSON files
directory = 'mean_2std'

for ticker in tickers:
    input_file_path = os.path.join(directory, f'filtered_high_low_changes_{ticker}_with_intensity.json')
    output_file_path = os.path.join(directory, f'filtered_high_low_changes_{ticker}_with_intensity.json')
    
    if os.path.exists(input_file_path):
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        
        for element in data:
            print(element.keys())
            if ('option_data_p' in element.keys() and element["option_data_p"] == [] and element["option_data_p"] != None) or 'option_data_p' not in element.keys():
                if ('option_data_p' in element.keys() and element["option_data_p"] == [] and element["option_data_p"] != None):
                    print("1")
                if 'options_data_p' not in element.keys():
                    print("2") 
                
                
                timespan_str = element.get("timestamp", "")
                if timespan_str:
                    try:
                        timespan = datetime.strptime(timespan_str, '%Y-%m-%dT%H:%M:%S').date()
                        maturity = correct_maturity(timespan)
                        strike_price = round((element["high"] + element["low"]) / 2, 2)
                        strike_price = nearest_strike_price(strike_price)

                        maturity_str = maturity.strftime('%y%m%d')
                        strike_price_str = f'{int(strike_price * 1000):08d}'
                        option_symbol = f'O:{ticker}{maturity_str}P{strike_price_str}'

                        start_date = timespan.strftime('%Y-%m-%d')
                        end_date = (timespan + timedelta(days=1)).strftime('%Y-%m-%d')

                        option_data = fetch_option_data(api_key, option_symbol, 1, 'minute', start_date, end_date)
                        # print(option_data)
                        open_prices = extract_open_prices_and_timestamps(option_data)

                        # Add option data to the element
                        element["option_data_p"] = open_prices

                        # Calculate and add time until maturity
                        time_until_maturity = calculate_time_until_maturity(maturity, timespan)
                        element["time_until_maturity"] = time_until_maturity
                        
                    except ValueError as e:
                        print(f"Error parsing date {timespan_str}: {e}")
                time.sleep(21)


                # Save the modified JSON back to the file
                with open(output_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                
                print(f"Modified JSON saved to {output_file_path}")
    
    else:
        print(f"File {input_file_path} does not exist.")
    
    # Sleep to avoid hitting API rate limits
