import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def random_function():
    return np.random.choice([-1, 1])


def step_function(s, delt, mu, sigma):
    return s + mu * s * delt + sigma * s * random_function() * np.sqrt(delt)


def payoff(df, k):
    return max(df["price"].iloc[-1] - k, 0)


def create_monte_carlo(init_price, end, mu=.12, sigma=.7, n=256):
    p_df = pd.DataFrame(columns=["time", "price"])

    p_df.loc[0] = [0, init_price]

    for i in range(1, end * n + 1):
        p_df.loc[i] = [i / n, step_function(p_df["price"][i - 1], end / n, mu, sigma)]

    return p_df


if __name__ == '__main__':
    p_df = create_monte_carlo(40, 1)
    plt.plot(p_df["time"], p_df["price"])
    plt.show()
