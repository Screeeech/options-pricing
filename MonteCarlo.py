import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def random_function():
    return np.random.choice([-1, 1])


def step_function(s, delt, mu, sigma):
    return s + mu * s * delt + sigma * s * random_function() * np.sqrt(delt)


def create_monte_carlo(init_price, end, period, mu= .12, sigma=.7, n=256):
    p_df = pd.DataFrame(columns=["time-" + period, "price"])

    p_df.loc[0] = [0, init_price]

    for i in range(1, end * n + 1):
        p_df.loc[i] = [i/n, step_function(p_df["price"][i-1], end/n, mu, sigma)]

    plt.plot(p_df["time-" + period], p_df["price"])
    plt.show()


if __name__ == '__main__':
    create_monte_carlo(40, 1, "days")
