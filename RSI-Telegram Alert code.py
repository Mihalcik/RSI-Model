#This model 
import yfinance as yf
import pandas as pd
import ta
import time
import schedule
import requests

# Telegram Bot Config
BOT_TOKEN = '8157123569:AAFp5an8o5Ttek05fufXtpAYF-NXGU7Sy-0'
CHAT_ID = '5630340660'

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

# Stock list
TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "ORCL", "AMD", "IBM", "CSCO", "QCOM", "TXN", "INTC", "SAP", "ADBE", "CRM", "INTU", "NOW", "PYPL", "SHOP", "SNOW", "UBER", "TWLO", "DOCU", "ZM", "SPOT", "PANW", "CRWD", "NET", "OKTA", "ZS", "MDB", "DDOG", "FSLY", "BILL", "ASAN", "TEAM", "MNDY", "ESTC", "HUBS", "WDAY", "ADSK", "ANSS", "CDNS", "SNPS", "AKAM", "VRSN"]

# Check RSI
def check_rsi(stock):
    try:
        data = yf.download(stock, period="1mo", interval="1h", progress=False)
        if data.empty:
            return None
        close_series = data['Close'].squeeze()  # Make sure it's 1h
        data['RSI'] = ta.momentum.RSIIndicator(close=close_series, window=14).rsi()
        latest_rsi = data['RSI'].iloc[-1]
        if latest_rsi < 30:
            return f" {stock} is OVERSOLD. RSI: {latest_rsi:.2f}"
        elif latest_rsi > 70:
            return f" {stock} is OVERBOUGHT. RSI: {latest_rsi:.2f}"

    except Exception as e:
        return f"Error with {stock}: {e}"

# Screen function
def screen_stocks():
    print("\n Scanning stocks...\n")
    for ticker in TICKERS:
        signal = check_rsi(ticker)
        if signal:
            print(signal)
            send_telegram(signal)

# Scheduler
schedule.every(15).minutes.do(screen_stocks)

print("RSI Screener running... Sending Telegram alerts...")
screen_stocks()

while True:
    schedule.run_pending()
    time.sleep(1)



