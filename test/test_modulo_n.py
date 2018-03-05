#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A test of the generic_test against the simplistic ModuloN class
"""

import unittest

from hypothesis import strategies as st

from src import *

from modulo_n import ModuloN


class ModuloNTests(EqualityTests, FieldTests, LatticeWithComplement):

    @property
    def bottom(self):
        return self.zero

    @property
    def top(self):
        return -self.one

    unittest.skip("bottom is zero")
    def test_generic_2000_bottom_type(self):
        pass

    unittest.skip("top is -one")
    def test_generic_2001_top_type(self):
        pass

    def test_generic_2020_zero_type(self):
        self.assertIsInstance(self.zero, ModuloN)

    def test_generic_2021_one_type(self):
        self.assertIsInstance(self.one, ModuloN)


@Given(st.builds(ModuloN.bit, st.integers()))
class Test_ModuloN_bit(ModuloNTests):
    zero = ModuloN.bit(0)
    one = ModuloN.bit(1)
    bottom = zero
    top = one


@Given(st.builds(ModuloN.byte, st.integers()))
class Test_ModuloN_byte(ModuloNTests):
    zero = ModuloN.byte(0)
    one = ModuloN.byte(1)
    bottom = zero
    top = ModuloN.byte(-1)


@Given(st.builds(ModuloN.word, st.integers()))
class Test_ModuloN_word(ModuloNTests):
    zero = ModuloN.word(0)
    one = ModuloN.word(1)


if __name__ == '__main__':
    # Run the tests
    SUITE = unittest.TestSuite()
    name = None  # :TRICK: need to introdcue 'name' before iterating through locals
    value = None  # :TRICK: need to introdcue 'value' before iterating through locals
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
