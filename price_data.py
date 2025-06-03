import yfinance as yf, pandas as pd, matplotlib.pyplot as plt, numpy as np
import math
import scipy.stats as S
# fetch stock price data
aapl = yf.Ticker("AAPL")
prices_df = aapl.history("6mo")

# get list of close prices
close_list = prices_df["Close"].tolist()

#get number of data points
close_list_size = len(close_list)

# build axes
import stat_helper as sh
Y = close_list
X = sh.generate_X(close_list_size)

# plot price data
fig, axs = plt.subplots(2)
axs[0].plot(X, Y, color="blue", label="Price")

# plot other indicators

var_list = []
seen = []
for price in Y:
    seen.append(price)
    # calculate current variance
    var_list.append(sh.variance(seen))
            # plot running variance

vol_list = [math.sqrt(variance) for variance in var_list]

# regress Y
reg_Y_info = S.linregress(X, Y)
b0 = reg_Y_info.intercept
b1 = reg_Y_info.slope
reg = [(b0 + b1*x)for x in X]

# get sma
sma_period = 5
sma = sh.sma(Y, sma_period)

#axs[1].plot(X, var_list, color="mediumvioletred", linestyle="dashed", label="Variance")
axs[1].plot(X, vol_list, color="pink", linestyle="dashed", label="Volatility")
axs[0].plot(X, reg, color="red", label="LinReg")
axs[0].plot(sma[0], sma[1], color="green", label="SMA")
axs[0].legend()
axs[1].legend()
plt.show()