import numpy as np

class Interval():
    '''
    Basic object that enables interval set usability and readability.

    **Usage**

    Creating interval [-1, 1]:

    >>> I = Interval(lower_bound=-1, upper_bound=1)

    Accessing lower bound:

    >>> I.get_lower_bound()
    '''

    def __init__(self, lower_bound: float, upper_bound: float, lower_inclusive: bool = True, upper_inclusive: bool = True):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.lower_inclusive = lower_inclusive
        self.upper_inclusive = upper_inclusive

    def __repr__(self):
        '''
        Returns list set display of interval assuming element inclusivity stays True always.
        '''
        return [self.lower_bound, self.upper_bound]
    
    def __str__(self):
        return f"Interval [{self.lower_bound}, {self.upper_bound}]"

    def get_lower_bound(self):
        return self.lower_bound
    
    def get_upper_bound(self):
        return self.upper_bound
    
    def to_np(self):
        return np.ndarray(self)