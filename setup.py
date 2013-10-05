# -*- coding: utf-8 -*-

from setuptools import setup

import sys
sys.path.append("test")

import cmigemo

setup(
    name             = "cmigemo",
    version          = cmigemo.__version__,
    author           = "Masafumi Oyamada",
    author_email     = "stillpedant@gmail.com",
    url              = "https://github.com/mooz/python-cmigemo",
    description      = "A pure python binding for C/Migemo",
    long_description = cmigemo.__doc__,
    test_suite       = "test_cmigemo",
    packages         = ["cmigemo"],
    classifiers      = ["Operating System :: POSIX"],
    keywords         = "C/Migemo ctypes",
    license          = "MIT",
    )
