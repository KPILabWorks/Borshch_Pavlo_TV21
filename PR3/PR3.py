# Практична робота №3
# Варіант №4
# Використовуючи Numba, реалізуйте обчислення енергетичних інтегралів методом Монте-Карло для прогнозування навантаження на електричну мережу.
# Порівняйте точність прогнозування енергетичних споживань при різних кількостях ітерацій.
import numpy as np
from numba import njit, prange
import matplotlib.pyplot as plt

@njit
def energy_consumption_model(x):
    """
    Example model for predicting electrical grid load.
    """
    return np.sin(x) + np.cos(2 * x) + 0.5 * np.sin(3 * x)

@njit(parallel=True)
def monte_carlo_integration(n_samples, a, b):
    """
    Calculation of energy integrals using the Monte Carlo method.
    """
    total = 0.0
    for i in prange(n_samples):
        x = np.random.uniform(a, b)
        total += energy_consumption_model(x)
    return (b - a) * total / n_samples

# Integration limits
a, b = 0, 10

# Different iteration values
iterations = [100, 500, 1000, 5000, 10000, 50000]
true_value = 0.0  # Theoretical integral value (for comparison)

# Computing integrals and errors
errors = []
values = []
for n in iterations:
    integral_value = monte_carlo_integration(n, a, b)
    values.append(integral_value)
    errors.append(abs(integral_value - true_value))

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(iterations, errors, marker='o', linestyle='--', label='Error')
plt.xscale('log')
plt.xlabel('Number of iterations')
plt.ylabel('Absolute error')
plt.title('Error dependence on the number of iterations')
plt.legend()
plt.grid()
plt.show()

# Output integral values
for n, val in zip(iterations, values):
    print(f'Number of iterations: {n}, approximate integral value: {val:.5f}')
