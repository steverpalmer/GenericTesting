#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A library of generic test for the python built-in types.
"""

import fractions
import types
import collections

from hypothesis import assume

from .isclose import IsClose
from .core import ClassUnderTest
from .numbers_abc import IntegralTests, RationalTests, RealTests, ComplexTests
from .collections_abc import (ElementT, ValueT, SetTests, KeysViewTests, ItemsViewTests, ValuesViewTests,
                              MutableSetTests, MappingTests, MutableMappingTests)


class intTests(IntegralTests):
    zero = 0
    one = 1
    real_zero = float(0)

    # TODO: tests for bit_length, to_bytes, from_bytes


class FractionTests(RationalTests):
    zero = fractions.Fraction(0)
    one = fractions.Fraction(1)
    real_zero = float(fractions.Fraction(0))
    half = fractions.Fraction(1, 2)


class floatTests(RealTests):
    zero = 0.0
    one = 1.0
    root_two = 2.0 ** 0.5

    def test_generic_2220_addition_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        assume(not self.isclose(a, b) and not self.isclose(b, c))
        super().test_generic_2220_addition_associativity(a, b, c)

    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))

    # TODO: tests for as_integer_ratio, is_integer, hex, fromhex


class complexTests(ComplexTests):
    zero = complex(0)
    one = complex(1)
    real_zero = 0.0
    i = complex(0, 1)

    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    def test_generic_2238_multiplication_addition_right_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2238_multiplication_addition_right_distributivity(a, b, c)

    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))


class frozensetTests(SetTests):

    empty = frozenset()

    def test_generic_2600_issubset_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.issubset(b), a <= b)

    def test_generic_2601_isuperset_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.issuperset(b), a >= b)

    def test_generic_2602_union_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.union(b), a | b)

    def test_generic_2603_intersection_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.intersection(b), a & b)

    def test_generic_2604_difference_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.difference(b), a - b)

    def test_generic_2605_symmetric_difference_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertEqual(a.symmetric_difference(b), a ^ b)


class setTests(MutableSetTests, frozensetTests):

    empty = set()

    def copy(self, s: ClassUnderTest) -> ClassUnderTest:
        return s.copy()

    def singleton_constructor(self, a: ElementT) -> ClassUnderTest:
        return set([a])

    def test_generic_2010_copy_helper_definition(self, a: ClassUnderTest) -> None:
        b = a.copy()
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(a, b)

    def test_generic_2610_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a |= b
        self.assertEqual(a, a_copy | b)
        a_nother.update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2611_intersection_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a &= b
        self.assertEqual(a, a_copy & b)
        a_nother.intersection_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2612_difference_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a -= b
        self.assertEqual(a, a_copy - b)
        a_nother.difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2613_symmetric_difference_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = a.copy()
        a_nother = a.copy()
        a ^= b
        self.assertEqual(a, a_copy ^ b)
        a_nother.symmetric_difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2614_remove_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        a.add(b)
        a_copy = a.copy()
        a.remove(b)
        a_copy.discard(b)
        self.assertEqual(a, a_copy)
        with self.assertRaises(KeyError):
            a.remove(b)

    def test_generic_2615_pop_definition(self, a: ClassUnderTest) -> None:
        if a:
            a_copy = a.copy()
            b = a.pop()
            self.assertTrue(b in a_copy)
            self.assertTrue(b not in a)
            a_copy.discard(b)
            self.assertEqual(a, a_copy)
        else:
            with self.assertRaises(KeyError):
                a.pop()

    def test_generic_2616_clear_definition(self, a: ClassUnderTest) -> None:
        a.clear()
        self.assertEqual(a, self.empty)


class dictKeysViewTests(KeysViewTests):

    empty = dict().keys()


class dictItemsViewTests(ItemsViewTests):

    empty = dict().items()


class dictValuesViewTests(ValuesViewTests):
    pass


class MappingProxyTypeTests(MappingTests):

    empty = types.MappingProxyType(dict())

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return types.MappingProxyType({a: b})


class dictTests(MutableMappingTests):

    empty = dict()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return {a: b}

    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        return a.copy()


class CounterTests(dictTests):

    empty = collections.Counter()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.Counter({a: b})

    def test_generic_2505_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        a_copy = self.copy(a)
        a.update(b)
        self.assertLessEqual(b.keys(), a.keys())
        for k in a:
            self.assertEqual(a[k], b[k] + a_copy[k])

    # TODO: add tests for Counter specific methods


class OrderedDictTests(dictTests):

    empty = collections.OrderedDict()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.OrderedDict([(a, b)])

    # TODO: add tests for OrderedDict specific features and methods


class defaultdictTests(dictTests):

    def __init__(self, default_factory, methodName=None):
        super().__init__(methodName)
        self._default_factory = default_factory

    @property
    def empty(self):
        return collections.defaultdict(self._default_factory)

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.defaultdict(self._default_factory, [(a, b)])


__all__ = ('intTests', 'FractionTests', 'floatTests', 'complexTests',
           'frozensetTests', 'setTests',
           'dictKeysViewTests', 'dictItemsViewTests', 'dictValuesViewTests', 'MappingProxyTypeTests',
           'dictTests', 'CounterTests', 'OrderedDictTests', 'defaultdictTests')
