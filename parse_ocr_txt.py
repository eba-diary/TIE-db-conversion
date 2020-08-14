#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""parse_ocr_txt.py: Parse raw OCR'd text of Kalfatovik's Nile Notes of a Howadji
"""

import re
import json
from difflib import SequenceMatcher

FIRST_ENTRY_NBR = 789               # First entry number to parse. Used to check for failed entries.
LAST_ENTRY_NBR = 1150               # Last entry number to parse. Used to check for failed entries.
OCR_FILENAME = "raw_ocr.txt"        # Filename of OCR text
TITLES_FILENAME = "titles.json"     # Filename of JSON list containing potential titles
OUTPUT_FILENAME = "ocr_parsed.json" # Filename of JSON output

# keys of the dictionaries that represent Entries and Works respectively
entry_keys = ["number", "name", "works", "travel_date", "nationality"]
work_keys = ["title", "publishing_info", "annotation"]

ocr_file = open(OCR_FILENAME)
ocr_text = ocr_file.read()
ocr_file.close()

ocr_text = re.sub(r"(\n+)(\d{4}-\d{4})( )(\d{3})( ?)", "", ocr_text)
ocr_text = re.sub(r"(\n+)(\d| )+(Nile Notes of a Howadji)( ?)", "", ocr_text)
ocr_text = re.sub(r"\n{3,}", "\n\n", ocr_text)
ocr_text.rstrip()
entry_paragraphs = ocr_text.split("\n\n")

entries = []
good_entry_nbrs = []
entry_nbr = FIRST_ENTRY_NBR
while len(entry_paragraphs) > 0:
    try:
        #prepare entry
        entry = dict.fromkeys(entry_keys)
        entry["works"] = []

        #read entry title
        paragraph = entry_paragraphs.pop(0)
        lead = str(entry_nbr)
        if len(lead) < 4: lead = "0" + lead
        if not paragraph.startswith(lead):
            raise RuntimeError("Expected start of entry {0} but got '{1}'".format(entry_nbr, paragraph))
        entry["number"] = entry_nbr
        entry["name"] = paragraph[5:]

        #read first work paragraph
        paragraph = entry_paragraphs.pop(0)
        work = dict.fromkeys(work_keys)
        work["title"] = paragraph.replace("\n", "")
        entry["works"].append(work)

        paragraph = entry_paragraphs.pop(0)
        if not paragraph.startswith("Date of Travel"):
            #read second work paragraph
            work = dict.fromkeys(work_keys)
            work["title"] = paragraph.replace("\n", "")
            entry["works"].append(work)
            paragraph = entry_paragraphs.pop(0)

        #read date of travel paragraph
        entry["travel_date"] = paragraph[len("Date of Travel: ") : paragraph.index("Nationality")].strip()
        entry["nationality"] = paragraph[paragraph.index("Nationality: ") + len("Nationality: "):].strip()

        #read first annotation
        paragraph = entry_paragraphs.pop(0)
        entry["works"][0]["annotation"] = paragraph.replace("\n", "")
        if re.match(r"\d{4} ", entry_paragraphs[0]): #if the next paragraph is an entry title
            if len(entry["works"]) == 2:
                entry["works"][1]["annotation"] = paragraph.replace("\n", "")
        else:
            #read second annotation
            paragraph = entry_paragraphs.pop(0)
            entry["works"][1]["annotation"] = paragraph.replace("\n", "")
        entries.append(entry)
        good_entry_nbrs.append(entry_nbr)
        entry_nbr += 1
    except (IndexError, ValueError, RuntimeError):
        # if there's a problem with this entry, we skip to the next one
        next_entry_found = False
        while not next_entry_found and len(entry_paragraphs) > 0:
            next_paragraph = entry_paragraphs[0]
            next_entry_nbr = re.match(r"(\d{4}) ", next_paragraph)
            if next_entry_nbr:
                next_entry_found = True
                entry_nbr = int(next_entry_nbr.group(0))
            else:
                entry_paragraphs.pop(0)

# separate the title of each work from its publishing information
titles = json.load(open(TITLES_FILENAME))
for entry_index, entry in enumerate(entries):
    for work_index, work in enumerate(entry["works"]):
        title = work["title"]
        words = title.split(" ")
        title_confidences = {}
        for word_nbr in range(2 if len(words) > 2 else 1, len(words)): # start with 2 words if possible to avoid false positives
            substring = " ".join(words[:word_nbr])
            similarities = {title: SequenceMatcher(None, substring, title).ratio() for title in titles}
            best_match = max(similarities, key=similarities.get)
            title_confidences[word_nbr] = (best_match, similarities[best_match])
        title_end_index = max(title_confidences, key=lambda title: title_confidences[title][1])
        final_title = " ".join(words[:title_end_index])
        publishing_info = " ".join(words[title_end_index:])
        entries[entry_index]["works"][work_index]["title"] = final_title
        entries[entry_index]["works"][work_index]["publishing_info"] = publishing_info
        titles.remove(title_confidences[title_end_index][0]) # remove the best match from this list to reduce runtime
    print("Separated titles and publishing info of {0}/{1} entries".format(entry_index + 1, len(entries)))

# load them into a JSON file
with open(OUTPUT_FILENAME, 'w') as output:
    json.dump(entries, output)

failed_entry_nbrs = [nbr for nbr in range(FIRST_ENTRY_NBR, LAST_ENTRY_NBR + 1) if nbr not in good_entry_nbrs]

print("# of successful entries:", len(entries))
print("# of entries failed:", len(failed_entry_nbrs))
print("Entry numbers of failed entries:")
print(failed_entry_nbrs)
print("DONE")