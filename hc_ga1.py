import math
from math import sin, cos
import operator
import random, time
import copy
import numpy as np
from geneticalgorithm import geneticalgorithm as ga

def solve_with_GA(params):
    # algorithm = AlgorithmGaBihc([params['function'],params['bounds'][0]],params['maxFes'],dimensions=params['dimensions'],steps=10000,popSize=100)
    # try:
    #     _explored_points = algorithm.run()
    # except Exception as _:
    #     pass    
    # return {'f_value': algorithm.be, 'solution': algorithm.bv}
    alg = ga(function=params['function'],dimension=params['ndim'],variable_type='real',variable_boundaries=np.array(params['bounds']),algorithm_parameters={
                                       'max_num_iteration': 100000,\
                                       'population_size':100,\
                                       'mutation_probability':0.1,\
                                       'elit_ratio': 0.01,\
                                       'crossover_probability': 0.5,\
                                       'parents_portion': 0.3,\
                                       'crossover_type':'uniform',\
                                       'max_iteration_without_improv':None})
    alg.run()
    return {'f_value': alg.best_function, 'solution': alg.best_variable}