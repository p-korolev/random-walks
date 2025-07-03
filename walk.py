import math
import random as rd
import stat_helper as sh
import matplotlib.pyplot as plt
import numpy as np

from interval import Interval 
from typing import Union, List, Any

class Walk():
    def __init__(self,
                 size: int = 0, 
                 start_val: float = None,
                 add_interval: Interval = None,
                 add_probability: float = None,
                 uniform_random: bool = True):
        '''
        Creates a random walk using generate_walk. Walk stored in current_walk as a list.

        :param size: Number of steps in the walk.
        :param start_val: Starting value: current_walk[0].
        :param add_interval: Interval to take next random additive step.
        :param add_probability: Probability that we step forward.
        :param uniform_random: True if random values should come from Reals. False for Integers.
        '''       
        # handle missing parameters when selected walk size>0
        if (size!=0 and (start_val==None or add_interval == None or add_probability==None)):
            raise Exception("Missing Parameters.")

        # initalize attributes
        self.start = start_val                       # walk start value
        self.current_walk = [start_val]              # initial walk path (start value)
        self.size = 1                                # current size before generating walk
        if size == 0: self.size = 0
        self.current_value = start_val               # initial last appended step position
        self.add_interval = add_interval
        self.add_probability = add_probability
        self.float_steps = uniform_random

        # generate walk given walk parameters
        self.generate_walk(num_steps=size, 
                           add_interval=add_interval,
                           add_probability=add_probability,
                           uniform=uniform_random)

    # view current walk path
    def view_walk(self) -> List[float]:
        return self.current_walk
    
    def view_walk_np(self) -> np.ndarray:
        return np.ndarray(self.current_walk)

    # get current walk size
    def get_size(self) -> int:
        return self.size
    
    # generate walk beginning at current value
    def generate_walk(self, num_steps: int, add_interval: Interval = Interval(-1,1), add_probability: float = 0.5, uniform: bool = False) -> None:
        '''
        Generates walk given parameters and updates object attributes.

        :param num_steps: Number of steps in the walk.
        :param add_interval: Interval to take next random additive step.
        :param add_probability: Probability that we step forward.
        :param uniform: True if random values should come from Reals. False for Integers.

        **Usage**

        Generate a 100 step walk starting at self.start, adding a random value d in D = [-4.56, 5.88] (subset of R) with probability 72%, while
        subtracting the value with probability 1 - 72%:

        >>> interval = Interval(-4.56, 5.88)

        >>> self.generate_walk(num_steps=100, add_interval=interval, add_probability=0.72, uniform=True)
        '''
       
        # for validation
        count_over, count_under = 0, 0
        # generate walk
        for step in range(num_steps - 1):
            # get +/- decision
            decision = rd.uniform(0,1)

            # if interval subset R
            if (uniform):
                # generate random +/- value
                random_val = rd.uniform(add_interval.get_lower_bound(), add_interval.get_upper_bound())
                # if decision within add_probability, add radom value
                # else, subtract
                if decision<add_probability:
                    count_under += 1

                    # append new step
                    self.current_walk.append(self.current_value + random_val)

                    # update current step
                    self.current_value = self.current_walk[-1]

                    # update size
                    self.size += 1
                else:
                    count_over += 1
                    self.current_walk.append(self.current_value - random_val)
                    self.current_value = self.current_walk[-1]
                    self.size += 1

            # if interval subset Z
            if (not uniform):
                random_val = rd.randint(add_interval.get_lower_bound(), add_interval.get_upper_bound())
                if decision<add_probability:
                    self.current_walk.append(self.current_value + random_val)
                    self.current_value = self.current_walk[-1]
                    self.size += 1
                else:
                    self.current_walk.append(self.current_value - random_val) 
                    self.current_value = self.current_walk[-1]
                    self.size += 1
        
    # re-generate walk beginning at start value
    def regenerate_walk(self) -> None:
        # save previous values
        last_walk_steps = self.size - 1

        #re-initialize values
        self.size = 1           
        self.current_walk = [self.start]
        self.current_value = self.start             
        
        # generate new walk and override
        self.generate_walk(num_steps =  last_walk_steps, 
                           add_interval = self.add_interval,
                           add_probability = self.add_probability,
                           uniform = self.float_steps)

    # get step differences
    # return list will be of size n-1, if size(walk) = n
    def get_stepdiff(self) -> List[float]:
        # base case
        if (self.size<2):
            return None

        stepdiff = []
        # traverse walk and append difference to next step
        for step_index in range(self.size - 1):
            stepdiff.append(self.current_walk[step_index + 1] - self.current_walk[step_index])
        
        # return stepdiff, len = n-1
        return stepdiff
    
    # return list of new step's direction, 1: up, -1: down
    def get_step_direction(self) -> List[float]:
        diff = self.get_stepdiff()
        directions = []
        for value in diff:
            directions.append(value/abs(value))
        return directions
        
    # plot current walk and walk attributes
    def plot_walk(self, 
                  linemarker: bool = True,
                  show_sma: bool = False, 
                  sma_period: int = None, 
                  show_running_variance: bool = False, 
                  show_volatility: bool = False) -> None:
        color = ["steelblue", "turquoise", "mediumvioletred", "darkviolet"]

        # plot walk
        X = sh.generate_X(self.size)
        Y = self.current_walk 
        if linemarker: plt.plot(X, Y, color=color[0], marker='o', label="Walk") 
        else: plt.plot(X, Y, color=color[0], label="Walk")

        # plot moving average
        if (show_sma):
            # generate (X: period accounted, Y: average for period)
            sma_tuple = sh.sma(self.current_walk, sma_period)
            
            # pull X, Y independently
            sma_X = sma_tuple[0] 
            sma_Y = sma_tuple[1]

            # plot moving average
            plt.plot(sma_X, sma_Y, color = color[1], label="Simple Moving Average")
        
        # plot running variance
        if (show_running_variance):
            var_list = []
            seen = []
            for step in self.current_walk:
                seen.append(step)

                # calculate current variance
                var_list.append(sh.variance(seen))
            # plot running variance
            plt.plot(X, var_list, color=color[2], label="Variance")

        # plot volatility (standard dev)
        if (show_volatility):
            vol_list = []
            seen = []
            for step in self.current_walk:
                seen.append(step)

                # calculate current volatility = sqrt(variance)
                vol_list.append(math.sqrt(sh.variance(seen)))
            # plot running volatility (sd)
            plt.plot(X, vol_list, color=color[3], label="Volatility (sd)")

        plt.legend()
        plt.show()
