"""Assignment 1 - Tests

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

This module contains sample test cases that you can use to test your code.
These are a very incomplete set of test cases! We will be testing your code on
a much more thorough set of tests.

The self-test on MarkUs runs all of the tests below, along with a few others.
Make sure you run the self-test on MarkUs after submitting your code!

Once you have the entire program completed, that is, after Task 5, your
code should pass all of the tests we've provided.  As you develop your code,
test cases for parts that you haven't written yet will fail, of course.

But as you work through the earlier phases of the assignment, you can run the
individual tests below for each method as you complete it. We encourage you to
add further test cases in this file to improve your confidence in your code.

Tip: if you put your mouse inside a pytest function and right click, the "run"
menu will give you the option of running just that test function.
"""
import pytest
from typing import Dict
from distance_map import DistanceMap
from domain import Truck, Parcel, Fleet
from scheduler import GreedyScheduler
from container import PriorityQueue, _shorter
from experiment import SchedulingExperiment

# This variable is used in the special pytest test case defined by function
# test_experiment below.  The variable defines a single scheduling experiment
# test case to be run. It gives a unique identifier for the test case, and
# specifies both the configuration to use and the correct statistics to expect.
test_arguments = [
    ('1-small',
     {
         'depot_location': 'Toronto',
         'parcel_file': 'data/parcel-data-small.txt',
         'truck_file': 'data/truck-data-small.txt',
         'map_file': 'data/map-data.txt',
         'algorithm': 'greedy',
         'parcel_priority': 'volume',
         'parcel_order': 'non-decreasing',
         'truck_order': 'non-decreasing',
         'verbose': 'false'
     },
     {
         'fleet': 3,
         'unused_trucks': 0,
         'unused_space': 0,
         'avg_distance': 192.7,
         'avg_fullness': 100,
         'unscheduled': 0
     }),
    # You can add additional test cases here!
    # Write these in the format:
    # (<test_id>, <config dictionary>, <expected_stats dictionary>)
    # If you're adding multiple tests: remember to add a comma (,) after the
    # tuple!
]


def test_add_distance_dif() -> None:
    """Test add_distance with different distance between cities."""
    m = DistanceMap()
    m.add_distance('Toronto', 'Vancouver', 234, 333)
    expected = {'Toronto - Vancouver': [234, 333]}
    actual = m._map
    assert actual == expected


def test_add_distance_same() -> None:
    """Test add_distance with same distance between cities."""
    m = DistanceMap()
    m.add_distance('Toronto', 'Oakville', 23)
    expected = {'Toronto - Oakville': [23, 23]}
    actual = m._map
    assert actual == expected


def test_add_distance_exists() -> None:
    """Test add_distance with cities that already exists."""
    m = DistanceMap()
    m.add_distance('Toronto', 'Oakville', 23)
    m.add_distance('Toronto', 'Oakville', 56)
    expected = {'Toronto - Oakville': [23, 23]}
    actual = m._map
    assert actual == expected


def test_distance_same() -> None:
    """Test distance with cities that has same distance go and back"""
    m = DistanceMap()
    m.add_distance('Toronto', 'Oakville', 23)
    actual = m.distance('Oakville', 'Toronto')
    expected = 23
    assert actual == expected


def test_distance_diff() -> None:
    """Test distance with cities that has different distance go and back"""
    m = DistanceMap()
    m.add_distance('Hamilton', 'Oakville', 23, 13)
    actual = m.distance('Oakville', 'Hamilton')
    expected = 13
    assert actual == expected


def test_distance_none() -> None:
    """Test distance with cities that has same distance go and back"""
    m = DistanceMap()
    m.add_distance('Toronto', 'Oakville', 23)
    actual = m.distance('Vancouver', 'Toronto')
    expected = -1
    assert actual == expected


def test_distance_map_basic() -> None:
    """Test DistanceMap when a single distance is provided."""
    m = DistanceMap()
    assert m.distance('Montreal', 'Toronto') == -1
    m.add_distance('Montreal', 'Toronto', 4)
    assert m.distance('Montreal', 'Toronto') == 4


