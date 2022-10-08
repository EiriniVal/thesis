# get vocab with types and frequences from two files generated by sent_lang_identification.py script with the sentences
# Author: Eirini Valkana
import collections
from urllib.request import urlopen
import xml.etree.ElementTree as ET


def parse_extra_latin_xml_file(input_url, xml_element_for_sentences, outfile_name):
    with open(outfile_name, "w", encoding="utf-8") as out:
        with urlopen(input_url) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for element in root.iter():
                if element.tag == xml_element_for_sentences:
                    out.write(element.text+"\n")
    return outfile_name


def get_types_freq_dict(*input_files):
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
    new_dict = {}
    for key, value in dict_to_filter.items():
        # if word (key) only in latin keep it
        if key not in comp_dict:
            new_dict[key] = value
        elif dict_to_filter[key] >= freq_difference * comp_dict[key]:
            # print(key)
            new_dict[key] = value

    # print(new_dict)
    return new_dict


def get_lexica_with_bible():
    en_dict = get_types_freq_dict("./agree_sent_en.txt")
    la_dict = get_types_freq_dict("./agree_sent_la.txt", parse_extra_latin_xml_file("https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/Latin.xml", "seg", "latin_bible_sentences.txt"))
    # print(en_dict)
    # print(la_dict)
    la_filtered = filter_lexicon(la_dict, en_dict, 3)
    # print(la_filtered)
    en_filtered = filter_lexicon(en_dict, la_dict, 11)
    # print(en_filtered)
    print(f"Length of unfiltered lexica:\n EN: {len(en_dict)},\n LA: {len(la_dict)}\n\n Length of filtered lexica:\n "
          f"EN: {len(en_filtered)},\n LA: {len(la_filtered)}")

    return en_filtered, la_filtered
