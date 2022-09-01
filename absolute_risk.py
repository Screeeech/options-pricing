import numpy as np
from scipy import integrate
import history_analysis as hanal
from options_pricer import symbol_parts
from scipy.stats import norm


def return_at_s(s, x, k):
    return np.maximum(s - x, 0) - k


def return_of_bets_at_s(bets, s):
    return np.sum([return_at_s(s, symbol_parts(bets.iloc[i]["contractSymbol"])[3], bets.iloc[i]["ask"]) for i in
                   range(bets.shape[0])])


def lreimann(lbound, ubound, contract_symbol, k, probability_density, delx):
    x = np.linspace(lbound, ubound, int(delx * (ubound - lbound)))
    return np.sum([return_at_s(x[i], symbol_parts(contract_symbol)[3], k)*probability_density(x[i]) / delx for i in range(len(x) - 1)])


def calculate_expected_return(contract_symbol, k, normal_function, lbound, ubound, dollar_resolution=20):
    return lreimann(lbound, ubound, contract_symbol, k, normal_function, dollar_resolution)


# print(calculate_expected_return("AAPL220902C00070000", 91.50, lambda x: norm.pdf(x, 161.50, 7), 161.50-7, 161.50+7))
