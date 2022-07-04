# Author: Eirini Valkana
# !/usr/bin/python

from lxml import etree
import os
import re
import pandas as pd
from collections import defaultdict


def has_old_char(token):
    """ assess if a token includes an old alphabet character ȝæðþƿ Returns True if yes:
    """
    # if token has yogh as number 3
    pattern = re.match(r"[^0-9\s]*3[^0-9\s]+|[^0-9\s]+3[^0-9\s]*", token)
    if pattern:
        return True
    # if token has old alphabet
    pattern2 = re.match(r".*[ȝæðþƿ].*", token)
    if pattern2:
        return True
    return False


# TODO what about pronoun "I"? should i not count it as numeral anyway?
def is_roman_numeral(token):
    """ assess if a token is a roman numeral. Returns True if it is:
    the code was inspired from: https://dev.to/alexdjulin/a-python-regex-to-validate-roman-numerals-2g99
    it was modified so that it captures the middle ages variants of roman numerals which include
    lowercase letters,
    the last unit written as j instead of i,
    and the additive notation variant (iiii instead of iv)
    """
    pattern = re.compile(r"""   
                             ^([Mm]){0,3}
                             (CM|cm|CD|cd|([Dd])?([Cc]){0,4})?
                             (XC|xc|XL|xl|([Ll])?([Xx]){0,4})?
                             (IX|ix|IV|iv|([Vv])?([Ii]){2,4}([Jj])?)?$
                        """, re.VERBOSE)
    if re.match(pattern, token):
        return True
    return False


def has_scribal_abbrev(token):
    pattern = re.compile(r"[a-z]+([~=])+[a-z]*([~=])*", re.IGNORECASE)
    if re.match(pattern, token):
        return True
    return False


def is_number(token):
    pattern = re.compile("^[+-]?(\d*\.)?\d+$")
    if re.match(pattern, token):
        return True
    return False


def get_vocab_counts(filename):
    """ counts tokens, types and yields returns the vocabulary (distinct words) of a single xml file"""
    token_counter = 0
    tree = etree.parse(filename)
    root = tree.getroot()
    # distinct words ALL
    vocab = set()

    # distinct words no roman numerals, no numbers, no lowercasing
    vocab_no_numbers = set()

    # distinct words no roman numerals, no numbers, with lowercasing
    vocab_strict = set()

    # roman_numerals
    roman_numerals = {}

    # scribal_abbrev
    scribal_abbrev = {}

    # old_alphabet
    old_alphabet = {}

    # numbers
    numbers = {}

    for element in root.iter():
        if element.tag == "year":
            year_info = element.text
        if element.tag == "token":
            vocab.add(element.text)

            if has_old_char(element.text):
                element.attrib["old_char"] = "True"
                old_alphabet[element.get("id")] = element.text
                token_counter += 1
                # add to strict vocab lowercased
                vocab_strict.add(element.text.lower())
                # add to no num vocab
                vocab_no_numbers.add(element.text)

            elif is_roman_numeral(element.text):
                element.attrib["rom_num"] = "True"
                roman_numerals[element.get("id")] = element.text

            elif has_scribal_abbrev(element.text):
                element.attrib["scrib_abbrev"] = "True"
                scribal_abbrev[element.get("id")] = element.text
                token_counter += 1
                vocab_strict.add(element.text.lower())
                vocab_no_numbers.add(element.text)

            elif is_number(element.text):
                element.attrib["num"] = "True"
                numbers[element.get("id")] = element.text

            else:
                token_counter += 1


            # print(token_counter, element.text)

    type_counter = len(vocab_strict)

    # update xml files with info related to special tokens
    f = open(filename, 'wb')
    f.write(etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True))
    f.close()

    # token counter is without numbers, type_counter is the length of the strict vocab aka no numbers, no roman numerals and lowercased

    return token_counter, type_counter, vocab, old_alphabet, roman_numerals, scribal_abbrev, year_info, numbers, vocab_no_numbers, vocab_strict


# get_vocab_counts("MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/01_MEMT_Texts/agnus_castus_converted.xml")


