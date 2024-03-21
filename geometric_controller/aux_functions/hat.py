import numpy as np

def hat(x):
    """
    Skew-symmetric matrix (hat operator) for a 3x1 vector x.
    """
    return np.array([[0, -x[2], x[1]],
                     [x[2], 0, -x[0]],
                     [-x[1], x[0], 0]])
