import pandas as pd
import numpy as np

class StockSummary:

    @staticmethod
    def summary_stats(df: pd.DataFrame) -> dict:
        """
        Returns 52-week high, low, average close, and volatility.
        """
        df = df.sort_values("Date").copy()
        last_52w = df.tail(252)

        returns = last_52w["Close"].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)

        return {
            "52_week_high": float(last_52w["High"].max()),
            "52_week_low": float(last_52w["Low"].min()),
            "average_close": float(last_52w["Close"].mean()),
            "volatility": float(volatility)
        }

    @staticmethod
    def recent_performance(df: pd.DataFrame, days=30) -> dict:
        """
        Returns last N-day return and average volume.
        """
        recent = df.sort_values("Date").tail(days)

        total_return = (
            recent["Close"].iloc[-1] / recent["Close"].iloc[0] - 1
        )

        return {
            "period_days": days,
            "return_pct": float(total_return * 100),
            "avg_volume": float(recent["Volume"].mean())
        }
