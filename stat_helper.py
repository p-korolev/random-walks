import math, numpy as np

# convert data_set[float] to np array
def convert_set_np(data_set: list[float]) -> np.ndarray:
    return np.array(data_set)

# generate X: returns list from 1 to size
def generate_X(size: int) -> list[int]:
    return list(range(1, size+1))

#helper partitioning function
def partition_set(lst: list, n: int) -> list[list]:
    '''Partitions list into n lists'''
    # pick up key indexing info
    length = len(lst)
    index_border = (length//n)*n
    
    # p: current partition, final_P: returned list
    p = []
    final_P = []
    for i in range(index_border):
        if ((i+1)%n) == 0:
            p.append(lst[i])
            final_P.append(p)
            p=[]
            continue
        if i+1%n != 0 or i==0:
            p.append(lst[i])   

    # Append then rest of the list if n !divides len(lst)  
    if (len(lst)%n!=0):
        final_P.append(lst[index_border:])

    return final_P

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

# get moving average given period
def sma(data_set: list[float], period: int) -> tuple[list]:
    '''Returns tuple where tuple[0] -> X axis, tuple[1] -> Y axis (Y[i] stores the SMA value after X[i] days for given period)'''
    # basic variables
    size = len(data_set)
    reversed_data = data_set[::-1]

    #partition data into periods
    split = partition_set(reversed_data, period)

    # get moving average X, Y values
    sma_Y, sma_X = [], []
    x_index = -1
    day_count = 0
    for partition in split:
        sma_Y.append(average(partition))
        day_count += len(split[x_index])
        sma_X.append(day_count)
        x_index -= 1

    # re-reverse moving average values 
    sma_Y = sma_Y[::-1]

    return sma_X, sma_Y

import scipy.stats as S
# return regression Y values given X, Y sets
def get_Ylistregress(X: list, Y: list[float]) -> list[float]:
    # load regression info
    regbase = S.linregress(X, Y)

    # pull function variables
    b0, b1 = regbase.intercept, regbase.slope

    # build and return Y_regression values list
    Y_reg = [(b0 + b1*x) for x in X]
    return Y_reg

# return normal index
from scipy.stats import norm
def get_normal(value: float) -> float:
    return norm.cdf(value)