def corpus_profiling():
    """ create a dataframe with the following columns: subcorpus, filename, tokens, types, old_alph counts,
    roman_numeral counts, scribal abbrev counts """

    corpus_data = defaultdict(list)

    # initialize vocabulary (sets)
    vocab_corpus1 = set()
    vocab_corpus2 = set()
    vocab_corpus3 = set()
    vocab_total = set()

    vocab_nonum_1 = set()
    vocab_nonum_2 = set()
    vocab_nonum_3 = set()
    vocab_nonum_total = set()

    vocab_strict_1 = set()
    vocab_strict_2 = set()
    vocab_strict_3 = set()
    vocab_strict_total = set()

    for root, dirs, files in os.walk("./data/MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/", topdown=False):
        for name in files:
            infile = os.path.join(root, name)
            token_counter, type_counter, vocab, old_alphabet, roman_numerals, scribal_abbrev, year_info, numbers, vocab_no_numbers, vocab_strict = get_vocab_counts(infile)

            # add sub-corpus name
            if "01_MEMT" in root:
                # print(root)
                corpus_data["sub_corpus"].append("01_MEMT")

                # generate vocabulary of MEMT subcorpus
                vocab_corpus1 = vocab_corpus1.union(vocab)
                vocab_nonum_1 = vocab_nonum_1.union(vocab_no_numbers)
                vocab_strict_1 = vocab_strict_1.union(vocab_strict)

            if "02_EMEMT" in root:
                corpus_data["sub_corpus"].append("02_EMEMT")

                # generate vocabulary of EMEMT subcorpus
                vocab_corpus2 = vocab_corpus2.union(vocab)
                vocab_nonum_2 = vocab_nonum_2.union(vocab_no_numbers)
                vocab_strict_2 = vocab_strict_2.union(vocab_strict)

            if "03_LMEMT" in root:
                corpus_data["sub_corpus"].append("03_LMEMT")

                # generate vocabulary of LMEMT subcorpus
                vocab_corpus3 = vocab_corpus3.union(vocab)
                vocab_nonum_3 = vocab_nonum_3.union(vocab_no_numbers)
                vocab_strict_3 = vocab_strict_3.union(vocab_strict)

                # if letter in date remove
                year_info = "".join(filter(str.isdigit, year_info))

                # if year info is span keep first year
                if "-" in year_info:
                    year_info = year_info.split("-")[0]

            # generate vocabulary of the whole corpus
            vocab_total = vocab_total.union(vocab)
            vocab_nonum_total = vocab_nonum_total.union(vocab_no_numbers)
            vocab_strict_total = vocab_strict_total.union(vocab_strict)


            # CREATE DATAFRAME

            # gather data
            corpus_data["filename"].append(name)
            corpus_data["year"].append(year_info)
            corpus_data["tokens"].append(token_counter)
            corpus_data["types"].append(type_counter)
            corpus_data["old_alphabet_counts"].append(len(old_alphabet))
            corpus_data["roman_numerals_counts"].append(len(roman_numerals))
            corpus_data["scribal_abbrev_counts"].append(len(scribal_abbrev))
            corpus_data["numbers"].append(len(numbers))

    df = pd.DataFrame(data=corpus_data)

    return df, vocab_total, vocab_corpus1, vocab_corpus2, vocab_corpus3, vocab_nonum_total, vocab_nonum_1, vocab_nonum_2, vocab_nonum_3, vocab_strict_total, vocab_strict_1, vocab_strict_2, vocab_strict_3


def main():
    """ write files """
    df, vocab_total, vocab_corpus1, vocab_corpus2, vocab_corpus3, vocab_nonum_total, vocab_nonum_1, vocab_nonum_2, vocab_nonum_3, vocab_strict_total, vocab_strict_1, vocab_strict_2, vocab_strict_3 = corpus_profiling()

    # write dataframe to csv
    os.makedirs('./corpus_profiling', exist_ok=True)
    df.to_csv('./corpus_profiling/corpus_data.csv')

    os.makedirs('./vocabulary', exist_ok=True)

    # write vocabularies in files
    with open('./vocabulary/vocab_total.txt', "w") as out:
        for elem in vocab_total:
            out.write(elem+"\n")

    with open('./vocabulary/vocab_corpus1.txt', "w") as out1:
        for elem in vocab_corpus1:
            out1.write(elem+"\n")

    with open('./vocabulary/vocab_corpus2.txt', "w") as out2:
        for elem in vocab_corpus2:
            out2.write(elem+"\n")

    with open('./vocabulary/vocab_corpus3.txt', "w") as out3:
        for elem in vocab_corpus3:
            out3.write(elem+"\n")

    with open('./vocabulary/vocab_nonum_total.txt', "w") as out4:
        for elem in vocab_nonum_total:
            out4.write(elem+"\n")

    with open('./vocabulary/vocab_nonum_corpus1.txt', "w") as out5:
        for elem in vocab_nonum_1:
            out5.write(elem+"\n")

    with open('./vocabulary/vocab_nonum_corpus2.txt', "w") as out6:
        for elem in vocab_nonum_2:
            out6.write(elem+"\n")

    with open('./vocabulary/vocab_nonum_corpus3.txt', "w") as out7:
        for elem in vocab_nonum_3:
            out7.write(elem+"\n")

    with open('./vocabulary/vocab_strict_total.txt', "w") as out8:
        for elem in vocab_strict_total:
            out8.write(elem + "\n")

    with open('./vocabulary/vocab_strict_corpus1.txt', "w") as out9:
        for elem in vocab_strict_1:
            out9.write(elem + "\n")

    with open('./vocabulary/vocab_strict_corpus2.txt', "w") as out10:
        for elem in vocab_strict_2:
            out10.write(elem + "\n")

    with open('./vocabulary/vocab_strict_corpus3.txt', "w") as out11:
        for elem in vocab_strict_3:
            out11.write(elem + "\n")


if __name__ == "__main__":
    main()
