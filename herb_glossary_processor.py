# Author: Eirini Valkana
# !/usr/bin/python

import re
from collections import defaultdict
import json


def get_dict_from_herb_glossary(filename):
    """
    function that removes annotations from the herb glossary and writes the information in a json format file
    :param filename: the herb glossary
    :return: json file
    """
    herb_dict = defaultdict(dict)
    # patterns that denote annotations by the transcribers
    replacements = [
        (r"\s\n", ""),
        (r"\[}|}]", ""),
        (r"\[{|{]", ""),
        (r"\[\\.+\\]", ""),
        (r"\[/.+/]", ""),
        (r"\[\^.+\^]", ""),
        (r"\|P_\w*$", "")]
    with open(filename, "rb") as infile:
        for line in infile:
            # catch Unicode Decode Error
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                # print(line)
                line = line.decode('cp1252').encode("utf-8").decode("utf-8")
            # if line is not empty
            # print(line, "The line is not empty")
            for old, new in replacements:
                line = re.sub(old, new, line)
            if len(line.strip()):
                # print(line.strip())
                line = line.strip()
                line = re.split(": |, |- ", line)
                # print(line)
                for word in line[1:]:
                    if word.startswith("gall.") and re.sub("gall\.\s?", "", word) != "":
                        herb_dict[line[0]]["fr"] = re.sub("gall\. ", "", word)
                    elif re.match("angl?\.\s?", word) and re.sub("angl?\.\s?", "", word) != "":
                        herb_dict[line[0]]["en"] = re.sub("angl?\.\s?", "", word)
                    else:
                        herb_dict[line[0]]

    json_glossary = json.dumps(herb_dict, sort_keys=True, indent=4, ensure_ascii=False)
    print(json_glossary)
    with open("data/herb_glossary.json", "w") as outfile:
        outfile.write(json_glossary)


get_dict_from_herb_glossary("data/trilingual_herb_glossary_converted.txt")

