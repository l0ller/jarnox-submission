import yfinance as yf
import os

SYMBOLS = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

for sym in SYMBOLS:
    df = yf.download(sym, start="2020-01-01")
    df.reset_index(inplace=True)
    df["Symbol"] = sym.replace(".NS", "")
    df.to_csv(f"{DATA_DIR}/{sym.replace('.NS','')}.csv", index=False)
