import numpy as np
import matplotlib.pyplot as plt

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from util import plot_matrix

def matrix_generator(n, R):
    coordinates = {}
    head = 0
    r1, r2, r3 = R
    for i in range(n):
        head += i
        for j in range(head, head+i+1):
            coordinates[(i-j+head, j-head)] = j

    A = np.zeros((n*(n+1)//2, n*(n+1)//2))
    for pair in coordinates:
        x, y = pair
        value = coordinates[pair]
        
        if x > 0:
            A[value, coordinates[(x-1, y)]] = r1
            A[value, coordinates[(x-1, y+1)]] = -r2
        if y > 0:
            A[value, coordinates[(x, y-1)]] = -r3
            A[value, coordinates[(x+1, y-1)]] = r2
        if x+y < n-1:
            A[value, coordinates[(x, y+1)]] = r3
            A[value, coordinates[(x+1, y)]] = -r1

    return A

if __name__ == '__main__':
    plot_matrix(matrix_generator, r_lim=3)

        
