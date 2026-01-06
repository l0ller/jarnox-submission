import numpy as np
import pandas as pd
from fastapi import HTTPException
from core.cache import get_cache, set_cache

def get_symbol_data_cached(df, symbol: str):
    cache_key = f"symbol:{symbol}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    sub = df[df["Symbol"] == symbol.upper()].sort_values("Date")

    if sub.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    sub = sub.replace([np.inf, -np.inf], np.nan)
    sub = sub.astype(object).where(pd.notna(sub), None)

    data = sub.tail(365).to_dict(orient="records")
    set_cache(cache_key, data)

    return data
