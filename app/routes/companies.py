from fastapi import APIRouter, Request
from app.services import get_df
from core.state import symbols_cache

router = APIRouter()

@router.get("/companies")
def list_companies(request: Request):
    cached = symbols_cache.get("symbols")
    if cached:
        return cached

    df = get_df(request.app)
    symbols = sorted(df["Symbol"].unique().tolist())

    symbols_cache.set("symbols", symbols)
    return symbols
