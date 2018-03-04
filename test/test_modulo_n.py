#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A test of the generic_test against the simplistic ModuloN class
"""

import unittest

from hypothesis import strategies as st

from src import *

from modulo_n import ModuloN


@Given(st.builds(ModuloN.bit, st.integers()))
class Test_ModuloN_bit(EqualityTests, FieldTests, LatticeWithComplement):
    zero = ModuloN.bit(0)
    one = ModuloN.bit(1)
    real_zero = float(zero)

    bottom = zero
    top = one


@Given(st.builds(ModuloN.byte, st.integers()))
class Test_ModuloN_byte(EqualityTests, FieldTests, LatticeWithComplement):
    zero = ModuloN.byte(0)
    one = ModuloN.byte(1)
    real_zero = float(zero)

    bottom = zero
    top = ModuloN.byte(-1)


@Given(st.builds(ModuloN.word, st.integers()))
class Test_ModuloN_word(EqualityTests, FieldTests, LatticeWithComplement):
    zero = ModuloN.word(0)
    one = ModuloN.word(1)
    real_zero = float(zero)

    bottom = zero
    top = ModuloN.word(-1)


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
