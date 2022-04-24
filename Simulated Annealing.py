from numpy.random import rand,randn
from numpy import asarray
from random import seed
from math import exp

def objective(x):
    return x[0]**2.0

def annealer(objective, bounds, n_iterations, step_size,initial_temp):
    best_point=bounds[:,0] + rand(len(bounds)) * (bounds[:,1] - bounds[:,0])
    best_value=objective(best_point)
    current_point,current_value=best_point,best_value

    for i in range(n_iterations):
        new_point=current_point + randn(len(bounds)) * step_size
        new_value=objective(new_point)

        if new_value < best_value:
            best_point,best_value=new_point,new_value
            print(f'{i} -> f({best_point}) = {best_value}')

        difference=new_value-current_value
        temperature=initial_temp/(i+1)
        metropolis_acceptance=exp(-difference/temperature)
        if difference < 0 and rand() < metropolis_acceptance:
            current_point,current_value=new_point,new_value
    return [best_point,best_value]

bounds = asarray([[-5.0, 5.0]])
n_iterations = 1000
step_size = 0.1
initial_temp=10
bp,bv=annealer(objective, bounds, n_iterations, step_size,initial_temp)
print(bp,bv)