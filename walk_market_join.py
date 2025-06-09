from walk import Walk
import price_data_config as pconfig
import stat_helper as S


class List(list):
    def is_empty(self):
        return len(self) == 0
    
    def to_walk(self):
        '''
        Given a list of points [x1, x2, ..., xn], convert it to a Walk object and store points in lst as the current walk.

        *Usage*

        Convert list L into a walk:

        >>> L = [1,3,5,7,9,11]
        >>> list_to_walk(L)
        '''
        # walk stored here
        walk = Walk()

        # fill attributes
        if (self.is_empty()):
            raise Exception("List is empty, cannot complete walk.")
        walk.start = self[0]
        walk.current_walk = self
        walk.size = len(self)
        walk.current_value = self[-1]
        



def list_to_walk(lst: list):
    '''
    Given a list of points [x1, x2, ..., xn], convert it to a Walk object and store points in lst as the current walk.

    *Usage*

    Convert list L into a walk:

    >>> L = [1,3,5,7,9,11]
    >>> list_to_walk(L)
    '''

    pass

