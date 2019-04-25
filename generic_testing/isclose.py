#!/usr/bin/env python3
# Copyright 2019 Steve Palmer

"""Extension to math.isclose and cmath.isclose."""

import numbers
import math
import cmath
from collections import namedtuple

__version__ = '0.1'


class IsClose(namedtuple('IsClose', ('rel_tol', 'abs_tol'))):
    """Make the IsClose of math and cmath a little more convenient."""

    @staticmethod
    def _rel_tol_helper(rel_tol) -> float:
        """Exposes the default value of rel_tol to the library IsClose function.

        >>> IsClose._rel_tol_helper("fred")
        Traceback (most recent call last):
            ...
        TypeError: rel_tol must be a real number
        >>> IsClose._rel_tol_helper(-1.0)
        Traceback (most recent call last):
            ...
        ValueError: rel_tol must be non-negative
        >>> IsClose._rel_tol_helper(0.001)
        0.001
        >>> IsClose._rel_tol_helper(None)
        1e-09
        """
        if rel_tol is None:
            result = 1e-09  # §9.2.1  math.IsClose rel_tol default value (and cmath.IsClose)
        elif not isinstance(rel_tol, numbers.Real):
            raise TypeError("rel_tol must be a real number")
        else:
            result = float(rel_tol)
            if result < 0.0:
                raise ValueError("rel_tol must be non-negative")
        return result

    @staticmethod
    def _abs_tol_helper(abs_tol) -> float:
        """Exposes the default value of abs_tol to the library IsClose function.

        >>> IsClose._abs_tol_helper("fred")
        Traceback (most recent call last):
            ...
        TypeError: abs_tol must be a real number
        >>> IsClose._abs_tol_helper(-1.0)
        Traceback (most recent call last):
            ...
        ValueError: abs_tol must be non-negative
        >>> IsClose._abs_tol_helper(1e-30)
        1e-30
        >>> IsClose._abs_tol_helper(None)
        0.0
        """
        if abs_tol is None:
            result = 0.0  # §9.2.1  math.IsClose abs_tol default value (and cmath.IsClose)
        elif not isinstance(abs_tol, numbers.Real):
            raise TypeError("abs_tol must be a real number")
        else:
            result = float(abs_tol)
            if result < 0.0:
                raise ValueError("abs_tol must be non-negative")
        return result

    @staticmethod
    def _polymorphic(a: numbers.Number, b: numbers.Number, rel_tol: float, abs_tol: float) -> bool:
        """Polymorphic isclose.

        >>> IsClose._polymorphic(complex(1), float(1), 0.0, 0.0)
        True
        >>> IsClose._polymorphic(float(1), complex(2), 0.0, 0.0)
        False
        >>> IsClose._polymorphic(float(2), float(1), 0.0, 0.0)
        False
        >>> IsClose._polymorphic(1, float(1), 0.0, 0.0)
        True
        >>> IsClose._polymorphic(datetime.timedelta(1), datetime.timedelta(1), 0.0, 0.0)
        True
        >>> IsClose._polymorphic(datetime.timedelta(1, microseconds=1), datetime.timedelta(1), 0.0, 0.0)
        False
        >>> IsClose._polymorphic(datetime.timedelta(1, microseconds=1), datetime.timedelta(1), 1e-9, 0.0)
        True
        """
        if not isinstance(a, numbers.Number) or not isinstance(b, numbers.Number):
            # try and do something reasonable
            result = False
            if a == b:
                result = True
            else:
                try:
                    difference = abs(a - b)
                except BaseException:
                    pass
                else:
                    try:
                        if difference < rel_tol * max(abs(a), abs(b)):
                            result = True
                    except BaseException:
                        pass
                    if not result:
                        if type(a) == type(b):
                            try:
                                abs_tol = type(a)(abs_tol)
                            except BaseException:
                                pass
                        try:
                            if difference <= abs_tol:
                                result = True
                        except BaseException:
                            pass
        elif isinstance(a, numbers.Complex) or isinstance(b, numbers.Complex):
            result = cmath.isclose(complex(a), complex(b), rel_tol=rel_tol, abs_tol=abs_tol)
        else:
            result = math.isclose(float(a), float(b), rel_tol=rel_tol, abs_tol=abs_tol)
        return result

    @staticmethod
    def polymorphic(a: numbers.Number, b: numbers.Number, *, rel_tol: float = None, abs_tol: float = None) -> bool:
        """Polymorphic isclose.

        >>> IsClose.polymorphic(complex(1/3, 1/3), complex(0.3333333333333333333333, 0.33333333333333333333))
        True
        >>> IsClose.polymorphic(float(2), float(1))
        False
        """
        rel_tol = IsClose._rel_tol_helper(rel_tol)
        abs_tol = IsClose._abs_tol_helper(abs_tol)
        return IsClose._polymorphic(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

    def __new__(cls, rel_tol: numbers.Real = None, abs_tol: numbers.Real = None) -> 'IsClose':
        return super().__new__(cls, IsClose._rel_tol_helper(rel_tol), IsClose._abs_tol_helper(abs_tol))

    def __call__(self, a: numbers.Number, b: numbers.Number) -> bool:
        """Apply IsClose().

        >>> myisclose = IsClose()
        >>> myisclose(1.0, 1.0)
        True
        """
        return IsClose._polymorphic(a, b, rel_tol=self.rel_tol, abs_tol=self.abs_tol)

    def close(self):
        """close function.

        >>> myisclose = IsClose()
        >>> callable(myisclose.close)
        True
        """
        return self

    def notclose(self):
        """not close function.

        >>> myisclose = IsClose()
        >>> callable(myisclose.notclose)
        True
        """
        return lambda a, b: not self(a, b)

    # the following only make sense to floats

    def much_less_than(self):
        """definitely less function."""
        def result(a: float, b: float) -> bool:
            return a < b and not self(a, b)
        return result

    def less_than_or_close(self):
        """less or close function."""
        def result(a: float, b: float) -> bool:
            return a < b or self(a, b)

    def much_greater_than(self):
        """definitely greater function."""
        def result(a: float, b: float) -> bool:
            return a > b and not self(a, b)
        return result

    def greater_than_or_close(self):
        """greater or close function."""
        def result(a: float, b: float) -> bool:
            return a > b or self(a, b)
        return result


__all__ = ('IsClose')

if __name__ == '__main__':
    import datetime  # noqa F401
    import doctest
    doctest.testmod()
