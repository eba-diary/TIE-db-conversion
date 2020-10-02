#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""guess_traveler_gender.py - Looks at the travelers table and uses Wolfram Client Library to
execute code that guesses the traveler's gender from their name. The guess is put in the gender
column if it has null value. If the guess is indeterminate, it will not change the gender in the DB.

This requires Wolfram Client Library for Python and a Wolfram Kernel.
https://reference.wolfram.com/language/WolframClientForPython/
"""
import sqlite3

WOLFRAM_KERNEL_LOCATION = "/opt/Mathematica/SystemFiles/Kernel/Binaries/Linux-x86-64/WolframKernel"

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession(WOLFRAM_KERNEL_LOCATION)