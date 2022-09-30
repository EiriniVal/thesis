## GET EN AND LA SENTENCES
# get trained furl
# open files and get sentences iteratively
# apply furl on sentence
# apply langid on sentence
# if langid = furl = en write sentence in a file of en sentences
# if langid = furl = la write sentence in a file of la sentences
# Author: Eirini Valkana

from models.furl.charlm import CharLM
from models.furl.identifier import LanguageIdentifier
from my_utils.util import open_read_lines
from models.furl.predict import train_furl
import os
import xml.etree.ElementTree as ET
import langid
import re
from string import digits

# determine the languages we're interested in
langid.set_languages(['en', 'la'])


def main():
    furl_identifier = train_furl(open_read_lines("./models/EN.txt"), open_read_lines("./models/LA.txt"))

    with open("./agree_sent_en.txt", "w") as out_en, open("./agree_sent_la.txt", "w") as out_la:
        for root, dirs, files in os.walk("./data/MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/", topdown=False):
            for name in files:
                infile = os.path.join(root, name)
                # print(infile)
                # parse xml file
                tree = ET.parse(infile)
                tree_root = tree.getroot()
                for element in tree_root.iter():
                    # get sentence from tokens
                    if element.tag == "sentence":
                        sent_id = element.get("id")
                        # print(sent_id)
                        sentence_string = ""
                        for child in element:
                            # make sure it is not a roman numeral
                            if child.tag == "token" and child.get("rom_num") != "True":
                                # remove digits from tokens
                                child.text = ''.join(i for i in child.text if not i.isnumeric() or i == "3")
                                # print(child.text)
                                if child.text != "":
                                    if child.text != "3":
                                        # TODO for some unknown reason some 3s are still left
                                        sentence_string += f"{child.text} "
                        # print(sent_id, "\t", sentence_string)

                        # clean string from punctuation except ~ and =
                        sentence_string = re.sub(r'[^\w\s=~]', '', sentence_string)
                        # print(sentence_string)

                        # get language predictions
                        pred_lang_furl = furl_identifier.identify(sentence_string)[0]  # EN or LA
                        pred_lang_langid = langid.classify(sentence_string)[0]  # en or la

                        # if models agree
                        if pred_lang_furl == pred_lang_langid.upper():
                            # print("AGREEMENT: ", infile, sent_id, sentence_string)
                            if pred_lang_furl == "EN":
                                # print(pred_lang_langid.upper(), pred_lang_furl)
                                # print(sentence_string)

                                out_en.write(infile + "\t" + sent_id + "\t" + sentence_string + "\n")

                            else:

                                # print(pred_lang_langid.upper(), pred_lang_furl)
                                # print(sentence_string)
                                out_la.write(infile + "\t" + sent_id + "\t" + sentence_string + "\n")
                        else:
                            continue


main()
