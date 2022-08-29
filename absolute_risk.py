import numpy as np
from scipy import integrate
import history_analysis as hanal
from options_pricer import symbol_parts
from scipy.stats import norm


def caculate_risk(s, bets):
    risk = []
    for i in range(bets.shape[0]):
        risk.append((symbol_parts(bets.iloc[i].contractSymbol)[3] - s + bets.iloc[i]["ask"]) / s)

    bets["risk"] = risk


def return_at_s(s, x, k):
    return np.maximum(s - x, 0) - k


def return_of_bets_at_s(bets, s):
    return np.sum([return_at_s(s, symbol_parts(bets.iloc[i]["contractSymbol"])[3], bets.iloc[i]["ask"]) for i in
                   range(bets.shape[0])])


# Do not use, integration does not work with this function
# Use lreimann()
def returns_over_s(s, mu, sigma, bets):
    return integrate.quad(lambda x: return_of_bets_at_s(bets, x), s * (1 + mu + sigma), s * (1 + mu - sigma))


def lreimann(lbound, ubound, contract_symbol, delx):
    x = np.linspace(lbound, ubound, int(delx * (ubound - lbound)))
    k = symbol_parts(contract_symbol)[3]

    return np.sum([return_at_s(contract_symbol, x[i], k) / delx for i in range(len(x) - 1)])


def trap_reimann(lbound, ubound, bets, delx, mu, sigma):
    x = np.linspace(lbound, ubound, int(delx * (ubound - lbound)))
    base1 = return_of_bets_at_s(bets, x[0])
    integral = 0
    for i in range(len(x) - 1):
        base2 = return_of_bets_at_s(bets, x[i + 1])
        # what is this formatting, if you're wrapping at least make it neat
        integral += .5 * (x[i + 1] - x[i]) * (
                    base1 * norm.pdf(x[i], x[i] * (1 + mu), x[i] * sigma) + base2 * norm.pdf(x[i + 1],
                                                                                             x[i + 1] * (1 + mu),
                                                                                             x[i + 1] * sigma))
        base1 = base2
    return integral


def calculate_expected_return(bet, k, normal_function, s, mu, sigma):
    return lreimann(s*(1+mu-sigma), s*(1+mu-sigma), bet, 20)


def find_max_integral(bets, function):
    beg = 0
    end = bets.shape[0]

    result = -1
    while beg != end:
        mid = (beg + end) // 2
        if function(mid) > function(end):
            end = mid

        else:
            beg = mid + 1
        result = beg

    return result


def uniform_risk_cutoff(ticker, s, bets, sigma_range=(-1, 1), dollar_resolution=20):
    # bets = price_options(ticker, "2022-08-26", .091)
    caculate_risk(s, bets)
    bets.sort_values("risk")

    dollar_resolution = np.minimum(dollar_resolution, 100)
    mu, sigma = hanal.get_stats(ticker, 1)
    max_int = find_max_integral(bets, lambda m: lreimann(s * (1 + mu + (sigma_range[0] * sigma)),
                                                         s * (1 + mu + (sigma_range[1] * sigma)),
                                                         bets.iloc[:m], dollar_resolution))

    return max_int


def normal_risk_cutoff(ticker, s, bets, sigma_range=(-1, 1), dollar_resolution=20):
    # bets = price_options(ticker, "2022-08-26", .091)
    caculate_risk(s, bets)
    bets.sort_values("risk")

    dollar_resolution = np.minimum(dollar_resolution, 100)
    mu, sigma = hanal.get_stats(ticker, 1)
    max_int = find_max_integral(bets, lambda m: trap_reimann(s * (1 + mu + (sigma_range[0] * sigma)),
                                                             s * (1 + mu + (sigma_range[1] * sigma)),
                                                             bets.iloc[:m], dollar_resolution, mu, sigma))

    return max_int


"""
priced_options = price_options("aapl", "2022-08-26", .091)
cutoff = risk_cutoff("aapl", 171.52, priced_options)
print(cutoff)
"""
