# Experimental ML Technical Analysis Dashboard

A Python + Streamlit learning project for exploring market-data processing, technical indicators, forecasting, and machine-learning workflows.

> **Portfolio note:** This is an experimental/educational project. It is not a production trading system and its forecasts should not be used as financial advice.

## What this project demonstrates

- Loading and cleaning market data
- Calculating technical indicators such as RSI, MACD, and moving averages
- Preparing feature sets for machine-learning models
- Training a `RandomForestRegressor`
- Experimenting with Prophet-based time-series forecasting
- Building multi-page data applications with Streamlit
- Presenting charts and model output interactively

## Tech stack

- Python
- Streamlit
- Pandas / NumPy
- scikit-learn
- Prophet
- yfinance
- Plotly

## Project structure

```text
AI_Technical_Analysis.py/
├── Home.py
├── backend/
│   ├── ai_model.py
│   ├── data_loader.py
│   ├── indicators.py
│   ├── ml_predictor.py
│   └── utils.py
├── pages/
├── frontend/
├── requirements.txt
└── README.md
```

## Current modeling approach

The repository currently includes two forecasting experiments:

### Random Forest
`backend/ml_predictor.py` builds features from OHLCV market data and technical indicators, then trains a `RandomForestRegressor` to estimate the next closing price.

### Prophet
`backend/ai_model.py` prepares closing-price data for Prophet and generates a forecast with trend and uncertainty output.

## Known limitations

This project intentionally remains a learning environment. Current limitations include:

- The Random Forest workflow uses a conventional random train/test split rather than a time-series walk-forward evaluation.
- Multi-day prediction uses a simplified iterative approach.
- Market regime changes, transaction costs, slippage, and execution constraints are not modeled.
- Model scores are learning metrics, not guarantees of future performance.

Documenting these limitations is part of the project: the goal is to understand the full ML workflow, not to overstate model accuracy.

## Run locally

```bash
git clone https://github.com/rvale92/AI_Technical_Analysis.py.git
cd AI_Technical_Analysis.py

python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
streamlit run Home.py
```

## Why I built it

I built this project to strengthen my Python, data-processing, troubleshooting, and machine-learning fundamentals while experimenting with an end-to-end application rather than isolated scripts.
