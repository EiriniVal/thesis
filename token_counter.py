# Author: Eirini Valkana
# !/usr/bin/python

from lxml import etree
import os
import re
import csv
import pandas as pd


def has_old_char(token):
    """ assess if a token includes an old alphabet character ȝæðþƿ Returns True if yes:
    """
    if "ȝ"|"3"|"æ"|"ð"|"þ"|"ƿ" in token:
        return True
    return False


def is_roman_numeral(token):
    """ assess if a token is a roman numeral. Returns True if it is:
    the code was inspired from: https://dev.to/alexdjulin/a-python-regex-to-validate-roman-numerals-2g99
    it was modified so that it captures the middle ages variants of roman numerals which include
    lowercase letters,
    the last unit written as j instead of i,
    and the additive notation variant (iiii instead of iv)
    """
    pattern = re.compile(r"""   
                             ^(M|m){0,3}
                             (CM|cm|CD|cd|(D|d)?(C|c){0,4})?
                             (XC|xc|XL|xl|(L|l)?(X|x){0,4})?
                             (IX|ix|IV|iv|(V|v)?(I|i){0,4}(J|j)?)?$
                        """, re.VERBOSE)
    if re.match(pattern, token):
        return True
    return False


def has_scribal_abbrev(token):
    pattern = re.compile(r"[a-z]+(~|=)+[a-z]*(~|=)*")
    if re.match(pattern, token):
        return True
    return False


def get_vocab_counts(filename):
    """ counts tokens, types and yields returns the vocabulary (distinct words) of a single xml file"""
    token_counter = 0
    tree = etree.parse(filename)
    root = tree.getroot()
    # distinct words
    vocab = set()

    # roman_numerals
    roman_numerals = []

    # scribal_abbrev
    scribal_abbrev = []

    # old_alphabet
    old_alphabet = []

    for element in root.iter():
        if element.tag == "token":
            token_counter += 1
            vocab.add(element.text)

            if has_old_char(element.text):
                old_alphabet.append(element.text)

            if is_roman_numeral(element.text):
                roman_numerals.append(element.text)

            if has_scribal_abbrev(element.text):
                scribal_abbrev.append(element.text)

            # print(token_counter, element.text)

    type_counter = len(vocab)
    # print(f"Filename: {filename} \n\nNumber of tokens (running words): {token_counter} \n\nNumber of types: {type_counter} "
    #       f"\n\nVocabulary of {filename}: {vocab}")
    return token_counter, type_counter, vocab, old_alphabet, roman_numerals, scribal_abbrev

# get_vocab_counts("MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/01_MEMT_Texts/agnus_castus_converted.xml")


def corpus_profiling():
    """ create a csv table with the following columns: subcorpus, filename, tokens, types, old_alph counts, roman_numeral counts, scribal abbrev counts """
    for root, dirs, files in os.walk("./MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/", topdown=False):
        for name in files:
            # print(name)
            token_counter, type_counter, vocab, old_alphabet, roman_numerals, scribal_abbrev = get_vocab_counts(name)





