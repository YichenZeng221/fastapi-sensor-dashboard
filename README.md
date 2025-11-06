# FastAPI Sensor Dashboard

A lightweight FastAPI app to visualize commissioning power data (CSV) and highlight power alerts.

## Features

- Parse CSV files, auto-detect all `kw` columns and aggregate into `total_kw`
- Dashboard summary (avg / max / min / alert count)
- Time-series chart (Chart.js)
- Alert logging and trend chart

## Quickstart

```bash
# 1) Create and activate a virtual environment (skip if you already have one)
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the FastAPI app
uvicorn app:app --reload

# Then open in your browser:
# http://127.0.0.1:8000
# API docs: http://127.0.0.1:8000/docs



## **Project Structure**
.
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── data/
    ├── sensor_data.csv
    └── alerts_log.csv

    
# FastAPI Sensor Dashboard
A lightweight FastAPI app to visualize commissioning power data (CSV) and highlight power alerts.

<img width="1209" height="1477" alt="Screenshot 2025-11-05 at 7 53 04 PM" src="https://github.com/user-attachments/assets/92eb1037-9a9b-4f27-90ef-1615d4f50962" />
<img width="2560" height="1440" alt="Screenshot 2025-11-05 at 7 53 37 PM" src="https://github.com/user-attachments/assets/8eadedc5-39bd-4115-8b3c-7f9205b47e0a" />
