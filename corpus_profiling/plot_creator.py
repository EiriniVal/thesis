# Script for generating the bar charts in the plots directory.

import matplotlib.pyplot as plt
import pandas as pd
import os

# #7a6679
# #ae6a86
# #e16e77
# #ff8151
# #ffa600
df = pd.read_csv("./corpus_data.csv")

df2 = df.groupby(['sub_corpus'])[['tokens', 'roman_numerals_counts', 'scribal_abbrev_counts', 'old_alphabet_counts', 'numbers']].sum()

print(df2)

df2['Percentage of old alphabet characters'] = ((df2['old_alphabet_counts'] / df2['tokens']) *100)
df2['Percentage of scribal abbreviations'] = ((df2['scribal_abbrev_counts'] / df2['tokens']) *100)
df2['Percentage of roman numerals'] = ((df2['roman_numerals_counts'] / df2['tokens']) *100)
df2['Percentage of modern numerals'] = ((df2['numbers'] / df2['tokens']) *100)


os.makedirs('./plots', exist_ok=True)

df2[['Percentage of old alphabet characters']].plot(kind='bar', color='#ae6a86').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/old_alphabet_bar_chart.pdf")
print(df2['Percentage of old alphabet characters'] )

df2[['Percentage of scribal abbreviations']].plot(kind='bar', color='#ae6a86').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/scribal_abbreviations_bar_chart.pdf")
print(df2['Percentage of scribal abbreviations'])

df2[['Percentage of roman numerals']].plot(kind='bar', color='#ae6a86').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/roman_numerals_bar_chart.pdf")
print(df2['Percentage of roman numerals'])

df2[['Percentage of modern numerals']].plot(kind='bar', color='#ae6a86').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/modern_numerals_bar_chart.pdf")
print(df2['Percentage of modern numerals'])
