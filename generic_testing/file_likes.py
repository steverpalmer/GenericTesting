# Copyright 2019 Steve Palmer

"""a library of generic tests for the file-like properties."""

from collections import Counter
import enum
from time import sleep
import os

import hypothesis

from generic_testing.timeout import Timeout
from generic_testing.core import ClassUnderTest
from generic_testing.collections_abc import IterableTests


class IOBaseTests(IterableTests):
    """Tests of IOBase inheritable properties."""

    def test_generic_2400_iter_returns_an_iterator(self, a: ClassUnderTest) -> None:
        """Test __iter__ method."""
        hypothesis.assume(not a.closed)
        # The document does not say that the iterator behaviour is only valid on readable streams,
        # but the expected  behaviour in this case is not obvious, so let's restrict the test
        if a.readable():
            super().test_generic_2400_iter_returns_an_iterator(a)

    def test_generic_2401_iterator_protocol_observed(self, a: ClassUnderTest) -> None:
        """Test iterator protocol."""
        hypothesis.assume(not a.closed)
        # The document does not say that the iterator behaviour is only valid on readable streams,
        # but the expected behaviour in this case is not obvious, so let's restrict the test
        if a.readable():
            super().test_generic_2401_iterator_protocol_observed(a)

    def test_generic_2700_closed(self, a: ClassUnderTest) -> None:
        """a.closed"""
        a.closed
        #  If we don't raise an exception, then we've passed ...

    def test_generic_2701_close_and_closed(self, a: ClassUnderTest) -> None:
        """a.close(); a.closed"""
        hypothesis.assume(not a.closed)
        a.close()
        self.assertTrue(a.closed)
        a.close()
        self.assertTrue(a.closed)

    def test_generic_2702_close_and_read(self, a: ClassUnderTest) -> None:
        """a.close(); a.read()"""
        hypothesis.assume(not a.closed)
        if a.readable():
            a.close()
            with self.assertRaises(ValueError):
                a.read()

    def test_generic_2703_fileno_is_int(self, a: ClassUnderTest) -> None:
        """a.fileno()"""
        hypothesis.assume(not a.closed)
        try:
            a_fileno = a.fileno()
            self.assertIsInstance(a_fileno, int)
            self.assertIsNotNone(os.fstat(a.fileno()))  # hopefully testing that the value is a real file descriptor
        except OSError:
            pass

    def test_generic_2704_has_query_methods(self, a: ClassUnderTest) -> None:
        """check verious query methods don't raise exceptions."""
        hypothesis.assume(not a.closed)
        a.isatty()
        a.readable()
        a.writable()
        a.seekable()
        #  If we don't through an exception, then we've passed ...

    def test_generic_2705_has_read_methods(self, a: ClassUnderTest) -> None:
        """check verious read methods exist."""
        hypothesis.assume(not a.closed)
        self.assertTrue(callable(a.read))
        # Althought 3.7.2 says that readinto is part of the interface of io.IOBase,
        # It makes no sense appied to TestIOBase since (as it also states)
        # "Python's character strings are immutable.
        # Instead of requiring it here, I test it in the cases when it does make sense
        # See Python Issue 35848
        # self.assertTrue(callable(a.readinto))
        self.assertTrue(callable(a.readline))
        self.assertTrue(callable(a.readlines))

    def test_generic_2706_has_seek_methods(self, a: ClassUnderTest) -> None:
        """check verious seek methods exist."""
        hypothesis.assume(not a.closed)
        self.assertTrue(callable(a.seek))
        self.assertTrue(callable(a.tell))
        self.assertTrue(callable(a.truncate))

    def test_generic_2707_has_write_methods(self, a: ClassUnderTest) -> None:
        """check verious write methods exist."""
        hypothesis.assume(not a.closed)
        self.assertTrue(callable(a.write))
        self.assertTrue(callable(a.writelines))
        self.assertTrue(callable(a.flush))

    def test_generic_2708_read_when_not_readable(self, a: ClassUnderTest) -> None:
        """check that OSError is raised when appropriate"""
        hypothesis.assume(not a.closed)
        if not a.readable():
            with self.assertRaises(OSError):
                a.read()
        if not a.seekable():
            with self.assertRaises(OSError):
                a.seek(0)
            with self.assertRaises(OSError):
                a.tell()
            with self.assertRaises(OSError):
                a.truncate()
        if not a.writable():
            with self.assertRaises(OSError):
                a.truncate()


