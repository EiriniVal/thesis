# Author: Eirini Valkana
# script that appies LangId (by Liu et al.) line by line on a test set with Latin and English senquences

import langid

langid.set_languages(['en','la'])

with open("test.txt", "r") as infile:
    with open("langid_results.txt", "w") as outfile:
        for line in infile:
            outfile.write(f"{line} {langid.classify(line)}\n")

print("The results file was written.")





