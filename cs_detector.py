# Author: Eirini Valkana
# script that detects code_switches by applying a language identifier model on the token level

from xml.etree import ElementTree as ET
import os
from bs4 import BeautifulSoup
import unicodedata


def get_content(input_file):
    """
    Get content tag of an xml file.
    :param input_file:
    :return:
    """
    with open(input_file, "r") as infile:
        tree = ET.parse(infile)
        root = tree.getroot()

        # get content tag
        content = root.find("content")  # 'xml.etree.ElementTree.Element'

    return content


def generate_sent(sent_xml_elem: etree):
    """
    Gets xml tag sentence and merges all the token tags to regenerate the sentence
    :return:
    """
    # contents = f.read()
    # soup = BeautifulSoup(contents, 'xml')
    # source = soup.find('sourceDesc')
    token_tags = sent_xml_elem.xpa


def apply_lang_model():
    pass


def write_cs_attrib_token():
    pass


def write_cs_attrib_sent():
    pass


def main():
    for root, dirs, files in os.walk("../MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy", topdown=False):
        # print(root,dirs)
        for name in files:
            pass
    # get directory of files (no funct)
    # for file in directory (no funct)
    # get_content()
    # for sentence in content (no funct)
    # for token in sentence (no funct)
    # token_level_cs (apply_lang_model, write_cs_attrib_token)
    # save tokens and generate_sent (generate_sent())
    # sentence_level_cs (apply_lang_model, write_cs_attrib_sent())
    # save new xml 
    pass


get_content("testing.xml")
