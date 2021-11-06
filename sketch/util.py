import json
import pathlib
import pickle
import numpy as np
import time
import matplotlib.pyplot as plt

def RK4(f, Y0, tspan, nt):
    tstart, tend = tspan[0], tspan[1]
    h = (tstart - tend) / (nt - 1)
    t = np.linspace(tstart, tend, nt)
    numvar = Y0.shape[0]
    Y = np.zeros((numvar, nt))
    Y.T[0] = Y0

    for i in range(nt - 1):
        yn = Y[:, i]
        k1 = f(yn, t[i])
        k2 = f(yn + k1 * h / 2, t[i] + h / 2)
        k3 = f(yn + k2 * h / 2, t[i] + h / 2)
        k4 = f(yn + k3 * h, t[i] + h)
        Y[:, i + 1] = yn + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return Y


def identical(x):
    return x

def RoPpSc_robust_closure(r, addtail=identical):
    def RoPpSc_robost(Y, t):
        n = Y.shape[0]
        f = np.zeros(n)
        f[0] = Y[0] * (addtail(r[2]) * Y[1] - addtail(r[0]) * Y[2])
        f[-1] = Y[-1] * (addtail(r[0]) * Y[-3] - addtail(r[1]) * Y[-2])
        for i in range(1, n - 1):
            if i % 2 == 0:
                f[i] = Y[i] * (
                    addtail(r[0]) * (Y[i - 2] - Y[i + 2])
                    - addtail(r[1]) * Y[i - 1]
                    + addtail(r[2]) * Y[i + 1]
                )
            else:
                f[i] = Y[i] * (addtail(r[1]) * Y[i + 1] - addtail(r[2]) * Y[i - 1])
        return f
    return RoPpSc_robost


def dump_result(matrix, path, prefix="RPS"):
    filename = "{}-{}.pkl".format(
        prefix, time.strftime("%Y-%m-%d-%H:%M:%S".format(prefix), time.localtime())
    )
    data = {"shape": matrix.shape, "result": matrix}
    with open(path / filename, "wb") as f:
        pickle.dump(data, f)


def parse_argv(argv):
    if len(argv) <= 1:
        print("Usage: python main.py ./data_path/config.json")
        exit(0)
    config_path = pathlib.Path(argv[1])
    data_dir = config_path.parent

    with open(config_path, "rt") as config_file:
        config = json.load(config_file)

    return config, data_dir

def get_data_files(data_dir):
    return list(data_dir.glob("RPS-*.pkl"))