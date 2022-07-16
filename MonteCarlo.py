import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def random_function():
    return np.random.choice([-1, 1])


def monte_expression(s, delt, mu, sigma):
    return s + mu * s * delt + sigma * s * random_function() * np.sqrt(delt)


def create_monte_carlo(init_price, end, mu=.12, sigma=.7, n=256):
    pricehist = np.zeros(n)
    pricehist[0] = init_price

    for i in range(1, n):
        pricehist[i] = monte_expression(pricehist[i - 1], end / n, mu, sigma)

    return pricehist


def price_estimate(r, k, m, init_price, end, sigma=.7, n=256):
    f = lambda x: np.max((create_monte_carlo(init_price, end, mu=r, sigma=sigma, n=n)[-1] - x, 0))
    k_list = np.full(m, k)
    k_list = list(map(f, k_list))
    m_avg = np.mean(k_list)
    return (1 + r * (end/n))**-n * m_avg


if __name__ == '__main__':
    '''p_df = create_monte_carlo(40, 1)
    plt.plot(p_df["time"], p_df["price"])
    plt.show()
    '''
    print(price_estimate(.06, 50, 1000, 40, 5/12, sigma=.2, n=254))
