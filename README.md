# AI-Powered Technical Stock Analysis Dashboard

A Streamlit-based dashboard for technical analysis of stocks with AI-powered predictions using Prophet.

## Features

- Real-time stock data fetching using yfinance
- Technical indicators (SMA, EMA, Bollinger Bands, VWAP, RSI, MACD)
- Interactive candlestick charts with Plotly
- AI-powered price predictions using Facebook Prophet
- Clean, modular code structure

## Project Structure

```
AI_Technical_Analysis/
├── backend/
│   ├── data_loader.py         # Stock data fetching
│   ├── indicators.py          # Technical indicators
│   ├── ai_model.py            # Prophet model logic
│   └── utils.py               # Helper functions
├── frontend/
│   ├── app.py                 # Main Streamlit app
│   ├── components.py          # UI components
│   └── layout.py              # Layout helpers
├── assets/                    # Static files
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI_Technical_Analysis.git
cd AI_Technical_Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run frontend/app.py
```

The app will be available at http://localhost:8501

## Dependencies

- streamlit>=1.44.0
- yfinance==0.2.40
- pandas>=2.0.0
- plotly>=6.0.0
- prophet>=1.1.0
- numpy>=1.20.0
- python-dateutil>=2.8.2 