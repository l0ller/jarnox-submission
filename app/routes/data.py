from fastapi import APIRouter, Request, HTTPException
from app.services import get_df, get_symbol_data, get_summary, compare_symbols, top_gainers_losers
from core.predictor import predict_next_close
from core.state import data_cache

router = APIRouter()

@router.get("/data/{symbol}")
def stock_data(request: Request, symbol: str):
    cache_key = f"data:{symbol.upper()}"
    cached = data_cache.get(cache_key)
    if cached:
        return cached

    df = get_df(request.app)
    data = get_symbol_data(df, symbol)

    data_cache.set(cache_key, data)
    return data

@router.get("/summary/{symbol}")
def stock_summary(request: Request, symbol: str):
    df = get_df(request.app)
    return get_summary(df, symbol)

@router.get("/compare")
def compare(
    request: Request,
    symbol1: str,
    symbol2: str
):
    df = get_df(request.app)
    return compare_symbols(df, symbol1, symbol2)

@router.get("/movers")
def movers(request: Request):
    df = get_df(request.app)
    return top_gainers_losers(df)

@router.get("/predict/{symbol}")
def predict(symbol: str, request: Request):
    df = get_df(request.app)
    sub = df[df["Symbol"] == symbol.upper()].tail(30)

    if sub.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    pred = predict_next_close(sub["Close"].tolist())

    return {
        "symbol": symbol.upper(),
        "predicted_close": float(pred)
    }