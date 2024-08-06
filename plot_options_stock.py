import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

# List of tickers
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "TSLA", "JNJ", "V", 
    "JPM", "MA", "PG", "DIS", 
    "ADBE", "NFLX", "PYPL", "INTC", "KO"
]

# Paths to the folders containing the JSON files
stock_folder_path = "open_close_time"
options_folder_path = "options"

# Function to extract strike price from filename
def extract_strike_price(filename):
    # The strike price is in the last 8 characters before the file extension
    # e.g., AAPL220916P00170000 -> 00170000 (strike price is 170.00)
    strike_price_str = filename[-13:-5]
    return int(strike_price_str) / 1000

# Function to plot stock and option prices over time with dual y-axes and strike price line
def plot_stock_and_option_prices(tickers, stock_folder_path, options_folder_path):
    for ticker in tickers:
        stock_file_path = os.path.join(stock_folder_path, f"open_close_time_{ticker}.json")
        option_files = [f for f in os.listdir(options_folder_path) if f.startswith(ticker)]
        
        if os.path.exists(stock_file_path) and option_files:
            # Plot stock data
            with open(stock_file_path, 'r') as stock_file:
                stock_data = json.load(stock_file)
                
            stock_prices = [item[0] for item in stock_data]
            stock_timestamps = [datetime.fromtimestamp(item[2] / 1000) for item in stock_data]
            
            fig, ax1 = plt.subplots(figsize=(12, 8))
            ax1.plot(stock_timestamps, stock_prices, label=f'{ticker} Stock Price', color='blue')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Stock Price', color='blue')
            ax1.tick_params(axis='y', labelcolor='blue')

            # Create a second y-axis for option prices
            ax2 = ax1.twinx()
            for option_file in option_files:
                with open(os.path.join(options_folder_path, option_file), 'r') as opt_file:
                    option_data = json.load(opt_file)
                
                option_timestamps = [datetime.fromtimestamp(item["timestamp"]/1000) for item in option_data]
                option_open_prices = [item["open_price"] for item in option_data]

                ax2.plot(option_timestamps, option_open_prices, label=f'{ticker} Option Open Price', linestyle='dashed', color='orange')

                # Extract and plot strike price
                strike_price = extract_strike_price(option_file)
                ax1.axhline(strike_price, color='red', linestyle='--', label=f'Strike Price {strike_price:.2f}')
            
            ax2.set_ylabel('Option Open Price', color='orange')
            ax2.tick_params(axis='y', labelcolor='orange')

            # Title and grid
            plt.title(f'{ticker} Stock and Option Prices Over Time')
            fig.tight_layout()
            plt.grid(True)
            plt.legend(loc='best')
            plt.show()

# Call the function to plot the stock and option prices
plot_stock_and_option_prices(tickers, stock_folder_path, options_folder_path)
