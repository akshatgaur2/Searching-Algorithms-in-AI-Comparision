from numpy import asarray
from numpy.random import randn, rand


def objective(x):
    return x[0] ** 2.0


def hillclimbing(objective, bounds, n_iterations, step_size):
    initial_point = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
    initial_val = objective(initial_point)
    for i in range(n_iterations):
        new_point = initial_point + randn(len(bounds)) * step_size
        new_val = objective(new_point)
        if new_val <= initial_val:
            initial_point, initial_val = new_point, new_val
            print(f'{i} -> f({initial_point}) = {initial_val}')
    return [initial_point, initial_val]


def Evolution_Global_Optimization():
    pass


def Basin_Hopping_Optimization():
    pass


def Simulated_Annealing():
    pass


def BFGS():
    pass


def Nelder_Mead():
    pass


def Particle_Swarm_Optimization():
    pass


def Simple_Genetic_Algorithm():
    pass


bounds = asarray([[-5.0, 5.0]])
n_iterations = 1000
step_size = 0.1
hillclimbing(objective, bounds, n_iterations, step_size)
