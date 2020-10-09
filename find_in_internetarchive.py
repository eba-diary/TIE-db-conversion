#!/usr/bin/env python
# -*- coding: utf-8 -*-

from internetarchive import search_items
from json import JSONDecodeError
import string
import sqlite3

DATABASE_FILE = "travelogues.test.sqlite3"

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
        title = publication[1].translate(str.maketrans(string.punctuation, " "*len(string.punctuation)))
        author = " OR ".join(publication[2].split(" "))
        results = search_items(f"title:({title}) AND creator:({author}) AND mediatype:(texts)", fields=["type"]).iter_as_items()
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