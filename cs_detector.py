# Author: Eirini Valkana
# script that detects code_switches by applying a language identifier model on the token level

from xml.etree import ElementTree as ET
import os
from bs4 import BeautifulSoup
import unicodedata
from my_utils.util import train_furl_model, open_read_lines


def get_root_content(input_file) -> ET.Element:
    """
    Get root and content tag of an xml file.
    :param input_file:
    :return:
    """
    with open(input_file, "r") as infile:
        tree = ET.parse(infile)
        root = tree.getroot()

        # get content tag
        content = root.find("content")  # 'xml.etree.ElementTree.Element'

    return root, content


def get_sentences(content_element: ET.Element) -> ET.Element:
    """
    Get all sentence tags from content.
    :param content_element:
    :return:
    """
    for child in content_element:
        if child.tag == "sentence":
            yield child


def get_tokens(sentence_element: ET.Element) -> ET.Element:
    """
    Get all token tags of a sentence.
    :param sentence_element:
    :return:
    """
    for child in sentence_element:
        if child.tag == "token":
            yield child


def generate_sent(sent_xml_elem: ET.Element):
    """
    Gets xml tag sentence and merges all the token tags to regenerate the sentence
    :return:
    """
    # contents = f.read()
    # soup = BeautifulSoup(contents, 'xml')
    # source = soup.find('sourceDesc')
    pass


def write_cs_attrib_token(token_element: ET.Element) -> ET.Element:
    token_element.set('cs', 'yes')
    return token_element



def write_cs_attrib_sent():
    pass


def main():
    # TODO change model to the most efficient one
    # for now use Furl
    en_train = open_read_lines("models/EN.txt")
    la_train = open_read_lines("models/LA.txt")
    furl_identifier = train_furl_model(en_train, la_train)

    # get directory of files (no funct)
    for root, dirs, files in os.walk("toy_corpus", topdown=False):
        # print(root,dirs)
        # for file in directory (no funct)
        for name in files:
            infile = os.path.join(root, name)
            tree_root, content = get_root_content(infile)  # get root and content tags
            # generator # for sentence in content (no funct)
            for sentence in get_sentences(content):

                # TOKEN LEVEL CS
                for token in get_tokens(sentence):
                    # spaces added around token for better ngram results
                    token_label = furl_identifier.identify(" "+token.text+" ")  # tuple (label, perplexities dict)
                    # print(f'{token.text}: {token_label}')
                    if token_label[0] == "LA":
                        token = write_cs_attrib_token(token)
                    # print(type(token))

            # update xml files with info related to code_switching
            f = open(f'{infile.replace(".xml", "_cs.xml")}', 'wb')
            # ET.indent(root)
            f.write(ET.tostring(tree_root, encoding='utf-8', xml_declaration=True))
            f.close()


    # save tokens and generate_sent (generate_sent())
    # sentence_level_cs (apply_lang_model, write_cs_attrib_sent())
    # save new xml 


if __name__ == '__main__':
    main()
