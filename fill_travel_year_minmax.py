#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""fill_travel_year_minmax.py - Parses the travel_dates column and puts the min and max years into
the appropriate columns
"""

import sqlite3
import re

DATABASE_FILE = "travelogues.test.sqlite3"

connection = sqlite3.connect(DATABASE_FILE)
db = connection.cursor()

db.execute("SELECT id, travel_dates FROM publications")
publications = db.fetchall()

def get_year(datetoken, get_min):
    """ Get the min or max year from a date token from the database.
        Tokens are a single year or range of two years.
        datetoken - date token from the database.
        get_min - gets the min if true, max if false
    """
    year = None
    match = re.match(
        r"(^[0-9]{3}-$)|(^[0-9]{4}\-$)|(^[0-9]{4}$)|(^[0-9]{4}-[0-9]{2}$|(^[0-9]{4}-[0-9]{4}$))",
        datetoken
        )
    if match:
        partial_year = match.group(0)[:3].replace("-", "")
        year = partial_year + ("0" if get_min else "9")
    return year

for publication in publications:
    pub_id = publication[0]
    datestring = publication[1]
    if datestring == None: continue

    datestring = re.sub(r"[^0-9 \-]", "", datestring).strip()
    dates = datestring.split()
    min_year = get_year(dates[0], True)
    max_year = get_year(dates[-1], False)
    
        
    db.execute("""UPDATE publications
                  SET travel_year_min = ?, travel_year_max = ?
                  WHERE id = ?""", (min_year, max_year, pub_id))
connection.commit()
