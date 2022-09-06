# Author: Eirini Valkana
# script that appies LangId (by Liu et al.) line by line on a test set with Latin and English senquences

import langid
from my_utils import util
from sklearn.metrics import balanced_accuracy_score
import os

# determine the languages we're interested in
langid.set_languages(['en', 'la'])

# TODO: test langid model on the same data as Furl?


def validate_model(folds: int):
    """
    Validates model using k-folds.
    :return:
    """
    bal_acc_all = []
    y_pred = []
    with open("../EN.txt", "r") as english_file:
        lines_en = english_file.readlines()
    with open("../LA.txt", "r") as latin_file:
        lines_la = latin_file.readlines()

    os.makedirs("./results", exist_ok=True)

    for i in range(folds):
        with open("./results/langid_fold{}.txt".format(i), "w") as outfile:
            # get data for testing
            train_en, test_en, train_la, test_la, all_test_sentences, y_real = util.get_train_test_data(lines_en, lines_la)

            for sentence in all_test_sentences:
                label = langid.classify(sentence)[0]
                if label == "en":
                    code = 0
                else:
                    code = 1
                y_pred.append(code)

                outfile.write(f'{label}\t{sentence.strip()}\n')

            # get balanced accuracy
            bal_acc = balanced_accuracy_score(y_real, y_pred)
            bal_acc_all.append(bal_acc)

            outfile.write(f'Prediction array: {y_pred}')

            # empty array for next fold
            y_pred = []
            print(f'Accuracy of fold {i}: {bal_acc}')

    return bal_acc_all


def main():
    mean_acc = util.mean_accuracy(validate_model(10))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model: {mean_acc}")


if __name__ == '__main__':
    main()






