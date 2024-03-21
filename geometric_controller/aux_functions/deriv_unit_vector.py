import numpy as np

def deriv_unit_vector(q, q_dot, q_ddot):
    nq = np.linalg.norm(q)
    u = q / nq
    u_dot = q_dot / nq - q * np.dot(q, q_dot) / nq**3

    u_ddot = q_ddot / nq - q_dot / nq**3 * (2 * np.dot(q, q_dot)) \
        - q / nq**3 * (np.dot(q_dot, q_dot) + np.dot(q, q_ddot)) \
        + 3 * q / nq**5 * np.dot(q, q_dot)**2

    return u, u_dot, u_ddot
