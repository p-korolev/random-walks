# Helper module for stats

import math
import numpy as np
import pandas as pd
import scipy.stats as S

from scipy.stats import norm
from typing import Union, List, Any

def convert_set_np(data_set: List[float]) -> np.ndarray:
    return np.array(data_set)

# Returns incremental list from 1 to size
def generate_X(size: int) -> list[int]:
    return list(range(1, size+1))

# Partinioning function for rolling calculations
def partition_set(lst: List, n: int) -> List[List[Any]]:
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
    if (len(lst)%n!=0):
        final_P.append(lst[index_border:])
    return final_P

def average(data_set: Union[List, pd.Series]) -> float:
    return sum(data_set)/len(data_set)

def variance(data_set: Union[List, pd.Series]) -> float:
    size = len(data_set)
    if size<2:
        return 0
    mean = average(data_set)
    s = 0
    for val in data_set:
        s += (val - mean)**2
    variance = s/(size-1)
    return variance

def sd(data_set: Union[List, pd.Series]) -> float:
    return math.sqrt(variance(data_set))

# Moving average using partitioning function
def sma(data_set: Union[List, pd.Series], period: int) -> tuple[list]:
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

def get_Ylistregress(X: list, Y: list[float]) -> list[float]:
    regbase = S.linregress(X, Y)
    b0, b1 = regbase.intercept, regbase.slope
    Y_reg = [(b0 + b1*x) for x in X]
    return Y_reg

def get_normal(value: float) -> float:
    return norm.cdf(value)
