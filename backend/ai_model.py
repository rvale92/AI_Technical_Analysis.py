from prophet import Prophet
import pandas as pd
from typing import Tuple, Dict

def prepare_data_for_prophet(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare stock data for Prophet model"""
    return pd.DataFrame({
        'ds': data.index,
        'y': data['Close']
    })

def train_prophet_model(data: pd.DataFrame) -> Prophet:
    """Train Prophet model"""
    model = Prophet()
    model.fit(data)
    return model

def make_predictions(model: Prophet, periods: int = 30) -> Tuple[pd.DataFrame, Dict]:
    """Make predictions using Prophet model"""
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    # Analyze the forecast
    analysis = analyze_forecast(forecast)
    
    return forecast, analysis

def analyze_forecast(forecast: pd.DataFrame) -> Dict:
    """Analyze the forecast results"""
    trend_slope = (forecast['yhat'].iloc[-1] - forecast['yhat'].iloc[0]) / len(forecast)
    uncertainty = forecast['yhat_upper'].mean() - forecast['yhat_lower'].mean()
    
    analysis = {
        'trend': {
            'slope': trend_slope,
            'description': 'strong upward' if trend_slope > 0.1 else 'strong downward' if trend_slope < -0.1 else 'stable'
        },
        'seasonality': {
            'weekly': bool('weekly' in forecast.columns and forecast['weekly'].mean() > 0.2)
        },
        'uncertainty': {
            'value': uncertainty,
            'level': 'high' if uncertainty > 0.5 else 'low' if uncertainty < 0.2 else 'moderate'
        }
    }
    
    return analysis 