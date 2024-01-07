# code for codingame autumn challenge
# refactoring older version of silver.py


# import references
import sys,math
from typing import List, NamedTuple, Dict
from dataclasses import dataclass

# generic classes
# Vector - x,y coordinates
# Polygon - list of vectors representing the x,y coordinates of the edges in order - first and last item should be the same


# classes to hold objects

# game class - overall object holding the state for a particular game turn, holds turn, value and creature

# shoal class
#   creature class
# team class 
#   drone class


# useful functions
def point_in_polygon(polygon, point) ->bool:
    """
    Raycasting Algorithm to find out whether a point is in a given polygon.
    Performs the even-odd-rule Algorithm to find out whether a point is in a given polygon.
    This runs in O(n) where n is the number of edges of the polygon.
     *
    :param polygon: an array representation of the polygon where polygon[i][0] is the x Value of the i-th point and polygon[i][1] is the y Value.
    :param point:   an array representation of the point where point[0] is its x Value and point[1] is its y Value
    :return: whether the point is in the polygon (not on the edge, just turn < into <= and > into >= for that)
    """

    # A point is in a polygon if a line from the point to infinity crosses the polygon an odd number of times
    odd = False
    # For each edge (In this case for each point of the polygon and the previous one)
    i = 0
    j = len(polygon) - 1
    while i < len(polygon) - 1:
        i = i + 1
        # If a line from the point into infinity crosses this edge
        # One point needs to be above, one below our y coordinate
        # ...and the edge doesn't cross our Y corrdinate before our x coordinate (but between our x coordinate and infinity)

        if (((polygon[i][1] > point[1]) != (polygon[j][1] > point[1])) and (point[0] < (
                (polygon[j][0] - polygon[i][0]) * (point[1] - polygon[i][1]) / (polygon[j][1] - polygon[i][1])) +
                                                                            polygon[i][0])):
            # Invert odd
            odd = not odd
        j = i
    # If the number of crossings was odd, the point is in the polygon
    return odd


# initiate game

# create required lists and dict


# initiate turn
# clear objects that are round specific
# store input values
# update object attributes based on inputs and previous round info

# list possible next steps

# value game state after each possible next step

# choose best value next step

# print debug info to error stream

# print game outputs
