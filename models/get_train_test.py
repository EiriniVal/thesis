import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import ShuffleSplit
from math import isclose
import pathlib


def get_lines(input_file):
    with open(input_file, "r") as infile:
        return infile.readlines()


def change_length(length: int, infile_path, dir_name):
    os.makedirs(f"./{dir_name}", exist_ok=True)
    with open(infile_path, "r") as infile:
        # it is a path lib object, we only need the filename for writing it
        filename = infile_path.name
        outfile_path = f"./{dir_name}/{filename.replace('.txt', '')}_length{length}.txt"
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


def kf_split_data(folds: int, lines_array, lang_code, dir_name):
    os.makedirs(f"./training_data_{dir_name}", exist_ok=True)
    os.makedirs(f"./testing_data_{dir_name}", exist_ok=True)
    kf = KFold(n_splits=folds, random_state=1, shuffle=True)
    f = 1
    for train_index, test_index in kf.split(lines_array):
        print("TRAIN:", train_index, "TEST:", test_index)

        train_file = f"./training_data_{dir_name}/train_{lang_code}_fold{f}.txt"
        test_file = f"./testing_data_{dir_name}/test_{lang_code}_fold{f}.txt"

        with open(train_file, 'w') as trainfile, open(test_file, 'w') as testfile:
            trainfile.write(''.join(lines_array[train_index[j]] for j in range(len(train_index))))
            testfile.write(''.join(lines_array[test_index[i]] for i in range(len(test_index))))

        f += 1

    print("Training and testing files were written in the training_data and testing_data directories respectively.")


def main():
    # write files for LA and EN with train and test data using k-fold
    kf_split_data(5, get_lines("./LA.txt"), "la", "original")
    kf_split_data(5, get_lines("./EN.txt"), "en", "original")

    # go to the testing directory and for each file change the length of the sequences and copy them to another file
    for path in pathlib.Path("./testing_data_original").iterdir():
        # for each file
        if path.is_file():
            # generate new directories including files with different lengths for sequences
            change_length(40, path, "testing_data_len40")
            change_length(20, path, "testing_data_len20")
            change_length(10, path, "testing_data_len10")


if __name__ == '__main__':
    main()
