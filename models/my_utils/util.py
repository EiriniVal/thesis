# Author: Eirini Valkana
import numpy as np
import sys
import os
from sklearn.model_selection import train_test_split, cross_val_score, KFold, ShuffleSplit

np.set_printoptions(threshold=sys.maxsize)


# data split 10-fold
def k_fold_split(k: int, test: float, X_data, y_data):
    """

    :param k: number of folds
    :param test: proportion of test data, must be float
    :param X_data: X array of main data (sentences)
    :param y_data: labels of data (0, 1)
    :return: tuple of tuples containing lists of the corresponding training and test data splits
    for both the main data (X) and the label (y) dataset
    """
    X_folds = []
    y_folds = []
    ss = ShuffleSplit(n_splits=k, test_size=test, random_state=0)
    for train_index, test_index in ss.split(X_data):
        X_folds.append(([X_data[train_index[j]] for j in range(len(train_index))],
                       [X_data[test_index[i]] for i in range(len(test_index))]))
    for y_train_index, y_test_index in ss.split(y_data):
        y_folds.append(([y_data[y_train_index[j]] for j in range(len(y_train_index))],
                       [y_data[y_test_index[i]] for i in range(len(y_test_index))]))

    return X_folds, y_folds


# map lang sentences to 0s and 1s
def binary_map_labels_sentences(*sentences_files):
    """

    :param sentences_files: path to EN.txt and LA.txt
    :return: Sentences arrays (X) and binary label (y) arrays for English (0) and Latin sentences (1)
    """
    for filename in sentences_files:
        with open(filename, "r") as infile:
            line_list = infile.readlines()
            if "EN.txt" in filename:
                X_en = np.char.asarray(line_list)
                y_en = np.zeros(len(line_list))
            else:
                X_la = np.char.asarray(line_list)
                y_la = np.ones(len(line_list))

    X = np.char.asarray(np.concatenate((X_en, X_la)))
    y = np.concatenate((y_en, y_la))

    return X, y


# def ngram_binary_map(*sentences_files):
#     """
#
#     :param sentences_files:
#     :return:
#     """
#     for filename in sentences_files:
#         with open(filename, "r") as infile:
#             line_list = infile.readlines()
#             if "EN.txt" in filename:
#                 X_en = np.char.asarray(line_list)
#                 y_en = np.zeros(len(line_list))
#             else:
#                 X_la = np.char.asarray(line_list)
#                 y_la = np.ones(len(line_list))
#
#     return X_en, X_la, y_en, y_la


# def ngram_k_fold(k: int, test: float, X_lang1, y_lang1):
#     """
#
#     :return: returns folds for only 1 language
#     """
#     X_folds = []
#     y_folds = []
#
#     kf = KFold(n_splits=10, random_state=0, shuffle=False)
#
#     for train_index, test_index in kf.split(X_lang1):
#         X_folds.append(([X_lang1[train_index[j]] for j in range(len(train_index))],
#                         [X_lang1[test_index[i]] for i in range(len(test_index))]))
#     for y_train_index, y_test_index in kf.split(y_lang1):
#         y_folds.append(([y_lang1[y_train_index[j]] for j in range(len(y_train_index))],
#                         [y_lang1[y_test_index[i]] for i in range(len(y_test_index))]))
#
#     return X_folds, y_folds
# print(binary_map_labels_sentences("models/EN.txt", "models/LA.txt"))

# data = binary_map_labels_sentences("models/EN.txt", "models/LA.txt")

# print(type(k_fold_split(10,0.20,data[0],data[1])[0][0][0]))


def data_split_ngram_model():
    with open("../EN.txt", "r") as english_file:
        lines_en = english_file.readlines()
    with open("../LA.txt", "r") as latin_file:
        lines_la = latin_file.readlines()

    for i in range(10):
        train_en, test_en, train_la, test_la = train_test_split(lines_en, lines_la, test_size=0.20, random_state=i,
                                                            shuffle=False)
        # get sentences of both languages for testing
        all_test_sentences = test_en + test_la

        # trainmodel(train_en, train_la, all_test_sentences)







