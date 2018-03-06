#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A simplistic ModuloN class to help test the generic_test library.
"""

import numbers
import operator
import math


def _operator_fallbacks(fallback_operator, doc=""):
    if fallback_operator is None:
        return (None, None)

    def forward(a, b):
        if isinstance(b, type(a)):
            if a._modulus != b._modulus:
                raise ValueError("inconsistent modulus values")
            return type(a)(a._modulus, fallback_operator(a._value, b._value), is_trusted=True)
        elif isinstance(b, int):
            return fallback_operator(int(a), b)
        elif isinstance(b, float):
            return fallback_operator(float(a), b)
        elif isinstance(b, complex):
            return fallback_operator(complex(a), b)
        else:
            return NotImplemented
    forward.__name__ = '__' + fallback_operator.__name__ + '__'
    forward.__doc__ = doc

    def reverse(b, a):
        if isinstance(a, ModuloN):
            if a._modulus != b._modulus:
                raise ValueError("inconsistent modulus values")
            return type(a)(a._modulus, fallback_operator(a._value, b._value), is_trusted=True)
        elif isinstance(a, numbers.Integral):
            return fallback_operator(int(a), int(b))
        elif isinstance(a, numbers.Real):
            return fallback_operator(float(a), float(b))
        elif isinstance(a, numbers.Complex):
            return fallback_operator(complex(a), complex(b))
        else:
            return NotImplemented
    reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
    reverse.__doc__ = doc

    return forward, reverse


class ModuloN(numbers.Integral):

    __slots__ = ('_modulus', '__value')

    def __init__(self, modulus: int, value: int=None, *, is_trusted=False) -> None:
        """
        >>> _ = ModuloN(8, 3)
        >>> ModuloN(-2)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive
        >>> ModuloN(8, 10)
        ModuloN(8, 2)
        """
        if not is_trusted:
            if modulus <= 0:
                raise ValueError("Modulus must be positive")
        self._modulus = modulus
        self._value = value

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, value: int):
        if value is None:
            value = 0
        self.__value = value % self._modulus

    @classmethod
    def bit(cls, value=None):
        return cls(2, value, is_trusted=True)

    @classmethod
    def digit(cls, value=None):
        return cls(10, value, is_trusted=True)

    @classmethod
    def nibble(cls, value=None):
        return cls(16, value, is_trusted=True)

    @classmethod
    def byte(cls, value=None):
        return cls(256, value, is_trusted=True)

    @classmethod
    def short(cls, value=None):
        return cls(65536, value, is_trusted=True)

    @classmethod
    def word(cls, value=None):
        return cls(4294967296, value, is_trusted=True)

    @property
    def modulus(self) -> int:
        return self._modulus

    def __repr__(self) -> str:
        specials = {2: "{self.__class__.__name__}.bit({self._value})",
                    10: "{self.__class__.__name__}.digit({self._value})",
                    16: "{self.__class__.__name__}.nibble({self._value})",
                    256: "{self.__class__.__name__}.byte({self._value})",
                    65536: "{self.__class__.__name__}.short({self._value})",
                    4294967296: "{self.__class__.__name__}.word({self._value})"}
        return specials.get(self._modulus, "{self.__class__.__name__}({self._modulus}, {self._value})").format(self=self)

    def __str__(self) -> str:
        return "{self._value}(%{self._modulus})".format(self=self)

    def __bytes__(self) -> bytes:
        return bytes(self._value)

    def __format(self, format_spec) -> str:
        return format(self._value, format_spec)

    def __eq__(self, other) -> bool:
        if isinstance(other, ModuloN):
            result = self._modulus == other._modulus and self._value == other._value
        else:
            result = int(self) == other
        return result

    def __le__(self, other) -> bool:
        if isinstance(other, ModuloN):
            result = self._modulus == other._modulus and self._value <= other._value
        else:
            result = int(self) <= other
        return result

    def __ge__(self, other) -> bool:
        return other.__le__(self)

    def __lt__(self, other) -> bool:
        if isinstance(other, ModuloN):
            result = self._modulus == other._modulus and self._value < other._value
        else:
            result = int(self) <= other
        return result

    def __gt__(self, other) -> bool:
        return other.__lt__(self)

    def __hash__(self) -> int:
        # Since __eq__ above allows ModuloN values to be equal to the open integers,
        # we can only rely on the _value field for the hash.
        return hash(self._value)

    def __bool__(self) -> bool:
        return self._value != 0

    __add__, __radd__ = _operator_fallbacks(operator.add)

    __sub__, __rsub__ = _operator_fallbacks(operator.sub)

    __mul__, __rmul__ = _operator_fallbacks(operator.mul)

    def __truediv__(self, other) -> float:
        if isinstance(other, ModuloN):
            result = self._value / other._value
        else:
            result = self._value / other
        return result

    def __rtruediv__(self, other) -> 'ModuloN':
        return other / self._value

    # FIXME: The following two could be better if modulus is prime!
    __floordiv__, __rfloordiv__ = _operator_fallbacks(operator.floordiv)

    __mod__, __rmod__ = _operator_fallbacks(operator.mod)

    __pow__, __rpow__ = (None, None)

    # FIXME: This needs some thinging about
#     def __pow__(self, other: Union['ModuloN', int]) -> Union['ModuloN', float]:
#         other_value = self._other_value(other)
#         if other_value > 0:
#             result = ModuloN(self._modulus, pow(self._value, self._other_value(other), self._modulus))
#         else:
#             result = pow(self._value, self._other_value(other))
#         return result
# 
#     def __rpow__(self, other: 'ModuloN', modulo: int=None) -> 'ModuloN':
#         return self.__pow__(other, modulo)

    __lshift__, __rlshift__ = _operator_fallbacks(None) # operator.lshift)

    __rshift__, __rrshift__ = _operator_fallbacks(None) # operator.rshift)

    __and__, __rand__ = _operator_fallbacks(None) # operator.and_)

    __xor__, __rxor__ = _operator_fallbacks(None) # operator.xor)

    __or__, __ror__ = _operator_fallbacks(None) # operator.or_)

    def __neg__(self) -> 'ModuloN':
        return type(self)(self._modulus, -self._value, is_trusted=True)

    def __pos__(self) -> 'ModuloN':
        return type(self)(self._modulus, self._value, is_trusted=True)

    __abs__ = None

    def __invert__(self) -> 'ModuloN':
        return type(self)(self._modulus, ~self._value, is_trusted=True)

    def __int__(self) -> int:
        return self._value

    def __index__(self) -> int:
        return self._value

    def __round__(self, n: int) -> 'ModuloN':
        return self

    def __floor__(self) -> 'ModuloN':
        return self

    def __ceil__(self) -> 'ModuloN':
        return self

    def __trunc__(self) -> 'ModuloN':
        return self


class ModuloPow2(ModuloN):

    def __init__(self, modulus: int, value: int=None, *, is_trusted: bool=False) -> None:
        """
        >>> _ = ModuloPow2(8, 3)
        >>> ModuloPow2(-2)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive
        >>> ModuloPow2(3)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive power of two
        >>> ModuloPow2(0.5)
        Traceback (most recent call last):
            ...
        ValueError: Modulus must be positive power of two
        >>> ModuloPow2(8, 10)
        ModuloPow2(8, 2)
        """
        if not is_trusted:
            if modulus <= 0:
                raise ValueError("Modulus must be positive")
            bits = math.log2(modulus)
            if not bits.is_integer() or bits < 0.0:
                raise ValueError("Modulus must be positive power of two")
        self._modulus = modulus
        self._value = value

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, value: int):
        if value is None:
            value = 0
        self.__value = value & (self._modulus - 1)

    __lshift__, __rlshift__ = _operator_fallbacks(operator.lshift)

    __rshift__, __rrshift__ = _operator_fallbacks(operator.rshift)

    __and__, __rand__ = _operator_fallbacks(operator.and_)

    __xor__, __rxor__ = _operator_fallbacks(operator.xor)

    __or__, __ror__ = _operator_fallbacks(operator.or_)



__all__ = ('ModuloN', 'ModuloPow2')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
