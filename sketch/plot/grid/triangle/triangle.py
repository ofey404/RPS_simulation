from os import confstr
import sys
import numpy as np
from numpy import core, square
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from math import sqrt


def v_add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]


def v_mul(k, v):
    return [v[0] * k, v[1] * k]


def generate_all_edges(size):
    u = [1, 0]
    v = [1 / 2, sqrt(3) / 2]

    subscripts = [[i, j] for i in range(size) for j in range(size) if i + j < size]
    origins = [v_add(v_mul(i, u), v_mul(j, v)) for i, j in subscripts]

    edge_1 = [1 / 2, sqrt(3) / 2]
    edges_type_1 = [(v_add(o, edge_1), o) for o in origins]
    edge_2 = [1, 0]
    edges_type_2 = [(o, v_add(o, edge_2)) for o in origins]

    # For edge 3 we need a shift of origin to get the whole set.
    edge_3 = [1 / 2, -sqrt(3) / 2]
    shift = [1 / 2, sqrt(3) / 2]
    origins_shifted = [v_add(shift, o) for o in origins]
    edges_type_3 = [(v_add(os, edge_3), os) for os in origins_shifted]

    return (edges_type_1, edges_type_2, edges_type_3)


def edge_to_arrow(ax, edge, color="k"):
    ax.arrow(
        edge[0][0],
        edge[0][1],
        edge[1][0] - edge[0][0],
        edge[1][1] - edge[0][1],
        head_width=0.05,
        head_length=0.1,
        length_includes_head=True,
        fc=color,
        ec=color,
    )

def plot_edge_set(ax, edges, color):
    for e1 in edges:
        edge_to_arrow(ax, e1, color=color)


def plot_2d_triangle_grid(size, filepath):
    edges_type_1, edges_type_2, edges_type_3 = generate_all_edges(size)
    fig, ax = plt.subplots(subplot_kw={"aspect": "equal"})
    plot_edge_set(ax, edges_type_1, color="red")
    plot_edge_set(ax, edges_type_2, color="blue")
    plot_edge_set(ax, edges_type_3, color="black")
    plt.savefig(filepath)
    plt.close()


def main():
    for i in range(1, 7):
        plot_2d_triangle_grid(i, "./2d_triangle_grid_{}.png".format(i))


if __name__ == "__main__":
    main()
