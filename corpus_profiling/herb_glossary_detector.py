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

# import argparse
# import pathlib
#
# parser = argparse.ArgumentParser(description='Find herbs in Old English texts.')
# parser.add_argument('--herb_glossary', type=dict,
#                     help=' A dict of dicts with herbs and their corresponding names in other languages')
# parser.add_argument('--input', type=pathlib.Path,
#                     help='path to the input file(s)')
# parser.add_argument('--output',
#                     help='name of the output csv file')
#
# args = parser.parse_args()
#
# import requests
# import json
#
#
# def jprint(obj):
#     # create a formatted string of the Python JSON object
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)
#
# response = requests.get("https://latinwordnet.exeter.ac.uk/api/lemmas/filix/n/synsets")
#
# results = response.json()["results"]
#
# for key, value in results[0].items():
#     if key == "gloss":
#         print(value)