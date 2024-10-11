# Install required libraries
# pip install streamlit prophet yfinance plotly pandas

import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import time

# Set the start date for historical data and today's date
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast and Suggestion App')

# List of companies' stocks (removed Netflix, Facebook, Shopify, and Amazon; added Visa)
stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', 'TSLA', 'NVDA', 'PFE', 'MRNA', 'V')

# Select box for the user to pick a stock
selected_stock = st.selectbox('Select dataset for prediction', stocks)

# Slider to pick the number of years for prediction
n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

# Caching the data load function to avoid re-fetching
@st.cache_data
def load_data(ticker):
    for _ in range(3):  # Retry 3 times
        try:
            data = yf.download(ticker, START, TODAY)
            if data.empty:
                st.warning(f"No data returned for ticker: {ticker}")
                return pd.DataFrame()  # Return an empty DataFrame if no data is returned
            data.reset_index(inplace=True)
            return data
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            time.sleep(1)  # Add delay between retries
    return pd.DataFrame()  # Return empty DataFrame if all retries fail

# Loading data for the selected stock
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

# Display raw data if it's available
if not data.empty:
    st.subheader('Raw data')
    st.write(data.tail())

    # Function to plot the raw stock data
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    # Prepare the data for Prophet model (forecasting)
    df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

    # Predict forecast with Prophet
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show forecast data and plot the forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)

    # Benchmark comparison with S&P 500 (SPY)
    benchmark = 'SPY'  # S&P 500 ETF
    benchmark_data = yf.download(benchmark, START, TODAY)
    benchmark_data.reset_index(inplace=True)  # Reset the index to get Date as a column

    # Function to plot stock vs S&P 500
    def plot_stock_vs_benchmark(stock_data, benchmark_data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name="Stock Close"))
        fig.add_trace(go.Scatter(x=benchmark_data['Date'], y=benchmark_data['Close'], name="S&P 500 Close"))
        fig.layout.update(title_text='Stock vs S&P 500', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    # Display comparison
    plot_stock_vs_benchmark(data, benchmark_data)

else:
    st.error(f"Unable to load data for {selected_stock}. Please try another stock.")

# Stock Suggestion Module
moving_avg_period = 30

# Function to fetch stock data for a given ticker
def fetch_stock_data(ticker):
    """
    Fetch stock data for a given ticker.
    """
    try:
        data = yf.download(ticker, period='60d')
        return data
    except Exception as e:
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

# Function to suggest stocks that are trending upwards
def suggest_stocks(stocks):
    """
    Suggest stocks that are trending upwards.
    """
    suggestions = []
    
    for stock in stocks:
        data = fetch_stock_data(stock)
        
        if data.empty or data['Close'].empty:
            continue
        
        data['Moving_Avg'] = data['Close'].rolling(window=moving_avg_period).mean()
        
        # Check if there is enough data to make the comparison
        if len(data) < moving_avg_period:
            continue
        
        # Get the most recent price and moving average
        recent_price = data['Close'].iloc[-1]
        recent_moving_avg = data['Moving_Avg'].iloc[-1]
        
        if recent_price > recent_moving_avg:
            suggestions.append(stock)
        
        # Adding a delay to avoid rate-limiting
        time.sleep(1)  # Adjust delay as needed to prevent API rate-limiting
    
    return suggestions

# Get stock suggestions based on recent performance
suggested_stocks = suggest_stocks(stocks)

# Display the suggested stocks
st.subheader('Suggested stocks to buy')
if suggested_stocks:
    st.write("Stocks trending upwards based on recent performance:")
    st.write(suggested_stocks)
else:
    st.write("No stocks are currently trending upwards.")