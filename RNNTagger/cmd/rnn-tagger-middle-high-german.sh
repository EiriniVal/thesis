#!/bin/sh

# Set these paths appropriately

BIN=./bin
SCRIPTS=./scripts
LIB=./lib
PyRNN=./PyRNN
PyNMT=./PyNMT
TMP=/tmp/rnn-tagger$$
LANGUAGE=middle-high-german

TOKENIZER="perl ${SCRIPTS}/tokenize.pl"
ABBR_LIST=${LIB}/Tokenizer/${LANGUAGE}-abbreviations
TAGGER="python3 $PyRNN/rnn-annotate.py"
RNNPAR=${LIB}/PyRNN/${LANGUAGE}
REFORMAT="perl ${SCRIPTS}/reformat.pl"
LEMMATIZER="python3 $PyNMT/nmt-translate.py"
NMTPAR=${LIB}/PyNMT/${LANGUAGE}
NORMPAR=${LIB}/PyNMT/${LANGUAGE}-norm

$TOKENIZER -a $ABBR_LIST $1 > $TMP.tok

$TAGGER $RNNPAR $TMP.tok > $TMP.tagged

$REFORMAT $TMP.tagged > $TMP.reformatted

$LEMMATIZER --print_source $NMTPAR $TMP.reformatted > $TMP.lemmas
$LEMMATIZER --print_source $NORMPAR $TMP.reformatted > $TMP.norm

$SCRIPTS/lemma-lookup.pl $TMP.lemmas $TMP.tagged | cut -f3 > $TMP.lemmatized
$SCRIPTS/lemma-lookup.pl $TMP.norm $TMP.tagged > $TMP.normalized

paste $TMP.normalized $TMP.lemmatized

rm $TMP.tok  $TMP.tagged  $TMP.reformatted $TMP.lemmas $TMP.normalized $TMP.lemmatized
