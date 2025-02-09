import numpy as np
# Define the eom function
from ..aux_functions.hat import hat
from ..aux_functions.split_to_states import split_to_states
from ..position_control import position_control
# from geometric_controller.test_functions.command import command


def eom(env, t, X, desired, k, param):
    e3 = np.array([0, 0, 1])
    impact_force = np.array([0., 0., 0.])

    m = param['m']
    J = param['J']

    x, v, W, R, _, _ = split_to_states(X)

    # if t>= 6.30:
    #     print("here")

    pos_ctrl_tuple = position_control(X, desired, k, param)
    f, M, ei_dot, eI_dot, _, _ = pos_ctrl_tuple

    # f, M, ei_dot, eI_dot, _, _ = 0, (0,0,0),(0,0,0), (0,0,0) , 0, 0

    # adding some noises and disturbances to the dynamics
    # # random noise
    # f += np.random.rand()*20-10
    # Mnoise1 = np.random.rand()*3-1.5
    # Mnoise2 = np.random.rand()*3-1.5
    # Mnoise3 = np.random.rand()*1-0.5
    # M = (M[0]+Mnoise1, M[1]+Mnoise2, M[2]+Mnoise3)

    # # impulse noise between second 5 and 5.4 ( in the direction of motor thrust)
    # if 5.4>=t>=5.0:
    #     f += 15

    # Adding impulse force between second 5 and 5.4 ( in the x direction)

    if env.impact_force_start_time <= t <= env.impact_force_start_time + env.impact_force_duration:
        # impact_force[0] = 15.
        impact_force = env.impact_force

    # impact_force = env.impact_force * np.sin(t * 2 * np.pi/2.) * 2.

    # impact_force = np.array([1,0,0]) * np.sign(np.sin(t * 2 * np.pi/1.)) * 4.

    # impact_force = env.impact_force * np.sign(np.sin(t * 2 * np.pi/2.)) * 2.

    # impact_force = np.array([1,0,0]) * np.sign(np.sin(t * 2 * np.pi/3.)) * 2.

    # impact_force = env.impact_force * 2

    # f = 18.62

    # M = (0,0,0)

    # print(f"v: {v}")

    xdot = v
    vdot = param['g'] * e3 - f / m * R @ e3 + param['x_delta'] / m + impact_force / m
    Wdot = np.linalg.solve(J, (-hat(W) @ J @ W + M + param['R_delta']))
    Rdot = R @ hat(W)

    Xdot = np.concatenate([xdot, vdot, Wdot, Rdot.flatten(), ei_dot, eI_dot])

    return Xdot, pos_ctrl_tuple