# Copyright 2018 Steve Palmer

"""A library of generic test for the augmented assignment operators."""

from hypothesis import assume

from .core import GenericTests, ClassUnderTest


class LatticeAugmentedAssignmentTests(GenericTests):
    """Tests of the __ior__ and __iand__ assignment operators."""

    def test_generic_2280_ior_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a |= b; a == a₀ | b"""
        a_expected = a | b
        a |= b
        self.assertEqual(a, a_expected)

    def test_generic_2281_iand_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a &= b; a == a₀ & b"""
        a_expected = a & b
        a &= b
        self.assertEqual(a, a_expected)


class LatticeWithComplementAugmentedTests(LatticeAugmentedAssignmentTests):
    """Tests of the lattice assignment operators."""

    def test_generic_2282_isub_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a -= b; a == a₀ - b"""
        a_expected = a - b
        a -= b
        self.assertEqual(a, a_expected)

    def test_generic_2283_ixor_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a ^= b; a == a₀ ^ b"""
        a_expected = a ^ b
        a ^= b
        self.assertEqual(a, a_expected)


class ComplexAugmentedAssignmentTests(GenericTests):
    """Tests of the basic arithmetic assignment operators."""

    def test_generic_2282_isub_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a -= b; a == a₀ - b"""
        a_expected = a - b
        a -= b
        self.assertEqual(a, a_expected)

    def test_generic_2284_iadd_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a += b; a == a₀ + b"""
        a_expected = a + b
        a += b
        self.assertEqual(a, a_expected)

    def test_generic_2285_imul_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a *= b; a == a₀ * b"""
        a_expected = a * b
        a *= b
        self.assertEqual(a, a_expected)

    def test_generic_2286_itruediv_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a /= b; a == a₀ / b"""
        assume(not b == self.zero)
        a_expected = a / b
        a /= b
        self.assertEqual(a, a_expected)


class FloorDivAugmentedAssignmentTests(GenericTests):
    """Tests of the __ifloor__ and __imod__ assignment operators."""

    def test_generic_2287_ifloordiv_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a //= b; a == a₀ // b"""
        assume(not b == self.zero)
        a_expected = a // b
        a //= b
        self.assertEqual(a, a_expected)

    def test_generic_2288_imod_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """a %= b; a == a₀ % b"""
        assume(not b == self.zero)
        a_expected = a % b
        a %= b
        self.assertEqual(a, a_expected)


class IntegralAugmentedAssignmentTests(ComplexAugmentedAssignmentTests):
    """Tests of the integer arithmetic assignment operators."""

    def test_generic_2392_ilshift_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """0 <= b ⇒ a <<= b; a == a₀ << b"""
        assume(self.zero <= b)
        a_expected = a << b
        a <<= b
        self.assertEqual(a, a_expected)

    def test_generic_2393_irshift_definition(self, a: ClassUnderTest, b: ClassUnderTest):
        """0 <= b ⇒ a >>= b; a == a₀ >> b"""
        assume(self.zero <= b)
        a_expected = a >> b
        a >>= b
        self.assertEqual(a, a_expected)


__all__ = ('LatticeAugmentedAssignmentTests', 'LatticeWithComplementAugmentedTests',
           'ComplexAugmentedAssignmentTests', 'FloorDivAugmentedAssignmentTests',
           'IntegralAugmentedAssignmentTests')
