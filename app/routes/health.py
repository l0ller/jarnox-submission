from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health")
def health(request: Request):
    if not hasattr(request.app.state, "df") or request.app.state.df is None:
        return {
            "status": "starting",
            "rows": 0,
            "symbols": 0
        }

    df = request.app.state.df
    return {
        "status": "ok",
        "rows": int(len(df)),
        "symbols": int(df["Symbol"].nunique())
    }
