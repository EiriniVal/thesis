# Author: Eirini Valkana
# !/usr/bin/python

from lxml import etree
import os
import re
# import stanza
from bs4 import BeautifulSoup
import unicodedata
from nltk import sent_tokenize, word_tokenize

# # stanza.download('en')
# nlp = stanza.Pipeline(lang='en', processors='tokenize')


def normalize_structure_txt(filename) -> tuple:
    """
    function that removes annotations from the Middle Modern English Medical Corpus
    :return: tuple containing the normalized text as a string, and the encoding of the file
    """
    # counter = 0
    lines = ""
    # patterns that denote annotations by the transcribers
    replacements = [
        (r"\s\n", " "),
        (r"\[}|}]", ""),
        (r"\[{|{]", ""),
        (r"\[\\.+\\]", ""),
        (r"\[/.+/]", ""),
        (r"\[\^.+\^]", "")]
    with open(filename, "rb") as infile:
        encoding = "utf-8"
        for line in infile:
            # catch Unicode Decode Error
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                # print(line)
                line = line.decode('cp1252').encode("utf-8").decode("utf-8")
            # if line is not empty
            if len(line.strip()):
                page_pattern = re.search(r"\|P_\w*", line)
                # print(line, "The line is not empty")
                for old, new in replacements:
                    line = re.sub(old, new, line)
                # fix words like .herbe.
                match = re.findall(r"\.\w+\.", line)
                if match:
                    for i in match:
                        line = re.sub(i, i.strip("."), line)
                # if there is page info remove the | so that tokenization is smooth later on
                elif page_pattern:
                    line = line.replace("|", "")

                lines += line

            else:
                # print(line,"The line is empty")
                pass

    return lines, encoding


# CREATE DICTIONARIES FOR EACH OF THE CORPORA: KEY WILL BE THE NAME OF THE XML FILE WHICH WILL BE GENERATED AND VALUE WILL BE A TUPLE WITH THE META INFORMATION
# THE KEY AKA THE FILE NAME IS NEEDED IN ORDER TO MAP THE META INFORMATION TO THE CORRECT XML FILES IN A SECOND STEP


def get_meta_corpus1():
    meta_dict = {}
    for root, dirs, files in os.walk("../../MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/01_MEMT_Texts", topdown=False):
        for name in files:
            # if file is info file
            if name.endswith("_info_converted.txt"):
                infile = os.path.join(root, name)
                # look at the first line where the author and the title is included and separated by a comma
                with open(infile, "r") as f:
                    first_line = f.readline()
                    # if there is a comma and subsequently an author
                    if ", " in first_line:
                        # get author and title
                        author = first_line.split(", ")[0]
                        title = first_line.split(", ")[1].rstrip("\n")
                        year = "-"
                        volume = "-"
                        pages = "-"
                    else:
                        title = first_line.rstrip("\n")
                        author = "-"
                        year = "-"
                        volume = "-"
                        pages = "-"

                    # get name of xml file to be the key of the dict and have a mapping later
                    meta_dict[name.replace("_info_converted.txt", "_converted.xml")] = (author, title, year, volume, pages)

    return meta_dict



def get_meta_corpus2():
    meta_dict = {}
    for root, dirs, files in os.walk("../../MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/02_EMEMT_Corpus", topdown=False):
        for name in files:
            infile = os.path.join(root, name)
            # process differently category 6 files
            if root.endswith(" 6"):
                # year_philosophicaltransactionsvolume_pages
                title = "Philosophical Transactions"
                author = "-"
                year, volume, pages = name.rstrip(".txt").split("_")
            else:
                # year_author_title
                volume = "-"
                pages = "-"
                full_match = re.match("(\d+)_(\w+)_(\w+)", name)
                half_match = re.match("(\d+)_(\w+)", name)
                if full_match is not None:
                    year = full_match.group(1)
                    author = full_match.group(2)
                    title = " ".join(re.findall('[A-Z][^A-Z]*', full_match.group(3)))
                # OR year_title
                else:
                    year = half_match.group(1)
                    author = "-"
                    title = " ".join(re.findall('[A-Z][^A-Z]*', half_match.group(2)))

            meta_dict[name.replace(".txt", ".xml")] = (author, title, year, volume, pages)

    return meta_dict


# TODO get metadata for LMEMT from TEI xmls
def get_meta_corpus3():
    tei = "{http://www.tei-c.org/ns/1.0}"
    meta_dict = {}
    for root, dirs, files in os.walk("../../03_LMEMT_digital", topdown=False):
        for name in files:
            infile = os.path.join(root, name)
            # print(infile)
            tree = etree.parse(infile)
            with open(infile, "r", encoding="utf-8") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'xml')
                source = soup.find('sourceDesc')
                if source.find("persName") is not None:
                    author = source.find("persName").get_text()
                if author == "Unknown":
                    author = "-"
                if source.find("title") is not None:
                    title = source.find("title").get_text().replace("\n", " ")
                    title = ' '.join(title.split())
                else:
                    title = "-"
                # if source.find("date") is not None:
                #     year = source.find("date").get_text()
                # elif source.find("date") == "":
                #     year = name.partition("_")[0]
                # else:
                #     year = "-"
                # < biblScope unit = "vol" > 1 < / biblScope >
                # < biblScope unit = "page" > 81 < / biblScope >
                if source.find("biblScope", unit="vol") is not None:
                    volume = source.find("biblScope", unit="vol").get_text()
                else:
                    volume = "-"
                if source.find("biblScope", unit="page") is not None:
                    pages = source.find("biblScope", unit="page").get_text()
                else:
                    pages = "-"
                # get year info from filename
                year = name.partition("_")[0]
            # TODO fix encoding in order to have right name in dictionary
            name = unicodedata.normalize("NFC", name)
            meta_dict[name] = (author, title, year, volume, pages)
    return meta_dict


