import numpy as np

def command_lissajous(t):
    A = 1
    B = 1
    C = 0.2

    d = np.pi / 2 * 0

    a = 1
    b = 2
    c = 2
    alt = -1

    desired = {}

    x = A * np.sin(a * t + d)
    y = B * np.sin(b * t)
    z = alt + C * np.cos(2 * t)

    desired['x'] = np.array([x, y, z])

    vx = A * a * np.cos(a * t + d)
    vy = B * b * np.cos(b * t)
    vz = C * c * -np.sin(c * t)

    desired['v'] = np.array([vx, vy, vz])

    ax = A * a**2 * -np.sin(a * t + d)
    ay = B * b**2 * -np.sin(b * t)
    az = C * c**2 * -np.cos(c * t)

    desired['x_2dot'] = np.array([ax, ay, az])

    ax = A * a**3 * -np.cos(a * t + d)
    ay = B * b**3 * -np.cos(b * t)
    az = C * c**3 * np.sin(c * t)

    desired['x_3dot'] = np.array([ax, ay, az])

    ax = A * a**4 * np.sin(a * t + d)
    ay = B * b**4 * np.sin(b * t)
    az = C * c**4 * np.cos(c * t)

    desired['x_4dot'] = np.array([ax, ay, az])

    w = 2 * np.pi / 10
    desired['b1'] = np.array([np.cos(w * t), np.sin(w * t), 0])
    desired['b1_dot'] = w * np.array([-np.sin(w * t), np.cos(w * t), 0])
    desired['b1_2dot'] = w**2 * np.array([-np.cos(w * t), -np.sin(w * t), 0])

    return desired

