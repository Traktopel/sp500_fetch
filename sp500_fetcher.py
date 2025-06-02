import pandas as pd
import yfinance as yf
import os

def get_sp500_tickers():
    """Get the list of S&P 500 company tickers"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url, header=0)[0]
    tickers = table['Symbol'].tolist()
    return tickers

def download_historical_data(ticker, start_date="2000-01-01", end_date=None):
    """Download historical OHLCV data for a given ticker"""
    if end_date is None:
        end_date = pd.Timestamp.now().strftime('%Y-%m-%d')

    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def main():
    # Create output directory if it doesn't exist
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # Get S&P 500 tickers
    tickers = get_sp500_tickers()

    # Download data for each ticker
    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        data = download_historical_data(ticker)
        filename = os.path.join(output_dir, f"{ticker}.csv")
        data.to_csv(filename)
        print(f"Saved data to {filename}")

if __name__ == "__main__":
    main()