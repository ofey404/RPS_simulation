import matplotlib.pyplot as plt
from math import sqrt

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from util import v_add, v_mul, plot_edge_set, generate_triangular_edges_from_origin
import util


def triangle_to_characteristic_length(triangle_size):
    if triangle_size % 3 != 0:
        Exception("triangle_size should be division of 3, but {}".format(triangle_size))
    return triangle_size // 3


def above_border1(point, characteristic_length):
    x = point[0]
    y = point[1]
    # - 0.05 to fix the floating point error
    return y > -0.05 + -sqrt(3) * x + sqrt(3) * characteristic_length


def above_border2(point, characteristic_length):
    x = point[0]
    y = point[1]
    # - 0.05 to fix the floating point error
    return y > -0.05 + sqrt(3) * x - 2 * sqrt(3) * characteristic_length


def below_border3(point, characteristic_length):
    x = point[0]
    y = point[1]
    # 0.05 to fix the floating point error
    return y < 0.05 + sqrt(3) * characteristic_length


def test_border():
    assert above_border1([0, 0], 1) == False
    assert above_border1([1, 0], 1) == True
    assert above_border1([1, 0], 2) == False
    assert above_border1([2, 0], 2) == True

    assert above_border2([2, 0], 1) == True
    assert above_border2([3, 0], 1) == False
    assert above_border2([4, 0], 2) == True
    assert above_border2([5, 0], 2) == False

    print("test passed")
    exit(0)


def point_out_of_hexagon(point, triangle_size):
    s = triangle_to_characteristic_length(triangle_size)
    if above_border1(point, s) and above_border2(point, s) and below_border3(point, s):
        return False
    return True


def strip_not_hexagon_edges(triangle_edges, triangle_size):
    ans = []
    for edge in triangle_edges:
        start = edge[0]
        end = edge[1]
        if point_out_of_hexagon(start, triangle_size) or point_out_of_hexagon(
            end, triangle_size
        ):
            continue
        ans.append(edge)
    return ans


def plot_2d_hexagon_grid(size, filepath):
    edges_type_1, edges_type_2, edges_type_3 = generate_triangular_edges_from_origin(
        size
    )
    edges_type_1 = strip_not_hexagon_edges(edges_type_1, size)
    edges_type_2 = strip_not_hexagon_edges(edges_type_2, size)
    edges_type_3 = strip_not_hexagon_edges(edges_type_3, size)

    fig, ax = plt.subplots(subplot_kw={"aspect": "equal"})
    plot_edge_set(ax, edges_type_1, color="red")
    plot_edge_set(ax, edges_type_2, color="blue")
    plot_edge_set(ax, edges_type_3, color="black")
    plt.savefig(filepath)
    plt.close()


def main():
    for i in range(3, 3 * 7, 3):
        plot_2d_hexagon_grid(i, "./2d_triangle_grid_{}.png".format(i))


if __name__ == "__main__":
    main()
