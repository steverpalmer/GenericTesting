#!/usr/bin/env python3
# Copyright 2021 Steve Palmer

"""A test of the generic_test.built_in_file_like_tests using the built-in file-like types."""

import unittest
import io
import tempfile

from hypothesis import strategies as st

from generic_testing_test_context import generic_testing


def _make_raw_temp_file(b: bytes):
    result = tempfile.TemporaryFile(buffering=0)
    result.write(b)
    result.seek(0)
    return result


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(_make_raw_temp_file),
        int: st.integers(),
        bytes: st.binary(),
    }
)
class Test_FileIO(generic_testing.FileIOTests):
    pass


def _make_buffered_temp_file(b: bytes):
    result = tempfile.TemporaryFile()
    result.write(b)
    result.seek(0)
    return result


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(_make_buffered_temp_file),
        int: st.integers(),
        bytes: st.binary(),
    }
)
class Test_BufferedIO(generic_testing.BufferedIOBaseTests):
    pass


def _make_buffered_reader_file(b: bytes):
    return io.BufferedReader(_make_raw_temp_file(b))


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(_make_buffered_reader_file),
        int: st.integers(),
        bytes: st.binary(),
    }
)
class Test_BufferedReader(generic_testing.BufferedIOBaseTests):
    pass


class Test_BufferedReader2(unittest.TestCase):
    def test_os_error(self):
        b = b"hello"
        f = tempfile.TemporaryFile()
        f.write(b)
        f.seek(0)
        OUT = io.BufferedReader(f)
        # Standard Library io module states:
        # writeable()
        #   Return True is the stream supports writing. If False, write() and truncate() will raise OSError.
        self.assertFalse(OUT.writable())
        with self.assertRaises(OSError):
            OUT.truncate(0)


def _make_buffered_writer_file(b: bytes):
    return io.BufferedWriter(_make_raw_temp_file(b))


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(_make_buffered_writer_file),
        int: st.integers(),
        bytes: st.binary(),
    }
)
class Test_BufferedWriter(generic_testing.BufferedIOBaseTests):
    pass


def _make_buffered_random_file(b: bytes):
    return io.BufferedRandom(_make_raw_temp_file(b))


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(_make_buffered_random_file),
        int: st.integers(),
        bytes: st.binary(),
    }
)
class Test_BufferedRandom(generic_testing.BufferedIOBaseTests):
    pass


def _make_buffered_pair_file(b: bytes):
    return io.BufferedRWPair(_make_raw_temp_file(b), _make_raw_temp_file(b))


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(_make_buffered_pair_file),
        int: st.integers(),
        bytes: st.binary(),
    }
)
class Test_BufferedRWPair(generic_testing.BufferedIOBaseTests):
    def test_generic_2591_detach(self, a: generic_testing.ClassUnderTest) -> None:
        """io.BufferedRWPair.detach"""
        # hypothesis.assume(not a.closed)
        with self.assertRaises(io.UnsupportedOperation):
            a.detach()


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(io.BytesIO),
        int: st.integers(),
        bytes: st.binary(),
    }
)
class Test_BytesIO(generic_testing.BytesIOTests):
    pass


def _make_text_temp_file(s: str):
    result = tempfile.TemporaryFile("w+t")
    result.write(s)
    result.seek(0)
    return result


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(_make_text_temp_file),
        int: st.integers(),
        str: st.text(),
    }
)
class Test_TextIO(generic_testing.TextIOBaseTests):
    pass


@generic_testing.Given(
    {
        generic_testing.ClassUnderTest: st.builds(io.StringIO),
        int: st.integers(),
        str: st.text(),
    }
)
class Test_StringIO(generic_testing.StringIOTests):
    pass


__all__ = (
    "Test_FileIO",
    "Test_BufferedIO",
    "Test_BytesIO",
    "Test_TextIO",
    "Test_StringIO",
)


if __name__ == "__main__":
    SUITE = unittest.TestSuite()
    if True:
        name = None
        value = None
        for name, value in locals().items():
            if name.startswith("Test_"):
                SUITE.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(value))
    else:
        SUITE.addTest(
            unittest.defaultTestLoader.loadTestsFromTestCase(Test_BufferedReader2)
        )
    unittest.TextTestRunner(verbosity=2).run(SUITE)
