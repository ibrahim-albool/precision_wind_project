import numpy as np
import os
import pandas as pd
np.random.seed(1111)

class Initializer:
    def __init__(self, env, dynamics_randomization=False):
        self.env = env
        self.initialize(dynamics_randomization)

    def initialize(self, dynamics_randomization):
        env = self.env
        env.dynamics_randomization = dynamics_randomization

        state_est_size = 10
        env.observation_space = np.zeros(state_est_size)
        env.action_space = np.zeros(1)
        env.end_episode = False

        env.impact_forces_list = np.array([[0., 0., 0.],
                                           [15., 0., 0.],
                                           [0., 15., 0.],
                                           [0., 0., 15.],
                                           [-15., 0., 0.],
                                           [0., -15., 0.],
                                           [0., 0., -15.]])
        env.impact_forces_list /= 15.
        env.impact_forces_list *= 1.
        # env.impact_force_index = np.random.randint(env.impact_forces_list.shape[0])
        # env.impact_force_index = 6
        env.impact_force_index = 1
        env.impact_force = env.impact_forces_list[env.impact_force_index]

        env.l2_norm_err_list = []
        env.exp_num = 0



    def reset(self):
        env = self.env
        # super(Environment, env).reset()
        env.counter = 0
        env.end_episode = False

        # env.impact_force_index = np.random.randint(env.impact_forces_list.shape[0]-2)+1
        env.impact_force_index += 1
        if env.impact_force_index > 5:
            env.impact_force_index = 1
        env.impact_force = env.impact_forces_list[env.impact_force_index]


        env.l2_norm_err_list = []
        # env.time_shift = env.exp_num/200.
        env.time_shift = np.random.rand()
        env.exp_num += 1
        print(f"Experiment Number {env.exp_num}")

        return env.control_engine.get_full_states()
