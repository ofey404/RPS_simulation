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

def coordinate(n):
    coordinates = {}
    head = 0
    for i in range(n):
        head += i
        for j in range(head, head+i+1):
            coordinates[(i-j+head, j-head)] = j
    return coordinates

def matrix_generator(n, R):
    r1, r2, r3 = R
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

def RoPpSc(Y,t):
    n = Y.shape[0]
    F = np.zeros(n)
    F = Y * np.matmul(A, Y)
    return F

def colormesh(Y, n, pathname):
    data = np.zeros((n, n))
    for pair in coordinates:
        data[pair] = Y[coordinates[pair]]

    fig, ax = plt.subplots()
    ax.pcolormesh(data)
    plt.savefig(pathname)
    plt.close()
    

if __name__ == '__main__':
    Y0 = np.array([0.1]+[0.01]*20+[0.1]+[0.01]*5+[0.1])
    tspan, nt = [0, 1000], 10001

    coordinates = coordinate(7)
    R = (1,2,1.5)
    A = matrix_generator(7, R)
    
    result = RK4(RoPpSc, Y0, tspan, nt)
    for i in range(nt)[::1000]:
        pathname = './RPS={}.png'.format(i)
        colormesh(result[:,i], 7, pathname)
       
    
