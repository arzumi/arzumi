"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict, List


class DistanceMap:
    """
    A Map class that stores the distance between two cities, back and forth

    === Private Attributes ===
    _map: a dictionary that stores the starting city and the destination
     as a key, and the distance between the two cities as the value

    === Representation Invariants ===
    The location must a string object, and it must exist on Earth

    === Sample usage ===
    test the initializer
    >>> map1 = DistanceMap()
    >>> map1._map
    {}
    """
    # Attribute type
    _map: Dict[str, List[int]]

    def __init__(self) -> None:
        """
        Initialize the class
        >>> m1 = DistanceMap()
        >>> m1._map
        {}
        """
        self._map = {}

    def add_distance(self, city1: str, city2: str, dist1: int,
                     dist2: int = 0) -> None:
        """
        Add the starting city, the destination, and
        the distance between the two cities into the map.

        >>> map1 = DistanceMap()
        >>> map1.add_distance('Toronto', 'Hamilton', 9)
        >>> print(map1._map)
        {'Toronto - Hamilton': [9, 9]}

        >>> map2 = DistanceMap()
        >>> map2.add_distance('Vancouver', 'Toronto', 9, 10)
        >>> print(map2._map)
        {'Vancouver - Toronto': [9, 10]}
        """
        key = city1 + " - " + city2
        if key not in self._map:
            self._map[key] = []
            if dist2 != 0:
                self._map[key].append(dist1)
                self._map[key].append(dist2)
            else:
                self._map[key].append(dist1)
                self._map[key].append(dist1)

    def distance(self, city1: str, city2: str) -> int:
        """
        Return the distance from city1 to city2.

        >>> map1 = DistanceMap()
        >>> map1.add_distance('Toronto', 'Hamilton', 9)
        >>> map1.add_distance('Vancouver', 'Toronto', 9, 10)

        >>> map1.distance('Toronto', 'Hamilton')
        9
        >>> map1.distance('Vancouver', 'Toronto')
        9
        >>> map1.distance('Toronto', 'Vancouver')
        10
        """
        key1 = city1 + " - " + city2
        key2 = city2 + " - " + city1

        if city1 == city2:
            return 0

        if (key1 not in self._map) and (key2 not in self._map):
            return -1

        if (key1 not in self._map) and (key2 in self._map):
            return self._map[key2][1]

        return self._map[key1][0]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
