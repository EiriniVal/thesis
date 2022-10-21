# Author: Eirini Valkana

import os
import xml.etree.ElementTree as ET
import subprocess
from collections import defaultdict
from numba import jit, cuda
# to measure exec time
from timeit import default_timer as timer

# function optimized to run on gpu
@jit(target_backend='cuda')
def get_pos_info(filename):  # sent_id: (tokens, tokens_ids, sentence_string)
    tree = ET.parse(filename)
    tree_root = tree.getroot()
    for element in tree_root.iter():
        # if element is sentence feed it as one in the rnn_tagger
        if element.tag == "sentence":
            info_per_sentence = defaultdict(list)
            pos_list = []
            lemma_list = []
            token_list = []
            token_id_list = []
            sent_id = element.get("id")

            # save all tokens in sentence
            for child in element.iter():
                if child.tag == "token":
                    token_text = child.text
                    token_id = child.get("id")
                    token_list.append(token_text)
                    token_id_list.append(token_id)

            # get raw sentence string to feed to the rnntagger
            sentence_string = " ".join(token_list)

            # sentences_per_file[sent_id] = (token_list, token_id_list, sentence_string)
            info_per_sentence[sent_id].append(sentence_string)
            info_per_sentence[sent_id].append(token_id_list)

            p = subprocess.Popen(f"echo {sentence_string.encode('utf-8')} | cmd/rnn-tagger-middle-english.sh",
                                 stdout=subprocess.PIPE,
                                 shell=True, cwd="./RNNTagger")

            tokens = p.communicate()[0].decode("utf-8").split("\n")
            for token in tokens:
                if len(token.split("\t")) == 3:
                    token, token_pos, token_lemma = token.split("\t")
                    # print(token, token_pos, token_lemma)
                    pos_list.append(token_pos)
                    lemma_list.append(token_lemma)

            info_per_sentence[sent_id].append(pos_list)
            info_per_sentence[sent_id].append(lemma_list)

            print(info_per_sentence)
            wd = os.getcwd()
            os.chdir(wd)

            for key, value in info_per_sentence.items():
                if key == sent_id:
                    for child in element.iter():
                        if child.tag == "token":
                            index = value[1].index(child.get("id")) # search for index of token using the ids not the tokens!!, then use this index to find the correspondent value in the pos list and lemma list
                            token_pos = value[2][index]
                            token_lemma = value[3][index]
                            child.attrib["pos"] = token_pos
                            child.attrib["lemma"] = token_lemma

    f = open(filename, 'wb')
    f.write(ET.tostring(tree_root, encoding='utf-8', xml_declaration=True))
    f.close()


def main():
    # os.makedirs('./raw_sentences_files', exist_ok=True)
    for root, dirs, files in os.walk("./MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS-Copy", topdown=False):
        for name in files:
            infile = os.path.join(root, name)
            get_pos_info(infile)


if __name__ == "__main__":
    start = timer()
    main()
    print(timer() - start)
