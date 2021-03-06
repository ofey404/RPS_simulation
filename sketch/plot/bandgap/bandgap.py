import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from math import sin, cos, sqrt, pi

r1 = 1
r2 = 1


def f1_factory(r1, r2, r3):
    def f1_positive(k):
        return r1 * sin(k) + sqrt(
            (r1 ** 2 + r2 ** 2) * sin(k) ** 2 + (r3 - r2 * cos(k)) ** 2
        )

    def f1_negative(k):
        return r1 * sin(k) - sqrt(
            (r1 ** 2 + r2 ** 2) * sin(k) ** 2 + (r3 - r2 * cos(k)) ** 2
        )

    return (np.vectorize(f1_positive), np.vectorize(f1_negative))


def plot_bandgap(r, filepath):
    x = np.arange(-1 * pi, pi, 0.01)

    r3 = r2 / r

    f1_positive, f1_negative = f1_factory(r1, r2, r3)
    y1 = f1_positive(x)
    y2 = f1_negative(x)

    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.xlabel("k")
    plt.ylabel("λ")
    plt.xticks([-pi, -pi/2, 0, pi/2, pi], ["$-\pi$", "$-\pi/2$", "$0$", "$\pi/2$", "$\pi$"])

    # plt.show()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()


def plot_ellipse(r, filepath):
    r3 = r2 / r

    xy = (0, -r3)
    width = 4 * r1 * r2 / sqrt(r1 ** 2 + r2 ** 2)
    height = r2 * 2

    fig, ax = plt.subplots()
    e = Ellipse(xy=xy, width=width, height=height, angle=0, linewidth=2, fill=False)
    ax.add_artist(e)
    ax.arrow(0, 0, xy[0]+width/2, xy[1], head_width=0.05, head_length=0.1, length_includes_head=True, fc='k', ec='k')

    ax.set_xlim(-width, width)
    ax.set_ylim(-r3 - height, 1)
    ax.set_xlabel("h1")
    ax.set_ylabel("h2")
    ax.xaxis.set_label_coords(0.9, 0.5)
    ax.yaxis.set_label_coords(0.5, 0.1)

    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.spines["left"].set_smart_bounds(True)
    ax.spines["bottom"].set_smart_bounds(True)
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")

    # plt.show()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()


def plot(r):
    plot_bandgap(r, "./bandgap-{:.2}.png".format(r))
    plot_ellipse(r, "./ellipse-{:.2}.png".format(r))


def main():
    for r in [0.5, 1.0, 1.5, 2.0]:
        plot(r)


if __name__ == "__main__":
    main()
