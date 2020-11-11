"""download_ia_texts.py - Looks at each publication's the ia_ident column in the DB to see if it has
an associated Internet Archive entry, and tries to download the DJVU plaintext scan
"""
from internetarchive import get_files
import sqlite3

DATABASE_FILE = "travelogues.sqlite3"

connection = sqlite3.connect(DATABASE_FILE)
db = connection.cursor()

db.execute("SELECT ia_ident FROM publications WHERE ia_ident NOT NULL")
ia_idents = [publication[0] for publication in db.fetchall()]

for ident in ia_idents:
    files = get_files(ident, glob_pattern="*djvu.txt", formats="txt")
    try:
        txt_file = next(files)
        txt_file.download(file_path=f"./txt_files/{ident}.txt")
    except StopIteration:
        print("No djvu plaintext scan found for", ident)