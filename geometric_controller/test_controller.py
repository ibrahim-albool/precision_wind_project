import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp

# Test controller script
from geometric_controller.aux_functions.generate_output_arrays import generate_output_arrays
from geometric_controller.aux_functions.plot_3x1 import plot_3x1
from geometric_controller.position_control import position_control
from geometric_controller.test_functions.command import command
from geometric_controller.test_functions.eom import eom


def test_controller():
    # Simulation parameters
    dt = 0.01
    t_span = (0, 10.0 + dt)
    t = np.arange(t_span[0], t_span[1], dt)
    N = len(t)

    # Quadrotor parameters
    J1, J2, J3 = 0.02, 0.02, 0.04
    param = {}
    k = {}
    param['J'] = np.diag([J1, J2, J3])
    param['m'] = 2
    param['d'] = 0.169
    param['ctf'] = 0.0135
    param['x_delta'] = np.array([0.5, 0.8, -1])
    param['R_delta'] = np.array([0.2, 1.0, -0.1])
    param['g'] = 9.81

    # Controller gains
    k['x'], k['v'], k['i'] = 10, 8, 10
    param['c1'], param['sigma'] = 1.5, 10
    k['R'], k['W'], k['I'] = 1.5, 0.35, 10
    param['c2'] = 2
    k['y'], k['wy'], k['yI'] = 0.8, 0.15, 2
    param['c3'] = 2

    # Initial conditions
    x0, v0, R0, W0 = np.zeros(3), np.zeros(3), np.eye(3), np.zeros(3)
    # x0 = np.array([0,0, 0])
    X0 = np.concatenate([x0, v0, W0, R0.flatten(), np.zeros(6)])

    # Continuous Numerical integration Solver
    solver_result = solve_ivp(eom, t_span, X0, args=(k, param), t_eval=t, rtol=1e-6, atol=1e-6)
    X = solver_result.y.T

    # Discrete Integration
    # The discrete integration is more applicable in our case because we can have access to the states at each time step
    # which is not the case with solve_ipv; it does the calculations and returns the results when it is done
    # X_accum = X0
    # X = np.zeros((N,X0.shape[0]))
    # for i in range(N):
    #     Xdot = eom(t[i], X_accum, k, param)
    #     X[i] = X_accum
    #     X_accum += Xdot*dt
    #     # if 5.5>=t[i]>=5.0:
    #     #     k['x'], k['v'], k['i'] = 30, 20, 30
    #     #     k['R'], k['W'], k['I'] = 4., 0.90, 25
    #     #     k['y'], k['wy'], k['yI'] = 2.5, 0.7, 6
    #     # # print(t[i])
    #     # else:
    #     #     k['x'], k['v'], k['i'] = 10, 8, 10
    #     #     k['R'], k['W'], k['I'] = 1.5, 0.35, 10
    #     #     k['y'], k['wy'], k['yI'] = 0.8, 0.15, 2


    print("# Post-processing")
    # Post-processing
    e, d, R, f, M = generate_output_arrays(N)

    x, v, W, ei, eI = X[:, :3].T, X[:, 3:6].T, X[:, 6:9].T, X[:, 18:21].T, X[:, 21:24].T

    for i in range(N):
        R[:, :, i] = X[i, 9:18].reshape(3, 3)
        des = command(t[i])
        f[:, i], M[:, i], _, _, err, calc = position_control(X[i, :], des, k, param)
        e['x'][:, i], e['v'][:, i], e['R'][:, i], e['W'][:, i], e['y'][:, i], e['Wy'][:, i] = err['x'], err['v'], err[
            'R'], err['W'], err['y'], err['Wy']
        d['x'][:, i], d['v'][:, i], d['b1'][:, i], d['R'][:, :, i] = des['x'], des['v'], des['b1'], calc['R']

    # Plot data
    linetype, linewidth = 'k', 1
    xlabel_ = 'time (s)'

    t = np.arange(0,10.01,0.01)

    plt.figure()
    plot_3x1(t, e['R'], '', xlabel_, 'e_R', linetype, linewidth)
    # plt.gca().set_fontname('Times New Roman')

    plt.figure()
    plot_3x1(t, e['x'], '', xlabel_, 'e_x', linetype, linewidth)
    # plt.gca().set_fontname('Times New Roman')

    plt.figure()
    plot_3x1(t, e['v'], '', xlabel_, 'e_v', linetype, linewidth)
    # plt.gca().set_fontname('Times New Roman')

    plt.figure()
    plot_3x1(t, eI * np.array([k['I'], k['I'], k['yI']]).reshape((-1,1)), '', xlabel_, 'e', linetype, linewidth)
    plt.plot(t, param['R_delta'] * np.ones((N, 3)), '', xlabel_, 'e_I', 'r', linewidth)
    # plt.gca().set_fontname('Times New Roman')

    plt.figure()
    plot_3x1(t, ei * k['i'], '', xlabel_, 'e_i', linetype, linewidth)
    plt.plot(t, param['x_delta'] * np.ones((N, 3)), '', xlabel_, 'e_i', 'r', linewidth)
    # plt.gca().set_fontname('Times New Roman')

    plt.figure()
    plot_3x1(t, x, '', xlabel_, 'x', linetype, linewidth)
    plot_3x1(t, d['x'], '', xlabel_, 'x', 'r', linewidth)
    # plt.gca().set_fontname('Times New Roman')

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(x[0, :500], x[1, :500], x[2, :500], 'k')
    ax.plot3D(x[0, 500:550], x[1, 500:550], x[2, 500:550], 'g')
    ax.plot3D(x[0, 550:], x[1, 550:], x[2, 550:], 'k')
    ax.plot3D(d['x'][0], d['x'][1], d['x'][2], 'r', label='ref')
    plt.legend()
    # ax.set_xlabel('$x_1$', interpreter='latex')
    # ax.set_ylabel('$x_2$', interpreter='latex')
    # ax.set_zlabel('$x_3$', interpreter='latex')
    # ax.set_boxon(True)
    # ax.grid(True)
    # ax.set_fontname('Times New Roman')

    plt.show()

if __name__ == "__main__":
    # Run the test controller
    test_controller()
