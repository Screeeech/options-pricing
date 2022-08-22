import pandas as pd
from options_pricer import price_options
from absolute_risk import risk_cutoff
import yfinance as yf
import pickle


bets = []
dow = pd.read_csv("dow.csv")

for ticker in dow["Symbol"]:
    print(ticker)
    try:
        priced_options = price_options(ticker, "2022-08-26", .091)
    except:
        continue
    bets.append(priced_options[:risk_cutoff(ticker, yf.download(ticker).iloc[-1]["Adj Close"], priced_options)])


with open('dow_bets_2022-08-26.pkl', 'wb') as f:
    pickle.dump(bets, f)
