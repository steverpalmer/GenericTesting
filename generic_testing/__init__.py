# Copyright 2018 Steve Palmer

"""Merge generic_testing into a single namespace."""

import version as _version
assert _version.version.is_backwards_compatible_with('1.0.0')

version = _version.Version('0.1.1')

from timeout import Timeout, version as timeout_version
assert timeout_version.is_backwards_compatible_with('1.0.0')

from isclose import IsClose, isclose, version as isclose_version
assert isclose_version.is_backwards_compatible_with('1.0.0')

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
