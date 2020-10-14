#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""find_in_internetarchive.py - Searches Internet Archive for publications in the database using
their titles and author names. This gets stored in the ia_ident column. It also updates the iiif
column with the presumed IIIF manifest link.

If the ia_ident column already has a value, the publication is skipped and no changes will be made
to its row.
"""
from internetarchive import search_items
from json import JSONDecodeError
import re
import sqlite3

DATABASE_FILE = "travelogues.sqlite3"

connection = sqlite3.connect(DATABASE_FILE)
db = connection.cursor()

db.execute(
    """SELECT p.id, p.title, t.name, p.ia_ident FROM contributions c
        JOIN publications p ON p.id = c.publication_id
        JOIN travelers t ON t.id = c.traveler_id
        WHERE c.type = 'Author'
    """
    )
publications = db.fetchall()

succeeded = []
for publication in publications:
    publication_id = publication[0]
    current_ident = publication[3]
    if current_ident == None and publication_id not in succeeded:
        title = re.sub(r"[^\w\s']", " ", publication[1])
        author = " OR ".join(re.sub(r"[^\w\s]|[0-9]", "", publication[2]).split())
        results = search_items(f"title:({title}) AND creator:({author}) AND mediatype:(texts) AND -access-restricted-item:(true)", fields=["type"]).iter_as_items()
        try:
            ident = next(results).identifier
            print(ident)
            db.execute(
                """UPDATE publications
                    SET ia_ident = ?,
                        iiif = ?
                    WHERE id = ?""",
                (ident,f"https://iiif.archivelab.org/iiif/{ident}/manifest.json", publication_id))
            succeeded.append(publication_id)
        except (StopIteration, JSONDecodeError):
            print("Failed to find anything for", publication_id, title)

connection.commit()