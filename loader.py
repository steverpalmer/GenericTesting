#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

Find the right generic test for a given class
"""

import collections
import numbers
import fractions

import core
import relations
import collections_abc
import numbers_abc
import built_in_types

class GenericTestLoader:

    def __init__(self):
        self._superclass_mapping = collections.OrderedDict([(type(object), relations.EqualityTests)])

    def register(self, T: type, T_Tests: core.GenericTests):
        self._superclass_mapping[T] = T_Tests

    def discover(self, T: type) -> core.GenericTests:
        for known_T in reversed(self._superclass_mapping):
            if issubclass(T, known_T):
                return self._superclass_mapping[known_T]
        raise TypeError()

defaultGenericTestLoader = GenericTestLoader()

# Abstract Base Clases
defaultGenericTestLoader.register(collections.abc.Iterable, collections_abc.IterableTests)
defaultGenericTestLoader.register(collections.abc.Sized, collections_abc.SizedTests)
defaultGenericTestLoader.register(collections.abc.Container, collections_abc.ContainerTests)
defaultGenericTestLoader.register(collections.abc.Set, collections_abc.SetTests)
defaultGenericTestLoader.register(collections.abc.MutableSet, collections_abc.MutableSetTests)
defaultGenericTestLoader.register(numbers.Complex, numbers_abc.ComplexTests)
defaultGenericTestLoader.register(numbers.Real, numbers_abc.RealTests)
defaultGenericTestLoader.register(numbers.Rational, numbers_abc.RationalTests)
defaultGenericTestLoader.register(numbers.Integral, numbers_abc.IntegralTests)

# Concrete classes
defaultGenericTestLoader.register(set, built_in_types.setTests)
defaultGenericTestLoader.register(frozenset, built_in_types.frozensetTests)
defaultGenericTestLoader.register(complex, built_in_types.complexTests)
defaultGenericTestLoader.register(float, built_in_types.floatTests)
defaultGenericTestLoader.register(fractions.Fraction, built_in_types.FractionTests)
defaultGenericTestLoader.register(int, built_in_types.intTests)


if __name__ == '__main__':

    # Define the Class that I'm going to test
    from typing import List
    class IntSetDecorator(collections.abc.Set):

        def __init__(self, value: List[int]) -> None:
            super().__init__()
            self.data = frozenset(value)

        def __iter__(self):
            return iter(self.data)
 
        def __len__(self):
            return len(self.data)
 
        def __contains__(self, key):
            return key in self.data

        def sum(self):
            return sum(self)

        def __repr__(self):
            return "MyClass({self.data})".format(self=self)

    # Define the tests
    from hypothesis import strategies as st
    @core.Given({core.ClassUnderTest: st.builds(IntSetDecorator), collections_abc.ElementT: st.integers()})
    class IntSetDecoratorTests(defaultGenericTestLoader.discover(IntSetDecorator)):
        empty = IntSetDecorator([])

        def test_sum(self):
            isd = IntSetDecorator([1, 3, 5])
            self.assertEqual(isd.sum(), 9)

    # Define a unittest.TextTestResult decorator to control cascade failure effects
    from limited_text_test_result import LimitedTextTestResult

    # Run the tests
    from functools import partial
    import unittest
    TR = unittest.TextTestRunner(verbosity=2, resultclass=partial(LimitedTextTestResult, max_failures=None, max_errors=1))
    TR.run(unittest.defaultTestLoader.loadTestsFromTestCase(IntSetDecoratorTests))

