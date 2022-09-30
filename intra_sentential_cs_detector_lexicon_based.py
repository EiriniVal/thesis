# Author: Eirini Valkana
# search for Latin code-switches in English sentences file (agree_sent_en.txt)
import xml.etree.ElementTree
from create_lexicon import get_lexica
from itertools import groupby
from operator import itemgetter

en_filtered, la_filtered = get_lexica()


def identify_lang(token):
    if token in en_filtered.keys():
        lang_id = "EN"
    elif token in la_filtered.keys():
        lang_id = "LA"
    else:
        lang_id = "UNK"
    return lang_id


def get_sentences_from_xml_files():
    pass


def detect_la_cs_in_en_sent(en_sentence: xml.etree.ElementTree.Element):
    # tok1, tok2, tok3:
    ids_langs_dict = {}
    for element in en_sentence.iter():
        if element.tag == "token":
            token_id = element.get("id")
            token_lang = identify_lang(element.text)
            ids_langs_dict[token_id] = token_lang

    mylist = list(ids_langs_dict.items())
    print(mylist)

    # enumerated_dict = enumerate(mydict.items())
    # # print(enumerated_dict)
    la_indices_list = []

    for index, element in enumerate(mylist):
        print(element)
        if element[1] == "LA":
            la_indices_list.append(index)

    possible_cs = []
    for k, g in groupby(enumerate(la_indices_list), lambda ix: ix[0] - ix[1]):
        l = list(map(itemgetter(1), g))
        possible_cs.append(l)

    print(possible_cs)

    for element in possible_cs:
        if len(element) >= 2:
            print(element)  # true cs
            cs_sequence = mylist[element[0]: element[-1] + 1]










