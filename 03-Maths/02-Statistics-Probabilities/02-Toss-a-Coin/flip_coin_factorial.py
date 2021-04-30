# pylint: disable=missing-docstring

import math


def count_possibilities(n_toss, n_heads):
    return math.factorial(n_toss)/(math.factorial(n_heads)*math.factorial(n_toss - n_heads))


def count_total_possibilities(n_toss):
    return 2 ** n_toss


def probability(n_toss):
    proba = {}
    for toss in range(n_toss+1):
        print(f'{toss}: {count_possibilities(n_toss, toss)/count_total_possibilities(n_toss)}')
        proba[toss] = count_possibilities(n_toss, toss)/count_total_possibilities(n_toss)
    return proba
