import numpy as np
from tqdm import tqdm
from Animator import Animator, Plotter

class PWR:
    def __init__(self, n, dim):
        self.n = n
        self.dim = dim
        self.atoms = np.random.uniform(0, self.dim, size=(self.n, 2))
        self.neutrons = np.random.uniform(0, self.dim, size=(5, 2))
        colors = "green blue".split()
        self.plotter = Plotter(custom=colors)

    def update(self, i):
        self.plot(i)
        self.update_neutrons()
       
    def plot(self, i):
        lim = (0, self.dim)
        self.plotter.scatter(self.atoms[:,0], self.atoms[:,1], lim, lim, c=0)
        self.plotter.scatter(self.neutrons[:,0], self.neutrons[:,1], lim, lim, redraw=False, s=10, c=1)
        self.plotter.show_stats(f"Generation: {i+1}, reactivity: {0}")

    def update_neutrons(self):
        pass

if __name__ ==  "__main__":
    n = 10
    dim = 100
    pwr = PWR(n, dim)
    anim = Animator(pwr.update, interval=25)
    anim.animate()