import numpy as np

def true_data(t):
    w = 1
    ship_x = 3 * np.sin(w * t)
    ship_y = 2 * np.cos(w * t)
    ship_z = 0

    uav_wrt_ship_x = 0.1 * np.cos(5 * np.pi * t)
    uav_wrt_ship_y = 0.1 * np.sin(5 * np.pi * t)
    uav_wrt_ship_z = 1.0 * np.sin(2 * t)

    uav_x = ship_x + uav_wrt_ship_x
    uav_y = ship_y + uav_wrt_ship_y
    uav_z = ship_z + uav_wrt_ship_z

    x_ship = np.array([ship_x, ship_y, ship_z])
    x_uav = np.array([uav_x, uav_y, uav_z])
    x_us = np.array([uav_wrt_ship_x, uav_wrt_ship_y, uav_wrt_ship_z])

    return x_ship, x_uav, x_us
