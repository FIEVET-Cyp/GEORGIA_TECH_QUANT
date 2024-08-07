import json
import os
from get_data_options import fetch_option_data, fetch_stock_data
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

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
    
    # Check if the input file exists
    if os.path.exists(input_file_path):
        # Read the JSON file
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        
        # Add delta_1w to each element
        for element in data:
            timespan_str = element.get("timestamp", "")
            if "delta_1w" not in element.keys() :
                if timespan_str:
                    try:
                        timespan = datetime.strptime(timespan_str, '%Y-%m-%dT%H:%M:%S')
                        time_1w = (timespan + relativedelta(days=7)).strftime('%Y-%m-%d')
                        timespan = timespan.strftime('%Y-%m-%d')
                        price_1w = fetch_stock_data(api_key,ticker, time_1w, time_1w)
                        price_spot = fetch_stock_data(api_key,ticker, timespan, timespan)
                        # Fetch stock data for delta_1w
                        if price_1w == None or price_spot == None:
                            element["delta_1w"] = None
                        else: 
                            element["delta_1w"] = price_1w - price_spot
                        print(element["delta_1w"])
                    except ValueError as e:
                        print(f"Error parsing date {timespan_str}: {e}")
            
                    # Save the modified JSON back to the file
                    with open(output_file_path, 'w') as file:
                        json.dump(data, file, indent=4)
                    
                    print(f"Modified JSON saved to {output_file_path}")
                else:
                    print(f"File {input_file_path} does not exist.")
