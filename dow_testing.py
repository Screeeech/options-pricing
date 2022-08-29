import pandas as pd
from options_pricer import price_options
from absolute_risk import normal_risk_cutoff, uniform_risk_cutoff
import yfinance as yf
import pickle

uniform_bets = []
normal_bets = []
dow = pd.read_csv("dow.csv")

for ticker in dow["Symbol"]:
    print(ticker)
    try:
        # maybe we can also return the last price in price_options()
        # that way we don't have to download data again at the end of
        # loop to input s
        priced_options = price_options(ticker, "2022-08-26", .091)
    except:
        continue

    uniform_bets.append(priced_options[:uniform_risk_cutoff(ticker, yf.download(ticker).iloc[-1]["Adj Close"],
                                                            priced_options)])
    normal_bets.append(priced_options[:normal_risk_cutoff(ticker, yf.download(ticker).iloc[-1]["Adj Close"],
                                                          priced_options)])

with open('uniform_dow_bets_2022-08-26.pkl', 'wb') as f:
    pickle.dump(uniform_bets, f)

with open('normal_bets_2022-08-26.pkl', 'wb') as f:
    pickle.dump(normal_bets, f)
