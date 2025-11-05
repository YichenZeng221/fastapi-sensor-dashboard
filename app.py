from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from pathlib import Path
import re

# FastAPI Initialization
app = FastAPI(title="Data Center Power Dashboard")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sensor_data.csv"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
ALERT_LOG = LOG_DIR / "alerts_log.csv"

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Load Sensor Data
def load_data():
    """Load and process sensor data, sum all (kW) columns."""
    df = pd.read_csv(DATA_FILE)
    df.rename(columns={df.columns[0]: "timestamp"}, inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    kw_cols = [c for c in df.columns if re.search(r"\(kW\)", c)]
    df["total_kw"] = df[kw_cols].sum(axis=1)
    return df[["timestamp", "total_kw"]]


# Home Page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Summary Stats
@app.get("/summary")
def summary():
    df = load_data()
    avg = df["total_kw"].mean()
    max_v = df["total_kw"].max()
    min_v = df["total_kw"].min()
    alerts = df[df["total_kw"] > 100]

    if not alerts.empty:
        alerts["log_time"] = pd.Timestamp.now()
        alerts.to_csv(ALERT_LOG, mode="a", header=not ALERT_LOG.exists(), index=False)

    return {
        "rows": len(df),
        "average_kw": round(avg, 2),
        "max_kw": round(max_v, 2),
        "min_kw": round(min_v, 2),
        "alerts": int(len(alerts)),
    }


# Power Series (last 200)
@app.get("/series")
def series():
    df = load_data().tail(200)
    return {
        "timestamp": df["timestamp"].astype(str).tolist(),
        "total_kw": df["total_kw"].tolist(),
    }


# Show All Alert Points (No Grouping)


@app.get("/alerts/trend")
def alert_trend():
    """
    Return all alert points computed directly from sensor_data.csv
    so the chart always has data without relying on the alerts_log.csv.
    """
    df = load_data()
    alerts = df[df["total_kw"] > 100].copy()
    if alerts.empty:
        return {"dates": [], "counts": []}

    # 排序并只取最近 500 个点避免前端太重（可按需调小/调大）
    alerts = alerts.sort_values("timestamp").tail(500)

    return {
        "dates": alerts["timestamp"].astype(str).tolist(),
        "counts": [1] * len(alerts),
    }


"""
Run with:
  uvicorn app:app --reload

Visit:
  http://127.0.0.1:8000/
"""
