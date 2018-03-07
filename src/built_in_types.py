# Copyright 2018 Steve Palmer

"""A library of generic test for the python built-in types."""

import fractions
import types
import collections
from functools import wraps

from hypothesis import assume

from .isclose import IsClose
from .core import ClassUnderTest
from .numbers_abc import IntegralTests, RationalTests, RealTests, ComplexTests
from .collections_abc import (ElementT, ValueT, SetTests, KeysViewTests, ItemsViewTests, ValuesViewTests,
                              MutableSetTests, MappingTests, MutableMappingTests)
from .augmented_assignment import (ComplexAugmentedAssignmentTests, FloorDivAugmentedAssignmentTests,
                                   IntegralAugmentedAssignmentTests, LatticeWithComplementAugmentedTests)


class intTests(IntegralTests, IntegralAugmentedAssignmentTests, FloorDivAugmentedAssignmentTests, LatticeWithComplementAugmentedTests):
    """Tests of int class properties."""

    zero = 0
    one = 1

    def test_generic_2020_zero_type(self):
        self.assertIsInstance(self.zero, int)

    def test_generic_2021_one_type(self):
        self.assertIsInstance(self.one, int)

    # To avoid << and >> related test killing performance,
    # restrict the test range on b or [0 .. 63]

    @wraps(IntegralTests.test_generic_2390_lshift_definition)
    def test_generic_2390_lshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        super().test_generic_2390_lshift_definition(a, b & 63)

    @wraps(IntegralTests.test_generic_2391_rshift_definition)
    def test_generic_2391_rshift_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        super().test_generic_2391_rshift_definition(a, b & 63)

    @wraps(IntegralAugmentedAssignmentTests.test_generic_2392_ilshift_definition)
    def test_generic_2392_ilshift_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        super().test_generic_2392_ilshift_definition(a, b & 63)

    @wraps(IntegralAugmentedAssignmentTests.test_generic_2393_irshift_definition)
    def test_generic_2393_irshift_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        super().test_generic_2393_irshift_definition(a, b & 63)

    # TODO: tests for bit_length, to_bytes, from_bytes


class FractionTests(RationalTests, ComplexAugmentedAssignmentTests, FloorDivAugmentedAssignmentTests):
    """Tests of Fraction class properties."""

    zero = fractions.Fraction(0)
    one = fractions.Fraction(1)
    half = fractions.Fraction(1, 2)

    def test_generic_2020_zero_type(self):
        self.assertIsInstance(self.zero, fractions.Fraction)

    def test_generic_2021_one_type(self):
        self.assertIsInstance(self.one, fractions.Fraction)

    def test_generic_2022_half_type(self):
        self.assertIsInstance(self.half, fractions.Fraction)


class floatTests(RealTests, ComplexAugmentedAssignmentTests, FloorDivAugmentedAssignmentTests):
    """Tests of float class properties."""

    zero = 0.0
    one = 1.0
    root_two = 2.0 ** 0.5

    def test_generic_2020_zero_type(self):
        self.assertIsInstance(self.zero, float)

    def test_generic_2021_one_type(self):
        self.assertIsInstance(self.one, float)

    def test_generic_2023_root_two_type(self):
        self.assertIsInstance(self.root_two, float)

    @wraps(RealTests.test_generic_2220_addition_associativity)
    def test_generic_2220_addition_associativity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        assume(not self.isclose(a, b) and not self.isclose(b, c))
        super().test_generic_2220_addition_associativity(a, b, c)

    @wraps(RealTests.test_generic_2237_multiplication_addition_left_distributivity)
    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    @wraps(RealTests.test_generic_2274_abs_is_subadditive)
    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))

    # TODO: tests for as_integer_ratio, is_integer, hex, fromhex


class complexTests(ComplexTests, ComplexAugmentedAssignmentTests):
    """Tests of complex class properties."""

    zero = complex(0)
    one = complex(1)
    i = complex(0, 1)

    def test_generic_2020_zero_type(self):
        self.assertIsInstance(self.zero, complex)

    def test_generic_2021_one_type(self):
        self.assertIsInstance(self.one, complex)

    def test_generic_2024_i_type(self):
        self.assertIsInstance(self.i, complex)

    @wraps(ComplexTests.test_generic_2237_multiplication_addition_left_distributivity)
    def test_generic_2237_multiplication_addition_left_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    @wraps(ComplexTests.test_generic_2238_multiplication_addition_right_distributivity)
    def test_generic_2238_multiplication_addition_right_distributivity(self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(not IsClose.over_numbers(b, -c, rel_tol=self.isclose.rel_tol ** 0.5, abs_tol=self.isclose.abs_tol * 100.0))
        super().test_generic_2238_multiplication_addition_right_distributivity(a, b, c)

    @wraps(ComplexTests.test_generic_2274_abs_is_subadditive)
    def test_generic_2274_abs_is_subadditive(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))


