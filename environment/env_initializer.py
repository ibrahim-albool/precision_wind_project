import numpy as np
import os


class Initializer:
    def __init__(self, env, dynamics_randomization=False):
        self.env = env
        self.initialize(dynamics_randomization)

    def initialize(self, dynamics_randomization):
        env = self.env

        state_est_size = 7
        env.observation_space = np.zeros(state_est_size)
        env.action_space = np.zeros(4)

        # plant states
        env.ypf_2 = 0.
        env.ypf_1 = 0.
        env.upf_2 = 0.
        env.upf_1 = 0.
        env.yps_1 = 0.
        env.ups_1 = 0.

        # states
        env.r = 0.
        env.r_dot = 0.
        env.error = 0.
        env.error_dot = 0.
        env.y = 0.
        env.y_dot = 0.
        env.u = 0.

        # PID states
        env.Ic_1 = 0.
        env.error_1 = 0.
        env.Dc_1 = 0.

        env.counter = 0
        env.ref_arr = np.zeros((10000,))
        env.ref_arr[1000:] = 1.
        env.ref_dot_arr = np.zeros((10000,))
        env.ref_dot_arr[1000] = 1000.

        env.y_res = []
        env.y_dot_res = []
        env.u_res = []
        env.r_res = []
        env.r_dot_res = []




    def reset(self):
        env = self.env

        # plant states
        env.ypf_2 = 0.
        env.ypf_1 = 0.
        env.upf_2 = 0.
        env.upf_1 = 0.
        env.yps_1 = 0.
        env.ups_1 = 0.

        # states
        env.r = 0.
        env.r_dot = 0.
        env.error = 0.
        env.error_dot = 0.
        env.y = 0.
        env.y_dot = 0.
        env.u = 0.

        # PID states
        env.Ic_1 = 0.
        env.error_1 = 0.
        env.Dc_1 = 0.

        env.counter = 0

        env.y_res = []
        env.y_dot_res = []
        env.u_res = []
        env.r_res = []
        env.r_dot_res = []

        return env.control_engine.get_full_state()
