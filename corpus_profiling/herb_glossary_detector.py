# Author: Eirini Valkana
# !/usr/bin/python

# script.py --herb_glossary [default is the trilingual one, DICT] --input files or file [if files then]
# --outfile

# get stats: out of all herbs in the glossary how many in Latin, English, French?
# filename, token id, herb, language ---> csv + printing

# get stats
# herb_name, language, number of instances ---> csv outfile
# out of all herbs detected, how many in Latin, English, French?
# print(language_stats: Latin, French, English)

import argparse
import pathlib
import requests
import json

# parser = argparse.ArgumentParser(description='Find herbs from 14th century Herb Glossary in Middle English texts.')
# parser.add_argument('--herb_glossary', type=dict,
#                     help=' A dict of dicts with herbs and their corresponding names in other languages')
# parser.add_argument('--input', type=pathlib.Path,
#                     help='path to the input file(s)')
# parser.add_argument('--output',
#                     help='name of the output csv file')
#
# args = parser.parse_args()


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def open_read_json(path_to_file):
    with open(path_to_file, "r") as infile:
        return json.load(infile)


herbs_dict = open_read_json("../data/herb_glossary.json")


# def check_if_herb(path_to_file):
#     with open(path_to_file)
#     for index, versions in herbs_dict.items():
#         for version, word in versions.items():
#






