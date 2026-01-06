import pandas as pd
from fastapi import HTTPException
import numpy as np

def get_df(app):
    return app.state.df

def get_symbol_data(df, symbol: str):
    sub = df[df["Symbol"] == symbol.upper()].sort_values("Date")

    if sub.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    # 🔹 Replace invalid values
    sub = sub.replace([np.inf, -np.inf], np.nan)

    # 🔹 Convert NaN → None (JSON-safe)
    sub = sub.astype(object).where(pd.notna(sub), None)

    return sub.tail(365).to_dict(orient="records")



def get_summary(df: pd.DataFrame, symbol: str):
    sub = df[df["Symbol"] == symbol.upper()]
    if sub.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    return {
        "symbol": symbol.upper(),
        "52w_high": float(sub["Close"].max()),
        "52w_low": float(sub["Close"].min()),
        "avg_close": float(sub["Close"].mean())
    }


def compare_symbols(df, s1, s2):
    a = df[df["Symbol"] == s1.upper()]
    b = df[df["Symbol"] == s2.upper()]
    if a.empty or b.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    return {
        s1.upper(): float((a["Close"].iloc[-1] / a["Close"].iloc[0] - 1) * 100),
        s2.upper(): float((b["Close"].iloc[-1] / b["Close"].iloc[0] - 1) * 100)
    }


def top_gainers_losers(df: pd.DataFrame, n=3):
    latest = df.sort_values("Date").groupby("Symbol").tail(2)

    latest["pct_change"] = (
        latest.groupby("Symbol")["Close"].pct_change() * 100
    )

    ranked = latest.dropna().sort_values("pct_change", ascending=False)

    return {
        "top_gainers": ranked.head(n)[["Symbol", "pct_change"]].to_dict("records"),
        "top_losers": ranked.tail(n)[["Symbol", "pct_change"]].to_dict("records")
    }

def reload_data(app):
    from core.data_loader import StockDataLoader
    from core.metrics import StockMetrics

    df = StockDataLoader.load_ohlcv("data")
    df = StockMetrics.add_basic_metrics(df)
    df.sort_values(["Symbol", "Date"], inplace=True)

    app.state.df = df
