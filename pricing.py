import math
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import stat_helper as sh

def get_size(frame: pd.DataFrame) -> int:
    return frame.size

def extract_prices(frame: pd.DataFrame) -> np.ndarray:
    return np.array(frame["Close"].tolist())

def extract_column(frame: pd.DataFrame, metric: str) -> np.ndarray:
    metric = metric.strip().lower()
    return np.array(frame[metric].tolist())

def generate_X_axis(Y: np.array) -> np.ndarray:
    axis = sh.generate_X(len(Y))
    return axis

def fetch_price_data(stock: str, timerange: str) -> pd.DataFrame:
    '''
    :param timerange: 1m, 1h, 1d, 1w, 1mo, 3mo, 6mo, 1y, 2y, 5y
    '''
    timerange = timerange.lower().strip()
    load = yf.Ticker(stock)
    frame = load.history(timerange)
    return frame 

def plot_price_data(stock: str, timerange: str, sma_period=3, multiple_sma=False, show_variance=False):
    colors = ["blue", "green", "orange", "red", " purple", "pink"]

    # general data load
    data = fetch_price_data(stock, timerange)

    # create two plot indeces
    fig, axs = plt.subplots(2)

    # get & plot price data
    prices = extract_prices(data)
    X = generate_X_axis(prices)
    axs[0].plot(X, prices, color=colors[0], label="Price")

    # basic indicator -- Simple Moving Average
    sma = sh.sma(prices, sma_period)

    # treat two moving averages
    if (multiple_sma):
        secondary_period = sma_period*2
        secondary_sma = sh.sma(prices, secondary_period)
        axs[0].plot(np.array(sma[0]), np.array(sma[1]), color=colors[1], label=f"SMA {sma_period}")
        axs[0].plot(np.array(secondary_sma[0]), np.array(secondary_sma[1]), color=colors[2], label=f"SMA {secondary_period}")
    if (not multiple_sma):
        axs[0].plot(np.array(sma[0]), np.array(sma[1]), color=colors[1], label=f"SMA {sma_period}")
    
    # basic indicator -- Linear Regression
    prices_reg = sh.get_Ylistregress(X, prices)

    # plot regression line
    axs[0].plot(X, prices_reg, color=colors[3], label="Linreg.")
    
    # get variance data
    prices_var = []
    seen = []
    for price in prices:
        seen.append(price)
        # calculate current variance
        prices_var.append(sh.variance(seen))
        # plot running variance

    prices_vol = [math.sqrt(variance) for variance in prices_var]
    prices_var = np.array(prices_var)
    prices_vol = np.array(prices_vol)

    # plot variance/volatility 
    if (show_variance):
        axs[1].plot(X, prices_var, color=colors[4], label="Variance")
        axs[1].plot(X, prices_vol, color=colors[5], linestyle="dashed", label="Volatility")
    if (not show_variance):
        axs[1].plot(X, prices_vol, color=colors[5], linestyle="dashed", label="Volatility")
    axs[0].legend()
    axs[1].legend()
    plt.show()





