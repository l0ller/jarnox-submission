📈 Stock Data Intelligence Platform

A mini full-stack financial data platform built with FastAPI + Pandas + Chart.js, featuring historical stock analysis, comparisons, and next-day price prediction — fully containerized using Docker.

🚀 Features
📊 Stock Analytics

View historical OHLCV stock data

Interactive line charts with 30-day and 90-day filters

Multi-stock comparison on the same timeline

🔮 Price Prediction

Predicts next day closing price using recent historical data

Prediction displayed directly on the chart as a dashed line

Clean separation between historical data and forecast

🧠 Data Intelligence

Automatic metric computation (returns, moving averages, etc.)

Handles missing, NaN, and infinite values safely for JSON APIs

Efficient Pandas slicing for large datasets

🗂️ Symbol Management

Add new stock symbols dynamically

Refresh individual or all symbols

Reloads data without restarting the server

⚡ Performance & Reliability

In-memory caching of processed data

Avoids repeated heavy computations on every request

Fast API responses even with large datasets

🐳 Dockerized Deployment

Single-command Docker build & run

No local Python or dependency conflicts

Ready for cloud or local deployment

🏗️ Architecture Overview
jarnox-submission/
│
├── app/
│   ├── main.py            # FastAPI app & lifecycle
│   ├── routes.py          # API endpoints
│   └── services.py        # Data access & caching logic
│
├── core/
│   ├── data_loader.py     # CSV → DataFrame loader
│   ├── metrics.py         # Feature engineering
│   ├── predictor.py       # Next-day close prediction
│   └── symbol_manager.py  # Download / refresh symbols
│
├── data/                  # CSV stock data
├── frontend/              # HTML + JS dashboard
├── scripts/               # Utility scripts
├── Dockerfile
├── requirements.txt
└── README.md

🔁 Data Flow

Startup

CSV files are loaded from /data

Metrics are computed once

DataFrame cached in app.state.df

API Request

Routes fetch cached DataFrame

Filter & transform data safely

Return JSON-serializable responses

Frontend

Fetches data via REST APIs

Chart.js renders interactive charts

Prediction line appended dynamically

🌐 API Endpoints
Health
GET /health


Returns app status, total rows, and symbol count.

Companies
GET /companies


Returns list of available stock symbols.

Stock Data
GET /data/{symbol}


Returns last 365 days of historical data for a symbol.

Stock Summary
GET /summary/{symbol}


Returns computed metrics and insights.

Compare Stocks
GET /compare?symbol1=AAPL&symbol2=MSFT


Returns aligned comparison metrics.

Top Movers
GET /movers


Top gainers and losers based on latest returns.

Prediction
GET /predict/{symbol}


Predicts next trading day closing price.

Symbol Management
POST /symbols/download?symbol=TSLA
POST /symbols/refresh?symbol=TSLA
POST /symbols/refresh-all

📊 Frontend Dashboard

Sidebar for symbol selection & comparison

Interactive chart with hover tooltips

30 / 90 day filters

Prediction shown as dashed extension

Compare mode overrides single-stock view cleanly

🧠 Prediction Logic

Uses last 30 closing prices

Lightweight statistical approach (fast & explainable)

Designed to be easily replaceable with ML models later

Prediction intentionally isolated from historical data

⚡ Caching Strategy

Entire processed DataFrame stored in memory

Avoids repeated disk I/O and recomputation

Reloads cache only when symbols are refreshed

Simple, reliable, and ideal for read-heavy workloads

🐳 Docker Setup
Build Image
docker build -t stock-dashboard .

Run Container
docker run -p 8000:8000 stock-dashboard

Access

API: http://localhost:8000

UI: http://localhost:8000/ui

🛠️ Tech Stack

Backend: FastAPI, Pandas, NumPy

Frontend: HTML, CSS, Vanilla JS, Chart.js

Deployment: Docker

Data: CSV-based OHLCV data

🧪 Design Decisions & Trade-offs

CSV instead of DB: Faster iteration, simpler deployment

In-memory cache: Optimal for analytics-heavy reads

Statistical prediction: Lightweight, interpretable

Vanilla JS frontend: No framework overhead

🔮 Future Improvements

ML-based forecasting models

Confidence intervals for predictions

WebSocket live price updates

Database backend (PostgreSQL / DuckDB)

User-specific dashboards

👨‍💻 Author

Built by Uday Joshi
As part of a technical submission for the Jarnox Internship.