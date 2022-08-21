# Script to shuffle and split the English and Latin sentences into train and test data (80%-20%)
# Author: Eirini Valkana

import random
from sklearn.model_selection import train_test_split


with open(filename) as infile:
