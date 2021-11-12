import sys
from math import sqrt
import numpy as np
from util import parse_argv, get_data_files
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import pickle


def get_xy(data, ts):
    n, _ = data["shape"]
    x = np.arange(n)
    y = data["result"][:, ts]
    return (x, y)


def set_fig_ratio(ax, ratio):
    # Thanks to https://jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl/
    ratio = 0.3
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    # the abs method is used to make sure that all numbers are positive
    # because x and y axis of an axes maybe inversed.
    ax.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * ratio)


class Circle(Ellipse):
    def __init__(self, xy, diameter, color=None, alpha=None):
        super().__init__(xy=xy, width=diameter, height=diameter, angle=0)
        self.set_alpha(alpha if alpha is not None else 0.5)
        self.set_facecolor(color if color is not None else np.random.rand(3))


class Visualizer:
    def __init__(self, data, config, left_polarization=False) -> None:
        self.data = data
        self.config = config

        self.T = 2000
        self.result = self.data["result"]
        self.windowed_result = self.result[:, -self.T :]

        # Exclude first X in plt_temporal_mass_average()
        self.exculde_first_S_in_average = 2
        self.left_polarization = left_polarization

        self.color_scale = [np.random.rand(3) for _ in range(data["shape"][0])]
        self.border = sum(data["result"][:, 0]) / 5

    def plt_temporal_mass_average(self, filepath):
        result = self.windowed_result

        fig, ax = plt.subplots()

        x = np.arange(self.data["shape"][0])
        avg = np.average(result, axis=1)

        if self.left_polarization:
            x = x[: -self.exculde_first_S_in_average]
            avg = avg[: -self.exculde_first_S_in_average]
        else:
            x = x[self.exculde_first_S_in_average :]
            avg = avg[self.exculde_first_S_in_average :]


        log_avg = np.log(avg)
        k, b = np.polyfit(x, log_avg, 1)

        ax.scatter(x, log_avg)
        ax.plot(x, k * x + b, "k-")
        ax.set_xlabel("S")
        ax.set_ylabel("log_avg")

        set_fig_ratio(ax, 0.3)
        plt.savefig(filepath, bbox_inches="tight")
        plt.close()

    def plt_temporal_mass_average_visualization(self, filepath):
        fig, ax = plt.subplots(subplot_kw={"aspect": "equal"})
        result = self.windowed_result

        x = np.arange(self.data["shape"][0])
        avg = np.average(result, axis=1)

        n = x.shape[0]
        previous_xy = None
        for i in range(n):
            xy = (x[i], 0 if i % 2 == 0 else sqrt(3))
            diameter = avg[i]
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
        ax.set_ylim(-self.border, self.border + sqrt(3))

        plt.xlabel("S")

        plt.savefig(filepath, bbox_inches="tight")
        plt.close()

    def plt_temporal_mass_variance(self, filepath):
        result = self.windowed_result

        fig, ax = plt.subplots()

        x = np.arange(self.data["shape"][0])
        var = np.var(result, axis=1)

        k, b = np.polyfit(x, var, 1)

        ax.scatter(x, var)
        ax.plot(x, k * x + b, "k-")
        ax.set_xlabel("S")
        ax.set_ylabel("$\sigma$")

        set_fig_ratio(ax, 0.3)

        plt.savefig(filepath, bbox_inches="tight")
        plt.close()


def plot(data, config, output_dir, prefix=""):
    n, t = data["shape"]
    left_polarization = False
    if "expect_left_polarization" in config.keys():
        left_polarization = config["expect_left_polarization"]
    v = Visualizer(data, config, left_polarization)
    v.plt_temporal_mass_average(
        output_dir / "{}temporal_mass_average.png".format(prefix)
    )
    v.plt_temporal_mass_variance(
        output_dir / "{}temporal_mass_variance.png".format(prefix)
    )
    v.plt_temporal_mass_average_visualization(
        output_dir / "{}temporal_mass_average_visualization.png".format(prefix)
    )


def main(argv):
    config, data_dir = parse_argv(argv)
    fp = get_data_files(data_dir)
    data_file_path = ""
    data_addtail_file_path = ""
    for f in fp:
        if f.name.startswith("RPS-addtail"):
            data_addtail_file_path = f
        else:
            data_file_path = f

    np.random.seed(250)

    with open(data_file_path, "rb") as data_file, open(
        data_addtail_file_path, "rb"
    ) as data_addtail_file:
        data = pickle.load(data_file)
        data_addtail = pickle.load(data_addtail_file)
        plot(data, config, output_dir=data_dir)
        plot(data_addtail, config, output_dir=data_dir, prefix="addtail-")


if __name__ == "__main__":
    main(sys.argv)
