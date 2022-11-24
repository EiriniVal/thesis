# Script that detects intra-sentential Latin code-switches within the sentences that were labeled as English from the
# two language models, and within those which remained unlabeled

import xml.etree.ElementTree as ET
from create_lexicon import get_lexica_with_bible
from itertools import groupby
from operator import itemgetter
import json
from collections import defaultdict

# get filtered lexica for English and Latin
en_filtered, la_filtered = get_lexica_with_bible()


def get_latin_herbs():
    """
    This function extracts all the Latin entries from the Trilingual Herb Glossary.
    :return: a set of the herb names
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


def identify_lang(token):
    """
    This function identifies the language of a token by using lexicon lookup.
    :param token: the token to be labeled
    :return: the language code, namely EN for English, LA for Latin, and UNK for unknown
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
    This functions resolves the unknown tokens based on their context tokens.
    :param input_list: A list of tuples representing the indices and the language codes of the tokens composing a
    sentence.
    :return: A new list of tuples representing the indices and the new language codes of the tokens composing a
    sentence.
    """
    new_list = []
    for index, elem in enumerate(input_list):

        if elem[1] == 'UNK':

            # if UNK token at the beginning of sentence get language of next token
            if index == 0 and index+1 <= (len(input_list)-1):
                new_elem = (elem[0], input_list[index+1][1])
                new_list.append(new_elem)

            # if UNK token at the end of the sentences get language of previous token
            elif index == len(input_list)-1:
                new_elem = (elem[0], input_list[index-1][1])
                new_list.append(new_elem)

            # if surrounding tokens of the UNK token are both in Latin get the language of the surrounding tokens
            elif index + 1 <= (len(input_list) - 1) and input_list[index-1][1] == input_list[index+1][1]:
                if input_list[index-1][1] == "LA":
                    new_elem = (elem[0], input_list[index-1][1])
                    new_list.append(new_elem)

                # leave UNK tokens surrounded by EN AND UNK on both ends unresolved
                else:
                    new_list.append(elem)
            else:
                new_list.append(elem)

        else:
            new_list.append(elem)

    return new_list


def detect_la_cs_in_sent(sentence):
    """
    This function detects all the Latin intra-sentential code-switching entities found inside a sentence.
    If at least two adjacent tokens are in LA, then they constitute a code-switch. However, if a token identified
    as Latin has not adjacent Latin tokens but it is included in the Trilingual Herb Glossary, it is also counted
    as a code-switch.
    :param sentence: the sentence to be searched for Latin intra-sentential code-switches
    :return: tuple containing a list of lists with the detected intra-sentential code-switching spans,
    and a list with the indices and language labels of all the tokens within a sentence.
    """
    herb_indices = []
    cs_sequences_per_sentence = []
    possible_cs = []
    ids_langs_dict = {}
    if ET.iselement(sentence):
        for element in sentence.iter():
            if element.tag == "token":
                token_id = element.get("id")
                # if a Latin token is a herb
                if element.get("lang_id") == "LA":
                    ids_langs_dict[token_id] = "LA"
                    herb_indices.append(token_id)
                else:
                    token_lang = identify_lang(element.text)
                    ids_langs_dict[token_id] = token_lang
    else:
        token_id = 1
        for token in sentence.split():
            if token.lower() in latin_herbs_set:
                token_lang = "LA"
                herb_indices.append(token_id)
            else:
                token_lang = identify_lang(token)
            ids_langs_dict[token_id] = token_lang
            token_id += 1

    # the language tags for each token
    mylist = list(ids_langs_dict.items())
    # [(0, 'EN'), (1, 'EN'), (2, 'EN'), (3, 'EN'), (4, 'EN'), (5, 'LA'), (6, 'LA'), (7, 'LA'), (8, 'LA'), ...]

    # resolve unknown tokens
    mylist = resolve_unk(mylist)

    la_indices_list = []

    for index, element in enumerate(mylist):

        if element[1] == "LA":
            la_indices_list.append(index)

    # get the indices of possible intra-sentential code-switches
    # e.g. [[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [17, 18, 19]]
    for k, g in groupby(enumerate(la_indices_list), lambda ix: ix[0] - ix[1]):
        l = list(map(itemgetter(1), g))
        possible_cs.append(l)

    for element in possible_cs:
        # if the span of the possible code-switch is at least two tokens
        if len(element) >= 2:
            # save the starting and ending indices of the code-switches
            # e.g [[(5, 'LA'), (15, 'LA')], [(17, 'LA'), (19, 'LA')]]
            cs_sequence = [mylist[element[0]], mylist[element[-1]]]
            cs_sequences_per_sentence.append(cs_sequence)

        # if the span of the possible code-switch is only 1 token
        elif len(element) == 1:
            # only consider it if it is a Latin herb
            if element[0]+1 in herb_indices:
                cs_sequences_per_sentence.append([mylist[element[0]], mylist[element[0]]])

    return cs_sequences_per_sentence, mylist


def get_cs_sentences(infile_path, outfile_name):
    """
    This functions returns the results of the intra-sentential code-switching detection on a given file.
    :param infile_path: the file with one sentence per line on which the code-switching detection will be performed
    :param outfile_name: the filename of the output txt file with tab separated information
    :return:
    """
    results_dict = defaultdict(dict)
    sent_id_dict = defaultdict(dict)
    with open(outfile_name, "w", encoding="utf-8") as out1:
        with open(infile_path, "r") as infile:
            for line in infile:
                if len(line.split("\t")) == 3:
                    origin_file, sent_id, sentence = line.strip("\n").split("\t")
                cs_list, lang_id_list = detect_la_cs_in_sent(sentence)
                if len(cs_list) >= 1:
                    print(f"Code-switch detected in {origin_file}: \n "
                          f"\t sentence id: {sent_id}")
                    out1.write(f"Code-switch detected in {origin_file}:\n")
                    out1.write(f"\t sentence id: {sent_id}\n")
                    for cs in cs_list:
                        print(f"\t span: {cs[0][0]} - {cs[1][0]}\n\n")
                        out1.write(f"\t span: {cs[0][0]} - {cs[1][0]}\n\n")
                    # out1.write(origin_file + "\t" + sent_id + "\t" + str(cs_list) + "\t" + sentence + "\n")
                    info_dict = {"sentence": sentence, "lang_id_list": lang_id_list, "cs_span": cs_list}
                    sent_id_dict[sent_id] = info_dict
                    results_dict[origin_file] = sent_id_dict
                else:
                    continue


def main():
    get_cs_sentences("./sent_labeled_en.txt", "intra_sent_cs_results_in_en_sentences.txt")
    get_cs_sentences("./sent_unlabeled.txt", "intra_sent_cs_results_in_unk_sentences.txt")


if __name__ == "__main__":
    main()
