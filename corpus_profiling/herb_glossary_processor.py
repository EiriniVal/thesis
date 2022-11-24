# Script that processes the Trilingual Herb Glossary and structures its contents into a JSON file.

import re
from collections import defaultdict
import json


def generate_variable_names(num_var, lang_code):
    i = 1
    variable_names = []
    while i <= num_var:
        name = f"{lang_code}_v{i}"
        variable_names.append(name)
        i += 1

    return variable_names


def generate_versions_list(line):
    if re.search(",|/", line):
        return re.split(r",\s?|\s?/\s?", line)
    else:
        return [line]


def get_dict_from_herb_glossary(filename):
    """
    function that removes annotations from the herb glossary and writes the information in a json format file
    :param filename: the herb glossary
    :return: json file
    """
    herb_dict = defaultdict(dict)
    latin_v2 = ""
    herb_id = 1
    # remove annotations from the glossary
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
                line = line.decode('cp1252').encode("utf-8").decode("utf-8")
            for old, new in replacements:
                line = re.sub(old, new, line)
                line = line.strip()
            if len(line):
                line_split = re.split(": ", line)

                # get Latin entries
                latin = line_split[0]

                # if latin has more than one words e.g. "Accorum, affrodisia: angl. lavre"
                if re.search(",|/", latin):
                    la_var_names = generate_variable_names(len(re.split(r",\s?|\s?/\s?", latin)), "Latin")
                    latin_versions = generate_versions_list(latin)
                else:
                    la_var_names = generate_variable_names(1, "Latin")
                    latin_versions = [latin]

                # n is the name of the variable that denotes the language, v is the word itself
                for n, v in zip(la_var_names, latin_versions):
                    herb_dict[herb_id][n] = v.lower()

                # if original line has additional information on English and French and not only on Latin
                if len(line_split) != 1:
                    eng_fr = line_split[1]
                    # split on angl. and get word
                    eng_fr_split = re.split(r"angl?\.\s?", eng_fr)
                    if eng_fr_split[0] != "":
                        # ['gall. lavendre, ', '']
                        # ['gall. -, '']
                        # ['', 'hemelok']
                        # ['', '']

                        # get French entries
                        if "gall." in eng_fr_split[0]:
                            french_version = re.sub(r"gall\.\s?", "", eng_fr_split[0])
                            if french_version != "- ":
                                french_version = re.sub(r",\s?", "", french_version)

                                herb_dict[herb_id]["French"] = french_version.lower()

                    # get English entries
                    if eng_fr_split[1] != "":
                        english = eng_fr_split[1]
                        if re.search(",|/", english):
                            en_var_names = generate_variable_names(len(re.split(r",\s?|\s?/\s?", english)), "English")
                            english_versions = generate_versions_list(english)
                        else:
                            en_var_names = generate_variable_names(1, "English")
                            english_versions = [english]

                    for n_e, v_e in zip(en_var_names, english_versions):
                        herb_dict[herb_id][n_e] = v_e.lower()

                herb_id += 1

    # write glossary in a JSON file
    json_glossary = json.dumps(herb_dict, sort_keys=True, indent=4, ensure_ascii=False)
    print(json_glossary)
    with open("../data/herb_glossary.json", "w") as outfile:
        outfile.write(json_glossary)


get_dict_from_herb_glossary("../data/trilingual_herb_glossary_converted.txt")

