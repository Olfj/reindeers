from Animator import Animator
from Reactor import PWR
import numpy as np

if __name__ ==  "__main__":
    n = 100
    dim = 100
    n_initial_neutrons = 200
    speed = 1
    seed = 42
    pwr = PWR(n, dim, n_initial_neutrons, speed, seed=seed)
    anim = Animator(pwr.update, interval=25)
    anim.animate()