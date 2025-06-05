import math, random as rd, stat_helper as sh, matplotlib.pyplot as plt

class Walk():
    def __init__(self, start_val: float):
        self.size = 1                                # initial size
        self.start = start_val                       # walk start value
        self.current_walk = [start_val]              # initial walk path (start value)
        self.current_value = start_val               # initial last appended step position
        
        # will update once walk gets generated
        self.add_interval = None 
        self.add_probability = None
        self.float_steps = False 

    # view current walk path
    def view_walk(self) -> list:
        return self.current_walk
    
    # get current walk size
    def get_size(self) -> int:
        return self.size
    
    # generate walk beginning at current value
    def generate_walk(self, num_steps: int, add_interval: list = [1, 1], 
                      add_probability: float = 0.5, uniform: bool = False) -> None:
        '''Custom add_interval format: [0, x]'''
        # update walk characteristics
        self.size += num_steps
        self.add_interval = add_interval
        self.add_probability = add_probability
        self.float_steps = uniform

        # for validation
        count_over, count_under = 0, 0
        # generate walk
        for step in range(num_steps):
            # get +/- decision
            decision = rd.uniform(0,1)

            # if interval subset Z
            if (uniform):
                # generate random +/- value
                random_val = rd.uniform(add_interval[0], add_interval[1])
                # if decision within add_probability, add radom value
                # else, subtract
                if decision<add_probability:
                    count_under += 1
                    self.current_walk.append(self.current_value + random_val)
                    self.current_value = self.current_walk[-1]
                else:
                    count_over += 1
                    self.current_walk.append(self.current_value - random_val)
                    self.current_value = self.current_walk[-1]

            # if interval subset R
            if (not uniform):
                random_val = rd.randint(add_interval[0], add_interval[1])
                if decision<add_probability:
                    self.current_walk.append(self.current_value + random_val)
                    self.current_value = self.current_walk[-1]
                else:
                    self.current_walk.append(self.current_value - random_val) 
                    self.current_value = self.current_walk[-1]
        
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
    def get_stepdiff(self) -> list[float]:
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
    def get_step_direction(self) -> list[float]:
        diff = self.get_stepdiff()
        directions = []
        for value in diff:
            directions.append(value/abs(value))
        return directions
        
    # plot current walk and walk attributes
    def plot_walk(self, linemarker: bool = True,
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


