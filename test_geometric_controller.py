# from geometric_controller import GeometricControllerEnv
from environment import Environment
from geometric_controller.plot_data import plot_geometric_data


def test_controller():
    
    env = Environment()
    env.reset()

    done = False

    while not done:
        if 5.5 >= env.t[env.counter] >= 5.0:
            action = 1.
        else:
            action = 0.

        # action = 1.

        full_states, reward, done, _ = env.step(action)
    
    plot_geometric_data(env)



if __name__ == "__main__":
    # Run the test controller
    test_controller()
