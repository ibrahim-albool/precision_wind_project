import numpy as np
import os
import pandas as pd


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



    def reset(self):
        env = self.env
        # super(Environment, env).reset()
        env.counter = 0

        return env.control_engine.get_full_states()
