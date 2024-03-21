import numpy as np

def satdot(sigma, y, ydot):
    z_dot = np.zeros_like(ydot)

    for k in range(len(y)):
        if y[k] > sigma or y[k] < -sigma:
            z_dot[k] = 0
        else:
            z_dot[k] = ydot[k]

    return z_dot
