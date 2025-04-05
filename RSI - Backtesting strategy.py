#What it does
#1. Downloads historical stock price data using Yahoo Finance (`yfinance`).
#2. Calculates the RSI using the `ta` library.
#3. Simulates trades based on RSI thresholds:
 #  - Buys when RSI drops below a defined level (e.g., 30).
  # - Sells when RSI rises above a defined level (e.g., 70).
#4. Tracks trades and computes the final portfolio value for each ticker.
#5. Prints trade logs and a summary of results for all tickers.

#Limitations:
#Does not include trading fees, slippage, or spread.
#Assumes full position is bought/sold instantly at the current price.
#Backtests only one strategy (RSI) with fixed thresholds.
#Uses simplified cash/position logic (no portfolio management or diversification).

#Possible Improvements:
#Add support for stop-loss and take-profit levels.
#Incorporate multiple indicators or strategies.
#Simulate partial position sizing or leverage.
#Include performance metrics (e.g., Sharpe ratio, max drawdown).
#Visualize results with plots.

import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator

def backtest_rsi_strategy(
    ticker: str,
    period: str = "1mo",
    interval: str = "1h",
    rsi_period: int = 7,         # Faster RSI
    rsi_buy: float = 30,         # More frequent buys
    rsi_sell: float = 70,        # More frequent sells
    data_type: str = "close",
    initial_cash: float = 100.0
):
    data = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    if data_type.lower() not in ["close", "open", "high", "low"]:
        raise ValueError("Invalid data_type. Use: 'close', 'open', 'high', or 'low'")

    price_series = data[data_type.capitalize()].dropna()
    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.squeeze()

    rsi = RSIIndicator(close=price_series, window=rsi_period).rsi()

    cash = initial_cash
    position = 0
    trade_log = []

    for date in price_series.index:
        current_price = price_series.loc[date]
        current_rsi = rsi.loc[date]

        if current_rsi < rsi_buy and cash > 0:
            position = cash / current_price
            trade_log.append((date, "BUY", current_price, position))
            cash = 0

        elif current_rsi > rsi_sell and position > 0:
            cash = position * current_price
            trade_log.append((date, "SELL", current_price, position))
            position = 0

    final_value = cash + (position * price_series.iloc[-1])
    trade_df = pd.DataFrame(trade_log, columns=["Date", "Action", "Price", "Shares"])

    print(f"=== Trade Log for {ticker} ===")
    print(trade_df)
    print("\n=== Summary ===")
    print(f"Final Value: €{final_value:.2f}")
    print(f"Profit: €{final_value - initial_cash:.2f}\n")

    return trade_df, final_value

if __name__ == "__main__":
    tickers = [
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "ORCL", "AMD", "IBM", "CSCO", "QCOM", "TXN", "INTC", "SAP", "ADBE", "CRM", "INTU", "NOW", "PYPL", "SHOP", "SNOW", "UBER", "TWLO", "DOCU", "ZM", "SPOT", "PANW", "CRWD", "NET", "OKTA", "ZS", "MDB", "DDOG", "FSLY", "BILL", "ASAN", "TEAM", "MNDY", "ESTC", "HUBS", "WDAY", "ADSK", "ANSS", "CDNS", "SNPS", "AKAM", "VRSN"
    ]
    results = {}

    for ticker in tickers:
        print(f"Running RSI strategy for {ticker}...\n")
        trade_df, final_value = backtest_rsi_strategy(
            ticker,
            period="1mo",
            interval="1h",
            rsi_period=7,
            rsi_buy=30,
            rsi_sell=70,
            data_type="close",
            initial_cash=100.0
        )
        results[ticker] = final_value

    print("=== Final Portfolio Values ===")
    for ticker, value in results.items():
        print(f"{ticker}: Final Value = €{value:.2f}")

