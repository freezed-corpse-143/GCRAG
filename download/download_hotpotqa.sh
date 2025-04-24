#!/bin/bash
# Code adapted from IRCoT project: https://github.com/StonyBrookNLP/ircot


# Configuration
DOWNLOAD_DIR="download/hotpotqa"

mkdir -p "$DOWNLOAD_DIR"

if [ ! -f "$DOWNLOAD_DIR/hotpot_train_v1.1.json" ]; then
    wget http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_train_v1.1.json \
         -O "$DOWNLOAD_DIR/hotpot_train_v1.1.json"
else
    echo "Training set already exists at $DOWNLOAD_DIR/hotpot_train_v1.1.json"
fi

if [ ! -f "$DOWNLOAD_DIR/hotpot_dev_distractor_v1.json" ]; then
    wget http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json \
         -O "$DOWNLOAD_DIR/hotpot_dev_distractor_v1.json"
else
    echo "Dev set already exists at $DOWNLOAD_DIR/hotpot_dev_distractor_v1.json"
fi

if [ ! -f "$DOWNLOAD_DIR/hotpot_dev_fullwiki_v1.json" ]; then
    wget http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_fullwiki_v1.json \
         -O "$DOWNLOAD_DIR/hotpot_dev_fullwiki_v1.json"
else
    echo "Dev set already exists at $DOWNLOAD_DIR/hotpot_dev_distractor_v1.json"
fi

if [ ! -f "$DOWNLOAD_DIR/hotpot_test_fullwiki_v1.json" ]; then
    wget http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_test_fullwiki_v1.json \
         -O "$DOWNLOAD_DIR/hotpot_test_fullwiki_v1.json"
else
    echo "Dev set already exists at $DOWNLOAD_DIR/hotpot_dev_distractor_v1.json"
fi

if [ ! -f "$DOWNLOAD_DIR/hotpot_evaluate_v1.py" ]; then
    wget https://raw.githubusercontent.com/hotpotqa/hotpot/master/hotpot_evaluate_v1.py -O "$DOWNLOAD_DIR/hotpot_evaluate_v1.py"
else
    echo "$DOWNLOAD_DIR/hotpot_evaluate_v1.py already exists"
fi

echo "Dataset download complete."
