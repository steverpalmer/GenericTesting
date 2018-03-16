#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test against the simplistic ModuloN class."""

import unittest

from hypothesis import strategies as st

from generic_testing import ClassUnderTest, Given, EqualityTests, PartialOrderingTests, FieldTests, AbsoluteValueTests, \
    TotalOrderingTests, LatticeWithComplementTests, FloorDivModTests, ExponentiationTests, BitShiftTests

from modulo_n import ModuloN, ModuloPow2


class ModuloNTests(EqualityTests, PartialOrderingTests, AbsoluteValueTests):

    def test_generic_2273_abs_is_multiplicitive(self):
        pass


@Given(st.builds(ModuloN, st.integers(min_value=1), st.integers()))
class Test_ModuloN(ModuloNTests):
    zero = 0
    one = 1


class ModuloNSingleModulusTests(ModuloNTests, TotalOrderingTests, FieldTests, FloorDivModTests, ExponentiationTests):
    pass


@Given(st.builds(ModuloN.digit, st.integers()))
class Test_ModuloN_digit(ModuloNSingleModulusTests):
    zero = ModuloN.digit(0)
    one = ModuloN.digit(1)


class ModuloSinglePow2Tests(ModuloNSingleModulusTests, LatticeWithComplementTests, BitShiftTests):

    @property
    def bottom(self):
        return self.zero

    @property
    def top(self):
        return -self.one

    def test_generic_2391_rshift_definition(self) -> None:
        pass

@Given(st.builds(ModuloPow2.bit, st.integers()))
class Test_ModuloPow2_bit(ModuloSinglePow2Tests):
    zero = ModuloPow2.bit(0)
    one = ModuloPow2.bit(1)


@Given(st.builds(ModuloPow2.short, st.integers()))
class Test_ModuloPow2_short(ModuloSinglePow2Tests):
    zero = ModuloPow2.short(0)
    one = ModuloPow2.short(1)


if __name__ == '__main__':
    # Run the tests
    SUITE = unittest.TestSuite()
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloN))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloN_digit))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloPow2_bit))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloPow2_short))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
