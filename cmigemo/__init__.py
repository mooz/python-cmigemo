# -*- coding: utf-8 -*-

"""A C/Migemo binding for python written in pure python using ctypes."""

__version__ = "0.0.2"

DICTID_INVALID = 0
DICTID_MIGEMO = 1
DICTID_ROMA2HIRA = 2
DICTID_HIRA2KATA = 3
DICTID_HAN2ZEN = 4
DICTID_ZEN2HAN = 5

OPINDEX_OR = 0
OPINDEX_NEST_IN = 1
OPINDEX_NEST_OUT = 2
OPINDEX_SELECT_IN = 3
OPINDEX_SELECT_OUT = 4
OPINDEX_NEWLINE = 5

from migemo import Migemo
