# Author: Eirini Valkana
# !/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import os


df = pd.read_csv("corpus_profiling/corpus_data.csv")

df2 = df.groupby(['sub_corpus'])[['tokens', 'roman_numerals_counts', 'scribal_abbrev_counts', 'old_alphabet_counts', 'numbers']].sum()

df2['Perc_old_alpha'] = (df2['old_alphabet_counts'] / df2['tokens']) *100
df2['Perc_scribal'] = (df2['scribal_abbrev_counts'] / df2['tokens']) *100
df2['Perc_roman'] = (df2['roman_numerals_counts'] / df2['tokens']) *100
df2['Perc_num'] = (df2['numbers'] / df2['tokens']) *100

os.makedirs('./corpus_profiling/plots', exist_ok=True)

df2[['Perc_old_alpha']].plot(kind='bar', color='purple').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./corpus_profiling/plots/old_alphabet_bar_chart.pdf")

df2[['Perc_scribal']].plot(kind='bar', color='yellow').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./corpus_profiling/plots/scribal_abbreviations_bar_chart.pdf")

df2[['Perc_roman']].plot(kind='bar', color='orange').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./corpus_profiling/plots/roman_numerals_bar_chart.pdf")

df2[['Perc_num']].plot(kind='bar', color='crimson').set_xticklabels(df2.index, rotation="horizontal")
plt.savefig("./corpus_profiling/plots/modern_numerals_bar_chart.pdf")
