# Copyright 2019 Steve Palmer

"""a library of generic tests for the file-like properties."""

import hypothesis

from generic_testing.core import ClassUnderTest
from generic_testing.collections_abc import IterableTests


class IOBaseTests(IterableTests):
    """Tests of IOBase inheritable properties."""

    def test_generic_3000_close_and_closed(self, a: ClassUnderTest) -> None:
        """a.close(); a.closed"""
        hypothesis.assume(not a.closed)
        a.close()
        self.assertTrue(a.closed)
        a.close()
        self.assertTrue(a.closed)

    def test_generic_3010_fileno_is_int(self, a: ClassUnderTest) -> None:
        """a.fileno()"""
        hypothesis.assume(not a.closed)
        try:
            self.assertIsInstance(a.fileno(), int)
        except OSError:
            pass

    def test_generic_3020_has_query_methods(self, a: ClassUnderTest) -> None:
        """a.fileno()"""
        self.assertTrue(callable(a.flush))
        self.assertTrue(callable(a.isatty))
        self.assertTrue(callable(a.readable))
        self.assertTrue(callable(a.writable))
        self.assertTrue(callable(a.seekable))


class RawIOBaseTests(IOBaseTests):
    pass


class BufferedIOBaseTests(IOBaseTests):
    pass


class TextIOBaseTests(IOBaseTests):
    pass


__all__ = ('IOBaseTests', 'RawIOBaseTests', 'BufferedIOBaseTests', 'TextIOBaseTests')
