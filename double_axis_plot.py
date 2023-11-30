import matplotlib.pyplot as plt
import numpy as np
from Reactor import PWR
from tqdm import tqdm

# # Generate some sample data
# x = np.linspace(0, 10, 100)
# y1 = np.sin(x)
# y2 = 2 * np.cos(x)

def moving_average(x, w=50):
    return np.convolve(x, np.ones(w), 'valid') / w

n = 100
dim = 100
n_initial_neutrons = 200
speed = 1
rng = np.random.default_rng(seed=42)
pwr = PWR(n, dim, n_initial_neutrons, speed, rng)

length = 6000

gens = np.arange(length)
temps = np.zeros(length)
reactivities = np.zeros(length)

for gen in tqdm(gens):
    reactivities[gen] = pwr.get_reactivity()
    temps[gen] = pwr.temperature
    pwr.update()


reactivities = moving_average(reactivities)
temps = moving_average(temps)
gens = np.arange(5951)
# Create the first plot
fig, ax1 = plt.subplots()

# Plot the first function on the left y-axis
color = 'tab:orange'
ax1.set_xlabel('Time steps')
ax1.set_ylabel('Temperature ⁰K', color=color)
ax1.plot(gens[3000:], temps[3000:], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Create the second y-axis on the right
ax2 = ax1.twinx()

# Plot the second function on the right y-axis
color = 'tab:blue'
ax2.set_ylabel('Reactivity', color=color)
ax2.plot(gens[3000:], reactivities[3000:], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Show the plot
plt.show()
