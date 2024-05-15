import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import poisson

# Definicja funkcji intensywności lambda_1(t) i lambda_2(t)
def lambda_1(t):
    return np.cos(t) + 1

def lambda_2(t):
    return np.sin(t) + 1

# Maksymalna wartość intensywności w przedziale [0, T]
T = 15
lambda_max_1 = 2  # max(lambda_1(t))
lambda_max_2 = 2  # max(lambda_2(t))

# Generowanie czasów oczekiwania niejednorodnego procesu Poissona metodą przerzedzania
def generate_inhomogeneous_poisson_process(lambda_t, lambda_max, T):
    times = []
    t = 0
    while True:
        U_1 = np.random.uniform(0, 1)
        t = t - (1 / lambda_max) * np.log(U_1)
        if t > T:
            break
        U_2 = np.random.uniform(0, 1)
        if U_2 <= lambda_t(t) / lambda_max:
            times.append(t)
    times.sort()
    return times

# Generowanie procesów
np.random.seed(42)
times_1 = generate_inhomogeneous_poisson_process(lambda_1, lambda_max_1, T)
np.random.seed(43)
times_2 = generate_inhomogeneous_poisson_process(lambda_2, lambda_max_2, T)

# Łączenie procesów
combined_times = sorted(times_1 + times_2)

# Sprawdzenie poprawności: intensywność procesu wynikowego
def combined_lambda(t):
    return lambda_1(t) + lambda_2(t)

def integral_combined_lambda(t):
    result, _ = quad(combined_lambda, 0, t)
    return result

# Generowanie dystrybuanty
times_grid = np.linspace(0, T, 100)
empirical_counts = [np.sum(np.array(combined_times) <= t) for t in times_grid]

# Wykres dystrybuanty
plt.figure(figsize=(10, 6))

# Empiryczna dystrybuanta
plt.step(times_grid, empirical_counts, where='post', label='Empirical CDF', color='blue')

plt.xlabel('Time')
plt.ylabel('Cumulative Count')
plt.legend()
plt.show()
