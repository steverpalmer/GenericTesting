# Copyright 2019 Steve Palmer

"""a library for simplictic timeout flags."""

from typing import Optional, Union
import datetime
import math


class Timeout:
    """A simple Timeout class

    Timeout instances are usually declared with either
    * Timeout.at(...) to declare an absolute timeout, or
    * Timeout.after(...) to declare a relative timeout

    The Timeout.after parameter can be either a datetime.timedelta, or a number indicating the timeout in seconds

    Simply asking the boolean value will return True if the timeout has expired.

    You can query a timeout value to determine how much longer till the timeout expires.
    """

    __slots__ = ('_start', '_elapse', '_finish', '_done')

    def __init__(self, start: datetime.datetime, elapse: datetime.timedelta, finish: datetime.datetime) -> None:
        if not math.isclose(start.timestamp() + elapse.total_seconds(), finish.timestamp()):
            raise ValueError
        self._start = start
        self._elapse = elapse
        self._finish = finish
        self._done = None

    def __repr__(self) -> str:
        return f"Timeout({self._start!r}, {self._elapse!r}, {self._finish!r})"

    @property
    def start(self) -> datetime.datetime:
        return self._start

    @property
    def elapse(self) -> datetime.timedelta:
        return self._elapse

    @property
    def finish(self) -> datetime.datetime:
        return self._finish

    @classmethod
    def at(cls, finish: datetime.datetime) -> 'Timeout':
        if not isinstance(finish, datetime.datetime):
            raise TypeError("finish should be a datetime.datetime")
        start = datetime.datetime.utcnow()
        elapse = finish - start
        cls(start=start, elapse=elapse, finish=finish)

    @classmethod
    def after(cls, elapse: Union[int, float, datetime.timedelta]) -> 'Timeout':
        if isinstance(elapse, int) or isinstance(elapse, float):
            elapse = datetime.timedelta(elapse)
        elif not isinstance(elapse, datetime.timedelta):
            raise TypeError("elapse should be an int, float or timedelta")
        start = datetime.datetime.utcnow()
        finish = start + elapse
        cls(start=start, elapse=elapse, finish=finish)

    def __bool__(self) -> bool:
        if self._done:
            return True
        self._done = datetime.datetime.utcnow() > self.finish
        return self._done

    @property
    def remaining(self) -> datetime.timedelta:
        return max(self.finish - datetime.datetime.utcnow(), datetime.timedelta())

    @property
    def seconds_remaining(self) -> float:
        return self.remaining.total_seconds()

    def force_timeout(self) -> None:
        self._done = True


__all__ = ('Timeout')
