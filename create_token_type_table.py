import pandas as pd
import matplotlib.pyplot as plt
from profiler import corpus_profiling

corpus_data = pd.read_csv("corpus_profiling/corpus_data.csv")

total_num_types = len(corpus_profiling()[1])
num_types_1 = len(corpus_profiling()[2])
num_types_2 = len(corpus_profiling()[3])
num_types_3 = len(corpus_profiling()[4])

print(total_num_types, num_types_1, num_types_2, num_types_3)

df2 = corpus_data.groupby("sub_corpus").agg({"tokens": sum, "types": [num_types_1, num_types_2, num_types_3]})
df2.loc["Total", "tokens"] = df2["tokens"].sum()
df2.loc["Total", "types"] = total_num_types

# write table with tokens and types counts only for sub-corpora and the whole corpus
df2.to_csv('./corpus_profiling/corpus_tokens_types.csv')

# create plots
# percentage = 100 * float(part)/float(whole)
# df2 = corpus_data.groupby(['sub_corpus']).agg({"tokens": sum, 'old_alphabet_counts': 'sum'})
# df2['percentage'] = (df2['old_alphabet_counts'] / df2['tokens']) *100
#
# print(df2)
