import numpy as np
from scipy.integrate import solve_ivp

from geometric_controller.attitude_control import attitude_control
from geometric_controller.attitude_control_decoupled_yaw import attitude_control_decoupled_yaw
from geometric_controller.aux_functions.deriv_unit_vector import deriv_unit_vector
from geometric_controller.aux_functions.hat import hat
from geometric_controller.aux_functions.sat import sat
from geometric_controller.aux_functions.satdot import satdot
from geometric_controller.aux_functions.split_to_states import split_to_states
from geometric_controller.aux_functions.vee import vee


def position_control(X, desired, k, param):
    use_decouple = True

    x, v, W, R, ei, eI = split_to_states(X)

    sigma = param['sigma']
    c1 = param['c1']
    m = param['m']
    g = param['g']
    e3 = np.array([0, 0, 1])
    
    error = {}
    calculated = {}

    error['x'] = x - desired['x']
    error['v'] = v - desired['v']
    A = -k['x'] * error['x'] - k['v'] * error['v'] - m * g * e3 + m * desired['x_2dot'] - k['i'] * sat(sigma, ei)

    ei_dot = error['v'] + c1 * error['x']
    b3 = R @ e3
    f = -np.dot(A, b3)
    ea = g * e3 - f / m * b3 - desired['x_2dot'] + param['x_delta'] / m
    A_dot = -k['x'] * error['v'] - k['v'] * ea + m * desired['x_3dot'] - k['i'] * satdot(sigma, ei, ei_dot)

    ei_ddot = ea + c1 * error['v']
    b3_dot = R @ hat(W) @ e3
    f_dot = -np.dot(A_dot, b3) - np.dot(A, b3_dot)
    eb = -f_dot / m * b3 - f / m * b3_dot - desired['x_3dot']
    A_ddot = -k['x'] * ea - k['v'] * eb + m * desired['x_4dot'] - k['i'] * satdot(sigma, ei, ei_ddot)

    b3c, b3c_dot, b3c_ddot = deriv_unit_vector(-A, -A_dot, -A_ddot)
    A2 = -hat(desired['b1']) @ b3c
    A2_dot = -hat(desired['b1_dot']) @ b3c - hat(desired['b1']) @ b3c_dot
    A2_ddot = -hat(desired['b1_2dot']) @ b3c - 2 * hat(desired['b1_dot']) @ b3c_dot - hat(desired['b1']) @ b3c_ddot

    b2c, b2c_dot, b2c_ddot = deriv_unit_vector(A2, A2_dot, A2_ddot)
    b1c = hat(b2c) @ b3c
    b1c_dot = hat(b2c_dot) @ b3c + hat(b2c) @ b3c_dot
    b1c_ddot = hat(b2c_ddot) @ b3c + 2 * hat(b2c_dot) @ b3c_dot + hat(b2c) @ b3c_ddot

    Rc = np.column_stack((b1c, b2c, b3c))
    Rc_dot = np.column_stack((b1c_dot, b2c_dot, b3c_dot))
    Rc_ddot = np.column_stack((b1c_ddot, b2c_ddot, b3c_ddot))

    Wc = vee(Rc.T @ Rc_dot)
    Wc_dot = vee(Rc.T @ Rc_ddot - hat(Wc) @ hat(Wc))

    W3 = np.dot(R @ e3, Rc @ Wc)
    W3_dot = np.dot(R @ e3, Rc @ Wc_dot) + np.dot(R @ hat(W) @ e3, Rc @ Wc_dot)

    # Run attitude controller
    if use_decouple:
        M, eI_dot, error['b'], error['W'], error['y'], error['Wy'] = attitude_control_decoupled_yaw(
            R, W, eI, b3c, b3c_dot, b3c_ddot, b1c, W3, W3_dot, k, param)
        error['R'] = 1 / 2 * vee(Rc.T @ R - R.T @ Rc)
    else:
        M, eI_dot, error['b'], error['W'] = attitude_control(
            R, W, eI, Rc, Wc, Wc_dot, k, param)
        error['y'] = 0
        error['Wy'] = 0

    # Only used for comparison between two controllers


    # Saving data
    calculated['b3'] = b3c
    calculated['b3_dot'] = b3c_dot
    calculated['b3_ddot'] = b3c_ddot
    calculated['b1'] = b1c
    calculated['R'] = Rc
    calculated['W'] = Wc
    calculated['W_dot'] = Wc_dot
    calculated['W3'] = np.dot(np.dot(R, e3), np.dot(Rc, Wc))
    calculated['W3_dot'] = np.dot(R @ e3, Rc @ Wc_dot) + np.dot(R @ hat(W), Rc @ Wc_dot)

    return f, M, ei_dot, eI_dot, error, calculated
