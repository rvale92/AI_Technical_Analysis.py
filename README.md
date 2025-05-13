# AI-Powered Technical Stock Analysis Dashboard

A Streamlit application for comprehensive technical analysis of stocks and cryptocurrencies with AI-powered price predictions, trading strategies, and real-time market insights.

## Live Demo

Check out the live application at: [https://rvale92.github.io/AI_Technical_Analysis.py/](https://rvale92.github.io/AI_Technical_Analysis.py/)

## Features

- **Real-time Market Data**: Fetch and analyze stock and crypto data from Yahoo Finance
- **AI-Powered Predictions**: Machine learning models to predict future price movements
- **Technical Indicators**: SMA, EMA, RSI, MACD, Bollinger Bands, Volume profiling
- **Trading Strategies**: Backtest various trading strategies with performance metrics
- **Interactive Visualization**: Responsive Plotly charts with dark theme UI
- **Multi-page Interface**: Organized navigation with dedicated views for different analysis tasks

## Project Structure

```
AI_Technical_Analysis/
├── Home.py                    # Main app entry point
├── backend/                   # Backend functionality
│   ├── data_loader.py         # Market data fetching with robust error handling
│   ├── ml_predictor.py        # Machine learning prediction engine
│   ├── indicators.py          # Technical indicators calculation
│   ├── utils.py               # Utility functions
│   └── ai_model.py            # AI model implementation
├── pages/                     # Streamlit multi-page components
│   ├── 1_🤖_ML_Predictions.py    # ML-based market predictions
│   ├── 2_📈_Trading_Strategies.py # Trading strategy backtesting
│   └── 3_📊_Market_Metrics.py     # Technical analysis metrics
├── frontend/                  # UI components
│   ├── components.py          # Reusable UI elements
│   └── layout.py              # Layout configuration
├── .streamlit/                # Streamlit configuration
├── static/                    # Static assets
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rvale92/AI_Technical_Analysis.py.git
cd AI_Technical_Analysis.py
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run Home.py
```

The application will be available at http://localhost:8501

## Key Features

### ML Predictions
- **Price Forecasting**: ML-powered price predictions with confidence metrics
- **Model Insights**: Understand the factors influencing price predictions
- **Confidence Metrics**: Evaluate prediction reliability with statistical metrics

### Trading Strategies
- **Strategy Backtesting**: Test trading strategies against historical data
- **Performance Metrics**: Analyze returns, drawdown, Sharpe ratio, and win rate
- **Strategy Comparison**: Compare multiple strategies side by side

### Market Metrics
- **Technical Indicators**: Comprehensive suite of technical analysis tools
- **Volume Analysis**: Understand trading volume patterns and distribution
- **Support/Resistance**: Identify key price levels

## Technologies Used

- **Streamlit**: Interactive web application framework
- **Pandas/NumPy**: Data manipulation and analysis
- **yfinance**: Yahoo Finance market data API
- **Scikit-learn**: Machine learning algorithms
- **Plotly**: Interactive charts and visualizations

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rvale92/AI_Technical_Analysis.py/issues).

## License

This project is [MIT](LICENSE) licensed.

## Acknowledgements

- [Yahoo Finance](https://finance.yahoo.com/) for market data
- [Streamlit](https://streamlit.io/) for the web application framework
- [Plotly](https://plotly.com/) for interactive visualizations 