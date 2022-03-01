"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Optional
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """
    A scheduler that assigns a random parcel to
    a random truck.
    """
    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Assign the random parcel to a random truck"""

        result = []
        new_parcels = parcels[:]
        shuffle(new_parcels)

        for parcel in new_parcels:
            temp_truck_lst = []
            random_truck = choice(trucks)

            while len(trucks) > 0 and not random_truck.pack(parcel):
                temp_truck_lst.append(random_truck)
                trucks.remove(random_truck)
                if len(trucks) > 0:
                    random_truck = choice(trucks)

            if not trucks:
                result.append(parcel)

            for truck in temp_truck_lst:
                trucks.append(truck)

        return result


def _parcel_small_volume(item1: Parcel, item2: Parcel) -> bool:
    """
    Return true if <item1> has less volume than <item2>.
    >>> item1_ = Parcel(1, 5, 'Toronto', 'Hamilton')
    >>> item2_ = Parcel(2, 6, 'Toronto', 'Hamilton')
    >>> _parcel_small_volume(item1_, item2_)
    True
    >>> item3_ = Parcel(3, 20, 'Toronto', 'Hamilton')
    >>> item4_ = Parcel(4, 6, 'Toronto', 'Hamilton')
    >>> _parcel_small_volume(item3_, item4_)
    False
    """
    return item1.volume < item2.volume


def _parcel_large_volume(item1: Parcel, item2: Parcel) -> bool:
    """
    Return true if <item1> has larger volume than <item2>.
    >>> item5_ = Parcel(5, 7, 'Toronto', 'Hamilton')
    >>> item6_ = Parcel(6, 6, 'Vancouver', 'Hamilton')
    >>> _parcel_large_volume(item5_, item6_)
    True
    >>> item7_ = Parcel(7, 20, 'Toronto', 'Hamilton')
    >>> item8_ = Parcel(8, 60, 'Vancouver', 'Hamilton')
    >>> _parcel_large_volume(item7_, item8_)
    False
    """
    return item1.volume > item2.volume


def _parcel_small_des(item1: Parcel, item2: Parcel) -> bool:
    """
    Return true if <item1> has less characters
     in its destination than <item2>.
    >>> item1_ = Parcel(9, 5, 'Hamilton', 'Toronto')
    >>> item2_ = Parcel(10, 6, 'Hamilton','Vancouver')
    >>> _parcel_small_des(item1_, item2_)
    True
    >>> item3_ = Parcel(11, 20, 'Vancouver', 'Toronto')
    >>> item4_ = Parcel(12, 6, 'Oakville', 'Ajax')
    >>> _parcel_small_des(item3_, item4_)
    False
    """
    return item1.destination < item2.destination


def _parcel_large_des(item1: Parcel, item2: Parcel) -> bool:
    """
    Return true if <item1> has more characters
     in its destination than <item2>.
    >>> item1_ = Parcel(13, 5, 'Toronto', 'York')
    >>> item2_ = Parcel(14, 6, 'Vancouver', 'Brampton')
    >>> _parcel_large_des(item1_, item2_)
    True
    >>> item3_ = Parcel(15, 20, 'Toronto', 'Oakville')
    >>> item4_ = Parcel(16, 6, 'Ajax', 'Toronto')
    >>> _parcel_large_des(item3_, item4_)
    False
    """
    return item1.destination > item2.destination


def _truck_most_space(item1: Truck, item2: Truck) -> bool:
    """
    Return true if <item1> has more capacity than <item2>.
    >>> t1 = Truck(1423, 10, 'Toronto')
    >>> t2 = Truck(1333, 10, 'Toronto')
    >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
    >>> t2.pack(p)
    True
    >>> _truck_most_space(t1, t2)
    True
    >>> t3 = Truck(1424, 10, 'Toronto')
    >>> t4 = Truck(1336, 10, 'Toronto')
    >>> p2 = Parcel(2, 5, 'Buffalo', 'Hamilton')
    >>> t3.pack(p2)
    True
    >>> _truck_most_space(t3, t4)
    False
    """
    return item1.available_space > item2.available_space


def _truck_less_space(item1: Truck, item2: Truck) -> bool:
    """
    Return true if <item1> has less capacity than <item2>.
    >>> t1 = Truck(1423, 10, 'Toronto')
    >>> t2 = Truck(1333, 10, 'Toronto')
    >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
    >>> t1.pack(p)
    True
    >>> _truck_less_space(t1, t2)
    True
    >>> t3 = Truck(1424, 10, 'Toronto')
    >>> t4 = Truck(1336, 10, 'Toronto')
    >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
    >>> t4.pack(p)
    True
    >>> _truck_less_space(t3, t4)
    False
    """
    return item1.available_space < item2.available_space


class GreedyScheduler(Scheduler):
    """
    A scheduler that assign parcels according to their priority to the desired
    truck.

    === Private Attributes ===
    _parcel_priority: Indicate parcel priority
    _parcel_order: Indicate parcel order
    _truck_order: Indicate truck order

    === Representation Invariants ===
    _priorities dictionary needs to have parcel_priority, parcel_order,
    and truck_order as its keys.
    _parcel_priority, _parcel_order, and _truck_order must be valid strings.
    Valid strings for _parcel_priority: volume, destination
    Valid strings for _parcel_order: non-increasing, non-decreasing
    Valid strings for _truck_order: non-increasing , non-decreasing
    """
    _parcel_priority: str
    _parcel_order: str
    _truck_order: str

    def __init__(self, priorities: Dict[str, str]) -> None:
        """An initializer for class GreedyScheduler.
        >>> f = {'parcel_priority': 'destination', 'parcel_order': 'non-increasing', 'truck_order': 'non-increasing'}
        >>> g = GreedyScheduler(f)
        >>> g._parcel_priority
        'destination'
        >>> g._parcel_order
        'non-increasing'
        >>> g._truck_order
        'non-increasing'
        """
        self._parcel_priority = priorities['parcel_priority']
        self._parcel_order = priorities['parcel_order']
        self._truck_order = priorities['truck_order']

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Assign parcels to trucks according to parcel priority, parcel order
        and truck order
        """
        result = []
        if self._parcel_priority == 'destination':
            temp_parcel = self._parcel_sort_destination(parcels)
            result = self._truck_helper(temp_parcel, trucks)
        if self._parcel_priority == 'volume':
            temp_parcel = self._parcel_sort_volume(parcels)
            result = self._truck_helper(temp_parcel, trucks)

        return result

    def _parcel_sort_destination(self, parcels: List[Parcel]) -> List[Parcel]:
        """Sort the parcels by their destination according to their parcel
        order"""
        result = []
        count = len(parcels)
        if self._parcel_order == 'non-increasing':
            parcel_queue = PriorityQueue(_parcel_large_des)
            for parcel in parcels:
                parcel_queue.add(parcel)

            while count > 0:
                result.append(parcel_queue.remove())
                count -= 1

        if self._parcel_order == 'non-decreasing':
            parcel_queue = PriorityQueue(_parcel_small_des)
            for parcel in parcels:
                parcel_queue.add(parcel)

            while count > 0:
                result.append(parcel_queue.remove())
                count -= 1

        return result

    def _parcel_sort_volume(self, parcels: List[Parcel]) -> List[Parcel]:
        """Sort the parcels by their destination according to
        their parcel order"""
        result = []
        count = len(parcels)
        if self._parcel_order == 'non-increasing':
            parcel_queue = PriorityQueue(_parcel_large_volume)
            for parcel in parcels:
                parcel_queue.add(parcel)

            while count > 0:
                result.append(parcel_queue.remove())
                count -= 1

        if self._parcel_order == 'non-decreasing':
            parcel_queue = PriorityQueue(_parcel_small_volume)
            for parcel in parcels:
                parcel_queue.add(parcel)

            while count > 0:
                result.append(parcel_queue.remove())
                count -= 1

        return result

    def _truck_helper(self, parcels: List[Parcel],
                      trucks: List[Truck]) -> List[Parcel]:
        """Pack the parcel to desired truck or return it if it is not packed
        >>> p17 = Parcel(17, 25, 'York', 'Toronto')
        >>> p21 = Parcel(21, 10, 'York', 'London')
        >>> p13 = Parcel(13, 8, 'York', 'London')
        >>> p42 = Parcel(42, 20, 'York', 'Toronto')
        >>> p25 = Parcel(25, 15, 'York', 'Toronto')
        >>> p61 = Parcel(61, 15, 'York', 'Hamilton')
        >>> p76 = Parcel(76, 20, 'York', 'London')
        >>> t1 = Truck(1, 40, 'York')
        >>> t2 = Truck(2, 40, 'York')
        >>> t3 = Truck(3, 25, 'York')
        >>> from domain import Fleet
        >>> f = Fleet()
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.add_truck(t3)
        >>> config = {'parcel_priority': 'destination','parcel_order': 'non-decreasing','truck_order': 'non-decreasing'}
        >>> scheduler = GreedyScheduler(config)
        >>> unscheduled = scheduler.schedule([p17, p21, p13, p42, p25, p61, p76],[t1, t2, t3])
        >>> unscheduled == [p42]
        True
        """
        result = []
        for parcel in parcels:
            available_truck = []
            for truck in trucks:
                if truck.available_space >= parcel.volume:
                    available_truck.append(truck)

            desired_truck = []
            for truck in available_truck:
                if truck.route[-1] == parcel.destination:
                    desired_truck.append(truck)

            if len(desired_truck) == 0:
                temp = self._truck_pack_parcel(parcel, available_truck)
                if temp is not None:
                    result.append(temp)

            if len(desired_truck) > 0:
                temp = self._truck_pack_parcel(parcel, desired_truck)
                if temp is not None:
                    result.append(temp)
        return result

    def _truck_pack_parcel(self, parcel: Parcel,
                           trucks: List[Truck]) -> Optional[Parcel]:
        """Pack one parcel onto a truck. Truck list does not have parcel's
        destination"""
        result = []
        if self._truck_order == 'non-increasing':
            truck_queue = PriorityQueue(_truck_most_space)
            for truck in trucks:
                truck_queue.add(truck)
            count = len(trucks)
            sorted_truck = []
            not_packed = True
            while count > 0:
                sorted_truck.append(truck_queue.remove())
                count -= 1
            i = 0
            while not_packed and i < len(sorted_truck):
                if sorted_truck[i].pack(parcel):
                    not_packed = False
                else:
                    i += 1
            if not_packed is True:
                result.append(parcel)

        if self._truck_order == 'non-decreasing':
            truck_queue = PriorityQueue(_truck_less_space)
            for truck in trucks:
                truck_queue.add(truck)
            count = len(trucks)
            sorted_truck = []
            not_packed = True
            while count > 0:
                sorted_truck.append(truck_queue.remove())
                count -= 1

            i = 0
            while not_packed and i < len(sorted_truck):
                if sorted_truck[i].pack(parcel):
                    not_packed = False
                else:
                    i += 1
            if not_packed is True:
                result.append(parcel)

        if len(result) == 1:
            return result[0]
        else:
            return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
