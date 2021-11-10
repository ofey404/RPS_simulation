import numpy as np
import matplotlib.pyplot as plt

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
    r = 1
    R = (1, 1, r)
    mat = matrix_generator(7, R)
    # 求本征值
    eigens = np.linalg.eigvals((0+1j)*mat)
    reals, imags = [], []
    for eigen in eigens:
        reals.append(eigen.real)
        imags.append(eigen.imag)

    plt.scatter(reals, imags)
    plt.show()
    

            
            