class frozensetTests(SetTests):
    """Tests of frozenset class properties."""

    empty = frozenset()

    def test_generic_2010_empty_type(self) -> None:
        self.assertIsInstance(self.empty, frozenset)

    def test_generic_2600_issubset_defintion(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a.issubset(b) ⇔ a <= b"""
        self.assertEqual(a.issubset(b), a <= b)

    def test_generic_2601_isuperset_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a.issuperset(b) ⇔ b <= a"""
        self.assertEqual(a.issuperset(b), b <= a)

    def test_generic_2602_union_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a.union(b) == a | b"""
        self.assertEqual(a.union(b), a | b)

    def test_generic_2603_intersection_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a.intersection(b) == a & b"""
        self.assertEqual(a.intersection(b), a & b)

    def test_generic_2604_difference_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a.difference(b) == a - b"""
        self.assertEqual(a.difference(b), a - b)

    def test_generic_2605_symmetric_difference_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """a.symmetric_difference(b) == a ^ b"""
        self.assertEqual(a.symmetric_difference(b), a ^ b)


class setTests(MutableSetTests, frozensetTests):
    """Tests of set class properties."""

    empty = set()

    def copy(self, s: ClassUnderTest) -> ClassUnderTest:
        return s.copy()

    def singleton_constructor(self, a: ElementT) -> ClassUnderTest:
        return set([a])

    def test_generic_2010_empty_type(self) -> None:
        self.assertIsInstance(self.empty, set)

    def test_generic_2502_pop_definition(self, a: ClassUnderTest) -> None:
        """Test pop method"""
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

    def test_generic_2504_clear_definition(self, a: ClassUnderTest) -> None:
        """Test clear method"""
        a.clear()
        self.assertEqual(a, self.empty)

    def test_generic_2505_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """Test update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a |= b
        self.assertEqual(a, a_copy | b)
        a_nother.update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2610_intersection_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """Test intersection_update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a &= b
        self.assertEqual(a, a_copy & b)
        a_nother.intersection_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2611_difference_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """Test difference_update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a -= b
        self.assertEqual(a, a_copy - b)
        a_nother.difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2612_symmetric_difference_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """Test symmetric_difference_update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a ^= b
        self.assertEqual(a, a_copy ^ b)
        a_nother.symmetric_difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2613_remove_definition(self, a: ClassUnderTest, b: ElementT) -> None:
        """Test remove method"""
        a.add(b)
        a_copy = a.copy()
        a.remove(b)
        a_copy.discard(b)
        self.assertEqual(a, a_copy)
        with self.assertRaises(KeyError):
            a.remove(b)


class dictKeysViewTests(KeysViewTests):
    """Tests of dict KeysView class properties."""

    empty = dict().keys()

    def test_generic_2010_empty_type(self) -> None:
        pass


class dictItemsViewTests(ItemsViewTests):
    """Tests of dict ItemsView class properties."""

    empty = dict().items()

    def test_generic_2010_empty_type(self) -> None:
        pass


class dictValuesViewTests(ValuesViewTests):
    """Tests of dict ValuesView class properties."""


class MappingProxyTypeTests(MappingTests):
    """Tests of MappingProxyType class properties."""

    empty = types.MappingProxyType(dict())

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return types.MappingProxyType({a: b})

    def test_generic_2010_empty_type(self) -> None:
        self.assertIsInstance(self.empty, types.MappingProxyType)


class dictTests(MutableMappingTests):
    """Tests of dict class properties."""

    empty = dict()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return {a: b}

    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        return a.copy()

    def test_generic_2010_empty_type(self) -> None:
        self.assertIsInstance(self.empty, dict)


class CounterTests(dictTests):
    """Tests of Counter class properties."""

    empty = collections.Counter()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.Counter({a: b})

    def test_generic_2010_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.Counter)

    def test_generic_2505_update_definition(self, a: ClassUnderTest, b: ClassUnderTest) -> None:
        """Test Counter update method"""
        a_copy = self.copy(a)
        a.update(b)
        self.assertLessEqual(b.keys(), a.keys())
        for k in a:
            self.assertEqual(a[k], b[k] + a_copy[k])

    # TODO: add tests for Counter specific methods


class OrderedDictTests(dictTests):
    """Tests of OrderedDict class properties."""

    empty = collections.OrderedDict()

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.OrderedDict([(a, b)])

    def test_generic_2010_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.OrderedDict)

    # TODO: add tests for OrderedDict specific features and methods


class defaultdictTests(dictTests):
    """Tests of defaultdict class properties."""

    def __init__(self, default_factory, methodName=None):
        """add default_factory parameter to test constructor."""
        super().__init__(methodName)
        self._default_factory = default_factory

    @property
    def empty(self):
        return collections.defaultdict(self._default_factory)

    def singleton_constructor(self, a: ElementT, b: ValueT) -> ClassUnderTest:
        return collections.defaultdict(self._default_factory, [(a, b)])

    def test_generic_2010_empty_type(self) -> None:
        self.assertIsInstance(self.empty, collections.defaultdict)


__all__ = ('intTests', 'FractionTests', 'floatTests', 'complexTests',
           'frozensetTests', 'setTests',
           'dictKeysViewTests', 'dictItemsViewTests', 'dictValuesViewTests', 'MappingProxyTypeTests',
           'dictTests', 'CounterTests', 'OrderedDictTests', 'defaultdictTests')
