import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os



HIST_FILE = r"C:\Powerbi project\stock_data_historical.csv"
CURR_FILE = r"C:\Powerbi project\stock_data_current.csv"
TEMP_FILE = r"C:\Powerbi project\_tmp.csv"


symbols = [
    
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "NVDA",
    "AMD", "INTC", "QCOM", "ADBE", "ORCL", "IBM", "CSCO", "AVGO",
    "TXN", "MU", "AMAT", "LRCX","JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "V", "MA", "PYPL",
    "WMT", "COST", "HD", "LOW", "NKE", "MCD", "SBUX", "KO", "PEP",
    "XOM", "CVX", "COP", "SLB","BA", "CAT", "GE", "HON","SPY", "QQQ", "DIA", "IWM", "XLK", "XLF", "XLE",
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "WIPRO.NS","HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS",
    "ITC.NS", "LT.NS", "BHARTIARTL.NS"
]

if os.path.exists(HIST_FILE):
    df_hist = pd.read_csv(HIST_FILE, parse_dates=["date"])
    last_dates = df_hist.groupby("symbol")["date"].max().to_dict()
else:
    df_hist = pd.DataFrame()
    last_dates = {}


hist_rows = []

for symbol in symbols:
    print(f"Updating history for {symbol}")

    start_date = last_dates.get(symbol)
    if start_date is not None:
        start_date = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        start_date = "2018-01-01"

    ticker = yf.Ticker(symbol)
    hist = ticker.history(start=start_date)

    if hist.empty:
        continue

    hist.reset_index(inplace=True)

    hist["symbol"] = symbol
    hist.rename(columns={
        "Date": "date",
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Volume": "volume"
    }, inplace=True)

    hist["price_change"] = hist["close_price"] - hist["open_price"]
    hist["percent_change"] = (hist["price_change"] / hist["open_price"]) * 100
    hist["year"] = hist["date"].dt.year

    hist_rows.append(hist[[
        "symbol", "date", "year",
        "open_price", "high_price", "low_price", "close_price",
        "price_change", "percent_change", "volume"
    ]])


if hist_rows:
    df_new_hist = pd.concat(hist_rows, ignore_index=True)
    df_hist = pd.concat([df_hist, df_new_hist], ignore_index=True)
    df_hist.drop_duplicates(subset=["symbol", "date"], keep="last", inplace=True)
    df_hist.sort_values(["symbol", "date"], inplace=True)

    df_hist.to_csv(TEMP_FILE, index=False)
    os.replace(TEMP_FILE, HIST_FILE)

print("Historical data updated")


current_rows = []

for symbol in symbols:
    print(f"Fetching current snapshot for {symbol}")
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if data.empty:
        continue
    row = data.iloc[-1]
    current_rows.append({
        "symbol": symbol,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_price": round(row["Open"], 2),
        "high_price": round(row["High"], 2),
        "low_price": round(row["Low"], 2),
        "close_price": round(row["Close"], 2),
        "price_change": round(row["Close"] - row["Open"], 2),
        "percent_change": round(((row["Close"] - row["Open"]) / row["Open"]) * 100, 2),
        "volume": int(row["Volume"])
    })
df_current = pd.DataFrame(current_rows)
df_current.to_csv(TEMP_FILE, index=False)
os.replace(TEMP_FILE, CURR_FILE)

print("Current market snapshot updated")
