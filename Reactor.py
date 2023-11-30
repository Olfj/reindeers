import numpy as np
from Animator import Animator, Plotter

class PWR:

    COLLISION_ENERGY = 200 * 1.602 * 10e-13
    HEAT_CAPACITY = 4.184
    BASE_TEMPERATURE = 548
    FLOW = 4.97 * 10e-13
    VOLUME =  59.47 * 10e-13
    REACTION_PROB = 0.85
    CONTROL_ROD_ABSORB = 0.01
    CONTROL_ROD_INSERTION_RATE = 1.0015

    def __init__(self, n, dim, n_neutrons, speed, rng, n_blocks=10):
        ''' n_neutrons: number of initial neutrons '''
        self.radius = 0.75
        self.n = n
        self.dim = dim
        self.speed = speed
        self.block_size = int(dim / n_blocks)
        self.atoms = rng.uniform(0, self.dim, size=(self.n, 2))
        self.collided  = np.zeros((self.n))
        self.neutrons = rng.uniform(0, self.dim, size=(n_neutrons, 2))
        self.directions = rng.uniform(0, 2*np.pi, size=n_neutrons)
        colors = "green blue".split()
        self.plotter = Plotter(custom=colors)
        self.atom_table = self.init_atom_table()
        self.reaction_prob = self.REACTION_PROB
        self.temperature = self.BASE_TEMPERATURE
        self.n_old_neutrons = n_neutrons
        self.control_rod_absorb = self.CONTROL_ROD_ABSORB 

    def init_atom_table(self):
        '''Partitions the world. Used to store atoms'''
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
        '''Returns a list of atoms that are possible collision prospects'''
        floored_pos = tuple(np.floor(position / self.block_size).astype(int))
        collidable = self.atom_table.get(floored_pos)
        return collidable if collidable else []

    def update(self, i):
        self.plot(i)
        self.n_old_neutrons = len(self.neutrons)
        self.absorb()
        self.move_neutrons()
        energy = self.collide()
        self.adjust_temperature(energy)
        self.adjust_reaction_prob()
        self.adjust_control_rods()


    def plot(self, i):
        '''Plots the neutrons and atoms'''
        lim = (0, self.dim)
        atoms = self.atoms[np.nonzero(self.collided == 0)[0]]
        self.plotter.scatter(self.atoms[:,0], self.atoms[:,1], lim, lim, c=0)
        self.plotter.scatter(self.neutrons[:,0], self.neutrons[:,1], lim, lim, redraw=False, s=10, c=1)
        stats = f"Generation: {i+1}, temperature: {self.temperature:.4f}, reactivity: {self.get_reactivity():.4f}"
        self.plotter.show_stats(stats)

    def move_neutrons(self):
        '''Move all neutrons'''
        direction = np.array([np.cos(self.directions), np.sin(self.directions)]).T
        self.neutrons += self.speed * direction

    def collide(self):
        '''Collision detection'''
        new_positions = self.neutrons.copy()
        new_directions = self.directions.copy()
        energy = 0

        for i, neutron in enumerate(self.neutrons):
            collidable = self.get_collidable(neutron)
            for index in collidable:
                if self.norm(self.atoms[index] - neutron) < self.radius:# and self.collided[index] == 0:
                    if np.random.rand() < self.reaction_prob:
                        dirs = np.random.uniform(0, 2*np.pi, 2)
                        poss = np.full((2,2), self.atoms[index]) + 1.1 * self.radius * np.array([np.cos(dirs), np.sin(dirs)]).T
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
        rand = np.random.rand(len(self.neutrons))
        mask = np.nonzero(rand < self.control_rod_absorb)[0]
        self.neutrons = np.delete(self.neutrons, mask, axis=0)
        self.directions = np.delete(self.directions, mask)

    def adjust_temperature(self, energy):
        ''''Change in water temperature as a function of fission and flow'''
        self.temperature = self.BASE_TEMPERATURE + energy / (self.HEAT_CAPACITY * (self.VOLUME - self.FLOW))
        #self.temperature = (self.VOLUME * temp + self.FLOW * self.BASE_TEMPERATURE) / self.VOLUME

    def adjust_reaction_prob(self):
        '''Adjusts the probability of fission as a function of water temperature'''
        self.reaction_prob = self.REACTION_PROB * self.BASE_TEMPERATURE / self.temperature

    def adjust_control_rods(self):
        '''Increases likelihood of absorbtion by moving control rods a little'''
        insertion = self.control_rod_absorb * self.CONTROL_ROD_INSERTION_RATE
        self.control_rod_absorb = min(insertion, 0.023)#0.02272)

    def get_reactivity(self):
        '''Returns the reactivity'''
        if self.n_old_neutrons == 0:
            return 0
        else:
            return len(self.neutrons) / self.n_old_neutrons
        
    def norm(self, u):
        '''Length of a vector'''
        return np.sqrt((u * u).sum())

if __name__ ==  "__main__":
    n = 100
    dim = 100
    n_initial_neutrons = 200
    speed = 1
    rng = np.random.default_rng(seed=42)
    pwr = PWR(n, dim, n_initial_neutrons, speed, rng)
    anim = Animator(pwr.update, interval=25)
    anim.animate()