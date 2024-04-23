from environment import Environment
from geometric_controller.plot_data import plot_geometric_data


def test_controller():
    
    env = Environment()
    env.reset()

    done = False

    reward_list = []

    while not done:
        if 5.5 >= env.t[env.counter] >= 5.0:
            action = 1.
        else:
            action = 0.

        # action = 1.

        full_states, reward, done, _ = env.step(action)
        reward_list.append(reward)
        # print(f"full_states = {full_states}")
        print(f"counter = {env.counter}, reward = {reward}, error_norm = {env.error_norm}")

    print(f"Non-discounted return = {sum(reward_list)}")

    # plot_geometric_data(env)



if __name__ == "__main__":
    # Run the test controller
    test_controller()
