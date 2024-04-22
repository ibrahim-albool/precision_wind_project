from geometric_controller.geometric_controller_env import GeometricControllerEnv
from geometric_controller.plot_data import plot_geometric_data


def test_controller():
    
    env = GeometricControllerEnv()



    for i in range(env.N):
        if 5.5 >= env.t[i] >= 5.0:
            action = 1.
        else:
            action = 0.

        # action = 1.

        env.step(action)
    
    plot_geometric_data(env)



if __name__ == "__main__":
    # Run the test controller
    test_controller()
