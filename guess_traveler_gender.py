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
DATABASE_FILE = "travelogues.sqlite3"

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession(WOLFRAM_KERNEL_LOCATION)

connection = sqlite3.connect(DATABASE_FILE)
db = connection.cursor()

db.execute("SELECT id, name, gender FROM travelers")
travelers = db.fetchall()

for traveler in travelers:
    if traveler[2] == None: #traveler[2] is gender
        name = traveler[1]
        traveler_id = traveler[0]
        # The following evaluates
        # Classify["NameGender", First[TextCases[name, "GivenName"]]]
        # in Wolfram Kernel
        gender = session.evaluate(
            wl.System.Classify("NameGender",
                wl.System.First(wl.System.TextCases(name, "GivenName")))
            )
        if type(gender) is str and gender != "Indeterminate":
            db.execute("""UPDATE travelers
                        SET gender = ?
                        WHERE id = ?""", (gender, traveler_id))

connection.commit()
session.stop()