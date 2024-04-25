import matplotlib.pyplot as plt
from .aux_functions.plot_3x1 import plot_3x1
import numpy as np
def plot_geometric_data(geometric_controller):
    env = geometric_controller
    # Plot data
    linetype, linewidth = 'k', 1
    xlabel_ = 'time (s)'


    # plt.figure()
    # plot_3x1(env.t, env.e['R'], '', xlabel_, 'e_R', linetype, linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.e['x'], '', xlabel_, 'e_x', linetype, linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.e['v'], '', xlabel_, 'e_v', linetype, linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.eI * np.array([env.k['I'], env.k['I'], env.k['yI']]).reshape((-1,1)), '', xlabel_, 'e', linetype, linewidth)
    # plt.plot(env.t, env.param['R_delta'] * np.ones((env.N, 3)), '', xlabel_, 'e_I', 'r', linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.ei * env.k['i'], '', xlabel_, 'e_i', linetype, linewidth)
    # plt.plot(env.t, env.param['x_delta'] * np.ones((env.N, 3)), '', xlabel_, 'e_i', 'r', linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.x, '', xlabel_, 'x', linetype, linewidth)
    # plot_3x1(env.t, env.d['x'], '', xlabel_, 'x', 'r', linewidth)

    # plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.plot3D(env.x[0, :500], env.x[1, :500], env.x[2, :500], 'k')
    # ax.plot3D(env.x[0, 500:550], env.x[1, 500:550], env.x[2, 500:550], 'g')
    # ax.plot3D(env.x[0, 550:], env.x[1, 550:], env.x[2, 550:], 'k')
    # ax.plot3D(env.d['x'][0], env.d['x'][1], env.d['x'][2], 'r', label='ref')
    # plt.legend()


    # plot 3d
    plt.figure("3D Trajectory")
    ax = plt.axes(projection='3d')
    # different colors
    active_controller_list = np.array(geometric_controller.active_controller_list)
    active_0 = active_controller_list == 0
    active_1 = active_controller_list == 1
    env.t = env.t[:env.counter]
    env.x = env.x[:, :env.counter]
    env.d['x'] = env.d['x'][:, :env.counter]

    ax.scatter3D(env.x[0, active_0], env.x[1, active_0], env.x[2, active_0], 'blue', label='UAV ctrl 0')
    ax.scatter3D(env.x[0, active_1], env.x[1, active_1], env.x[2, active_1], 'green', label='UAV ctrl 1')
    ax.plot3D(env.d['x'][0], env.d['x'][1], env.d['x'][2], 'r', label='ref')

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.legend()


    plt.figure("Active Controller")
    plt.title("Active Controller Vs. Time", fontsize=24)
    plt.plot(env.t, active_controller_list, label='active controller', c='blue', linewidth=2.5)
    plt.xlabel("Time (s)", fontsize=24)
    plt.ylabel("Active Controller (0/1)", fontsize=24)
    # plt.legend(loc='lower right', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)






    plt.show()
