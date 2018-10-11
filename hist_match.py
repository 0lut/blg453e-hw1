import numpy as np


def calculate_hist(x):
    bins = [np.sum(x == b) for b in range(256)]
    return np.array(bins)


def calculate_cdf(bins):
    A = np.sum(bins)
    cdf = [np.sum(bins[:i]) for i in range(1, len(bins)+1)] / A
    return cdf
