from os import confstr
import sys
import numpy as np
from numpy import core
from util import parse_argv, get_data_files
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import pickle


def get_xy(data, ts):
    n, _ = data["shape"]
    x = np.arange(n)
    y = data["result"][:, ts]
    return (x, y)


class Circle(Ellipse):
    def __init__(self, xy, diameter, color=None, alpha=None):
        super().__init__(xy=xy, width=diameter, height=diameter, angle=0)
        self.set_alpha(alpha if alpha is not None else 0.5)
        self.set_facecolor(color if color is not None else np.random.rand(3))


class Visualizer:
    def __init__(self, data, config) -> None:
        self.data = data
        self.config = config

        self.color_scale = [np.random.rand(3) for _ in range(data["shape"][0])]
        self.border = sum(data["result"][:, 0]) / 4

    def plt_visualize_1D(self, ts, filepath):
        fig, ax = plt.subplots(subplot_kw={"aspect": "equal"})
        xs, ys = get_xy(self.data, ts)
        n = xs.shape[0]
        previous_xy = None
        for i in range(n):
            xy = (xs[i], 0 if i % 2 == 0 else 1)
            diameter = ys[i]
            ax.add_artist(Circle(xy=xy, diameter=diameter, color=self.color_scale[i]))
            # ax.add_artist(Circle(xy=xy, diameter=diameter))
            if previous_xy:
                ax.arrow(
                    previous_xy[0],
                    previous_xy[1],
                    xy[0] - previous_xy[0],
                    xy[1] - previous_xy[1],
                )
            previous_xy = xy

        ax.set_xlim(-self.border, n + self.border)
        ax.set_ylim(-self.border, self.border)

        # plt.show()
        plt.savefig(filepath)
        plt.close()

    def plt_log_x(self, ts, filepath):
        x, y = get_xy(self.data, ts)
        y = np.log(y)

        k, b = np.polyfit(x, y, 1)

        plt.bar(x, y)
        plt.xlabel("site alpha")
        plt.ylabel("log(x_alpha)")

        plt.plot(x, k * x + b, "k-")

        plt.savefig(filepath)
        plt.close()


def main(argv):
    config, data_dir = parse_argv(argv)
    data_file_path = get_data_files(data_dir)[0]
    step = config["plot_step"]

    np.random.seed(42)

    with open(data_file_path, "rb") as data_file:
        data = pickle.load(data_file)
        n, t = data["shape"]
        v = Visualizer(data, config)
        for plot_ts in range(0, t, step):
            v.plt_log_x(plot_ts, data_dir / "log_plt_{}.png".format(plot_ts))
            v.plt_visualize_1D(
                plot_ts, data_dir / "visualization_{}.png".format(plot_ts)
            )


if __name__ == "__main__":
    main(sys.argv)
