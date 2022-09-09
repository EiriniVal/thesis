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
from my_utils import util


def predict(identifier, test_subset, fold, results_directory: str):
    """
    A function that predicts the language of sequences given a language model.

    :param results_directory: the name of the directory where the results files will be saved.
    :param identifier: The language identifier model with the trained models added
    :param test_subset: An array of sequences for testing.
    :param fold: The fold number, for distinguishing the test files.
    :return: An array of the predicted (binary) labels.
    """
    os.makedirs(f"./{results_directory}", exist_ok=True)
    y_pred = []
    with open(f"./{results_directory}/furl_fold{fold}.txt", "w") as outfile:
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


def k_fold_val(fold_num: int, path_to_en, path_to_la, results_directory):
    bal_acc_all = []
    with open(path_to_en, "r") as english_file:
        lines_en = english_file.readlines()
    with open(path_to_la, "r") as latin_file:
        lines_la = latin_file.readlines()

    # 10-fold validation
    for i in range(fold_num):
        train_en, test_en, train_la, test_la, all_test_sentences, y_real = util.get_train_test_data(lines_en, lines_la)

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
        y_pred = predict(identifier, all_test_sentences, i, results_directory)

        bal_acc = balanced_accuracy_score(y_real, y_pred)

        print(f'Accuracy of fold {i}: {bal_acc}')

        bal_acc_all.append(bal_acc)

    return bal_acc_all


def main():
    mean_acc = util.compute_mean_std(k_fold_val(10, "../EN.txt", "../LA.txt", "results_original"))
    print(f"Mean balanced accuracy of Furl ngram model on original data: {mean_acc[0]}")
    print(f"Standard deviation of Furl ngram model on original data: {mean_acc[1]}")

    en_short = util.change_length(20, "../EN.txt")
    la_short = util.change_length(20, "../LA.txt")
    mean_acc_short = util.compute_mean_std(k_fold_val(10, en_short, la_short, "results_short"))
    print(f"Mean balanced accuracy of Furl ngram model on short data: {mean_acc_short[0]}")
    print(f"Standard deviation of Furl ngram model on short data: {mean_acc_short[1]}")

    en_shorter = util.change_length(10, "../EN.txt")
    la_shorter = util.change_length(10, "../LA.txt")
    mean_acc_shorter = util.compute_mean_std(k_fold_val(10, en_shorter, la_shorter, "results_shorter"))
    print(f"Mean balanced accuracy of Furl ngram model on shorter data: {mean_acc_shorter[0]}")
    print(f"Standard deviation of Furl ngram model on shorter data: {mean_acc_shorter[1]}")

    en_shortest = util.change_length(2, "../EN.txt")
    la_shortest = util.change_length(2, "../LA.txt")
    mean_acc_shortest = util.compute_mean_std(k_fold_val(10, en_shortest, la_shortest, "results_shortest"))
    print(f"Mean balanced accuracy of Furl ngram model on shortest data: {mean_acc_shortest[0]}")
    print(f"Standard deviation of Furl ngram model on shortest data: {mean_acc_shortest[1]}")


if __name__ == '__main__':
    main()
