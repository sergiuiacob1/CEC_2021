# We import the algorithm (You can use from pyade import * to import all of them)
import pyade.lshade
import numpy as np
import math


def callback(population_size, individual_size, bounds, func, opts, memory_size, callback, max_evals, seed, population,
             init_size, m_cr, m_f, archive, all_indexes, current_generation, num_evals, n, i, max_iters, r, cr, f, p,
             mutated, crossed, k, fitness, c_fitness, indexes, weights, new_population_size, best_indexes=None):
    print(f'Generation #{int(current_generation)}:')
    mean = np.mean(population)
    print(f'\tmean: {mean}')


def solve_with_LSHADE(input_params):
    # You may want to use a variable so its easier to change it if we want
    algorithm = pyade.lshade

    # We get default parameters for a problem with two variables
    lshade_params = algorithm.get_default_params(dim=input_params['ndim'])
    lshade_params['bounds'] = np.array(input_params['bounds'])
    lshade_params['func'] = input_params['function']
    lshade_params['callback'] = callback

    solution, fitness = algorithm.apply(**lshade_params)
    print(f'Solution: {solution}, fitness: {fitness}')

    f_value = input_params['function'](solution)

    return {'f_value': f_value, 'solution': solution}
