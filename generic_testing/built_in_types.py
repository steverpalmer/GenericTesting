# Copyright 2021 Steve Palmer

"""A library of generic test for the python built-in types."""

import collections
from functools import wraps
import fractions
import types

from hypothesis import assume

from .isclose import IsClose, isclose
from .core import ClassUnderTest
from .relations import EqualityTests, TotalOrderingTests
from .arithmetic import AdditionMonoidTests, ScalarT
from .numbers_abc import IntegralTests, RationalTests, RealTests, ComplexTests
from .collections_abc import (
    ElementT,
    HashableMixinTests,
    SetTests,
    KeysViewTests,
    ItemsViewTests,
    ValuesViewTests,
    MutableSetTests,
    MappingTests,
    MutableMappingTests,
    SequenceTests,
    MutableSequenceTests,
)
from .augmented_assignment import (
    ComplexAugmentedAssignmentMixinTests,
    FloorDivAugmentedAssignmentMixinTests,
    IntegralAugmentedAssignmentMixinTests,
    LatticeWithComplementAugmentedAssignmentMixinTests,
)


__all__ = (
    "intTests",
    "FractionTests",
    "floatTests",
    "complexTests",
    "frozensetTests",
    "setTests",
    "dictKeysViewTests",
    "dictItemsViewTests",
    "dictValuesViewTests",
    "MappingProxyTypeTests",
    "dictTests",
    "CounterTests",
    "OrderedDictTests",
    "defaultdictTests",
    "tupleTests",
    "listTests",
)


class intTests(
    IntegralAugmentedAssignmentMixinTests,
    FloorDivAugmentedAssignmentMixinTests,
    LatticeWithComplementAugmentedAssignmentMixinTests,
    IntegralTests,
):
    """Tests of int class properties."""

    zero = 0
    one = 1

    # To avoid << and >> related test killing performance,
    # restrict the test range on b or [0 .. 63]

    @wraps(IntegralTests.test_generic_2390_lshift_definition)
    def test_generic_2390_lshift_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        super().test_generic_2390_lshift_definition(a, b & 63)

    @wraps(IntegralTests.test_generic_2391_rshift_definition)
    def test_generic_2391_rshift_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        super().test_generic_2391_rshift_definition(a, b & 63)

    @wraps(IntegralAugmentedAssignmentMixinTests.test_generic_2392_ilshift_definition)
    def test_generic_2392_ilshift_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ):
        super().test_generic_2392_ilshift_definition(a, b & 63)

    @wraps(IntegralAugmentedAssignmentMixinTests.test_generic_2393_irshift_definition)
    def test_generic_2393_irshift_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ):
        super().test_generic_2393_irshift_definition(a, b & 63)

    # TODO: tests for bit_length, to_bytes, from_bytes


class FractionTests(
    ComplexAugmentedAssignmentMixinTests,
    FloorDivAugmentedAssignmentMixinTests,
    RationalTests,
):
    """Tests of Fraction class properties."""

    zero = fractions.Fraction(0)
    one = fractions.Fraction(1)
    half = fractions.Fraction(1, 2)


class floatTests(
    ComplexAugmentedAssignmentMixinTests,
    FloorDivAugmentedAssignmentMixinTests,
    RealTests,
):
    """Tests of float class properties."""

    zero = 0.0
    one = 1.0
    root_two = 2.0 ** 0.5

    @wraps(RealTests.test_generic_2220_addition_associativity)
    def test_generic_2220_addition_associativity(
        self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest
    ) -> None:
        rel_tol = 1e-7
        assume(
            not isclose(abs(a), abs(b), rel_tol=rel_tol)
            and not isclose(abs(b), abs(c), rel_tol=rel_tol)  # noqa W504
        )
        super().test_generic_2220_addition_associativity(a, b, c)

    @wraps(RealTests.test_generic_2237_multiplication_addition_left_distributivity)
    def test_generic_2237_multiplication_addition_left_distributivity(
        self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest
    ) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(
            not isclose(
                b,
                -c,
                rel_tol=isclose.default_rel_tol ** 0.5,
                abs_tol=isclose.default_abs_tol * 100.0,
            )
        )
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    @wraps(RealTests.test_generic_2274_abs_is_subadditive)
    def test_generic_2274_abs_is_subadditive(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))

    # TODO: tests for as_integer_ratio, is_integer, hex, fromhex


