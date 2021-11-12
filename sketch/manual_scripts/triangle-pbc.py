from pfapack import pfaffian as pf
import numpy as np
import matplotlib.pyplot as plt

def matrix_generator(l, w, R):
    coordinates = {}
    r1, r2, r3 = R
    
    layer, count = 0, 0
    for i in range(w):
        for j in range(l):
            coordinates[(j, layer)] = count
            count += 1
        layer += 1

    A = np.zeros((w*l, w*l))
    for pair in coordinates:
        x, y = pair
        value = coordinates[pair]

        A[value, coordinates[((x+1+l)%l, y)]] = -r1
        A[value, coordinates[((x-1+l)%l, y)]] = r1
        if y > 0:
            A[value, coordinates[(x, y-1)]] = -r3
            A[value, coordinates[((x+l+1)%l, y-1)]] = r2
        if y < w-1:
            A[value, coordinates[(x, y+1)]] = r3
            A[value, coordinates[((x-1+l)%l, y+1)]] = -r2
            

    return A

    

if __name__ == '__main__':
    x = []
    dets = []
    for r in np.arange(0, 3, 0.01):
        R = (1, r, 1)
        mat = matrix_generator(6, 4, R)
        det = pf.pfaffian(mat)
        x.append(r)
        dets.append(det)


    fig, ax = plt.subplots()

    ax.set_xlim(0, 1.0)
    ax.set_ylim(-500, 500)

    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.spines["left"].set_smart_bounds(True)
    ax.spines["bottom"].set_smart_bounds(True)
    ax.plot(x, dets)

    for x, y in zip(x, dets):
        print("({:.3}, {})".format(x, y))

    plt.show()