def test_parcel() -> None:
    """Test if we have created a parcel object"""
    p1 = Parcel(3, 45, 'Chicago', 'Los Angeles')
    expected = 'Los Angeles'
    actual = p1.destination
    assert expected == actual


def test_truck() -> None:
    """Test if we have created a truck object"""
    t1 = Truck(2, 5, 'Tokyo')
    expected1 = []
    actual1 = t1.parcel_lst
    assert expected1 == actual1
    expected2 = 5
    actual2 = t1.available_space
    assert expected2 == actual2


def test_truck_pack_all() -> None:
    """Test pack -> all parcels packed"""
    t1 = Truck(1, 8, 'Vancouver')
    p1 = Parcel(1, 3, 'Boston', 'York')
    p2 = Parcel(3, 2, 'Richmond', 'Toronto')
    expected1 = True
    actual1 = t1.pack(p1)
    assert expected1 == actual1
    expected2 = True
    actual2 = t1.pack(p2)
    assert expected2 == actual2


def test_truck_pack_partial() -> None:
    """Test pack -> one packed one not packed"""
    t1 = Truck(1, 8, 'Vancouver')
    p1 = Parcel(1, 3, 'Boston', 'York')
    p2 = Parcel(3, 7, 'Richmond', 'Toronto')
    expected1 = True
    actual1 = t1.pack(p1)
    assert expected1 == actual1
    expected2 = False
    actual2 = t1.pack(p2)
    assert expected2 == actual2


def test_truck_pack_none() -> None:
    """Test pack -> one packed one not packed"""
    t1 = Truck(1, 8, 'Vancouver')
    p1 = Parcel(1, 9, 'Boston', 'York')
    p2 = Parcel(3, 10, 'Richmond', 'Toronto')
    expected1 = False
    actual1 = t1.pack(p1)
    assert expected1 == actual1
    expected2 = False
    actual2 = t1.pack(p2)
    assert expected2 == actual2


def test_truck_fullness_empty() -> None:
    """Test fullness -> empty truck"""
    t1 = Truck(1, 10, 'Toronto')
    expected = 0.0
    actual = t1.fullness()
    assert expected == actual


def test_truck_fullness_full() -> None:
    """Test fullness -> full truck"""
    t1 = Truck(1, 9, 'Vancouver')
    p1 = Parcel(1, 4, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 5, 'London', 'Istanbul')
    assert t1.pack(p1) is True
    assert t1.pack(p2) is True
    expected = 100.0
    actual = t1.fullness()
    assert actual == expected


def test_truck_fullness_partial() -> None:
    """Test fullness -> partial full truck"""
    t1 = Truck(1, 8, 'Vancouver')
    p1 = Parcel(1, 4, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 10, 'London', 'Istanbul')
    assert t1.pack(p1) is True
    assert t1.pack(p2) is False
    expected = 50.0
    actual = t1.fullness()
    assert actual == expected


def test_add_truck_num() -> None:
    """Test add_truck"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    expected = 3
    actual = f.num_trucks()
    assert expected == actual


def test_nonempty_trucks_full() -> None:
    """Test non empty trucks with full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 8, 'London', 'Istanbul')
    p3 = Parcel(3, 45, 'Osaka', 'Tokyo')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t3.pack(p3) is True
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 3 == f.num_nonempty_trucks()


def test_nonempty_trucks_empty() -> None:
    """Test non empty trucks with empty trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 0 == f.num_nonempty_trucks()


def test_nonempty_trucks_partial() -> None:
    """Test non empty trucks with partial trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 10, 'Vancouver')
    t3 = Truck(3, 15, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 20, 'London', 'Istanbul')
    p3 = Parcel(3, 10, 'Osaka', 'Tokyo')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is False
    assert t3.pack(p3) is True
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 2 == f.num_nonempty_trucks()


