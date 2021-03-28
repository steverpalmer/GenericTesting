#!/usr/bin/env python3
# Copyright 2021 Steve Palmer

"""A library for simple timeout flags."""

import asyncio
import datetime
import math
import numbers
import signal
import time
import typing
import warnings

try:
    import version as _version

    if not _version.version.is_backwards_compatible_with("1.0.0"):
        raise ImportError
except ImportError:
    _version = type("_version", (object,), {"Version": lambda self, s: s})()


__all__ = ("version", "Timeout")
version = _version.Version("2.0.0")


ClockDeltaT = numbers.Real


class Timeout:
    """A simple Timeout class

    Simply asking the boolean value of a Timeout instance will return True if the timeout has expired.

    You can query a timeout value to determine how much longer till the timeout expires.
    """

    __slots__ = ("_delay", "_start", "_clock")
    # _delay: ClockDeltaT = non-negative time in _clock delta units from _start before the timeout is reached.
    # _start: float = time the timeout starts, using the _clock.
    # _clock: Callable[[], float] the clock to use returning a Real number.

    @staticmethod
    def _delay_param(
        delay: typing.Union[ClockDeltaT, datetime.timedelta, type(None)]
    ) -> ClockDeltaT:
        """
        Convert a delay argument into the internal type, clipping below at 0.

        Specifically, will convert datetime.timedelta objects to seconds on the fly.
        WARNING: you should using a seconds clock in you are going to use datetime.timedelta objects.
        """
        if delay is None:
            delay = float("inf")
        elif isinstance(delay, datetime.timedelta):
            delay = delay.total_seconds()
        result = max(0, delay)
        return result

    def __init__(
        self,
        delay: typing.Union[ClockDeltaT, datetime.timedelta] = None,
        start: float = None,
        *,
        clock: typing.Callable[[], float] = None,
    ) -> None:
        """
        >>> Timeout(2.5)
        Timeout(2.5)
        >>> Timeout(datetime.timedelta(minutes=3))
        Timeout(180.0)
        >>> Timeout()
        Timeout()
        >>> Timeout(float("inf"))
        Timeout()
        """
        self._clock = clock or time.monotonic
        self._delay = Timeout._delay_param(delay)
        self.restart(start)

    def __repr__(self) -> str:
        """
        >>> Timeout(6)
        Timeout(6)
        """
        return "Timeout()" if math.isinf(self._delay) else f"Timeout({self._delay!r})"

    def __str__(self) -> str:
        return f"Timeout(in {self.remaining} seconds)"

    @property
    def _finish(self) -> float:
        return self._start + self._delay

    @property
    def delay(self) -> ClockDeltaT:
        """
        >>> Timeout(6).delay
        6
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
    def _remaining(self) -> ClockDeltaT:
        return self._finish - self._clock()

    @property
    def remaining(self) -> ClockDeltaT:
        return max(0, self._remaining)

    @property
    def elapse(self) -> ClockDeltaT:
        """Elapse time since start.
        >>> t = Timeout(0)
        >>> time.sleep(1)
        >>> t.elapse >= 1
        True
        """
        return self._clock() - self._start

    @classmethod
    def at(cls, when: datetime.datetime, *, clock=None) -> "Timeout":
        """
        >>> t = Timeout.at(datetime.datetime(2150, 1, 1))
        >>> t = Timeout.at(datetime.datetime.today())
        >>> t = Timeout.at(datetime.datetime.now())
        >>> t = Timeout.at(datetime.datetime.utcnow())
        >>> t = Timeout.at(datetime.datetime.now(datetime.timezone.utc))
        """
        return cls(when - datetime.datetime.now(when.tzinfo), clock=clock)

    def wait(self) -> bool:
        """Sleep until timeout.
        >>> t = Timeout(1)
        >>> t.wait()
        False
        >>> bool(t)
        True
        """
        remaining = self._remaining
        if remaining < 0:
            warnings.warn("Timeout Overrun", RuntimeWarning)
        elif math.isinf(remaining):
            signal.pause()
        else:
            time.sleep(remaining)
        return remaining < 0

    def iterator(
        self,
        *,
        do_restart: bool = False,
        do_quick_start: bool = False,
    ) -> typing.Iterator[bool]:
        """
        >>> [o for _, o in zip(range(3), Timeout(1).iterator())]
        [False, False, False]
        """
        if do_restart:
            self.restart()
        if do_quick_start:
            yield bool(self)
        while True:
            late = self.wait()
            self.recycle()
            yield late

    def __iter__(self) -> typing.Iterator[bool]:
        return self.iterator(do_restart=True, do_quick_start=True)

    async def async_wait(self) -> bool:
        remaining = self._remaining
        if remaining < 0:
            warnings.warn("Timeout Overrun", RuntimeWarning)
        elif math.isinf(remaining):
            await asyncio.Event().wait()
        else:
            await asyncio.sleep(self.remaining)
        return remaining < 0

    async def _aiterator(self, do_quick_start: bool) -> typing.AsyncIterator[bool]:
        if do_quick_start:
            yield bool(self)
        while True:
            late = await self.async_wait()
            self.recycle()
            yield late

    def aiterator(
        self, *, do_restart: bool = False, do_quick_start: bool = False
    ) -> typing.AsyncIterator[bool]:
        if do_restart:
            self.restart()
        return self._aiterator(do_quick_start)

    def __aiter__(self) -> typing.AsyncIterator[bool]:
        return self.aiterator(do_restart=True, do_quick_start=True)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
