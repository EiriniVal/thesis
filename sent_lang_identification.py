# Script that uses the agreement of FurL and LangID for the detection of inter-sentential code-switches, in other words
# for the language identification of the sentences in the corpus.

from my_utils.util import open_read_lines
from models.furl.predict import train_furl
import os
import xml.etree.ElementTree as ET
import langid
import re

# determine the languages we're interested in
langid.set_languages(['en', 'la'])


def main():

    # get trained FurL model on the English and Latin sentences that I manually collected
    furl_identifier = train_furl(open_read_lines("./models/EN.txt"), open_read_lines("./models/LA.txt"))

    with open("./sent_labeled_en.txt", "w", encoding='utf-8') as out_en, \
            open("./sent_labeled_la.txt", "w", encoding='utf-8') as out_la, \
            open("./sent_unlabeled.txt", "w", encoding='utf-8') as out_unk:
        for root, dirs, files in os.walk("./data/MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy/", topdown=False):
            for name in files:

                infile = os.path.join(root, name)
                tree = ET.parse(infile)
                tree_root = tree.getroot()

                for element in tree_root.iter():
                    # get sentence from tokens
                    if element.tag == "sentence":
                        sent_id = element.get("id")
                        sentence_string = ""
                        for child in element:
                            # numerals are removed
                            if child.tag == "token" and child.get("rom_num") != "True":
                                # remove digits
                                child.text = ''.join(i for i in child.text if not i.isnumeric() or i == "3")

                                if child.text != "":
                                    if child.text != "3":
                                        sentence_string += f"{child.text} "

                        # remove punctuation except ~ and =
                        sentence_string = re.sub(r'[^\w\s=~]', '', sentence_string)

                        # get language predictions
                        pred_lang_furl = furl_identifier.identify(sentence_string)[0]  # EN or LA
                        pred_lang_langid = langid.classify(sentence_string)[0]  # en or la

                        # if models agree
                        if pred_lang_furl == pred_lang_langid.upper():

                            # if prediction is English
                            if pred_lang_furl == "EN":
                                # add sentence to English file
                                out_en.write(infile + "\t" + sent_id + "\t" + sentence_string + "\n")
                            # if prediction is Latin
                            else:
                                # add sentence to Latin file
                                out_la.write(infile + "\t" + sent_id + "\t" + sentence_string + "\n")
                        # if models disagree
                        else:
                            # add sentence to the file with the unlabeled sentences
                            out_unk.write(infile + "\t" + sent_id + "\t" + sentence_string + "\n")


if __name__ == "__main__":
    main()
    