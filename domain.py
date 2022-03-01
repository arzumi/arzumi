"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """
    A package to be delivered by trucks.

    === Public Attributes ===
    id: The ID of the parcel
    volume: The volume of the parcel
    source: The origin of the parcel
    destination: The place where the pracel will be delivered

    === Representation Invariants ===
    volume >= 0
    source and destination must be string objects, and they are
    valid cities that exist on Earth

    === Sample Usage ===
    initialize the class
    >>> p1 = Parcel(1, 5, 'Vancouver', 'Toronto')

    >>> p1.id
    1
    >>> p1.volume
    5
    >>> p1.source
    'Vancouver'
    >>> p1.destination
    'Toronto'
    """

    # Attribute type
    id: int
    volume: int
    source: str
    destination: str

    def __init__(self, p_id: int, volume: int, source: str,
                 destination: str) -> None:
        """
        Initialize the class.
        >>> p1 = Parcel(1, 5, 'Vancouver', 'Toronto')
        >>> p1.id
        1
        >>> p1.volume
        5
        >>> p1.source
        'Vancouver'
        >>> p1.destination
        'Toronto'
        """
        self.id = p_id
        self.volume = volume
        self.source = source
        self.destination = destination


class Truck:
    """
    A vehicle that carries parcels.

    === Public Attributes ===
    id: The ID of the truck.
    volume: The amount of volume that the truck can store.
    depot: The starting location of the truck.
    parcel_lst: A list that stores the parcel objects.
    route: A list of locations that trucks need to go
    available_space: Available space for the truck
    """

    # Attribute types
    id: int
    volume: int
    depot: str
    parcel_lst: List[Parcel]
    route: List[str]
    available_space: int

    def __init__(self, t_id: int, volume: int, depot: str) -> None:
        """
        Initialize the class.
        >>> t1 = Truck(1, 6, 'Toronto')
        >>> t1.id
        1
        >>> t1.volume
        6
        >>> t1.depot
        'Toronto'
        >>> t1.parcel_lst
        []
        >>> t1.route
        ['Toronto']
        """
        self.id = t_id
        self.volume = volume
        self.depot = depot
        self.parcel_lst = []
        self.route = [self.depot]
        self.available_space = volume

    def pack(self, p: Parcel) -> bool:
        """
        Return true if we have successfully packed the parcel
        in the truck, false otherwise.

        >>> t1 = Truck(1, 6, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Vancouver')
        >>> p2 = Parcel(1, 2, 'Brampton', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        False
        """
        curr_parvol = 0
        for parcel in self.parcel_lst:
            curr_parvol += parcel.volume
        if self.volume >= (curr_parvol + p.volume):
            self.parcel_lst.append(p)
            self.available_space -= p.volume
            if self.route[-1] != p.destination:
                self.route.append(p.destination)
            return True
        return False

    def fullness(self) -> float:
        """
        Return the percentage of the fullness of the truck,
        that is: total volume of all parcels/capacity of the truck.

        >>> t1 = Truck(1, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Vancouver', 'Toronto')

        >>> t1.pack(p1)
        True
        >>> t1.fullness()
        50.0
        """
        parvol = 0.0
        for p in self.parcel_lst:
            parvol += p.volume
        return (parvol / self.volume) * 100.0


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        result = ''
        for truck in self.trucks:
            data = ''
            for parcel in truck.parcel_lst:
                data += 'Parcel_id: ' + \
                        str(parcel.id) + ' ' + 'Parcel_vol: ' + \
                        str(parcel.volume) + ' ' + 'Parcel_source: ' + \
                        str(parcel.source) + ' ' + 'Parcel_destination: ' + \
                        str(parcel.destination) + '\n'
            result += 'Truck_id: ' + str(truck.id) + ' ' + 'Volume: ' + \
                      str(truck.volume) + ' ' + 'Depot: ' + \
                      str(truck.depot) + '\n' + data
        return result.strip()

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        count = 0
        for truck in self.trucks:
            if truck.volume > truck.available_space:
                count += 1
        return count

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        result = {}
        for t in self.trucks:
            if t.id not in result:
                result[t.id] = []
                for p in t.parcel_lst:
                    result[t.id].append(p.id)
        return result

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        result_p = 0
        result_t = 0
        used_trucks = []
        for t in self.trucks:
            if len(t.parcel_lst) > 0:
                used_trucks.append(t)
        for t in used_trucks:
            for p in t.parcel_lst:
                result_p += p.volume
        for t in used_trucks:
            result_t += t.volume
        return result_t - result_p

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        result = 0.0
        for t in self.trucks:
            result += t.fullness()
        return result

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        count = 0.0
        for t in self.trucks:
            if t.fullness() != 0.0:
                count += 1
        return self._total_fullness() / count

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36

        #our example to calculate truck's route with more than one destination
        >>> t3 = Truck(1444, 10, 'Toronto')
        >>> p3 = Parcel(3, 5, 'Toronto', 'Hamilton')
        >>> p4 = Parcel(4, 5, 'Ajax', 'Oakville')
        >>> t3.pack(p3)
        True
        >>> t3.pack(p4)
        True
        >>> m.add_distance('Hamilton', 'Oakville', 10, 12)
        >>> m.add_distance('Toronto', 'Oakville', 15, 20)
        >>> h = Fleet()
        >>> h.add_truck(t3)
        >>> h.total_distance_travelled(m)
        39
        """
        result = 0
        for truck in self.trucks:
            if len(truck.route) > 1:
                result += dmap.distance(truck.route[-1], truck.route[0])
                j = 1
                for i in range(len(truck.route) - 1):
                    result += dmap.distance(truck.route[i], truck.route[j])
                    j += 1

        return result

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        count = 0.0
        for f in self.trucks:
            if len(f.parcel_lst) != 0:
                count += 1
        return self.total_distance_travelled(dmap) / count


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
