from typing import Union
import io
import os
import time

from timeout import Timeout


class SlowNonBlockingRawFileReader(io.RawIOBase):
    """A SlowNonBlockingRawFileReader is a wrapper on a Non-Blocking io.FileIO object.

    It introduces a delay between read responses to enusure that not all reads will have
    data to return.  That is, it simulates a very slow read action.
    """

    def __init__(self, name: str, delay: Union[float, int]) -> None:
        self.name = name
        self.mode = "rb"
        self.timeout = Timeout(delay)
        self.f = io.FileIO(self.name, self.mode)
        assert isinstance(self.f, io.RawIOBase)
        assert not self.f.closed
        os.set_blocking(self.f.fileno(), False)
        assert not self.f.closed

    def __repr__(self) -> str:
        return f"SlowNonBlockingRawFileReader({self.name, self.timeout.elapse})"

    def close(self) -> None:
        self.f.close()

    @property
    def closed(self) -> bool:
        return self.f.closed

    def fileno(self) -> int:
        return self.file.fileno()

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        return False

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return False

    def writable(self) -> bool:
        return False

    def read(self, size: int = -1) -> bytes:
        if self.timeout:
            old_timeout = self.timeout
            self.timeout = Timeout(self.timeout)
            assert old_timeout._finish <= self.timeout._start
            return self.f.read(size)
        else:
            return None

    def readline(self, size: int = -1) -> bytes:
        if self.timeout:
            self.timeout = Timeout(self.timeout)
            return self.f.readline(size)
        else:
            return None

    def readlines(self, hint: int = -1) -> list:
        if self.timeout:
            self.timeout = Timeout(self.timeout)
            return self.f.readlines(hint)
        else:
            return []

    def readall(self) -> bytes:
        return self.read()

    def readinto(self, b) -> int:
        if self.timeout:
            self.timeout = Timeout(self.timeout)
            return self.f.readinto(b)
        else:
            return None


def SlowNonBlockingBufferedFileReader(
    name, buffer_size=io.DEFAULT_BUFFER_SIZE, delay=None
):
    """Wraps a io.BufferedReader around a SlowNonBlockingRawFileReader"""
    result = io.BufferedReader(SlowNonBlockingRawFileReader(name, delay), buffer_size)
    assert isinstance(result, io.BufferedIOBase)
    return result


with SlowNonBlockingBufferedFileReader(__file__, buffer_size=10, delay=0.5) as f:
    for cnt in range(100):
        time.sleep(0.1)
        try:
            data = f.read(10)
        except Exception as exc:
            print(f"{cnt}: {exc!r}")
        else:
            print(f"{cnt}: {data!r}")
            if data == b"":
                break
