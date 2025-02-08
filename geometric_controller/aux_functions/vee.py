import numpy as np

def vee(S):
    return np.array([-S[1, 2], S[0, 2], -S[0, 1]])