def meta_info_dict():
    meta_dict = {**get_meta_corpus1(), **get_meta_corpus2(), **get_meta_corpus3()}
    return meta_dict

# CONVERT TXT FILES TO XML AND ADD HEADER NODE WITH METADATA INFO
# TODO add these metadata in the header node of the xml tree (merge three dicts ?)


def text_to_xml():
    """
    function that converts every txt file in the Middle English Medical Corpus directory into xml by applying
    sentence segmentation and tokenization. The function also prints the counts of tokens and types a) per text and
    b) total

    :return:
    """
    # get meta information dict
    meta_dict = meta_info_dict()
    print(meta_dict)
    yogh = ""
    total_token_counter = 0
    token_counter = 0
    total_unique_tokens = set()
    unique_tokens = set()
    sentence_counter = 0
    token_in_sent_counter= 0
    # real corpus: "./MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy"
    for root, dirs, files in os.walk("../../MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy", topdown=False):
        # print(root,dirs)
        for name in files:
            infile = os.path.join(root, name)
            # print(infile)
            # get processed file and encoding (tuple)
            normalized_text, encoding = normalize_structure_txt(infile)

            # convert to xml
            # do not open info files from MEMT(1)
            if not name.endswith("_info_converted.txt"):
                # open new xml file for writing and maintain the original name
                newfile = infile.replace(".txt", ".xml")
                with open(newfile, "w") as outfile:

                    sentences = sent_tokenize(normalized_text)
                    # create header of tree for meta information
                    tree_root = etree.Element("text")

                    tree_header = etree.Element("header")
                    tree_root.append(tree_header)

                    author = etree.Element("author")
                    title = etree.Element("title")
                    year = etree.Element("year")
                    volume = etree.Element("volume")
                    pages = etree.Element("pages")
                    tree_header.append(author)
                    tree_header.append(title)
                    tree_header.append(year)
                    tree_header.append(volume)
                    tree_header.append(pages)

                    # this is wrong it removes t from end of filename e.g. 1777_GEN_Aitken_MedicalImprovemen.xml
                    # 1777_GEN_Aitken_MedicalImprovement.xml
                    new_name = name.replace("txt", "xml")
                    new_name =unicodedata.normalize("NFC", new_name)
                    print(f"SEARCH FOR: {new_name} ")
                    if new_name in meta_dict.keys():
                        print(new_name)
                        author.text, title.text, year.text, volume.text, pages.text = meta_dict[new_name]

                    # create root of tree for the whole text
                    content = etree.Element("content")
                    tree_root.append(content)

                    for sent in sentences:
                        tokens_sent = word_tokenize(sent)
                        # TODO
                        page_pattern1 = re.search(r"P_\w*", tokens_sent[0])
                        # if sentence has one token and this token is page info
                        if len(tokens_sent) == 1 and page_pattern1:
                            page = etree.Element("page")
                            page.text = page_pattern1.group()
                            content.append(page)
                        else:
                            sentence_counter += 1
                            # add sentence tag and sentence id
                            sent_id = f"s{sentence_counter}"
                            sentence = etree.Element("sentence", id=sent_id)
                            # print(sent)
                            content.append(sentence)

                            for sent_token in tokens_sent:
                                # if token is NOT space characters only
                                if not sent_token.isspace():
                                        page_pattern = re.search(r"P_\w*", sent_token)
                                        # if there is page info
                                        if page_pattern:
                                            page = etree.Element("page")
                                            page.text = page_pattern.group()
                                            sentence.append(page)
                                        else:
                                            token_counter += 1
                                            token_in_sent_counter += 1
                                            total_token_counter += 1
                                            unique_tokens.add(sent_token)
                                            total_unique_tokens.add(sent_token)

                                            # add token ids
                                            token_id = f"s{sentence_counter}t{token_in_sent_counter}"
                                            token = etree.Element("token", id=token_id)

                                            sentence.append(token)
                                            token.text = sent_token

                            token_in_sent_counter = 0
                    sentence_counter = 0

                    xml_bytes = etree.tostring(tree_root, encoding=encoding, xml_declaration=True, pretty_print=True)
                    xml_str = xml_bytes.decode(encoding)
                    outfile.write(xml_str)
                    print("file is written")


                # print(f"number of tokens in {root}: {token_counter}")
        # print(f"number of types{root}: {len(unique_tokens)}")
        token_counter = 0
        unique_tokens.clear()

    # print(f"total number of tokens: {total_token_counter}")
    # print(f"total number of types: {len(total_unique_tokens)}")


def main():
    text_to_xml()


if __name__ == "__main__":
    main()
