#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""parse_ocr_txt.py: Parse raw ORC'd text of Kalfatovik's Nile Notes of a Howadji
"""

FIRST_ENTRY_NBR = 789
OCR_FILENAME = "raw_ocr.txt"

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