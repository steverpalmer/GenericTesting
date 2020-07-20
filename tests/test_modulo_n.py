#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test against the simplistic ModuloN class."""

import unittest

from hypothesis import strategies as st

from modulo_n import ModuloN, ModuloPow2

from generic_testing_test_context import generic_testing


@generic_testing.Given(st.builds(ModuloN.decimal_digit, st.integers()))
class Test_ModuloN_decimal_digit(
    generic_testing.defaultGenericTestLoader.discover(ModuloN, use_docstring_yaml=True)
):
    zero = ModuloN.decimal_digit(0)
    one = ModuloN.decimal_digit(1)


class ModuloPow2Tests(
    generic_testing.defaultGenericTestLoader.discover(
        ModuloPow2, use_docstring_yaml=True
    )
):
    @property
    def bottom(self):
        return self.zero

    @property
    def top(self):
        return -self.one


@generic_testing.Given(st.builds(ModuloPow2.bit, st.integers()))
class Test_ModuloPow2_bit(ModuloPow2Tests):
    zero = ModuloPow2.bit(0)
    one = ModuloPow2.bit(1)


@generic_testing.Given(st.builds(ModuloPow2.u16, st.integers()))
class Test_ModuloPow2_u16(ModuloPow2Tests):
    zero = ModuloPow2.u16(0)
    one = ModuloPow2.u16(1)


if __name__ == "__main__":
    # Run the tests
    SUITE = unittest.TestSuite()
    SUITE.addTest(
        unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloN_decimal_digit)
    )
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloPow2_bit))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloPow2_u16))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
