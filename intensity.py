import json
import os

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
    input_file_path = os.path.join(directory, f'filtered_high_low_changes_{ticker}.json')
    output_file_path = os.path.join(directory, f'filtered_high_low_changes_{ticker}_with_intensity.json')
    
    # Check if the input file exists
    if os.path.exists(input_file_path):
        # Read the JSON file
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        
        # Add intensity to each element
        for element in data:
            high = element.get("high", 0)
            low = element.get("low", 0)
            element["intensity"] = high - low
        
        # Save the modified JSON back to the file
        with open(output_file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"Modified JSON saved to {output_file_path}")
    else:
        print(f"File {input_file_path} does not exist.")
