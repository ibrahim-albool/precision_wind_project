import numpy as np

def generate_output_arrays(N):
    error = {
        'x': np.zeros((3, N)),
        'v': np.zeros((3, N)),
        'R': np.zeros((3, N)),
        'W': np.zeros((3, N)),
        'y': np.zeros((1, N)),
        'Wy': np.zeros((1, N)),
    }

    desired = {
        'x': np.zeros((3, N)),
        'v': np.zeros((3, N)),
        'b1': np.zeros((3, N)),
        'R': np.zeros((3, 3, N)),
    }

    R = np.zeros((3, 3, N))
    f = np.zeros((1, N))
    M = np.zeros((3, N))

    return error, desired, R, f, M
