import yfinance as yf
import pandas as pd
from prophet import Prophet
import os
from datetime import datetime

def analyze_stock(symbol, save_dir="reports", history_dir="data"):
    today = datetime.today().strftime('%Y-%m-%d')
    print(f"🔍 正在分析: {symbol}")

    df = yf.download(symbol, period="6mo")
    if df.empty:
        print(f"⚠️ 無法取得 {symbol} 的資料")
        return

    df.reset_index(inplace=True)
    prophet_df = df[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet(daily_seasonality=True)
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    actual = df.iloc[-1]["Close"]
    yesterday = df.iloc[-1]["Date"]
    forecast_row = forecast[forecast["ds"] == yesterday]
    forecast_val = forecast_row["yhat"].values[0] if not forecast_row.empty else None
    error = actual - forecast_val if forecast_val else None

    hist_df = pd.DataFrame([[yesterday, actual, forecast_val, error]],
                           columns=["date", "actual", "forecast", "error"])
    hist_path = os.path.join(history_dir, f"{symbol}_actual_vs_forecast.csv")
    if os.path.exists(hist_path):
        prev = pd.read_csv(hist_path)
        hist_df = pd.concat([prev, hist_df], ignore_index=True)
    hist_df.to_csv(hist_path, index=False)

    os.makedirs(save_dir, exist_ok=True)
    report_path = os.path.join(save_dir, f"{symbol}_report_{today}.xlsx")
    with pd.ExcelWriter(report_path) as writer:
        df.to_excel(writer, sheet_name="Raw Data", index=False)
        forecast.to_excel(writer, sheet_name="Forecast", index=False)
        hist_df.to_excel(writer, sheet_name="Error Log", index=False)

    print(f"✅ 完成分析：{symbol}，已儲存報告至 {report_path}")