class complexTests(ComplexAugmentedAssignmentMixinTests, ComplexTests):
    """Tests of complex class properties."""

    zero = complex(0)
    one = complex(1)
    i = complex(0, 1)

    @wraps(ComplexTests.test_generic_2237_multiplication_addition_left_distributivity)
    def test_generic_2237_multiplication_addition_left_distributivity(
        self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest
    ) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(
            not isclose(
                b,
                -c,
                rel_tol=isclose.default_rel_tol ** 0.5,
                abs_tol=isclose.default_abs_tol * 100.0,
            )
        )
        super().test_generic_2237_multiplication_addition_left_distributivity(a, b, c)

    @wraps(ComplexTests.test_generic_2238_multiplication_addition_right_distributivity)
    def test_generic_2238_multiplication_addition_right_distributivity(
        self, a: ClassUnderTest, b: ClassUnderTest, c: ClassUnderTest
    ) -> None:
        # :FUDGE: this consistently fails when b is close to -c due to the limitations of floating point numbers.
        # Therefore, continue the test only when the b is not close of -c
        assume(
            not isclose(
                b,
                -c,
                rel_tol=isclose.default_rel_tol ** 0.5,
                abs_tol=isclose.default_abs_tol * 100.0,
            )
        )
        super().test_generic_2238_multiplication_addition_right_distributivity(a, b, c)

    @wraps(ComplexTests.test_generic_2274_abs_is_subadditive)
    def test_generic_2274_abs_is_subadditive(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        self.assertCloseOrLessThan(abs(a + b), abs(a) + abs(b))


class _frozensetTests(SetTests):
    """Tests of frozenset class inheritable properties."""

    empty = frozenset()

    def test_generic_2600_issubset_defintion(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.issubset(b) ⇔ a <= b"""
        self.assertEqual(a.issubset(b), a <= b)

    def test_generic_2601_isuperset_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.issuperset(b) ⇔ b <= a"""
        self.assertEqual(a.issuperset(b), b <= a)

    def test_generic_2602_union_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.union(b) == a | b"""
        self.assertEqual(a.union(b), a | b)

    def test_generic_2603_intersection_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.intersection(b) == a & b"""
        self.assertEqual(a.intersection(b), a & b)

    def test_generic_2604_difference_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.difference(b) == a - b"""
        self.assertEqual(a.difference(b), a - b)

    def test_generic_2605_symmetric_difference_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a.symmetric_difference(b) == a ^ b"""
        self.assertEqual(a.symmetric_difference(b), a ^ b)


class frozensetTests(HashableMixinTests, _frozensetTests):
    """Tests of frozenset class properties."""


class setTests(MutableSetTests, _frozensetTests):
    """Tests of set class properties."""

    empty = set()

    def copy(self, s: ClassUnderTest) -> ClassUnderTest:
        return s.copy()

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

    def test_generic_2505_update_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """Test update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a |= b
        self.assertEqual(a, a_copy | b)
        a_nother.update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2610_intersection_update_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """Test intersection_update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a &= b
        self.assertEqual(a, a_copy & b)
        a_nother.intersection_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2611_difference_update_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """Test difference_update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a -= b
        self.assertEqual(a, a_copy - b)
        a_nother.difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2612_symmetric_difference_update_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """Test symmetric_difference_update method"""
        a_copy = a.copy()
        a_nother = a.copy()
        a ^= b
        self.assertEqual(a, a_copy ^ b)
        a_nother.symmetric_difference_update(b)
        self.assertEqual(a, a_nother)

    def test_generic_2613_remove_definition(
        self, a: ClassUnderTest, b: ElementT
    ) -> None:
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


class dictItemsViewTests(ItemsViewTests):
    """Tests of dict ItemsView class properties."""

    empty = dict().items()


class dictValuesViewTests(ValuesViewTests):
    """Tests of dict ValuesView class properties."""


class MappingProxyTypeTests(MappingTests):
    """Tests of MappingProxyType class properties."""

    empty = types.MappingProxyType(dict())


class dictTests(MutableMappingTests):
    """Tests of dict class properties."""

    empty = dict()

    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        return a.copy()


class CounterTests(dictTests):
    """Tests of Counter class properties."""

    empty = collections.Counter()

    def test_generic_2505_update_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
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


class _tupleTests(
    EqualityTests, TotalOrderingTests, SequenceTests, AdditionMonoidTests
):
    """Tests of tuple class inheritable properties."""

    empty = tuple()

    @property
    def zero(self):
        return self.empty

    def test_generic_2110_equality_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a == b ⇔ a[i] == b[i]"""
        expected = True
        if len(a) != len(b):
            expected = False
        else:
            i = 0
            while i < len(a):
                if a[i] != b[i]:
                    expected = False
                    break
                i += 1
        self.assertEqual(a == b, expected)

    def test_generic_2145_less_or_equal_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """a <= b ⇔ a[j] <= b[j] and for i < j: a[i] == b[i]"""
        a_len = len(a)
        b_len = len(b)
        i_max = a_len if a_len <= b_len else b_len
        i = 0
        while i < i_max:
            if not a[i] == b[i]:
                break
            i += 1
        if i == a_len:
            expected = True
        elif i == b_len:
            expected = False
        else:
            expected = a[i] <= b[i]
        self.assertEqual(a <= b, expected)

    def test_generic_2239_multiplication_commutativity(
        self, r: ScalarT, a: ClassUnderTest
    ) -> None:
        """r * a == a * r"""
        self.assertEqual(r * a, a * r)

    def test_generic_2620_add_definition(
        self, a: ClassUnderTest, b: ClassUnderTest
    ) -> None:
        """(a + b)[i] == a[i] if i < len(a) else b[i - len(a)]"""
        a_len = len(a)
        c = a + b
        self.assertEqual(len(c), a_len + len(b))
        i = 0
        for x in c:
            self.assertEqual(x, a[i] if i < a_len else b[i - a_len])
            i += 1

    def test_generic_2621_mul_definition(self, a: ClassUnderTest, b: ScalarT) -> None:
        """(a * b)[i] == a[i % len(a)]"""
        a_len = len(a)
        c = a * b
        b = max(b, 0)  # clipped
        self.assertEqual(len(c), a_len * b)
        i = 0
        for x in c:
            self.assertEqual(x, a[i % a_len])
            i += 1

    def test_generic_2622_min_definition(self, a: ClassUnderTest) -> None:
        """min(a) in a and min(a) <= a[i]"""
        if len(a) > 0:
            try:
                a_min = min(a)
            except TypeError:
                return  # min not accept the supplied types
            self.assertTrue(a_min in a)
            for x in a:
                self.assertLessEqual(a_min, x)
        else:
            with self.assertRaises(ValueError):
                min(a)

    def test_generic_2623_max_definition(self, a: ClassUnderTest) -> None:
        """max(a) in a and a[i] <= max(a)"""
        if len(a) > 0:
            try:
                a_max = max(a)
            except TypeError:
                return  # max not accept the supplied types
            self.assertTrue(a_max in a)
            for x in a:
                self.assertLessEqual(x, a_max)
        else:
            with self.assertRaises(ValueError):
                min(a)


class tupleTests(HashableMixinTests, _tupleTests):
    """Tests of tuple class properties."""


class listTests(_tupleTests, MutableSequenceTests):
    """Tests of list class properties."""

    empty = list()

    def copy(self, a: ClassUnderTest) -> ClassUnderTest:
        return a.copy()

    def test_generic_2630_clear_definition(self, a: ClassUnderTest) -> None:
        """a.clear(); a == list()"""
        a.clear()
        self.assertEqual(a, self.empty)

    def test_generic_2631_copy_definition(self, a: ClassUnderTest) -> None:
        """a_copy = a.copy(); a_copy == a and id(a_copy) != id(a)"""
        a_copy = a.copy()
        self.assertEqual(a_copy, a)
        self.assertNotEqual(id(a_copy), id(a))

    def test_generic_2632_imul_definition(self, a: ClassUnderTest, b: ScalarT) -> None:
        """a *= b; a == a₀ * b"""
        a_copy = self.copy(a)
        a *= b
        self.assertEqual(a, a_copy * b)
