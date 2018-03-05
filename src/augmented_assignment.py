"""
Copyright 2018 Steve Palmer

A library of generic test for the augmented assignment operators...
 * __ior__, __iand__
 * __iadd__, __isub__, __imul__, __itruediv__, etc
"""

import abc

from hypothesis import assume

from .core import GenericTests, ClassUnderTest


class LatticeAugmentedAssignmentTests(GenericTests):

    def test_generic_2280_ior_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        a_expected = a | b
        a |= b
        self.assertEqual(a, a_expected)

    def test_generic_2281_iand_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        a_expected = a & b
        a &= b
        self.assertEqual(a, a_expected)


class LatticeWithComplementAugmentedTests(LatticeAugmentedAssignmentTests):

    def test_generic_2282_isub_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        a_expected = a - b
        a -= b
        self.assertEqual(a, a_expected)

    def test_generic_2283_ixor_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        a_expected = a ^ b
        a ^= b
        self.assertEqual(a, a_expected)


class ComplexAugmentedAssignmentTests(GenericTests):

    def test_generic_2282_isub_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        a_expected = a - b
        a -= b
        self.assertEqual(a, a_expected)

    def test_generic_2284_iadd_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        a_expected = a + b
        a += b
        self.assertEqual(a, a_expected)

    def test_generic_2285_imul_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        a_expected = a * b
        a *= b
        self.assertEqual(a, a_expected)

    def test_generic_2286_itruediv_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        assume(not b == self.zero)
        a_expected = a / b
        a /= b
        self.assertEqual(a, a_expected)


class FloorDivAugmentedAssignmentTests(GenericTests):

    def test_generic_2287_ifloordiv_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        assume(not b == self.zero)
        a_expected = a // b
        a //= b
        self.assertEqual(a, a_expected)

    def test_generic_2288_imod_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        assume(not b == self.zero)
        a_expected = a % b
        a %= b
        self.assertEqual(a, a_expected)


class IntegralAugmentedAssignmentTests(ComplexAugmentedAssignmentTests):

    def test_generic_2392_ilshift_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        assume(self.zero <= b)
        a_expected = a << b
        a <<= b
        self.assertEqual(a, a_expected)

    def test_generic_2393_irshift_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        assume(self.zero <= b)
        a_expected = a >> b
        a >>= b
        self.assertEqual(a, a_expected)


__all__ = ('LatticeAugmentedAssignmentTests', 'LatticeWithComplementAugmentedTests',
           'ComplexAugmentedAssignmentTests', 'FloorDivAugmentedAssignmentTests',
           'IntegralAugmentedAssignmentTests')
