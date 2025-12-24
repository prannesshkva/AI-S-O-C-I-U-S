import pandas as pd
import os
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

CURR_FILE = r"C:\Powerbi project\stock_data_current.csv"
SIGNAL_FILE = r"C:\Powerbi project\stock_signals_daily.csv"
TEMP_FILE = r"C:\Powerbi project\_tmp_signal.csv"


GROQ_API_KEY = ""

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    groq_api_key=GROQ_API_KEY,
    temperature=0.2
)

def load_csv_safe(path, columns):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path)


COMPANY_MAP = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "NFLX": "Netflix Inc.",
    "NVDA": "NVIDIA Corporation",
    "AMD": "Advanced Micro Devices Inc.",
    "INTC": "Intel Corporation",
    "QCOM": "Qualcomm Incorporated",
    "ADBE": "Adobe Inc.",
    "COST": "Costco Wholesale Corporation",
    "SBUX": "Starbucks Corporation",
    "CRM": "Salesforce Inc.",
    "ORCL": "Oracle Corporation",
    "IBM": "International Business Machines Corporation",
    "JPM": "JPMorgan Chase & Co.",
    "BAC": "Bank of America Corporation",
    "WFC": "Wells Fargo & Company",
    "GS": "Goldman Sachs Group Inc.",
    "MS": "Morgan Stanley",
    "AXP": "American Express Company",
    "V": "Visa Inc.",
    "MA": "Mastercard Incorporated",
    "WMT": "Walmart Inc.",
    "HD": "Home Depot Inc.",
    "NKE": "Nike Inc.",
    "MCD": "McDonald's Corporation",
    "XOM": "Exxon Mobil Corporation",
    "CVX": "Chevron Corporation",
    "RELIANCE": "Reliance Industries Limited",
    "TCS": "Tata Consultancy Services Limited",
    "INFY": "Infosys Limited",
    "WIPRO": "Wipro Limited",
    "HCLTECH": "HCL Technologies Limited",
    "LT": "Larsen & Toubro Limited",
    "ITC": "ITC Limited",
    "HDFCBANK": "HDFC Bank Limited",
    "ICICIBANK": "ICICI Bank Limited",
    "SBIN": "State Bank of India",
    "AXISBANK": "Axis Bank Limited",
    "KOTAKBANK": "Kotak Mahindra Bank Limited",
    "BHARTIARTL": "Bharti Airtel Limited",
    "HINDUNILVR": "Hindustan Unilever Limited",
    "ASIANPAINT": "Asian Paints Limited",
    "MARUTI": "Maruti Suzuki India Limited",
    "TATAMOTORS": "Tata Motors Limited",
    "SUNPHARMA": "Sun Pharmaceutical Industries Limited",
    "DRREDDY": "Dr. Reddy's Laboratories Limited",
    "CIPLA": "Cipla Limited",
    "SPY": "SPDR S&P 500 ETF Trust",
    "QQQ": "Invesco QQQ Trust",
    "DIA": "SPDR Dow Jones Industrial Average ETF Trust",
    "IWM": "iShares Russell 2000 ETF",
    "XLK": "Technology Select Sector SPDR Fund",
    "XLF": "Financial Select Sector SPDR Fund",
    "XLE": "Energy Select Sector SPDR Fund"
}

df_price = load_csv_safe(
    CURR_FILE,
    ["symbol", "date", "open_price", "high_price", "low_price",
     "close_price", "price_change", "percent_change", "volume"]
)

if df_price.empty:
    raise RuntimeError("stock_data_current.csv is empty. Run price fetch first.")

def generate_signal(pct):
    if pct >= 1.0:
        return "BUY"
    elif pct <= -1.0:
        return "SELL"
    return "HOLD"

def llm_reasoning(symbol, pct, signal):
    prompt = f"""
You are a market analyst.

Stock: {symbol}
Daily price change (%): {pct}
Signal: {signal}

Explain the short-term market context in ONE concise sentence along with investment advice.
Avoid special characters, asterisks, or strange hyphen symbols.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )
    return response.content.strip()


today = datetime.today().strftime("%Y-%m-%d")
rows = []

for _, row in df_price.iterrows():
    symbol = row["symbol"]
    pct = round(float(row["percent_change"]), 2)
    signal = generate_signal(pct)

    rows.append({
        "symbol": symbol,
        "company_name": COMPANY_MAP.get(symbol, symbol),
        "date": today,
        "percent_change": pct,
        "trade_signal": signal,
        "llm_reasoning": llm_reasoning(symbol, pct, signal)
    })

df_new = pd.DataFrame(rows)

df_old = load_csv_safe(
    SIGNAL_FILE,
    ["symbol", "company_name", "date",
     "percent_change", "trade_signal", "llm_reasoning"]
)

if not df_old.empty:
    df_final = pd.concat([df_old, df_new], ignore_index=True)
    df_final.drop_duplicates(
        subset=["symbol", "date"],
        keep="last",
        inplace=True
    )
else:
    df_final = df_new

df_final.to_csv(TEMP_FILE, index=False)
os.replace(TEMP_FILE, SIGNAL_FILE)

print("Trade signals with company names generated successfully")
