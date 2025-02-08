import numpy as np

def sat(sigma, y):
    z = np.zeros_like(y)

    for k in range(len(y)):
        if y[k] > sigma:
            z[k] = sigma
        elif y[k] < -sigma:
            z[k] = -sigma
        else:
            z[k] = y[k]

    return z
