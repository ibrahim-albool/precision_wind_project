import numpy as np

def command_line(t):
    height = 1

    desired = {}

    desired['x'] = np.array([0.5 * t, 0, -height])
    desired['v'] = np.array([0.5 * 1, 0, 0])
    desired['x_2dot'] = np.array([0, 0, 0])
    desired['x_3dot'] = np.array([0, 0, 0])
    desired['x_4dot'] = np.array([0, 0, 0])

    w = 2 * np.pi / 10
    desired['b1'] = np.array([np.cos(w * t), np.sin(w * t), 0])
    desired['b1_dot'] = w * np.array([-np.sin(w * t), np.cos(w * t), 0])
    desired['b1_2dot'] = w**2 * np.array([-np.cos(w * t), -np.sin(w * t), 0])

    return desired
