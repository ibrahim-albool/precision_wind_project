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




    def reset(self):
        env = self.env
        # super(Environment, env).reset()

        return env.control_engine.get_full_states()
