# Copyright 2019 Steve Palmer

"""a library for simplictic timeout flags."""

from typing import Union
import time


class Timeout:
    """A simple Timeout class

    Simply asking the boolean value of a Timeout instance will return True if the timeout has expired.

    You can query a timeout value to determine how much longer till the timeout expires.
    """

    __slots__ = ('_start', '_elapse', '_finish', '_done')

    def __init__(self, elapse: Union[int, float]) -> None:
        self._start = time.monotonic()
        self._elapse = max(0, elapse)
        self._finish = self._start + self._elapse

    def __repr__(self) -> str:
        return f"Timeout({self._elapse!r})"

    def __str__(self) -> str:
        return f"Timeout(in {self.remaining} seconds)"

    @property
    def elapse(self) -> Union[float, int]:
        return self._elapse

    def __bool__(self) -> bool:
        return time.monotonic() >= self.finish

    @property
    def remaining(self) -> float:
        return max(0, self._finish - time.monotonic())

    @property
    def elapse_so_far(self) -> float:
        return min(time.monotonic() - time.monotonic(), self._elapse)


__all__ = ('Timeout')
