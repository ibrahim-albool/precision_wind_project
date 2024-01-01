from .step_engine import ControlEngine
import numpy as np


class Environment:
    def __init__(self, dynamics_randomization=False):
        self.control_engine = ControlEngine(self, dynamics_randomization)

    def step(self, action):
        return self.control_engine.processStep(action)

    def reset(self):
        return self.control_engine.initializer.reset()


    def render(self):

        return self.control_engine.get_full_states()
