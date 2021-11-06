import sys

import numpy as np
import matplotlib.pyplot as plt
import imageio
import time
import pickle


def get_xy(data, ts):
    n, _ = data["shape"]
    x = np.arange(n)
    y = data["result"][:, ts]
    return (x, y)


def plt_log_x(data, ts, filepath):
    x, y = get_xy(data, ts)

    y = np.log(y)

    k, b = np.polyfit(x, y, 1)

    plt.bar(x, y)
    plt.xlabel("site alpha")
    plt.ylabel("log(x_alpha)")

    plt.plot(x, k*x+b, 'k-')

    plt.savefig(filepath)
    plt.close()


# def polyfit_with_cov(data, ts, filepath)

def print_xy(data, ts):
    x, y = get_xy(data, ts)
    print("\nts = {}".format(ts))
    print(y)


def main():
    if len(sys.argv) <= 1:
        print("Usage: python RPS_plot.py RPS-2021-11-04-15:59:44.pkl")

    usage = """[0] Plot with log polyfit (plt_log_x).
[1] Print x and y.
Input to select function: """

    function = input(usage)

    with open(sys.argv[1], "rb") as data_file:
        data = pickle.load(data_file)
        n, t = data["shape"]
        for i in range(0, 5000, 500):

            if function == "0":
                plt_log_x(data, i, "log_plt_{}.png".format(i))
            elif function == "1":
                print_xy(data, i)
            else:
                print("No function {}".format(function))
                break


if __name__ == "__main__":
    main()
