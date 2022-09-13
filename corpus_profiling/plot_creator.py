# Author: Eirini Valkana
# !/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import os


df = pd.read_csv("corpus_data.csv")

df2 = df.groupby(['sub_corpus'])[['tokens', 'roman_numerals_counts', 'scribal_abbrev_counts', 'old_alphabet_counts', 'numbers']].sum()

print(df2)

# total_roman_counts = df2['roman_numerals_counts'].sum()
# total_modern_num_counts = df2['numbers'].sum()
# total_abbrev_counts = df2['scribal_abbrev_counts'].sum()
# total_old_alpha_counts = df2['old_alphabet_counts'].sum()


df2['Tokens with old alphabet characters percentage'] = ((df2['old_alphabet_counts'] / df2['tokens']) *100)
df2['Scribal abbreviation percentage'] = ((df2['scribal_abbrev_counts'] / df2['tokens']) *100)
df2['Roman numerals percentage'] = ((df2['roman_numerals_counts'] / df2['tokens']) *100)
df2['Modern numerals percentage'] = ((df2['numbers'] / df2['tokens']) *100)


# df2['Tokens with old alphabet characters percentage'] = ((df2['old_alphabet_counts'] / total_old_alpha_counts) * 100)
# df2['Scribal abbreviation percentage'] = ((df2['scribal_abbrev_counts'] / total_abbrev_counts) * 100)
# df2['Roman numerals percentage'] = ((df2['roman_numerals_counts'] / total_roman_counts) * 100)
# df2['Modern numerals percentage'] = ((df2['numbers'] / total_modern_num_counts) * 100)

os.makedirs('./plots', exist_ok=True)

df2[['Tokens with old alphabet characters percentage']].plot(kind='bar', color='purple').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/old_alphabet_bar_chart.pdf")

df2[['Scribal abbreviation percentage']].plot(kind='bar', color='yellow').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/scribal_abbreviations_bar_chart.pdf")

df2[['Roman numerals percentage']].plot(kind='bar', color='orange').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/roman_numerals_bar_chart.pdf")

df2[['Modern numerals percentage']].plot(kind='bar', color='crimson').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./plots/modern_numerals_bar_chart.pdf")
