#!/usr/bin/env python3
# Copyright 2021 Steve Palmer

"""A test of the generic_test.loader using the type inheritance."""

from typing import List
import collections
import enum

from hypothesis import strategies as st

from generic_testing_test_context import generic_testing


@generic_testing.Given(st.integers())
class Test_int(generic_testing.defaultGenericTestLoader.discover(int)):
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


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(IntSetDecorator),
        generic_testing.collections_abc.ElementT: st.integers(),
    }
)
class Test_IntSetDecorator(
    generic_testing.defaultGenericTestLoader.discover(IntSetDecorator)
):
    empty = IntSetDecorator([])

    def test_total(self):
        isd = IntSetDecorator([1, 3, 5])
        self.assertEqual(isd.total(), 9)


class E1(enum.IntEnum):
    RED = 1
    BLUE = 2
    GREEN = 2


@generic_testing.Given(generic_testing.enum_strategy_dict(E1))
class Test_E1(generic_testing.defaultGenericTestLoader.discover(E1)):
    pass


if __name__ == "__main__":
    # Run the tests
    import unittest

    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_int))
    SUITE.addTest(
        unittest.defaultTestLoader.loadTestsFromTestCase(Test_IntSetDecorator)
    )
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_E1))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
