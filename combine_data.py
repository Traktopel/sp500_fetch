import pandas as pd
import os
import requests
from datetime import datetime

def get_balance_sheet_data(ticker, api_key):
    """Get balance sheet data from Financial Modeling Prep API"""
    url = f"https://api.fmpcloud.com/api/v3/balance_sheet/{ticker}?period=quarter&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching data for {ticker}: {response.status_code}")
            return None

        data = response.json()
        if 'error' in data:
            print(f"Error fetching data for {ticker}: {data['error']}")
            return None

        return data
    except requests.exceptions.RequestException as e:
        print(f"Connection error for {ticker}: {str(e)}")
        return None

def combine_data(ticker, balance_sheet_data, ohclv_data):
    """Combine balance sheet and OHLCV data"""
    # Extract relevant fields from balance sheet data
    if balance_sheet_data is not None and 'balanceSheet' in balance_sheet_data:
        bs_data = balance_sheet_data['balanceSheet']
        if bs_data:
            total_assets = bs_data[0]['totalAssets']
            total_liabilities = bs_data[0]['totalLiabilities']
            shareholders_equity = bs_data[0]['shareholdersEquity']

            # Add balance sheet data to OHLCV data
            ohclv_data['Total Assets'] = total_assets
            ohclv_data['Total Liabilities'] = total_liabilities
            ohclv_data['Shareholders Equity'] = shareholders_equity

    return ohclv_data

def main():
    # Get API key from environment variable or hardcode it
    api_key = os.getenv('FMP_API_KEY', 'demo')  # Replace 'demo' with your actual API key

    # Get list of tickers from OHLCV data directory
    data_dir = "data"
    tickers = [f.replace('.csv', '') for f in os.listdir(data_dir) if f.endswith('.csv')]

    for ticker in tickers:
        print(f"Processing {ticker}...")

        # Load OHLCV data
        ohclv_file = os.path.join(data_dir, f"{ticker}.csv")
        ohclv_data = pd.read_csv(ohclv_file)

        # Get balance sheet data
        balance_sheet_data = get_balance_sheet_data(ticker, api_key)

        # Combine data
        combined_data = combine_data(ticker, balance_sheet_data, ohclv_data)

        # Save combined data
        output_file = os.path.join(data_dir, f"{ticker}_combined.csv")
        combined_data.to_csv(output_file)
        print(f"Saved combined data to {output_file}")

if __name__ == "__main__":
    main()