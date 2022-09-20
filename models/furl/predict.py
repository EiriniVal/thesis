#!/usr/bin/env python3
# coding: utf8
#
# PCL 2, FS 2018

import os
import sys
import pathlib

from charlm import CharLM
from identifier import LanguageIdentifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from my_utils import util


def predict(identifier, test_subset, fold, test_filename):
    """
    A function that predicts the language of sequences given a language model.

    :param results_directory: the name of the directory where the results files will be saved.
    :param identifier: The language identifier model with the trained models added
    :param test_subset: An array of sequences for testing.
    :param fold: The fold number, for distinguishing the test files.
    :return: An array of the predicted (binary) labels.
    """
    os.makedirs(f"./results_directory", exist_ok=True)
    y_pred = []
    with open(f"./results_directory/furl_{test_filename}", "w") as outfile:
        for line in test_subset:
            label = identifier.identify(line.strip())[0]
            if label == "EN":
                code = 0
            else:
                code = 1
            y_pred.append(code)
            outfile.write(f'{label}\t{line.strip()}\n')
        outfile.write(f'Prediction array: {y_pred}')
    return y_pred


# def k_fold_val(fold_num: int, path_to_en, path_to_la, results_directory):
#     bal_acc_all = []
#     # with open(path_to_en, "r") as english_file:
#     #     lines_en = english_file.readlines()
#     # with open(path_to_la, "r") as latin_file:
#     #     lines_la = latin_file.readlines()
#
#     # # 10-fold validation
#     # for i in range(fold_num):
#     #     train_en, test_en, train_la, test_la, all_test_sentences, y_real = util.get_train_test_data(lines_en, lines_la)
#     #     print(test_en)
#     #     # train n-gram model for English
#     #     identifier = LanguageIdentifier()
#     #     model1 = CharLM()
#     #     model1.train(train_en)
#     #     identifier.add_model("EN", model1)
#     #
#     #     # train n-gram model for Latin
#     #     model2 = CharLM()
#     #     model2.train(train_la)
#     #     identifier.add_model("LA", model2)
#
#         # predict will return an array with the predicted values and it will write the prediction files
#         y_pred = predict(identifier, all_test_sentences, i, results_directory)
#
#         bal_acc = balanced_accuracy_score(y_real, y_pred)
#
#         print(f'Accuracy of fold {i}: {bal_acc}')
#
#         bal_acc_all.append(bal_acc)
#
#     return bal_acc_all

def train_furl(train_en, train_la):
    identifier = LanguageIdentifier()
    model1 = CharLM()
    model1.train(train_en)
    identifier.add_model("EN", model1)

    # train n-gram model for Latin
    model2 = CharLM()
    model2.train(train_la)
    identifier.add_model("LA", model2)

    return identifier


def k_fold_val(train_directory, test_directory, folds):
    # open training_data directory and testing data directory
    # train_furl() on en and la, and predict() with it the respective datasets in testing_data directory
    # repeat 5 times
    en_lines = []
    la_lines = []
    en_testlines = []
    la_testlines = []
    bal_acc_all = []
    f = 1
    while f <= folds:
        for path in pathlib.Path(train_directory).iterdir():
            if path.is_file():
                # go by fold num
                if f"fold{f}" in str(path):
                    # get en lines
                    with open(path, "r") as infile:
                        if "en" in str(path):
                            en_lines = infile.readlines()
                            print(f"Training file en: {path}")
                        else:
                            la_lines = infile.readlines()
                            print(f"Training file la: {path}")

        # train model
        identifier = train_furl(en_lines, la_lines)

        for testpath in pathlib.Path(test_directory).iterdir():
            if testpath.is_file():
                if f"fold{f}" in str(testpath):
                    # get en lines
                    with open(testpath, "r") as testfile:
                        if "_en_" in str(testpath):
                            en_testlines = testfile.readlines()
                            y_real_en = [0] * len(en_testlines)
                            filename_en = testpath.name
                            print(f"Testing file en: {testpath}")
                        else:
                            la_testlines = testfile.readlines()
                            y_real_la = [1] * len(la_testlines)
                            filename_la = testpath.name
                            print(f"Testing file la: {testpath}")

        # prediction for EN
        y_pred_en = predict(identifier, en_testlines, f, filename_en)

        print(f"### FOLD {f} ###")

        print(f"Out of {len(y_real_en)} English sentences, {y_pred_en.count(1)} were misclassified as Latin.")

        # prediction for LA
        y_pred_la = predict(identifier, la_testlines, f, filename_la)

        print(f"Out of {len(y_real_la)} Latin sentences, {y_pred_la.count(0)} were misclassified as English.")

        # get all values
        y_real = y_real_en + y_real_la
        y_pred = y_pred_en + y_pred_la

        bal_acc = balanced_accuracy_score(y_real, y_pred)
        print(f'Accuracy of fold {f}: {bal_acc}')
        bal_acc_all.append(bal_acc)

        f += 1

    return bal_acc_all


def main():
    mean_acc = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_original", 5))
    print(f"Mean balanced accuracy of Furl ngram model on original data: {mean_acc[0]}")
    print(f"Standard deviation of Furl ngram model on original data: {mean_acc[1]}")

    mean_acc_short = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_len40", 5))
    print(f"Mean balanced accuracy of Furl ngram model on sequences of ~= 40 characters: {mean_acc_short[0]}")
    print(f"Standard deviation of Furl ngram model on sequences of ~= 40 characters: {mean_acc_short[1]}")

    mean_acc_shorter = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_len20", 5))
    print(f"Mean balanced accuracy of Furl ngram model on sequences of ~= 20 characters: {mean_acc_shorter[0]}")
    print(f"Standard deviation of Furl ngram model on on sequences of ~= 20 characters: {mean_acc_shorter[1]}")

    mean_acc_shortest = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_len10", 5))
    print(f"Mean balanced accuracy of Furl ngram model on sequences of ~= 10 characters: {mean_acc_shortest[0]}")
    print(f"Standard deviation of Furl ngram model on sequences of ~= 10 characters: {mean_acc_shortest[1]}")


if __name__ == '__main__':
    main()
