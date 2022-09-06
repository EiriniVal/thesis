# Author: Eirini Valkana
# script that appies LangId (by Liu et al.) line by line on a test set with Latin and English senquences

import langid

# determine the languages we're interested in
langid.set_languages(['en', 'la'])

# TODO: test langid model on the same data as Furl?


def apply_model():
    with open("test.txt", "r") as infile:
        with open("langid_results.txt", "w") as outfile:
            for line in infile:
                print(type(langid.classify(line)))

    print("The results file was written.")





