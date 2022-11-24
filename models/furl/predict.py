# Script that trains and evaluates FurL.

import os
import pathlib
from charlm import CharLM
from identifier import LanguageIdentifier
from sklearn.metrics import balanced_accuracy_score
from my_utils import util


def predict(identifier, test_subset, test_filename):
    """
    A function that predicts the language of the sequences within a file given a language model.
    :param identifier: The language identifier model with the trained models included.
    :param test_subset: An array of sequences for testing.
    :param test_filename: name of test file
    :return: An array of the predicted language labels: 1 for Latin, 0 for English.
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
    en_lines = []
    la_lines = []
    en_testlines = []
    la_testlines = []
    bal_acc_all = []

    # positive class is 1 = LA
    # true positives = real value and pred value is 1 (LA)
    tp = 0
    # true negatives = real value and pred value is 0 (EN)
    tn = 0
    # false positives = real value is 0 (EN) and pred value is 1 (LA)
    fp = 0
    # false negatives = real value is 1 (LA) and pred value is 0 (EN)
    fn = 0

    f = 1
    while f <= folds:
        for path in pathlib.Path(train_directory).iterdir():
            if path.is_file():
                # go by fold num
                if f"fold{f}" in str(path):
                    # get en lines
                    with open(path, "r") as infile:
                        if "_en_" in str(path):
                            en_lines = infile.readlines()
                            print(f"Training file en: {path}")
                        else:
                            la_lines = infile.readlines()
                            print(f"Training file la: {path}")

        # train model
        identifier = train_furl(en_lines, la_lines)

        print(f"\n### FOLD {f} ###\n")

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
        y_pred_en = predict(identifier, en_testlines, filename_en)
        print(f"Out of {len(y_real_en)} English sentences, {y_pred_en.count(1)} were misclassified as Latin.")

        # r1c1 y_pred_en.count(0) r1c2 y_pred_en.count(1)

        # prediction for LA
        y_pred_la = predict(identifier, la_testlines, filename_la)
        print(f"Out of {len(y_real_la)} Latin sentences, {y_pred_la.count(0)} were misclassified as English.")

        # r2c1 y_pred_la.count(0) r2c2 y_pred_la.count(1)

        # get all values
        y_real = y_real_en + y_real_la
        y_pred = y_pred_en + y_pred_la

        bal_acc = balanced_accuracy_score(y_real, y_pred)
        print(f'Balanced accuracy of fold {f}: {bal_acc}')
        bal_acc_all.append(bal_acc)

        tp += y_pred_la.count(1)
        tn += y_pred_en.count(0)

        fp += y_pred_en.count(1)
        fn += y_pred_la.count(0)

        f += 1

    # GENERATE TABLE
    print(f"\n{util.make_cross_val_table(tp, tn, fp, fn)}\n")

    return bal_acc_all


def main():
    print(f"###### TESTING FURL ON ORIGINAL DATA ######\n")
    mean_acc = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_original", 5))
    print(f"\nMean balanced accuracy of Furl ngram model on original data: {mean_acc[0]}")
    print(f"Standard deviation of Furl ngram model on original data: {mean_acc[1]}\n\n")

    print(f"###### TESTING FURL ON DATA ~= 40 CHARACTERS ######\n")
    # evaluate on data of approx. 40 characters, the training data remains the original dataset
    mean_acc_short = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_len40", 5))
    print(f"\nMean balanced accuracy of Furl ngram model on sequences of ~= 40 characters: {mean_acc_short[0]}")
    print(f"Standard deviation of Furl ngram model on sequences of ~= 40 characters: {mean_acc_short[1]}\n\n")

    print(f"###### TESTING FURL ON DATA ~= 20 CHARACTERS ######\n")
    # evaluate on data of approx. 20 characters, the training data remains the original dataset
    mean_acc_shorter = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_len20", 5))
    print(f"\nMean balanced accuracy of Furl ngram model on sequences of ~= 20 characters: {mean_acc_shorter[0]}")
    print(f"Standard deviation of Furl ngram model on on sequences of ~= 20 characters: {mean_acc_shorter[1]}\n\n")

    print(f"###### TESTING FURL ON DATA ~= 10 CHARACTERS ######\n")
    # evaluate on data of approx. 10 characters, the training data remains the original dataset
    mean_acc_shortest = util.compute_mean_std(k_fold_val("../training_data_original", "../testing_data_len10", 5))
    print(f"\nMean balanced accuracy of Furl ngram model on sequences of ~= 10 characters: {mean_acc_shortest[0]}")
    print(f"Standard deviation of Furl ngram model on sequences of ~= 10 characters: {mean_acc_shortest[1]}\n\n")


if __name__ == '__main__':
    main()
