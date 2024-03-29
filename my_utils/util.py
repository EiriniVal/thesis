import numpy as np
import sys
import pandas as pd
from sklearn.model_selection import train_test_split, ShuffleSplit
from math import isclose

np.set_printoptions(threshold=sys.maxsize)


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


def compute_mean_std(input_list: list):
    """
    Function that computes the mean and the standard deviation of
    :param input_list: the data.
    :return: tuple containing the mean and the standard deviation
    """
    return np.mean(input_list), np.std(input_list)


# def get_train_test_data(lines_en, lines_la):
#
#     # split data of each language into training and testing
#     train_en, test_en = train_test_split(lines_en, test_size=0.20, random_state=None)
#     train_la, test_la = train_test_split(lines_la, test_size=0.20, random_state=None)
#
#     # get an array with the real labels of the test subset, so that we can later compare with the predicted labels
#     y_en_real = [0] * len(test_en)
#     y_la_real = [1] * len(test_la)
#
#     # get sentences of both languages for testing
#     all_test_sentences = test_en + test_la
#     # get an array with all the real labels of the test dataset
#     y_real = y_en_real + y_la_real
#
#     return train_en, test_en, train_la, test_la, all_test_sentences, y_real

def get_train_test_data(lines_en, lines_la):

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

    return train_en, test_en, train_la, test_la, all_test_sentences, y_real

def change_length(length: int, infile_path):
    with open(infile_path, "r") as infile:
        outfile_path = f"{infile_path.replace('.txt','')}_length{length}.txt"
        with open(outfile_path, "w") as outfile:
            for line in infile:
                line = line.strip()
                # if whole string +- 5 length get it
                if isclose(len(line), length, abs_tol=5):
                    outfile.write(line+"\n")
                # else process it to get a substring
                else:
                    # if the set length is smaller than the length of the original line we can move to processing
                    if length < len(line):
                        outfile.write(line[:length]+"\n")
    return outfile_path


def make_cross_val_table(tp, tn, fp, fn):
    data = {"GOLD LA": [tp, fn],
            "GOLD EN": [fp, tn]}
    df = pd.DataFrame(data)
    df.index = ["PREDICTED LA", "PREDICTED EN"]
    df.style.set_properties(**{'border': '1px black solid !important'})
    return df


def open_read_lines(filepath):
    with open(filepath, "r") as infile:
        return infile.readlines()
