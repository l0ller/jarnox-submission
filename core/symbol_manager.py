import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")

def download_symbol(symbol: str) -> dict:
    symbol = symbol.upper()
    file_path = DATA_DIR / f"{symbol}.csv"

    ticker = yf.Ticker(symbol)
    df = ticker.history(period="max")

    if df.empty:
        raise ValueError("Invalid or unavailable symbol")

    df.reset_index(inplace=True)
    df["Symbol"] = symbol
    df.rename(columns=str.title, inplace=True)

    df.to_csv(file_path, index=False)

    return {
        "symbol": symbol,
        "rows": len(df),
        "last_date": str(df["Date"].iloc[-1])
    }


def refresh_symbol(symbol: str) -> dict:
    symbol = symbol.upper()
    file_path = DATA_DIR / f"{symbol}.csv"

    if not file_path.exists():
        raise ValueError("Symbol not found locally")

    old_df = pd.read_csv(file_path)
    last_date = pd.to_datetime(old_df["Date"]).max()

    ticker = yf.Ticker(symbol)
    new_df = ticker.history(start=last_date)

    if new_df.empty:
        return {"symbol": symbol, "status": "already up to date"}

    new_df.reset_index(inplace=True)
    new_df["Symbol"] = symbol
    new_df.rename(columns=str.title, inplace=True)

    merged = pd.concat([old_df, new_df]).drop_duplicates(subset=["Date"])
    merged.to_csv(file_path, index=False)

    return {
        "symbol": symbol,
        "new_rows": len(new_df),
        "total_rows": len(merged)
    }
