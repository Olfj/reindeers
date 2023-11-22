import numpy as np
from tqdm import tqdm
from Animator import Animator, Plotter

class PWR:
    def __init__(self, n, dim, n_neutrons, speed, n_blocks=10):
        ''' n_neutrons: number of initial neutrons '''
        self.radius = 5
        self.n = n
        self.dim = dim
        self.speed = speed
        self.block_size = int(dim/n_blocks)
        self.atoms = np.random.uniform(0, self.dim, size=(self.n, 2))
        self.neutrons = np.random.uniform(0, self.dim, size=(n_neutrons, 2))
        self.directions = np.random.uniform(-np.pi, np.pi, size=n_neutrons)
        colors = "green blue".split()
        self.plotter = Plotter(custom=colors)
        self.atom_table = self.init_atom_table()

    def init_atom_table(self):
        atom_table = {}
        hashed_positions = np.floor(self.atoms/self.block_size).astype(int)
        for index, position in enumerate(hashed_positions):
            hashed_pos = tuple(position)
            if val := atom_table.get(hashed_pos):
                val.append(index)
            else:
                val = [index]
            atom_table.update({hashed_pos: val})
        return atom_table
    
    def get_collidable(self, position):
        collidable = self.atom_table.get(tuple(np.floor(position/self.block_size).astype(int)))
        return collidable if collidable else []

    def update(self, i):
        self.plot(i)
        self.move_neutrons()
        self.collide()

    def plot(self, i):
        lim = (0, self.dim)
        self.plotter.scatter(self.atoms[:,0], self.atoms[:,1], lim, lim, c=0)
        self.plotter.scatter(self.neutrons[:,0], self.neutrons[:,1], lim, lim, redraw=False, s=10, c=1)
        self.plotter.show_stats(f"Generation: {i+1}, reactivity: {0}")

    def move_neutrons(self):
        ''' Move all neutrons '''
        self.neutrons += self.speed * np.array([np.cos(self.directions), np.sin(self.directions)]).T

    def collide(self):
        new_positions = self.neutrons.copy()
        new_directions = self.directions.copy()
        for neutron in self.neutrons:
            collidable = self.get_collidable(neutron)
            for index in collidable:
                if np.linalg.norm(self.atoms[index] - neutron) < self.radius:

                    dirs = np.random.uniform(-np.pi, np.pi, 3)
                    poss = np.full((3,2), neutron) + 1.1*self.radius*np.array([np.cos(dirs), np.sin(dirs)]).T
                    new_directions = np.append(new_directions, dirs)
                    new_positions = np.append(new_positions, poss, axis=0)
        self.neutrons = new_positions
        self.directions = new_directions

if __name__ ==  "__main__":
    n = 10
    dim = 100
    n_initial_neutrons = 3
    speed = 1
    pwr = PWR(n, dim, n_initial_neutrons, speed)
    anim = Animator(pwr.update, interval=25)
    anim.animate()