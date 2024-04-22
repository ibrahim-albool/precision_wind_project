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

        if action >= 0.5:  # Aggressive gains
            env.k['x'], env.k['v'], env.k['i'] = 30, 20, 30
            env.k['R'], env.k['W'], env.k['I'] = 4., 0.90, 25
            env.k['y'], env.k['wy'], env.k['yI'] = 2.5, 0.7, 6
            env.active_controller = 1
        else:  # normal gains
            env.k['x'], env.k['v'], env.k['i'] = 10, 8, 10
            env.k['R'], env.k['W'], env.k['I'] = 1.5, 0.35, 10
            env.k['y'], env.k['wy'], env.k['yI'] = 0.8, 0.15, 2
            env.active_controller = 0

        env.active_controller_list.append(env.active_controller)

        env.dynamics_step()
        full_states = self.get_full_states()
        reward = self.reward()



        env.counter += 1
        done = env.counter >= env.N

        # # show the plots
        # if done:
        #     self.plot_curves()

        return full_states, reward, done, {}

    # get the states of interest
    def get_full_states(self):
        env = self.env

        pos_current = env.x[:, env.counter]
        pos_error = env.e['x'][:, env.counter]
        pos_des = env.d['x'][:, env.counter]
        error_norm = np.array(np.linalg.norm(pos_error)).reshape(-1,)


        states = np.concatenate((pos_current, pos_error, pos_des, error_norm ))

        # states = np.clip(np.abs(states), 0., 5.0) / 5.

        return states.reshape(-1, 1)

    def reward(self):
        env = self.env
        squared_errors = np.array([0., 0., 0.])

        weights = np.array([0.05,
                            0.85,
                            0.1])

        reward = -np.sum(weights * squared_errors)

        return reward
