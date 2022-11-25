# Code-switching detection in the Corpus of Early English Medical Writing

### Activate Environment
```console
conda env create -f environment.yml
```

```console
conda activate thesis_venv
```

### Pre-processing

#### Converting the .rtf files of the first sub-corpus (MEMT) to .txt
- Important: the input files for this script are not included in this repo due to space limit
- ./preprocessing/rtf_to_txt_converter.py 

```console
python3 ./preprocessing/rtf_to_txt_converter.py
```

#### Converting all the .txt files of all three sub-corpora to .xml
The following script extracts meta-information from the texts, clears the texts from annotations, applies sentence segmentation and tokenization, and structures the texts in XML format.
- Important: the input files for this script are not included in this repo due to space limit
- ./preprocessing/txt_to_xml_converter.py

```console
python3 ./preprocessing/txt_to_xml_converter.py
```

### Corpus profiling
The following script annotates the XML files with information regarding old alphabet characters, scribal abbreviations, roman and modern numerals, and generates the file called corpus_data.csv containing some statistical information regarding each text in the corpus. For practical reasons it also generates the vocabularies of each subcorpus separately and of the whole corpus in total using three approaches. In the first approach every type is considered for the generation of the vocabulary. In the second approach all numerals are ignored, and in the third approach all numerals are ignores and lower-casing is also applied to the words. The vocabulary files named vocab_no_num* belong to the second category, and the files named vocab_strict* belong to the third category.
- Important: the input files for this script are not included in this repo due to space limit
- ./corpus_profiling/profiler.py

```console
python3 ./corpus_profiling/profiler.py
```

#### Generation of table with tokens and types counts per file.
- ./corpus_profiling/create_token_type_table.py

```console
python3 ./corpus_profiling/create_token_type_table.py
```

#### Generation of bar charts for roman numerals, modern numerals, scribal abbreviations and old characters.
- ./corpus_profiling/plot_creator.py

```console
python3 ./corpus_profiling/plot_creator.py
```
### Trilingual Herb Glossary

#### Converting the glossary to JSON format
- ./corpus_profiling/herb_glossary_processor.py

```console
python3 ./corpus_profiling/herb_glossary_processor.py
```

#### Detecting herbs in the Corpus of Early English Medical Writing
- ./corpus_profiling/herb_glossary_detector.py

```console
python3 ./corpus_profiling/herb_glossary_detector.py
```

### Code-switching detection

#### Evaluation of language models
The files ./models/EN.txt and ./models/LA.txt include English and Latin sequences that
were manually collected from the corpus. 

The data are then split into training and testing using 5-folds. The training instances 
are located in the directory training_data and their corresponding testing instances are 
located in the directory testing_data. Right after, the sequences included in the files 
of the testing_data directory are truncated to certain lengths. The files with the new 
lengths are included in the corresponding 
directories, namely ./testing_data_len10, ./testing_data_len20, and ./testing_data_len40.

- ./models/get_train_test.py

```console
python3 ./models/get_train_test.py
```

##### Training and Evaluation of FurL

- ./models/furl/predict.py

```console
python3 ./models/furl/predict.py >> ./models/furl/acc_std_furl.txt
```

##### Evaluation of LangID 
- ./models/langid/apply_langid.py 

```console
python3 ./models/langid/apply_langid.py >> ./models/langid/acc_std_langid.txt
```

#### Lexicon-based approach

#### Inter-sentential code-switching detection (language identification of the corpus' sentences)
The language identification of the sentences depends on the agreement of the two language models, FurL and LangID. 
- ./sentence_level_lang_id.py

```console
export PYTHONPATH="${PYTHONPATH}:/mnt/c/Users/Irene/Desktop/DIGITAL_LINGUISTICS/master_thesis/thesis/models/furl"
```
```console
python3 ./sentence_level_lang_id.py
```
- output: 
  - sent_labeled_en.txt (English sentences)  
  - sent_labeled_la.txt (Latin sentences/inter-sentential code-switches)
  - sent_unlabeled.txt (Unlabeled sentences)

#### Generation of the English and Latin lexica
At this step, the lexica are also filtered. For the Latin lexicon the Latin Bible is used as additional material.
- ./create_lexicon.py

#### Intra-sentential code-switching detection
- ./intra_sentential_cs_detection.py

```console
python3 ./intra_sentential_cs_detection.py
```

- output:
  - intra_sent_cs_results_in_en_sentences.txt: intra-sentential code-switches within the sentences labeled as English by both language models, namely the sentences in sent_labeled_en.txt
  - intra_sent_cs_results_in_unk_sentences.txt: intra-sentential code-switches within the unlabeled sentences due to the disagreement of the language models, namely the sentences in sent_unlabeled.txt

#### Counting the code-switches
Sentences with at least one intra-sentential code-switch:
- in the English sentences
```console
grep "sentence" ./intra_sent_cs_results_in_en_sentences.txt | wc -l

1182
```
- in the unlabeled sentences
```console
grep "sentence" intra_sent_cs_results_in_unk_sentences.txt | wc -l

1275
```

Sentences that are inter-sentential code-switches:
```console
wc -l sent_labeled_la.txt

2721
```

