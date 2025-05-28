import math, numpy as np

#get mean of sample
def average(data_set: list[float]) -> float:
    avg = sum(data_set)/len(data_set)
    return avg

# get variance of data set
def variance(data_set: list[float]) -> float:
    # sample size
    size = len(data_set)

    # base check
    if size<2:
        return 0
    
    # get mean
    mean = average(data_set)
    s = 0
    for val in data_set:
        s += (val - mean)**2
    variance = s/(size-1)
    return variance

# get standard devation of data set
def sd(data_set: list[float]) -> float:
    variance = variance(data_set)
    return math.sqrt(variance)

# generate X: returns list from 1 to size
def generate_X(size: int) -> list[int]:
    return list(range(1, size+1))

# get moving average given period
def sma(data_set: list[float], period: int) -> tuple[list]:
    '''Returns tuple where tuple[0] -> X axis, tuple[1] -> Y axis'''
    import partition
    # basic variables
    size = len(data_set)
    reversed_data = data_set[::-1]
    split = partition.partition_set(reversed_data, period)

    # get moving average values
    sma_Y = []
    for partition in split:
        sma_Y.append(average(partition))

    # re-reverse
    sma_Y = sma_Y[::-1]

    # get respective X values
    sma_X = []
    X = generate_X(size)
    for x in X:
        if x%period==0:
            sma_X.append(x)

    return sma_X, sma_Y

# convert data_set[float] to np array
def convert_set_np(data_set: list[float]) -> np.ndarray:
    return np.array(data_set)

# return normal index
from scipy.stats import norm
def get_normal(value: float) -> float:
    return norm.cdf(value)

