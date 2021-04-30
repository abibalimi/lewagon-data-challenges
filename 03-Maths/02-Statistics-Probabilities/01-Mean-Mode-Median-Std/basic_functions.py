# pylint:disable=C0111,C0103
from collections import Counter

def my_mean(samples):
    return sum(samples)/len(samples)


def my_standard_deviation(samples):
    mean_ = my_mean(samples)
    squared_sum = sum([(x-mean_) ** 2 for x in samples])
    return (squared_sum/(len(samples) -1)) ** 0.5


def my_median(samples):
    samples.sort()
    mid = len(samples) // 2
    if len(samples) % 2 :
        return samples[mid]
    return (samples[mid-1]+samples[mid]) / 2


def my_mode(samples):
    compteur = Counter(samples)
    return [k for k, v in compteur.items() if v == compteur.most_common(1)[0][1]][0]
