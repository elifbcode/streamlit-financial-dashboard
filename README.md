📈 Streamlit Financial Analysis Dashboard

This project is a sophisticated, interactive web application built with Python to provide technical analysis and visualization of real-time stock market data using Yahoo Finance. It serves as a strong portfolio piece demonstrating skills in data processing, modern visualization, and web application development with Streamlit.

✨ Features

Dynamic Data Fetching: Fetches up-to-date historical price data for any valid stock ticker (e.g., MSFT, AAPL, TSLA) using the yfinance library.

Technical Indicators: Calculates and plots key technical indicators directly on the price chart:

Simple Moving Averages (SMA): 20-day and 50-day SMA lines.

Relative Strength Index (RSI): A separate chart visualizing the 14-day RSI (with Overbought/Oversold levels).

Interactive Visualization: Uses the Plotly library to render responsive and zoomable Candlestick and Bar charts (Volume).

Key Performance Indicators (KPIs): Displays essential metrics (Latest Close Price, Daily Change, Average Volume) and fundamental company information (Industry, Market Cap).

Modular Code Structure: Clean separation of UI logic (app.py) from data processing and plotting functions (fin_funcs.py).

Dark Mode: Configured for a modern Dark Mode aesthetic (.streamlit/config.toml).

🛠️ Technologies & Libraries

Python 3.x

Streamlit: For rapid web application development.

Pandas: For data manipulation and time-series management.

yfinance: For fetching live stock market data.

Plotly: For interactive and dynamic charting.

pandas-ta: For calculating technical indicators (SMA, RSI).

🚀 How to Run Locally

Clone the Repository:

git clone [https://github.com/elifbcode/streamlit-financial-dashboard.git](https://github.com/elifbcode/streamlit-financial-dashboard.git)
cd streamlit-financial-dashboard


Install Dependencies:

pip install -r requirements.txt


Run the Application:

streamlit run app.py


Your dashboard will automatically open in your web browser.
