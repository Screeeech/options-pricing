import numpy as np
from scipy.integrate import quad
from scipy.special import erfc
from scipy.stats import norm
import matplotlib.pyplot as plt


def d1(s, kmax, r, sigma, t):
    # return np.sum([(np.log(s/k)+(r+sigma**2/2)*t)*(1/(sigma*np.sqrt(t))) for k in range(1, kmax+1)])
    return (np.log(s / kmax) + (r + sigma ** 2 / 2) * t) / (sigma * np.sqrt(t))


def d2(s, kmax, r, sigma, t):
    return d1(s, kmax, r, sigma, t) - sigma * np.sqrt(t)


def step(s, kmax, r, sigma, t, premium):
    return (s / 2) * erfc(-1 * d1(s, kmax, r, sigma, t)/np.sqrt(2)) - (premium / 2) * np.exp(-1 * r * t) * erfc(-1 * d2(s, kmax, r, sigma, t)/np.sqrt(2))
    # return s * norm.cdf(d1(s, kmax, r, sigma, t)) - premium * np.exp(-1 * r * t) * norm.cdf(d2(s, kmax, r, sigma, t))


def final_price(t, n, s, kmax, r, sigma, premium):
    prices = [s]
    for i in range(n):
        prices.append(step(prices[i-1], kmax, r, sigma, t/n, premium))
    return prices[-1]


# print(final_price(5/12, 200, 40, 50, .06, 0.2, 50))
# print(step(40, 50, .06, 0.2, 5/12, 50))
print(step(40, 50, .06, 0.2, 200*(5/12)/254, 50))
k = np.linspace(5/12, 2, 100)
values = list(map(lambda x: step(40, 50, .06, 0.2, x, 50), k))
plt.plot(k, values)
plt.show()
# print(d1(50, 52, .01, 0.2, 1))
# print(d2(50, 52, .01, 0.2, 1))
