import matplotlib.pyplot as plt
import numpy as np
from Reactor import PWR
from tqdm import tqdm
from matplotlib.gridspec import GridSpec

def moving_average(x, w=50):
    return np.convolve(x, np.ones(w), 'valid') / w

n = 100
dim = 100
n_initial_neutrons = 200
speed = 1
rng = np.random.default_rng(seed=42)
average = 50

pwr = PWR(n, dim, n_initial_neutrons, speed, rng, plot_data=False)

length = 10049

gens = np.arange(length)
temps = np.zeros(length)
reactivities = np.zeros(length)

for gen in tqdm(gens):
    reactivities[gen] = pwr.get_reactivity()
    temps[gen] = pwr.temperature
    pwr.update(1)


reactivities = moving_average(reactivities)
temps = moving_average(temps)
gens = np.arange(length-49)

# Some example data to display
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

fig = plt.figure()
gs = GridSpec(nrows=2, ncols=1)
axleft = fig.add_subplot(gs[0, 0])
axleft0 = axleft
axleft1 = axleft0.twinx() 

# Plot the first function on the left y-axis
color = 'tab:orange'
axleft0.set_xlabel('Time steps')
axleft0.set_ylabel('Temperature ⁰K', color=color)
axleft0.plot(gens[:2000], temps[:2000], color=color)
axleft0.tick_params(axis='y', labelcolor=color)

# Plot the second function on the right y-axis
color = 'tab:blue'
axleft1.set_ylabel('Reactivity', color=color)
axleft1.plot(gens[:2000], reactivities[:2000], color=color)
axleft1.tick_params(axis='y', labelcolor=color)


axright = fig.add_subplot(gs[1, 0])
axright0 = axright
axright1 = axright0.twinx()

# Plot the first function on the left y-axis
color = 'tab:orange'
axright0.set_xlabel('Time steps')
axright0.set_ylabel('Temperature ⁰K', color=color)
axright0.plot(gens[2000:], temps[2000:], color=color)
axright0.tick_params(axis='y', labelcolor=color)

# Plot the second function on the right y-axis
color = 'tab:blue'
axright1.set_ylabel('Reactivity', color=color)
axright1.plot(gens[2000:], reactivities[2000:], color=color)
axright1.tick_params(axis='y', labelcolor=color)


plt.show()