#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""csv_to_tie_db.py: Adds rows from the travelogues .csv file to the .sqlite3 SQL database
"""

import sqlite3
import csv

DATABASE_FILE = "travelogues.sqlite3"
CSV_FILE = "travelogues.csv"
CSV_COLUMNS = [
    "DATE OF TRAVEL",
    "TITLE",
    "PLACE OF PUBLICATION",
    "PUBLISHER",
    "DATE OF PUBLICATION",
    "SUMMARY",
    "URL",
    "IIIF"
    ]

connection = sqlite3.connect(DATABASE_FILE)
db = connection.cursor()

with open(CSV_FILE) as csvfile:
    reader = csv.DictReader(csvfile)
    travelers = []
    for row in reader:
        #insert traveler/get traveler ID
        traveler = (row["NAME OF TRAVELER"], row["NATIONALITY"])
        traveler_id = None
        if traveler != ("", ""):
            if traveler not in travelers:
                travelers.append(traveler)
                db.execute("""INSERT INTO travelers (name, nationality)
                            VALUES (?, ?)""", traveler)
                traveler_id = db.lastrowid
            else:
                db.execute("SELECT id FROM travelers WHERE name=? AND nationality=?", traveler)
                traveler_id = db.fetchall()[0][0]

        #insert publications
        publication = [row[column] for column in CSV_COLUMNS]
        publication = [cell if cell != "" else None for cell in publication] #make empty string cells NULL in db
        publication.append(traveler_id)
        db.execute("""INSERT INTO publications (travel_dates, title, publication_place, publisher, publication_date, summary, url, iiif, traveler_id)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", publication)

connection.commit()