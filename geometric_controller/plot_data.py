import matplotlib.pyplot as plt
from geometric_controller.aux_functions.plot_3x1 import plot_3x1
import numpy as np
def plot_geometric_data(geometric_controller):
    env = geometric_controller
    # Plot data
    linetype, linewidth = 'k', 1
    xlabel_ = 'time (s)'


    plt.figure()
    plot_3x1(env.t, env.e['R'], '', xlabel_, 'e_R', linetype, linewidth)

    plt.figure()
    plot_3x1(env.t, env.e['x'], '', xlabel_, 'e_x', linetype, linewidth)

    plt.figure()
    plot_3x1(env.t, env.e['v'], '', xlabel_, 'e_v', linetype, linewidth)

    plt.figure()
    plot_3x1(env.t, env.eI * np.array([env.k['I'], env.k['I'], env.k['yI']]).reshape((-1,1)), '', xlabel_, 'e', linetype, linewidth)
    plt.plot(env.t, env.param['R_delta'] * np.ones((env.N, 3)), '', xlabel_, 'e_I', 'r', linewidth)

    plt.figure()
    plot_3x1(env.t, env.ei * env.k['i'], '', xlabel_, 'e_i', linetype, linewidth)
    plt.plot(env.t, env.param['x_delta'] * np.ones((env.N, 3)), '', xlabel_, 'e_i', 'r', linewidth)

    plt.figure()
    plot_3x1(env.t, env.x, '', xlabel_, 'x', linetype, linewidth)
    plot_3x1(env.t, env.d['x'], '', xlabel_, 'x', 'r', linewidth)

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(env.x[0, :500], env.x[1, :500], env.x[2, :500], 'k')
    ax.plot3D(env.x[0, 500:550], env.x[1, 500:550], env.x[2, 500:550], 'g')
    ax.plot3D(env.x[0, 550:], env.x[1, 550:], env.x[2, 550:], 'k')
    ax.plot3D(env.d['x'][0], env.d['x'][1], env.d['x'][2], 'r', label='ref')
    plt.legend()


    plt.show()
