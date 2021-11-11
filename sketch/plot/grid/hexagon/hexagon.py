from os import confstr
import sys
import numpy as np
from numpy import core, square
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from math import sqrt

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from util import v_add, v_mul, plot_edge_set


def main():
    for i in range(1, 7):
        plot_2d_triangle_grid(i, "./2d_triangle_grid_{}.png".format(i))


if __name__ == "__main__":
    main()
