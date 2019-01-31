#!/usr/bin/env python3
# Copyright 2018 Steve Palmer

"""A test of the generic_test.built_in_file_like_tests using the built-in file-like types."""

import unittest
import io
import tempfile

from hypothesis import strategies as st

from generic_testing import *


def _make_raw_temp_file(b: bytes):
    result = tempfile.TemporaryFile(buffering=0)
    result.write(b)
    result.seek(0)
    return result


@Given({ClassUnderTest: st.builds(_make_raw_temp_file), int: st.integers(), bytes: st.binary()})
class Test_FileIO(FileIOTests):
    pass


def _make_buffered_temp_file(b: bytes):
    result = tempfile.TemporaryFile()
    result.write(b)
    result.seek(0)
    return result


@Given({ClassUnderTest: st.builds(_make_buffered_temp_file), int: st.integers(), bytes: st.binary()})
class Test_BufferedIO(BufferedIOBaseTests):
    pass


@Given({ClassUnderTest: st.builds(io.BytesIO)})
class Test_BytesIO(BytesIOTests):
    pass


def _make_text_temp_file(s: str):
    result = tempfile.TemporaryFile('w+t')
    result.write(s)
    result.seek(0)
    return result


@Given({ClassUnderTest: st.builds(_make_text_temp_file), int: st.integers(), str: st.text()})
class Test_TextIO(TextIOBaseTests):
    pass


@Given({ClassUnderTest: st.builds(io.StringIO)})
class Test_StringIO(StringIOTests):
    pass


__all__ = ('Test_FileIO', 'Test_BufferedIO', 'Test_BytesIO', 'Test_TextIO', 'Test_StringIO')


if __name__ == '__main__':
    SUITE = unittest.TestSuite()
    name = None
    value = None
    for name, value in locals().items():
        if name.startswith('Test_'):
            SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    TR = unittest.TextTestRunner(verbosity=2)
    TR.run(SUITE)
