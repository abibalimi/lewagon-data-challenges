# pylint: disable=missing-docstring

import numpy as np
from flip_coin_factorial import probability
from simulate_reality import play_n_game



def mean_squared_error(n_games, n_toss):
    '''TO DO: return the squared error between the theoretical and "actual"
     results (obtained through simulation)'''
    #probas = np.array(list(probability(n_toss).values()))
    #n_games_probas = np.array(list(play_n_game(n_games, n_toss).values()))
    #return np.square(probas - n_games_probas).mean()
    #def mean_squared_error(n_games, n_toss):
    #'''TO DO: return the squared error between the theoretical and "actual" results (obtained through simulation)'''
    theoretical_results = probability(n_toss)
    actual_results = play_n_game(n_games, n_toss)
    squared_error = 0
    for k, v in theoretical_results.items():
        actual_result = actual_results[k]
        squared_error += (actual_result - theoretical_results[k])**2
    mse = squared_error/len(theoretical_results)
    return mse
