#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test against the simplistic ModuloN class."""

import unittest

from hypothesis import strategies as st

from generic_testing import *

from modulo_n import ModuloN, ModuloPow2


@Given(st.builds(ModuloN.digit, st.integers()))
class Test_ModuloN_digit(defaultGenericTestLoader.discover(ModuloN)):
    zero = ModuloN.digit(0)
    one = ModuloN.digit(1)


class ModuloPow2Tests(defaultGenericTestLoader.discover(ModuloPow2)):
    @property
    def bottom(self): return self.zero 
    @property
    def top(self): return ~self.zero


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
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloN_digit))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloPow2_bit))
    SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ModuloPow2_short))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
