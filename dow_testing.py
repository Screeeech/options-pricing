from options_pricer import price_options
from history_analysis import get_stats
from absolute_risk import calculate_expected_return
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
from scipy.stats import norm
import pandas as pd
import pickle

bets = []
dow = pd.read_csv("dow.csv")

for ticker in dow["Symbol"]:
    print(ticker)
    try:
        # maybe we can also return the last price in price_options()
        # that way we don't have to download data again at the end of
        # loop to input s
        priced_options = price_options(ticker, "2022-09-02", .091)
    except:
        continue

    mu, std = get_stats("aapl", 1, end=date.today() - relativedelta(days=7))

    expected_returns = []
    drops = []
    for i in range(priced_options.shape[0]):
        s = yf.download(ticker, progress=False).iloc[-1]["Adj Close"]
        expected_returns.append(calculate_expected_return(priced_options.iloc[i]["contractSymbol"],
                                                          priced_options.iloc[i]["ask"],
                                                          lambda x: norm.pdf(x, s, std),
                                                          s * (1 + mu - std), s * (1 + mu + std)))
        if expected_returns[i] <= 0:
            drops.append(i)

    priced_options["expected_returns"] = expected_returns
    bets.append(priced_options.drop(priced_options.index[drops]))

with open('dow_bets.pickle', 'wb') as f:
    pickle.dump(bets, f)
