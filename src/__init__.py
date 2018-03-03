#!/usr/bin/env python3
"""
Copyright 2018 Steve Palmer

Merge generic_testing into a single namespace
"""
from . import isclose

from .core import *
from .arithmetic import *
from .lattices import *
from .numbers_abc import *
from .collections_abc import *
from .built_in_types import *
from .loader import *