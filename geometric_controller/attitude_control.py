import numpy as np
from scipy.integrate import solve_ivp

from geometric_controller.aux_functions.hat import hat
from geometric_controller.aux_functions.vee import vee


def attitude_control(R, W, eI, Rd, Wd, Wd_dot, k, param):

    eR = 1 / 2 * vee(Rd.T @ R - R.T @ Rd)
    eW = W - R.T @ Rd @ Wd

    kR = np.diag([k['R'], k['R'], k['y']])
    kW = np.diag([k['W'], k['W'], k['wy']])

    M = - kR @ eR \
        - kW @ eW \
        - k['I'] * eI \
        + hat(R.T @ Rd @ Wd) @ param['J'] @ R.T @ Rd @ Wd \
        + param['J'] @ R.T @ Rd @ Wd_dot

    eI_dot = eW + param['c2'] * eR

    return M, eI_dot, eR, eW
