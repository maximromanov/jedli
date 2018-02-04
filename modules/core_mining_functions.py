#!C:\Python34\python.exe

"""
Core functions for working with Arabic sources
"""

import re
from re import match
from timeit import timeit

def deNoise(text):
    """
    This function eliminates all diacriticals from the text in
    order to faciliate its computational processing
    """
    noise = re.compile(""" َ  | # Fatha
                             ً  | # Tanwin Fath
                             ُ  | # Damma
                             ٌ  | # Tanwin Damm
                             ِ  | # Kasra
                             ٍ  | # Tanwin Kasr
                             ْ  | # Sukun
                             ـ | # Tatwil/Kashida
                             ّ # Tashdid
                             """, re.VERBOSE)
    text = re.sub(noise, "", text)
    text = re.sub("ﭐ", "ا", text) # replace alif-wasla with simple alif
    return text


def natural_sort(l, x):
    #http://stackoverflow.com/questions/6849047/naturally-sort-a-list-of-alpha-numeric-tuples-by-the-tuples-first-element-in-py
    """
    This function natural-sorts a list of lists (l),
    taking the element at index "x" as key
    natural sorting sorts alphabetical parts of a string alphabetically
    and numerical parts of a string numerically
    therefore, this function splits the string into alphabetical and numerical parts
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda item: [ convert(c) for c in re.split("([0-9]+)", x(item)) ]
    return sorted(l, key = alphanum_key)


def eraseNotes(text):
    """
    This function eliminates all end of page notes, as their
    presence might interfer with the computational analysis of
    the text. I think that the function is not very effective yet
    """    
    while "\n[1]" in text:
        point1 = text.find("\n[1]")        
        point2 = text.find("*", point1)
        text = text.replace(text[point1:point2], "\n")
    return text


def deNoise2(text):
    """
    This function converts all notes in the text to percentage
    symbols in order to eliminate these redundant digits that
    might interfer in the anlaysis of the text
    """
    noise = re.compile("\[\d*]", re.VERBOSE)
    text = re.sub(noise, "%", text)
    return text

def ignore_interword_characters(clause):
    """replace space in the search term with a regex that ignores 
    spaces, footnote references, line breaks, punctuation etc"""
    return re.sub(" ", r"(?:\W|\d|{}:|{}:|{}:)+".format("الصفحة", "الجزء", "الحديث"), clause)

