import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def random_function():
    return np.random.choice([-1, 1])


def monte_expression(s, delt, mu, sigma):
    return s + mu * s * delt + sigma * s * random_function() * np.sqrt(delt)


def payoff(df, k):
    return np.max([df["price"].iloc[-1] - k, 0])


def create_monte_carlo(init_price, end, mu=.12, sigma=.7, n=256):
    p_df = pd.DataFrame(columns=["time", "price"])

    p_df.loc[0] = [0, init_price]

    for i in range(1, n):
        p_df.loc[i] = [end * (i / n), monte_expression(p_df["price"][i - 1], end / n, mu, sigma)]

    return p_df


def premium_estimate(r, m, init_price, end, sigma=.7, n=256):
    f = lambda k: np.max([create_monte_carlo(init_price, end, mu=r, sigma=sigma, n=n)["price"].iloc[-1] - k, 0])
    k_list = np.arange(1,m+1)
    k_list = list(map(f,k_list))
    m_avg = np.mean(k_list)
    return (1 + r * (end/n))**-n * m_avg


if __name__ == '__main__':
    '''p_df = create_monte_carlo(40, 1)
    plt.plot(p_df["time"], p_df["price"])
    plt.show()
    '''
    print(premium_estimate(.06, 100000, 40, 5/12, sigma=.2, n=254))
