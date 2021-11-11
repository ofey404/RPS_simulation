import numpy as np
import matplotlib.pyplot as plt

def plot_matrix(matrix_generator, r_lim):
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

        plt.scatter(reals, imags, marker="x", color="green")
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