import numpy as np
from tqdm import tqdm
from Animator import Animator, Plotter

class PWR:

    COLLISION_ENERGY = 200 * 1.602 * 10e-13
    HEAT_CAPACITY = 4.186
    BASE_TEMPERATURE = 548
    FLOW = 1 / 10
    REACTIVITY = 0.85
    CONTROL_ROD_ABSORB = 0.0225

    def __init__(self, n, dim, n_neutrons, speed, n_blocks=10):
        ''' n_neutrons: number of initial neutrons '''
        self.radius = 0.75
        self.n = n
        self.dim = dim
        self.speed = speed
        self.block_size = int(dim/n_blocks)
        self.atoms = np.random.uniform(0, self.dim, size=(self.n, 2))
        self.collided  = np.zeros((self.n))
        self.neutrons = np.random.uniform(0, self.dim, size=(n_neutrons, 2))
        self.directions = np.random.uniform(-np.pi, np.pi, size=n_neutrons)
        colors = "green blue".split()
        self.plotter = Plotter(custom=colors)
        self.atom_table = self.init_atom_table()
        self.reactivity = self.REACTIVITY
        self.temperature = self.BASE_TEMPERATURE
        self.volume = 10e-10

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
        energy = self.collide()
        self.adjust_temperature(energy)
        self.adjust_reactivity()
        self.absorb()

    def plot(self, i):
        lim = (0, self.dim)
        atoms = self.atoms[np.nonzero(self.collided == 0)[0]]
        self.plotter.scatter(self.atoms[:,0], self.atoms[:,1], lim, lim, c=0)
        self.plotter.scatter(self.neutrons[:,0], self.neutrons[:,1], lim, lim, redraw=False, s=10, c=1)
        self.plotter.show_stats(f"Generation: {i+1}, temperature: {self.temperature:.4f}, reactivity: {self.reactivity:.4f}")

    def move_neutrons(self):
        '''Move all neutrons'''
        self.neutrons += self.speed * np.array([np.cos(self.directions), np.sin(self.directions)]).T

    def collide(self):
        '''Collision detection'''
        new_positions = self.neutrons.copy()
        new_directions = self.directions.copy()
        energy = 0
        for i, neutron in enumerate(self.neutrons):
            collidable = self.get_collidable(neutron)
            for index in collidable:
                if np.linalg.norm(self.atoms[index] - neutron) < self.radius:# and self.collided[index] == 0:
                    if np.random.rand() < self.reactivity:
                        dirs = np.random.uniform(-np.pi, np.pi, 2)
                        poss = np.full((2,2), self.atoms[index]) + 1.1*self.radius*np.array([np.cos(dirs), np.sin(dirs)]).T
                        new_directions = np.append(new_directions, dirs)
                        new_positions = np.append(new_positions, poss, axis=0)
                        dir = np.array([np.cos(self.directions[i]), np.sin(self.directions[i])]).T
                        new_positions[i] = self.atoms[index] + dir * self.radius * 1.1
                        energy += self.COLLISION_ENERGY

                        self.collided[index] = 1
        self.neutrons = new_positions % self.dim
        self.directions = new_directions
        return energy
    
    def absorb(self):
        '''Control rod absorbtion'''
        mask = np.random.rand(len(self.neutrons))
        mask = np.nonzero(mask < self.CONTROL_ROD_ABSORB)[0]
        self.neutrons = np.delete(self.neutrons, mask, axis=0)
        self.directions = np.delete(self.directions, mask)

    def adjust_temperature(self, energy):
        ''''Change in water temperature as a function of fission and flow'''
        v_current = self.volume * (1 - self.FLOW)
        v_in = self.volume * self.FLOW
        temp = self.temperature + energy / (self.HEAT_CAPACITY * self.volume)
        self.temperature = (v_current * temp + v_in * self.BASE_TEMPERATURE) / self.volume

    def adjust_reactivity(self):
        self.reactivity = self.REACTIVITY * self.BASE_TEMPERATURE / self.temperature

if __name__ ==  "__main__":
    n = 100
    dim = 100
    n_initial_neutrons = 200
    speed = 1
    pwr = PWR(n, dim, n_initial_neutrons, speed)
    anim = Animator(pwr.update, interval=25)
    anim.animate()