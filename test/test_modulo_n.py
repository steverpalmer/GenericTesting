#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test against the simplistic ModuloN class."""

import unittest

from hypothesis import strategies as st

from generic_testing import *

from modulo_n import ModuloN, ModuloPow2


class ModuloNTests(EqualityTests, TotalOrderingTests, FieldTests, FloorDivModTests, AbsoluteValueTests):

    @unittest.skip("abs is not multiplicitive in this class")
    def test_generic_2273_abs_is_multiplicitive(self):
        pass


@Given(st.builds(ModuloN.digit, st.integers()))
class Test_ModuloN_digit(ModuloNTests):
    zero = ModuloN.digit(0)
    one = ModuloN.digit(1)


class ModuloPow2Tests(ModuloNTests, LatticeWithComplement):

    @property
    def bottom(self):
        return self.zero

    @property
    def top(self):
        return -self.one


@Given(st.builds(ModuloPow2.bit, st.integers()))
class Test_ModuloPow2_bit(ModuloPow2Tests):
    zero = ModuloPow2.bit(0)
    one = ModuloPow2.bit(1)


@Given(st.builds(ModuloPow2.short, st.integers()))
class Test_ModuloPow2_short(ModuloPow2Tests):
    zero = ModuloPow2.short(0)
    one = ModuloPow2.short(1)


if __name__ == '__main__':
    # Run the tests
    SUITE = unittest.TestSuite()
    name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=1)
    TR.run(SUITE)
