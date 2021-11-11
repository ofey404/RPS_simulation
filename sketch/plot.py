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


class Circle(Ellipse):
    def __init__(self, xy, diameter, color=None, alpha=None):
        super().__init__(xy=xy, width=diameter, height=diameter, angle=0)
        self.set_alpha(alpha if alpha is not None else 0.5)
        self.set_facecolor(color if color is not None else np.random.rand(3))


class Visualizer:
    def __init__(self, data, config) -> None:
        self.data = data
        self.config = config

        self.T = 2000
        self.result = self.data["result"]
        self.windowed_result = self.result[:, -self.T:]
        self.exculde_first_S_in_average = 2

        self.color_scale = [np.random.rand(3) for _ in range(data["shape"][0])]
        self.border = sum(data["result"][:, 0]) / 5

    def plt_temporal_mass_average(self, filepath):
        result = self.windowed_result

        x = np.arange(self.data["shape"][0])
        avg = np.average(result, axis=1)

        x = x[self.exculde_first_S_in_average:]
        avg = avg[self.exculde_first_S_in_average:]

        log_avg = np.log(avg)
        k, b = np.polyfit(x, log_avg, 1)

        plt.scatter(x, log_avg)
        plt.plot(x, k * x + b, "k-")
        plt.xlabel("S")
        plt.ylabel("log_avg")
        plt.savefig(filepath)
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

        plt.savefig(filepath)
        plt.close()

    def plt_temporal_mass_variance(self, filepath):
        result = self.windowed_result

        x = np.arange(self.data["shape"][0])
        var = np.var(result, axis=1)

        k, b = np.polyfit(x, var, 1)

        plt.scatter(x, var)
        plt.plot(x, k * x + b, "k-")
        plt.xlabel("S")
        plt.ylabel("$\sigma$")
        plt.savefig(filepath)
        plt.close()


def main(argv):
    config, data_dir = parse_argv(argv)
    data_file_path = get_data_files(data_dir)[0]
    step = config["plot_step"]

    np.random.seed(250)

    with open(data_file_path, "rb") as data_file:
        data = pickle.load(data_file)
        n, t = data["shape"]
        v = Visualizer(data, config)
        v.plt_temporal_mass_average(data_dir / "temporal_mass_average.png")
        v.plt_temporal_mass_variance(data_dir / "temporal_mass_variance.png")
        v.plt_temporal_mass_average_visualization(
            data_dir / "temporal_mass_average_visualization.png"
        )


if __name__ == "__main__":
    main(sys.argv)
