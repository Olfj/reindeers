from Animator import Animator
from ReactorSingleCollision import PWR
import numpy as np

if __name__ ==  "__main__":
    n = 1
    dim = 5
    n_initial_neutrons = 1
    speed = 0.06
    seed = 42
    pwr = PWR(n, dim, n_initial_neutrons, speed, seed=seed)
    anim = Animator(pwr.update, interval=25, save=True, fps=20, frames=50, name='single collision')
    anim.animate()