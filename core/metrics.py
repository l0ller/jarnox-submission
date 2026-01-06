"""
Feature engineering utilities for stock data.
Includes technical indicators, future targets,
and external market alignment.
"""

import pandas as pd
import numpy as np

class StockMetrics:

    @staticmethod
    def add_basic_metrics(df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values("Date").copy()

        # Daily Return
        df["Daily_Return"] = (df["Close"] - df["Open"]) / df["Open"]

        # 7-Day Moving Average
        df["MA_7"] = df["Close"].rolling(window=7).mean()

        return df

    @staticmethod
    def add_52_week_levels(df: pd.DataFrame) -> dict:
        last_52w = df.tail(252)

        return {
            "52_week_high": float(last_52w["High"].max()),
            "52_week_low": float(last_52w["Low"].min()),
            "average_close": float(last_52w["Close"].mean())
        }

    @staticmethod
    def calculate_volatility(df: pd.DataFrame) -> float:
        returns = df["Close"].pct_change().dropna()
        return float(returns.std() * np.sqrt(252))
