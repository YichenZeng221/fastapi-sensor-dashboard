# Data Center Commissioning Dashboard

A tiny FastAPI app to visualize commissioning power data (CSV) and highlight power alerts.

## Features
- Parse CSV, auto-detect all `(kW)` columns and aggregate to `total_kw`
- Dashboard summary (avg / max / min / alert count)
- Time-series chart (Chart.js)
- Alert logging and trend chart

## Project Structure