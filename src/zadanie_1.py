import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import poisson

# Definicja funkcji intensywności lambda(t)
def lambda_t(t):
    return 5 * np.sin(t) + 6

# Maksymalna wartość lambda(t) w przedziale [0, T]
T = 10
lambda_max = max(lambda_t(t) for t in np.linspace(0, T, 1000))

# Generowanie czasów oczekiwania niejednorodnego procesu Poissona metodą przerzedzania
def generate_inhomogeneous_poisson_process(lambda_t, lambda_max, T):
    events = []
    t = 0
    while t < T:
        u = np.random.uniform()
        t += -np.log(u) / lambda_max  # generowanie czasów dla jednorodnego procesu Poissona
        if t < T and np.random.uniform() < lambda_t(t) / lambda_max:
            events.append(t)
    return np.array(events)

# Generowanie procesów
np.random.seed(42)
events = generate_inhomogeneous_poisson_process(lambda_t, lambda_max, T)

# Sprawdzenie poprawności: N_t ~ Poiss(calka od 0 do t lambda(s) ds)
def integral_lambda(t):
    result, _ = quad(lambda_t, 0, t)
    return result

# Generowanie dystrybuanty
times = np.linspace(0, T, 100)
empirical_counts = [np.sum(events <= t) for t in times]

# Wykres dystrybuanty
plt.figure(figsize=(10, 6))
plt.step(times, empirical_counts, where='post', label='Empirical CDF')
plt.xlabel('Time')
plt.ylabel('Cumulative Count')
plt.legend()
plt.show()
