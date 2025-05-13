import numpy as np
import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

class MLPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = MinMaxScaler()
        self.confidence = {}
        
    def prepare_data(self, df):
        """Prepare data for ML model."""
        if df is None:
            st.error("No data available for prediction.")
            return None, None, None, None
            
        try:
            # If dataframe doesn't have the required columns, calculate them
            if 'SMA_20' not in df.columns and 'SMA20' in df.columns:
                df['SMA_20'] = df['SMA20']
                
            if 'SMA_50' not in df.columns and 'SMA50' in df.columns:
                df['SMA_50'] = df['SMA50']
            
            # Make sure we have all required columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Check if all required base columns exist
            if not all(col in df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in df.columns]
                st.error(f"Missing required columns: {', '.join(missing)}")
                return None, None, None, None
                
            # Calculate technical indicators if not present
            if 'SMA_20' not in df.columns and 'SMA20' not in df.columns:
                df['SMA_20'] = df['Close'].rolling(window=20, min_periods=5).mean()
                
            if 'SMA_50' not in df.columns and 'SMA50' not in df.columns:
                df['SMA_50'] = df['Close'].rolling(window=50, min_periods=10).mean()
                
            if 'RSI' not in df.columns:
                delta = df['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(window=14, min_periods=1).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
                rs = gain / loss.replace(0, float('inf'))
                df['RSI'] = 100 - (100 / (1 + rs))
                
            if 'MACD' not in df.columns:
                exp1 = df['Close'].ewm(span=12, adjust=False, min_periods=5).mean()
                exp2 = df['Close'].ewm(span=26, adjust=False, min_periods=10).mean()
                df['MACD'] = exp1 - exp2
            
            features = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Add technical indicators to features if they exist
            if 'SMA_20' in df.columns:
                features.append('SMA_20')
            elif 'SMA20' in df.columns:
                features.append('SMA20')
                
            if 'SMA_50' in df.columns:
                features.append('SMA_50')
            elif 'SMA50' in df.columns:
                features.append('SMA50')
                
            if 'RSI' in df.columns:
                features.append('RSI')
                
            if 'MACD' in df.columns:
                features.append('MACD')
            
            # Remove rows with NaN values
            df = df.dropna()
            
            if len(df) < 50:  # Require minimum amount of data
                st.error("Insufficient data for reliable predictions. Need at least 50 data points.")
                return None, None, None, None
            
            # Create target variable (next day's closing price)
            df['Target'] = df['Close'].shift(-1)
            df = df[:-1]  # Remove last row since it won't have a target
            
            # Prepare features and target
            X = df[features].values
            y = df['Target'].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            return X_scaled, y, df, features
        except Exception as e:
            st.error(f"Error preparing data for ML model: {str(e)}")
            return None, None, None, None
        
    def train(self, X, y):
        """Train the ML model."""
        if X is None or y is None:
            return 0.0
            
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            self.model.fit(X_train, y_train)
            score = self.model.score(X_test, y_test)
            
            # Store confidence metrics
            self.confidence = {
                'model_score': score,
                'num_features': X.shape[1],
                'training_samples': len(X_train)
            }
            
            return score
        except Exception as e:
            st.error(f"Error training ML model: {str(e)}")
            return 0.0
        
    def predict(self, data, prediction_days=7):
        """Make predictions for multiple days ahead."""
        if data is None:
            return None
            
        try:
            # Prepare data for prediction
            X, y, df, features = self.prepare_data(data)
            
            if X is None or y is None or df is None:
                return None
                
            # Train the model
            score = self.train(X, y)
            
            # Current date range
            last_date = df.index[-1]
            
            # Create future date range
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=prediction_days,
                freq='D'
            )
            
            # Get the most recent data point for prediction
            last_features = X[-1].reshape(1, -1)
            predicted_prices = []
            
            # Iteratively predict each day
            for _ in range(prediction_days):
                # Predict next day's price
                next_price = self.model.predict(last_features)[0]
                predicted_prices.append(next_price)
                
                # Update features for next prediction
                # This is a simplified approach - just shifting the closing price
                new_features = last_features.copy()
                new_features[0, features.index('Close')] = next_price
                last_features = new_features
            
            # Create prediction dataframe
            prediction_df = pd.DataFrame({
                'Predicted': predicted_prices
            }, index=future_dates)
            
            return prediction_df
            
        except Exception as e:
            st.error(f"Error making predictions: {str(e)}")
            return None
        
    def predict_single(self, X):
        """Make prediction for a single data point."""
        if X is None:
            return None
            
        try:
            return self.model.predict(X)
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            return None
        
    def get_prediction_metrics(self, y_true, y_pred):
        """Calculate prediction performance metrics."""
        if y_true is None or y_pred is None:
            return None
            
        try:
            mse = np.mean((y_true - y_pred) ** 2)
            rmse = np.sqrt(mse)
            mae = np.mean(np.abs(y_true - y_pred))
            
            return {
                'MSE': mse,
                'RMSE': rmse,
                'MAE': mae
            }
        except Exception as e:
            st.error(f"Error calculating prediction metrics: {str(e)}")
            return None
            
    def get_confidence_metrics(self, data):
        """Return confidence metrics for the prediction."""
        X, y, df, features = self.prepare_data(data)
        
        if X is None or y is None:
            return {
                "confidence": "low",
                "score": 0.0,
                "reliability": "insufficient data" 
            }
            
        score = self.train(X, y)
        
        reliability = "low"
        if score > 0.7:
            reliability = "high"
        elif score > 0.5:
            reliability = "medium"
            
        return {
            "confidence": f"{score:.2%}",
            "score": score,
            "reliability": reliability,
            "features_used": len(features),
            "data_points": len(X)
        } 