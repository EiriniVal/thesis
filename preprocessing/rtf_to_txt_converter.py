# Script that converts all the RTF files of the MEMT subcorpus to TXT.

import glob
from striprtf.striprtf import rtf_to_text

# path to the original directory of the first subcorpus with the .rtf files, as it was published in the CD-ROM
# Important: for space efficiency reasons this directory is not included in the main directory of the thesis
directory = 'MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS/01_MEMT_Texts'

for filename in glob.iglob(fr'{directory}/*'):
    with open(filename, "r", encoding='utf-8') as f:
        with open(f'{filename.rstrip(".rtf")}_converted.txt', "w", encoding='utf-8') as out:
            out.write(rtf_to_text(f.read()))
