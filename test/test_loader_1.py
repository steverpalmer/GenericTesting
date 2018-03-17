#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.loader using the type inheritance."""

from typing import List
import collections

from hypothesis import strategies as st

from generic_testing import *


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

    def test_total(self):
        isd = IntSetDecorator([1, 3, 5])
        self.assertEqual(isd.total(), 9)


if __name__ == '__main__':
    # Run the tests
    import unittest
    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_int))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_IntSetDecorator))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
