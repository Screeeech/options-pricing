import numpy as np
from scipy.integrate import quad
from scipy.special import erfc
from scipy.stats import norm


def d1(s, kmax, r, sigma, t):
    # return np.sum([(np.log(s/k)+(r+sigma**2/2)*t)*(1/(sigma*np.sqrt(t))) for k in range(1, kmax+1)])
    return (np.log(s/kmax)+(r+sigma**2/2)*t)/(sigma*np.sqrt(t))


def d2(s, kmax, r, sigma, t):
    return d1(s, kmax, r, sigma, t) - sigma*np.sqrt(t)


def price(s, kmax, r, sigma, t, premium):
    return (s/2)*erfc(-1*d1(s, kmax, r, sigma, t)) - (premium/2)*np.exp(-1*r*t)*erfc(-1*d2(s, kmax, r, sigma, t))
    # return s * norm.cdf(d1(s, kmax, r, sigma, t)) - premium * np.exp(-1 * r * t) * norm.cdf(d2(s, kmax, r, sigma, t))


print(price(40, 50, .06, 0.2, 5/12, 50))
