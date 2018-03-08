# Copyright 2018 Steve Palmer

"""Merge generic_testing into a single namespace."""

__version__ = "0.1"

from .isclose import IsClose

from .core import *
from .relations import *
from .arithmetic import *
from .lattices import *
from .numbers_abc import *
from .collections_abc import *
from .augmented_assignment import *
from .built_in_types import *
from .loader import *
