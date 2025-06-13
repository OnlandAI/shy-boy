import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import joblib

def train_model(symbol, history_dir="data", model_dir="models"):
    path = os.path.join(history_dir, f"{symbol}_actual_vs_forecast.csv")
    if not os.path.exists(path):
        print(f"❌ 找不到歷史記錄：{path}")
        return

    df = pd.read_csv(path)
    df.dropna(inplace=True)

    # 特徵：weekday, forecast value
    df["weekday"] = pd.to_datetime(df["date"]).dt.weekday
    X = df[["forecast", "weekday"]]
    y = df["actual"]

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, f"{symbol}_model.pkl"))
    print(f"✅ 模型訓練完成：{symbol}")