#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A library of generic test for the python built-in types.
"""

import fractions
import unittest

from hypothesis import assume, strategies as st

from isclose import IsClose
from core import Given, ClassUnderTest
from numbers_abc import *
from collections_abc import ElementT, SetTests, MutableSetTests, KeysViewTests, ItemsViewTests, ValuesViewTests

#=======================================================================================================================
# Unbound tests
#=======================================================================================================================


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
                _ = a.pop()

    def test_generic_2616_clear_definition(self, a: ClassUnderTest) -> None:
        a.clear()
        self.assertEqual(a, self.empty)


class dictKeysViewTests(KeysViewTests):

    empty = dict().keys()


class dictItemsViewTests(ItemsViewTests):

    empty = dict().items()


class dictValuesViewTests(ValuesViewTests):
    pass


__all__ = ('intTests', 'FractionTests', 'floatTests', 'complexTests',
           'frozensetTests', 'setTests',
           'dictKeysViewTests', 'dictItemsViewTests', 'dictValuesViewTests')



if __name__ == '__main__':

#=======================================================================================================================
# Bound tests
#=======================================================================================================================

    @Given({ClassUnderTest: st.integers()})
    class Test_int(intTests):
        pass

    FRACTIONS_RANGE = 10000000000

    @Given({ClassUnderTest: st.fractions(min_value=fractions.Fraction(-FRACTIONS_RANGE),
                                         max_value=fractions.Fraction(FRACTIONS_RANGE),
                                         max_denominator=FRACTIONS_RANGE)})
    class Test_Fraction(FractionTests):
        pass

    FLOATS_RANGE = 1e30

    @Given({ClassUnderTest: st.floats(min_value=-FLOATS_RANGE, max_value=FLOATS_RANGE)})
    class Test_float(floatTests):
        pass

    # :TODO: This is under consideration (https://github.com/HypothesisWorks/hypothesis-python/issues/1076), but here's my quick&dirty attempt
    @st.cacheable
    @st.base_defines_strategy(True)
    def complex_numbers(min_real_value=None, max_real_value=None, min_imag_value=None, max_imag_value=None, allow_nan=None, allow_infinity=None):
        """Returns a strategy that generates complex numbers.

        Examples from this strategy shrink by shrinking their component real
        and imaginary parts.

        """
        from hypothesis.searchstrategy.numbers import ComplexStrategy
        return ComplexStrategy(
            st.tuples(
                st.floats(min_value=min_real_value, max_value=max_real_value, allow_nan=allow_nan, allow_infinity=allow_infinity),
                st.floats(min_value=min_imag_value, max_value=max_imag_value, allow_nan=allow_nan, allow_infinity=allow_infinity)))

    COMPLEX_RANGE = 1e10

    @Given({ClassUnderTest: complex_numbers(-COMPLEX_RANGE, COMPLEX_RANGE,
                                            -COMPLEX_RANGE, COMPLEX_RANGE,
                                            allow_nan=False, allow_infinity=False)})
    class Test_complex(complexTests):
        pass


    element_st = st.integers()
    @Given({ClassUnderTest: st.frozensets(element_st), ElementT: element_st})
    class Test_frozenset(frozensetTests):
        pass


    element_st = st.integers()
    @Given({ClassUnderTest: st.sets(element_st), ElementT: element_st})
    class Test_set(setTests):
        pass

    key_st = st.integers()
    value_st = st.integers()
    @Given({ClassUnderTest: st.builds(lambda m: m.keys(), st.dictionaries(key_st, value_st)), ElementT: key_st})
    class Test_dict_KeysView(dictKeysViewTests):
        pass


    key_st = st.integers()
    value_st = st.integers()
    @Given({ClassUnderTest: st.builds(lambda m: m.items(), st.dictionaries(key_st, value_st)), ElementT: key_st})
    class Test_dict_ItemsView(dictItemsViewTests):
        pass


    key_st = st.integers()
    value_st = st.integers()
    @Given({ClassUnderTest: st.builds(lambda m: m.values(), st.dictionaries(key_st, value_st)), ElementT: key_st})
    class Test_dict_ValuesView(dictValuesViewTests):
        pass


    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_int))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Fraction))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_float))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_complex))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_frozenset))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_set))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_KeysView))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_ItemsView))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_dict_ValuesView))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)

