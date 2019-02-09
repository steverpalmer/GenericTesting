# Copyright 2019 Steve Palmer

"""a library of generic tests for the file-like properties."""

from collections import Counter
import abc
import enum
import time
import os
import unittest
import io

import hypothesis

from generic_testing.timeout import Timeout
from generic_testing.core import ClassUnderTest
from generic_testing.collections_abc import IterableTests


class IOBaseTests(IterableTests):
    """Tests of IOBase inheritable properties."""

    @property
    @abc.abstractmethod
    def dtype(self) -> type:
        """as numpy.dtype, returns either bytes or str as appropriate"""
        pass

    def _to_dtype(self, msg):
        if isinstance(msg, self.dtype):
            result = msg
        elif issubclass(self.dtype, str):
            result = msg.decode()
        else:
            result = msg.encode()
        assert isinstance(result, self.dtype)
        return result

    def _ensure_readable(self, a: ClassUnderTest) -> None:
        if not a.readable():
            self.skipTest("Test only applies to readable streams")

    def _ensure_seekable(self, a: ClassUnderTest) -> None:
        if not a.seekable():
            self.skipTest("Test only applies to seekable streams")

    def _ensure_writable(self, a: ClassUnderTest) -> None:
        if not a.writable():
            self.skipTest("Test only applies to writable streams")

    def _ensure_blocking(self, a: ClassUnderTest) -> None:
        try:
            if not os.get_blocking(a.fileno()):
                self.skipTest("Test only applies to blocking streams")
        except OSError:
            pass

    def _ensure_non_interative(self, a: ClassUnderTest) -> None:
        if a.isatty():
            self.skipTest("Test only applies to non interactive streams")

    def test_generic_2400_iter_returns_an_iterator(self, a: ClassUnderTest) -> None:
        """Test __iter__ method."""
        hypothesis.assume(not a.closed)
        # The document does not say that the iterator behaviour is only valid on readable streams,
        # but the expected  behaviour in this case is not obvious, so let's restrict the test
        self._ensure_readable(a)
        super().test_generic_2400_iter_returns_an_iterator(a)

    def test_generic_2401_iterator_protocol_observed(self, a: ClassUnderTest) -> None:
        """Test iterator protocol."""
        hypothesis.assume(not a.closed)
        # The document does not say that the iterator behaviour is only valid on readable streams,
        # but the expected behaviour in this case is not obvious, so let's restrict the test
        self._ensure_readable(a)
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

    def test_generic_2703_fileno(self, a: ClassUnderTest) -> None:
        """io.IOBase.fileno()"""
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
        if a.readable():
            raise unittest.SkipTest("Test only applies to non readable streams")
        with self.assertRaises(OSError):
            a.read()

    def test_generic_2708_seek_when_not_seekable(self, a: ClassUnderTest) -> None:
        """check that OSError is raised when appropriate"""
        hypothesis.assume(not a.closed)
        if a.seekable():
            raise unittest.SkipTest("Test only applies to non seekable streams")
        with self.assertRaises(OSError):
            a.seek(0)
        with self.assertRaises(OSError):
            a.tell()
        with self.assertRaises(OSError):
            a.truncate()

    def test_generic_2708_write_when_not_writable(self, a: ClassUnderTest) -> None:
        """check that OSError is raised when appropriate"""
        hypothesis.assume(not a.closed)
        if a.writable():
            raise unittest.SkipTest("Test only applies to non writable streams")
        with self.assertRaises(OSError):
            a.write(self.dtype())
        with self.assertRaises(OSError):
            a.truncate()


