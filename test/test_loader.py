#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A test of the generic_test.loader.
"""

from typing import List
import collections
from functools import reduce

from hypothesis import strategies as st

from src import *


@Given(st.integers())
class Test_int(defaultGenericTestLoader.discover(int)):
    pass


class IntSetDecorator(collections.abc.Set):
    """
    A class discribing a set of ints, with an extra method 'total'.
    """

    def __init__(self, value: List[int]) -> None:
        super().__init__()
        self.data = frozenset(value)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data

    def total(self):
        return sum(self)

    def __repr__(self):
        return "MyClass({self.data})".format(self=self)


@Given({core.ClassUnderTest: st.builds(IntSetDecorator), collections_abc.ElementT: st.integers()})
class Test_IntSetDecorator(defaultGenericTestLoader.discover(IntSetDecorator)):
    empty = IntSetDecorator([])

    def test_generic_2010_empty_type(self):
        self.assertIsInstance(self.empty, IntSetDecorator)

    def test_sum(self):
        isd = IntSetDecorator([1, 3, 5])
        self.assertEqual(isd.total(), 9)


class BitSet:
    """
    An embrionic class describing a set of ints, stored as bitmasks.
    """

    def __init__(self, values: List[int]) -> None:
        self._value = reduce((lambda x, y: (x | pow(2, y))), values, 0)

    def __eq__(self, other: 'BitSet'):
        return self._value == other._value

    def __contains__(self, value: int):
        return bool(self._value & pow(2, value))

#         def _iterator(self):
#             result = 1
#             while result <= self._value:
#                 if result in self:
#                     yield result
#                 result *= 2
#
#         def __iter__(self):
#             return self._iterator()


element_st = st.integers(min_value=0, max_value=63)


@Given({core.ClassUnderTest: st.builds(BitSet, st.lists(element_st)), collections_abc.ElementT: element_st})
class Test_BitSet(defaultGenericTestLoader.discover(BitSet)):
    pass


if __name__ == '__main__':
    # Run the tests
    import unittest
    SUITE = unittest.TestSuite()
    name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
