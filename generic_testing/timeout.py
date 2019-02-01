# Copyright 2019 Steve Palmer

"""a library for simplictic timeout flags."""

from typing import Union
import time
import datetime


class Timeout:
    """A simple Timeout class

    Simply asking the boolean value of a Timeout instance will return True if the timeout has expired.

    You can query a timeout value to determine how much longer till the timeout expires.
    """

    # __slots__ = ('_delay', '_start', '_finish', '_out')

    def __init__(self, delay: Union[int, float, datetime.timedelta], start: float = None) -> None:
        if isinstance(delay, datetime.timedelta):
            delay = delay.total_seconds()
        self._delay = max(0, delay)
        self.restart(start)

    def __repr__(self) -> str:
        """
        >>> Timeout(6)
        Timeout(6)
        """
        return f"Timeout({self._delay!r})"

    def __str__(self) -> str:
        return f"Timeout(in {self.remaining} seconds)"

    @property
    def delay(self) -> Union[float, int]:
        """
        >>> Timeout(6).delay
        6
        """
        return self._delay

    @delay.setter
    def delay(self, delay: Union[int, float]):
        """
        >>> t = Timeout(6)
        >>> t.delay = 5
        >>> t.delay
        5
        """
        self._delay = max(0, delay)
        self.restart(self._start)

    def __bool__(self) -> bool:
        """
        >>> t = Timeout(6)
        >>> bool(t)
        False
        >>> time.sleep(6)
        >>> bool(t)
        True
        """
        self._out = self._out or (time.monotonic() >= self._finish)
        return self._out

    def recycle(self) -> None:
        """Restart timeout from the last time it timed out
        >>> t = Timeout(6)
        >>> bool(t)
        False
        >>> time.sleep(6)
        >>> bool(t)
        True
        >>> time.sleep(3)
        >>> bool(t)
        True
        >>> t.recycle()
        >>> bool(t)
        False
        >>> time.sleep(4)
        >>> bool(t)
        True
        """
        self.restart(self._finish)

    def restart(self, start=None) -> None:
        """Restart timeout from, by default, now
        >>> t = Timeout(6)
        >>> bool(t)
        False
        >>> time.sleep(6)
        >>> bool(t)
        True
        >>> time.sleep(3)
        >>> bool(t)
        True
        >>> t.restart()
        >>> bool(t)
        False
        >>> time.sleep(4)
        >>> bool(t)
        False
        """
        if start is None:
            start = time.monotonic()
        self._start = start
        self._finish = self._start + self._delay
        self._out = False

    @property
    def remaining(self) -> Union[float, int]:
        return max(0, self._finish - time.monotonic())

    @property
    def elapse(self) -> Union[float, int]:
        return min(time.monotonic() - time.monotonic(), self._elapse)

    def wait(self) -> None:
        while self:
            time.sleep(self.remaining)

    @classmethod
    def at(cls, when: datetime.datetime) -> 'Timeout':
        return cls(when - datetime.now(datetime.timezone.utc))

    @classmethod
    def clone(cls, timeout: 'Timeout') -> 'Timeout':
        return cls(timeout._delay, timeout._repeat, timeout._start)


__all__ = ('Timeout')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
