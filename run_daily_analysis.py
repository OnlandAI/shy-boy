from stock_assistant import analyze_stock
import os
from datetime import datetime

def load_stock_list(path="stock_list.txt"):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

print(f"📆 {datetime.now().strftime('%Y-%m-%d %H:%M')} 開始每日分析")

symbols = load_stock_list()
for symbol in symbols:
    try:
        analyze_stock(symbol)
    except Exception as e:
        print(f"❌ 錯誤（{symbol}）：{e}")