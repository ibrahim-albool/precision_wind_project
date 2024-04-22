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


        try:
            env.dynamics_step()
        except Exception as e:
            env.warning_happened = True
            print('----------------------------------- Warning ----------------------------------')
        full_states = self.get_full_states()

        reward = self.reward()



        env.counter += 1
        done = env.counter >= env.N or env.warning_happened

        # # show the plots
        # if done:
        #     self.plot_curves()

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

        return states.reshape(-1, 1)

    def reward(self):
        env = self.env

        if env.warning_happened:
            return -200.

        # errors_reward = np.power(np.e, -10 * np.abs(env.pos_error)) - 0.5 * np.power(env.pos_error, 2)
        error_norm_reward = np.power(np.e, -10 * np.abs(env.error_norm)) - 0.5 * np.power(env.error_norm, 2)

        # rewards = np.concatenate((errors_reward, error_norm_reward))
        # weights = np.array([1., 1., 1., 1.])

        # reward = np.sum(weights * rewards)

        return error_norm_reward[0] # reward
