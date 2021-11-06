from os import confstr
import sys
import numpy as np
from util import parse_argv, get_data_files
import matplotlib.pyplot as plt
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

# def init(argv):


def main(argv):
    config, data_dir = parse_argv(argv)
    data_file_path = get_data_files(data_dir)[0]
    step = config["plot_step"]

    with open(data_file_path, "rb") as data_file:
        data = pickle.load(data_file)
        n, t = data["shape"]
        for i in range(0, t, step):
            plt_log_x(data, i, data_dir / "log_plt_{}.png".format(i))


if __name__ == "__main__":
    main(sys.argv)
