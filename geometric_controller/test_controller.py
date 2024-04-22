from geometric_controller.geometric_controller_env import GeometricControllerEnv
from geometric_controller.plot_data import plot_geometric_data


def test_controller():
    
    env = GeometricControllerEnv()


    for i in range(env.N):
        env.step(0.)
    
    plot_geometric_data(env)



if __name__ == "__main__":
    # Run the test controller
    test_controller()
