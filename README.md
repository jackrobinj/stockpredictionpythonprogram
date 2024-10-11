# Stock Forecast and Suggestion App

This is a Streamlit-based web application that allows users to forecast stock prices and get stock suggestions based on recent performance. The app uses historical stock data to predict future trends using the Prophet model and also provides a comparison with the S&P 500 index.

## Features

- **Stock Forecasting**: Select a stock, and the app will provide a forecast for up to 4 years using the Prophet model.
- **Stock Suggestion Module**: Recommends stocks that are trending upwards based on their moving average.
- **Historical Data Visualization**: Displays raw data and interactive charts for selected stocks.
- **S&P 500 Benchmark Comparison**: Compare selected stock performance with the S&P 500 (SPY) ETF.

## Libraries Required

To run the app, you'll need the following Python libraries:

```bash
pip install streamlit prophet yfinance plotly pandas

How to Run the App
1.Clone the repository or download the code.
2.Install the required libraries using the command above.
3.Run the following command in your terminal to start the Streamlit app:
  streamlit run app.py

Dataset
The app fetches historical stock data from Yahoo Finance using the yfinance API.

Usage
Select a stock from the dropdown list.
Choose the number of years for the forecast (1-4 years).
The app will display the stock’s raw data and forecasted prices.
View the stock performance in comparison with the S&P 500 index.
Get stock suggestions based on their recent moving average trends.
Stock List
Google (GOOG)
Apple (AAPL)
Microsoft (MSFT)
GameStop (GME)
Tesla (TSLA)
Nvidia (NVDA)
Pfizer (PFE)
Moderna (MRNA)
Visa (V)
Stock Suggestion Module
The app suggests stocks that are trending upwards based on the last 30-day moving average.

Author
Jack Robin J

License
This project is licensed under the MIT License - see the LICENSE file for details.

### Instructions:
- Save the above content as a `README.md` file.
- Upload it to your GitHub repository for the project.

Feel free to modify the content or add additional sections like "Known Issues" or "Future Improvements" if needed.
