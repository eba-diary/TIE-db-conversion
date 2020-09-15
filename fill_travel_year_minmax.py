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

for publication in publications:
    pub_id = publication[0]
    datestring = publication[1]
    if datestring == None: continue

    datestring = re.sub(r"[^0-9 \-]", "", datestring).strip()
    print(datestring)
    dates = datestring.split()
    if len(dates) == 1:
        match = re.match(r"^[0-9]{3}-", dates[0])
        if match:
            partial_year = match.group(0)[:3].replace("-", "")
        
