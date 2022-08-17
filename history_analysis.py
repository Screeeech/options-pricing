import yfinance as yf
import pandas as pd
import re
from datetime import date
import numpy as np
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt


def retrive_weekly_data(ticker, look_back, end=date.today()):
    stock_data = yf.download(ticker, (end - relativedelta(years=look_back)).strftime("%Y-%m-%d"),
                             end.strftime("%Y-%m-%d"), adjusted=True)
    stock_data["pct change"] = stock_data['Adj Close'].pct_change()
    return stock_data.iloc[1:].resample("W", label="right").mean()


def get_stats(ticker, look_back, end=date.today()):
    data = retrive_weekly_data(ticker, look_back, end)
    return np.mean(data["pct change"]), np.std(data["pct change"])


data = retrive_weekly_data("aapl", 1, end=date.today() - relativedelta(days=5))
plt.hist(data["pct change"])
plt.show()

# mu, std = get_stats("aapl", 1, end=date.today() - relativedelta(days=5))
# print(mu, std)
