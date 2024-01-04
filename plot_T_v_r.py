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

absorption_rates = [0.0215]

for rate in absorption_rates:

    pwr = PWR(n, dim, n_initial_neutrons, speed, seed=rng, plot_data=False, absorb_rate=rate)

    length = 100049

    gens = np.arange(length)
    temps = np.zeros(length)
    reactivities = np.zeros(length)

    for gen in tqdm(gens):
        reactivities[gen] = pwr.get_reactivity()
        temps[gen] = pwr.temperature
        pwr.update(1)
        if pwr.temperature > 670:
            break

    reactivities = moving_average(reactivities)
    temps = moving_average(temps)
    gens = np.arange(length - 49)

    for iterations in [(0, 500), (0, 1000), (0, 5000), (0, 10000), (2000, 2500), (0, 20000), (0, 50000), (0, 100000)]:

        fig, ax_left = plt.subplots(figsize=(12, 5))

        color_left = 'tab:orange'
        color_right = 'tab:blue'

        ax_right = ax_left.twinx()

        ax_left.set_xlabel('Time steps')
        ax_left.set_title('Temperature (K) and reactivity. Absorption rate= ' + str(rate))
        ax_left.set_ylabel('K')
        line1, = ax_left.plot(gens[iterations[0]:iterations[1]], temps[iterations[0]:iterations[1]], color=color_left, label='K')
        ax_left.tick_params(axis='y')

        ax_right.set_ylabel('Reactivity')
        line2, = ax_right.plot(gens[iterations[0]:iterations[1]], reactivities[iterations[0]:iterations[1]], label='Reactivity')
        ax_right.tick_params(axis='y')

        lines = [line1, line2]
        ax_left.legend(lines, [line.get_label() for line in lines], loc='upper left', bbox_to_anchor=(0.4, -0.2), ncol=2)

        plt.tight_layout()
        plt.savefig('plots/T_v_r/Absorption rate = ' + str(rate) + 'iterations = ' + str(iterations[1]) + '.png', bbox_inches='tight')
        plt.close()
