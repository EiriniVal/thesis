#!/usr/bin/env python3
# coding: utf8
#
# PCL 2, FS 2018

import os
import sys

from charlm import CharLM
from identifier import LanguageIdentifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
import numpy as np


def predict(identifier, test_subset, fold):
    """
    A function that predicts the language of sequences given a language model.

    :param identifier: The language identifier model with the trained models added
    :param test_subset: An array of sequences for testing.
    :param fold: The fold number, for distinguishing the test files.
    :return: An array of the predicted (binary) labels.
    """
    os.makedirs("./results", exist_ok=True)
    code = ""
    y_pred = []
    with open("./results/furl_fold{}.txt".format(fold), "w") as outfile:
        for line in test_subset:
            label = identifier.identify(line.strip())
            if label == "EN":
                code = 0
            else:
                code = 1
            y_pred.append(code)
            outfile.write(f'{label}\t{line.strip()}\n')
        outfile.write(f'Prediction array: {y_pred}')
    return y_pred


def k_fold_val(fold_num: int):
    bal_acc_all = []
    with open("../EN.txt", "r") as english_file:
        lines_en = english_file.readlines()
    with open("../LA.txt", "r") as latin_file:
        lines_la = latin_file.readlines()

    # 10-fold validation
    for i in range(fold_num):
        # split data of each language into training and testing
        train_en, test_en = train_test_split(lines_en, test_size=0.20, random_state=None)
        train_la, test_la = train_test_split(lines_la, test_size=0.20, random_state=None)

        # get an array with the real labels of the test subset, so that we can later compare with the predicted labels
        y_en_real = [0] * len(test_en)
        y_la_real = [1] * len(test_la)

        # get sentences of both languages for testing
        all_test_sentences = test_en + test_la
        # get an array with all the real labels of the test dataset
        y_real = y_en_real + y_la_real

        # train n-gram model for English
        identifier = LanguageIdentifier()
        model1 = CharLM()
        model1.train(train_en)
        identifier.add_model("EN", model1)

        # train n-gram model for Latin
        model2 = CharLM()
        model2.train(train_la)
        identifier.add_model("LA", model2)

        # predict will return an array with the predicted values and it will write the prediction files
        y_pred = predict(identifier, all_test_sentences, i)

        bal_acc = balanced_accuracy_score(y_real, y_pred)

        print(f'Accuracy of fold {i}: {bal_acc}')

        bal_acc_all.append(bal_acc)

    return bal_acc_all


def main():
    acc_list = k_fold_val(10)

    mean_accuracy = sum(acc_list) / len(acc_list)

    print(f"Mean accuracy of Furl ngram model: {mean_accuracy}")


if __name__ == '__main__':
    main()
