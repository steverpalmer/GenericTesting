#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

Find the right generic test for a given class
"""

import enum
import collections
import numbers
import fractions

import core
import relations
import collections_abc
import numbers_abc
import built_in_types

@enum.unique
class _ContainerLikeFlags(enum.IntEnum):
    Init = 0
    Container = 1
    Iterable = 2
    Sized = 4

    @staticmethod
    def discover(T: type):
        result = _ContainerLikeFlags.Init
        if issubclass(T, collections.abc.Container):
            result |= _ContainerLikeFlags.Container
        if issubclass(T, collections.abc.Iterable):
            result |= _ContainerLikeFlags.Iterable
        if issubclass(T, collections.abc.Sized):
            result |= _ContainerLikeFlags.Sized
        return result


class GenericTestLoader:

    def __init__(self):
        self._superclass_mapping = collections.OrderedDict([(type(object), relations.EqualityTests)])

    def register(self, T: type, T_Tests: core.GenericTests):
        self._superclass_mapping[T] = T_Tests

    @staticmethod
    def _is_user_defined(obj, mthd) -> bool:
        return getattr(obj, mthd, None) is not getattr(object, mthd, None)

    collection_like_list = ([],  # Init
                            [collections_abc.ContainerTests],  # Container
                            [collections_abc.IterableTests],  # Iterable
                            [collections_abc.ContainerOverIterableTests],  # Container and Iterable
                            [collections_abc.SizedTests],  # Sized
                            [collections_abc.SizedTests, collections_abc.ContainerTests],  # Sized and Container
                            [collections_abc.SizedOverIterableTests],  # Sized and Iterable
                            [collections_abc.ContainerOverIterableTests, collections_abc.SizedOverIterableTests])  # Sized, Iterable and Container

    def discover(self, T: type) -> core.GenericTests:
        result = None
        for known_T in reversed(self._superclass_mapping):
            if issubclass(T, known_T):
                result = self._superclass_mapping[known_T]
        if result is None:
            # Need to work a bit harder
            base_class_list = list(self.collection_like_list[_ContainerLikeFlags.discover(T)])
            print(base_class_list)
            if GenericTestLoader._is_user_defined(T, '__eq__'):
                if GenericTestLoader._is_user_defined(T, '__ne__'):
                    base_class_list.append(relations.EqualityTests)
                else:
                    base_class_list.append(relations.EqualsOnlyTests)
            if GenericTestLoader._is_user_defined(T, '__le__'):
                if GenericTestLoader._is_user_defined(T, '__ge__') and \
                   GenericTestLoader._is_user_defined(T, '__lt__') and \
                   GenericTestLoader._is_user_defined(T, '__gt__'):
                    # :TODO: determine if Total or Partial Order somehow
                    base_class_list.append(relations.PartialOrderingTests)
                else:
                    base_class_list.append(relations.LessOrEqualTests)
            if base_class_list:
                class result(*base_class_list):
                    pass
        if result is None:
            raise TypeError()
        return result


defaultGenericTestLoader = GenericTestLoader()

# The following should be ordered from the most abstract to the most specific.
# They are searched in the reverse order.

# Abstract Base Clases
defaultGenericTestLoader.register(collections.abc.Set, collections_abc.SetTests)
defaultGenericTestLoader.register(collections.abc.MutableSet, collections_abc.MutableSetTests)
defaultGenericTestLoader.register(numbers.Complex, numbers_abc.ComplexTests)
defaultGenericTestLoader.register(numbers.Real, numbers_abc.RealTests)
defaultGenericTestLoader.register(numbers.Rational, numbers_abc.RationalTests)
defaultGenericTestLoader.register(numbers.Integral, numbers_abc.IntegralTests)

# Concrete classes
defaultGenericTestLoader.register(set, built_in_types.setTests)
defaultGenericTestLoader.register(frozenset, built_in_types.frozensetTests)
defaultGenericTestLoader.register(dict, built_in_types.dictTests)
defaultGenericTestLoader.register(collections.Counter, built_in_types.CounterTests)
defaultGenericTestLoader.register(collections.OrderedDict, built_in_types.OrderedDictTests)
defaultGenericTestLoader.register(collections.defaultdict, built_in_types.defaultdictTests)

defaultGenericTestLoader.register(complex, built_in_types.complexTests)
defaultGenericTestLoader.register(float, built_in_types.floatTests)
defaultGenericTestLoader.register(fractions.Fraction, built_in_types.FractionTests)
defaultGenericTestLoader.register(int, built_in_types.intTests)


if __name__ == '__main__':

    # Test1: Define the Class that I'm going to test
    from typing import List
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

    # Define the tests
    from hypothesis import strategies as st
    @core.Given({core.ClassUnderTest: st.builds(IntSetDecorator), collections_abc.ElementT: st.integers()})
    class Test_IntSetDecorator(defaultGenericTestLoader.discover(IntSetDecorator)):
        empty = IntSetDecorator([])

        def test_sum(self):
            isd = IntSetDecorator([1, 3, 5])
            self.assertEqual(isd.total(), 9)

    # Test2: bit set?
    import functools
    class BitSet:
        """
        An embrionic class describing a set of ints, stored as bitmasks.
        """

        def __init__(self, values: List[int]) -> None:
            self._value = functools.reduce((lambda x, y: (x | pow(2, y))), values, 0)

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

    #Define the tests
    element_st = st.integers(min_value=0, max_value=63)
    @core.Given({core.ClassUnderTest: st.builds(BitSet, st.lists(element_st)), collections_abc.ElementT: element_st})
    class Test_BitSet(defaultGenericTestLoader.discover(BitSet)):
        pass

    # Run the tests
    from limited_text_test_result import LimitedTextTestResult
    from functools import partial
    import unittest
    SUITE = unittest.TestSuite()
#    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_IntSetDecorator))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_BitSet))
    TR = unittest.TextTestRunner(verbosity=2, resultclass=partial(LimitedTextTestResult, max_failures=None, max_errors=1))
    TR.run(SUITE)

