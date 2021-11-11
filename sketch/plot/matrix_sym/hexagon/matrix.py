import matplotlib.pyplot as plt
import numpy as np

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
    r_lim = 3
    all_eigens = []
    for r in np.arange(0, r_lim, 0.1):
        R = (1, 1, r)
        mat = matrix_generator(7, R)
        # 求本征值
        eigens = np.linalg.eigvals((0+1j)*mat)
        reals, imags = [], []
        for eigen in eigens:
            reals.append(eigen.real)
            imags.append(eigen.imag)

        plt.scatter(reals, imags)
        plt.xlabel("real")
        plt.ylabel("imag")
        # plt.show()
        plt.savefig("./{:.2}.png".format(r))
        plt.close()

        all_eigens.append(eigens)

    xs = []
    ys = []
    for i, eigens in zip(np.arange(0, r_lim, 0.1), all_eigens):
        for e in eigens:
            xs.append(i)
            ys.append(e.real)

    plt.scatter(xs, ys)
    plt.xlabel("r")
    plt.ylabel("real")
    plt.savefig("./summary.png".format(r))
    # plt.show()
    plt.close()
            
            


