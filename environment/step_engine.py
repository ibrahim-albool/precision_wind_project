import numpy as np

from .env_initializer import Initializer


class ControlEngine:
    def __init__(self, env, dynamics_randomization):
        self.env = env
        self.initializer = Initializer(env, dynamics_randomization)

    def processStep(self, action):
        env = self.env
        # print(action)
        action = np.clip(action, 0., 1.) > 0.5
        full_states, reward = self.step(action)

        # Early termination
        done = env.counter >= env.eps_length  # True

        # show the plots
        if done:
            self.plot_curves()


        return full_states, reward, done, {}



    # get the states of interest
    def get_basic_states(self):
        env = self.env

        states = np.array([
            env.xn,
            env.V_xn,
            env.u_x_n
        ], dtype=np.float32)

        states = np.clip(np.abs(states), 0., 5.0) / 5.

        return states.reshape(-1, 1)

    # augment the states
    # basic_states is an
    def get_full_states(self, basic_states=None):
        if basic_states is None:
            basic_states = [self.get_basic_states()]
        basic_states = np.concatenate(basic_states, axis=1)
        means = basic_states.mean(axis=1)
        maxs = basic_states.max(axis=1)
        mins = basic_states.min(axis=1)
        norms = np.linalg.norm(basic_states, ord=2, axis=1)
        states = np.concatenate([means, maxs, mins, norms])
        return states



    def reward(self):
        env = self.env
        squared_errors = np.array([env.u_controller_x ** 2,
                                   env.xn ** 2,
                                   env.V_xn ** 2])

        weights = np.array([0.05,
                            0.85,
                            0.1])

        reward = -np.sum(weights * squared_errors)

        return reward

    # controller_type True means pd, False means SMC
    def step(self, controller_type):
        env = self.env

        # controller_type = True

        rewards = []
        basic_states = []

        for i in range(env.N):
            u_controller_x = self.step_controller_x(env.xn, env.V_xn, 0., 0., controller_type)
            u_controller_y = self.step_pd_y(env.yn, env.V_yn, env.y_ref[env.counter], env.V_y_ref[env.counter])

            V_w = env.V_w_arr[env.counter]

            u_x = u_controller_x + V_w
            u_y = u_controller_y

            self.plant(u_x, u_y)

            env.u_controller_x = u_controller_x
            env.u_controller_y = u_controller_x
            env.u_x_n = u_x
            env.u_y_n = u_y

            env.counter += 1
            env.t += env.Ts


            env.x_arr.append(env.xn_1)
            env.V_x_arr.append(env.V_xn_1)
            env.y_arr.append(env.yn_1)
            env.V_y_arr.append(env.V_yn_1)

            env.u_x_arr.append(u_x)
            env.u_y_arr.append(u_y)
            env.controller_selection_arr.append(int(controller_type))

            rewards.append(self.reward())
            basic_states.append(self.get_basic_states())
            if env.counter >= env.eps_length:
                break

        reward = np.average(rewards)
        full_states = self.get_full_states(basic_states)
        return full_states, reward

    def step_controller_x(self, x, V_x, x_ref=0, V_x_ref=0., select_pd=True):
        if select_pd:
            return self.step_pd_x(x, V_x, x_ref, V_x_ref)
        else:
            return self.step_SMC_x(x, x_ref)


    def step_pd_x(self, x, V_x, x_ref=0, V_x_ref=0.):
        env = self.env

        Kpx = env.Kpx
        Kdx = env.Kdx

        u_x = Kpx * (x_ref - x) + Kdx * (V_x_ref - V_x)
        u_x = np.clip(u_x, -env.thersh_limit, env.thersh_limit)

        return u_x

    def step_pd_y(self, y, V_y, y_ref, V_y_ref):
        env = self.env

        Kpy = env.Kpy
        Kdy = env.Kdy

        u_y = Kpy * (y_ref - y) + Kdy * (V_y_ref - V_y)
        u_y = np.clip(u_y, -env.thersh_limit, env.thersh_limit)

        return u_y

    def step_SMC_x(self, x, x_ref=0.):
        env = self.env
        sigma = np.sign(x_ref-x + 1e-16)
        u_x = np.clip(sigma * env.thersh_limit, -env.thersh_limit, env.thersh_limit)

        return u_x

    # returns y, y_dot
    def plant(self, u_x, u_y):
        env = self.env
        Ts = env.Ts

        env.xn_1 = env.xn
        env.V_xn_1 = env.V_xn
        env.yn_1 = env.yn
        env.V_yn_1 = env.V_yn

        env.xn = env.xn_1 + Ts * env.V_xn_1 + 0.5 * Ts ** 2 * u_x
        env.V_xn = env.V_xn_1 + Ts * u_x
        env.yn = env.yn_1 + Ts * env.V_yn_1 + 0.5 * Ts ** 2 * u_y
        env.V_yn = env.V_yn_1 + Ts * u_y



    def plot_curves(self):
        env = self.env
        import matplotlib.pyplot as plt

        plt.figure('Boat States')

        plt.subplot(411)
        plt.title('Horizontal location')
        plt.plot(env.t_array, env.x_ref_arr, 'r--', label='x_ref')
        plt.plot(env.t_array, env.x_arr, 'b', label='x')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        plt.legend()
        plt.grid()

        plt.subplot(412)
        plt.title('Horizontal velocity')
        plt.plot(env.t_array, env.V_x_ref_arr, 'r--', label='V_x_ref')
        plt.plot(env.t_array, env.V_x_arr, 'b', label='V_x')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        plt.legend()
        plt.grid()

        plt.subplot(413)
        plt.title('Vertical location')
        plt.plot(env.t_array, env.y_ref_arr[:env.eps_length], 'r--', label='y_ref')
        plt.plot(env.t_array, env.y_arr, 'b', label='y')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        plt.legend()
        plt.grid()

        plt.subplot(414)
        plt.title('Vertical velocity')
        plt.plot(env.t_array, env.V_y_ref_arr[:env.eps_length], 'r--', label='V_y_ref')
        plt.plot(env.t_array, env.V_y_arr, 'b', label='V_y')
        plt.legend()
        plt.grid()

        plt.figure('Control Signals')

        plt.subplot(411)
        plt.title('u_x')
        plt.plot(env.t_array, env.u_x_arr, 'b', label='x')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        plt.legend()
        plt.grid()

        plt.subplot(412)
        plt.title('V_w')
        plt.plot(env.t_array, env.V_w_arr, 'b', label='x')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        plt.legend()
        plt.grid()

        plt.subplot(413)
        plt.title('u_y')
        plt.plot(env.t_array, env.u_y_arr, 'b', label='x')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        plt.legend()
        plt.grid()

        plt.subplot(414)
        plt.title('controller selection (0=SMC, 1=pd)')
        plt.plot(env.t_array, env.controller_selection_arr, 'b', label='c selection')
        plt.legend()
        plt.grid()


        # -------------------
        plt.figure('2-d location')

        plt.title('2-d location')
        plt.plot(env.x_ref_arr, env.y_ref_arr[:env.eps_length], 'r--', label='x_ref')
        plt.plot(env.x_arr, env.y_arr, 'b', label='x')
        plt.grid()


        plt.show()
