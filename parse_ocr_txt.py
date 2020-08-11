#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""parse_ocr_txt.py: Parse raw ORC'd text of Kalfatovik's Nile Notes of a Howadji
"""

import re

FIRST_ENTRY_NBR = 789           # First entry number to parse. Used for error checking.
OCR_FILENAME = "raw_ocr.txt"    # Filename of OCR text

class Entry:
    """Represents an entry in the book"""
    def __init__(self, number, name, works, travel_date, nationality):
        self.number = number
        self.name = name
        self.works = []
        self.travel_date = travel_date
        self.nationality = nationality

class Work:
    """Represents an author's work/publication"""
    def __init__(self, title, annotation):
        self.title = title
        self.annotation = annotation

def is_page_header(line):
    """Return True if the given line of text is a page header
    e.g. "278 Nile Notes of a Howadji" (even pages) or "1880-1889 - 279 " (odd pages)
    """
    even_page =  bool(re.match(r"(\d{1,3})( )(Nile Notes of a Howadji)( ?)", line))
    odd_page =  bool(re.match(r"(\d{4}-\d{4})( )(\d{3})( ?)", line))
    return even_page or odd_page

ocr_file = open(OCR_FILENAME)
ocr_lines = ocr_file.readlines()
ocr_file.close()

entries = []
current_entry = FIRST_ENTRY_NBR
for line in ocr_lines:
    print(line)