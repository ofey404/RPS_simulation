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

def RoPpSc(Y,t):
    n = Y.shape[0]
    F = np.zeros(n)
    F = np.matmul(A, Y)
    return F
    

if __name__ == '__main__':
    Y0 = np.array([0.01]*10)
    tspan, nt = [0, 500], 10001
    r1, r2, r3 = 1, 2, 1
    A = np.array([[0, -r3, r2, 0, 0, 0, 0, 0, 0, 0],
                  [r3, 0, -r1, -r3, r2, 0, 0, 0, 0, 0],
                  [-r2, r1, 0, 0, -r3, r2, 0, 0, 0, 0],
                  [0, r3, 0, 0, -r1, 0, -r3, r2, 0, 0],
                  [0, -r2, r3, r1, 0, -r1, 0, -r3, r2, 0],
                  [0, 0, -r2, 0, r1, 0, 0, 0, -r3, r2],
                  [0, 0, 0, r3, 0, 0, 0, -r1, 0, 0],
                  [0, 0, 0, -r2, r3, 0, r1, 0, -r1, 0],
                  [0, 0, 0, 0, -r2, r3, 0, r1, 0, -r1],
                  [0, 0, 0, 0, 0, -r2, 0, 0, r1, 0]])


    
    result = RK4(RoPpSc, Y0, tspan, nt)
    for i in range(nt)[::2000]:
        print('{}, t={}'.format(result[:, i], i))
    print(result.shape)
    plt.bar(np.arange(10), result[:,-1])
    plt.yscale('log')
    plt.show()
