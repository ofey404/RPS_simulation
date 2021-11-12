import numpy as np
import matplotlib.pyplot as plt
import pickle

result = None
with open("./RPS_wavepackage_gif.pkl", "rb") as f:
    result = pickle.load(f)["result"]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

tspan, nt = [0, 1500], 15001

for i in range(nt)[6000:11000:1000]:
    xs = np.arange(81)
    ys = result[:, i]
    zs = i

    ax.plot(xs, ys, zs, zdir="y")
    ax.set_xlabel("n")
    ax.set_xlim(0, 50)
    ax.set_ylabel("time")
    # ax.set_zlabel("count")

plt.show()