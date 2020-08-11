#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""parse_ocr_txt.py: Parse raw ORC'd text of Kalfatovik's Nile Notes of a Howadji
"""

import re

FIRST_ENTRY_NBR = 789           # First entry number to parse.
OCR_FILENAME = "raw_ocr.txt"    # Filename of OCR text

# keys of the dictionaries that represent Entries and Works respectively
entry_keys = ["number", "name", "works", "travel_date", "nationality"]
work_keys = ["title", "annotation"]

def is_page_header(line):
    """Return True if the given line of text is a page header
    e.g. "278 Nile Notes of a Howadji" (even pages) or "1880-1889 - 279 " (odd pages)
    """
    even_page =  bool(re.match(r"(\d| )+(Nile Notes of a Howadji)( ?)", line))
    odd_page =  bool(re.match(r"(\d{4}-\d{4})( )(\d{3})( ?)$", line))
    return even_page or odd_page

ocr_file = open(OCR_FILENAME)
ocr_lines = ocr_file.readlines()
ocr_file.close()

ocr_lines = filter(lambda line: not is_page_header(line), ocr_lines)
ocr_text = "".join(ocr_lines)
ocr_text = re.sub(r"\n{3,}", "\n\n", ocr_text)
entry_paragraphs = ocr_text.split("\n\n")

#if the next paragraph isn't an entry title
    #read second annotation

entries = []

#prepare entry
entry = dict.fromkeys(entry_keys)
entry["works"] = []

#read entry title
paragraph = entry_paragraphs.pop(0)
entry_nbr = FIRST_ENTRY_NBR
lead = str(entry_nbr)
if len(lead) < 4: lead = "0" + lead
if not paragraph.startswith(lead):
    raise RuntimeError("Expected start of entry {0} but got '{1}'".format(current_entry_nbr, paragraph))
entry["number"] = entry_nbr
entry["name"] = paragraph[5:]

#read first work paragraph
paragraph = entry_paragraphs.pop(0)
work = dict.fromkeys(work_keys)
work["title"] = paragraph
entry["works"].append(work)

#if the next paragraph doesn't start with "Date of Travel"
paragraph = entry_paragraphs.pop(0)
if not paragraph.startswith("Date of Travel"):
    #read second work paragraph
    work = dict.fromkeys(work_keys)
    work["title"] = paragraph
    entry["works"].append(work)
    paragraph = entry_paragraphs.pop(0)

#read date of travel paragraph
entry["travel_date"] = paragraph[len("Date of Travel: ") : paragraph.index("Nationality")].strip()
entry["nationality"] = paragraph[paragraph.index("Nationality: ") + len("Nationality: "):].strip()

#read first annotation
paragraph = entry_paragraphs.pop(0)


print(entry)