from geometric_controller.test_functions.command_lissajous import command_lissajous


def command(t):
    # Uncomment the following line if you want to use the command_line function
    # from command_line import command_line

    # Use either command_line or command_lissajous based on your preference
    return command_lissajous(t)
