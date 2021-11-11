import sys
import matplotlib.pyplot as plt
from math import sqrt

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from util import v_add, v_mul, plot_edge_set, generate_triangular_edges_from_origin
import util


def plot_2d_triangle_grid(size, filepath):
    u = util.u
    v = util.v
    subscripts = [[i, j] for i in range(size) for j in range(size) if i + j < size]
    origins = [v_add(v_mul(i, u), v_mul(j, v)) for i, j in subscripts]

    edges_type_1, edges_type_2, edges_type_3 = generate_triangular_edges_from_origin(
        origins
    )
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
