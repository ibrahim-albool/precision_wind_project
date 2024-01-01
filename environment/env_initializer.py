import numpy as np
import os
import pandas as pd

class Initializer:
    def __init__(self, env, dynamics_randomization=False):
        self.env = env
        self.initialize(dynamics_randomization)

    def initialize(self, dynamics_randomization):
        env = self.env

        df = pd.read_excel('environment/y_ref.xlsx', sheet_name='Sheet1')
        env.y_ref = df["y_ref"].to_numpy()
        env.V_y_ref = df["V_y_ref"].to_numpy()


        state_est_size = 12
        env.observation_space = np.zeros(state_est_size)
        env.action_space = np.zeros(1)

        env.T = 10.
        env.Ts = 0.01
        env.eps_length = int(10./env.Ts)
        # period of execution of NN
        env.N = 2


        env.Kpx = 20.
        env.Kdx = 20.

        env.Kpy = 1.5
        env.Kdy = 15.

        env.thersh_limit = 5.

        env.t = 0.
        env.counter = 0



        env.xn = 0.
        env.V_xn = 0.
        env.yn = 0.
        env.V_yn = 0.

        env.xn_1 = 0.
        env.V_xn_1 = 0.
        env.yn_1 = 0.
        env.V_yn_1 = 0.

        env.V_w_arr = np.zeros((env.eps_length,))

        env.x_ref_arr = np.zeros((env.eps_length,))
        env.V_x_ref_arr = np.zeros((env.eps_length,))
        env.y_ref_arr = env.y_ref
        env.V_y_ref_arr = env.V_y_ref

        env.t_array = np.arange(0, env.T, env.Ts)



    def reset(self):
        env = self.env

        # plant states

        env.t = 0.
        env.counter = 0

        # from -3 to 3
        env.xn = 3.0 #np.random.rand()*6-3.
        env.V_xn = 0.
        env.yn = -1.
        env.V_yn = 0.

        env.xn_1 = 0.
        env.V_xn_1 = 0.
        env.yn_1 = 0.
        env.V_yn_1 = 0.

        env.u_x_n = 0.
        env.u_y_n = 0.
        env.u_controller_x = 0.
        env.u_controller_y = 0.

        env.V_w_arr = np.zeros((env.eps_length,))
        # 0.2 + 0.4 * rand ( from 0.2 to 0.6 )
        impulse_width_rand = np.random.rand() #*0. +0.5
        impulse_width = int(impulse_width_rand * 0.4 / env.Ts + 0.2 / env.Ts)
        # 1.0 + 5.0 * rand ( from 1.0 to 6.0 )
        impulse_start_rand = np.random.rand() *0. +1.0
        impulse_start = int(impulse_start_rand * 3.0 / env.Ts + 1.0 / env.Ts)
        env.V_w_arr[impulse_start:impulse_start + impulse_width] = 15.


        env.x_arr = []
        env.V_x_arr = []
        env.y_arr = []
        env.V_y_arr = []


        env.u_x_arr = []
        env.u_y_arr = []
        env.controller_selection_arr = []



        return env.control_engine.get_full_states()
