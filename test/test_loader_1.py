#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.loader using the type inheritance."""

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

    def test_total(self):
        isd = IntSetDecorator([1, 3, 5])
        self.assertEqual(isd.total(), 9)


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