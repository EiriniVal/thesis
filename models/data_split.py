# Training and Test data preparation
# Script to shuffle and split the English and Latin sentences into train and test data (80%-20%)
# Author: Eirini Valkana

import random
from sklearn.model_selection import train_test_split
import argparse

parser = argparse.ArgumentParser(description='Split data into train and test.')
parser.add_argument('--input', nargs='+',type=argparse.FileType('r'), required=True, help='The path of one or more input .txt files with one sentences per line.')
parser.add_argument('--train_prc', type=float, required=True, help='The percentage of the training data (for splitting).')
parser.add_argument('--test_prc', type=float, required=True, help='The percentage of the testing data (for splitting).')
args = parser.parse_args()

def main():
    all_test_sentences = []
    for file in args.input:
        sentences = []
        for sent in file:
            sentences.append(sent.rstrip())
        # print(sentences)

        # for each file get percentage for training and test by splitting into two lists
        train, test = train_test_split(sentences, test_size=args.test_prc, train_size=args.train_prc)
        # print(len(train))
        # print(len(test))

        # write new training file per input file with subset of sentences only
        with open(f"furl/data/{file.name}", "w") as out:
            for elem in train:
                out.write(elem+"\n")

        # get a list of all test sentences from all input files
        all_test_sentences += test

    # print(all_test_sentences)

    # shuffle test sentences
    random.shuffle(all_test_sentences)

    print(all_test_sentences)

    # write test file with all languages shuffled
    with open("furl/test.txt", "w") as out2:
        for elem in all_test_sentences:
            out2.write(elem+"\n")


if __name__ == "__main__":
    main()