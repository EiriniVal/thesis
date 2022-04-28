# Author: Eirini Valkana
# !/usr/bin/python

# TODO add attributes for root element: author, title, year
# TODO add ids to tokens: what kind of ids?
# TODO add header for metadata in xmls

from lxml import etree
import os
import re
import stanza

# stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors='tokenize')


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
        (r"\[\\.+\\]", ""),
        (r"\[/.+/]", ""),
        (r"\[\^.+\^]", ""),
        (r"\|P_\d*\s", "")]
    with open(filename, "rb") as infile:
        encoding = "utf-8"
        for line in infile:
            # catch Unicode Decode Error
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                print(line)
                line = line.decode('cp1252').encode("utf-8").decode("utf-8")
            # if line is not empty
            if len(line.strip()):
                # print(line, "The line is not empty")
                for old, new in replacements:
                    line = re.sub(old, new, line)
                lines += line
            else:
                # print(line,"The line is empty")
                pass

    return lines, encoding


def text_to_xml():
    """
    function that converts every txt file in the Middle English Medical Corpus directory into xml by applying
    sentence segmentation and tokenization. The function also prints the counts of tokens and types a) per text and
    b) total

    :return:
    """
    yogh = ""
    total_token_counter = 0
    token_counter = 0
    total_unique_tokens = set()
    unique_tokens = set()
    # real corpus: "./MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy"
    for root, dirs, files in os.walk("./TOY-CORPUS", topdown=False):
        # print(root,dirs)
        for name in files:
            infile = os.path.join(root, name)
            print(infile)
            # get processed file and encoding (tuple)
            normalized_text, encoding = normalize_structure_txt(infile)

            # convert to xml
            # do not open info files from MEMT(1)
            if not name.endswith("_info_converted.txt"):
                # open new xml file for writing and maintain the original name
                with open(f"{infile.rstrip('.txt')}.xml", "w") as outfile:

                    doc = nlp(normalized_text)
                    # create root of tree for the whole text
                    tree_root = etree.Element("text")

                    for sent in doc.sentences:
                        sentence = etree.Element("sentence")
                        # print(sent)
                        tree_root.append(sentence)
                        for sent_token in sent.tokens:
                            # if token is NOT space characters only
                            if not sent_token.text.isspace():
                                # if the token is 3 (yogh letter)
                                if sent_token.text == "3":
                                    # save it to add it to the next token to fix wrong splitting of stanza
                                    yogh = sent_token.text
                                else:
                                    # if the token is a macron add it to the previous token tag as text
                                    if sent_token.text == "~":
                                        macron = sent_token.text
                                        token.text += macron
                                    else:
                                        token_counter += 1
                                        total_token_counter += 1
                                        unique_tokens.add(yogh+sent_token.text)
                                        total_unique_tokens.add(yogh+sent_token.text)
                                        token = etree.Element("token")
                                        sentence.append(token)
                                        token.text = yogh+sent_token.text
                                    yogh = ""

                    xml_bytes = etree.tostring(tree_root, encoding=encoding, xml_declaration=True, pretty_print=True)
                    xml_str = xml_bytes.decode(encoding)
                    outfile.write(xml_str)
                    print("file is written")

        print(f"number of tokens in {root}: {token_counter}")
        print(f"number of types{root}: {len(unique_tokens)}")
        token_counter = 0
        unique_tokens.clear()

    print(f"total number of tokens: {total_token_counter}")
    print(f"total number of types: {len(total_unique_tokens)}")


# TODO get metadata for MEMT 01 from info files
def get_meta_corpus1():
    meta_dict = {}
    for root, dirs, files in os.walk("./TOY-CORPUS/1", topdown=False):
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
                        author, title = first_line.split(", ")
                        year = "-"
                        volume = "-"
                        pages = "-"
                    else:
                        title = first_line
                        author = "-"
                        year = "-"
                        volume = "-"
                        pages = "-"

                    # get name of xml file to be the key of the dict and have a mapping later
                    meta_dict[infile.rstrip("_info_converted.txt") + "_converted.xml"] = (author, title, year, volume, pages)

    return meta_dict


# TODO get metadata for EMEMT from filenames
def get_meta_corpus2():
    meta_dict = {}
    for root, dirs, files in os.walk("./TOY-CORPUS/2", topdown=False):
        for name in files:
            infile = os.path.join(root, name)
            # process differently category 6 files
            if root.endswith(" 6"):
                # year_philosophicaltransactionsvolume_pages
                title = "Philosophical Transactions"
                author = "-"
                year, volume, pages = name.split("_")
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

            meta_dict[name.rstrip(".txt")+".xml"] = (author, title, year, volume, pages)

    return meta_dict


# TODO get metadata for LMEMT from TEI xmls
def get_metadata_corpus3():

# TODO add these metadata in the header node of the xml tree (merge three dicts ?)


def main():
    text_to_xml()


if __name__ == "__main__":
    main()
