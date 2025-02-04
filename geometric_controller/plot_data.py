import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.proj3d import proj_transform
matplotlib.use('TkAgg')
from .aux_functions.plot_3x1 import plot_3x1
import numpy as np


class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)


def generate_impact_forces_arrows(t, x, d, dt, t_impact, duration, impact_force):
    arrow_length = 0.5
    dx, dy, dz = np.clip(impact_force, -arrow_length, arrow_length)
    calc_num_of_arrows = lambda x: int(np.round((np.tanh(x * 2.0 - 2) + 1) * 2 + 4))
    def time_instants_to_indices(t, time_instants):
        current_index = 0
        indices = []
        for time_instant in time_instants:
            if current_index >= len(t):
                return indices
            while abs(t[current_index]-time_instant) >= dt/2.:
                current_index += 1
                if current_index >= len(t):
                    return indices
            indices.append(current_index)
        return indices

    # number_of_arrows = 10
    number_of_arrows = calc_num_of_arrows(duration)
    step = duration / (number_of_arrows - 1)
    forces_time_instants = np.arange(t_impact, t_impact + duration + 0.001, step)
    indices = time_instants_to_indices(t, forces_time_instants)

    # verifying that estimated and real time samples match
    # print(f"instants={forces_time_instants}")
    # print(f"   times={[t[i] for i in indices]}")

    arrows = [Arrow3D(x[0, i] - dx, x[1, i] - dy, x[2, i] - dz, dx, dy, dz, mutation_scale=20,
                      lw=1.5, arrowstyle="-|>", color="orange") for i in indices]

    return arrows


def plot_geometric_data(geometric_controller):
    env = geometric_controller
    # Plot data
    linetype, linewidth = 'k', 1
    xlabel_ = 'Time (s)'


    # plt.figure()
    # plot_3x1(env.t, env.e['R'], 'e_R', xlabel_, 'e_R', linetype, linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.e['x'], 'e_x', xlabel_, 'e_x', linetype, linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.e['v'], 'e_v', xlabel_, 'e_v', linetype, linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.eI * np.array([env.k['I'], env.k['I'], env.k['yI']]).reshape((-1,1)), 'e_I', xlabel_, 'e', linetype, linewidth)
    # plt.plot(env.t, env.param['R_delta'] * np.ones((env.N, 3)), '', xlabel_, 'e_I', 'r', linewidth)
    #
    # plt.figure()
    # plot_3x1(env.t, env.ei * env.k['i'], 'x_delta', xlabel_, 'e_i', linetype, linewidth)
    # plt.plot(env.t, env.param['x_delta'] * np.ones((env.N, 3)), '', xlabel_, 'e_i', 'r', linewidth)

    # plt.figure()
    y_signals = [env.d['x'], env.x, env.e['x']]
    norms = [np.linalg.norm(s, axis=0) for s in y_signals]

    plot_3x1(x=env.t, y_signals=y_signals, norms=norms, switching=geometric_controller.active_controller_list, title_='Trajectory Tracking', xlabel_=xlabel_, ylabels=['x-axis position (m)', 'y-axis position (m)', 'z-axis position (m)'], linetypes=["-", "--", "-."], linewidth=2)
    # plot_3x1(x=env.t, y=env.d['x'], title_='desired_x', xlabel_=xlabel_, ylabel_='x', linetype='green', linewidth=2)
    # plot_3x1(x=env.t, y=env.e['x'], title_='e_x', xlabel_=xlabel_, ylabel_='e_x', linetype='purple', linewidth=2)
    plt.show()

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

    ax.scatter3D(env.x[0, active_0], env.x[1, active_0], env.x[2, active_0], s=5, c='blue', label='UAV ctrl 0')
    ax.scatter3D(env.x[0, active_1], env.x[1, active_1], env.x[2, active_1], s=5, c='red', label='UAV ctrl 1')
    ax.plot3D(env.d['x'][0], env.d['x'][1], env.d['x'][2], 'green', label='ref')

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.legend()

    arrows = generate_impact_forces_arrows(env.t, env.x, env.d, env.dt, env.impact_force_start_time, env.impact_force_duration, env.impact_force)
    for arrow in arrows:
        ax.add_artist(arrow)


    plt.figure("Active Controller")
    plt.title("Active Controller Vs. Time", fontsize=24)
    plt.plot(env.t, active_controller_list, label='active controller', c='blue', linewidth=2.5)
    plt.xlabel("Time (s)", fontsize=24)
    plt.ylabel("Active Controller (0/1)", fontsize=24)
    # plt.legend(loc='lower right', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)






    plt.show()