class RawIOBaseTests(IOBaseTests):
    """Tests of RawIOBase inheritable properties."""

    @staticmethod
    def _check_line(line):
        sp = line.split(b'\n')
        len_sp = len(sp)
        at_eof = len_sp < 2
        wellformed = at_eof or (len_sp == 2 and len(sp[1]) == 0)
        return (at_eof, wellformed)

    def test_generic_2710_raw_readall(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.readall()"""
        hypothesis.assume(not a.closed)
        if a.readable():
            State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
            timeout = Timeout(10)
            state = State.Looping
            while state == State.Looping:
                a_readall = a.readall()
                if a_readall is None:
                    if timeout:
                        state = State.Timeout
                    else:
                        sleep(0.1)
                else:
                    self.assertIsInstance(a_readall, bytes)
                    if a_readall == b'':
                        state = State.EOF_Found
            if state == State.EOF_Found:
                self.assertEqual(a.readall(), b'')

    def test_generic_2711_raw_readinto(self, a: ClassUnderTest, n: int) -> None:
        """io.RawIOBase.readinto(_)"""
        hypothesis.assume(not a.closed)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        if a.readable():
            a_readinto = a.readinto(bytearray(0))
            self.assertEqual(a_readinto, 0)
            buf = bytearray(n)
            State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
            timeout = Timeout(10)
            state = State.Looping
            while state == State.Looping:
                a_readinto = a.readinto(buf)
                if a_readinto is None:
                    if timeout:
                        state = State.Timeout
                    else:
                        sleep(0.1)
                else:
                    self.assertTrue(0 <= a_readinto <= n)
                    if a_readinto == 0:
                        state = State.EOF_Found
            if state == State.EOF_Found:
                self.assertEqual(a.readinto(buf), 0)

    def test_generic_2712_raw_read_unlimited(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.read()"""
        hypothesis.assume(not a.closed)
        if a.readable():
            State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
            timeout = Timeout(10)
            state = State.Looping
            while state == State.Looping:
                a_read = a.read()
                if a_read is None:
                    if timeout:
                        state = State.Timeout
                    else:
                        sleep(0.1)
                else:
                    self.assertIsInstance(a_read, bytes)
                    if a_read == b'':
                        state = State.EOF_Found
            if state == State.EOF_Found:
                self.assertEqual(a.read(), b'')

    def test_generic_2713_raw_read_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.RawIOBase.read(n)"""
        hypothesis.assume(not a.closed)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        if a.readable():
            a_read = a.read(0)
            self.assertEqual(a_read, b'')
            State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
            timeout = Timeout(10)
            state = State.Looping
            while state == State.Looping:
                a_read = a.read(n)
                if a_read is None:
                    if timeout:
                        state = State.Timeout
                    else:
                        sleep(0.1)
                else:
                    self.assertIsInstance(a_read, bytes)
                    self.assertTrue(0 <= len(a_read) <= n)
                    if a_read == b'':
                        state = State.EOF_Found
            if state == State.EOF_Found:
                self.assertEqual(a.read(n), b'')

    def test_generic_2714_raw_readline_unlimited(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.readline()"""
        hypothesis.assume(not a.closed)
        if a.readable():
            State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
            timeout = Timeout(10)
            state = State.Looping
            while state == State.Looping:
                a_readline = a.readline()
                if a_readline is None:
                    if timeout:
                        state = State.Timeout
                    else:
                        sleep(0.1)
                else:
                    self.assertIsInstance(a_readline, bytes)
                    sp = a_readline.split(b'\n')
                    if len(sp) < 2:
                        state = State.EOF_Found
                    else:
                        self.assertTrue(len(sp) == 2 and len(sp[1]) == 0, "multiline response to readline")
            if state == State.EOF_Found:
                self.assertEqual(a.readline(), b'')

    def test_generic_2715_raw_readline_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.RawIOBase.readline(n)"""
        hypothesis.assume(not a.closed)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        if a.readable():
            a_readline = a.readline(0)
            self.assertEqual(a_readline, b'')
            State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
            timeout = Timeout(10)
            state = State.Looping
            while state == State.Looping:
                a_readline = a.readline(n)
                if a_readline is None:
                    if timeout:
                        state = State.Timeout
                    else:
                        sleep(0.1)
                else:
                    self.assertIsInstance(a_readline, bytes)
                    self.assertLessEqual(len(a_readline), n)
                    if len(a_readline) < n:
                        sp = a_readline.split(b'\n')
                        if len(sp) < 2:
                            state = State.EOF_Found
                        else:
                            self.assertTrue(len(sp) == 2 and len(sp[1]) == 0, "multiline response to readline")
            if state == State.EOF_Found:
                self.assertEqual(a.readline(n), b'')


class FileIOTests(RawIOBaseTests):
    """Tests of FileIO properties."""

    def test_generic_2718_name(self, a: ClassUnderTest) -> None:
        """io.FileIO.name"""
        hypothesis.assume(not a.closed)
        self.assertIsInstance(a.mode, str)
        name = a.name
        if isinstance(name, int):
            self.assertEqual(name, a.fileno())
        else:
            self.assertTrue(isinstance(name, bytes) or isinstance(name, str))
            self.assertTrue(len(name) > 0)

    def test_generic_2719_mode(self, a: ClassUnderTest) -> None:
        """io.FileIO.mode"""
        hypothesis.assume(not a.closed)
        self.assertIsInstance(a.mode, str)
        mode = a.mode
        self.assertIsInstance(mode, str)
        self.assertTrue('b' in mode)
        c = Counter(mode)
        self.assertLessEqual(set(c.keys()), set('brwxa+'), f"Unexpected mode character: {mode}")
        self.assertSetEqual(set(c.values()), {1}, f"Duplicate mode character: {mode}")


class BufferedIOBaseTests(IOBaseTests):
    """Tests of RawIOBase inheritable properties."""

    def test_generic_2720_raw(self, a: ClassUnderTest) -> None:
        pass


class BytesIOTests(BufferedIOBaseTests):
    pass


class TextIOBaseTests(IOBaseTests):
    pass


class StringIOTests(TextIOBaseTests):
    pass


__all__ = ('IOBaseTests', 'RawIOBaseTests', 'FileIOTests', 'BufferedIOBaseTests', 'BytesIOTests', 'TextIOBaseTests', 'StringIOTests')
