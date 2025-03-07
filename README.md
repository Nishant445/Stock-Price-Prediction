# Stock Price Prediction Web Application

This project implements a stock price prediction system as a web application using the Django framework. It predicts stock prices using two different models: ARIMA (AutoRegressive Integrated Moving Average) and LSTM (Long Short-Term Memory).
The user can specify the number of days for which they want the stock price prediction, and they can also view fundamental data and news related to the stock.

The stock data is obtained and trained using the yfinance API, and the application allows users to explore the historical stock data and recent news.

## Technologies Used

Django (Web Framework)
Python (Programming Language)
ARIMA (Time Series Model)
LSTM (Deep Learning Model)
yfinance API (Stock Data Fetching)
Pandas (Data Handling)
NumPy (Numerical Operations)
Matplotlib (Data Visualization)
Plotly (Interactive Plots)

## Project Overview
The stock price prediction web application provides the following features:

Stock Price Prediction: Predict future stock prices using ARIMA and LSTM models.
Historical Data: View the stock's historical price data.
Fundamental Data: Get key fundamental data about the stock, such as market cap, P/E ratio, and more.
Stock News: View recent news articles related to the stock.
Model Choice: Users can choose between ARIMA and LSTM models to generate predictions.
The stock price data and fundamental data are fetched using the yfinance API, and the user can specify how many days they want predictions for.

## Key Features

Stock Price Prediction: Predicts future stock prices based on past data using ARIMA and LSTM models.
Interactive Dashboard: A simple and intuitive user interface to interact with stock predictions and view results.
View Historical Stock Data: Displays historical stock prices and allows users to visualize the data in various formats.
View Fundamental Data: Shows key financial data such as market cap, PE ratio, dividends, etc.
News Related to Stocks: Displays recent news related to the selected stock.
yfinance API Integration: Fetches real-time stock price data and financial information.

## Features

. Stock Price Prediction
Users can select a stock ticker and specify the number of days they want predictions for.
The application uses ARIMA and LSTM models to predict future stock prices.
Predictions are displayed along with the historical data for comparison.
2. Historical Stock Data
Displays the stock price data for the last specified period, fetched using the yfinance API.
Users can visualize the data in interactive charts.
3. Fundamental Data
Displays key financial metrics such as the P/E ratio, market capitalization, EPS, dividend yield, and other stock fundamentals.
4. Stock News
Displays the latest news related to the selected stock, fetched from yfinance and other sources.
5. Model Choice
Users can choose between the ARIMA or LSTM models for stock price prediction.
ARIMA is used for time-series forecasting, particularly effective for simpler time series data.
LSTM is a deep learning model that can capture complex patterns in sequential data.

## Acknowledgements

yfinance API: For fetching stock data and fundamental data.
Django: For creating the web framework.
ARIMA: For time-series modeling.
LSTM: For advanced sequential data prediction.
