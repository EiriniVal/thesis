# Author: Eirini Valkana
# script that appies LangId (by Liu et al.) line by line on a test set with Latin and English senquences

import langid
from my_utils import util
import pathlib
from sklearn.metrics import balanced_accuracy_score
import os

# determine the languages we're interested in
langid.set_languages(['en', 'la'])


def langid_predict(test_sentences: list, outfile_name):
    os.makedirs(f"./results_directory", exist_ok=True)
    y_pred = []
    with open(f"./results_directory/langid_{outfile_name}", "w") as outfile:
        for sent in test_sentences:
            label = langid.classify(sent)[0]
            if label == "en":
                code = 0
            else:
                code = 1
            y_pred.append(code)
            outfile.write(f'{label}\t{sent.strip()}\n')
    return y_pred


def validate_model(test_directory, folds):
    """
    Validates model using k-folds.
    :return:
    """
    bal_acc_all = []
    f = 1
    while f <= folds:
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

        print(f"### FOLD {f} ###")

        # prediction for EN
        y_pred_en = langid_predict(en_testlines, filename_en)
        print(f"Out of {len(y_real_en)} English sentences, {y_pred_en.count(1)} were misclassified as Latin.")

        # prediction for LA
        y_pred_la = langid_predict(la_testlines, filename_la)
        print(f"Out of {len(y_real_la)} Latin sentences, {y_pred_la.count(0)} were misclassified as English.")

        # get all values
        y_real = y_real_en + y_real_la
        y_pred = y_pred_en + y_pred_la

        bal_acc = balanced_accuracy_score(y_real, y_pred)
        print(f'Balanced accuracy of fold {f}: {bal_acc}')
        bal_acc_all.append(bal_acc)

        f += 1

    return bal_acc_all


def main():
    print(f"###### TESTING LANGID ON ORIGINAL DATA ######")
    mean_acc = util.compute_mean_std(validate_model("../testing_data_original", 5))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on data of various lengths: {mean_acc[0]}")
    print(f"Standard deviation of Langid (Lui et al., 2012) model on data of various lengths: {mean_acc[1]}")

    print(f"###### TESTING LANGID ON DATA ~= 40 CHARACTERS ######")
    mean_acc_short = util.compute_mean_std(validate_model("../testing_data_len40", 5))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on short data: {mean_acc_short[0]}")
    print(f"Standard deviation of Langid (Lui et al., 2012) model on short data: {mean_acc_short[1]}")

    print(f"###### TESTING LANGID ON DATA ~= 20 CHARACTERS ######")
    mean_acc_shorter = util.compute_mean_std(validate_model("../testing_data_len20", 5))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on shorter data: {mean_acc_shorter[0]}")
    print(f"Standard deviation of Langid (Lui et al., 2012) model on shorter data: {mean_acc_shorter[1]}")

    print(f"###### TESTING LANGID ON DATA ~= 10 CHARACTERS ######")
    mean_acc_shortest = util.compute_mean_std(validate_model("../testing_data_len10", 5))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on shortest data: {mean_acc_shortest[0]}")
    print(f"Standard deviation of Langid (Lui et al., 2012) model on shortest data: {mean_acc_shortest[1]}")


if __name__ == '__main__':
    main()
