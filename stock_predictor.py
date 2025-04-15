import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import os

def get_stock_trend(ticker):
    end = datetime.now()
    start = end - timedelta(days=30)

    stock = yf.download(ticker, start=start, end=end)

    if stock.empty:
        return None, None, "Invalid Ticker Symbol or No Data", None

    # Calculate average return
    stock['Change'] = stock['Close'].pct_change()
    avg_return = stock['Change'].mean()
    trend = "Upward 📈" if avg_return > 0 else "Downward 📉"
    suggestion = "Invest ✅" if avg_return > 0 else "Don't Invest ❌"

    # Generate graph
    graph_path = f"static/{ticker}_plot.png"
    plt.figure(figsize=(10, 4))
    plt.plot(stock.index, stock['Close'], label='Close Price', color='blue')
    plt.title(f"{ticker} - Last 30 Days Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

    return round(avg_return * 100, 2), trend, suggestion, graph_path
