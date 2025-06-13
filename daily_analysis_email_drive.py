import os
import pandas as pd
from datetime import datetime
from stock_assistant import analyze_stock
from google.oauth2 import service_account
from googleapiclient.discovery import build
import smtplib
from email.message import EmailMessage

def load_stock_list(path="stock_list.txt"):
    with open(path, "r") as f:
        return [line.strip().upper() for line in f if line.strip()]

def merge_excel_reports(symbols, report_dir="reports", output_path="daily_stock_report.xlsx"):
    today = datetime.today().strftime("%Y-%m-%d")
    output_file = os.path.join(report_dir, f"{today}.xlsx")
    with pd.ExcelWriter(output_file) as writer:
        for symbol in symbols:
            file_path = os.path.join(report_dir, f"{symbol}_report_{today}.xlsx")
            if os.path.exists(file_path):
                df = pd.read_excel(file_path, sheet_name="Forecast")
                df.to_excel(writer, sheet_name=symbol, index=False)
    return output_file

def upload_to_gdrive(file_path, folder_id, creds_json="gdrive_service_account.json"):
    creds = service_account.Credentials.from_service_account_file(creds_json, scopes=["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [folder_id]
    }
    media = {"mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}

    with open(file_path, "rb") as f:
        media["body"] = f
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()

def send_email_report(file_path, to_email, sender_email, app_password):
    msg = EmailMessage()
    msg["Subject"] = "📊 每日股票分析報告"
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content("附件為今日股票分析報告。")

    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

if __name__ == "__main__":
    symbols = load_stock_list()
    today = datetime.today().strftime("%Y-%m-%d")
    for symbol in symbols:
        analyze_stock(symbol)

    merged_report = merge_excel_reports(symbols)

    # ⬇️ 請根據你的設定填寫以下資訊
    gdrive_folder_id = "your_google_drive_folder_id"
    upload_to_gdrive(merged_report, gdrive_folder_id)

    sender_email = "your_email@gmail.com"
    app_password = "your_gmail_app_password"
    send_email_report(merged_report, "tommycococheung@gmail.com", sender_email, app_password)