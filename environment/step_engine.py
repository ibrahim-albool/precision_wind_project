import numpy as np

from .env_initializer import Initializer


class ControlEngine:
    def __init__(self, env, dynamics_randomization):
        self.env = env
        self.initializer = Initializer(env, dynamics_randomization)

    def processStep(self, action):
        env = self.env

        action = np.clip(action, 0., 1.)
        action = self.fill_in_gains(action)
        self.step(action)

        # Early termination
        done = np.abs(env.error) > 100. or \
               env.counter > 10000  # True

        # show the plots
        if done:
            self.plot_curves()

        reward = self.reward()

        return self.get_full_state(), reward, done, {}

    def get_full_state(self):
        env = self.env

        states = np.array([
            env.r,
            env.r_dot,
            env.error,
            env.error_dot,
            env.y,
            env.y_dot,
            env.u
        ])
        gain = np.array([0.005,
                         0.00005,
                         0.005,
                         0.00005,
                         0.005,
                         0.00005,
                         0.001])
        offset = np.array([0.5,
                           0.5,
                           0.5,
                           0.5,
                           0.5,
                           0.5,
                           0.5])
        clip_max = np.array([100.,
                             10000.,
                             100.,
                             10000.,
                             100.,
                             10000.,
                             500.])
        clip_min = np.array([-100.,
                             -10000.,
                             -100.,
                             -10000.,
                             -100.,
                             -10000.,
                             -500.])
        states = np.clip(states, clip_min, clip_max)
        states = states * gain + offset

        return states

    # the NN runs at 250 Hz. whereas the controller runs at 1kHz.
    def step(self, gains):
        env = self.env
        for _ in range(4):
            env.r = self.gen_ref()
            env.r_dot = self.gen_ref_dot()
            env.error = env.r - env.yps_1
            env.error_dot = env.r_dot - env.ypf_1
            env.u = self.step_PID(env.error, gains)
            env.y, env.y_dot = self.plant(env.u)
            env.counter += 1
        env.y_res.append(env.y)
        env.y_dot_res.append(env.y_dot)
        env.u_res.append(env.u)
        env.r_res.append(env.r)
        env.r_dot_res.append(env.r_dot)

    def fill_in_gains(self, actions):
        gain = np.array([200.,
                         200.,
                         200.,
                         1000.])
        offset = np.array([-100.,
                           -100.,
                           -100.,
                           -500.])
        actions = actions * gain + offset
        return actions

    def step_PID(self, error, params):
        env = self.env
        P, I, D, N = params
        Ts = 1e-3
        # reward of the predefined gains = 2435.26
        # P = -1.99976633687983
        # I = -0.62802624974027
        # D = -0.393281303487897
        # N = 44.6971267850786

        Ic = I * Ts * env.error_1 + env.Ic_1
        env.Ic_1 = Ic

        Dc = D * N * error - D * N * env.error_1 + (1 - N * Ts) * env.Dc_1

        u = P * error + Ic + Dc

        env.error_1 = error
        env.Dc_1 = Dc

        return u

    # returns y, y_dot
    def plant(self, upf):
        env = self.env
        Ts = 1e-3

        # The first and second plant are the decomposition of an original plant into a plant and an integrator.
        # This was done to easily extract the derivative.

        # y of the first plant
        ypf = upf - 2.00997554244489 * env.upf_1 + 1.00997554244489 * env.upf_2 + 1.99501347669693 * env.ypf_1 - 0.995012479192682 * env.ypf_2
        env.ypf_2 = env.ypf_1
        env.ypf_1 = ypf
        env.upf_2 = env.upf_1
        env.upf_1 = upf

        # y of the second plant
        yps = Ts * env.ups_1 + env.yps_1
        env.yps_1 = yps
        ups = ypf
        env.ups_1 = ups

        # y, y_dot
        return yps, ypf

    def gen_ref(self):
        env = self.env
        return env.ref_arr[env.counter % env.ref_arr.shape[0]]

    def gen_ref_dot(self):
        env = self.env
        return env.ref_dot_arr[env.counter % env.ref_arr.shape[0]]

    def reward(self):
        env = self.env
        errors = np.array([env.error**2,
                           env.error_dot**2,
                           env.u**2])
        weights = np.array([0.01,
                            0.0001,
                            0.01])
        exp_weights = np.array([0.5,
                                0.3,
                                0.2])
        reward = exp_weights * np.exp(- errors * weights)

        return np.sum(reward)

    def plot_curves(self):
        env = self.env
        import matplotlib.pyplot as plt

        y = np.array(env.y_res)
        y_dot = np.array(env.y_dot_res)
        u = np.array(env.u_res)
        r = np.array(env.r_res)
        r_dot = np.array(env.r_dot_res)

        plt.figure('PID w non-minimum phase plant control')

        plt.subplot(311)
        plt.title('Position')
        plt.plot(r)
        plt.plot(y, '--')

        plt.subplot(312)
        plt.title('Velocity')
        plt.plot(r_dot)
        plt.plot(y_dot, '--')

        plt.subplot(313)
        plt.title('Plant Input')
        plt.plot(u)

        plt.show()