def test_parcel_allocations_empty() -> None:
    """Test parcel allocations with empty trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 10, 'Vancouver')
    t3 = Truck(3, 15, 'Toronto')
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    expected = {1: [], 2: [], 3: []}
    assert f.parcel_allocations() == expected


def test_parcel_allocations_full() -> None:
    """Test parcel allocations with empty trucks"""
    t1 = Truck(1, 50, 'New Jersey')
    t2 = Truck(2, 20, 'Vancouver')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 20, 'London', 'Istanbul')
    p3 = Parcel(3, 10, 'Osaka', 'Tokyo')
    assert t1.pack(p1) is True
    assert t1.pack(p3) is True
    assert t2.pack(p2) is True
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    expected = {1: [1, 3], 2: [2]}
    assert f.parcel_allocations() == expected


def test_parcel_allocations_partial() -> None:
    """Test parcel allocations with partial empty trucks"""
    t1 = Truck(1, 50, 'New Jersey')
    t2 = Truck(2, 20, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 20, 'London', 'Istanbul')
    p3 = Parcel(3, 10, 'Osaka', 'Tokyo')
    assert t1.pack(p1) is True
    assert t1.pack(p3) is True
    assert t2.pack(p2) is True
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    expected = {1: [1, 3], 2: [2], 3: []}
    assert f.parcel_allocations() == expected


def test_total_unused_space_empty() -> None:
    """Test total unused space with empty trucks"""
    t1 = Truck(1, 50, 'New Jersey')
    t2 = Truck(2, 20, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    expected = 0
    assert expected == f.total_unused_space()


def test_total_unused_space_full() -> None:
    """Test total unused space with full trucks"""
    t1 = Truck(1, 50, 'New Jersey')
    t2 = Truck(2, 20, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 20, 'London', 'Istanbul')
    p3 = Parcel(3, 10, 'Osaka', 'Tokyo')
    p4 = Parcel(4, 10, 'Brampton', 'Oakville')
    assert t1.pack(p1) is True
    assert t1.pack(p3) is True
    assert t2.pack(p2) is True
    assert t3.pack(p4) is True
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    expected = 70
    assert expected == f.total_unused_space()


def test_total_unused_space_partial() -> None:
    """Test total unused space with partial full trucks"""
    t1 = Truck(1, 50, 'New Jersey')
    t2 = Truck(2, 20, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 20, 'London', 'Istanbul')
    p4 = Parcel(4, 80, 'Brampton', 'Oakville')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t3.pack(p4) is False
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    expected = 45
    assert expected == f.total_unused_space()


def test_total_fullness_empty() -> None:
    """Test total fullness with empty trucks"""
    t1 = Truck(1, 50, 'New Jersey')
    t2 = Truck(2, 20, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 0.0 == f._total_fullness()


def test_total_fullness_full() -> None:
    """Test total fullness with full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 8, 'London', 'Istanbul')
    p3 = Parcel(3, 45, 'Osaka', 'Tokyo')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t3.pack(p3) is True
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 300 == f._total_fullness()


def test_total_fullness_partial() -> None:
    """Test total fullness with partial full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 4, 'London', 'Istanbul')
    p3 = Parcel(3, 50, 'Osaka', 'Tokyo')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t3.pack(p3) is False
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 150 == f._total_fullness()


def test_average_fullness_partial() -> None:
    """Test average fullness with partially empty trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    t4 = Truck(4, 20, 'Havana')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 3, 'London', 'Istanbul')
    p3 = Parcel(3, 50, 'Osaka', 'Tokyo')
    p4 = Parcel(4, 1, 'London', 'Istanbul')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t2.pack(p4) is True
    assert t3.pack(p3) is False
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    f.add_truck(t4)
    assert 75 == f.average_fullness()


