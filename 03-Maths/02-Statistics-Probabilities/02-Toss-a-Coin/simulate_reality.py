# pylint: disable=missing-docstring

import random
import numpy as np


def play_one_game(n_toss):
    '''TO DO: return the number of heads'''
    heads_counter = 0
    for toss in range(n_toss):
        if random.randint(0, 1) == 1:
            heads_counter +=1
    return heads_counter


def play_n_game(n_games, n_toss):
    '''TO DO: return a dictionary.
    The keys will be the possible head counts of each game
    The values will correspond to the probability of a game ending with that
     number of heads.
    '''
    head_counter = [play_one_game(n_toss) for game in range(n_games+1)]
    return dict(zip(np.arange(n_toss+1), np.bincount(head_counter, minlength=n_toss+1)/n_games))
