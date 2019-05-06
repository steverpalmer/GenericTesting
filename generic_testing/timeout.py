#!/usr/bin/env python3
# Copyright 2019 Steve Palmer

"""A library for simple timeout flags."""

import numbers
import typing
import time
import datetime

__version__ = '0.1'


ClockDeltaT = numbers.Real


class Timeout:
    """A simple Timeout class

    Simply asking the boolean value of a Timeout instance will return True if the timeout has expired.

    You can query a timeout value to determine how much longer till the timeout expires.
    """

    __slots__ = ('_delay', '_start', '_clock')
    # _delay: ClockDeltaT = non-negative time in _clock delta units from _start before the timeout is reached.
    # _start: float = time the timeout starts, using the _clock.
    # _clock: Callable[[], float] the clock to use returning a Real number.

    @staticmethod
    def _delay_param(delay: typing.Union[ClockDeltaT, datetime.timedelta]) -> ClockDeltaT:
        """
        Convert a delay argument into the internal type.

        Specifically, will convert datetime.timedelta objects to seconds on the fly.
        WARNING: you shoulb using a seconds clock in you are going to use datetime.timedelta objects.
        """
        if isinstance(delay, datetime.timedelta):
            delay = delay.total_seconds()
        result = max(0, delay)
        return result

    def __init__(self,
                 delay: typing.Union[ClockDeltaT, datetime.timedelta],
                 start: float = None,
                 *,
                 clock: typing.Callable[[], float] = None) -> None:
        self._clock = clock or time.monotonic
        self._delay = Timeout._delay_param(delay)
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
    def _finish(self) -> float:
        return self._start + self._delay

    @property
    def delay(self) -> ClockDeltaT:
        """
        >>> Timeout(6).delay
        6.0
        """
        return self._delay

    @delay.setter
    def delay(self, delay: typing.Union[ClockDeltaT, datetime.timedelta]):
        """
        >>> t = Timeout(6)
        >>> t.delay = 5
        >>> t.delay
        5
        """
        self._delay = Timeout._delay_param(delay)

    def __bool__(self) -> bool:
        """
        >>> t = Timeout(6)
        >>> bool(t)
        False
        >>> time.sleep(6)
        >>> bool(t)
        True
        """
        return self._clock() >= self._finish

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
        self._start = self._finish

    def restart(self, start: float = None) -> None:
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
            start = self._clock()
        self._start = start

    @property
    def remaining(self) -> ClockDeltaT:
        return max(0, self._finish - self._clock())

    @property
    def elapse(self) -> ClockDeltaT:
        return self._clock() - self._start

    def wait(self) -> None:
        time.sleep(self.remaining)

    @classmethod
    def at(cls, when: datetime.datetime, *, clock=None) -> 'Timeout':
        return cls(when - datetime.now(datetime.timezone.utc), clock=clock)

    def copy(self) -> 'Timeout':
        result = Timeout(self._delay, self._start, clock=self._clock)
        return result


__all__ = ('Timeout')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
