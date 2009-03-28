from collections import defaultdict
from math import sqrt


class GridMap(object):
    """ Represents a rectangular grid map. The map consists of 
        nrows X ncols coordinates (squares). Some of the squares
        can be blocked (by obstacles).
    """
    def __init__(self, ncols, nrows):
        """ Create a new GridMap with the given amount of cols and rows.
        """
        self.nrows = nrows
        self.ncols = ncols
        
        self.map = [[0] * self.ncols for i in range(self.nrows)]
        self.blocked = defaultdict(lambda: False)
    
    def set_blocked(self, coord, blocked=True):
        """ Set the blocked state of a coordinate.
        @blocked: True for blocked, False for unblocked.
        """
        bx, by = coord
        try:
            self.map[by][bx] = blocked
        except IndexError:
            # Some sprite can be out of the level area
            return
    
        if blocked:
            self.blocked[coord] = True
        else:
            if coord in self.blocked:
                del self.blocked[coord]

    def set_blocked_multi(self, coords, blocked=True):
        """As set_blocked but to multiple coordinates"""
        for coord in coords:
            self.set_blocked(coord, blocked)
    
    def move_cost(self, c1, c2):
        """ Compute the cost of movement from one coordinate to
            another. 
            
            The cost is the Euclidean distance.
        """
        return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) 
    
    def successors(self, c):
        """ Compute the successors of coordinate 'c': all the 
            coordinates that can be reached by one step from 'c'.
        """
        slist = []
        
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue 
                    
                newrow = c[0] + drow
                newcol = c[1] + dcol
                if (    0 <= newrow <= self.nrows - 1 and
                        0 <= newcol <= self.ncols - 1 and
                        self.map[newrow][newcol] == 0):
                    slist.append((newrow, newcol))
        
        return slist
    
    def __str__(self):
        """Repr the map in ASCII"""
        st = ""
        for row in range(self.nrows):
            for col in range(self.ncols):
                st+= "%s" % ('O' if self.map[row][col] else '.')
            st+="\n"
        return st

