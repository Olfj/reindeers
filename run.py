import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from Reactor import PWR

def run_absorb():
    n = 100
    dim = 100
    n_initial_neutrons = 500
    speed = 1
    seed = 42
    absorb_rates = np.linspace(0.01, 0.3, 20)
    epochs = 2000
    th_epoch = 1000
    max_temperature = 700
    max_reactivity = 2
    repetitions = 1

    temperatures = np.zeros(absorb_rates.size)
    reactivities = np.zeros(absorb_rates.size)

    for r in range(repetitions):
        for i, a_rate in enumerate(absorb_rates):
            model = PWR(n, dim, n_initial_neutrons, speed, a_rate, seed=seed, plot_data=False)
            acc_temperature = 0
            acc_reactivity = 0
            for epoch in tqdm(range(epochs)):
                model.update(epoch)
                # Discard beginning
                if epoch >= th_epoch:
                    acc_temperature += model.temperature
                    acc_reactivity += model.get_reactivity()
                # Reached upper reasonable bound
                if model.temperature > 700:
                    temperatures[i] += max_temperature
                    reactivities[i] += max_reactivity # acc_reactivity / epoch
                    print(f'===for a_rate = {a_rate}===')
                    print(f'Reached Max temperature')
                    break
            else:
                temperatures[i] += acc_temperature / (epochs-th_epoch)
                reactivities[i] += acc_reactivity / (epochs-th_epoch)
                print(f'===for a_rate = {a_rate}===')
                print(f'T = {temperatures[i]}')
                print(f'r = {reactivities[i]}')
                
    temperatures = temperatures / repetitions
    reactivities = reactivities / repetitions

    fig = plt.figure(figsize=(10,10))
    gs = fig.add_gridspec(2, 1)
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[1,0])
    ax1.set_title('Average temperature/$A_c$')
    ax1.set_xlabel('$A_c$')
    ax1.set_ylabel('T')
    ax2.set_title('Average reactivity/$A_c$')
    ax2.set_xlabel('$A_c$')
    ax2.set_ylabel('$r$')

    ax1.scatter(absorb_rates, temperatures)
    ax2.scatter(absorb_rates, reactivities)
    ax1.plot(absorb_rates, [598.84]*len(absorb_rates), c='k', linestyle='dashed')
    ax2.plot(absorb_rates, [1]*len(absorb_rates), c='k', linestyle='dashed')
    plt.show()
    

if __name__ == '__main__':
    run_absorb()