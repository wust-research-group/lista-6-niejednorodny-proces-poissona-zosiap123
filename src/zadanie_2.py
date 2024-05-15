import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import poisson

# Definicja funkcji intensywności lambda(t)
def lambda_t(t):
    return np.cos(t) + 1

# Funkcja m(t) - całka z lambda(t) od 0 do t
def m_t(t):
    return quad(lambda_t, 0, t)[0]

# Funkcja odwrotna do dystrybuanty F(t)
def inverse_F(u, T):
    from scipy.optimize import brentq
    return brentq(lambda t: m_t(t) / m_t(T) - u, 0, T)

# Parametry
T = 15

# Obliczenie m(T)
m_T = m_t(T)

# Generowanie liczby zdarzeń N_T
np.random.seed(42)
N_T = np.random.poisson(m_T)

# Generowanie czasów zdarzeń
u = np.random.uniform(0, 1, N_T)
times = np.sort([inverse_F(ui, T) for ui in u])

# Sprawdzenie poprawności: N_t ~ Poiss(calka od 0 do t lambda(s) ds)
times_grid = np.linspace(0, T, 100)
empirical_counts = [np.sum(np.array(times) <= t) for t in times_grid]

# Wykres dystrybuanty
plt.figure(figsize=(10, 6))

# Empiryczna dystrybuanta
plt.step(times_grid, empirical_counts, where='post', label='Empirical CDF', color='blue')

plt.xlabel('Time')
plt.ylabel('Cumulative Count')
plt.legend()
plt.show()
