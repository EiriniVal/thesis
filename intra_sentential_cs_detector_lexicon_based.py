# Author: Eirini Valkana
# search for intra-sentential Latin code-switches inside the English sentences file (agree_sent_en.txt)

import xml.etree.ElementTree as ET
from create_lexicon import get_lexica_with_bible
from itertools import groupby
from operator import itemgetter
import json

en_filtered, la_filtered = get_lexica_with_bible()


def get_latin_herbs():
    """
    get all Latin herb names in a set
    :return:
    """
    latin_herbs = set()
    with open("./data/herb_glossary.json", "r") as infile:
        herbs_dict = json.load(infile)
    for herb_id, language_versions in herbs_dict.items():
        for lang, herb_name in language_versions.items():
            if "Latin" in lang:
                latin_herbs.add(herb_name)
    return latin_herbs


latin_herbs_set = get_latin_herbs()
print(latin_herbs_set)


def identify_lang(token):
    """
    identify the language of a token based on the two vocabularies created.
    :param token:
    :return:
    """
    if token.lower() in en_filtered.keys():
        lang_id = "EN"
    elif token.lower() in la_filtered.keys():
        lang_id = "LA"
    else:
        lang_id = "UNK"
    return lang_id


def resolve_unk(input_list: list):
    """

    :param input_list: A list of tuples representing the indices and the language code of the token of a sentence.
    as values.
    :return: A dict with UNK elements resolved. (if possible)
    """
    new_list = []
    for index, elem in enumerate(input_list):
        # print(index, elem)
        if elem[1] == 'UNK':
            # print(index)
            # if index == 0 get language of next token
            if index == 0 and index+1 <= (len(input_list)-1):
                new_elem = (elem[0], input_list[index+1][1])
                new_list.append(new_elem)

            # if index == len(list)-1 get language of previous token
            elif index == len(input_list)-1:
                new_elem = (elem[0], input_list[index-1][1])
                new_list.append(new_elem)

            # if surrounding tokens have the same language EXCEPT UNK get the language of the surrounding tokens
            elif index + 1 <= (len(input_list) - 1) and input_list[index-1][1] == input_list[index+1][1]:
                if input_list[index-1][1] != "UNK":
                    new_elem = (elem[0], input_list[index-1][1])
                    new_list.append(new_elem)
                # unresolved
                else:
                    new_list.append(elem)
            else:
                # unresolved
                new_list.append(elem)

        else:
            new_list.append(elem)

    return new_list


def detect_la_cs_in_en_sent(en_sentence):
    """
    Function that returns all the Latin intra-sentential code-switches found inside an english sentence.
    The smallest span of Latin tokens that can constitute a code-switch is two tokens.
    However, if a single token identified as Latin is contained in the latin herb names glossary, it is also counted
    as a code-switch.
    :param en_sentence: the sentence string
    :return: a list of lists containing the spans of code-switches within the sentences in the form of tuples
    """
    # tok1, tok2, tok3:
    herb_indices = []
    cs_sequences_per_sentence = []
    possible_cs = []
    ids_langs_dict = {}
    if ET.iselement(en_sentence):
        for element in en_sentence.iter():
            if element.tag == "token":
                token_id = element.get("id")
                # if token is a herb and has already a LA language tag
                if element.get("lang_id") == "LA":
                    ids_langs_dict[token_id] = "LA"
                    herb_indices.append(token_id)
                else:
                    token_lang = identify_lang(element.text)
                    ids_langs_dict[token_id] = token_lang
    else:
        token_id = 1
        for token in en_sentence.split():
            if token.lower() in latin_herbs_set:
                # print("HERB:", token, token_id)
                token_lang = "LA"
                herb_indices.append(token_id)
            else:
                token_lang = identify_lang(token)
            ids_langs_dict[token_id] = token_lang
            token_id += 1

    # print("HERB INDICES", herb_indices)
    mylist = list(ids_langs_dict.items())  # the language tags for each token
    # [(0, 'EN'), (1, 'EN'), (2, 'EN'), (3, 'EN'), (4, 'EN'), (5, 'LA'), (6, 'LA'), (7, 'LA'), (8, 'LA'), ...]
    # print(mylist)

    # RESOLVE UNK
    mylist = resolve_unk(mylist)

    # enumerated_dict = enumerate(mydict.items())
    # # print(enumerated_dict)
    la_indices_list = []

    for index, element in enumerate(mylist):
        # print(element)
        #
        if element[1] == "LA":
            la_indices_list.append(index)

    for k, g in groupby(enumerate(la_indices_list), lambda ix: ix[0] - ix[1]):
        l = list(map(itemgetter(1), g))
        possible_cs.append(l)

    # print("POSSIBLE CS", possible_cs)  # e.g. [[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [17, 18, 19]]

    for element in possible_cs:
        if len(element) >= 2:
            # print(element)  # true cs
            cs_sequence = [mylist[element[0]], mylist[element[-1]]]  # [(5, 'LA'), (6, 'LA'), (7, 'LA'), (8, 'LA'),
            # (9, 'LA'), (10, 'LA'), (11, 'LA'), (12, 'LA'), (13, 'LA'), (14, 'LA'), (15, 'LA')]
            cs_sequences_per_sentence.append(cs_sequence)
        elif len(element) == 1:
            # TODO explain +1
            if element[0]+1 in herb_indices:
                cs_sequences_per_sentence.append([mylist[element[0]], mylist[element[0]]])



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
                if len(cs_list) >= 1:
                    print(f" Code-switch detected in {origin_file}: \n "
                          f"\t sentence id: {sent_id}")
                    for cs in cs_list:
                        print(f"\t span: {cs[0][0]} - {cs[1][0]}\n\n")
                    out.write(origin_file + "\t" + sent_id + "\t" + str(cs_list) + "\t" + sentence + "\n")
                else:
                    continue


def main():
    get_cs_sentences("agree_sent_en.txt", "cs_detection_results_in_en_sentences_with_herbs_unk_resolved.txt")


main()
