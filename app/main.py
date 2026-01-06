from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import routers individually
from app.routes.health import router as health_router
from app.routes.companies import router as companies_router
from app.routes.data import router as data_router
from app.routes.symbols import router as symbols_router

from contextlib import asynccontextmanager
from core.data_loader import StockDataLoader
from core.metrics import StockMetrics

DATA_DIR = "data"

@asynccontextmanager
async def lifespan(app: FastAPI):
    df = StockDataLoader.load_ohlcv(DATA_DIR)
    df = StockMetrics.add_basic_metrics(df)
    df.sort_values(["Symbol", "Date"], inplace=True)
    app.state.df = df

    print(f"✅ Loaded {len(df)} rows across {df['Symbol'].nunique()} symbols")
    yield
    app.state.df = None

app = FastAPI(
    title="Stock Data Intelligence API",
    description="Mini financial data platform for Jarnox internship",
    version="1.0.0",
    lifespan=lifespan,
)

# Include all routers
app.include_router(health_router)
app.include_router(companies_router)
app.include_router(data_router)
app.include_router(symbols_router)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")
