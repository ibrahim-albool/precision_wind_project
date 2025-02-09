import numpy as np

from geometric_controller.plot_data import plot_geometric_data
from .env_initializer import Initializer
np.random.seed(1111)

class ControlEngine:
    def __init__(self, env, dynamics_randomization):
        self.env = env
        self.initializer = Initializer(env, dynamics_randomization)

    def processStep(self, action):
        env = self.env
        # print(action)
        action = np.clip(action, 0., 1.) > 0.5

        # action = 1.

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

        # if env.counter >= 500:
        #     env.param['m'] = 1
        env.dynamics_step()
        full_states = self.get_full_states()
        reward = self.reward()
        env.l2_norm_err_list.append(env.error_norm)

        env.counter += 1
        done = env.counter >= env.N or env.end_episode

        # # show the plots
        if done:
            print(f"impact force: {env.impact_force}")

            L2_error_norm = np.array(env.l2_norm_err_list).flatten() * np.sqrt(env.dt) # dt will be squared in the L2 Norm
            L2_error_norm = np.linalg.norm(L2_error_norm)
            Linf_error_norm = np.max(env.l2_norm_err_list)
            print(f"L2 error norm {L2_error_norm}")
            print(f"Linf error norm {Linf_error_norm}")
            plot_geometric_data(env)

        # print(f"counter = {env.counter}, reward = {reward}, error_norm = {env.error_norm}")

        return full_states, reward, done, {}

    # get the states of interest
    def get_full_states(self):
        env = self.env

        env.pos_current = env.x[:, env.counter]
        env.pos_error = env.e['x'][:, env.counter]
        env.pos_des = env.d['x'][:, env.counter]
        env.error_norm = np.array(np.linalg.norm(env.pos_error)).reshape(-1,)


        states = np.concatenate((env.pos_current, env.pos_error, env.pos_des, env.error_norm ))

        # states = np.clip(np.abs(states), 0., 5.0) / 5.

        return states

    def reward(self):
        env = self.env

        if env.error_norm[0] > 20.:
            env.end_episode = True
            return -500.

        # errors_reward = np.power(np.e, -10 * np.abs(env.pos_error)) - 0.5 * np.power(env.pos_error, 2)
        error_norm_reward = np.power(np.e, -10 * np.abs(env.error_norm)) - 0.5 * np.power(env.error_norm, 2)

        # rewards = np.concatenate((errors_reward, error_norm_reward))
        # weights = np.array([1., 1., 1., 1.])

        # reward = np.sum(weights * rewards)

        return error_norm_reward[0] # reward
