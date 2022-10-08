# Author: Eirini Valkana
# !/usr/bin/python

import os
import json
import xml.etree.ElementTree as ET


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def open_read_json(path_to_file):
    with open(path_to_file, "r") as infile:
        return json.load(infile)


herbs_dict = open_read_json("../data/herb_glossary.json")

# print(herbs_dict)

def get_herb_id(token):
    herb_id = ""
    lang_id = ""
    for id, lang_versions in herbs_dict.items():
        for lang, herb_name in lang_versions.items():
            # every herb in the glossary is lowercased, therefore we should also lowercase the tokens
            if token.lower() == herb_name:
                # print(herb_id, lang)
                if "Latin" in lang:
                    lang_id = "LA"
                elif "English" in lang:
                    lang_id = "EN"
                elif "French" in lang:
                    lang_id = "FR"
                herb_id = id
                #  a token may have more than one herb ids, e.g. "walewort", but for simplification reasons we are only
                #  keeping one id
    return herb_id, lang_id


def find_herbs_write_file(path_to_file):
    tree = ET.parse(path_to_file)
    tree_root = tree.getroot()
    for element in tree_root.iter():
        if element.tag == "token":
            # if the token is a herb (if list is not empty)
            herb_id, lang_id = get_herb_id(element.text.lower())
            if herb_id != "" and lang_id != "":
                element.attrib["herb_id"] = herb_id
                element.attrib["lang_id"] = lang_id
                print(herb_id, lang_id)

    # update xml files with info related to special tokens
    f = open(path_to_file, 'wb')
    f.write(ET.tostring(tree_root, encoding='utf-8', xml_declaration=True))
    f.close()


def main():
    for root, dirs, files in os.walk("../data/MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/", topdown=False):
        for name in files:
            infile = os.path.join(root, name)
            # update xml files with herb findings
            find_herbs_write_file(infile)


if '__name__' == main():
    main()

