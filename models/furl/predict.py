#!/usr/bin/env python3
# coding: utf8
#
# PCL 2, FS 2018

import os
import sys

from charlm import CharLM
from identifier import LanguageIdentifier
from sklearn.model_selection import train_test_split


def main():
    with open("../EN.txt", "r") as english_file:
        lines_en = english_file.readlines()
    with open("../LA.txt", "r") as latin_file:
        lines_la = latin_file.readlines()

    for i in range(10):
        train_en, test_en = train_test_split(lines_en, test_size=0.20, random_state=None)

        train_la, test_la = train_test_split(lines_la, test_size=0.20, random_state=None)

        # get sentences of both languages for testing
        all_test_sentences = test_en + test_la

        identifier = LanguageIdentifier()
        model1 = CharLM()
        model1.train(train_en)
        identifier.add_model("EN", model1)

        model2 = CharLM()
        model2.train(train_la)
        identifier.add_model("LA", model2)

        predict(identifier, all_test_sentences, i)


def predict(identifier, test_subset, fold):
    """
	Evaluate the classifier with the test set.
	"""

    code = ""
    with open("results_furl_{}.txt".format(fold),"w") as outfile:
        for line in test_subset:
            label = identifier.identify(line.strip())
            if label == "EN":
                code = 0
            else:
                code = 1

            outfile.write(f'{code}\t{line.strip()}\n')


if __name__ == '__main__':
    main()
