import numpy as np
from scipy.integrate import solve_ivp

from .aux_functions.hat import hat


def attitude_control_decoupled_yaw(R, W, eI, b3d, b3d_dot, b3d_ddot, b1c, wc3, wc3_dot, k, param):
    # R = y[:9].reshape(3, 3)
    # W = y[9:12]
    # eI = y[12:]

    J = param['J']
    c2 = param['c2']
    c3 = param['c3']

    e1 = np.array([1, 0, 0])
    e2 = np.array([0, 1, 0])
    e3 = np.array([0, 0, 1])

    b1 = R @ e1
    b2 = R @ e2
    b3 = R @ e3

    kb = k['R']
    kw = k['W']

    w = W[0] * b1 + W[1] * b2
    b3_dot = hat(w) @ b3

    wd = hat(b3d) @ b3d_dot
    wd_dot = hat(b3d) @ b3d_ddot

    eb = hat(b3d) @ b3
    ew = w + hat(b3) @ hat(b3) @ wd
    tau = - kb * eb - kw * ew - J[0, 0] * np.dot(b3, wd) * b3_dot \
        - J[0, 0] * hat(b3) @ hat(b3) @ wd_dot - k['I'] * np.dot(eI[:2], [b1, b2])

    tau1 = np.dot(b1, tau)
    tau2 = np.dot(b2, tau)

    M1 = tau1 + J[2, 2] * W[2] * W[1]
    M2 = tau2 - J[2, 2] * W[2] * W[0]

    ey = -np.dot(b2, b1c)
    ewy = W[2] - wc3

    M3 = - k['y'] * ey - k['wy'] * ewy - k['yI'] * eI[2] + J[2, 2] * wc3_dot

    eI_dot = np.array([b1.T @ (c2 * eb + ew), b2.T @ ( c2 * eb + ew), c3 * ey + ewy])

    return (M1, M2, M3), eI_dot, eb, ew, ey, ewy

