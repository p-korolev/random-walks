import numpy as np

from numbers import Real

class Interval:
    def __init__(self, 
                 lower_bound: Real, 
                 upper_bound: Real, 
                 lower_inclusive: bool = True, 
                 upper_inclusive: bool = True):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.lower_inclusive = lower_inclusive
        self.upper_inclusive = upper_inclusive

    def __repr__(self):
        return [self.lower_bound, self.upper_bound]
    
    def __str__(self):
        return f"Interval [{self.lower_bound}, {self.upper_bound}]"

    def get_lower_bound(self):
        return self.lower_bound
    
    def get_upper_bound(self):
        return self.upper_bound
    
    def to_np(self):
        return np.ndarray(self)

