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
    edges_type_1, edges_type_2, edges_type_3 = generate_triangular_edges_from_origin(
        size
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
