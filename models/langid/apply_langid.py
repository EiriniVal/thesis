# Author: Eirini Valkana
# script that appies LangId (by Liu et al.) line by line on a test set with Latin and English senquences

import langid
from my_utils import util
from sklearn.metrics import balanced_accuracy_score
import os

# determine the languages we're interested in
langid.set_languages(['en', 'la'])

# TODO: test langid model on the same data as Furl?


def validate_model(folds: int, path_to_en, path_to_la,  results_directory: str):
    """
    Validates model using k-folds.
    :return:
    """
    bal_acc_all = []
    y_pred = []
    with open(path_to_en, "r") as english_file:
        lines_en = english_file.readlines()
    with open(path_to_la, "r") as latin_file:
        lines_la = latin_file.readlines()

    os.makedirs(f"./{results_directory}", exist_ok=True)

    for i in range(folds):
        with open(f"./{results_directory}/langid_fold{i}.txt", "w") as outfile:
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
    mean_acc = util.compute_mean_std(validate_model(10, "../EN.txt", "../LA.txt", "results_original"))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on data of various lengths: {mean_acc[0]}")
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on data of various lengths: {mean_acc[1]}")

    en_short = util.change_length(20, "../EN.txt")
    la_short = util.change_length(20, "../LA.txt")
    mean_acc_short = util.compute_mean_std(validate_model(10, en_short, la_short, "results_short"))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on short data: {mean_acc_short[0]}")
    print(f"Standard deviation of Furl ngram model on short data: {mean_acc_short[1]}")

    en_shorter = util.change_length(10, "../EN.txt")
    la_shorter = util.change_length(10, "../LA.txt")
    mean_acc_shorter = util.compute_mean_std(validate_model(10, en_shorter, la_shorter, "results_shorter"))
    print(f"Mean balanced accuracy of Langid (Lui et al., 2012) model on shorter data: {mean_acc_shorter[0]}")
    print(f"Standard deviation of Langid (Lui et al., 2012) model on shorter data: {mean_acc_shorter[1]}")


if __name__ == '__main__':
    main()






