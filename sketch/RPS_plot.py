import sys

import numpy as np
import matplotlib.pyplot as plt
import imageio
import time
import pickle


def plt_log_x(data, ts, filepath):
    n, _ = data["shape"]
    x = np.arange(n)
    y = np.log(data["result"][:, ts])

    k, b = np.polyfit(x, y, 1)

    plt.plot(x, y)
    plt.xlabel("site alpha")
    plt.ylabel("log(x_alpha)")

    plt.plot(x, k*x+b, 'k-')

    plt.savefig(filepath)
    plt.close()


def main():
    if len(sys.argv) <= 1:
        print("Usage: python RPS_plot.py RPS-2021-11-04-15:59:44.pkl")
    with open(sys.argv[1], "rb") as data_file:
        data = pickle.load(data_file)
        n, t = data["shape"]
        for i in range(t)[::10000]:
            plt_log_x(data, i, "log_plt_{}.png".format(i))


if __name__ == "__main__":
    main()
