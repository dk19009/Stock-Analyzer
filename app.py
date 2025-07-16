import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("📈 Stock Price Analyzer")

# Sidebar inputs
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch stock data
stock = yf.download(ticker, start=start_date, end=end_date)

if stock.empty:
    st.error("No data found. Check ticker symbol.")
else:

    # Plot closing prices
    st.subheader(f"{ticker} Closing Price Chart")
    st.line_chart(stock["Close"])

    # Plot 7-day, 30-day, 90-day Moving Averages
    st.subheader("Moving Averages")
    ma_periods = [7, 30, 90]
    for ma in ma_periods:
        stock[f"MA{ma}"] = stock["Close"].rolling(ma).mean()

    fig, ax = plt.subplots()
    ax.plot(stock["Close"], label="Close", linewidth=1.5)
    for ma in ma_periods:
        ax.plot(stock[f"MA{ma}"], label=f"MA {ma}")
    ax.legend()
    st.pyplot(fig)

    # Plot Daily Returns
    st.subheader("Daily Returns")
    stock["Daily Return (%)"] = stock["Close"].pct_change() * 100
    st.line_chart(stock["Daily Return (%)"])
