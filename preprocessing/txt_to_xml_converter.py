# Script that structures all the TXT files of the corpus to XML.

from lxml import etree
import os
import re
from bs4 import BeautifulSoup
import unicodedata
from nltk import sent_tokenize, word_tokenize


def normalize_structure_txt(filename) -> tuple:
    """
    This function removes annotations and blank lines from the texts of Corpus of Early English Medical Writing.
    :return: Tuple containing the normalized text as a single string, and the encoding of the file.
    """
    lines = ""

    # annotation patterns to be removed
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
                # if encoding is WINDOWS-1252 convert to UTF-8
                line = line.decode('cp1252').encode("utf-8").decode("utf-8")

            # if line is not empty
            if len(line.strip()):

                # search for page pattern in the line, indicated by the annotation |P_x, e.g. |P_12
                page_pattern = re.search(r"\|P_\w*", line)

                for old, new in replacements:
                    line = re.sub(old, new, line)

                # remove full stops surrounding single words on both ends, e.g. .herbe.
                match = re.findall(r"\.\w+\.", line)

                if match:
                    for i in match:
                        line = re.sub(i, i.strip("."), line)
                elif page_pattern:
                    line = line.replace("|", "")

                lines += line
            else:
                pass

    return lines, encoding


def get_meta_corpus1():
    """
    This function collects the meta-information (author, title, year, volume, pages) for all texts included in the
    first sub-corpus (MEMT), using the corresponding *_info_converted.txt files that contain the meta-data for each
    text.
    :return: A dictionary where the keys are the filenames of the XML files that will be afterwards generated, and the
    values are tuples that contain the meta-information per text in the form (author, title, year, volume, pages)
    """
    meta_dict = {}
    # Important: for space efficiency reasons this directory is not included in the main directory of the thesis
    for root, dirs, files in os.walk("../../MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/01_MEMT_Texts", topdown=False):
        for name in files:
            # if file is the info file
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
    """
    This function collects the meta-information (author, title, year, volume, pages) for all texts included in the
    second sub-corpus (EMEMT), using regular expressions on the corresponding filenames that contain the meta-data
    for each text.
    :return: A dictionary where the keys are the filenames of the XML files that will be afterwards generated, and the
    values are tuples that contain the meta-information per text in the form (author, title, year, volume, pages)
    """
    meta_dict = {}
    # Important: for space efficiency reasons this directory is not included in the main directory of the thesis
    for root, dirs, files in os.walk("../../MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/02_EMEMT_Corpus", topdown=False):
        for name in files:
            infile = os.path.join(root, name)

            # process differently Category 6 filenames that have the form year_philosophicaltransactionsvolume_pages
            if root.endswith(" 6"):
                title = "Philosophical Transactions"
                author = "-"
                year, volume, pages = name.rstrip(".txt").split("_")
            else:
                # rest of the filenames have form year_author_title or year_title

                # year_author_title
                volume = "-"
                pages = "-"
                full_match = re.match("(\d+)_(\w+)_(\w+)", name)
                half_match = re.match("(\d+)_(\w+)", name)
                if full_match is not None:
                    year = full_match.group(1)
                    author = full_match.group(2)
                    title = " ".join(re.findall('[A-Z][^A-Z]*', full_match.group(3)))

                # year_title
                else:
                    year = half_match.group(1)
                    author = "-"
                    title = " ".join(re.findall('[A-Z][^A-Z]*', half_match.group(2)))

            meta_dict[name.replace(".txt", ".xml")] = (author, title, year, volume, pages)

    return meta_dict