def test_average_fullness_full_all() -> None:
    """Test average fullness with full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 5, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 8, 'London', 'Istanbul')
    p3 = Parcel(3, 45, 'Osaka', 'Tokyo')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t3.pack(p3) is True
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 100 == f.average_fullness()


def test_total_distance_travelled_empty() -> None:
    """Test total distance travelled with empty trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    m = DistanceMap()
    m.add_distance('Toronto', 'Hamilton', 9)
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 0 == f.total_distance_travelled(m)


def test_total_distance_travelled_full() -> None:
    """Test total distance travelled with full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 2, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 4, 'London', 'Istanbul')
    p3 = Parcel(3, 20, 'Osaka', 'Tokyo')
    p4 = Parcel(4, 3, 'Oakville', 'London')
    p5 = Parcel(5, 4, 'London', 'Istanbul')
    assert t1.pack(p1) is True
    assert t1.pack(p4) is True
    assert t2.pack(p2) is True
    assert t2.pack(p5) is True
    assert t3.pack(p3) is True
    m = DistanceMap()
    m.add_distance('New Jersey', 'Tokyo', 9)
    m.add_distance('Tokyo', 'London', 10)
    m.add_distance('New Jersey', 'London', 11, 13)
    m.add_distance('Istanbul', 'Vancouver', 15, 20)
    m.add_distance('Toronto', 'Tokyo', 15, 20)
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 102 == f.total_distance_travelled(m)


def total_distance_travelled_partial() -> None:
    """Test total distance travelled with partial full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 2, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 4, 'London', 'Istanbul')
    p3 = Parcel(3, 80, 'Osaka', 'Tokyo')
    p5 = Parcel(5, 4, 'London', 'Istanbul')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t2.pack(p5) is True
    assert t3.pack(p3) is False
    m = DistanceMap()
    m.add_distance('New Jersey', 'Tokyo', 9)
    m.add_distance('Tokyo', 'London', 10)
    m.add_distance('New Jersey', 'London', 11, 13)
    m.add_distance('Istanbul', 'Vancouver', 15, 20)
    m.add_distance('Toronto', 'Tokyo', 15, 20)
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 53 == f.total_distance_travelled(m)


def test_average_distance_travelled_full() -> None:
    """Test average distance travelled for full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 2, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 4, 'London', 'Istanbul')
    p3 = Parcel(3, 20, 'Osaka', 'Tokyo')
    p4 = Parcel(4, 3, 'Oakville', 'London')
    p5 = Parcel(5, 4, 'London', 'Istanbul')
    assert t1.pack(p1) is True
    assert t1.pack(p4) is True
    assert t2.pack(p2) is True
    assert t2.pack(p5) is True
    assert t3.pack(p3) is True
    m = DistanceMap()
    m.add_distance('New Jersey', 'Tokyo', 9)
    m.add_distance('Tokyo', 'London', 10)
    m.add_distance('New Jersey', 'London', 11, 13)
    m.add_distance('Istanbul', 'Vancouver', 15, 20)
    m.add_distance('Toronto', 'Tokyo', 15, 20)
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 34 == f.average_distance_travelled(m)


def test_average_distance_travelled_partial() -> None:
    """Test total distance travelled with partial full trucks"""
    t1 = Truck(1, 5, 'New Jersey')
    t2 = Truck(2, 8, 'Vancouver')
    t3 = Truck(3, 45, 'Toronto')
    p1 = Parcel(1, 2, 'Osaka', 'Tokyo')
    p2 = Parcel(2, 4, 'London', 'Istanbul')
    p3 = Parcel(3, 80, 'Osaka', 'Tokyo')
    p5 = Parcel(5, 4, 'London', 'Istanbul')
    assert t1.pack(p1) is True
    assert t2.pack(p2) is True
    assert t2.pack(p5) is True
    assert t3.pack(p3) is False
    m = DistanceMap()
    m.add_distance('New Jersey', 'Tokyo', 9)
    m.add_distance('Tokyo', 'London', 10)
    m.add_distance('New Jersey', 'London', 11, 13)
    m.add_distance('Istanbul', 'Vancouver', 15, 20)
    m.add_distance('Toronto', 'Tokyo', 15, 20)
    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)
    assert 26.5 == f.average_distance_travelled(m)


def test_num_trucks_doctest() -> None:
    """Test the doctest provided for Fleet.num_trucks"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    f.add_truck(t1)
    assert f.num_trucks() == 1


