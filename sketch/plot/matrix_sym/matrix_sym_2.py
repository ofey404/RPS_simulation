from mpmath.functions.functions import im
import sympy
import time
import pathlib
import pickle

def matrix_generator_sym(n, R):
    coordinates = {}
    head = 0
    r1, r2, r3 = R
    for i in range(n):
        head += i
        for j in range(head, head+i+1):
            coordinates[(i-j+head, j-head)] = j

    # A = np.zeros((n*(n+1)//2, n*(n+1)//2))
    A = [[0 for _ in range(n*(n+1)//2)] for _ in range(n*(n+1)//2)]

    for pair in coordinates:
        x, y = pair
        value = coordinates[pair]
        
        if x > 0:
            A[value][coordinates[(x-1, y)]] = r1
            A[value][coordinates[(x-1, y+1)]] = -r2
        if y > 0:
            A[value][coordinates[(x, y-1)]] = -r3
            A[value][coordinates[(x+1, y-1)]] = r2
        if x+y < n-1:
            A[value][coordinates[(x, y+1)]] = r3
            A[value][coordinates[(x+1, y)]] = -r1

    return sympy.Matrix(A)

def play():
    r = sympy.symbols('r')
    print(r** 2 + 1)
    mat = sympy.Matrix([[1, r], [r**2, -1]])
    print(mat)
    e = mat.eigenvals()
    print(e)


def main():
    r = sympy.symbols('r')
    R = (1, 1, r)
    mat = matrix_generator_sym(4, R)
    # print(mat)
    # print(len(mat))
    # print(len(mat[0]))
    eigens = mat.eigenvals()
    print(eigens)
    filename = "matrix-eigens-4.pkl"
    data = {"eigens": eigens}
    path = pathlib.Path('.')
    with open(path / filename, "wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    main()