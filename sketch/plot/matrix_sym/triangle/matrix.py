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

        
