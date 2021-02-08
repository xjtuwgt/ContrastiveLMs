#!/usr/bin/env bash

# DEFINE data related (please make changes according to your configurations)
# DATA ROOT folder where you put data files
DATA_ROOT=./data/
PROCS=${1:-"download"} # define the processes you want to run, e.g. "download,preprocess,train" or "preprocess" only

# Add current pwd to PYTHONPATH
export DIR_TMP="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$PYTHONPATH:$DIR_TMP:$DIR_TMP/hgntransformers
export PYTORCH_PRETRAINED_BERT_CACHE=$DATA_ROOT/models/pretrained_cache

mkdir -p $DATA_ROOT/models/pretrained_cache

# 0. Build Database from Wikipedia
download() {
    [[ -d $DATA_ROOT ]] || mkdir -p $DATA_ROOT/dataset/data_raw; mkdir -p $DATA_ROOT/knowledge

    wget -P $DATA_ROOT/dataset/data_raw/ http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_train_v1.1.json
    wget -P $DATA_ROOT/dataset/data_raw/ http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json
    wget -P $DATA_ROOT/dataset/data_raw http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_fullwiki_v1.json
    wget -P $DATA_ROOT/dataset/data_raw/ http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_test_fullwiki_v1.json
    if [[ ! -f $DATA_ROOT/knowledge/enwiki_ner.db ]]; then
        wget -P $DATA_ROOT/knowledge/ https://nlp.stanford.edu/projects/hotpotqa/enwiki-20171001-pages-meta-current-withlinks-abstracts.tar.bz2
        tar -xjvf $DATA_ROOT/knowledge/enwiki-20171001-pages-meta-current-withlinks-abstracts.tar.bz2 -C $DATA_ROOT/knowledge
        # Required: DrQA and Spacy
        python dataUtils/db_builder.py $DATA_ROOT/knowledge/enwiki-20171001-pages-meta-current-withlinks-abstracts $DATA_ROOT/knowledge/enwiki_ner.db
    fi
}

preprocess() {
  echo "1. Data Analysis of Database"
  echo $DATA_ROOT/knowledge/enwiki_ner.db
  # Input: enwiki_ner.db
  # Output: doc_link_ner.json
  python dataUtils/db_stat_infor.py --data_base $DATA_ROOT/knowledge/enwiki_ner.db
}

for proc in "download" "preprocess"
do
    if [[ ${PROCS:-"download"} =~ $proc ]]; then
        $proc
    fi
done
