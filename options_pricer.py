import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import date
import re
from dateutil.relativedelta import relativedelta


def symbol_parts(symbol):
    r = re.search("^[A-Z]*", symbol)
    index = r.span()[1]
    ticker = symbol[0:index]
    year = 2000 + int(symbol[index:index + 2])
    month = int(symbol[index + 2: index + 4])
    day = int(symbol[index + 4: index + 6])
    opt_type = symbol[index + 6: index + 7]
    strike_price = int(symbol[index + 7:]) / 1000
    return ticker, date(year, month, day), opt_type, strike_price


def get_sigma(stock_data):
    log_returns = np.array([stock_data[i + 1] / stock_data[i] for i in range(len(stock_data) - 1)])
    return np.sqrt(np.mean(log_returns ** 2))


def get_d1(sigma, t, s, x, r):
    return 1 / (sigma * np.sqrt(t)) * (np.log(s / x) + (r + sigma ** 2 / 2) * t)


def option_price(symbol, r):
    ticker, t, option_type, x = symbol_parts(symbol)
    t = (t - date.today()).days / 365
    stock_data = yf.download(ticker, (date.today() - relativedelta(days=30)).strftime("%Y-%m-%d"),
                             date.today().strftime("%Y-%m-%d"),
                             adjusted=True, progress=False)['Adj Close']
    s = stock_data[-1]
    sigma = get_sigma(stock_data)
    d1 = get_d1(sigma, t, s, x, r)
    d2 = d1 - sigma * np.sqrt(t)
    return norm.cdf(d1) * s - norm.cdf(d2) * x * np.exp(-1 * r * t)


def price_options(ticker, date, mu):
    aapl = yf.Ticker(ticker)
    calls = aapl.option_chain(date=date).calls

    priced_options = pd.DataFrame(columns=["contractSymbol", "price", "ask"])
    for i in range(calls.shape[0]):
        price = option_price(calls.iloc[i].contractSymbol, mu)
        if price > calls.iloc[i].ask:
            priced_options.loc[i] = [calls.iloc[i].contractSymbol, price, calls.iloc[i].ask]

    return priced_options


# pd.to_pickle(priced_options, "priced_options.pickle")
# print(price_options("aapl", "2022-08-26", .091))
