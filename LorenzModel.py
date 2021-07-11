import numpy as np
from scipy.integrate import odeint


def f(state, t, rho, sigma, beta):
    x, y, z = state  # Unpack the state vector
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # Derivatives


def run_lorenz(initial_state, t, dt, rho, sigma, beta):
    times = np.arange(0.0, t, dt)
    result = odeint(f, initial_state, times, args=(rho, sigma, beta))
    return np.array(np.array(result).T)