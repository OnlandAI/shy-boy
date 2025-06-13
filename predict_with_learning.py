import pandas as pd
import os
import joblib

def correct_forecast(forecast_df, symbol, model_dir="models"):
    model_path = os.path.join(model_dir, f"{symbol}_model.pkl")
    if not os.path.exists(model_path):
        return forecast_df

    model = joblib.load(model_path)
    forecast_df = forecast_df.copy()
    forecast_df["weekday"] = pd.to_datetime(forecast_df["ds"]).dt.weekday
    forecast_df["yhat_corrected"] = model.predict(forecast_df[["yhat", "weekday"]])
    return forecast_df