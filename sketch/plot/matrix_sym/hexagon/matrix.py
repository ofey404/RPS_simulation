import numpy as np
import matplotlib.pyplot as plt

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from util import plot_matrix


def matrix_generator(n, R):
    r1, r2, r3 = R

    l = 2*n-1
    coordinates = {}
    head, layer = 0, n
    for i in range(n):
        layer = l-n+i+1
        for j in range(head, head+layer):
            coordinates[(j-head+n-i-1, i)] = j
        head += layer
        
    for i in range(n, l):
        layer = l+n-i-1
        for j in range(head, head+layer):
            coordinates[(j-head, i)] = j
        head += layer

    A = np.zeros((3*n**2-3*n+1, 3*n**2-3*n+1))
    for pair in coordinates:
        x, y = pair
        value = coordinates[pair]
        
        if x > 0 and x+y > n-1:
            A[value, coordinates[(x-1, y)]] = r1
        if x > 0 and y< l-1:
            A[value, coordinates[(x-1, y+1)]] = -r2
        if y<l-1 and x+y<l+n-2:
            A[value, coordinates[(x, y+1)]] = r3
        if x+y < l+n-2 and x<l-1:
            A[value, coordinates[(x+1, y)]] = -r1
        if x<l-1 and y>0:
            A[value, coordinates[(x+1, y-1)]] = r2
        if y>0 and x+y>n-1:
            A[value, coordinates[(x, y-1)]] = -r3

    return A
    

if __name__ == '__main__':
    plot_matrix(matrix_generator, r_lim=3)