def test_num_nonempty_trucks_doctest() -> None:
    """Test the doctest provided for Fleet.num_nonempty_trucks"""
    f = Fleet()

    t1 = Truck(1423, 10, 'Toronto')
    f.add_truck(t1)
    p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
    assert t1.pack(p1) is True

    p2 = Parcel(2, 4, 'Toronto', 'Montreal')
    assert t1.pack(p2) is True
    assert t1.fullness() == 90.0

    t2 = Truck(5912, 20, 'Toronto')
    f.add_truck(t2)
    p3 = Parcel(3, 2, 'New York', 'Windsor')
    assert t2.pack(p3) is True
    assert t2.fullness() == 10.0

    t3 = Truck(1111, 50, 'Toronto')
    f.add_truck(t3)
    assert f.num_nonempty_trucks() == 2


def test_parcel_allocations_doctest() -> None:
    """Test the doctest provided for Fleet.parcel_allocations"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
    p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
    assert t1.pack(p1) is True
    assert t1.pack(p2) is True
    t2 = Truck(1333, 10, 'Toronto')
    p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
    assert t2.pack(p3) is True
    f.add_truck(t1)
    f.add_truck(t2)
    assert f.parcel_allocations() == {1423: [27, 12], 1333: [28]}


def test_total_unused_space_doctest() -> None:
    """Test the doctest provided for Fleet.total_unused_space"""
    f = Fleet()
    assert f.total_unused_space() == 0

    t = Truck(1423, 1000, 'Toronto')
    p = Parcel(1, 5, 'Buffalo', 'Hamilton')
    assert t.pack(p) is True

    f.add_truck(t)
    assert f.total_unused_space() == 995


def test_average_fullness_doctest() -> None:
    """Test the doctest provided for Fleet.average_fullness"""
    f = Fleet()
    t = Truck(1423, 10, 'Toronto')
    p = Parcel(1, 5, 'Buffalo', 'Hamilton')
    assert t.pack(p) is True

    f.add_truck(t)
    assert f.average_fullness() == 50.0


def test_total_distance_travelled_doctest() -> None:
    """Test the doctest provided for Fleet.total_distance_travelled"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
    assert t1.pack(p1) is True

    t2 = Truck(1333, 10, 'Toronto')
    p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
    assert t2.pack(p2) is True

    m = DistanceMap()
    m.add_distance('Toronto', 'Hamilton', 9)
    f.add_truck(t1)
    f.add_truck(t2)
    assert f.total_distance_travelled(m) == 36


