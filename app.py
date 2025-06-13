import streamlit as st
from stock_assistant import analyze_stock
import datetime

st.set_page_config(page_title="📈 股票分析助手", layout="centered")
st.title("📈 即時股票分析助手（NAS Streamlit）")

symbol = st.text_input("請輸入股票代碼（例如：TSLA, AAPL, 0700.HK）", "TSLA")

if st.button("🔍 開始分析"):
    with st.spinner(f"正在分析 {symbol}..."):
        try:
            analyze_stock(symbol)
            st.success(f"{symbol} 分析完成！報告已儲存。")

            today = datetime.datetime.now().strftime("%Y-%m-%d")
            report_path = f"reports/{symbol}_report_{today}.xlsx"
            with open(report_path, "rb") as f:
                st.download_button("📥 下載報告", f, file_name=report_path, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")