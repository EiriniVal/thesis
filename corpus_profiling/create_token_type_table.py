# Script for generating the table with the token and type counts.

import pandas as pd
import os
import subprocess

counts_dict = {}

for root, dirs, files in os.walk("../vocabulary", topdown=False):
    for name in files:
        infile = os.path.join(root, name)
        p1 = subprocess.run(['wc', '-l', infile], capture_output=True)
        counts_dict[name] = p1.stdout.decode('utf8').split(" ")[0]

print(counts_dict)

corpus_data = pd.read_csv("./corpus_data.csv")

# get vocabulary data

for key, value in counts_dict.items():
    if key == 'vocab_corpus1.txt':
        vocab_len_1 = '{:,}'.format(int(value))
    if key == 'vocab_corpus2.txt':
        vocab_len_2 = '{:,}'.format(int(value))
    if key == 'vocab_corpus3.txt':
        vocab_len_3 = '{:,}'.format(int(value))
    if key == 'vocab_total.txt':
        vocab_len = '{:,}'.format(int(value))
    if key == 'vocab_nonum_corpus1.txt':
        vocab_nonum_1 = '{:,}'.format(int(value))
    if key == 'vocab_nonum_corpus2.txt':
        vocab_nonum_2 = '{:,}'.format(int(value))
    if key == 'vocab_nonum_corpus3.txt':
        vocab_nonum_3 = '{:,}'.format(int(value))
    if key == 'vocab_nonum_total.txt':
        vocab_nonum = '{:,}'.format(int(value))
    if key == 'vocab_strict_corpus1.txt':
        vocab_strict_1 = '{:,}'.format(int(value))
    if key == 'vocab_strict_corpus2.txt':
        vocab_strict_2 = '{:,}'.format(int(value))
    if key == 'vocab_strict_corpus3.txt':
        vocab_strict_3 = '{:,}'.format(int(value))
    if key == 'vocab_strict_total.txt':
        vocab_strict = '{:,}'.format(int(value))

df2 = corpus_data.groupby("sub_corpus").agg({"tokens": sum})
df3 = df2["tokens"].map('{:,.0f}'.format).to_frame()
df3 = df3.assign(**{"types_all": [vocab_len_1, vocab_len_2, vocab_len_3],
                    "types_w/o_numbers": [vocab_nonum_1, vocab_nonum_2, vocab_nonum_3],
                    "types_strict": [vocab_strict_1, vocab_strict_2, vocab_strict_3]})
df3.loc["Total", "tokens"] = '{:,}'.format(int(df2["tokens"].sum()))
df3.loc["Total", "types_all"] = vocab_len
df3.loc["Total", "types_w/o_numbers"] = vocab_nonum
df3.loc["Total", "types_strict"] = vocab_strict


# write table with tokens and types counts only for sub-corpora and the whole corpus
df3.to_csv('./corpus_tokens_types.csv')
