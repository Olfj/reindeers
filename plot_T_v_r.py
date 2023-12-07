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

pwr = PWR(n, dim, n_initial_neutrons, speed, seed=rng, plot_data=False, absorb_rate=0.021)

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

color_left = 'tab:orange'
color_right = 'tab:blue'

axleft = fig.add_subplot(gs[0, 0])
axleft0 = axleft
axleft1 = axleft0.twinx() 


axleft0.set_xlabel('Time steps')
axleft0.set_ylabel('Temperature ⁰K', color=color_left)
axleft0.plot(gens, temps, color=color_left)
axleft0.tick_params(axis='y', labelcolor=color_left)

axleft1.set_ylabel('Reactivity', color=color_right)
axleft1.plot(gens, reactivities, color=color_right)
axleft1.tick_params(axis='y', labelcolor=color_right)


# axleft0.set_xlabel('Time steps')
# axleft0.set_ylabel('Temperature ⁰K', color=color_left)
# axleft0.plot(gens[:1000], temps[:1000], color=color_left)
# axleft0.tick_params(axis='y', labelcolor=color_left)

# axleft1.set_ylabel('Reactivity', color=color_right)
# axleft1.plot(gens[:1000], reactivities[:1000], color=color_right)
# axleft1.tick_params(axis='y', labelcolor=color_right)


# axright = fig.add_subplot(gs[1, 0])
# axright0 = axright
# axright1 = axright0.twinx()

# axright0.set_xlabel('Time steps')
# axright0.set_ylabel('Temperature ⁰K', color=color_left)
# axright0.plot(gens[4000:4500], temps[4000:4500], color=color_left)
# axright0.tick_params(axis='y', labelcolor=color_left)

# axright1.set_ylabel('Reactivity', color=color_right)
# axright1.plot(gens[4000:4500], reactivities[4000:4500], color=color_right)
# axright1.tick_params(axis='y', labelcolor=color_right)


plt.show()