def get_meta_corpus3():
    """
    This function collects the meta-information (author, title, year, volume, pages) for all texts included in the
    third sub-corpus (LMEMT), using the corresponding nodes from the TEI XML files that came with the corpus. The only
    exception is that the year information is extracted by the filename.
    :return: A dictionary where the keys are the filenames of the XML files that will be afterwards generated, and the
    values are tuples that contain the meta-information per text in the form (author, title, year, volume, pages)
    """
    # tei = "{http://www.tei-c.org/ns/1.0}"

    meta_dict = {}

    # Important: for space efficiency reasons this directory is not included in the main directory of the thesis
    for root, dirs, files in os.walk("../../03_LMEMT_digital", topdown=False):
        for name in files:
            infile = os.path.join(root, name)
            tree = etree.parse(infile)
            with open(infile, "r", encoding="utf-8") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'xml')
                source = soup.find('sourceDesc')

                # get author information
                if source.find("persName") is not None:
                    author = source.find("persName").get_text()
                if author == "Unknown":
                    author = "-"

                # get title information
                if source.find("title") is not None:
                    title = source.find("title").get_text().replace("\n", " ")
                    title = ' '.join(title.split())
                else:
                    title = "-"

                # get volume information
                if source.find("biblScope", unit="vol") is not None:
                    volume = source.find("biblScope", unit="vol").get_text()
                else:
                    volume = "-"

                # get page information
                if source.find("biblScope", unit="page") is not None:
                    pages = source.find("biblScope", unit="page").get_text()
                else:
                    pages = "-"

                # get year information from the filename
                year = name.partition("_")[0]

            # fix encoding in order to have right name in dictionary
            name = unicodedata.normalize("NFC", name)
            meta_dict[name] = (author, title, year, volume, pages)

    return meta_dict


def meta_info_dict():
    """
    This function merges all three meta-information dictionaries into one dictionary.
    :return: A dictionary where the keys are the filenames of the XML files that will be afterwards generated, and the
    values are tuples that contain the meta-information per text in the form (author, title, year, volume, pages)
    """
    meta_dict = {**get_meta_corpus1(), **get_meta_corpus2(), **get_meta_corpus3()}
    return meta_dict


def text_to_xml():
    """
    This function converts every TXT file of the Corpus of Early English Medical Writing into XML by applying
    sentence segmentation and tokenization. The meta information collected from each file is also inserted in the XML.
    """
    # get meta information dict
    meta_dict = meta_info_dict()
    print(meta_dict)

    total_token_counter = 0
    token_counter = 0
    total_unique_tokens = set()
    unique_tokens = set()
    sentence_counter = 0
    token_in_sent_counter= 0

    # Important: for space efficiency reasons this directory is not included in the main directory of the thesis
    for root, dirs, files in os.walk("../../MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy", topdown=False):
        for name in files:
            infile = os.path.join(root, name)

            # get processed text in string and its encoding
            normalized_text, encoding = normalize_structure_txt(infile)

            # convert to xml

            # ignore info files from the MEMT subcorpus
            if not name.endswith("_info_converted.txt"):

                # open new xml file for writing and preserve the original filename
                newfile = infile.replace(".txt", ".xml")
                with open(newfile, "w") as outfile:

                    # apply sentence segmentation
                    sentences = sent_tokenize(normalized_text)

                    # create header node and add the meta information
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

                    new_name = name.replace("txt", "xml")
                    new_name =unicodedata.normalize("NFC", new_name)

                    print(f"SEARCHING FOR: {new_name} ")
                    if new_name in meta_dict.keys():
                        author.text, title.text, year.text, volume.text, pages.text = meta_dict[new_name]

                    # create root of XML
                    content = etree.Element("content")
                    tree_root.append(content)

                    for sent in sentences:

                        # apply tokenization
                        tokens_sent = word_tokenize(sent)

                        page_pattern1 = re.search(r"P_\w*", tokens_sent[0])
                        if len(tokens_sent) == 1 and page_pattern1:
                            page = etree.Element("page")
                            page.text = page_pattern1.group()
                            content.append(page)
                        else:
                            sentence_counter += 1

                            # add sentence tag and sentence id
                            sent_id = f"s{sentence_counter}"
                            sentence = etree.Element("sentence", id=sent_id)

                            content.append(sentence)

                            for sent_token in tokens_sent:

                                # if token is not space characters only
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

                                            # add token id
                                            token_id = f"s{sentence_counter}t{token_in_sent_counter}"
                                            token = etree.Element("token", id=token_id)

                                            sentence.append(token)
                                            token.text = sent_token

                            token_in_sent_counter = 0
                    sentence_counter = 0

                    # write XML file
                    xml_bytes = etree.tostring(tree_root, encoding=encoding, xml_declaration=True, pretty_print=True)
                    xml_str = xml_bytes.decode(encoding)
                    outfile.write(xml_str)
                    print("File is written.")

        token_counter = 0
        unique_tokens.clear()


def main():
    text_to_xml()


if __name__ == "__main__":
    main()
