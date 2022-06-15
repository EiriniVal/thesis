# Author: Eirini Valkana
import glob
import os
from striprtf.striprtf import rtf_to_text

directory = 'MIDDLE-MODERN-ENGLISH-MEDICAL-CORPUS - Copy/01_MEMT_Texts'
# path of the given file
# abs_path = os.path.dirname(os.path.abspath(directory))
# counter = 0

# get all rtf files
for filename in glob.iglob(fr'{directory}/*'):
    #print(filename)
    #counter +=1
    #print(counter)
    with open(filename, "r", encoding='utf-8') as f:
        with open(f'{filename.rstrip(".rtf")}_converted.txt', "w", encoding='utf-8') as out:
            out.write(rtf_to_text(f.read()))

