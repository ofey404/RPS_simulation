import math
import numpy as np

def matrix_generator(n):
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
            A[value, coordinates[(x-1, y)]] = 1
        if x > 0 and y< l-1:
            A[value, coordinates[(x-1, y+1)]] = -2
        if y<l-1 and x+y<l+n-2:
            A[value, coordinates[(x, y+1)]] = 3
        if x+y < l+n-2 and x<l-1:
            A[value, coordinates[(x+1, y)]] = -1
        if x<l-1 and y>0:
            A[value, coordinates[(x+1, y-1)]] = 2
        if y>0 and x+y>n-1:
            A[value, coordinates[(x, y-1)]] = -3

    return A

    

if __name__ == '__main__':
    print(matrix_generator(3))
            
            


