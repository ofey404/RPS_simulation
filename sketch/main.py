import numpy as np
import matplotlib.pyplot as plt
from util import RK4, RoPpSc_robust_closure, dump_result, parse_argv
import sys


def addtail(x):
    return x - 0.3 + 0.5 * np.random.rand()


def main(argv):
    config, data_dir = parse_argv(argv)
    
    Y0 = np.array([config["Y0"]] * config["n"])
    tspan, nt = config["tspan"], config["nt"]
    r = np.array(config["r"])
    
    RoPpSc = RoPpSc_robust_closure(r)
    result = RK4(RoPpSc, Y0, tspan, nt)

    RoPpSc_addtail = RoPpSc_robust_closure(r, addtail=addtail)
    result_addtail = RK4(RoPpSc_addtail, Y0, tspan, nt)

    dump_result(result, path=data_dir, prefix="RPS")
    dump_result(result_addtail, path=data_dir, prefix="RPS-addtail")


if __name__ == "__main__":
    main(sys.argv)
