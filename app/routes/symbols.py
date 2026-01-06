from fastapi import APIRouter, HTTPException, Request
from core.symbol_manager import download_symbol, refresh_symbol
from core.state import symbols_cache, data_cache
from app.services import reload_data
import os

router = APIRouter()

@router.post("/symbols/download")
def download_new_symbol(symbol: str):
    try:
        res = download_symbol(symbol)
        symbols_cache.invalidate("symbols")
        data_cache.invalidate(f"data:{symbol.upper()}")
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/symbols/refresh")
def refresh_existing_symbol(symbol: str):
    try:
        res = refresh_symbol(symbol)
        data_cache.invalidate(f"data:{symbol.upper()}")
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/symbols/refresh-all")
def refresh_all_symbols(request: Request):
    data_dir = "data"
    symbols = [
        f.replace(".csv", "")
        for f in os.listdir(data_dir)
        if f.endswith(".csv")
    ]

    results = {}
    for sym in symbols:
        try:
            results[sym] = refresh_symbol(sym)
        except Exception as e:
            results[sym] = str(e)

    reload_data(request.app)

    # invalidate caches
    data_cache.invalidate()
    symbols_cache.invalidate()

    return {
        "status": "refreshed",
        "symbols_updated": len(symbols)
    }
