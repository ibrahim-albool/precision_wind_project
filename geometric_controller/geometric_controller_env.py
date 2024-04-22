import numpy as np
import matplotlib.pyplot as plt

# Test controller script
from geometric_controller.aux_functions.generate_output_arrays import generate_output_arrays
from geometric_controller.aux_functions.plot_3x1 import plot_3x1
from geometric_controller.test_functions.command import command
from geometric_controller.test_functions.eom import eom

class GeometricControllerEnv:
    def __init__(self):
        self.dt = 0.01
        self.t_span = (0, 10.0 + self.dt)
        self.t = np.arange(self.t_span[0], self.t_span[1], self.dt)
        self.N = len(self.t)

        # Quadrotor parameters
        self.J1, self.J2, self.J3 = 0.02, 0.02, 0.04
        self.param = {}
        self.k = {}
        self.param['J'] = np.diag([self.J1, self.J2, self.J3])
        self.param['m'] = 2
        self.param['d'] = 0.169
        self.param['ctf'] = 0.0135
        self.param['x_delta'] = np.array([0.5, 0.8, -1])
        self.param['R_delta'] = np.array([0.2, 1.0, -0.1])
        self.param['g'] = 9.81

        # Controller gains
        self.k['x'], self.k['v'], self.k['i'] = 10, 8, 10
        self.param['c1'], self.param['sigma'] = 1.5, 10
        self.k['R'], self.k['W'], self.k['I'] = 1.5, 0.35, 10
        self.param['c2'] = 2
        self.k['y'], self.k['wy'], self.k['yI'] = 0.8, 0.15, 2
        self.param['c3'] = 2

        # Initial conditions
        self.x0, self.v0, self.R0, self.W0 = np.zeros(3), np.zeros(3), np.eye(3), np.zeros(3)
        # x0 = np.array([0,0, 0])
        self.X0 = np.concatenate([self.x0, self.v0, self.W0, self.R0.flatten(), np.zeros(6)])

        # Discrete Integration
        # The discrete integration is more applicable in our case because we can have access to the states at each time step
        # which is not the case with solve_ipv; it does the calculations and returns the results when it is done
        self.X_accum = self.X0
        self.X = np.zeros((self.N, self.X0.shape[0]))
        self.e, self.d, self.R, self.f, self.M = generate_output_arrays(self.N)
        self.x, self.v, self.W, self.ei, self.eI = self.X[:, :3].T, self.X[:, 3:6].T, self.X[:, 6:9].T, self.X[:, 18:21].T, self.X[:, 21:24].T

        self.sim_step = 0




    def step(self, action):
        self.dynamics_step()
        self.sim_step += 1

    def dynamics_step(self):
        i = self.sim_step
        self.desired = command(self.t[i])
        self.Xdot, self.pos_ctrl_tuple = eom(self.t[i], self.X_accum, self.desired, self.k, self.param)
        self.X[i] = self.X_accum
        self.X_accum += self.Xdot*self.dt

        # for observation purposes
        self.R[:, :, i] = self.X[i, 9:18].reshape(3, 3)
        self.f[:, i], self.M[:, i], _, _, self.err, self.calc = self.pos_ctrl_tuple
        self.e['x'][:, i], self.e['v'][:, i], self.e['R'][:, i], self.e['W'][:, i], self.e['y'][:, i], self.e['Wy'][:, i] = self.err['x'], self.err['v'], self.err[
            'R'], self.err['W'], self.err['y'], self.err['Wy']
        self.d['x'][:, i], self.d['v'][:, i], self.d['b1'][:, i], self.d['R'][:, :, i] = self.desired['x'], self.desired['v'], self.desired['b1'], self.calc['R']

        # if 5.5>=t[i]>=5.0:
        #     k['x'], k['v'], k['i'] = 30, 20, 30
        #     k['R'], k['W'], k['I'] = 4., 0.90, 25
        #     k['y'], k['wy'], k['yI'] = 2.5, 0.7, 6
        # # print(t[i])
        # else:
        #     k['x'], k['v'], k['i'] = 10, 8, 10
        #     k['R'], k['W'], k['I'] = 1.5, 0.35, 10
        #     k['y'], k['wy'], k['yI'] = 0.8, 0.15, 2



    def reset(self):
        self.dt = 0.01
        self.t_span = (0, 10.0 + self.dt)
        self.t = np.arange(self.t_span[0], self.t_span[1], self.dt)
        self.N = len(self.t)

        # Quadrotor parameters
        self.J1, self.J2, self.J3 = 0.02, 0.02, 0.04
        self.param = {}
        self.k = {}
        self.param['J'] = np.diag([self.J1, self.J2, self.J3])
        self.param['m'] = 2
        self.param['d'] = 0.169
        self.param['ctf'] = 0.0135
        self.param['x_delta'] = np.array([0.5, 0.8, -1])
        self.param['R_delta'] = np.array([0.2, 1.0, -0.1])
        self.param['g'] = 9.81

        # Controller gains
        self.k['x'], self.k['v'], self.k['i'] = 10, 8, 10
        self.param['c1'], self.param['sigma'] = 1.5, 10
        self.k['R'], self.k['W'], self.k['I'] = 1.5, 0.35, 10
        self.param['c2'] = 2
        self.k['y'], self.k['wy'], self.k['yI'] = 0.8, 0.15, 2
        self.param['c3'] = 2

        # Initial conditions
        self.x0, self.v0, self.R0, self.W0 = np.zeros(3), np.zeros(3), np.eye(3), np.zeros(3)
        # x0 = np.array([0,0, 0])
        self.X0 = np.concatenate([self.x0, self.v0, self.W0, self.R0.flatten(), np.zeros(6)])

        # Discrete Integration
        # The discrete integration is more applicable in our case because we can have access to the states at each time step
        # which is not the case with solve_ipv; it does the calculations and returns the results when it is done
        self.X_accum = self.X0
        self.X = np.zeros((self.N, self.X0.shape[0]))
        self.e, self.d, self.R, self.f, self.M = generate_output_arrays(self.N)
        self.x, self.v, self.W, self.ei, self.eI = self.X[:, :3].T, self.X[:, 3:6].T, self.X[:, 6:9].T, self.X[:,
                                                                                                        18:21].T, self.X[
                                                                                                                  :,
                                                                                                                  21:24].T

        self.sim_step = 0


