# Copyright 2019 Steve Palmer

"""a library of generic tests for the file-like properties."""

from generic_testing.core import ClassUnderTest
from generic_testing.collections_abc import IterableTests


class IOBaseTests(IterableTests):
    """Tests of IOBase inheritable properties."""

    def test_generic_3000_fileno_is_int(self, a: ClassUnderTest) -> None:
        """a.fileno()"""
        try:
            self.assertIsInstance(a.fileno(), int)
        except OSError:
            pass


class RawIOBaseTests(IOBaseTests):
    pass


class BufferedIOBaseTests(IOBaseTests):
    pass


class TextIOBaseTests(IOBaseTests):
    pass


__all__ = ('IOBaseTests', 'RawIOBaseTests', 'BufferedIOBaseTests', 'TextIOBaseTests')
