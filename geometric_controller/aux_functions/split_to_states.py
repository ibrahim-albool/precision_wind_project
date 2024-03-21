import numpy as np

def split_to_states(X):
    x = X[0:3]
    v = X[3:6]
    W = X[6:9]
    R = X[9:18].reshape((3, 3))
    ei = X[18:21]
    eI = X[21:]

    return x, v, W, R, ei, eI
