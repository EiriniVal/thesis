# Author: Eirini Valkana
# search for Latin code-switches in English sentences file (agree_sent_en.txt)
import xml.etree.ElementTree as ET
from create_lexicon import get_lexica_with_bible
from itertools import groupby
from operator import itemgetter

en_filtered, la_filtered = get_lexica_with_bible()


def identify_lang(token):
    if token.lower() in en_filtered.keys():
        lang_id = "EN"
    elif token.lower() in la_filtered.keys():
        lang_id = "LA"
    else:
        lang_id = "UNK"
    return lang_id


def detect_la_cs_in_en_sent(en_sentence):
    # tok1, tok2, tok3:
    ids_langs_dict = {}
    if ET.iselement(en_sentence):
        for element in en_sentence.iter():
            if element.tag == "token":
                token_id = element.get("id")
                token_lang = identify_lang(element.text)
                ids_langs_dict[token_id] = token_lang
    else:
        token_id = 1
        for token in en_sentence.split():
            token_lang = identify_lang(token)
            ids_langs_dict[token_id] = token_lang
            token_id += 1

    mylist = list(ids_langs_dict.items())  # the language tags for each token
    # [(0, 'EN'), (1, 'EN'), (2, 'EN'), (3, 'EN'), (4, 'EN'), (5, 'LA'), (6, 'LA'), (7, 'LA'), (8, 'LA'), ...]
    # print(mylist)

    # enumerated_dict = enumerate(mydict.items())
    # # print(enumerated_dict)
    la_indices_list = []

    for index, element in enumerate(mylist):
        # print(element)
        if element[1] == "LA":
            la_indices_list.append(index)

    possible_cs = []
    for k, g in groupby(enumerate(la_indices_list), lambda ix: ix[0] - ix[1]):
        l = list(map(itemgetter(1), g))
        possible_cs.append(l)

    # print(possible_cs)  # e.g. [[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [17, 18, 19]]

    cs_sequences_per_sentence = []
    for element in possible_cs:
        if len(element) >= 2:
            # print(element)  # true cs
            cs_sequence = [mylist[element[0]], mylist[element[-1]]]  # [(5, 'LA'), (6, 'LA'), (7, 'LA'), (8, 'LA'),
            # (9, 'LA'), (10, 'LA'), (11, 'LA'), (12, 'LA'), (13, 'LA'), (14, 'LA'), (15, 'LA')]
            cs_sequences_per_sentence.append(cs_sequence)
    # print(cs_sequences_per_sentence)
    # instead of saving the whole sequence save the start and end of the code-switch span
    # instead of [[(5, 'LA'), (6, 'LA'), (7, 'LA'), (8, 'LA'), (9, 'LA'), (10, 'LA'), (11, 'LA'), (12, 'LA'),
    # (13, 'LA'), (14, 'LA'), (15, 'LA')], [(17, 'LA'), (18, 'LA'), (19, 'LA')]]
    # we get: [[(5, 'LA'), (15, 'LA')], [(17, 'LA'), (19, 'LA')]]
    return cs_sequences_per_sentence


def get_sentences_from_xml_files():
    pass


def get_cs_sentences(infile_path, outfile_name):
    with open(outfile_name, "w", encoding="utf-8") as out:
        with open(infile_path, "r") as infile:
            for line in infile:
                if len(line.split("\t")) == 3:
                    origin_file, sent_id, sentence = line.split("\t")
                cs_list = detect_la_cs_in_en_sent(sentence)
                if len(cs_list) >=1:
                    print(f" Code-switch detected in {origin_file}: \n "
                          f"\t sentence id: {sent_id}")
                    for cs in cs_list:
                        print(f"\t span: {cs[0][0]} - {cs[1][0]}\n\n")
                    out.write(origin_file + "\t" + sent_id + "\t" + str(cs_list) + "\n")
                else:
                    continue


def main():
    get_cs_sentences("agree_sent_en.txt", "cs_detection_results_in_en_sentences.txt")


main()


