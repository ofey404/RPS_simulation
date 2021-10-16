import numpy as np
import matplotlib.pyplot as plt

def RK4(f, Y0, tspan, nt):
    tstart, tend = tspan[0], tspan[1]
    h = (tstart-tend)/(nt-1)
    t = np.linspace(tstart, tend, nt)
    numvar = Y0.shape[0]
    Y = np.zeros((numvar, nt))
    Y.T[0] = Y0

    for i in range(nt-1):
        yn = Y[:,i]
        k1 = f(yn, t[i])
        k2 = f(yn+k1*h/2, t[i]+h/2)
        k3 = f(yn+k2*h/2, t[i]+h/2)
        k4 = f(yn+k3*h, t[i]+h)
        Y[:,i+1] = yn + h/6*(k1+2*k2+2*k3+k4)
    return Y

def RoPpSc(Y, t):
    n = Y.shape[0]
    f = np.zeros(n)
    f[0] = Y[0]*(r[2]*Y[1] - r[0]*Y[2])
    f[-1] = Y[-1]*(r[0]*Y[-3] - r[1]*Y[-2])
    for i in range(1, n-1):
        if i%2 == 0:
            f[i] = Y[i]*(r[0]*(Y[i-2]-Y[i+2]) - r[1]*Y[i-1] + r[2]*Y[i+1])
        else:
            f[i] = Y[i]*(r[1]*Y[i+1] - r[2]*Y[i-1])
    return f

if __name__ == '__main__':
    Y0 = np.array([0.01, 0.05, 0.005, 0.1, 0.005, 0.05]+[0.01]*55)
    tspan, nt = [0, 200], 5000
    r = np.array([1, 1, 1])
    result = RK4(RoPpSc, Y0, tspan, nt)
    plt.bar(np.arange(61), result[:,-1])
    plt.yscale('log')
    plt.show()
