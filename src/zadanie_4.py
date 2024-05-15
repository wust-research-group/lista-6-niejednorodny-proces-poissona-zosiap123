import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import poisson

# Definicja funkcji intensywności lambda(t)
def lambda_t(t):
    return np.cos(t) + 1

# Definicja funkcji p_k(t)
def p_1(t):
    return 0.5 * (1 + np.sin(t))

def p_2(t):
    return 1 - p_1(t)

# Maksymalna wartość lambda(t) w przedziale [0, T]
T = 15
lambda_max = 2

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
times = generate_inhomogeneous_poisson_process(lambda_t, lambda_max, T)

# Przypisanie znaczników Z_i
labels = []
for t in times:
    p = p_1(t)
    if np.random.uniform(0, 1) < p:
        labels.append(1)
    else:
        labels.append(2)

# Podział zdarzeń na podprocesy
times_1 = [times[i] for i in range(len(times)) if labels[i] == 1]
times_2 = [times[i] for i in range(len(times)) if labels[i] == 2]

# Funkcje intensywności dla podprocesów
def lambda_1(t):
    return p_1(t) * lambda_t(t)

def lambda_2(t):
    return p_2(t) * lambda_t(t)

# Całki z intensywności
def integral_lambda_1(t):
    return quad(lambda_1, 0, t)[0]

def integral_lambda_2(t):
    return quad(lambda_2, 0, t)[0]

# Generowanie dystrybuant
times_grid = np.linspace(0, T, 100)
empirical_counts_1 = [np.sum(np.array(times_1) <= t) for t in times_grid]
empirical_counts_2 = [np.sum(np.array(times_2) <= t) for t in times_grid]

# Wykres dystrybuant
plt.figure(figsize=(12, 6))

# Empiryczna dystrybuanta dla podprocesu 1
plt.step(times_grid, empirical_counts_1, where='post', label='Empirical CDF (Process 1)', color='blue')

# Empiryczna dystrybuanta dla podprocesu 2
plt.step(times_grid, empirical_counts_2, where='post', label='Empirical CDF (Process 2)', color='green')

plt.xlabel('Time')
plt.ylabel('Cumulative Count')
plt.legend()
plt.show()
