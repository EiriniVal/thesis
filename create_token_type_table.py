import pandas as pd

corpus_data = pd.read_csv("corpus_profiling/corpus_data.csv")


df2 = corpus_data.groupby("sub_corpus").agg({"tokens": sum, "types": sum})
df2.loc['Total']= df2.sum()

# write table with tokens and types counts only for sub-corpora and the whole corpus
df2.to_csv('./corpus_profiling/corpus_tokens_types.csv')




