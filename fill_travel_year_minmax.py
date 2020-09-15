#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""fill_travel_year_minmax.py - Parses the travel_dates column and puts the min and max years into
the appropriate columns
"""

import sqlite3
import re

DATABASE_FILE = "travelogues.sqlite3"

connection = sqlite3.connect(DATABASE_FILE)
db = connection.cursor()

db.execute("SELECT id, travel_dates FROM publications")
publications = db.fetchall()