def test_average_distance_travelled_doctest() -> None:
    """Test the doctest provided for Fleet.average_distance_travelled"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
    assert t1.pack(p1) is True

    t2 = Truck(1333, 10, 'Toronto')
    p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
    assert t2.pack(p2) is True

    m = DistanceMap()
    m.add_distance('Toronto', 'Hamilton', 9)
    f.add_truck(t1)
    f.add_truck(t2)
    assert f.average_distance_travelled(m) == 18.0


def test_priority_queue_is_empty_doctest() -> None:
    """Test the doctest provided for PriorityQueue.is_empty"""
    pq = PriorityQueue(str.__lt__)
    assert pq.is_empty() is True

    pq.add('fred')
    assert pq.is_empty() is False


def test_priority_queue_add_remove_doctest() -> None:
    """Test the doctest provided for PriorityQueue.add and
    PriorityQueue.remove"""
    pq = PriorityQueue(_shorter)
    pq.add('fred')
    pq.add('arju')
    pq.add('monalisa')
    pq.add('hat')
    assert pq.remove() == 'hat'
    assert pq.remove() == 'fred'
    assert pq.remove() == 'arju'
    assert pq.remove() == 'monalisa'


def test_greedy_scheduler_example() -> None:
    """Test GreedyScheduler on the example provided."""
    p17 = Parcel(17, 25, 'York', 'Toronto')
    p21 = Parcel(21, 10, 'York', 'London')
    p13 = Parcel(13, 8, 'York', 'London')
    p42 = Parcel(42, 20, 'York', 'Toronto')
    p25 = Parcel(25, 15, 'York', 'Toronto')
    p61 = Parcel(61, 15, 'York', 'Hamilton')
    p76 = Parcel(76, 20, 'York', 'London')

    t1 = Truck(1, 40, 'York')
    t2 = Truck(2, 40, 'York')
    t3 = Truck(3, 25, 'York')

    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)

    # We've left parcel_file, truck_file, and map_file empty in the config
    # dictionary below because you should *not* use these in your
    # GreedyScheduler. It is not responsible for reading data from these files.
    config = {'depot_location': 'York',
              'parcel_file': '',
              'truck_file': '',
              'map_file': '',
              'algorithm': 'greedy',
              'parcel_priority': 'destination',
              'parcel_order': 'non-increasing',
              'truck_order': 'non-increasing',
              'verbose': 'false'}

    scheduler = GreedyScheduler(config)
    unscheduled = scheduler.schedule([p17, p21, p13, p42, p25, p61, p76],
                                     [t1, t2, t3])

    assert unscheduled == [p76]

    truck_parcels = f.parcel_allocations()
    assert truck_parcels[1] == [17, 61]
    assert truck_parcels[2] == [42, 25]
    assert truck_parcels[3] == [21, 13]


################################################################################
# The test below uses pytest.mark.parametrize.
#
# This provides a way of running the same test code with different parameters
# without having to repeat the body multiple times.
#
# The line above the test_experiment method works as follows:
# @pytest.mark.parametrize('test_id, config, expected_stats', test_arguments)
#                           ^                                 ^
#                    These are the parameters        This is a list where each
#                    of test_experiment that         element is a tuple
#                    we're filling.                  containing values for those
#                                                    parameters.
#
# test_arguments is the variable defined near the top of this module.
#
# We have included one item in test_arguments for you. This is a tuple
# representing the following parameter configurations:
#     test_id        = '1-small'
#     config         = {'depot_location': 'Toronto', ...}
#     expected_stats = {'fleet': 3, ...}
#
# If you want to add additional test cases, you create a tuple with the same
# format and add it to the list.
#
# For more details, see:
# https://docs.pytest.org/en/stable/parametrize.html
#
# NOTE: if you get a "FileNotFoundError", try replacing the filename
# with the full path to the file (e.g., "C:\\Users\\David\\Documents\\...")
################################################################################
@pytest.mark.parametrize('stat', [
    'fleet', 'unused_trucks', 'unused_space', 'avg_distance', 'avg_fullness',
    'unscheduled'])
class TestExperiment:
    """
    Tests for SchedulingExperiment.run
    """
    @pytest.mark.parametrize('test_id, config, expected_stats', test_arguments)
    def test_experiment(self, test_id: str, config: Dict[str, str],
                        expected_stats: Dict[str, str], stat: str) -> None:
        """Run the SchedulingExperiment on the given config and expected_stats.
        Assert that the stat returned from the experiment matches
        expected_stats[stat].
        """
        experiment = SchedulingExperiment(config)
        results = experiment.run()

        # pytest.approx lets us use approximate values so we can avoid
        # failing a test case over very small differences in floating point
        # values. These can arise simply from doing mathematical operations in
        # a different order. [If you find this intriguing, take csc336!]

        # In this case, we're making sure our actual value is in the range
        # (expected - 1e-1, expected + 1e-1)
        expected = expected_stats[stat]
        actual = results[stat]
        assert actual == pytest.approx(expected, abs=1e-1)


if __name__ == '__main__':
    pytest.main(['a1_starter_tests.py'])
