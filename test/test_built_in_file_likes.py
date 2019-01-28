#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.built_in_file_like_tests using the built-in file-like types."""

import unittest
import io

from hypothesis import strategies as st

from generic_testing import *


@Given({ClassUnderTest: st.builds(io.BytesIO, st.binary())})
class Test_BinaryIO(IOBaseTests):
    pass


__all__ = ('Test_BinaryIO')


if __name__ == '__main__':
    SUITE = unittest.TestSuite()
    name = None
    value = None
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
