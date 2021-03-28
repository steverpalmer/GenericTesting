# Copyright 2018 Steve Palmer

"""Merge generic_testing into a single namespace."""

try:
    import version as _version

    if not _version.version.is_backwards_compatible_with("1.0.0"):
        raise ImportError("Incompatible Version of version")
except ImportError:
    _version = type("_version", (object,), {"Version": lambda self, s: s})()  # Dummy

version = _version.Version("0.1.1")

from .timeout import Timeout, version as timeout_version
if not isinstance(timeout_version, str) and not timeout_version.is_backwards_compatible_with("2.0.0"):
    raise ImportError("Incompatible version of timeout")

from .isclose import IsClose, isclose, version as isclose_version
if not isinstance(isclose_version, str) and not isclose_version.is_backwards_compatible_with("1.0.0"):
    raise ImportError("Incompatible version of isclose")

from .core import *
from .relations import *
from .arithmetic import *
from .lattices import *
from .numbers_abc import *
from .collections_abc import *
from .augmented_assignment import *
from .built_in_types import *
from .enums import *
from .file_likes import *

from .loader import *
