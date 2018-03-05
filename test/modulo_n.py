#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

A simplistic ModuloN class to help test the generic_test library.
"""

import numbers
import operator


class ModuloN(numbers.Integral):

    __slots__ = ('_modulus', '_value')

    def __init__(self, modulus: int, value: int=None) -> None:
        if modulus <= 0:
            raise ValueError("Modulus must be positive")
        if value is None:
            value = 0
        self._modulus = modulus
        self._value = value % modulus

    @classmethod
    def bit(cls, value=None):
        return cls(2, value)

    @classmethod
    def digit(cls, value=None):
        return cls(10, value)

    @classmethod
    def nibble(cls, value=None):
        return cls(16, value)

    @classmethod
    def byte(cls, value=None):
        return cls(256, value)

    @classmethod
    def short(cls, value=None):
        return cls(65536, value)

    @classmethod
    def word(cls, value=None):
        return cls(4294967296, value)

    @property
    def modulus(self) -> int:
        return self._modulus

    def __repr__(self) -> str:
        specials = {2: "ModuloN.bit({self._value})",
                    10: "ModuloN.digit({self._value})",
                    16: "ModuloN.nibble({self._value})",
                    256: "ModuloN.byte({self._value})",
                    65536: "ModuloN.short({self._value})",
                    4294967296: "ModuloN.word({self._value})"}
        return specials.get(self._modulus, "ModuloN({self._modulus}, {self._value})").format(self=self)

    def __str__(self) -> str:
        return str(self._value)

    def __bytes__(self) -> bytes:
        return bytes(self._value)

    def __format(self, format_spec) -> str:
        return format(self._value, format_spec)

    __le__ = None
    __ge__ = None
    __lt__ = None
    __gt__ = None

    def __eq__(self, other) -> bool:
        if isinstance(other, ModuloN):
            result = self._modulus == other._modulus and self._value == other._value
        else:
            result = int(self) == other
        return result

    def __hash__(self) -> int:
        # Since __eq__ above allows ModuloN values to be equal to the open integers,
        # we can only rely on the _value field for the hash.
        return hash(self._value)

    def __bool__(self) -> bool:
        return self._value != 0

    def _operator_fallbacks(fallback_operator, doc=""):
        def forward(a, b):
            if isinstance(b, ModuloN):
                if a._modulus != b._modulus:
                    raise ValueError("inconsistent modulus values")
                return ModuloN(a._modulus, fallback_operator(a._value, b._value))
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
                return ModuloN(max(a._modulus, b._modulus), fallback_operator(a._value, b._value))
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

    __lshift__, __rlshift__ = _operator_fallbacks(operator.lshift)

    __rshift__, __rrshift__ = _operator_fallbacks(operator.rshift)

    __and__, __rand__ = _operator_fallbacks(operator.and_)

    __xor__, __rxor__ = _operator_fallbacks(operator.xor)

    __or__, __ror__ = _operator_fallbacks(operator.or_)

    def __neg__(self) -> 'ModuloN':
        return ModuloN(self._modulus, -self._value)

    def __pos__(self) -> 'ModuloN':
        return ModuloN(self._modulus, self._value)

    __abs__ = None

    def __invert__(self) -> 'ModuloN':
        return ModuloN(self._modulus, ~self._value)

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


__all__ = ('ModuloN')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