class RawIOBaseTests(IOBaseTests):
    """Tests of RawIOBase inheritable properties."""

    @property
    def dtype(self) -> type:
        return bytes

    @property
    def max_test_time_seconds(self) -> float:
        """Some of these tests use a timeout, not to enforce any performance
        on the methods, but just to stop any tests hanging.  In such cases,
        the testing will be incomplete.
        """
        return 1.0

    def pause(self, delay_seconds=0.1) -> None:
        """Delay test execution, particularly in the case of a Non-Blocking ClassUnderTest
        """
        time.sleep(delay_seconds)

    def test_generic_2710_readall(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.readall()"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
        timeout = Timeout(self.max_test_time_seconds)
        state = State.Looping
        while state == State.Looping:
            a_readall = a.readall()
            if a_readall is None:
                if timeout:
                    state = State.Timeout
                else:
                    self.delay()
            else:
                self.assertIsInstance(a_readall, bytes)
                if a_readall == b'':
                    state = State.EOF_Found
        if state == State.EOF_Found:
            self.assertEqual(a.readall(), b'')

    def test_generic_2711_readinto(self, a: ClassUnderTest, n: int) -> None:
        """io.RawIOBase.readinto(_)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_readinto = a.readinto(bytearray(0))
        self.assertEqual(a_readinto, 0)
        buf = bytearray(n)
        State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
        timeout = Timeout(self.max_test_time_seconds)
        state = State.Looping
        while state == State.Looping:
            a_readinto = a.readinto(buf)
            if a_readinto is None:
                if timeout:
                    state = State.Timeout
                else:
                    self.pause()
            else:
                self.assertTrue(0 <= a_readinto <= n)
                if a_readinto == 0:
                    state = State.EOF_Found
        if state == State.EOF_Found:
            self.assertEqual(a.readinto(buf), 0)

    def test_generic_2712_read_unlimited(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.read()"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
        timeout = Timeout(self.max_test_time_seconds)
        state = State.Looping
        while state == State.Looping:
            a_read = a.read()
            if a_read is None:
                if timeout:
                    state = State.Timeout
                else:
                    self.pause()
            else:
                self.assertIsInstance(a_read, bytes)
                if a_read == b'':
                    state = State.EOF_Found
        if state == State.EOF_Found:
            self.assertEqual(a.read(), b'')

    def test_generic_2713_read_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.RawIOBase.read(n)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_read = a.read(0)
        self.assertEqual(a_read, b'')
        State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
        timeout = Timeout(self.max_test_time_seconds)
        state = State.Looping
        while state == State.Looping:
            a_read = a.read(n)
            if a_read is None:
                if timeout:
                    state = State.Timeout
                else:
                    self.pause()
            else:
                self.assertIsInstance(a_read, bytes)
                self.assertTrue(0 <= len(a_read) <= n)
                if a_read == b'':
                    state = State.EOF_Found
        if state == State.EOF_Found:
            self.assertEqual(a.read(n), b'')

    def test_generic_2714_readline_unlimited(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.readline()"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
        timeout = Timeout(self.max_test_time_seconds)
        state = State.Looping
        while state == State.Looping:
            a_readline = a.readline()
            if a_readline is None:
                if timeout:
                    state = State.Timeout
                else:
                    self.pause()
            else:
                self.assertIsInstance(a_readline, bytes)
                sp = a_readline.split(b'\n')
                if len(sp) < 2:
                    state = State.EOF_Found
                else:
                    self.assertTrue(len(sp) == 2 and len(sp[1]) == 0, "multiline response to readline")
        if state == State.EOF_Found:
            self.assertEqual(a.readline(), b'')

    def test_generic_2715_readline_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.RawIOBase.readline(n)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_readline = a.readline(0)
        self.assertEqual(a_readline, b'')
        State = enum.Enum('State', ('Looping', 'EOF_Found', 'Timeout'))
        timeout = Timeout(self.max_test_time_seconds)
        state = State.Looping
        while state == State.Looping:
            a_readline = a.readline(n)
            if a_readline is None:
                if timeout:
                    state = State.Timeout
                else:
                    self.pause()
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

    # TODO: readlines

    def test_generic_2720_write(self, a: ClassUnderTest, b: bytes) -> None:
        """io.RawIOBase.write(b)"""
        hypothesis.assume(not a.closed)
        self._ensure_writable(a)
        a_write = a.write(b)
        if a_write is not None:
            self.assertIsInstance(a_write, int)
            self.assertTrue(0 <= a_write <= len(b))

    def test_generic_2721_writelines(self, a: ClassUnderTest, n: int, b: bytes) -> None:
        """io.RawIOBase.writelines"""
        hypothesis.assume(not a.closed)
        self._ensure_writable(a)
        n = (n & 0xFF) + 1
        a.writelines([b] * n)
        # test passes if this does not raise an exception

    def test_generic_2730_tell(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.tell()"""
        hypothesis.assume(not a.closed)
        self._ensure_seekable(a)
        a.tell()
        # test passes if this does not raise an exception

    def test_generic_2731_seek(self, a: ClassUnderTest) -> None:
        """io.RawIOBase.seek()"""
        hypothesis.assume(not a.closed)
        self._ensure_seekable(a)
        a.seek(0)
        a.seek(0, 2)
        a.seek(0, 0)
        a.seek(0, 1)
        # test passes if this does not raise an exception

    def test_generic_2735_truncate(self, a: ClassUnderTest, n: int) -> None:
        """io.RawIOBase.truncate()"""
        hypothesis.assume(not a.closed)
        self._ensure_seekable(a)
        self._ensure_writable(a)
        n = n & 0xFFFF  # limit size of n to something reasonable
        start = a.tell()
        a_truncate = a.truncate(n)
        finish = a.tell()
        self.assertIsInstance(a_truncate, int)
        self.assertEqual(a_truncate, n)
        self.assertEqual(start, finish)


class ReadWriteStorageBinarySteamTests:
    """Discrete test of steams with Read/Write Semantics """

    def test_generic_2790_read_seek_write(self, a: ClassUnderTest, b: bytes, n: int) -> None:
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_seekable(a)
        self._ensure_writable(a)
        a.seek(0)
        original = a.read()
        length = len(original)
        position = n % length if length > 0 else 0
        a.seek(position)
        written = a.write(b)
        self.assertEqual(written, len(b))
        expected = bytearray(original)
        expected[position:position + written] = b
        a.seek(0)
        self.assertEqual(a.read(), expected)


class FileIOTests(RawIOBaseTests, ReadWriteStorageBinarySteamTests):
    """Tests of FileIO properties."""

    def test_generic_2740_name(self, a: ClassUnderTest) -> None:
        """io.FileIO.name"""
        hypothesis.assume(not a.closed)
        self.assertIsInstance(a.mode, str)
        name = a.name
        if isinstance(name, int):
            self.assertEqual(name, a.fileno())
        else:
            self.assertTrue(isinstance(name, bytes) or isinstance(name, str))
            self.assertTrue(len(name) > 0)

    def test_generic_2741_mode(self, a: ClassUnderTest) -> None:
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
    """Tests of BufferedIOBase inheritable properties."""

    @property
    def dtype(self) -> type:
        return bytes

    @property
    def max_test_time_seconds(self) -> float:
        """Some of these tests use a timeout, not to enforce any performance
        on the methods, but just to stop any tests hanging.  In such cases,
        the testing will be incomplete.
        """
        return 1.0

    def pause(self, delay_seconds=0.1) -> None:
        """Delay test execution, particularly in the case of a Non-Blocking ClassUnderTest
        """
        time.sleep(delay_seconds)

    def test_generic_2711_readinto(self, a: ClassUnderTest, n: int) -> None:
        """io.BufferedIOBase.readinto(_)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        self._ensure_non_interative(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_readinto = a.readinto(bytearray(0))
        self.assertEqual(a_readinto, 0)
        buf = bytearray(n)
        while True:
            a_readinto = a.readinto(buf)
            self.assertTrue(0 <= a_readinto <= n)
            if a_readinto < n:
                break
        self.assertEqual(a.readinto(buf), 0)

    def test_generic_2712_read_unlimited(self, a: ClassUnderTest) -> None:
        """io.BufferedIOBase.read()"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        a_read = a.read()
        self.assertIsInstance(a_read, bytes)
        self.assertEqual(a.read(), b'')

    def test_generic_2713_read_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.BufferedIOBase.read(n)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        self._ensure_non_interative(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_read = a.read(0)
        self.assertEqual(a_read, b'')
        while True:
            a_read = a.read(n)
            self.assertIsInstance(a_read, bytes)
            self.assertLessEqual(len(a_read), n)
            if len(a_read) < n:
                break
        self.assertEqual(a.read(n), b'')

    def test_generic_2714_readline_unlimited(self, a: ClassUnderTest) -> None:
        """io.BufferedIOBase.readline()"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        while True:
            a_readline = a.readline()
            self.assertIsInstance(a_readline, bytes)
            sp = a_readline.split(b'\n')
            if len(sp) < 2:
                break
            else:
                self.assertTrue(len(sp) == 2 and len(sp[1]) == 0, "multiline response to readline")
        self.assertEqual(a.readline(), b'')

    def test_generic_2715_readline_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.BufferedIOBase.readline(n)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        self._ensure_non_interative(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_readline = a.readline(0)
        self.assertEqual(a_readline, b'')
        while True:
            a_readline = a.readline(n)
            self.assertIsInstance(a_readline, bytes)
            self.assertLessEqual(len(a_readline), n)
            if len(a_readline) < n:
                sp = a_readline.split(b'\n')
                if len(sp) < 2:
                    break
                else:
                    self.assertTrue(len(sp) == 2 and len(sp[1]) == 0, "multiline response to readline")
        self.assertEqual(a.readline(n), b'')

    # TODO: readlines

    def test_generic_2716_read1_unlimited(self, a: ClassUnderTest) -> None:
        """io.BufferedIOBase.read1()"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        self._ensure_non_interative(a)
        while True:
            a_read1 = a.read1()
            self.assertIsInstance(a_read1, bytes)
            if a_read1 == b'':
                break
        self.assertEqual(a.read1(), b'')

    def test_generic_2717_read1_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.BufferedIOBase.read1(n)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        self._ensure_non_interative(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_read = a.read(0)
        self.assertEqual(a_read, b'')
        while True:
            a_read1 = a.read1(n)
            self.assertIsInstance(a_read1, bytes)
            self.assertLessEqual(len(a_read1), n)
            if a_read1 == b'':
                break
        self.assertEqual(a.read1(n), b'')

    def test_generic_2718_readinto1(self, a: ClassUnderTest, n: int) -> None:
        """io.BufferedIOBase.readinto1(_)"""
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_blocking(a)
        self._ensure_non_interative(a)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_readinto1 = a.readinto1(bytearray(0))
        self.assertEqual(a_readinto1, 0)
        buf = bytearray(n)
        while True:
            a_readinto1 = a.readinto1(buf)
            self.assertTrue(0 <= a_readinto1 <= n)
            if a_readinto1 == 0:
                break
        self.assertEqual(a.readinto1(buf), 0)

    def test_generic_2750_raw(self, a: ClassUnderTest) -> None:
        """io.BufferedIOBase.raw"""
        hypothesis.assume(not a.closed)
        try:
            self.assertIsInstance(a.raw, io.RawIOBase)
        except AttributeError:
            pass

    def test_generic_2751_detach(self, a: ClassUnderTest) -> None:
        """io.BufferedIOBase.detach"""
        hypothesis.assume(not a.closed)
        try:
            self.assertIsInstance(a.detach(), io.RawIOBase)
        except io.UnsupportedOperation:
            pass


class BytesIOTests(BufferedIOBaseTests, ReadWriteStorageBinarySteamTests):

    def test_generic_2703_fileno(self, a: ClassUnderTest) -> None:
        """io.BytesIO.fileno()"""
        hypothesis.assume(not a.closed)
        with self.assertRaises(OSError):
            a.fileno()

    def test_generic_2704_has_query_methods(self, a: ClassUnderTest) -> None:
        """io.BytesIO query methods as expected."""
        hypothesis.assume(not a.closed)
        self.assertFalse(a.isatty())
        self.assertTrue(a.readable())
        self.assertTrue(a.writable())
        self.assertTrue(a.seekable())

    def test_generic_2760_getbuffer(self, a: ClassUnderTest) -> None:
        """io.BytesIO.getbuffer"""
        hypothesis.assume(not a.closed)
        # TODO: figure out a better set of tests...!
        a.getbuffer()

    def test_generic_2761_getvalue(self, a: ClassUnderTest) -> None:
        """io.BytesIO.getvalue"""
        hypothesis.assume(not a.closed)
        a_getvalue = a.getvalue()
        self.assertIsInstance(a_getvalue, bytes)

    def test_generic_2716_read1_unlimited(self, a: ClassUnderTest) -> None:
        """io.BytesIOBase.read1()"""
        hypothesis.assume(not a.closed)
        a_read1 = a.read1()
        self.assertIsInstance(a_read1, bytes)
        self.assertEqual(a.read1(), b'')

    def test_generic_2717_read1_limited(self, a: ClassUnderTest, n: int) -> None:
        """io.BytesIOBase.read1(n)"""
        hypothesis.assume(not a.closed)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_read1 = a.read1(0)
        self.assertEqual(a_read1, b'')
        while True:
            a_read1 = a.read1(n)
            self.assertIsInstance(a_read1, bytes)
            self.assertLessEqual(len(a_read1), n)
            if len(a_read1) < n:
                break
        self.assertEqual(a.read1(n), b'')

    def test_generic_2718_readinto1(self, a: ClassUnderTest, n: int) -> None:
        """io.BytesIO.readinto1(_)"""
        hypothesis.assume(not a.closed)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_readinto1 = a.readinto1(bytearray(0))
        self.assertEqual(a_readinto1, 0)
        buf = bytearray(n)
        while True:
            a_readinto1 = a.readinto1(buf)
            self.assertTrue(0 <= a_readinto1 <= n)
            if a_readinto1 < n:
                break
        self.assertEqual(a.readinto1(buf), 0)

    def test_generic_2730_tell(self, a: ClassUnderTest, n: int) -> None:
        """io.BytesIO.tell()"""
        hypothesis.assume(not a.closed)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a_tell = a.tell()
        self.assertEqual(a_tell, 0)
        a_read = a.read(n)
        a_tell = a.tell()
        self.assertEqual(a_tell, len(a_read))

    def test_generic_2731_seek(self, a: ClassUnderTest, n: int) -> None:
        """io.BytesIO.seek()"""
        hypothesis.assume(not a.closed)
        n = (n & 0xFFFF) + 1  # limit size of n to something reasonable
        a.seek(0, 2)
        a_size = a.tell()
        self.assertLessEqual(0, a_size)
        a.seek(1, 1)
        self.assertEqual(a.tell(), a_size + 1)
        a.seek(n)
        self.assertEqual(a.tell(), n)

    def test_generic_2735_truncate(self, a: ClassUnderTest, n: int) -> None:
        """io.BytesIO.truncate()"""
        # TODO:
        hypothesis.assume(not a.closed)
        self._ensure_seekable(a)
        self._ensure_writable(a)
        n = n & 0xFFFF  # limit size of n to something reasonable
        start = a.tell()
        a_truncate = a.truncate(n)
        finish = a.tell()
        self.assertIsInstance(a_truncate, int)
        self.assertEqual(a_truncate, n)
        self.assertEqual(start, finish)

    def test_generic_2751_detach(self, a: ClassUnderTest) -> None:
        """io.BytesIO.detach"""
        hypothesis.assume(not a.closed)
        with self.assertRaises(io.UnsupportedOperation):
            a.detach()


class TextIOBaseTests(IOBaseTests):
    """Tests of TextIOBase inheritable properties."""

    @property
    def dtype(self) -> type:
        return str


class ReadWriteStorageTextSteamTests:
    """Discrete test of steams with Read/Write Semantics """

    def test_generic_2790_read_seek_write(self, a: ClassUnderTest, s: str, n: int) -> None:
        hypothesis.assume(not a.closed)
        self._ensure_readable(a)
        self._ensure_seekable(a)
        self._ensure_writable(a)
        a.seek(0)
        original = a.read()
        length = len(original)
        position = n % length if length > 0 else 0
        a.seek(position)
        written = a.write(s)
        self.assertEqual(written, len(s))
        expected = original[:position] + s + original[min(position + written, length):]
        a.seek(0)
        self.assertEqual(a.read(), expected)


class StringIOTests(TextIOBaseTests, ReadWriteStorageTextSteamTests):
    pass


__all__ = ('IOBaseTests', 'RawIOBaseTests', 'FileIOTests', 'BufferedIOBaseTests', 'BytesIOTests', 'TextIOBaseTests', 'StringIOTests')
