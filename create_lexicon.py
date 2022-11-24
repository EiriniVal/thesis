# Script to generate lexica with types and frequencies for both languages language.

import collections
from urllib.request import urlopen
import xml.etree.ElementTree as ET


def parse_extra_latin_xml_file(input_url, xml_element_for_sentences, outfile_name):
    """
    This functions extracts the sentences from the Latin Bible XML file and adds them to a TXT file.
    :param input_url: url to the xml
    :param xml_element_for_sentences: the name of the xml node corresponding to sentences
    :param outfile_name: the name of the output file
    :return: the name of the output file
    """
    with open(outfile_name, "w", encoding="utf-8") as out:
        with urlopen(input_url) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for element in root.iter():
                if element.tag == xml_element_for_sentences:
                    out.write(element.text+"\n")
    return outfile_name


def get_types_freq_dict(*input_files):
    """
    This function generates a lexicon given some input files.
    :param input_files: the input files containing one sentence per line
    :return: dictionary with keys being the types and values being the corresponding counts
    """
    tokens_total = []
    for file in input_files:
        with open(file, "r") as infile:
            for line in infile:
                if len(line.split("\t")) == 3:
                    filename, sent_id, sent = line.split("\t")
                else:
                    sent = line
                # lower case before adding to lexicon
                tokens = sent.lower().strip().split(" ")
                tokens_total += tokens
    vocab_dict = dict(collections.Counter(tokens_total))
    vocab_dict = dict(sorted(vocab_dict.items(), key=lambda item: item[1], reverse=True))
    try:
        vocab_dict.pop('')
    except KeyError:
        print(f'Key to be deleted is not in the dictionary')
    return vocab_dict


def filter_lexicon(dict_to_filter, comp_dict, freq_difference):
    """
    This function filters a lexicon using the following techniques:
    a) if a type only occurs in lexicon A, it is preserved
    b) if a type of lexicon A occurs also in lexicon B
        - it is preserved if its counts in lexicon A are at least "n" times higher than the counts in lexicon B
        - else the type is removed

    :param dict_to_filter: the lexicon in language A to be filtered
    :param comp_dict: the lexicon in language B, which will be used in comparison
    :param freq_difference: "n"
    :return:
    """
    new_dict = {}
    for key, value in dict_to_filter.items():
        if key not in comp_dict:
            new_dict[key] = value
        elif dict_to_filter[key] >= freq_difference * comp_dict[key]:
            new_dict[key] = value

    return new_dict


def get_lexica_with_bible():
    """
    This function generates the filtered lexica for each language.
    :return tuple containing the English filtered lexicon and the Latin filtered lexicon
    """
    en_dict = get_types_freq_dict("./sent_labeled_en.txt")
    la_dict = get_types_freq_dict("./sent_labeled_la.txt", parse_extra_latin_xml_file("https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/Latin.xml", "seg", "latin_bible_sentences.txt"))

    la_filtered = filter_lexicon(la_dict, en_dict, 3)
    en_filtered = filter_lexicon(en_dict, la_dict, 11)

    return en_filtered, la_filtered