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
    # regex groups: 1:(YYY-) 2:(YYYY-) 3:(YYYY) 4:(YYYY-YY) 5:(YYYY-YYYY)
    match = re.match(
        r"(^[0-9]{3}-$)|(^[0-9]{4}\-$)|(^[0-9]{4}$)|(^[0-9]{4}-[0-9]{2}$)|(^[0-9]{4}-[0-9]{4}$)",
        datetoken
        )
    if match.group(1):
        year = match.group(1)[:3].replace("-", "") + "0"
    elif match.group(2):
        year = match.group(2).replace("-", "")
    elif match.group(3):
        year = match.group(3)
    elif match.group(4):
        years = match.group(4).split("-")
        if get_min:
            year = years[0]
        else:
            year = years[0][:2] + years[1]
    elif match.group(5):
        year = match.group(5).split("-")[0 if get_min else 1]
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
